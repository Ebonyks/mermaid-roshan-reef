#!/usr/bin/env python3
"""Build the Main Hall's lossless one-pixel Sprite3D seam safety bleed.

The accepted source tiles remain immutable and non-overlapping. Mobile raster
precision can expose clear rows or columns where exactly adjacent Sprite3D
quads meet. Each runtime tile appends the first approved row and/or column of
its lower and right neighbors. Adjacent cards therefore render the same
approved master pixels at their one-pixel geometric overlap.

No pixel is generated, interpolated, scaled, cropped from the approved view,
or substituted. The manifest records both source and derived hashes and
verifies every appended edge byte-for-byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


SOURCE_TEMPLATE = "main_hall_room_led_r{row}_c{column}.png"
OUTPUT_TEMPLATE = "main_hall_room_led_r{row}_c{column}_bleed.png"
ROW_HEIGHTS = (470, 471)
COLUMNS = 4


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pixels_equal(left: Image.Image, right: Image.Image) -> bool:
    return ImageChops.difference(left, right).getbbox() is None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tile-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    arguments = parser.parse_args()

    arguments.out_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    source_tiles: dict[tuple[int, int], Image.Image] = {}
    source_paths: dict[tuple[int, int], Path] = {}

    for row, expected_height in enumerate(ROW_HEIGHTS):
        for column in range(COLUMNS):
            source_path = arguments.tile_dir / SOURCE_TEMPLATE.format(
                row=row, column=column)
            with Image.open(source_path) as opened_source:
                source = opened_source.copy()
            if source.mode != "RGB":
                raise ValueError(
                    f"Expected RGB source tile, got {source.mode}: "
                    f"{source_path}")
            if source.size != (836, expected_height):
                raise ValueError(
                    f"Unexpected tile size {source.size}: {source_path}")
            source_tiles[(row, column)] = source
            source_paths[(row, column)] = source_path

    for row, _expected_height in enumerate(ROW_HEIGHTS):
        logical_top = sum(ROW_HEIGHTS[:row])
        for column in range(COLUMNS):
            source = source_tiles[(row, column)]
            source_path = source_paths[(row, column)]
            bleed_right = column < COLUMNS - 1
            bleed_down = row < len(ROW_HEIGHTS) - 1
            output_path = arguments.out_dir / OUTPUT_TEMPLATE.format(
                row=row, column=column)
            render_width = source.width + int(bleed_right)
            render_height = source.height + int(bleed_down)
            derived = Image.new("RGB", (render_width, render_height))
            derived.paste(source, (0, 0))

            right_edge_exact = True
            lower_edge_exact = True
            corner_exact = True
            if bleed_right:
                right_edge = source_tiles[(row, column + 1)].crop(
                    (0, 0, 1, source.height))
                derived.paste(right_edge, (source.width, 0))
                right_edge_exact = _pixels_equal(
                    derived.crop((
                        source.width, 0,
                        source.width + 1, source.height)),
                    right_edge)
            if bleed_down:
                lower_edge = source_tiles[(row + 1, column)].crop(
                    (0, 0, source.width, 1))
                derived.paste(lower_edge, (0, source.height))
                lower_edge_exact = _pixels_equal(
                    derived.crop((
                        0, source.height,
                        source.width, source.height + 1)),
                    lower_edge)
            if bleed_right and bleed_down:
                corner = source_tiles[(row + 1, column + 1)].crop(
                    (0, 0, 1, 1))
                derived.paste(corner, (source.width, source.height))
                corner_exact = _pixels_equal(
                    derived.crop((
                        source.width, source.height,
                        source.width + 1, source.height + 1)),
                    corner)
            derived.save(output_path, format="PNG", optimize=True)

            with Image.open(output_path) as opened_result:
                result = opened_result.copy()
            source_body_exact = _pixels_equal(
                result.crop((0, 0, source.width, source.height)), source)
            source_exact = (
                source_body_exact and right_edge_exact
                and lower_edge_exact and corner_exact)
            if not source_exact:
                raise RuntimeError(
                    f"Tile r{row} c{column} bleed changed approved pixels")

            records.append({
                "row": row,
                "column": column,
                "source_path": source_path.as_posix(),
                "source_dimensions": list(source.size),
                "source_sha256": _sha256(source_path),
                "runtime_path": output_path.as_posix(),
                "runtime_dimensions": list(result.size),
                "runtime_sha256": _sha256(output_path),
                "approved_source_body_pixel_exact": source_body_exact,
                "appended_right_edge_matches_approved_neighbor":
                    right_edge_exact,
                "appended_lower_edge_matches_approved_neighbor":
                    lower_edge_exact,
                "appended_corner_matches_approved_neighbor": corner_exact,
                "logical_source_rectangle": [
                    column * source.width,
                    logical_top,
                    (column + 1) * source.width,
                    logical_top + source.height,
                ],
                "runtime_render_rectangle": [
                    column * source.width,
                    logical_top,
                    column * source.width + result.width,
                    logical_top + result.height,
                ],
                "seam_overlap_pixels": [
                    int(bleed_right), int(bleed_down)],
            })

    manifest = {
        "schema": 2,
        "purpose": (
            "Mobile-renderer raster safety for every Main Hall horizontal "
            "and vertical Sprite3D tile boundary"
        ),
        "art_change": (
            "none; exact approved right/lower neighbor-edge duplication only"
        ),
        "source_tile_rectangles_remain_non_overlapping": True,
        "runtime_render_overlap_pixels": [1, 1],
        "scaling": False,
        "interpolation": False,
        "crop_or_content_loss": False,
        "new_art": False,
        "all_source_pixels_preserved": all(
            bool(record["approved_source_body_pixel_exact"])
            for record in records
        ),
        "all_bleed_edges_match_approved_neighbors": all(
            bool(record[
                "appended_right_edge_matches_approved_neighbor"])
            and bool(record[
                "appended_lower_edge_matches_approved_neighbor"])
            and bool(record[
                "appended_corner_matches_approved_neighbor"])
            for record in records
        ),
        "tiles": records,
    }
    arguments.manifest.parent.mkdir(parents=True, exist_ok=True)
    arguments.manifest.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
