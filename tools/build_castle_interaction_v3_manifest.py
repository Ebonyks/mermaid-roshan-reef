#!/usr/bin/env python3
"""Build the integration-safe Pearl Castle interaction-v3 manifest.

The active manifest contains 29 generated-v2 bases and 38 additive generated
full-object sheets. The four approved room-derived Mermaid Pool bases remain
runtime evidence outside ``assets`` so retired generated-v2 pool cutouts cannot
silently return. This tool registers existing pixels only; it never edits art.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image

from castle_interaction_v3_specs import ADDITIONS, validate_specs


ROOT = Path(__file__).resolve().parents[1]
V1_MANIFEST = ROOT / "assets/flats/castle/interactions/castle_interactions.json"
V2_MANIFEST = ROOT / "assets/flats/castle/interactions_v2/castle_interactions_v2.json"
SOURCE_REPORT = ROOT / "assets_src/imagegen/castle_object_animations_v3/castle_interactions_v3_source_preparation.json"
NORMALIZATION_REPORT = ROOT / "assets/flats/castle/interactions_v3/castle_interactions_v3_normalization.json"
OUTPUT = ROOT / "assets/flats/castle/interactions_v3/castle_interactions_v3.json"
SPECS_PATH = ROOT / "tools/castle_interaction_v3_specs.py"
FIXTURE_RUNTIME = ROOT / "scripts/arena/castle_fixture_rigs.gd"
ROOM_RUNTIME = ROOT / "scripts/arena/castle_rooms_25d.gd"
WATER_SHADER = ROOT / "assets/shaders/castle_fixture_water.gdshader"
RIPPLE_TEXTURE = ROOT / "assets/terrain/up_water_nrm.jpg"
CAUSTICS_TEXTURE = ROOT / "assets/terrain/caustics.png"

ACTIVE_V2_ASSETS = 29
ACTIVE_V2_INSTANCES = 34
V3_ADDITIONS = 38
LEGACY_POOL_ASSETS = 4
MANIFEST_ASSETS = 67
MANIFEST_INSTANCES = 72
OVERALL_ASSETS = 71
OVERALL_INSTANCES = 76
MANIFEST_JOLT = 8
MANIFEST_WATER = 10
OVERALL_WATER = 14
ROOM_BUDGET_BYTES = 24 * 1024 * 1024
POOL_ROOM = "mermaid_pool"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_text_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"required input is missing: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} is not a JSON object")
    return value


def index_assets(report: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for value in report.get("assets", []):
        if not isinstance(value, dict) or not str(value.get("id", "")):
            raise ValueError(f"{label} contains an invalid asset record")
        asset_id = str(value["id"])
        if asset_id in result:
            raise ValueError(f"{label} contains duplicate id {asset_id}")
        result[asset_id] = value
    return result


def frame_cells(sheet: Image.Image) -> tuple[list[Image.Image], int]:
    if sheet.width % 4 or sheet.height % 2:
        raise ValueError("runtime sheet is not an exact 4x2 grid")
    cell = sheet.width // 4
    if sheet.height // 2 != cell:
        raise ValueError("runtime sheet cells are not square")
    frames = []
    for index in range(8):
        column = index % 4
        row = index // 4
        frames.append(sheet.crop((
            column * cell, row * cell,
            (column + 1) * cell, (row + 1) * cell,
        )))
    return frames, cell


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int]:
    bbox = frame.getchannel("A").point(
        lambda value: 255 if value >= 16 else 0
    ).getbbox()
    if bbox is None:
        raise ValueError("runtime state has no visible alpha silhouette")
    return bbox


def frame_sha256(frame: Image.Image) -> str:
    return hashlib.sha256(frame.convert("RGBA").tobytes()).hexdigest()


def review_is_accepted(status: str) -> bool:
    value = status.strip().lower()
    return value.startswith("accepted") or value.startswith("pass")


def integration_rosters(
    v1: dict[str, Any], v2: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active = copy.deepcopy(v2.get("assets", []))
    if len(active) != ACTIVE_V2_ASSETS:
        raise ValueError(
            "v3 requires the current 29-asset v2 baseline; merge origin/dev "
            f"before building (found {len(active)})"
        )
    if sum(len(value.get("instances", [])) for value in active) != ACTIVE_V2_INSTANCES:
        raise ValueError("active v2 physical-instance count is not 34")
    if any(str(value.get("room", "")) == POOL_ROOM for value in active):
        raise ValueError("retired generated-v2 Mermaid Pool art was reintroduced")
    retired = v2.get("retired_rooms", {})
    if not isinstance(retired, dict) or POOL_ROOM not in retired:
        raise ValueError("v2 does not record the retired Mermaid Pool")
    legacy = [
        copy.deepcopy(value) for value in v1.get("assets", [])
        if str(value.get("room", "")) == POOL_ROOM
    ]
    if len(legacy) != LEGACY_POOL_ASSETS:
        raise ValueError("approved room-derived Mermaid Pool roster is not four")
    if sum(len(value.get("instances", [])) for value in legacy) != 4:
        raise ValueError("approved room-derived Mermaid Pool instance count is not four")
    return active, legacy


def report_indexes(
    source: dict[str, Any], normalized: dict[str, Any]
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if int(source.get("schema_version", 0)) != 3:
        raise ValueError("source preparation schema is not 3")
    if int(normalized.get("schema_version", 0)) != 3:
        raise ValueError("normalization schema is not 3")
    source_tool = ROOT / str(source.get("tool", ""))
    normalizer_tool = ROOT / str(normalized.get("tool", ""))
    if not source_tool.is_file() or source.get("tool_sha256") != repository_text_sha256(source_tool):
        raise ValueError("source preparation tool hash is stale")
    if not normalizer_tool.is_file() or normalized.get("tool_sha256") != repository_text_sha256(normalizer_tool):
        raise ValueError("normalization tool hash is stale")
    if normalized.get("source_preparation_sha256") != repository_text_sha256(SOURCE_REPORT):
        raise ValueError("normalization references stale source preparation")
    source_index = index_assets(source, "source preparation")
    normalized_index = index_assets(normalized, "normalization")
    expected = {str(value["id"]) for value in ADDITIONS}
    if set(source_index) != expected or set(normalized_index) != expected:
        raise ValueError("v3 preparation/normalization roster differs from specs")
    return source_index, normalized_index


def anchor_pixel(cell: int, padding: float, mode: str) -> tuple[float, float]:
    if mode == "top_center":
        return (cell * 0.5, padding)
    if mode == "bottom_center":
        return (cell * 0.5, cell - padding)
    return (cell * 0.5, cell * 0.5)


def target_anchor(size: list[float], mode: str, hall: bool) -> tuple[float, float]:
    width, height = float(size[0]), float(size[1])
    if hall:
        if mode == "top_center":
            return (0.0, -height * 0.5)
        if mode == "bottom_center":
            return (0.0, height * 0.5)
        return (0.0, 0.0)
    if mode == "top_center":
        return (width * 0.5, 0.0)
    if mode == "bottom_center":
        return (width * 0.5, height)
    return (width * 0.5, height * 0.5)


def runtime_mapping(
    spec: dict[str, Any], normalized: dict[str, Any], cell: int
) -> dict[str, Any]:
    """Fit every authored alpha bound into the placement box about one anchor."""
    boxes = [tuple(float(component) for component in value)
             for value in normalized.get("frame_bboxes", [])]
    if len(boxes) != 8:
        raise ValueError(f"{spec['id']}: normalization has no eight frame bounds")
    mode = str(spec["anchor_mode"])
    padding = float(normalized.get("padding_pixels", 6))
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
            raise ValueError(f"{spec['id']}: {mode} anchor crosses placement {key} edge")
        scales.append(available[key] / extent)
    scale = min(scales)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError(f"{spec['id']}: derived runtime scale is invalid")
    hall = str(spec["room"]) == "main_hall"
    desired = target_anchor(spec["placement_size"], mode, hall)
    relative_anchor = (
        (anchor[0] - cell * 0.5) * scale,
        (anchor[1] - cell * 0.5) * scale,
    )
    offset = [
        round(desired[0] - relative_anchor[0], 6),
        round(desired[1] - relative_anchor[1], 6),
    ]
    mapped_bounds = []
    for box in boxes:
        mapped = [
            offset[0] + (box[0] - cell * 0.5) * scale,
            offset[1] + (box[1] - cell * 0.5) * scale,
            offset[0] + (box[2] - cell * 0.5) * scale,
            offset[1] + (box[3] - cell * 0.5) * scale,
        ]
        mapped_bounds.append([round(value, 6) for value in mapped])
    tolerance = 0.05
    if hall:
        limits = (-width * 0.5, -height * 0.5, width * 0.5, height * 0.5)
    else:
        limits = (0.0, 0.0, width, height)
    for index, box in enumerate(mapped_bounds):
        if (box[0] < limits[0] - tolerance or box[1] < limits[1] - tolerance
                or box[2] > limits[2] + tolerance or box[3] > limits[3] + tolerance):
            raise ValueError(f"{spec['id']}: mapped frame {index} exceeds placement")
    return {
        "runtime_scale": round(scale, 9),
        "runtime_center_offset": offset if not hall else copy.deepcopy(spec["runtime_center_offset"]),
        "hall_center_offset": offset if hall else copy.deepcopy(spec["hall_center_offset"]),
        "source_anchor_pixel": [round(anchor[0], 6), round(anchor[1], 6)],
        "target_anchor": [round(desired[0], 6), round(desired[1], 6)],
        "union_anchor_extents": {key: round(value, 6) for key, value in extents.items()},
        "mapped_frame_bounds": mapped_bounds,
        "placement_limits": [round(value, 6) for value in limits],
        "fit_method": "uniform_scale_all_frame_alpha_extents_about_fixed_anchor",
    }


def build_addition(
    spec: dict[str, Any], prepared: dict[str, Any], normalized: dict[str, Any]
) -> dict[str, Any]:
    asset_id = str(spec["id"])
    source_path = ROOT / str(prepared.get("path", ""))
    sheet_path = ROOT / str(normalized.get("runtime_path", ""))
    if not source_path.is_file() or sha256(source_path) != prepared.get("prepared_sha256"):
        raise ValueError(f"{asset_id}: prepared source is missing or stale")
    if not sheet_path.is_file() or sha256(sheet_path) != normalized.get("runtime_sha256"):
        raise ValueError(f"{asset_id}: normalized sheet is missing or stale")
    provenance = copy.deepcopy(prepared.get("provenance", {}))
    if not isinstance(provenance, dict):
        raise ValueError(f"{asset_id}: source provenance is invalid")
    provenance_path = ROOT / str(provenance.get("batch_manifest", ""))
    if not provenance_path.is_file() or provenance.get("batch_manifest_sha256") != repository_text_sha256(provenance_path):
        raise ValueError(f"{asset_id}: provenance manifest hash is stale")
    if not review_is_accepted(str(provenance.get("codex_visual_review_status", ""))):
        raise ValueError(f"{asset_id}: Codex visual review is not accepted")
    if not provenance.get("accepted_prompt_sha256") or not provenance.get("accepted_native_sha256"):
        raise ValueError(f"{asset_id}: generation prompt/native hash is missing")
    with Image.open(sheet_path) as image_value:
        sheet = image_value.convert("RGBA")
    frames, cell = frame_cells(sheet)
    if cell != int(spec["runtime_cell_size"]) or max(sheet.size) > 1024:
        raise ValueError(f"{asset_id}: runtime dimensions violate spec/mobile cap")
    boxes = [alpha_bbox(frame) for frame in frames]
    hashes = [frame_sha256(frame) for frame in frames]
    if hashes != normalized.get("frame_sha256") or [list(value) for value in boxes] != normalized.get("frame_bboxes"):
        raise ValueError(f"{asset_id}: normalization frame evidence is stale")
    if len(set(hashes)) != 8:
        raise ValueError(f"{asset_id}: authored states are not all distinct")
    mapping = runtime_mapping(spec, normalized, cell)
    alpha = sheet.getchannel("A")
    histogram = alpha.histogram()
    border = (list(alpha.crop((0, 0, sheet.width, 1)).getdata())
              + list(alpha.crop((0, sheet.height - 1, sheet.width, sheet.height)).getdata())
              + list(alpha.crop((0, 0, 1, sheet.height)).getdata())
              + list(alpha.crop((sheet.width - 1, 0, sheet.width, sheet.height)).getdata()))
    physics = str(spec["physics_mode"])
    timeline = copy.deepcopy(spec["timeline_sequence"])
    return {
        "pack": "v3_addition",
        "id": asset_id,
        "room": spec["room"],
        "item_id": spec["item"],
        "instances": [spec["item"]],
        "name": spec["name"],
        "placement_position": copy.deepcopy(spec["position"]),
        "placement_position_mode": spec["position_mode"],
        "placement_size": copy.deepcopy(spec["placement_size"]),
        "hotspot_size": copy.deepcopy(spec["hotspot_size"]),
        "hotspot_offset": copy.deepcopy(spec["hotspot_offset"]),
        "z": spec["z"],
        "color": copy.deepcopy(spec["color"]),
        "semantic_action": spec["semantic_action"],
        "render_mode": spec["render_mode"],
        "frame_count": 8,
        "hframes": 4,
        "vframes": 2,
        "sound": spec["sound"],
        "close_sound": "",
        "sound_frame": spec["sound_frame"],
        "pitch": spec["pitch"],
        "close_pitch": 1.0,
        "frame_duration_seconds": spec["frame_duration_seconds"],
        "fixed_pivot": True,
        "root_transform_animation": physics != "none",
        "secondary_root_physics": physics != "none",
        "normalized_use_review": "codex_visual_review_accepted_2026-08-02",
        "human_visual_review": str(provenance.get("human_review_status", "pending")),
        "sheet": sheet_path.relative_to(ROOT).as_posix(),
        "sheet_sha256": sha256(sheet_path),
        "raw_chroma_master": source_path.relative_to(ROOT).as_posix(),
        "raw_chroma_master_sha256": sha256(source_path),
        "accepted_native_sha256": provenance["accepted_native_sha256"],
        "grid": copy.deepcopy(spec["grid"]),
        "authored_frame_count": 8,
        "timeline_sequence": timeline,
        "timeline_frame_count": len(timeline),
        "cell_size": [cell, cell],
        "sheet_dimensions": list(sheet.size),
        "frame_bboxes": [list(value) for value in boxes],
        "frame_sha256": hashes,
        "unique_frame_count": 8,
        "placement_bbox": list(boxes[int(spec["rest_frame"])]),
        "placement_geometry_role": "v3_spec_box_fitted_from_all_normalized_alpha_extents",
        "alignment_frame": int(spec["rest_frame"]),
        "anchor_mode": spec["anchor_mode"],
        "runtime_scale": mapping["runtime_scale"],
        "runtime_center_offset": mapping["runtime_center_offset"],
        "hall_center_offset": mapping["hall_center_offset"],
        "runtime_mapping": mapping,
        "rest_frame": spec["rest_frame"],
        "transparent_pixels": histogram[0],
        "partial_alpha_pixels": sum(histogram[1:255]),
        "opaque_pixels": histogram[255],
        "total_pixels": sheet.width * sheet.height,
        "transparent_border": all(value == 0 for value in border),
        "normalization": {
            "report": NORMALIZATION_REPORT.relative_to(ROOT).as_posix(),
            "report_sha256": repository_text_sha256(NORMALIZATION_REPORT),
            "source_preparation_report": SOURCE_REPORT.relative_to(ROOT).as_posix(),
            "source_preparation_report_sha256": repository_text_sha256(SOURCE_REPORT),
            "source_sha256": normalized.get("source_sha256"),
            "runtime_sha256": normalized.get("runtime_sha256"),
            "uniform_scale": normalized.get("uniform_scale"),
            "padding_pixels": normalized.get("padding_pixels"),
            "edge_gap_pixels": normalized.get("edge_gap_pixels"),
            "anchor_spread_pixels": copy.deepcopy(normalized.get("anchor_spread_pixels", [])),
            "per_frame_alpha_qa": copy.deepcopy(normalized.get("per_frame_alpha_qa", [])),
            "changed_fraction_from_rest": copy.deepcopy(normalized.get("changed_fraction_from_rest", [])),
            "fixed_anchor_translation_only": bool(normalized.get("fixed_anchor_translation_only", False)),
            "one_uniform_scale_across_all_frames": bool(normalized.get("one_uniform_scale_across_all_frames", False)),
            "per_frame_scale_used": bool(normalized.get("per_frame_scale_used", True)),
            "subject_geometry_warped": bool(normalized.get("subject_geometry_warped", True)),
            "state_pixels_synthesized": bool(normalized.get("state_pixels_synthesized", True)),
            "whole_object_translation_only": True,
            "repainted_pixels": False,
        },
        "source_preparation": {
            "report": SOURCE_REPORT.relative_to(ROOT).as_posix(),
            "report_sha256": repository_text_sha256(SOURCE_REPORT),
            "native_copy_sha256": prepared.get("native_copy_sha256"),
            "prepared_sha256": prepared.get("prepared_sha256"),
            "native_dimensions": copy.deepcopy(provenance.get("accepted_native_dimensions", [])),
            "prepared_dimensions": copy.deepcopy(prepared.get("prepared_dimensions", [])),
            "exact_chroma_inset_pixels": prepared.get("exact_chroma_inset_pixels"),
            "whole_cell_uniform_scale_only": bool(prepared.get("whole_cell_uniform_scale_only", False)),
            "connected_outer_field_plus_global_near_key": bool(
                prepared.get("connected_outer_field_plus_global_near_key", False)
            ),
            "key_field_pixels_normalized": prepared.get("key_field_pixels_normalized"),
            "global_near_key_pixels_normalized": prepared.get(
                "global_near_key_pixels_normalized"
            ),
            "global_key_distance": prepared.get("global_key_distance"),
            "edge_despill_pixels": prepared.get("edge_despill_pixels"),
            "subject_geometry_warped": bool(prepared.get("subject_geometry_warped", True)),
            "state_pixels_synthesized": bool(prepared.get("state_pixels_synthesized", True)),
        },
        "provenance": provenance,
        "provenance_manifest": provenance_path.relative_to(ROOT).as_posix(),
        "provenance_manifest_sha256": repository_text_sha256(provenance_path),
        "physics_mode": physics,
        "physics_pivot": copy.deepcopy(spec["physics_pivot"]),
        "physics_max_angle_radians": spec["physics_max_angle_radians"],
        "physics_impulse_scale": spec["physics_impulse_scale"],
        "water_layers": copy.deepcopy(spec["water_layers"]),
        "primary_animation_is_overlay": False,
        "generated_hidden_surfaces": any(token in str(spec["semantic_action"])
                                         for token in ("open", "reveal", "lift_lid", "unlatch")),
    }


def active_rooms(v2: dict[str, Any], additions: list[dict[str, Any]]) -> dict[str, Any]:
    rooms = copy.deepcopy(v2.get("rooms", {}))
    by_room: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in additions:
        by_room[str(entry["room"])].append({
            "id": entry["item_id"],
            "asset_id": entry["id"],
            "semantic_action": entry["semantic_action"],
            "pack": "v3_addition",
        })
    for room_id, values in by_room.items():
        room = rooms.setdefault(room_id, {"physical_item_count": 0, "instances": []})
        instances = room.setdefault("instances", [])
        instances.extend(copy.deepcopy(values))
        room["physical_item_count"] = len(instances)
    expected = {
        "main_hall": 14, "opera_hall": 8, "kitchen": 14,
        "library": 8, "playroom": 8, "craft_room": 8,
        "mermaid_pool": 4, "bubble_bath": 8,
    }
    measured = {room: int(rooms.get(room, {}).get("physical_item_count", -1))
                for room in expected}
    if measured != expected:
        raise ValueError(f"active room inventory {measured} != {expected}")
    return dict(sorted(rooms.items()))


def decoded_rgba_by_room(
    assets: list[dict[str, Any]], legacy: list[dict[str, Any]]
) -> dict[str, int]:
    totals: Counter[str] = Counter()
    seen: set[str] = set()
    for entry in [*assets, *legacy]:
        path_value = entry.get("sheet", entry.get("atlas", ""))
        path = ROOT / str(path_value)
        key = (str(entry["room"]), path.resolve().as_posix())
        if key in seen:
            continue
        seen.add(key)
        if not path.is_file():
            raise ValueError(f"runtime visual is missing: {path_value}")
        with Image.open(path) as image_value:
            width, height = image_value.size
        totals[str(entry["room"])] += width * height * 4
    result = dict(sorted(totals.items()))
    over = {room: value for room, value in result.items() if value > ROOM_BUDGET_BYTES}
    if over:
        raise ValueError(f"per-room decoded RGBA budget exceeded: {over}")
    return result


def main() -> None:
    validate_specs()
    v1 = load_json(V1_MANIFEST)
    v2 = load_json(V2_MANIFEST)
    active_v2, legacy_pool = integration_rosters(v1, v2)
    source_report = load_json(SOURCE_REPORT)
    normalization_report = load_json(NORMALIZATION_REPORT)
    source_index, normalized_index = report_indexes(source_report, normalization_report)

    base_assets = []
    for original in active_v2:
        value = copy.deepcopy(original)
        value["pack"] = "v2_base"
        base_assets.append(value)
    additions = [
        build_addition(spec, source_index[str(spec["id"])], normalized_index[str(spec["id"])])
        for spec in ADDITIONS
    ]
    legacy_evidence = []
    for original in legacy_pool:
        value = copy.deepcopy(original)
        value["pack"] = "legacy_room_derived_base"
        legacy_evidence.append(value)
    assets = [*base_assets, *additions]
    manifest_instances = sum(len(value.get("instances", [])) for value in assets)
    if len(assets) != MANIFEST_ASSETS or manifest_instances != MANIFEST_INSTANCES:
        raise ValueError("active combined manifest is not 67 assets / 72 instances")
    manifest_jolt = sum(str(value.get("physics_mode", "none")) != "none" for value in assets)
    manifest_water = sum(bool(value.get("water_layers", [])) for value in assets)
    if manifest_jolt != MANIFEST_JOLT or manifest_water != MANIFEST_WATER:
        raise ValueError(f"active mechanics count is Jolt={manifest_jolt}, water={manifest_water}")
    room_bytes = decoded_rgba_by_room(assets, legacy_evidence)
    rooms = active_rooms(v2, additions)

    contract = copy.deepcopy(v2.get("contract", {}))
    contract.update({
        "timeline_frames_min": 4,
        "timeline_frames_max": 12,
        "authored_state_count": 8,
        "primary_animation_is_overlay": False,
        "water_renderer": WATER_SHADER.relative_to(ROOT).as_posix(),
        "water_renderer_sha256": sha256(WATER_SHADER),
        "water_ripple_texture": RIPPLE_TEXTURE.relative_to(ROOT).as_posix(),
        "water_ripple_texture_sha256": sha256(RIPPLE_TEXTURE),
        "water_caustics_texture": CAUSTICS_TEXTURE.relative_to(ROOT).as_posix(),
        "water_caustics_texture_sha256": sha256(CAUSTICS_TEXTURE),
        "water_node_type": "Sprite3D",
        "water_material_type": "ShaderMaterial",
        "water_depth_write": False,
        "water_geometry_source": "per_asset_manifest_layers",
        "water_mask_source": "runtime_cached_exact_polygon_image_texture",
        "water_dynamic_geometry_source": "authored_atlas_frame_index",
        "jolt_body_cap": 12,
        "jolt_awake_cap": 8,
        "jolt_logic_authority": False,
        "room_decoded_rgba_budget_bytes": ROOM_BUDGET_BYTES,
        "legacy_pool_runtime_source": "approved_room_derived_v1_atlases",
        "retired_v2_pool_reintroduced": False,
    })
    timelines = [int(value["timeline_frame_count"]) for value in assets]
    summary = {
        "asset_count": len(assets),
        "physical_instance_count": manifest_instances,
        "generated_sheet_count": len(assets),
        "v2_base_asset_count": len(base_assets),
        "v3_addition_asset_count": len(additions),
        "legacy_room_derived_asset_count": len(legacy_evidence),
        "legacy_room_derived_instance_count": 4,
        "overall_asset_count": len(assets) + len(legacy_evidence),
        "overall_physical_instance_count": manifest_instances + 4,
        "water_interaction_count": manifest_water,
        "overall_water_interaction_count": manifest_water + 4,
        "jolt_component_count": manifest_jolt,
        "decoded_rgba_bytes_by_room": room_bytes,
        "max_room_decoded_rgba_bytes": max(room_bytes.values()),
        "room_decoded_rgba_budget_bytes": ROOM_BUDGET_BYTES,
        "missing_count": 0,
    }
    if (summary["overall_asset_count"] != OVERALL_ASSETS
            or summary["overall_physical_instance_count"] != OVERALL_INSTANCES
            or summary["overall_water_interaction_count"] != OVERALL_WATER):
        raise ValueError("overall castle totals are not 71 assets / 76 instances / 14 water")
    payload = {
        "schema_version": 3,
        "generated_on": "2026-08-02",
        "generator": "tools/build_castle_interaction_v3_manifest.py",
        "generator_sha256": repository_text_sha256(Path(__file__)),
        "source_manifests": {
            "v1_room_derived": V1_MANIFEST.relative_to(ROOT).as_posix(),
            "v1_room_derived_sha256": repository_text_sha256(V1_MANIFEST),
            "v2_active": V2_MANIFEST.relative_to(ROOT).as_posix(),
            "v2_active_sha256": repository_text_sha256(V2_MANIFEST),
            "v3_specs": SPECS_PATH.relative_to(ROOT).as_posix(),
            "v3_specs_sha256": repository_text_sha256(SPECS_PATH),
            "v3_source_preparation": SOURCE_REPORT.relative_to(ROOT).as_posix(),
            "v3_source_preparation_sha256": repository_text_sha256(SOURCE_REPORT),
            "v3_normalization": NORMALIZATION_REPORT.relative_to(ROOT).as_posix(),
            "v3_normalization_sha256": repository_text_sha256(NORMALIZATION_REPORT),
            "fixture_runtime": FIXTURE_RUNTIME.relative_to(ROOT).as_posix(),
            "fixture_runtime_sha256": repository_text_sha256(FIXTURE_RUNTIME),
            "room_runtime": ROOM_RUNTIME.relative_to(ROOT).as_posix(),
            "room_runtime_sha256": repository_text_sha256(ROOM_RUNTIME),
        },
        "visual_review_evidence": {
            "codex_reviewed_v3_assets": V3_ADDITIONS,
            "codex_review_status": "accepted_or_pass_pending_owner_review",
            "human_review_status": "pending",
            "reviewed_frame_indices": list(range(8)),
            "evidence_source": "per_asset_provenance_plus_normalization_alpha_qa",
        },
        "contract": contract,
        "frame_contract": {
            "minimum": 4,
            "maximum": 12,
            "delivered_authored_states": 8,
            "delivered_timeline_min": min(timelines),
            "delivered_timeline_max": max(timelines),
        },
        "rooms": rooms,
        "retired_rooms": copy.deepcopy(v2.get("retired_rooms", {})),
        "legacy_room_derived_assets": legacy_evidence,
        "assets": assets,
        "missing_generated_assets": [],
        "summary": summary,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes((json.dumps(payload, indent=2) + "\n").encode("utf-8"))
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
