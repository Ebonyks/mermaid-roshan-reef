#!/usr/bin/env python3
"""Normalize generated artwork for the Mermaid Roshan asset pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument("input", type=Path)
	parser.add_argument("output", type=Path)
	parser.add_argument("--max-size", type=int, default=1024)
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	with Image.open(args.input) as source:
		image = source.convert("RGBA") if "A" in source.getbands() else source.convert("RGB")
		if max(image.size) > args.max_size:
			image.thumbnail((args.max_size, args.max_size), Image.Resampling.LANCZOS)
		args.output.parent.mkdir(parents=True, exist_ok=True)
		image.save(args.output, format="PNG", optimize=True)


if __name__ == "__main__":
	main()
