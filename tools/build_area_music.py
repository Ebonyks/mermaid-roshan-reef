#!/usr/bin/env python3
"""Build deterministic, project-owned music for quiet game areas.

The score catalog is declarative and human-readable.  This renderer uses only
mathematical oscillators and seeded noise: no samples, soundfonts, protected
recordings, downloaded media, MIDI synthesizer, or network service is read.

Outputs are 48 kHz stereo Ogg Vorbis loops with hash-backed provenance,
explicit sample loop tags, Godot loop import settings, and a minimum managed
Vorbis rate that satisfies the project's 64 kbps music floor even for sparse
arrangements.

Usage from the repository root:
    python tools/build_area_music.py --catalog-check
    python tools/build_area_music.py
    python tools/build_area_music.py --cue opera_detective
    python tools/build_area_music.py --check
    python tools/build_area_music.py --ffmpeg C:/path/to/ffmpeg.exe
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from typing import Any

import numpy as np
import scipy
from scipy.io import wavfile


SAMPLE_RATE = 48_000
CHANNELS = 2
TARGET_LUFS = -18.0
PEAK_CEILING_DBTP = -3.0
PCM_PEAK_TARGET_DBFS = -3.4
VORBIS_TARGET = "96k"
VORBIS_MINIMUM = "80k"
VORBIS_MAXIMUM = "128k"
MINIMUM_MEASURED_BITRATE = 64_000
MINIMUM_LOOP_SECONDS = 24.0
MAXIMUM_LOOP_SECONDS = 40.0
GENERATOR_VERSION = 2
SCORES_PATH = Path("assets_src/audio/music/area_music_scores.json")
OUTPUT_DIR = Path("assets/audio/music")
MANIFEST_NAME = "area_music_manifest.json"
MANIFEST_SCHEMA = "reef.area-music-manifest.v1"
SCORE_SCHEMA = "reef.area-music-scores.v1"

EXPECTED_IDS = (
    "castle_opera_hall",
    "castle_kitchen",
    "castle_library",
    "castle_playroom",
    "castle_craft_room",
    "castle_mermaid_pool",
    "castle_bubble_bath",
    "castle_dining_room",
    "castle_royal_bedroom",
    "castle_sleepover_bedroom",
    "castle_movie_lounge",
    "castle_family_gallery",
    "opera_lobby",
    "opera_chef",
    "opera_detective",
    "opera_ballerina",
    "opera_candymaker",
    "opera_doctor",
    "opera_farmer",
    "opera_boxer",
    "opera_magician",
    "opera_painter",
    "opera_astronaut",
    "opera_racer",
    "opera_popstar",
    "opera_nursery",
    "opera_boss_dragon",
    "opera_boss_phantom",
    "opera_boss_maestro",
    "northern",
    "galaxy",
    "ember",
    "dungeon_ice",
    "dungeon_ember",
    "combat_ice",
    "combat_fire",
    "combat_tutorial",
    "stuffie_battle",
    "dustboss",
    "picture_snowman",
    "picture_garden",
    "picture_trampoline",
    "picture_xmas",
)

SCALES: dict[str, tuple[int, ...]] = {
    "major": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
}

# Partials are deliberately modest and band-limited at render time.  The
# profiles describe a shared storybook toy orchestra rather than attempting
# to imitate recorded instruments or a General MIDI soundfont.
INSTRUMENTS: dict[str, dict[str, Any]] = {
    "piano": {
        "partials": ((1.0, 1.0), (2.0, 0.34), (3.0, 0.16), (4.0, 0.07)),
        "attack": 0.006, "release": 0.16, "decay": 1.5, "vibrato": 0.0,
    },
    "toy_piano": {
        "partials": ((1.0, 1.0), (2.02, 0.48), (3.98, 0.18), (6.1, 0.06)),
        "attack": 0.003, "release": 0.10, "decay": 3.6, "vibrato": 0.0,
    },
    "music_box": {
        "partials": ((1.0, 1.0), (2.01, 0.38), (3.91, 0.22), (6.03, 0.08)),
        "attack": 0.002, "release": 0.18, "decay": 3.0, "vibrato": 0.0,
    },
    "celesta": {
        "partials": ((1.0, 1.0), (2.0, 0.30), (3.01, 0.16), (5.05, 0.08)),
        "attack": 0.004, "release": 0.20, "decay": 2.3, "vibrato": 0.0,
    },
    "marimba": {
        "partials": ((1.0, 1.0), (3.98, 0.20), (9.9, 0.035)),
        "attack": 0.004, "release": 0.11, "decay": 4.2, "vibrato": 0.0,
    },
    "pizzicato": {
        "partials": ((1.0, 1.0), (2.0, 0.42), (3.0, 0.22), (4.0, 0.10)),
        "attack": 0.003, "release": 0.09, "decay": 5.0, "vibrato": 0.0,
    },
    "banjo": {
        "partials": ((1.0, 1.0), (2.0, 0.66), (3.0, 0.44), (4.0, 0.27), (5.0, 0.13)),
        "attack": 0.002, "release": 0.07, "decay": 6.2, "vibrato": 0.0,
    },
    "ukulele": {
        "partials": ((1.0, 1.0), (2.0, 0.40), (3.0, 0.17), (4.0, 0.07)),
        "attack": 0.003, "release": 0.10, "decay": 4.0, "vibrato": 0.0,
    },
    "harp": {
        "partials": ((1.0, 1.0), (2.0, 0.34), (3.0, 0.15), (4.0, 0.07), (5.0, 0.035)),
        "attack": 0.004, "release": 0.20, "decay": 2.1, "vibrato": 0.0,
    },
    "clarinet": {
        "partials": ((1.0, 1.0), (3.0, 0.28), (5.0, 0.10), (7.0, 0.035)),
        "attack": 0.035, "release": 0.14, "decay": 0.12, "vibrato": 0.0035, "noise": 0.008,
    },
    "flute": {
        "partials": ((1.0, 1.0), (2.0, 0.10), (3.0, 0.025)),
        "attack": 0.055, "release": 0.17, "decay": 0.08, "vibrato": 0.0045, "noise": 0.012,
    },
    "warm_strings": {
        "partials": ((1.0, 1.0), (2.0, 0.34), (3.0, 0.20), (4.0, 0.12), (5.0, 0.07), (6.0, 0.04)),
        "attack": 0.10, "release": 0.24, "decay": 0.03, "vibrato": 0.0035,
    },
    "fiddle": {
        "partials": ((1.0, 1.0), (2.0, 0.42), (3.0, 0.26), (4.0, 0.14), (5.0, 0.07)),
        "attack": 0.035, "release": 0.14, "decay": 0.10, "vibrato": 0.005,
    },
    "warm_brass": {
        "partials": ((1.0, 1.0), (2.0, 0.42), (3.0, 0.18), (4.0, 0.07)),
        "attack": 0.030, "release": 0.15, "decay": 0.14, "vibrato": 0.0015,
    },
    "accordion": {
        "partials": ((1.0, 1.0), (2.0, 0.24), (3.0, 0.31), (4.0, 0.08), (5.0, 0.10)),
        "attack": 0.025, "release": 0.12, "decay": 0.16, "vibrato": 0.003,
    },
    "warm_pad": {
        "partials": ((1.0, 1.0), (2.0, 0.18), (3.0, 0.08), (4.0, 0.035)),
        "attack": 0.18, "release": 0.30, "decay": 0.015, "vibrato": 0.002,
    },
    "soft_synth": {
        "partials": ((1.0, 1.0), (2.0, 0.24), (3.0, 0.14), (5.0, 0.055)),
        "attack": 0.018, "release": 0.12, "decay": 0.24, "vibrato": 0.0025,
    },
    "warm_bass": {
        "partials": ((1.0, 1.0), (2.0, 0.18), (3.0, 0.06)),
        "attack": 0.016, "release": 0.12, "decay": 0.30, "vibrato": 0.0,
    },
    "synth_bass": {
        "partials": ((1.0, 1.0), (2.0, 0.28), (3.0, 0.10), (4.0, 0.04)),
        "attack": 0.009, "release": 0.09, "decay": 0.65, "vibrato": 0.0,
    },
    "bell": {
        "partials": ((1.0, 1.0), (2.01, 0.34), (2.72, 0.18), (4.08, 0.10), (5.4, 0.045)),
        "attack": 0.002, "release": 0.20, "decay": 3.5, "vibrato": 0.0,
    },
    "chime": {
        "partials": ((1.0, 1.0), (2.76, 0.28), (4.14, 0.12), (5.43, 0.06)),
        "attack": 0.002, "release": 0.25, "decay": 2.7, "vibrato": 0.0,
    },
}

VALID_TEXTURES = {
    "aquatic", "bluegrass", "boss", "bounce", "cinematic", "combat",
    "drive", "flowing", "folk", "gentle", "lullaby", "march", "polka",
    "pop", "space", "swing", "theatre", "tiptoe", "waltz",
}
VALID_PERCUSSION = {
    "none", "bluegrass", "brush", "bubble", "pop", "pulse", "shaker",
    "sleigh", "soft_combat", "soft_march", "tiptoe", "tutorial_brush",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _cue_score_sha256(cue: dict[str, Any]) -> str:
    canonical = json.dumps(cue, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _seed_for(*parts: object) -> int:
    text = ":".join(str(part) for part in parts)
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "little")


def _serial_for(slug: str) -> int:
    return _seed_for("reef-area-music", slug) & 0x7FFFFFFF


def _find_ffmpeg(explicit: str | None, repo_root: Path) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("REEF_FFMPEG"):
        candidates.append(Path(os.environ["REEF_FFMPEG"]))
    candidates.extend(sorted((repo_root / ".video-tools").glob("ffmpeg-*/bin/ffmpeg.exe")))
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.extend(
            sorted(
                Path(local_app_data).glob("Programs/MermaidReefTools/FFmpeg/*/bin/ffmpeg.exe"),
                reverse=True,
            )
        )
    # Prefer the repository/managed runtime over an unrelated PATH install so
    # an ordinary build remains byte-reproducible on the owner's machine.
    command = shutil.which("ffmpeg")
    if command:
        candidates.append(Path(command))
    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if resolved.is_file():
            return resolved
    raise FileNotFoundError(
        "FFmpeg was not found. Pass --ffmpeg or set REEF_FFMPEG to the pinned executable."
    )


def _find_ffprobe(ffmpeg: Path) -> Path:
    sibling = ffmpeg.with_name("ffprobe.exe" if ffmpeg.suffix.lower() == ".exe" else "ffprobe")
    if sibling.is_file():
        return sibling
    command = shutil.which("ffprobe")
    if command:
        return Path(command).resolve()
    raise FileNotFoundError("ffprobe was not found beside FFmpeg or on PATH")


def _tool_version(tool: Path) -> str:
    result = subprocess.run(
        [str(tool), "-hide_banner", "-version"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()[0].strip()


def _load_catalog(repo_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    score_path = repo_root / SCORES_PATH
    data = json.loads(score_path.read_text(encoding="utf-8"))
    if data.get("schema") != SCORE_SCHEMA:
        raise ValueError(f"Unexpected score schema in {score_path}")
    if data.get("bpm_unit") != "notated_denominator":
        raise ValueError("Score BPM must count the notated denominator unit, including eighths in 6/8")
    motif = data.get("roshan_motif", {})
    if motif.get("scale_degrees") != [0, 2, 4, 5, 4, 2]:
        raise ValueError("The score catalog must preserve the approved six-note Roshan contour")
    rhythm_units = motif.get("rhythm_units")
    if not isinstance(rhythm_units, list) or len(rhythm_units) != 6 or sum(rhythm_units) <= 0:
        raise ValueError("The Roshan motif needs six positive rhythm units")
    cues = data.get("cues")
    if not isinstance(cues, list):
        raise ValueError("Score catalog cues must be a list")
    actual_ids = [str(cue.get("id", "")) for cue in cues]
    if actual_ids != list(EXPECTED_IDS):
        missing = sorted(set(EXPECTED_IDS) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(EXPECTED_IDS))
        raise ValueError(
            f"Score IDs/order do not match runtime contract; missing={missing}, extra={extra}"
        )
    for cue in cues:
        _validate_cue(cue)
    for field in ("title", "brief", "motif_treatment"):
        values = [str(cue[field]) for cue in cues]
        if len(set(values)) != len(values):
            raise ValueError(f"Every area cue needs a unique {field}")
    composition_signatures = {
        json.dumps(
            {
                key: cue[key]
                for key in (
                    "bpm", "meter", "bars", "tonic_midi", "mode", "texture",
                    "percussion", "instruments", "progression", "melody",
                )
            },
            sort_keys=True,
        )
        for cue in cues
    }
    if len(composition_signatures) != len(cues):
        raise ValueError("Every area cue needs a unique compositional signature")
    return data, cues


def _validate_cue(cue: dict[str, Any]) -> None:
    slug = str(cue.get("id", ""))
    if not re.fullmatch(r"[a-z0-9_]+", slug):
        raise ValueError(f"Invalid cue ID: {slug!r}")
    for field in ("title", "family", "area", "brief", "motif_treatment"):
        if not isinstance(cue.get(field), str) or not str(cue[field]).strip():
            raise ValueError(f"{slug}: missing human-readable {field}")
    if len(str(cue["brief"]).split()) < 12:
        raise ValueError(f"{slug}: musical brief is too terse to audit")
    bpm = float(cue.get("bpm", 0.0))
    meter = cue.get("meter")
    bars = int(cue.get("bars", 0))
    if bpm < 50.0 or bpm > 160.0:
        raise ValueError(f"{slug}: BPM out of child-friendly range")
    if not isinstance(meter, list) or len(meter) != 2 or int(meter[0]) < 2 or int(meter[1]) not in (2, 4, 8):
        raise ValueError(f"{slug}: invalid meter")
    if bars < 4:
        raise ValueError(f"{slug}: loop is too short to develop")
    duration = bars * int(meter[0]) * 60.0 / bpm
    if duration < MINIMUM_LOOP_SECONDS - 0.001 or duration > MAXIMUM_LOOP_SECONDS + 0.001:
        raise ValueError(
            f"{slug}: {duration:.2f}s loop is outside {MINIMUM_LOOP_SECONDS:.0f}-{MAXIMUM_LOOP_SECONDS:.0f}s"
        )
    mode = str(cue.get("mode", ""))
    if mode not in SCALES:
        raise ValueError(f"{slug}: unsupported mode {mode!r}")
    if str(cue.get("texture", "")) not in VALID_TEXTURES:
        raise ValueError(f"{slug}: unsupported texture")
    if str(cue.get("percussion", "")) not in VALID_PERCUSSION:
        raise ValueError(f"{slug}: unsupported percussion style")
    instruments = cue.get("instruments")
    if not isinstance(instruments, dict) or set(instruments) != {"lead", "harmony", "bass", "accent"}:
        raise ValueError(f"{slug}: instrumentation must name lead/harmony/bass/accent")
    for role, instrument in instruments.items():
        if instrument not in INSTRUMENTS:
            raise ValueError(f"{slug}: unsupported {role} instrument {instrument!r}")
    progression = cue.get("progression")
    melody = cue.get("melody")
    if not isinstance(progression, list) or len(progression) < 4 or not all(isinstance(x, int) for x in progression):
        raise ValueError(f"{slug}: progression needs at least four integer scale degrees")
    if not isinstance(melody, list) or len(melody) < 8 or not all(x is None or isinstance(x, int) for x in melody):
        raise ValueError(f"{slug}: melody needs at least eight scale-degree/rest events")
    energy = float(cue.get("energy", -1.0))
    if not 0.0 <= energy <= 1.0:
        raise ValueError(f"{slug}: energy must be in [0, 1]")
    adaptive = cue.get("adaptive_markers")
    if adaptive is not None:
        expected = {"prowl_beat", "anticipation_start_beat", "action_beat"}
        if not isinstance(adaptive, dict) or set(adaptive) != expected:
            raise ValueError(
                f"{slug}: adaptive_markers must contain exactly {sorted(expected)}"
            )
        try:
            prowl_beat = float(adaptive["prowl_beat"])
            anticipation_beat = float(adaptive["anticipation_start_beat"])
            action_beat = float(adaptive["action_beat"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{slug}: adaptive marker beats must be numeric") from exc
        total_beats = bars * int(meter[0])
        if not (0.0 <= prowl_beat < anticipation_beat < action_beat < total_beats):
            raise ValueError(f"{slug}: adaptive marker order is invalid")
        if action_beat - anticipation_beat < 4.0:
            raise ValueError(f"{slug}: adaptive anticipation needs at least four beats")


def _midi_frequency(midi_note: int) -> float:
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def _degree_to_midi(tonic: int, mode: str, degree: int, octave: int = 0) -> int:
    scale = SCALES[mode]
    octave_delta, index = divmod(degree, len(scale))
    return tonic + scale[index] + 12 * (octave + octave_delta)


def _note_envelope(count: int, attack_seconds: float, release_seconds: float, decay: float) -> np.ndarray:
    envelope = np.ones(count, dtype=np.float64)
    attack = min(count, max(1, int(round(attack_seconds * SAMPLE_RATE))))
    release = min(count, max(1, int(round(release_seconds * SAMPLE_RATE))))
    if attack:
        phase = np.linspace(0.0, math.pi * 0.5, attack, endpoint=True)
        envelope[:attack] *= np.sin(phase) ** 2
    if release:
        phase = np.linspace(0.0, math.pi * 0.5, release, endpoint=True)
        envelope[-release:] *= np.cos(phase) ** 2
    if decay > 0.0:
        envelope *= np.exp(-decay * np.arange(count, dtype=np.float64) / SAMPLE_RATE)
    return envelope


def _synth_note(instrument: str, midi_note: int, seconds: float, seed: int) -> np.ndarray:
    profile = INSTRUMENTS[instrument]
    count = max(8, int(round(seconds * SAMPLE_RATE)))
    time = np.arange(count, dtype=np.float64) / SAMPLE_RATE
    frequency = _midi_frequency(midi_note)
    vibrato = float(profile.get("vibrato", 0.0))
    if vibrato:
        rate = 5.0 + ((_seed_for(seed, "vibrato") % 17) / 20.0)
        instantaneous = frequency * (1.0 + vibrato * np.sin(2.0 * math.pi * rate * time))
        phase = 2.0 * math.pi * np.cumsum(instantaneous) / SAMPLE_RATE
    else:
        phase = 2.0 * math.pi * frequency * time
    signal = np.zeros(count, dtype=np.float64)
    normalizer = 0.0
    for multiplier, gain in profile["partials"]:
        if frequency * float(multiplier) >= SAMPLE_RATE * 0.46:
            continue
        signal += float(gain) * np.sin(phase * float(multiplier))
        normalizer += abs(float(gain))
    if normalizer:
        signal /= normalizer
    noise_gain = float(profile.get("noise", 0.0))
    if noise_gain:
        rng = np.random.default_rng(seed)
        noise = rng.standard_normal(count)
        noise = (noise + np.roll(noise, 1) + np.roll(noise, 2) + np.roll(noise, 3)) * 0.25
        signal += noise * noise_gain
    envelope = _note_envelope(
        count,
        float(profile["attack"]),
        min(float(profile["release"]), seconds * 0.35),
        float(profile["decay"]),
    )
    return signal * envelope


def _synth_drum(kind: str, velocity: float, seed: int) -> np.ndarray:
    durations = {"kick": 0.22, "brush": 0.16, "shaker": 0.09, "wood": 0.11, "bubble": 0.14, "sleigh": 0.20}
    seconds = durations[kind]
    count = int(round(seconds * SAMPLE_RATE))
    time = np.arange(count, dtype=np.float64) / SAMPLE_RATE
    rng = np.random.default_rng(seed)
    if kind == "kick":
        f0, f1 = 92.0, 48.0
        slope = (f1 - f0) / seconds
        phase = 2.0 * math.pi * (f0 * time + 0.5 * slope * time * time)
        signal = np.sin(phase) * np.exp(-18.0 * time)
    elif kind == "wood":
        signal = (
            np.sin(2.0 * math.pi * 540.0 * time)
            + 0.42 * np.sin(2.0 * math.pi * 870.0 * time)
        ) * np.exp(-38.0 * time)
    elif kind == "bubble":
        f0, f1 = 360.0, 650.0
        slope = (f1 - f0) / seconds
        phase = 2.0 * math.pi * (f0 * time + 0.5 * slope * time * time)
        signal = np.sin(phase) * np.exp(-25.0 * time)
    elif kind == "sleigh":
        noise = rng.standard_normal(count)
        high = noise - np.roll(noise, 1)
        bells = sum(
            0.18 * np.sin(2.0 * math.pi * frequency * time)
            for frequency in (1320.0, 1760.0, 2217.0)
        )
        signal = (0.18 * high + bells) * np.exp(-17.0 * time)
    else:
        noise = rng.standard_normal(count)
        if kind == "brush":
            smooth = (noise + np.roll(noise, 1) + np.roll(noise, 2)) / 3.0
            signal = 0.30 * smooth * np.exp(-18.0 * time)
        else:
            high = noise - np.roll(noise, 1)
            signal = 0.20 * high * np.exp(-42.0 * time)
    envelope = _note_envelope(count, 0.003, min(0.04, seconds * 0.3), 0.0)
    return signal * envelope * velocity


def _add_circular(track: np.ndarray, start_sample: int, mono: np.ndarray, gain: float, pan: float) -> None:
    total = track.shape[0]
    if mono.size == 0 or total == 0:
        return
    angle = (max(-1.0, min(1.0, pan)) + 1.0) * math.pi * 0.25
    stereo = np.column_stack((mono * math.cos(angle), mono * math.sin(angle))) * gain
    source = 0
    destination = start_sample % total
    while source < stereo.shape[0]:
        count = min(total - destination, stereo.shape[0] - source)
        track[destination : destination + count] += stereo[source : source + count]
        source += count
        destination = 0


def _cue_clock(cue: dict[str, Any]) -> tuple[int, float, int, int]:
    beats_per_bar = int(cue["meter"][0])
    bars = int(cue["bars"])
    total_beats = beats_per_bar * bars
    sample_count = int(round(total_beats * 60.0 * SAMPLE_RATE / float(cue["bpm"])))
    samples_per_beat = sample_count / float(total_beats)
    return sample_count, samples_per_beat, beats_per_bar, bars


def _event_sample(beat: float, samples_per_beat: float) -> int:
    return int(round(beat * samples_per_beat))


def _add_note(
    track: np.ndarray,
    cue: dict[str, Any],
    instrument: str,
    degree: int,
    start_beat: float,
    duration_beats: float,
    gain: float,
    pan: float,
    event_id: str,
    octave: int,
    samples_per_beat: float,
) -> None:
    midi_note = _degree_to_midi(int(cue["tonic_midi"]), str(cue["mode"]), degree, octave)
    seconds = max(0.045, duration_beats * samples_per_beat / SAMPLE_RATE)
    mono = _synth_note(instrument, midi_note, seconds, _seed_for(cue["id"], event_id, midi_note))
    _add_circular(track, _event_sample(start_beat, samples_per_beat), mono, gain, pan)


def _developed_root(cue: dict[str, Any], bar: int, bars: int) -> tuple[int, bool]:
    progression = cue["progression"]
    if bar == bars - 1:
        return 0, False
    if bar < bars // 2:
        return int(progression[bar % len(progression)]), False
    # The second half deliberately changes harmonic order and alternates first
    # inversion.  It is a development pass, not a duplicated phrase block.
    return int(progression[(bar + 2) % len(progression)]), (bar % 2 == 0)


def _arrange_harmony(
    track: np.ndarray,
    cue: dict[str, Any],
    samples_per_beat: float,
    beats_per_bar: int,
    bars: int,
) -> None:
    texture = str(cue["texture"])
    energy = float(cue["energy"])
    harmony = str(cue["instruments"]["harmony"])
    bass = str(cue["instruments"]["bass"])
    harmony_gain = 0.070 + energy * 0.020
    bass_gain = 0.085 + energy * 0.025
    for bar in range(bars):
        bar_beat = float(bar * beats_per_bar)
        root, inversion = _developed_root(cue, bar, bars)
        chord = [root, root + 2, root + 4]
        if inversion:
            chord = [root + 2, root + 4, root + 7]
        if texture in {"lullaby", "aquatic", "space", "theatre", "flowing"}:
            step = 0.5 if beats_per_bar <= 4 else 1.0
            pulses = int(math.ceil(beats_per_bar / step))
            for pulse in range(pulses):
                position = pulse * step
                if position >= beats_per_bar:
                    break
                degree = chord[(pulse + (1 if bar >= bars // 2 else 0)) % len(chord)]
                _add_note(
                    track, cue, harmony, degree, bar_beat + position, step * 1.45,
                    harmony_gain * (0.86 if pulse % 2 else 1.0), -0.30 + 0.12 * (pulse % 3),
                    f"harmony:{bar}:{pulse}", 0, samples_per_beat,
                )
        elif texture == "waltz":
            for pulse in range(beats_per_bar):
                for voice, degree in enumerate(chord if pulse == 0 else chord[1:]):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + pulse, 0.78,
                        harmony_gain * (0.78 if pulse else 1.0), -0.34 + voice * 0.22,
                        f"waltz:{bar}:{pulse}:{voice}", 0, samples_per_beat,
                    )
        elif texture == "polka":
            # Oom-pah is the physical verb of both handwork cues: bass lands on
            # the numbered beat below, while short accordion/toy-machine chords
            # answer on each off-beat. Without this branch a declared polka used
            # the generic sustained-chord pattern and did not sound like its brief.
            for pulse in range(beats_per_bar):
                for voice, degree in enumerate(chord[1:]):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + pulse + 0.5, 0.34,
                        harmony_gain * (0.94 if pulse % 2 else 1.04),
                        -0.28 + voice * 0.38, f"polka:{bar}:{pulse}:{voice}",
                        0, samples_per_beat,
                    )
        elif texture == "bluegrass":
            step = 0.5
            for pulse in range(int(beats_per_bar / step)):
                degree = chord[(pulse * 2 + bar) % len(chord)]
                _add_note(
                    track, cue, harmony, degree, bar_beat + pulse * step, step * 0.72,
                    harmony_gain * (0.92 if pulse % 2 else 1.05), -0.28 + 0.12 * (pulse % 2),
                        f"bluegrass:{bar}:{pulse}", 0, samples_per_beat,
                    )
        elif texture == "tiptoe":
            positions = [0.5, max(1.5, beats_per_bar * 0.5 + 0.5)]
            for pulse, position in enumerate(positions):
                if position >= beats_per_bar:
                    continue
                for voice, degree in enumerate(chord[1:]):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + position, 0.52,
                        harmony_gain * 0.82, -0.24 + voice * 0.32,
                        f"tiptoe:{bar}:{pulse}:{voice}", 0, samples_per_beat,
                    )
        elif texture == "swing":
            # Late off-beat comping gives the padded boxing practice its
            # bounce without turning the score into a hard jazz pastiche.
            positions = [beat + 2.0 / 3.0 for beat in range(beats_per_bar)]
            for pulse, position in enumerate(positions):
                if position >= beats_per_bar:
                    continue
                for voice, degree in enumerate(chord[1:]):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + position, 0.30,
                        harmony_gain * (0.96 if pulse % 2 else 1.04),
                        -0.28 + voice * 0.36, f"swing:{bar}:{pulse}:{voice}",
                        0, samples_per_beat,
                    )
        elif texture == "march":
            for pulse in range(beats_per_bar):
                voices = chord if pulse == 0 else chord[1:]
                for voice, degree in enumerate(voices):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + pulse, 0.55,
                        harmony_gain * (1.02 if pulse == 0 else 0.78),
                        -0.32 + voice * 0.26, f"march:{bar}:{pulse}:{voice}",
                        0, samples_per_beat,
                    )
        elif texture in {"bounce", "folk"}:
            step = max(1, beats_per_bar // 3)
            for pulse, position in enumerate(range(0, beats_per_bar, step)):
                degree = chord[(pulse + bar) % len(chord)]
                _add_note(
                    track, cue, harmony, degree, bar_beat + float(position), 0.62,
                    harmony_gain * (1.0 if pulse % 2 == 0 else 0.84),
                    -0.24 + 0.18 * (pulse % 3), f"bounce:{bar}:{pulse}",
                    0, samples_per_beat,
                )
        elif texture in {"boss", "combat", "drive", "pop"}:
            step = 1 if texture in {"combat", "drive", "pop"} else max(1, beats_per_bar // 2)
            for pulse, position in enumerate(range(0, beats_per_bar, step)):
                for voice, degree in enumerate(chord):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + float(position),
                        0.62 if step == 1 else max(0.75, step * 0.72),
                        harmony_gain * (1.0 if pulse == 0 else 0.74),
                        -0.34 + voice * 0.28, f"action:{bar}:{pulse}:{voice}",
                        0, samples_per_beat,
                    )
        elif texture in {"cinematic", "gentle"}:
            positions = [0.0] if texture == "gentle" else [0.0, beats_per_bar * 0.5]
            for pulse, position in enumerate(positions):
                for voice, degree in enumerate(chord):
                    _add_note(
                        track, cue, harmony, degree, bar_beat + position,
                        max(0.8, beats_per_bar * (0.72 if texture == "gentle" else 0.42)),
                        harmony_gain * (1.0 if pulse == 0 else 0.78),
                        -0.36 + voice * 0.28, f"sustain:{bar}:{pulse}:{voice}",
                        0, samples_per_beat,
                    )
        else:
            raise ValueError(f"Unhandled harmonic texture: {texture}")
        bass_positions = [0.0]
        if texture == "polka":
            bass_positions = [float(beat) for beat in range(beats_per_bar)]
        elif beats_per_bar >= 3:
            bass_positions.append(float(beats_per_bar // 2))
        for pulse, position in enumerate(bass_positions):
            bass_degree = root if pulse == 0 else root + 4
            _add_note(
                track, cue, bass, bass_degree, bar_beat + position,
                min(float(beats_per_bar) * 0.48, 1.8), bass_gain, -0.08,
                f"bass:{bar}:{pulse}", -1, samples_per_beat,
            )


def _add_motif(
    track: np.ndarray,
    cue: dict[str, Any],
    catalog: dict[str, Any],
    start_bar: int,
    developed: bool,
    samples_per_beat: float,
    beats_per_bar: int,
) -> None:
    motif = catalog["roshan_motif"]
    degrees = [int(value) for value in motif["scale_degrees"]]
    units = [float(value) for value in motif["rhythm_units"]]
    unit_beat = beats_per_bar / sum(units)
    instrument = str(cue["instruments"]["lead"] if not developed else cue["instruments"]["accent"])
    energy = float(cue["energy"])
    texture = str(cue["texture"])
    articulation = 0.88
    if texture in {"lullaby", "aquatic", "space", "flowing", "cinematic", "gentle"}:
        articulation = 0.96
    elif texture in {"polka", "bluegrass", "tiptoe", "bounce", "combat", "drive"}:
        articulation = 0.68
    elif texture in {"march", "swing", "pop"}:
        articulation = 0.78
    cursor = float(start_bar * beats_per_bar)
    for index, (degree, length_units) in enumerate(zip(degrees, units)):
        # Development preserves the recognizable contour but changes register,
        # articulation, pan, and the harmony beneath it.
        octave = 1 if not developed else (1 + (1 if index in (2, 3) else 0))
        duration = unit_beat * length_units * articulation * (0.90 if developed else 1.0)
        _add_note(
            track, cue, instrument, degree, cursor, duration,
            (0.105 + energy * 0.035) * (0.82 if developed else 1.0),
            (-0.12 + index * 0.045) if not developed else (0.18 - index * 0.035),
            f"motif:{'developed' if developed else 'home'}:{index}:{cue['motif_treatment']}",
            octave, samples_per_beat,
        )
        cursor += unit_beat * length_units


def _arrange_melody(
    track: np.ndarray,
    cue: dict[str, Any],
    catalog: dict[str, Any],
    samples_per_beat: float,
    beats_per_bar: int,
    bars: int,
) -> None:
    lead = str(cue["instruments"]["lead"])
    energy = float(cue["energy"])
    pattern = list(cue["melody"])
    _add_motif(track, cue, catalog, 0, False, samples_per_beat, beats_per_bar)
    midpoint = bars // 2
    _add_motif(track, cue, catalog, midpoint, True, samples_per_beat, beats_per_bar)
    phrase_starts = [1, midpoint + 1]
    unit = beats_per_bar * 2.0 / len(pattern)
    for phrase_index, start_bar in enumerate(phrase_starts):
        if start_bar + 2 > bars:
            continue
        phrase = pattern
        if phrase_index == 1:
            # Rotate the answer and lift selected degrees.  Rests move with the
            # phrase, so the second half cannot be a byte/phrase repeat.
            rotation = 3 % len(pattern)
            phrase = pattern[rotation:] + pattern[:rotation]
        for index, degree_value in enumerate(phrase):
            if degree_value is None:
                continue
            degree = int(degree_value)
            if phrase_index == 1 and index % 4 in (1, 2):
                degree += 1
            start = start_bar * beats_per_bar + index * unit
            _add_note(
                track, cue, lead, degree, start, unit * (0.72 if str(cue["texture"]) in {"tiptoe", "polka", "combat"} else 0.88),
                0.090 + energy * 0.042, 0.10 if phrase_index == 0 else -0.08,
                f"melody:{phrase_index}:{index}", 1, samples_per_beat,
            )
    accent = str(cue["instruments"]["accent"])
    for bar in range(2, bars - 1, 4):
        root, _ = _developed_root(cue, bar, bars)
        _add_note(
            track, cue, accent, root + 7, (bar + 1) * beats_per_bar - 0.55,
            0.44, 0.060 + energy * 0.020, 0.32,
            f"accent:{bar}", 1, samples_per_beat,
        )


def _percussion_events(style: str, beats_per_bar: int) -> list[tuple[float, str, float, float]]:
    half = beats_per_bar * 0.5
    if style == "none":
        return []
    if style == "brush":
        return [(half, "brush", 0.16, 0.18), (max(0.5, beats_per_bar - 1.0), "brush", 0.11, -0.15)]
    if style == "tiptoe":
        return [(0.5, "wood", 0.11, -0.22), (max(1.5, half + 0.5), "wood", 0.09, 0.22)]
    if style == "bubble":
        return [(0.5, "bubble", 0.12, -0.25), (half + 0.5, "bubble", 0.10, 0.25)]
    if style == "soft_march":
        events = [(0.0, "kick", 0.14, 0.0), (half, "kick", 0.10, 0.0)]
        for beat in range(1, beats_per_bar, 2):
            events.append((float(beat), "brush", 0.13, 0.16))
        return events
    if style == "tutorial_brush":
        return [
            (float(beat), "kick" if beat == 0 else "brush", 0.13 if beat == 0 else 0.10, -0.08 + beat * 0.05)
            for beat in range(beats_per_bar)
        ]
    if style in {"shaker", "bluegrass"}:
        events = [(beat * 0.5, "shaker", 0.055 if beat % 2 else 0.07, -0.28 if beat % 2 else 0.28) for beat in range(beats_per_bar * 2)]
        if style == "bluegrass":
            events.extend((float(beat), "brush", 0.10, 0.18) for beat in range(1, beats_per_bar, 2))
        return events
    if style == "sleigh":
        return [(float(beat), "sleigh", 0.065 if beat else 0.09, -0.22 + 0.11 * (beat % 4)) for beat in range(beats_per_bar)]
    if style in {"pulse", "pop", "soft_combat"}:
        events: list[tuple[float, str, float, float]] = [(0.0, "kick", 0.15, 0.0)]
        if beats_per_bar >= 4:
            events.append((half, "kick", 0.11, 0.0))
            events.extend([(1.0, "brush", 0.12, 0.16), (3.0, "brush", 0.12, -0.16)])
        if style in {"pop", "soft_combat"}:
            events.extend((beat * 0.5, "shaker", 0.045, -0.24 if beat % 2 else 0.24) for beat in range(beats_per_bar * 2))
        if style == "soft_combat":
            events.append((max(0.5, beats_per_bar - 0.5), "wood", 0.075, 0.1))
        return events
    raise ValueError(f"Unsupported percussion style: {style}")


def _arrange_percussion(
    track: np.ndarray,
    cue: dict[str, Any],
    samples_per_beat: float,
    beats_per_bar: int,
    bars: int,
) -> None:
    style = str(cue["percussion"])
    events = _percussion_events(style, beats_per_bar)
    energy_scale = 0.72 + float(cue["energy"]) * 0.28
    for bar in range(bars):
        # Pull percussion back during the home motif and change emphasis after
        # the midpoint.  Timing stays exact; only orchestration develops.
        section_scale = 0.72 if bar in (0, bars // 2) else 1.0
        if bar >= bars // 2 and bar % 2:
            section_scale *= 0.88
        for event_index, (position, kind, velocity, pan) in enumerate(events):
            mono = _synth_drum(
                kind,
                velocity * energy_scale * section_scale,
                _seed_for(cue["id"], "drum", bar, event_index, kind),
            )
            _add_circular(
                track,
                _event_sample(bar * beats_per_bar + position, samples_per_beat),
                mono,
                1.0,
                pan,
            )


def _arrange_adaptive_timing(
    track: np.ndarray,
    cue: dict[str, Any],
    samples_per_beat: float,
) -> None:
    """Author a quiet wait and one unmistakable action downbeat.

    The boss seeks into this passage when its wind-up starts and corrects to
    the action marker when the vulnerable animation frame actually opens.
    This remains one rendered Music stream: no runtime stem, sample player,
    or live synthesis is needed to make the score teach the interaction.
    """
    adaptive = cue.get("adaptive_markers")
    if not isinstance(adaptive, dict):
        return
    anticipation_beat = float(adaptive["anticipation_start_beat"])
    action_beat = float(adaptive["action_beat"])
    start_sample = _event_sample(anticipation_beat, samples_per_beat)
    action_sample = _event_sample(action_beat, samples_per_beat)
    hush_count = max(0, action_sample - start_sample)
    if hush_count <= 0:
        return

    # Pull the full arrangement rapidly out of the way, then leave a long,
    # almost-silent breath. The final three sparse bell steps are a musical
    # countdown, not a second instruction track.
    fade_count = min(hush_count, max(1, _event_sample(1.0, samples_per_beat)))
    envelope = np.full(hush_count, 0.045, dtype=np.float64)
    envelope[:fade_count] = np.linspace(1.0, 0.045, fade_count, endpoint=True)
    track[start_sample:action_sample] *= envelope[:, np.newaxis]

    accent = str(cue["instruments"]["accent"])
    for index, (lead_beats, degree, gain) in enumerate(
        ((1.5, 0, 0.060), (1.0, 2, 0.078), (0.5, 4, 0.098))
    ):
        _add_note(
            track, cue, accent, degree, action_beat - lead_beats, 0.20,
            gain, -0.22 + index * 0.22, f"adaptive_count:{index}", 1,
            samples_per_beat,
        )

    # The vulnerable frame opens on this friendly, full-spectrum downbeat.
    # Bell owns the instant; warm harmony and kick give it enough body to read
    # from a phone speaker without making Grand Puff sound threatening.
    harmony = str(cue["instruments"]["harmony"])
    for voice, degree in enumerate((0, 2, 4)):
        _add_note(
            track, cue, harmony, degree, action_beat, 1.10,
            0.135 if voice == 0 else 0.112,
            -0.30 + voice * 0.30, f"adaptive_action_chord:{voice}", 0,
            samples_per_beat,
        )
    _add_note(
        track, cue, accent, 7, action_beat, 0.85, 0.155, 0.12,
        "adaptive_action_bell", 1, samples_per_beat,
    )
    kick = _synth_drum(
        "kick", 0.24, _seed_for(cue["id"], "adaptive_action_kick")
    )
    _add_circular(track, action_sample, kick, 1.0, 0.0)


def _seam_metrics(samples: np.ndarray) -> dict[str, float]:
    if samples.shape[0] < 3:
        return {"boundary_jump": 0.0, "adjacent_p999": 0.0, "jump_ratio": 0.0}
    adjacent = np.max(np.abs(np.diff(samples, axis=0)), axis=1)
    boundary = float(np.max(np.abs(samples[0] - samples[-1])))
    p999 = float(np.percentile(adjacent, 99.9))
    return {
        "boundary_jump": round(boundary, 8),
        "adjacent_p999": round(p999, 8),
        "jump_ratio": round(boundary / max(p999, 1.0e-9), 5),
    }


def _render_float(cue: dict[str, Any], catalog: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    sample_count, samples_per_beat, beats_per_bar, bars = _cue_clock(cue)
    track = np.zeros((sample_count, CHANNELS), dtype=np.float64)
    _arrange_harmony(track, cue, samples_per_beat, beats_per_bar, bars)
    _arrange_melody(track, cue, catalog, samples_per_beat, beats_per_bar, bars)
    _arrange_percussion(track, cue, samples_per_beat, beats_per_bar, bars)
    _arrange_adaptive_timing(track, cue, samples_per_beat)
    dry = track.copy()
    # Circular delay/reverb keeps the loop mathematically periodic.  np.roll
    # wraps whole-canvas audio; no cut tail is hidden at the seam.
    delay_a = max(1, int(round(0.137 * SAMPLE_RATE)))
    delay_b = max(1, int(round(0.263 * SAMPLE_RATE)))
    track += np.roll(dry, delay_a, axis=0)[:, ::-1] * 0.105
    track += np.roll(dry, delay_b, axis=0) * 0.055
    track /= 1.16
    track -= np.mean(track, axis=0, keepdims=True)
    # Gentle symmetric saturation controls additive peaks without a lookahead
    # limiter whose state could disagree across the loop boundary.
    track = np.tanh(track * 1.35) / math.tanh(1.35)
    peak = float(np.max(np.abs(track)))
    if peak <= 1.0e-9:
        raise ValueError(f"{cue['id']}: rendered silence")
    track *= (10.0 ** (-6.0 / 20.0)) / peak
    metrics = {
        "sample_count": sample_count,
        "duration_seconds": round(sample_count / SAMPLE_RATE, 6),
        "samples_per_beat": round(samples_per_beat, 8),
        "raw_seam": _seam_metrics(track),
        "development": {
            "midpoint_bar": bars // 2,
            "changes": ["progression_order", "alternating_inversion", "melody_rotation", "answer_note_lifts", "motif_instrument_and_register"],
        },
    }
    if float(metrics["raw_seam"]["jump_ratio"]) > 4.0:
        raise ValueError(f"{cue['id']}: raw loop boundary is anomalous: {metrics['raw_seam']}")
    return track, metrics


def _write_pcm(path: Path, samples: np.ndarray) -> np.ndarray:
    pcm = np.clip(np.rint(samples * 32767.0), -32767.0, 32767.0).astype("<i2")
    wavfile.write(path, SAMPLE_RATE, pcm)
    return pcm


def _measure_loudness(ffmpeg: Path, path: Path) -> dict[str, float]:
    command = [
        str(ffmpeg), "-hide_banner", "-nostdin", "-i", str(path),
        "-af", f"loudnorm=I={TARGET_LUFS}:TP={PEAK_CEILING_DBTP}:LRA=7:print_format=json",
        "-f", "null", "-",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    matches = re.findall(r"\{\s*\"input_i\".*?\}", result.stderr, flags=re.DOTALL)
    if not matches:
        raise ValueError(f"Could not parse FFmpeg loudness report for {path}")
    report = json.loads(matches[-1])
    return {
        "integrated_lufs": float(report["input_i"]),
        "true_peak_dbtp": float(report["input_tp"]),
        "loudness_range_lu": float(report["input_lra"]),
        "threshold_lufs": float(report["input_thresh"]),
    }


def _normalise_pcm(ffmpeg: Path, track: np.ndarray, temp_dir: Path) -> tuple[np.ndarray, dict[str, Any]]:
    analysis_path = temp_dir / "analysis.wav"
    _write_pcm(analysis_path, track)
    before = _measure_loudness(ffmpeg, analysis_path)
    gain_db = TARGET_LUFS - before["integrated_lufs"]
    normalised = track * (10.0 ** (gain_db / 20.0))
    peak_limit = 10.0 ** (PCM_PEAK_TARGET_DBFS / 20.0)
    peak = float(np.max(np.abs(normalised)))
    peak_limited = False
    if peak > peak_limit:
        normalised *= peak_limit / peak
        peak_limited = True
    final_path = temp_dir / "normalised.wav"
    pcm = _write_pcm(final_path, normalised)
    after = _measure_loudness(ffmpeg, final_path)
    rms = float(np.sqrt(np.mean((pcm.astype(np.float64) / 32767.0) ** 2)))
    peak_int = int(np.max(np.abs(pcm.astype(np.int32))))
    return pcm, {
        "normalization_gain_db": round(gain_db, 4),
        "peak_limited": peak_limited,
        "pcm_peak": peak_int,
        "pcm_peak_dbfs": round(20.0 * math.log10(max(peak_int, 1) / 32767.0), 4),
        "pcm_rms_dbfs": round(20.0 * math.log10(max(rms, 1.0e-12)), 4),
        "pcm_loudness": after,
    }


def _ogg_crc(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if crc & 0x80000000 else (crc << 1) & 0xFFFFFFFF
    return crc


def _canonicalize_ogg(path: Path, serial: int) -> None:
    data = bytearray(path.read_bytes())
    offset = 0
    pages = 0
    while offset < len(data):
        if data[offset : offset + 4] != b"OggS" or offset + 27 > len(data):
            raise ValueError(f"Malformed Ogg page in {path} at byte {offset}")
        segment_count = data[offset + 26]
        header_end = offset + 27 + segment_count
        if header_end > len(data):
            raise ValueError(f"Truncated Ogg lacing table in {path}")
        body_size = sum(data[offset + 27 : header_end])
        page_end = header_end + body_size
        if page_end > len(data):
            raise ValueError(f"Truncated Ogg page body in {path}")
        data[offset + 14 : offset + 18] = struct.pack("<I", serial)
        data[offset + 22 : offset + 26] = b"\x00\x00\x00\x00"
        data[offset + 22 : offset + 26] = struct.pack("<I", _ogg_crc(bytes(data[offset:page_end])))
        offset = page_end
        pages += 1
    if pages == 0:
        raise ValueError(f"No Ogg pages found in {path}")
    path.write_bytes(data)


def _encode_ogg(ffmpeg: Path, wav_path: Path, destination: Path, cue: dict[str, Any], sample_count: int, serial: int) -> None:
    command = [
        str(ffmpeg), "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
        "-fflags", "+bitexact", "-i", str(wav_path), "-map_metadata", "-1",
        "-ac", str(CHANNELS), "-ar", str(SAMPLE_RATE), "-c:a", "libvorbis",
        "-b:a", VORBIS_TARGET, "-minrate", VORBIS_MINIMUM, "-maxrate", VORBIS_MAXIMUM,
        "-flags:a", "+bitexact",
        "-metadata", f"TITLE={cue['title']}",
        "-metadata", "ARTIST=Mermaid Roshan",
        "-metadata", "ALBUM=Reef of Light Area Music",
        "-metadata", f"CUE_ID={cue['id']}",
        "-metadata", f"BPM={cue['bpm']}",
        "-metadata", "BPM_UNIT=notated_denominator",
        "-metadata", f"METER={cue['meter'][0]}/{cue['meter'][1]}",
        "-metadata", "LOOPSTART=0",
        "-metadata", f"LOOPEND={sample_count}",
        "-metadata", f"LOOPLENGTH={sample_count}",
        "-metadata", "LICENSE=Project-owned original composition and synthesis",
        "-metadata", "COMMENT=Deterministic offline synthesis; no samples or soundfonts",
        "-serial_offset", str(serial), str(destination),
    ]
    subprocess.run(command, check=True)
    _canonicalize_ogg(destination, serial)


def _probe_ogg(ffprobe: Path, path: Path) -> dict[str, Any]:
    command = [
        str(ffprobe), "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:format_tags:stream=codec_name,sample_rate,channels:stream_tags",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    stream = (data.get("streams") or [{}])[0]
    fmt = data.get("format", {})
    tags: dict[str, str] = {}
    for source in (fmt.get("tags", {}), stream.get("tags", {})):
        tags.update({str(key).upper(): str(value) for key, value in source.items()})
    return {
        "codec": str(stream.get("codec_name", "")),
        "sample_rate_hz": int(stream.get("sample_rate", 0)),
        "channels": int(stream.get("channels", 0)),
        "duration_seconds": float(fmt.get("duration", 0.0)),
        "file_bytes": int(fmt.get("size", path.stat().st_size)),
        "average_bitrate_bps": int(fmt.get("bit_rate", 0)),
        "tags": tags,
    }


def _decode_pcm(ffmpeg: Path, path: Path) -> np.ndarray:
    command = [
        str(ffmpeg), "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le", "-ac", str(CHANNELS), "-ar", str(SAMPLE_RATE), "-",
    ]
    decoded = subprocess.run(command, check=True, capture_output=True).stdout
    pcm = np.frombuffer(decoded, dtype="<i2")
    if pcm.size % CHANNELS:
        raise ValueError(f"Decoded PCM channel alignment failed for {path}")
    return pcm.reshape((-1, CHANNELS)).astype(np.float64) / 32767.0


def _verify_encoded(
    ffmpeg: Path,
    ffprobe: Path,
    path: Path,
    cue: dict[str, Any],
    expected_samples: int,
) -> dict[str, Any]:
    probe = _probe_ogg(ffprobe, path)
    if probe["codec"] != "vorbis" or probe["sample_rate_hz"] != SAMPLE_RATE or probe["channels"] != CHANNELS:
        raise ValueError(f"{path}: wrong codec/rate/channels: {probe}")
    if int(probe["average_bitrate_bps"]) < MINIMUM_MEASURED_BITRATE:
        raise ValueError(f"{path}: measured bitrate is below {MINIMUM_MEASURED_BITRATE}")
    tags = probe["tags"]
    required_tags = {
        "CUE_ID": str(cue["id"]),
        "BPM": str(cue["bpm"]),
        "BPM_UNIT": "notated_denominator",
        "METER": f"{cue['meter'][0]}/{cue['meter'][1]}",
        "LOOPSTART": "0",
        "LOOPEND": str(expected_samples),
        "LOOPLENGTH": str(expected_samples),
    }
    for key, expected in required_tags.items():
        if tags.get(key) != expected:
            raise ValueError(f"{path}: tag {key}={tags.get(key)!r}; expected {expected!r}")
    decoded = _decode_pcm(ffmpeg, path)
    if abs(decoded.shape[0] - expected_samples) > 256:
        raise ValueError(f"{path}: decoded {decoded.shape[0]} samples; expected about {expected_samples}")
    seam = _seam_metrics(decoded)
    if seam["jump_ratio"] > 5.0:
        raise ValueError(f"{path}: decoded loop boundary is anomalous: {seam}")
    loudness = _measure_loudness(ffmpeg, path)
    if loudness["true_peak_dbtp"] > PEAK_CEILING_DBTP + 0.05:
        raise ValueError(f"{path}: true peak {loudness['true_peak_dbtp']:.2f} dBTP exceeds ceiling")
    if not TARGET_LUFS - 1.5 <= loudness["integrated_lufs"] <= TARGET_LUFS + 0.75:
        raise ValueError(f"{path}: loudness {loudness['integrated_lufs']:.2f} LUFS is not near target")
    probe["decoded_sample_count"] = int(decoded.shape[0])
    probe["decoded_seam"] = seam
    probe["loudness"] = loudness
    return probe


def _import_text(cue: dict[str, Any]) -> str:
    source = f"res://assets/audio/music/{cue['id']}.ogg"
    digest = hashlib.md5(source.encode("utf-8")).hexdigest()
    beat_count = int(cue["bars"]) * int(cue["meter"][0])
    return (
        "[remap]\n\n"
        "importer=\"oggvorbisstr\"\n"
        "type=\"AudioStreamOggVorbis\"\n"
        f"path=\"res://.godot/imported/{cue['id']}.ogg-{digest}.oggvorbisstr\"\n\n"
        "[deps]\n\n"
        f"source_file=\"{source}\"\n"
        f"dest_files=[\"res://.godot/imported/{cue['id']}.ogg-{digest}.oggvorbisstr\"]\n\n"
        "[params]\n\n"
        "loop=true\n"
        "loop_offset=0.0\n"
        f"bpm={float(cue['bpm']):.1f}\n"
        f"beat_count={beat_count}\n"
        f"bar_beats={int(cue['meter'][0])}\n"
    )


def _write_import(path: Path, cue: dict[str, Any]) -> None:
    # Exact Godot import creates a stable resource UID. Preserve it during a
    # later selective cue rebuild instead of making unrelated resource identity
    # churn merely because the audio bytes changed.
    uid_line = ""
    if path.is_file():
        match = re.search(r'^uid="[^"]+"$', path.read_text(encoding="utf-8"), flags=re.MULTILINE)
        if match:
            uid_line = match.group(0) + "\n"
    text = _import_text(cue)
    if uid_line:
        text = text.replace(
            'type="AudioStreamOggVorbis"\n',
            'type="AudioStreamOggVorbis"\n' + uid_line,
            1,
        )
    path.write_text(text, encoding="utf-8", newline="\n")


def _verify_import(path: Path, cue: dict[str, Any]) -> None:
    text = path.read_text(encoding="utf-8")
    required = [
        "importer=\"oggvorbisstr\"",
        "type=\"AudioStreamOggVorbis\"",
        "loop=true",
        "loop_offset=0",
        f"bpm={float(cue['bpm']):.1f}",
        f"beat_count={int(cue['bars']) * int(cue['meter'][0])}",
        f"bar_beats={int(cue['meter'][0])}",
        f"source_file=\"res://assets/audio/music/{cue['id']}.ogg\"",
    ]
    for token in required:
        if token not in text:
            raise ValueError(f"{path}: missing import setting {token}")


def _render_one(
    repo_root: Path,
    ffmpeg: Path,
    ffprobe: Path,
    catalog: dict[str, Any],
    cue: dict[str, Any],
) -> dict[str, Any]:
    slug = str(cue["id"])
    output_path = repo_root / OUTPUT_DIR / f"{slug}.ogg"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    track, render_metrics = _render_float(cue, catalog)
    with tempfile.TemporaryDirectory(prefix=f"reef-area-music-{slug}-") as temp:
        temp_dir = Path(temp)
        pcm, normalization = _normalise_pcm(ffmpeg, track, temp_dir)
        wav_path = temp_dir / "normalised.wav"
        wavfile.write(wav_path, SAMPLE_RATE, pcm)
        encoded_path = temp_dir / f"{slug}.ogg"
        serial = _serial_for(slug)
        _encode_ogg(ffmpeg, wav_path, encoded_path, cue, int(render_metrics["sample_count"]), serial)
        probe = _verify_encoded(ffmpeg, ffprobe, encoded_path, cue, int(render_metrics["sample_count"]))
        shutil.copyfile(encoded_path, output_path)
    import_path = output_path.with_name(output_path.name + ".import")
    _write_import(import_path, cue)
    _verify_import(import_path, cue)
    return {
        "id": slug,
        "title": cue["title"],
        "family": cue["family"],
        "area": cue["area"],
        "brief": cue["brief"],
        "cue_score_sha256": _cue_score_sha256(cue),
        "path": output_path.relative_to(repo_root).as_posix(),
        "import_path": import_path.relative_to(repo_root).as_posix(),
        "tempo_bpm": cue["bpm"],
        "meter": cue["meter"],
        "bars": cue["bars"],
        "tonic_midi": cue["tonic_midi"],
        "mode": cue["mode"],
        "texture": cue["texture"],
        "percussion": cue["percussion"],
        "instruments": cue["instruments"],
        "motif_treatment": cue["motif_treatment"],
        "progression": cue["progression"],
        "melody": cue["melody"],
        "energy": cue["energy"],
        **(
            {"adaptive_markers": cue["adaptive_markers"]}
            if "adaptive_markers" in cue else {}
        ),
        "seed_namespace": slug,
        "seed_derivation": "SHA-256(cue_id:event_role:event_index[:midi_note])",
        "ogg_stream_serial": serial,
        "loop_import": {
            "enabled": True,
            "offset_seconds": 0.0,
            "beat_count": int(cue["bars"]) * int(cue["meter"][0]),
            "bar_beats": int(cue["meter"][0]),
        },
        **render_metrics,
        **normalization,
        **probe,
        "pcm_sha256": hashlib.sha256(pcm.tobytes()).hexdigest(),
        "sha256": _sha256(output_path),
    }


def _manifest(
    repo_root: Path,
    ffmpeg: Path,
    catalog: dict[str, Any],
    records: list[dict[str, Any]],
    generator_sha256: str,
    score_catalog_sha256: str,
) -> dict[str, Any]:
    script_path = Path(__file__).resolve()
    return {
        "schema": MANIFEST_SCHEMA,
        "generation_method": "Deterministic offline NumPy additive/physical-style synthesis; no samples, soundfonts, downloaded audio, protected recordings, or network services",
        "seed_derivation": "All noise and micro-variation use SHA-256-derived NumPy PCG64 seeds namespaced by cue ID and event; no unseeded random state",
        "license": "Project-owned original composition and synthesis",
        "generator": script_path.relative_to(repo_root).as_posix(),
        "generator_version": GENERATOR_VERSION,
        "generator_sha256": generator_sha256,
        "score_catalog": SCORES_PATH.as_posix(),
        "score_schema": SCORE_SCHEMA,
        "score_catalog_sha256": score_catalog_sha256,
        "dependencies": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "ffmpeg": _tool_version(ffmpeg),
        },
        "target": {
            "codec": "Ogg Vorbis",
            "sample_rate_hz": SAMPLE_RATE,
            "channels": CHANNELS,
            "integrated_lufs": TARGET_LUFS,
            "true_peak_ceiling_dbtp": PEAK_CEILING_DBTP,
            "vorbis_target_bitrate": VORBIS_TARGET,
            "vorbis_minimum_bitrate": VORBIS_MINIMUM,
            "vorbis_maximum_bitrate": VORBIS_MAXIMUM,
            "minimum_measured_bitrate_bps": MINIMUM_MEASURED_BITRATE,
            "bpm_unit": "notated_denominator",
            "minimum_loop_seconds": MINIMUM_LOOP_SECONDS,
            "maximum_loop_seconds": MAXIMUM_LOOP_SECONDS,
            "loop_tags": [
                "CUE_ID", "BPM", "BPM_UNIT", "METER", "LOOPSTART",
                "LOOPEND", "LOOPLENGTH",
            ],
        },
        "roshan_motif": catalog["roshan_motif"],
        "complete_catalog": [record["id"] for record in records] == list(EXPECTED_IDS),
        "files": records,
    }


def _build(
    repo_root: Path,
    ffmpeg: Path,
    catalog: dict[str, Any],
    cues: list[dict[str, Any]],
    selected_ids: list[str] | None,
    generator_sha256: str,
    score_catalog_sha256: str,
) -> Path:
    ffprobe = _find_ffprobe(ffmpeg)
    selected = cues
    if selected_ids:
        requested = set(selected_ids)
        unknown = sorted(requested - set(EXPECTED_IDS))
        if unknown:
            raise ValueError(f"Unknown cue IDs: {unknown}")
        selected = [cue for cue in cues if cue["id"] in requested]
    records: list[dict[str, Any]] = []
    for index, cue in enumerate(selected, start=1):
        print(f"MUSIC|build {index:02d}/{len(selected):02d}|{cue['id']}|{cue['title']}", flush=True)
        records.append(_render_one(repo_root, ffmpeg, ffprobe, catalog, cue))
    script_path = Path(__file__).resolve()
    score_path = repo_root / SCORES_PATH
    if _text_sha256(script_path) != generator_sha256 \
            or _text_sha256(score_path) != score_catalog_sha256:
        raise RuntimeError(
            "Generator or score catalog changed during rendering; refusing to "
            "write a manifest for mixed provenance. Run the build again."
        )
    manifest = _manifest(
        repo_root, ffmpeg, catalog, records, generator_sha256,
        score_catalog_sha256,
    )
    # A selective development render may replace the requested OGGs, but it
    # must never overwrite the canonical proof with an intentionally partial
    # catalog. Only a complete-catalog build owns the release manifest.
    manifest_path = repo_root / OUTPUT_DIR / MANIFEST_NAME
    if selected_ids:
        manifest_path = repo_root / "audit/area_music/area_music_manifest.partial.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return manifest_path


def _check(repo_root: Path, ffmpeg: Path, catalog: dict[str, Any], cues: list[dict[str, Any]]) -> Path:
    ffprobe = _find_ffprobe(ffmpeg)
    manifest_path = repo_root / OUTPUT_DIR / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("Unexpected area-music manifest schema")
    if manifest.get("generator_sha256") != _text_sha256(Path(__file__).resolve()):
        raise ValueError("Area-music manifest was built by a different generator revision")
    if manifest.get("score_catalog_sha256") != _text_sha256(repo_root / SCORES_PATH):
        raise ValueError("Area-music manifest was built from a different score catalog revision")
    current_dependencies = {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "ffmpeg": _tool_version(ffmpeg),
    }
    if manifest.get("dependencies") != current_dependencies:
        raise ValueError(
            "Area-music verification dependencies differ from the recorded render toolchain: "
            f"current={current_dependencies}, recorded={manifest.get('dependencies')}"
        )
    records = manifest.get("files", [])
    if [record.get("id") for record in records] != list(EXPECTED_IDS):
        raise ValueError("Area-music manifest is partial or out of runtime order")
    cue_by_id = {str(cue["id"]): cue for cue in cues}
    for index, record in enumerate(records, start=1):
        slug = str(record["id"])
        cue = cue_by_id[slug]
        path = repo_root / str(record["path"])
        import_path = repo_root / str(record["import_path"])
        print(f"MUSIC|check {index:02d}/{len(records):02d}|{slug}", flush=True)
        if _sha256(path) != record.get("sha256"):
            raise ValueError(f"Hash mismatch: {path}")
        if record.get("cue_score_sha256") != _cue_score_sha256(cue):
            raise ValueError(f"Cue-score hash mismatch: {slug}")
        _verify_import(import_path, cue)
        probe = _verify_encoded(ffmpeg, ffprobe, path, cue, int(record["sample_count"]))
        if int(probe["file_bytes"]) != int(record["file_bytes"]):
            raise ValueError(f"Size mismatch: {path}")
        if int(probe["average_bitrate_bps"]) != int(record["average_bitrate_bps"]):
            raise ValueError(f"Bitrate mismatch: {path}")
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-check", action="store_true", help="validate scores without writing audio")
    parser.add_argument("--check", action="store_true", help="validate committed audio, imports, and manifest")
    parser.add_argument("--cue", action="append", help="render only one cue ID; repeat for more")
    parser.add_argument("--ffmpeg", help="path to the pinned FFmpeg executable")
    args = parser.parse_args()
    if args.catalog_check and args.check:
        parser.error("--catalog-check and --check are mutually exclusive")
    repo_root = Path(__file__).resolve().parents[1]
    generator_sha256 = _text_sha256(Path(__file__).resolve())
    score_catalog_sha256 = _text_sha256(repo_root / SCORES_PATH)
    catalog, cues = _load_catalog(repo_root)
    if args.catalog_check:
        durations = [int(cue["bars"]) * int(cue["meter"][0]) * 60.0 / float(cue["bpm"]) for cue in cues]
        print(
            f"MUSIC|catalog ALL OK|cues={len(cues)}|duration={min(durations):.2f}-{max(durations):.2f}s|"
            f"motif={catalog['roshan_motif']['scale_degrees']}"
        )
        return 0
    ffmpeg = _find_ffmpeg(args.ffmpeg, repo_root)
    if args.check:
        path = _check(repo_root, ffmpeg, catalog, cues)
    else:
        path = _build(
            repo_root, ffmpeg, catalog, cues, args.cue,
            generator_sha256, score_catalog_sha256,
        )
    print(f"MUSIC|result ALL OK|{path.relative_to(repo_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
