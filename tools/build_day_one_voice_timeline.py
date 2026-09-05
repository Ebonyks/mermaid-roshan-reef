"""Build and validate hash-bound voice plans for Day One editorial videos.

This tool intentionally does not mux audio or copy video into the project.  It
records editorial source metadata, maps authored voice cues to exact source
time spans, and emits a review-only mix plan.  A later audio pass can replace
``pending`` cue bindings with real, hash-bound audio without changing timing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "day-one-voice-timeline-v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_SHA256 = "3f84e5dd1402382067ad8fb06c66405acb71468fe096122aab18d9934b874b99"
EMPTY_AUDIO_SHA256 = hashlib.sha256(b"").hexdigest()
DEFAULT_SOURCE_PATH = (
    r"C:\Users\Peter\Downloads\grok-0e40140f-8759-4188-8e0f-6ba103909db8.mp4"
)
EXPECTED_CLIPS = [f"D1-C{index:02d}" for index in range(13)]


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_rate(value: str) -> float:
    try:
        rate = Fraction(value)
    except (ValueError, ZeroDivisionError):
        return 0.0
    return float(rate)


def _number(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _probe(path: Path, ffprobe_bin: str = "ffprobe") -> dict[str, Any]:
    command = [
        ffprobe_bin,
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def inspect_source(path: Path, ffprobe_bin: str = "ffprobe") -> dict[str, Any]:
    """Return deterministic metadata for one source, rejecting non-silent media."""

    if not path.is_file():
        raise ValueError(f"source does not exist: {path}")
    payload = _probe(path, ffprobe_bin)
    streams = payload.get("streams", [])
    videos = [stream for stream in streams if stream.get("codec_type") == "video"]
    audios = [stream for stream in streams if stream.get("codec_type") == "audio"]
    if len(videos) != 1:
        raise ValueError(f"source must contain exactly one video stream; found {len(videos)}")
    if audios:
        raise ValueError("source must be silent; an audio stream was found")
    video = videos[0]
    fps = _parse_rate(str(video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"))
    duration = _number(video.get("duration") or payload.get("format", {}).get("duration"))
    if duration <= 0 or fps <= 0:
        raise ValueError("source must expose positive duration and frame rate")
    source_hash = file_sha256(path)
    return {
        "source_sha256": source_hash,
        # The source is one silent video stream.  Keeping the container hash
        # as the video binding avoids an untracked demux/re-encode artifact.
        "video_sha256": source_hash,
        "video_hash_mode": "single_video_stream_container_sha256",
        # A silent source has a required, reproducible empty audio binding.
        "audio_sha256": EMPTY_AUDIO_SHA256,
        "audio_hash_mode": "sha256_empty_audio_stream",
        "duration_s": duration,
        "width": int(video.get("width", 0)),
        "height": int(video.get("height", 0)),
        "fps": fps,
        "frame_count": int(video.get("nb_frames") or 0),
        "audio_stream_count": 0,
        "codec": str(video.get("codec_name") or "unknown"),
    }


def _sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value.lower()):
        raise ValueError(f"{label} must be a 64-character lowercase SHA-256")


def _review_path(path: Path) -> None:
    """Prevent review artifacts from entering a runtime assets directory."""

    lowered = {part.lower() for part in path.resolve().parts}
    if "assets" in lowered:
        raise ValueError("review output must stay outside the runtime assets directory")


def empty_ledger() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "project": "Mermaid Roshan: Reef of Light",
        "purpose": "Day One contextual voice editorial intake",
        "runtime_delivery": False,
        "source_copy_policy": "preserve_external_source; never_copy_to_runtime",
        "sources": [],
        "incoming_uploads": {
            "window_hours": 48,
            "expected_clip_ids": EXPECTED_CLIPS,
            "schema_rule": "each upload is independently hash-bound and silent-video validated",
        },
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def save_json(path: Path, value: dict[str, Any]) -> None:
    _review_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value))


def intake_source(
    source_path: Path,
    ledger_path: Path,
    source_id: str,
    clip_ids: list[str],
    visual_acceptance: str = "unresolved",
    ffprobe_bin: str = "ffprobe",
) -> dict[str, Any]:
    metadata = inspect_source(source_path, ffprobe_bin)
    if metadata["source_sha256"] != SOURCE_SHA256:
        raise ValueError(
            "source hash mismatch; this intake only registers the supplied editorial reference "
            f"({SOURCE_SHA256})"
        )
    if not source_id or not clip_ids:
        raise ValueError("source_id and at least one clip_id are required")
    ledger = load_json(ledger_path) if ledger_path.is_file() else empty_ledger()
    if ledger.get("schema") != SCHEMA:
        raise ValueError(f"ledger schema must be {SCHEMA}")
    source = {
        "source_id": source_id,
        "clip_ids": sorted(set(clip_ids)),
        "source_kind": "editorial_rough",
        "source_path": str(source_path.resolve()),
        **metadata,
        "visual_acceptance": visual_acceptance,
        "accepted_for_delivery": False,
        "audio_mux_status": "not_permitted_pending_voice_review",
    }
    sources = [item for item in ledger.get("sources", []) if item.get("source_id") != source_id]
    sources.append(source)
    ledger["sources"] = sorted(sources, key=lambda item: item["source_id"])
    save_json(ledger_path, ledger)
    return source


def _source(ledger: dict[str, Any], source_id: str) -> dict[str, Any]:
    for source in ledger.get("sources", []):
        if source.get("source_id") == source_id:
            return source
    raise ValueError(f"ledger has no source {source_id}")


def validate_cues(ledger: dict[str, Any], sidecar: dict[str, Any], require_audio: bool = False) -> list[str]:
    errors: list[str] = []
    if sidecar.get("schema") != SCHEMA:
        errors.append(f"sidecar schema must be {SCHEMA}")
    source_id = sidecar.get("source_id")
    try:
        source = _source(ledger, str(source_id))
    except ValueError as exc:
        return [str(exc)]
    for key in ("source_sha256", "video_sha256", "audio_sha256"):
        try:
            _sha(source.get(key), f"source {key}")
        except ValueError as exc:
            errors.append(str(exc))
    if sidecar.get("source_sha256") != source.get("source_sha256"):
        errors.append("sidecar source_sha256 does not match ledger")
    if sidecar.get("video_sha256") != source.get("video_sha256"):
        errors.append("sidecar video_sha256 does not match ledger")
    if sidecar.get("audio_sha256") != source.get("audio_sha256"):
        errors.append("sidecar audio_sha256 does not match ledger")
    duration = float(source.get("duration_s", 0.0))
    previous_end = 0.0
    keys: set[str] = set()
    for index, cue in enumerate(sidecar.get("cues", [])):
        label = f"cue {index}"
        key = cue.get("event_key")
        if not isinstance(key, str) or not key or key in keys:
            errors.append(f"{label} has a missing or duplicate stable event_key")
        keys.add(str(key))
        timing = cue.get("timing", {})
        start = float(timing.get("start_s", -1.0))
        end = float(timing.get("end_s", -1.0))
        if not (0 <= start < end <= duration):
            errors.append(f"{label} span {start:g}-{end:g}s is outside source duration")
        if start < previous_end:
            errors.append(f"{label} overlaps the preceding cue")
        previous_end = max(previous_end, end)
        if timing.get("time_stretch") is not False:
            errors.append(f"{label} must set timing.time_stretch=false")
        if not cue.get("line") or not cue.get("voice_asset_key"):
            errors.append(f"{label} needs line and voice_asset_key")
        audio = cue.get("audio", {})
        status = audio.get("status")
        audio_hash = audio.get("sha256")
        if status == "ready":
            try:
                _sha(audio_hash, f"{label} audio.sha256")
            except ValueError as exc:
                errors.append(str(exc))
        elif status == "pending":
            if require_audio:
                errors.append(f"{label} audio binding is pending")
        else:
            errors.append(f"{label} audio.status must be ready or pending")
        if timing.get("mux") is not False:
            errors.append(f"{label} must set timing.mux=false until audio review is complete")
    if sidecar.get("delivery_acceptance") != "pending_human_and_device_review":
        errors.append("delivery_acceptance must remain pending_human_and_device_review")
    mix = sidecar.get("mix_plan", {})
    if mix.get("time_stretch") is not False or mix.get("mux") is not False:
        errors.append("mix_plan must forbid time-stretch and mux while cues are pending")
    return errors


def build_plan(ledger_path: Path, cue_path: Path, output_path: Path, require_audio: bool = False) -> dict[str, Any]:
    ledger = load_json(ledger_path)
    sidecar = load_json(cue_path)
    errors = validate_cues(ledger, sidecar, require_audio=require_audio)
    if errors:
        raise ValueError("invalid cue sidecar:\n- " + "\n- ".join(errors))
    source = _source(ledger, str(sidecar["source_id"]))
    plan = {
        "schema": SCHEMA,
        "artifact": "review_only_voice_timeline_and_mix_plan",
        "source_id": source["source_id"],
        "source_sha256": source["source_sha256"],
        "video_sha256": source["video_sha256"],
        "audio_sha256": source["audio_sha256"],
        "source_path": source["source_path"],
        "duration_s": source["duration_s"],
        "cues": sidecar["cues"],
        "mix_plan": sidecar["mix_plan"],
        "delivery_acceptance": "pending_human_and_device_review",
        "runtime_path": None,
        "muxed_video": None,
    }
    save_json(output_path, plan)
    return plan


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    intake = sub.add_parser("intake", help="validate and register a silent editorial source")
    intake.add_argument("--source", type=Path, default=Path(DEFAULT_SOURCE_PATH))
    intake.add_argument("--ledger", type=Path, required=True)
    intake.add_argument("--source-id", required=True)
    intake.add_argument("--clip-id", action="append", required=True)
    intake.add_argument("--visual-acceptance", default="unresolved")
    intake.add_argument("--ffprobe", default="ffprobe")
    plan = sub.add_parser("plan", help="validate cues and write a review-only mix plan")
    plan.add_argument("--ledger", type=Path, required=True)
    plan.add_argument("--cues", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--require-audio", action="store_true")
    check = sub.add_parser("validate", help="validate a ledger and cue sidecar")
    check.add_argument("--ledger", type=Path, required=True)
    check.add_argument("--cues", type=Path, required=True)
    check.add_argument("--require-audio", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "intake":
            source = intake_source(
                args.source,
                args.ledger,
                args.source_id,
                args.clip_id,
                args.visual_acceptance,
                args.ffprobe,
            )
            print(json.dumps(source, sort_keys=True))
        elif args.command == "plan":
            plan = build_plan(args.ledger, args.cues, args.output, args.require_audio)
            print(json.dumps({"status": "PASS", "output": str(args.output), "cue_count": len(plan["cues"])}, sort_keys=True))
        else:
            errors = validate_cues(load_json(args.ledger), load_json(args.cues), args.require_audio)
            if errors:
                print(json.dumps({"status": "FAIL", "errors": errors}, sort_keys=True))
                return 1
            print(json.dumps({"status": "PASS", "cue_count": len(load_json(args.cues).get("cues", []))}, sort_keys=True))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
