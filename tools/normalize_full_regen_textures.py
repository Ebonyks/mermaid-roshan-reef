#!/usr/bin/env python3
"""Normalize generated texture candidates for mobile import and repetition."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
TEXTURE_DIR = ROOT / "assets" / "full_texture_regen_2026-07-18" / "textures"
REPORT = ROOT / "audit" / "full_regen_2026-07-18" / "texture_normalization.json"
MAX_SIDE = 1024
EDGE_BAND = 72
PLANET_VARIANT_NAMES = {
	"R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground_b.png",
	"R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground_c.png",
}

TILE_BOTH = {
	"R007_REEF_CAUSTIC_GROUND_TREATMENT",
	"R032_CASTLE_KITCHEN_COUNTER_TEXTURE",
	"R033_CASTLE_KITCHEN_FLOOR_TEXTURE",
	"R034_CASTLE_KITCHEN_WOOD_TEXTURE",
	"R044_BUTTERFLY_WORLD_PLANET_SURFACE",
	"R050_DUNGEON_ARENA_FLOOR",
}
TILE_HORIZONTAL = {"R008_REEF_BACKDROP_SEAMOUNTS"}


def role_id(path: Path) -> str:
	return path.stem.split("__", 1)[0].upper()


def resize_mobile(image: Image.Image) -> Image.Image:
	width, height = image.size
	longest = max(width, height)
	if longest <= MAX_SIDE:
		return image
	scale = MAX_SIDE / float(longest)
	new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
	return image.resize(new_size, Image.Resampling.LANCZOS)


def blend_opposite_edges(array: np.ndarray, axis: int, band: int) -> np.ndarray:
	length = array.shape[axis]
	band = min(band, max(2, length // 5))
	result = array.astype(np.float32, copy=True)
	for index in range(band):
		weight = 0.5 * (1.0 + np.cos(np.pi * index / float(band - 1)))
		left_slice = [slice(None)] * result.ndim
		right_slice = [slice(None)] * result.ndim
		left_slice[axis] = index
		right_slice[axis] = length - 1 - index
		left = array[tuple(left_slice)].astype(np.float32)
		right = array[tuple(right_slice)].astype(np.float32)
		average = 0.5 * (left + right)
		result[tuple(left_slice)] = left * (1.0 - weight) + average * weight
		result[tuple(right_slice)] = right * (1.0 - weight) + average * weight
	return np.clip(result, 0.0, 255.0).astype(np.uint8)


def make_seamless(image: Image.Image, horizontal: bool, vertical: bool) -> Image.Image:
	array = np.asarray(image.convert("RGB"))
	if horizontal:
		array = blend_opposite_edges(array, axis=1, band=EDGE_BAND)
	if vertical:
		array = blend_opposite_edges(array, axis=0, band=EDGE_BAND)
	# Quantization during the second-axis blend can separate pixels that were
	# already paired on the first axis. Pin the outer samples after both passes.
	if horizontal:
		edge = ((array[:, 0].astype(np.uint16) + array[:, -1].astype(np.uint16)) // 2).astype(np.uint8)
		array[:, 0] = edge
		array[:, -1] = edge
	if vertical:
		edge = ((array[0].astype(np.uint16) + array[-1].astype(np.uint16)) // 2).astype(np.uint8)
		array[0] = edge
		array[-1] = edge
	return Image.fromarray(array, mode="RGB")


def alpha_metrics(image: Image.Image) -> dict[str, float]:
	if "A" not in image.getbands():
		return {"transparent_ratio": 0.0, "partial_ratio": 0.0, "opaque_ratio": 1.0}
	alpha = np.asarray(image.getchannel("A"))
	pixels = float(alpha.size)
	return {
		"transparent_ratio": float(np.count_nonzero(alpha <= 8) / pixels),
		"partial_ratio": float(np.count_nonzero((alpha > 8) & (alpha < 247)) / pixels),
		"opaque_ratio": float(np.count_nonzero(alpha >= 247) / pixels),
	}


def build_planet_variants(base_path: Path) -> list[Path]:
	with Image.open(base_path) as source:
		base = source.convert("RGB")
	variant_b = ImageEnhance.Color(base.transpose(Image.Transpose.ROTATE_90)).enhance(0.88)
	variant_c = ImageChops.offset(base.transpose(Image.Transpose.FLIP_LEFT_RIGHT), base.width // 3, base.height // 5)
	variant_b = make_seamless(variant_b, horizontal=True, vertical=True)
	variant_c = make_seamless(variant_c, horizontal=True, vertical=True)
	paths = [
		base_path.with_name("R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground_b.png"),
		base_path.with_name("R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground_c.png"),
	]
	variant_b.save(paths[0], format="PNG", optimize=True)
	variant_c.save(paths[1], format="PNG", optimize=True)
	return paths


def main() -> None:
	rows: list[dict[str, object]] = []
	for path in sorted(TEXTURE_DIR.glob("*.png")):
		if path.name in PLANET_VARIANT_NAMES:
			continue
		with Image.open(path) as source:
			image = source.convert("RGBA" if "A" in source.getbands() else "RGB")
		original_size = image.size
		image = resize_mobile(image)
		role = role_id(path)
		if role in TILE_BOTH:
			image = make_seamless(image, horizontal=True, vertical=True)
		elif role in TILE_HORIZONTAL:
			image = make_seamless(image, horizontal=True, vertical=False)
		image.save(path, format="PNG", optimize=True)
		rows.append(
			{
				"path": path.relative_to(ROOT).as_posix(),
				"original_size": list(original_size),
				"normalized_size": list(image.size),
				"tile_mode": "both" if role in TILE_BOTH else "horizontal" if role in TILE_HORIZONTAL else "isolated",
				**alpha_metrics(image),
			}
		)
	planet_base = TEXTURE_DIR / "R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground.png"
	if planet_base.exists():
		for path in build_planet_variants(planet_base):
			with Image.open(path) as image:
				rows.append(
					{
						"path": path.relative_to(ROOT).as_posix(),
						"original_size": list(image.size),
						"normalized_size": list(image.size),
						"tile_mode": "both_derived_variant",
						**alpha_metrics(image),
					}
				)
	REPORT.parent.mkdir(parents=True, exist_ok=True)
	REPORT.write_text(json.dumps({"asset_count": len(rows), "assets": rows}, indent=2) + "\n", encoding="utf-8")
	print(json.dumps({"asset_count": len(rows), "report": REPORT.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
	main()
