# Sky Lagoon Blender continuation for Claude — 2026-07-20

## 2026-07-21 PNW flat-prototype workorder

The owner rejected the realistic botanical sheets and every procedural PNW
Blender attempt. Do **not** use branch `codex/sky-lagoon-pnw-trees`, its builder,
or its eighteen GLBs as a base. They are preserved only as rejected history.

The art-direction source of truth for the next modeling pass is flat image art:

- `assets_src/concepts/sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png`
- `assets_src/concepts/sky_lagoon_pnw_shrub_variants_flat_2026-07-21.png`
- the twenty-four named crop cards under
  `assets_src/concepts/sky_lagoon_pnw_flat/`
- `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md`

The required future roster is twelve trees (Coastal Douglas-fir, western
redcedar, western hemlock, Sitka spruce, shore pine, Pacific yew, bigleaf
maple, red alder, black cottonwood, Pacific madrone, Garry oak, and Pacific
dogwood) plus six shrubs (salal, low Oregon grape, red-flowering currant,
oceanspray, salmonberry, and native trailing blackberry). Build both approved
A/B forms for every shrub, for twelve shrub meshes total. Each B form changes
the footprint, mass layout, negative space, and stem gesture; do not produce a
mirror, palette swap, or accent-only variation.

Trailing, creeping, crescent, bridge, cane-arch, and tunnel-like silhouettes
belong to trailing blackberry only. The other B forms are deliberately salal
terrace, Oregon-grape spear-fan, currant candelabra, oceanspray tiered wedge,
and salmonberry clustered tower. Do not reintroduce the rejected repeated-arch
pattern while translating them.

The old `sky_lagoon_pnw_shrub_prototypes_flat_2026-07-21.png`, all legacy
no-suffix shrub crop cards, and evergreen huckleberry are superseded and must
not be modeled or restored.

These references are approved prototypes, not authorization to replace the
current runtime family. Keep GEN2 plus GEN5 wired as the fallback until every
new model independently passes. Model the silhouette and primary volumes, not
the illustration's surface grooves: two to five crown masses, very few thick
branches, broad cel planes, and one oversized species cue. Do not create leaf
cloud algorithms, twig networks, individual needle/leaf clutter, dense bark,
or literal geometry for every painted scallop, berry, or flower.

Trees 7, 9, and 11 were specifically revised because their first prototypes
used oversized leaf badges. Do not restore those badges or model separate leaf
emblems: the crown masses already represent leaves. Tree 7 bigleaf maple uses
only sparse hanging paired V-shaped double samaras; tree 9 black cottonwood
uses sparse hanging coral catkin/seed ornaments; tree 11 Garry oak uses sparse
golden acorns. Trees 8 red alder and 12 Pacific dogwood remain the successful
ornament grammar anchors. Extra tree details must be genuine reproductive cues
such as samaras, catkins, seed tufts, acorns, pinecones, berries, or flowers.

Match the prototype palette and value hierarchy. Reject any mesh below 4.5/5
at 0, 45, or 135 degrees, or below 4.5 in the Godot Mobile scene. The upper
computer grade remains 4.9. Species realism never overrides the rounded
storybook toy language or phone-scale readability.

Use these habitat constraints during the later scene pass:

- snow: Douglas-fir, western redcedar, western hemlock, Sitka spruce, or shore
  pine only;
- wet bank: red alder, black cottonwood, or salmonberry;
- moist ground: western redcedar, western hemlock, Sitka spruce, Pacific yew,
  bigleaf maple, Pacific dogwood, salal, salmonberry, or trailing blackberry;
- dry ground: shore pine, Pacific madrone, Garry oak, low Oregon grape,
  red-flowering currant, oceanspray, or trailing blackberry;
- never place a broadleaf, shrub, mushroom, or tropical plant in snow, and
  never grow foliage from open water, path paving, bridge masonry, track, or
  building floors.

The Mermaid Roshan stained glass remains protected. Do not alter its image,
material, plane, opening, or visibility while changing vegetation.

## Current production baseline

Continue from the editable Blender sources in this branch; do not reconstruct
the accepted runtime family from the rejected procedural tree files.

- `assets_src/blender/sky_lagoon_quality_kit.blend` owns the non-tree Lagoon
  kit and three cloud exports.
- `assets_src/blender/sky_lagoon_tree_gen5.blend` owns all eight accepted
  extensions. The GEN3 trial/extensions sources and the removed GEN4 production
  files are rejected iterations and must not be re-exported over GEN5.
- The four shipped GEN2 anchors remain untouched:
  `tree_pineroundf.glb`, `tree_fall.glb`, `tree_fall2.glb`, and
  `tree_fat.glb`.
- Fixed 0/45/135-degree tree reviews live in
  `assets_src/blender/qa_sky_lagoon_tree_gen5/`.

The accepted runtime roster is exactly twelve tree designs: the four original anchors
plus ancient oak, dancing birch, umbrella, blossom cloud, windswept,
twin-heart, weeping willow, and celebration snow pine. The old
`lagoon_tree_meadow_*`, `coral_*`, `willow_*`, `evergreen`, and `alpine_*`
experiments are rejected and must not be wired or promoted.

Targeted-revision run `29816404035` is the accepted 51-view Mobile evidence set. The
accepted runtime scores are 4.6–4.8/5: ancient oak 4.7, dancing birch 4.7,
umbrella 4.7, blossom cloud 4.8, windswept 4.8, twin-heart 4.7, weeping
willow 4.8, and celebration snow pine 4.7. Do not overwrite these with an
older generation or accept a future refinement below the same scene score.

The later-merged Ember Fortress gateway is temporarily code-native in
`scripts/arena/sky_lagoon.gd`. Its accepted local placement is `(72, -150)`,
diagonally beyond the far rainbow gate: the complete 6.5-unit prop radius has
7.5 units of dry-bank clearance from the moat, its centre is 28.26 units
inside the grand-tour railway centreline, and it is 35.78 units from the race
gate. When producing its Blender version, preserve the vertical plum/coral
ring, butter-gold inner lip, three-lobe flame crest, lavender/aqua planted
stones, no floating text, no OmniLight, and the semantic role
`lagoon_ember_gateway`. Do not restore the rejected black/orange horizontal
torus, move it back into the train corridor, or place it inside the moat.

## Continuation contract

Any future Blender refinement must preserve a score of at least 4.5/5 in all
three isolated views and in the Godot Mobile scene audit. Use the original four
trees as the quality floor. Preserve genuinely different trunk graphs, crown
silhouettes, negative spaces, habitat reads, and height/width ratios; a palette
swap is not a new tree design.

GEN5 is intentionally hybrid: new tapered trunk/branch/root graphs provide the
structural variation, while independently posed and Mobile-decimated GEN2 crown
fragments preserve the approved sculpted cut planes and painted surface rhythm.
Do not revert to whole-tree warps or simple procedural blobs. The celebration
tree uses the approved Northern pine sculpt with surface-positioned ornaments.

Keep these placement rules intact:

- temperate broadleaves, mushrooms, flowers, and shrubs stay on dry meadow;
- the weeping willow stays at the pond edge;
- only the original rounded pine and celebration snow pine enter Alpine snow;
- no tropical palm returns to Sky Lagoon;
- all placements continue to clear paths, water ribbons, the castle/moat,
  playground, train corridor, and island rim.

The Mermaid Roshan stained glass at
`assets/book/hall/glass_mermaid.png` is protected and must remain a separate,
unchanged image plane. The castle source keeps a full-depth aperture around it.

## Deterministic rebuild and review

Run with Blender 4.4.3:

```text
blender --background --python tools/build_sky_lagoon_quality_kit.py
blender --background --python tools/build_sky_lagoon_tree_gen5.py
blender --background --python tools/render_glb_turntable_batch.py -- assets/sky_lagoon/lagoon_kit/lagoon_tree_ancient_oak.glb assets_src/blender/qa_sky_lagoon_tree_gen5 lagoon_tree_ancient_oak
```

Append additional `GLB OUT_DIR STEM` triples to the last command for every
changed tree; the batch renderer pays the Eevee startup cost only once.

After any accepted edit, update `ASSET_LICENSES.md`, the Sky Lagoon audit and
ledger, rerun parser/inference gates, and require green import/probes plus all
52 fixed scene captures before proposing integration into `dev`.
