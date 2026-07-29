# Sky Lagoon playground revision — 2026-07-29

All generated imagery in this directory was made with the built-in Codex
image-generation tool in default mode. No CLI, API, Blender, model, mesh, or
runtime 3D art was used.

## Accepted single-seat swing

Reference inputs:

- Existing two-seat swing: style and materials only.
- `roshan_swing_0.png`: authored two-hand pose and mermaid-seat clearance only.

Accepted prompt:

> Use case: precise-object-edit. Asset type: transparent 2.5D game prop sprite
> for a preschool Mermaid Roshan playground. Image 1 is the exact swing-set
> edit target. Image 2 is a character pose reference used only to measure the
> horizontal spacing of Roshan's two closed hands; do not add the character.
> Preserve the complete accepted swing design from Image 1, but move its
> exactly two suspension ropes inward so that, when Roshan from Image 2 is
> centered on the shell chair, each straight vertical rope passes directly
> behind and through the center of one closed hand. Her hands are approximately
> shoulder-width apart. Attach the two ropes to two gold fittings near the
> inner left and inner right of the chair, rather than its outer arms. Keep the
> large wide supportive shell chair unchanged and centered. Keep exactly one
> swing seat, exactly two ropes, the sturdy teal A-frame, shell ornaments,
> colors, painted PNW storybook style, perspective, full-prop framing, and flat
> solid #ff00ff chroma background. Empty prop; no person. Avoid two seats, four
> ropes, a tiny seat, spare ropes, shadows, scenery, 3D rendering, Blender look,
> text, or watermark.

Files and SHA-256:

- `swing_single_mermaid_gripfit_chroma_raw.png` — 1338×1176,
  `d0939f1071ea7c7c45225399931a6305de06ff30db382456789bd47eb9595545`.
- `swing_single_mermaid_gripfit_alpha_master.png` — 1338×1176,
  `0d62941af2a3a5c6b0436242c7fbd0959983c78a10adbb1637571d3c229d4e21`.
- Runtime card `assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png`
  — 655×576,
  `cf75805c32df02bb6e8d92d536e65a41cec1c8587a21db383b84c1c2f36e31fd`.

The full alpha master is preserved. The runtime card is a single Lanczos
downsample to 2.47 authored pixels per displayed 720p pixel, inside the
Speedy-tier density and mobile-texture limits. The runtime animation uses a
1.38 horizontal pose scale; the grip-fit capture verifies both authored fists
sit on the two rope centers without increasing Roshan's height.

Two other iterations are retained for audit:

- `swing_single_mermaid_chroma_raw.png`: one-seat structural pass rejected
  because its rope pair was too wide for the authored grip.
- A stricter normalized-position edit was visually reviewed but rejected
  because it did not improve the accepted rope geometry; it was not installed.

## Screen-one/screen-two bush repair

Accepted prompt:

> Use case: precise-object-edit. Asset type: one source tile in a continuous
> 6×2 high-resolution Sky Lagoon background grid. Preserve its exact square
> composition and every pixel outside the localized tree repair as closely as
> possible. Remove only the single oversized dark-green conifer tree stamped
> into the foreground bush near the lower center-left. Replace that tree
> footprint naturally with the same low rounded leafy shrub canopy and distant
> small conifer line already surrounding it, so no tall foreground tree remains
> in this tile. Keep the sky, clouds, snowy mountains, distant tree line,
> foreground shrub boundary, rocks, flowers, palette, perspective, lighting,
> framing, dimensions, and all edge pixels unchanged. Avoid new trees, pasted
> stickers, repeated stamps, changed scenery, blur, crop, padding, borders,
> text, characters, equipment, frames, plane, castle, or watermark.

- `tile_r0_c1_stamp_removed_raw.png` — 1254×1254,
  `63d5e34a606d5a4f1520b8b0181cb2c542540b95a60ba76ba659717414b4f049`.

The repair is installed through `GRID_RAW_OVERRIDES`; it receives the original
115px seam feather rather than being pasted onto the assembled panorama. The
separate near-tree Sprite3D at x=-27 was also retired because it was the
remaining visible “asset stamp” against the otherwise complete hedge.
