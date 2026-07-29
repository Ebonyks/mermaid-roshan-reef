#!/usr/bin/env python3
"""Build the seam-safe Sky Lagoon 6x2 grid from overscanned native edits.

The 2172x724 panorama is composition reference only.  Each 362x362 logical
cell is supplied to image generation with 41 pixels of context on every side,
yielding a 444x444 reference crop.  The service returns a 1254px square; all
twelve raw squares are then laid onto one 6144x2048 canvas with their native
overscan feathered together.  No generated square is enlarged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src/sky_lagoon/reductive_rebuild_2026-07-28"
REFERENCE = SOURCE_DIR / "snow_mountain_cabins_offroad_edit_raw.png"
PLATE = SOURCE_DIR / "sky_lagoon_reductive_reference_plate_3x1.png"
OBJECT_EDIT_DIR = SOURCE_DIR / "object_removals"
GRID_REF_DIR = SOURCE_DIR / "grid_references"
GRID_RAW_DIR = SOURCE_DIR / "grid_raw"
MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
TILE_DIR = ROOT / "assets/flats/sky_lagoon/main"
REPORT = ROOT / "audit/sky_lagoon_reductive_grid.json"
SEAM_CAPTURE = ROOT / "audit/sky_lagoon_reductive_seams.jpg"
CASTLE_CARD_RAW = SOURCE_DIR / "castle_depth_card_transparent_raw.png"
CASTLE_CARD = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png"
)
OWNER_STAINED_GLASS = SOURCE_DIR / "stained_glass_owner_reference.png"
STAINED_GLASS_AUDIT = ROOT / "audit/sky_lagoon_stained_glass_replacement.json"

SOURCE_TILE = 362
SOURCE_OVERSCAN = 41
SOURCE_CROP = SOURCE_TILE + SOURCE_OVERSCAN * 2
RAW_SIZE = 1254
TILE_SIZE = 1024
GRID_COLUMNS = 6
GRID_ROWS = 2
RAW_OVERSCAN = (RAW_SIZE - TILE_SIZE) // 2

# Local square edits.  The generated output is only allowed to replace the
# interior window; the outer feather returns byte-for-byte to the approved
# reference so a local removal cannot soften the panorama.
OBJECT_CROPS = {
	"central_tree_grove_removed": {
		"box": (330, 0, 774, 444),
		"interior": (24, 12, 432, 436),
	},
	"castle_tree_removed": {
		"box": (1220, 0, 1664, 444),
		"interior": (24, 12, 432, 436),
	},
	"castle_removed": {
		"box": (1528, 0, 2172, 644),
		"interior": (28, 18, 636, 632),
	},
}


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _fit_square(image: Image.Image, size: int) -> Image.Image:
	return image.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)


def _feathered_rectangle(
	size: tuple[int, int],
	box: tuple[int, int, int, int],
	feather: int = 64,
) -> Image.Image:
	mask = Image.new("L", size, 0)
	draw = ImageDraw.Draw(mask)
	draw.rectangle(box, fill=255)
	return mask.filter(ImageFilter.GaussianBlur(feather))


def make_object_references() -> None:
	OBJECT_EDIT_DIR.mkdir(parents=True, exist_ok=True)
	with Image.open(REFERENCE) as source:
		source = source.convert("RGB")
		for name, spec in OBJECT_CROPS.items():
			source.crop(spec["box"]).save(
				OBJECT_EDIT_DIR / f"{name}_reference.png", optimize=True
			)


def assemble_reference_plate() -> None:
	with Image.open(REFERENCE) as source:
		plate = source.convert("RGB")
	for name, spec in OBJECT_CROPS.items():
		raw_path = OBJECT_EDIT_DIR / f"{name}_raw.png"
		if not raw_path.exists():
			raise FileNotFoundError(raw_path)
		box = spec["box"]
		width = box[2] - box[0]
		height = box[3] - box[1]
		with Image.open(raw_path) as raw:
			replacement = raw.convert("RGB").resize(
				(width, height), Image.Resampling.LANCZOS
			)
		original = plate.crop(box)
		diff = ImageChops.difference(replacement, original).convert("L")
		# Select the authored object-removal change rather than fading an
		# entire generated rectangle over the sharp source.  Expansion closes
		# the tree/castle silhouettes; the small feather hides antialiased
		# edges without creating a translucent duplicate.
		change_mask = diff.point(lambda value: 255 if value >= 24 else 0)
		change_mask = change_mask.filter(ImageFilter.MaxFilter(19))
		change_mask = change_mask.filter(ImageFilter.GaussianBlur(5.0))
		bounds_mask = _feathered_rectangle(
			(width, height), spec["interior"], feather=18
		)
		mask = ImageChops.multiply(change_mask, bounds_mask)
		plate.paste(Image.composite(replacement, original, mask), (box[0], box[1]))
	plate.save(PLATE, optimize=True)


def _padded_crop(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
	left = max(0, box[0])
	top = max(0, box[1])
	right = min(image.width, box[2])
	bottom = min(image.height, box[3])
	crop = image.crop((left, top, right, bottom))
	padded = Image.new("RGB", (box[2] - box[0], box[3] - box[1]))
	padded.paste(crop, (left - box[0], top - box[1]))
	if left > box[0]:
		width = left - box[0]
		edge = crop.crop((0, 0, width, crop.height)).transpose(
			Image.Transpose.FLIP_LEFT_RIGHT
		)
		padded.paste(edge, (0, top - box[1]))
	if right < box[2]:
		width = box[2] - right
		edge = crop.crop(
			(crop.width - width, 0, crop.width, crop.height)
		).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
		padded.paste(edge, (right - box[0], top - box[1]))
	if top > box[1]:
		height = top - box[1]
		edge = padded.crop(
			(0, height, padded.width, height * 2)
		).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
		padded.paste(edge, (0, 0))
	if bottom < box[3]:
		height = box[3] - bottom
		start = bottom - box[1]
		edge = padded.crop(
			(0, start - height, padded.width, start)
		).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
		padded.paste(edge, (0, start))
	return padded


def make_grid_references() -> None:
	GRID_REF_DIR.mkdir(parents=True, exist_ok=True)
	with Image.open(PLATE) as source:
		source = source.convert("RGB")
		for row in range(GRID_ROWS):
			for column in range(GRID_COLUMNS):
				box = (
					column * SOURCE_TILE - SOURCE_OVERSCAN,
					row * SOURCE_TILE - SOURCE_OVERSCAN,
					(column + 1) * SOURCE_TILE + SOURCE_OVERSCAN,
					(row + 1) * SOURCE_TILE + SOURCE_OVERSCAN,
				)
				crop = _padded_crop(source, box)
				if crop.size != (SOURCE_CROP, SOURCE_CROP):
					raise RuntimeError(f"bad reference crop {row},{column}: {crop.size}")
				crop.save(
					GRID_REF_DIR / f"tile_r{row}_c{column}_reference.png",
					optimize=True,
				)


def _raw_mask() -> Image.Image:
	mask = Image.new("L", (RAW_SIZE, RAW_SIZE), 255)
	pixels = mask.load()
	for y in range(RAW_SIZE):
		for x in range(RAW_SIZE):
			edge = min(x, y, RAW_SIZE - 1 - x, RAW_SIZE - 1 - y)
			if edge >= RAW_OVERSCAN:
				value = 255
			else:
				t = edge / max(1.0, float(RAW_OVERSCAN))
				value = round(255.0 * t * t * (3.0 - 2.0 * t))
			pixels[x, y] = value
	return mask.filter(ImageFilter.GaussianBlur(1.0))


def assemble_grid() -> None:
	accum = Image.new("RGBA", (TILE_SIZE * GRID_COLUMNS, TILE_SIZE * GRID_ROWS))
	mask = _raw_mask()
	for row in range(GRID_ROWS):
		for column in range(GRID_COLUMNS):
			path = GRID_RAW_DIR / f"tile_r{row}_c{column}_raw.png"
			if not path.exists():
				raise FileNotFoundError(path)
			with Image.open(path) as source:
				raw = _fit_square(source, RAW_SIZE).convert("RGBA")
			raw.putalpha(mask)
			accum.alpha_composite(
				raw,
				(
					column * TILE_SIZE - RAW_OVERSCAN,
					row * TILE_SIZE - RAW_OVERSCAN,
				),
			)
	master = Image.new("RGB", accum.size, (96, 204, 228))
	master.paste(accum.convert("RGB"), mask=accum.getchannel("A"))
	MASTER.parent.mkdir(parents=True, exist_ok=True)
	master.save(MASTER, optimize=True)
	TILE_DIR.mkdir(parents=True, exist_ok=True)
	for row in range(GRID_ROWS):
		for column in range(GRID_COLUMNS):
			tile = master.crop(
				(
					column * TILE_SIZE,
					row * TILE_SIZE,
					(column + 1) * TILE_SIZE,
					(row + 1) * TILE_SIZE,
				)
			)
			tile.save(
				TILE_DIR
				/ f"flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{column}.png",
				optimize=True,
			)
	_write_audit(master)


def prepare_depth_cards() -> None:
	"""Install audited generated cutouts without exceeding the mobile limit."""
	if not CASTLE_CARD_RAW.exists():
		raise FileNotFoundError(CASTLE_CARD_RAW)
	with Image.open(CASTLE_CARD_RAW) as source:
		card = source.convert("RGBA")
		alpha_box = card.getchannel("A").getbbox()
		if alpha_box is None:
			raise RuntimeError("castle depth card has no visible pixels")
		# Retain a small transparent gutter so bilinear sampling never touches
		# the opposite edge of the cutout.
		gutter = 10
		box = (
			max(0, alpha_box[0] - gutter),
			max(0, alpha_box[1] - gutter),
			min(card.width, alpha_box[2] + gutter),
			min(card.height, alpha_box[3] + gutter),
		)
		card = card.crop(box)
		scale = min(1.0, 1024.0 / float(max(card.size)))
		if scale < 1.0:
			card = card.resize(
				(
					max(1, round(card.width * scale)),
					max(1, round(card.height * scale)),
				),
				Image.Resampling.LANCZOS,
			)
		CASTLE_CARD.parent.mkdir(parents=True, exist_ok=True)
		card.save(CASTLE_CARD, optimize=True)


def replace_stained_glass() -> None:
	"""Replace only the castle window contents with the owner-supplied panel."""
	if not CASTLE_CARD.exists():
		raise FileNotFoundError(CASTLE_CARD)
	if not OWNER_STAINED_GLASS.exists():
		raise FileNotFoundError(OWNER_STAINED_GLASS)
	with Image.open(CASTLE_CARD) as castle_source:
		before = castle_source.convert("RGBA")
	with Image.open(OWNER_STAINED_GLASS) as glass_source:
		# Exact outer bounds of the pointed black window in the supplied image.
		glass = glass_source.convert("RGB").crop((101, 8, 780, 1176))
	target_box = (431, 214, 622, 506)
	glass = glass.resize(
		(target_box[2] - target_box[0], target_box[3] - target_box[1]),
		Image.Resampling.LANCZOS,
	)
	mask = Image.new("L", before.size, 0)
	draw = ImageDraw.Draw(mask)
	# This mask stays inside the castle's existing gold frame. The outer
	# castle, frame, towers, door, and bridge remain byte-for-byte unchanged.
	draw.polygon(
		[
			(526, 214),
			(571, 228),
			(603, 260),
			(622, 300),
			(622, 506),
			(431, 506),
			(431, 300),
			(449, 260),
			(480, 228),
		],
		fill=255,
	)
	mask = mask.filter(ImageFilter.GaussianBlur(0.45))
	after = before.copy()
	layer = Image.new("RGBA", before.size)
	layer.paste(glass.convert("RGBA"), (target_box[0], target_box[1]))
	after.paste(layer, (0, 0), mask)
	diff_box = ImageChops.difference(before, after).getbbox()
	allowed_box = (427, 210, 626, 510)
	if diff_box is None:
		raise RuntimeError("stained-glass replacement made no visible change")
	if (
		diff_box[0] < allowed_box[0]
		or diff_box[1] < allowed_box[1]
		or diff_box[2] > allowed_box[2]
		or diff_box[3] > allowed_box[3]
	):
		raise RuntimeError(
			f"stained-glass replacement escaped the window: {diff_box}"
		)
	after.save(CASTLE_CARD, optimize=True)
	STAINED_GLASS_AUDIT.parent.mkdir(parents=True, exist_ok=True)
	STAINED_GLASS_AUDIT.write_text(
		json.dumps(
			{
				"castle_card": CASTLE_CARD.relative_to(ROOT).as_posix(),
				"owner_reference": OWNER_STAINED_GLASS.relative_to(ROOT).as_posix(),
				"owner_reference_sha256": _sha256(OWNER_STAINED_GLASS),
				"replacement_bounds": list(diff_box),
				"allowed_bounds": list(allowed_box),
				"outside_window_changed_pixels": 0,
			},
			indent=2,
		)
		+ "\n",
		encoding="utf-8",
	)


def _difference(left: Image.Image, right: Image.Image) -> float:
	diff = ImageChops.difference(left.convert("RGB"), right.convert("RGB"))
	histogram = diff.histogram()
	total = sum(value * (index % 256) for index, value in enumerate(histogram))
	return total / (left.width * left.height * 3.0 * 255.0)


def _write_audit(master: Image.Image) -> None:
	seams: list[dict[str, float | int | str | bool]] = []
	for x in range(TILE_SIZE, master.width, TILE_SIZE):
		jump = _difference(
			master.crop((x - 1, 0, x, master.height)),
			master.crop((x, 0, x + 1, master.height)),
		)
		near = max(
			1e-9,
			(
				_difference(
					master.crop((x - 2, 0, x - 1, master.height)),
					master.crop((x - 1, 0, x, master.height)),
				)
				+ _difference(
					master.crop((x, 0, x + 1, master.height)),
					master.crop((x + 1, 0, x + 2, master.height)),
				)
			)
			* 0.5,
		)
		seams.append({
			"axis": "vertical",
			"pixel": x,
			"jump": jump,
			"near_jump": near,
			"ratio": jump / near,
			"pass": jump / near <= 1.75,
		})
	for y in range(TILE_SIZE, master.height, TILE_SIZE):
		jump = _difference(
			master.crop((0, y - 1, master.width, y)),
			master.crop((0, y, master.width, y + 1)),
		)
		near = max(
			1e-9,
			(
				_difference(
					master.crop((0, y - 2, master.width, y - 1)),
					master.crop((0, y - 1, master.width, y)),
				)
				+ _difference(
					master.crop((0, y, master.width, y + 1)),
					master.crop((0, y + 1, master.width, y + 2)),
				)
			)
			* 0.5,
		)
		seams.append({
			"axis": "horizontal",
			"pixel": y,
			"jump": jump,
			"near_jump": near,
			"ratio": jump / near,
			"pass": jump / near <= 1.75,
		})
	capture = Image.new("RGB", (960, 560), "white")
	for index, x in enumerate(range(TILE_SIZE, master.width, TILE_SIZE)):
		strip = master.crop((x - 64, 0, x + 64, master.height)).resize(
			(128, 420), Image.Resampling.LANCZOS
		)
		capture.paste(strip, (32 + index * 176, 24))
	horizontal = master.crop(
		(0, TILE_SIZE - 64, master.width, TILE_SIZE + 64)
	).resize((960, 96), Image.Resampling.LANCZOS)
	capture.paste(horizontal, (0, 464))
	SEAM_CAPTURE.parent.mkdir(parents=True, exist_ok=True)
	capture.save(SEAM_CAPTURE, quality=95, subsampling=0)
	report = {
		"reference": {
			"path": REFERENCE.relative_to(ROOT).as_posix(),
			"size": [2172, 724],
			"usage": "composition_reference_only",
			"sha256": _sha256(REFERENCE),
		},
		"master": {
			"path": MASTER.relative_to(ROOT).as_posix(),
			"size": list(master.size),
			"ratio": master.width / master.height,
			"per_screen_native_coverage": [2048, 2048],
			"sha256": _sha256(MASTER),
		},
		"grid": {
			"columns": GRID_COLUMNS,
			"rows": GRID_ROWS,
			"tile_size": [TILE_SIZE, TILE_SIZE],
			"raw_generated_size": [RAW_SIZE, RAW_SIZE],
			"native_overscan": RAW_OVERSCAN,
		},
		"seams": seams,
		"all_seams_pass": all(bool(seam["pass"]) for seam in seams),
	}
	REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"command",
		choices=(
			"object-references",
			"plate",
			"grid-references",
			"assemble",
			"cards",
			"stained-glass",
		),
	)
	args = parser.parse_args()
	if args.command == "object-references":
		make_object_references()
	elif args.command == "plate":
		assemble_reference_plate()
	elif args.command == "grid-references":
		make_grid_references()
	elif args.command == "assemble":
		assemble_grid()
	elif args.command == "cards":
		prepare_depth_cards()
	else:
		replace_stained_glass()


if __name__ == "__main__":
	main()
