"""Assemble one complete native PNG per page using unchanged original IDAT.

The root-frozen selection and provenance checker are mandatory. This tool never
selects takes, crops/resizes pixels, adds visible text or changes the old book.
Root runs the create-PDF operation marker exactly once before first authoring.
Existing PDF verification preserves PDF bytes. Actual renderer sampling is an
honest diagnostic separate from strict original-IDAT/RGB/CTM source integrity.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import struct
import subprocess
import zlib
from pathlib import Path
from validate_selection import (HERE, ROOT, SCRIPT, SELECTION, FROZEN_SCRIPT,
    NATIVE_SIZE, sha_bytes, sha_file, validate)
PDF = HERE / "output/pdf/Mermaid_Roshan_Here_I_Am_Detective_32_Pages.pdf"
CHECK = HERE / "verification/book_check.json"
PROVENANCE = HERE / "verification/provenance_check.json"
RENDER_DIR = ROOT / "tmp/pdfs/rumi_visual_detective_20261012"
W, H = 512.0, 768.0
MAX_PDF_BYTES = 100 * 1024 * 1024


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


def check_marker():
    path = HERE / "verification/authoring_marker_receipt.json"
    marker = json.loads(path.read_bytes())
    if marker["marker_call_count"] != 1 or marker["result"]["exit_code"] != 0:
        raise ValueError("First authoring requires the root's successful exactly-once create-PDF marker receipt.")
    if marker["arguments"] != ["--operation-kind", "create", "--expected-output-count", "1", "--output-format", "pdf"]:
        raise ValueError("Marker must describe this edition's one new PDF creation operation.")
    if Path(marker["script"]).name != "mark_artifact_operation_started.mjs":
        raise ValueError("Unexpected operation marker script.")
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha_file(path),
            "call_count": 1, "operation_kind": "create"}


def verify_pdf(pdf_path, rows):
    from pypdf import PdfReader
    reader = PdfReader(pdf_path, strict=True)
    if len(reader.pages) != 32:
        raise ValueError("Actual PDF must contain exactly 32 pages.")
    embedded = []
    for row, page in zip(rows, reader.pages):
        full_box = [0.0, 0.0, W, H]
        if list(map(float, page.mediabox)) != full_box or list(map(float, page.cropbox)) != full_box:
            raise ValueError(f"Page {row['number']} MediaBox/CropBox differs from whole native aspect.")
        if page.get("/Rotate", 0) != 0 or page.get("/UserUnit", 1) != 1 or page.get("/Annots"):
            raise ValueError(f"Page {row['number']} has rotation, altered user units or annotations.")
        for box in ["/TrimBox", "/BleedBox", "/ArtBox"]:
            if box in page and list(map(float, page[box])) != full_box:
                raise ValueError(f"Page {row['number']} contains a clipped {box}.")
        resources = page["/Resources"].get_object()
        if set(resources) != {"/XObject"}:
            raise ValueError(f"Page {row['number']} has resources beyond its one native image.")
        objects = resources["/XObject"].get_object()
        if set(objects) != {"/NativePage"}:
            raise ValueError(f"Page {row['number']} needs exactly the original native image.")
        image = objects["/NativePage"].get_object()
        operations = page.get_contents().operations
        operators = [operator for _, operator in operations]
        matrices = [list(map(float, args)) for args, operator in operations if operator == b"cm"]
        calls = [args for args, operator in operations if operator == b"Do"]
        if operators != [b"cm", b"q", b"cm", b"Do", b"Q"]:
            raise ValueError(f"Page {row['number']} has unexpected drawing/text/clip operations.")
        if matrices != [[1.0, 0.0, 0.0, 1.0, 0.0, 0.0], [W, 0.0, 0.0, H, 0.0, 0.0]] or calls != [["/NativePage"]]:
            raise ValueError(f"Page {row['number']} must place exactly one complete unrotated image at the full page CTM.")
        if image.get("/Subtype") != "/Image" or image.get("/Type") != "/XObject":
            raise ValueError(f"Page {row['number']} selected XObject is not an image.")
        if (int(image["/Width"]), int(image["/Height"])) != NATIVE_SIZE or image["/ColorSpace"] != "/DeviceRGB" or image["/BitsPerComponent"] != 8:
            raise ValueError(f"Page {row['number']} altered native dimensions/colour.")
        if image.get("/SMask") or image.get("/Mask") or image.get("/ImageMask") or image.get("/Interpolate", False) or image.get("/Decode"):
            raise ValueError(f"Page {row['number']} has transparency, interpolation or colour remapping.")
        if image.get("/Filter") != "/FlateDecode":
            raise ValueError(f"Page {row['number']} must retain the literal original PNG compression stream.")
        params = image.get("/DecodeParms")
        if not params or dict(params) != {"/Predictor": 15, "/Colors": 3, "/BitsPerComponent": 8, "/Columns": NATIVE_SIZE[0]}:
            raise ValueError(f"Page {row['number']} needs the original PNG predictor parameters.")
        idat, encoding = native_png_idat(ROOT / row["path"])
        if image._data != idat:
            raise ValueError(f"Page {row['number']} IDAT bytes were recompressed or changed.")
        decoded = image.get_data()
        pixel_hash = sha_bytes(decoded)
        if len(decoded) != NATIVE_SIZE[0] * NATIVE_SIZE[1] * 3 or pixel_hash != row["rgb_pixel_sha256"]:
            raise ValueError(f"Page {row['number']} decoded embedded RGB differs from native.")
        if (page.extract_text() or "").strip():
            raise ValueError(f"Page {row['number']} unexpectedly has selectable text overlays.")
        embedded.append({"number": row["number"], "dimensions": list(NATIVE_SIZE),
                         "color_space": "/DeviceRGB", "bits_per_component": 8,
                         "filters": ["/FlateDecode"], "decode_parameters": dict(params),
                         "decoded_rgb_sha256": pixel_hash, "native_pixel_match": True,
                         "original_idat_sha256": encoding["idat_sha256"],
                         "original_idat_bytes_preserved": True, "actual_image_transform": matrices[1],
                         "complete_frame_geometry": True})
        if row["number"] % 8 == 0:
            print(f"Original IDAT/RGB/full-page CTM checks: {row['number']}/32 passed.", flush=True)
    return embedded


def build(selection_sha256, selection_path=SELECTION, verify_existing=False, preflight=False):
    provenance, rows = validate(selection_path, selection_sha256)
    script = json.loads(SCRIPT.read_bytes())
    for row in rows:
        row.update(pdf_placement_points=[0, 0, W, H], raster_resize=False, crop=False,
                   visible_text_overlays=False, distortion=False)
    print("Frozen selection/provenance: 32 unique complete RGB native pages verified.", flush=True)
    if preflight:
        if verify_existing:
            raise ValueError("Choose preflight or verify-existing.")
        print(json.dumps({"status": "PREFLIGHT_PASS_NO_PDF_AUTHORING", "script_sha256": FROZEN_SCRIPT,
                          "selection_sha256": selection_sha256, "pages": 32, "story_words": provenance["story_words"]}), flush=True)
        return provenance
    marker = None
    if verify_existing:
        if not PDF.is_file():
            raise ValueError("--verify-existing requires this edition's already authored PDF.")
        existing_pdf_hash = sha_file(PDF)
        encodings = [native_png_idat(ROOT / row["path"])[1] for row in rows]
    else:
        if PDF.exists():
            raise ValueError("Preserve authored PDF bytes; use --verify-existing instead of overwriting.")
        marker = check_marker()
        encodings = write_native_png_pdf(rows, PDF, script["title"])
        existing_pdf_hash = None
    if PDF.stat().st_size >= MAX_PDF_BYTES:
        raise ValueError("Native original-IDAT PDF exceeds 100MiB packaging bound; no resample/recompression fallback permitted.")
    embedded = verify_pdf(PDF, rows)
    print("Rendering all32 actual PDF pages at144dpi for honest sampling diagnostics and visual review.", flush=True)
    method, renders, contacts, qa_font = render_and_compare(PDF, rows)
    for snapshot in provenance["source_input_snapshots"]:
        if sha_file(Path(snapshot["path"])) != snapshot["sha256"]:
            raise ValueError(f"Frozen input changed during authoring/rendering: {snapshot['path']}")
    if existing_pdf_hash and sha_file(PDF) != existing_pdf_hash:
        raise ValueError("Read-only verification changed the authored PDF.")
    render_exact = all(row["native_pixel_match"] for row in renders)
    checker_path = HERE / "validate_selection.py"
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = {"schema": "rumi_detective_book_check_v1",
              "status": "NATIVE_IDAT_RGB_GEOMETRY_PASS_RENDER_EXACT_VISUAL_ACCEPTANCE_PENDING" if render_exact else "NATIVE_IDAT_RGB_GEOMETRY_PASS_RENDER_SAMPLING_NON_EXACT_VISUAL_ACCEPTANCE_PENDING",
              "title": script["title"], "script_sha256": FROZEN_SCRIPT,
              "selection": {"path": Path(selection_path).resolve().relative_to(ROOT).as_posix(), "sha256": selection_sha256},
              "builder": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": sha_file(Path(__file__))},
              "checker": {"path": checker_path.relative_to(ROOT).as_posix(), "sha256": sha_file(checker_path)},
              "provenance_check": {"path": PROVENANCE.relative_to(ROOT).as_posix(), "sha256": sha_file(PROVENANCE)},
              "transcript": {"path": "assets_src/books/rumi_visual_detective_20261012/MANUSCRIPT.txt", "sha256": sha_file(HERE / "MANUSCRIPT.txt"), "entry_order_exact": True},
              "pdf": {"path": PDF.relative_to(ROOT).as_posix(), "sha256": sha_file(PDF), "bytes": PDF.stat().st_size,
                      "actual_page_count": 32, "page_dimensions_points": [W, H], "physical_size_inches": [W/72, H/72],
                      "one_complete_native_image_per_page": True, "selectable_story_text": False,
                      "lettering_source": "generated within native page art"},
              "story_words": provenance["story_words"], "total_source_panels": 102, "story_source_panels": 101,
              "native_sources": rows, "unique_native_sha256_count": 32, "unique_rgb_pixel_sha256_count": 32,
              "embedded_images": embedded, "all_embedded_rgb_pixels_match_native": True,
              "all_original_idat_streams_preserved": True, "render_method": method, "render_dpi": 144,
              "renders": renders, "all_actual_render_rgb_pixels_match_native": render_exact,
              "render_sampling_diagnostic": {"status": "EXACT" if render_exact else "NON_EXACT",
                  "exact_page_count": sum(row["native_pixel_match"] for row in renders),
                  "non_exact_page_count": sum(not row["native_pixel_match"] for row in renders),
                  "limit": "Actual renderer snapshots may sample differently. Measured differences are not repaired or described as exact. Original compressed IDAT bytes, decoded embedded RGB and whole-image placement are strict delivery integrity gates; renderer equality is a separate diagnostic."},
              "contacts": contacts, "qa_label_font": qa_font, "delivery_fonts": [],
              "image_encoding": {"method": "original native PNG IDAT, PDF FlateDecode Predictor15", "native_png_recompressed": False, "native_pixels_changed": False, "pages": encodings},
              "verification_mode": "existing PDF bytes preserved" if verify_existing else "new edition original PNG IDAT author and verify",
              "visual_review_requirement": "Human inspection of all exact selected native pages and final PDF renders: lettering, tails/order, single-tail identity, prop/contact geometry, distinct actions and print size.",
              "not_claimed": ["OCR or extracted-story-text verification of bitmap lettering", "semantic uniqueness from hashes alone", "owner/child/print acceptance", "runtime/cinematic/global master-audit acceptance"]}
    if marker:
        result["authoring_marker"] = marker
    CHECK.parent.mkdir(parents=True, exist_ok=True)
    CHECK.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "pdf_sha256": result["pdf"]["sha256"], "pages": 32,
                      "bytes": result["pdf"]["bytes"], "original_idat_and_rgb_match": True,
                      "actual_render_pixel_match": render_exact, "render_diagnostic": "EXACT" if render_exact else "NON_EXACT"}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=SELECTION)
    parser.add_argument("--selection-sha256", required=True, help="SHA-256 explicitly frozen by root after selecting/reviewing all32 pages")
    parser.add_argument("--preflight", action="store_true", help="Read-only source/native/provenance checks; no PDF, renders or receipts authored")
    parser.add_argument("--verify-existing", action="store_true", help="Preserve PDF bytes; verify strict embedding and refresh renders/check receipts")
    args = parser.parse_args()
    build(args.selection_sha256, args.selection, args.verify_existing, args.preflight)
