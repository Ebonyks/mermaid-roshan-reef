# D1-C08-S06 — Safe Baby Eagle wing blast

> `STATUS`: DRAFT  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

## Why this shot is being rebuilt

- [C08_S06_v1_wing_blast.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C08_S06_v1_wing_blast.mp4): frames 48–144 jump to a clean bright room without readable airflow causality.
- [C08_S06_v2_wing_blast.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C08_S06_v2_wing_blast.mp4): frames 48–107 form a tornado-like ring and frames 108–144 alter the clean-room read.

Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.

## Full-frame reconstruction map

| Output frames | Required full-frame content |
|---|---|
| 000–047 | One standing baby eagle plants both feet and prepares both wings. Every changed frame is a new complete flattened image. |
| 048–107 | It performs one broad soft wing blast and only dust plus lightweight clutter move toward storage. Every changed frame is a new complete flattened image. |
| 108–144 | The last dust clears while all characters remain anchored. Every changed frame is a new complete flattened image. |

## Binding plan

| Slot | Job | Status / source |
|---|---|---|
| IMAGE_1 | Stuffie Room geography | missing_approved_shot_opening_frame: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/location/room_playroom_background.png |
| IMAGE_2 | standing Baby Eagle identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/baby_eagle_standing_BABY_EAGLE_STANDING_IDENTITY.png |
| IMAGE_3 | four-bunny identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/playroom_bunny_PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png |
| IMAGE_4 | Roshan identity | approved_source_authority_available: https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/handoff_art/characters/roshan_roshan_base.png |

IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.

## Locked result

- Camera: locked.
- Must move: one safe wing blast clears integrated dust and light clutter.
- Must not move: walls, furniture, Roshan, exactly four bunnies, one eagle, room topology, and floor contacts.
- End state: the clean established room is revealed with all cast safe and anchored.
- Reject: no tornado, character lift, violent impact, magic-only flash, furniture relocation, topology change, duplicate cast, text, or HUD.
- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.

## Files

- [Paste-ready Grok prompt](PROMPT.txt)
- [Machine-readable DRAFT shot card](SHOT_PACKET.json)
