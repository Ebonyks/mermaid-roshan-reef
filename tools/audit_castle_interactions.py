#!/usr/bin/env python3
"""Blocking integrity and alpha-depth audit for Castle interaction atlases.

This audit deliberately treats only alpha >= 128 as depth-writing.  That is
the same binary boundary used by the Castle Sprite3D alpha-cut material, and
keeps semi-transparent antialiasing from being mistaken for an opaque wall
that can hide Roshan.
"""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
	ROOT / "assets" / "flats" / "castle" / "interactions"
	/ "castle_interactions.json"
)
DEPTH_MANIFEST_PATH = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
AUDIO_MANIFEST_PATH = (
	ROOT / "assets" / "audio" / "castle" / "castle_interaction_sfx_manifest.json"
)
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
ROSHAN_PATH = ROOT / "assets" / "characters" / "roshan_25d" / "roshan_directional.png"
AUDIO_ROOT = (ROOT / "assets" / "audio" / "castle").resolve()

DEPTH_ALPHA_THRESHOLD = 128
MAX_TEXTURE_EDGE = 1024
MIN_TRANSPARENT_FRACTION = 0.13
BACKGROUND_COLOR_TOLERANCE = 6
MAX_BACKGROUND_LIKE_FRACTION = 0.31
BACKGROUND_CONDITIONAL_FRACTION = 0.18
MAX_CONDITIONAL_REST_COVERAGE = 0.36
MAX_CONDITIONAL_BACKGROUND_PIXELS = 1600
MIN_SOURCE_SILHOUETTE_RETENTION = 0.95
MIN_CHASSIS_ALPHA_IOU = 0.12
MIN_CHANGED_CELL_FRACTION = 0.005
MAX_CHANGED_CELL_FRACTION = 0.80
MIN_CHANGED_PIXELS = 24
MIN_ROSHAN_VISIBLE_FRACTION = 0.15
MAX_AUDIO_SYNC_ERROR_SECONDS = 0.002
TIMELINE_SYNC = "sound_starts_with_frame_0_and_ends_with_frame_7"

EXPECTED_ROOM_COUNTS = {
	"bubble_bath": 4,
	"craft_room": 4,
	"kitchen": 7,
	"library": 4,
	"main_hall": 7,
	"mermaid_pool": 4,
	"opera_hall": 4,
	"playroom": 4,
}

# asset id: (room, item id, semantic action, sound basename, instance ids)
EXPECTED_ASSETS: dict[str, tuple[str, str, str, str, tuple[str, ...]]] = {
	"main_hall_tapestry": (
		"main_hall", "tapestry", "unfurl_cloth", "curtain_swish.ogg",
		("tapestry_right",),
	),
	"main_hall_sconce": (
		"main_hall", "sconce", "toggle_shell_light", "light_switch.ogg",
		("sconce_a0", "sconce_a1", "sconce_a2", "sconce_b0", "sconce_b1", "sconce_b2"),
	),
	"opera_hall_curtains": (
		"opera_hall", "curtains", "open_stage_curtains", "curtain_swish.ogg",
		("curtains",),
	),
	"opera_hall_chandelier": (
		"opera_hall", "chandelier", "chandelier_light_chase", "light_switch.ogg",
		("chandelier",),
	),
	"opera_hall_footlights": (
		"opera_hall", "footlights", "stage_footlight_chase", "light_switch.ogg",
		("footlights",),
	),
	"opera_hall_stage_star": (
		"opera_hall", "stage_star", "marquee_star_light_chase", "light_switch.ogg",
		("stage_star",),
	),
	"kitchen_sink": (
		"kitchen", "sink", "turn_faucet_and_run_water", "faucet_water.ogg",
		("sink",),
	),
	"kitchen_pan_1": (
		"kitchen", "pan_1", "swing_pan_on_hook", "pan_clang.ogg", ("pan_1",),
	),
	"kitchen_pan_2": (
		"kitchen", "pan_2", "swing_pan_on_hook", "pan_clang.ogg", ("pan_2",),
	),
	"kitchen_pan_3": (
		"kitchen", "pan_3", "swing_pan_on_hook", "pan_clang.ogg", ("pan_3",),
	),
	"kitchen_pan_4": (
		"kitchen", "pan_4", "swing_pan_on_hook", "pan_clang.ogg", ("pan_4",),
	),
	"kitchen_oven": (
		"kitchen", "oven", "open_oven_door_and_warm_fire", "oven_door.ogg",
		("oven",),
	),
	"kitchen_fridge": (
		"kitchen", "fridge", "unlatch_and_open_fridge_door", "fridge_door.ogg",
		("fridge",),
	),
	"library_book_stack": (
		"library", "book_stack", "open_top_book_and_turn_pages", "page_flip.ogg",
		("book_stack",),
	),
	"library_magic_book": (
		"library", "magic_book", "open_book_and_turn_pages", "page_flip.ogg",
		("magic_book",),
	),
	"library_pearl_table": (
		"library", "pearl_table", "wake_reading_pearl", "light_switch.ogg",
		("pearl_table",),
	),
	"library_pearl_lamp": (
		"library", "pearl_lamp", "toggle_pearl_lamp", "light_switch.ogg",
		("pearl_lamp",),
	),
	"playroom_play_tent": (
		"playroom", "play_tent", "open_and_close_tent_flap", "curtain_swish.ogg",
		("play_tent",),
	),
	"playroom_stuffie_nook": (
		"playroom", "stuffie_nook", "stuffie_friends_wave", "toy_blocks.ogg",
		("stuffie_nook",),
	),
	"playroom_stacking_toy": (
		"playroom", "stacking_toy", "lift_and_restack_rings", "toy_blocks.ogg",
		("stacking_toy",),
	),
	"playroom_blocks": (
		"playroom", "blocks", "topple_and_restack_blocks", "toy_blocks.ogg",
		("blocks",),
	),
	"craft_room_ribbon_rack": (
		"craft_room", "ribbon_rack", "unroll_and_retract_ribbon", "ribbon_roll.ogg",
		("ribbon_rack",),
	),
	"craft_room_idea_board": (
		"craft_room", "idea_board", "flip_idea_notes", "page_flip.ogg",
		("idea_board",),
	),
	"craft_room_paint_table": (
		"craft_room", "paint_table", "stir_paint_with_brush", "craft_brush.ogg",
		("paint_table",),
	),
	"craft_room_palette": (
		"craft_room", "palette", "mix_palette_colors", "craft_brush.ogg",
		("palette",),
	),
	"mermaid_pool_star_float": (
		"mermaid_pool", "star_float", "float_and_make_ripples", "bubble_water.ogg",
		("star_float",),
	),
	"mermaid_pool_waterfall": (
		"mermaid_pool", "waterfall", "surge_waterfall_flow", "bubble_water.ogg",
		("waterfall",),
	),
	"mermaid_pool_flower_float": (
		"mermaid_pool", "flower_float", "open_flower_and_make_ripples", "bubble_water.ogg",
		("flower_float",),
	),
	"mermaid_pool_seahorse_fountain": (
		"mermaid_pool", "seahorse_fountain", "spray_seahorse_fountain", "bubble_water.ogg",
		("seahorse_fountain",),
	),
	"bubble_bath_rubber_duck": (
		"bubble_bath", "rubber_duck", "squeak_dive_and_pop_up", "duck_squeak.ogg",
		("rubber_duck",),
	),
	"bubble_bath_bathtub": (
		"bubble_bath", "bathtub", "turn_taps_and_fill_bubbles", "bubble_water.ogg",
		("bathtub",),
	),
	"bubble_bath_sink": (
		"bubble_bath", "sink", "turn_faucet_and_run_water", "faucet_water.ogg",
		("sink",),
	),
	"bubble_bath_toilet": (
		"bubble_bath", "toilet", "flap_seat_and_flush", "toilet_flush.ogg",
		("toilet",),
	),
}

REPEATED_ACTION_ALLOWLIST = {
	"turn_faucet_and_run_water": {"kitchen_sink", "bubble_bath_sink"},
	"swing_pan_on_hook": {
		"kitchen_pan_1", "kitchen_pan_2", "kitchen_pan_3", "kitchen_pan_4",
	},
}


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _text_sha256(path: Path) -> str:
	"""Hash repository text consistently across LF/CRLF working trees."""
	data = path.read_bytes().replace(b"\r\n", b"\n")
	return hashlib.sha256(data).hexdigest()


def _check(condition: bool, message: str, failures: list[str]) -> None:
	if not condition:
		failures.append(message)


def _repo_path(value: object, label: str, failures: list[str]) -> Path | None:
	if not isinstance(value, str) or not value:
		failures.append(f"{label} must be a non-empty repository-relative path")
		return None
	path = Path(value)
	if path.is_absolute():
		failures.append(f"{label} must not be absolute: {value}")
		return None
	resolved = (ROOT / path).resolve()
	try:
		resolved.relative_to(ROOT.resolve())
	except ValueError:
		failures.append(f"{label} escapes the repository: {value}")
		return None
	return resolved


def _depth_crops(depth_manifest: dict[str, Any]) -> dict[tuple[str, str], tuple[int, int, int, int]]:
	crops: dict[tuple[str, str], tuple[int, int, int, int]] = {}
	for room_id, room in depth_manifest.get("rooms", {}).items():
		for card in room.get("cards", []):
			if card.get("role") != "item":
				continue
			item_id = str(card.get("id", "")).removeprefix("item_")
			crop = card.get("crop", [])
			if len(crop) == 4:
				crops[(str(room_id), item_id)] = tuple(int(value) for value in crop)
	return crops


def _audit_current_runtime_contract(
	depth_manifest: dict[str, Any], failures: list[str],
) -> None:
	current_name = "runtime_correction_2026_08_22"
	revision = depth_manifest.get(current_name)
	if not isinstance(revision, dict):
		failures.append(f"Depth manifest must declare {current_name}")
		return
	_check(revision.get("status") == "accepted_current_runtime",
		"Current Castle correction must be marked accepted_current_runtime", failures)
	_check(revision.get("fixture_physics") == "analytic_2d",
		"Current Castle fixture physics must be analytic_2d", failures)
	required_predecessors = {
		"runtime_correction_2026_07_29",
		"runtime_correction_2026_08_01",
		"runtime_correction_2026_08_04",
	}
	superseded = revision.get("supersedes_runtime_corrections")
	_check(isinstance(superseded, list) and set(superseded) == required_predecessors,
		"Current Castle correction must supersede every historical runtime contract",
		failures)
	for predecessor_name in sorted(required_predecessors):
		predecessor = depth_manifest.get(predecessor_name)
		if not isinstance(predecessor, dict):
			failures.append(f"Depth manifest must preserve {predecessor_name}")
			continue
		_check(predecessor.get("status") == "historical_superseded",
			f"{predecessor_name} must be marked historical_superseded", failures)
		_check(predecessor.get("superseded_by") == current_name,
			f"{predecessor_name} must point to {current_name}", failures)
	contract = revision.get("runtime_node_contract")
	if not isinstance(contract, dict):
		failures.append("Current Castle runtime_node_contract must be an object")
		return
	root_contract = depth_manifest.get("runtime_node_contract")
	if not isinstance(root_contract, dict):
		failures.append("Root Castle runtime_node_contract must be an object")
		return
	required_contract_keys = {
		"camera", "coordinate_system", "world_art_allowed",
		"world_art_forbidden", "world_root",
	}
	_check(set(contract) == required_contract_keys,
		"Current Castle correction must declare exactly the core 2D runtime keys",
		failures)
	_check(all(root_contract.get(key) == value for key, value in contract.items()),
		"Current Castle correction must be an exact subset of the root runtime contract",
		failures)
	_check(contract.get("world_root") == "Node2D",
		"Current Castle world root must be Node2D", failures)
	_check(contract.get("camera") == "none",
		"Current Castle contract must not use a 3D camera", failures)
	_check(contract.get("coordinate_system") == "direct_canvas_coordinates",
		"Current Castle coordinates must be direct canvas coordinates", failures)
	_check(contract.get("world_art_allowed") == ["Sprite2D:unshaded"],
		"Current Castle world art must be unshaded Sprite2D", failures)
	for forbidden_type in (
		"Node3D", "Sprite3D", "Camera3D", "MeshInstance3D",
		"MultiMeshInstance3D", "CSGShape3D", "Decal",
	):
		_check(forbidden_type in contract.get("world_art_forbidden", []),
			f"Current Castle contract must forbid {forbidden_type}", failures)


def _audio_durations(
	audio_manifest: dict[str, Any], failures: list[str],
) -> dict[str, float]:
	_check(audio_manifest.get("schema") == "reef.castle-interaction-sfx.v1",
		"Castle SFX manifest schema must be reef.castle-interaction-sfx.v1", failures)
	generator_path = _repo_path(
		audio_manifest.get("generator"), "Castle SFX generator", failures)
	if generator_path is None or not generator_path.is_file():
		failures.append("Castle SFX generator file is missing")
	else:
		_check(audio_manifest.get("generator_sha256")
			== _text_sha256(generator_path),
			"Castle SFX generator_sha256 does not match generator bytes", failures)
	files = audio_manifest.get("files")
	if not isinstance(files, list):
		failures.append("Castle SFX manifest files must be a list")
		return {}
	durations: dict[str, float] = {}
	for index, entry in enumerate(files):
		if not isinstance(entry, dict):
			failures.append(f"Castle SFX manifest entry {index} must be an object")
			continue
		path = entry.get("path")
		duration_ms = entry.get("duration_ms")
		if not isinstance(path, str) or not path:
			failures.append(f"Castle SFX manifest entry {index} has no path")
			continue
		if path in durations:
			failures.append(f"Castle SFX manifest repeats path {path}")
			continue
		if not isinstance(duration_ms, int) or isinstance(duration_ms, bool) \
			or duration_ms <= 0:
			failures.append(f"Castle SFX manifest {path} has invalid duration_ms")
			continue
		sound_path = _repo_path(path, f"Castle SFX manifest {path}", failures)
		if sound_path is None:
			continue
		try:
			sound_path.relative_to(AUDIO_ROOT)
		except ValueError:
			failures.append(f"Castle SFX manifest {path} must stay under assets/audio/castle")
			continue
		if not sound_path.is_file():
			failures.append(f"Castle SFX manifest {path} file is missing")
			continue
		_check(entry.get("file_bytes") == sound_path.stat().st_size,
			f"Castle SFX manifest {path} file_bytes does not match file size", failures)
		_check(entry.get("sha256") == _sha256(sound_path),
			f"Castle SFX manifest {path} sha256 does not match file bytes", failures)
		_check(sound_path.read_bytes()[:4] == b"OggS",
			f"Castle SFX manifest {path} is not an Ogg stream", failures)
		durations[path] = duration_ms / 1000.0
	return durations


def _roshan_mask() -> np.ndarray:
	image = Image.open(ROSHAN_PATH).convert("RGBA")
	if image.width < 256 or image.height < 256:
		raise ValueError(f"unexpected Roshan directional sheet size {image.size}")
	frame = image.crop((0, 0, 256, 256))
	bbox = frame.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("Roshan reference frame is fully transparent")
	return np.asarray(frame.crop(bbox).getchannel("A"), dtype=np.uint8)


def _best_roshan_visibility(prop_depth: np.ndarray, roshan_alpha: np.ndarray) -> float:
	"""Return the best visible fraction at three deterministic floor positions."""
	height, width = prop_depth.shape
	scale = 0.55 * height / roshan_alpha.shape[0]
	char_width = max(1, round(roshan_alpha.shape[1] * scale))
	char_height = max(1, round(roshan_alpha.shape[0] * scale))
	resized = Image.fromarray(roshan_alpha, mode="L").resize(
		(char_width, char_height), Image.Resampling.LANCZOS)
	character = np.asarray(resized, dtype=np.uint8) >= DEPTH_ALPHA_THRESHOLD
	visible_fractions: list[float] = []
	for normalized_x in (0.20, 0.50, 0.80):
		x_pos = round(normalized_x * width - char_width / 2)
		y_pos = height - char_height - 1
		x0 = max(0, x_pos)
		y0 = max(0, y_pos)
		x1 = min(width, x_pos + char_width)
		y1 = min(height, y_pos + char_height)
		if x0 >= x1 or y0 >= y1:
			visible_fractions.append(0.0)
			continue
		character_crop = character[
			y0 - y_pos:y1 - y_pos, x0 - x_pos:x1 - x_pos]
		character_pixels = int(np.count_nonzero(character_crop))
		if character_pixels == 0:
			visible_fractions.append(0.0)
			continue
		occluded = prop_depth[y0:y1, x0:x1]
		visible = int(np.count_nonzero(character_crop & ~occluded))
		visible_fractions.append(visible / character_pixels)
	return max(visible_fractions, default=0.0)


def _frame_cells(
	atlas: np.ndarray,
	cell_width: int,
	cell_height: int,
	hframes: int,
	frame_count: int,
) -> list[np.ndarray]:
	frames: list[np.ndarray] = []
	for index in range(frame_count):
		x_pos = (index % hframes) * cell_width
		y_pos = (index // hframes) * cell_height
		frames.append(atlas[y_pos:y_pos + cell_height, x_pos:x_pos + cell_width])
	return frames


def _audit_asset(
	record: dict[str, Any],
	crops: dict[tuple[str, str], tuple[int, int, int, int]],
	audio_durations: dict[str, float],
	roshan_alpha: np.ndarray,
	failures: list[str],
	metrics: dict[str, list[float]],
) -> None:
	asset_id = str(record.get("id", "<missing-id>"))
	prefix = f"{asset_id}:"
	expected = EXPECTED_ASSETS.get(asset_id)
	if expected is not None:
		expected_room, expected_item, expected_action, expected_sound, expected_instances = expected
		_check(record.get("room") == expected_room,
			f"{prefix} room must be {expected_room}", failures)
		_check(record.get("item_id") == expected_item,
			f"{prefix} item_id must be {expected_item}", failures)
		_check(record.get("semantic_action") == expected_action,
			f"{prefix} semantic_action must be {expected_action}", failures)
		_check(record.get("sound") == f"assets/audio/castle/{expected_sound}",
			f"{prefix} sound must be assets/audio/castle/{expected_sound}", failures)
		instances = record.get("instances", [])
		_check(isinstance(instances, list) and set(instances) == set(expected_instances)
			and len(instances) == len(expected_instances),
			f"{prefix} instances do not match the approved physical uses", failures)

	action = record.get("semantic_action")
	_check(isinstance(action, str) and bool(action.strip()),
		f"{prefix} semantic_action is empty", failures)
	_check(record.get("fixed_pivot") is True,
		f"{prefix} fixed_pivot must be true", failures)
	_check(record.get("root_transform_animation") is False,
		f"{prefix} root_transform_animation must be false", failures)
	_check(record.get("normalized_use_review")
		== "accepted_visual_review_2026-08-01",
		f"{prefix} normalized-use visual review is not accepted", failures)
	_check(record.get("transparent_border") is True,
		f"{prefix} transparent_border evidence must be true", failures)

	cell_size = record.get("cell_size")
	hframes = record.get("hframes")
	vframes = record.get("vframes")
	frame_count = record.get("frame_count")
	if not (
		isinstance(cell_size, list) and len(cell_size) == 2
		and all(isinstance(value, int) and not isinstance(value, bool) and value > 0
			for value in cell_size)
		and isinstance(hframes, int) and not isinstance(hframes, bool) and hframes > 0
		and isinstance(vframes, int) and not isinstance(vframes, bool) and vframes > 0
		and isinstance(frame_count, int) and not isinstance(frame_count, bool)
	):
		failures.append(f"{prefix} invalid cell_size/hframes/vframes/frame_count")
		return
	cell_width, cell_height = cell_size
	_check(4 <= frame_count <= 12,
		f"{prefix} frame_count {frame_count} is outside 4..12", failures)
	_check(hframes * vframes >= frame_count,
		f"{prefix} {hframes}x{vframes} grid cannot hold {frame_count} frames", failures)
	_check(max(cell_width, cell_height) <= MAX_TEXTURE_EDGE,
		f"{prefix} cell {cell_width}x{cell_height} exceeds 1024px", failures)
	_check(record.get("reviewed_frame_indices") == list(range(frame_count)),
		f"{prefix} reviewed_frame_indices must cover every frame in order", failures)
	duration = record.get("frame_duration_seconds")
	duration_valid = isinstance(duration, (int, float)) and not isinstance(duration, bool) \
		and 0.04 <= float(duration) <= 0.50
	_check(duration_valid,
		f"{prefix} frame_duration_seconds must be in 0.04..0.50", failures)
	sound_frame = record.get("sound_frame")
	_check(sound_frame == 0 and not isinstance(sound_frame, bool),
		f"{prefix} sound_frame must be exactly 0 for synchronized playback", failures)
	_check(record.get("timeline_sync") == TIMELINE_SYNC,
		f"{prefix} timeline_sync must be {TIMELINE_SYNC!r}", failures)
	if duration_valid:
		animation_duration = float(duration) * frame_count
		declared_animation_duration = record.get("animation_duration_seconds")
		_check(isinstance(declared_animation_duration, (int, float))
			and not isinstance(declared_animation_duration, bool)
			and float(declared_animation_duration) == animation_duration,
			f"{prefix} animation_duration_seconds must exactly equal "
			"frame_duration_seconds * frame_count", failures)
		sound_value = record.get("sound")
		sound_duration = audio_durations.get(str(sound_value))
		if sound_duration is None:
			failures.append(f"{prefix} sound is missing from Castle SFX duration manifest")
		else:
			declared_sound_duration = record.get("sound_duration_seconds")
			_check(isinstance(declared_sound_duration, (int, float))
				and not isinstance(declared_sound_duration, bool)
				and float(declared_sound_duration) == sound_duration,
				f"{prefix} sound_duration_seconds must exactly match duration_ms",
				failures)
			sync_error = abs(animation_duration - sound_duration)
			metrics["audio_sync_error"].append(sync_error)
			_check(sync_error <= MAX_AUDIO_SYNC_ERROR_SECONDS,
				f"{prefix} animation/audio duration error {sync_error:.6f}s exceeds "
				f"{MAX_AUDIO_SYNC_ERROR_SECONDS:.3f}s", failures)

	source_path = _repo_path(record.get("source"), f"{prefix} source", failures)
	atlas_path = _repo_path(record.get("atlas"), f"{prefix} atlas", failures)
	if source_path is None or not source_path.is_file():
		failures.append(f"{prefix} source file is missing")
	else:
		_check(record.get("source_sha256") == _sha256(source_path),
			f"{prefix} source_sha256 does not match source bytes", failures)
		if isinstance(record.get("source"), str) and str(record["source"]).startswith(
			"assets_src/"):
			try:
				source_rgba = np.asarray(Image.open(source_path).convert("RGBA"), dtype=np.uint8)
				source_alpha = source_rgba[:, :, 3]
				source_border = max(
					int(source_alpha[0, :].max()), int(source_alpha[-1, :].max()),
					int(source_alpha[:, 0].max()), int(source_alpha[:, -1].max()),
				)
				source_occupancy = float(np.mean(
					source_alpha >= DEPTH_ALPHA_THRESHOLD))
				_check(source_border == 0,
					f"{prefix} external clean source needs a transparent outer border",
					failures)
				_check(0.005 <= source_occupancy <= 1.0 - MIN_TRANSPARENT_FRACTION,
					f"{prefix} external source occupancy {source_occupancy:.3f} is not sane",
					failures)
			except Exception as exc:
				failures.append(f"{prefix} external clean source cannot be decoded: {exc}")
	if atlas_path is None or not atlas_path.is_file():
		failures.append(f"{prefix} atlas file is missing")
		return
	_check(record.get("atlas_sha256") == _sha256(atlas_path),
		f"{prefix} atlas_sha256 does not match atlas bytes", failures)

	try:
		atlas_image = Image.open(atlas_path).convert("RGBA")
	except Exception as exc:
		failures.append(f"{prefix} atlas cannot be decoded: {exc}")
		return
	expected_size = (cell_width * hframes, cell_height * vframes)
	_check(atlas_image.size == expected_size,
		f"{prefix} atlas is {atlas_image.size}, expected {expected_size}", failures)
	_check(max(atlas_image.size) <= MAX_TEXTURE_EDGE,
		f"{prefix} atlas {atlas_image.size} exceeds 1024px", failures)
	if atlas_image.size != expected_size:
		return
	atlas = np.asarray(atlas_image, dtype=np.uint8)
	frames = _frame_cells(atlas, cell_width, cell_height, hframes, frame_count)

	declared_hashes = record.get("frame_sha256")
	if not isinstance(declared_hashes, list) or len(declared_hashes) != frame_count:
		failures.append(f"{prefix} frame_sha256 must contain exactly {frame_count} hashes")
		declared_hashes = []
	actual_hashes = [hashlib.sha256(frame.tobytes()).hexdigest() for frame in frames]
	if declared_hashes:
		_check(declared_hashes == actual_hashes,
			f"{prefix} one or more full-cell frame hashes do not match", failures)
	unique_count = len(set(actual_hashes))
	_check(unique_count >= 4,
		f"{prefix} has only {unique_count} unique full-cell frames; need at least 4", failures)
	_check(record.get("unique_frame_count") == unique_count,
		f"{prefix} unique_frame_count does not match decoded frames", failures)

	depth_masks: list[np.ndarray] = []
	for index, frame in enumerate(frames):
		alpha = frame[:, :, 3]
		border_alpha = max(
			int(alpha[0, :].max()), int(alpha[-1, :].max()),
			int(alpha[:, 0].max()), int(alpha[:, -1].max()),
		)
		_check(border_alpha == 0,
			f"{prefix} frame {index} does not have a fully transparent outer border", failures)
		depth = alpha >= DEPTH_ALPHA_THRESHOLD
		depth_masks.append(depth)
		depth_pixels = int(np.count_nonzero(depth))
		coverage = depth_pixels / depth.size
		metrics["coverage"].append(coverage)
		_check(depth_pixels > 0, f"{prefix} frame {index} is empty", failures)
		_check(coverage < 0.995,
			f"{prefix} frame {index} is an opaque full-cell rectangle", failures)
		_check(coverage <= 1.0 - MIN_TRANSPARENT_FRACTION,
			f"{prefix} frame {index} leaves only {1.0 - coverage:.3f} transparent area; "
			f"need {MIN_TRANSPARENT_FRACTION:.3f}", failures)
		visible = _best_roshan_visibility(depth, roshan_alpha)
		metrics["roshan_visibility"].append(visible)
		_check(visible >= MIN_ROSHAN_VISIBLE_FRACTION,
			f"{prefix} frame {index} hides too much of Roshan in all sampled placements "
			f"(best visible fraction {visible:.3f})", failures)

	# Any atlas capacity after frame_count must be byte-for-byte blank, not just
	# alpha-zero, so hidden RGB cannot leak through future sampling changes.
	for index in range(frame_count, hframes * vframes):
		x_pos = (index % hframes) * cell_width
		y_pos = (index // hframes) * cell_height
		unused = atlas[y_pos:y_pos + cell_height, x_pos:x_pos + cell_width]
		_check(not bool(np.any(unused)),
			f"{prefix} unused atlas cell {index} is not blank RGBA", failures)

	if frames:
		rest = frames[0]
		rest_depth = depth_masks[0]
		minimum_iou = 1.0
		for index, depth in enumerate(depth_masks[1:], start=1):
			union = int(np.count_nonzero(rest_depth | depth))
			iou = int(np.count_nonzero(rest_depth & depth)) / max(1, union)
			minimum_iou = min(minimum_iou, iou)
			_check(iou >= MIN_CHASSIS_ALPHA_IOU,
				f"{prefix} frame {index} loses fixed-pivot chassis overlap "
				f"(rest IoU {iou:.3f})", failures)
		for index in range(1, len(depth_masks)):
			previous = depth_masks[index - 1]
			current = depth_masks[index]
			union = int(np.count_nonzero(previous | current))
			iou = int(np.count_nonzero(previous & current)) / max(1, union)
			minimum_iou = min(minimum_iou, iou)
			_check(iou >= MIN_CHASSIS_ALPHA_IOU,
				f"{prefix} frame {index - 1}->{index} has discontinuous alpha chassis "
				f"(IoU {iou:.3f})", failures)
		metrics["chassis_iou"].append(minimum_iou)

		changed_counts: list[int] = []
		for frame in frames[1:]:
			delta = np.max(np.abs(
				frame.astype(np.int16) - rest.astype(np.int16)), axis=2)
			changed_counts.append(int(np.count_nonzero(delta > 8)))
		largest_change = max(changed_counts, default=0)
		changed_fraction = largest_change / (cell_width * cell_height)
		metrics["changed_fraction"].append(changed_fraction)
		_check(largest_change >= MIN_CHANGED_PIXELS
			and changed_fraction >= MIN_CHANGED_CELL_FRACTION,
			f"{prefix} action is not materially animated "
			f"({largest_change} changed pixels, {changed_fraction:.4f} of cell)", failures)
		_check(changed_fraction <= MAX_CHANGED_CELL_FRACTION,
			f"{prefix} action changes {changed_fraction:.3f} of the full cell; "
			"motion is not localized", failures)

	# Room-derived rest poses must retain the source silhouette while avoiding
	# pixels that are effectively the healed room plate.  The narrow six-level
	# color comparison is paired with a conditional allowance for compact,
	# low-coverage props whose painted colors legitimately resemble the plate.
	source_value = record.get("source")
	if isinstance(source_value, str) and source_value.startswith(
		"assets/flats/castle/rooms/"):
		room_id = str(record.get("room", ""))
		item_id = str(record.get("item_id", ""))
		crop = crops.get((room_id, item_id))
		if crop is None:
			failures.append(f"{prefix} room-derived source has no depth-manifest item crop")
		else:
			left, top, right, bottom = crop
			_check((right - left, bottom - top) == (cell_width, cell_height),
				f"{prefix} cell size does not match healed-room crop {crop}", failures)
			room_rest_depth = rest_depth
			room_rest_rgb = rest[:, :, :3].astype(np.int16)
			if source_path is not None and source_path.is_file():
				try:
					source_image = Image.open(source_path).convert("RGBA")
					_check(source_image.size == (cell_width, cell_height),
						f"{prefix} room-derived source size {source_image.size} does not "
						f"match cell {(cell_width, cell_height)}", failures)
					if source_image.size == (cell_width, cell_height):
						source_rgba = np.asarray(source_image, dtype=np.uint8)
						source_depth = source_rgba[:, :, 3] \
							>= DEPTH_ALPHA_THRESHOLD
						# The delivered rest base applies the builder's exact one-pixel
						# sampling guard before any action artwork is added. Reconstruct
						# that base rather than counting frame-zero faucet/light overlays.
						room_rest_depth = np.array(source_depth, copy=True)
						room_rest_depth[0, :] = False
						room_rest_depth[-1, :] = False
						room_rest_depth[:, 0] = False
						room_rest_depth[:, -1] = False
						room_rest_rgb = source_rgba[:, :, :3].astype(np.int16)
						source_depth_pixels = int(np.count_nonzero(source_depth))
						rest_depth_pixels = int(np.count_nonzero(room_rest_depth))
						overlap_pixels = int(np.count_nonzero(
							source_depth & room_rest_depth))
						retention = overlap_pixels / max(1, source_depth_pixels)
						metrics["silhouette_retention"].append(retention)
						_check(source_depth_pixels > 0,
							f"{prefix} room-derived source silhouette is empty", failures)
						_check(retention >= MIN_SOURCE_SILHOUETTE_RETENTION,
							f"{prefix} retains only {retention:.4f} of the source "
							f"silhouette; need {MIN_SOURCE_SILHOUETTE_RETENTION:.2f}", failures)
						if "source_depth_pixels" in record:
							_check(record.get("source_depth_pixels") == source_depth_pixels,
								f"{prefix} source_depth_pixels declaration is inaccurate",
								failures)
						if "rest_depth_pixels" in record:
							_check(record.get("rest_depth_pixels") == rest_depth_pixels,
								f"{prefix} rest_depth_pixels declaration is inaccurate",
								failures)
						if "silhouette_retention" in record:
							declared_retention = record.get("silhouette_retention")
							_check(isinstance(declared_retention, (int, float))
								and not isinstance(declared_retention, bool)
								and abs(float(declared_retention) - retention) <= 0.000001,
								f"{prefix} silhouette_retention declaration is inaccurate",
								failures)
				except Exception as exc:
					failures.append(f"{prefix} room-derived source cannot be decoded: {exc}")
			background_path = ROOM_DIR / f"room_{room_id}_background.png"
			if not background_path.is_file():
				failures.append(f"{prefix} healed room background is missing")
			elif (right - left, bottom - top) == (cell_width, cell_height):
				background = np.asarray(
					Image.open(background_path).convert("RGB").crop(crop), dtype=np.int16)
				color_delta = np.max(np.abs(room_rest_rgb - background), axis=2)
				opaque_pixels = int(np.count_nonzero(room_rest_depth))
				background_like = int(np.count_nonzero(
					room_rest_depth & (color_delta <= BACKGROUND_COLOR_TOLERANCE)))
				background_fraction = background_like / max(1, opaque_pixels)
				background_rest_coverage = background_like / room_rest_depth.size
				metrics["background_fraction"].append(background_fraction)
				_check(background_fraction <= MAX_BACKGROUND_LIKE_FRACTION,
					f"{prefix} rest frame has {background_fraction:.3f} background-like "
					f"depth pixels; limit is {MAX_BACKGROUND_LIKE_FRACTION:.3f}", failures)
				if background_fraction > BACKGROUND_CONDITIONAL_FRACTION:
					_check(background_rest_coverage <= MAX_CONDITIONAL_REST_COVERAGE
						and background_like <= MAX_CONDITIONAL_BACKGROUND_PIXELS,
						f"{prefix} background-like fraction {background_fraction:.3f} "
						f"above {BACKGROUND_CONDITIONAL_FRACTION:.2f} is allowed only for "
						f"coverage <= {MAX_CONDITIONAL_REST_COVERAGE:.2f} and <= "
						f"{MAX_CONDITIONAL_BACKGROUND_PIXELS} pixels (got "
						f"{background_rest_coverage:.3f}, {background_like})", failures)
	else:
		# Standalone/generated sources can have source-canvas padding cropped or
		# added by the builder.  The delivered rest cell is authoritative here.
		rest_coverage = int(np.count_nonzero(rest_depth)) / rest_depth.size
		_check(0.005 <= rest_coverage <= 1.0 - MIN_TRANSPARENT_FRACTION,
			f"{prefix} standalone-source rest occupancy {rest_coverage:.3f} is not sane",
			failures)

	sound_path = _repo_path(record.get("sound"), f"{prefix} sound", failures)
	if sound_path is None:
		return
	try:
		sound_path.resolve().relative_to(AUDIO_ROOT)
	except ValueError:
		failures.append(f"{prefix} sound must stay under assets/audio/castle")
		return
	if not sound_path.is_file():
		failures.append(f"{prefix} sound file is missing")
	elif sound_path.read_bytes()[:4] != b"OggS":
		failures.append(f"{prefix} sound is not an Ogg stream (missing OggS header)")


def main() -> None:
	failures: list[str] = []
	metrics: dict[str, list[float]] = defaultdict(list)
	try:
		manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
		depth_manifest = json.loads(DEPTH_MANIFEST_PATH.read_text(encoding="utf-8"))
		audio_manifest = json.loads(AUDIO_MANIFEST_PATH.read_text(encoding="utf-8"))
		roshan_alpha = _roshan_mask()
	except Exception as exc:
		print(f"FAIL: Castle interaction audit inputs cannot be loaded: {exc}")
		raise SystemExit(1)

	_check(manifest.get("schema_version") == 1,
		"manifest schema_version must be 1", failures)
	_check(manifest.get("generator") == "tools/build_castle_interaction_atlases.py",
		"manifest generator is not the approved atlas builder", failures)
	_audit_current_runtime_contract(depth_manifest, failures)
	frame_contract = manifest.get("frame_contract", {})
	_check(isinstance(frame_contract, dict)
		and frame_contract.get("minimum") == 4
		and frame_contract.get("maximum") == 12
		and frame_contract.get("delivered") == 8,
		"manifest frame_contract must declare 4..12 with 8 delivered frames", failures)
	audio_durations = _audio_durations(audio_manifest, failures)

	visual_review = manifest.get("visual_review_evidence")
	if not isinstance(visual_review, dict):
		failures.append("visual_review_evidence must be an object")
	else:
		expected_contact = "audit/castle_interactions/castle_interaction_frames.png"
		_check(visual_review.get("path") == expected_contact,
			f"visual review contact path must be {expected_contact}", failures)
		_check(visual_review.get("reviewed_frame_indices") == list(range(8)),
			"visual review evidence must cover contact frames 0 through 7", failures)
		contact_path = _repo_path(
			visual_review.get("path"), "visual review contact", failures)
		if contact_path is None or not contact_path.is_file():
			failures.append("visual review contact file is missing")
		else:
			_check(visual_review.get("sha256") == _sha256(contact_path),
				"visual review contact sha256 does not match file bytes", failures)
			try:
				with Image.open(contact_path) as contact_image:
					contact_dimensions = [contact_image.width, contact_image.height]
				_check(visual_review.get("dimensions") == contact_dimensions,
					"visual review contact dimensions are inaccurate", failures)
			except Exception as exc:
				failures.append(f"visual review contact cannot be decoded: {exc}")
	rooms = manifest.get("rooms")
	assets = manifest.get("assets")
	if not isinstance(rooms, dict) or not isinstance(assets, list):
		print("FAIL: Castle interaction manifest must contain rooms and assets")
		raise SystemExit(1)

	_check(set(rooms) == set(EXPECTED_ROOM_COUNTS),
		f"room roster must be exactly {sorted(EXPECTED_ROOM_COUNTS)}", failures)
	room_instances: dict[str, list[dict[str, Any]]] = {}
	for room_id, expected_count in EXPECTED_ROOM_COUNTS.items():
		room = rooms.get(room_id, {})
		instances = room.get("instances", []) if isinstance(room, dict) else []
		if not isinstance(instances, list):
			instances = []
			failures.append(f"{room_id}: instances must be a list")
		room_instances[room_id] = [item for item in instances if isinstance(item, dict)]
		_check(len(room_instances[room_id]) == len(instances),
			f"{room_id}: every instance must be an object", failures)
		_check(room.get("physical_item_count") == len(instances)
			and len(instances) == expected_count,
			f"{room_id}: physical item count must be {expected_count}", failures)
		ids = [str(item.get("id", "")) for item in room_instances[room_id]]
		_check(all(ids) and len(ids) == len(set(ids)),
			f"{room_id}: instance ids must be non-empty and unique within the room", failures)

	physical_count = sum(len(instances) for instances in room_instances.values())
	average = physical_count / max(1, len(rooms))
	non_hall_counts = [
		len(instances) for room_id, instances in room_instances.items()
		if room_id != "main_hall"
	]
	_check(4.0 <= average <= 6.0,
		f"physical item average {average:.3f} is outside 4..6", failures)
	_check(all(count >= 4 for count in non_hall_counts),
		"every non-hall room must contain at least 4 physical items", failures)
	_check(physical_count == 38,
		f"physical instance count must be 38, got {physical_count}", failures)

	asset_records = [record for record in assets if isinstance(record, dict)]
	_check(len(asset_records) == len(assets), "every asset entry must be an object", failures)
	asset_ids = [str(record.get("id", "")) for record in asset_records]
	_check(len(asset_ids) == len(set(asset_ids)), "asset ids must be unique", failures)
	_check(set(asset_ids) == set(EXPECTED_ASSETS),
		"asset roster must contain the 33 approved interaction atlases exactly", failures)
	_check(len(asset_records) == 33,
		f"unique animated asset count must be 33, got {len(asset_records)}", failures)
	atlas_values = [record.get("atlas") for record in asset_records]
	_check(len(set(str(value) for value in atlas_values)) == 33,
		"all 33 animated assets must have unique atlas paths", failures)

	asset_by_id = {str(record.get("id", "")): record for record in asset_records}
	manifest_instances: dict[str, list[tuple[str, str]]] = defaultdict(list)
	for room_id, instances in room_instances.items():
		for instance in instances:
			instance_id = str(instance.get("id", ""))
			asset_id = str(instance.get("asset_id", ""))
			record = asset_by_id.get(asset_id)
			if record is None:
				failures.append(f"{room_id}/{instance_id}: unknown asset_id {asset_id}")
				continue
			_check(record.get("room") == room_id,
				f"{room_id}/{instance_id}: asset belongs to another room", failures)
			_check(instance.get("semantic_action") == record.get("semantic_action"),
				f"{room_id}/{instance_id}: semantic action disagrees with asset", failures)
			manifest_instances[asset_id].append((room_id, instance_id))
	for asset_id, record in asset_by_id.items():
		declared = record.get("instances", [])
		actual_ids = [instance_id for _, instance_id in manifest_instances.get(asset_id, [])]
		_check(isinstance(declared, list) and sorted(str(value) for value in declared)
			== sorted(actual_ids),
			f"{asset_id}: asset instances disagree with room instance roster", failures)

	action_assets: dict[str, set[str]] = defaultdict(set)
	for record in asset_records:
		action_assets[str(record.get("semantic_action", ""))].add(str(record.get("id", "")))
	for action, action_asset_ids in action_assets.items():
		if len(action_asset_ids) <= 1:
			continue
		_check(REPEATED_ACTION_ALLOWLIST.get(action) == action_asset_ids,
			f"semantic action {action!r} is reused outside its approved item family: "
			f"{sorted(action_asset_ids)}", failures)

	crops = _depth_crops(depth_manifest)
	for record in asset_records:
		try:
			_audit_asset(record, crops, audio_durations, roshan_alpha, failures, metrics)
		except Exception as exc:
			failures.append(f"{record.get('id', '<missing-id>')}: audit error: {exc}")

	summary = manifest.get("summary", {})
	_check(isinstance(summary, dict), "manifest summary must be an object", failures)
	if isinstance(summary, dict):
		_check(summary.get("room_count") == 8, "summary room_count must be 8", failures)
		_check(summary.get("unique_animated_assets") == 33,
			"summary unique_animated_assets must be 33", failures)
		_check(summary.get("physical_item_instances") == 38,
			"summary physical_item_instances must be 38", failures)
		declared_average = summary.get("average_items_per_room")
		_check(isinstance(declared_average, (int, float))
			and abs(float(declared_average) - average) <= 0.001,
			"summary average_items_per_room does not match room roster", failures)
		_check(summary.get("minimum_non_hall_room_items") == min(non_hall_counts),
			"summary minimum_non_hall_room_items does not match room roster", failures)

	print(json.dumps({
		"rooms": len(rooms),
		"unique_atlases": len(asset_records),
		"physical_instances": physical_count,
		"average_items_per_room": round(average, 3),
		"maximum_depth_coverage": round(max(metrics["coverage"], default=0.0), 4),
		"maximum_background_like_fraction": round(
			max(metrics["background_fraction"], default=0.0), 4),
		"minimum_chassis_alpha_iou": round(min(metrics["chassis_iou"], default=0.0), 4),
		"minimum_sampled_roshan_visibility": round(
			min(metrics["roshan_visibility"], default=0.0), 4),
		"minimum_material_changed_fraction": round(
			min(metrics["changed_fraction"], default=0.0), 4),
		"minimum_source_silhouette_retention": round(
			min(metrics["silhouette_retention"], default=0.0), 4),
		"maximum_audio_sync_error_seconds": round(
			max(metrics["audio_sync_error"], default=0.0), 6),
	}, indent=2))
	if failures:
		for failure in failures:
			print(f"FAIL: {failure}")
		raise SystemExit(1)
	print("CASTLE INTERACTION AUDIT: ALL OK")


if __name__ == "__main__":
	main()
