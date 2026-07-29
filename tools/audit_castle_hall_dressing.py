#!/usr/bin/env python3
"""Audit the Pearl Castle Main Hall dressing and build review evidence.

The audit treats each doorway mouth, threshold, and carpet landing as one
protected rectangle. Only Main Hall-native loose decor may remain outside
those rectangles. Destination-room furniture is retained in its source room,
not exported into the hub.

The generated board is review evidence only. It does not turn the flattened
concept screens into runtime art; production still separates architecture,
doors, props, foregrounds, and characters onto Sprite3D cards.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "audit" / "castle_sprite3d"
REFERENCE_PATHS = {
    "A": AUDIT_DIR / "main_hall_screen_a_tightened_preview.png",
    "B": AUDIT_DIR / "main_hall_screen_b_tightened_preview.png",
}
CANDIDATE_PATHS = {
    "A": AUDIT_DIR / "main_hall_screen_a_cleanup_candidate.png",
    "B": AUDIT_DIR / "main_hall_screen_b_cleanup_candidate.png",
}
SCREEN_PATHS = {
    "A": AUDIT_DIR / "main_hall_screen_a_clear_preview.png",
    "B": AUDIT_DIR / "main_hall_screen_b_clear_preview.png",
}
OUTPUT_BOARD = AUDIT_DIR / "main_hall_2x1_interface_concept_clear.png"
OUTPUT_CLEARANCE = AUDIT_DIR / "main_hall_door_clearance_audit.png"
OUTPUT_INVARIANCE = AUDIT_DIR / "main_hall_dressing_invariance_audit.png"
OUTPUT_MANIFEST = AUDIT_DIR / "main_hall_prop_compatibility_audit.json"

# The ImageGen candidates restore the wall/floor behind the removed objects.
# Only these regions are composited over the original tightened screens; every
# pixel outside the feathered mask remains byte-identical to the reference.
EDIT_REGIONS = {
    "A": [
        [270, 445, 455, 685],
        [555, 445, 725, 685],
        [1470, 475, 1672, 710],
    ],
    "B": [
        [375, 205, 570, 430],
        [340, 425, 605, 700],
        [1030, 495, 1220, 710],
        [1220, 495, 1420, 710],
        [0, 590, 405, 941],
    ],
}
EDIT_MASK_FEATHER = 6

DOOR_ZONES = {
    "A": [
        {"id": "opera", "rect": [749, 438, 1029, 685]},
        {"id": "library", "rect": [1187, 442, 1360, 685]},
        {"id": "kitchen", "rect": [1383, 442, 1534, 685]},
    ],
    "B": [
        {"id": "stuffie", "rect": [198, 440, 358, 685]},
        {"id": "craft", "rect": [648, 440, 805, 685]},
        {"id": "pool", "rect": [957, 440, 1112, 685]},
        {"id": "bath", "rect": [1180, 440, 1336, 685]},
        {"id": "throne_stair", "rect": [1419, 478, 1672, 685]},
    ],
}

KEPT_HALL_DECOR = {
    "A": [
        {
            "id": "courtyard_coral_vase",
            "family": "main_hall",
            "rect": [87, 455, 173, 653],
        },
        {
            "id": "wall_bay_shell_fountain",
            "family": "main_hall",
            "rect": [420, 520, 607, 653],
        },
        {
            "id": "entry_foreground_shell_fountain",
            "family": "main_hall",
            "rect": [128, 630, 310, 900],
        },
    ],
    "B": [
        {
            "id": "throne_gallery_coral_vase_and_pearl_table",
            "family": "main_hall",
            "rect": [72, 458, 195, 652],
        },
    ],
}

REMOVED_GROUPS = [
    {
        "screen": "A",
        "group": "library_console_stool_books_and_plants",
        "source_family": "library",
        "old_location": "between courtyard column and shell fountain",
        "decision": "return_to_source_room",
    },
    {
        "screen": "A",
        "group": "loose_pool_coral_cluster",
        "source_family": "mermaid_pool",
        "old_location": "beside Opera threshold",
        "decision": "return_to_source_room",
    },
    {
        "screen": "A",
        "group": "cropped_chair_rug_tea_table_and_display",
        "source_family": "library+kitchen",
        "old_location": "beside Kitchen threshold and screen seam",
        "decision": "return_to_source_rooms",
    },
    {
        "screen": "B",
        "group": "jars_and_chimes_wall_shelf",
        "source_family": "craft_room+kitchen",
        "old_location": "above Stuffie landing",
        "decision": "return_to_source_rooms",
    },
    {
        "screen": "B",
        "group": "coral_shell_planter",
        "source_family": "mermaid_pool",
        "old_location": "between Stuffie and Craft thresholds",
        "decision": "return_to_source_room",
    },
    {
        "screen": "B",
        "group": "book_and_pearl_lamp_table",
        "source_family": "library",
        "old_location": "between Pool and Bath thresholds",
        "decision": "return_to_source_room",
    },
    {
        "screen": "B",
        "group": "purple_shell_chair",
        "source_family": "library+bubble_bath",
        "old_location": "beside Bath threshold",
        "decision": "return_to_source_rooms",
    },
    {
        "screen": "B",
        "group": "large_foreground_shell_fountain",
        "source_family": "main_hall",
        "old_location": "projected directly below Stuffie landing",
        "decision": "remove_from_screen_b_keep_screen_a_instance",
    },
    {
        "screen": "A+B",
        "group": "destination_vignette_dressing_pass",
        "source_family": (
            "opera+library+kitchen+playroom+craft_room+mermaid_pool+bubble_bath"
        ),
        "old_location": "around all destination entrances",
        "decision": "rejected_wholesale",
    },
]

FINAL_PROMPTS = {
    "A": (
        "Precise-object edit of the 1672x941 tightened Screen A. Remove the "
        "library console/stool/books/plants, loose pool coral cluster, and "
        "cropped chair/rug/tea furniture; restore only the existing wall, "
        "baseboard, and floor. Preserve all architecture, doors, signs, "
        "corridors, Roshan, carpet, and Main Hall fountains."
    ),
    "B": (
        "Precise-object edit of the 1672x941 tightened Screen B. Remove the "
        "craft/kitchen wall shelf, pool planter, library lamp table, shell "
        "chair, and the foreground fountain below the Stuffie approach; "
        "restore only the existing wall, baseboard, carpet, and floor. "
        "Preserve all architecture, doors, signs, corridors, and throne."
    ),
}

GENERATOR_PATHS = {
    "A": (
        "C:/Users/Peter/.codex/generated_images/"
        "019fa1a6-6274-77b2-bb27-38aa32e6e4dd/"
        "call_BvhJfMe0EMr7JlioBl7prWWe.png"
    ),
    "B": (
        "C:/Users/Peter/.codex/generated_images/"
        "019fa1a6-6274-77b2-bb27-38aa32e6e4dd/"
        "call_7DY51my4MF6NriHBHxdDN0KL.png"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    font_path = Path(
        "C:/Windows/Fonts/arialbd.ttf" if bold
        else "C:/Windows/Fonts/arial.ttf"
    )
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size)
    return ImageFont.load_default()


def _rect_intersects(left: list[int], right: list[int]) -> bool:
    return not (
        left[2] <= right[0]
        or right[2] <= left[0]
        or left[3] <= right[1]
        or right[3] <= left[1]
    )


def _edit_mask(size: tuple[int, int], screen: str) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    for rectangle in EDIT_REGIONS[screen]:
        draw.rectangle(tuple(rectangle), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(EDIT_MASK_FEATHER))


def _materialize_clear_screens() -> tuple[
    dict[str, Image.Image],
    dict[str, dict[str, object]],
]:
    images: dict[str, Image.Image] = {}
    metrics: dict[str, dict[str, object]] = {}
    for screen in ("A", "B"):
        reference = Image.open(REFERENCE_PATHS[screen]).convert("RGB")
        candidate = Image.open(CANDIDATE_PATHS[screen]).convert("RGB")
        if reference.size != candidate.size:
            raise ValueError(
                f"Screen {screen} candidate size {candidate.size} does not "
                f"match reference {reference.size}"
            )
        mask = _edit_mask(reference.size, screen)
        final = Image.composite(candidate, reference, mask)
        final.save(SCREEN_PATHS[screen], format="PNG", optimize=True)

        reference_pixels = np.asarray(reference, dtype=np.int16)
        final_pixels = np.asarray(final, dtype=np.int16)
        mask_pixels = np.asarray(mask, dtype=np.uint8)
        channel_delta = np.abs(final_pixels - reference_pixels)
        outside = mask_pixels == 0
        inside = mask_pixels > 0
        metrics[screen] = {
            "reference_path": str(REFERENCE_PATHS[screen].relative_to(ROOT)),
            "reference_sha256": _sha256(REFERENCE_PATHS[screen]),
            "cleanup_candidate_path": str(
                CANDIDATE_PATHS[screen].relative_to(ROOT)
            ),
            "cleanup_candidate_sha256": _sha256(CANDIDATE_PATHS[screen]),
            "edit_regions": EDIT_REGIONS[screen],
            "mask_feather_pixels": EDIT_MASK_FEATHER,
            "edited_mask_coverage": float(inside.mean()),
            "outside_mask_max_channel_delta": int(
                channel_delta[outside].max(initial=0)
            ),
            "outside_mask_pixel_exact": bool(
                np.all(channel_delta[outside] == 0)
            ),
            "inside_mask_mean_absolute_channel_delta": float(
                channel_delta[inside].mean()
            ),
        }
        images[screen] = final
    return images, metrics


def _validate(images: dict[str, Image.Image]) -> list[dict[str, object]]:
    if images["A"].size != (1672, 941) or images["B"].size != (1672, 941):
        raise ValueError(
            "Both cleared concept screens must remain exactly 1672x941"
        )

    checks: list[dict[str, object]] = []
    for screen, decor_items in KEPT_HALL_DECOR.items():
        for decor in decor_items:
            overlaps = [
                zone["id"]
                for zone in DOOR_ZONES[screen]
                if _rect_intersects(decor["rect"], zone["rect"])
            ]
            checks.append(
                {
                    "screen": screen,
                    "decor": decor["id"],
                    "family": decor["family"],
                    "door_zone_overlaps": overlaps,
                    "pass": len(overlaps) == 0,
                }
            )
    if not all(bool(check["pass"]) for check in checks):
        raise ValueError("Kept Main Hall decor overlaps a protected doorway")
    return checks


def _panel_image(image: Image.Image, width: int, height: int) -> Image.Image:
    panel = image.copy()
    panel.thumbnail((width, height), Image.Resampling.LANCZOS)
    return panel


def _draw_elevator_control(
    canvas: Image.Image,
    center: tuple[int, int],
) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y = center
    draw.ellipse(
        (x - 45 + 5, y - 45 + 7, x + 45 + 5, y + 45 + 7),
        fill="#534b86",
    )
    draw.ellipse(
        (x - 45, y - 45, x + 45, y + 45),
        fill="#76e9cc",
        outline="#51488c",
        width=4,
    )
    draw.polygon(
        [(x - 10, y - 50), (x + 10, y - 50), (x, y - 36)],
        fill="#f3c95d",
        outline="#ffffff",
    )
    label = "↕"
    font = _font(24)
    box = draw.textbbox((0, 0), label, font=font)
    draw.text(
        (x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2 - 2),
        label,
        fill="#332d70",
        font=font,
    )


def _write_review_board(images: dict[str, Image.Image]) -> None:
    canvas = Image.new("RGB", (1814, 620), "#f4f1ff")
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (18, 17),
        "SCREEN A — ENTRY GALLERY",
        fill="#302a68",
        font=_font(30, bold=True),
    )
    draw.text(
        (916, 17),
        "SCREEN B — THRONE GALLERY",
        fill="#302a68",
        font=_font(30, bold=True),
    )
    for screen, x in (("A", 18), ("B", 916)):
        panel = _panel_image(images[screen], 880, 495)
        canvas.paste(panel, (x, 74))
        _draw_elevator_control(canvas, (x + 817, 511))
    draw.text(
        (18, 588),
        (
            "CLEAR-DRESSING REVIEW — destination furniture returned to its "
            "room; entrances and carpet landings remain unobstructed"
        ),
        fill="#49417f",
        font=_font(17),
    )
    canvas.save(OUTPUT_BOARD, format="PNG", optimize=True)


def _write_clearance_board(images: dict[str, Image.Image]) -> None:
    panel_width = 810
    panel_height = 456
    header = 78
    canvas = Image.new("RGBA", (1660, 566), "#f4f1ffff")
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (18, 14),
        "PEARL CASTLE MAIN HALL — PROTECTED DOOR APPROACHES",
        fill="#302a68",
        font=_font(27, bold=True),
    )
    draw.text(
        (18, 48),
        "Green = doorway mouth + threshold + landing; no loose prop may overlap.",
        fill="#49417f",
        font=_font(17),
    )
    for screen, x in (("A", 14), ("B", 836)):
        panel = _panel_image(images[screen], panel_width, panel_height).convert(
            "RGBA"
        )
        scale_x = panel.width / images[screen].width
        scale_y = panel.height / images[screen].height
        overlay = Image.new("RGBA", panel.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        for zone in DOOR_ZONES[screen]:
            rect = zone["rect"]
            scaled = (
                int(rect[0] * scale_x),
                int(rect[1] * scale_y),
                int(rect[2] * scale_x),
                int(rect[3] * scale_y),
            )
            overlay_draw.rectangle(
                scaled,
                fill=(92, 235, 177, 58),
                outline=(24, 150, 105, 255),
                width=3,
            )
            overlay_draw.text(
                (scaled[0] + 4, scaled[1] + 4),
                str(zone["id"]).replace("_", " ").upper(),
                fill=(15, 95, 72, 255),
                font=_font(13, bold=True),
                stroke_width=2,
                stroke_fill=(244, 255, 250, 235),
            )
        panel.alpha_composite(overlay)
        canvas.alpha_composite(panel, (x, header))
    canvas.convert("RGB").save(
        OUTPUT_CLEARANCE,
        format="PNG",
        optimize=True,
    )


def _write_invariance_board(images: dict[str, Image.Image]) -> None:
    cell_width = 500
    cell_height = 282
    header = 78
    row_gap = 22
    canvas = Image.new(
        "RGB",
        (cell_width * 3 + 40, header + cell_height * 2 + row_gap + 28),
        "#f4f1ff",
    )
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (18, 12),
        "MAIN HALL CLEANUP — CONTENT INVARIANCE",
        fill="#302a68",
        font=_font(27, bold=True),
    )
    draw.text(
        (18, 47),
        (
            "Reference | final composite | amplified changed pixels "
            "(cyan outlines = permitted edit regions)"
        ),
        fill="#49417f",
        font=_font(16),
    )

    for row, screen in enumerate(("A", "B")):
        y = header + row * (cell_height + row_gap)
        reference = Image.open(REFERENCE_PATHS[screen]).convert("RGB")
        final = images[screen]
        difference = np.abs(
            np.asarray(final, dtype=np.int16)
            - np.asarray(reference, dtype=np.int16)
        ).max(axis=2)
        amplified = np.clip(difference * 6, 0, 255).astype(np.uint8)
        heat = Image.fromarray(
            np.stack(
                [
                    amplified,
                    (amplified // 5).astype(np.uint8),
                    (amplified // 8).astype(np.uint8),
                ],
                axis=2,
            ),
            mode="RGB",
        )

        panels = [reference, final, heat]
        for column, panel_source in enumerate(panels):
            panel = _panel_image(panel_source, cell_width, cell_height)
            x = 10 + column * (cell_width + 10)
            canvas.paste(panel, (x, y))
            if column == 2:
                overlay = ImageDraw.Draw(canvas)
                scale_x = panel.width / reference.width
                scale_y = panel.height / reference.height
                for rectangle in EDIT_REGIONS[screen]:
                    overlay.rectangle(
                        (
                            x + int(rectangle[0] * scale_x),
                            y + int(rectangle[1] * scale_y),
                            x + int(rectangle[2] * scale_x),
                            y + int(rectangle[3] * scale_y),
                        ),
                        outline="#56e7d1",
                        width=2,
                    )
        draw.text(
            (16, y + 8),
            f"SCREEN {screen}",
            fill="#ffffff",
            font=_font(15, bold=True),
            stroke_width=3,
            stroke_fill="#302a68",
        )
    canvas.save(OUTPUT_INVARIANCE, format="PNG", optimize=True)


def main() -> None:
    images, invariance = _materialize_clear_screens()
    placement_checks = _validate(images)
    _write_review_board(images)
    _write_clearance_board(images)
    _write_invariance_board(images)
    manifest = {
        "schema": 1,
        "purpose": (
            "Main Hall prop-family compatibility and protected doorway audit"
        ),
        "policy": {
            "hub_floor_family": "main_hall_only",
            "destination_identity": (
                "large wall-mounted symbol above the corresponding arch"
            ),
            "protected_area": (
                "door mouth + threshold + direct landing to carpet"
            ),
            "destination_room_props_in_hub": False,
            "runtime_art_contract": (
                "separate unshaded Sprite3D cards at real scene depth"
            ),
        },
        "screens": {
            screen: {
                "path": str(path.relative_to(ROOT)),
                "dimensions": list(images[screen].size),
                "sha256": _sha256(path),
                "generator_path": GENERATOR_PATHS[screen],
                "final_prompt_summary": FINAL_PROMPTS[screen],
                "runtime_status": (
                    "concept-only; native long edge is below 2048"
                ),
            }
            for screen, path in SCREEN_PATHS.items()
        },
        "content_invariance": invariance,
        "protected_door_zones": DOOR_ZONES,
        "kept_main_hall_decor": KEPT_HALL_DECOR,
        "placement_checks": placement_checks,
        "all_kept_decor_clears_door_zones": all(
            bool(check["pass"]) for check in placement_checks
        ),
        "removed_or_returned_groups": REMOVED_GROUPS,
        "review_board": {
            "path": str(OUTPUT_BOARD.relative_to(ROOT)),
            "dimensions": list(Image.open(OUTPUT_BOARD).size),
            "sha256": _sha256(OUTPUT_BOARD),
        },
        "clearance_board": {
            "path": str(OUTPUT_CLEARANCE.relative_to(ROOT)),
            "dimensions": list(Image.open(OUTPUT_CLEARANCE).size),
            "sha256": _sha256(OUTPUT_CLEARANCE),
        },
        "invariance_board": {
            "path": str(OUTPUT_INVARIANCE.relative_to(ROOT)),
            "dimensions": list(Image.open(OUTPUT_INVARIANCE).size),
            "sha256": _sha256(OUTPUT_INVARIANCE),
        },
    }
    OUTPUT_MANIFEST.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "OK: cleared screens are 1672x941; "
        f"{len(placement_checks)} kept decor groups clear all door zones"
    )
    print(f"OK: wrote {OUTPUT_BOARD.relative_to(ROOT)}")
    print(f"OK: wrote {OUTPUT_CLEARANCE.relative_to(ROOT)}")
    print(f"OK: wrote {OUTPUT_INVARIANCE.relative_to(ROOT)}")
    print(f"OK: wrote {OUTPUT_MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
