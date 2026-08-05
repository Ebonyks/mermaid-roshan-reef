#!/usr/bin/env python3
"""Constrain Pearl Castle clean-plate healing to live rendered silhouettes.

The approved 1024x576 room composites are immutable inputs.  Earlier clean
plates correctly removed the extracted source cards, but the normalized V2/V4
animation states do not always have the same silhouette as those source cards.
That mismatch exposed scanline-fill bands around the live objects.

For every tiled single-screen room this tool rebuilds the native baseline as:

* approved full-room pixels outside the actually rendered legacy union;
* existing clean-plate fill inside active V2 frame unions and static mid/front
  cards only.

V4 source-owned objects are healed by the V4 delivery builder after these
baselines land.  ``--check`` reconstructs the selected runtime tiles (V4 when
routed, otherwise the canonical baseline) and requires zero changed pixels
outside the combined static + active V2 + active V4 live-alpha union.

No approved full-room image or logical clean plate is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import distance_transform_edt


ROOT = Path(__file__).resolve().parents[1]
ROOM_ROOT = ROOT / "assets" / "flats" / "castle" / "rooms"
MASTER_ROOT = ROOT / "assets_src" / "castle" / "room_backgrounds_2k"
FABLE_MANIFEST = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
V2_MANIFEST = (
	ROOT / "assets" / "flats" / "castle" / "interactions_v2"
	/ "castle_interactions_v2.json")
V4_MANIFEST = (
	ROOT / "assets" / "flats" / "castle" / "interactions_v4"
	/ "castle_interactions_v4.json")
PROVENANCE_PATH = (
	MASTER_ROOT / "castle_live_alpha_baseline_repair.json")
CONTACT_PATH = (
	ROOT / "audit" / "castle_sprite3d"
	/ "castle_live_alpha_baseline_repair_contact.png")
TOOL_PATH = "tools/repair_castle_room_native_backgrounds.py"

ROOM_IDS = (
	"opera_hall",
	"kitchen",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
)
LOGICAL_SIZE = (1024, 576)
STATIC_ROLES = {"foreground", "midground"}
# The Pool water oval was retired from ROOM_LAYOUTS because it is scenery, not
# a foreground occluder.  Keeping its old FABLE midground mask here preserved
# the crude scanline clean plate across nearly the whole pool even after the
# runtime card was removed.  The water now stays flattened into the background.
RETIRED_STATIC_CARDS = {("mermaid_pool", "mid_pool")}
# Every world card is ALPHA_CUT_DISCARD with alpha_scissor_threshold = 0.5.
# Use the same threshold after frame placement/filtering so the repair envelope
# describes pixels that can actually write color/depth at runtime.
LIVE_ALPHA_THRESHOLD = 128
# Source-card crops normally equal ROOM_ITEMS positions.  The accepted Library
# book stack is intentionally inset 13 logical pixels from its wider source
# card, and the runtime registry is authoritative for that one placement.
V2_POSITION_OVERRIDES = {
	("library", "book_stack"): (13.0, 365.0),
}


def _sha256_bytes(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


def _sha256(path: Path) -> str:
	return _sha256_bytes(path.read_bytes())


def _raw_sha256(image: Image.Image) -> str:
	return _sha256_bytes(image.tobytes())


def _relative(path: Path) -> str:
	return path.relative_to(ROOT).as_posix()


def _png_bytes(image: Image.Image) -> bytes:
	stream = io.BytesIO()
	image.save(stream, format="PNG", optimize=True)
	return stream.getvalue()


def _atomic_write(path: Path, data: bytes) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	temporary = path.with_name(path.name + ".tmp")
	temporary.write_bytes(data)
	temporary.replace(path)


def _load_json(path: Path) -> dict[str, Any]:
	parsed = json.loads(path.read_text(encoding="utf-8"))
	if not isinstance(parsed, dict):
		raise ValueError(f"{path} must contain a JSON object")
	return parsed


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
	# Pillow 12.3.0 is pinned in CI. Its bundled default face is identical on
	# Windows and Linux, unlike an OS-font lookup whose pixels would invalidate
	# the provenance contact hash on a fresh Ubuntu runner.
	_ = bold
	return ImageFont.load_default(size=size)


def _binary_mask(mask: Image.Image) -> Image.Image:
	values = np.asarray(mask.convert("L"), dtype=np.uint8)
	return Image.fromarray(
		(values >= LIVE_ALPHA_THRESHOLD).astype(np.uint8) * 255,
		mode="L")


def _mask_metrics(mask: Image.Image) -> dict[str, Any]:
	values = np.asarray(mask, dtype=np.uint8)
	bbox = mask.getbbox()
	return {
		"bbox": list(bbox) if bbox is not None else None,
		"owned_pixels": int(np.count_nonzero(values)),
		"raw_pixel_sha256": _raw_sha256(mask),
	}


def _frame_union(entry: dict[str, Any], position: tuple[float, float]
		) -> tuple[Image.Image, dict[str, Any]]:
	sheet_path = ROOT / str(entry["sheet"])
	if not sheet_path.exists():
		raise FileNotFoundError(sheet_path)
	actual_sheet_hash = _sha256(sheet_path)
	declared_sheet_hash = str(entry.get("sheet_sha256", ""))
	if declared_sheet_hash and actual_sheet_hash != declared_sheet_hash:
		raise ValueError(f"sheet hash mismatch: {sheet_path}")

	grid = entry.get("grid", [])
	if not isinstance(grid, list) or len(grid) != 2:
		grid = [entry.get("hframes", 0), entry.get("vframes", 0)]
	columns, rows = int(grid[0]), int(grid[1])
	if columns <= 0 or rows <= 0:
		raise ValueError(f"invalid frame grid for {entry.get('id')}: {grid}")

	sheet = Image.open(sheet_path).convert("RGBA")
	if sheet.width % columns or sheet.height % rows:
		raise ValueError(f"sheet does not divide by grid: {sheet_path}")
	frame_width = sheet.width // columns
	frame_height = sheet.height // rows
	declared_cell = entry.get("cell_size", [frame_width, frame_height])
	if [frame_width, frame_height] != [int(value) for value in declared_cell]:
		raise ValueError(f"cell-size mismatch for {entry.get('id')}")
	frame_count = int(entry.get(
		"authored_frame_count", entry.get("frame_count", 0)))
	if frame_count < 1 or frame_count > columns * rows:
		raise ValueError(f"invalid frame count for {entry.get('id')}")

	runtime_scale = float(entry.get("runtime_scale", 1.0))
	if runtime_scale <= 0.0:
		raise ValueError(f"invalid runtime scale for {entry.get('id')}")
	center_offset = entry.get(
		"runtime_center_offset", [frame_width * 0.5, frame_height * 0.5])
	center_x = position[0] + float(center_offset[0])
	center_y = position[1] + float(center_offset[1])
	union = Image.new("L", LOGICAL_SIZE, 0)
	for frame_index in range(frame_count):
		column = frame_index % columns
		row = frame_index // columns
		frame_alpha = sheet.crop((
			column * frame_width,
			row * frame_height,
			(column + 1) * frame_width,
			(row + 1) * frame_height,
		)).getchannel("A")
		# Sprite3D centers each atlas cell.  This inverse affine reproduces the
		# exact room-space center/scale used by castle_rooms_25d.gd.
		placed = frame_alpha.transform(
			LOGICAL_SIZE,
			Image.Transform.AFFINE,
			(
				1.0 / runtime_scale,
				0.0,
				frame_width * 0.5 - center_x / runtime_scale,
				0.0,
				1.0 / runtime_scale,
				frame_height * 0.5 - center_y / runtime_scale,
			),
			resample=Image.Resampling.BILINEAR,
		)
		union = ImageChops.lighter(union, placed)
	union = _binary_mask(union)
	record = {
		"asset_id": str(entry.get("id", "")),
		"frame_count": frame_count,
		"grid": [columns, rows],
		"position": [position[0], position[1]],
		"runtime_center_offset": [
			float(center_offset[0]), float(center_offset[1])],
		"runtime_scale": runtime_scale,
		"sheet": _relative(sheet_path),
		"sheet_sha256": actual_sheet_hash,
		"union": _mask_metrics(union),
	}
	return union, record


def _static_union(room_id: str, room_record: dict[str, Any]
		) -> tuple[Image.Image, list[dict[str, Any]]]:
	union = Image.new("L", LOGICAL_SIZE, 0)
	records: list[dict[str, Any]] = []
	for card in room_record.get("cards", []):
		if str(card.get("role", "")) not in STATIC_ROLES:
			continue
		card_id = str(card["id"])
		if not _static_card_is_active(room_id, card_id):
			continue
		crop = [int(value) for value in card["crop"]]
		if len(crop) != 4:
			raise ValueError(f"invalid static crop: {room_id}:{card_id}")
		path = ROOM_ROOT / f"room_{room_id}_{card_id}.png"
		card_image = Image.open(path).convert("RGBA")
		expected_size = (crop[2] - crop[0], crop[3] - crop[1])
		if card_image.size != expected_size:
			raise ValueError(
				f"static-card size mismatch: {path} is {card_image.size}, "
				f"expected {expected_size}")
		local = Image.new("L", LOGICAL_SIZE, 0)
		local.paste(_binary_mask(card_image.getchannel("A")), crop[:2])
		union = ImageChops.lighter(union, local)
		records.append({
			"id": card_id,
			"role": str(card["role"]),
			"crop": crop,
			"path": _relative(path),
			"sha256": _sha256(path),
			"mask": _mask_metrics(local),
		})
	return union, records


def _static_card_is_active(room_id: str, card_id: str) -> bool:
	"""Mirror the explicit static-card retirements in ROOM_LAYOUTS."""
	return (room_id, card_id) not in RETIRED_STATIC_CARDS


def _item_cards(room_record: dict[str, Any]) -> dict[str, dict[str, Any]]:
	return {
		str(card["id"]): card
		for card in room_record.get("cards", [])
		if str(card.get("role", "")) == "item"
	}


def _active_v4_entries(v4: dict[str, Any], room_id: str
		) -> list[dict[str, Any]]:
	routes = v4.get("runtime_background_tiles", {})
	if room_id not in routes:
		return []
	return [
		entry for entry in v4.get("assets", [])
		if str(entry.get("room", "")) == room_id
	]


def _live_unions(room_id: str, room_record: dict[str, Any],
		v2: dict[str, Any], v4: dict[str, Any]
		) -> tuple[Image.Image, Image.Image, dict[str, Any]]:
	static_mask, static_records = _static_union(room_id, room_record)
	legacy_union = static_mask.copy()
	final_union = static_mask.copy()
	visual_records: list[dict[str, Any]] = []
	active_v4 = _active_v4_entries(v4, room_id)
	overridden_instances = {
		str(instance)
		for entry in active_v4
		for instance in entry.get("instances", [])
	}
	v2_assets = {
		str(entry["id"]): entry for entry in v2.get("assets", [])
	}
	cards = _item_cards(room_record)
	room_v2 = v2.get("rooms", {}).get(room_id, {})
	for instance in room_v2.get("instances", []):
		item_id = str(instance["id"])
		if item_id in overridden_instances:
			continue
		entry = v2_assets[str(instance["asset_id"])]
		card_id = "item_" + item_id
		if card_id not in cards:
			raise ValueError(f"missing source card for {room_id}:{item_id}")
		crop = [int(value) for value in cards[card_id]["crop"]]
		position = V2_POSITION_OVERRIDES.get(
			(room_id, item_id), (float(crop[0]), float(crop[1])))
		mask, record = _frame_union(entry, position)
		record.update({"instance": item_id, "pack": "v2_base"})
		legacy_union = ImageChops.lighter(legacy_union, mask)
		final_union = ImageChops.lighter(final_union, mask)
		visual_records.append(record)

	for entry in active_v4:
		ownership = entry.get("source_ownership", {})
		source_rect = [int(value) for value in ownership.get("source_rect", [])]
		if len(source_rect) != 4:
			raise ValueError(f"missing V4 source rect: {entry.get('id')}")
		ownership_path = ROOT / str(entry.get("mask_path", ""))
		ownership_image = Image.open(ownership_path).convert("RGBA").getchannel("A")
		if ownership_image.size != (source_rect[2], source_rect[3]):
			raise ValueError(f"V4 ownership size drifted: {entry.get('id')}")
		ownership_image = ownership_image.point(
			lambda value: 255 if value >= 48 else 0)
		ownership_full = Image.new("L", LOGICAL_SIZE, 0)
		ownership_full.paste(ownership_image, source_rect[:2])
		# V4 delivery heals the complete accepted source footprint so no baked
		# edge/contact fragment can remain behind a narrower authored state.
		final_union = ImageChops.lighter(final_union, ownership_full)
		for instance in entry.get("instances", []):
			mask, record = _frame_union(
				entry, (source_rect[0], source_rect[1]))
			record.update({"instance": str(instance), "pack": "v4_native"})
			final_union = ImageChops.lighter(final_union, mask)
			visual_records.append(record)

	legacy_union = _binary_mask(legacy_union)
	final_union = _binary_mask(final_union)
	return legacy_union, final_union, {
		"static_cards": static_records,
		"active_visuals": visual_records,
		"v4_overridden_instances": sorted(overridden_instances),
	}


def _bubble_bath_toilet_repair_mask(room_record: dict[str, Any],
		v2: dict[str, Any]) -> tuple[Image.Image, dict[str, Any]]:
	"""Cover both the source toilet and every normalized authored state.

	The original scanline clean plate left a pale toilet-shaped block and pieces
	of the source outer ring/base behind the animated fixture.  A background can
	serve every seat/lid state only when the complete source ownership and complete
	authored-frame union are filled coherently.
	"""
	card = next(
		entry for entry in room_record.get("cards", [])
		if str(entry.get("id", "")) == "item_toilet")
	crop = [int(value) for value in card["crop"]]
	card_path = ROOM_ROOT / "room_bubble_bath_item_toilet.png"
	card_image = Image.open(card_path).convert("RGBA")
	if card_image.size != (crop[2] - crop[0], crop[3] - crop[1]):
		raise ValueError("bubble-bath toilet source-card size drifted")
	source_alpha = card_image.getchannel("A").point(
		lambda value: 255 if value > 0 else 0)
	source_mask = Image.new("L", LOGICAL_SIZE, 0)
	source_mask.paste(source_alpha, crop[:2])
	asset = next(
		entry for entry in v2.get("assets", [])
		if str(entry.get("id", "")) == "bubble_bath_toilet")
	frame_mask, frame_record = _frame_union(
		asset, (float(crop[0]), float(crop[1])))
	combined = ImageChops.lighter(source_mask, frame_mask).filter(
		ImageFilter.MaxFilter(9)).point(lambda value: 255 if value > 0 else 0)
	return combined, {
		"room": "bubble_bath",
		"instance": "toilet",
		"source_card": _relative(card_path),
		"source_card_sha256": _sha256(card_path),
		"source_crop": crop,
		"source_alpha_threshold": 1,
		"authored_frame_union": frame_record,
		"dilation_radius_logical_pixels": 4,
		"repair_mask": _mask_metrics(combined),
	}


def _harmonic_context_fill(image: Image.Image, mask: Image.Image,
		iterations: int = 120) -> Image.Image:
	"""Fill a local ownership mask from surrounding approved scene context."""
	values = np.asarray(image.convert("RGB"), dtype=np.float32)
	unknown = np.asarray(mask.convert("L"), dtype=np.uint8) > 0
	if not np.any(unknown):
		return image.convert("RGB")
	if np.all(unknown):
		raise ValueError("context-fill mask covers the complete room")
	_, nearest = distance_transform_edt(
		unknown, return_distances=True, return_indices=True)
	filled = values[nearest[0], nearest[1]].copy()
	for _iteration in range(iterations):
		padded = np.pad(filled, ((1, 1), (1, 1), (0, 0)), mode="edge")
		average = (
			padded[:-2, 1:-1] + padded[2:, 1:-1]
			+ padded[1:-1, :-2] + padded[1:-1, 2:]) * 0.25
		filled[unknown] = average[unknown]
	output = values.copy()
	output[unknown] = filled[unknown]
	return Image.fromarray(
		np.clip(output, 0, 255).astype(np.uint8), mode="RGB")


def _pixel_difference_metrics(candidate: Image.Image, approved: Image.Image,
		live_mask: Image.Image) -> dict[str, int]:
	candidate_values = np.asarray(candidate.convert("RGB"), dtype=np.int16)
	approved_values = np.asarray(approved.convert("RGB"), dtype=np.int16)
	maximum_delta = np.max(np.abs(candidate_values - approved_values), axis=2)
	owned = np.asarray(live_mask, dtype=np.uint8) > 0
	changed = maximum_delta > 0
	visible_delta = maximum_delta > 20
	return {
		"changed_pixels": int(np.count_nonzero(changed)),
		"changed_outside_live_union_pixels": int(np.count_nonzero(
			changed & ~owned)),
		"changed_outside_live_union_pixels_gt20": int(np.count_nonzero(
			visible_delta & ~owned)),
		"maximum_delta_outside_live_union": int(
			maximum_delta[~owned].max()) if np.any(~owned) else 0,
	}


def _runtime_v4_master(room_id: str, route: dict[str, Any]
		) -> tuple[Image.Image, list[dict[str, Any]]]:
	canvas_size = tuple(int(value) for value in route["native_canvas_size"])
	grid = [int(value) for value in route["grid"]]
	tile_size = tuple(int(value) for value in route["tile_dimensions"])
	columns, rows = grid
	tiles = route.get("tiles", [])
	if len(tiles) != columns * rows:
		raise ValueError(f"invalid V4 runtime tile count for {room_id}")
	master = Image.new("RGB", canvas_size)
	records: list[dict[str, Any]] = []
	for index, tile in enumerate(tiles):
		row = index // columns
		column = index % columns
		path = ROOT / str(tile["path"])
		image = Image.open(path).convert("RGB")
		if image.size != tile_size:
			raise ValueError(f"V4 tile-size mismatch: {path}")
		master.paste(image, (column * tile_size[0], row * tile_size[1]))
		records.append({
			"row": row,
			"column": column,
			"path": _relative(path),
			"sha256": _sha256(path),
		})
	return master, records


def _route_source_hashes_match(route: dict[str, Any]) -> bool:
	for record in route.get("source_tiles", []):
		path = ROOT / str(record.get("path", ""))
		if not path.exists() or _sha256(path) != str(record.get("sha256", "")):
			return False
	return True


def build_expected_baselines() -> dict[str, dict[str, Any]]:
	"""Return deterministic in-memory native masters and audit records."""
	fable = _load_json(FABLE_MANIFEST)
	v2 = _load_json(V2_MANIFEST)
	v4 = _load_json(V4_MANIFEST) if V4_MANIFEST.exists() else {
		"assets": [], "runtime_background_tiles": {}}
	results: dict[str, dict[str, Any]] = {}
	for room_id in ROOM_IDS:
		room_record = fable["rooms"][room_id]
		source_path = ROOM_ROOT / f"room_{room_id}.png"
		clean_path = ROOM_ROOT / f"room_{room_id}_background.png"
		approved_logical = Image.open(source_path).convert("RGB")
		clean_logical = Image.open(clean_path).convert("RGB")
		if approved_logical.size != LOGICAL_SIZE \
				or clean_logical.size != LOGICAL_SIZE:
			raise ValueError(f"logical room size changed: {room_id}")
		if str(room_record.get("source_sha256", "")) != _sha256(source_path) \
				or str(room_record.get("background_sha256", "")) != _sha256(
					clean_path):
			raise ValueError(f"FABLE source hash mismatch: {room_id}")

		master_size = tuple(int(value) for value in room_record["master_dimensions"])
		approved_native = approved_logical.resize(
			master_size, Image.Resampling.LANCZOS)
		unrepaired_native = clean_logical.resize(
			master_size, Image.Resampling.LANCZOS)
		legacy_union, final_union, ownership = _live_unions(
			room_id, room_record, v2, v4)
		targeted_repairs: list[dict[str, Any]] = []
		toilet_repair_mask: Image.Image | None = None
		if room_id == "bubble_bath":
			toilet_repair_mask, toilet_record = \
				_bubble_bath_toilet_repair_mask(room_record, v2)
			legacy_union = ImageChops.lighter(
				legacy_union, toilet_repair_mask)
			final_union = ImageChops.lighter(final_union, toilet_repair_mask)
			toilet_record.update({
				"method": "nearest_context_initialized_harmonic_fill",
				"jacobi_iterations": 120,
				"approved_source_pixels_only": True,
				"protected_originals_modified": False,
			})
			targeted_repairs.append(toilet_record)
		legacy_native = legacy_union.resize(
			master_size, Image.Resampling.NEAREST)
		final_native = final_union.resize(
			master_size, Image.Resampling.NEAREST)
		repaired = approved_native.copy()
		repaired.paste(unrepaired_native, (0, 0), legacy_native)
		if toilet_repair_mask is not None:
			toilet_context = _harmonic_context_fill(
				approved_logical, toilet_repair_mask, iterations=120)
			toilet_context_native = toilet_context.resize(
				master_size, Image.Resampling.LANCZOS)
			toilet_native_mask = toilet_repair_mask.resize(
				master_size, Image.Resampling.NEAREST)
			repaired.paste(
				toilet_context_native, (0, 0), toilet_native_mask)

		master_path = ROOT / str(room_record["master"])
		master_bytes = _png_bytes(repaired)
		tile_outputs: list[dict[str, Any]] = []
		for tile in room_record.get("runtime_tiles", []):
			rect = tuple(int(value) for value in tile["master_rectangle"])
			path = ROOT / str(tile["path"])
			image = repaired.crop(rect)
			data = _png_bytes(image)
			tile_outputs.append({
				"path": path,
				"relative_path": _relative(path),
				"image": image,
				"bytes": data,
				"sha256": _sha256_bytes(data),
				"master_rectangle": list(rect),
			})

		routes = v4.get("runtime_background_tiles", {})
		route = routes.get(room_id)
		if route is None:
			runtime_master = repaired
			runtime_tiles = tile_outputs
			route_name = "canonical_live_alpha_baseline"
			source_hashes_match = True
		else:
			runtime_master, runtime_tiles = _runtime_v4_master(room_id, route)
			route_name = str(route.get("route", ""))
			source_hashes_match = _route_source_hashes_match(route)
		if runtime_master.size != master_size:
			raise ValueError(f"runtime master size mismatch: {room_id}")

		record = {
			"room_id": room_id,
			"approved_source": {
				"path": _relative(source_path),
				"sha256": _sha256(source_path),
				"dimensions": list(approved_logical.size),
			},
			"existing_hidden_fill": {
				"path": _relative(clean_path),
				"sha256": _sha256(clean_path),
				"dimensions": list(clean_logical.size),
			},
			"master": {
				"path": _relative(master_path),
				"dimensions": list(master_size),
				"sha256": _sha256_bytes(master_bytes),
			},
			"legacy_live_union": _mask_metrics(legacy_union),
			"final_live_union": _mask_metrics(final_union),
			"ownership": ownership,
			"targeted_background_repairs": targeted_repairs,
			"unrepaired_metrics": _pixel_difference_metrics(
				unrepaired_native, approved_native, legacy_native),
			"repaired_baseline_metrics": _pixel_difference_metrics(
				repaired, approved_native, legacy_native),
			"runtime": {
				"route": route_name,
				"source_tile_hashes_match_baseline": source_hashes_match,
				"metrics": _pixel_difference_metrics(
					runtime_master, approved_native, final_native),
				"tiles": [{
					"path": str(tile["relative_path"])
						if "relative_path" in tile else str(tile["path"]),
					"sha256": str(tile["sha256"]),
				} for tile in runtime_tiles],
			},
			"baseline_tiles": [{
				"path": tile["relative_path"],
				"sha256": tile["sha256"],
				"master_rectangle": tile["master_rectangle"],
			} for tile in tile_outputs],
	}
		results[room_id] = {
			"approved": approved_native,
			"unrepaired": unrepaired_native,
			"legacy_mask": legacy_native,
			"final_mask": final_native,
			"master": repaired,
			"master_path": master_path,
			"master_bytes": master_bytes,
			"tiles": tile_outputs,
			"record": record,
		}
	return results


def expected_baseline_master(room_id: str) -> Image.Image:
	"""Reusable hook for the all-room 2K/tile builder."""
	if room_id not in ROOM_IDS:
		raise KeyError(room_id)
	return build_expected_baselines()[room_id]["master"].copy()


def _provenance(results: dict[str, dict[str, Any]],
		contact_sha256: str) -> dict[str, Any]:
	return {
		"schema": 1,
		"purpose": (
			"Restore approved room pixels outside exact live Sprite3D alpha "
			"ownership; retain prior hidden fill only beneath rendered objects"),
		"tool": TOOL_PATH,
		"protected_originals_modified": False,
		"logical_canvas_size": list(LOGICAL_SIZE),
		"live_alpha_threshold": LIVE_ALPHA_THRESHOLD,
		"runtime_contract": (
			"SpriteBase3D.ALPHA_CUT_DISCARD / alpha_scissor_threshold 0.5"),
		"approved_native_transform": (
			"whole-canvas Pillow Image.Resampling.LANCZOS; no crop or padding"),
		"ownership_scale_transform": (
			"logical binary live-alpha union to native canvas with NEAREST"),
		"room_count": len(results),
		"rooms": [results[room_id]["record"] for room_id in ROOM_IDS],
		"contact_sheet": {
			"path": _relative(CONTACT_PATH),
			"sha256": contact_sha256,
			"review_output_ignored": True,
		},
	}


def _contact_bytes(results: dict[str, dict[str, Any]]) -> bytes:
	panel_size = (384, 216)
	label_height = 38
	columns = 3
	canvas = Image.new(
		"RGB",
		(panel_size[0] * columns,
			(panel_size[1] + label_height) * len(ROOM_IDS)),
		"#332c68")
	draw = ImageDraw.Draw(canvas)
	labels = (
		("approved", "APPROVED FULL ROOM"),
		("unrepaired", "OLD CLEAN FILL (AUDIT)"),
		("master", "LIVE-ALPHA BASELINE"),
	)
	for row, room_id in enumerate(ROOM_IDS):
		for column, (key, label) in enumerate(labels):
			x = column * panel_size[0]
			y = row * (panel_size[1] + label_height)
			preview = results[room_id][key].resize(
				panel_size, Image.Resampling.LANCZOS)
			canvas.paste(preview, (x, y))
			draw.rectangle(
				(x, y + panel_size[1], x + panel_size[0],
					y + panel_size[1] + label_height),
				fill="#332c68")
			draw.text(
				(x + 8, y + panel_size[1] + 5),
				f"{room_id.replace('_', ' ').upper()} — {label}",
				font=_font(14, bold=True), fill="#ffffff")
	return _png_bytes(canvas)


def _update_fable(results: dict[str, dict[str, Any]]) -> None:
	manifest = _load_json(FABLE_MANIFEST)
	for room_id, result in results.items():
		room = manifest["rooms"][room_id]
		record = result["record"]
		room["master_sha256"] = record["master"]["sha256"]
		output_tiles = {
			tile["relative_path"]: tile for tile in result["tiles"]
		}
		for tile in room.get("runtime_tiles", []):
			path = str(tile["path"])
			if path not in output_tiles:
				raise ValueError(f"unexpected FABLE tile: {path}")
			tile["sha256"] = output_tiles[path]["sha256"]
		room["upscale_method"] = (
			"approved full-room whole-canvas Lanczos to native size; prior "
			"hidden fill retained only inside exact live-alpha ownership")
		room["native_live_alpha_baseline"] = {
			"provenance": _relative(PROVENANCE_PATH),
			"live_alpha_threshold": LIVE_ALPHA_THRESHOLD,
			"legacy_live_union_pixel_sha256": (
				record["legacy_live_union"]["raw_pixel_sha256"]),
			"approved_pixels_restored_outside_live_union": True,
			"changed_outside_live_union_pixels": (
				record["repaired_baseline_metrics"]
				["changed_outside_live_union_pixels"]),
		}
	# Preserve the established manifest's human-reviewed key order; only the
	# seven room records above are semantically updated.
	data = (json.dumps(manifest, indent=2) + "\n").encode()
	_atomic_write(FABLE_MANIFEST, data)


def _write_outputs(results: dict[str, dict[str, Any]]) -> None:
	for result in results.values():
		_atomic_write(result["master_path"], result["master_bytes"])
		for tile in result["tiles"]:
			_atomic_write(tile["path"], tile["bytes"])
	_update_fable(results)
	contact_data = _contact_bytes(results)
	_atomic_write(CONTACT_PATH, contact_data)
	provenance = _provenance(results, _sha256_bytes(contact_data))
	_atomic_write(
		PROVENANCE_PATH,
		(json.dumps(provenance, indent=2, sort_keys=True) + "\n").encode(),
	)


def _check_outputs(results: dict[str, dict[str, Any]]) -> list[str]:
	problems: list[str] = []
	for room_id, result in results.items():
		master_path: Path = result["master_path"]
		if not master_path.exists() or master_path.read_bytes() != result[
				"master_bytes"]:
			problems.append(f"{room_id}: native master is stale")
		for tile in result["tiles"]:
			if not tile["path"].exists() or tile["path"].read_bytes() != tile[
					"bytes"]:
				problems.append(f"{room_id}: baseline tile is stale: {tile['path']}")
		repaired_metrics = result["record"]["repaired_baseline_metrics"]
		if repaired_metrics["changed_outside_live_union_pixels"] != 0:
			problems.append(f"{room_id}: baseline changed outside live union")
		runtime = result["record"]["runtime"]
		if not runtime["source_tile_hashes_match_baseline"]:
			problems.append(f"{room_id}: V4 route was not rebuilt from baseline")
		if runtime["metrics"]["changed_outside_live_union_pixels"] != 0:
			problems.append(
				f"{room_id}: runtime changed outside combined live union")

	contact_data = _contact_bytes(results)
	# Review captures live under the intentionally ignored audit tree.  Validate
	# them when present locally, but do not make a fresh CI clone require an
	# untracked review artifact.
	if CONTACT_PATH.exists() and CONTACT_PATH.read_bytes() != contact_data:
		problems.append("contact sheet is stale")
	expected_provenance = _provenance(results, _sha256_bytes(contact_data))
	if not PROVENANCE_PATH.exists():
		problems.append("provenance is missing")
	else:
		actual_provenance = _load_json(PROVENANCE_PATH)
		if actual_provenance != expected_provenance:
			problems.append("provenance is stale")

	fable = _load_json(FABLE_MANIFEST)
	for room_id, result in results.items():
		room = fable["rooms"][room_id]
		if room.get("master_sha256") != result["record"]["master"]["sha256"]:
			problems.append(f"{room_id}: FABLE master hash is stale")
		expected_tiles = {
			tile["relative_path"]: tile["sha256"] for tile in result["tiles"]
		}
		for tile in room.get("runtime_tiles", []):
			if tile.get("sha256") != expected_tiles.get(str(tile.get("path"))):
				problems.append(f"{room_id}: FABLE tile hash is stale")
				break
	return problems


def _print_metrics(results: dict[str, dict[str, Any]]) -> None:
	for room_id in ROOM_IDS:
		record = results[room_id]["record"]
		before = record["unrepaired_metrics"]
		after = record["runtime"]["metrics"]
		print(
			"CASTLE_LIVE_ALPHA|ROOM|%s|before_outside=%d|"
			"before_outside_gt20=%d|runtime_outside=%d|"
			"runtime_outside_gt20=%d|route=%s" % (
				room_id,
				before["changed_outside_live_union_pixels"],
				before["changed_outside_live_union_pixels_gt20"],
				after["changed_outside_live_union_pixels"],
				after["changed_outside_live_union_pixels_gt20"],
				record["runtime"]["route"],
			))


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--check", action="store_true",
		help="validate native baselines, active runtime tiles, provenance, and QA")
	args = parser.parse_args()
	try:
		results = build_expected_baselines()
		_print_metrics(results)
		if args.check:
			problems = _check_outputs(results)
			if problems:
				for problem in problems:
					print(f"CASTLE_LIVE_ALPHA|FAIL|{problem}", file=sys.stderr)
				print(
					f"CASTLE_LIVE_ALPHA|RESULT|FAIL|count={len(problems)}",
					file=sys.stderr)
				return 1
			print(
				f"CASTLE_LIVE_ALPHA|RESULT|OK|rooms={len(ROOM_IDS)}|"
				"outside_live_union=0")
			return 0
		_write_outputs(results)
		print(
			f"CASTLE_LIVE_ALPHA|BUILT|rooms={len(ROOM_IDS)}|"
			"protected_originals_modified=false")
		return 0
	except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
		print(f"CASTLE_LIVE_ALPHA|ERROR|{error}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
