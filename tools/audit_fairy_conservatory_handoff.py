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
	check("background master meets per-screen native coverage",
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
	check("handoff manifest records exactly two generated gaps",
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
