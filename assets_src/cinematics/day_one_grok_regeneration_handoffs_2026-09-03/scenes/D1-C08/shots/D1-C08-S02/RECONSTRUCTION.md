# D1-C08-S02 — Roshan clears the left rescue pin

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S03_v1_right_basket_ears_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/384abc966b92b27bd61a735319a7639ef68ac15b/clips_flat/C08_S03_v1_right_basket_ears_REGEN.mp4): branch frames 000–144: The opposite-basket warning is also invented and exposes a full bunny rather than an ears-only cue.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/arena/castle_rooms_25d.gd`.
- Event rule: Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens.
- Entry state: accepted D1-C08-S01 pre-contact endpoint.
- Single causal action: one left rescue pin pops after Roshan's contact.
- Required outgoing seam: the left pin is gone; the right pin still visibly holds one Baby Eagle.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | Roshan's hand completes one physical contact with the left pin bunny. Every changed frame is a new complete flattened image. |
| 048–083 | only the left bunny expands slightly and pops into a small lavender sparkle burst. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | the right pin remains attached and Baby Eagle remains safely held on that side. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: the left pin is gone; the right pin still visibly holds one Baby Eagle. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | pinned Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |
| IMAGE_4 | rescue-pin identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one left rescue pin pops after Roshan's contact.
- Must not move: right pin, Baby Eagle, room, clutter, Roshan anatomy, and dirty state.
- End state: the left pin is gone; the right pin still visibly holds one Baby Eagle.
- Reject: no right-pin pop, simultaneous pair, basket, four bunnies, eagle release, room cleanup, wing blast, text, HUD, or pearl reward.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
