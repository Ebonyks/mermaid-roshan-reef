#!/usr/bin/env python3
"""Audit rendered Main Hall bloom and tile joins from Godot screenshots.

The source-tile pipeline already proves pixel-exact reconstruction. This gate
adds the missing renderer-level evidence: the same left-hand camera with the
shell lights on/off must show localized positive bloom, and the central
two-screen join plus horizontal card join must not reveal a dark raster gap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_rgb(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        return opened.convert("RGB")


def _luma(array: np.ndarray) -> np.ndarray:
    return (
        array[..., 0] * 0.2126
        + array[..., 1] * 0.7152
        + array[..., 2] * 0.0722
    )


def _edge_metrics(array: np.ndarray, orientation: str, coordinate: int) -> dict[str, float]:
    if orientation == "vertical":
        left = array[:, coordinate - 1, :]
        right = array[:, coordinate, :]
        edge = np.abs(left - right)
        offsets = (-10, -8, -6, 6, 8, 10)
        neighbors = [
            np.abs(array[:, coordinate + offset - 1, :] - array[:, coordinate + offset, :])
            for offset in offsets
        ]
        seam_luma = _luma(array[:, coordinate, :]).mean()
        neighbor_luma = 0.5 * (
            _luma(array[:, coordinate - 2, :]).mean()
            + _luma(array[:, coordinate + 1, :]).mean()
        )
    else:
        upper = array[coordinate - 1, :, :]
        lower = array[coordinate, :, :]
        edge = np.abs(upper - lower)
        offsets = (-10, -8, -6, 6, 8, 10)
        neighbors = [
            np.abs(array[coordinate + offset - 1, :, :] - array[coordinate + offset, :, :])
            for offset in offsets
        ]
        seam_luma = _luma(array[coordinate, :, :]).mean()
        neighbor_luma = 0.5 * (
            _luma(array[coordinate - 2, :, :]).mean()
            + _luma(array[coordinate + 1, :, :]).mean()
        )
    local_baseline = float(np.mean([neighbor.mean() for neighbor in neighbors]))
    edge_mean = float(edge.mean())
    gap_ratio = float(seam_luma / max(neighbor_luma, 0.001))
    return {
        "edge_mean_abs_rgb": round(edge_mean, 4),
        "edge_p95_abs_rgb": round(float(np.percentile(edge, 95)), 4),
        "local_baseline_mean_abs_rgb": round(local_baseline, 4),
        "edge_to_local_ratio": round(edge_mean / max(local_baseline, 0.001), 4),
        "seam_to_neighbor_luma_ratio": round(gap_ratio, 4),
    }


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    font_path = Path(
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    )
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size)
    return ImageFont.load_default()


def _write_proof(
    lights_on: Image.Image,
    lights_off: Image.Image,
    seam: Image.Image,
    output: Path,
) -> None:
    preview_size = (640, 360)
    on_preview = lights_on.resize(preview_size, Image.Resampling.LANCZOS)
    off_preview = lights_off.resize(preview_size, Image.Resampling.LANCZOS)
    difference = ImageChops.difference(lights_on, lights_off)
    difference = difference.point(lambda value: min(255, value * 4))
    diff_preview = difference.resize(preview_size, Image.Resampling.LANCZOS)
    seam_width = seam.width
    seam_crop = seam.crop(
        (max(0, seam_width // 2 - 96), 0, min(seam_width, seam_width // 2 + 96), seam.height)
    )
    seam_preview = seam_crop.resize(preview_size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1280, 800), "#f4f1ff")
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (18, 12),
        "CASTLE MAIN HALL — MOBILE RENDER BLOOM / SEAM PROOF",
        font=_font(22, bold=True),
        fill="#302a68",
    )
    panels = (
        ("lights on", on_preview, (0, 52)),
        ("lights off", off_preview, (640, 52)),
        ("absolute difference ×4", diff_preview, (0, 430)),
        ("central A/B join", seam_preview, (640, 430)),
    )
    for label, panel, position in panels:
        canvas.paste(panel, position)
        draw.rectangle(
            (position[0], position[1], position[0] + 639, position[1] + 359),
            outline="#6659a8",
            width=2,
        )
        draw.text(
            (position[0] + 12, position[1] + 10),
            label,
            font=_font(17, bold=True),
            fill="#302a68",
            stroke_width=2,
            stroke_fill="#ffffff",
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lights-on", required=True, type=Path)
    parser.add_argument("--lights-off", required=True, type=Path)
    parser.add_argument("--seam", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--proof", required=True, type=Path)
    args = parser.parse_args()

    lights_on = _load_rgb(args.lights_on)
    lights_off = _load_rgb(args.lights_off)
    seam = _load_rgb(args.seam)
    if lights_on.size != lights_off.size:
        raise ValueError(
            f"Light captures differ in size: {lights_on.size} vs {lights_off.size}"
        )

    on_array = np.asarray(lights_on, dtype=np.float32)
    off_array = np.asarray(lights_off, dtype=np.float32)
    height, width = on_array.shape[:2]
    # Keep the architecture/light band, excluding the moving character and
    # bottom interactions. Side UI circles are also outside this center mask.
    x0, x1 = int(width * 0.13), int(width * 0.87)
    y0, y1 = int(height * 0.07), int(height * 0.58)
    on_region = on_array[y0:y1, x0:x1, :]
    off_region = off_array[y0:y1, x0:x1, :]
    on_luma = _luma(on_region)
    off_luma = _luma(off_region)
    positive = on_luma - off_luma
    absolute_rgb = np.abs(on_region - off_region)
    # A bloom halo is positive light away from clipped-white cores.
    halo_mask = (
        (positive > 4.0)
        & (on_luma < 245.0)
        & (off_luma < 245.0)
    )
    full_positive = _luma(on_array) - _luma(off_array)
    yy, xx = np.ogrid[:height, :width]
    fixture_mask = np.zeros((height, width), dtype=bool)
    # First two Screen-A fixtures are unobscured by HUD circles. Their authored
    # positions are mapped from the exact 1672x941 logical play screen.
    for art_x in (290.0, 790.0):
        center_x = art_x / 1672.0 * width
        center_y = 215.0 / 941.0 * height
        radius = height * 0.105
        fixture_mask |= (xx - center_x) ** 2 + (yy - center_y) ** 2 <= radius ** 2
    architecture_mask = np.zeros((height, width), dtype=bool)
    architecture_mask[y0:y1, x0:x1] = True
    far_field_mask = architecture_mask & ~fixture_mask
    fixture_gain = float(np.maximum(full_positive[fixture_mask], 0.0).mean())
    far_field_gain = float(np.maximum(full_positive[far_field_mask], 0.0).mean())
    bloom_metrics = {
        "on_mean_luma": round(float(on_luma.mean()), 4),
        "off_mean_luma": round(float(off_luma.mean()), 4),
        "mean_positive_luma_delta": round(float(np.maximum(positive, 0.0).mean()), 4),
        "positive_luma_p95": round(float(np.percentile(np.maximum(positive, 0.0), 95)), 4),
        "changed_pixel_fraction_over_3_rgb": round(
            float(np.mean(np.max(absolute_rgb, axis=2) > 3.0)), 6
        ),
        "unsaturated_halo_fraction": round(float(halo_mask.mean()), 6),
        "unsaturated_halo_mean_delta": round(
            float(positive[halo_mask].mean()) if np.any(halo_mask) else 0.0,
            4,
        ),
        "fixture_region_positive_mean_delta": round(fixture_gain, 4),
        "far_field_positive_mean_delta": round(far_field_gain, 4),
        "localized_fixture_gain_ratio": round(
            fixture_gain / max(far_field_gain, 0.001), 4
        ),
    }
    bloom_pass = (
        bloom_metrics["on_mean_luma"] > bloom_metrics["off_mean_luma"] + 0.25
        and bloom_metrics["mean_positive_luma_delta"] >= 0.6
        and bloom_metrics["positive_luma_p95"] >= 3.0
        and bloom_metrics["changed_pixel_fraction_over_3_rgb"] >= 0.01
        and bloom_metrics["unsaturated_halo_fraction"] >= 0.002
        and bloom_metrics["unsaturated_halo_mean_delta"] >= 4.0
        and bloom_metrics["mean_positive_luma_delta"] <= 35.0
        and bloom_metrics["positive_luma_p95"] <= 70.0
        and bloom_metrics["fixture_region_positive_mean_delta"]
            >= bloom_metrics["far_field_positive_mean_delta"] + 3.0
        and bloom_metrics["localized_fixture_gain_ratio"] >= 1.15
    )

    seam_array = np.asarray(seam, dtype=np.float32)
    seam_height, seam_width = seam_array.shape[:2]
    vertical = _edge_metrics(seam_array, "vertical", seam_width // 2)
    horizontal = _edge_metrics(seam_array, "horizontal", seam_height // 2)
    vertical_pass = (
        vertical["edge_mean_abs_rgb"] <= max(
            35.0, vertical["local_baseline_mean_abs_rgb"] * 5.0 + 5.0
        )
        and vertical["seam_to_neighbor_luma_ratio"] >= 0.72
    )
    horizontal_pass = (
        horizontal["edge_mean_abs_rgb"] <= max(
            30.0, horizontal["local_baseline_mean_abs_rgb"] * 5.0 + 5.0
        )
        and horizontal["seam_to_neighbor_luma_ratio"] >= 0.72
    )
    blocking_pass = bloom_pass and vertical_pass and horizontal_pass
    result = {
        "schema": 1,
        "purpose": "Godot Mobile-rendered Main Hall bloom and tile-join gate",
        "inputs": {
            "lights_on": {
                "path": args.lights_on.as_posix(),
                "dimensions": list(lights_on.size),
                "sha256": _sha256(args.lights_on),
            },
            "lights_off": {
                "path": args.lights_off.as_posix(),
                "dimensions": list(lights_off.size),
                "sha256": _sha256(args.lights_off),
            },
            "seam": {
                "path": args.seam.as_posix(),
                "dimensions": list(seam.size),
                "sha256": _sha256(args.seam),
            },
        },
        "bloom": {**bloom_metrics, "pass": bloom_pass},
        "rendered_seams": {
            "central_screen_join": {**vertical, "pass": vertical_pass},
            "horizontal_tile_join": {**horizontal, "pass": horizontal_pass},
        },
        "blocking_pass": blocking_pass,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    _write_proof(lights_on, lights_off, seam, args.proof)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if blocking_pass else 1)


if __name__ == "__main__":
    main()
