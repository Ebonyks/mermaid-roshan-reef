#!/usr/bin/env python3
"""Build uncropped audit contact sheets for the PNW woody-plant turntables."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "assets_src" / "blender" / "qa_sky_lagoon_pnw_woody_plants"
TREES = [
    "lagoon_tree_douglas_fir",
    "lagoon_tree_western_redcedar",
    "lagoon_tree_western_hemlock",
    "lagoon_tree_sitka_spruce",
    "lagoon_tree_shore_pine",
    "lagoon_tree_pacific_yew",
    "lagoon_tree_bigleaf_maple",
    "lagoon_tree_red_alder",
    "lagoon_tree_black_cottonwood",
    "lagoon_tree_pacific_madrone",
    "lagoon_tree_garry_oak",
    "lagoon_tree_pacific_dogwood",
]
SHRUBS = [
    "lagoon_shrub_salal_a",
    "lagoon_shrub_salal_b",
    "lagoon_shrub_oregon_grape_a",
    "lagoon_shrub_oregon_grape_b",
    "lagoon_shrub_red_flowering_currant_a",
    "lagoon_shrub_red_flowering_currant_b",
    "lagoon_shrub_oceanspray_a",
    "lagoon_shrub_oceanspray_b",
    "lagoon_shrub_salmonberry_a",
    "lagoon_shrub_salmonberry_b",
    "lagoon_shrub_trailing_blackberry_a",
    "lagoon_shrub_trailing_blackberry_b",
]


def build_sheet(names: list[str], angle: int, output: Path, columns: int) -> None:
    frame = (350, 513)
    label_height = 40
    margin = 12
    rows = math.ceil(len(names) / columns)
    sheet = Image.new("RGB", (
        margin + columns * (frame[0] + margin),
        margin + rows * (frame[1] + label_height + margin)), (20, 16, 34))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=17)
    for index, name in enumerate(names):
        row, column = divmod(index, columns)
        x = margin + column * (frame[0] + margin)
        y = margin + row * (frame[1] + label_height + margin)
        path = QA / (name + "_%03d.png" % angle)
        with Image.open(path) as source:
            contained = ImageOps.contain(source.convert("RGB"), frame,
                                         method=Image.Resampling.LANCZOS)
            paste_x = x + (frame[0] - contained.width) // 2
            paste_y = y + (frame[1] - contained.height) // 2
            sheet.paste(contained, (paste_x, paste_y))
        draw.text((x + 3, y + frame[1] + 7), name.removeprefix("lagoon_"),
                  fill=(245, 238, 220), font=font)
    sheet.save(output, optimize=True)


for view_angle in (0, 45, 135):
    build_sheet(TREES, view_angle,
                QA / ("pnw_tree_family_%03d_contact.png" % view_angle), 4)
    build_sheet(SHRUBS, view_angle,
                QA / ("pnw_shrub_family_%03d_contact.png" % view_angle), 3)
print("PNW_WOODY_CONTACT|trees=12|shrubs=6|views=3")
