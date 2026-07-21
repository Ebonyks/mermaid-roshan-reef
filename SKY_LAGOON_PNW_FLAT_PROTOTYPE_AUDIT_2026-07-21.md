# Sky Lagoon PNW flat-prototype audit — 2026-07-21

## Decision

The realistic PNW botanical sheets and the procedural Blender replacements are
rejected. They do not belong to the established Sky Lagoon family. The accepted
art-direction source is now the pair of flat prototype sheets in this branch:

- `assets_src/concepts/sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png`
- `assets_src/concepts/sky_lagoon_pnw_shrub_prototypes_flat_2026-07-21.png`

The eighteen named cards under `assets_src/concepts/sky_lagoon_pnw_flat/` are
cropped references for later modeling. They are not runtime textures and no
shipped GLB or scene placement changes in this pass. The current accepted GEN2
plus GEN5 runtime tree family therefore remains the safe fallback.

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
| Salal | 4.9 | 4.8 | 4.8 | 4.8 |
| Low Oregon grape | 4.9 | 4.9 | 4.9 | 4.9 |
| Red-flowering currant | 4.9 | 4.8 | 4.8 | 4.8 |
| Oceanspray | 4.8 | 4.8 | 4.7 | 4.8 |
| Salmonberry | 4.9 | 4.9 | 4.9 | 4.9 |
| Evergreen huckleberry | 4.9 | 4.8 | 4.8 | 4.8 |

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
  Pacific yew, bigleaf maple, Pacific dogwood, salal, or evergreen huckleberry;
- dry open ground: shore pine, Pacific madrone, Garry oak, low Oregon grape,
  red-flowering currant, or oceanspray;
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

The shrub generation used the quality-kit sheet plus the accepted tree sheet:

> Create the matching flat asset-prototype sheet for six native Seattle/PNW
> shrubs. Match the references exactly: polished rounded Sky Lagoon
> toy-diorama assets, chunky hand-painted forms, broad cel-shaded planes, soft
> mint/aqua/sage/lavender/coral/cream palette, subtle navy-purple edge accents,
> child-readable silhouette, deep navy studio background. This is for later
> easy low-poly Blender translation. Absolutely no botanical realism, no
> individual-leaf clutter, no thin twig network, no fine textures, no
> filigree. Each shrub must use only 2–4 large foliage masses, a few thick
> stems at most, and oversized iconic flowers, berries, or leaf emblems.
> Arrange exactly six isolated shrubs in a clean 3-column by 2-row grid, equal
> visual scale, generous spacing, no overlaps. Exact order: salal, low Oregon
> grape, red-flowering currant; oceanspray, salmonberry, evergreen huckleberry.
> They must look like companion pieces to the corrected twelve-tree sheet and
> to the existing Sky Lagoon fountain, bench, flowers, train, and playground,
> not like field-guide illustrations. Maximum visual-design grade target
> 4.9/5.

Repository copies are normalized to a 1024px longest side. The untouched raw
generation masters remain in the local image-generation provenance store; the
named cards are deterministically reproduced by
`tools/slice_sky_lagoon_pnw_prototypes.py`.
