# D1-C07-S06 — Exactly one pinned Baby Eagle

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C07_S06_v1_eagle_discover.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S06_v1_eagle_discover.mp4): frames 0–144 do not hold one exact pinned identity and clean reveal state.
- [C07_S06_v1_eagle_pinned.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S06_v1_eagle_pinned.mp4): usable as motion reference, but frames 108–144 still need full identity/topology confirmation.
- [C07_S06_v2_eagle_pinned.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S06_v2_eagle_pinned.mp4): frames 0–144 introduce an unrelated brown animal and identity conflict.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | Show exactly one baby eagle partly concealed under soft grounded room mess. Every changed frame is a new complete flattened image. |
| 048–107 | Roshan moves into concerned eye contact while the bird remains alert, intact, and visibly pinned. Every changed frame is a new complete flattened image. |
| 108–144 | Both settle as roshan resolves to help. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | dirty Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/roshan_roshan_base.png |
| IMAGE_3 | pinned Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/handoff_art/characters/baby_eagle_pinned_BABY_EAGLE_PINNED_STATE.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: Roshan makes eye contact with one pinned bird.
- Must not move: dirty room, clutter contact, bird position, turquoise/yellow/pink identity, beak, two wings, two feet, and Roshan's tail.
- End state: exactly one unharmed Baby Eagle is visibly pinned and Roshan is ready to help.
- Reject: no second bird, brown substitute animal, duplicate body, backpack, crushed anatomy, horror, bunny takeover, cleanup, room change, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
