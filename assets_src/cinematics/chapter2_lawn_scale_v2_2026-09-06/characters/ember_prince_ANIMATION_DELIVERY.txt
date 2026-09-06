# Ember Prince concrete animation delivery V2

Motion status: **REVIEW**. Identity remains approved private canon.

## Runtime atlas

`EMBER_PRINCE_RUNTIME_ATLAS.png` remains the 1024×768 transparent utility atlas:

| Cells | Motion | Timing |
| --- | --- | --- |
| 1–2 | `idle_glance` | 1.35 fps, `1 → 2 → 1`, loop |
| 3–6 | superseded walk keys | retained as source history only |
| 7–8 | `cinderstep` source keys | 3 fps one-shot mapping with settle |

`EMBER_PRINCE_WALK_ATLAS.png` is the production walk authority: a power-of-two
2048×1024 RGBA atlas containing sixteen 256×512 cells in an 8×2 layout. The
cycle plays at 14.285714 fps and covers two complete sleek steps with distinct
heel contact, foot-flat, compression, toe-off, passing and high-point phases.
Hair, coat tails and tail overlap the body on staggered frames. Individual walk
cells live under `walk_frames/`.

Utility PNG cells live under `frames/`. Silent 1024×576 H.264 review clips
and 512×288 GIF loops live under `animations/`. The MP4s are the review
authority for timing; the atlas is the pixel authority.

`EMBER_PRINCE_SPRITE_FRAMES.tres` exposes `idle_glance`, `sleek_walk` and
`cinderstep` to an `AnimatedSprite2D`. The walk and idle loop; Cinderstep lands
and returns to its guarded neutral pose.

## Acceptance checks

- The 16-frame walk stays narrow and level, shows two complete weight
  transfers, and remains visibly quicker than the King without foot sliding.
- Cinderstep reads through spacing rather than teleportation or blur.
- Shell remains anatomical and stable; the exposed red skin halo is visible in
  the rear idle/glance key.
- Prince's gaze and acting never imply shared candle fascination.
