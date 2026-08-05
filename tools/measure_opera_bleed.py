#!/usr/bin/env python3
"""Measure the horizontal bleed margin of each Pearl Opera career painting.

The four ``world_<career>_c{0,1}r{0,1}.png`` tiles compose into a 2048-square
master.  ``scripts/opera_world_backdrop_2d.gd`` (``_draw_tile_set``) draws
``master[448:1600, 0:2048]`` across the whole 1280x720 screen.  Vertically that
crop is exactly the sharp band, so painting-normalized y maps straight to
screen y.  Horizontally the artwork is inset inside a blurred bleed margin, so
a coordinate derived from the painting has to be remapped onto the span the
painting actually occupies on screen.

This script measures that span by column-wise second-derivative energy and
prints the ``BLEED`` table used by ``scripts/opera_stage_paths.gd``.  Re-run it
whenever a world painting is regenerated.

    python tools/measure_opera_bleed.py
"""

from __future__ import annotations

import os
import sys

import numpy as np
from PIL import Image

BACKDROPS = "assets/opera/worlds/backdrops"
CAREERS = [
    "chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
    "boxer", "magician", "painter", "astronaut", "racer", "popstar", "nursery",
]
# The engine's crop of the composed master (opera_world_backdrop_2d.gd:66-75).
CROP = (0, 448, 2048, 1600)
# A column counts as sharp when its high-frequency energy clears this fraction
# of the frame's 90th percentile.  Generous on purpose: we want the outermost
# genuinely-painted column, not the outermost busy one.
SHARP_FRACTION = 0.25


def composed_master(career: str) -> Image.Image | None:
    tiles = {}
    for column in (0, 1):
        for row in (0, 1):
            path = os.path.join(BACKDROPS, f"world_{career}_c{column}r{row}.png")
            if not os.path.exists(path):
                return None
            tiles[(column, row)] = Image.open(path).convert("L")
    width, height = tiles[(0, 0)].size
    master = Image.new("L", (width * 2, height * 2))
    for (column, row), tile in tiles.items():
        master.paste(tile, (column * width, row * height))
    return master


def sharp_span(career: str) -> tuple[float, float] | None:
    master = composed_master(career)
    if master is None:
        return None
    drawn = np.asarray(master.crop(CROP), dtype=np.float32)
    energy = np.abs(drawn[:, 2:] - 2 * drawn[:, 1:-1] + drawn[:, :-2]).mean(axis=0)
    sharp = np.where(energy > np.percentile(energy, 90) * SHARP_FRACTION)[0]
    if sharp.size == 0:
        return None
    width = drawn.shape[1]
    return float(sharp[0]) / width, float(sharp[-1] + 1) / width


def main() -> int:
    spans: dict[str, tuple[float, float]] = {}
    for career in CAREERS:
        span = sharp_span(career)
        if span is None:
            print(f"# {career}: no tiles on disk", file=sys.stderr)
            continue
        spans[career] = span
    if not spans:
        print("no career tiles found - run from the repository root", file=sys.stderr)
        return 1

    print("const BLEED: Dictionary = {")
    for career, (low, high) in spans.items():
        print(f'\t"{career}": [{low:.4f}, {high:.4f}],')
    print("}")

    lows = [low for low, _ in spans.values()]
    highs = [high for _, high in spans.values()]
    print(
        f"\n# default [{np.mean(lows):.4f}, {np.mean(highs):.4f}]; "
        f"per-career spread costs at most "
        f"{max(max(lows) - min(lows), max(highs) - min(highs)) * 1280:.1f}px",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
