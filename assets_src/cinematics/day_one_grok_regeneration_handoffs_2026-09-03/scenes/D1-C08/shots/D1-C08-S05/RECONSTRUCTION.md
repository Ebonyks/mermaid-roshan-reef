# D1-C08-S05 — Baby Eagle thanks Roshan and departs

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S07_v1_clean_endpoint_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S07_v1_clean_endpoint_REGEN.mp4): release frames 000–144; side-wall drift 048–144: The one-Eagle/four-bunny endpoint is not a game state and the room projection drifts into invented side-wall geometry.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/arena/castle_rooms_25d.gd`.
- Event rule: Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens.
- Entry state: accepted D1-C08-S04 clean post-rescue endpoint.
- Single causal action: one Baby Eagle rises and departs after the rescue.
- Required outgoing seam: Roshan remains in the clean room after Baby Eagle exits; the next event may open the picker UI.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | begin in the exact clean post-rescue room with one free Baby Eagle beside Roshan. Every changed frame is a new complete flattened image. |
| 048–083 | Baby Eagle gives one happy chirp, rises slightly, and begins a gentle upward departure. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | the bird fades only after clearing Roshan while the clean room holds for the companion-picker seam. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: Roshan remains in the clean room after Baby Eagle exits; the next event may open the picker UI. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | clean Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | freed Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/baby_eagle_standing_BABY_EAGLE_STANDING_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: subtle upward follow.
- Must move: one Baby Eagle rises and departs after the rescue.
- Must not move: clean room, Roshan, fixture positions, bird identity, empty pin locations, and UI-free frame.
- End state: Roshan remains in the clean room after Baby Eagle exits; the next event may open the picker UI.
- Reject: no four bunnies, wing-blast cleanup, new companion choice, visible picker UI, duplicate bird, room drift, basket action, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
