# Sky Lagoon reductive 6×2 rebuild

Mode: OpenAI built-in image generation (`imagegen`) for raster edits, followed
by deterministic local assembly and chroma-key removal. No Blender, model,
GLB, CLI image-generation API, canvas extension, or runtime mesh was used.

The approved 2172×724 panorama remains the composition reference. It is not a
runtime texture. Twelve independently detailed 1254×1254 overscan edits are
feathered into one 6144×2048 exact-3:1 master, then cropped losslessly into a
6×2 grid of 1024×1024 Sprite3D cards. Each 2048×2048 playable screen therefore
receives four native tiles.

## Tile prompt set

Common prompt:

> Precise image edit. This is one overscanned tile of 12 for a seamless native
> 6144×2048 Mermaid Roshan Sky Lagoon background. Faithfully repaint this exact
> crop at maximum native detail in the established pastel storybook / Codex PNW
> asset-pack design language. Preserve edge colors and geometry for overlap
> feathering. No text, watermark, border, canvas extension, blur, hard seam, or
> redesign.

Tile-specific constraints:

- r0c0: preserve the far-left tree, clouds, and mountain valley.
- r0c1: preserve the isolated ridge fir and low shrub canopy; do not restore
  the removed foreground grove.
- r0c2: remove ghosted/tall foreground conifers; heal with low shrubs and
  distant tiny fir silhouettes.
- r0c3: remove tall foreground conifers; retain the off-road hillside cabin.
- r0c4: retain the snow-capped mountain, three terrace cabins, and completely
  unobstructed winding road; remove the ghosted foreground tree.
- r0c5: keep castle/drawbridge absent; remove foreground conifers and heal the
  shore for separate depth cards.
- r1c0: preserve blocked water access, stepping stones, rope posts, and path.
- r1c1: remove cropped large trees; preserve path, lawn, flowers, and shrubs.
- r1c2: preserve an open playground lawn and straight path; remove ghosted
  large trees.
- r1c3: preserve the open playground lawn, path, and partial off-road cabin;
  remove foreground tree canopies.
- r1c4: keep castle/drawbridge absent; preserve the clear path junction, lake,
  and mountain route; remove the castle-side tree.
- r1c5: keep castle/drawbridge absent; preserve lake, shoreline, path, and
  flowers; remove the castle-side tree.

## Castle extraction prompt

> Background extraction only. Isolate the complete approved Mermaid Roshan
> castle and its attached drawbridge exactly as shown, including every purple
> tower, shell finial, turquoise window, coral door, gold railing, stone
> footing, and the Mermaid Roshan stained-glass panel. Preserve its exact 2D
> storybook design, proportions, colors, outlines, front view, and bridge
> perspective. Remove all scenery. Place only the intact castle plus drawbridge
> on solid #00FF00 with no shadow, spill, text, watermark, or redesign.

The generated glass was rejected because its character rendering drifted.
`stained_glass_owner_reference.png` is the owner-supplied replacement. The
preparation tool restricts its pixel changes to the existing gold window
frame; `audit/sky_lagoon_stained_glass_replacement.json` records the changed
bounds and confirms zero changes outside the window.

## Reused approved assets

- `sky_lagoon_plane_v5_hd_grade.png` remains the Day One arrival plane.
- `sky_lagoon_tree_sticker_{tall,medium}_v1.png` are the existing approved PNW
  cutouts derived from prior mural trees; no new tree family was generated.
- Existing playground equipment, frames, book pages, Roshan sprites, contact
  shadows, and the single drifting cloud are reused unchanged.

