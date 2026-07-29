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
import json
import math
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
ANALYSIS_SIZE = (320, 180)
BOIL_THRESHOLD = 8


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


def video_info(video: Path) -> tuple[float, int]:
    data = json.loads(run([
        command("ffprobe"),
        "-v", "error",
        "-count_frames",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=avg_frame_rate,r_frame_rate,nb_frames,nb_read_frames,duration:format=duration",
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
    return fps, count


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
    fps, count = video_info(video)
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
    fps, count = video_info(video)
    with tempfile.TemporaryDirectory(prefix="cinematic-audit-") as temp:
        cut_frames = cuts(extract_frames(video, Path(temp), fps, count))
    starts = [0] + cut_frames
    ends = [cut - 1 for cut in cut_frames] + [count]
    ends[-1] = count - 1
    manifest = {
        "schema": "cinematic-quality-v2",
        "frame_index_origin": 0,
        "video": {"path": str(video), "fps": fps, "frame_count": count},
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
    action_count = sum((bool(args.manifest), bool(args.bootstrap), args.analyze))
    if action_count != 1:
        parser.error("provide exactly one of --manifest, --bootstrap, or --analyze")
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
    profile_scene_floor, profile_identity_floor = THRESHOLD_PROFILES[args.profile]
    scene_floor = args.scene_floor if args.scene_floor is not None else profile_scene_floor
    identity_floor = args.identity_floor if args.identity_floor is not None else profile_identity_floor
    for name, value in (("scene", scene_floor), ("identity", identity_floor)):
        if not 0.0 <= value <= 5.0:
            parser.error(f"{name} floor must be between 0 and 5")
    fps, count = video_info(args.video)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_manifest(manifest, count, scene_floor, identity_floor)
    report = {"schema": "cinematic-quality-report-v1", "video": str(args.video), "fps": fps,
              "frame_count": count, "threshold_profile": args.profile,
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
