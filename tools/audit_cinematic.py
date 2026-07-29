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
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
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


def video_info(video: Path) -> tuple[float, int]:
    data = json.loads(run([command("ffprobe"), "-v", "error", "-select_streams", "v:0",
                           "-show_entries", "stream=avg_frame_rate,nb_frames", "-of", "json", str(video)]))
    stream = data["streams"][0]
    n, d = stream["avg_frame_rate"].split("/")
    fps = float(n) / float(d)
    count = int(stream.get("nb_frames") or 0)
    if fps <= 0 or count <= 0:
        fail("video must expose a positive frame rate and frame count")
    return fps, count


def extract_frames(video: Path, destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    run([command("ffmpeg"), "-hide_banner", "-loglevel", "error", "-i", str(video),
         "-vsync", "0", str(destination / "frame_%06d.png")])
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
    ordered = sorted(deltas)
    median = ordered[len(ordered) // 2]
    # Conservative: reviewers may split a long shot further, but a cut is not
    # accidentally scored as continuity jitter.
    threshold = max(24.0, median * 3.5)
    return [index + 2 for index, value in enumerate(deltas) if value >= threshold]


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
    by_frame = {sample.get("frame"): sample for sample in values if isinstance(sample, dict)}
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
    previous_end = 0
    for scene in scenes:
        for key in ("id", "background_id", "start_frame", "end_frame", "characters", "tracks", "review"):
            if key not in scene:
                errors.append(f"scene missing '{key}'")
        if not isinstance(scene.get("start_frame"), int) or not isinstance(scene.get("end_frame"), int):
            continue
        if scene["start_frame"] != previous_end + 1:
            errors.append(f"scene {scene.get('id')}: scenes must be contiguous and start at frame {previous_end + 1}")
        if scene["end_frame"] < scene["start_frame"] or scene["end_frame"] > frame_count:
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
    if previous_end != frame_count:
        errors.append(f"scenes end at frame {previous_end}, but video has {frame_count} frames")

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
        cut_frames = cuts(extract_frames(video, Path(temp)))
    starts = [1] + cut_frames
    ends = [cut - 1 for cut in cut_frames] + [count]
    manifest = {
        "schema": "cinematic-quality-v1",
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
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"BOOTSTRAP|frames={count}|fps={fps:g}|candidate_scenes={len(starts)}|manifest={output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--bootstrap", type=Path, help="write a review-manifest skeleton")
    parser.add_argument("--report", type=Path, help="write JSON audit report")
    parser.add_argument(
        "--profile",
        choices=sorted(THRESHOLD_PROFILES),
        default="production",
        help="named score-floor profile; production remains the blocking default",
    )
    parser.add_argument("--scene-floor", type=float, help="override the profile scene-score floor")
    parser.add_argument("--identity-floor", type=float, help="override the profile passport-score floor")
    args = parser.parse_args()
    if bool(args.manifest) == bool(args.bootstrap):
        parser.error("provide exactly one of --manifest or --bootstrap")
    if not args.video.is_file():
        parser.error(f"video does not exist: {args.video}")
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
