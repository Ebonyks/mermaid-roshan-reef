"""Build Grand Puff's short cartoon sneeze; no recordings or samples."""
from __future__ import annotations

import argparse
import array
import math
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RATE = 48_000


def envelope(t: float, start: float, length: float, decay: float = 1.8) -> float:
    u = (t - start) / length
    if not 0.0 < u < 1.0:
        return 0.0
    return math.sin(math.pi * u) ** 0.66 * math.exp(-decay * u)


def render() -> bytes:
    duration = 0.44
    rng = random.Random(349)
    air, chest, edge, phase = 0.0, 0.0, 0.0, 0.0
    samples = []
    for i in range(round(RATE * duration)):
        t = i / RATE
        noise = rng.uniform(-1.0, 1.0)
        air += 0.27 * (noise - air)
        chest += 0.045 * (noise - chest)
        edge += 0.53 * (noise - edge)
        phase += math.tau * (155.0 + 124.0 * math.exp(-t * 11.0) - 94.0 * t) / RATE
        voiced = (math.sin(phase) + 0.38 * math.sin(phase * 2)
                  + 0.22 * math.sin(phase * 3) + 0.12 * math.sin(phase * 5))
        intake = envelope(t, 0.0, 0.071)
        consonant = envelope(t, 0.047, 0.138, 2.4)
        release = envelope(t, 0.102, 0.282, 2.1)
        value = 0.19 * intake * voiced
        value += consonant * (0.85 * (edge - chest) + 0.31 * (noise - edge))
        value += release * (0.33 * voiced + 0.44 * (air - chest))
        samples.append(value)
    gain = 10 ** (-6.0 / 20.0) / max(abs(value) for value in samples)
    pcm = array.array("h", (round(32767 * gain * value) for value in samples))
    # PCM input format is explicitly little-endian.
    if __import__("sys").byteorder != "little":
        pcm.byteswap()
    return pcm.tobytes()


def build(folder: Path) -> None:
    path = folder / "grand_puff_sneeze.ogg"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-i", "pipe:0",
        "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact",
        "-c:a", "libvorbis", "-q:a", "4", str(path),
    ], input=render(), check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    dest = ROOT / "assets/audio/sfx"
    if args.check:
        with tempfile.TemporaryDirectory() as name:
            candidate = Path(name)
            build(candidate)
            if any(path.read_bytes() != (dest / path.name).read_bytes()
                   for path in candidate.iterdir()):
                print("Grand Puff cold SFX: encoded byte mismatch")
                return 1
    else:
        build(dest)
    print("Grand Puff cold SFX: sneeze OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
