"""Refine Pearl Castle static depth cards to physical foreground subjects.

The room cards were originally cut with broad routing polygons. Their RGB is
pixel-exact source-room art, but some alpha mattes still own attached pieces of
wall, floor, rugs, and contact-shadow smear. In the Canvas2D runtime, those
pixels still draw in front of Roshan and can hide her.

This tool is deliberately independent of the V4 interaction builders/audits.
It preserves each original card alpha plane under ``assets_src`` and rebuilds
the runtime PNG from the approved room plate plus a reviewed, card-local keep
mask.  It never paints, resamples, or substitutes visible RGB.  Fully
transparent output pixels are normalized to transparent black.

Run from the repository root:

    python tools/refine_castle_depth_cards.py --apply
    python tools/refine_castle_depth_cards.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
SOURCE_ROOT = ROOT / "assets_src" / "castle" / "depth_cards"
SOURCE_ALPHA_ROOT = SOURCE_ROOT / "source_alpha"
PROVENANCE_PATH = SOURCE_ROOT / "static_depth_card_refinement.json"
CONTACT_PATH = (
    ROOT / "audit" / "castle_static_depth_cards"
    / "static_depth_card_refinement_contact.png"
)
RUNTIME_LAYOUT_PATH = ROOT / "scripts" / "arena" / "castle_rooms_25d.gd"
ALPHA_SCISSOR_THRESHOLD = 128
MASK_FEATHER_RADIUS = 0.75


Shape = dict[str, Any]


def polygon(*points: tuple[int, int]) -> Shape:
	return {"type": "polygon", "points": [list(point) for point in points]}


def ellipse(box: tuple[int, int, int, int]) -> Shape:
	return {"type": "ellipse", "box": list(box)}


def rounded_rectangle(
		box: tuple[int, int, int, int], radius: int = 0) -> Shape:
	return {"type": "rounded_rectangle", "box": list(box), "radius": radius}


@dataclass(frozen=True)
class CardSpec:
	room: str
	card_id: str
	position: tuple[int, int]
	keep_shapes: tuple[Shape, ...]
	method: str = "reviewed_physical_subject_intersection"

	@property
	def path(self) -> Path:
		return ROOM_DIR / f"room_{self.room}_{self.card_id}.png"

	@property
	def source_room_path(self) -> Path:
		return ROOM_DIR / f"room_{self.room}.png"

	@property
	def source_alpha_path(self) -> Path:
		return SOURCE_ALPHA_ROOT / f"room_{self.room}_{self.card_id}_alpha.png"


def preserve_card(room: str, card_id: str, position: tuple[int, int]) -> CardSpec:
	# A full-card shape records that the existing silhouette is intentionally
	# preserved.  The shape is replaced with the exact dimensions in provenance.
	return CardSpec(
		room, card_id, position, (), "preserve_approved_alpha_zero_hidden_rgb")


# Coordinates are local to each existing cropped PNG.  Every region was traced
# over an alpha-scissor checker preview.  The regions are intentionally outside
# the painted outlines; the retained edge itself always comes from the original
# alpha plane.
CARD_SPECS: tuple[CardSpec, ...] = (
	preserve_card("opera_hall", "front_left", (0, 252)),
	preserve_card("opera_hall", "front_right", (750, 252)),
	CardSpec("kitchen", "front_left", (0, 354), (
		# Stockpot, traced below the painted cabinet edge behind its lid.
		polygon((10, 88), (20, 68), (38, 60), (43, 49), (62, 40),
			(88, 34), (108, 39), (122, 50), (132, 68), (136, 96),
			(128, 121), (112, 143), (84, 155), (50, 153), (25, 137),
			(13, 116)),
		# Left coral is a separate subject; the cabinet and floor between the
		# coral and stockpot are intentionally not retained.
		polygon((0, 88), (20, 83), (39, 97), (55, 119), (66, 151),
			(64, 181), (48, 205), (22, 218), (0, 218)),
		# Utensil jar and spoons.
		polygon((129, 60), (141, 49), (159, 42), (181, 43), (201, 53),
			(218, 73), (225, 100), (222, 134), (210, 158), (191, 174),
			(158, 174), (137, 157), (130, 126)),
		# Foreground shell bowl.
		polygon((55, 129), (69, 113), (91, 105), (119, 106), (143, 115),
			(160, 130), (178, 133), (193, 150), (198, 178), (190, 204),
			(172, 222), (73, 222), (55, 204), (48, 178)),
		# Pearls and shell forms at the crop edge, without the green cabinet
		# triangle that used to join them to the utensil jar.
		polygon((166, 188), (181, 177), (194, 163), (211, 158),
			(229, 165), (240, 181), (260, 184), (286, 199), (286, 222),
			(160, 222)),
	)),
	CardSpec("kitchen", "front_right", (650, 324), (
		# Tabletop begins at its cream/gold edge; the green rear counter strip
		# above it is background and must not write depth.
		polygon((15, 75), (47, 62), (82, 59), (112, 63), (145, 68),
			(180, 70), (215, 70), (251, 67), (286, 61), (315, 64),
			(340, 76), (355, 96), (355, 112), (342, 124), (318, 129),
			(285, 125), (250, 134), (210, 133), (175, 140), (135, 132),
			(95, 137), (55, 128), (22, 111), (8, 91)),
		# Objects sitting above the tabletop are retained independently so the
		# background between them stays transparent.
		ellipse((101, 31, 189, 97)),
		ellipse((197, 80, 229, 116)),
		polygon((234, 56), (248, 45), (270, 42), (294, 48), (311, 61),
			(321, 81), (319, 101), (304, 111), (271, 112), (244, 101),
			(234, 82)),
		ellipse((34, 108, 101, 194)),
		ellipse((128, 121, 194, 176)),
		ellipse((242, 108, 318, 197)),
		rounded_rectangle((321, 178, 374, 252), 18),
	)),
	CardSpec("library", "front_left", (0, 273), (
		polygon((70, 10), (105, 0), (165, 0), (205, 18), (235, 48),
			(257, 80), (275, 116), (275, 165), (260, 190), (225, 210),
			(180, 211), (140, 210), (110, 198), (90, 170), (82, 140),
			(65, 120), (55, 90), (58, 50)),
	)),
	CardSpec("library", "front_right", (724, 273), (
		polygon((40, 10), (70, 0), (145, 0), (185, 20), (210, 50),
			(220, 95), (210, 135), (195, 165), (170, 190), (130, 210),
			(75, 210), (35, 192), (15, 160), (20, 120), (30, 75)),
		# Right stack: one shape per outlined book/pearl.  Broad stack
		# polygons retained a single purple floor slab between the books.
		ellipse((223, 83, 260, 118)),
		polygon((215, 104), (300, 108), (300, 137), (211, 139)),
		polygon((210, 132), (300, 134), (300, 165), (207, 165)),
		polygon((204, 158), (300, 159), (300, 194), (201, 195)),
		polygon((208, 187), (300, 184), (300, 224), (204, 226)),
		polygon((199, 217), (300, 213), (300, 253), (197, 255)),
		polygon((196, 247), (300, 241), (300, 281), (194, 285)),
		polygon((202, 270), (300, 268), (300, 282), (198, 285)),
		# Smaller foreground stack.
		polygon((124, 183), (205, 184), (217, 202), (208, 220),
			(120, 216), (114, 199)),
		polygon((117, 207), (213, 208), (219, 238), (205, 250),
			(113, 244), (108, 223)),
		polygon((124, 235), (211, 238), (214, 271), (202, 279),
			(121, 275), (116, 252)),
		polygon((137, 265), (213, 270), (215, 286), (205, 289),
			(135, 286), (130, 276)),
	)),
	CardSpec("playroom", "front_left", (0, 319), (
		polygon((0, 35), (35, 25), (65, 15), (110, 7), (135, 22),
			(155, 35), (185, 25), (210, 40), (220, 62), (217, 160),
			(203, 179), (175, 185), (35, 185), (0, 176)),
	)),
	CardSpec("playroom", "front_right", (777, 319), (
		polygon((40, 30), (70, 15), (110, 5), (145, 15), (185, 10),
			(220, 25), (247, 48), (247, 175), (225, 185), (40, 185),
			(15, 178), (15, 70)),
		polygon((58, 0), (151, 0), (156, 37), (55, 37)),
	)),
	CardSpec("craft_room", "front_left", (0, 316), (
		# Thin top and cabinet body are distinct to exclude the torn floor/wall
		# wedges that were connected at the right edge.
		polygon((0, 66), (42, 75), (90, 81), (140, 81), (188, 74),
			(232, 62), (250, 68), (255, 82), (247, 96), (205, 100),
			(150, 102), (95, 101), (42, 96), (0, 88)),
		polygon((0, 86), (30, 91), (90, 96), (150, 96), (205, 92),
			(244, 84), (244, 210), (230, 227), (30, 230), (0, 216)),
		rounded_rectangle((178, 0, 214, 78), 8),
		ellipse((130, 54, 226, 96)),
	)),
	CardSpec("craft_room", "front_right", (720, 316), (
		# Paint dishes, two brush cups, and rolled-paper cups are separate from
		# the workstation so gaps show the healed room background.
		polygon((0, 24), (24, 12), (60, 8), (91, 19), (99, 48),
			(86, 72), (40, 78), (0, 66)),
		rounded_rectangle((91, 0, 162, 79), 10),
		rounded_rectangle((151, 0, 232, 82), 10),
		polygon((220, 12), (250, 5), (283, 12), (304, 25), (304, 78),
			(278, 86), (236, 80), (218, 58)),
		polygon((0, 69), (42, 75), (92, 80), (145, 80), (198, 77),
			(250, 70), (288, 63), (304, 68), (304, 216), (285, 228),
			(25, 228), (5, 215), (5, 92)),
	)),
	CardSpec("mermaid_pool", "front_left", (0, 430), (
		polygon((0, 16), (10, 12), (20, 29), (18, 55), (29, 72),
			(25, 96), (0, 105)),
		polygon((19, 42), (35, 35), (58, 39), (79, 47), (96, 61),
			(102, 84), (96, 108), (78, 122), (45, 123), (24, 105)),
		polygon((0, 91), (25, 88), (49, 101), (70, 94), (91, 100),
			(107, 111), (129, 110), (155, 123), (160, 146), (0, 146)),
	)),
	CardSpec("mermaid_pool", "front_right", (885, 435), (
		polygon((76, 11), (103, 7), (121, 20), (130, 43), (126, 84),
			(112, 103), (91, 96), (72, 79)),
		polygon((36, 40), (57, 29), (75, 39), (87, 61), (83, 97),
			(66, 113), (43, 108), (28, 84)),
		polygon((0, 84), (28, 72), (48, 82), (66, 96), (89, 92),
			(108, 102), (139, 111), (139, 141),
			(0, 141)),
	)),
)


RETIRED_CARDS: tuple[dict[str, Any], ...] = (
	{
		"room": "bubble_bath",
		"id": "front_left",
		"role": "foreground",
		"path": "assets/flats/castle/rooms/room_bubble_bath_front_left.png",
		"position": [0, 358],
		"reason": "phone_scale_shell_towel_basket_silhouette_reads_as_a_false_second_bathtub",
	},
	{
		"room": "bubble_bath",
		"id": "front_right",
		"role": "foreground",
		"path": "assets/flats/castle/rooms/room_bubble_bath_front_right.png",
		"position": [798, 358],
		"reason": "phone_scale_shell_towel_basket_silhouette_reads_as_a_false_second_bathtub",
	},
	{
		"room": "main_hall",
		"id": "front_left",
		"role": "foreground",
		"path": "assets/flats/castle/rooms/room_main_hall_front_left.png",
		"position": [0, 0],
		"reason": "approved_panorama_already_contains_complete_hall_architecture",
	},
	{
		"room": "main_hall",
		"id": "front_right",
		"role": "foreground",
		"path": "assets/flats/castle/rooms/room_main_hall_front_right.png",
		"position": [750, 0],
		"reason": "approved_panorama_already_contains_complete_hall_architecture",
	},
	{
		"room": "mermaid_pool",
		"id": "mid_pool",
		"role": "midground",
		"path": "assets/flats/castle/rooms/room_mermaid_pool_mid_pool.png",
		"position": [0, 218],
		"reason": "pool_water_oval_is_background_not_a_physical_depth_subject",
	},
)


def sha256_bytes(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
	with path.open("rb") as stream:
		return hashlib.sha256(stream.read()).hexdigest()


def relative(path: Path) -> str:
	return path.relative_to(ROOT).as_posix()


def rasterize_shapes(size: tuple[int, int], shapes: Iterable[Shape],
		feather_radius: float = 0.0) -> Image.Image:
	mask = Image.new("L", size, 0)
	draw = ImageDraw.Draw(mask)
	for shape in shapes:
		shape_type = str(shape.get("type", ""))
		if shape_type == "polygon":
			draw.polygon([tuple(point) for point in shape["points"]], fill=255)
		elif shape_type == "ellipse":
			draw.ellipse(tuple(shape["box"]), fill=255)
		elif shape_type == "rounded_rectangle":
			draw.rounded_rectangle(
				tuple(shape["box"]), radius=int(shape.get("radius", 0)), fill=255)
		else:
			raise ValueError(f"unsupported keep shape: {shape_type!r}")
	if feather_radius > 0.0:
		mask = mask.filter(ImageFilter.GaussianBlur(feather_radius))
	return mask


def clean_rgba(rgb: np.ndarray, alpha: np.ndarray) -> Image.Image:
	rgba = np.dstack((rgb.copy(), alpha.copy())).astype(np.uint8)
	rgba[rgba[:, :, 3] == 0, :3] = 0
	return Image.fromarray(rgba, "RGBA")


def metrics(image: Image.Image) -> dict[str, Any]:
	rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
	alpha = rgba[:, :, 3]
	hidden = (alpha == 0) & np.any(rgba[:, :, :3] != 0, axis=2)
	nonzero = alpha > 0
	core = alpha >= ALPHA_SCISSOR_THRESHOLD
	if np.any(core):
		y_values, x_values = np.nonzero(core)
		bbox = [
			int(x_values.min()), int(y_values.min()),
			int(x_values.max()) + 1, int(y_values.max()) + 1,
		]
	else:
		bbox = [0, 0, 0, 0]
	return {
		"alpha_pixels": int(np.count_nonzero(nonzero)),
		"core_pixels": int(np.count_nonzero(core)),
		"hidden_rgb_pixels": int(np.count_nonzero(hidden)),
		"core_bbox": bbox,
	}


def raw_plane_hash(alpha: np.ndarray) -> str:
	return sha256_bytes(np.asarray(alpha, dtype=np.uint8).tobytes())


def core_plane_hash(alpha: np.ndarray) -> str:
	core = np.where(
		alpha >= ALPHA_SCISSOR_THRESHOLD, 255, 0).astype(np.uint8)
	return sha256_bytes(core.tobytes())


def source_alpha(spec: CardSpec, bootstrap: bool) -> Image.Image:
	if spec.source_alpha_path.is_file():
		return Image.open(spec.source_alpha_path).convert("L")
	if not bootstrap:
		raise FileNotFoundError(
			f"missing source alpha evidence: {relative(spec.source_alpha_path)}")
	card = Image.open(spec.path).convert("RGBA")
	spec.source_alpha_path.parent.mkdir(parents=True, exist_ok=True)
	card.getchannel("A").save(spec.source_alpha_path, optimize=True)
	return card.getchannel("A")


def source_card(spec: CardSpec, bootstrap: bool) -> tuple[Image.Image, Image.Image]:
	current = Image.open(spec.path).convert("RGBA")
	alpha_image = source_alpha(spec, bootstrap)
	if alpha_image.size != current.size:
		raise ValueError(f"source alpha size mismatch: {relative(spec.path)}")
	x, y = spec.position
	room = Image.open(spec.source_room_path).convert("RGB")
	width, height = current.size
	if x < 0 or y < 0 or x + width > room.width or y + height > room.height:
		raise ValueError(f"card crop escapes room plate: {relative(spec.path)}")
	rgb = np.asarray(room.crop((x, y, x + width, y + height)), dtype=np.uint8)
	alpha = np.asarray(alpha_image, dtype=np.uint8)
	# Reconstruct the original broad card exactly, including source-room RGB below
	# transparent alpha.  The output path cleans that latent RGB; retaining it here
	# makes the before/after provenance honest and reproducible after first apply.
	source_rgba = np.dstack((rgb.copy(), alpha.copy())).astype(np.uint8)
	return Image.fromarray(source_rgba, "RGBA"), alpha_image


def refined_card(spec: CardSpec, bootstrap: bool = False) -> tuple[Image.Image, Image.Image]:
	source, alpha_image = source_card(spec, bootstrap)
	alpha = np.asarray(alpha_image, dtype=np.uint8)
	if spec.method.startswith("preserve_"):
		refined_alpha = alpha.copy()
	else:
		keep = np.asarray(rasterize_shapes(
			source.size, spec.keep_shapes, MASK_FEATHER_RADIUS), dtype=np.uint8)
		refined_alpha = np.minimum(alpha, keep)
		# Gaussian feathering can round a boundary sample to exactly the
		# alpha-scissor threshold one pixel outside the authored hard shape.
		# Keep that soft fringe for filtering, but never let it write depth.
		hard_keep = np.asarray(rasterize_shapes(
			source.size, spec.keep_shapes), dtype=np.uint8)
		outside_core = (hard_keep == 0) & (
			refined_alpha >= ALPHA_SCISSOR_THRESHOLD)
		refined_alpha[outside_core] = ALPHA_SCISSOR_THRESHOLD - 1
	rgb = np.asarray(source.convert("RGB"), dtype=np.uint8)
	return clean_rgba(rgb, refined_alpha), source


def png_bytes(image: Image.Image) -> bytes:
	stream = io.BytesIO()
	image.save(stream, format="PNG", optimize=True)
	return stream.getvalue()


def png_bytes_preserving_pixels(path: Path, image: Image.Image) -> bytes:
	"""Preserve committed PNG bytes only for an exact decoded-pixel match.

	Pinned Pillow versions can still use different zlib encodings on Windows
	and Linux. Runtime behavior is defined by the decoded image, while the
	provenance continues to bind the exact committed artifact bytes. A mode,
	size, or single-channel pixel change always forces a rebuilt encoding.
	"""
	if path.is_file():
		try:
			existing_bytes = path.read_bytes()
			with Image.open(io.BytesIO(existing_bytes)) as existing:
				if existing.mode == image.mode and existing.size == image.size \
						and existing.tobytes() == image.tobytes():
					return existing_bytes
		except (OSError, ValueError):
			pass
	return png_bytes(image)


def raw_pixel_hash(image: Image.Image) -> str:
	return sha256_bytes(image.tobytes())


def provenance_shapes(spec: CardSpec, size: tuple[int, int]) -> list[Shape]:
	if spec.keep_shapes:
		return [json.loads(json.dumps(shape)) for shape in spec.keep_shapes]
	return [rounded_rectangle((0, 0, size[0], size[1]), 0)]


def card_record(spec: CardSpec, output: Image.Image, source: Image.Image) -> dict[str, Any]:
	alpha = np.asarray(output.getchannel("A"), dtype=np.uint8)
	x, y = spec.position
	width, height = output.size
	return {
		"room": spec.room,
		"id": spec.card_id,
		"role": "foreground",
		"path": relative(spec.path),
		"position": [x, y],
		"crop": [x, y, x + width, y + height],
		"source_sha256": sha256_bytes(source.tobytes()),
		"source_sha256_kind": "raw_rgba_bytes",
		"source_room_path": relative(spec.source_room_path),
		"source_room_sha256": sha256_file(spec.source_room_path),
		"source_alpha_path": relative(spec.source_alpha_path),
		"source_alpha_sha256": sha256_file(spec.source_alpha_path),
		"output_sha256": sha256_bytes(
			png_bytes_preserving_pixels(spec.path, output)),
		"alpha_sha256": raw_plane_hash(alpha),
		"core_mask_sha256": core_plane_hash(alpha),
		"before": metrics(source),
		"after": metrics(output),
		"keep_shapes": provenance_shapes(spec, output.size),
		"mask_feather_radius": 0.0 if spec.method.startswith("preserve_")
			else MASK_FEATHER_RADIUS,
		"method": spec.method,
		"visible_rgb_operation": "none_source_room_pixels_only",
		"transparent_rgb_operation": "zero_rgb_where_alpha_is_zero",
	}


def checker_preview(image: Image.Image, scale: int = 2) -> Image.Image:
	image = image.convert("RGBA")
	width, height = image.size
	checker = Image.new("RGB", image.size, (238, 229, 246))
	draw = ImageDraw.Draw(checker)
	cell = 12
	for y in range(0, height, cell):
		for x in range(0, width, cell):
			if (x // cell + y // cell) % 2:
				draw.rectangle((x, y, x + cell - 1, y + cell - 1),
					fill=(207, 194, 222))
	checker.paste(image, mask=image.getchannel("A"))
	return checker.resize((width * scale, height * scale), Image.Resampling.NEAREST)


def contact_sheet(entries: list[tuple[CardSpec, Image.Image, Image.Image]]) -> Image.Image:
	rows: list[Image.Image] = []
	for spec, before, after in entries:
		before_preview = checker_preview(before)
		after_preview = checker_preview(after)
		width = before_preview.width + after_preview.width
		height = max(before_preview.height, after_preview.height) + 30
		row = Image.new("RGB", (width, height), "white")
		row.paste(before_preview, (0, 30))
		row.paste(after_preview, (before_preview.width, 30))
		before_core = metrics(before)["core_pixels"]
		after_core = metrics(after)["core_pixels"]
		ImageDraw.Draw(row).text(
			(4, 5),
			f"{spec.room}:{spec.card_id}  before {before_core}  after {after_core}",
			fill="black",
		)
		rows.append(row)
	width = max(row.width for row in rows)
	height = sum(row.height for row in rows)
	sheet = Image.new("RGB", (width, height), "white")
	y = 0
	for row in rows:
		sheet.paste(row, (0, y))
		y += row.height
	return sheet


def build_outputs(bootstrap: bool) -> tuple[
		list[tuple[CardSpec, Image.Image, Image.Image]], dict[str, Any], Image.Image]:
	entries: list[tuple[CardSpec, Image.Image, Image.Image]] = []
	records: list[dict[str, Any]] = []
	for spec in CARD_SPECS:
		output, source = refined_card(spec, bootstrap)
		if metrics(output)["hidden_rgb_pixels"] != 0:
			raise ValueError(f"hidden RGB survived: {relative(spec.path)}")
		if not spec.method.startswith("preserve_") \
				and metrics(output)["core_pixels"] >= metrics(source)["core_pixels"]:
			raise ValueError(f"trim did not reduce core alpha: {relative(spec.path)}")
		entries.append((spec, source, output))
		records.append(card_record(spec, output, source))
	sheet = contact_sheet(entries)
	retired: list[dict[str, Any]] = []
	for record in RETIRED_CARDS:
		value = dict(record)
		path = ROOT / value["path"]
		value["source_sha256"] = sha256_file(path)
		retired.append(value)
	provenance = {
		"schema_version": 2,
		"generated_by": "tools/refine_castle_depth_cards.py",
		"alpha_scissor_threshold": ALPHA_SCISSOR_THRESHOLD,
		"runtime_layout_path": relative(RUNTIME_LAYOUT_PATH),
		"cards": records,
		"retired_cards": retired,
		"contact_sheet": {
			"path": relative(CONTACT_PATH),
			"raw_pixel_sha256": raw_pixel_hash(sheet),
		},
		"constraints": {
			"visible_rgb_repainted": False,
			"source_room_art_reused_exactly": True,
			"transparent_rgb_zeroed": True,
			"legacy_hall_front_cards_runtime_retired": True,
			"pool_mid_card_runtime_retired": True,
			"bubble_bath_false_tub_card_runtime_retired": True,
		},
	}
	return entries, provenance, sheet


def json_bytes(value: dict[str, Any]) -> bytes:
	return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def apply() -> int:
	entries, provenance, sheet = build_outputs(bootstrap=True)
	for spec, _source, output in entries:
		spec.path.write_bytes(png_bytes_preserving_pixels(spec.path, output))
	CONTACT_PATH.parent.mkdir(parents=True, exist_ok=True)
	CONTACT_PATH.write_bytes(png_bytes_preserving_pixels(CONTACT_PATH, sheet))
	PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	PROVENANCE_PATH.write_bytes(json_bytes(provenance))
	for record in provenance["cards"]:
		print(
			"CASTLE_DEPTH_REFINE|CARD|"
			f"{record['room']}:{record['id']}|"
			f"core={record['before']['core_pixels']}->{record['after']['core_pixels']}|"
			f"hidden_rgb={record['before']['hidden_rgb_pixels']}->0"
		)
	print("CASTLE_DEPTH_REFINE|RESULT=APPLIED")
	return 0


def check() -> int:
	problems: list[str] = []
	try:
		entries, expected_provenance, expected_sheet = build_outputs(bootstrap=False)
	except (FileNotFoundError, OSError, ValueError) as exc:
		print(f"CASTLE_DEPTH_REFINE|FAIL|{exc}")
		print("CASTLE_DEPTH_REFINE|RESULT=FAIL|count=1")
		return 1
	for spec, _source, expected in entries:
		try:
			actual = Image.open(spec.path).convert("RGBA")
			actual.load()
		except (OSError, ValueError) as exc:
			problems.append(f"cannot decode {relative(spec.path)}: {exc}")
			continue
		if actual.size != expected.size or actual.tobytes() != expected.tobytes():
			problems.append(f"card differs from deterministic output: {relative(spec.path)}")
		if metrics(actual)["hidden_rgb_pixels"]:
			problems.append(f"hidden RGB remains: {relative(spec.path)}")
	if not PROVENANCE_PATH.is_file():
		problems.append(f"missing provenance: {relative(PROVENANCE_PATH)}")
	else:
		try:
			actual_provenance = json.loads(PROVENANCE_PATH.read_text("utf-8"))
		except (OSError, json.JSONDecodeError) as exc:
			problems.append(f"cannot read provenance: {exc}")
		else:
			if actual_provenance != expected_provenance:
				problems.append("provenance differs from deterministic output")
	if not CONTACT_PATH.is_file():
		problems.append(f"missing contact sheet: {relative(CONTACT_PATH)}")
	else:
		try:
			actual_sheet = Image.open(CONTACT_PATH)
			actual_sheet.load()
		except (OSError, ValueError) as exc:
			problems.append(f"cannot decode contact sheet: {exc}")
		else:
			if actual_sheet.mode != expected_sheet.mode \
					or actual_sheet.size != expected_sheet.size \
					or actual_sheet.tobytes() != expected_sheet.tobytes():
				problems.append("contact sheet differs from deterministic output")
	if problems:
		for problem in problems:
			print(f"CASTLE_DEPTH_REFINE|FAIL|{problem}")
		print(f"CASTLE_DEPTH_REFINE|RESULT=FAIL|count={len(problems)}")
		return 1
	print("CASTLE_DEPTH_REFINE|RESULT=OK|cards=16|hidden_rgb=0")
	return 0


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--apply", action="store_true",
			help="preserve source alpha evidence and write refined cards/provenance")
	mode.add_argument("--check", action="store_true",
			help="verify cards/provenance without writing")
	args = parser.parse_args()
	return apply() if args.apply else check()


if __name__ == "__main__":
	raise SystemExit(main())
