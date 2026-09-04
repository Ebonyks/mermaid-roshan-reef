# D1-C09-S04 — Exactly three Art Room grime cards

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C09_S04_three_grime_zones.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C09_S04_three_grime_zones.mp4): frames 0–144 introduce the wrong child cast and weaken the fixed three-zone layout.
- [C09_S04_v1_three_grime_OFFICIAL.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C09_S04_v1_three_grime_OFFICIAL.mp4): frames 48–144 do not keep all three grime locations simultaneously readable.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Show the exact post-collection front art room with all four loose supply groups absent. Every changed frame is a new complete flattened image. |
| 048–107 | Exactly three small lavender grime cards remain at the left counter, rectangular center desk, and right counter. Every changed frame is a new complete flattened image. |
| 108–144 | Roshan points once without touching. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | runtime-locked Art Room front projection | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/location/room_craft_room_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | fixture topology | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/location/ART_ROOM_FIXTURE_IDENTITY_SHEET.png |
| IMAGE_4 | grime material | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/objects/grime_desk.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Roshan points and exactly three fixed grime targets remain readable.
- Must not move: two shell windows, two pearl columns, chandelier, shell board, rectangular desk, two curved counters, rear shelves, and front projection.
- End state: exactly three grime cards remain visible at left, center, and right.
- Reject: no fourth target, floor grime, toxic sludge, supply duplicate, cleanup, desk glow, floating objects, side wall, doorway, room rotation, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
