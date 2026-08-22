#!/usr/bin/env python3
"""Build the audited runtime contract for Pearl Castle object animations.

Generated full-object states are registered by the normalization tool, while
the approved v1 cell remains placement authority. This builder hashes all
delivery/source material and emits object-local water outlets/cavities plus
strictly cosmetic Jolt metadata. It never paints or synthesizes a frame.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
V1_MANIFEST = ROOT / "assets/flats/castle/interactions/castle_interactions.json"
SHEET_DIR = ROOT / "assets/flats/castle/interactions_v2"
RAW_ROOT = ROOT / "assets_src/imagegen/castle_object_animations_v2"
NORMALIZATION_REPORT = SHEET_DIR / "castle_interactions_v2_normalization.json"
OUTPUT = SHEET_DIR / "castle_interactions_v2.json"
CONTACT_SHEET = (
    ROOT
    / "audit/castle_interactions_v2"
    / "castle_interaction_frames_v2.png"
)
WATER_SHADER = ROOT / "assets/shaders/castle_fixture_water.gdshader"
RIPPLE_TEXTURE = ROOT / "assets/terrain/up_water_nrm.jpg"
CAUSTICS_TEXTURE = ROOT / "assets/terrain/caustics.png"

RETIRED_V2_ROOMS = {"mermaid_pool"}
ALIGNMENT_FRAME = {
    "main_hall_tapestry": 7,
}

ANCHOR_MODE = {
    "main_hall_tapestry": "top_center",
    "main_hall_sconce": "center",
    "opera_hall_curtains": "top_center",
    "opera_hall_chandelier": "top_center",
    "opera_hall_stage_star": "center",
    "craft_room_idea_board": "center",
    "craft_room_palette": "center",
    "craft_room_ribbon_rack": "center",
    "kitchen_oven": "top_center",
    "kitchen_pan_1": "top_center",
    "kitchen_pan_2": "top_center",
    "kitchen_pan_3": "top_center",
    "kitchen_pan_4": "top_center",
}

PHYSICS_MODE = {
    "opera_hall_chandelier": "hinge_z",
    "kitchen_pan_1": "hinge_z",
    "kitchen_pan_2": "hinge_z",
    "kitchen_pan_3": "hinge_z",
    "kitchen_pan_4": "hinge_z",
    "mermaid_pool_flower_float": "buoyant",
    "mermaid_pool_star_float": "buoyant",
    "bubble_bath_rubber_duck": "buoyant",
}

PHYSICS_PIVOT = {
    "opera_hall_chandelier": [0.5, 0.02],
    "kitchen_pan_1": [0.5, 0.04],
    "kitchen_pan_2": [0.5, 0.04],
    "kitchen_pan_3": [0.5, 0.04],
    "kitchen_pan_4": [0.5, 0.04],
    "mermaid_pool_flower_float": [0.5, 0.5],
    "mermaid_pool_star_float": [0.5, 0.5],
    "bubble_bath_rubber_duck": [0.5, 0.5],
}

RETURN_9 = [0, 1, 2, 3, 4, 3, 2, 1, 0]
CYCLE_12 = [0, 1, 2, 3, 4, 5, 6, 7, 5, 3, 1, 0]
STATEFUL_8 = list(range(8))
TIMELINE_SEQUENCE = {
    "main_hall_tapestry": [7, 6, 4, 2, 0, 1, 2, 3, 4, 5, 6, 7],
    "main_hall_sconce": STATEFUL_8,
    "opera_hall_chandelier": CYCLE_12,
    "opera_hall_footlights": CYCLE_12,
    "opera_hall_stage_star": CYCLE_12,
    "kitchen_pan_1": CYCLE_12,
    "kitchen_pan_2": CYCLE_12,
    "kitchen_pan_3": CYCLE_12,
    "kitchen_pan_4": CYCLE_12,
    "library_book_stack": CYCLE_12,
    "library_magic_book": CYCLE_12,
    "library_pearl_table": CYCLE_12,
    "library_pearl_lamp": CYCLE_12,
    "playroom_stuffie_nook": CYCLE_12,
    "playroom_stacking_toy": CYCLE_12,
    "playroom_blocks": CYCLE_12,
    "craft_room_idea_board": CYCLE_12,
    "craft_room_paint_table": CYCLE_12,
    "craft_room_palette": CYCLE_12,
    "mermaid_pool_star_float": CYCLE_12,
    "mermaid_pool_flower_float": CYCLE_12,
    "bubble_bath_rubber_duck": CYCLE_12,
}

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.convert("RGBA").getchannel("A")
    thresholded = alpha.point(lambda value: 255 if value >= 16 else 0)
    bbox = thresholded.getbbox()
    if bbox is None:
        raise ValueError("animation frame has no visible alpha silhouette")
    return bbox


def repository_text_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def anchor(bbox: tuple[int, int, int, int], mode: str) -> tuple[float, float]:
    left, top, right, bottom = bbox
    if mode == "top_center":
        return ((left + right) * 0.5, float(top))
    if mode == "bottom_center":
        return ((left + right) * 0.5, float(bottom))
    return ((left + right) * 0.5, (top + bottom) * 0.5)


def frame_hash(frame: Image.Image) -> str:
    return hashlib.sha256(frame.convert("RGBA").tobytes()).hexdigest()


def raw_master_for(asset_id: str) -> Path:
    matches = sorted(RAW_ROOT.rglob(f"{asset_id}_sheet_chroma.png"))
    if len(matches) != 1:
        raise ValueError(
            f"{asset_id}: expected one chroma master, found {len(matches)}"
        )
    return matches[0]


def normalization_index() -> dict[str, dict[str, Any]]:
    if not NORMALIZATION_REPORT.is_file():
        raise ValueError("run normalize_castle_interaction_v2_sheets.py first")
    report = json.loads(NORMALIZATION_REPORT.read_text(encoding="utf-8"))
    return {str(entry["id"]): entry for entry in report.get("assets", [])}


def _ellipse(
    role: str,
    center: tuple[float, float],
    radius: tuple[float, float],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "role": role,
        "shape": "ellipse",
        "center": list(center),
        "radius": list(radius),
        **extra,
    }


def water_layers_for(asset_id: str) -> list[dict[str, Any]]:
    if asset_id == "kitchen_sink":
        return [
            {
                "role": "stream",
                "shape": "polygon",
                "stream": True,
                "points": [
                    [0.610, 0.315], [0.645, 0.320],
                    [0.570, 0.600], [0.530, 0.600],
                ],
                "z_offset": 0.010,
                "render_priority": 2,
            },
            _ellipse(
                "basin", (0.515, 0.600), (0.235, 0.060),
                z_offset=0.009, flow_start=0.12, render_priority=1,
            ),
        ]
    if asset_id == "bubble_bath_sink":
        return [
            {
                "role": "stream",
                "shape": "polygon",
                "stream": True,
                "points": [
                    [0.485, 0.145], [0.515, 0.145],
                    [0.520, 0.350], [0.480, 0.350],
                ],
                "z_offset": 0.010,
                "render_priority": 2,
            },
            _ellipse(
                "basin", (0.500, 0.360), (0.220, 0.055),
                z_offset=0.009, flow_start=0.12, render_priority=1,
            ),
        ]
    if asset_id == "bubble_bath_bathtub":
        return [
            {
                "role": "stream",
                "shape": "polygon",
                "stream": True,
                "points": [
                    [0.190, 0.155], [0.218, 0.155],
                    [0.235, 0.350], [0.195, 0.350],
                ],
                "z_offset": 0.010,
                "render_priority": 2,
            },
            _ellipse(
                "fill", (0.515, 0.425), (0.325, 0.105),
                z_offset=0.008, flow_start=0.16, render_priority=1,
            ),
        ]
    if asset_id == "bubble_bath_toilet":
        return [
            _ellipse(
                "vortex", (0.510, 0.615), (0.120, 0.028),
                z_offset=0.003, flow_start=0.08, render_priority=1,
                active_frames=[2, 3, 4],
                contact_role="inside_bowl_cavity",
                cavity_bounds_normalized=[0.365, 0.570, 0.290, 0.090],
                occlusion_contract="front_surface_confined_to_inner_bowl_waterline",
                deep=[0.30, 0.70, 0.82, 1.0],
                shallow=[0.74, 0.95, 0.98, 1.0],
                alpha_base=0.56,
                turbulence=0.52,
                edge_foam=0.18,
                flow_speed=1.25,
            ),
        ]
    if asset_id == "mermaid_pool_flower_float":
        return [
            _ellipse(
                "ripple", (0.340, 0.780), (0.275, 0.065),
                z_offset=-0.010, render_priority=0,
            ),
        ]
    if asset_id == "mermaid_pool_star_float":
        return [
            _ellipse(
                "ripple", (0.500, 0.770), (0.420, 0.080),
                z_offset=-0.010, render_priority=0,
            ),
        ]
    if asset_id == "bubble_bath_rubber_duck":
        return [
            _ellipse(
                "ripple", (0.500, 0.760), (0.380, 0.075),
                z_offset=-0.010, render_priority=0,
            ),
        ]
    if asset_id == "mermaid_pool_waterfall":
        colors = [
            ([0.32, 0.58, 0.76, 1.0], [0.40, 0.72, 0.95, 1.0]),
            ([0.56, 0.48, 0.75, 1.0], [0.70, 0.60, 0.94, 1.0]),
            ([0.78, 0.48, 0.62, 1.0], [0.98, 0.60, 0.78, 1.0]),
            ([0.78, 0.66, 0.34, 1.0], [0.98, 0.82, 0.42, 1.0]),
            ([0.38, 0.70, 0.58, 1.0], [0.48, 0.88, 0.72, 1.0]),
        ]
        layers: list[dict[str, Any]] = []
        for index, (deep, shallow) in enumerate(colors):
            left = 0.335 + (0.400 * index / len(colors))
            right = 0.335 + (0.400 * (index + 1) / len(colors))
            layers.append({
                "role": "waterfall_band",
                "shape": "polygon",
                "stream": True,
                "deep": deep,
                "shallow": shallow,
                "points": [
                    [left, 0.265], [right, 0.265],
                    [right + 0.014, 0.805], [left - 0.014, 0.805],
                ],
                "z_offset": 0.008 + index * 0.0002,
                "render_priority": 1 + index,
            })
        layers.append(
            _ellipse(
                "waterfall_splash", (0.535, 0.820), (0.275, 0.040),
                z_offset=0.010, flow_start=0.64, render_priority=7,
            )
        )
        return layers
    if asset_id == "mermaid_pool_bubble_fountain":
        return [{
            "role": "bubble_emitter",
            "outlet_frames": [
                [0.625, 0.160], [0.625, 0.150],
                [0.625, 0.130], [0.625, 0.100],
                [0.625, 0.075], [0.625, 0.105],
                [0.625, 0.140], [0.625, 0.160],
            ],
            "relative_centers": [
                [0.000, -0.010], [-0.055, -0.020],
                [0.050, -0.030], [-0.105, -0.035],
            ],
            "flow_start": 0.15,
            "z_offset": 0.010,
        }]
    return []


def generated_entry(
    base: dict[str, Any],
    sheet_path: Path,
    normalized: dict[str, Any],
) -> dict[str, Any]:
    asset_id = str(base["id"])
    design_reference = ROOT / str(base["source"])
    placement_reference = ROOT / str(base["atlas"])
    raw_master = raw_master_for(asset_id)
    provenance_path = raw_master.parent / "provenance.json"
    if not provenance_path.is_file():
        raise ValueError(f"{asset_id}: ImageGen provenance manifest is missing")

    sheet = Image.open(sheet_path).convert("RGBA")
    if sheet.width % 4 or sheet.height % 2:
        raise ValueError(f"{asset_id}: sheet must be an exact 4x2 grid")
    if max(sheet.size) > 1024:
        raise ValueError(f"{asset_id}: runtime sheet exceeds 1024 px")
    if sha256(sheet_path) != str(normalized.get("runtime_sha256", "")):
        raise ValueError(f"{asset_id}: normalize report does not match runtime sheet")
    if not bool(normalized.get("alpha_matte_recovered", False)):
        raise ValueError(f"{asset_id}: interior alpha recovery is not recorded")
    if bool(normalized.get("rgb_subject_repainted", True)):
        raise ValueError(f"{asset_id}: normalization repainted subject pixels")

    cell_size = (sheet.width // 4, sheet.height // 2)
    bboxes: list[tuple[int, int, int, int]] = []
    hashes: list[str] = []
    for index in range(8):
        column = index % 4
        row = index // 4
        frame = sheet.crop((
            column * cell_size[0],
            row * cell_size[1],
            (column + 1) * cell_size[0],
            (row + 1) * cell_size[1],
        ))
        bboxes.append(alpha_bbox(frame))
        hashes.append(frame_hash(frame))

    placement_size_values = base.get("cell_size", [])
    placement_bbox_values = base.get("rest_alpha_bbox", [])
    if len(placement_size_values) != 2 or len(placement_bbox_values) != 4:
        raise ValueError(f"{asset_id}: v1 placement geometry is incomplete")
    placement_size = tuple(int(value) for value in placement_size_values)
    placement_bbox = tuple(int(value) for value in placement_bbox_values)

    align_index = int(ALIGNMENT_FRAME.get(asset_id, 0))
    generated_bbox = bboxes[align_index]
    ref_width = float(placement_bbox[2] - placement_bbox[0])
    ref_height = float(placement_bbox[3] - placement_bbox[1])
    gen_width = float(generated_bbox[2] - generated_bbox[0])
    gen_height = float(generated_bbox[3] - generated_bbox[1])
    runtime_scale = math.sqrt((ref_width * ref_height) / (gen_width * gen_height))
    runtime_scale = max(0.10, min(3.0, runtime_scale))

    mode = str(normalized.get(
        "anchor_mode", ANCHOR_MODE.get(asset_id, "bottom_center")
    ))
    ref_anchor = anchor(placement_bbox, mode)
    padding = float(normalized.get("padding_pixels", 6))
    if mode == "top_center":
        gen_anchor = (cell_size[0] * 0.5, padding)
    elif mode == "bottom_center":
        gen_anchor = (cell_size[0] * 0.5, cell_size[1] - padding)
    else:
        gen_anchor = (cell_size[0] * 0.5, cell_size[1] * 0.5)
    generated_cell_center = (cell_size[0] * 0.5, cell_size[1] * 0.5)
    center_offset = (
        ref_anchor[0] - (gen_anchor[0] - generated_cell_center[0]) * runtime_scale,
        ref_anchor[1] - (gen_anchor[1] - generated_cell_center[1]) * runtime_scale,
    )

    alpha = sheet.getchannel("A")
    histogram = alpha.histogram()
    border_values = (
        list(alpha.crop((0, 0, sheet.width, 1)).get_flattened_data())
        + list(alpha.crop(
            (0, sheet.height - 1, sheet.width, sheet.height)
        ).get_flattened_data())
        + list(alpha.crop((0, 0, 1, sheet.height)).get_flattened_data())
        + list(alpha.crop(
            (sheet.width - 1, 0, sheet.width, sheet.height)
        ).get_flattened_data())
    )
    timeline = list(TIMELINE_SEQUENCE.get(asset_id, RETURN_9))
    rest_frame = 7 if asset_id == "main_hall_tapestry" else 0
    sound_path = str(base.get("sound", ""))
    close_sound_path = ""
    if asset_id == "kitchen_fridge":
        sound_path = "assets/audio/castle/fridge_open.ogg"
        close_sound_path = "assets/audio/castle/fridge_close.ogg"
    entry = {
        "id": asset_id,
        "room": base["room"],
        "item_id": base["item_id"],
        "instances": base["instances"],
        "semantic_action": base["semantic_action"],
        "render_mode": "generated_full_object_states",
        "frame_count": 8,
        "hframes": 4,
        "vframes": 2,
        "sound": sound_path,
        "close_sound": close_sound_path,
        "sound_frame": int(base.get("sound_frame", 0)),
        "pitch": 1.0,
        "close_pitch": 0.94 if asset_id == "kitchen_fridge" else 1.0,
        "frame_duration_seconds": float(base.get("frame_duration_seconds", 0.10)),
        "fixed_pivot": True,
        "root_transform_animation": PHYSICS_MODE.get(asset_id, "none") != "none",
        "secondary_root_physics": PHYSICS_MODE.get(asset_id, "none") != "none",
        "normalized_use_review": "codex_visual_review_accepted_2026-08-01",
        "sheet": sheet_path.relative_to(ROOT).as_posix(),
        "sheet_sha256": sha256(sheet_path),
        "raw_chroma_master": raw_master.relative_to(ROOT).as_posix(),
        "raw_chroma_master_sha256": sha256(raw_master),
        "design_reference": design_reference.relative_to(ROOT).as_posix(),
        "design_reference_sha256": sha256(design_reference),
        "placement_reference": placement_reference.relative_to(ROOT).as_posix(),
        "placement_reference_sha256": sha256(placement_reference),
        "placement_geometry_role": "v1_runtime_rest_cell",
        "grid": [4, 2],
        "authored_frame_count": 8,
        "timeline_sequence": timeline,
        "timeline_frame_count": len(timeline),
        "cell_size": list(cell_size),
        "frame_bboxes": [list(value) for value in bboxes],
        "frame_sha256": hashes,
        "unique_frame_count": len(set(hashes)),
        "placement_size": list(placement_size),
        "placement_bbox": list(placement_bbox),
        "alignment_frame": align_index,
        "anchor_mode": mode,
        "runtime_scale": round(runtime_scale, 8),
        "runtime_center_offset": [round(value, 6) for value in center_offset],
        "hall_center_offset": [
            round(center_offset[0] - placement_size[0] * 0.5, 6),
            round(center_offset[1] - placement_size[1] * 0.5, 6),
        ],
        "rest_frame": rest_frame,
        "transparent_pixels": histogram[0],
        "partial_alpha_pixels": sum(histogram[1:255]),
        "opaque_pixels": histogram[255],
        "total_pixels": sheet.width * sheet.height,
        "transparent_border": all(value == 0 for value in border_values),
        "normalization": {
            "report": NORMALIZATION_REPORT.relative_to(ROOT).as_posix(),
            "report_sha256": repository_text_sha256(NORMALIZATION_REPORT),
            "uniform_scale": normalized.get("uniform_scale"),
            "padding_pixels": normalized.get("padding_pixels"),
            "anchor_spread_pixels": normalized.get("anchor_spread_pixels"),
            "alpha_matte_recovered": bool(normalized.get(
                "alpha_matte_recovered", False
            )),
            "alpha_recovery": normalized.get("alpha_recovery", ""),
            "rgb_subject_repainted": bool(normalized.get(
                "rgb_subject_repainted", True
            )),
            "whole_object_translation_only": True,
            "whole_sheet_uniform_scale_only": True,
            "repainted_pixels": False,
        },
        "physics_mode": PHYSICS_MODE.get(asset_id, "none"),
        "physics_pivot": PHYSICS_PIVOT.get(asset_id, [0.5, 0.5]),
        "water_layers": water_layers_for(asset_id),
        "primary_animation_is_overlay": False,
        "generated_hidden_surfaces": asset_id in {
            "kitchen_fridge", "kitchen_oven", "playroom_play_tent",
        },
        "provenance_manifest": (
            provenance_path.relative_to(ROOT).as_posix()
            if provenance_path.is_file() else ""
        ),
        "provenance_manifest_sha256": (
            repository_text_sha256(provenance_path) if provenance_path.is_file() else ""
        ),
    }
    if asset_id == "kitchen_fridge":
        entry["open_hold_step"] = 4
    return entry


def main() -> None:
    base_manifest = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
    base_assets = {str(entry["id"]): entry for entry in base_manifest["assets"]}
    normalized = normalization_index()
    output_assets: list[dict[str, Any]] = []
    missing: list[str] = []
    for asset_id, base in sorted(base_assets.items()):
        if str(base.get("room", "")) in RETIRED_V2_ROOMS:
            continue
        sheet_path = SHEET_DIR / f"{asset_id}_sheet.png"
        if not sheet_path.is_file():
            missing.append(asset_id)
            continue
        if asset_id not in normalized:
            raise ValueError(f"{asset_id}: missing normalization record")
        output_assets.append(
            generated_entry(base, sheet_path, normalized[asset_id])
        )
    if missing:
        raise ValueError("missing generated sheets: " + ", ".join(missing))

    if not CONTACT_SHEET.is_file():
        raise ValueError("build the v2 contact sheet before the manifest")
    with Image.open(CONTACT_SHEET) as contact_image:
        contact_dimensions = list(contact_image.size)
    payload = {
        "schema_version": 2,
        "generated_on": "2026-08-02",
        "generator": "tools/build_castle_interaction_v2_manifest.py",
        "generator_sha256": repository_text_sha256(Path(__file__)),
        "visual_review_evidence": {
            "path": CONTACT_SHEET.relative_to(ROOT).as_posix(),
            "sha256": sha256(CONTACT_SHEET),
            "dimensions": contact_dimensions,
            "reviewed_frame_indices": list(range(8)),
            "evidence_status": "generated_fixed_canvas_contact_sheet",
            "review_source": "per_asset_provenance_visual_review_records",
        },
        "contract": {
            "timeline_frames_min": 4,
            "timeline_frames_max": 12,
            "authored_state_count": 8,
            "primary_animation_is_overlay": False,
            "water_renderer": WATER_SHADER.relative_to(ROOT).as_posix(),
            "water_renderer_sha256": repository_text_sha256(WATER_SHADER),
            "water_ripple_texture": RIPPLE_TEXTURE.relative_to(ROOT).as_posix(),
            "water_ripple_texture_sha256": sha256(RIPPLE_TEXTURE),
            "water_caustics_texture": CAUSTICS_TEXTURE.relative_to(ROOT).as_posix(),
            "water_caustics_texture_sha256": sha256(CAUSTICS_TEXTURE),
            "water_node_type": "Sprite2D",
            "water_shader_domain": "canvas_item",
            "water_depth_write": False,
            "water_geometry_source": "per_asset_manifest_layers",
            "water_mask_source": "runtime_cached_exact_polygon_image_texture",
            "water_color_space": "source_color_uniforms_no_manual_srgb_conversion",
            "spring_component_cap": 12,
            "spring_active_cap": 8,
            "spring_logic_authority": False,
            "jolt_body_cap": 0,
            "jolt_awake_cap": 0,
            "jolt_logic_authority": False,
        },
        "frame_contract": {
            "minimum": 4,
            "maximum": 12,
            "delivered_authored_states": 8,
            "delivered_timeline_min": min(
                entry["timeline_frame_count"] for entry in output_assets
            ),
            "delivered_timeline_max": max(
                entry["timeline_frame_count"] for entry in output_assets
            ),
        },
        "rooms": {
            room_id: room
            for room_id, room in base_manifest.get("rooms", {}).items()
            if room_id not in RETIRED_V2_ROOMS
        },
        "retired_rooms": {
            "mermaid_pool": "2026-08-02 full-room regeneration uses room-derived v1 atlases"
        },
        "assets": output_assets,
        "missing_generated_assets": [],
        "summary": {
            "asset_count": len(output_assets),
            "physical_instance_count": sum(
                len(entry["instances"]) for entry in output_assets
            ),
            "generated_sheet_count": len(output_assets),
            "spring_component_count": sum(
                entry["physics_mode"] != "none" for entry in output_assets
            ),
            "jolt_component_count": 0,
            "water_interaction_count": sum(
                bool(entry["water_layers"]) for entry in output_assets
            ),
            "missing_count": 0,
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(json.dumps(payload["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
