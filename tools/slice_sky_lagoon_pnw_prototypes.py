#!/usr/bin/env python3
"""Slice the accepted flat PNW prototype sheets into named reference cards."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "concepts"
OUTPUT = SOURCE / "sky_lagoon_pnw_flat"

TREE_SHEET = SOURCE / "sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png"
TREE_NAMES = (
	"douglas_fir",
	"western_redcedar",
	"western_hemlock",
	"sitka_spruce",
	"shore_pine",
	"pacific_yew",
	"bigleaf_maple",
	"red_alder",
	"black_cottonwood",
	"pacific_madrone",
	"garry_oak",
	"pacific_dogwood",
)

SHRUB_SHEET = SOURCE / "sky_lagoon_pnw_shrub_prototypes_flat_2026-07-21.png"
SHRUB_NAMES = (
	"salal",
	"oregon_grape",
	"red_flowering_currant",
	"oceanspray",
	"salmonberry",
	"evergreen_huckleberry",
)


def normalize_sheet(sheet_path: Path) -> None:
	"""Keep review art inside the repository's 1024px texture ceiling."""
	with Image.open(sheet_path) as source:
		if max(source.size) <= 1024:
			return
		scale = 1024.0 / max(source.size)
		size = (round(source.width * scale), round(source.height * scale))
		normalized = source.resize(size, Image.Resampling.LANCZOS)
		normalized.save(sheet_path, optimize=True)


def slice_sheet(sheet_path: Path, names: tuple[str, ...], columns: int, rows: int,
		prefix: str, row_edges: tuple[int, ...] | None = None) -> None:
	with Image.open(sheet_path) as source:
		if row_edges is None:
			row_edges = tuple(round(row * source.height / rows)
				for row in range(rows + 1))
		if len(row_edges) != rows + 1 or row_edges[0] != 0 or row_edges[-1] != source.height:
			raise ValueError(f"Invalid row edges for {sheet_path.name}: {row_edges}")
		for index, name in enumerate(names):
			row, column = divmod(index, columns)
			box = (
				round(column * source.width / columns),
				row_edges[row],
				round((column + 1) * source.width / columns),
				row_edges[row + 1],
			)
			card = source.crop(box)
			card.save(OUTPUT / f"lagoon_{prefix}_{name}.png", optimize=True)


def main() -> None:
	OUTPUT.mkdir(parents=True, exist_ok=True)
	normalize_sheet(TREE_SHEET)
	normalize_sheet(SHRUB_SHEET)
	# The generated tree gallery has clean but intentionally unequal row gaps.
	# These boundaries preserve every planted base without neighboring artifacts.
	slice_sheet(TREE_SHEET, TREE_NAMES, 4, 3, "tree", (0, 371, 661, 1024))
	slice_sheet(SHRUB_SHEET, SHRUB_NAMES, 3, 2, "shrub")
	print(f"SKY_LAGOON_PNW_FLAT|trees={len(TREE_NAMES)}|shrubs={len(SHRUB_NAMES)}")


if __name__ == "__main__":
	main()
