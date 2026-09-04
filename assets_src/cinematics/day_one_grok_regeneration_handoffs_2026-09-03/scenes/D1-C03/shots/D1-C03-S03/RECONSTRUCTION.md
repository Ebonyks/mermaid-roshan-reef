# D1-C03-S03 — Swimming bunny in the dirty tub

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C03_S03_v1_swimming_bunny_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C03_S03_v1_swimming_bunny_REGEN.mp4): release frames 000–144: The swimmer is coherent, but Roshan is a black silhouette/substitute and the bunny mostly holds instead of paddling visibly.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/games/day_one_bathroom_cleanup.gd`.
- Event rule: one dirty tub, one separate swimming bunny, an authorized tool basket, and two later live cleaning gestures.
- Entry state: accepted D1-C03-S02 endpoint.
- Single causal action: one bunny paddles and Roshan reacts.
- Required outgoing seam: the single swimmer is clearly visible and needs gentle rescue.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | one approved swimming dust bunny paddles weakly but safely in the murky tub. Every changed frame is a new complete flattened image. |
| 048–083 | the water stays dirty and the bunny remains a coherent single creature. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | roshan reacts with concern at frame edge. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: the single swimmer is clearly visible and needs gentle rescue. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty bathroom layout | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/location/room_bubble_bath_dirty_day_one.png |
| IMAGE_2 | swimming bunny identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/characters/swimming_bunny_dust_bunny_swimming.png |
| IMAGE_3 | murky tub material | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/objects/target_tub_grime_v1.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one bunny paddles and Roshan reacts.
- Must not move: tub geometry, sink, dirty water state, bunny anatomy, and Roshan edge position.
- End state: the single swimmer is clearly visible and needs gentle rescue.
- Reject: no duplicate bunny, land bunny, clean water, drowning terror, invented anatomy, room redesign, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
