#!/usr/bin/env python3
"""Rebuild the Main Hall runtime grid with its two screens registered.

The two approved 2048 x 1153 source masters were authored with the same
fixture/floor band at different source Y coordinates. Cropping both masters
from Y=212 raised Screen B by 65 pixels at runtime, causing the carpet,
walkway, door sockets, and interactive Sprite3D fixtures to overlap.

This tool preserves both source masters and crops one unscaled 1672 x 941
playable view from each:

* Screen A: x=376, y=212
* Screen B: x=376, y=147

Each view is sliced losslessly into two 836-pixel columns and 470/471-pixel
rows. The existing one-pixel Mobile render bleed is then rebuilt from those
new non-overlapping source tiles. No pixels are generated, scaled, blended,
or interpolated.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "assets_src" / "castle" / "main_hall_alignment"
RUNTIME_ROOT = (
	ROOT / "assets" / "flats" / "castle" / "main_hall_2screen")
TILE_ROOT = RUNTIME_ROOT / "tiles"
BLEED_ROOT = TILE_ROOT / "runtime_bleed"
AUDIT_ROOT = ROOT / "audit" / "castle_sprite3d"

SOURCE_A = SOURCE_ROOT / "main_hall_screen_a_fixture_aligned_master.png"
SOURCE_B = SOURCE_ROOT / "main_hall_screen_b_fixture_aligned_master.png"
VIEW_A = (376, 212, 2048, 1153)
VIEW_B = (376, 147, 2048, 1088)
VIEW_SIZE = (1672, 941)
TILE_WIDTH = 836
TOP_HEIGHT = 470
BOTTOM_HEIGHT = 471
FIXTURE_MASTER_Y = {"A": 427, "B": 362}
EXPECTED_RUNTIME_FIXTURE_Y = 215

MANIFEST_PATH = AUDIT_ROOT / "castle_hall_runtime_registration.json"
CONTACT_PATH = AUDIT_ROOT / "castle_hall_runtime_registration.png"


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _pixel_equal(left: Image.Image, right: Image.Image) -> bool:
	return ImageChops.difference(left, right).getbbox() is None


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
	path = Path(
		"C:/Windows/Fonts/arialbd.ttf"
		if bold else "C:/Windows/Fonts/arial.ttf")
	if path.exists():
		return ImageFont.truetype(str(path), size)
	return ImageFont.load_default()


def _floor_edge_y(view: Image.Image) -> int:
	"""Return the strongest horizontal architectural edge near the walkway."""
	array = np.asarray(view.convert("RGB"), dtype=np.float32)
	luminance = array.mean(axis=2)
	score = np.abs(np.diff(luminance, axis=0)).mean(axis=1)
	start = 600
	end = 665
	return int(start + np.argmax(score[start:end]))


def _write_contact(view_a: Image.Image, view_b: Image.Image) -> None:
	preview_a = view_a.resize((836, 470), Image.Resampling.LANCZOS)
	preview_b = view_b.resize((836, 470), Image.Resampling.LANCZOS)
	canvas = Image.new("RGB", (1672, 548), "#efeaff")
	canvas.paste(preview_a, (0, 78))
	canvas.paste(preview_b, (836, 78))
	draw = ImageDraw.Draw(canvas)
	draw.text(
		(20, 14),
		"PEARL CASTLE - LOSSLESS TWO-SCREEN REGISTRATION",
		font=_font(26, bold=True),
		fill="#302a68")
	draw.text(
		(20, 48),
		"A y=212 | B y=147 | shared fixture y=215 | no scale/blend",
		font=_font(17),
		fill="#514784")
	edge_a = round(_floor_edge_y(view_a) * 470 / 941) + 78
	edge_b = round(_floor_edge_y(view_b) * 470 / 941) + 78
	draw.line((0, edge_a, 836, edge_a), fill="#56f0bd", width=3)
	draw.line((836, edge_b, 1671, edge_b), fill="#56f0bd", width=3)
	draw.line((836, 78, 836, 547), fill="#f6c14d", width=3)
	CONTACT_PATH.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(CONTACT_PATH, format="PNG", optimize=True)


def main() -> None:
	source_a = Image.open(SOURCE_A).convert("RGB")
	source_b = Image.open(SOURCE_B).convert("RGB")
	view_a = source_a.crop(VIEW_A)
	view_b = source_b.crop(VIEW_B)
	if view_a.size != VIEW_SIZE or view_b.size != VIEW_SIZE:
		raise ValueError(
			f"Expected {VIEW_SIZE}, got {view_a.size} and {view_b.size}")

	TILE_ROOT.mkdir(parents=True, exist_ok=True)
	BLEED_ROOT.mkdir(parents=True, exist_ok=True)
	records: list[dict[str, object]] = []
	views = (view_a, view_b)
	view_rects = (VIEW_A, VIEW_B)
	screen_ids = ("A", "B")

	for screen_index, view in enumerate(views):
		screen_id = screen_ids[screen_index]
		view_rect = view_rects[screen_index]
		for local_column in range(2):
			column = screen_index * 2 + local_column
			for row, (top, height) in enumerate(
					((0, TOP_HEIGHT), (TOP_HEIGHT, BOTTOM_HEIGHT))):
				left = local_column * TILE_WIDTH
				tile = view.crop(
					(left, top, left + TILE_WIDTH, top + height))
				path = TILE_ROOT / (
					f"main_hall_room_led_r{row}_c{column}.png")
				tile.save(path, format="PNG", optimize=True)
				master_rect = (
					view_rect[0] + left,
					view_rect[1] + top,
					view_rect[0] + left + TILE_WIDTH,
					view_rect[1] + top + height,
				)
				records.append({
					"screen": screen_id,
					"row": row,
					"column": column,
					"path": path.relative_to(ROOT).as_posix(),
					"dimensions": list(tile.size),
					"sha256": _sha256(path),
					"master_source_rect": list(master_rect),
				})

	for column in range(4):
		top_path = TILE_ROOT / (
			f"main_hall_room_led_r0_c{column}.png")
		bottom_path = TILE_ROOT / (
			f"main_hall_room_led_r1_c{column}.png")
		top = Image.open(top_path).convert("RGB")
		bottom = Image.open(bottom_path).convert("RGB")
		derived = Image.new("RGB", (TILE_WIDTH, TOP_HEIGHT + 1))
		derived.paste(top, (0, 0))
		derived.paste(
			bottom.crop((0, 0, TILE_WIDTH, 1)), (0, TOP_HEIGHT))
		bleed_path = BLEED_ROOT / (
			f"main_hall_room_led_r0_c{column}_bleed.png")
		derived.save(bleed_path, format="PNG", optimize=True)

		if not _pixel_equal(
				derived.crop((0, 0, TILE_WIDTH, TOP_HEIGHT)), top):
			raise RuntimeError(f"Column {column} changed approved pixels")
		if not _pixel_equal(
				derived.crop((0, TOP_HEIGHT, TILE_WIDTH, TOP_HEIGHT + 1)),
				bottom.crop((0, 0, TILE_WIDTH, 1))):
			raise RuntimeError(
				f"Column {column} bleed row is not source-exact")

		for record in records:
			if record["column"] == column and record["row"] == 0:
				record["runtime_bleed_path"] = (
					bleed_path.relative_to(ROOT).as_posix())
				record["runtime_bleed_dimensions"] = list(derived.size)
				record["runtime_bleed_sha256"] = _sha256(bleed_path)
				record["runtime_bleed_source_exact"] = True
				break

	reconstructions: dict[str, bool] = {}
	for screen_index, view in enumerate(views):
		screen_id = screen_ids[screen_index]
		reconstructed = Image.new("RGB", VIEW_SIZE)
		for local_column in range(2):
			column = screen_index * 2 + local_column
			for row, (top, _height) in enumerate(
					((0, TOP_HEIGHT), (TOP_HEIGHT, BOTTOM_HEIGHT))):
				path = TILE_ROOT / (
					f"main_hall_room_led_r{row}_c{column}.png")
				reconstructed.paste(
					Image.open(path).convert("RGB"),
					(local_column * TILE_WIDTH, top))
		reconstructions[screen_id] = _pixel_equal(reconstructed, view)
		if not reconstructions[screen_id]:
			raise RuntimeError(
				f"Screen {screen_id} tiles do not reconstruct exactly")

	fixture_runtime_y = {
		"A": FIXTURE_MASTER_Y["A"] - VIEW_A[1],
		"B": FIXTURE_MASTER_Y["B"] - VIEW_B[1],
	}
	floor_edges = {
		"A": _floor_edge_y(view_a),
		"B": _floor_edge_y(view_b),
	}
	if any(
			value != EXPECTED_RUNTIME_FIXTURE_Y
			for value in fixture_runtime_y.values()
	):
		raise RuntimeError(
			f"Fixture sockets are not aligned: {fixture_runtime_y}")
	if abs(floor_edges["A"] - floor_edges["B"]) > 4:
		raise RuntimeError(
			f"Walkway bands are not aligned: {floor_edges}")

	_write_contact(view_a, view_b)
	manifest = {
		"schema": 1,
		"purpose": (
			"Lossless Main Hall screen, walkway, socket, and Sprite3D "
			"registration"),
		"new_art": False,
		"scaling": False,
		"interpolation": False,
		"blend": False,
		"source_masters_preserved": True,
		"screen_views": {
			"A": {
				"source": SOURCE_A.relative_to(ROOT).as_posix(),
				"source_sha256": _sha256(SOURCE_A),
				"rect": list(VIEW_A),
				"dimensions": list(view_a.size),
			},
			"B": {
				"source": SOURCE_B.relative_to(ROOT).as_posix(),
				"source_sha256": _sha256(SOURCE_B),
				"rect": list(VIEW_B),
				"dimensions": list(view_b.size),
			},
		},
		"vertical_registration_delta_pixels": 65,
		"fixture_runtime_y": fixture_runtime_y,
		"walkway_edge_runtime_y": floor_edges,
		"walkway_edge_delta_pixels": abs(
			floor_edges["A"] - floor_edges["B"]),
		"tile_reconstruction_pixel_exact": reconstructions,
		"tiles": records,
		"contact_sheet": {
			"path": CONTACT_PATH.relative_to(ROOT).as_posix(),
			"sha256": _sha256(CONTACT_PATH),
		},
	}
	MANIFEST_PATH.write_text(
		json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(
		"OK: Main Hall A/B registered losslessly; "
		f"fixture_y={fixture_runtime_y}; walkway_y={floor_edges}")


if __name__ == "__main__":
	main()
