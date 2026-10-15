"""Assemble 32 complete native manga pages without changing delivery pixels.

The explicit root-owned selection is required. This renderer does not select
takes, crop images, resize raster data, re-letter artwork or add visible marks.
The physical PDF placement is 512x768 points. Decoded embedded RGB must match
every native page exactly. At 144 dpi, renderer output has the native dimensions;
its sampling differences are measured separately from source integrity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import subprocess
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT = HERE / "story_script.json"
SELECTION = HERE / "selected_art.json"
PDF = HERE / "output/pdf/Mermaid_Roshan_Here_I_Am_32_Pages.pdf"
CHECK = HERE / "verification/book_check.json"
RENDER_DIR = ROOT / "tmp/pdfs/rumi_voice_book_20261011"
W, H = 512.0, 768.0
NATIVE_SIZE = (1024, 1536)
ENCODING_RECEIPT = HERE / "verification/encoding_optimization.json"
MAX_PDF_BYTES = 100 * 1024 * 1024


def sha_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def sha_file(path):
    return sha_bytes(path.read_bytes())


def resolve_art(raw):
    path = (ROOT / raw.replace("\\", "/")).resolve(strict=True)
    if not path.is_relative_to((HERE / "native").resolve()) or path.suffix.lower() != ".png":
        raise ValueError(f"Selected art must be a native PNG in this edition: {raw}")
    return path


def rgb_record(path):
    from PIL import Image
    with Image.open(path) as image:
        if image.mode != "RGB" or image.size != NATIVE_SIZE:
            raise ValueError(f"Native RGB 1024x1536 required, without conversion: {path}: {image.mode}/{image.size}")
        if image.info.get("icc_profile"):
            raise ValueError(f"ICC source needs explicitly profiled PDF embedding: {path}")
        return {"dimensions": list(image.size), "mode": image.mode, "rgb_pixel_sha256": sha_bytes(image.tobytes())}


def native_png_idat(path):
    """Read unchanged PNG compression payloads; never decode/recompress them."""
    payload = path.read_bytes()
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"PNG signature required: {path}")
    offset, chunks, ihdr, ended = 8, [], None, False
    chunk_types = []
    while offset < len(payload):
        if len(payload) - offset < 12:
            raise ValueError(f"Truncated PNG chunk: {path}")
        length = struct.unpack(">I", payload[offset:offset + 4])[0]
        kind = payload[offset + 4:offset + 8]
        data = payload[offset + 8:offset + 8 + length]
        end = offset + 12 + length
        if end > len(payload) or zlib.crc32(kind + data) & 0xFFFFFFFF != struct.unpack(">I", payload[end - 4:end])[0]:
            raise ValueError(f"Invalid PNG chunk length/CRC: {path}")
        chunk_types.append(kind.decode("ascii"))
        if kind == b"IHDR":
            if ihdr is not None or offset != 8 or length != 13:
                raise ValueError(f"Exactly one first IHDR required: {path}")
            ihdr = struct.unpack(">IIBBBBB", data)
        elif kind == b"IDAT":
            chunks.append(data)
        elif kind == b"acTL":
            raise ValueError(f"Animated PNG is unsupported for direct image embedding: {path}")
        elif kind == b"IEND":
            if length != 0 or end != len(payload):
                raise ValueError(f"PNG IEND must terminate the native file: {path}")
            ended = True
            offset = end
            break
        offset = end
    if ihdr != (NATIVE_SIZE[0], NATIVE_SIZE[1], 8, 2, 0, 0, 0) or not chunks or not ended:
        raise ValueError(f"Native PNG must be 1024x1536, 8-bit RGB type2, standard compression/filter, noninterlaced: {path}: {ihdr}")
    idat = b"".join(chunks)
    return idat, {"ihdr": {"width": ihdr[0], "height": ihdr[1], "bits": 8, "colour_type": 2, "interlaced": False},
                  "idat_chunk_count": len(chunks), "idat_bytes": len(idat), "idat_sha256": sha_bytes(idat),
                  "chunk_types": chunk_types, "crc_verified": True, "idat_recompressed": False}


def write_native_png_pdf(rows, pdf_path, title):
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, EncodedStreamObject, DecodedStreamObject, NameObject, NumberObject
    writer = PdfWriter()
    writer.add_metadata({"/Title": title, "/Author": "Mermaid Roshan story project",
                         "/Subject": "32 unique complete native manga page images; original PNG IDAT streams; no image crop/resize or text overlay",
                         "/Creator": "build_book.py / native PNG IDAT lossless assembly"})
    encodings = []
    for row in rows:
        idat, encoding = native_png_idat(ROOT / row["path"])
        image = EncodedStreamObject()
        image._data = idat
        image.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Image"),
                      NameObject("/Width"): NumberObject(NATIVE_SIZE[0]), NameObject("/Height"): NumberObject(NATIVE_SIZE[1]),
                      NameObject("/ColorSpace"): NameObject("/DeviceRGB"), NameObject("/BitsPerComponent"): NumberObject(8),
                      NameObject("/Filter"): NameObject("/FlateDecode"),
                      NameObject("/DecodeParms"): DictionaryObject({NameObject("/Predictor"): NumberObject(15),
                          NameObject("/Colors"): NumberObject(3), NameObject("/BitsPerComponent"): NumberObject(8),
                          NameObject("/Columns"): NumberObject(NATIVE_SIZE[0])})})
        page = writer.add_blank_page(width=W, height=H)
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/XObject"): DictionaryObject({NameObject("/NativePage"): writer._add_object(image)})})
        content = DecodedStreamObject()
        content.set_data(b"1 0 0 1 0 0 cm\nq\n512 0 0 768 0 0 cm\n/NativePage Do\nQ\n")
        page[NameObject("/Contents")] = writer._add_object(content)
        encodings.append({"number": row["number"], **encoding})
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    writer.write(pdf_path)
    writer.close()
    if pdf_path.stat().st_size >= MAX_PDF_BYTES:
        raise ValueError("Original-IDAT PDF still exceeds the bounded 100MiB packaging requirement; no alternative compression attempted")
    return encodings


def render_and_compare(pdf_path, rows):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    render_paths = [RENDER_DIR / f"page_{n:02}.png" for n in range(1, 33)]
    bundled_poppler = Path("C:/Users/Peter/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe")
    poppler = str(bundled_poppler) if bundled_poppler.is_file() else shutil.which("pdftoppm")
    if poppler:
        prefix = RENDER_DIR / "poppler_page"
        subprocess.run([poppler, "-png", "-r", "144", "-aa", "no", "-aaVector", "no", str(pdf_path), str(prefix)], check=True, capture_output=True)
        produced = sorted(RENDER_DIR.glob("poppler_page-*.png"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
        if len(produced) != 32:
            raise ValueError("Poppler must render exactly all 32 pages")
        for source, target in zip(produced, render_paths):
            source.replace(target)
        method = f"Poppler pdftoppm ({poppler}), 144 dpi; font/vector anti-aliasing disabled; no render crop"
    else:
        import pypdfium2 as pdfium
        document = pdfium.PdfDocument(str(pdf_path))
        if len(document) != 32:
            raise ValueError("PDFium must find exactly 32 pages")
        for index, path in enumerate(render_paths):
            page = document[index]
            bitmap = page.render(scale=2, rotation=0, crop=(0, 0, 0, 0), no_smoothimage=True, no_smoothpath=True, no_smoothtext=True)
            bitmap.to_pil().save(path)
            bitmap.close()
            page.close()
        document.close()
        method = "pypdfium2 fallback; bundled/PATH Poppler unavailable; 144 dpi, image/path/text smoothing disabled, no crop/rotation"
    renders = []
    for row, path in zip(rows, render_paths):
        with Image.open(path) as image:
            if image.size != NATIVE_SIZE:
                raise ValueError(f"Rendered page {row['number']} dimension mismatch: {image.size}")
            pixels = image.convert("RGB").tobytes()
        actual = sha_bytes(pixels)
        matches = actual == row["rgb_pixel_sha256"]
        with Image.open(ROOT / row["path"]) as native:
            expected = np.asarray(native, dtype=np.int16)
        actual_pixels = np.frombuffer(pixels, dtype=np.uint8).reshape(NATIVE_SIZE[1], NATIVE_SIZE[0], 3).astype(np.int16)
        delta = np.abs(actual_pixels - expected)
        renders.append({"number": row["number"], "path": path.relative_to(ROOT).as_posix(), "sha256": sha_file(path),
                        "dimensions": list(NATIVE_SIZE), "rgb_pixel_sha256": actual, "native_pixel_match": matches,
                        "sampling_diagnostic": {"status": "EXACT" if matches else "NON_EXACT",
                            "changed_rgb_pixels": int(np.any(delta, axis=2).sum()),
                            "total_rgb_pixels": int(NATIVE_SIZE[0] * NATIVE_SIZE[1]),
                            "changed_channel_values": int(np.count_nonzero(delta)),
                            "max_channel_difference": int(delta.max()),
                            "mean_absolute_channel_difference": float(delta.mean()),
                            "mean_absolute_difference_by_rgb_channel": delta.mean(axis=(0, 1)).tolist()}})
    qa_font = Path("C:/Windows/Fonts/calibrib.ttf")
    font = ImageFont.truetype(str(qa_font), 23)
    contacts = []
    for sheet in range(4):
        contact = Image.new("RGB", (1410, 1100), "#E8EDF1")
        draw = ImageDraw.Draw(contact)
        for position in range(8):
            index = sheet * 8 + position
            x, y = 18 + (position % 4) * 350, 18 + (position // 4) * 536
            with Image.open(render_paths[index]) as rendered:
                # These are explicitly review-only thumbnails, never delivery.
                rendered.thumbnail((330, 495))
                contact.paste(rendered.convert("RGB"), (x, y))
            draw.text((x, y + 501), f"Page {index + 1}", fill="#243858", font=font)
        path = RENDER_DIR / f"book_contact_{sheet + 1:02}.png"
        contact.save(path)
        contacts.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha_file(path), "review_only_thumbnail": True})
    return method, renders, contacts, {"path": qa_font.as_posix(), "sha256": sha_file(qa_font), "role": "contact labels only; no font or text overlay in delivery PDF"}


def build(selection_path=SELECTION, pdf_path=PDF, verify_existing=False, optimize_encoding=False):
    from pypdf import PdfReader

    selection_path, pdf_path = Path(selection_path).resolve(strict=True), Path(pdf_path).resolve()
    script_hash, selection_hash = sha_file(SCRIPT), sha_file(selection_path)
    script = json.loads(SCRIPT.read_text(encoding="utf-8"))
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    source_pages, selected = script["pages"], selection["pages"]
    expected_numbers = list(range(1, 33))
    if len(source_pages) != 32 or [p["number"] for p in source_pages] != expected_numbers:
        raise ValueError("Source must contain exactly 32 consecutive book pages")
    if len(selected) != 32 or [p["number"] for p in selected] != expected_numbers:
        raise ValueError("Explicit selection must contain exactly 32 consecutive native page mappings")
    if selection["script_sha256"] != script_hash:
        raise ValueError("Selection does not bind the current frozen source script")
    if source_pages[0]["kind"] != "cover" or any(p["kind"] != "story" for p in source_pages[1:]):
        raise ValueError("Source must have cover1 and narrative story2-32")
    rows = []
    for page, selected_page in zip(source_pages, selected):
        path = resolve_art(selected_page["path"])
        actual = rgb_record(path)
        file_hash = sha_file(path)
        if file_hash != selected_page["sha256"] or actual["rgb_pixel_sha256"] != selected_page["rgb_pixel_sha256"] or actual["dimensions"] != selected_page["dimensions"]:
            raise ValueError(f"Selected native source/hash mismatch on page {page['number']}")
        rows.append({"number": page["number"], "kind": page["kind"], "path": path.relative_to(ROOT).as_posix(),
                     "sha256": file_hash, "take": selected_page["take"], **actual,
                     "pdf_placement_points": [0, 0, W, H], "raster_resize": False, "crop": False,
                     "visible_text_overlays": False, "distortion": False})
    if len({r["sha256"] for r in rows}) != 32 or len({r["rgb_pixel_sha256"] for r in rows}) != 32:
        raise ValueError("Every book page must have unique native bytes and decoded RGB pixels")

    print("Native/selection preflight: 32 unique complete RGB pages verified.", flush=True)
    if verify_existing and optimize_encoding:
        raise ValueError("Choose either verify-existing or the bounded encoding optimization")
    encoding_before, encodings = None, []
    authored_path = pdf_path
    if verify_existing:
        if not pdf_path.is_file():
            raise ValueError("--verify-existing requires the previously authored PDF")
        existing_pdf_hash = sha_file(pdf_path)
    else:
        if optimize_encoding:
            encoding_before = json.loads(ENCODING_RECEIPT.read_text(encoding="utf-8"))
            if sha_file(pdf_path) != encoding_before["previous_pdf"]["sha256"] or pdf_path.stat().st_size != encoding_before["previous_pdf"]["bytes"]:
                raise ValueError("Encoding baseline does not match the existing PDF")
            RENDER_DIR.mkdir(parents=True, exist_ok=True)
            backup = RENDER_DIR / "encoding_previous_ascii85.pdf"
            if backup.exists() and sha_file(backup) != encoding_before["previous_pdf"]["sha256"]:
                raise ValueError("Existing encoding baseline backup differs; do not overwrite it")
            if not backup.exists():
                shutil.copyfile(pdf_path, backup)
            authored_path = RENDER_DIR / "native_png_idat_candidate.pdf"
        encodings = write_native_png_pdf(rows, authored_path, script["title"])
        print(f"Original PNG IDAT packaging: {authored_path.stat().st_size:,} bytes, below 100MiB.", flush=True)
        existing_pdf_hash = None

    reader = PdfReader(authored_path)
    if len(reader.pages) != 32:
        raise ValueError("Final PDF must contain exactly 32 actual pages")
    embedded = []
    for row, page in zip(rows, reader.pages):
        if list(map(float, page.mediabox)) != [0.0, 0.0, W, H] or list(map(float, page.cropbox)) != [0.0, 0.0, W, H] or page.get("/Rotate", 0) != 0:
            raise ValueError(f"PDF page {row['number']} has wrong page geometry/crop/rotation")
        objects = page["/Resources"]["/XObject"].get_object()
        operations = page.get_contents().operations
        matrices = [list(map(float, args)) for args, operator in operations if operator == b"cm"]
        image_calls = [args for args, operator in operations if operator == b"Do"]
        allowed = {b"cm", b"BT", b"Tf", b"TL", b"ET", b"q", b"Do", b"Q"}
        if matrices != [[1.0, 0.0, 0.0, 1.0, 0.0, 0.0], [W, 0.0, 0.0, H, 0.0, 0.0]] or len(image_calls) != 1 or image_calls[0][0] not in objects or any(operator not in allowed for _, operator in operations):
            raise ValueError(f"PDF page {row['number']} must have one un-clipped, un-rotated, complete native image filling its page")
        images = [obj.get_object() for obj in objects.values() if obj.get_object().get("/Subtype") == "/Image"]
        if len(images) != 1:
            raise ValueError(f"PDF page {row['number']} must contain exactly one native image")
        image = images[0]
        filters = image.get("/Filter", [])
        filters = [str(f) for f in filters] if isinstance(filters, list) else [str(filters)]
        if any(f not in ["/ASCII85Decode", "/FlateDecode"] for f in filters):
            raise ValueError(f"PDF page {row['number']} image is not losslessly encoded: {filters}")
        if (int(image["/Width"]), int(image["/Height"])) != NATIVE_SIZE or image["/ColorSpace"] != "/DeviceRGB" or image["/BitsPerComponent"] != 8 or image.get("/SMask") or image.get("/Interpolate", False):
            raise ValueError(f"PDF page {row['number']} altered source geometry/colour/interpolation")
        decode_params = image.get("/DecodeParms")
        idat_hash = None
        if encodings:
            expected_params = {"/Predictor": 15, "/Colors": 3, "/BitsPerComponent": 8, "/Columns": NATIVE_SIZE[0]}
            if filters != ["/FlateDecode"] or not decode_params or dict(decode_params) != expected_params:
                raise ValueError(f"PDF page {row['number']} does not use the standard original-PNG predictor embedding")
            idat_hash = sha_bytes(image._data)
            if idat_hash != encodings[row["number"] - 1]["idat_sha256"]:
                raise ValueError(f"PDF page {row['number']} compression stream differs from original native PNG IDAT bytes")
        pixel_hash = sha_bytes(image.get_data())
        if pixel_hash != row["rgb_pixel_sha256"]:
            raise ValueError(f"Embedded decoded pixels differ from native page {row['number']}")
        if (page.extract_text() or "").strip():
            raise ValueError(f"Unexpected selectable text overlay on PDF page {row['number']}")
        embedded.append({"number": row["number"], "dimensions": list(NATIVE_SIZE), "color_space": str(image["/ColorSpace"]),
                         "bits_per_component": 8, "filters": filters, "decoded_rgb_sha256": pixel_hash, "native_pixel_match": True,
                         "actual_image_transform": matrices[1], "complete_frame_geometry": True,
                         "decode_parameters": dict(decode_params) if decode_params else None,
                         "original_idat_sha256": idat_hash, "original_idat_bytes_preserved": bool(idat_hash)})
        if row["number"] % 8 == 0:
            print(f"Lossless embedded-pixel/geometry checks: {row['number']}/32 pages passed.", flush=True)
    print("Rendering all 32 actual PDF pages at 144 dpi for sampling diagnostics and visual review.", flush=True)
    method, renders, contacts, qa_font = render_and_compare(authored_path, rows)
    if sha_file(SCRIPT) != script_hash or sha_file(selection_path) != selection_hash or any(sha_file(ROOT / row["path"]) != row["sha256"] for row in rows) or (existing_pdf_hash and sha_file(pdf_path) != existing_pdf_hash):
        raise ValueError("Frozen script/selection/native source changed during authoring or rendering")
    if optimize_encoding:
        authored_path.replace(pdf_path)
    transcript = HERE / "MANUSCRIPT.txt"
    story_words = sum(len(re.findall(r"\S+", entry["text"])) for p in source_pages if p["kind"] == "story" for panel in p["panels"] for entry in panel["entries"])
    render_exact = all(row["native_pixel_match"] for row in renders)
    result = {"schema": "rumi_voice_book_check_v2", "status": "NATIVE_EMBEDDING_PASS_RENDER_EXACT_VISUAL_ACCEPTANCE_PENDING" if render_exact else "NATIVE_EMBEDDING_PASS_RENDER_SAMPLING_NON_EXACT_VISUAL_ACCEPTANCE_PENDING",
              "title": script["title"], "script_sha256": script_hash,
              "selection": {"path": selection_path.relative_to(ROOT).as_posix(), "sha256": selection_hash},
              "builder": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": sha_file(Path(__file__))},
              "transcript": {"path": transcript.relative_to(ROOT).as_posix(), "sha256": sha_file(transcript)},
              "pdf": {"path": pdf_path.relative_to(ROOT).as_posix(), "sha256": sha_file(pdf_path), "bytes": pdf_path.stat().st_size,
                      "actual_page_count": 32, "page_dimensions_points": [W, H], "physical_size_inches": [W/72, H/72],
                      "one_complete_native_image_per_page": True, "selectable_story_text": False, "lettering_source": "generated within native page art"},
              "story_words": story_words, "native_sources": rows, "unique_native_sha256_count": 32, "unique_rgb_pixel_sha256_count": 32,
              "embedded_images": embedded, "all_embedded_rgb_pixels_match_native": True,
              "render_method": method, "render_dpi": 144, "renders": renders, "all_actual_render_rgb_pixels_match_native": render_exact,
              "render_sampling_diagnostic": {"status": "EXACT" if render_exact else "NON_EXACT",
                  "exact_page_count": sum(row["native_pixel_match"] for row in renders),
                  "non_exact_page_count": sum(not row["native_pixel_match"] for row in renders),
                  "limit": "Renderer snapshots may resample during display. Per-page differences are measured, not repaired or claimed exact. Exact decoded embedded RGB and full-image placement remain the strict delivery/source integrity gates; renderer RGB equality is a separate diagnostic."},
              "contacts": contacts, "qa_label_font": qa_font, "delivery_fonts": [],
              "not_claimed": ["OCR/extracted-text verification of bitmap lettering", "semantic uniqueness from hash equality alone", "owner/child/print acceptance", "runtime or cinematic acceptance"],
              "visual_review_requirement": "Each exact selected native page needs human lettering, attribution, anatomy, staging/contact and distinct-action review. Exact decoded embedded pixels preserve those sources; actual PDF renders separately need full-frame/layout inspection.",
              "verification_mode": "existing PDF bytes preserved" if verify_existing else "original PNG IDAT author and verify",
              "image_encoding": {"method": "original native PNG IDAT streams, PDF FlateDecode with Predictor15" if encodings else "existing lossless container",
                  "native_png_recompressed": False, "native_pixels_changed": False, "pages": encodings}}
    if encoding_before is not None:
        previous_renders = {r["number"]: r for r in encoding_before["previous_render_records"]}
        equality = [{"number": row["number"], "render_rgb_equals_previous_pdf": row["rgb_pixel_sha256"] == previous_renders[row["number"]]["rgb_pixel_sha256"],
                     "render_png_bytes_equal_previous_pdf": row["sha256"] == previous_renders[row["number"]]["sha256"]} for row in renders]
        encoding_before.update({"status": "LOSSLESS_ORIGINAL_IDAT_PACKAGING_PASS_VISUAL_ACCEPTANCE_SEPARATE",
            "optimized_pdf": result["pdf"], "builder": result["builder"], "native_idat_records": encodings,
            "all_embedded_rgb_pixels_match_native": True, "all_original_idat_streams_preserved": True,
            "native_source_bytes_unchanged": True, "script_selection_bytes_unchanged": True,
            "bytes_saved": encoding_before["previous_pdf"]["bytes"] - result["pdf"]["bytes"],
            "under_100_mib": result["pdf"]["bytes"] < MAX_PDF_BYTES, "render_comparison_to_previous_pdf": equality,
            "all_render_rgb_equals_previous_pdf": all(r["render_rgb_equals_previous_pdf"] for r in equality),
            "actual_render_rgb_equals_native": render_exact, "actual_render_diagnostic": "EXACT" if render_exact else "NON_EXACT",
            "contacts": contacts, "previous_pdf_backup": (RENDER_DIR / "encoding_previous_ascii85.pdf").relative_to(ROOT).as_posix()})
        ENCODING_RECEIPT.write_text(json.dumps(encoding_before, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        result["encoding_optimization"] = {"path": ENCODING_RECEIPT.relative_to(ROOT).as_posix(), "sha256": sha_file(ENCODING_RECEIPT)}
    CHECK.parent.mkdir(parents=True, exist_ok=True)
    CHECK.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"pdf_sha256": result["pdf"]["sha256"], "pages": 32, "bytes": result["pdf"]["bytes"],
                      "unique_sources": 32, "embedded_pixel_match": True, "actual_render_pixel_match": render_exact,
                      "render_diagnostic": result["render_sampling_diagnostic"]["status"], "renderer": method}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=SELECTION)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--verify-existing", action="store_true", help="Verify/render the already authored PDF without rewriting its bytes")
    parser.add_argument("--optimize-encoding", action="store_true", help="Bounded original PNG IDAT packaging pass, preserving the previous PDF receipt/backup")
    args = parser.parse_args()
    build(args.selection, args.pdf, args.verify_existing, args.optimize_encoding)
