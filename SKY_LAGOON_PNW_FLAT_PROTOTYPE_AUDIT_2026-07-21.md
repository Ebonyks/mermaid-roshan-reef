# Sky Lagoon PNW flat-prototype audit — 2026-07-21

## Decision

The realistic PNW botanical sheets and the procedural Blender replacements are
rejected. They do not belong to the established Sky Lagoon family. The accepted
art-direction source is now the pair of flat prototype sheets in this branch:

- `assets_src/concepts/sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png`
- `assets_src/concepts/sky_lagoon_pnw_shrub_variants_flat_2026-07-21.png`

The twenty-four named cards under `assets_src/concepts/sky_lagoon_pnw_flat/` are
cropped references for later modeling. They are not runtime textures and no
shipped GLB or scene placement changes in this pass. The current accepted GEN2
plus GEN5 runtime tree family therefore remains the safe fallback.

The first six-shrub sheet is superseded. Evergreen huckleberry repeated salal's
dark rounded berry mound and pale bell-flower read at phone scale. Native
trailing blackberry (`Rubus ursinus`) replaces it, and every shrub now has two
structurally distinct prototypes. A/B variants change footprint, height/width
ratio, foliage-mass placement, stem gesture, negative space, and accent
placement; mirrors, recolors, and flower-only rearrangements do not qualify.
An initial variant pass also repeated crescent, bridge, and tunnel silhouettes
across several species. That pass is rejected. Trailing, creeping, cane-arch,
and tunnel-like forms are now exclusive to trailing blackberry; the other B
variants use terraced, spear-fan, candelabra, tiered-wedge, and clustered-tower
architectures.

## Why the previous families failed

The successful Sky Lagoon group communicates an object with a large silhouette,
two to five primary volumes, broad color planes, and one or two oversized story
cues. The realistic botanical sheets instead communicated species through leaf
anatomy, bark, thin twigs, and dense repeated detail. Those sheets were polished
as field-guide illustrations but foreign to the rounded toy-diorama world and
impractical as Mobile mesh blueprints.

The subsequent procedural Blender family compounded the problem. Species facts
were converted directly into branch algorithms before composition and character
had been approved in 2D. This produced repeated crown blobs, visible mechanical
branch scaffolds, poor value separation, and near-black shrubs in the scene.
Technical CI success did not make those models visually acceptable.

| Family | Standalone design | Sky Lagoon consistency | Mobile modelability | Decision |
| --- | ---: | ---: | ---: | --- |
| Existing quality-kit group | 4.7–4.9 | 4.8 | 4.7 | primary style anchor |
| Rejected realistic PNW sheets | 4.7 | 3.4 | 2.8 | reject |
| Rejected procedural PNW GLBs | 3.0–4.3 | 3.2 | 3.8 | reject despite green run `29840034919` |
| Corrected flat PNW prototypes | 4.6–4.9 | 4.7–4.9 | 4.6–4.9 | accept as modeling references |

## Shared visual grammar

The corrected family matches `sky_lagoon_quality_2026-07-20.png` through:

- a single readable silhouette at phone scale;
- two to five main crown or foliage masses rather than leaf-level geometry;
- rounded, hand-shaped toy proportions and broad cel-shaded planes;
- the established mint, aqua, sage, lavender, coral, cream, muted-gold, warm
  wood, and navy-purple palette;
- one oversized species cue, such as a drooping leader, maple emblem, pale
  paired trunk, madrone ribbon, flower, tassel, or berry cluster;
- a compact planted base that visually belongs beside the fountain, train,
  playground, castle, and existing meadow plants.

The small painted grooves inside foliage are surface-language suggestions, not
instructions to create separate leaf meshes. A Blender interpretation must
preserve the primary masses and emblematic cue while simplifying those grooves.

## Accepted item audit

The computer-review ceiling is 4.9/5. Every prototype passes the 4.5 threshold;
acceptance here means **flat modeling reference accepted**, not runtime asset
accepted.

| Prototype | Species read | Group consistency | Modelability | Overall |
| --- | ---: | ---: | ---: | ---: |
| Coastal Douglas-fir | 4.8 | 4.8 | 4.8 | 4.8 |
| Western redcedar | 4.8 | 4.8 | 4.7 | 4.8 |
| Western hemlock | 4.9 | 4.8 | 4.7 | 4.8 |
| Sitka spruce | 4.7 | 4.8 | 4.7 | 4.7 |
| Shore pine | 4.9 | 4.8 | 4.8 | 4.8 |
| Pacific yew | 4.7 | 4.8 | 4.8 | 4.7 |
| Bigleaf maple | 4.9 | 4.9 | 4.8 | 4.9 |
| Red alder | 4.8 | 4.7 | 4.8 | 4.7 |
| Black cottonwood | 4.7 | 4.7 | 4.7 | 4.6 |
| Pacific madrone | 4.9 | 4.9 | 4.8 | 4.9 |
| Garry oak | 4.9 | 4.8 | 4.8 | 4.8 |
| Pacific dogwood | 4.9 | 4.9 | 4.8 | 4.9 |
| Salal A | 4.8 | 4.8 | 4.8 | 4.8 |
| Salal B | 4.8 | 4.9 | 4.9 | 4.9 |
| Low Oregon grape A | 4.9 | 4.9 | 4.9 | 4.9 |
| Low Oregon grape B | 4.8 | 4.8 | 4.8 | 4.8 |
| Red-flowering currant A | 4.8 | 4.8 | 4.8 | 4.8 |
| Red-flowering currant B | 4.9 | 4.9 | 4.8 | 4.9 |
| Oceanspray A | 4.8 | 4.8 | 4.8 | 4.8 |
| Oceanspray B | 4.8 | 4.8 | 4.8 | 4.8 |
| Salmonberry A | 4.9 | 4.9 | 4.9 | 4.9 |
| Salmonberry B | 4.9 | 4.9 | 4.9 | 4.9 |
| Trailing blackberry A | 4.9 | 4.9 | 4.8 | 4.9 |
| Trailing blackberry B | 4.9 | 4.9 | 4.9 | 4.9 |

## Translation and placement gate

No future mesh passes merely because it resembles the reference from one view.
Each Blender version must independently score at least 4.5 in isolated 0°, 45°,
and 135° views and in the Godot Mobile scene. It must use broad volumes, keep
the intended color/value separation, avoid thin twig networks and individual
leaf clutter, and remain recognizable at the target phone scale.

Placement must also preserve ecological continuity:

- snow: Douglas-fir, western redcedar, western hemlock, Sitka spruce, or shore
  pine only; no broadleaf, shrub, mushroom, or tropical plant;
- wet bank: red alder, black cottonwood, or salmonberry;
- moist meadow/woodland: western redcedar, western hemlock, Sitka spruce,
  Pacific yew, bigleaf maple, Pacific dogwood, salal, salmonberry, or trailing
  blackberry;
- dry open ground: shore pine, Pacific madrone, Garry oak, low Oregon grape,
  red-flowering currant, oceanspray, or trailing blackberry;
- no plant may emerge from open water, exposed path paving, bridge masonry,
  railway, building floors, or other non-growing surfaces.

The Mermaid Roshan stained glass remains protected and unchanged. Any later
castle work must keep its image plane and full-depth aperture intact.

## Provenance and generation prompts

Species selection was checked against the King County Native Plant Guide, its
printable native-plant list, Seattle's Green Lake Vegetation Management Plan,
and Washington DNR forest guidance:

- https://green2.kingcounty.gov/gonative/Plant.aspx?Act=list
- https://green2.kingcounty.gov/gonative/Print.aspx?Act=plantlist
- https://www.seattle.gov/documents/Departments/ParksAndRecreation/PoliciesPlanning/Vegetation%20Management%20Plans/GreenLakeVMP.pdf
- https://www.dnr.wa.gov/programs-and-services/forest-resources/habitat-conservation/identifying-mature-and-old-forests

Tree reference inputs were `sky_lagoon_quality_2026-07-20.png` (primary) and
`sky_lagoon_tree_family_gen5_2026-07-20.png` (secondary silhouette reminder).
The accepted tree generation prompt was:

> Create a new flat asset-prototype sheet for the Sky Lagoon in exactly the
> same polished toy-diorama style, proportions, material simplicity, soft
> pastel palette, chunky readable forms, navy-purple outline accents, and
> child-friendly presentation as the FIRST reference image. Use the SECOND
> reference only as a loose reminder that tree silhouettes should differ;
> simplify substantially beyond it. This is an art-direction sheet for later
> low-poly Blender modeling, not a botanical painting. Make every tree
> intentionally easy to model: one strong trunk system, only 2–5 large crown
> masses, very few visible branches, no fine needles, no dense individual
> leaves, no intricate bark texture, no filigree, no photorealism. Rounded
> hand-painted toy geometry, broad cel-shaded planes, oversized signature
> features, clean silhouettes readable at phone size. Arrange exactly twelve
> isolated trees in a clean 4-column by 3-row grid, equal visual scale,
> generous spacing, no overlap, on the same deep navy studio background used
> by the FIRST reference. No words, labels, numbers, borders, people,
> buildings, or scenery. Keep the exact species order left-to-right,
> top-to-bottom: Coastal Douglas-fir, western redcedar, western hemlock, Sitka
> spruce; shore pine, Pacific yew, bigleaf maple, red alder; black cottonwood,
> Pacific madrone, Garry oak, Pacific dogwood. Use the unified Sky Lagoon
> palette: mint, aqua, sage, pale jade, lavender shadow, coral accent, warm
> cream and muted gold. Every asset must feel like it belongs beside the
> existing rounded castle, fountain, playground, train, alpine pines, and
> flowers. Maximum visual-design grade target 4.9/5; reject realism and
> micro-detail.

The first shrub generation used the quality-kit sheet plus the accepted tree
sheet, but its evergreen huckleberry was rejected as redundant with salal. The
initial replacement-and-variant generation used the quality-kit sheet as the
primary style anchor, that first shrub sheet as a rendering-language reference,
and the accepted tree sheet for planted-base and value hierarchy. Its prompt is
retained below as rejected iteration provenance:

- Image 1: `assets_src/concepts/sky_lagoon_quality_2026-07-20.png`
- Image 2: superseded historical
  `assets_src/concepts/sky_lagoon_pnw_shrub_prototypes_flat_2026-07-21.png`
- Image 3: `assets_src/concepts/sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png`

```text
Use case: stylized-concept.
Asset type: flat model-reference sheet for a mobile Godot storybook game's Sky Lagoon.

Create a NEW portrait-format shrub family sheet containing exactly twelve isolated shrubs: two visually distinct variants for each of six native Seattle/PNW shrub species. Use Image 1 as the primary non-negotiable Sky Lagoon style and palette anchor. Use Image 2 for the accepted shrub rendering language, but replace its evergreen huckleberry role with trailing blackberry and expand every remaining species into a real silhouette pair. Use Image 3 only for consistency of planted bases, rounded volume treatment, and value hierarchy.

This is flat art direction for later simple low-poly modeling, not botanical realism. Match the established polished rounded toy-diorama look: chunky hand-shaped forms, broad cel-shaded planes, matte pastel color blocking, gentle asymmetry, navy-purple edge accents, and clean child-readable silhouettes. Palette: mint, aqua, sage, deep jade, lavender, coral, warm cream, muted gold, and warm brown on a deep navy studio background.

Arrange the assets in an exact 2-column by 6-row gallery. Each row is one species pair, Variant A on the left and Variant B on the right. Equal visual scale, generous empty spacing, complete planted bases, no overlap. No words, letters, labels, numbers, borders, people, buildings, pots, scenery, watermark, or logo.

Exact row order and designs:

Row 1 — Salal:
A: low wide three-lobe deep-jade mound, cream bell cluster concentrated on the left, a few lavender-black berries.
B: asymmetrical crescent-shaped two-tier mound spilling to the right, open notch near center, cream bells concentrated on the right and fewer berries.
Both must read as salal, but footprints and negative spaces must differ clearly.

Row 2 — Low Oregon grape:
A: low radial starburst rosette with four large pointed aqua leaf masses, three upright muted-gold flower spikes and a few lavender berries.
B: offset stepped fan with three broad pointed leaf tiers rising diagonally, two leaning gold flower spikes, visible open wedge between tiers.
Do not create many individual leaves.

Row 3 — Red-flowering currant:
A: upright rounded three-mass shrub with a short forked trunk and five oversized hanging coral tassels.
B: broad arching V-shaped shrub with two separated crown masses, visible central gap, and three longer rose-coral tassels.
No twig network.

Row 4 — Oceanspray:
A: compact fountain of three pale-jade masses with five broad cream blossom plumes arcing outward.
B: windswept crescent with three stepped foliage masses and four solid cream blossom sprays swept to one side.
Treat each blossom spray as one simple chunky cluster, never dozens of tiny flowers.

Row 5 — Salmonberry:
A: broad low three-cloud mint mound with three oversized magenta five-petal flowers and four orange-coral berry clusters.
B: split arching two-wing shrub with an open central gap, two flowers at different heights and three large berry clusters.
Keep leaves abstract and chunky.

Row 6 — Native trailing blackberry (Rubus ursinus), replacing evergreen huckleberry:
A: low creeping crescent bramble with two thick curved canes, three large lobed leaf pads, two oversized white five-petal flowers, and four dark blackberry clusters.
B: compact arching bramble with a clear tunnel-like negative space, three chunky leaf masses, one cream flower, and five purple-black aggregate berry clusters.
No sharp thorns, no thin tangled vines, no leaf clutter.

For every pair, Variant B must change overall width/height ratio, foliage-mass placement, stem gesture, negative space, and accent placement. Mirroring, recoloring, or merely moving flowers does not count. All twelve must remain practical to model using two to four main foliage volumes, very few thick stems, and a handful of oversized emblem features. Reject photorealism, field-guide illustration, micro-detail, dense leaf anatomy, exposed twig webs, glossy plastic, primitive spheres, copied silhouettes, and any design that would be difficult to reproduce as a low-poly mobile mesh. Maximum visual-design grade target 4.9/5.
```

The owner rejected that first paired iteration because trailing and arching
silhouettes repeated outside blackberry. The accepted sheet is the next
image-edit revision. Image 1 was the superseded paired iteration, Image 2 was
`sky_lagoon_quality_2026-07-20.png`, and Image 3 was the accepted PNW tree
sheet. The exact accepted revision prompt was:

```text
Use case: stylized-concept revision.
Asset type: revised flat model-reference sheet for a mobile Godot storybook game's Sky Lagoon.

Revise Image 1 into a complete portrait shrub family sheet with the same exact 2-column by 6-row layout, deep navy studio background, polished rounded toy-diorama rendering, palette, scale, spacing, and planted bases. Image 2 is the non-negotiable Sky Lagoon style and color-quality anchor. Image 3 is only a reference for broad rounded volume treatment and low-poly modelability.

The current sheet repeats a trailing crescent or tunnel-like arch across too many shrubs. Correct that. TRAILING, CREEPING, CASCADING, CRESCENT, TUNNEL, AND CANE-ARCH SILHOUETTES ARE RESERVED EXCLUSIVELY FOR THE NATIVE TRAILING BLACKBERRY IN ROW 6. Rows 1–5 must have no tunnel opening, no bridge-shaped central gap, no long horizontal trailing limb, and no low creeping crescent.

Preserve the species order exactly. Preserve all five left-column Variant A designs and both row-6 trailing blackberry designs as closely as possible. Replace only the right-column Variant B designs in rows 1–5 with the following clearly different, non-trailing architectures:

Row 1 Salal B: a compact upright stepped mound, taller than A, with four staggered deep-jade foliage blocks rising toward the back-left like a soft terraced hill. Solid planted center, no arch or central hole. Cream bell cluster high on the right; a few lavender-black berries low on the left.

Row 2 Low Oregon grape B: a strongly vertical asymmetric spear-fan, with three large pointed leaf tiers stacked upward and leaning slightly left, plus two short muted-gold flower spikes at unequal heights. Solid base and a narrow triangular profile. No horizontal sweep, arch, or gap.

Row 3 Red-flowering currant B: a narrow upright candelabra form with three short thick stems and three separated rounded crown clusters at different heights. Four large rose-coral tassels hang close to the vertical masses. No spanning branch, split arch, or bridge shape.

Row 4 Oceanspray B: a broad solid tiered wedge, like a rounded triangular hedge with three overlapping pale-jade blocks ascending to one side. Four chunky cream blossom plumes point upward at staggered heights. No windswept crescent, long outward sweep, or open center.

Row 5 Salmonberry B: a tall asymmetric clustered tower with one large lower mint mass and two smaller upper masses stepping diagonally. Two oversized magenta flowers and three orange-coral berry clusters occupy different heights. Solid central silhouette, no paired wings, arch, tunnel, or trailing stem.

Row 6 Native trailing blackberry A and B: keep the low creeping thick-cane bramble and the compact cane arch. Blackberry is the ONLY row allowed to trail, creep, make a crescent, or form a tunnel-like negative space.

Every pair must still differ in width/height ratio, foliage-mass placement, stem gesture, negative space, and accent placement. The new B designs must also differ from one another: terraced mound, spear-fan, candelabra, tiered wedge, clustered tower. Do not replace one repeated pattern with another. Keep all plants practical to model with two to four primary foliage volumes, very few thick stems, and oversized emblem features.

No words, letters, labels, numbers, borders, people, buildings, pots, scenery, watermark, or logo. Reject photorealism, field-guide detail, micro-leaves, thin twig webs, glossy plastic, primitive-sphere piles, copied silhouettes, and any non-blackberry trailing or arching growth. Maximum computer grade target 4.9/5.
```

Repository copies are normalized to a 1024px longest side. The untouched raw
generation masters remain in the local image-generation provenance store; the
named cards are deterministically reproduced by
`tools/slice_sky_lagoon_pnw_prototypes.py`.
