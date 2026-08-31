# Chapter 3 Fairy Conservatory handoff — art provenance

Date: 2026-08-30

Status: owner-directed Fairy Pond correction rebuilt after independent Sol
found a native-coverage enlargement and a threshold strip in the first
correction. The six-panel native replacement passes focused independent Sol
art review. Exact Godot 4.7.2 runtime, device, child, owner, and release
acceptance remain separate gates. The earlier Sol pass applied only to the
subsequently rejected Sky Lagoon version.

## Scope and gap

The approved Lily-Pad Fairy World is the location authority. Its existing V5
panorama and V2 pond plates are orthographic/top-down compositions, so direct
reuse inside an upright doorway would repeat the rejected perspective error.
The repository also did not contain a standalone true-2D walkable rainbow
causeway or Butterfly House landmark. Generation therefore covers the missing
eye-level Fairy Pond background plus those two foreground gaps.

No file under `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified. Existing Fairy Pond art supplies
location, palette, foliage, water, and outline authority only; no protected or
Sky Lagoon pixel is inserted into the new background.

## Selected correction — native-coverage upright Fairy Pond background

- Six selected 1254×1254 built-in ImageGen panels:
  - `top_left.png`: `exec-95013e94-cb9e-459f-a7c6-88ce52d70abb`
  - `top_center.png`: `exec-a1798b3a-d111-402b-a08e-455f15694cb2`
  - `top_right.png`: `exec-e3c60551-45fb-46aa-8dd8-38997d075a82`
  - `bottom_left.png`: `exec-11630358-710f-4636-b283-ffe0a1ccc2ab`
  - `bottom_center.png`: `exec-f6352de8-a64d-45b1-b5dc-855e8c9ed7a7`
  - `bottom_right.png`: `exec-039ee267-2c93-4ccf-bf3c-55fcfad0df70`
- Runtime master: `masters/handoff_background_master_3640x2048.png`.
- Retained non-delivery references:
  `raw/fairy_pond_horizon_openai_raw.png` (1672×941) and
  `raw/fairy_pond_native_center_openai_raw.png` (1254×1254). Neither is
  enlarged or inserted into the selected master.
- Binding location/style references:
  - `assets/fairy/pond_panorama.png`: aqua-to-violet water, lily pads,
    lavender reeds, sparkles, and Fairy Pond identity.
  - `assets_src/fairy_v2/concepts/background_twilight.png` and
    `background_dawn.png`: approved Fairy World foliage, outline, and water
    language.
- Shared prompt brief: polished 2D Lily-Pad Fairy World storybook art using
  the approved Fairy Pond palette and rounded painted forms; upright eye-level
  sky-and-water perspective; no Sky Lagoon motifs, characters, text, HUD, or
  readable object at a join.
- Panel prompt set:
  - top left: left garden bank, open sky and pond at the right join;
  - top center: open central sky/pond corridor with a clear horizon;
  - top right: right garden bank, open sky and pond at the left join;
  - bottom left: water-only foreground, left bank and open water right;
  - bottom center: pure open aqua/deep-blue corridor, no plants;
  - bottom right: water-only foreground, right bank and open water left.
- Processing: `tools/build_fairy_conservatory_handoff_art.py` places every
  panel at exact 1:1 pixel scale. Top horizons are aligned at `y=480` using
  lossless cropping plus one 12-pixel reflection of open sky. Broad,
  low-frequency palette harmonization affects only the center panels; it does
  not move or redraw a painted form. Linear feathers stay inside generated
  open-sky/open-water overlaps. No source image is enlarged. The complete
  3640×2048 master is then sliced into eight exact non-overlapping runtime
  tiles. Every source, master, and tile has a manifest hash.

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

`tools/build_fairy_conservatory_handoff_art.py` assembles one continuous
3640×2048 16:9 master from the six native generated panels, then slices that
master into a 4×2 grid of non-overlapping 910×1024 runtime cards. No source
pixel is enlarged and no readable object crosses a generated join. Input/output
SHA-256 hashes, dimensions, source placements, reference authority, and runtime
paths are recorded in `asset_manifest.json`.

## Review status

- Alpha extraction: passed local visual inspection.
- Whole-subject containment: passed local visual inspection.
- Rainbow color order and perspective: passed local visual inspection.
- Butterfly House landmark readability: passed local visual inspection.
- Integrated 1280×720 composition, phone-scale target readability, hall-door
  continuity, full-width threshold coverage, Lily-Pad Fairy World identity,
  native per-screen coverage, and larger-vision scope: passed local correction
  review on 2026-08-30.
- Independent Sol focused artistic review: **PASS** on 2026-08-30. It found no
  visible panel seam at 1280×720, no procedural extension or repeated-stamp
  issue, a fully filled Hall threshold, correct upright pond perspective, no
  Sky Lagoon leakage, and clear castle→Rainbow Skyway→Butterfly House→Fairy
  World progression. Target-device, child, owner, exact-engine runtime, and
  release acceptance remain separate.
