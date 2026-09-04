# D1-C08 selective regeneration — Stuffie Room — Two-Pin Rescue and Baby Eagle Departure

> `ARCHIVE_COMPLETE`: true (source archive)  
> `REGENERATION_GUIDE_COMPLETE`: true  
> `GENERATION_READY`: false  
> `DELIVERY_ACCEPTED`: false

[Open the immutable source visual archive](https://github.com/Ebonyks/mermaid-roshan-reef/tree/076661afb9e092627eb5dfae7c39fecb27463892/assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1). This repair guide changes no approved source art. It does supersede a source beat when that beat conflicts with the current implemented event.

## Implemented-event authority

- `scripts/arena/castle_rooms_25d.gd`
- Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens.
- Release MP4s, old MP4s, boards, and runtime captures are evidence only; none is an IMAGE binding or delivery frame.

## New release decision

| Released shot | Verdict | Exact finding | Action |
|---|---|---|---|
| D1-C08-S02 ([C08_S02_v1_left_basket_ears_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S02_v1_left_basket_ears_REGEN.mp4)) | `REPLACE_WITH_GAME_EVENT` | Frames 000–144: Basket warnings do not occur in gameplay; the bunny body is already outside the basket. | Replace with corrected C08-S01: Roshan approaches the exact two-pin rescue state. |
| D1-C08-S03 ([C08_S03_v1_right_basket_ears_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S03_v1_right_basket_ears_REGEN.mp4)) | `REPLACE_WITH_GAME_EVENT` | Frames 000–144: The opposite-basket warning is also invented and exposes a full bunny rather than an ears-only cue. | Replace with corrected C08-S02: Roshan clears the left rescue pin after physical contact. |
| D1-C08-S04 ([C08_S04_v1_four_bunnies_emerge_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S04_v1_four_bunnies_emerge_REGEN.mp4)) | `REPLACE_WITH_GAME_EVENT` | Frames 000–144; count failure 048–144: The game has two rescue pins, not four emerging basket bunnies; the rendered count also grows ambiguous beyond four. | Replace with corrected C08-S03: reframe the still-pinned right bunny after the left pin clears. |
| D1-C08-S06 ([C08_S06_v1_wing_blast_clean_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S06_v1_wing_blast_clean_REGEN.mp4)) | `REPLACE_WITH_GAME_EVENT` | Frames 000–144: Baby Eagle never performs a wing-blast cleanup. Gameplay completes when Roshan clears the second pin. | Replace with corrected C08-S04: Roshan clears the right pin and the room resolves from that contact. |
| D1-C08-S07 ([C08_S07_v1_clean_endpoint_REGEN.mp4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-regen-motion-ref-2026-09-03/C08_S07_v1_clean_endpoint_REGEN.mp4)) | `REPLACE_WITH_GAME_EVENT` | Frames 000–144; side-wall drift 048–144: The one-Eagle/four-bunny endpoint is not a game state and the room projection drifts into invented side-wall geometry. | Replace with corrected C08-S05: Baby Eagle thanks Roshan, rises, and departs from the clean room before the picker UI. |

## Accepted from the new release for rough motion

- None.

## Replaced with implemented events

- D1-C08-S02 → D1-C08-S01: Replace with corrected C08-S01: Roshan approaches the exact two-pin rescue state.
- D1-C08-S03 → D1-C08-S02: Replace with corrected C08-S02: Roshan clears the left rescue pin after physical contact.
- D1-C08-S04 → D1-C08-S03: Replace with corrected C08-S03: reframe the still-pinned right bunny after the left pin clears.
- D1-C08-S06 → D1-C08-S04: Replace with corrected C08-S04: Roshan clears the right pin and the room resolves from that contact.
- D1-C08-S07 → D1-C08-S05: Replace with corrected C08-S05: Baby Eagle thanks Roshan, rises, and departs from the clean room before the picker UI.

## Earlier rough references still retained

- None. Existing candidates may inform motion only; none are retained as the preferred rough shot.

## Regenerate — complete active queue

| Shot | Replacement | Card | Reconstruction |
|---|---|---|---|
| D1-C08-S01 | Roshan approaches the two-pin rescue | [D1-C08-S01 card](shots/D1-C08-S01/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C08-S01/RECONSTRUCTION.md) |
| D1-C08-S02 | Roshan clears the left rescue pin | [D1-C08-S02 card](shots/D1-C08-S02/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C08-S02/RECONSTRUCTION.md) |
| D1-C08-S03 | Roshan reframes the remaining right pin | [D1-C08-S03 card](shots/D1-C08-S03/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C08-S03/RECONSTRUCTION.md) |
| D1-C08-S04 | Roshan clears the right pin and completes the room | [D1-C08-S04 card](shots/D1-C08-S04/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C08-S04/RECONSTRUCTION.md) |
| D1-C08-S05 | Baby Eagle thanks Roshan and departs | [D1-C08-S05 card](shots/D1-C08-S05/SHOT_PACKET.json) | [weak frames and rebuild](shots/D1-C08-S05/RECONSTRUCTION.md) |

## Operator gate

1. Open the linked source archive and the reconstruction page for the selected shot.
2. Supply the missing human-approved, clean, HUD-free IMAGE_1 named in the DRAFT card.
3. Bind only the two to four planned images; never bind storyboards, contact sheets, gameplay captures, or MP4 frames.
4. Paste `PROMPT.txt` unchanged unless the accepted endpoint requires a purely positional clarification.
5. Generate one shot only. Submit its full-frame endpoint for Sol/human approval before the next continuous shot.

The loose audit accepts coherent clips for assembly without pretending they are final delivery. This page lists every remaining regeneration card for the scene and no accepted card. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.
