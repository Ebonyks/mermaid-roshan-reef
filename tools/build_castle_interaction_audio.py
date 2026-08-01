#!/usr/bin/env python3
"""Build deterministic, project-owned sound effects for castle interactions.

The sounds are synthesized from mathematical oscillators and seeded noise.  No
downloaded samples or protected voice recordings are read.  Output is mono
24 kHz Ogg Vorbis for the mobile target, with canonical Ogg stream serials and
a hash-backed manifest.

Usage:
    python tools/build_castle_interaction_audio.py
    python tools/build_castle_interaction_audio.py --check
    python tools/build_castle_interaction_audio.py --ffmpeg C:/path/ffmpeg.exe
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
from typing import Callable

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, chirp, sosfilt


SAMPLE_RATE = 24_000
CHANNELS = 1
VORBIS_QUALITY = 4
TARGET_PEAK_DBFS = -3.0
TARGET_PEAK = 10.0 ** (TARGET_PEAK_DBFS / 20.0)
GENERATOR_VERSION = 1
OUTPUT_DIR = Path("assets/audio/castle")
MANIFEST_NAME = "castle_interaction_sfx_manifest.json"


def _samples(seconds: float) -> int:
	return int(round(seconds * SAMPLE_RATE))


def _time(seconds: float) -> np.ndarray:
	return np.arange(_samples(seconds), dtype=np.float64) / SAMPLE_RATE


def _fade(signal: np.ndarray, attack: float = 0.005, release: float = 0.04) -> np.ndarray:
	result = np.asarray(signal, dtype=np.float64).copy()
	attack_n = min(_samples(attack), result.size)
	release_n = min(_samples(release), result.size)
	if attack_n:
		result[:attack_n] *= np.linspace(0.0, 1.0, attack_n, endpoint=True)
	if release_n:
		result[-release_n:] *= np.linspace(1.0, 0.0, release_n, endpoint=True)
	return result


def _add(track: np.ndarray, start: float, sound: np.ndarray, gain: float = 1.0) -> None:
	start_n = _samples(start)
	if start_n >= track.size:
		return
	end_n = min(start_n + sound.size, track.size)
	track[start_n:end_n] += sound[: end_n - start_n] * gain


def _tone(
	frequency: float,
	duration: float,
	decay: float = 8.0,
	harmonics: tuple[tuple[float, float], ...] = ((1.0, 1.0),),
	attack: float = 0.002,
) -> np.ndarray:
	t = _time(duration)
	signal = np.zeros_like(t)
	for multiplier, gain in harmonics:
		signal += gain * np.sin(2.0 * math.pi * frequency * multiplier * t)
	envelope = np.exp(-decay * t)
	return _fade(signal * envelope, attack=attack, release=min(0.04, duration * 0.2))


def _sweep(
	start_hz: float,
	end_hz: float,
	duration: float,
	method: str = "linear",
	decay: float = 2.0,
) -> np.ndarray:
	t = _time(duration)
	signal = chirp(t, f0=start_hz, f1=end_hz, t1=duration, method=method)
	return _fade(signal * np.exp(-decay * t), attack=0.004, release=min(0.05, duration * 0.25))


def _noise(
	rng: np.random.Generator,
	duration: float,
	low_hz: float,
	high_hz: float,
	attack: float = 0.02,
	release: float = 0.08,
) -> np.ndarray:
	count = _samples(duration)
	white = rng.standard_normal(count)
	nyquist = SAMPLE_RATE * 0.5
	low = max(20.0, low_hz) / nyquist
	high = min(nyquist - 100.0, high_hz) / nyquist
	if low <= 0.001:
		sos = butter(3, high, btype="lowpass", output="sos")
	elif high >= 0.999:
		sos = butter(3, low, btype="highpass", output="sos")
	else:
		sos = butter(3, (low, high), btype="bandpass", output="sos")
	filtered = sosfilt(sos, white)
	rms = float(np.sqrt(np.mean(filtered * filtered)))
	if rms > 0.0:
		filtered /= rms * 4.0
	return _fade(filtered, attack=attack, release=release)


def _knock(frequency: float = 180.0, duration: float = 0.11) -> np.ndarray:
	t = _time(duration)
	low = np.sin(2.0 * math.pi * frequency * t)
	high = 0.36 * np.sin(2.0 * math.pi * frequency * 2.37 * t)
	click = 0.18 * np.sign(np.sin(2.0 * math.pi * frequency * 4.1 * t))
	return _fade((low + high + click) * np.exp(-34.0 * t), attack=0.001, release=0.025)


def _new_track(duration: float) -> np.ndarray:
	return np.zeros(_samples(duration), dtype=np.float64)


def _rng(slug: str) -> np.random.Generator:
	seed = int.from_bytes(hashlib.sha256(slug.encode("utf-8")).digest()[:8], "little")
	return np.random.Generator(np.random.PCG64(seed))


def _faucet_water() -> np.ndarray:
	rng = _rng("faucet_water")
	track = _new_track(1.20)
	_add(track, 0.045, _knock(520.0, 0.09), 0.52)
	water = _noise(rng, 0.84, 650.0, 7_800.0, attack=0.14, release=0.16)
	water *= 0.78 + 0.16 * np.sin(2.0 * math.pi * 7.0 * _time(0.84))
	_add(track, 0.18, water, 0.78)
	for when, pitch in ((0.30, 1320.0), (0.47, 1580.0), (0.66, 1190.0), (0.83, 1740.0)):
		_add(track, when, _sweep(pitch, pitch * 0.62, 0.12, decay=14.0), 0.11)
	_add(track, 1.01, _knock(470.0, 0.10), 0.45)
	return track


def _toilet_flush() -> np.ndarray:
	rng = _rng("toilet_flush")
	track = _new_track(1.80)
	_add(track, 0.035, _knock(235.0, 0.13), 0.70)
	_add(track, 0.20, _knock(620.0, 0.08), 0.35)
	whoosh = _noise(rng, 1.20, 95.0, 4_600.0, attack=0.20, release=0.28)
	t = _time(1.20)
	whoosh *= 0.80 + 0.20 * np.sin(2.0 * math.pi * (2.7 + 4.8 * t) * t)
	_add(track, 0.28, whoosh, 1.05)
	_add(track, 0.36, _sweep(330.0, 92.0, 0.96, method="logarithmic", decay=1.5), 0.28)
	_add(track, 0.57, _sweep(780.0, 180.0, 0.75, method="logarithmic", decay=2.2), 0.12)
	_add(track, 1.52, _knock(205.0, 0.16), 0.62)
	return track


def _fridge_door() -> np.ndarray:
	track = _new_track(1.16)
	_add(track, 0.04, _knock(760.0, 0.075), 0.42)
	_add(track, 0.10, _sweep(170.0, 66.0, 0.30, method="logarithmic", decay=5.0), 0.31)
	_add(track, 0.20, _tone(92.0, 0.42, decay=7.0, harmonics=((1.0, 1.0), (2.0, 0.24))), 0.37)
	for pitch in (880.0, 1110.0, 1320.0):
		_add(track, 0.49, _tone(pitch, 0.32, decay=7.0), 0.10)
	_add(track, 0.94, _knock(125.0, 0.19), 0.92)
	_add(track, 0.98, _tone(410.0, 0.10, decay=28.0), 0.15)
	return track


def _oven_door() -> np.ndarray:
	rng = _rng("oven_door")
	track = _new_track(1.30)
	_add(track, 0.04, _knock(680.0, 0.08), 0.36)
	_add(track, 0.14, _sweep(250.0, 78.0, 0.28, method="logarithmic", decay=4.5), 0.33)
	_add(track, 0.25, _knock(128.0, 0.18), 0.74)
	crackle = _noise(rng, 0.72, 1_200.0, 9_400.0, attack=0.08, release=0.14)
	gate = np.clip(rng.random(crackle.size) * 2.7 - 1.35, 0.0, 1.0)
	crackle *= 0.30 + 0.70 * gate
	_add(track, 0.32, crackle, 0.45)
	_add(track, 0.99, _knock(118.0, 0.22), 0.94)
	_add(track, 1.02, _tone(520.0, 0.13, decay=24.0), 0.14)
	return track


def _pan_clang() -> np.ndarray:
	track = _new_track(0.92)
	for when, gain, base in ((0.04, 1.0, 720.0), (0.30, 0.42, 910.0)):
		for ratio, partial_gain in ((1.0, 1.0), (1.42, 0.62), (2.11, 0.36), (3.37, 0.18)):
			_add(track, when, _tone(base * ratio, 0.70, decay=6.2 + ratio, attack=0.001), gain * partial_gain * 0.34)
	return track


def _curtain_swish() -> np.ndarray:
	rng = _rng("curtain_swish")
	track = _new_track(1.00)
	swish = _noise(rng, 0.82, 330.0, 6_700.0, attack=0.13, release=0.18)
	t = _time(0.82)
	swish *= 0.60 + 0.40 * np.sin(math.pi * np.clip(t / 0.82, 0.0, 1.0))
	_add(track, 0.08, swish, 0.75)
	for when in (0.09, 0.22, 0.37, 0.55, 0.73):
		_add(track, when, _tone(1450.0, 0.07, decay=35.0), 0.075)
	return track


def _page_flip() -> np.ndarray:
	rng = _rng("page_flip")
	track = _new_track(0.76)
	page = _noise(rng, 0.48, 620.0, 8_800.0, attack=0.05, release=0.12)
	t = _time(0.48)
	page *= np.sin(math.pi * np.clip(t / 0.48, 0.0, 1.0))
	_add(track, 0.08, page, 0.72)
	_add(track, 0.48, _knock(390.0, 0.10), 0.33)
	_add(track, 0.54, _noise(rng, 0.14, 900.0, 7_000.0, attack=0.01, release=0.08), 0.25)
	return track


def _toy_blocks() -> np.ndarray:
	track = _new_track(1.10)
	knocks = (
		(0.05, 245.0, 0.72),
		(0.20, 310.0, 0.62),
		(0.34, 205.0, 0.78),
		(0.49, 370.0, 0.54),
		(0.62, 265.0, 0.60),
	)
	for when, pitch, gain in knocks:
		_add(track, when, _knock(pitch, 0.13), gain)
	for pitch in (620.0, 820.0, 1040.0):
		_add(track, 0.69, _tone(pitch, 0.34, decay=8.0), 0.11)
	_add(track, 0.91, _knock(185.0, 0.16), 0.56)
	return track


def _craft_brush() -> np.ndarray:
	rng = _rng("craft_brush")
	track = _new_track(0.96)
	for when, duration, gain in ((0.06, 0.24, 0.60), (0.32, 0.25, 0.70), (0.60, 0.22, 0.55)):
		stroke = _noise(rng, duration, 500.0, 6_200.0, attack=0.035, release=0.07)
		_add(track, when, stroke, gain)
	_add(track, 0.83, _tone(930.0, 0.11, decay=28.0), 0.18)
	return track


def _ribbon_roll() -> np.ndarray:
	rng = _rng("ribbon_roll")
	track = _new_track(1.06)
	roll = _noise(rng, 0.78, 220.0, 3_800.0, attack=0.10, release=0.16)
	t = _time(0.78)
	roll *= 0.72 + 0.28 * np.sin(2.0 * math.pi * (7.0 + 6.0 * t) * t)
	_add(track, 0.06, roll, 0.58)
	for index, when in enumerate((0.12, 0.24, 0.37, 0.51, 0.66)):
		_add(track, when, _knock(520.0 + 45.0 * index, 0.06), 0.13)
	_add(track, 0.82, _sweep(540.0, 1020.0, 0.18, decay=8.0), 0.13)
	return track


def _bubble_water() -> np.ndarray:
	rng = _rng("bubble_water")
	track = _new_track(1.48)
	water = _noise(rng, 1.24, 120.0, 3_600.0, attack=0.18, release=0.24)
	_add(track, 0.09, water, 0.54)
	bubbles = ((0.17, 410.0), (0.33, 560.0), (0.52, 360.0), (0.71, 690.0), (0.93, 480.0), (1.13, 620.0))
	for when, pitch in bubbles:
		_add(track, when, _sweep(pitch, pitch * 1.75, 0.13, decay=9.0), 0.17)
	return track


def _light_switch() -> np.ndarray:
	track = _new_track(0.82)
	_add(track, 0.045, _knock(880.0, 0.07), 0.50)
	for when, pitch, gain in ((0.14, 659.25, 0.22), (0.22, 830.61, 0.19), (0.30, 987.77, 0.17), (0.38, 1318.51, 0.14)):
		_add(track, when, _tone(pitch, 0.40, decay=7.6), gain)
	return track


def _duck_squeak() -> np.ndarray:
	track = _new_track(0.62)
	t = _time(0.36)
	phase = 2.0 * math.pi * (620.0 * t + 0.5 * (980.0 - 620.0) / 0.36 * t * t)
	squeak = np.sin(phase) + 0.34 * np.sin(2.0 * phase) + 0.15 * np.sin(3.0 * phase)
	squeak *= (1.0 + 0.12 * np.sin(2.0 * math.pi * 24.0 * t))
	squeak = _fade(squeak, attack=0.018, release=0.09)
	_add(track, 0.055, squeak, 0.48)
	_add(track, 0.43, _knock(330.0, 0.10), 0.22)
	return track


Synthesizer = Callable[[], np.ndarray]


EFFECTS: tuple[dict[str, object], ...] = (
	{
		"slug": "faucet_water",
		"synth": _faucet_water,
		"semantic_action": "knob turns; water starts, flows, then stops",
		"events_ms": {"knob_open": 45, "water_start": 180, "knob_close": 1010},
	},
	{
		"slug": "toilet_flush",
		"synth": _toilet_flush,
		"semantic_action": "seat lifts, lever clicks, bowl flushes, seat settles",
		"events_ms": {"seat_lift": 35, "lever": 200, "flush_start": 280, "seat_settle": 1520},
	},
	{
		"slug": "fridge_door",
		"synth": _fridge_door,
		"semantic_action": "latch releases, fridge door opens, chimes, then closes",
		"events_ms": {"latch": 40, "door_open": 100, "chime": 490, "door_close": 940},
	},
	{
		"slug": "oven_door",
		"synth": _oven_door,
		"semantic_action": "latch releases, oven opens onto fire, then closes",
		"events_ms": {"latch": 40, "door_open": 140, "fire": 320, "door_close": 990},
	},
	{
		"slug": "pan_clang",
		"synth": _pan_clang,
		"semantic_action": "hanging pan rings twice and decays naturally",
		"events_ms": {"primary_clang": 40, "secondary_clang": 300},
	},
	{
		"slug": "curtain_swish",
		"synth": _curtain_swish,
		"semantic_action": "curtain slides across its rings and settles",
		"events_ms": {"swish_start": 80, "ring_slide": 90, "settle": 900},
	},
	{
		"slug": "page_flip",
		"synth": _page_flip,
		"semantic_action": "book page lifts, flips, and lands",
		"events_ms": {"page_lift": 80, "page_land": 480},
	},
	{
		"slug": "toy_blocks",
		"synth": _toy_blocks,
		"semantic_action": "blocks tumble, stacking rings chime, pieces settle",
		"events_ms": {"blocks_start": 50, "rings": 690, "settle": 910},
	},
	{
		"slug": "craft_brush",
		"synth": _craft_brush,
		"semantic_action": "brush paints three strokes and taps the paint pot",
		"events_ms": {"stroke_one": 60, "stroke_two": 320, "stroke_three": 600, "pot_tap": 830},
	},
	{
		"slug": "ribbon_roll",
		"synth": _ribbon_roll,
		"semantic_action": "ribbon spool unrolls through its guides and springs back",
		"events_ms": {"unroll": 60, "guide_clicks": 120, "retract": 820},
	},
	{
		"slug": "bubble_water",
		"synth": _bubble_water,
		"semantic_action": "pool water burbles while bubbles rise and pop",
		"events_ms": {"water_start": 90, "first_bubble": 170, "last_bubble": 1130},
	},
	{
		"slug": "light_switch",
		"synth": _light_switch,
		"semantic_action": "switch clicks and the pearl light answers with a chime",
		"events_ms": {"switch": 45, "chime_start": 140, "chime_peak": 380},
	},
	{
		"slug": "duck_squeak",
		"synth": _duck_squeak,
		"semantic_action": "rubber duck compresses, squeaks, and pops back",
		"events_ms": {"compress": 55, "release": 430},
	},
)


def _finish_audio(raw: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
	audio = np.asarray(raw, dtype=np.float64)
	if audio.ndim != 1 or audio.size == 0:
		raise ValueError("synthesizer must return a non-empty mono signal")
	# Remove tiny filter offsets and reserve three decibels of headroom.
	audio -= float(np.mean(audio))
	peak = float(np.max(np.abs(audio)))
	if not np.isfinite(peak) or peak <= 0.0:
		raise ValueError("synthesizer returned silent or non-finite audio")
	audio *= TARGET_PEAK / peak
	audio = np.clip(audio, -1.0, 1.0)
	pcm = np.rint(audio * 32767.0).astype("<i2")
	pcm_peak = int(np.max(np.abs(pcm.astype(np.int32))))
	rms = float(np.sqrt(np.mean((pcm.astype(np.float64) / 32767.0) ** 2)))
	metrics: dict[str, object] = {
		"sample_count": int(pcm.size),
		"duration_ms": int(round(pcm.size * 1000.0 / SAMPLE_RATE)),
		"pcm_peak": pcm_peak,
		"peak_dbfs": round(20.0 * math.log10(pcm_peak / 32767.0), 3),
		"rms_dbfs": round(20.0 * math.log10(max(rms, 1.0e-12)), 3),
		"pcm_sha256": hashlib.sha256(pcm.tobytes()).hexdigest(),
	}
	return pcm, metrics


def _find_ffmpeg(explicit: str | None, repo_root: Path) -> Path:
	candidates: list[Path] = []
	if explicit:
		candidates.append(Path(explicit))
	if os.environ.get("REEF_FFMPEG"):
		candidates.append(Path(os.environ["REEF_FFMPEG"]))
	command = shutil.which("ffmpeg")
	if command:
		candidates.append(Path(command))
	candidates.extend(sorted((repo_root / ".video-tools").glob("ffmpeg-*/bin/ffmpeg.exe")))
	local_app_data = os.environ.get("LOCALAPPDATA")
	if local_app_data:
		candidates.extend(
			sorted(Path(local_app_data).glob("Programs/MermaidReefTools/FFmpeg/*/bin/ffmpeg.exe"))
		)
	for candidate in candidates:
		resolved = candidate.expanduser().resolve()
		if resolved.is_file():
			return resolved
	raise FileNotFoundError(
		"FFmpeg was not found. Pass --ffmpeg or set REEF_FFMPEG to the pinned executable."
	)


def _ffmpeg_version(ffmpeg: Path) -> str:
	result = subprocess.run(
		[str(ffmpeg), "-hide_banner", "-version"],
		check=True,
		capture_output=True,
		text=True,
	)
	return result.stdout.splitlines()[0].strip()


def _ogg_crc(data: bytes) -> int:
	crc = 0
	for byte in data:
		crc ^= byte << 24
		for _ in range(8):
			crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if crc & 0x80000000 else (crc << 1) & 0xFFFFFFFF
	return crc


def _canonicalize_ogg(path: Path, serial: int) -> None:
	"""Give every Ogg page a stable stream serial and recompute page CRCs."""
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
		checksum = _ogg_crc(bytes(data[offset:page_end]))
		data[offset + 22 : offset + 26] = struct.pack("<I", checksum)
		offset = page_end
		pages += 1
	if pages == 0:
		raise ValueError(f"No Ogg pages found in {path}")
	path.write_bytes(data)


def _encode_ogg(ffmpeg: Path, pcm: np.ndarray, destination: Path, serial: int) -> None:
	destination.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(prefix="reef-castle-sfx-") as temp_dir:
		wav_path = Path(temp_dir) / "source.wav"
		ogg_path = Path(temp_dir) / "encoded.ogg"
		wavfile.write(wav_path, SAMPLE_RATE, pcm)
		command = [
			str(ffmpeg),
			"-hide_banner",
			"-loglevel",
			"error",
			"-nostdin",
			"-y",
			"-fflags",
			"+bitexact",
			"-i",
			str(wav_path),
			"-map_metadata",
			"-1",
			"-ac",
			str(CHANNELS),
			"-ar",
			str(SAMPLE_RATE),
			"-c:a",
			"libvorbis",
			"-q:a",
			str(VORBIS_QUALITY),
			"-flags:a",
			"+bitexact",
			"-serial_offset",
			str(serial),
			str(ogg_path),
		]
		subprocess.run(command, check=True)
		_canonicalize_ogg(ogg_path, serial)
		shutil.copyfile(ogg_path, destination)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _serial_for(slug: str) -> int:
	# FFmpeg exposes the muxer offset as a signed 31-bit option even though the
	# Ogg page field itself is unsigned.  Staying inside that range also makes
	# the command portable across FFmpeg builds.
	return int.from_bytes(hashlib.sha256(("reef-castle-" + slug).encode("utf-8")).digest()[:4], "little") & 0x7FFFFFFF


def _verify_ogg(ffmpeg: Path, path: Path, expected_samples: int) -> None:
	command = [
		str(ffmpeg),
		"-hide_banner",
		"-loglevel",
		"error",
		"-i",
		str(path),
		"-f",
		"s16le",
		"-ac",
		"1",
		"-ar",
		str(SAMPLE_RATE),
		"-",
	]
	decoded = subprocess.run(command, check=True, capture_output=True).stdout
	decoded_samples = len(decoded) // 2
	# Vorbis may preserve a few codec-delay samples at the tail, but not enough
	# to alter interaction timing perceptibly.
	if abs(decoded_samples - expected_samples) > 256:
		raise ValueError(
			f"{path} decoded to {decoded_samples} samples; expected approximately {expected_samples}"
		)
	decoded_pcm = np.frombuffer(decoded, dtype="<i2").astype(np.int32)
	if decoded_pcm.size == 0 or int(np.max(np.abs(decoded_pcm))) > 32767:
		raise ValueError(f"{path} did not decode to valid peak-safe PCM")


def _build(repo_root: Path, ffmpeg: Path) -> Path:
	output_dir = repo_root / OUTPUT_DIR
	output_dir.mkdir(parents=True, exist_ok=True)
	records: list[dict[str, object]] = []
	for definition in EFFECTS:
		slug = str(definition["slug"])
		synth = definition["synth"]
		if not callable(synth):
			raise TypeError(f"No synthesizer registered for {slug}")
		pcm, metrics = _finish_audio(synth())
		serial = _serial_for(slug)
		path = output_dir / f"{slug}.ogg"
		_encode_ogg(ffmpeg, pcm, path, serial)
		_verify_ogg(ffmpeg, path, int(metrics["sample_count"]))
		records.append(
			{
				"id": slug,
				"path": path.relative_to(repo_root).as_posix(),
				"semantic_action": definition["semantic_action"],
				"events_ms": definition["events_ms"],
				"codec": "Ogg Vorbis",
				"channels": CHANNELS,
				"sample_rate_hz": SAMPLE_RATE,
				"vorbis_quality": VORBIS_QUALITY,
				"ogg_stream_serial": serial,
				**metrics,
				"file_bytes": path.stat().st_size,
				"sha256": _sha256(path),
			}
		)
	script_path = Path(__file__).resolve()
	manifest = {
		"schema": "reef.castle-interaction-sfx.v1",
		"generation_method": "deterministic offline NumPy/SciPy synthesis; no sampled or downloaded audio",
		"generator": script_path.relative_to(repo_root).as_posix(),
		"generator_version": GENERATOR_VERSION,
		"generator_sha256": _sha256(script_path),
		"ffmpeg": _ffmpeg_version(ffmpeg),
		"target": {
			"codec": "Ogg Vorbis",
			"sample_rate_hz": SAMPLE_RATE,
			"channels": CHANNELS,
			"peak_ceiling_dbfs": TARGET_PEAK_DBFS,
		},
		"license": "Project-owned original synthesis; no external source material",
		"files": records,
	}
	manifest_path = output_dir / MANIFEST_NAME
	manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
	return manifest_path


def _check(repo_root: Path, ffmpeg: Path) -> Path:
	manifest_path = repo_root / OUTPUT_DIR / MANIFEST_NAME
	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	if manifest.get("schema") != "reef.castle-interaction-sfx.v1":
		raise ValueError("Unexpected castle interaction SFX manifest schema")
	if manifest.get("generator_sha256") != _sha256(Path(__file__).resolve()):
		raise ValueError("Castle interaction SFX manifest was built by a different generator revision")
	if len(manifest.get("files", [])) != len(EFFECTS):
		raise ValueError("Castle interaction SFX manifest has the wrong number of files")
	expected_ids = [str(definition["slug"]) for definition in EFFECTS]
	actual_ids = [str(record.get("id")) for record in manifest["files"]]
	if actual_ids != expected_ids:
		raise ValueError("Castle interaction SFX manifest IDs or ordering do not match the generator")
	for record in manifest["files"]:
		path = repo_root / str(record["path"])
		if _sha256(path) != record["sha256"]:
			raise ValueError(f"Hash mismatch: {path}")
		if path.stat().st_size != int(record["file_bytes"]):
			raise ValueError(f"Size mismatch: {path}")
		if float(record["peak_dbfs"]) > TARGET_PEAK_DBFS + 0.01:
			raise ValueError(f"Peak ceiling exceeded: {path}")
		_verify_ogg(ffmpeg, path, int(record["sample_count"]))
	return manifest_path


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="validate committed files without rebuilding")
	parser.add_argument("--ffmpeg", help="path to the pinned FFmpeg executable")
	args = parser.parse_args()
	repo_root = Path(__file__).resolve().parents[1]
	ffmpeg = _find_ffmpeg(args.ffmpeg, repo_root)
	manifest_path = _check(repo_root, ffmpeg) if args.check else _build(repo_root, ffmpeg)
	verb = "validated" if args.check else "built"
	print(f"Castle interaction SFX {verb}: {manifest_path.relative_to(repo_root).as_posix()}")
	print(f"Files: {len(EFFECTS)} | {SAMPLE_RATE} Hz mono | peak ceiling {TARGET_PEAK_DBFS:.1f} dBFS")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
