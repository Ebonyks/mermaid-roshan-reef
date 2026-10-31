#!/usr/bin/env python3
"""Measure how Mermaid Roshan's runtime frames and playback code behave.

Numbers only: this script reads committed atlases and scripts and prints or
writes JSON. It never writes an image.

    python -B docs/handoffs/codex_roshan_motion_language_2026-10-04/tools/measure_roshan_motion.py
    python -B .../measure_roshan_motion.py --write   # refresh data/motion_measurements.json

Definitions
- fin side: horizontal offset of the lowest fifth of the opaque figure from
  the top quarter, divided by the cell width. Negative means the fin sits to
  the viewer's left. |value| <= 0.06 is reported as centred.
- ponytail side: centroid of saturated blue or green hair pixels in the top
  third of the figure relative to the head's opaque centroid, divided by the
  figure width. The rainbow ponytail is the only blue/green mass up there.
- silhouette change: 1 - IoU of the alpha masks (alpha > 32) of two cells.
  "raw" compares the cells as stored (what a plain region player shows);
  "aligned" first moves the second mask so the centroids match, isolating
  shape change from drift.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "data" / "motion_measurements.json"
BASE = "assets/characters/roshan_25d/"
CAREERS = "assets/opera/worlds/actors/animation/"
BASE_SHEETS = {
	"roshan_directional.png": (4, 2),
	"roshan_swim_front.png": (4, 4),
	"roshan_swim_back.png": (4, 4),
	"roshan_gesture_a.png": (4, 4),
	"roshan_gesture_b.png": (4, 4),
	"roshan_gesture_c.png": (4, 4),
	"roshan_gesture_d.png": (4, 2),
	"roshan_play_a.png": (4, 4),
	"roshan_play_b.png": (4, 4),
	"roshan_base.png": (1, 1),
}
CAREER_ROWS = ["idle", "travel", "work", "cheer"]
GESTURE_ROWS = {
	"wave": ("roshan_gesture_a.png", 0), "cheer": ("roshan_gesture_a.png", 1),
	"clap": ("roshan_gesture_a.png", 2), "twirl": ("roshan_gesture_a.png", 3),
	"look": ("roshan_gesture_b.png", 0), "giggle": ("roshan_gesture_b.png", 1),
	"sleep": ("roshan_gesture_b.png", 2), "point": ("roshan_gesture_b.png", 3),
	"collect": ("roshan_gesture_c.png", 0), "boing": ("roshan_gesture_c.png", 1),
	"hairtwirl": ("roshan_gesture_c.png", 2), "hum": ("roshan_gesture_c.png", 3),
	"flop": ("roshan_gesture_d.png", 0), "carry": ("roshan_gesture_d.png", 1),
}
SCRIPTS = [
	"scripts/player.gd", "scripts/roshan_sprite_loop.gd",
	"scripts/sprite_transition_2d.gd", "scripts/opera_roshan_actor.gd",
	"scripts/arena/castle_rooms_25d.gd", "scripts/day_one_contact_action_2d.gd",
	"scripts/arena/sky_lagoon_layout.json",
]


def sha256(rel: str) -> str:
	return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def cells(rel: str, cols: int, rows: int) -> list[list[np.ndarray]]:
	img = np.asarray(Image.open(ROOT / rel).convert("RGBA"))
	h, w = img.shape[:2]
	ch, cw = h // rows, w // cols
	return [[img[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] for c in range(cols)]
		for r in range(rows)]


def fin_side(cell: np.ndarray) -> float | None:
	alpha = cell[:, :, 3] > 32
	ys, _ = np.nonzero(alpha)
	if ys.size == 0:
		return None
	y0, y1 = int(ys.min()), int(ys.max())
	height = y1 - y0 + 1
	top = np.nonzero(alpha[y0:y0 + height // 4])[1]
	bottom = np.nonzero(alpha[y1 - height // 5:y1 + 1])[1]
	return round(float((bottom.mean() - top.mean()) / cell.shape[1]), 3)


def ponytail_side(cell: np.ndarray) -> float | None:
	rgba = cell.astype(float) / 255.0
	alpha = rgba[:, :, 3] > 0.5
	ys, xs = np.nonzero(alpha)
	if ys.size == 0:
		return None
	y0, y1 = int(ys.min()), int(ys.max())
	band = slice(y0, y0 + int((y1 - y0) * 0.33))
	r, g, b = rgba[band, :, 0], rgba[band, :, 1], rgba[band, :, 2]
	hi = np.maximum(np.maximum(r, g), b)
	lo = np.minimum(np.minimum(r, g), b)
	sat = (hi - lo) / np.maximum(hi, 1e-6)
	streak = (((b > r + 0.08) & (b > g - 0.02)) | ((g > r) & (g > b + 0.1)))
	streak &= (sat > 0.35) & alpha[band]
	if streak.sum() < 30:
		return None
	head_x = np.nonzero(alpha[band])[1].mean()
	width = max(int(xs.max() - xs.min()), 1)
	return round(float((np.nonzero(streak)[1].mean() - head_x) / width), 3)


def side_label(value: float | None, tolerance: float) -> str:
	if value is None:
		return "?"
	return "L" if value < -tolerance else "R" if value > tolerance else "C"


def change(a: np.ndarray, b: np.ndarray, aligned: bool) -> float:
	m1, m2 = a[:, :, 3] > 32, b[:, :, 3] > 32
	if aligned:
		y1, x1 = np.nonzero(m1)
		y2, x2 = np.nonzero(m2)
		if y1.size and y2.size:
			dy = int(round(y1.mean() - y2.mean()))
			dx = int(round(x1.mean() - x2.mean()))
			pad = 128
			big = np.zeros((m2.shape[0] + 2 * pad, m2.shape[1] + 2 * pad), bool)
			big[pad + dy:pad + dy + m2.shape[0], pad + dx:pad + dx + m2.shape[1]] = m2
			m2 = big[pad:pad + m2.shape[0], pad:pad + m2.shape[1]]
	union = np.logical_or(m1, m2).sum()
	return round(float(1.0 - np.logical_and(m1, m2).sum() / union) * 100.0, 1) if union else 0.0


def summary(values: list[float]) -> dict:
	ordered = sorted(values)
	return {"n": len(ordered), "min": ordered[0], "median": ordered[len(ordered) // 2],
		"max": ordered[-1]}


def measure_base() -> dict:
	result = {}
	for name, (cols, rows) in BASE_SHEETS.items():
		grid = cells(BASE + name, cols, rows)
		flat = [cell for row in grid for cell in row]
		entry = {
			"sha256": sha256(BASE + name),
			"grid": [cols, rows],
			"fin_side": [[fin_side(c) for c in row] for row in grid],
			"fin_side_label": [" ".join(side_label(fin_side(c), 0.06) for c in row) for row in grid],
			"ponytail_side_label": [" ".join(side_label(ponytail_side(c), 0.05) for c in row) for row in grid],
		}
		if name.startswith("roshan_swim_"):
			ring = [(flat[i], flat[(i + 1) % len(flat)]) for i in range(len(flat))]
			entry["cycle_change_raw"] = summary([change(a, b, False) for a, b in ring])
			entry["cycle_change_aligned"] = summary([change(a, b, True) for a, b in ring])
		elif len(flat) > 1 and name != "roshan_directional.png":
			pairs = [(row[i], row[i + 1]) for row in grid for i in range(len(row) - 1)]
			entry["row_change_aligned"] = summary([change(a, b, True) for a, b in pairs])
		result[name] = entry
	return result


def measure_careers() -> dict:
	rows_out, maxima = {}, []
	aligned_all = []
	for path in sorted((ROOT / CAREERS).glob("roshan_*_sheet_a.png")):
		rel = path.relative_to(ROOT).as_posix()
		career = path.name[len("roshan_"):-len("_sheet_a.png")]
		grid = cells(rel, 4, 4)
		per_row = {}
		for r, row_name in enumerate(CAREER_ROWS):
			raw = [change(grid[r][i], grid[r][(i + 1) % 4], False) for i in range(4)]
			aligned_all += [change(grid[r][i], grid[r][(i + 1) % 4], True) for i in range(4)]
			per_row[row_name] = raw
			maxima.append(max(raw))
		rows_out[career] = {"sha256": sha256(rel), "adjacent_change_raw_with_wrap": per_row}
	return {
		"careers": rows_out,
		"rows": len(maxima),
		"rows_max_raw_at_least_40": sum(1 for v in maxima if v >= 40.0),
		"rows_max_raw_at_least_25": sum(1 for v in maxima if v >= 25.0),
		"adjacent_change_aligned_all": summary(aligned_all),
	}


def number(text: str, pattern: str) -> float | None:
	match = re.search(pattern, text, re.S)
	return float(match.group(1)) if match else None


def measure_code() -> dict:
	read = lambda rel: (ROOT / rel).read_text(encoding="utf-8")
	loop, smooth = read("scripts/roshan_sprite_loop.gd"), read("scripts/sprite_transition_2d.gd")
	player, opera = read("scripts/player.gd"), read("scripts/opera_roshan_actor.gd")
	castle, contact = read("scripts/arena/castle_rooms_25d.gd"), read("scripts/day_one_contact_action_2d.gd")
	base_fps = number(loop, r"BASE_SWIM_FPS := ([\d.]+)")
	max_fps = number(loop, r"MAX_FPS := ([\d.]+)")
	multiplier = number(loop, r"SMOOTHNESS_MULTIPLIER := (\d+)")
	cap = number(smooth, r"MAX_TRANSITION_SECONDS := ([\d.]+)")
	blend = {}
	for label, fps in (("base_fps", base_fps), ("max_fps", max_fps)):
		if fps and multiplier and cap:
			interval = 1.0 / fps
			duration = min(interval * (multiplier - 1) / multiplier, cap)
			blend[label] = {"fps": fps, "blend_seconds": round(duration, 4),
				"share_of_interval_with_two_copies": round(duration / interval, 3)}
	verbs = {k: float(v) for k, v in re.findall(r'"(\w+)": \{"len": ([\d.]+)\}', player)}
	keys = number(player, r"ROSHAN_25D_KEYFRAMES := (\d+)")
	opera_fps = {k: float(v) for k, v in re.findall(
		r'"(idle|travel|work|cheer)": ([\d.]+),', opera.split("const BALLERINA")[0])}
	sky = json.loads(read("scripts/arena/sky_lagoon_layout.json")).get("roshan_route", {})
	region = re.search(r"pose\.region = Rect2\(([\d.]+), ([\d.]+), 256\.0, 256\.0\)", contact)
	return {
		"castle_swim_loop": {
			"base_fps": base_fps, "max_fps": max_fps,
			"idle_breath_px": number(loop, r"IDLE_BREATH_PIXELS := ([\d.]+)"),
			"crossfade_multiplier": multiplier, "crossfade_cap_seconds": cap,
			"crossfade": blend,
		},
		"castle_idle_rotation_tween": {
			"radians": number(castle, r'"rotation", -([\d.]+),\s*\n?\s*([\d.]+)\)'),
			"seconds_per_half": number(castle, r'"rotation", -[\d.]+,\s*\n?\s*([\d.]+)\)'),
		},
		"player_gestures": {
			"keys_per_gesture": keys,
			"seconds_per_key": {k: round(v / keys, 3) for k, v in sorted(verbs.items())} if keys else {},
			"twirl_flips_mid_spin": "spin_flip: bool = spin_u >= 0.5" in player,
			"idle_directional_unflipped": '"directional", _classic_direction_frame(view_angle), false)' in player,
			"gesture_uses_view_flip": "_set_classic_sequence(ROSHAN_25D_GESTURES[verb] as Array, verb_phase, flip)" in player,
		},
		"opera_actor_fps": opera_fps,
		"day_one_contact_action": {
			"static_directional_frame": int(float(region.group(1)) // 256) if region else None,
			"move_px_per_second": number(contact, r"delta, 0\.0\) \* ([\d.]+) \* unit_scale"),
			"contact_seconds": number(contact, r"work_time >= ([\d.]+)"),
		},
		"sky_lagoon_route": {"medium": sky.get("medium"), "directional_frame": sky.get("frame")},
	}


def gesture_entry_swaps(base: dict) -> dict:
	"""Fin side the child sees when the legacy player enters a gesture.

	player.gd draws idle directional frames unflipped and draws gesture rows
	with the view flip. Near the camera the idle heading is frame 0/1 with
	flip false, or frame 7 with flip true (view_angle > 0.15).
	"""
	directional = base["roshan_directional.png"]["fin_side"]
	idle = {0: directional[0][0], 1: directional[0][1], 7: directional[1][3]}
	swim_front = [v for row in base["roshan_swim_front.png"]["fin_side"] for v in row]
	out = {}
	for verb, (sheet, row) in GESTURE_ROWS.items():
		grid = base[sheet]["fin_side"]
		first = grid[row][0]
		out[verb] = {
			"gesture_first_frame_fin": first,
			"vs_idle_frame0_unflipped": side_label(idle[0], 0.06) + "->" + side_label(first, 0.06),
			"vs_idle_frame7_flipped": side_label(idle[7], 0.06) + "->" + side_label(-first, 0.06),
			"vs_swim_same_flip": side_label(float(np.median(swim_front)), 0.06) + "->" + side_label(first, 0.06),
		}
	return out


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
	parser.add_argument("--write", action="store_true", help="write data/motion_measurements.json")
	args = parser.parse_args()
	base = measure_base()
	head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
		text=True, check=False).stdout.strip()
	data = {
		"schema": "reef.roshan-motion-measurements.v1",
		"source_head": head,
		"numbers_only": True,
		"base_world": base,
		"gesture_entry_fin_side": gesture_entry_swaps(base),
		"career_atlases": measure_careers(),
		"code": measure_code(),
		"script_sha256": {rel: sha256(rel) for rel in SCRIPTS},
	}
	text = json.dumps(data, indent=1, sort_keys=False) + "\n"
	if args.write:
		OUT.parent.mkdir(parents=True, exist_ok=True)
		OUT.write_text(text, encoding="utf-8", newline="\n")
		print(f"wrote {OUT.relative_to(ROOT).as_posix()}")
	else:
		sys.stdout.write(text)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
