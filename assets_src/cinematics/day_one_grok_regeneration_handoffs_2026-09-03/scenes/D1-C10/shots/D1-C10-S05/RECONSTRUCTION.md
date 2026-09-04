# D1-C10-S05 — Blank awakened desk hand-gap seam

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C10_S05_v1_before_play_OFFICIAL.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C10_S05_v1_before_play_OFFICIAL.mp4): frames 0–144 hide too much of Roshan behind the desk and weaken the hand gap.
- [C10_S05_v1_before_play.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C10_S05_v1_before_play.mp4): frames 0–144 use a less reliable room/character composition.
- [C10_S05_v2_before_play.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C10_S05_v2_before_play.mp4): frames 0–144 do not preserve the exact blank-desk seam.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Show the awakened but blank rectangular center desk with roshan smiling at frame edge. Every changed frame is a new complete flattened image. |
| 048–107 | Roshan raises one hand toward the desk without touching. Every changed frame is a new complete flattened image. |
| 108–144 | Hold a clear ui-free hand gap before gameplay. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | runtime-locked clean Art Room | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/location/room_craft_room_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | fixture and desk topology | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/location/ART_ROOM_FIXTURE_IDENTITY_SHEET.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Roshan makes one pre-touch hand raise.
- Must not move: blank desk, front room geometry, Roshan face/body, fixture order, and UI-free frame.
- End state: the blank desk is awake and Roshan's hand remains visibly short of contact.
- Reject: no customizer UI, bubbles, pointer hand, text, completed design, attack effects, extra limb, fade, desk transformation, room drift, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
