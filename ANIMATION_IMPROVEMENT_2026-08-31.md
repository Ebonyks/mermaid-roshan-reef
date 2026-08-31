# Animation improvement — cheapest-wins evaluation (2026-08-31)

_First evaluation of the **Animation improvement wing** (master audit
section 3.4; rules `DL-ANIM-01`–`DL-ANIM-06`, design 06 section 20). Owner
mandate: the most efficient methods of improving animation with the least
investment in compute or behind-the-scenes animation work. Method: a
mechanism-level inventory of the runtime at the current head, then triage
by cost, with the cheapest wins implemented in the same change as
exemplars._

## 1. What the inventory found

- **The vocabulary exists but is fragmented.** `scripts/juice.gd` already
  carried the right discipline (rest-scale memoization, prior-tween kill,
  cosmetic-only contract) but was 3D-typed and nearly unused — 11 call
  sites, 7 of them haptics. Meanwhile ~150 `create_tween` sites hand-roll
  four recurring patterns: scale-pop feedback (~63 `"scale"` tween sites),
  looping A→B→A idles (28 `set_loops`), fade-and-free VFX (~55
  `"modulate"` sites), and rise-and-settle entrances (~72 `"position"`
  sites). De-facto house easing was already consistent (`TRANS_SINE` 72,
  `TRANS_BACK` 33, `TRANS_QUAD` 31) — it just was not written down.
- **The best reward moments had the least motion on the reward.** The
  medal celebration card appeared and vanished instantly (only its sparkle
  ring animated); a collected pearl was `queue_free`d on contact with all
  feedback beside, not on, the pearl; the fairy boss bloom snapped to 0.72
  scale at the win moment. The critter collection pop
  (`scripts/collection_system.gd`) was the lone site doing it right.
- **A latent drift-bug class**: the stuffie QTE telegraph read the live
  `node.scale` as its loop targets, freezing whatever mid-squash scale the
  build frame saw — a hit landing during the telegraph left the enemy
  permanently puffed.
- **A per-call allocation on the universal reward path**: `_sparkle_burst`
  built a fresh `BoxMesh` + `StandardMaterial3D` every call — runtime
  material creation is a named `DL-PERF-03` hard mobile cost, and
  celebrations fire bursts in loops (fairy bloom: one random-color burst
  every 0.18 s).
- **Per-frame decorative trig is real but mostly load-bearing**: the reef's
  `_tick_life` (14 MultiMesh fish transforms × 3 trig each), movers,
  turtle bone poses, god rays, pearls, and friend-orb halos run
  unconditionally whenever `main._process` reaches its tail — including
  under `level2`, `north`, `galaxy`, `ember`, `combat`, `stuffie`,
  `dungeon`, and `opera` (only kart returns early). This is measurable
  compute, but gating it changes what is visible under those modes, so it
  is a measured package, not a blind fix (section 3).

## 2. Implemented now — the exemplar set (this change)

Zero new assets, zero new frames, engine-side tweens only:

| Site | Pattern taught | Change |
|---|---|---|
| `scripts/juice.gd` | The shared vocabulary | `pop_in` (2D entrance), `pulse` (telegraph loop), `vanish` (pickup payoff) join `squash`/`flash`/`shake`; wing bounds `MIN_DUR`/`MAX_DUR`/`MIN_PULSE_PERIOD`. `pulse`/`vanish` are canvas-agnostic by design (`Node` + property-path scale as Variant): the same primitives serve today's spatial arenas and the true-2D migration's cards, and they add zero 3D-API tokens to the GAME2D shrinking manifest — the first push proved the gate works by tripping it with 3D-typed signatures, and the rework keeps the manifest exact |
| `scripts/medal_system.gd` | HUD entrance/exit | Card pops and fades in via `Juice.pop_in`; exit fade rides the existing teardown tween at the same total lifetime; probe-asserted rect, counts, and meta keys unchanged |
| `scripts/stuffie_battle.gd` | Loop hygiene | Telegraph becomes `Juice.pulse(node)` — same 1.18×/3×/0.18 s shape, rest-scale remembered, prior tween killed (fixes the drift bug) |
| `scripts/main.gd` (pearls) | Payoff on the object | `Juice.vanish(p)` replaces instant `queue_free`; the node leaves every logic list first, so count/HUD/save timing is exactly as before |
| `scripts/main.gd` (`_sparkle_burst`) | Allocation-free effects | One shared `BoxMesh` + a quantized per-color material cache (capped); only the particles node is per-call |
| `scripts/games/fairy.gd` | Ease the math you have | Bloom seeds at 0.18 and grows on a cubic ease-out inside the existing per-frame lerp — the pop lands at the win moment; no tween fights the per-frame writer |

Gate: `tools/audit_animation_polish.py` (+ its unittest, both wired into
`scripts/ci.sh`) holds the vocabulary bounds and keeps the exemplars
wired. `probes.yml` wiring is NOT included — workflows are
explicit-task-only; the same two lines are proposed to the owner for the
next explicitly-scoped workflow package.

## 3. Triaged backlog — filed, not improvised

**Apply-as-touched next sites** (each is one primitive call when its file
is next open; `DL-ANIM-02` forbids a bulk retrofit): day-one
room-complete and already-clean beats (`main.gd:6902-6946` — the armed
boss door deserves the entrance beat its message promises), the bathroom
supply-hunt completion (`games/day_one_bathroom_cleanup.gd:679-689`,
which already owns an unused `_spawn_sparkle`), sticker toast and
objective cards already close to the pattern, and the ~60 hand-rolled
scale-pops as their files are touched.

**Measured packages (open findings, not blind fixes):**

- `MA-ANIM-002` back half: state-gate the reef's decorative ticks under
  non-reef modes. Owner-visible composition question (which modes still
  show the reef?) plus a frame-time measurement — coordinate with the
  tablet performance wing (Fable), which owns device numbers; the round
  may prepare the gate behind a report-only flag.
- Companion/room-marker per-frame sin writes: migrate to looping tweens
  only if the tablet wing's captures show `_process` cost there; otherwise
  leave — they are state-gated already.

**Reuse-of-authored-frames shelf (rung 2 of `DL-ANIM-01`, needs no new
art):** Roshan's 128 live cells include 4-keyframe gesture rows that can
be held/ping-ponged for new beats; `SpriteTransition2D` (built, working)
gives 2–4 intermediate states between any two accepted cels;
`RoshanSpriteLoop.setup_sprite_2d` exists with **zero callers** — the 2D
migration's mode work should consume it rather than write a new player.
`roshan_sprite_loop.gd` vs `player.gd` frame-stepping duplication is
consolidation debt for the platform era (M4+), not this wing.

**Rejected for this project:** introducing `GPUParticles2D`/CPU 2D
particle systems (the canvas layer's `_draw()` sparkles are cheaper and
already styled); AnimationPlayer/AnimationTree authoring for feedback
(node-graph overhead for what three tween lines do); any new-frame
generation for feedback purposes (`DL-ANIM-01` rung 3 is for character
acting under section 9 gates, and full-frame cinematic production is out
of scope here entirely); global idle motion on world props (violates
`DL-MOT-03` — idle noise competes with objectives).

## 4. What enters the framework

- The **wing** (master audit section 3.4, Standing) with rules
  `DL-ANIM-01`–`DL-ANIM-06` (design 06 section 20): cheapest-channel
  ladder, one shared vocabulary, engine-side/allocation-free decoration,
  rest-state hygiene, payoff-on-the-object, approved-art transform-only.
- **Deterministic gate** `tools/audit_animation_polish.py` in
  `scripts/ci.sh`; the accepted exemplars are named in design 06 §20 so
  "similar to previous work" is enforceable against actual previous work.
- **Findings** `MA-ANIM-001` (reward beats without motion on the earned
  object — exemplar sites fixed, remaining sites listed) and
  `MA-ANIM-002` (decorative compute: per-call allocation fixed; ungated
  reef ticks open as a measured package).
