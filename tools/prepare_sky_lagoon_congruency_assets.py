#!/usr/bin/env python3
"""Prepare audited Sky Lagoon sprite cards without modifying source masters.

The image-generation service returns padded chroma-key canvases.  This tool
trims the keyed alpha image, adds a small transparent safety gutter, and
downsamples once to the authored-pixel budget used by the runtime audit.
It also losslessly slices the approved 3:1 panorama and builds the tiny
contact-shadow sprite used by every grounded card.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def trim_and_resize(
		source: Path,
		output: Path,
		max_edge: int | None,
		target_height: int | None,
		pad_ratio: float,
) -> None:
	image = Image.open(source).convert("RGBA")
	alpha = image.getchannel("A")
	bounds = alpha.getbbox()
	if bounds is None:
		raise ValueError(f"{source} has no visible pixels")
	image = image.crop(bounds)
	pad = max(2, round(max(image.size) * pad_ratio))
	padded = Image.new("RGBA", (image.width + pad * 2, image.height + pad * 2))
	padded.alpha_composite(image, (pad, pad))
	if target_height is not None:
		scale = min(1.0, target_height / padded.height, 1024 / max(padded.size))
	elif max_edge is not None:
		scale = min(1.0, max_edge / max(padded.size))
	else:
		raise ValueError("one output size is required")
	size = (
		max(1, round(padded.width * scale)),
		max(1, round(padded.height * scale)),
	)
	if size != padded.size:
		padded = padded.resize(size, Image.Resampling.LANCZOS)
	output.parent.mkdir(parents=True, exist_ok=True)
	padded.save(output, optimize=True)


def slice_panorama(source: Path, output_dir: Path, count: int) -> None:
	image = Image.open(source).convert("RGB")
	if image.width % count != 0:
		raise ValueError(f"{source} width {image.width} is not divisible by {count}")
	tile_width = image.width // count
	output_dir.mkdir(parents=True, exist_ok=True)
	for index in range(count):
		tile = image.crop((index * tile_width, 0, (index + 1) * tile_width, image.height))
		tile.save(
			output_dir / f"flat_sky_lagoon_main_panorama_v2_tile_{index}.png",
			optimize=True,
		)


def make_contact_shadow(output: Path) -> None:
	canvas = Image.new("RGBA", (256, 128))
	mask = Image.new("L", canvas.size)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((28, 42, 228, 102), fill=150)
	mask = mask.filter(ImageFilter.GaussianBlur(13))
	color = Image.new("RGBA", canvas.size, (18, 67, 78, 0))
	color.putalpha(mask.point(lambda value: round(value * 0.52)))
	output.parent.mkdir(parents=True, exist_ok=True)
	color.save(output, optimize=True)


def grade_sprite(
		source: Path,
		output: Path,
		red: float,
		green: float,
		blue: float,
		brightness: float,
		matte: float,
		gamma: float,
) -> None:
	image = Image.open(source).convert("RGBA")
	rgb = image.convert("RGB")
	if matte > 0.0:
		blurred = rgb.filter(ImageFilter.GaussianBlur(1.6))
		smoothed = Image.blend(rgb, blurred, min(1.0, matte))
		interior = image.getchannel("A").point(lambda value: 255 if value >= 180 else 0)
		rgb = Image.composite(smoothed, rgb, interior)
	r, g, b = rgb.split()
	def curve(value: int, factor: float) -> int:
		scaled = max(0.0, min(1.0, value * factor * brightness / 255.0))
		return round((scaled ** gamma) * 255.0)
	r = r.point(lambda value: curve(value, red))
	g = g.point(lambda value: curve(value, green))
	b = b.point(lambda value: curve(value, blue))
	result = Image.merge("RGBA", (r, g, b, image.getchannel("A")))
	output.parent.mkdir(parents=True, exist_ok=True)
	result.save(output, optimize=True)


def parser() -> argparse.ArgumentParser:
	result = argparse.ArgumentParser()
	subparsers = result.add_subparsers(dest="command", required=True)
	sprite = subparsers.add_parser("sprite")
	sprite.add_argument("--input", type=Path, required=True)
	sprite.add_argument("--output", type=Path, required=True)
	size = sprite.add_mutually_exclusive_group(required=True)
	size.add_argument("--max-edge", type=int)
	size.add_argument("--height", type=int)
	sprite.add_argument("--pad-ratio", type=float, default=0.035)
	panorama = subparsers.add_parser("panorama")
	panorama.add_argument("--input", type=Path, required=True)
	panorama.add_argument("--output-dir", type=Path, required=True)
	panorama.add_argument("--count", type=int, default=4)
	shadow = subparsers.add_parser("shadow")
	shadow.add_argument("--output", type=Path, required=True)
	grade = subparsers.add_parser("grade")
	grade.add_argument("--input", type=Path, required=True)
	grade.add_argument("--output", type=Path, required=True)
	grade.add_argument("--red", type=float, default=1.0)
	grade.add_argument("--green", type=float, default=1.0)
	grade.add_argument("--blue", type=float, default=1.0)
	grade.add_argument("--brightness", type=float, default=1.0)
	grade.add_argument("--matte", type=float, default=0.0)
	grade.add_argument("--gamma", type=float, default=1.0)
	return result


def main() -> None:
	args = parser().parse_args()
	if args.command == "sprite":
		trim_and_resize(
			args.input,
			args.output,
			args.max_edge,
			args.height,
			args.pad_ratio,
		)
	elif args.command == "panorama":
		slice_panorama(args.input, args.output_dir, args.count)
	elif args.command == "shadow":
		make_contact_shadow(args.output)
	else:
		grade_sprite(
			args.input,
			args.output,
			args.red,
			args.green,
			args.blue,
			args.brightness,
			args.matte,
			args.gamma,
		)


if __name__ == "__main__":
	main()
