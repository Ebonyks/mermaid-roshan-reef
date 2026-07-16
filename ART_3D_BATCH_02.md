# 3D Replacement Batch 02

_Built: 2026-07-14 with Blender 4.4.3_

Batch 02 replaces the score-1/2 picture-game icon family with transparent
orthographic renders from reusable 3D models. The runtime remains 2D because
these objects are large touch targets, growth-stage layers, and detachable
ornaments. Their editable source geometry is stored in
`assets_src/blender/low_score_batch_02.blend`.

Protected book art was not opened or modified. In particular, the carrot,
watering can, friendship flower, snowman source art, characters, family
cutouts, and child-owned toys remain outside this build.

## Runtime replacements

| Family | Runtime files | Functional contract | Provisional score |
|---|---|---|---:|
| Snowman coal | `coal.png` | Same image serves two selectable eyes and two placed face pieces | 4/5 |
| Growth stages | `seed.png`, `sprout.png`, `k_sprout.png` | Seed and sprout remain centered, distinct, and readable at 42-150px | 4/5 |
| Flower family | `flower.png`-`flower4.png`, `k_flower1.png`, `k_flower2.png` | Six distinct blossoms share stem, leaf, contour, scale, and palette rules | 4/5 |
| Bush family | `k_bush.png`, `k_bush2.png` | Rounded shrub and flowering shrub; the former 1/5 cone silhouette is retired | 4/5 |
| Tree family | `tree.png`, `k_pine.png`, `xtree.png`, `k_xmastree.png` | Broadleaf, pine, and empty Christmas-tree roles remain distinct | 4/5 |
| Reward icons | `sun.png`, `star.png` | Friendly non-character silhouettes without invented faces | 4/5 |
| Detachable ornaments | `orn1.png`-`orn5.png` | Five independent shapes with consistent caps and hanging loops | 4/5 |

## Christmas logic correction

The prior `xtree.png` already contained colored bulbs and a star, while the
game separately asked the child to place five ornaments and then add the
protected friendship flower as the topper. The new `xtree.png` and
`k_xmastree.png` are deliberately empty: no bulbs, no star, and no baked
ornaments. The five ornament files remain separate and the friendship flower
continues to be loaded directly from protected book art.

## Rendering contract

- 21 editable source models produce 23 runtime PNGs.
- Every PNG is 512x512 RGBA, power-of-two, and below the 1024px limit.
- Materials are rough, nonmetallic, and use broad Mermaid Roshan palette
  regions. Freestyle contours are navy rather than black.
- Files retain their existing names, so picture-game touch sizing, centered
  aspect behavior, growth transitions, and ornament coordinates need no code
  changes.
- No faces were invented for plants, coal, sun, star, or ornaments.

Final acceptance requires a Mobile screenshot of the garden, snowman,
trampoline, and Christmas picture games. The generated source and runtime
assets pass Blender visual review at 4/5 provisionally.
