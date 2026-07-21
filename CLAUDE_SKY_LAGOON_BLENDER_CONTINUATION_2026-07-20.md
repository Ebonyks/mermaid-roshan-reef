# Sky Lagoon Blender continuation for Claude — 2026-07-20

## Current production baseline

Continue from the editable Blender sources in this branch; do not reconstruct
the accepted runtime family from the rejected procedural tree files.

- `assets_src/blender/sky_lagoon_quality_kit.blend` owns the non-tree Lagoon
  kit and three cloud exports.
- `assets_src/blender/sky_lagoon_tree_gen4.blend` owns all eight accepted
  extensions. The GEN3 trial/extensions `.blend` files are rejected iteration
  evidence only and must not be re-exported over GEN4.
- The four shipped GEN2 anchors remain untouched:
  `tree_pineroundf.glb`, `tree_fall.glb`, `tree_fall2.glb`, and
  `tree_fat.glb`.
- Fixed 0/45/135-degree tree reviews live in
  `assets_src/blender/qa_sky_lagoon_tree_gen4/`.

The runtime roster is exactly twelve tree designs: the four original anchors
plus ancient oak, dancing birch, umbrella, blossom cloud, windswept,
twin-heart, weeping willow, and celebration snow pine. The old
`lagoon_tree_meadow_*`, `coral_*`, `willow_*`, `evergreen`, and `alpine_*`
experiments are rejected and must not be wired or promoted.

## Continuation contract

Any future Blender refinement must preserve a score of at least 4.5/5 in all
three isolated views and in the Godot Mobile scene audit. Use the original four
trees as the quality floor. Preserve genuinely different trunk graphs, crown
silhouettes, negative spaces, habitat reads, and height/width ratios; a palette
swap is not a new tree design.

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
blender --background --python tools/build_sky_lagoon_tree_gen4.py
blender --background --python tools/render_glb_turntable.py -- assets/sky_lagoon/lagoon_kit/lagoon_tree_ancient_oak.glb assets_src/blender/qa_sky_lagoon_tree_gen4 lagoon_tree_ancient_oak
```

Repeat the last command for each changed tree GLB and role stem.

After any accepted edit, update `ASSET_LICENSES.md`, the Sky Lagoon audit and
ledger, rerun parser/inference gates, and require green import/probes plus all
51 fixed scene captures before proposing integration into `dev`.
