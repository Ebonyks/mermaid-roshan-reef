# CAMERA AUDIT & REDESIGN — 2026-07-19

Why this exists: camera-inside-geometry shots are the most common visual failure
in the game right now. Three representative screenshots from the Northern
Kingdom (dark void with HUD only; camera inside a mountain peak; camera inside
the grand-hall wall) share one root cause — **no camera in the project tests
whether its position is inside geometry**. This document is (1) a full audit of
every camera implementation with file:line references, and (2) a redesign that
fits this codebase's analytic-collision world (no physics bodies — a stock
SpringArm3D would fix nothing).

---

## PART 1 — AUDIT

### 1.1 Camera inventory (12 implementations)

| # | Owner | Kind | FOV | Follow / smoothing | Occlusion handling |
|---|-------|------|-----|--------------------|--------------------|
| 1 | `player.gd:1024-1033` | chase (free swim, walk arenas) | 38 +3.5·spd | fixed offset back 25 / high 9, lerp `1-pow(.001,dt)` | **none** (venue hand-tuning + fade_walls only) |
| 2 | `kart.gd` (5 paths: select 2162, paint 2254, countdown 2290, race 3009, podium 3300) | chase | init 68; race band 62–83 | dist 12.5–19, lerp `dt*4` | vertical terrain clamp only, terrain mode only (3026-3029); **float mode: none** |
| 3 | `galaxy.gd` planet 1361-1367 / hall 1692-1697 | spherical chase | 70 fixed | dist 13 / 11.5, lerp `dt*5` | **none** (can clip planet, dome, moons) |
| 4 | `combat_arena.gd:129-135` | static overhead | 58 | none (fixed) | n/a (high angle) |
| 5 | `dungeon_puzzle_room.gd:211-217` | static overhead | 58 | none; cam is a **local var**, unreachable after build | n/a |
| 6 | `stuffie_battle.gd:149-155` | static overhead | 58 | none | n/a |
| 7 | `opera_act.gd:543-549` | static overhead + guest kart engine seizes cam | 56 | none | n/a |
| 8 | `games/fairy.gd:206-208, 362-365` | hijacks `player.cam`, top-down | (player's) | lerp `1-pow(.002,dt)` | none |
| 9 | `games/slide_race.gd:405-408` | hijacks `player.cam` | (player's) | lerp `1-pow(.0008,dt)` | none |
| 10 | `games/side_scroll.gd:63-65, 157-163` | hijacks `player.cam`, side-on | (player's) | lerp `1-pow(.002,dt)` | none |
| 11 | `arena/sky_lagoon.gd:1892-1895` | hijacks `player.cam` for toy-ride moment | (player's) | lerp `1-pow(.05,dt)` | none |
| 12 | `dev_mode.gd:180-203` | dev orbit/top/side/front/tripod | (player's) | lerp, `cam_smooth` | none (dev tool, fine) |

Plus ~30 probe scripts that build throwaway cameras (fine — offline tooling).

### 1.2 Findings, ranked by severity

**F1 (critical) — Zero occlusion/collision handling anywhere.**
`grep intersect_ray|RayCast3D scripts/*.gd` → no gameplay hits. Every chase
camera lerps to a fixed offset behind its subject. Whenever the offset point is
inside a hill, wall, roof, or planet, the camera renders from inside it
(backface culling → void/sky, or a screen-filling wall slab). This is the root
cause of all three screenshots. Note the fix cannot be a physics
raycast/SpringArm3D: world collision is **analytic** — `m.arena_solids`
AABB/cylinder dicts built by `_wall_solid` (`main.gd:1503-1520`) plus height
oracles `northern_walk_h` / `lagoon_walk_h` (`main.gd:3500, 4092`) and
`_terrain_y` in kart. There is almost nothing for a physics ray to hit.

**F2 (critical) — No ground/terrain clamp on the main chase camera.**
`player.gd:1030` sets target y = `position.y + cam_high + cam_pitch_off` with no
height-oracle check. On any downhill walk (Northern entry descends from h≈33.6)
the ground behind and above the player rises over the camera → camera under the
hillside. Kart solved this for itself (`kart.gd:3026-3029`) — the fix never
reached the far more used player camera.

**F3 (high) — Venue framing is hand-tuned from main.gd instead of resolved.**
`player.gd:184` comment admits it: "reduced indoors so the camera does not clip
walls". Ocean castle hall: back 10 / high 4.2 (`main.gd:4321-4322`); restores
25 / 6.5 at three exits (`4744, 5017, 5050`). Two defects:
- **Northern Kingdom got none of this** — its grand hall interior, mezzanine
  and roofed town houses run with the full 25-unit outdoor boom
  (`arena/northern_kingdom.gd` contains zero camera code).
- **Restore drift bug**: boot default is `cam_high = 9.0` (`player.gd:185`) but
  every restore writes 6.5 — framing permanently changes after the first
  interior visit.

**F4 (high) — Teleports and mode exits never snap the camera.**
Worlds sit at huge offsets (northern y=-2200, stuffie -2400, opera -2600,
galaxy +9000). No portal or mode exit repositions `player.cam`; the chase lerp
(~0.1 s half-life, ~1 s to settle) flies the camera through the world on every
transition. Modes 8-11 hijack `player.cam` and leave it parked where the mode
ended, so the resuming chase cam swoops through arbitrary geometry.

**F5 (high) — Fragile, duplicated make_current handoffs.**
- kart/galaxy teardown: conditional `_player_node.cam.make_current()`
  (`kart.gd:3323-3324`, `galaxy.gd:1843-1844`) then `queue_free()` — if the
  guard fails there is **no current camera at all**. No fallback anywhere.
- Only galaxy has a re-assert path after a nested mode
  (`resume_from_combat`, `galaxy.gd:1798-1799`); kart has none.
- Arena modes 4-7 never restore the player cam themselves; restoration lives
  only in main's `_end_*` callbacks (`main.gd:2492, 2538, 2563, 2594`). Early
  exits that skip `finish_cb` — `combat_arena.cancel(false)`
  (`combat_arena.gd:519`, used at `dungeon_level.gd:168`),
  `opera_act.cancel()` mid-race (`opera_act.gd:2268-2284`) — free the current
  camera and rely on an outer owner to re-current one.
- `dungeon_puzzle_room.gd` keeps its cam in a local variable — the mode cannot
  restore or even reference it after build.

**F6 (medium) — Copy-paste divergence.**
The right-stick/right-drag peek is duplicated between `player.gd:1011-1022` and
`galaxy.gd:84-110` ("same feel and constants as player.gd" per its own comment)
and has already drifted: pitch clamp −4.5..8.0 vs −4.0..7.0. Kart never
received peek at all. The static `_build_camera()` body is pasted 4× across the
arena modes with drifting constants (fov 58/58/58/56, offsets (0,31,32) →
(0,24,34)). Smoothing constants differ per file with no rationale
(`pow(0.05,dt)` in sky_lagoon is ~30× snappier than slide's `pow(0.0008,dt)`).

**F7 (medium) — The one occlusion mitigation covers one venue.**
`_tick_wall_fade` (`main.gd:4490-4514`) alpha-fades registered walls that
occlude Roshan (seg-vs-AABB test `_seg_box`, `main.gd:4467-4488`). Registered
only by `arena/castle_hall.gd` (5 sites) and one sky_lagoon wall. Northern
Kingdom registers nothing. Terrain/roofs can't fade anyway — fading is a
complement to, not a substitute for, a boom resolver.

**F8 (low) — Lens/clip-plane hygiene.**
`near` is never set on any gameplay camera (default 0.05) despite ±2600–9000
world offsets and far planes of 1500/2500/default-4000 — needless depth
precision loss on mobile. Kart's init fov 68 (`kart.gd:2082`) sits outside its
own steady-state band 62–83 → visible first-frame FOV jump. `l2` cutscene
(`player.gd:672-675`) freezes the cam wherever it happened to be and only
look_at's.

---

## PART 2 — REDESIGN

### 2.1 Design principles

1. **The camera never renders from inside geometry.** Enforced by a resolver,
   not by per-venue tuning. The diorama art direction (38° long lens, high
   chase) stays — the boom just shortens when reality intrudes.
2. **One implementation, many profiles.** One boom resolver, one peek module,
   one handoff helper. Modes contribute *constants*, not *code*.
3. **Snap on discontinuity, smooth on continuity.** Teleports/mode swaps snap;
   normal play smooths. Boom shortening (obstacle appears) is instant; boom
   recovery (obstacle passed) is smoothed. This is the industry-standard rule
   that prevents both clipping and pumping.
4. **Fit the codebase.** No new scene architecture, no physics bodies. New file
   `scripts/camera_kit.gd` (static funcs, like existing helper style) + small
   patches at the listed sites. Analytic tests only — mobile-cheap (the fade
   tick already does seg-AABB per wall per frame).

### 2.2 The core: analytic boom resolver (`scripts/camera_kit.gd`)

```gdscript
class_name CameraKit
# All queries run against the SAME data player collision uses:
#   m.arena_solids  — AABB {cx,cz,hx,hz,y0,y1} / cylinder {x,z,r,y0,y1}
#   ground oracle   — northern_walk_h / lagoon_walk_h / (reef: seabed) per venue
# so the camera can never disagree with the world the player feels.

# Return the fraction t (0..1] along focus->want at which the segment first
# enters a solid; 1.0 if clear. Slab method per AABB (same math as main._seg_box
# but returning tmin instead of bool), |dxz| vs r for cylinders.
static func boom_hit_t(m: Node, focus: Vector3, want: Vector3) -> float

# Ground oracle sampled at N points along the boom (not just the endpoint —
# a ridge mid-boom must also lift the camera):
static func ground_clear_y(m: Node, focus: Vector3, pos: Vector3, off: float) -> float

# The one entry point every chase camera calls:
static func resolve(m: Node, focus: Vector3, want: Vector3,
		prof: Dictionary) -> Vector3:
	var t := boom_hit_t(m, focus, want)
	var pos := focus.lerp(want, clampf(t - 0.03, 0.08, 1.0))  # skin + min boom
	pos.y = maxf(pos.y, ground_clear_y(m, focus, pos, prof.get("floor_off", 1.4)))
	if prof.has("max_y"):        # interior ceiling envelope (roofs aren't solids)
		pos.y = minf(pos.y, float(prof["max_y"]))
	if prof.has("sphere"):       # galaxy/kart-float planet: [center, min_radius]
		var s: Array = prof["sphere"]
		var d: Vector3 = pos - (s[0] as Vector3)
		if d.length() < float(s[1]):
			pos = (s[0] as Vector3) + d.normalized() * float(s[1])
	return pos
```

Integration in `player.gd` (replacing lines 1024-1033's raw lerp):

```gdscript
var want := position + Vector3(-sin(cyaw) * back_eff, cam_high + cam_pitch_off,
		-cos(cyaw) * back_eff)
var focus := position + Vector3(0, 1.5, 0)
var resolved := CameraKit.resolve(m, focus, want, m.cam_profile)
# asymmetric smoothing: instant in, smoothed out
var cur_len := cam.position.distance_to(focus)
var new_len := resolved.distance_to(focus)
if new_len < cur_len:
	cam.position = resolved                       # snap in — never clip
else:
	cam.position = cam.position.lerp(resolved, 1.0 - pow(0.001, delta))
cam.look_at(focus)
```

**Why this specific shape works here:** every wall the player can't swim
through is already an `arena_solids` entry with a generous pad (0.3–1.6), and
every walkable surface has a height oracle — the two structures the resolver
consumes. Nothing new to author per venue. Cost: N_solids seg tests + ~4 height
samples per frame — the castle hall has the most solids (~60); trivially
cheaper than the sway shaders already running.

### 2.3 Venue camera profiles (kills the main.gd hand-tuning)

One dictionary on main, written by whoever builds/enters a venue, read by the
resolver and the chase offset:

```gdscript
# main.gd
var cam_profile: Dictionary = CAM_OUTDOOR
const CAM_OUTDOOR  := {"back": 25.0, "high": 9.0, "fov": 38.0, "floor_off": 1.4, "far": 900.0}
const CAM_INTERIOR := {"back": 10.0, "high": 4.2, "fov": 38.0, "floor_off": 1.0, "far": 300.0}
```

- `_enter_castle_hall` → `cam_profile = CAM_INTERIOR` (replaces `main.gd:4321-4322`).
- Northern grand hall / mezzanine: `northern_kingdom.gd` sets
  `CAM_INTERIOR` + `{"max_y": <roof slab underside − 1>}` when the player
  crosses the hall threshold (an `arena_zones`-style xz test — the plumbing the
  castle already uses for y-bands), restores `CAM_OUTDOOR` on exit.
- All three exit-restores (`4744, 5017, 5050`) → `cam_profile = CAM_OUTDOOR`,
  which also fixes the 9.0 vs 6.5 drift bug by having exactly one source of
  truth (decide once: 9.0 boot value wins unless Peter prefers the 6.5 feel —
  they've been shipping mixed).
- `player.cam_back/cam_high` become reads of the profile (dev_mode sliders
  `dev_mode.gd:308-309, 748-750` keep working by writing the profile).

### 2.4 Snap-on-discontinuity API

```gdscript
# player.gd
func snap_cam() -> void:
	cam_orbit = 0.0; cam_pitch_off = 0.0
	# compute want exactly as the chase tick does, resolve, place instantly
	cam.position = CameraKit.resolve(...)
	cam.look_at(position + Vector3(0, 1.5, 0))
```

Call sites: every world portal / `_enter_level2` / northern entry / arena
enter+exit, and the teardown of every `player.cam`-hijacking mode (fairy,
slide_race, side_scroll, sky_lagoon toy ride). This removes the through-world
swoop (F4) with one line per site.

### 2.5 Handoff: one helper + a watchdog

```gdscript
# camera_kit.gd
static func restore_player_cam(m: Node) -> void:
	if m.player != null and m.player.cam != null and m.player.cam.is_inside_tree():
		m.player.snap_cam()
		m.player.cam.make_current()
```

- Replaces the four guarded restores in main.gd `_end_*` and the two mode
  teardowns (`kart.gd:3323`, `galaxy.gd:1843`).
- **Watchdog** (2 lines in `main._process`): if
  `get_viewport().get_camera_3d() == null` → `restore_player_cam(self)`.
  Converts every "freed the current camera" bug (F5's cancel(false) paths,
  dungeon's local-var cam) from a black screen into a self-heal.
- Mode contract, documented at the top of camera_kit.gd: *a mode that calls
  make_current() must call restore_player_cam() in its teardown — including
  cancel paths; the watchdog is a net, not the mechanism.*

### 2.6 One peek module

Move `player.gd:1011-1022` into `CameraKit.tick_peek(state, input...) ->
Vector2` (orbit, pitch) with the constants defined once (gamepad 2.6/9.0 rates,
mouse 0.005/0.02, clamps ±PI·0.9 and −4.5..8.0, return-drift pow(0.35,dt)).
player.gd and galaxy.gd both call it (fixes the drifted galaxy pitch clamp);
kart can opt in later for free.

### 2.7 Mode-specific fixes

- **kart float mode**: pass `{"sphere": [BW_CENTER, BW_RADIUS + 3.0]}` in its
  profile — stops camera-through-planet on the rainbow race. Set init fov to
  62.0 (`kart.gd:2082`) to kill the first-frame jump.
- **galaxy**: same sphere clamp `[ORIGIN, PLANET_R + 2.5]`; hall mode gets
  `max_y` under the hall ceiling.
- **Northern Kingdom fade walls**: register the grand-hall side walls and the
  town house walls into `fade_walls` via the existing `main.gd:1534` helper —
  complements the shorter interior boom exactly as in the ocean castle.
- **Clip planes**: `near = 0.3` on all gameplay cams; `far` from the venue
  profile (outdoor 900 covers the 720u northern strip with fog; interiors 300).
- **Static arena cams (4-7)**: leave as-is visually (high angles don't clip);
  just route their teardown through `restore_player_cam` and store dungeon's
  cam in a member var.

### 2.8 Rollout order (each step independently shippable, probe-gated)

1. **P0 — player.gd resolver + ground clamp + snap_cam + watchdog + northern
   interior profile.** This alone eliminates every reported screenshot class.
2. **P1 — profile system replacing main.gd hand-tunes; restore-drift fix;
   near/far; northern fade_walls.**
3. **P2 — shared peek; kart/galaxy sphere clamps; kart FOV init; handoff
   helper adoption in all mode teardowns.**
4. **P3 (optional polish)** — occlusion-aware look-ahead (bias `focus` toward
   velocity), per-venue smoothing constants table, kart peek.

### 2.9 Verification — `scripts/probe_camera.gd`

New probe, pattern of `probe_northern.gd` (walks routes with per-frame vel,
wall-clock paced — static sampling is proven insufficient, see 2026-07-13
lesson) plus the screenshot-probe pattern (`probe_castle_shots.gd`, non-headless)
for eyeballs:

- Routes: northern spawn → forest downhill → town street → hall threshold →
  mezzanine stairs → back out; ocean castle hall full loop; reef open water.
- Per-frame asserts: (a) `cam.position` inside no `arena_solids` entry
  (point-in-AABB/cylinder), (b) `cam.y >= walk_h + 0.4` in walk arenas,
  (c) a current camera exists (`get_camera_3d() != null`) across every
  mode enter/exit in the route (combat in/out, toy ride in/out).
- Screenshot set at the three known-bad spots from this audit's screenshots.
- Add to `ci.sh` trusted list — `probe_northern`'s silent breakage showed
  untrusted probes rot.

### 2.10 Risks / notes

- **Analytic solids don't cover authored GLB props** (trees, houses use
  `_wall_solid` only where a blocker was added). Where a prop lacks a solid the
  camera can still enter it — same as the player can. Acceptable: player-reach
  parity, and P0's ground clamp covers the terrain cases that dominate.
- The resolver reads `m.arena_solids`, which is rebuilt per venue — cheap, but
  the reef (non-arena free swim) has few solids; ground clamp there should use
  the seabed/terrain height the reef tick already knows.
- Multi-session repo: land P0 as one narrow commit on a `claude/camera-rig`
  branch per AGENTS.md; the fade-wall registrations for northern are a separate
  commit (touches northern_kingdom.gd, which other sessions are active in).
