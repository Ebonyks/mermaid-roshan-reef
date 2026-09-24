#!/usr/bin/env python3
"""Original nonverbal crowd/crockery bed over the existing pearl-hall ambience.

No speech, family recordings, samples from outside the project or network calls.
The seeded formant murmurs are an indistinct storybook crowd, not named people.
Run from the project root; outputs and measurements are provenance-backed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

import numpy as np
from scipy.io import wavfile
import build_area_music as music

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/audio/ambience_hall.ogg"
OUTPUT = ROOT / "assets/audio/ambience_opera_foyer.ogg"
MANIFEST = ROOT / "assets_src/audio/music/opera_foyer_ambience_manifest.json"
RATE = 48000
SECONDS = 32


def render(ffmpeg: Path) -> np.ndarray:
    rng = np.random.default_rng(20260906)
    count = RATE * SECONDS
    room = music._decode_pcm(ffmpeg, SOURCE)
    # Preserve the source file and reuse its quiet interior tone underneath.
    room = np.tile(room, (int(np.ceil(count / len(room))), 1))[:count]
    room = room / max(float(np.sqrt(np.mean(room * room))), 1e-9)
    track = room * 0.006
    for guest in range(14):
        pan = float(rng.uniform(-0.8, 0.8))
        base = float(rng.uniform(110, 240))
        for phrase in range(9):
            duration = float(rng.uniform(0.6, 1.7))
            t = np.arange(round(duration * RATE)) / RATE
            pitch = base * (1 + 0.035 * np.sin(2 * np.pi * t / duration))
            phase = 2 * np.pi * np.cumsum(pitch) / RATE
            vowel = float(rng.uniform(420, 760))
            signal = np.zeros_like(t)
            for harmonic in range(1, 16):
                frequency = base * harmonic
                gain = (np.exp(-((frequency - vowel) / 210) ** 2)
                        + 0.3 * np.exp(-((frequency - 1300) / 320) ** 2)) / harmonic
                signal += gain * np.sin(phase * harmonic)
            # Overlapping, irregular syllable-shaped envelopes, no phonemes/words.
            envelope = np.sin(np.pi * t / duration) ** 2
            envelope *= 0.25 + 0.75 * np.sin(np.pi * t * rng.uniform(2, 4)) ** 2
            signal *= envelope
            signal /= max(float(np.max(np.abs(signal))), 1e-9)
            music._add_circular(track, int(rng.integers(count)), signal,
                                float(rng.uniform(0.003, 0.008)), pan)
    # Intermittent cup-and-saucer taps put the activity at the refreshment carts.
    for tap in range(18):
        t = np.arange(int(RATE * 0.32)) / RATE
        frequency = float(rng.uniform(1350, 2150))
        signal = sum(gain * np.sin(2 * np.pi * frequency * ratio * t)
                     for ratio, gain in [(1, 1), (1.53, 0.3), (2.17, 0.12)])
        signal *= np.minimum(t / 0.003, 1) * np.exp(-t * 22)
        music._add_circular(track, int(rng.integers(count)), signal,
                            float(rng.uniform(0.002, 0.004)), float(rng.uniform(-0.8, 0.8)))
    dry = track.copy()
    track += np.roll(dry, int(0.18 * RATE), axis=0)[:, ::-1] * 0.24
    track += np.roll(dry, int(0.31 * RATE), axis=0) * 0.12
    # Ease out the tiny endpoint difference in the reused room bed so the
    # audio loop joins continuously without a click.
    n = RATE // 4
    blend = np.linspace(0, 1, n)[:, None]
    track[:n] += (track[-1] - track[0]) * (1 - blend) ** 2
    track -= np.mean(track, axis=0)
    return track


def main() -> None:
    ffmpeg = music._find_ffmpeg(None, ROOT)
    track = render(ffmpeg)
    with tempfile.TemporaryDirectory(prefix="reef-opera-crowd-") as temp:
        wav = Path(temp) / "crowd.wav"
        wavfile.write(wav, RATE, track.astype(np.float32))
        subprocess.run([str(ffmpeg), "-v", "error", "-y", "-i", str(wav),
                        "-af", "loudnorm=I=-27:TP=-9:LRA=7", "-ar", str(RATE),
                        "-c:a", "libvorbis", "-b:a", "96k", "-minrate", "80k",
                        "-metadata", "LOOPSTART=0", "-metadata", f"LOOPEND={len(track)}",
                        "-metadata", f"LOOPLENGTH={len(track)}", str(OUTPUT)], check=True)
    music._canonicalize_ogg(OUTPUT, music._serial_for("opera_foyer_ambience"))
    decoded = music._decode_pcm(ffmpeg, OUTPUT)
    metrics = music._measure_loudness(ffmpeg, OUTPUT)
    delivery = music._probe_ogg(music._find_ffprobe(ffmpeg), OUTPUT)
    assert metrics["true_peak_dbtp"] < -9.0, metrics
    assert music._seam_metrics(decoded)["jump_ratio"] < 4.0
    assert delivery["average_bitrate_bps"] >= 64000
    assert delivery["tags"]["LOOPEND"] == str(len(track))
    source = "res://assets/audio/ambience_opera_foyer.ogg"
    digest = hashlib.md5(source.encode()).hexdigest()
    imported = f"res://.godot/imported/ambience_opera_foyer.ogg-{digest}.oggvorbisstr"
    import_path = OUTPUT.with_name(OUTPUT.name + ".import")
    uid = ""
    if import_path.exists():
        match = re.search(r'^uid="[^"]+"$', import_path.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            uid = match.group(0) + "\n"
    import_path.write_text(
        '[remap]\n\nimporter="oggvorbisstr"\ntype="AudioStreamOggVorbis"\n'
        f'{uid}path="{imported}"\n\n[deps]\n\nsource_file="{source}"\n'
        f'dest_files=["{imported}"]\n\n[params]\n\nloop=true\n'
        'loop_offset=0.0\nbpm=0.0\nbeat_count=0\nbar_beats=4\n', encoding="utf-8")
    manifest = {
        "description": "Popular opera foyer: diffuse nonverbal crowd and occasional crockery, existing hall tone reused",
        "source": SOURCE.relative_to(ROOT).as_posix(), "source_sha256": music._sha256(SOURCE),
        "output": OUTPUT.relative_to(ROOT).as_posix(), "sha256": music._sha256(OUTPUT),
        "generator": Path(__file__).resolve().relative_to(ROOT).as_posix(),
        "generator_sha256": music._text_sha256(Path(__file__)), "seed": 20260906,
        "license": "Project-owned deterministic synthesis and existing project hall ambience; no external media",
        "duration_seconds": len(decoded) / RATE, "sample_rate": RATE, "channels": 2,
        "loudness": metrics, "loop": music._seam_metrics(decoded),
        "delivery": delivery,
        "listening_review": "Pending owner audition; technical measurements are not a listening approval",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("OPERA FOYER AMBIENCE BUILT", metrics)


if __name__ == "__main__":
    main()
