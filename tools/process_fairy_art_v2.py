#!/usr/bin/env python3
"""Normalize and publish generated Fairy Pond art for Godot Mobile.

The V2 subject masters are kept under assets_src/fairy_v2/concepts; the V3
continuous background masters live under assets_src/fairy_v3/concepts, and the
V4 cue masters live under assets_src/fairy_v4. This entry point normalizes the
source concepts, then delegates the continuous pond and 2D sprite-card builds.

Usage:
    python tools/process_fairy_art_v2.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from process_fairy_background_flow import main as build_background_flow
from process_fairy_readability_art import main as build_sprite_cards


ROOT = Path(__file__).resolve().parents[1]
CONCEPT_DIR = ROOT / "assets_src" / "fairy_v2" / "concepts"
MAX_EDGE = 1024


def _resize(image: Image.Image, maximum: int) -> Image.Image:
	copy = image.copy()
	copy.thumbnail((maximum, maximum), Image.Resampling.LANCZOS)
	return copy


def _normalize_concepts() -> None:
	for source in sorted(CONCEPT_DIR.glob("*.png")):
		image = Image.open(source)
		if max(image.size) <= MAX_EDGE:
			continue
		mode = "RGBA" if image.mode == "RGBA" else "RGB"
		image = _resize(image.convert(mode), MAX_EDGE)
		image.save(source, format="PNG", optimize=True)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--concepts-only", action="store_true")
	args = parser.parse_args()
	_normalize_concepts()
	if args.concepts_only:
		print(f"normalized concept masters in {CONCEPT_DIR}")
		return
	build_background_flow()
	build_sprite_cards()


if __name__ == "__main__":
	main()
