#!/usr/bin/env python3
"""Normalize one generated combat FX cutout onto an exact RGBA canvas."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def sha256(path: Path) -> str:
	hash_value = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			hash_value.update(chunk)
	return hash_value.hexdigest()


def checkerboard(width: int, height: int, cell: int = 16) -> Image.Image:
	image = Image.new("RGBA", (width, height), (232, 232, 238, 255))
	draw = ImageDraw.Draw(image)
	for y in range(0, height, cell):
		for x in range(0, width, cell):
			if (x // cell + y // cell) % 2:
				draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(190, 192, 204, 255))
	return image


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	parser.add_argument("--width", type=int, required=True)
	parser.add_argument("--height", type=int, required=True)
	parser.add_argument("--margin", type=int, default=8)
	parser.add_argument("--component-min", type=int, default=1)
	parser.add_argument("--component-max", type=int, default=1)
	parser.add_argument("--alpha-threshold", type=int, default=8)
	parser.add_argument("--report", type=Path, required=True)
	parser.add_argument("--qa", type=Path, required=True)
	args = parser.parse_args()

	source = Image.open(args.input).convert("RGBA")
	alpha = source.getchannel("A")
	bbox = alpha.point(lambda value: 255 if value >= args.alpha_threshold else 0).getbbox()
	if bbox is None:
		raise ValueError("input has no visible pixels")
	crop = source.crop(bbox)
	available_width = args.width - args.margin * 2
	available_height = args.height - args.margin * 2
	if available_width <= 0 or available_height <= 0:
		raise ValueError("margin leaves no drawable canvas")
	scale = min(available_width / crop.width, available_height / crop.height)
	resized_size = (
		max(1, round(crop.width * scale)),
		max(1, round(crop.height * scale)),
	)
	resized = crop.resize(resized_size, Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", (args.width, args.height), (0, 0, 0, 0))
	position = (
		(args.width - resized.width) // 2,
		(args.height - resized.height) // 2,
	)
	canvas.alpha_composite(resized, position)

	args.output.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(args.output, optimize=True)
	qa = checkerboard(args.width, args.height)
	qa.alpha_composite(canvas)
	args.qa.parent.mkdir(parents=True, exist_ok=True)
	qa.save(args.qa, optimize=True)

	output_alpha = canvas.getchannel("A")
	solid_mask = output_alpha.point(lambda value: 255 if value >= args.alpha_threshold else 0)
	visible_bbox = solid_mask.getbbox()
	mask_bytes = bytes(1 if value else 0 for value in solid_mask.getdata())
	mask_array = np.frombuffer(mask_bytes, dtype=np.uint8).reshape((args.height, args.width))
	labels, component_count = ndimage.label(
		mask_array,
		structure=[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
	)
	del labels
	alpha_values = list(output_alpha.getdata())
	semi_alpha_pixels = sum(1 for value in alpha_values if 0 < value < 255)
	visible_pixels = sum(1 for value in alpha_values if value > 0)
	margin_pass = bool(
		visible_bbox
		and visible_bbox[0] >= args.margin
		and visible_bbox[1] >= args.margin
		and visible_bbox[2] <= args.width - args.margin
		and visible_bbox[3] <= args.height - args.margin
	)
	failures: list[str] = []
	if not margin_pass:
		failures.append("visible bounds do not preserve the requested margin")
	if not args.component_min <= component_count <= args.component_max:
		failures.append(
			f"connected components {component_count} outside "
			f"{args.component_min}..{args.component_max}")

	report = {
		"pass": not failures,
		"failures": failures,
		"input": str(args.input),
		"input_sha256": sha256(args.input),
		"output": str(args.output),
		"output_sha256": sha256(args.output),
		"canvas": [args.width, args.height],
		"mode": canvas.mode,
		"source_bbox": list(bbox),
		"visible_bbox": list(visible_bbox) if visible_bbox else None,
		"uniform_scale": round(scale, 6),
		"position": list(position),
		"connected_components": int(component_count),
		"allowed_components": [args.component_min, args.component_max],
		"visible_pixels": visible_pixels,
		"semi_alpha_pixels": semi_alpha_pixels,
		"semi_alpha_ratio": round(semi_alpha_pixels / max(visible_pixels, 1), 6),
		"qa_checker": str(args.qa),
	}
	args.report.parent.mkdir(parents=True, exist_ok=True)
	args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(report, indent=2))
	return 0 if report["pass"] else 1


if __name__ == "__main__":
	raise SystemExit(main())
