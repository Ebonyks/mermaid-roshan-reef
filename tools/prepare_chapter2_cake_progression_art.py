#!/usr/bin/env python3
"""Prepare Chapter 2 cake-progression ImageGen masters for runtime.

The selected masters use the same pale checker matte as the accepted final
cake.  Reuse the audited border-connected matte removal and whole-canvas
premultiplied-alpha resize so every stage keeps its authored composition.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from prepare_chapter2_birthday_art import _prepare


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = (
	ROOT
	/ "assets_src/imagegen/chapter2_cake_progression_2026-08-31/native"
)
DEST_ROOT = ROOT / "assets/chapter2/birthday"
STAGES = (
	("chapter2_chef_batter_unstirred_native.png",
		"chapter2_chef_batter_unstirred.png"),
	("chapter2_chef_batter_stirred_native.png",
		"chapter2_chef_batter_stirred.png"),
	("chapter2_chef_baked_tiers_unstacked_native.png",
		"chapter2_chef_baked_tiers_unstacked.png"),
	("chapter2_chef_stacked_unfrosted_cake_native.png",
		"chapter2_chef_stacked_unfrosted_cake.png"),
	("chapter2_chef_frosted_rainbow_cake_native.png",
		"chapter2_chef_frosted_rainbow_cake.png"),
	("chapter2_candied_strawberries_tray_native.png",
		"chapter2_candied_strawberries_tray.png"),
	("chapter2_grand_five_strawberry_cake_native.png",
		"chapter2_grand_five_strawberry_cake.png"),
)
SAFE_INSET_DESTINATIONS = {
	"chapter2_chef_baked_tiers_unstacked.png",
	"chapter2_candied_strawberries_tray.png",
	"chapter2_grand_five_strawberry_cake.png",
}
SAFE_CONTENT_SIZE = (960, 960)


def _apply_whole_canvas_safe_inset(destination: Path) -> None:
	"""Scale the complete flattened RGBA canvas uniformly into safe padding."""
	image = Image.open(destination).convert("RGBA")
	if image.size != (1024, 1024):
		raise RuntimeError(f"unexpected staged runtime size: {image.size}")
	image = image.convert("RGBa").resize(
		SAFE_CONTENT_SIZE, Image.Resampling.LANCZOS).convert("RGBA")
	canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
	canvas.alpha_composite(image, (
		(1024 - SAFE_CONTENT_SIZE[0]) // 2,
		(1024 - SAFE_CONTENT_SIZE[1]) // 2,
	))
	canvas.save(destination, format="PNG", optimize=True)


def main() -> None:
	for source_name, destination_name in STAGES:
		destination = DEST_ROOT / destination_name
		_prepare(SOURCE_ROOT / source_name, destination)
		if destination_name in SAFE_INSET_DESTINATIONS:
			_apply_whole_canvas_safe_inset(destination)


if __name__ == "__main__":
	main()
