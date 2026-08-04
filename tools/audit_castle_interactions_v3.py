#!/usr/bin/env python3
"""Blocking independent audit for Pearl Castle interaction-v3 delivery.

Pixels, anchors, placement, water contacts, provenance, and inventories are
remeasured here rather than trusted from the builder. Visible exact or near-key
magenta has a zero-pixel allowance because an opaque keyed island can cover
Roshan even when the outer cutout border is transparent.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any

from PIL import Image, ImageChops, ImageDraw

from castle_interaction_v3_specs import ADDITIONS, validate_specs


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/flats/castle/interactions_v3/castle_interactions_v3.json"
V1_MANIFEST = ROOT / "assets/flats/castle/interactions/castle_interactions.json"
V2_MANIFEST = ROOT / "assets/flats/castle/interactions_v2/castle_interactions_v2.json"
SOURCE_REPORT = ROOT / "assets_src/imagegen/castle_object_animations_v3/castle_interactions_v3_source_preparation.json"
NORMALIZATION_REPORT = ROOT / "assets/flats/castle/interactions_v3/castle_interactions_v3_normalization.json"
PREPARER = ROOT / "tools/prepare_castle_interaction_v3_sources.py"
NORMALIZER = ROOT / "tools/normalize_castle_interaction_v3_sheets.py"
BUILDER = ROOT / "tools/build_castle_interaction_v3_manifest.py"
SPECS_PATH = ROOT / "tools/castle_interaction_v3_specs.py"
FIXTURE_RUNTIME = ROOT / "scripts/arena/castle_fixture_rigs.gd"
ROOM_RUNTIME = ROOT / "scripts/arena/castle_rooms_25d.gd"
WATER_SHADER = ROOT / "assets/shaders/castle_fixture_water.gdshader"
RIPPLE_TEXTURE = ROOT / "assets/terrain/up_water_nrm.jpg"
CAUSTICS_TEXTURE = ROOT / "assets/terrain/caustics.png"
LICENSES = ROOT / "ASSET_LICENSES.md"
EXPORT_PRESETS = ROOT / "export_presets.cfg"
CI_SCRIPT = ROOT / "scripts/ci.sh"
CONTACT_SHEET = ROOT / "audit/castle_v3_work/castle_interactions_v3_contact_sheet.png"

KEY = (255, 0, 255)
ALPHA_THRESHOLD = 16
SOURCE_INSET = 4
GLOBAL_KEY_DISTANCE = 96.0
PADDING = 6
FIT_PADDING = 12
RESAMPLED_CHROMA_ALPHA_LIMIT = 96
DETACHED_ARTIFACT_MAX_PIXELS = 96
ROOM_BUDGET_BYTES = 24 * 1024 * 1024
EXPECTED_ACTIVE_ROOMS = {
    "main_hall": 13, "opera_hall": 8, "kitchen": 14, "library": 8,
    "playroom": 8, "craft_room": 8, "mermaid_pool": 4, "bubble_bath": 8,
}
EXPECTED_OVERALL_ROOMS = {**EXPECTED_ACTIVE_ROOMS, "mermaid_pool": 8}
DYNAMIC_WATER_IDS = {"kitchen_seafoam_kettle", "bubble_bath_shell_shower"}
NEW_JOLT_IDS = {"playroom_rocking_horse", "mermaid_pool_sailboat"}
ROOM_LOGICAL_SIZE = {
    **{room: (1024.0, 576.0) for room in EXPECTED_ACTIVE_ROOMS},
    "main_hall": (3344.0, 941.0),
}
RETIRED_V2_ASSET_IDS = {"main_hall_tapestry"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_text_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def add_error(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        add_error(errors, f"missing required JSON: {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"cannot read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        add_error(errors, f"{path.relative_to(ROOT)} is not a JSON object")
        return {}
    return value


def index_assets(values: Any, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(values, list):
        add_error(errors, f"{label} is not a list")
        return result
    for value in values:
        if not isinstance(value, dict) or not str(value.get("id", "")):
            add_error(errors, f"{label} contains an invalid record")
            continue
        asset_id = str(value["id"])
        if asset_id in result:
            add_error(errors, f"{label} contains duplicate id {asset_id}")
        result[asset_id] = value
    return result


def without_pack(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("pack", None)
    return result


def frame_cells(sheet: Image.Image) -> tuple[list[Image.Image], int]:
    if sheet.width % 4 or sheet.height % 2:
        raise ValueError("sheet is not an exact 4x2 grid")
    cell = sheet.width // 4
    if sheet.height // 2 != cell:
        raise ValueError("sheet cells are not square")
    frames = []
    for index in range(8):
        column, row = index % 4, index // 4
        frames.append(sheet.crop((column * cell, row * cell,
                                  (column + 1) * cell, (row + 1) * cell)))
    return frames, cell


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int]:
    bbox = frame.getchannel("A").point(
        lambda value: 255 if value >= ALPHA_THRESHOLD else 0
    ).getbbox()
    if bbox is None:
        raise ValueError("frame has no visible alpha silhouette")
    return bbox


def anchor_point(frame: Image.Image, bbox: tuple[int, int, int, int], mode: str) -> tuple[float, float]:
    left, top, right, bottom = bbox
    if mode == "center":
        return ((left + right) * 0.5, (top + bottom) * 0.5)
    height = bottom - top
    band_height = max(5, int(round(height * 0.12)))
    band_top = top if mode == "top_center" else max(top, bottom - band_height)
    band_bottom = min(bottom, top + band_height) if mode == "top_center" else bottom
    band = frame.getchannel("A").crop((0, band_top, frame.width, band_bottom))
    band_bbox = band.point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    anchor_x = (left + right) * 0.5
    if band_bbox is not None:
        anchor_x = (band_bbox[0] + band_bbox[2]) * 0.5
    return (anchor_x, float(top if mode == "top_center" else bottom))


def measured_alpha(frame: Image.Image) -> tuple[dict[str, Any], int]:
    bbox = alpha_bbox(frame)
    alpha = frame.getchannel("A")
    histogram = alpha.histogram()
    exact = near = hidden_rgb = 0
    for red, green, blue, alpha_value in frame.getdata():
        if alpha_value == 0 and (red or green or blue):
            hidden_rgb += 1
        if alpha_value < ALPHA_THRESHOLD:
            continue
        if (red, green, blue) == KEY:
            exact += 1
        if red >= 220 and blue >= 220 and green <= 55:
            near += 1
    border = (list(alpha.crop((0, 0, frame.width, 1)).getdata())
              + list(alpha.crop((0, frame.height - 1, frame.width, frame.height)).getdata())
              + list(alpha.crop((0, 0, 1, frame.height)).getdata())
              + list(alpha.crop((frame.width - 1, 0, frame.width, frame.height)).getdata()))
    visible = sum(histogram[ALPHA_THRESHOLD:])
    return ({
        "alpha_bbox": list(bbox), "visible_pixels": visible,
        "transparent_pixels": histogram[0],
        "partial_alpha_pixels": sum(histogram[1:255]),
        "opaque_pixels": histogram[255],
        "visible_exact_chroma_pixels": exact,
        "visible_near_chroma_pixels": near,
        "visible_near_chroma_ratio": round(near / float(max(1, visible)), 9),
        "transparent_canvas_border": all(value == 0 for value in border),
    }, hidden_rgb)


def material_changed_fraction(base: Image.Image, frame: Image.Image) -> float:
    base_rgba, frame_rgba = base.convert("RGBA"), frame.convert("RGBA")
    visible = ImageChops.lighter(base_rgba.getchannel("A"), frame_rgba.getchannel("A")).point(
        lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
    channels = ImageChops.difference(base_rgba, frame_rgba).split()
    rgb = ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]), channels[2])
    changed = ImageChops.lighter(rgb.point(lambda value: 255 if value >= 18 else 0),
                                 channels[3].point(lambda value: 255 if value >= 16 else 0))
    changed = ImageChops.multiply(changed, visible)
    return changed.histogram()[255] / float(max(1, visible.histogram()[255]))


def source_has_exact_inset(image: Image.Image, frame_index: int) -> bool:
    column, row = frame_index % 4, frame_index // 4
    cell = image.crop((column * 256, row * 256,
                       (column + 1) * 256, (row + 1) * 256)).convert("RGB")
    for y in range(256):
        for x in range(256):
            if (x < SOURCE_INSET or y < SOURCE_INSET
                    or x >= 256 - SOURCE_INSET or y >= 256 - SOURCE_INSET) \
                    and cell.getpixel((x, y)) != KEY:
                return False
    return True


def anchor_pixel(cell: int, padding: float, mode: str) -> tuple[float, float]:
    if mode == "top_center":
        return (cell * 0.5, padding)
    if mode == "bottom_center":
        return (cell * 0.5, cell - padding)
    return (cell * 0.5, cell * 0.5)


def target_anchor(size: list[Any], mode: str, hall: bool) -> tuple[float, float]:
    width, height = float(size[0]), float(size[1])
    if hall:
        return ((0.0, -height * 0.5) if mode == "top_center" else
                (0.0, height * 0.5) if mode == "bottom_center" else (0.0, 0.0))
    return ((width * 0.5, 0.0) if mode == "top_center" else
            (width * 0.5, height) if mode == "bottom_center" else
            (width * 0.5, height * 0.5))


def expected_runtime_mapping(spec: dict[str, Any], normalized: dict[str, Any], cell: int) -> dict[str, Any]:
    boxes = [tuple(float(component) for component in value)
             for value in normalized.get("frame_bboxes", [])]
    if len(boxes) != 8:
        raise ValueError("normalization has no eight frame bounds")
    mode = str(spec["anchor_mode"])
    padding = float(normalized.get("padding_pixels", PADDING))
    anchor = anchor_pixel(cell, padding, mode)
    extents = {
        "left": max(anchor[0] - value[0] for value in boxes),
        "right": max(value[2] - anchor[0] for value in boxes),
        "up": max(anchor[1] - value[1] for value in boxes),
        "down": max(value[3] - anchor[1] for value in boxes),
    }
    width, height = (float(value) for value in spec["placement_size"])
    if mode == "top_center":
        available = {"left": width * 0.5, "right": width * 0.5,
                     "up": 0.0, "down": height}
    elif mode == "bottom_center":
        available = {"left": width * 0.5, "right": width * 0.5,
                     "up": height, "down": 0.0}
    else:
        available = {"left": width * 0.5, "right": width * 0.5,
                     "up": height * 0.5, "down": height * 0.5}
    scales = []
    for key, extent in extents.items():
        if extent <= 0.001:
            continue
        if available[key] <= 0.0:
            raise ValueError(f"{mode} anchor crosses placement {key} edge")
        scales.append(available[key] / extent)
    scale = min(scales)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("runtime scale is not finite and positive")
    hall = str(spec["room"]) == "main_hall"
    desired = target_anchor(spec["placement_size"], mode, hall)
    relative = ((anchor[0] - cell * 0.5) * scale,
                (anchor[1] - cell * 0.5) * scale)
    offset = [round(desired[0] - relative[0], 6),
              round(desired[1] - relative[1], 6)]
    mapped = [[
        round(offset[0] + (box[0] - cell * 0.5) * scale, 6),
        round(offset[1] + (box[1] - cell * 0.5) * scale, 6),
        round(offset[0] + (box[2] - cell * 0.5) * scale, 6),
        round(offset[1] + (box[3] - cell * 0.5) * scale, 6),
    ] for box in boxes]
    limits = ((-width * 0.5, -height * 0.5, width * 0.5, height * 0.5)
              if hall else (0.0, 0.0, width, height))
    return {
        "runtime_scale": round(scale, 9),
        "runtime_center_offset": offset if not hall else copy.deepcopy(spec["runtime_center_offset"]),
        "hall_center_offset": offset if hall else copy.deepcopy(spec["hall_center_offset"]),
        "source_anchor_pixel": [round(anchor[0], 6), round(anchor[1], 6)],
        "target_anchor": [round(desired[0], 6), round(desired[1], 6)],
        "union_anchor_extents": {key: round(value, 6) for key, value in extents.items()},
        "mapped_frame_bounds": mapped,
        "placement_limits": [round(value, 6) for value in limits],
        "fit_method": "uniform_scale_all_frame_alpha_extents_about_fixed_anchor",
    }


def numbers_in_unit_interval(value: Any) -> bool:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return math.isfinite(float(value)) and 0.0 <= float(value) <= 1.0
    return isinstance(value, (list, tuple)) and all(
        numbers_in_unit_interval(item) for item in value)


def point_to_runtime_pixel(entry: dict[str, Any], point: list[Any], cell: int) -> tuple[float, float]:
    width, height = (float(value) for value in entry["placement_size"])
    hall = str(entry["room"]) == "main_hall"
    if hall:
        target = ((float(point[0]) - 0.5) * width,
                  (float(point[1]) - 0.5) * height)
        offset = entry["hall_center_offset"]
    else:
        target = (float(point[0]) * width, float(point[1]) * height)
        offset = entry["runtime_center_offset"]
    scale = float(entry["runtime_scale"])
    return (cell * 0.5 + (target[0] - float(offset[0])) / scale,
            cell * 0.5 + (target[1] - float(offset[1])) / scale)


def distance_to_visible_alpha(frame: Image.Image, point: tuple[float, float]) -> float:
    alpha = frame.getchannel("A")
    px, py = point
    best = math.inf
    for y in range(frame.height):
        for x in range(frame.width):
            if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD:
                best = min(best, math.hypot((x + 0.5) - px, (y + 0.5) - py))
    return best


def midpoint(first: list[Any], second: list[Any]) -> list[float]:
    return [(float(first[0]) + float(second[0])) * 0.5,
            (float(first[1]) + float(second[1])) * 0.5]


def audit_water_contact(spec: dict[str, Any], entry: dict[str, Any],
                        frames: list[Image.Image], cell: int, errors: list[str]) -> None:
    asset_id = str(spec["id"])
    frame = frames[4]
    for layer in spec["water_layers"]:
        role, shape = str(layer.get("role", "water")), str(layer.get("shape", ""))
        if shape == "polygon":
            point_frames = layer.get("points_frames", [])
            points = point_frames[4] if point_frames else layer.get("points", [])
            if not isinstance(points, list) or len(points) < 3:
                add_error(errors, f"{asset_id}: {role} has invalid polygon geometry")
                continue
            if bool(layer.get("stream", False)):
                outlet = point_to_runtime_pixel(entry, midpoint(points[0], points[1]), cell)
                distance = distance_to_visible_alpha(frame, outlet)
                if distance > cell * 0.14:
                    add_error(errors, f"{asset_id}: {role} outlet misses frame-4 alpha by {distance:.1f}px")
                endpoint = point_to_runtime_pixel(entry, midpoint(points[-2], points[-1]), cell)
                distance = distance_to_visible_alpha(frame, endpoint)
                if distance > cell * 0.24:
                    add_error(errors, f"{asset_id}: {role} endpoint misses its cavity by {distance:.1f}px")
        elif shape == "ellipse":
            center, radius = layer.get("center", []), layer.get("radius", [])
            if not (isinstance(center, list) and len(center) == 2
                    and isinstance(radius, list) and len(radius) == 2):
                add_error(errors, f"{asset_id}: {role} has invalid ellipse geometry")
                continue
            cx, cy = (float(value) for value in center)
            rx, ry = (float(value) for value in radius)
            candidates = [[cx, cy], [cx-rx, cy], [cx+rx, cy], [cx, cy-ry], [cx, cy+ry]]
            distance = min(distance_to_visible_alpha(
                frame, point_to_runtime_pixel(entry, value, cell)) for value in candidates)
            if distance > cell * 0.24:
                add_error(errors, f"{asset_id}: {role} misses frame-4 object alpha by {distance:.1f}px")


def audit_hotspot(spec: dict[str, Any], errors: list[str]) -> None:
    asset_id = str(spec["id"])
    width, height = (float(value) for value in spec["hotspot_size"])
    if width < 112.0 or height < 112.0:
        add_error(errors, f"{asset_id}: hotspot {width:g}x{height:g} is below 112x112")
    x = float(spec["position"][0]) + float(spec["hotspot_offset"][0])
    y = float(spec["position"][1]) + float(spec["hotspot_offset"][1])
    room_width, room_height = ROOM_LOGICAL_SIZE[str(spec["room"])]
    if x < 0.0 or y < 0.0 or x + width > room_width or y + height > room_height:
        add_error(errors, f"{asset_id}: hotspot leaves {spec['room']} logical bounds")


def audit_prepared_source(spec: dict[str, Any], entry: dict[str, Any],
                          prepared: dict[str, Any], errors: list[str]) -> None:
    asset_id = str(spec["id"])
    path = ROOT / str(prepared.get("path", ""))
    if not path.is_file():
        add_error(errors, f"{asset_id}: prepared source is missing")
        return
    actual_hash = sha256(path)
    if actual_hash != prepared.get("prepared_sha256"):
        add_error(errors, f"{asset_id}: prepared source hash is stale")
    if entry.get("raw_chroma_master") != path.relative_to(ROOT).as_posix() \
            or entry.get("raw_chroma_master_sha256") != actual_hash:
        add_error(errors, f"{asset_id}: manifest prepared-source path/hash differs")
    with Image.open(path) as image_value:
        source, original_mode = image_value.convert("RGB"), image_value.mode
    if source.size != (1024, 512) or original_mode != "RGB":
        add_error(errors, f"{asset_id}: prepared source is not 1024x512 RGB")
        return
    for index in range(8):
        if not source_has_exact_inset(source, index):
            add_error(errors, f"{asset_id}: source frame {index} lacks exact 4px key inset")
    expected_fields = {
        "grid": [4, 2], "cell_size": [256, 256],
        "prepared_dimensions": [1024, 512], "exact_chroma_inset_pixels": 4,
        "whole_cell_uniform_scale_only": True,
        "connected_outer_field_plus_global_near_key": True,
        "global_key_distance": GLOBAL_KEY_DISTANCE,
        "subject_geometry_warped": False, "state_pixels_synthesized": False,
    }
    for key, value in expected_fields.items():
        if prepared.get(key) != value:
            add_error(errors, f"{asset_id}: prepared-source {key} evidence differs")
    if int(prepared.get("key_field_pixels_normalized", -1)) <= 0 \
            or int(prepared.get("global_near_key_pixels_normalized", -1)) < 0:
        add_error(errors, f"{asset_id}: key normalization metrics are missing")
    preparation_evidence = entry.get("source_preparation", {})
    expected_preparation = {
        "report": SOURCE_REPORT.relative_to(ROOT).as_posix(),
        "report_sha256": repository_text_sha256(SOURCE_REPORT),
        "native_copy_sha256": prepared.get("native_copy_sha256"),
        "prepared_sha256": prepared.get("prepared_sha256"),
        "prepared_dimensions": prepared.get("prepared_dimensions"),
        "exact_chroma_inset_pixels": prepared.get("exact_chroma_inset_pixels"),
        "whole_cell_uniform_scale_only": True,
        "connected_outer_field_plus_global_near_key": True,
        "key_field_pixels_normalized": prepared.get("key_field_pixels_normalized"),
        "global_near_key_pixels_normalized": prepared.get("global_near_key_pixels_normalized"),
        "global_key_distance": GLOBAL_KEY_DISTANCE,
        "edge_despill_pixels": prepared.get("edge_despill_pixels"),
        "subject_geometry_warped": False,
        "state_pixels_synthesized": False,
    }
    for key, value in expected_preparation.items():
        if preparation_evidence.get(key) != value:
            add_error(errors, f"{asset_id}: manifest preparation {key} differs")
    provenance = prepared.get("provenance", {})
    if not isinstance(provenance, dict):
        add_error(errors, f"{asset_id}: provenance is invalid")
        return
    ledger = ROOT / str(provenance.get("batch_manifest", ""))
    if not ledger.is_file() or provenance.get("batch_manifest_sha256") != repository_text_sha256(ledger):
        add_error(errors, f"{asset_id}: provenance ledger path/hash is stale")
    prompt = str(provenance.get("accepted_prompt", ""))
    if not prompt or provenance.get("accepted_prompt_sha256") != text_sha256(prompt):
        add_error(errors, f"{asset_id}: accepted prompt evidence is stale")
    if not re.fullmatch(r"[0-9a-f]{64}", str(provenance.get("accepted_native_sha256", ""))):
        add_error(errors, f"{asset_id}: accepted native hash is invalid")
    dimensions = provenance.get("accepted_native_dimensions", [])
    if not (isinstance(dimensions, list) and len(dimensions) == 2
            and all(isinstance(value, int) and value > 0 for value in dimensions)):
        add_error(errors, f"{asset_id}: accepted native dimensions are invalid")
    review = str(provenance.get("codex_visual_review_status", "")).lower()
    if not (review.startswith("accepted") or review.startswith("pass")):
        add_error(errors, f"{asset_id}: Codex visual review is not accepted")
    if not str(provenance.get("human_review_status", "pending")).lower().startswith("pending"):
        add_error(errors, f"{asset_id}: provenance incorrectly claims human acceptance")
    if int(provenance.get("accepted_attempt", 0)) < 1 or entry.get("provenance") != provenance:
        add_error(errors, f"{asset_id}: accepted-attempt/manifest provenance differs")
    if entry.get("accepted_native_sha256") != provenance.get("accepted_native_sha256"):
        add_error(errors, f"{asset_id}: manifest native hash differs")
    if (entry.get("provenance_manifest") != ledger.relative_to(ROOT).as_posix()
            or entry.get("provenance_manifest_sha256") != repository_text_sha256(ledger)):
        add_error(errors, f"{asset_id}: manifest provenance path/hash differs")


def audit_runtime_sheet(spec: dict[str, Any], entry: dict[str, Any],
                        normalized: dict[str, Any], errors: list[str]) -> tuple[list[Image.Image], int] | None:
    asset_id = str(spec["id"])
    path = ROOT / str(normalized.get("runtime_path", ""))
    if not path.is_file():
        add_error(errors, f"{asset_id}: runtime sheet is missing")
        return None
    actual_hash = sha256(path)
    if actual_hash != normalized.get("runtime_sha256"):
        add_error(errors, f"{asset_id}: normalization runtime hash is stale")
    if entry.get("sheet") != path.relative_to(ROOT).as_posix() or entry.get("sheet_sha256") != actual_hash:
        add_error(errors, f"{asset_id}: manifest runtime path/hash differs")
    with Image.open(path) as image_value:
        original_mode, sheet = image_value.mode, image_value.convert("RGBA")
    if original_mode != "RGBA":
        add_error(errors, f"{asset_id}: runtime sheet is not RGBA")
    try:
        frames, cell = frame_cells(sheet)
    except ValueError as exc:
        add_error(errors, f"{asset_id}: {exc}")
        return None
    expected_cell = int(spec["runtime_cell_size"])
    if cell != expected_cell or list(sheet.size) != [expected_cell * 4, expected_cell * 2]:
        add_error(errors, f"{asset_id}: runtime dimensions differ from spec")
    if max(sheet.size) > 1024:
        add_error(errors, f"{asset_id}: runtime sheet exceeds 1024px")
    boxes = [alpha_bbox(frame) for frame in frames]
    hashes = [hashlib.sha256(frame.tobytes()).hexdigest() for frame in frames]
    serialized_boxes = [list(value) for value in boxes]
    if len(set(hashes)) != 8:
        add_error(errors, f"{asset_id}: eight authored states are not distinct")
    if normalized.get("frame_sha256") != hashes or entry.get("frame_sha256") != hashes:
        add_error(errors, f"{asset_id}: frame hashes are stale")
    if normalized.get("frame_bboxes") != serialized_boxes or entry.get("frame_bboxes") != serialized_boxes:
        add_error(errors, f"{asset_id}: frame bounds are stale")
    mode = str(spec["anchor_mode"])
    anchors = [anchor_point(frame, box, mode) for frame, box in zip(frames, boxes)]
    spread = [round(max(value[0] for value in anchors) - min(value[0] for value in anchors), 3),
              round(max(value[1] for value in anchors) - min(value[1] for value in anchors), 3)]
    if spread[0] > 1.5 or spread[1] > 1.5:
        add_error(errors, f"{asset_id}: fixed anchor drifts {spread}")
    if normalized.get("anchor_spread_pixels") != spread:
        add_error(errors, f"{asset_id}: anchor-spread evidence is stale")
    edge_gap = min(min(box[0], box[1], cell-box[2], cell-box[3]) for box in boxes)
    if edge_gap < PADDING:
        add_error(errors, f"{asset_id}: alpha padding is only {edge_gap}px")
    normalization_evidence = entry.get("normalization", {})
    expected_normalization = {
        "report": NORMALIZATION_REPORT.relative_to(ROOT).as_posix(),
        "report_sha256": repository_text_sha256(NORMALIZATION_REPORT),
        "source_preparation_report": SOURCE_REPORT.relative_to(ROOT).as_posix(),
        "source_preparation_report_sha256": repository_text_sha256(SOURCE_REPORT),
        "source_sha256": normalized.get("source_sha256"),
        "runtime_sha256": normalized.get("runtime_sha256"),
        "uniform_scale": normalized.get("uniform_scale"),
        "padding_pixels": normalized.get("padding_pixels"),
        "edge_gap_pixels": normalized.get("edge_gap_pixels"),
        "anchor_spread_pixels": normalized.get("anchor_spread_pixels"),
        "changed_fraction_from_rest": normalized.get("changed_fraction_from_rest"),
        "fixed_anchor_translation_only": True,
        "one_uniform_scale_across_all_frames": True,
        "per_frame_scale_used": False,
        "subject_geometry_warped": False,
        "state_pixels_synthesized": False,
        "whole_object_translation_only": True,
        "repainted_pixels": False,
    }
    for key, value in expected_normalization.items():
        if normalization_evidence.get(key) != value:
            add_error(errors, f"{asset_id}: manifest normalization {key} differs")
    if (int(normalized.get("padding_pixels", -1)) != PADDING
            or int(normalized.get("fit_padding_pixels", -1)) != FIT_PADDING
            or int(normalized.get("edge_gap_pixels", -1)) != edge_gap):
        add_error(errors, f"{asset_id}: padding evidence differs from pixels")
    uniform_scale = float(normalized.get("uniform_scale", math.nan))
    if not math.isfinite(uniform_scale) or uniform_scale <= 0.0:
        add_error(errors, f"{asset_id}: normalization scale is invalid")
    expected_flags = {
        "one_uniform_scale_across_all_frames": True,
        "per_frame_scale_used": False,
        "fixed_anchor_translation_only": True,
        "subject_geometry_warped": False,
        "state_pixels_synthesized": False,
        "primary_animation_is_overlay": False,
    }
    for key, value in expected_flags.items():
        if normalized.get(key) != value:
            add_error(errors, f"{asset_id}: normalization {key} contract differs")
    if int(normalized.get("detached_artifact_max_pixels", -1)) != DETACHED_ARTIFACT_MAX_PIXELS:
        add_error(errors, f"{asset_id}: detached-artifact limit is stale")
    removed = normalized.get("resampled_chroma_pixels_removed", [])
    if not isinstance(removed, list) or len(removed) != 8 \
            or int(normalized.get("resampled_chroma_alpha_limit", -1)) != RESAMPLED_CHROMA_ALPHA_LIMIT:
        add_error(errors, f"{asset_id}: resampled-chroma evidence is incomplete")
    corrections = normalized.get("anchor_translation_corrections", [])
    if not isinstance(corrections, list) or len(corrections) != 8:
        add_error(errors, f"{asset_id}: anchor correction evidence is incomplete")

    recorded_qa = normalized.get("per_frame_alpha_qa", [])
    manifest_qa = entry.get("normalization", {}).get("per_frame_alpha_qa", [])
    if not isinstance(recorded_qa, list) or len(recorded_qa) != 8:
        add_error(errors, f"{asset_id}: per-frame alpha QA is incomplete")
        recorded_qa = []
    if not isinstance(manifest_qa, list) or len(manifest_qa) != 8:
        add_error(errors, f"{asset_id}: manifest per-frame alpha QA is incomplete")
        manifest_qa = []
    visible_counts = []
    for index, frame in enumerate(frames):
        measured, hidden_rgb = measured_alpha(frame)
        visible_counts.append(measured["visible_pixels"])
        if index >= len(recorded_qa) or recorded_qa[index] != measured:
            add_error(errors, f"{asset_id}: frame {index} alpha QA is stale")
        if index >= len(manifest_qa) or manifest_qa[index] != measured:
            add_error(errors, f"{asset_id}: frame {index} manifest alpha QA is stale")
        if not measured["transparent_canvas_border"]:
            add_error(errors, f"{asset_id}: frame {index} touches canvas border")
        if measured["visible_exact_chroma_pixels"]:
            add_error(errors, f"{asset_id}: frame {index} retains visible #FF00FF")
        if measured["visible_near_chroma_pixels"] or measured["visible_near_chroma_ratio"]:
            add_error(errors, f"{asset_id}: frame {index} retains visible near-key magenta")
        if hidden_rgb:
            add_error(errors, f"{asset_id}: frame {index} retains RGB under zero alpha")
        if measured["partial_alpha_pixels"] <= 0:
            add_error(errors, f"{asset_id}: frame {index} lacks an antialiased matte")
        if measured["visible_pixels"] < 100:
            add_error(errors, f"{asset_id}: frame {index} lacks a usable silhouette")
    if visible_counts and min(visible_counts) / float(max(visible_counts)) < 0.12:
        add_error(errors, f"{asset_id}: a frame collapses to a detached fragment")
    measured_changes = [round(material_changed_fraction(frames[0], frame), 8) for frame in frames]
    if normalized.get("changed_fraction_from_rest") != measured_changes:
        add_error(errors, f"{asset_id}: changed-fraction evidence is stale")
    if any(value <= 0.001 for value in measured_changes[1:]):
        add_error(errors, f"{asset_id}: a non-rest state has no material object change")
    if max(measured_changes[1:], default=0.0) < 0.05:
        add_error(errors, f"{asset_id}: sequence lacks a material use animation")
    return frames, cell


def audit_addition(spec: dict[str, Any], entry: dict[str, Any], prepared: dict[str, Any],
                   normalized: dict[str, Any], errors: list[str]) -> None:
    asset_id = str(spec["id"])
    audit_hotspot(spec, errors)
    expected = {
        "pack": "v3_addition", "room": spec["room"], "item_id": spec["item"],
        "instances": [spec["item"]], "name": spec["name"],
        "placement_position": spec["position"], "placement_position_mode": spec["position_mode"],
        "placement_size": spec["placement_size"], "hotspot_size": spec["hotspot_size"],
        "hotspot_offset": spec["hotspot_offset"], "z": spec["z"], "color": spec["color"],
        "semantic_action": spec["semantic_action"], "render_mode": "generated_full_object_states",
        "frame_count": 8, "hframes": 4, "vframes": 2,
        "sound": spec["sound"], "sound_frame": spec["sound_frame"],
        "pitch": spec["pitch"], "frame_duration_seconds": spec["frame_duration_seconds"],
        "fixed_pivot": True,
        "root_transform_animation": spec["physics_mode"] != "none",
        "secondary_root_physics": spec["physics_mode"] != "none",
        "grid": [4, 2], "authored_frame_count": 8,
        "timeline_sequence": spec["timeline_sequence"],
        "timeline_frame_count": spec["timeline_frame_count"], "rest_frame": spec["rest_frame"],
        "anchor_mode": spec["anchor_mode"], "physics_mode": spec["physics_mode"],
        "physics_pivot": spec["physics_pivot"],
        "physics_max_angle_radians": spec["physics_max_angle_radians"],
        "physics_impulse_scale": spec["physics_impulse_scale"],
        "water_layers": json.loads(json.dumps(spec["water_layers"])),
        "primary_animation_is_overlay": False,
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            add_error(errors, f"{asset_id}: manifest {key} differs from specs")
    sound_path = ROOT / str(spec["sound"])
    if not sound_path.is_file():
        add_error(errors, f"{asset_id}: declared interaction sound is missing")
    timeline = entry.get("timeline_sequence", [])
    if not isinstance(timeline, list) or not 4 <= len(timeline) <= 12 or set(timeline) != set(range(8)):
        add_error(errors, f"{asset_id}: timeline violates 4-12/all-eight-state contract")
    if entry.get("normalized_use_review") != "codex_visual_review_accepted_2026-08-02":
        add_error(errors, f"{asset_id}: normalized-use review is missing")
    if not str(entry.get("human_visual_review", "pending")).lower().startswith("pending"):
        add_error(errors, f"{asset_id}: manifest incorrectly claims human acceptance")
    audit_prepared_source(spec, entry, prepared, errors)
    result = audit_runtime_sheet(spec, entry, normalized, errors)
    if result is None:
        return
    frames, cell = result
    try:
        mapping = expected_runtime_mapping(spec, normalized, cell)
    except (KeyError, TypeError, ValueError) as exc:
        add_error(errors, f"{asset_id}: cannot derive runtime mapping: {exc}")
        return
    if entry.get("runtime_mapping") != mapping or entry.get("runtime_scale") != mapping["runtime_scale"]:
        add_error(errors, f"{asset_id}: runtime mapping/scale differs from measured alpha")
    if entry.get("runtime_center_offset") != mapping["runtime_center_offset"] \
            or entry.get("hall_center_offset") != mapping["hall_center_offset"]:
        add_error(errors, f"{asset_id}: runtime anchor offset differs")
    limits = mapping["placement_limits"]
    for index, box in enumerate(mapping["mapped_frame_bounds"]):
        if (box[0] < limits[0]-0.05 or box[1] < limits[1]-0.05
                or box[2] > limits[2]+0.05 or box[3] > limits[3]+0.05):
            add_error(errors, f"{asset_id}: mapped frame {index} exceeds placement")
    for layer in spec["water_layers"]:
        shape = str(layer.get("shape", ""))
        coordinates = ([layer.get("points", [])] if shape == "polygon" else
                       [layer.get("center", []), layer.get("radius", [])])
        coordinates.extend(layer.get("points_frames", []))
        if shape not in {"polygon", "ellipse"} or not all(
                numbers_in_unit_interval(value) for value in coordinates):
            add_error(errors, f"{asset_id}: water geometry leaves object-local [0,1]")
        if shape == "ellipse":
            center, radius = layer.get("center", []), layer.get("radius", [])
            if (isinstance(center, list) and len(center) == 2
                    and isinstance(radius, list) and len(radius) == 2
                    and (float(center[0])-float(radius[0]) < 0.0
                         or float(center[1])-float(radius[1]) < 0.0
                         or float(center[0])+float(radius[0]) > 1.0
                         or float(center[1])+float(radius[1]) > 1.0)):
                add_error(errors, f"{asset_id}: water ellipse leaves object-local bounds")
        active = layer.get("active_frames", [])
        if active and (not isinstance(active, list)
                       or any(not isinstance(value, int) or value not in range(8) for value in active)):
            add_error(errors, f"{asset_id}: water active_frames are invalid")
    if asset_id in DYNAMIC_WATER_IDS:
        if timeline != [0, 1, 2, 3, 4, 4, 4, 5, 6, 7]:
            add_error(errors, f"{asset_id}: dry/open/flow-hold timeline differs")
        streams = [layer for layer in spec["water_layers"] if bool(layer.get("stream", False))]
        if len(streams) != 1:
            add_error(errors, f"{asset_id}: dynamic fixture lacks one stream")
        else:
            point_frames = streams[0].get("points_frames", [])
            if not isinstance(point_frames, list) or len(point_frames) != 8:
                add_error(errors, f"{asset_id}: stream lacks eight outlet geometries")
            elif len({json.dumps(value, sort_keys=True) for value in point_frames}) < 4:
                add_error(errors, f"{asset_id}: outlet geometry barely changes")
            if streams[0].get("active_frames") != [4]:
                add_error(errors, f"{asset_id}: stream must activate only on atlas frame 4")
        if any(layer.get("active_frames") != [4] for layer in spec["water_layers"]):
            add_error(errors, f"{asset_id}: all fluid layers must use atlas frame 4")
    if spec["water_layers"]:
        audit_water_contact(spec, entry, frames, cell, errors)


def audit_runtime_contract(manifest: dict[str, Any], assets: list[dict[str, Any]],
                           errors: list[str]) -> None:
    contract = manifest.get("contract", {})
    expected = {
        "water_renderer": WATER_SHADER.relative_to(ROOT).as_posix(),
        "water_renderer_sha256": sha256(WATER_SHADER),
        "water_ripple_texture": RIPPLE_TEXTURE.relative_to(ROOT).as_posix(),
        "water_ripple_texture_sha256": sha256(RIPPLE_TEXTURE),
        "water_caustics_texture": CAUSTICS_TEXTURE.relative_to(ROOT).as_posix(),
        "water_caustics_texture_sha256": sha256(CAUSTICS_TEXTURE),
        "water_node_type": "Sprite3D", "water_material_type": "ShaderMaterial",
        "water_depth_write": False,
        "water_geometry_source": "per_asset_manifest_layers",
        "water_mask_source": "runtime_cached_exact_polygon_image_texture",
        "water_dynamic_geometry_source": "authored_atlas_frame_index",
        "jolt_body_cap": 12, "jolt_awake_cap": 8, "jolt_logic_authority": False,
        "room_decoded_rgba_budget_bytes": ROOM_BUDGET_BYTES,
        "retired_v2_pool_reintroduced": False,
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            add_error(errors, f"runtime contract {key} differs")
    fixture_source = FIXTURE_RUNTIME.read_text(encoding="utf-8")
    room_source = ROOM_RUNTIME.read_text(encoding="utf-8")
    fixture_code = "\n".join(line.split("#", 1)[0] for line in fixture_source.splitlines())
    shader_source = WATER_SHADER.read_text(encoding="utf-8")
    required_fixture = [
        "Sprite3D.new()", "ShaderMaterial.new()", "material.shader = WATER_SHADER",
        "points_frames", "active_frames", "water_frame_index", "atlas_frame: int = -1",
        "MAX_JOLT_BODIES := 12", "MAX_AWAKE_BODIES := 8",
    ]
    for token in required_fixture:
        if token not in fixture_code:
            add_error(errors, f"fixture runtime lacks {token}")
    if "MeshInstance3D" in fixture_code:
        add_error(errors, "fixture runtime uses forbidden MeshInstance3D water")
    if "shader_type spatial" not in shader_source or "depth_draw_never" not in shader_source:
        add_error(errors, "water shader does not preserve transparent depth")
    if "depth_draw_opaque" in shader_source:
        add_error(errors, "water shader writes opaque depth")
    for token in ["items.append_array(fixture_rigs.room_additions(room_id))",
                  "fixture_rigs.apply_frame(", "atlas_frame"]:
        if token not in room_source:
            add_error(errors, f"room runtime lacks {token}")
    if re.search(r'if\s+room_id\s*==\s*"mermaid_pool"\s*:\s*\n\s*v2_visual\s*=\s*\{\}',
                 room_source):
        add_error(errors, "room runtime blanket-clears new Mermaid Pool visuals")
    if "res://assets/flats/castle/interactions_v3/castle_interactions_v3.json" not in fixture_source:
        add_error(errors, "fixture runtime does not declare v3 manifest")
    jolt = sum(str(value.get("physics_mode", "none")) != "none" for value in assets)
    water = sum(bool(value.get("water_layers", [])) for value in assets)
    if jolt != 8 or water != 10:
        add_error(errors, f"active mechanics count is Jolt={jolt}, water={water}")


def audit_declarations(additions: list[dict[str, Any]],
                       prepared_index: dict[str, dict[str, Any]], errors: list[str]) -> None:
    licenses = LICENSES.read_text(encoding="utf-8")
    for entry in additions:
        prepared = prepared_index.get(str(entry["id"]), {})
        for path_value in [prepared.get("path", ""), entry.get("sheet", "")]:
            if path_value and str(path_value) not in licenses:
                add_error(errors, f"ASSET_LICENSES omits {path_value}")
        provenance = prepared.get("provenance", {})
        ledger = str(provenance.get("batch_manifest", "")) if isinstance(provenance, dict) else ""
        if ledger and ledger not in licenses:
            add_error(errors, f"ASSET_LICENSES omits {ledger}")
    for path in [SOURCE_REPORT, NORMALIZATION_REPORT, MANIFEST]:
        relative = path.relative_to(ROOT).as_posix()
        if relative not in licenses:
            add_error(errors, f"ASSET_LICENSES omits {relative}")
    export_text = EXPORT_PRESETS.read_text(encoding="utf-8")
    if export_text.count(MANIFEST.relative_to(ROOT).as_posix()) < 2:
        add_error(errors, "Android/Windows export declarations omit v3 manifest")
    ci_text = CI_SCRIPT.read_text(encoding="utf-8")
    audit_commands = ("python tools/audit_castle_interactions_v3.py",
                      "python3 tools/audit_castle_interactions_v3.py")
    if not any(command in ci_text for command in audit_commands):
        add_error(errors, "scripts/ci.sh does not run v3 static audit")


def decoded_rgba_by_room(assets: list[dict[str, Any]], legacy: list[dict[str, Any]],
                         errors: list[str]) -> dict[str, int]:
    totals: Counter[str] = Counter()
    seen: set[tuple[str, str]] = set()
    for entry in [*assets, *legacy]:
        path_value = str(entry.get("sheet", entry.get("atlas", "")))
        path = ROOT / path_value
        key = (str(entry.get("room", "")), path.resolve().as_posix())
        if key in seen:
            continue
        seen.add(key)
        if not path.is_file():
            add_error(errors, f"decoded-budget visual is missing: {path_value}")
            continue
        with Image.open(path) as image_value:
            width, height = image_value.size
        totals[str(entry.get("room", ""))] += width * height * 4
    result = dict(sorted(totals.items()))
    for room, value in result.items():
        if value > ROOM_BUDGET_BYTES:
            add_error(errors, f"{room}: decoded RGBA {value} exceeds 24MiB")
    return result


def build_contact_sheet(additions: list[dict[str, Any]]) -> None:
    cell, label_width = 96, 240
    canvas = Image.new("RGBA", (label_width + cell * 8, cell * len(additions)),
                       (32, 38, 58, 255))
    draw = ImageDraw.Draw(canvas)
    for row, entry in enumerate(additions):
        draw.text((8, row * cell + 8), str(entry["id"]), fill=(245, 245, 255, 255))
        with Image.open(ROOT / str(entry["sheet"])) as image_value:
            frames, _ = frame_cells(image_value.convert("RGBA"))
        for index, frame in enumerate(frames):
            checker = Image.new("RGBA", (cell, cell), (214, 222, 235, 255))
            checker_draw = ImageDraw.Draw(checker)
            for y in range(0, cell, 12):
                for x in range(0, cell, 12):
                    if (x // 12 + y // 12) % 2:
                        checker_draw.rectangle((x, y, x+11, y+11), fill=(174, 184, 204, 255))
            preview = frame.copy()
            preview.thumbnail((cell-4, cell-4), Image.Resampling.LANCZOS)
            checker.alpha_composite(preview, ((cell-preview.width)//2, (cell-preview.height)//2))
            canvas.alpha_composite(checker, (label_width + index * cell, row * cell))
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(CONTACT_SHEET, optimize=True)
    print(f"WROTE|{CONTACT_SHEET.relative_to(ROOT).as_posix()}")


def audit(write_contact_sheet: bool = False) -> int:
    errors: list[str] = []
    validate_specs()
    required = [MANIFEST, V1_MANIFEST, V2_MANIFEST, SOURCE_REPORT,
                NORMALIZATION_REPORT, PREPARER, NORMALIZER, BUILDER, SPECS_PATH,
                FIXTURE_RUNTIME, ROOM_RUNTIME, WATER_SHADER, RIPPLE_TEXTURE,
                CAUSTICS_TEXTURE, LICENSES, EXPORT_PRESETS, CI_SCRIPT]
    for path in required:
        if not path.is_file():
            add_error(errors, f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1

    manifest = load_json(MANIFEST, errors)
    v1 = load_json(V1_MANIFEST, errors)
    v2 = load_json(V2_MANIFEST, errors)
    source_report = load_json(SOURCE_REPORT, errors)
    normalization_report = load_json(NORMALIZATION_REPORT, errors)
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1

    if int(manifest.get("schema_version", 0)) != 3:
        add_error(errors, "manifest schema is not 3")
    if manifest.get("generator") != BUILDER.relative_to(ROOT).as_posix() \
            or manifest.get("generator_sha256") != repository_text_sha256(BUILDER):
        add_error(errors, "manifest builder path/hash is stale")
    if int(source_report.get("schema_version", 0)) != 3 \
            or int(source_report.get("asset_count", -1)) != 38:
        add_error(errors, "source preparation report is not schema-3/38")
    if source_report.get("tool_sha256") != repository_text_sha256(PREPARER):
        add_error(errors, "source preparation tool hash is stale")
    if int(source_report.get("exact_chroma_inset_pixels", -1)) != SOURCE_INSET \
            or float(source_report.get("global_key_distance", -1.0)) != GLOBAL_KEY_DISTANCE:
        add_error(errors, "source preparation key policy is stale")
    if int(normalization_report.get("schema_version", 0)) != 3 \
            or int(normalization_report.get("asset_count", -1)) != 38:
        add_error(errors, "normalization report is not schema-3/38")
    if normalization_report.get("tool_sha256") != repository_text_sha256(NORMALIZER):
        add_error(errors, "normalization tool hash is stale")
    if normalization_report.get("source_preparation_sha256") != repository_text_sha256(SOURCE_REPORT):
        add_error(errors, "normalization source-preparation hash is stale")
    if int(normalization_report.get("max_visible_near_chroma_pixels", -1)) != 0 \
            or float(normalization_report.get("max_visible_near_chroma_ratio", -1.0)) != 0.0:
        add_error(errors, "normalization report permits visible near-key magenta")
    if normalization_report.get("visible_near_chroma_policy") != "zero_pixels_across_all_304_frames":
        add_error(errors, "normalization near-key policy is not zero across 304 frames")

    source_manifest = manifest.get("source_manifests", {})
    path_hash_pairs = [
        ("v1_room_derived", "v1_room_derived_sha256", V1_MANIFEST),
        ("v2_active", "v2_active_sha256", V2_MANIFEST),
        ("v3_specs", "v3_specs_sha256", SPECS_PATH),
        ("v3_source_preparation", "v3_source_preparation_sha256", SOURCE_REPORT),
        ("v3_normalization", "v3_normalization_sha256", NORMALIZATION_REPORT),
        ("fixture_runtime", "fixture_runtime_sha256", FIXTURE_RUNTIME),
        ("room_runtime", "room_runtime_sha256", ROOM_RUNTIME),
    ]
    for path_key, hash_key, path in path_hash_pairs:
        if source_manifest.get(path_key) != path.relative_to(ROOT).as_posix() \
                or source_manifest.get(hash_key) != repository_text_sha256(path):
            add_error(errors, f"source manifest {path_key} path/hash is stale")

    v2_assets = v2.get("assets", [])
    if len(v2_assets) != 29 or sum(len(value.get("instances", [])) for value in v2_assets) != 34:
        add_error(errors, "active v2 baseline is not 29 assets / 34 instances")
    if any(str(value.get("room", "")) == "mermaid_pool" for value in v2_assets):
        add_error(errors, "active v2 reintroduces retired pool sheets")
    if "mermaid_pool" not in v2.get("retired_rooms", {}):
        add_error(errors, "active v2 does not record retired pool")
    legacy_expected = [value for value in v1.get("assets", [])
                       if str(value.get("room", "")) == "mermaid_pool"]
    legacy = manifest.get("legacy_room_derived_assets", [])
    if len(legacy_expected) != 4 or len(legacy) != 4:
        add_error(errors, "legacy room-derived pool roster is not four")
        legacy = legacy if isinstance(legacy, list) else []
    elif [without_pack(value) for value in legacy] != legacy_expected \
            or any(value.get("pack") != "legacy_room_derived_base" for value in legacy):
        add_error(errors, "legacy pool evidence is not an immutable V1 deep copy")

    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        add_error(errors, "manifest assets is not a list")
        assets = []
    base = [value for value in assets if value.get("pack") == "v2_base"]
    additions = [value for value in assets if value.get("pack") == "v3_addition"]
    unknown = [value.get("id") for value in assets
               if value.get("pack") not in {"v2_base", "v3_addition"}]
    if unknown:
        add_error(errors, f"manifest has unknown packs: {unknown}")
    expected_base = [
        value for value in v2_assets
        if str(value.get("id", "")) not in RETIRED_V2_ASSET_IDS
    ]
    if len(base) != 28 \
            or [without_pack(value) for value in base] != expected_base:
        add_error(errors, "active v2_base entries differ from the audited retirement map")
    if len(additions) != 38:
        add_error(errors, f"v3 addition roster has {len(additions)} assets")
    if len(assets) != 66 or sum(len(value.get("instances", [])) for value in assets) != 71:
        add_error(errors, "active manifest is not 66 assets / 71 instances")
    ids = [str(value.get("id", "")) for value in assets]
    if len(ids) != len(set(ids)):
        add_error(errors, "active manifest has duplicate asset ids")

    source_index = index_assets(source_report.get("assets", []), "source assets", errors)
    normalized_index = index_assets(normalization_report.get("assets", []),
                                    "normalization assets", errors)
    addition_index = index_assets(additions, "manifest additions", errors)
    expected_ids = {str(value["id"]) for value in ADDITIONS}
    if set(source_index) != expected_ids or set(normalized_index) != expected_ids \
            or set(addition_index) != expected_ids:
        add_error(errors, "v3 source/normalization/manifest IDs differ from specs")
    runtime_names = {path.name for path in NORMALIZATION_REPORT.parent.glob("*_sheet.png")}
    expected_names = {f"{value['id']}_sheet.png" for value in ADDITIONS}
    if runtime_names != expected_names:
        add_error(errors, "runtime-sheet roster differs from 38 specs")
    for spec in ADDITIONS:
        asset_id = str(spec["id"])
        if asset_id in addition_index and asset_id in source_index and asset_id in normalized_index:
            audit_addition(spec, addition_index[asset_id], source_index[asset_id],
                           normalized_index[asset_id], errors)

    physics_additions = {str(value["id"]) for value in additions
                         if str(value.get("physics_mode", "none")) != "none"}
    if physics_additions != NEW_JOLT_IDS:
        add_error(errors, f"new Jolt roster differs: {sorted(physics_additions)}")
    if len([value for value in additions if value.get("water_layers")]) != 5:
        add_error(errors, "v3 does not add exactly five water fixtures")
    audit_runtime_contract(manifest, assets, errors)

    rooms = manifest.get("rooms", {})
    measured_active = {room: int(rooms.get(room, {}).get("physical_item_count", -1))
                       for room in EXPECTED_ACTIVE_ROOMS}
    if measured_active != EXPECTED_ACTIVE_ROOMS:
        add_error(errors, f"active room counts differ: {measured_active}")
    overall: dict[str, set[str]] = {room: set() for room in EXPECTED_OVERALL_ROOMS}
    for value in [*assets, *legacy]:
        room = str(value.get("room", ""))
        if room not in overall:
            continue
        for instance in value.get("instances", []):
            instance_id = str(instance)
            if instance_id in overall[room]:
                add_error(errors, f"{room}: duplicate runtime item {instance_id}")
            overall[room].add(instance_id)
    measured_overall = {room: len(values) for room, values in overall.items()}
    if measured_overall != EXPECTED_OVERALL_ROOMS:
        add_error(errors, f"overall room counts differ: {measured_overall}")

    room_bytes = decoded_rgba_by_room(assets, legacy, errors)
    summary = manifest.get("summary", {})
    expected_summary = {
        "asset_count": 66, "physical_instance_count": 71,
        "generated_sheet_count": 66, "v2_base_asset_count": 28,
        "v3_addition_asset_count": 38, "legacy_room_derived_asset_count": 4,
        "legacy_room_derived_instance_count": 4, "overall_asset_count": 70,
        "overall_physical_instance_count": 75, "water_interaction_count": 10,
        "overall_water_interaction_count": 14, "jolt_component_count": 8,
        "decoded_rgba_bytes_by_room": room_bytes,
        "max_room_decoded_rgba_bytes": max(room_bytes.values(), default=0),
        "room_decoded_rgba_budget_bytes": ROOM_BUDGET_BYTES, "missing_count": 0,
    }
    for key, value in expected_summary.items():
        if summary.get(key) != value:
            add_error(errors, f"summary {key} differs: {summary.get(key)!r} != {value!r}")
    review = manifest.get("visual_review_evidence", {})
    if int(review.get("codex_reviewed_v3_assets", -1)) != 38 \
            or str(review.get("human_review_status", "")).lower() != "pending":
        add_error(errors, "top-level visual review evidence is stale")
    frame_contract = manifest.get("frame_contract", {})
    if frame_contract.get("minimum") != 4 or frame_contract.get("maximum") != 12 \
            or frame_contract.get("delivered_authored_states") != 8:
        add_error(errors, "top-level frame contract differs")
    audit_declarations(additions, source_index, errors)

    if write_contact_sheet and not errors:
        build_contact_sheet(additions)
    if errors:
        for error in errors:
            print("FAIL: " + error)
        print(f"CASTLEV3|AUDIT_FAIL|errors={len(errors)}")
        return 1
    print("CASTLEV3|AUDIT_OK|active=66/71|overall=70/75|water=10+4|jolt=8|near_key=0")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-contact-sheet", action="store_true",
                        help="write ignored checkerboard evidence after a clean audit")
    args = parser.parse_args()
    return audit(args.write_contact_sheet)


if __name__ == "__main__":
    raise SystemExit(main())
