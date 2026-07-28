#!/usr/bin/env python3
"""Publish the single-canvas Fairy Pond panorama and its ornament sprites.

The pond is generated once as one continuous landscape.  This script performs
only deterministic normalization: it scales that source to the runtime 4:1
power-of-two contract and removes the flat red key from the two ornament
cutouts.  It never tiles, mirrors, joins, or crossfades background images.

Usage:
	python tools/process_fairy_panorama.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "fairy_v5" / "concepts"
MASTER_DIR = ROOT / "assets_src" / "fairy_v5" / "runtime_textures"
RUNTIME_DIR = ROOT / "assets" / "fairy"
PANORAMA_SOURCE = SOURCE_DIR / "fairy_pond_panorama_raw.png"
ORNAMENT_SOURCE = SOURCE_DIR / "pond_ornaments_chroma.png"
PANORAMA_SIZE = (4096, 1024)
CARD_EDGE = 1024
SUBJECT_EDGE = 920


def _publish_panorama() -> None:
	if not PANORAMA_SOURCE.exists():
		raise FileNotFoundError(PANORAMA_SOURCE)
	image = Image.open(PANORAMA_SOURCE).convert("RGB")
	# The built-in generator's wide canvas is normalized to the requested 4:1
	# runtime surface in one resample.  No spatially separate plates exist.
	image = image.resize(PANORAMA_SIZE, Image.Resampling.LANCZOS)
	RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
	target = RUNTIME_DIR / "pond_panorama.png"
	image.save(target, format="PNG", optimize=True)
	print(f"wrote {target.relative_to(ROOT)} size={image.width}x{image.height}")


def _remove_red_key(image: Image.Image) -> Image.Image:
	rgba = image.convert("RGBA")
	pixels = list(rgba.getdata())
	cleaned: list[tuple[int, int, int, int]] = []
	for red, green, blue, _alpha in pixels:
		# Generated subjects deliberately contain no red.  The generous
		# dominance threshold removes the key and its antialiasing fringe while
		# preserving cream/gold flower centers.
		is_key = red > 120 and red > green * 1.32 and red > blue * 1.32
		cleaned.append((red, green, blue, 0 if is_key else 255))
	rgba.putdata(cleaned)
	return rgba


def _write_card(image: Image.Image, target: Path) -> None:
	bounds = image.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError(f"no opaque ornament found for {target}")
	subject = image.crop(bounds)
	subject.thumbnail((SUBJECT_EDGE, SUBJECT_EDGE), Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", (CARD_EDGE, CARD_EDGE), (0, 0, 0, 0))
	canvas.alpha_composite(
		subject,
		((CARD_EDGE - subject.width) // 2, (CARD_EDGE - subject.height) // 2),
	)
	target.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(target, format="PNG", optimize=True)
	print(f"wrote {target.relative_to(ROOT)}")


def _publish_ornaments() -> None:
	if not ORNAMENT_SOURCE.exists():
		raise FileNotFoundError(ORNAMENT_SOURCE)
	sheet = Image.open(ORNAMENT_SOURCE).convert("RGB")
	midpoint = sheet.width // 2
	halves = {
		"ornament_lily_cluster.png": sheet.crop((0, 0, midpoint, sheet.height)),
		"ornament_lavender_reeds.png": sheet.crop((midpoint, 0, sheet.width, sheet.height)),
	}
	for name, image in halves.items():
		_write_card(_remove_red_key(image), MASTER_DIR / name)


def main() -> None:
	_publish_panorama()
	_publish_ornaments()


if __name__ == "__main__":
	main()
