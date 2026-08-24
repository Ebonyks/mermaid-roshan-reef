#!/usr/bin/env python3
"""Build the Day One Art Studio runtime cards from preserved ImageGen natives.

The generator returned correct RGBA subjects with high-opacity decorative glow
outside the drawn contour.  This tool derives a mask from the painted subject,
expands it only far enough to retain the dark ink edge, and intersects it with
the original alpha.  RGB subject pixels are never repainted.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/imagegen/day_one_art_studio_2026-08-23"
DEST = ROOT / "assets/castle/day_one_art_studio"


def _largest_component(mask: Image.Image) -> Image.Image:
	width, height = mask.size
	data = bytearray(mask.tobytes())
	seen = bytearray(width * height)
	best: list[int] = []
	for start, value in enumerate(data):
		if value == 0 or seen[start]:
			continue
		seen[start] = 1
		stack = [start]
		component: list[int] = []
		while stack:
			index = stack.pop()
			component.append(index)
			x = index % width
			y = index // width
			if x > 0:
				neighbor = index - 1
				if data[neighbor] and not seen[neighbor]:
					seen[neighbor] = 1
					stack.append(neighbor)
			if x + 1 < width:
				neighbor = index + 1
				if data[neighbor] and not seen[neighbor]:
					seen[neighbor] = 1
					stack.append(neighbor)
			if y > 0:
				neighbor = index - width
				if data[neighbor] and not seen[neighbor]:
					seen[neighbor] = 1
					stack.append(neighbor)
			if y + 1 < height:
				neighbor = index + width
				if data[neighbor] and not seen[neighbor]:
					seen[neighbor] = 1
					stack.append(neighbor)
		if len(component) > len(best):
			best = component
	output = bytearray(width * height)
	for index in best:
		output[index] = 255
	return Image.frombytes("L", mask.size, bytes(output))


def _clean_subject_alpha(image: Image.Image, mode: str) -> Image.Image:
	image = image.convert("RGBA")
	rgb = image.convert("RGB")
	alpha = image.getchannel("A")
	pixels = rgb.load()
	mask = Image.new("L", image.size, 0)
	mask_pixels = mask.load()

	for y in range(image.height):
		for x in range(image.width):
			r, g, b = pixels[x, y]
			luma = (299 * r + 587 * g + 114 * b) // 1000
			if mode == "grime":
				# The accepted grime is a pale lavender/mint dry mark.  Its
				# generated aura is either near-white or near-black and is not
				# part of the represented counter residue.
				keep = 118 <= luma <= 232 and max(r, g, b) - min(r, g, b) >= 6
			else:
				# Bright painted interiors define the prop; a bounded expansion
				# restores the adjacent deep-plum authored contour.
				keep = luma >= 92
			mask_pixels[x, y] = 255 if keep else 0

	mask = mask.filter(ImageFilter.MaxFilter(15 if mode == "grime" else 13))
	mask = ImageChops.multiply(mask, alpha.point(lambda value: 255 if value else 0))
	mask = _largest_component(mask)
	clean_alpha = ImageChops.multiply(alpha, mask)
	result = image.copy()
	result.putalpha(clean_alpha)
	return result


def _save(source_name: str, dest_name: str, size: tuple[int, int],
		crop: tuple[int, int, int, int] | None = None, mode: str = "prop") -> None:
	image = Image.open(SOURCE / source_name).convert("RGBA")
	if crop is not None:
		image = image.crop(crop)
	image = _clean_subject_alpha(image, mode)
	image = image.resize(size, Image.Resampling.LANCZOS)
	image.save(DEST / dest_name, format="PNG", optimize=True)


def main() -> None:
	DEST.mkdir(parents=True, exist_ok=True)
	_save("loose_brush_bundle_native.png", "loose_brush_bundle.png", (768, 512))
	_save("paint_bottle_pair_native.png", "paint_bottle_pink.png", (384, 512),
		(0, 0, 768, 1024))
	_save("paint_bottle_pair_native.png", "paint_bottle_blue.png", (384, 512),
		(768, 0, 1536, 1024))
	_save("paint_cups_native.png", "paint_cups.png", (768, 512))
	_save("grime_patches_native.png", "grime_left.png", (512, 306),
		(0, 130, 720, 560), "grime")
	_save("grime_patches_native.png", "grime_desk.png", (512, 346),
		(680, 120, 1360, 580), "grime")
	_save("grime_patches_native.png", "grime_right.png", (512, 307),
		(1330, 140, 2048, 570), "grime")
	_save("magic_cleaning_brush_native.png", "magic_cleaning_brush.png",
		(936, 1024))


if __name__ == "__main__":
	main()
