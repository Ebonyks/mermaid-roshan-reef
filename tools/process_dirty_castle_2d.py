#!/usr/bin/env python3
"""Build runtime-ready dirty-castle sprites, cinematic frames, and QA sheets."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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
)

FRAMES = (
	("frame_01_arrival_dirty.png", "01_arrival_dirty.png"),
	("frame_02_choose_tools.png", "02_choose_tools.png"),
	("frame_03_roshan_window.png", "03_roshan_window.png"),
	("frame_04_daddy_floor.png", "04_daddy_floor.png"),
	("frame_05_eagle_dust.png", "05_eagle_dust.png"),
	("frame_06_all_clean.png", "06_all_clean.png"),
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


def _split_atlas(source: Path, output_dir: Path, names: tuple[str, ...]) -> list[Path]:
	if len(names) != 6:
		raise ValueError("dirty-castle atlases must contain exactly six sprites")
	output_dir.mkdir(parents=True, exist_ok=True)
	image = Image.open(source).convert("RGBA")
	outputs: list[Path] = []
	for index, name in enumerate(names):
		col = index % 3
		row = index // 3
		left = round(col * image.width / 3)
		right = round((col + 1) * image.width / 3)
		top = round(row * image.height / 2)
		bottom = round((row + 1) * image.height / 2)
		sprite = _fit_sprite(image.crop((left, top, right, bottom)))
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
) -> None:
	output.parent.mkdir(parents=True, exist_ok=True)
	canvas = Image.new("RGB", (1024, 1024), (28, 20, 43))
	draw = ImageDraw.Draw(canvas)
	font = ImageFont.load_default()
	draw.text((20, 14), title, fill=(255, 244, 219), font=font)
	margin_x = 20
	margin_top = 42
	gap = 10
	cell_w = (1024 - margin_x * 2 - gap * (columns - 1)) // columns
	cell_h = (1024 - margin_top - 20 - gap * (rows - 1)) // rows
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
		if alpha.getbbox() is None:
			raise ValueError(f"{path} is fully transparent")


def main() -> None:
	sprites: list[Path] = []
	for atlas, output_dir, names in ATLASES:
		sprites.extend(_split_atlas(atlas, output_dir, names))
	_validate_sprites(sprites)
	frames = _process_frames()
	_contact_sheet(
		sprites,
		AUDIT / "sprites_contact.png",
		columns=6,
		rows=3,
		title="Dirty Castle cleanup runtime sprites - 18 transparent 512x512 assets",
	)
	_contact_sheet(
		frames,
		AUDIT / "cinematic_contact.png",
		columns=2,
		rows=3,
		title="Dirty Castle cleanup cinematic - 6 runtime frames at 1024x576",
	)
	print(f"Wrote {len(sprites)} sprites and {len(frames)} cinematic frames")


if __name__ == "__main__":
	main()
