#!/usr/bin/env python3
"""Prepare the perspective-correct Sky Lagoon castle and restore owner glass."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src/sky_lagoon/castle_symmetry_2026-07-29"
RAW_CARD = SOURCE_DIR / "castle_perspective_transparent_raw.png"
OWNER_STAINED_GLASS = (
	ROOT
	/ "assets_src/sky_lagoon/reductive_rebuild_2026-07-28"
	/ "stained_glass_owner_reference.png"
)
OUTPUT_CARD = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_perspective_v2.png"
)
AUDIT_REPORT = ROOT / "audit/sky_lagoon_castle_perspective.json"

RAW_WINDOW_BOX = (532, 250, 726, 554)
RAW_WINDOW_POLYGON = (
	(623, 250),
	(664, 260),
	(695, 282),
	(716, 318),
	(726, 352),
	(726, 554),
	(532, 554),
	(532, 350),
	(541, 313),
	(560, 281),
	(589, 260),
)
OWNER_CROP = (101, 8, 780, 1176)
GUTTER = 10
MAX_EDGE = 1024


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _transform_point(
	point: tuple[int, int],
	crop_box: tuple[int, int, int, int],
	scale: float,
) -> tuple[int, int]:
	return (
		round((point[0] - crop_box[0]) * scale),
		round((point[1] - crop_box[1]) * scale),
	)


def _alpha_row_centroid(alpha: Image.Image, y: int) -> float:
	"""Return the coverage-weighted x center for one silhouette row."""
	row = alpha.crop((0, y, alpha.width, y + 1))
	values = [row.getpixel((x, 0)) for x in range(row.width)]
	total = sum(values)
	if total == 0:
		raise RuntimeError(f"castle has no visible pixels on audit row {y}")
	return sum(x * value for x, value in enumerate(values)) / float(total)


def build() -> None:
	with Image.open(RAW_CARD) as source:
		raw = source.convert("RGBA")
	alpha_box = raw.getchannel("A").getbbox()
	if alpha_box is None:
		raise RuntimeError("balanced castle source has no visible pixels")
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
	bridge_audit_y = round(card.height * 0.88)
	bridge_centroid_x = _alpha_row_centroid(alpha, bridge_audit_y)
	bridge_offset_ratio = (
		(card.width * 0.5 - bridge_centroid_x) / float(card.width)
	)
	if bridge_offset_ratio < 0.10:
		raise RuntimeError(
			"castle lost its oblique in-scene bridge perspective: "
			f"offset={bridge_offset_ratio:.5f}"
		)
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
				"projection": "oblique_three_quarter",
				"bridge_audit_row": bridge_audit_y,
				"bridge_centroid_x": bridge_centroid_x,
				"bridge_left_offset_ratio": bridge_offset_ratio,
				"oblique_bridge_pass": bridge_offset_ratio >= 0.10,
				"mobile_max_edge_pass": max(card.size) <= MAX_EDGE,
				"transparent_gutter_pass": True,
			},
			indent=2,
		)
		+ "\n",
		encoding="utf-8",
	)
	print(OUTPUT_CARD)
	print(AUDIT_REPORT)


if __name__ == "__main__":
	build()
