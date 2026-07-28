#!/usr/bin/env python3
"""Prepare the Sky Lagoon shoreline repair and depth-separated tree cards."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/sky_lagoon/tree_card_rebuild_2026-07-28"
OLD_MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v3_hd_3x1.png"
NEW_MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v4_hd_3x1.png"
TILE_DIR = ROOT / "assets/flats/sky_lagoon/main"
SPRITE_DIR = ROOT / "assets/sprites/sky_lagoon"
TILE_SIZE = 1024


def _fit_square(path: Path) -> Image.Image:
	with Image.open(path) as source:
		return source.convert("RGB").resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)


def _preserve_side_seams(
	generated: Image.Image,
	original: Image.Image,
	preserve_left: bool,
	preserve_right: bool,
) -> Image.Image:
	"""Return to approved neighboring tiles over narrow feathered seams."""
	mask = Image.new("L", generated.size, 0)
	if preserve_left:
		for x in range(32):
			value = round(255 * (31 - x) / 31)
			mask.paste(value, (x, 0, x + 1, TILE_SIZE))
	if preserve_right:
		for x in range(TILE_SIZE - 32, TILE_SIZE):
			value = round(255 * (x - (TILE_SIZE - 32)) / 31)
			mask.paste(value, (x, 0, x + 1, TILE_SIZE))
	return Image.composite(original, generated, mask.filter(ImageFilter.GaussianBlur(1.0)))


def _heal_horizontal_seam(top: Image.Image, bottom: Image.Image) -> tuple[Image.Image, Image.Image]:
	"""Bridge the independently regenerated halves without a hard card seam."""
	combined = Image.new("RGB", (TILE_SIZE, TILE_SIZE * 2))
	combined.paste(top, (0, 0))
	combined.paste(bottom, (0, TILE_SIZE))
	upper = combined.crop((0, TILE_SIZE - 40, TILE_SIZE, TILE_SIZE - 8))
	lower = combined.crop((0, TILE_SIZE + 8, TILE_SIZE, TILE_SIZE + 40))
	for offset in range(64):
		t = offset / 63.0
		upper_y = min(31, round(offset * 31 / 63))
		lower_y = min(31, round(offset * 31 / 63))
		row_a = upper.crop((0, upper_y, TILE_SIZE, upper_y + 1))
		row_b = lower.crop((0, lower_y, TILE_SIZE, lower_y + 1))
		row = Image.blend(row_a, row_b, t)
		combined.paste(row, (0, TILE_SIZE - 32 + offset))
	return (
		combined.crop((0, 0, TILE_SIZE, TILE_SIZE)),
		combined.crop((0, TILE_SIZE, TILE_SIZE, TILE_SIZE * 2)),
	)


def _remove_checkerboard(source: Image.Image) -> Image.Image:
	"""Convert the generator preview checker into transparent alpha."""
	rgba = source.convert("RGBA")
	pixels = rgba.load()
	for y in range(rgba.height):
		for x in range(rgba.width):
			r, g, b, _ = pixels[x, y]
			bright = min(r, g, b)
			chroma = max(r, g, b) - bright
			if bright >= 222 and chroma <= 12:
				alpha = max(0, min(255, (222 - bright) * 10 + chroma * 5))
				pixels[x, y] = (r, g, b, alpha)
	return rgba


def _save_card(source: Image.Image, box: tuple[int, int, int, int], name: str) -> None:
	card = _remove_checkerboard(source.crop(box))
	alpha = card.getchannel("A")
	bounds = alpha.getbbox()
	if bounds is None:
		raise RuntimeError(f"No opaque artwork found for {name}")
	card = card.crop(bounds)
	if max(card.size) > 380:
		scale = 380.0 / max(card.size)
		card = card.resize(
			(round(card.width * scale), round(card.height * scale)),
			Image.Resampling.LANCZOS,
		)
	# Cards inherit the mural's soft painted value range; this also avoids
	# scintillating one-pixel highlights on the Speedy mobile tier.
	alpha = card.getchannel("A")
	rgb = ImageEnhance.Contrast(card.convert("RGB")).enhance(0.78)
	rgb = ImageEnhance.Brightness(rgb).enhance(1.16)
	card = rgb.filter(ImageFilter.GaussianBlur(0.45)).convert("RGBA")
	card.putalpha(alpha)
	card.save(SPRITE_DIR / name, optimize=True)


def _prepare_cards() -> None:
	with Image.open(SOURCE / "tree_sticker_family_raw.png") as sheet_source:
		sheet = sheet_source.convert("RGB")
		width = sheet.width
		third = width // 3
		_save_card(sheet, (0, 0, third, sheet.height), "sky_lagoon_tree_sticker_tall_v1.png")
		_save_card(
			sheet,
			(third, 0, third * 2, sheet.height),
			"sky_lagoon_tree_sticker_medium_v1.png",
		)
		_save_card(
			sheet,
			(third * 2, 0, width, sheet.height),
			"sky_lagoon_tree_sticker_slender_v1.png",
		)

	with Image.open(SPRITE_DIR / "sky_lagoon_cloud_family_v7_hd_grade.png") as cloud_source:
		cloud = cloud_source.convert("RGBA")
		alpha = cloud.getchannel("A")
		left = cloud.crop((0, 0, round(cloud.width * 0.31), cloud.height))
		bounds = left.getchannel("A").getbbox()
		if bounds is None:
			raise RuntimeError("Cloud crop has no alpha")
		left.crop(bounds).save(SPRITE_DIR / "sky_lagoon_cloud_single_v1.png", optimize=True)


def _replacement_column(column: int) -> tuple[Image.Image, Image.Image]:
	top = _fit_square(SOURCE / f"tile_r0_c{column}_tree_removed_raw.png")
	bottom = _fit_square(SOURCE / f"tile_r1_c{column}_tree_removed_raw.png")
	with Image.open(
		TILE_DIR / f"flat_sky_lagoon_main_panorama_v3_tile_r0_c{column}.png"
	) as old_top:
		top = _preserve_side_seams(top, old_top.convert("RGB"), column > 0, column < 5)
	with Image.open(
		TILE_DIR / f"flat_sky_lagoon_main_panorama_v3_tile_r1_c{column}.png"
	) as old_bottom:
		bottom = _preserve_side_seams(
			bottom, old_bottom.convert("RGB"), column > 0, column < 5
		)
	return _heal_horizontal_seam(top, bottom)


def _prepare_mural() -> None:
	with Image.open(OLD_MASTER) as old_master_source:
		master = old_master_source.convert("RGB")
	for column in (0, 1, 4):
		top, bottom = _replacement_column(column)
		master.paste(top, (column * TILE_SIZE, 0))
		master.paste(bottom, (column * TILE_SIZE, TILE_SIZE))
	master.save(NEW_MASTER, optimize=True)

	for row in range(2):
		for column in range(6):
			tile = master.crop((
				column * TILE_SIZE,
				row * TILE_SIZE,
				(column + 1) * TILE_SIZE,
				(row + 1) * TILE_SIZE,
			))
			tile.save(
				TILE_DIR / f"flat_sky_lagoon_main_panorama_v4_tile_r{row}_c{column}.png",
				optimize=True,
			)

	with Image.open(OLD_MASTER) as old_master_source:
		old_master = old_master_source.convert("RGB")
	for column in (2, 3, 5):
		box = (
			column * TILE_SIZE,
			0,
			(column + 1) * TILE_SIZE,
			TILE_SIZE * 2,
		)
		if ImageChops.difference(master.crop(box), old_master.crop(box)).getbbox() is not None:
			raise RuntimeError(f"Tree repair changed untouched column {column}")


def main() -> None:
	SPRITE_DIR.mkdir(parents=True, exist_ok=True)
	_prepare_mural()
	_prepare_cards()
	print("SKY_LAGOON_TREE_CARDS|mural=6144x2048|tiles=12|repaired_columns=3|cards=3|clouds=1")


if __name__ == "__main__":
	main()
