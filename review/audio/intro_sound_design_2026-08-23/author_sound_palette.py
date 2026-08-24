"""Author deterministic, nonvoice intro sound-design source masters.

This file intentionally has no dependency on runtime game audio.  Every source
is synthesized from a stable SHA-256-derived seed, making re-authoring and
auditing reproducible.  Outputs are compact 48 kHz stereo WAV masters in
``authored/``; the existing review mix and renderer are deliberately out of
scope.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt


SAMPLE_RATE = 48_000
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authored"


def seed_for(label: str) -> int:
	return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "little")


def rng_for(label: str) -> np.random.Generator:
	return np.random.default_rng(seed_for(label))


def timebase(seconds: float) -> np.ndarray:
	return np.arange(round(seconds * SAMPLE_RATE), dtype=np.float64) / SAMPLE_RATE


def smoothstep(x: np.ndarray) -> np.ndarray:
	return x * x * (3.0 - 2.0 * x)


def fade(seconds: float, attack: float, release: float) -> np.ndarray:
	n = round(seconds * SAMPLE_RATE)
	env = np.ones(n, dtype=np.float64)
	attack_n = min(n, round(attack * SAMPLE_RATE))
	release_n = min(n, round(release * SAMPLE_RATE))
	if attack_n:
		env[:attack_n] = smoothstep(np.linspace(0.0, 1.0, attack_n, endpoint=False))
	if release_n:
		env[-release_n:] *= smoothstep(np.linspace(1.0, 0.0, release_n, endpoint=False))
	return env


def band_noise(label: str, seconds: float, low: float, high: float) -> np.ndarray:
	noise = rng_for(label).standard_normal(round(seconds * SAMPLE_RATE))
	low_hz = max(20.0, low)
	high_hz = min(SAMPLE_RATE * 0.48, high)
	sos = butter(3, [low_hz, high_hz], btype="bandpass", fs=SAMPLE_RATE, output="sos")
	return sosfilt(sos, noise)


def lowpass(signal: np.ndarray, cutoff: float) -> np.ndarray:
	sos = butter(3, cutoff, btype="lowpass", fs=SAMPLE_RATE, output="sos")
	return sosfilt(sos, signal)


def tone(seconds: float, frequency: float, amplitude: float = 1.0) -> np.ndarray:
	t = timebase(seconds)
	return amplitude * np.sin(2.0 * math.pi * frequency * t)


def stereo(mono: np.ndarray, label: str, width: float = 0.12) -> np.ndarray:
	"""Make gentle decorrelation without widening the child-focused center."""
	rng = rng_for(label + ":stereo")
	texture = lowpass(rng.standard_normal(mono.size), 1900.0)
	texture /= max(1e-9, float(np.max(np.abs(texture))))
	t = np.arange(mono.size, dtype=np.float64) / SAMPLE_RATE
	pan = width * 0.55 * np.sin(2.0 * math.pi * 0.065 * t + rng.random() * math.tau)
	left = mono * (1.0 + pan) + texture * width * 0.012
	right = mono * (1.0 - pan) - texture * width * 0.012
	return np.column_stack((left, right))


def finish(signal: np.ndarray) -> np.ndarray:
	peak = float(np.max(np.abs(signal)))
	if peak > 0.82:
		signal = signal * (0.82 / peak)
	return np.asarray(np.round(signal * 32767.0), dtype=np.int16)


def write_master(name: str, signal: np.ndarray) -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	wavfile.write(OUT / name, SAMPLE_RATE, finish(signal))


def flight_exterior() -> np.ndarray:
	seconds = 8.0
	t = timebase(seconds)
	# A soft turbofan-like bed: slow spool movement plus a separate air layer,
	# with no sharp transient or tonal alarm.
	spool = 92.0 + 7.0 * np.sin(2.0 * math.pi * 0.075 * t)
	phase = 2.0 * math.pi * np.cumsum(spool) / SAMPLE_RATE
	engine = 0.46 * np.sin(phase) + 0.16 * np.sin(2.0 * phase + 0.12)
	engine += 0.07 * np.sin(3.0 * phase + 0.3)
	air = band_noise("flight:air", seconds, 260.0, 1800.0)
	air /= max(1e-9, float(np.max(np.abs(air))))
	air *= 0.14 + 0.035 * np.sin(2.0 * math.pi * 0.11 * t)
	return stereo((engine + air) * fade(seconds, 0.45, 0.65) * 0.42, "flight", 0.20)


def cabin_room() -> np.ndarray:
	seconds = 6.0
	t = timebase(seconds)
	# Interior room tone is intentionally warm and nearly static to leave space
	# for owner-recorded dialogue later; it does not imitate speech.
	room = 0.22 * tone(seconds, 72.0)
	room += 0.08 * tone(seconds, 144.0, 1.0)
	air = band_noise("cabin:air", seconds, 170.0, 720.0)
	air /= max(1e-9, float(np.max(np.abs(air))))
	air *= 0.065 + 0.018 * np.sin(2.0 * math.pi * 0.17 * t)
	wood = 0.025 * np.sin(2.0 * math.pi * (242.0 + 3.0 * np.sin(2.0 * math.pi * 0.07 * t)) * t)
	return stereo((room + air + wood) * fade(seconds, 0.7, 0.7) * 0.33, "cabin", 0.08)


def reveal(label: str, seconds: float, base: float) -> np.ndarray:
	t = timebase(seconds)
	progress = np.clip(t / seconds, 0.0, 1.0)
	env = smoothstep(progress) * smoothstep(1.0 - progress)
	glide = base * (0.72 + 0.42 * progress)
	phase = 2.0 * math.pi * np.cumsum(glide) / SAMPLE_RATE
	voice = np.sin(phase) + 0.35 * np.sin(2.01 * phase + 0.4) + 0.16 * np.sin(3.02 * phase)
	shimmer = band_noise(label + ":shimmer", seconds, 2200.0, 7600.0)
	shimmer /= max(1e-9, float(np.max(np.abs(shimmer))))
	# A continuous swell with a few very soft grains reads as wonder, not a UI chime.
	grains = np.zeros_like(t)
	for index, center in enumerate(np.linspace(0.28, seconds - 0.25, 5)):
		width = 0.18 + 0.025 * (index % 2)
		window = np.exp(-0.5 * ((t - center) / width) ** 2)
		grains += window * np.sin(2.0 * math.pi * (base * (1.4 + 0.08 * index)) * t)
	mono = (0.38 * voice + 0.055 * shimmer + 0.045 * grains) * env * 0.78
	return stereo(mono, label, 0.30)


def forest_lakeside() -> np.ndarray:
	seconds = 8.0
	t = timebase(seconds)
	water = band_noise("forest:water", seconds, 70.0, 520.0)
	water /= max(1e-9, float(np.max(np.abs(water))))
	water *= 0.17 + 0.03 * np.sin(2.0 * math.pi * 0.09 * t)
	leaves = band_noise("forest:leaves", seconds, 850.0, 4600.0)
	leaves /= max(1e-9, float(np.max(np.abs(leaves))))
	leaves *= 0.032 + 0.012 * np.sin(2.0 * math.pi * 0.13 * t + 1.1)
	drops = np.zeros_like(t)
	for index, center in enumerate((0.74, 2.12, 3.93, 5.1, 6.75)):
		if center >= seconds:
			continue
		local = np.maximum(0.0, t - center)
		window = (local >= 0.0) * np.exp(-local * (6.0 + 0.4 * index))
		drops += window * (0.28 * np.sin(2.0 * math.pi * (590.0 + index * 43.0) * local))
	mono = (water + leaves + drops) * fade(seconds, 0.55, 0.75) * 0.46
	return stereo(mono, "forest", 0.34)


def otter_plane_action() -> np.ndarray:
	seconds = 9.0
	t = timebase(seconds)
	mono = np.zeros_like(t)
	# Three soft, rounded glissandi suggest playful movement around the parked plane.
	for index, center in enumerate((1.0, 3.2, 5.75, 7.35)):
		length = 0.72 if index % 2 == 0 else 0.52
		local = t - center
		mask = (local >= 0.0) & (local < length)
		phase = 2.0 * math.pi * np.cumsum(320.0 + 150.0 * np.sin(np.pi * np.clip(local, 0, length) / length)) / SAMPLE_RATE
		env = np.exp(-5.4 * np.maximum(local, 0.0)) * (local < length)
		mono += mask * 0.14 * np.sin(phase + index * 0.7) * env
	# Rounded contact pulses are low-mid and deliberately unlike a UI click or combat hit.
	for index, center in enumerate((1.55, 4.12, 6.5, 8.12)):
		local = np.maximum(0.0, t - center)
		mono += 0.13 * np.exp(-local * (9.0 + index)) * np.sin(2.0 * math.pi * (118.0 + 8.0 * index) * local)
	air = band_noise("otter:air", seconds, 900.0, 3500.0)
	air /= max(1e-9, float(np.max(np.abs(air))))
	mono += air * (0.018 + 0.01 * np.sin(2.0 * math.pi * 0.21 * t))
	return stereo(mono * fade(seconds, 0.35, 0.55) * 1.35, "otter-plane", 0.42)


def reunion_walk() -> np.ndarray:
	seconds = 7.0
	t = timebase(seconds)
	mono = np.zeros_like(t)
	# A paired, quiet footfall texture supports the exterior reunion without
	# implying dialogue; soft filtered air keeps it connected to the flight scene.
	for index, center in enumerate((0.65, 1.28, 2.0, 2.64, 3.38, 4.02, 4.74, 5.4, 6.08)):
		local = np.maximum(0.0, t - center)
		mono += 0.095 * np.exp(-local * 13.0) * np.sin(2.0 * math.pi * (92.0 + (index % 2) * 17.0) * local)
	air = band_noise("reunion:air", seconds, 180.0, 1100.0)
	air /= max(1e-9, float(np.max(np.abs(air))))
	mono += air * (0.032 + 0.01 * np.sin(2.0 * math.pi * 0.12 * t))
	return stereo(mono * fade(seconds, 0.5, 0.65) * 1.55, "reunion", 0.24)


def bridge_water_arrival() -> np.ndarray:
	seconds = 6.0
	t = timebase(seconds)
	water = band_noise("bridge:water", seconds, 45.0, 700.0)
	water /= max(1e-9, float(np.max(np.abs(water))))
	water *= 0.18 + 0.035 * np.sin(2.0 * math.pi * 0.10 * t)
	wood = np.zeros_like(t)
	for index, center in enumerate((0.5, 1.7, 2.85, 4.15, 5.25)):
		local = np.maximum(0.0, t - center)
		wood += 0.10 * np.exp(-local * 7.0) * np.sin(2.0 * math.pi * (148.0 + 11.0 * index) * local)
	# A low, sustained arrival resonance gives the castle bridge a sense of place;
	# it intentionally avoids a pitched one-shot/chime silhouette.
	# The retained home bed has strong D/F-sharp-family energy; F-sharp3 keeps
	# this sustained arrival consonant without copying or sampling that bed.
	arrival = 0.055 * np.sin(2.0 * math.pi * 185.0 * t) * smoothstep(np.clip(t / 2.2, 0.0, 1.0))
	mono = (water + wood + arrival) * fade(seconds, 0.6, 0.8) * 0.48
	return stereo(mono, "bridge-water", 0.38)


def main() -> None:
	masters = {
		"flight_exterior_loop.wav": flight_exterior(),
		"cabin_room_loop.wav": cabin_room(),
		# D4 and A3 are consonant reveal anchors for the retained D/F-sharp-family bed.
		"reveal_island.wav": reveal("reveal-island", 2.2, 293.66),
		"reveal_castle.wav": reveal("reveal-castle", 2.6, 220.0),
		"forest_lakeside_loop.wav": forest_lakeside(),
		"otter_plane_action_loop.wav": otter_plane_action(),
		"reunion_walk_loop.wav": reunion_walk(),
		"bridge_water_arrival_loop.wav": bridge_water_arrival(),
	}
	for name, signal in masters.items():
		write_master(name, signal)
	print(f"wrote {len(masters)} deterministic 48 kHz stereo masters to {OUT}")


if __name__ == "__main__":
	main()
