# D1-C01-S02 — Daddy offers his hand on the dock

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C01_S02_v1_dock_handoffer_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/384abc966b92b27bd61a735319a7639ef68ac15b/clips_flat/C01_S02_v1_dock_handoffer_REGEN.mp4): branch frames 000–144: Daddy is already outside and offering at frame 0; the required plane exit, turn, and Roshan-from-doorway handoff never occur.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Implemented-event contract

- Runtime authority: `scripts/day_one_director.gd`.
- Event rule: arrival media precedes the dirty-castle discovery; the lagoon handoff must preserve Roshan, Daddy, the stationary plane, and the closed castle.
- Entry state: accepted clean endpoint extracted from D1-C01-S01.
- Single causal action: Daddy exits and offers; Roshan completes one hand contact.
- Required outgoing seam: Roshan and Daddy hold hands beside the unchanged stationary plane.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–023 | Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state. Every changed frame is a new complete flattened image. |
| 024–047 | daddy exits the stationary pearl plane, turns, and offers one open hand. Every changed frame is a new complete flattened image. |
| 048–083 | roshan places her hand in his while both tails and costumes remain coherent. Every changed frame is a new complete flattened image. |
| 084–107 | Complete the same dominant action without adding a second event or changing topology. Every changed frame is a new complete flattened image. |
| 108–131 | they settle at child-safe distance with correct hand contact. Every changed frame is a new complete flattened image. |
| 132–144 | Hold the exact endpoint: Roshan and Daddy hold hands beside the unchanged stationary plane. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | layout and lighting | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c01_lagoon_landing_castle_approach_visual_v1/handoff_art/location/sky_lagoon_panorama_master_v5_hd_3x1.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c01_lagoon_landing_castle_approach_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | Daddy identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c01_lagoon_landing_castle_approach_visual_v1/handoff_art/characters/daddy_daddy_master.png |
| IMAGE_4 | pearl plane identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c01_lagoon_landing_castle_approach_visual_v1/handoff_art/objects/06_AIRPLANE_EXACT.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Daddy exits and offers; Roshan completes one hand contact.
- Must not move: plane, dock, waterline, castle silhouette, costumes, crowns, glasses, and continuous tails.
- End state: Roshan and Daddy hold hands beside the unchanged stationary plane.
- Reject: no pulling, floating hands, legs, extra cast, costume drift, plane redesign, text, HUD, or camera drift.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
