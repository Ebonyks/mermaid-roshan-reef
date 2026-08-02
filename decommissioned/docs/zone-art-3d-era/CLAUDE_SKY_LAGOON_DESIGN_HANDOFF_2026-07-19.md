# Claude design handoff - Sky Lagoon cohesion pass

## Goal

Convert the approved direction sheets into Blender-authored, Mobile-safe runtime
models, then replace every current Sky Lagoon family below 4/5 without touching
protected art or changing gameplay contracts. The audit source is
`SKY_LAGOON_STYLE_COHESION_AUDIT_2026-07-19.md`; the machine-readable queue is
`audit/sky_lagoon_cohesion_ledger_2026-07-19.csv`.

This is a design and construction handoff. The generated sheets are references,
not final textures and not proof of runtime integration.

## Non-negotiable constraints

1. Never modify, replace, crop, recolor, relight, or regenerate files in
   `assets/book/`, `assets/audio/voices/`, or `assets/characters/friends/`.
2. The existing book image in each memory display and the castle stained-glass
   plane remains a separate unshaded protected plane. New geometry surrounds it
   but never overlaps it.
3. Do not auto-generate stuffed animals. They are reserved for child-owned toy
   sources.
4. A single leaf cannot be a ground plant. Use a rooted baby rosette,
   multi-leaf clump, reed bed, shrub, flowering plant, or mature tree. Alpine
   surfaces accept complete snowy pines, not tropical plants or mushrooms.
5. The Butterfly gate must read as one complete butterfly: body, head, two
   antennae, and four wings. Its central opening must agree with the trigger and
   remain unobstructed.
6. Keep the Mobile renderer and Speedy tier as the visual baseline. Prefer
   embedded matte materials and texture-free geometry. No Forward+-only effect.
7. Preserve gameplay nodes, triggers, saved keys, route widths, collision
   volumes, and seat metadata. Replace visual shells around contracts.

## Selected direction set

| Runtime family | Primary reference | Construction target |
|---|---|---|
| Butterfly World gate | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/butterfly_world_gate_turnaround_v1.png` | Replace `lagoon_butterfly_world_gate.glb`; <=3000 tris, <=10 materials, open center >=50% width and >=65% height |
| Pearl Castle exterior | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/pearl_castle_exterior_turnaround_v2.png` | New exterior-shell GLB; <=6000 tris; separate door and protected glass plane; retain moat and collision contracts |
| Alpine chalet family | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/alpine_chalet_family_v1.png` | Three variants, <=2500 tris each; real door openings, terrain plinth, supported snow |
| Alpine mountain/cave | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/alpine_mountain_cave_kit_v1.png` | Modular crag, foothill, cave, snowbank, cairn; <=3000 tris per module; complete rooted pine saplings only |
| Story lantern | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/storybook_path_lantern_turnaround_v1.png` | Replace `lagoon_story_lantern.glb`; <=1500 tris; stout plinth; separate emissive pearl mesh |
| Memory surround | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/protected_memory_frame_turnaround_v1.png` | Replace frame geometry only; <=1800 tris; portrait opening 2:3; no overlap with image plane |
| Companion train cars | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/courtyard_train_companion_cars_v1.png` | Tender, coach, gondola, caboose; <=2500 tris each; one shared axle/coupler/chassis standard |
| Path, bridge, water edge | `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/path_bridge_water_edge_kit_v1.png` | Visual shells only; preserve established solids and traversal; varied stone clusters, broad bridge curbs |

Reuse these already accepted references rather than regenerating them:

- `gen2/generated/r021_locomotive_identity/turnaround_v1_repair_1024.png`
- `gen2/generated/r021_track_straight/turnaround_v1_1024.png`
- `gen2/generated/r021_track_quarter_curve/turnaround_v1_1024.png`
- `gen2/generated/r021_station_platform_low/turnaround_v1_1024.png`
- `gen2/generated/r021_station_shelter_open/turnaround_v1_1024.png`

## Runtime contracts to preserve

### Train

- Source integration: `scripts/arena/courtyard_train.gd`.
- Car root sits on the railhead at the bogie midpoint; local `+Z` is travel.
- Preserve the five-car order, offsets, wheelbases, `axles` metadata, toy/seat
  names, station dwell, moving colliders, clip guard, and hide/show behavior.
- The passenger coach remains visibly open and its bench remains inside.
- The arbitrary-height route cannot be replaced by a decorative fixed circle.
  A segment kit may skin the existing samples, or the current procedural mesh
  may be rebuilt to match the accepted rail profile.

### Castle

- Source integration: `scripts/arena/sky_lagoon.gd::_build_pearl_castle()`.
- Keep `m.l2_door`, `g["door_closed_y"]`, `g["entry"]`, `g["door_solid"]`,
  `g["arch"]`, the moat, bridge traversal, back hatch, and glass image plane.
- The exterior GLB is a visual shell. Do not duplicate a solid shell around the
  navigable foyer or block the forgiving rectangular doorway.
- Fit the existing vertical protected image into the tall pointed recess. Do
  not use the rejected square-recess castle reference.

### Alpine corner

- Source integration: `_build_christmas_village()`, `_build_alpine_mountain()`,
  `_village_cottage()`, and `_alpine_crag()` in `scripts/arena/sky_lagoon.gd`.
- Retain house entry arrays, bonuses, cave entrance/secret positions, train
  clearances, snowfield terrain conformance, and child-readable cairn trail.
- Place snow on upward-facing ledges; never use flat floating snow discs.

### Gates, frames, and path props

- Keep the existing race and Butterfly trigger positions exactly aligned with
  their visible openings.
- Memory and stained-glass images remain separate protected planes.
- Shell and rainbow motifs are structural accents, not substitutes for clear
  object silhouettes.

## Required deliverables from Claude

1. Editable `.blend` source under `assets_src/blender/`.
2. Runtime GLBs under `assets/sky_lagoon/` with embedded matte materials.
3. One isolated QA render per GLB and a family contact sheet.
4. Old runtime files copied byte-for-byte into a dated backup folder before
   replacement, with SHA-256 manifest.
5. `ASSET_LICENSES.md` entries for every new source, GLB, and QA set.
6. Updated structural audit covering triangle/material budgets, empty gateway
   opening, train roots/axles/couplers, and protected-plane separation.
7. Speedy Mobile captures at arrival, memory frame, plant close-up, Fairy Pond,
   playground, race arch, Butterfly gate, castle facade, train in motion,
   station, Alpine village, and cave.
8. Sparkly comparison captures for arrival, castle, and Alpine corner.

## Acceptance standard

- No sub-4/5 family remains in the scored ledger.
- Technical probes are green, but visual acceptance still requires human review.
- At phone scale, no thin post, wire loop, trim row, or detail disappears.
- No object floats, clips into terrain, blocks a trigger, or contradicts its
  ecosystem.
- The train, castle, and Alpine corner each read as a deliberately authored
  family before the camera reaches close-up range.
- Do not self-award 5/5. Record candidates as 4/5 until owner review.

## Provenance

The new sheets were made with the built-in OpenAI image-generation tool. The
tool did not expose a deterministic seed or model build identifier, so neither
is claimed. Untouched masters are in `raw/`; normalized 1024px review copies are
in `selected/`; the superseded square-window castle is in `rejected/`. Exact
prompts and hashes are stored beside the batch.
