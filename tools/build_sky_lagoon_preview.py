#!/usr/bin/env python3
"""Build the exact high-resolution 3:1 Sky Lagoon preview from runtime art."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
OUT_DAY_ONE = ROOT / "audit/sky_lagoon_preview_day_one_3x1.jpg"
OUT_REVISIT = ROOT / "audit/sky_lagoon_preview_revisit_3x1.jpg"
WORLD_LEFT = -72.0
WORLD_TOP = 33.5
WORLD_WIDTH = 144.0
WORLD_HEIGHT = 48.0


def place(
	canvas: Image.Image,
	path: str,
	x: float,
	y: float,
	world_height: float,
	opacity: float = 1.0,
) -> None:
	sprite = Image.open(ROOT / path).convert("RGBA")
	scale = canvas.height / WORLD_HEIGHT
	height = max(1, round(world_height * scale))
	width = max(1, round(sprite.width * height / sprite.height))
	sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
	if opacity < 1.0:
		sprite.putalpha(sprite.getchannel("A").point(lambda value: round(value * opacity)))
	center_x = round((x - WORLD_LEFT) / WORLD_WIDTH * canvas.width)
	center_y = round((WORLD_TOP - y) / WORLD_HEIGHT * canvas.height)
	canvas.alpha_composite(sprite, (center_x - width // 2, center_y - height // 2))


def shadow(canvas: Image.Image, x: float, y: float, object_height: float) -> None:
	bottom = y - object_height * 0.5 + max(0.08, object_height * 0.025)
	place(
		canvas,
		"assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png",
		x,
		bottom,
		max(0.55, object_height * 0.068),
	)


def build_preview(show_plane: bool) -> Image.Image:
	canvas = Image.open(MASTER).convert("RGBA")
	# Sky card first, then distant PNW standees.
	place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png", -10.0, 29.0, 3.2)
	for path, x, y, height in (
		("assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png", 26.0, 6.5, 9.5),
		("assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_medium_v1.png", -27.0, 6.2, 8.5),
	):
		place(canvas, path, x, y, height)
	# The full stained-glass castle is one extracted depth card; the clean
	# plate deliberately has no duplicate facade underneath it.
	place(
		canvas,
		"assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png",
		53.5,
		10.8,
		31.0,
	)

	# Three activity easels, each with its own protected book page.
	for x, page in (
		(-34.5, "assets/book/hall/p_snowman.jpg"),
		(-17.5, "assets/book/hall/p_garden.jpg"),
		(33.3, "assets/book/hall/p_trampoline.jpg"),
	):
		shadow(canvas, x, 4.4, 12.95)
		place(canvas, page, x, 4.4, 9.05)
		place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_activity_frame_v3.png", x, 4.4, 12.95)

	for path, x, y, height in (
		("assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png", -9.5, 5.0, 12.0),
		("assets/sprites/sky_lagoon/sky_lagoon_swing_v3_compact.png", 2.5, 5.0, 11.0),
		("assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png", 13.0, 1.85, 4.2),
	):
		shadow(canvas, x, y, height)
		place(canvas, path, x, y, height)
	if show_plane:
		shadow(canvas, -58.0, 4.85, 12.0)
		place(
			canvas,
			"assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
			-58.0,
			4.85,
			12.0,
		)

	# Roshan appears once, at the arrival end, as she does on stage entry.
	shadow(canvas, -55.0, 4.0, 7.8)
	place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png", -55.0, 4.0, 7.8)
	return canvas


def main() -> None:
	OUT_DAY_ONE.parent.mkdir(parents=True, exist_ok=True)
	build_preview(True).convert("RGB").save(
		OUT_DAY_ONE, quality=94, subsampling=0, optimize=True
	)
	build_preview(False).convert("RGB").save(
		OUT_REVISIT, quality=94, subsampling=0, optimize=True
	)
	print(OUT_DAY_ONE)
	print(OUT_REVISIT)


if __name__ == "__main__":
	main()
