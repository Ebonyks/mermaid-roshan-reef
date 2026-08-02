# Dust Bunny Boss — stress test, timing audit and fun-factor review (2026-08-02)

The game's **first boss**, stress-tested end to end: 25 simulated-child
encounters plus 5 control extremes on a new generic octagon arena, a visual
capture pass, and an audit of both the encounter and the process that built
it.

Everything below is measured, not estimated. Raw output:
`scripts/probe_dust_boss_balance.gd` (advisory), reference frames from
`scripts/probe_dust_boss_shots.gd`.

> **Art note.** The boss cutout used throughout this test is a **placeholder**
> — `dust_bunny_curl_ears.png` is a regular cast member, and no boss-scale dust
> bunny exists in this repository (see `DUST_BUNNY_BOSS_2026-08-02.md` §0). The
> real art is on the owner's machine and has not landed yet. Every measurement
> below is about **behaviour, timing and framing**, none of which depends on
> which cutout is drawn — the audit stands unchanged when the art is swapped,
> and the capture pass should simply be re-run to re-review legibility.

---

## 0. What was run

| Piece | What it does |
| --- | --- |
| `scripts/games/octagon_stage.gd` | **New.** The generic octagonal boss arena — the repo had none (see §1) |
| `scripts/games/dust_boss.gd` | The boss, ported onto it. AI unchanged; all 33 contract checks still pass |
| `scripts/probe_dust_boss_balance.gd` | 25 persona encounters + 5 control extremes, fixed 0.05 s timestep, real `touch_ui` taps |
| `scripts/probe_dust_boss_shots.gd` | 10 rendered frames, one per beat, mobile renderer at 1280×720 |
| `scripts/probe_dust_boss.gd` | The contract probe, now also asserting the **camera contract** (§3.1) |

**There was no generic octagonal stage to reuse.** `combat_arena.gd`,
`dungeon_puzzle_room.gd` and `stuffie_battle.gd` each carry their own copy of
the same overhead ring, and all three clamp with a **circle**, not an octagon
(`flat.length() > RADIUS - 3.0`, three times over). The arena *art*
(`dungeon_arena.glb`) is a 32-gon disc of radius 27 with 8 wall runs. So
`OctagonStage` is the first true octagon containment in the codebase — eight
half-planes, two passes, analytic and allocation-free — and the first arena rig
a Family-A satellite can actually reuse.

### The personas

Five archetypes × five variations, calibrated to a 3–5 year old on a phone:
`reaction` (seconds from the star lighting up to the finger landing), `err`
(wrong-moment taps), `speed` (fraction of full stick deflection actually
held), `wander`, `gawk` (seconds frozen watching her own sparkles), `mash`
(taps/second thrown regardless). Controls: **asleep** (no input), **blind**
(never looks at the star, mashes 2/s), **robot** (0.15 s reaction), **slowpoke**
(4 s reaction, 4 s gawk), **rooted** (never moves).

---

## 1. The three findings that matter

### 1.1 Mashing is exactly as good as reading the tell — the icon is decorative

| Control | Behaviour | Fight |
| --- | --- | ---: |
| `robot` | perfect, 0.15 s reaction, watches the star | **22.5 s** |
| `blind` | **never looks at the star**, taps 2×/s | **23.3 s** |
| `masher` ×5 | 48 taps/fight, 85 % of them thrown while he is shielded | **23.3 s** (median) |
| `speedy` ×5 | watches, reacts in ~0.7 s | **24.7 s** (median) |

A player who never once looks at the icon finishes **0.8 s (3.6 %) behind a
perfect player**, and *faster* than every casual, wander and timid run. The
fight's entire lesson — wait, watch, then tap — is unenforced. 67 % of all
taps across 25 runs (265 of 396) were thrown while he was shielded and cost
nothing whatsoever.

This is not a tuning problem. The model in
`scratchpad/tune_model.py` sweeps every timing candidate (shorter holds,
fake-out leaps, tighter windows, 5 HP) and the mash-vs-read ratio stays
**0.93–0.96 in every one** — mashing wins under all of them. Only a *soft cost
for a wrong tap* or a *differential reward for a clean one* changes it (§4.1).

### 1.2 The encounter is a fixed-length ride, not a fight

Median encounter: **33.5 s total, 29.3 s of "fight"**. Of that, the states
that can accept a meaningful input total **~6 s**; the rest is on a timer no
player can touch:

| State | Median seconds | Player agency |
| --- | ---: | --- |
| showing | 6.3 | none by design |
| prowl | 12.4 | none (taps bounce) |
| wind-up | 2.8 | none |
| **vulnerable** | **6.1** | **the whole game** |
| struck | 7.0 | none |

`prowl` totals 12.4 s and `struck` exactly 7.0 s in *every* run because both
are fixed holds. The `rooted` control — stick never moved — wins in 24.8 s
with 3/3 windows: **movement is optional too**, because he leaps to her (91 %
of windows opened with her already in reach).

### 1.3 25 of 25 encounters finished below the design floor

Median fight 29.3 s against a 45–120 s band; **2 of 25 in band**, both
outliers (a timid child at 65.5 s and one at 56.9 s). For comparison the
repo's own opera acts target 120–240 s. The first boss in the game is
currently shorter than the walk to it.

---

## 2. Timing-window analysis

| Phase | Window | Prowl before it | Conversion (measured) |
| --- | ---: | ---: | ---: |
| puffy (0 hits) | 2.6 s | 3.4 s | ~93 % |
| dizzy (1 hit) | 3.2 s | 4.0 s | ~93 % |
| angry (2 hits) | 2.1 s | 2.4 s | ~76 % |

Overall conversion **78.1 %** (75 hits / 96 windows). Window length is
essentially the only variable that decides conversion: **≈15 percentage points
per second** of window across the measured range. The fight puts its *shortest*
window last, where it absorbs most of the misses — which is defensible as
escalation, and is exactly the owner's spec.

Measured reaction latency (star-on → landing tap), median by archetype:
speedy 0.70 s, casual 1.40 s, wander 2.05 s, timid 2.45 s, masher 0.50 s. So
the 2.6 s opening window forgives every archetype; the 2.1 s angry window is
the only one that ever bites.

**The tell is redundant with the leap.** `_tick_vuln` sets `db_flash = 1.0`
for the whole window and nothing else in the fight puts him above ~2.4 units,
so "he is high in the air" and "the star is flashing" are the same event. A
child can ignore the icon completely and read the jump — which is what the
blind control does.

---

## 3. Defects found (and what was done about them)

These are cases where the encounter did not do what it claimed. **All four
were invisible to the entire probe suite**, which was green throughout.

### 3.1 The camera never belonged to the arena — FIXED

`scripts/player.gd:560` carries a hard-coded list of game ids that own the
player and camera (`slide, fairyshoot, kart, galaxy, combat, stuffie, dungeon,
dolls, brawl`). `dustboss` was not in it, so the free-swim chase camera
re-aimed the lens every frame, *after* the stage had framed the ring. The
first capture pass shows the result: the boss cropped into a corner of a
lavender void, the tell off-screen entirely.

Fixed by adding `dustboss` to the list, with a comment naming the failure mode
for the next mode that lands.

### 3.2 The action was framed off the bottom of the phone — FIXED

Even with the camera restored, Roshan projected to **y = 975 on a 1280×720
canvas** — 255 px below the screen — and the star above the boss's head was
cropped off the top. `OctagonStage.fit_camera()` now *solves* the framing
against the real projection: it pushes the lens back until the near rim, the
far rim and the apex of a leap plus its icon are all inside a 6 % safe area,
then `frame_camera()` re-asserts that pose every tick.

`probe_dust_boss.gd` now asserts all four of those points plus "the arena
keeps the camera while the fight runs" — so this class of bug cannot ship
again silently.

### 3.3 Tapping the boss did nothing in Hybrid touch — FIXED

World taps route hit-engine → `CombatArena` → interaction director. The boss
registers neither, so on the phone the most natural act a 4-year-old can
perform — **tapping the big fluffy thing** — fell through to tap-to-swim and
produced nothing. Only the button (labelled **"JUMP"**, §5.3) actually bonked
him.

`DustBossGame.on_world_tap()` now takes the tap, and is *more* generous than
the button: a tap that visibly lands on his card counts as in-reach however
far away she is standing. Asserted in the probe.

### 3.4 The airborne shadow flew with the boss — FIXED

The contact shadow was parented to the boss, so it rose with him and an
airborne leap read exactly like a ground hop. It now stays on the deck and
shrinks and fades with height — the standard way "he is UP THERE" is
communicated without words.

### 3.5 Nine voice events, zero audio — OPEN (owner decision)

`_say("roshan", "dustboss_show" | "_tell" | "_leap" | "_dizzy" | "_hit" |
"_angry" | "_again" | "_win" | "_closer")` — **none of these clips exist**, so
every one falls through to the generic pitched "yay". The rule, the
reassurance after a missed window, and both phase changes therefore reach a
non-reading child as **on-screen text only**, which is the one thing CLAUDE.md
forbids. Two ways out, and this is the owner's call:

1. record nine short family lines (the project's normal path), or
2. carry the same information in **pictograms** — see the Codex handoff
   (`CODEX_BOSS_ART_HANDOFF_2026-08-02.md` §3), which specifies them.

### 3.6 An unattended fight never ends — OPEN (owner decision)

The `asleep` control ran the full 300 s cap: **33 windows offered, 0 hits,
mercy pegged at 33**, and the encounter simply loops. That is correct
"no fail state" behaviour and it is also a phone left on a car seat. The mercy
ramp caps at +2.2 s window / +6 reach / −40 % speed and then stops helping.
Options: let the mercy ramp continue past its caps until the window is
effectively permanent; or after N unanswered windows have Grand Puff flop over
laughing and befriend himself (a win she did not have to earn, which this game
already does elsewhere). Recommend the latter — it ends the session kindly.

---

## 4. Fun-factor audit — what would actually make this better for her

Ranked. Everything here respects the hard rules: no fail states, nothing that
can be lost, nothing that needs reading.

### 4.1 Make reading the tell *pay*, without making mashing *hurt* — highest value

The data is unambiguous that mashing is optimal, and the model shows no timing
change fixes it. Two levers:

- **Reward, not punishment (recommended).** The repo already has the
  mechanism: `MedalSystem` has **no case for this boss at all**
  (`medal_system.gd:110-129`), so the first boss in the game is the only
  content that cannot be ranked. Rank it on *wasted taps*, which the measured
  data shows discriminates exactly the right way:

  | Tier | Rule | Achieved by |
  | --- | --- | --- |
  | gold | 0 taps while shielded | 2/25 runs — **0/5 mashers** |
  | silver | ≤2 wasted | 9/25 — **0/5 mashers** |
  | bronze | won | 25/25 |

  Note the trap this avoids: a *fast-hit* bonus would reward the wrong
  children — mashers' median latency is 0.50 s and the blind control's is
  0.50 s, while genuine watchers sit at 0.65–0.80 s. **A speed bonus is a mash
  detector.** Wasted-tap tiers are the opposite.

- **A soft, comic cost (owner's call).** A wasted tap makes him inflate and
  re-settle (+0.8 s before the next window). Modelled: the reading player's
  fight is unchanged at 23.2 s while the masher's goes to 40.6 s — a 1.75×
  gap, with no fail state and no lost progress. It only lands on the
  behaviour being discouraged. Risk: a child who mashes *because she is
  excited* gets a longer fight without understanding why, so it only works if
  the re-settle is **funny and legible** (an art dependency — see the handoff).

### 4.2 Give the 19 non-interactive seconds something to do

83 % of the encounter is a timer. The cheapest honest fix is not to shorten
the holds (the reviewers were right that the hit reaction *is* the payoff —
it is where the bonk is celebrated) but to **give the prowl a small verb that
cannot affect the outcome**: dust motes he kicks up that pop for sparkles.
Caution from the review: keep the prowl longer than the window, or the fight
stops being about waiting. Suggested budget: 2 motes per prowl, purely
cosmetic, no timing effect.

### 4.3 Make the icon carry information the jump does not

Right now airborne ⇔ flashing. The owner's spec is "airborne **and**
flashing", which only becomes a real condition if he sometimes leaps
**without** the star. One or two fake-out leaps per phase would make the icon
load-bearing and add drama — but note the measured consequence: fake-outs add
~7 s to the encounter and do **not** close the mash gap on their own. Pair
with 4.1 or it changes nothing.

### 4.4 Let the showing shorten on replay

6.3 s of un-skippable reveal every single time; a 4-year-old replays a
favourite 5–10 times a session. The review is right that the demo flash must
survive (it is the only teaching moment) — so keep the flash, drop the swell
and the parade hop on replays behind a saved `dustboss_seen` flag. Saves ~3 s
per replay without deleting the lesson.

### 4.5 Put Roshan back in her own boss fight

In every captured frame the message banner sits exactly where she stands, so
the hero is not visible during her own fight. Move the banner to the top of
the frame or make it a corner card (§5 of the handoff).

### 4.6 Rejected after review — recorded so they are not re-proposed

| Proposal | Why it was dropped |
| --- | --- |
| Raise every `window_t` | `glide` is computed from `win` (`dust_boss.gd:214`), so a longer window makes him *drift away more slowly* — the "free" allowance is not free |
| Widen the glimmer to 0.80 | The shielded star would reach alpha 0.70 against the open star's strobe trough of 0.55 — the tell would read *brighter while shielded* |
| Fast-hit (`SNAP_T`) bonus | Rewards mashers (0.50 s) over watchers (0.65–0.80 s) — see 4.1 |
| Halve the hit-reaction holds | That hold *is* the celebration; cutting it removes the payoff the fight is built to deliver |
| Cut the demo flash from the showing | It is the only place the rule is taught |
| A "dust storm" projectile phase | Contradicts the codex canon quoted in the character sheet: dust bunnies are *friendly helpers, not pests or monsters* |
| Gate `MERCY_SLOW` by phase | The claimed escalation inversion needs 8 missed windows; the worst real persona reached 4 |

---

## 5. Combat-system findings beyond this boss

1. **`HitEngine` is bypassed.** The boss does its own distance check, so it
   inherits none of the shared tap routing, feedback or probe surface, and the
   "enemies are always in the forefront" rule did not apply to it (§3.3 was
   the symptom). Any future boss should either use `HitEngine` or explicitly
   document why not.
2. **There is no boss template.** Telegraph → window → phases → mercy →
   showing → defeat-as-friendship is a shape every future boss will want.
   `OctagonStage` is the arena half; the encounter half should be extracted
   from `dust_boss.gd` once a second boss exists (extract, don't rewrite).
3. **The action button says "JUMP"** in a fight whose only verb is a bonk.
   It is the shared reef control label; a mode should be able to relabel it.
4. **Three arena rigs are still duplicated.** `combat_arena`,
   `dungeon_puzzle_room` and `stuffie_battle` can migrate onto `OctagonStage`
   one at a time, probe-gated — each migration deletes a copy of the same
   camera, clamp and input code.

---

## 6. Process audit — the stress test itself

**The headline process finding: the entire trusted probe suite was green while
the encounter was visually broken in three separate ways.** Behaviour probes
verify that the game *is* winnable; nothing verified that it was *watchable*.

What the persona harness cannot see, and what should cover it:

| Blind spot | Cover it with |
| --- | --- |
| Camera framing, cropping, safe area | The new `_framing_case()` assertions — cheap, headless, deterministic |
| What the screen actually looks like | `probe_dust_boss_shots.gd` under xvfb, as an advisory capture step |
| Whether voice lines exist | A one-line audit: every `_say()` event a mode uses must resolve to a file, or be listed as a known gap |
| Legibility (contrast, silhouette, overlap) | Human review of the captures — the audit tool cannot judge this |
| Frame pacing on the real phone | Nothing currently; the APK on the device is the only truth |

Harness blind spots worth naming: it models the child's *reaction*, not her
*comprehension* (a child who does not understand the rule is modelled as one
with a slow reaction); it cannot tell frustration from patience; and it
reports a healthy encounter for a fight nobody could see. Its most valuable
property is that it asked one falsifying question — *does never looking at the
star still win?* — and answered it with a number.

**Recommended standard for every future boss**: contract probe (behaviour) +
framing assertions (camera) + persona playtest (balance, advisory) + capture
pass (visual, advisory) + a voice-coverage check. Four of the five now exist
and are wired up; the fifth is one grep.

**Weakest link in tonight's process**: the balance harness is advisory and
prints no failure token, so — as the process lens put it — the run that proved
mashing beats watching was labelled `quick` and nothing in the repo could act
on it. Advisory output only works if a human reads it; this document is that
read.

---

## 7. What changed in the code tonight

| Change | Why |
| --- | --- |
| `scripts/games/octagon_stage.gd` (new) | The generic octagon arena the repo lacked; solved framing; true octagon containment |
| `scripts/games/dust_boss.gd` | Ported to the octagon (AI unchanged); ground shadow fixed; `on_world_tap` added |
| `scripts/player.gd` | `dustboss` added to the camera-ownership list (§3.1) |
| `scripts/main.gd` | World taps during the boss fight route to the boss (§3.3) |
| `scripts/probe_dust_boss.gd` | +6 camera-contract checks, +1 world-tap check (now 40) |
| `scripts/probe_dust_boss_balance.gd` (new) | The 25-encounter persona playtest and its control extremes |
| `scripts/probe_dust_boss_shots.gd` (new) | The 10-frame visual capture pass |

The AI itself — states, timings, phases, mercy — is **unchanged**, so every
number in this document describes the boss as it stands today. All tuning
proposals in §4 are deliberately left unapplied: they are the owner's call.
