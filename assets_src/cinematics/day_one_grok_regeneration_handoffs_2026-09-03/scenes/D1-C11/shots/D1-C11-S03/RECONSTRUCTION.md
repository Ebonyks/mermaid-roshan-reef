# D1-C11-S03 — Coherent Main Hall-to-arena threshold

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C11_S03_door_opens_arena.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C11_S03_door_opens_arena.mp4): frames 48–144 land in a pearl-hall-like alternate space rather than the approved arena.
- [C11_S03_v1_door_open_arena.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C11_S03_v1_door_open_arena.mp4): frames 0–144 do not preserve a coherent hall-door-to-arena orientation.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | The exact boss door opens once from the accepted hall endpoint. Every changed frame is a new complete flattened image. |
| 048–107 | The approved octagonal arena appears with coherent floor, walls, depth, and entry orientation. Every changed frame is a new complete flattened image. |
| 108–144 | Roshan stays at the threshold while the camera stops on the empty landing zone. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | Main Hall door-side layout | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/location/main_hall_screen_b_room_led_master.png |
| IMAGE_2 | approved arena geography | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/location/DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png |
| IMAGE_3 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/characters/roshan_roshan_base.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: gentle push-in.
- Must move: one door opens and one coherent arena volume is revealed.
- Must not move: hall-door proportions, arena ring, walls, lamps, central platform, landing zone, and Roshan threshold position.
- End state: the empty arena landing zone is clearly framed beyond the open door.
- Reject: no Grand Puff yet, unrelated room, giant void, dark horror, geography jump, arena redesign, Roshan entering center, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
