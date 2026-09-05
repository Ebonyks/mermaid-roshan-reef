# D1-C08-S03 — Roshan reframes the remaining right pin

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S04_v1_four_bunnies_emerge_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/384abc966b92b27bd61a735319a7639ef68ac15b/clips_flat/C08_S04_v1_four_bunnies_emerge_REGEN.mp4): branch frames 000–144; count failure 048–144: The game has two rescue pins, not four emerging basket bunnies; the rendered count also grows ambiguous beyond four.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/arena/castle_rooms_25d.gd`.
- Event rule: Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens.
- Entry state: accepted D1-C08-S02 one-pin endpoint.
- Single causal action: Roshan makes one short move toward the right pin.
- Required outgoing seam: one right pin remains; Roshan is poised before contact and Baby Eagle is still safe.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | begin with the left pin absent and the right pin still attached to Baby Eagle. Every changed frame is a new complete flattened image. |
| 048–083 | Roshan shifts once across the fixed floor toward the right pin. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | she stops with her hand visibly short of the remaining bunny. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: one right pin remains; Roshan is poised before contact and Baby Eagle is still safe. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | pinned Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |
| IMAGE_4 | remaining right-pin identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: short lateral.
- Must move: Roshan makes one short move toward the right pin.
- Must not move: right-pin contact, Baby Eagle, absent left pin, room, clutter, and dirty state.
- End state: one right pin remains; Roshan is poised before contact and Baby Eagle is still safe.
- Reject: no reappearing left pin, basket, extra bunny, pop, release, cleanup, wing blast, text, HUD, or camera rotation.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
