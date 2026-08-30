# Chapter 3 Fairy Conservatory handoff — art provenance

Date: 2026-08-30

Status: selected runtime assets; independent Sol visual/art audit passed
2026-08-30. Exact Godot 4.7.2 runtime, device, child, owner, and release
acceptance remain separate pending gates.

## Scope and gap

The approved Sky Lagoon v5 panorama already supplies the handoff world's sky,
cloud, distant-island, and color language. It is reused directly as the stage
background. The repository did not contain a standalone true-2D walkable
rainbow causeway or a standalone Butterfly House landmark that could be used
as a physical stage destination. Generation was limited to those two gaps.

No file under `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified. Review references supplied style,
color, architecture, and perspective only; none contributes delivery pixels.

## Selected generation 1 — rainbow walkway

- Built-in ImageGen result: `exec-3648d4fe-ca54-44e2-bdc9-a3eb1f3f1453`
- Native source: `raw/rainbow_walkway_openai_raw.png`
- Runtime derivative: `assets/flats/fairy_conservatory_handoff/rainbow_walkway.png`
- Reference roles:
  - `assets_src/imagegen/boot_splash_2026-08-01/candidates/candidate_b_rainbow_bridge_celebration_raw.png`: one-point perspective and readable travel direction only.
  - `assets/flats/castle/fairy_conservatory/moonflower_door_open.png`: Pearl Castle shell/gold/lavender trim language only.
  - `assets_src/blender/qa_sky_lagoon_quality_kit/lagoon_rainbow_race_arch.png`: approved rainbow order and saturation family only.
- Prompt brief used: Create one isolated, transparent, front-facing-perspective
  storybook rainbow walkway for a preschool 2D game. The causeway must be broad
  at the bottom, narrow toward one centered vanishing point, use the approved
  coral, peach, yellow, mint, aqua, and lavender order, and use Pearl Castle
  shell/gold/lavender rails. No characters, text, HUD, landscape, horizon,
  separate portal, or dark void. Keep the entire subject inside the canvas.
- Processing: native alpha retained; transparent bounds cropped; the complete
  subject was uniformly normalized inside a 1024×1024 RGBA canvas. No component
  was moved, redrawn, relit, warped, or composited from another asset.

## Selected generation 2 — Butterfly House

- Built-in ImageGen result: `exec-7f598cda-3e9c-441d-aa73-cd4038000612`
- Native source: `raw/butterfly_house_openai_raw.png`
- Runtime derivative: `assets/flats/fairy_conservatory_handoff/butterfly_house.png`
- Reference roles:
  - `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/butterfly_world_gate_turnaround_v1.png`: butterfly silhouette and destination identity only.
  - `assets_src/sky_lagoon/reductive_rebuild_2026-07-28/stained_glass_owner_reference.png`: approved stained-glass material and outline family only; any depicted character was excluded from the requested output.
  - `assets/flats/castle/fairy_conservatory/moonflower_door_open.png`: Pearl Castle shell/gold/lavender architectural language only.
  - `assets/fairy/sprites/boss_bloom.png`: fairy-world floral color continuity only.
- Prompt brief used: Create one isolated, child-readable Butterfly House as a
  physical 2D landmark: a symmetrical butterfly-shaped stained-glass
  conservatory with a large open central entrance, broad purple outlines,
  pale-gold and shell trim, aqua/lavender shadows, and restrained lily planters.
  It must read at phone scale and contain no character, labels, HUD, portal
  ring, generic meadow, detached pearl strings, or cropped architecture.
- Processing: the RGB generator result contained a neutral checker
  presentation field. Only border-connected light-neutral pixels were removed;
  a one-pixel matte support and 0.8-pixel feather were applied before uniform
  whole-subject normalization. The interior and architecture remain the native
  generation.

The prompt briefs above preserve the complete semantic generation request but
are normalized for local documentation; the Codex task log remains the
authority for the original tool-call strings.

## Approved reused stage background

`tools/build_fairy_conservatory_handoff_art.py` reconstructs the approved
6144×2048 Sky Lagoon v5 panorama from its twelve existing runtime tiles, then
crops one continuous 3640×2048 16:9 master. It slices that master into a 4×2
grid of non-overlapping 910×1024 runtime cards. No object is independently
regenerated across a seam. Input/output SHA-256 hashes, crop coordinates,
dimensions, matte settings, and runtime paths are recorded in
`asset_manifest.json`.

## Review status

- Alpha extraction: passed local visual inspection.
- Whole-subject containment: passed local visual inspection.
- Rainbow color order and perspective: passed local visual inspection.
- Butterfly House landmark readability: passed local visual inspection.
- Integrated 1280×720 composition, phone-scale target readability, hall-door
  continuity, and larger-vision scope: passed independent Sol review on
  2026-08-30. Sol requested deterministic runtime/probe corrections only and
  found no art flaw requiring regeneration. This scoped visual pass does not
  grant target-device, child, owner, exact-engine runtime, or release
  acceptance.
