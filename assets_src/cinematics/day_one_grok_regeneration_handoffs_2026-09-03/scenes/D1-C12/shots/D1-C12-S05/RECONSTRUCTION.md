# D1-C12-S05 — Post-friendship arena vignette

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C12_S05_v1_grand_puff_friend.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C12_S05_v1_grand_puff_friend.mp4): frames 0–144 use the wrong Main Hall-like location and do not inherit the arena friendship state.
- [C12_S05_v2_grand_puff_friend.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C12_S05_v2_grand_puff_friend.mp4): frames 0–144 fail arena and new-friend continuity.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Grand puff sits upright with the newly friendly small rainbow bunny in the accepted post-friendship arena. Every changed frame is a new complete flattened image. |
| 048–107 | Grand puff gives one soft laugh and squash while the bunny makes one tiny grateful bounce. Every changed frame is a new complete flattened image. |
| 108–144 | Both settle as separate friendly bodies. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | accepted D1-C13-S05 endpoint | missing_approved_shot_opening_frame: accepted final arena state from D1-C13-S05 |
| IMAGE_2 | Grand Puff identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c12_restored_castle_finale_visual_v1/handoff_art/characters/grand_puff_BOSS_DUST_BUNNY_IDENTITY.png |
| IMAGE_3 | approved rainbow bunny identity | missing_human_approved_authority: dedicated approved rainbow dust bunny identity; the generated concept and MP4 are not pixel authorities |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one soft Grand Puff laugh/squash and one tiny bunny bounce.
- Must not move: arena topology, Grand Puff identity, rainbow bunny identity, positions, floor contacts, and friendly state.
- End state: Grand Puff rests upright smiling with exactly two teeth while the separate rainbow bunny settles beside him.
- Reject: no Main Hall, defeat, injury, attack, smoke, boss UI, invented cleanup, morphing, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
