# B-roll: the same story, richer coverage

Owner commission: redraw the existing shots from different angles so the edit can move between complementary views. This is a companion to [repaired V2](https://github.com/Ebonyks/mermaid-roshan-reef/tree/0b26557f9500983f7ba2eb670df072dffd352779/design/cinematics/v2), not another full retelling and not a rewrite of game events.

Start with [START_GROK.txt](START_GROK.txt). [PUBLICATION.json](PUBLICATION.json) contains immutable private visual archive and verification links. The public packet is navigation and shot direction; the **private packet includes the actual images**. Login failure must be reported as `HANDOFF_BLOCKED`, not worked around with invented references.

## Included

- **36 A/B pairs:** one fresh B01 camera proposal for every V2 shot, including Day One and the Chapter 2 finale. [PAIRS.json](PAIRS.json) is the exact mapping.
- **10 newly generated candidate storyboard sheets / 108 illustrated beats:** start, contact/action and endpoint for every shot, plus 36 historical boards preserved as source evidence.
- **41 actual existing visual references:** room masters, main characters, props, known camera crops and endpoint references, copied byte-for-byte into the private archive.
- Each `shots/<B-ID>/` has `PLAN.json`, `SHOT_CARD.txt`, `FIRST_FRAME_BRIEF.txt` and a short `PROMPT.txt` with sound direction. Original A plans and canon are frozen alongside them.
- [Editorial guide](EDITORIAL_GUIDE.md), [board QC](BOARD_QC.json), [queue](QUEUE.json), [return template](RESHOOT_RETURN_TEMPLATE.json) and a persistent [reshoot protocol](reshoots/README.md).
- Private `index.html` gives an all-shot visual review gallery. View it from a downloaded private packet; GitHub displays individual PNGs directly. The public HTML copy cannot display private images by itself.

Owner Rumi correction: [RUMI_CORRECTION.json](RUMI_CORRECTION.json) replaces only her cake/candle appearances with `LAWN_A_v3` and `LAWN_B_v3`. Use the actual adult Rumi reference, not the rejected v2 depictions. Other scene direction is retained; corrected artwork still awaits owner review.

## Creative direction

Use low contact-level views, high obliques, three-quarter ensembles and over-the-shoulder inserts. Keep near/mid/far room anchors so the spaces have depth. The camera stays locked within each 4-second generation; variety comes from separate approved setups. Do not manufacture depth by mirroring, digitally cropping, or animating static layers.

The first six recommended reviews cover tub cleaning, craft pickup, the small stocked craft worktable, Eagle rescue, cooperative boss cleaning and the clean-hall group payoff. A source HOLD or exhausted attempt cap still blocks its dependent B-roll. Group/camera approval does not substitute for the owner's approval of each complete first-frame candidate.

## Acceptance limits

The new boards are **illustrated planning concepts, not first-frame candidates or approved new architecture**. Nine corrective redraws were made across six board families; remaining panel-specific issues are listed in `BOARD_QC.json`. In particular, do not copy inferred room corners, modified prop forms, panel-to-panel camera changes, or compressed staging into an execution opening. The actual source references and exact state plan control.

`ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` are separate. The archive can be published and checked while openings remain unapproved. None of these I2V jobs is currently generation-ready or delivery-accepted. Actual frame-by-frame provenance and human/device review remain independent blocking gates. `MA-VIS-006` remains open.

No runtime art, saved progress, protected original, A-roll attempt history or game integration changes are part of this handoff. Local files are staging only; use the immutable GitHub packet and verification receipt.
