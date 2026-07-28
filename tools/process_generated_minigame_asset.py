#!/usr/bin/env python3
"""Normalize regenerated minigame art to the project's runtime texture rules."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


SIZES = {
    "background": (2048, 1024),
    "background-square": (1024, 1024),
    "background-tall": (512, 1024),
    "sprite-square": (1024, 1024),
    "sprite-wide": (2048, 1024),
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--kind", required=True, choices=sorted(SIZES))
    parser.add_argument("--grid-cols", type=int)
    parser.add_argument("--grid-rows", type=int)
    parser.add_argument("--cell-index", type=int)
    return parser.parse_args()


def _grid_cell(
    image: Image.Image,
    columns: int | None,
    rows: int | None,
    index: int | None,
) -> Image.Image:
    values = (columns, rows, index)
    if all(value is None for value in values):
        return image
    if any(value is None for value in values):
        raise SystemExit("--grid-cols, --grid-rows, and --cell-index must be used together")
    assert columns is not None and rows is not None and index is not None
    if columns < 1 or rows < 1 or index < 0 or index >= columns * rows:
        raise SystemExit("invalid grid dimensions or cell index")
    column = index % columns
    row = index // columns
    left = round(image.width * column / columns)
    top = round(image.height * row / rows)
    right = round(image.width * (column + 1) / columns)
    bottom = round(image.height * (row + 1) / rows)
    return image.crop((left, top, right, bottom))


def _fit_sprite(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    source = image.convert("RGBA")
    margin = 48
    bounds = (size[0] - margin * 2, size[1] - margin * 2)
    source.thumbnail(bounds, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    offset = ((size[0] - source.width) // 2, (size[1] - source.height) // 2)
    canvas.alpha_composite(source, offset)
    return canvas


def main() -> None:
    args = _parse_args()
    size = SIZES[args.kind]
    with Image.open(args.input) as image:
        source = _grid_cell(
            image,
            args.grid_cols,
            args.grid_rows,
            args.cell_index,
        )
        if args.kind.startswith("background"):
            output = ImageOps.fit(
                source.convert("RGB"),
                size,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
        else:
            output = _fit_sprite(source, size)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output, format="PNG", optimize=True)
    print(f"{args.output}: {output.width}x{output.height} {output.mode}")


if __name__ == "__main__":
    main()
