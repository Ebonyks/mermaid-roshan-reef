#!/usr/bin/env python3
"""Master selected provisional voice takes into the non-destructive runtime layer."""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import math
import re
import shutil
import struct
import subprocess
import tempfile
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "tmp" / "filler_selection_report.json"
DEFAULT_CANDIDATES = ROOT / "tmp" / "filler_candidates" / "parler"
DEFAULT_OUT = ROOT / "assets" / "audio" / "voices" / "filler_v1"
PROTECTED_PATTERNS = (
    "faron*.ogg", "daddy*.ogg", "chuck.ogg", "chuck_bark.ogg",
    "chuck_whimper.ogg",
)
ALLOWED_DADDY_FILLERS = {
    "daddy_dance_talk", "daddy_dance_win", "daddy_assist_ready",
    "daddy_hide_seek_start", "daddy_hide_seek_found", "daddy_hide_seek_visit",
}
LIMITER_LINEAR = 0.668344  # -3.5 dBFS; leaves margin for Vorbis reconstruction.
PROMPT_WORD_EQUIVALENTS = {
    "aw": "aww", "ah": "aww", "oh": "aww",
    "woo": "wow", "wooo": "wow", "woooo": "wow", "wooooo": "wow",
    "woooow": "wow", "whoooaa": "whoa",
    "we": "whee", "wee": "whee", "weee": "whee", "wheee": "whee",
    "teehee": "heehee", "hihi": "heehee", "hehe": "heehee", "hehehe": "heehee",
    "hulu": "huluu", "huloo": "huluu", "huluo": "huluu", "hulaloo": "huluu",
    "lamb": "lamba", "lamma": "lamba", "lambda": "lamba", "lemma": "lamba",
    "plushie": "plushy", "cart": "kart", "card": "kart",
    "colour": "color", "dr": "doctor", "karim": "kareem",
    "flower": "flour", "shoe": "shoo",
    "bleh": "blegh", "blah": "blegh", "em": "them",
    "tada": "tadaa", "tadah": "tadaa",
}
GROUP_F0_RANGES = {
    "roshan": (225.0, 360.0),
    "huluu": (145.0, 275.0),
    "evie": (190.0, 340.0),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_text_sha256(path: Path) -> str:
    """Hash UTF-8 source with platform-independent LF line endings."""
    text = path.read_text(encoding="utf-8")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def root_relative(path: Path) -> str:
    """Return a portable repository-relative artifact path for provenance."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        # This should only be reached for a caller-supplied staging path.  Keep
        # the record useful without serialising a machine-specific absolute
        # path into the shipped manifest.
        return path.name


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def normalize_prompt_words(value: str) -> list[str]:
    """Use the selector's narrow reviewed semantic-word normalization."""
    normalized = value.lower().replace("lamb-a", "lamba")
    for contraction, expanded in {
        "he's": "he is", "you'll": "you will", "didn't": "did not",
        "that's": "that is", "i'm": "i am", "it's": "it is",
        "let's": "let us", "where's": "where is",
    }.items():
        normalized = normalized.replace(contraction, expanded)
    normalized = normalized.replace("re-laying", "relaying").replace("re laying", "relaying")
    normalized = normalized.replace("tip-toe", "tiptoe").replace("tee hee", "heehee")
    normalized = normalized.replace("uh oh", "oh")
    normalized = re.sub(r"\bmyoo[ -]?sha\b", "mewsha", normalized)
    normalized = re.sub(r"\bta[ -]?da+a\b", "tadaa", normalized)
    normalized = re.sub(r"\bsh+h+\b", "shh", normalized)
    normalized = re.sub(r"\bhee[ -]+hee(?:[ -]+hee)*\b", "heehee", normalized)
    canonical = [
        PROMPT_WORD_EQUIVALENTS.get(word, word)
        for word in re.findall(r"[a-z0-9]+", normalized)
    ]
    collapsed: list[str] = []
    for word in canonical:
        if word == "shh" and collapsed and collapsed[-1] == "shh":
            continue
        if word in {"he", "hee", "heehee"}:
            if not collapsed or collapsed[-1] != "heehee":
                collapsed.append("heehee")
        else:
            collapsed.append(word)
    return collapsed


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


def ogg_container_evidence(path: Path) -> dict[str, object]:
    """Capture the byte-level Ogg structure used by the repeatability gate."""
    payload = path.read_bytes()
    cursor = 0
    serials: set[int] = set()
    page_crcs: list[bytes] = []
    page_count = 0
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
        serials.add(int.from_bytes(payload[cursor + 14:cursor + 18], "little"))
        page_crcs.append(bytes(payload[cursor + 22:cursor + 26]))
        page_count += 1
        cursor = page_end
    if not page_count:
        raise RuntimeError(f"empty Ogg stream: {path}")
    return {
        "file_sha256": sha256_file(path),
        "byte_length": len(payload),
        "page_count": page_count,
        "serials": sorted(serials),
        "page_crc_sha256": hashlib.sha256(b"".join(page_crcs)).hexdigest(),
    }


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


def final_metrics(path: Path) -> dict[str, object]:
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


def encode_ogg(source: Path, destination: Path, audio_filter: str,
               serial_offset: int) -> list[str]:
    command = [
        "ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(source),
        "-af", audio_filter, "-ac", "1", "-c:a", "libvorbis", "-b:a", "96k",
        "-serial_offset", str(serial_offset), str(destination),
    ]
    run(command)
    stabilize_ogg_pages(destination, serial_offset)
    return command


def master_source(source: Path, destination: Path) -> tuple[
        dict[str, object], list[str]]:
    """Master one source WAV and return verified metrics plus portable command."""
    measured = loudnorm_measure(source)
    gain_db = -16.0 - float(measured["input_i"])
    serial_offset = int.from_bytes(
        hashlib.sha256(destination.stem.encode("utf-8")).digest()[:4], "big"
    ) & 0x7FFFFFFF
    metrics: dict[str, object] = {}
    command_provenance: list[str] = []
    audio_filter = ""
    for _master_attempt in range(5):
        audio_filter = (
            f"volume={gain_db:.3f}dB,"
            f"alimiter=limit={LIMITER_LINEAR}:attack=5:release=50:level=false,"
            "aresample=48000"
        )
        encode_ogg(source, destination, audio_filter, serial_offset)
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

    # FFmpeg's Ogg muxer normally chooses a random serial.  We replace it with
    # a key-derived serial above, then prove byte-for-byte repeatability by
    # encoding the identical source a second time with the identical command.
    # This evidence is retained in the final manifest; a file hash alone does
    # not explain whether deterministic encoding was actually tested.
    repeat_path = destination.with_name(destination.stem + ".determinism.ogg")
    try:
        encode_ogg(source, repeat_path, audio_filter, serial_offset)
        first_ogg = ogg_container_evidence(destination)
        repeat_ogg = ogg_container_evidence(repeat_path)
        if first_ogg["file_sha256"] != repeat_ogg["file_sha256"]:
            raise RuntimeError(
                f"non-deterministic Ogg encode for {destination}: "
                f"{first_ogg['file_sha256']} != {repeat_ogg['file_sha256']}"
            )
        metrics["ogg_determinism"] = {
            "verified": True,
            "method": "identical source/filter/FFmpeg command; fixed serial and recomputed page CRCs",
            "primary": first_ogg,
            "repeat": repeat_ogg,
            "serial_offset": serial_offset,
        }
    finally:
        repeat_path.unlink(missing_ok=True)
    return metrics, command_provenance


def mix_group_pcm16(sources: list[Path], delays_ms: list[int],
                    destination: Path) -> dict[str, object]:
    """Deterministically sum mono PCM16 WAVs with fixed sample offsets."""
    if len(sources) != len(delays_ms) or not sources:
        raise RuntimeError("group mix sources/delays are invalid")
    sample_rate = 0
    decoded: list[array.array[int]] = []
    for source in sources:
        with wave.open(str(source), "rb") as handle:
            if handle.getnchannels() != 1 or handle.getsampwidth() != 2 \
                    or handle.getcomptype() != "NONE":
                raise RuntimeError(f"group component is not mono PCM16: {source}")
            if sample_rate == 0:
                sample_rate = handle.getframerate()
            elif handle.getframerate() != sample_rate:
                raise RuntimeError("group component sample rates do not match")
            samples = array.array("h")
            samples.frombytes(handle.readframes(handle.getnframes()))
            decoded.append(samples)
    offsets = [round(sample_rate * delay_ms / 1000) for delay_ms in delays_ms]
    frame_count = max(offset + len(samples) for offset, samples in zip(offsets, decoded))
    accumulator = [0] * frame_count
    for offset, samples in zip(offsets, decoded):
        for index, sample in enumerate(samples):
            accumulator[offset + index] += int(sample)
    divisor = len(decoded)
    mixed = array.array("h", (
        max(-32768, min(32767, int(value / divisor))) for value in accumulator
    ))
    with wave.open(str(destination), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(mixed.tobytes())
    return {
        "implementation": "python-stdlib-wave deterministic PCM16 integer mix",
        "sample_rate_hz": sample_rate,
        "channels": 1,
        "sample_width_bytes": 2,
        "delays_ms": delays_ms,
        "normalization_divisor": divisor,
        "frame_count": frame_count,
    }


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


def candidate_row_with_hash(row: dict[str, object], manifest_path: Path) -> dict[str, object]:
    """Copy one generated row while making its ignored WAV auditable later."""
    declared_path = Path(str(row.get("raw_path", ""))).resolve()
    local_path = (manifest_path.parent / declared_path.name).resolve()
    raw_path = local_path if local_path.is_file() else declared_path
    if not raw_path.is_file():
        raise RuntimeError(
            f"candidate WAV is unavailable; cannot preserve durable evidence: {raw_path}"
        )
    raw_sha = sha256_file(raw_path)
    declared_sha = row.get("raw_sha256")
    if declared_sha and str(declared_sha).lower() != raw_sha:
        raise RuntimeError(
            f"candidate hash mismatch in {manifest_path}: {raw_path}"
        )
    durable = dict(row)
    durable["raw_path"] = root_relative(raw_path)
    durable["raw_sha256"] = raw_sha
    durable["raw_hash_verified"] = True
    return durable


def rejected_candidate_reasons(candidate: dict[str, object], threshold: float,
                               selected: bool) -> list[str]:
    if selected:
        return []
    reasons: list[str] = []
    primary_wer = candidate.get("wer")
    secondary_wer = candidate.get("secondary_wer")
    if primary_wer != 0.0 and secondary_wer != 0.0:
        reasons.append("ASR_WORD_ERROR_RATE_NONZERO")
    score = candidate.get("selection_score")
    if score is None or float(score) < threshold:
        reasons.append("SELECTION_SCORE_BELOW_THRESHOLD")
    if candidate.get("f0_median_hz") is None:
        reasons.append("F0_UNAVAILABLE")
    if int(candidate.get("clipped_samples") or 0) != 0:
        reasons.append("CLIPPED_SAMPLES")
    if not reasons:
        reasons.append("LOWER_SCORE_THAN_SELECTED_ELIGIBLE_TAKE")
    return reasons


def selection_evidence(report: list[dict[str, object]],
                       selection_provenance: dict[str, object],
                       local_candidates: dict[tuple[int, str, str], Path]
                       ) -> dict[str, object]:
    """Embed selected and rejected candidate hashes instead of relying on tmp/."""
    minimum = float(selection_provenance.get("minimum_selection_score", 0.0))
    short_minimum = float(selection_provenance.get("minimum_short_selection_score", minimum))
    short_max_words = int(selection_provenance.get("short_selection_max_words", 2))
    evidence: dict[str, object] = {}
    for row in report:
        expected = str(row["expected"])
        word_count = len(re.findall(r"[A-Za-z0-9]+", expected))
        threshold = short_minimum if word_count <= short_max_words else minimum
        chosen = row.get("chosen")
        chosen_identity = (
            int(chosen.get("attempt", -1)), str(row["key"]),
            str(chosen.get("selected_raw_sha256") or chosen.get("source_sha256") or "").lower(),
        ) if isinstance(chosen, dict) else None
        candidate_records: list[dict[str, object]] = []
        for candidate in row.get("candidates", []):
            if not isinstance(candidate, dict):
                raise RuntimeError(f"invalid candidate record for {row['key']}")
            identity = (
                int(candidate.get("attempt", -1)), str(row["key"]),
                str(candidate.get("source_sha256") or "").lower(),
            )
            path = local_candidates.get(
                identity, Path(str(candidate.get("path", ""))).resolve(),
            )
            durable = dict(candidate)
            if not path.is_file():
                raise RuntimeError(
                    f"candidate WAV is unavailable; cannot preserve durable evidence: {path}"
                )
            raw_sha = sha256_file(path)
            declared_sha = candidate.get("source_sha256")
            if declared_sha and str(declared_sha).lower() != raw_sha:
                raise RuntimeError(f"selection report hash mismatch: {path}")
            durable["path"] = root_relative(path)
            durable["raw_sha256"] = raw_sha
            durable["raw_hash_verified"] = True
            selected = chosen_identity == identity
            durable["selection_disposition"] = "SELECTED" if selected else "REJECTED"
            durable["rejection_reasons"] = rejected_candidate_reasons(
                candidate, threshold, selected,
            )
            candidate_records.append(durable)
        selected_record = next(
            (item for item in candidate_records if item["selection_disposition"] == "SELECTED"),
            None,
        )
        if row.get("status") == "SELECTED" and selected_record is None:
            raise RuntimeError(f"selected candidate missing from evidence: {row['key']}")
        evidence[str(row["key"])] = {
            "character": row["character"], "expected": expected,
            "status": row["status"], "threshold": threshold,
            "candidate_count": len(candidate_records),
            "selected_attempt": selected_record.get("attempt") if selected_record else None,
            "selected_seed": selected_record.get("seed") if selected_record else None,
            "selected_raw_sha256": selected_record.get("raw_sha256") if selected_record else None,
            "candidates": candidate_records,
        }
    return evidence


def validate_selected_input(row: dict[str, object], chosen: dict[str, object],
                            source_meta: dict[str, object], source: Path) -> None:
    """Reject a report/source mismatch before any delivery bytes are made."""
    if str(source_meta.get("key")) != str(row["key"]):
        raise RuntimeError(f"selected source key mismatch for {row['key']}")
    if str(source_meta.get("character")) != str(row["character"]):
        raise RuntimeError(f"selected source character mismatch for {row['key']}")
    catalog_text = str(source_meta.get("text") or "")
    expected_words = normalize_prompt_words(str(row["expected"]))
    if normalize_prompt_words(catalog_text) != expected_words:
        raise RuntimeError(f"selected source catalog text mismatch for {row['key']}")
    generated_segments = source_meta.get("generation_segments")
    if isinstance(generated_segments, list) and generated_segments:
        effective_text = " ".join(str(segment) for segment in generated_segments)
    else:
        effective_text = str(source_meta.get("generation_text") or source_meta.get("text"))
    effective_words = normalize_prompt_words(effective_text)
    semantic_words = chosen.get("semantic_gate_expected_words")
    authorized_words = [str(word) for word in semantic_words] \
        if isinstance(semantic_words, list) and semantic_words else expected_words
    if effective_words != authorized_words:
        raise RuntimeError(f"selected source transcript mismatch for {row['key']}")
    manifest_source = Path(str(source_meta.get("raw_path", ""))).resolve()
    if manifest_source != source and manifest_source.name != source.name:
        raise RuntimeError(f"selected source path mismatch for {row['key']}")
    for field in ("attempt", "seed"):
        if int(chosen.get(field, -1)) != int(source_meta.get(field, -2)):
            raise RuntimeError(f"selected {field} mismatch for {row['key']}")
    generation_fields = (
        source_meta.get("generation_text"),
        source_meta.get("generation_segments"),
        source_meta.get("segment_seeds"),
    )
    captured_fields = [value is not None for value in generation_fields]
    if not all(captured_fields):
        # Attempts 1-5 used the original one-prompt/one-seed renderer;
        # attempts 6-7 added generation_text before explicit segment arrays.
        # Their immutable manifests still capture exact text, seed,
        # description, model revision and WAV hash. Preserve the missing
        # fields as explicitly reconstructed evidence, and reject this legacy
        # compatibility path for the complete schema introduced in attempt 8.
        if int(source_meta.get("attempt", -1)) > 7:
            raise RuntimeError(f"selected generation prompt is incomplete for {row['key']}")
        if source_meta.get("generation_text") is not None \
                and not str(source_meta.get("generation_text")):
            raise RuntimeError(f"selected generation text is empty for {row['key']}")
        return
    if not source_meta.get("generation_text") or not source_meta.get("generation_segments"):
        raise RuntimeError(f"selected generation prompt is incomplete for {row['key']}")
    if not source_meta.get("segment_seeds"):
        raise RuntimeError(f"selected segment seeds are missing for {row['key']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--selection-provenance", type=Path)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    incomplete = [row["key"] for row in report if row["status"] != "SELECTED"]
    if incomplete:
        parser.error(f"selection cohort is incomplete ({len(incomplete)} retry lines)")
    selection_provenance_path = args.selection_provenance
    if selection_provenance_path is None:
        selection_provenance_path = args.report.with_name(
            args.report.name.replace("filler_selection_report", "filler_selection_provenance")
        )
    if not selection_provenance_path.exists():
        parser.error("selection provenance is missing")
    selection_provenance = json.loads(selection_provenance_path.read_text(encoding="utf-8"))
    provenance: dict[str, dict[str, object]] = {}
    local_candidates: dict[tuple[int, str, str], Path] = {}
    generation_runs: dict[str, object] = {}
    for manifest_path in sorted(args.candidates.glob("attempt_*/*manifest.json")):
        manifest_bytes = manifest_path.read_bytes()
        manifest_rows = json.loads(manifest_bytes.decode("utf-8"))
        manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
        durable_rows = [candidate_row_with_hash(row, manifest_path) for row in manifest_rows]
        attempts = sorted({int(row["attempt"]) for row in manifest_rows})
        for row, durable_row in zip(manifest_rows, durable_rows):
            declared_path = Path(str(row["raw_path"])).resolve()
            local_path = (manifest_path.parent / declared_path.name).resolve()
            provenance[str(declared_path)] = row
            provenance[str(local_path)] = row
            local_candidates[(
                int(row["attempt"]), str(row["key"]),
                str(durable_row["raw_sha256"]).lower(),
            )] = local_path
        run_path = manifest_path.with_name("run_provenance.json")
        if run_path.exists():
            base_run_record = json.loads(run_path.read_text(encoding="utf-8"))
            base_run_record["capture_state"] = "CAPTURED_AT_GENERATION"
        else:
            # Attempts 1-2 predated run_provenance.json.  Preserve every
            # reproducibility field that was captured in their candidate
            # manifest and explicitly label the one unavailable historical
            # datum instead of silently dropping the runs.
            models = {str(row["model"]) for row in manifest_rows}
            revisions = {str(row["model_revision"]) for row in manifest_rows}
            tokenizer_revisions = {
                str(row["description_tokenizer_revision"]) for row in manifest_rows
            }
            base_run_record = {
                "attempt": attempts[0],
                "capture_state": "RECONSTRUCTED_FROM_CANDIDATE_MANIFEST",
                "candidate_manifest_sha256": manifest_hash,
                "model": next(iter(models)),
                "model_revision": next(iter(revisions)),
                "description_tokenizer_revision": next(iter(tokenizer_revisions)),
                "parler_code_revision": "d108732cd57788ec86bc857d99a6cabd66663d68",
                "generator_sha256": "NOT_CAPTURED_AT_GENERATION",
            }
        for attempt in attempts:
            attempt_rows = [
                row for row in durable_rows if int(row["attempt"]) == attempt
            ]
            run_record = dict(base_run_record)
            run_record["attempt"] = attempt
            run_record["source_batch"] = manifest_path.parent.name
            run_record["candidate_manifest_path"] = root_relative(manifest_path)
            run_record["candidate_manifest_sha256"] = manifest_hash
            run_record["candidate_count"] = len(attempt_rows)
            run_record["candidate_rows_sha256"] = canonical_json_sha256(attempt_rows)
            run_record["candidate_rows"] = attempt_rows
            if run_path.exists():
                run_record["run_provenance_path"] = root_relative(run_path)
                run_record["run_provenance_sha256"] = sha256_file(run_path)
            generation_runs[f"attempt_{attempt}"] = run_record
    if not generation_runs:
        parser.error("no candidate generation manifests found")
    candidate_selection_evidence = selection_evidence(
        report, selection_provenance, local_candidates,
    )
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
            if str(row["key"]).startswith("everyone_"):
                # These are strictly audited source layers for everyone.ogg,
                # not independently addressable runtime cues.
                continue
            chosen = row["chosen"]
            source_identity = (
                int(chosen["attempt"]), str(row["key"]),
                str(chosen.get("selected_raw_sha256") or chosen.get("source_sha256") or "").lower(),
            )
            source = local_candidates.get(source_identity)
            if source is None:
                raise RuntimeError(f"selected source has no local candidate mirror: {row['key']}")
            source_sha = sha256_file(source)
            if source_sha != chosen.get("selected_raw_sha256"):
                raise RuntimeError(f"selected source hash mismatch for {row['key']}")
            source_meta = provenance.get(str(source))
            if not source_meta or source_sha != source_meta.get("raw_sha256"):
                raise RuntimeError(f"missing or mismatched candidate provenance for {row['key']}")
            validate_selected_input(row, chosen, source_meta, source)
            selection_record = candidate_selection_evidence.get(str(row["key"]))
            if not isinstance(selection_record, dict) \
                    or selection_record.get("selected_raw_sha256") != source_sha \
                    or selection_record.get("selected_attempt") != chosen.get("attempt") \
                    or selection_record.get("selected_seed") != chosen.get("seed"):
                raise RuntimeError(f"selection evidence mismatch for {row['key']}")
            character = str(row["character"])
            key = str(row["key"])
            if character in {"faron", "chuck"} \
                    or (character == "daddy" and key not in ALLOWED_DADDY_FILLERS):
                raise RuntimeError(f"protected speaker entered filler cohort: {row['key']}")
            destination = stage / f"{row['key']}.ogg"
            metrics, ffmpeg_command_provenance = master_source(source, destination)
            sanitized_selection = {
                key: value for key, value in chosen.items() if key != "path"
            }
            captured_generation_text = source_meta.get("generation_text")
            generation_segments = source_meta.get("generation_segments") \
                or [captured_generation_text or source_meta.get("text")]
            generation_text = " ".join(str(segment) for segment in generation_segments)
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
                "candidate_manifest_text": source_meta.get("text"),
                "candidate_manifest_generation_text": captured_generation_text,
                "selection_metrics": sanitized_selection,
                "selected_input_provenance": {
                    "candidate_path": root_relative(source),
                    "candidate_manifest": root_relative(
                        Path(str(source_meta.get("raw_path", source))).resolve().parent
                        / "trial_manifest.json"
                    ),
                    "attempt": chosen["attempt"], "seed": chosen["seed"],
                    "raw_sha256": source_sha, "validated": True,
                },
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
        report_by_key = {str(item["key"]): item for item in report}
        components = []
        component_source_paths: list[Path] = []
        for component_key in component_keys:
            component_report = report_by_key.get(component_key)
            chosen_component = component_report.get("chosen") \
                if isinstance(component_report, dict) else None
            chosen_identity = (
                int(chosen_component.get("attempt", -1)), component_key,
                str(chosen_component.get("selected_raw_sha256")
                    or chosen_component.get("source_sha256") or "").lower(),
            ) if isinstance(chosen_component, dict) else None
            chosen_path = local_candidates.get(chosen_identity) \
                if chosen_identity is not None else None
            components.append(provenance.get(str(chosen_path)) if chosen_path else None)
            if chosen_path is not None:
                component_source_paths.append(chosen_path)
        if any(component is None for component in components):
            raise RuntimeError("missing generated component for everyone.ogg")
        component_selection_records: list[dict[str, object]] = []
        for component_key, component, selected_component_path in zip(
                component_keys, components, component_source_paths):
            selection_record = candidate_selection_evidence.get(component_key)
            if not isinstance(selection_record, dict):
                raise RuntimeError(
                    f"missing strict ASR/DNSMOS selection evidence for {component_key}; "
                    "duration-only group mixing is forbidden"
                )
            selected_candidates = [
                candidate for candidate in selection_record.get("candidates", [])
                if isinstance(candidate, dict)
                and candidate.get("selection_disposition") == "SELECTED"
            ]
            if len(selected_candidates) != 1:
                raise RuntimeError(
                    f"{component_key} must have exactly one selected candidate record"
                )
            selected_candidate = selected_candidates[0]
            if (selected_candidate.get("wer") != 0.0
                    and selected_candidate.get("secondary_wer") != 0.0):
                raise RuntimeError(f"{component_key} has no zero-WER ASR gate")
            for field in ("selection_score", "dnsmos_ovrl", "dnsmos_sig", "dnsmos_bak",
                          "f0_median_hz", "semantic_gate_schema"):
                if selected_candidate.get(field) is None:
                    raise RuntimeError(f"{component_key} missing strict evidence: {field}")
            if selected_candidate.get("semantic_gate_schema") != 3:
                raise RuntimeError(f"{component_key} has unsupported semantic gate schema")
            if int(selected_candidate.get("clipped_samples") or 0) != 0:
                raise RuntimeError(f"{component_key} has clipped samples")
            f0 = float(selected_candidate.get("f0_median_hz") or 0.0)
            f0_low, f0_high = GROUP_F0_RANGES[str(component["character"])]
            duration = float(selected_candidate.get("duration_s") or 0.0)
            active = float(selected_candidate.get("active_duration_s") or 0.0)
            voiced_fraction = float(
                selected_candidate.get("voiced_frame_fraction") or 0.0)
            if not (f0_low <= f0 <= f0_high):
                raise RuntimeError(f"{component_key} is outside its character F0 range")
            if not (0.35 <= active <= 2.5 and 0.35 <= duration <= 4.0 \
                    and active / max(duration, 0.001) >= 0.25 \
                    and voiced_fraction >= 0.20):
                raise RuntimeError(f"{component_key} failed active-speech bounds")
            if component.get("text") != "Hooray!" \
                    or component.get("generation_text") != "Hooray!" \
                    or selected_candidate.get("semantic_gate_expected_words") != ["hooray"] \
                    or selected_candidate.get("semantic_gate_transcript_words") != ["hooray"]:
                raise RuntimeError(f"{component_key} failed exact Hooray semantic identity")
            component_path = selected_component_path
            component_sha = sha256_file(component_path)
            if component_sha != selected_candidate.get("raw_sha256"):
                raise RuntimeError(f"{component_key} selection/source hash mismatch")
            if int(component.get("attempt", -1)) != int(selected_candidate.get("attempt", -2)) \
                    or int(component.get("seed", -1)) != int(selected_candidate.get("seed", -2)):
                raise RuntimeError(f"{component_key} attempt/seed mismatch")
            component_selection_records.append({
                "key": component_key,
                "attempt": component["attempt"], "seed": component["seed"],
                "raw_path": root_relative(component_path), "raw_sha256": component_sha,
                "selection": selected_candidate,
            })
        raw_component_paths = component_source_paths
        component_paths: list[Path] = []
        component_trim_records: list[dict[str, object]] = []
        trim_filter = (
            "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-55dB:"
            "stop_periods=1:stop_duration=0.25:stop_threshold=-55dB,apad=pad_dur=0.08"
        )
        for index, raw_component_path in enumerate(raw_component_paths):
            component_path = stage / f"everyone_component_{index}.wav"
            trim_command = [
                "ffmpeg", "-y", "-hide_banner", "-nostats", "-i",
                str(raw_component_path), "-af", trim_filter, "-ac", "1",
                str(component_path),
            ]
            run(trim_command)
            component_duration = float(json.loads(run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "json", str(component_path),
            ]).stdout)["format"]["duration"])
            if not 0.35 <= component_duration <= 2.5:
                raise RuntimeError(
                    f"group component duration outside bounds: {component_path} "
                    f"({component_duration:.3f}s)")
            component_paths.append(component_path)
            component_trim_records.append({
                "source_raw_sha256": sha256_file(raw_component_path),
                "trimmed_wav_sha256": sha256_file(component_path),
                "trimmed_duration_s": round(component_duration, 4),
                "ffmpeg_command": [
                    "ffmpeg", "-y", "-hide_banner", "-nostats", "-i",
                    "$COMPONENT_SOURCE_WAV", "-af", trim_filter, "-ac", "1",
                    "$TRIMMED_COMPONENT_WAV",
                ],
            })
        group_source = stage / "everyone_source.wav"
        mix_algorithm = mix_group_pcm16(
            component_paths, [0, 70, 140], group_source,
        )
        group_repeat_source = stage / "everyone_source.determinism.wav"
        repeat_mix_algorithm = mix_group_pcm16(
            component_paths, [0, 70, 140], group_repeat_source,
        )
        if mix_algorithm != repeat_mix_algorithm:
            raise RuntimeError("everyone mix algorithm evidence changed between passes")
        group_source_sha256 = sha256_file(group_source)
        group_repeat_sha256 = sha256_file(group_repeat_source)
        if group_source_sha256 != group_repeat_sha256:
            raise RuntimeError(
                "non-deterministic everyone source mix: "
                f"{group_source_sha256} != {group_repeat_sha256}"
            )
        everyone_path = stage / "everyone.ogg"
        everyone_metrics, everyone_master_command = master_source(group_source, everyone_path)
        component_records = []
        for component, selection_record, component_path in zip(
                components, component_selection_records, component_source_paths):
            component_records.append({
                key: value for key, value in component.items() if key != "raw_path"
            } | {
                "raw_path": root_relative(component_path),
                "raw_sha256": sha256_file(component_path),
                "selection_evidence": selection_record,
            })
        manifest_rows.append({
            "key": "everyone", "character": "everyone", "text": "Hooray!",
            "status": "PROVISIONAL_SYNTHETIC_FILLER",
            "model": component_records[0]["model"],
            "model_revision": component_records[0]["model_revision"],
            "description_tokenizer_revision": component_records[0]["description_tokenizer_revision"],
            "component_attempts": sorted({int(item["attempt"]) for item in component_records}),
            "components": component_records,
            "component_mix_input_trims": component_trim_records,
            "mix_algorithm": mix_algorithm,
            "mix_determinism": {
                "verified": True,
                "method": "deterministic PCM16 integer mix repeated byte-for-byte",
                "primary_source_wav_sha256": group_source_sha256,
                "repeat_source_wav_sha256": group_repeat_sha256,
            },
            "source_wav_sha256": group_source_sha256,
            "final_ogg_sha256": hashlib.sha256(everyone_path.read_bytes()).hexdigest(),
            "delivery_metrics": everyone_metrics,
            "ffmpeg_command": everyone_master_command,
        })
        group_source.unlink()
        group_repeat_source.unlink()
        for component_path in component_paths:
            component_path.unlink()
        print(
            f"FILLER_MASTER|everyone|{everyone_metrics['integrated_lufs']} LUFS|"
            f"{everyone_metrics['true_peak_dbtp']} dBTP")
        expected_files = {f"{row['key']}.ogg" for row in manifest_rows}
        actual_files = {path.name for path in stage.glob("*.ogg")}
        if actual_files != expected_files:
            raise RuntimeError("staged OGG set does not match manifest cohort")
        manifest = {
            "manifest_schema": 3,
            "provenance_schema": {
                "generation_runs": 3,
                "candidate_selection_evidence": 1,
                "deterministic_ogg_evidence": 1,
            },
            "status": "PROVISIONAL_SYNTHETIC_FILLER",
            "replacement_policy": "Replace with confirmed consented talent recordings when available.",
            "protected_recordings_modified": False,
            "faron_modified": False,
            "protected_recording_hashes": protected_hashes,
            "generation_run_provenance": generation_runs,
            "generation_attempt_count": len(generation_runs),
            "selection_provenance": selection_provenance,
            "selection_report": {
                "path": root_relative(args.report),
                "sha256": sha256_file(args.report),
            },
            "candidate_selection_evidence": candidate_selection_evidence,
            "pipeline_hash_mode": "utf8_lf",
            "pipeline_script_sha256": {
                path.relative_to(ROOT).as_posix(): normalized_text_sha256(path)
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
