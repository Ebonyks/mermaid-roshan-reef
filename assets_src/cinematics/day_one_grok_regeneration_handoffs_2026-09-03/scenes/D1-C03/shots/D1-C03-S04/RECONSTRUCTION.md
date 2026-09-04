# D1-C03-S04 — Pre-contact tool resolve

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C03_S04_v1_tool_reach.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C03_S04_v1_tool_reach.mp4): frames 48–144 do not preserve a clear pre-contact endpoint.
- [C03_S04_v1_tools_resolve.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C03_S04_v1_tools_resolve.mp4): frames 0–47 begin from an unstable dirty-room composition and frames 108–144 leave the tool gap ambiguous.
- [C03_S04_v2_tools_resolve.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C03_S04_v2_tools_resolve.mp4): frames 48–144 drift tool/room relationships during the resolve.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Roshan follows her gaze from the swimmer toward the dirty sink and approved tools. Every changed frame is a new complete flattened image. |
| 048–107 | She reaches toward the nearest approved tool without changing the room state. Every changed frame is a new complete flattened image. |
| 108–144 | Her hand stops in a clean visible gap before contact. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty bathroom layout | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/location/room_bubble_bath_dirty_day_one.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | approved tool group | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/handoff_art/objects/cleanup_basket.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: subtle push-in.
- Must move: Roshan makes one gaze-and-reach action.
- Must not move: dirty room, murky tub, swimmer, sink, tools, grime, and character anatomy.
- End state: Roshan holds a determined pre-contact hand gap while all dirt remains.
- Reject: no scrub, tool teleport, UI pointer, extra supplies, room redesign, cleanup, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
