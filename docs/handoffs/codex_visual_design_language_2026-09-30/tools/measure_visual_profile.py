#!/usr/bin/env python3
"""Measure the visual profile of existing art. Read-only; writes numbers, never images.

Reproduces the measurements in VISUAL_LANGUAGE_AUDIT.md:

  contour   colour of the dark silhouette edge of RGBA cutouts, per asset family
  shadows   hue family of the darkest 15% of pixels in each castle room background
  palette   dominant colours (k-means) of a set of images
  identity  share of pixels near named identity colours (for example Roshan's tail)

Usage, from the repository root:

  python -B docs/handoffs/codex_visual_design_language_2026-09-30/tools/measure_visual_profile.py contour
  python -B docs/handoffs/codex_visual_design_language_2026-09-30/tools/measure_visual_profile.py shadows
  python -B docs/handoffs/codex_visual_design_language_2026-09-30/tools/measure_visual_profile.py palette FILE [FILE ...]
  python -B docs/handoffs/codex_visual_design_language_2026-09-30/tools/measure_visual_profile.py identity FILE [FILE ...] --group tail=#968be6,#c8a6f6 --group hair=#a76c3b

These are source-file indicators, not state-local evidence: under `DL-VIS-08`
they never justify recolouring or regenerating approved art on their own.

Add --out PATH to write JSON to a file; otherwise JSON goes to stdout.
Requires Pillow. Enumerates tracked files with `git ls-files`. Protected
paths (assets/book/, assets/characters/friends/) are skipped. The method is a
sampled indicator, not an acceptance check: a family's numbers describe the
files sampled with the stated seed.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict

try:
	from PIL import Image
except ImportError:  # pragma: no cover - environment guard
	sys.exit("measure_visual_profile.py needs Pillow (pip install Pillow)")

PROTECTED = ("assets/book/", "assets/characters/friends/")
OPAQUE = 200
CLEAR = 40
DARK_LUMA = 90
MAX_PIXELS = 4_200_000


def tracked(pattern: str) -> list[str]:
	out = subprocess.run(["git", "ls-files", pattern], capture_output=True, text=True, check=True).stdout
	return [p for p in out.split() if not p.startswith(PROTECTED)]


def luma(rgb: tuple[int, int, int]) -> float:
	return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def describe(rgb: tuple[float, float, float]) -> dict:
	h, light, sat = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
	return {
		"hex": "#%02x%02x%02x" % tuple(round(c) for c in rgb),
		"hue": round(h * 360),
		"saturation": round(sat, 2),
		"lightness": round(light, 2),
	}


def rgba_pixels(image: Image.Image) -> tuple[bytes, int, int]:
	rgba = image.convert("RGBA")
	return rgba.tobytes(), rgba.width, rgba.height


def edge_pixels(path: str, cap: int = 250_000) -> list[tuple[int, int, int]]:
	image = Image.open(path)
	if image.mode not in ("RGBA", "LA", "PA") and "transparency" not in image.info:
		return []
	if image.width * image.height > MAX_PIXELS:
		return []
	data, width, height = rgba_pixels(image)
	step = max(1, int(((width * height) / cap) ** 0.5))

	def alpha(x: int, y: int) -> int:
		return data[(y * width + x) * 4 + 3]

	found = []
	for y in range(1, height - 1, step):
		for x in range(1, width - 1, step):
			i = (y * width + x) * 4
			if data[i + 3] < OPAQUE:
				continue
			if min(alpha(x + 1, y), alpha(x - 1, y), alpha(x, y + 1), alpha(x, y - 1)) < CLEAR:
				found.append((data[i], data[i + 1], data[i + 2]))
	return found


def family_of(path: str) -> str:
	parts = path.split("/")
	return "/".join(parts[1:3]) if len(parts) > 3 else parts[1]


def measure_contour(per_family: int, seed: int) -> dict:
	families: dict[str, list[str]] = defaultdict(list)
	for path in tracked("assets/*.png"):
		families[family_of(path)].append(path)
	rng = random.Random(seed)
	rows = []
	for name in sorted(families, key=lambda key: (-len(families[key]), key)):
		files = sorted(families[name])
		rng.shuffle(files)
		edges: list[tuple[int, int, int]] = []
		sampled = []
		for path in files[:per_family]:
			try:
				found = edge_pixels(path)
			except OSError:
				found = []
			if found:
				edges.extend(found)
				sampled.append(path)
		if len(edges) < 200:
			continue
		dark = [c for c in edges if luma(c) < DARK_LUMA]
		row = {
			"family": name,
			"files": len(families[name]),
			"sampled": sampled,
			"edge_pixels": len(edges),
			"dark_edge_share": round(len(dark) / len(edges), 2),
		}
		if dark:
			mean = tuple(sum(c[d] for c in dark) / len(dark) for d in range(3))
			row["dark_edge_mean"] = describe(mean)
			bins = Counter("#%02x%02x%02x" % (c[0] // 16 * 16, c[1] // 16 * 16, c[2] // 16 * 16) for c in dark)
			row["top_dark_bins"] = bins.most_common(5)
		rows.append(row)
	return {
		"measure": "contour",
		"method": (
			f"Opaque pixels (alpha >= {OPAQUE}) with a 4-neighbour below alpha {CLEAR}, on a grid "
			f"of about 250,000 samples per file; 'dark' means luma < {DARK_LUMA}. Up to {per_family} "
			f"files per family, shuffled with seed {seed}."
		),
		"families": rows,
	}


def measure_shadows() -> dict:
	rooms: dict[str, list[str]] = defaultdict(list)
	for path in tracked("assets/flats/castle/rooms/background_tiles/*.png"):
		match = re.search(r"room_(.+?)_background_r\d+_c\d+\.png$", path)
		if match:
			rooms[match.group(1)].append(path)
	rows = []
	for room, files in sorted(rooms.items()):
		pixels: list[tuple[int, int, int]] = []
		for path in sorted(files):
			image = Image.open(path).convert("RGB")
			image = image.resize((max(1, image.width // 6), max(1, image.height // 6)))
			raw = image.tobytes()
			pixels.extend((raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 3))
		ordered = sorted(pixels, key=luma)
		count = len(ordered)
		shadow = ordered[: count * 15 // 100]
		cool = neutral = warm = 0
		for rgb in shadow:
			h, _light, sat = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
			if sat < 0.10:
				neutral += 1
			elif 170 <= h * 360 <= 300:
				cool += 1
			else:
				warm += 1
		total = max(1, len(shadow))
		rows.append({
			"room": room,
			"tiles": len(files),
			"luma_p15": round(luma(ordered[count * 15 // 100]), 1),
			"luma_p50": round(luma(ordered[count // 2]), 1),
			"shadow_cool_share": round(cool / total, 2),
			"shadow_neutral_share": round(neutral / total, 2),
			"shadow_warm_share": round(warm / total, 2),
		})
	return {
		"measure": "shadows",
		"method": (
			"Castle room background tiles downsampled 6x; the darkest 15% of pixels by luma are "
			"classified cool (saturation >= 0.10 and hue 170-300), neutral (saturation < 0.10) or warm."
		),
		"rooms": rows,
	}


def measure_palette(files: list[str], k: int, seed: int) -> dict:
	rng = random.Random(seed)
	pixels: list[tuple[int, int, int]] = []
	for path in files:
		if path.startswith(PROTECTED):
			continue
		image = Image.open(path).convert("RGBA")
		image = image.resize((max(1, image.width // 2), max(1, image.height // 2)))
		raw = image.tobytes()
		pixels.extend((raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 4) if raw[i + 3] >= 230)
	if not pixels:
		return {"measure": "palette", "files": files, "clusters": []}
	sample = rng.sample(pixels, min(40_000, len(pixels)))
	centres = [tuple(float(v) for v in c) for c in rng.sample(sample, k)]
	groups: list[list[tuple[int, int, int]]] = []
	for _ in range(25):
		groups = [[] for _ in range(k)]
		for c in sample:
			nearest = min(range(k), key=lambda i: sum((c[d] - centres[i][d]) ** 2 for d in range(3)))
			groups[nearest].append(c)
		centres = [
			tuple(sum(c[d] for c in group) / len(group) for d in range(3)) if group else centres[i]
			for i, group in enumerate(groups)
		]
	clusters = [
		{"share": round(len(group) / len(sample), 3), **describe(centres[i])}
		for i, group in enumerate(groups) if group
	]
	clusters.sort(key=lambda row: -row["share"])
	return {
		"measure": "palette",
		"method": f"k-means (k={k}, 25 iterations, seed {seed}) on up to 40,000 opaque pixels (alpha >= 230) at half size.",
		"files": files,
		"clusters": clusters,
	}


def parse_hex(value: str) -> tuple[int, int, int]:
	value = value.strip().lstrip("#")
	return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def measure_identity(files: list[str], groups: list[str], tolerance: int) -> dict:
	"""Share of opaque pixels near each named identity colour group."""
	parsed: dict[str, list[tuple[int, int, int]]] = {}
	for group in groups:
		name, _, colours = group.partition("=")
		parsed[name] = [parse_hex(c) for c in colours.split(",") if c.strip()]
	limit = tolerance * tolerance
	rows = []
	for path in files:
		if path.startswith(PROTECTED):
			continue
		image = Image.open(path).convert("RGBA")
		image = image.resize((max(1, image.width // 4), max(1, image.height // 4)))
		raw = image.tobytes()
		opaque = 0
		hits = {name: 0 for name in parsed}
		for i in range(0, len(raw), 4):
			if raw[i + 3] < 230:
				continue
			opaque += 1
			pixel = (raw[i], raw[i + 1], raw[i + 2])
			for name, colours in parsed.items():
				if any(sum((pixel[d] - c[d]) ** 2 for d in range(3)) <= limit for c in colours):
					hits[name] += 1
		rows.append({
			"file": path,
			"opaque_pixels_quarter_size": opaque,
			**{f"{name}_share": round(count / max(1, opaque), 3) for name, count in hits.items()},
		})
	return {
		"measure": "identity",
		"method": (
			f"Quarter-size opaque pixels (alpha >= 230) within RGB distance {tolerance} of any colour "
			"in each named group. Costume, pose and framing change these shares; compare like with like."
		),
		"groups": {name: ["#%02x%02x%02x" % c for c in colours] for name, colours in parsed.items()},
		"files": rows,
	}


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	sub = parser.add_subparsers(dest="command", required=True)
	contour = sub.add_parser("contour")
	contour.add_argument("--per-family", type=int, default=8)
	contour.add_argument("--seed", type=int, default=7)
	shadows = sub.add_parser("shadows")
	palette = sub.add_parser("palette")
	palette.add_argument("files", nargs="+")
	palette.add_argument("--k", type=int, default=12)
	palette.add_argument("--seed", type=int, default=5)
	identity = sub.add_parser("identity")
	identity.add_argument("files", nargs="+")
	identity.add_argument("--group", action="append", required=True,
		help="name=#hex,#hex,... (repeatable)")
	identity.add_argument("--tolerance", type=int, default=32)
	for command in (contour, shadows, palette, identity):
		command.add_argument("--out")
	args = parser.parse_args(argv)
	if args.command == "contour":
		result = measure_contour(args.per_family, args.seed)
	elif args.command == "shadows":
		result = measure_shadows()
	elif args.command == "identity":
		result = measure_identity(args.files, args.group, args.tolerance)
	else:
		result = measure_palette(args.files, args.k, args.seed)
	text = json.dumps(result, indent=1, ensure_ascii=False) + "\n"
	if args.out:
		with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
			handle.write(text)
	else:
		sys.stdout.write(text)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
