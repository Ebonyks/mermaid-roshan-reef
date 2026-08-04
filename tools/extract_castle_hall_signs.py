#!/usr/bin/env python3
"""Derive the Main Hall door badges from approved, already-shipped castle art.

The source backgrounds remain untouched.  Each badge is cropped once and is
uniformly resized onto a transparent 256 px card for Sprite3D use.  The Dream
House badge comes from the already-transparent crest in its approved doorway,
so no piece of the purple portal architecture is copied into the sign.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
HALL = ROOT / "assets/flats/castle/main_hall_2screen"
DREAM_HOUSE = ROOT / "assets/flats/castle/dream_house"
OUTPUT = ROOT / "assets/flats/castle/main_hall_redraw_2026-08-03/signs"
MANIFEST = (
	ROOT
	/ "assets_src/imagegen/castle_main_hall_redraw_2026-08-03/sign_reuse_manifest.json"
)

CANVAS_SIZE = (256, 256)

# center x/y and ellipse radius x/y in the untouched approved source master.
BADGES = {
	"sign_opera_hall.png": ("a", (1005, 345), (62, 51)),
	"sign_library.png": ("a", (1486, 500), (52, 49)),
	"sign_kitchen.png": ("a", (1752, 498), (52, 48)),
	"sign_playroom.png": ("b", (324, 453), (50, 44)),
	"sign_craft_room.png": ("b", (837, 447), (50, 47)),
	"sign_mermaid_pool.png": ("b", (1203, 441), (47, 45)),
	"sign_bubble_bath.png": ("b", (1467, 439), (48, 46)),
}


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def fit_on_card(image: Image.Image, max_size: tuple[int, int]) -> Image.Image:
	image = image.copy()
	image.thumbnail(max_size, Image.Resampling.LANCZOS)
	card = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
	position = (
		(CANVAS_SIZE[0] - image.width) // 2,
		(CANVAS_SIZE[1] - image.height) // 2,
	)
	card.alpha_composite(image, position)
	return card


def extract_round_badge(
	image: Image.Image, center: tuple[int, int], radii: tuple[int, int]
) -> tuple[Image.Image, list[int]]:
	cx, cy = center
	rx, ry = radii
	pad = 2
	box = [cx - rx - pad, cy - ry - pad, cx + rx + pad, cy + ry + pad]
	crop = image.crop(tuple(box)).convert("RGBA")
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse(
		(pad, pad, crop.width - pad - 1, crop.height - pad - 1), fill=255
	)
	mask = mask.filter(ImageFilter.GaussianBlur(0.5))
	crop.putalpha(mask)
	return fit_on_card(crop, (232, 220)), box


def extract_family_badge(image: Image.Image) -> tuple[Image.Image, list[int]]:
	# This box follows only the cream/gold house medallion.  A hand-audited
	# polygon traces its scalloped cap and lower shell; unlike the old ellipse,
	# it excludes the purple scrollwork and navy doorway arch behind the crest.
	box = [158, 0, 335, 178]
	crop = image.crop(tuple(box)).convert("RGBA")
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.polygon([
		(88, 0), (111, 4), (128, 14), (146, 19), (160, 31),
		(168, 45), (176, 58), (176, 77), (172, 95), (164, 111),
		(151, 124), (137, 133), (121, 139), (105, 144), (72, 144),
		(56, 139), (40, 133), (26, 124), (14, 111), (6, 95),
		(1, 77), (2, 58), (9, 44), (18, 31), (31, 22), (48, 16),
		(64, 6),
	], fill=255)
	draw.polygon([
		(55, 116), (70, 112), (88, 116), (106, 112), (122, 117),
		(126, 134), (120, 151), (107, 163), (89, 174), (72, 164),
		(59, 152), (52, 135),
	], fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(0.45))
	crop.putalpha(ImageChops.multiply(crop.getchannel("A"), mask))
	return fit_on_card(crop, (102, 98)), box


def main() -> None:
	OUTPUT.mkdir(parents=True, exist_ok=True)
	MANIFEST.parent.mkdir(parents=True, exist_ok=True)
	sources = {
		"a": HALL / "main_hall_screen_a_room_led_master.png",
		"b": HALL / "main_hall_screen_b_room_led_master.png",
		"family": DREAM_HOUSE / "family_wing_hall_insert.png",
	}
	images = {key: Image.open(path) for key, path in sources.items()}
	records: list[dict[str, object]] = []

	for output_name, (source_key, center, radii) in BADGES.items():
		card, box = extract_round_badge(images[source_key], center, radii)
		output_path = OUTPUT / output_name
		card.save(output_path, optimize=True)
		records.append(
			{
				"output": output_path.relative_to(ROOT).as_posix(),
				"output_sha256": sha256(output_path),
				"output_dimensions": list(card.size),
				"source": sources[source_key].relative_to(ROOT).as_posix(),
				"source_sha256": sha256(sources[source_key]),
				"source_crop_xyxy": box,
				"derivation": "approved crop + soft ellipse alpha + Lanczos resize",
			}
		)

	family_card, family_box = extract_family_badge(images["family"])
	family_output = OUTPUT / "sign_family_gallery.png"
	family_card.save(family_output, optimize=True)
	records.append(
		{
			"output": family_output.relative_to(ROOT).as_posix(),
			"output_sha256": sha256(family_output),
			"output_dimensions": list(family_card.size),
			"source": sources["family"].relative_to(ROOT).as_posix(),
			"source_sha256": sha256(sources["family"]),
			"source_crop_xyxy": family_box,
			"derivation": (
				"approved crest-only crop + hand-traced semantic alpha + "
				"whole-object Lanczos resize"
			),
		}
	)

	manifest = {
		"schema": "castle_main_hall_sign_reuse_v1",
		"purpose": "separate unshaded Sprite3D door signs over blank sockets",
		"new_generation_used": False,
		"protected_sources_modified": False,
		"canvas_dimensions": list(CANVAS_SIZE),
		"records": sorted(records, key=lambda item: str(item["output"])),
	}
	MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(f"Wrote {len(records)} reused signs and {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
	main()
