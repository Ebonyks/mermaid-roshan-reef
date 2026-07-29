#!/usr/bin/env python3
"""Rebuild the 15-second opening test as a stable 42.5-second V2 animatic.

The source movie contains thirty independently redrawn nine-frame storyboard
groups.  This tool preserves that approved 2D art while changing its temporal
presentation:

- retimes the story to the approved 24 fps / 1020-frame direction brief;
- removes the prohibited landing-wheel group and the incorrect final release;
- removes production frame-number labels from reused poses;
- holds selected drawings as deliberate limited-animation poses instead of
  replaying every unstable redraw; and
- creates the reveal from one locked plate with an authored ease-out.

It does not call a generator, modify source art, or synthesize family audio.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


FPS = 24
SOURCE_FRAME_COUNT = 270
OUTPUT_FRAME_COUNT = 1020
SOURCE_GROUP_SIZE = 9
SOURCE_SIZE = (1280, 720)
LABEL_FIRST_FRAME = 135
FINAL_HANDHOLD_FRAME = 260


@dataclass(frozen=True)
class Shot:
    id: str
    duration_frames: int
    source_groups: tuple[int, ...] = ()
    adaptive_offsets: tuple[int, ...] = (0, 2, 4, 6, 8)
    mode: str = "poses"


SHOTS = (
    Shot("01_open_sky", 48, (0, 1)),
    Shot("02_safe_room", 48, (2,)),
    Shot("03_roshan_notices", 48, (3, 4)),
    Shot("04_daddy_notices", 36, (5,)),
    Shot("05_the_choice", 48, (6, 7)),
    Shot("06_reassurance", 60, (8, 9)),
    # Source group 10 is the prohibited landing-wheel/runway insert.
    Shot("07_arrival_felt_inside", 54, (11, 12)),
    Shot("08_daddy_demonstrates", 60, (13,)),
    Shot("09_roshan_copies", 42, (14,)),
    Shot("10_the_offered_hand", 72, (15, 16, 17)),
    Shot("11_together_to_the_door", 48, (18,)),
    Shot("12_new_air", 60, (19, 20)),
    Shot("13_complete_safe_route", 60, (21,)),
    Shot("14_crossing", 96, (22, 23, 24, 25), (0, 4, 8)),
    Shot("15_invitation", 54, (26,), (0, 4, 8)),
    Shot("16_wonder_arrives", 66, (27,)),
    Shot("17_reef_is_waiting", 84, mode="reveal"),
    # Source group 29 breaks the handhold and makes Daddy wave. Reuse the
    # accepted group-28 endpoint instead.
    Shot("18_final_handoff", 36, mode="final_hold"),
)


def find_video_tool(repo_root: Path, name: str) -> Path:
    configured = os.environ.get(f"MERMAID_{name.upper()}")
    if configured:
        candidate = Path(configured).expanduser().resolve()
        if candidate.is_file():
            return candidate
        raise ValueError(f"MERMAID_{name.upper()} does not point to a file: {candidate}")
    executable = shutil.which(name)
    if executable:
        return Path(executable)
    local_tools = sorted(
        (repo_root / ".video-tools").glob(f"ffmpeg-*-essentials_build/bin/{name}.exe"),
        reverse=True,
    )
    if local_tools:
        return local_tools[0]
    raise ValueError(f"{name} was not found; run tools/setup_video_tools.cmd")


def extract_frames(ffmpeg: Path, video: Path, destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-loglevel", "error",
            "-i", str(video),
            "-vsync", "0",
            "-start_number", "0",
            str(destination / "source_%04d.png"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise ValueError(completed.stderr.strip() or "FFmpeg frame extraction failed")
    frames = sorted(destination.glob("source_*.png"))
    if len(frames) != SOURCE_FRAME_COUNT:
        raise ValueError(
            f"expected {SOURCE_FRAME_COUNT} source frames, decoded {len(frames)}"
        )
    return frames


def distribute(total: int, item_count: int) -> list[int]:
    if item_count <= 0:
        raise ValueError("cannot distribute frames across an empty pose list")
    quotient, remainder = divmod(total, item_count)
    return [
        quotient + (1 if index < remainder else 0)
        for index in range(item_count)
    ]


def distribute_quiet_motion_quiet(total: int, item_count: int) -> list[int]:
    """Give anticipation and settle poses twice the weight of breakdown poses."""
    if item_count <= 2:
        return distribute(total, item_count)
    weights = [2] + [1] * (item_count - 2) + [2]
    weight_total = sum(weights)
    exact = [total * weight / weight_total for weight in weights]
    holds = [max(1, int(value)) for value in exact]
    remainder = total - sum(holds)
    order = sorted(
        range(item_count),
        key=lambda index: exact[index] - int(exact[index]),
        reverse=True,
    )
    for index in order[:remainder]:
        holds[index] += 1
    if sum(holds) != total:
        raise ValueError("weighted pose distribution did not preserve duration")
    return holds


def source_indices(shot: Shot, profile: str) -> list[int]:
    if shot.mode != "poses":
        return [FINAL_HANDHOLD_FRAME]
    if profile == "dense":
        offsets = tuple(range(SOURCE_GROUP_SIZE))
    elif profile == "sparse":
        offsets = (0, 4, 8)
    else:
        offsets = shot.adaptive_offsets
    return [
        group * SOURCE_GROUP_SIZE + offset
        for group in shot.source_groups
        for offset in offsets
    ]


def remove_production_label(image: Image.Image) -> Image.Image:
    """Replace the fixed top-left review label from adjacent approved pixels."""
    base = image.convert("RGB")
    replacement = base.copy()
    left, top, right, bottom = 8, 8, 144, 86
    width = right - left
    adjacent = base.crop((right, top, right + width, bottom))
    adjacent = adjacent.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    replacement.paste(adjacent, (left, top))
    replacement = replacement.filter(ImageFilter.GaussianBlur(10))

    # Keep the label area fully opaque, then feather broadly toward the live
    # picture on the right and bottom. This avoids both text ghosting and a
    # rectangular clone-stamp edge.
    y_grid, x_grid = np.mgrid[0:base.height, 0:base.width]
    x_alpha = np.where(
        x_grid <= 140,
        1.0,
        np.clip((280.0 - x_grid) / 140.0, 0.0, 1.0),
    )
    y_alpha = np.where(
        y_grid <= 82,
        1.0,
        np.clip((200.0 - y_grid) / 118.0, 0.0, 1.0),
    )
    mask = Image.fromarray(
        (np.minimum(x_alpha, y_alpha) * 255.0).astype(np.uint8),
        mode="L",
    )
    result = Image.composite(replacement, base, mask)
    result.paste(base.crop((0, 0, base.width, 8)), (0, 0))
    result.paste(base.crop((0, 0, 8, base.height)), (0, 0))
    return result


def remove_early_destination(image: Image.Image) -> Image.Image:
    """Withhold the premature island/castle silhouette from the opening sky."""
    base = image.convert("RGB")
    array = np.asarray(base).copy()
    left, top, right, bottom = 960, 455, 1268, 704
    width = right - left
    source_left = left - width
    source = array[top:bottom, source_left:left]
    array[top:bottom, left:right] = source[:, ::-1]
    replacement = Image.fromarray(array, mode="RGB")
    mask = Image.new("L", base.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((990, 485, 1245, 680), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(24))
    return Image.composite(replacement, base, mask)


def fit_size(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    if image.size == size:
        return image
    return image.resize(size, Image.Resampling.LANCZOS)


def load_pose(source: Path, source_index: int, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as opened:
        pose = opened.convert("RGB")
        if source_index < 18:
            pose = remove_early_destination(pose)
        if source_index >= LABEL_FIRST_FRAME:
            pose = remove_production_label(pose)
        return fit_size(pose, size)


def write_pose(
    source_frames: list[Path],
    source_index: int,
    pose_dir: Path,
    size: tuple[int, int],
) -> Path:
    destination = pose_dir / f"source_{source_index:04d}.png"
    if not destination.exists():
        load_pose(source_frames[source_index], source_index, size).save(
            destination,
            format="PNG",
            optimize=True,
        )
    return destination


def link_or_copy(source: Path, destination: Path) -> None:
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def ease_out_cubic(value: float) -> float:
    return 1.0 - (1.0 - value) ** 3


def reveal_frame(base: Image.Image, progress: float) -> Image.Image:
    eased = ease_out_cubic(progress)
    scale = 1.06 - 0.06 * eased
    width, height = base.size
    resized = base.resize(
        (round(width * scale), round(height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def render(
    source_frames: list[Path],
    output_dir: Path,
    profile: str,
    size: tuple[int, int],
    source_video: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=False)
    pose_dir = output_dir / "_poses"
    pose_dir.mkdir()
    output_index = 0
    shot_records: list[dict[str, Any]] = []
    label_cleaned: set[int] = set()

    for shot in SHOTS:
        shot_start = output_index
        indices = source_indices(shot, profile)
        if shot.mode == "poses":
            holds = (
                distribute_quiet_motion_quiet(shot.duration_frames, len(indices))
                if profile == "adaptive"
                else distribute(shot.duration_frames, len(indices))
            )
            for source_index, hold_count in zip(indices, holds):
                pose_path = write_pose(source_frames, source_index, pose_dir, size)
                if source_index >= LABEL_FIRST_FRAME:
                    label_cleaned.add(source_index)
                for _ in range(hold_count):
                    link_or_copy(
                        pose_path,
                        output_dir / f"frame_{output_index:06d}.png",
                    )
                    output_index += 1
        elif shot.mode == "reveal":
            source_index = FINAL_HANDHOLD_FRAME
            base = load_pose(source_frames[source_index], source_index, size)
            label_cleaned.add(source_index)
            moving_frames = 29  # Approved 1.2-second ease at 24 fps, rounded.
            for local_index in range(shot.duration_frames):
                if local_index < moving_frames:
                    progress = local_index / (moving_frames - 1)
                    pose_path = pose_dir / f"reveal_{local_index:03d}.png"
                    reveal_frame(base, progress).save(
                        pose_path,
                        format="PNG",
                        optimize=True,
                    )
                else:
                    pose_path = pose_dir / "reveal_028.png"
                link_or_copy(
                    pose_path,
                    output_dir / f"frame_{output_index:06d}.png",
                )
                output_index += 1
        elif shot.mode == "final_hold":
            source_index = FINAL_HANDHOLD_FRAME
            pose_path = write_pose(source_frames, source_index, pose_dir, size)
            label_cleaned.add(source_index)
            for _ in range(shot.duration_frames):
                link_or_copy(
                    pose_path,
                    output_dir / f"frame_{output_index:06d}.png",
                )
                output_index += 1
        else:
            raise ValueError(f"unsupported shot mode: {shot.mode}")

        shot_records.append(
            {
                "id": shot.id,
                "output_start_frame": shot_start,
                "output_end_frame": output_index - 1,
                "source_frames": indices,
                "mode": shot.mode,
            }
        )

    if output_index != OUTPUT_FRAME_COUNT:
        raise ValueError(
            f"timeline generated {output_index} frames, expected {OUTPUT_FRAME_COUNT}"
        )

    provenance = {
        "schema": "opening-cinematic-stabilized-v1",
        "source_video": str(source_video),
        "source_sha256": hashlib.sha256(source_video.read_bytes()).hexdigest().upper(),
        "source_frame_count": SOURCE_FRAME_COUNT,
        "output_fps": FPS,
        "output_frame_count": OUTPUT_FRAME_COUNT,
        "output_duration_seconds": OUTPUT_FRAME_COUNT / FPS,
        "profile": profile,
        "size": list(size),
        "method": "approved-source-pose reuse, deterministic holds, label cleanup, locked-plate reveal",
        "new_generated_art": False,
        "derived_repairs": [
            "opening island/castle silhouette removed to preserve delayed reveal",
            "production frame-number labels removed from reused poses",
        ],
        "source_ranges_excluded": [
            {"start": 90, "end": 98, "reason": "prohibited landing-wheel/runway insert"},
            {"start": 261, "end": 269, "reason": "final hand release and wave violate continuity lock"},
        ],
        "label_cleaned_source_frames": sorted(label_cleaned),
        "shots": shot_records,
    }
    (output_dir / "provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n",
        encoding="utf-8",
    )
    return provenance


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", 1)
        size = (int(width_text), int(height_text))
    except (ValueError, AttributeError) as error:
        raise argparse.ArgumentTypeError("size must be WIDTHxHEIGHT") from error
    if min(size) < 2 or any(dimension % 2 for dimension in size):
        raise argparse.ArgumentTypeError("width and height must be even and at least 2")
    return size


def validate_timeline() -> None:
    if sum(shot.duration_frames for shot in SHOTS) != OUTPUT_FRAME_COUNT:
        raise ValueError("shot durations do not total 1020 frames")
    used_groups = {
        group for shot in SHOTS for group in shot.source_groups
    }
    if 10 in used_groups or 29 in used_groups:
        raise ValueError("prohibited source groups entered the stabilized timeline")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_video", type=Path)
    parser.add_argument("output_frames", type=Path)
    parser.add_argument(
        "--profile",
        choices=("dense", "sparse", "adaptive"),
        default="adaptive",
        help="pose density; adaptive is the approved balance",
    )
    parser.add_argument("--size", type=parse_size, default=SOURCE_SIZE)
    args = parser.parse_args()
    if not args.input_video.is_file():
        parser.error(f"input video does not exist: {args.input_video}")
    if args.output_frames.exists():
        parser.error(f"output path already exists: {args.output_frames}")

    validate_timeline()
    repo_root = Path(__file__).resolve().parents[1]
    try:
        ffmpeg = find_video_tool(repo_root, "ffmpeg")
        with tempfile.TemporaryDirectory(prefix="opening-cinematic-source-") as temp:
            source_frames = extract_frames(ffmpeg, args.input_video, Path(temp))
            provenance = render(
                source_frames,
                args.output_frames,
                args.profile,
                args.size,
                args.input_video.resolve(),
            )
    except ValueError as error:
        parser.error(str(error))
    print(
        "OPENING_REGEN|"
        f"profile={provenance['profile']}|frames={provenance['output_frame_count']}|"
        f"fps={provenance['output_fps']}|duration={provenance['output_duration_seconds']:g}|"
        f"new_art={str(provenance['new_generated_art']).lower()}|"
        f"output={args.output_frames}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
