# D1-C05-S05 — Sick seahorse with mouth plug

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C05_S05_v1_sick_seahorse_plug_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C05_S05_v1_sick_seahorse_plug_REGEN.mp4): release frames 000–144: The mouth plug is readable, but the pool is already clean and Roshan is full-body from frame 0 instead of entering only at the edge of a dirty-state close-up.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/games/day_one_pool_cleanup.gd`.
- Event rule: the dirty pool begins with six surface targets, three waterfall lanes, and an eight-tug seahorse obstruction.
- Entry state: approved right-center seahorse close composition; skip regeneration only if Sol confirms the existing mouth plug and topology.
- Single causal action: Roshan enters the edge while the weak seahorse coughs once.
- Required outgoing seam: the mouth plug is readable and still lodged.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | show the exact long-snouted seahorse at correct right-center scale. Every changed frame is a new complete flattened image. |
| 048–083 | a soggy pink wrapper-and-weed plug remains unmistakably lodged in its mouth nozzle. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | roshan's concerned face enters at frame edge and stops. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: the mouth plug is readable and still lodged. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | pool geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c05_pool_dirty_discovery_visual_v1/handoff_art/location/room_mermaid_pool_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c05_pool_dirty_discovery_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | sick seahorse identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c05_pool_dirty_discovery_visual_v1/handoff_art/objects/seahorse_sick.png |
| IMAGE_4 | mouth plug material | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c05_pool_dirty_discovery_visual_v1/handoff_art/objects/seahorse_mouth_trash.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Roshan enters the edge while the weak seahorse coughs once.
- Must not move: seahorse topology, right-center position, plug contact, pool geography, and dirty state.
- End state: the mouth plug is readable and still lodged.
- Reject: no different animal, plug beside the mouth, clean flow, frightening injury, extraction, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
