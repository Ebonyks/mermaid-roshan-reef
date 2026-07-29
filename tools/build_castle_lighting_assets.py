#!/usr/bin/env python3
"""Build the final Pearl Castle fixture assembly and reused tapestry cards."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


INK = (48, 35, 82, 255)
GOLD = (236, 179, 88, 255)
PEARL = (252, 235, 229, 255)


def build_sconce_assembly(sconce_path: Path, output: Path) -> None:
	canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
	draw = ImageDraw.Draw(canvas)
	# An architectural mounting plaque hides the obsolete baked fixture while
	# remaining a single reusable Sprite3D object in both hall halves.
	draw.rounded_rectangle((148, 24, 876, 990), radius=250,
		fill=(64, 43, 96, 255), outline=INK, width=30)
	draw.rounded_rectangle((178, 54, 846, 960), radius=225,
		outline=GOLD, width=22)
	draw.ellipse((430, 78, 594, 242), fill=(114, 84, 151, 255),
		outline=GOLD, width=14)
	draw.ellipse((462, 110, 562, 210), fill=PEARL, outline=INK, width=10)
	for x in (205, 819):
		for y in (305, 706):
			draw.ellipse((x - 22, y - 22, x + 22, y + 22),
				fill=PEARL, outline=GOLD, width=8)
	sconce = Image.open(sconce_path).convert("RGBA")
	sconce.thumbnail((800, 800), Image.Resampling.LANCZOS)
	canvas.alpha_composite(sconce,
		((1024 - sconce.width) // 2, 182))
	output.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(output, optimize=True)


def build_sconce_glow_reuse(sconce_path: Path, output: Path) -> None:
	"""Crop only the approved fixture's pearl core for a discreet light glint."""
	sconce = Image.open(sconce_path).convert("RGBA")
	glow = sconce.crop((424, 414, 600, 590))
	soft_circle = Image.new("L", glow.size, 0)
	draw = ImageDraw.Draw(soft_circle)
	draw.ellipse((2, 2, glow.width - 3, glow.height - 3), fill=255)
	soft_circle = soft_circle.filter(ImageFilter.GaussianBlur(1.5))
	glow.putalpha(ImageChops.multiply(glow.getchannel("A"), soft_circle))
	output.parent.mkdir(parents=True, exist_ok=True)
	glow.save(output, optimize=True)


def build_tapestry_reuse(tile_root: Path, output: Path) -> None:
	"""Extract the approved main-hall shell tapestry as a clean alpha prop."""
	master = _reconstruct_tiles(tile_root)
	crop = master.crop((85, 105, 215, 425))
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	# Gold hanging bar and pearl finials.
	draw.line((14, 33, 116, 33), fill=255, width=10)
	draw.ellipse((9, 28, 20, 39), fill=255)
	draw.ellipse((110, 28, 121, 39), fill=255)
	# Rope triangle and the swallow-tail fabric silhouette.
	draw.line((34, 34, 65, 4, 96, 34), fill=255, width=7, joint="curve")
	draw.polygon(((34, 34), (97, 34), (97, 276), (66, 306), (34, 276)),
		fill=255)
	mask = mask.filter(ImageFilter.MaxFilter(3))
	crop.putalpha(mask)
	output.parent.mkdir(parents=True, exist_ok=True)
	crop.save(output, optimize=True)


def build_playroom_portal_reuse(tile_root: Path, output: Path) -> None:
	"""Reuse an approved open arch to repair the A/B junction and seventh route."""
	master = _reconstruct_tiles(tile_root)
	# First complete small arch on Screen B. The alpha silhouette keeps only the
	# architecture/open corridor; the room marker is a separate existing prop.
	crop = master.crop((2010, 178, 2260, 590))
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	# Keep the arched crown, corridor opening, narrow jambs, and individual
	# feet. Avoid the old full-width rectangle that pasted a foreign floor
	# patch across the A/B join.
	draw.ellipse((20, 92, 230, 302), fill=255)
	draw.rectangle((50, 194, 200, 345), fill=255)
	draw.rectangle((20, 194, 58, 345), fill=255)
	draw.rectangle((192, 194, 230, 345), fill=255)
	mask = mask.filter(ImageFilter.MaxFilter(3))
	crop.putalpha(mask)
	output.parent.mkdir(parents=True, exist_ok=True)
	crop.save(output, optimize=True)


def _reconstruct_tiles(tile_root: Path) -> Image.Image:
	master = Image.new("RGBA", (3344, 941), (0, 0, 0, 0))
	for row in range(2):
		for column in range(4):
			source = tile_root / f"main_hall_room_led_r{row}_c{column}.png"
			tile = Image.open(source).convert("RGBA")
			top = 0 if row == 0 else 470
			master.alpha_composite(tile, (column * 836, top))
	return master


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--out-dir", type=Path, required=True)
	parser.add_argument("--tile-root", type=Path)
	args = parser.parse_args()
	build_sconce_assembly(
		args.out_dir / "castle_shell_sconce_touchable.png",
		args.out_dir / "castle_shell_sconce_assembly.png",
	)
	build_sconce_glow_reuse(
		args.out_dir / "castle_shell_sconce_touchable.png",
		args.out_dir / "castle_sconce_glow_reuse.png",
	)
	if args.tile_root is not None:
		build_tapestry_reuse(
			args.tile_root,
			args.out_dir / "castle_royal_tapestry_reuse.png",
		)
		build_playroom_portal_reuse(
			args.tile_root,
			args.out_dir / "castle_playroom_portal_reuse.png",
		)


if __name__ == "__main__":
	main()
