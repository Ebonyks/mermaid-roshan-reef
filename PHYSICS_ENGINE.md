# The game's physics: ReefPhysics (kinematic feel) + Jolt (rigid dynamics)

The project runs a two-layer physics architecture:

1. **ReefPhysics** (`scripts/physics.gd`) — the kinematic game-feel layer:
   Roshan, minigame bodies, magnets, springs. Documented below.
2. **Jolt Physics** — Godot 4.4's built-in rigid-body engine, enabled via
   `physics/3d/physics_engine="Jolt Physics"` in `project.godot`. It owns
   true dynamics: props that tumble, collide, stack and come to rest.

## The Jolt layer (`_build_jolt_world` in main.gd)

- **Static world collision is baked once from the same analytic oracles the
  kinematic layer uses**: a 141×141 `HeightMapShape3D` sampled from
  `seabed_y()` (~80 KB) plus one static cylinder per entry in the `solids`
  registry. One source of truth, two consumers.
- **Dynamic props** (currently 4 cargo barrels spilled around the shipwreck,
  placed outside the treasure-trigger radius) are `RigidBody3D`s tuned for
  underwater feel: `gravity_scale 0.3`, `linear_damp 1.6` — they sink slowly,
  scoot when shoved, and settle.
- **Roshan couples to Jolt through impulses, not collision**: her motion
  stays fully analytic (she never fights the solver). Each physics tick,
  `main._physics_process` applies a flattened contact shove within 4.5 u
  plus a swim-wake force along her velocity to any prop within 7 u. The
  flattening matters: her analytic floor keeps her above sand-resting props,
  and an unflattened radial push would loft them instead of scooting them.
- Layers: 1 = static world, 2 = props.

### Jolt in the minigames

Per-game rigid bodies live in `game_props` (freed by `_clear_game`; bodies
tagged `no_shove` opt out of Roshan's shove/wake, `ttl` metadata makes
self-freeing debris). Builders: `_jolt_static_box`, `_jolt_ball`,
`_jolt_debris`, and `_slide_plank(..., solid=true)` for visual planks with
matching collision.

- **Go-Kart Cove (`gokart`)** — a NEW minigame, Jolt-native racing: swim to
  the kart pad in the reef (near the west rocks) to race a turtle two laps
  around a walled oval. The kart is a `RigidBody3D` with arcade shaping
  (authored forward speed + tire grip + soft wall bumper + gentle
  auto-align steering, so holding UP races and steering picks your line);
  Jolt owns the wall/floor collisions. The turtle rubber-bands so a child
  at full throttle reels him in and usually wins. `probe_gokart.gd` drives
  it headless.
- **Race (play place / rainbow slide)** — six light Jolt beach balls on the
  arena floor (static ground plate) that Roshan scatters while climbing.
- **Penguin slide** — the chute's planks and rails bake matching static
  collision, and the chase snowball is now a real rolling `RigidBody3D`:
  gravity does the chasing down the grade; the game only intervenes if it
  falls too far behind or catches all the way up.
- **Fairy Pond shooter** — every zapped shadow bug spawns a tumbling Jolt
  debris chunk kicked along the bolt direction (`ttl`-freed, no gameplay
  dependency — pure juice).

**Which layer does a new feature belong to?** If the player or a minigame
needs authored, forgiving, tunable motion → ReefPhysics. If an object should
tumble/stack/roll believably and nothing depends on its exact path → a Jolt
`RigidBody3D` (add it to `jolt_props` to receive Roshan's shove/wake).

# ReefPhysics — the kinematic game-feel engine

`scripts/physics.gd` (`class_name ReefPhysics`) is a self-contained, static,
allocation-free physics module. Everything in the game that moves under
simulated forces now runs through it, replacing the nine hand-rolled
integrators that used to be scattered across `player.gd` and `main.gd`.

## Why isn't Roshan a Jolt body?

The target device is a 3–4-year-old Android phone and the gameplay layer is
authored motion: magnets that pull a 4yo to goals, probes that teleport the
player, forgiving arcade collision. Running the player and minigames through
a rigid-body solver means fighting it with kinematic overrides every frame.
So the game-feel layer stays analytic (ReefPhysics), while Jolt — kept
deliberately small — handles the objects that genuinely benefit from real
dynamics. The Jolt scene stays tiny (one heightfield, ~a dozen static
cylinders, a handful of rigid props), which is well within the phone budget.

## Core ideas

**Media, not weights.** A `Medium` is a rule-set for motion: `gravity`,
`drag` (fraction of velocity retained per second, applied as `pow(drag, dt)`
so it is frame-rate independent), `control` (thrust authority), and
`buoyancy` near the water surface. Presets:

| medium | gravity | drag | control | feel |
|---|---|---|---|---|
| `water_medium()` | 13 | 0.18 | 1.0 | the original hand-tuned swim |
| `air_medium()` | 30 | 0.90 | 0.15 | crisp ballistic breach arcs |
| `land_medium()` | 20 | 0.15 | 1.0 | Sky-Lagoon dream-hop |
| `free_medium(g)` | g | 1.0 | 0 | projectiles / orbs |

A `Body` carries a water medium and an air medium and switches automatically
when it crosses `World.water_y` — that boundary crossing also sets
`body.splashed` so the game can spawn surface FX. Water vs land is therefore
a change of *rules* (can you hover? do you stop when you let go? is jump a
kick or a hop?), not a heavier gravity constant.

**One world model.** `World` describes the environment analytically:
a ground oracle (`seabed_y` / `lagoon_h` heightfields or a flat floor),
ceiling, dome/radius bound, the water surface height, and the game's
existing cylinder+box soft-`solids` registry. `ReefPhysics.collide()` is the
single implementation of the eject-and-slide collision model that
`player.gd` pioneered.

**Fixed substepping.** `step()` integrates in fixed `1/60 s` substeps
(capped), so trajectories are identical at 30 fps on an old phone, 120 fps,
or `Engine.time_scale = 6` in the headless probes.

**States.** After each step a body is `ST_SWIM` (in water — resting on the
seabed still counts as swimming), `ST_GROUND` (on land: idle friction stops
you, SPACE hops), or `ST_AIR` (ballistic, no jump until landing).

## Who uses it

| system | engine features used |
|---|---|
| Roshan (`player.gd`) | full body: media switch at `WATER_TOP` (real surface **breach**), buoyant bobbing at the waterline, land rules in the Sky Lagoon, arena dome/floor/solids |
| fetch ball | `free_medium(9.5)` projectile body |
| Chuck | `toward_xz()` constant-speed seek |
| melody orbs | weightless bodies with `bounce=1` in a reflect `box` |
| dolls (2D) | `Body2D` gravity fall with terminal drift; exponential mouse-follow |
| trampoline (2D) | `Body2D` with restitution on the mat; taps inject `jump_for_height()` energy (was a canned tween) |
| finger chains | `spring2()` damped angular spring |
| penguin slide | `track_speed()` along-grade sled + `lateral()` steering |
| magnets (stars, door, play-place checkpoints, crown updraft) | `magnet()` — the frame-rate-correct exponential form of the old `lerp(delta*k)` pulls |

| shop hanging kelp | `spring2()` pendulums — swing when brushed, settle when left |

Deliberately **not** on the engine: pure choreography — parametric creature
orbits, the fairy-pond rail shooter's positional strafing, the 2D rainbow
slide ride, tween bells. Those are animations, not force simulations.

## Foliage: the engine feeds the GPU, it doesn't replace it

The 2,600+ seagrass/kelp MultiMesh instances are animated by their vertex
shader (`_sway_grass_mat`) — ambient sway costs zero CPU and zero memory per
blade, which is why mass foliage must NOT become physics bodies (thousands of
GDScript spring updates + a full MultiMesh buffer re-upload per frame would
sink the target phone).

Instead, the engine and the shader are bridged by uniforms: every frame
`_tick_foliage_push()` writes Roshan's body position and speed into the few
(memoized) sway materials, and the GPU bends each blade away from her —
meadows part as she swims through, harder the faster she moves. Interaction
lives in the physics state; per-blade motion stays on the GPU.

For plants that deserve true secondary motion (recoil after a brush), use a
`spring2()` pendulum per plant like the shop kelp — dozens are fine, meadows
are not. Rule of thumb: **reacts to gameplay → engine; ambient mass motion →
shader; choreography → parametric.**

## Feel changes shipped with the migration

- **Surface breach**: the invisible lid at `WATER_TOP - 3` is gone; a jump
  near the surface carries Roshan into the air on a real arc with splash
  sparkles both ways, and buoyancy bobs her at the waterline instead of
  pinning her under a ceiling.
- **Sky Lagoon is land**: gravity holds Roshan to the hills, releasing the
  stick stops her (ground friction), SPACE is a hop. Underwater feel is
  unchanged — same constants, same syrup, now only *in water*.
- **Trampoline is physical**: real gravity + restitution instead of tweens.
- **Dolls fall**, they don't ride a conveyor.
- Frame-rate bugs fixed: dolls mouse-follow and garden butterflies were
  per-frame (raced on 120 Hz screens); all magnets now use the exponential
  form the cameras already used.

## Tuning

Player feel constants live at the top of `player.gd` (`SWIM_ACCEL`,
`JUMP_WATER`, `JUMP_LAND`, `TURN_RATE`); medium presets at the top of
`physics.gd`. Equilibrium speed under thrust `a` and drag `d` is
`a / -ln(d)` — water: `43.7 / 1.715 ≈ 25 u/s`, unchanged from the old build.

## Validation

Headless probes (`godot --headless -s scripts/probe_games.gd`, plus
`probe_fetch`, `probe_race`, `probe_mg2d`, `probe_l2`) drive the real game
at `time_scale 6` and assert wins; they are the engine's regression suite.
