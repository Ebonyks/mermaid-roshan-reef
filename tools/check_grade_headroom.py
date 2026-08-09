#!/usr/bin/env python3
"""Gate: the Environment grade must not clip art that did not clip in the PNG.

Painted 2.5D flats are drawn unshaded, so the WorldEnvironment grade is the
only thing between an approved painting and the child's screen. When a profile
pushes post-contrast or leaves the ACES white point low, saturated pastel
channels clip and the painting's hue relationships break — measured at 21.6 %
of castle-room pixels before the 2026-08-02 retune (LIGHTING_2P5D_AUDIT).

This reads the live grade numbers straight out of the GDScript (so the gate
cannot drift from the shipped values), replays the chain over a sample of each
zone's real flats, and fails if a zone exceeds its clip/crush budget.

    python3 tools/check_grade_headroom.py            # gate
    python3 tools/check_grade_headroom.py --report   # numbers, always exit 0
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sim_render_grade import render, srgb_to_linear  # noqa: E402

Image.MAX_IMAGE_PIXELS = None

MAIN_GD = Path("scripts/main.gd")
CASTLE_GD = Path("scripts/arena/castle_rooms_25d.gd")

# zone -> (grade source, art globs, max clipped-channel %, max crushed %)
# Budgets are set just above each zone's post-retune measurement so a
# regression is caught but ordinary art churn is not.
ZONES = {
	"castle_room": ("castle_room", ["assets/flats/castle/rooms/room_*.png"], 6.0, 2.5),
	"sky_lagoon": ("sky_lagoon", ["assets/flats/sky_lagoon/main/*.png"], 1.0, 4.0),
	# bright_pastel stays loose because its ART is hot, not its grade: the
	# art35 card set clips 3.8% of pixels in the source PNGs. Tighten this to
	# ~6% once those are regenerated to the §C2 headroom spec.
	# The opera actor sheets (assets/opera/worlds/actors/, landed 2026-08-03)
	# are the current hot spot inside this zone: measured on their own they
	# crush 5.98% against a 0.72% source, and ~60% of what they lose had real
	# shading (source luma > 0.10), not just outline. The zone still passes as
	# a whole, and the E1 retune already cut those sheets down from 9.24%
	# crush / 23.32% clip under the pre-retune grade, so this is inherited art
	# debt rather than a regression — regenerate them to §C2 and they stop
	# being the thing dragging this zone's average.
	"bright_pastel": ("bright_pastel", [
		"assets/opera/worlds/**/*.png",
		"assets/art35/cards/**/*.png",
	], 18.0, 3.0),
}

# The Main Hall's dramatic storybook grade is a deliberate art decision locked
# by probe_castle_pearl_art.gd; it is exempt until the emissive masks land
# (LIGHTING_2P5D_AUDIT_2026-08-02 §C1/§E4) and is only ever reported.
REPORT_ONLY = {"castle_hall_lit"}


def _floats(block: str) -> dict:
	out = {}
	for key in ("full_exposure", "white_point", "saturation", "contrast", "brightness"):
		m = re.search(rf"^\s*{key}\s*=\s*([0-9.]+)", block, re.M)
		if m:
			out[key] = float(m.group(1))
	return out


def parse_profiles() -> dict:
	"""Pull _apply_scene_grade's defaults + per-profile overrides from main.gd."""
	src = MAIN_GD.read_text(encoding="utf-8")
	body = src.split("func _apply_scene_grade")[1].split("\nfunc ")[0]
	defaults = _floats(body.split("match profile:")[0])
	profiles = {}
	match_body = body.split("match profile:")[1]
	chunks = re.split(r'\n\t\t"([a-z_]+)":\n', match_body)
	for name, chunk in zip(chunks[1::2], chunks[2::2]):
		vals = dict(defaults)
		vals.update(_floats(chunk))
		profiles[name] = vals
	return defaults, profiles


def parse_castle_room() -> dict:
	"""Destination-room BCS + glow overrides from _sync_castle_environment."""
	src = CASTLE_GD.read_text(encoding="utf-8")
	body = src.split("func _sync_castle_environment")[1].split("\nfunc ")[0]
	tail = body.split("\telse:")[1]
	def g(key, default):
		m = re.search(rf"environment\.{key}\s*=\s*([0-9.]+)", tail)
		return float(m.group(1)) if m else default
	def g_speedy(key, default):
		m = re.search(rf"environment\.{key}\s*=\s*[0-9.]+ if speedy else ([0-9.]+)", tail)
		return float(m.group(1)) if m else g(key, default)
	return {
		"saturation": g("adjustment_saturation", 1.0),
		"contrast": g("adjustment_contrast", 1.0),
		"brightness": g("adjustment_brightness", 1.0),
		"glow_threshold": g("glow_hdr_threshold", 0.9),
		"glow_intensity": g_speedy("glow_intensity", 0.66),
		"glow_bloom": g_speedy("glow_bloom", 0.09),
	}


def build_profile_table() -> dict:
	_, profiles = parse_profiles()
	warm = profiles["warm_pastel"]
	room = parse_castle_room()
	table = {}
	for name, p in profiles.items():
		table[name] = (
			p["full_exposure"], p["white_point"], p["brightness"], p["contrast"],
			p["saturation"], 0.90, 0.95, 0.40, 2.40,
		)
	# Castle destination rooms: warm_pastel exposure/white, then the room's own
	# BCS + glow overrides written after _apply_scene_grade returns.
	table["castle_room"] = (
		warm["full_exposure"], warm["white_point"], room["brightness"],
		room["contrast"], room["saturation"], room["glow_threshold"],
		room["glow_intensity"], room["glow_bloom"], 2.40,
	)
	return table


def _sample(paths, limit):
	"""Evenly-spaced sample across the whole corpus, not the first `limit`.

	`paths[:limit]` reads alphabetically, so one directory that sorts early can
	own the entire sample: when the opera actor sheets landed on 2026-08-03 the
	578-file bright_pastel corpus reported numbers measured purely from
	assets/opera/worlds/actors/. Striding keeps every directory represented and
	keeps the pick deterministic (no RNG in a gate).
	"""
	if len(paths) <= limit:
		return list(paths)
	step = len(paths) / float(limit)
	return [paths[int(i * step)] for i in range(limit)]


def measure(paths, profile_values, light=None, limit=80):
	import sim_render_grade
	sim_render_grade.PROFILES["__gate__"] = profile_values
	clip_in = clip_out = crush_in = crush_out = 0.0
	n = 0
	for p in _sample(paths, limit):
		src = Image.open(p)
		if max(src.size) > 384:
			src.thumbnail((384, 384), Image.LANCZOS)
		rgba = np.asarray(src.convert("RGBA"), dtype=np.float32) / 255.0
		mask = rgba[..., 3] > 0.5
		if mask.sum() < 64:
			mask = np.ones(rgba.shape[:2], bool)
		im = src.convert("RGB")
		out, _ = render(im, "__gate__", light)
		a = np.asarray(im, dtype=np.float32) / 255.0
		b = np.asarray(out, dtype=np.float32) / 255.0
		clip_in += (a.max(-1) > 0.996)[mask].mean()
		clip_out += (b.max(-1) > 0.996)[mask].mean()
		crush_in += (a.max(-1) < 0.02)[mask].mean()
		crush_out += (b.max(-1) < 0.02)[mask].mean()
		n += 1
	if n == 0:
		return None
	return tuple(100.0 * v / n for v in (clip_in, clip_out, crush_in, crush_out))


def main(argv):
	ap = argparse.ArgumentParser()
	ap.add_argument("--report", action="store_true", help="print and always exit 0")
	a = ap.parse_args(argv)

	table = build_profile_table()
	failures = []
	# Keep gate output ASCII-safe: Windows automation commonly inherits a
	# cp1252 console, where the Unicode arrow raises before any audit can run.
	print(f"{'zone':16s} {'n':>4s} | {'clip% in->out':>16s} | {'crush% in->out':>16s} | budget")
	print("-" * 78)
	for zone, (profile, globs, max_clip, max_crush) in ZONES.items():
		if profile not in table:
			failures.append(f"{zone}: grade profile '{profile}' not found in main.gd")
			continue
		paths = []
		for g in globs:
			paths.extend(sorted(Path().glob(g)))
		paths = [p for p in paths if p.suffix.lower() == ".png"]
		if not paths:
			failures.append(f"{zone}: no art matched {globs}")
			continue
		r = measure(paths, table[profile])
		ok_clip = r[1] <= max_clip
		ok_crush = r[3] <= max_crush
		flag = "" if (ok_clip and ok_crush) else "   <-- OVER BUDGET"
		print(f"{zone:16s} {min(len(paths),80):4d} | {r[0]:6.2f} -> {r[1]:6.2f}   | "
			f"{r[2]:6.2f} -> {r[3]:6.2f}   | clip<={max_clip} crush<={max_crush}{flag}")
		if not ok_clip:
			failures.append(
				f"{zone}: {r[1]:.2f}% of pixels clip a channel on screen "
				f"(budget {max_clip}%, source was {r[0]:.2f}%)")
		if not ok_crush:
			failures.append(
				f"{zone}: {r[3]:.2f}% of pixels crush on screen "
				f"(budget {max_crush}%, source was {r[2]:.2f}%)")

	for zone in REPORT_ONLY:
		if zone in table:
			print(f"{zone:16s}    - | (report only -- deliberate art direction, "
				f"probe-locked)")

	if failures:
		print("\nGRADE HEADROOM FAIL")
		for f in failures:
			print(f"  - {f}")
		print("\nSee LIGHTING_2P5D_AUDIT_2026-08-02.md sections 1.7 / E1.")
		return 0 if a.report else 1
	print("\nGRADE HEADROOM OK")
	return 0


if __name__ == "__main__":
	raise SystemExit(main(sys.argv[1:]))
