# Dust Bunny Boss — stress test, timing audit and fun-factor review (2026-08-02)

The game's **first boss**, stress-tested end to end: 25 simulated-child
encounters plus 5 control extremes on a new generic octagon arena, a visual
capture pass, and an audit of both the encounter and the process that built
it.

Everything below is measured, not estimated. Raw output:
`scripts/probe_dust_boss_balance.gd` (advisory), reference frames from
`scripts/probe_dust_boss_shots.gd`.

> **SUPERSEDED IN PART — see §8.** The encounter has since been composed with
> `DustBunnyBossSprite` (the authored art and the owner's three-taps-per-window
> contract). §1.1 and §1.3 are the *before* measurements; §8 is the after, and
> the headline finding — mashing equals reading — is now closed.
>
> **Art note (historic).** The boss cutout used throughout this test was a **placeholder**
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

## 6b. Second pass — five more defects, found by the review panel

The adversarial review of the audit itself surfaced five defects the first
pass missed. Four are fixed; all were verified in code before acting on them.

### D1. Nine voice events fired **twice** — FIXED
`show_msg()` already calls `_say(speaker, vo)` itself
(`audio_director.gd:60-64`), so every `show_msg(...)` + `_say(...)` pair in the
encounter was two triggers on the same beat, and `_land_hit` added a third
(`m.voice.play()`). Today they all collapse into one fallback noise; the moment
real clips land they would have spoken over each other on two players. Every
beat now passes its event name as the `vo` argument — one trigger, one voice.

### D2. Winning the game's first boss earned no medal — FIXED
`MEDALS.md` is binding: *"Bronze = completion. Every finished game earns at
least bronze."* `MedalSystem.TIERS` had no `dustboss` row, so the boss was the
only content in the game that could not be ranked. It now ranks on **wasted
taps** — taps thrown while he was shielded and the fight was live — which is
the axis §4.1 argued for, and the measured set confirms it discriminates the
right behaviour:

| Tier | Rule | Measured |
| --- | --- | --- |
| gold | 0 wasted | 1/25 — **0 of 5 mashers** |
| silver | ≤2 wasted | 9/25 — **0 of 5 mashers** |
| bronze | won | 25/25 |

The counter deliberately does **not** tick during the showing, the hit reaction
or the befriending: the teaching beat and the celebration must never cost her a
tier. (`dust_boss_fr["won"]` is left `true` on purpose — flipping it routes
into `_add_won_star`, which dereferences a `"node"` key this fr does not have.)

### D3. The button said "JUMP" in a fight whose only verb is a bonk — FIXED
The shared reef action button defaults to `JUMP` with an up-arrow pictogram and
had no `dustboss` arm. It now reads **BONK!** while he is open and **WAIT**
while he is shut, through the same `action_label()` seam kart and the promenade
already use. Asserted in the probe on both sides of the window.

### D4. The same tap had two different answers — FIXED
The action button was never passed into `showing`, `struck` or `friends`, so
pressing it there did *nothing*; but a tap on the **screen** in those same
states ran the full shield answer and could print *"Too puffy! Wait for him to
JUMP and FLASH!"* over the teaching line itself, and over *"BONK! He is all
DIZZY"*. Both paths now give the same sparkle-only answer in those three
states — never silent, never scolding — and damage still exists only in
`_tick_vuln`.

### D5. Dead exit line — LEFT AS IS
`_fail_line()` has no callers repo-wide, so the boss's entry there is
unreachable. Harmless; noted because it means there is no in-fiction way *out*
of the fight (§3.6).

> **Note on the numbers after this pass.** Removing the stray
> `m.voice.play()` also removed a `randf()` call, which re-aligns the shared
> RNG stream — so the re-run reports median 26.1 s rather than 29.3 s. That is
> seed drift, not an improvement: the floor (22.7 s), the mash-equals-read
> result and the in-band count (3/25) are unchanged in substance.

---

## 7. What changed in the code tonight

| Change | Why |
| --- | --- |
| `scripts/games/octagon_stage.gd` (new) | The generic octagon arena the repo lacked; solved framing; true octagon containment |
| `scripts/games/dust_boss.gd` | Ported to the octagon (AI unchanged); ground shadow fixed; `on_world_tap` added |
| `scripts/player.gd` | `dustboss` added to the camera-ownership list (§3.1) |
| `scripts/main.gd` | World taps during the boss fight route to the boss (§3.3) |
| `scripts/probe_dust_boss.gd` | +6 camera-contract checks, +world-tap, +pose map, +button label, +medal (now 48) |
| `scripts/medal_system.gd`, `scripts/probe_rank.gd` | the boss's medal row and its tier-math cases |
| `scripts/touch_ui.gd` | BONK!/WAIT pictograms |
| `scripts/probe_dust_boss_balance.gd` (new) | The 25-encounter persona playtest and its control extremes |
| `scripts/probe_dust_boss_shots.gd` (new) | The 10-frame visual capture pass |

The AI itself — states, timings, phases, mercy — is **unchanged**, so every
number in this document describes the boss as it stands today. All tuning
proposals in §4 are deliberately left unapplied: they are the owner's call.


---

## 8. After the composition (2026-08-02, later)

The two halves were composed on the owner's instruction:
`DustBunnyBossSprite` now owns the damage core — **three rounds of three quick
taps**, a 0.75 s window (0.65 s in the final round), 1.25× action speed once two
rounds are down, the flinch chain and the implosion — while this file keeps the
octagon arena, the travel, the showing, the mercy ramp, the medal, the framing
and the ending. Same 25 personas, same harness, same seeds.

### The headline finding is closed

| Control | Before (1 tap / 2.6 s) | After (3 taps / 0.75 s) |
| --- | ---: | ---: |
| `robot` — perfect play | 22.5 s | 23.5 s |
| `blind` — **never looks at the star** | 23.3 s (**+3.6 %**) | 31.5 s (**+34 %**) |
| `masher` ×5 median | 23.3 s | 34.7 s |
| `speedy` ×5 median | 24.7 s | 25.3 s |

Ignoring the tell used to cost 0.8 s. It now costs **8 s and a third of the
fight**, because three taps inside 0.75 s must be *aimed at the window* — a
continuous drum no longer suffices. Watching is now the fast way to play.

### The rest of the measured set

| | Before | After |
| --- | ---: | ---: |
| Fight length, median | 29.3 s | **40.2 s** |
| In the 45–120 s band | 2/25 | **12/25** |
| Window conversion | 78.1 % | **56.0 %** |
| Mercy steps used, mean | 0.84 | **2.36** |
| Taps per fight, mean | 15.9 | **28.4** |
| Agency density, median | ~19 % | **26 %** |

Conversion falling is the point: a window is now something you can *miss*,
which is what makes landing one mean anything. The mercy ramp went from
decorative to load-bearing — the median child now uses it twice per fight, and
it is what keeps a missed window costless.

### One regression found and fixed in the same pass

The `slowpoke` control (4 s reaction, 4 s gawk) went from 104 s to **229.6 s**:
three taps inside even a mercy-stretched 2.25 s window is out of reach for that
hand, so she simply collected windows. A longer window cannot fix a slow hand.

So deep mercy now also **gives her taps**: after 4 missed windows the fight
lands the first tap of each window for her, after 8 the second — capped so a
round can never complete itself. The window she finally reads needs only one
real tap. Slowpoke: **229.6 s → 132.3 s**, and every other control is
unchanged (robot 23.5 s, blind 31.5 s, rooted 31.8 s) because the ramp does not
engage until the fourth miss.

### Still open after the composition

- **The unattended fight still never ends** (`asleep`: 35 windows, 300 s cap).
- **The nine voice clips still do not exist**, so the rule still reaches a
  non-reader as text (the art now carries dizzy and angry unaided, which is a
  real improvement, but "tap three times, fast" is not yet sayable in pictures).
- **The arena is still primitives** and the message banner still sits where
  Roshan stands.
- Fight length is now *inside* the band for half the personas; the slowest tail
  (132 s) sits above it. That is the price of the no-fail guarantee and looks
  like the right trade.
