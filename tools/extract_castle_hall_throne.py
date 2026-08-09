#!/usr/bin/env python3
"""Extract the approved pearl-shell throne as a transparent runtime card.

The source is the accepted Regen-01 flat-storybook turnaround sheet.  This tool
crops its orthographic front view and removes only the connected cream studio
matte.  It does not repaint, upscale, interpolate RGB, or add visual content.
The manifest records the exact source rectangle, mask, dimensions, and hashes.
"""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops


SOURCE_SIZE = (1536, 1024)
SOURCE_RECT = (48, 16, 570, 540)
MATTE_DISTANCE_LIMIT = 50.0
MATTE_CHANNEL_LIMIT = 43
OBJECT_FLOOR_Y = 503


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _connected_studio_matte(crop: Image.Image) -> Image.Image:
    """Return object alpha after removing only border-connected studio matte."""
    width, height = crop.size
    pixels = crop.load()
    candidates = bytearray(width * height)
    for y in range(height):
        # The accepted sheet uses a gently varying cream field.  Sampling both
        # clear side gutters per row follows that gradient without modeling or
        # changing any subject pixels.
        samples = [pixels[x, y] for x in range(12)]
        samples.extend(pixels[x, y] for x in range(width - 12, width))
        background = tuple(
            sum(sample[channel] for sample in samples) / len(samples)
            for channel in range(3)
        )
        for x in range(width):
            color = pixels[x, y]
            delta = tuple(abs(color[channel] - background[channel])
                          for channel in range(3))
            distance = math.sqrt(sum(value * value for value in delta))
            if max(delta) <= MATTE_CHANNEL_LIMIT \
                    and distance <= MATTE_DISTANCE_LIMIT:
                candidates[y * width + x] = 1

    connected = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()
    for x in range(width):
        for y in (0, height - 1):
            index = y * width + x
            if candidates[index] and not connected[index]:
                connected[index] = 1
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            index = y * width + x
            if candidates[index] and not connected[index]:
                connected[index] = 1
                queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y),
                       (x, y - 1), (x, y + 1)):
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            index = ny * width + nx
            if candidates[index] and not connected[index]:
                connected[index] = 1
                queue.append((nx, ny))

    alpha = Image.new("L", crop.size, 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        for x in range(width):
            if connected[y * width + x]:
                alpha_pixels[x, y] = 0
    return alpha


def _remove_turnaround_floor_shadow(alpha: Image.Image) -> Image.Image:
    """Remove the source sheet's soft floor shadow below the chair base.

    The runtime card casts its own scene-depth contact shadow.  The accepted
    front-view object ends at source y=518; pixels below it belong only to the
    turnaround sheet's diffuse studio floor shadow.
    """
    result = alpha.copy()
    pixels = result.load()
    for y in range(OBJECT_FLOOR_Y, result.height):
        for x in range(result.width):
            pixels[x, y] = 0
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    arguments = parser.parse_args()

    with Image.open(arguments.source) as opened:
        source = opened.convert("RGB")
    if source.size != SOURCE_SIZE:
        raise ValueError(
            f"Expected accepted Regen-01 sheet at {SOURCE_SIZE}; "
            f"got {source.width}x{source.height}: {arguments.source}")

    crop = source.crop(SOURCE_RECT)
    mask = _remove_turnaround_floor_shadow(_connected_studio_matte(crop))

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
        "purpose": "Pixel-preserving approved pearl-shell throne Sprite3D cutout",
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
            "method": (
                "border-connected accepted cream-studio matte removal + "
                "source-sheet floor-shadow exclusion"
            ),
            "distance_limit": MATTE_DISTANCE_LIMIT,
            "channel_limit": MATTE_CHANNEL_LIMIT,
            "object_floor_y_in_crop": OBJECT_FLOOR_Y,
            "source_authority": "accepted Regen-01 orthographic front view",
        },
    }
    arguments.manifest.parent.mkdir(parents=True, exist_ok=True)
    arguments.manifest.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
