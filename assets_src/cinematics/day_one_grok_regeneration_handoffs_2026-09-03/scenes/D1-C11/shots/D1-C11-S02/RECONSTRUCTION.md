# D1-C11-S02 — Main Hall boss-door approach

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C11_S02_approach_boss_door.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C11_S02_approach_boss_door.mp4): frames 48–144 do not reliably hold the exact door geometry and pre-contact seam.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Roshan glides through the approved clean main hall toward the glowing boss door. Every changed frame is a new complete flattened image. |
| 048–107 | Her continuous rainbow tail moves naturally while the closed door remains unchanged. Every changed frame is a new complete flattened image. |
| 108–144 | She stops and holds one hand just before the handle seam. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | Main Hall Screen-B layout | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/location/main_hall_screen_b_room_led_master.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | connected hall topology | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/objects/main_hall_screen_a_room_led_master.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: smooth follow.
- Must move: Roshan makes one continuous approach and stops.
- Must not move: Main Hall architecture, four restored route lights, boss-door geometry, handle seam, and Roshan identity.
- End state: Roshan's hand is just before the unchanged closed boss-door seam.
- Reject: no door redesign, curtain-to-wood morph, legs, adult proportions, extra cast, teleport, text, HUD, or camera drift.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
