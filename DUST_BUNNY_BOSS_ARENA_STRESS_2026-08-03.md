# Dust Bunny Boss — arena stress test, 24 encounters (2026-08-03)

**Harness:** `scripts/probe_dust_boss_arena.gd` (advisory, no gate tokens)
**Frames:** `scripts/probe_dust_boss_shots.gd`, ten beats under xvfb
**Predecessor:** `DUST_BUNNY_BOSS_STRESS_TEST_2026-08-02.md` asked *is it
winnable and is it fun to play*. This one asks **where do the seconds go** and
**what is the child actually looking at while they go**.

```
godot --headless -s scripts/probe_dust_boss_arena.gd
DUSTBOSS_SHOT_OUT=/tmp/dustshots LIBGL_ALWAYS_SOFTWARE=1 \
  xvfb-run -a godot --rendering-method mobile --resolution 1280x720 \
  -s scripts/probe_dust_boss_shots.gd
```

24 encounters = six child archetypes (speedy / casual / wander / masher /
timid / stroll) × four seeds, so every archetype meets four different hop
patterns and four different mercy ramps.

### A note on how the pixels were measured

No harness in this project produces a 1280×720 root viewport — headless
reports 1280×1280, xvfb 1280×1024 — and `OctagonStage.fit_camera()` solves its
framing from *whatever viewport it finds*. A probe that trusts
`Camera3D.unproject_position` is therefore measuring a camera the phone will
never have; the first run of this harness reported the boss at 42% of canvas
height, which is a 1:1-viewport artefact. The probe now re-solves the shipped
framing algorithm against 1280×720 and projects by hand. **Every pixel number
below is the number the child's phone produces.**

---

## 1. Result in one line

All 24 encounters were won, none hit the 300 s cap, nothing was cropped, and
the camera framing is correct. The fight is **shorter than its design band, a
third of it is untouchable, and there is no place in the arena where the boss
can be seen cleanly at the moment he must be read.**

---

## 2. Pacing

| | median | min | max |
|---|---|---|---|
| Fight length (showing excluded) | **40.5 s** | 24.7 s | 57.6 s |
| Windows offered | **5** | 3 | 7 |
| Gap between windows | **7.5 s** | — | — |
| Longest dead air | 0.40 s | 0.10 s | 2.60 s |

Design band is 45–120 s. **15 of 24 encounters land under it, 9 inside it,
none over.** The band was set when a round was one tap; a round is three taps
now, but only three rounds are needed, so a child who reads the tell at all
finishes in five windows.

### Where the ~46 s of a median encounter goes

| beat | seconds | share | can she touch it? |
|---|---|---|---|
| showing | 6.3 | 13.7% | no — taps only sparkle |
| prowl | 16.9 | 36.3% | walk only; taps bounce |
| wind-up | 3.5 | 7.8% | walk only; taps bounce |
| **window open** | **10.9** | **23.3%** | **yes — this is the game** |
| struck / dizzy / angry hold | 7.0 | 15.2% | no |
| befriending | 1.6 | 3.5% | no |

**32.4% of the boss fight is a hold she cannot touch**, and the `struck` hold
is *exactly* 7.0 s in all 24 encounters — a fixed toll of `STRUCK_T + DIZZY_T`
and `STRUCK_T + ANGRY_T`, paid identically whether she is cruising or
struggling. Against 10.9 s of actual window, the fight spends more time
narrating itself than being played.

Dead air is **not** a problem: the longest stretch with nothing moving and
nothing flashing is 0.40 s median. The prowl is busy. It just has nothing in
it that the child can affect or read — which is a different failure, and an
art one.

**Pacing verdicts.** The window budget is right; the *padding* is not. The
showing is 6.3 s of fixed teaching before the first window (correct on first
meeting, dead weight on the tenth), and the 7.0 s struck hold is where an
encounter that should feel like a boss goes quiet. Both are code constants
(`SHOW_T`, `STRUCK_T`, `DIZZY_T`, `ANGRY_T`) and neither needs art to change —
but both are exactly where new art would pay for itself, because they are
already reserved, uninterrupted screen time.

---

## 3. Arena use — the ring is about three times bigger than the fight

| | median | of |
|---|---|---|
| Cells the **boss** ever occupies | **33%** | 52 reachable cells |
| Cells **Roshan** ever occupies | **46%** | 52 reachable cells |
| Boss max radius reached | 19.6 | apothem 24.0 |
| Roshan max radius reached | 23.0 | apothem 24.0 |

Two thirds of the octagon floor never has the boss on it. The fight happens in
the middle third, and the child orbits a little wider. The eight wall panels,
eight corner posts, four crates and four dust mounds are dressing for a room
the fight does not visit.

This is not an argument for shrinking the ring — a convex arena that always
lets a dragged finger make progress is worth keeping. It is an argument for
**spending the art budget on what is actually on screen** (the back of the
room, the deck under the middle third, the boss's own nest) rather than on
eight identical rim segments.

---

## 4. Staging — measured at the instant she must read the tell

| | value |
|---|---|
| Boss card height | **172 px** (24% of a 720-tall phone) |
| Readable bunny inside the card (~0.6 of it) | **≈103 px** (14%) |
| Share of the frame the boss covers | **2.0%** |
| Tell inside the 6% safe area | **126 / 126 windows** |
| Boss body cropped | **0 / 126** |
| Roshan↔boss on-screen distance | 46 px |
| **Prop directly behind the boss** | **126 / 126 windows (100%)** — crates 95, mounds 30, nest 1 |

Two of these are good news and should be protected: the camera solve works —
nothing is cropped, the tell always clears the safe area — and the boss leaps
*at* Roshan, so the pair are 46 px apart when the window opens. She never has
to look in two places.

The rest is the finding. **The thing she must read is 2% of the phone, and
100% of the time it is drawn against a pastel prop of the same hue and the
same soft-blob shape family.** There is no clean silhouette anywhere in the
ring at the only moment legibility matters.

---

## 5. What the ten captured frames show

Reviewed: showing rise, demo flash, shielded hop, wind-up, **window open**,
struck/dizzy, dizzy prowl, angry prowl, angry window, befriending.

1. **There is no attic.** The octagon is a lavender slab floating in flat pink
   void. No wall, no ceiling, no window, no horizon. ~40–45% of every frame is
   empty background. The fiction — *the biggest dust bunny in the Pearl Castle
   attic, on the nest where he hoarded the castle's shine* — is not on screen
   in any form.
2. **The message banner sits on the boss.** In the angry-prowl frame it clips
   him across the middle; in the window-open frame it cuts his lower body; in
   the befriending frame the implosion is squeezed into the strip above it.
   The banner occupies the horizontal band the fight happens in.
3. **Roshan is not in a single one of the ten frames.** The child cannot see
   herself in her own boss fight.
4. **No health pips.** `_update_hud()` writes `⭐ TAP NOW! 💜💜💜` to
   `hud_game`, and it does not appear anywhere in any frame. She has no way to
   know she is two thirds of the way through.
5. **The scenery does not read as objects.** Crates and dust mounds are the
   same value and hue as the deck; they render as pale smudges on the floor.
   The nest — the whole reason the room exists — is invisible behind him.
6. **The contact shadow is a hard-edged navy quad.** Under the angry boss it
   reads as a rectangular hole in the floor, not a shadow.
7. **The tell is the generic reward star** (`assets/mg/star.png`). The
   authored `boss_tell_open.png` / `boss_tell_shielded.png` requested on
   2026-08-02 never landed, so open and shielded are the *same object at two
   alphas* — precisely what that handoff said must not happen. The same star
   means "you won a sticker" everywhere else in the game.
8. **The lamp beads bloom to white blobs**, and the painted wood-plank floor
   outside the octagon is drawn in a far more detailed language than the flat
   lavender platform on top of it. Two rooms, one frame.

The boss art itself is excellent and is not the problem — the jump, laugh,
flinch, angry and implode sheets all read beautifully. He is a good character
standing in an unbuilt room.

---

## 6. What this asks for

**Art** — `CODEX_BOSS_STAGE_HANDOFF_2026-08-03.md`, which this report is the
evidence for: the attic itself, a deck that is a floor, scenery with a value
contract that separates it from the boss, the two tell badges that are still
outstanding, a real soft shadow, and the beat-filling props that give the 36%
prowl and the 15% struck hold something to be about.

**Engineering** (not Codex work, listed here so it is not lost):

| # | finding | fix |
|---|---|---|
| E1 | Banner covers the boss and the arena's action band | give the boss arena a top-anchored banner slot, or fade the banner during `vuln` |
| E2 | Roshan absent from all ten frames | frame check for the player in `fit_camera`, the same way the boss's leap apex is checked |
| E3 | `hud_game` pips never appear in the arena | the arena hides `hud_layer`; the boss needs its own pip row |
| E4 | 7.0 s fixed `struck` hold, 15% of the fight | scale the hold with how the fight is going, or fill it (see art §7) |
| E5 | Fight is under band (15/24) | `SHOW_T` on repeat visits, and/or a fourth round once she is winning fast |
| E6 | Contact shadow is a hard quad | soft radial alpha, same treatment as `OctagonStage.glow()` |
