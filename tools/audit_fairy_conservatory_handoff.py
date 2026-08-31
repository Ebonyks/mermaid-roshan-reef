#!/usr/bin/env python3
"""Fail-closed static acceptance audit for the Chapter 3 fairy handoff."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_ROOT = ROOT / "assets" / "flats" / "fairy_conservatory_handoff"
HANDOFF_SOURCE = ROOT / "assets_src" / "fairy_conservatory_handoff_2026-08-30"
DOOR_ROOT = ROOT / "assets" / "flats" / "castle" / "fairy_conservatory"
DOOR_SOURCE = (
	ROOT / "assets_src" / "castle"
	/ "fairy_conservatory_chapter3_2026-08-30"
)

failures: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
	status = "OK" if condition else "FAIL"
	suffix = f" ({detail})" if detail else ""
	print(f"FAIRYHANDOFF|{status}|{label}{suffix}")
	if not condition:
		failures.append(label)


def digest(path: Path) -> str:
	hasher = sha256()
	with path.open("rb") as source:
		for block in iter(lambda: source.read(1024 * 1024), b""):
			hasher.update(block)
	return hasher.hexdigest()


def image(path: Path) -> Image.Image | None:
	if not path.is_file():
		check(f"asset exists: {path.relative_to(ROOT).as_posix()}", False)
		return None
	try:
		return Image.open(path)
	except (OSError, ValueError) as error:
		check(f"asset decodes: {path.relative_to(ROOT).as_posix()}", False, str(error))
		return None


def gd_function_body(source: str, function_name: str) -> str:
	marker = f"func {function_name}("
	start = source.find(marker)
	if start < 0:
		return ""
	next_function = source.find("\nfunc ", start + len(marker))
	return source[start:] if next_function < 0 else source[start:next_function]


def py_function_body(source: str, function_name: str) -> str:
	marker = f"def {function_name}("
	start = source.find(marker)
	if start < 0:
		return ""
	next_function = source.find("\ndef ", start + len(marker))
	return source[start:] if next_function < 0 else source[start:next_function]


def audit_cutout(path: Path) -> Image.Image | None:
	asset = image(path)
	if asset is None:
		return None
	label = path.name
	check(f"{label} is 1024-square", asset.size == (1024, 1024), str(asset.size))
	check(f"{label} is RGBA", asset.mode == "RGBA", asset.mode)
	if asset.mode != "RGBA":
		return asset
	alpha = np.asarray(asset.getchannel("A"), dtype=np.uint8)
	corners = [int(alpha[0, 0]), int(alpha[0, -1]),
		int(alpha[-1, 0]), int(alpha[-1, -1])]
	check(f"{label} corners are transparent", not any(corners), str(corners))
	check(f"{label} has a visible subject", bool(np.count_nonzero(alpha)))
	return asset


def audit_background() -> None:
	master_path = HANDOFF_SOURCE / "masters" / "handoff_background_master_3640x2048.png"
	master = image(master_path)
	if master is None:
		return
	check("background master meets per-screen runtime coverage",
		master.size[0] >= 2048 and master.size[1] >= 2048, str(master.size))
	check("background master preserves 16:9 stage crop",
		master.size == (3640, 2048), str(master.size))
	rows: list[np.ndarray] = []
	all_tiles_valid = True
	for row in range(2):
		columns: list[np.ndarray] = []
		for column in range(4):
			path = HANDOFF_ROOT / "background" / f"handoff_background_r{row}_c{column}.png"
			tile = image(path)
			if tile is None:
				all_tiles_valid = False
				continue
			check(f"background r{row}c{column} is runtime-safe",
				tile.size == (910, 1024) and max(tile.size) <= 1024,
				str(tile.size))
			columns.append(np.asarray(tile.convert("RGB"), dtype=np.uint8))
		if len(columns) == 4:
			rows.append(np.concatenate(columns, axis=1))
		else:
			all_tiles_valid = False
	if all_tiles_valid and len(rows) == 2:
		rebuilt = np.concatenate(rows, axis=0)
		source = np.asarray(master.convert("RGB"), dtype=np.uint8)
		check("background tiles reconstruct the continuous master exactly",
			rebuilt.shape == source.shape and np.array_equal(rebuilt, source))
	builder_path = ROOT / "tools" / "build_fairy_conservatory_handoff_art.py"
	if builder_path.is_file():
		builder = builder_path.read_text(encoding="utf-8")
		build_body = py_function_body(builder, "_build_background")
		align_body = py_function_body(builder, "_align_top_panel")
		assemble_body = py_function_body(builder, "_assemble_native_background")
		check("background builder authors the target master without ImageOps.fit",
			"ImageOps.fit" not in build_body)
		check("generated background panels are never resized",
			".resize(" not in build_body
			and ".resize(" not in align_body
			and ".resize(" not in assemble_body)


def audit_threshold_coverage(open_view: dict[str, object]) -> None:
	walkway_path = HANDOFF_ROOT / "rainbow_walkway.png"
	walkway = image(walkway_path)
	if walkway is None:
		return
	walkway = walkway.convert("RGBA")
	bounds = walkway.getchannel("A").getbbox()
	if bounds is None:
		check("rainbow walkway has threshold alpha", False)
		return
	walkway = walkway.crop(bounds)
	scale = 630.0 / max(walkway.size)
	walkway = walkway.resize(
		(max(1, round(walkway.width * scale)),
		 max(1, round(walkway.height * scale))),
		Image.Resampling.LANCZOS,
	)
	alpha = np.asarray(walkway.getchannel("A"), dtype=np.uint8)
	center_left = round(walkway.width * 0.33)
	center_right = round(walkway.width * 0.67)
	center_rows = np.flatnonzero(
		np.any(alpha[:, center_left:center_right] >= 64, axis=1))
	if not center_rows.size:
		check("rainbow walkway has a measurable center foot", False)
		return
	opening = open_view.get("opening_mask", {})
	opening_left = int(opening.get("left", -1))
	opening_right = int(opening.get("right", -1))
	opening_bottom = int(opening.get("bottom", -1))
	overdraw = int(open_view.get("walkway_threshold_overdraw_pixels", -1))
	center_foot = int(center_rows[-1]) + 1
	top = opening_bottom - center_foot + overdraw
	left = 512 - walkway.width // 2
	coverage = np.zeros((1024, 1024), dtype=np.uint8)
	y_start = max(0, top)
	y_end = min(1024, top + walkway.height)
	x_start = max(0, left)
	x_end = min(1024, left + walkway.width)
	coverage[y_start:y_end, x_start:x_end] = alpha[
		y_start - top:y_end - top,
		x_start - left:x_end - left,
	]
	region = coverage[
		opening_bottom - 6:opening_bottom + 1,
		opening_left:opening_right,
	]
	covered = int(np.count_nonzero(region >= 64))
	check("rainbow walkway fully covers the door threshold before clipping",
		region.size > 0 and covered == region.size,
		f"covered={covered}/{region.size} overdraw={overdraw}")


def audit_manifests() -> None:
	handoff_manifest_path = HANDOFF_SOURCE / "asset_manifest.json"
	door_manifest_path = DOOR_SOURCE / "asset_manifest.json"
	for path in (handoff_manifest_path, door_manifest_path):
		check(f"manifest exists: {path.relative_to(ROOT).as_posix()}", path.is_file())
	if not handoff_manifest_path.is_file() or not door_manifest_path.is_file():
		return
	handoff = json.loads(handoff_manifest_path.read_text(encoding="utf-8"))
	door = json.loads(door_manifest_path.read_text(encoding="utf-8"))
	check("handoff manifest records built-in ImageGen",
		handoff.get("generation_method") == "OpenAI built-in image generation")
	background = handoff.get("background", {})
	check("handoff background is the generated upright Fairy Pond",
		background.get("reference_authority")
		== "Lily-Pad Fairy World / Fairy Pond")
	panels = background.get("panels", [])
	expected_panels = {
		"top_left", "top_center", "top_right",
		"bottom_left", "bottom_center", "bottom_right",
	}
	check("handoff records all six native generated panels",
		len(panels) == 6
		and {str(record.get("name", "")) for record in panels} == expected_panels)
	for record in panels:
		panel_path = ROOT / str(record.get("path", ""))
		panel = image(panel_path)
		if panel is None:
			continue
		check(f"native panel dimensions match: {panel_path.name}",
			panel.size == (1254, 1254)
			and record.get("dimensions") == [1254, 1254], str(panel.size))
		check(f"native panel hash matches: {panel_path.name}",
			digest(panel_path) == record.get("sha256"))
		check(f"native panel remains at 1:1 scale: {panel_path.name}",
			float(record.get("scale", -1.0)) == 1.0)
	master_record = background.get("master", {})
	check("background master is authored at target native dimensions",
		master_record.get("authored_at_target_dimensions") is True)
	check("background master forbids source-pixel enlargement",
		master_record.get("source_pixel_upscale") is False)
	check("native panel geometry reconstructs the exact master",
		master_record.get("panel_size") == [1254, 1254]
		and master_record.get("panel_step") == [1193, 794]
		and master_record.get("panel_overlap") == [61, 460]
		and 1254 + 2 * 1193 == 3640
		and 1254 + 794 == 2048)
	check("generated panel horizon remains above the 50% line",
		int(master_record.get("aligned_horizon_y", 2048)) <= 1024)
	reference_paths = {
		str(record.get("path", ""))
		for record in background.get("reference_inputs", [])
	}
	check("approved Fairy Pond panorama is the primary background reference",
		"assets/fairy/pond_panorama.png" in reference_paths)
	check("handoff background excludes Sky Lagoon reference authority",
		all("sky_lagoon" not in path.lower() for path in reference_paths))
	check("handoff manifest records exactly two generated foreground gaps",
		set(handoff.get("generated_subjects", {}))
		== {"rainbow_walkway", "butterfly_house"})
	for record in handoff.get("generated_subjects", {}).values():
		runtime = ROOT / str(record.get("runtime", ""))
		check(f"runtime hash matches manifest: {runtime.name}",
			runtime.is_file() and digest(runtime) == record.get("runtime_sha256"))
	review = handoff.get("review_only_composite", {})
	check("placement composite is explicitly non-delivery",
		review.get("delivery_pixels") is False)
	open_view = door.get("states", {}).get("open", {}).get("view_composition", {})
	horizon = float(open_view.get("horizon_fraction", 1.0))
	check("door horizon is at or below the 50% line", horizon <= 0.5,
		f"fraction={horizon:.4f}")
	check("door view uses the Lily-Pad Fairy World authority",
		open_view.get("location_authority")
		== "Lily-Pad Fairy World / Fairy Pond")
	opening_bottom = int(open_view.get("opening_mask", {}).get("bottom", -1))
	walkway_base = int(open_view.get("walkway_visible_base_y", -2))
	check("rainbow art begins at the exact door-opening base",
		open_view.get("walkway_base_matches_opening_base") is True
		and walkway_base == opening_bottom,
		f"walkway={walkway_base} opening={opening_bottom}")
	audit_threshold_coverage(open_view)
	check("door manifest names the Rainbow Stage destination",
		"Rainbow Stage" in str(open_view.get("destination", "")))
	for state in ("closed", "open"):
		record = door.get("states", {}).get(state, {})
		runtime = ROOT / str(record.get("runtime", ""))
		check(f"door {state} hash matches manifest",
			runtime.is_file() and digest(runtime) == record.get("runtime_sha256"))
		hall_review = record.get("hall_review", {})
		hall_path = ROOT / str(hall_review.get("path", ""))
		check(f"door {state} Hall review is explicitly non-delivery",
			hall_review.get("delivery_pixels") is False)
		check(f"door {state} Hall review hash matches manifest",
			hall_path.is_file() and digest(hall_path) == hall_review.get("sha256"))


def audit_runtime_contract() -> None:
	stage_path = ROOT / "scripts" / "arena" / "fairy_conservatory_handoff_2d.gd"
	main_path = ROOT / "scripts" / "main.gd"
	save_path = ROOT / "scripts" / "save_state.gd"
	castle_path = ROOT / "scripts" / "arena" / "castle_rooms_25d.gd"
	door_path = ROOT / "scripts" / "arena" / "fairy_conservatory_door_2d.gd"
	pause_path = ROOT / "scripts" / "pause_menu.gd"
	route_probe_path = ROOT / "scripts" / "probe_fairy_conservatory_route.gd"
	handoff_probe_path = ROOT / "scripts" / "probe_fairy_conservatory_handoff.gd"
	for path in (
		stage_path, main_path, save_path, castle_path, door_path, pause_path,
		route_probe_path, handoff_probe_path,
	):
		check(f"runtime source exists: {path.relative_to(ROOT).as_posix()}", path.is_file())
	if not all(path.is_file() for path in (
		stage_path, main_path, save_path, castle_path, door_path, pause_path,
		route_probe_path, handoff_probe_path,
	)):
		return
	stage = stage_path.read_text(encoding="utf-8")
	for forbidden in (
		"Node3D", "Sprite3D", "Camera3D", "MeshInstance3D",
		"Vector3", "Transform3D", "StandardMaterial3D",
	):
		check(f"new stage excludes {forbidden}", forbidden not in stage)
	for required in (
		"Vector2(910.0, 1024.0)",
		"Vector2(640.0, 600.0)",
		"Vector2(640.0, 500.0)",
		"Vector2(640.0, 375.0)",
		'"no_fail_state": true',
		'"has_timer": false',
		'"butterfly_house"',
	):
		check(f"stage contract contains {required}", required in stage)
	main = main_path.read_text(encoding="utf-8")
	save = save_path.read_text(encoding="utf-8")
	castle = castle_path.read_text(encoding="utf-8")
	door = door_path.read_text(encoding="utf-8")
	pause = pause_path.read_text(encoding="utf-8")
	route_probe = route_probe_path.read_text(encoding="utf-8")
	handoff_probe = handoff_probe_path.read_text(encoding="utf-8")
	for key in (
		"chapter3_fairy_door_revealed",
		"chapter3_fairy_door_opened",
		"chapter3_fairy_mission_started",
	):
		check(f"save schema includes {key}", key in save)
		check(f"main owns {key}", key in main)
	check("Main Hall owns one whole door card",
		"MoonflowerConservatoryDoor" in door
		and "DOOR_CENTER := Vector2(1672.0, 385.0)" in door)
	check("Main Hall route bypasses fake room portal list",
		'm.call("_start_fairy_conservatory_handoff")' in door)
	check("approved Castle V4 payload stays independent",
		"MoonflowerConservatory" not in castle)
	check("Main ticks the independent doorway overlay",
		'_fairy_conservatory_door_ref().call("tick")' in main)
	check("Galaxy return recognizes the handoff",
		"fairy_conservatory_galaxy_return" in main
		and 'call_deferred("_start_fairy_conservatory_handoff", true)' in main)
	check("active stage receives an explicit tick",
		'fairy_conservatory_handoff.call("tick", delta)' in main)
	main_leave = gd_function_body(main, "_leave_current_activity")
	pause_leave = gd_function_body(pause, "_leave_current_activity")
	check("Main leave wrapper does not duplicate Galaxy scheduling",
		'_start_galaxy' not in main_leave)
	check("PauseMenu owns exactly one Fairy Pond Galaxy restart",
		pause_leave.count('call_deferred("_start_galaxy")') == 1)
	load_body = gd_function_body(save, "load_save")
	check("Opera completion waits for the in-Hall reveal before persisting",
		"fairy_candle_reveal" not in load_body
		and 'save_data.get("opera_done"' not in load_body[
			load_body.find("legacy_fairy_route"):load_body.find("combat_ice_done")])
	check("isolated handoff probe covers the guided reverse walk",
		'"rainbow_return"' in handoff_probe
		and '"guided reverse walk completes home"' in handoff_probe)
	for evidence in (
		"fresh door is dormant",
		"reveal creates exactly one hotspot",
		"open route removes the reveal pointer",
		"Hall suspend/resume preserves camera offset",
	):
		check(f"route probe covers {evidence}", evidence in route_probe)


def audit_ledger() -> None:
	licenses = (ROOT / "ASSET_LICENSES.md").read_text(encoding="utf-8")
	for token in (
		"moonflower_door_closed.png",
		"moonflower_door_open.png",
		"moonflower_door_{closed,open}_hall_1280x720.png",
		"rainbow_walkway.png",
		"butterfly_house.png",
		"fairy_pond_horizon_openai_raw.png",
		"fairy_pond_native_center_openai_raw.png",
		"background_panels/{top_left,top_center,top_right,bottom_left,bottom_center,bottom_right}.png",
		"handoff_background_master_3640x2048.png",
		"handoff_background_r{0..1}_c{0..3}.png",
		"rainbow_stage_composite_1280x720.png",
	):
		check(f"license ledger covers {token}", token in licenses)


def main() -> int:
	closed = audit_cutout(DOOR_ROOT / "moonflower_door_closed.png")
	opened = audit_cutout(DOOR_ROOT / "moonflower_door_open.png")
	audit_cutout(HANDOFF_ROOT / "rainbow_walkway.png")
	audit_cutout(HANDOFF_ROOT / "butterfly_house.png")
	if closed is not None and opened is not None \
			and closed.mode == "RGBA" and opened.mode == "RGBA":
		closed_box = closed.getchannel("A").getbbox()
		open_box = opened.getchannel("A").getbbox()
		if closed_box and open_box:
			closed_center = (closed_box[0] + closed_box[2]) * 0.5
			open_center = (open_box[0] + open_box[2]) * 0.5
			check("door states share the same horizontal pivot",
				abs(closed_center - open_center) <= 1.0,
				f"closed={closed_center} open={open_center}")
			check("door states share the same visual height",
				closed_box[3] - closed_box[1] == open_box[3] - open_box[1])
	audit_background()
	audit_manifests()
	audit_runtime_contract()
	audit_ledger()
	print(f"FAIRYHANDOFF|RESULT={'FAIL' if failures else 'OK'}|failures={len(failures)}")
	return 1 if failures else 0


if __name__ == "__main__":
	sys.exit(main())
