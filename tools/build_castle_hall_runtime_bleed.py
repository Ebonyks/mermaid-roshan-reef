#!/usr/bin/env python3
"""Build the Main Hall's lossless one-pixel Sprite3D seam safety bleed.

The accepted source tiles remain immutable and non-overlapping. Mobile raster
precision can expose a one-pixel clear row where two exactly adjacent
Sprite3D quads meet. For each top-row tile, this tool appends the first source
row of the corresponding bottom tile. The two runtime cards therefore render
the same approved master pixels at their one-pixel geometric overlap.

No pixel is generated, interpolated, scaled, cropped from the approved view,
or substituted. The manifest records both source and derived hashes and
verifies the appended row byte-for-byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


TOP_TEMPLATE = "main_hall_room_led_r0_c{column}.png"
BOTTOM_TEMPLATE = "main_hall_room_led_r1_c{column}.png"
OUTPUT_TEMPLATE = "main_hall_room_led_r0_c{column}_bleed.png"


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

    for column in range(4):
        top_path = arguments.tile_dir / TOP_TEMPLATE.format(column=column)
        bottom_path = arguments.tile_dir / BOTTOM_TEMPLATE.format(column=column)
        output_path = arguments.out_dir / OUTPUT_TEMPLATE.format(column=column)
        with Image.open(top_path) as opened_top:
            top = opened_top.copy()
        with Image.open(bottom_path) as opened_bottom:
            bottom = opened_bottom.copy()
        if top.mode != "RGB" or bottom.mode != "RGB":
            raise ValueError(
                f"Expected RGB source tiles, got {top.mode} and {bottom.mode}"
            )
        if top.width != bottom.width or top.height != 470 \
                or bottom.height != 471:
            raise ValueError(
                f"Unexpected column {column} tile sizes: "
                f"{top.size} and {bottom.size}"
            )

        first_bottom_row = bottom.crop((0, 0, bottom.width, 1))
        derived = Image.new("RGB", (top.width, top.height + 1))
        derived.paste(top, (0, 0))
        derived.paste(first_bottom_row, (0, top.height))
        derived.save(output_path, format="PNG", optimize=True)

        with Image.open(output_path) as opened_result:
            result = opened_result.copy()
        source_body_exact = _pixels_equal(
            result.crop((0, 0, top.width, top.height)), top)
        appended_row_exact = _pixels_equal(
            result.crop((0, top.height, top.width, top.height + 1)),
            first_bottom_row,
        )
        if not source_body_exact or not appended_row_exact:
            raise RuntimeError(
                f"Column {column} seam bleed changed an approved pixel")

        records.append({
            "column": column,
            "top_source_path": top_path.as_posix(),
            "top_source_dimensions": list(top.size),
            "top_source_sha256": _sha256(top_path),
            "bottom_source_path": bottom_path.as_posix(),
            "bottom_source_dimensions": list(bottom.size),
            "bottom_source_sha256": _sha256(bottom_path),
            "runtime_path": output_path.as_posix(),
            "runtime_dimensions": list(result.size),
            "runtime_sha256": _sha256(output_path),
            "approved_source_body_pixel_exact": source_body_exact,
            "appended_row_matches_bottom_first_row": appended_row_exact,
            "logical_source_rectangle": [
                column * top.width, 0, (column + 1) * top.width, top.height
            ],
            "runtime_render_rectangle": [
                column * top.width, 0,
                (column + 1) * top.width, top.height + 1
            ],
            "seam_overlap_pixels": 1,
        })

    manifest = {
        "schema": 1,
        "purpose": (
            "Mobile-renderer raster safety for the Main Hall horizontal "
            "Sprite3D tile boundary"
        ),
        "art_change": "none; exact approved edge-row duplication only",
        "source_tile_rectangles_remain_non_overlapping": True,
        "runtime_render_overlap_pixels": 1,
        "scaling": False,
        "interpolation": False,
        "crop_or_content_loss": False,
        "new_art": False,
        "all_source_pixels_preserved": all(
            bool(record["approved_source_body_pixel_exact"])
            for record in records
        ),
        "all_bleed_rows_match_approved_lower_source": all(
            bool(record["appended_row_matches_bottom_first_row"])
            for record in records
        ),
        "tiles": records,
    }
    arguments.manifest.parent.mkdir(parents=True, exist_ok=True)
    arguments.manifest.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
