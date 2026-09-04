# D1-C07-S04 — One supported swinging dust bunny

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C07_S04_v1_swing_bunny.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S04_v1_swing_bunny.mp4): frames 48–144 make support contact weak or unclear.
- [C07_S04_v2_swing_bunny.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S04_v2_swing_bunny.mp4): frames 48–144 lose the rope and turn the bunny into a floating trail.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Show exactly one intact lavender playroom dust bunny attached to the established support. Every changed frame is a new complete flattened image. |
| 048–107 | The bunny makes one small gentle swing with visible rope contact. Every changed frame is a new complete flattened image. |
| 108–144 | The swing settles and one harmless dust trace falls. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | playroom bunny identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |
| IMAGE_3 | support and nook topology | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/objects/room_playroom_item_stuffie_nook.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: slow pendulum-follow.
- Must move: one supported bunny swings and settles.
- Must not move: dirty room, basket, support, rope contact, bunny face, ears, body, and curl silhouette.
- End state: one bunny remains safely attached and settled.
- Reject: no second bunny, smoke creature, floating trail, detached rope, clone, scary expression, rescue, cleanup, room rotation, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
