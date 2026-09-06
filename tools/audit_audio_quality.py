#!/usr/bin/env python3
"""Deterministic technical/semantic inventory for every production audio file."""

from __future__ import annotations

import argparse
import ast
import csv
import gzip
import hashlib
import io
import json
import math
import re
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path


AUDIO_SUFFIXES = {".ogg", ".wav", ".mp3"}
VOICE_ROOT_REL = "assets/audio/voices/"
FILLER_ROOT_REL = "assets/audio/voices/filler_v1/"
FILLER_MANIFEST_NAME = "FILLER_MANIFEST.json"
TEACHER_ROOT_REL = "assets/audio/teacher/"
TEACHER_MANIFEST_REL = "assets_src/teacher_learning_2026-09-05/audio_manifest.json"
TEACHER_SOURCE_SNAPSHOT_REL = (
    "assets_src/teacher_learning_2026-09-05/make_voices_generation_source.py.gz")
TEACHER_KEYS = {
    "roshan_teacher_start", "teacher_pattern", "teacher_count", "teacher_add",
    "teacher_match", "teacher_choose", "teacher_help",
    *(f"teacher_number_{number}" for number in range(1, 11)),
}
TEACHER_SOURCE_PROVENANCE = {
    # Pinned generation-time evidence from the reviewed manifest. These hashes
    # identify the weights used; the model files are intentionally not runtime
    # repository dependencies and are not remeasured on the audit host.
    "model_sha256": "8fbea51ea711f2af382e88c833d9e288c6dc82ce5e98421ea61c058ce21a34cb",
    "voices_sha256": "b58979d4eb5b1fdbe783c93f9f43c21217cb8f07af9d3860547371a5b2c8b646",
    "model_reference": "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX",
    "model_license": "Apache-2.0 (upstream Kokoro-82M ONNX distribution)",
    "voice_identity": (
        "Synthetic Kokoro af_heart; no family recording, protected voice, "
        "or identity cloning used."),
}
PROTECTED = {
    "assets/audio/voices/chuck.ogg",
    "assets/audio/voices/chuck_bark.ogg",
    "assets/audio/voices/chuck_whimper.ogg",
    "assets/audio/voices/daddy1.ogg",
    "assets/audio/voices/daddy2.ogg",
    "assets/audio/voices/daddy3.ogg",
}
ALLOWED_DADDY_FILLERS = {
    "daddy_dance_talk", "daddy_dance_win", "daddy_assist_ready",
    "daddy_hide_seek_start", "daddy_hide_seek_found", "daddy_hide_seek_visit",
}
NEW_EXACT_VOICES = {
    "assets/audio/voices/roshan_op_racer_tune_up.ogg",
    "assets/audio/voices/roshan_op_racer_to_the_line.ogg",
}
LEGACY_LOW_MUSIC = {
    "assets/audio/music/dolls.ogg",
    "assets/audio/music/fetch.ogg",
    "assets/audio/music/melody.ogg",
    "assets/audio/music/race.ogg",
    "assets/audio/music/seek.ogg",
}
LEGACY_MUSIC = {
    "assets/audio/music/banjo.ogg",
    "assets/audio/music/castle_open.ogg",
    "assets/audio/music/finale.ogg",
    "assets/audio/music/hall.ogg",
    "assets/audio/music/home.ogg",
    "assets/audio/music/level2.ogg",
    "assets/audio/music/shop.ogg",
    "assets/audio/music/treasure.ogg",
    "assets/audio/music/world.ogg",
    "assets/audio/music/world_night.ogg",
} | LEGACY_LOW_MUSIC
TEXT_SUFFIXES = {".gd", ".tscn", ".tres", ".godot", ".json", ".md"}


def is_faron(rel: str) -> bool:
    """Return whether *rel* is a legacy Faron recording.

    Faron is protected by speaker identity, not by a hand-maintained list: new
    Faron cues must therefore be protected automatically.  The provisional
    filler directory is deliberately excluded from this test.
    """
    return (rel.startswith(VOICE_ROOT_REL) and not rel.startswith(FILLER_ROOT_REL)
            and Path(rel).name.lower().startswith("faron")
            and Path(rel).suffix.lower() in AUDIO_SUFFIXES)


def protected_kind(rel: str) -> str | None:
    if is_faron(rel):
        return "protected_faron"
    if rel in PROTECTED:
        return "protected_family"
    return None


def _git_head_paths(root: Path) -> set[str]:
    """Read tracked voice paths from HEAD when this is a git worktree.

    The fallback to an empty set is intentional for unit-test fixtures and
    source archives.  A production checkout has the git baseline and gets the
    stronger unchanged-byte check in :func:`protected_audit`.
    """
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "--", VOICE_ROOT_REL],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return set()
    return {
        line.strip() for line in result.stdout.splitlines()
        if line.strip().lower().endswith(tuple(AUDIO_SUFFIXES))
    }


def protected_audit(root: Path) -> dict[str, object]:
    """Audit Faron and family recordings independently of synthetic filler.

    Faron paths come from both the checkout and HEAD so a deleted protected
    recording is caught.  Family recordings are the explicit sacred set.  A
    git checkout compares bytes to HEAD; non-git fixtures still report the
    actual inventory without inventing a baseline.
    """
    audio_root = root / "assets" / "audio" / "voices"
    actual: dict[str, Path] = {}
    if audio_root.exists():
        for path in audio_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in AUDIO_SUFFIXES:
                rel = path.relative_to(root).as_posix()
                kind = protected_kind(rel)
                if kind:
                    actual[rel] = path
    head_paths = _git_head_paths(root)
    expected = set(PROTECTED) | {
        rel for rel in head_paths if is_faron(rel)
    }
    issues: list[str] = []
    entries: list[dict[str, object]] = []
    for rel in sorted(expected | set(actual)):
        path = actual.get(rel)
        kind = protected_kind(rel) or ("protected_faron" if is_faron(rel) else "protected_family")
        if path is None:
            issues.append(f"missing protected recording: {rel}")
            entries.append({"path": rel, "kind": kind, "state": "MISSING"})
            continue
        actual_hash = sha256(path)
        head_hash = ""
        if rel in head_paths or rel in PROTECTED:
            result = subprocess.run(
                ["git", "show", f"HEAD:{rel}"],
                cwd=root, capture_output=True, check=False,
            )
            if result.returncode == 0:
                head_hash = hashlib.sha256(result.stdout).hexdigest()
        state = "UNCHANGED" if head_hash and actual_hash == head_hash else "UNVERIFIED"
        if head_hash and actual_hash != head_hash:
            state = "MODIFIED"
            issues.append(f"protected recording changed: {rel}")
        entries.append({
            "path": rel, "kind": kind, "state": state,
            "sha256": actual_hash, "head_sha256": head_hash,
        })
    return {
        "blocking": bool(issues),
        "issues": issues,
        "count": len(entries),
        "faron_count": sum(item["kind"] == "protected_faron" for item in entries),
        "family_count": sum(item["kind"] == "protected_family" for item in entries),
        "entries": entries,
    }


def _metric_mismatch(issues: list[str], label: str, actual: object,
                     expected: object, tolerance: float = 0.0) -> None:
    if actual is None or expected is None:
        issues.append(f"{label} missing")
        return
    try:
        actual_number = float(actual)
        expected_number = float(expected)
        if not math.isfinite(actual_number) or not math.isfinite(expected_number):
            issues.append(f"{label} is non-finite")
        elif abs(actual_number - expected_number) > tolerance:
            issues.append(f"{label} mismatch: actual={actual!r} manifest={expected!r}")
    except (TypeError, ValueError):
        if actual != expected:
            issues.append(f"{label} mismatch: actual={actual!r} manifest={expected!r}")


def decoded_signal(path: Path) -> dict[str, float | int | str]:
    """Decode the delivery signal and recompute safety metrics from samples."""
    result = subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
        "-f", "f32le", "-ac", "1", "-ar", "48000", "-",
    ], capture_output=True, check=False)
    if result.returncode != 0:
        return {"decode_ok": False, "error": result.stderr.decode(errors="replace").strip()}
    raw = result.stdout
    if len(raw) % 4:
        return {"decode_ok": False, "error": "decoded f32 stream has a partial sample"}
    samples = [value[0] for value in struct.iter_unpack("<f", raw)]
    if not samples or any(not math.isfinite(value) for value in samples):
        return {"decode_ok": False, "error": "decoded signal is empty or non-finite"}
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    return {
        "decode_ok": True,
        "duration_s": round(len(samples) / 48000.0, 6),
        "decoded_peak_linear": round(peak, 7),
        "decoded_clipped_samples": sum(abs(value) >= 0.999 for value in samples),
        "decoded_rms_dbfs": round(20.0 * math.log10(max(rms, 1.0e-12)), 2),
        "dc_offset": round(sum(samples) / len(samples), 8),
    }


def ogg_serials(path: Path) -> tuple[set[int], str | None]:
    """Read Ogg page serials so deterministic page evidence is testable."""
    payload = path.read_bytes()
    serials: set[int] = set()
    cursor = 0
    while cursor < len(payload):
        if payload[cursor:cursor + 4] != b"OggS" or cursor + 27 > len(payload):
            return set(), f"invalid Ogg page at byte {cursor}"
        segment_count = payload[cursor + 26]
        table_end = cursor + 27 + segment_count
        if table_end > len(payload):
            return set(), f"truncated Ogg lacing table at byte {cursor}"
        page_end = table_end + sum(payload[cursor + 27:table_end])
        if page_end > len(payload):
            return set(), f"truncated Ogg page at byte {cursor}"
        serials.add(int.from_bytes(payload[cursor + 14:cursor + 18], "little"))
        cursor = page_end
    return serials, None


def _safe_relative(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        return None
    candidate = Path(value)
    if "\\" in value or any(part == ".." for part in candidate.parts):
        return None
    return root / candidate


def validate_hash_map(root: Path, issues: list[str], label: str,
                      values: object) -> dict[str, str]:
    """Validate captured script/artifact hashes and return the valid subset."""
    if values is None:
        return {}
    if not isinstance(values, dict):
        issues.append(f"{label} must be an object")
        return {}
    valid: dict[str, str] = {}
    for relative, expected in values.items():
        path = _safe_relative(root, relative)
        if path is None or not isinstance(expected, str) \
                or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            issues.append(f"{label} contains invalid hash record: {relative!r}")
            continue
        if not path.is_file():
            issues.append(f"{label} path missing: {relative}")
            continue
        actual = sha256(path)
        if actual.lower() != expected.lower():
            issues.append(f"{label} mismatch: {relative}")
            continue
        valid[str(relative).replace("\\", "/")] = actual
    return valid


def normalized_text_sha256(path: Path) -> str:
    """Hash UTF-8 source with platform-independent LF line endings."""
    text = path.read_text(encoding="utf-8")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate_text_hash_map(root: Path, issues: list[str], label: str,
                           values: object) -> dict[str, str]:
    """Validate source hashes without depending on Git checkout EOL policy."""
    if values is None:
        return {}
    if not isinstance(values, dict):
        issues.append(f"{label} must be an object")
        return {}
    valid: dict[str, str] = {}
    for relative, expected in values.items():
        path = _safe_relative(root, relative)
        if path is None or not isinstance(expected, str) \
                or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            issues.append(f"{label} contains invalid hash record: {relative!r}")
            continue
        if not path.is_file():
            issues.append(f"{label} path missing: {relative}")
            continue
        actual = normalized_text_sha256(path)
        if actual.lower() != expected.lower():
            issues.append(f"{label} mismatch: {relative}")
            continue
        valid[str(relative).replace("\\", "/")] = actual
    return valid


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def authoritative_filler_lines(root: Path,
                               excluded_keys: set[str] | None = None) -> dict[str, tuple[str, str]]:
    """Read the legacy generator and frozen contextual catalogs as authority."""
    source = root / "tools" / "make_voices.py"
    if not source.exists():
        return {"everyone": ("everyone", "Hooray!")}
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    lines: dict[str, tuple[str, str]] | None = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "LINES"
                for target in node.targets):
            value = ast.literal_eval(node.value)
            lines = {str(key): (str(item[0]), str(item[1])) for key, item in value.items()}
            break
    if lines is None:
        raise RuntimeError("tools/make_voices.py has no literal LINES catalog")
    excluded = (excluded_keys or set()) & TEACHER_KEYS
    expected = {
        key: value for key, value in lines.items()
        if value[0] != "faron" and key not in excluded
    }
    contextual_path = root / "audit" / "DAY_ONE_CONTEXTUAL_VOICE_COVERAGE_2026-09-01.json"
    if contextual_path.is_file():
        contextual = json.loads(contextual_path.read_text(encoding="utf-8"))
        for row in contextual.get("rows", []):
            if not isinstance(row, dict):
                continue
            audio_path = Path(str(row.get("audio_path", "")))
            key = audio_path.stem
            caption = str(row.get("caption", ""))
            if not key or not caption:
                continue
            prior = expected.get(key)
            value = ("roshan", caption)
            if prior is not None and prior != value:
                raise RuntimeError(
                    f"contextual filler authority conflicts with tools/make_voices.py: {key}")
            expected[key] = value
    expected["everyone"] = ("everyone", "Hooray!")
    return expected


def validate_teacher_manifest(root: Path) -> dict[str, object]:
    """Validate the separately delivered Teacher speech cohort."""
    manifest_path = root / TEACHER_MANIFEST_REL
    teacher_root = root / TEACHER_ROOT_REL
    actual_names = ({path.name for path in teacher_root.glob("*.ogg")}
                    if teacher_root.is_dir() else set())
    if not manifest_path.is_file():
        issues = (["Teacher audio manifest is missing"] if actual_names else [])
        return {"present": False, "blocking": bool(issues), "issues": issues,
                "declared_keys": set(), "expected_names": set()}
    issues: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"present": True, "blocking": True,
                "issues": [f"Teacher audio manifest is invalid: {exc}"],
                "declared_keys": set(), "expected_names": set()}
    entries = manifest.get("entries")
    if manifest.get("schema_version") != 1:
        issues.append("Teacher audio manifest schema_version must be 1")
    if not isinstance(entries, list):
        entries = []
        issues.append("Teacher audio manifest entries must be an array")
    authority = authoritative_filler_lines(root)
    generator = manifest.get("generator")
    if not isinstance(generator, dict):
        generator = {}
        issues.append("Teacher audio manifest generator must be an object")
    if generator.get("script") != "tools/make_voices.py":
        issues.append("Teacher generator script path is invalid")
    source_hash = generator.get("script_sha256")
    snapshot_path = root / TEACHER_SOURCE_SNAPSHOT_REL
    try:
        snapshot = gzip.decompress(snapshot_path.read_bytes())
    except (OSError, EOFError, gzip.BadGzipFile) as exc:
        snapshot = b""
        issues.append(f"Teacher generator source snapshot is unavailable: {exc}")
    if not isinstance(source_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", source_hash):
        issues.append("Teacher generator script_sha256 is invalid")
    elif snapshot and hashlib.sha256(snapshot).hexdigest() != source_hash.lower():
        issues.append("Teacher generator source snapshot hash mismatch")
    current_generator = root / "tools/make_voices.py"
    if snapshot and current_generator.is_file():
        normalized_snapshot = snapshot.replace(b"\r\n", b"\n")
        normalized_current = current_generator.read_bytes().replace(b"\r\n", b"\n")
        if normalized_snapshot != normalized_current:
            issues.append("Teacher generator snapshot disagrees with current normalized source")
    speaker_config = generator.get("speaker_config")
    expected_speaker = {
        "character": "roshan", "voice": "af_heart",
        "pitch_factor": 1.24, "speed": 1.02,
    }
    if speaker_config != expected_speaker:
        issues.append("Teacher speaker_config disagrees with generation authority")
    source_provenance = manifest.get("source_provenance")
    if not isinstance(source_provenance, dict):
        issues.append("Teacher source_provenance must be an object")
    else:
        for field, expected in TEACHER_SOURCE_PROVENANCE.items():
            if source_provenance.get(field) != expected:
                issues.append(
                    f"Teacher source_provenance {field} disagrees with pinned generation evidence")
    delivery = manifest.get("delivery")
    if not isinstance(delivery, dict):
        delivery = {}
        issues.append("Teacher delivery must be an object")
    for field, expected in (("directory", "assets/audio/teacher"),
                            ("sample_rate_hz", 48000), ("channels", 1),
                            ("codec", "vorbis"), ("target_lufs", -16.0),
                            ("true_peak_limit_dbtp", -1.5), ("files_count", 17)):
        if delivery.get(field) != expected:
            issues.append(f"Teacher delivery {field} disagrees with policy")
    declared_keys: set[str] = set()
    expected_names: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(f"Teacher entry {index} must be an object")
            continue
        key = entry.get("key")
        if not isinstance(key, str) or not key or Path(key).name != key or Path(key).suffix:
            issues.append(f"Teacher entry {index} has unsafe key: {key!r}")
            continue
        if key in declared_keys:
            issues.append(f"duplicate Teacher entry: {key}")
        declared_keys.add(key)
        if key not in TEACHER_KEYS:
            issues.append(f"unrecognized Teacher cohort key: {key}")
        name = f"{key}.ogg"
        expected_names.add(name)
        expected_path = f"{TEACHER_ROOT_REL}{name}"
        if entry.get("output_path") != expected_path:
            issues.append(f"{name} has invalid Teacher output_path")
        expected_line = authority.get(key)
        actual_line = (str(entry.get("speaker", "")), str(entry.get("text", "")))
        if expected_line is None:
            issues.append(f"{name} is absent from tools/make_voices.py authority")
        elif actual_line != expected_line:
            issues.append(f"{name} speaker/text disagrees with tools/make_voices.py")
        expected_text_hash = hashlib.sha256(str(entry.get("text", "")).encode()).hexdigest()
        if entry.get("source_text_sha256") != expected_text_hash:
            issues.append(f"{name} source_text_sha256 mismatch")
        for field, expected in (("kokoro_voice", "af_heart"),
                                ("pitch_factor", 1.24), ("speed", 1.02),
                                ("source_line_table", "tools/make_voices.py:LINES")):
            if entry.get(field) != expected:
                issues.append(f"{name} {field} disagrees with generator")
        path = root / expected_path
        if not path.is_file():
            issues.append(f"Teacher manifest entry missing OGG: {name}")
            continue
        expected_hash = entry.get("output_sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
            issues.append(f"{name} has missing/invalid output_sha256")
        elif sha256(path).lower() != expected_hash.lower():
            issues.append(f"{name} hash mismatch")
        if entry.get("output_bytes") != path.stat().st_size:
            issues.append(f"{name} output_bytes mismatch")
        meta = probe(path)
        integrated, lra, peak = loudness(path) if meta.get("decode_ok") else (None, None, None)
        signal = decoded_signal(path) if meta.get("decode_ok") else {"decode_ok": False}
        if not meta.get("decode_ok") or not signal.get("decode_ok"):
            issues.append(f"{name} media decode failed")
            continue
        for field, expected in (("codec", meta.get("codec")),
                                ("sample_rate_hz", meta.get("sample_rate_hz")),
                                ("channels", meta.get("channels"))):
            if entry.get(field) != expected:
                issues.append(f"{name} {field} mismatch")
        _metric_mismatch(issues, f"{name} bitrate_kbps",
                         meta.get("bitrate_kbps"), entry.get("bitrate_kbps"), 1.0)
        _metric_mismatch(issues, f"{name} duration_s",
                         signal.get("duration_s"), entry.get("duration_s"), 0.02)
        _metric_mismatch(issues, f"{name} true_peak_dbtp",
                         peak, entry.get("true_peak_dbtp"), 0.1)
        _metric_mismatch(issues, f"{name} decoded_peak_linear",
                         signal.get("decoded_peak_linear"), entry.get("decoded_peak_linear"), 0.0001)
        _metric_mismatch(issues, f"{name} decoded_rms_dbfs",
                         signal.get("decoded_rms_dbfs"), entry.get("decoded_rms_dbfs"), 0.1)
        if entry.get("decoded_clipped_samples") != signal.get("decoded_clipped_samples"):
            issues.append(f"{name} decoded_clipped_samples mismatch")
        measured_clips = int(signal.get("decoded_clipped_samples", -1))
        if measured_clips != 0:
            issues.append(f"{name} has decoded clipped samples: {measured_clips}")
        peak_limit = float(delivery.get("true_peak_limit_dbtp", -1.5))
        if peak is None or peak > peak_limit:
            issues.append(
                f"{name} true peak exceeds Teacher delivery limit: {peak!r} > {peak_limit}")
        if float(signal.get("duration_s", 0.0)) < 0.4:
            if entry.get("quality_status") != "PASS_WITH_NOTE" or entry.get("integrated_lufs") != -70.0:
                issues.append(f"{name} short-program quality claim is invalid")
        else:
            _metric_mismatch(issues, f"{name} integrated_lufs",
                             integrated, entry.get("integrated_lufs"), 0.1)
            _metric_mismatch(issues, f"{name} loudness_range_lu",
                             lra, entry.get("loudness_range_lu"), 0.1)
            if entry.get("quality_status") != "PASS":
                issues.append(f"{name} quality_status must be PASS")
    for missing in sorted(expected_names - actual_names):
        # The entry-level message names the same defect; avoid duplicate output.
        if f"Teacher manifest entry missing OGG: {missing}" not in issues:
            issues.append(f"Teacher manifest entry missing OGG: {missing}")
    nested_names = {
        path.relative_to(teacher_root).as_posix()
        for path in teacher_root.rglob("*.ogg")
    } if teacher_root.is_dir() else set()
    for unexpected in sorted(nested_names - expected_names):
        issues.append(f"unlisted Teacher OGG: {unexpected}")
    for missing_key in sorted(TEACHER_KEYS - declared_keys):
        issues.append(f"required Teacher cohort key missing: {missing_key}")
    declared_count = manifest.get("delivery", {}).get("files_count") \
        if isinstance(manifest.get("delivery"), dict) else None
    if declared_count != len(entries):
        issues.append("Teacher manifest files_count disagrees with entries")
    return {"present": True, "blocking": bool(issues), "issues": issues,
            "declared_keys": declared_keys, "expected_names": expected_names,
            "entry_count": len(entries)}


def _expected_ogg_serial(key: str) -> int:
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF


def _candidate_evidence(root: Path, attempt: int,
                        manifest_value: object = None) -> dict[str, dict[str, object]]:
    """Load optional local candidate rows for stronger source verification."""
    path = _safe_relative(root, manifest_value) if manifest_value is not None else None
    if path is None:
        path = root / "tmp" / "filler_candidates" / "parler" / f"attempt_{attempt}" / "trial_manifest.json"
    if not path.is_file():
        return {}
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(rows, list):
        return {}
    return {
        str(row["key"]): row for row in rows
        if isinstance(row, dict) and isinstance(row.get("key"), str)
        and int(row.get("attempt", -1)) == attempt
    }


def group_component_issues(component: dict[str, object]) -> list[str]:
    """Return independent blockers for one authored Hooray mix layer."""
    issues: list[str] = []
    character = str(component.get("character", ""))
    selection = component.get("selection_evidence", {}).get("selection", {})
    f0_ranges = {
        "roshan": (225.0, 360.0),
        "huluu": (145.0, 275.0),
        "evie": (190.0, 340.0),
    }
    f0 = float(selection.get("f0_median_hz") or 0.0)
    duration = float(selection.get("duration_s") or 0.0)
    active = float(selection.get("active_duration_s") or 0.0)
    voiced_fraction = float(selection.get("voiced_frame_fraction") or 0.0)
    if character not in f0_ranges \
            or not (f0_ranges[character][0] <= f0 <= f0_ranges[character][1]):
        issues.append(f"everyone.ogg {character} component F0 out of range")
    if not (0.35 <= active <= 2.5 and 0.35 <= duration <= 4.0 \
            and active / max(duration, 0.001) >= 0.25 \
            and voiced_fraction >= 0.20):
        issues.append(f"everyone.ogg {character} component active-speech bounds failed")
    if component.get("text") != "Hooray!" \
            or component.get("generation_text") != "Hooray!" \
            or selection.get("semantic_gate_expected_words") != ["hooray"] \
            or selection.get("semantic_gate_transcript_words") != ["hooray"]:
        issues.append(f"everyone.ogg {character} component semantic identity mismatch")
    return issues


def validate_generation_evidence(root: Path, manifest: dict[str, object],
                                 entries: list[dict[str, object]],
                                 generation_runs: dict[str, object],
                                 issues: list[str]) -> None:
    """Cross-check captured hashes, selected source metadata, and Ogg proof."""
    pipeline_hashes = manifest.get("pipeline_script_sha256")
    if pipeline_hashes is not None:
        if manifest.get("pipeline_hash_mode") == "utf8_lf":
            validate_text_hash_map(
                root, issues, "pipeline_script_sha256", pipeline_hashes)
        else:
            validate_hash_map(root, issues, "pipeline_script_sha256", pipeline_hashes)
    selection_provenance = manifest.get("selection_provenance")
    if isinstance(selection_provenance, dict):
        selector_hash = selection_provenance.get("selector_sha256")
        if selector_hash is not None:
            validator = validate_text_hash_map \
                if selection_provenance.get("selector_hash_mode") == "utf8_lf" \
                else validate_hash_map
            validator(root, issues, "selection_provenance.selector_sha256",
                      {"tools/select_filler_voices.py": selector_hash})
        report_hash = selection_provenance.get("report_sha256")
        if report_hash is not None and not isinstance(report_hash, str):
            issues.append("selection_provenance.report_sha256 is invalid")
        elif isinstance(report_hash, str) and not re.fullmatch(r"[0-9a-fA-F]{64}", report_hash):
            issues.append("selection_provenance.report_sha256 is invalid")
    candidate_cache: dict[int, dict[str, dict[str, object]]] = {}
    for run_name, record in generation_runs.items():
        match = re.fullmatch(r"attempt_(\d+)", str(run_name))
        if not match or not isinstance(record, dict):
            issues.append(f"invalid generation run record: {run_name!r}")
            continue
        attempt = int(match.group(1))
        if record.get("attempt") is not None and record.get("attempt") != attempt:
            issues.append(f"generation run attempt mismatch: {run_name}")
        candidate_rows = record.get("candidate_rows")
        candidate_rows_hash = record.get("candidate_rows_sha256")
        if isinstance(candidate_rows, list):
            if record.get("candidate_count") != len(candidate_rows):
                issues.append(f"{run_name} embedded candidate count mismatch")
            if not isinstance(candidate_rows_hash, str) \
                    or not re.fullmatch(r"[0-9a-fA-F]{64}", candidate_rows_hash):
                issues.append(f"{run_name}.candidate_rows_sha256 is invalid")
            elif canonical_json_sha256(candidate_rows).lower() != candidate_rows_hash.lower():
                issues.append(f"{run_name} embedded candidate rows hash mismatch")
            embedded_candidates: dict[str, dict[str, object]] = {}
            for row in candidate_rows:
                if not isinstance(row, dict) or row.get("attempt") != attempt \
                        or not isinstance(row.get("key"), str):
                    issues.append(f"{run_name} has invalid embedded candidate row")
                    continue
                embedded_candidates[str(row["key"])] = row
            candidate_cache[attempt] = embedded_candidates
        elif record.get("capture_state") == "CAPTURED_AT_GENERATION":
            issues.append(f"{run_name} lacks embedded candidate rows")
        generator_hash = record.get("generator_sha256")
        if generator_hash not in (None, "NOT_CAPTURED_AT_GENERATION"):
            if not isinstance(generator_hash, str) \
                    or not re.fullmatch(r"[0-9a-fA-F]{64}", generator_hash):
                issues.append(f"{run_name}.generator_sha256 is invalid")
            run_path_value = record.get("run_provenance_path")
            if isinstance(run_path_value, str):
                run_path = root / run_path_value
                captured_run_hash = record.get("run_provenance_sha256")
                if captured_run_hash is not None and (
                        not isinstance(captured_run_hash, str)
                        or not re.fullmatch(r"[0-9a-fA-F]{64}", captured_run_hash)):
                    issues.append(f"{run_name}.run_provenance_sha256 is invalid")
                if run_path.is_file():
                    if isinstance(captured_run_hash, str) \
                            and sha256(run_path).lower() != captured_run_hash.lower():
                        issues.append(f"{run_name} run provenance hash mismatch")
                    try:
                        run_payload = json.loads(run_path.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        issues.append(f"{run_name} run provenance is unreadable")
                    else:
                        if run_payload.get("generator_sha256") != generator_hash:
                            issues.append(f"{run_name} generator hash disagrees with run provenance")
        candidate_manifest_value = record.get("candidate_manifest_path")
        candidate_path = _safe_relative(root, candidate_manifest_value)
        if candidate_path is None:
            candidate_path = root / "tmp" / "filler_candidates" / "parler" / str(run_name) / "trial_manifest.json"
        captured_manifest_hash = record.get("candidate_manifest_sha256")
        if captured_manifest_hash is not None:
            if not isinstance(captured_manifest_hash, str) \
                    or not re.fullmatch(r"[0-9a-fA-F]{64}", captured_manifest_hash):
                issues.append(f"{run_name}.candidate_manifest_sha256 is invalid")
            elif candidate_path.is_file() and sha256(candidate_path).lower() != captured_manifest_hash.lower():
                issues.append(f"{run_name} candidate manifest hash mismatch")
        if candidate_path.is_file():
            external_candidates = _candidate_evidence(
                root, attempt, candidate_manifest_value)
            if attempt in candidate_cache and external_candidates != candidate_cache[attempt]:
                issues.append(f"{run_name} embedded candidate rows disagree with local manifest")
            candidate_cache[attempt] = external_candidates
    for entry in entries:
        key = str(entry.get("key", ""))
        name = f"{key}.ogg"
        if key == "everyone":
            components = entry.get("components")
            if not isinstance(components, list):
                continue
            component_rows = components
        else:
            component_rows = [entry]
        for component in component_rows:
            if not isinstance(component, dict):
                continue
            attempt = component.get("attempt", component.get("selected_attempt"))
            seed = component.get("seed")
            source_hash = component.get("raw_sha256", component.get("source_wav_sha256"))
            if not isinstance(attempt, int) or attempt < 1:
                continue
            run = generation_runs.get(f"attempt_{attempt}")
            if not isinstance(run, dict):
                continue
            if run.get("attempt") is not None and run.get("attempt") != attempt:
                issues.append(f"{name} attempt disagrees with generation run")
            candidates = candidate_cache.get(attempt, {})
            candidate = candidates.get(str(component.get("key", key)))
            if candidate:
                if seed is not None and candidate.get("seed") != seed:
                    issues.append(f"{name} selected seed disagrees with candidate evidence")
                if source_hash is not None and candidate.get("raw_sha256") != source_hash:
                    issues.append(f"{name} selected source hash disagrees with candidate evidence")
                candidate_segments = candidate.get("generation_segments")
                if isinstance(candidate_segments, list) and candidate_segments:
                    candidate_generation_text = " ".join(
                        str(segment) for segment in candidate_segments)
                else:
                    candidate_generation_text = candidate.get("generation_text")
                if component.get("generation_text") is not None \
                        and candidate_generation_text is not None \
                        and component.get("generation_text") != candidate_generation_text:
                    issues.append(f"{name} generation text disagrees with candidate evidence")
                if component.get("segment_seeds") is not None and candidate.get("segment_seeds") is not None \
                        and component.get("segment_seeds") != candidate.get("segment_seeds"):
                    issues.append(f"{name} segment seeds disagree with candidate evidence")
        if key != "everyone":
            selection = entry.get("selection_metrics")
            if isinstance(selection, dict):
                selected_attempt = entry.get("selected_attempt")
                if selection.get("attempt") is not None and selection.get("attempt") != selected_attempt:
                    issues.append(f"{name} selected attempt disagrees with selection metrics")
                if selection.get("seed") is not None and selection.get("seed") != entry.get("seed"):
                    issues.append(f"{name} selected seed disagrees with selection metrics")
                for field in ("source_sha256", "selected_raw_sha256"):
                    if selection.get(field) is not None and selection.get(field) != entry.get("source_wav_sha256"):
                        issues.append(f"{name} {field} disagrees with source_wav_sha256")
        command = entry.get("ffmpeg_command")
        if not isinstance(command, list) or "-serial_offset" not in command:
            issues.append(f"{name} lacks explicit deterministic Ogg serial evidence")
        else:
            serial_index = command.index("-serial_offset") + 1
            try:
                command_serial = int(command[serial_index])
            except (IndexError, TypeError, ValueError):
                command_serial = -1
            serial_key = str(entry.get("final_audio_alias_of") or key)
            if command_serial != _expected_ogg_serial(serial_key):
                issues.append(f"{name} deterministic Ogg serial evidence is invalid")


def validate_filler_manifest(root: Path,
                             expected_lines: dict[str, tuple[str, str]] | None = None
                             ) -> dict[str, object]:
    """Validate the optional provisional filler cohort and return its state.

    The absence of ``FILLER_MANIFEST.json`` is allowed while the cohort is
    being generated.  Once present, every OGG must have one manifest entry and
    every entry must have a matching hash and delivery measurement.
    """
    manifest_path = root / FILLER_ROOT_REL / FILLER_MANIFEST_NAME
    if not manifest_path.exists():
        return {
            "present": False, "blocking": False, "issues": [],
            "expected_names": set(), "entry_count": 0,
        }
    issues: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "present": True, "blocking": True,
            "issues": [f"cannot read filler manifest: {exc}"],
            "expected_names": set(), "entry_count": 0,
        }
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return {
            "present": True, "blocking": True,
            "issues": ["filler manifest entries must be a list"],
            "expected_names": set(), "entry_count": 0,
        }
    contextual_proof: dict[str, dict[str, object]] = {}
    if manifest.get("contextual_append_only") is True:
        provenance_value = manifest.get("contextual_cohort_provenance_path")
        provenance_path = _safe_relative(root, provenance_value)
        if provenance_path is None or not provenance_path.is_file():
            issues.append("contextual cohort provenance is missing")
        else:
            expected_provenance_hash = manifest.get("contextual_cohort_provenance_sha256")
            if not isinstance(expected_provenance_hash, str) \
                    or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_provenance_hash):
                issues.append("contextual cohort provenance hash is invalid")
            elif sha256(provenance_path).lower() != expected_provenance_hash.lower():
                issues.append("contextual cohort provenance hash mismatch")
            try:
                provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                issues.append("contextual cohort provenance is unreadable")
            else:
                if provenance.get("selection_report_sha256") != \
                        manifest.get("contextual_cohort_selection_report_sha256"):
                    issues.append("contextual selection report hash mismatch")
                proof_entries = provenance.get("entries", [])
                if not isinstance(proof_entries, list):
                    issues.append("contextual provenance entries must be a list")
                else:
                    contextual_proof = {
                        str(item.get("key")): item for item in proof_entries
                        if isinstance(item, dict) and isinstance(item.get("key"), str)
                    }
    expected_names: set[str] = set()
    entry_by_name: dict[str, dict[str, object]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("key"), str):
            issues.append(f"entry {index} has no string key")
            continue
        key = str(entry["key"])
        name = f"{key}.ogg"
        if (not key or Path(key).name != key or Path(key).suffix
                or "\\" in key or "/" in key):
            issues.append(f"entry {index} has unsafe key: {key!r}")
            continue
        if name in expected_names:
            issues.append(f"duplicate filler entry: {name}")
        expected_names.add(name)
        entry_by_name[name] = entry
    authority = expected_lines if expected_lines is not None else authoritative_filler_lines(root)
    authority_names = {f"{key}.ogg" for key in authority}
    for missing in sorted(authority_names - expected_names):
        issues.append(f"authoritative filler key missing: {missing}")
    for extra in sorted(expected_names - authority_names):
        issues.append(f"non-authoritative filler key present: {extra}")
    generation_runs = manifest.get("generation_run_provenance")
    if not isinstance(generation_runs, dict):
        issues.append("generation_run_provenance must be an object")
        generation_runs = {}
    validate_generation_evidence(root, manifest, entries, generation_runs, issues)
    filler_root = root / FILLER_ROOT_REL
    actual_names = {path.name for path in filler_root.glob("*.ogg")}
    for missing in sorted(expected_names - actual_names):
        issues.append(f"manifest entry missing OGG: {missing}")
    for unexpected in sorted(actual_names - expected_names):
        issues.append(f"unlisted filler OGG: {unexpected}")
    for name in sorted(expected_names & actual_names):
        path = filler_root / name
        entry = entry_by_name[name]
        key = str(entry["key"])
        if key in authority:
            expected_character, expected_text = authority[key]
            if entry.get("character") != expected_character:
                issues.append(
                    f"{name} character mismatch: {entry.get('character')!r} != {expected_character!r}")
            if entry.get("text") != expected_text:
                issues.append(f"{name} authored text mismatch")
        is_contextual = isinstance(entry.get("contextual_cue_id"), str)
        expected_status = "PROVISIONAL_SYNTHETIC_CONTEXTUAL" if is_contextual \
            else "PROVISIONAL_SYNTHETIC_FILLER"
        if entry.get("status") != expected_status:
            issues.append(f"{name} has invalid provisional status")
        if is_contextual:
            proof = contextual_proof.get(key)
            if proof is None:
                issues.append(f"{name} missing contextual cohort provenance")
            elif canonical_json_sha256(proof) != canonical_json_sha256(entry):
                issues.append(f"{name} disagrees with contextual cohort provenance")
        character = entry.get("character")
        if character in {"faron", "chuck"} \
                or (character == "daddy" and key not in ALLOWED_DADDY_FILLERS):
            issues.append(f"{name} contains protected speaker identity")
        if key == "everyone":
            components = entry.get("components")
            if not isinstance(components, list) or len(components) != 3:
                issues.append("everyone.ogg must have three generated components")
            else:
                component_keys = {component.get("key") for component in components}
                if component_keys != {
                        "everyone_roshan", "everyone_huluu", "everyone_evie"}:
                    issues.append("everyone.ogg component identity set mismatch")
                for component in components:
                    attempt = component.get("attempt")
                    if f"attempt_{attempt}" not in generation_runs:
                        issues.append(f"everyone.ogg component attempt missing: {attempt!r}")
                    for field in ("generation_text", "generation_segments", "segment_seeds",
                                  "raw_sha256", "speaker", "description"):
                        if not component.get(field):
                            issues.append(f"everyone.ogg component missing {field}")
                    issues.extend(group_component_issues(component))
        else:
            attempt = entry.get("selected_attempt")
            if not isinstance(attempt, int) or attempt < 1:
                issues.append(f"{name} has invalid selected_attempt")
            elif not is_contextual and f"attempt_{attempt}" not in generation_runs:
                issues.append(f"{name} selected attempt has no generation provenance")
            for field in ("generation_text", "generation_segments", "segment_seeds",
                          "source_wav_sha256", "speaker_preset", "description"):
                if not entry.get(field):
                    issues.append(f"{name} missing {field}")
            selection = entry.get("selection_metrics")
            if not isinstance(selection, dict):
                issues.append(f"{name} missing selection_metrics")
            else:
                if selection.get("semantic_gate_schema") != 3:
                    issues.append(f"{name} did not pass semantic gate schema 3")
                if selection.get("semantic_gate_expected_words") != \
                        selection.get("semantic_gate_transcript_words"):
                    issues.append(f"{name} semantic gate words do not match")
        expected_hash = entry.get("final_ogg_sha256")
        actual_hash = sha256(path)
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
            issues.append(f"{name} has missing/invalid final_ogg_sha256")
        elif actual_hash.lower() != expected_hash.lower():
            issues.append(f"{name} hash mismatch: actual={actual_hash} manifest={expected_hash}")
        meta = probe(path)
        measured_lufs, _lra, measured_peak = loudness(path) if meta.get("decode_ok") else (None, None, None)
        serials, serial_error = ogg_serials(path)
        if serial_error:
            issues.append(f"{name} deterministic Ogg parse failed: {serial_error}")
        elif len(serials) != 1:
            issues.append(f"{name} must use one deterministic Ogg serial: {sorted(serials)}")
        else:
            serial_key = str(entry.get("final_audio_alias_of") or key)
            if serials != {_expected_ogg_serial(serial_key)}:
                issues.append(f"{name} Ogg serial does not match deterministic key")
        delivery = entry.get("delivery_metrics")
        if not isinstance(delivery, dict):
            issues.append(f"{name} has no delivery_metrics")
            delivery = {}
        if not meta.get("decode_ok"):
            issues.append(f"{name} cannot be decoded: {meta.get('probe_error', 'unknown error')}")
            continue
        decoded = decoded_signal(path)
        if not decoded.get("decode_ok"):
            issues.append(f"{name} decoded signal failed: {decoded.get('error', 'unknown error')}")
            continue
        measured_duration = float(decoded["duration_s"])
        probe_duration = float(meta.get("duration_seconds", 0.0) or 0.0)
        if abs(measured_duration - probe_duration) > 0.02:
            issues.append(f"{name} decoded duration disagrees with ffprobe")
        try:
            duration = float(delivery.get("duration_s", 0.0) or 0.0)
        except (TypeError, ValueError):
            duration = float("nan")
        if not math.isfinite(duration) or not 0.25 <= duration <= 30.0:
            issues.append(f"{name} duration outside voice bounds: {duration}")
        if not 0.25 <= measured_duration <= 30.0:
            issues.append(f"{name} recomputed duration outside voice bounds: {measured_duration}")
        if abs(measured_duration - duration) > 0.02:
            issues.append(f"{name} duration disagrees with manifest delivery_metrics")
        clipped = int(decoded["decoded_clipped_samples"])
        if clipped != 0:
            issues.append(f"{name} has decoded clipped samples: {clipped}")
        try:
            manifest_clipped = int(delivery.get("decoded_clipped_samples", -1) or 0)
        except (TypeError, ValueError):
            manifest_clipped = -1
        if manifest_clipped != clipped:
            issues.append(f"{name} decoded clipping count disagrees with manifest")
        measured_dc = float(decoded["dc_offset"])
        if not math.isfinite(measured_dc) or abs(measured_dc) > 0.01:
            issues.append(f"{name} recomputed DC offset is unsafe: {measured_dc}")
        dc_offset = delivery.get("dc_offset")
        try:
            manifest_dc = float(dc_offset)
        except (TypeError, ValueError):
            manifest_dc = float("nan")
        if not math.isfinite(manifest_dc) or abs(manifest_dc) > 0.01:
            issues.append(f"{name} has invalid DC offset: {dc_offset!r}")
        elif abs(measured_dc - manifest_dc) > 0.0001:
            issues.append(f"{name} DC offset disagrees with manifest")
        _metric_mismatch(
            issues, f"{name} decoded_peak_linear", decoded.get("decoded_peak_linear"),
            delivery.get("decoded_peak_linear"), 0.0001,
        )
        if meta.get("codec") != "vorbis":
            issues.append(f"{name} codec is not vorbis: {meta.get('codec')!r}")
        if meta.get("sample_rate_hz") != 48000:
            issues.append(f"{name} sample rate is not 48000 Hz: {meta.get('sample_rate_hz')!r}")
        if meta.get("channels") != 1:
            issues.append(f"{name} is not mono: {meta.get('channels')!r}")
        if float(meta.get("bitrate_kbps", 0) or 0) < 64.0:
            issues.append(f"{name} bitrate below 64 kbps: {meta.get('bitrate_kbps')!r}")
        _metric_mismatch(issues, f"{name} codec", meta.get("codec"), delivery.get("codec"))
        _metric_mismatch(issues, f"{name} sample_rate_hz", meta.get("sample_rate_hz"), delivery.get("sample_rate_hz"))
        _metric_mismatch(issues, f"{name} channels", meta.get("channels"), delivery.get("channels"))
        if delivery.get("bit_rate_bps") is not None:
            # ffprobe may report format vs stream bitrate; permit 1 kbps of
            # rounding while still requiring the manifest to describe reality.
            _metric_mismatch(
                issues, f"{name} bit_rate_bps",
                float(meta.get("bitrate_kbps", 0)) * 1000.0,
                delivery.get("bit_rate_bps"), 1000.0,
            )
        if measured_lufs is None:
            issues.append(f"{name} integrated loudness unavailable")
        else:
            if not -17.0 <= measured_lufs <= -15.0:
                issues.append(f"{name} loudness outside -16 +/- 1 LUFS: {measured_lufs}")
            _metric_mismatch(issues, f"{name} integrated_lufs", measured_lufs, delivery.get("integrated_lufs"), 0.1)
        if measured_peak is None:
            issues.append(f"{name} true peak unavailable")
        else:
            if measured_peak > -1.5:
                issues.append(f"{name} true peak above -1.5 dBTP: {measured_peak}")
            _metric_mismatch(issues, f"{name} true_peak_dbtp", measured_peak, delivery.get("true_peak_dbtp"), 0.1)
    return {
        "present": True, "blocking": bool(issues), "issues": issues,
        "expected_names": expected_names, "entry_count": len(entries),
        "manifest_path": manifest_path.relative_to(root).as_posix(),
    }


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path: Path) -> dict[str, object]:
    result = run([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate",
        "-show_entries", "format=duration,bit_rate", "-of", "json",
        str(path),
    ])
    if result.returncode != 0:
        return {"decode_ok": False, "probe_error": result.stderr.strip()}
    payload = json.loads(result.stdout)
    stream = payload.get("streams", [{}])[0]
    fmt = payload.get("format", {})
    return {
        "decode_ok": True,
        "codec": stream.get("codec_name", ""),
        "sample_rate_hz": int(stream.get("sample_rate", 0) or 0),
        "channels": int(stream.get("channels", 0) or 0),
        "bitrate_kbps": round(float(fmt.get("bit_rate", 0) or 0) / 1000.0, 2),
        "duration_seconds": round(float(fmt.get("duration", 0) or 0), 6),
    }


def loudness(path: Path) -> tuple[float | None, float | None, float | None]:
    result = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-filter_complex", "ebur128=peak=true", "-f", "null", "-",
    ])
    text = result.stderr
    summaries = list(re.finditer(
        r"Summary:\s*\n\s*Integrated loudness:.*?I:\s*([-+\w.]+) LUFS"
        r".*?Loudness range:.*?LRA:\s*([-+\w.]+) LU"
        r".*?True peak:.*?Peak:\s*([-+\w.]+) dBFS",
        text, re.DOTALL,
    ))
    if not summaries:
        return None, None, None

    def number(value: str) -> float | None:
        try:
            parsed = float(value)
        except ValueError:
            return None
        return round(parsed, 2)

    match = summaries[-1]
    return number(match.group(1)), number(match.group(2)), number(match.group(3))


def category(rel: str) -> str:
    if rel.startswith("assets/audio/voices/") \
            or rel.startswith("assets/audio/teacher/") \
            or rel.startswith("assets/audio/chapter2_lawn/") \
            or rel == "assets/audio/voice_yay.mp3":
        return "voice"
    if rel.startswith("assets/audio/music/"):
        return "music"
    if rel.startswith("assets/audio/castle/"):
        return "castle_sfx"
    if rel.startswith("assets/audio/sfx/"):
        return "combat_sfx"
    if "ambience" in rel:
        return "ambience"
    if rel.endswith("ui_tap.ogg"):
        return "ui"
    return "sfx"


def grade(rel: str, meta: dict[str, object], peak: float | None) -> tuple[str, int, str, str]:
    if not meta.get("decode_ok") or float(meta.get("duration_seconds", 0) or 0) <= 0:
        return "F", 1, "P0", "REPLACE_CORRUPT"
    if peak is not None and peak > 0.0:
        return "F", 1, "P1", "REPLACE_CLIPPING"
    if rel in LEGACY_LOW_MUSIC:
        return "D", 2, "P2", "LISTEN_REPLACE_CANDIDATE"
    if rel.startswith("assets/audio/castle/"):
        return "C", 3, "P2", "LISTEN_REPLACE_CANDIDATE"
    if rel == "assets/audio/purr.wav":
        return "C", 3, "P2", "LISTEN_REPLACE_CANDIDATE"
    if rel in LEGACY_MUSIC:
        return "C", 3, "P2", "LISTEN_REPLACE_CANDIDATE"
    if protected_kind(rel):
        return "B", 4, "P2", "KEEP_PROTECTED"
    if rel.startswith(FILLER_ROOT_REL):
        return "A", "", "P1", "REVIEW_PROVISIONAL_FILLER"
    if category(rel) == "voice" and peak is not None and peak > -1.5:
        return "B", 3, "P2", "RENDER_TRUE_PEAK_SAFE"
    if rel in NEW_EXACT_VOICES:
        return "A", 4, "P1", "REVIEW_NEW_EXACT_VOICE"
    if Path(rel).suffix == ".wav":
        return "B", 4, "P3", "KEEP_REVIEW_DEVICE"
    return "A", 4, "P3", "KEEP_PENDING_HUMAN"


def source_text(root: Path) -> str:
    chunks: list[str] = []
    for top in ("scripts", "scenes", "project.godot"):
        path = root / top
        files = [path] if path.is_file() else path.rglob("*")
        for candidate in files:
            if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                try:
                    chunks.append(candidate.read_text(encoding="utf-8"))
                except UnicodeDecodeError:
                    continue
    return "\n".join(chunks)


def build_rows(root: Path, filler_validation: dict[str, object] | None = None) -> list[dict[str, object]]:
    text = source_text(root)
    filler_validation = filler_validation or validate_filler_manifest(root)
    filler_names = set(filler_validation.get("expected_names", set()))
    rows: list[dict[str, object]] = []
    audio_root = root / "assets" / "audio"
    for path in sorted(
            (p for p in audio_root.rglob("*") if p.suffix.lower() in AUDIO_SUFFIXES),
            key=lambda p: p.as_posix().lower()):
        rel = path.relative_to(root).as_posix()
        meta = probe(path)
        integrated, lra, peak = loudness(path) if meta.get("decode_ok") else (None, None, None)
        # EBU integrated loudness is not meaningful below the 400 ms gate.
        # Keep true peak, but do not present the filter's -70 LUFS sentinel as
        # a real loudness measurement for taps and other very short SFX.
        if float(meta.get("duration_seconds", 0) or 0) < 0.4:
            integrated = None
            lra = None
        technical, subjective, severity, decision = grade(rel, meta, peak)
        basename = path.name
        filler = rel.startswith(FILLER_ROOT_REL)
        kind = protected_kind(rel)
        cohort = ("filler_v1" if filler else kind or
                  ("legacy_voice" if category(rel) == "voice" else category(rel)))
        legacy_path = f"{VOICE_ROOT_REL}{basename}"
        shadowed_by = f"{FILLER_ROOT_REL}{basename}" if basename in filler_names and not filler else ""
        rows.append({
            "path": rel,
            "category": category(rel),
            "cohort": cohort,
            "protected": bool(kind),
            "filler_manifest_present": bool(filler_validation.get("present")),
            "filler_manifest_blocking": bool(filler_validation.get("blocking")) if filler else False,
            "shadowed_legacy_path": legacy_path if filler and (root / legacy_path).exists() else "",
            "shadowed_by_filler_path": shadowed_by,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "codec": meta.get("codec", ""),
            "sample_rate_hz": meta.get("sample_rate_hz", 0),
            "channels": meta.get("channels", 0),
            "bitrate_kbps": meta.get("bitrate_kbps", 0),
            "duration_seconds": meta.get("duration_seconds", 0),
            "integrated_lufs": integrated if integrated is not None else "",
            "loudness_range_lu": lra if lra is not None else "",
            "true_peak_dbtp": peak if peak is not None else "",
            "technical_grade": technical,
            "human_grade_1_to_5": subjective,
            "human_review_state": "OPEN_DEVICE_LISTENING",
            "severity": severity,
            "decision": decision,
            "runtime_reference_count": text.count(basename),
            "routing": "dynamic_voice" if category(rel) == "voice" else "asset_or_dynamic",
            "provenance": "protected_original" if kind else (
                "provisional_filler_manifest" if filler else "see_ASSET_LICENSES"),
        })
    return rows


def csv_text(rows: list[dict[str, object]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().replace("\r\n", "\n")


def summary(rows: list[dict[str, object]],
            filler_validation: dict[str, object] | None = None,
            protected_validation: dict[str, object] | None = None,
            teacher_validation: dict[str, object] | None = None) -> dict[str, object]:
    technical = Counter(str(row["technical_grade"]) for row in rows)
    decisions = Counter(str(row["decision"]) for row in rows)
    categories = Counter(str(row["category"]) for row in rows)
    return {
        "schema": "reef.audio-quality-audit.v1",
        "inventory_count": len(rows),
        "inventory_sha256": hashlib.sha256(csv_text(rows).encode()).hexdigest(),
        "technical_grades": dict(sorted(technical.items())),
        "categories": dict(sorted(categories.items())),
        "cohorts": dict(sorted(Counter(str(row["cohort"]) for row in rows).items())),
        "decisions": dict(sorted(decisions.items())),
        "protected_count": sum(bool(row["protected"]) for row in rows),
        "protected_recordings": protected_validation or {},
        "filler_manifest": {
            key: value for key, value in (filler_validation or {}).items()
            if key != "expected_names"
        },
        "teacher_manifest": {
            key: value for key, value in (teacher_validation or {}).items()
            if key not in {"declared_keys", "expected_names"}
        },
        "human_review_state": "OPEN_DEVICE_LISTENING",
        "required_external_gates": [
            "owner voice identity", "Lenovo Tab M11", "older Android phone",
            "mono fold-down", "child comprehension",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out-dir", type=Path, default=Path("audit"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    csv_path = out_dir / "audio_quality_ledger_2026-08-24.csv"
    json_path = out_dir / "audio_quality_summary_2026-08-24.json"
    teacher_validation = validate_teacher_manifest(root)
    teacher_keys = set(teacher_validation.get("declared_keys", set()))
    filler_validation = validate_filler_manifest(
        root, authoritative_filler_lines(root, teacher_keys))
    protected_validation = protected_audit(root)
    rows = build_rows(root, filler_validation)
    rendered_csv = csv_text(rows)
    rendered_json = json.dumps(
        summary(rows, filler_validation, protected_validation, teacher_validation),
        indent=2, sort_keys=True,
    ) + "\n"
    blocking = (list(filler_validation.get("issues", []))
                + list(teacher_validation.get("issues", []))
                + list(protected_validation.get("issues", [])))
    if blocking:
        print("AUDIO_QUALITY|BLOCKED|" + " | ".join(str(item) for item in blocking))
        return 1
    if args.check:
        ok = (csv_path.read_text(encoding="utf-8") == rendered_csv
              and json_path.read_text(encoding="utf-8") == rendered_json)
        print(f"AUDIO_QUALITY|check {len(rows)}/{len(rows)}|{'PASS' if ok else 'STALE'}")
        return 0 if ok else 1
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path.write_text(rendered_csv, encoding="utf-8", newline="")
    json_path.write_text(rendered_json, encoding="utf-8", newline="")
    print(f"AUDIO_QUALITY|write {len(rows)}|{csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
