# Full Texture Regeneration Post-Stress Analysis - 2026-07-18

This update compares the original game-wide audit with the completed isolated
candidate pass in `assets/full_texture_regen_2026-07-18/`. Northern Kingdom is
included. Runtime asset paths have not been changed.

## Final Candidate Coverage

- 88 audited roles
- 85 rebuilt roles with candidates
- 137 GLB models and 30 normalized PNG textures
- 137/137 models passed structural and render stress
- 30/30 textures passed size, alpha, entropy, and edge stress
- 85/85 target roles have at least one candidate
- 17 Northern Kingdom candidates are included
- 28 accepted and 1 rejected image-generation source are retained
- 2 book assets remain source-locked at 5/5
- 1 cat/manual-toy role remains intentionally ungenerated

Generated work is recorded as 4/5 candidate work. Only owner acceptance can
promote a candidate to 5/5.

## Failures Caught During This Pass

1. **Generic geometry survived file-level audit.** Early procedural families
   were technically valid but collapsed into recolored primitives. Coral was
   split into antler, fan, brain, table, whip, and finger growth families;
   Northern houses received six different configurations; snow peaks became
   vertical crags instead of rock piles.
2. **Color-space conversion washed out the palette.** Blender inputs were
   initially treated as linear values. Explicit sRGB-to-linear conversion
   restored the intended pastel saturation and navy/lavender separation.
3. **Correct category did not guarantee correct anatomy.** The first generated
   butterfly had four visible legs; the validator also briefly miscounted wing
   motif layers as extra wings. The accepted source has four complete wings,
   six legs, and two antennae, while structural checks now use exact anatomy
   component names. Shrimp, octopus, jellyfish, and fish models use named,
   countable anatomy.
4. **A seamless file can still make a repetitive environment.** The first
   Butterfly World meadow showed an obvious grid. The pack now supplies three
   seam-safe variants and carries a hard deployment rule against repeating one
   variant en masse. Repetition remains a composition concern, not merely an
   edge-pixel concern.
5. **Transparent cutouts retained matte color.** The lavender ornament source
   failed alpha/chroma review and was regenerated rather than accepted through
   cleanup. Connected-background removal and alpha-ratio checks remain required.
6. **Render validation can fail independently of geometry.** Initial review
   lights were not scaled to asset bounds, producing overexposed small props and
   dark large worlds. Bound-relative camera and light placement fixed four blank
   or unreadable world renders.
7. **Bright forms disappeared at phone scale.** White cloud and snow forms read
   in close-up but lost their silhouette on bright scenes. Clouds gained a
   restrained navy/lavender underside and stronger wind-curl geometry, then the
   entire pack was rerendered and revalidated.
8. **Functional state was mistaken for asset variety.** Empty Christmas trees,
   decorated trees, and loose ornaments are not redundant variants. Their roles
   are now explicit: R075 is the start state, R084 contains manipulated pieces,
   and R076 is the completed state with exactly five ornaments.
9. **Protected identity could be changed by a presentation rebuild.** R020 now
   provides frames and placement only; protected paintings are mounted unchanged.
   Carrot and watering can remain untouched, and cat/toy work stays manual-only.

## Updated Recurring Failure Guide

### Silhouette Before Texture

Reject a focal asset when its identity depends on a label, color swap, or surface
detail. At 112 px, the outline must distinguish stars, gates, houses, creatures,
vehicles, and interactive props without explanatory text.

### Families Need Structural Variation

Three recolors of one mesh are one asset, not a family. Variation must change
height rhythm, mass distribution, profile, opening placement, branching, or
functional attachments. Review the family together and at placement density.

### Anatomy Must Be Both Visible and Machine-Checkable

Name and count the defining parts, but also inspect the rendered silhouette.
Validators must ignore decoration layers and test exact structural components.
For small creatures, paired appendages must remain separable at gameplay scale.

### Cel Shading Is an Art System, Not a Saturation Filter

Required ingredients are broad color grouping, dark contour or geometric edge
accents, cool aqua/lavender shadow logic, low specularity, and restrained value
ranges. Glossy plastic, unbounded white, black ambient shadows, and noisy PBR
detail remain automatic review failures.

### Repetition Requires Deployment Evidence

Edge matching is necessary but insufficient. Every tile or clump family needs a
3x3 repetition view and an authored placement rule. Large motifs should wrap
once or use variants; mass foliage needs multiple asymmetric profiles and density
limits to avoid both patterning and transparent overdraw.

### Biome and Gameplay Purity

Reusable undersea assets cannot include flowers, sky, beach, or baked ground.
Interactive pieces cannot be merged into their completed state. Backgrounds,
props, effects, and objective signals remain separate so the game can animate,
hide, collect, or replace them independently.

### Bright-Scene Contrast Must Be Tested on Mobile

Pastel does not mean low contrast. White, snow, cloud, ice, and pale architecture
need cool edge accents or a darker underside. Test on the actual Mobile renderer
at gameplay size; a studio close-up cannot prove readability.

### Source Lock Is a Pipeline Feature

Protected paths and known book-derived roles must be explicit exclusions before
generation begins. Presentation candidates may frame protected art but never
redraw it. Rejected and superseded generations stay in the repository so the
same failure is not unknowingly repeated.

## Residual Risks and Integration Requirements

- Owner visual review is still required before any candidate becomes 5/5.
- The R044 ground must follow its randomized/wrap-once deployment rule.
- R020 frames must receive existing protected paintings without texture changes.
- R083 cat parts require the child's own source material and manual production.
- Runtime integration needs role-by-role backup, staging screenshots, Mobile
  performance captures, and probe validation. This pass intentionally stops
  before modifying working game assets.

The complete per-role verdict is in
`audit/full_regen_2026-07-18/candidate_role_review.csv`; every generated file is
listed in `candidate_asset_review.csv` and hashed in the pack manifest.
