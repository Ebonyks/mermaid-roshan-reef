#!/usr/bin/env python3
"""Build the Chapter 3 Moonflower Conservatory doorway Sprite2D cards.

The shell doorway architecture is normalized from its selected presentation
source.  The open view is then rebuilt deterministically from the approved Sky
Lagoon panorama and the selected Chapter 3 Rainbow Stage cutouts.  This makes
the doorway reveal the handoff stage rather than falsely opening straight into
the Fairy Pond.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = (
    ROOT / "assets_src" / "castle"
    / "fairy_conservatory_chapter3_2026-08-30"
)
RAW_ROOT = SOURCE_ROOT / "raw"
ALPHA_ROOT = SOURCE_ROOT / "alpha"
RUNTIME_ROOT = ROOT / "assets" / "flats" / "castle" / "fairy_conservatory"
REVIEW_ROOT = SOURCE_ROOT / "review"
MANIFEST_PATH = SOURCE_ROOT / "asset_manifest.json"

CANVAS_EDGE = 1024
SUBJECT_EDGE = 960
BACKGROUND_MINIMUM = 232
BACKGROUND_MAXIMUM_SPREAD = 18
MATTE_EROSION = 1
MATTE_FEATHER = 0.8

SOURCES = {
    "closed": RAW_ROOT / "moonflower_door_closed_checker_raw.png",
    "open": RAW_ROOT / "moonflower_door_open_checker_raw.png",
}

SKY_TILE_PATTERN = (
    ROOT / "assets" / "flats" / "sky_lagoon" / "main"
    / "flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{column}.png"
)
HALL_TILE_PATTERN = (
    ROOT / "assets" / "flats" / "castle"
    / "main_hall_redraw_2026-08-03" / "tiles"
    / "main_hall_room_led_r{row}_c{column}.png"
)
WALKWAY_SOURCE = (
    ROOT / "assets" / "flats" / "fairy_conservatory_handoff"
    / "rainbow_walkway.png"
)
HOUSE_SOURCE = (
    ROOT / "assets" / "flats" / "fairy_conservatory_handoff"
    / "butterfly_house.png"
)
BUTTERFLY_SOURCE = ROOT / "assets" / "mg" / "butterfly.png"

HORIZON_Y = 468
OPENING_LEFT = 316
OPENING_RIGHT = 708
OPENING_TOP = 228
OPENING_SPRING = 438
OPENING_BOTTOM = 965
HALL_LOGICAL_SIZE = (3344, 941)
HALL_DOOR_CENTER = (1672, 385)
HALL_DOOR_CARD_EDGE = round(CANVAS_EDGE * 0.4896)
HALL_REVIEW_LEFT = 836
HALL_REVIEW_WIDTH = 1672


def _hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _connected(mask: np.ndarray, seeds: list[int]) -> np.ndarray:
    """Return the 8-connected portion of ``mask`` reached from ``seeds``."""
    height, width = mask.shape
    flat = mask.ravel()
    reached = bytearray(width * height)
    queue: deque[int] = deque()

    def push(index: int) -> None:
        if not reached[index] and bool(flat[index]):
            reached[index] = 1
            queue.append(index)

    for seed in seeds:
        push(seed)
    while queue:
        index = queue.popleft()
        y_pos, x_pos = divmod(index, width)
        for y_next in range(max(0, y_pos - 1), min(height, y_pos + 2)):
            row = y_next * width
            for x_next in range(max(0, x_pos - 1), min(width, x_pos + 2)):
                push(row + x_next)
    return np.frombuffer(reached, dtype=np.uint8).reshape(
        (height, width)).astype(bool)


def _extract_subject(source: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    rgb = np.asarray(source.convert("RGB"), dtype=np.uint8)
    height, width = rgb.shape[:2]
    minimum = rgb.min(axis=2)
    spread = rgb.max(axis=2) - minimum
    neutral = (minimum >= BACKGROUND_MINIMUM) & (
        spread <= BACKGROUND_MAXIMUM_SPREAD)

    border_seeds: list[int] = []
    border_seeds.extend(range(width))
    border_seeds.extend((height - 1) * width + x_pos for x_pos in range(width))
    border_seeds.extend(y_pos * width for y_pos in range(height))
    border_seeds.extend(y_pos * width + width - 1 for y_pos in range(height))
    background = _connected(neutral, border_seeds)
    foreground = ~background

    center_index = (height // 2) * width + width // 2
    if not foreground.ravel()[center_index]:
        y_pos, x_pos = np.unravel_index(
            int(np.argmax(foreground)), foreground.shape)
        center_index = int(y_pos) * width + int(x_pos)
    subject = _connected(foreground, [center_index])
    hard_alpha = Image.fromarray(subject.astype(np.uint8) * 255, "L")
    core = hard_alpha
    for _ in range(MATTE_EROSION):
        core = core.filter(ImageFilter.MinFilter(3))
    alpha = core.filter(ImageFilter.GaussianBlur(MATTE_FEATHER))
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError("checker removal left no doorway subject")

    rgba = np.dstack((rgb, np.asarray(alpha, dtype=np.uint8)))
    rgba[rgba[:, :, 3] == 0, :3] = 0
    extracted = Image.fromarray(rgba, "RGBA").crop(bounds)
    return extracted, {
        "source_dimensions": [width, height],
        "source_subject_bbox": list(bounds),
        "border_connected_background_pixels": int(background.sum()),
        "subject_core_pixels": int(subject.sum()),
    }


def _fit_card(subject: Image.Image) -> Image.Image:
    scale = min(SUBJECT_EDGE / subject.width, SUBJECT_EDGE / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    fitted = subject.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS_EDGE, CANVAS_EDGE), (0, 0, 0, 0))
    canvas.alpha_composite(
        fitted,
        ((CANVAS_EDGE - fitted.width) // 2,
         (CANVAS_EDGE - fitted.height) // 2),
    )
    return canvas


def _opening_mask() -> Image.Image:
    """Mask the clear architectural opening, inset under the inner arch lip."""
    mask = Image.new("L", (CANVAS_EDGE, CANVAS_EDGE), 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice(
        (
            OPENING_LEFT,
            OPENING_TOP,
            OPENING_RIGHT,
            OPENING_SPRING * 2 - OPENING_TOP,
        ),
        start=180,
        end=360,
        fill=255,
    )
    draw.rectangle(
        (OPENING_LEFT, OPENING_SPRING, OPENING_RIGHT, OPENING_BOTTOM),
        fill=255,
    )
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def _approved_sky() -> Image.Image:
    """Reconstruct the approved 6x2 Sky Lagoon panorama and choose its calm bay."""
    panorama = Image.new("RGB", (6144, 2048))
    for row in range(2):
        for column in range(6):
            path = Path(str(SKY_TILE_PATTERN).format(row=row, column=column))
            if not path.is_file():
                raise FileNotFoundError(path)
            tile = Image.open(path).convert("RGB")
            if tile.size != (1024, 1024):
                raise ValueError(f"unexpected Sky Lagoon tile size: {path} {tile.size}")
            panorama.paste(tile, (column * 1024, row * 1024))
    # The source horizon sits near the middle of this crop.  Cropping 200 px
    # from its top aligns the visible cloud bank with HORIZON_Y after resize.
    calm_bay = panorama.crop((2048, 200, 4096, 2048))
    return calm_bay.resize(
        (CANVAS_EDGE, CANVAS_EDGE), Image.Resampling.LANCZOS).convert("RGBA")


def _place_runtime_sprite(
        scene: Image.Image, path: Path, center: tuple[int, int], edge: int) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    sprite = Image.open(path).convert("RGBA")
    bounds = sprite.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError(f"approved runtime sprite has no alpha subject: {path}")
    sprite = sprite.crop(bounds)
    scale = edge / max(sprite.size)
    sprite = sprite.resize(
        (max(1, round(sprite.width * scale)),
         max(1, round(sprite.height * scale))),
        Image.Resampling.LANCZOS,
    )
    scene.alpha_composite(
        sprite,
        (center[0] - sprite.width // 2, center[1] - sprite.height // 2),
    )


def _approved_open_scene() -> Image.Image:
    """Compose the open view from the approved sky and handoff-stage art."""
    scene = _approved_sky()
    # The physical house sits at the horizon; the one-point walkway begins
    # there and grows toward the threshold.  The doorway mask supplies the
    # final side/bottom clipping, so these remain whole-sprite placements.
    _place_runtime_sprite(scene, HOUSE_SOURCE, (512, 440), 170)
    _place_runtime_sprite(scene, WALKWAY_SOURCE, (512, 718), 520)
    _place_runtime_sprite(scene, BUTTERFLY_SOURCE, (582, 366), 34)
    return scene


def _replace_open_view(card: Image.Image) -> Image.Image:
    """Remove the generated placeholder garden and reveal approved game art."""
    opening = _opening_mask()
    architecture = card.copy()
    architecture_alpha = np.asarray(
        architecture.getchannel("A"), dtype=np.uint8).copy()
    mask_array = np.asarray(opening, dtype=np.uint8)
    architecture_alpha[mask_array >= 128] = 0
    architecture.putalpha(Image.fromarray(architecture_alpha, "L"))

    scene = _approved_open_scene()
    clipped_scene = Image.new("RGBA", card.size, (0, 0, 0, 0))
    clipped_scene.paste(scene, (0, 0), opening)
    clipped_scene.alpha_composite(architecture)
    return clipped_scene


def _audit(card: Image.Image) -> dict[str, object]:
    alpha = np.asarray(card.getchannel("A"), dtype=np.uint8)
    corners = [
        int(alpha[0, 0]), int(alpha[0, -1]),
        int(alpha[-1, 0]), int(alpha[-1, -1]),
    ]
    if card.size != (CANVAS_EDGE, CANVAS_EDGE):
        raise ValueError(f"runtime card has wrong size: {card.size}")
    if any(corners):
        raise ValueError(f"runtime card corners are not transparent: {corners}")
    bounds = card.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("runtime card has no visible subject")
    return {
        "dimensions": list(card.size),
        "alpha_bbox": list(bounds),
        "corner_alpha": corners,
        "visible_alpha_pixels": int(np.count_nonzero(alpha)),
    }


def _approved_hall_logical() -> tuple[Image.Image, list[Path]]:
    panorama = Image.new("RGB", (7280, 2048))
    inputs: list[Path] = []
    for row in range(2):
        for column in range(8):
            path = Path(str(HALL_TILE_PATTERN).format(
                row=row, column=column))
            if not path.is_file():
                raise FileNotFoundError(path)
            tile = Image.open(path).convert("RGB")
            if tile.size != (910, 1024):
                raise ValueError(f"unexpected Main Hall tile size: {path} {tile.size}")
            panorama.paste(tile, (column * 910, row * 1024))
            inputs.append(path)
    logical = panorama.resize(HALL_LOGICAL_SIZE, Image.Resampling.LANCZOS)
    return logical.convert("RGBA"), inputs


def _build_hall_review(
        hall: Image.Image, card: Image.Image, state: str) -> Path:
    """Flatten the exact Hall placement for review only, never runtime."""
    placed = hall.copy()
    fitted = card.resize(
        (HALL_DOOR_CARD_EDGE, HALL_DOOR_CARD_EDGE),
        Image.Resampling.LANCZOS,
    )
    placed.alpha_composite(
        fitted,
        (HALL_DOOR_CENTER[0] - fitted.width // 2,
         HALL_DOOR_CENTER[1] - fitted.height // 2),
    )
    crop = placed.crop((
        HALL_REVIEW_LEFT,
        0,
        HALL_REVIEW_LEFT + HALL_REVIEW_WIDTH,
        HALL_LOGICAL_SIZE[1],
    )).resize((1280, 720), Image.Resampling.LANCZOS)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    path = REVIEW_ROOT / f"moonflower_door_{state}_hall_1280x720.png"
    crop.save(path, format="PNG", optimize=True)
    return path


def main() -> None:
    ALPHA_ROOT.mkdir(parents=True, exist_ok=True)
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    approved_hall, hall_inputs = _approved_hall_logical()
    records: dict[str, object] = {}
    for state, source_path in SOURCES.items():
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        subject, extraction = _extract_subject(Image.open(source_path))
        card = _fit_card(subject)
        if state == "open":
            card = _replace_open_view(card)
        alpha_path = ALPHA_ROOT / f"moonflower_door_{state}_alpha_master.png"
        runtime_path = RUNTIME_ROOT / f"moonflower_door_{state}.png"
        card.save(alpha_path, format="PNG", optimize=True)
        card.save(runtime_path, format="PNG", optimize=True)
        hall_review_path = _build_hall_review(approved_hall, card, state)
        audit = _audit(card)
        records[state] = {
            "raw_source": source_path.relative_to(ROOT).as_posix(),
            "raw_sha256": _hash(source_path),
            "alpha_master": alpha_path.relative_to(ROOT).as_posix(),
            "alpha_master_sha256": _hash(alpha_path),
            "runtime": runtime_path.relative_to(ROOT).as_posix(),
            "runtime_sha256": _hash(runtime_path),
            "extraction": extraction,
            "audit": audit,
            "hall_review": {
                "path": hall_review_path.relative_to(ROOT).as_posix(),
                "sha256": _hash(hall_review_path),
                "dimensions": [1280, 720],
                "delivery_pixels": False,
            },
        }
        if state == "open":
            approved_inputs = [
                *[
                    Path(str(SKY_TILE_PATTERN).format(row=row, column=column))
                    for row in range(2) for column in range(6)
                ],
                WALKWAY_SOURCE,
                HOUSE_SOURCE,
                BUTTERFLY_SOURCE,
            ]
            records[state]["approved_runtime_inputs"] = [
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": _hash(path),
                }
                for path in approved_inputs
            ]
            records[state]["view_composition"] = {
                "method": "deterministic whole-pixel composite from approved runtime art",
                "horizon_y": HORIZON_Y,
                "horizon_fraction": HORIZON_Y / CANVAS_EDGE,
                "destination": "Rainbow Stage causeway ending at the Butterfly House",
                "opening_mask": {
                    "left": OPENING_LEFT,
                    "right": OPENING_RIGHT,
                    "top": OPENING_TOP,
                    "spring": OPENING_SPRING,
                    "bottom": OPENING_BOTTOM,
                },
            }
        print(
            f"wrote {runtime_path.relative_to(ROOT)} "
            f"bbox={audit['alpha_bbox']} sha256={records[state]['runtime_sha256']}"
        )
        print(f"wrote {hall_review_path.relative_to(ROOT)}")

    manifest = {
        "schema": 1,
        "purpose": "Chapter 3 Moonflower Conservatory doorway before/after art",
        "generator": (
            "OpenAI built-in image generation for doorway architecture; "
            "deterministic approved-runtime-art composite for the open view"
        ),
        "processing": {
            "matte": "border-connected light-neutral presentation removal",
            "background_minimum_rgb": BACKGROUND_MINIMUM,
            "background_maximum_channel_spread": BACKGROUND_MAXIMUM_SPREAD,
            "matte_core_erosion_pixels": MATTE_EROSION,
            "matte_feather_radius_pixels": MATTE_FEATHER,
            "whole_subject_normalization": f"fit within {SUBJECT_EDGE}px on {CANVAS_EDGE}px RGBA canvas",
            "open_view": (
                "Sky Lagoon v5 runtime tiles plus selected Chapter 3 rainbow "
                "walkway and Butterfly House cutouts; no direct Fairy Pond view"
            ),
        },
        "hall_review_inputs": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": _hash(path),
            }
            for path in hall_inputs
        ],
        "recommended_runtime_placement": {
            "hall_logical_center": [1672.0, 385.0],
            "target_visual_height": 470.0,
            "approach_foot": [1672.0, 620.0],
            "screen_join_x": 1672.0,
            "object_role": "single whole Sprite2D card spanning the join",
        },
        "states": records,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
