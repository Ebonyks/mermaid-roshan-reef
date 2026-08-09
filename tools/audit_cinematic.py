#!/usr/bin/env python3
"""Auditable quality gates for a rendered cinematic.

This tool deliberately does not attempt to decide whether a character is
"beautiful".  It creates a strict, reproducible record for the things a video
encoder cannot know: shot boundaries, required per-frame tracks, contact spans,
human review scores, and production-wide character identity review.

Use --bootstrap to turn a movie into a scene/quality manifest skeleton.  Fill
the generated tracks and reviews before running the blocking audit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageStat


QUALITY_FLOOR = 4.8
SCENE_FLOOR = 4.85
IDENTITY_FLOOR = 4.9
ANIMATIC_SCENE_FLOOR = 4.25
ANIMATIC_IDENTITY_FLOOR = 4.5
THRESHOLD_PROFILES = {
    "production": (SCENE_FLOOR, IDENTITY_FLOOR),
    "animatic": (ANIMATIC_SCENE_FLOOR, ANIMATIC_IDENTITY_FLOOR),
}
REQUIRED_SCORES = ("construction", "identity", "motion", "contact", "style", "performance")
FRAME_REGENERATION_SCORES = ("identity", "topology", "style", "neighbor_continuity")
FRAME_REGENERATION_FLOOR = 4.9
ANALYSIS_SIZE = (320, 180)
PRODUCTION_DELIVERY_SIZE = (1280, 720)
VIDEO_GEOMETRY_TOLERANCE = 1e-6
BOIL_THRESHOLD = 8
SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
FULL_FRAME_GENERATION_METHOD = "full_frame_image_generation"
FORBIDDEN_TEMPORAL_METHODS = (
    "chroma",
    "cross_dissolve",
    "cutout",
    "interpolation",
    "morph",
    "optical_flow",
    "procedural_warp",
    "rig",
    "sprite",
    "tween",
)


def fail(message: str) -> None:
    raise ValueError(message)


def command(name: str) -> str:
    candidate = shutil.which(name)
    if not candidate:
        fail(f"{name} was not found. Run tools/setup_video_tools.cmd or put it on PATH.")
    return candidate


def run(args: list[str]) -> str:
    completed = subprocess.run(args, check=False, capture_output=True, text=True)
    if completed.returncode:
        fail(completed.stderr.strip() or "external video command failed")
    return completed.stdout


def parse_rate(value: Any) -> float:
    if not isinstance(value, str) or "/" not in value:
        return 0.0
    numerator, denominator = value.split("/", 1)
    try:
        parsed_denominator = float(denominator)
        return float(numerator) / parsed_denominator if parsed_denominator else 0.0
    except ValueError:
        return 0.0


def parse_aspect_ratio(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    separator = ":" if ":" in value else "/" if "/" in value else None
    if separator is None:
        return None
    numerator, denominator = value.split(separator, 1)
    try:
        parsed_numerator = int(numerator)
        parsed_denominator = int(denominator)
    except ValueError:
        return None
    if parsed_numerator <= 0 or parsed_denominator <= 0:
        return None
    common = math.gcd(parsed_numerator, parsed_denominator)
    return parsed_numerator // common, parsed_denominator // common


def normalized_rotation(value: Any) -> float | None:
    try:
        rotation = float(value) % 360.0
    except (TypeError, ValueError):
        return None
    if not math.isfinite(rotation):
        return None
    if math.isclose(rotation, 0.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE) or math.isclose(
        rotation, 360.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE
    ):
        return 0.0
    return rotation


def video_info(video: Path) -> dict[str, Any]:
    data = json.loads(run([
        command("ffprobe"),
        "-v", "error",
        "-count_frames",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=avg_frame_rate,r_frame_rate,nb_frames,nb_read_frames,duration,"
        "width,height,sample_aspect_ratio,display_aspect_ratio:"
        "stream_tags=rotate:stream_side_data=rotation:format=duration",
        "-of", "json",
        str(video),
    ]))
    if not data.get("streams"):
        fail("video has no readable video stream")
    stream = data["streams"][0]
    fps = parse_rate(stream.get("avg_frame_rate"))
    if fps <= 0:
        fps = parse_rate(stream.get("r_frame_rate"))
    encoded_count = int(stream.get("nb_frames") or 0)
    packet_count = int(stream.get("nb_read_frames") or 0)
    duration = float(stream.get("duration") or data.get("format", {}).get("duration") or 0.0)
    displayed_count = int(round(fps * duration)) if fps > 0 and duration > 0 else 0
    # Theora may expose fewer decoded frames than its logical constant-rate
    # display timeline when held drawings are timestamped across gaps. In that
    # case nb_read_frames is not the frame count required by the animation
    # contract.
    count = encoded_count or displayed_count or packet_count
    if fps <= 0 or count <= 0:
        fail("video must expose a positive frame rate and frame count")
    width = int(stream.get("width") or 0)
    height = int(stream.get("height") or 0)
    if width <= 0 or height <= 0:
        fail("video must expose positive coded width and height")

    sample_aspect_text = stream.get("sample_aspect_ratio")
    sample_aspect = parse_aspect_ratio(sample_aspect_text)
    reported_display_aspect_text = stream.get("display_aspect_ratio")
    reported_display_aspect = parse_aspect_ratio(reported_display_aspect_text)

    raw_rotations: list[Any] = []
    tags = stream.get("tags")
    if isinstance(tags, dict) and "rotate" in tags:
        raw_rotations.append(tags["rotate"])
    side_data = stream.get("side_data_list")
    if isinstance(side_data, list):
        for item in side_data:
            if isinstance(item, dict) and "rotation" in item:
                raw_rotations.append(item["rotation"])
    rotations = [normalized_rotation(value) for value in raw_rotations]
    rotation_metadata_valid = all(value is not None for value in rotations)
    valid_rotations = [value for value in rotations if value is not None]
    rotation = valid_rotations[0] if valid_rotations else 0.0
    rotation_conflict = any(
        not math.isclose(value, rotation, abs_tol=VIDEO_GEOMETRY_TOLERANCE)
        for value in valid_rotations[1:]
    )

    display_size: tuple[float, float] | None = None
    effective_display_aspect: float | None = None
    if sample_aspect is not None and rotation_metadata_valid and not rotation_conflict:
        display_width = width * sample_aspect[0] / sample_aspect[1]
        display_height = float(height)
        if math.isclose(rotation, 90.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE) or math.isclose(
            rotation, 270.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE
        ):
            display_width, display_height = display_height, display_width
        display_size = display_width, display_height
        effective_display_aspect = display_width / display_height

    reported_effective_aspect: float | None = None
    if reported_display_aspect is not None:
        reported_effective_aspect = (
            reported_display_aspect[0] / reported_display_aspect[1]
        )
        if math.isclose(rotation, 90.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE) or math.isclose(
            rotation, 270.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE
        ):
            reported_effective_aspect = 1.0 / reported_effective_aspect

    return {
        "fps": fps,
        "frame_count": count,
        "coded_size": (width, height),
        "sample_aspect_ratio": sample_aspect,
        "sample_aspect_ratio_text": sample_aspect_text,
        "reported_display_aspect_ratio": reported_display_aspect,
        "reported_display_aspect_ratio_text": reported_display_aspect_text,
        "reported_effective_aspect_ratio": reported_effective_aspect,
        "rotation_degrees": rotation,
        "rotation_metadata_valid": rotation_metadata_valid,
        "rotation_conflict": rotation_conflict,
        "display_size": display_size,
        "effective_display_aspect_ratio": effective_display_aspect,
    }


def validate_video_delivery(info: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_width, expected_height = PRODUCTION_DELIVERY_SIZE
    coded_width, coded_height = info["coded_size"]
    if (coded_width, coded_height) != PRODUCTION_DELIVERY_SIZE:
        errors.append(
            f"video coded size {coded_width}x{coded_height} does not match required "
            f"{expected_width}x{expected_height} landscape delivery"
        )

    sample_aspect = info.get("sample_aspect_ratio")
    if sample_aspect != (1, 1):
        errors.append(
            "video sample aspect ratio must be explicit square pixels (1:1); "
            f"found {info.get('sample_aspect_ratio_text')!r}"
        )

    rotation = info.get("rotation_degrees")
    if not info.get("rotation_metadata_valid", False):
        errors.append("video contains unreadable rotation metadata")
    elif info.get("rotation_conflict", False):
        errors.append("video contains conflicting rotation metadata")
    elif not isinstance(rotation, (int, float)) or not math.isclose(
        float(rotation), 0.0, abs_tol=VIDEO_GEOMETRY_TOLERANCE
    ):
        rotation_text = (
            f"{rotation:g}" if isinstance(rotation, (int, float)) else repr(rotation)
        )
        errors.append(
            f"video rotation metadata is {rotation_text} degrees; delivery must be "
            "encoded in native landscape orientation"
        )

    display_size = info.get("display_size")
    if display_size is None:
        errors.append("video displayed dimensions cannot be derived from its metadata")
    else:
        display_width, display_height = display_size
        if display_width <= display_height:
            errors.append(
                f"video displayed orientation is not landscape ({display_width:g}x{display_height:g})"
            )
        if not (
            math.isclose(display_width, expected_width, abs_tol=VIDEO_GEOMETRY_TOLERANCE)
            and math.isclose(display_height, expected_height, abs_tol=VIDEO_GEOMETRY_TOLERANCE)
        ):
            errors.append(
                f"video displayed size {display_width:g}x{display_height:g} does not "
                f"match required {expected_width}x{expected_height} delivery"
            )

    reported_aspect = info.get("reported_effective_aspect_ratio")
    derived_aspect = info.get("effective_display_aspect_ratio")
    if reported_aspect is not None and derived_aspect is not None and not math.isclose(
        float(reported_aspect), float(derived_aspect), rel_tol=VIDEO_GEOMETRY_TOLERANCE
    ):
        errors.append(
            "video display-aspect metadata conflicts with coded dimensions and "
            "sample aspect ratio"
        )
    return errors


def video_geometry_report(info: dict[str, Any]) -> dict[str, Any]:
    return {
        "coded_size": list(info["coded_size"]),
        "sample_aspect_ratio": list(info["sample_aspect_ratio"])
        if info.get("sample_aspect_ratio") is not None
        else None,
        "sample_aspect_ratio_text": info.get("sample_aspect_ratio_text"),
        "reported_display_aspect_ratio": list(info["reported_display_aspect_ratio"])
        if info.get("reported_display_aspect_ratio") is not None
        else None,
        "reported_display_aspect_ratio_text": info.get("reported_display_aspect_ratio_text"),
        "rotation_degrees": info.get("rotation_degrees"),
        "rotation_metadata_valid": info.get("rotation_metadata_valid"),
        "rotation_conflict": info.get("rotation_conflict"),
        "display_size": list(info["display_size"])
        if info.get("display_size") is not None
        else None,
        "effective_display_aspect_ratio": info.get("effective_display_aspect_ratio"),
    }


def extract_frames(
    video: Path,
    destination: Path,
    fps: float | None = None,
    frame_count: int | None = None,
) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    arguments = [
        command("ffmpeg"),
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(video),
    ]
    if fps is None:
        arguments += ["-vsync", "0"]
    else:
        fps_text = f"{fps:.12g}"
        # Materialize the declared constant-rate display timeline, including
        # the tail hold, before applying frame-indexed gates.
        arguments += [
            "-vf", f"tpad=stop_mode=clone:stop_duration=10,fps={fps_text}",
            "-fps_mode", "cfr",
        ]
        if frame_count is not None:
            arguments += ["-frames:v", str(frame_count)]
    arguments += [
        "-start_number", "0",
        str(destination / "frame_%06d.png"),
    ]
    run(arguments)
    frames = sorted(destination.glob("frame_*.png"))
    if not frames:
        fail("decoder produced no frames")
    return frames


def frame_delta(left: Path, right: Path) -> float:
    with Image.open(left).convert("L") as a, Image.open(right).convert("L") as b:
        # Downsample: scene-cut detection should respond to composition, not grain.
        a = a.resize((160, 90)); b = b.resize((160, 90))
        return float(ImageStat.Stat(ImageChops.difference(a, b)).mean[0])


def cuts(frames: list[Path]) -> list[int]:
    deltas = [frame_delta(a, b) for a, b in zip(frames, frames[1:])]
    if not deltas:
        return []
    median = statistics.median(deltas)
    # Conservative: reviewers may split a long shot further, but a cut is not
    # accidentally scored as continuity jitter.
    threshold = max(24.0, median * 3.5)
    # Return the zero-indexed target frame of each transition.
    return [index + 1 for index, value in enumerate(deltas) if value >= threshold]


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(fraction * len(ordered)) - 1))
    return float(ordered[index])


def transition_metrics(left: Path, right: Path) -> tuple[float, float, int]:
    with Image.open(left).convert("L") as first, Image.open(right).convert("L") as second:
        first = first.resize(ANALYSIS_SIZE)
        second = second.resize(ANALYSIS_SIZE)
        difference = ImageChops.difference(first, second)
        histogram = difference.histogram()
        pixel_count = ANALYSIS_SIZE[0] * ANALYSIS_SIZE[1]
        changed = sum(histogram[BOIL_THRESHOLD + 1:]) / pixel_count
        cumulative = 0
        p95_target = math.ceil(pixel_count * 0.95)
        p95 = 255
        for value, occurrences in enumerate(histogram):
            cumulative += occurrences
            if cumulative >= p95_target:
                p95 = value
                break
        return float(ImageStat.Stat(difference).mean[0]), float(changed), p95


def analyze_frames(frames: list[Path], lattice: int) -> dict[str, Any]:
    deltas: list[float] = []
    changed_fractions: list[float] = []
    p95_changes: list[int] = []
    for left, right in zip(frames, frames[1:]):
        delta, changed_fraction, p95 = transition_metrics(left, right)
        deltas.append(delta)
        changed_fractions.append(changed_fraction)
        p95_changes.append(p95)

    median_delta = statistics.median(deltas) if deltas else 0.0
    cut_threshold = max(24.0, median_delta * 3.5)
    candidate_cuts = [
        {"target_frame": index + 1, "mean_delta": round(value, 4)}
        for index, value in enumerate(deltas)
        if value >= cut_threshold
    ]
    lattice_values = [
        value for target, value in enumerate(deltas, start=1)
        if lattice > 0 and target % lattice == 0
    ]
    non_lattice_values = [
        value for target, value in enumerate(deltas, start=1)
        if lattice <= 0 or target % lattice != 0
    ]
    lattice_ratio = (
        statistics.mean(lattice_values) / statistics.mean(non_lattice_values)
        if lattice_values and non_lattice_values and statistics.mean(non_lattice_values) > 0
        else 0.0
    )
    return {
        "analysis_resolution": list(ANALYSIS_SIZE),
        "transition_count": len(deltas),
        "mean_delta": round(statistics.mean(deltas), 4) if deltas else 0.0,
        "median_delta": round(median_delta, 4),
        "p95_delta": round(percentile(deltas, 0.95), 4),
        "max_delta": round(max(deltas), 4) if deltas else 0.0,
        "near_hold_ratio": round(
            sum(value <= 0.5 for value in deltas) / len(deltas), 4
        ) if deltas else 0.0,
        "mean_changed_fraction_over_8": round(
            statistics.mean(changed_fractions), 4
        ) if changed_fractions else 0.0,
        "median_changed_fraction_over_8": round(
            statistics.median(changed_fractions), 4
        ) if changed_fractions else 0.0,
        "p95_changed_fraction_over_8": round(
            percentile(changed_fractions, 0.95), 4
        ),
        "p95_pixel_change": int(percentile([float(value) for value in p95_changes], 0.95)),
        "candidate_cut_threshold": round(cut_threshold, 4),
        "candidate_cuts": candidate_cuts,
        "lattice": {
            "period": lattice,
            "boundary_count": len(lattice_values),
            "mean_boundary_delta": round(statistics.mean(lattice_values), 4)
            if lattice_values else 0.0,
            "mean_non_boundary_delta": round(statistics.mean(non_lattice_values), 4)
            if non_lattice_values else 0.0,
            "boundary_to_non_boundary_ratio": round(lattice_ratio, 4),
        },
    }


def analyze(video: Path, report_path: Path | None, lattice: int) -> None:
    info = video_info(video)
    fps = float(info["fps"])
    count = int(info["frame_count"])
    with tempfile.TemporaryDirectory(prefix="cinematic-analysis-") as temp:
        frames = extract_frames(video, Path(temp), fps, count)
        if len(frames) != count:
            fail(f"decoder produced {len(frames)} frames, ffprobe reported {count}")
        metrics = analyze_frames(frames, lattice)
    report = {
        "schema": "cinematic-automatic-analysis-v1",
        "video": str(video),
        "fps": fps,
        "frame_count": count,
        "duration": count / fps,
        "geometry": video_geometry_report(info),
        "metrics": metrics,
        "limitations": [
            "Automatic pixel metrics do not judge character identity, anatomy, contact, emotion, or story intent.",
            "Candidate cuts are evidence for reviewer classification, not authoritative edit decisions.",
            "Boil metrics include intentional motion unless reviewers provide static-region masks.",
        ],
    }
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        "CINEMATIC_ANALYSIS|"
        f"frames={count}|fps={fps:g}|median_delta={metrics['median_delta']:g}|"
        f"hold_ratio={metrics['near_hold_ratio']:g}|"
        f"changed_over_8={metrics['mean_changed_fraction_over_8']:g}|"
        f"candidate_cuts={len(metrics['candidate_cuts'])}"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def artifact_path(
    record: Any,
    label: str,
    manifest_dir: Path,
    errors: list[str],
) -> Path | None:
    if not isinstance(record, dict):
        errors.append(f"{label}: requires path and sha256")
        return None
    path_value = record.get("path")
    expected_hash = record.get("sha256")
    if not isinstance(path_value, str) or not path_value:
        errors.append(f"{label}: missing path")
        return None
    if not isinstance(expected_hash, str) or not SHA256_PATTERN.fullmatch(expected_hash):
        errors.append(f"{label}: sha256 must be 64 hexadecimal characters")
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = manifest_dir / path
    path = path.resolve()
    if not path.is_file():
        errors.append(f"{label}: file does not exist: {path}")
        return None
    actual_hash = sha256_file(path)
    if actual_hash.lower() != expected_hash.lower():
        errors.append(
            f"{label}: sha256 mismatch; expected {expected_hash.lower()}, "
            f"found {actual_hash.lower()}"
        )
        return None
    return path


def image_size(path: Path, label: str, errors: list[str]) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            image.load()
            return image.size
    except (OSError, ValueError) as error:
        errors.append(f"{label}: unreadable image: {error}")
        return None


def validate_native_canvas_aspect(
    size: tuple[int, int],
    delivery_size: list[int],
    maximum_aspect_error: float,
    label: str,
    errors: list[str],
) -> None:
    native_width, native_height = size
    delivery_width, delivery_height = delivery_size
    native_orientation = (native_width > native_height) - (native_width < native_height)
    delivery_orientation = (delivery_width > delivery_height) - (
        delivery_width < delivery_height
    )
    if native_orientation != delivery_orientation:
        errors.append(
            f"{label}: native canvas orientation {native_width}x{native_height} does not "
            f"match delivery orientation {delivery_width}x{delivery_height}"
        )
        return
    delivery_aspect = delivery_width / delivery_height
    aspect_error = abs(native_width / native_height / delivery_aspect - 1)
    if aspect_error > maximum_aspect_error:
        errors.append(
            f"{label}: native canvas aspect error {aspect_error:.6f} exceeds "
            f"{maximum_aspect_error:.6f} for required delivery"
        )


def mask_position(
    path: Path,
    expected_size: tuple[int, int] | None,
    anchor: str,
    label: str,
    errors: list[str],
) -> tuple[float, float] | None:
    try:
        with Image.open(path).convert("L") as mask:
            if expected_size is not None and mask.size != expected_size:
                errors.append(
                    f"{label}: mask size {mask.size} does not match frame size "
                    f"{expected_size}"
                )
                return None
            binary = mask.point(lambda value: 255 if value >= 128 else 0)
            bounds = binary.getbbox()
            if bounds is None:
                errors.append(f"{label}: mask contains no subject pixels")
                return None
            left, top, right, bottom = bounds
            center_x = (left + right) / (2.0 * mask.width)
            center_y = (top + bottom) / (2.0 * mask.height)
            if anchor == "center":
                return center_x, center_y
            if anchor == "bbox_left":
                return left / mask.width, center_y
            if anchor == "bbox_right":
                return right / mask.width, center_y
            if anchor == "bbox_top":
                return center_x, top / mask.height
            if anchor == "bbox_bottom":
                return center_x, bottom / mask.height
            if anchor in ("leading_edge_left", "leading_edge_right"):
                strip_width = max(1, round(mask.width * 0.07))
                if anchor == "leading_edge_left":
                    strip_left = left
                    strip_right = min(right, left + strip_width)
                    edge_x = left / mask.width
                else:
                    strip_left = max(left, right - strip_width)
                    strip_right = right
                    edge_x = right / mask.width
                edge_bounds = binary.crop(
                    (strip_left, 0, strip_right, mask.height)
                ).getbbox()
                if edge_bounds is None:
                    errors.append(f"{label}: leading-edge strip contains no pixels")
                    return None
                edge_center_y = (edge_bounds[1] + edge_bounds[3]) / (
                    2.0 * mask.height
                )
                return edge_x, edge_center_y
            errors.append(f"{label}: unsupported position_anchor '{anchor}'")
            return None
    except (OSError, ValueError) as error:
        errors.append(f"{label}: unreadable mask: {error}")
        return None


def mask_geometry(
    path: Path,
    expected_size: tuple[int, int] | None,
    label: str,
    errors: list[str],
) -> dict[str, float] | None:
    try:
        with Image.open(path).convert("L") as mask:
            if expected_size is not None and mask.size != expected_size:
                errors.append(
                    f"{label}: mask size {mask.size} does not match frame size "
                    f"{expected_size}"
                )
                return None
            binary = mask.point(lambda value: 255 if value >= 128 else 0)
            bounds = binary.getbbox()
            if bounds is None:
                errors.append(f"{label}: mask contains no subject pixels")
                return None
            left, top, right, bottom = bounds
            foreground_pixels = binary.histogram()[255]
            return {
                "bbox_width": (right - left) / mask.width,
                "bbox_height": (bottom - top) / mask.height,
                "coverage": foreground_pixels / (mask.width * mask.height),
            }
    except (OSError, ValueError) as error:
        errors.append(f"{label}: unreadable mask: {error}")
        return None


def image_delta(left: Path, right: Path) -> float:
    with Image.open(left).convert("RGB") as first, Image.open(right).convert("RGB") as second:
        if first.size != second.size:
            second = second.resize(first.size, Image.Resampling.LANCZOS)
        difference = ImageChops.difference(first, second)
        return float(statistics.mean(ImageStat.Stat(difference).mean))


def exact_pixel_ratio(left: Path, right: Path) -> float:
    with Image.open(left).convert("RGB") as first, Image.open(right).convert("RGB") as second:
        if first.size != second.size:
            second = second.resize(first.size, Image.Resampling.LANCZOS)
        difference = ImageChops.difference(first, second)
        histogram = difference.convert("L").histogram()
        return histogram[0] / (first.width * first.height)


def frame_regeneration_score_block(
    label: str,
    scores: Any,
    errors: list[str],
) -> None:
    if not isinstance(scores, dict):
        errors.append(f"{label}: requires human_review")
        return
    for criterion in FRAME_REGENERATION_SCORES:
        value = scores.get(criterion)
        if not isinstance(value, (int, float)):
            errors.append(f"{label}: missing human score '{criterion}'")
        elif value < FRAME_REGENERATION_FLOOR:
            errors.append(
                f"{label}: {criterion}={value:g} is below "
                f"{FRAME_REGENERATION_FLOOR:g}"
            )


def validate_frame_regeneration_manifest(
    manifest: dict[str, Any],
    frame_count: int,
    manifest_dir: Path,
) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    reports: list[dict[str, Any]] = []
    if manifest.get("schema") != "cinematic-frame-regeneration-v1":
        errors.append("frame regeneration manifest requires schema cinematic-frame-regeneration-v1")
    origin = manifest.get("frame_index_origin")
    if origin != 0:
        errors.append("frame regeneration manifest requires frame_index_origin 0")
        origin = 0
    canvas_policy = manifest.get("canvas_policy", "exact_native_size")
    if canvas_policy not in (
        "exact_native_size",
        "uniform_full_canvas_normalization",
    ):
        errors.append(
            "frame regeneration manifest canvas_policy must be "
            "exact_native_size or uniform_full_canvas_normalization"
        )
        canvas_policy = "exact_native_size"
    delivery_size = manifest.get("delivery_size")
    maximum_aspect_error = manifest.get("maximum_native_aspect_error", 0.002)
    aspect_delivery_size = list(PRODUCTION_DELIVERY_SIZE)
    aspect_error_tolerance = 0.002
    if canvas_policy == "uniform_full_canvas_normalization":
        if (
            not isinstance(delivery_size, list)
            or len(delivery_size) != 2
            or not all(isinstance(value, int) and value > 0 for value in delivery_size)
        ):
            errors.append(
                "uniform_full_canvas_normalization requires positive "
                "delivery_size [width, height]"
            )
            delivery_size = None
        elif tuple(delivery_size) != PRODUCTION_DELIVERY_SIZE:
            errors.append(
                "uniform_full_canvas_normalization delivery_size must be "
                f"{list(PRODUCTION_DELIVERY_SIZE)} for production"
            )
        if (
            not isinstance(maximum_aspect_error, (int, float))
            or maximum_aspect_error < 0
            or maximum_aspect_error > 0.1
        ):
            errors.append("maximum_native_aspect_error must be in [0, 0.1]")
            maximum_aspect_error = 0.002
        aspect_error_tolerance = maximum_aspect_error
    frames = manifest.get("frames")
    if not isinstance(frames, list) or not frames:
        return errors + ["frame regeneration manifest requires at least one frame"], reports

    last_frame = origin + frame_count - 1
    seen_frames: set[int] = set()
    for entry_index, frame in enumerate(frames):
        if not isinstance(frame, dict):
            errors.append(f"frame entry {entry_index}: invalid")
            continue
        frame_number = frame.get("frame")
        label = f"frame {frame_number}" if isinstance(frame_number, int) else f"frame entry {entry_index}"
        if not isinstance(frame_number, int):
            errors.append(f"{label}: frame must be an integer")
            continue
        if frame_number < origin or frame_number > last_frame:
            errors.append(f"{label}: frame is outside video range {origin}-{last_frame}")
        if frame_number in seen_frames:
            errors.append(f"{label}: duplicate frame")
        seen_frames.add(frame_number)

        method = frame.get("generation_method")
        if method != FULL_FRAME_GENERATION_METHOD:
            errors.append(
                f"{label}: generation_method must be "
                f"{FULL_FRAME_GENERATION_METHOD}"
            )
        method_text = str(method).lower()
        declared_techniques = frame.get("delivery_techniques")
        if not isinstance(declared_techniques, list):
            errors.append(f"{label}: delivery_techniques must be a list")
            declared_techniques = []
        technique_text = " ".join(str(value).lower() for value in declared_techniques)
        for forbidden in FORBIDDEN_TEMPORAL_METHODS:
            if forbidden in method_text or forbidden in technique_text:
                errors.append(f"{label}: forbidden delivery technique '{forbidden}'")
        if frame.get("temporal_derivation") != "none":
            errors.append(f"{label}: temporal_derivation must be 'none'")

        attempt = frame.get("attempt")
        if not isinstance(attempt, int) or attempt < 1:
            errors.append(f"{label}: attempt must be a positive integer")
        prompt_hash = frame.get("prompt_sha256")
        if not isinstance(prompt_hash, str) or not SHA256_PATTERN.fullmatch(prompt_hash):
            errors.append(f"{label}: prompt_sha256 must be 64 hexadecimal characters")
        prompt_path = artifact_path(
            frame.get("prompt"),
            f"{label} prompt",
            manifest_dir,
            errors,
        )
        if (
            prompt_path
            and isinstance(prompt_hash, str)
            and SHA256_PATTERN.fullmatch(prompt_hash)
            and sha256_file(prompt_path).lower() != prompt_hash.lower()
        ):
            errors.append(f"{label}: prompt_sha256 does not match prompt artifact")
        generation_references = frame.get("generation_references")
        generation_reference_reports: list[dict[str, Any]] = []
        if not isinstance(generation_references, list) or not generation_references:
            errors.append(f"{label}: requires generation_references")
            generation_references = []
        for reference_index, reference in enumerate(generation_references):
            reference_label = f"{label} generation_reference {reference_index}"
            if not isinstance(reference, dict):
                errors.append(f"{reference_label}: invalid")
                continue
            reference_path = artifact_path(
                reference,
                reference_label,
                manifest_dir,
                errors,
            )
            reference_role = reference.get("role")
            if reference_role not in (
                "appearance_authority",
                "accepted_neighbor",
                "negative_position_example",
                "position_only",
            ):
                errors.append(f"{reference_label}: invalid role")
            if reference.get("used_as_delivery_pixels") is not False:
                errors.append(
                    f"{reference_label}: used_as_delivery_pixels must be false"
                )
            generation_reference_reports.append(
                {
                    "role": reference_role,
                    "path": str(reference_path) if reference_path else None,
                }
            )
        action_state = frame.get("action_state")
        if action_state not in ("motion", "hold"):
            errors.append(f"{label}: action_state must be 'motion' or 'hold'")
        elif action_state == "hold" and not frame.get("hold_reason"):
            errors.append(f"{label}: an intentional hold requires hold_reason")
        frame_regeneration_score_block(label, frame.get("human_review"), errors)

        candidate = artifact_path(
            frame.get("candidate"),
            f"{label} candidate",
            manifest_dir,
            errors,
        )
        previous = artifact_path(
            frame.get("previous_reference"),
            f"{label} previous_reference",
            manifest_dir,
            errors,
        ) if frame_number > origin else None
        following_data = frame.get("next_reference")
        following = (
            artifact_path(
                following_data,
                f"{label} next_reference",
                manifest_dir,
                errors,
            )
            if following_data is not None
            else None
        )
        candidate_size = image_size(candidate, f"{label} candidate", errors) if candidate else None
        if candidate_size is not None:
            validate_native_canvas_aspect(
                candidate_size,
                aspect_delivery_size,
                aspect_error_tolerance,
                f"{label} candidate",
                errors,
            )
        for reference_name, reference in (
            ("previous_reference", previous),
            ("next_reference", following),
        ):
            if reference and candidate_size:
                reference_size = image_size(reference, f"{label} {reference_name}", errors)
                if reference_size is not None:
                    if canvas_policy == "exact_native_size" and reference_size != candidate_size:
                        errors.append(
                            f"{label}: {reference_name} size {reference_size} does not "
                            f"match candidate size {candidate_size}"
                        )
                    validate_native_canvas_aspect(
                        reference_size,
                        aspect_delivery_size,
                        aspect_error_tolerance,
                        f"{label} {reference_name}",
                        errors,
                    )

        guide = frame.get("position_guide")
        guide_path: Path | None = None
        guide_metrics: dict[str, Any] | None = None
        if guide is not None:
            if not isinstance(guide, dict):
                errors.append(f"{label}: position_guide must be an object")
            else:
                guide_path = artifact_path(
                    guide,
                    f"{label} position_guide",
                    manifest_dir,
                    errors,
                )
                if guide.get("role") != "position_only":
                    errors.append(f"{label}: position_guide role must be 'position_only'")
                if guide.get("used_as_delivery_pixels") is not False:
                    errors.append(
                        f"{label}: position_guide used_as_delivery_pixels must be false"
                    )
                if candidate and guide_path and sha256_file(candidate) == sha256_file(guide_path):
                    errors.append(f"{label}: candidate may not reuse position-guide pixels")
                if candidate and guide_path:
                    guide_delta = image_delta(candidate, guide_path)
                    guide_exact_ratio = exact_pixel_ratio(candidate, guide_path)
                    min_guide_delta = guide.get("min_mean_pixel_delta", 2.0)
                    max_exact_ratio = guide.get("max_exact_pixel_ratio", 0.05)
                    if not isinstance(min_guide_delta, (int, float)) or min_guide_delta < 0:
                        errors.append(
                            f"{label}: position_guide min_mean_pixel_delta must be nonnegative"
                        )
                        min_guide_delta = 2.0
                    if (
                        not isinstance(max_exact_ratio, (int, float))
                        or max_exact_ratio < 0
                        or max_exact_ratio > 1
                    ):
                        errors.append(
                            f"{label}: position_guide max_exact_pixel_ratio must be in [0, 1]"
                        )
                        max_exact_ratio = 0.05
                    if guide_delta < min_guide_delta:
                        errors.append(
                            f"{label}: candidate-to-guide mean pixel delta "
                            f"{guide_delta:.4f} is below {min_guide_delta:.4f}"
                        )
                    if guide_exact_ratio > max_exact_ratio:
                        errors.append(
                            f"{label}: exact guide-pixel ratio {guide_exact_ratio:.5f} "
                            f"exceeds {max_exact_ratio:.5f}"
                        )
                    guide_metrics = {
                        "candidate_mean_pixel_delta": round(guide_delta, 4),
                        "exact_pixel_ratio": round(guide_exact_ratio, 6),
                        "min_mean_pixel_delta": min_guide_delta,
                        "max_exact_pixel_ratio": max_exact_ratio,
                    }

        subjects = frame.get("subjects")
        subject_reports: list[dict[str, Any]] = []
        if not isinstance(subjects, list) or not subjects:
            errors.append(f"{label}: requires at least one audited subject")
            subjects = []
        for subject_index, subject in enumerate(subjects):
            if not isinstance(subject, dict):
                errors.append(f"{label} subject {subject_index}: invalid")
                continue
            subject_id = subject.get("id")
            subject_label = f"{label} subject {subject_id or subject_index}"
            if not subject_id:
                errors.append(f"{subject_label}: missing id")
            candidate_mask = artifact_path(
                subject.get("candidate_mask"),
                f"{subject_label} candidate_mask",
                manifest_dir,
                errors,
            )
            guide_mask = (
                artifact_path(
                    subject.get("position_guide_mask"),
                    f"{subject_label} position_guide_mask",
                    manifest_dir,
                    errors,
                )
                if guide_path
                else None
            )
            position_anchor = subject.get("position_anchor", "center")
            if position_anchor not in (
                "center",
                "bbox_left",
                "bbox_right",
                "bbox_top",
                "bbox_bottom",
                "leading_edge_left",
                "leading_edge_right",
            ):
                errors.append(f"{subject_label}: invalid position_anchor")
                position_anchor = "center"
            position_axis = subject.get("position_axis", "xy")
            if position_axis not in ("x", "y", "xy"):
                errors.append(f"{subject_label}: position_axis must be x, y, or xy")
                position_axis = "xy"
            candidate_position = (
                mask_position(
                    candidate_mask,
                    candidate_size,
                    position_anchor,
                    f"{subject_label} candidate_mask",
                    errors,
                )
                if candidate_mask
                else None
            )
            candidate_geometry = (
                mask_geometry(
                    candidate_mask,
                    candidate_size,
                    f"{subject_label} candidate_mask",
                    errors,
                )
                if candidate_mask
                else None
            )
            guide_size = (
                image_size(guide_path, f"{label} position_guide", errors)
                if guide_path
                else candidate_size
            )
            guide_position = (
                mask_position(
                    guide_mask,
                    guide_size,
                    position_anchor,
                    f"{subject_label} position_guide_mask",
                    errors,
                )
                if guide_mask
                else None
            )
            max_position_error = subject.get(
                "max_position_error",
                subject.get("max_center_error", 0.015),
            )
            if (
                not isinstance(max_position_error, (int, float))
                or max_position_error <= 0
                or max_position_error > 1
            ):
                errors.append(f"{subject_label}: max_position_error must be in (0, 1]")
                max_position_error = 0.015
            required_direction = subject.get("required_direction")
            if required_direction not in (None, "right", "left", "up", "down", "still"):
                errors.append(
                    f"{subject_label}: required_direction must be right, left, up, "
                    "down, still, or omitted"
                )
                required_direction = None
            max_step_error = subject.get("max_step_error")
            if max_step_error is not None and (
                not isinstance(max_step_error, (int, float))
                or max_step_error <= 0
                or max_step_error > 1
            ):
                errors.append(f"{subject_label}: max_step_error must be in (0, 1]")
                max_step_error = None
            max_cross_axis_step = subject.get("max_cross_axis_step")
            if max_cross_axis_step is not None and (
                not isinstance(max_cross_axis_step, (int, float))
                or max_cross_axis_step <= 0
                or max_cross_axis_step > 1
            ):
                errors.append(
                    f"{subject_label}: max_cross_axis_step must be in (0, 1]"
                )
                max_cross_axis_step = None
            max_bbox_height_step = subject.get("max_bbox_height_step")
            if max_bbox_height_step is not None and (
                not isinstance(max_bbox_height_step, (int, float))
                or max_bbox_height_step <= 0
                or max_bbox_height_step > 1
            ):
                errors.append(
                    f"{subject_label}: max_bbox_height_step must be in (0, 1]"
                )
                max_bbox_height_step = None
            position_error = None
            if candidate_position and guide_position:
                if position_axis == "x":
                    position_error = abs(candidate_position[0] - guide_position[0])
                elif position_axis == "y":
                    position_error = abs(candidate_position[1] - guide_position[1])
                else:
                    position_error = math.dist(candidate_position, guide_position)
                if position_error > max_position_error:
                    errors.append(
                        f"{subject_label}: position error {position_error:.5f} exceeds "
                        f"{max_position_error:.5f}"
                    )
            subject_reports.append(
                {
                    "id": subject_id,
                    "position_anchor": position_anchor,
                    "position_axis": position_axis,
                    "candidate_position": candidate_position,
                    "candidate_geometry": candidate_geometry,
                    "guide_position": guide_position,
                    "position_error": round(position_error, 6)
                    if position_error is not None
                    else None,
                    "max_position_error": max_position_error,
                    "required_direction": required_direction,
                    "max_step_error": max_step_error,
                    "max_cross_axis_step": max_cross_axis_step,
                    "max_bbox_height_step": max_bbox_height_step,
                }
            )

        reports.append(
            {
                "frame": frame_number,
                "native_size": list(candidate_size) if candidate_size else None,
                "canvas_policy": canvas_policy,
                "delivery_size": delivery_size,
                "prompt": str(prompt_path) if prompt_path else None,
                "generation_references": generation_reference_reports,
                "candidate_to_previous_delta": round(image_delta(candidate, previous), 4)
                if candidate and previous
                else None,
                "candidate_to_next_delta": round(image_delta(candidate, following), 4)
                if candidate and following
                else None,
                "position_guide": guide_metrics,
                "subjects": subject_reports,
            }
        )
    subject_sequences: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for report in reports:
        frame_number = report.get("frame")
        if not isinstance(frame_number, int):
            continue
        for subject in report.get("subjects", []):
            subject_id = subject.get("id")
            if subject_id:
                subject_sequences.setdefault(subject_id, []).append(
                    (frame_number, subject)
                )
    for subject_id, sequence in subject_sequences.items():
        ordered = sorted(sequence, key=lambda item: item[0])
        for (previous_frame, previous_subject), (
            current_frame,
            current_subject,
        ) in zip(ordered, ordered[1:]):
            if current_frame != previous_frame + 1:
                continue
            previous_candidate = previous_subject.get("candidate_position")
            current_candidate = current_subject.get("candidate_position")
            previous_guide = previous_subject.get("guide_position")
            current_guide = current_subject.get("guide_position")
            previous_geometry = previous_subject.get("candidate_geometry")
            current_geometry = current_subject.get("candidate_geometry")
            if isinstance(previous_geometry, dict) and isinstance(
                current_geometry,
                dict,
            ):
                bbox_height_step = (
                    current_geometry["bbox_height"]
                    - previous_geometry["bbox_height"]
                )
                current_subject["bbox_height_step_from_previous"] = round(
                    bbox_height_step,
                    6,
                )
                max_bbox_height_step = current_subject.get(
                    "max_bbox_height_step"
                )
                if max_bbox_height_step is None:
                    max_bbox_height_step = previous_subject.get(
                        "max_bbox_height_step"
                    )
                elif previous_subject.get("max_bbox_height_step") not in (
                    None,
                    max_bbox_height_step,
                ):
                    errors.append(
                        f"subject {subject_id}: max_bbox_height_step changes "
                        f"between frames {previous_frame} and {current_frame}"
                    )
                if (
                    max_bbox_height_step is not None
                    and abs(bbox_height_step) > max_bbox_height_step
                ):
                    errors.append(
                        f"subject {subject_id}: frame "
                        f"{previous_frame}->{current_frame} bbox-height step "
                        f"{bbox_height_step:.5f} exceeds "
                        f"{max_bbox_height_step:.5f}"
                    )
            if not all(
                isinstance(position, tuple)
                for position in (
                    previous_candidate,
                    current_candidate,
                    previous_guide,
                    current_guide,
                )
            ):
                continue
            direction = current_subject.get("required_direction")
            previous_direction = previous_subject.get("required_direction")
            if direction is None:
                direction = previous_direction
            elif previous_direction not in (None, direction):
                errors.append(
                    f"subject {subject_id}: required_direction changes between "
                    f"frames {previous_frame} and {current_frame}"
                )
            axis = 1 if direction in ("up", "down") else 0
            cross_axis = 0 if axis == 1 else 1
            actual_step = current_candidate[axis] - previous_candidate[axis]
            expected_step = current_guide[axis] - previous_guide[axis]
            max_step_error = current_subject.get("max_step_error")
            if max_step_error is None:
                max_step_error = previous_subject.get("max_step_error")
            elif previous_subject.get("max_step_error") not in (
                None,
                max_step_error,
            ):
                errors.append(
                    f"subject {subject_id}: max_step_error changes between "
                    f"frames {previous_frame} and {current_frame}"
                )
            step_error = abs(actual_step - expected_step)
            current_subject["step_from_previous"] = round(actual_step, 6)
            current_subject["expected_step_from_previous"] = round(
                expected_step,
                6,
            )
            current_subject["step_error"] = round(step_error, 6)
            if max_step_error is not None and step_error > max_step_error:
                errors.append(
                    f"subject {subject_id}: frame {previous_frame}->{current_frame} "
                    f"step error {step_error:.5f} exceeds {max_step_error:.5f}"
                )
            max_cross_axis_step = current_subject.get("max_cross_axis_step")
            if max_cross_axis_step is None:
                max_cross_axis_step = previous_subject.get("max_cross_axis_step")
            elif previous_subject.get("max_cross_axis_step") not in (
                None,
                max_cross_axis_step,
            ):
                errors.append(
                    f"subject {subject_id}: max_cross_axis_step changes between "
                    f"frames {previous_frame} and {current_frame}"
                )
            cross_axis_step = (
                current_candidate[cross_axis] - previous_candidate[cross_axis]
            )
            current_subject["cross_axis_step_from_previous"] = round(
                cross_axis_step,
                6,
            )
            if (
                max_cross_axis_step is not None
                and abs(cross_axis_step) > max_cross_axis_step
            ):
                errors.append(
                    f"subject {subject_id}: frame {previous_frame}->{current_frame} "
                    f"cross-axis step {cross_axis_step:.5f} exceeds "
                    f"{max_cross_axis_step:.5f}"
                )
            direction_failed = (
                (direction == "right" and actual_step <= 0)
                or (direction == "left" and actual_step >= 0)
                or (direction == "down" and actual_step <= 0)
                or (direction == "up" and actual_step >= 0)
                or (
                    direction == "still"
                    and max_step_error is not None
                    and abs(actual_step) > max_step_error
                )
            )
            if direction_failed:
                errors.append(
                    f"subject {subject_id}: frame {previous_frame}->{current_frame} "
                    f"moves {actual_step:.5f}, violating required_direction "
                    f"'{direction}'"
                )
    return errors, reports


def score_block(name: str, scores: dict[str, Any], floor: float, errors: list[str]) -> None:
    for criterion in REQUIRED_SCORES:
        value = scores.get(criterion)
        if not isinstance(value, (int, float)):
            errors.append(f"{name}: missing human score '{criterion}'")
        elif value < floor:
            errors.append(f"{name}: {criterion}={value:g} is below {floor:g}")


def validate_track(scene: dict[str, Any], track: dict[str, Any], errors: list[str]) -> None:
    label = f"scene {scene['id']} track {track.get('id', '<unnamed>')}"
    values = track.get("samples")
    if not isinstance(values, list) or not values:
        errors.append(f"{label}: requires per-frame samples")
        return
    by_frame: dict[int, dict[str, Any]] = {}
    for sample in values:
        if not isinstance(sample, dict) or not isinstance(sample.get("frame"), int):
            errors.append(f"{label}: invalid sample")
            continue
        frame = sample["frame"]
        if frame in by_frame:
            errors.append(f"{label}: duplicate frame {frame}")
        by_frame[frame] = sample
    for frame in range(scene["start_frame"], scene["end_frame"] + 1):
        if frame not in by_frame:
            errors.append(f"{label}: missing frame {frame}")
            break
    max_step = track.get("max_step")
    if isinstance(max_step, (int, float)):
        ordered = [by_frame.get(frame) for frame in range(scene["start_frame"], scene["end_frame"] + 1)]
        for previous, current in zip(ordered, ordered[1:]):
            if not previous or not current or not previous.get("visible", True) or not current.get("visible", True):
                continue
            if all(isinstance(item.get(key), (int, float)) for item in (previous, current) for key in ("x", "y")):
                step = ((current["x"] - previous["x"]) ** 2 + (current["y"] - previous["y"]) ** 2) ** 0.5
                if step > max_step:
                    errors.append(f"{label}: frame {current['frame']} moves {step:.3f}, above max_step {max_step:.3f}")
                    break


def validate_manifest(
    manifest: dict[str, Any],
    frame_count: int,
    scene_floor: float = SCENE_FLOOR,
    identity_floor: float = IDENTITY_FLOOR,
) -> list[str]:
    errors: list[str] = []
    scenes = manifest.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        return ["manifest requires at least one scene"]
    origin = manifest.get("frame_index_origin", 1)
    if origin not in (0, 1):
        errors.append("frame_index_origin must be 0 or 1")
        origin = 1
    previous_end = origin - 1
    expected_last_frame = origin + frame_count - 1
    for scene in scenes:
        for key in (
            "id", "background_id", "start_frame", "end_frame", "characters",
            "tracks", "contacts", "review",
        ):
            if key not in scene:
                errors.append(f"scene missing '{key}'")
        if not isinstance(scene.get("start_frame"), int) or not isinstance(scene.get("end_frame"), int):
            continue
        if scene["start_frame"] != previous_end + 1:
            errors.append(f"scene {scene.get('id')}: scenes must be contiguous and start at frame {previous_end + 1}")
        if scene["end_frame"] < scene["start_frame"] or scene["end_frame"] > expected_last_frame:
            errors.append(f"scene {scene.get('id')}: invalid frame range")
        previous_end = scene["end_frame"]
        if isinstance(scene.get("review"), dict):
            score_block(f"scene {scene.get('id')}", scene["review"], scene_floor, errors)
        tracks = scene.get("tracks", [])
        if not isinstance(tracks, list) or not tracks:
            errors.append(f"scene {scene.get('id')}: requires at least one per-frame track")
            tracks = []
        tracked_characters = {track.get("character_id") for track in tracks if isinstance(track, dict)}
        for character_id in scene.get("characters", []):
            if character_id not in tracked_characters:
                errors.append(f"scene {scene.get('id')}: character {character_id} has no tracked landmark")
        for track in tracks:
            if isinstance(track, dict):
                validate_track(scene, track, errors)
            else:
                errors.append(f"scene {scene.get('id')}: invalid track")
        contacts = scene.get("contacts", [])
        if not isinstance(contacts, list):
            errors.append(f"scene {scene.get('id')}: contacts must be a list")
        else:
            for contact in contacts:
                if not isinstance(contact, dict):
                    errors.append(f"scene {scene.get('id')}: invalid contact")
                    continue
                if not contact.get("id") or not isinstance(contact.get("start_frame"), int) or not isinstance(
                    contact.get("end_frame"), int
                ):
                    errors.append(f"scene {scene.get('id')}: contact requires id/start_frame/end_frame")
                elif (
                    contact["start_frame"] < scene["start_frame"]
                    or contact["end_frame"] > scene["end_frame"]
                    or contact["end_frame"] < contact["start_frame"]
                ):
                    errors.append(f"scene {scene.get('id')}: contact {contact.get('id')} is outside the scene")
    if previous_end != expected_last_frame:
        errors.append(
            f"scenes end at frame {previous_end}, but video ends at frame {expected_last_frame}"
        )

    passports = manifest.get("character_passports")
    if not isinstance(passports, dict) or not passports:
        errors.append("manifest requires character_passports")
    else:
        for character_id, passport in passports.items():
            if not isinstance(passport, dict):
                errors.append(f"character passport {character_id}: invalid")
                continue
            score_block(
                f"character {character_id}",
                passport.get("global_review", {}),
                identity_floor,
                errors,
            )
            if not passport.get("reference_image") or not passport.get("landmarks"):
                errors.append(f"character {character_id}: requires reference_image and canonical landmarks")
        for scene in scenes:
            for character_id in scene.get("characters", []):
                if character_id not in passports:
                    errors.append(f"scene {scene.get('id')}: character {character_id} has no passport")
    return errors


def bootstrap(video: Path, output: Path) -> None:
    info = video_info(video)
    fps = float(info["fps"])
    count = int(info["frame_count"])
    with tempfile.TemporaryDirectory(prefix="cinematic-audit-") as temp:
        cut_frames = cuts(extract_frames(video, Path(temp), fps, count))
    starts = [0] + cut_frames
    ends = [cut - 1 for cut in cut_frames] + [count]
    ends[-1] = count - 1
    manifest = {
        "schema": "cinematic-quality-v2",
        "frame_index_origin": 0,
        "video": {
            "path": str(video),
            "fps": fps,
            "frame_count": count,
            "geometry": video_geometry_report(info),
        },
        "character_passports": {
            "REPLACE_WITH_CHARACTER_ID": {
                "reference_image": "REPLACE_WITH_APPROVED_TURNAROUND.png",
                "landmarks": ["REPLACE_WITH_CANONICAL_LANDMARKS"],
                "global_review": {key: 0 for key in REQUIRED_SCORES},
            }
        },
        "scenes": [
            {"id": f"scene_{index + 1:02d}", "background_id": "REPLACE_WITH_LAYOUT_ID",
             "start_frame": start, "end_frame": end, "characters": ["REPLACE_WITH_CHARACTER_ID"],
             "tracks": [{"id": "REPLACE_WITH_FACE_OR_BODY_ANCHOR", "character_id": "REPLACE_WITH_CHARACTER_ID",
                         "max_step": 0.02, "samples": []}],
             "contacts": [], "review": {key: 0 for key in REQUIRED_SCORES}}
            for index, (start, end) in enumerate(zip(starts, ends))
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"BOOTSTRAP|frames={count}|fps={fps:g}|candidate_scenes={len(starts)}|manifest={output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument(
        "--frame-regeneration-manifest",
        type=Path,
        help="audit full-frame regeneration provenance and position-only guides",
    )
    parser.add_argument("--bootstrap", type=Path, help="write a review-manifest skeleton")
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="write/print automatic pixel-transition evidence without claiming artistic approval",
    )
    parser.add_argument("--report", type=Path, help="write JSON audit report")
    parser.add_argument(
        "--lattice",
        type=int,
        default=9,
        help="segment period to measure in automatic analysis (0 disables)",
    )
    parser.add_argument(
        "--profile",
        choices=sorted(THRESHOLD_PROFILES),
        default="production",
        help="named score-floor profile; production remains the blocking default",
    )
    parser.add_argument("--scene-floor", type=float, help="override the profile scene-score floor")
    parser.add_argument("--identity-floor", type=float, help="override the profile passport-score floor")
    args = parser.parse_args()
    action_count = sum((
        bool(args.manifest),
        bool(args.frame_regeneration_manifest),
        bool(args.bootstrap),
        args.analyze,
    ))
    if action_count != 1:
        parser.error(
            "provide exactly one of --manifest, --frame-regeneration-manifest, "
            "--bootstrap, or --analyze"
        )
    if not args.video.is_file():
        parser.error(f"video does not exist: {args.video}")
    if args.lattice < 0:
        parser.error("lattice must be zero or a positive integer")
    if args.analyze:
        analyze(args.video, args.report, args.lattice)
        return 0
    if args.bootstrap:
        bootstrap(args.video, args.bootstrap)
        return 0
    if args.frame_regeneration_manifest:
        info = video_info(args.video)
        fps = float(info["fps"])
        count = int(info["frame_count"])
        manifest_path = args.frame_regeneration_manifest.resolve()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        errors = validate_video_delivery(info)
        frame_errors, frame_reports = validate_frame_regeneration_manifest(
            manifest,
            count,
            manifest_path.parent,
        )
        errors.extend(frame_errors)
        report = {
            "schema": "cinematic-frame-regeneration-report-v1",
            "video": str(args.video),
            "fps": fps,
            "frame_count": count,
            "geometry": video_geometry_report(info),
            "passed": not errors,
            "errors": errors,
            "frames": frame_reports,
        }
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(
                json.dumps(report, indent=2) + "\n",
                encoding="utf-8",
            )
        for error in errors:
            print(f"FRAME_REGENERATION_AUDIT|FAIL|{error}")
        print(
            "FRAME_REGENERATION_AUDIT|"
            f"{'PASS' if not errors else 'FAIL'}|"
            f"frames={len(frame_reports)}|errors={len(errors)}"
        )
        return 0 if not errors else 1
    profile_scene_floor, profile_identity_floor = THRESHOLD_PROFILES[args.profile]
    scene_floor = args.scene_floor if args.scene_floor is not None else profile_scene_floor
    identity_floor = args.identity_floor if args.identity_floor is not None else profile_identity_floor
    for name, value in (("scene", scene_floor), ("identity", identity_floor)):
        if not 0.0 <= value <= 5.0:
            parser.error(f"{name} floor must be between 0 and 5")
    info = video_info(args.video)
    fps = float(info["fps"])
    count = int(info["frame_count"])
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_video_delivery(info)
    errors.extend(validate_manifest(manifest, count, scene_floor, identity_floor))
    report = {"schema": "cinematic-quality-report-v1", "video": str(args.video), "fps": fps,
              "frame_count": count, "geometry": video_geometry_report(info),
              "threshold_profile": args.profile,
              "thresholds": {"scene_floor": scene_floor, "identity_floor": identity_floor},
              "passed": not errors, "errors": errors}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for error in errors:
        print(f"CINEMATIC_AUDIT|FAIL|{error}")
    print(f"CINEMATIC_AUDIT|{'PASS' if not errors else 'FAIL'}|errors={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"CINEMATIC_AUDIT|ERROR|{error}", file=sys.stderr)
        raise SystemExit(2)
