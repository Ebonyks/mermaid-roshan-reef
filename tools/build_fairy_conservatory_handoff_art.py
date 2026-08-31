#!/usr/bin/env python3
"""Build the Chapter 3 Rainbow Stage and Butterfly House 2D art package.

The continuous 16:9 stage background is the approved Lily-Pad Fairy World
redrawn at an upright eye-level perspective.  The walkable rainbow causeway
and Butterfly House remain separate whole-sprite subjects.  The 3640x2048
background is assembled from six independently generated 1254-square panels
at exact 1:1 pixel scale.  Open sky and water overlap between panels, with no
readable landmark crossing a seam.  The completed master is then sliced
without seams and its hashes and authority are recorded.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


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
BACKGROUND_PRIOR_RAW = RAW_ROOT / "fairy_pond_horizon_openai_raw.png"
BACKGROUND_CENTER_REFERENCE = RAW_ROOT / "fairy_pond_native_center_openai_raw.png"
BACKGROUND_PANEL_ROOT = RAW_ROOT / "background_panels"
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
BACKGROUND_PANEL_SIZE = (1254, 1254)
BACKGROUND_PANEL_STEP = (1193, 794)
BACKGROUND_PANEL_OVERLAP = (61, 460)
BACKGROUND_ALIGNED_HORIZON_Y = 480
BACKGROUND_VERTICAL_BLEND_END = 1190
BACKGROUND_PANEL_SPECS = (
	("top_left", "exec-95013e94-cb9e-459f-a7c6-88ce52d70abb", 0, 0, 12),
	("top_center", "exec-a1798b3a-d111-402b-a08e-455f15694cb2", 1, 0, -64),
	("top_right", "exec-e3c60551-45fb-46aa-8dd8-38997d075a82", 2, 0, 0),
	("bottom_left", "exec-11630358-710f-4636-b283-ffe0a1ccc2ab", 0, 1, 0),
	("bottom_center", "exec-f6352de8-a64d-45b1-b5dc-855e8c9ed7a7", 1, 1, 0),
	("bottom_right", "exec-039ee267-2c93-4ccf-bf3c-55fcfad0df70", 2, 1, 0),
)


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


def _align_top_panel(source: Image.Image, shift_y: int) -> Image.Image:
	"""Align generated horizons by cropping or reflecting edge sky, never scaling."""
	if source.size != BACKGROUND_PANEL_SIZE:
		raise ValueError(
			f"bad generated panel size: {source.size} != {BACKGROUND_PANEL_SIZE}")
	pixels = np.asarray(source.convert("RGB"), dtype=np.uint8)
	height, width = pixels.shape[:2]
	aligned = np.empty_like(pixels)
	if shift_y > 0:
		# The small reflected strip is open sky only.  No landmark or source
		# pixel is enlarged, and the 12-pixel strip is outside the stage crop.
		aligned[:shift_y] = pixels[:shift_y][::-1]
		aligned[shift_y:] = pixels[:height - shift_y]
	elif shift_y < 0:
		crop = -shift_y
		aligned[:height - crop] = pixels[crop:]
		aligned[height - crop:] = pixels[-1:]
	else:
		aligned[:] = pixels
	return Image.fromarray(aligned, "RGB")


def _horizontal_row(panels: list[Image.Image]) -> Image.Image:
	"""Join three native panels through their generated open-water overlaps."""
	if len(panels) != 3:
		raise ValueError("background row must contain exactly three panels")
	row = Image.new("RGB", (BACKGROUND_MASTER_SIZE[0], BACKGROUND_PANEL_SIZE[1]))
	row.paste(panels[0], (0, 0))
	overlap = BACKGROUND_PANEL_OVERLAP[0]
	mask_pixels = np.full(
		(BACKGROUND_PANEL_SIZE[1], BACKGROUND_PANEL_SIZE[0]), 255,
		dtype=np.uint8,
	)
	mask_pixels[:, :overlap] = np.round(
		np.linspace(0.0, 255.0, overlap, dtype=np.float32),
	).astype(np.uint8)[None, :]
	mask = Image.fromarray(mask_pixels, "L")
	for column, panel in enumerate(panels[1:], start=1):
		row.paste(panel, (column * BACKGROUND_PANEL_STEP[0], 0), mask)
	return row


def _smooth_rows(values: np.ndarray, radius: int) -> np.ndarray:
	"""Low-pass a per-row color correction so no painted feature is traced."""
	window = radius * 2 + 1
	padded = np.pad(values, ((radius, radius), (0, 0)), mode="edge")
	cumulative = np.vstack((
		np.zeros((1, values.shape[1]), dtype=np.float32),
		np.cumsum(padded, axis=0, dtype=np.float32),
	))
	return (cumulative[window:] - cumulative[:-window]) / float(window)


def _harmonize_center_edges(
		left: Image.Image, center: Image.Image, right: Image.Image) -> Image.Image:
	"""Match only broad edge palette, leaving every generated form intact."""
	left_pixels = np.asarray(left.convert("RGB"), dtype=np.float32)
	center_pixels = np.asarray(center.convert("RGB"), dtype=np.float32)
	right_pixels = np.asarray(right.convert("RGB"), dtype=np.float32)
	overlap = BACKGROUND_PANEL_OVERLAP[0]
	left_delta = (
		left_pixels[:, -overlap:].mean(axis=1)
		- center_pixels[:, :overlap].mean(axis=1)
	)
	right_delta = (
		right_pixels[:, :overlap].mean(axis=1)
		- center_pixels[:, -overlap:].mean(axis=1)
	)
	left_delta = np.clip(_smooth_rows(left_delta, 42), -72.0, 72.0)
	right_delta = np.clip(_smooth_rows(right_delta, 42), -72.0, 72.0)
	left_weight = np.linspace(
		1.0, 0.0, BACKGROUND_PANEL_SIZE[0], dtype=np.float32)
	right_weight = 1.0 - left_weight
	corrected = center_pixels.copy()
	corrected += left_delta[:, None, :] * left_weight[None, :, None]
	corrected += right_delta[:, None, :] * right_weight[None, :, None]
	return Image.fromarray(
		np.clip(corrected, 0.0, 255.0).astype(np.uint8), "RGB")


def _assemble_native_background(
		top_panels: list[Image.Image], bottom_panels: list[Image.Image]) -> Image.Image:
	"""Assemble six 1:1 panels into the exact 3640x2048 production master."""
	top_row = _horizontal_row(top_panels)
	bottom_row = _horizontal_row(bottom_panels)
	master = Image.new("RGB", BACKGROUND_MASTER_SIZE)
	master.paste(top_row, (0, 0))
	local_blend_end = BACKGROUND_VERTICAL_BLEND_END - BACKGROUND_PANEL_STEP[1]
	mask_pixels = np.full(
		(BACKGROUND_PANEL_SIZE[1], BACKGROUND_MASTER_SIZE[0]), 255,
		dtype=np.uint8,
	)
	mask_pixels[:local_blend_end] = np.round(
		np.linspace(
			0.0, 255.0, local_blend_end, dtype=np.float32,
		)[:, None]
	).astype(np.uint8)
	mask = Image.fromarray(mask_pixels, "L")
	master.paste(bottom_row, (0, BACKGROUND_PANEL_STEP[1]), mask)
	return master


def _build_background() -> tuple[list[Path], list[Path], list[dict[str, object]]]:
	references = [
		BACKGROUND_PRIOR_RAW,
		BACKGROUND_CENTER_REFERENCE,
		FAIRY_POND_REFERENCE,
		FAIRY_TWILIGHT_REFERENCE,
		FAIRY_DAWN_REFERENCE,
	]
	for path in references:
		if not path.is_file():
			raise FileNotFoundError(path)
	panel_records: list[dict[str, object]] = []
	top_panels: list[Image.Image] = []
	bottom_panels: list[Image.Image] = []
	for name, result_id, column, row, shift_y in BACKGROUND_PANEL_SPECS:
		path = BACKGROUND_PANEL_ROOT / f"{name}.png"
		if not path.is_file():
			raise FileNotFoundError(path)
		panel = Image.open(path).convert("RGB")
		if panel.size != BACKGROUND_PANEL_SIZE:
			raise ValueError(
				f"bad generated panel size: {path} {panel.size}")
		if row == 0:
			prepared = _align_top_panel(panel, shift_y)
			top_panels.append(prepared)
		else:
			prepared = panel
			bottom_panels.append(prepared)
		panel_records.append({
			"name": name,
			"result_id": result_id,
			"path": path,
			"column": column,
			"row": row,
			"position": [
				column * BACKGROUND_PANEL_STEP[0],
				row * BACKGROUND_PANEL_STEP[1],
			],
			"horizon_alignment_shift_y": shift_y,
		})
	top_panels[1] = _harmonize_center_edges(
		top_panels[0], top_panels[1], top_panels[2])
	bottom_panels[1] = _harmonize_center_edges(
		bottom_panels[0], bottom_panels[1], bottom_panels[2])
	master = _assemble_native_background(top_panels, bottom_panels)
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
	return references, outputs, panel_records


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
	background_inputs, background_tiles, panel_records = _build_background()
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
			"reference_authority": "Lily-Pad Fairy World / Fairy Pond",
			"reference_inputs": [
				{"path": path.relative_to(ROOT).as_posix(), "sha256": _hash(path)}
				for path in background_inputs
			],
			"panels": [
				{
					"name": str(record["name"]),
					"result_id": str(record["result_id"]),
					"path": Path(record["path"]).relative_to(ROOT).as_posix(),
					"dimensions": list(BACKGROUND_PANEL_SIZE),
					"sha256": _hash(Path(record["path"])),
					"row": int(record["row"]),
					"column": int(record["column"]),
					"position": list(record["position"]),
					"horizon_alignment_shift_y": int(
						record["horizon_alignment_shift_y"]),
					"scale": 1.0,
					"role": "native generated full-frame background panel",
				}
				for record in panel_records
			],
			"panel_prompt_set": {
				"shared": (
					"Polished 2D Lily-Pad Fairy World storybook art using the "
					"approved Fairy Pond palette and rounded painted forms; upright "
					"eye-level sky-and-water perspective, no Sky Lagoon motifs, no "
					"characters, no text, and open sky/water at every join."
				),
				"top_left": "Left garden bank; open sky and pond toward the right seam.",
				"top_center": "Open central sky and pond corridor with a clear horizon.",
				"top_right": "Right garden bank; open sky and pond toward the left seam.",
				"bottom_left": "Water-only foreground; left bank, open water to the right.",
				"bottom_center": "Pure open aqua/deep-blue water corridor; no plants.",
				"bottom_right": "Water-only foreground; right bank, open water to the left.",
			},
			"master": {
				"path": BACKGROUND_MASTER.relative_to(ROOT).as_posix(),
				"dimensions": list(BACKGROUND_MASTER_SIZE),
				"sha256": _hash(BACKGROUND_MASTER),
				"authored_at_target_dimensions": True,
				"source_pixel_upscale": False,
				"panel_size": list(BACKGROUND_PANEL_SIZE),
				"panel_step": list(BACKGROUND_PANEL_STEP),
				"panel_overlap": list(BACKGROUND_PANEL_OVERLAP),
				"aligned_horizon_y": BACKGROUND_ALIGNED_HORIZON_Y,
				"assembly_method": (
					"six generated full-frame panels placed at native 1:1 scale; "
					"top horizons aligned by lossless crop or a 12-pixel open-sky "
					"edge reflection; broad low-frequency center-panel palette "
					"harmonization preserves all painted forms; linear feathering "
					"occurs only inside generated open-sky/open-water overlaps; no "
					"source image is enlarged"
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
			"seam_policy": (
				"generated joins cross open sky/water only; the accepted continuous "
				"master is then sliced into eight non-overlapping runtime tiles"
			),
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
