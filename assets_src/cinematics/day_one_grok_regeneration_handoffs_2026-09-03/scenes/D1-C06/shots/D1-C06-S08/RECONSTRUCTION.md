# D1-C06-S08 — Rumi thanks Roshan and opens her arms

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C06_S08_v1_rumi_invitation_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C06_S08_v1_rumi_invitation_REGEN.mp4): release frames 104–144: Rumi's thanks and open-arm invitation work through frame 103, but Roshan then approaches and starts the hug before the dedicated hug shot.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/games/day_one_pool_cleanup.gd`.
- Event rule: pool_surface → waterfall → seahorse is the fixed order; Rumi rises only after all three complete.
- Entry state: accepted D1-C06-S07 Rumi reveal endpoint.
- Single causal action: Rumi makes one thanks-to-invitation gesture.
- Required outgoing seam: Rumi's arms are open and Roshan remains separate before the hug.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | rumi places one hand over her heart and gives one warm speaking gesture. Every changed frame is a new complete flattened image. |
| 048–083 | she opens both arms toward Roshan while both bodies stay separate. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | she holds the clear invitation. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: Rumi's arms are open and Roshan remains separate before the hug. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | clean pool geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/location/room_mermaid_pool_background.png |
| IMAGE_2 | Rumi identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/characters/rumi_rumi_full_body_identity.png |
| IMAGE_3 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/handoff_art/characters/roshan_roshan_base.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Rumi makes one thanks-to-invitation gesture.
- Must not move: Rumi and Roshan identities, scale, faces, hands, continuous tails, pool, and both streams.
- End state: Rumi's arms are open and Roshan remains separate before the hug.
- Reject: no subtitles, synthetic dialogue, hand deformation, extra cast, fused bodies, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
