# D1-C03-S02 — Roshan crosses the dirty-bathroom threshold

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- Shot is absent from the delivered clip set.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Roshan crosses into the single-tub dirty bathroom. Every changed frame is a new complete flattened image. |
| 048–107 | She looks from the murky tub to the dirty sink while moving fully inside. Every changed frame is a new complete flattened image. |
| 108–144 | She settles with the entrance and room orientation still readable. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty bathroom layout | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/location/room_bubble_bath_dirty_day_one.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | dirty tub material | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/objects/target_tub_grime_v1.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: short follow.
- Must move: Roshan crosses and makes one tub-to-sink look.
- Must not move: single tub, sink, tools, grime cards, entrance, child identity, clothes, and continuous tail.
- End state: Roshan is fully inside and the entrance remains spatially clear.
- Reject: no legs, shoes, room rotation, second tub, cleaning, extra cast, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
