# CC0/Non-Original Asset Replacement Workorder (owner directive 2026-07-22)

Owner: "wait until assets are stable, and then remove all cc0 assets in game.
I want all original art... these cc0 assets are among the weakest in the
game currently." Refined in-session: this is a staged handoff, not a mass
deletion — generate real replacements first, wire them in as the primary
path (old file stays as an inert fallback), and only delete the old
CC0/CC-BY file once the replacement clears the project's normal review loop.
Later in the same session, the owner asked for the objects to actually be
generated, not just queued as tasks — **24 of the confirmed-live items were
generated for real this pass** (deterministic Blender geometry, exported to
GLB, wired into the game) using `pip install bpy` in-session rather than
waiting on a separate Codex/Blender environment. Status below.

## Key finding — read first

The project runs a "strangler fig" pattern for this exact kind of swap: a
`*_GEN2` lookup dict (or an `assets/aquatic2/` shadow folder) is checked
before the legacy CC0/CC-BY path, so dropping in a same-role replacement and
registering it automatically stops the old file from ever being reached.
See `NATURE_GEN2`, `KIT_GEN2`, `AQ_GEN2`, `CREATURE_GEN2`, `SHIP_GEN2` in
`scripts/main.gd`, and `StoryArtFactory` (`scripts/story_art.gd`) for the
flat-card variant.

Tracing those dicts (and, critically, the actual call sites — not just
"is there a dict entry") turned up a lot of CC0/CC-BY inventory that's
**already dead code**, replaced months ago with nobody circling back to
delete the orphaned original. That group needs zero art work; it's a free
deletion once the owner blesses it (Group 0). Verifying call sites also
caught two items that looked live on a shallower first pass but turned out
to already be dead too — `assets/castle/bed.glb` (no reference anywhere) and
`assets/aquatic/SeaWeed{,1,2}.glb` (superseded by the `seagrass.png` card,
kart.gd:1542) — both corrected into Group 0 below; `assets/galaxy/{butterfly1,
butterfly2}.glb` likewise turned out to be buried behind two other already-
shipped replacements (`BUTTERFLY_STORY_GLB` card, then a gen2 sprite card)
before the raw glb is ever reached, so those moved to Group 0 too.

## Group 0 — already superseded, dead code, zero regen needed

Not reachable by any live code path. Deleting these today would be a
visual no-op. **Not deleted this pass** — flagged for a separate
owner-approved cleanup commit.

- `assets/nature/{flower_purpleA,flower_redA,flower_yellowB,grass_leafsLarge,
  mushroom_red,mushroom_tanGroup,plant_bush,plant_bushLargeTriangle,
  tree_palm,tree_default_fall,tree_simple_fall,tree_fat,
  tree_pineRoundF}.glb` — 13 of 16 Kenney Nature Kit files; routed through
  `NATURE_GEN2` or `StoryArtFactory.plant()` in `_nature()` (main.gd:3590).
- `assets/kits/play/*.glb` — all 6 Tiny Treats playground pieces; 100%
  covered by `KIT_GEN2`.
- `assets/galaxy/{fruit_apple,fruit_banana,fruit_melon,fruit_orange,beetle,
  ladybug,trop_palm1,trop_palm2,trop_fern,trop_monstera,trop_bigleaf,
  butterfly1,butterfly2}.glb` — 13 files; fruit/bugs render via
  `StoryArtFactory.fruit()`/`.bug()`, tropical foliage via
  `StoryArtFactory.plant()`, butterflies via `BUTTERFLY_STORY_GLB` then a
  gen2 sprite card (galaxy.gd:480-508) before the raw glb array is ever
  reached.
- `assets/aquatic/{Coral,Coral1-6,Rock,Rock1-11,FanShell,SmallFanShell,
  SpiralShell,SandDollar,StarFish,ClownFish,Turtle,Dolphin,Shark,Hammerhead,
  Whale,StingRay,Squid,Penguin,Octopus,Lobster,Crab}.glb` — 33 of 44 Riley
  aquatic-pack files; fully covered by `AQ_GEN2`/`CREATURE_GEN2`.
- `assets/aquatic/{Carp,Dory,Eel,Tuna,Seal}.glb` — 5 files with no spawn
  code at all anymore (retired 2026-07-11, main.gd:1791-1792 comment).
- `assets/aquatic/{SeaWeed,SeaWeed1,SeaWeed2}.glb` — 3 files; kart.gd:1542
  prefers `assets/props/gen2/seagrass.png` first.
- `assets/castle/bed.glb` — no reference anywhere in `scripts/`.
- `assets/vehicles/monstertruck.glb` — already superseded by
  `monstertruck_story.glb`, kept only as `legacy_glb`.

**Total: ~70 files removable with zero art work**, pending owner sign-off.

## Group 1 — already flagged for retirement, no regen needed

- `assets/sky/lagoon_day_2k.hdr`, `assets/sky/lagoon_dusk_2k.hdr` (Poly
  Haven, CC0) — zero script references; `ART_GAP_WORKORDER_2026-07-18.md`
  already says "do NOT re-wire; delete or replace with painted panoramas."

## Group 2 — generated and wired this pass (24 items)

Built with `tools/build_cc0_replacement_kit.py` (deterministic bpy geometry,
same technique as the pearl-castle/Northern-Kingdom kits — texture-free flat
matte materials, bevel-rounded storybook silhouettes). Ran via
`pip install bpy==4.4.0` directly in this session (no separate Blender app
needed) since no art-generation CI workflow exists yet. All 24 exported
clean, none over the 6k-triangle prop budget, and both `gdtoolkit.parser`
and `tools/lint_inference.py` pass on every edited script.

| # | path | replaces | wired via | status |
|---|---|---|---|---|
| 1 | `assets/vehicles/gokart_story.glb` | `assets/vehicles/gokart.glb` (CC-BY) | `kart.gd` VEHICLES `"glb"`, old path now `"legacy_glb"` | generated, wired |
| 2 | `assets/vehicles/motorcycle_story.glb` | `assets/vehicles/motorcycle.glb` (CC0) | `kart.gd` VEHICLES `"glb"`, old path now `"legacy_glb"` | generated, wired |
| 3-5 | `assets/props/gen2/crystal{1,2,3}.glb` | `assets/galaxy/crystal{1,2,3}.glb` (CC0) | `galaxy.gd` `CRYSTALS`, `kart.gd` `BW_CRYSTALS`/`BW_DECO_CRYSTALS` repointed | generated, wired |
| 6 | `assets/props/gen2/crystal_castle.glb` | `assets/galaxy/crystal_castle.glb` (CC0) | `galaxy.gd`/`kart.gd` `CASTLE_GLB`/`BW_CASTLE_GLB` repointed | generated, wired |
| 7 | `assets/props/gen2/galaxy_tray.glb` | `assets/galaxy/tray.glb` (CC0) | `galaxy.gd` `TRAY_GLB` repointed | generated, wired |
| 8-10 | `assets/props/gen2/{cliffrock_block,cliffrock_large,rock_boulder}.glb` | `assets/nature/{cliff_block_rock,cliff_large_rock,rock_largeA}.glb` (CC0) | new `NATURE_GEN2` entries | generated, wired |
| 11-14 | `assets/props/gen2/{ship_wreck,ship_chest,ship_barrel,ship_ghost}.glb` | `assets/ship/{ship-wreck,chest,barrel,ship-ghost}.glb` (CC0) | new `SHIP_GEN2` dict + gen2-first check added to `_spawn()` (main.gd) | generated, wired |
| 15-17 | `assets/props/gen2/kit_{tower_square,flag,wall}.glb` | `assets/kits/castle/{tower-square,flag,wall}.glb` (CC0) | new `KIT_GEN2` entries | generated, wired |
| 18-21 | `assets/props/gen2/kit_{bench,fountain,hedge,hedge_long}.glb` | `assets/kits/park/{bench,fountain,hedge_straight,hedge_straight_long}.glb` (CC0) | new `KIT_GEN2` entries | generated, wired |
| 22-24 | `assets/props/gen2/kit_{bookcase,chair,table}.glb` | `assets/kits/furniture/{bookcase,chair,table}.glb` (CC0) | new `KIT_GEN2` entries | generated, wired |

Source: `assets_src/blender/cc0_replacement_kit.blend` (editable) +
`assets_src/blender/qa_cc0_replacement_kit/*.png` (one isolated render per
piece, Workbench solid-material captures — this session had no GPU/EGL for a
full Eevee/Cycles pass). `ASSET_LICENSES.md` rows added.

**What's still outstanding before these can be promoted and the old
CC0/CC-BY files deleted** (this session had no Godot binary, so none of
this could be done locally — matches CLAUDE.md's known limitation):
1. **CI Mobile-render capture.** The project's stress-test loop requires
   near/mid/gameplay-distance views on the actual Mobile renderer, not just
   an isolated Blender/Workbench render. Push this branch, let
   `probes.yml` run import + trusted probes, and pull runtime screenshots
   the way `SKY_LAGOON_ART_AUDIT_2026-07-19.md` and friends did.
2. **Vehicle orientation is unverified.** `yaw_fix` on both new vehicles was
   left at a guessed value with an explicit "UNVERIFIED render" comment in
   kart.gd — the old moto/kart models faced different local axes and the
   correct fix can only be confirmed by actually seeing the kart drive.
   Check this first; a wrong yaw means the kart visibly drives sideways.
3. **Owner visual acceptance** per `ART_SCORING_GOVERNANCE_2026-07-18.md` —
   no self-awarded score; these are first-draft geometry (a few hundred to
   ~1,200 triangles each), matching the "two or three rejected iterations
   is normal" expectation, not finished 5/5 art.
4. **Only after 1-3 pass**, in follow-up commits: delete the 24 superseded
   CC0/CC-BY files, their `ASSET_LICENSES.md` rows, and the now-dead
   `"legacy_glb"` vehicle fallbacks — one asset or tightly related group per
   commit, per the Refactor-rules precedent.

## Item #1 (throne) — not regenerated; needs a wiring check instead

`assets/castle/throne.glb` (CC-BY, Poly by Google) is **not** a missing-art
problem the way the rest of this list is. `assets/castle/pearl_kit/
pearl_shell_throne.glb` already exists, is already committed (from the
2026-07-18 pearl-castle pass), and `castle_hall.gd:135` already tries it
first via `_pearl("pearl_shell_throne", ...)`. `_static_prop()`
(castle_hall.gd:27-46) only returns null if `ResourceLoader.exists()` fails
or the load/instantiate fails — both should succeed for a committed,
already-audited GLB. The CC-BY fallback at castle_hall.gd:136-143 is very
likely already dead code in practice, just like the Group 0 items above —
but the very last commit before this session (`244dada`, "castle throne no
longer swallows the chase cam") treats "all three throne variants" as
live possibilities worth registering collision for, so this needs an actual
CI/Godot check, not an assumption. **Action: verify whether
`authored_throne` ever resolves to null in the shipped game; if not, move
`throne.glb` to Group 0 and delete the dead fallback branch. No new
modeling needed either way.**

## Special cases (not a Blender-geometry swap)

- **`assets/audio/music/{world,world_night,level2,hall,home}.ogg`** (CC0,
  Juhani Junkala JRPG Packs) — music, not visual art. Needs an owner
  decision on approach (composition brief vs. keep) before anyone drafts a
  brief; no precedent in this repo for original music composition.
- **`assets/terrain/up_*_rgh.jpg`** (14 files, ambientCG CC0) — grayscale
  roughness utility maps; regenerate via the existing terrain-tile tooling
  rather than a fresh art brief — low priority, mechanical.
- **`assets/shaders/toon_water.gdshader`** (CC0 base, godotshaders.com) —
  code, not an asset, already substantially rewritten. Only relevant if the
  owner wants the water shader rewritten from a blank page.

## Remaining open items (unverified live call site)

`assets/kits/castle/{tower-base,tower-square-base,tower-square-mid,
tower-square-top-roof-high,tower-top,wall-narrow-gate}.glb` — no call site
found in either audit pass. Confirm with a grep before generating; if dead,
they belong in Group 0 instead.
