#!/usr/bin/env python3
"""Build the Chapter 3 Rainbow Stage and Butterfly House 2D art package.

The continuous 16:9 stage background is the approved Lily-Pad Fairy World
redrawn at an upright eye-level perspective.  The walkable rainbow causeway
and Butterfly House remain separate whole-sprite subjects.  This script
preserves every native source, normalizes the complete generated background,
slices it without seams, and records hashes and reference authority.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "assets_src" / "fairy_conservatory_handoff_2026-08-30"
RAW_ROOT = SOURCE_ROOT / "raw"
MASTER_ROOT = SOURCE_ROOT / "masters"
REVIEW_ROOT = SOURCE_ROOT / "review"
RUNTIME_ROOT = ROOT / "assets" / "flats" / "fairy_conservatory_handoff"
BACKGROUND_ROOT = RUNTIME_ROOT / "background"
MANIFEST_PATH = SOURCE_ROOT / "asset_manifest.json"
REVIEW_STAGE = REVIEW_ROOT / "rainbow_stage_composite_1280x720.png"

WALKWAY_RAW = RAW_ROOT / "rainbow_walkway_openai_raw.png"
HOUSE_RAW = RAW_ROOT / "butterfly_house_openai_raw.png"
BACKGROUND_RAW = RAW_ROOT / "fairy_pond_horizon_openai_raw.png"
WALKWAY_RUNTIME = RUNTIME_ROOT / "rainbow_walkway.png"
HOUSE_RUNTIME = RUNTIME_ROOT / "butterfly_house.png"
BACKGROUND_MASTER = MASTER_ROOT / "handoff_background_master_3640x2048.png"
FAIRY_POND_REFERENCE = ROOT / "assets" / "fairy" / "pond_panorama.png"
FAIRY_TWILIGHT_REFERENCE = (
	ROOT / "assets_src" / "fairy_v2" / "concepts"
	/ "background_twilight.png"
)
FAIRY_DAWN_REFERENCE = (
	ROOT / "assets_src" / "fairy_v2" / "concepts"
	/ "background_dawn.png"
)
ROSHAN_SOURCE = ROOT / "assets" / "characters" / "roshan_25d" / "roshan_base.png"

CANVAS_EDGE = 1024
SUBJECT_EDGE = 1000
BACKGROUND_MASTER_SIZE = (3640, 2048)
BACKGROUND_TILE_SIZE = (910, 1024)
BACKGROUND_GRID = (4, 2)


def _hash(path: Path) -> str:
	digest = sha256()
	with path.open("rb") as source:
		for block in iter(lambda: source.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def _connected(mask: np.ndarray, seeds: list[int]) -> np.ndarray:
	height, width = mask.shape
	flat = mask.ravel()
	reached = bytearray(width * height)
	queue: deque[int] = deque()

	def push(index: int) -> None:
		if not reached[index] and bool(flat[index]):
			reached[index] = 1
			queue.append(index)

	for seed in seeds:
		push(seed)
	while queue:
		index = queue.popleft()
		y_pos, x_pos = divmod(index, width)
		for y_next in range(max(0, y_pos - 1), min(height, y_pos + 2)):
			row = y_next * width
			for x_next in range(max(0, x_pos - 1), min(width, x_pos + 2)):
				push(row + x_next)
	return np.frombuffer(reached, dtype=np.uint8).reshape(
		(height, width)).astype(bool)


def _remove_connected_neutral_field(source: Image.Image) -> Image.Image:
	"""Remove only the checker/white field connected to the canvas border."""
	rgb = np.asarray(source.convert("RGB"), dtype=np.uint8)
	height, width = rgb.shape[:2]
	minimum = rgb.min(axis=2)
	maximum = rgb.max(axis=2)
	neutral = (minimum >= 232) & ((maximum - minimum) <= 10)
	seeds = list(range(width))
	seeds.extend((height - 1) * width + x_pos for x_pos in range(width))
	seeds.extend(y_pos * width for y_pos in range(height))
	seeds.extend(y_pos * width + width - 1 for y_pos in range(height))
	background = _connected(neutral, seeds)
	alpha = Image.fromarray((~background).astype(np.uint8) * 255, "L")
	alpha = alpha.filter(ImageFilter.MinFilter(3))
	alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))
	rgba = np.dstack((rgb, np.asarray(alpha, dtype=np.uint8)))
	rgba[rgba[:, :, 3] == 0, :3] = 0
	return Image.fromarray(rgba, "RGBA")


def _normalize_subject(source: Image.Image, remove_field: bool) -> Image.Image:
	if remove_field:
		source = _remove_connected_neutral_field(source)
	else:
		source = source.convert("RGBA")
	bounds = source.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError("generated source has no visible subject")
	subject = source.crop(bounds)
	scale = min(SUBJECT_EDGE / subject.width, SUBJECT_EDGE / subject.height)
	subject = subject.resize(
		(max(1, round(subject.width * scale)),
		 max(1, round(subject.height * scale))),
		Image.Resampling.LANCZOS,
	)
	canvas = Image.new("RGBA", (CANVAS_EDGE, CANVAS_EDGE), (0, 0, 0, 0))
	canvas.alpha_composite(
		subject,
		((CANVAS_EDGE - subject.width) // 2,
		 (CANVAS_EDGE - subject.height) // 2),
	)
	return canvas


def _audit_cutout(image: Image.Image) -> dict[str, object]:
	if image.size != (CANVAS_EDGE, CANVAS_EDGE) or image.mode != "RGBA":
		raise ValueError(f"bad cutout format: {image.size} {image.mode}")
	alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
	corner_alpha = [
		int(alpha[0, 0]), int(alpha[0, -1]),
		int(alpha[-1, 0]), int(alpha[-1, -1]),
	]
	if any(corner_alpha):
		raise ValueError(f"cutout corners are not transparent: {corner_alpha}")
	return {
		"dimensions": [CANVAS_EDGE, CANVAS_EDGE],
		"mode": "RGBA",
		"alpha_bbox": list(image.getchannel("A").getbbox() or ()),
		"corner_alpha": corner_alpha,
		"visible_alpha_pixels": int(np.count_nonzero(alpha)),
	}


def _build_background() -> tuple[list[Path], list[Path], tuple[int, int]]:
	inputs = [
		BACKGROUND_RAW,
		FAIRY_POND_REFERENCE,
		FAIRY_TWILIGHT_REFERENCE,
		FAIRY_DAWN_REFERENCE,
	]
	for path in inputs:
		if not path.is_file():
			raise FileNotFoundError(path)
	source = Image.open(BACKGROUND_RAW).convert("RGB")
	source_dimensions = source.size
	master = ImageOps.fit(
		source,
		BACKGROUND_MASTER_SIZE,
		method=Image.Resampling.LANCZOS,
		centering=(0.5, 0.5),
	)
	if master.size != BACKGROUND_MASTER_SIZE:
		raise ValueError(f"bad background master size: {master.size}")
	MASTER_ROOT.mkdir(parents=True, exist_ok=True)
	master.save(BACKGROUND_MASTER, format="PNG", optimize=True)

	BACKGROUND_ROOT.mkdir(parents=True, exist_ok=True)
	outputs: list[Path] = []
	for row in range(BACKGROUND_GRID[1]):
		for column in range(BACKGROUND_GRID[0]):
			left = column * BACKGROUND_TILE_SIZE[0]
			top = row * BACKGROUND_TILE_SIZE[1]
			tile = master.crop((
				left, top,
				left + BACKGROUND_TILE_SIZE[0],
				top + BACKGROUND_TILE_SIZE[1],
			))
			path = BACKGROUND_ROOT / f"handoff_background_r{row}_c{column}.png"
			tile.save(path, format="PNG", optimize=True)
			outputs.append(path)
	return inputs, outputs, source_dimensions


def _place_review_sprite(
		canvas: Image.Image, source: Image.Image,
		center: tuple[int, int], edge: int) -> None:
	source = source.convert("RGBA")
	bounds = source.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError("review sprite has no visible subject")
	source = source.crop(bounds)
	scale = edge / max(source.size)
	source = source.resize(
		(max(1, round(source.width * scale)),
		 max(1, round(source.height * scale))),
		Image.Resampling.LANCZOS,
	)
	canvas.alpha_composite(
		source,
		(center[0] - source.width // 2, center[1] - source.height // 2),
	)


def _place_registered_review_sprite(
		canvas: Image.Image, source: Image.Image, center: tuple[int, int],
		target_visible_size: tuple[int, int]) -> None:
	"""Match runtime scaling of a padded registration card exactly."""
	source = source.convert("RGBA")
	bounds = source.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError("registered review sprite has no visible subject")
	visible_size = (bounds[2] - bounds[0], bounds[3] - bounds[1])
	scale = min(
		target_visible_size[0] / visible_size[0],
		target_visible_size[1] / visible_size[1],
	)
	registered = source.resize(
		(max(1, round(source.width * scale)),
		 max(1, round(source.height * scale))),
		Image.Resampling.LANCZOS,
	)
	canvas.alpha_composite(
		registered,
		(center[0] - registered.width // 2,
		 center[1] - registered.height // 2),
	)


def _build_review_stage(
		background: Image.Image, walkway: Image.Image,
		house: Image.Image) -> None:
	"""Flatten the intended runtime placement for visual audit only."""
	if not ROSHAN_SOURCE.is_file():
		raise FileNotFoundError(ROSHAN_SOURCE)
	preview = background.convert("RGBA").resize(
		(1280, 720), Image.Resampling.LANCZOS)
	_place_review_sprite(preview, walkway, (640, 500), 620)
	_place_review_sprite(preview, house, (640, 184), 270)
	_place_registered_review_sprite(
		preview, Image.open(ROSHAN_SOURCE), (640, 594), (134, 172))
	REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
	preview.save(REVIEW_STAGE, format="PNG", optimize=True)


def main() -> None:
	for path in (WALKWAY_RAW, HOUSE_RAW):
		if not path.is_file():
			raise FileNotFoundError(path)
	RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
	MASTER_ROOT.mkdir(parents=True, exist_ok=True)

	walkway = _normalize_subject(Image.open(WALKWAY_RAW), remove_field=False)
	house = _normalize_subject(Image.open(HOUSE_RAW), remove_field=True)
	walkway.save(WALKWAY_RUNTIME, format="PNG", optimize=True)
	house.save(HOUSE_RUNTIME, format="PNG", optimize=True)
	background_inputs, background_tiles, source_dimensions = _build_background()
	_build_review_stage(Image.open(BACKGROUND_MASTER), walkway, house)

	manifest = {
		"schema": 1,
		"purpose": "Chapter 3 Rainbow Stage handoff and Butterfly House landmark",
		"generation_method": "OpenAI built-in image generation",
		"art_gap": (
			"No approved upright Fairy Pond stage plate, standalone walkable "
			"rainbow causeway, or true-2D Butterfly House landmark existed. "
			"The background redraw is bound to the approved Lily-Pad Fairy "
			"World rather than Sky Lagoon."
		),
		"background": {
			"result_id": "exec-f94c58c7-28bd-455d-897c-c0c7a16588a3",
			"raw": BACKGROUND_RAW.relative_to(ROOT).as_posix(),
			"raw_dimensions": list(source_dimensions),
			"raw_sha256": _hash(BACKGROUND_RAW),
			"reference_authority": "Lily-Pad Fairy World / Fairy Pond",
			"reference_inputs": [
				{"path": path.relative_to(ROOT).as_posix(), "sha256": _hash(path)}
				for path in background_inputs[1:]
			],
			"master": {
				"path": BACKGROUND_MASTER.relative_to(ROOT).as_posix(),
				"dimensions": list(BACKGROUND_MASTER_SIZE),
				"sha256": _hash(BACKGROUND_MASTER),
				"whole_canvas_transform": (
					"centered ImageOps.fit with Lanczos resampling; no local "
					"retouch, object move, seam blend, or tile regeneration"
				),
			},
			"runtime_tiles": [
				{
					"path": path.relative_to(ROOT).as_posix(),
					"dimensions": list(BACKGROUND_TILE_SIZE),
					"sha256": _hash(path),
				}
				for path in background_tiles
			],
			"seam_policy": "single approved master sliced into non-overlapping tiles",
		},
		"generated_subjects": {
			"rainbow_walkway": {
				"result_id": "exec-3648d4fe-ca54-44e2-bdc9-a3eb1f3f1453",
				"raw": WALKWAY_RAW.relative_to(ROOT).as_posix(),
				"raw_sha256": _hash(WALKWAY_RAW),
				"runtime": WALKWAY_RUNTIME.relative_to(ROOT).as_posix(),
				"runtime_sha256": _hash(WALKWAY_RUNTIME),
				"processing": "uniform whole-subject normalization from native RGBA",
				"audit": _audit_cutout(walkway),
			},
			"butterfly_house": {
				"result_id": "exec-7f598cda-3e9c-441d-aa73-cd4038000612",
				"raw": HOUSE_RAW.relative_to(ROOT).as_posix(),
				"raw_sha256": _hash(HOUSE_RAW),
				"runtime": HOUSE_RUNTIME.relative_to(ROOT).as_posix(),
				"runtime_sha256": _hash(HOUSE_RUNTIME),
				"processing": (
					"border-connected neutral checker removal, one-pixel matte "
					"support, 0.8-pixel feather, uniform whole-subject normalization"
				),
				"audit": _audit_cutout(house),
			},
		},
		"review_only_composite": {
			"path": REVIEW_STAGE.relative_to(ROOT).as_posix(),
			"dimensions": [1280, 720],
			"sha256": _hash(REVIEW_STAGE),
			"delivery_pixels": False,
			"purpose": "visual placement audit; runtime remains separate Canvas sprites",
			"rainbow_path_reaches_stage_base_y": 720,
		},
	}
	MANIFEST_PATH.write_text(
		json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(f"wrote {BACKGROUND_MASTER.relative_to(ROOT)}")
	for path in background_tiles:
		print(f"wrote {path.relative_to(ROOT)}")
	print(f"wrote {WALKWAY_RUNTIME.relative_to(ROOT)}")
	print(f"wrote {HOUSE_RUNTIME.relative_to(ROOT)}")
	print(f"wrote {REVIEW_STAGE.relative_to(ROOT)}")
	print(f"wrote {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
	main()
