# D1-C07 selective regeneration — Stuffie Room — Dirty Discovery and Two-Pin Reveal

> `ARCHIVE_COMPLETE`: true (source archive)  
> `REGENERATION_GUIDE_COMPLETE`: true  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

[Open the immutable source visual archive](https://github.com/Ebonyks/mermaid-roshan-reef/tree/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1). This repair guide changes no approved source art. It does supersede a source beat when that beat conflicts with the current implemented event.

## Implemented-event authority

- `scripts/arena/castle_rooms_25d.gd`
- one Baby Eagle is visibly held by exactly two rescue pin bunnies; no swing or partial-wing hunt exists.
- Release MP4s, old MP4s, boards, and runtime captures are evidence only; none is an IMAGE binding or delivery frame.

## New release decision

| Released shot | Verdict | Exact finding | Action |
|---|---|---|---|
| D1-C07-S04 ([C07_S04_v1_swinging_bunny_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C07_S04_v1_swinging_bunny_REGEN.mp4)) | `OMIT_SUPERSEDED_EVENT` | Frames 000–144; detachment 108–144: No swinging-bunny event exists in gameplay, and the rendered bunny loses its support before landing on the floor. | Remove this shot from the corrected cut; do not regenerate the invented event. |
| D1-C07-S05 ([C07_S05_v1_partial_wing_trail_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C07_S05_v1_partial_wing_trail_REGEN.mp4)) | `OMIT_SUPERSEDED_EVENT` | Frames 000–144; full reveal 048–144: Gameplay presents one visible Baby Eagle held by two pin bunnies; it does not hide the bird behind a partial-wing trail. | Remove this shot from the corrected cut; do not regenerate the invented event. |
| D1-C07-S06 ([C07_S06_v1_pinned_baby_eagle_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C07_S06_v1_pinned_baby_eagle_REGEN.mp4)) | `REGENERATE` | Frames 000–144: One Eagle is present, but neither of the two required rescue-pin bunnies is visible and the bird becomes free/upright before player action. | Reveal exactly one Baby Eagle visibly held by exactly two distinct pin bunnies; no release yet. |

## Accepted from the new release for rough motion

- None.

## Removed from the corrected game-congruent cut

- D1-C07-S04 — No swinging-bunny event exists in gameplay, and the rendered bunny loses its support before landing on the floor.
- D1-C07-S05 — Gameplay presents one visible Baby Eagle held by two pin bunnies; it does not hide the bird behind a partial-wing trail.

## Earlier rough references still retained

- [C07_S01_v2_empty_dirty_stuffie.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S01_v2_empty_dirty_stuffie.mp4) — retain as rough reference.
- [C07_S02_v2_roshan_enters.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S02_v2_roshan_enters.mp4) — retain as rough reference.

## Regenerate — complete active queue

| Shot | Replacement | Card | Reconstruction |
|---|---|---|---|
| D1-C07-S06 | One Baby Eagle held by exactly two rescue pins | [D1-C07-S06 card](shots/D1-C07-S06/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C07-S06/RECONSTRUCTION.md) |

## Reject as continuity authority

- [C07_S06_v2_eagle_pinned.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C07_S06_v2_eagle_pinned.mp4)

## Operator gate

1. Open the linked source archive and the reconstruction page for the selected shot.
2. Supply the missing human-approved, clean, HUD-free IMAGE_1 named in the DRAFT card.
3. Bind only the two to four planned images; never bind storyboards, contact sheets, gameplay captures, or MP4 frames.
4. Paste `PROMPT.txt` unchanged unless the accepted endpoint requires a purely positional clarification.
5. Generate one shot only. Submit its full-frame endpoint for Sol/human approval before the next continuous shot.

The loose audit accepts coherent clips for assembly without pretending they are final delivery. This page lists every remaining regeneration card for the scene and no accepted card. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.
