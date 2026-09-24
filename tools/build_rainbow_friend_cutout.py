#!/usr/bin/env python3
"""Build the rainbow dust bunny follower cutout from its approved concept.

The concept (assets_src/characters/grand_puff_2026-09-13/references/
rainbow_dust_bunny_concept.png) is the rainbow dust bunny identity used for the
Day One transformation. Its background is a baked neutral checkerboard, so the
cutout is a derived isolation only: flood-fill the near-neutral light
background from the image edges (stopping at the drawn outline), soften the
mask edge, crop, resize and centre on a transparent power-of-two canvas. No
pixel of the character is redrawn or recoloured.

  python tools/build_rainbow_friend_cutout.py          build + provenance
  python tools/build_rainbow_friend_cutout.py --check  verify committed output
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/characters/grand_puff_2026-09-13/references/rainbow_dust_bunny_concept.png"
OUTPUT = ROOT / "assets/sprites/dust_bunnies/rainbow_friend.png"
PROVENANCE = ROOT / "assets_src/characters/rainbow_dust_bunny_2026-09-23/PROVENANCE.json"
CANVAS = 512
PAD = 12


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def is_background(rgb: tuple[int, int, int]) -> bool:
	# The baked checkerboard is light, near-neutral grey/white.
	return min(rgb) >= 185 and max(rgb) - min(rgb) <= 14


def build() -> int:
	from PIL import Image, ImageFilter
	image = Image.open(SOURCE).convert("RGB")
	width, height = image.size
	pixels = image.load()
	seen = bytearray(width * height)
	queue: deque[tuple[int, int]] = deque()
	for x in range(width):
		for y in (0, height - 1):
			if is_background(pixels[x, y]) and not seen[y * width + x]:
				seen[y * width + x] = 1
				queue.append((x, y))
	for y in range(height):
		for x in (0, width - 1):
			if is_background(pixels[x, y]) and not seen[y * width + x]:
				seen[y * width + x] = 1
				queue.append((x, y))
	while queue:
		x, y = queue.popleft()
		for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
			nx, ny = x + dx, y + dy
			if 0 <= nx < width and 0 <= ny < height and not seen[ny * width + nx] \
					and is_background(pixels[nx, ny]):
				seen[ny * width + nx] = 1
				queue.append((nx, ny))
	mask = Image.new("L", (width, height), 0)
	mask_pixels = mask.load()
	for y in range(height):
		for x in range(width):
			if not seen[y * width + x]:
				mask_pixels[x, y] = 255
	mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
	rgba = image.convert("RGBA")
	rgba.putalpha(mask)
	bbox = mask.point(lambda v: 255 if v > 8 else 0).getbbox()
	box = (max(0, bbox[0] - PAD), max(0, bbox[1] - PAD),
		min(width, bbox[2] + PAD), min(height, bbox[3] + PAD))
	cut = rgba.crop(box)
	scale = CANVAS / max(cut.size)
	cut = cut.resize((round(cut.size[0] * scale), round(cut.size[1] * scale)), Image.LANCZOS)
	canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
	canvas.alpha_composite(cut, ((CANVAS - cut.size[0]) // 2, CANVAS - cut.size[1]))
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(OUTPUT, optimize=True)
	PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
	record = {
		"schema": "derived_cutout/1",
		"asset": "assets/sprites/dust_bunnies/rainbow_friend.png",
		"role": "rainbow dust bunny follower card (owner canon 2026-09-23, DL-CIN-16)",
		"source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
		"source_sha256": sha256(SOURCE),
		"source_dimensions": [width, height],
		"transform": [
			"flood-fill the near-neutral light baked checkerboard (min channel >= 185, "
			"channel spread <= 14) from the image edges, stopping at the drawn outline",
			"mask edge: 3x3 minimum filter, then 0.8 px Gaussian blur",
			f"crop to the character bounding box plus {PAD} px: {list(box)}",
			f"Lanczos resize to {cut.size[0]}x{cut.size[1]} (longest side {CANVAS})",
			f"centred horizontally and bottom-aligned on a transparent {CANVAS}x{CANVAS} canvas",
		],
		"appearance_changed": False,
		"source_overwritten": False,
		"output_sha256": sha256(OUTPUT),
		"output_dimensions": [CANVAS, CANVAS],
	}
	PROVENANCE.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
	print(f"RAINBOWFRIEND|BUILT|{OUTPUT.relative_to(ROOT)}|{record['output_sha256']}")
	return 0


def check() -> int:
	if not OUTPUT.is_file() or not PROVENANCE.is_file():
		print("RAINBOWFRIEND|FAIL|missing output or provenance")
		return 1
	record = json.loads(PROVENANCE.read_text(encoding="utf-8"))
	ok = sha256(OUTPUT) == record.get("output_sha256") \
		and sha256(SOURCE) == record.get("source_sha256")
	print("RAINBOWFRIEND|RESULT|" + ("ALL OK" if ok else "HASH DRIFT"))
	return 0 if ok else 1


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	parser.add_argument("--check", action="store_true")
	return check() if parser.parse_args().check else build()


if __name__ == "__main__":
	sys.exit(main())
