#!/usr/bin/env python3
"""Build the small, full-bleed Pearl Castle room-selector pictures."""

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "imagegen" / "castle_room_buttons_2026-08-01"
OUTPUT_DIR = ROOT / "assets" / "ui" / "castle_room_buttons"
OUTPUT_SIZE = (400, 224)

ROOM_MASTERS = {
    "main_hall": "castle_button_main_hall_master.png",
    "opera_hall": "castle_button_opera_house_master.png",
    "kitchen": "castle_button_kitchen_master.png",
    "library": "castle_button_library_master.png",
    "playroom": "castle_button_playroom_master.png",
    "craft_room": "castle_button_craft_room_master.png",
    "mermaid_pool": "castle_button_mermaid_pool_master.png",
    "bubble_bath": "castle_button_bubble_bath_master.png",
}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for room_id, master_name in ROOM_MASTERS.items():
        source_path = SOURCE_DIR / master_name
        output_path = OUTPUT_DIR / f"room_{room_id}.png"
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing room-button master: {source_path}")
        with Image.open(source_path) as source:
            thumbnail = ImageOps.fit(
                source.convert("RGB"),
                OUTPUT_SIZE,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            thumbnail.save(output_path, format="PNG", optimize=True)
        print(f"{room_id}: {source_path.name} -> {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
