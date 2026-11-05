"""Verify the complete V31 proof and its bounded changes against sealed V30.

This is mechanical evidence only. Character, story, clinical, owner, child and
physical-print acceptance remain separate. Running this helper writes only the
current revision's complete/verification.json receipt.
"""

from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageFilter
from pypdf import PdfReader
import pypdfium2 as pdfium


V = Path(__file__).resolve().parent
L = V.parents[1]
R = L.parents[2]
C = V / "complete"
OLD = V.parent / "v30_identity" / "complete"
BASE = "19ee6ce8ec4c20c05714f101d0d222a33477e400"
EXPECTED_CHANGED = [12, 13, 23, 31, 33]
TEXT_CHANGED = {12, 13, 23, 31}
W, H, SCALE = 504, 360, 3


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_bytes(path):
    relative = path.resolve().relative_to(R.resolve()).as_posix()
    return subprocess.check_output(["git", "show", BASE + ":" + relative], cwd=R)


def compact(text):
    return "".join(text.split())


def layer_signature(layer):
    # V31 records the already-derived canvas transform explicitly; adding this
    # diagnostic field does not authorize repainting an unchanged V30 mask.
    semantic = {key: value for key, value in layer.items()
                if key != "clip_canvas_transform_points"}
    return json.dumps(semantic, sort_keys=True, separators=(",", ":"))


def box_on_proof(box):
    x, y, width, height = box
    return (x * SCALE, (H - y - height) * SCALE,
            (x + width) * SCALE, (H - y) * SCALE)


def polygon_on_proof(layer):
    """Project a reference polygon through the *actual* recorded draw operation.

    The candidate may be a crop of a scene or a patch placed on a cutout. A
    full-canvas max-fit assumption would silently misplace those scopes. First
    map reference points into the candidate's native source canvas, then map
    that native source box into its recorded PDF target box. This also handles
    optional placement target boxes without depending on renderer defaults.
    """
    rw, rh = layer["clip_reference_size"]
    cl, ct, cr, cb = layer.get("source_canvas_box", [0, 0, rw, rh])
    iw, ih = layer["native_size"]
    left, top, right, bottom = layer["source_box_pixels"]
    x, y, width, height = layer["target_box_points"]
    assert cr > cl and cb > ct and right > left and bottom > top
    assert width > 0 and height > 0
    polygon = layer["clip_polygon_source_pixels"]
    assert len(polygon) >= 3
    result = []
    for px, py in polygon:
        assert cl <= px <= cr and ct <= py <= cb, ("Invalid reference clip", layer)
        native_x = (px - cl) * iw / (cr - cl)
        native_y = (py - ct) * ih / (cb - ct)
        # The embedded source box encloses the clip, including rounding.
        assert left - 1e-6 <= native_x <= right + 1e-6
        assert top - 1e-6 <= native_y <= bottom + 1e-6
        pdf_x = x + (native_x - left) * width / (right - left)
        pdf_y = y + (bottom - native_y) * height / (bottom - top)
        result.append((pdf_x * SCALE, (H - pdf_y) * SCALE))
    return result


def declared_change_mask(index, current, baseline, size):
    page_id = "back_cover" if index == 33 else index
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    old_layers = [layer for layer in baseline["layers"] if layer["page"] == page_id]
    new_layers = [layer for layer in current["layers"] if layer["page"] == page_id]
    old_signatures = {layer_signature(layer) for layer in old_layers}
    new_signatures = {layer_signature(layer) for layer in new_layers}
    exposed_polygons = []
    # Unchanged V30 face/neckline polygons grant no scope for a new V31 edit.
    for collection, opposite in ((new_layers, old_signatures), (old_layers, new_signatures)):
        for layer in collection:
            if ("clip_polygon_source_pixels" in layer
                    and layer_signature(layer) not in opposite):
                points = polygon_on_proof(layer)
                draw.polygon(points, fill=255)
                exposed_polygons.append({"source": layer["source_key"],
                                         "proof_polygon": points})
    text_boxes = []
    if index in TEXT_CHANGED:
        for provenance in (baseline, current):
            for line in provenance["text_lines"]:
                if line["page"] == page_id:
                    draw.rectangle(box_on_proof(line["box"]), fill=255)
                    text_boxes.append(line["box"])
    placement_boxes = []
    if index == 31:
        for layer in old_layers + new_layers:
            # Only foreground cutouts: never authorize a whole stationery plate.
            if layer["role"] == "story_art" and layer["alpha"]:
                draw.rectangle(box_on_proof(layer["target_box_points"]), fill=255)
                placement_boxes.append(layer["target_box_points"])
    assert exposed_polygons or text_boxes or placement_boxes, ("Missing declared scope", index)
    mask = mask.filter(ImageFilter.MaxFilter(7))  # Three proof pixels at exposed boundaries.
    return mask, {"new_or_changed_clip_polygons": exposed_polygons,
                  "old_and_new_text_boxes": text_boxes,
                  "old_and_new_foreground_placement_boxes": placement_boxes}


def embedded_font(font):
    descriptor = font.get("/FontDescriptor")
    if descriptor:
        descriptor = descriptor.get_object()
        if any(descriptor.get(key) for key in ("/FontFile", "/FontFile2", "/FontFile3")):
            return True
    return any(embedded_font(value.get_object()) for value in font.get("/DescendantFonts", []))


def inspect_resources(reader):
    filters = Counter()
    fonts = set()
    seen = set()

    def image_filter(obj):
        key = id(obj)
        if key in seen:
            return
        seen.add(key)
        value = str(obj.get("/Filter"))
        assert "/DCTDecode" not in value and "/JPXDecode" not in value, ("Lossy PDF image", value)
        filters[value] += 1
        if obj.get("/SMask"):
            image_filter(obj["/SMask"].get_object())

    def resources(res):
        res = res.get_object()
        for value in res.get("/Font", {}).values():
            font = value.get_object()
            name = str(font.get("/BaseFont"))
            if "Sniglet" in name:
                assert embedded_font(font), ("Unembedded Sniglet", name)
                fonts.add(name)
        for value in res.get("/XObject", {}).values():
            obj = value.get_object()
            if obj.get("/Subtype") == "/Image":
                image_filter(obj)
            elif obj.get("/Subtype") == "/Form" and obj.get("/Resources"):
                resources(obj["/Resources"])

    for page in reader.pages:
        resources(page["/Resources"])
    assert fonts, "No embedded Sniglet font"
    return dict(filters), sorted(fonts)


def main():
    book = read(L / "book.json")
    baseline_book = read(V / "BOOK_BASELINE.json")
    baseline_layout = read(OLD / "page_provenance.json")
    layout = read(C / "page_provenance.json")
    assert baseline_book == json.loads(git_bytes(L / "book.json"))
    assert sha(OLD / "page_provenance.json") == hashlib.sha256(
        git_bytes(OLD / "page_provenance.json")).hexdigest()
    assert len(book["pages"]) == 32 and book["story_pages"] == 32
    assert [page["page"] for page in book["pages"]] == list(range(1, 33))
    assert book["cover"] == baseline_book["cover"], "Front cover changed outside V31 scope"
    assert book["back_cover"]["art"] == baseline_book["back_cover"]["art"]
    for patch in baseline_book["back_cover"].get("local_patches", []):
        assert patch in book["back_cover"].get("local_patches", []), "V30 rear identity mask changed"
    for page, previous in zip(book["pages"], baseline_book["pages"]):
        assert page["mode"] == previous["mode"]
        if page["page"] not in TEXT_CHANGED:
            assert page == previous, ("Unexpected story-page config change", page["page"])
        if page["page"] != 31:
            assert page["art"] == previous["art"], ("Original main art replaced", page["page"])
    # Every sealed V30 source, including unused Eagle and original cover masters,
    # must still match the immutable Git baseline. New derivatives do not replace it.
    preserved = []
    old_source_files = sorted({layer["file"] for layer in baseline_layout["layers"]}
                              | {baseline_layout["font"]["file"]})
    for relative in old_source_files:
        path = (L / relative).resolve()
        expected = hashlib.sha256(git_bytes(path)).hexdigest()
        assert sha(path) == expected, ("Sealed original source modified", relative)
        preserved.append({"file": relative, "sha256": expected, "matches_git_baseline": True})
    for layer in layout["layers"]:
        path = (L / layer["file"]).resolve()
        assert sha(path) == layer["sha256"], ("Layer source hash mismatch", layer["file"])
        with Image.open(path) as image:
            assert list(image.size) == layer["native_size"]
    assert sha(L / layout["font"]["file"]) == layout["font"]["sha256"]
    assert "Sniglet" in Path(layout["font"]["file"]).name

    pdf = C / "Mermaid_Roshan_LANDSCAPE_ROUGH.pdf"
    reader = PdfReader(pdf)
    assert len(reader.pages) == 34
    assert all(list(page.mediabox) == [0, 0, W, H] for page in reader.pages)
    manuscript = {page["page"]: page for page in book["pages"]}
    visible_font_events = 0
    for index, page in enumerate(reader.pages):
        page_id = "front_cover" if index == 0 else "back_cover" if index == 33 else index

        def check_visible_text(text, _cm, _tm, font, size):
            nonlocal visible_font_events
            if text.strip():
                assert font is not None and "Sniglet" in str(font.get("/BaseFont")), (
                    "Visible text uses another font", index, text)
                if isinstance(page_id, int):
                    assert size >= 18, ("Story text below18pt", index, text, size)
                visible_font_events += 1

        extracted = compact(page.extract_text(visitor_text=check_visible_text))
        declared_lines = [line for line in layout["text_lines"] if line["page"] == page_id]
        for line in declared_lines:
            assert compact(line["text"]) in extracted, ("PDF text mismatch", index, line["text"])
            x, y, width, height = line["box"]
            margin = 24 if isinstance(page_id, int) else 18
            assert x >= margin and y >= margin and x + width <= W - margin and y + height <= H - margin, (
                "Text outside safety inset", index, line)
            if isinstance(page_id, int):
                assert line["font_size"] >= 18
        if isinstance(page_id, int):
            assert compact(manuscript[index]["text"]) in extracted
            assert compact(manuscript[index]["text"]) in compact(
                "".join(line["text"] for line in declared_lines))
            for bubble in manuscript[index].get("speech_bubbles", []):
                assert compact(bubble["text"]) in extracted
    assert visible_font_events
    filters, fonts = inspect_resources(reader)

    changed, unchanged, outside, screens = [], [], [], []
    doc = pdfium.PdfDocument(str(pdf))
    try:
        for index in range(34):
            path = C / f"page_{index:02}.png"
            old_path = OLD / f"page_{index:02}.png"
            old_hash = sha(old_path)
            assert old_hash == hashlib.sha256(git_bytes(old_path)).hexdigest(), (
                "Sealed V30 proof modified", index)
            with Image.open(path) as image:
                proof = image.convert("RGB")
            with Image.open(old_path) as image:
                baseline = image.convert("RGB")
            assert proof.size == baseline.size == (W * SCALE, H * SCALE)
            page = doc[index]
            rendered = page.render(scale=SCALE).to_pil().convert("RGB")
            assert ImageChops.difference(rendered, proof).getbbox() is None, (
                "PDF/native-proof pixel mismatch", index)
            page.close()
            proof_hash = sha(path)
            diff = ImageChops.difference(proof, baseline)
            if index not in EXPECTED_CHANGED:
                assert proof_hash == old_hash, ("Undeclared proof-byte change", index)
                assert diff.getbbox() is None
                unchanged.append(index)
            else:
                assert diff.getbbox() is not None, ("Declared change has no visible effect", index)
                changed.append(index)
                mask, scopes = declared_change_mask(index, layout, baseline_layout, proof.size)
                remainder = ImageChops.multiply(diff, Image.merge("RGB", [ImageChops.invert(mask)] * 3))
                assert remainder.getbbox() is None, ("Outside declared scopes changed", index, remainder.getbbox())
                outside.append({"page": index, "outside_declared_regions_changed_pixels": 0,
                                "boundary_allowance_proof_pixels": 3,
                                "polygon_mapping": "actual recorded native source-box to PDF target-box",
                                "declared_scopes": scopes})
            screens.append({"page_index": index, "dimensions": list(proof.size),
                            "png_sha256": proof_hash, "v30_png_sha256": old_hash,
                            "byte_identical_to_v30": proof_hash == old_hash})
    finally:
        doc.close()
    assert changed == EXPECTED_CHANGED and len(unchanged) == 29
    result = {"status": "MECHANICAL_PASS; EXTERNAL_ACCEPTANCE_SEPARATE", "revision": "V31",
              "baseline_commit": BASE, "total_pages": 34, "story_pages": 32,
              "trim_points": [W, H], "book_json_sha256": sha(L / "book.json"),
              "baseline_book_snapshot_sha256": sha(V / "BOOK_BASELINE.json"),
              "page_provenance_sha256": sha(C / "page_provenance.json"),
              "pdf_sha256": sha(pdf), "pdf_bytes": pdf.stat().st_size,
              "native_text_matches_manuscript": True,
              "story_text_sniglet_at_least18pt": True,
              "story_text_safety_margin_points": 24, "cover_text_safety_margin_points": 18,
              "lossless_pdf_raster_matches_all34screenshots": True,
              "pdf_image_filters": filters, "embedded_fonts": fonts,
              "changed_pages": changed, "unchanged_pages_byte_identical_to_v30": unchanged,
              "outside_region_preservation": outside, "preserved_sources": preserved,
              "screenshots": screens,
              "scope": "Source/text/geometry/lossless-export and exact bounded-delta verification. No inferred visual, clinical, child, owner or print acceptance."}
    (C / "verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                         encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("screenshots", "preserved_sources", "outside_region_preservation")}, indent=2))


if __name__ == "__main__":
    main()
