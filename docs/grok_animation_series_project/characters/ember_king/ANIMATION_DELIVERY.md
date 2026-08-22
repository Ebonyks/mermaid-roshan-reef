# Ember King concrete animation delivery V2

Motion status: **REVIEW**. Identity remains approved private canon.

## Runtime atlas

`EMBER_KING_RUNTIME_ATLAS.png` remains the 1024×768 transparent utility atlas:

| Cells | Motion | Timing |
| --- | --- | --- |
| 1–2 | `idle` | 1.35 fps, `1 → 2 → 1`, loop |
| 3–6 | superseded walk keys | retained as source history only |
| 7–8 | `cape_fan` source keys | 2.2 fps one-shot mapping with settle |

`EMBER_KING_WALK_ATLAS.png` is the production walk authority: a power-of-two
2048×1024 RGBA atlas containing sixteen 256×512 cells in an 8×2 layout. The
cycle plays at 10 fps and covers two complete heavy steps: contact, foot-flat,
compression, toe-off, passing, high point and opposite contact, with cape lag
continuing across the loop. Individual walk cells live under `walk_frames/`.

Utility PNG cells live under `frames/`. Silent 1024×576 H.264 review clips
and 512×288 GIF loops live under `animations/`. The MP4s are the review
authority for timing; the atlas is the pixel authority.

`EMBER_KING_SPRITE_FRAMES.tres` exposes `idle`, `heavy_walk` and `cape_fan` to
an `AnimatedSprite2D`. The first two loop; `cape_fan` finishes on the neutral
idle key.

## Acceptance checks

- The 16-frame walk must show two complete weight transfers without held-pose
  jumps or duplicated cells.
- Shell and cape mass lag the feet rather than sliding with the body.
- The cape endpoint remains fully inside its cell and the shell remains visible.
- No candle is baked into any reusable frame.
