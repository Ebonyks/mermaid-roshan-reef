# Sky Lagoon background resolution audit — 2026-07-27

## Scope and disposition

The superseded runtime panorama was a 1024×341 downscale of the approved
generated art. It has been removed. The approved generated master is now
preserved byte-for-byte at its native 2172×724 dimensions and exact 3:1
aspect ratio. Runtime reconstruction uses three non-overlapping lossless
724×724 crops on adjacent unshaded Sprite3D cards at one coherent depth.

No stretch, crop of the master composition, padding, canvas extension,
letterbox, or ratio-changing regeneration remains.

## Before / after

| Artifact | Dimensions | Ratio | Ratio delta from 3:1 | SHA-256 |
|---|---:|---:|---:|---|
| Superseded scaled runtime panorama | 1024×341 | 3.0029325513 | 0.0029325513 | `2bd485457797d912ab6719efe88403d824acd9f3e79db9dd6cd6b3a7de677a4d` |
| Preserved approved master | 2172×724 | 3.0000000000 | 0.0000000000 | `7952b4579c922025a3030b3ddd976247fde138f697f00468b5a08fd5b88d66e3` |
| Runtime reconstruction | 2172×724 | 3.0000000000 | 0.0000000000 | Pixel-exact reconstruction of master |

The native long edge is 2172 pixels, satisfying the ≥2048 requirement
without upscaling.

## Lossless tile ledger

Coordinates are `(x, y, width, height)` in native-master pixels.

| Tile | Rectangle | Dimensions | SHA-256 |
|---|---:|---:|---|
| `flat_sky_lagoon_main_panorama_tile_0.png` | `(0, 0, 724, 724)` | 724×724 | `78b1a33e5487d9dfbb75ab92fea5de84c20f4c1a7164eb5b1e8c8e9dba842703` |
| `flat_sky_lagoon_main_panorama_tile_1.png` | `(724, 0, 724, 724)` | 724×724 | `b32ac8aebab3cbdf5d82a00f7004104981039a487ea0df829a44061b5e110a78` |
| `flat_sky_lagoon_main_panorama_tile_2.png` | `(1448, 0, 724, 724)` | 724×724 | `ee3477137069b0fe3a5e007d84ca79fbdd52e82c2fa796c8ebbd988dcd159e3a` |

Tiles cover `[0,2172)×[0,724)` exactly, with no gap, overlap, or scaling.
Each runtime texture has a long edge of 724 pixels.

## Content invariance and seams

- Pixel reconstruction comparison: exact; `ImageChops.difference()` returned
  a null bounding box.
- 50% master/reconstruction overlay:
  `audit/sky_lagoon_panorama_content_invariance_overlay.png`
  (`b300df1ddb616e873d4c8d3a8d0e0d51eb98d0849a30c9b21266ba48e59f6650`).
- Seam capture:
  `audit/sky_lagoon_panorama_seam_capture.png`
  (`1fa87682faed7114de38ee23648e409cea1cdf038faa19343d5ed724688d0890`).
- Seam-capture source rectangles:
  `(700, 0, 48, 724)` around x=724 and
  `(1424, 0, 48, 724)` around x=1448.

## Sprite3D, camera, touch, and navigation validation

`scripts/probe_l2.gd` validates:

- the 2172×724 native master and exact 3:1 ratio;
- all three 724×724 runtime tiles;
- three backdrop cards at x = -48, 0, 48, y = 24, z = -18;
- a shared depth and exact 48-world-unit edge meeting;
- 23 unshaded Sprite3D world-art cards, zero MeshInstance3D world art,
  zero CanvasItem world art, and no invalid pixel scale;
- at least four real depth layers and no more than 14 simultaneously visible
  cards for the Speedy-tier overdraw budget;
- one activity frame in each screen;
- first touch highlights and second touch launches the minigame;
- plane, playground, castle, Northern transition, camera follow, and traversal
  behavior remain reachable.

Static validation is:

```text
python -m gdtoolkit.parser scripts/arena/sky_lagoon_promenade.gd scripts/probe_l2.gd
python tools/lint_inference.py scripts/arena/sky_lagoon_promenade.gd scripts/probe_l2.gd
git diff --check
```

The exact-revision GitHub import, analyzer, trusted-probe, and visual-capture
run is linked in the implementation handoff for this audit.
