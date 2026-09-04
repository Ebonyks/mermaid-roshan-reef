# D1-C13-S01 — Roshan's final cleaning pass

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C13_S01_v1_roshan_cleanup.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C13_S01_v1_roshan_cleanup.mp4): frames 0–144 are 1264×720 and drift arena/action continuity.
- [C13_S01_v2_roshan_cleanup.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C13_S01_v2_roshan_cleanup.mp4): useful action reference, but frames 48–144 still need exact arena, brush contact, and native 1280×720 reconstruction.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–031 | Roshan holds the approved magic cleaning brush and makes one gentle pass across grand puff's front and near floor. Every changed frame is a new complete flattened image. |
| 032–071 | One localized dusty shell band becomes clean while grand puff compresses playfully without damage. Every changed frame is a new complete flattened image. |
| 072–095 | Roshan and grand puff settle as separate bodies. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | approved arena geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/location/DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | Grand Puff identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/characters/grand_puff_BOSS_DUST_BUNNY_IDENTITY.png |
| IMAGE_4 | magic cleaning brush identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c10_art_room_restored_visual_v1/handoff_art/objects/magic_cleaning_brush.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one physically held brush pass makes one localized clean patch.
- Must not move: octagonal arena, central platform, walls, lamps, Grand Puff topology, Roshan identity, and unaffected dust bands.
- End state: Roshan holds the brush at frame edge and Grand Puff rests centered with one localized clean patch.
- Reject: no Daddy, Rumi, Baby Eagle, rainbow bunny, morphing, clone, merged body, extra limb, topology change, cropped character, attack, defeat, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
