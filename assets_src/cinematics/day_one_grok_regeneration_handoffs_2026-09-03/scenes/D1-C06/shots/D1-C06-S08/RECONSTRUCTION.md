# D1-C06-S08 — Rumi thanks Roshan and opens her arms

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C06_rumi_swim.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C06_rumi_swim.mp4): frames 0–144 depict swimming rather than the required thanks and invitation beat.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Rumi places one hand over her heart and gives one warm speaking gesture. Every changed frame is a new complete flattened image. |
| 048–107 | She opens both arms toward roshan while both bodies stay separate. Every changed frame is a new complete flattened image. |
| 108–144 | She holds the clear invitation. Every changed frame is a new complete flattened image. |

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
