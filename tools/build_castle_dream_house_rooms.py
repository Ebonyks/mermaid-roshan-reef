#!/usr/bin/env python3
"""Build native-square Pearl Castle dream-house wing art from approved parts.

The room shells are deterministic 2048x2048 compositions of the project's
approved seamless castle textures. Readable furniture stays on independent
transparent Sprite3D cards copied non-destructively from the approved Blender
QA renders. The runtime sees only the centered 2048x1152 gameplay crop, split
into four non-overlapping 1024x576 cards.

The wing gallery and all five physical portals reuse the approved hall portal.

The ImageGen dining-room concept is composition reference only. No pixel from
that sub-2K reference enters a runtime asset.
"""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path

import numpy as np
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

PEARL_QA = ROOT / "assets_src" / "blender" / "qa_pearl_castle_kit"
ART35_QA = ROOT / "assets_src" / "blender" / "qa_art_pass35"
PROP_SOURCES = {
	"dining_table.png": (ART35_QA / "kitchen_table_set.png", "largest"),
	"dining_seat.png": (PEARL_QA / "pearl_cloud_pouf.png", "all"),
	"provisions_hutch.png": (PEARL_QA / "pearl_provisions_hutch.png", "all"),
	"canopy_bed.png": (PEARL_QA / "pearl_canopy_bed.png", "all"),
	"bedside_table.png": (PEARL_QA / "pearl_bedside_table.png", "all"),
	"shell_wardrobe.png": (PEARL_QA / "pearl_shell_wardrobe.png", "all"),
	"story_cushion.png": (PEARL_QA / "pearl_story_cushion.png", "all"),
	"dream_bed_0.png": (ART35_QA / "dream_bed_0.png", "all"),
	"dream_bed_1.png": (ART35_QA / "dream_bed_1.png", "all"),
	"dream_bed_2.png": (ART35_QA / "dream_bed_2.png", "all"),
	"cloud_settee.png": (PEARL_QA / "pearl_cloud_settee.png", "all"),
	"cloud_pouf.png": (PEARL_QA / "pearl_cloud_pouf.png", "all"),
	"shell_arch.png": (PEARL_QA / "pearl_shell_arch.png", "all"),
	"shell_window.png": (PEARL_QA / "pearl_shell_window.png", "all"),
	"shell_chandelier.png": (PEARL_QA / "pearl_shell_chandelier.png", "all"),
}

HALL_PORTAL_SOURCE = (
	ROOT / "assets" / "flats" / "castle" / "main_hall_2screen"
	/ "castle_playroom_portal_cutout_reuse.png"
)
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
		draw.rounded_rectangle((480, 458, 1568, 1032), radius=86,
			fill=(35, 27, 62, 245), outline=(244, 216, 188, 245), width=34)
		draw.rounded_rectangle((528, 506, 1520, 984), radius=54,
			fill=(18, 22, 49, 255), outline=(114, 80, 135, 230), width=18)

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
	array = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
	mask = array[:, :, 3] > 8
	height, width = mask.shape
	seen = np.zeros(mask.shape, dtype=bool)
	best: list[tuple[int, int]] = []
	for y, x in np.argwhere(mask):
		if seen[y, x]:
			continue
		seen[y, x] = True
		queue: deque[tuple[int, int]] = deque([(int(y), int(x))])
		component: list[tuple[int, int]] = []
		while queue:
			cy, cx = queue.popleft()
			component.append((cy, cx))
			for ny, nx in ((cy - 1, cx), (cy + 1, cx),
					(cy, cx - 1), (cy, cx + 1)):
				if 0 <= ny < height and 0 <= nx < width \
						and mask[ny, nx] and not seen[ny, nx]:
					seen[ny, nx] = True
					queue.append((ny, nx))
		if len(component) > len(best):
			best = component
	keep = np.zeros(mask.shape, dtype=bool)
	for y, x in best:
		keep[y, x] = True
	array[:, :, 3] = np.where(keep, array[:, :, 3], 0)
	return Image.fromarray(array, mode="RGBA")


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


def build_prop_assets() -> list[dict[str, object]]:
	records: list[dict[str, object]] = []
	for output_name, (source_path, mode) in PROP_SOURCES.items():
		image = Image.open(source_path).convert("RGBA")
		if mode == "largest":
			image = largest_alpha_component(image)
		image = crop_alpha(image)
		output_path = DREAM_ROOT / output_name
		image.save(output_path, format="PNG", optimize=True)
		records.append({
			"path": output_path.relative_to(ROOT).as_posix(),
			"dimensions": list(image.size),
			"sha256": sha256(output_path),
			"source": source_path.relative_to(ROOT).as_posix(),
			"source_sha256": sha256(source_path),
			"transform": "transparent-border crop; largest alpha component only"
				if mode == "largest" else "transparent-border crop only",
		})
	return records


def _draw_portal_crest(draw: ImageDraw.ImageDraw, kind: str,
		accent: tuple[int, int, int, int]) -> None:
	# The approved stuffie plaque is covered, not edited in place. Bold
	# pictograms keep every doorway readable without words.
	draw.ellipse((52, -8, 198, 88), fill=(248, 221, 191, 255),
		outline=(78, 51, 101, 255), width=6)
	draw.ellipse((70, 5, 180, 78), fill=accent,
		outline=(255, 239, 210, 255), width=5)
	ink = (76, 48, 100, 255)
	cream = (255, 240, 207, 255)
	if kind == "house":
		draw.polygon(((91, 42), (125, 16), (159, 42)),
			fill=(244, 144, 159, 255), outline=ink)
		draw.rounded_rectangle((99, 39, 151, 69), radius=5,
			fill=cream, outline=ink, width=4)
		draw.rounded_rectangle((119, 50, 132, 69), radius=3,
			fill=(117, 199, 198, 255), outline=ink, width=3)
	elif kind == "dining":
		draw.ellipse((91, 17, 159, 70), fill=cream, outline=ink, width=4)
		for center_x, center_y, color in (
				(111, 40, (242, 137, 91, 255)),
				(129, 34, (112, 193, 139, 255)),
				(138, 50, (242, 190, 112, 255))):
			draw.ellipse((center_x - 6, center_y - 6,
				center_x + 6, center_y + 6), fill=color, outline=ink, width=2)
		draw.line((82, 22, 82, 67), fill=ink, width=4)
		draw.line((168, 22, 168, 67), fill=ink, width=4)
	elif kind == "moon":
		draw.ellipse((94, 14, 158, 72), fill=(255, 225, 133, 255),
			outline=ink, width=4)
		draw.ellipse((117, 9, 165, 60), fill=accent)
	elif kind == "sleepover":
		for center_x in (103, 125, 147):
			draw.regular_polygon((center_x, 42, 12), n_sides=5,
				rotation=-18, fill=(255, 226, 137, 255), outline=ink)
		draw.rounded_rectangle((91, 56, 159, 69), radius=6,
			fill=cream, outline=ink, width=3)
	elif kind == "movie":
		draw.rounded_rectangle((87, 17, 163, 70), radius=9,
			fill=(37, 31, 70, 255), outline=cream, width=5)
		draw.polygon(((116, 29), (116, 58), (144, 43)),
			fill=(255, 222, 133, 255), outline=ink)


def build_family_portal_assets() -> list[dict[str, object]]:
	source = Image.open(HALL_PORTAL_SOURCE).convert("RGBA")
	styles = {
		"family_wing_portal.png": ("house", (188, 226, 218, 255)),
		"family_portal_dining.png": ("dining", (244, 185, 191, 255)),
		"family_portal_royal_bedroom.png": ("moon", (177, 214, 232, 255)),
		"family_portal_sleepover_bedroom.png": (
			"sleepover", (213, 185, 230, 255)),
		"family_portal_movie_lounge.png": ("movie", (187, 170, 221, 255)),
	}
	records: list[dict[str, object]] = []
	variants: dict[str, Image.Image] = {}
	for output_name, (kind, accent) in styles.items():
		image = source.copy()
		_draw_portal_crest(ImageDraw.Draw(image, "RGBA"), kind, accent)
		output_path = DREAM_ROOT / output_name
		image.save(output_path, format="PNG", optimize=True)
		variants[output_name] = image
		records.append({
			"path": output_path.relative_to(ROOT).as_posix(),
			"dimensions": list(image.size),
			"sha256": sha256(output_path),
			"source": HALL_PORTAL_SOURCE.relative_to(ROOT).as_posix(),
			"source_sha256": sha256(HALL_PORTAL_SOURCE),
			"transform": (
				"approved full portal reused unchanged below a new "
				"project-authored picture crest"),
		})

	# A full architectural insert cleanly replaces the unused first wall bay
	# without changing the approved hall master beneath it.
	insert = Image.new("RGBA", (370, 540), (0, 0, 0, 0))
	wall = tint(tile_image(WALL_TEXTURE, insert.size, 256), (213, 184, 222), 0.38)
	mask = Image.new("L", insert.size, 0)
	ImageDraw.Draw(mask).rounded_rectangle((5, 5, 364, 535), radius=42, fill=255)
	insert.paste(wall.convert("RGBA"), (0, 0), mask)
	draw = ImageDraw.Draw(insert, "RGBA")
	draw.rounded_rectangle((5, 5, 364, 535), radius=42,
		outline=(244, 218, 194, 250), width=12)
	draw.rounded_rectangle((18, 34, 352, 94), radius=26,
		fill=(242, 214, 191, 238), outline=(88, 57, 108, 240), width=8)
	for center_x in (31, 339):
		draw.rounded_rectangle((center_x - 20, 78, center_x + 20, 526),
			radius=18, fill=(226, 198, 222, 245),
			outline=(91, 58, 111, 245), width=7)
	insert.alpha_composite(variants["family_wing_portal.png"], (60, 118))
	insert_path = DREAM_ROOT / "family_wing_hall_insert.png"
	insert.save(insert_path, format="PNG", optimize=True)
	records.append({
		"path": insert_path.relative_to(ROOT).as_posix(),
		"dimensions": list(insert.size),
		"sha256": sha256(insert_path),
		"source": HALL_PORTAL_SOURCE.relative_to(ROOT).as_posix(),
		"source_sha256": sha256(HALL_PORTAL_SOURCE),
		"transform": (
			"approved portal plus project-authored wall-texture surround; "
			"non-destructive Main Hall depth-card insert"),
	})
	return records


def build_meal_plate() -> Path:
	scale = 3
	image = Image.new("RGBA", (176 * scale, 112 * scale), (0, 0, 0, 0))
	draw = ImageDraw.Draw(image, "RGBA")
	draw.ellipse((8 * scale, 22 * scale, 168 * scale, 102 * scale),
		fill=(247, 227, 224, 255), outline=(82, 57, 104, 255), width=5 * scale)
	draw.ellipse((22 * scale, 31 * scale, 154 * scale, 88 * scale),
		fill=(255, 248, 238, 255), outline=(222, 151, 184, 255), width=6 * scale)
	# A complete pretend meal must read even after the plate is scaled onto the
	# table: star sandwich, peas, and carrot coins use the approved toy palette.
	draw.regular_polygon((82 * scale, 58 * scale, 24 * scale),
		n_sides=5, rotation=-18, fill=(242, 190, 112, 255),
		outline=(91, 59, 104, 255))
	for center_x, center_y in ((118, 50), (132, 57), (118, 66)):
		draw.ellipse(((center_x - 7) * scale, (center_y - 7) * scale,
			(center_x + 7) * scale, (center_y + 7) * scale),
			fill=(112, 193, 139, 255), outline=(65, 92, 91, 255),
			width=2 * scale)
	for center_x, center_y in ((43, 53), (48, 69)):
		draw.ellipse(((center_x - 9) * scale, (center_y - 6) * scale,
			(center_x + 9) * scale, (center_y + 6) * scale),
			fill=(242, 137, 91, 255), outline=(111, 69, 100, 255),
			width=2 * scale)
	image = image.resize((176, 112), Image.Resampling.LANCZOS)
	path = DREAM_ROOT / "meal_plate.png"
	image.save(path, format="PNG", optimize=True)
	return path


def build_movie_frame() -> Path:
	scale = 2
	image = Image.new("RGBA", (720 * scale, 400 * scale), (0, 0, 0, 0))
	draw = ImageDraw.Draw(image, "RGBA")
	draw.rounded_rectangle((8 * scale, 8 * scale, 712 * scale, 392 * scale),
		radius=70 * scale, outline=(76, 48, 101, 255), width=30 * scale)
	draw.rounded_rectangle((30 * scale, 30 * scale, 690 * scale, 370 * scale),
		radius=52 * scale, outline=(245, 214, 176, 255), width=22 * scale)
	draw.ellipse((318 * scale, 0, 402 * scale, 70 * scale),
		fill=(250, 225, 194, 255), outline=(76, 48, 101, 255), width=8 * scale)
	draw.pieslice((336 * scale, 12 * scale, 384 * scale, 58 * scale),
		0, 180, fill=(197, 150, 190, 255))
	image = image.resize((720, 400), Image.Resampling.LANCZOS)
	path = DREAM_ROOT / "movie_screen_frame.png"
	image.save(path, format="PNG", optimize=True)
	return path


def exact_equal(left: Image.Image, right: Image.Image) -> bool:
	return ImageChops.difference(left, right).getbbox() is None


def build() -> None:
	for directory in (DREAM_ROOT, MASTER_ROOT, TILE_ROOT, AUDIT_ROOT):
		directory.mkdir(parents=True, exist_ok=True)

	records: list[dict[str, object]] = []
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

	prop_records = build_prop_assets()
	prop_records.extend(build_family_portal_assets())
	for path in (build_meal_plate(), build_movie_frame()):
		with Image.open(path) as image:
			prop_records.append({
				"path": path.relative_to(ROOT).as_posix(),
				"dimensions": list(image.size),
				"sha256": sha256(path),
				"source": "project-authored deterministic Pillow drawing",
				"transform": "new shared component in approved pearl material language",
			})

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
		portal = Image.open(DREAM_ROOT / portal_name).convert("RGBA").resize(
			(160, 264), Image.Resampling.LANCZOS)
		gallery_stage.alpha_composite(portal, (70 + index * 235, 189))
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
		"schema": "castle_dream_house_room_art_v2",
		"method": "deterministic composition from approved project textures, prop QA renders, and the approved hall portal",
		"imagegen_reference": {
			"path": IMAGEGEN_REFERENCE.relative_to(ROOT).as_posix(),
			"exists": IMAGEGEN_REFERENCE.exists(),
			"sha256": sha256(IMAGEGEN_REFERENCE) if IMAGEGEN_REFERENCE.exists() else "",
			"role": "composition_reference_only",
			"used_as_runtime_pixels": False,
		},
		"background_sources": [
			{"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
			for path in [WALL_TEXTURE, *FLOOR_TEXTURES.values()]
		],
		"rooms": records,
		"props": prop_records,
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
			"gallery_room": "family_gallery",
			"destinations": {
				"dining_room": "family_portal_dining.png",
				"royal_bedroom": "family_portal_royal_bedroom.png",
				"sleepover_bedroom": "family_portal_sleepover_bedroom.png",
				"movie_lounge": "family_portal_movie_lounge.png",
			},
			"floating_route_buttons": False,
		},
		"protected_originals_modified": False,
		"runtime_world_art": "unshaded Sprite3D cards only",
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
