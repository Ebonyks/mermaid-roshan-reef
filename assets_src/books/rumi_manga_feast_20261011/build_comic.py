"""Render the 32-page manga review edition from explicitly staged panels.

The script owns every crop, page rectangle and lettering anchor. This builder
does not invent crops, stretch artwork, modify sources or add runtime assets.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DEFAULT_SCRIPT = HERE / "comic_script.json"
DEFAULT_PDF = HERE / "output/pdf/Mermaid_Roshan_Song_Beneath_the_Pool_Manga_32_Pages.pdf"
W, H = 576.0, 720.0
FONT_SIZE, LEADING = 13.4, 15.7
INK, PAPER = "#243858", "#FFFDF8"
COLORS = {"Roshan": "#AC4775", "Rumi": "#7953A2", "Hana": "#A85238", "Nari": "#397D79", "Duri": "#5C658C", "Narrator": "#465F73", "Magician Imp": "#70519C", "Performer Imp": "#86509A", "Trio": "#55797B", "Everyone": "#55797B"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    return sha(path.read_bytes())


def normalize(text):
    return " ".join(text.split())


def resolve_source(raw):
    path = (ROOT / raw.replace("\\", "/")).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError(f"Missing or out-of-repository image: {raw}")
    return path


def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    records = []
    for name, filename in [("MangaText", "calibri.ttf"), ("MangaBold", "calibrib.ttf"), ("MangaItalic", "calibrii.ttf"), ("MangaTitle", "georgiab.ttf")]:
        path = Path("C:/Windows/Fonts") / filename
        pdfmetrics.registerFont(TTFont(name, str(path)))
        records.append({"name": name, "source": path.as_posix(), "sha256": file_sha(path)})
    pdfmetrics.registerFontFamily("MangaText", normal="MangaText", bold="MangaBold", italic="MangaItalic", boldItalic="MangaBold")
    return records


def build(script_path=DEFAULT_SCRIPT, pdf_path=DEFAULT_PDF, render=True):
    from PIL import Image, ImageDraw, ImageFont
    from pypdf import PdfReader
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph

    script = json.loads(script_path.read_text(encoding="utf-8"))
    script_hash = file_sha(script_path)
    pages = script["pages"]
    if len(pages) != 32 or [p["number"] for p in pages] != list(range(1, 33)):
        raise ValueError("Exactly 32 actual consecutively numbered pages required")
    if pages[0]["kind"] != "cover" or pages[-1]["kind"] != "back" or any(p["kind"] != "story" for p in pages[1:-1]):
        raise ValueError("Cover, 30 story pages and back required")
    fonts = register_fonts()
    base_style = ParagraphStyle("MangaDialogue", fontName="MangaText", fontSize=FONT_SIZE, leading=LEADING, textColor=HexColor(INK))
    narrator_style = ParagraphStyle("MangaNarration", parent=base_style, fontName="MangaItalic", textColor=HexColor(COLORS["Narrator"]))
    title_style = ParagraphStyle("MangaTitle", parent=base_style, fontName="MangaTitle", fontSize=28, leading=32, alignment=1)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    verification = HERE / "verification"
    verification.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H), pageCompression=1)
    c.setTitle(script["title"])
    c.setAuthor("Mermaid Roshan story project")
    c.setSubject("32-page manga review book; authored crops, English balloons, original artwork preserved")
    c.setCreator("build_comic.py / explicit manga page script")
    cache, sources, panel_records, text_records = {}, {}, [], []

    def art(panel):
        path = resolve_source(panel["art"])
        crop = panel.get("crop", [0, 0, 1, 1])
        if len(crop) != 4 or not (0 <= crop[0] < crop[2] <= 1 and 0 <= crop[1] < crop[3] <= 1):
            raise ValueError(f"Invalid crop: {crop}")
        key = (path.as_posix(), tuple(crop))
        if key not in cache:
            with Image.open(path) as source:
                pixels = [round(crop[0] * source.width), round(crop[1] * source.height), round(crop[2] * source.width), round(crop[3] * source.height)]
                cropped = source.crop(pixels).convert("RGB")
                payload = io.BytesIO()
                cropped.save(payload, "JPEG", quality=95, subsampling=0, optimize=True)
                data = payload.getvalue()
                record = {"source": path.relative_to(ROOT).as_posix(), "source_sha256": file_sha(path), "source_dimensions": list(source.size),
                          "crop_normalized": crop, "crop_pixels": pixels, "cropped_dimensions": list(cropped.size),
                          "embedding": {"format": "JPEG", "quality": 95, "subsampling": 0, "resize": False, "sha256": sha(data), "byte_length": len(data)}}
                cache[key] = ImageReader(io.BytesIO(data)), cropped.size, record
                sources[record["source"]] = {"sha256": record["source_sha256"], "dimensions": record["source_dimensions"]}
        return cache[key]

    def page_rect(rect):
        x, y, width, height = rect
        if not (0 <= x < 1 and 0 <= y < 1 and width > 0 and height > 0 and x + width <= 1.00001 and y + height <= 1.00001):
            raise ValueError(f"Invalid page rectangle: {rect}")
        return x * W, (1 - y - height) * H, width * W, height * H

    def lettering(page_number, panel_index, entry, rect):
        px, py, pw, ph = rect
        speaker, line = entry.get("speaker", "Narrator"), entry["line"]
        anchor = entry.get("box")
        if anchor is None:
            raise ValueError(f"Missing authored lettering anchor page{page_number}/panel{panel_index}: {line}")
        ax, ay, aw, ah = anchor
        if not (0 <= ax and 0 <= ay and aw > 0 and ah > 0 and ax + aw <= 1.00001 and ay + ah <= 1.00001):
            raise ValueError(f"Lettering box outside panel: {anchor}")
        x, top, width, available_height = px + ax * pw, py + (1 - ay) * ph, aw * pw, ah * ph
        role = entry.get("role", "caption" if speaker == "Narrator" else "speech")
        style = title_style if role == "title" else narrator_style if speaker == "Narrator" else base_style
        show_label = entry.get("show_speaker", False)
        label = "" if speaker == "Narrator" or role == "title" or not show_label else '<font name="MangaBold" color="' + COLORS.get(speaker, "#55797B") + '">' + escape(speaker) + ": </font>"
        p = Paragraph(label + escape(line).replace("\n", "<br/>"), style)
        padding_x, padding_y = (8, 5) if role == "speech" else (5, 3)
        actual_width, paragraph_height = p.wrap(width - 2 * padding_x, 10000)
        actual_height = paragraph_height + 2 * padding_y
        if actual_height > available_height + 0.25:
            raise ValueError(f"Lettering overflow page{page_number}/panel{panel_index}: {actual_height:.1f}>{available_height:.1f}: {line}")
        if entry.get("align") == "bottom":
            top -= available_height - actual_height
        bottom = top - actual_height
        c.setFillColor(HexColor("#FFFFFF" if role == "speech" else "#FFF8E9"))
        c.setStrokeColor(HexColor(INK))
        c.setLineWidth(0.8)
        if role == "speech":
            c.roundRect(x, bottom, width, actual_height, actual_height / 2, fill=1, stroke=1)
            if entry.get("tail"):
                tx, ty = entry["tail"]
                target_x, target_y = px + tx * pw, py + (1 - ty) * ph
                # A target inside the balloon has no outward tail. Drawing one
                # across the paragraph would conceal already-typeset letters.
                if not (x <= target_x <= x + width and bottom <= target_y <= top):
                    tip = c.beginPath()
                    origin_x = min(max(target_x, x + 10), x + width - 10)
                    origin_y = bottom if target_y <= bottom else top
                    tip.moveTo(origin_x - 5, origin_y)
                    tip.lineTo(target_x, target_y)
                    tip.lineTo(origin_x + 5, origin_y)
                    tip.close()
                    c.drawPath(tip, fill=1, stroke=1)
        else:
            c.rect(x, bottom, width, actual_height, fill=1, stroke=1)
        p.drawOn(c, x + padding_x, bottom + padding_y)
        within = x >= px - 0.1 and x + width <= px + pw + 0.1 and bottom >= py - 0.1 and top <= py + ph + 0.1
        text_records.append({"page": page_number, "panel": panel_index, "speaker": speaker, "line": line, "role": role,
                             "authored_anchor_normalized": anchor, "actual_box_points": [x, bottom, width, actual_height],
                             "paragraph_points": [x + padding_x, bottom + padding_y, actual_width, paragraph_height],
                             "font_size_pt": style.fontSize, "speaker_label_rendered": show_label, "within_panel": within, "safe_anchor_note": entry.get("safe_anchor_note", "Authored image region; visual review required")})

    for page in pages:
        if not 1 <= len(page["panels"]) <= 5:
            raise ValueError(f"Page{page['number']}:1-5 panels required")
        c.setFillColor(HexColor(PAPER))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        for index, panel in enumerate(page["panels"], 1):
            rect = page_rect(panel["rect"])
            x, y, width, height = rect
            reader, dimensions, record = art(panel)
            caption_top = panel.get("lettering_top_pt", 0)
            caption_bottom = panel.get("lettering_bottom_pt", 0)
            image_height = height - caption_top - caption_bottom
            if image_height <= 0:
                raise ValueError("Lettering lanes leave no illustration")
            ratio = min(width / dimensions[0], image_height / dimensions[1])
            actual_width, actual_height = dimensions[0] * ratio, dimensions[1] * ratio
            actual = [x + (width - actual_width) / 2, y + caption_bottom + (image_height - actual_height) / 2, actual_width, actual_height]
            coverage = actual_width * actual_height / (width * image_height)
            if coverage < panel.get("minimum_coverage", 0.86):
                raise ValueError(f"Page{page['number']}/panel{index}: excessive image containment {coverage:.3f}; author crop or rectangle")
            c.setFillColor(HexColor("#EAF3F2"))
            c.rect(x, y, width, height, fill=1, stroke=0)
            c.drawImage(reader, *actual, preserveAspectRatio=True)
            c.setStrokeColor(HexColor(INK))
            c.setLineWidth(1.05)
            c.rect(x, y, width, height, fill=0, stroke=1)
            panel_records.append({"page": page["number"], "panel": index, "rect_points": list(rect), "reading_order": index,
                                  "purpose": panel.get("purpose", "Original story action"), "art": {**record, "placed_image_points": actual,
                                  "art_area_coverage_fraction": round(coverage, 5), "caption_top_points": caption_top,
                                  "caption_bottom_points": caption_bottom, "fit": "contain declared crop only; no distortion or automatic clipping"},
                                  "text": panel.get("text", [])})
            for entry in panel.get("text", []):
                lettering(page["number"], index, entry, rect)
        if page["kind"] == "story":
            c.setFillColor(HexColor(INK))
            c.setFont("MangaText", 9)
            c.drawCentredString(W / 2, 5, str(page["number"]))
        c.showPage()
    c.save()

    collisions = []
    for i, first in enumerate(text_records):
        for second in text_records[i + 1:]:
            if first["page"] != second["page"]:
                continue
            ax, ay, aw, ah = first["actual_box_points"]
            bx, by, bw, bh = second["actual_box_points"]
            dx = min(ax + aw, bx + bw) - max(ax, bx)
            dy = min(ay + ah, by + bh) - max(ay, by)
            if dx > 1 and dy > 1:
                collisions.append({"page": first["page"], "first": first["line"], "second": second["line"], "overlap_points": [dx, dy]})
    if collisions:
        raise ValueError("Visible lettering collision: " + json.dumps(collisions, ensure_ascii=False))

    page_fill = []
    for page in pages:
        records = [p for p in panel_records if p["page"] == page["number"]]
        frame_area = sum(p["rect_points"][2] * p["rect_points"][3] for p in records)
        image_area = sum(p["art"]["placed_image_points"][2] * p["art"]["placed_image_points"][3] for p in records)
        # All authored panels are disjoint. Sample the content area to also
        # expose large unframed holes hidden by per-panel containment checks.
        largest_empty_row = current = 0
        for scan_y in range(16, 704):
            covered = sum(p["rect_points"][2] for p in records if p["rect_points"][1] <= scan_y < p["rect_points"][1] + p["rect_points"][3])
            current = current + 1 if covered < 100 else 0
            largest_empty_row = max(largest_empty_row, current)
        page_fill.append({"page": page["number"], "frame_area_fraction_of_content": round(frame_area / (544 * 688), 5),
                          "image_area_fraction_of_content": round(image_area / (544 * 688), 5), "largest_nearly_empty_horizontal_band_pt": largest_empty_row})
    if any(p["frame_area_fraction_of_content"] < 0.82 or p["largest_nearly_empty_horizontal_band_pt"] > 30 for p in page_fill):
        raise ValueError("Page-wide geometry hole: " + json.dumps([p for p in page_fill if p["frame_area_fraction_of_content"] < 0.82 or p["largest_nearly_empty_horizontal_band_pt"] > 30]))

    reader = PdfReader(pdf_path)
    extracted = [normalize(p.extract_text() or "") for p in reader.pages]
    missing = []
    for page in pages:
        for panel in page["panels"]:
            for entry in panel.get("text", []):
                if normalize(entry["line"]) not in extracted[page["number"] - 1]:
                    missing.append({"page": page["number"], "line": entry["line"]})
    if len(reader.pages) != 32 or missing or not all(t["within_panel"] for t in text_records):
        raise ValueError(f"PDF page/text/bounds check failed: missing={missing}")
    for path, record in sources.items():
        if file_sha(ROOT / path) != record["sha256"]:
            raise ValueError(f"Source changed during build: {path}")
    if file_sha(script_path) != script_hash:
        raise ValueError("Script changed during build; rerun after source freeze")
    source_lines = script.get("preserved_story_lines", [])
    assembled_lines = [entry["line"] for p in pages if p["kind"] == "story" for panel in p["panels"] for entry in panel.get("text", [])]
    assembled_text = normalize(" ".join(assembled_lines))
    original_text = normalize(" ".join(source_lines))
    if source_lines and assembled_text != original_text:
        raise ValueError("Original story words/order changed during panel redistribution")
    check = {"status": "PASS", "pdf": pdf_path.relative_to(ROOT).as_posix(), "pdf_sha256": file_sha(pdf_path), "pdf_byte_length": pdf_path.stat().st_size,
             "actual_pdf_pages": 32, "format": "8 x 10 inches;576 x720pt;16pt outer margins;6pt gutters;English manga reading order",
             "script": script_path.relative_to(ROOT).as_posix(), "script_sha256": script_hash, "fonts": fonts,
             "panel_count": len(panel_records), "story_panel_count": sum(p["kind"] == "story" for p in pages for _ in p["panels"]),
             "story_word_count": len(re.findall(r"\b[\w'-]+\b", assembled_text)), "text_entry_count": len(text_records),
             "all_script_lines_extract_completely": not missing, "all_text_within_panel_bounds": True,
             "no_visible_text_box_collisions": not collisions, "page_fill_review_metrics": page_fill,
             "original_story_words_and_order_preserved": assembled_text == original_text if source_lines else "No source baseline supplied",
             "minimum_story_font_size_pt": FONT_SIZE, "minimum_art_area_coverage_fraction": min(p["art"]["art_area_coverage_fraction"] for p in panel_records),
             "source_files": sources, "panels": panel_records, "text_bounds": text_records,
             "encoding": "Source pixels preserved; declared normalized crops;separate RGB JPEG95/subsampling0 encodings without resize",
             "acceptance_limits": "Machine page/text/anchor/hash checks are separate from exact visual/art/narrative/owner/child review. No runtime or print-production acceptance."}
    if render:
        import pypdfium2
        destination = ROOT / "tmp/pdfs/rumi_manga_feast_20261011"
        destination.mkdir(parents=True, exist_ok=True)
        document = pypdfium2.PdfDocument(str(pdf_path))
        paths = []
        for index in range(len(document)):
            page = document[index]
            bitmap = page.render(scale=2)
            path = destination / f"page_{index + 1:02d}.png"
            bitmap.to_pil().convert("RGB").save(path)
            paths.append(path)
            bitmap.close()
            page.close()
        document.close()
        font = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 18)
        sheets = []
        for group in range(4):
            sheet = Image.new("RGB", (1410, 930), "#E7EDF2")
            draw = ImageDraw.Draw(sheet)
            for offset in range(8):
                i = group * 8 + offset
                x, y = 18 + offset % 4 * 348, 18 + offset // 4 * 455
                with Image.open(paths[i]) as image:
                    thumb = image.copy()
                    thumb.thumbnail((330, 413), Image.Resampling.LANCZOS)
                    sheet.paste(thumb, (x, y))
                draw.text((x, y + 416), f"Page{i + 1}", font=font, fill=INK)
            path = verification / f"pdf_contact_{group + 1:02d}.png"
            sheet.save(path)
            sheets.append({"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha(path), "pages": list(range(group * 8 + 1, group * 8 + 9))})
        check["contact_sheets"] = sheets
        check["rendered_page_count"] = 32
        check["render_directory_ignored"] = destination.relative_to(ROOT).as_posix()
    (verification / "book_check.json").write_text(json.dumps(check, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"MANGA_BOOK_OK pages=32 panels={len(panel_records)} story_words={check['story_word_count']} pdf_bytes={check['pdf_byte_length']} sha256={check['pdf_sha256']}")
    return check


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    build(args.script.resolve(), args.output.resolve(), not args.no_render)
