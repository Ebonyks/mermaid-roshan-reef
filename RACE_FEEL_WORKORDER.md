# RACE FEEL WORK ORDER — the slide racer (`game == "slide"`)
# Audit tool + measured diagnosis + iterate-until-green protocol for Claude Code.
# Companion files: scripts/probe_race_feel.gd (telemetry harness), feel_targets.json (rubric)

## Why it "feels bad" — measured, ranked

Live telemetry (Godot 4.4.1 headless, `--fixed-fps 60`, 9 instrumented runs across
both modes and 5 input policies) against kart-feel heuristics:

| # | Root cause | Measurement | Kart-class reference |
|---|-----------|-------------|---------------------|
| 1 | **Heading snaps at every track joint.** The chute is a 26-segment polyline (avg 9.6 m); tangent is constant per segment, so Roshan's yaw, her roll basis, AND the camera aim all step 4–6.5° instantaneously every 0.37 s at speed. | `yaw_jerk_max=6.53°/frame`, 20 snaps/run | Spline-continuous; heading is C1, snap ≈ 0 |
| 2 | **No driving system — the game runs on autopilot.** v is a scripted function of slope, clamped [13..26]; progress `ds = v·dt` has no x term, so the racing line is cosmetic: inside-line vs outside-line policies finish in an identical 10.63 s (`line_advantage=0.00`), and full-commit cornering gains 0.00 s over hands-off. | `speed_agency=0.000`, `line_advantage=0.00s`, `skill_time_delta=0.00s` | Drift is the core verb: steering into bends is a risk/reward speed system; line choice changes lap time; skill has a ceiling above the assist floor |
| 3 | **No perceived-speed cues.** Camera FOV is hard-coded 60° at all speeds (`player.gd:78`); no speed particles, no wind audio; non-track decor ≈ 6 objects/100 m (one cheering penguin every 40 m) so there's nothing streaming past to create optic flow. | FOV dynamic range = 0°, decor 5.6/100 m | FOV widens 10–15° with speed; dense near-field trackside detail |
| 4 | **Consequence-free walls.** Bank contact = silent `vx *= -0.3`. No sound, no shake, no haptic, no speed loss. | 0 feedback channels on bounce | Thump SFX + shake + speed penalty + recovery beat |
| 5 | **No ceremony.** `g["timer"]=-1` — no 3-2-1-GO; music is the reused 8.9 s fetch loop; the finish is a text message; total run 10.6 s, one S-curve shape, over before flow starts. | countdown=false, dur=10.6 s | Countdown, race music, finish-line celebration, 20–30 s+ of rhythm |
| 6 | **Dolly camera, not a chase cam.** Cam is glued to the track tangent; steering translates the sprite laterally on screen but the world never rotates or leans in response. | camera_responds_to_steering=false | Camera lags/leads into steer, rolls with lean |
| 7 | **Chase mode: decorative difficulty + the game's only fail state.** A noisy 300 ms-lag "toddler policy" wins 5/5 the instant the catch window opens (t≈6.6 s); yet missing at the bottom is a hard fail — the only one in the game. | winrate 5/5 @ 6.6 s; fail state present | Rubber-band tension without hard loss (this game's own no-fail principle) |

Steering response itself is **fine** (`latency63=0.28 s`, terminal lateral ≈ 9.9 m/s
vs 26 forward) — don't touch the steer constants; the problem is everything the
steering is embedded in.

---

## The audit tool

`scripts/probe_race_feel.gd` — run headless, no display:

```
$GODOT --headless --fixed-fps 60 -s scripts/probe_race_feel.gd
```

It executes 9 runs — fish mode under {no-input, bang-bang, reactive-seeker},
chase mode ×5 under a noisy toddler policy, chase ×1 under perfect play — plus a
static track-geometry pass, printing `FEEL|` lines and writing
`user://race_feel.json` for machine diffing between iterations. Input is injected
through the real touch path (`touch_ui.stick_vec`), so what it measures is what a
finger gets. Compare every metric against `feel_targets.json`: a tuning iteration
is **GREEN** only when all `must` bands pass and `probe_audit.gd` still passes
(no regression to the rest of the game).

**Protocol per iteration:** (1) change ONE subsystem below, (2) run the harness,
(3) paste the FEEL| block + which targets flipped, (4) commit only on
no-regression. Never tune two subsystems in one commit — feel changes interact.

---

## Fix plan (one phase per commit, in this order)

### R1 — Spline the track (kills root cause #1)
Replace per-segment sampling with Catmull–Rom interpolation in `_slide_sample`:
sample position via `Curve3D` (add points from the existing `path` array,
`bake_interval=1.0`) or hand-rolled Catmull–Rom over `path`; derive tangent by
central difference of two nearby samples (Δs=0.5 m), never from segment indices.
Keep the plank *visuals* as-is (26 boxes are fine to look at — raise N to 40 if
gaps show); only the motion/camera path becomes smooth.
**Gate:** `yaw_jerk_max < 1.0`, `yaw_snaps = 0`. Everything else unchanged.

### R2 — Speed as a reward channel (root cause #2)
Keep SLIDE_GRAV/FRICT as the passive baseline. Add:
- `g["boost"]` decaying at 3.5/s; effective speed `v_eff = v + boost`, allowed to
  exceed VMAX up to 38.
- **Boost rings**: 3 golden arches on the racing line (reuse `_halo` + torus mesh);
  passing within 3 m adds +9 boost, chime up-gliss, burst.
- **Fish give +4 boost** in fish mode (collecting now *feels* like something).
- **Wall hit: −20 % of v_eff** (floor at VMIN) — pairs with R4 feedback.
- Optional tuck: holding the action button adds +3 to gravity gain but widens
  steering damping (risk/reward a 4-yo can ignore).
**Gate:** `speed_agency > 0.5`, `speed_range_ratio > 2.3`, seeker still collects 5/5,
toddler chase winrate stays ≥ 0.6.

### R2.5 — SPARKLE DRIFT (the missing driving system)
Measured proof of autopilot: inside-line vs outside-line policies finish in an
identical 10.63 s (`line_advantage=0.00`), and a full-commit cornering policy
gains 0.00 s over no input. Lateral position is cosmetic; there is no driving
model, only a lane slider. The fix is a one-thumb drift system — the MK8 Deluxe
philosophy: the assist floor stays (zero input still finishes — correct for a
4-yo), skill raises the ceiling.

**A. Curvature-coupled progress (the racing line becomes real, zero UI):**
In `_tick_slide`, compute signed curvature κ(s) by central difference of
tangents (Δs = 3 m): `kappa = signf(t0.cross(t1).y) * angle_between / ds`.
Progress becomes `g["s"] += (v + boost) * (1.0 - clampf(x * kappa_lat, -0.22, 0.22)) * delta`
where `kappa_lat` is κ scaled so hugging the inside of the sharpest bend gains
~20 %. Invisible, no reading required, physically truthful (inside arc IS shorter).

**B. Drift state (single input — the thumb they're already using):**
- Entry: |steer| ≥ 0.6 with sign matching κ, sustained 0.25 s, |κ| above a
  bend threshold → `g["drift"] = true`.
- During: extra lateral pull toward the inside (+40 % steer authority inward
  only — carving); Roshan's model counter-rotates into the bend
  `yaw_visual = yaw + clampf(kappa_sign * 0.35, ...)` beyond her travel
  direction (the visual signature of drift); roll deepens; snow/rainbow spray
  `GPUParticles3D` at her tail; rising shimmer loop pitch-follows meter.
- Meter/tiers: 0.8 s → tier 1 SILVER (+5 boost), 1.6 s → tier 2 GOLD (+9),
  2.4 s → tier 3 RAINBOW (+14, holds, no overcharge penalty). Store
  `g["drift_tier"]`. Spark color on her tail per tier (her palette's answer
  to blue/orange/pink mini-turbos).
- Release (bend ends, κ sign flips, or steer released): add tier boost to
  `g["boost"]` (R2's decaying channel), tier-pitched chime, FOV kick, burst.
- **No spin-out, ever.** Sloppy exit into a wall gets the R4 thump — that IS
  the drift lesson, and it's gentle.
**C. Teach by demonstration:** on the first bend the baby penguin (chase) or a
cheering penguin (fish) visibly drifts with sparks — kids copy motion; optional
voice line "Lean into the turns for sparkles!" via `_say`.
**D. Chase integration:** penguin pacing keys off the player's v_eff so drifting
reads as visibly reeling him in; the R6 rescue beat remains the floor.
**Gate (harness measures all of these already):** `line_advantage ≥ 1.2 s`,
`skill_time_delta ≥ 2.0 s`, `drift_uptime` 3–8 s, drifter policy reaches
tier ≥ 2, no-input run still completes, toddler chase winrate stays in band.

### R3 — Perceived speed (root cause #3)
- FOV: `cam.fov = lerpf(cam.fov, remap(v_eff, 13, 38, 58, 72), 6*delta)` inside
  `_tick_slide` only; restore 60 in `_clear_game`.
- Speed streaks: one `GPUParticles3D` parented ahead of the camera, emitting
  short stretched quads streaming backward, `amount` scaled by v_eff (cap 40,
  respect the Speedy quality tier by halving).
- Decor density: place a trackside object every ~8 m alternating sides —
  candy-cane poles, ice crystals, flags, more penguins (reuse `_aq_game` +
  `_course_box`; rainbow theme gets the rainbow palette). Target ≥ 25/100 m
  of *non-track* decor. Keep each under ~200 tris; static, no lights.
- Wind loop: quiet whoosh AudioStreamPlayer, volume mapped to v_eff.
**Gate:** fov range ≥ 10°, decor ≥ 25/100 m, particles present; frame budget on
device is the human's call — flag if node count grows > +150.

### R4 — Walls that answer back (root cause #4)
On bounce: thump sound (Kenney impact pack, CC0), 0.15 s camera shake
(amplitude ∝ v_eff), snow/sparkle burst at contact, `Input.vibrate_handheld(60)`
(Android; wrap in OS.has_feature check), and the −20 % from R2.
**Gate:** feedback channels ≥ 3, penalty ≥ 10 %.

### R5 — Ceremony (root cause #5)
- Countdown: freeze `s` for 2.4 s at start; "3…2…1…GO!" as Label3D over the
  chute + three descending chimes and a high GO chime; release with a +6 boost
  ("rocket start") if the player is touching the stick when GO fires — teachable
  by feel alone, no reading.
- Lengthen the run to ~20 s: extend the path (z −180→200, two S-periods,
  a mid-run flat "breather" then a steeper final drop) — keep N proportional
  (~40 points) so avg segment stays ≤ 10 m for the visual planks.
- Race music: new slot (Phase 3 of the main upgrade script sources CC0; until
  then keep fetch but raise pitch_scale 1.06 during the slide as a placeholder).
- Finish: burst the existing confetti + 1.6 s result hold like the other games;
  in fish mode say the fish count out loud via `_say` if a voice line exists.
**Gate:** countdown=true, duration in [18,30], celebration hold ≥ 1.5 s.

### R6 — Chase mode: tension without failure (root cause #7)
- Widen the flee: penguin lateral speed 7.5 → 9.0 and gap curve
  `SLIDE_LEAD*(1.0-p)^0.8` so he stays ahead longer (tension), catch window
  opens in the final third.
- **Remove the fail state**: if `s >= total` uncaught, the baby penguin trips on
  a snow pile at the finish, giggles, and a short 6 s "second chance" chute
  section spawns where he's slow — the catch always lands, the win line varies
  ("You got him at the finish line!"). `_end_game(true, …)` always.
- Toddler-policy winrate target 0.6–0.9 on the *first* chute (so the rescue beat
  actually plays sometimes), 1.0 including the rescue.
**Gate:** no_fail=true; toddler first-chute winrate in band; probe_audit green.

### R7 — Chase camera micro-feel (root cause #6, last — retune after R1–R6)
- Lateral lead: `cam_target += right * clampf(vx*0.35, -3.5, 3.5)`.
- Roll: build the look_at with an up vector tilted by `-vx*0.015` (clamp ±0.12 rad)
  so the horizon leans into the carve.
- Keep position lerp constant as-is (τ≈0.14 s measured good).
**Gate:** camera_responds_to_steering=true; yaw_jerk still < 1.0; latency63 ≤ 0.30.

---

## Guardrails
- The slide is also L2's "Rainbow Slide" via `_l2_start_slide()` (`rainbow_slide_mode`,
  `game=="race"` path) — after each phase run `probe_audit.gd` AND `probe_l2.gd`;
  the L2 star-persistence assertion must stay green.
- Mobile renderer, 3–4-year-old phone: no new OmniLights on the chute, particles
  respect the Speedy tier, decor is unshaded/static.
- Touch-first: every new mechanic must be operable with one thumb on the stick;
  the tuck button is optional garnish, never required for the win.
- Do not modify SLIDE_STEER, the vx damping constant, or the cam position lerp
  without a failing metric that names them.
