# Day One Stuffie Room — two-storyboard Grok handoff

## Purpose

This module adds the Day One Stuffie Room to the Mermaid Roshan animation
series as two separate, short-shot storyboards:

1. `SQ030` — Roshan enters, reacts in shock, notices one Dust Bunny swinging
   from the center light, then discovers sad Baby Eagle on the floor with two
   Dust Bunnies playing on the spread wings.
2. `SQ040` — after the room looks clean and Baby Eagle is standing, exactly
   four new Dust Bunnies spring from the two foreground toy baskets; two reach
   the lights and two land on the floor, then Baby Eagle blows all four away
   with one broad, safe wing gust.

These are separate editorial storyboards, not one oversized generation. Every
shot is six or eight seconds at request time and is trimmed to its authored
duration. No shot exceeds Grok's 15-second ceiling.

The gameplay source and exact accepted art are fixed at commit
`2d5acdb8b496c4a3d27dcd5ebe272fdbdc2af37f`. The same references are copied
into this Grok package so the sequence does not depend on Project memory.

## Read before generating

1. `../../project_guide/00_PROJECT_CONSTITUTION_COPY_PASTE.md`
2. `../../project_guide/01_STYLE_BIBLE.md`
3. `../../project_guide/02_CAST_REGISTRY.md`
4. `../../characters/roshan/IDENTITY_CARD.md`
5. `../../characters/baby_eagle/IDENTITY_CARD.md`
6. `../../characters/playroom_dust_bunny/IDENTITY_CARD.md`
7. `../../locations/stuffie_room/LOCATION_CARD.md`
8. `01_REFERENCE_UPLOAD_MATRIX.md`
9. `02_SCENE_ENVIRONMENT_AND_ACTION_BRIEF.md`
10. `03_STORYBOARD_A_DIRTY_DISCOVERY.md`
11. `04_STORYBOARD_B_BASKET_WING_BLAST.md`
12. `07_GROK_PROMPTS_COPY_PASTE.md`
13. `08_REVIEW_GATES.md`

## Non-negotiable corrections

- Use `BABY_EAGLE_STANDING_IDENTITY.png` and
  `BABY_EAGLE_PINNED_STATE.png`. Never use the backpack-packing, body-cropped
  `assets/book/baby_eagle.png` image.
- Roshan enters from screen-left and remains off-center left during the first
  reveal so Baby Eagle and every Dust Bunny stay fully visible.
- Storyboard A contains exactly three Dust Bunnies: one on the center light and
  two playing on Baby Eagle's wings. No background, basket or floor bunnies.
- Storyboard B contains exactly four different Dust Bunnies. All four visibly
  come out of the two foreground baskets: two per basket. One from each basket
  reaches a light; one from each basket lands on the floor.
- Storyboard B has two light bunnies and two floor bunnies—never more, never
  fewer. The earlier wing bunnies are absent.
- Baby Eagle's gust is playful and nonviolent. The Dust Bunnies leave as intact,
  surprised, softly spinning fluff. No death, injury, impact or explosion.
- Gameplay sprites and room screenshots are reference authorities only. Every
  delivered shot remains a newly generated complete 16:9 frame sequence.
- Grok audio stays off. Approved family voices and licensed sound are added
  separately during editing.

## First message for the sequence chat

```text
This chat owns the two Day One Stuffie Room storyboards for the private Mermaid
Roshan animation series. Read the Project Constitution, Style Bible, Roshan,
Baby Eagle and Playroom Dust Bunny identity cards, Stuffie Room location card,
and every file in modules/day_one_dirty_stuffie_room before generating.

Treat references by domain. The room image controls geography. Roshan, Baby
Eagle and Playroom Dust Bunny files control identity and named pose vocabulary.
Approved base-video stills control finished painted-cel style and motion
cadence. Accepted ending frames control immediate continuity.

Before generating, return a concise confirmation of: (1) the five shots in the
dirty-discovery storyboard; (2) its exact count of three Dust Bunnies; (3) the
six shots in the clean-room basket storyboard; (4) its exact count and landing
split of four Dust Bunnies; (5) the rejected backpack Baby Eagle image; (6)
Roshan's left-side entry; (7) the harmless wing-gust rule; and (8) audio-off and
15-second limits. Name any file you cannot open instead of guessing. Do not
generate yet.
```

## Module state

- Handoff status: `READY_FOR_ANCHOR_GENERATION`
- Game source: commit `2d5acdb8`
- Storyboard A: `PLANNED`, five shots, approximately 20 seconds assembled
- Storyboard B: `PLANNED`, six shots, approximately 28 seconds assembled
- Baby Eagle: `APPROVED_PRIVATE_CANON`
- Playroom Dust Bunny: `APPROVED`
- Stuffie Room clean geography: approved recurring location anchor
- Human approval required for all six anchor stills before motion generation
