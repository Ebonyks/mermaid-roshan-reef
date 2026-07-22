# CC0 Ocean Replacement 2D-to-3D Handoff

This is a concept-only handoff for the Group 2 Regen 35 and its three-file
live-SeaWeed addendum in
`CC0_REPLACEMENT_WORKORDER_2026-07-22.md` (source branch commit `9580af64`).
It does not alter world topology, spawning, gameplay, runtime paths, or the
legacy assets.

`REGEN_35_PROMPT_PLAN.md` is the coverage authority. The accepted sheets now
cover `35/35` numbered entries and all three live-SeaWeed addendum entries.
The six entries `23–28` are concept-only until their callsites are verified.

## Accepted sheets

| Kingdom direction | Sheet | In-scope legacy roles only |
|---|---|---|
| Caribbean | `caribbean_nautical_live_replacements.png` | `assets/ship/barrel.glb`, `chest.glb`, `cliff_cave_rock.glb`, `ship-ghost.glb`, `ship-wreck.glb` |
| Norwegian cold water | `norwegian_rock_kelp_live_replacements.png` | `assets/nature/cliff_block_rock.glb`, `cliff_large_rock.glb`, `rock_largeA.glb`; `assets/aquatic/SeaWeed.glb`, `SeaWeed1.glb`, `SeaWeed2.glb` |

Additional accepted Regen sheets:

- `regen_01_pearl_shell_throne.png`
- `regen_02_03_vehicles.png`
- `regen_04_06_crystal_family.png`
- `regen_07_crystal_castle.png`
- `regen_08_serving_tray.png`
- `regen_09_10_butterflies.png`
- `regen_11_pearl_castle_bed.png`
- `regen_20_22_castle_live_modules.png`
- `regen_23_28_castle_pending_modules.png` (concept-only hold)
- `regen_29_32_park_and_rooted_hedges.png`
- `regen_33_35_pearl_furniture.png`

## Ecosystem composition references

- `context_caribbean_reef_density.png` shows a clear swim corridor framed by
  abundant Caribbean branching and massive coral, sea fans, tube sponges and
  rooted seagrass.
- `context_norway_kelp_coldwater_coral_zones.png` keeps rooted shallow Norwegian
  kelp forest separate from deep cold-water coral and sponge habitat.

These two images govern placement and density only. They do not add Regen IDs,
authorize combined habitat meshes, or replace the existing original coral kit.

Both accepted sheets are untouched 1536x1024 built-in image-generation
outputs. The kingdom names are visual-direction labels for these replacement
families, not authorization to create new gates, fauna, regions, or travel
logic. The three seaweed roles currently dress the kart track; Claude must
preserve that actual runtime role unless the owner separately changes it.

## Rejected evidence

`rejected/caribbean_nautical_plinth_v1.png` is retained for provenance only.
It added turquoise display plinths beneath the props, conflicting with the
project rule that each reusable object expose its natural support geometry
without a baked ground patch or combined base. Do not model from it.

`rejected/regen_07_crystal_castle_clutter_v1.png` added freestanding crystal
clutter around the castle foundation. `rejected/regen_09_10_butterfly_pose_anatomy_v1.png`
lacked a reliable closed-wing state and consistent leg anatomy. Both were
replaced by corrected accepted sheets and must not be modeled.

## Claude reconstruction contract

- Reconstruct one asset, or one tightly related family, per commit.
- Split every sheet row into an independently named mesh. A sheet is never one
  combined runtime object.
- Preserve the accepted silhouette, orthographic proportions, natural contact
  edge, and broad color blocks. Resolve small view inconsistencies by favoring
  the clearest phone-size silhouette.
- Use original Mobile-safe low-poly geometry, matte embedded materials, thick
  kelp blades, and broad rock planes. Do not embed the reference sheet as a
  runtime texture or use transparent plant cards.
- Wire through the matching override/shadow pattern so the old path goes dark
  before deletion. Do not delete any current CC0/CC-BY/non-original file in the
  modeling commit.
- Run `tools/glb_check.py`, document editable source and license, identify the
  runtime destination, capture the exported GLB in the Mobile renderer, and run
  the trusted probes for the exact commit.
- Only a later owner-approved cleanup commit may delete the superseded legacy
  file. These sheets are reference-only and establish no 4/5 score.

Exact prompts and the rejected-iteration reason are in `PROMPTS.md`.
The corrected numbered manifest and family prompts are in
`REGEN_35_PROMPT_PLAN.md`.
