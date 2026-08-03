#!/usr/bin/env python3
"""Blocking integrity audit for Pearl Castle dream-house rooms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
	ROOT / "audit" / "castle_dream_house"
	/ "dream_house_room_art_manifest.json"
)
RUNTIME_SCRIPT = ROOT / "scripts" / "arena" / "castle_rooms_25d.gd"
REQUIRED_ROOMS = {
	"family_gallery",
	"dining_room",
	"royal_bedroom",
	"sleepover_bedroom",
	"movie_lounge",
}
REQUIRED_ROLEPLAY = {
	'"roleplay_action": "enter_room"',
	'"roleplay_action": "serve_meal"',
	'"roleplay_action": "eat_meal"',
	'"roleplay_action": "sleep"',
	'"roleplay_action": "watch_movie"',
	'"roleplay_action": "relax"',
}
PROTECTED_MOVIE_PATHS = {
	"res://assets/book/hall/p_slide.jpg",
	"res://assets/book/hall/p_trampoline.jpg",
	"res://assets/book/hall/p_garden.jpg",
	"res://assets/book/hall/p_snowman.jpg",
	"res://assets/book/hall/p_xmas.jpg",
}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def check(condition: bool, message: str, failures: list[str]) -> None:
	if not condition:
		failures.append(message)


def repo_path(value: object, label: str, failures: list[str]) -> Path:
	check(isinstance(value, str) and bool(value),
		f"{label} must be a non-empty repository path", failures)
	path = ROOT / str(value)
	check(path.is_file(), f"{label} missing: {value}", failures)
	return path


def main() -> None:
	failures: list[str] = []
	check(MANIFEST_PATH.is_file(),
		"dream-house art manifest is missing", failures)
	if failures:
		raise SystemExit("\n".join(f"FAIL: {item}" for item in failures))
	manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
	check(manifest.get("schema") == "castle_dream_house_room_art_v3",
		"unexpected dream-house manifest schema", failures)
	check(manifest.get("protected_originals_modified") is False,
		"manifest does not preserve protected originals", failures)
	check(manifest.get("runtime_world_art") == "unshaded Sprite3D cards only",
		"runtime world-art method changed", failures)

	check(manifest.get("blender_runtime_pixels") is False,
		"Blender render pixels are not blocked from runtime", failures)
	check(manifest.get("source_visual_medium")
		== "polished flattened 2D storybook illustration",
		"dream-house source medium is not approved 2D storybook art", failures)
	node_inventory = manifest.get("node_type_inventory", {})
	check(node_inventory.get("world_art_node") == "Sprite3D",
		"world-art node inventory is not Sprite3D", failures)
	check(node_inventory.get("forbidden_world_nodes") == [],
		"node inventory contains forbidden world-art nodes", failures)

	production_sheets = manifest.get("production_sheets", [])
	check(len(production_sheets) == 2,
		"expected exactly two accepted 2D production sheets", failures)
	sheet_roles = {str(record.get("role", "")) for record in production_sheets}
	check(sheet_roles == {
			"physical_door_family", "four_room_furnishing_family"},
		"2D production-sheet roles changed", failures)
	allowed_alpha_sources: set[str] = set()
	for sheet_record in production_sheets:
		role = str(sheet_record.get("role", "sheet"))
		expected_prompt_id = {
			"physical_door_family": "physical-door-family",
			"four_room_furnishing_family": "four-room-furnishing-family",
		}.get(role, "")
		check(sheet_record.get("prompt_id") == expected_prompt_id,
			f"{role} prompt id changed", failures)
		prompt_path = repo_path(
			sheet_record.get("prompt_path"), f"{role} prompt ledger", failures)
		if prompt_path.is_file():
			check(sha256(prompt_path) == sheet_record.get("prompt_sha256"),
				f"{role} prompt ledger hash changed", failures)
		chroma_path = repo_path(
			sheet_record.get("chroma_path"), f"{role} chroma sheet", failures)
		alpha_path = repo_path(
			sheet_record.get("alpha_path"), f"{role} alpha sheet", failures)
		if chroma_path.is_file():
			check(sha256(chroma_path) == sheet_record.get("chroma_sha256"),
				f"{role} chroma sheet hash changed", failures)
		if alpha_path.is_file():
			check(sha256(alpha_path) == sheet_record.get("alpha_sha256"),
				f"{role} alpha sheet hash changed", failures)
			with Image.open(alpha_path) as alpha_image:
				check(list(alpha_image.size) == sheet_record.get("dimensions"),
					f"{role} alpha sheet dimensions drifted", failures)
				alpha_min, alpha_max = alpha_image.convert("RGBA").getchannel(
					"A").getextrema()
				check(alpha_min == 0 and alpha_max == 255,
					f"{role} alpha sheet lacks clean transparency", failures)
			allowed_alpha_sources.add(
				alpha_path.relative_to(ROOT).as_posix())


	imagegen_reference = manifest.get("imagegen_reference", {})
	check(imagegen_reference.get("role") == "composition_reference_only",
		"ImageGen output is not reference-only", failures)
	check(imagegen_reference.get("used_as_runtime_pixels") is False,
		"ImageGen reference pixels entered runtime art", failures)
	reference_path = repo_path(
		imagegen_reference.get("path"), "ImageGen reference", failures)
	if reference_path.is_file():
		check(sha256(reference_path) == imagegen_reference.get("sha256"),
			"ImageGen reference hash changed", failures)

	physical_layout = manifest.get("physical_layout", {})
	expected_destinations = {
		"dining_room": "family_portal_dining.png",
		"royal_bedroom": "family_portal_royal_bedroom.png",
		"sleepover_bedroom": "family_portal_sleepover_bedroom.png",
		"movie_lounge": "family_portal_movie_lounge.png",
	}
	check(physical_layout.get("gallery_room") == "family_gallery",
		"physical gallery room changed", failures)
	check(physical_layout.get("destinations") == expected_destinations,
		"physical gallery destination map changed", failures)
	check(physical_layout.get("floating_route_buttons") is False,
		"floating route buttons returned", failures)
	check(physical_layout.get("main_hall_entry")
		== "assets/flats/castle/dream_house/family_wing_hall_insert.png",
		"constructed Main Hall wing entry changed", failures)
	repo_path(physical_layout.get("main_hall_entry"),
		"constructed Main Hall wing entry", failures)

	contact_path = repo_path(manifest.get("contact_sheet"),
		"dream-house room contact", failures)
	if contact_path.is_file():
		with Image.open(contact_path) as contact:
			check(contact.size == (1536, 576),
				"dream-house room contact dimensions changed", failures)
	layout_contact = manifest.get("layout_contact", {})
	layout_contact_path = repo_path(layout_contact.get("path"),
		"dream-house layout contact", failures)
	if layout_contact_path.is_file():
		with Image.open(layout_contact_path) as contact:
			check(contact.size == (1280, 576),
				"dream-house layout contact dimensions changed", failures)
		check(sha256(layout_contact_path) == layout_contact.get("sha256"),
			"dream-house layout contact hash changed", failures)

	furnished_review = manifest.get("furnished_room_review", {})
	furnished_contact_path = repo_path(
		furnished_review.get("path"), "furnished-room placement contact", failures)
	if furnished_contact_path.is_file():
		check(sha256(furnished_contact_path) == furnished_review.get("sha256"),
			"furnished-room placement contact hash changed", failures)
		with Image.open(furnished_contact_path) as contact:
			check(list(contact.size) == furnished_review.get("dimensions")
				== [2048, 1152],
				"furnished-room contact dimensions changed", failures)
	check(furnished_review.get("critical_overlaps") == [],
		"gallery doors or sleepover beds overlap", failures)
	check(furnished_review.get("protected_movie_pixels_copied") is False,
		"protected movie pixels were copied into placement evidence", failures)
	placement_records = furnished_review.get("placements", [])
	check(len(placement_records) == 24,
		"furnished-room placement inventory is incomplete", failures)
	for placement in placement_records:
		check(float(placement.get("visible_fraction", 0.0)) >= 0.999,
			f"furnished card is clipped: {placement.get('room_id')}:"
			f"{placement.get('item_id')}", failures)

	hall_entry_contact = manifest.get("hall_entry_contact", {})
	hall_entry_contact_path = repo_path(hall_entry_contact.get("path"),
		"Main Hall wing-entry contact", failures)
	if hall_entry_contact_path.is_file():
		with Image.open(hall_entry_contact_path) as contact:
			check(contact.size == (1024, 576),
				"Main Hall wing-entry contact dimensions changed", failures)
		check(sha256(hall_entry_contact_path)
			== hall_entry_contact.get("sha256"),
			"Main Hall wing-entry contact hash changed", failures)
	hall_entry_source_path = repo_path(hall_entry_contact.get("source"),
		"Main Hall wing-entry contact source", failures)
	if hall_entry_source_path.is_file():
		check(sha256(hall_entry_source_path)
			== hall_entry_contact.get("source_sha256"),
			"Main Hall wing-entry source changed", failures)
	check(hall_entry_contact.get("source_crop") == [376, 212, 2048, 1153],
		"Main Hall wing-entry source crop changed", failures)
	check(hall_entry_contact.get("insert_position") == [35, 200],
		"Main Hall wing-entry insert position changed", failures)

	room_records = manifest.get("rooms", [])
	room_ids = {str(record.get("room_id", "")) for record in room_records}
	check(room_ids == REQUIRED_ROOMS,
		f"dream-house room set changed: {sorted(room_ids)}", failures)
	for record in room_records:
		room_id = str(record.get("room_id", ""))
		master_path = repo_path(
			record.get("master"), f"{room_id} master", failures)
		if not master_path.is_file():
			continue
		with Image.open(master_path) as master_image:
			master = master_image.convert("RGB")
		check(master.size == (2048, 2048),
			f"{room_id} master must be 2048x2048", failures)
		check(list(master.size) == record.get("master_dimensions"),
			f"{room_id} manifest master dimensions drifted", failures)
		check(sha256(master_path) == record.get("master_sha256"),
			f"{room_id} master hash changed", failures)
		crop_box = tuple(int(value) for value in record.get(
			"runtime_crop", []))
		check(crop_box == (0, 448, 2048, 1600),
			f"{room_id} runtime crop changed", failures)
		if len(crop_box) != 4:
			continue
		gameplay = master.crop(crop_box)
		reconstruction = Image.new("RGB", (2048, 1152))
		tiles = record.get("tiles", [])
		check(len(tiles) == 4,
			f"{room_id} must have four runtime tiles", failures)
		for tile_record in tiles:
			tile_path = repo_path(
				tile_record.get("path"), f"{room_id} tile", failures)
			if not tile_path.is_file():
				continue
			with Image.open(tile_path) as tile_image:
				tile = tile_image.convert("RGB")
				check(tile.size == (1024, 576),
					f"{room_id} runtime tile is not 1024x576", failures)
				check(list(tile.size) == tile_record.get("dimensions"),
					f"{room_id} tile dimensions drifted", failures)
				check(sha256(tile_path) == tile_record.get("sha256"),
					f"{room_id} tile hash changed", failures)
				left = int(tile_record.get("column", -1)) * 1024
				top = int(tile_record.get("row", -1)) * 576
				reconstruction.paste(tile, (left, top))
		check(ImageChops.difference(
			gameplay, reconstruction).getbbox() is None,
			f"{room_id} tiles do not reconstruct the native crop", failures)

	prop_records = manifest.get("props", [])
	check(len(prop_records) >= 22,
		"dream-house prop inventory is incomplete", failures)
	required_portal_paths = {
		"assets/flats/castle/dream_house/family_wing_portal.png",
		"assets/flats/castle/dream_house/family_portal_dining.png",
		"assets/flats/castle/dream_house/family_portal_royal_bedroom.png",
		"assets/flats/castle/dream_house/family_portal_sleepover_bedroom.png",
		"assets/flats/castle/dream_house/family_portal_movie_lounge.png",
		"assets/flats/castle/dream_house/family_wing_hall_insert.png",
	}
	prop_paths = {str(record.get("path", "")) for record in prop_records}
	check(required_portal_paths <= prop_paths,
		"physical dream-house portal inventory is incomplete", failures)
	door_sheet_source = (
		"assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/"
		"door_family_sheet_alpha.png"
	)
	for record in prop_records:
		if str(record.get("path", "")) in required_portal_paths:
			check(record.get("source") == door_sheet_source,
				"physical portal does not come from the accepted 2D door family",
				failures)

	for record in prop_records:
		prop_path = repo_path(record.get("path"), "dream-house prop", failures)
		if not prop_path.is_file():
			continue
		with Image.open(prop_path) as prop:
			check(max(prop.size) <= 1024,
				f"runtime prop exceeds 1024: {prop_path.name}", failures)
			check(list(prop.size) == record.get("dimensions"),
				f"prop dimensions drifted: {prop_path.name}", failures)
			alpha_min, alpha_max = prop.convert("RGBA").getchannel(
				"A").getextrema()
			check(alpha_min == 0 and alpha_max >= 128,
				f"prop lacks a transparent silhouette: {prop_path.name}",
				failures)
		check(sha256(prop_path) == record.get("sha256"),
			f"prop hash changed: {prop_path.name}", failures)
		source_value = record.get("source")
		check(record.get("blender_runtime_pixels") is False,
			f"prop permits Blender runtime pixels: {prop_path.name}", failures)
		check(isinstance(source_value, str)
			and source_value in allowed_alpha_sources,
			f"prop is not extracted from an accepted 2D sheet: {prop_path.name}",
			failures)
		check("/blender/" not in str(source_value).replace("\\", "/"),
			f"prop still references a Blender source: {prop_path.name}", failures)
		if isinstance(source_value, str) \
				and source_value.startswith("assets"):
			source_path = repo_path(
				source_value, f"{prop_path.name} source", failures)
			if source_path.is_file():
				check(sha256(source_path) == record.get("source_sha256"),
					f"approved source changed: {source_path.name}", failures)

	for legacy_path in (
			"assets/flats/castle/dream_house/shell_arch.png",
			"assets/flats/castle/dream_house/shell_window.png"):
		check(not (ROOT / legacy_path).exists(),
			f"unused Blender-derived runtime card returned: {legacy_path}",
			failures)
	runtime_text = RUNTIME_SCRIPT.read_text(encoding="utf-8")
	for placement in placement_records:
		source_position = placement.get("source_position", [])
		if not isinstance(source_position, list) or len(source_position) != 2:
			check(False, "placement source position is malformed", failures)
			continue
		token = (
			f'"pos": Vector2({float(source_position[0]):.1f}, '
			f'{float(source_position[1]):.1f}), '
			f'"z": {float(placement.get("z", 0.0)):.2f}, '
			f'"scale": {float(placement.get("uniform_scale", 1.0)):.2f}')
		check(token in runtime_text,
			f"runtime placement drifted: {placement.get('room_id')}:"
			f"{placement.get('item_id')}", failures)
	for door_token in (
			'"pos": Vector2(-40.0, 79.0), "z": 0.86, "scale": 0.60',
			'"pos": Vector2(200.0, 77.0), "z": 0.87, "scale": 0.60',
			'"pos": Vector2(448.0, 89.0), "z": 0.88, "scale": 0.60',
			'"pos": Vector2(680.0, 89.0), "z": 0.89, "scale": 0.60'):
		check(door_token in runtime_text,
			f"physical gallery door placement drifted: {door_token}", failures)
	check('"z": 0.01, "scale": 0.82, "shaded": false' in runtime_text,
		"Main Hall family-wing door scale drifted", failures)
	for room_id in REQUIRED_ROOMS:
		check(f'"id": "{room_id}"' in runtime_text,
			f"runtime room missing: {room_id}", failures)
		check(f'"{room_id}":' in runtime_text,
			f"runtime room layout/items missing: {room_id}", failures)
	for contract in REQUIRED_ROLEPLAY:
		check(contract in runtime_text,
			f"role-play contract missing: {contract}", failures)
	for destination, portal_file in expected_destinations.items():
		check(f'"room_destination": "{destination}"' in runtime_text,
			f"physical gallery route missing: {destination}", failures)
		check(portal_file in runtime_text,
			f"physical portal art missing: {portal_file}", failures)
		check(f'"{destination}": "family_gallery"' in runtime_text,
			f"Back route does not return to gallery: {destination}", failures)
	check('"family_gallery": "main_hall"' in runtime_text,
		"gallery Back route does not return to Main Hall", failures)
	check("family_wing_hall_insert.png" in runtime_text,
		"constructed Main Hall wing entry is not loaded", failures)
	check('"DreamHouseDoor_"' not in runtime_text,
		"floating dream-house route buttons remain in runtime", failures)
	check("m.castle_room_link_layer.visible = false" in runtime_text,
		"obsolete floating route layer is not locked off", failures)

	for movie_path in PROTECTED_MOVIE_PATHS:
		check(movie_path in runtime_text,
			f"direct protected movie path missing: {movie_path}", failures)
	check("dining_room_reference_1254.png" not in runtime_text,
		"reference-only ImageGen file is loaded by runtime", failures)
	check("MeshInstance3D.new()" not in runtime_text,
		"dream-house runtime introduced modeled world art", failures)
	check("Sprite3D.new()" in runtime_text,
		"dream-house runtime no longer constructs Sprite3D world cards",
		failures)
	for forbidden_node in (
			"Sprite2D.new()", "AnimatedSprite2D.new()",
			"TextureRect.new()", "Polygon2D.new()"):
		check(forbidden_node not in runtime_text,
			f"forbidden world-art node constructor found: {forbidden_node}",
			failures)

	result = {
		"rooms": len(room_records),
		"runtime_tiles": sum(len(record.get("tiles", []))
			for record in room_records),
		"props": len(prop_records),
		"failures": len(failures),
	}
	print(json.dumps(result, indent=2))
	if failures:
		for failure in failures:
			print("FAIL:", failure)
		raise SystemExit(1)


if __name__ == "__main__":
	main()
