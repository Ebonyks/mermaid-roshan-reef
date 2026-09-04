# D1-C06-S03 — Rainbow waterfall restarts top-down

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C06_S03_v1_rainbow_waterfall_restart_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C06_S03_v1_rainbow_waterfall_restart_REGEN.mp4): release frames 000–047 missing blocked start; 048–144 wrong clearing: The waterfall starts clean; later debris becomes a central raised dark mass and the flow retracts instead of clearing from the top source downward.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/games/day_one_pool_cleanup.gd`.
- Event rule: pool_surface → waterfall → seahorse is the fixed order; Rumi rises only after all three complete.
- Entry state: accepted blocked-source endpoint inherited from D1-C05-S04.
- Single causal action: one top-down clearing front.
- Required outgoing seam: clean rainbow reaches the lower lip without changing the rest of the room.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | clean rainbow ignites at the exact blocked top source. Every changed frame is a new complete flattened image. |
| 048–083 | the clean band travels downward and pushes sludge and debris away. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | the flow reaches the lower lip and settles. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: clean rainbow reaches the lower lip without changing the rest of the room. Every changed frame is a new complete flattened image. |

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
