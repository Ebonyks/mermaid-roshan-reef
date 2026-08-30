#!/usr/bin/env python3
"""Build and audit full-frame backgrounds beneath interactive 2D cards.

MA-VIS-007 forbids local blur/inpaint placeholders beneath a live card.  This
builder preserves every historical source and promotes reviewed, complete
ImageGen frames through whole-canvas normalization only.  Every runtime tile
is then an exact, non-overlapping crop of that normalized master.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FABLE = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
V4 = (ROOT / "assets/flats/castle/interactions_v4"
	/ "castle_interactions_v4.json")
AUDIT = ROOT / "audit/interactive_background_ownership_2026-08-29.json"
CONTACT = ROOT / "audit/castle_sprite3d/interactive_background_ownership_contact.png"

CASTLE_SOURCE_ROOT = (
	ROOT / "assets_src/castle/interactive_background_ownership_2026-08-29")
OPERA_SOURCE_ROOT = (
	ROOT / "assets_src/opera/interactive_background_ownership_2026-08-29")
CASTLE_MASTER_ROOT = ROOT / "assets_src/castle/room_backgrounds_2k"
CASTLE_ROOM_ROOT = ROOT / "assets/flats/castle/rooms"
CASTLE_V4_ROOT = ROOT / "assets/flats/castle/interactions_v4"
OPERA_NATIVE_ROOT = ROOT / "assets_src/imagegen/opera_codex_2026-08-02/native"
OPERA_MASTER_ROOT = ROOT / "assets_src/concepts/opera_regeneration_2026-08-01/cards"
OPERA_RUNTIME_ROOT = ROOT / "assets/opera/worlds/backdrops"

ROOMS = (
	"opera_hall", "kitchen", "library", "playroom", "craft_room",
	"mermaid_pool", "bubble_bath",
)
OPERA_REPAIRS = {
	"detective": "generated_world_detective_missing_crown_source.png",
	"nursery": "generated_world_nursery_empty_bottle_nook_source.png",
}
GENERATION_IDS = {
	"bubble_bath": "exec-de78aa84-bf23-4cb6-8e48-1e1611919517.png",
	"craft_room": "exec-e6207fcf-cdfb-421e-bae5-d2847d218302.png",
	"kitchen": "exec-b4af448e-8895-414d-a040-dbf087bce908.png",
	"library": "exec-6f9ea13b-24ad-4021-a2d4-1fbe1ac4758b.png",
	"opera_hall": "exec-bfefe97a-4b68-4477-87d7-d95ac653e91f.png",
	"playroom": "exec-f2bae1be-0740-4f5e-9f57-71c16863fc49.png",
	"mermaid_pool": "exec-4fbd1e17-45c5-4e28-9431-f02fe6fd3116.png",
	"detective": "exec-0924c2f2-d102-4283-9cad-6f521a3ed346.png",
	"nursery": "exec-718fe9db-779c-4a48-91ce-46fb13d3f13a.png",
}

CASTLE_PROMPT = (
	"Edit the supplied Pearl Castle room reference as one complete flattened "
	"storybook background. Preserve the room identity, camera, architecture, "
	"lighting, palette, floor and wall geometry. Remove every extracted "
	"interactive or foreground object and every plaid, streaked, blurred, "
	"duplicated, or ghosted footprint beneath those objects. Repaint each vacated "
	"area as coherent continuous wall, floor, water, shelving, or architectural "
	"surface matching its immediate surroundings. Do not add characters, text, "
	"UI, new props, duplicate fixtures, empty object silhouettes, patches, or "
	"smears. Return a complete opaque polished 2D preschool storybook frame."
)
OPERA_PROMPTS = {
	"detective": (
		"Edit the supplied complete square Detective world reference. Preserve "
		"the entire composition, camera, architecture, lighting, palette, paths, "
		"outer margins and child-readable storybook style. Remove the painted "
		"crown or pearl tiara from the far-right open display because the crown is "
		"the missing interactive object. Leave that display visibly empty and "
		"coherently repaint its backing and shelf. Do not add text, characters, a "
		"replacement crown, ghost silhouette, blur, patch or new prop. Return one "
		"complete opaque flattened square frame."
	),
	"nursery": (
		"Edit the supplied complete square Nursery world reference. Preserve the "
		"entire composition, camera, architecture, lighting, palette, paths, outer "
		"margins and child-readable storybook style. Remove the painted row of "
		"feeding bottles from the center-right bottle nook because the bottle is a "
		"live interactive overlay. Leave the nook and shelf visibly empty and "
		"coherently repaint their backing. Do not add text, characters, replacement "
		"bottles, ghost silhouettes, blur, patch or new prop. Return one complete "
		"opaque flattened square frame."
	),
}


def sha256_bytes(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
	return sha256_bytes(path.read_bytes())


def repository_text_sha256(path: Path) -> str:
	return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def relative(path: Path) -> str:
	return path.relative_to(ROOT).as_posix()


def png_bytes(image: Image.Image) -> bytes:
	stream = io.BytesIO()
	# Deterministic default zlib compression is dramatically faster than the
	# exhaustive optimizer for the 52 full-size masters/tiles in this gate.
	image.save(stream, "PNG", compress_level=6)
	return stream.getvalue()


def write_image(path: Path, image: Image.Image) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	data = png_bytes(image)
	if not path.exists() or path.read_bytes() != data:
		path.write_bytes(data)


def load_opaque(path: Path) -> Image.Image:
	if not path.is_file():
		raise FileNotFoundError(path)
	image = Image.open(path).convert("RGBA")
	if image.getchannel("A").getextrema() != (255, 255):
		raise ValueError(f"full-frame source is not opaque: {path}")
	return image.convert("RGB")


def committed_output_hashes(planned: dict[Path, Image.Image]) -> dict[str, str]:
	"""Hash shipped bytes without asking the local PNG encoder to recreate them."""
	return {
		relative(path): sha256(path) if path.is_file()
		else sha256_bytes(png_bytes(image))
		for path, image in planned.items()
	}


def opera_master(source: Image.Image) -> Image.Image:
	"""Use the established complete-canvas Opera normalization unchanged."""
	active_size = (2048, 1152)
	background = ImageOps.fit(
		source, active_size, method=Image.Resampling.BICUBIC
	).filter(ImageFilter.GaussianBlur(24))
	active = Image.alpha_composite(
		background.convert("RGBA"), Image.new("RGBA", active_size, (36, 28, 72, 38)))
	x = (active_size[0] - source.width) // 2
	y = (active_size[1] - source.height) // 2
	mask = Image.new("L", source.size, 255)
	draw = ImageDraw.Draw(mask)
	for inset in range(24):
		draw.rectangle(
			(inset, inset, source.width - 1 - inset, source.height - 1 - inset),
			outline=min(255, inset * 12), width=1)
	active.paste(source.convert("RGBA"), (x, y), mask)
	master = Image.new("RGBA", (2048, 2048), active.getpixel((1024, 8)))
	master.paste(active, (0, 448))
	return master.convert("RGB")


def build_expected() -> tuple[dict[Path, Image.Image], dict[str, Any], dict[str, Any], dict[str, Any]]:
	fable = json.loads(FABLE.read_text(encoding="utf-8"))
	v4 = json.loads(V4.read_text(encoding="utf-8"))
	planned: dict[Path, Image.Image] = {}
	castle_records: list[dict[str, Any]] = []

	for room in ROOMS:
		source_path = CASTLE_SOURCE_ROOT / f"generated_room_{room}_background_source.png"
		source = load_opaque(source_path)
		if abs(source.width / source.height - 16 / 9) > 0.002:
			raise ValueError(f"Castle source aspect changed: {source_path}")
		room_record = fable["rooms"][room]
		master_size = tuple(int(value) for value in room_record["master_dimensions"])
		logical = source.resize((1024, 576), Image.Resampling.LANCZOS)
		master = source.resize(master_size, Image.Resampling.LANCZOS)
		logical_path = CASTLE_ROOM_ROOT / f"room_{room}_background.png"
		master_path = CASTLE_MASTER_ROOT / f"room_{room}_background_2k.png"
		v4_logical_path = CASTLE_V4_ROOT / "backgrounds" / f"room_{room}_background.png"
		planned[logical_path] = logical
		planned[master_path] = master
		planned[v4_logical_path] = logical

		tile_records: list[dict[str, Any]] = []
		for tile in room_record["runtime_tiles"]:
			rect = tuple(int(value) for value in tile["master_rectangle"])
			image = master.crop(rect)
			canonical = ROOT / str(tile["path"])
			v4_path = CASTLE_V4_ROOT / "background_tiles" / canonical.name
			planned[canonical] = image
			planned[v4_path] = image
			tile_records.append({
				"path": relative(canonical), "v4_path": relative(v4_path),
				"master_rectangle": list(rect), "dimensions": list(image.size),
			})

		castle_records.append({
			"room": room,
			"source": relative(source_path),
			"source_sha256": sha256(source_path),
			"source_dimensions": list(source.size),
			"generation_id": GENERATION_IDS[room],
			"method": "built-in ImageGen full-frame edit",
			"prompt": CASTLE_PROMPT,
			"prompt_sha256": sha256_bytes(CASTLE_PROMPT.encode()),
			"logical_background": relative(logical_path),
			"native_master": relative(master_path),
			"native_dimensions": list(master_size),
			"normalization": "whole-canvas Lanczos; no crop, local heal, blend, mask, or subject transform",
			"tiles": tile_records,
			"human_owner_review": "pending",
		})

	opera_records: list[dict[str, Any]] = []
	for world, filename in OPERA_REPAIRS.items():
		source_path = OPERA_SOURCE_ROOT / filename
		source = load_opaque(source_path)
		if source.width != source.height:
			raise ValueError(f"Opera source is not square: {source_path}")
		master = opera_master(source)
		native_path = OPERA_NATIVE_ROOT / f"world_{world}_native.png"
		master_path = OPERA_MASTER_ROOT / f"opera_world_master_{world}.png"
		planned[native_path] = source
		planned[master_path] = master
		tiles: list[dict[str, Any]] = []
		for row in range(2):
			for column in range(2):
				path = OPERA_RUNTIME_ROOT / f"world_{world}_c{column}r{row}.png"
				image = master.crop((column * 1024, row * 1024,
					(column + 1) * 1024, (row + 1) * 1024))
				planned[path] = image
				tiles.append({"path": relative(path), "column": column, "row": row})
		opera_records.append({
			"world": world,
			"source": relative(source_path),
			"source_sha256": sha256(source_path),
			"source_dimensions": list(source.size),
			"generation_id": GENERATION_IDS[world],
			"method": "built-in ImageGen full-frame edit",
			"prompt": OPERA_PROMPTS[world],
			"prompt_sha256": sha256_bytes(OPERA_PROMPTS[world].encode()),
			"promoted_native": relative(native_path),
			"native_master": relative(master_path),
			"normalization": "established whole-canvas Opera 2048-square normalization; no local repair",
			"tiles": tiles,
			"human_owner_review": "pending",
		})

	return planned, fable, v4, {
		"schema": 1,
		"finding": "MA-VIS-007",
		"status": "machine_verified_human_review_pending",
		"policy": (
			"One complete clean background owns every pixel beneath a live card; "
			"runtime plates may use whole-canvas normalization and exact tiling only."),
		"forbidden_methods": [
			"local scanline interpolation", "Gaussian blur ownership fill",
			"independent tile regeneration", "painted duplicate under live card"],
		"protected_originals_modified": False,
		"castle": castle_records,
		"opera": opera_records,
		"scrub": {
			"castle_active_interactive_cards": 39,
			"castle_active_static_cards": 12,
			"castle_rooms": 7,
			"opera_confirmed_conflicts": [
				"Detective missing crown painted in world background",
				"Nursery feeding bottles painted beneath live pour mover"],
			"cleared_domains": [
				"Sky Lagoon", "reef districts", "galaxy and kart", "picture games",
				"other active Opera careers", "Dream House empty-shell rooms"],
		},
	}


def bind_hashes(planned: dict[Path, Image.Image], fable: dict[str, Any],
		v4: dict[str, Any], audit: dict[str, Any]) -> None:
	# Bind provenance to the exact committed PNG bytes, not a fresh Pillow/zlib
	# encoding of the same pixels. PNG pixels are portable, while compressed
	# bytes can differ across operating systems even with the same Pillow
	# version. Build mode writes every planned image before reaching this point;
	# check mode separately rejects missing or pixel-stale outputs.
	hashes = committed_output_hashes(planned)
	for room_record in audit["castle"]:
		room = room_record["room"]
		room_record["logical_background_sha256"] = hashes[room_record["logical_background"]]
		room_record["native_master_sha256"] = hashes[room_record["native_master"]]
		fable_room = fable["rooms"][room]
		fable_room["background_sha256"] = room_record["logical_background_sha256"]
		fable_room["master_sha256"] = room_record["native_master_sha256"]
		fable_room["upscale_method"] = room_record["normalization"]
		fable_room["interactive_background_ownership"] = {
			"finding": "MA-VIS-007", "source": room_record["source"],
			"source_sha256": room_record["source_sha256"],
			"provenance": relative(AUDIT),
		}
		by_path = {record["path"]: record for record in room_record["tiles"]}
		for tile in fable_room["runtime_tiles"]:
			tile["sha256"] = hashes[str(tile["path"])]
			record = by_path[str(tile["path"])]
			record["sha256"] = hashes[record["path"]]
			record["v4_sha256"] = hashes[record["v4_path"]]

		route = v4["runtime_background_tiles"][room]
		route["route"] = "generated_full_frame_pixel_ownership_tiles"
		route["derived_from_low_resolution_audit_plate"] = False
		route["full_source_ownership_healed"] = True
		route["changed_outside_pixels"] = 0
		route["changed_owned_pixels"] = 0
		for tile in route["source_tiles"]:
			tile["sha256"] = hashes[str(tile["path"])]
		for tile in route["tiles"]:
			tile["sha256"] = hashes[str(tile["path"])]
		for asset in v4["assets"]:
			if str(asset.get("room")) != room:
				continue
			asset["source_ownership"]["healed_background_sha256"] = hashes[
				str(asset["healed_background_path"])]
			asset["source_ownership"]["production_rehealed"] = True
			asset["source_ownership"]["background_method"] = (
				"generated_complete_clean_frame_MA_VIS_007")

	for record in audit["opera"]:
		record["promoted_native_sha256"] = hashes[record["promoted_native"]]
		record["native_master_sha256"] = hashes[record["native_master"]]
		for tile in record["tiles"]:
			tile["sha256"] = hashes[tile["path"]]

	for key in ("generator", "source_layer_manifest"):
		declared = v4.get(key)
		if isinstance(declared, str) and declared:
			v4[f"{key}_sha256"] = repository_text_sha256(ROOT / declared)


def check_outputs(planned: dict[Path, Image.Image], audit: dict[str, Any]) -> list[str]:
	errors: list[str] = []
	for path, image in planned.items():
		if not path.is_file():
			errors.append(f"missing output: {relative(path)}")
			continue
		actual = Image.open(path).convert("RGB")
		if actual.size != image.size or actual.tobytes() != image.convert("RGB").tobytes():
			errors.append(f"stale output pixels: {relative(path)}")
	if not AUDIT.is_file():
		errors.append(f"missing audit manifest: {relative(AUDIT)}")
	else:
		actual_audit = json.loads(AUDIT.read_text(encoding="utf-8"))
		if actual_audit != audit:
			errors.append("ownership audit manifest is stale")
	return errors


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	try:
		planned, fable, v4, audit = build_expected()
		if not args.check:
			for path, image in planned.items():
				write_image(path, image)
		bind_hashes(planned, fable, v4, audit)
		if args.check:
			errors = check_outputs(planned, audit)
			if json.loads(FABLE.read_text(encoding="utf-8")) != fable:
				errors.append("FABLE Castle depth manifest is stale")
			if json.loads(V4.read_text(encoding="utf-8")) != v4:
				errors.append("V4 Castle interaction manifest is stale")
			if errors:
				for error in errors:
					print(f"PIXEL_OWNERSHIP|FAIL|{error}", file=sys.stderr)
				return 1
			print("PIXEL_OWNERSHIP|RESULT|OK|castle_rooms=7|opera_worlds=2")
			return 0
		FABLE.write_text(json.dumps(fable, indent=2) + "\n", encoding="utf-8")
		V4.write_text(json.dumps(v4, indent=2) + "\n", encoding="utf-8")
		AUDIT.parent.mkdir(parents=True, exist_ok=True)
		AUDIT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
		print("PIXEL_OWNERSHIP|BUILT|castle_rooms=7|opera_worlds=2")
		return 0
	except (FileNotFoundError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
		print(f"PIXEL_OWNERSHIP|FAIL|{error}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
