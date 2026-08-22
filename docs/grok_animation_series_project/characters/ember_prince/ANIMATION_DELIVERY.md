# Ember Prince concrete animation delivery V1

Motion status: **REVIEW**. Identity remains approved private canon.

## Runtime atlas

`EMBER_PRINCE_RUNTIME_ATLAS.png` is a 1024×768 transparent RGBA atlas arranged
as four 256×384 cells across two rows:

| Cells | Motion | Timing |
| --- | --- | --- |
| 1–2 | `idle_glance` | 1.35 fps, `1 → 2 → 1`, loop |
| 3–6 | `sleek_walk` | 6.25 fps, four-key loop |
| 7–8 | `cinderstep` source keys | 3 fps one-shot mapping with settle |

Individual PNG cells live under `frames/`. Silent 1024×576 H.264 review clips
and 512×288 GIF loops live under `animations/`. The MP4s are the review
authority for timing; the atlas is the pixel authority.

`EMBER_PRINCE_SPRITE_FRAMES.tres` exposes `idle_glance`, `sleek_walk` and
`cinderstep` to an `AnimatedSprite2D`. The walk and idle loop; Cinderstep lands
and returns to its guarded neutral pose.

## Acceptance checks

- Walk stays narrow and level with visibly quicker cadence than the King.
- Cinderstep reads through spacing rather than teleportation or blur.
- Shell remains anatomical and stable; the exposed red skin halo is visible in
  the rear idle/glance key.
- Prince's gaze and acting never imply shared candle fascination.
