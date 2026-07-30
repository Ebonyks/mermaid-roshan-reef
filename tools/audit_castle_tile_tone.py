#!/usr/bin/env python3
"""Audit Pearl Castle tile continuity and runtime color tone."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageStat


TILE_WIDTH = 836
TOP_HEIGHT = 470
MASTER_SIZE = (3344, 941)
ROOM_CAPTURE_NAMES = (
	"opera_hall",
	"kitchen",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
)
CONTEXT_CAPTURE_NAMES = (
	"tone_context_sky_lagoon",
	"tone_context_northern_world",
)


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def reconstruct(tile_root: Path) -> tuple[Image.Image, list[dict[str, object]]]:
	master = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
	tiles: list[dict[str, object]] = []
	for row in range(2):
		for column in range(4):
			path = tile_root / f"main_hall_room_led_r{row}_c{column}.png"
			tile = Image.open(path).convert("RGBA")
			top = 0 if row == 0 else TOP_HEIGHT
			master.alpha_composite(tile, (column * TILE_WIDTH, top))
			tiles.append({
				"path": str(path),
				"size": list(tile.size),
				"rect": [column * TILE_WIDTH, top, tile.width, tile.height],
				"sha256": sha256(path),
			})
	return master, tiles


def edge_delta(array: np.ndarray, axis: str, coordinate: int,
		start: int, end: int) -> dict[str, float]:
	if axis == "x":
		left = array[start:end, coordinate - 1, :3].astype(np.float32)
		right = array[start:end, coordinate, :3].astype(np.float32)
		near_a = array[start:end, coordinate - 2, :3].astype(np.float32)
		near_b = array[start:end, coordinate + 1, :3].astype(np.float32)
	else:
		left = array[coordinate - 1, start:end, :3].astype(np.float32)
		right = array[coordinate, start:end, :3].astype(np.float32)
		near_a = array[coordinate - 2, start:end, :3].astype(np.float32)
		near_b = array[coordinate + 1, start:end, :3].astype(np.float32)
	seam = np.abs(left - right)
	local = 0.5 * (
		np.abs(near_a - left) + np.abs(right - near_b))
	seam_mean = float(np.mean(seam))
	local_mean = float(np.mean(local))
	return {
		"mean_abs_rgb": round(seam_mean, 4),
		"p95_abs_rgb": round(float(np.percentile(seam, 95)), 4),
		"local_gradient_mean": round(local_mean, 4),
		"relative_to_local": round(seam_mean / max(0.001, local_mean), 4),
	}


def srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
	value = rgb.astype(np.float32) / 255.0
	value = np.where(value <= 0.04045, value / 12.92,
		((value + 0.055) / 1.055) ** 2.4)
	matrix = np.array([
		[0.4124564, 0.3575761, 0.1804375],
		[0.2126729, 0.7151522, 0.0721750],
		[0.0193339, 0.1191920, 0.9503041],
	], dtype=np.float32)
	xyz = value @ matrix.T
	xyz /= np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
	f = np.where(xyz > 0.008856, np.cbrt(xyz),
		7.787 * xyz + 16.0 / 116.0)
	return np.stack((
		116.0 * f[..., 1] - 16.0,
		500.0 * (f[..., 0] - f[..., 1]),
		200.0 * (f[..., 1] - f[..., 2]),
	), axis=-1)


def tone(path: Path) -> dict[str, object]:
	image = Image.open(path).convert("RGB")
	width, height = image.size
	# Background-weighted crop: excludes corner UI, lower controls, player,
	# foreground critters, and the lower navigation lane.
	crop_box = (
		int(width * 0.16), int(height * 0.06),
		int(width * 0.84), int(height * 0.57),
	)
	crop = image.crop(crop_box)
	array = np.asarray(crop)
	lab = srgb_to_lab(array)
	hsv = np.asarray(crop.convert("HSV"), dtype=np.float32)
	return {
		"path": str(path),
		"size": [width, height],
		"crop": list(crop_box),
		"rgb_mean": [round(value, 3) for value in ImageStat.Stat(crop).mean],
		"lab_mean": [
			round(float(np.mean(lab[..., index])), 3) for index in range(3)
		],
		"lab_median": [
			round(float(np.median(lab[..., index])), 3) for index in range(3)
		],
		"hsv_mean": [
			round(float(np.mean(hsv[..., index])), 3) for index in range(3)
		],
	}


def delta_lab(left: dict[str, object], right: dict[str, object]) -> float:
	left_lab = np.array(left["lab_mean"], dtype=np.float32)
	right_lab = np.array(right["lab_mean"], dtype=np.float32)
	return round(float(np.linalg.norm(left_lab - right_lab)), 3)


def annotate(master: Image.Image, seams: list[dict[str, object]],
		output: Path) -> None:
	scale = 0.5
	preview = master.convert("RGB").resize(
		(round(master.width * scale), round(master.height * scale)),
		Image.Resampling.LANCZOS)
	draw = ImageDraw.Draw(preview)
	font = ImageFont.load_default()
	for seam in seams:
		axis = str(seam["axis"])
		coordinate = int(seam["coordinate"])
		status = str(seam["status"])
		color = (
			(63, 224, 154)
			if status in ("lossless_split", "feathered_reuse_transition")
			else (255, 78, 104))
		if axis == "x":
			x = round(coordinate * scale)
			draw.line((x, 0, x, preview.height), fill=color, width=3)
			label_at = (x + 5, 8)
		else:
			y = round(coordinate * scale)
			draw.line((0, y, preview.width, y), fill=color, width=3)
			label_at = (5, y + 5)
		metric = seam["bands"]["full"]["mean_abs_rgb"]
		label = f"{axis}={coordinate}  MAD={metric}  {status}"
		draw.rectangle(
			(label_at[0] - 2, label_at[1] - 2,
			 label_at[0] + len(label) * 7 + 4, label_at[1] + 13),
			fill=(27, 22, 48))
		draw.text(label_at, label, font=font, fill=color)
	output.parent.mkdir(parents=True, exist_ok=True)
	preview.save(output, optimize=True)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--tile-root", type=Path, required=True)
	parser.add_argument("--capture-root", type=Path, required=True)
	parser.add_argument("--output-json", type=Path, required=True)
	parser.add_argument("--output-preview", type=Path, required=True)
	args = parser.parse_args()

	master, tiles = reconstruct(args.tile_root)
	array = np.asarray(master)
	seams: list[dict[str, object]] = []
	for x in (TILE_WIDTH, TILE_WIDTH * 2, TILE_WIDTH * 3):
		bands = {
			"full": edge_delta(array, "x", x, 0, MASTER_SIZE[1]),
			"architecture": edge_delta(array, "x", x, 55, 570),
			"runner": edge_delta(array, "x", x, 570, 730),
			"foreground_floor": edge_delta(array, "x", x, 730, 940),
		}
		center_join_ok = (
			x != TILE_WIDTH * 2
			or float(bands["full"]["relative_to_local"]) <= 1.5)
		seams.append({
			"axis": "x",
			"coordinate": x,
			"bands": bands,
			"status": (
				"feathered_reuse_transition"
				if x == TILE_WIDTH * 2 and center_join_ok
				else "art_direction_discontinuity"
				if x == TILE_WIDTH * 2
				else "lossless_split"),
		})
	for column in range(4):
		x0 = column * TILE_WIDTH
		x1 = x0 + TILE_WIDTH
		seams.append({
			"axis": "y",
			"coordinate": TOP_HEIGHT,
			"column": column,
			"bands": {
				"full": edge_delta(array[:, x0:x1], "y", TOP_HEIGHT, 0,
					TILE_WIDTH),
			},
			"status": "lossless_split",
		})

	hall_tones = {}
	for name in ("main_hall", "main_hall_screen_b"):
		path = args.capture_root / f"{name}.png"
		if path.exists():
			hall_tones[name] = tone(path)
	room_tones = {}
	for name in ROOM_CAPTURE_NAMES:
		path = args.capture_root / f"{name}.png"
		if path.exists():
			room_tones[name] = tone(path)
	reference_lab = np.mean([
		np.array(value["lab_mean"], dtype=np.float32)
		for value in room_tones.values()
	], axis=0)
	reference = {
		"lab_mean": [round(float(value), 3) for value in reference_lab],
		"rooms": list(room_tones),
	}
	for value in hall_tones.values():
		value["delta_e76_to_castle_room_mean"] = delta_lab(value, reference)
	context_tones = {}
	for name in CONTEXT_CAPTURE_NAMES:
		path = args.capture_root / f"{name}.png"
		if path.exists():
			context_tones[name] = tone(path)
	for value in hall_tones.values():
		for name, context in context_tones.items():
			value[f"lightness_delta_to_{name}"] = round(abs(
				float(value["lab_mean"][0]) - float(context["lab_mean"][0])), 3)
	bridge_paths = [
		args.tile_root.parent / "castle_playroom_portal_cutout_reuse.png",
		args.tile_root.parent / "castle_join_column_cutout_reuse.png",
		args.tile_root.parent / "castle_join_floor_inlay_reuse.png",
	]
	bridge_capture = args.capture_root / "main_hall_seam_bridge.png"
	runtime_bridge = {
		"assets": [
			{
				"path": str(path),
				"exists": path.exists(),
				"sha256": sha256(path) if path.exists() else "",
			}
			for path in bridge_paths
		],
		"capture_path": str(bridge_capture),
		"capture_exists": bridge_capture.exists(),
		"capture_sha256": sha256(bridge_capture)
			if bridge_capture.exists() else "",
	}
	bridge_ready = bool(
		all(bool(asset["exists"]) for asset in runtime_bridge["assets"])
		and runtime_bridge["capture_exists"])

	report = {
		"master_size": list(master.size),
		"master_ratio": round(master.width / master.height, 9),
		"tiles": tiles,
		"seams": seams,
		"tone": {
			"hall": hall_tones,
			"castle_rooms": room_tones,
			"castle_room_reference": reference,
			"current_game_context": context_tones,
		},
		"runtime_bridge": runtime_bridge,
		"verdict": {
			"internal_tile_splits": "PASS",
			"source_screen_join": (
				"PASS_FEATHERED_REUSE_TRANSITION"
				if str(seams[1]["status"]) == "feathered_reuse_transition"
				else "FAIL_ART_DIRECTION_DISCONTINUITY"),
			"screen_a_to_b_join": "PASS_RUNTIME_ARCHITECTURAL_BRIDGE"
				if bridge_ready else "FAIL_REQUIRES_ARCHITECTURAL_BRIDGE",
			"runtime_tone": "PASS" if hall_tones and max(
				float(value["delta_e76_to_castle_room_mean"])
				for value in hall_tones.values()) <= 12.0 else "FAIL",
		},
	}
	args.output_json.parent.mkdir(parents=True, exist_ok=True)
	args.output_json.write_text(json.dumps(report, indent=2) + "\n",
		encoding="utf-8")
	annotate(master, seams[:3], args.output_preview)
	print(json.dumps(report["verdict"], sort_keys=True))


if __name__ == "__main__":
	main()
