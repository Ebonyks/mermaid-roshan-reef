# HitEngine — the shared enemies-get-hit pipeline

`scripts/hit_engine.gd` (`HitEngine`, RefCounted, Phase-7 mold: receives
`main` by reference). Built 2026-07-28. An encounter keeps its enemy
dictionaries exactly as it always has and lends them to the engine, which
adds one uniform interface on top:

```gdscript
he = HitEngine.new(m)
he.fx_root = self          # parent for transient death FX
he.camera = cam            # picking lens (the encounter's own camera)
he.targets = enemies       # the encounter's enemy dicts, by reference
he.on_hit = Callable(self, "_on_engine_hit")   # optional response override

he.tap_pick(screen_pos)    # -> which enemy a screen tap landed on ({} = miss)
he.tap(screen_pos)         # -> tap_pick + hit(enemy, 1, "tap")
he.hit(enemy, dmg, source) # -> THE damage entry point, every source
he.play_death(enemy, style, cfg)   # -> dying-animation library + disposal
```

## Design rules

- **One damage funnel.** Every way an enemy can be damaged — taps,
  projectiles (`"shot_ice"` / `"shot_fire"`), and future COMBO_SYSTEM.md
  verbs (`"mash"`, `"slice"`, ...) — goes through `hit()`. The `source`
  string is the open seam: new damage kinds are new strings, not new code
  paths. When the encounter sets `on_hit` it owns the response (freeze,
  phase rules, befriending); otherwise the default hp pipeline runs and
  plays the enemy's death style at zero.
- **Picking is screen-space unprojection** (InteractionDirector's proven
  technique): no collision shapes, no raycasts, nothing for Jolt to
  simulate, works on dict-driven analytic enemies. Per-enemy knobs:
  `aim_h` (aim-point height), `screen_radius` (generous by default —
  110 px; make bosses bigger).
- **Death styles are cosmetic; state flips immediately.** `play_death`
  sets the record's `state` first (win checks and HUD counts never wait
  on a tween), fires `on_defeated`, then animates. Styles: `"pop"` (the
  arena's popcorn burst, ember-theme aware), `"shrink"` (the brawler's
  scale-away), `"flop"` (comic keel-over, never grim). Disposal per style
  via `cfg.dispose`: `"hide"`, `"free"`, `"keep"`.
- **ENEMY PRIORITY RULE (owner decision 2026-07-28).** Enemies are
  *always* in the forefront of every other object on stage: an enemy
  overlapping any prop/friend/interactable takes the tap, and the object
  under it is not interacted with. Mechanically: encounters append their
  engine to `main.hit_engines` at start (and erase it on every teardown
  path); `main._on_touch_world` gives those engines first refusal on the
  tap *before* `InteractionDirector` picks anything. Only a tap that hits
  no enemy falls through to the world. Level design opts a specific
  encounter out by setting `tap_priority = false` on its engine.
- **No fail states enter through the engine** — it only ever acts on
  enemies, and nothing dies without an input (`probe_hit` proves both the
  miss case and the zero-input case; `probe_passive` still guards the
  global rule).

## Clients

- **CombatArena** (2026-07-28): imps and boss register at `start()`; taps
  route from `touch_ui.world_touched` → `main._on_touch_world` →
  `main._combat_arena_ref()` → `arena.on_world_tap()` (Hybrid mode only —
  Classic has no world-tap concept and keeps the button-only game).
  Tapping an imp freezes it into the existing freeze→popcorn dying
  sequence; tapping the boss follows the same phase rules as the adaptive
  action button. Projectiles funnel through `hit()` too.

## Migration roadmap (one client per commit, probe-gated)

1. `stuffie_battle.gd` `_hit_enemy` → `hit()` with an `on_hit` override
   (dizzy→befriend stays the client's response; probe_stuffie gates).
2. `games/brawl.gd` pop → `hit()` + `play_death("shrink")`; the
   COMBO_SYSTEM.md pop-chain meter hangs off the same funnel.
3. `opera_act.gd` imps/boss.
4. COMBO_SYSTEM.md verb bubbles feed `hit(enemy, dmg, verb)` — the
   `source` seam was shaped for this.

## Probe

`scripts/probe_hit.gd` (in ci.sh): routed-tap → freeze → pop, picking
accuracy (far taps miss), agency (idle frames defeat nobody), boss phase
rules through the engine, and the generic hp pipeline + `"flop"` death +
disposal for engine-only clients.
