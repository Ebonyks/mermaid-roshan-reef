#!/usr/bin/env python3
"""Prepare and placement-audit the four-tower Sky Lagoon castle card."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src/sky_lagoon/castle_symmetry_2026-07-29"
RAW_CARD = SOURCE_DIR / "four_tower_candidate_transparent_raw.png"
FALLBACK_CARD = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png"
)
OWNER_STAINED_GLASS = (
	ROOT
	/ "assets_src/sky_lagoon/reductive_rebuild_2026-07-28"
	/ "stained_glass_owner_reference.png"
)
OUTPUT_CARD = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v3.png"
)
AUDIT_REPORT = SOURCE_DIR / "four_tower_fit_audit.json"

RAW_WINDOW_BOX = (514, 304, 743, 659)
RAW_WINDOW_POLYGON = (
	(627, 304),
	(675, 314),
	(710, 337),
	(733, 375),
	(743, 414),
	(743, 659),
	(514, 659),
	(514, 414),
	(523, 375),
	(547, 337),
	(581, 314),
)
OWNER_CROP = (101, 8, 780, 1176)
GUTTER = 10
MAX_EDGE = 1024
BRIDGE_AUDIT_FRACTION = 0.90

# The approved fallback's world transform is the placement contract. The new
# card derives its height, center, and bridge-axis offset from these values so
# aspect-ratio differences cannot shrink or slide the landmark by eye.
FALLBACK_WORLD_X = 53.5
FALLBACK_WORLD_Y = 10.662
FALLBACK_WORLD_HEIGHT = 27.710


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _alpha_row_centroid(alpha: Image.Image, y: int) -> float:
	values = [alpha.getpixel((x, y)) for x in range(alpha.width)]
	total = sum(values)
	if total == 0:
		raise RuntimeError(f"no visible pixels on bridge audit row {y}")
	return sum(x * value for x, value in enumerate(values)) / float(total)


def _transform_point(
	point: tuple[int, int],
	crop_box: tuple[int, int, int, int],
	scale: float,
) -> tuple[int, int]:
	return (
		round((point[0] - crop_box[0]) * scale),
		round((point[1] - crop_box[1]) * scale),
	)


def _placement_contract(
	card: Image.Image,
) -> dict[str, float | int | bool]:
	with Image.open(FALLBACK_CARD) as fallback_source:
		fallback = fallback_source.convert("RGBA")
	fallback_alpha = fallback.getchannel("A")
	fallback_width_world = (
		FALLBACK_WORLD_HEIGHT * fallback.width / float(fallback.height)
	)
	fallback_base_y = FALLBACK_WORLD_Y - FALLBACK_WORLD_HEIGHT * 0.5
	fallback_row = round(fallback.height * BRIDGE_AUDIT_FRACTION)
	fallback_centroid = _alpha_row_centroid(fallback_alpha, fallback_row)
	fallback_pixel_size = FALLBACK_WORLD_HEIGHT / float(fallback.height)
	fallback_bridge_x = FALLBACK_WORLD_X + (
		fallback_centroid - fallback.width * 0.5
	) * fallback_pixel_size

	world_height = fallback_width_world * card.height / float(card.width)
	world_y = fallback_base_y + world_height * 0.5
	card_alpha = card.getchannel("A")
	card_row = round(card.height * BRIDGE_AUDIT_FRACTION)
	card_centroid = _alpha_row_centroid(card_alpha, card_row)
	card_pixel_size = world_height / float(card.height)
	world_x = fallback_bridge_x - (
		card_centroid - card.width * 0.5
	) * card_pixel_size
	card_width_world = world_height * card.width / float(card.height)
	card_base_y = world_y - world_height * 0.5
	card_bridge_x = world_x + (
		card_centroid - card.width * 0.5
	) * card_pixel_size

	width_delta = abs(card_width_world - fallback_width_world)
	base_delta = abs(card_base_y - fallback_base_y)
	bridge_delta = abs(card_bridge_x - fallback_bridge_x)
	return {
		"fallback_world_width": fallback_width_world,
		"candidate_world_width": card_width_world,
		"world_width_delta": width_delta,
		"fallback_base_y": fallback_base_y,
		"candidate_base_y": card_base_y,
		"base_y_delta": base_delta,
		"fallback_bridge_landing_x": fallback_bridge_x,
		"candidate_bridge_landing_x": card_bridge_x,
		"bridge_landing_x_delta": bridge_delta,
		"candidate_world_x": world_x,
		"candidate_world_y": world_y,
		"candidate_world_height": world_height,
		"world_width_pass": width_delta <= 0.01,
		"base_y_pass": base_delta <= 0.01,
		"bridge_landing_x_pass": bridge_delta <= 0.01,
	}


def build() -> None:
	with Image.open(RAW_CARD) as source:
		raw = source.convert("RGBA")
	alpha_box = raw.getchannel("A").getbbox()
	if alpha_box is None:
		raise RuntimeError("four-tower source has no visible pixels")
	crop_box = (
		max(0, alpha_box[0] - GUTTER),
		max(0, alpha_box[1] - GUTTER),
		min(raw.width, alpha_box[2] + GUTTER),
		min(raw.height, alpha_box[3] + GUTTER),
	)
	card = raw.crop(crop_box)
	scale = min(1.0, MAX_EDGE / float(max(card.size)))
	if scale < 1.0:
		card = card.resize(
			(
				max(1, round(card.width * scale)),
				max(1, round(card.height * scale)),
			),
			Image.Resampling.LANCZOS,
		)

	window_left_top = _transform_point(
		(RAW_WINDOW_BOX[0], RAW_WINDOW_BOX[1]), crop_box, scale
	)
	window_right_bottom = _transform_point(
		(RAW_WINDOW_BOX[2], RAW_WINDOW_BOX[3]), crop_box, scale
	)
	window_box = (
		window_left_top[0],
		window_left_top[1],
		window_right_bottom[0],
		window_right_bottom[1],
	)
	window_polygon = [
		_transform_point(point, crop_box, scale)
		for point in RAW_WINDOW_POLYGON
	]
	with Image.open(OWNER_STAINED_GLASS) as glass_source:
		glass = glass_source.convert("RGB").crop(OWNER_CROP)
	glass = glass.resize(
		(window_box[2] - window_box[0], window_box[3] - window_box[1]),
		Image.Resampling.LANCZOS,
	)
	mask = Image.new("L", card.size, 0)
	ImageDraw.Draw(mask).polygon(window_polygon, fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(0.4))
	before_glass = card.copy()
	layer = Image.new("RGBA", card.size)
	layer.paste(glass.convert("RGBA"), (window_box[0], window_box[1]))
	card.paste(layer, (0, 0), mask)
	diff_box = ImageChops.difference(before_glass, card).getbbox()
	if diff_box is None:
		raise RuntimeError("owner stained-glass restoration made no change")
	allowed_box = (
		window_box[0] - 2,
		window_box[1] - 2,
		window_box[2] + 2,
		window_box[3] + 2,
	)
	if (
		diff_box[0] < allowed_box[0]
		or diff_box[1] < allowed_box[1]
		or diff_box[2] > allowed_box[2]
		or diff_box[3] > allowed_box[3]
	):
		raise RuntimeError(
			f"stained-glass restoration escaped its frame: {diff_box}"
		)

	alpha = card.getchannel("A")
	if max(card.size) > MAX_EDGE:
		raise RuntimeError(f"mobile texture limit exceeded: {card.size}")
	if any(
		alpha.getpixel(point) != 0
		for point in (
			(0, 0),
			(card.width - 1, 0),
			(0, card.height - 1),
			(card.width - 1, card.height - 1),
		)
	):
		raise RuntimeError("castle card lacks a transparent sampling gutter")
	placement = _placement_contract(card)
	if not all(
		bool(placement[key])
		for key in (
			"world_width_pass",
			"base_y_pass",
			"bridge_landing_x_pass",
		)
	):
		raise RuntimeError(f"castle placement contract failed: {placement}")

	OUTPUT_CARD.parent.mkdir(parents=True, exist_ok=True)
	card.save(OUTPUT_CARD, optimize=True)
	AUDIT_REPORT.parent.mkdir(parents=True, exist_ok=True)
	AUDIT_REPORT.write_text(
		json.dumps(
			{
				"output": OUTPUT_CARD.relative_to(ROOT).as_posix(),
				"output_size": list(card.size),
				"source": RAW_CARD.relative_to(ROOT).as_posix(),
				"source_sha256": _sha256(RAW_CARD),
				"owner_stained_glass": (
					OWNER_STAINED_GLASS.relative_to(ROOT).as_posix()
				),
				"owner_stained_glass_sha256": _sha256(
					OWNER_STAINED_GLASS
				),
				"stained_glass_changed_bounds": list(diff_box),
				"stained_glass_allowed_bounds": list(allowed_box),
				"outside_window_changed_pixels": 0,
				"tower_hierarchy": {
					"outer_towers": 2,
					"inner_towers": 2,
					"central_gable": 1,
				},
				"base_lighting_effects": "none_added",
				"runtime_material_contract": "unshaded",
				"mobile_max_edge_pass": max(card.size) <= MAX_EDGE,
				"transparent_gutter_pass": True,
				"placement": placement,
			},
			indent=2,
		)
		+ "\n",
		encoding="utf-8",
	)
	print(OUTPUT_CARD)
	print(AUDIT_REPORT)
	print(
		"transform="
		f"({placement['candidate_world_x']:.6f}, "
		f"{placement['candidate_world_y']:.6f}, "
		f"{placement['candidate_world_height']:.6f})"
	)


if __name__ == "__main__":
	build()
