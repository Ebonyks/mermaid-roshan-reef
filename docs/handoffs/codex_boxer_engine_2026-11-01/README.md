# Codex handoff: Boxer engine, Editions 1–2 and the engine foundation

## 0. Delivery status

| Field | Value |
|---|---|
| Status | Work order issued; implementation not started |
| Start | After the 7 November 2026 demo (`ODR-BOXER-SCHEDULE-20261101`) |
| Prepared by | Claude: written analysis, numbers-only measurements and specification. No game change and no image. |
| Recipient | Codex |
| Build on | `codex/boxer-contact-engine-20261031` at `22df5b7541c7ddc28f8b7acd7f4947c8807e5dc0` (CI green, not merged). At preparation it was 34 commits behind dev `27c88288bf6e39582072811443df79919e7bbb89`; sync it first (BX0). |
| This packet's branch | `claude/boxer-engine-handoff-20261101`, one docs-only commit on top of the Boxer branch |
| Finding | [`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015) (new, P1). Related: [`MA-OPERA-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-009). |
| Evidence | [EVALUATION.md](EVALUATION.md), [data/results_22df5b75.txt](data/results_22df5b75.txt), [harness/](harness/) |
| Later editions | [ROADMAP.md](ROADMAP.md) |

## 1. Owner request

The owner asked Claude, on 2026-11-01, to explore the floating-glove boxing
interface and then to refine the Boxer engine. In the owner's words: "Refining
the demo should be the next step. Playing through it time after time,
analyzing the ideal timing, rhythm and flow of these games prior to
presenting for human review and handoff." Also: "Evaluate a collision engine
for the game itself with the gloves as well, insuring that it works properly,
before completing handoff."

After reviewing the evaluation, the owner added: "Hooks should also be a part
of the game, which adds variation and disrupts the simple Punch block." On
the longer term: "I suspect this mini game is going to reoccur a minimum of
four to five times, with new additions. Complexit changes in additions as time
goes on. We are building the engine that is allowing these next steps to come
into place. Using this engine is a part of the final boss. Battle is likely."
The owner also asked for engine and gameplay to come before story placement.

## 2. Owner decisions (2026-11-01)

| ID | Decision | Owner's words |
|---|---|---|
| `ODR-BOXER-WARNING-20261101` | Each punch gets a flashing warning that shows its direction. The warning is new for boxing and does not reuse Grand Puff's. | "Flashing animation before a punch that show the direction of the upcoming punch would be ideal"; "Don't re-use from puff, new for boxing game." |
| `ODR-BOXER-HOOKS-20261101` | Hooks are part of the Boxer. | "Hooks should also be a part of the game, which adds variation and disrupts the simple Punch block." |
| `ODR-BOXER-EDITIONS-20261101` | The Boxer returns at least four or five times with growing additions; this engine enables them and will likely serve a boss battle. Engine and gameplay come before story placement. | Quoted in section 1 |
| `ODR-BOXER-COUNTER-GATE-20261101` | In Title Imp a block opens the counter. After two unblocked punches in a row, the imp tires and opens anyway. | "Use the defaults" (review decision 1) |
| `ODR-BOXER-COUNTER-WINDOW-20261101` | The counter window is 2.4 s, never below 2.0 s. With help on, it stays open until she punches. | "Use the defaults" (review decision 3) |
| `ODR-BOXER-SOUNDS-20261101` | Reuse existing sound effects for launch, "now" and count-in ticks. No new voice recordings. | "Use the defaults" (review decision 4) |
| `ODR-BOXER-SCHEDULE-20261101` | Codex starts after the 7 November demo and builds on the Boxer branch. | "Use the defaults" (review decision 5) |
| `ODR-BOXER-EDITION-ORDER-20261101` | Edition order: hooks, then rhythm, then reading the guard, then two at once. | "Use the defaults" (roadmap decision 1) |
| `ODR-BOXER-FAMILY-SPARRING-20261101` | Optional Family Sparring arrives in Edition 3, parent-started and outside the required path. | "Use the defaults" (roadmap decision 2) |
| `ODR-BOXER-NO-DODGE-20261101` | Ducking and dodging stay out for now. | "Use the defaults" (roadmap decision 3) |
| `ODR-BOXER-FLOATING-GLOVES-20261101` | The opponent stays as floating gloves for now. | "Use the defaults" (roadmap decision 4) |

Review decision 2 (spread the lanes or add hooks) was answered by
`ODR-BOXER-HOOKS-20261101`. This work order spreads the jab lanes as well.

## 3. What the evaluation found

Details and every number: [EVALUATION.md](EVALUATION.md).

- **C1, exact contact math.** `OperaBoxingContact.sweep` agreed with an
  independent reference in 340,000 cases.
- **C2, held guard works.** A still glove anywhere in the path blocked in
  all 18,240 placements.
- **C3, moving guards judged alternately.** Mid-flight errors stay within
  one frame of fist travel. Launch and landing frames can be wrong by one frame
  of glove travel. A 0.25 s stutter raises Title Imp errors to 17.4% of swipe
  tests.
- **C4, lanes too close.** One glove parked at the centre blocks both lanes.
- **C5, high guard counts as an early punch.** The upper 60% of either lane
  (70% with help) in Title Imp registers as one.
- **C6, finger lift counts as a miss.** Lifting after a guard in Title Imp is
  a failed try.
- **C7, help jumps and stays.** One slip adds two help levels, and help never
  steps back down.
- **C8, blocking is optional.** The counter opens whether or not she blocks.
- **C9, silent moments.** No sound when the counter opens, when a punch
  launches, or for any Soft Guard punch.
- **Timing and flow.** Typical players take 6 of about 9–11 counter chances,
  slow players 6 of 15–25. Random scribbling ties purposeful play in Title Imp
  (`DL-AGE-05`). Title Imp is two-thirds to three-quarters of all play.

## 4. Scope

**In:**
- The rule fixes in today's engine.
- An encounter data model with today's numbers as the shipped defaults.
- Curved paths and contact v2.
- The new boxing warning.
- An opponent brain and a beat clock.
- Edition 1: retimed, spread lanes, sounds, feel layer, device profiles.
- Edition 2: hooks, aimed counters and the Hook Pad drill.
- The evaluation turned into permanent probe cases.

**Out (planned in [ROADMAP.md](ROADMAP.md)):**
- Combos, early catch, one-two, Pearl Power, telemetry, Family Sparring and
  the free sparring ring (Edition 3).
- Stances, body shots, sway and uppercut (Edition 4).
- Two attackers, balls, big swings and sticky gloves (Edition 5).
- The boss toolkit.
- Story placement, new voice recordings, new Roshan poses, and ducking or
  dodging.

## 5. Binding rules for this work

- `DL-AGE-01`: every new objective has a short spoken line and a visual
  pointer. Use existing recordings.
- `DL-AGE-02`: one finger completes everything.
- `DL-AGE-03`: no lost progress.
- `DL-AGE-04`: no passive win, and mercy never makes mindless tapping optimal.
- `DL-AGE-05`: purposeful play is faster than random input.
- `DL-INT-09`: the five-phase two-glove specialist, owned touches and no
  health.
- `DL-INT-14`: the planned first-to-six bout, still pending.
- `DL-QA-02`: probes exercise real state transitions and negative controls.
- `DL-QA-12`: Opera integration acceptance evidence.
- `DL-UI-04`: one touch owns one route for its lifetime.
- True 2D only, the Mobile renderer, and save keys added with defaults and
  never removed.
- [ROADMAP.md](ROADMAP.md) section 2: the warning never lies; one new idea per
  edition; fair timing floors; flash-safe by construction; skill adds
  celebration and never takes progress away.

## 6. Work packages

Do them in order. Each package keeps the full probe suite green before the
next starts. Behavior-preserving steps come before behavior changes, following
the refactor rules in `CLAUDE.md`.

### BX0. Sync and reproduce

1. After the demo, bring `codex/boxer-contact-engine-20261031` up to date
   with dev, merge this packet's branch into it, and rerun the full suite.
2. Copy `harness/*.gd` to `tmp/claude_boxer_eval/`. The packet folder has a
   `.gdignore`, so Godot does not load scripts from it in place. Run each
   script with `harness/run_iso.sh`, as described in section 9.
3. Confirm the C4–C9 numbers reproduce at the synced head. Record any
   differences in the impact record before changing behavior.

### BX1. Rule fixes in today's engine (C5–C9)

Keep each fix small and separately probed.

- **C5.** While the imp is closed, a glove touching the imp's target creates
  no gesture event, no help change and no demo replay. A soft bump on the
  imp's guard is allowed as cosmetic feedback. Guards anywhere in a lane must
  never read as punches.
- **C6.** In Title Imp, releasing a glove after a move that was not a punch
  attempt emits nothing, matching Soft Guard. Glove Guide and Jab Practice
  keep their wordless retry cue for real short tries.
- **C7.** Help has one owner and one step per real mistake. Remove the
  duplicate `restart_demo()` path between `OperaBoxingSurface` and
  `OperaCareerWorld2D._on_boxing_gesture`. Step help back down one level after
  two accepted actions in a row. Keep the 0–2 range and the per-phase reset.
  Help widens timing and target size; it never lets a random tap score.
- **C8** (`ODR-BOXER-COUNTER-GATE-20261101`). A block opens the counter
  window. An unblocked punch does not, except that after two unblocked
  punches in a row the imp tires (gloves droop and wobble) and opens anyway.
  Keep the fresh-strike rule.
- **C9** (`ODR-BOXER-SOUNDS-20261101`). Add a sound at punch launch, at
  counter-window open, and at each Soft Guard punch's windup and launch, all
  from existing effects (section 8).

### BX2. Encounter data model

Move today's hard-coded values into data resources without changing behavior,
then prove the existing probes still pass unchanged.

- **Edition.** An ordered list of phases.
- **Phase.** Mode, goal, scoring rule, enabled moves, move pool or script,
  tempo, help settings, warning style.
- **Attack.** Kind, side, path, beats for windup, flight and recovery, radius
  curve, target pad, counter opening produced, sounds, warning parameters.
- **Opponent.** Glove art and transforms, signature timing.
- **Device profile.** Thumb gain, hit areas and lane spacing in millimetres.

The shipped values that become Edition 1's starting defaults:

| Value | Now |
|---|---|
| Phase goals | Guide 2, Jab 4, Guard 3, Title Imp 6, Belt 1 |
| Soft Guard | 0.8 s windup, then 2.4 s flight (`COUNTER_SECONDS` 3.2, `COUNTER_WINDUP` 0.8) |
| Title Imp | Taunt 1.4 s; windup 1.15 s (+0.45 with help); flight 0.9 s (`IMP_TRAVEL_SECONDS`); counter window 1.7 s (+0.5); reset 0.85 s after a window, 0.58 + 0.65 s after a landed counter |
| Lanes | From x 0.43/0.57 at y 0.20 to x 0.46/0.54 at y 0.86 of the stage |
| Fist radius | 160 × (0.78 + 0.25 × progress) × 0.34 px |
| Glove contact radius | 168 × (0.92 + 0.38 × reach) × 0.34 px |
| Target radius | 78 + 18 × help px; belt 56 px |
| Glove rest | x 0.31/0.69, y 0.84 |
| Phone controls | `EDGE_GAIN` (2.4, 1.15); bays at least 110 px or 18% of the screen width; phone below a 600 dp short side |
| Idle help | 5 s and 10 s (`FIRST_ASSIST_SECONDS`, `STRONG_ASSIST_SECONDS`) |

### BX3. Curved paths and contact v2

- **Paths.** Attack paths are lines or quadratic and cubic curves in
  stage-relative coordinates. Each frame, cut the travelled part of a path into
  pieces no longer than 8 px of fist travel, or 1/240 s, whichever is shorter.
  Sweep each piece.
- **Joint sweep (C3).** Sweep each glove's movement since the last frame
  together with each attack's movement over the same interval. Both discs move
  in one `OperaBoxingContact.sweep` call. Today `_frame_start_gloves` is
  assigned at the start of `_process`, which makes the interpolation inert.
  Assign it after each frame's sweeps instead, and treat a drag event as moving
  the glove's end point, not as its own sweep against a frozen fist. Include
  the frame in which a flight begins, so a swat at launch counts.
- **Several attacks at once.** Resolve the earliest contact per attack. One
  glove may block more than one attack in a frame. Unowned gloves deflect
  without scoring, as now.
- **Stutters.** A long frame is subdivided at the 8 px or 1/240 s rule. The
  glove's path inside one long frame is the straight segment between input
  samples. Document that this is the only remaining approximation.

### BX4. Boxing warning (`ODR-BOXER-WARNING-20261101`)

New code for boxing only. Do not use `EncounterWarningCue2D` or any Grand
Puff warning art.

1. **Windup.** The attacking glove pulls back toward the side it will swing
   from, on the first beat.
2. **Swoosh.** A storybook streak drawn along the attack's own path data,
   ending in a "block here" spot at the target pad.
3. **Count-in.** Three flashes, one every 0.6 s, at 0.0, 0.6 and 1.2 s from
   windup start. Each has a tick sound. The third looks and sounds different,
   meaning "here it comes". Launch is at 1.5 s and arrival 2.4 s at entry
   level. The swoosh stays softly lit, not flashing, during flight.
4. **Reward.** A block bursts the swoosh into stars and opens the counter
   with its "now" sound.
5. **Phone.** The edge bay on the matching side glows steadily, without
   flashing.
6. **Built-in limits.** The warning scheduler rejects any schedule with more
   than 3 flashes in any second, flash starts closer than 334 ms, more than
   2.5 s of flashing per warning, or two areas flashing at once. A flash is a
   brightness and scale pulse of the swoosh and the attacking glove only. No
   full-screen flash, no saturated red, no stripes.
7. **One source.** The warning and the collision use the same path
   evaluation function, so the warning cannot drift from the truth.

### BX5. Opponent brain and beat clock

- **Beat clock.** One tempo per phase, 0.6 s per beat by default. Windups,
  flashes, launches and counter windows start on beats. Optional sync to the
  career music.
- **Brain.** Scripted sequences plus weighted choice under fairness rules: no
  more than two attacks from one side in a row early in a bout, a minimum gap
  of one beat between a resolved attack and the next windup, the mix rising
  within a bout, and mercy pauses when help is at maximum.
- **Fixed lengths.** Windup lengths are fixed per difficulty step. Never add
  random waits.

### BX6. Edition 1: tuning, feel and device profiles

- **Lanes (C4).** Each jab lane at least 132 px from the stage centre line at
  every point. A starting proposal is from x 0.38/0.62 at y 0.20 to x
  0.39/0.61 at y 0.86. Prove it with the parking gate.
- **Timing.** Warning start to arrival 2.4 s at entry level on tablet and
  phone, with a 2.0 s floor as play gets easier. Counter window 2.4 s, open
  until she punches when help is on (`ODR-BOXER-COUNTER-WINDOW-20261101`).
  Soft Guard keeps its slow flight and gains the warning and sounds.
- **Feel.** A simulation freeze of about 60 ms on a block and 90 ms on a
  counter. During the freeze, contact evaluation pauses with the fist, and
  input is buffered, not dropped. Add a squash on the opponent glove, a shake
  of at most 6 px on counters only, stars from `impact_puff.png`, and layered
  existing sounds. Add positive tiers Pop, Sparkle and Pearl for presentation
  only; progress is identical. Optional 30 ms vibration on a block where the
  device supports it.
- **Device profiles.** Express gain, hit areas and lane spacing in
  millimetres per profile. Keep today's values until the phone and Tab M11 test
  says otherwise. This package builds the mechanism, not new tuning guesses.

### BX7. Edition 2: hooks (`ODR-BOXER-HOOKS-20261101`)

- **Path.** A quadratic curve from beside the attacking glove (about x 0.30,
  y 0.26 of the stage for a hook toward Roshan's left), through a control point
  further out and lower (about x 0.10, y 0.50), to her left pad (about x 0.37,
  y 0.80). Mirror it for the right. The arc is about 516 px against about
  418 px for a straight jab, about 1.0 s at the jab's speed. Aim at pads, never
  at the face.
- **Geometry check** (`harness/hook_geometry.py`). A glove parked at the
  centre misses both hooks by 81 px and still blocks a centre jab. A glove at
  the left side blocks the left hook and misses the jab by 91 px.
- **Warning.** A curved swoosh along the arc, with the same count-in. The
  windup swings the glove back wide to its side.
- **Aimed counter.** The side that hooked is left open, so its counter target
  glows on that side. Punching the guarded side is a soft bump with no
  progress, no failed try and no help change, and the open side glows brighter.
- **Teaching.** A Hook Pad drill before the bout: the existing focus mitt
  swings slowly along a hook path, three times per side. The bout then mixes
  centre jabs with hooks from both sides under the BX5 fairness rules.
- **Phases.** Glove Guide, Jab Practice, Soft Guard, Hook Pad, a hooks bout
  (Title Imp with hooks) and Belt. Phase goals and save meaning stay stable for
  Edition 1. Edition 2 is a new data entry, reachable where the owner places it
  later. Until then, reach it from the DEV playtest menu only.

### BX8. Test gates

Add the cases to `scripts/probe_boxing_contact_cases.gd`, which
`scripts/probe_opera_2d.gd` and `scripts/probe_boxing_contact.gd` already run.
New probe files in the CI roster would touch `.github/workflows/probes.yml`,
which is high-risk and needs an explicit owner task. Use fixed seeds and keep
the added runtime small. Desktop timings for reference: the full 900-game run
took 116 s, the full collision integration 794 s, the contact maths 0.4 s per
200,000 calls.

| Gate | Pass condition |
|---|---|
| Contact maths | A 20,000-case subset of `harness/geometry_check.gd`: 0 missed, 0 false |
| Held guard | A grid subset of `harness/collision_integration.gd` at 30 and 60 fps with one stutter: 100% match |
| Joint sweep | `harness/crossing_v3.gd`, both drills and hooks, steady 30 and 60 fps: no wrong call more than 1 px from the contact edge |
| C5 and C6 | Guarding at any lane point while the imp is closed, then lifting, creates no failed try and no help change |
| C7 | One slip changes help by at most one level; two accepted actions step it back |
| C8 | An unblocked punch opens no window, except the tired opening after two in a row |
| Warning honesty | The swoosh samples equal the collision path within 1 px; every schedule passes the flash limits |
| Bots, per edition | A fixed-seed subset of `harness/playthrough.gd`: typical player takes at least 80% of counter chances; slow at least 60%; random scribbling at least 1.5 times slower than typical in every phase; one parked glove blocks at most half of a mixed bout; typical full visit under 5 minutes; p90 gap between points at most 15 s |
| Hooks | The typical player blocks at least 70% of hooks after the drill; a centre-parked glove blocks no hook |
| Passive | No input earns nothing in every phase, phone and tablet |

### BX9. Records and documents

- Add impact records for every change. Move `MA-OPERA-015` to
  `FIXED_PENDING_VERIFICATION` only when its gates pass at an exact head.
- Update `DL-INT-09` for hooks and editions.
- Add an implementation section to
  `design/BOXING_GAME_PROJECT_2026-08-09.md` with the warning's flash limits as
  binding for the boxing warning.
- A game-wide flash-safety rule is a separate proposal for the owner.
- Each new asset gets its `ASSET_LICENSES.md` line in the same commit.

## 7. Acceptance criteria

| ID | Criterion | Evidence level |
|---|---|---|
| AC-1 | BX1 fixes pass their gates; existing Boxer probes unchanged except where a fix is the explicit goal | V3 |
| AC-2 | Contact maths, held-guard and joint-sweep gates pass | V2–V3 |
| AC-3 | Warning honesty and flash limits pass; the warning shares no code or art with Grand Puff's | V3 |
| AC-4 | Timing floors hold: 2.4 s entry warning-to-arrival, 2.0 s floor, 2.4 s counter window, help keeps it open | V3 |
| AC-5 | Bot gates pass for Edition 1 and Edition 2 | V3 |
| AC-6 | Hook gates pass | V3 |
| AC-7 | Passive gate passes; full CI suite green; no new 3D debt; save keys only added with defaults | V3 |
| AC-8 | Phone and Lenovo Tab M11: touch comfort on both control layouts, steady frame rate during warnings and hitstop, flashes look gentle | V5 |
| AC-9 | Roshan plays both editions without adult verbal instruction | V6 |
| AC-10 | Owner accepts the warning's look and the hooks' feel | V7 |

Report what was implemented, what was machine-verified at the named head, and
what acceptance remains (`design/AUDIT_DEVELOPMENT_CONTRACT.md`).

## 8. Art and audio requests (Codex builds; Claude only describes)

| Item | Description | New file? |
|---|---|---|
| Windup and hook windup | Reuse `glove_left.png` and `glove_right.png` with 2D transforms. The attacking glove rotates about 35 degrees outward and moves about 60 px toward its side over the first beat. A small wiggle on each tick. | No |
| Tired imp | The same gloves droop about 80 px and wobble gently for the tired opening | No |
| Swoosh | A painted storybook motion streak drawn along the attack path: soft cream core, lavender-aqua edge and the game's navy outline, a tapered tail at the opponent end and a rounded end at the pad. A dim lit state and a bright flash state. Path-driven, so one texture serves straight and curved attacks. | One small texture (at most 1024 px, or power of two), or a procedural strip in the same palette |
| "Block here" spot | Reuse `fx_invite_ring_0.png` to `fx_invite_ring_3.png`, tinted, at the target pad | No |
| Hook Pad mitt | Reuse `focus_mitt.png` moving along a slow hook path | No |
| Stars | Reuse `impact_puff.png` | No |
| Sounds | Ticks: `combat_pop.wav` at a high pitch. Third tick and launch: `combat_charge_ring.wav` at a raised pitch. Counter "now": `chime.ogg`. Choose other existing effects if clearer, but add no new sound file and no voice recording. | No |

Hashes of the reused files at `22df5b75` (SHA-256 of the Git blob):

| File | Bytes | SHA-256 |
|---|---|---|
| `assets/opera/worlds/boxer_quality_20261019/glove_left.png` | 207974 | `05404e12d2b5d57435de2772cf416622929cbaf1b2a516ca570b8c1b4e704033` |
| `assets/opera/worlds/boxer_quality_20261019/glove_right.png` | 183564 | `ec18be3560ffcf9b88f62282da2dc7bd52b162ec4e81c6ea6b9d22105a40248f` |
| `assets/opera/worlds/boxer_quality_20261019/focus_mitt.png` | 234344 | `7e992937b342b9c30d064e4e7b4d33bc6ed19c0df31b08e8a59603fd570b32d2` |
| `assets/opera/worlds/boxer_quality_20261019/impact_puff.png` | 170792 | `459d5f4ed6f11d51540fd31611056b739c2c7113f7a55d72ff78ec0445bb96ea` |
| `assets/audio/sfx/combat_charge_ring.wav` | 19448 | `0dca6754636cb7218e165dc9c8c2784ef06787ca7ffbb8065b7b528060adf0bf` |
| `assets/audio/sfx/combat_pop.wav` | 9746 | `26856598c6cdce07b63c1eb23833d05af01972d11fdac32d41c183b8597f46cd` |
| `assets/audio/sfx/combat_bonk.wav` | 13274 | `6965f73cda39888f10433f6e0335b259916094b4420fadc4e8dc5fd3d5925ed0` |
| `assets/audio/chime.ogg` | 11155 | `b9643d923ab82daaa56ad4a010b8463c8a911333caaa226f2eefff8bb3c681fd` |

Source files evaluated, also at `22df5b75`:

| File | Bytes | SHA-256 |
|---|---|---|
| `scripts/opera_boxing_surface.gd` | 35190 | `ed9917765b94b746329dfd90f81bbcc8d021f37ef90f610bb008c92f53a07502` |
| `scripts/opera_boxing_contact.gd` | 1940 | `f4c2eaf90f76a93ebd9beb2d533acf7291cbf40ac08ac87e71fde02bf0b7adb4` |
| `scripts/opera_career_world_2d.gd` | 242951 | `5ad06f19eba86ca94b6a06a093bac79a909895fb188f0d477d8193fb8fbd8700` |
| `scripts/probe_boxing_contact_cases.gd` | 23271 | `00cff45c25e089a45e36d2a5ab60d6707c24111ad97574cde0beb7ed983a19e4` |
| `design/BOXING_GAME_PROJECT_2026-08-09.md` | 20186 | `5c80fdaf18665e268da7465a30c90f6ea3cba64090cb477a1558d02e636a7cd7` |

## 9. Rerunning the evaluation

From the repository root of a Boxer checkout:

```bash
mkdir -p tmp/claude_boxer_eval && cp docs/handoffs/codex_boxer_engine_2026-11-01/harness/*.gd tmp/claude_boxer_eval/
H=docs/handoffs/codex_boxer_engine_2026-11-01/harness
$H/run_iso.sh geometry 15m -s tmp/claude_boxer_eval/geometry_check.gd
$H/run_iso.sh integ 40m -s tmp/claude_boxer_eval/collision_integration.gd
$H/run_iso.sh cross3_imp 30m -s tmp/claude_boxer_eval/crossing_v3.gd -- mode=boxing_imp
$H/run_iso.sh cross3_guard 30m -s tmp/claude_boxer_eval/crossing_v3.gd -- mode=boxing_guard
$H/run_iso.sh play 40m -s tmp/claude_boxer_eval/playthrough.gd -- runs=120
(cd $H && python -B geometry_numbers.py && python -B high_guard.py && python -B hook_geometry.py)
```

| Script | Prints | Notes |
|---|---|---|
| `geometry_check.gd` | `GEOM` lines | Convex-search reference; 340,000 cases |
| `collision_integration.gd` | `HELD`, `PARK`, `IMPGATE`, `ASSIST` | Its `CROSS` lines feed the glove one frame late and are superseded by `crossing_v3.gd` |
| `crossing_v3.gd` | `CROSS3` | Godot's real order: the frame's input event first, then `_process(delta)` to the same time. Errors labelled launch, mid-flight or landing. A `999` launch value marks a late landing block whose truth window was empty. |
| `crossing_debug.gd` | `DEBUG` | Per-case diagnosis that identified the launch and landing frames |
| `boundary_checks.gd` | `RELEASE` | Its boundary search exceeded 40 minutes and was replaced by `crossing_v3.gd` |
| `playthrough.gd` | `PLAY`, `VOICE`, `LAYOUT` | Mirrors `_on_boxing_gesture`; profiles quick, typical, slow, random scribbler and centre parker |
| `run_iso.sh` | Logs | Fresh APPDATA per run. A direct run would write the desktop save. |

Pitfalls found while measuring:
- Feeding the input event after `_process` lags the glove one frame and
  inflates crossing errors.
- Curved or clamped glove paths during a stutter diverge from the straight
  segment the engine must assume.
- The packet folder's `.gdignore` keeps Godot from loading these scripts in
  place; copy them to `tmp/` first.

## 10. Constraints

- **Medium.** True 2D only, the Mobile renderer, no new 3D nodes, models or
  lights.
- **Protected content.** Recorded family voices and protected art stay
  untouched. Any new texture is at most 1024 px or a power of two, with its
  `ASSET_LICENSES.md` line in the same commit.
- **Saves.** Never remove a save key; add new ones with defaults. Edition 1
  keeps the Boxer's existing save bit and reward meaning.
- **Story.** Placement of later editions, and any boss use, is decided later
  by the owner.
- **Safety and process.** Existing security and release precedence are
  unchanged. Merge into dev only with a green exact-head Probe Suite, after the
  demo freeze.
