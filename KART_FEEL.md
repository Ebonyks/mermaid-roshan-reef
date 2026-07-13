# KART FEEL — comparative audit of the race engine (`scripts/kart.gd`)
# Companion files: scripts/probe_kart_feel.gd (telemetry harness, in the CI gate)
# Method: the same rubric RACE_FEEL_WORKORDER.md applied to the slide racer,
# re-aimed at the kart engine and benchmarked against kart-class references.

## What kart-class games actually do (the reference model)

Every beloved arcade kart racer — Mario Kart 8 Deluxe, Crash Team Racing,
Diddy Kong Racing, the Beach Buggy line on mobile — is built on the same five
pillars, whatever the physics under the hood:

1. **Drift + mini-turbo is the core verb.** Steering hard into a bend enters a
   drift state that *holds an arc* (it never feeds raw inward velocity); holding
   it charges visible tiers (MK8's blue → orange → pink sparks; CTR's three
   turbo pips), and releasing pays out boost. This is the entire skill ceiling:
   lap time comes from cornering craft, not reflexes.
2. **The racing line is physically real.** The inside of a bend is a shorter
   arc, so line choice changes lap time even without drift. AI visibly dives
   for apexes, which *teaches* the line by demonstration.
3. **The assist floor is separate from the skill ceiling.** MK8D's auto-
   accelerate + smart steering let a four-year-old finish every race; none of it
   caps what a skilled thumb can do. Assists shape the floor, never the ceiling.
4. **Speed is a continuous perceptual channel.** FOV widens with speed (not
   just on boost), the camera pulls back, near-field particles stream past,
   engine pitch rises. Boost then *kicks* on top of an already-breathing system.
5. **Contact is drama, and payoffs are ceremony.** Bumps thump, squash and
   shake; boosts flash and chime; a rocket start rewards being ready at GO.

## Audit: this engine against that model (before this pass)

Strong already — the 225-race sim campaign bought real feel:
- ✔ Distinct vehicle identities (speed/steer/slip/mass/wall) that matter.
- ✔ Mass-weighted bumper physics with squash, hop, shake, thunk, voice.
- ✔ Turbo meter + player-timed release (agency), pickups as the economy.
- ✔ Rubber-band tuned for "losing stays close, winning stays possible".
- ✔ Touch co-pilot + pickup magnet (platform fairness, sim-measured).
- ✔ Countdown, podium, payout ceremony; banked corners; variable width.

Gaps, ranked by feel impact (each mirrors a slide-audit root cause):

| # | Finding | Evidence (pre-change) | Kart-class reference |
|---|---------|----------------------|---------------------|
| F1 | **The racing line was cosmetic.** `k["s"] += speed * delta` had no lat term: inside line, outside line and no-input all posted identical lap times. `lat` only mattered for pickups and walls. | `_update_player`/`_update_ai` progress lines | Inside arc IS shorter; line choice changes lap time |
| F2 | **No drift system — the core kart verb was missing.** Per-vehicle `slip` smoothed steering response but there was no drift state, no charge tiers, no release payoff. Skill ceiling = turbo timing only. | no drift state existed | MK/CTR drift: hold-arc, tiered sparks, release boost |
| F3 | **Speed read as boost on/off, not continuous.** FOV 68 flat, snapping to 76 only while turbo burned; camera distance likewise binary; zero near-field optic flow in the air beside the road. | `_update_camera` pre-change | FOV + pull-back mapped to speed, streak particles |
| F4 | **Linear acceleration ramp.** `move_toward(speed, target, 40)` — the same pull at 5 % speed as at 95 %, so launches read sluggish. | accel constant | Fat low-end torque, soft top-end approach |
| F5 | **No slipstream.** The pack-presence AI puts rivals on screen, but tucking in behind one did nothing — pack racing had presence, not physics. | no draft check | Draft tow + charge while in the tow |
| F6 | **No ready-at-GO reward.** The countdown was pure wait. | countdown block | Rocket start for input held at GO |
| F7 | **Frame-pacing risk on the target phone.** `_pos_at` was an O(n) linear walk over 260 samples, called dozens of times per frame for 8 karts — and feel work adds more callers. Frame hitches ARE feel. | `_pos_at` while-loop | O(log n) lookup |

Steering response itself was already right (snappy latv lerp, per-vehicle rates,
visual nose-yaw + lean) — untouched, per the workorder rule: don't tune what
isn't failing.

## What was implemented (this pass)

- **F1 → curvature-coupled progress.** `_advance()` scales progress by
  `1 - lat·κ` (capped ±18 %), with κ from a precomputed signed-curvature table
  (travel-frame, reverse-lap aware). The inside line now genuinely shortens the
  lap; invisible, no reading, physically truthful. AI uses the same physics and
  gains an inside-line bias so the pack visibly dives for apexes (the rubber
  band keeps outcomes fair).
- **F2 → SPARKLE DRIFT.** Hold a hard steer (≥0.6) into a bend for 0.25 s:
  entry hop + chime, then the drift *holds the carve line for you* — it eases
  onto ~60 % of the way to the inside rail (lock-an-arc, the MK model; raw
  inward authority would grind the wall in half a second). Holding charges
  SILVER (0.8 s) → GOLD (1.6 s) → RAINBOW (2.4 s) with tier chimes and a
  persistent tail spray recolored per tier; release pays 0.55/0.95/1.4 s of
  turbo with squash + burst + "SPARKLE DRIFT!" flash. A wall scrape spills the
  charge — the drift lesson, and the only penalty (no spin-out, ever). Zero
  input still finishes every race: the floor is untouched, the ceiling is new.
- **F3 → continuous speed channel.** FOV = 62 + 14·(speed/1.5vmax) + 4 boost
  kick; camera distance scales with the same term; horizon rolls ±0.10 rad into
  the carve; thin streak particles stream past the lens above ~62 % speed or on
  boost (halved amount on the Speedy tier; CPUParticles, unshaded, no lights).
- **F4 → launch punch.** Acceleration ×1.8 below 60 % of target speed.
- **F5 → slipstream.** Within 2.5–12 u behind a rival, |Δlat| < 2.6: +8 %
  target speed and a slow turbo-meter trickle while in the tow.
- **F6 → rocket start.** Any input held the instant GO fires → 0.9 s boost,
  chime, "ROCKET START!" — teachable purely by feel.
- **F7 → hot-path fix.** `_pos_at` is now a `bsearch` (O(log n)); curvature is
  a table lookup, so the new per-kart-per-frame physics costs ~nothing.

## Gates (probe_kart_feel.gd, runs in ci.sh + the probes workflow)

Steering is injected through the real touch path (`touch_ui.stick_vec`), solo
runs use a bare track (no pickups/shortcut) so the measurement is handling:

- assist floor: zero-input solo run finishes (hard FAIL otherwise)
- racing line: outside-line minus inside-line ≥ 0.3 s (expect ~1.5–4 s)
- skill ceiling: drift policy reaches tier ≥ 2 and beats no-input by ≥ 0.3 s
- speed channel: observed FOV range ≥ 8°
- integration: full-pack terrain race completes through the real glue;
  the ✕ quit restores the world

## Pass 2 — mobile-racer audit (owner playtest: "still feels bad, items don't work")

The right references for THIS game are the one-finger mobile racers, not
console MK: **Mario Kart Tour** (steering is the only input; acceleration,
items and ramp tricks are automatic or assisted) and **Beach Buggy Racing 2**
(huge readable powerups, constant engine audio, ramps everywhere). Against
those, the ranked gaps found in pass 2:

| # | Finding | Evidence | Mobile-racer reference |
|---|---------|----------|------------------------|
| F8 | **Bumps stole the player's boost.** `_resolve_collisions` set the lighter kart's `boost_t` to 0.1 on every contact — the bumper AI deliberately hunts the player's lane, so nearly every earned zip died within seconds. This alone explains "items don't work". | collision block | contact never cancels an active boost; it's drama, not punishment |
| F9 | **Half the items had no felt effect.** Shell/star only charged a meter at the bottom of the screen — an abstraction a 4-year-old never connects to the chime. Only bubbles produced a visible whoosh. A full meter could also sit unused forever if the tap never came. | `_check_pickups` | every pickup DOES something immediately; MK Tour fires stored items automatically when the player doesn't |
| F10 | **No jumps.** Flagged not-done in pass 1; never built. Air time + landing boost is a core mobile-racer beat (auto-trick ramps are MK Tour's signature moment for one-finger players). | no ramp/air code existed | ramps launch you automatically; landing pays a boost |
| F11 | **Total engine silence.** The race plays over music + occasional chimes; there is no continuous pitch-follows-speed layer, which is the single strongest subconscious speed cue. Blocked in pass 1 on an OGG asset — unblocked now via `AudioStreamGenerator` (procedural, no asset, no license line). | no engine audio path | constant engine loop, pitch mapped to speed |

## Pass 2 — what shipped

- **F8 →** a bump no longer strips the PLAYER's `boost_t` (rivals still lose
  theirs). The mass identity is untouched — she still gets shoved and slowed.
- **F9 →** every pickup now pays instantly: shell = 0.4 s zip + meter,
  star = 0.7 s zip + meter, bubble unchanged, rainbow = full meter AND an
  immediate full-length turbo ("RAINBOW POWER!"). Plus the MK-Tour assist:
  a meter that sits full for 2.5 s fires itself ("TURBO!" flash) — agency for
  the thumb that taps, a floor for the one that doesn't. Boost FOV kick
  raised so firing visibly stretches the screen.
- **F10 → JUMP RAMPS** (`ramps` in configure(), 3 per lap by default):
  golden glowing wedges on the racing line; driving one launches kart AND
  rivals into a 0.85 s arc (nose pitches up then down, "WHEEE!" flash for
  the player), and every clean landing pays a 0.5 s boost — the auto-trick.
  Steering authority halves mid-air (floaty, readable). No input required.
- **F11 → procedural engine hum**: `AudioStreamGenerator` putt-putt (soft
  saw + octave), pitch 58→208 Hz with speed + a boost bump, quiet (-18 dB)
  under the music. No asset, no ledger line. Skipped on the Speedy tier
  (per-frame buffer fill is CPU). **Verify on device** — crackle under
  frame drops would mean lowering the mix rate or gating it off.

## Not done (candidates for a later pass)

- AI drift sparks (teach-by-demonstration).
- Haptics: `Input.vibrate_handheld()` on bumps/drift release/landings (Android).
- A real recorded engine/wind OGG to replace the procedural hum if it
  reads as too "toy" on device.
