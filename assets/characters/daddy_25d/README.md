# Daddy Mermaid 2.5D sprite contract

These atlases are project-owned, non-destructive animation derivatives of the
protected Daddy Mermaid design. They replace a static cutout only at explicitly
animated call sites; the protected sources remain unchanged.

## Atlas contract

All runtime atlases use row-major frame order and exact 256 x 256 cells.

| Atlas | Grid | Frames | Timing | Playback |
|---|---:|---:|---:|---|
| `daddy_idle.png` | 4 x 2 | 8 | 4 fps | seamless loop |
| `daddy_swim.png` | 4 x 4 | 16 | 8 fps | seamless moving loop |
| `daddy_gesture_a.png` | 4 x 4 | 4 per row | 6 fps | one-shot row, then idle |
| `daddy_victory.png` | 4 x 2 | 8 | 8 fps, then 0.30 s final hold | one-shot, then idle; 1.30 s total |

`daddy_gesture_a.png` assigns rows in this order:

1. wave
2. invite
3. clap
4. hug

The tail-root/torso junction is the spatial anchor for every frame. The torso
may breathe or act, but it must not skate within a cell. Every successive frame
contains authored movement through the continuous tail and large bifurcated
fluke; hair, cape, side fins, and fluke use follow-through. The build pipeline
aligns every complete drawing to one shared torso anchor before sticker baking,
so runtime playback needs no per-frame translation that could suppress motion.

Animation priority is action, then movement, then idle. One-shots return to
idle. Victory must read and complete inside the combat arena's shortest success
window; the eight 8 fps frames plus final hold must never exceed 1.30 seconds.

## Sources and derivation

Identity and costume authority is `assets_src/daddy_master.png`. The protected
runtime friend cutout `assets/characters/friends/daddy.webp` and approved
sticker `assets/characters/stickers/daddy.png` are comparison references. None
of these three files is modified by this animation set.

Native generated sheets and full provenance are retained in
`assets_src/imagegen/daddy_25d_tailmotion_2026-08-01/`. OpenAI built-in image
generation created complete atlas images on a flat green field. The production
pipeline removes only the border-connected matte, preserves enclosed green
colors in Daddy's rainbow design, normalizes each cell to 256 x 256, and applies
the established white sticker rim and navy contact-shadow language. The earlier
static-tail candidates in `assets_src/imagegen/daddy_25d_2026-08-01/` are
rejected review material and are not shipped as runtime art.

## Mobile constraints

- Runtime sheets are at most 1024 px on either axis: 1024 x 512 for idle and
  victory, and 1024 x 1024 for swim and gestures.
- The complete subject uses a common 188 px normalized span inside each padded
  cell; callsite pixel sizes restore the established apparent standee height.
- Use an unshaded, shadowless Sprite3D/material path under the Mobile renderer.
- Do not add lights, physics bodies, skeletal rigs, procedural tail deformation,
  or per-frame texture allocations for these clips.
- Keep one texture resident for the active clip and switch atlas regions; hidden
  cameos do no animation work until shown.
