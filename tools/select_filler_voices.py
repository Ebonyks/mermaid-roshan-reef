#!/usr/bin/env python3
"""Audit and select provisional synthetic voice takes from candidate batches.

Run this with the isolated audit environment documented in VOICE_MANIFEST.md.
It never writes runtime assets; accepted raw WAVs stay under ignored tmp/ until
the complete cohort has passed and is explicitly mastered for delivery.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

import librosa
import numpy as np
from faster_whisper import WhisperModel
from speechmos import dnsmos


ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "assets" / "audio" / "voices"
DEFAULT_CANDIDATES = ROOT / "tmp" / "filler_candidates" / "parler"
DEFAULT_SELECTED = ROOT / "tmp" / "filler_selected_raw"
MIN_SELECTION_SCORE = 2.65
MIN_SHORT_SELECTION_SCORE = 1.85
CACHE_SCHEMA = 3

# ASR systems routinely spell these authored names, sound words, and
# homophones differently even when the pronunciation is correct.  Keep this
# list deliberately narrow: it may remove spelling-only differences, but it
# must never forgive omitted instructions or ordinary word substitutions.
ASR_WORD_EQUIVALENTS = {
    "aw": "aww", "ah": "aww", "oh": "aww",
    "woo": "wow", "wooo": "wow", "woooo": "wow", "wooooo": "wow",
    "woooow": "wow", "whoooaa": "whoa",
    "we": "whee", "wee": "whee", "weee": "whee", "wheee": "whee",
    "teehee": "heehee", "hihi": "heehee", "hehe": "heehee", "hehehe": "heehee",
    "hulu": "huluu", "huloo": "huluu", "huluo": "huluu", "hulaloo": "huluu",
    "lamb": "lamba", "lamma": "lamba", "lambda": "lamba", "lemma": "lamba",
    "plushie": "plushy",
    "cart": "kart", "card": "kart",
    "colour": "color",
    "dr": "doctor",
    "karim": "kareem",
    "flower": "flour",
    "bunk": "bonk", "buck": "bonk",
    "bopped": "bop", "twirlbopped": "twirlbop",
    "shoe": "shoo",
    "bleh": "blegh", "blah": "blegh",
    "em": "them",
    "tada": "tadaa", "tadah": "tadaa",
}

F0_RANGES = {
    "roshan": (195.0, 290.0), "huluu": (145.0, 275.0),
    "evie": (190.0, 340.0), "harper": (145.0, 285.0),
    "rosalina": (135.0, 260.0), "imp": (135.0, 300.0),
    "wacky": (75.0, 195.0), "shop": (75.0, 205.0),
    "sparkle": (220.0, 500.0), "rumi": (160.0, 310.0),
    "mewsha": (180.0, 360.0),
}

EXPECTED_SPEAKERS = {
    "roshan": "Laura", "huluu": "Lea", "evie": "Jenna", "harper": "Lauren",
    "wacky": "Gary", "shop": "Jon", "sparkle": "Tina", "rosalina": "Rose",
    "imp": "Mike", "rumi": "Emily", "mewsha": "Joy",
}


def load_lines() -> dict[str, tuple[str, str]]:
    spec = importlib.util.spec_from_file_location("legacy_make_voices", ROOT / "tools" / "make_voices.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load tools/make_voices.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(module.LINES)


def normalize_words(text: str) -> list[str]:
    normalized = text.lower().replace("lamb-a", "lamba")
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
    words = re.findall(r"[a-z0-9]+", normalized)
    canonical = [ASR_WORD_EQUIVALENTS.get(word, word) for word in words]
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


def minimum_score(expected: str) -> float:
    return MIN_SHORT_SELECTION_SCORE if len(normalize_words(expected)) <= 2 else MIN_SELECTION_SCORE


def word_error_rate(expected: str, actual: str) -> float:
    left = normalize_words(expected)
    right = normalize_words(actual)
    previous = list(range(len(right) + 1))
    for index, word in enumerate(left, 1):
        current = [index]
        for other_index, other in enumerate(right, 1):
            current.append(min(
                previous[other_index] + 1,
                current[other_index - 1] + 1,
                previous[other_index - 1] + (word != other),
            ))
        previous = current
    return previous[-1] / max(1, len(left))


def loudness(path: Path) -> dict[str, float | None]:
    result = subprocess.run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-filter_complex", "ebur128=peak=true", "-f", "null", "-",
    ], capture_output=True, text=True, check=False)
    matches = list(re.finditer(
        r"Summary:\s*\n\s*Integrated loudness:.*?I:\s*([-+\w.]+) LUFS"
        r".*?Loudness range:.*?LRA:\s*([-+\w.]+) LU"
        r".*?True peak:.*?Peak:\s*([-+\w.]+) dBFS",
        result.stderr, re.DOTALL,
    ))
    if not matches:
        return {"integrated_lufs": None, "lra_lu": None, "true_peak_dbtp": None}
    values: list[float | None] = []
    for value in matches[-1].groups():
        try:
            values.append(round(float(value), 3))
        except ValueError:
            values.append(None)
    return dict(zip(("integrated_lufs", "lra_lu", "true_peak_dbtp"), values))


def signal_metrics(path: Path) -> dict[str, float | int | None]:
    source_sr = int(librosa.get_samplerate(path))
    audio, sr = librosa.load(path, sr=24000, mono=True)
    if not len(audio):
        return {"duration_s": 0.0, "codec_sample_rate_hz": source_sr}
    rms = librosa.feature.rms(y=audio, frame_length=1024, hop_length=240)[0]
    threshold = max(10 ** (-45 / 20), float(np.max(rms)) * 10 ** (-32 / 20))
    active_idx = np.flatnonzero(rms >= threshold)
    active_duration = max(0.001, len(active_idx) * 240 / sr)
    f0, voiced_flag, _voiced_prob = librosa.pyin(
        audio, fmin=65.0, fmax=500.0, sr=sr,
        frame_length=2048, hop_length=240,
    )
    voiced = f0[np.isfinite(f0)]
    f0_median = float(np.median(voiced)) if voiced.size >= 4 else None
    centroid = librosa.feature.spectral_centroid(
        y=audio, sr=sr, n_fft=1024, hop_length=240,
    )[0]
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13, n_fft=1024, hop_length=240)
    audio16 = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    mos = dnsmos.run(np.clip(audio16, -1.0, 1.0).astype(np.float32), sr=16000, return_df=False)
    result: dict[str, float | int | None] = {
        "duration_s": round(len(audio) / sr, 4),
        "active_duration_s": round(active_duration, 4),
        "peak_linear": round(float(np.max(np.abs(audio))), 6),
        "clipped_samples": int(np.count_nonzero(np.abs(audio) >= 0.999)),
        "f0_median_hz": round(f0_median, 2) if f0_median else None,
        "voiced_frame_fraction": round(float(np.mean(voiced_flag)), 4),
        "spectral_centroid_hz": round(
            float(np.median(centroid[active_idx])) if active_idx.size else float(np.median(centroid)), 2),
        "mfcc_mean": [round(float(value), 5) for value in np.mean(mfcc, axis=1)],
        "dnsmos_ovrl": round(float(mos["ovrl_mos"]), 4),
        "dnsmos_sig": round(float(mos["sig_mos"]), 4),
        "dnsmos_bak": round(float(mos["bak_mos"]), 4),
        "codec_sample_rate_hz": source_sr,
    }
    result.update(loudness(path))
    return result


def score(character: str, metrics: dict[str, object]) -> float:
    value = float(metrics["dnsmos_ovrl"])
    centroid = float(metrics.get("spectral_centroid_hz") or 0.0)
    if centroid < 900.0:
        value -= min(0.35, (900.0 - centroid) / 1200.0)
    f0 = metrics.get("f0_median_hz")
    low, high = F0_RANGES.get(character, (70.0, 500.0))
    if f0 is None:
        value -= 0.5
    elif float(f0) < low:
        value -= min(0.5, math.log2(low / max(float(f0), 1.0)))
    elif float(f0) > high:
        value -= min(0.5, math.log2(float(f0) / high))
    return round(value, 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--selected", type=Path, default=DEFAULT_SELECTED)
    parser.add_argument("--report", type=Path, default=ROOT / "tmp" / "filler_selection_report.json")
    parser.add_argument("--retry-file", type=Path, default=ROOT / "tmp" / "filler_retry_keys.txt")
    parser.add_argument(
        "--provenance", type=Path,
        default=ROOT / "tmp" / "filler_selection_provenance.json",
    )
    parser.add_argument(
        "--cache", type=Path,
        default=ROOT / "tmp" / "filler_candidate_audit_cache.json",
    )
    parser.add_argument("--secondary-whisper-model", default="small.en")
    args = parser.parse_args()
    lines = load_lines()
    manifests: list[dict[str, object]] = []
    for path in sorted(args.candidates.glob("attempt_*/*manifest.json")):
        manifests.extend(json.loads(path.read_text(encoding="utf-8")))
    by_key: dict[str, list[dict[str, object]]] = {}
    for entry in manifests:
        character = str(entry["character"])
        if entry.get("speaker") != EXPECTED_SPEAKERS.get(character):
            continue
        by_key.setdefault(str(entry["key"]), []).append(entry)
    whisper = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    secondary_whisper: WhisperModel | None = None
    cache: dict[str, dict[str, object]] = {}
    if args.cache.exists():
        cache_document = json.loads(args.cache.read_text(encoding="utf-8"))
        if cache_document.get("schema") == CACHE_SCHEMA:
            cache = dict(cache_document.get("entries", {}))
    args.selected.mkdir(parents=True, exist_ok=True)
    report: list[dict[str, object]] = []
    for key, (character, expected) in lines.items():
        if character == "faron":
            continue
        candidates: list[dict[str, object]] = []
        cache_keys: dict[str, str] = {}
        for entry in by_key.get(key, []):
            path = Path(str(entry["raw_path"]))
            if not path.exists():
                continue
            source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
            cache_key = hashlib.sha256(f"{source_sha}\0{expected}".encode()).hexdigest()
            cache_keys[str(path)] = cache_key
            if cache_key in cache:
                row = dict(cache[cache_key])
                row.update({"path": str(path), "attempt": entry.get("attempt"), "seed": entry.get("seed")})
                row["wer"] = round(word_error_rate(expected, str(row.get("transcript", ""))), 4)
                if "secondary_transcript" in row:
                    row["secondary_wer"] = round(word_error_rate(
                        expected, str(row["secondary_transcript"]),
                    ), 4)
            else:
                segments, _info = whisper.transcribe(
                    str(path), language="en", beam_size=5, best_of=5,
                    condition_on_previous_text=False, vad_filter=False,
                    word_timestamps=True, temperature=0.0,
                )
                segment_list = list(segments)
                transcript = " ".join(segment.text.strip() for segment in segment_list).strip()
                wer = word_error_rate(expected, transcript)
                row = {
                    "path": str(path), "attempt": entry.get("attempt"),
                    "seed": entry.get("seed"), "transcript": transcript,
                    "wer": round(wer, 4), "source_sha256": source_sha,
                    "asr_avg_logprob": round(float(np.mean([
                        segment.avg_logprob for segment in segment_list
                    ])), 4) if segment_list else None,
                }
                if wer == 0.0:
                    row.update(signal_metrics(path))
                    row["selection_score"] = score(character, row)
                cache[cache_key] = {
                    name: value for name, value in row.items()
                    if name not in {"path", "attempt", "seed"}
                }
            candidates.append(row)
        for row in candidates:
            if (
                (row.get("wer") == 0.0 or row.get("secondary_wer") == 0.0)
                and "selection_score" not in row
            ):
                path = Path(str(row["path"]))
                row.update(signal_metrics(path))
                row["selection_score"] = score(character, row)
                cache_key = cache_keys[str(path)]
                cache[cache_key] = {
                    name: value for name, value in row.items()
                    if name not in {"path", "attempt", "seed"}
                }
        if candidates and not any(row.get("wer") == 0.0 for row in candidates):
            if secondary_whisper is None:
                secondary_whisper = WhisperModel(
                    args.secondary_whisper_model, device="cpu", compute_type="int8",
                )
            for row in sorted(candidates, key=lambda item: int(item.get("attempt") or 0), reverse=True):
                path = Path(str(row["path"]))
                if "secondary_wer" not in row:
                    segments, _info = secondary_whisper.transcribe(
                        str(path), language="en", beam_size=5, best_of=5,
                        condition_on_previous_text=False, vad_filter=False,
                        word_timestamps=True, temperature=0.0,
                    )
                    segment_list = list(segments)
                    transcript = " ".join(
                        segment.text.strip() for segment in segment_list
                    ).strip()
                    row["secondary_transcript"] = transcript
                    row["secondary_wer"] = round(word_error_rate(expected, transcript), 4)
                    row["secondary_asr_avg_logprob"] = round(float(np.mean([
                        segment.avg_logprob for segment in segment_list
                    ])), 4) if segment_list else None
                    if row["secondary_wer"] == 0.0:
                        row.update(signal_metrics(path))
                        row["selection_score"] = score(character, row)
                    cache_key = cache_keys[str(path)]
                    cache[cache_key] = {
                        name: value for name, value in row.items()
                        if name not in {"path", "attempt", "seed"}
                    }
                if row.get("secondary_wer") == 0.0:
                    break
        threshold = minimum_score(expected)
        eligible = [
            row for row in candidates
            if (row.get("wer") == 0.0 or row.get("secondary_wer") == 0.0)
            and float(row.get("selection_score", -999.0)) >= threshold
            and row.get("f0_median_hz") is not None
            and int(row.get("clipped_samples") or 0) == 0
        ]
        chosen = max(eligible, key=lambda row: float(row["selection_score"])) if eligible else None
        if chosen is not None:
            primary_pass = chosen.get("wer") == 0.0
            chosen["semantic_gate_schema"] = CACHE_SCHEMA
            chosen["semantic_gate_asr"] = "primary" if primary_pass else "secondary"
            chosen["semantic_gate_transcript"] = (
                chosen.get("transcript") if primary_pass
                else chosen.get("secondary_transcript")
            )
            chosen["semantic_gate_expected_words"] = normalize_words(expected)
            chosen["semantic_gate_transcript_words"] = normalize_words(
                str(chosen["semantic_gate_transcript"])
            )
            destination = args.selected / f"{key}.wav"
            shutil.copyfile(Path(str(chosen["path"])), destination)
            chosen["selected_raw_sha256"] = hashlib.sha256(destination.read_bytes()).hexdigest()
        report.append({
            "key": key, "character": character, "expected": expected,
            "status": "SELECTED" if chosen else "RETRY_REQUIRED",
            "chosen": chosen, "candidates": candidates,
        })
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        args.cache.write_text(json.dumps(
            {"schema": CACHE_SCHEMA, "entries": cache}, indent=2, sort_keys=True,
        ) + "\n", encoding="utf-8")
        print(f"FILLER_SELECT|{key}|{report[-1]['status']}|{chosen.get('selection_score') if chosen else '-'}", flush=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    retry_keys = [str(row["key"]) for row in report if row["status"] == "RETRY_REQUIRED"]
    args.retry_file.write_text("\n".join(retry_keys) + ("\n" if retry_keys else ""), encoding="utf-8")
    selected_count = sum(row["status"] == "SELECTED" for row in report)
    speechmos_spec = importlib.util.find_spec("speechmos")
    speechmos_hashes: dict[str, str] = {}
    if speechmos_spec and speechmos_spec.submodule_search_locations:
        speechmos_root = Path(next(iter(speechmos_spec.submodule_search_locations)))
        speechmos_hashes = {
            path.relative_to(speechmos_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(speechmos_root.rglob("*"))
            if path.is_file() and path.suffix in {".onnx", ".pt", ".pth"}
        }
    provenance = {
        "status": "MACHINE_CANDIDATE_FILTER_ONLY",
        "human_and_device_review_required": True,
        "whisper_model": "tiny.en", "whisper_compute_type": "int8",
        "secondary_whisper_model": args.secondary_whisper_model,
        "minimum_selection_score": MIN_SELECTION_SCORE,
        "minimum_short_selection_score": MIN_SHORT_SELECTION_SCORE,
        "short_selection_max_words": 2,
        "asr_word_equivalents": ASR_WORD_EQUIVALENTS,
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("faster-whisper", "librosa", "numpy", "speechmos")
        },
        "speechmos_model_artifact_sha256": speechmos_hashes,
        "python": sys.version, "platform": platform.platform(),
        "ffmpeg": subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, check=True,
        ).stdout.splitlines()[0],
        "selector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "candidate_manifest_sha256": {
            path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(args.candidates.glob("attempt_*/*manifest.json"))
        },
        "report_sha256": hashlib.sha256(args.report.read_bytes()).hexdigest(),
        "selected_count": selected_count, "retry_count": len(report) - selected_count,
    }
    chosen_rows = [row for row in report if row["status"] == "SELECTED"]
    identity_cohorts: dict[str, object] = {}
    for character in sorted({str(row["character"]) for row in chosen_rows}):
        character_rows = [row for row in chosen_rows if row["character"] == character]
        f0_values = np.array([
            float(row["chosen"]["f0_median_hz"]) for row in character_rows
            if row["chosen"].get("f0_median_hz") is not None
        ])
        identity_cohorts[character] = {
            "speaker_preset": EXPECTED_SPEAKERS[character],
            "selected_lines": len(character_rows),
            "f0_median_hz": round(float(np.median(f0_values)), 3) if f0_values.size else None,
            "f0_iqr_hz": round(float(np.percentile(f0_values, 75) - np.percentile(f0_values, 25)), 3)
            if f0_values.size else None,
            "selection_score_mean": round(float(np.mean([
                row["chosen"]["selection_score"] for row in character_rows
            ])), 4),
            "mfcc_centroid": np.mean(np.array([
                row["chosen"]["mfcc_mean"] for row in character_rows
            ]), axis=0).round(5).tolist(),
        }
    provenance["identity_cohorts"] = identity_cohorts
    provenance["speaker_presets_unique"] = len(set(EXPECTED_SPEAKERS.values())) == len(EXPECTED_SPEAKERS)
    args.provenance.write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"FILLER_SELECT|SUMMARY|selected={selected_count}|retry={len(report) - selected_count}")
    return 0 if selected_count == len(report) else 2


if __name__ == "__main__":
    raise SystemExit(main())
