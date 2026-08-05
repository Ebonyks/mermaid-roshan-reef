#!/usr/bin/env python3
"""Synthesize the combat SFX pack (combat wing 2026-08).

Six tiny, gentle, license-clean sounds for the combat feel stack:

  combat_pop.wav          the landed-hit pop (pitch-laddered by the chain)
  combat_bonk.wav         the HARM reaction of a surviving enemy
  combat_poof.wav         the death topper under the pop/shrink/flop styles
  combat_freeze.wav       the arena's icy freeze tinkle
  combat_charge_ring.wav  the charge ring appearing (stage chimes are m.chime)
  combat_fizzle.wav       the kind-miss (wrong element / shell block)

Deterministic pure-stdlib synthesis (no numpy, seeded noise), 44.1 kHz
mono 16-bit WAV, soft amplitudes and 8 ms fades — child-friendly, no harsh
transients. Provenance: generated entirely by this script; no external
sources. License: project code. Recorded replacements can drop in at the
same paths any time (every caller checks ResourceLoader.exists).

Run from the repo root:  python tools/gen_combat_sfx.py
"""
import math
import os
import random
import struct
import wave

RATE = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "sfx")
RNG = random.Random(20260801)


def render(name, seconds, sample_fn, peak=0.28):
    n = int(RATE * seconds)
    fade = int(RATE * 0.008)
    frames = []
    for i in range(n):
        t = i / RATE
        v = sample_fn(t, i)
        if i < fade:
            v *= i / fade
        if i > n - fade:
            v *= (n - i) / fade
        frames.append(max(-1.0, min(1.0, v)) * peak)
    path = os.path.join(OUT, name)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(
            struct.pack("<h", int(v * 32767)) for v in frames))
    print("wrote", os.path.normpath(path))


def sweep(t, f0, f1, dur):
    # phase-correct linear sweep
    k = (f1 - f0) / dur
    return math.sin(2.0 * math.pi * (f0 * t + 0.5 * k * t * t))


def main():
    os.makedirs(OUT, exist_ok=True)

    noise = [RNG.uniform(-1.0, 1.0) for _ in range(RATE)]

    def smooth(i, width):
        j0 = max(0, i - width)
        seg = noise[j0:i + 1]
        return sum(seg) / len(seg) if seg else 0.0

    def pop(t, i):
        body = sweep(t, 540.0, 270.0, 0.11) * math.exp(-28.0 * t)
        click = noise[i % RATE] * math.exp(-400.0 * t) * 0.35
        return body + click
    render("combat_pop.wav", 0.11, pop)

    def bonk(t, i):
        f = sweep(t, 175.0, 118.0, 0.15)
        harm = 0.3 * sweep(t, 350.0, 236.0, 0.15)
        return (f + harm) * math.exp(-20.0 * t)
    render("combat_bonk.wav", 0.15, bonk)

    def poof(t, i):
        return smooth(i, 8) * math.exp(-14.0 * t) * 2.2
    render("combat_poof.wav", 0.26, poof, peak=0.22)

    def freeze(t, i):
        v = 0.0
        for k, f in enumerate((1318.5, 1760.0, 2217.5)):
            t0 = t - 0.06 * k
            if t0 > 0.0:
                v += math.sin(2.0 * math.pi * f * t0) * math.exp(-18.0 * t0)
        return v * 0.5
    render("combat_freeze.wav", 0.32, freeze, peak=0.2)

    def ring(t, i):
        vib = 12.0 * math.sin(2.0 * math.pi * 6.0 * t)
        base = math.sin(2.0 * math.pi * ((440.0 + vib) * t + 1000.0 * t * t))
        attack = min(1.0, t / 0.03)
        return base * attack * math.exp(-9.0 * t)
    render("combat_charge_ring.wav", 0.22, ring, peak=0.18)

    def fizzle(t, i):
        hiss = smooth(i, 4) * math.exp(-22.0 * t) * 1.8
        droop = 0.45 * sweep(t, 320.0, 150.0, 0.18) * math.exp(-16.0 * t)
        return hiss + droop
    render("combat_fizzle.wav", 0.18, fizzle, peak=0.2)


if __name__ == "__main__":
    main()
