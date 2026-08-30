# Moonflower Conservatory doorway provenance

The dormant doorway and open architectural frame were created 2026-08-30 with
the built-in OpenAI image-generation tool. License: project original, all
rights reserved. URL: none. The final open destination is not generated
scenery: it is a deterministic composite of already-approved runtime art. No
protected book art, family voice, or friend portrait was modified,
recompressed, or used as delivery pixels.

The accepted Main Hall screenshots were style, material, front-perspective, and
scale references only. Runtime alpha, 1024-square normalization, opening-mask
replacement, horizon placement, and stage-cutout placement are deterministic
processing by
`tools/build_fairy_conservatory_door_art.py`.

## Selected closed state

Generated source:
`raw/moonflower_door_closed_checker_raw.png`
(`exec-7f34dd4c-331b-49eb-902d-bf7f0150811b.png`).

Final prompt:

> Create the BEFORE state of a hidden Moonflower Conservatory entrance for the
> Pearl Castle Main Hall: a dormant, sealed, tall shell-framed arched relief
> with two closed lavender moonflower petals meeting like doors, one small
> pearl center, and subtle butterfly-wing geometry in the carved trim. Match
> the accepted Pearl Castle's straight-on 2D storybook palette and materials.
> Isolated cutout only; no surrounding wall, floor, characters, fairies, bugs,
> text, UI, open gap, portal ring, 3D rendering, or watermark.

## Selected open state

Architectural source:
`raw/moonflower_door_open_checker_raw.png`
(`exec-0a904f77-34d6-4014-8e60-19b232325232.png`). Its generated garden is a
placeholder removed in full by the deterministic opening mask; only the shell
frame, edge-on lavender leaves, hinges, flower carvings, and single crown pearl
remain delivery pixels.

Architecture correction prompt:

> Create the corrected final complete square doorway asset. Preserve the
> straight-on shell architecture and narrow edge-on open purple doors. Place
> one central pearl in the shell crown and no pearl knobs or mirrored circular
> ornaments on the door leaves, side frames, hinges, or handles. Keep the
> camera straight-on and isolate the doorway on a plain light field.

The final runtime view inside that architecture reuses these exact project
assets; the manifest records each SHA-256:

- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r{0..1}_c{0..5}.png`
- `assets/flats/fairy_conservatory_handoff/rainbow_walkway.png`
- `assets/flats/fairy_conservatory_handoff/butterfly_house.png`
- `assets/mg/butterfly.png`

The horizon is authored at `y = 468 / 1024` (45.7% of the complete frame).
The Butterfly House sits at that eye-level destination line and the rainbow
causeway widens toward the threshold. Both new subjects are the targeted art
gaps documented in
`assets_src/fairy_conservatory_handoff_2026-08-30/PROVENANCE.md`; they are
scaled only as whole transparent sprites. This view therefore previews the
intermediate Rainbow Stage instead of falsely opening straight into the Fairy
Pond.

## Rejected iterations retained

- `raw/moonflower_door_open_wide_rejected.png`: open leaves remained flat in
  the image plane and the destination used an overhead pond plate.
- `raw/moonflower_door_open_pond_rejected.png`: hinge angle improved, but the
  upright doorway still exposed a top-down pond and duplicated the pearl as two
  handles.
- `raw/moonflower_door_open_sky_horizon_rejected.png`: the eye-level sky/path
  correction was good, but multiple pearl-like beads remained and the horizon
  needed its final placement cleanup.
- `raw/moonflower_door_open_generated_garden_rejected.png`: one-pearl,
  edge-on-door geometry was acceptable, but its invented floating gardens and
  generic flower path did not match Fairy Pond or Butterfly World. It is kept
  only as rejection evidence and contributes no destination pixels.

The repository manifest records source, alpha-master, and runtime SHA-256
hashes after the deterministic build.

The two 1280×720 files under `review/` reconstruct the approved 7280×2048 Main
Hall from its sixteen existing runtime tiles, apply the exact logical center
and `0.4896` card scale used by `FairyConservatoryDoor2D`, crop one 1672×941 Hall view,
and resize that whole view to the 1280×720 base canvas. They are placement
evidence only (`delivery_pixels: false`) and do not replace either runtime door
card or any accepted Hall pixel.
