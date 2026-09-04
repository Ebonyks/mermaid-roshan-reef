# D1-C08-S02 — Left basket ears-only warning

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S02_left_basket_ears.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C08_S02_left_basket_ears.mp4): frames 48–144 drift bunny anatomy beyond the approved ears-only read.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | The established left basket makes one small warning wobble. Every changed frame is a new complete flattened image. |
| 048–107 | Exactly one pair of lavender bunny ears rises briefly above the rim and ducks back. Every changed frame is a new complete flattened image. |
| 108–144 | The basket becomes still without a full bunny emerging. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | bunny ear and color identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |
| IMAGE_3 | left-side landmark | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/objects/room_playroom_item_play_tent.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one left basket wobble and one ear-pair peek.
- Must not move: left basket, dirty room, background, rim, and hidden bunny body.
- End state: the left basket is still after one ears-only warning.
- Reject: no full body, second ear pair, claws, scary eyes, duplicated basket, room change, cleanup, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
