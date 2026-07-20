# Sky Lagoon style-cohesion audit - 2026-07-19

## Scope

This pass grades every distinct item family visible in the 17-view Mobile-render
review set at `assets_src/sky_lagoon/runtime_candidate_046fbcf/`. The score is
not a technical-validity score and is not an isolated beauty score. It measures
how closely an item matches the strongest items in the same frame: rounded
storybook-toy geometry, navy-purple contour structure, broad pastel color
blocks, aqua/lavender shadows, readable child-scale silhouettes, and motifs
that support an actual gameplay role.

The protected book image and protected character/friend art are graded only to
record that they remain authoritative. They are not regeneration candidates.

## Grade anchors

- **5/5:** authoritative source art or owner-approved final art; no automatic
  award from a probe or an agent review.
- **4/5:** coherent with adjacent accepted families at gameplay distance; clear
  silhouette, grounded construction, restrained detail, and correct function.
- **3/5:** broadly compatible palette but visibly generic, thin, assembled, or
  under-authored beside neighboring assets.
- **2/5:** a different modeling dialect, weak anatomy/construction, or a
  placeholder that dominates the frame.
- **1/5:** unmistakable primitive placeholder or major functional silhouette
  failure.
- **0/5:** missing, broken, or unusable.

## Result

Twenty-nine visible families were graded. Two protected families remain 5/5,
thirteen environment families pass at 4/5, and fourteen families score below
4/5. All fourteen low families now have either a new reference sheet in
`assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/` or an existing
accepted train reference in `gen2/generated/`. None of the references is being
misrepresented as an integrated runtime replacement.

| Visible family | Score | Consistency finding | Required direction |
|---|---:|---|---|
| Protected story-memory image | 5/5 | Authoritative book art | Preserve bytes and presentation; never regenerate |
| Protected character/friend art | 5/5 | Authoritative until its separately approved 3D migration | Excluded from this pass |
| Meadow terrain surface | 4/5 | Broad graphic color masses support the toy world | Retain; review only when terrain materials change |
| Rounded meadow trees | 4/5 | Complete rooted habit and readable canopy masses | Retain |
| Baby rosette | 4/5 | Complete baby plant; directly satisfies the ground-plant rule | Retain |
| Developed meadow shrub | 4/5 | Strong complete silhouette and color grouping | Retain |
| Flower clusters | 4/5 | Complete multi-stem plant family, not isolated leaves | Retain |
| Mushroom family | 4/5 | Grounded cluster and child-readable scale | Retain outside snow biome |
| Pond reeds | 4/5 | Rooted multi-stem wetland habit | Retain at water edges only |
| Snowbanks | 4/5 | Low modeled transition breaks the shader boundary | Retain |
| Cloud family | 4/5 | Softer atmospheric role justifies reduced outlines | Retain high and off the castle sightline |
| Playground equipment | 4/5 | Strong shared contour language and immediate function | Retain |
| Rainbow race arch | 4/5 | Clear functional gate and restrained cloud feet | Retain |
| Dream stars | 4/5 | Large objective silhouette and consistent color hierarchy | Retain |
| Fairy Pond water | 4/5 | Distinct readable destination with coherent cool palette | Retain |
| Pearl-cobble path | 3/5 | Flat repeated slabs do not match authored props | Replace visual shell with the path/bridge kit direction |
| Castle bridge | 3/5 | Functional but assembled and weakly related to the castle | Replace visual shell; preserve collision and route width |
| Riverbank stones | 3/5 | Better than a bare shader edge but too small and generic | Replace with varied 5-8 stone clusters |
| Protected-memory frame | 3/5 | Thin surround loses against adjacent outlined props | Replace surround only; never touch the image plane |
| Story lanterns | 3/5 | Thin modern posts read as another asset family | Replace with stout shell-and-pearl lanterns |
| Butterfly World gate | 2/5 | Open loops function, but do not resolve as one complete butterfly | Replace with a complete body, head, antennae, four wings, and open passage |
| Pearl Castle exterior | 3/5 | Palette works, but stacked primitives and crenellation rows dominate | Replace exterior visual shell; preserve door, glass, moat, and solids contracts |
| Train station | 3/5 | Shell roof helps, but platform and shelter remain thin | Rebuild from accepted platform and shelter sheets |
| Train locomotive | 1/5 | Primitive toy blocks fail next to the playground and castle | Replace from the accepted locomotive identity sheet |
| Tender, coach, gondola, caboose | 2/5 | Function exists but family identity is inconsistent and under-modeled | Replace with one shared wheel/coupler/chassis system |
| Courtyard rails and ties | 2/5 | Navy rails are readable but the procedural ribbon is visually crude | Restyle from accepted straight/curve references while preserving the route |
| Alpine chalets | 2/5 | Box/roof construction and mixed accents read as a separate prototype | Replace with the three-chalet family |
| Alpine mountain and cave | 2/5 | Stacked box crags, black cap, and cave shell do not read as one landform | Replace with rounded faceted modules and terrain-aware snow ledges |
| Alpine pines and decorated tree | 3/5 | Complete plants, but current silhouettes and decoration drift from the new biome | Rebuild as complete multi-tier snowy pines; no loose bulbs or isolated leaves |

## Binding plant rule

A single detached leaf must never represent a complete plant emerging from
terrain. A ground plant needs a believable root or attachment point and a
complete growth habit: baby rosette, multi-leaf clump, reed bed, shrub,
flowering plant, or mature tree. In snow, only habitat-appropriate complete
plants such as multi-tier pines are allowed. Tropical plants and mushrooms are
not valid Alpine dressing.

## Main repeating failures

1. **Assembly language drift.** Procedural boxes, cylinders, and thin posts sit
   beside rounded authored props without a common bevel, contour, or plinth.
2. **Thinness at phone scale.** Wire gates, lantern posts, station posts, and
   narrow trim disappear or flicker at gameplay distance.
3. **Motif substitution for construction.** Adding a shell or rainbow cannot
   rescue an object whose silhouette, anatomy, grounding, or gameplay opening
   is unresolved.
4. **Incorrect hierarchy.** The least-authored objects - train, castle shell,
   and Alpine mountain - occupy the largest and most frequently viewed areas.
5. **Biome leakage.** Plant acceptability was checked by asset name rather than
   by complete habit plus the surface/ecosystem where it is placed.
6. **Technical pass treated as visual pass.** Probe success proves loading and
   gameplay contracts, not a 4/5 or 5/5 art result.

## Evidence and limitation

The source evidence is the 17-view candidate capture set and its contact sheet.
The Opera courtyard gate and any later additions that are absent from those
frames remain **ungraded**, not implicitly passed. Claude should add targeted
captures before accepting those roles.
