# D1-C11-S04 — Grand Puff lands in the fixed arena

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C11_grand_puff_reveal.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C11_grand_puff_reveal.mp4): frames 0–144 use an unstable arena/hall context and do not fully lock Grand Puff topology.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Grand puff makes one soft landing squash in the approved empty arena. Every changed frame is a new complete flattened image. |
| 048–107 | He settles upright with three tiers, symmetrical spiral ears, pearl paws, and exactly two small teeth. Every changed frame is a new complete flattened image. |
| 108–144 | One lavender four-point forehead sparkle gives a playful vulnerability pulse. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | approved arena geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/handoff_art/location/DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png |
| IMAGE_2 | Grand Puff identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/characters/grand_puff_BOSS_DUST_BUNNY_IDENTITY.png |
| IMAGE_3 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/handoff_art/characters/roshan_roshan_base.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Grand Puff lands, squashes once, and settles.
- Must not move: arena topology, landing zone, Roshan's safe edge position, Grand Puff tiers, ears, paws, face, and teeth.
- End state: Grand Puff is upright, cute, smiling, and centered in the fixed arena.
- Reject: no pearl hall, smoke body, attack, sharp teeth, injury, defeat, title, text, HUD, or arena morph.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
