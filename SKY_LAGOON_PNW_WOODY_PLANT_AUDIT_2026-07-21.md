# Sky Lagoon PNW woody-plant audit — 2026-07-21

## Outcome

The rejected Sky Lagoon GEN5 tree family and generic meadow shrub were removed.
Their runtime roles, GLBs, Blender source, concept sheet, QA renders, and tree
builder no longer ship. They are replaced by twelve new Seattle-area tree
species and six new native shrubs, each with an independent branch graph,
diagnostic botanical cues, and habitat metadata.

The automatic score ceiling is 4.9/5. Any asset below 4.5 is rejected rather
than averaged into the family. All eighteen final isolated assets pass at
4.6–4.8 across fixed 0°, 45°, and 135° Eevee/toon reviews. Runtime Mobile
scores are recorded only after exact-branch CI capture review.

## Species and ecological basis

Species selection was checked against local-government and Washington sources:

- [King County Native Plant Guide](https://green2.kingcounty.gov/gonative/Plant.aspx?Act=list)
  supplies local species, sun, and moisture ranges.
- [King County printable native plant list](https://green2.kingcounty.gov/gonative/Print.aspx?Act=plantlist)
  confirms the tree and shrub roster.
- [Seattle Green Lake Vegetation Management Plan](https://www.seattle.gov/documents/Departments/ParksAndRecreation/PoliciesPlanning/Vegetation%20Management%20Plans/GreenLakeVMP.pdf)
  provides a Seattle-specific native-tree context.
- [Washington DNR mature and old forests](https://www.dnr.wa.gov/programs-and-services/forest-resources/habitat-conservation/identifying-mature-and-old-forests)
  supports the dominant west-side conifer context.
- [West Tiger Mountain NRCA](https://dnr.wa.gov/natural-areas/natural-resources-conservation-areas/west-tiger-mountain-natural-resources-conservation-area)
  provides nearby Puget Lowland forest context.

No web photograph was copied, traced, embedded, or used as a runtime texture.
King County photo pages state that their imagery requires permission, so the
workflow used textual species information and newly generated concept art only.

The tree roster is coastal Douglas-fir, western redcedar, western hemlock,
Sitka spruce, shore pine, Pacific yew, bigleaf maple, red alder, black
cottonwood, Pacific madrone, Garry oak, and Pacific dogwood. The shrub roster is
salal, low Oregon grape, red-flowering currant, oceanspray, salmonberry, and
evergreen huckleberry.

## Placement continuity

`scripts/arena/sky_lagoon.gd` now applies the following ecosystem rules before
placing any tree or shrub:

- river channels, the pond disc, castle/moat, maintained route, playground,
  Alpine houses, train corridor, mountain solid, and island rim are forbidden;
- red alder, black cottonwood, and salmonberry must be within 42 world units of
  a water edge;
- redcedar, hemlock, Sitka spruce, yew, bigleaf maple, dogwood, salal, and
  evergreen huckleberry must be within 82 units of a water edge;
- shore pine, madrone, Garry oak, Oregon grape, red-flowering currant, and
  oceanspray must remain at least 20 units from water;
- only Douglas-fir, redcedar, hemlock, Sitka spruce, and shore pine may occupy
  painted snow;
- broadleaf trees, tropical palms, isolated leaf meshes, flowers, shrubs, and
  mushrooms are rejected on snow; mushrooms also remain in the moister zone.

The pond’s prior non-native willow pair was replaced by red alder and black
cottonwood on dry bank positions outside the water disc. The Alpine pines now
use the new Douglas-fir and Sitka spruce models.

## Reject/regenerate history

### Pass 1 — rejected

The first deterministic export established eighteen unique branch graphs, but
the broadleaf leaves were too small and frequently edge-on. Maple, alder,
cottonwood, madrone, oak, and dogwood read as unfinished trunks at gameplay
distance. Shrubs were botanically distinct but too skeletal. Douglas-fir,
redcedar, Sitka spruce, Oregon grape, and oceanspray also exceeded the intended
triangle budget before scene multiplication.

### Pass 2 — rejected for refinement

Species-specific crown masses fixed the missing-canopy read: umbrella maple,
narrow cottonwood flame, compact glossy madrone, wide open Garry oak, tiered
dogwood, and separate shrub habits. The pass was still held because broadleaf
crown surfaces relied too heavily on smooth low-poly masses.

### Pass 3 — accepted for runtime audit

Large signature palmate, rounded, triangular, oval, and lobed leaves were added
to the outer crown silhouettes. Conifer pad subdivisions were reduced where
they did not change the outline. Dogwood and salmonberry material sets were
deduplicated. Fixed 0°, 45°, and 135° turntables were regenerated for every
asset, followed by uncropped family contact sheets.

## Scoring rubric

The score is the sum of silhouette/branch architecture (1.5), botanical cue
(1.2), project style and palette (1.0), multi-angle robustness (0.7), and Mobile
geometry/metadata discipline (0.5), capped at 4.9.

| Species | Isolated score | Primary acceptance cue |
|---|---:|---|
| coastal Douglas-fir | 4.7 | tall irregular cone, exposed furrowed trunk, separated whorls and cones |
| western redcedar | 4.8 | buttressed base, broad layered skirt, hanging scale-spray curtains and bent tip |
| western hemlock | 4.7 | narrow feathered cone, pronounced bowed leader and dangling bough ends |
| Sitka spruce | 4.7 | dense broad prickly skirt and stiff radial architecture |
| shore pine | 4.6 | crooked wind-pruned trunk, open negative space, terminal needle clouds and cones |
| Pacific yew | 4.6 | twisted multi-stem understory form, flat sprays, dark foliage and red arils |
| bigleaf maple | 4.7 | massive spreading fork, wide umbrella crown, oversized palmate silhouette leaves |
| red alder | 4.6 | pale straight trunk, airy high oval crown, rounded leaves, catkins and cones |
| black cottonwood | 4.6 | tall narrow rising crown and triangular diagnostic leaves |
| Pacific madrone | 4.8 | peeling coral trunk, sinuous branching, compact evergreen masses and berries |
| Garry oak | 4.7 | low heavy fork, wide open crown, lobed leaves and acorns |
| Pacific dogwood | 4.8 | horizontal layered crown, four-bracted white flowers and red fruit |
| salal | 4.6 | low arching evergreen habit, glossy leaves, bells and dark berries |
| low Oregon grape | 4.7 | radial spiny compound leaves, upright gold racemes and blue fruit |
| red-flowering currant | 4.8 | airy upright habit and multiple hanging coral-pink flower chains |
| oceanspray | 4.8 | fountain canes and cascading cream plumes |
| salmonberry | 4.7 | arching canes, palmate leaves, magenta flowers and salmon fruit clusters |
| evergreen huckleberry | 4.7 | dense fine-stem habit, small evergreen leaves, bells and blue-black berries |

Full geometry, material, source-height, habitat, and final runtime scores live
in `audit/sky_lagoon_pnw_woody_plant_ledger_2026-07-21.csv`.

## Deterministic evidence

- Builder: `tools/build_sky_lagoon_pnw_woody_plants.py`
- Editable source: `assets_src/blender/sky_lagoon_pnw_woody_plants.blend`
- GLBs: `assets/sky_lagoon/lagoon_kit/lagoon_tree_*.glb` and
  `lagoon_shrub_*.glb`
- Isolated views and contacts:
  `assets_src/blender/qa_sky_lagoon_pnw_woody_plants/`
- Structural gate: `tools/audit_sky_lagoon_kit.py`
- Mobile scene review: `scripts/probe_sky_lagoon_art.gd`

Structural audit result before CI: 18/18 woody assets passed; no textures;
2,430–7,486 triangles per tree, 2,588–6,172 per shrub, at most eight materials;
all five semantic extras present. Mermaid stained-glass SHA-256 remains
`94952B4C13455F7A3966DB32D7FC49F652DD5B933325AD9C3D37DE9B93C3D4A0`.

## Image-generation provenance and prompts

The generated images are style and morphology references only. No pixel from
them is used by a runtime material.

Tree reference output:
`assets_src/concepts/sky_lagoon_pnw_tree_species_2026-07-21.png`

```text
Create a high-end 3D botanical concept sheet for a pastel storybook game, arranged as exactly twelve clearly separated full-tree specimens in a 4 by 3 grid on a clean pale aqua studio background. No text, no labels, no people, no buildings, no ground clutter. Each specimen is an isolated orthographic three-quarter view and must have a radically different, species-readable silhouette. Ordered left-to-right, top-to-bottom: (1) coastal Douglas-fir, very tall irregular cone, sparse lower limbs and thick deeply furrowed trunk; (2) western redcedar, broad buttressed base, layered drooping curtain-like scale sprays and bent crown tip; (3) western hemlock, narrow feathered cone with unmistakably bowed drooping leader and dangling branch tips; (4) Sitka spruce, sturdy broad spiky skirt, stiff radial branches and strong pointed top; (5) shore pine, crooked windswept open crown with sparse paired-needle tufts and small cones; (6) Pacific yew, small twisted multi-stem understory tree, flat dark sprays and a few red arils; (7) bigleaf maple, huge spreading limbs, broad umbrella crown and unmistakable oversized five-lobed leaf clusters with moss accents; (8) red alder, pale smooth straight trunk, high airy oval crown, rounded serrated leaf clusters, catkins and tiny cones; (9) black cottonwood, tall columnar crown with rising branches and triangular fluttering leaf clusters; (10) Pacific madrone, sculptural peeling coral-cinnamon trunk, sinuous branches, compact glossy evergreen crown and red berries; (11) Garry oak, wide rugged open crown with heavy crooked limbs, lobed foliage and visible acorns; (12) Pacific dogwood, small layered horizontal crown with large four-bracted white blossoms and red fruit. Art direction: premium Wind-Waker-inspired cel-shaded toy diorama without copying any existing IP asset, rounded low-poly forms, navy-plum edge language, aqua/lavender shadows, cohesive mint-jade-teal foliage with species accents, child-readable at gameplay distance. Strong trunk-to-crown transitions, visible branch architecture, convincing root flares, no generic sphere crowns, no repeated templates, no flat cardboard cutouts, no photorealism.
```

Shrub reference output:
`assets_src/concepts/sky_lagoon_pnw_shrub_species_2026-07-21.png`

```text
Create a high-end 3D botanical concept sheet for a pastel storybook game, arranged as exactly six clearly separated full-shrub specimens in a 3 by 2 grid on a clean pale lavender studio background. No text, no labels, no people, no buildings, no ground clutter. Each specimen is an isolated orthographic three-quarter view and must have a radically different, species-readable silhouette. Ordered left-to-right, top-to-bottom: (1) salal, low arching evergreen thicket with large glossy oval leaves, bell-like pale blossoms and purple-black berries; (2) low Oregon grape, compact radial evergreen rosette-shrub with unmistakable spiny compound leaves, upright yellow flower racemes and dusty blue berries; (3) red-flowering currant, airy upright branching shrub with many dangling saturated pink flower clusters; (4) oceanspray, broad fountain-shaped woody shrub covered in creamy cascading plume sprays; (5) salmonberry, loose arching cane shrub with bright magenta five-petaled flowers and salmon-orange raspberry-like fruit; (6) evergreen huckleberry, dense upright fine-twigged evergreen shrub with small dark glossy leaves, pink-white bells and blue-black berries. Art direction: premium Wind-Waker-inspired cel-shaded toy diorama without copying any existing IP asset, rounded low-poly forms, navy-plum edge language, aqua/lavender shadows, cohesive mint-jade-teal foliage with coral, butter-gold and berry accents, child-readable at gameplay distance. Visible branch architecture and grounded bases, no generic hedge blobs, no repeated templates, no flat cardboard cutouts, no photorealism.
```
