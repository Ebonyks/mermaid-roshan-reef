# CC0/Non-Original Asset Replacement Workorder (owner directive 2026-07-22)

Owner: "wait until assets are stable, and then remove all cc0 assets in game.
I want all original art... these cc0 assets are among the weakest in the
game currently." Refined in-session: **this is a handoff, not a deletion
pass.** Codex generates each replacement directly (deterministic Blender
geometry — its own lane per `assets/ART_GENERATION_CONTRACT.md`, since every
item below is a world/environment asset, not a book-derived character); **the
old CC0/CC-BY/non-original file is only deleted once its replacement is
built, wired, and probes are green.** No mass deletion happens in this pass.
The staged queue is in "Group 2 — the generation queue" below: 39 items.

## Key finding — read first

The project already runs a "strangler fig" pattern for exactly this kind of
swap: a `*_GEN2` lookup dict (or an `assets/aquatic2/` shadow folder) is
checked before the legacy CC0/CC-BY path, so dropping in a same-role
replacement and registering it automatically stops the old file from ever
being reached — zero risk, no behavior change to verify beyond the probe
suite. See `NATURE_GEN2`, `KIT_GEN2`, `AQ_GEN2`, `CREATURE_GEN2` in
`scripts/main.gd`, and `StoryArtFactory` (`scripts/story_art.gd`) for the
flat-card variant. **New replacements should be wired the same way.**

Tracing those dicts against actual call sites turned up something the owner
should know: **a large chunk of the CC0/CC-BY inventory is already dead
code** — replaced months ago, with nobody circling back to delete the now-
unreachable original file. That group needs zero Codex/Blender work; it's a
free deletion once the owner blesses it (Group 0 below). The real regen list
(Group 2) is much smaller than "every CC0 path in ASSET_LICENSES.md."

## Group 0 — already superseded, dead code, zero regen needed

These files are not reachable by any live code path (confirmed by grep
against every `*_GEN2`/`*_ART` dict and the raw load call sites). Deleting
them today would be a no-op visually. **Not deleted in this pass** — flagged
for a separate owner-approved cleanup commit, since "no replacement needed"
wasn't explicitly covered by the "don't remove until replacement arrives"
rule and deserves its own explicit go-ahead.

- `assets/nature/{flower_purpleA,flower_redA,flower_yellowB,grass_leafsLarge,
  mushroom_red,mushroom_tanGroup,plant_bush,plant_bushLargeTriangle,
  tree_palm,tree_default_fall,tree_simple_fall,tree_fat,
  tree_pineRoundF}.glb` — 13 of 16 Kenney Nature Kit files; routed through
  `NATURE_GEN2` or `StoryArtFactory.plant()` in `_nature()` (main.gd:3590).
- `assets/kits/play/*.glb` — all 6 Tiny Treats playground pieces; 100%
  covered by `KIT_GEN2` (main.gd:3654).
- `assets/galaxy/{fruit_apple,fruit_banana,fruit_melon,fruit_orange,beetle,
  ladybug,trop_palm1,trop_palm2,trop_fern,trop_monstera,trop_bigleaf}.glb`
  — 11 files (8 CC-BY, 3 CC0); galaxy.gd never loads these paths directly —
  fruit/bugs render via `StoryArtFactory.fruit()`/`.bug()` (galaxy.gd:582,
  819) and tropical foliage via `StoryArtFactory.plant()` (galaxy.gd:526).
- `assets/aquatic/{Coral,Coral1-6,Rock,Rock1-11,FanShell,SmallFanShell,
  SpiralShell,SandDollar,StarFish,ClownFish,Turtle,Dolphin,Shark,Hammerhead,
  Whale,StingRay,Squid,Penguin,Octopus,Lobster,Crab}.glb` — 33 of 44 Riley
  aquatic-pack files; fully covered by `AQ_GEN2`/`CREATURE_GEN2` in
  `_place_aq()` (main.gd:1676-1697), or by `assets/aquatic2/` shadow files.
- `assets/aquatic/{Carp,Dory,Eel,Tuna,Seal}.glb` — 5 files with **no spawn
  code at all** anymore (main.gd:1791-1792 comment confirms these were
  retired from the "small darting schools" pass on 2026-07-11; only a dead
  color-table entry at line 1571-1576 still names them).
- `assets/vehicles/monstertruck.glb` — already has a shipping replacement
  (`monstertruck_story.glb`, GEN2-authored); kept only as `legacy_glb` in
  kart.gd:192-193. Removing it needs no new art, just confirming the story
  glb is solid, then a one-line kart.gd edit.

**Total: 63 files removable with zero art work**, pending owner sign-off.

## Group 1 — already flagged for retirement, no regen needed

- `assets/sky/lagoon_day_2k.hdr`, `assets/sky/lagoon_dusk_2k.hdr` (Poly
  Haven, CC0) — confirmed **zero script references**; already called out in
  `ART_GAP_WORKORDER_2026-07-18.md` line 38-39: "scored 2/5 and deliberately
  unwired — do NOT re-wire; delete or replace with painted panoramas." If a
  painted sky panorama is ever wanted, that's new original art, not a
  like-for-like CC0 swap — no action needed for this workorder.

## Group 2 — the generation queue (39 items)

Every item below is a **world/environment asset**, which per
`assets/ART_GENERATION_CONTRACT.md`'s two-pipeline split is Codex's own lane
directly: a deterministic Python/Blender generator script in `tools/`, flat
multi-material texture-free geometry, no Meshy and no book-art involved
(none of these are book-derived characters — that lane is reserved for
Roshan/friends and stays untouched). Follow the contract's stress-test loop
exactly as the Northern Kingdom kit and pearl-castle kit did: generate →
capture near/mid/gameplay-distance on the Mobile renderer via CI → reject on
silhouette/material/scale/repetition → regenerate → owner acceptance. Ship
each asset with its generator script, `assets_src/blender/` source, QA
renders, and an `ASSET_LICENSES.md` row in the same commit, then wire it
through the matching `*_GEN2` dict (or a new one, following the
`KIT_GEN2`/`NATURE_GEN2` pattern) so the old file goes dark before it's
deleted in a follow-up commit.

Priority: **P0** = highest-visibility/furthest along, work these first.
**P1** = high-reuse or high-traffic. **P2** = standard queue. **P3** =
unverified live call site — confirm with a grep before generating; if dead,
move it to Group 0 instead and skip it. `state` starts `queued` for every
row; flip to `generating` / `review` / `shipped` as work lands (mirrors the
`gen2/meshy/tasks.json` state convention used for the NPC pipeline).

| # | task id | path | pri | state | source/license | live call site(s) | notes |
|---|---|---|---|---|---|---|---|
| 1 | cc0_throne | `assets/castle/throne.glb` | **P0** | queued | CC-BY 3.0, Poly by Google | castle_hall.gd:136-143 (fallback when `pearl_shell_throne` is absent) | finish the already-started `pearl_shell_throne` piece (castle_hall.gd:135) — furthest along, actively camera-tuned right now |
| 2 | cc0_gokart | `assets/vehicles/gokart.glb` | P1 | queued | CC-BY 3.0, Poly by Google | kart.gd:185 | wire like `monstertruck_story.glb` did (primary + legacy fallback) |
| 3 | cc0_motorcycle | `assets/vehicles/motorcycle.glb` | P1 | queued | CC0, poly.pizza (AliceCassie) | kart.gd:178 | same pattern |
| 4 | cc0_crystal1 | `assets/galaxy/crystal1.glb` | P1 | queued | CC0, iPoly3D | galaxy.gd:34 (`CRYSTALS`), kart.gd rainbow-track deco | 1 of 3 crystal variants |
| 5 | cc0_crystal2 | `assets/galaxy/crystal2.glb` | P1 | queued | CC0, iPoly3D | galaxy.gd:34 | 2 of 3 |
| 6 | cc0_crystal3 | `assets/galaxy/crystal3.glb` | P1 | queued | CC0, iPoly3D | galaxy.gd:34 | 3 of 3 — batch all 3 in one commit, swap `CRYSTALS` array together |
| 7 | cc0_crystal_castle | `assets/galaxy/crystal_castle.glb` | P2 | queued | CC0, CreativeTrio | galaxy.gd:40,610 (`CASTLE_GLB`) | single landmark model |
| 8 | cc0_galaxy_tray | `assets/galaxy/tray.glb` | P2 | queued | CC0, MilkAndBanana | galaxy.gd:47,569 (`TRAY_GLB`) | already re-textured once (nano-banana) — good scale/placement reference |
| 9 | cc0_butterfly1 | `assets/galaxy/butterfly1.glb` | P2 | queued | CC-BY 3.0, Poly by Google | galaxy.gd:44,502 (`BUTTERFLY_GLBS`) | 1 of 2 flutter variants |
| 10 | cc0_butterfly2 | `assets/galaxy/butterfly2.glb` | P2 | queued | CC-BY 3.0, Poly by Google | galaxy.gd:44,502 | 2 of 2 — batch with #9 |
| 11 | cc0_castle_bed | `assets/castle/bed.glb` | P1 | queued | CC0, Kenney ("Bed Single") | castle furniture builders | same class of work as the shipped 58-piece `pearl_kit` — this bed is the one holdout |
| 12 | cc0_cliff_block_rock | `assets/nature/cliff_block_rock.glb` | P2 | queued | CC0, Kenney Nature Kit | `_nature()` fallback, main.gd (world cliff/rock dressing) | reuse the `assets/props/gen2/rock*.glb` toolchain/style already built for aquatic rocks |
| 13 | cc0_cliff_large_rock | `assets/nature/cliff_large_rock.glb` | P2 | queued | CC0, Kenney Nature Kit | `_nature()` fallback | same family as #12 |
| 14 | cc0_rock_largeA | `assets/nature/rock_largeA.glb` | P2 | queued | CC0, Kenney Nature Kit | `_nature()` fallback | same family as #12 — batch 12-14 |
| 15 | cc0_ship_barrel | `assets/ship/barrel.glb` | P2 | queued | CC0, Kenney Pirate Kit | main.gd:1393, 6317 (shop/undercroft) | 1 of 5-piece nautical set |
| 16 | cc0_ship_chest | `assets/ship/chest.glb` | P2 | queued | CC0, Kenney Pirate Kit | main.gd:1393, 6317 | 2 of 5 |
| 17 | cc0_ship_cliff_cave_rock | `assets/ship/cliff_cave_rock.glb` | P2 | queued | CC0, Kenney Pirate Kit | main.gd:1393 | 3 of 5 |
| 18 | cc0_ship_ghost | `assets/ship/ship-ghost.glb` | P2 | queued | CC0, Kenney Pirate Kit | main.gd:1393 | 4 of 5 |
| 19 | cc0_ship_wreck | `assets/ship/ship-wreck.glb` | P2 | queued | CC0, Kenney Pirate Kit | main.gd:1393 | 5 of 5 — batch 15-19 as one nautical-prop generator pass |
| 20 | cc0_kit_tower_square | `assets/kits/castle/tower-square.glb` | P1 | queued | CC0, Kenney Castle Kit | sky_lagoon.gd:158, northern_kingdom.gd:1224 (confirmed live) | extend `KIT_GEN2` the same way `play/*` was covered |
| 21 | cc0_kit_flag | `assets/kits/castle/flag.glb` | P1 | queued | CC0, Kenney Castle Kit | sky_lagoon.gd:160, northern_kingdom.gd:1031,1228 | batch with #20/#22 |
| 22 | cc0_kit_wall | `assets/kits/castle/wall.glb` | P1 | queued | CC0, Kenney Castle Kit | sky_lagoon.gd:164 | batch with #20/#21 |
| 23 | cc0_kit_tower_base | `assets/kits/castle/tower-base.glb` | **P3** | queued | CC0, Kenney Castle Kit | none found this pass — verify before generating | may belong in Group 0 |
| 24 | cc0_kit_tower_square_base | `assets/kits/castle/tower-square-base.glb` | **P3** | queued | CC0, Kenney Castle Kit | none found this pass — verify | may belong in Group 0 |
| 25 | cc0_kit_tower_square_mid | `assets/kits/castle/tower-square-mid.glb` | **P3** | queued | CC0, Kenney Castle Kit | none found this pass — verify | may belong in Group 0 |
| 26 | cc0_kit_tower_square_top_roof | `assets/kits/castle/tower-square-top-roof-high.glb` | **P3** | queued | CC0, Kenney Castle Kit | none found this pass — verify | may belong in Group 0 |
| 27 | cc0_kit_tower_top | `assets/kits/castle/tower-top.glb` | **P3** | queued | CC0, Kenney Castle Kit | none found this pass — verify | may belong in Group 0 |
| 28 | cc0_kit_wall_narrow_gate | `assets/kits/castle/wall-narrow-gate.glb` | **P3** | queued | CC0, Kenney Castle Kit | none found this pass — verify | may belong in Group 0 |
| 29 | cc0_park_bench | `assets/kits/park/bench.glb` | P1 | queued | CC0, Tiny Treats Pretty Park | sky_lagoon.gd, northern_kingdom.gd, courtyard_train.gd:247, castle_hall.gd | highest-reuse kit piece on this list |
| 30 | cc0_park_fountain | `assets/kits/park/fountain.glb` | P1 | queued | CC0, Tiny Treats Pretty Park | sky_lagoon.gd:332, northern_kingdom.gd:1232 | batch with #29 |
| 31 | cc0_park_hedge_straight | `assets/kits/park/hedge_straight.glb` | P1 | queued | CC0, Tiny Treats Pretty Park | main.gd:3730 (`park/hedge`) | batch with #29 |
| 32 | cc0_park_hedge_straight_long | `assets/kits/park/hedge_straight_long.glb` | P1 | queued | CC0, Tiny Treats Pretty Park | sky_lagoon.gd:340 | batch with #29-31 |
| 33 | cc0_furn_bookcase | `assets/kits/furniture/bookcase.glb` | P1 | queued | CC0, Quaternius Ultimate Furniture | main.gd:3724, castle_hall.gd:194, northern_kingdom.gd:1653 | pairs with the shipped pearl-castle furniture style |
| 34 | cc0_furn_chair | `assets/kits/furniture/chair.glb` | P1 | queued | CC0, Quaternius Ultimate Furniture | main.gd:3726, castle_hall.gd:198-199 | batch with #33 |
| 35 | cc0_furn_table | `assets/kits/furniture/table.glb` | P1 | queued | CC0, Quaternius Ultimate Furniture | main.gd:3724, castle_hall.gd:196 | batch with #33-34 |
| 36 | cc0_seaweed0 | `assets/aquatic/SeaWeed.glb` | P2 | queued | "free use, no redistribution" (Riley pack) | kart.gd:1545 (track scatter) | reuse the `assets/props/gen2/seagrass.png` art direction already approved for the reef |
| 37 | cc0_seaweed1 | `assets/aquatic/SeaWeed1.glb` | P2 | queued | "free use, no redistribution" (Riley pack) | kart.gd:1545 | batch with #36 |
| 38 | cc0_seaweed2 | `assets/aquatic/SeaWeed2.glb` | P2 | queued | "free use, no redistribution" (Riley pack) | kart.gd:1545 | batch with #36-37 |
| 39 | cc0_kit_castle_verify | (task) — confirm items #23-28 | P3 | queued | — | — | one grep pass before generating any of #23-28; if a role is unused, strike it and note in Group 0 instead |

Suggested batching (one commit per batch, in priority order): **#1** solo →
**#2-3** vehicles → **#4-6** crystals → **#20-22** castle-kit trio →
**#29-32** park kit → **#33-35** furniture kit → **#11** bed → **#7-10**
galaxy landmarks/butterflies → **#12-14** nature rocks → **#15-19** ship
props → **#36-38** seaweed → **#39/#23-28** castle-kit tail, generate only
what survives verification.

### Special cases (not a straight 2D→3D swap)

- **`assets/audio/music/world.ogg, world_night.ogg, level2.ogg, hall.ogg,
  home.ogg`** (CC0, Juhani Junkala JRPG Packs) — these are *music*, not
  visual art. If original scores are wanted, that's a composition brief for
  Codex (mood/tempo/instrumentation per scene), not a Blender pipeline;
  the project already has precedent for from-scratch audio (numpy synthesis
  for SFX, Kokoro TTS for voice) but no precedent for original music
  composition — needs an owner decision on approach before Codex drafts a
  brief.
- **`assets/terrain/up_*_rgh.jpg`** (14 files, ambientCG CC0) — these are
  grayscale roughness utility maps, not illustrated art. They should be
  regenerated by the existing terrain-tile tooling (matching how `_nrm.jpg`
  normal maps are already "flattened to neutral" per ASSET_LICENSES.md
  line 29) rather than a fresh Codex art brief — low priority, mechanical.
- **`assets/shaders/toon_water.gdshader`** (CC0 base, godotshaders.com) —
  this is code, not an asset; the project has already rewritten it
  substantially (pastel bands, sparkle, scrolling normals, Speedy toggle).
  Not part of a 2D-art-to-3D handoff; only relevant if the owner wants the
  water shader rewritten from a blank page.

## Execution rule for whoever picks this up

**Gated behind P0:** `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md` P0 says "do not
begin new generation until P0 is closed." This workorder queues behind that
— check P0's status before starting any Group 2 item.

1. Codex writes/runs the deterministic Blender generator script for one
   Group 2 item (or a tightly related small batch, e.g. the 3 galaxy
   crystals), guided by `ART_STYLE_GUIDE.md`.
2. Runtime capture + stress-test loop per `assets/ART_GENERATION_CONTRACT.md`
   (near/mid/gameplay Mobile views via CI); iterate until it clears review.
3. Adds the `ASSET_LICENSES.md` row, wires it through the matching `*_GEN2`
   dict (or a new dict following that pattern) in the same commit.
4. Probe suite green on CI for the exact commit; owner acceptance per
   `ART_SCORING_GOVERNANCE_2026-07-18.md`.
5. **Only then**, in a follow-up commit, delete the superseded CC0/CC-BY
   file and remove its `ASSET_LICENSES.md` line and any now-dead fallback
   code path.
6. One asset (or tightly related small group) per commit — mirrors the
   Refactor-rules precedent of small, probed, reversible steps.
