#!/usr/bin/env python3
"""Master selected provisional voice takes into the non-destructive runtime layer."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "tmp" / "filler_selection_report.json"
DEFAULT_CANDIDATES = ROOT / "tmp" / "filler_candidates" / "parler"
DEFAULT_OUT = ROOT / "assets" / "audio" / "voices" / "filler_v1"
PROTECTED_PATTERNS = (
    "faron*.ogg", "daddy*.ogg", "chuck.ogg", "chuck_bark.ogg",
    "chuck_whimper.ogg",
)
LIMITER_LINEAR = 0.668344  # -3.5 dBFS; leaves margin for Vorbis reconstruction.


def stabilize_ogg_pages(path: Path, serial: int) -> None:
    """Replace FFmpeg's random Ogg serial and recompute every page checksum."""
    payload = bytearray(path.read_bytes())
    cursor = 0
    while cursor < len(payload):
        if payload[cursor:cursor + 4] != b"OggS" or cursor + 27 > len(payload):
            raise RuntimeError(f"invalid Ogg page at byte {cursor}: {path}")
        segment_count = payload[cursor + 26]
        header_end = cursor + 27 + segment_count
        if header_end > len(payload):
            raise RuntimeError(f"truncated Ogg lacing table at byte {cursor}: {path}")
        page_end = header_end + sum(payload[cursor + 27:header_end])
        if page_end > len(payload):
            raise RuntimeError(f"truncated Ogg page at byte {cursor}: {path}")
        payload[cursor + 14:cursor + 18] = serial.to_bytes(4, "little")
        payload[cursor + 22:cursor + 26] = b"\0\0\0\0"
        crc = 0
        for value in payload[cursor:page_end]:
            crc ^= value << 24
            for _bit in range(8):
                crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF \
                    if crc & 0x80000000 else (crc << 1) & 0xFFFFFFFF
        payload[cursor + 22:cursor + 26] = crc.to_bytes(4, "little")
        cursor = page_end
    path.write_bytes(payload)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError("command failed:\n" + " ".join(command) + "\n" + result.stderr[-4000:])
    return result


def loudnorm_measure(path: Path) -> dict[str, str]:
    result = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
        "loudnorm=I=-16:TP=-1.8:LRA=11:print_format=json",
        "-f", "null", "-",
    ])
    blocks = re.findall(r"\{\s*\"input_i\".*?\}", result.stderr, re.DOTALL)
    if not blocks:
        raise RuntimeError(f"no loudnorm measurement for {path}")
    return json.loads(blocks[-1])


def final_metrics(path: Path) -> dict[str, float | int | str]:
    probe = json.loads(run([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate,duration:format=bit_rate,duration",
        "-of", "json", str(path),
    ]).stdout)
    stream = probe["streams"][0]
    format_info = probe["format"]
    result = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-filter_complex", "ebur128=peak=true", "-f", "null", "-",
    ])
    matches = list(re.finditer(
        r"Summary:\s*\n\s*Integrated loudness:.*?I:\s*([-+\w.]+) LUFS"
        r".*?True peak:.*?Peak:\s*([-+\w.]+) dBFS",
        result.stderr, re.DOTALL,
    ))
    if not matches:
        raise RuntimeError(f"no final loudness measurement for {path}")
    integrated, peak = (float(value) for value in matches[-1].groups())
    decoded = subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
        "-f", "f32le", "-ac", "1", "-ar", "48000", "-",
    ], capture_output=True, check=True).stdout
    samples = [value[0] for value in struct.iter_unpack("<f", decoded)]
    if not samples or any(not math.isfinite(value) for value in samples):
        raise RuntimeError(f"non-finite or empty decode for {path}")
    peak_linear = max(abs(value) for value in samples)
    dc_offset = sum(samples) / len(samples)
    duration = float(format_info.get("duration") or stream.get("duration") or 0.0)
    return {
        "codec": str(stream["codec_name"]),
        "sample_rate_hz": int(stream["sample_rate"]),
        "channels": int(stream["channels"]),
        "bit_rate_bps": int(format_info.get("bit_rate") or stream.get("bit_rate") or 0),
        "duration_s": round(duration, 4),
        "integrated_lufs": integrated,
        "true_peak_dbtp": peak,
        "decoded_peak_linear": round(peak_linear, 7),
        "decoded_clipped_samples": sum(abs(value) >= 0.999 for value in samples),
        "dc_offset": round(dc_offset, 8),
    }


def master_source(source: Path, destination: Path) -> tuple[
        dict[str, float | int | str], list[str]]:
    """Master one source WAV and return verified metrics plus portable command."""
    measured = loudnorm_measure(source)
    gain_db = -16.0 - float(measured["input_i"])
    serial_offset = int.from_bytes(
        hashlib.sha256(destination.stem.encode("utf-8")).digest()[:4], "big"
    ) & 0x7FFFFFFF
    metrics: dict[str, float | int | str] = {}
    command_provenance: list[str] = []
    for _master_attempt in range(5):
        audio_filter = (
            f"volume={gain_db:.3f}dB,"
            f"alimiter=limit={LIMITER_LINEAR}:attack=5:release=50:level=false,"
            "aresample=48000"
        )
        run([
            "ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(source),
            "-af", audio_filter, "-ac", "1", "-c:a", "libvorbis", "-b:a", "96k",
            "-serial_offset", str(serial_offset),
            str(destination),
        ])
        stabilize_ogg_pages(destination, serial_offset)
        command_provenance = [
            "ffmpeg", "-y", "-hide_banner", "-nostats", "-i", "$SOURCE_WAV",
            "-af", audio_filter, "-ac", "1", "-c:a", "libvorbis", "-b:a", "96k",
            "-serial_offset", str(serial_offset),
            "$OUTPUT_OGG",
        ]
        metrics = final_metrics(destination)
        integrated = float(metrics["integrated_lufs"])
        if -17.0 <= integrated <= -15.0:
            break
        gain_db += max(-3.0, min(3.0, -16.0 - integrated))
    if metrics["codec"] != "vorbis" or metrics["sample_rate_hz"] != 48000 \
            or metrics["channels"] != 1 or metrics["bit_rate_bps"] < 64000 \
            or metrics["integrated_lufs"] < -17.0 \
            or metrics["integrated_lufs"] > -15.0 \
            or metrics["true_peak_dbtp"] > -1.5:
        raise RuntimeError(f"delivery gate failed for {destination}: {metrics}")
    if metrics["duration_s"] < 0.25 or metrics["duration_s"] > 30.0 \
            or metrics["decoded_clipped_samples"] != 0 \
            or abs(float(metrics["dc_offset"])) > 0.01:
        raise RuntimeError(f"decoded-signal gate failed for {destination}: {metrics}")
    return metrics, command_provenance


def committed_protected_hashes() -> dict[str, str]:
    voice_dir = ROOT / "assets" / "audio" / "voices"
    paths: set[Path] = set()
    for pattern in PROTECTED_PATTERNS:
        paths.update(voice_dir.glob(pattern))
    evidence: dict[str, str] = {}
    for path in sorted(paths):
        relative = path.relative_to(ROOT).as_posix()
        committed = subprocess.run(
            ["git", "show", f"HEAD:{relative}"], cwd=ROOT, capture_output=True, check=True,
        ).stdout
        expected = hashlib.sha256(committed).hexdigest()
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"protected recording changed: {relative}")
        evidence[relative] = actual
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    incomplete = [row["key"] for row in report if row["status"] != "SELECTED"]
    if incomplete:
        parser.error(f"selection cohort is incomplete ({len(incomplete)} retry lines)")
    provenance: dict[str, dict[str, object]] = {}
    component_provenance: dict[str, dict[str, object]] = {}
    generation_runs: dict[str, object] = {}
    for manifest_path in sorted(args.candidates.glob("attempt_*/*manifest.json")):
        manifest_bytes = manifest_path.read_bytes()
        manifest_rows = json.loads(manifest_bytes.decode("utf-8"))
        manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
        for row in manifest_rows:
            provenance[str(Path(str(row["raw_path"])).resolve())] = row
            component_provenance[str(row["key"])] = row
        run_path = manifest_path.with_name("run_provenance.json")
        if run_path.exists():
            run_record = json.loads(run_path.read_text(encoding="utf-8"))
            run_record["capture_state"] = "CAPTURED_AT_GENERATION"
            run_record["candidate_manifest_sha256"] = manifest_hash
        else:
            # Attempts 1-2 predated run_provenance.json.  Preserve every
            # reproducibility field that was captured in their candidate
            # manifest and explicitly label the one unavailable historical
            # datum instead of silently dropping the runs.
            attempts = {int(row["attempt"]) for row in manifest_rows}
            models = {str(row["model"]) for row in manifest_rows}
            revisions = {str(row["model_revision"]) for row in manifest_rows}
            tokenizer_revisions = {
                str(row["description_tokenizer_revision"]) for row in manifest_rows
            }
            run_record = {
                "attempt": next(iter(attempts)),
                "capture_state": "RECONSTRUCTED_FROM_CANDIDATE_MANIFEST",
                "candidate_manifest_sha256": manifest_hash,
                "model": next(iter(models)),
                "model_revision": next(iter(revisions)),
                "description_tokenizer_revision": next(iter(tokenizer_revisions)),
                "parler_code_revision": "d108732cd57788ec86bc857d99a6cabd66663d68",
                "generator_sha256": "NOT_CAPTURED_AT_GENERATION",
            }
        generation_runs[manifest_path.parent.name] = run_record
    selection_provenance_path = ROOT / "tmp" / "filler_selection_provenance.json"
    if not selection_provenance_path.exists():
        parser.error("selection provenance is missing")
    selection_provenance = json.loads(selection_provenance_path.read_text(encoding="utf-8"))
    expected_out = (ROOT / "assets" / "audio" / "voices" / "filler_v1").resolve()
    staging_root = (ROOT / "tmp").resolve()
    resolved_out = args.out.resolve()
    if resolved_out != expected_out and staging_root not in resolved_out.parents:
        parser.error("--out must be filler_v1 or a staging directory below tmp/")
    if args.out.exists():
        parser.error("runtime filler directory already exists; remove it explicitly before remastering")
    protected_hashes = committed_protected_hashes()
    manifest_rows: list[dict[str, object]] = []
    tmp_root = ROOT / "tmp"
    tmp_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="filler_master_", dir=tmp_root) as stage_name:
        stage = Path(stage_name)
        for row in report:
            chosen = row["chosen"]
            source = Path(str(chosen["path"])).resolve()
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            if source_sha != chosen.get("selected_raw_sha256"):
                raise RuntimeError(f"selected source hash mismatch for {row['key']}")
            source_meta = provenance.get(str(source))
            if not source_meta or source_sha != source_meta.get("raw_sha256"):
                raise RuntimeError(f"missing or mismatched candidate provenance for {row['key']}")
            if str(row["character"]) in {"faron", "daddy", "chuck"}:
                raise RuntimeError(f"protected speaker entered filler cohort: {row['key']}")
            destination = stage / f"{row['key']}.ogg"
            metrics, ffmpeg_command_provenance = master_source(source, destination)
            sanitized_selection = {
                key: value for key, value in chosen.items() if key != "path"
            }
            generation_text = source_meta.get("generation_text") or source_meta.get("text")
            generation_segments = source_meta.get("generation_segments") or [generation_text]
            segment_seeds = source_meta.get("segment_seeds") or [source_meta.get("seed")]
            prompt_capture_state = (
                "CAPTURED_AT_GENERATION"
                if source_meta.get("generation_text") is not None
                and source_meta.get("generation_segments") is not None
                and source_meta.get("segment_seeds") is not None
                else "RECONSTRUCTED_FROM_CANDIDATE_MANIFEST"
            )
            manifest_rows.append({
                "key": row["key"], "character": row["character"], "text": row["expected"],
                "status": "PROVISIONAL_SYNTHETIC_FILLER", "selected_attempt": chosen["attempt"],
                "seed": chosen["seed"], "mood": source_meta.get("mood"),
                "speaker_preset": source_meta.get("speaker"), "model": source_meta.get("model"),
                "model_revision": source_meta.get("model_revision"),
                "description_tokenizer_revision": source_meta.get("description_tokenizer_revision"),
                "description": source_meta.get("description"),
                "generation_text": generation_text,
                "generation_segments": generation_segments,
                "segment_seeds": segment_seeds,
                "generation_prompt_capture_state": prompt_capture_state,
                "selection_metrics": sanitized_selection,
                "source_wav_sha256": source_sha,
                "final_ogg_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                "delivery_metrics": metrics, "ffmpeg_command": ffmpeg_command_provenance,
            })
            print(f"FILLER_MASTER|{row['key']}|{metrics['integrated_lufs']} LUFS|{metrics['true_peak_dbtp']} dBTP")

        # The discovery and reminder repeat the same sentence.  Ship one
        # immutable take under both semantic keys so a delayed reminder keeps
        # identity/prosody stable; runtime also suppresses an immediate restart.
        talk_entry = next(item for item in manifest_rows if item["key"] == "harper")
        hint_entry = next(item for item in manifest_rows if item["key"] == "harper_hint")
        shutil.copyfile(stage / "harper.ogg", stage / "harper_hint.ogg")
        for field in (
                "selected_attempt", "seed", "mood", "speaker_preset", "model",
                "model_revision", "description_tokenizer_revision", "description",
                "generation_text", "generation_segments", "segment_seeds",
                "generation_prompt_capture_state",
                "selection_metrics", "source_wav_sha256", "delivery_metrics",
                "ffmpeg_command"):
            hint_entry[field] = talk_entry[field]
        hint_entry["final_ogg_sha256"] = hashlib.sha256(
            (stage / "harper_hint.ogg").read_bytes()).hexdigest()
        hint_entry["final_audio_alias_of"] = "harper"

        # Replace the legacy Kokoro group cheer with three pinned Parler
        # identities.  Slight offsets keep it intelligible on a mono tablet
        # speaker while still reading as several friends cheering together.
        component_keys = ["everyone_roshan", "everyone_huluu", "everyone_evie"]
        components = [component_provenance.get(key) for key in component_keys]
        if any(component is None for component in components):
            raise RuntimeError("missing generated component for everyone.ogg")
        component_paths = [Path(str(component["raw_path"])) for component in components]
        for component_path in component_paths:
            component_duration = float(json.loads(run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "json", str(component_path),
            ]).stdout)["format"]["duration"])
            if not 0.35 <= component_duration <= 2.5:
                raise RuntimeError(
                    f"group component duration outside bounds: {component_path} "
                    f"({component_duration:.3f}s)")
        group_source = stage / "everyone_source.wav"
        mix_command = [
            "ffmpeg", "-y", "-hide_banner", "-nostats",
            "-i", str(component_paths[0]), "-i", str(component_paths[1]),
            "-i", str(component_paths[2]), "-filter_complex",
            "[0]adelay=0[a0];[1]adelay=70[a1];[2]adelay=140[a2];"
            "[a0][a1][a2]amix=inputs=3:duration=longest:normalize=1",
            "-ac", "1", str(group_source),
        ]
        run(mix_command)
        everyone_path = stage / "everyone.ogg"
        everyone_metrics, everyone_master_command = master_source(group_source, everyone_path)
        component_records = []
        for component in components:
            component_path = Path(str(component["raw_path"]))
            component_records.append({
                key: value for key, value in component.items() if key != "raw_path"
            } | {"raw_sha256": hashlib.sha256(component_path.read_bytes()).hexdigest()})
        manifest_rows.append({
            "key": "everyone", "character": "everyone", "text": "Hooray!",
            "status": "PROVISIONAL_SYNTHETIC_FILLER",
            "model": component_records[0]["model"],
            "model_revision": component_records[0]["model_revision"],
            "description_tokenizer_revision": component_records[0]["description_tokenizer_revision"],
            "component_attempts": sorted({int(item["attempt"]) for item in component_records}),
            "components": component_records,
            "mix_command": [
                "ffmpeg", "-y", "-hide_banner", "-nostats",
                "-i", "$EVERYONE_ROSHAN_WAV", "-i", "$EVERYONE_HULUU_WAV",
                "-i", "$EVERYONE_EVIE_WAV", "-filter_complex",
                "[0]adelay=0[a0];[1]adelay=70[a1];[2]adelay=140[a2];"
                "[a0][a1][a2]amix=inputs=3:duration=longest:normalize=1",
                "-ac", "1", "$GROUP_SOURCE_WAV",
            ],
            "source_wav_sha256": hashlib.sha256(group_source.read_bytes()).hexdigest(),
            "final_ogg_sha256": hashlib.sha256(everyone_path.read_bytes()).hexdigest(),
            "delivery_metrics": everyone_metrics,
            "ffmpeg_command": everyone_master_command,
        })
        group_source.unlink()
        print(
            f"FILLER_MASTER|everyone|{everyone_metrics['integrated_lufs']} LUFS|"
            f"{everyone_metrics['true_peak_dbtp']} dBTP")
        expected_files = {f"{row['key']}.ogg" for row in manifest_rows}
        actual_files = {path.name for path in stage.glob("*.ogg")}
        if actual_files != expected_files:
            raise RuntimeError("staged OGG set does not match manifest cohort")
        manifest = {
            "status": "PROVISIONAL_SYNTHETIC_FILLER",
            "replacement_policy": "Replace with confirmed consented talent recordings when available.",
            "protected_recordings_modified": False,
            "faron_modified": False,
            "protected_recording_hashes": protected_hashes,
            "generation_run_provenance": generation_runs,
            "selection_provenance": selection_provenance,
            "pipeline_script_sha256": {
                path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (
                    ROOT / "tools" / "make_parler_voice_trials.py",
                    ROOT / "tools" / "select_filler_voices.py",
                    ROOT / "tools" / "master_filler_voices.py",
                )
            },
            "codec_target": "48 kHz mono Ogg Vorbis 96 kbps, -16 LUFS, <= -1.5 dBTP",
            "premaster_dynamics": (
                "Per-file measured gain with iterative EBU R128 verification and a "
                "-3.5 dBFS true-peak limiter before Vorbis encoding."
            ),
            "entries": manifest_rows,
        }
        (stage / "FILLER_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(stage, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
