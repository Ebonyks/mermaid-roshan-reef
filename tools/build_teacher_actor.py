#!/usr/bin/env python3
"""Build Teacher Roshan's transparent Opera atlas and static actor card.

The selected built-in ImageGen result painted a neutral checker presentation
field instead of returning alpha. This builder removes only border-connected
near-neutral pixels, preserves the generated native source, then applies one
whole-canvas premultiplied-alpha Lanczos normalization to the established
1024px atlas size. The static actor is a lossless-role derivative of idle frame
zero and keeps the established 512px Opera fallback contract.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import subprocess
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
	ROOT
	/ "assets_src/imagegen/teacher_roshan_2026-09-03/raw"
	/ "teacher_roshan_sheet_raw.png"
)
ATLAS_OUTPUT = (
	ROOT / "assets/opera/worlds/actors/animation/roshan_teacher_sheet_a.png"
)
STATIC_OUTPUT = ROOT / "assets/opera/worlds/actors/roshan_teacher.png"
ALPHA_OUTPUT = (
	ROOT
	/ "assets_src/imagegen/teacher_roshan_2026-09-03"
	/ "teacher_roshan_sheet_alpha_native.png"
)
PACK_REPORT = (
	ROOT
	/ "assets_src/imagegen/teacher_roshan_2026-09-03"
	/ "teacher_roshan_sheet_pack_report.json"
)
ATLAS_SIZE = (1024, 1024)
CELL_SIZE = 256
STATIC_SIZE = (512, 512)


def _is_presentation_pixel(pixel: tuple[int, int, int]) -> bool:
	lo = min(pixel)
	hi = max(pixel)
	return lo >= 190 and hi - lo <= 25


def _remove_border_presentation(image: Image.Image) -> Image.Image:
	rgb = image.convert("RGB")
	width, height = rgb.size
	pixels = rgb.load()
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
		for neighbor_x, neighbor_y in (
			(x - 1, y),
			(x + 1, y),
			(x, y - 1),
			(x, y + 1),
		):
			if not (0 <= neighbor_x < width and 0 <= neighbor_y < height):
				continue
			index = neighbor_y * width + neighbor_x
			if background[index]:
				continue
			if not _is_presentation_pixel(pixels[neighbor_x, neighbor_y]):
				continue
			background[index] = 1
			queue.append((neighbor_x, neighbor_y))

	alpha = Image.new("L", rgb.size, 255)
	alpha.putdata([0 if value else 255 for value in background])
	if alpha.getbbox() in (None, (0, 0, width, height)):
		raise RuntimeError("presentation removal did not isolate bounded figures")
	result = rgb.convert("RGBA")
	result.putalpha(alpha)
	return result


def _resize_alpha(image: Image.Image, size: tuple[int, int]) -> Image.Image:
	return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def _audit_atlas(atlas: Image.Image) -> None:
	if atlas.size != ATLAS_SIZE:
		raise RuntimeError(f"unexpected atlas size: {atlas.size}")
	if atlas.getchannel("A").getextrema() != (0, 255):
		raise RuntimeError("atlas must contain transparent and opaque pixels")
	for row in range(4):
		for column in range(4):
			cell = atlas.getchannel("A").crop((
				column * CELL_SIZE,
				row * CELL_SIZE,
				(column + 1) * CELL_SIZE,
				(row + 1) * CELL_SIZE,
			))
			if cell.getbbox() is None:
				raise RuntimeError(f"atlas cell {row},{column} is empty")


def main() -> None:
	image = Image.open(SOURCE)
	if image.size != (1254, 1254):
		raise RuntimeError(f"unexpected accepted-master size: {image.size}")
	alpha_native = _remove_border_presentation(image)
	ALPHA_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	alpha_native.save(ALPHA_OUTPUT, format="PNG", optimize=True)
	subprocess.run([
		sys.executable,
		"tools/prepare_opera_roshan_animation.py",
		"--input-alpha",
		str(ALPHA_OUTPUT.relative_to(ROOT)),
		"--output",
		str(ATLAS_OUTPUT.relative_to(ROOT)),
		"--report",
		str(PACK_REPORT.relative_to(ROOT)),
	], check=True, cwd=ROOT)
	atlas = Image.open(ATLAS_OUTPUT).convert("RGBA")
	_audit_atlas(atlas)

	idle = atlas.crop((0, 0, CELL_SIZE, CELL_SIZE))
	static_actor = _resize_alpha(idle, STATIC_SIZE)
	if static_actor.getchannel("A").getbbox() is None:
		raise RuntimeError("static idle derivative is empty")
	STATIC_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	static_actor.save(STATIC_OUTPUT, format="PNG", optimize=True)
	print(f"built {ATLAS_OUTPUT.relative_to(ROOT)}")
	print(f"built {STATIC_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
	main()
