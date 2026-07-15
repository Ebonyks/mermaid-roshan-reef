#!/usr/bin/env python3
"""Remove only border-connected chroma pixels and optionally split a grid."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def parse_color(value: str) -> np.ndarray:
	value = value.strip().lstrip("#")
	if len(value) != 6:
		raise argparse.ArgumentTypeError("color must be a six-digit RGB hex value")
	return np.array([int(value[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.int16)


def connected_key_mask(rgb: np.ndarray, key: np.ndarray, threshold: float) -> np.ndarray:
	distance = np.linalg.norm(rgb.astype(np.int16) - key, axis=2)
	candidate = distance <= threshold
	height, width = candidate.shape
	connected = np.zeros_like(candidate)
	queue: deque[tuple[int, int]] = deque()

	for x in range(width):
		if candidate[0, x]:
			queue.append((0, x))
		if candidate[height - 1, x]:
			queue.append((height - 1, x))
	for y in range(height):
		if candidate[y, 0]:
			queue.append((y, 0))
		if candidate[y, width - 1]:
			queue.append((y, width - 1))

	while queue:
		y, x = queue.popleft()
		if connected[y, x] or not candidate[y, x]:
			continue
		connected[y, x] = True
		if y > 0:
			queue.append((y - 1, x))
		if y + 1 < height:
			queue.append((y + 1, x))
		if x > 0:
			queue.append((y, x - 1))
		if x + 1 < width:
			queue.append((y, x + 1))
	return connected


def crop_subject(image: Image.Image, padding: int) -> Image.Image:
	alpha = image.getchannel("A")
	bounds = alpha.getbbox()
	if bounds is None:
		raise ValueError("no opaque subject pixels found")
	left, top, right, bottom = bounds
	return image.crop(
		(
			max(0, left - padding),
			max(0, top - padding),
			min(image.width, right + padding),
			min(image.height, bottom + padding),
		)
	)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("input", type=Path)
	parser.add_argument("output", type=Path)
	parser.add_argument("--key", type=parse_color, default=parse_color("#00ff00"))
	parser.add_argument("--threshold", type=float, default=70.0)
	parser.add_argument("--crop", action="store_true")
	parser.add_argument("--padding", type=int, default=8)
	args = parser.parse_args()

	image = Image.open(args.input).convert("RGBA")
	pixels = np.array(image)
	mask = connected_key_mask(pixels[:, :, :3], args.key, args.threshold)
	pixels[mask, 3] = 0
	# Transparent texels still participate in GPU filtering. Clearing their RGB
	# prevents the chroma key from bleeding around dark illustrated outlines.
	pixels[mask, :3] = 0
	result = Image.fromarray(pixels, "RGBA")
	if args.crop:
		result = crop_subject(result, args.padding)
	args.output.parent.mkdir(parents=True, exist_ok=True)
	result.save(args.output)
	print(f"removed {int(mask.sum())} border-connected key pixels; saved {args.output}")


if __name__ == "__main__":
	main()
