#!/usr/bin/env python3
"""Build full-resolution polished Main Hall interaction previews.

ImageGen is used only as a localized repair source for banners and door
plaques. The accepted 1672x941 clear screens remain the pixel source
everywhere else. Foreground play objects are composited from existing project
sprites and also emitted as transparent layers so the handoff can keep them
as independent unshaded Sprite3D cards.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "audit" / "castle_sprite3d"
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"

BASE_PATHS = {
    "A": AUDIT_DIR / "main_hall_screen_a_clear_preview.png",
    "B": AUDIT_DIR / "main_hall_screen_b_clear_preview.png",
}
POLISH_CANDIDATES = {
    "A": AUDIT_DIR / "main_hall_screen_a_polish_candidate.png",
    "B": AUDIT_DIR / "main_hall_screen_b_polish_candidate.png",
}
FOREGROUND_CLEANUP_CANDIDATES = {
    "A": AUDIT_DIR / "main_hall_screen_a_foreground_cleanup_candidate.png",
}
POLISHED_BASES = {
    "A": AUDIT_DIR / "main_hall_screen_a_polished_base.png",
    "B": AUDIT_DIR / "main_hall_screen_b_polished_base.png",
}
INTERACTION_LAYERS = {
    "A": AUDIT_DIR / "main_hall_screen_a_interaction_layer.png",
    "B": AUDIT_DIR / "main_hall_screen_b_interaction_layer.png",
}
FINAL_PREVIEWS = {
    "A": AUDIT_DIR / "main_hall_screen_a_fullres_play_preview.png",
    "B": AUDIT_DIR / "main_hall_screen_b_fullres_play_preview.png",
}
MANIFEST_PATH = AUDIT_DIR / "main_hall_polish_interaction_manifest.json"
AUDIT_BOARD = AUDIT_DIR / "main_hall_polish_interaction_audit.png"

FOUNTAIN_LEFT = ROOM_DIR / "room_main_hall_item_fountain_left_v2.png"
FOUNTAIN_RIGHT = ROOM_DIR / "room_main_hall_item_fountain_right_v2.png"
STAR_SOURCE = ROOT / "assets" / "mg" / "star.png"
SHADOW_SOURCE = ROOM_DIR / "room_actor_shadow.png"
PEARL_SHELL_PATH = AUDIT_DIR / "main_hall_touch_pearl_shell.png"
STAR_TOUCH_PATH = AUDIT_DIR / "main_hall_touch_wishing_star.png"

SCREEN_SIZE = (1672, 941)
MASK_FEATHER = 6

POLISH_REGIONS = {
    "A": [
        [92, 215, 220, 500],
        [430, 215, 555, 500],
        [785, 145, 990, 305],
        [1155, 295, 1360, 450],
        [1360, 295, 1555, 450],
    ],
    "B": [
        [0, 230, 92, 515],
        [325, 225, 445, 515],
        [180, 300, 380, 465],
        [625, 295, 835, 465],
        [930, 295, 1140, 465],
        [1150, 295, 1370, 465],
    ],
}

CLEANUP_REGIONS = {
    # The old large foreground fountain was baked into the concept frame.
    # Remove it inside this region only, then restore the higher-quality
    # fountain as its own interaction/depth card.
    "A": [[108, 610, 338, 930]],
}

# Positions are top-left in the 1672x941 composition space. Every object sits
# below the carpet rather than in a door mouth or threshold landing.
INTERACTIONS = {
    "A": [
        {
            "id": "fountain_play_a",
            "kind": "shell_fountain",
            "source": FOUNTAIN_LEFT,
            "position": [110, 742],
            "size": [214, 182],
            "z": 4.10,
            "hit_size": [242, 210],
            "shadow_size": [200, 50],
            "shadow_offset": [7, 146],
            "shadow_z": 4.08,
            "animation": "splash_and_pearl_bob",
            "sound": "ui_tap.ogg",
            "pitch": 1.80,
        },
        {
            "id": "wish_star_a",
            "kind": "wishing_star",
            "source": STAR_TOUCH_PATH,
            "position": [460, 810],
            "size": [112, 110],
            "z": 3.70,
            "hit_size": [144, 144],
            "shadow_size": [96, 24],
            "shadow_offset": [8, 90],
            "shadow_z": 3.68,
            "animation": "spin_glow_and_sparkle",
            "sound": "chime.ogg",
            "pitch": 1.75,
        },
        {
            "id": "pearl_chime_a",
            "kind": "pearl_shell_chime",
            "source": PEARL_SHELL_PATH,
            "position": [735, 824],
            "size": [112, 82],
            "z": 3.55,
            "hit_size": [144, 132],
            "shadow_size": [104, 26],
            "shadow_offset": [4, 64],
            "shadow_z": 3.53,
            "animation": "hop_open_and_ring",
            "sound": "chime.ogg",
            "pitch": 2.05,
        },
        {
            "id": "wish_star_opera",
            "kind": "wishing_star",
            "source": STAR_TOUCH_PATH,
            "position": [1240, 805],
            "size": [112, 110],
            "z": 3.65,
            "hit_size": [144, 144],
            "shadow_size": [96, 24],
            "shadow_offset": [8, 90],
            "shadow_z": 3.63,
            "animation": "spin_glow_and_sparkle",
            "sound": "chime.ogg",
            "pitch": 1.95,
        },
    ],
    "B": [
        {
            "id": "fountain_play_b",
            "kind": "shell_fountain",
            "source": FOUNTAIN_RIGHT,
            "position": [360, 742],
            "size": [214, 182],
            "z": 4.10,
            "hit_size": [242, 210],
            "shadow_size": [200, 50],
            "shadow_offset": [7, 146],
            "shadow_z": 4.08,
            "animation": "splash_and_pearl_bob",
            "sound": "ui_tap.ogg",
            "pitch": 1.95,
        },
        {
            "id": "wish_star_b",
            "kind": "wishing_star",
            "source": STAR_TOUCH_PATH,
            "position": [690, 810],
            "size": [112, 110],
            "z": 3.70,
            "hit_size": [144, 144],
            "shadow_size": [96, 24],
            "shadow_offset": [8, 90],
            "shadow_z": 3.68,
            "animation": "spin_glow_and_sparkle",
            "sound": "chime.ogg",
            "pitch": 1.90,
        },
        {
            "id": "pearl_chime_b",
            "kind": "pearl_shell_chime",
            "source": PEARL_SHELL_PATH,
            "position": [970, 824],
            "size": [112, 82],
            "z": 3.55,
            "hit_size": [144, 132],
            "shadow_size": [104, 26],
            "shadow_offset": [4, 64],
            "shadow_z": 3.53,
            "animation": "hop_open_and_ring",
            "sound": "chime.ogg",
            "pitch": 2.15,
        },
        {
            "id": "wish_star_throne",
            "kind": "wishing_star",
            "source": STAR_TOUCH_PATH,
            "position": [1260, 805],
            "size": [112, 110],
            "z": 3.65,
            "hit_size": [144, 144],
            "shadow_size": [96, 24],
            "shadow_offset": [8, 90],
            "shadow_z": 3.63,
            "animation": "spin_glow_and_sparkle",
            "sound": "chime.ogg",
            "pitch": 2.05,
        },
    ],
}

HUD_RECT = [1456, 710, 1638, 892]

# The world-prop layer must not overlap the HUD or any door landing.
DOOR_APPROACHES = {
    "A": [
        [749, 438, 1029, 705],
        [1187, 442, 1360, 705],
        [1383, 442, 1534, 705],
    ],
    "B": [
        [198, 440, 358, 705],
        [648, 440, 805, 705],
        [957, 440, 1112, 705],
        [1180, 440, 1336, 705],
        [1419, 478, 1672, 705],
    ],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    path = Path(
        "C:/Windows/Fonts/arialbd.ttf" if bold
        else "C:/Windows/Fonts/arial.ttf"
    )
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _rect_intersects(left: list[int], right: list[int]) -> bool:
    return not (
        left[2] <= right[0]
        or right[2] <= left[0]
        or left[3] <= right[1]
        or right[3] <= left[1]
    )


def _mask(size: tuple[int, int], regions: list[list[int]]) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    for rectangle in regions:
        draw.rectangle(tuple(rectangle), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(MASK_FEATHER))


def _candidate_canvas(
    candidate: Image.Image,
    base: Image.Image,
) -> Image.Image:
    if candidate.height != base.height:
        raise ValueError(
            f"Candidate height {candidate.height} != base height {base.height}"
        )
    if candidate.width not in (base.width, base.width - 1):
        raise ValueError(
            f"Candidate width {candidate.width} is not {base.width} or "
            f"{base.width - 1}"
        )
    canvas = base.copy()
    canvas.paste(candidate, (0, 0))
    return canvas


def _polish_bases() -> tuple[
    dict[str, Image.Image],
    dict[str, dict[str, object]],
]:
    outputs: dict[str, Image.Image] = {}
    metrics: dict[str, dict[str, object]] = {}
    for screen in ("A", "B"):
        base = Image.open(BASE_PATHS[screen]).convert("RGB")
        candidate = Image.open(POLISH_CANDIDATES[screen]).convert("RGB")
        if base.size != SCREEN_SIZE:
            raise ValueError(f"Screen {screen} base is {base.size}, not 1672x941")
        candidate_canvas = _candidate_canvas(candidate, base)
        polish_mask = _mask(base.size, POLISH_REGIONS[screen])
        output = Image.composite(candidate_canvas, base, polish_mask)

        cleanup_record: dict[str, object] | None = None
        cleanup_regions = CLEANUP_REGIONS.get(screen, [])
        if cleanup_regions:
            cleanup_path = FOREGROUND_CLEANUP_CANDIDATES[screen]
            cleanup_candidate = Image.open(cleanup_path).convert("RGB")
            cleanup_canvas = _candidate_canvas(cleanup_candidate, output)
            cleanup_mask = _mask(base.size, cleanup_regions)
            before_cleanup = output
            output = Image.composite(
                cleanup_canvas,
                before_cleanup,
                cleanup_mask,
            )
            cleanup_delta = np.abs(
                np.asarray(output, dtype=np.int16)
                - np.asarray(before_cleanup, dtype=np.int16)
            )
            cleanup_mask_pixels = np.asarray(cleanup_mask, dtype=np.uint8)
            cleanup_outside = cleanup_mask_pixels == 0
            cleanup_record = {
                "candidate": str(cleanup_path.relative_to(ROOT)),
                "candidate_dimensions": list(cleanup_candidate.size),
                "candidate_sha256": _sha256(cleanup_path),
                "regions": cleanup_regions,
                "mask_coverage": float((cleanup_mask_pixels > 0).mean()),
                "outside_mask_pixel_exact": bool(
                    np.all(cleanup_delta[cleanup_outside] == 0)
                ),
                "outside_mask_max_channel_delta": int(
                    cleanup_delta[cleanup_outside].max(initial=0)
                ),
                "replacement": (
                    "higher-quality existing Main Hall fountain emitted "
                    "as an independent Sprite3D-ready interaction card"
                ),
            }

        output.save(POLISHED_BASES[screen], format="PNG", optimize=True)

        base_pixels = np.asarray(base, dtype=np.int16)
        output_pixels = np.asarray(output, dtype=np.int16)
        mask_pixels = np.asarray(polish_mask, dtype=np.uint8)
        allowed_mask = _mask(
            base.size,
            POLISH_REGIONS[screen] + cleanup_regions,
        )
        allowed_mask_pixels = np.asarray(allowed_mask, dtype=np.uint8)
        delta = np.abs(output_pixels - base_pixels)
        outside = allowed_mask_pixels == 0
        metrics[screen] = {
            "base": str(BASE_PATHS[screen].relative_to(ROOT)),
            "base_sha256": _sha256(BASE_PATHS[screen]),
            "candidate": str(POLISH_CANDIDATES[screen].relative_to(ROOT)),
            "candidate_dimensions": list(candidate.size),
            "candidate_sha256": _sha256(POLISH_CANDIDATES[screen]),
            "regions": POLISH_REGIONS[screen],
            "polish_mask_coverage": float((mask_pixels > 0).mean()),
            "foreground_cleanup": cleanup_record,
            "total_allowed_mask_coverage": float(
                (allowed_mask_pixels > 0).mean()
            ),
            "outside_mask_pixel_exact": bool(np.all(delta[outside] == 0)),
            "outside_mask_max_channel_delta": int(delta[outside].max(initial=0)),
            "final_dimensions": list(output.size),
            "final_sha256": _sha256(POLISHED_BASES[screen]),
        }
        outputs[screen] = output
    return outputs, metrics


def _derive_touch_assets() -> None:
    fountain = Image.open(FOUNTAIN_LEFT).convert("RGBA")
    # Exact source crop: upper shell and pearl, no enlargement.
    pearl_shell = fountain.crop((55, 4, 167, 86))
    pearl_shell.save(PEARL_SHELL_PATH, format="PNG", optimize=True)

    star = Image.open(STAR_SOURCE).convert("RGBA")
    star.thumbnail((112, 110), Image.Resampling.LANCZOS)
    star.save(STAR_TOUCH_PATH, format="PNG", optimize=True)


def _draw_elevator_hud(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = HUD_RECT
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2
    radius = (right - left) // 2
    draw.ellipse(
        (left + 8, top + 10, right + 8, bottom + 10),
        fill="#51467e",
    )
    draw.ellipse(
        (left, top, right, bottom),
        fill="#76e9cc",
        outline="#51488c",
        width=6,
    )
    draw.polygon(
        [
            (center_x - 16, top - 3),
            (center_x + 16, top - 3),
            (center_x, top + 21),
        ],
        fill="#f3c95d",
        outline="#ffffff",
    )
    label = "↕"
    font = _font(42)
    bounds = draw.textbbox((0, 0), label, font=font)
    draw.text(
        (
            center_x - (bounds[2] - bounds[0]) / 2,
            center_y - (bounds[3] - bounds[1]) / 2 - 3,
        ),
        label,
        fill="#332d70",
        font=font,
    )


def _compose_interactions(
    polished: dict[str, Image.Image],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for screen in ("A", "B"):
        layer = Image.new("RGBA", SCREEN_SIZE, (0, 0, 0, 0))
        for item in INTERACTIONS[screen]:
            position = tuple(item["position"])
            shadow = Image.open(SHADOW_SOURCE).convert("RGBA")
            shadow = shadow.resize(
                tuple(item["shadow_size"]),
                Image.Resampling.LANCZOS,
            )
            shadow_position = (
                position[0] + item["shadow_offset"][0],
                position[1] + item["shadow_offset"][1],
            )
            layer.alpha_composite(shadow, shadow_position)

            source = Image.open(Path(item["source"])).convert("RGBA")
            target_size = tuple(item["size"])
            if source.size != target_size:
                source = source.resize(target_size, Image.Resampling.LANCZOS)
            layer.alpha_composite(source, position)
            rectangle = [
                position[0],
                position[1],
                position[0] + target_size[0],
                position[1] + target_size[1],
            ]
            approach_overlaps = [
                index
                for index, approach in enumerate(DOOR_APPROACHES[screen])
                if _rect_intersects(rectangle, approach)
            ]
            hud_overlap = _rect_intersects(rectangle, HUD_RECT)
            if approach_overlaps or hud_overlap:
                raise ValueError(
                    f"{item['id']} overlaps approaches {approach_overlaps} "
                    f"or HUD={hud_overlap}"
                )
            records.append(
                {
                    **{
                        key: (
                            str(value.relative_to(ROOT))
                            if isinstance(value, Path)
                            else value
                        )
                        for key, value in item.items()
                    },
                    "screen": screen,
                    "rectangle": rectangle,
                    "world_node_type": "unshaded Sprite3D",
                    "shadow_source": str(SHADOW_SOURCE.relative_to(ROOT)),
                    "shadow_position": list(shadow_position),
                    "shadow_node_type": "unshaded Sprite3D",
                    "door_approach_overlaps": approach_overlaps,
                    "hud_overlap": hud_overlap,
                    "pass": True,
                }
            )
        layer.save(INTERACTION_LAYERS[screen], format="PNG", optimize=True)
        final = polished[screen].convert("RGBA")
        final.alpha_composite(layer)
        final_rgb = final.convert("RGB")
        _draw_elevator_hud(final_rgb)
        final_rgb.save(FINAL_PREVIEWS[screen], format="PNG", optimize=True)
    return records


def _write_audit_board() -> None:
    canvas = Image.new("RGB", (1660, 565), "#f4f1ff")
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (18, 14),
        "PEARL CASTLE MAIN HALL — FULL-RES POLISH + PLAY LAYER",
        fill="#302a68",
        font=_font(27, bold=True),
    )
    draw.text(
        (18, 49),
        (
            "Uniform crests and plaques; reused Sprite3D-ready play objects "
            "occupy the foreground without blocking doors or elevator."
        ),
        fill="#49417f",
        font=_font(16),
    )
    for column, screen in enumerate(("A", "B")):
        image = Image.open(FINAL_PREVIEWS[screen]).convert("RGB")
        image.thumbnail((810, 456), Image.Resampling.LANCZOS)
        x = 14 + column * 822
        y = 82
        canvas.paste(image, (x, y))
        draw.text(
            (x + 12, y + 12),
            f"SCREEN {screen} — 1672×941 SOURCE",
            fill="#ffffff",
            font=_font(18, bold=True),
            stroke_width=3,
            stroke_fill="#302a68",
        )
    canvas.save(AUDIT_BOARD, format="PNG", optimize=True)


def main() -> None:
    _derive_touch_assets()
    polished, invariance = _polish_bases()
    interaction_records = _compose_interactions(polished)
    _write_audit_board()
    manifest = {
        "schema": 1,
        "purpose": (
            "Full-resolution Main Hall polish and child interaction handoff"
        ),
        "screen_dimensions": list(SCREEN_SIZE),
        "resolution_changed": False,
        "polish_policy": {
            "banner_crest": (
                "identical open white shell + one pearl + three aqua waves"
            ),
            "standard_door_plaque": (
                "cream scalloped medallion, gold rim, thick navy outline"
            ),
            "opera_exception": "same language on one wider masks plaque",
            "imagegen_pixels_outside_masks": "preserved exactly",
        },
        "polish_invariance": invariance,
        "interaction_policy": {
            "source_art": "existing project sprites only",
            "world_node_type": "unshaded Sprite3D",
            "hud_node_type": "Control",
            "no_reading_required": True,
            "minimum_visual_hit_size": [132, 132],
            "door_approach_overlap_allowed": False,
            "elevator_hud_overlap_allowed": False,
        },
        "node_type_inventory": {
            "touchable_world_prop_cards": {
                "count": len(interaction_records),
                "type": "unshaded Sprite3D",
            },
            "contact_shadow_cards": {
                "count": len(interaction_records),
                "type": "unshaded Sprite3D",
            },
            "elevator_hud": {
                "count": 1,
                "type": "Control",
                "reuse": "same omnipresent instance in both camera views",
            },
            "nonconforming_new_world_nodes": {
                "count": 0,
                "types": [
                    "Sprite2D",
                    "AnimatedSprite2D",
                    "TextureRect",
                    "Polygon2D",
                    "custom CanvasItem drawing",
                    "model",
                    "GLB",
                    "procedural mesh",
                ],
            },
        },
        "runtime_eligibility": {
            "accepted": False,
            "reason": (
                "background composition references remain 1672x941 and "
                "must not feed runtime before native exact-ratio long edge "
                "is at least 2048"
            ),
            "minimum_native_background_dimensions": [2048, 1153],
            "interaction_cards_ready_for_depth_reconstruction": True,
        },
        "interactions": interaction_records,
        "derived_touch_assets": {
            "pearl_shell": {
                "path": str(PEARL_SHELL_PATH.relative_to(ROOT)),
                "dimensions": list(Image.open(PEARL_SHELL_PATH).size),
                "sha256": _sha256(PEARL_SHELL_PATH),
                "derivation": (
                    "exact crop (55,4,167,86) from "
                    "room_main_hall_item_fountain_left_v2.png"
                ),
            },
            "wishing_star": {
                "path": str(STAR_TOUCH_PATH.relative_to(ROOT)),
                "dimensions": list(Image.open(STAR_TOUCH_PATH).size),
                "sha256": _sha256(STAR_TOUCH_PATH),
                "derivation": (
                    "single high-quality downsample from assets/mg/star.png"
                ),
            },
        },
        "outputs": {
            screen: {
                "polished_base": str(POLISHED_BASES[screen].relative_to(ROOT)),
                "interaction_layer": str(
                    INTERACTION_LAYERS[screen].relative_to(ROOT)
                ),
                "fullres_preview": str(
                    FINAL_PREVIEWS[screen].relative_to(ROOT)
                ),
                "dimensions": list(Image.open(FINAL_PREVIEWS[screen]).size),
                "sha256": _sha256(FINAL_PREVIEWS[screen]),
            }
            for screen in ("A", "B")
        },
        "audit_board": {
            "path": str(AUDIT_BOARD.relative_to(ROOT)),
            "dimensions": list(Image.open(AUDIT_BOARD).size),
            "sha256": _sha256(AUDIT_BOARD),
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print("OK: full-resolution polished bases remain 1672x941")
    print(
        f"OK: {len(interaction_records)} interaction cards clear every "
        "door approach and the elevator HUD"
    )
    print(f"OK: wrote {AUDIT_BOARD.relative_to(ROOT)}")
    print(f"OK: wrote {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
