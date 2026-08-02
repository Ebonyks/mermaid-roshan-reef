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
	check(manifest.get("schema") == "castle_dream_house_room_art_v2",
		"unexpected dream-house manifest schema", failures)
	check(manifest.get("protected_originals_modified") is False,
		"manifest does not preserve protected originals", failures)
	check(manifest.get("runtime_world_art") == "unshaded Sprite3D cards only",
		"runtime world-art method changed", failures)

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
	check(len(prop_records) >= 23,
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
	approved_portal_source = (
		"assets/flats/castle/main_hall_2screen/"
		"castle_playroom_portal_cutout_reuse.png"
	)
	for record in prop_records:
		if str(record.get("path", "")) in required_portal_paths:
			check(record.get("source") == approved_portal_source,
				"physical portal does not reuse the approved castle portal",
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
		if isinstance(source_value, str) \
				and source_value.startswith("assets"):
			source_path = repo_path(
				source_value, f"{prop_path.name} source", failures)
			if source_path.is_file():
				check(sha256(source_path) == record.get("source_sha256"),
					f"approved source changed: {source_path.name}", failures)

	runtime_text = RUNTIME_SCRIPT.read_text(encoding="utf-8")
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
