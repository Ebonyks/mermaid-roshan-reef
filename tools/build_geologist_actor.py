#!/usr/bin/env python3
"""Build the transparent 1024px Geologist Roshan runtime atlas.

The selected built-in ImageGen result painted a neutral checker presentation
field instead of returning alpha.  This builder removes only border-connected
near-neutral pixels, preserves the generated native source, then applies one
whole-canvas Lanczos normalization to the established 1024px atlas size.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/imagegen/geologist_roshan_2026-08-30/raw/geologist_roshan_sheet_raw.png"
OUTPUT = ROOT / "assets/opera/worlds/actors/animation/roshan_geologist_sheet_a.png"


def _is_presentation_pixel(pixel: tuple[int, int, int]) -> bool:
	lo = min(pixel)
	hi = max(pixel)
	return lo >= 190 and hi - lo <= 25


def main() -> None:
	image = Image.open(SOURCE).convert("RGB")
	width, height = image.size
	pixels = image.load()
	background = bytearray(width * height)
	queue: deque[tuple[int, int]] = deque()

	def seed(x: int, y: int) -> None:
		index = y * width + x
		if not background[index] and _is_presentation_pixel(pixels[x, y]):
			background[index] = 1
			queue.append((x, y))

	for x in range(width):
		seed(x, 0)
		seed(x, height - 1)
	for y in range(height):
		seed(0, y)
		seed(width - 1, y)

	while queue:
		x, y = queue.popleft()
		for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
			if nx < 0 or ny < 0 or nx >= width or ny >= height:
				continue
			index = ny * width + nx
			if background[index] or not _is_presentation_pixel(pixels[nx, ny]):
				continue
			background[index] = 1
			queue.append((nx, ny))

	rgba = image.convert("RGBA")
	alpha = Image.new("L", image.size, 255)
	alpha.putdata([0 if value else 255 for value in background])
	rgba.putalpha(alpha)
	# Premultiply before resizing so transparent presentation pixels cannot
	# leave a pale matte around hair, hands, fins, or helmet edges.
	premultiplied = Image.new("RGBA", rgba.size)
	premultiplied.putdata([
		(r * a // 255, g * a // 255, b * a // 255, a)
		for r, g, b, a in rgba.getdata()
	])
	premultiplied = premultiplied.resize((1024, 1024), Image.Resampling.LANCZOS)
	result = Image.new("RGBA", premultiplied.size)
	result.putdata([
		(
			min(255, r * 255 // a) if a else 0,
			min(255, g * 255 // a) if a else 0,
			min(255, b * 255 // a) if a else 0,
			a,
		)
		for r, g, b, a in premultiplied.getdata()
	])
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	result.save(OUTPUT, optimize=True)


if __name__ == "__main__":
	main()
