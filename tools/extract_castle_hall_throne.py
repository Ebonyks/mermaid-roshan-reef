#!/usr/bin/env python3
"""Extract the approved Main Hall shell throne as a transparent runtime card.

The source is the prior approved high-resolution Screen-B painting. This tool
only crops existing RGB pixels and authors an alpha silhouette around the
already-painted throne; it does not repaint, upscale, interpolate RGB, or add
new visual content. The manifest records the exact source rectangle, mask,
dimensions, and hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


SOURCE_RECT = (1790, 355, 1975, 540)
MASK_SCALE = 4


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _scaled_box(box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(value * MASK_SCALE for value in box)


def _scaled_points(
    points: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    return [(x * MASK_SCALE, y * MASK_SCALE) for x, y in points]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    arguments = parser.parse_args()

    with Image.open(arguments.source) as opened:
        source = opened.convert("RGB")
    if source.size != (2048, 1153):
        raise ValueError(
            "Expected approved Screen-B master at 2048x1153; "
            f"got {source.width}x{source.height}: {arguments.source}")

    crop = source.crop(SOURCE_RECT)
    mask = Image.new(
        "L", (crop.width * MASK_SCALE, crop.height * MASK_SCALE), 0)
    draw = ImageDraw.Draw(mask)
    # Keep the recognizable shell seat, finial, pearl standards, and platform;
    # deliberately exclude the old alcove, rainbow arch, wall, and staircase.
    # This prevents the retained object from reading as a rectangular inset.
    draw.polygon(_scaled_points([
        (88, 25), (108, 33), (121, 46), (136, 57),
        (149, 89), (141, 116), (121, 139), (62, 139),
        (42, 120), (32, 95), (39, 65), (55, 50), (73, 38),
    ]), fill=255)
    draw.polygon(_scaled_points([
        (79, 0), (105, 0), (111, 27), (105, 38),
        (79, 38), (73, 27),
    ]), fill=255)
    draw.polygon(_scaled_points([
        (23, 104), (44, 104), (49, 166), (18, 166),
    ]), fill=255)
    draw.polygon(_scaled_points([
        (144, 104), (163, 104), (165, 166), (140, 166),
    ]), fill=255)
    # Preserve the chair's lower pearl platform without the painted stair.
    draw.rounded_rectangle(
        _scaled_box((16, 133, 165, 184)),
        radius=7 * MASK_SCALE,
        fill=255,
    )
    mask = mask.resize(crop.size, Image.Resampling.LANCZOS)
    # Remove the old dark chair-back/alcove pixels from inside the audited
    # silhouette while preserving the dark painted outlines touching the
    # bright shell, pearl, and gold object. A small max filter expands only
    # from existing bright source pixels; it never alters RGB.
    bright_source = crop.convert("L").point(
        lambda value: 255 if value >= 100 else 0)
    bright_with_outlines = bright_source.filter(ImageFilter.MaxFilter(5))
    mask = ImageChops.multiply(mask, bright_with_outlines)

    result = crop.convert("RGBA")
    result.putalpha(mask)
    alpha_bbox = mask.getbbox()
    if alpha_bbox is None:
        raise RuntimeError("Throne mask is empty")

    # RGB invariance is blocking: alpha is the only authored channel.
    if ImageChops.difference(result.convert("RGB"), crop).getbbox() is not None:
        raise RuntimeError("Throne extraction changed approved RGB pixels")

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(arguments.output, format="PNG", optimize=True)
    manifest = {
        "schema": 1,
        "purpose": "Pixel-preserving approved shell-throne Sprite3D cutout",
        "source": {
            "path": arguments.source.as_posix(),
            "dimensions": list(source.size),
            "sha256": _sha256(arguments.source),
        },
        "source_rectangle": list(SOURCE_RECT),
        "output": {
            "path": arguments.output.as_posix(),
            "dimensions": list(result.size),
            "sha256": _sha256(arguments.output),
            "alpha_bbox": list(alpha_bbox),
            "long_edge_within_1024_limit": max(result.size) <= 1024,
        },
        "rgb_pixel_invariance": True,
        "upscaled": False,
        "generated_rgb_pixels": False,
        "mask": {
            "method": "manually audited antialiased silhouette",
            "supersample": MASK_SCALE,
            "source_authority": "approved Screen-B throne silhouette only",
        },
    }
    arguments.manifest.parent.mkdir(parents=True, exist_ok=True)
    arguments.manifest.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
