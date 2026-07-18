#!/usr/bin/env python3
"""Normalize generated Fairy Pond art for Godot Mobile.

The image-generation masters are kept under assets_src/fairy_v2/concepts.
This script creates the <=1024px runtime textures after chroma removal.  It is
deliberately independent of Blender so texture preparation is reproducible in
the lightweight CI/import environment.

Usage:
    python tools/process_fairy_art_v2.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CONCEPT_DIR = ROOT / "assets_src" / "fairy_v2" / "concepts"
KEYED_DIR = ROOT / "tmp" / "fairy_v2" / "key_removed"
RUNTIME_DIR = ROOT / "assets" / "fairy"
SUBJECT_DIR = ROOT / "assets_src" / "fairy_v2" / "runtime_textures"
MAX_EDGE = 1024
SUBJECT_EDGE = 960

BACKGROUNDS = {
	"background_dawn.png": "pond_dawn.png",
	"background_twilight.png": "pond_twilight.png",
	"background_clearing.png": "pond_boss_clearing.png",
}

SUBJECTS = {
	"bug_jewel.png": "bug_jewel.png",
	"bug_moth.png": "bug_moth.png",
	"bug_firefly.png": "bug_firefly.png",
	"boss_leaf.png": "boss_leaf.png",
	"boss_seed.png": "boss_seed.png",
	"boss_sprout.png": "boss_sprout.png",
	"boss_bud.png": "boss_bud.png",
	"boss_opening.png": "boss_opening.png",
	"boss_bloom.png": "boss_bloom.png",
}


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


def _save_background(source: Path, target: Path) -> None:
	image = Image.open(source).convert("RGB")
	image = _resize(image, MAX_EDGE)
	target.parent.mkdir(parents=True, exist_ok=True)
	image.save(target, format="PNG", optimize=True)


def _save_subject(source: Path, target: Path) -> None:
	image = Image.open(source).convert("RGBA")
	bounds = image.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError(f"no opaque subject found in {source}")
	image = image.crop(bounds)
	image = _resize(image, SUBJECT_EDGE)
	canvas = Image.new("RGBA", (MAX_EDGE, MAX_EDGE), (0, 0, 0, 0))
	x = (MAX_EDGE - image.width) // 2
	y = (MAX_EDGE - image.height) // 2
	canvas.alpha_composite(image, (x, y))
	target.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(target, format="PNG", optimize=True)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--concepts-only", action="store_true")
	args = parser.parse_args()
	_normalize_concepts()
	if args.concepts_only:
		print(f"normalized concept masters in {CONCEPT_DIR}")
		return
	for source_name, target_name in BACKGROUNDS.items():
		_save_background(CONCEPT_DIR / source_name, RUNTIME_DIR / target_name)
	for source_name, target_name in SUBJECTS.items():
		_save_subject(KEYED_DIR / source_name, SUBJECT_DIR / target_name)
	print(f"wrote {len(BACKGROUNDS)} pond plates to {RUNTIME_DIR}")
	print(f"wrote {len(SUBJECTS)} relief masters to {SUBJECT_DIR}")


if __name__ == "__main__":
	main()
