#!/usr/bin/env python3
"""Build the room-led Main Hall comparison board and machine audit.

This tool creates review evidence only. It never writes runtime art and never
rescales a source for use by the game.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from statistics import fmean

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit" / "castle_sprite3d"
OUT_BOARD = AUDIT / "castle_room_led_reference_board.png"
OUT_JSON = AUDIT / "castle_room_led_visual_audit.json"

ROOMS = [
    ("Royal Kitchen", ROOT / "assets/flats/castle/rooms/room_kitchen.png"),
    ("Royal Library", ROOT / "assets/flats/castle/rooms/room_library.png"),
    ("Stuffie Playroom", ROOT / "assets/flats/castle/rooms/room_playroom.png"),
    ("Craft Room", ROOT / "assets/flats/castle/rooms/room_craft_room.png"),
    ("Mermaid Pool", ROOT / "assets/flats/castle/rooms/room_mermaid_pool.png"),
    ("Bubble Bath", ROOT / "assets/flats/castle/rooms/room_bubble_bath.png"),
]

HALLS = [
    (
        "Screen A — topology valid, visual finish rejected",
        AUDIT / "main_hall_screen_a_fullres_play_preview.png",
    ),
    (
        "Screen B — topology valid, visual finish rejected",
        AUDIT / "main_hall_screen_b_fullres_play_preview.png",
    ),
]

PAPER = (246, 243, 255)
INK = (44, 38, 92)
MUTED = (96, 86, 132)
GOLD = (222, 170, 68)
TEAL = (63, 184, 187)
CORAL = (232, 126, 139)
PLUM = (83, 49, 112)
GOOD = (66, 153, 121)
BAD = (190, 72, 87)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for name in names:
        candidate = Path("C:/Windows/Fonts") / name
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def fit_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    face: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int = 6,
) -> int:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        trial = word if not line else f"{line} {word}"
        if draw.textbbox((0, 0), trial, font=face)[2] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    x, y = xy
    height = draw.textbbox((0, 0), "Ag", font=face)[3]
    for part in lines:
        draw.text((x, y), part, font=face, fill=fill)
        y += height + line_gap
    return y


def metrics(path: Path) -> dict[str, object]:
    with Image.open(path) as source:
        rgb = source.convert("RGB")
        sample = rgb.resize((256, 144), Image.Resampling.LANCZOS)
        hsv = sample.convert("HSV")
        lum = sample.convert("L")
        hist = lum.histogram()
        count = sum(hist)

        def percentile(fraction: float) -> int:
            target = count * fraction
            running = 0
            for value, amount in enumerate(hist):
                running += amount
                if running >= target:
                    return value
            return 255

        sat_mean = ImageStat.Stat(hsv).mean[1] / 255.0
        luma_p10 = percentile(0.10)
        luma_p90 = percentile(0.90)
        colors = sample.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
        palette = colors.getpalette() or []
        dominant: list[dict[str, object]] = []
        for amount, index in sorted(colors.getcolors() or [], reverse=True):
            offset = index * 3
            color = tuple(palette[offset : offset + 3])
            dominant.append(
                {
                    "rgb": color,
                    "hex": "#%02x%02x%02x" % color,
                    "share": round(amount / (256 * 144), 4),
                }
            )
        probabilities = [amount / count for amount in hist if amount]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        return {
            "path": path.relative_to(ROOT).as_posix(),
            "width": rgb.width,
            "height": rgb.height,
            "aspect_ratio": round(rgb.width / rgb.height, 9),
            "sha256": sha256(path),
            "mean_saturation": round(sat_mean, 4),
            "luma_p10": luma_p10,
            "luma_p90": luma_p90,
            "luma_span_p10_p90": luma_p90 - luma_p10,
            "luma_entropy_bits": round(entropy, 4),
            "dominant_colors": dominant,
        }


def palette_from_rooms() -> list[tuple[int, int, int]]:
    swatches: list[tuple[int, int, int]] = []
    for _, path in ROOMS:
        with Image.open(path) as source:
            reduced = source.convert("RGB").resize((160, 90), Image.Resampling.LANCZOS)
            quantized = reduced.quantize(colors=6, method=Image.Quantize.MEDIANCUT)
            palette = quantized.getpalette() or []
            for amount, index in sorted(quantized.getcolors() or [], reverse=True)[:3]:
                if amount < 240:
                    continue
                offset = index * 3
                color = tuple(palette[offset : offset + 3])
                if all(sum(abs(a - b) for a, b in zip(color, prior)) > 55 for prior in swatches):
                    swatches.append(color)
    return swatches[:12]


def build_board() -> None:
    width, height = 2400, 2050
    canvas = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(canvas)
    title = font(54, bold=True)
    h2 = font(30, bold=True)
    label = font(23, bold=True)
    body = font(21)
    small = font(18)

    draw.text((54, 35), "Pearl Castle — room-led Main Hall intervention", font=title, fill=INK)
    draw.text(
        (56, 103),
        "Primary reference: the Castle rooms. Secondary lesson: Sky Lagoon/Northern depth rhythm. Blueprint only — no new runtime art.",
        font=body,
        fill=MUTED,
    )

    draw.text((54, 150), "1. Castle-native visual language", font=h2, fill=INK)
    cell_w, cell_h = 370, 208
    gap = 18
    start_x, y = 54, 200
    for index, (name, path) in enumerate(ROOMS):
        x = start_x + index * (cell_w + gap)
        with Image.open(path) as image:
            preview = fit_cover(image, (cell_w, cell_h))
        canvas.paste(preview, (x, y))
        draw.rounded_rectangle((x, y, x + cell_w, y + cell_h), radius=12, outline=INK, width=4)
        draw.rectangle((x, y + cell_h - 38, x + cell_w, y + cell_h), fill=(30, 25, 63))
        draw.text((x + 12, y + cell_h - 33), name, font=label, fill=(255, 255, 255))

    swatches = palette_from_rooms()
    draw.text((54, 430), "Shared room palette", font=label, fill=INK)
    sx = 270
    for color in swatches:
        draw.rounded_rectangle((sx, 425, sx + 112, 466), radius=8, fill=color, outline=(255, 255, 255), width=2)
        sx += 124

    draw.text((54, 500), "2. Current two-screen hub — keep navigation, replace visual hierarchy", font=h2, fill=INK)
    hall_w, hall_h = 1128, 635
    hall_y = 550
    for index, (name, path) in enumerate(HALLS):
        x = 54 + index * 1164
        with Image.open(path) as image:
            preview = fit_cover(image, (hall_w, hall_h))
        canvas.paste(preview, (x, hall_y))
        draw.rounded_rectangle((x, hall_y, x + hall_w, hall_y + hall_h), radius=12, outline=BAD, width=5)
        draw.rectangle((x, hall_y, x + hall_w, hall_y + 42), fill=(92, 39, 66))
        draw.text((x + 14, hall_y + 8), name, font=label, fill=(255, 245, 249))

        overlay = Image.new("RGBA", (hall_w, hall_h), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle((0, 42, hall_w, 435), fill=(*PLUM, 34), outline=(*PLUM, 180), width=4)
        od.rectangle((0, 435, hall_w, 525), fill=(*TEAL, 38), outline=(*TEAL, 190), width=4)
        od.rectangle((0, 525, hall_w, hall_h), fill=(*CORAL, 42), outline=(*CORAL, 190), width=4)
        od.text((16, 54), "FAR: window / niche / textile bays", font=small, fill=(*PLUM, 255))
        od.text((16, 445), "PLAYER: carpet + clear thresholds", font=small, fill=(20, 92, 92, 255))
        od.text((16, 535), "NEAR: 2–3 clustered activity islands", font=small, fill=(121, 35, 57, 255))
        canvas.paste(overlay, (x, hall_y), overlay)

    lower_y = 1225
    draw.text((54, lower_y), "3. Room-led correction", font=h2, fill=INK)

    boxes = [
        (
            "Architecture",
            "Alternate aqua shell windows, deep plum pearl niches, and Opera/Craft textile-light bays. Brick becomes support, not the whole room.",
            TEAL,
        ),
        (
            "Depth",
            "Far wall/window cards, scenic-middle fixtures, the player/door plane, and near interaction islands must occupy real Z and show parallax/occlusion.",
            PLUM,
        ),
        (
            "Foreground",
            "Replace the evenly spaced star row with asymmetric families: fountain + bubbles + bunny; cloud seat + sleepy bunny; shell sound toy + response effects.",
            CORAL,
        ),
        (
            "Continuity",
            "Screen A stays ceremonial; Screen B grows warmer and culminates at the unchanged far-right throne. Door order and protected approaches do not move.",
            GOLD,
        ),
    ]
    box_w, box_h = 554, 250
    for index, (heading, copy, accent) in enumerate(boxes):
        x = 54 + index * (box_w + 26)
        y0 = lower_y + 58
        draw.rounded_rectangle((x, y0, x + box_w, y0 + box_h), radius=18, fill=(255, 255, 255), outline=accent, width=5)
        draw.text((x + 24, y0 + 20), heading, font=label, fill=INK)
        draw_wrapped(draw, (x + 24, y0 + 64), copy, body, MUTED, box_w - 48, line_gap=8)

    draw.text((54, 1572), "4. Reuse first", font=h2, fill=INK)
    reuse = [
        ("USE NOW", "Current room layers, Main Hall throne/fountains/doors/columns, approved signs and shell lighting.", GOOD),
        ("USE SELECTIVELY", "Recent day-one dust bunnies and sparkle/bubble response effects; cleanup tools only during cleanup play.", GOLD),
        ("HOLD", "Uncommitted illustrated skins in the dirty-castle worktree until clean provenance and the 4.5/5 Sprite3D audit pass.", BAD),
    ]
    y0 = 1630
    for heading, copy, accent in reuse:
        draw.rounded_rectangle((54, y0, 2346, y0 + 92), radius=16, fill=(255, 255, 255), outline=accent, width=4)
        draw.text((78, y0 + 20), heading, font=label, fill=accent)
        draw_wrapped(draw, (330, y0 + 19), copy, body, INK, 1960, line_gap=4)
        y0 += 108

    draw.rounded_rectangle((54, 1960, 2346, 2020), radius=14, fill=INK)
    draw.text(
        (78, 1974),
        "Acceptance: exact 1672:941 composition ratio • native long edge ≥2048 • lossless ≤1024 tiles • Sprite3D-only world • zero entrance obstruction",
        font=body,
        fill=(255, 255, 255),
    )

    AUDIT.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_BOARD, optimize=True)


def build_audit() -> None:
    room_metrics = [metrics(path) | {"label": label} for label, path in ROOMS]
    hall_metrics = [metrics(path) | {"label": label} for label, path in HALLS]
    report = {
        "schema": "castle-room-led-visual-audit-v1",
        "date": "2026-07-28",
        "decision": {
            "topology": "retain current two-screen hub",
            "visual_finish": "current hall previews rejected; room-led intervention required",
            "primary_reference": "current Castle room composites",
            "secondary_reference": "Sky Lagoon and Northern composition/depth techniques only",
            "new_runtime_art_created": False,
        },
        "rooms": room_metrics,
        "current_halls": hall_metrics,
        "room_aggregate": {
            "mean_saturation": round(fmean(item["mean_saturation"] for item in room_metrics), 4),
            "mean_luma_span_p10_p90": round(fmean(item["luma_span_p10_p90"] for item in room_metrics), 2),
            "mean_luma_entropy_bits": round(fmean(item["luma_entropy_bits"] for item in room_metrics), 4),
        },
        "hall_aggregate": {
            "mean_saturation": round(fmean(item["mean_saturation"] for item in hall_metrics), 4),
            "mean_luma_span_p10_p90": round(fmean(item["luma_span_p10_p90"] for item in hall_metrics), 2),
            "mean_luma_entropy_bits": round(fmean(item["luma_entropy_bits"] for item in hall_metrics), 4),
        },
        "reuse_sources": {
            "active_room_layers": "assets/flats/castle/rooms/",
            "recent_day_one_commit": "95132b6b310c34aa1d7fba5330d72f36fed9d4d7",
            "recent_day_one_branch": "codex/day-one-opening-final",
            "dirty_skin_candidate_commit": "6d8aa7a9b165e5fda2c4d335d52613fc80da0e16",
            "dirty_skin_status": "hold: worktree has uncommitted illustrated skins",
        },
        "board": {
            "path": OUT_BOARD.relative_to(ROOT).as_posix(),
            "sha256": sha256(OUT_BOARD),
            "width": 2400,
            "height": 2050,
            "runtime_asset": False,
        },
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_board()
    build_audit()
    print(OUT_BOARD)
    print(OUT_JSON)
