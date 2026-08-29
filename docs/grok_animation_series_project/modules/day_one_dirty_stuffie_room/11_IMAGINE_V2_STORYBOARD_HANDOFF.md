# Imagine V2 storyboard handoff

This supersedes the older multi-shot prompt grouping for new Grok Imagine work.
It follows `design/templates/IMAGINE_SHOT_CARD_V1.md`: one movie per archive
packet, one shot per generation job, and only two to four role-labeled images
per job.

## Regenerated storyboards

- Movie A, discovery: `assets_src/cinematics/day_one_stuffie_discovery_v2/`
  contains six narrative panels and a 3×2 shot board.
- Movie B, basket wave and clean reveal:
  `assets_src/cinematics/day_one_stuffie_basket_clean_v2/` contains seven
  narrative panels and a 4×2 shot board.

Together the two boards use all ten new dirty-room perspective screenshots.
The final gust returns to the matched front dirty/clean room pair so the causal
rule is unambiguous: all four bunnies fully leave first, and only the trailing
gust replaces the dirty background with the clean background.

### Immutable GitHub handoff

- [Movie A archive packet](https://github.com/Ebonyks/mermaid-roshan-reef/tree/8cfef94c712002c7d5a6586c87a49c9017fdca5b/assets_src/cinematics/day_one_stuffie_discovery_v2)
- [Movie A storyboard](https://github.com/Ebonyks/mermaid-roshan-reef/blob/8cfef94c712002c7d5a6586c87a49c9017fdca5b/assets_src/cinematics/day_one_stuffie_discovery_v2/storyboards/SQ030_DISCOVERY_SHOT_BOARD.png)
- [Movie B archive packet](https://github.com/Ebonyks/mermaid-roshan-reef/tree/8cfef94c712002c7d5a6586c87a49c9017fdca5b/assets_src/cinematics/day_one_stuffie_basket_clean_v2)
- [Movie B storyboard](https://github.com/Ebonyks/mermaid-roshan-reef/blob/8cfef94c712002c7d5a6586c87a49c9017fdca5b/assets_src/cinematics/day_one_stuffie_basket_clean_v2/storyboards/SQ040_BASKET_CLEAN_SHOT_BOARD.png)
- [Imagine shot-card authority](https://github.com/Ebonyks/mermaid-roshan-reef/blob/8cfef94c712002c7d5a6586c87a49c9017fdca5b/design/templates/IMAGINE_SHOT_CARD_V1.md)

GitHub verification at content commit `8cfef94c712002c7d5a6586c87a49c9017fdca5b`
found zero missing files across both manifests and all 80 archived assets. This
is the URL handoff; do not create or upload a ZIP.

## Exact story counts

- Movie A shows one center-light bunny and two separate wing bunnies: three.
- Movie B shows four new bunnies from the baskets: exactly two reach separate
  lights and exactly two land on opposite floor sides.
- Movie B ends with zero bunnies, a clean room, standing bag-free Baby Eagle,
  and Roshan at screen-left.

## What Grok may receive

Do not upload either storyboard board as a visual reference. The boards explain
story order only. Each `shots/<shot_id>/` folder contains:

- `PROMPT.txt`: short, action-first, timed image-to-video direction;
- `SHOT_PACKET_DRAFT.json`: the intended two-to-four image bindings and exact
  blockers.

The draft cards are not executable `SHOT_PACKET.json` files yet. The new guide
requires IMAGE_1 to be an owner-approved, complete, clean, UI-free first frame.
The perspective screenshots are layout candidates, not complete first frames
for character shots. Every binding must also be opened from its immutable
GitHub URL and human accepted before generation.

## Independent status claims

- `ARCHIVE_COMPLETE`: becomes true after the packet content is pushed and its
  immutable GitHub tree and manifest are verified.
- `GENERATION_READY`: false until each shot has its approved first frame and
  accepted two-to-four bindings.
- `DELIVERY_ACCEPTED`: false. Grok image-to-video output remains motion
  reference only under the full-frame cinematic rule.

No ZIP is required or supplied. Use the GitHub packet folders directly.
