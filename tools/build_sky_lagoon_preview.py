#!/usr/bin/env python3
"""Build the exact high-resolution 3:1 Sky Lagoon preview from runtime art."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
OUT_DAY_ONE = ROOT / "audit/sky_lagoon_congruency_preview_3x1.jpg"
OUT_REVISIT = ROOT / "audit/sky_lagoon_preview_revisit_3x1.jpg"
OUT_SCREEN_PATTERN = "sky_lagoon_preview_day_one_screen_%d.jpg"
OUT_SWING_FIT = ROOT / "audit/sky_lagoon_swing_roshan_fit.jpg"
OUT_CASTLE_FIT = (
	ROOT
	/ "assets_src/sky_lagoon/castle_symmetry_2026-07-29"
	/ "qa_four_tower_fit_2screen.jpg"
)
OUT_CASTLE_FOCUS = (
	ROOT
	/ "assets_src/sky_lagoon/castle_symmetry_2026-07-29"
	/ "qa_door_only_focus_2screen.jpg"
)
WORLD_LEFT = -72.0
WORLD_TOP = 33.5
WORLD_WIDTH = 144.0
WORLD_HEIGHT = 48.0
LAYOUT_PATH = ROOT / "scripts/arena/sky_lagoon_layout.json"
LAYOUT = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))


def place(
	canvas: Image.Image,
	path: str,
	x: float,
	y: float,
	world_height: float,
	opacity: float = 1.0,
	width_scale: float = 1.0,
	tint: tuple[int, int, int] | None = None,
) -> None:
	sprite = Image.open(ROOT / path).convert("RGBA")
	scale = canvas.height / WORLD_HEIGHT
	height = max(1, round(world_height * scale))
	width = max(1, round(sprite.width * height / sprite.height * width_scale))
	sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
	if tint is not None:
		alpha = sprite.getchannel("A")
		sprite = Image.new("RGBA", sprite.size, (*tint, 0))
		sprite.putalpha(alpha)
	if opacity < 1.0:
		sprite.putalpha(sprite.getchannel("A").point(lambda value: round(value * opacity)))
	center_x = round((x - WORLD_LEFT) / WORLD_WIDTH * canvas.width)
	center_y = round((WORLD_TOP - y) / WORLD_HEIGHT * canvas.height)
	canvas.alpha_composite(sprite, (center_x - width // 2, center_y - height // 2))


def place_master_anchor(canvas: Image.Image, contract: dict[str, object]) -> None:
	path = str(contract["path"]).removeprefix("res://")
	sprite = Image.open(ROOT / path).convert("RGBA")
	height = round(float(contract["height_master"]))
	width = round(sprite.width * height / sprite.height)
	sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
	scale = height / float(contract["texture_size"][1])
	anchor_pixel = contract["anchor_pixel"]
	anchor_master = contract["anchor_master"]
	left = round(float(anchor_master[0]) - float(anchor_pixel[0]) * scale)
	top = round(float(anchor_master[1]) - float(anchor_pixel[1]) * scale)
	canvas.alpha_composite(sprite, (left, top))


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
	# Sky card first. The independently generated tall tree is intentionally
	# absent: the shared layout contract records that v5 has no source socket
	# for it and that both legacy placements blocked the mountain path.
	place(canvas, "assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png", -10.0, 29.0, 3.2)
	# The bridge's visible tip is the canonical castle anchor. Runtime and this
	# preview consume the same master-space socket rather than converting it
	# independently through center- versus bottom-aligned coordinates.
	place_master_anchor(canvas, LAYOUT["cards"]["castle"])

	for path, x, y, height in (
		("assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png", -11.5, 6.61, 11.4),
		("assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png", 3.0, 6.80, 11.8),
		("assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png", 17.0, 1.20, 4.5),
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
	day_one = build_preview(True)
	day_one.convert("RGB").save(
		OUT_DAY_ONE, quality=94, subsampling=0, optimize=True
	)
	build_preview(False).convert("RGB").save(
		OUT_REVISIT, quality=94, subsampling=0, optimize=True
	)
	# Review the playground-to-castle join as one continuous two-page frame.
	# The half-resolution copy is evidence only; runtime continues to use the
	# native 6144x2048 master and independent 1024px depth cards.
	day_one.crop((2048, 0, 6144, 2048)).resize(
		(2048, 1024), Image.Resampling.LANCZOS
	).convert("RGB").save(
		OUT_CASTLE_FIT, quality=94, subsampling=0, optimize=True
	)
	focused = day_one.copy()
	place(
		focused,
		"assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png",
		51.5312,
		6.6083,
		6.3302,
		opacity=0.64,
		tint=(255, 209, 64),
	)
	focused.crop((2048, 0, 6144, 2048)).resize(
		(2048, 1024), Image.Resampling.LANCZOS
	).convert("RGB").save(
		OUT_CASTLE_FOCUS, quality=94, subsampling=0, optimize=True
	)
	for screen_index in range(3):
		left = screen_index * 2048
		day_one.crop((left, 0, left + 2048, 2048)).convert("RGB").save(
			OUT_DAY_ONE.parent / (OUT_SCREEN_PATTERN % (screen_index + 1)),
			quality=94,
			subsampling=0,
			optimize=True,
		)
	swing_fit = build_preview(False)
	place(
		swing_fit,
		"assets/sprites/sky_lagoon/roshan_playground/roshan_swing_0.png",
		3.0,
		6.80 - 3.60 * (11.8 / 18.4),
		8.34,
		width_scale=1.38,
	)
	swing_fit.crop((2048, 0, 4096, 2048)).convert("RGB").save(
		OUT_SWING_FIT, quality=94, subsampling=0, optimize=True
	)
	print(OUT_DAY_ONE)
	print(OUT_REVISIT)
	print(OUT_SWING_FIT)
	print(OUT_CASTLE_FIT)
	print(OUT_CASTLE_FOCUS)


if __name__ == "__main__":
	main()
