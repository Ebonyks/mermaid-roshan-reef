"""Build clean Pearl Castle plates and non-overlapping Sprite2D art cards.

The complete room images are immutable source composites. This tool reuses
their pixels in two ways:

* exact-pixel alpha cards for every authored object/layer region;
* a clean architecture plate whose card-owned pixels are filled exclusively
  from surrounding pixels in the same source image.

No image generation or outside artwork is involved. Card masks receive unique
pixel ownership, so an object cannot be baked into the runtime background and
also appear on one or more Sprite2D cards.
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
MERMAID_POOL_GENERATED_SOURCE = (
	ROOT / "assets_src" / "imagegen" / "mermaid_pool_room_2026-08-02"
	/ "room_mermaid_pool_fullframe_v3_native.png")
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
		("mid_pool", (0, 218, 1024, 530), (
			_poly(
				(285, 218), (850, 218), (925, 245), (982, 275),
				(1024, 310), (1024, 385), (992, 420), (950, 448),
				(880, 470), (790, 490), (680, 505), (580, 515),
				(460, 515), (340, 505), (230, 488), (140, 465),
				(72, 438), (25, 408), (0, 380), (0, 305),
				(40, 280), (105, 255), (190, 235)),
		)),
		("front_left", (0, 430, 160, 576), (
			_poly(
				(0, 452), (20, 440), (55, 445), (80, 460),
				(95, 482), (116, 494), (129, 530), (155, 565),
				(160, 576), (0, 576)),
		)),
		("front_right", (885, 435, 1024, 576), (
			_poly(
				(1024, 455), (990, 445), (960, 455), (945, 485),
				(930, 505), (925, 530), (900, 560), (890, 576),
				(1024, 576)),
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

# Four or more touchable props per destination room. These masks are tighter
# than navigation occluders so their atlas cards never carry a rectangular
# patch of wall, water, counter, or floor over Roshan.
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
			_poly((468, 111), (556, 111), (602, 180), (584, 286),
				(440, 286), (422, 180)),
		)),
		("chandelier", (418, 0, 608, 126), (
			_ellipse((434, 5, 590, 88)),
			_poly((448, 58), (576, 58), (584, 80), (565, 94),
				(459, 94), (440, 80)),
			_ellipse((450, 80, 466, 108)),
			_ellipse((478, 82, 494, 112)),
			_ellipse((506, 82, 522, 114)),
			_ellipse((534, 82, 550, 112)),
			_ellipse((562, 80, 578, 108)),
		)),
		("footlights", (414, 286, 610, 330), (
			_poly((418, 287), (606, 287), (606, 310), (418, 310)),
			_ellipse((426, 286, 439, 299)),
			_ellipse((459, 286, 472, 299)),
			_ellipse((493, 286, 506, 299)),
			_ellipse((527, 286, 540, 299)),
			_ellipse((560, 286, 573, 299)),
			_ellipse((585, 286, 598, 299)),
		)),
		("stage_star", (490, 309, 534, 354), (
			_ellipse((492, 311, 532, 352)),
		)),
	],
	"kitchen": [
		("sink", (62, 176, 263, 300), (
			_poly((80, 229), (96, 214), (119, 204), (147, 198),
				(183, 199), (213, 207), (237, 220), (244, 239),
				(238, 256), (218, 269), (194, 278), (122, 278),
				(98, 269), (80, 253), (75, 238)),
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
			_poly((297, 270), (483, 270), (488, 280), (488, 329),
				(474, 349), (452, 353), (322, 353), (298, 344),
				(289, 326)),
		)),
		("fridge", (631, 84, 771, 347), (
			_rounded_rect((634, 86, 768, 341), 27),
		)),
	],
	"library": [
		("book_stack", (0, 365, 165, 576), (
			_poly((2, 389), (89, 372), (131, 400), (119, 430),
				(150, 452), (138, 482), (161, 505), (151, 548),
				(104, 572), (19, 566), (2, 531)),
		)),
		("magic_book", (445, 145, 582, 314), (
			_poly((484, 214), (522, 204), (555, 220), (565, 264),
				(541, 293), (493, 283), (474, 249)),
			_ellipse((461, 274, 566, 309)),
		)),
		("pearl_table", (392, 315, 634, 437), (
			_ellipse((410, 318, 614, 374)),
			_poly((463, 350), (561, 350), (573, 410), (548, 433),
				(476, 433), (451, 410)),
		)),
		("pearl_lamp", (4, 225, 92, 305), (
			_poly((8, 260), (12, 245), (25, 233), (42, 227),
				(60, 231), (75, 243), (83, 259), (81, 278),
				(70, 292), (57, 301), (26, 301), (12, 291),
				(6, 275)),
			_ellipse((30, 247, 67, 286)),
		)),
	],
	"playroom": [
		("play_tent", (105, 235, 270, 366), (
			_poly((116, 347), (132, 292), (174, 244), (207, 242),
				(251, 291), (262, 348), (232, 362), (137, 362)),
		)),
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
		("ribbon_rack", (270, 82, 396, 203), (
			_ellipse((275, 90, 291, 113)),
			_poly((284, 96), (383, 96), (383, 103), (284, 103)),
			_ellipse((376, 90, 393, 113)),
			_rounded_rect((289, 99, 300, 176), 2),
			_rounded_rect((301, 100, 312, 184), 2),
			_rounded_rect((313, 99, 324, 190), 2),
			_rounded_rect((325, 100, 336, 162), 2),
			_rounded_rect((337, 99, 348, 193), 2),
			_rounded_rect((349, 99, 360, 181), 2),
			_rounded_rect((361, 99, 372, 189), 2),
		)),
		("idea_board", (377, 103, 647, 274), (
			_poly((399, 131), (512, 107), (625, 131), (643, 242),
				(616, 266), (408, 266), (381, 242)),
		)),
		("paint_table", (400, 272, 624, 367), (
			_poly((410, 289), (614, 289), (621, 335), (599, 364),
				(425, 364), (403, 335)),
		)),
		("palette", (0, 320, 304, 576), (
			_poly((8, 360), (34, 337), (78, 322), (116, 324),
				(139, 348), (136, 386), (104, 404), (48, 402),
				(15, 384)),
			_rounded_rect((74, 323, 182, 384), 18),
		)),
	],
	"mermaid_pool": [
		("star_float", (530, 290, 620, 360), (
			_poly((576, 299), (587, 314), (609, 318), (596, 330),
				(600, 346), (577, 339), (557, 347), (560, 331),
				(540, 322), (565, 314)),
		)),
		("waterfall", (300, 80, 455, 265), (
			_poly((328, 88), (405, 88), (429, 116), (428, 218),
				(418, 241), (403, 255), (340, 255), (320, 242),
				(309, 220), (310, 115)),
		)),
		("flower_float", (310, 300, 415, 385), (
			_ellipse((315, 319, 408, 375)),
			_ellipse((329, 307, 394, 368)),
		)),
		("seahorse_fountain", (635, 90, 830, 305), (
			_ellipse((705, 239, 820, 292)),
			_ellipse((722, 97, 802, 166)),
			_poly((692, 126), (749, 119), (771, 141), (758, 165),
				(720, 169), (690, 154)),
			_poly((748, 143), (794, 164), (803, 207), (790, 242),
				(812, 264), (805, 287), (762, 288), (733, 265),
				(731, 218), (713, 183)),
			_poly((688, 151), (724, 151), (713, 193), (700, 225),
				(688, 269), (654, 271), (663, 226), (674, 188)),
			_ellipse((669, 173, 691, 195)),
			_ellipse((657, 205, 681, 230)),
		)),
	],
	"bubble_bath": [
		("rubber_duck", (279, 207, 320, 247), (
			_ellipse((287, 225, 317, 244)),
			_ellipse((288, 210, 310, 233)),
			_poly((280, 220), (291, 218), (292, 229), (283, 231)),
			_poly((312, 224), (320, 229), (313, 236)),
		)),
		("bathtub", (76, 157, 397, 355), (
			_poly((107, 226), (137, 194), (185, 176), (285, 170),
				(351, 199), (386, 256), (379, 307), (349, 343),
				(143, 351), (91, 308), (87, 265)),
			_poly((149, 231), (149, 188), (164, 169), (206, 158),
				(235, 165), (241, 187), (226, 199), (200, 185),
				(176, 194), (176, 231)),
		)),
		("sink", (440, 137, 645, 310), (
			_ellipse((462, 140, 621, 211)),
			_rounded_rect((466, 185, 619, 286), 20),
			_ellipse((459, 265, 626, 304)),
			_poly((507, 191), (507, 160), (518, 148), (532, 147),
				(545, 160), (545, 190)),
		)),
		("toilet", (753, 154, 906, 346), (
			_ellipse((793, 157, 889, 245)),
			_ellipse((764, 222, 873, 288)),
			_poly((778, 260), (856, 257), (874, 301), (859, 337),
				(789, 339), (770, 307)),
		)),
	],
}


def _normalized_backdrop(room_id: str) -> Image.Image:
	path = ROOM_DIR / f"room_{room_id}.png"
	source_path = path
	if room_id == "kitchen":
		source_path = KITCHEN_GENERATED_SOURCE
	elif room_id == "mermaid_pool":
		source_path = MERMAID_POOL_GENERATED_SOURCE
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
	layer order and can hide Roshan. The provisional clean plate supplies a
	same-canvas background estimate. Strong source/plate differences seed the object, close
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
	# threshold remains a true silhouette for mobile layer ordering.
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
	"""Create a small transparent contact-shadow card for Sprite2D actors."""
	shadow = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
	mask = Image.new("L", shadow.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((10, 11, 246, 55), fill=145)
	mask = mask.filter(ImageFilter.GaussianBlur(6.0))
	shadow.putalpha(mask)
	shadow.save(ROOM_DIR / "room_actor_shadow.png", optimize=True)


def main() -> None:
	# Accepted runtime-correction evidence predates the deterministic room
	# rebuilds. Preserve every dated record rather than silently erasing newer
	# reviewed audits whenever the clean plates are regenerated.
	prior_runtime_corrections: dict[str, dict[str, object]] = {}
	if AUDIT_PATH.exists():
		try:
			prior_manifest = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
			for key, value in prior_manifest.items():
				if key.startswith("runtime_correction_") and isinstance(value, dict):
					prior_runtime_corrections[key] = value
		except (OSError, json.JSONDecodeError):
			prior_runtime_corrections = {}
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
			"world_root": "Node2D",
			"camera": "none",
			"coordinate_system": "direct_canvas_coordinates",
			"world_art_allowed": ["Sprite2D:unshaded"],
			"world_art_forbidden": [
				"Node3D",
				"Sprite3D",
				"Camera3D",
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
			"reference_steady_sprite2d_inventory": {
				"background": 1,
				"touch_props": {
					"minimum_per_destination_room": 4,
					"maximum_per_room": 7,
					"average_per_room": 4.75,
					"physical_instances": 38,
				},
				"midground_max": 1,
				"foreground_max": 2,
				"player": 1,
				"contact_shadow": 1,
			},
			"native_master_runtime_note": (
				"Background and any over-1024 layer counts expand only by "
				"the minimum lossless non-overlapping tile count in Canvas order."),
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
	for key, value in prior_runtime_corrections.items():
		manifest[key] = value
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
		elif room_id == "mermaid_pool":
			with Image.open(MERMAID_POOL_GENERATED_SOURCE) as generated:
				room_record.update({
					"generation_master": MERMAID_POOL_GENERATED_SOURCE.relative_to(
						ROOT).as_posix(),
					"generation_master_dimensions": list(generated.size),
					"generation_master_sha256": _sha256(
						MERMAID_POOL_GENERATED_SOURCE),
					"generation_method": (
						"OpenAI built-in ImageGen complete full-frame "
						"reference-guided regeneration"),
					"generation_prompt_record": (
						"assets_src/imagegen/mermaid_pool_room_2026-08-02/"
						"PROVENANCE.md"),
				})
		manifest["rooms"][room_id] = room_record
	_build_actor_shadow()
	AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
	AUDIT_PATH.write_text(
		json.dumps(manifest, indent=2, sort_keys=True) + "\n",
		encoding="utf-8")


if __name__ == "__main__":
	main()
