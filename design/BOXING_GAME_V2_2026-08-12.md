# Opera Boxing Engine 2.0

Date: 2026-08-12

Status: implementation-ready design decision

Runtime: Godot 4.7.1-stable, Mobile renderer, fixed 1280x720 Opera stage

Audience: one specific four-year-old; one-finger completion is mandatory

## 1. Decision

Boxing 2.0 will be a friendly counterboxing game, not a damage game.

The child reads one large visual tell, moves a glove into a generous guard or
target, punches a bright opening, and immediately gets a playful celebration.
The game contains real skill in aim, timing, hand alternation, and returning to
guard. It contains no health, knockout, lives, lost progress, negative grade,
punishing timer, or fail state.

The core technical decision is equally important:

- Punch recognition, opponent timing, quality measurement, and progress remain
  in a deterministic fixed-step 2D model.
- Jolt may react to an already accepted hit through one optional hanging prop.
  It never decides whether a punch counted.
- Every broadly correct punch advances the activity by the same amount. Cleaner
  technique changes spectacle and charges Pearl Power sooner; it never gates
  completion.
- The existing five-phase Opera career, Opera star bit, reward flow, approved
  art, and recorded boxer voices remain authoritative. One generic,
  add-only Opera checkpoint map is introduced so completed training phases
  survive an exit; no boxing score or physics state is persisted.

This is the safe version of the market's strongest boxing loop:

`read the tell -> guard or aim -> punch the opening -> celebrate -> recover`

## 2. Research method and limits

Research was checked on 2026-08-12. "Popular" means visible mobile-store scale,
not a claim about monthly active users. Google Play publishes broad lifetime
download bands and review counts; Apple publishes ratings and sometimes a live
category rank. Those figures can vary by region and are not directly
comparable to publisher claims.

The comparison prioritizes current store pages and official control/support
pages. Store reviews are used only as anecdotal evidence about feel problems,
not as population-level research.

## 3. Mobile boxing market

| Game | Visible scale on 2026-08-12 | Important abilities and systems | Transfer to Roshan | Deliberately reject |
|---|---|---|---|---|
| [World Robot Boxing](https://play.google.com/store/apps/details?id=com.jumpgames.rswrb) | 50M+ Google Play downloads, 2.34M reviews, 4.5 | Jabs, uppercuts and specials; a large robot roster, arenas, PvP, trophies and paint customization | Oversized rival personality, obvious specials, trophy celebration | Damage, currencies, paid power-ups, PvP and grind |
| [Punch Boxing 3D](https://play.google.com/store/apps/details?id=com.yx.boxinghero) | 50M+ downloads, 1.02M reviews, 4.4 | Jab, hook, uppercut, combos, special moves, a 30+ opponent career and gym upgrades | A tiny recognizable punch vocabulary adapted into short Roshan encounters | Realistic violence, stat gear, upgrade grind and gesture ambiguity beyond the validated punch set |
| [Real Boxing 2](https://play.google.com/store/apps/details?id=com.vividgames.realboxing2) | 50M+ downloads, 296K reviews, 4.6 | Tap jab; hold haymaker; directional uppercut/body blow; block, parry, dodge and movement; career, bosses, tournaments and mechanic-specific training | Teach one action in a dedicated drill, then combine it in the title match; clear counter windows | Dense controls, damage, energy gates, ads, paid progression |
| [Boxing Star](https://play.google.com/store/apps/details?id=com.ftt.boxingstar.gl.aos) | 10M+ downloads, 863K reviews, 4.6, Editors' Choice | Jabs, hooks, uppercuts, training, MegaPunch, expressive rivals and story | Expressive imp poses, clean one-two rhythm, a skill-earned Pearl Power celebration | Knockdowns, leagues/chat, random paid gear and daily pressure |
| [Real Boxing](https://play.google.com/store/apps/details?id=com.vividgames.realboxing) | 10M+ downloads, 531K reviews | Compact punches and combos, adaptive rivals, career, speed-bag/heavy-bag/rope training | Training props should rehearse the exact match actions | Damage, multiplayer, progression economy |
| [Prizefighters 2](https://play.google.com/store/apps/details?id=com.koalitygame.prizefighters2) | 5M+ downloads, 18.9K reviews, 4.1 | Readable tells, counters and power moves; training, sparring, careers, styles and management | The tell-response-counter loop creates depth without many controls | Reading-heavy management, aging, condition loss, scheduling |

Two specialist comparisons sharpen the physics decision:

- [Super Boxing Championship](https://play.google.com/store/apps/details?id=air.com.stickrunningsupreme.sbc)
  has 1M+ downloads and advertises full-body weight/collision physics plus 11
  moves. Its weight and secondary motion are appealing, but an older review
  still displayed on the store reports the arms sometimes becoming unable to
  punch or block. This is anecdotal, but it illustrates why simulation must
  not own child-facing hit validation. The app itself was last updated in
  August 2023.
- The official [Real Boxing 2 control guide](https://support.vividgames.com/rb2/gameplay/103.html)
  and [training guide](https://support.vividgames.com/rb2/gameplay/93.html)
  show distinct controls and gym props tied to attributes such as stamina,
  speed and strength. Its separate
  [tutorial guide](https://support.vividgames.com/rb2/gameplay/341.html)
  teaches haymakers, counters, specials, dodges and parries step by step.
  The official [World Robot Boxing 2 FAQ](https://www.reliancegames.com/faq/wrb2-faq.html)
  is a same-series mechanic comparator showing the other common pattern:
  successful hits charge a visually obvious special. Its mechanics must not
  be mistaken for the original game's 50M+ store scale above. A related
  [Boxing Star X control guide](https://wiki.boxingstarx.com/how-to-start/controls)
  similarly documents guard, weave and counter controls for that franchise,
  but not necessarily the exact base-game build in the table.

### 3.1 Market abilities that recur

The popular games repeatedly use:

- A small punch set: jab, heavy/hook or uppercut.
- Defense: guard, dodge or weave.
- Counterplay: recognize a tell, defend, then use the opening.
- Distance, aim and timing rather than button speed alone.
- Short training activities tied to match actions or attributes.
- Distinctive rivals, arenas, belts and trophies.
- A special move earned by successful play.
- Strong contact confirmation through pose, sound, particles and crowd
  response.
- Customization or a visible record of achievement.

Commercial games also lean on energy timers, ads, daily streaks, PvP, loot,
random gear stats, health/revive kits and escalating grind. None belongs in a
private preschool game.

### 3.2 The useful market conclusion

The most transferable idea is counterboxing, not combat attrition. Patience,
recognition and a clean response can be genuinely learned. Damage and loss add
no useful skill for this audience.

Responsiveness is foundational. Current store feedback for multiple games
describes delayed or missed hit registration as destroying the sense of skill;
World Robot Boxing's current release notes explicitly promote instant,
frame-precise response. Roshan must never wonder whether the game noticed a
correct gesture.

## 4. Version 1 assessment

The current `OperaBoxingSurface` already has an unusually good safety and input
foundation:

- Two gloves have independent, sticky touch ownership.
- Releasing one finger cannot release the other glove.
- One finger can finish every phase sequentially; two fingers are expressive,
  not required.
- Touch/mouse deduplication, focus-loss cleanup and phase cleanup exist.
- A valid punch requires a real forward drag; passive waiting does not win.
- Assistance replays the ghost demonstration and widens geometry.
- Imp contact is a bubble/recoil event and cannot remove progress or change a
  save.
- Career and save authority remain outside the specialist surface.

Version 1's weakness is not difficulty. It is that almost every successful
punch feels and scores the same:

- Drag samples directly assign glove position. There is no measured path,
  velocity, acceleration, recoil or deformation state.
- Contact tests only the sampled endpoint against a target circle plus a
  forward-projection threshold. A fast swipe can cross a target between input
  packets and miss.
- Punch speed, path straightness, alternation, timing quality and snap-back are
  not measured.
- A held finger must release before another punch; retracting naturally does
  not re-arm it.
- Glove return is a single exponential lerp, so it reads as a cursor returning
  rather than a padded object recovering.
- The guard activity samples a final position; it does not reward intercepting
  the padded counter.
- Opponent timing runs in variable frame time, which is harder to make
  partition-stable across a 30 fps phone, a fast editor and frame hitches.
- Progress pearls show quantity only. There is no positive visual language for
  a particularly clean punch.
- The shared Opera competition currently derives curtain cheer partly from a
  34-second boxer par time. That quietly rewards rushing even though the boxer
  hides the rival bars. Speed-to-finish is the wrong mastery signal here.

The V1 game therefore has basic aim and open-window skill, but little room for
the child to become visibly better.

## 5. Version 2 experience principles

1. **Reliable before realistic.** A directed gesture inside generous geometry
   always counts, independent of speed and physics solver state.
2. **Mastery without punishment.** Technique creates more celebration, never
   less progress.
3. **One lesson at a time.** Training teaches the exact action used in the
   finale.
4. **One-finger complete, two-finger expressive.** Simultaneous play is fun but
   never a gate.
5. **Tell before motion.** Every imp action has a large pose, color, sound and
   roughly one-second warning.
6. **No shame language.** There is a normal pop, a brighter sparkle and a Pearl
   flourish; there is no bad grade, broken combo or red X.
7. **Short and finishable.** The full career targets three to four minutes,
   with 20-45 second activities and no deadline.
8. **No face-target framing.** Mitts, gloves, guard bubbles and the imp's padded
   chest emblem are targets.

## 6. Core controls

### Claim

Touch near either resting glove to claim it. The nearest free glove wins that
finger until release. A second finger may independently claim the other glove.
Crossing fingers never swaps ownership.

### Punch

Drag a glove from its guard home toward the glowing target. Contact uses a
swept path, so crossing a target between touch packets still counts. A broad,
directed motion counts at any reasonable child speed.

### Recover

Pull the glove back below 33% extension to re-arm it, even while the finger is
still held. Releasing makes it spring back to guard. This creates a natural
forward-back-forward jab rhythm without forcing repeated taps.

### Guard

Move either glove into the large colored bubble on the telegraphed side. Early
placement succeeds. Meeting the padded counter closer to its arrival makes a
brighter parry flourish, but is never required.

### One-two

The next suggested glove glows. Using it produces a rainbow link and extra
Pearl charge. Using the other glove still lands the punch and advances the
round. Alternation is a mastery opportunity, not a correctness gate.

There are intentionally no required hooks, uppercuts, movement stick, stamina
button or separate special button. The preschool vocabulary is punch, recover,
guard and one-two.

## 7. The real skill model

Every accepted **phase-unit** action advances the same monotonic
cheer/progress meter. A defensive action in a combined title exchange may open
the counter and charge spectacle without replacing its required punch; the
explicit outcome table in section 8.4 is authoritative. The engine also
calculates a session-local `technique` value for presentation. It is never
saved and never exposed as a number to the child.

For a punch:

```text
technique = 0.40 * aim
          + 0.25 * straightness
          + 0.20 * open_window_timing
          + 0.15 * coordination
```

All terms are clamped to 0..1:

- At contact, form the directed ray from the extension origin through the
  logical glove center. `aim = 1 - perpendicular_target_distance / 82px`,
  where the distance is the target center's lateral distance to that ray, not
  endpoint-clamped distance to the finite first-contact segment. Clamp it to
  0..1. A centered slow and fast punch therefore have the same aim. The 82 px
  mastery radius stays fixed when assistance widens acceptance, so assist can
  admit a Pop without falsely manufacturing a high technique tier.
- `straightness = direct_origin_to_contact_distance / sampled_path_length`.
- In a normal open window, let `u` be normalized elapsed open time;
  `open_window_timing = 1 - 0.5 * abs(2*u - 1)`, so even an edge-of-window hit
  retains 0.5. An assisted held-open period and a mode with no timing window
  use a neutral 0.75.
- Outside a suggested one-two beat, `coordination = 1 - start_extension/0.33`
  for an armed glove, rewarding a fuller return within the already valid guard
  zone. In a one-two beat, `coordination` is 1 for the suggested alternating
  hand and 0 for the other hand. The other hand still produces a full Pop and
  phase unit.

The components are measured from time-stamped samples resampled onto the
fixed-step timeline. Technique values are quantized to 1/255 before choosing a
presentation tier: Pop below 0.68, Sparkle from 0.68 through 0.84, and Pearl at
0.85 or above. These are initial playtest thresholds, not reward gates.
Forward speed does not decide success and is not part of the grade; it
scales squash, puff size and sound energy within safe limits. This avoids
teaching frantic swiping while still making a confident punch feel stronger.

Recovery after a hit lights the cuff as immediate readiness feedback and
affects the next punch. The current impact's presentation never waits for a
later gesture to finish scoring it.

The child sees only positive tiers:

| Internal tier | Meaning | Feedback | Progress |
|---|---|---|---|
| Pop | Broadly directed accepted action | Soft pop, bubbles, small target recoil | +1 |
| Sparkle | Cleaner aim/timing/path | Brighter ring, pitched impact, crowd clap | +1 |
| Pearl | Very clean action or a clean alternating pair | Pearl burst, rainbow trail, larger friendly recoil | +1 |

No tier is announced as lesser. A Pop is a complete success.

The shared Opera result must special-case boxer presentation: elapsed time and
miss count do not lower its curtain call. Every completion receives the same
saved reward and a full positive bow. Session technique may add pearl flares,
an extra imp pose and a longer crowd flourish; it never removes the baseline
celebration. `competition.note_miss()` remains unused by boxer.

### Pearl Power

Six orbiting lights form a non-reading special meter around the championship
crest. They are visually distinct from the six horizontal round lamps that
show required title punches.

- Every accepted title punch lights one segment.
- A Sparkle/Pearl punch or a bright timed parry may light one bonus segment.
- Segments never drain, including after a miss or imp contact.
- The accepted punch that fills the sixth segment automatically becomes Pearl
  Power. If a parry fills it, the next accepted open-window punch becomes
  Pearl Power. The effect is a bubble wave, bell flourish, crowd cheer and
  exaggerated imp cartwheel/bow.
- There is no extra button. Basic play is guaranteed to charge it by the end;
  skilled play earns the spectacle earlier.

This transfers the market's earned-special appeal without damage, currencies
or failure pressure.

## 8. Shipping career: five phases

Keep the existing five Opera phases and save/reward integration. Change their
internal teaching and presentation, not the career topology.

| Phase | Existing mode | Goal | V2 lesson | Completion |
|---|---|---:|---|---|
| 1. GLOVE WAKE-UP | `boxing_guide` | 2 | Claim, extend and recover each glove | One extend-then-recover cycle with each glove, either order, same finger allowed |
| 2. RAINBOW MITTS | `boxing_jab` | 6 | Aim, clean forward path and optional left/right rhythm | Six accepted mitt punches across three tiny sub-rounds |
| 3. BUBBLE GUARD | `boxing_guard` | 3 | Read a side tell and move a glove to guard | Three child-caused guard entries; a late/no guard only repeats the cue |
| 4. TITLE IMP | `boxing_imp` | 6 | Combine tell, guard, opening, counter and one-two | Six accepted padded-chest/mitt punches across three friendly rounds |
| 5. BELT | `boxing_belt` | 1 | Deliberate final forward punch | One glove-to-belt punch, then curtain call |

### 8.1 Glove Wake-Up

- One resting glove pulses while a ghost finger demonstrates forward and back.
- The target is a large mitt at mid-screen.
- A hand's unit is banked only after its accepted extension subsequently
  retracts below 33% or its finger releases. The celebrated hand then stays
  banked and instruction moves to the other.
- If the child uses the same finger twice, the phase behaves identically.
- Two simultaneous extensions cannot finish the phase until both recover.

### 8.2 Rainbow Mitts

Use three wordless sub-rounds, two hits each:

1. **Reach:** large stationary left and right mitts.
2. **Aim:** a mitt gently visits one of four known locations, then stops and
   waits. It never needs to be chased while moving.
3. **One-two:** the suggested glove and matching mitt share a color. Either
   glove succeeds; correct alternation earns the rainbow/Pearl flourish.

Targets always settle before becoming hittable. Motion is anticipation, not a
precision tracking tax.

### 8.3 Bubble Guard

- The imp or pad rig raises one glove and paints a large same-side bubble.
- Base timing is a 1.5-second still tell followed by 1.3 seconds of slow padded
  counter travel, for contact at 2.8 seconds. Assist 1 uses 1.9 + 1.6 = 3.5
  seconds; Assist 2 uses 2.3 + 1.9 = 4.2 seconds.
- Crossing into the bubble after the tell is the required child action; simply
  leaving a glove parked before the cue cannot passively complete the phase.
- Entry is accepted from tell onset through contact. A glove already inside at
  tell onset must exit and re-enter; it never scores from mere occupancy.
- Early guard is a full success. A near-arrival intercept earns extra sparkle.
- Quantize `parry_timing = (entry_time - tell_hold) / counter_travel` to 1/255
  and clamp it to 0..1. A value at or above 0.75 (the final quarter of padded
  counter travel) is a bright timed parry and may light one bonus Pearl
  segment. Earlier entry is still a complete guard success.
- No guard produces bubbles, a funny wobble and an immediate, slower replay.
- Progress and Pearl lights never change backward.

### 8.4 Title Imp

One friendly boxer imp carries the whole finale. Three internal rounds use
recognizable poses rather than increasing speed:

1. **Find the opening:** windup -> padded glove extends -> chest star opens.
   Punch the star.
2. **Guard and answer:** side tell -> guard or harmless bubble tap -> guaranteed
   open star -> punch.
3. **Pearl one-two:** two large mitt/chest lights appear in sequence. Either
   hand advances; clean alternation charges or triggers Pearl Power.

The state loop is:

```text
TAUNT -> TELL -> PADDED_CONTACT -> OPEN -> CHILD_PUNCH -> RECOIL -> RESET
```

Hard guarantees:

- Without an accepted child punch, `OPEN` cannot time out until it has been
  drawn on at least two rendered frames and accumulated at least 1.5 seconds
  of fixed-step simulation, so a frame hitch cannot skip it.
- After two late/blocked attempts, the next opening holds until a hit.
- Imp contact can add visual recoil only. It cannot alter any progress, quality
  history, Pearl charge, competition state or save state.
- A guarded or early punch re-cues the same opening; it cannot reset the round.
- The imp ends in `bopped` then `bow`, not knockout or defeat.

Title outcomes are explicit and separate:

| Outcome | Title progress | Pearl segments | Other state |
|---|---:|---:|---|
| Accepted open-window punch | +1, capped at six | +1; +1 bonus for Sparkle/Pearl | Recoil, next beat |
| Accepted guard | +0 | +1 only for a bright timed parry | Guaranteed opening |
| Miss, guarded/early punch or imp contact | +0 | +0 | Re-cue; no loss |

Only the six accepted punches complete TITLE IMP. A guard can create the
opening and charge spectacle, but it cannot replace a required punch.

### 8.5 Belt

Stop all opponent timelines, cancel stale finger claims and show the existing
belt. A real forward glove path is still required. The belt punch releases
Pearl Power if it has not yet fired, guaranteeing a celebratory ending.

## 9. Assistance and pacing

Assistance reacts to time since the last accepted child action, never to a
visible failure counter:

| Time without accepted action | Assistance |
|---:|---|
| 0-4 s | Normal pulse and target trail |
| 4 s | Replay the wordless ghost gesture and existing voice cue |
| 8 s | Widen target/corridor about 20%; slow the next imp tell |
| 12 s | Move the target closer to the demonstrated route and hold the next opening until contact |

Input immediately dismisses redundant demonstrations. Assistance cannot move
a glove, bank progress or fire Pearl Power. Geometry returns to baseline on
the next activity, so the game always offers mastery without trapping the
child in a permanently hard state.

Initial tuning targets for supervised playtest are:

| Parameter | Base | Assist 1 | Assist 2 |
|---|---:|---:|---:|
| Target radius | 82 px | 100 px | 118 px |
| Required forward reach | 55% | 48% | 42% |
| Direction corridor | +/-50 degrees | +/-62 degrees | target-only guidance |
| Imp windup | 1.5 s | 1.9 s | 2.3 s |
| Open window | 2.0 s | 2.6 s | held until hit |
| Guard warning | 2.8 s | 3.5 s | 4.2 s |

These are starting values, not acceptance claims. Tune them from the child's
actual hand paths. Assistance escalates from elapsed time without accepted
work; exploratory presses and harmless misses do not instantly promote the
assist tier.

## 10. Feel model

Create `BoxingFeelModel extends RefCounted`. `OperaBoxingSurface` continues to
own touch routing and drawing; `OperaCareerWorld2D` continues to own progress
and completion.

Run the model with the repository's established 1/60-second fixed substep and
a capped hitch accumulator. The surface stamps each input with its monotonic
local receive time. Input events update finger targets immediately for visual
response; the model queues the ordered samples and linearly resamples each
finger target at fixed-tick times. A geometric path with the same timestamps
therefore has the same authoritative ticks whether Android delivered 30, 60 or
120 drag packets per second.

Process at most eight substeps (133 ms) per rendered update and discard excess
catch-up time rather than fast-forwarding child-facing states. Retain only the
normal substep remainder. `OPEN` timeout additionally requires two explicit
render acknowledgements; an accepted child punch may resolve it sooner.

World time and gesture time have separate catch-up budgets. World/opponent
simulation remains capped at eight steps. Before rebasing after a hitch, the
gesture sampler may drain up to 32 fixed input steps (533 ms) from the real,
ordered, time-stamped sample path while holding target/opponent hittability at
its last simulated snapshot. A genuine directed crossing already received
during a 500 ms stall therefore counts once; discarded world time cannot make
a closed target become open. The same 1/60 resampling and technique
quantization used normally apply to this path.

After draining that bounded gesture window, rebase the input-sampling epoch to
the current monotonic clock (`max(now, latest_receive_timestamp)`). Drop any
older remainder and seed each held glove's previous/current authoritative
positions from its latest finger target at that rebased time, with a
non-scoring discontinuity flag for one fixed step. This also works when a held,
stationary finger emitted no event during the hitch. Only an unsampled
positional jump is non-scoring; validated queued segments are never discarded
without recognition. The seed step may update ownership and visuals but cannot
create velocity, a swept contact or technique. This prevents both a phantom
giant sweep and an input backlog hundreds of milliseconds ahead of simulation.

On focus loss or app pause: cancel touch owners, clear queued samples and the
accumulator, freeze opponent/open/assist clocks and emit no outcomes. On
resume, re-cue the current target or safe `TELL` state from its beginning with
no catch-up, progress or assist escalation.

Each glove tracks:

- Owner, finger target and authoritative logical position.
- Previous position for swept contact.
- Filtered forward velocity and peak forward velocity.
- Origin, extension, lateral error and accumulated path length.
- State: `READY`, `EXTENDING`, `IMPACT`, `RETRACTING`.
- Per-extension hit latch.
- Recovery hysteresis; re-arm below 33% extension.
- Visual-only squash, rotation, cuff lag and recoil offsets.

### 10.1 Contact

Use swept-circle/capsule intersection from the previous logical glove center to
the new center. A contact is eligible only when the glove is owned, in
`EXTENDING`, has increasing extension and positive forward velocity, has met
the assisted minimum reach, and crosses a target that was already active and
hittable before the step. Retraction, automatic return, a newly appearing
target over a parked glove and visual-only recoil can never score.

Resolve the earliest eligible crossing **per glove**. Sort resulting events by
time-of-impact and then hand index. Two different live targets may each pay
once on the same step. A single-use target/opportunity is reserved by the first
sorted event and pays at most once; later contacts get cosmetic bounce only.
Cap awarded units at the phase goal before emitting career work. This removes
fast-swipe tunnelling without allowing a two-finger double payment.

Suggested event fields:

```text
hand, target_id, contact_point, contact_normal,
reach, aim, straightness, timing, alternated,
forward_speed, presentation_tier, effect_strength
```

The surface emits accepted work exactly once per reserved target. Career
progress never reads speed, quality tier, visual state or a physics body.

### 10.2 Responsive weight

Do not make the visible glove lag far behind a finger. That would look weighty
but feel broken.

- The authoritative tip follows the finger in the same input/render cycle.
- Perceived mass comes from velocity-based glove rotation, cuff lag, squash at
  contact, a short local recoil and a critically damped return spring.
- Cap any visual-only displacement to about 20 px and clear it immediately on
  focus loss, phase change or a new claim.
- Use a 30-45 ms local impact emphasis pose. Never change global `time_scale`
  or freeze input.
- A 3-5 px stage-layer micro-jolt may accompany a Pearl hit for at most 70 ms;
  targets, pointer cues and UI remain stationary. Provide a reduce-motion
  path that sets this to zero.

### 10.3 Feedback stack

An accepted hit should acknowledge within the next rendered frame:

1. Contact-point flash and glove squash.
2. Existing pop/bonk audio with tightly bounded pitch/volume variation.
3. Target, bag or imp recoil in the analytic impact direction.
4. Bubbles, ring and stars scaled by presentation tier.
5. Pearl light/crowd response where earned.

Aim for visual acknowledgement within 33 ms at the 30 fps device target and
audio onset within 50 ms. No effect may delay the next accepted input.

## 11. Jolt decision

The project setting selects Jolt as the **3D** physics backend. The boxer is a
2D Canvas `Control`. Godot's official [Jolt documentation](https://docs.godotengine.org/en/4.7/tutorials/physics/using_jolt_physics.html)
also configures it under Physics -> 3D; it does not replace 2D gesture logic.
Godot's [physics interpolation guidance](https://docs.godotengine.org/en/4.7/tutorials/physics/interpolation/physics_interpolation_introduction.html)
notes that interpolation can add input delay and that fast-input situations
may need a different scheme or higher tick rate. That makes interpolated rigid
bodies the wrong authority for a touch punch.

### 11.1 What Jolt may do

Define a presentation-only `ImpactResponder` interface. Ship an
`AnalyticPendulumResponder` first. Optionally prototype one
`JoltBagResponder`:

- One `StaticBody3D` anchor, one `RigidBody3D` bag and one `PinJoint3D` joining
  them. Leave Jolt-unsupported pin bias/damping/clamp properties at defaults;
  tune the body's gravity, mass and damping instead.
- Give the bag one simple `CapsuleShape3D` or `CylinderShape3D` so mass/inertia
  are well-defined. Set `collision_layer = 0`, `collision_mask = 0`,
  `contact_monitor = false` and `max_contacts_reported = 0`.
- Use the Canvas XY screen plane: lock linear Z and angular X/Y, allow angular
  Z, enable sleep and cap the visible swing to 22 degrees.
- It receives a one-way impulse derived from an already accepted `PunchEvent`.
- Only `JoltBagResponder` may read the body's transform, solely to expose a
  presentation pose. No authoritative system reads body state, and the
  responder emits no gameplay signal or target geometry.
- If initialization fails or the Speedy path disables it, the analytic
  responder takes over with identical gameplay outcomes.

Testing selects injectable responder modes `ANALYTIC`, `JOLT` and
`FAILED_INIT`; it does not try to switch Godot's project-wide 3D backend at
runtime. The configured backend remains Jolt for every mode.

If a Jolt prop requires a full-screen 3D `SubViewport`, do not ship it. A small
isolated prop viewport or an existing 3D host must pass the performance gate.

### 11.2 What Jolt must never do

- Own glove position or chase a finger.
- Detect whether a punch landed.
- Estimate child punch quality from solver impulse.
- Advance or block an imp state.
- Affect target geometry, Pearl charge, progress or saves.
- Add a ragdoll, soft body, rope fleet or more than one awake dynamic prop.

### 11.3 Jolt go/no-go gate

Jolt garnish ships only if all are true on the Lenovo Tab M11 and the older
phone:

- The child-visible reaction is clearly preferable in an A/B review.
- Gameplay event logs are identical in `ANALYTIC`, `JOLT` and `FAILED_INIT`
  modes. Each run starts from a cloned save fixture; compare normalized
  gameplay fields while excluding `save_generation` and backup metadata that
  legitimately change on every write.
- 30 fps is sustained, p95 total frame time remains below 33.3 ms and the prop
  adds no recurring hitch.
- At most one dynamic body is awake; it sleeps promptly after settling.
- No full-screen transparent viewport or material violates the overdraw
  budget.

If any criterion fails, retain the deterministic analytic pendulum. The game
does not need Jolt to feel good; it needs authored response, reliable contact
and well-tuned secondary motion.

## 12. Presentation and resources

Version 2 reuses the approved boxer world/stage tiles, rival pose family,
crest, belt, FX and protected boxer voices listed in
`design/BOXING_GAME_PROJECT_2026-08-09.md`.

No new generated art is required.

For the default engine, keep the independently drawn gloves and procedural
halos/trails. If the optional physical bag passes its prototype gate, derive a
new transparent heavy-bag runtime image non-destructively from the approved
`opera_job_boxer_stage_states_training_bag_rig.png` source card. Preserve the
source, store the derivative at a new path and add its provenance to
`ASSET_LICENSES.md` in the same implementation commit. Do not touch protected
voices.

Optional self-expression is limited to three large glove-color choices in the
corner tableau. Color is cosmetic, uses existing drawing/tint capability and
need not be persisted. There are no equipment stats or random rewards.

## 13. Save and privacy contract

- Add one generic top-level `opera_act_checkpoints` dictionary with default
  `{}`. It maps a stable Opera career ID to the next phase index. This is an
  add-only, backward-compatible save-schema change, not a boxing score.
- Immediately after each completed boxer phase, clamp and save the next phase
  index. On entry, resume at that phase with zero transient phase progress.
- Values `0..phase_count` are valid. `phase_count` is the terminal sentinel
  "BELT completed; Opera reward finalization pending," not an index to clamp
  back to BELT.
- BELT first writes that terminal sentinel. It then performs reward
  finalization: set the Boxer star, compute the first-time/replay reward, erase
  the checkpoint and write those mutations together in one save transaction.
  Existing dirty-write retry applies to the whole transaction.
- If interruption occurs after the sentinel write but before finalization, the
  next explicit Boxer door/continue input resumes the curtain call and runs
  the same transaction. A passive tick never awards or wins. A terminal
  sentinel is authoritative even when the star already exists: star absent
  pays the first-time reward; star present pays the replay reward; both erase
  the sentinel atomically with payment. A valid star plus nonterminal
  checkpoint is an interrupted replay and resumes at that phase; a starred act
  with no checkpoint starts a fresh replay at phase 0. Atomic whole-save
  replacement makes the terminal transaction idempotent and prevents duplicate
  pearls.
- Only exact integers in `0..phase_count` are valid. Missing, non-integer,
  negative or above-range career entries are erased and use 0; corrupt high
  values can never clamp into the reward-authorizing terminal sentinel. The
  star remains authoritative for whether a terminal reward is first-time or
  replay, not for discarding an active replay checkpoint.
- Completion still sets the existing Boxer bit in `opera_stars`; existing
  `opera_progress`, `opera_done` and Opera reward handling remain unchanged.
- Technique, Pearl charge, assists, glove color, opponent pose and touch IDs
  are session-local.
- Do not persist partial punches, partial phase progress, touch ownership,
  timers or Jolt/pendulum state. The durable boundary is a completed short
  activity, preventing both lost training and phantom actions after resume.
- Do not add analytics or child telemetry. Tune from supervised observational
  playtests and deterministic probes.

## 14. Required probes

Preserve all V1 ownership, mouse, deduplication, one-finger, passive-progress,
friendly-hit, lifecycle and save assertions. Add:

- The same time-stamped geometric path partitioned as 30, 60 and 120 Hz input
  produces identical accepted target/hand/order logs and presentation tiers;
  continuous technique components match within one 1/255 quantization step.
- A fast segment crossing a target counts even when neither endpoint is inside
  it.
- A slow, broadly directed punch still counts.
- Identical centered spatial paths at slow and fast reasonable speeds produce
  the same aim and tier when timing is held constant; speed changes only the
  bounded physical feedback.
- Short and sideways motion does not advance.
- Straight/accurate/timely motion gets a higher cosmetic tier but identical
  progress.
- Retracting below the hysteresis threshold re-arms once without release.
- Retracting, automatic return and a target activating over a stationary glove
  cannot score even when their swept geometry overlaps.
- Holding or stationary drag spam cannot duplicate a hit.
- Both gloves can hit two different live targets on the same simulation step;
  two gloves crossing one single-use target award it only once in stable
  time-of-impact/hand order.
- GLOVE WAKE-UP does not bank either hand until its accepted extension recovers
  below 33% or releases.
- Guard requires a child-caused entry after the tell; no parked/passive glove
  advances it.
- Parry timing quantizes identically across frame partitions; entry in the
  final 25% of counter travel earns exactly one bonus segment, while earlier
  guard entry remains a full success without the bonus.
- A 500 ms rendered-frame hitch consumes no more than eight fixed steps and
  cannot time out an opening before its simulated duration and two render
  acknowledgements. Focus loss freezes all clocks, clears samples/accumulator,
  and resume safely re-cues without a phantom contact or catch-up.
- A 500 ms hitch while a glove is held rebases input time, seeds one
  non-scoring step at the latest target and cannot create a giant unsampled
  sweep, delayed punch, artificial velocity or quality bonus. A real ordered
  target crossing within the retained 533 ms gesture window still counts once
  against the pre-hitch target snapshot.
- The same hitch with a stationary held finger and no new input event rebases
  to the current monotonic clock and cannot leave the gesture cursor stale or
  score the seed.
- Assistance changes geometry/presentation only and never creates work.
- Pearl charge is monotonic and a basic-play path is guaranteed to trigger it.
- Boxer curtain presentation is independent of elapsed completion time; equal
  technique at slow and fast paces produces the same result.
- `ANALYTIC`, `JOLT` and `FAILED_INIT` responder modes produce identical
  progress, completion and normalized gameplay save fields from cloned
  fixtures.
- No authoritative code outside `JoltBagResponder` reads a Jolt body's state;
  the responder exposes presentation pose only.
- Exiting after each completed training phase and reloading resumes at the next
  phase in both first-time and starred replay runs. Missing, malformed,
  negative and above-range checkpoints reset to phase 0 and can never
  manufacture a terminal reward.
- A saved terminal sentinel never awards on passive ticks; one explicit
  Boxer continue input finalizes exactly once, and crash/reload fixtures around
  the transaction cannot duplicate first-time or replay pearls.
- Geometry and contact remain correct through the existing 1280x720 root
  transform on tablet and tall-phone aspect ratios.

## 15. Child playtest acceptance

Test without instrumentation that collects personal data. The supervised
observer records only session notes.

Version 2 is ready when:

- The child discovers the forward punch from the ghost cue within about 30
  seconds without reading.
- Every phase can be completed with one finger and without adult correction.
- Two-finger play works but is never requested by the game.
- The child can predict at least one imp tell on a replay.
- A second playthrough shows a visible opportunity for cleaner aim,
  alternation, timing or recovery, even though the first playthrough already
  completed.
- No miss, imp tap or pause causes visible loss or a request to restart.
- No required gesture rewards frantic speed or uncomfortable repeated motion.
- The whole career ends positively within roughly three to four minutes of
  active play.

Tune geometry and timing from observation, not from making the probe bot's
ideal path the expected child path.

## 16. Implementation slices

1. **Baseline:** preserve V1 captures and trusted probes; record device frame
   timing.
2. **Feel model:** extract fixed-step glove/opponent state, swept contact and
   retraction re-arm with unchanged career progress.
3. **Positive mastery:** add technique events, tiered feedback and monotonic
   Pearl Power.
4. **Training/finale:** retune the existing five modes into the V2 teaching
   ladder and three title rounds.
5. **Device and child test:** tune assists, windows, response latency and
   reduce-motion behavior.
6. **Optional Jolt experiment:** add the one-body responder only after the
   analytic game is green and enjoyable; remove it if the go/no-go gate fails.

Each slice must pass parser/inference gates, the trusted Opera probes, no-input
negative tests and the full project CI before proceeding.

## 17. Explicit non-goals

- No health, lives, damage, knockout, loss, restart demand or negative grade.
- No hook/uppercut requirement, movement stick, stamina or rapid-tap mechanic.
- No player-versus-player, chat, ads, purchases, loot, daily streak or stat
  equipment.
- No new portal, overworld activity, save track or reading-dependent goal.
- No authoritative Jolt gloves, opponent, hit detection or scoring.
- No full-body ragdoll, SoftBody3D, rope simulation fleet or global camera
  shake.
- No destructive edits or recompression of protected art or family voices.
