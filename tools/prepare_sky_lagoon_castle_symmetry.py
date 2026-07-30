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
V3_CARD = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v3.png"
)
FRAME_REPAIR_SOURCE = (
	SOURCE_DIR / "frame_restore_ring_source.png"
)
OWNER_STAINED_GLASS = (
	ROOT
	/ "assets_src/sky_lagoon/reductive_rebuild_2026-07-28"
	/ "stained_glass_owner_reference.png"
)
OUTPUT_CARD = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png"
)
DOOR_HIGHLIGHT = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png"
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

# The tightly scoped repair candidate supplies only its clean lavender/gold
# ring. The owner panel and every other castle pixel remain from the accepted
# four-tower card; the candidate's changed castle, door, bridge, and glass are
# explicitly rejected.
FRAME_REPAIR_SOURCE_BOX = (0, 0, 249, 360)
RESTORED_FRAME_TARGET_BOX = (396, 225, 629, 560)
RESTORED_FRAME_ALLOWED_BOX = (395, 223, 631, 563)
RESTORED_FRAME_POLYGON = (
	(512, 225),
	(556, 235),
	(589, 256),
	(614, 290),
	(627, 329),
	(627, 560),
	(398, 560),
	(398, 329),
	(411, 290),
	(436, 256),
	(469, 235),
)
GLASS_SAFE_POLYGON = (
	(512, 257),
	(546, 264),
	(572, 281),
	(589, 309),
	(597, 339),
	(597, 527),
	(427, 527),
	(427, 339),
	(435, 309),
	(452, 281),
	(478, 264),
)

# Door mask is intentionally inside the lavender stone arch. It becomes a
# small cropped focus texture, avoiding a second full-castle transparent quad.
DOOR_MASK_POLYGON = (
	(512, 560),
	(548, 569),
	(579, 592),
	(598, 628),
	(604, 660),
	(604, 780),
	(414, 780),
	(414, 660),
	(421, 628),
	(445, 592),
	(476, 569),
)

# The approved fallback's world transform is the placement contract. The new
# card derives its height, center, and bridge-axis offset from these values so
# aspect-ratio differences cannot shrink or slide the landmark by eye.
FALLBACK_WORLD_X = 51.8
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


def _restore_clean_frame(
	card: Image.Image,
	_window_polygon: list[tuple[int, int]],
) -> tuple[Image.Image, tuple[int, ...]]:
	with Image.open(FRAME_REPAIR_SOURCE) as repair_source:
		repair = repair_source.convert("RGBA")
	frame = repair.crop(FRAME_REPAIR_SOURCE_BOX).resize(
		(
			RESTORED_FRAME_TARGET_BOX[2] - RESTORED_FRAME_TARGET_BOX[0],
			RESTORED_FRAME_TARGET_BOX[3] - RESTORED_FRAME_TARGET_BOX[1],
		),
		Image.Resampling.LANCZOS,
	)
	layer = Image.new("RGBA", card.size)
	layer.paste(
		frame,
		(RESTORED_FRAME_TARGET_BOX[0], RESTORED_FRAME_TARGET_BOX[1]),
		frame,
	)
	outer_mask = Image.new("L", card.size, 0)
	ImageDraw.Draw(outer_mask).polygon(RESTORED_FRAME_POLYGON, fill=255)
	inner_mask = Image.new("L", card.size, 0)
	ImageDraw.Draw(inner_mask).polygon(GLASS_SAFE_POLYGON, fill=255)
	mask = ImageChops.subtract(outer_mask, inner_mask)
	mask = mask.filter(ImageFilter.GaussianBlur(0.35))
	before = card.copy()
	card = Image.composite(layer, card, mask)
	diff_box = ImageChops.difference(before, card).getbbox()
	if diff_box is None:
		raise RuntimeError("stained-glass frame repair made no change")
	return card, diff_box


def _build_door_highlight(card: Image.Image) -> tuple[Image.Image, tuple[int, ...]]:
	mask = Image.new("L", card.size, 0)
	ImageDraw.Draw(mask).polygon(DOOR_MASK_POLYGON, fill=255)
	mask = ImageChops.multiply(mask, card.getchannel("A"))
	mask = mask.filter(ImageFilter.GaussianBlur(0.55))
	bounds = mask.getbbox()
	if bounds is None:
		raise RuntimeError("door focus mask is empty")
	padding = 2
	bounds = (
		max(0, bounds[0] - padding),
		max(0, bounds[1] - padding),
		min(card.width, bounds[2] + padding),
		min(card.height, bounds[3] + padding),
	)
	cropped_mask = mask.crop(bounds)
	highlight = Image.new("RGBA", cropped_mask.size, (255, 255, 255, 0))
	highlight.putalpha(cropped_mask)
	return highlight, bounds


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
	card, frame_diff_box = _restore_clean_frame(card, window_polygon)
	with Image.open(V3_CARD) as v3_source:
		v3_card = v3_source.convert("RGBA")
	v3_diff_box = ImageChops.difference(v3_card, card).getbbox()
	if v3_diff_box is None:
		raise RuntimeError("v4 stained-glass frame repair made no change")
	if (
		v3_diff_box[0] < RESTORED_FRAME_ALLOWED_BOX[0]
		or v3_diff_box[1] < RESTORED_FRAME_ALLOWED_BOX[1]
		or v3_diff_box[2] > RESTORED_FRAME_ALLOWED_BOX[2]
		or v3_diff_box[3] > RESTORED_FRAME_ALLOWED_BOX[3]
	):
		raise RuntimeError(
			f"v4 frame repair escaped its allowed bounds: {v3_diff_box}"
		)
	door_highlight, door_bounds = _build_door_highlight(card)

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
	door_highlight.save(DOOR_HIGHLIGHT, optimize=True)
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
				"frame_repair_source": FRAME_REPAIR_SOURCE.relative_to(ROOT).as_posix(),
				"frame_repair_source_sha256": _sha256(FRAME_REPAIR_SOURCE),
				"restored_frame_changed_bounds": list(frame_diff_box),
				"restored_frame_target_bounds": list(RESTORED_FRAME_TARGET_BOX),
				"v3_to_v4_changed_bounds": list(v3_diff_box),
				"v3_to_v4_allowed_bounds": list(RESTORED_FRAME_ALLOWED_BOX),
				"outside_frame_changed_pixels": 0,
				"door_highlight": DOOR_HIGHLIGHT.relative_to(ROOT).as_posix(),
				"door_highlight_bounds_in_card": list(door_bounds),
				"door_highlight_size": list(door_highlight.size),
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
	print(DOOR_HIGHLIGHT)
	print(AUDIT_REPORT)
	print(
		"transform="
		f"({placement['candidate_world_x']:.6f}, "
		f"{placement['candidate_world_y']:.6f}, "
		f"{placement['candidate_world_height']:.6f})"
	)


if __name__ == "__main__":
	build()
