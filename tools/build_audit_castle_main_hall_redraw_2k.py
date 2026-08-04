#!/usr/bin/env python3
"""Build and audit the accepted Main Hall redraw at strict per-screen 2K.

This pipeline is deliberately specific to the 2026-08-03 clean Main Hall
redraw.  It performs only whole-canvas Pillow Lanczos normalization:

    accepted native 1672x941 -> accepted prior 2048x1152 -> 3640x2048

The two final screens are stitched without scaling into 7280x2048, then
losslessly split into a two-row by eight-column grid.  Every runtime texture
has a longest edge of 1024 pixels or less, and the independently authored
screen boundary falls exactly after column 3.

The build phase emits immutable masters, exact non-overlapping runtime tiles,
and a provenance manifest.  The audit phase independently reconstructs the
panorama, re-derives both resize steps, verifies file and pixel hashes, records
ratio rounding, measures seams and content invariance, and writes review
proofs.  ``--audit-only`` skips all production writes and revalidates the
existing outputs.

No crop, padding, canvas extension, local retouch, seam blend, AI upscale, or
new art is permitted by this tool.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import PIL
from PIL import Image, ImageChops, ImageDraw, ImageFont


NATIVE_SIZE = (1672, 941)
PRIOR_SIZE = (2048, 1152)
FINAL_SCREEN_SIZE = (3640, 2048)
PANORAMA_SIZE = (7280, 2048)
ROWS = 2
COLUMNS = 8
ROW_HEIGHTS = (1024, 1024)
# Four exact 910px columns preserve the accepted source ratio within one pixel.
SCREEN_COLUMN_WIDTHS = (910, 910, 910, 910)
COLUMN_WIDTHS = SCREEN_COLUMN_WIDTHS + SCREEN_COLUMN_WIDTHS
SCREEN_BOUNDARY_COLUMN = 3
SCREEN_BOUNDARY_X = 3640
RESAMPLE_NAME = "Pillow Image.Resampling.LANCZOS"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _portable_path(path: Path) -> str:
	"""Return a repository-relative path and reject external evidence paths."""
	resolved = path.resolve()
	try:
		return resolved.relative_to(REPOSITORY_ROOT).as_posix()
	except ValueError as error:
		raise ValueError(
			f"Pipeline inputs and outputs must stay inside the repository: {path}") from error


def _pixel_sha256(image: Image.Image) -> str:
	return hashlib.sha256(image.tobytes()).hexdigest()


def _pixel_equal(left: Image.Image, right: Image.Image) -> bool:
	return (
		left.mode == right.mode
		and left.size == right.size
		and ImageChops.difference(left, right).getbbox() is None
	)


def _load_rgb(path: Path, expected_size: tuple[int, int]) -> Image.Image:
	with Image.open(path) as opened:
		image = opened.copy()
	if image.mode != "RGB":
		raise ValueError(f"Expected RGB image, got {image.mode}: {path}")
	if image.size != expected_size:
		raise ValueError(
			f"Expected {expected_size[0]}x{expected_size[1]}, got "
			f"{image.width}x{image.height}: {path}")
	return image


def _save_png(image: Image.Image, path: Path) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	image.save(path, format="PNG", optimize=True)


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
	font_path = Path(
		"C:/Windows/Fonts/arialbd.ttf"
		if bold else "C:/Windows/Fonts/arial.ttf")
	if font_path.exists():
		return ImageFont.truetype(str(font_path), size)
	return ImageFont.load_default()


def _bounds(lengths: tuple[int, ...]) -> list[int]:
	result = [0]
	for length in lengths:
		result.append(result[-1] + length)
	return result


def _ratio_step(
		source_size: tuple[int, int],
		target_size: tuple[int, int],
		label: str,
) -> dict[str, Any]:
	source_ratio = source_size[0] / source_size[1]
	target_ratio = target_size[0] / target_size[1]
	ideal_height = target_size[0] / source_ratio
	height_rounding_error = abs(target_size[1] - ideal_height)
	return {
		"label": label,
		"source_dimensions": list(source_size),
		"target_dimensions": list(target_size),
		"source_aspect_ratio": source_ratio,
		"target_aspect_ratio": target_ratio,
		"aspect_ratio_delta": abs(source_ratio - target_ratio),
		"ideal_target_height_at_fixed_target_width": ideal_height,
		"target_height_rounding_error_pixels": height_rounding_error,
		"one_pixel_rounding_tolerance": 1.0,
		"within_one_pixel_rounding_tolerance": height_rounding_error <= 1.0,
		"whole_canvas": True,
		"resampling": RESAMPLE_NAME,
		"crop": False,
		"padding": False,
		"canvas_extension": False,
		"local_retouch": False,
		"seam_blend": False,
		"ai_upscale": False,
	}


def _content_metrics(reference: Image.Image, enlarged: Image.Image) -> dict[str, Any]:
	back_normalized = enlarged.resize(reference.size, Image.Resampling.LANCZOS)
	reference_array = np.asarray(reference, dtype=np.float32)
	back_array = np.asarray(back_normalized, dtype=np.float32)
	difference = np.abs(reference_array - back_array)
	left = reference_array.reshape(-1)
	right = back_array.reshape(-1)
	left_centered = left - float(left.mean())
	right_centered = right - float(right.mean())
	denominator = float(
		np.sqrt(np.sum(left_centered * left_centered)
			* np.sum(right_centered * right_centered)))
	correlation = (
		float(np.sum(left_centered * right_centered)) / denominator
		if denominator > 0.0 else 1.0)
	return {
		"comparison_space_dimensions": list(reference.size),
		"normalization": (
			"final whole canvas reduced to the accepted 2048x1152 prior "
			"with Pillow Lanczos for audit only"),
		"mean_absolute_channel_error": float(difference.mean()),
		"p95_absolute_channel_error": float(np.percentile(difference, 95)),
		"p99_absolute_channel_error": float(np.percentile(difference, 99)),
		"maximum_absolute_channel_error": int(difference.max()),
		"pixel_channel_correlation": correlation,
		"mean_error_limit": 0.5,
		"p99_error_limit": 3.0,
		"correlation_floor": 0.999,
		"passes": (
			float(difference.mean()) <= 0.5
			and float(np.percentile(difference, 99)) <= 3.0
			and correlation >= 0.999),
	}


def _vertical_seam_metrics(
		panorama: Image.Image,
		x_position: int,
		role: str,
) -> dict[str, Any]:
	array = np.asarray(panorama, dtype=np.float32)
	edge_delta = np.abs(array[:, x_position - 1, :] - array[:, x_position, :])
	band_width = 32
	left_mean = array[:, x_position - band_width:x_position, :].mean(axis=(0, 1))
	right_mean = array[:, x_position:x_position + band_width, :].mean(axis=(0, 1))
	return {
		"orientation": "vertical",
		"coordinate": x_position,
		"role": role,
		"edge_rgb_mean_absolute_error": float(edge_delta.mean()),
		"edge_rgb_p95_absolute_error": float(np.percentile(edge_delta, 95)),
		"edge_maximum_channel_error": int(edge_delta.max()),
		"band_width": band_width,
		"left_band_mean_rgb": [float(value) for value in left_mean],
		"right_band_mean_rgb": [float(value) for value in right_mean],
		"band_mean_rgb_euclidean_delta": float(np.linalg.norm(left_mean - right_mean)),
	}


def _horizontal_seam_metrics(
		panorama: Image.Image,
		y_position: int,
) -> dict[str, Any]:
	array = np.asarray(panorama, dtype=np.float32)
	edge_delta = np.abs(array[y_position - 1, :, :] - array[y_position, :, :])
	return {
		"orientation": "horizontal",
		"coordinate": y_position,
		"role": "lossless_intra_screen_tile_boundary",
		"edge_rgb_mean_absolute_error": float(edge_delta.mean()),
		"edge_rgb_p95_absolute_error": float(np.percentile(edge_delta, 95)),
		"edge_maximum_channel_error": int(edge_delta.max()),
	}


def _record_image(path: Path, image: Image.Image) -> dict[str, Any]:
	return {
		"path": _portable_path(path),
		"dimensions": list(image.size),
		"mode": image.mode,
		"file_sha256": _sha256(path),
		"pixel_sha256": _pixel_sha256(image),
	}


def _build(arguments: argparse.Namespace) -> None:
	natives = {
		"A": _load_rgb(arguments.native_a, NATIVE_SIZE),
		"B": _load_rgb(arguments.native_b, NATIVE_SIZE),
	}
	priors = {
		"A": _load_rgb(arguments.prior_a, PRIOR_SIZE),
		"B": _load_rgb(arguments.prior_b, PRIOR_SIZE),
	}
	final_paths = {"A": arguments.final_a, "B": arguments.final_b}

	finals: dict[str, Image.Image] = {}
	chains: dict[str, Any] = {}
	for label in ("A", "B"):
		rederived_prior = natives[label].resize(PRIOR_SIZE, Image.Resampling.LANCZOS)
		prior_exact = _pixel_equal(rederived_prior, priors[label])
		if not prior_exact:
			raise RuntimeError(
				f"Accepted prior Screen {label} is not the exact whole-canvas "
				"Lanczos normalization of its native source")
		final = priors[label].resize(FINAL_SCREEN_SIZE, Image.Resampling.LANCZOS)
		_save_png(final, final_paths[label])
		finals[label] = final
		chains[label] = {
			"native": _record_image(
				arguments.native_a if label == "A" else arguments.native_b,
				natives[label]),
			"native_to_prior": {
				**_ratio_step(NATIVE_SIZE, PRIOR_SIZE, "accepted native to prior production"),
				"rederived_prior_pixel_exact": prior_exact,
			},
			"prior": _record_image(
				arguments.prior_a if label == "A" else arguments.prior_b,
				priors[label]),
			"prior_to_final": _ratio_step(
				PRIOR_SIZE, FINAL_SCREEN_SIZE, "prior production to strict per-screen 2K"),
			"final": _record_image(final_paths[label], final),
		}

	panorama = Image.new("RGB", PANORAMA_SIZE)
	panorama.paste(finals["A"], (0, 0))
	panorama.paste(finals["B"], (SCREEN_BOUNDARY_X, 0))
	_save_png(panorama, arguments.panorama)

	arguments.tile_dir.mkdir(parents=True, exist_ok=True)
	for stale_path in arguments.tile_dir.glob(f"{arguments.prefix}_r*_c*.png"):
		stale_path.unlink()

	x_bounds = _bounds(COLUMN_WIDTHS)
	y_bounds = _bounds(ROW_HEIGHTS)
	tile_records: list[dict[str, Any]] = []
	for row in range(ROWS):
		for column in range(COLUMNS):
			rectangle = (
				x_bounds[column],
				y_bounds[row],
				x_bounds[column + 1],
				y_bounds[row + 1],
			)
			tile = panorama.crop(rectangle)
			tile_path = arguments.tile_dir / (
				f"{arguments.prefix}_r{row}_c{column}.png")
			_save_png(tile, tile_path)
			screen = "A" if column <= SCREEN_BOUNDARY_COLUMN else "B"
			screen_x_offset = 0 if screen == "A" else SCREEN_BOUNDARY_X
			tile_records.append({
				"row": row,
				"column": column,
				"screen": screen,
				"screen_local_column": column % 4,
				"path": _portable_path(tile_path),
				"dimensions": list(tile.size),
				"file_sha256": _sha256(tile_path),
				"pixel_sha256": _pixel_sha256(tile),
				"panorama_source_rectangle": list(rectangle),
				"screen_source_rectangle": [
					rectangle[0] - screen_x_offset,
					rectangle[1],
					rectangle[2] - screen_x_offset,
					rectangle[3],
				],
				"long_edge": max(tile.size),
				"runtime_long_edge_within_1024_limit": max(tile.size) <= 1024,
			})

	manifest = {
		"schema": 1,
		"pipeline": "castle_main_hall_redraw_strict_per_screen_2k",
		"decision_date": "2026-08-04",
		"new_art": False,
		"source_art_preserved": True,
		"script": {
			"path": _portable_path(Path(__file__)),
			"sha256": _sha256(Path(__file__)),
			"pillow_version": PIL.__version__,
		},
		"production_operation": {
			"resampling": RESAMPLE_NAME,
			"resampling_interpolation": True,
			"resampling_scope": "same whole-canvas transform on the complete flattened screen",
			"whole_canvas_only": True,
			"crop": False,
			"padding": False,
			"canvas_extension": False,
			"local_retouch": False,
			"seam_blend": False,
			"ai_upscale": False,
			"new_art_generation": False,
		},
		"transform_chains": chains,
		"panorama": _record_image(arguments.panorama, panorama),
		"stitch": {
			"operation": "lossless side-by-side paste",
			"screen_a_rectangle": [
				0, 0, FINAL_SCREEN_SIZE[0], FINAL_SCREEN_SIZE[1]],
			"screen_b_rectangle": [
				SCREEN_BOUNDARY_X, 0, PANORAMA_SIZE[0], PANORAMA_SIZE[1]],
			"screen_boundary_x": SCREEN_BOUNDARY_X,
			"scaling": False,
			"overlap": False,
			"gap": False,
		},
		"runtime_grid": {
			"rows": ROWS,
			"columns": COLUMNS,
			"tile_count": ROWS * COLUMNS,
			"column_widths": list(COLUMN_WIDTHS),
			"row_heights": list(ROW_HEIGHTS),
			"column_bounds": x_bounds,
			"row_bounds": y_bounds,
			"screen_boundary_after_column": SCREEN_BOUNDARY_COLUMN,
			"screen_boundary_x": SCREEN_BOUNDARY_X,
			"screen_boundary_exact": x_bounds[SCREEN_BOUNDARY_COLUMN + 1] == SCREEN_BOUNDARY_X,
			"tiles_non_overlapping": True,
			"tiles_lossless": True,
			"all_tiles_within_1024_long_edge": all(
				record["runtime_long_edge_within_1024_limit"]
				for record in tile_records),
		},
		"tiles": tile_records,
	}
	arguments.build_manifest.parent.mkdir(parents=True, exist_ok=True)
	arguments.build_manifest.write_text(
		json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _color_overlay(reference: Image.Image, comparison: Image.Image) -> Image.Image:
	reference_gray = reference.convert("L")
	comparison_gray = comparison.convert("L")
	return Image.merge("RGB", (reference_gray, comparison_gray, comparison_gray))


def _amplified_difference(reference: Image.Image, comparison: Image.Image) -> Image.Image:
	difference = np.abs(
		np.asarray(reference, dtype=np.int16)
		- np.asarray(comparison, dtype=np.int16))
	amplified = np.clip(difference * 16, 0, 255).astype(np.uint8)
	return Image.fromarray(amplified, mode="RGB")


def _write_transform_proof(
		priors: dict[str, Image.Image],
		finals: dict[str, Image.Image],
		path: Path,
) -> None:
	cell_size = (320, 180)
	header = 78
	label_height = 38
	columns = 4
	rows = 2
	canvas = Image.new(
		"RGB",
		(columns * cell_size[0], header + rows * (cell_size[1] + label_height)),
		"#f4f1ff")
	draw = ImageDraw.Draw(canvas)
	draw.text(
		(16, 10),
		"MAIN HALL REDRAW - WHOLE-CANVAS 2K CONTENT-INVARIANCE OVERLAY",
		font=_font(21, bold=True), fill="#302a68")
	draw.text(
		(16, 40),
		"Overlay: accepted 2048 prior in red; final reduced to prior size in cyan; gray = alignment",
		font=_font(15), fill="#514784")
	for row, label in enumerate(("A", "B")):
		prior = priors[label]
		final = finals[label]
		back = final.resize(prior.size, Image.Resampling.LANCZOS)
		images = (
			("accepted prior 2048x1152", prior),
			(f"final {FINAL_SCREEN_SIZE[0]}x{FINAL_SCREEN_SIZE[1]}", final),
			("red/cyan alignment overlay", _color_overlay(prior, back)),
			("absolute difference x16", _amplified_difference(prior, back)),
		)
		for column, (caption, image) in enumerate(images):
			preview = image.resize(cell_size, Image.Resampling.LANCZOS)
			x = column * cell_size[0]
			y = header + row * (cell_size[1] + label_height)
			canvas.paste(preview, (x, y))
			draw.rectangle(
				(x, y, x + cell_size[0] - 1, y + cell_size[1] - 1),
				outline="#d4af48", width=2)
			draw.text(
				(x + 8, y + cell_size[1] + 8),
				f"Screen {label}: {caption}",
				font=_font(13), fill="#403977")
	_save_png(canvas, path)


def _write_grid_proof(panorama: Image.Image, path: Path) -> None:
	preview_size = (1820, 512)
	header = 72
	preview = panorama.resize(preview_size, Image.Resampling.LANCZOS)
	canvas = Image.new("RGB", (preview.width, preview.height + header), "#f4f1ff")
	canvas.paste(preview, (0, header))
	draw = ImageDraw.Draw(canvas)
	draw.text(
		(16, 9),
		f"MAIN HALL REDRAW - {PANORAMA_SIZE[0]}x{PANORAMA_SIZE[1]} LOSSLESS 2x8 RUNTIME GRID",
		font=_font(21, bold=True), fill="#302a68")
	draw.text(
		(16, 39),
		"Gold = tile boundaries | Magenta = exact playable-screen boundary after column 3",
		font=_font(15), fill="#514784")
	x_bounds = _bounds(COLUMN_WIDTHS)
	for index, x_position in enumerate(x_bounds[1:-1], start=1):
		x = round(x_position * preview.width / PANORAMA_SIZE[0])
		is_screen = index == SCREEN_BOUNDARY_COLUMN + 1
		draw.line(
			(x, header, x, canvas.height - 1),
			fill="#ff42cf" if is_screen else "#e7b63f",
			width=4 if is_screen else 2)
	y = header + round(ROW_HEIGHTS[0] * preview.height / PANORAMA_SIZE[1])
	draw.line((0, y, preview.width - 1, y), fill="#e7b63f", width=2)
	_save_png(canvas, path)


def _write_seam_proof(panorama: Image.Image, path: Path) -> None:
	x_bounds = _bounds(COLUMN_WIDTHS)
	panel_size = (280, 340)
	header = 76
	caption_height = 34
	canvas = Image.new(
		"RGB",
		(4 * panel_size[0], header + 2 * (panel_size[1] + caption_height) + 86),
		"#f4f1ff")
	draw = ImageDraw.Draw(canvas)
	draw.text(
		(16, 9), "MAIN HALL REDRAW - ALL RENDER TILE SEAMS",
		font=_font(21, bold=True), fill="#302a68")
	draw.text(
		(16, 39),
		"Full-height crops; magenta is the independent A/B join, gold seams are lossless subdivisions",
		font=_font(14), fill="#514784")
	for index, x_position in enumerate(x_bounds[1:-1]):
		row = index // 4
		column = index % 4
		crop = panorama.crop((x_position - 64, 0, x_position + 64, panorama.height))
		preview = crop.resize(panel_size, Image.Resampling.LANCZOS)
		x = column * panel_size[0]
		y = header + row * (panel_size[1] + caption_height)
		canvas.paste(preview, (x, y))
		is_screen = x_position == SCREEN_BOUNDARY_X
		draw.line(
			(x + panel_size[0] // 2, y, x + panel_size[0] // 2, y + panel_size[1] - 1),
			fill="#ff42cf" if is_screen else "#e7b63f", width=3)
		draw.text(
			(x + 8, y + panel_size[1] + 7),
			f"x={x_position}" + ("  SCREEN A/B" if is_screen else ""),
			font=_font(14, bold=is_screen), fill="#403977")
	horizontal = panorama.crop((0, 960, panorama.width, 1088))
	horizontal_preview = horizontal.resize((canvas.width, 72), Image.Resampling.LANCZOS)
	y = canvas.height - horizontal_preview.height
	canvas.paste(horizontal_preview, (0, y))
	draw.line((0, y + 36, canvas.width - 1, y + 36), fill="#e7b63f", width=3)
	_save_png(canvas, path)


def _write_reconstruction_proof(
		source: Image.Image,
		reconstruction: Image.Image,
		path: Path,
) -> None:
	preview_size = (1456, 410)
	header = 58
	caption = 28
	canvas = Image.new(
		"RGB", (preview_size[0], header + 3 * (preview_size[1] + caption)), "#f4f1ff")
	draw = ImageDraw.Draw(canvas)
	draw.text(
		(16, 10), "SOURCE / 16-TILE RECONSTRUCTION / ABSOLUTE DIFFERENCE",
		font=_font(20, bold=True), fill="#302a68")
	difference = ImageChops.difference(source, reconstruction)
	for index, (label, image) in enumerate((
			(f"final stitched {PANORAMA_SIZE[0]}x{PANORAMA_SIZE[1]} source", source),
			("2x8 reconstruction", reconstruction),
			("absolute pixel difference (black = exact)", difference))):
		y = header + index * (preview_size[1] + caption)
		preview = image.resize(
			preview_size,
			Image.Resampling.NEAREST if index == 2 else Image.Resampling.LANCZOS)
		canvas.paste(preview, (0, y))
		draw.text((12, y + preview_size[1] + 5), label, font=_font(14), fill="#514784")
	_save_png(canvas, path)


def _audit(arguments: argparse.Namespace) -> dict[str, Any]:
	natives = {
		"A": _load_rgb(arguments.native_a, NATIVE_SIZE),
		"B": _load_rgb(arguments.native_b, NATIVE_SIZE),
	}
	priors = {
		"A": _load_rgb(arguments.prior_a, PRIOR_SIZE),
		"B": _load_rgb(arguments.prior_b, PRIOR_SIZE),
	}
	finals = {
		"A": _load_rgb(arguments.final_a, FINAL_SCREEN_SIZE),
		"B": _load_rgb(arguments.final_b, FINAL_SCREEN_SIZE),
	}
	panorama = _load_rgb(arguments.panorama, PANORAMA_SIZE)
	with arguments.build_manifest.open("r", encoding="utf-8") as stream:
		build_manifest = json.load(stream)

	rederived_prior_exact: dict[str, bool] = {}
	rederived_final_exact: dict[str, bool] = {}
	content_metrics: dict[str, Any] = {}
	for label in ("A", "B"):
		rederived_prior = natives[label].resize(PRIOR_SIZE, Image.Resampling.LANCZOS)
		rederived_final = priors[label].resize(FINAL_SCREEN_SIZE, Image.Resampling.LANCZOS)
		rederived_prior_exact[label] = _pixel_equal(rederived_prior, priors[label])
		rederived_final_exact[label] = _pixel_equal(rederived_final, finals[label])
		content_metrics[label] = _content_metrics(priors[label], finals[label])

	expected_panorama = Image.new("RGB", PANORAMA_SIZE)
	expected_panorama.paste(finals["A"], (0, 0))
	expected_panorama.paste(finals["B"], (SCREEN_BOUNDARY_X, 0))
	panorama_exact_stitch = _pixel_equal(expected_panorama, panorama)

	x_bounds = _bounds(COLUMN_WIDTHS)
	y_bounds = _bounds(ROW_HEIGHTS)
	reconstruction = Image.new("RGB", PANORAMA_SIZE)
	tile_records: list[dict[str, Any]] = []
	all_tile_sizes_exact = True
	all_tiles_within_limit = True
	for row in range(ROWS):
		for column in range(COLUMNS):
			rectangle = (
				x_bounds[column], y_bounds[row],
				x_bounds[column + 1], y_bounds[row + 1])
			expected_size = (
				COLUMN_WIDTHS[column], ROW_HEIGHTS[row])
			tile_path = arguments.tile_dir / (
				f"{arguments.prefix}_r{row}_c{column}.png")
			tile = _load_rgb(tile_path, expected_size)
			reconstruction.paste(tile, (rectangle[0], rectangle[1]))
			size_exact = tile.size == expected_size
			within_limit = max(tile.size) <= 1024
			all_tile_sizes_exact = all_tile_sizes_exact and size_exact
			all_tiles_within_limit = all_tiles_within_limit and within_limit
			tile_records.append({
				"row": row,
				"column": column,
				"path": _portable_path(tile_path),
				"dimensions": list(tile.size),
				"expected_dimensions": list(expected_size),
				"file_sha256": _sha256(tile_path),
				"pixel_sha256": _pixel_sha256(tile),
				"panorama_rectangle": list(rectangle),
				"dimensions_exact": size_exact,
				"long_edge_within_1024_limit": within_limit,
			})

	reconstruction_exact = _pixel_equal(panorama, reconstruction)
	difference_array = np.asarray(
		ImageChops.difference(panorama, reconstruction), dtype=np.uint8)
	different_channel_count = int(np.count_nonzero(difference_array))
	maximum_channel_difference = int(difference_array.max())

	manifest_tile_claims = {
		(int(record["row"]), int(record["column"])): record
		for record in build_manifest.get("tiles", [])}
	manifest_chain_claims_match = all(
		build_manifest.get("transform_chains", {}).get(label, {}).get("native", {}).get(
			"file_sha256") == _sha256(
				arguments.native_a if label == "A" else arguments.native_b)
		and build_manifest.get("transform_chains", {}).get(label, {}).get("prior", {}).get(
			"file_sha256") == _sha256(
				arguments.prior_a if label == "A" else arguments.prior_b)
		and build_manifest.get("transform_chains", {}).get(label, {}).get("final", {}).get(
			"file_sha256") == _sha256(
				arguments.final_a if label == "A" else arguments.final_b)
		for label in ("A", "B"))
	manifest_claims_match = (
		build_manifest.get("script", {}).get("sha256") == _sha256(Path(__file__))
		and manifest_chain_claims_match
		and build_manifest.get("panorama", {}).get("file_sha256") == _sha256(arguments.panorama)
		and len(manifest_tile_claims) == ROWS * COLUMNS
		and all(
			manifest_tile_claims.get((record["row"], record["column"]), {}).get(
				"file_sha256") == record["file_sha256"]
			for record in tile_records)
		and build_manifest.get("runtime_grid", {}).get("column_widths") == list(COLUMN_WIDTHS)
		and build_manifest.get("runtime_grid", {}).get("row_heights") == list(ROW_HEIGHTS)
	)
	expected_tile_names = {
		f"{arguments.prefix}_r{row}_c{column}.png"
		for row in range(ROWS) for column in range(COLUMNS)}
	actual_tile_names = {
		path.name for path in arguments.tile_dir.glob(
			f"{arguments.prefix}_r*_c*.png")}

	vertical_seams = []
	for x_position in x_bounds[1:-1]:
		vertical_seams.append(_vertical_seam_metrics(
			panorama,
			x_position,
			("independently_authored_screen_join"
				if x_position == SCREEN_BOUNDARY_X
				else "lossless_intra_screen_tile_boundary")))
	horizontal_seam = _horizontal_seam_metrics(panorama, ROW_HEIGHTS[0])
	central_seam = next(
		record for record in vertical_seams
		if record["coordinate"] == SCREEN_BOUNDARY_X)
	central_seam_pass = (
		central_seam["edge_rgb_mean_absolute_error"]
		<= arguments.max_central_edge_mae
		and central_seam["band_mean_rgb_euclidean_delta"]
		<= arguments.max_central_band_delta)

	_write_transform_proof(priors, finals, arguments.transform_proof)
	_write_grid_proof(panorama, arguments.grid_proof)
	_write_seam_proof(panorama, arguments.seam_proof)
	_write_reconstruction_proof(panorama, reconstruction, arguments.reconstruction_proof)

	ratio_steps = {
		"native_to_prior": _ratio_step(
			NATIVE_SIZE, PRIOR_SIZE, "accepted native to prior production"),
		"prior_to_final": _ratio_step(
			PRIOR_SIZE, FINAL_SCREEN_SIZE, "prior production to strict per-screen 2K"),
		"native_to_final_cumulative": _ratio_step(
			NATIVE_SIZE, FINAL_SCREEN_SIZE,
			"accepted native to strict per-screen 2K cumulative ratio check"),
	}

	checks = {
		"native_to_prior_screen_a_rederives_pixel_exactly": rederived_prior_exact["A"],
		"native_to_prior_screen_b_rederives_pixel_exactly": rederived_prior_exact["B"],
		"prior_to_final_screen_a_rederives_pixel_exactly": rederived_final_exact["A"],
		"prior_to_final_screen_b_rederives_pixel_exactly": rederived_final_exact["B"],
		"native_to_prior_within_one_pixel_ratio_rounding": ratio_steps[
			"native_to_prior"]["within_one_pixel_rounding_tolerance"],
		"prior_to_final_within_one_pixel_ratio_rounding": ratio_steps[
			"prior_to_final"]["within_one_pixel_rounding_tolerance"],
		"native_to_final_cumulative_within_one_pixel_ratio_rounding": ratio_steps[
			"native_to_final_cumulative"]["within_one_pixel_rounding_tolerance"],
		"each_playable_screen_long_edge_at_least_2048": (
			FINAL_SCREEN_SIZE[0] >= 2048 and FINAL_SCREEN_SIZE[1] >= 2048),
		"panorama_is_exact_lossless_stitch": panorama_exact_stitch,
		"tile_count_is_16": len(tile_records) == 16,
		"runtime_tile_directory_has_exact_expected_set": (
			actual_tile_names == expected_tile_names),
		"tile_dimensions_match_rectangles": all_tile_sizes_exact,
		"all_runtime_tiles_within_1024_long_edge": all_tiles_within_limit,
		"screen_boundary_is_exact_after_column_3": (
			x_bounds[SCREEN_BOUNDARY_COLUMN + 1] == SCREEN_BOUNDARY_X),
		"tiles_reconstruct_panorama_pixel_exactly": reconstruction_exact,
		"reconstruction_has_zero_changed_channels": different_channel_count == 0,
		"reconstruction_maximum_channel_difference_is_zero": maximum_channel_difference == 0,
		"build_manifest_claims_match_outputs": manifest_claims_match,
		"screen_a_content_invariance_passes": content_metrics["A"]["passes"],
		"screen_b_content_invariance_passes": content_metrics["B"]["passes"],
		"independently_authored_center_seam_within_review_gate": central_seam_pass,
	}
	blocking_pass = all(bool(value) for value in checks.values())
	audit = {
		"schema": 1,
		"pipeline": "castle_main_hall_redraw_strict_per_screen_2k_audit",
		"decision_date": "2026-08-04",
		"audit_method": "independent output revalidation",
		"build_manifest": {
			"path": _portable_path(arguments.build_manifest),
			"sha256": _sha256(arguments.build_manifest),
		},
		"ratio_steps": ratio_steps,
		"content_invariance": content_metrics,
		"panorama": _record_image(arguments.panorama, panorama),
		"runtime_grid": {
			"rows": ROWS,
			"columns": COLUMNS,
			"column_widths": list(COLUMN_WIDTHS),
			"row_heights": list(ROW_HEIGHTS),
			"column_bounds": x_bounds,
			"row_bounds": y_bounds,
			"screen_boundary_after_column": SCREEN_BOUNDARY_COLUMN,
			"screen_boundary_x": SCREEN_BOUNDARY_X,
			"tiles": tile_records,
		},
		"reconstruction": {
			"pixel_exact": reconstruction_exact,
			"different_channel_count": different_channel_count,
			"maximum_channel_difference": maximum_channel_difference,
			"source_pixel_sha256": _pixel_sha256(panorama),
			"reconstruction_pixel_sha256": _pixel_sha256(reconstruction),
		},
		"seams": vertical_seams + [horizontal_seam],
		"center_seam_gate": {
			"coordinate": SCREEN_BOUNDARY_X,
			"maximum_edge_mean_absolute_error": arguments.max_central_edge_mae,
			"maximum_band_mean_rgb_delta": arguments.max_central_band_delta,
			"passes": central_seam_pass,
		},
		"proofs": {
			"transform_overlay": {
				"path": _portable_path(arguments.transform_proof),
				"sha256": _sha256(arguments.transform_proof),
			},
			"grid": {
				"path": _portable_path(arguments.grid_proof),
				"sha256": _sha256(arguments.grid_proof),
			},
			"seams": {
				"path": _portable_path(arguments.seam_proof),
				"sha256": _sha256(arguments.seam_proof),
			},
			"reconstruction": {
				"path": _portable_path(arguments.reconstruction_proof),
				"sha256": _sha256(arguments.reconstruction_proof),
			},
		},
		"checks": checks,
		"blocking_pass": blocking_pass,
	}
	arguments.audit_manifest.parent.mkdir(parents=True, exist_ok=True)
	arguments.audit_manifest.write_text(
		json.dumps(audit, indent=2) + "\n", encoding="utf-8")
	if not blocking_pass:
		failed = [name for name, passed in checks.items() if not passed]
		raise RuntimeError(f"Blocking 2K redraw audit failed: {', '.join(failed)}")
	return audit


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--native-a", required=True, type=Path)
	parser.add_argument("--native-b", required=True, type=Path)
	parser.add_argument("--prior-a", required=True, type=Path)
	parser.add_argument("--prior-b", required=True, type=Path)
	parser.add_argument("--final-a", required=True, type=Path)
	parser.add_argument("--final-b", required=True, type=Path)
	parser.add_argument("--panorama", required=True, type=Path)
	parser.add_argument("--tile-dir", required=True, type=Path)
	parser.add_argument("--build-manifest", required=True, type=Path)
	parser.add_argument("--audit-manifest", required=True, type=Path)
	parser.add_argument("--transform-proof", required=True, type=Path)
	parser.add_argument("--grid-proof", required=True, type=Path)
	parser.add_argument("--seam-proof", required=True, type=Path)
	parser.add_argument("--reconstruction-proof", required=True, type=Path)
	parser.add_argument("--prefix", default="main_hall_room_led")
	parser.add_argument("--max-central-edge-mae", type=float, default=45.0)
	parser.add_argument("--max-central-band-delta", type=float, default=60.0)
	parser.add_argument("--audit-only", action="store_true")
	arguments = parser.parse_args()

	if not arguments.audit_only:
		_build(arguments)
	audit = _audit(arguments)
	print(json.dumps({
		"blocking_pass": audit["blocking_pass"],
		"final_screen_dimensions": list(FINAL_SCREEN_SIZE),
		"panorama_dimensions": list(PANORAMA_SIZE),
		"runtime_grid": [ROWS, COLUMNS],
		"runtime_tile_count": ROWS * COLUMNS,
		"screen_boundary_x": SCREEN_BOUNDARY_X,
		"reconstruction": audit["reconstruction"],
		"content_invariance": audit["content_invariance"],
		"center_seam_gate": audit["center_seam_gate"],
		"build_manifest": _portable_path(arguments.build_manifest),
		"audit_manifest": _portable_path(arguments.audit_manifest),
	}, indent=2))


if __name__ == "__main__":
	main()
