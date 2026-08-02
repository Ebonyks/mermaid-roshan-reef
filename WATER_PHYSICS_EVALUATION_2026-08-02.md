# Water physics evaluation — Jolt water transitions across the game (2026-08-02)

Scope: (1) how widely the Jolt-based water physics system — objects
transitioning in and out of water — has actually been instituted, zone by
zone (lagoon, castle, every other body of water); (2) the recommended way to
integrate visual animations and effects into it; (3) how effects should
*proc* (trigger) on each system so the game keeps one continuous water
language. Companion handoff for the art:
`CODEX_WATER_FX_WORKORDER_2026-08-02.md`.

Successor to `JOLT_PHYSICS_AUDIT_2026-07-18.md` (still accurate for the
engine-selection rationale) and written against the 2.5D charter
(`GAME_REDESIGN_2P5D_2026-07-27.md`) and
`VISUAL_DESIGN_AUDIT_2026-07-28.md`.

---

## 1. Verdict up front

**The Jolt water system exists as a finished, probe-gated engine primitive
with zero shipped consumers.** The prop fleet + swell tide in
`scripts/games/side_scroll.gd` (built 2026-07-27) is exactly the intended
"objects transitioning in and out of water" system — waterlogged rigid
bodies riding a shared wave, wake-shoved by Roshan — and it is complete,
tuned, and covered by a trusted probe (`probe_props.gd`, including a
dedicated swell case). But no live zone opts in:

| Zone / water body | Jolt water system? | What it actually runs |
|---|---|---|
| Reef free swim (surface breach) | **No** (analytic) | Inline ReefPhysics media rules in `player.gd:661-705`: water→air swap at `WATER_TOP`, buoyant band, splash ring + sparkles + twirl verb on crossing. The only *live* water-transition physics in the game. |
| Sky Lagoon — shipped 2.5D promenade | **No** | `sky_lagoon_promenade.gd` never calls `props_arena()`, never spawns a `prop()`, never sets `cfg.swell` — the tide and fleet have never run in the shipped game. |
| Sky Lagoon — legacy 3D (rivers, moat, ponds, fairy pond) | **No** | Carved terrain water sheets with `_toon_water_mat`; wet/dry medium switch via the `land_dry` oracle, but **no splash FX proc** on entering/leaving rivers or the moat. No bodies. |
| Pearl Castle (all 21 interior stages) | **No** | `castle_rooms_25d.gd` — pure 2D. Water is depicted by deterministic frame atlases + sound: bathtub (`turn_taps_and_fill_bubbles`, 3×3 atlas), sink, toilet, rubber duck, and the mermaid-pool room's waterfall / bubble fountain / floats. Note: `scripts/arena/castle_hall.gd` (named in CLAUDE.md) no longer exists; the castle went 2.5D. |
| Bubble-bath bathtub specifically | **No** | The eight-frame fixed-pivot tap/water/bubble atlas (`bubble_bath_bathtub_atlas.png`). It is the best-looking water *animation* in the game and involves no physics at all. |
| Fetch lake (Chuck) | **No** | Splashes are pure logic — a miss counter, a message, 💦 pips (`games/fetch.gd:208-278`). |
| Northern Kingdom (fords, splash pool, frozen fountain) | **No** | Painted/analytic terrain dressing (`arena/northern_kingdom.gd`). |
| Physics lab (dev mode) | **Yes** | `main.gd:7080-7154`: 12 Jolt barrels/balls plus the `_physlab_standees()` preview of the prop fleet with waterlogged tuning. Dev-gated, never reachable in normal play. |
| oceanfft buoyancy addon | Dead | `disabled_addons/` + root `example/`; stays dead per the swell's own header comment. |

Two clarifications the owner should have straight:

1. **"Jolt everywhere" was never the design.** The binding pattern is
   *"logic analytic, garnish Jolt"* (`JOLT_PHYSICS_AUDIT_2026-07-18.md`,
   restated in `side_scroll.gd:675-686` and `MINIGAME_ENGINES.md`). Roshan,
   objectives, and anything win-critical stay on the analytic ReefPhysics
   model; Jolt bodies are cosmetic garnish with a hard fleet cap
   (`PROPS_MAX := 12`) and a sleep contract. That is the right call for the
   Helio G88 phone and must not change.
2. **The transition machinery is double-built and half-connected.**
   `ReefPhysics.Body` has first-class surface-crossing support —
   `world.water_y` plus a `splashed` flag (+1 entered / −1 left,
   `physics.gd:101,163-166`) purpose-built for spawning surface FX — and
   **nothing consumes it**: the only live ReefPhysics call anywhere is the
   shop kelp spring (`games/shop.gd:278`). Meanwhile the player's shipped
   breach re-implements the same rules inline. The `splashed` flag is the
   natural proc point the FX work below should finally cash in.

### How the swell + prop system works (for reference)

- `prop()` (`side_scroll.gd:722`) — a "physical standee": a flat sprite
  cutout on a real `RigidBody3D`, alpha-scissor quad, axis-locked so it
  only tumbles in the screen plane, low-friction toy material,
  sleep-enabled, capped at 12 per stage. `props_arena()` builds the
  invisible static shell (floor slab + 4 walls) that contains them.
- The **swell** (`side_scroll.gd:796-829`) — one deterministic traveling
  wave, a pure function of stage clock and x (~11 s period, ~105-unit
  wavelength), sampled by every motion channel: awake bodies get it as a
  real solver force fading over ~6 s since last disturbance; **sleeping
  bodies rock only their sprite** (never woken — the perf contract);
  Roshan's hover and the parallax layers add the same phase.
- **Pairing rule** (in-code, binding): a swell stage waterlogs its props —
  `gravity_scale ≲ 0.4`, `damp ~1.0` — so the tide out-pulls friction on
  buoyant bodies only. Deck furniture stays put; sea toys drift.
- Proven by `probe_props.gd` (shove coupling, fleet cap, sleep contract,
  and all three swell contracts) on every CI push.

**The gap, in one sentence: the water physics system is done; the game
just doesn't use it yet — and the FX layer that would make its
transitions *visible* was never designed.** That FX layer is what the rest
of this document and the Codex handoff specify.

---

## 2. How visual animations and effects should integrate

### Principle: physics decides *when*, traditional animation decides *what it looks like*

Every water system the game has (or will get) already emits — or can
trivially emit — a small set of **discrete events**. Visual effects should
be authored as **Codex-painted frame atlases** (traditional, hand-timed
animation in the bathtub-atlas idiom — the proven best-looking water in the
game) and *proc'd* from those events. No shaders beyond the existing
`_toon_water_mat`, no GPU particles for the core vocabulary, no physics in
the FX themselves. This keeps effects:

- **identical across renderers** (Mobile everywhere — hard rule),
- **deterministic** (probes can assert "a splash card spawned", never
  "the particles looked right"),
- **cheap** (one alpha quad playing an atlas, exactly like the 44-card
  promenade already renders), and
- **stylistically owned by Codex**, which per the 2026-07-27 owner decision
  outranks every other art channel.

### The shared water-FX vocabulary

One small set of atlases, reused *everywhere* water appears, is what buys
visual continuity. The full art spec is the Codex workorder; the engine
side needs exactly one new primitive:

`fx_card(atlas, pos, size, cfg)` — spawn an unshaded alpha-scissor quad at
a real world position/depth, step through the atlas frames on the fixed
timings the castle interactions already use (`frame_duration` per spec),
free itself on the last frame. One implementation on `SideScrollStage`
(promenades + castle rooms via their canvas equivalent) and one thin
`main.gd` wrapper for the 3D free-swim world. Cap: ≤4 concurrent FX cards
per stage, oldest evicted — same spirit as `PROPS_MAX`.

Because the card sits at the *object's* depth in 2.5D stages, the depth
buffer sorts it against standees and Roshan correctly — effects obey the
same layering law as everything else in the redesign (and unlike the
living-world screen overlay, which `VISUAL_DESIGN_AUDIT_2026-07-28.md`
§3.6 already flags as the wrong home for world FX).

### Proc points, per system

| System | Event source (exists today) | Effect proc'd |
|---|---|---|
| Prop fleet (Jolt) | `props_tick()` — impulse magnitude at wake; sleep→wake transition; a new one-line surface check when a stage declares a waterline | Splash card sized by impulse tier; ripple ring where a prop settles through the waterline; **sleeping props and the ambient swell never proc anything** — the tide is scenery, not events |
| Roshan breach (reef) | `was_airborne` flip in `player.gd:698-705` → `on_player_jump` | Keep the surf ring + sparkles; add the `splash_breach` card at the crossing point so entry and exit read as *drawn* moments, not just rings |
| ReefPhysics bodies (future: fetch ball, thrown toys) | `body.splashed` (+1/−1) — already computed, currently unread | Small splash card + plink; this is the flag's designed purpose, finally consumed |
| Legacy 3D lagoon rivers/moat/fairy pond | The wet/dry oracle flip (`land_dry`, one frame of lag, invisible) | `splash_small` card + ripple on river/moat entry and exit — the single cheapest fix for the "silent" water boundaries the lagoon has today |
| Castle rooms (2D atlases) | Tap → `INTERACTION_SPECS` semantic actions | Already correct. The bathtub/sink/fountain atlases **are** the reference art; the new vocabulary must match them, not replace them |
| Fetch lake | The existing miss branch (`fetch.gd:276-278`) | Play the same `splash_medium` card at Chuck's landing point instead of message-only — the one place a "splash" currently has no picture |

### Procing rules (the part that keeps it from becoming noise)

1. **Tiered by energy, not random.** Vertical speed / impulse magnitude
   selects small / medium / breach. Same thresholds engine-wide so the
   same event always looks the same size.
2. **Cooldown per emitter** (~0.5 s, the jump-kick cooldown idiom) so a
   body jostling at the waterline reads as bobbing, not machine-gun
   splashes.
3. **Ambient ≠ event.** The swell, sleeping-prop sway, toon-water shimmer
   and mural bob are continuous channels and never spawn cards. Cards mean
   *something happened*.
4. **No proc without sound + no sound without proc.** Every card pairs
   with the existing `castle/bubble_water.ogg` family (or a new OGG in the
   same family), the same coupling the castle atlases already enforce via
   `sound_frame`.
5. **Probe-visible.** Card spawns increment a counter on `main.g` so
   `probe_props.gd` (extended) and `probe_passive.gd` can assert both
   presence *and* absence (zero input ⇒ zero event cards — the swell alone
   must never fire one).

---

## 3. Visual continuity through the game

The game currently speaks **four unrelated water dialects**: painted atlas
water (castle — excellent), toon-shader sheet water (3D lagoon/moat/rivers
— good), logic-only water (fetch — invisible), and physics water with no
visuals at all (the unshipped fleet). Continuity comes from three bindings:

1. **One vocabulary, drawn once.** The Codex atlas set (workorder) is the
   *only* splash/ripple/bubble art, reused in the reef, the lagoon, the
   promenades, fetch, and any future bathtub-scale interaction. Same
   silhouette language as the bubble-bath atlas: navy/purple outline,
   pastel aqua/lavender foam, white sparkle dots.
2. **One clock.** `swell_phase()` is already the shared tide for props,
   hover and layers. Promenade water murals (L2 water bands), floating
   standees, and ripple-drift should all sample it, so every underwater
   stage breathes on the same ~11 s cycle. In the 3D reef, the existing
   `_toon_water_mat` time inputs stay as they are — the player never sees
   both at once.
3. **One palette.** All water FX and water surfaces draw from the toon
   water pair already in use (`Color(0.2,0.55,0.8)` deep / `(0.5,0.82,0.9)`
   light, foam near-white) — the same family in the shader water, the
   castle atlases, and the new cards.

## 4. Recommended order of work (all probe-gated, one step per commit)

**STATUS 2026-08-02 (same day, follow-up commit): P1–P4 are INSTITUTED.**
`scripts/fx_water.gd` is the vocabulary satellite (atlas-ready flipbook,
styled procedural stand-in until the Codex art lands); consumers wired:
reef surface breach (`on_player_jump` crossing flag), lagoon/fjord wet-dry
flips (`on_player_wet_change`), the fetch lake, and the prop-fleet
waterline (`props_tick` cfg `water_y`). The toy-castle brawl courtyard is
the first live swell + prop-fleet stage (6 waterlogged pastel blocks).
Probe coverage: `probe_props` `_fx_case`, `probe_passive` zero-proc
assertion. First-ever human inspection frames: `probe_human_art_audit`
shots 20–22 in the CI visual-review artifact. Still open: P0 (Codex
atlases — the workorder), the reef-pilot swell promenade, and the
ReefPhysics `splashed`-flag consumer (no live `Body` exists yet to wire).

1. **P0 — Codex paints the vocabulary** (workorder; no code dependency).
2. **P1 — `fx_card()` primitive** + counters, with a `probe_fx` case and a
   `probe_passive` no-proc assertion.
3. **P2 — First consumer: reef breach** swaps its sparkle-only moment to
   `splash_breach` + ring (visual-only, zero probe-trajectory risk).
4. **P3 — First swell stage ships.** The next underwater promenade (reef
   pilot, per charter order) turns on `swell` + a ≤12-prop fleet of sea
   toys, with waterline procs. This is the moment the Jolt water system is
   finally *instituted* in live play.
5. **P4 — Cheap retrofits:** lagoon river/moat entry splash (legacy 3D
   path), fetch lake splash card, ReefPhysics `splashed` consumer for the
   fetch ball.
6. **P5 — Castle stays as-is.** The bathtub atlas idiom is already the
   target quality; new castle water interactions keep using per-prop
   atlases, now drawn against the shared vocabulary so they match.

Non-goals, restated so they survive this document: no buoyancy solver
revival (oceanfft stays dead), no Jolt for objectives or Roshan, no
particles-for-water on the Mobile renderer, no per-stage bespoke splash
art.
