# D1-C08-S01 — Roshan approaches the two-pin rescue

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S02_v1_left_basket_ears_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S02_v1_left_basket_ears_REGEN.mp4): release frames 000–144: Basket warnings do not occur in gameplay; the bunny body is already outside the basket.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/arena/castle_rooms_25d.gd`.
- Event rule: Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens.
- Entry state: accepted D1-C07-S06 exact two-pin endpoint.
- Single causal action: Roshan makes one careful approach toward the left pin.
- Required outgoing seam: Roshan is poised before the left pin; both pins still hold the Eagle.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | inherit the exact C07-S06 state with one Baby Eagle held by two distinct pin bunnies. Every changed frame is a new complete flattened image. |
| 048–083 | Roshan moves toward the left pin while the right pin and Baby Eagle remain fixed. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | her hand stops in a visible gap before the left pin. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: Roshan is poised before the left pin; both pins still hold the Eagle. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | pinned Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |
| IMAGE_4 | two rescue-pin identities | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: subtle push-in.
- Must move: Roshan makes one careful approach toward the left pin.
- Must not move: one Baby Eagle, both pin bunnies, pin contacts, clutter, room topology, and dirty state.
- End state: Roshan is poised before the left pin; both pins still hold the Eagle.
- Reject: no basket, swing, four-bunny group, touch, pop, release, cleanup, wing blast, text, HUD, or extra cast.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
