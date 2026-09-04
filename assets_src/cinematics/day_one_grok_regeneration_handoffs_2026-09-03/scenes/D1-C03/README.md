# D1-C03 selective regeneration — Bubble Bathroom — Dirty Entry

> `ARCHIVE_COMPLETE`: true (source archive)  
> `REGENERATION_GUIDE_COMPLETE`: true  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

[Open the immutable source visual archive](https://github.com/Ebonyks/mermaid-roshan-reef/tree/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1). This repair guide changes no approved source art. It does supersede a source beat when that beat conflicts with the current implemented event.

## Implemented-event authority

- `scripts/games/day_one_bathroom_cleanup.gd`
- one dirty tub, one separate swimming bunny, an authorized tool basket, and two later live cleaning gestures.
- Release MP4s, old MP4s, boards, and runtime captures are evidence only; none is an IMAGE binding or delivery frame.

## New release decision

| Released shot | Verdict | Exact finding | Action |
|---|---|---|---|
| D1-C03-S02 ([C03_S02_v1_dirty_bathroom_threshold_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C03_S02_v1_dirty_bathroom_threshold_REGEN.mp4), [C03_S02_v1_threshold_cross_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C03_S02_v1_threshold_cross_REGEN.mp4)) | `REGENERATE` | Frames 000–144 both variants: Neither variant establishes the doorway. One starts mid-room and ends seated by the sink; the other begins inside the bathtub and crosses the tub instead of the threshold. | Start with the entrance readable; cross fully inside, look tub-to-sink, and preserve the single-tub orientation. |
| D1-C03-S03 ([C03_S03_v1_swimming_bunny_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C03_S03_v1_swimming_bunny_REGEN.mp4)) | `REGENERATE` | Frames 000–144: The swimmer is coherent, but Roshan is a black silhouette/substitute and the bunny mostly holds instead of paddling visibly. | Use approved Roshan at frame edge and one weak-but-safe paddling swimmer in murky water. |
| D1-C03-S04 ([C03_S04_v1_precontact_tools_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C03_S04_v1_precontact_tools_REGEN.mp4)) | `REGENERATE` | Frames 000–144 swimmer absent; 060–144 premature contact: The required swimmer disappears and Roshan advances into scrub-brush contact rather than stopping at the pre-contact seam. | Keep swimmer, tub, sink, tools, and grime; stop Roshan's hand visibly before the nearest tool. |

## Accepted from the new release for rough motion

- None.

## Earlier rough references still retained

- [C03_S01_v2_empty_dirty_bath.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C03_S01_v2_empty_dirty_bath.mp4) — retain as rough reference.

## Regenerate — complete active queue

| Shot | Replacement | Card | Reconstruction |
|---|---|---|---|
| D1-C03-S02 | Roshan crosses the dirty-bathroom threshold | [D1-C03-S02 card](shots/D1-C03-S02/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C03-S02/RECONSTRUCTION.md) |
| D1-C03-S03 | Swimming bunny in the dirty tub | [D1-C03-S03 card](shots/D1-C03-S03/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C03-S03/RECONSTRUCTION.md) |
| D1-C03-S04 | Pre-contact tool resolve | [D1-C03-S04 card](shots/D1-C03-S04/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C03-S04/RECONSTRUCTION.md) |

## Reject as continuity authority

- [C03_bunny_discover.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/blob/5ca170e11c77ea55c3224f9f275b94b8fd62ca36/clips/C03_bunny_discover.mp4)

## Operator gate

1. Open the linked source archive and the reconstruction page for the selected shot.
2. Supply the missing human-approved, clean, HUD-free IMAGE_1 named in the DRAFT card.
3. Bind only the two to four planned images; never bind storyboards, contact sheets, gameplay captures, or MP4 frames.
4. Paste `PROMPT.txt` unchanged unless the accepted endpoint requires a purely positional clarification.
5. Generate one shot only. Submit its full-frame endpoint for Sol/human approval before the next continuous shot.

The loose audit accepts coherent clips for assembly without pretending they are final delivery. This page lists every remaining regeneration card for the scene and no accepted card. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.
