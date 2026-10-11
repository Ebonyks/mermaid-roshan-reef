"""Build and verify the exact 32-page under-pool comic review book.

Artwork is read from repository sources. Crops, PDF encodings and page/panel
mapping are recorded; native source files are never changed. This builder does
not update licenses, audit impacts, source-generation manifests or runtime art.
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
DEFAULT_PDF = HERE / "output/pdf/Mermaid_Roshan_Song_Beneath_the_Pool_32_Pages.pdf"
W = 576.0
H = 720.0
MARGIN = 22.0
GUTTER = 9.0
PAGE_TOP = H - MARGIN
PAGE_BOTTOM = 29.0
FONT_SIZE = 13.4
LEADING = 15.7
INK = "#243858"
CREAM = "#FFF8EB"
SPEAKER_COLORS = {
    "Roshan": "#AC4775", "Rumi": "#7953A2", "Hana": "#A85238",
    "Nari": "#397D79", "Duri": "#5C658C", "Narrator": "#465F73",
    "Performer Imp": "#86509A", "Magician Imp": "#70519C",
    "Imp": "#86509A", "Imps": "#86509A", "Everyone": "#55797B",
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def normalized_text(text: str) -> str:
    return " ".join(text.split())


def source_path(raw: str) -> Path:
    path = (ROOT / raw.replace("\\", "/")).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"Art path is outside repository: {raw}")
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    choices = {
        "ComicText": ["C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/arial.ttf"],
        "ComicBold": ["C:/Windows/Fonts/calibrib.ttf", "C:/Windows/Fonts/arialbd.ttf"],
        "ComicItalic": ["C:/Windows/Fonts/calibrii.ttf", "C:/Windows/Fonts/ariali.ttf"],
        "BookTitle": ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/calibrib.ttf"],
    }
    records = []
    for name, candidates in choices.items():
        path = next((Path(p) for p in candidates if Path(p).is_file()), None)
        if path is None:
            raise FileNotFoundError(f"No embedded font available for {name}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
        records.append({"name": name, "source": path.as_posix(), "sha256": sha_file(path)})
    pdfmetrics.registerFontFamily("ComicText", normal="ComicText", bold="ComicBold", italic="ComicItalic", boldItalic="ComicBold")
    return records


def page_rectangles(count: int, layout: str = "stack"):
    available = PAGE_TOP - PAGE_BOTTOM
    width = W - 2 * MARGIN
    if count == 2 and layout == "pair":
        panel_width = (width - GUTTER) / 2
        return [
            (MARGIN, PAGE_BOTTOM, panel_width, available),
            (MARGIN + panel_width + GUTTER, PAGE_BOTTOM, panel_width, available),
        ]
    if count == 3 and layout == "hero_pair":
        top_height = (available - GUTTER) * 0.57
        bottom_height = available - GUTTER - top_height
        bottom_width = (width - GUTTER) / 2
        return [
            (MARGIN, PAGE_TOP - top_height, width, top_height),
            (MARGIN, PAGE_BOTTOM, bottom_width, bottom_height),
            (MARGIN + bottom_width + GUTTER, PAGE_BOTTOM, bottom_width, bottom_height),
        ]
    if layout != "stack":
        raise ValueError(f"Unsupported page layout: {layout}")
    height = (available - GUTTER * (count - 1)) / count
    return [(MARGIN, PAGE_TOP - (index + 1) * height - index * GUTTER, width, height) for index in range(count)]


def build(script_path: Path, pdf_path: Path, render: bool = True):
    from PIL import Image, ImageDraw, ImageFont
    from pypdf import PdfReader
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph

    script = json.loads(script_path.read_text(encoding="utf-8"))
    pages = script.get("pages", [])
    if len(pages) != 32 or [p.get("number") for p in pages] != list(range(1, 33)):
        raise ValueError("Book must have exactly 32 consecutively numbered actual PDF pages")
    if pages[0].get("kind") != "cover" or pages[-1].get("kind") != "back":
        raise ValueError("Page 1 must be cover; page 32 must be back")
    if any(p.get("kind") != "story" for p in pages[1:-1]):
        raise ValueError("Pages 2-31 must be story pages")
    for page in pages:
        if not 1 <= len(page.get("panels", [])) <= 3:
            raise ValueError(f"Page {page['number']} must contain 1-3 panels")

    fonts = register_fonts()
    text_style = ParagraphStyle("Dialogue", fontName="ComicText", fontSize=FONT_SIZE, leading=LEADING, textColor=HexColor(INK), spaceAfter=0)
    narrator_style = ParagraphStyle("Narration", parent=text_style, fontName="ComicItalic", textColor=HexColor(SPEAKER_COLORS["Narrator"]))
    title_style = ParagraphStyle("Title", fontName="BookTitle", fontSize=31, leading=37, alignment=1, textColor=HexColor(INK))
    subtitle_style = ParagraphStyle("Subtitle", parent=text_style, alignment=1, fontSize=15.5, leading=19)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    verification = HERE / "verification"
    verification.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H), pageCompression=1)
    c.setTitle(script.get("title", "Mermaid Roshan and the Song Beneath the Pool"))
    c.setAuthor("Mermaid Roshan story project")
    c.setSubject("Exact 32-page comic book review candidate, 8 x 10 inches; original artwork preserved")
    c.setCreator("Project-authored comic script and build_comic.py")
    artwork_cache = {}
    source_records = {}
    panels_out = []
    text_bounds = []

    def paragraph(text, style, width):
        p = Paragraph(text, style)
        pw, ph = p.wrap(width, 10000)
        return p, pw, ph

    def artwork(panel):
        path = source_path(panel["art"])
        crop = panel.get("crop", [0.0, 0.0, 1.0, 1.0])
        if len(crop) != 4 or any(not isinstance(v, (int, float)) for v in crop):
            raise ValueError(f"Invalid normalized crop: {crop}")
        x0, y0, x1, y1 = crop
        if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            raise ValueError(f"Crop is outside source bounds: {crop}")
        key = (path.as_posix(), tuple(crop))
        if key not in artwork_cache:
            with Image.open(path) as source:
                dimensions = source.size
                pixels = (round(x0 * source.width), round(y0 * source.height), round(x1 * source.width), round(y1 * source.height))
                if pixels[2] <= pixels[0] or pixels[3] <= pixels[1]:
                    raise ValueError(f"Empty pixel crop: {crop}")
                image = source.crop(pixels).convert("RGB")
                encoded = io.BytesIO()
                image.save(encoded, format="JPEG", quality=95, subsampling=0, optimize=True)
                payload = encoded.getvalue()
                record = {
                    "source": path.relative_to(ROOT).as_posix(), "source_sha256": sha_file(path),
                    "source_dimensions": list(dimensions), "crop_normalized": list(crop),
                    "crop_pixels": list(pixels), "cropped_dimensions": list(image.size),
                    "embedding": {"format": "JPEG", "quality": 95, "subsampling": 0, "optimize": True,
                                  "resize": False, "sha256": sha_bytes(payload), "byte_length": len(payload)},
                }
                artwork_cache[key] = (ImageReader(io.BytesIO(payload)), image.size, record)
                source_records[path.relative_to(ROOT).as_posix()] = {"sha256": record["source_sha256"], "dimensions": list(dimensions)}
        return artwork_cache[key]

    def paint_art(panel, rect):
        x, y, width, height = rect
        reader, size, record = artwork(panel)
        ratio = min(width / size[0], height / size[1])
        aw, ah = size[0] * ratio, size[1] * ratio
        actual = (x + (width - aw) / 2, y + (height - ah) / 2, aw, ah)
        c.drawImage(reader, *actual, preserveAspectRatio=True, mask="auto")
        return {**record, "art_box_points": list(rect), "placed_image_points": list(actual),
                "art_area_coverage_fraction": round(aw * ah / (width * height), 5),
                "fit": "contain; no distortion, no additional crop"}

    def prepared_lines(panel, width):
        prepared = []
        for entry in panel.get("text", []):
            speaker = str(entry.get("speaker", "Narrator"))
            line = str(entry.get("line", "")).strip()
            if not line:
                raise ValueError("Panel text entries must be nonempty")
            color = SPEAKER_COLORS.get(speaker, "#55797B")
            if speaker == "Narrator":
                markup = escape(line).replace("\n", "<br/>")
                style = narrator_style
            else:
                markup = '<font name="ComicBold" color="' + color + '">' + escape(speaker) + ": </font>" + escape(line).replace("\n", "<br/>")
                style = text_style
            p, pw, ph = paragraph(markup, style, width - 20)
            prepared.append((entry, speaker, p, pw, ph, color))
        return prepared

    def draw_panel(page, panel_index, panel, rect):
        x, y, width, height = rect
        lines = prepared_lines(panel, width - 12)
        band = 14 + sum(item[4] + 10 for item in lines) if lines else 0
        # Portrait side-by-side rescue crops and the cast back page should have
        # their frame around the artwork, rather than tall empty painted bands.
        # This changes only page geometry; the complete declared crop is kept.
        if page.get("layout") == "pair" or page.get("kind") == "back":
            _reader, image_size, _record = artwork(panel)
            fitted_height = (width - 8) * image_size[1] / image_size[0] + band + 8
            if fitted_height < height:
                y += (height - fitted_height) / 2
                height = fitted_height
                rect = (x, y, width, height)
        art_height = height - band - 8
        if art_height < 64 or (lines and band >= height * 0.65):
            raise ValueError(f"Page {page['number']} panel {panel_index}: text leaves insufficient art ({art_height:.1f}pt)")
        c.setFillColor(HexColor("#EEF5F2"))
        c.roundRect(x, y, width, height, 9, fill=1, stroke=0)
        clip = c.beginPath()
        clip.roundRect(x + 1.5, y + 1.5, width - 3, height - 3, 7.5)
        c.saveState()
        c.clipPath(clip, stroke=0, fill=0)
        art_record = paint_art(panel, (x + 4, y + band + 4, width - 8, art_height))
        if lines:
            c.setFillColor(HexColor(CREAM))
            c.rect(x + 1, y + 1, width - 2, band + 1, fill=1, stroke=0)
        c.restoreState()
        cursor = y + band - 7
        for entry, speaker, p, pw, ph, color in lines:
            bx, by, bw, bh = x + 7, cursor - ph - 5, width - 14, ph + 10
            c.setFillColor(HexColor("#FFFDF8" if speaker != "Narrator" else "#FFF3D9"))
            c.setStrokeColor(HexColor(color if speaker != "Narrator" else "#E0CFAB"))
            c.setLineWidth(0.55)
            c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=1)
            p.drawOn(c, bx + 9, by + 5)
            text_bounds.append({"page": page["number"], "panel": panel_index, "speaker": speaker, "line": entry["line"],
                                "font_size_pt": FONT_SIZE, "leading_pt": LEADING, "box_points": [bx, by, bw, bh],
                                "paragraph_points": [bx + 9, by + 5, pw, ph], "within_panel": by >= y and by + bh <= y + height})
            cursor = by - 5
        c.setStrokeColor(HexColor(INK))
        c.setLineWidth(1.4)
        c.roundRect(x, y, width, height, 9, fill=0, stroke=1)
        panels_out.append({"page": page["number"], "panel": panel_index, "rect_points": list(rect),
                           "art": art_record, "dialogue_band_height_pt": band, "text": panel.get("text", [])})

    def draw_cover(page):
        title = page.get("display_title", script.get("title", "Mermaid Roshan and the Song Beneath the Pool"))
        p, pw, ph = paragraph(escape(title).replace("\n", "<br/>"), title_style, W - 60)
        if ph > 135:
            raise ValueError("Cover title is too tall")
        p.drawOn(c, 30, H - 28 - ph)
        title_bottom = H - 40 - ph
        cover_panel = page["panels"][0]
        x, y, width, height = 22.0, 88.0, W - 44, title_bottom - 88
        _reader, image_size, _record = artwork(cover_panel)
        fitted_height = (width - 12) * image_size[1] / image_size[0] + 12
        if fitted_height < height:
            y += (height - fitted_height) / 2
            height = fitted_height
        c.setFillColor(HexColor("#EEF5F2"))
        c.roundRect(x, y, width, height, 12, fill=1, stroke=0)
        record = paint_art(cover_panel, (x + 6, y + 6, width - 12, height - 12))
        c.setStrokeColor(HexColor(INK))
        c.setLineWidth(1.5)
        c.roundRect(x, y, width, height, 12, fill=0, stroke=1)
        panels_out.append({"page": 1, "panel": 1, "rect_points": [x, y, width, height], "art": record, "text": cover_panel.get("text", [])})
        entries = cover_panel.get("text", [])
        subtitle = "\n".join(e["line"] for e in entries) or page.get("subtitle", "Rumi's undersea adventure")
        p, pw, ph = paragraph(escape(subtitle).replace("\n", "<br/>"), subtitle_style, W - 80)
        if ph > 50:
            raise ValueError("Cover subtitle overflows")
        p.drawOn(c, 40, 68 - ph)
        for entry in entries:
            text_bounds.append({"page": 1, "panel": 1, "speaker": entry.get("speaker", "Narrator"), "line": entry["line"],
                                "font_size_pt": 15.5, "within_panel": True, "placement": "cover subtitle"})

    for page in pages:
        c.setFillColor(HexColor(CREAM))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        if page["kind"] == "cover":
            if len(page["panels"]) != 1:
                raise ValueError("Cover has one art panel")
            draw_cover(page)
        else:
            rectangles = page_rectangles(len(page["panels"]), page.get("layout", "stack"))
            for i, (panel, rect) in enumerate(zip(page["panels"], rectangles), 1):
                draw_panel(page, i, panel, rect)
            c.setFont("ComicText", 10)
            c.setFillColor(HexColor("#7186A2"))
            c.drawCentredString(W / 2, 13, str(page["number"]))
        c.showPage()
    c.save()

    reader = PdfReader(str(pdf_path))
    extracted_pages = [normalized_text(p.extract_text() or "") for p in reader.pages]
    missing = []
    for page in pages:
        for panel in page["panels"]:
            for entry in panel.get("text", []):
                expected = normalized_text(entry["line"])
                if expected not in extracted_pages[page["number"] - 1]:
                    missing.append({"page": page["number"], "line": entry["line"]})
    if len(reader.pages) != 32 or missing or any(not r["within_panel"] for r in text_bounds):
        raise ValueError(f"PDF verification failed: pages={len(reader.pages)}, missing={missing}")
    if any(abs(float(p.mediabox.width) - W) > 0.01 or abs(float(p.mediabox.height) - H) > 0.01 for p in reader.pages):
        raise ValueError("PDF has inconsistent page size")
    for path, record in source_records.items():
        if sha_file(ROOT / path) != record["sha256"]:
            raise ValueError(f"Source changed during assembly: {path}")
    story_words = sum(len(re.findall(r"\b[\w'-]+\b", e["line"])) for p in pages if p["kind"] == "story" for panel in p["panels"] for e in panel.get("text", []))
    check = {
        "status": "PASS", "pdf": pdf_path.relative_to(ROOT).as_posix(), "pdf_sha256": sha_file(pdf_path),
        "pdf_byte_length": pdf_path.stat().st_size, "actual_pdf_pages": len(reader.pages),
        "format": "8 x 10 inches; 576 x 720 PDF points; exact 32 pages including cover and back",
        "script": script_path.relative_to(ROOT).as_posix(), "script_sha256": sha_file(script_path),
        "story_word_count": story_words, "panel_count": len(panels_out), "text_entry_count": len(text_bounds),
        "all_script_lines_extract_completely": not missing, "all_text_within_panel_bounds": all(r["within_panel"] for r in text_bounds),
        "minimum_story_font_size_pt": FONT_SIZE, "fonts": fonts, "source_files": source_records,
        "encoding": "Declared normalized crops, RGB JPEG quality95/subsampling0, no resize; source PNGs unchanged",
        "panels": panels_out, "text_bounds": text_bounds,
        "letterbox_review": [{"page": p["page"], "panel": p["panel"],
                               "art_area_coverage_fraction": p["art"]["art_area_coverage_fraction"],
                               "source": p["art"]["source"],
                               "status": "REVIEW_COMPOSITION" if p["art"]["art_area_coverage_fraction"] < 0.60 else "FIT_WITHIN_TARGET"}
                              for p in panels_out],
        "acceptance_limits": "Machine layout/count/text/provenance checks only. Exact artwork, narrative, child and owner review remain separate. No runtime or print-production acceptance.",
    }
    if render:
        import pypdfium2

        renders = ROOT / "tmp/pdfs/rumi_underpool_20261010"
        renders.mkdir(parents=True, exist_ok=True)
        document = pypdfium2.PdfDocument(str(pdf_path))
        rendered = []
        for index in range(len(document)):
            pdf_page = document[index]
            bitmap = pdf_page.render(scale=2.0)
            image = bitmap.to_pil().convert("RGB")
            path = renders / f"page_{index + 1:02d}.png"
            image.save(path)
            rendered.append(path)
            bitmap.close()
            pdf_page.close()
        document.close()
        contact_records = []
        thumb_width, thumb_height = 330, 413
        padding, label_height = 18, 25
        font = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 18)
        for group in range(4):
            sheet = Image.new("RGB", (4 * thumb_width + 5 * padding, 2 * (thumb_height + label_height) + 3 * padding), "#e7edf2")
            draw = ImageDraw.Draw(sheet)
            for offset in range(8):
                index = group * 8 + offset
                x = padding + (offset % 4) * (thumb_width + padding)
                y = padding + (offset // 4) * (thumb_height + label_height + padding)
                with Image.open(rendered[index]) as page_image:
                    thumb = page_image.copy()
                    thumb.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
                    sheet.paste(thumb, (x, y))
                draw.text((x, y + thumb_height + 3), f"Page {index + 1}", font=font, fill=INK)
            target = verification / f"pdf_contact_{group + 1:02d}.png"
            sheet.save(target)
            contact_records.append({"path": target.relative_to(ROOT).as_posix(), "sha256": sha_file(target), "pages": list(range(group * 8 + 1, group * 8 + 9))})
        check["rendered_page_count"] = len(rendered)
        check["render_directory_ignored"] = renders.relative_to(ROOT).as_posix()
        check["contact_sheets"] = contact_records
    (verification / "book_check.json").write_text(json.dumps(check, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"COMIC_BOOK_OK pages=32 panels={len(panels_out)} story_words={story_words} pdf_bytes={pdf_path.stat().st_size} sha256={check['pdf_sha256']}")
    return check


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    build(args.script.resolve(), args.output.resolve(), render=not args.no_render)
