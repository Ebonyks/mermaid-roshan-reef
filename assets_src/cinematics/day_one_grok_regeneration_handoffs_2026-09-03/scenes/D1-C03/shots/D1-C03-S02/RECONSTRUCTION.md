# D1-C03-S02 — Roshan crosses the dirty-bathroom threshold

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C03_S02_v1_dirty_bathroom_threshold_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/384abc966b92b27bd61a735319a7639ef68ac15b/clips_flat/C03_S02_v1_dirty_bathroom_threshold_REGEN.mp4): branch frames 000–144 both variants: Neither variant establishes the doorway. One starts mid-room and ends seated by the sink; the other begins inside the bathtub and crosses the tub instead of the threshold.
- [C03_S02_v1_threshold_cross_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/384abc966b92b27bd61a735319a7639ef68ac15b/clips_flat/C03_S02_v1_threshold_cross_REGEN.mp4): branch frames 000–144 both variants: Neither variant establishes the doorway. One starts mid-room and ends seated by the sink; the other begins inside the bathtub and crosses the tub instead of the threshold.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/games/day_one_bathroom_cleanup.gd`.
- Event rule: one dirty tub, one separate swimming bunny, an authorized tool basket, and two later live cleaning gestures.
- Entry state: accepted D1-C03-S01 dirty-room endpoint.
- Single causal action: Roshan crosses and makes one tub-to-sink look.
- Required outgoing seam: Roshan is fully inside and the entrance remains spatially clear.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | roshan crosses into the single-tub dirty bathroom. Every changed frame is a new complete flattened image. |
| 048–083 | she looks from the murky tub to the dirty sink while moving fully inside. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | she settles with the entrance and room orientation still readable. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: Roshan is fully inside and the entrance remains spatially clear. Every changed frame is a new complete flattened image. |

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
