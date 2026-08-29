# Reference upload matrix

## Stable authorities in this Project

- `ROSHAN_IDENTITY` → `../../characters/roshan/ROSHAN_FRONT_IDENTITY.png`
- `ROSHAN_REAR` → `../../characters/roshan/ROSHAN_REAR_POSE_SHEET.png`
- `EAGLE_STANDING` →
  `../../characters/baby_eagle/BABY_EAGLE_STANDING_IDENTITY.png`
- `EAGLE_PINNED` →
  `../../characters/baby_eagle/BABY_EAGLE_PINNED_STATE.png`
- `BUNNY_HOP` →
  `../../characters/playroom_dust_bunny/PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png`
- `BUNNY_LIGHT_SWING` →
  `../../characters/playroom_dust_bunny/MOTION_LIGHT_SWING.png`
- `BUNNY_BOUNDER` →
  `../../characters/playroom_dust_bunny/MOTION_BOUNDER.png`
- `BUNNY_TWIRLER` →
  `../../characters/playroom_dust_bunny/MOTION_TWIRLER.png`
- `STUFFIE_ROOM_CLEAN` →
  `../../locations/stuffie_room/STUFFIE_ROOM_CLEAN_GEOGRAPHY.png`
- `STUFFIE_ROOM_DIRTY` →
  `../../locations/stuffie_room/STUFFIE_ROOM_DIRTY_GEOGRAPHY.png`

`EAGLE_STANDING` is the sole complete-body identity authority. `EAGLE_PINNED`
controls the low sad pose only. `BUNNY_HOP` controls ordinary Dust Bunny
identity; the other bunny images control pose/action without creating new
species or characters.

## Optional dirty perspective authorities

The ten aliases `P01_LEFT_DOORWAY` through `P10_REAR_RIGHT` map to the
normalized images under
`../../locations/stuffie_room/perspectives_dirty/`. Exact filenames, camera
roles and hashes are listed in that folder's `PERSPECTIVE_SET.md`.

For a perspective transition, attach exactly one selected `Pxx` authority,
the identity image for every character entering the dependent shot and the
accepted previous ending frame when continuity requires it. Do not attach
multiple viewpoints and ask Grok to average them. These optional angles are
dirty-state authorities only and never replace `STUFFIE_ROOM_CLEAN` after the
final gust.

## Explicit rejected reference

Never upload or use `assets/book/baby_eagle.png`. It shows Baby Eagle packing a
backpack and crops the lower body. It has no authority in either storyboard.

## Anchor reference order

| Anchor | Attach in this order | Purpose |
|---|---|---|
| `A01_DIRTY_ENTRY` | `STUFFIE_ROOM_DIRTY`, `ROSHAN_IDENTITY`, one base-video interior style still | Lock the complete dirty geography and Roshan's screen-left entry lane. |
| `A02_CENTER_LIGHT` | accepted `A01_DIRTY_ENTRY`, `BUNNY_HOP`, `BUNNY_LIGHT_SWING`, one style still | Lock the sole light swinger and Roshan's upward eyeline. |
| `A03_PINNED_EAGLE` | accepted `A01_DIRTY_ENTRY`, `EAGLE_STANDING`, `EAGLE_PINNED`, `BUNNY_HOP`, `ROSHAN_IDENTITY` | Lock the correct bag-free eagle, two wing bunnies and left-side Roshan. |
| `B01_DIRTY_CALM` | `STUFFIE_ROOM_DIRTY`, `EAGLE_STANDING`, `ROSHAN_IDENTITY`, one style still | Lock the still-dirty room and standing Baby Eagle before wave two. |
| `B02_BASKET_AMBUSH` | accepted `B01_DIRTY_CALM`, `BUNNY_HOP`, `BUNNY_LIGHT_SWING`, `BUNNY_BOUNDER`, `BUNNY_TWIRLER` | Lock exactly four distinct bunny trajectories from the two visible baskets while preserving the dirty room. |
| `B03_WING_BLAST` | accepted `B02_BASKET_AMBUSH`, `EAGLE_STANDING`, `BUNNY_HOP`, `STUFFIE_ROOM_CLEAN` | Lock the readable wing-flap silhouette, all four intact bunnies in the gust and the clean authority as the end state only. |

## Per-shot reference order

| Shot | Attach in this order |
|---|---|
| `SQ030_SH010` | approved `A01_DIRTY_ENTRY`, `ROSHAN_IDENTITY` |
| `SQ030_SH020` | accepted `SH010` ending frame, `ROSHAN_IDENTITY` |
| `SQ030_SH030` | approved `A02_CENTER_LIGHT`, `BUNNY_LIGHT_SWING`, `ROSHAN_IDENTITY` |
| `SQ030_SH040` | accepted `SH030` ending frame, `ROSHAN_IDENTITY` |
| `SQ030_SH050` | approved `A03_PINNED_EAGLE`, `EAGLE_STANDING`, `EAGLE_PINNED`, `BUNNY_HOP` |
| `SQ040_SH010` | approved `B01_DIRTY_CALM`, `EAGLE_STANDING`, `ROSHAN_IDENTITY` |
| `SQ040_SH020` | accepted `SH010` ending frame, `STUFFIE_ROOM_DIRTY` |
| `SQ040_SH030` | approved `B02_BASKET_AMBUSH`, `BUNNY_LIGHT_SWING`, `BUNNY_BOUNDER`, `BUNNY_TWIRLER` |
| `SQ040_SH040` | accepted `SH030` ending frame, `EAGLE_STANDING` |
| `SQ040_SH050` | approved `B03_WING_BLAST`, `EAGLE_STANDING`, `BUNNY_HOP`, `STUFFIE_ROOM_CLEAN` |
| `SQ040_SH060` | accepted `SH050` ending frame, `STUFFIE_ROOM_CLEAN`, `EAGLE_STANDING`, `ROSHAN_IDENTITY` |

Keep normal packs to three to five images. Reattach the exact accepted ending
frame for continuous motion; do not rely on a phrase such as “same room.”
