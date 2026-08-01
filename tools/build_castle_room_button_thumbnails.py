#!/usr/bin/env python3
"""Build lightweight castle elevator thumbnails from approved room composites."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
OUTPUT_DIR = ROOT / "assets" / "ui" / "castle_room_buttons"
ROOM_IDS = (
	"main_hall",
	"opera_hall",
	"kitchen",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
)
OUTPUT_SIZE = (440, 264)
MAIN_HALL_SOURCE = (
	ROOT / "assets_src" / "castle" / "main_hall_alignment"
	/ "main_hall_screen_b_fixture_aligned_master.png"
)


def build_thumbnail(room_id: str) -> None:
	source_path = (
		MAIN_HALL_SOURCE
		if room_id == "main_hall"
		else SOURCE_DIR / f"room_{room_id}.png"
	)
	output_path = OUTPUT_DIR / f"room_{room_id}.png"
	with Image.open(source_path) as source:
		image = source.convert("RGBA")
		if room_id == "main_hall":
			# Match the exact accepted runtime Screen B source rectangle, then
			# retain its centered portal gallery and throne at the card's 5:3.
			image = image.crop((376, 147, 2048, 1088))
			left = (image.width - 1568) // 2
			image = image.crop((left, 0, left + 1568, image.height))
		else:
			# The 220x132 runtime card is 5:3. Remove only 32 pixels from each
			# horizontal edge of the 16:9 master so the defining centerpiece
			# remains centered without distortion or newly painted pixels.
			left = (image.width - 960) // 2
			image = image.crop((left, 0, left + 960, image.height))
		image = image.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
		image.save(output_path, format="PNG", optimize=True)
	print(f"built {output_path.relative_to(ROOT)}")


def main() -> None:
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	for room_id in ROOM_IDS:
		build_thumbnail(room_id)


if __name__ == "__main__":
	main()
