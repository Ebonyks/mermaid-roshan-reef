"""Two owner-authorized neutral Guide review candidates; no runtime mutation.

Based on the approved repository Kokoro workflow. Run once: destinations and
journal must not already exist. Exactly one ONNX inference per declared cue.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import onnxruntime as ort
import soundfile as sf
from kokoro_onnx.tokenizer import Tokenizer


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "candidates"
MODEL = ROOT / "tools/kokoro/model.onnx"
VOICES = ROOT / "tools/kokoro/voices.bin"
EXPECTED_MODEL = "8fbea51ea711f2af382e88c833d9e288c6dc82ce5e98421ea61c058ce21a34cb"
EXPECTED_VOICES = "b58979d4eb5b1fdbe783c93f9f43c21217cb8f07af9d3860547371a5b2c8b646"
CUES = (
    ("guide_seek_tap_wiggly_tree", "Tap the wiggly tree!"),
    ("guide_dolls_catch_three", "Move left and right. Catch three sleepy dolls!"),
)
SR = 24000


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, capture_output=True)


def measure(path: Path) -> tuple[dict, list[str]]:
    command = [FFMPEG, "-hide_banner", "-nostats", "-i", str(path),
               "-af", "loudnorm=I=-16:TP=-2:LRA=7:print_format=json", "-f", "null", "-"]
    output = run(command).stderr.decode("utf-8", "replace")
    start = output.rfind("{")
    if start < 0:
        raise RuntimeError("No loudness measurement JSON for " + path.name)
    return json.JSONDecoder().raw_decode(output[start:])[0], command


def stats(audio: np.ndarray) -> dict:
    return {"finite": bool(np.isfinite(audio).all()), "samples": int(audio.size),
            "sample_peak": float(np.max(np.abs(audio))), "dc_mean": float(audio.mean()),
            "duration_seconds": float(audio.size / SR)}


FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
if not FFMPEG or not FFPROBE:
    raise RuntimeError("Approved ffmpeg/ffprobe runtime unavailable")
RESUME = sys.argv[1:] == ["--resume-measurement"]
if sys.argv[1:] and not RESUME:
    raise RuntimeError("Unknown command arguments")
if OUT.exists() and not RESUME:
    raise RuntimeError("No-overwrite guard: candidates directory already exists")
if digest(MODEL) != EXPECTED_MODEL or digest(VOICES) != EXPECTED_VOICES:
    raise RuntimeError("Approved local model hashes changed")
if not RESUME:
    OUT.mkdir(parents=True)
    for child in ("native", "derived", "review"):
        (OUT / child).mkdir()
snapshot = OUT / ("generate_candidates_resume_source.py" if RESUME else "generate_candidates_source.py")
if snapshot.exists():
    raise RuntimeError("No-overwrite guard: source snapshot exists")
shutil.copyfile(__file__, snapshot)
if not RESUME:
    (OUT / "LICENSE_PROVENANCE.txt").write_text(
    "Owner-authorized neutral synthetic Guide review cues, 2026-10-14.\n"
    "Project-authored instructional text. No family reference audio, clone, or impersonation.\n"
    "Existing approved repository Kokoro workflow; exact model/voices hashes in manifest.\n"
    "Upstream ONNX model card declares Apache-2.0, verified 2026-10-14:\n"
    "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX\n"
    "Local runtime and model binaries are not redistributed with the game.\n"
    "Generation and technical measurements grant no human, device, child, or owner acceptance.\n",
        encoding="utf-8")
manifest_path = OUT / "generation_manifest.json"
if RESUME:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["synthesis_calls"] != 1 or len(manifest["attempts"]) != 1:
        raise RuntimeError("Resume requires exactly one existing native take")
    if (OUT / "native" / (CUES[1][0] + ".wav")).exists() or any((OUT / "review").iterdir()):
        raise RuntimeError("Resume state differs from documented parser failure")
    manifest["preserved_postprocess_failures"] = [{
        "status": manifest["status"], "failure": manifest.get("failure"),
        "finished_utc": manifest.get("finished_utc"), "wall_seconds": manifest.get("wall_seconds"),
        "synthesis_calls_at_failure": manifest["synthesis_calls"],
        "repair": "Parse bounded loudnorm JSON with raw_decode; reuse existing native take without re-synthesis",
    }]
    manifest["resume_source_sha256"] = digest(snapshot)
    manifest["resumed_utc"] = stamp()
    manifest["status"] = "RESUMING_MEASUREMENT_WITH_NATIVE_REUSE"
    manifest["acceptance"]["machine"] = "PENDING"
else:
    manifest = {
    "schema": "reef.objective-guide-candidates.v1", "status": "GENERATING",
    "started_utc": stamp(), "owner_authorization_date": "2026-10-14",
    "owner_scope": "Two bounded neutral Guide cues; no cloning, protected-voice mutation or paid API",
    "identity": "Neutral adult synthetic Guide; af_heart, unpitched, speed 1.0",
    "model_reference": "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX",
    "model_license": "Apache-2.0 (upstream ONNX model card)",
    "model_source": "tools/kokoro/model.onnx", "model_sha256": EXPECTED_MODEL,
    "voices_source": "tools/kokoro/voices.bin", "voices_sha256": EXPECTED_VOICES,
    "generator_source_sha256": digest(OUT / "generate_candidates_source.py"),
    "runtime_versions": {p: importlib.metadata.version(p) for p in (
        "kokoro-onnx", "onnxruntime", "soundfile", "numpy")},
    "ffmpeg_version": run([FFMPEG, "-version"]).stdout.decode().splitlines()[0],
    "ffprobe_version": run([FFPROBE, "-version"]).stdout.decode().splitlines()[0],
    "onnx": {"provider": "CPUExecutionProvider", "intra_op_threads": 2,
             "inter_op_threads": 1, "execution_mode": "ORT_SEQUENTIAL"},
    "paid_api_calls": 0, "synthesis_calls": 0, "attempts": [],
    "protected_original_changes": 0,
    "acceptance": {"machine": "PENDING", "human_listening": "NOT_MEASURED",
                   "device": "NOT_MEASURED", "child": "NOT_MEASURED", "owner": "NOT_MEASURED"},
    }
save_json(manifest_path, manifest)
options = ort.SessionOptions()
options.intra_op_num_threads = 2
options.inter_op_num_threads = 1
options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
session = ort.InferenceSession(str(MODEL), sess_options=options, providers=["CPUExecutionProvider"])
voices = np.load(VOICES)
tokenizer = Tokenizer()
started = time.perf_counter()
try:
    for key, text in CUES:
        native = OUT / "native" / (key + ".wav")
        if RESUME and key == CUES[0][0]:
            record = manifest["attempts"][0]
            if digest(native) != record["native"]["sha256"]:
                raise RuntimeError("Preserved first native take hash changed")
            audio, native_sr = sf.read(native, dtype="float32")
            if native_sr != SR:
                raise RuntimeError("Preserved first native sample rate changed")
            record["native_reused_after_measurement_parser_repair"] = True
        else:
            phonemes = tokenizer.phonemize(text, lang="en-us")
            ids = tokenizer.tokenize(phonemes)
            if len(ids) > 500:
                raise RuntimeError("Unexpected long cue tokens")
            record = {"key": key, "text": text, "voice": "af_heart", "speed": 1.0,
                      "pitch_change": False, "language": "en-us", "phonemes": phonemes,
                      "token_count": len(ids), "status": "INFERENCE_STARTED", "started_utc": stamp()}
            manifest["synthesis_calls"] += 1
            manifest["attempts"].append(record)
            save_json(manifest_path, manifest)
            inference_start = time.perf_counter()
            audio = session.run(None, {
                "input_ids": np.array([[0, *ids, 0]], dtype=np.int64),
                "style": voices["af_heart"][len(ids)],
                "speed": np.full(1, 1.0, dtype=np.float32),
            })[0].reshape(-1)
            record["inference_seconds"] = round(time.perf_counter() - inference_start, 6)
        record["native_stats"] = stats(audio)
        if not np.isfinite(audio).all() or audio.size == 0 or np.max(np.abs(audio)) >= 1.0:
            raise RuntimeError("Native samples are nonfinite, empty or clipped")
        if not native.exists():
            sf.write(native, audio, SR, subtype="FLOAT")
        # Preserve native model samples exactly; trimming applies only to a derivative.
        nonquiet = np.flatnonzero(np.abs(audio) > 10 ** (-60 / 20))
        if not nonquiet.size:
            raise RuntimeError("Generated cue has no nonquiet speech")
        first = max(0, int(nonquiet[0]) - int(0.04 * SR))
        last = min(audio.size, int(nonquiet[-1]) + 1 + int(0.10 * SR))
        derived = OUT / "derived" / (key + "_trim.wav")
        if not derived.exists():
            sf.write(derived, audio[first:last], SR, subtype="FLOAT")
        record["native"] = {"path": native.relative_to(OUT).as_posix(), "sha256": digest(native),
                            "sample_rate_hz": SR, "format": "WAV float32 mono; unmodified model samples"}
        record["native_to_review"] = {
            "trim_threshold_dbfs": -60, "retained_native_sample_range": [first, last],
            "leading_pad_seconds": 0.04, "trailing_pad_seconds": 0.10,
            "derivative_path": derived.relative_to(OUT).as_posix(), "derivative_sha256": digest(derived),
            "resample_to_hz": 48000, "pitch_change": False, "retiming": False,
            "loudness_target_lufs": -16, "true_peak_target_dbtp": -2,
        }
        measured, first_command = measure(derived)
        record["loudnorm_first_pass"] = measured
        record["loudnorm_first_command"] = first_command
        filt = ("loudnorm=I=-16:TP=-2:LRA=7:measured_I=" + measured["input_i"]
                + ":measured_TP=" + measured["input_tp"]
                + ":measured_LRA=" + measured["input_lra"]
                + ":measured_thresh=" + measured["input_thresh"]
                + ":offset=" + measured["target_offset"] + ":linear=true:print_format=json")
        export = OUT / "review" / (key + ".ogg")
        encode = [FFMPEG, "-hide_banner", "-nostats", "-n", "-i", str(derived),
                  "-af", filt, "-ar", "48000", "-ac", "1", "-c:a", "libvorbis", "-b:a", "96k", str(export)]
        run(encode)
        post, post_command = measure(export)
        probe_command = [FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(export)]
        probe = json.loads(run(probe_command).stdout)
        stream = probe["streams"][0]
        decoded = np.frombuffer(run([FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(export),
                                     "-f", "f32le", "-acodec", "pcm_f32le", "-"]).stdout, dtype="<f4")
        lufs = float(post["input_i"])
        peak = float(post["input_tp"])
        verification = {
            "codec": stream["codec_name"], "sample_rate_hz": int(stream["sample_rate"]),
            "channels": int(stream["channels"]), "bitrate_kbps": int(stream.get("bit_rate", 0)) / 1000,
            "duration_seconds": float(stream.get("duration", probe["format"]["duration"])),
            "integrated_lufs": lufs, "true_peak_dbtp": peak,
            "decoded_finite": bool(np.isfinite(decoded).all()),
            "decoded_sample_peak": float(np.max(np.abs(decoded))), "decoded_dc_mean": float(decoded.mean()),
        }
        passed = (verification["codec"] == "vorbis" and verification["sample_rate_hz"] == 48000
                  and verification["channels"] == 1 and verification["bitrate_kbps"] >= 64
                  and verification["decoded_finite"] and verification["decoded_sample_peak"] < 1.0
                  and abs(verification["decoded_dc_mean"]) < 0.001 and math.isfinite(lufs)
                  and abs(lufs + 16) <= 1 and math.isfinite(peak) and peak <= -1.5)
        record["review"] = {"path": export.relative_to(OUT).as_posix(), "sha256": digest(export),
                            "bytes": export.stat().st_size, "verification": verification,
                            "encoding_command": encode, "measurement_command": post_command,
                            "ffprobe_command": probe_command, "machine_pass": passed}
        record["status"] = "CANDIDATE_MACHINE_PASS" if passed else "CANDIDATE_MACHINE_FAIL"
        record["finished_utc"] = stamp()
        save_json(manifest_path, manifest)
        print(json.dumps({"key": key, "status": record["status"], **verification}), flush=True)
        if not passed:
            raise RuntimeError("Candidate technical delivery check failed: " + key)
    manifest["status"] = "CANDIDATE_MACHINE_PASS"
    manifest["acceptance"]["machine"] = "PASS"
except Exception as error:
    manifest["status"] = "GENERATION_OR_EXPORT_FAILED"
    manifest["failure"] = type(error).__name__ + ": " + str(error)
    manifest["acceptance"]["machine"] = "FAIL"
    raise
finally:
    manifest["finished_utc"] = stamp()
    manifest["wall_seconds"] = round(time.perf_counter() - started, 6)
    save_json(manifest_path, manifest)
print(json.dumps({"status": manifest["status"], "synthesis_calls": manifest["synthesis_calls"],
                  "manifest": str(manifest_path), "manifest_sha256": digest(manifest_path)}), flush=True)
