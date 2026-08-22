# Ember King concrete animation delivery V1

Motion status: **REVIEW**. Identity remains approved private canon.

## Runtime atlas

`EMBER_KING_RUNTIME_ATLAS.png` is a 1024×768 transparent RGBA atlas arranged as
four 256×384 cells across two rows:

| Cells | Motion | Timing |
| --- | --- | --- |
| 1–2 | `idle` | 1.35 fps, `1 → 2 → 1`, loop |
| 3–6 | `heavy_walk` | 4.35 fps, four-key loop |
| 7–8 | `cape_fan` source keys | 2.2 fps one-shot mapping with settle |

Individual PNG cells live under `frames/`. Silent 1024×576 H.264 review clips
and 512×288 GIF loops live under `animations/`. The MP4s are the review
authority for timing; the atlas is the pixel authority.

`EMBER_KING_SPRITE_FRAMES.tres` exposes `idle`, `heavy_walk` and `cape_fan` to
an `AnimatedSprite2D`. The first two loop; `cape_fan` finishes on the neutral
idle key.

## Acceptance checks

- The walk must feel like contact → compression → overstep → recovery.
- Shell and cape mass lag the feet rather than sliding with the body.
- The cape endpoint remains fully inside its cell and the shell remains visible.
- No candle is baked into any reusable frame.
