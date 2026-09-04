# D1-C03-S04 — Pre-contact tool resolve

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C03_S04_v1_precontact_tools_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C03_S04_v1_precontact_tools_REGEN.mp4): release frames 000–144 swimmer absent; 060–144 premature contact: The required swimmer disappears and Roshan advances into scrub-brush contact rather than stopping at the pre-contact seam.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/games/day_one_bathroom_cleanup.gd`.
- Event rule: one dirty tub, one separate swimming bunny, an authorized tool basket, and two later live cleaning gestures.
- Entry state: accepted D1-C03-S03 endpoint.
- Single causal action: Roshan makes one gaze-and-reach action.
- Required outgoing seam: Roshan holds a determined pre-contact hand gap while all dirt remains.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | roshan follows her gaze from the swimmer toward the dirty sink and approved tools. Every changed frame is a new complete flattened image. |
| 048–083 | she reaches toward the nearest approved tool without changing the room state. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | her hand stops in a clean visible gap before contact. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: Roshan holds a determined pre-contact hand gap while all dirt remains. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty bathroom layout | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/location/room_bubble_bath_dirty_day_one.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | approved tool group | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/objects/cleanup_basket.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: subtle push-in.
- Must move: Roshan makes one gaze-and-reach action.
- Must not move: dirty room, murky tub, swimmer, sink, tools, grime, and character anatomy.
- End state: Roshan holds a determined pre-contact hand gap while all dirt remains.
- Reject: no scrub, tool teleport, UI pointer, extra supplies, room redesign, cleanup, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
