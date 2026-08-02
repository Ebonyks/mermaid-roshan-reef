# Ember Fortress full graphics regeneration audit — 2026-07-21

## Outcome

The complete visual scope of the generic, IP-safe world internally requested as
“Bowser World” was inventoried and reviewed. Its shipped identity remains
**Ember Fortress**; no branded character, symbol, architecture, music, or UI
was introduced.

Every active visual role below 4/5 was rebuilt or replaced. The result is a
**4/5 Mobile-renderer candidate**, not a self-awarded 5/5. Only owner review can
establish 5/5. The exhaustive row-level record is
`audit/ember_visual_inventory_2026-07-21.csv`.

## Evaluation scale

- **1/5:** blockout, engine primitive, broken placement/state, or unreadable.
- **2/5:** valid but generic, repetitive, weakly themed, or unproved at runtime.
- **3/5:** coherent and functional but missing a focal finish or evidence case.
- **4/5:** authored, role-readable, correctly scaled, and inspected in Godot
  4.4.1 Forward Mobile at representative gameplay views.
- **5/5:** owner-accepted shipped result only.

Hard caps used here: no runtime evidence ≤2; visible clipping/inversion or an
engine-primitive focal role ≤1; no role is scored above the evidence that shows
it.

## Scope and disposition

The ledger contains 42 visual roles across the spherical overworld and its
six-room dungeon. Thirty-seven failing roles were regenerated/rebuilt; five
already-valid or protected presentation roles were retained. Protected Roshan
character routing, book art, friend art, and family voices were not modified.

The coherent deterministic kit contains 39 texture-free GLBs:

- world: planet shell and polar plazas, four tower variants, rampart, flag,
  Great Gate, modeled flame veil, sentry, and Ember King;
- overworld props: lantern, separate flame, distant beacon, geyser, three crag
  and three crystal variants, ash moon, and rainbow home ring;
- dungeon: arena, door, imp, boss, basket, fire/ice projectiles, pedestal,
  lantern, statue, stepping stone, pictogram family, clue plaque, direction
  marker, completion spark, and pearl receiver.

Runtime-only atmosphere, particles, HUD, and pointers remain separate layers.
Shared ordinary-dungeon assets were not overwritten: Ember rooms opt into
`DungeonArt.EMBER_PATHS`, so other dungeons retain their existing visuals.

## Measured output

- 39 GLBs, 1,901,852 bytes total; largest file 305,232 bytes.
- 25,038 triangles across the complete library; largest individual asset is
  the 5,516-triangle planet.
- 361 material slots/mesh islands across the library; all materials are simple
  embedded matte/emissive colors and there are no runtime textures.
- Editable source: `assets_src/blender/ember_fortress_kit.blend`.
- Deterministic builder: `tools/build_ember_fortress_kit.py`.
- Parsed measurements: `assets_src/blender/qa_ember_fortress_kit/ember_fortress_kit_metrics.csv`.
- Isolated renders and three contact sheets:
  `assets_src/blender/qa_ember_fortress_kit/`.

The full library is not instantiated simultaneously. Speedy retains at most
one nearby lantern OmniLight and hides the King/avatar detail lights. No new
light type or texture memory was added. Exact device frame timing remains an
APK play-test concern; this audit does not convert successful desktop Mobile
rendering into a Lenovo Tab M11 performance claim.

## Runtime defects found and corrected

The review loop rejected several technically valid renders before acceptance:

1. The authored sky sphere sat at 750 m while cameras clipped around 400–450 m,
   producing a black world. It now fits inside the far plane at 180 m.
2. The generic ground-alignment fitter shifted the spherical planet upward by
   one radius. The shell is now centered on the exact analytic world origin.
3. The original Ember King placement blocked the Great Gate approach. He was
   reduced to 5.8 m and moved beside the approach line.
4. The modeled gate retained an opaque slab after the flame veil disappeared.
   The overworld gate is now an open frame; only the separate veil changes
   visibility.
5. Lantern flames floated above their bowls. Their authored transform and scale
   now register to the assembly; lit/unlit states remain separate geometry and
   material states.
6. The home ring was edge-on and the sphere’s pole triangle fan formed a dark
   pinwheel. The ring now faces the approach and sits over a quiet authored
   two-level portal plaza.
7. Dungeon stepping stones inherited a 0.3 scale and were too small; Ember uses
   0.82. Arena rays were rebuilt in the floor plane.
8. Imported Blender suffixes caused exact child-name lookup to show overlapping
   pictograms. Theme lookup now accepts the deterministic suffixes and shows
   one symbol only.

## Evidence

Authoritative runtime evidence was captured from Godot 4.4.1 using Vulkan
**Forward Mobile**, Speedy quality, 1280×720 expand canvas:

- `audit/ember_runtime_2026-07-21/01_planet_arrival.png`
- `02_citadel_gate_closed.png` and `06_citadel_gate_open.png`
- `03_lantern_unlit_gameplay.png` and `04_lantern_lit_gameplay.png`
- `05_friendly_geyser.png`, `07_home_ring.png`, and `08_ash_moon.png`
- `09_dungeon_combat.png` and `10_dungeon_puzzle.png`
- `contact_mobile.png` — the complete runtime review sheet.

Isolated evidence is useful for assets hidden behind later-room progression,
but never raises a role above 4/5. The runtime probe is
`scripts/probe_ember_art.gd`; deterministic gameplay/state assertions remain
in `scripts/probe_ember.gd`.

## Gameplay and safety invariants

- Five persistent lanterns still open the Great Gate only when all are lit.
- The six Ember dungeon rooms retain independent `ember_progress` and
  `ember_done` checkpoints.
- Lava and geysers remain friendly hop/launch verbs with no damage or failure.
- The home portal remains available at all times.
- Analytic spherical movement remains body-free; no mass gameplay physics body
  was introduced.
- Existing voice guidance, visual beacons, touch controls, and non-reader HUD
  remain intact.
- No existing runtime art was overwritten, so a separate byte-backup archive
  would duplicate unchanged repository files; reversal is the theme-routing
  and dedicated-directory commit itself.

## Promotion gate

Before dev integration: parser and inference lint must pass for every changed
GDScript; `probe_ember.gd` and the full trusted probe suite must be green for
the exact branch HEAD; the branch must be reconciled with current `origin/dev`;
and exact-HEAD CI must remain green. Master is outside this task.
