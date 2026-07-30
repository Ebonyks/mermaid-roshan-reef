"""Build clean Pearl Castle plates and non-overlapping Sprite3D art cards.

The complete room images are immutable source composites. This tool reuses
their pixels in two ways:

* exact-pixel alpha cards for every authored object/depth region;
* a clean architecture plate whose card-owned pixels are filled exclusively
  from surrounding pixels in the same source image.

No image generation or outside artwork is involved. Card masks receive unique
pixel ownership, so an object cannot be baked into the runtime background and
also appear on one or more Sprite3D cards.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps
from scipy.ndimage import (
	binary_fill_holes,
	distance_transform_edt,
	label,
)
from skimage.filters import sobel
from skimage.segmentation import watershed


ROOT = Path(__file__).resolve().parents[1]
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
AUDIT_PATH = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
KITCHEN_GENERATED_SOURCE = (
	ROOT / "assets_src" / "castle" / "room_regenerations"
	/ "room_kitchen_fullframe_v3_1672x941.png")
CANVAS = (1024, 576)


def _poly(*points: tuple[int, int]) -> tuple[str, tuple[tuple[int, int], ...]]:
	return ("polygon", points)


def _ellipse(box: tuple[int, int, int, int]) -> tuple[str, tuple[int, int, int, int]]:
	return ("ellipse", box)

def _rounded_rect(box: tuple[int, int, int, int], radius: int) -> tuple:
	return ("rounded_rectangle", (box, radius))


# Each piece is (output suffix, crop box, mask shapes in 1024x576 coordinates).
# The hand-authored silhouettes intentionally stay a few pixels inside objects:
# hiding too little of Roshan reads better than hiding her behind empty floor.
PIECES: dict[str, list[tuple[str, tuple[int, int, int, int], tuple]]] = {
	"main_hall": [
		("front_left", (0, 0, 274, 558), (
			_poly((0, 0), (160, 0), (160, 365), (181, 400), (170, 492), (67, 492), (67, 455), (0, 455)),
			_poly((122, 390), (213, 378), (262, 423), (251, 504), (199, 541), (142, 520), (128, 478)),
		)),
		("front_right", (750, 0, 1024, 558), (
			_poly((864, 0), (1024, 0), (1024, 455), (957, 455), (957, 492), (854, 492), (843, 400), (864, 365)),
			_poly((902, 390), (811, 378), (762, 423), (773, 504), (825, 541), (882, 520), (896, 478)),
		)),
	],
	"opera_hall": [
		("front_left", (0, 252, 274, 576), (
			_poly((0, 252), (72, 263), (142, 298), (196, 358), (238, 433), (274, 576), (0, 576)),
		)),
		("front_right", (750, 252, 1024, 576), (
			_poly((1024, 252), (952, 263), (882, 298), (828, 358), (786, 433), (750, 576), (1024, 576)),
		)),
	],
	"kitchen": [
		("front_left", (0, 354, 286, 576), (
			_poly((0, 410), (45, 392), (80, 397), (111, 367), (173, 354), (222, 387), (245, 438), (286, 476), (286, 576), (0, 576)),
		)),
		("front_right", (650, 324, 1024, 576), (
			_poly(
				(694, 364), (731, 335), (826, 324), (916, 340),
				(955, 376), (982, 413), (1024, 430), (1024, 464),
				(966, 466), (923, 451), (865, 467), (798, 469),
				(742, 451), (690, 458), (650, 442), (650, 405)),
			_ellipse((687, 421, 758, 526)),
			_ellipse((784, 429, 858, 548)),
			_ellipse((899, 418, 975, 528)),
			_poly(
				(989, 456), (1024, 443), (1024, 576), (982, 576),
				(976, 519)),
		)),
	],
	"library": [
		("front_left", (0, 273, 300, 576), (
			_poly((0, 359), (37, 335), (58, 303), (99, 280), (168, 273), (224, 304), (259, 357), (279, 435), (300, 576), (0, 576)),
		)),
		("front_right", (724, 273, 1024, 576), (
			_poly((1024, 359), (987, 335), (966, 303), (925, 280), (856, 273), (800, 304), (765, 357), (745, 435), (724, 576), (1024, 576)),
		)),
	],
	"playroom": [
		("front_left", (0, 319, 247, 576), (
			_poly((0, 381), (42, 342), (102, 323), (167, 319), (214, 347), (240, 397), (247, 576), (0, 576)),
		)),
		("front_right", (777, 319, 1024, 576), (
			_poly((1024, 381), (982, 342), (922, 323), (857, 319), (810, 347), (784, 397), (777, 576), (1024, 576)),
		)),
	],
	"craft_room": [
		("front_left", (0, 316, 304, 576), (
			_poly((0, 385), (38, 351), (100, 324), (191, 316), (263, 343), (292, 402), (304, 576), (0, 576)),
		)),
		("front_right", (720, 316, 1024, 576), (
			_poly((1024, 385), (986, 351), (924, 324), (833, 316), (761, 343), (732, 402), (720, 576), (1024, 576)),
		)),
	],
	"mermaid_pool": [
		("mid_pool", (0, 212, 1024, 382), (
			_poly((0, 220), (1024, 220), (1024, 330), (948, 348), (837, 364), (705, 376), (319, 376), (187, 364), (76, 348), (0, 330)),
		)),
		("front_left", (0, 378, 205, 576), (
			_poly((0, 424), (38, 389), (82, 378), (128, 407), (158, 451), (196, 481), (205, 576), (0, 576)),
		)),
		("front_right", (819, 378, 1024, 576), (
			_poly((1024, 424), (986, 389), (942, 378), (896, 407), (866, 451), (828, 481), (819, 576), (1024, 576)),
		)),
	],
	"bubble_bath": [
		("front_left", (0, 358, 226, 576), (
			_poly((0, 401), (40, 372), (88, 358), (151, 371), (195, 410), (226, 576), (0, 576)),
		)),
		("front_right", (798, 358, 1024, 576), (
			_poly((1024, 401), (984, 372), (936, 358), (873, 371), (829, 410), (798, 576), (1024, 576)),
		)),
	],
}

# Three touchable, independently animated props per room. These masks are
# deliberately tighter than navigation occluders so a wiggle or pulse does not
# lift a rectangular patch of floor with the object.
ITEMS: dict[str, list[tuple[str, tuple[int, int, int, int], tuple]]] = {
	"main_hall": [
		("throne", (430, 150, 594, 354), (
			_poly((448, 170), (512, 148), (576, 170), (594, 244), (575, 345), (449, 345), (430, 244)),
		)),
		("fountain_left", (122, 379, 268, 546), (
			_poly((127, 410), (167, 384), (218, 384), (260, 414), (268, 477), (238, 532), (163, 546), (126, 500)),
		)),
		("fountain_right", (756, 379, 902, 546), (
			_poly((764, 414), (806, 384), (857, 384), (897, 410), (898, 500), (861, 546), (786, 532), (756, 477)),
		)),
	],
	"opera_hall": [
		("curtains", (414, 100, 610, 309), (
			_poly((466, 111), (558, 111), (610, 185), (589, 287), (435, 287), (414, 185)),
		)),
		("chandelier", (418, 0, 608, 126), (
			_ellipse((427, 5, 599, 112)),
		)),
		("stage_star", (463, 286, 559, 361), (
			_poly((512, 286), (528, 318), (559, 323), (535, 346), (540, 361), (512, 348), (484, 361), (489, 346), (463, 323), (496, 318)),
		)),
	],
	"kitchen": [
		("sink", (62, 176, 263, 300), (
			_poly((80, 229), (96, 214), (119, 204), (147, 198),
				(183, 199), (213, 207), (237, 220), (246, 239),
				(240, 258), (221, 272), (195, 281), (121, 281),
				(96, 272), (79, 255), (74, 238)),
			_poly((137, 230), (137, 197), (145, 187), (161, 182),
				(174, 187), (181, 198), (177, 205), (166, 198),
				(157, 200), (157, 230)),
		)),
		("pan_1", (300, 132, 341, 215), (
			_poly((319, 136), (325, 136), (326, 169), (320, 169)),
			_ellipse((302, 164, 340, 208)),
		)),
		("pan_2", (337, 132, 382, 215), (
			_poly((357, 136), (363, 136), (364, 169), (358, 169)),
			_ellipse((339, 164, 381, 209)),
		)),
		("pan_3", (379, 132, 424, 215), (
			_poly((399, 136), (405, 136), (406, 169), (400, 169)),
			_ellipse((381, 164, 423, 209)),
		)),
		("pan_4", (418, 132, 449, 215), (
			_poly((433, 136), (439, 136), (440, 169), (434, 169)),
			_ellipse((420, 164, 449, 208)),
		)),
		("oven", (289, 244, 491, 356), (
			_poly((296, 270), (484, 270), (491, 279), (491, 331),
				(476, 351), (452, 356), (321, 356), (296, 346),
				(289, 326)),
		)),
		("fridge", (631, 84, 771, 347), (
			_rounded_rect((633, 85, 769, 345), 28),
		)),
	],
	"library": [
		("magic_book", (445, 145, 582, 314), (
			_poly((486, 159), (547, 178), (573, 246), (535, 303), (470, 282), (445, 214)),
		)),
		("pearl_table", (392, 315, 634, 437), (
			_ellipse((402, 318, 624, 382)),
			_poly((463, 349), (565, 349), (578, 420), (548, 437), (471, 437), (448, 420)),
		)),
		("pearl_lamp", (0, 225, 124, 371), (
			_poly((7, 260), (53, 226), (98, 247), (120, 305), (108, 356), (51, 371), (6, 341)),
		)),
	],
	"playroom": [
		("stuffie_nook", (380, 140, 646, 330), (
			_poly((398, 193), (452, 151), (570, 143), (628, 192), (646, 284), (608, 327), (413, 327), (380, 280)),
		)),
		("stacking_toy", (218, 284, 350, 441), (
			_poly((254, 294), (306, 294), (332, 337), (342, 401), (315, 438), (250, 438), (224, 401), (235, 337)),
		)),
		("blocks", (626, 320, 751, 420), (
			_poly((636, 339), (706, 320), (744, 352), (751, 405), (626, 420)),
		)),
	],
	"craft_room": [
		("idea_board", (377, 103, 647, 274), (
			_poly((398, 131), (512, 105), (626, 131), (647, 246), (617, 270), (405, 270), (377, 246)),
		)),
		("paint_table", (400, 272, 624, 367), (
			_poly((409, 289), (615, 289), (624, 337), (601, 367), (423, 367), (400, 337)),
		)),
		("palette", (0, 320, 304, 576), (
			_poly((0, 382), (48, 346), (104, 326), (180, 320), (246, 345), (284, 402), (304, 576), (0, 576)),
		)),
	],
	"mermaid_pool": [
		("waterfall", (285, 45, 466, 278), (
			_poly((333, 62), (420, 62), (459, 129), (450, 235), (408, 275), (327, 266), (291, 221), (285, 121)),
		)),
		("flower_float", (371, 218, 512, 329), (
			_ellipse((379, 229, 503, 323)),
		)),
		("bubble_fountain", (553, 183, 711, 325), (
			_poly((575, 270), (603, 226), (655, 203), (692, 231), (711, 288), (675, 320), (606, 325)),
		)),
	],
	"bubble_bath": [
		("bathtub", (76, 157, 397, 355), (
			_poly((91, 215), (139, 175), (285, 161), (365, 195), (397, 278), (358, 346), (137, 355), (77, 304)),
		)),
		("sink", (440, 137, 645, 310), (
			_poly((469, 174), (512, 140), (564, 146), (613, 185), (641, 247), (625, 299), (461, 310), (440, 255)),
		)),
		("toilet", (753, 154, 906, 346), (
			_poly((802, 158), (868, 169), (902, 230), (900, 319), (868, 345), (777, 340), (753, 291), (768, 216)),
		)),
	],
}


def _normalized_backdrop(room_id: str) -> Image.Image:
	path = ROOM_DIR / f"room_{room_id}.png"
	source_path = KITCHEN_GENERATED_SOURCE if room_id == "kitchen" else path
	image = Image.open(source_path).convert("RGB")
	if image.size != CANVAS:
		image = image.resize(CANVAS, Image.Resampling.LANCZOS)
		image.save(path, optimize=True)
	return image


def _shape_mask(shapes: tuple) -> Image.Image:
	mask = Image.new("L", CANVAS, 0)
	draw = ImageDraw.Draw(mask)
	for shape_type, geometry in shapes:
		if shape_type == "polygon":
			draw.polygon(geometry, fill=255)
		elif shape_type == "ellipse":
			draw.ellipse(geometry, fill=255)
		else:
			box, radius = geometry
			draw.rounded_rectangle(box, radius=radius, fill=255)
	return mask.filter(ImageFilter.GaussianBlur(0.65))


def _build_piece(image: Image.Image, room_id: str, suffix: str,
		crop_box: tuple[int, int, int, int], mask: Image.Image) -> None:
	rgba = image.convert("RGBA")
	rgba.putalpha(mask)
	crop = rgba.crop(crop_box)
	crop.save(ROOM_DIR / f"room_{room_id}_{suffix}.png", optimize=True)


def _refine_mask_to_painted_outline(image: Image.Image,
		provisional_background: Image.Image, raw_mask: Image.Image,
		crop_box: tuple[int, int, int, int]) -> Image.Image:
	"""Contract a routing mask to the painted object's actual outer edge.

	The authored polygons identify which object owns a region, but they are not
	valid alpha mattes: opaque wall and floor pixels inside those polygons write
	depth and can hide Roshan. The provisional clean plate supplies a same-scene
	background estimate. Strong source/plate differences seed the object, close
	matches seed transparency, and an RGB-edge watershed settles the uncertain
	band on the illustration's inked outline.
	"""
	left, top, right, bottom = crop_box
	raw_crop = np.asarray(
		raw_mask.crop(crop_box), dtype=np.float32) / 255.0
	raw_core = raw_crop >= 0.20
	if not np.any(raw_core):
		return Image.new("L", CANVAS, 0)

	source = np.asarray(
		image.crop(crop_box), dtype=np.float32) / 255.0
	clean = np.asarray(
		provisional_background.crop(crop_box), dtype=np.float32) / 255.0
	difference = np.max(np.abs(source - clean), axis=2) * 255.0
	edge = np.max(np.stack(
		[sobel(source[:, :, channel]) for channel in range(3)]), axis=0)

	markers = np.zeros(raw_core.shape, dtype=np.uint8)
	markers[~raw_core] = 1
	markers[raw_core & (difference <= 9.0)] = 1
	strong_foreground = raw_core & (difference >= 48.0)
	markers[strong_foreground] = 2
	if not np.any(strong_foreground):
		return raw_mask

	segmented = watershed(edge, markers) == 2
	refined = segmented & raw_core
	components, component_count = label(refined)
	minimum_component = max(8, int(np.count_nonzero(raw_core) * 0.008))
	kept = np.zeros(refined.shape, dtype=bool)
	for component_id in range(1, component_count + 1):
		component = components == component_id
		if np.count_nonzero(component) >= minimum_component \
				and np.any(component & strong_foreground):
			kept |= component
	refined = binary_fill_holes(kept) & raw_core

	# A sub-pixel matte keeps the authored antialiasing, while the 50% alpha
	# threshold remains a true silhouette for mobile depth testing.
	local_alpha = Image.fromarray(
		refined.astype(np.uint8) * 255, mode="L").filter(
			ImageFilter.GaussianBlur(0.55))
	local_alpha = ImageChops.multiply(
		local_alpha, raw_mask.crop(crop_box))
	full_alpha = Image.new("L", CANVAS, 0)
	full_alpha.paste(local_alpha, (left, top))
	return full_alpha


def _clean_plate(image: Image.Image, owned_mask: Image.Image) -> Image.Image:
	"""Fill owned pixels from unowned scanlines in the same source image."""
	# Cards keep their antialiased edge pixels. Only the fully opaque ownership
	# core is removed from the architecture plate; expanding this mask leaked
	# broad scanline-fill halos beyond the card silhouettes at runtime.
	mask_array = np.asarray(owned_mask, dtype=np.uint8) >= 250
	source = np.asarray(image, dtype=np.float32)
	height, width = mask_array.shape

	# Nearest-neighbour fill is the fallback for a row/column wholly covered by
	# an object. The primary fill interpolates unowned pixels on each horizontal
	# and vertical scanline; this continues the room's existing wall/floor color
	# fields without inventing a new motif or retaining a blurred object ghost.
	indices = distance_transform_edt(
		mask_array, return_distances=False, return_indices=True)
	nearest = source[indices[0], indices[1]]
	horizontal = nearest.copy()
	vertical = nearest.copy()
	horizontal_valid = np.zeros(mask_array.shape, dtype=bool)
	vertical_valid = np.zeros(mask_array.shape, dtype=bool)
	x_positions = np.arange(width)
	y_positions = np.arange(height)
	for y_pos in range(height):
		known_x = np.flatnonzero(~mask_array[y_pos])
		if known_x.size == 0:
			continue
		horizontal_valid[y_pos, :] = True
		for channel in range(3):
			horizontal[y_pos, :, channel] = np.interp(
				x_positions, known_x, source[y_pos, known_x, channel])
	for x_pos in range(width):
		known_y = np.flatnonzero(~mask_array[:, x_pos])
		if known_y.size == 0:
			continue
		vertical_valid[:, x_pos] = True
		for channel in range(3):
			vertical[:, x_pos, channel] = np.interp(
				y_positions, known_y, source[known_y, x_pos, channel])

	filled = source.copy()
	both = mask_array & horizontal_valid & vertical_valid
	horizontal_only = mask_array & horizontal_valid & ~vertical_valid
	vertical_only = mask_array & vertical_valid & ~horizontal_valid
	neither = mask_array & ~horizontal_valid & ~vertical_valid
	filled[both] = horizontal[both] * 0.72 + vertical[both] * 0.28
	filled[horizontal_only] = horizontal[horizontal_only]
	filled[vertical_only] = vertical[vertical_only]
	filled[neither] = nearest[neither]
	filled = np.clip(filled, 0, 255).astype(np.uint8)
	smoothed = np.asarray(
		Image.fromarray(filled, "RGB").filter(ImageFilter.GaussianBlur(2.5)),
		dtype=np.uint8)
	filled[mask_array] = smoothed[mask_array]
	return Image.fromarray(filled, "RGB")


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _build_actor_shadow() -> None:
	"""Create a small transparent contact-shadow card for Sprite3D actors."""
	shadow = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
	mask = Image.new("L", shadow.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((10, 11, 246, 55), fill=145)
	mask = mask.filter(ImageFilter.GaussianBlur(6.0))
	shadow.putalpha(mask)
	shadow.save(ROOM_DIR / "room_actor_shadow.png", optimize=True)


def main() -> None:
	manifest: dict[str, object] = {
		"schema": 1,
		"owner_native_environment_contract": {
			"required_minimum_long_edge": 2048,
			"required_reference_aspect_ratio": [16, 9],
			"ratio_rounding_tolerance_pixels": 1.0,
			"master_power_of_two_required": False,
			"runtime_tile_max_long_edge": 1024,
			"runtime_tiles_lossless_no_scale": True,
			"low_resolution_reference_dimensions": [1024, 576],
			"status": "legacy_resolution_nonconforming",
			"handoff": "FABLE_CASTLE_2K_REGEN_HANDOFF_2026-07-26.md",
		},
		"runtime_node_contract": {
			"world_root": "Node3D",
			"camera": "Camera3D:perspective",
			"world_art_allowed": ["Sprite3D:unshaded"],
			"world_art_forbidden": [
				"Sprite2D",
				"AnimatedSprite2D",
				"TextureRect",
				"Polygon2D",
				"CanvasItem custom drawing",
				"MeshInstance3D",
				"MultiMeshInstance3D",
				"CSGShape3D",
				"Decal",
			],
			"ui_only_allowed": [
				"CanvasLayer",
				"Control",
				"Button",
				"Panel",
				"Label",
			],
			"reference_steady_sprite3d_inventory": {
				"background": 1,
				"touch_props": 3,
				"midground_max": 1,
				"foreground_max": 2,
				"player": 1,
				"contact_shadow": 1,
			},
			"native_master_runtime_note": (
				"Background and any over-1024 layer counts expand only by "
				"the minimum lossless non-overlapping tile count."),
		},
			"source_policy": (
			"Approved complete room-composite pixels only; Kitchen v3 retains "
			"the accepted full-frame project ImageGen regeneration and replaces "
			"only its defective two-spout kettle from a recorded single-object "
			"generation"),
		"clean_fill": (
			"horizontal/vertical scanline interpolation plus nearest unmasked "
			"fallback from the same room composite, applied only beneath fully "
			"opaque card ownership; antialiased source boundaries are preserved"),
		"rooms": {},
	}
	for room_id, pieces in PIECES.items():
		image = _normalized_backdrop(room_id)

		specs: list[tuple[str, str, tuple[int, int, int, int], tuple]] = []
		for item_id, crop_box, shapes in ITEMS.get(room_id, []):
			specs.append(("item", f"item_{item_id}", crop_box, shapes))
		for suffix, crop_box, shapes in pieces:
			if suffix.startswith("front_"):
				specs.append(("foreground", suffix, crop_box, shapes))
		for suffix, crop_box, shapes in pieces:
			if suffix.startswith("mid_"):
				specs.append(("midground", suffix, crop_box, shapes))

		claimed = Image.new("L", CANVAS, 0)
		union = Image.new("L", CANVAS, 0)
		raw_unique_masks: list[Image.Image] = []
		card_records: list[dict[str, object]] = []
		for role, suffix, crop_box, shapes in specs:
			raw_mask = _shape_mask(shapes)
			union = ImageChops.lighter(union, raw_mask)
			claimed_binary = claimed.point(lambda value: 255 if value > 0 else 0)
			available = ImageOps.invert(claimed_binary)
			unique_mask = ImageChops.multiply(raw_mask, available)
			claimed = ImageChops.lighter(claimed, raw_mask)
			raw_unique_masks.append(unique_mask)
			card_records.append({
				"id": suffix,
				"role": role,
				"crop": list(crop_box),
			})

		provisional_background = _clean_plate(image, union)
		unique_masks: list[Image.Image] = []
		refined_union = Image.new("L", CANVAS, 0)
		for index, card_record in enumerate(card_records):
			crop = tuple(int(value) for value in card_record["crop"])
			if str(card_record["id"]) == "item_stage_star":
				# This source is already authored as a precise concave star
				# polygon; watershed would incorrectly contract into its glow.
				refined_mask = raw_unique_masks[index]
			else:
				refined_mask = _refine_mask_to_painted_outline(
					image, provisional_background, raw_unique_masks[index], crop)
			if np.count_nonzero(
					np.asarray(refined_mask, dtype=np.uint8) >= 128) < 64:
				refined_mask = Image.new("L", CANVAS, 0)
			unique_masks.append(refined_mask)
			refined_union = ImageChops.lighter(refined_union, refined_mask)
			_build_piece(
				image, room_id, str(card_record["id"]), crop, refined_mask)
			alpha_array = np.asarray(refined_mask, dtype=np.uint8)
			card_record["alpha_pixels"] = int(np.count_nonzero(alpha_array))
			card_record["depth_opaque_pixels"] = int(np.count_nonzero(
				alpha_array >= 128))
			raw_alpha_array = np.asarray(
				raw_unique_masks[index], dtype=np.uint8)
			card_record["routing_depth_pixels"] = int(np.count_nonzero(
				raw_alpha_array >= 128))
			card_record["depth_footprint_reduction_ratio"] = round(
				1.0 - (
					int(card_record["depth_opaque_pixels"])
					/ max(1, int(card_record["routing_depth_pixels"]))),
				6)
			card_record["alpha_outline_refined"] = True

		background_path = ROOM_DIR / f"room_{room_id}_background.png"
		background = _clean_plate(image, refined_union)
		background.save(background_path, optimize=True)

		reconstruction = background.convert("RGBA")
		for card_record in card_records:
			card_path = ROOM_DIR / (
				f"room_{room_id}_{card_record['id']}.png")
			card = Image.open(card_path).convert("RGBA")
			crop = card_record["crop"]
			reconstruction.alpha_composite(
				card, (int(crop[0]), int(crop[1])))
		reconstruction_array = np.asarray(
			reconstruction.convert("RGB"), dtype=np.int16)
		occupancy = np.zeros((CANVAS[1], CANVAS[0]), dtype=np.uint8)
		for mask in unique_masks:
			occupancy += (
				np.asarray(mask, dtype=np.uint8) > 0).astype(np.uint8)
		source_array = np.asarray(image, dtype=np.uint8)
		background_array = np.asarray(background, dtype=np.uint8)
		owned = np.asarray(refined_union, dtype=np.uint8) > 0
		changed = np.any(source_array != background_array, axis=2)
		owned_count = int(np.count_nonzero(owned))
		changed_count = int(np.count_nonzero(changed & owned))
		source_path = ROOM_DIR / f"room_{room_id}.png"
		source_aspect: float = image.width / image.height
		reference_aspect: float = CANVAS[0] / CANVAS[1]
		ratio_pixel_delta: float = min(
			abs(image.height - image.width / reference_aspect),
			abs(image.width - image.height * reference_aspect))
		native_master_compliant: bool = (
			max(image.size) >= 2048
			and ratio_pixel_delta <= 1.0)
		room_record: dict[str, object] = {
			"source": source_path.name,
			"background": background_path.name,
			"source_dimensions": list(image.size),
			"background_dimensions": list(background.size),
			"source_aspect_ratio": round(source_aspect, 9),
			"reference_aspect_ratio": round(reference_aspect, 9),
			"aspect_ratio_delta": round(
				abs(source_aspect - reference_aspect), 12),
			"aspect_ratio_pixel_delta": round(ratio_pixel_delta, 6),
			"native_master_compliant": native_master_compliant,
			"runtime_tiles": [],
			"source_sha256": _sha256(source_path),
			"background_sha256": _sha256(background_path),
			"cards": card_records,
			"card_count": len(card_records),
			"card_overlap_pixels": int(np.count_nonzero(occupancy > 1)),
			"owned_background_pixels": owned_count,
			"changed_owned_pixels": changed_count,
			"changed_owned_ratio": (
				round(changed_count / owned_count, 6)
				if owned_count > 0 else 0.0),
			"resting_reconstruction_mean_abs_error": round(float(np.abs(
				reconstruction_array - source_array.astype(np.int16)).mean()), 6),
		}
		if room_id == "kitchen":
			with Image.open(KITCHEN_GENERATED_SOURCE) as generated:
				room_record.update({
					"generation_master": KITCHEN_GENERATED_SOURCE.relative_to(
						ROOT).as_posix(),
					"generation_master_dimensions": list(generated.size),
					"generation_master_sha256": _sha256(
						KITCHEN_GENERATED_SOURCE),
					"generation_method": (
						"OpenAI built-in ImageGen complete full-frame "
						"regeneration plus recorded single-kettle topology "
						"repair"),
					"generation_prompt_record": (
						"assets_src/castle/room_regenerations/"
						"room_kitchen_fullframe_v3_provenance.md"),
				})
		manifest["rooms"][room_id] = room_record
	_build_actor_shadow()
	AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
	AUDIT_PATH.write_text(
		json.dumps(manifest, indent=2, sort_keys=True) + "\n",
		encoding="utf-8")


if __name__ == "__main__":
	main()
