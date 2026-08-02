# Sky Lagoon 6x2 HD generation record

The 6144x2048 v3 panorama uses twelve OpenAI built-in image-generation edits.
Each input was one exact 362x362 crop from the approved 2172x724 v2 master,
ordered `tile_r0_c0` through `tile_r1_c5`.

Shared prompt:

> Use case: precise-object-edit. Asset type: one tile in a seamless 6-column
> by 2-row high-resolution game-background reconstruction. Faithfully repaint
> this exact square reference crop with much higher native painted detail.
> Preserve the established Mermaid Roshan pastel hand-painted storybook sprite
> style, every object, silhouette, crop boundary, camera, scale, and placement
> exactly. Square output. No text, watermark, new objects, removed objects,
> shifted objects, or canvas extension. Maintain edge colors and geometry for
> direct stitching. Increase only fine painted texture and edge clarity.

Tile-specific invariants:

- `r0c0` through `r0c3`: preserve all trees, clouds, mountains, and flowers.
- `r0c4`: preserve the mountain path and castle towers.
- `r0c5`: preserve the Mermaid Roshan stained-glass subject and architecture.
- `r1c0`: preserve the water edge, stepping stones, rope posts, and runway.
- `r1c1`: preserve the path, lawn, rocks, shrubs, and flowers.
- `r1c2` and `r1c3`: keep the playground lawn open and empty for Sprite3D
  equipment cards.
- `r1c4`: preserve the castle base, lagoon, drawbridge, and path junction.
- `r1c5`: preserve the castle door, drawbridge, lagoon, and foreground flora.

The generated interiors were resized to 1024px squares and joined with a
96px source-conditioned edge transition. The full master and twelve runtime
tiles are the preserved outputs; temporary service files are not required to
ship or reproduce the crop, stitch, and audit stages.
