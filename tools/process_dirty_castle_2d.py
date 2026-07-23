#!/usr/bin/env python3
"""Build runtime-ready dirty-castle sprites, cinematic frames, and QA sheets."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "concepts" / "dirty_castle_cleanup_2026-07-22"
PROCESSED = SOURCE / "processed"
RUNTIME = ROOT / "assets" / "castle" / "dirty_cleanup_2d"
CINEMATIC = ROOT / "assets" / "cinematics" / "dirty_castle"
AUDIT = ROOT / "audit" / "dirty_castle_2d_2026-07-22"

SPRITE_SIZE = 512
SPRITE_CONTENT = 448
FRAME_SIZE = (1024, 576)

ATLASES = (
	(
		PROCESSED / "dirty_targets_atlas_alpha.png",
		RUNTIME / "targets",
		(
			"target_dust_bunnies.png",
			"target_cobweb.png",
			"target_muddy_footprints.png",
			"target_floor_scuff.png",
			"target_sticky_spill.png",
			"target_window_smudge.png",
		),
	),
	(
		PROCESSED / "cleanup_tools_atlas_alpha.png",
		RUNTIME / "tools",
		(
			"tool_shell_suds_bucket.png",
			"tool_star_sponge.png",
			"tool_rainbow_mop.png",
			"tool_shell_scrub_brush.png",
			"tool_shell_spray_bottle.png",
			"tool_dustpan_broom.png",
		),
	),
	(
		PROCESSED / "cleanup_feedback_atlas_alpha.png",
		RUNTIME / "effects",
		(
			"fx_soap_bubbles.png",
			"fx_gold_sparkle.png",
			"fx_wipe_swoosh.png",
			"fx_soap_foam.png",
			"fx_clean_ring.png",
			"fx_all_clean_badge.png",
		),
	),
	(
		PROCESSED / "dust_bunny_cast_atlas_alpha.png",
		RUNTIME / "critters" / "dust_bunnies",
		(
			"dust_bunny_curl_ears.png",
			"dust_bunny_siblings.png",
			"dust_bunny_hop.png",
			"dust_bunny_shell_hide.png",
			"dust_bunny_sleepy.png",
			"dust_bunny_family.png",
		),
	),
	(
		PROCESSED / "clutter_targets_atlas_alpha.png",
		RUNTIME / "targets",
		(
			"target_toy_blocks.png",
			"target_craft_scraps.png",
			"target_tipped_books.png",
			"target_buttons_beads.png",
			"target_leaf_trail.png",
			"target_cloud_cushions.png",
		),
	),
	(
		PROCESSED / "room_grime_targets_atlas_alpha.png",
		RUNTIME / "targets",
		(
			"target_dusty_shelf.png",
			"target_cloudy_mirror.png",
			"target_bath_soap_ring.png",
			"target_flour_spill.png",
			"target_fireplace_smudge.png",
			"target_paint_splats.png",
		),
	),
	(
		PROCESSED / "expanded_tools_atlas_alpha.png",
		RUNTIME / "tools",
		(
			"tool_ribbon_duster.png",
			"tool_window_squeegee.png",
			"tool_cleaning_cloths.png",
			"tool_sorting_basket.png",
			"tool_shell_broom.png",
			"tool_dusting_mitt.png",
		),
	),
	(
		PROCESSED / "mess_action_fx_atlas_alpha.png",
		RUNTIME / "effects",
		(
			"fx_dust_bunny_hop.png",
			"fx_dust_poof.png",
			"fx_dust_bunny_trail.png",
			"fx_dust_bunny_peek.png",
			"fx_dust_bunny_friend_heart.png",
			"fx_dust_bunny_cloud_nest.png",
		),
	),
	(
		PROCESSED / "progress_badges_atlas_alpha.png",
		RUNTIME / "progress",
		(
			"progress_one_pearl.png",
			"progress_two_pearls.png",
			"progress_three_pearls.png",
			"badge_tidy_stack.png",
			"badge_dust_bunny_home.png",
			"badge_dust_bunny_helper.png",
		),
	),
	(
		PROCESSED / "object_mess_vignettes_atlas_alpha.png",
		RUNTIME / "targets" / "vignettes",
		(
			"vignette_dusty_chandelier.png",
			"vignette_crooked_banner.png",
			"vignette_smudged_throne.png",
			"vignette_messy_pantry.png",
			"vignette_messy_craft_table.png",
			"vignette_messy_toy_chest.png",
		),
	),
	(
		PROCESSED / "playroom_clutter_atlas_alpha.png",
		RUNTIME / "rooms" / "playroom",
		(
			"playroom_puzzle_tiles.png",
			"playroom_stacking_rings.png",
			"playroom_shell_tea_set.png",
			"playroom_dressup_pile.png",
			"playroom_balls_beanbag.png",
			"playroom_wheeled_shell_toy.png",
		),
	),
	(
		PROCESSED / "library_clutter_atlas_alpha.png",
		RUNTIME / "rooms" / "library",
		(
			"library_fallen_books.png",
			"library_bookmark_ribbons.png",
			"library_story_scrolls.png",
			"library_book_cart.png",
			"library_reading_cushions.png",
			"library_picture_cards.png",
		),
	),
	(
		PROCESSED / "royal_kitchen_targets_atlas_alpha.png",
		RUNTIME / "rooms" / "royal_kitchen",
		(
			"kitchen_sink_plates.png",
			"kitchen_counter_flour.png",
			"kitchen_stove_drips.png",
			"kitchen_tipped_cups.png",
			"kitchen_crooked_pan.png",
			"kitchen_cabinet_jars.png",
		),
	),
	(
		PROCESSED / "bubble_bath_targets_atlas_alpha.png",
		RUNTIME / "rooms" / "bubble_bath",
		(
			"bath_tub_soap_ring.png",
			"bath_foggy_mirror.png",
			"bath_vanity_droplets.png",
			"bath_rumpled_towels.png",
			"bath_toy_basket.png",
			"bath_water_droplet_trail.png",
		),
	),
	(
		PROCESSED / "royal_loo_undercroft_targets_atlas_alpha.png",
		RUNTIME / "rooms" / "basement",
		(
			"loo_toilet_soap_ring.png",
			"loo_crooked_paper_rolls.png",
			"loo_brush_holder.png",
			"loo_clean_water_splash.png",
			"undercroft_dusty_storage.png",
			"undercroft_stair_cobweb.png",
		),
	),
	(
		PROCESSED / "castle_rooms_vignettes_atlas_alpha.png",
		RUNTIME / "targets" / "room_vignettes",
		(
			"room_vignette_playroom.png",
			"room_vignette_library.png",
			"room_vignette_royal_kitchen.png",
			"room_vignette_bubble_bath.png",
			"room_vignette_royal_loo.png",
			"room_vignette_undercroft.png",
		),
	),
)

FRAMES = (
	("frame_01_arrival_dirty.png", "01_arrival_dirty.png"),
	("frame_02_dust_bunnies_reveal.png", "02_dust_bunnies_reveal.png"),
	("frame_02_choose_tools.png", "03_choose_tools.png"),
	("frame_04_dust_bunny_roundup.png", "04_dust_bunny_roundup.png"),
	("frame_03_roshan_window.png", "05_roshan_window.png"),
	("frame_04_daddy_floor.png", "06_daddy_floor.png"),
	("frame_05_eagle_dust.png", "07_eagle_dust.png"),
	("frame_08_hall_clean_reveal.png", "08_hall_clean_reveal.png"),
	("frame_09_playroom_doorway.png", "09_playroom_doorway.png"),
	("frame_10_playroom_before.png", "10_playroom_before.png"),
	("frame_09_toy_room_sort.png", "11_playroom_sort.png"),
	("frame_12_playroom_details.png", "12_playroom_details.png"),
	("frame_13_playroom_clean.png", "13_playroom_clean.png"),
	("frame_14_library_doorway.png", "14_library_doorway.png"),
	("frame_15_library_before.png", "15_library_before.png"),
	("frame_10_library_bunny_helpers.png", "16_library_bunny_helpers.png"),
	("frame_17_library_last_book.png", "17_library_last_book.png"),
	("frame_18_library_clean_storytime.png", "18_library_clean_storytime.png"),
	("frame_19_basement_descent.png", "19_basement_descent.png"),
	("frame_08_pantry_team.png", "20_pantry_team.png"),
	("frame_21_kitchen_doorway.png", "21_kitchen_doorway.png"),
	("frame_22_kitchen_jobs.png", "22_kitchen_jobs.png"),
	("frame_23_kitchen_sink.png", "23_kitchen_sink.png"),
	("frame_24_kitchen_counter_stove.png", "24_kitchen_counter_stove.png"),
	("frame_25_kitchen_clean.png", "25_kitchen_clean.png"),
	("frame_26_bath_discovery.png", "26_bath_discovery.png"),
	("frame_27_bath_mirror.png", "27_bath_mirror.png"),
	("frame_28_bath_tub_toys.png", "28_bath_tub_toys.png"),
	("frame_29_bath_clean.png", "29_bath_clean.png"),
	("frame_30_loo_reveal.png", "30_loo_reveal.png"),
	("frame_31_loo_team.png", "31_loo_team.png"),
	("frame_32_loo_clean.png", "32_loo_clean.png"),
	("frame_33_undercroft_before.png", "33_undercroft_before.png"),
	("frame_34_undercroft_clean.png", "34_undercroft_clean.png"),
	("frame_11_final_inspection.png", "35_final_inspection.png"),
	("frame_06_all_clean.png", "36_all_clean.png"),
)


def _fit_sprite(cell: Image.Image) -> Image.Image:
	alpha = cell.getchannel("A")
	bounds = alpha.getbbox()
	if bounds is None:
		raise ValueError("atlas cell contains no opaque pixels")
	content = cell.crop(bounds)
	scale = min(SPRITE_CONTENT / content.width, SPRITE_CONTENT / content.height)
	size = (
		max(1, round(content.width * scale)),
		max(1, round(content.height * scale)),
	)
	content = content.resize(size, Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
	offset = ((SPRITE_SIZE - size[0]) // 2, (SPRITE_SIZE - size[1]) // 2)
	canvas.alpha_composite(content, offset)
	return canvas


def _clear_key_green(image: Image.Image) -> Image.Image:
	pixels = [
		(0, 0, 0, 0)
		if opacity > 0 and red < 64 and green > 175 and blue < 80
		else (red, green, blue, opacity)
		for red, green, blue, opacity in image.getdata()
	]
	cleaned = Image.new("RGBA", image.size, (0, 0, 0, 0))
	cleaned.putdata(pixels)
	return cleaned


def _split_atlas(source: Path, output_dir: Path, names: tuple[str, ...]) -> list[Path]:
	if len(names) != 6:
		raise ValueError("dirty-castle atlases must contain exactly six sprites")
	output_dir.mkdir(parents=True, exist_ok=True)
	image = Image.open(source).convert("RGBA")
	alpha = image.getchannel("A")
	alpha_bytes = alpha.tobytes()
	width, height = image.size
	runs: list[tuple[int, int, int, int]] = []
	parents: list[int] = []
	previous: list[tuple[int, int, int]] = []

	def find(label: int) -> int:
		while parents[label] != label:
			parents[label] = parents[parents[label]]
			label = parents[label]
		return label

	def union(first: int, second: int) -> None:
		first_root = find(first)
		second_root = find(second)
		if first_root != second_root:
			parents[second_root] = first_root

	for y in range(height):
		offset = y * width
		current: list[tuple[int, int, int]] = []
		x = 0
		while x < width:
			while x < width and alpha_bytes[offset + x] <= 4:
				x += 1
			if x >= width:
				break
			start = x
			while x < width and alpha_bytes[offset + x] > 4:
				x += 1
			end = x - 1
			label = len(parents)
			parents.append(label)
			current.append((start, end, label))
			runs.append((y, start, end, label))
			for previous_start, previous_end, previous_label in previous:
				if previous_end < start - 1:
					continue
				if previous_start > end + 1:
					break
				union(label, previous_label)
		previous = current

	areas: dict[int, int] = {}
	x_totals: dict[int, float] = {}
	y_totals: dict[int, float] = {}
	for y, start, end, label in runs:
		root = find(label)
		length = end - start + 1
		areas[root] = areas.get(root, 0) + length
		x_totals[root] = x_totals.get(root, 0.0) + (start + end) * length / 2.0
		y_totals[root] = y_totals.get(root, 0.0) + y * length

	centers = (
		(width / 6.0, height / 4.0),
		(width / 2.0, height / 4.0),
		(width * 5.0 / 6.0, height / 4.0),
		(width / 6.0, height * 3.0 / 4.0),
		(width / 2.0, height * 3.0 / 4.0),
		(width * 5.0 / 6.0, height * 3.0 / 4.0),
	)
	assignments: dict[int, int] = {}
	for root, area in areas.items():
		if area < 16:
			continue
		cx = x_totals[root] / area
		cy = y_totals[root] / area
		assignments[root] = min(
			range(6),
			key=lambda index: (cx - centers[index][0]) ** 2 + (cy - centers[index][1]) ** 2,
		)

	masks = [Image.new("L", image.size, 0) for _ in range(6)]
	draws = [ImageDraw.Draw(mask) for mask in masks]
	for y, start, end, label in runs:
		root = find(label)
		index = assignments.get(root)
		if index is not None:
			draws[index].line((start, y, end, y), fill=255)

	outputs: list[Path] = []
	for index, name in enumerate(names):
		mask = masks[index].filter(ImageFilter.MaxFilter(3))
		cell = Image.new("RGBA", image.size, (0, 0, 0, 0))
		cell.paste(image, (0, 0), mask)
		sprite = _clear_key_green(_fit_sprite(cell))
		out = output_dir / name
		sprite.save(out, optimize=True)
		outputs.append(out)
	return outputs


def _center_crop_16_9(image: Image.Image) -> Image.Image:
	target_ratio = 16.0 / 9.0
	ratio = image.width / image.height
	if ratio > target_ratio:
		width = round(image.height * target_ratio)
		left = (image.width - width) // 2
		box = (left, 0, left + width, image.height)
	else:
		height = round(image.width / target_ratio)
		top = (image.height - height) // 2
		box = (0, top, image.width, top + height)
	return image.crop(box)


def _process_frames() -> list[Path]:
	CINEMATIC.mkdir(parents=True, exist_ok=True)
	outputs: list[Path] = []
	for source_name, output_name in FRAMES:
		image = Image.open(SOURCE / "cinematic_raw" / source_name).convert("RGB")
		image = _center_crop_16_9(image)
		image = image.resize(FRAME_SIZE, Image.Resampling.LANCZOS)
		out = CINEMATIC / output_name
		image.save(out, optimize=True)
		outputs.append(out)
	return outputs


def _contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
	copy = image.copy()
	copy.thumbnail(size, Image.Resampling.LANCZOS)
	return copy


def _contact_sheet(
	images: list[Path],
	output: Path,
	columns: int,
	rows: int,
	title: str,
	canvas_size: int = 1024,
) -> None:
	output.parent.mkdir(parents=True, exist_ok=True)
	canvas = Image.new("RGB", (canvas_size, canvas_size), (28, 20, 43))
	draw = ImageDraw.Draw(canvas)
	font = ImageFont.load_default()
	draw.text((20, 14), title, fill=(255, 244, 219), font=font)
	margin_x = 20
	margin_top = 42
	gap = 10
	cell_w = (canvas_size - margin_x * 2 - gap * (columns - 1)) // columns
	cell_h = (canvas_size - margin_top - 20 - gap * (rows - 1)) // rows
	for index, path in enumerate(images):
		col = index % columns
		row = index // columns
		x = margin_x + col * (cell_w + gap)
		y = margin_top + row * (cell_h + gap)
		checker = Image.new("RGB", (cell_w, cell_h), (238, 230, 244))
		check_draw = ImageDraw.Draw(checker)
		step = 16
		for cy in range(0, cell_h, step):
			for cx in range(0, cell_w, step):
				if ((cx // step) + (cy // step)) % 2:
					check_draw.rectangle(
						(cx, cy, min(cx + step - 1, cell_w - 1), min(cy + step - 1, cell_h - 1)),
						fill=(218, 207, 228),
					)
		source = Image.open(path).convert("RGBA")
		thumb = _contain(source, (cell_w - 8, cell_h - 24))
		tx = (cell_w - thumb.width) // 2
		ty = (cell_h - 24 - thumb.height) // 2
		checker.paste(thumb, (tx, ty), thumb)
		label = path.stem.replace("_", " ")
		check_draw.text((4, cell_h - 18), label, fill=(51, 36, 72), font=font)
		canvas.paste(checker, (x, y))
	canvas.save(output, optimize=True)


def _validate_sprites(paths: list[Path]) -> None:
	for path in paths:
		image = Image.open(path)
		if image.mode != "RGBA" or image.size != (SPRITE_SIZE, SPRITE_SIZE):
			raise ValueError(f"{path} must be a {SPRITE_SIZE}x{SPRITE_SIZE} RGBA PNG")
		alpha = image.getchannel("A")
		if alpha.getpixel((0, 0)) != 0 or alpha.getpixel((SPRITE_SIZE - 1, SPRITE_SIZE - 1)) != 0:
			raise ValueError(f"{path} does not have transparent corners")
		bounds = alpha.getbbox()
		if bounds is None:
			raise ValueError(f"{path} is fully transparent")
		if bounds[0] < 24 or bounds[1] < 24 or bounds[2] > SPRITE_SIZE - 24 or bounds[3] > SPRITE_SIZE - 24:
			raise ValueError(f"{path} does not preserve touch/pulse padding")
		key_green_pixels = sum(
			1
			for red, green, blue, opacity in image.getdata()
			if opacity > 8 and red < 64 and green > 175 and blue < 80
		)
		if key_green_pixels:
			raise ValueError(f"{path} retains {key_green_pixels} chroma-key green pixels")


def _validate_frames(paths: list[Path]) -> None:
	for path in paths:
		image = Image.open(path)
		if image.mode != "RGB" or image.size != FRAME_SIZE:
			raise ValueError(f"{path} must be a {FRAME_SIZE[0]}x{FRAME_SIZE[1]} RGB PNG")
	expected = {path.resolve() for path in paths}
	actual = {path.resolve() for path in CINEMATIC.glob("*.png")}
	if actual != expected:
		extra = sorted(str(path) for path in actual - expected)
		missing = sorted(str(path) for path in expected - actual)
		raise ValueError(f"cinematic directory mismatch; extra={extra}, missing={missing}")


def _validate_manifest() -> None:
	manifest_path = RUNTIME / "manifest.json"
	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	for key in ("godot_handoff", "narrative_handoff", "storyboard_prompt_record"):
		handoff_path = ROOT / manifest[key].removeprefix("res://")
		if not handoff_path.is_file():
			raise ValueError(f"{key} does not exist: {handoff_path}")
	sprite_paths = [
		path
		for paths in manifest["groups"].values()
		for path in paths
	]
	frame_paths = [item["path"] for item in manifest["cinematic"]]
	if len(sprite_paths) != 96 or len(set(sprite_paths)) != 96:
		raise ValueError("manifest must enumerate 96 unique runtime sprites")
	if len(frame_paths) != 36 or len(set(frame_paths)) != 36:
		raise ValueError("manifest must enumerate 36 unique cinematic frames")
	for resource_path in sprite_paths + frame_paths:
		if not resource_path.startswith("res://"):
			raise ValueError(f"manifest path is not a Godot resource path: {resource_path}")
		if not (ROOT / resource_path.removeprefix("res://")).is_file():
			raise ValueError(f"manifest path does not exist: {resource_path}")


def main() -> None:
	sprites: list[Path] = []
	for atlas, output_dir, names in ATLASES:
		sprites.extend(_split_atlas(atlas, output_dir, names))
	_validate_sprites(sprites)
	frames = _process_frames()
	_validate_frames(frames)
	_validate_manifest()
	_contact_sheet(
		sprites,
		AUDIT / "sprites_contact.png",
		columns=12,
		rows=8,
		title="Dirty Castle cleanup runtime sprites - 96 transparent 512x512 assets",
		canvas_size=2048,
	)
	_contact_sheet(
		frames,
		AUDIT / "cinematic_contact.png",
		columns=4,
		rows=9,
		title="Dirty Castle cleanup cinematic - 36 runtime frames at 1024x576",
		canvas_size=2048,
	)
	print(f"Wrote {len(sprites)} sprites and {len(frames)} cinematic frames")


if __name__ == "__main__":
	main()
