#!/usr/bin/env python3
"""Promote the accepted 2026-08-01 Opera regeneration batch.

Native generated candidates remain untouched in the dated staging directory.
Only delivery copies are normalized, matted, sliced, or fitted here.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import shutil

from PIL import Image, ImageFilter

from prepare_opera_2d_props import _matte_card
from prepare_opera_2d_worlds import _fit_actor, _remove_edge_field


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "assets_src/concepts/opera_regeneration_2026-08-01/cards"
JOB_ROOT = ROOT / "assets_src/concepts/opera_jobs_flat_2026-07-21"
JOB_CARDS = JOB_ROOT / "cards"
HOUSE_ROOT = ROOT / "assets_src/concepts/opera_house_flat"
HOUSE_CARDS = HOUSE_ROOT / "cards"
ACTORS = ROOT / "assets/opera/worlds/actors"

FINALE_NAMES = {
	"doctor_performance_boss_finale_2026-07-24.png",
	"farmer_performance_boss_finale_2026-07-24.png",
	"boxer_performance_boss_finale_2026-07-24.png",
	"magician_performance_boss_finale_2026-07-24.png",
	"painter_performance_boss_finale_2026-07-24.png",
	"astronaut_engineer_performance_boss_finale_2026-07-24.png",
	"racecar_driver_performance_boss_finale_2026-07-24.png",
	"pop_star_performance_boss_finale_2026-07-24.png",
}

FARMER_GAMEPLAY_NAMES = (
	"apple", "berries", "carrot", "corn", "happy_piggy_group", "hay_bale",
	"mud_splash", "piggy_fed", "piggy_hop", "piggy_munch",
	"piggy_target_medallion", "piggy_trot_a", "piggy_trot_b", "pumpkin",
	"toss_arc", "vegetable_basket",
)

CREST_NAMES = (
	"chef", "detective", "ballerina", "candy", "dragon", "doctor",
	"farmer", "boxer", "magician", "phantom", "painter", "engineer",
	"racer", "singer", "maestro", "house",
)


def _normalize(source: Path, target: Path, size: tuple[int, int]) -> None:
	target.parent.mkdir(parents=True, exist_ok=True)
	with Image.open(source) as image:
		image.convert("RGB").resize(size, Image.Resampling.LANCZOS).save(
			target, optimize=True, compress_level=9
		)


def _field_distance(pixel: tuple[int, ...], field: tuple[int, int, int]) -> int:
	return sum((int(pixel[index]) - field[index]) ** 2 for index in range(3))


def _central_component(source: Image.Image) -> Image.Image:
	"""Return the dominant central object, excluding disconnected neighbours."""
	image = source.convert("RGBA")
	width, height = image.size
	pixels = image.load()
	edge_samples = []
	for x in range(0, width, max(1, width // 32)):
		edge_samples.extend((pixels[x, 0], pixels[x, height - 1]))
	for y in range(0, height, max(1, height // 32)):
		edge_samples.extend((pixels[0, y], pixels[width - 1, y]))
	field = tuple(
		sorted(int(pixel[channel]) for pixel in edge_samples)[len(edge_samples) // 2]
		for channel in range(3)
	)
	foreground = bytearray(width * height)
	for y in range(height):
		for x in range(width):
			pixel = pixels[x, y]
			if _field_distance(pixel, field) > 34 * 34 or max(pixel[:3]) > 104:
				foreground[y * width + x] = 1

	seen = bytearray(width * height)
	components: list[tuple[float, int, tuple[int, int, int, int]]] = []
	center_x, center_y = width / 2.0, height / 2.0
	for start in range(width * height):
		if seen[start] or not foreground[start]:
			continue
		queue = deque([start])
		seen[start] = 1
		area = 0
		x0 = x1 = start % width
		y0 = y1 = start // width
		while queue:
			index = queue.popleft()
			x, y = index % width, index // width
			area += 1
			x0, y0, x1, y1 = min(x0, x), min(y0, y), max(x1, x), max(y1, y)
			for dy in (-1, 0, 1):
				for dx in (-1, 0, 1):
					nx, ny = x + dx, y + dy
					if 0 <= nx < width and 0 <= ny < height:
						other = ny * width + nx
						if foreground[other] and not seen[other]:
							seen[other] = 1
							queue.append(other)
		if area >= 120:
			cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
			box_width, box_height = x1 - x0 + 1, y1 - y0 + 1
			# Sheet divider lines are large connected components but never art.
			if ((box_width > width * 0.82 and box_height < height * 0.10) or
					(box_height > height * 0.82 and box_width < width * 0.10) or
					(box_width > width * 0.82 and box_height > height * 0.82 and
						area < width * height * 0.20)):
				continue
			distance = ((cx - center_x) / width) ** 2 + ((cy - center_y) / height) ** 2
			components.append((distance, area, (x0, y0, x1 + 1, y1 + 1)))
	if not components:
		raise RuntimeError("No central object found")
	# Prefer a large component close to the expected cell center.
	components.sort(key=lambda item: item[0] - min(item[1] / (width * height), 0.25) * 1.4)
	x0, y0, x1, y1 = components[0][2]
	margin = max(4, round(min(width, height) * 0.025))
	return image.crop((max(0, x0 - margin), max(0, y0 - margin),
		min(width, x1 + margin), min(height, y1 + margin)))


def _extract_grid_object(sheet: Path, index: int, columns: int = 4,
		rows: int = 4, pad: float = 0.17) -> Image.Image:
	with Image.open(sheet) as source:
		row, column = divmod(index, columns)
		cell_w, cell_h = source.width / columns, source.height / rows
		x0 = max(0, round((column - pad) * cell_w))
		y0 = max(0, round((row - pad) * cell_h))
		x1 = min(source.width, round((column + 1 + pad) * cell_w))
		y1 = min(source.height, round((row + 1 + pad) * cell_h))
		return _central_component(source.crop((x0, y0, x1, y1)))


def _extract_grid_region(sheet: Path, index: int, columns: int = 4,
		rows: int = 4, pad: float = 0.12) -> Image.Image:
	"""Crop a slightly overlapping clean-field cell without subject slicing."""
	with Image.open(sheet) as source:
		row, column = divmod(index, columns)
		cell_w, cell_h = source.width / columns, source.height / rows
		return source.convert("RGBA").crop((
			max(0, round((column - pad) * cell_w)),
			max(0, round((row - pad) * cell_h)),
			min(source.width, round((column + 1 + pad) * cell_w)),
			min(source.height, round((row + 1 + pad) * cell_h)),
		))


def _extract_adaptive_grid_region(sheet: Path, index: int,
		columns: int = 4, rows: int = 4) -> Image.Image:
	"""Place dividers in the actual navy gaps between overlapping subjects."""
	with Image.open(sheet) as raw:
		source = raw.convert("RGBA")
		pixels = source.load()
		corners = (pixels[0, 0], pixels[source.width - 1, 0],
			pixels[0, source.height - 1], pixels[source.width - 1, source.height - 1])
		field = tuple(sum(int(pixel[channel]) for pixel in corners) // 4
			for channel in range(3))
		x_counts = [sum(_field_distance(pixels[x, y], field) > 34 * 34 or
			max(pixels[x, y][:3]) > 104 for y in range(source.height))
			for x in range(source.width)]
		y_counts = [sum(_field_distance(pixels[x, y], field) > 34 * 34 or
			max(pixels[x, y][:3]) > 104 for x in range(source.width))
			for y in range(source.height)]
		x_edges = [0]
		for divider in range(1, columns):
			expected = round(divider * source.width / columns)
			radius = max(8, source.width // (columns * 5))
			x_edges.append(min(range(expected - radius, expected + radius + 1),
				key=lambda x: x_counts[x]))
		x_edges.append(source.width)
		y_edges = [0]
		for divider in range(1, rows):
			expected = round(divider * source.height / rows)
			radius = max(8, source.height // (rows * 5))
			y_edges.append(min(range(expected - radius, expected + radius + 1),
				key=lambda y: y_counts[y]))
		y_edges.append(source.height)
		row, column = divmod(index, columns)
		return source.crop((x_edges[column], y_edges[row],
			x_edges[column + 1], y_edges[row + 1]))


def _extract_inset_grid_cell(sheet: Path, index: int, inset: int = 5) -> Image.Image:
	with Image.open(sheet) as source:
		row, column = divmod(index, 4)
		x0, y0 = round(column * source.width / 4), round(row * source.height / 4)
		x1, y1 = round((column + 1) * source.width / 4), round((row + 1) * source.height / 4)
		return source.convert("RGBA").crop((x0 + inset, y0 + inset, x1 - inset, y1 - inset))


def _fit_card(subject: Image.Image, target: Path, size: int = 1024) -> None:
	field = (4, 25, 54, 255)
	canvas = Image.new("RGBA", (size, size), field)
	max_side = round(size * 0.91)
	scale = min(max_side / subject.width, max_side / subject.height)
	resized = subject.resize((max(1, round(subject.width * scale)),
		max(1, round(subject.height * scale))), Image.Resampling.LANCZOS)
	canvas.alpha_composite(resized, ((size - resized.width) // 2,
		(size - resized.height) // 2))
	target.parent.mkdir(parents=True, exist_ok=True)
	canvas.convert("RGB").save(target, optimize=True, compress_level=9)


def _promote_generated_cards() -> None:
	for source in STAGE.glob("opera_job_*.png"):
		shutil.copyfile(source, JOB_CARDS / source.name)

	for name in FINALE_NAMES:
		_normalize(STAGE / name,
			ROOT / "assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24" / name,
			(1024, 576))

	_normalize(STAGE / "opera_rival_costume_sheet_master.png",
		ROOT / "assets_src/concepts/opera_rivals_2026-07-29/opera_rival_costume_sheet_master.png",
		(1024, 768))
	farmer_target = JOB_ROOT / "farmer_gameplay_sheet_2026-07-21.png"
	_normalize(STAGE / "farmer_gameplay_sheet.png", farmer_target, (1024, 1024))
	with Image.open(farmer_target) as image:
		for index, name in enumerate(FARMER_GAMEPLAY_NAMES):
			row, column = divmod(index, 4)
			box = (column * 256, row * 256, (column + 1) * 256, (row + 1) * 256)
			image.crop(box).resize((1024, 1024), Image.Resampling.LANCZOS).save(
				JOB_CARDS / f"opera_job_farmer_gameplay_{name}.png", optimize=True)

	for state in ("ground", "middle", "full"):
		shutil.copyfile(STAGE / f"opera_upper_access_floor_selector_{state}.png",
			HOUSE_CARDS / f"opera_upper_access_floor_selector_{state}.png")

	# P3-03 is a complete accepted kit; retain the native sheet and derive cards.
	audience = STAGE / "opera_house_audience_kit.png"
	shutil.copyfile(audience, HOUSE_ROOT / "opera_house_audience_kit_2026-08-01.png")
	with Image.open(audience) as image:
		for index in range(16):
			row, column = divmod(index, 4)
			box = (round(column * image.width / 4), round(row * image.height / 4),
				round((column + 1) * image.width / 4), round((row + 1) * image.height / 4))
			image.crop(box).resize((1024, 1024), Image.Resampling.LANCZOS).save(
				HOUSE_CARDS / f"opera_audience_module_{index + 1:02d}.png", optimize=True)


def _promote_path_a() -> None:
	crest_sheet = HOUSE_ROOT / "opera_house_crest_wayfinding_kit_2026-07-21.png"
	for index, name in enumerate(CREST_NAMES):
		# This sheet has a continuous navy field and slightly overlapping oval
		# bounds, so an overlapping region is the lossless Path A extraction.
		_fit_card(_extract_adaptive_grid_region(crest_sheet, index),
			HOUSE_CARDS / f"opera_crest_{name}.png")

	for slug in ("pastry_chef", "detective", "ballerina", "painter"):
		sheet = JOB_ROOT / f"{slug}_outfit_sheet_2026-07-21.png"
		crest = _extract_grid_object(sheet, 10)
		# The extended extraction intentionally crosses the source divider so
		# the badge is never clipped; discard its thin top-line remnant.
		crest = crest.crop((0, min(8, crest.height - 1), crest.width, crest.height))
		_fit_card(crest,
			JOB_CARDS / f"opera_job_{slug}_outfit_job_crest.png")

	# The astronaut bottom row contains six unequal cells; the rocket crest is first.
	astronaut = JOB_ROOT / "astronaut_engineer_outfit_sheet_2026-07-21.png"
	with Image.open(astronaut) as image:
		crest = _central_component(image.crop((0, round(image.height * 0.68),
			round(image.width * 0.23), image.height)))
	_fit_card(crest, JOB_CARDS / "opera_job_astronaut_engineer_outfit_job_crest.png")

	# Recover full objects from the clean sheets for the three edge-debris cards.
	path_a = (
		(HOUSE_ROOT / "opera_house_stage_backstage_kit_2026-07-21.png", 6,
			HOUSE_CARDS / "opera_stage_scenic_backdrop.png"),
		(HOUSE_ROOT / "opera_house_lobby_services_kit_2026-07-21.png", 11,
			HOUSE_CARDS / "opera_lobby_services_handwashing_bubble_markers.png"),
		(HOUSE_ROOT / "opera_house_stage_backstage_kit_2026-07-21.png", 0,
			HOUSE_CARDS / "opera_stage_elliptical_proscenium.png"),
	)
	for sheet, index, target in path_a:
		_fit_card(_extract_grid_object(sheet, index), target)

	# Split genuine two-state source cards; preserve the source card itself.
	for source_name, output_names in (
		("opera_stage_house_curtain_states.png",
			("opera_stage_house_curtain_closed.png", "opera_stage_house_curtain_open.png")),
		("opera_architecture_medallion_states.png",
			("opera_architecture_medallion_dark.png", "opera_architecture_medallion_lit.png")),
	):
		with Image.open(HOUSE_CARDS / source_name) as image:
			for index, output_name in enumerate(output_names):
				part = image.crop((round(index * image.width / 2), 0,
					round((index + 1) * image.width / 2), image.height))
				_fit_card(_central_component(part), HOUSE_CARDS / output_name)


def _promote_actors() -> None:
	ACTORS.mkdir(parents=True, exist_ok=True)
	for name in ("imp_mischief", "imp_captain", "imp_mischief_bopped",
			"imp_mischief_bow", "imp_captain_bopped", "imp_captain_bow"):
		_fit_actor(_remove_edge_field(STAGE / f"{name}.png"), 512).save(
			ACTORS / f"{name}.png", optimize=True)

	for source_name, target_name in (
		("roshan_doctor_stethoscope.png", "roshan_doctor.png"),
		("roshan_racer_steering_wheel.png", "roshan_racer.png"),
	):
		_fit_actor(_remove_edge_field(STAGE / source_name), 512).save(
			ACTORS / target_name, optimize=True)

	# P2-04/05/07 are approved art with only matting/crop failures.
	for career in ("boxer", "magician", "farmer"):
		source = JOB_CARDS / f"opera_job_{career}_outfit_hero_front_three_quarter.png"
		_fit_actor(_matte_card(source), 512).save(ACTORS / f"roshan_{career}.png", optimize=True)


def main() -> None:
	if not STAGE.is_dir():
		raise SystemExit(f"staging directory not found: {STAGE}")
	JOB_CARDS.mkdir(parents=True, exist_ok=True)
	HOUSE_CARDS.mkdir(parents=True, exist_ok=True)
	_promote_generated_cards()
	_promote_path_a()
	_promote_actors()
	print("promoted accepted Opera regeneration assets")


if __name__ == "__main__":
	main()
