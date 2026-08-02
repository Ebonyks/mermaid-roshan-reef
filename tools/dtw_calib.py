#!/usr/bin/env python3
"""Calibrate the spoken-spell matcher's accept thresholds (MIC_SPELLS.md).

scripts/mic_input.gd decides whether a heard sound is a spell using two
numbers, ACCEPT_DIST and ACCEPT_RATIO. Guessing them is how you ship a game
that either never hears the child or casts fireballs at the dishwasher, and
the probe suite cannot help: it asserts the DECISION, so it only tells you the
thresholds are wrong after you have already picked them.

This is a faithful port of that matcher -- the same 20-band mean-removed
features, the same resample to 32 frames, the same banded DTW, the same
distance -- so the thresholds can be derived from measured separation instead.
Run it after changing BANDS, NORM_FRAMES, DTW_BAND, DUR_WEIGHT or the feature
front end, and copy the resulting numbers into mic_input.gd.

    python3 tools/dtw_calib.py

Synthetic words stand in for the real ones and mirror why FREEZE and FIREBALL
are separable at all: word A is one fricative-vowel-fricative sweep, word B is
three humps over twice the duration. Recorded audio is noisier than this, which
is why ACCEPT_DIST ships as a loose ceiling and ACCEPT_RATIO -- which is
scale-invariant, and therefore survives a different room -- does the work.
"""
import math
import random

BANDS = 20
NORM_FRAMES = 32
DTW_BAND = 8
DUR_WEIGHT = 0.15
TEMPLATES_PER_WORD = 5
INF = float("inf")

# the shipped values in scripts/mic_input.gd
ACCEPT_DIST = 0.45
ACCEPT_RATIO = 0.60

TRIALS = 40
SEED = 20260802


# ----- feature front end (mirrors MicInput._read_frame / _normalise_frame) ---

def normalise(f):
    m = sum(f) / len(f)
    return [x - m for x in f]


def frame(center, width, jitter, rng):
    """One feature frame: a tent centred on `center` in mel-band space, which
    is what a formant looks like once magnitudes are logged and mean-removed."""
    return normalise([-abs(b - center) / width + rng.uniform(-jitter, jitter)
                      for b in range(BANDS)])


def word_a(frames, jitter, rng):
    """One syllable: high -> low -> high in a single gesture."""
    out = []
    for i in range(frames):
        t = i / max(frames - 1, 1)
        out.append(frame(15.0 - 9.0 * math.sin(t * math.pi), 4.0, jitter, rng))
    return out


def word_b(frames, jitter, rng):
    """Three syllables walking down the band range."""
    out = []
    for i in range(frames):
        t = i / max(frames - 1, 1)
        out.append(frame(9.0 + 5.0 * math.sin(t * math.pi * 3.0) - 3.0 * t,
                         3.4, jitter, rng))
    return out


def drifted(is_a, frames, shift, wscale, rng, jitter=0.35):
    """The same word said differently: formants shifted, mouth more or less
    open. This is the realistic hard case -- a child never repeats herself."""
    out = []
    for i in range(frames):
        t = i / max(frames - 1, 1)
        if is_a:
            center, width = 15.0 - 9.0 * math.sin(t * math.pi), 4.0
        else:
            center, width = 9.0 + 5.0 * math.sin(t * math.pi * 3.0) - 3.0 * t, 3.4
        out.append(frame(center + shift, width * wscale, jitter, rng))
    return out


def noise_word(frames, rng, width=9.0, jitter=0.9):
    """Room noise: spectrally incoherent frame to frame, so DTW cannot align."""
    return [frame(rng.uniform(2.0, 17.0), width, jitter, rng) for _ in range(frames)]


def blended(rng, jitter=0.2):
    """A near-miss: a real-looking utterance that is neither word. The
    recogniser must prefer silence over a plausible guess."""
    return [frame(12.0 - 4.0 * math.sin(i / 23.0 * math.pi * 2.0), 5.0, jitter, rng)
            for i in range(24)]


# ----- matcher (mirrors MicInput._resample / _local / _dtw / classify) -------

def resample(frames):
    n = len(frames)
    out = []
    for i in range(NORM_FRAMES):
        pos = i * (n - 1) / (NORM_FRAMES - 1)
        i0 = int(math.floor(pos))
        i1 = min(i0 + 1, n - 1)
        t = pos - i0
        a, b = frames[i0], frames[i1]
        out.extend(a[k] + (b[k] - a[k]) * t for k in range(BANDS))
    return out


def local(a, ai, b, bi):
    oa, ob = ai * BANDS, bi * BANDS
    return sum(abs(a[oa + k] - b[ob + k]) for k in range(BANDS)) / BANDS


def dtw(a, b):
    n = NORM_FRAMES
    cost = [INF] * (n * n)
    for i in range(n):
        lo, hi = max(0, i - DTW_BAND), min(n - 1, i + DTW_BAND)
        row, prow = i * n, (i - 1) * n
        for j in range(lo, hi + 1):
            d = local(a, i, b, j)
            if i == 0 and j == 0:
                cost[row + j] = d
                continue
            best = INF
            if i > 0:
                best = min(best, cost[prow + j])
                if j > 0:
                    best = min(best, cost[prow + j - 1])
            if j > 0:
                best = min(best, cost[row + j - 1])
            cost[row + j] = best + d
    total = cost[(n - 1) * n + (n - 1)]
    return INF if total == INF else total / (2 * n)


def score(templates, frames, dur):
    """Returns (best_word, best_distance, runner_up_distance)."""
    norm = resample(frames)
    best_word, best, runner = "", INF, INF
    for word, lst in templates.items():
        word_best = INF
        for data, tdur in lst:
            d = dtw(norm, data)
            if tdur > 0 and dur > 0:
                d += DUR_WEIGHT * abs(math.log(dur / tdur))
            word_best = min(word_best, d)
        if word_best < best:
            runner, best, best_word = best, word_best, word
        elif word_best < runner:
            runner = word_best
    return best_word, best, runner


def verdict(templates, frames, dur):
    word, best, runner = score(templates, frames, dur)
    if not word or best > ACCEPT_DIST:
        return "", best, runner
    if runner < INF and best > ACCEPT_RATIO * runner:
        return "", best, runner
    return word, best, runner


def enroll(maker, frames, dur, rng):
    out = []
    for i in range(TEMPLATES_PER_WORD):
        n = frames + (i % 3) - 1
        out.append((resample(maker(n, 0.05, rng)), dur * (0.92 + 0.04 * (i % 3))))
    return out


# ----- reports --------------------------------------------------------------

def separation_table():
    """Where each class of sound actually lands. This is the table quoted in
    mic_input.gd above ACCEPT_DIST."""
    rows = {}

    def add(tag, word, best, runner):
        d, r = rows.setdefault(tag, ([], []))
        d.append(best)
        r.append(best / runner if runner < INF else 0.0)

    for trial in range(TRIALS):
        rng = random.Random(SEED + trial)
        T = {"ice": enroll(word_a, 18, 0.40, rng), "fire": enroll(word_b, 34, 0.82, rng)}
        for jit, tag in ((0.30, "same word, clean"), (0.60, "same word, noisy"),
                         (1.20, "same word, very noisy")):
            for maker, n, dur in ((word_a, 17, 0.40), (word_b, 33, 0.82)):
                add(tag, *score(T, maker(n, jit, rng), dur))
        for shift in (1.0, -1.0, 1.5, -1.5):
            ws = 1.15 if shift > 0 else 0.9
            add("same word, sloppy delivery", *score(T, drifted(True, 17, shift, ws, rng), 0.40))
            add("same word, sloppy delivery", *score(T, drifted(False, 33, shift, ws, rng), 0.82))
        add("ambiguous half-word", *score(T, blended(rng), 0.6))
        for i in range(8):
            add("room noise", *score(T, noise_word(20 + i, rng), 0.5))

    print("=== where each class of sound lands (%d trials) ===" % TRIALS)
    print("%-30s %-18s %s" % ("", "distance", "ratio best/runner"))
    for tag, (d, r) in rows.items():
        print("  %-28s %.2f-%.2f%9s%.2f-%.2f" % (tag, min(d), max(d), "", min(r), max(r)))
    print()
    print("  ACCEPT_DIST  = %.2f   (ceiling; only guard when one word is enrolled)" % ACCEPT_DIST)
    print("  ACCEPT_RATIO = %.2f   (the real discriminator)" % ACCEPT_RATIO)


def probe_headroom():
    """Every assertion scripts/probe_mic.gd makes, over many seeds, with the
    head-room each one has left. Anything at or below zero ships a red probe."""
    stats = {}

    def note(k, ok, headroom):
        s = stats.setdefault(k, [0, 0, 1e9])
        s[0] += 1
        s[1] += 1 if ok else 0
        s[2] = min(s[2], headroom)

    for trial in range(TRIALS):
        rng = random.Random(SEED + trial)
        T = {"ice": enroll(word_a, 18, 0.40, rng), "fire": enroll(word_b, 34, 0.82, rng)}
        for i in range(6):
            w, b, r = verdict(T, word_a(17 + i % 3, 0.60, rng), 0.40)
            note("a spoken ICE is recognised", w == "ice", ACCEPT_RATIO - b / r)
            w, b, r = verdict(T, word_b(33 + i % 3, 0.60, rng), 0.82)
            note("a spoken FIRE is recognised", w == "fire", ACCEPT_RATIO - b / r)
            w, _, _ = verdict(T, word_a(17 + i % 3, 0.60, rng), 0.40)
            note("the two spells are never confused", w != "fire", 0.0)
            w, _, _ = verdict(T, word_b(33 + i % 3, 0.60, rng), 0.82)
            note("the two spells are never confused", w != "ice", 0.0)
        for shift in (1.0, -1.0, 1.5, -1.5):
            ws = 1.15 if shift > 0 else 0.9
            w, b, r = verdict(T, drifted(True, 17, shift, ws, rng), 0.40)
            note("a sloppier delivery still lands", w == "ice", ACCEPT_RATIO - b / r)
            w, b, r = verdict(T, drifted(False, 33, shift, ws, rng), 0.82)
            note("a sloppier delivery still lands", w == "fire", ACCEPT_RATIO - b / r)
        for i in range(8):
            w, b, r = verdict(T, noise_word(20 + i, rng), 0.5)
            note("room noise casts no spell", w == "", b / r - ACCEPT_RATIO)
        w, b, r = verdict(T, blended(rng), 0.6)
        note("an ambiguous sound stays silent", w == "", b / r - ACCEPT_RATIO)

    print()
    print("=== probe_mic.gd assertions, with head-room ===")
    worst_ok = True
    for k, (n, ok, worst) in stats.items():
        flag = "" if ok == n else "   <-- WOULD SHIP A RED PROBE"
        worst_ok = worst_ok and ok == n
        print("  %-36s %4d/%-4d  %+.3f%s" % (k, ok, n, worst, flag))
    return worst_ok


if __name__ == "__main__":
    separation_table()
    ok = probe_headroom()
    raise SystemExit(0 if ok else 1)
