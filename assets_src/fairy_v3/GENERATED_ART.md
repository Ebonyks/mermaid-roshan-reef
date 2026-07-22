# Fairy Pond V3 continuous backgrounds

The three background masters were generated with the built-in OpenAI image
generation tool on 2026-07-22. They replace only the Fairy Pond floor plates;
the V2 bugs, leaf shield, and five flower-growth reliefs remain unchanged. No
protected book art, family voice, or friend source was used or modified.

The full-size generated files remain in the Codex generated-image store. The
registered project masters in `concepts/` are normalized to 1024x1024. Runtime
plates are rebuilt by `tools/process_fairy_background_flow.py`.

## Shared texture contract

- Orthographic top-down pond corridor with an open central flight lane.
- One consistent fine-paper watercolor grain, thin indigo-blue contour weight,
  rounded stone scale, sea-glass lily pads, scalloped moss banks, and lavender
  wetland flowers.
- Medium aqua, mint, moss, lavender, and periwinkle palette; no separate
  vignette, moon icon, decorative frame, characters, text, or watermark.
- Compatible horizontal bank edges so the three 3D floor plates read as one
  continuous environment.

## Prompt set

1. `background_dawn_master.png`: establish the master storybook texture family
   at calm magical dawn, balancing the pale V2 dawn and saturated V2 twilight;
   preserve a quiet central 55 percent and restrain lily-pad density.
2. `background_twilight_continuation.png`: use the new dawn plate as the exact
   style/material reference; continue its corridor and shift only gently into
   friendly blue-hour light with sparse warm firefly points at the banks.
3. `background_boss_continuation.png`: use the new twilight plate as the exact
   reference; continue the same pond and widen only the central water into a
   readable boss pool with subtle lavender ripple arcs, without a circular
   vignette or daylight reset.

## Reproducible finishing pass

`tools/process_fairy_background_flow.py` normalizes the sources to 1024px,
reduces saturation toward one material family, adds a shared 6 percent aqua
balance tint, and targets mean luminance 182 -> 170 -> 166. Each next plate
begins with a crisp mirrored continuation of the previous shoreline; its color
ramps toward the next phase before a narrow interior dissolve returns to the
authored continuation. The resulting adjacent edge-row delta is zero.

`tools/audit_fairy_art_v2.py` rejects a background sequence when an adjacent
luminance jump exceeds 16, mean-palette distance exceeds 48, or edge seam mean
error exceeds 2.
