"""Trim, resize, and validate the pass-35 generated sprite replacements."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def remove_chroma_key(image: Image.Image) -> Image.Image:
	"""Remove the neon green or magenta key sampled from the image corners."""
	image = image.convert("RGBA")
	corners = [
		image.getpixel((0, 0)), image.getpixel((image.width - 1, 0)),
		image.getpixel((0, image.height - 1)),
		image.getpixel((image.width - 1, image.height - 1)),
	]
	green_key = sum(pixel[1] for pixel in corners) > sum(pixel[0] + pixel[2] for pixel in corners)
	pixels = list(image.getdata())
	cleaned: list[tuple[int, int, int, int]] = []
	for red, green, blue, _alpha in pixels:
		strength = min(green - red, green - blue) if green_key else min(red - green, blue - green)
		key_channel = green if green_key else min(red, blue)
		if strength <= 42 or key_channel <= 115:
			cleaned.append((red, green, blue, 255))
			continue
		alpha = max(0, min(255, round((132 - strength) * 255.0 / 90.0)))
		if alpha < 58:
			cleaned.append((0, 0, 0, 0))
			continue
		if green_key:
			green = min(green, round(max(red, blue) * 1.08))
		else:
			neutral = round(green * 1.12)
			red = min(red, neutral)
			blue = min(blue, neutral)
		cleaned.append((red, green, blue, alpha))
	image.putdata(cleaned)
	return image


def process(source: Path, destination: Path, max_edge: int, chroma_key: bool) -> tuple[int, int, float]:
	with Image.open(source) as opened:
		image = remove_chroma_key(opened) if chroma_key else opened.convert("RGBA")

	alpha = image.getchannel("A")
	bbox = alpha.point(lambda value: 255 if value >= 8 else 0).getbbox()
	if bbox is None:
		raise ValueError(f"{source} contains no opaque subject")

	padding = max(8, round(max(image.size) * 0.015))
	left = max(0, bbox[0] - padding)
	top = max(0, bbox[1] - padding)
	right = min(image.width, bbox[2] + padding)
	bottom = min(image.height, bbox[3] + padding)
	image = image.crop((left, top, right, bottom))

	longest = max(image.size)
	if longest > max_edge:
		scale = max_edge / longest
		image = image.resize(
			(max(1, round(image.width * scale)), max(1, round(image.height * scale))),
			Image.Resampling.LANCZOS,
		)
	if chroma_key:
		image.putalpha(image.getchannel("A").point(lambda value: 0 if value < 72 else value))

	destination.parent.mkdir(parents=True, exist_ok=True)
	image.save(destination, optimize=True)

	alpha = image.getchannel("A")
	opaque = sum(1 for value in alpha.getdata() if value >= 220)
	coverage = opaque / float(image.width * image.height)
	corner_alpha = [alpha.getpixel(point) for point in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1))]
	if max(corner_alpha) > 8:
		raise ValueError(f"{destination} does not have transparent corners: {corner_alpha}")
	if coverage < 0.08:
		raise ValueError(f"{destination} subject coverage is too low: {coverage:.3f}")
	return image.width, image.height, coverage


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--source-dir", type=Path, required=True)
	parser.add_argument("--destination-dir", type=Path, required=True)
	parser.add_argument("--max-edge", type=int, default=1024)
	parser.add_argument("--chroma-key", action="store_true")
	parser.add_argument("--strict-magenta", action="store_true", help=argparse.SUPPRESS)
	args = parser.parse_args()

	for source in sorted(args.source_dir.glob("*.png")):
		destination = args.destination_dir / source.name
		width, height, coverage = process(source, destination, args.max_edge, args.chroma_key or args.strict_magenta)
		print(f"PASS35_SPRITE|{source.name}|{width}x{height}|coverage={coverage:.3f}")


if __name__ == "__main__":
	main()
