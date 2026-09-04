# D1-C07-S06 — One Baby Eagle held by exactly two rescue pins

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C07_S06_v1_pinned_baby_eagle_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C07_S06_v1_pinned_baby_eagle_REGEN.mp4): release frames 000–144: One Eagle is present, but neither of the two required rescue-pin bunnies is visible and the bird becomes free/upright before player action.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/arena/castle_rooms_25d.gd`.
- Event rule: one Baby Eagle is visibly held by exactly two rescue pin bunnies; no swing or partial-wing hunt exists.
- Entry state: accepted D1-C07-S02 dirty-room entry endpoint, with the stale swinging/partial-wing S04–S05 beats omitted.
- Single causal action: Roshan makes one edge entrance and concerned look; the pinned trio only breathes.
- Required outgoing seam: one unharmed Baby Eagle remains visibly held by exactly two pin bunnies while Roshan is ready to help.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | show the exact dirty Stuffie Room floor position with one Baby Eagle fully readable beneath soft clutter. Every changed frame is a new complete flattened image. |
| 048–083 | show exactly two separate lavender rescue-pin bunnies visibly holding the left and right sides while Roshan enters the edge. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | Roshan makes concerned eye contact and stops before either pin is touched. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: one unharmed Baby Eagle remains visibly held by exactly two pin bunnies while Roshan is ready to help. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | pinned Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |
| IMAGE_4 | two rescue-pin identities | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Roshan makes one edge entrance and concerned look; the pinned trio only breathes.
- Must not move: Baby Eagle position, two pin contacts, dirty room, clutter, floor landmarks, bodies, and cast count.
- End state: one unharmed Baby Eagle remains visibly held by exactly two pin bunnies while Roshan is ready to help.
- Reject: no missing pin, third bunny, basket, swing, partial-wing trail, release, cleanup, bird rise, duplicate body, injury, text, HUD, or camera drift.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
