#!/usr/bin/env python3
"""Review-only seed measurement of the painted Main Hall doorways.

Reads the approved Main Hall master tiles (8x2 grid of 910x1024 RGB PNGs under
assets/flats/castle/main_hall_redraw_2026-08-03/tiles/), scans outward from each
HALL_PORTALS centre line for the warm cream/gold frame, and writes per-door
opening/frame measurements in hall-art logical units (3344x941) plus a contact
sheet overlay. Deterministic; needs Pillow and numpy; run from the repo root:

    python3 audit/door_highlight_rewrite_2026-09-30/measure_hall_door_geometry.py

This is diagnostic seed data for CODEX_DOOR_HIGHLIGHT_REWRITE_HANDOFF_2026-09-30.md.
It is not runtime evidence and it changes no project asset. The seven standard
arched doors measure cleanly; Opera Hall and Royal Hall curtains/columns defeat
the colour scan and are marked LOW confidence for a manual re-trace.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TILES = ROOT / "assets/flats/castle/main_hall_redraw_2026-08-03/tiles"
NATIVE = (7280, 2048)
LOGICAL = (3344.0, 941.0)
KX = NATIVE[0] / LOGICAL[0]
KY = NATIVE[1] / LOGICAL[1]
# Copied from scripts/arena/castle_rooms_25d.gd HALL_PORTALS at dev e7899cc0.
PORTALS = {
	"family_gallery": (210, 300, 160, 305), "library": (380, 300, 160, 305),
	"kitchen": (545, 300, 160, 305), "opera_hall": (875, 180, 300, 425),
	"playroom": (1940, 300, 160, 305), "craft_room": (2140, 300, 160, 305),
	"mermaid_pool": (2340, 300, 160, 305), "bubble_bath": (2540, 300, 160, 305),
	"__royal_hall": (2870, 150, 350, 470),
}
LOW_CONFIDENCE = {"opera_hall", "__royal_hall"}
THRESHOLD_Y = {"__royal_hall": 470.0}  # stop at the top stair; stairs are warm
# Copied from scripts/arena/fairy_conservatory_door_2d.gd at dev e7899cc0.
GATE = ROOT / "assets/flats/castle/fairy_conservatory/butterfly_gate_available.png"
GATE_SCALE = 0.5372  # AVAILABLE_ART_SCALE
GATE_CENTER = (1672.0, 620.0 - (992.0 - 512.0) * GATE_SCALE)  # AVAILABLE_CENTER
GATE_TOUCH_RECT = (1396.0, 142.0, 552.0, 498.0)  # DOOR_HOTSPOT_RECT


def load_master() -> tuple[Image.Image, dict[str, str]]:
	master = Image.new("RGB", NATIVE)
	hashes: dict[str, str] = {}
	for row in range(2):
		for col in range(8):
			path = TILES / f"main_hall_room_led_r{row}_c{col}.png"
			hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(
				path.read_bytes()).hexdigest()
			master.paste(Image.open(path).convert("RGB"), (col * 910, row * 1024))
	return master, hashes


def first_run(row: np.ndarray, start: int, step: int, limit: int, want: bool,
		minrun: int) -> int | None:
	count = 0
	for i in range(limit):
		x = start + step * i
		if x < 0 or x >= row.shape[0]:
			return None
		if bool(row[x]) == want:
			count += 1
			if count >= minrun:
				return x - step * (minrun - 1)
		else:
			count = 0
	return None


def rdp(points: list[tuple[float, float]], eps: float) -> list[tuple[float, float]]:
	if len(points) < 3:
		return points
	(x1, y1), (x2, y2) = points[0], points[-1]
	den = math.hypot(y2 - y1, x2 - x1) or 1.0
	best, index = 0.0, 0
	for i in range(1, len(points) - 1):
		x0, y0 = points[i]
		d = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / den
		if d > best:
			best, index = d, i
	if best > eps:
		return rdp(points[:index + 1], eps)[:-1] + rdp(points[index:], eps)
	return [points[0], points[-1]]


def measure_gate() -> dict:
	"""Measure the revealed Moonflower gate's painted doorway inside its card.

	The cream doorway frame is found on rows that cross plain water (card y
	600-780, above the lily pads); the opening's vertical extent is read on
	the centre column between the purple reveal bands. Card pixels map to
	hall art through the satellite's own centre and scale.
	"""
	image = Image.open(GATE).convert("RGBA")
	rgba = np.asarray(image).astype(np.int32)
	red, green, blue, alpha = (rgba[..., i] for i in range(4))
	luma = 0.299 * red + 0.587 * green + 0.114 * blue
	spread = rgba[..., :3].max(axis=2) - rgba[..., :3].min(axis=2)
	cream = (alpha > 200) & (luma >= 175) & (red >= blue - 5) & (spread <= 70)
	purple = (alpha > 200) & (blue > red + 25) & (luma < 150)
	centre = 512
	inner_l: list[int] = []
	inner_r: list[int] = []
	outer_l: list[int] = []
	outer_r: list[int] = []
	for yy in range(600, 781, 4):
		row = cream[yy]
		left = first_run(row, centre, -1, 400, True, 4)
		right = first_run(row, centre, 1, 400, True, 4)
		if left is None or right is None:
			continue
		left_out = first_run(row, left, -1, 200, False, 6)
		right_out = first_run(row, right, 1, 200, False, 6)
		if left_out is None or right_out is None:
			continue
		inner_l.append(left)
		inner_r.append(right)
		outer_l.append(left_out)
		outer_r.append(right_out)
	column = purple[:, centre]
	apex = next(yy for yy in range(700, 0, -1) if column[yy])
	# Walk up from below the card's base: the first cream run is the threshold
	# step, and its top edge is the opening's bottom. Scanning down from the
	# water instead would stop on the white lily flowers.
	base = next(yy for yy in range(1020, 700, -1)
		if cream[yy, centre] and cream[yy - 1, centre] and cream[yy - 2, centre])
	threshold = next(yy for yy in range(base, 700, -1)
		if not any(cream[yy - k, centre] for k in range(4))) + 1
	to_x = lambda px: round(GATE_CENTER[0] + (px - 512) * GATE_SCALE, 1)
	to_y = lambda py: round(GATE_CENTER[1] + (py - 512) * GATE_SCALE, 1)
	median = lambda values: sorted(values)[len(values) // 2]
	frame_x = [to_x(median(outer_l)), to_x(median(outer_r))]
	opening_x = [to_x(median(inner_l)), to_x(median(inner_r))]
	result = {
		"confidence": "MEDIUM_VERIFY_IN_OVERLAY",
		"source": GATE.relative_to(ROOT).as_posix(),
		"source_sha256": hashlib.sha256(GATE.read_bytes()).hexdigest(),
		"card_to_hall_art": {"centre": list(GATE_CENTER), "scale": GATE_SCALE},
		"current_touch_rect": list(GATE_TOUCH_RECT),
		"opening_x": opening_x,
		"opening_apex_y": to_y(apex),
		"opening_threshold_y": to_y(threshold),
		"frame_outer_x": frame_x,
		"touch_to_frame_width_ratio": round(
			GATE_TOUCH_RECT[2] / (frame_x[1] - frame_x[0]), 2),
	}
	preview = Image.new("RGBA", image.size, (120, 110, 170, 255))
	preview.alpha_composite(image)
	draw = ImageDraw.Draw(preview)
	card = lambda x, y: ((x - GATE_CENTER[0]) / GATE_SCALE + 512,
		(y - GATE_CENTER[1]) / GATE_SCALE + 512)
	tx, ty, tw, th = GATE_TOUCH_RECT
	draw.rectangle([card(tx, ty), card(tx + tw, ty + th)],
		outline=(255, 255, 0, 255), width=6)
	for x in (median(outer_l), median(outer_r)):
		draw.line([(x, 560), (x, 820)], fill=(255, 0, 255, 255), width=5)
	for x in (median(inner_l), median(inner_r)):
		draw.line([(x, 560), (x, 820)], fill=(0, 255, 0, 255), width=5)
	draw.line([(centre - 60, apex), (centre + 60, apex)], fill=(0, 255, 0, 255), width=5)
	draw.line([(centre - 60, threshold), (centre + 60, threshold)],
		fill=(0, 255, 0, 255), width=5)
	preview.convert("RGB").resize((512, 512), Image.LANCZOS).save(
		OUT / "measured_moonflower_gate_overlay.jpg", quality=90)
	return result


def main() -> None:
	master, tile_hashes = load_master()
	rgb = np.asarray(master).astype(np.int32)
	lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
	warm = ((rgb[..., 0] - rgb[..., 2]) > 8) & (lum > 120)
	doors: dict[str, dict] = {}
	crops: list[Image.Image] = []
	for pid, (x, y, w, h) in PORTALS.items():
		centre = int((x + w / 2) * KX)
		top = int(y * KY)
		bottom = int(THRESHOLD_Y.get(pid, 598.0) * KY)
		inner: list[tuple[int, int, int]] = []
		outer: list[tuple[int, int | None, int | None]] = []
		# Scan upward from the threshold and stop at the arch apex so crest
		# ornaments above the doorway can never be mistaken for the opening.
		for yy in range(bottom, top, -2):
			row = warm[yy]
			if row[centre]:
				break
			left = first_run(row, centre, -1, int(w * KX * 0.7), True, 4)
			right = first_run(row, centre, 1, int(w * KX * 0.7), True, 4)
			if left is None or right is None:
				continue
			left_out = first_run(row, left, -1, int(40 * KX), False, 6)
			right_out = first_run(row, right, 1, int(40 * KX), False, 6)
			inner.append((yy, left, right))
			outer.append((yy, left_out, right_out))
		inner.reverse()
		outer.reverse()
		widths = [r - l for (_, l, r) in inner]
		lower = sorted(widths[len(widths) // 2:])
		median_width = lower[len(lower) // 2]
		spring = next(yy for (yy, l, r) in inner if r - l >= 0.97 * median_width)
		below = [(yy, l, r) for (yy, l, r) in inner if yy >= spring]
		out_l = [lo for (yy, lo, _) in outer if lo is not None and yy >= spring]
		out_r = [ro for (yy, _, ro) in outer if ro is not None and yy >= spring]
		lg = lambda px, py: (round(px / KX, 1), round(py / KY, 1))
		opening = [lg(l, yy) for (yy, l, _) in inner] \
			+ [lg(r, yy) for (yy, _, r) in reversed(inner)]
		opening = rdp(opening, 0.6)
		frame = [lg(lo, yy) for (yy, lo, _) in outer if lo is not None] \
			+ [lg(ro, yy) for (yy, _, ro) in reversed(outer) if ro is not None]
		frame = rdp(frame, 0.6)
		doors[pid] = {
			"confidence": "LOW_RETRACE_REQUIRED" if pid in LOW_CONFIDENCE else "HIGH",
			"current_hotspot_rect": [x, y, w, h],
			"opening_apex_y": round(inner[0][0] / KY, 1),
			"opening_spring_y": round(spring / KY, 1),
			"opening_threshold_y": round(inner[-1][0] / KY, 1),
			"opening_x": [round(float(np.median([l for (_, l, _) in below])) / KX, 1),
				round(float(np.median([r for (_, _, r) in below])) / KX, 1)],
			"frame_outer_x": [round(float(np.median(out_l)) / KX, 1) if out_l else None,
				round(float(np.median(out_r)) / KX, 1) if out_r else None],
			"opening_polygon": [list(p) for p in opening],
			"frame_outer_polyline_below_apex": [list(p) for p in frame],
		}
		pad = 30
		box = (int((x - pad) * KX), int((y - pad) * KY),
			int((x + w + pad) * KX), int((y + h + pad) * KY))
		crop = master.crop(box)
		draw = ImageDraw.Draw(crop)
		draw.rectangle([(x * KX - box[0], y * KY - box[1]),
			((x + w) * KX - box[0], (y + h) * KY - box[1])],
			outline=(255, 255, 0), width=3)
		draw.line([(px * KX - box[0], py * KY - box[1])
			for (px, py) in opening + [opening[0]]], fill=(0, 255, 0), width=4)
		draw.line([(px * KX - box[0], py * KY - box[1])
			for (px, py) in frame], fill=(255, 0, 255), width=3)
		crop.thumbnail((360, 520))
		crops.append(crop)
	sheet = Image.new("RGB", (sum(c.width for c in crops) + 10 * len(crops), max(
		c.height for c in crops)), (20, 20, 30))
	offset = 0
	for crop in crops:
		sheet.paste(crop, (offset, 0))
		offset += crop.width + 10
	sheet.save(OUT / "measured_door_geometry_overlay.jpg", quality=90)
	(OUT / "measured_door_geometry.json").write_text(json.dumps({
		"schema": "door_highlight_review_geometry_v1",
		"status": "REVIEW_SEED_NOT_RUNTIME_EVIDENCE",
		"units": "Main Hall art logical units (HALL_LOGICAL_SIZE 3344x941); stage px = logical * 1280/1672",
		"source_master": "8x2 tiles at 910x1024 composed to 7280x2048; native px = logical * 7280/3344",
		"source_tile_sha256": tile_hashes,
		"method": "centre-line outward scan for warm frame pixels (R-B>8, luma>120); upward from threshold to apex; RDP 0.6",
		"legend": "overlay: yellow = current HALL_PORTALS hotspot rect, green = painted opening, magenta = painted frame outer edge",
		"doors": doors,
		"moonflower_gate": measure_gate(),
	}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
	main()
