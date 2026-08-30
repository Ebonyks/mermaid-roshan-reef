#!/usr/bin/env python3
"""Build non-destructive single-owner Craft table cards and review evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
OUTPUT_DIR = ROOT / "assets" / "castle" / "day_one_room_corrections_2026-08-30"
MANIFEST_PATH = Path(__file__).with_name("craft_table_alpha_cleanup_manifest.json")
REFINEMENT_PATH = (
    ROOT / "assets_src" / "castle" / "depth_cards"
    / "static_depth_card_refinement.json"
)
CORE_ALPHA_THRESHOLD = 224
ANTIALIAS_FRINGE_RADIUS = 2


def sha256(path: Path) -> str:
    hash_value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def reviewed_body_mask(side: str, size: tuple[int, int]) -> tuple[Image.Image, int]:
    refinement = json.loads(REFINEMENT_PATH.read_text(encoding="utf-8"))
    card_id = f"front_{side}"
    entry = next(
        card for card in refinement["cards"]
        if card.get("room") == "craft_room" and card.get("id") == card_id
    )
    scale = 4
    mask = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    draw = ImageDraw.Draw(mask)
    selected = 0
    for shape in entry["keep_shapes"]:
        if shape.get("type") != "polygon":
            continue
        points = shape["points"]
        width = max(point[0] for point in points) - min(point[0] for point in points)
        max_y = max(point[1] for point in points)
        # The repository review manifest separates broad tabletop/body polygons
        # from narrow prop masks. Fill only those broad physical table owners.
        if width < 200 or max_y < 100:
            continue
        draw.polygon([(x * scale, y * scale) for x, y in points], fill=255)
        selected += 1
    mask = mask.resize(size, Image.Resampling.LANCZOS)
    return mask, selected


def clean_card(side: str, source_path: Path, output_path: Path) -> dict[str, object]:
    image = Image.open(source_path).convert("RGBA")
    alpha = image.getchannel("A")
    core = alpha.point(lambda value: 255 if value >= CORE_ALPHA_THRESHOLD else 0)
    near_core = core.filter(ImageFilter.MaxFilter(ANTIALIAS_FRINGE_RADIUS * 2 + 1))
    alpha_pixels = list(alpha.getdata())
    core_pixels = list(core.getdata())
    near_pixels = list(near_core.getdata())
    fringe_alpha = Image.new("L", image.size)
    fringe_alpha.putdata([
        255 if core_value else original_alpha if near_value else 0
        for original_alpha, core_value, near_value
        in zip(alpha_pixels, core_pixels, near_pixels)
    ])
    body_mask, selected_shape_count = reviewed_body_mask(side, image.size)
    cleaned_alpha = ImageChops.lighter(fringe_alpha, body_mask)
    full_room = Image.open(SOURCE_DIR / "room_craft_room.png").convert("RGB")
    crop_x = 0 if side == "left" else 720
    crop_rgb = full_room.crop((crop_x, 316, crop_x + image.width, 316 + image.height))
    red, green, blue = crop_rgb.split()
    zero = Image.new("L", image.size, 0)
    red = Image.composite(red, zero, cleaned_alpha)
    green = Image.composite(green, zero, cleaned_alpha)
    blue = Image.composite(blue, zero, cleaned_alpha)
    output = Image.merge("RGBA", (red, green, blue, cleaned_alpha))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(output_path, optimize=False, compress_level=9)
    return {
        "source_path": source_path.relative_to(ROOT).as_posix(),
        "source_sha256": sha256(source_path),
        "approved_rgb_source_path": (
            SOURCE_DIR / "room_craft_room.png").relative_to(ROOT).as_posix(),
        "approved_rgb_source_sha256": sha256(SOURCE_DIR / "room_craft_room.png"),
        "reviewed_mask_manifest_path": REFINEMENT_PATH.relative_to(ROOT).as_posix(),
        "reviewed_mask_manifest_sha256": sha256(REFINEMENT_PATH),
        "reviewed_table_body_polygon_count": selected_shape_count,
        "runtime_path": output_path.relative_to(ROOT).as_posix(),
        "runtime_sha256": sha256(output_path),
        "dimensions": list(output.size),
        "source_partial_alpha_pixels": sum(0 < value < 255 for value in alpha_pixels),
        "runtime_partial_alpha_pixels": sum(
            0 < value < 255 for value in cleaned_alpha.getdata()),
        "removed_peripheral_alpha_pixels": sum(
            original > 0 and cleaned == 0
            for original, cleaned in zip(alpha_pixels, cleaned_alpha.getdata())),
        "recovered_reviewed_body_pixels": sum(
            original == 0 and cleaned > 0
            for original, cleaned in zip(alpha_pixels, cleaned_alpha.getdata())),
    }


def compose(
    background: Image.Image,
    cards: list[tuple[Image.Image, tuple[int, int]]],
) -> Image.Image:
    result = background.convert("RGBA")
    for card, position in cards:
        result.alpha_composite(card.convert("RGBA"), position)
    return result.convert("RGB")


def build_review_sheet(cleaned: dict[str, Path], output_path: Path) -> None:
    background = Image.open(
        ROOT / "assets" / "flats" / "castle" / "interactions_v4"
        / "backgrounds" / "room_craft_room_background.png").convert("RGB")
    left = Image.open(SOURCE_DIR / "room_craft_room_front_left.png")
    right = Image.open(SOURCE_DIR / "room_craft_room_front_right.png")
    palette = Image.open(SOURCE_DIR / "room_craft_room_item_palette.png")
    clean_left = Image.open(cleaned["left"])
    clean_right = Image.open(cleaned["right"])
    panels = [
        ("BACKGROUND ONLY - NO TABLES", compose(background, [])),
        ("SOURCE LEFT - ONE TABLE", compose(background, [(left, (0, 316))])),
        ("SOURCE RIGHT - ONE TABLE", compose(background, [(right, (720, 316))])),
        ("REJECTED DUPLICATE - LEFT + PALETTE", compose(
            background, [(left, (0, 316)), (palette, (0, 320))])),
        ("FINAL - TWO ALPHA-CLEAN SINGLE OWNERS", compose(
            background, [(clean_left, (0, 316)), (clean_right, (720, 316))])),
    ]
    panel_size = (512, 288)
    caption_height = 32
    sheet = Image.new("RGB", (1024, (caption_height + 288) * 3), "#201a34")
    draw = ImageDraw.Draw(sheet)
    for index, (caption, panel) in enumerate(panels):
        column = index % 2
        row = index // 2
        x = column * panel_size[0]
        y = row * (caption_height + panel_size[1])
        draw.rectangle((x, y, x + panel_size[0], y + caption_height), fill="#201a34")
        draw.text((x + 10, y + 9), caption, fill="#fff4bf")
        sheet.paste(panel.resize(panel_size, Image.Resampling.LANCZOS),
                    (x, y + caption_height))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, optimize=False, compress_level=9)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-output", type=Path)
    args = parser.parse_args()
    outputs = {
        "left": OUTPUT_DIR / "craft_table_front_left_alpha_clean.png",
        "right": OUTPUT_DIR / "craft_table_front_right_alpha_clean.png",
    }
    entries = []
    for side, output_path in outputs.items():
        entries.append(clean_card(
            side, SOURCE_DIR / f"room_craft_room_front_{side}.png", output_path))
    manifest = {
        "schema": "day_one_craft_table_alpha_cleanup_v2",
        "method": (
            "Recover RGB only from the approved room_craft_room.png crop. Promote "
            "source-card alpha >=224 to opaque; preserve original antialias values "
            "within two pixels of that core; union only the broad tabletop/body "
            "polygons already reviewed in static_depth_card_refinement.json; zero "
            "all other alpha and hidden RGB. Originals remain unchanged."
        ),
        "core_alpha_threshold": CORE_ALPHA_THRESHOLD,
        "antialias_fringe_radius_pixels": ANTIALIAS_FRINGE_RADIUS,
        "entries": entries,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if args.audit_output:
        build_review_sheet(outputs, args.audit_output.resolve())


if __name__ == "__main__":
    main()
