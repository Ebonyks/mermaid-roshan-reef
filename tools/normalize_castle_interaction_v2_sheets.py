#!/usr/bin/env python3
"""Register and pad generated Pearl Castle object-state sheets.

ImageGen sometimes lays out its second conceptual row at a different local
origin. Runtime Sprite3D playback cannot compensate per frame, so this tool
moves each complete generated state onto one audited fixed pivot. It applies a
single whole-sheet scale only when required for transparent cell padding; it
never warps, repaints, or synthesizes an action state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SHEET_DIR = ROOT / "assets/flats/castle/interactions_v2"
REPORT_PATH = SHEET_DIR / "castle_interactions_v2_normalization.json"
PADDING = 6
ALPHA_THRESHOLD = 16

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
EXPECTED_COUNT = 33


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("empty animation frame")
    return bbox


def anchor_point(
    image: Image.Image,
    bbox: tuple[int, int, int, int],
    mode: str,
) -> tuple[float, float]:
    left, top, right, bottom = bbox
    if mode == "center":
        return ((left + right) * 0.5, (top + bottom) * 0.5)
    height = bottom - top
    band_height = max(5, int(round(height * 0.12)))
    band_top = top if mode == "top_center" else max(top, bottom - band_height)
    band_bottom = min(bottom, top + band_height) if mode == "top_center" else bottom
    band = image.getchannel("A").crop((0, band_top, image.width, band_bottom))
    band_mask = band.point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
    band_bbox = band_mask.getbbox()
    anchor_x = (left + right) * 0.5
    if band_bbox is not None:
        anchor_x = (band_bbox[0] + band_bbox[2]) * 0.5
    anchor_y = float(top if mode == "top_center" else bottom)
    return (anchor_x, anchor_y)


def cell_frames(sheet: Image.Image) -> tuple[list[Image.Image], int, int]:
    if sheet.width % 4 or sheet.height % 2:
        raise ValueError("sheet is not an exact 4x2 grid")
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


def recover_interior_alpha(frame: Image.Image) -> tuple[Image.Image, int]:
    """Recover subject opacity and discard only low-alpha exact chroma spill."""
    alpha = frame.getchannel("A")
    visible = alpha.point(lambda value: 255 if value >= 8 else 0)
    interior = visible.filter(ImageFilter.MinFilter(5))
    boosted = alpha.point(lambda value: min(255, int(round(value * 1.35))))
    recovered = Image.composite(
        Image.new("L", frame.size, 255),
        boosted,
        interior,
    )
    recovered_values = list(recovered.get_flattened_data())
    removed_spill = 0
    for index, (red, green, blue, source_alpha) in enumerate(
        frame.get_flattened_data()
    ):
        if (
            source_alpha < 128
            and red >= 248
            and blue >= 248
            and green <= 12
        ):
            if recovered_values[index] > 0:
                removed_spill += 1
            recovered_values[index] = 0
    recovered.putdata(recovered_values)
    result = frame.copy()
    result.putalpha(recovered)
    return result, removed_spill


def component_sizes(mask: Image.Image) -> list[int]:
    """Return 4-connected component sizes for a binary L-mode image."""
    width, height = mask.size
    pixels = mask.tobytes()
    seen = bytearray(width * height)
    sizes: list[int] = []
    for seed, value in enumerate(pixels):
        if value == 0 or seen[seed]:
            continue
        seen[seed] = 1
        stack = [seed]
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            x = current % width
            if x > 0:
                neighbor = current - 1
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if x + 1 < width:
                neighbor = current + 1
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if current >= width:
                neighbor = current - width
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if current + width < width * height:
                neighbor = current + width
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def remove_tiny_alpha_islands(
    frame: Image.Image,
    minimum_pixels: int = 8,
) -> tuple[Image.Image, int]:
    alpha_values = list(frame.getchannel("A").get_flattened_data())
    width, height = frame.size
    visible = bytearray(
        1 if value >= ALPHA_THRESHOLD else 0 for value in alpha_values
    )
    seen = bytearray(width * height)
    removed = 0
    for seed, value in enumerate(visible):
        if value == 0 or seen[seed]:
            continue
        seen[seed] = 1
        stack = [seed]
        component: list[int] = []
        while stack:
            current = stack.pop()
            component.append(current)
            x = current % width
            if x > 0:
                neighbor = current - 1
                if visible[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if x + 1 < width:
                neighbor = current + 1
                if visible[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if current >= width:
                neighbor = current - width
                if visible[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if current + width < width * height:
                neighbor = current + width
                if visible[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
        if len(component) < minimum_pixels:
            for index in component:
                alpha_values[index] = 0
            removed += len(component)
    result = frame.copy()
    result.getchannel("A")
    cleaned_alpha = Image.new("L", frame.size)
    cleaned_alpha.putdata(alpha_values)
    result.putalpha(cleaned_alpha)
    return result, removed


def enclosed_hole_count(
    frame: Image.Image,
    bbox: tuple[int, int, int, int],
) -> int:
    alpha = frame.getchannel("A").crop(bbox)
    transparent = alpha.point(
        lambda value: 255 if value < ALPHA_THRESHOLD else 0
    )
    width, height = transparent.size
    pixels = transparent.tobytes()
    seen = bytearray(width * height)
    holes = 0
    for seed, value in enumerate(pixels):
        if value == 0 or seen[seed]:
            continue
        seen[seed] = 1
        stack = [seed]
        touches_edge = False
        while stack:
            current = stack.pop()
            x = current % width
            y = current // width
            touches_edge = (
                touches_edge
                or x == 0
                or y == 0
                or x + 1 == width
                or y + 1 == height
            )
            if x > 0:
                neighbor = current - 1
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if x + 1 < width:
                neighbor = current + 1
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if y > 0:
                neighbor = current - width
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
            if y + 1 < height:
                neighbor = current + width
                if pixels[neighbor] and not seen[neighbor]:
                    seen[neighbor] = 1
                    stack.append(neighbor)
        if not touches_edge:
            holes += 1
    return holes


def frame_alpha_qa(frame: Image.Image) -> dict[str, Any]:
    bbox = alpha_bbox(frame)
    alpha = frame.getchannel("A")
    binary = alpha.point(
        lambda value: 255 if value >= ALPHA_THRESHOLD else 0
    )
    sizes = component_sizes(binary)
    visible_pixels = sum(sizes)
    exact_chroma = 0
    near_chroma = 0
    for red, green, blue, alpha_value in frame.get_flattened_data():
        if alpha_value < 128:
            continue
        if red >= 248 and blue >= 248 and green <= 12:
            exact_chroma += 1
        if red >= 220 and blue >= 220 and green <= 55:
            near_chroma += 1
    border = (
        list(alpha.crop((0, 0, frame.width, 1)).get_flattened_data())
        + list(alpha.crop(
            (0, frame.height - 1, frame.width, frame.height)
        ).get_flattened_data())
        + list(alpha.crop((0, 0, 1, frame.height)).get_flattened_data())
        + list(alpha.crop(
            (frame.width - 1, 0, frame.width, frame.height)
        ).get_flattened_data())
    )
    return {
        "fixed_canvas_size": [frame.width, frame.height],
        "alpha_bbox": list(bbox),
        "visible_pixels": visible_pixels,
        "canvas_coverage_ratio": round(
            visible_pixels / float(frame.width * frame.height), 8
        ),
        "component_count": len(sizes),
        "component_sizes": sizes,
        "tiny_component_count": sum(size < 8 for size in sizes),
        "largest_component_ratio": round(
            (sizes[0] if sizes else 0) / float(max(1, visible_pixels)), 8
        ),
        "enclosed_transparent_hole_count": enclosed_hole_count(frame, bbox),
        "visible_exact_chroma_pixels": exact_chroma,
        "visible_near_chroma_pixels": near_chroma,
        "visible_near_chroma_ratio": round(
            near_chroma / float(max(1, visible_pixels)), 8
        ),
        "transparent_canvas_border": all(value == 0 for value in border),
    }


def pivot_for(
    frame: Image.Image,
    mode: str,
) -> tuple[tuple[int, int, int, int], tuple[float, float]]:
    bbox = alpha_bbox(frame)
    return bbox, anchor_point(frame, bbox, mode)


def normalize(path: Path, destination_path: Path) -> dict[str, Any]:
    before_hash = sha256(path)
    sheet = Image.open(path).convert("RGBA")
    frames, cell_width, cell_height = cell_frames(sheet)
    recovered = [recover_interior_alpha(frame) for frame in frames]
    cleaned = [remove_tiny_alpha_islands(value[0]) for value in recovered]
    frames = [value[0] for value in cleaned]
    removed_spill = sum(value[1] for value in recovered)
    removed_islands = sum(value[1] for value in cleaned)
    asset_id = path.stem.removesuffix("_sheet")
    mode = ANCHOR_MODE.get(asset_id, "bottom_center")
    measured = [pivot_for(frame, mode) for frame in frames]
    target_x = cell_width * 0.5
    if mode == "top_center":
        target_y = float(PADDING)
    elif mode == "bottom_center":
        target_y = float(cell_height - PADDING)
    else:
        target_y = cell_height * 0.5
    scale = 1.0
    for bbox, source_anchor in measured:
        left, top, right, bottom = bbox
        extents_and_space = (
            (source_anchor[0] - left, target_x - PADDING),
            (right - source_anchor[0], cell_width - PADDING - target_x),
            (source_anchor[1] - top, target_y - PADDING),
            (bottom - source_anchor[1], cell_height - PADDING - target_y),
        )
        for extent, available in extents_and_space:
            if extent > 0.0:
                scale = min(scale, max(0.01, available) / extent)
    scale = min(1.0, scale)
    output = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    for index, (frame, (bbox, source_anchor)) in enumerate(zip(frames, measured)):
        cropped = frame.crop(bbox)
        anchor_local = (
            (source_anchor[0] - bbox[0]) * scale,
            (source_anchor[1] - bbox[1]) * scale,
        )
        if scale < 0.999999:
            size = (
                max(1, int(round(cropped.width * scale))),
                max(1, int(round(cropped.height * scale))),
            )
            cropped = cropped.convert("RGBa").resize(
                size, Image.Resampling.LANCZOS
            ).convert("RGBA")
        destination = (
            int(round(target_x - anchor_local[0])),
            int(round(target_y - anchor_local[1])),
        )
        cell = Image.new("RGBA", (cell_width, cell_height), (0, 0, 0, 0))
        cell.alpha_composite(cropped, destination)
        cell, post_scale_removed = remove_tiny_alpha_islands(cell)
        removed_islands += post_scale_removed
        output.alpha_composite(
            cell,
            ((index % 4) * cell_width, (index // 4) * cell_height),
        )

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(destination_path, optimize=True, compress_level=9)
    normalized = Image.open(destination_path).convert("RGBA")
    normalized_frames, _width, _height = cell_frames(normalized)
    after_bboxes = [alpha_bbox(frame) for frame in normalized_frames]
    after_anchors = [
        anchor_point(frame, bbox, mode)
        for frame, bbox in zip(normalized_frames, after_bboxes)
    ]
    edge_gap = min(
        min(
            bbox[0],
            bbox[1],
            cell_width - bbox[2],
            cell_height - bbox[3],
        )
        for bbox in after_bboxes
    )
    x_values = [point[0] for point in after_anchors]
    y_values = [point[1] for point in after_anchors]
    return {
        "id": asset_id,
        "path": path.relative_to(ROOT).as_posix(),
        "input_sha256": before_hash,
        "runtime_sha256": sha256(destination_path),
        "grid": [4, 2],
        "cell_size": [cell_width, cell_height],
        "frame_count": 8,
        "anchor_mode": mode,
        "uniform_scale": round(scale, 8),
        "padding_pixels": PADDING,
        "edge_gap_pixels": edge_gap,
        "anchor_spread_pixels": [
            round(max(x_values) - min(x_values), 3),
            round(max(y_values) - min(y_values), 3),
        ],
        "frame_bboxes": [list(bbox) for bbox in after_bboxes],
        "unique_frame_count": len({
            hashlib.sha256(frame.tobytes()).hexdigest()
            for frame in normalized_frames
        }),
        "whole_object_translation_only": True,
        "whole_sheet_uniform_scale_only": True,
        "alpha_matte_recovered": True,
        "alpha_recovery": "5x5 interior opacity plus 1.35x soft-edge alpha",
        "low_alpha_exact_chroma_removed_pixels": removed_spill,
        "tiny_alpha_island_pixels_removed": removed_islands,
        "per_frame_alpha_qa": [
            frame_alpha_qa(frame) for frame in normalized_frames
        ],
        "fixed_canvas_review": True,
        "rgb_subject_repainted": False,
        "repainted_pixels": False,
    }


def validate_entry(
    entry: dict[str, Any],
    path_override: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    path = path_override or ROOT / str(entry["path"])
    if not path.is_file():
        return [f"{entry['id']}: runtime sheet missing"]
    if sha256(path) != entry.get("runtime_sha256"):
        errors.append(f"{entry['id']}: runtime hash differs from normalization report")
    if not bool(entry.get("alpha_matte_recovered", False)):
        errors.append(f"{entry['id']}: interior alpha recovery is not recorded")
    if bool(entry.get("rgb_subject_repainted", True)):
        errors.append(f"{entry['id']}: subject RGB was repainted")
    if not bool(entry.get("fixed_canvas_review", False)):
        errors.append(f"{entry['id']}: fixed-canvas alpha review is missing")
    sheet = Image.open(path).convert("RGBA")
    try:
        frames, cell_width, cell_height = cell_frames(sheet)
    except ValueError as exc:
        return [f"{entry['id']}: {exc}"]
    mode = str(entry.get("anchor_mode", "bottom_center"))
    boxes = [alpha_bbox(frame) for frame in frames]
    anchors = [
        anchor_point(frame, bbox, mode)
        for frame, bbox in zip(frames, boxes)
    ]
    edge_gap = min(
        min(bbox[0], bbox[1], cell_width - bbox[2], cell_height - bbox[3])
        for bbox in boxes
    )
    if edge_gap < PADDING - 2:
        errors.append(f"{entry['id']}: cell edge gap {edge_gap}px is unsafe")
    spread_x = max(point[0] for point in anchors) - min(point[0] for point in anchors)
    spread_y = max(point[1] for point in anchors) - min(point[1] for point in anchors)
    if spread_x > 2.0 or spread_y > 2.0:
        errors.append(
            f"{entry['id']}: pivot drift is {spread_x:.2f},{spread_y:.2f}px"
        )
    unique = len({
        hashlib.sha256(frame.tobytes()).hexdigest() for frame in frames
    })
    if unique < 4:
        errors.append(f"{entry['id']}: only {unique} visually unique frames")
    qa = entry.get("per_frame_alpha_qa", [])
    if not isinstance(qa, list) or len(qa) != 8:
        errors.append(f"{entry['id']}: per-frame alpha QA is incomplete")
    else:
        for index, (frame, recorded) in enumerate(zip(frames, qa)):
            measured = frame_alpha_qa(frame)
            if measured != recorded:
                errors.append(f"{entry['id']}: frame {index} alpha QA is stale")
                continue
            if not measured["transparent_canvas_border"]:
                errors.append(
                    f"{entry['id']}: frame {index} touches its canvas border"
                )
            if int(measured["visible_exact_chroma_pixels"]) != 0:
                errors.append(
                    f"{entry['id']}: frame {index} retains visible exact chroma"
                )
            if float(measured["visible_near_chroma_ratio"]) > 0.002:
                errors.append(
                    f"{entry['id']}: frame {index} has excessive near-chroma spill"
                )
            if int(measured["visible_pixels"]) < 100:
                errors.append(
                    f"{entry['id']}: frame {index} has no usable silhouette"
                )
            if int(measured["tiny_component_count"]) > 0:
                errors.append(
                    f"{entry['id']}: frame {index} has tiny alpha islands"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        if not REPORT_PATH.is_file():
            print("FAIL: normalization report is missing")
            return 1
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        entries = report.get("assets", [])
        errors: list[str] = []
        if report.get("tool_sha256") != sha256(Path(__file__)):
            errors.append("normalization tool hash differs from its report")
        if int(report.get("schema_version", 0)) != 2:
            errors.append("normalization report schema is not 2")
        if not bool(report.get("transactional", False)):
            errors.append("normalization report does not record a transaction")
        if not bool(report.get("one_time_guard", False)):
            errors.append("normalization report does not record rerun protection")
        if len(entries) != EXPECTED_COUNT:
            errors.append(
                f"normalization roster has {len(entries)} assets, expected {EXPECTED_COUNT}"
            )
        runtime = sorted(SHEET_DIR.glob("*_sheet.png"))
        if len(runtime) != EXPECTED_COUNT:
            errors.append(
                f"runtime sheet roster has {len(runtime)} assets, expected {EXPECTED_COUNT}"
            )
        for entry in entries:
            errors.extend(validate_entry(entry))
        if errors:
            for error in errors:
                print("FAIL: " + error)
            return 1
        print(
            f"CASTLEV2|NORMALIZATION_OK|assets={len(entries)}|"
            f"padding={PADDING}|unique_min=4|transactional=true"
        )
        return 0

    if REPORT_PATH.exists():
        print(
            "FAIL: normalization report already exists; refusing destructive rerun. "
            "Use --check to validate the accepted runtime sheets."
        )
        return 1
    paths = sorted(SHEET_DIR.glob("*_sheet.png"))
    if len(paths) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} generated sheets before normalization; "
            f"found {len(paths)}"
        )
    stage_root = Path(
        tempfile.mkdtemp(prefix=".castle_v2_normalize_", dir=SHEET_DIR)
    )
    normalized_dir = stage_root / "normalized"
    backup_dir = stage_root / "backup"
    entries: list[dict[str, Any]] = []
    committed: list[Path] = []
    try:
        staged_paths: dict[Path, Path] = {}
        for path in paths:
            staged = normalized_dir / path.name
            entry = normalize(path, staged)
            validation_errors = validate_entry(entry, staged)
            if validation_errors:
                raise ValueError("; ".join(validation_errors))
            entries.append(entry)
            staged_paths[path] = staged
        report = {
            "schema_version": 2,
            "generated_on": "2026-08-01",
            "tool": "tools/normalize_castle_interaction_v2_sheets.py",
            "tool_sha256": sha256(Path(__file__)),
            "method": "interior_alpha_recovery_then_fixed_pivot_translation_and_optional_uniform_scale",
            "transactional": True,
            "one_time_guard": True,
            "rgb_subject_repainted": False,
            "alpha_matte_recovered": True,
            "padding_pixels": PADDING,
            "assets": entries,
        }
        report_stage = stage_root / REPORT_PATH.name
        report_stage.write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        backup_dir.mkdir(parents=True, exist_ok=True)
        for path in paths:
            shutil.copy2(path, backup_dir / path.name)
        try:
            for path in paths:
                os.replace(staged_paths[path], path)
                committed.append(path)
            os.replace(report_stage, REPORT_PATH)
        except Exception:
            if REPORT_PATH.exists():
                REPORT_PATH.unlink()
            for path in committed:
                shutil.copy2(backup_dir / path.name, path)
            raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)
    for entry in entries:
        print(
            f"NORMALIZED|{entry['id']}|scale={entry['uniform_scale']}|"
            f"edge={entry['edge_gap_pixels']}|drift={entry['anchor_spread_pixels']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
