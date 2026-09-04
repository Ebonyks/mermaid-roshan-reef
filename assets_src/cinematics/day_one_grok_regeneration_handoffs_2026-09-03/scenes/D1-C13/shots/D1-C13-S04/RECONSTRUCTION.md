# D1-C13-S04 — Rumi's contained rinse

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C13_S04_v1_rumi_rinse.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C13_S04_v1_rumi_rinse.mp4): strongest motion reference, but frames 0–144 are 1264×720 and need fixed arena/identity reconstruction.
- [C13_S04_v2_rumi_rinse.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C13_S04_v2_rumi_rinse.mp4): frames 48–144 drift Rumi/arena relationships and are 1264×720.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–031 | Rumi sends one low contained violet-and-rainbow water ribbon around grand puff's base. Every changed frame is a new complete flattened image. |
| 032–071 | The rinse clears the final grime without creating a basin or changing the arena. Every changed frame is a new complete flattened image. |
| 072–095 | Rumi and grand puff settle separately around one small prismatic cradle. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | approved arena geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/location/DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png |
| IMAGE_2 | Rumi identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/characters/rumi_rumi_full_body_identity.png |
| IMAGE_3 | Grand Puff identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/characters/grand_puff_BOSS_DUST_BUNNY_IDENTITY.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one contained water-ribbon rinse clears the final grime.
- Must not move: arena ring, platform, lamps, Grand Puff topology, Rumi adult identity, braid, clothes, continuous tail, and prismatic cradle.
- End state: Grand Puff is fully clean and friendly beside one small prismatic cradle; no rainbow bunny is visible yet.
- Reject: no Roshan, Daddy, Baby Eagle, Mermaid Pool conversion, basin, morphing, merged tails, extra limbs, arena change, early bunny, attack, defeat, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
