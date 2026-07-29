"""Build approved castle item style replacements from existing 2D art.

The legacy Main Hall pedestal fountains are the only touch-prop style outliers.
This tool preserves them and extracts the richer shell fountain already painted
in the approved Main Hall dressed concept. The source is downsampled once to its
correct 1024-wide runtime scale; the right-hand copy is then mirrored.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps
from skimage.restoration import inpaint


ROOT = Path(__file__).resolve().parents[1]
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
SOURCE = (
	ROOT / "audit" / "castle_sprite3d"
	/ "main_hall_screen_b_dressed_preview.png")
LEFT = ROOM_DIR / "room_main_hall_item_fountain_left_v2.png"
RIGHT = ROOM_DIR / "room_main_hall_item_fountain_right_v2.png"
BACKGROUND_SOURCE = ROOM_DIR / "room_main_hall_background.png"
BACKGROUND_V2 = ROOM_DIR / "room_main_hall_background_v2.png"
ORIGINAL_COMPOSITE = ROOM_DIR / "room_main_hall.png"
DEPTH_MANIFEST = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
SOURCE_CROP = (10, 628, 360, 925)
RUNTIME_SIZE = (214, 182)


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def main() -> None:
	source = Image.open(SOURCE).convert("RGBA")
	mask = Image.new("L", source.size, 0)
	draw = ImageDraw.Draw(mask)
	# The outer basin, raised shell bowl, crown shell, and waterfall are one
	# contiguous fountain silhouette. Including the water inside those shapes
	# preserves the source painting without bringing a rectangular floor patch.
	draw.ellipse((15, 758, 356, 920), fill=255)
	draw.ellipse((88, 683, 272, 758), fill=255)
	draw.polygon(
		((137, 684), (145, 653), (158, 638), (177, 658),
		 (191, 639), (211, 660), (220, 686), (207, 710),
		 (181, 724), (154, 711)),
		fill=255)
	draw.polygon(
		((123, 708), (239, 708), (230, 850), (116, 850)),
		fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(1.2))
	source.putalpha(mask)
	crop = source.crop(SOURCE_CROP)
	left = crop.resize(RUNTIME_SIZE, Image.Resampling.LANCZOS)
	left.save(LEFT, optimize=True)
	ImageOps.mirror(left).save(RIGHT, optimize=True)

	# The old clean plate was authored to sit behind the broad legacy
	# pedestals. Its scanline fill becomes visible around the tighter new shell
	# silhouette. Refill exactly the old fountain-owned pixels from their real
	# neighboring architecture in the immutable room composite. Biharmonic
	# inpainting is confined to the padded legacy alpha silhouettes; every
	# unmasked source pixel remains untouched.
	background = Image.open(BACKGROUND_SOURCE).convert("RGB")
	original = Image.open(ORIGINAL_COMPOSITE).convert("RGB")
	repair_mask = Image.new("L", original.size, 0)
	for filename, position in (
			("room_main_hall_item_fountain_left.png", (122, 379)),
			("room_main_hall_item_fountain_right.png", (756, 379)),
	):
		alpha = Image.open(ROOM_DIR / filename).convert("RGBA").getchannel("A")
		placed = Image.new("L", original.size, 0)
		placed.paste(alpha, position)
		repair_mask = ImageChops.lighter(repair_mask, placed)
	repair_mask = repair_mask.filter(ImageFilter.MaxFilter(11))
	repair_array = inpaint.inpaint_biharmonic(
		np.asarray(original, dtype=np.float32) / 255.0,
		np.asarray(repair_mask, dtype=np.uint8) > 0,
		channel_axis=-1)
	repair = Image.fromarray(
		np.clip(repair_array * 255.0, 0, 255).astype(np.uint8),
		"RGB")
	feather = repair_mask.filter(ImageFilter.GaussianBlur(1.5))
	Image.composite(repair, background, feather).save(
		BACKGROUND_V2, optimize=True)

	if DEPTH_MANIFEST.exists():
		manifest = json.loads(DEPTH_MANIFEST.read_text(encoding="utf-8"))
		main_hall = manifest["rooms"]["main_hall"]
		main_hall["runtime_background"] = BACKGROUND_V2.name
		main_hall["runtime_background_dimensions"] = list(
			Image.open(BACKGROUND_V2).size)
		main_hall["runtime_background_sha256"] = _sha256(BACKGROUND_V2)
		main_hall["runtime_texture_overrides"] = {
			"item_fountain_left": LEFT.name,
			"item_fountain_right": RIGHT.name,
		}
		main_hall["style_gate"] = {
			"threshold": 4.5,
			"legacy_fountain_score": 3.3,
			"replacement_fountain_score": 4.7,
			"audit": "FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md",
		}
		DEPTH_MANIFEST.write_text(
			json.dumps(manifest, indent=2, sort_keys=True) + "\n",
			encoding="utf-8")

	for path in (SOURCE, LEFT, RIGHT, BACKGROUND_SOURCE, BACKGROUND_V2):
		with Image.open(path) as image:
			print(
				f"{path.relative_to(ROOT).as_posix()} "
				f"{image.width}x{image.height} sha256={_sha256(path)}")


if __name__ == "__main__":
	main()
