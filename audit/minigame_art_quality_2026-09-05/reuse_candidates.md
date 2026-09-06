# Existing-art reuse audit for weak PictureGames assets — 2026-09-05

This is a visual reuse screen, not an acceptance score. I inspected the raster pixels of each listed candidate. No runtime binding or source asset was changed. A candidate must still pass provenance, exact-purpose mapping, Mobile runtime capture, contact/anchor checks, and independent Sol/Luna review.

## Direct findings

| Existing path | Intended use | Decision | Observed fit and blocking issue |
|---|---|---|---|
| `assets/terrain/flower.png` | One mature garden result | Candidate for a new family member, not direct drop-in | Clean transparent painted flower, strong contour/shading, readable stem and roots. It is a tall full plant whose aspect and rooted bottom do not match the current 228×228 mature-state slot; direct reuse would crop or change layout semantics. |
| `assets/terrain/flower2.png` | One mature garden result | Candidate for a new family member, not direct drop-in | Clean transparent three-flower plant with painted shading and roots. Strong visual finish, but its clustered composition and tall footprint cannot replace a single existing result without role/layout changes. |
| `assets/props/story/flower_coral.png` | One mature garden result | Single-state candidate only | Clean transparent single coral flower with roots and strong storybook contour. It cannot supply the complete six-state family (sprout plus five distinct results), and its full-plant scale needs a dedicated slot review. |
| `assets/props/story/flower_lavender.png` | One mature garden result | Single-state candidate only | Clean transparent lavender cluster with painted leaves and roots. Semantically flower-compatible, but clustered/tall and cannot be mapped across all mature roles. |
| `assets/fairy/sprites/boss_sprout.png` | Sprout | Rejected for direct reuse | High-finish transparent plant/bud, but it is a fairy boss growth state with oversized four-leaf framing and a curled central shoot. It lacks the current garden sprout’s simple soil-contact/readability role and would change stage semantics. |
| `assets/fairy/sprites/boss_seed.png` | Seed/sprout | Rejected | High-finish transparent asset, but the seed is a large cracked rock with an emerging plant, not the garden’s tappable seed/sprout progression. |
| `assets/art35/cards/mg/wateringcan_wateringcan.png` | Watering can | Rejected | Transparent but flat icon geometry with no painted material, handle/spout detail, or approved can angle; weaker than a replacement target. |
| `assets/art35/cards/mg/carrot_carrot.png` | Carrot | Rejected | Same simple flat card-style carrot treatment as the live weak carrot; no material or contour improvement. |
| `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_farmer_gameplay_carrot.png` | Carrot | Rejected | Viewed image is a pig character on a dark framed concept card, not a clean carrot prop; cannot be cropped/reused as runtime art. |
| `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_farmer_stage_states_flower_parallax.png` | Garden flowers | Rejected | Framed dark concept card containing a ground border and flower bed; no isolated transparent object and wrong multi-object composition. |
| `assets_src/sky_lagoon/qa_kit/lagoon_flower_cluster_lavender.png` / `_coral.png` | Mature flower | Rejected | Visible pale background and low-detail faceted/flat rendering; wrong medium and alpha for the painted garden family. |

## Live weak controls

`assets/mg/wateringcan.png` visibly contains the can plus background/plant pixels and a hard crop boundary. `assets/mg/carrot.png` is a small flat silhouette with minimal material treatment. The live garden sprout and five mature files are a simple pastel/vector-like family. The inspected reuse set does not provide a complete role-compatible replacement family.

## Replacement recommendation

Do not force a partial swap. The best reuse path is to treat the coral and lavender story flowers, and possibly the terrain flower variants, as style/identity references or one-state candidates while commissioning or locating a coordinated family of one sprout plus five mature results. Watering can and carrot remain genuine replacement gaps; no clean transparent, correctly angled, child-readable watering can or carrot was found in the inspected approved/runtime inventory.
