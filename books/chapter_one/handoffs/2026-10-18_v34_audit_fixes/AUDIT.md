# Grand Puff book: page-by-page audit (V33)

Status: `SUPPORTING_CURRENT` audit evidence for the V34 work order in
[README.md](README.md). Written by Claude on 2026-10-17, corrected
2026-10-18. Claude made no images. Baseline: V33, commit
`a14a26ee356296c84b7251ce8222f371740ed2cb` on branch
`codex/mermaid-roshan-picture-book`. On 2026-10-18 the owner accepted every
suggested default in the open-questions table.

The book is close: 11 of 34 pages work as they stand, 18 need polish and 5
need a fix before print. The biggest problems are the owner-rejected page 4,
two spreads that repeat an image (8–9 and 24–25), and low-contrast captions on
seven full-art pages. Every fix stays inside the book's source-art rule,
DL-ASSET-08: crops, cutouts, layout, local inpaint or outpaint, or wording. No
scene needs redrawing; one optional new pose for page 9 needs the owner's OK.

## Fix first

These ten changes, in this order, clear every Fix verdict and the most visible
Polish items.

| # | Pages | Problem | Fix inside the rules |
| --- | --- | --- | --- |
| 1 | 4 (with 5 and 23) | The owner-rejected dusty-object page is still in the book, facing the much stronger hall. Its cobweb hangs between floating shells, not "in the corners", while page 5 shows real corner cobwebs. | Replace it with the quiet help-request page (Q1): the shut shell door isolated from the page 23 source, with a soft sound behind it. Put the hall first (4) and the door second (5). |
| 2 | 24–25 | Two Grand Puffs face each other across the gutter at different sizes. Puff fills half of page 24, is Roshan-sized on 25 and bigger than Daddy on 26. | Remove Puff from page 25. Let Roshan hold her sponge out toward page 24's Puff across the fold, at least 0.5 in from the gutter. |
| 3 | 8–9 | The same Roshan pose appears twice side by side: lean, reach, face, hair and object-left layout all match. | Needs the owner's OK: commission one new page 9 pose, Roshan pulling the plug chain as the dirty water drains; it also shows "let the water out". Without it, vary the two pages' scale and placement only. Don't crop page 8 to hands (BK-PG-09 bans severed-hand stickers) or mirror Roshan (her rainbow lock would switch sides). |
| 4 | 1, 7, 11, 13, 14, 16, 20 | Caption contrast drops below 3:1 under parts of these lines. Worst is page 1, "Look, Daddy!": 2.0:1 typical, 1.3:1 at its brightest. | Move each caption onto a darker or quieter area, or set it in navy where the art is light. The page rows below name the spot. |
| 5 | All full-art pages | The PDF is exactly 7 × 5 in (504 × 360 pt) with no bleed or trim box. Page 1's tiara touches the top edge. | For a print service, export a bleed edition: outpaint about 0.125 in on every edge, an allowed extension. Keep key detail at least 0.125 in inside the trim. |
| 6 | 11, 12, 15 | The stuck cup keeps changing: a dark metal can in the seahorse (11), another can in the net (12), a pink cup in Roshan's hands (15). Page 12's bank adds a third can. | Recolor page 11's cup to match page 15 with a local inpaint. Take the can out of page 12's bank (BK-BG-08: one object, one role). |
| 7 | 22 | The scrubbing in the text is not shown, the room is never named, and the banks show fresh spills while Roshan tidies. | Add "In the art room," to the caption. Set the existing yellow sponge cutout on the table, ready for the scrub, without faking a hand action. Swap the bank props for tidy ones. |
| 8 | 18–19 | A dark stone toy store faces a bright pink playroom, so the spread reads as two rooms. Roshan grins as she says "Someone needs help!" | Bridge it in words. Give Roshan an alert, concerned face with a local edit. |
| 9 | 24, 25 | Cowering bunnies (24) and popcorn-eating spectators (25) are left over from the battle version. In a care story they read as fear and spectacle. | Replace them with caring actions. New marginal bunny poses are already owner-authorized. |
| 10 | 27 | The text says "his colors began to shine", but no color shows under the foam. | Add a few faint rainbow glints in gaps of the foam with a local inpaint. Concealment and staging stay intact. |

Contrast figures are WCAG luminance ratios against the caption-free art; see
the method below and [caption_contrast_v33.tsv](caption_contrast_v33.tsv).

## Covers and opening (front cover, pages 1–6)

The opening sets up place, goal and tools in six pages; replace page 4 and fix
page 1's first caption. F = full-art page, C = cutouts on blue stationery.

| Page | Verdict | What works | Needs improvement | Unclear |
| --- | --- | --- | --- | --- |
| [Front cover](../../landscape/revisions/v33_story_covers/complete/page_00.png) | Polish | Roshan is centered and welcoming, and the navy title reads at about 10:1 over open sky. A worried Puff peeking from a doorway sets up the mystery. V33 removed the paint spill, so the cover now promises cleaning, not crafts. | The 13 pt subtitle runs across the bottom of Roshan's tail; move it to clear floor or under the title. Puff is small and shadowed at the far right, and a touch of local door light would help a child find him. | The castle is spotless and the rainbow waterfall fully shown, yet Puff is still unwell. Is this a before or an after moment, and should a book titled Hidden Rainbow show the rainbow up front? (Q7) |
| [Page 1](../../landscape/revisions/v33_story_covers/complete/page_01.png) · F | Fix | An intimate profile, a hand on the porthole and the castle framed like a jewel. A four-word hook that starts on a right-hand page, as planned. | "Look, Daddy!" is white over the bright sea inside the porthole: 2.0:1 typical, 1.3:1 at its brightest, the weakest line in the book. Move it onto the dark metal wall or set it in navy. The tiara tip touches the top edge and will be trimmed. | — |
| [Page 2](../../landscape/revisions/v33_story_covers/complete/page_02.png) · F | Polish | A clear establishing shot: the dock leads the eye to the door, and the navy caption sits in calm sky at about 7:1. The stained-glass mermaid rewards a second look. | The text says "Roshan and Daddy landed", but neither is visible and the plane windows are dark. Accept it as an establishing shot, or reword to "The plane landed at Sky Lagoon." | Is the stained-glass mermaid meant to be Roshan? Children will assume so. |
| [Page 3](../../landscape/revisions/v33_story_covers/complete/page_03.png) · F | Strong | One clear action: Roshan opens the door. Bright outside against dark inside builds curiosity, Daddy is relaxed and supportive, and the caption sits in quiet floor space. | The doorway shows boulders, which reads as a cave; page 5's hall has no rocks. A local inpaint could turn the rock piles into dusty shadow. | Roshan has a clearly pointed ear here, like Daddy and Rumi, while page 1's reads rounded at print size. Which is canon? (Q6) |
| [Page 4](../../landscape/revisions/v33_story_covers/complete/page_04.png) · C | Fix | Clean cutouts, a well-crafted chest and high-contrast navy text. | Owner-rejected and still open. Likely reasons: no character or action; the web hangs between floating shells rather than "in the corners"; it shows inside details before page 5 says "Inside"; the chest never matters again; and "chest" can mean a body part to a four-year-old. | What replaces it? (Q1) |
| [Page 5](../../landscape/revisions/v33_story_covers/complete/page_05.png) · F | Polish | A grand interior with real cobwebs in real corners. Roshan states the goal: "Let's clean it together!" | The dust is faint at print size, so "dust covered the floor" is barely visible, and Roshan and Daddy are small at the far left. A local pass adding visible dust drifts would match the words. | Its doors show theatre masks, a book and a teapot, rooms the story never visits, while page 23's doors match the rooms Roshan cleans. Same hall or two? (Q14) |
| [Page 6](../../landscape/revisions/v33_story_covers/complete/page_06.png) · C | Polish | Big, clear objects teach the words. "One little job at a time." is the book's best theme line, and the bank bunny in a tub foreshadows page 7. | The "brush" is drawn as a feather duster, and children will call it that; page 9 uses a different scrub brush. Add "said Daddy" to the quote for read-aloud clarity. | The theme line never returns. Should it echo once near the end? (Q10) |

## Bath and pool (pages 7–17)

This is the book's strongest stretch, with two clean before-and-after pairs
(7 to 10, 11 to 16) and planted payoffs; spread 8–9 repeats a pose and four
captions need moving.

| Page | Verdict | What works | Needs improvement | Unclear |
| --- | --- | --- | --- | --- |
| [Page 7](../../landscape/revisions/v33_story_covers/complete/page_07.png) · F | Strong | A funny, gross-but-cute bunny entrance: dripping gunk reads instantly as dirty, and "Splash, splash!" invites joining in. It also shows bunnies as playful, which page 19 relies on. | The caption crosses the busy tub base and puddles: 4.1–4.8:1 typical, 2.7:1 at its lightest. Drop it onto the darker floor. | — |
| [Page 8](../../landscape/revisions/v33_story_covers/complete/page_08.png) · C | Polish | Clear hand, sponge and basin contact. The half-clean sink shows progress, and "Round and round" has rhythm. | This sink, a smooth basin on a drawer cabinet, differs from the speckled pedestal sink on pages 7 and 10. With page 9 it repeats one pose side by side (Fix first, item 3). | — |
| [Page 9](../../landscape/revisions/v33_story_covers/complete/page_09.png) · C | Polish | The plug and chain on the bank quietly explain "let the water out", and the tub bridges dirty page 7 and clean page 10. | Same lean-and-reach pose as page 8, on the same spread. The plug on the bank is tiny, so the draining is easy to miss; the new pose proposed in Fix first, item 3 would show it. | Its rainbow scrub brush differs from page 6's duster. One brush or several? |
| [Page 10](../../landscape/revisions/v33_story_covers/complete/page_10.png) · F | Strong | The same room as page 7, transformed: a satisfying before and after. A warm Roshan-and-bunny moment, a hidden Lamma in the towel basket, and a navy caption at about 8:1. | The bunny sits dripping on the rim rather than splashing, so "splashed again" is a small stretch. | — |
| [Page 11](../../landscape/revisions/v33_story_covers/complete/page_11.png) · F | Fix | A strong problem picture. Rumi's reaching hand creates empathy, the seahorse cup and gunked waterfall are planted for later, and Roshan's net shows agency. | The white caption sits on the pale pool rim: 2.5–3.0:1 typical, 1.8:1 at its lightest, and its first word lands on Roshan's tail fin. Move it onto the dark gunk. Keep "under the gunk": it follows the owner's 2026-09-26 wording that Rumi is trapped underwater by gunk. | — |
| [Page 12](../../landscape/revisions/v33_story_covers/complete/page_12.png) · C | Polish | A tactile, satisfyingly gross net, the "I'll help!" and "Scoop, scoop!" refrains, and real pool trash on the banks. | Rumi's backstory ("hundreds of years") sits on a page without Rumi; pair it with page 16 or 17. The net holds a metal can and the bank shows another (BK-BG-08), which muddles page 15's "A cup was stuck". | Is the can in the net meant to be the seahorse's cup? |
| [Page 13](../../landscape/revisions/v33_story_covers/complete/page_13.png) · F | Polish | An excellent partial reveal: warm bands pushing through green sludge make progress visible and build to page 14. | Roshan speaks and "kept clearing" but is not in the picture. This is a recorded source gap (BK-PG-07), so any fix, such as compositing the existing net cutout in from an edge, needs the owner's OK. Line 1 crosses the bright orange reflection (1.6:1 at its lightest). | — |
| [Page 14](../../landscape/revisions/v33_story_covers/complete/page_14.png) · F | Polish | The first big wow: a full rainbow with its reflection, centered, plus a simple magic rule for the pool. | The longest full-art caption (17 words, three lines) sits over rainbow reflection and floating debris, 2.2:1 at its lightest; trim or move it. | Daddy speaks, but he has not appeared since page 5 and is not on this page. (Q5) |
| [Page 15](../../landscape/revisions/v33_story_covers/complete/page_15.png) · F | Polish | Clear cause and effect: cup out, water flows. Roshan's delight and an endearing seahorse, with navy text that reads well on the bright water. | The cup is a dark metal can on page 11 but pink here; match them with a local recolor. The pool is already crystal clear before page 16 says "The gunk was gone." | — |
| [Page 16](../../landscape/revisions/v33_story_covers/complete/page_16.png) · F | Strong | The same room as page 11, transformed, with Rumi rising in the center, arms open: a triumphant payoff. | Line 1 sits on pale pink tiles (3.7:1 typical, 2.6:1 at its lightest); move it lower or set it in navy. Roshan is absent from her own triumph, though page 17 answers that at once. | — |
| [Page 17](../../landscape/revisions/v33_story_covers/complete/page_17.png) · C | Strong | A warm, tender hug, a clean text block on the left, and a tiny seahorse on the bank that recalls the fountain. | Nothing needed. | — |

## Baby Eagle, art room and the last door (pages 18–23)

The Eagle rescue is canon-correct and kind, and page 23's light trails are the
book's best structural device; page 22 needs a fix and spread 18–19 needs a
bridge.

| Page | Verdict | What works | Needs improvement | Unclear |
| --- | --- | --- | --- | --- |
| [Page 18](../../landscape/revisions/v33_story_covers/complete/page_18.png) · F | Polish | Roshan's hand cupped to her ear matches "Chirp, chirp!", so a non-reader can follow the page. The dusty toy room sets up the next problem. | Roshan grins while saying "Someone needs help!"; a local edit to an alert face would sell it. Facing page 19, this dark stone toy store and the bright pink playroom read as two rooms, so bridge it in words (Fix first, item 8). | Is page 18 the playroom, or a storeroom beside it? |
| [Page 19](../../landscape/revisions/v33_story_covers/complete/page_19.png) · F | Strong | Canon is right: two playful bunnies pin Baby Eagle, with no blanket. Their happy faces against his worried one tell "they wanted to play, but he was stuck", and page 6's duster returns. | Roshan is already brushing here, but "I'll help!" comes on page 20. Move the line here, or drop it from page 20, since it already appears on page 12. | — |
| [Page 20](../../landscape/revisions/v33_story_covers/complete/page_20.png) · F | Polish | A clear release: motion lines, Eagle's open wings, giggling bunnies, and the same room as page 19. | The long navy line over the mid-pink floor is the weakest navy caption (3.4:1 typical, 3.0:1 at its darkest). Lift it into the lighter floor or shorten it. | — |
| [Page 21](../../landscape/revisions/v33_story_covers/complete/page_21.png) · C | Strong | "Sorry!" and "Let's play gently" make excellent social-emotional repair. The balloons give the small bunnies voices without enlarging them, and the toy props explain their play. | Nothing needed. | Eagle's wing-to-beak, eyes-down pose reads shy rather than "free!" Is shy acceptance the intent? |
| [Page 22](../../landscape/revisions/v33_story_covers/complete/page_22.png) · C | Fix | The sorting action is clear, and the round cart matches the art room on page 30. | The room is never named; "In the art room," fixes that and pays off page 23's palette door. "Then she scrubbed the table" is not shown, as the team's own review notes; set the existing yellow sponge on the table. The banks show fresh spills that contradict tidying and repeat the foreground props. It is also the third use of the page 8 and 9 pose. | — |
| [Page 23](../../landscape/revisions/v33_story_covers/complete/page_23.png) · F | Polish | Light trails from finished doors to the last door let a child see "all done but one", and the ellipsis primes the page turn. | Line 2 runs through the gold frieze, and a chandelier chain cuts through "behind"; the plain floor band below is empty. Roshan reads calm at print size, and the fourth door's emblem hides behind her head. | Should the door feel magical or uncertain? The violet glow and incoming sparkles read as an invitation. (Q4) |

## Grand Puff and the ending (pages 24–32 and rear cover)

The care-and-wash climax (26–29) and the bubble nap land beautifully; spread
24–25 needs one Puff instead of two, and some battle-era acting should go.

| Page | Verdict | What works | Needs improvement | Unclear |
| --- | --- | --- | --- | --- |
| [Page 24](../../landscape/revisions/v33_story_covers/complete/page_24.png) · C | Polish | A sympathetic reveal: droopy eyes and small dust puffs turn the rumble into a friend who feels ill. Three short lines and a strong page turn from page 23. | The cowering bunnies on the right bank are a battle-version leftover; give them a caring action. Spread problem with page 25 (Fix first, item 2). | Is the big lavender body Puff's dust coat or Puff himself? The pictures imply a coat, since a small rainbow Puff pops out on page 28, but nothing on page 24 reads as dust on top of him. (Q2) |
| [Page 25](../../landscape/revisions/v33_story_covers/complete/page_25.png) · C | Fix | Roshan's kind offer with a soapy sponge, and "we'll" foreshadows the helpers. | A second, smaller Puff faces page 24's across the gutter; remove it and let Roshan reach toward page 24. The popcorn-eating spectators read as watching a sick friend for fun. Keep the owner's wording, but read "Hold on" warmly so it isn't heard as "grab on". | — |
| [Page 26](../../landscape/revisions/v33_story_covers/complete/page_26.png) · F | Strong | The cooperative climax: every helper has a tool and contact, Eagle holds a brush in his beak, and Puff's blissful face shows comfort. "Scrub, scrub!" lands. | White text on the mid-tone ceiling passes (4.6:1 typical, 3.8:1 at its lightest); navy would be worse there, about 3.2:1, so at most thicken the outline. Roshan is the smallest figure at her own climax, which the source staging fixes in place. | — |
| [Page 27](../../landscape/revisions/v33_story_covers/complete/page_27.png) · F | Polish | Total concealment sets up the POP page turn, and staging identical to page 26 makes a spot-the-difference pair. | "His colors began to shine", but no color shows; a few rainbow glints in the foam gaps would match the words (Fix first, item 10). | — |
| [Page 28](../../landscape/revisions/v33_story_covers/complete/page_28.png) · F | Strong | The emotional peak: a color burst, "POP!", joyful helpers, and dust heaps that show "the dust fell away". | Nothing needed. | Puff drops from bigger-than-Daddy to dust-bunny size. Page 29 explains it with "soft and small", but see Q2. |
| [Page 29](../../landscape/revisions/v33_story_covers/complete/page_29.png) · F | Strong | A calm landing where every gaze converges on Puff. "He felt like himself again" is the book's thesis. | Nothing needed. | — |
| [Page 30](../../landscape/revisions/v33_story_covers/complete/page_30.png) · F | Polish | A quiet breath after the climax; the tidy carts reward page 22's sorting. | The text says the whole castle is clean, but the picture is an empty art room the story never named, right after Puff's dusty attic. Try "The art room was tidy. Pearl Castle was clean again." | Why the art room? (Q11) |
| [Page 31](../../landscape/revisions/v33_story_covers/complete/page_31.png) · C | Polish | Gratitude and the invitation close the arc, and sleepy bank bunnies foreshadow the nap. | Roshan's finger-on-chin "thinking" pose fights her exclamations, and the two figures stand far apart. Use a more welcoming existing pose, move them closer, and drop one of the two "said Roshan" tags. | — |
| [Page 32](../../landscape/revisions/v33_story_covers/complete/page_32.png) · F | Strong | A perfect bedtime ending. "Room for everyone" includes the bunnies who trapped Eagle, so forgiveness is visible, and dusk in the windows ends the day. | Line 2 crosses a pillar and banners (3.2:1 at its lightest); shorten it or nudge it. | — |
| [Rear cover](../../landscape/revisions/v33_story_covers/complete/page_33.png) | Polish | True to the story now that V33 retired the craft scene, with a hidden Lamma for sharp eyes. | It repeats page 26 exactly, minus the caption. A tighter crop of the same scene, which the rules allow, would relate without repeating. | Should the back carry a one-line blurb? (Q8) |

## Open questions and accepted defaults

The owner accepted every default below on 2026-10-18. Q6's default names no
answer, so it remains an owner hold.

| # | Decision | Pages | Why it matters | Accepted default |
| --- | --- | --- | --- | --- |
| Q1 | What replaces page 4? | 4, 5, 23 | The rejected insert still faces the strongest early page, and nothing hints at Puff before page 23. | The quiet help-request page recommended on 2026-10-02: the shut shell door isolated from the page 23 art, with a soft sound behind it. Hall on 4, door on 5, so "Inside" still opens the castle and page 23's "One last door" pays it off. |
| Q2 | Is the big lavender body Puff's dust coat? | 24–29 | Pages 28–29 imply it, since a small rainbow Puff pops out, but page 24 draws the lavender as his body. | Yes, a coat, matching the game's new "dusty coat" wording. Let the words carry it ("He was covered in dust"), or add a light grey dusting at the edges of the page 24 cutout. |
| Q3 | What is the "low rumble"? | 23–24 | It is never explained. Game commit ee5a9cec (2026-10-17) recasts Puff as "a friend with a cold" who sneezes. | Make it a symptom the reveal explains, such as a big sniffly sneeze, and keep "He did not feel well." Book and game then agree. |
| Q4 | Should the last door feel magical or uncertain? | 23 | The violet glow and incoming sparkle trails read as an invitation, which works against "a low rumble". | Keep the trails, and dim the light seam locally so the door is the darkest thing in the hall. |
| Q5 | Where is Daddy between pages 5 and 26, and who explains the magic pool? | 6–25 | He hands over tools, vanishes, then speaks once from off the page on 14. | Narrate the rule on page 14 ("The pool was magic! It made the water rainbow-colored.") and keep his return on page 26 as a surprise. |
| Q6 | Does Roshan have pointed ears? | 1, 3 | Page 3 shows a pointed ear like Daddy's and Rumi's, page 1's reads rounded, and the base atlas hides her ears. | Owner's call; then match the other page with a local edit. Held: no default answer. |
| Q7 | What moment does the front cover show? | Cover, 13–14 | The castle is spotless and the rainbow waterfall fully shown while Puff is still unwell, under the title Hidden Rainbow. | Keep it as a promise image and accept the waterfall spoiler, unless the title's mystery matters more. |
| Q8 | Should the rear cover repeat page 26 exactly? | Rear, 26 | Readers see the same picture twice. | A tighter crop on Puff's happy face, Roshan and Eagle, plus one Sniglet line such as "One little job at a time." |
| Q9 | One caption system? | All | Body text switches between 18 pt and 20 pt on eight spreads (4–5, 6–7, 10–11, 12–13, 14–15, 16–17, 18–19, 22–23), and outlined white text is weakest on light art. | 20 pt throughout. Navy where the art behind the words is light, white where it is dark, and white with a heavier navy outline on mid-tones such as the ceiling on pages 26–29. |
| Q10 | Should "One little job at a time" return? | 6, 30 | It is the book's theme, said once and never paid off. | Echo it once, on page 30 or on the rear cover. |
| Q11 | Is page 30's art room on purpose? | 22, 30 | It is the only clean, empty room available, but the text claims the whole castle. | Keep the picture and name the room in the text. |
| Q12 | Keep the battle-era bunny acting? | 24, 25 | Cowering and popcorn read as fear and spectacle in a care story. | Replace them with caring actions; marginal bunny poses are already authorized. |
| Q13 | Where will the book be printed? | All full-art pages | A print service needs about 0.125 in of bleed per edge; a home printer does not. | Keep the current trim PDF for home printing and add a separate bleed edition for a print service. |
| Q14 | Which hall is the castle's hub? | 5, 23 | Page 5's doors (masks, book, teapot) don't match the rooms visited; page 23's (bear, palette, water drop) do. | Leave page 5 alone unless the Q1 door page makes the hub matter; children are unlikely to map its emblems. |

## Method and limits

All 34 V33 page proofs (1512 × 1080 px) were viewed directly, with spreads
taken from the V33 print dummy: story page 1 on the right, reveals at 23 to 24
and 27 to 28. Contrast is the WCAG luminance ratio between a caption's fill
colour and the caption-free source art under each text line the renderer
recorded; [caption_contrast.py](caption_contrast.py) reproduces it. "Typical"
uses the median background pixel; "lightest" and "darkest" use the worst 10%
for white and navy text respectively. The 0.4 pt outline on white captions is
not counted. For scale, 3:1 is the usual floor for large text, and every
stationery page measures 10.4–11.7:1.

This audit does not establish child response, speech-language review,
physical print quality or owner acceptance. The team's internal V32 review
scored every page 4.9 of 5; this audit grades pages against each other to
show where effort pays most.
