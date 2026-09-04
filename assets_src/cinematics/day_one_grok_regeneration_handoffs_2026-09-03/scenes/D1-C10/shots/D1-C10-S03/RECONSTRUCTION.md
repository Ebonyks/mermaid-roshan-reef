# D1-C10-S03 — Clean Art Room reveal with readable Roshan

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C10_S03_clean_reveal.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C10_S03_clean_reveal.mp4): frames 48–144 obscure Roshan behind or beneath the center desk.
- [C10_S03_v1_clean_reveal_OFFICIAL.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C10_S03_v1_clean_reveal_OFFICIAL.mp4): frames 48–144 leave Roshan insufficiently readable at child scale.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Begin with three grime cards gone, four supplies stored once, and roshan fully readable at runtime scale. Every changed frame is a new complete flattened image. |
| 048–107 | Pull back once to reveal the complete clean front layout. Every changed frame is a new complete flattened image. |
| 108–144 | Hold before desk activation. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | runtime-locked Art Room front projection | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/location/room_craft_room_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | fixture topology | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/location/ART_ROOM_FIXTURE_IDENTITY_SHEET.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: small pullback.
- Must move: one restrained clean-room pullback.
- Must not move: rectangular desk, two counters, shelves, two windows, two columns, chandelier, Roshan identity, and blank desk state.
- End state: the complete clean room and fully readable Roshan are stable in one front projection.
- Reject: no Roshan hidden under furniture, doorway, reverse view, extra supplies, completed painting, dust bunny, desk transformation, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
