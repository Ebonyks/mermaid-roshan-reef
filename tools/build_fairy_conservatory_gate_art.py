#!/usr/bin/env python3
"""Build the plot-available Butterfly Gate card for the Pearl Castle Hall.

The dormant state remains the approved minimal Moonflower relief.  Once the
Chapter 3 plot reveals the route, the exact approved Butterfly House facade
becomes the castle gate and its greenhouse aperture is replaced with the
approved upright sunrise Lily-Pad Fairy World.  No rainbow causeway is used in
the castle doorway.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = (
	ROOT / "assets_src" / "castle"
	/ "fairy_conservatory_gate_available_2026-08-30"
)
ALPHA_ROOT = SOURCE_ROOT / "alpha"
REVIEW_ROOT = SOURCE_ROOT / "review"
MANIFEST_PATH = SOURCE_ROOT / "asset_manifest.json"
RUNTIME_ROOT = ROOT / "assets" / "flats" / "castle" / "fairy_conservatory"

DORMANT_SOURCE = RUNTIME_ROOT / "moonflower_door_closed.png"
GATE_SOURCE = (
	ROOT / "assets" / "flats" / "fairy_conservatory_handoff"
	/ "butterfly_house.png"
)
BACKGROUND_MASTER = (
	ROOT / "assets_src" / "fairy_conservatory_handoff_2026-08-30"
	/ "masters" / "handoff_background_master_3640x2048.png"
)
LILY_CLUSTER_SOURCE = ROOT / "assets" / "fairy" / "sprites" / "ornament_lily_cluster.png"
RUNTIME_PATH = RUNTIME_ROOT / "butterfly_gate_available.png"
ALPHA_PATH = ALPHA_ROOT / "butterfly_gate_available_alpha_master.png"

CANVAS_EDGE = 1024
TARGET_FOOT_Y = 992

# Clear interior of the approved Butterfly House's cream-and-purple arch.
# Coordinates are measured on the unshifted 1024-square runtime cutout; the
# complete approved facade is translated only far enough to share the dormant
# door's exact floor foot.
APERTURE_LEFT = 389
APERTURE_RIGHT = 638
APERTURE_TOP = 448
APERTURE_SPRING = 570
APERTURE_BOTTOM = 901

HALL_TILE_PATTERN = (
	ROOT / "assets" / "flats" / "castle"
	/ "main_hall_redraw_2026-08-03" / "tiles"
	/ "main_hall_room_led_r{row}_c{column}.png"
)
HALL_LOGICAL_SIZE = (3344, 941)
HALL_REVIEW_LEFT = 836
HALL_REVIEW_WIDTH = 1672
HALL_FOOT = (1672.0, 620.0)
DORMANT_CARD_SCALE = 0.4896
AVAILABLE_CARD_SCALE = 0.5372
DORMANT_CARD_CENTER = (1672.0, 385.0)
AVAILABLE_CARD_CENTER = (
	1672.0,
	HALL_FOOT[1] - (TARGET_FOOT_Y - CANVAS_EDGE * 0.5) * AVAILABLE_CARD_SCALE,
)


def _hash(path: Path) -> str:
	digest = sha256()
	with path.open("rb") as source:
		for block in iter(lambda: source.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def _audit(card: Image.Image) -> dict[str, object]:
	if card.size != (CANVAS_EDGE, CANVAS_EDGE):
		raise ValueError(f"gate card has wrong size: {card.size}")
	if card.mode != "RGBA":
		raise ValueError(f"gate card is not RGBA: {card.mode}")
	alpha = np.asarray(card.getchannel("A"), dtype=np.uint8)
	corners = [
		int(alpha[0, 0]), int(alpha[0, -1]),
		int(alpha[-1, 0]), int(alpha[-1, -1]),
	]
	if any(corners):
		raise ValueError(f"gate card corners are not transparent: {corners}")
	bounds = card.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError("gate card has no visible subject")
	if bounds[3] != TARGET_FOOT_Y:
		raise ValueError(
			f"gate foot {bounds[3]} does not match dormant foot {TARGET_FOOT_Y}")
	return {
		"dimensions": list(card.size),
		"alpha_bbox": list(bounds),
		"corner_alpha": corners,
		"visible_alpha_pixels": int(np.count_nonzero(alpha)),
	}


def _registered_gate() -> tuple[Image.Image, int]:
	if not GATE_SOURCE.is_file():
		raise FileNotFoundError(GATE_SOURCE)
	gate = Image.open(GATE_SOURCE).convert("RGBA")
	if gate.size != (CANVAS_EDGE, CANVAS_EDGE):
		raise ValueError(f"unexpected Butterfly Gate size: {gate.size}")
	bounds = gate.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError("approved Butterfly Gate has no alpha subject")
	shift_y = TARGET_FOOT_Y - bounds[3]
	if shift_y < 0:
		raise ValueError(f"approved Butterfly Gate exceeds target foot: {bounds}")
	card = Image.new("RGBA", gate.size, (0, 0, 0, 0))
	card.alpha_composite(gate, (0, shift_y))
	return card, shift_y


def _aperture_mask(shift_y: int) -> Image.Image:
	mask = Image.new("L", (CANVAS_EDGE, CANVAS_EDGE), 0)
	draw = ImageDraw.Draw(mask)
	draw.pieslice(
		(
			APERTURE_LEFT,
			APERTURE_TOP + shift_y,
			APERTURE_RIGHT,
			APERTURE_SPRING * 2 - APERTURE_TOP + shift_y,
		),
		start=180,
		end=360,
		fill=255,
	)
	draw.rectangle(
		(
			APERTURE_LEFT,
			APERTURE_SPRING + shift_y,
			APERTURE_RIGHT,
			APERTURE_BOTTOM + shift_y,
		),
		fill=255,
	)
	return mask.filter(ImageFilter.GaussianBlur(0.55))


def _upright_lily_portal(shift_y: int) -> tuple[Image.Image, dict[str, object]]:
	if not BACKGROUND_MASTER.is_file():
		raise FileNotFoundError(BACKGROUND_MASTER)
	background = Image.open(BACKGROUND_MASTER).convert("RGBA")
	portal_width = APERTURE_RIGHT - APERTURE_LEFT
	portal_height = APERTURE_BOTTOM - APERTURE_TOP
	portal = ImageOps.fit(
		background,
		(portal_width, portal_height),
		method=Image.Resampling.LANCZOS,
		centering=(0.5, 0.5),
	)
	layer = Image.new("RGBA", (CANVAS_EDGE, CANVAS_EDGE), (0, 0, 0, 0))
	layer.alpha_composite(portal, (APERTURE_LEFT, APERTURE_TOP + shift_y))
	if not LILY_CLUSTER_SOURCE.is_file():
		raise FileNotFoundError(LILY_CLUSTER_SOURCE)
	lily_cluster = Image.open(LILY_CLUSTER_SOURCE).convert("RGBA")
	lily_bounds = lily_cluster.getchannel("A").getbbox()
	if lily_bounds is None:
		raise ValueError("approved lily cluster has no alpha subject")
	lily_cluster = lily_cluster.crop(lily_bounds)
	lily_edge = 176
	lily_scale = lily_edge / max(lily_cluster.size)
	lily_cluster = lily_cluster.resize(
		(
			max(1, round(lily_cluster.width * lily_scale)),
			max(1, round(lily_cluster.height * lily_scale)),
		),
		Image.Resampling.LANCZOS,
	)
	lily_left = round((APERTURE_LEFT + APERTURE_RIGHT - lily_cluster.width) * 0.5)
	lily_top = APERTURE_BOTTOM + shift_y - lily_cluster.height
	layer.alpha_composite(lily_cluster, (lily_left, lily_top))
	# The accepted handoff master records its aligned horizon at 778/2048.
	source_horizon_y = 778
	portal_horizon_y = round(source_horizon_y / background.height * portal_height)
	return layer, {
		"location_authority": "Lily-Pad Fairy World / Fairy Pond",
		"source_dimensions": list(background.size),
		"source_horizon_y": source_horizon_y,
		"source_horizon_fraction": source_horizon_y / background.height,
		"portal_dimensions": [portal_width, portal_height],
		"portal_horizon_y": APERTURE_TOP + shift_y + portal_horizon_y,
		"portal_horizon_fraction": portal_horizon_y / portal_height,
		"source_pixel_upscale": False,
		"crop_alignment": "centered upright portrait crop; whole crop uniformly downsampled",
		"foreground_lily_cluster": {
			"path": LILY_CLUSTER_SOURCE.relative_to(ROOT).as_posix(),
			"whole_sprite_uniform_edge": lily_edge,
			"threshold_foot_y": APERTURE_BOTTOM + shift_y,
		},
	}


def _compose_available_gate() -> tuple[Image.Image, dict[str, object]]:
	gate, shift_y = _registered_gate()
	mask = _aperture_mask(shift_y)
	architecture = gate.copy()
	architecture_alpha = np.asarray(
		architecture.getchannel("A"), dtype=np.uint8).copy()
	mask_array = np.asarray(mask, dtype=np.uint8)
	architecture_alpha[mask_array >= 128] = 0
	architecture.putalpha(Image.fromarray(architecture_alpha, "L"))

	portal, portal_record = _upright_lily_portal(shift_y)
	portal.putalpha(mask)
	result = portal.copy()
	result.alpha_composite(architecture)

	# Outside the intentionally replaced aperture, every visible source pixel is
	# the exact approved Butterfly House facade translated by ``shift_y``.
	gate_pixels = np.asarray(gate, dtype=np.uint8)
	result_pixels = np.asarray(result, dtype=np.uint8)
	outside = mask_array == 0
	if not np.array_equal(gate_pixels[outside], result_pixels[outside]):
		raise ValueError("Butterfly Gate pixels changed outside the aperture")
	portal_record.update({
		"gate_y_shift": shift_y,
		"aperture": {
			"left": APERTURE_LEFT,
			"right": APERTURE_RIGHT,
			"top": APERTURE_TOP + shift_y,
			"spring": APERTURE_SPRING + shift_y,
			"bottom": APERTURE_BOTTOM + shift_y,
		},
		"threshold_matches_aperture_base": True,
		"rainbow_walkway_delivery_pixels": False,
		"greenhouse_interior_delivery_pixels": False,
	})
	return result, portal_record


def _approved_hall_logical() -> tuple[Image.Image, list[Path]]:
	panorama = Image.new("RGB", (7280, 2048))
	inputs: list[Path] = []
	for row in range(2):
		for column in range(8):
			path = Path(str(HALL_TILE_PATTERN).format(row=row, column=column))
			if not path.is_file():
				raise FileNotFoundError(path)
			tile = Image.open(path).convert("RGB")
			if tile.size != (910, 1024):
				raise ValueError(f"unexpected Main Hall tile: {path} {tile.size}")
			panorama.paste(tile, (column * 910, row * 1024))
			inputs.append(path)
	logical = panorama.resize(HALL_LOGICAL_SIZE, Image.Resampling.LANCZOS)
	return logical.convert("RGBA"), inputs


def _hall_review(
		hall: Image.Image, card: Image.Image, state: str,
		center: tuple[float, float], scale: float) -> Path:
	placed = hall.copy()
	edge = round(CANVAS_EDGE * scale)
	fitted = card.resize((edge, edge), Image.Resampling.LANCZOS)
	placed.alpha_composite(
		fitted,
		(round(center[0] - edge * 0.5), round(center[1] - edge * 0.5)),
	)
	crop = placed.crop((
		HALL_REVIEW_LEFT,
		0,
		HALL_REVIEW_LEFT + HALL_REVIEW_WIDTH,
		HALL_LOGICAL_SIZE[1],
	)).resize((1280, 720), Image.Resampling.LANCZOS)
	REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
	path = REVIEW_ROOT / f"fairy_conservatory_{state}_hall_1280x720.png"
	crop.save(path, format="PNG", optimize=True)
	return path


def main() -> None:
	ALPHA_ROOT.mkdir(parents=True, exist_ok=True)
	RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
	available, portal_record = _compose_available_gate()
	available.save(ALPHA_PATH, format="PNG", optimize=True)
	available.save(RUNTIME_PATH, format="PNG", optimize=True)
	audit = _audit(available)

	hall, hall_inputs = _approved_hall_logical()
	dormant = Image.open(DORMANT_SOURCE).convert("RGBA")
	dormant_review = _hall_review(
		hall, dormant, "dormant", DORMANT_CARD_CENTER, DORMANT_CARD_SCALE)
	available_review = _hall_review(
		hall, available, "available", AVAILABLE_CARD_CENTER,
		AVAILABLE_CARD_SCALE)

	manifest = {
		"schema": 1,
		"purpose": "Chapter 3 Pearl Castle dormant-to-available Butterfly Gate state correction",
		"generation_method": "deterministic composite of approved project artwork",
		"state_mapping": {
			"closed": "approved minimal Moonflower relief",
			"revealed": "available Butterfly Gate with sunrise Lily-Pad Fairy World",
			"open": "same available Butterfly Gate; route entry does not alter its identity",
		},
		"approved_inputs": [
			{
				"role": "dormant castle door",
				"path": DORMANT_SOURCE.relative_to(ROOT).as_posix(),
				"sha256": _hash(DORMANT_SOURCE),
			},
			{
				"role": "Butterfly Door Gate architecture",
				"path": GATE_SOURCE.relative_to(ROOT).as_posix(),
				"sha256": _hash(GATE_SOURCE),
			},
			{
				"role": "sunrise Lily-Pad Fairy World portal view",
				"path": BACKGROUND_MASTER.relative_to(ROOT).as_posix(),
				"sha256": _hash(BACKGROUND_MASTER),
			},
			{
				"role": "foreground lily-pad threshold cluster",
				"path": LILY_CLUSTER_SOURCE.relative_to(ROOT).as_posix(),
				"sha256": _hash(LILY_CLUSTER_SOURCE),
			},
		],
		"excluded_inputs": [
			"assets/flats/fairy_conservatory_handoff/rainbow_walkway.png",
			"the Butterfly House greenhouse corridor formerly visible inside the gate aperture",
		],
		"runtime": {
			"path": RUNTIME_PATH.relative_to(ROOT).as_posix(),
			"sha256": _hash(RUNTIME_PATH),
			"alpha_master": ALPHA_PATH.relative_to(ROOT).as_posix(),
			"alpha_master_sha256": _hash(ALPHA_PATH),
			"audit": audit,
			"portal_composition": portal_record,
		},
		"placement": {
			"floor_foot": list(HALL_FOOT),
			"dormant_center": list(DORMANT_CARD_CENTER),
			"dormant_scale": DORMANT_CARD_SCALE,
			"available_center": list(AVAILABLE_CARD_CENTER),
			"available_scale": AVAILABLE_CARD_SCALE,
			"plot_reveal_is_dramatic_state_change": True,
		},
		"hall_review_inputs": [
			{"path": path.relative_to(ROOT).as_posix(), "sha256": _hash(path)}
			for path in hall_inputs
		],
		"reviews": {
			"dormant": {
				"path": dormant_review.relative_to(ROOT).as_posix(),
				"sha256": _hash(dormant_review),
				"dimensions": [1280, 720],
				"delivery_pixels": False,
			},
			"available": {
				"path": available_review.relative_to(ROOT).as_posix(),
				"sha256": _hash(available_review),
				"dimensions": [1280, 720],
				"delivery_pixels": False,
			},
		},
	}
	MANIFEST_PATH.write_text(
		json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(f"wrote {RUNTIME_PATH.relative_to(ROOT)} sha256={_hash(RUNTIME_PATH)}")
	print(f"wrote {dormant_review.relative_to(ROOT)}")
	print(f"wrote {available_review.relative_to(ROOT)}")
	print(f"wrote {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
	main()
