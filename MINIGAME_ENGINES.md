# Minigame engine consolidation — audit & plan (2026-07-18)

Owner direction: the minigame roster keeps growing; instead of every new game
bringing its own loop, camera, and input code, the game should run on a small
set of **key engines** that take per-game configuration. Goals: smaller code
(and APK), smoother play on the M11, and one touch grammar a 4-year-old only
has to learn once.

This document is the game-wide audit of every playable mode, the recommended
engine set, and the migration map. First shipped step: the **SideScrollStage**
engine (`scripts/games/side_scroll.gd`) with the rebuilt 2.5D catch-the-babies
nursery as its first client (see §7).

---

## 1. What exists today — full mode inventory

Two architectural families, which do NOT share a base:

- **Family A — arena satellites** (`scripts/games/*.gd`, RefCounted, state on
  `main.g`, driven by main's `_start_game → _tick_game → _end_game`
  lifecycle, nodes reclaimed by `_clear_game` via `game_nodes`).
- **Family B — standalone mode nodes** (`kart.gd`, `galaxy.gd`,
  `combat_arena.gd`, `dungeon_level.gd`, `dungeon_puzzle_room.gd`,
  `dance_engine.gd`: own `_process`, own camera/HUD/env save-restore, report
  back through a `finish_cb`).

| Mode | File (lines) | Perspective | Core verb | Input today |
|---|---|---|---|---|
| Fetch (Chuck) | games/fetch.gd (318) | 3D free-swim arena | timed aim + throw | tap/Space |
| **Dolls** | games/dolls.gd | **2.5D side-scroll stage** (was 2D canvas) | **catch falling babies** | stick/keys/drag |
| Seek (Lamb-a') | games/seek.gd (159) | 3D free-swim arena | hide & seek | face buttons + swim |
| Treasure | games/treasure.gd (113) | 3D free-swim arena | checkpoint chain | swim |
| Melody | games/melody.gd (532) | 3D free-swim theater | collect 7 orbs | swim |
| Shop | games/shop.gd (431) | 3D free-swim cabin | browse/buy | proximity + tap |
| Play-place course | games/slide_race.gd (a) | 3D vertical course | checkpoint chain | swim |
| Penguin/rainbow slide | games/slide_race.gd (b/c) | 3D on-rails downhill | steer, collect/chase | stick x |
| Fairy pond | games/fairy.gd (640) | **overhead auto-scroll shooter** | dodge + auto-shoot + nova | stick + tap |
| Kart race | kart.gd (3323) | 3D spline racer | steer/drift/turbo | stick + tap |
| Galaxy | galaxy.gd (1841) | 3D spherical platformer | explore/collect | stick + tap |
| Combat arena | combat_arena.gd (533) | overhead octagon | dodge + one-button shoot | stick + tap |
| Dungeon | dungeon_level.gd + dungeon_puzzle_room.gd (639) | overhead octagon rooms | combat/puzzle alternation | stick + tap |
| Picture games ×5 | games/picture_games.gd (593) | 2D canvas | tap-to-place / chase | tap, stick |
| Dance | games/dance_engine.gd (509) | 2D canvas rhythm | tap lanes on beat | lane buttons |
| Critter collection | collection_system.gd (452) | ambient in-world | approach + catch | tap |
| Stuffie battle | stuffie_battle.gd | overhead octagon, YOU are the creature | one-button attack + DODGE QTE | stick + tap + big dodge bubble |
| Companion wing | companion.gd | ambient in-world | follow / tokens / den entrance | proximity + tap |

### Duplication found by the audit (the cost of no engines)

1. **The composite input read** (`keys ∥ joy_axis ∥ touch_ui.stick_vec`, and
   `Space ∥ joy A/B ∥ touch_ui.action`) is re-implemented ~12×; kart.gd and
   galaxy.gd even re-declare their own `joy_axis`/`joy_pressed` copies of
   main's.
2. **Horizontal catcher/mover**: dolls, the picture-game snowman chase, and
   the slide steer are the same left/right verb written three times.
3. **Collect-N / checkpoint chain**: slide course, treasure, melody orbs,
   critter collection, picture-game garden/xmas — five implementations of
   "fixed set → proximity → count to N → sparkle + reward."
4. **Overhead room rig**: combat_arena and dungeon_puzzle_room duplicate the
   `CENTER`, camera, avatar, `_move_input`, `_action_pressed`, and env
   save/restore nearly verbatim.
5. **Primitive-art toolkit** (`_mat/_box/_sphere/_soft_mat` variants) copied
   ~5× (main, melody, combat, puzzle, kart/galaxy tints).
6. **Reward funnels**: `_reward()` is the intended single RewardDirector, but
   picture-games, kart, combat, and dungeon each carry bespoke
   pearl/sticker/save code beside it.
7. **No-fail mercy logic** ("never fail, escalate help") re-invented per game
   (dolls drop-spread, fetch arc-widen, slide magnets, fairy `fs_fails`,
   seek help radius).

---

## 2. One universal engine, or several? (evaluated)

The tempting alternative is a single `MiniGameEngine` API that every game —
dungeon, catcher, runner, shooter, racer — configures. Evaluated honestly:

**What a single API would buy.** One lifecycle to learn and probe; plumbing
(input, rewards, mercy, teardown) written exactly once; every new game is
"just config"; accessibility and safety rules (no-fail, voice objectives,
tap targets) enforced in one place instead of promised in eight.

**Why a single API fails at the simulation layer.** The games genuinely
disagree where it matters most — the *feel*:
- **Kinematics:** a drift-charging kart on a banked spline, a gravity-fed
  slide, a hovering catcher on a line, and a globe-walker share no motion
  math. A config flag per behavior turns configs into a worse programming
  language than GDScript.
- **Camera:** chase-on-spline, side-on glide, top-down scroll, and octagon
  overhead are four different rigs with four different tuning surfaces; feel
  work (KART_FEEL.md-style) needs each to stay small and owned.
- **The god-object lesson is already in this repo:** main.gd at ~8.9k lines
  *is* the one-engine-that-does-everything, and every phase since has been
  spent taking it apart. A universal engine rebuilds that problem one level
  down, with every game paying the complexity of every other game's
  features — and a regression in the shared simulation breaks all ten games
  at once instead of one.
- **Probe determinism:** analytic, per-mode simulations are why the bots can
  drive every game; a mega-engine's interacting feature flags multiply the
  state space the probes must cover.

**The synthesis that IS strong enough to support all of them: one contract,
few engines.** What is truly identical across every minigame is not the
simulation — it is the *plumbing*. So standardize that as the single
**MiniGame contract** every game (and every engine) sits on:

1. **Lifecycle** — `build(cfg) → tick(delta) → end(win)`, teardown through
   `game_nodes`/`_clear_game`, state on `main.g` (already Family A's shape;
   Family B's `finish_cb` nodes migrate to it over time).
2. **GameInput** — the one-finger grammar (drag/point ∥ stick ∥ keys ∥ pad,
   tap = THE button) read from one helper, never re-implemented.
3. **RewardDirector** — every win funnels through `_reward()`; no bespoke
   pearl/sticker/save code.
4. **Mercy hooks** — a standard "escalate help on struggle" pattern (widen,
   slow, magnetize) instead of per-game reinvention.
5. **Objective voice + pointer** — firing `_say()` + golden pointer is part
   of the contract, so the non-reader rule can't be forgotten.
6. **Probe surface** — objective state readable from `main.g`, motion
   analytic, so one bot pattern drives any conforming game.

Under that single contract sit the **four perspective engines** below — each
owning one kind of simulation and camera — and games become thin objective
scripts on top. New minigame cost drops to "pick an engine, write the
objective"; the feel stays hand-tuned per perspective; and nothing ever
grows big enough to become the next main.gd.

## 3. Recommended engine set: **four engines + two kits**

More than four adds abstraction without coverage; fewer forces perspectives
that don't mix (a side-scroller and a spline racer share almost no math).
Every engine keeps the hard rules: mobile renderer, no fail states, voice +
pointer objectives, one finger + one button.

### E1 — Adventure/room engine (the dungeon-action interface)
The owner's "dungeon / action-adventure" engine. Today three files share one
overhead-room formula; consolidate into a `RoomStage` base owning the octagon
camera rig, avatar, env save/restore, HUD strip, and the one-button verb read.
- **Absorbs:** `combat_arena.gd` (encounter configs), `dungeon_puzzle_room.gd`
  (puzzle configs), `dungeon_level.gd` (stays as the room sequencer).
- **Grows into:** the ZELDA_GAMEPLAY_WORKORDER path — the same room logic
  played embodied in real arenas by `player.gd` (workorder item S1), plus the
  grab/push/switch verb set. New "dungeon-type adventures" are then room
  tables + encounter dicts, not new code.

### E2 — Side-scroll stage engine (SHIPPED: `scripts/games/side_scroll.gd`)
The catch-babies interface, rebuilt per owner direction as a 2.5D stage: the
**real 3D Roshan** (wardrobe skin included) on a left/right line before a
side-on camera, 3D-meshed babies falling in front of the nursery book page.
- **Modes:** `tick()` = steer-on-a-line (catch games); `run_tick()` = the
  Mario-run seam — auto-run + tap-to-hop, in the engine, no client yet;
  `brawl_tick()` = **walk-the-plane with depth** (Castle Crashers style):
  x + z inside a band, a sliding stage window for gated wave progression,
  facing the run, tap = the bop.
- **Two heroes:** `companion_open`/`companion_tick` put a second hero on the
  plane as an illustrated-cutout billboard (per the art direction). AI-driven
  by default; a second gamepad takes her over the moment its stick moves and
  hands back after 4s idle — player 2 when present, helper when not.
- **Owns:** the unified one-finger read (drag-to-point ∥ stick ∥ keys ∥ pad).
  In brawl mode P1's pad reads are device-0 only so pad 2 belongs to the
  companion.
- **Clients:** dolls (catch), **toy-castle brawler** (`games/brawl.gd`,
  brawl — Huluu the stuffie is player 2; her stuns assist but only Roshan's
  tap pops an imp, so the AI partner can never hand a passive run a win).
  **Next:** picture-game snowman chase (catch), one-touch runners (run).

### E3 — Overhead scroller/shooter engine (the fairy bullet-heaven interface)
`games/fairy.gd` already is this engine in shape (auto-scroll track, dodge
window, auto-fire, mercy escalation, boss phases) — it is just single-tenant.
Parameterize it like the kart: `configure({track_len, scroll_speed, waves,
hazards, boss, skin})`.
- **Absorbs:** fairy pond (first client, unchanged behavior).
- **Grows into:** any future top-down dodge/collect/shoot game (garden-pest
  chase, bubble parade…) as config tables. Combat-arena movement could
  eventually ride it too, but E1 is its better home (room-based, not
  scrolling).

### E4 — Race/rail engine (exists: `kart.gd`, see RACE_ENGINE.md)
Already the proof that the engine approach works: one config-driven node
(themes, tracks, vehicles, hazards, payouts). Keep it.
- **Candidate merge:** the penguin/rainbow slide (slide_race.gd modes b/c) is
  a second spline-rail implementation (Catmull-Rom + arc-length LUT, steer-x,
  chase cam — kart has all of these). Long-term: a `rail` preset of the kart
  engine (gravity-fed, no AI pack). Short-term: keep, but move its spline
  sampling to a shared `Spline3` helper so the math exists once.

### K1 — Course/collect kit (library, not an engine)
The "spawn set → magnet/assist → count to N → reward" loop as a helper the
3D free-swim games call. **Precedent already in-tree:** treasure has no tick
of its own — it runs on slide_race's `_tick_course`. Extend that pattern to
melody's orbs and the picture-game tap-sets instead of new engines: these
games' identity is their set dressing, not their loop.

### K2 — Canvas kit (already shared)
`picture_games.gd`'s letterboxed stage + widget factories + `_mg2d_win`
reward flow, and `dance_engine.gd`. Fine as-is; don't force 2D book-art games
into 3D engines. Snowman-chase graduates to E2; the rest stay.

**Deliberate one-offs (do not engine-ize):** galaxy.gd (a single bespoke
level; generalizing a planet-walker for one client is negative-value),
shop.gd and seek.gd (their loops are their content; K1 helpers only), and
fetch.gd (timing minigame, shares only input/reward plumbing).

---

## 4. The single touch interface

One grammar across every engine, so the player's hand never re-learns:
- **drag / hold** = point where to be (stage games) or steer (stick emerges
  under the finger — touch_ui already does this in-world)
- **tap** = THE button (throw, nova, turbo, hop, buy)
- nothing else. No gestures, no multi-touch requirements, no reading.

Implementation path: `SideScrollStage.tick()` is the first engine-owned
composite read. Next mechanical step: lift it into a small static
`GameInput` helper (`axis_x()`, `axis(vec)`, `tap_just()`, `point_x()`)
and delete the ~12 per-game copies one game per commit, probe-gated —
including kart/galaxy's private `joy_axis` clones. That helper is also where
a future accessibility tweak (bigger dead-zones, hold-assist) lands once for
every game at the same time.

## 5. Consolidation map

| Game | Runs on (now) | Target | Effort |
|---|---|---|---|
| Dolls | **E2 SideScrollStage** ✅ | — | done |
| Toy-castle brawler (co-op) | **E2 brawl mode** ✅ | — | done |
| Snowman chase (picture) | bespoke canvas | E2 catch mode | small |
| Future one-touch runners | — | E2 `run_tick` | config only |
| Fairy pond | bespoke (engine-shaped) | E3 via `configure()` | small |
| Combat arena | bespoke | E1 RoomStage | medium |
| Dungeon puzzle rooms | bespoke | E1 RoomStage | medium |
| Dungeon sequencer | dungeon_level.gd | E1 (unchanged role) | none |
| Kart / future races | **E4** ✅ | — | done |
| Penguin + rainbow slides | slide_race.gd rails | shared spline helper, later E4 `rail` preset | medium |
| Treasure | slide course tick ✅ | K1 (formalize) | small |
| Melody orbs | bespoke collect | K1 | small |
| Play-place course | slide_race.gd | K1 host | none |
| Garden/xmas/trampoline/slide (picture) | K2 canvas kit ✅ | — | none |
| Dance | own node | K2 neighbor; leave | none |
| Fetch / Seek / Shop / Galaxy | bespoke | leave (one-offs) | — |

## 6. What this buys

- **Code/file size:** the duplicated input reads, room rigs, spline math, and
  primitive-art kits are the bulk of the ~5.9k lines in combat/dungeon/slide/
  fairy outside their actual game rules; consolidation converts future games
  from ~500-line files into config tables, and is the main lever for the
  main.gd < 2.5k refactor target beyond the Phase-7 extractions.
- **Smoothness:** engines own their camera and assist logic, so feel fixes
  (banking, mercy tuning, camera breathing) land once and every client game
  inherits them — the way KART_FEEL.md gates already work for races.
- **Probe cost:** one probe per engine exercises every client's shared
  machinery; per-game probes shrink to objective checks.

## 7. Migration order (each step mechanical, probe-green before merge)

1. ✅ **E2 shipped** — SideScrollStage + dolls 2.5D rebuild (this branch).
2. Snowman chase → E2 catch mode (deletes the duplicate mover).
3. `GameInput` helper; adopt in Family-A games, then kart/galaxy.
4. Fairy → E3 `configure()` (behavior-preserving parameterization).
5. RoomStage base under combat + puzzle rooms (E1), per the Zelda workorder's
   S1 so embodied rooms land on the same base.
6. `Spline3` helper shared by kart + slide; evaluate the E4 `rail` preset.
7. Formalize K1 (course/collect) API; move melody orbs onto it.

Per the refactor rules: extractions stay mechanical, one move per commit,
behavior identical unless the change *is* the task (as the dolls rebuild was).

---

## 8. SideScrollStage API (engine E2)

`scripts/games/side_scroll.gd`, RefCounted satellite (state on `main.g`
`ss_*` keys; every node registered in `main.game_nodes` so `_clear_game`
reclaims the stage).

```gdscript
# scale note: the v4 Roshan is ~7 world units tall (3.7× model scale in
# player.gd) — stages are sized against HER; the 2D era maps at 25 px/unit
var stage := SideScrollStage.new(main)
stage.open({
    "origin": main.ARENA_POS + Vector3(0, 2.5, 0),  # stage floor center
    "half_w": 23.2,           # playfield half-width (world units)
    "hover": 3.0,             # avatar float height above the floor
    "steer_speed": 24.8, "bob_amp": 0.5,
    "cam_h": 12.0, "cam_dist": 20.5, "look_h": 10.5, "cam_follow": 0.25,
    "backdrop": "res://assets/book/nursery_bg.jpg",  # optional book-page mural
    "backdrop_size": Vector2(36.0, 49.8), "backdrop_z": -28.0,
    "run_speed": 20.0, "jump_v": 30.0, "gravity": 64.0,  # run mode only
})
var s := stage.tick(delta)   # catch mode: {"mx", "px", "moved"}
var r := stage.run_tick(delta)  # run mode: {"x", "y", "grounded", "hopped"}
var b := stage.brawl_tick(delta)  # brawl: {"mx","mz","px","pz","tap","moved"}
stage.set_bounds(l, r)   # brawl: the sliding stage window ("half_d" = depth)
stage.companion_open(tex, height, start)   # player-2 cutout hero
var p2 := stage.companion_tick(delta, want_x, want_z, speed)
	# → {"x","z","tap","human"} — AI toward want unless pad 2 is live
stage.root()   # the stage Node3D — parent set dressing & fallers under it
stage.glow(color, size)   # additive billboard halo for pickups/fallers
stage.close()  # safe when never opened; called from _clear_game
```

The engine drives the **real player node** (position, lean, facing) and
`player.cam`; `player.gd` skips its own movement/camera for `game == "dolls"`
(the same self-driven list as slide/fairy/kart). Composite input: arrows/AD ∥
gamepad left-x ∥ virtual stick ∥ press-and-point (emulated mouse from touch —
one finger points where Roshan should swim). `moved` feeds the Phase-6 verb
gate so passive runs can never win a catch game.

Dolls stage geometry (for probe writers): stage-local x ∈ [−23.2, 23.2],
babies spawn at y 28, catchable below y 8.8 within |Δx| < 5.4, missed at
y 1.2 (pillow landing). `main.g["dolls"]` holds the falling `Node3D`s;
`probe_audit.gd` chases the lowest baby's `global_position.x` against
`main.player.global_position.x` through the touch stick (gain 1/3.6 units).
