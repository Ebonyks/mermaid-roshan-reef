#!/usr/bin/env python3
"""Build the native Pearl Castle dream-house wing and its 2D card assets.

The room shells remain deterministic 2048x2048 compositions of approved
Castle textures. Every readable furnishing and physical doorway is extracted
from one of two accepted, project-original 2D storybook sheets. The rejected
Blender QA renders remain preserved as historical sources but contribute no
runtime pixels.

The runtime sees only unshaded Sprite2D Canvas cards. Background gameplay crops are
split into exact non-overlapping tiles; transparent object cards retain their
original sheet pixels apart from chroma removal and cell cropping.
"""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ROOM_ROOT = ROOT / "assets" / "flats" / "castle" / "rooms"
TILE_ROOT = ROOM_ROOT / "background_tiles"
DREAM_ROOT = ROOT / "assets" / "flats" / "castle" / "dream_house"
MASTER_ROOT = ROOT / "assets_src" / "castle" / "dream_house_rooms_2k"
AUDIT_ROOT = ROOT / "audit" / "castle_dream_house"
IMAGEGEN_REFERENCE = (
	ROOT / "assets_src" / "imagegen" / "castle_dream_house_2026-08-01"
	/ "dining_room_reference_1254.png"
)
GENERATED_ROOT = (
	ROOT / "assets_src" / "imagegen"
	/ "castle_dream_house_2d_repair_2026-08-02"
)
DOOR_CHROMA_SHEET = GENERATED_ROOT / "door_family_sheet_chroma.png"
DOOR_ALPHA_SHEET = GENERATED_ROOT / "door_family_sheet_alpha.png"
FURNISHING_CHROMA_SHEET = GENERATED_ROOT / "furnishing_family_sheet_chroma.png"
FURNISHING_ALPHA_SHEET = GENERATED_ROOT / "furnishing_family_sheet_alpha.png"
REPAIR_PROMPTS = GENERATED_ROOT / "PROMPTS.md"

MASTER_SIZE = (2048, 2048)
GAMEPLAY_CROP = (0, 448, 2048, 1600)
GAMEPLAY_SIZE = (2048, 1152)
RUNTIME_TILE_SIZE = (1024, 576)

WALL_TEXTURE = ROOT / "assets" / "terrain" / "up_castle_col.jpg"
FLOOR_TEXTURES = {
	"family_gallery": ROOT / "assets" / "terrain" / "castle_floor_col.jpg",
	"dining_room": ROOT / "assets" / "terrain" / "kitchen_floor_col.jpg",
	"royal_bedroom": ROOT / "assets" / "terrain" / "castle_floor_col.jpg",
	"sleepover_bedroom": ROOT / "assets" / "terrain" / "bathroom_tile_col.jpg",
	"movie_lounge": ROOT / "assets" / "terrain" / "castle_carpet_col.jpg",
}

ROOMS = {
	"family_gallery": {
		"tint": (224, 202, 234),
		"floor_tint": (226, 209, 236),
		"feature": "family_gallery",
	},
	"dining_room": {
		"tint": (238, 214, 235),
		"floor_tint": (210, 244, 235),
		"feature": "door",
	},
	"royal_bedroom": {
		"tint": (239, 209, 226),
		"floor_tint": (232, 213, 231),
		"feature": "moon_window",
	},
	"sleepover_bedroom": {
		"tint": (225, 211, 242),
		"floor_tint": (238, 220, 240),
		"feature": "three_alcoves",
	},
	"movie_lounge": {
		"tint": (201, 190, 231),
		"floor_tint": (108, 78, 132),
		"feature": "screen_recess",
	},
}

FURNISHING_CELLS = {
	"dining_table.png": (0, 0),
	"dining_seat.png": (1, 0),
	"provisions_hutch.png": (2, 0),
	"meal_plate.png": (3, 0),
	"canopy_bed.png": (0, 1),
	"shell_wardrobe.png": (1, 1),
	"bedside_table.png": (2, 1),
	"story_cushion.png": (3, 1),
	"dream_bed_0.png": (0, 2),
	"dream_bed_1.png": (1, 2),
	"dream_bed_2.png": (2, 2),
	"shell_chandelier.png": (3, 2),
	"cloud_settee.png": (0, 3),
	"cloud_pouf.png": (1, 3),
	"movie_screen_frame.png": (2, 3),
	"shell_popcorn_bowl.png": (3, 3),
}

# Four approved silhouettes cross their nominal 4x4 cells. These generous
# regions contain the complete source object, stay clear of every neighboring
# object, and are intentionally fixed so the extraction remains reproducible.
FURNISHING_REPAIR_REGIONS = {
	"dining_table.png": (16, 89, 410, 331),
	"canopy_bed.png": (11, 349, 337, 681),
	"story_cushion.png": (923, 398, 1233, 673),
	"movie_screen_frame.png": (603, 931, 950, 1210),
}
FURNISHING_REPAIR_CANVASES = {
	"dining_table.png": (292, 223),
	"canopy_bed.png": (296, 272),
	"story_cushion.png": (287, 223),
	"movie_screen_frame.png": (313, 264),
}

# The door sheet is intentionally asymmetric: three portals on the first row,
# two centered on the second. Regions are generous and never overlap.
DOOR_SHEET_REGIONS = {
	"family_wing_portal.png": (0, 0, 560, 512),
	"family_portal_dining.png": (560, 0, 1024, 512),
	"family_portal_royal_bedroom.png": (1024, 0, 1536, 512),
	"family_portal_sleepover_bedroom.png": (250, 512, 760, 1024),
	"family_portal_movie_lounge.png": (760, 512, 1270, 1024),
}
FURNISHED_PREVIEW_PLACEMENTS: dict[str, list[dict[str, object]]] = {
	"family_gallery": [
		{"id": "gallery_dining_door", "file": "family_portal_dining.png",
			"pos": (-40.0, 79.0), "scale": 0.60, "z": 0.86},
		{"id": "gallery_royal_bedroom_door",
			"file": "family_portal_royal_bedroom.png",
			"pos": (200.0, 77.0), "scale": 0.60, "z": 0.87},
		{"id": "gallery_sleepover_door",
			"file": "family_portal_sleepover_bedroom.png",
			"pos": (448.0, 89.0), "scale": 0.60, "z": 0.88},
		{"id": "gallery_movie_door",
			"file": "family_portal_movie_lounge.png",
			"pos": (680.0, 89.0), "scale": 0.60, "z": 0.89},
	],
	"dining_room": [
		{"id": "dining_chandelier", "file": "shell_chandelier.png",
			"pos": (408.0, -28.0), "scale": 0.68, "z": 0.72},
		{"id": "provisions_hutch", "file": "provisions_hutch.png",
			"pos": (33.0, 155.0), "scale": 0.78, "z": 0.82},
		{"id": "dining_table", "file": "dining_table.png",
			"pos": (366.0, 264.0), "scale": 1.14, "z": 2.05},
		{"id": "dining_seat_left", "file": "dining_seat.png",
			"pos": (175.0, 357.0), "scale": 0.86, "z": 2.32},
		{"id": "dining_seat_right", "file": "dining_seat.png",
			"pos": (670.0, 357.0), "scale": 0.86, "z": 2.32,
			"flip_h": True},
		*[
			{"id": f"meal_plate_{index}", "file": "meal_plate.png",
				"pos": position, "scale": 0.20, "z": 2.46 + index * 0.01}
			for index, position in enumerate([
				(277.0, 262.0), (342.0, 248.0), (407.0, 248.0),
				(472.0, 262.0), (327.0, 290.0), (417.0, 290.0)])
		],
	],
	"royal_bedroom": [
		{"id": "shell_wardrobe", "file": "shell_wardrobe.png",
			"pos": (52.0, 164.0), "scale": 0.83, "z": 0.92},
		{"id": "canopy_bed", "file": "canopy_bed.png",
			"pos": (353.0, 175.0), "scale": 1.25, "z": 1.20},
		{"id": "bedside_table", "file": "bedside_table.png",
			"pos": (681.0, 214.0), "scale": 0.63, "z": 1.42},
		{"id": "reading_cushion", "file": "story_cushion.png",
			"pos": (742.0, 349.0), "scale": 0.44, "z": 2.25},
	],
	"sleepover_bedroom": [
		{"id": "sleepover_chandelier", "file": "shell_chandelier.png",
			"pos": (408.0, -33.0), "scale": 0.54, "z": 0.72},
		{"id": "dream_bed_0", "file": "dream_bed_0.png",
			"pos": (83.0, 290.0), "scale": 0.88, "z": 1.90},
		{"id": "dream_bed_1", "file": "dream_bed_1.png",
			"pos": (387.0, 287.0), "scale": 0.88, "z": 1.92},
		{"id": "dream_bed_2", "file": "dream_bed_2.png",
			"pos": (688.0, 292.0), "scale": 0.88, "z": 1.94},
	],
	"movie_lounge": [
		{"id": "movie_screen", "file": "movie_screen_frame.png",
			"pos": (356.0, 98.0), "scale": 1.60, "z": 0.76},
		{"id": "cloud_settee_left", "file": "cloud_settee.png",
			"pos": (109.0, 351.0), "scale": 0.74, "z": 2.12},
		{"id": "cloud_settee_right", "file": "cloud_settee.png",
			"pos": (613.0, 351.0), "scale": 0.74, "z": 2.12,
			"flip_h": True},
		{"id": "cloud_pouf", "file": "cloud_pouf.png",
			"pos": (402.0, 396.0), "scale": 0.62, "z": 2.52},
		{"id": "movie_popcorn", "file": "shell_popcorn_bowl.png",
			"pos": (412.0, 333.0), "scale": 0.25, "z": 2.64},
	],
}

HALL_SCREEN_A_SOURCE = (
	ROOT / "assets_src" / "castle" / "main_hall_alignment"
	/ "main_hall_screen_a_fixture_aligned_master.png"
)
HALL_SCREEN_A_CROP = (376, 212, 2048, 1153)


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def tile_image(path: Path, size: tuple[int, int], tile_px: int = 512) -> Image.Image:
	source = Image.open(path).convert("RGB").resize(
		(tile_px, tile_px), Image.Resampling.LANCZOS)
	result = Image.new("RGB", size)
	for y in range(0, size[1], tile_px):
		for x in range(0, size[0], tile_px):
			result.paste(source, (x, y))
	return result


def tint(image: Image.Image, color: tuple[int, int, int], amount: float) -> Image.Image:
	overlay = Image.new("RGB", image.size, color)
	return Image.blend(image, overlay, amount)


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int, int],
		bottom: tuple[int, int, int, int]) -> Image.Image:
	strip = Image.new("RGBA", (1, size[1]))
	pixels = strip.load()
	for y in range(size[1]):
		t = y / max(1, size[1] - 1)
		pixels[0, y] = tuple(
			int(round(top[index] + (bottom[index] - top[index]) * t))
			for index in range(4)
		)
	return strip.resize(size, Image.Resampling.BILINEAR)


def draw_arch(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
		fill: tuple[int, int, int, int], outline: tuple[int, int, int, int],
		width: int = 28) -> None:
	left, top, right, bottom = box
	radius = (right - left) // 2
	draw.rectangle((left, top + radius, right, bottom), fill=fill)
	draw.pieslice((left, top, right, top + radius * 2), 180, 360, fill=fill)
	draw.line((left, top + radius, left, bottom), fill=outline, width=width)
	draw.line((right, top + radius, right, bottom), fill=outline, width=width)
	draw.arc((left, top, right, top + radius * 2), 180, 360,
		fill=outline, width=width)


def build_room_master(room_id: str, config: dict[str, object]) -> Image.Image:
	wall = tile_image(WALL_TEXTURE, MASTER_SIZE, 384)
	wall = tint(wall, config["tint"], 0.23)
	wall = ImageEnhance.Contrast(wall).enhance(0.92)
	canvas = wall.convert("RGBA")

	# A vaulted ceiling and a pearl rail give the empty shell the same broad,
	# child-readable architecture as the approved flattened castle rooms.
	draw = ImageDraw.Draw(canvas, "RGBA")
	draw.ellipse((-420, -900, 2468, 720), fill=(74, 49, 105, 74),
		outline=(240, 207, 164, 215), width=26)
	draw.rounded_rectangle((70, 304, 1978, 372), radius=34,
		fill=(246, 220, 192, 228), outline=(109, 72, 119, 230), width=10)
	draw.rounded_rectangle((86, 326, 1962, 352), radius=13,
		fill=(192, 147, 182, 210))

	# Floor starts inside the playable band. The source texture remains whole;
	# soft perspective lines supply depth without warping readable objects.
	floor_y = 1110
	floor = tile_image(FLOOR_TEXTURES[room_id], (2048, 938), 384)
	floor = tint(floor, config["floor_tint"], 0.18)
	floor = ImageEnhance.Brightness(floor).enhance(1.06)
	floor.putalpha(vertical_gradient(floor.size,
		(255, 255, 255, 220), (255, 255, 255, 255)).getchannel("A"))
	canvas.alpha_composite(floor, (0, floor_y))
	draw = ImageDraw.Draw(canvas, "RGBA")
	draw.rounded_rectangle((0, floor_y - 34, 2048, floor_y + 34), radius=20,
		fill=(245, 218, 190, 235), outline=(102, 67, 117, 235), width=10)
	vanish = (1024, floor_y + 4)
	for bottom_x in range(-320, 2369, 224):
		draw.line((vanish[0], vanish[1], bottom_x, 2048),
			fill=(91, 67, 111, 62), width=7)
	for step in range(1, 8):
		t = step / 8.0
		y = int(floor_y + (t ** 1.62) * (2048 - floor_y))
		draw.line((0, y, 2048, y), fill=(91, 67, 111, 54), width=7)

	# Side pilasters keep every room in the approved Pearl Castle material
	# language while leaving the center open for independent prop cards.
	for center_x in (110, 1938):
		draw.rounded_rectangle((center_x - 62, 360, center_x + 62, 1138),
			radius=48, fill=(224, 196, 221, 235),
			outline=(93, 61, 112, 235), width=12)
		draw.ellipse((center_x - 86, 316, center_x + 86, 440),
			fill=(247, 221, 195, 240), outline=(93, 61, 112, 235), width=10)
		draw.rounded_rectangle((center_x - 88, 1086, center_x + 88, 1150),
			radius=24, fill=(246, 219, 190, 240),
			outline=(93, 61, 112, 235), width=10)

	feature = str(config["feature"])
	if feature == "family_gallery":
		# Four architectural bays make the new wing's topology visible before
		# its independent picture-door cards are added at runtime.
		draw.rounded_rectangle((126, 470, 1922, 1430), radius=92,
			fill=(196, 167, 211, 92), outline=(244, 218, 194, 230), width=24)
		for center_x in (300, 770, 1240, 1710):
			draw_arch(draw, (center_x - 190, 690, center_x + 190, 1390),
				(73, 52, 105, 155), (237, 207, 190, 235), 22)
			draw.ellipse((center_x - 66, 584, center_x + 66, 716),
				fill=(247, 219, 190, 235), outline=(99, 65, 116, 235), width=12)
	elif feature == "door":
		draw_arch(draw, (792, 486, 1256, 1118),
			(112, 201, 203, 245), (245, 217, 192, 255), 34)
		draw_arch(draw, (842, 540, 1206, 1118),
			(83, 157, 172, 235), (111, 72, 122, 220), 18)
	elif feature == "moon_window":
		draw_arch(draw, (760, 458, 1288, 1010),
			(112, 197, 211, 230), (244, 219, 197, 255), 34)
		draw.ellipse((886, 560, 1086, 760), fill=(255, 236, 164, 238))
		draw.ellipse((952, 520, 1125, 720), fill=(112, 197, 211, 255))
	elif feature == "three_alcoves":
		for left in (238, 774, 1310):
			draw_arch(draw, (left, 520, left + 500, 1118),
				(103, 77, 132, 160), (243, 217, 196, 235), 24)
	elif feature == "screen_recess":
		# The authored 2D movie-screen card supplies the complete surround.
		# Leaving the wall uninterrupted prevents a doubled picture-frame read.
		pass

	# Room-specific rugs remain background regions, never duplicated furniture.
	if room_id == "family_gallery":
		draw.rounded_rectangle((170, 1435, 1878, 1910), radius=180,
			fill=(130, 91, 162, 105), outline=(246, 216, 188, 190), width=20)
		for center_x in (330, 790, 1250, 1710):
			draw.ellipse((center_x - 22, 1550, center_x + 22, 1594),
				fill=(248, 214, 142, 140), outline=(102, 67, 117, 170), width=7)
	elif room_id in ("royal_bedroom", "sleepover_bedroom"):
		rug_color = (205, 126, 174, 120) if room_id == "royal_bedroom" \
			else (150, 119, 203, 110)
		draw.ellipse((320, 1250, 1728, 1900), fill=rug_color,
			outline=(246, 216, 188, 190), width=20)
	elif room_id == "movie_lounge":
		for x in range(250, 1800, 250):
			for y in range(1260, 1900, 220):
				draw.regular_polygon((x, y, 14), n_sides=5, rotation=-18,
					fill=(247, 220, 138, 82))

	# Warm center light, cool vignette, and faint paper grain complete the
	# flattened storybook read without any runtime shader dependency.
	light = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
	light_draw = ImageDraw.Draw(light, "RGBA")
	for radius in range(980, 80, -70):
		alpha = int(3 + (980 - radius) / 900 * 3)
		light_draw.ellipse((1024 - radius, 780 - radius,
			1024 + radius, 780 + radius), fill=(255, 222, 175, alpha))
	canvas = Image.alpha_composite(canvas, light.filter(ImageFilter.GaussianBlur(36)))
	vignette = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
	vignette_draw = ImageDraw.Draw(vignette, "RGBA")
	for inset in range(0, 180, 12):
		alpha = int(18 * (1.0 - inset / 180.0))
		vignette_draw.rounded_rectangle((inset, inset, 2047 - inset, 2047 - inset),
			radius=180, outline=(42, 24, 70, alpha), width=18)
	canvas = Image.alpha_composite(canvas, vignette)
	return canvas.convert("RGB")


def largest_alpha_component(image: Image.Image) -> Image.Image:
	image = image.convert("RGBA")
	width, height = image.size
	alpha = bytearray(image.getchannel("A").tobytes())
	visited = bytearray(width * height)
	best: list[int] = []
	for start, value in enumerate(alpha):
		if value <= 8 or visited[start]:
			continue
		visited[start] = 1
		queue: deque[int] = deque([start])
		component: list[int] = []
		while queue:
			index = queue.popleft()
			component.append(index)
			x = index % width
			y = index // width
			for neighbor in (
					index - 1 if x > 0 else -1,
					index + 1 if x + 1 < width else -1,
					index - width if y > 0 else -1,
					index + width if y + 1 < height else -1):
				if neighbor >= 0 and alpha[neighbor] > 8 and (
						not visited[neighbor]):
					visited[neighbor] = 1
					queue.append(neighbor)
		if len(component) > len(best):
			best = component
	kept_alpha = bytearray(width * height)
	for index in best:
		kept_alpha[index] = alpha[index]
	image.putalpha(Image.frombytes("L", image.size, bytes(kept_alpha)))
	return image


def crop_alpha(image: Image.Image, padding: int = 6) -> Image.Image:
	image = image.convert("RGBA")
	bbox = image.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("transparent source has no opaque pixels")
	left = max(0, bbox[0] - padding)
	top = max(0, bbox[1] - padding)
	right = min(image.width, bbox[2] + padding)
	bottom = min(image.height, bbox[3] + padding)
	return image.crop((left, top, right, bottom))


def grid_cell_box(image: Image.Image, column: int, row: int,
		columns: int = 4, rows: int = 4) -> tuple[int, int, int, int]:
	return (
		round(column * image.width / columns),
		round(row * image.height / rows),
		round((column + 1) * image.width / columns),
		round((row + 1) * image.height / rows),
	)


def extract_sheet_region(sheet: Image.Image,
		region: tuple[int, int, int, int],
		largest_only: bool = False) -> Image.Image:
	image = crop_alpha(sheet.crop(region), padding=4)
	if largest_only:
		image = crop_alpha(largest_alpha_component(image), padding=4)
	return image


def alpha_profile(image: Image.Image) -> dict[str, object]:
	"""Return deterministic edge, dimension, and alpha-bbox-center data."""
	alpha = image.convert("RGBA").getchannel("A")
	bbox = alpha.getbbox()
	if bbox is None:
		raise ValueError("transparent image has no opaque pixels")
	center_x = (bbox[0] + bbox[2]) * 0.5
	center_y = (bbox[1] + bbox[3]) * 0.5
	return {
		"dimensions": list(image.size),
		"alpha_bbox": list(bbox),
		"alpha_edge_margins": [
			bbox[0], bbox[1], image.width - bbox[2], image.height - bbox[3]],
		"alpha_center_normalized": [
			center_x / image.width,
			center_y / image.height],
	}


def contain_fit_repaired_region(sheet: Image.Image,
		region: tuple[int, int, int, int],
		target_size: tuple[int, int],
		target_center_normalized: tuple[float, float]) -> Image.Image:
	"""Fit a complete approved silhouette into its existing runtime card.

	The tight source alpha bounds are scaled down only as much as needed for a
	4px transparent safety margin. Placement is then solved against the legacy
	card's weighted alpha center, so runtime positions and scales remain stable.
	"""
	source = sheet.crop(region).convert("RGBA")
	source_bbox = source.getchannel("A").getbbox()
	if source_bbox is None:
		raise ValueError(f"repaired source region is empty: {region}")
	object_image = source.crop(source_bbox)
	object_width, object_height = object_image.size
	object_center = alpha_profile(object_image)["alpha_center_normalized"]
	source_center_x = float(object_center[0]) * object_width
	source_center_y = float(object_center[1]) * object_height
	target_width, target_height = target_size
	target_center_x = float(target_center_normalized[0]) * target_width
	target_center_y = float(target_center_normalized[1]) * target_height
	margin = 4.0
	limits = [
		(target_width - 2.0 * margin) / object_width,
		(target_height - 2.0 * margin) / object_height,
	]
	if source_center_x > 0.0:
		limits.append((target_center_x - margin) / source_center_x)
	if object_width - source_center_x > 0.0:
		limits.append((target_width - margin - target_center_x)
			/ (object_width - source_center_x))
	if source_center_y > 0.0:
		limits.append((target_center_y - margin) / source_center_y)
	if object_height - source_center_y > 0.0:
		limits.append((target_height - margin - target_center_y)
			/ (object_height - source_center_y))
	scale = min(1.0, *limits)
	if scale <= 0.0:
		raise ValueError(
			f"repaired source cannot fit {target_size}: {region}")
	resized = object_image.resize((
		max(1, round(object_width * scale)),
		max(1, round(object_height * scale))), Image.Resampling.LANCZOS)
	resized_center = alpha_profile(resized)["alpha_center_normalized"]
	resized_center_x = float(resized_center[0]) * resized.width
	resized_center_y = float(resized_center[1]) * resized.height
	left = round(target_center_x - resized_center_x)
	top = round(target_center_y - resized_center_y)
	card = Image.new("RGBA", target_size, (0, 0, 0, 0))
	card.alpha_composite(resized, (left, top))
	return card


def furnishing_source_regions_non_overlapping() -> list[dict[str, object]]:
	"""Report any intersection among the four repaired source regions."""
	items = list(FURNISHING_REPAIR_REGIONS.items())
	overlaps: list[dict[str, object]] = []
	for index, (left_name, left_region) in enumerate(items):
		for right_name, right_region in items[index + 1:]:
			width = max(0, min(left_region[2], right_region[2])
				- max(left_region[0], right_region[0]))
			height = max(0, min(left_region[3], right_region[3])
				- max(left_region[1], right_region[1]))
			if width > 0 and height > 0:
				overlaps.append({
					"left": left_name,
					"right": right_name,
					"intersection": [width, height],
				})
	return overlaps


def generated_record(output_path: Path, source_path: Path,
		source_region: tuple[int, int, int, int]) -> dict[str, object]:
	with Image.open(output_path) as image:
		dimensions = list(image.size)
	return {
		"path": output_path.relative_to(ROOT).as_posix(),
		"dimensions": dimensions,
		"sha256": sha256(output_path),
		"source": source_path.relative_to(ROOT).as_posix(),
		"source_sha256": sha256(source_path),
		"source_region": list(source_region),
		"transform": (
			"built-in ImageGen 2D storybook sheet; flat chroma removed with "
			"the installed ImageGen helper; deterministic cell crop or "
			"preservation-first source-region contain-fit"),
		"blender_runtime_pixels": False,
	}


def build_prop_assets() -> list[dict[str, object]]:
	records: list[dict[str, object]] = []
	with Image.open(FURNISHING_ALPHA_SHEET) as source:
		sheet = source.convert("RGBA")
		for output_name, (column, row) in FURNISHING_CELLS.items():
			legacy_region = grid_cell_box(sheet, column, row)
			legacy_image = extract_sheet_region(
				sheet, legacy_region, largest_only=output_name != "meal_plate.png")
			if output_name in FURNISHING_REPAIR_REGIONS:
				target_size = FURNISHING_REPAIR_CANVASES[output_name]
				if legacy_image.size != target_size:
					raise RuntimeError(
						f"legacy canvas changed for {output_name}: "
						f"{legacy_image.size} != {target_size}")
				legacy_profile = alpha_profile(legacy_image)
				region = FURNISHING_REPAIR_REGIONS[output_name]
				image = contain_fit_repaired_region(
					sheet, region, target_size, tuple(
						float(value) for value in legacy_profile[
							"alpha_center_normalized"]))
			else:
				region = legacy_region
				image = legacy_image
			output_path = DREAM_ROOT / output_name
			# Use an explicit binary handle for the repaired cards. This keeps the
			# deterministic overwrite stable on Windows when an audit viewer has a
			# read handle open on a prior generated card.
			if output_name in FURNISHING_REPAIR_REGIONS:
				with output_path.open("wb") as stream:
					image.save(stream, format="PNG", optimize=True)
			else:
				image.save(output_path, format="PNG", optimize=True)
			record = generated_record(
				output_path, FURNISHING_ALPHA_SHEET, region)
			if output_name in FURNISHING_REPAIR_REGIONS:
				after = alpha_profile(image)
				before = alpha_profile(legacy_image)
				before_center = before["alpha_center_normalized"]
				after_center = after["alpha_center_normalized"]
				record["preservation_repair"] = {
					"before": before,
					"after": after,
					"alpha_center_delta": [
						float(after_center[0]) - float(before_center[0]),
						float(after_center[1]) - float(before_center[1])],
					"source_region_non_overlapping": True,
				}
			records.append(record)
	return records


def build_family_portal_assets() -> list[dict[str, object]]:
	records: list[dict[str, object]] = []
	with Image.open(DOOR_ALPHA_SHEET) as source:
		sheet = source.convert("RGBA")
		for output_name, region in DOOR_SHEET_REGIONS.items():
			image = extract_sheet_region(
				sheet, region, largest_only=output_name != "meal_plate.png")
			output_path = DREAM_ROOT / output_name
			image.save(output_path, format="PNG", optimize=True)
			records.append(generated_record(
				output_path, DOOR_ALPHA_SHEET, region))
			if output_name == "family_wing_portal.png":
				insert_path = DREAM_ROOT / "family_wing_hall_insert.png"
				image.save(insert_path, format="PNG", optimize=True)
				records.append(generated_record(
					insert_path, DOOR_ALPHA_SHEET, region))
	return records


def build_furnished_room_contact(
		preview_by_room: dict[str, Image.Image]) -> dict[str, object]:
	room_order = [
		"dining_room", "royal_bedroom",
		"sleepover_bedroom", "movie_lounge"]
	contact = Image.new("RGBA", (2048, 1152), (27, 19, 49, 255))
	placement_records: list[dict[str, object]] = []
	for room_index, room_id in enumerate(room_order):
		stage = preview_by_room[room_id].convert("RGBA")
		for item in sorted(
				FURNISHED_PREVIEW_PLACEMENTS[room_id],
				key=lambda value: float(value["z"])):
			source_path = DREAM_ROOT / str(item["file"])
			with Image.open(source_path) as source:
				card = source.convert("RGBA")
			if bool(item.get("flip_h", False)):
				card = card.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
			scale = float(item["scale"])
			rendered_size = (
				max(1, round(card.width * scale)),
				max(1, round(card.height * scale)))
			rendered = card.resize(rendered_size, Image.Resampling.LANCZOS)
			source_x, source_y = item["pos"]
			left = round(float(source_x) + card.width * 0.5
				- rendered.width * 0.5)
			top = round(float(source_y) + card.height * 0.5
				- rendered.height * 0.5)
			stage.alpha_composite(rendered, (left, top))
			right = left + rendered.width
			bottom = top + rendered.height
			clipped_width = max(0, min(1024, right) - max(0, left))
			clipped_height = max(0, min(576, bottom) - max(0, top))
			placement_records.append({
				"room_id": room_id,
				"item_id": str(item["id"]),
				"asset": source_path.relative_to(ROOT).as_posix(),
				"source_position": [float(source_x), float(source_y)],
				"uniform_scale": scale,
				"rendered_bbox": [left, top, right, bottom],
				"visible_fraction": round(
					clipped_width * clipped_height
					/ max(1, rendered.width * rendered.height), 6),
				"z": float(item["z"]),
			})
		contact.alpha_composite(
			stage, ((room_index % 2) * 1024, (room_index // 2) * 576))

	contact_path = (
		AUDIT_ROOT / "dream_house_furnished_rooms_contact.png")
	contact.convert("RGB").save(contact_path, format="PNG", optimize=True)

	critical_groups = {
		"gallery_doors": [
			value for value in FURNISHED_PREVIEW_PLACEMENTS["family_gallery"]],
		"sleepover_beds": [
			value for value in FURNISHED_PREVIEW_PLACEMENTS["sleepover_bedroom"]
			if str(value["id"]).startswith("dream_bed_")],
	}
	critical_overlaps: list[dict[str, object]] = []
	for group_id, items in critical_groups.items():
		rendered_rects: list[tuple[str, tuple[float, float, float, float]]] = []
		for item in items:
			with Image.open(DREAM_ROOT / str(item["file"])) as source:
				width, height = source.size
			scale = float(item["scale"])
			x, y = item["pos"]
			left = float(x) + width * (1.0 - scale) * 0.5
			top = float(y) + height * (1.0 - scale) * 0.5
			rendered_rects.append((str(item["id"]), (
				left, top, left + width * scale, top + height * scale)))
		for index, (left_id, left_rect) in enumerate(rendered_rects):
			for right_id, right_rect in rendered_rects[index + 1:]:
				intersection_width = max(0.0,
					min(left_rect[2], right_rect[2])
					- max(left_rect[0], right_rect[0]))
				intersection_height = max(0.0,
					min(left_rect[3], right_rect[3])
					- max(left_rect[1], right_rect[1]))
				if intersection_width > 0.5 and intersection_height > 0.5:
					critical_overlaps.append({
						"group": group_id,
						"left": left_id,
						"right": right_id,
						"overlap": [
							round(intersection_width, 3),
							round(intersection_height, 3)],
					})
	return {
		"path": contact_path.relative_to(ROOT).as_posix(),
		"sha256": sha256(contact_path),
		"dimensions": list(contact.size),
		"rooms": room_order,
		"placements": placement_records,
		"critical_overlaps": critical_overlaps,
		"protected_movie_pixels_copied": False,
	}


def exact_equal(left: Image.Image, right: Image.Image) -> bool:
	return ImageChops.difference(left, right).getbbox() is None


def build() -> None:
	for directory in (DREAM_ROOT, MASTER_ROOT, TILE_ROOT, AUDIT_ROOT):
		directory.mkdir(parents=True, exist_ok=True)

	records: list[dict[str, object]] = []
	# Write the small transparent cards before the large room image batch. This
	# keeps deterministic PNG replacement reliable on Windows under concurrent
	# audit/read handles without changing any generated content or paths.
	prop_records = build_prop_assets()
	previews: list[Image.Image] = []
	preview_by_room: dict[str, Image.Image] = {}
	for room_id, config in ROOMS.items():
		master = build_room_master(room_id, config)
		master_path = MASTER_ROOT / f"room_{room_id}_background_master.png"
		master.save(master_path, format="PNG", optimize=True)
		gameplay = master.crop(GAMEPLAY_CROP)
		preview_path = ROOM_ROOT / f"room_{room_id}_background.png"
		preview = gameplay.resize((1024, 576), Image.Resampling.LANCZOS)
		preview.save(preview_path, format="PNG", optimize=True)
		previews.append(preview)
		preview_by_room[room_id] = preview

		reconstruction = Image.new("RGB", GAMEPLAY_SIZE)
		tiles: list[dict[str, object]] = []
		for row in range(2):
			for column in range(2):
				left = column * RUNTIME_TILE_SIZE[0]
				top = row * RUNTIME_TILE_SIZE[1]
				box = (left, top, left + RUNTIME_TILE_SIZE[0],
					top + RUNTIME_TILE_SIZE[1])
				tile = gameplay.crop(box)
				tile_path = TILE_ROOT / (
					f"room_{room_id}_background_r{row}_c{column}.png")
				tile.save(tile_path, format="PNG", optimize=True)
				reconstruction.paste(tile, (left, top))
				tiles.append({
					"row": row,
					"column": column,
					"path": tile_path.relative_to(ROOT).as_posix(),
					"dimensions": list(tile.size),
					"master_rectangle": list(box),
					"sha256": sha256(tile_path),
				})
		if not exact_equal(gameplay, reconstruction):
			raise RuntimeError(f"{room_id} runtime tiles do not reconstruct")
		records.append({
			"room_id": room_id,
			"master": master_path.relative_to(ROOT).as_posix(),
			"master_dimensions": list(master.size),
			"master_sha256": sha256(master_path),
			"runtime_crop": list(GAMEPLAY_CROP),
			"runtime_crop_dimensions": list(gameplay.size),
			"preview": preview_path.relative_to(ROOT).as_posix(),
			"preview_dimensions": list(preview.size),
			"preview_sha256": sha256(preview_path),
			"tiles": tiles,
		})

	prop_records.extend(build_family_portal_assets())
	furnished_review = build_furnished_room_contact(preview_by_room)
	repaired_props = [
		record for record in prop_records
		if "preservation_repair" in record]
	region_overlaps = furnishing_source_regions_non_overlapping()
	if region_overlaps:
		raise RuntimeError(
			f"repaired furnishing source regions overlap: {region_overlaps}")

	contact = Image.new("RGB", (1536, 576), (27, 19, 49))
	for index, preview in enumerate(previews):
		contact.paste(preview.resize((512, 288), Image.Resampling.LANCZOS),
			((index % 3) * 512, (index // 3) * 288))
	contact_path = AUDIT_ROOT / "dream_house_room_shells_contact.png"
	contact.save(contact_path, format="PNG", optimize=True)

	# Stage the exact physical gallery doors over its native-backed runtime
	# preview so human review covers the new layout, not only empty shells.
	gallery_stage = preview_by_room["family_gallery"].convert("RGBA")
	portal_names = [
		"family_portal_dining.png",
		"family_portal_royal_bedroom.png",
		"family_portal_sleepover_bedroom.png",
		"family_portal_movie_lounge.png",
	]
	for index, portal_name in enumerate(portal_names):
		portal = Image.open(DREAM_ROOT / portal_name).convert("RGBA")
		portal.thumbnail((210, 280), Image.Resampling.LANCZOS)
		center_x = 150 + index * 235
		gallery_stage.alpha_composite(
			portal, (round(center_x - portal.width / 2), 496 - portal.height))
	layout_contact = Image.new("RGBA", (1280, 576), (27, 19, 49, 255))
	layout_contact.alpha_composite(gallery_stage, (0, 0))
	hall_insert = Image.open(
		DREAM_ROOT / "family_wing_hall_insert.png").convert("RGBA")
	hall_insert.thumbnail((240, 440), Image.Resampling.LANCZOS)
	layout_contact.alpha_composite(hall_insert, (1035, 78))
	layout_draw = ImageDraw.Draw(layout_contact, "RGBA")
	layout_draw.line((1012, 288, 1036, 288), fill=(248, 216, 150, 255), width=8)
	layout_draw.polygon(((1028, 278), (1044, 288), (1028, 298)),
		fill=(248, 216, 150, 255))
	layout_contact_path = AUDIT_ROOT / "dream_house_layout_contact.png"
	layout_contact.convert("RGB").save(
		layout_contact_path, format="PNG", optimize=True)

	with Image.open(HALL_SCREEN_A_SOURCE) as source:
		hall_entry_review = source.crop(HALL_SCREEN_A_CROP).convert("RGBA")
	with Image.open(DREAM_ROOT / "family_wing_hall_insert.png") as source:
		hall_entry_review.alpha_composite(source.convert("RGBA"), (35, 200))
	hall_entry_contact = hall_entry_review.resize(
		(1024, 576), Image.Resampling.LANCZOS)
	hall_entry_contact_path = (
		AUDIT_ROOT / "dream_house_hall_entry_contact.png")
	hall_entry_contact.convert("RGB").save(
		hall_entry_contact_path, format="PNG", optimize=True)

	manifest = {
		"schema": "castle_dream_house_room_art_v3",
		"method": "native room shells plus two accepted 2D storybook production sheets; no Blender render pixels",
		"imagegen_reference": {
			"path": IMAGEGEN_REFERENCE.relative_to(ROOT).as_posix(),
			"exists": IMAGEGEN_REFERENCE.exists(),
			"sha256": sha256(IMAGEGEN_REFERENCE) if IMAGEGEN_REFERENCE.exists() else "",
			"role": "composition_reference_only",
			"used_as_runtime_pixels": False,
		},
		"production_sheets": [
			{
				"role": "physical_door_family",
				"prompt_id": "physical-door-family",
				"prompt_path": REPAIR_PROMPTS.relative_to(ROOT).as_posix(),
				"prompt_sha256": sha256(REPAIR_PROMPTS),
				"chroma_path": DOOR_CHROMA_SHEET.relative_to(ROOT).as_posix(),
				"chroma_sha256": sha256(DOOR_CHROMA_SHEET),
				"alpha_path": DOOR_ALPHA_SHEET.relative_to(ROOT).as_posix(),
				"alpha_sha256": sha256(DOOR_ALPHA_SHEET),
				"dimensions": list(Image.open(DOOR_ALPHA_SHEET).size),
			},
			{
				"role": "four_room_furnishing_family",
				"prompt_id": "four-room-furnishing-family",
				"prompt_path": REPAIR_PROMPTS.relative_to(ROOT).as_posix(),
				"prompt_sha256": sha256(REPAIR_PROMPTS),
				"chroma_path": FURNISHING_CHROMA_SHEET.relative_to(ROOT).as_posix(),
				"chroma_sha256": sha256(FURNISHING_CHROMA_SHEET),
				"alpha_path": FURNISHING_ALPHA_SHEET.relative_to(ROOT).as_posix(),
				"alpha_sha256": sha256(FURNISHING_ALPHA_SHEET),
				"dimensions": list(Image.open(FURNISHING_ALPHA_SHEET).size),
			},
		],
		"blender_runtime_pixels": False,
		"background_sources": [
			{"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
			for path in [WALL_TEXTURE, *FLOOR_TEXTURES.values()]
		],
		"rooms": records,
		"props": prop_records,
		"furnishing_repair_audit": {
			"source_sheet": FURNISHING_ALPHA_SHEET.relative_to(ROOT).as_posix(),
			"source_sheet_sha256": sha256(FURNISHING_ALPHA_SHEET),
			"source_region_non_overlaps": region_overlaps,
			"objects": repaired_props,
			"contact_evidence": {
				"path": furnished_review["path"],
				"sha256": furnished_review["sha256"],
				"dimensions": furnished_review["dimensions"],
			},
		},
		"furnished_room_review": furnished_review,
		"contact_sheet": contact_path.relative_to(ROOT).as_posix(),
		"layout_contact": {
			"path": layout_contact_path.relative_to(ROOT).as_posix(),
			"sha256": sha256(layout_contact_path),
		},
		"hall_entry_contact": {
			"path": hall_entry_contact_path.relative_to(ROOT).as_posix(),
			"sha256": sha256(hall_entry_contact_path),
			"source": HALL_SCREEN_A_SOURCE.relative_to(ROOT).as_posix(),
			"source_sha256": sha256(HALL_SCREEN_A_SOURCE),
			"source_crop": list(HALL_SCREEN_A_CROP),
			"insert_position": [35, 200],
		},
		"physical_layout": {
			"main_hall_entry": (
				"assets/flats/castle/dream_house/family_wing_hall_insert.png"),
			"main_hall_entry_runtime_mode": (
				"source_owned_hall_background_portal_with_sprite2d_sign"),
			"main_hall_entry_separate_insert_loaded": False,
			"gallery_room": "family_gallery",
			"destinations": {
				"dining_room": "family_portal_dining.png",
				"royal_bedroom": "family_portal_royal_bedroom.png",
				"sleepover_bedroom": "family_portal_sleepover_bedroom.png",
				"movie_lounge": "family_portal_movie_lounge.png",
			},
			"floating_route_buttons": False,
		},
		"node_type_inventory": {
			"world_art_node": "Sprite2D Canvas",
			"world_art_builder": "_new_card",
			"world_art_material": "unshaded storybook card",
			"forbidden_world_nodes": [],
			"hud_exception": "Control and CanvasItem only",
		},
		"source_visual_medium": "polished flattened 2D storybook illustration",
		"protected_originals_modified": False,
		"runtime_world_art": "unshaded Sprite2D Canvas cards only",
	}
	manifest_path = AUDIT_ROOT / "dream_house_room_art_manifest.json"
	manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(json.dumps({
		"rooms": len(records),
		"props": len(prop_records),
		"manifest": manifest_path.relative_to(ROOT).as_posix(),
	}, indent=2))


if __name__ == "__main__":
	build()
