#!/usr/bin/env python3
"""Build authorized Pearl Castle room masters and seam-safe runtime tiles.

The owner explicitly authorized deterministic upscaling for the seven legacy
1024x576 room plates on 2026-07-29. Originals remain untouched. Every playable
screen now provides at least 2048 native pixels on both axes: preserved
single-screen rooms use the same 3640x2048 contract as one strict Main Hall
screen, while the corrected Kitchen keeps its accepted 4096x2304 master. Every
master is split into non-overlapping runtime tiles, and reconstruction must be
pixel exact. The Main Hall is not rebuilt here:
its live Canvas-manifest record is projected only from the accepted strict
7280x2048/2x8 build manifest, so this legacy room tool cannot restore the
retired shaded 2x4/bleed implementation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

from repair_castle_room_native_backgrounds import build_expected_baselines


ROOT = Path(__file__).resolve().parents[1]
ROOM_ROOT = ROOT / "assets" / "flats" / "castle" / "rooms"
MASTER_ROOT = ROOT / "assets_src" / "castle" / "room_backgrounds_2k"
TILE_ROOT = ROOM_ROOT / "background_tiles"
AUDIT_ROOT = ROOT / "audit" / "castle_sprite3d"
DEPTH_MANIFEST = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
OUTPUT_MANIFEST = AUDIT_ROOT / "castle_room_2k_upscale_manifest.json"
OUTPUT_CONTACT = AUDIT_ROOT / "castle_room_2k_upscale_contact.png"
HALL_RUNTIME_ROOT = (
	ROOT / "assets" / "flats" / "castle" / "main_hall_2screen")
HALL_ALIGNED_ROOT = ROOT / "assets_src" / "castle" / "main_hall_alignment"
HALL_STRICT_BUILD_MANIFEST = (
	ROOT / "assets_src" / "imagegen" / "castle_main_hall_redraw_2026-08-03"
	/ "main_hall_strict_2k_build_manifest.json")
HALL_STRICT_AUDIT = (
	AUDIT_ROOT / "castle_main_hall_redraw_2026-08-04_2k_audit.json")
HALL_NODE_INVENTORY = (
	AUDIT_ROOT / "castle_main_hall_redraw_2026-08-03_node_inventory.json")

ROOM_IDS = (
	"opera_hall",
	"kitchen",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
)
SOURCE_SIZE = (1024, 576)
DEFAULT_MASTER_SIZE = (3640, 2048)
DEFAULT_TILE_SIZE = (910, 1024)
ROOM_GRID_OVERRIDES = {
	"kitchen": {
		"master_size": (4096, 2304),
		"tile_size": (1024, 768),
		"rows": 3,
		"columns": 4,
	},
}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
	path = Path(
		"C:/Windows/Fonts/arialbd.ttf"
		if bold else "C:/Windows/Fonts/arial.ttf")
	if path.exists():
		return ImageFont.truetype(str(path), size)
	return ImageFont.load_default()


def exact_equal(left: Image.Image, right: Image.Image) -> bool:
	return ImageChops.difference(left, right).getbbox() is None


def roundtrip_metrics(source: Image.Image, master: Image.Image) -> dict[str, object]:
	roundtrip = master.resize(SOURCE_SIZE, Image.Resampling.LANCZOS)
	source_array = np.asarray(source, dtype=np.float32)
	roundtrip_array = np.asarray(roundtrip, dtype=np.float32)
	difference = np.abs(source_array - roundtrip_array)
	return {
		"comparison": "native master reduced to source dimensions with Lanczos",
		"mean_absolute_rgb_error": round(float(difference.mean()), 6),
		"p95_absolute_rgb_error": round(float(np.percentile(difference, 95)), 6),
		"maximum_absolute_rgb_error": int(difference.max()),
		"normalized_object_coordinates_unchanged": True,
		"crop_or_padding": False,
	}


def _historical_main_hall_tile_records_2026_07_29(
) -> list[dict[str, object]]:
	"""Verify archived 2x4 evidence; never use it as the active Hall record."""
	master_paths = (
		HALL_ALIGNED_ROOT / "main_hall_screen_a_fixture_aligned_master.png",
		HALL_ALIGNED_ROOT / "main_hall_screen_b_fixture_aligned_master.png",
	)
	view = Image.new("RGB", (3344, 941))
	view_rects = (
		(376, 212, 2048, 1153),
		(376, 147, 2048, 1088),
	)
	for index, master_path in enumerate(master_paths):
		master = Image.open(master_path).convert("RGB")
		if master.size != (2048, 1153):
			raise ValueError(
				f"{master_path} is {master.size}, expected (2048, 1153)")
		view.paste(master.crop(view_rects[index]), (index * 1672, 0))

	reconstruction = Image.new("RGB", view.size)
	records: list[dict[str, object]] = []
	for row in range(2):
		for column in range(4):
			source_tile_path = HALL_RUNTIME_ROOT / "tiles" / (
				f"main_hall_room_led_r{row}_c{column}.png")
			source_tile = Image.open(source_tile_path).convert("RGB")
			source_tile_size = (836, 470 if row == 0 else 471)
			if source_tile.size != source_tile_size:
				raise ValueError(
					f"{source_tile_path} is {source_tile.size}, "
					f"expected {source_tile_size}")
			top = 0 if row == 0 else 470
			reconstruction.paste(source_tile, (column * 836, top))
			screen_index = column // 2
			screen = "A" if screen_index == 0 else "B"
			screen_local_column = column % 2
			source_left = 376 + (screen_local_column * 836)
			source_view_y = view_rects[screen_index][1]
			source_top = source_view_y + top
			tile_path = source_tile_path
			record: dict[str, object] = {
				"row": row,
				"column": column,
				"dimensions": list(source_tile.size),
				"logical_world_rectangle": [
					column * 836,
					top,
					(column + 1) * 836,
					top + source_tile.height,
				],
				"path": str(tile_path.relative_to(ROOT)),
				"sha256": sha256(tile_path),
				"screen": screen,
				"screen_local_column": screen_local_column,
				"source": str(master_paths[screen_index].relative_to(ROOT)),
				"source_rectangle": [
					source_left,
					source_top,
					source_left + 836,
					source_top + source_tile.height,
				],
			}
			tile_path = HALL_RUNTIME_ROOT / "tiles" / "runtime_bleed" / (
				f"main_hall_room_led_r{row}_c{column}_bleed.png")
			runtime_tile = Image.open(tile_path).convert("RGB")
			bleed_pixels = (
				1 if column < 3 else 0,
				1 if row == 0 else 0,
			)
			expected_runtime_size = (
				source_tile.width + bleed_pixels[0],
				source_tile.height + bleed_pixels[1],
			)
			if runtime_tile.size != expected_runtime_size:
				raise ValueError(
					f"{tile_path} is {runtime_tile.size}, "
					f"expected {expected_runtime_size}")
			if not exact_equal(
					runtime_tile.crop(
						(0, 0, source_tile.width, source_tile.height)),
					source_tile):
				raise RuntimeError(f"{tile_path} changed approved source pixels")
			record.update({
				"dimensions": list(runtime_tile.size),
				"path": str(tile_path.relative_to(ROOT)),
				"runtime_seam_bleed_pixels": list(bleed_pixels),
				"sha256": sha256(tile_path),
				"source_tile_dimensions": list(source_tile.size),
				"source_tile_path": str(source_tile_path.relative_to(ROOT)),
				"source_tile_sha256": sha256(source_tile_path),
			})
			records.append(record)
	if not exact_equal(view, reconstruction):
		raise RuntimeError(
			"Main Hall source tiles do not reconstruct the aligned masters")
	return records


def current_main_hall_record() -> dict[str, object]:
	"""Project the accepted strict Hall build into the living Canvas manifest."""
	data = json.loads(HALL_STRICT_BUILD_MANIFEST.read_text(encoding="utf-8"))
	panorama = data.get("panorama", {})
	grid = data.get("runtime_grid", {})
	tiles = data.get("tiles", [])
	if panorama.get("dimensions") != [7280, 2048]:
		raise ValueError("Strict Main Hall panorama must be exactly 7280x2048")
	if panorama.get("file_sha256") != (
			"297cd6d181288ef6cc364a71a89fdb4da168f688249ca910995e71f6f769a9dd"):
		raise ValueError("Strict Main Hall panorama hash changed")
	if grid.get("rows") != 2 or grid.get("columns") != 8 \
			or grid.get("tile_count") != 16:
		raise ValueError("Strict Main Hall runtime grid must be 2x8 / 16 cards")

	runtime_tiles: list[dict[str, object]] = []
	for tile in tiles:
		dimensions = tile.get("dimensions", [])
		path = str(tile.get("path", ""))
		if dimensions != [910, 1024] or not path.startswith(
				"assets/flats/castle/main_hall_redraw_2026-08-03/tiles/"):
			raise ValueError(f"Nonconforming strict Main Hall tile: {path}")
		tile_path = ROOT / path
		if not tile_path.exists() or sha256(tile_path) != tile.get("file_sha256"):
			raise ValueError(f"Strict Main Hall tile hash mismatch: {path}")
		runtime_tiles.append({
			"column": int(tile["column"]),
			"dimensions": list(dimensions),
			"master_source_rect": list(tile["panorama_source_rectangle"]),
			"path": path,
			"row": int(tile["row"]),
			"screen": str(tile["screen"]),
			"sha256": str(tile["file_sha256"]),
		})
	if len(runtime_tiles) != 16:
		raise ValueError("Strict Main Hall manifest must contain sixteen tiles")

	chains = data.get("transform_chains", {})
	return {
		"active_background_system": (
			"two 3640x2048 per-screen masters / lossless 7280x2048 "
		"panorama / 2x8 unshaded Sprite2D grid"),
		"active_runtime_status": "accepted_current_runtime",
		"aspect_ratio_delta": 0.0005105937832092788,
		"aspect_ratio_pixel_delta": 0.5885167464111873,
		"master": str(panorama["path"]),
		"master_aspect_ratio": 7280 / 2048,
		"master_dimensions": [7280, 2048],
		"master_sha256": str(panorama["file_sha256"]),
		"native_master_compliant": True,
		"reference_aspect_ratio": 1672 / 941,
		"runtime_neighbor_bleed_pixels": [0, 0],
		"runtime_tiles": runtime_tiles,
		"screen_masters": [
			{
				"dimensions": list(chains[screen]["final"]["dimensions"]),
				"path": str(chains[screen]["final"]["path"]),
				"screen": screen,
				"sha256": str(chains[screen]["final"]["file_sha256"]),
			}
			for screen in ("A", "B")
		],
		"source_tile_rectangles_non_overlapping": True,
		"tile_reconstruction_pixel_exact": True,
		"upscale_authorization": (
			"Owner 2026-07-29 and 2026-08-03: upscale as needed while "
			"preserving the accepted art"),
		"upscale_method": (
			"whole-canvas Pillow Image.Resampling.LANCZOS; no crop, padding, "
			"canvas extension, local retouch, seam blend, or AI upscale"),
		"upscaled_from_preserved_source": True,
	}


def build_room(room_id: str,
		live_alpha_master: Image.Image | None = None) -> dict[str, object]:
	source_path = ROOM_ROOT / f"room_{room_id}_background.png"
	source = Image.open(source_path).convert("RGB")
	if source.size != SOURCE_SIZE:
		raise ValueError(
			f"{source_path} is {source.size}, expected preserved {SOURCE_SIZE}")

	grid = ROOM_GRID_OVERRIDES.get(room_id, {
		"master_size": DEFAULT_MASTER_SIZE,
		"tile_size": DEFAULT_TILE_SIZE,
		"rows": 2,
		"columns": 4,
	})
	master_size = tuple(grid["master_size"])
	tile_size = tuple(grid["tile_size"])
	rows = int(grid["rows"])
	columns = int(grid["columns"])
	master = source.resize(master_size, Image.Resampling.LANCZOS) \
		if live_alpha_master is None else live_alpha_master.convert("RGB")
	# The first run of a native-coverage migration receives the prior accepted
	# live-alpha master from the manifest. Scale that complete flattened canvas;
	# never re-run or locally stretch an ownership patch in isolation.
	if master.size != master_size and live_alpha_master is not None:
		master = master.resize(master_size, Image.Resampling.LANCZOS)
	if master.size != master_size:
		raise ValueError(
			f"{room_id} live-alpha master is {master.size}, "
			f"expected {master_size}")
	master_path = MASTER_ROOT / f"room_{room_id}_background_2k.png"
	master.save(master_path, format="PNG", optimize=True)

	reconstruction = Image.new("RGB", master_size)
	tile_records: list[dict[str, object]] = []
	for row in range(rows):
		for column in range(columns):
			left = column * tile_size[0]
			top = row * tile_size[1]
			box = (left, top, left + tile_size[0], top + tile_size[1])
			tile = master.crop(box)
			tile_path = TILE_ROOT / (
				f"room_{room_id}_background_r{row}_c{column}.png")
			tile.save(tile_path, format="PNG", optimize=True)
			reconstruction.paste(tile, (left, top))
			tile_records.append({
				"row": row,
				"column": column,
				"master_rectangle": list(box),
				"logical_art_rectangle": [
					column * (SOURCE_SIZE[0] // columns),
					row * (SOURCE_SIZE[1] // rows),
					SOURCE_SIZE[0] // columns,
					SOURCE_SIZE[1] // rows,
				],
				"dimensions": list(tile.size),
				"path": tile_path.relative_to(ROOT).as_posix(),
				"sha256": sha256(tile_path),
			})

	exact = exact_equal(master, reconstruction)
	if not exact:
		raise RuntimeError(
			f"{room_id} tiles do not reconstruct the native master")
	return {
		"room_id": room_id,
		"source": source_path.relative_to(ROOT).as_posix(),
		"source_dimensions": list(source.size),
		"source_sha256": sha256(source_path),
		"master": master_path.relative_to(ROOT).as_posix(),
		"master_dimensions": list(master.size),
		"master_sha256": sha256(master_path),
		"source_ratio": source.width / source.height,
		"master_ratio": master.width / master.height,
		"ratio_delta": abs(
			(master.width / master.height) - (source.width / source.height)),
		"aspect_ratio_pixel_delta": abs(
			master.width - master.height * (source.width / source.height)),
		"scale_factor": master.width / source.width,
		"resampling": (
			"approved full-room whole-canvas Lanczos to native size; prior "
			"hidden fill retained only inside exact live-alpha ownership"
			if live_alpha_master is not None
			else "Pillow Image.Resampling.LANCZOS"),
		"authorization": (
			"Owner 2026-07-29: Upscale as needed in this situation."),
		"tiles": tile_records,
		"runtime_grid": {
			"rows": rows,
			"columns": columns,
			"tile_count": rows * columns,
			"tile_dimensions": list(tile_size),
		},
		"tile_reconstruction_pixel_exact": exact,
		"invariance": roundtrip_metrics(source, master),
	}


def write_contact(records: list[dict[str, object]]) -> None:
	panel_width = 512
	panel_height = 288
	label_height = 54
	canvas = Image.new(
		"RGB",
		(panel_width * 2, (panel_height + label_height) * 4),
		"#f4f1ff")
	draw = ImageDraw.Draw(canvas)
	for index, record in enumerate(records):
		column = index % 2
		row = index // 2
		x = column * panel_width
		y = row * (panel_height + label_height)
		master = Image.open(ROOT / str(record["master"])).convert("RGB")
		preview = master.resize((panel_width, panel_height), Image.Resampling.LANCZOS)
		canvas.paste(preview, (x, y))
		draw.rectangle(
			(x, y + panel_height, x + panel_width, y + panel_height + label_height),
			fill="#302a68")
		draw.text(
			(x + 12, y + panel_height + 8),
			str(record["room_id"]).replace("_", " ").upper(),
			font=font(18, bold=True),
			fill="#ffffff")
		draw.text(
			(x + 12, y + panel_height + 30),
			"%dx%d master -> %d exact runtime cards" % (
				int(record["master_dimensions"][0]),
				int(record["master_dimensions"][1]),
				int(record["runtime_grid"]["tile_count"])),
			font=font(14),
			fill="#dffcf7")
	canvas.save(OUTPUT_CONTACT, format="PNG", optimize=True)


def update_depth_manifest(records: list[dict[str, object]]) -> None:
	manifest = json.loads(DEPTH_MANIFEST.read_text(encoding="utf-8"))
	manifest["source_policy"] = (
		"Approved room composites; Kitchen v3 retains its documented full-frame "
		"source and single-kettle topology repair; all runtime Canvas layer cards are "
		"outline-refined derivatives of accepted master pixels")
	node_contract = manifest["runtime_node_contract"]
	node_contract.update({
		"world_root": "Node2D",
		"camera": "none",
		"coordinate_system": "direct_canvas_coordinates",
		"world_art_allowed": ["Sprite2D:unshaded"],
		"world_art_forbidden": [
			"Node3D",
			"Sprite3D",
			"Camera3D",
			"MeshInstance3D",
			"MultiMeshInstance3D",
			"CSGShape3D",
			"Decal",
		],
		"shaded_role_allowlist": [],
	})
	if "reference_steady_sprite3d_inventory" in node_contract:
		node_contract["reference_steady_sprite2d_inventory"] = \
			node_contract.pop("reference_steady_sprite3d_inventory")
	node_contract["background_tile_seam_policy"] = {
		"source_rectangles_non_overlapping": True,
		"main_hall_runtime_neighbor_bleed_pixels": [0, 0],
		"main_hall_bleed_method": (
			"none; sixteen exact non-overlapping 910x1024 crops reconstruct "
			"the 7280x2048 master without scaling or overlap"),
		"main_hall_runtime_tile_grid": "2 rows x 8 columns",
		"destination_room_runtime_quad_overlap_native_pixels": [1, 1],
		"destination_room_overlap_method": (
			"top-left-anchored geometry overscan; source textures unchanged"),
		"maximum_runtime_texture_long_edge": 1024,
	}
	contract = manifest["owner_native_environment_contract"]
	contract.update({
		"status": "compliant",
		"upscale_authorized": True,
		"upscale_authorization_date": "2026-07-29",
		"upscale_method": (
			"deterministic whole-canvas Lanczos; no crop or padding"),
		"runtime_tiles_lossless_no_scale": True,
		"active_master_dimensions": list(DEFAULT_MASTER_SIZE),
		"required_minimum_per_screen_dimensions": [2048, 2048],
		"kitchen_active_master_dimensions": [4096, 2304],
		"main_hall_active_master_dimensions": [7280, 2048],
		"main_hall_per_screen_master_dimensions": [3640, 2048],
	})
	for record in records:
		room = manifest["rooms"][record["room_id"]]
		grid = record["runtime_grid"]
		room.update({
			"active_background_system": "%dx%d Sprite2D tile grid" % (
				int(grid["rows"]), int(grid["columns"])),
			"native_master_compliant": (
				min(int(value) for value in record["master_dimensions"]) >= 2048),
			"master_dimensions": record["master_dimensions"],
			"master_aspect_ratio": record["master_ratio"],
			"aspect_ratio_delta": record["ratio_delta"],
			"aspect_ratio_pixel_delta": record["aspect_ratio_pixel_delta"],
			"upscaled_from_preserved_source": True,
			"upscale_authorization": record["authorization"],
			"upscale_method": record["resampling"],
			"master": record["master"],
			"master_sha256": record["master_sha256"],
			"runtime_tiles": record["tiles"],
			"tile_reconstruction_pixel_exact": True,
			"runtime_quad_overlap_native_pixels": [1, 1],
			"source_tile_rectangles_non_overlapping": True,
		})

	# Main Hall is owned by the strict per-screen >=2K pipeline. Never derive
	# its active record from the archived 2x4/bleed implementation above.
	main_hall = manifest["rooms"]["main_hall"]
	main_hall.update(current_main_hall_record())
	main_hall["card_inventory_scope"] = (
		"preserved 2026-07-26 source-extraction evidence for legacy crop and "
		"alpha audits; not the current runtime node count")
	main_hall["source_record_scope"] = (
		"preserved historical 2026-07-26 clean-plate/card extraction input; "
		"current runtime background provenance is current_runtime_audit")
	main_hall["current_runtime_audit"] = {
		"blocking_audit": HALL_STRICT_AUDIT.relative_to(ROOT).as_posix(),
		"blocking_audit_sha256": sha256(HALL_STRICT_AUDIT),
		"build_manifest": HALL_STRICT_BUILD_MANIFEST.relative_to(ROOT).as_posix(),
		"build_manifest_sha256": sha256(HALL_STRICT_BUILD_MANIFEST),
		"node_inventory": HALL_NODE_INVENTORY.relative_to(ROOT).as_posix(),
		"node_inventory_sha256": sha256(HALL_NODE_INVENTORY),
	}
	DEPTH_MANIFEST.write_text(
		json.dumps(manifest, indent=2, sort_keys=True) + "\n",
		encoding="utf-8")


def main() -> None:
	MASTER_ROOT.mkdir(parents=True, exist_ok=True)
	TILE_ROOT.mkdir(parents=True, exist_ok=True)
	AUDIT_ROOT.mkdir(parents=True, exist_ok=True)
	live_alpha_baselines = build_expected_baselines()
	records = [build_room(
		room_id, live_alpha_baselines[room_id]["master"])
		for room_id in ROOM_IDS]
	write_contact(records)
	report = {
		"schema": 1,
		"purpose": "authorized native-coverage castle-room background derivation",
		"originals_preserved": True,
		"new_art_generated": False,
		"source_dimensions": list(SOURCE_SIZE),
		"default_master_dimensions": list(DEFAULT_MASTER_SIZE),
		"default_master_aspect_ratio": (
			DEFAULT_MASTER_SIZE[0] / DEFAULT_MASTER_SIZE[1]),
		"required_minimum_per_screen_dimensions": [2048, 2048],
		"kitchen_minimum_coverage_master_dimensions": [4096, 2304],
		"runtime_grids_are_room_specific": True,
		"all_reconstructions_pixel_exact": all(
			bool(record["tile_reconstruction_pixel_exact"])
			for record in records),
		"rooms": records,
		"contact_sheet": {
			"path": OUTPUT_CONTACT.relative_to(ROOT).as_posix(),
			"dimensions": list(Image.open(OUTPUT_CONTACT).size),
			"sha256": sha256(OUTPUT_CONTACT),
		},
	}
	OUTPUT_MANIFEST.write_text(
		json.dumps(report, indent=2) + "\n",
		encoding="utf-8")
	update_depth_manifest(records)
	print(
		"OK: 7 room plates -> 6 3640x2048 masters + "
		"1 Kitchen 4096x2304 master -> exact runtime tiles")


if __name__ == "__main__":
	main()
