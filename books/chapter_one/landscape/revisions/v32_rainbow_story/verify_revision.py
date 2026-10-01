"""Verify V32 against the immutable V31 baseline through explicit pagination.

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
OLD = V.parent / "v31_story_clarity" / "complete"
BASE = "07734bb43018ffdefef3644f337db8fa46038d5b"
EXPECTED_CHANGED = [4, 13, 14, 22, 30, 31]
STRICT_DELTA = {13, 14, 22, 30}
TEXT_ONLY = {14, 22}
EXPECTED_MAPPING = {0: 0, 1: 1, 2: 2, 3: 3, 4: None, 33: 33}
EXPECTED_MAPPING.update({n: n - 1 for n in range(5, 23)})
EXPECTED_MAPPING.update({n: n for n in range(23, 30)})
EXPECTED_MAPPING.update({30: 22, 31: 30, 32: 32})
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
    # Pagination changes page labels; explicit canvas transform metadata is
    # derived geometry, not new creative pixels. Neither grants edit scope.
    semantic = {key: value for key, value in layer.items()
                if key not in ("page", "clip_canvas_transform_points")}
    return json.dumps(semantic, sort_keys=True, separators=(",", ":"))


def page_id(index):
    return "front_cover" if index == 0 else "back_cover" if index == 33 else index


def layers_for(provenance, index):
    return [layer for layer in provenance["layers"]
            if layer["page"] == page_id(index)]


def text_for(provenance, index):
    return [line for line in provenance["text_lines"]
            if line["page"] == page_id(index)]


def read_pagination():
    document = read(V / "pagination.json")
    rows = document if isinstance(document, list) else document["rows"]
    assert isinstance(rows, list)
    mapping = {}
    statuses = {}
    for row in rows:
        n = row["new_page"]
        assert isinstance(n, int) and not isinstance(n, bool) and 0 <= n <= 33
        assert n not in mapping, ("Duplicate pagination row", n)
        previous = row["baseline_page"]
        assert previous is None or (isinstance(previous, int)
                                     and not isinstance(previous, bool)
                                     and 0 <= previous <= 33)
        assert isinstance(row["status"], str) and row["status"].strip()
        mapping[n] = previous
        statuses[n] = row["status"]
    assert set(mapping) in (set(range(1, 33)), set(range(34))), "Incomplete pagination"
    # Covers are fixed when the explicit ledger contains story rows only.
    for n in (0, 33):
        mapping.setdefault(n, n)
        statuses.setdefault(n, "unchanged fixed cover")
    assert mapping == EXPECTED_MAPPING, ("Unexpected pagination", mapping)
    return document, mapping, statuses

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


def declared_change_mask(index, baseline_index, current, baseline, size):
    assert index in STRICT_DELTA
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    old_layers = layers_for(baseline, baseline_index)
    new_layers = layers_for(current, index)
    old_signatures = {layer_signature(layer) for layer in old_layers}
    new_signatures = {layer_signature(layer) for layer in new_layers}
    exposed_polygons = []
    # Only genuinely added/changed/removed native polygons authorize pixels.
    # An unchanged V31 patch relocated by page numbering grants no new scope.
    for collection, opposite in ((new_layers, old_signatures),
                                 (old_layers, new_signatures)):
        for layer in collection:
            if ("clip_polygon_source_pixels" in layer
                    and layer_signature(layer) not in opposite):
                points = polygon_on_proof(layer)
                draw.polygon(points, fill=255)
                exposed_polygons.append({"source": layer["source_key"],
                                         "proof_polygon": points})
    text_boxes = []
    for provenance, number in ((baseline, baseline_index), (current, index)):
        for line in text_for(provenance, number):
            draw.rectangle(box_on_proof(line["box"]), fill=255)
            text_boxes.append(line["box"])
    if index in TEXT_ONLY:
        assert not exposed_polygons, ("Text-only page acquires new art scope", index)
    if index == 13:
        assert exposed_polygons, "Restored rainbow lane has no removed aqua scope"
        assert not any("clip_polygon_source_pixels" in layer for layer in new_layers), (
            "Waterfall restoration must expose the existing source, not a new patch", index)
    if index == 30:
        assert exposed_polygons, "Character/brush removal has no bounded native mask"
    assert exposed_polygons or text_boxes, ("Missing declared scope", index)
    mask = mask.filter(ImageFilter.MaxFilter(7))  # Three proof-pixel AA allowance.
    return mask, {"new_changed_or_removed_clip_polygons": exposed_polygons,
                  "old_and_new_text_boxes": text_boxes,
                  "foreground_placement_scope": []}

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



def config_without_page(page):
    return {key: value for key, value in page.items() if key != "page"}


def verify_existing_layout_swap(layout, baseline_layout):
    """Page31 may rearrange existing sources, not import a new scene canvas."""
    allowed = layers_for(baseline_layout, 30) + layers_for(baseline_layout, 31)
    permitted = {(layer["file"], layer["sha256"]) for layer in allowed}
    current = layers_for(layout, 31)
    assert current
    for layer in current:
        assert (layer["file"], layer["sha256"]) in permitted, (
            "Page31 layout uses a new raster instead of existing30/31 sources", layer)
    old_backgrounds = {(layer["file"], layer["sha256"])
                       for layer in layers_for(baseline_layout, 31)
                       if layer["role"] == "integrated_stationery"}
    current_backgrounds = {(layer["file"], layer["sha256"])
                           for layer in current
                           if layer["role"] == "integrated_stationery"}
    assert old_backgrounds and current_backgrounds == old_backgrounds, (
        "Page31 must reuse the existing page31 stationery base")
    # Existing face/rest-bank derivatives are reusable pixels; all retained files
    # are independently verified against immutable Git, including old31 masks.
    return {"scope_type": "existing-source stationery and foreground layout swap",
            "allowed_delta": "whole page, with every image source/hash constrained to sealed V31 pages30/31",
            "outside_declared_regions_changed_pixels": None,
            "reason": "Different existing stationery and foreground placements legitimately affect the complete layout; no bounded-inpaint preservation claim is made.",
            "current_layers": current,
            "allowed_source_files": sorted({layer["file"] for layer in allowed})}


def main():
    book = read(L / "book.json")
    baseline_book = read(V / "BOOK_BASELINE.json")
    baseline_layout = read(OLD / "page_provenance.json")
    layout = read(C / "page_provenance.json")
    pagination, mapping, statuses = read_pagination()
    assert baseline_book == json.loads(git_bytes(L / "book.json"))
    assert sha(OLD / "page_provenance.json") == hashlib.sha256(
        git_bytes(OLD / "page_provenance.json")).hexdigest()
    assert len(book["pages"]) == 32 and book["story_pages"] == 32
    assert [page["page"] for page in book["pages"]] == list(range(1, 33))
    assert book["page_size_points"] == baseline_book["page_size_points"] == [W, H]
    assert book["cover"] == baseline_book["cover"], "Front cover changed outside V32 scope"
    assert book["back_cover"] == baseline_book["back_cover"], "Rear cover changed outside V32 scope"
    manuscript = {page["page"]: page for page in book["pages"]}
    old_manuscript = {page["page"]: page for page in baseline_book["pages"]}
    for n in range(1, 33):
        page = manuscript[n]
        previous_index = mapping[n]
        if previous_index is None:
            assert n == 4
            continue
        previous = old_manuscript[previous_index]
        assert page["mode"] == previous["mode"], ("Undeclared mode change", n)
        if n not in EXPECTED_CHANGED:
            assert config_without_page(page) == config_without_page(previous), (
                "Unchanged mapped page config differs", n, previous_index)
        if n != 31:
            assert page["art"] == previous["art"], ("Original main art replaced", n)
        new_layers = layers_for(layout, n)
        old_layers = layers_for(baseline_layout, previous_index)
        if n in TEXT_ONLY or n not in EXPECTED_CHANGED:
            assert [layer_signature(x) for x in new_layers] == [
                layer_signature(x) for x in old_layers], (
                    "Text-only or unchanged mapped source geometry changed", n)
        elif n in (13, 30):
            # Full unmasked source remains untouched; only local masks differ.
            assert [layer_signature(x) for x in new_layers
                    if "clip_polygon_source_pixels" not in x] == [
                        layer_signature(x) for x in old_layers
                        if "clip_polygon_source_pixels" not in x], (
                            "Bounded repair replaced the complete base artwork", n)
    layout_swap_scope = verify_existing_layout_swap(layout, baseline_layout)

    # Preserve EVERY V31 registered source, even those now unused after the merge,
    # not just images visible in the previous proof. The font is protected too.
    old_source_files = sorted(
        {source["file"] for source in baseline_book["sources"].values()
         if "file" in source}
        | {layer["file"] for layer in baseline_layout["layers"]}
        | {baseline_layout["font"]["file"]})
    preserved = []
    for relative in old_source_files:
        path = (L / relative).resolve()
        expected = hashlib.sha256(git_bytes(path)).hexdigest()
        assert sha(path) == expected, ("Sealed V31 source modified", relative)
        preserved.append({"file": relative, "sha256": expected,
                          "matches_git_baseline": True})
    for layer in layout["layers"]:
        path = (L / layer["file"]).resolve()
        assert sha(path) == layer["sha256"], ("Layer source hash mismatch", layer["file"])
        with Image.open(path) as image:
            assert list(image.size) == layer["native_size"]
    assert sha(L / layout["font"]["file"]) == layout["font"]["sha256"]
    assert layout["font"] == baseline_layout["font"]
    assert "Sniglet" in Path(layout["font"]["file"]).name
    # Preserve all34 old proof files, including the merged old31 endpoint.
    old_hashes = {}
    for index in range(34):
        old_path = OLD / f"page_{index:02}.png"
        digest = sha(old_path)
        assert digest == hashlib.sha256(git_bytes(old_path)).hexdigest(), (
            "Sealed V31 proof modified", index)
        old_hashes[index] = digest

    pdf = C / "Mermaid_Roshan_LANDSCAPE_ROUGH.pdf"
    reader = PdfReader(pdf)
    assert len(reader.pages) == 34
    assert all(list(page.mediabox) == [0, 0, W, H] for page in reader.pages)
    visible_font_events = 0
    for index, page in enumerate(reader.pages):
        identifier = page_id(index)

        def check_visible_text(text, _cm, _tm, font, size):
            nonlocal visible_font_events
            if text.strip():
                assert font is not None and "Sniglet" in str(font.get("/BaseFont")), (
                    "Visible text uses another font", index, text)
                if isinstance(identifier, int):
                    assert size >= 18, ("Story text below18pt", index, text, size)
                visible_font_events += 1

        extracted = compact(page.extract_text(visitor_text=check_visible_text))
        declared_lines = text_for(layout, index)
        for line in declared_lines:
            assert compact(line["text"]) in extracted, ("PDF text mismatch", index, line["text"])
            x, y, width, height = line["box"]
            margin = 24 if isinstance(identifier, int) else 18
            assert x >= margin and y >= margin and x + width <= W - margin and y + height <= H - margin, (
                "Text outside safety inset", index, line)
            if isinstance(identifier, int):
                assert line["font_size"] >= 18
        if isinstance(identifier, int):
            assert compact(manuscript[index]["text"]) in extracted
            assert compact(manuscript[index]["text"]) in compact(
                "".join(line["text"] for line in declared_lines))
            for bubble in manuscript[index].get("speech_bubbles", []):
                assert compact(bubble["text"]) in extracted
    assert visible_font_events
    filters, fonts = inspect_resources(reader)
    assert all("FlateDecode" in value for value in filters), ("Non-Flate PDF image", filters)

    changed, unchanged, outside, screens = [], [], [], []
    doc = pdfium.PdfDocument(str(pdf))
    try:
        for index in range(34):
            path = C / f"page_{index:02}.png"
            previous_index = mapping[index]
            with Image.open(path) as image:
                proof = image.convert("RGB")
            assert proof.size == (W * SCALE, H * SCALE)
            page = doc[index]
            rendered = page.render(scale=SCALE).to_pil().convert("RGB")
            assert ImageChops.difference(rendered, proof).getbbox() is None, (
                "PDF/native-proof pixel mismatch", index)
            page.close()
            proof_hash = sha(path)
            previous_hash = None
            identical = False
            baseline = None
            if previous_index is not None:
                previous_hash = old_hashes[previous_index]
                with Image.open(OLD / f"page_{previous_index:02}.png") as image:
                    baseline = image.convert("RGB")
                assert baseline.size == proof.size
                identical = proof_hash == previous_hash
            if index not in EXPECTED_CHANGED:
                assert baseline is not None
                assert identical, ("Undeclared mapped proof-byte change", index, previous_index)
                assert ImageChops.difference(proof, baseline).getbbox() is None
                unchanged.append(index)
            else:
                changed.append(index)
                if baseline is not None:
                    diff = ImageChops.difference(proof, baseline)
                    assert diff.getbbox() is not None, ("Declared change has no visible effect", index)
                if index in STRICT_DELTA:
                    mask, scopes = declared_change_mask(index, previous_index, layout,
                                                        baseline_layout, proof.size)
                    remainder = ImageChops.multiply(diff, Image.merge(
                        "RGB", [ImageChops.invert(mask)] * 3))
                    assert remainder.getbbox() is None, (
                        "Outside declared scopes changed", index, remainder.getbbox())
                    outside.append({"page": index, "baseline_page": previous_index,
                                    "outside_declared_regions_changed_pixels": 0,
                                    "boundary_allowance_proof_pixels": 3,
                                    "polygon_mapping": "actual recorded native source-box to PDF target-box",
                                    "declared_scopes": scopes})
                elif index == 31:
                    outside.append({"page": index, "baseline_page": previous_index,
                                    "additional_existing_layout_baseline_page": 31,
                                    **layout_swap_scope})
                else:
                    assert index == 4 and previous_index is None
                    outside.append({"page": 4, "baseline_page": None,
                                    "scope_type": "new source-derived page",
                                    "outside_declared_regions_changed_pixels": None,
                                    "reason": "No predecessor page; full native source/layout/identity visual review is required. Source preservation and draw provenance are checked, without a false outside-mask claim.",
                                    "current_layers": layers_for(layout, 4)})
            screens.append({"page_index": index,
                            "baseline_page_index": previous_index,
                            "pagination_status": statuses[index],
                            "dimensions": list(proof.size),
                            "png_sha256": proof_hash,
                            "v31_mapped_png_sha256": previous_hash,
                            "byte_identical_to_mapped_v31": identical})
    finally:
        doc.close()
    assert changed == EXPECTED_CHANGED and len(unchanged) == 28
    result = {"status": "MECHANICAL_PASS; EXTERNAL_ACCEPTANCE_SEPARATE",
              "revision": "V32", "baseline_commit": BASE,
              "total_pages": 34, "story_pages": 32, "trim_points": [W, H],
              "book_json_sha256": sha(L / "book.json"),
              "baseline_book_snapshot_sha256": sha(V / "BOOK_BASELINE.json"),
              "page_provenance_sha256": sha(C / "page_provenance.json"),
              "pagination_sha256": sha(V / "pagination.json"),
              "pagination": pagination,
              "pdf_sha256": sha(pdf), "pdf_bytes": pdf.stat().st_size,
              "native_text_matches_manuscript": True,
              "story_text_sniglet_at_least18pt": True,
              "story_text_safety_margin_points": 24,
              "cover_text_safety_margin_points": 18,
              "lossless_pdf_raster_matches_all34screenshots": True,
              "pdf_image_filters": filters, "embedded_fonts": fonts,
              "changed_pages": changed,
              "unchanged_pages_byte_identical_to_mapped_v31": unchanged,
              "strict_bounded_delta_pages": sorted(STRICT_DELTA),
              "outside_region_preservation": outside,
              "preserved_sources": preserved,
              "all34sealed_v31_proofs_match_git_baseline": True,
              "screenshots": screens,
              "scope": "Mapped pagination, immutable original sources, typography, lossless34-page export and strict local-delta checks. Page4 is new; page31 is a verified existing-source full layout swap, with no false bounded-delta claim. No inferred visual, clinical, child, owner or print acceptance."}
    (C / "verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                         encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("screenshots", "preserved_sources",
                                     "outside_region_preservation", "pagination")}, indent=2))


if __name__ == "__main__":
    main()
