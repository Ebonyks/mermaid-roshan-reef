# Chapter 3 Fairy Conservatory handoff — art provenance

Date: 2026-08-30

Status: owner-directed Fairy Pond correction selected after local visual and
static-art review. Exact Godot 4.7.2 runtime, device, child, owner, independent
Sol re-review, and release acceptance remain separate gates. The earlier Sol
pass applied only to the subsequently rejected Sky Lagoon version.

## Scope and gap

The approved Lily-Pad Fairy World is the location authority. Its existing V5
panorama and V2 pond plates are orthographic/top-down compositions, so direct
reuse inside an upright doorway would repeat the rejected perspective error.
The repository also did not contain a standalone true-2D walkable rainbow
causeway or Butterfly House landmark. Generation therefore covers the missing
eye-level Fairy Pond background plus those two foreground gaps.

No file under `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified. Review references supplied style,
color, architecture, and perspective only; none contributes delivery pixels.

## Selected correction — upright Fairy Pond background

- Built-in ImageGen result: `exec-f94c58c7-28bd-455d-897c-c0c7a16588a3`
- Native source: `raw/fairy_pond_horizon_openai_raw.png` (1672×941 RGB)
- Runtime master: `masters/handoff_background_master_3640x2048.png`
- Binding location/style reference:
  - `assets/fairy/pond_panorama.png`: aqua-to-violet water, lily pads,
    lavender reeds, sparkles, moonlit Fairy Pond identity.
  - `assets_src/fairy_v2/concepts/background_twilight.png` and
    `background_dawn.png`: approved Fairy World foliage, outline, and water
    language.
- Prompt brief used: Redraw the Lily-Pad Fairy World as a straight-ahead,
  eye-level pond vista for a 16:9 preschool stage. Keep the sky above a horizon
  no lower than the frame midpoint, keep every lily pad below that horizon,
  reserve a broad central water corridor for the rainbow walkway, carry the
  environment to the exact bottom edge, and exclude Sky Lagoon mountains,
  cabins, grass, roads, characters, buildings, bridge, HUD, and text.
- Processing: the complete flattened source is centered and uniformly fit to
  the 3640×2048 master with Lanczos resampling, then sliced into eight exact
  non-overlapping runtime tiles. There is no local retouch, object movement,
  seam blend, or independent tile generation. The selected native source and
  its hash remain preserved beside the master.

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

## Corrected continuous stage background

`tools/build_fairy_conservatory_handoff_art.py` normalizes the complete selected
Fairy Pond redraw to one continuous 3640×2048 16:9 master, then slices that
master into a 4×2 grid of non-overlapping 910×1024 runtime cards. No object is
independently regenerated across a seam. Input/output SHA-256 hashes,
dimensions, whole-canvas transform, reference authority, and runtime paths are
recorded in `asset_manifest.json`.

## Review status

- Alpha extraction: passed local visual inspection.
- Whole-subject containment: passed local visual inspection.
- Rainbow color order and perspective: passed local visual inspection.
- Butterfly House landmark readability: passed local visual inspection.
- Integrated 1280×720 composition, phone-scale target readability, hall-door
  continuity, exact threshold registration, Lily-Pad Fairy World identity, and
  larger-vision scope: passed local correction review on 2026-08-30. This
  scoped review cannot grant independent Sol, target-device, child, owner,
  exact-engine runtime, or release acceptance.
