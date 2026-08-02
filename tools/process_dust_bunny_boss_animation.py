#!/usr/bin/env python3
"""Normalize generated dust-bunny boss sheets into four-frame mobile atlases."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "assets_src" / "concepts" / "dust_bunny_animated_2026-07-27"
CHROMA_ROOT = SOURCE_ROOT / "boss_chroma"
RUNTIME_ROOT = ROOT / "assets" / "sprites" / "dust_bunnies" / "boss"
SHEET_SIZE = (1024, 1024)
CELL_SIZE = (512, 512)


def _is_key_like(red: int, green: int, blue: int) -> bool:
	return green > 180 and green > red * 1.7 and green > blue * 1.7


def _validate_grid(
	image: Image.Image,
	label: str,
	minimum_coverage: float,
) -> None:
	if image.size != SHEET_SIZE:
		raise ValueError(f"{label}: expected {SHEET_SIZE}, got {image.size}")
	rgb = image.convert("RGB")
	for frame_index in range(4):
		column = frame_index % 2
		row = frame_index // 2
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
				f"{label}: frame {frame_index} has too little subject coverage "
				f"({coverage:.3f})"
			)
		if coverage > 0.82:
			raise ValueError(
				f"{label}: frame {frame_index} has too much subject coverage "
				f"({coverage:.3f})"
			)
	for corner in (
		(0, 0),
		(SHEET_SIZE[0] - 1, 0),
		(0, SHEET_SIZE[1] - 1),
		(SHEET_SIZE[0] - 1, SHEET_SIZE[1] - 1),
	):
		red, green, blue = rgb.getpixel(corner)
		if not _is_key_like(red, green, blue):
			raise ValueError(f"{label}: corner {corner} is not chroma green")


def _normalize(
	source: Path,
	output: Path,
	label: str,
	minimum_coverage: float = 0.04,
) -> None:
	image = Image.open(source).convert("RGB")
	ratio = image.width / float(max(image.height, 1))
	if abs(ratio - 1.0) > 0.02:
		raise ValueError(f"{label}: expected a square 2x2 source sheet, got {image.size}")
	normalized = image.resize(SHEET_SIZE, Image.Resampling.LANCZOS)
	_validate_grid(normalized, label, minimum_coverage)
	output.parent.mkdir(parents=True, exist_ok=True)
	normalized.save(output, optimize=True)
	print(f"{label}: wrote {output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


def _validate_runtime(path: Path) -> None:
	image = Image.open(path)
	if image.mode != "RGBA":
		raise ValueError(f"{path.name}: expected RGBA runtime texture, got {image.mode}")
	if image.size != SHEET_SIZE:
		raise ValueError(
			f"{path.name}: expected runtime size {SHEET_SIZE}, got {image.size}"
		)
	alpha = image.getchannel("A")
	corners = (
		(0, 0),
		(SHEET_SIZE[0] - 1, 0),
		(0, SHEET_SIZE[1] - 1),
		(SHEET_SIZE[0] - 1, SHEET_SIZE[1] - 1),
	)
	if any(alpha.getpixel(corner) != 0 for corner in corners):
		raise ValueError(f"{path.name}: expected transparent atlas corners")
	alpha_values = list(alpha.get_flattened_data())
	transparent = sum(1 for value in alpha_values if value == 0)
	partial = sum(1 for value in alpha_values if 0 < value < 255)
	if transparent < int(SHEET_SIZE[0] * SHEET_SIZE[1] * 0.25):
		raise ValueError(f"{path.name}: too little transparent background")
	if partial < 100:
		raise ValueError(f"{path.name}: alpha edge matte is unexpectedly hard")
	print(f"{path.name}: RGBA OK, transparent={transparent}, partial={partial}")


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--jump-source", type=Path)
	parser.add_argument("--laugh-source", type=Path)
	parser.add_argument("--flinch-source", type=Path)
	parser.add_argument("--angry-source", type=Path)
	parser.add_argument("--implode-source", type=Path)
	parser.add_argument("--validate-runtime", action="store_true")
	args = parser.parse_args()
	sources = {
		"jump": args.jump_source,
		"laugh_vulnerable": args.laugh_source,
		"flinch": args.flinch_source,
		"angry": args.angry_source,
		"implode": args.implode_source,
	}
	if not any(sources.values()) and not args.validate_runtime:
		parser.error("provide at least one boss animation source or validate runtime")
	for label, source in sources.items():
		if source is None:
			continue
		minimum_coverage = 0.005 if label == "implode" else 0.04
		_normalize(
			source,
			CHROMA_ROOT / f"dust_bunny_boss_{label}_atlas_chroma.png",
			label,
			minimum_coverage,
		)
	if args.validate_runtime:
		runtime_paths = sorted(RUNTIME_ROOT.glob("dust_bunny_boss_*.png"))
		if len(runtime_paths) != 5:
			raise ValueError(
				f"expected five boss runtime atlases, found {len(runtime_paths)}"
			)
		for runtime_path in runtime_paths:
			_validate_runtime(runtime_path)


if __name__ == "__main__":
	main()
