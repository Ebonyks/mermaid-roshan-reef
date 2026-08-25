#!/usr/bin/env python3
"""Deterministic technical/semantic inventory for every production audio file."""

from __future__ import annotations

import argparse
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
PROTECTED = {
    "assets/audio/voice_yay.mp3",
    "assets/audio/voices/chuck.ogg",
    "assets/audio/voices/chuck_bark.ogg",
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
    if rel == "assets/audio/voice_yay.mp3":
        return "C", 1, "P1", "KEEP_PROTECTED_RESTRICT_FALLBACK"
    if rel.startswith("assets/audio/castle/"):
        return "C", 3, "P2", "LISTEN_REPLACE_CANDIDATE"
    if rel == "assets/audio/purr.wav":
        return "C", 3, "P2", "LISTEN_REPLACE_CANDIDATE"
    if rel in LEGACY_MUSIC:
        return "C", 3, "P2", "LISTEN_REPLACE_CANDIDATE"
    if rel in PROTECTED:
        return "B", 4, "P2", "KEEP_PROTECTED"
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


def build_rows(root: Path) -> list[dict[str, object]]:
    text = source_text(root)
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
        rows.append({
            "path": rel,
            "category": category(rel),
            "protected": rel in PROTECTED,
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
            "provenance": "protected_original" if rel in PROTECTED else "see_ASSET_LICENSES",
        })
    return rows


def csv_text(rows: list[dict[str, object]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().replace("\r\n", "\n")


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    technical = Counter(str(row["technical_grade"]) for row in rows)
    decisions = Counter(str(row["decision"]) for row in rows)
    categories = Counter(str(row["category"]) for row in rows)
    return {
        "schema": "reef.audio-quality-audit.v1",
        "inventory_count": len(rows),
        "inventory_sha256": hashlib.sha256(csv_text(rows).encode()).hexdigest(),
        "technical_grades": dict(sorted(technical.items())),
        "categories": dict(sorted(categories.items())),
        "decisions": dict(sorted(decisions.items())),
        "protected_count": sum(bool(row["protected"]) for row in rows),
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
    rows = build_rows(root)
    rendered_csv = csv_text(rows)
    rendered_json = json.dumps(summary(rows), indent=2, sort_keys=True) + "\n"
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
