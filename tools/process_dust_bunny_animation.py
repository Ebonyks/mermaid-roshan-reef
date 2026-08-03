#!/usr/bin/env python3
"""Normalize generated dust-bunny animation sheets for the mobile runtime."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "assets_src" / "concepts" / "dust_bunny_animated_2026-07-27"
CHROMA_ROOT = SOURCE_ROOT / "chroma"
SHEET_SIZE = (768, 512)
CELL_SIZE = (256, 256)
KEY = (0, 255, 0)


def _is_key_like(red: int, green: int, blue: int) -> bool:
	return green > 180 and green > red * 1.7 and green > blue * 1.7


def _validate_grid(
	image: Image.Image,
	label: str,
	minimum_coverage: float = 0.08,
) -> None:
	if image.size != SHEET_SIZE:
		raise ValueError(f"{label}: expected {SHEET_SIZE}, got {image.size}")
	rgb = image.convert("RGB")
	for frame_index in range(6):
		column = frame_index % 3
		row = frame_index // 3
		cell = rgb.crop(
			(
				column * CELL_SIZE[0],
				row * CELL_SIZE[1],
				(column + 1) * CELL_SIZE[0],
				(row + 1) * CELL_SIZE[1],
			)
		)
		subject_pixels = sum(
			1
			for red, green, blue in cell.get_flattened_data()
			if not _is_key_like(red, green, blue)
		)
		coverage = subject_pixels / float(CELL_SIZE[0] * CELL_SIZE[1])
		if coverage < minimum_coverage:
			raise ValueError(
				f"{label}: frame {frame_index} has too little subject coverage ({coverage:.3f})"
			)
		if coverage > 0.78:
			raise ValueError(
				f"{label}: frame {frame_index} has too much subject coverage ({coverage:.3f})"
			)
	for corner in ((0, 0), (SHEET_SIZE[0] - 1, 0), (0, SHEET_SIZE[1] - 1),
			(SHEET_SIZE[0] - 1, SHEET_SIZE[1] - 1)):
		red, green, blue = rgb.getpixel(corner)
		if not _is_key_like(red, green, blue):
			raise ValueError(f"{label}: corner {corner} is not chroma green")


def _normalize(
	source: Path,
	output: Path,
	label: str,
	minimum_coverage: float = 0.08,
) -> None:
	image = Image.open(source).convert("RGB")
	ratio = image.width / float(max(image.height, 1))
	if abs(ratio - 1.5) > 0.02:
		raise ValueError(f"{label}: expected a 3:2 source sheet, got {image.size}")
	normalized = image.resize(SHEET_SIZE, Image.Resampling.LANCZOS)
	_validate_grid(normalized, label, minimum_coverage)
	output.parent.mkdir(parents=True, exist_ok=True)
	normalized.save(output, optimize=True)
	print(f"{label}: wrote {output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--idle-source", type=Path)
	parser.add_argument("--hop-source", type=Path)
	parser.add_argument("--defeat-source", type=Path)
	args = parser.parse_args()
	if args.idle_source is None and args.hop_source is None and args.defeat_source is None:
		parser.error("provide at least one animation source")
	if args.idle_source is not None:
		_normalize(
			args.idle_source,
			CHROMA_ROOT / "dust_bunny_idle_atlas_chroma.png",
			"idle",
		)
	if args.hop_source is not None:
		_normalize(
			args.hop_source,
			CHROMA_ROOT / "dust_bunny_hop_atlas_chroma.png",
			"hop",
		)
	if args.defeat_source is not None:
		_normalize(
			args.defeat_source,
			CHROMA_ROOT / "dust_bunny_defeat_atlas_chroma.png",
			"defeat",
			0.005,
		)


if __name__ == "__main__":
	main()
