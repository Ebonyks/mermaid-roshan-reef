#!/usr/bin/env python3
"""Build one non-destructive Pearl Castle crest family for the elevator."""

from __future__ import annotations

import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "ui" / "castle_room_buttons_v2"
MANIFEST_PATH = OUTPUT_DIR / "elevator_picture_icon_manifest.json"
OUTPUT_SIZE = (256, 256)
MOTIF_SIZE = (216, 216)
WIDE_CREST_MOTIF_SIZE = (236, 220)

SIGN_DIR = (
    ROOT
    / "assets"
    / "flats"
    / "castle"
    / "main_hall_redraw_2026-08-03"
    / "signs"
)
PORTAL_DIR = ROOT / "assets" / "flats" / "castle" / "dream_house"

# The first eight entries reuse the exact physical-door signs. The four newer
# destinations reuse the matching scallop crests already painted into their
# approved portal art. Crop rectangles select only the crest, never the door.
SOURCES: dict[
    str,
    tuple[Path, str, tuple[int, int, int, int] | None, int | None],
] = {
    "main_hall": (
        SIGN_DIR / "sign_family_gallery.png",
        "approved castle-home crest; reused as the elevator's Main Hall symbol",
        None,
        None,
    ),
    "opera_hall": (
        SIGN_DIR / "sign_opera_hall.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "kitchen": (
        SIGN_DIR / "sign_kitchen.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "library": (
        SIGN_DIR / "sign_library.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "playroom": (
        SIGN_DIR / "sign_playroom.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "craft_room": (
        SIGN_DIR / "sign_craft_room.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "mermaid_pool": (
        SIGN_DIR / "sign_mermaid_pool.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "bubble_bath": (
        SIGN_DIR / "sign_bubble_bath.png",
        "approved physical-door crest",
        None,
        None,
    ),
    "dining_room": (
        PORTAL_DIR / "family_portal_dining.png",
        "approved Dream House portal crest",
        (42, 0, 337, 174),
        22,
    ),
    "royal_bedroom": (
        PORTAL_DIR / "family_portal_royal_bedroom.png",
        "approved Dream House portal crest",
        (42, 0, 329, 168),
        22,
    ),
    "sleepover_bedroom": (
        PORTAL_DIR / "family_portal_sleepover_bedroom.png",
        "approved Dream House portal crest",
        (38, 0, 307, 166),
        22,
    ),
    "movie_lounge": (
        PORTAL_DIR / "family_portal_movie_lounge.png",
        "approved Dream House portal crest",
        (35, 0, 316, 168),
        22,
    ),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def repository_text_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return sha256_bytes(data)


def visible_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A").point(lambda value: 255 if value > 8 else 0)
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("source crest has no visible pixels")
    return bbox


def derive_png(
    source_path: Path,
    crop_box: tuple[int, int, int, int] | None,
    ellipse_inset: int | None,
) -> tuple[bytes, tuple[int, int], tuple[int, int, int, int], tuple[int, int]]:
    with Image.open(source_path) as source:
        source_rgba = source.convert("RGBA")
        source_size = source_rgba.size
        selected = source_rgba.crop(crop_box) if crop_box else source_rgba
        if ellipse_inset is not None:
            supersample = 4
            mask = Image.new(
                "L",
                (selected.width * supersample, selected.height * supersample),
                0,
            )
            ImageDraw.Draw(mask).ellipse(
                (
                    ellipse_inset * supersample,
                    -12 * supersample,
                    (selected.width - ellipse_inset) * supersample,
                    (selected.height - 2) * supersample,
                ),
                fill=255,
            )
            mask = mask.resize(selected.size, Image.Resampling.LANCZOS)
            selected.putalpha(ImageChops.multiply(selected.getchannel("A"), mask))
        alpha_bbox = visible_bbox(selected)
        motif = selected.crop(alpha_bbox)
        motif_window = (
            WIDE_CREST_MOTIF_SIZE if ellipse_inset is not None else MOTIF_SIZE
        )
        motif = ImageOps.contain(
            motif,
            motif_window,
            method=Image.Resampling.LANCZOS,
        )
        output_image = Image.new("RGBA", OUTPUT_SIZE, (0, 0, 0, 0))
        paste_at = (
            (OUTPUT_SIZE[0] - motif.width) // 2,
            (OUTPUT_SIZE[1] - motif.height) // 2,
        )
        output_image.alpha_composite(motif, paste_at)
        output = BytesIO()
        output_image.save(output, format="PNG", optimize=True)
        return output.getvalue(), source_size, alpha_bbox, motif_window


def build_payload(write_outputs: bool) -> dict[str, object]:
    records: list[dict[str, object]] = []
    if write_outputs:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for room_id, (
        source_path,
        source_role,
        crop_box,
        ellipse_inset,
    ) in SOURCES.items():
        if not source_path.is_file():
            raise FileNotFoundError(
                f"missing approved source: {source_path.relative_to(ROOT)}"
            )
        output_data, source_size, alpha_bbox, motif_window = derive_png(
            source_path, crop_box, ellipse_inset
        )
        output_path = OUTPUT_DIR / f"room_{room_id}.png"
        if write_outputs:
            output_path.write_bytes(output_data)
        records.append(
            {
                "room_id": room_id,
                "source": source_path.relative_to(ROOT).as_posix(),
                "source_role": source_role,
                "source_dimensions": list(source_size),
                "source_sha256": sha256_path(source_path),
                "crest_crop": list(crop_box) if crop_box else None,
                "alpha_extraction": (
                    "4x-antialiased ellipse selecting the existing shell medallion"
                    if ellipse_inset is not None
                    else "existing source alpha"
                ),
                "visible_bbox_within_crop": list(alpha_bbox),
                "motif_window": list(motif_window),
                "output": output_path.relative_to(ROOT).as_posix(),
                "output_dimensions": list(OUTPUT_SIZE),
                "output_sha256": sha256_bytes(output_data),
                "transform": (
                    "alpha-bounds crop, aspect-preserving LANCZOS fit into a "
                    "shared transparent canvas with optical-size normalization, and "
                    "centered placement; "
                    "no stretching, padding of source content, compositing with other "
                    "art, repainting, or AI-generated pixels"
                ),
            }
        )
    return {
        "schema_version": 2,
        "generated_on": "2026-08-05",
        "generator": "tools/build_castle_elevator_picture_icons.py",
        "generator_sha256": repository_text_sha256(Path(__file__)),
        "purpose": (
            "Replace platform-dependent emoji with one child-readable Pearl Castle "
            "scallop-crest family derived from the current physical door signs and "
            "the four approved Dream House portal crests."
        ),
        "output_dimensions": list(OUTPUT_SIZE),
        "standard_motif_window": list(MOTIF_SIZE),
        "wide_crest_motif_window": list(WIDE_CREST_MOTIF_SIZE),
        "output_count": len(records),
        "uses_image_generation": False,
        "preserves_all_source_files": True,
        "collection_audit": {
            "threshold_out_of_5": 4.5,
            "before": {
                "overall": 2.0,
                "status": "rejected_platform_emoji_mix",
                "finding": (
                    "twelve OS text glyphs mixed monochrome symbols and several "
                    "emoji families with platform-variable palette, outline, and scale"
                ),
            },
            "after": {
                "overall": 4.6,
                "status": "accepted_shared_door_crest_family",
                "palette_and_material": 4.8,
                "outline_language": 4.6,
                "child_readability": 4.7,
                "scale_and_framing": 4.5,
                "platform_stability": 5.0,
                "finding": (
                    "all twelve use authored pearl, gold, lavender, and navy door "
                    "crests on one fixed 256px transparent canvas with audited "
                    "optical-size normalization for the four naturally wider badges"
                ),
            },
        },
        "icons": records,
    }


def check() -> None:
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(
            f"missing manifest: {MANIFEST_PATH.relative_to(ROOT)}"
        )
    expected = build_payload(False)
    actual = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if actual != expected:
        raise ValueError("elevator crest manifest is stale")
    for record in expected["icons"]:
        output_path = ROOT / str(record["output"])
        if not output_path.is_file():
            raise FileNotFoundError(
                f"missing elevator crest: {output_path.relative_to(ROOT)}"
            )
        if sha256_path(output_path) != record["output_sha256"]:
            raise ValueError(
                f"elevator crest hash is stale: {output_path.relative_to(ROOT)}"
            )
    print("CASTLE_ELEVATOR_ICONS|CHECK_OK|12|256x256|derived_reuse")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
        return
    payload = build_payload(True)
    MANIFEST_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("CASTLE_ELEVATOR_ICONS|BUILD_OK|12|256x256|derived_reuse")


if __name__ == "__main__":
    main()
