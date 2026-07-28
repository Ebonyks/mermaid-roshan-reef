#!/usr/bin/env python3
"""Build the exact high-resolution 3:1 Sky Lagoon preview from runtime art."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v4_hd_3x1.png"
OUT = ROOT / "audit/sky_lagoon_congruency_preview_3x1.jpg"
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


def main() -> None:
	canvas = Image.open(MASTER).convert("RGBA")
	# Sky card first, then distant PNW standees.
	place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png", -10.0, 29.0, 3.2)
	for path, x, y, height in (
		("assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png", 26.0, 6.5, 9.5),
		("assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_medium_v1.png", -27.0, 6.2, 8.5),
	):
		place(canvas, path, x, y, height)
	for x, y, height in ((-24.0, 1.3, 6.55), (23.5, 1.35, 6.3), (62.0, 1.55, 6.8)):
		shadow(canvas, x, y, height)
		place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway_audited.png", x, y, height)

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
		("assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png", -58.0, 4.85, 12.0),
		("assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png", -9.5, 5.0, 12.0),
		("assets/sprites/sky_lagoon/sky_lagoon_swing_v3_compact.png", 2.5, 5.0, 11.0),
		("assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png", 13.0, 1.85, 4.2),
	):
		shadow(canvas, x, y, height)
		place(canvas, path, x, y, height)

	# Roshan appears once, at the arrival end, as she does on stage entry.
	shadow(canvas, -55.0, 4.0, 7.8)
	place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png", -55.0, 4.0, 7.8)

	OUT.parent.mkdir(parents=True, exist_ok=True)
	canvas.convert("RGB").save(OUT, quality=94, subsampling=0, optimize=True)
	print(OUT)


if __name__ == "__main__":
	main()
