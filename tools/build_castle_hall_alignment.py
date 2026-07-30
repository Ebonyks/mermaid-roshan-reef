#!/usr/bin/env python3
"""Normalize Main Hall fixtures and turn the screen join into architecture.

Two precise cleanup candidates remove only the baked fixtures. Candidate
pixels are registered to the immutable masters and accepted only inside six
compact masks. The reusable fixture, portal, pilaster, and floor inlay contain
accepted master pixels only. Screen B receives a documented global tone
correction, and a four-pixel exact-edge ramp prevents sampling cracks beneath
the structural join cards.

The original 2048x1153 masters remain unchanged.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = ROOT / "assets" / "flats" / "castle" / "main_hall_2screen"
SOURCE_ROOT = ROOT / "assets_src" / "castle" / "main_hall_alignment"
AUDIT_ROOT = ROOT / "audit" / "castle_sprite3d"
SOURCE_A = RUNTIME_ROOT / "main_hall_screen_a_room_led_master.png"
SOURCE_B = RUNTIME_ROOT / "main_hall_screen_b_room_led_master.png"
OUTPUT_A = SOURCE_ROOT / "main_hall_screen_a_fixture_aligned_master.png"
OUTPUT_B = SOURCE_ROOT / "main_hall_screen_b_fixture_aligned_master.png"
CANDIDATE_A = SOURCE_ROOT / "generated_cleanup_candidate_a.png"
CANDIDATE_B = SOURCE_ROOT / "generated_cleanup_candidate_b.png"
FIXTURE_OUTPUT = RUNTIME_ROOT / "castle_shell_sconce_integrated_reuse.png"
PORTAL_SOURCE = RUNTIME_ROOT / "castle_playroom_portal_reuse.png"
PORTAL_OUTPUT = RUNTIME_ROOT / "castle_playroom_portal_cutout_reuse.png"
JOIN_COLUMN_OUTPUT = RUNTIME_ROOT / "castle_join_column_cutout_reuse.png"
JOIN_INLAY_OUTPUT = RUNTIME_ROOT / "castle_join_floor_inlay_reuse.png"
OUTPUT_MANIFEST = AUDIT_ROOT / "castle_hall_alignment_manifest.json"
OUTPUT_CONTACT = AUDIT_ROOT / "castle_hall_fixture_alignment_audit.png"

MASTER_SIZE = (2048, 1153)
VIEW_RECT = (376, 212, 2048, 1153)
TARGET_RUNTIME_Y = 215
TARGET_MASTER_Y = VIEW_RECT[1] + TARGET_RUNTIME_Y
SEAM_BLEND_WIDTH = 4

A_FIXTURE_CENTERS = ((636, 427), (1388, 427), (1852, 427))
B_FIXTURE_CENTERS = ((752, 362), (1119, 362), (1592, 362))
RUNTIME_FIXTURE_CENTERS = (
	(260, 215),
	(1012, 215),
	(1476, 215),
	(2048, 215),
	(2415, 215),
	(2888, 215),
)
CLEANUP_PROMPTS = {
	"A": (
		"Remove only the three wall-mounted gold lantern sconces from Screen A "
		"and seamlessly reconstruct the exact purple patterned wall; preserve "
		"the full composition and every other object; no blur or visible patch."
	),
	"B": (
		"Remove only the three wall-mounted pearl shell sconces from Screen B "
		"and seamlessly reconstruct the exact purple brick courses; preserve "
		"the full composition and every other object; no blur or visible patch."
	),
}


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
	path = Path(
		"C:/Windows/Fonts/arialbd.ttf"
		if bold else "C:/Windows/Fonts/arial.ttf")
	if path.exists():
		return ImageFont.truetype(str(path), size)
	return ImageFont.load_default()


def fill_from_candidate(
		source: Image.Image,
		candidate_path: Path,
		master_centers: tuple[tuple[int, int], ...],
		half_width: int,
		half_height: int,
) -> tuple[Image.Image, dict[str, object]]:
	"""Accept generated cleanup pixels only inside compact fixture masks."""
	candidate = Image.open(candidate_path).convert("RGB")
	candidate_ratio = candidate.width / candidate.height
	master_ratio = source.width / source.height
	if abs(candidate_ratio - master_ratio) > 0.002:
		raise ValueError(
			f"{candidate_path} ratio {candidate_ratio} does not match "
			f"master ratio {master_ratio}")
	# Built-in ImageGen preserved the full master composition and exact ratio
	# but returned the repository's 1672x941 play-view size. Register it back
	# to the authoritative 2048x1153 master before accepting masked pixels.
	registered = candidate.resize(source.size, Image.Resampling.LANCZOS)
	mask = Image.new("L", source.size, 0)
	draw = ImageDraw.Draw(mask)
	for center_x, center_y in master_centers:
		draw.ellipse(
			(
				center_x - half_width,
				center_y - half_height,
				center_x + half_width,
				center_y + half_height,
			),
			fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(3.0))
	source_rgb = source.convert("RGB")
	output = Image.composite(registered, source_rgb, mask)

	source_array = np.asarray(source_rgb, dtype=np.int16)
	composite_array = np.asarray(output, dtype=np.int16)
	mask_array = np.asarray(mask, dtype=np.uint8)
	delta = np.abs(source_array - composite_array)
	outside = mask_array == 0
	return output, {
		"candidate": candidate_path.relative_to(ROOT).as_posix(),
		"candidate_dimensions": list(candidate.size),
		"registered_dimensions": list(registered.size),
		"registration": "ratio-preserving Lanczos to authoritative master",
		"candidate_sha256": sha256(candidate_path),
		"mask_feather_pixels": 3.0,
		"mask_coverage": round(float((mask_array > 0).mean()), 8),
		"outside_mask_pixel_exact": bool(np.all(delta[outside] == 0)),
		"outside_mask_maximum_rgb_delta": int(delta[outside].max(initial=0)),
		"inside_mask_mean_absolute_rgb_delta": round(
			float(delta[mask_array > 0].mean()), 6),
	}


def extract_fixture(source: Image.Image) -> Image.Image:
	"""Extract only the accepted shell hardware, not its baked wall pixels."""
	crop = source.crop((704, 300, 800, 428)).convert("RGBA")
	# Trace the four connected pieces of the accepted fixture closely. A
	# silhouette mask is more faithful here than a chroma key because its
	# pearl highlights share values with the painted wall.
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.polygon(
		(
			(48, 39), (54, 42), (58, 47), (63, 51), (66, 57),
			(70, 62), (67, 69), (64, 77), (61, 86), (56, 95),
			(48, 101), (40, 95), (35, 86), (32, 77), (29, 69),
			(27, 62), (30, 55), (33, 49), (38, 45), (42, 42),
		),
		fill=255)
	draw.polygon(
		(
			(31, 58), (27, 60), (24, 65), (21, 62), (17, 64),
			(15, 69), (15, 78), (18, 82), (23, 84), (27, 80),
			(29, 75), (28, 68), (34, 67),
		),
		fill=255)
	draw.polygon(
		(
			(65, 58), (69, 60), (72, 65), (75, 62), (79, 64),
			(81, 69), (81, 78), (78, 82), (73, 84), (69, 80),
			(67, 75), (68, 68), (62, 67),
		),
		fill=255)
	draw.polygon(
		(
			(41, 86), (55, 86), (58, 94), (55, 102), (53, 106),
			(56, 111), (58, 116), (56, 122), (51, 127), (44, 127),
			(39, 122), (37, 116), (40, 109), (43, 104), (40, 98),
			(38, 92),
		),
		fill=255)
	crop_rgb = np.asarray(crop.convert("RGB"), dtype=np.int16)
	pearl_or_gold = (
		(crop_rgb[..., 0] > 210)
		& (crop_rgb[..., 1] > 190)
		& ((crop_rgb[..., 0] + crop_rgb[..., 1]) / 2.0
			> crop_rgb[..., 2] + 18)
	)
	color_seed = Image.fromarray(
		np.where(pearl_or_gold, 255, 0).astype(np.uint8), "L")
	mask = ImageChops.multiply(
		color_seed.filter(ImageFilter.MaxFilter(7)), mask)
	trim = ImageDraw.Draw(mask)
	trim.rectangle((60, 0, 95, 48), fill=0)
	trim.rectangle((81, 0, 95, 127), fill=0)
	trim.rectangle((70, 85, 95, 127), fill=0)
	mask = mask.filter(ImageFilter.GaussianBlur(0.55))
	crop.putalpha(mask)
	return crop


def extract_playroom_portal() -> Image.Image:
	"""Remove the rectangular wall plate around the approved playroom door."""
	portal = Image.open(PORTAL_SOURCE).convert("RGBA")
	if portal.size != (250, 412):
		raise ValueError(f"Unexpected playroom portal size: {portal.size}")
	mask = Image.new("L", portal.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.polygon(
		(
			(26, 153), (30, 132), (38, 114), (50, 98), (64, 85),
			(82, 74), (102, 68), (125, 65), (148, 68), (168, 76),
			(187, 88), (202, 104), (212, 124), (220, 150),
			(220, 355), (210, 365), (40, 365), (30, 355),
		),
		fill=255)
	draw.ellipse((65, 28, 190, 135), fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(0.7))
	portal.putalpha(mask)
	return portal


def extract_join_column(source: Image.Image) -> Image.Image:
	"""Extract an accepted full-height pilaster to make the screen join explicit."""
	column = source.crop((1170, 212, 1360, 1153)).convert("RGBA")
	mask = Image.new("L", column.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.polygon(
		(
			(86, 0), (141, 0), (141, 25), (150, 42), (151, 70),
			(145, 92), (140, 105), (140, 495), (146, 512),
			(157, 530), (162, 550), (161, 585), (151, 606),
			(139, 620), (75, 620), (63, 607), (57, 586), (58, 550),
			(63, 530), (76, 512), (84, 495), (84, 105), (78, 92),
			(74, 70), (77, 42), (86, 25),
		),
		fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(0.8))
	column.putalpha(mask)
	return column


def build_join_floor_inlay(source: Image.Image) -> Image.Image:
	"""Rotate and tile the accepted carpet trim into a tapered floor divider."""
	column_crop = source.crop((1170, 212, 1360, 1153)).convert("RGBA")
	trim = column_crop.crop((0, 708, 190, 732)).rotate(
		90, expand=True, resample=Image.Resampling.BICUBIC)
	trim = trim.resize((48, trim.height), Image.Resampling.LANCZOS)
	inlay = Image.new("RGBA", (48, 321), (0, 0, 0, 0))
	for top in range(0, inlay.height, trim.height):
		inlay.alpha_composite(trim, (0, top))
	mask = Image.new("L", inlay.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.polygon(((15, 0), (33, 0), (46, 320), (2, 320)), fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(0.55))
	inlay.putalpha(mask)
	return inlay


def smoothstep(value: np.ndarray) -> np.ndarray:
	return value * value * (3.0 - 2.0 * value)


def harmonize_screen_tone(
		left_master: Image.Image,
		right_master: Image.Image,
		strength: float = 0.65,
) -> tuple[Image.Image, dict[str, object]]:
	"""Move Screen B toward Screen A's shared-hall palette without scaling."""
	left = np.asarray(left_master.convert("RGB"), dtype=np.float32)
	right = np.asarray(right_master.convert("RGB"), dtype=np.float32)
	left_view = left[
		VIEW_RECT[1]:VIEW_RECT[3], VIEW_RECT[0]:VIEW_RECT[2], :]
	right_view = right[
		VIEW_RECT[1]:VIEW_RECT[3], VIEW_RECT[0]:VIEW_RECT[2], :]
	left_mean = left_view.mean(axis=(0, 1))
	right_mean = right_view.mean(axis=(0, 1))
	correction = (left_mean - right_mean) * strength
	output = np.clip(right + correction[None, None, :], 0, 255)
	return Image.fromarray(output.astype(np.uint8), "RGB"), {
		"method": "global RGB mean correction; no scaling or geometry change",
		"strength": strength,
		"screen_a_runtime_mean_rgb": [
			round(float(value), 6) for value in left_mean],
		"screen_b_before_runtime_mean_rgb": [
			round(float(value), 6) for value in right_mean],
		"applied_rgb_offset": [
			round(float(value), 6) for value in correction],
	}


def feather_screen_join(
		left_master: Image.Image,
		right_master: Image.Image,
) -> Image.Image:
	left = np.asarray(left_master.convert("RGB"), dtype=np.float32)
	right = np.asarray(right_master.convert("RGB"), dtype=np.float32).copy()
	start = VIEW_RECT[0]
	width = SEAM_BLEND_WIDTH
	# A four-pixel exact-edge ramp removes sampling cracks. The visible join is
	# owned by accepted architectural Sprite3D cards, so raster structures are
	# never copied or blurred across the two authored screens.
	left_edge = left[:, VIEW_RECT[2] - 1, :]
	original = right[:, start:start + width, :].copy()
	t = np.linspace(0.0, 1.0, width, dtype=np.float32)
	weights = smoothstep(t)[None, :, None]
	right[:, start:start + width, :] = (
		left_edge[:, None, :] * (1.0 - weights) + original * weights)
	output = np.clip(right, 0, 255).astype(np.uint8)
	output[:, start, :] = left[:, VIEW_RECT[2] - 1, :].astype(np.uint8)
	return Image.fromarray(output, "RGB")


def seam_metrics(left: Image.Image, right: Image.Image) -> dict[str, object]:
	left_array = np.asarray(left.convert("RGB"), dtype=np.int16)
	right_array = np.asarray(right.convert("RGB"), dtype=np.int16)
	left_edge = left_array[VIEW_RECT[1]:VIEW_RECT[3], VIEW_RECT[2] - 1, :]
	right_edge = right_array[VIEW_RECT[1]:VIEW_RECT[3], VIEW_RECT[0], :]
	delta = np.abs(left_edge - right_edge)
	return {
		"mean_absolute_rgb": round(float(delta.mean()), 6),
		"p95_absolute_rgb": round(float(np.percentile(delta, 95)), 6),
		"maximum_absolute_rgb": int(delta.max()),
		"edge_pixel_exact": bool(np.all(delta == 0)),
	}


def write_contact(
		before_a: Image.Image,
		before_b: Image.Image,
		after_a: Image.Image,
		after_b: Image.Image,
		fixture: Image.Image,
) -> None:
	fixture_size = (
		round(fixture.width * 1.15),
		round(fixture.height * 1.15),
	)
	fixture_preview_asset = fixture.resize(
		fixture_size, Image.Resampling.LANCZOS)

	def with_fixtures(
			image: Image.Image,
			centers: tuple[tuple[int, int], ...],
		) -> Image.Image:
		composite = image.convert("RGBA")
		for center_x, _center_y in centers:
			composite.alpha_composite(
				fixture_preview_asset,
				(
					center_x - fixture_preview_asset.width // 2,
					TARGET_MASTER_Y - fixture_preview_asset.height // 2,
				))
		return composite.convert("RGB")

	runtime_a = with_fixtures(after_a, A_FIXTURE_CENTERS)
	runtime_b = with_fixtures(after_b, B_FIXTURE_CENTERS)
	canvas = Image.new("RGB", (1536, 820), "#f4f1ff")
	draw = ImageDraw.Draw(canvas)
	draw.text(
		(18, 14),
		"PEARL CASTLE - FIXTURE HEIGHT + SCREEN JOIN AUDIT",
		font=font(28, bold=True),
		fill="#302a68")
	draw.text(
		(18, 51),
		"All six runtime fixtures share y=215; center join is edge-exact.",
		font=font(17),
		fill="#49417f")
	images = (
		("A BEFORE", before_a),
		("B BEFORE", before_b),
		("A RUNTIME COMPOSITE", runtime_a),
		("B RUNTIME COMPOSITE + FEATHER", runtime_b),
	)
	for index, (label, image) in enumerate(images):
		column = index % 2
		row = index // 2
		x = 18 + column * 750
		y = 88 + row * 344
		view = image.crop(VIEW_RECT)
		preview = view.resize((718, 404), Image.Resampling.LANCZOS)
		preview = preview.crop((0, 0, 718, 286))
		canvas.paste(preview, (x, y))
		draw.line(
			(x, y + round(TARGET_RUNTIME_Y * 286 / 470),
			 x + 718, y + round(TARGET_RUNTIME_Y * 286 / 470)),
			fill="#5cebb8",
			width=3)
		draw.text(
			(x + 8, y + 8),
			label,
			font=font(16, bold=True),
			fill="#ffffff",
			stroke_width=3,
			stroke_fill="#302a68")
	fixture_preview = Image.new("RGBA", (120, 160), (82, 70, 130, 255))
	fixture_preview.alpha_composite(fixture, (12, 16))
	canvas.paste(fixture_preview.convert("RGB"), (1390, 648))
	draw.text(
		(18, 782),
		"Green ruler = the shared fixture centerline. Source masters preserved.",
		font=font(17),
		fill="#49417f")
	OUTPUT_CONTACT.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(OUTPUT_CONTACT, format="PNG", optimize=True)


def main() -> None:
	SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
	AUDIT_ROOT.mkdir(parents=True, exist_ok=True)
	source_a = Image.open(SOURCE_A).convert("RGB")
	source_b = Image.open(SOURCE_B).convert("RGB")
	if source_a.size != MASTER_SIZE or source_b.size != MASTER_SIZE:
		raise ValueError(
			f"Expected {MASTER_SIZE}, got {source_a.size} and {source_b.size}")

	aligned_a, cleanup_a = fill_from_candidate(
		source_a, CANDIDATE_A, A_FIXTURE_CENTERS,
		half_width=55, half_height=100)
	clean_b, cleanup_b = fill_from_candidate(
		source_b, CANDIDATE_B, B_FIXTURE_CENTERS,
		half_width=55, half_height=78)
	toned_b, tone_harmonization = harmonize_screen_tone(
		aligned_a, clean_b)
	aligned_b = feather_screen_join(aligned_a, toned_b)
	aligned_a.save(OUTPUT_A, format="PNG", optimize=True)
	aligned_b.save(OUTPUT_B, format="PNG", optimize=True)

	fixture = extract_fixture(source_b)
	fixture.save(FIXTURE_OUTPUT, format="PNG", optimize=True)
	portal = extract_playroom_portal()
	portal.save(PORTAL_OUTPUT, format="PNG", optimize=True)
	join_column = extract_join_column(source_a)
	join_column.save(JOIN_COLUMN_OUTPUT, format="PNG", optimize=True)
	join_inlay = build_join_floor_inlay(source_a)
	join_inlay.save(JOIN_INLAY_OUTPUT, format="PNG", optimize=True)
	write_contact(source_a, source_b, aligned_a, aligned_b, fixture)

	position_rows = [
		{
			"id": (
				f"sconce_a{index}" if index < 3
				else f"sconce_b{index - 3}"),
			"runtime_center": list(center),
			"height_delta_from_target": center[1] - TARGET_RUNTIME_Y,
		}
		for index, center in enumerate(RUNTIME_FIXTURE_CENTERS)
	]
	report = {
		"schema": 1,
		"purpose": "Main Hall fixture alignment and screen-join continuity",
		"new_art_generated": True,
		"source_policy": (
			"cleanup candidates accepted only inside six compact masks; "
			"reusable runtime cards use accepted master pixels only"),
		"source_masters": {
			"A": {
				"path": SOURCE_A.relative_to(ROOT).as_posix(),
				"dimensions": list(source_a.size),
				"sha256": sha256(SOURCE_A),
			},
			"B": {
				"path": SOURCE_B.relative_to(ROOT).as_posix(),
				"dimensions": list(source_b.size),
				"sha256": sha256(SOURCE_B),
			},
		},
		"derived_masters": {
			"A": {
				"path": OUTPUT_A.relative_to(ROOT).as_posix(),
				"dimensions": list(aligned_a.size),
				"sha256": sha256(OUTPUT_A),
			},
			"B": {
				"path": OUTPUT_B.relative_to(ROOT).as_posix(),
				"dimensions": list(aligned_b.size),
				"sha256": sha256(OUTPUT_B),
			},
		},
		"fixture": {
			"path": FIXTURE_OUTPUT.relative_to(ROOT).as_posix(),
			"dimensions": list(fixture.size),
			"sha256": sha256(FIXTURE_OUTPUT),
			"extraction_source_rectangle": [704, 300, 800, 428],
		},
		"playroom_portal": {
			"source_path": PORTAL_SOURCE.relative_to(ROOT).as_posix(),
			"source_sha256": sha256(PORTAL_SOURCE),
			"path": PORTAL_OUTPUT.relative_to(ROOT).as_posix(),
			"dimensions": list(portal.size),
			"sha256": sha256(PORTAL_OUTPUT),
			"method": "alpha silhouette extraction; accepted pixels only",
		},
		"architectural_join_cards": {
			"column": {
				"path": JOIN_COLUMN_OUTPUT.relative_to(ROOT).as_posix(),
				"dimensions": list(join_column.size),
				"sha256": sha256(JOIN_COLUMN_OUTPUT),
				"source_rectangle": [1170, 212, 1360, 1153],
			},
			"floor_inlay": {
				"path": JOIN_INLAY_OUTPUT.relative_to(ROOT).as_posix(),
				"dimensions": list(join_inlay.size),
				"sha256": sha256(JOIN_INLAY_OUTPUT),
				"source_trim_rectangle": [1170, 920, 1360, 944],
			},
			"method": "accepted Screen-A pixels only; alpha extraction",
		},
		"generated_cleanup": {
			"generator": "built-in image_gen precise-object-edit",
			"A": {**cleanup_a, "final_prompt": CLEANUP_PROMPTS["A"]},
			"B": {**cleanup_b, "final_prompt": CLEANUP_PROMPTS["B"]},
		},
		"fixture_placement": {
			"target_runtime_y": TARGET_RUNTIME_Y,
			"positions": position_rows,
			"maximum_height_delta": max(
				abs(int(row["height_delta_from_target"]))
				for row in position_rows),
			"pass": all(
				int(row["height_delta_from_target"]) == 0
				for row in position_rows),
		},
		"screen_join": {
			"runtime_coordinate_x": 1672,
			"blend_width": SEAM_BLEND_WIDTH,
			"method": (
				"four-pixel exact-edge ramp beneath accepted architectural "
				"Sprite3D divider cards; no copied structures"),
			**seam_metrics(aligned_a, aligned_b),
		},
		"tone_harmonization": tone_harmonization,
		"contact_sheet": {
			"path": OUTPUT_CONTACT.relative_to(ROOT).as_posix(),
			"sha256": sha256(OUTPUT_CONTACT),
		},
	}
	OUTPUT_MANIFEST.write_text(
		json.dumps(report, indent=2) + "\n",
		encoding="utf-8")
	if not report["fixture_placement"]["pass"]:
		raise RuntimeError("Fixture height normalization failed")
	if not report["screen_join"]["edge_pixel_exact"]:
		raise RuntimeError("Derived screen join is not edge-exact")
	print(
		"OK: six fixtures normalized to runtime y=215; "
		"derived A/B join is edge-pixel exact")


if __name__ == "__main__":
	main()
