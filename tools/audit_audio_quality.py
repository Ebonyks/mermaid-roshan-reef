#!/usr/bin/env python3
"""Deterministic technical/semantic inventory for every production audio file."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


AUDIO_SUFFIXES = {".ogg", ".wav", ".mp3"}
VOICE_ROOT_REL = "assets/audio/voices/"
FILLER_ROOT_REL = "assets/audio/voices/filler_v1/"
FILLER_MANIFEST_NAME = "FILLER_MANIFEST.json"
PROTECTED = {
    "assets/audio/voices/chuck.ogg",
    "assets/audio/voices/chuck_bark.ogg",
    "assets/audio/voices/chuck_whimper.ogg",
    "assets/audio/voices/daddy1.ogg",
    "assets/audio/voices/daddy2.ogg",
    "assets/audio/voices/daddy3.ogg",
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
        if abs(float(actual) - float(expected)) > tolerance:
            issues.append(f"{label} mismatch: actual={actual!r} manifest={expected!r}")
    except (TypeError, ValueError):
        if actual != expected:
            issues.append(f"{label} mismatch: actual={actual!r} manifest={expected!r}")


def authoritative_filler_lines(root: Path) -> dict[str, tuple[str, str]]:
    """Read the literal generator catalog without importing generation code."""
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
    expected = {
        key: value for key, value in lines.items() if value[0] != "faron"
    }
    expected["everyone"] = ("everyone", "Hooray!")
    return expected


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
        if entry.get("status") != "PROVISIONAL_SYNTHETIC_FILLER":
            issues.append(f"{name} has invalid provisional status")
        if entry.get("character") in {"faron", "daddy", "chuck"}:
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
        else:
            attempt = entry.get("selected_attempt")
            if not isinstance(attempt, int) or attempt < 1:
                issues.append(f"{name} has invalid selected_attempt")
            elif f"attempt_{attempt}" not in generation_runs:
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
        delivery = entry.get("delivery_metrics")
        if not isinstance(delivery, dict):
            issues.append(f"{name} has no delivery_metrics")
            delivery = {}
        if not meta.get("decode_ok"):
            issues.append(f"{name} cannot be decoded: {meta.get('probe_error', 'unknown error')}")
            continue
        duration = float(delivery.get("duration_s", 0.0) or 0.0)
        if not 0.25 <= duration <= 30.0:
            issues.append(f"{name} duration outside voice bounds: {duration}")
        if int(delivery.get("decoded_clipped_samples", -1) or 0) != 0:
            issues.append(f"{name} has decoded clipped samples")
        dc_offset = delivery.get("dc_offset")
        if dc_offset is None or abs(float(dc_offset)) > 0.01:
            issues.append(f"{name} has invalid DC offset: {dc_offset!r}")
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
    if rel.startswith("assets/audio/voices/") or rel == "assets/audio/voice_yay.mp3":
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
            protected_validation: dict[str, object] | None = None) -> dict[str, object]:
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
    filler_validation = validate_filler_manifest(root)
    protected_validation = protected_audit(root)
    rows = build_rows(root, filler_validation)
    rendered_csv = csv_text(rows)
    rendered_json = json.dumps(
        summary(rows, filler_validation, protected_validation),
        indent=2, sort_keys=True,
    ) + "\n"
    blocking = list(filler_validation.get("issues", [])) + list(protected_validation.get("issues", []))
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
