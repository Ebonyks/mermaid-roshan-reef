#!/usr/bin/env python3
"""Normalize Mermaid Roshan pool sheets into exact runtime atlas cells.

The accepted ImageGen outputs include thin white grid gutters.  Runtime
AtlasTextures address fixed-size cells, so this script crops those gutters,
rebuilds the cells at exact sizes, and uses the installed ImageGen chroma-key
helper for the two transparent atlases.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Final

from PIL import Image, ImageDraw


CELL_SIZE: Final[int] = 256
GUTTER_INSET: Final[int] = 6
RESAMPLING = Image.Resampling.LANCZOS


def _cell_bounds(
	width: int,
	height: int,
	columns: int,
	rows: int,
	column: int,
	row: int,
) -> tuple[int, int, int, int]:
	left = round(column * width / columns) + GUTTER_INSET
	top = round(row * height / rows) + GUTTER_INSET
	right = round((column + 1) * width / columns) - GUTTER_INSET
	bottom = round((row + 1) * height / rows) - GUTTER_INSET
	return left, top, right, bottom


def _normalize_source(source: Path, output: Path, size: tuple[int, int]) -> None:
	with Image.open(source) as image:
		normalized = image.convert("RGB").resize(size, RESAMPLING)
	output.parent.mkdir(parents=True, exist_ok=True)
	normalized.save(output, format="PNG", optimize=True)


def _rebuild_grid(
	source: Path,
	columns: int,
	rows: int,
	*,
	background: tuple[int, int, int],
) -> Image.Image:
	with Image.open(source) as opened:
		image = opened.convert("RGB")
		atlas = Image.new(
			"RGB",
			(columns * CELL_SIZE, rows * CELL_SIZE),
			background,
		)
		for row in range(rows):
			for column in range(columns):
				bounds = _cell_bounds(
					image.width,
					image.height,
					columns,
					rows,
					column,
					row,
				)
				cell = image.crop(bounds).resize(
					(CELL_SIZE, CELL_SIZE),
					RESAMPLING,
				)
				atlas.paste(cell, (column * CELL_SIZE, row * CELL_SIZE))
	return atlas


def _remove_chroma(source: Path, output: Path, helper: Path) -> None:
	subprocess.run(
		[
			sys.executable,
			str(helper),
			"--input",
			str(source),
			"--out",
			str(output),
			"--auto-key",
			"border",
			"--soft-matte",
			"--transparent-threshold",
			"12",
			"--opaque-threshold",
			"220",
			"--despill",
			"--force",
		],
		check=True,
	)


def _clear_cell_edges(
	output: Path,
	columns: int,
	rows: int,
	edge: int = 3,
) -> None:
	with Image.open(output) as opened:
		rgba = opened.convert("RGBA")
	alpha = rgba.getchannel("A")
	draw = ImageDraw.Draw(alpha)
	for row in range(rows):
		for column in range(columns):
			left = column * CELL_SIZE
			top = row * CELL_SIZE
			right = left + CELL_SIZE - 1
			bottom = top + CELL_SIZE - 1
			draw.rectangle((left, top, left + edge - 1, bottom), fill=0)
			draw.rectangle((right - edge + 1, top, right, bottom), fill=0)
			draw.rectangle((left, top, right, top + edge - 1), fill=0)
			draw.rectangle((left, bottom - edge + 1, right, bottom), fill=0)
	rgba.putalpha(alpha)
	rgba.save(output, format="PNG", optimize=True)


def _process_transparent_atlas(
	source: Path,
	normalized_source: Path,
	runtime: Path,
	columns: int,
	rows: int,
	helper: Path,
) -> None:
	size = (columns * CELL_SIZE, rows * CELL_SIZE)
	_normalize_source(source, normalized_source, size)
	chroma_cells = _rebuild_grid(
		source,
		columns,
		rows,
		background=(0, 255, 0),
	)
	temporary = normalized_source.with_name(f".{normalized_source.stem}.cells.png")
	chroma_cells.save(temporary, format="PNG", optimize=True)
	try:
		runtime.parent.mkdir(parents=True, exist_ok=True)
		_remove_chroma(temporary, runtime, helper)
		_clear_cell_edges(runtime, columns, rows)
	finally:
		temporary.unlink(missing_ok=True)


def _build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Build exact-cell Mermaid Roshan pool story atlases.",
	)
	parser.add_argument("--ornaments", type=Path, required=True)
	parser.add_argument("--whale", type=Path, required=True)
	parser.add_argument("--storyboard", type=Path, required=True)
	parser.add_argument("--repo-root", type=Path, default=Path.cwd())
	parser.add_argument(
		"--chroma-helper",
		type=Path,
		default=(
			Path.home()
			/ ".codex"
			/ "skills"
			/ ".system"
			/ "imagegen"
			/ "scripts"
			/ "remove_chroma_key.py"
		),
	)
	return parser


def main() -> None:
	args = _build_parser().parse_args()
	root = args.repo_root.resolve()
	runtime_dir = root / "assets" / "castle" / "pool_2d"
	source_dir = root / "assets_src" / "concepts" / "roshan_pool_2d"

	_process_transparent_atlas(
		args.ornaments,
		source_dir / "poolside_ornaments_atlas_chroma_2026-07-22.png",
		runtime_dir / "poolside_ornaments_atlas.png",
		4,
		3,
		args.chroma_helper,
	)
	_process_transparent_atlas(
		args.whale,
		source_dir / "whale_states_atlas_chroma_2026-07-22.png",
		runtime_dir / "whale_states_atlas.png",
		4,
		2,
		args.chroma_helper,
	)

	_normalize_source(
		args.storyboard,
		source_dir / "whale_rescue_storyboard_2026-07-22.png",
		(3 * CELL_SIZE, 3 * CELL_SIZE),
	)
	story_atlas = _rebuild_grid(
		args.storyboard,
		3,
		3,
		background=(255, 255, 255),
	)
	story_atlas.save(
		runtime_dir / "whale_rescue_storyboard.png",
		format="PNG",
		optimize=True,
	)


if __name__ == "__main__":
	main()
