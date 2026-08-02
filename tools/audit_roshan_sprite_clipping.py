#!/usr/bin/env python3
"""Prove that no Mermaid Roshan 2.5D frame renders with her art cut off.

The generated sheets pack their figures on a ~236-250px pitch instead of the
nominal 256px cell pitch, so a plain hframes/vframes slice clips the top of her
head in the lower rows and leaks the next row's head in as a sliver. The
runtime compensates with the per-frame window table in
scripts/roshan_sprite_frames.gd; this tool measures the actual art and checks
that table still holds.

    python3 tools/audit_roshan_sprite_clipping.py              # audit, exit 1 on clipping
    python3 tools/audit_roshan_sprite_clipping.py --emit-table # regenerate the GDScript table
    python3 tools/audit_roshan_sprite_clipping.py --contact    # write a before/after contact sheet

Run this after ANY regeneration of the sheets in assets/characters/roshan_25d/:
new art means new packing, which means the table must be re-emitted.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SHEET_ROOT = ROOT / "assets" / "characters" / "roshan_25d"
TABLE_GD = ROOT / "scripts" / "roshan_sprite_frames.gd"
CONTACT = ROOT / "audit" / "roshan_sprite" / "roshan_frame_windows.png"

CELL = 256
ALPHA = 8
MIN_BLOB = 60
SEARCH = 80
# ghost pixels (another frame's art leaking in) cost double a lost own pixel,
# so the search prefers a window that both keeps her whole and stays clean
GHOST_WEIGHT = 2

SHEETS = {
	"directional": ("roshan_directional.png", 4, 2),
	"swim_front": ("roshan_swim_front.png", 4, 4),
	"swim_back": ("roshan_swim_back.png", 4, 4),
	"gesture_a": ("roshan_gesture_a.png", 4, 4),
	"gesture_b": ("roshan_gesture_b.png", 4, 4),
	"gesture_c": ("roshan_gesture_c.png", 4, 4),
	"gesture_d": ("roshan_gesture_d.png", 4, 2),
	"play_a": ("roshan_play_a.png", 4, 4),
	"play_b": ("roshan_play_b.png", 4, 4),
}


def ownership_map(alpha: np.ndarray, cols: int, rows: int) -> np.ndarray:
	"""Label every lit pixel with the 1-based frame index that owns it.

	Ownership is by blob centroid: a figure that drifts across a cell seam still
	belongs to the frame it was painted for.
	"""
	mask = alpha > ALPHA
	labels, count = ndimage.label(ndimage.binary_dilation(mask, iterations=3))
	labels = labels * mask
	owners = np.zeros_like(labels)
	for label in range(1, count + 1):
		ys, xs = np.where(labels == label)
		if len(ys) < MIN_BLOB:
			continue
		row = min(int(ys.mean()) // CELL, rows - 1)
		col = min(int(xs.mean()) // CELL, cols - 1)
		owners[labels == label] = row * cols + col + 1
	return owners


def summed_area(mask: np.ndarray) -> np.ndarray:
	return np.pad(np.cumsum(np.cumsum(mask.astype(np.int64), 0), 1), ((1, 0), (1, 0)))


def window_sum(table: np.ndarray, x: int, y: int, size: int = CELL) -> int:
	return int(
		table[y + size, x + size] - table[y, x + size] - table[y + size, x] + table[y, x]
	)


def measure(sheet_key: str) -> list[dict]:
	name, cols, rows = SHEETS[sheet_key]
	alpha = np.array(Image.open(SHEET_ROOT / name).convert("RGBA"))[:, :, 3]
	height, width = alpha.shape
	owners = ownership_map(alpha, cols, rows)
	out: list[dict] = []
	for index in range(cols * rows):
		ox, oy = (index % cols) * CELL, (index // cols) * CELL
		own = owners == index + 1
		total = int(own.sum())
		if total == 0:
			out.append({"i": index, "empty": True, "best": (0, 0)})
			continue
		alien = (owners > 0) & (~own)
		s_own, s_alien = summed_area(own), summed_area(alien)

		# bind the per-frame state as defaults: the closure outlives this loop.
		# Returns None for a window that would fall off the texture.
		def score(sx: int, sy: int, ox=ox, oy=oy, total=total,
				s_own=s_own, s_alien=s_alien):
			x0, y0 = ox + sx, oy + sy
			if x0 < 0 or y0 < 0 or x0 + CELL > width or y0 + CELL > height:
				return None
			return total - window_sum(s_own, x0, y0), window_sum(s_alien, x0, y0)

		best = None
		for sy in range(-SEARCH, SEARCH + 1):
			for sx in range(-SEARCH, SEARCH + 1):
				got = score(sx, sy)
				if got is None:
					continue
				lost, ghost = got
				rank = (lost + GHOST_WEIGHT * ghost, lost, ghost, abs(sx) + abs(sy))
				if best is None or rank < best[0]:
					best = (rank, (sx, sy), lost, ghost)
		naive = score(0, 0)
		out.append(
			{
				"i": index,
				"total": total,
				"naive_lost": naive[0],
				"naive_ghost": naive[1],
				"best": best[1],
				"best_lost": best[2],
				"best_ghost": best[3],
				"score": score,
			}
		)
	return out


def shipped_table() -> dict[str, list[tuple[int, int]]]:
	"""Parse the SHIFTS table the runtime actually ships."""
	text = TABLE_GD.read_text(encoding="utf-8")
	body = text.split("const SHIFTS := {", 1)[1]
	table: dict[str, list[tuple[int, int]]] = {}
	for key, block in re.findall(r'"(\w+)":\s*\[(.*?)\n\t\],', body, re.S):
		table[key] = [
			(int(a), int(b))
			for a, b in re.findall(r"Vector2\((-?\d+),\s*(-?\d+)\)", block)
		]
	return table


def emit_table(measured: dict[str, list[dict]]) -> str:
	lines = ["const SHIFTS := {"]
	for key in SHEETS:
		lines.append('\t"%s": [' % key)
		shifts = [f["best"] for f in measured[key]]
		for start in range(0, len(shifts), 4):
			row = ", ".join(f"Vector2({x}, {y})" for x, y in shifts[start : start + 4])
			lines.append(f"\t\t{row},")
		lines.append("\t],")
	lines.append("}")
	return "\n".join(lines)


def contact_sheet(measured: dict[str, list[dict]]) -> None:
	"""Red = art the naive grid throws away, green = art the fix recovers."""
	CONTACT.parent.mkdir(parents=True, exist_ok=True)
	tiles = []
	for key, (name, cols, rows) in SHEETS.items():
		img = Image.open(SHEET_ROOT / name).convert("RGBA")
		alpha = np.array(img)[:, :, 3]
		owners = ownership_map(alpha, cols, rows)
		rgba = np.array(img)
		for frame in measured[key]:
			if frame.get("empty"):
				continue
			index = frame["i"]
			ox, oy = (index % cols) * CELL, (index // cols) * CELL
			own = owners == index + 1
			naive = np.zeros_like(own)
			naive[oy : oy + CELL, ox : ox + CELL] = True
			sx, sy = frame["best"]
			fixed = np.zeros_like(own)
			fixed[oy + sy : oy + sy + CELL, ox + sx : ox + sx + CELL] = True
			lost = own & ~naive
			rgba[lost] = [255, 40, 40, 255]
			rgba[own & ~fixed] = [255, 0, 255, 255]
			recovered = lost & fixed
			rgba[recovered] = [40, 230, 90, 255]
		tile = Image.fromarray(rgba, "RGBA").resize((512, 512 * rows // 4 or 256))
		tiles.append((key, tile))
	cols_n = 3
	rows_n = (len(tiles) + cols_n - 1) // cols_n
	sheet = Image.new("RGBA", (cols_n * 520, rows_n * 540), (24, 22, 38, 255))
	for i, (key, tile) in enumerate(tiles):
		sheet.paste(tile, ((i % cols_n) * 520 + 4, (i // cols_n) * 540 + 4), tile)
	sheet.save(CONTACT)
	print(f"contact sheet -> {CONTACT.relative_to(ROOT)}")


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--emit-table", action="store_true")
	parser.add_argument("--contact", action="store_true")
	args = parser.parse_args()

	measured = {key: measure(key) for key in SHEETS}

	if args.emit_table:
		print(emit_table(measured))
		return 0
	if args.contact:
		contact_sheet(measured)

	shipped = shipped_table()
	failures: list[str] = []
	naive_lost = naive_ghost = ship_lost = ship_ghost = total = 0

	for key in SHEETS:
		frames = measured[key]
		table = shipped.get(key)
		if table is None:
			failures.append(f"FAIL {key}: no SHIFTS entry in roshan_sprite_frames.gd")
			continue
		if len(table) != len(frames):
			failures.append(
				f"FAIL {key}: SHIFTS has {len(table)} frames, sheet has {len(frames)}"
			)
			continue
		for frame in frames:
			if frame.get("empty"):
				continue
			total += frame["total"]
			naive_lost += frame["naive_lost"]
			naive_ghost += frame["naive_ghost"]
			shipped_score = frame["score"](*table[frame["i"]])
			if shipped_score is None:
				failures.append(
					f"FAIL {key}[{frame['i']}]: shipped window {table[frame['i']]} "
					"falls off the texture"
				)
				continue
			lost, ghost = shipped_score
			ship_lost += lost
			ship_ghost += ghost
			if lost > 0:
				failures.append(
					f"FAIL {key}[{frame['i']}]: shipped window clips {lost}px of Roshan "
					f"({100.0 * lost / frame['total']:.2f}% of the figure); "
					f"best window is {table[frame['i']]} -> {frame['best']}"
				)

	print(f"naive 256px grid : {naive_lost:6} px of Roshan clipped, {naive_ghost:6} px ghost")
	print(f"shipped windows  : {ship_lost:6} px of Roshan clipped, {ship_ghost:6} px ghost")
	if total:
		print(f"                   ({100.0 * naive_lost / total:.2f}% -> "
			f"{100.0 * ship_lost / total:.2f}% of her art lost)")
	for line in failures:
		print(line)
	if failures:
		return 1
	print("OK: every Roshan frame renders whole")
	return 0


if __name__ == "__main__":
	sys.exit(main())
