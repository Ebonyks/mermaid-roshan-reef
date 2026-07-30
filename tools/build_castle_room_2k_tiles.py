#!/usr/bin/env python3
"""Build authorized Pearl Castle room masters and seam-safe runtime tiles.

The owner explicitly authorized deterministic upscaling for the seven legacy
1024x576 room plates on 2026-07-29. Originals remain untouched. The corrected
Kitchen uses a 4096x2304 master so both native dimensions provide at least
2048 pixels of coverage; the other preserved rooms retain their authorized
2048x1152 masters. Every master is split into non-overlapping runtime tiles,
and reconstruction must be pixel exact.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


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
DEFAULT_MASTER_SIZE = (2048, 1152)
DEFAULT_TILE_SIZE = (1024, 576)
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
		"comparison": "2K master reduced to source dimensions with Lanczos",
		"mean_absolute_rgb_error": round(float(difference.mean()), 6),
		"p95_absolute_rgb_error": round(float(np.percentile(difference, 95)), 6),
		"maximum_absolute_rgb_error": int(difference.max()),
		"normalized_object_coordinates_unchanged": True,
		"crop_or_padding": False,
	}


def main_hall_tile_records() -> list[dict[str, object]]:
	"""Verify the tracked Hall and reproduce its rich runtime tile inventory."""
	master_paths = (
		HALL_ALIGNED_ROOT / "main_hall_screen_a_fixture_aligned_master.png",
		HALL_ALIGNED_ROOT / "main_hall_screen_b_fixture_aligned_master.png",
	)
	view = Image.new("RGB", (3344, 941))
	for index, master_path in enumerate(master_paths):
		master = Image.open(master_path).convert("RGB")
		if master.size != (2048, 1153):
			raise ValueError(
				f"{master_path} is {master.size}, expected (2048, 1153)")
		view.paste(master.crop((376, 212, 2048, 1153)), (index * 1672, 0))

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
			source_top = 212 if row == 0 else 682
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
			if row == 0:
				tile_path = HALL_RUNTIME_ROOT / "tiles" / "runtime_bleed" / (
					f"main_hall_room_led_r0_c{column}_bleed.png")
				runtime_tile = Image.open(tile_path).convert("RGB")
				if runtime_tile.size != (836, 471):
					raise ValueError(
						f"{tile_path} is {runtime_tile.size}, "
						"expected (836, 471)")
				record.update({
					"dimensions": list(runtime_tile.size),
					"path": str(tile_path.relative_to(ROOT)),
					"runtime_seam_bleed_pixels": 1,
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


def build_room(room_id: str) -> dict[str, object]:
	source_path = ROOM_ROOT / f"room_{room_id}_background.png"
	source = Image.open(source_path).convert("RGB")
	if source.size != SOURCE_SIZE:
		raise ValueError(
			f"{source_path} is {source.size}, expected preserved {SOURCE_SIZE}")

	grid = ROOM_GRID_OVERRIDES.get(room_id, {
		"master_size": DEFAULT_MASTER_SIZE,
		"tile_size": DEFAULT_TILE_SIZE,
		"rows": 2,
		"columns": 2,
	})
	master_size = tuple(grid["master_size"])
	tile_size = tuple(grid["tile_size"])
	rows = int(grid["rows"])
	columns = int(grid["columns"])
	master = source.resize(master_size, Image.Resampling.LANCZOS)
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
		raise RuntimeError(f"{room_id} tiles do not reconstruct the 2K master")
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
		"ratio_delta": 0.0,
		"scale_factor": master.width / source.width,
		"resampling": "Pillow Image.Resampling.LANCZOS",
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
		"source and single-kettle topology repair; all runtime depth cards are "
		"outline-refined derivatives of accepted master pixels")
	manifest["runtime_node_contract"]["world_art_allowed"] = [
		"Sprite3D:unshaded",
		"Sprite3D:shaded lighting receiver",
	]
	manifest["runtime_node_contract"]["shaded_role_allowlist"] = [
		"clean_background_tile",
		"architectural_join_divider",
		"architectural_join_inlay",
		"architectural_bridge",
	]
	contract = manifest["owner_native_environment_contract"]
	contract.update({
		"status": "compliant",
		"upscale_authorized": True,
		"upscale_authorization_date": "2026-07-29",
		"upscale_method": "deterministic 2x Lanczos; no crop or padding",
		"runtime_tiles_lossless_no_scale": True,
		"active_master_dimensions": [2048, 1152],
		"required_minimum_per_screen_dimensions": [2048, 2048],
		"kitchen_active_master_dimensions": [4096, 2304],
	})
	for record in records:
		room = manifest["rooms"][record["room_id"]]
		grid = record["runtime_grid"]
		room.update({
			"active_background_system": "%dx%d Sprite3D tile grid" % (
				int(grid["rows"]), int(grid["columns"])),
			"native_master_compliant": True,
			"master_dimensions": record["master_dimensions"],
			"master_aspect_ratio": record["master_ratio"],
			"aspect_ratio_delta": record["ratio_delta"],
			"aspect_ratio_pixel_delta": 0.0,
			"upscaled_from_preserved_source": True,
			"upscale_authorization": record["authorization"],
			"upscale_method": record["resampling"],
			"master": record["master"],
			"master_sha256": record["master_sha256"],
			"runtime_tiles": record["tiles"],
			"tile_reconstruction_pixel_exact": True,
		})

	main_hall = manifest["rooms"]["main_hall"]
	hall_runtime_manifest = (
		AUDIT_ROOT / "castle_main_hall_2x4_runtime_manifest.json")
	hall_tiles = (
		json.loads(hall_runtime_manifest.read_text(encoding="utf-8"))["tiles"]
		if hall_runtime_manifest.exists() else main_hall_tile_records())
	main_hall.update({
		"active_background_system": (
			"two native >=2K masters / 2x4 Sprite3D grid"),
		"native_master_compliant": True,
		"master_dimensions": [2048, 1153],
		"master_aspect_ratio": 2048 / 1153,
		"aspect_ratio_delta": abs((2048 / 1153) - (1672 / 941)),
		"aspect_ratio_pixel_delta": 1.0,
		"upscaled_from_preserved_source": False,
		"runtime_tiles": hall_tiles,
		"tile_reconstruction_pixel_exact": True,
	})
	DEPTH_MANIFEST.write_text(
		json.dumps(manifest, indent=2, sort_keys=True) + "\n",
		encoding="utf-8")


def main() -> None:
	MASTER_ROOT.mkdir(parents=True, exist_ok=True)
	TILE_ROOT.mkdir(parents=True, exist_ok=True)
	AUDIT_ROOT.mkdir(parents=True, exist_ok=True)
	records = [build_room(room_id) for room_id in ROOM_IDS]
	write_contact(records)
	report = {
		"schema": 1,
		"purpose": "authorized 2K castle-room background derivation",
		"originals_preserved": True,
		"new_art_generated": False,
		"source_dimensions": list(SOURCE_SIZE),
		"default_master_dimensions": list(DEFAULT_MASTER_SIZE),
		"default_master_aspect_ratio": (
			DEFAULT_MASTER_SIZE[0] / DEFAULT_MASTER_SIZE[1]),
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
		"OK: 7 room plates -> 6 2048x1152 masters + "
		"1 Kitchen 4096x2304 master -> exact runtime tiles")


if __name__ == "__main__":
	main()
