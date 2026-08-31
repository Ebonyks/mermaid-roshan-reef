#!/usr/bin/env python3
"""Prepare the accepted Chapter 2 birthday cake for runtime.

The accepted ImageGen master contains a pale checkerboard rather than genuine
alpha.  The checker is removed only when it is both near-neutral/near-white and
connected to the canvas border.  This preserves the cake's enclosed cream
frosting and pearls, then applies one uniform whole-canvas resize in
premultiplied-alpha space so transparent checker RGB cannot create a white
fringe.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
	ROOT
	/ "assets_src/imagegen/chapter2_birthday_2026-08-30/native"
	/ "chapter2_grand_candied_strawberry_cake_native.png"
)
DEST = (
	ROOT
	/ "assets/chapter2/birthday"
	/ "chapter2_grand_candied_strawberry_cake.png"
)
SINGLE_STRAWBERRY_SOURCE = (
	ROOT
	/ "assets_src/imagegen/chapter2_birthday_2026-08-30/native"
	/ "sky_lagoon_strawberry_single_native.png"
)
SINGLE_STRAWBERRY_DEST = (
	ROOT
	/ "assets/chapter2/birthday"
	/ "sky_lagoon_strawberry_single.png"
)
CANDLE_SOURCE_ROOT = ROOT / "assets_src/imagegen/chapter_two_rainbow_candle_2026-08-30"
UNLIT_CANDLE_SOURCE = CANDLE_SOURCE_ROOT / "rainbow_candle_discovery_unlit_reference.png"
LIT_CANDLE_SOURCE = CANDLE_SOURCE_ROOT / "rainbow_candle_large_flame_later_reference.png"
UNLIT_CANDLE_DEST = ROOT / "assets/chapter2/birthday/rainbow_candle_unlit.png"
LIT_CANDLE_DEST = ROOT / "assets/chapter2/birthday/rainbow_candle_large_flame.png"
RUNTIME_SIZE = (1024, 1024)


def _is_checker_pixel(red: int, green: int, blue: int,
		minimum_channel: int, maximum_spread: int) -> bool:
	return min(red, green, blue) >= minimum_channel \
		and max(red, green, blue) - min(red, green, blue) <= maximum_spread


def _remove_border_checker(image: Image.Image, minimum_channel: int = 228,
		maximum_spread: int = 4) -> Image.Image:
	rgb = image.convert("RGB")
	width, height = rgb.size
	pixels = rgb.load()
	background = bytearray(width * height)
	queue: deque[int] = deque()

	def seed(x: int, y: int) -> None:
		index = y * width + x
		if background[index]:
			return
		red, green, blue = pixels[x, y]
		if not _is_checker_pixel(red, green, blue,
				minimum_channel, maximum_spread):
			return
		background[index] = 1
		queue.append(index)

	for x in range(width):
		seed(x, 0)
		seed(x, height - 1)
	for y in range(height):
		seed(0, y)
		seed(width - 1, y)

	while queue:
		index = queue.popleft()
		x = index % width
		y = index // width
		for neighbor_x, neighbor_y in (
			(x - 1, y),
			(x + 1, y),
			(x, y - 1),
			(x, y + 1),
		):
			if not (0 <= neighbor_x < width and 0 <= neighbor_y < height):
				continue
			neighbor = neighbor_y * width + neighbor_x
			if background[neighbor]:
				continue
			red, green, blue = pixels[neighbor_x, neighbor_y]
			if not _is_checker_pixel(red, green, blue,
					minimum_channel, maximum_spread):
				continue
			background[neighbor] = 1
			queue.append(neighbor)

	hard_alpha = Image.new("L", rgb.size, 255)
	hard_alpha.putdata([0 if value else 255 for value in background])
	if hard_alpha.getbbox() in (None, (0, 0, width, height)):
		raise RuntimeError("checker removal did not isolate a bounded cake subject")

	# The generator antialiased the dark cake outline against the checker.  A
	# hard key therefore leaves a pale one-pixel fringe.  Recover the edge by
	# comparing each two-pixel boundary sample with its nearest opaque interior
	# colour and nearest checker colour, then solve the simple matte equation
	# C = alpha * foreground + (1 - alpha) * background.
	core = hard_alpha.filter(ImageFilter.MinFilter(5))
	hard = bytearray(hard_alpha.tobytes())
	core_data = bytearray(core.tobytes())
	alpha_data = bytearray(hard_alpha.tobytes())
	output_pixels = bytearray(rgb.tobytes())

	def nearest_colour(x: int, y: int, target: bytearray, want_set: bool) -> tuple[int, int, int]:
		best_distance = 10_000
		best = pixels[x, y]
		for radius_y in range(-6, 7):
			neighbor_y = y + radius_y
			if not 0 <= neighbor_y < height:
				continue
			for radius_x in range(-6, 7):
				neighbor_x = x + radius_x
				if not 0 <= neighbor_x < width:
					continue
				index = neighbor_y * width + neighbor_x
				if bool(target[index]) != want_set:
					continue
				distance = radius_x * radius_x + radius_y * radius_y
				if distance < best_distance:
					best_distance = distance
					best = pixels[neighbor_x, neighbor_y]
		return best

	for y in range(height):
		for x in range(width):
			index = y * width + x
			if not hard[index] or core_data[index]:
				continue
			composite = pixels[x, y]
			foreground = nearest_colour(x, y, core_data, True)
			checker = nearest_colour(x, y, hard, False)
			direction = tuple(foreground[channel] - checker[channel] for channel in range(3))
			numerator = sum(
				(composite[channel] - checker[channel]) * direction[channel]
				for channel in range(3)
			)
			denominator = max(1, sum(value * value for value in direction))
			matte = max(0.0, min(1.0, numerator / denominator))
			alpha_data[index] = round(matte * 255)
			pixel_offset = index * 3
			output_pixels[pixel_offset:pixel_offset + 3] = bytes(foreground)

	clean_rgb = Image.frombytes("RGB", rgb.size, bytes(output_pixels))
	alpha = Image.frombytes("L", rgb.size, bytes(alpha_data))
	result = clean_rgb.convert("RGBA")
	result.putalpha(alpha)
	return result


def _prepare(source: Path, destination: Path, minimum_channel: int = 228,
		maximum_spread: int = 4) -> None:
	image = Image.open(source)
	if image.size != (1254, 1254):
		raise RuntimeError(f"unexpected accepted-master size: {image.size}")
	image = _remove_border_checker(image, minimum_channel, maximum_spread)
	# Resize in premultiplied-alpha space to prevent hidden checker RGB from
	# leaking into the antialiased runtime edge.
	image = image.convert("RGBa").resize(RUNTIME_SIZE, Image.Resampling.LANCZOS).convert("RGBA")
	if image.getchannel("A").getextrema() != (0, 255):
		raise RuntimeError("runtime cake must contain both transparent and opaque pixels")
	destination.parent.mkdir(parents=True, exist_ok=True)
	image.save(destination, format="PNG", optimize=True)


def main() -> None:
	_prepare(SOURCE, DEST)
	_prepare(SINGLE_STRAWBERRY_SOURCE, SINGLE_STRAWBERRY_DEST)
	_prepare(UNLIT_CANDLE_SOURCE, UNLIT_CANDLE_DEST)
	# The accepted lit reference contains a pale checker-baked glow outside the
	# saturated rainbow flame. Treat that low-chroma glow envelope as matte; the
	# large coloured flame itself remains intact and phone-readable.
	_prepare(LIT_CANDLE_SOURCE, LIT_CANDLE_DEST, 205, 45)


if __name__ == "__main__":
	main()
