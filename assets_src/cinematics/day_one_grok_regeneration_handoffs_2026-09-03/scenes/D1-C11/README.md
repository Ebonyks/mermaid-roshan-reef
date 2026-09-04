# D1-C11 selective regeneration — Boss Door and Grand Puff Reveal

> `ARCHIVE_COMPLETE`: true (source archive)  
> `REGENERATION_GUIDE_COMPLETE`: true  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

[Open the immutable source visual archive](https://github.com/Ebonyks/mermaid-roshan-reef/tree/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1). This repair guide changes no approved source art. It does supersede a source beat when that beat conflicts with the current implemented event.

## Implemented-event authority

- `scripts/day_one_director.gd and scripts/games/dust_boss.gd`
- all four rooms arm the boss door; the empty octagonal arena precedes Grand Puff's soft showing.
- Release MP4s, old MP4s, boards, and runtime captures are evidence only; none is an IMAGE binding or delivery frame.

## New release decision

| Released shot | Verdict | Exact finding | Action |
|---|---|---|---|
| D1-C11-S02 ([C11_S02_v1_boss_door_approach_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C11_S02_v1_boss_door_approach_REGEN.mp4)) | `ACCEPT_MOTION_REFERENCE` | Frames minor 132–144: Main Hall geometry, Roshan, closed door, and approach are coherent; only the final hand reaches the handle instead of stopping just before it. | Retain for rough assembly; require a clean pre-contact endpoint for final delivery. |
| D1-C11-S03 ([C11_S03_v1_door_open_arena_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C11_S03_v1_door_open_arena_REGEN.mp4)) | `ACCEPT_MOTION_REFERENCE` | Frames none blocking: The door opens into the octagonal arena, Roshan stays at threshold, and the landing zone remains empty; exact predecessor-frame inheritance is unproven. | Retain for rough assembly; audit the final seam independently. |
| D1-C11-S04 ([C11_S04_v1_grand_puff_lands_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C11_S04_v1_grand_puff_lands_REGEN.mp4)) | `REGENERATE` | Frames 006–071 impact/topology; 066–144 expression: A dark crater, oversized cloud, and pancake-flat squash destabilize Grand Puff; the recovered face remains menacing and the vulnerability sparkle does not read. | Use a soft vertical landing, at most ten-percent squash, full three-tier recovery by 2.5 seconds, cute two-teeth face, and one four-point sparkle pulse. |

## Accepted from the new release for rough motion

- [C11_S02_v1_boss_door_approach_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C11_S02_v1_boss_door_approach_REGEN.mp4) — retained as motion/editorial reference only; `DELIVERY_ACCEPTED` remains false.
- [C11_S03_v1_door_open_arena_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C11_S03_v1_door_open_arena_REGEN.mp4) — retained as motion/editorial reference only; `DELIVERY_ACCEPTED` remains false.

## Earlier rough references still retained

- [C11_S01_route_lights.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C11_S01_route_lights.mp4) — retain as rough reference.

## Regenerate — complete active queue

| Shot | Replacement | Card | Reconstruction |
|---|---|---|---|
| D1-C11-S04 | Grand Puff lands in the fixed arena | [D1-C11-S04 card](shots/D1-C11-S04/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C11-S04/RECONSTRUCTION.md) |

## Reject as continuity authority

- [C11_S01_v1_routes_converge.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C11_S01_v1_routes_converge.mp4)

## Operator gate

1. Open the linked source archive and the reconstruction page for the selected shot.
2. Supply the missing human-approved, clean, HUD-free IMAGE_1 named in the DRAFT card.
3. Bind only the two to four planned images; never bind storyboards, contact sheets, gameplay captures, or MP4 frames.
4. Paste `PROMPT.txt` unchanged unless the accepted endpoint requires a purely positional clarification.
5. Generate one shot only. Submit its full-frame endpoint for Sol/human approval before the next continuous shot.

The loose audit accepts coherent clips for assembly without pretending they are final delivery. This page lists every remaining regeneration card for the scene and no accepted card. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.
