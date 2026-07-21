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

SHRUB_SHEET = SOURCE / "sky_lagoon_pnw_shrub_variants_flat_2026-07-21.png"
SHRUB_NAMES = (
	"salal_a",
	"salal_b",
	"oregon_grape_a",
	"oregon_grape_b",
	"red_flowering_currant_a",
	"red_flowering_currant_b",
	"oceanspray_a",
	"oceanspray_b",
	"salmonberry_a",
	"salmonberry_b",
	"trailing_blackberry_a",
	"trailing_blackberry_b",
)

STALE_SHRUB_CARDS = (
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
		prefix: str, row_edges: tuple[int, ...] | None = None,
		column_edges: tuple[int, ...] | None = None) -> None:
	with Image.open(sheet_path) as source:
		if row_edges is None:
			row_edges = tuple(round(row * source.height / rows)
				for row in range(rows + 1))
		if column_edges is None:
			column_edges = tuple(round(column * source.width / columns)
				for column in range(columns + 1))
		if len(row_edges) != rows + 1 or row_edges[0] != 0 or row_edges[-1] != source.height:
			raise ValueError(f"Invalid row edges for {sheet_path.name}: {row_edges}")
		if (len(column_edges) != columns + 1 or column_edges[0] != 0
				or column_edges[-1] != source.width):
			raise ValueError(f"Invalid column edges for {sheet_path.name}: {column_edges}")
		for index, name in enumerate(names):
			row, column = divmod(index, columns)
			box = (
				column_edges[column],
				row_edges[row],
				column_edges[column + 1],
				row_edges[row + 1],
			)
			card = source.crop(box)
			card.save(OUTPUT / f"lagoon_{prefix}_{name}.png", optimize=True)


def main() -> None:
	OUTPUT.mkdir(parents=True, exist_ok=True)
	normalize_sheet(TREE_SHEET)
	normalize_sheet(SHRUB_SHEET)
	for stale_name in STALE_SHRUB_CARDS:
		stale_path = OUTPUT / f"lagoon_shrub_{stale_name}.png"
		stale_path.unlink(missing_ok=True)
	# The generated tree gallery has clean but intentionally unequal row gaps.
	# These boundaries preserve every planted base without neighboring artifacts.
	slice_sheet(TREE_SHEET, TREE_NAMES, 4, 3, "tree", (0, 377, 671, 1024),
		(0, 256, 512, 779, 1024))
	# The portrait variant gallery also uses unequal row spacing. Split through
	# the measured navy gaps so every base stays complete and isolated.
	slice_sheet(SHRUB_SHEET, SHRUB_NAMES, 2, 6, "shrub",
		(0, 190, 364, 533, 690, 845, 1024))
	print(f"SKY_LAGOON_PNW_FLAT|trees={len(TREE_NAMES)}|shrubs={len(SHRUB_NAMES)}")


if __name__ == "__main__":
	main()
