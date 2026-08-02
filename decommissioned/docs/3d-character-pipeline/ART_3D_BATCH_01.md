# 3D Replacement Batch 01

_Built: 2026-07-14 with Blender 4.4.3_

This is the first production mesh pass for runtime art scored 2/5 or lower.
It deliberately excludes book art, legacy character models, family cutouts,
and child-owned stuffed animals. Those protected families were not opened,
edited, modeled, or replaced.

## Production assets

| Asset | Runtime role | Triangles | Mesh nodes | GLB size | Animation | Provisional score |
|---|---|---:|---:|---:|---|---:|
| `assets/props/gen2/anemone_story.glb` | garden crowns, cavern lights, reef meadow scatter | 1,056 | 1 | 0.05 MB | static | 4/5 |
| `assets/props/gen2/urchin_story.glb` | reef meadow scatter and fairy-stage hazards | 816 | 1 | 0.04 MB | static | 4/5 |
| `assets/props/gen2/butterfly_story.glb` | Galaxy and Butterfly World ambient butterflies | 2,040 | 3 | 0.05 MB | separate left/right wing pivots | 4/5 |
| `assets/props/gen2/giant_fish_story.glb` | distant main-reef whale | 3,028 | 2 | 0.09 MB | linked tail and horizontal flukes | 4/5 |
| `assets/vehicles/monstertruck_story.glb` | selectable kart monster truck | 5,292 | 1 | 0.18 MB | static vehicle body | 4/5 |

All five GLBs use embedded matte palette materials and contain no raster image
payload. Static parts were joined down to eight mesh nodes across the complete
batch. Anemone and urchin meshes were also decimated for MultiMesh use.
The butterfly has a complete body, antennae, paired forewings, and paired
hindwings. The whale has paired pectoral fins, one dorsal fin, a caudal stock,
and two horizontal flukes. No non-character marine prop gained a face.

## Runtime routing

- `scripts/main.gd` prefers the new anemone and urchin in hero placements and
  Mobile-conscious meadow MultiMeshes. Scatter counts are 180 anemones and 100
  urchins; legacy procedural meshes remain missing-file fallbacks.
- `scripts/galaxy.gd` and `scripts/kart.gd` prefer the complete butterfly mesh.
  Runtime flap motion rotates the two wing pivots rather than stretching the
  whole insect. Existing cards and old GLBs remain fallback tiers.
- `scripts/main.gd` prefers the animated giant fish for the distant whale role.
- `scripts/kart.gd` prefers the new monster truck while preserving the old rover
  as a missing-file fallback and preserving the existing gameplay dimensions,
  paint system, collision contract, and yaw correction.

## Reproducibility and QA

- Source: `assets_src/blender/low_score_batch_01.blend`
- Builder: `tools/build_low_score_batch_01.py`
- Renders: `assets_src/blender/qa_low_score_batch_01/*.png`
- Structural validation: 5 valid GLBs, 12,232 total triangles, 3 animation
  channels across butterfly and whale, and zero embedded images.
- Image validation: each QA PNG is 900x700, inside the new-texture limit.

The 4/5 ratings are provisional Blender-render scores. Promotion is wired but
not final until Godot imports the assets and a Mobile-render gameplay screenshot
confirms scale, orientation, materials, animation, collision, and draw cost.
No Godot binary is available in this environment, so CI/import and device review
remain the acceptance gate.
