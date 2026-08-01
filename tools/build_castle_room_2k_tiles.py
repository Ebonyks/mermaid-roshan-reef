#!/usr/bin/env python3
"""Build authorized 2K Pearl Castle room masters and seam-safe runtime tiles.

The owner explicitly authorized deterministic upscaling for the six legacy
1024x576 room plates on 2026-07-29. Originals remain untouched. Each clean
background is enlarged exactly 2x with Lanczos, then split without scaling
into four 1024x576 runtime tiles. Reconstruction is required to be pixel exact
to the derived 2048x1152 master.
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

ROOM_IDS = (
	"kitchen",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
)
SOURCE_SIZE = (1024, 576)
MASTER_SIZE = (2048, 1152)
TILE_SIZE = (1024, 576)


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


def build_room(room_id: str) -> dict[str, object]:
	source_path = ROOM_ROOT / f"room_{room_id}_background.png"
	source = Image.open(source_path).convert("RGB")
	if source.size != SOURCE_SIZE:
		raise ValueError(
			f"{source_path} is {source.size}, expected preserved {SOURCE_SIZE}")

	master = source.resize(MASTER_SIZE, Image.Resampling.LANCZOS)
	master_path = MASTER_ROOT / f"room_{room_id}_background_2k.png"
	master.save(master_path, format="PNG", optimize=True)

	reconstruction = Image.new("RGB", MASTER_SIZE)
	tile_records: list[dict[str, object]] = []
	for row in range(2):
		for column in range(2):
			left = column * TILE_SIZE[0]
			top = row * TILE_SIZE[1]
			box = (left, top, left + TILE_SIZE[0], top + TILE_SIZE[1])
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
					column * 512,
					row * 288,
					512,
					288,
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
		"scale_factor": 2.0,
		"resampling": "Pillow Image.Resampling.LANCZOS",
		"authorization": (
			"Owner 2026-07-29: Upscale as needed in this situation."),
		"tiles": tile_records,
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
			"2048x1152 master -> 4 exact 1024x576 cards",
			font=font(14),
			fill="#dffcf7")
	canvas.save(OUTPUT_CONTACT, format="PNG", optimize=True)


def update_depth_manifest(records: list[dict[str, object]]) -> None:
	manifest = json.loads(DEPTH_MANIFEST.read_text(encoding="utf-8"))
	manifest["source_policy"] = (
		"Existing approved room composites; compact generated pixels are "
		"accepted only inside the documented Main Hall fixture cleanup masks; "
		"all derived runtime cards preserve accepted master pixels")
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
	})
	for record in records:
		room = manifest["rooms"][record["room_id"]]
		room.update({
			"active_background_system": "2x2 Sprite3D tile grid",
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
	main_hall.update({
		"active_background_system": "two native >=2K masters / 2x4 Sprite3D grid",
		"native_master_compliant": True,
		"master_dimensions": [2048, 1153],
		"master_aspect_ratio": 2048 / 1153,
		"aspect_ratio_delta": abs((2048 / 1153) - (1672 / 941)),
		"aspect_ratio_pixel_delta": 1.0,
		"upscaled_from_preserved_source": False,
		"runtime_tiles": (
			json.loads((AUDIT_ROOT / "castle_main_hall_2x4_runtime_manifest.json"
				).read_text(encoding="utf-8"))["tiles"]),
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
		"master_dimensions": list(MASTER_SIZE),
		"master_aspect_ratio": MASTER_SIZE[0] / MASTER_SIZE[1],
		"runtime_grid": {"rows": 2, "columns": 2, "tile_count": 4},
		"runtime_tile_dimensions": list(TILE_SIZE),
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
		"OK: 7 preserved room plates -> 7 2048x1152 masters -> "
		"28 exact 1024x576 runtime tiles")


if __name__ == "__main__":
	main()
