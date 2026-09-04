# D1-C06-S03 — Rainbow waterfall restarts top-down

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C06_S03_rainbow_waterfall.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C06_S03_rainbow_waterfall.mp4): frames 0–47 begin too clean or from the wrong source composition.
- [C06_S03_v1_rainbow_restart.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C06_S03_v1_rainbow_restart.mp4): frames 48–144 reverse or blur the top-down causal read.
- [C06_S03_v2_rainbow.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C06_S03_v2_rainbow.mp4): frames 0–144 use an inconsistent composition.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Clean rainbow ignites at the exact blocked top source. Every changed frame is a new complete flattened image. |
| 048–107 | The clean band travels downward and pushes sludge and debris away. Every changed frame is a new complete flattened image. |
| 108–144 | The flow reaches the lower lip and settles. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | pool geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/location/room_mermaid_pool_background.png |
| IMAGE_2 | restored waterfall identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/objects/mermaid_pool_waterfall_rest.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: gentle downward tilt.
- Must move: one top-down clearing front.
- Must not move: fixture position, arches, flow direction, pool scale, and dirty room outside the cleared band.
- End state: clean rainbow reaches the lower lip without changing the rest of the room.
- Reject: no bottom-up start, instant clean room, separate basin, seahorse, Rumi, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
