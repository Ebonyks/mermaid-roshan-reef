#!/usr/bin/env python3
"""Losslessly split the two Pearl Castle hall screens into a 2x4 card grid.

The two source screens remain separate 16:9 masters. Each is divided into a
2x2 grid without scaling; together they form one logical two-row, four-column
runtime background. The script verifies exact pixel reconstruction for both
source screens and records every source rectangle and SHA-256 hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bounds(length: int) -> list[int]:
    return [0, length // 2, length]


def _pixel_equal(left: Image.Image, right: Image.Image) -> bool:
    difference = ImageChops.difference(left, right)
    return difference.getbbox() is None


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    windows_font = Path(
        "C:/Windows/Fonts/arialbd.ttf" if bold
        else "C:/Windows/Fonts/arial.ttf"
    )
    if windows_font.exists():
        return ImageFont.truetype(str(windows_font), size)
    return ImageFont.load_default()


def _write_proof(
    tiles: list[dict[str, object]],
    output_path: Path,
) -> None:
    columns = 4
    rows = 2
    cell_width = 420
    cell_height = 270
    header_height = 54
    canvas = Image.new(
        "RGB",
        (columns * cell_width, header_height + rows * cell_height),
        "#f4f1ff",
    )
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (16, 14),
        "PEARL CASTLE MAIN HALL — LOSSLESS 2×4 BACKGROUND CARD GRID",
        fill="#302a68",
        font=_font(20, bold=True),
    )
    for tile_record in tiles:
        row = int(tile_record["row"])
        column = int(tile_record["column"])
        tile_path = Path(str(tile_record["path"]))
        tile = Image.open(tile_path).convert("RGB")
        tile.thumbnail((cell_width - 18, cell_height - 42), Image.Resampling.LANCZOS)
        x = column * cell_width + (cell_width - tile.width) // 2
        y = header_height + row * cell_height + 4
        canvas.paste(tile, (x, y))
        draw.rectangle(
            (
                column * cell_width + 4,
                header_height + row * cell_height + 2,
                (column + 1) * cell_width - 5,
                header_height + (row + 1) * cell_height - 4,
            ),
            outline="#d4af48",
            width=3,
        )
        label = (
            f"r{row} c{column}  "
            f"{tile_record['dimensions'][0]}×{tile_record['dimensions'][1]}"
        )
        draw.text(
            (column * cell_width + 12, header_height + (row + 1) * cell_height - 32),
            label,
            fill="#403977",
            font=_font(16),
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)


def _split_screen(
    source_path: Path,
    screen_index: int,
    output_dir: Path,
    prefix: str,
    view_rectangle: tuple[int, int, int, int] | None,
) -> tuple[list[dict[str, object]], bool, Image.Image]:
    source_master = Image.open(source_path).convert("RGB")
    source = (
        source_master.crop(view_rectangle)
        if view_rectangle is not None
        else source_master
    )
    x_bounds = _bounds(source.width)
    y_bounds = _bounds(source.height)
    reconstruction = Image.new("RGB", source.size)
    records: list[dict[str, object]] = []

    for row in range(2):
        for local_column in range(2):
            global_column = screen_index * 2 + local_column
            rectangle = (
                x_bounds[local_column],
                y_bounds[row],
                x_bounds[local_column + 1],
                y_bounds[row + 1],
            )
            tile = source.crop(rectangle)
            if max(tile.size) > 1024:
                raise ValueError(
                    f"{source_path} produces {tile.size[0]}x{tile.size[1]} tile "
                    "larger than the 1024px runtime limit"
                )
            tile_name = f"{prefix}_r{row}_c{global_column}.png"
            tile_path = output_dir / tile_name
            tile.save(tile_path, format="PNG", optimize=True)
            reconstruction.paste(tile, (rectangle[0], rectangle[1]))
            records.append({
                "row": row,
                "column": global_column,
                "screen": "A" if screen_index == 0 else "B",
                "screen_local_column": local_column,
                "source": str(source_path),
                "source_rectangle": [
                    rectangle[0] + (view_rectangle[0] if view_rectangle else 0),
                    rectangle[1] + (view_rectangle[1] if view_rectangle else 0),
                    rectangle[2] + (view_rectangle[0] if view_rectangle else 0),
                    rectangle[3] + (view_rectangle[1] if view_rectangle else 0),
                ],
                "logical_world_rectangle": [
                    rectangle[0] + screen_index * source.width,
                    rectangle[1],
                    rectangle[2] + screen_index * source.width,
                    rectangle[3],
                ],
                "dimensions": list(tile.size),
                "path": str(tile_path),
                "sha256": _sha256(tile_path),
            })

    return records, _pixel_equal(source, reconstruction), reconstruction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen-a", required=True, type=Path)
    parser.add_argument("--screen-b", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--proof", required=True, type=Path)
    parser.add_argument("--reconstruction-dir", type=Path)
    parser.add_argument("--prefix", default="main_hall_bg")
    parser.add_argument("--view-x", type=int)
    parser.add_argument("--view-y", type=int)
    parser.add_argument("--view-width", type=int)
    parser.add_argument("--view-height", type=int)
    arguments = parser.parse_args()

    arguments.out_dir.mkdir(parents=True, exist_ok=True)
    screen_a = Image.open(arguments.screen_a)
    screen_b = Image.open(arguments.screen_b)
    if screen_a.size != screen_b.size:
        raise ValueError(
            f"Screen dimensions differ: {screen_a.size} vs {screen_b.size}"
        )
    view_values = (
        arguments.view_x,
        arguments.view_y,
        arguments.view_width,
        arguments.view_height,
    )
    if any(value is not None for value in view_values) \
            and not all(value is not None for value in view_values):
        raise ValueError("All four --view-* values are required together")
    view_rectangle: tuple[int, int, int, int] | None = None
    if all(value is not None for value in view_values):
        view_rectangle = (
            int(arguments.view_x),
            int(arguments.view_y),
            int(arguments.view_x + arguments.view_width),
            int(arguments.view_y + arguments.view_height),
        )
        if view_rectangle[0] < 0 or view_rectangle[1] < 0 \
                or view_rectangle[2] > screen_a.width \
                or view_rectangle[3] > screen_a.height:
            raise ValueError(
                f"View {view_rectangle} exceeds master {screen_a.size}"
            )
    runtime_size = (
        (view_rectangle[2] - view_rectangle[0],
         view_rectangle[3] - view_rectangle[1])
        if view_rectangle is not None
        else screen_a.size
    )

    records_a, exact_a, reconstruction_a = _split_screen(
        arguments.screen_a,
        0,
        arguments.out_dir,
        arguments.prefix,
        view_rectangle,
    )
    records_b, exact_b, reconstruction_b = _split_screen(
        arguments.screen_b,
        1,
        arguments.out_dir,
        arguments.prefix,
        view_rectangle,
    )
    records = sorted(
        records_a + records_b,
        key=lambda record: (int(record["row"]), int(record["column"])),
    )
    production_width = 2048
    production_height = round(
        production_width * runtime_size[1] / runtime_size[0]
    )
    production_x_bounds = _bounds(production_width)
    production_y_bounds = _bounds(production_height)
    source_ratio = runtime_size[0] / runtime_size[1]
    production_ratio = production_width / production_height
    manifest = {
        "schema": 1,
        "purpose": "Pearl Castle Main Hall logical 2-row x 4-column Sprite3D grid",
        "art_change": "none; lossless crop only",
        "logical_grid": {"rows": 2, "columns": 4, "tile_count": 8},
        "source_master_dimensions": list(screen_a.size),
        "runtime_view_rectangle": (
            list(view_rectangle) if view_rectangle is not None else None
        ),
        "source_screen_dimensions": list(runtime_size),
        "source_aspect_ratio": source_ratio,
        "logical_background_dimensions": [runtime_size[0] * 2, runtime_size[1]],
        "production_target": {
            "minimum_native_long_edge": 2048,
            "screen_dimensions": [production_width, production_height],
            "screen_aspect_ratio": production_ratio,
            "ratio_delta": abs(source_ratio - production_ratio),
            "one_pixel_rounding_tolerance": True,
            "tile_column_widths": [
                production_x_bounds[1] - production_x_bounds[0],
                production_x_bounds[2] - production_x_bounds[1],
            ],
            "tile_row_heights": [
                production_y_bounds[1] - production_y_bounds[0],
                production_y_bounds[2] - production_y_bounds[1],
            ],
            "world_dimensions_unchanged": True,
            "scaling_permitted": False,
        },
        "sources": {
            "A": {
                "path": str(arguments.screen_a),
                "sha256": _sha256(arguments.screen_a),
                "pixel_exact_reconstruction": exact_a,
            },
            "B": {
                "path": str(arguments.screen_b),
                "sha256": _sha256(arguments.screen_b),
                "pixel_exact_reconstruction": exact_b,
            },
        },
        "all_sources_reconstruct_exactly": exact_a and exact_b,
        "tiles": records,
    }
    arguments.manifest.parent.mkdir(parents=True, exist_ok=True)
    reconstruction_dir = (
        arguments.reconstruction_dir
        if arguments.reconstruction_dir is not None
        else arguments.proof.parent
    )
    reconstruction_dir.mkdir(parents=True, exist_ok=True)
    reconstruction_a_path = (
        reconstruction_dir / "main_hall_2x4_exact_reconstruction_screen_a.png")
    reconstruction_b_path = (
        reconstruction_dir / "main_hall_2x4_exact_reconstruction_screen_b.png")
    reconstruction_a.save(reconstruction_a_path, format="PNG", optimize=True)
    reconstruction_b.save(reconstruction_b_path, format="PNG", optimize=True)
    manifest["exact_reconstruction_proofs"] = {
        "A": {
            "path": str(reconstruction_a_path),
            "sha256": _sha256(reconstruction_a_path),
            "pixel_exact": exact_a,
        },
        "B": {
            "path": str(reconstruction_b_path),
            "sha256": _sha256(reconstruction_b_path),
            "pixel_exact": exact_b,
        },
    }
    arguments.manifest.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_proof(records, arguments.proof)
    if not manifest["all_sources_reconstruct_exactly"]:
        raise RuntimeError("Tile reconstruction changed source pixels")


if __name__ == "__main__":
    main()
