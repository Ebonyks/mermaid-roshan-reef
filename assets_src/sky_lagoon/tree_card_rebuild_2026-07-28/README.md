# Sky Lagoon tree-card rebuild source ledger

Generation mode: OpenAI built-in image generation, project-bound local edit
workflow. External references: none.

- `tile_r0_c0_tree_removed_raw.png`: removed the left shoreline evergreen;
  restored sky, clouds, mountains, and low shore vegetation.
- `tile_r1_c0_tree_removed_raw.png`: removed the remaining trunk; restored a
  readable water/stone/shrub boundary.
- `tile_r0_c1_tree_removed_raw.png`: removed the foreground fir cluster;
  restored sky, mountains, cloud bank, and distant forest silhouettes.
- `tile_r1_c1_tree_removed_raw.png`: removed the remaining trunks; restored
  low shrubs, flowers, stones, and path edge.
- `tile_r0_c4_tree_removed_raw.png`: removed the castle-approach fir; restored
  the mountain path and flowered slope while preserving the castle tower.
- `tile_r1_c4_tree_removed_raw.png`: removed the remaining trunk; restored low
  vegetation, lagoon edge, castle, bridge, and path.
- `tree_sticker_family_raw.png`: a three-member transparent PNW evergreen
  family—tall, medium, and slender—with planted stone-and-shrub footings.

Accepted runtime derivatives are prepared by
`tools/prepare_sky_lagoon_tree_cards.py`. It preserves neighboring seams,
heals regenerated horizontal joins, reconstructs the exact 6144x2048 master,
creates twelve lossless tiles, removes the generated checker, crops alpha
bounds, and applies the audited Speedy-tier density/matte grade.
