# Full Texture Regeneration Failure Analysis - 2026-07-18

This report freezes the pre-regeneration baseline for every runtime role in
`audit/game_art_ledger_pass35_2026-07-16.csv`. Northern Kingdom is in scope.
Protected book/family art and manually sourced cat/toy work remain excluded.

## Scope

- Audited runtime roles: **88**
- Regeneration targets: **85**
- Protected/manual exclusions: **3**
- Candidate destination: `assets/full_texture_regen_2026-07-18/`
- Score ceiling before owner review: **4/5**

## Frequent failure patterns

- **primitive or generic geometry:** 38 target roles
- **uncategorized polish gap:** 16 target roles
- **anatomy or identity error:** 13 target roles
- **composition scale or occlusion:** 11 target roles
- **missing runtime validation:** 9 target roles
- **repetition tiling or overdraw:** 8 target roles
- **material or rendering mismatch:** 7 target roles
- **environment or biome language:** 4 target roles
- **exposure bloom or emission:** 3 target roles
- **pipeline integrity or orphans:** 3 target roles

## Production implications

1. Silhouette and composition are judged before surface detail. A painted texture cannot rescue primitive focal geometry.
2. Repeated families require multiple asymmetric profiles and mass-placement captures; one attractive close-up is insufficient.
3. Materials use broad pastel color blocks, indigo outline shells, and matte-to-satin response. Avoid glossy plastic, black shadows, and white clipping.
4. Creatures must pass explicit anatomy checks. Butterflies need four separable wings; beetles need six legs and three readable body masses.
5. Reusable assets cannot bake ground islands, mixed biomes, cast shadows, or unrelated props into one texture or mesh.
6. Functional pieces remain separate when gameplay manipulates them: gates, ornaments, music bars, bells, and vehicle track signals.
7. Every candidate requires near, mid, gameplay-distance, repetition, reverse-angle, and Mobile-renderer evidence before owner review.
8. Orphans, duplicate extraction textures, corrupt provenance images, and unmerged material exports fail the pack even when they look acceptable.

## Exclusions retained in the ledger

- `R081_picture_games_carrot` - Picture Games / carrot: exclude_protected
- `R082_picture_games_watering_can` - Picture Games / watering can: exclude_protected
- `R083_picture_games_cat_parts` - Picture Games / cat parts: exclude_protected

## Next evidence update

After generation and stress testing, this report will gain post-pass failure
counts, rejected-iteration reasons, structural metrics, and links to the full
near/mid/gameplay contact sheets. No role becomes 5/5 until owner acceptance.
