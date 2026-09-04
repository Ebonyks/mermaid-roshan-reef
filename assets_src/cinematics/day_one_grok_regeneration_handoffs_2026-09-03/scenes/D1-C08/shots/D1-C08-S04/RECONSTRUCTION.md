# D1-C08-S04 — Roshan clears the right pin and completes the room

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S06_v1_wing_blast_clean_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S06_v1_wing_blast_clean_REGEN.mp4): release frames 000–144: Baby Eagle never performs a wing-blast cleanup. Gameplay completes when Roshan clears the second pin.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/arena/castle_rooms_25d.gd`.
- Event rule: Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens.
- Entry state: accepted D1-C08-S03 right-pin pre-contact endpoint.
- Single causal action: one right-pin contact causes one pop, the rescue release, and the game-authored clean resolve.
- Required outgoing seam: both pins are gone, the room is clean, and Baby Eagle is free but has not departed.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | Roshan's hand completes one physical contact with the remaining right pin bunny. Every changed frame is a new complete flattened image. |
| 048–083 | only that bunny pops into a small sparkle burst and Baby Eagle becomes free. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | the exact room resolves from dirty to clean while Baby Eagle stays in the same floor position. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: both pins are gone, the room is clean, and Baby Eagle is free but has not departed. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | Stuffie Room dirty-to-clean geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |
| IMAGE_4 | right rescue-pin identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one right-pin contact causes one pop, the rescue release, and the game-authored clean resolve.
- Must not move: Roshan, Baby Eagle identity, fixture positions, floor geography, absent left pin, and camera.
- End state: both pins are gone, the room is clean, and Baby Eagle is free but has not departed.
- Reject: no basket, four-bunny emergence, wing blast, tornado, magic before contact, duplicate eagle, relocation, text, HUD, or picker UI.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
