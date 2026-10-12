"""Render an explicitly unillustrated, 32-page story and action-staging proof.

One source book page becomes one PDF page. The renderer uses no scene artwork,
does not infer actions from old crops, and fails rather than omitting prose.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DEFAULT_SCRIPT = HERE / "story_script.json"
DEFAULT_PDF = HERE / "output/pdf/Story_and_Action_Revision_32_Pages.pdf"
RENDER_DIR = ROOT / "tmp/pdfs/rumi_action_story_20261011"
W, H = 576.0, 720.0
LEFT, RIGHT, BOTTOM = 24.0, 552.0, 32.0
PENDING = "STORY-SCRIPT PROOF - ACTION ILLUSTRATION PENDING"
INK, MUTED, ACCENT, PAPER = "#243858", "#627481", "#467E86", "#FFFDF8"
COLORS = {"Roshan": "#AC4775", "Rumi": "#7953A2", "Hana": "#A85238", "Nari": "#397D79", "Duri": "#5C658C", "Magician Imp": "#70519C", "Performer Imp": "#86509A"}


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normal(text):
    return " ".join(text.split())


def words(text):
    return len(re.findall(r"\S+", text))


def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    records = []
    for name, filename in [("ProofText", "calibri.ttf"), ("ProofBold", "calibrib.ttf"), ("ProofItalic", "calibrii.ttf")]:
        path = Path("C:/Windows/Fonts") / filename
        pdfmetrics.registerFont(TTFont(name, str(path)))
        records.append({"name": name, "source": path.as_posix(), "sha256": file_sha(path)})
    pdfmetrics.registerFontFamily("ProofText", normal="ProofText", bold="ProofBold", italic="ProofItalic", boldItalic="ProofBold")
    return records


def render_pdf(pdf_path):
    from PIL import Image, ImageDraw, ImageFont
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    paths = [RENDER_DIR / f"page_{n:02}.png" for n in range(1, 33)]
    poppler = shutil.which("pdftoppm")
    if poppler:
        prefix = RENDER_DIR / "poppler_page"
        subprocess.run([poppler, "-png", "-r", "144", str(pdf_path), str(prefix)], check=True, capture_output=True)
        generated = sorted(RENDER_DIR.glob("poppler_page-*.png"))
        if len(generated) != 32:
            raise ValueError("Poppler did not render all 32 pages")
        for source, target in zip(generated, paths):
            source.replace(target)
        method = "Poppler pdftoppm, 144 dpi"
    else:
        import pypdfium2 as pdfium
        document = pdfium.PdfDocument(str(pdf_path))
        if len(document) != 32:
            raise ValueError("PDFium did not find 32 pages")
        for n, path in enumerate(paths):
            page = document[n]
            bitmap = page.render(scale=2)
            bitmap.to_pil().save(path)
            bitmap.close()
            page.close()
        document.close()
        method = "pypdfium2 fallback, 144 dpi; Poppler absent on PATH"
    font = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 22)
    contacts = []
    for sheet in range(4):
        contact = Image.new("RGB", (1410, 930), "#E8EDF1")
        draw = ImageDraw.Draw(contact)
        for position in range(8):
            index = sheet * 8 + position
            x, y = 18 + (position % 4) * 350, 18 + (position // 4) * 456
            with Image.open(paths[index]) as page_image:
                page_image.thumbnail((330, 412))
                contact.paste(page_image.convert("RGB"), (x, y))
            draw.text((x, y + 418), f"Page {index + 1}", fill=INK, font=font)
        path = RENDER_DIR / f"story_contact_{sheet + 1:02}.png"
        contact.save(path)
        contacts.append(path)
    records = [{"page": n + 1, "path": path.relative_to(ROOT).as_posix(), "sha256": file_sha(path), "dimensions": list(Image.open(path).size)} for n, path in enumerate(paths)]
    return method, records, [{"path": p.relative_to(ROOT).as_posix(), "sha256": file_sha(p)} for p in contacts]


def build(script_path=DEFAULT_SCRIPT, pdf_path=DEFAULT_PDF):
    from pypdf import PdfReader
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph

    script_path, pdf_path = Path(script_path).resolve(), Path(pdf_path).resolve()
    script_hash = file_sha(script_path)
    source = json.loads(script_path.read_text(encoding="utf-8"))
    pages = source["pages"]
    if len(pages) != 32 or [p["number"] for p in pages] != list(range(1, 33)):
        raise ValueError("Exactly 32 consecutively numbered source pages required")
    if pages[0]["kind"] != "cover" or pages[-1]["kind"] != "back" or any(p["kind"] != "story" for p in pages[1:-1]):
        raise ValueError("Page 1 cover, pages 2-31 story and page 32 back required")
    fonts = register_fonts()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H), pageCompression=1)
    c.setTitle(source["title"] + " - Story and action proof")
    c.setSubject("Revised manuscript and explicit sequential-action staging; action illustrations pending")
    text_records, page_records = [], []
    all_ids = []

    def paragraph(raw, style, width):
        p = Paragraph(raw, style)
        _, height = p.wrap(width, 10000)
        return p, height

    def page_layout(page, story_size, stage_size):
        body = ParagraphStyle("Dialogue", fontName="ProofText", fontSize=story_size, leading=story_size + 2.1, textColor=HexColor(INK))
        stage = ParagraphStyle("Staging", fontName="ProofItalic", fontSize=stage_size, leading=stage_size + 1.8, textColor=HexColor(MUTED))
        width = RIGHT - LEFT - 26
        blocks = []
        for index, panel in enumerate(page["panels"], 1):
            if not isinstance(panel.get("stage"), str) or not panel["stage"].strip():
                raise ValueError(f"Page {page['number']} panel {index}: explicit staging required")
            stage_p, stage_h = paragraph('<font name="ProofBold">STAGING: </font>' + escape(panel["stage"]).replace("\n", "<br/>"), stage, width)
            entries = []
            for entry in panel.get("entries", []):
                speaker, text = entry["speaker"], entry["text"]
                if not isinstance(text, str) or not text.strip():
                    raise ValueError("Empty manuscript entry")
                color = COLORS.get(speaker, INK)
                raw = '<font name="ProofBold" color="' + color + '">' + escape(speaker) + ': </font>' + escape(text).replace("\n", "<br/>")
                p, height = paragraph(raw, body, width)
                entries.append((entry, p, height))
            total = 13 + 3 + stage_h + (5 if entries else 0) + sum(h + 3 for _, _, h in entries) + 7
            blocks.append({"index": index, "id": str(panel["id"]), "stage": panel["stage"], "stage_p": stage_p, "stage_h": stage_h, "entries": entries, "height": total})
        return blocks

    for page in pages:
        if not 1 <= len(page["panels"]) <= 6:
            raise ValueError(f"Page {page['number']}: 1-6 authored panels required")
        ids = [str(p["id"]) for p in page["panels"]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Page {page['number']}: repeated panel identifier")
        all_ids.extend((page["number"], pid) for pid in ids)
        c.setFillColor(HexColor(PAPER))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(HexColor(ACCENT))
        c.setFont("ProofBold", 10.3)
        c.drawString(LEFT, 703, PENDING)
        title_style = ParagraphStyle("PageTitle", fontName="ProofBold", fontSize=19.5, leading=22, textColor=HexColor(INK))
        title_p, title_h = paragraph(escape(f"{page['number']:02}  {page['title']}"), title_style, RIGHT - LEFT)
        title_p.drawOn(c, LEFT, 684 - title_h)
        top = 684 - title_h - 7
        if page.get("sequence"):
            sequence_style = ParagraphStyle("Sequence", fontName="ProofText", fontSize=11.2, leading=13.2, textColor=HexColor(ACCENT))
            seq_p, seq_h = paragraph(escape(str(page["sequence"])), sequence_style, RIGHT - LEFT)
            seq_p.drawOn(c, LEFT, top - seq_h)
            top -= seq_h + 7
        c.setStrokeColor(HexColor("#A7B7BF"))
        c.setLineWidth(0.6)
        c.line(LEFT, top, RIGHT, top)
        top -= 10
        chosen = None
        for story_size, stage_size in [(13.4, 12.6), (13.2, 12.5), (13.0, 12.5), (12.8, 12.5), (12.5, 12.5)]:
            blocks = page_layout(page, story_size, stage_size)
            used = sum(b["height"] for b in blocks) + max(0, len(blocks) - 1) * 5
            if used <= top - BOTTOM + 0.01:
                chosen = blocks, story_size, stage_size, used
                break
        if chosen is None:
            raise ValueError(f"Page {page['number']}: manuscript/staging exceeds one page at 12.5 pt; revise source staging")
        blocks, story_size, stage_size, used = chosen
        gap = min(10.0, max(5.0, (top - BOTTOM - sum(b["height"] for b in blocks)) / max(1, len(blocks) - 1)))
        y = top
        page_checks = []
        for block in blocks:
            start = y
            c.setFillColor(HexColor(ACCENT))
            c.setFont("ProofBold", 11.2)
            c.drawString(LEFT, y - 10, f"{block['index']:02}")
            c.setFillColor(HexColor(INK))
            c.setFont("ProofBold", 10.5)
            c.drawString(LEFT + 26, y - 10, block["id"])
            y -= 16
            x, width = LEFT + 26, RIGHT - LEFT - 26
            block["stage_p"].drawOn(c, x, y - block["stage_h"])
            text_records.append({"page": page["number"], "panel_id": block["id"], "role": "staging", "text": block["stage"], "font_size_pt": stage_size, "bounds_points": [x, y - block["stage_h"], width, block["stage_h"]]})
            y -= block["stage_h"] + (5 if block["entries"] else 0)
            for entry, p, height in block["entries"]:
                p.drawOn(c, x, y - height)
                text_records.append({"page": page["number"], "panel_id": block["id"], "role": "manuscript", "speaker": entry["speaker"], "text": entry["text"], "font_size_pt": story_size, "bounds_points": [x, y - height, width, height]})
                y -= height + 3
            y -= 7
            c.setStrokeColor(HexColor("#CFD9DC"))
            c.setLineWidth(0.5)
            if block is not blocks[-1]:
                c.line(LEFT + 26, y + 2, RIGHT, y + 2)
            page_checks.append({"panel_id": block["id"], "top_points": start, "bottom_points": y, "height_points": start - y})
            y -= gap
        if any(t["bounds_points"][1] < BOTTOM - 0.1 for t in text_records if t["page"] == page["number"]):
            raise ValueError(f"Page {page['number']}: text overflow")
        c.setFont("ProofText", 9.5)
        c.setFillColor(HexColor(MUTED))
        c.drawString(LEFT, 15, "Revised story and staging - unillustrated review edition")
        c.drawRightString(RIGHT, 15, f"{page['number']} / 32")
        c.showPage()
        page_records.append({"page": page["number"], "kind": page["kind"], "title": page["title"], "panel_count": len(blocks), "story_font_size_pt": story_size, "staging_font_size_pt": stage_size, "content_height_points": used, "panel_sections": page_checks})
    c.save()
    reader = PdfReader(pdf_path)
    if len(reader.pages) != 32:
        raise ValueError("Rendered PDF page count is not 32")
    extraction = []
    for page in pages:
        extracted = normal(reader.pages[page["number"] - 1].extract_text())
        if PENDING not in extracted:
            raise ValueError("An actual PDF page omits artwork-pending status")
        position = 0
        for panel in page["panels"]:
            ordered = [panel["stage"]] + [e["speaker"] + ": " + e["text"] for e in panel.get("entries", [])]
            for raw in ordered:
                line = normal(raw)
                found = extracted.find(line, position)
                if found < 0:
                    raise ValueError(f"Missing or out-of-order PDF text on page {page['number']}: {raw}")
                position = found + len(line)
        extraction.append({"page": page["number"], "complete_staging_and_manuscript_in_source_order": True})
    for page in reader.pages:
        if abs(float(page.mediabox.width) - W) > .01 or abs(float(page.mediabox.height) - H) > .01:
            raise ValueError("Unexpected page size")
    if file_sha(script_path) != script_hash:
        raise ValueError("Source script changed during build")
    rendering_method, renders, contacts = render_pdf(pdf_path)
    if file_sha(script_path) != script_hash:
        raise ValueError("Source script changed while rendering; rebuild the exact new revision")
    check = {"status": "SCRIPT_PROOF_MACHINE_VERIFIED_VISUAL_REVIEW_REQUIRED", "title": source["title"], "source_status": source.get("status"),
             "artifact_type": "revised manuscript and sequential-action staging proof", "action_illustration_pending": True, "source_artwork_used": False,
             "acceptance_limits": "No new action illustration, illustrated-book, runtime, cinematic, owner, child or print acceptance is claimed.",
             "pdf": pdf_path.relative_to(ROOT).as_posix(), "pdf_sha256": file_sha(pdf_path), "pdf_byte_length": pdf_path.stat().st_size,
             "script": script_path.relative_to(ROOT).as_posix(), "script_sha256": script_hash, "builder_sha256": file_sha(Path(__file__)), "font_provenance": fonts,
             "actual_pdf_pages": len(reader.pages), "format_points": [W, H], "panel_count": len(all_ids), "story_panel_count": sum(len(p["panels"]) for p in pages[1:-1]),
             "story_word_count": sum(words(e["text"]) for p in pages[1:-1] for a in p["panels"] for e in a.get("entries", [])),
             "staging_word_count": sum(words(a["stage"]) for p in pages for a in p["panels"]), "all_source_text_preserved_in_order": True,
             "all_text_within_page_bounds": True, "minimum_story_font_size_pt": min(p["story_font_size_pt"] for p in page_records),
             "minimum_staging_font_size_pt": min(p["staging_font_size_pt"] for p in page_records), "page_layout": page_records, "text_bounds": text_records,
             "extraction_checks": extraction, "rendering_method": rendering_method, "rendered_page_count": len(renders), "rendered_pages": renders, "contact_sheets": contacts}
    verification = HERE / "verification"
    verification.mkdir(parents=True, exist_ok=True)
    (verification / "story_proof_check.json").write_text(json.dumps(check, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"STORY_PROOF_OK pages=32 panels={check['panel_count']} story_words={check['story_word_count']} sha256={check['pdf_sha256']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    build(args.script, args.pdf)
