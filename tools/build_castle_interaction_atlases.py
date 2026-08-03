"""Build clean, fixed-pivot Pearl Castle interaction atlases.

The room composites remain immutable source art. Room-derived rest poses reuse
the already outline-refined depth-card alpha exactly; re-segmenting those cards
against a healed plate punched holes through low-contrast doors, boards, lamps,
and furniture. The few fixtures that could not be isolated from room pixels use
the reviewed ImageGen extraction masters recorded in the manifest.

Every delivered frame is a full, same-size prop cell.  Motion is confined to a
meaningful part of the prop (door, handle, water, page, light, toy piece, etc.),
so Roshan can pass behind transparent areas without being clipped by a moving
rectangle of wall or floor.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter
from scipy.ndimage import binary_closing, label


ROOT = Path(__file__).resolve().parents[1]
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
HALL_DIR = ROOT / "assets" / "flats" / "castle" / "main_hall_2screen"
SOURCE_DIR = ROOT / "assets_src" / "imagegen" / "castle_interactions_2026-08-01"
OUTPUT_DIR = ROOT / "assets" / "flats" / "castle" / "interactions"
AUDIT_DIR = ROOT / "audit" / "castle_interactions"
DEPTH_MANIFEST = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
MANIFEST_PATH = OUTPUT_DIR / "castle_interactions.json"
AUDIO_MANIFEST_PATH = (
	ROOT / "assets" / "audio" / "castle" / "castle_interaction_sfx_manifest.json")
CONTACT_PATH = AUDIT_DIR / "castle_interaction_frames.png"
MAX_TEXTURE_EDGE = 1024
FRAME_COUNT = 8
NORMALIZED_USE_REVIEW = "accepted_visual_review_2026-08-01"
TIMELINE_SYNC = "sound_starts_with_frame_0_and_ends_with_frame_7"


@dataclass(frozen=True)
class Spec:
	room: str
	item: str
	action: str
	mode: str
	sound: str
	sound_frame: int = 0
	duration: float = 0.10
	instances: tuple[str, ...] = ()
	external: str = ""
	threshold: int = 16
	cell: tuple[int, int] | None = None

	@property
	def asset_id(self) -> str:
		return f"{self.room}_{self.item}"

	@property
	def instance_ids(self) -> tuple[str, ...]:
		return self.instances or (self.item,)


SPECS: tuple[Spec, ...] = (
	Spec("main_hall", "tapestry", "unfurl_cloth", "tapestry",
		"castle/curtain_swish.ogg", duration=0.125,
		instances=("tapestry_right",), cell=(138, 328)),
	Spec("main_hall", "sconce", "toggle_shell_light", "lights",
		"castle/light_switch.ogg", duration=0.1025,
		instances=("sconce_a0", "sconce_a1", "sconce_a2",
			"sconce_b0", "sconce_b1", "sconce_b2"), cell=(160, 160)),
	Spec("opera_hall", "curtains", "open_stage_curtains", "curtains",
		"castle/curtain_swish.ogg", duration=0.125),
	Spec("opera_hall", "chandelier", "chandelier_light_chase", "lights",
		"castle/light_switch.ogg", duration=0.1025),
	Spec("opera_hall", "footlights", "stage_footlight_chase", "lights",
		"castle/light_switch.ogg", duration=0.1025),
	Spec("opera_hall", "stage_star", "marquee_star_light_chase", "lights",
		"castle/light_switch.ogg", duration=0.1025),
	Spec("kitchen", "sink", "turn_faucet_and_run_water", "faucet",
		"castle/faucet_water.ogg", duration=0.15),
	Spec("kitchen", "pan_1", "swing_pan_on_hook", "pan",
		"castle/pan_clang.ogg", duration=0.115, threshold=8),
	Spec("kitchen", "pan_2", "swing_pan_on_hook", "pan",
		"castle/pan_clang.ogg", duration=0.115, threshold=8),
	Spec("kitchen", "pan_3", "swing_pan_on_hook", "pan",
		"castle/pan_clang.ogg", duration=0.115, threshold=8),
	Spec("kitchen", "pan_4", "swing_pan_on_hook", "pan",
		"castle/pan_clang.ogg", duration=0.115, threshold=7),
	Spec("kitchen", "oven", "open_oven_door_and_warm_fire", "oven",
		"castle/oven_door.ogg", duration=0.1625),
	Spec("kitchen", "fridge", "unlatch_and_open_fridge_door", "fridge",
		"castle/fridge_door.ogg", duration=0.145),
	Spec("library", "book_stack", "open_top_book_and_turn_pages", "book",
		"castle/page_flip.ogg", duration=0.095),
	Spec("library", "magic_book", "open_book_and_turn_pages", "book",
		"castle/page_flip.ogg", duration=0.095),
	Spec("library", "pearl_table", "wake_reading_pearl", "pearl",
		"castle/light_switch.ogg", duration=0.1025),
	Spec("library", "pearl_lamp", "toggle_pearl_lamp", "lights",
		"castle/light_switch.ogg", duration=0.1025),
	Spec("playroom", "play_tent", "open_and_close_tent_flap", "tent",
		"castle/curtain_swish.ogg", duration=0.125),
	Spec("playroom", "stuffie_nook", "stuffie_friends_wave", "friends",
		"castle/toy_blocks.ogg", duration=0.1375),
	Spec("playroom", "stacking_toy", "lift_and_restack_rings", "rings",
		"castle/toy_blocks.ogg", duration=0.1375),
	Spec("playroom", "blocks", "topple_and_restack_blocks", "blocks",
		"castle/toy_blocks.ogg", duration=0.1375),
	Spec("craft_room", "ribbon_rack", "unroll_and_retract_ribbon", "ribbon",
		"castle/ribbon_roll.ogg", duration=0.1325),
	Spec("craft_room", "idea_board", "flip_idea_notes", "notes",
		"castle/page_flip.ogg", duration=0.095),
	Spec("craft_room", "paint_table", "stir_paint_with_brush", "paint",
		"castle/craft_brush.ogg", duration=0.12),
	Spec("craft_room", "palette", "mix_palette_colors", "paint",
		"castle/craft_brush.ogg", duration=0.12),
	Spec("mermaid_pool", "star_float", "float_and_make_ripples", "float",
		"castle/bubble_water.ogg", duration=0.185, threshold=8),
	Spec("mermaid_pool", "waterfall", "surge_waterfall_flow", "water",
		"castle/bubble_water.ogg", duration=0.185),
	Spec("mermaid_pool", "flower_float", "open_flower_and_make_ripples", "flower",
		"castle/bubble_water.ogg", duration=0.185),
	Spec("mermaid_pool", "seahorse_fountain", "spray_seahorse_fountain", "water",
		"castle/bubble_water.ogg", duration=0.185),
	Spec("bubble_bath", "rubber_duck", "squeak_dive_and_pop_up", "duck",
		"castle/duck_squeak.ogg", duration=0.0775, threshold=7,
		external="bathtub_alpha.png"),
	Spec("bubble_bath", "bathtub", "turn_taps_and_fill_bubbles", "bathtub",
		"castle/bubble_water.ogg", duration=0.185,
		external="bathtub_alpha.png"),
	Spec("bubble_bath", "sink", "turn_faucet_and_run_water", "faucet",
		"castle/faucet_water.ogg", duration=0.15,
		external="bathroom_sink_alpha_hard.png"),
	Spec("bubble_bath", "toilet", "flap_seat_and_flush", "toilet",
		"castle/toilet_flush.ogg", duration=0.225,
		external="toilet_alpha.png"),
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _depth_crops() -> dict[tuple[str, str], tuple[int, int, int, int]]:
	data = json.loads(DEPTH_MANIFEST.read_text(encoding="utf-8"))
	crops: dict[tuple[str, str], tuple[int, int, int, int]] = {}
	for room_id, room in data["rooms"].items():
		for card in room["cards"]:
			if card.get("role") != "item":
				continue
			item_id = str(card["id"]).removeprefix("item_")
			crops[(room_id, item_id)] = tuple(int(v) for v in card["crop"])
	return crops


def _source_path(spec: Spec) -> Path:
	if spec.external and (SOURCE_DIR / spec.external).exists():
		return SOURCE_DIR / spec.external
	if spec.room == "main_hall":
		name = (
			"castle_royal_tapestry_reuse.png"
			if spec.item == "tapestry"
			else "castle_shell_sconce_touchable.png"
		)
		return HALL_DIR / name
	return ROOM_DIR / f"room_{spec.room}_item_{spec.item}.png"


def _fit_external(source: Image.Image, size: tuple[int, int]) -> Image.Image:
	source = source.convert("RGBA")
	bbox = source.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("external source has no visible pixels")
	trimmed = source.crop(bbox)
	margin = 3
	scale = min(
		(size[0] - margin * 2) / trimmed.width,
		(size[1] - margin * 2) / trimmed.height,
	)
	new_size = (
		max(1, round(trimmed.width * scale)),
		max(1, round(trimmed.height * scale)),
	)
	trimmed = trimmed.resize(new_size, Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", size)
	position = ((size[0] - new_size[0]) // 2, size[1] - margin - new_size[1])
	canvas.alpha_composite(trimmed, position)
	return canvas


def _room_base(spec: Spec, crops: dict[tuple[str, str], tuple[int, int, int, int]]) -> Image.Image:
	path = _source_path(spec)
	image = Image.open(path).convert("RGBA")
	if spec.room == "main_hall":
		if spec.item == "sconce":
			bbox = image.getchannel("A").getbbox()
			if bbox is None:
				raise ValueError("sconce source is empty")
			return _fit_external(image.crop(bbox), spec.cell or (160, 160))
		if spec.cell is not None:
			return _fit_external(image, spec.cell)
		return image
	key = (spec.room, spec.item)
	if key not in crops:
		raise KeyError(f"missing source crop for {key}")
	crop = crops[key]
	size = (crop[2] - crop[0], crop[3] - crop[1])
	if spec.external and path.parent == SOURCE_DIR:
		if spec.item == "rubber_duck":
			return _fit_external(_extract_generated_duck(image), size)
		base = _fit_external(image, size)
		if spec.item == "bathtub":
			base = _remove_generated_duck(base)
		return base

	# The depth-card builder has already performed topology-aware watershed
	# refinement and the legacy blocking alpha audit verifies these bytes against
	# the healed plate. Preserve that accepted silhouette: a second color-delta
	# threshold here removes legitimate low-contrast interior pixels and lets the
	# actor draw through solid parts of the object.
	return image


def _extract_generated_duck(image: Image.Image) -> Image.Image:
	"""Color-isolate the approved yellow duck embedded in the clean tub source."""
	image = image.convert("RGBA")
	w, h = image.size
	region_box = (round(w * 0.64), round(h * 0.19), round(w * 0.84), round(h * 0.52))
	region = np.asarray(image.crop(region_box))
	rgb = region[:, :, :3]
	mask = (
		(region[:, :, 3] > 0)
		& (rgb[:, :, 0] >= 150)
		& (rgb[:, :, 1] >= 65)
		& (rgb[:, :, 2] <= 135)
		& (rgb[:, :, 0].astype(np.int16) - rgb[:, :, 2].astype(np.int16) >= 55)
	)
	mask = binary_closing(mask, iterations=3)
	components, count = label(mask)
	if count == 0:
		raise ValueError("generated tub duck color mask is empty")
	sizes = np.bincount(components.ravel())
	sizes[0] = 0
	mask = components == int(np.argmax(sizes))
	# Regrow the gold/orange outline immediately adjacent to the yellow body.
	mask = binary_closing(mask, iterations=2)
	alpha = np.where(mask, 255, 0).astype(np.uint8)
	result = Image.fromarray(region.copy(), mode="RGBA")
	result.putalpha(Image.fromarray(alpha, mode="L"))
	bbox = result.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("generated tub duck extraction is empty")
	return result.crop(bbox)


def _remove_generated_duck(image: Image.Image) -> Image.Image:
	"""Heal the generated tub's duck so the separately owned duck is unique."""
	w, h = image.size
	box = (round(w * 0.67), round(h * 0.24), round(w * 0.83), round(h * 0.53))
	width = box[2] - box[0]
	height = box[3] - box[1]
	source_box = (
		max(0, box[0] - width - round(w * 0.04)), box[1],
		max(0, box[0] - round(w * 0.04)), box[3],
	)
	patch = image.crop(source_box).resize((width, height), Image.Resampling.BICUBIC)
	mask = Image.new("L", (width, height))
	draw = ImageDraw.Draw(mask)
	draw.ellipse((0, 0, width - 1, height - 1), fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(max(1.0, min(width, height) * 0.08)))
	result = image.copy()
	result.paste(patch, box[:2], mask)
	return result


def _transparent_rgb(image: Image.Image) -> Image.Image:
	array = np.array(image.convert("RGBA"), copy=True)
	# Sprite-atlas filtering must never borrow an opaque texel from an adjacent
	# cell. A one-pixel transparent guard is therefore a delivery invariant,
	# including at the widest point of a transformed pan or diving duck.
	array[0, :, :] = 0
	array[-1, :, :] = 0
	array[:, 0, :] = 0
	array[:, -1, :] = 0
	array[array[:, :, 3] == 0, :3] = 0
	return Image.fromarray(array, mode="RGBA")


def _overlay(base: Image.Image) -> tuple[Image.Image, ImageDraw.ImageDraw]:
	layer = Image.new("RGBA", base.size)
	return layer, ImageDraw.Draw(layer)


def _composite(base: Image.Image, layer: Image.Image) -> Image.Image:
	return Image.alpha_composite(base, layer)


def _draw_glow(base: Image.Image, frame: int, anchors: list[tuple[float, float]]) -> Image.Image:
	w, h = base.size
	strength = (0.10, 0.35, 0.70, 1.0, 0.72, 0.42, 0.18, 0.0)[frame]
	layer, draw = _overlay(base)
	for index, (nx, ny) in enumerate(anchors):
		local = max(0.0, strength - abs((frame % max(1, len(anchors))) - index) * 0.08)
		radius = max(3, round(min(w, h) * (0.06 + local * 0.04)))
		x_pos, y_pos = round(nx * w), round(ny * h)
		draw.ellipse((x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius),
			fill=(255, 220, 104, round(65 + local * 150)))
	layer = layer.filter(ImageFilter.GaussianBlur(max(1.0, min(w, h) * 0.025)))
	return _composite(base, layer)


def _animate_lights(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	if h < w * 0.35:
		anchors = [(0.16 + index * 0.135, 0.48) for index in range(6)]
	elif w < h * 0.82:
		anchors = [(0.52, 0.37)]
	else:
		anchors = [(0.22 + index * 0.14, 0.67) for index in range(5)]
	return _draw_glow(base, frame, anchors)


def _animate_faucet(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	# The handle first turns, then a tapered stream reaches the basin.
	turn = (0, 12, 24, 30, 24, 12, 0, 0)[frame]
	handle_center = (round(w * 0.37), round(h * 0.24))
	length = max(4, round(w * 0.055))
	angle = math.radians(-20 + turn)
	draw.line((handle_center[0] - math.cos(angle) * length,
		handle_center[1] - math.sin(angle) * length,
		handle_center[0] + math.cos(angle) * length,
		handle_center[1] + math.sin(angle) * length),
		fill=(224, 151, 43, 255), width=max(2, round(w * 0.018)))
	flow = (0.0, 0.0, 0.35, 0.72, 1.0, 0.82, 0.36, 0.0)[frame]
	if flow > 0:
		x_pos = round(w * 0.52)
		y_start = round(h * 0.31)
		y_end = round(h * (0.38 + 0.30 * flow))
		width = max(2, round(w * (0.018 + flow * 0.014)))
		draw.line((x_pos, y_start, x_pos, y_end),
			fill=(105, 230, 248, 225), width=width)
		draw.arc((round(w * 0.31), round(h * 0.55), round(w * 0.72), round(h * 0.80)),
			0, 180, fill=(163, 245, 255, 210), width=max(1, width // 2))
	return _composite(base, layer)


def _animate_water(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	phase = frame / FRAME_COUNT
	for index in range(5):
		x_pos = round(w * (0.24 + 0.13 * index + 0.02 * math.sin((phase + index) * math.tau)))
		y_pos = round(h * (0.76 - ((phase + index * 0.19) % 1.0) * 0.52))
		radius = max(2, round(min(w, h) * (0.025 + (index % 2) * 0.012)))
		draw.ellipse((x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius),
			outline=(174, 246, 255, 220), width=max(1, radius // 3))
	stream_x = round(w * 0.50)
	for offset in (-0.055, 0.0, 0.055):
		x = stream_x + round(w * offset)
		draw.line((x, round(h * 0.23), x + round(math.sin(frame + offset) * 2), round(h * 0.78)),
			fill=(94, 222, 247, 95), width=max(1, round(w * 0.018)))
	return _composite(base, layer)


def _animate_pan(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	cut_y = max(1, round(h * 0.28))
	fixed = base.copy()
	fixed.paste((0, 0, 0, 0), (0, cut_y, w, h))
	body = base.crop((0, cut_y, w, h))
	angles = (0, -8, -15, -7, 9, 14, 6, 0)
	rotated = body.rotate(angles[frame], Image.Resampling.BICUBIC, expand=False,
		center=(w // 2, 0))
	fixed.alpha_composite(rotated, (0, cut_y))
	return fixed


def _animate_curtains(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	progress = (0.0, 0.18, 0.42, 0.72, 1.0, 0.72, 0.35, 0.0)[frame]
	result = base.copy()
	left_box = (round(w * 0.31), round(h * 0.30), round(w * 0.50), round(h * 0.87))
	right_box = (round(w * 0.50), left_box[1], round(w * 0.69), left_box[3])
	layer, draw = _overlay(base)
	draw.rounded_rectangle((left_box[0], left_box[1], right_box[2], left_box[3]),
		radius=max(2, round(w * 0.04)), fill=(43, 24, 74, round(235 * progress)))
	result = _composite(result, layer)
	for box, direction in ((left_box, -1), (right_box, 1)):
		panel = base.crop(box)
		new_width = max(2, round(panel.width * (1.0 - progress * 0.70)))
		panel = panel.resize((new_width, panel.height), Image.Resampling.BICUBIC)
		x_pos = box[0] if direction < 0 else box[2] - new_width
		result.alpha_composite(panel, (x_pos, box[1]))
	return result


def _animate_oven(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	progress = (0.0, 0.22, 0.50, 0.82, 1.0, 0.72, 0.30, 0.0)[frame]
	result = base.copy()
	door_box = (round(w * 0.12), round(h * 0.42), round(w * 0.88), round(h * 0.91))
	layer, draw = _overlay(base)
	draw.rounded_rectangle(door_box, radius=max(2, round(h * 0.05)),
		fill=(61, 26, 43, round(245 * progress)))
	if progress:
		for index in range(3):
			x = round(w * (0.34 + index * 0.15))
			y = round(h * (0.67 - 0.08 * math.sin(frame + index)))
			draw.polygon(((x, y + 13), (x - 6, y + 3), (x, y - 10), (x + 7, y + 3)),
				fill=(255, 144 + index * 24, 38, round(230 * progress)))
	result = _composite(result, layer)
	panel = base.crop(door_box)
	panel_h = max(2, round(panel.height * (1.0 - progress * 0.62)))
	panel = panel.resize((panel.width, panel_h), Image.Resampling.BICUBIC)
	result.alpha_composite(panel, (door_box[0], door_box[3] - panel_h))
	return result


def _animate_fridge(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	progress = (0.0, 0.14, 0.38, 0.68, 1.0, 0.70, 0.32, 0.0)[frame]
	result = base.copy()
	door_box = (round(w * 0.09), round(h * 0.04), round(w * 0.94), round(h * 0.97))
	layer, draw = _overlay(base)
	draw.rounded_rectangle(door_box, radius=max(2, round(w * 0.10)),
		fill=(39, 104, 108, round(250 * progress)))
	if progress:
		for shelf in (0.34, 0.55, 0.75):
			y = round(h * shelf)
			draw.line((round(w * 0.21), y, round(w * 0.78), y),
				fill=(209, 248, 232, round(235 * progress)), width=max(1, round(w * 0.018)))
	result = _composite(result, layer)
	door = base.crop(door_box)
	new_width = max(3, round(door.width * (1.0 - progress * 0.72)))
	door = door.resize((new_width, door.height), Image.Resampling.BICUBIC)
	result.alpha_composite(door, (door_box[2] - new_width, door_box[1]))
	return result


def _animate_book(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	progress = (0.0, 0.22, 0.55, 0.90, 1.0, 0.75, 0.35, 0.0)[frame]
	layer, draw = _overlay(base)
	cx, cy = round(w * 0.53), round(h * 0.43)
	span = round(w * (0.10 + 0.24 * progress))
	height = round(h * (0.08 + 0.12 * progress))
	page = (255, 238, 198, round(245 * progress))
	draw.polygon(((cx, cy), (cx - span, cy - height // 2),
		(cx - span, cy + height // 2), (cx, cy + round(height * 0.35))), fill=page)
	draw.polygon(((cx, cy), (cx + span, cy - height // 2),
		(cx + span, cy + height // 2), (cx, cy + round(height * 0.35))), fill=page)
	draw.line((cx, cy, cx, cy + round(height * 0.38)),
		fill=(178, 112, 125, round(255 * progress)), width=max(1, round(w * 0.012)))
	if 2 <= frame <= 5:
		flip = round(span * (0.8 - abs(3.5 - frame) * 0.18))
		draw.arc((cx - flip, cy - height, cx + flip, cy + height), 200, 335,
			fill=(255, 251, 222, 230), width=max(1, round(w * 0.018)))
	return _composite(base, layer)


def _animate_pearl(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	return _draw_glow(base, frame, [(0.51, 0.25), (0.51, 0.38)])


def _animate_tent(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	progress = (0.0, 0.18, 0.44, 0.78, 1.0, 0.72, 0.30, 0.0)[frame]
	layer, draw = _overlay(base)
	cx = round(w * 0.51)
	draw.polygon(((cx, round(h * 0.34)),
		(round(w * (0.34 + 0.15 * progress)), round(h * 0.91)),
		(round(w * (0.67 - 0.15 * progress)), round(h * 0.91))),
		fill=(50, 30, 75, round(225 * progress)))
	return _composite(base, layer)


def _animate_friends(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	friend = frame % 5
	x = round(w * (0.25 + friend * 0.125))
	y = round(h * (0.64 - (friend % 2) * 0.07))
	r = max(3, round(min(w, h) * 0.055))
	draw.arc((x - r, y - r * 2, x + r * 2, y + r), 190, 335,
		fill=(255, 239, 154, 245), width=max(2, r // 3))
	if frame in (2, 4, 6):
		draw.ellipse((x - r, y - r, x + r, y + r),
			outline=(255, 173, 211, 225), width=max(1, r // 3))
	return _composite(base, layer)


def _animate_rings(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	result = base.copy()
	band_h = max(3, round(h * 0.10))
	for ring in range(3):
		y = round(h * (0.54 + ring * 0.105))
		box = (round(w * 0.17), y, round(w * 0.82), min(h, y + band_h))
		part = base.crop(box)
		lift_phase = max(0.0, 1.0 - abs(frame - (ring + 2)) / 2.0)
		lift = round(h * 0.16 * lift_phase)
		if lift:
			result.paste((0, 0, 0, 0), box)
			result.alpha_composite(part, (box[0], box[1] - lift))
	return result


def _animate_blocks(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	result = base.copy()
	regions = (
		(round(w * 0.05), round(h * 0.37), round(w * 0.38), round(h * 0.79)),
		(round(w * 0.33), round(h * 0.42), round(w * 0.66), round(h * 0.84)),
		(round(w * 0.54), round(h * 0.14), round(w * 0.87), round(h * 0.57)),
	)
	progress = (0.0, 0.18, 0.48, 0.82, 1.0, 0.65, 0.28, 0.0)[frame]
	for index, box in enumerate(regions):
		part = base.crop(box)
		angle = (index - 1) * 18 * progress
		part = part.rotate(angle, Image.Resampling.BICUBIC, expand=False)
		result.paste((0, 0, 0, 0), box)
		offset = round(w * (index - 1) * 0.07 * progress)
		result.alpha_composite(part, (box[0] + offset, box[1] + round(h * 0.08 * progress)))
	return result


def _animate_notes(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	result = base.copy()
	centers = ((0.37, 0.45), (0.50, 0.39), (0.63, 0.48))
	index = frame % len(centers)
	cx, cy = centers[index]
	box = (round((cx - 0.075) * w), round((cy - 0.13) * h),
		round((cx + 0.075) * w), round((cy + 0.13) * h))
	note = base.crop(box)
	angle = (-10, -5, 8, 12, 7, -4, -8, 0)[frame]
	note = note.rotate(angle, Image.Resampling.BICUBIC, expand=False)
	result.alpha_composite(note, box[:2])
	return result


def _animate_paint(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	colors = ((246, 91, 142, 230), (84, 211, 220, 230), (255, 200, 69, 230))
	for index, color in enumerate(colors):
		angle = frame * 0.8 + index * 2.1
		x = round(w * (0.42 + math.cos(angle) * 0.12))
		y = round(h * (0.58 + math.sin(angle) * 0.08))
		r = max(2, round(min(w, h) * 0.025))
		draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
	brush_x = round(w * (0.30 + frame / 7.0 * 0.45))
	draw.line((brush_x, round(h * 0.28), round(w * 0.52), round(h * 0.62)),
		fill=(119, 72, 48, 245), width=max(2, round(w * 0.018)))
	return _composite(base, layer)


def _animate_ribbon(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	progress = (0.0, 0.22, 0.48, 0.76, 1.0, 0.72, 0.34, 0.0)[frame]
	points = []
	for step in range(9):
		x = w * (0.56 + step * 0.045 * progress)
		y = h * (0.50 + math.sin(step * 1.2 + frame * 0.5) * 0.08 * progress)
		points.append((round(x), round(y)))
	if len(points) > 1:
		draw.line(points, fill=(244, 101, 177, 235), width=max(2, round(h * 0.04)))
	return _composite(base, layer)


def _animate_flower(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	open_amount = (0.2, 0.42, 0.70, 0.95, 1.0, 0.75, 0.42, 0.2)[frame]
	cx, cy = round(w * 0.52), round(h * 0.56)
	for petal in range(6):
		angle = math.tau * petal / 6.0
		distance = min(w, h) * 0.13 * open_amount
		x = cx + math.cos(angle) * distance
		y = cy + math.sin(angle) * distance * 0.55
		rx = max(2, round(min(w, h) * 0.08 * open_amount))
		ry = max(2, round(rx * 0.55))
		draw.ellipse((round(x - rx), round(y - ry), round(x + rx), round(y + ry)),
			fill=(255, 139, 194, 110))
	draw.arc((round(w * 0.12), round(h * 0.62), round(w * 0.89), round(h * 0.96)),
		0, 180, fill=(155, 243, 255, 210), width=max(1, round(h * 0.025)))
	return _composite(base, layer)


def _animate_float(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	layer, draw = _overlay(base)
	radius = (0.12, 0.20, 0.28, 0.36, 0.42, 0.34, 0.24, 0.12)[frame]
	cx, cy = round(w * 0.50), round(h * 0.72)
	draw.ellipse((round(cx - w * radius), round(cy - h * radius * 0.28),
		round(cx + w * radius), round(cy + h * radius * 0.28)),
		outline=(160, 245, 255, 210), width=max(1, round(min(w, h) * 0.035)))
	return _composite(base, layer)


def _animate_bathtub(base: Image.Image, frame: int) -> Image.Image:
	result = _animate_water(base, frame)
	w, h = base.size
	layer, draw = _overlay(base)
	for index in range(4):
		x = round(w * (0.20 + index * 0.17 + 0.02 * math.sin(frame + index)))
		y = round(h * (0.38 - ((frame / 8.0 + index * 0.21) % 1.0) * 0.18))
		r = max(2, round(h * (0.025 + (index % 2) * 0.012)))
		draw.ellipse((x - r, y - r, x + r, y + r),
			outline=(221, 253, 255, 225), width=max(1, r // 3))
	return _composite(result, layer)


def _animate_duck(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	result = base.copy()
	progress = (0.0, 0.22, 0.45, 0.75, 1.0, 0.62, 0.25, 0.0)[frame]
	if progress:
		bbox = base.getchannel("A").getbbox()
		if bbox:
			part = base.crop(bbox)
			scale_y = max(0.62, 1.0 - progress * 0.26)
			part = part.resize((part.width, max(1, round(part.height * scale_y))),
				Image.Resampling.BICUBIC)
			result.paste((0, 0, 0, 0), bbox)
			result.alpha_composite(part, (bbox[0], bbox[3] - part.height + round(h * 0.05 * progress)))
	layer, draw = _overlay(base)
	draw.arc((round(w * 0.05), round(h * 0.58), round(w * 0.95), round(h * 0.92)),
		0, 180, fill=(154, 244, 255, round(220 * progress)), width=max(1, round(h * 0.035)))
	return _composite(result, layer)


def _animate_toilet(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	result = base.copy()
	layer, draw = _overlay(base)
	seat = (0.0, 0.35, 0.75, 1.0, 0.62, 0.28, 0.08, 0.0)[frame]
	cx, cy = round(w * 0.46), round(h * 0.51)
	rx = round(w * 0.25)
	ry = round(h * (0.055 + seat * 0.17))
	draw.ellipse((cx - rx, cy - ry - round(h * 0.13 * seat),
		cx + rx, cy + ry - round(h * 0.13 * seat)),
		outline=(255, 220, 181, round(245 * seat)), width=max(2, round(w * 0.035)))
	if frame >= 3:
		for arc_index in range(3):
			inset = arc_index * max(2, round(w * 0.035))
			draw.arc((cx - rx + inset, round(h * 0.48) + inset,
				cx + rx - inset, round(h * 0.67) - inset),
				frame * 32 + arc_index * 70, frame * 32 + 210 + arc_index * 70,
				fill=(113, 224, 242, 220), width=max(1, round(w * 0.018)))
	return _composite(result, layer)


def _animate_tapestry(base: Image.Image, frame: int) -> Image.Image:
	w, h = base.size
	cut_y = round(h * 0.18)
	result = base.copy()
	cloth = base.crop((0, cut_y, w, h))
	array = np.asarray(cloth)
	warped = np.zeros_like(array)
	for y_pos in range(cloth.height):
		shift = round(math.sin(frame * 0.72 + y_pos / max(1, cloth.height) * math.pi * 1.5) * 4)
		warped[y_pos] = np.roll(array[y_pos], shift, axis=0)
	result.paste((0, 0, 0, 0), (0, cut_y, w, h))
	result.alpha_composite(Image.fromarray(warped, mode="RGBA"), (0, cut_y))
	return result


def _frames(spec: Spec, base: Image.Image) -> list[Image.Image]:
	mode = spec.mode
	result: list[Image.Image] = []
	for frame in range(FRAME_COUNT):
		if mode == "lights":
			image = _animate_lights(base, frame)
		elif mode == "faucet":
			image = _animate_faucet(base, frame)
		elif mode == "water":
			image = _animate_water(base, frame)
		elif mode == "pan":
			image = _animate_pan(base, frame)
		elif mode == "curtains":
			image = _animate_curtains(base, frame)
		elif mode == "oven":
			image = _animate_oven(base, frame)
		elif mode == "fridge":
			image = _animate_fridge(base, frame)
		elif mode == "book":
			image = _animate_book(base, frame)
		elif mode == "pearl":
			image = _animate_pearl(base, frame)
		elif mode == "tent":
			image = _animate_tent(base, frame)
		elif mode == "friends":
			image = _animate_friends(base, frame)
		elif mode == "rings":
			image = _animate_rings(base, frame)
		elif mode == "blocks":
			image = _animate_blocks(base, frame)
		elif mode == "notes":
			image = _animate_notes(base, frame)
		elif mode == "paint":
			image = _animate_paint(base, frame)
		elif mode == "ribbon":
			image = _animate_ribbon(base, frame)
		elif mode == "flower":
			image = _animate_flower(base, frame)
		elif mode == "float":
			image = _animate_float(base, frame)
		elif mode == "bathtub":
			image = _animate_bathtub(base, frame)
		elif mode == "duck":
			image = _animate_duck(base, frame)
		elif mode == "toilet":
			image = _animate_toilet(base, frame)
		elif mode == "tapestry":
			image = _animate_tapestry(base, frame)
		else:
			raise ValueError(f"unknown animation mode: {mode}")
		result.append(_transparent_rgb(image))
	return result


def _grid(size: tuple[int, int]) -> tuple[int, int]:
	w, h = size
	preferred = ((4, 2), (3, 3), (2, 4), (1, 8))
	for columns, rows in preferred:
		if w * columns <= MAX_TEXTURE_EDGE and h * rows <= MAX_TEXTURE_EDGE:
			return columns, rows
	raise ValueError(f"no <=1024 atlas grid fits {size}")


def _build_atlas(frames: list[Image.Image]) -> tuple[Image.Image, int, int]:
	columns, rows = _grid(frames[0].size)
	atlas = Image.new("RGBA", (frames[0].width * columns, frames[0].height * rows))
	for index, frame in enumerate(frames):
		atlas.alpha_composite(frame,
			((index % columns) * frame.width, (index // columns) * frame.height))
	return atlas, columns, rows


def _frame_hashes(frames: list[Image.Image]) -> list[str]:
	return [hashlib.sha256(frame.tobytes()).hexdigest() for frame in frames]


def _contact_sheet(previews: list[tuple[Spec, list[Image.Image]]]) -> Image.Image:
	# Every delivered frame must be visible in the review artifact.  The earlier
	# even-frame-only sheet could conceal a bad intermediate cutout.
	columns = FRAME_COUNT
	cell_w = 160
	cell_h = 144
	rows = len(previews)
	canvas = Image.new("RGB", (columns * cell_w, rows * cell_h), (247, 244, 252))
	draw = ImageDraw.Draw(canvas)
	for row, (spec, frames) in enumerate(previews):
		for column, frame_index in enumerate(range(FRAME_COUNT)):
			frame = frames[frame_index]
			checker = Image.new("RGB", (cell_w - 8, cell_h - 28), (236, 232, 246))
			checker_draw = ImageDraw.Draw(checker)
			for y in range(0, checker.height, 12):
				for x in range(0, checker.width, 12):
					if (x // 12 + y // 12) % 2:
						checker_draw.rectangle((x, y, x + 11, y + 11), fill=(219, 213, 237))
			scale = min(checker.width / frame.width, checker.height / frame.height, 1.6)
			thumb = frame.resize((max(1, round(frame.width * scale)),
				max(1, round(frame.height * scale))), Image.Resampling.LANCZOS)
			checker.paste(thumb, ((checker.width - thumb.width) // 2,
				(checker.height - thumb.height) // 2), thumb)
			x_pos = column * cell_w + 4
			y_pos = row * cell_h + 24
			canvas.paste(checker, (x_pos, y_pos))
			draw.text((x_pos + 2, row * cell_h + 6),
				f"{spec.room}/{spec.item} f{frame_index}", fill=(38, 31, 91))
	return canvas


def main() -> None:
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	AUDIT_DIR.mkdir(parents=True, exist_ok=True)
	crops = _depth_crops()
	audio_manifest = json.loads(AUDIO_MANIFEST_PATH.read_text(encoding="utf-8"))
	audio_by_path = {
		str(record["path"]): record
		for record in audio_manifest.get("files", [])
		if isinstance(record, dict) and isinstance(record.get("path"), str)
	}
	assets: list[dict[str, object]] = []
	room_instances: dict[str, list[dict[str, object]]] = {}
	previews: list[tuple[Spec, list[Image.Image]]] = []
	for spec in SPECS:
		source_path = _source_path(spec)
		sound_path = "assets/audio/" + spec.sound
		audio_record = audio_by_path.get(sound_path)
		if audio_record is None:
			raise ValueError(f"missing synthesized-audio manifest record for {sound_path}")
		sound_duration = float(audio_record["duration_ms"]) / 1000.0
		animation_duration = spec.duration * FRAME_COUNT
		if spec.sound_frame != 0 or abs(animation_duration - sound_duration) > 0.002:
			raise ValueError(
				f"{spec.asset_id} timeline mismatch: frame={spec.sound_frame}, "
				f"animation={animation_duration:.4f}s, sound={sound_duration:.4f}s")
		base = _transparent_rgb(_room_base(spec, crops))
		frames = _frames(spec, base)
		atlas, columns, rows = _build_atlas(frames)
		atlas_path = OUTPUT_DIR / f"{spec.asset_id}_atlas.png"
		atlas.save(atlas_path, optimize=True)
		frame_hashes = _frame_hashes(frames)
		alpha = np.asarray(base.getchannel("A"))
		border_clear = bool(
			(np.max(alpha[0]) == 0) and (np.max(alpha[-1]) == 0)
			and (np.max(alpha[:, 0]) == 0) and (np.max(alpha[:, -1]) == 0)
		)
		asset_record: dict[str, object] = {
			"id": spec.asset_id,
			"room": spec.room,
			"item_id": spec.item,
			"instances": list(spec.instance_ids),
			"semantic_action": spec.action,
			"source": source_path.relative_to(ROOT).as_posix(),
			"source_sha256": _sha256(source_path),
			"atlas": atlas_path.relative_to(ROOT).as_posix(),
			"atlas_sha256": _sha256(atlas_path),
			"cell_size": [base.width, base.height],
			"hframes": columns,
			"vframes": rows,
			"frame_count": FRAME_COUNT,
			"frame_duration_seconds": spec.duration,
			"animation_duration_seconds": animation_duration,
			"frame_sha256": frame_hashes,
			"unique_frame_count": len(set(frame_hashes)),
			"sound": sound_path,
			"sound_duration_seconds": sound_duration,
			"sound_frame": spec.sound_frame,
			"timeline_sync": TIMELINE_SYNC,
			"fixed_pivot": True,
			"root_transform_animation": False,
			"transparent_border": border_clear,
			"rest_alpha_bbox": list(base.getchannel("A").getbbox() or (0, 0, 0, 0)),
			"normalized_use_review": NORMALIZED_USE_REVIEW,
			"reviewed_frame_indices": list(range(FRAME_COUNT)),
		}
		if source_path.parent == ROOM_DIR:
			source_alpha = np.asarray(
				Image.open(source_path).convert("RGBA").getchannel("A")) >= 128
			rest_alpha = alpha >= 128
			source_depth_pixels = int(np.count_nonzero(source_alpha))
			rest_depth_pixels = int(np.count_nonzero(rest_alpha))
			overlap_pixels = int(np.count_nonzero(source_alpha & rest_alpha))
			asset_record.update({
				"source_depth_pixels": source_depth_pixels,
				"rest_depth_pixels": rest_depth_pixels,
				"silhouette_retention": overlap_pixels / max(1, source_depth_pixels),
			})
		assets.append(asset_record)
		for instance_id in spec.instance_ids:
			room_instances.setdefault(spec.room, []).append({
				"id": instance_id,
				"asset_id": spec.asset_id,
				"semantic_action": spec.action,
			})
		previews.append((spec, frames))

	counts = {room: len(instances) for room, instances in sorted(room_instances.items())}
	physical_count = sum(counts.values())
	contact = _contact_sheet(previews)
	contact.save(CONTACT_PATH, optimize=True)
	manifest = {
		"schema_version": 1,
		"generated_on": str(date.today()),
		"generator": "tools/build_castle_interaction_atlases.py",
		"frame_contract": {"minimum": 4, "maximum": 12, "delivered": FRAME_COUNT},
		"visual_review_evidence": {
			"path": CONTACT_PATH.relative_to(ROOT).as_posix(),
			"sha256": _sha256(CONTACT_PATH),
			"reviewed_frame_indices": list(range(FRAME_COUNT)),
			"dimensions": list(contact.size),
		},
		"rooms": {
			room: {"physical_item_count": counts[room], "instances": room_instances[room]}
			for room in sorted(room_instances)
		},
		"assets": assets,
		"summary": {
			"room_count": len(counts),
			"unique_animated_assets": len(assets),
			"physical_item_instances": physical_count,
			"average_items_per_room": round(physical_count / len(counts), 3),
			"minimum_non_hall_room_items": min(
				count for room, count in counts.items() if room != "main_hall"),
			"character_overlap_gate": "transparent pixels never write prop-card depth",
		},
	}
	MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(f"built {len(assets)} atlases / {physical_count} instances")
	print(f"average items per room: {physical_count / len(counts):.2f}")
	print(MANIFEST_PATH.relative_to(ROOT))
	print(CONTACT_PATH.relative_to(ROOT))


if __name__ == "__main__":
	main()
