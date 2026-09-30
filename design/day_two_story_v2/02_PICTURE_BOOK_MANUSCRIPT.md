# 02 — Book Two manuscript: *Mermaid Roshan and the Rainbow Candle*

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE`
manuscript, 2026-09-30. Owner review pending. Title is a working title.

This is the printed-adventure anchor for Day Two. The game follows the book:
every page names the game beat it anchors, so the story the child hears read
aloud at bedtime is the story she plays. It continues Book One,
*Mermaid Roshan and the Hidden Rainbow*
(`books/chapter_one/landscape/book.json` on branch
`codex/mermaid-roshan-picture-book`).

## Book One style rules, carried over

- 7×5 inch landscape, 32 story pages plus covers; Sniglet, 18 pt minimum;
  the blue two-mound stationery background on reduced-art pages.
- Short concrete clauses, one idea per sentence, explicit names instead of
  "she/he" when a page changes subject.
- At most 16 caption words a page (Book One's measured maximum; its average
  is 11.3).
- Repeated useful phrases: **"I'll help!"**, **"One little job at a time."**,
  **"Let's play gently."**, and Book Two's echo of Book One's last line,
  **"There's room for everyone."**
- Paired sound words for actions: *Scrub, scrub! Pour, pour! Stamp, stamp!*
- Clear cause and effect on every spread; no lesson spoken aloud.
- Nothing scary: sickness is "not feeling well"; the King is loud, not cruel.
- Art rule for the book (`DL-ASSET-08`): reuse existing Grok and handoff
  frames and game art; crops, isolation and targeted in/outpainting are
  allowed; no full-scene redraws. Where no source exists, record the gap
  (marked **GAP** below) instead of inventing a scene.

## Callbacks to Book One

| Book One | Book Two |
|---|---|
| "Whoosh! The waterfall turned rainbow!" (p13) | The rainbow water fills the invitation rocket (p5), and "Whoosh!" the invitations fly (p6) |
| "Chirp, chirp! Someone needs help!" (p16) | Baby Eagle's cry for his sick tree (p7) |
| "One little job at a time." (p4) | Daddy's party plan (p3) and every finished job |
| The dust bunnies' "We were just playing!" (p19) | A dust bunny rolls a strawberry away and says it again (p9-10) |
| "There was room for everyone." (p32) | Lamma is asked to be the star (p18) |
| Everyone asleep in the bubbles (p32) | Everyone wakes in the bubbles (p1), and ends the day at a birthday sleepover while a secret door glows (p32) |
| "Sorry!" (p19 balloon) | The Prince whispers "Sorry" (p30) |

## Manuscript

Page numbers are story pages. "Beat" links to the level design and finale
IDs used across this package.

| Page | Text | Words | Art | Beat |
|---|---|---|---|---|
| Cover | *Mermaid Roshan and the Rainbow Candle* | — | Roshan under the blooming party tree holding the unlit rainbow candle, friends around her. **GAP**: needs a new composition of existing cutouts, like Book One's cover | — |
| 1 | Morning sun sparkled on the bubbles. "Wake up, birthday girl!" said Daddy. | 12 | The Book One bubble-nap pile in morning light. Source: Book One p32 art with a targeted light change | D2-OPEN-1 |
| 2 | It was her birthday! "Can we have a party?" "The best party ever," said Daddy. | 15 | Roshan sitting up in the bubbles, delighted; Daddy smiling. **GAP**: the pose exists in the Roshan atlas; the scene needs a composition | D2-OPEN-1 |
| 3 | Daddy drew a party plan. "Let's make it together. One little job at a time." | 15 | Daddy's Party Plan board with its pictures still empty: rocket, tree, strawberries, cake, banner, a little stage with an empty star, drum, candle; along the bottom, seven empty frames for the friends. **GAP**: new board art | D2-OPEN-2 |
| 4 | "First we practise on the Opera stage," said Daddy. "Then we do it for real!" | 15 | The Pearl Opera House stage, curtains open | D2-OPEN-3 |
| 5 | "First, the invitations!" At the pool, the seahorse filled Roshan's little rocket with rainbow water. | 15 | Mermaid Pool with the rainbow waterfall; the seahorse spraying rainbow water into the little rocket. Source: Day One pool art and `goal_astronaut.png`. **GAP**: the composition | J1-L2 |
| 6 | "For Evie! For Wacky and Chuck!" Whoosh! The invitations floated away to every friend. | 14 | Invitation bubbles rising from the pool over the castle. **GAP**: a new composition; any friend portrait shown must be the protected original, unaltered and small, with the owner's agreement | J1-L2 |
| 7 | "Chirp, chirp! Someone needs help!" Baby Eagle's tree had orange spots on its leaves. | 14 | Baby Eagle beside the sick tree at the meadow's edge. Source: the Tree Book packet's sick patient (`new_art/patient_spaced.png` on `dev`) | J2-L2 |
| 8 | Which tree? Which leaf? Which medicine? Spray, spray! "The tree feels better!" said Roshan. | 14 | Roshan in Arborist gear with the open Tree Book, then the same tree in blossom with Baby Eagle on a branch. Source: the Tree Book packet (reading pose, the healthy patient) | J2-L1, J2-L2 |
| 9 | Next, strawberries! One, two, three, four… A dust bunny rolled the last one away! | 14 | Strawberry grove on the Sky Lagoon; a dust bunny rolling a strawberry | J3-L2 |
| 10 | "We were just playing!" Baby Eagle found it. Five strawberries! "Let's play gently," said Roshan. | 15 | Baby Eagle pointing with a wing; five berries in the basket; the dust bunny looking sorry | J3-L2 |
| 11 | In the kitchen, Daddy tied her apron. Mix, mix! Stir, stir! Six rainbow colours swirled. | 15 | Kitchen; batter bowl. Source: `chapter2_chef_batter_stirred.png` | J4-L2 |
| 12 | Bake. Stack. Frost. Roshan put five strawberries on top. A rainbow cake! | 12 | The finished six-tier cake. Source: `chapter2_grand_five_strawberry_cake.png` (after the tier and berry fixes in [06](06_GRAPHICS_AUDIT.md#gfx-prop-cake-01)) | J4-L2 |
| 13 | Sniff, sniff. A little nose peeked out behind the flour. Bounce, bounce! She dropped her egg. | 16 | Lamma's nose and ear peeking behind a flour sack; round floury bounce marks on the floor; her lavender egg left behind, and Roshan picking it up. **GAP**: Lamma peek over kitchen art | LAMMA-3 |
| 14 | In the craft room, Roshan painted a banner. Stamp, stamp! Five birthday stars. | 13 | The birthday banner with the cake and candle in its medallion and five stars. Source: banner derivative states ([06](06_GRAPHICS_AUDIT.md#gfx-prop-banner-01)) | J5-L2 |
| 15 | The stuffies had a show, but no star. "Who will be our star?" asked Roshan. | 15 | Stuffie Playroom; Kitty and Bunny on their little stage either side of an empty star | LAMMA-JOIN |
| 16 | Roshan followed the clues. A tuft of wool. Floury bounce marks. A tiny "Baa!" | 14 | Three clue close-ups in a row: wool in the toy chest, bounce marks to the block tower, the play tent's wiggling flap | LAMMA-JOIN |
| 17 | There she was, in the play tent! A shy little lamb named Lamma. | 13 | Lamma peeking from the play tent. Source: the canonical Lamma poses ([06](06_GRAPHICS_AUDIT.md#gfx-lamma-01)) | LAMMA-JOIN |
| 18 | Roshan held out the egg. "Will you be our star? There's room for everyone." Lamma nodded. | 16 | Roshan kneeling with the egg in her open hand; Lamma bouncing out to hug it | LAMMA-JOIN |
| 19 | Point! Twirl! Bow! Lamma danced in the middle. The show had its star. | 13 | Kitty, Bunny and Lamma dancing on the little stage, Lamma in the middle; then the bow | J6-L2 |
| 20 | Roshan drummed. Daddy strummed. Baby Eagle plucked. The family band played their song! | 13 | The family band on the Opera Hall stage: Roshan at her pastel shell drums, Daddy with his ukulele, Baby Eagle with his bass. Source: the bands commission's scene candidates (`BAND-02` to `BAND-04`), pending the owner's approval | J7-L2 |
| 21 | In the library, the magic storybook glowed. Rainbow drips! There was the rainbow candle! | 14 | The unlit candle rising from the glowing storybook. Source: `rainbow_candle_unlit.png` | J8-L2 |
| 22 | Everyone came to the party. Lamma danced the star part. "We made all of this together!" | 16 | The party in the middle meadow: the stage, the tree with the banner, the cake on its pedestal, the friends; Lamma dancing in the middle of the show. **GAP**: a new composition | F1, F2 |
| 23 | Daddy lit the rainbow candle. It glowed and glowed. Everyone clapped! | 11 | The candle lit on the cake, warm light on every face. Source: `rainbow_candle_large_flame.png` | F3 |
| 24 | Then the Ember King came up the hill, with his guitar and his son. | 14 | King and Prince on the path, the King's guitar on his back; the Prince looking at the people. Source: the King and Prince identity sheets | F4 |
| 25 | "You made that?" asked the Prince. "All of us did. You can join us." | 14 | The Prince looking at the cake; Roshan with open hands | F4 |
| 26 | "That light belongs at a KING'S party!" boomed the King. "Father, it's her birthday." | 14 | The King pointing at the candle; the Prince's hand half raised | F4 |
| 27 | "Then let's see whose band is best!" Roshan felt small. "But we can play our song!" | 16 | Roshan picking up her two sticks, looking up at the King. Reference: the bands commission's `BAND-01` | F4 |
| 28 | Boom, boom! Strum, strum! Pluck, pluck! Roshan played all the way to the end. | 14 | The family band playing: Roshan drumming, Daddy strumming, Baby Eagle plucking. Source: `BAND-07` and `BAND-09` candidates | F5 |
| 29 | The King's band was loud, but Roshan's band played best. "She did it, Father." | 14 | The King's guitar flourish and the Prince's drum fill; then Roshan raising both sticks in delight. Source: `BAND-05`, `BAND-08` and `BAND-10` candidates | F5 |
| 30 | Whoosh! The King's magic took the candle. "Sorry," whispered the Prince, and they were gone. | 15 | The King holding the lit candle beside the intact cake; the Prince looking back. Source: `BAND-12` and `BAND-13` candidates | F6 |
| 31 | "He took our light," said Roshan. Lamma brought her party hat. Everyone held her close. | 15 | The friends around Roshan; Lamma holding up the hat | F7 |
| 32 | Roshan made a wish: "We'll find our light together." That night, a secret door glowed. | 15 | Roshan wishing with her eyes closed, friends around her; small insets: the friends waving goodbye, the birthday sleepover, and the glowing moonflower door | F7, F8 |
| Back cover | — | — | The ensemble in pastel, as Book One's approved rear cover H | — |

Every page keeps to Book One's measured limit of 16 caption words (Book One
averages 11.3). This manuscript averages 14.2.

## Art sourcing summary

- **Reusable today:** cake, batter and candle states; banner and stars;
  Baby Eagle, Rumi and dust bunny book art; Book One bubble-nap art; the King
  and Prince identity sheets; Sky Lagoon and castle room backgrounds.
- **In the Tree Book packet on `dev`:** the sick and healthy patient tree and
  the reading pose (pages 7-8).
- **Candidates awaiting the owner's approval:** the bands commission's scene
  designs for the band and the royals (pages 20 and 27-30), on branch
  `codex/battle-of-bands-20260920`. `DL-ASSET-08` allows handoff frames as a
  book source; these are not yet approved as first frames.
- **Needs the canonical Lamma poses first:** pages 13 and 15-19.
- **Genuine gaps:** cover, pages 2, 3, 5, 6, 13 and 22 compositions, and the
  finale spreads that the bands candidates do not cover.
