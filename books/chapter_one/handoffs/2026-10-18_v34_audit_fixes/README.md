# Codex handoff: picture book V34 audit fixes

Status: `SUPPORTING_CURRENT` governing work order, published for Codex on
2026-10-18. On 2026-10-19 the owner directed that this handoff governs the
next revision, with the accepted Q1–Q14 defaults.
[OWNER_DECISION_2026-10-19.md](OWNER_DECISION_2026-10-19.md) reconciles it
with Codex's
[V34 implementation review](../../landscape/revisions/v34_editorial_polish/README.md),
sets the final manuscript, and replaces W14 (rear cover) and W16 (print
edition). Read that record first. Claude wrote this packet and made no
images; Codex builds the derivatives.

- **Recipient:** Codex.
- **Baseline:** V33, commit `a14a26ee356296c84b7251ce8222f371740ed2cb`,
  branch `codex/mermaid-roshan-picture-book`, repository
  `Ebonyks/mermaid-roshan-reef`.
- **Output:** a V34 package at
  `books/chapter_one/landscape/revisions/v34_audit_fixes/` on the same
  branch, published and remotely verified the way V33 was.
- **Inputs in this folder:** [AUDIT.md](AUDIT.md) (page-by-page findings),
  [references.json](references.json) (path and SHA-256 of every source named
  below, the identity anchor and all 34 V33 proofs),
  [caption_contrast.py](caption_contrast.py) and
  [caption_contrast_v33.tsv](caption_contrast_v33.tsv) (contrast gate and
  its V33 baseline).

## Owner decision (2026-10-18)

After reading the audit, the owner wrote: "Go with your suggested defaults
for Q1-Q14 and write the Codex revision handoff for the picture book."

- This accepts the default for each open question Q1–Q14 in
  [AUDIT.md](AUDIT.md#open-questions-and-accepted-defaults) and commissions
  this V34 work order.
- Q6 (Roshan's ear shape) had no default answer, so it stays an owner hold.
  Make no ear edit.
- W3b, one new story 9 pose, is the only item outside DL-ASSET-08's ordinary
  permission. It stays `AWAITING_OWNER_OK` until the owner approves it in
  words. Do not generate it before then.
- Nothing here authorizes a full-scene redraw, a game or runtime change, or
  any release step.

## Rules that still bind

- **DL-ASSET-08:** use the existing Grok and storyboard frames. Cropping,
  isolation, contour cutouts, creative layout and local inpainting or
  outpainting are allowed. Full-scene redraws and invented scenes are not.
  Preserve originals, record every derivative's source and edit, and record a
  missing story moment as a gap.
- **Book design language** ([DESIGN_LANGUAGE.md](../../DESIGN_LANGUAGE.md)):
  two image treatments only (BK-PG-08); complete cutouts with no severed
  heads or hands (BK-PG-09); one object, one role (BK-BG-08); bank props
  stay in the bottom 15%, at most 12% of page width and height each, with
  the central gap empty (BK-BG-03 to BK-BG-07); Sniglet text with a 24 pt
  trim inset (cover text: 18 pt inset).
- **Canon:** the waterfall clears and turns rainbow; two dust bunnies trap
  Baby Eagle, never a blanket; the four-helper soap concealment, rainbow
  jump and exact landing on stories 26–29 stay as they are; 34 pages; story 1
  on a right-hand page; page-turn reveals at 23 to 24 and 27 to 28.
- **Identity:** bind `assets/characters/roshan_25d/roshan_base.png` for
  Roshan (tiara, brown wavy hair with the rainbow lock, pink ruffled top with
  lilac sleeves, iridescent lavender-to-rainbow tail). Marginal bunnies use
  the canonical lavender puff with spiral ears and pearl nubs, from the same
  reference the earlier bank work bound, never a prior generated cameo.
- **Records:** each new derivative gets an `ASSET_LICENSES.md` line, an
  impact record and ledger rows in the same change. Keep rejected takes as
  evidence.

## W2: exact manuscript changes

Line breaks are shown as " / ". Every story page not listed keeps its V33
words exactly.

| Story | V33 text | V34 text |
| --- | --- | --- |
| 4 | Cobwebs in the corners. / Dust on the chest! | Inside, dust covered the floor. / “Let’s clean it together!” / said Roshan. |
| 5 | Inside, dust covered the floor. / “Let’s clean it together!” / said Roshan. | Sniff, sniff! / Someone was sniffling behind a big shell door. / “Hello?” said Roshan. |
| 6 | Daddy gave her a brush and some sponges. / “One little job at a time.” | Daddy gave her a brush and some sponges. / “One little job at a time,” said Daddy. |
| 12 | Rumi had lived in Pearl Castle / for hundreds of years. / “I’ll help!” said Roshan. Scoop, scoop! | “I’ll help!” said Roshan. / Scoop, scoop! |
| 14 | Whoosh! The waterfall turned rainbow! / “This swimming pool is magic,” said Daddy. / “It makes the water rainbow-colored!” | Whoosh! The waterfall turned rainbow! / The swimming pool was magic! / It made the water rainbow-colored. |
| 16 | Fresh water flowed. The gunk was gone. / Up came Rumi. She was free! | The gunk was gone. Up came Rumi! / She had lived in Pearl Castle for hundreds of years. / Now she was free! |
| 18 | Chirp, chirp! / “Someone needs help!” said Roshan. | Chirp, chirp! / “Someone in the playroom needs help!” said Roshan. |
| 19 | In the playroom, two dust bunnies sat on Baby Eagle. / They wanted to play, but he was stuck. | Two dust bunnies sat on Baby Eagle. / They wanted to play, but he was stuck. / “I’ll help!” said Roshan. |
| 20 | “I’ll help!” said Roshan. / She gently brushed one bunny away, then the other. | She gently brushed one bunny away, / then the other. |
| 22 | Roshan put the paints in their places. / Then she scrubbed the table. Scrub, scrub! | In the art room, Roshan put the paints in their places. / Then she scrubbed the table. Scrub, scrub! |
| 23 | One last door was still shut. / A low rumble came from behind it... | Only the big shell door was still shut. / Behind it, someone sneezed... AH-CHOO! |
| 24 | Grand Puff! / He was so dusty. / He did not feel well. | Grand Puff! / He was covered in dust. / He did not feel well. |
| 30 | Pearl Castle was clean again. / It was time to rest. | The art room was tidy. / One little job at a time, / Pearl Castle was clean again. |
| 31 | “We helped your rainbow shine!” said Roshan. / “Thank you!” said Grand Puff. / “Come and rest with us!” said Roshan. | “We helped your rainbow shine!” said Roshan. / “Thank you!” said Grand Puff. / Roshan smiled. “Come and rest with us!” |
| Rear | (no text) | One little job at a time. |

Why: Q1 and Q3 turn the Puff mystery into a sound that grows (a sniffle on
5, a sneeze on 23), which page 24's dust explains. Q5 narrates the magic
pool, Q10 and Q11 name the art room and echo the theme, and the rest fix the
order problems on 12, 18–20 and 31 that the audit found. Story 11 keeps
"under the gunk", which follows the owner's 2026-09-26 wording.

## Work items

Each item names its sources by `references.json` work-item key.

### W1: replace page 4 and reorder 4–5 (Q1)

- Story 4 becomes the V33 story 5 page: the same hall art and local patches,
  with its words moved unchanged (W2), the W6 caption rules and the W17 dust
  drifts.
- Story 5 becomes a new cutout page. Its foreground is one contour cutout of
  the shut shell door, isolated from the story 23 art after the W11 dimming:
  the violet shell-fan door, its arched pearl-and-gold surround and the top
  landing. Leave out the hall wall, the other doors, Roshan, the light trails
  and the sparkles. The door reads closed and quiet, with no light leak. Size
  it to roughly 55–65% of the page height, below the usual top caption band.
- Behind it, reuse the V33 story 4 stationery banks unchanged (a curious
  bunny peeking beside a dusty book; an open book and lamp opposite). They
  hold no door, so BK-BG-08 holds.
- Take `v32_shell_cobweb` and `v32_dusty_chest` out of the page map. Keep the
  files and list them as owner-rejected in the V34 manifest.
- **Accept when:** 34 pages; reveal turns unchanged; the door cutout has a
  clean contour with no halo or rectangular backing and matches the story 23
  door.

### W3: spread 8–9 repeats one pose

- **W3a, do now:** keep both cutouts and change only scale and placement so
  the facing pages stop mirroring each other. Set story 8's sink group to
  about 75% of its V33 size, low and left; keep story 9's tub group at V33
  size or larger, right of center. Do not mirror Roshan (her rainbow lock
  would switch sides) and do not crop to hands (BK-PG-09).
- **W3b, `AWAITING_OWNER_OK`:** one new action cutout for story 9. Roshan, in
  the same identity, is behind the far rim of the same scallop tub, turned
  three-quarters toward the reader. One hand scrubs the inner wall with the
  rainbow scrub brush; the other lifts the plug chain while the last murky
  water swirls down the drain. A few green streaks remain. The child sees the
  water going out and the scrubbing, from a different angle than story 8's
  side lean. Bind `roshan_base.png` and the V33 story 9 cutout as identity and
  tub references.
- **Accept when:** the two Roshan figures on the spread clearly differ in
  scale and position (W3a) or in pose (W3b); contours are clean.

### W4: one Grand Puff on spread 24–25

- Story 25: mask Puff out of the `v29_sponge25` cutout pair; keep Roshan
  unchanged. Place her on the left of page 25 facing the gutter, holding her
  sponge out toward story 24's Puff across the fold, at least V33 size. Keep
  the sponge's nearest edge 36 pt (0.5 in) or more from the gutter edge.
- Story 24: Puff unchanged.
- **Accept when:** the open spread shows one Puff, and Roshan's reach points
  at him.

### W5: caring bank bunnies (Q12)

- Story 24 right bank: replace the two cowering bunnies (one under a shell,
  with tremble marks) with two small bunnies worried for Puff. One holds up a
  tiny tissue toward the page center; the other peeks out beside the books
  with a hopeful face. No tremble or sleep marks. The left bank stays.
- Story 25 right bank: replace the popcorn couch spectators with two small
  bunnies getting ready to help. One drags a tiny bucket of suds; the other
  carries a small folded towel. No popcorn, no couch and no sponge, since the
  foreground already has Roshan's sponge. The left bank stays.
- **Accept when:** native review reads care, not fear or spectacle, and the
  bank size, zone, gap and grounding checks pass.

### W6: one caption system and the contrast gate (Q9)

- Set every story caption to 20 pt Sniglet and re-wrap it. Cover type keeps
  its sizes.
- Pick each line's colour from the art behind it, using median relative
  luminance L: navy when L is 0.30 or more; white with the current 0.4 pt
  navy outline when L is 0.15 or less. In between, move the line, or use
  white with a navy outline of at least 1.0 pt (the renderer's halo path).
- Placement: story 1 onto the dark metal wall, or navy over the water; 7
  lower, on the darker floor; 11 onto the dark gunk, clear of Roshan's tail
  fin; 13 off the orange reflection, onto the darker teal water; 14 on darker
  water away from the reflection; 16 on the darker lower floor band; 20 on
  the lighter floor band; 23 down into the plain marble band below the
  carpet; 26–29 white with the heavier outline; 32 line 2 clear of the pillar
  and banners.
- Gate: `python -B books/chapter_one/handoffs/2026-10-18_v34_audit_fixes/caption_contrast.py books/chapter_one/landscape <V34 page_provenance.json> --out <V34 evidence TSV>`.
- **Accept when:** the gate reports zero FAIL lines, and every
  OUTLINE_REQUIRED line is recorded as using the heavier outline. The V33
  baseline is 11 FAIL, 5 OUTLINE_REQUIRED and 61 PASS of 77 lines.

### W7: the stuck cup stays one cup

- Story 11: local inpaint of the cup in the seahorse's mouth so it matches
  the pink scale-patterned cup Roshan holds on story 15, still slimed with
  gunk. Nothing else changes.
- Story 12: in the right bank, replace the algae-covered dented can with
  rubbish that is not a container, such as a slimy seaweed tangle. Keep the
  blue cap and the star wrapper. The net cutout is unchanged.
- **Accept when:** the cup is recognizably the same object on 11 and 15, and
  story 12's banks hold no can or cup.

### W8: story 22 shows the room and the scrub

- Words per W2.
- Rest the existing yellow sponge cutout (`v30_yellow_sponge`) on the table
  top near Roshan's free hand. It is not held, so no hand contact is faked.
- Banks: replace the tipped, spilling bottle and the paint-splashed paper
  with tidy-up details that repeat no foreground object: a small bunny
  pushing a tiny mop on the left, a small rinse bowl of clear water on the
  right.
- **Accept when:** the page shows sorting plus a sponge ready for the scrub,
  and the banks show cleaning, not new mess.

### W9: spread 18–19

- Words per W2: story 18 names the playroom, and story 19 no longer opens
  with it.
- Story 18: a local face edit gives Roshan an alert, concerned look: brows
  lifted and slightly pinched, a small open "oh" mouth, eyes toward the
  sound. Her hand-to-ear gesture, hair, tiara and the room stay unchanged.
- **Accept when:** concern reads at 7 × 5 in, and nothing outside the face
  polygon changes.

### W10: story 27 shows his colors starting to shine

- Local inpaint of four to six small, soft rainbow glints glowing through
  gaps in the foam over Puff's mass, away from the helpers. Do not reveal his
  outline, ears, face or pearls; keep the bubbles, helpers, staging and
  light.
- **Accept when:** the glints show at 7 × 5 in and the 27 to 28 reveal still
  surprises.

### W11: story 23 door mood (Q4)

- Local edit: dim the violet light seam and the sparkle burst at the shut
  door, so it is the darkest and quietest thing in the hall. Keep the four
  route-light trails, the hall, the stairs and Roshan unchanged.
- This dimmed door is the source for W1's cutout.
- **Accept when:** the door reads shut and shadowed, and the trails are
  intact.

### W12 and W13: text-only items

- W12, story 14 (Q5): narration replaces Daddy's line (W2). Daddy's return on
  story 26 stays a surprise.
- W13, story 30 (Q10, Q11): the art room is named and the theme line returns
  (W2). The picture is unchanged.

### W14: rear cover (Q8)

**Replaced on 2026-10-19:** the owner chose a spoiler-free rear instead; see
[the decision record](OWNER_DECISION_2026-10-19.md#rear-cover). The original
request follows as history.

- Re-frame the story 26 scene, with the V33 rear Lamma patch, tighter around
  Puff's smiling face. Keep Roshan (lower left) and Baby Eagle (lower right)
  whole. Daddy and Rumi may be cut at the frame edges, never through their
  faces.
- Density floor: keep at least 1,260 source pixels across the 7 in width
  (about 180 ppi). Never upscale. If the framing needs a tighter crop than
  that, stop at the floor and report it.
- Keep the Lamma inside the frame; if the crop would lose it, re-place the
  same patch on a visible shelf.
- Add "One little job at a time." in Sniglet, at least 18 pt, in quiet
  ceiling space, coloured by the W6 rule.
- **Accept when:** the rear is no longer identical to story 26, the density
  floor holds, the Lamma shows, and the line passes the contrast gate.

### W15: front cover

- Move "A Pearl Castle friendship story" off Roshan's tail to just under the
  title in the sky: navy, at its current size or up to 16 pt, inside the
  18 pt cover inset.
- Local light: brighten the shadowed doorway around Puff slightly, so his
  worried face reads at 7 × 5 in. His design and expression stay.
- The rainbow waterfall stays (Q7).
- **Accept when:** the subtitle clears the tail and passes the gate, and
  pixels outside the doorway polygon are unchanged.

### W16: print bleed edition (Q13)

**Replaced on 2026-10-19** for the owner's larger print size (at least
8 × 11 in, possibly 11 × 14 in); see
[the decision record](OWNER_DECISION_2026-10-19.md#print-edition-replaces-w16).
The original 7 × 5 in request follows as history.

- Keep the V34 trim PDF (7 × 5 in) for home printing.
- Add a print-service edition: MediaBox 522 × 378 pt (7.25 × 5.25 in),
  TrimBox 504 × 360 pt at a 9 pt offset, BleedBox equal to the MediaBox.
  Extend every full-art page and both covers by 9 pt on each side by
  outpainting the existing art; extend the stationery wash on cutout pages
  the same way, keeping the dotted perimeter and banks where they sit
  relative to the trim.
- Captions and key detail stay at least 9 pt inside the trim; story text
  keeps its 24 pt inset. Story 1's tiara meets the top trim: continue it
  into the bleed rather than moving the art.
- **Accept when:** both boxes are present, each page's trim area matches the
  trim edition pixel for pixel, and the outpainted strips match colour and
  line work at the seam.

### W17: smaller art edits

- Story 3: a local inpaint inside the open doorway only turns the boulder
  piles into dusty shadow (a dim floor, soft dust drifts, a faint column), so
  it reads as a dark, dusty hall rather than a cave. The door, Roshan, Daddy
  and the light stay.
- Story 4 (the V33 story 5 hall): a local inpaint adds soft grey-lavender
  dust drifts and tufts across the floor and along the red carpet, visible
  at 7 × 5 in. Characters, doors and architecture stay.
- Story 31: replace the finger-on-chin Roshan with a welcoming existing
  pose. Isolate Roshan from the front cover art, where her open hand reaches
  out, and remove the sponge and bubbles from her lower hand with a local
  inpaint. She already faces left, toward Puff, so no mirroring is needed.
  Move the two figures closer, leaving a gap of about a quarter of the page
  width.
- **Accept when:** each edit stays inside its polygon or cutout, and story 31
  shows a welcoming gesture toward Puff with a complete contour.

## Holds and deliberate no-change items

- **Q6 ear shape, owner hold:** inspect stories 1 and 3 at native resolution,
  report the ear shapes in the V34 evidence, and edit nothing.
- **Q7:** the front cover keeps its rainbow waterfall.
- **Q14:** the hall doors (masks, book, teapot) stay.
- **Story 13:** the clearing action stays a recorded source gap (BK-PG-07);
  only its caption moves. A net composite needs the owner's OK.
- **Q2:** Puff's dust coat is carried by the words only; the optional grey
  dusting at the cutout edges is not commissioned.
- Stories 2, 10, 21, 26, 28 and 29 change only through W6.

## Delivery and evidence

Follow the V33 package pattern on the same branch:

1. Package `books/chapter_one/landscape/revisions/v34_audit_fixes/` with a
   README, revision scope, generation jobs and evidence (prompts, reference
   roles and SHA-256, every native take including rejected ones), derivative
   art, and `complete/` holding the 34 proofs, the lossless master PDF, an
   email PDF of 25 MB or less, the reader page, verification, page provenance
   and print pagination. Add the bleed edition and its checks, the contrast
   TSV, a native visual review of every changed page and both covers, and the
   print dummy.
2. Update `book.json`, the renderer if needed, the book `README.md`,
   `PAGE_PLAN.md`, `REVIEW.md` and `STORY_COMPREHENSION_AUDIT.md`. Add a "V34
   owner decision (2026-10-18)" section to `DESIGN_LANGUAGE.md` that quotes
   the decision above and links this packet. Add `ASSET_LICENSES.md` lines,
   ledger rows (V34 README current, V33 README historical) and an impact
   record.
3. Run the V33 gate set plus W6: `verify_revision`, `audit_book.py` against
   V33, the email-export check, `caption_contrast.py`,
   `python -X utf8 -B tools/audit_document_authority.py`,
   `python -X utf8 -B tools/audit_development.py --base auto` and the two
   audit unit-test modules.
4. Push, then verify the V34 manifest and files over anonymous HTTPS from the
   exact commit, as V33's `verify_remote.py` does.
5. Report implementation, machine verification and open acceptance
   separately. Owner approval, a child reading, a speech-language review and
   a physical print test stay open. No game, runtime, protected-original,
   dev, master or release work.

## Report back

- One line per work item: done, held or blocked, with evidence paths.
- The caption gate counts beside the V33 baseline (11 / 5 / 61).
- The remote verification receipt: commit, manifest SHA-256, check time and
  access mode.
- Anything that could not be done inside DL-ASSET-08, recorded as a gap with
  its reason rather than invented.

## Files in this packet

- `README.md`: this work order.
- `AUDIT.md`: the page-by-page audit and the accepted defaults.
- `references.json`: repository paths and SHA-256 for every named source,
  the identity anchor, the book controls and the 34 V33 proofs.
- `caption_contrast.py`: the numbers-only contrast gate; it writes no
  images.
- `caption_contrast_v33.tsv`: the V33 baseline, 77 caption lines.
