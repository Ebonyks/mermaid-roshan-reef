#!/usr/bin/env python3
"""Stage deterministic Path A fixes from approved Opera source art.

This tool never overwrites source sheets or runtime assets.  It writes only to
the dated opera-regeneration staging directory so the review/promotion gate can
compare every derived card before promotion.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageStat

from prepare_opera_2d_worlds import _fit_actor, _remove_edge_field


ROOT = Path(__file__).resolve().parents[1]
HOUSE = ROOT / "assets_src/concepts/opera_house_flat"
JOBS = ROOT / "assets_src/concepts/opera_jobs_flat_2026-07-21"
ACTORS = ROOT / "assets/opera/worlds/actors"
STAGING = ROOT / "assets_src/concepts/opera_regeneration_2026-08-01/cards"
NAVY = (4, 22, 45)


CREST_NAMES = (
	"chef", "detective", "ballerina", "candy",
	"dragon", "doctor", "farmer", "boxer",
	"magician", "phantom", "painter", "engineer",
	"racer", "singer", "maestro", "house",
)


JOB_CREST_SHEETS = {
	"opera_job_pastry_chef_outfit_job_crest.png":
		"pastry_chef_outfit_sheet_2026-07-21.png",
	"opera_job_detective_outfit_job_crest.png":
		"detective_outfit_sheet_2026-07-21.png",
	"opera_job_ballerina_outfit_job_crest.png":
		"ballerina_outfit_sheet_2026-07-21.png",
	"opera_job_painter_outfit_job_crest.png":
		"painter_outfit_sheet_2026-07-21.png",
}


def _keep_largest_component(foreground: Image.Image) -> Image.Image:
	"""Drop disconnected neighboring-cell fragments from an RGBA crop."""
	alpha = foreground.getchannel("A")
	pixels = alpha.load()
	visited: set[tuple[int, int]] = set()
	components: list[list[tuple[int, int]]] = []
	for y in range(foreground.height):
		for x in range(foreground.width):
			if (x, y) in visited or pixels[x, y] <= 8:
				continue
			stack = [(x, y)]
			visited.add((x, y))
			component: list[tuple[int, int]] = []
			while stack:
				point = stack.pop()
				component.append(point)
				px, py = point
				for neighbor in ((px - 1, py), (px + 1, py),
						(px, py - 1), (px, py + 1)):
					nx, ny = neighbor
					if not (0 <= nx < foreground.width and 0 <= ny < foreground.height):
						continue
					if neighbor in visited or pixels[nx, ny] <= 8:
						continue
					visited.add(neighbor)
					stack.append(neighbor)
			components.append(component)
	if not components:
		raise RuntimeError("No connected art component remained")
	keep = set(max(components, key=len))
	result = foreground.copy()
	result_alpha = result.getchannel("A")
	result_pixels = result_alpha.load()
	for y in range(result.height):
		for x in range(result.width):
			if (x, y) not in keep:
				result_pixels[x, y] = 0
	result.putalpha(result_alpha)
	return result


def _place_on_navy(source: Image.Image, size: int, margin: int,
		primary_component_only: bool = False) -> Image.Image:
	"""Remove a connected edge field and center the surviving approved art."""
	working_path = STAGING / ".path_a_working.png"
	source.convert("RGB").save(working_path)
	foreground = _remove_edge_field(working_path)
	working_path.unlink()
	if primary_component_only:
		foreground = _keep_largest_component(foreground)
	bounds = foreground.getbbox()
	if bounds is None:
		raise RuntimeError("No foreground remained while reframing Path A art")
	foreground = foreground.crop(bounds)
	limit = size - margin * 2
	scale = min(limit / foreground.width, limit / foreground.height)
	new_size = (
		max(1, round(foreground.width * scale)),
		max(1, round(foreground.height * scale)),
	)
	foreground = foreground.resize(new_size, Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", (size, size), NAVY + (255,))
	position = ((size - foreground.width) // 2, (size - foreground.height) // 2)
	canvas.alpha_composite(foreground, position)
	return canvas.convert("RGB")


def _crop_with_padding(source: Image.Image,
		box: tuple[int, int, int, int]) -> Image.Image:
	"""Crop a box that may extend past the source, padding with edge navy."""
	left, top, right, bottom = box
	canvas = Image.new("RGB", (right - left, bottom - top), NAVY)
	intersection = (
		max(0, left), max(0, top), min(source.width, right), min(source.height, bottom),
	)
	if intersection[0] < intersection[2] and intersection[1] < intersection[3]:
		piece = source.crop(intersection).convert("RGB")
		canvas.paste(piece, (intersection[0] - left, intersection[1] - top))
	return canvas


def _bright_primary_crop(source: Image.Image, padding: int = 8,
		include_center_satellites: bool = False) -> Image.Image:
	"""Find the main bright art island while ignoring the navy presentation field.

	The source-sheet navy is a shallow gradient, so using it as an alpha key can
	leave connected background bands.  A brightness mask is used only to locate
	the approved object's bounds; the returned pixels are untouched source RGB.
	"""
	rgb = source.convert("RGB")
	pixels = rgb.load()
	visited: set[tuple[int, int]] = set()
	components: list[list[tuple[int, int]]] = []
	for y in range(rgb.height):
		for x in range(rgb.width):
			red, green, blue = pixels[x, y]
			if (x, y) in visited or red + green + blue <= 150:
				continue
			stack = [(x, y)]
			visited.add((x, y))
			component: list[tuple[int, int]] = []
			while stack:
				px, py = stack.pop()
				component.append((px, py))
				for neighbor in ((px - 1, py), (px + 1, py),
						(px, py - 1), (px, py + 1)):
					nx, ny = neighbor
					if not (0 <= nx < rgb.width and 0 <= ny < rgb.height):
						continue
					if neighbor in visited:
						continue
					nred, ngreen, nblue = pixels[nx, ny]
					if nred + ngreen + nblue <= 150:
						continue
					visited.add(neighbor)
					stack.append(neighbor)
			components.append(component)
	if not components:
		raise RuntimeError("No bright source-art component found")
	component = max(components, key=len)
	if include_center_satellites:
		center_x = rgb.width / 2.0
		center_y = rgb.height / 2.0
		radius = min(rgb.width, rgb.height) * 0.44
		selected: list[tuple[int, int]] = []
		for candidate in components:
			candidate_x = sum(point[0] for point in candidate) / len(candidate)
			candidate_y = sum(point[1] for point in candidate) / len(candidate)
			if ((candidate_x - center_x) ** 2
					+ (candidate_y - center_y) ** 2) ** 0.5 <= radius:
				selected.extend(candidate)
		if selected:
			component = selected
	left = max(0, min(point[0] for point in component) - padding)
	top = max(0, min(point[1] for point in component) - padding)
	right = min(rgb.width, max(point[0] for point in component) + padding + 1)
	bottom = min(rgb.height, max(point[1] for point in component) + padding + 1)
	return rgb.crop((left, top, right, bottom))


def stage_house_crests() -> None:
	"""Reframe shifted oval crests without neighboring-card bleed."""
	source_path = HOUSE / "opera_house_crest_wayfinding_kit_2026-07-21.png"
	with Image.open(source_path) as source:
		source = source.convert("RGB")
		pixels = source.load()
		visited: set[tuple[int, int]] = set()
		groups: list[list[tuple[int, int]]] = [[] for _unused in CREST_NAMES]
		centers = tuple((150 + column * 256, 150 + row * 256)
			for row in range(4) for column in range(4))
		for y in range(source.height):
			for x in range(source.width):
				red, green, blue = pixels[x, y]
				if (x, y) in visited or red + green + blue <= 150:
					continue
				stack = [(x, y)]
				visited.add((x, y))
				component: list[tuple[int, int]] = []
				while stack:
					px, py = stack.pop()
					component.append((px, py))
					for neighbor in ((px - 1, py), (px + 1, py),
							(px, py - 1), (px, py + 1)):
						nx, ny = neighbor
						if not (0 <= nx < source.width and 0 <= ny < source.height):
							continue
						if neighbor in visited:
							continue
						nred, ngreen, nblue = pixels[nx, ny]
						if nred + ngreen + nblue <= 150:
							continue
						visited.add(neighbor)
						stack.append(neighbor)
				if len(component) < 4:
					continue
				component_x = sum(point[0] for point in component) / len(component)
				component_y = sum(point[1] for point in component) / len(component)
				owner = min(range(len(centers)), key=lambda candidate:
					(component_x - centers[candidate][0]) ** 2
					+ (component_y - centers[candidate][1]) ** 2)
				groups[owner].extend(component)
		for index, name in enumerate(CREST_NAMES):
			if not groups[index]:
				raise RuntimeError(f"No crest art detected for {name}")
			padding = 12
			box = (
				max(0, min(point[0] for point in groups[index]) - padding),
				max(0, min(point[1] for point in groups[index]) - padding),
				min(source.width, max(point[0] for point in groups[index]) + padding + 1),
				min(source.height, max(point[1] for point in groups[index]) + padding + 1),
			)
			candidate = _place_on_navy(source.crop(box), 256, 9)
			candidate.save(STAGING / f"opera_crest_{name}.png", optimize=True)


def stage_job_crests() -> None:
	"""Reframe the requested outfit crests, including the six-cell astronaut row."""
	for output_name, sheet_name in JOB_CREST_SHEETS.items():
		with Image.open(JOBS / sheet_name) as source:
			# Standard outfit crest is row 3, column 3 in the authored 4x4 layout.
			cell = source.convert("RGB").crop((512, 512, 768, 768))
			_place_on_navy(cell, 1024, 72, primary_component_only=True).save(
				STAGING / output_name, optimize=True)

	with Image.open(JOBS / "astronaut_engineer_outfit_sheet_2026-07-21.png") as source:
		# This sheet's bottom row is six authored sub-cells.  The rocket crest is
		# the first one, not the uniform-grid r3c3 card produced by the old slicer.
		cell = source.convert("RGB").crop((0, 700, 220, 1024))
		_place_on_navy(cell, 1024, 72, primary_component_only=True).save(
			STAGING / "opera_job_astronaut_engineer_outfit_job_crest.png",
			optimize=True,
		)


def _split_pair(source_path: Path, output_names: tuple[str, str],
		overlap: int) -> None:
	with Image.open(source_path) as source:
		source = source.convert("RGB")
		midpoint = source.width // 2
		for index, output_name in enumerate(output_names):
			left = 0 if index == 0 else midpoint - overlap
			right = midpoint + overlap if index == 0 else source.width
			cell = source.crop((left, 0, right, source.height))
			_place_on_navy(cell, 256, 18).save(STAGING / output_name, optimize=True)


def stage_split_states() -> None:
	_split_pair(
		HOUSE / "cards/opera_stage_house_curtain_states.png",
		("opera_stage_house_curtain_closed.png", "opera_stage_house_curtain_open.png"),
		16,
	)
	# The architecture sheet's medallion pair crosses the old uniform cell
	# boundary.  Recut each complete state from the clean source sheet instead
	# of splitting the already-clipped legacy card.
	with Image.open(HOUSE / "opera_house_architecture_kit_2026-07-21.png") as source:
		source = source.convert("RGB")
		for box, output_name in (
			((450, 440, 625, 640), "opera_architecture_medallion_dark.png"),
			((615, 440, 790, 640), "opera_architecture_medallion_lit.png"),
		):
			_place_on_navy(source.crop(box), 256, 18).save(
				STAGING / output_name, optimize=True)


def _first_divider(source: Image.Image, axis: str,
		lower: int, upper: int) -> int:
	"""Find the darkest full-sheet divider in an expected authored range."""
	values: list[tuple[float, int]] = []
	if axis == "x":
		for coordinate in range(lower, upper):
			strip = source.crop((coordinate, 0, coordinate + 1, source.height))
			values.append((sum(ImageStat.Stat(strip).mean), coordinate))
	else:
		for coordinate in range(lower, upper):
			strip = source.crop((0, coordinate, source.width, coordinate + 1))
			values.append((sum(ImageStat.Stat(strip).mean), coordinate))
	return min(values)[1]


def _stage_actor_recut(job: str, output_name: str) -> None:
	with Image.open(JOBS / f"{job}_outfit_sheet_2026-07-21.png") as source:
		source = source.convert("RGB")
		right = _first_divider(source, "x", 240, 275)
		bottom = _first_divider(source, "y", 260, 335)
		cell = source.crop((3, 3, right, bottom))
	working_path = STAGING / f".{job}_hero_working.png"
	cell.save(working_path)
	actor = _remove_edge_field(working_path)
	# Enclosed tail/hair concavities are not edge-connected, so explicitly
	# clear only pixels still matching the sampled navy presentation field.
	rgba = actor.load()
	for y in range(actor.height):
		for x in range(actor.width):
			red, green, blue, alpha = rgba[x, y]
			if alpha and abs(red - NAVY[0]) + abs(green - NAVY[1]) + abs(blue - NAVY[2]) <= 35:
				rgba[x, y] = (red, green, blue, 0)
	actor = _fit_actor(actor)
	working_path.unlink()
	actor.save(STAGING / output_name, optimize=True)


def stage_actor_recuts() -> None:
	_stage_actor_recut("boxer", "roshan_boxer_fulltail.png")
	_stage_actor_recut("magician", "roshan_magician_cleanup.png")
	_stage_actor_recut("farmer", "roshan_farmer_hairfix.png")


def _fill_edge(image: Image.Image, edge: str, pixels: int) -> Image.Image:
	"""Erase a known neighbor sliver with the card's sampled navy field."""
	result = image.convert("RGB")
	if edge == "top":
		sample = Image.new("RGB", (result.width, pixels), NAVY)
		result.paste(sample, (0, 0))
	elif edge == "right":
		sample = result.crop((result.width - pixels - 1, 0,
			result.width - pixels, result.height)).resize(
			(pixels, result.height), Image.Resampling.NEAREST)
		result.paste(sample, (result.width - pixels, 0))
	else:
		raise ValueError(edge)
	return result


def stage_edge_cleanups() -> None:
	with Image.open(HOUSE / "cards/opera_stage_scenic_backdrop.png") as source:
		_fill_edge(source, "right", 7).save(
			STAGING / "opera_stage_scenic_backdrop.png", optimize=True)
	with Image.open(HOUSE / "cards/opera_lobby_services_handwashing_bubble_markers.png") as source:
		_fill_edge(source, "top", 12).save(
			STAGING / "opera_lobby_services_handwashing_bubble_markers.png",
			optimize=True,
		)
	with Image.open(HOUSE / "cards/opera_stage_elliptical_proscenium.png") as source:
		_place_on_navy(source.convert("RGB"), 256, 15).save(
			STAGING / "opera_stage_elliptical_proscenium.png", optimize=True)


def main() -> None:
	STAGING.mkdir(parents=True, exist_ok=True)
	stage_house_crests()
	stage_job_crests()
	stage_split_states()
	stage_actor_recuts()
	stage_edge_cleanups()
	print("OPERA_REGEN_PATH_A|crests=21|split_states=4|actors=3|cleanups=3")


if __name__ == "__main__":
	main()
