# ReefPhysics — the game's unified physics engine

`scripts/physics.gd` (`class_name ReefPhysics`) is a self-contained, static,
allocation-free physics module. Everything in the game that moves under
simulated forces now runs through it, replacing the nine hand-rolled
integrators that used to be scattered across `player.gd` and `main.gd`.

## Why not Godot physics (Jolt)?

The target device is a 3–4-year-old Android phone. The world is procedural
(analytic heightfields, dict-based solids), so adopting engine bodies would
mean baking collision shapes for everything and paying the physics-server
cost per frame. ReefPhysics keeps the game's proven analytic collision model
but gives it one correct, shared implementation.

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

Deliberately **not** on the engine: pure choreography — parametric creature
orbits, the fairy-pond rail shooter's positional strafing, the 2D rainbow
slide ride, tween bells. Those are animations, not force simulations.

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
