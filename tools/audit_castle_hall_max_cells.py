"""Audit independently generated Main Hall 2x4 fidelity candidates.

The candidates are evidence only. This script never promotes or modifies
runtime art: it records native dimensions and hashes, compares each candidate
against its approved low-resolution crop, and measures all internal seams.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "audit" / "castle_sprite3d"
SOURCE_DIR = AUDIT_DIR / "main_hall_2x4_tiles_preview"
CANDIDATE_DIR = AUDIT_DIR / "main_hall_2x4_max_native_candidates"
MANIFEST_PATH = AUDIT_DIR / "main_hall_2x4_max_native_audit.json"
CONTACT_PATH = AUDIT_DIR / "main_hall_2x4_REJECTED_max_native_contact.png"
OVERLAY_PATH = AUDIT_DIR / "main_hall_2x4_REJECTED_invariance.png"
SEAM_PATH = AUDIT_DIR / "main_hall_2x4_REJECTED_independent_cell_seams.png"
REFERENCE_RATIO = 16.0 / 9.0
REQUIRED_LONG_EDGE = 2048
CELLS = [(row, column) for row in range(2) for column in range(4)]

MANUAL_FINDINGS = {
	"r0c0": (
		"Rejected: the small Opera crop-edge fragment became a major half-door "
		"and arch; door/column geometry shifted."),
	"r0c1": (
		"Rejected: the Opera edge, columns, and door spacing were normalized "
		"instead of preserved."),
	"r0c2": (
		"Rejected: Playroom/Craft signs and arches were enlarged and centered; "
		"upper-wall landmarks drifted."),
	"r0c3": (
		"Rejected: Pool/Bath and throne architecture moved and changed scale; "
		"chandelier count and placement drifted."),
	"r1c0": (
		"Rejected: courtyard, furnishings, fountain, and Opera edge were "
		"recomposed rather than restored."),
	"r1c1": (
		"Rejected: Roshan's identity, pose, outfit, and scale changed; room "
		"furnishings and corridor proportions also drifted."),
	"r1c2": (
		"Rejected: doors and craft/play props were recomposed; the fountain "
		"became a new design and changed size."),
	"r1c3": (
		"Rejected: Pool/Bath dressing and throne stair were redesigned and "
		"repositioned."),
}

GENERATOR_FILES = {
	"r0c0": "call_Qusr2wxAOp3l7NvZiugKLtE8.png",
	"r0c1": "call_lamAcqzqvGVPzsu1bPmkGpIH.png",
	"r0c2": "call_pTrBftBaXQ4J5irv5t9t6AVH.png",
	"r0c3": "call_JrwzYVxNSNCx43CqtfkLVOp0.png",
	"r1c0": "call_2VcR2JD65cx86GRMFpmuYq2o.png",
	"r1c1": "call_8ZXQUEuS8MnY5qpGU22FR4Cj.png",
	"r1c2": "call_zmHcMau6WyVesxcjxgUZ7Qz1.png",
	"r1c3": "call_UJej1fxFs1hK4u13czzEJaiq.png",
}
GENERATOR_DIR = (
	"C:/Users/Peter/.codex/generated_images/"
	"019fa1a6-6274-77b2-bb27-38aa32e6e4dd")


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _ratio_pixel_delta(width: int, height: int) -> float:
	return min(
		abs(height - width / REFERENCE_RATIO),
		abs(width - height * REFERENCE_RATIO))


def _dhash(image: Image.Image) -> np.ndarray:
	small = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
	array = np.asarray(small, dtype=np.int16)
	return array[:, 1:] > array[:, :-1]


def _normalized_candidate(
		source: Image.Image, candidate: Image.Image) -> tuple[Image.Image, dict[str, float]]:
	normalized = candidate.convert("RGB").resize(
		source.size, Image.Resampling.LANCZOS)
	source_rgb = source.convert("RGB")
	source_array = np.asarray(source_rgb, dtype=np.float32)
	candidate_array = np.asarray(normalized, dtype=np.float32)
	mae = float(np.abs(source_array - candidate_array).mean())
	source_edges = np.asarray(
		source_rgb.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32)
	candidate_edges = np.asarray(
		normalized.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32)
	edge_mae = float(np.abs(source_edges - candidate_edges).mean())
	hash_hamming = int(np.count_nonzero(
		_dhash(source_rgb) != _dhash(normalized)))
	return normalized, {
		"normalized_rgb_mean_abs_error": round(mae, 4),
		"normalized_edge_mean_abs_error": round(edge_mae, 4),
		"dhash_hamming_64": hash_hamming,
	}


def _label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str) -> None:
	draw.text(xy, text, fill=(35, 31, 91), font=ImageFont.load_default())


def _build_contact(
		images: dict[str, Image.Image], path: Path, title: str) -> None:
	cell_width = 418
	cell_height = 235
	label_height = 24
	canvas = Image.new(
		"RGB", (cell_width * 4, (cell_height + label_height) * 2 + 34),
		(246, 244, 255))
	draw = ImageDraw.Draw(canvas)
	_label(draw, (10, 10), title)
	for row, column in CELLS:
		cell_id = f"r{row}c{column}"
		preview = images[cell_id].convert("RGB").resize(
			(cell_width, cell_height), Image.Resampling.LANCZOS)
		x_pos = column * cell_width
		y_pos = 34 + row * (cell_height + label_height)
		canvas.paste(preview, (x_pos, y_pos))
		_label(draw, (x_pos + 6, y_pos + cell_height + 5), cell_id)
	canvas.save(path, optimize=True)


def _build_overlay(
		sources: dict[str, Image.Image],
		normalized: dict[str, Image.Image]) -> None:
	overlays: dict[str, Image.Image] = {}
	for row, column in CELLS:
		cell_id = f"r{row}c{column}"
		source = sources[cell_id].convert("RGB")
		candidate = normalized[cell_id].convert("RGB")
		overlay = Image.blend(source, candidate, 0.5)
		difference = ImageChops.difference(source, candidate)
		# A narrow magenta strip at the bottom makes high-difference areas
		# visible without hiding the 50/50 landmark ghosting above.
		difference = difference.convert("L").convert("RGB")
		overlay.paste(difference.crop(
			(0, source.height - 48, source.width, source.height)),
			(0, source.height - 48))
		overlays[cell_id] = overlay
	_build_contact(
		overlays, OVERLAY_PATH,
		"50/50 source/candidate landmark overlay; bottom strip = difference")


def _boundary_mae(
		first: Image.Image, second: Image.Image, direction: str) -> float:
	first_array = np.asarray(first.convert("RGB"), dtype=np.float32)
	second_array = np.asarray(second.convert("RGB"), dtype=np.float32)
	if direction == "vertical":
		return float(np.abs(first_array[:, -1] - second_array[:, 0]).mean())
	return float(np.abs(first_array[-1, :] - second_array[0, :]).mean())


def _seam_records(
		sources: dict[str, Image.Image],
		normalized: dict[str, Image.Image]) -> list[dict[str, object]]:
	records: list[dict[str, object]] = []
	pairs: list[tuple[str, str, str]] = []
	for row in range(2):
		for column in range(3):
			pairs.append((
				f"r{row}c{column}", f"r{row}c{column + 1}", "vertical"))
	for column in range(4):
		pairs.append((f"r0c{column}", f"r1c{column}", "horizontal"))
	for first, second, direction in pairs:
		source_mae = _boundary_mae(sources[first], sources[second], direction)
		candidate_mae = _boundary_mae(
			normalized[first], normalized[second], direction)
		ratio = candidate_mae / max(source_mae, 0.001)
		records.append({
			"between": [first, second],
			"direction": direction,
			"source_boundary_mae": round(source_mae, 4),
			"candidate_boundary_mae": round(candidate_mae, 4),
			"candidate_to_source_ratio": round(ratio, 4),
			"pass": candidate_mae <= source_mae * 2.5 + 5.0,
		})
	return records


def _build_seam_proof(normalized: dict[str, Image.Image]) -> None:
	tile_width = 418
	tile_height = 235
	grid = Image.new("RGB", (tile_width * 4, tile_height * 2), (255, 0, 255))
	for row, column in CELLS:
		cell_id = f"r{row}c{column}"
		tile = normalized[cell_id].resize(
			(tile_width, tile_height), Image.Resampling.LANCZOS)
		grid.paste(tile, (column * tile_width, row * tile_height))
	canvas = Image.new("RGB", (grid.width, grid.height + 34), (246, 244, 255))
	canvas.paste(grid, (0, 34))
	draw = ImageDraw.Draw(canvas)
	_label(draw, (10, 10), "Independent max-native candidates reconstructed at shared edges")
	for column in range(1, 4):
		x_pos = column * tile_width
		draw.line((x_pos, 34, x_pos, canvas.height), fill=(255, 0, 255), width=1)
	draw.line(
		(0, 34 + tile_height, canvas.width, 34 + tile_height),
		fill=(255, 0, 255), width=1)
	canvas.save(SEAM_PATH, optimize=True)


def main() -> None:
	sources: dict[str, Image.Image] = {}
	candidates: dict[str, Image.Image] = {}
	normalized: dict[str, Image.Image] = {}
	cell_records: list[dict[str, object]] = []
	for row, column in CELLS:
		cell_id = f"r{row}c{column}"
		file_cell_id = f"r{row}_c{column}"
		source_path = SOURCE_DIR / f"main_hall_bg_{file_cell_id}.png"
		candidate_path = (
			CANDIDATE_DIR / f"main_hall_bg_{file_cell_id}_max.png")
		source = Image.open(source_path).convert("RGB")
		candidate = Image.open(candidate_path).convert("RGB")
		normalized_image, metrics = _normalized_candidate(source, candidate)
		sources[cell_id] = source
		candidates[cell_id] = candidate
		normalized[cell_id] = normalized_image
		long_edge = max(candidate.size)
		ratio_delta = _ratio_pixel_delta(*candidate.size)
		cell_records.append({
			"id": cell_id,
			"source_path": source_path.relative_to(ROOT).as_posix(),
			"source_dimensions": list(source.size),
			"source_sha256": _sha256(source_path),
			"candidate_path": candidate_path.relative_to(ROOT).as_posix(),
			"generator_output_path": (
				f"{GENERATOR_DIR}/{GENERATOR_FILES[cell_id]}"),
			"candidate_dimensions": list(candidate.size),
			"candidate_aspect_ratio": round(
				candidate.width / candidate.height, 9),
			"candidate_ratio_pixel_delta": round(ratio_delta, 6),
			"candidate_sha256": _sha256(candidate_path),
			"native_long_edge": long_edge,
			"native_minimum_2048_pass": long_edge >= REQUIRED_LONG_EDGE,
			"ratio_rounding_tolerance_pass": ratio_delta <= 1.0,
			"manual_fidelity_finding": MANUAL_FINDINGS[cell_id],
			"accepted_for_runtime": False,
			**metrics,
		})

	seams = _seam_records(sources, normalized)
	_build_contact(
		candidates, CONTACT_PATH,
		"Main Hall 2x4 built-in ImageGen maximum-native candidates")
	_build_overlay(sources, normalized)
	_build_seam_proof(normalized)
	manifest = {
		"schema": 1,
		"generator_path": "built-in image_gen.imagegen edit, one call per cell",
		"generation_policy": {
			"requested": (
				"maximum native landscape raster; exact 16:9 cell fidelity; "
				"no upscaling, interpolation, crop, padding, or redesign"),
			"native_minimum_long_edge": REQUIRED_LONG_EDGE,
			"ratio_rounding_tolerance_pixels": 1.0,
		},
		"result": {
			"accepted_cell_count": 0,
			"runtime_wiring_changed": False,
			"decision": (
				"All candidates rejected: every native long edge is below "
				"2048 and every cell has material composition drift."),
		},
		"cells": cell_records,
		"seams": seams,
		"all_seams_pass": all(bool(record["pass"]) for record in seams),
		"proofs": {
			"contact": CONTACT_PATH.relative_to(ROOT).as_posix(),
			"invariance_overlay": OVERLAY_PATH.relative_to(ROOT).as_posix(),
			"seam_reconstruction": SEAM_PATH.relative_to(ROOT).as_posix(),
		},
	}
	MANIFEST_PATH.write_text(
		json.dumps(manifest, indent=2, sort_keys=True) + "\n",
		encoding="utf-8")
	print(json.dumps({
		"manifest": str(MANIFEST_PATH.relative_to(ROOT)),
		"candidate_dimensions": sorted({
			tuple(record["candidate_dimensions"]) for record in cell_records}),
		"accepted_cell_count": 0,
		"seams_passed": sum(bool(record["pass"]) for record in seams),
		"seams_total": len(seams),
	}, indent=2))


if __name__ == "__main__":
	main()
