#!/usr/bin/env python3
"""Build labeled contact sheets from the pass-35 runtime art captures."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


GROUPS = {
	"reef": ("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_"),
	"lagoon": ("10_", "11_", "12_", "13_", "14_", "15_", "16_"),
	"collections_north": ("17_", "18_", "19_", "20_", "21_", "22_", "23_"),
	"castle": ("30_", "31_", "32_", "33_", "34_", "35_", "36_", "37_", "38_", "39_", "40_", "41_", "42_", "43_"),
	"arenas": ("50_", "51_", "52_", "53_", "54_", "55_", "56_", "57_"),
	"galaxy": ("60_", "61_", "62_", "63_", "64_"),
	"dungeon": ("70_",),
	"picture_kart": ("80_", "90_", "91_", "92_"),
}


def build_sheet(paths: list[Path], output: Path, columns: int = 3) -> None:
	thumb_size = (512, 288)
	label_height = 34
	margin = 14
	rows = math.ceil(len(paths) / columns)
	width = margin + columns * (thumb_size[0] + margin)
	height = margin + rows * (thumb_size[1] + label_height + margin)
	sheet = Image.new("RGB", (width, height), (22, 18, 38))
	draw = ImageDraw.Draw(sheet)
	font = ImageFont.load_default(size=18)
	for index, path in enumerate(paths):
		row, column = divmod(index, columns)
		x = margin + column * (thumb_size[0] + margin)
		y = margin + row * (thumb_size[1] + label_height + margin)
		with Image.open(path) as source:
			thumb = ImageOps.fit(source.convert("RGB"), thumb_size, method=Image.Resampling.LANCZOS)
		sheet.paste(thumb, (x, y))
		draw.text((x + 4, y + thumb_size[1] + 6), path.stem, fill=(244, 236, 220), font=font)
	output.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(output, optimize=True)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--captures",
		type=Path,
		default=Path("audit/runtime_shots_2026-07-16/pass_35"),
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=Path("audit/runtime_shots_2026-07-16/pass_35/contact_sheets"),
	)
	args = parser.parse_args()
	all_paths = sorted(args.captures.glob("*.png"))
	for group, prefixes in GROUPS.items():
		paths = [path for path in all_paths if path.name.startswith(prefixes)]
		if not paths:
			continue
		output = args.output / f"pass35_{group}.jpg"
		build_sheet(paths, output)
		print(f"ART35_CONTACT|{group}|{len(paths)}|{output}")


if __name__ == "__main__":
	main()
