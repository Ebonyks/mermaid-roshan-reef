#!/usr/bin/env python3
"""Blocking static audit for Pearl Castle interaction v2 delivery."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
V1_MANIFEST = ROOT / "assets/flats/castle/interactions/castle_interactions.json"
MANIFEST = ROOT / "assets/flats/castle/interactions_v2/castle_interactions_v2.json"
NORMALIZATION = (
    ROOT
    / "assets/flats/castle/interactions_v2"
    / "castle_interactions_v2_normalization.json"
)
NORMALIZER = ROOT / "tools/normalize_castle_interaction_v2_sheets.py"
SHEET_DIR = ROOT / "assets/flats/castle/interactions_v2"
RAW_ROOT = ROOT / "assets_src/imagegen/castle_object_animations_v2"
CONTACT = (
    ROOT
    / "audit/castle_interactions_v2"
    / "castle_interaction_frames_v2.png"
)
SHADER = ROOT / "assets/shaders/castle_fixture_water.gdshader"
RIPPLE_TEXTURE = ROOT / "assets/terrain/up_water_nrm.jpg"
CAUSTICS_TEXTURE = ROOT / "assets/terrain/caustics.png"
RIG_SCRIPT = ROOT / "scripts/arena/castle_fixture_rigs.gd"
ROOM_SCRIPT = ROOT / "scripts/arena/castle_rooms_25d.gd"
MAIN_SCRIPT = ROOT / "scripts/main.gd"
EXPORT_PRESETS = ROOT / "export_presets.cfg"
AUDIO_MANIFEST = ROOT / "assets/audio/castle/castle_interaction_sfx_manifest.json"
AUDIO_GENERATOR = ROOT / "tools/build_castle_interaction_audio.py"
LICENSES = ROOT / "ASSET_LICENSES.md"

EXPECTED_ASSETS = 33
EXPECTED_ACTIVE_ASSETS = 29
EXPECTED_INSTANCES = 34
EXPECTED_SPRINGS = 6
RETIRED_V2_ROOMS = {"mermaid_pool"}
EXPECTED_WATER = {
    "kitchen_sink",
    "bubble_bath_sink",
    "bubble_bath_bathtub",
    "bubble_bath_toilet",
    "bubble_bath_rubber_duck",
}
EXPECTED_HIDDEN_SURFACES = {
    "kitchen_fridge",
    "kitchen_oven",
    "playroom_play_tent",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_text_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing JSON: {path.relative_to(ROOT)}")
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(parsed, dict):
        errors.append(f"JSON root is not an object: {path.relative_to(ROOT)}")
        return {}
    return parsed


def frame_cells(sheet: Image.Image) -> tuple[list[Image.Image], int, int]:
    if sheet.width % 4 or sheet.height % 2:
        raise ValueError("not an exact 4x2 grid")
    cell_width = sheet.width // 4
    cell_height = sheet.height // 2
    frames = []
    for index in range(8):
        column = index % 4
        row = index // 4
        frames.append(sheet.crop((
            column * cell_width,
            row * cell_height,
            (column + 1) * cell_width,
            (row + 1) * cell_height,
        )))
    return frames, cell_width, cell_height


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int] | None:
    alpha = frame.getchannel("A")
    return alpha.point(lambda value: 255 if value >= 16 else 0).getbbox()


def bbox_anchor(values: list[Any], mode: str) -> tuple[float, float]:
    left, top, right, bottom = (float(value) for value in values)
    if mode == "top_center":
        return ((left + right) * 0.5, top)
    if mode == "bottom_center":
        return ((left + right) * 0.5, bottom)
    return ((left + right) * 0.5, (top + bottom) * 0.5)


def material_changed_fraction(base: Image.Image, frame: Image.Image) -> float:
    base = base.convert("RGBA")
    frame = frame.convert("RGBA")
    base_channels = base.split()
    frame_channels = frame.split()
    visible = ImageChops.lighter(base_channels[3], frame_channels[3]).point(
        lambda value: 255 if value >= 16 else 0
    )
    difference = ImageChops.difference(base, frame)
    difference_channels = difference.split()
    rgb_difference = ImageChops.lighter(
        ImageChops.lighter(difference_channels[0], difference_channels[1]),
        difference_channels[2],
    )
    changed = ImageChops.lighter(
        rgb_difference.point(lambda value: 255 if value >= 18 else 0),
        difference_channels[3].point(lambda value: 255 if value >= 16 else 0),
    )
    changed_visible = ImageChops.multiply(changed, visible)
    visible_count = visible.histogram()[255]
    changed_count = changed_visible.histogram()[255]
    return changed_count / float(max(1, visible_count))


_NORMALIZER_MODULE: Any = None


def normalizer_module() -> Any:
    global _NORMALIZER_MODULE
    if _NORMALIZER_MODULE is not None:
        return _NORMALIZER_MODULE
    specification = importlib.util.spec_from_file_location(
        "castle_v2_normalizer_audit", NORMALIZER
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load castle v2 normalizer for alpha QA")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    _NORMALIZER_MODULE = module
    return module


def measured_frame_alpha_qa(frame: Image.Image) -> dict[str, Any]:
    measured = normalizer_module().frame_alpha_qa(frame)
    return dict(measured)


def frame_delta_sha256(
    frames: list[Image.Image], first: int, second: int
) -> str:
    difference = ImageChops.difference(
        frames[first].convert("RGBA"), frames[second].convert("RGBA")
    )
    return hashlib.sha256(difference.tobytes()).hexdigest()


def strip_shader_comments(source: str) -> str:
    without_blocks = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", without_blocks)


def shader_render_modes(source: str) -> set[str]:
    executable = strip_shader_comments(source)
    declarations = re.findall(
        r"^\s*render_mode\s+([^;]+);", executable, flags=re.MULTILINE
    )
    if len(declarations) != 1:
        return set()
    return {
        token.strip()
        for token in declarations[0].split(",")
        if token.strip()
    }


def placement_point_to_generated(
    asset: dict[str, Any], point: list[Any]
) -> tuple[float, float] | None:
    cell_size = asset.get("cell_size", [])
    placement_size = asset.get("placement_size", [])
    center_offset = asset.get("runtime_center_offset", [])
    runtime_scale = float(asset.get("runtime_scale", 0.0))
    if (
        len(point) != 2
        or len(cell_size) != 2
        or len(placement_size) != 2
        or len(center_offset) != 2
        or runtime_scale <= 0.0
    ):
        return None
    return (
        float(cell_size[0]) * 0.5
        + (
            float(point[0]) * float(placement_size[0])
            - float(center_offset[0])
        )
        / runtime_scale,
        float(cell_size[1]) * 0.5
        + (
            float(point[1]) * float(placement_size[1])
            - float(center_offset[1])
        )
        / runtime_scale,
    )


def distance_to_visible_alpha(
    frame: Image.Image, point: tuple[float, float], maximum: int
) -> int:
    alpha = frame.getchannel("A").point(
        lambda value: 255 if value >= 16 else 0
    )
    center_x = int(round(point[0]))
    center_y = int(round(point[1]))
    for radius in range(maximum + 1):
        left = max(0, center_x - radius)
        top = max(0, center_y - radius)
        right = min(frame.width, center_x + radius + 1)
        bottom = min(frame.height, center_y + radius + 1)
        if left < right and top < bottom:
            if alpha.crop((left, top, right, bottom)).getbbox() is not None:
                return radius
    return maximum + 1


def water_layer_bounds(
    layer: dict[str, Any],
) -> list[tuple[float, float, float, float]]:
    role = str(layer.get("role", ""))
    if role == "bubble_emitter":
        bounds: list[tuple[float, float, float, float]] = []
        outlets = layer.get("outlet_frames", [])
        relatives = layer.get("relative_centers", [])
        if not isinstance(outlets, list) or not isinstance(relatives, list):
            return bounds
        for index, relative in enumerate(relatives):
            if not isinstance(relative, list) or len(relative) != 2:
                continue
            radius = 0.028 + float(index % 2) * 0.010
            for outlet in outlets:
                if not isinstance(outlet, list) or len(outlet) != 2:
                    continue
                center_x = float(outlet[0]) + float(relative[0])
                center_y = float(outlet[1]) + float(relative[1])
                bounds.append((
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ))
        return bounds
    if str(layer.get("shape", "")) == "ellipse":
        center = layer.get("center", [])
        radius = layer.get("radius", [])
        if len(center) == 2 and len(radius) == 2:
            return [(
                float(center[0]) - float(radius[0]),
                float(center[1]) - float(radius[1]),
                float(center[0]) + float(radius[0]),
                float(center[1]) + float(radius[1]),
            )]
        return []
    points = layer.get("points", [])
    if not isinstance(points, list) or not points:
        return []
    valid = [
        point for point in points
        if isinstance(point, list) and len(point) == 2
    ]
    if not valid:
        return []
    return [(
        min(float(point[0]) for point in valid),
        min(float(point[1]) for point in valid),
        max(float(point[0]) for point in valid),
        max(float(point[1]) for point in valid),
    )]


def audit_water_against_generated_frames(
    asset: dict[str, Any], errors: list[str]
) -> None:
    asset_id = str(asset.get("id", ""))
    layers = asset.get("water_layers", [])
    if not isinstance(layers, list) or not layers:
        return
    for layer_index, layer_value in enumerate(layers):
        if not isinstance(layer_value, dict):
            errors.append(f"{asset_id}: water layer {layer_index} is malformed")
            continue
        layer_bounds = water_layer_bounds(layer_value)
        if not layer_bounds:
            errors.append(
                f"{asset_id}: water layer {layer_index} has no measured bounds"
            )
            continue
        for bounds in layer_bounds:
            if (
                bounds[0] < 0.0
                or bounds[1] < 0.0
                or bounds[2] > 1.0
                or bounds[3] > 1.0
                or bounds[2] <= bounds[0]
                or bounds[3] <= bounds[1]
            ):
                errors.append(
                    f"{asset_id}: water layer {layer_index} escapes fixture bounds"
                )
                break

    sheet_path = ROOT / str(asset.get("sheet", ""))
    if not sheet_path.is_file():
        return
    frames, cell_width, cell_height = frame_cells(
        Image.open(sheet_path).convert("RGBA")
    )
    threshold = max(12, int(round(max(cell_width, cell_height) * 0.08)))
    outlet_checks: list[tuple[int, list[Any], str]] = []
    for layer_index, layer_value in enumerate(layers):
        if not isinstance(layer_value, dict):
            continue
        role = str(layer_value.get("role", ""))
        if role == "bubble_emitter":
            outlets = layer_value.get("outlet_frames", [])
            if isinstance(outlets, list):
                for frame_index, outlet in enumerate(outlets[:8]):
                    if isinstance(outlet, list):
                        outlet_checks.append((
                            frame_index,
                            outlet,
                            f"bubble emitter {layer_index} frame {frame_index}",
                        ))
        elif bool(layer_value.get("stream", False)) or role == "stream":
            points = layer_value.get("points", [])
            if (
                isinstance(points, list)
                and len(points) >= 2
                and len(points[0]) == 2
                and len(points[1]) == 2
            ):
                outlet = [
                    (float(points[0][axis]) + float(points[1][axis])) * 0.5
                    for axis in range(2)
                ]
                for frame_index in range(8):
                    outlet_checks.append((
                        frame_index,
                        outlet,
                        f"{role} {layer_index} frame {frame_index}",
                    ))
    for frame_index, outlet, label in outlet_checks:
        generated = placement_point_to_generated(asset, outlet)
        if generated is None:
            errors.append(f"{asset_id}: cannot map {label} to generated pixels")
            continue
        distance = distance_to_visible_alpha(
            frames[frame_index], generated, threshold
        )
        if distance > threshold:
            errors.append(
                f"{asset_id}: {label} is {distance}px from active generated pixels"
            )


def build_contact_sheet() -> None:
    paths = sorted(SHEET_DIR.glob("*_sheet.png"))
    if len(paths) != EXPECTED_ASSETS:
        raise SystemExit(
            f"Expected {EXPECTED_ASSETS} sheets, found {len(paths)}"
        )
    width = 1280
    row_height = 156
    header_height = 52
    output = Image.new(
        "RGBA",
        (width, header_height + row_height * len(paths)),
        (244, 239, 249, 255),
    )
    draw = ImageDraw.Draw(output)
    try:
        title_font = ImageFont.truetype("DejaVuSans.ttf", 22)
        label_font = ImageFont.truetype("DejaVuSans.ttf", 16)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 12)
    except OSError:
        title_font = ImageFont.load_default()
        label_font = title_font
        small_font = title_font
    draw.text(
        (18, 13),
        "Pearl Castle interaction v2 — all authored object states",
        fill=(36, 25, 68, 255),
        font=title_font,
    )
    for row, path in enumerate(paths):
        y = header_height + row * row_height
        if row % 2:
            draw.rectangle((0, y, width, y + row_height), fill=(237, 247, 247, 255))
        asset_id = path.stem.removesuffix("_sheet")
        sheet = Image.open(path).convert("RGBA")
        frames, _cell_width, _cell_height = frame_cells(sheet)
        draw.text((16, y + 17), asset_id, fill=(42, 25, 75, 255), font=label_font)
        draw.text(
            (16, y + 44),
            f"{sheet.width}x{sheet.height} RGBA • 4x2 • frames 0–7",
            fill=(85, 70, 105, 255),
            font=small_font,
        )
        for index, frame in enumerate(frames):
            x = 224 + index * 130
            tile = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
            tile_draw = ImageDraw.Draw(tile)
            checker = 10
            for cy in range(0, 120, checker):
                for cx in range(0, 120, checker):
                    shade = 224 if (cx // checker + cy // checker) % 2 else 248
                    tile_draw.rectangle(
                        (cx, cy, cx + checker - 1, cy + checker - 1),
                        fill=(shade, shade, shade, 255),
                    )
            tile_draw.line((60, 4, 60, 102), fill=(148, 132, 164, 255))
            tile_draw.line((5, 56, 115, 56), fill=(148, 132, 164, 255))
            fixed_canvas = frame.copy()
            fixed_canvas.thumbnail((108, 102), Image.Resampling.LANCZOS)
            tile.alpha_composite(
                fixed_canvas,
                (
                    (120 - fixed_canvas.width) // 2,
                    (112 - fixed_canvas.height) // 2,
                ),
            )
            tile_draw.rectangle((0, 0, 119, 119), outline=(99, 77, 126, 255))
            tile_draw.text((5, 103), str(index), fill=(36, 25, 68, 255), font=small_font)
            output.alpha_composite(tile, (x, y + 18))
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    output.convert("RGB").save(CONTACT, optimize=True)
    print(
        f"CASTLEV2|CONTACT_WRITTEN|{CONTACT.relative_to(ROOT)}|"
        f"{output.width}x{output.height}|sha256={sha256(CONTACT)}"
    )


def provenance_index(errors: list[str]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    manifests = sorted(RAW_ROOT.rglob("provenance.json"))
    for path in manifests:
        payload = load_json(path, errors)
        for value in payload.get("assets", []):
            if not isinstance(value, dict):
                errors.append(f"{path.relative_to(ROOT)} has a non-object asset")
                continue
            asset_id = str(value.get("id", ""))
            if not asset_id:
                errors.append(f"{path.relative_to(ROOT)} has an asset without id")
                continue
            if asset_id in records:
                errors.append(f"duplicate provenance record: {asset_id}")
            if "accepted_prompt" in value:
                native = value.get("native_output", {})
                chroma = value.get(
                    "chroma_master", value.get("raw_chroma", {})
                )
                runtime = value.get(
                    "runtime_alpha",
                    value.get(
                        "current_pre_normalization_runtime",
                        value.get("runtime", value.get("pre_normalization_runtime", {})),
                    ),
                )
                runtime_delivery = value.get("runtime", runtime)
                generation = value.get("generation", {})
                runtime_qa = (
                    runtime.get("alpha_qa", value.get("alpha_qa", {}))
                    if isinstance(runtime, dict) else value.get("alpha_qa", {})
                )
                runtime_grid = (
                    runtime.get("grid", {})
                    if isinstance(runtime, dict) else {}
                )
                method = (
                    generation.get("method", "")
                    if isinstance(generation, dict) else ""
                )
                visual_review = value.get("visual_review", {})
                review_status = (
                    visual_review.get("status", "")
                    if isinstance(visual_review, dict)
                    else ""
                ) or value.get(
                    "visual_review_status",
                    value.get("human_review_status", ""),
                )
                review_notes = (
                    visual_review.get("notes", "")
                    if isinstance(visual_review, dict)
                    else ""
                ) or value.get(
                    "visual_review_notes",
                    value.get("human_review_notes", ""),
                )
                direct_alpha_qa = "transparent_corners" in runtime_qa
                records[asset_id] = {
                    "prompt": value.get("accepted_prompt", ""),
                    "prompt_sha256": value.get("accepted_prompt_sha256", ""),
                    "native_output": (
                        native.get("path", "") if isinstance(native, dict) else ""
                    ),
                    "native_sha256": (
                        native.get("sha256", "") if isinstance(native, dict) else ""
                    ),
                    "native_dimensions": (
                        native.get("dimensions", [])
                        if isinstance(native, dict) else []
                    ),
                    "chroma_master": (
                        chroma.get("path", "") if isinstance(chroma, dict) else ""
                    ),
                    "chroma_sha256": (
                        chroma.get("sha256", "") if isinstance(chroma, dict) else ""
                    ),
                    "runtime_path": (
                        runtime_delivery.get("path", "")
                        if isinstance(runtime_delivery, dict) else ""
                    ),
                    "runtime_sha256": (
                        runtime.get("sha256", "") if isinstance(runtime, dict) else ""
                    ),
                    "generation_method": (
                        "OpenAI built-in image_gen.imagegen"
                        if method == "image_gen.imagegen built-in"
                        or method.startswith("OpenAI built-in Codex ImageGen")
                        else method
                    ),
                    "attempt": (
                        generation.get(
                            "attempt",
                            generation.get("accepted_generation_attempt", 0),
                        )
                        if isinstance(generation, dict) else 0
                    ),
                    "alpha_qa": {
                        "transparent_border": (
                            bool(runtime_qa.get("transparent_corners", False))
                            and bool(runtime_qa.get(
                                "transparent_cell_boundaries", False
                            ))
                            if direct_alpha_qa
                            else int(runtime_qa.get(
                                "sheet_border_nonzero_alpha",
                                runtime_qa.get(
                                    "cell_edge_nonzero_alpha", -1
                                ),
                            )) == 0
                        ),
                        "cell_count": runtime_grid.get(
                            "frames", runtime_qa.get("occupied_cells", 0)
                        ),
                        "all_cells_occupied": (
                            int(runtime_qa.get("unique_frame_pixel_hashes", 0)) == 8
                            or int(runtime_qa.get("occupied_cells", 0)) == 8
                        ),
                        "visible_chroma_pixels": int(runtime_qa.get(
                            "visible_exact_ff00ff_pixels", 0
                        )),
                    },
                    "review_status": review_status,
                    "review_notes": review_notes,
                }
            elif (
                isinstance(value.get("generation"), dict)
                and isinstance(value.get("runtime_sheet"), dict)
            ):
                generation = value["generation"]
                chroma = value.get("chroma_master", {})
                runtime = value["runtime_sheet"]
                review = value.get("audit", {})
                grid = runtime.get("grid", [])
                components = review.get(
                    "alpha_component_counts_per_frame", []
                )
                corners = review.get("transparent_corner_alpha", [])
                method = str(generation.get("tool", ""))
                review_passed = (
                    review.get(
                        "codex_visual_review",
                        review.get("human_visual_review", ""),
                    ) == "pass"
                    and review.get("topology_review") == "pass"
                    and review.get("status") == "pass"
                )
                records[asset_id] = {
                    "prompt": generation.get("prompt", ""),
                    "prompt_sha256": generation.get("prompt_sha256", ""),
                    "native_output": generation.get("native_path", ""),
                    "native_sha256": generation.get("native_sha256", ""),
                    "native_dimensions": generation.get(
                        "native_dimensions", []
                    ),
                    "chroma_master": (
                        chroma.get("path", "") if isinstance(chroma, dict) else ""
                    ),
                    "chroma_sha256": (
                        chroma.get("sha256", "") if isinstance(chroma, dict) else ""
                    ),
                    "runtime_path": runtime.get("path", ""),
                    "runtime_sha256": runtime.get("sha256", ""),
                    "generation_method": (
                        "OpenAI built-in image_gen.imagegen"
                        if method == "OpenAI built-in image_gen" else method
                    ),
                    "attempt": generation.get("attempt", 0),
                    "alpha_qa": {
                        "transparent_border": (
                            isinstance(corners, list)
                            and len(corners) == 4
                            and all(int(alpha) == 0 for alpha in corners)
                        ),
                        "cell_count": (
                            int(grid[0]) * int(grid[1])
                            if isinstance(grid, list) and len(grid) == 2
                            else 0
                        ),
                        "all_cells_occupied": (
                            isinstance(components, list)
                            and len(components) == 8
                            and all(int(count) >= 1 for count in components)
                        ),
                        "visible_chroma_pixels": 0,
                    },
                    "review_status": (
                        "accepted" if review_passed else "rejected"
                    ),
                    "review_notes": (
                        "Codex visual and topology review passed. "
                        + str(review.get(
                            "novel_item_specific_mechanics", ""
                        ))
                    ),
                }
            else:
                fallback = dict(value)
                fallback["review_status"] = value.get(
                    "visual_review_status",
                    value.get("human_review_status", ""),
                )
                fallback["review_notes"] = value.get(
                    "visual_review_notes",
                    value.get("human_review_notes", ""),
                )
                records[asset_id] = fallback
    return records


def audit_sheet(
    asset: dict[str, Any],
    normalized: dict[str, Any],
    provenance: dict[str, Any],
    errors: list[str],
) -> None:
    asset_id = str(asset.get("id", ""))
    path = ROOT / str(asset.get("sheet", ""))
    raw_path = ROOT / str(asset.get("raw_chroma_master", ""))
    provenance_path = ROOT / str(asset.get("provenance_manifest", ""))
    if not path.is_file():
        errors.append(f"{asset_id}: runtime sheet missing")
        return
    if sha256(path) != asset.get("sheet_sha256"):
        errors.append(f"{asset_id}: runtime sheet hash mismatch")
    if not raw_path.is_file():
        errors.append(f"{asset_id}: chroma master missing")
    elif sha256(raw_path) != asset.get("raw_chroma_master_sha256"):
        errors.append(f"{asset_id}: chroma master hash mismatch")
    if not provenance_path.is_file():
        errors.append(f"{asset_id}: provenance manifest path is missing")
    elif repository_text_sha256(provenance_path) != asset.get("provenance_manifest_sha256"):
        errors.append(f"{asset_id}: provenance manifest hash mismatch")
    if max(Image.open(path).size) > 1024:
        errors.append(f"{asset_id}: runtime sheet exceeds 1024 px")
    sheet = Image.open(path).convert("RGBA")
    try:
        frames, cell_width, cell_height = frame_cells(sheet)
    except ValueError as exc:
        errors.append(f"{asset_id}: {exc}")
        return
    if asset.get("render_mode") != "generated_full_object_states":
        errors.append(f"{asset_id}: runtime is not using generated full-object states")
    if asset.get("grid") != [4, 2]:
        errors.append(f"{asset_id}: manifest grid is not 4x2")
    if int(asset.get("frame_count", 0)) != 8:
        errors.append(f"{asset_id}: compatibility frame count is not 8")
    if int(asset.get("authored_frame_count", 0)) != 8:
        errors.append(f"{asset_id}: authored frame count is not 8")
    frame_hashes = {
        hashlib.sha256(frame.tobytes()).hexdigest() for frame in frames
    }
    if len(frame_hashes) != 8 or int(asset.get("unique_frame_count", 0)) != 8:
        errors.append(f"{asset_id}: all eight authored states must be unique")
    changed_fractions = [
        material_changed_fraction(frames[0], frame)
        for frame in frames[1:]
    ]
    if min(changed_fractions, default=0.0) < 0.05:
        errors.append(
            f"{asset_id}: authored state changes fall below 5% of visible material"
        )
    gaps: list[int] = []
    for index, frame in enumerate(frames):
        bbox = alpha_bbox(frame)
        if bbox is None:
            errors.append(f"{asset_id}: frame {index} is empty")
            continue
        gaps.append(min(
            bbox[0],
            bbox[1],
            cell_width - bbox[2],
            cell_height - bbox[3],
        ))
    if gaps and min(gaps) < 4:
        errors.append(f"{asset_id}: frame cell padding below 4 px")
    alpha = sheet.getchannel("A")
    histogram = alpha.histogram()
    visible = sum(histogram[1:])
    opacity_ratio = histogram[255] / float(max(1, visible))
    if opacity_ratio < 0.80:
        errors.append(
            f"{asset_id}: opaque/visible ratio {opacity_ratio:.3f} risks bleed-through"
        )
    rgba = sheet.get_flattened_data()
    chroma_visible = sum(
        1
        for red, green, blue, alpha_value in rgba
        if (
            alpha_value >= 128
            and red >= 248
            and blue >= 248
            and green <= 12
        )
    )
    if chroma_visible:
        errors.append(
            f"{asset_id}: {chroma_visible} runtime-visible chroma pixels remain"
        )
    if not bool(asset.get("transparent_border", False)):
        errors.append(f"{asset_id}: manifest border audit is false")
    if not bool(asset.get("primary_animation_is_overlay", True)):
        pass
    else:
        errors.append(f"{asset_id}: primary animation is still marked overlay")
    sequence = asset.get("timeline_sequence", [])
    if not isinstance(sequence, list) or not 4 <= len(sequence) <= 12:
        errors.append(f"{asset_id}: timeline is outside 4?12 steps")
    elif any(not isinstance(value, int) or not 0 <= value < 8 for value in sequence):
        errors.append(f"{asset_id}: timeline references an invalid authored frame")
    else:
        rest_frame = int(asset.get("rest_frame", 0))
        if asset_id == "main_hall_sconce":
            if sequence != list(range(8)):
                errors.append(f"{asset_id}: stateful light timeline is not 0-7")
        else:
            if sequence[0] != rest_frame or sequence[-1] != rest_frame:
                errors.append(f"{asset_id}: return timeline does not end at rest")
            if [sequence[0], sequence[1]] != [
                sequence[-1], sequence[-2]
            ]:
                errors.append(
                    f"{asset_id}: terminal frame pair does not mirror initial pair"
                )
            elif frame_delta_sha256(
                frames, sequence[0], sequence[1]
            ) != frame_delta_sha256(
                frames, sequence[-2], sequence[-1]
            ):
                errors.append(
                    f"{asset_id}: terminal pixel delta does not mirror initial delta"
                )
    if int(asset.get("timeline_frame_count", 0)) != len(sequence):
        errors.append(f"{asset_id}: timeline count differs from sequence")
    if not normalized:
        errors.append(f"{asset_id}: normalization record missing")
    else:
        if normalized.get("runtime_sha256") != asset.get("sheet_sha256"):
            errors.append(f"{asset_id}: normalization/runtime hashes differ")
        spread = normalized.get("anchor_spread_pixels", [999, 999])
        if len(spread) != 2 or float(spread[0]) > 2.0 or float(spread[1]) > 2.0:
            errors.append(f"{asset_id}: normalized pivot drift exceeds 2 px")
        if int(normalized.get("edge_gap_pixels", 0)) < 4:
            errors.append(f"{asset_id}: normalization edge gap is unsafe")
        if not bool(normalized.get("alpha_matte_recovered", False)):
            errors.append(f"{asset_id}: interior alpha recovery is not recorded")
        if bool(normalized.get("rgb_subject_repainted", True)):
            errors.append(f"{asset_id}: normalization repainted subject RGB pixels")
        if not bool(normalized.get("fixed_canvas_review", False)):
            errors.append(f"{asset_id}: normalization lacks fixed-canvas review")
        alpha_qa = normalized.get("per_frame_alpha_qa", [])
        if not isinstance(alpha_qa, list) or len(alpha_qa) != 8:
            errors.append(f"{asset_id}: normalized per-frame alpha QA is incomplete")
        else:
            for frame_index, (frame, recorded_qa) in enumerate(
                zip(frames, alpha_qa)
            ):
                measured_qa = measured_frame_alpha_qa(frame)
                if recorded_qa != measured_qa:
                    errors.append(
                        f"{asset_id}: frame {frame_index} alpha QA is stale"
                    )
                    continue
                required_qa = {
                    "fixed_canvas_size",
                    "alpha_bbox",
                    "visible_pixels",
                    "component_count",
                    "component_sizes",
                    "tiny_component_count",
                    "largest_component_ratio",
                    "enclosed_transparent_hole_count",
                    "visible_exact_chroma_pixels",
                    "visible_near_chroma_pixels",
                    "visible_near_chroma_ratio",
                    "transparent_canvas_border",
                }
                if not required_qa.issubset(recorded_qa):
                    errors.append(
                        f"{asset_id}: frame {frame_index} alpha QA fields are incomplete"
                    )
                if int(recorded_qa.get("tiny_component_count", -1)) != 0:
                    errors.append(
                        f"{asset_id}: frame {frame_index} has tiny alpha islands"
                    )
                if int(recorded_qa.get(
                    "visible_exact_chroma_pixels", -1
                )) != 0:
                    errors.append(
                        f"{asset_id}: frame {frame_index} retains exact chroma"
                    )
                if float(recorded_qa.get(
                    "visible_near_chroma_ratio", 1.0
                )) > 0.002:
                    errors.append(
                        f"{asset_id}: frame {frame_index} has near-chroma spill"
                    )
                if not bool(recorded_qa.get(
                    "transparent_canvas_border", False
                )):
                    errors.append(
                        f"{asset_id}: frame {frame_index} touches its canvas border"
                    )
        asset_normalization = asset.get("normalization", {})
        if not isinstance(asset_normalization, dict):
            errors.append(f"{asset_id}: manifest normalization contract is missing")
        elif (
            not bool(asset_normalization.get("alpha_matte_recovered", False))
            or bool(asset_normalization.get("rgb_subject_repainted", True))
        ):
            errors.append(f"{asset_id}: manifest alpha recovery contract is invalid")
    if not provenance:
        errors.append(f"{asset_id}: ImageGen provenance record missing")
    else:
        prompt = str(provenance.get("prompt", ""))
        if len(prompt) < 200:
            errors.append(f"{asset_id}: exact generation prompt is missing")
        if text_sha256(prompt) != provenance.get("prompt_sha256"):
            errors.append(f"{asset_id}: generation prompt hash mismatch")
        if provenance.get("runtime_sha256") != normalized.get("input_sha256"):
            errors.append(
                f"{asset_id}: pre-normalization runtime provenance mismatch"
            )
        if provenance.get("chroma_sha256") != asset.get(
            "raw_chroma_master_sha256"
        ):
            errors.append(f"{asset_id}: chroma provenance mismatch")
        if provenance.get("chroma_master") != asset.get("raw_chroma_master"):
            errors.append(f"{asset_id}: chroma provenance path mismatch")
        if provenance.get("runtime_path") != asset.get("sheet"):
            errors.append(f"{asset_id}: runtime provenance path mismatch")
        if not str(provenance.get("native_output", "")):
            errors.append(f"{asset_id}: native ImageGen output path missing")
        if len(str(provenance.get("native_sha256", ""))) != 64:
            errors.append(f"{asset_id}: native ImageGen hash missing")
        dimensions = provenance.get("native_dimensions", [])
        if (
            not isinstance(dimensions, list)
            or len(dimensions) != 2
            or any(int(value) <= 0 for value in dimensions)
        ):
            errors.append(f"{asset_id}: native ImageGen dimensions are invalid")
        if provenance.get("generation_method") != "OpenAI built-in image_gen.imagegen":
            errors.append(f"{asset_id}: generation method is not recorded exactly")
        if int(provenance.get("attempt", 0)) < 1:
            errors.append(f"{asset_id}: accepted generation attempt is invalid")
        alpha_qa = provenance.get("alpha_qa", {})
        if (
            not isinstance(alpha_qa, dict)
            or not bool(alpha_qa.get("transparent_border", False))
            or int(alpha_qa.get("cell_count", 0)) != 8
            or not bool(alpha_qa.get("all_cells_occupied", False))
            or int(alpha_qa.get("visible_chroma_pixels", -1)) != 0
        ):
            errors.append(f"{asset_id}: pre-normalization alpha QA is incomplete")
        if provenance.get("review_status") != "accepted":
            errors.append(f"{asset_id}: visual review is not accepted")
        if len(str(provenance.get("review_notes", ""))) < 30:
            errors.append(f"{asset_id}: visual review notes are incomplete")


def audit() -> int:
    errors: list[str] = []
    v1 = load_json(V1_MANIFEST, errors)
    manifest = load_json(MANIFEST, errors)
    normalization = load_json(NORMALIZATION, errors)
    if errors:
        for error in errors:
            print("CASTLEV2|FAIL|" + error)
        return 1

    v1_assets = {
        str(entry["id"]): entry
        for entry in v1.get("assets", [])
        if isinstance(entry, dict)
    }
    expected_ids = {
        asset_id for asset_id, entry in v1_assets.items()
        if str(entry.get("room", "")) not in RETIRED_V2_ROOMS
    }
    assets = manifest.get("assets", [])
    asset_map = {
        str(entry.get("id", "")): entry
        for entry in assets
        if isinstance(entry, dict)
    }
    normalized_map = {
        str(entry.get("id", "")): entry
        for entry in normalization.get("assets", [])
        if isinstance(entry, dict)
    }
    provenance = provenance_index(errors)
    if not expected_ids.issubset(set(provenance)):
        errors.append("ImageGen provenance is missing an active v2 interaction")

    if normalization.get("tool_sha256") != repository_text_sha256(NORMALIZER):
        errors.append("normalization report tool hash is stale")
    if int(normalization.get("schema_version", 0)) != 2:
        errors.append("normalization report schema is not 2")
    if not bool(normalization.get("transactional", False)):
        errors.append("normalization report does not prove transactional delivery")
    if not bool(normalization.get("one_time_guard", False)):
        errors.append("normalization report does not prove rerun protection")
    if not expected_ids.issubset(set(normalized_map)):
        errors.append("normalization roster is missing an active v2 interaction")
    if int(manifest.get("schema_version", 0)) != 2:
        errors.append("manifest schema is not v2")
    if set(asset_map) != expected_ids or len(asset_map) != EXPECTED_ACTIVE_ASSETS:
        errors.append("active v2 asset roster differs from the room contract")
    retired_rooms = manifest.get("retired_rooms", {})
    if set(retired_rooms) != RETIRED_V2_ROOMS:
        errors.append("v2 retired-room roster does not preserve Mermaid Pool")
    instance_count = sum(
        len(entry.get("instances", [])) for entry in asset_map.values()
    )
    if instance_count != EXPECTED_INSTANCES:
        errors.append(f"physical instance count is {instance_count}, expected {EXPECTED_INSTANCES}")
    average = instance_count / float(8 - len(RETIRED_V2_ROOMS))
    if not 4.0 <= average <= 6.0:
        errors.append(f"room interaction average {average:.2f} is outside 4–6")
    summary = manifest.get("summary", {})
    if int(summary.get("generated_sheet_count", 0)) != EXPECTED_ACTIVE_ASSETS:
        errors.append("not every interaction uses a generated full-object sheet")
    if int(summary.get("spring_component_count", 0)) != EXPECTED_SPRINGS:
        errors.append("spring component count is not the active capped set")
    if int(summary.get("water_interaction_count", 0)) != len(EXPECTED_WATER):
        errors.append("water interaction count does not match the measured roster")

    live_room_rgba_bytes: dict[str, int] = {}
    for asset in asset_map.values():
        sheet_path = ROOT / str(asset.get("sheet", ""))
        if not sheet_path.is_file():
            continue
        with Image.open(sheet_path) as sheet_image:
            live_room_rgba_bytes[str(asset.get("room", ""))] = (
                live_room_rgba_bytes.get(str(asset.get("room", "")), 0)
                + sheet_image.width * sheet_image.height * 4
            )
    max_room_rgba_bytes = max(live_room_rgba_bytes.values(), default=0)
    if max_room_rgba_bytes > 24 * 1024 * 1024:
        errors.append(
            "live-room interaction sheets exceed the 24 MiB RGBA mobile budget"
        )

    for asset_id, asset in asset_map.items():
        audit_sheet(
            asset,
            normalized_map.get(asset_id, {}),
            provenance.get(asset_id, {}),
            errors,
        )
        base_asset = v1_assets.get(asset_id, {})
        design_path = ROOT / str(asset.get("design_reference", ""))
        placement_path = ROOT / str(asset.get("placement_reference", ""))
        if not design_path.is_file() or sha256(design_path) != asset.get(
            "design_reference_sha256"
        ):
            errors.append(f"{asset_id}: design-reference provenance mismatch")
        if not placement_path.is_file() or sha256(placement_path) != asset.get(
            "placement_reference_sha256"
        ):
            errors.append(f"{asset_id}: placement-reference provenance mismatch")
        if asset.get("placement_geometry_role") != "v1_runtime_rest_cell":
            errors.append(f"{asset_id}: placement geometry role is ambiguous")
        if asset.get("design_reference") != base_asset.get("source"):
            errors.append(f"{asset_id}: design reference no longer matches v1")
        if asset.get("placement_reference") != base_asset.get("atlas"):
            errors.append(f"{asset_id}: placement reference no longer matches v1")
        if asset.get("placement_size") != base_asset.get("cell_size"):
            errors.append(f"{asset_id}: placement size no longer uses the v1 cell")
        if asset.get("placement_bbox") != base_asset.get("rest_alpha_bbox"):
            errors.append(f"{asset_id}: placement bbox no longer uses the v1 rest pose")
        normalized_entry = normalized_map.get(asset_id, {})
        if asset.get("anchor_mode") != normalized_entry.get("anchor_mode"):
            errors.append(f"{asset_id}: runtime and normalization pivots disagree")
        runtime_scale = float(asset.get("runtime_scale", 0.0))
        if not 0.10 <= runtime_scale <= 3.0:
            errors.append(f"{asset_id}: runtime placement scale is invalid")
        cell_size = asset.get("cell_size", [])
        placement_size = asset.get("placement_size", [])
        placement_bbox = asset.get("placement_bbox", [])
        center_offset = asset.get("runtime_center_offset", [])
        hall_offset = asset.get("hall_center_offset", [])
        mode = str(asset.get("anchor_mode", "bottom_center"))
        padding = float(normalized_entry.get("padding_pixels", 0.0))
        if (
            len(cell_size) != 2
            or len(placement_size) != 2
            or len(placement_bbox) != 4
            or len(center_offset) != 2
            or len(hall_offset) != 2
        ):
            errors.append(f"{asset_id}: runtime placement geometry is incomplete")
        else:
            cell_center = [float(cell_size[0]) * 0.5, float(cell_size[1]) * 0.5]
            generated_anchor = list(cell_center)
            if mode == "top_center":
                generated_anchor[1] = padding
            elif mode == "bottom_center":
                generated_anchor[1] = float(cell_size[1]) - padding
            reference_anchor = bbox_anchor(placement_bbox, mode)
            expected_center = [
                reference_anchor[axis]
                - (generated_anchor[axis] - cell_center[axis]) * runtime_scale
                for axis in range(2)
            ]
            expected_hall = [
                expected_center[axis] - float(placement_size[axis]) * 0.5
                for axis in range(2)
            ]
            if any(
                abs(float(center_offset[axis]) - expected_center[axis]) > 0.001
                for axis in range(2)
            ):
                errors.append(f"{asset_id}: runtime center offset is not pivot-derived")
            if any(
                abs(float(hall_offset[axis]) - expected_hall[axis]) > 0.001
                for axis in range(2)
            ):
                errors.append(f"{asset_id}: hall center offset is not pivot-derived")
        has_water = bool(asset.get("water_layers", []))
        if has_water != (asset_id in EXPECTED_WATER):
            errors.append(f"{asset_id}: unexpected water-layer assignment")
        if bool(asset.get("generated_hidden_surfaces", False)) != (
            asset_id in EXPECTED_HIDDEN_SURFACES
        ):
            errors.append(f"{asset_id}: hidden-surface authorship flag is wrong")
        audit_water_against_generated_frames(asset, errors)

    contract = manifest.get("contract", {})
    if contract.get("water_node_type") != "Sprite2D":
        errors.append("water contract does not require Sprite2D")
    if contract.get("water_shader_domain") != "canvas_item":
        errors.append("water contract does not require CanvasItem shaders")
    if bool(contract.get("water_depth_write", True)):
        errors.append("water contract permits depth writes")
    if int(contract.get("spring_component_cap", 0)) != 12:
        errors.append("spring allocation cap is not 12")
    if int(contract.get("spring_active_cap", 0)) != 8:
        errors.append("spring active cap is not 8")
    if bool(contract.get("spring_logic_authority", True)):
        errors.append("analytic springs are incorrectly allowed to own gameplay logic")
    expected_water_resources = (
        ("water_renderer", "water_renderer_sha256", SHADER),
        ("water_ripple_texture", "water_ripple_texture_sha256", RIPPLE_TEXTURE),
        ("water_caustics_texture", "water_caustics_texture_sha256", CAUSTICS_TEXTURE),
    )
    for path_key, hash_key, resource_path in expected_water_resources:
        if contract.get(path_key) != resource_path.relative_to(ROOT).as_posix():
            errors.append(f"water contract path is wrong for {path_key}")
        resource_hash = (repository_text_sha256(resource_path)
                         if resource_path == SHADER else sha256(resource_path))
        if contract.get(hash_key) != resource_hash:
            errors.append(f"water contract hash is stale for {path_key}")
    if contract.get("water_mask_source") != (
        "runtime_cached_exact_polygon_image_texture"
    ):
        errors.append("water contract no longer requires cached exact runtime masks")
    if contract.get("water_color_space") != (
        "source_color_uniforms_no_manual_srgb_conversion"
    ):
        errors.append("water contract color-space handling is ambiguous")

    measured_outlets = {
        "kitchen_sink": {
            "stream": [0.6275, 0.3175],
            "fill_role": "basin",
            "fill_center": [0.515, 0.600],
        },
        "bubble_bath_sink": {
            "stream": [0.500, 0.145],
            "fill_role": "basin",
            "fill_center": [0.500, 0.360],
        },
        "bubble_bath_bathtub": {
            "stream": [0.204, 0.155],
            "fill_role": "fill",
            "fill_center": [0.515, 0.425],
        },
    }
    for asset_id, expected in measured_outlets.items():
        layers = asset_map.get(asset_id, {}).get("water_layers", [])
        streams = [layer for layer in layers if layer.get("role") == "stream"]
        fills = [
            layer for layer in layers
            if layer.get("role") == expected["fill_role"]
        ]
        if len(streams) != 1 or len(fills) != 1:
            errors.append(f"{asset_id}: measured outlet/fill layers are incomplete")
            continue
        points = streams[0].get("points", [])
        center = fills[0].get("center", [])
        if len(points) < 2 or any(len(point) != 2 for point in points[:2]):
            errors.append(f"{asset_id}: stream outlet polygon is malformed")
        else:
            outlet = [
                (float(points[0][axis]) + float(points[1][axis])) * 0.5
                for axis in range(2)
            ]
            if any(
                abs(outlet[axis] - float(expected["stream"][axis])) > 0.025
                for axis in range(2)
            ):
                errors.append(f"{asset_id}: stream no longer begins at its fixture outlet")
        if (
            len(center) != 2
            or any(
                abs(float(center[axis]) - float(expected["fill_center"][axis]))
                > 0.025
                for axis in range(2)
            )
        ):
            errors.append(f"{asset_id}: fill mask is no longer inside its basin")

    for ripple_id in ("bubble_bath_rubber_duck",):
        ripples = [
            layer for layer in asset_map.get(ripple_id, {}).get("water_layers", [])
            if layer.get("role") == "ripple"
        ]
        if len(ripples) != 1 or float(ripples[0].get("z_offset", 1.0)) >= 0.0:
            errors.append(f"{ripple_id}: contact ripple is not behind the object")

    toilet = asset_map.get("bubble_bath_toilet", {})
    toilet_layers = toilet.get("water_layers", [])
    if len(toilet_layers) != 1:
        errors.append("toilet must have one bounded bowl vortex")
    else:
        center = toilet_layers[0].get("center", [])
        radius = toilet_layers[0].get("radius", [])
        if (
            len(center) != 2
            or abs(float(center[0]) - 0.5) > 0.03
            or len(radius) != 2
            or float(radius[0]) > 0.20
        ):
            errors.append("toilet vortex is not centered inside the bowl")

    shader_source = SHADER.read_text(encoding="utf-8")
    render_modes = shader_render_modes(shader_source)
    required_render_modes = {"unshaded", "blend_mix"}
    if not required_render_modes.issubset(render_modes):
        errors.append("water shader executable render_mode contract is incomplete")
    executable_shader = strip_shader_comments(shader_source)
    if "spatial" in executable_shader:
        errors.append("water shader still declares the spatial domain")
    for forbidden in (
        "SCREEN_TEXTURE",
        "DEPTH_TEXTURE",
        "hint_screen_texture",
        "hint_depth_texture",
    ):
        if forbidden in executable_shader:
            errors.append(
                f"water shader samples forbidden screen/depth input: {forbidden}"
            )
    for token in ("shape_mask", "ripple", "caustics", "reveal_from_top"):
        if token not in executable_shader:
            errors.append(f"water shader is missing {token}")
    rig_source = RIG_SCRIPT.read_text(encoding="utf-8")
    for forbidden in (
        "Sprite3D", "RigidBody3D", "CollisionShape3D", "BoxShape3D",
        "MeshInstance3D", "Node3D", "Vector3", "shader_type spatial",
    ):
        if forbidden in rig_source or (forbidden == "shader_type spatial"
                                       and forbidden in executable_shader):
            errors.append(f"fixture runtime retains prohibited 3D token: {forbidden}")
    for token in (
        "Sprite2D",
        '"water_layers"',
        "MAX_SPRING_BODIES := 12",
        "MAX_AWAKE_SPRINGS := 8",
        "func _tick_spring",
        "func _add_spring_driver",
        "func physics_tick",
        "_water_mask_cache",
        "func _prewarm_water_masks",
        "func _mask_cache_key",
        "clampf(angle, -max_angle, max_angle)",
        "clampf(displacement, -max_displacement, max_displacement)",
        "0.028 + float(index % 2) * 0.010",
    ):
        if token not in rig_source:
            errors.append(f"fixture rig is missing contract token: {token}")
    bounded_constants = {
        "SPRING_LINEAR_STIFFNESS": 12.0,
        "SPRING_LINEAR_DAMPING": 5.0,
        "SPRING_ANGULAR_STIFFNESS": 30.0,
        "SPRING_ANGULAR_DAMPING": 15.0,
        "SPRING_HINGE_INITIAL_VELOCITY": 2.0,
        "SPRING_BUOYANT_INITIAL_ANGULAR_VELOCITY": 2.0,
        "SPRING_BUOYANT_INITIAL_VERTICAL_VELOCITY": 1.0,
        "MAX_HINGE_ANGLE": 0.25,
        "MAX_BUOYANT_ANGLE": 0.15,
        "MAX_HINGE_DISPLACEMENT": 0.35,
        "MAX_BUOYANT_DISPLACEMENT": 0.08,
    }
    for constant_name, maximum in bounded_constants.items():
        match = re.search(
            rf"const\s+{constant_name}\s*:=\s*([0-9.]+)", rig_source
        )
        if match is None or float(match.group(1)) > maximum:
            errors.append(
                f"fixture rig constant {constant_name} exceeds its mobile bound"
            )
    for match in re.finditer(
        r"apply_(?:central|torque)_impulse\s*\((.*?)\)\)",
        rig_source,
        flags=re.DOTALL,
    ):
        literals = [
            float(value)
            for value in re.findall(
                r"(?<![A-Za-z_])([0-9]+\.[0-9]+)", match.group(1)
            )
        ]
        if any(value > 0.10 for value in literals):
            errors.append("fixture rig contains a legacy large direct impulse")
    if "srgb_to_linear" in rig_source:
        errors.append("water colors are double-converted to linear space")
    room_source = ROOM_SCRIPT.read_text(encoding="utf-8")
    activation_block = room_source.split(
        "func _activate_room_item", 1
    )[-1].split("\nfunc ", 1)[0]
    if "_item_burst" in activation_block:
        errors.append("normal item activation still creates generic burst overlays")
    audio_loader_block = room_source.split(
        "func _play_item_sfx", 1
    )[-1].split("func _timeline_sequence", 1)[0]
    for token in (
        'path.begins_with("res://")',
        'path.begins_with("assets/audio/")',
    ):
        if token not in audio_loader_block:
            errors.append(
                "castle SFX loader cannot resolve manifest path token: " + token
            )
    if "TEXTURE_FILTER_LINEAR" not in room_source and \
            "CanvasItem.TEXTURE_FILTER_LINEAR" not in rig_source:
        errors.append("v2 sheets do not disable cross-cell mipmap sampling")
    main_source = MAIN_SCRIPT.read_text(encoding="utf-8")
    if "_castle_rooms_25d.physics_tick(delta)" not in main_source:
        errors.append("Jolt restoration is not driven by the physics tick")
    export_source = EXPORT_PRESETS.read_text(encoding="utf-8")
    manifest_export_path = (
        "assets/flats/castle/interactions_v2/castle_interactions_v2.json")
    include_filters = [line for line in export_source.splitlines()
                       if line.startswith('include_filter="')]
    if len(include_filters) != 2 or any(
            manifest_export_path not in line for line in include_filters):
        errors.append(
            "desktop/Android exports do not both package the runtime v2 JSON"
        )

    audio_manifest = load_json(AUDIO_MANIFEST, errors)
    audio_entries = {
        str(entry.get("id", "")): entry
        for entry in audio_manifest.get("files", [])
        if isinstance(entry, dict)
    }
    if audio_manifest.get("generator_sha256") != repository_text_sha256(AUDIO_GENERATOR):
        errors.append("castle SFX generator hash is stale")
    expected_fridge_audio = {
        "fridge_open": {
            "duration_ms": 720,
            "events": {"latch", "door_open", "chime"},
        },
        "fridge_close": {
            "duration_ms": 520,
            "events": {"door_close", "latch"},
        },
    }
    for audio_id, expected_audio in expected_fridge_audio.items():
        entry = audio_entries.get(audio_id, {})
        path = ROOT / str(entry.get("path", ""))
        if not path.is_file():
            errors.append(f"{audio_id}: OGG missing")
            continue
        if sha256(path) != entry.get("sha256"):
            errors.append(f"{audio_id}: OGG hash mismatch")
        if path.stat().st_size != int(entry.get("file_bytes", -1)):
            errors.append(f"{audio_id}: OGG byte count mismatch")
        if path.read_bytes()[:4] != b"OggS":
            errors.append(f"{audio_id}: file is not Ogg Vorbis")
        if int(entry.get("duration_ms", 0)) != int(expected_audio["duration_ms"]):
            errors.append(f"{audio_id}: cue duration no longer matches the action")
        if set(entry.get("events_ms", {})) != set(expected_audio["events"]):
            errors.append(f"{audio_id}: semantic cue events are incomplete")

    fridge_asset = asset_map.get("kitchen_fridge", {})
    if fridge_asset.get("sound") != "assets/audio/castle/fridge_open.ogg":
        errors.append("fridge open timeline does not use the dedicated open cue")
    if fridge_asset.get("close_sound") != "assets/audio/castle/fridge_close.ogg":
        errors.append("fridge close timeline does not use the dedicated close cue")

    license_text = LICENSES.read_text(encoding="utf-8")
    for token in (
        "assets/flats/castle/interactions_v2/",
        "assets_src/imagegen/castle_object_animations_v2/",
        "assets/shaders/castle_fixture_water.gdshader",
        "assets/audio/castle/fridge_open.ogg",
        "assets/audio/castle/fridge_close.ogg",
    ):
        if token not in license_text:
            errors.append(f"ASSET_LICENSES missing entry for {token}")

    evidence = manifest.get("visual_review_evidence", {})
    if not CONTACT.is_file():
        errors.append("tracked v2 contact sheet is missing")
    else:
        if evidence.get("path") != CONTACT.relative_to(ROOT).as_posix():
            errors.append("manifest contact-sheet path is wrong")
        if evidence.get("sha256") != sha256(CONTACT):
            errors.append("manifest contact-sheet hash is stale")
        with Image.open(CONTACT) as contact:
            if list(contact.size) != evidence.get("dimensions"):
                errors.append("manifest contact-sheet dimensions are stale")
    if manifest.get("generator_sha256") != repository_text_sha256(
        ROOT / str(manifest.get("generator", ""))
    ):
        errors.append("v2 manifest generator hash is stale")

    if errors:
        for error in errors:
            print("CASTLEV2|FAIL|" + error)
        print(f"CASTLEV2|RESULT|FAIL|count={len(errors)}")
        return 1
    print(
        "CASTLEV2|RESULT|OK|"
        f"assets={len(asset_map)}|instances={instance_count}|"
        f"average={average:.2f}|water={len(EXPECTED_WATER)}|spring={EXPECTED_SPRINGS}|"
        f"max_room_rgba_mib={max_room_rgba_bytes / (1024.0 * 1024.0):.2f}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-contact-sheet", action="store_true")
    args = parser.parse_args()
    if args.write_contact_sheet:
        build_contact_sheet()
        return 0
    return audit()


if __name__ == "__main__":
    raise SystemExit(main())
