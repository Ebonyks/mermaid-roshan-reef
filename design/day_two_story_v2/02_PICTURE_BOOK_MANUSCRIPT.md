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
| "Chirp, chirp! Someone needs help!" (p16) | Baby Eagle's cry opens the day (p5) |
| "One little job at a time." (p4) | Daddy's party plan (p3) and every finished job |
| The dust bunnies' "We were just playing!" (p19) | A dust bunny rolls a strawberry away and says it again (p9-10), then helps build the wall (p29) |
| "Your rainbow was there all along!" (p31) | Grand Puff's rainbow protects the party (p29) |
| "There was room for everyone." (p32) | Lamma is invited onto the stuffie team (p18) |
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
| 3 | Daddy drew a party plan. "Let's make it together. One little job at a time." | 15 | Daddy's Party Plan board with its pictures still empty: tree, strawberries, cake, banner, stuffies, microphone, rocket, candle; along the bottom, the seven invited friends and one empty frame. **GAP**: new board art | D2-OPEN-2 |
| 4 | "First we practise on the Opera stage," said Daddy. "Then we do it for real!" | 15 | The Pearl Opera House stage, curtains open | D2-OPEN-3 |
| 5 | Chirp, chirp! Baby Eagle flew round and round. "Someone needs help!" said Roshan. | 13 | Baby Eagle circling over the Sky Lagoon lawn. Book One p16 composition as reference | J1-L2 |
| 6 | Baby Eagle's tree was sick. Its leaves drooped. A branch was broken. "I'll help!" said Roshan. | 16 | The sick party tree on the lawn. Source: Arborist art (sick state) | J1-L2 |
| 7 | Roshan opened her Tree Book. Which tree? The same leaf! What's wrong? Thirsty! Which medicine? Water! | 16 | Roshan in Arborist gear with the open Tree Book | J1-L1, J1-L2 |
| 8 | Pour, pour! Wrap, wrap! Pink blossoms opened. "Our party tree!" said Roshan. | 12 | The healed, blooming tree with Baby Eagle on a branch; the bark bandage on the mended branch | J1-L2 |
| 9 | Next, strawberries! One, two, three, four… A dust bunny rolled the last one away! | 14 | Strawberry grove on the Sky Lagoon; a dust bunny rolling a strawberry | J2-L2 |
| 10 | "We were just playing!" Baby Eagle found it. Five strawberries! "Let's play gently," said Roshan. | 15 | Baby Eagle pointing with a wing; five berries in the basket; the dust bunny looking sorry | J2-L2 |
| 11 | In the kitchen, Daddy tied her apron. Mix, mix! Stir, stir! Six rainbow colours swirled. | 15 | Kitchen; batter bowl. Source: `chapter2_chef_batter_stirred.png` | J3-L2 |
| 12 | Bake. Stack. Frost. Roshan put five strawberries on top. A rainbow cake! | 12 | The finished six-tier cake. Source: `chapter2_grand_five_strawberry_cake.png` (after the tier and berry fixes in [06](06_GRAPHICS_AUDIT.md#gfx-prop-cake-01)) | J3-L2 |
| 13 | Sniff, sniff. A little nose peeked out behind the flour. Bounce, bounce! She dropped her egg. | 16 | Lamma's nose and ear peeking behind a flour sack; round floury bounce marks on the floor; her lavender egg left behind, and Roshan picking it up. **GAP**: Lamma peek over kitchen art | LAMMA-3 |
| 14 | In the craft room, Roshan painted a banner. Stamp, stamp! Five birthday stars. | 13 | The birthday banner with five stars. Source: banner derivative states ([06](06_GRAPHICS_AUDIT.md#gfx-prop-banner-01)) | J4-L2 |
| 15 | The stuffies wanted to dance. "We need one more dancer," said Roshan. Who was hiding? | 15 | Stuffie Playroom; Kitty and Bunny looking around | J5-L2 |
| 16 | Roshan followed the clues. A tuft of wool. Floury bounce marks. A tiny "Baa!" | 14 | Three clue close-ups in a row: wool in the toy chest, bounce marks to the block tower, the play tent's wiggling flap | LAMMA-JOIN |
| 17 | There she was, in the play tent! A shy little lamb named Lamma. | 13 | Lamma peeking from the play tent. Source: the canonical Lamma poses ([06](06_GRAPHICS_AUDIT.md#gfx-lamma-01)) | LAMMA-JOIN |
| 18 | Roshan held out the egg. "Will you dance with us? There's room for everyone." Lamma nodded. | 16 | Roshan kneeling with the egg in her open hand; Lamma bouncing out to hug it | LAMMA-JOIN |
| 19 | Point! Twirl! Bow! The stuffie team danced together. | 8 | Kitty, Bunny and Lamma mid-bow with Roshan | J5-L2 |
| 20 | Rumi and Roshan sang. Then Rumi remembered a rainbow candle that needed a spark. | 14 | Opera Hall stage; Rumi at the microphone; a faint candle shape in a thought bubble | J6-L2 |
| 21 | At the pool, rainbow waterfall water filled Roshan's little rocket. Click, click! Not yet… | 14 | Mermaid Pool, rainbow waterfall, the parked rocket | J7-L2 |
| 22 | In the library, the magic storybook glowed. Rainbow drips! There was the rainbow candle! | 14 | The unlit candle rising from the glowing storybook. Source: `rainbow_candle_unlit.png` | J8-L2 |
| 23 | Everyone came to the party tree. Something for everyone! "We made all of this together!" | 15 | The whole party under the tree: cake, banner, stuffies, Rumi, rocket, and each friend beside the thing made for them | F1, F2 |
| 24 | Whoosh! The little rocket sent a spark. The candle glowed with rainbow light! | 13 | The candle lit, warm light on every face | F3 |
| 25 | Stomp. Stomp. STOMP! The Ember King came up the hill with his son. | 13 | King and Prince on the path; the Prince looking at the people | F4 |
| 26 | "You made that?" asked the Prince. "All of us did. You can join us." | 14 | The Prince looking at the cake; Roshan with open hands | F4 |
| 27 | "That light belongs at a KING'S party!" boomed the King. "Father, it's her birthday." | 14 | The King pointing at the candle; the Prince's hand half raised | F4 |
| 28 | Roshan felt small. "But I can keep my friends safe." Swish, swish! | 12 | Roshan in front of her friends, looking up at the King | F4, F5 |
| 29 | The dust bunnies made a wall. Baby Eagle brought the banner. Grand Puff puffed a rainbow. | 16 | The three shelter layers over the guests | F5 |
| 30 | "Enough games." The King reached over the rainbow and took the candle. "Sorry," whispered the Prince. | 16 | The King holding the lit candle beside the intact cake; the Prince looking back | F6 |
| 31 | "He took our light," said Roshan. Lamma brought her party hat. Everyone held her close. | 15 | The friends around Roshan; Lamma holding up the hat | F7 |
| 32 | Roshan made a wish: "We'll find our light together." That night, a secret door glowed. | 15 | Roshan wishing with her eyes closed, friends around her; inset: the birthday sleepover, and the glowing moonflower door | F7, F8 |
| Back cover | — | — | The ensemble in pastel, as Book One's approved rear cover H | — |

Every page keeps to Book One's measured limit of 16 caption words (Book One
averages 11.3). This manuscript averages 14.1.

## Art sourcing summary

- **Reusable today:** cake, batter and candle states; banner and stars;
  Baby Eagle, Rumi and dust bunny book art; Book One bubble-nap art; the King
  and Prince identity sheets; Sky Lagoon and castle room backgrounds.
- **Needs the Arborist art committed first:** pages 6–8.
- **Needs the canonical Lamma poses first:** pages 13 and 16–19.
- **Genuine gaps:** cover, pages 2, 3 and 13 compositions, and the finale
  spreads 23–32, which need either accepted cinematic frames or new
  compositions from existing cutouts.
