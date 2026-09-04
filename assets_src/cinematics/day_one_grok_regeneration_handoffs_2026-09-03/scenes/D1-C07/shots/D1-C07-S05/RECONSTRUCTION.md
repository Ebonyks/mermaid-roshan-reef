# D1-C07-S05 — Partial Baby Eagle wing trail

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C07_S05_wing_trail.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S05_wing_trail.mp4): frames 48–144 expose the full eagle too early instead of preserving the partial discovery.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Begin with roshan's gaze line and only a partly obscured turquoise, yellow, and pink wing beneath grounded clutter. Every changed frame is a new complete flattened image. |
| 048–107 | Reveal more of the same wing along the existing floor trail without exposing the full bird. Every changed frame is a new complete flattened image. |
| 108–144 | Stop while the wing remains partly hidden. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | Baby Eagle colors and anatomy | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: slow lateral reveal.
- Must move: one partial wing becomes identifiable.
- Must not move: every pile, fixture, floor contact, Roshan, and the hidden bird position.
- End state: one Baby Eagle wing is identifiable but the full bird is not yet revealed.
- Reject: no full-body reveal, duplicate bird, injury, arrow, moving furniture, cleanup, new prop, camera rotation, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
