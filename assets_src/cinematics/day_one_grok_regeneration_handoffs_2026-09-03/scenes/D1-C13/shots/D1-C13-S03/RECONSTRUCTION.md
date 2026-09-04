# D1-C13-S03 — Baby Eagle's safe wing lift

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C13_S03_v1_eagle_lift.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C13_S03_v1_eagle_lift.mp4): frames 48–144 collapse Grand Puff into a ring/bowl-like form and are 1264×720.
- [C13_S03_v2_eagle_lift.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C13_S03_v2_eagle_lift.mp4): useful motion reference, but frames 0–144 need exact eagle count, boss topology, and native 1280×720.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–031 | Exactly one baby eagle plants both feet and opens both wings. Every changed frame is a new complete flattened image. |
| 032–071 | One symmetrical soft wing blast lifts only residual dust toward the arena perimeter. Every changed frame is a new complete flattened image. |
| 072–095 | The eagle folds its wings and settles without moving grand puff. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | approved arena geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/location/DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png |
| IMAGE_2 | standing Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/characters/baby_eagle_standing_BABY_EAGLE_STANDING_IDENTITY.png |
| IMAGE_3 | Grand Puff identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/characters/grand_puff_BOSS_DUST_BUNNY_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one safe symmetrical wing blast lifts dust.
- Must not move: arena ring, central platform, Grand Puff, one eagle, floor contacts, and the final dusty shell.
- End state: one Baby Eagle rests with folded wings and the final dusty shell remains isolated.
- Reject: no Roshan, Daddy, Rumi, rainbow bunny, duplicate eagle, displaced character, tornado, morphing, clone, extra limb, arena change, attack, defeat, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
