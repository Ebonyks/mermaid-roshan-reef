# D1-C06-S05 — Two purification fronts meet

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C06_S05_v1_rumi_rises.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C06_S05_v1_rumi_rises.mp4): frames 0–144 are mislabeled Rumi-rise imagery and omit the required two-front purification.
- [C06_S05_v2_rumi_rises.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C06_S05_v2_rumi_rises.mp4): frames 0–144 are mislabeled Rumi-rise imagery and omit the required two-front purification.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Two distinct clear fronts spread from the fixed left and right sources. Every changed frame is a new complete flattened image. |
| 048–107 | Each front displaces algae through the same water volume. Every changed frame is a new complete flattened image. |
| 108–144 | The fronts meet once near center in one bright ripple. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | pool geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/location/room_mermaid_pool_background.png |
| IMAGE_2 | left source identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/objects/mermaid_pool_waterfall_rest.png |
| IMAGE_3 | right source identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/objects/mermaid_pool_seahorse_fountain_rest.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: two water fronts spread and meet once.
- Must not move: pool boundary, sources, fixtures, room geometry, and dry surfaces.
- End state: one joined bright ripple rests at pool center.
- Reject: no instant flash, dry floor, third source, overlay-only effect, characters, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
