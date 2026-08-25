#!/usr/bin/env python3
"""Build the small, project-original audio-quality replacement set."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import struct
import subprocess
import tempfile
import wave
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decoded_pcm_sha256(path: Path) -> str:
    result = subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
        "-f", "s16le", "-ar", "48000", "-ac", "1", "-",
    ], capture_output=True, check=True)
    return hashlib.sha256(result.stdout).hexdigest()


def synthesize_ui_tap(spec: dict[str, object], wav_path: Path) -> None:
    rate = int(spec["sample_rate_hz"])
    duration = float(spec["duration_seconds"])
    count = round(rate * duration)
    rng = random.Random(int(spec["seed"]))
    phase = 0.0
    samples: list[int] = []
    for index in range(count):
        t = index / rate
        progress = index / max(1, count - 1)
        frequency = float(spec["fundamental_start_hz"]) * (
            float(spec["fundamental_end_hz"]) / float(spec["fundamental_start_hz"])
        ) ** progress
        phase += 2.0 * math.pi * frequency / rate
        attack = min(1.0, t / 0.003)
        release = min(1.0, max(0.0, (duration - t) / 0.018))
        envelope = attack * release * math.exp(-float(spec["decay_per_second"]) * t)
        bubble = math.sin(phase) + 0.22 * math.sin(phase * 2.01 + 0.4)
        shell_tick = (rng.random() * 2.0 - 1.0) * math.exp(-85.0 * t) * 0.16
        value = math.tanh((bubble * 0.36 + shell_tick) * envelope)
        value = max(-float(spec["peak_ceiling"]), min(float(spec["peak_ceiling"]), value))
        samples.append(round(value * 32767.0))
    with wave.open(str(wav_path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(rate)
        stream.writeframes(b"".join(struct.pack("<h", sample) for sample in samples))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    spec_path = root / "assets_src/audio/quality_replacements_2026-08-24/ui_tap.json"
    output = root / "assets/audio/ui_tap.ogg"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="reef_audio_quality_") as temp_dir:
        wav_path = Path(temp_dir) / "ui_tap.wav"
        ogg_path = Path(temp_dir) / "ui_tap.ogg"
        synthesize_ui_tap(spec, wav_path)
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(wav_path), "-c:a", "libvorbis", "-q:a", "5",
            "-ar", "48000", "-ac", "1", str(ogg_path),
        ], check=True)
        if args.check:
            # Ogg stream serials are container metadata and need not be stable.
            # The decoded production samples are the deterministic contract.
            ok = output.is_file() and decoded_pcm_sha256(output) == decoded_pcm_sha256(ogg_path)
            print(f"AUDIO_REPLACEMENTS|ui_tap|{'PASS' if ok else 'STALE'}")
            return 0 if ok else 1
        output.write_bytes(ogg_path.read_bytes())
    print(
        f"AUDIO_REPLACEMENTS|ui_tap|container={sha256(output)}|"
        f"pcm={decoded_pcm_sha256(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
