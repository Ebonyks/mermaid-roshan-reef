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

The same command also audits the twelve standalone Sky Lagoon playground
poses.  Those cutouts do not use the atlas-window table, so they need their
own edge-margin and disconnected-fragment checks.

SCOPE: this tool measures the art and the table's INTENT. It cannot see how
Sprite3D consumes the table -- that blind spot is what shipped an invisible
Roshan on 2026-08-02 (audit section 8). The engine-side half is asserted by
probe_castle_pearl_art (roshan_frames_sample_their_own_window) and probe_l2.
"""

from __future__ import annotations

import argparse
import hashlib
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
PLAYGROUND_ROOT = ROOT / "assets" / "sprites" / "sky_lagoon" / "roshan_playground"
PROMENADE_GD = ROOT / "scripts" / "arena" / "sky_lagoon_promenade.gd"

CELL = 256
ALPHA = 8
MIN_BLOB = 60
SEARCH = 80
# ghost pixels (another frame's art leaking in) cost double a lost own pixel,
# so the search prefers a window that both keeps her whole and stays clean
GHOST_WEIGHT = 2
PLAYGROUND_ALPHA = 8
PLAYGROUND_MIN_COMPONENT = 16

PLAYGROUND_FRAMES = {
	"roshan_swing_0.png": 1,
	"roshan_swing_1.png": 1,
	"roshan_swing_2_v2.png": 8,
	"roshan_swing_3_v2.png": 8,
	"roshan_slide_0.png": 1,
	"roshan_slide_1.png": 1,
	"roshan_slide_2_v2.png": 8,
	"roshan_slide_3_v2.png": 8,
	"roshan_seesaw_0.png": 1,
	"roshan_seesaw_1.png": 1,
	"roshan_seesaw_2.png": 1,
	"roshan_seesaw_3.png": 1,
}
SUPERSEDED_PLAYGROUND_FRAMES = {
	"roshan_swing_2.png",
	"roshan_swing_3.png",
	"roshan_slide_2.png",
	"roshan_slide_3.png",
}
PLAYGROUND_REVIEWED_HASHES = {
	"roshan_slide_2_v2.png": "cb6cd27d5357bb59542bbdf95ef3fbf751759ce07046ea3607ec449c6a5d9613",
	"roshan_slide_3_v2.png": "8ec11afaf899b21548e4fdeeabc945cb90f5b62e6410a6319afaf22834e03271",
	"roshan_swing_2_v2.png": "211868892df1963e70300f71a02eb076b401d0af2dc2549ac229806cb99b7598",
	"roshan_swing_3_v2.png": "07cf65c0cc32189ca704a321e08ed9f90a6db04c666f6f086d4e8f99f33eb4be",
}

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


def inspect_playground_frame(path: Path, min_margin: int) -> list[str]:
	"""Return production defects for one standalone 512px action cutout."""
	failures: list[str] = []
	if not path.is_file():
		return [f"missing {path.name}"]
	with Image.open(path) as source:
		if source.size != (512, 512):
			failures.append(f"{path.name}: expected 512x512, got {source.size[0]}x{source.size[1]}")
		if "A" not in source.getbands():
			failures.append(f"{path.name}: missing alpha channel")
		alpha = np.array(source.convert("RGBA"))[:, :, 3]
	mask = alpha > PLAYGROUND_ALPHA
	if not mask.any():
		failures.append(f"{path.name}: empty alpha silhouette")
		return failures

	ys, xs = np.where(mask)
	margins = (
		int(xs.min()),
		int(ys.min()),
		int(mask.shape[1] - 1 - xs.max()),
		int(mask.shape[0] - 1 - ys.max()),
	)
	if min(margins) < min_margin:
		failures.append(
			f"{path.name}: silhouette margins L/T/R/B={margins}, "
			f"minimum is {min_margin}px"
		)

	labels, count = ndimage.label(mask)
	components = sorted(
		(int((labels == label).sum()), label)
		for label in range(1, count + 1)
		if int((labels == label).sum()) >= PLAYGROUND_MIN_COMPONENT
	)
	if len(components) > 1:
		sizes = sorted((size for size, _label in components), reverse=True)
		failures.append(
			f"{path.name}: {len(components)} disconnected visible components "
			f"({sizes} pixels); expected one complete Roshan silhouette"
		)
	return failures


def audit_playground_frames(root: Path = PLAYGROUND_ROOT) -> list[str]:
	"""Bind the runtime roster to the reviewed, unclipped standalone frames."""
	failures: list[str] = []
	for name, min_margin in PLAYGROUND_FRAMES.items():
		path = root / name
		failures.extend(inspect_playground_frame(path, min_margin))
		if path.is_file() and name in PLAYGROUND_REVIEWED_HASHES:
			digest = hashlib.sha256(path.read_bytes()).hexdigest()
			if digest != PLAYGROUND_REVIEWED_HASHES[name]:
				failures.append(
					f"{name}: reviewed pixel hash changed; expected "
					f"{PLAYGROUND_REVIEWED_HASHES[name]}, got {digest}"
				)
		if root == PLAYGROUND_ROOT:
			sidecar = Path(str(path) + ".import")
			if not sidecar.is_file():
				failures.append(f"{name}: missing Godot import sidecar")
			elif "compress/mode=2" not in sidecar.read_text(encoding="utf-8"):
				failures.append(f"{name}: 512px POT cutout is not VRAM compressed")
	for name in sorted(SUPERSEDED_PLAYGROUND_FRAMES):
		if (root / name).exists():
			failures.append(f"superseded clipped playground frame still active: {name}")

	if root == PLAYGROUND_ROOT:
		text = PROMENADE_GD.read_text(encoding="utf-8")
		block = text.split("const PLAY_FRAME_PATHS := {", 1)[1].split(
			"const PLAY_DURATIONS", 1
		)[0]
		shipped_names = {
			Path(value).name
			for value in re.findall(
				r'"res://assets/sprites/sky_lagoon/roshan_playground/([^\"]+\.png)"',
				block,
			)
		}
		expected_names = set(PLAYGROUND_FRAMES)
		if shipped_names != expected_names:
			failures.append(
				"PLAY_FRAME_PATHS roster mismatch: missing=%s extra=%s"
				% (
					sorted(expected_names - shipped_names),
					sorted(shipped_names - expected_names),
				)
			)
	return failures


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
	playground_failures = audit_playground_frames()
	if playground_failures:
		for line in playground_failures:
			print(f"FAIL playground: {line}")
		failures.extend(playground_failures)
	else:
		print(
			f"playground poses : {len(PLAYGROUND_FRAMES):6} whole, "
			"single-silhouette 512px frames"
		)
	if failures:
		return 1
	print("OK: every Roshan frame renders whole")
	return 0


if __name__ == "__main__":
	sys.exit(main())
