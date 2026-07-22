# CC0/Non-Original Asset Replacement Workorder (owner directive 2026-07-22)

Owner: "wait until assets are stable, and then remove all cc0 assets in game.
I want all original art... these cc0 assets are among the weakest in the
game currently." Refined in-session: **this is a handoff, not a deletion
pass.** Codex generates 2D concept art per item below; Claude converts each
to a game-ready 3D asset (Blender, matching the existing GEN2 pipeline) or a
StoryArtFactory card where that's the established pattern; **the old
CC0/CC-BY/non-original file is only deleted once its replacement is built,
wired, and probes are green.** No mass deletion happens in this pass.

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

## Group 2 — genuinely live, needs a real replacement before deletion

This is the actual Codex handoff list. Every item below is a **world/
environment asset**, which per `assets/ART_GENERATION_CONTRACT.md`'s
two-pipeline split is Codex's own lane directly: a deterministic Python/
Blender generator script in `tools/`, flat multi-material texture-free
geometry, no Meshy and no book-art involved (none of these are book-derived
characters — that lane is reserved for Roshan/friends and stays untouched).
Follow the contract's stress-test loop exactly as the Northern Kingdom kit
and pearl-castle kit did: generate → capture near/mid/gameplay-distance on
the Mobile renderer via CI → reject on silhouette/material/scale/repetition
→ regenerate → owner acceptance. Ship each asset with its generator script,
`assets_src/blender/` source, QA renders, and an `ASSET_LICENSES.md` row in
the same commit, then wire it through the matching `*_GEN2` dict (or a new
one, following the `KIT_GEN2`/`NATURE_GEN2` pattern) so the old file goes
dark before it's deleted in a follow-up commit.

| Item | Current source/license | Live call site(s) | Suggested integration point |
|---|---|---|---|
| `assets/castle/throne.glb` | CC-BY 3.0, Poly by Google | `castle_hall.gd:136-143` (fallback when `pearl_shell_throne` authored piece is absent) | Finish the `pearl_shell_throne` authored piece already referenced at castle_hall.gd:135 — this is furthest along of anything on this list; **highest priority, actively being camera-tuned right now** |
| `assets/vehicles/gokart.glb` | CC-BY 3.0, Poly by Google | `kart.gd:185` | Add to a `VEHICLE_GEN2`-style override or replace in place like `monstertruck_story.glb` did |
| `assets/vehicles/motorcycle.glb` | CC0, poly.pizza (AliceCassie) | `kart.gd:178` | Same pattern |
| `assets/galaxy/crystal1.glb, crystal2.glb, crystal3.glb` | CC0, iPoly3D | `galaxy.gd:34` (`CRYSTALS`), also referenced from kart.gd rainbow-track dressing per `ART_GAP_WORKORDER` | Model 3 crystal variants, swap `CRYSTALS` array to new paths |
| `assets/galaxy/crystal_castle.glb` | CC0, CreativeTrio | `galaxy.gd:40,610` (`CASTLE_GLB`) | Single landmark model |
| `assets/galaxy/tray.glb` | CC0, MilkAndBanana | `galaxy.gd:47,569` (`TRAY_GLB`) | Single prop, already re-textured once (nano-banana) — good scale/placement reference |
| `assets/galaxy/butterfly1.glb, butterfly2.glb` | CC-BY 3.0, Poly by Google | `galaxy.gd:44,502` (`BUTTERFLY_GLBS`) | Two flutter variants |
| `assets/castle/bed.glb` | CC0, Kenney ("Bed Single") | referenced via castle furniture builders | Same class of work as the already-shipped `pearl_kit` furniture (58 pieces) — this bed is the one holdout |
| `assets/nature/cliff_block_rock.glb, cliff_large_rock.glb` | CC0, Kenney Nature Kit | `_nature()` fallback, main.gd (world cliff/rock dressing) | Rock-family Blender pass, same family as `assets/props/gen2/rock*.glb` (already exists for aquatic rocks — reuse that toolchain/style) |
| `assets/nature/rock_largeA.glb` | CC0, Kenney Nature Kit | `_nature()` fallback | Same as above |
| `assets/ship/barrel.glb, chest.glb, cliff_cave_rock.glb, ship-ghost.glb, ship-wreck.glb` | CC0, Kenney Pirate Kit | main.gd:1393, 6317 (shop/undercroft dressing) | 5-piece nautical prop set |
| `assets/kits/castle/tower-square.glb, flag.glb, wall.glb` | CC0, Kenney Castle Kit | `sky_lagoon.gd:158-164`, `northern_kingdom.gd:1031,1224,1228` (confirmed live) | Extend `KIT_GEN2` the same way `play/*` was covered |
| `assets/kits/castle/tower-base.glb, tower-square-base.glb, tower-square-mid.glb, tower-square-top-roof-high.glb, tower-top.glb, wall-narrow-gate.glb` | CC0, Kenney Castle Kit | **no live call site found this pass** — verify with a repo-wide grep before commissioning; may belong in Group 0 | — |
| `assets/kits/park/bench.glb, fountain.glb, hedge_straight.glb, hedge_straight_long.glb` | CC0, Tiny Treats Pretty Park | `sky_lagoon.gd`, `northern_kingdom.gd`, `courtyard_train.gd`, `main.gd:3728-3730`, `castle_hall.gd` | Extend `KIT_GEN2` |
| `assets/kits/furniture/bookcase.glb, chair.glb, table.glb` | CC0, Quaternius Ultimate Furniture | `main.gd:3724-3726`, `castle_hall.gd:194-199`, `northern_kingdom.gd:1653` | Pairs naturally with the pearl-castle furniture kit style already shipped |
| `assets/aquatic/SeaWeed.glb, SeaWeed1.glb, SeaWeed2.glb` | "free use, no redistribution" (Riley pack) | `kart.gd:1545` (kart track scatter) | Reuse the `assets/props/gen2/seagrass.png` art direction already approved for the reef |

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
