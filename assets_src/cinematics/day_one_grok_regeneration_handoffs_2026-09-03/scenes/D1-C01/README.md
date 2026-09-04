# D1-C01 selective regeneration — Lagoon Landing and Castle Approach

> `ARCHIVE_COMPLETE`: true (source archive)  
> `REGENERATION_GUIDE_COMPLETE`: true  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

[Open the immutable source visual archive](https://github.com/Ebonyks/mermaid-roshan-reef/tree/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c01_lagoon_landing_castle_approach_visual_v1). This repair guide changes no approved source art. It does supersede a source beat when that beat conflicts with the current implemented event.

## Implemented-event authority

- `scripts/day_one_director.gd`
- arrival media precedes the dirty-castle discovery; the lagoon handoff must preserve Roshan, Daddy, the stationary plane, and the closed castle.
- Release MP4s, old MP4s, boards, and runtime captures are evidence only; none is an IMAGE binding or delivery frame.

## New release decision

| Released shot | Verdict | Exact finding | Action |
|---|---|---|---|
| D1-C01-S02 ([C01_S02_v1_dock_handoffer_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C01_S02_v1_dock_handoffer_REGEN.mp4)) | `REGENERATE` | Frames 000–144: Daddy is already outside and offering at frame 0; the required plane exit, turn, and Roshan-from-doorway handoff never occur. | Rebuild Daddy exit → offer → Roshan hand contact → stable two-character endpoint. |
| D1-C01-S03 ([C01_S03_v1_handinhand_castle_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C01_S03_v1_handinhand_castle_REGEN.mp4)) | `ACCEPT_MOTION_REFERENCE` | Frames none blocking: The paired travel, identities, tails, castle approach, and closed-door endpoint remain coherent; loss of the dock during frames 000–024 is an acceptable cut. | Retain this release clip for rough assembly only. |

## Accepted from the new release for rough motion

- [C01_S03_v1_handinhand_castle_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C01_S03_v1_handinhand_castle_REGEN.mp4) — retained as motion/editorial reference only; `DELIVERY_ACCEPTED` remains false.

## Earlier rough references still retained

- [C01_S01_v1_dock.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C01_S01_v1_dock.mp4) — retain as rough reference.
- [C01_S04_v1_castle_doors.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C01_S04_v1_castle_doors.mp4) — retain as rough reference.

## Regenerate — complete active queue

| Shot | Replacement | Card | Reconstruction |
|---|---|---|---|
| D1-C01-S02 | Daddy offers his hand on the dock | [D1-C01-S02 card](shots/D1-C01-S02/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C01-S02/RECONSTRUCTION.md) |

## Operator gate

1. Open the linked source archive and the reconstruction page for the selected shot.
2. Supply the missing human-approved, clean, HUD-free IMAGE_1 named in the DRAFT card.
3. Bind only the two to four planned images; never bind storyboards, contact sheets, gameplay captures, or MP4 frames.
4. Paste `PROMPT.txt` unchanged unless the accepted endpoint requires a purely positional clarification.
5. Generate one shot only. Submit its full-frame endpoint for Sol/human approval before the next continuous shot.

The loose audit accepts coherent clips for assembly without pretending they are final delivery. This page lists every remaining regeneration card for the scene and no accepted card. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.
