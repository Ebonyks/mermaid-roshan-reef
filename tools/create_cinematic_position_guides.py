#!/usr/bin/env python3
"""Create disposable position-only guides for full-frame image regeneration.

The outputs are never cinematic frames. They deliberately discard source color,
lighting, texture, internal detail, and scene background, retaining only a flat
subject footprint and position marks on a neutral field. The destination must
be under a directory named ``build`` so guide artifacts cannot be mistaken for
runtime art.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


GUIDE_COLOR = (0, 255, 110)
BACKGROUND_COLOR = (35, 28, 58)
LABEL = "POSITION_GUIDE_ONLY"


def parse_pair(value: str) -> tuple[float, float]:
    try:
        first, second = value.split(",", 1)
        result = (float(first), float(second))
    except (AttributeError, ValueError) as error:
        raise argparse.ArgumentTypeError("expected X,Y") from error
    if any(component < 0.0 or component > 1.0 for component in result):
        raise argparse.ArgumentTypeError("normalized coordinates must be in [0, 1]")
    return result


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = (int(component) for component in value.lower().split("x", 1))
    except (AttributeError, ValueError) as error:
        raise argparse.ArgumentTypeError("expected WIDTHxHEIGHT") from error
    if width < 2 or height < 2:
        raise argparse.ArgumentTypeError("dimensions must be at least 2")
    return width, height


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lerp(left: float, right: float, fraction: float) -> float:
    return left + (right - left) * fraction


def render_guides(
    source: Path,
    output: Path,
    frame_count: int,
    size: tuple[int, int],
    start_center: tuple[float, float],
    end_center: tuple[float, float],
    occupancy_width: float,
    guide_mode: str = "chroma_footprint",
) -> dict[str, object]:
    if "build" not in {part.lower() for part in output.resolve().parts}:
        raise ValueError("position guides must stay under an ignored build directory")
    if guide_mode not in {"chroma_footprint", "bounding_box", "marker_only"}:
        raise ValueError(f"unsupported guide mode: {guide_mode}")
    output.mkdir(parents=True, exist_ok=False)
    guide_dir = output / "guides"
    mask_dir = output / "masks"
    guide_dir.mkdir()
    mask_dir.mkdir()

    with Image.open(source).convert("RGBA") as opened:
        source_alpha = opened.getchannel("A")
        bounds = source_alpha.getbbox()
        if bounds is None:
            raise ValueError("source has no visible alpha")
        source_alpha = source_alpha.crop(bounds)

    target_width = round(size[0] * occupancy_width)
    target_height = round(target_width * source_alpha.height / source_alpha.width)
    subject_mask = source_alpha.resize((target_width, target_height), Image.Resampling.LANCZOS)
    subject_mask = subject_mask.point(lambda value: 255 if value >= 32 else 0)
    flat_subject = Image.new("RGB", subject_mask.size, GUIDE_COLOR)
    font = ImageFont.load_default()
    records: list[dict[str, object]] = []
    previous_mask: Image.Image | None = None
    previous_leading_edge: int | None = None
    previous_visible_box: tuple[int, int, int, int] | None = None

    for frame in range(frame_count):
        fraction = frame / (frame_count - 1) if frame_count > 1 else 0.0
        center = (
            lerp(start_center[0], end_center[0], fraction),
            lerp(start_center[1], end_center[1], fraction),
        )
        center_pixels = (round(center[0] * size[0]), round(center[1] * size[1]))
        left = center_pixels[0] - target_width // 2
        top = center_pixels[1] - target_height // 2

        mask = Image.new("L", size, 0)
        mask.paste(subject_mask, (left, top))
        mask_path = mask_dir / f"frame_{frame:06d}_mask.png"
        mask.save(mask_path, optimize=True)

        # A neutral field is mandatory. Supplying a scene plate here would give
        # the generator visual authority beyond the sole owner-approved
        # exception: subject position.
        guide = Image.new("RGB", size, BACKGROUND_COLOR)
        if guide_mode == "chroma_footprint":
            guide.paste(flat_subject, (left, top), subject_mask)
        draw = ImageDraw.Draw(guide)
        if previous_mask is not None and guide_mode == "chroma_footprint":
            expanded = previous_mask.filter(ImageFilter.MaxFilter(9))
            contracted = previous_mask.filter(ImageFilter.MinFilter(9))
            previous_outline = ImageChops.subtract(expanded, contracted)
            guide.paste(
                Image.new("RGB", size, (255, 35, 95)),
                (0, 0),
                previous_outline,
            )
            draw = ImageDraw.Draw(guide)
        visible_box = (
            max(0, left),
            max(0, top),
            min(size[0] - 1, left + target_width - 1),
            min(size[1] - 1, top + target_height - 1),
        )
        if guide_mode == "chroma_footprint":
            draw.rectangle(visible_box, outline=(255, 255, 255), width=2)
        elif guide_mode == "bounding_box":
            if previous_visible_box is not None:
                draw.rectangle(
                    previous_visible_box,
                    outline=(255, 35, 95),
                    width=4,
                )
            draw.rectangle(visible_box, outline=GUIDE_COLOR, width=4)
        leading_edge = min(size[0] - 1, left + target_width - 1)
        draw.line(
            (leading_edge, 0, leading_edge, size[1] - 1),
            fill=(255, 220, 0),
            width=3,
        )
        if previous_leading_edge is not None and guide_mode == "chroma_footprint":
            draw.line(
                (
                    previous_leading_edge,
                    0,
                    previous_leading_edge,
                    size[1] - 1,
                ),
                fill=(255, 35, 95),
                width=2,
            )
            arrow_y = 92
            draw.line(
                (
                    previous_leading_edge,
                    arrow_y,
                    leading_edge,
                    arrow_y,
                ),
                fill=(255, 255, 255),
                width=3,
            )
            draw.polygon(
                (
                    (leading_edge, arrow_y),
                    (leading_edge - 10, arrow_y - 7),
                    (leading_edge - 10, arrow_y + 7),
                ),
                fill=(255, 255, 255),
            )
        cross_radius = 14
        cross_x = leading_edge if guide_mode == "marker_only" else center_pixels[0]
        cross_color = (
            (255, 220, 0)
            if guide_mode == "marker_only"
            else (255, 255, 255)
        )
        draw.line(
            (
                cross_x - cross_radius,
                center_pixels[1],
                cross_x + cross_radius,
                center_pixels[1],
            ),
            fill=cross_color,
            width=3,
        )
        draw.line(
            (
                cross_x,
                center_pixels[1] - cross_radius,
                cross_x,
                center_pixels[1] + cross_radius,
            ),
            fill=cross_color,
            width=3,
        )
        draw.rectangle((8, 8, 232, 31), fill=(0, 0, 0))
        draw.text((14, 13), LABEL, fill=(255, 255, 255), font=font)
        draw.rectangle((8, 37, 256, 60), fill=(0, 0, 0))
        draw.text(
            (14, 42),
            f"TARGET_EDGE_X={leading_edge}",
            fill=(255, 220, 0),
            font=font,
        )
        if previous_leading_edge is not None:
            draw.rectangle((8, 66, 256, 89), fill=(0, 0, 0))
            draw.text(
                (14, 71),
                f"PREVIOUS_EDGE_X={previous_leading_edge}",
                fill=(255, 35, 95),
                font=font,
            )
        guide_path = guide_dir / f"frame_{frame:06d}_guide.png"
        guide.save(guide_path, optimize=True)
        records.append(
            {
                "frame": frame,
                "normalized_center": [round(center[0], 8), round(center[1], 8)],
                "leading_edge_x": leading_edge,
                "previous_leading_edge_x": previous_leading_edge,
                "guide": {
                    "path": str(guide_path.resolve()),
                    "sha256": sha256_file(guide_path),
                    "role": "position_only",
                    "used_as_delivery_pixels": False,
                },
                "mask": {
                    "path": str(mask_path.resolve()),
                    "sha256": sha256_file(mask_path),
                },
            }
        )
        previous_mask = mask
        previous_leading_edge = leading_edge
        previous_visible_box = visible_box

    manifest = {
        "schema": "cinematic-position-guides-v1",
        "label": LABEL,
        "source": {
            "path": str(source.resolve()),
            "sha256": sha256_file(source),
            "delivery_authority": False,
        },
        "frame_count": frame_count,
        "size": list(size),
        "start_center": list(start_center),
        "end_center": list(end_center),
        "occupancy_width": occupancy_width,
        "guide_mode": guide_mode,
        "appearance_authority": False,
        "position_authority_only": True,
        "reference_background": None,
        "frames": records,
    }
    (output / "position_guides.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="alpha image used only for footprint")
    parser.add_argument("output", type=Path)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--size", type=parse_size, default=(1280, 720))
    parser.add_argument("--start-center", type=parse_pair, required=True)
    parser.add_argument("--end-center", type=parse_pair, required=True)
    parser.add_argument("--occupancy-width", type=float, default=0.62)
    guide_modes = parser.add_mutually_exclusive_group()
    guide_modes.add_argument(
        "--marker-only",
        action="store_true",
        help="show only a neutral-field target-edge crosshair, not a footprint",
    )
    guide_modes.add_argument(
        "--bounding-box-only",
        action="store_true",
        help="show neutral-field subject bounds without a silhouette footprint",
    )
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error(f"source does not exist: {args.source}")
    if args.output.exists():
        parser.error(f"output already exists: {args.output}")
    if args.frames < 1:
        parser.error("--frames must be positive")
    if not 0.05 <= args.occupancy_width <= 1.5:
        parser.error("--occupancy-width must be between 0.05 and 1.5")
    try:
        manifest = render_guides(
            args.source,
            args.output,
            args.frames,
            args.size,
            args.start_center,
            args.end_center,
            args.occupancy_width,
            (
                "marker_only"
                if args.marker_only
                else "bounding_box"
                if args.bounding_box_only
                else "chroma_footprint"
            ),
        )
    except ValueError as error:
        parser.error(str(error))
    print(
        "POSITION_GUIDES|"
        f"frames={manifest['frame_count']}|size={manifest['size']}|"
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
