# D1-C09-S05 — Art Room pre-contact cleaning seam

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C09_S05_resolve_brush.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C09_S05_resolve_brush.mp4): frames 48–144 begin to read as active cleaning and fail to preserve a clean pre-contact seam.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Roshan looks across the left, center, and right grime cards. Every changed frame is a new complete flattened image. |
| 048–107 | She raises the approved magic cleaning brush toward them without touching. Every changed frame is a new complete flattened image. |
| 108–144 | She stops with a visible hand-to-tool gap and all grime present. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | runtime-locked Art Room front projection | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/location/room_craft_room_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | fixture topology | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/handoff_art/location/ART_ROOM_FIXTURE_IDENTITY_SHEET.png |
| IMAGE_4 | magic cleaning brush identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/objects/magic_cleaning_brush.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Roshan makes one pre-contact raise.
- Must not move: front projection, all fixtures, three grime cards, Roshan anatomy, brush identity, and dirty state.
- End state: all three grime cards remain and Roshan is ready for the next cleaning shot.
- Reject: no brush contact, grime removal, desk activation, reverse angle, extra limb, new fixture, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
