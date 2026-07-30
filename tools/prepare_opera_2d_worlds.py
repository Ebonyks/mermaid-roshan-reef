#!/usr/bin/env python3
"""Prepare approved Pearl Opera character art for Godot Canvas play.

Source masters are never changed.  The script:

* keeps the undersized 1024x576 scene keys in source as composition references;
* removes only the edge-connected navy presentation field from Roshan's
  approved outfit cards and fits the result into a 512x512 transparent actor;
* copies the existing costumed-rival QA portraits into stable 512px runtime
  slots.  Boxer is the exception: its owner-approved two-glove transparent
  match sprite is copied directly.

Run from the repository root:
    python tools/prepare_opera_2d_worlds.py
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import shutil

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUTFIT_SOURCE = ROOT / "assets_src/concepts/opera_jobs_flat_2026-07-21/cards"
RIVAL_SOURCE = ROOT / "assets_src/blender/qa_opera_rivals"
RIVAL_SHEET = (
    ROOT
    / "assets_src/concepts/opera_rivals_2026-07-29/opera_rival_costume_sheet_master.png"
)
WORLD_OUTPUT = ROOT / "assets/opera/worlds"
ACTOR_OUTPUT = WORLD_OUTPUT / "actors"

CAREERS = {
    "chef": "pastry_chef",
    "detective": "detective",
    "ballerina": "ballerina",
    "candymaker": "candy_maker",
    "doctor": "doctor",
    "farmer": "farmer",
    "boxer": "boxer",
    "magician": "magician",
    "painter": "painter",
    "astronaut": "astronaut_engineer",
    "racer": "racecar_driver",
    "popstar": "pop_star",
}

RIVAL_CELLS = {
    "chef": (0, 0),
    "detective": (1, 0),
    "ballerina": (2, 0),
    "candymaker": (3, 0),
    "doctor": (0, 1),
    "farmer": (1, 1),
    "magician": (2, 1),
    "painter": (3, 1),
    "astronaut": (0, 2),
    "racer": (1, 2),
    "popstar": (2, 2),
}


def _colour_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum((int(a[i]) - int(b[i])) ** 2 for i in range(3))


def _remove_edge_field(source: Path) -> Image.Image:
    """Remove the connected dark-navy card field, preserving outlined art."""
    image = Image.open(source).convert("RGBA")
    width, height = image.size
    pixels = image.load()
    corners = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]
    field = tuple(sum(int(c[channel]) for c in corners) // 4 for channel in range(3))
    threshold = 82 * 82
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def eligible(x: int, y: int) -> bool:
        colour = pixels[x, y]
        # The source cards have a near-black/navy presentation field.  Requiring
        # both field similarity and low luminance prevents dark outlines or hair
        # from being eaten even when they touch the card border.
        luminance = max(int(colour[0]), int(colour[1]), int(colour[2]))
        return luminance < 94 and _colour_distance(colour, field) <= threshold

    for x in range(width):
        for y in (0, height - 1):
            if eligible(x, y):
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if eligible(x, y):
                queue.append((x, y))

    mask = Image.new("L", image.size, 0)
    mask_pixels = mask.load()
    while queue:
        x, y = queue.popleft()
        index = y * width + x
        if seen[index]:
            continue
        seen[index] = 1
        if not eligible(x, y):
            continue
        mask_pixels[x, y] = 255
        if x > 0:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))
        # Checker squares meet at their corners, so eight-way growth is
        # required to classify the whole presentation field as one region.
        if x > 0 and y > 0:
            queue.append((x - 1, y - 1))
        if x + 1 < width and y > 0:
            queue.append((x + 1, y - 1))
        if x > 0 and y + 1 < height:
            queue.append((x - 1, y + 1))
        if x + 1 < width and y + 1 < height:
            queue.append((x + 1, y + 1))

    # A tiny feather removes the original card-field fringe without softening
    # the approved illustration itself.
    field_mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    alpha = Image.eval(field_mask, lambda value: 255 - value)
    # The source cards also carry a thin blue presentation frame.  It is not
    # character art and never enters the inner 30px, so clear that perimeter
    # explicitly after the connected-field pass.
    alpha_pixels = alpha.load()
    border = 30
    for y in range(height):
        for x in range(width):
            if x < border or y < border or x >= width - border or y >= height - border:
                alpha_pixels[x, y] = 0
    image.putalpha(alpha)
    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError(f"No actor remained after field removal: {source}")
    return image.crop(bounds)


def _fit_actor(actor: Image.Image, size: int = 512) -> Image.Image:
    max_side = size - 24
    scale = min(max_side / actor.width, max_side / actor.height)
    fitted = actor.resize(
        (max(1, round(actor.width * scale)), max(1, round(actor.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - fitted.width) // 2
    y = size - fitted.height - 8
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def _remove_checker(source: Image.Image) -> Image.Image:
    """Remove only the edge-connected light neutral checker presentation."""
    image = source.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def eligible(x: int, y: int) -> bool:
        colour = pixels[x, y]
        low = min(int(colour[0]), int(colour[1]), int(colour[2]))
        high = max(int(colour[0]), int(colour[1]), int(colour[2]))
        average = (int(colour[0]) + int(colour[1]) + int(colour[2])) // 3
        return high - low <= 18 and 214 <= average <= 250

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    field = Image.new("L", image.size, 0)
    field_pixels = field.load()
    while queue:
        x, y = queue.popleft()
        index = y * width + x
        if seen[index]:
            continue
        seen[index] = 1
        if not eligible(x, y):
            continue
        field_pixels[x, y] = 255
        if x > 0:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))
        if x > 0 and y > 0:
            queue.append((x - 1, y - 1))
        if x + 1 < width and y > 0:
            queue.append((x + 1, y - 1))
        if x > 0 and y + 1 < height:
            queue.append((x - 1, y + 1))
        if x + 1 < width and y + 1 < height:
            queue.append((x + 1, y + 1))

    alpha = Image.eval(field.filter(ImageFilter.GaussianBlur(0.8)), lambda value: 255 - value)
    # The checker can form small enclosed islands between a prop and the body
    # (for example inside a curled tail). Remove the same neutral checker range
    # there too. Costume whites are deliberately warm/cool tinted and retained.
    alpha_pixels = alpha.load()
    for y in range(height):
        for x in range(width):
            colour = pixels[x, y]
            low = min(int(colour[0]), int(colour[1]), int(colour[2]))
            high = max(int(colour[0]), int(colour[1]), int(colour[2]))
            if eligible(x, y) or (low >= 248 and high - low <= 3):
                alpha_pixels[x, y] = 0
    image.putalpha(alpha)
    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError("No rival remained after checker removal")
    return image.crop(bounds)


def main() -> None:
    WORLD_OUTPUT.mkdir(parents=True, exist_ok=True)
    ACTOR_OUTPUT.mkdir(parents=True, exist_ok=True)
    rival_sheet = Image.open(RIVAL_SHEET).convert("RGB") if RIVAL_SHEET.exists() else None

    for career, source_slug in CAREERS.items():
        outfit_source = (
            OUTFIT_SOURCE
            / f"opera_job_{source_slug}_outfit_hero_front_three_quarter.png"
        )
        roshan_output = ACTOR_OUTPUT / f"roshan_{career}.png"
        _fit_actor(_remove_edge_field(outfit_source)).save(roshan_output, optimize=True)

        rival_output = ACTOR_OUTPUT / f"rival_{career}.png"
        if career == "boxer":
            boxer_source = ROOT / "assets/opera/rivals/opera_rival_boxer_match.png"
            shutil.copyfile(boxer_source, rival_output)
        elif rival_sheet is not None:
            column, row = RIVAL_CELLS[career]
            x0 = round(column * rival_sheet.width / 4.0)
            x1 = round((column + 1) * rival_sheet.width / 4.0)
            y0 = round(row * rival_sheet.height / 3.0)
            y1 = round((row + 1) * rival_sheet.height / 3.0)
            cell = rival_sheet.crop((x0, y0, x1, y1))
            _fit_actor(_remove_checker(cell)).save(rival_output, optimize=True)
        else:
            qa_source = RIVAL_SOURCE / f"opera_rival_{career}_qa.png"
            qa = Image.open(qa_source).convert("RGBA")
            if qa.size != (512, 512):
                qa.thumbnail((512, 512), Image.Resampling.LANCZOS)
            qa.save(rival_output, optimize=True)

        print(f"prepared {career}: {roshan_output.relative_to(ROOT)}, {rival_output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
