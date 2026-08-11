#!/usr/bin/env python3
"""Build the phone-sized personalized castle-banner texture set.

The keyed and transparent source masters are preserved under assets_src.  This
script makes non-destructive color variants of the neutral painted cloth and
splits the authored motif sheet into individual transparent icons.
"""

from __future__ import annotations

import colorsys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "castle" / "logo_studio_v2"
OUTPUT_DIR = ROOT / "assets" / "flats" / "castle" / "logo_studio_v2"
BANNER_SOURCE = SOURCE_DIR / "castle_personal_banner_master.png"
MOTIF_SOURCE = SOURCE_DIR / "castle_banner_motifs_master.png"

BANNER_COLORS: dict[str, tuple[int, int, int]] = {
    "pink": (232, 143, 185),
    "gold": (244, 217, 104),
    "mint": (161, 213, 191),
    "ocean": (85, 169, 214),
    "purple": (154, 119, 200),
}
RAINBOW_COLORS: tuple[tuple[int, int, int], ...] = (
    (224, 128, 135),
    (240, 164, 95),
    (238, 207, 105),
    (132, 199, 151),
    (104, 184, 207),
    (164, 132, 202),
)
MOTIF_NAMES: tuple[str, ...] = (
    "rainbow",
    "shell",
    "kitty",
    "dog",
    "star",
    "heart",
    "crown",
    "butterfly",
)
# The generated board follows the requested 4x2 layout, but the painted
# silhouettes deliberately breathe across the mathematical cell centers.
# These gutters sit in the actual clear key-color gaps so no neighboring
# pearl, ear, or wing is clipped into an adjacent runtime icon.
MOTIF_BOXES: tuple[tuple[float, float, float, float], ...] = (
    (0.000, 0.000, 0.250, 0.500),
    (0.250, 0.000, 0.500, 0.500),
    (0.500, 0.000, 0.742, 0.500),
    (0.742, 0.000, 1.000, 0.500),
    (0.000, 0.500, 0.250, 1.000),
    (0.250, 0.500, 0.492, 1.000),
    (0.492, 0.500, 0.727, 1.000),
    (0.727, 0.500, 1.000, 1.000),
)


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("source has no visible pixels")
    return bbox


def crop_with_padding(image: Image.Image, padding: int) -> Image.Image:
    left, top, right, bottom = alpha_bbox(image)
    return image.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
    )


def fit_canvas(image: Image.Image, size: tuple[int, int], margin: int) -> Image.Image:
    available = (size[0] - margin * 2, size[1] - margin * 2)
    fitted = image.copy()
    fitted.thumbnail(available, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (size[0] - fitted.width) // 2
    y = (size[1] - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def cloth_pixel(r: int, g: int, b: int, x: float, y: float) -> bool:
    # Restrict recoloring to the cool neutral cloth.  The warm gold, pearl
    # medallion, shell capital, and finials remain exactly as authored.
    if x < 0.13 or x > 0.87 or y < 0.12 or y > 0.96:
        return False
    medallion = ((x - 0.50) / 0.31) ** 2 + ((y - 0.42) / 0.20) ** 2
    if medallion < 1.0:
        return False
    return b >= r - 20 and b >= g - 20 and max(r, g, b) - min(r, g, b) < 110


def recolor_banner(source: Image.Image, color_id: str) -> Image.Image:
    image = source.copy().convert("RGBA")
    pixels = image.load()
    width, height = image.size
    for py in range(height):
        y = py / max(1, height - 1)
        for px in range(width):
            r, g, b, a = pixels[px, py]
            if a == 0:
                continue
            x = px / max(1, width - 1)
            if not cloth_pixel(r, g, b, x, y):
                continue
            if color_id == "rainbow":
                band_x = min(0.999, max(0.0, (x - 0.13) / 0.74))
                color_position = band_x * (len(RAINBOW_COLORS) - 1)
                index = min(len(RAINBOW_COLORS) - 2, int(color_position))
                blend = color_position - index
                target = tuple(
                    round(RAINBOW_COLORS[index][channel] * (1.0 - blend)
                          + RAINBOW_COLORS[index + 1][channel] * blend)
                    for channel in range(3)
                )
            else:
                target = BANNER_COLORS[color_id]
            lightness = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)[1]
            target_h, target_l, target_s = colorsys.rgb_to_hls(
                target[0] / 255.0, target[1] / 255.0, target[2] / 255.0
            )
            # Retain the generated folds and highlights while keeping the
            # selected colors high-key and quiet enough for the emblem.
            final_l = min(0.96, max(0.50, lightness + (target_l - 0.78) * 0.42))
            nr, ng, nb = colorsys.hls_to_rgb(target_h, final_l, target_s * 0.72)
            pixels[px, py] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
    return image


def build_banners() -> None:
    source = crop_with_padding(Image.open(BANNER_SOURCE).convert("RGBA"), 12)
    for color_id in (*BANNER_COLORS.keys(), "rainbow"):
        banner = recolor_banner(source, color_id)
        output = fit_canvas(banner, (256, 512), 5)
        output.save(OUTPUT_DIR / f"castle_banner_{color_id}.png", optimize=True)


def build_motifs() -> None:
    sheet = Image.open(MOTIF_SOURCE).convert("RGBA")
    for index, motif_name in enumerate(MOTIF_NAMES):
        left, top, right, bottom = MOTIF_BOXES[index]
        cell = sheet.crop(
            (
                round(left * sheet.width),
                round(top * sheet.height),
                round(right * sheet.width),
                round(bottom * sheet.height),
            )
        )
        motif = crop_with_padding(cell, 10)
        output = fit_canvas(motif, (256, 256), 10)
        output.save(OUTPUT_DIR / f"castle_banner_motif_{motif_name}.png", optimize=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_banners()
    build_motifs()
    print(f"Built 6 banners and 8 motifs in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
