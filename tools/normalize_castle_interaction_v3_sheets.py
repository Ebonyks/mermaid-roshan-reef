#!/usr/bin/env python3
"""Key and register the 38 additive Pearl Castle v3 state sheets.

Every delivered frame is a complete generated object state.  This tool removes
the prepared chroma field, gives the cutout a clean antialiased matte, and moves
each state to one fixed anchor.  A single scale is calculated across all eight
states of an asset; per-frame scaling, warping, tweening, and repainting are
forbidden.
"""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

from PIL import Image, ImageChops

from castle_interaction_v3_specs import ADDITIONS


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "assets_src/imagegen/castle_object_animations_v3"
SOURCE_REPORT = SOURCE_ROOT / "castle_interactions_v3_source_preparation.json"
SHEET_DIR = ROOT / "assets/flats/castle/interactions_v3"
REPORT = SHEET_DIR / "castle_interactions_v3_normalization.json"
KEY = (255, 0, 255)
PADDING = 6
FIT_PADDING = 12
ALPHA_THRESHOLD = 16
RESAMPLED_CHROMA_ALPHA_LIMIT = 96
DETACHED_ARTIFACT_MAX_PIXELS = 96
EXPECTED_COUNT = 38


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def repository_text_sha256(path: Path) -> str:
	data = path.read_bytes().replace(b"\r\n", b"\n")
	return hashlib.sha256(data).hexdigest()


def source_path(spec: dict[str, Any]) -> Path:
	name = f"{spec['id']}_sheet_chroma.png"
	matches = sorted(SOURCE_ROOT.rglob(name))
	if len(matches) != 1:
		raise ValueError(f"{spec['id']}: expected one {name}, found {len(matches)}")
	return matches[0]


def runtime_path(spec: dict[str, Any]) -> Path:
	return SHEET_DIR / f"{spec['id']}_sheet.png"


def source_frames(sheet: Image.Image) -> list[Image.Image]:
	if sheet.size != (1024, 512):
		raise ValueError(f"prepared sheet dimensions {sheet.size} != (1024, 512)")
	frames: list[Image.Image] = []
	for index in range(8):
		column = index % 4
		row = index // 4
		frames.append(sheet.crop((
			column * 256,
			row * 256,
			(column + 1) * 256,
			(row + 1) * 256,
		)))
	return frames


def runtime_frames(sheet: Image.Image) -> tuple[list[Image.Image], int]:
	if sheet.width % 4 or sheet.height % 2:
		raise ValueError("runtime sheet is not an exact 4x2 grid")
	cell_width = sheet.width // 4
	cell_height = sheet.height // 2
	if cell_width != cell_height:
		raise ValueError("runtime cells are not square")
	frames: list[Image.Image] = []
	for index in range(8):
		column = index % 4
		row = index // 4
		frames.append(sheet.crop((
			column * cell_width,
			row * cell_height,
			(column + 1) * cell_width,
			(row + 1) * cell_height,
		)))
	return frames, cell_width


def _component_pixels(mask: bytearray, width: int, seed: int) -> list[int]:
	seen = {seed}
	stack = [seed]
	component: list[int] = []
	while stack:
		current = stack.pop()
		component.append(current)
		x = current % width
		for neighbor in (
			current - 1 if x else -1,
			current + 1 if x + 1 < width else -1,
			current - width if current >= width else -1,
			current + width if current + width < len(mask) else -1,
		):
			if neighbor >= 0 and mask[neighbor] and neighbor not in seen:
				seen.add(neighbor)
				stack.append(neighbor)
	return component


def chroma_to_rgba(cell: Image.Image) -> tuple[Image.Image, dict[str, int]]:
	"""Create a bounded two-pixel subject matte from the exact prepared key."""
	rgb = cell.convert("RGB")
	width, height = rgb.size
	colors = list(rgb.getdata())
	subject = bytearray(0 if pixel == KEY else 1 for pixel in colors)
	seen = bytearray(width * height)
	components: list[list[int]] = []
	for seed, visible in enumerate(subject):
		if not visible or seen[seed]:
			continue
		component = _component_pixels(subject, width, seed)
		for index in component:
			seen[index] = 1
		components.append(component)
	if not components:
		raise ValueError("animation frame has no visible subject")
	main_component = max(components, key=len)
	main_x = [index % width for index in main_component]
	main_y = [index // width for index in main_component]
	main_box = (min(main_x), min(main_y), max(main_x) + 1, max(main_y) + 1)
	tiny_removed = 0
	detached_removed = 0
	detached_components_removed = 0
	for component in components:
		if component is main_component:
			continue
		xs = [index % width for index in component]
		ys = [index // width for index in component]
		box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
		intersects_main_box = not (
			box[2] <= main_box[0]
			or box[0] >= main_box[2]
			or box[3] <= main_box[1]
			or box[1] >= main_box[3]
		)
		is_tiny = len(component) < 8
		is_detached_artifact = (
			len(component) <= DETACHED_ARTIFACT_MAX_PIXELS
			and not intersects_main_box
		)
		if not is_tiny and not is_detached_artifact:
			continue
		for index in component:
			subject[index] = 0
		if is_tiny:
			tiny_removed += len(component)
		else:
			detached_removed += len(component)
			detached_components_removed += 1

	# Distance inside the subject, capped at three pixels. The prepared step
	# already despilled boundary RGB, so these partial-alpha pixels do not
	# reintroduce a magenta halo.
	distance = bytearray(0 for _ in subject)
	queue: deque[int] = deque()
	for index, visible in enumerate(subject):
		if not visible:
			continue
		x = index % width
		y = index // width
		neighbors = (
			index - 1 if x else -1,
			index + 1 if x + 1 < width else -1,
			index - width if y else -1,
			index + width if y + 1 < height else -1,
		)
		if any(neighbor < 0 or not subject[neighbor] for neighbor in neighbors):
			distance[index] = 1
			queue.append(index)
	while queue:
		current = queue.popleft()
		if distance[current] >= 3:
			continue
		x = current % width
		for neighbor in (
			current - 1 if x else -1,
			current + 1 if x + 1 < width else -1,
			current - width if current >= width else -1,
			current + width if current + width < len(subject) else -1,
		):
			if neighbor >= 0 and subject[neighbor] and not distance[neighbor]:
				distance[neighbor] = distance[current] + 1
				queue.append(neighbor)
	alpha_values = []
	for index, visible in enumerate(subject):
		if not visible:
			alpha_values.append(0)
		elif distance[index] == 1:
			alpha_values.append(148)
		elif distance[index] == 2:
			alpha_values.append(224)
		else:
			alpha_values.append(255)
	# Zero RGB under transparent pixels before premultiplied resizing. Keeping
	# #FF00FF under alpha zero can reconstruct a visible key fringe when the
	# crop is resized and composited into the runtime cell.
	rgba_pixels = [
		(red, green, blue, alpha_value) if alpha_value else (0, 0, 0, 0)
		for (red, green, blue), alpha_value in zip(colors, alpha_values)
	]
	result = Image.new("RGBA", rgb.size, (0, 0, 0, 0))
	result.putdata(rgba_pixels)
	return result, {
		"tiny_subject_island_pixels_removed": tiny_removed,
		"detached_artifact_pixels_removed": detached_removed,
		"detached_artifact_components_removed": detached_components_removed,
		"detached_artifact_max_pixels": DETACHED_ARTIFACT_MAX_PIXELS,
		"partial_alpha_pixels_created": sum(0 < value < 255 for value in alpha_values),
	}


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int]:
	mask = frame.getchannel("A").point(
		lambda value: 255 if value >= ALPHA_THRESHOLD else 0
	)
	bbox = mask.getbbox()
	if bbox is None:
		raise ValueError("animation frame has no visible subject")
	return bbox


def anchor_point(
	frame: Image.Image,
	bbox: tuple[int, int, int, int],
	mode: str,
) -> tuple[float, float]:
	left, top, right, bottom = bbox
	if mode == "center":
		return ((left + right) * 0.5, (top + bottom) * 0.5)
	height = bottom - top
	band_height = max(5, int(round(height * 0.12)))
	band_top = top if mode == "top_center" else max(top, bottom - band_height)
	band_bottom = min(bottom, top + band_height) if mode == "top_center" else bottom
	band = frame.getchannel("A").crop((0, band_top, frame.width, band_bottom))
	band_bbox = band.point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
	anchor_x = (left + right) * 0.5
	if band_bbox is not None:
		anchor_x = (band_bbox[0] + band_bbox[2]) * 0.5
	anchor_y = float(top if mode == "top_center" else bottom)
	return (anchor_x, anchor_y)


def _resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
	return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def sanitize_resampled_chroma(frame: Image.Image) -> tuple[Image.Image, int]:
	"""Remove only low-alpha key pixels reconstructed by LANCZOS."""
	pixels = list(frame.convert("RGBA").getdata())
	removed = 0
	output: list[tuple[int, int, int, int]] = []
	for red, green, blue, alpha_value in pixels:
		if not alpha_value:
			output.append((0, 0, 0, 0))
			continue
		if red >= 220 and blue >= 220 and green <= 55:
			if alpha_value > RESAMPLED_CHROMA_ALPHA_LIMIT:
				raise ValueError(
					f"near-key subject pixel has alpha {alpha_value}; source matte is unsafe")
			output.append((0, 0, 0, 0))
			removed += 1
			continue
		output.append((red, green, blue, alpha_value))
	result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
	result.putdata(output)
	return result, removed


def frame_metrics(frame: Image.Image) -> dict[str, Any]:
	bbox = alpha_bbox(frame)
	alpha = frame.getchannel("A")
	histogram = alpha.histogram()
	visible_exact_key = 0
	visible_near_key = 0
	for red, green, blue, alpha_value in frame.getdata():
		if alpha_value < ALPHA_THRESHOLD:
			continue
		if (red, green, blue) == KEY:
			visible_exact_key += 1
		if red >= 220 and blue >= 220 and green <= 55:
			visible_near_key += 1
	border = (
		list(alpha.crop((0, 0, frame.width, 1)).getdata())
		+ list(alpha.crop((0, frame.height - 1, frame.width, frame.height)).getdata())
		+ list(alpha.crop((0, 0, 1, frame.height)).getdata())
		+ list(alpha.crop((frame.width - 1, 0, frame.width, frame.height)).getdata())
	)
	visible = sum(histogram[ALPHA_THRESHOLD:])
	return {
		"alpha_bbox": list(bbox),
		"visible_pixels": visible,
		"transparent_pixels": histogram[0],
		"partial_alpha_pixels": sum(histogram[1:255]),
		"opaque_pixels": histogram[255],
		"visible_exact_chroma_pixels": visible_exact_key,
		"visible_near_chroma_pixels": visible_near_key,
		"visible_near_chroma_ratio": round(visible_near_key / float(max(1, visible)), 9),
		"transparent_canvas_border": all(value == 0 for value in border),
	}


def material_changed_fraction(base: Image.Image, frame: Image.Image) -> float:
	base_rgba = base.convert("RGBA")
	frame_rgba = frame.convert("RGBA")
	visible = ImageChops.lighter(
		base_rgba.getchannel("A"), frame_rgba.getchannel("A")
	).point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
	difference = ImageChops.difference(base_rgba, frame_rgba)
	channels = difference.split()
	rgb = ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]), channels[2])
	changed = ImageChops.lighter(
		rgb.point(lambda value: 255 if value >= 18 else 0),
		channels[3].point(lambda value: 255 if value >= 16 else 0),
	)
	changed = ImageChops.multiply(changed, visible)
	return changed.histogram()[255] / float(max(1, visible.histogram()[255]))


def normalize(spec: dict[str, Any], destination: Path) -> dict[str, Any]:
	path = source_path(spec)
	with Image.open(path) as image_value:
		source = image_value.convert("RGB")
	keyed = [chroma_to_rgba(frame) for frame in source_frames(source)]
	frames = [value[0] for value in keyed]
	removed_islands = sum(value[1]["tiny_subject_island_pixels_removed"] for value in keyed)
	detached_artifact_pixels = sum(
		value[1]["detached_artifact_pixels_removed"] for value in keyed
	)
	detached_artifact_components = sum(
		value[1]["detached_artifact_components_removed"] for value in keyed
	)
	cell_size = int(spec["runtime_cell_size"])
	mode = str(spec["anchor_mode"])
	measured = [(alpha_bbox(frame), anchor_point(frame, alpha_bbox(frame), mode)) for frame in frames]
	target_x = cell_size * 0.5
	if mode == "top_center":
		target_y = float(PADDING)
	elif mode == "bottom_center":
		target_y = float(cell_size - PADDING)
	else:
		target_y = cell_size * 0.5
	fit_scale = 2.0
	for bbox, source_anchor in measured:
		left, top, right, bottom = bbox
		for extent, available in (
			(source_anchor[0] - left, target_x - FIT_PADDING),
			(right - source_anchor[0], cell_size - FIT_PADDING - target_x),
			(source_anchor[1] - top, target_y - FIT_PADDING),
			(bottom - source_anchor[1], cell_size - FIT_PADDING - target_y),
		):
			if extent > 0.0:
				fit_scale = min(fit_scale, max(0.01, available) / extent)
	scale = min(2.0, fit_scale)
	output = Image.new("RGBA", (cell_size * 4, cell_size * 2), (0, 0, 0, 0))
	anchor_translation_corrections: list[list[int]] = []
	resampled_chroma_pixels_removed: list[int] = []
	for index, (frame, (bbox, source_anchor)) in enumerate(zip(frames, measured)):
		cropped = frame.crop(bbox)
		anchor_local = (
			(source_anchor[0] - bbox[0]) * scale,
			(source_anchor[1] - bbox[1]) * scale,
		)
		size = (
			max(1, int(round(cropped.width * scale))),
			max(1, int(round(cropped.height * scale))),
		)
		if size != cropped.size:
			cropped = _resize_premultiplied(cropped, size)
		destination_xy = (
			int(round(target_x - anchor_local[0])),
			int(round(target_y - anchor_local[1])),
		)
		cell = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))
		cell.alpha_composite(cropped, destination_xy)
		cell, removed_chroma = sanitize_resampled_chroma(cell)
		resampled_chroma_pixels_removed.append(removed_chroma)
		# Resampling and integer placement can move the measured silhouette
		# anchor by a few pixels. Correct registration with translation only;
		# FIT_PADDING reserves room for this bounded correction.
		placed_bbox = alpha_bbox(cell)
		placed_anchor = anchor_point(cell, placed_bbox, mode)
		correction = [
			int(round(target_x - placed_anchor[0])),
			int(round(target_y - placed_anchor[1])),
		]
		if correction != [0, 0]:
			shifted = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))
			shifted.alpha_composite(cell, tuple(correction))
			cell = shifted
		anchor_translation_corrections.append(correction)
		output.alpha_composite(
			cell,
			((index % 4) * cell_size, (index // 4) * cell_size),
		)
	destination.parent.mkdir(parents=True, exist_ok=True)
	output.save(destination, optimize=True, compress_level=9)
	with Image.open(destination) as normalized_value:
		normalized = normalized_value.convert("RGBA")
	normalized_frames, measured_cell = runtime_frames(normalized)
	bboxes = [alpha_bbox(frame) for frame in normalized_frames]
	anchors = [anchor_point(frame, bbox, mode) for frame, bbox in zip(normalized_frames, bboxes)]
	edge_gap = min(
		min(bbox[0], bbox[1], measured_cell - bbox[2], measured_cell - bbox[3])
		for bbox in bboxes
	)
	frame_hashes = [hashlib.sha256(frame.tobytes()).hexdigest() for frame in normalized_frames]
	return {
		"id": spec["id"],
		"room": spec["room"],
		"source_path": path.relative_to(ROOT).as_posix(),
		"source_sha256": sha256(path),
		"runtime_path": destination.relative_to(ROOT).as_posix(),
		"runtime_sha256": sha256(destination),
		"grid": [4, 2],
		"frame_count": 8,
		"cell_size": [cell_size, cell_size],
		"sheet_dimensions": [cell_size * 4, cell_size * 2],
		"anchor_mode": mode,
		"uniform_scale": round(scale, 9),
		"padding_pixels": PADDING,
		"fit_padding_pixels": FIT_PADDING,
		"edge_gap_pixels": edge_gap,
		"anchor_translation_corrections": anchor_translation_corrections,
		"max_anchor_translation_pixels": max(
			max(abs(value) for value in correction)
			for correction in anchor_translation_corrections
		),
		"resampled_chroma_pixels_removed": resampled_chroma_pixels_removed,
		"resampled_chroma_alpha_limit": RESAMPLED_CHROMA_ALPHA_LIMIT,
		"anchor_spread_pixels": [
			round(max(value[0] for value in anchors) - min(value[0] for value in anchors), 3),
			round(max(value[1] for value in anchors) - min(value[1] for value in anchors), 3),
		],
		"frame_bboxes": [list(bbox) for bbox in bboxes],
		"frame_sha256": frame_hashes,
		"unique_frame_count": len(set(frame_hashes)),
		"changed_fraction_from_rest": [
			round(material_changed_fraction(normalized_frames[0], frame), 8)
			for frame in normalized_frames
		],
		"per_frame_alpha_qa": [frame_metrics(frame) for frame in normalized_frames],
		"tiny_subject_island_pixels_removed": removed_islands,
		"detached_artifact_pixels_removed": detached_artifact_pixels,
		"detached_artifact_components_removed": detached_artifact_components,
		"detached_artifact_max_pixels": DETACHED_ARTIFACT_MAX_PIXELS,
		"fixed_anchor_translation_only": True,
		"one_uniform_scale_across_all_frames": True,
		"per_frame_scale_used": False,
		"subject_geometry_warped": False,
		"state_pixels_synthesized": False,
		"primary_animation_is_overlay": False,
	}


def validate_entry(entry: dict[str, Any], override: Path | None = None) -> list[str]:
	errors: list[str] = []
	path = override or ROOT / str(entry.get("runtime_path", ""))
	asset_id = str(entry.get("id", ""))
	if not path.is_file():
		return [f"{asset_id}: runtime sheet is missing"]
	if override is None and sha256(path) != entry.get("runtime_sha256"):
		errors.append(f"{asset_id}: runtime hash is stale")
	with Image.open(path) as image_value:
		sheet = image_value.convert("RGBA")
	try:
		frames, cell_size = runtime_frames(sheet)
	except ValueError as exc:
		return [f"{asset_id}: {exc}"]
	if list(sheet.size) != entry.get("sheet_dimensions"):
		errors.append(f"{asset_id}: sheet dimensions differ from report")
	if entry.get("grid") != [4, 2] or int(entry.get("frame_count", 0)) != 8:
		errors.append(f"{asset_id}: grid or frame count differs from report")
	if entry.get("cell_size") != [cell_size, cell_size]:
		errors.append(f"{asset_id}: cell size differs from report")
	if max(sheet.size) > 1024:
		errors.append(f"{asset_id}: runtime sheet exceeds 1024")
	mode = str(entry.get("anchor_mode", "bottom_center"))
	boxes = [alpha_bbox(frame) for frame in frames]
	anchors = [anchor_point(frame, bbox, mode) for frame, bbox in zip(frames, boxes)]
	edge_gap = min(
		min(bbox[0], bbox[1], cell_size - bbox[2], cell_size - bbox[3])
		for bbox in boxes
	)
	if edge_gap < PADDING:
		errors.append(f"{asset_id}: transparent cell border is {edge_gap}px")
	if (
		int(entry.get("padding_pixels", -1)) != PADDING
		or int(entry.get("fit_padding_pixels", -1)) != FIT_PADDING
		or entry.get("edge_gap_pixels") != edge_gap
	):
		errors.append(f"{asset_id}: padding metrics differ from report")
	corrections = entry.get("anchor_translation_corrections", [])
	if not isinstance(corrections, list) or len(corrections) != 8:
		errors.append(f"{asset_id}: anchor translation evidence is incomplete")
	if int(entry.get("detached_artifact_max_pixels", -1)) != DETACHED_ARTIFACT_MAX_PIXELS:
		errors.append(f"{asset_id}: detached-artifact cleanup evidence is incomplete")
	removed_chroma = entry.get("resampled_chroma_pixels_removed", [])
	if (
		not isinstance(removed_chroma, list)
		or len(removed_chroma) != 8
		or int(entry.get("resampled_chroma_alpha_limit", -1))
		!= RESAMPLED_CHROMA_ALPHA_LIMIT
	):
		errors.append(f"{asset_id}: resampled chroma cleanup evidence is incomplete")
	spread = [
		round(max(value[0] for value in anchors) - min(value[0] for value in anchors), 3),
		round(max(value[1] for value in anchors) - min(value[1] for value in anchors), 3),
	]
	if spread[0] > 1.5 or spread[1] > 1.5:
		errors.append(f"{asset_id}: anchor drift is {spread[0]:.2f},{spread[1]:.2f}px")
	if entry.get("anchor_spread_pixels") != spread:
		errors.append(f"{asset_id}: anchor metrics differ from report")
	if entry.get("frame_bboxes") != [list(bbox) for bbox in boxes]:
		errors.append(f"{asset_id}: frame bounding boxes differ from report")
	hashes = [hashlib.sha256(frame.tobytes()).hexdigest() for frame in frames]
	if len(set(hashes)) != 8:
		errors.append(f"{asset_id}: authored states are not all unique")
	if entry.get("frame_sha256") != hashes or int(entry.get("unique_frame_count", 0)) != 8:
		errors.append(f"{asset_id}: frame hashes differ from report")
	qa = entry.get("per_frame_alpha_qa", [])
	if not isinstance(qa, list) or len(qa) != 8:
		errors.append(f"{asset_id}: per-frame alpha QA is incomplete")
	else:
		for index, (frame, recorded) in enumerate(zip(frames, qa)):
			measured = frame_metrics(frame)
			if measured != recorded:
				errors.append(f"{asset_id}: frame {index} alpha QA is stale")
				continue
			if not measured["transparent_canvas_border"]:
				errors.append(f"{asset_id}: frame {index} touches canvas border")
			if measured["visible_exact_chroma_pixels"]:
				errors.append(f"{asset_id}: frame {index} retains visible exact chroma")
			if measured["visible_near_chroma_pixels"]:
				errors.append(f"{asset_id}: frame {index} retains visible near-key chroma")
			if measured["visible_pixels"] < 100:
				errors.append(f"{asset_id}: frame {index} has no usable silhouette")
	if not bool(entry.get("one_uniform_scale_across_all_frames", False)):
		errors.append(f"{asset_id}: uniform scale contract is missing")
	if bool(entry.get("per_frame_scale_used", True)):
		errors.append(f"{asset_id}: per-frame scale is forbidden")
	if not bool(entry.get("fixed_anchor_translation_only", False)):
		errors.append(f"{asset_id}: fixed-anchor translation contract is missing")
	if bool(entry.get("subject_geometry_warped", True)) or bool(
		entry.get("state_pixels_synthesized", True)
	):
		errors.append(f"{asset_id}: forbidden geometry or state synthesis is declared")
	if bool(entry.get("primary_animation_is_overlay", True)):
		errors.append(f"{asset_id}: primary animation must be the complete fixture")
	return errors


def check_report() -> int:
	if not REPORT.is_file():
		print("FAIL: v3 normalization report is missing")
		return 1
	report = json.loads(REPORT.read_text(encoding="utf-8"))
	entries = report.get("assets", [])
	errors: list[str] = []
	expected_ids = {str(entry["id"]) for entry in ADDITIONS}
	if int(report.get("schema_version", 0)) != 3:
		errors.append("normalization report schema is not 3")
	if report.get("tool_sha256") != repository_text_sha256(Path(__file__)):
		errors.append("normalization tool hash differs from report")
	if not SOURCE_REPORT.is_file() or report.get("source_preparation_sha256") != repository_text_sha256(SOURCE_REPORT):
		errors.append("source preparation report hash is stale")
	if int(report.get("asset_count", -1)) != EXPECTED_COUNT or len(entries) != EXPECTED_COUNT:
		errors.append(f"normalization roster has {len(entries)} assets")
	if (
		int(report.get("max_visible_near_chroma_pixels", -1)) != 0
		or float(report.get("max_visible_near_chroma_ratio", -1.0)) != 0.0
	):
		errors.append("normalization report retains visible near-key chroma")
	entry_ids = {str(entry.get("id", "")) for entry in entries}
	if entry_ids != expected_ids:
		errors.append("normalization IDs differ from the 38 v3 specs")
	expected_names = {f"{entry['id']}_sheet.png" for entry in ADDITIONS}
	actual_names = {path.name for path in SHEET_DIR.glob("*_sheet.png")}
	if actual_names != expected_names:
		errors.append("runtime sheet roster differs from the 38 v3 specs")
	prepared_index: dict[str, dict[str, Any]] = {}
	if SOURCE_REPORT.is_file():
		prepared = json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))
		prepared_index = {str(entry.get("id", "")): entry for entry in prepared.get("assets", [])}
	for entry in entries:
		asset_id = str(entry.get("id", ""))
		prepared_entry = prepared_index.get(asset_id, {})
		source = ROOT / str(entry.get("source_path", ""))
		if (
			not source.is_file()
			or sha256(source) != entry.get("source_sha256")
			or entry.get("source_sha256") != prepared_entry.get("prepared_sha256")
		):
			errors.append(f"{asset_id}: prepared source linkage is stale")
		errors.extend(validate_entry(entry))
	if errors:
		for error in errors:
			print("FAIL: " + error)
		return 1
	print(f"CASTLEV3|NORMALIZATION_OK|assets={len(entries)}|padding={PADDING}|uniform=true")
	return 0


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	if args.check:
		return check_report()
	if REPORT.exists():
		print("FAIL: normalization report exists; use --check")
		return 1
	if not SOURCE_REPORT.is_file():
		raise SystemExit("run prepare_castle_interaction_v3_sources.py first")
	prepared = json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))
	prepared_index = {str(entry["id"]): entry for entry in prepared.get("assets", [])}
	if int(prepared.get("schema_version", 0)) != 3:
		raise SystemExit("source preparation schema is not 3")
	prepare_tool = ROOT / str(prepared.get("tool", ""))
	if not prepare_tool.is_file() or prepared.get("tool_sha256") != repository_text_sha256(prepare_tool):
		raise SystemExit("source preparation tool hash is stale")
	if set(prepared_index) != {str(entry["id"]) for entry in ADDITIONS}:
		raise SystemExit("source preparation roster does not match v3 specs")
	for spec in ADDITIONS:
		path = source_path(spec)
		record = prepared_index[str(spec["id"])]
		if not path.is_file() or sha256(path) != record.get("prepared_sha256"):
			raise SystemExit(f"{spec['id']}: prepared source is missing or stale")

	SHEET_DIR.mkdir(parents=True, exist_ok=True)
	stage_root = Path(tempfile.mkdtemp(prefix=".castle_v3_normalize_", dir=SHEET_DIR))
	entries: list[dict[str, Any]] = []
	committed: list[Path] = []
	try:
		staged: dict[Path, Path] = {}
		for spec in ADDITIONS:
			destination = runtime_path(spec)
			stage_path = stage_root / destination.name
			entry = normalize(spec, stage_path)
			entry["runtime_path"] = destination.relative_to(ROOT).as_posix()
			entry["source_preparation_sha256"] = str(
				prepared_index[str(spec["id"])]["prepared_sha256"]
			)
			validation_errors = validate_entry(entry, stage_path)
			if validation_errors:
				raise ValueError("; ".join(validation_errors))
			entries.append(entry)
			staged[destination] = stage_path
		max_near_ratio = max(
			float(frame["visible_near_chroma_ratio"])
			for entry in entries
			for frame in entry["per_frame_alpha_qa"]
		)
		max_near_pixels = max(
			int(frame["visible_near_chroma_pixels"])
			for entry in entries
			for frame in entry["per_frame_alpha_qa"]
		)
		payload = {
			"schema_version": 3,
			"generated_on": "2026-08-02",
			"tool": "tools/normalize_castle_interaction_v3_sheets.py",
			"tool_sha256": repository_text_sha256(Path(__file__)),
			"source_preparation": SOURCE_REPORT.relative_to(ROOT).as_posix(),
			"source_preparation_sha256": repository_text_sha256(SOURCE_REPORT),
			"method": "connected_and_global_near_key_alpha_then_premultiplied_resize_low_alpha_chroma_sanitize_fixed_anchor_translation_and_one_uniform_asset_scale",
			"transactional": True,
			"one_time_guard": True,
			"padding_pixels": PADDING,
			"fit_padding_pixels": FIT_PADDING,
			"visible_near_chroma_policy": "zero_pixels_across_all_304_frames",
			"max_visible_near_chroma_ratio": max_near_ratio,
			"max_visible_near_chroma_pixels": max_near_pixels,
			"asset_count": len(entries),
			"assets": entries,
		}
		report_stage = stage_root / REPORT.name
		report_stage.write_bytes((json.dumps(payload, indent=2) + "\n").encode("utf-8"))
		try:
			for destination, stage_path in staged.items():
				if destination.exists():
					raise FileExistsError(f"refusing to replace {destination}")
				os.replace(stage_path, destination)
				committed.append(destination)
			os.replace(report_stage, REPORT)
		except Exception:
			if REPORT.exists():
				REPORT.unlink()
			for destination in committed:
				destination.unlink(missing_ok=True)
			raise
	finally:
		shutil.rmtree(stage_root, ignore_errors=True)
	print(f"NORMALIZED|assets={len(entries)}|padding={PADDING}|uniform=true")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
