# Jolt Physics Audit — 2026-07-18

Scope: (1) where the Jolt physics engine is actually used, (2) what would make
the overworld (free-swim reef) feel and control better, (3) where cheap
"basic animation" wins are, using systems the game already has.

---

## 1. Jolt usage: configured everywhere, used almost nowhere (by design)

`project.godot` sets `[physics] 3d/physics_engine="Jolt Physics"` — the Jolt
module built into Godot 4.4. But the shipped game runs **zero physics bodies**
in normal play:

| Site | What it is | Status |
|---|---|---|
| `scripts/main.gd:5748-5880` "PHYSICS LAB" | 6 `RigidBody3D` barrels + 6 balls + 1 `StaticBody3D` floor disc, spawned only from the Developer Mode buttons (`dev_mode.gd:762-773`), shoved by Roshan via `apply_central_impulse` in `_physics_process` | The **only** live Jolt consumer. Dev-only, flagged "M11 grading — cleanse later" |
| `scripts/player.gd` | Plain `Node3D`; hand-integrated swim (accel 43.7, gravity 13, drag `pow(0.18, dt)`), analytic floor/ceiling/dome clamps, cylinder+box soft-solid eject-and-slide | No physics server involvement at all |
| `scripts/physics.gd` (`ReefPhysics`) | The analytic in-house engine (media, substepping, eject-and-slide) | Present as a library, but **only `games/shop.gd:278` (kelp `spring2`) calls it** in this tree |
| `scenes/` | — | No `*Body3D`, `Area3D`, or `CollisionShape3D` anywhere |
| `disabled_addons/tessarakkt.oceanfft` + root `example/` | `BuoyancyBody3D`, `FloatingRectangle.tscn`, `MotorRectangle.tscn` | Dead code. `example/` references the disabled addon and should be deleted alongside it |

**Verdict: keeping Jolt selected is correct and effectively free.** An idle
physics server costs almost nothing per tick, `main._physics_process` early
returns when no props exist, and Jolt is what makes the dev-mode prop
experiment meaningful. The analytic-collision decision is documented and
sound for the target phone (`PHYSICS_ENGINE.md`, CODE_AUDIT_2026_07). Do not
migrate gameplay onto engine bodies.

### Findings / actions

- **F1 — PHYSICS_ENGINE.md overstates reality.** Its "Who uses it" table says
  Roshan, the fetch ball, melody orbs, dolls and the trampoline run through
  ReefPhysics. In this tree only the shop kelp does; the full integration
  lives on the unmerged `physics-engine-improvements` branch (commit
  `a611688` carried the module "as a library"). Either merge that branch's
  player integration (see F3 — it is also the biggest feel win) or mark the
  doc as describing the parked branch.
- **F2 — Physics Lab disposition.** After the Lenovo M11 grading run decides,
  either cleanse (per its own header) or graduate a capped, sleep-enabled
  ring of ≤12 pushable props (barrels near the shipwreck) as ambient toy
  physics. Until then it is dev-gated and harmless.
- **F3 — `example/` folder.** Leftover sample scenes for the disabled ocean
  addon; the only non-dev scene files containing physics nodes. Delete with
  the addon whenever it is finally removed.

---

## 2. Overworld feel & control (free swim in the reef)

Current control model (`player.gd:646-816`): tank-style steering — stick X is
a yaw *rate* (1.8 rad/s flat), stick Y is thrust along facing; constant sink
(gravity 13) countered by SPACE/A/tap "jump" kicks (`vel.y = 16`, 0.4 s
cooldown); water surface is a hard invisible ceiling at `WATER_TOP - 3`;
camera is a 38° diorama chase cam with auto-recentering orbit.

Ranked, smallest-risk-first. **Caution:** probe_audit navigates with the
current constants — anything in tier B changes trajectories and must go one
change per commit through the CI probe gate.

### Tier A — visual-only, zero probe risk

1. **Bank into turns, pitch into climbs/dives.** Roshan rotates flat
   (`rotation.y = yaw + PI` only). Add `rotation.z` lean proportional to
   `turn * speed` and `rotation.x` from `vel.y`, both eased toward zero.
   Mermaids arc; this is the single cheapest "feels like swimming" win
   (~8 lines in `_process` before the camera block).
2. **Speed-reactive camera.** Lerp `cam_back` 25→28 and/or fov 38→41 with
   speed (the Wind Waker sail-stretch). The wake ribbon + speed lines already
   sell sprint; the camera doesn't yet.
3. **Streamline pose at sprint.** The tail amp already scales with speed but
   the arms keep idling. Blend the arm targets toward a swept-back streamline
   pose above ~26 speed (same threshold the speed lines use).

### Tier B — feel constants, probe-gated, one per commit

4. **Surface breach instead of ceiling clamp.** Today jumping at the surface
   silently hits `position.y > WATER_TOP - 3.0 → clamp` — a glass wall, the
   most "wrong-feeling" moment in free swim. The ReefPhysics `Body` was built
   for exactly this (WATER→AIR media switch, `splashed` flag, buoyant
   settle). Merging the parked player integration buys breach arcs + surface
   bobbing in one move; `on_player_jump` splash rings already exist as FX.
5. **Velocity alignment (carving).** Velocity only ever gets thrust along
   facing, so a fast turn skids sideways. Rotating a fraction of the existing
   velocity toward the new facing each frame (`vel` slerped toward `dir` at
   ~2/s, magnitude preserved) makes her carve like a fish instead of
   drifting like a hovercraft.
6. **Speed-shaped turn rate.** Flat 1.8 rad/s is sluggish from rest and
   twitchy at bean-sprint. Scale ~2.2 rad/s at rest → ~1.5 at full sprint.

### Non-goals

Direct camera-relative movement (move stick = world direction) would fight
the diorama lens and the one-finger drag stick; tank steering is the right
model for the player. Keep it.

---

## 3. More basic animations — extend the verb layer, don't add systems

The animation stack is already rich: procedural 26-bone swim, the R2-C
**verb layer** (7 authored gestures with probe signatures), `toy_pose`
choreography, HairSim, rigged critters with real idle/walk/run/happy clips,
and ~34 tweens in main. The verb library is the designed extension point —
each new verb is ~10 lines of `VERB_LIB` data + a `probe_verbs` signature.
No new assets, no new systems:

1. **`point`** — arm extended toward a target. Doubles as the CLAUDE.md
   "visual pointer" every new objective must fire, so it pays for itself.
2. **Collision "boing".** The soft-solid slide already detects inward
   velocity being cancelled; when it cancels more than a threshold, fire a
   short squash/startle verb + a bubble puff. Turns walls from dead stops
   into toys — big deal for a 4-year-old.
3. **`collect` scoop** on treasure/pearl pickup (short two-hand gather,
   reuse the `dig` arm idiom).
4. **Breach somersault** — pairs with finding F3/tier-B4; a `spin`-flagged
   verb (the twirl already proves the mechanism) fired when `splashed`.
5. **Idle variety.** Auto-idle only knows `look` (day) and `sleep` (night,
   `player.gd:884-892`). Add 2–3 more to the pool — hair-twirl, hum with head
   sway, blow-a-bubble (reuse the giggle chest track) — picked randomly.
6. **Social auto-wave.** First time a friend comes within ~10 units while
   idle, `play_verb("wave")`. All the pieces (idle_t, verb cooldown, friend
   positions on main) exist.

---

## Summary

Jolt is correctly configured, deliberately unused outside a dev-gated
experiment, and should stay that way. The feel ceiling is not the physics
engine — it is (a) the parked ReefPhysics player integration (surface breach
+ buoyancy) never having been merged, (b) missing bank/pitch body language,
and (c) the verb layer having only 7 gestures and 2 idle behaviours. All
three are extensions of systems the codebase already owns.
