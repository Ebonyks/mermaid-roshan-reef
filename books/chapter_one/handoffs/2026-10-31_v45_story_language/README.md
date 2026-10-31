# Codex work order: picture book V45, story and language

**Codex: start here.** V45 changes the words of "Mermaid Roshan and the Dust
Bunnies" so the book carries one clear moral. No art changes.

Status: `SUPPORTING_CURRENT` work order, published 2026-10-31. Written by
Claude, who made no images. V45 is not started.

- **Recipient:** Codex.
- **Baseline:** V44, commit `49a199846c61a39a3735e162214706b3687f12d3`,
  branch `codex/mermaid-roshan-picture-book`, repository
  `Ebonyks/mermaid-roshan-reef`. The V44 control file is
  `books/chapter_one/landscape/revisions/v44_door_and_consistency/BOOK_CURRENT.json`.
- **Output:** `books/chapter_one/landscape/revisions/v45_story_language/`,
  published and verified the way V44 was.
- **Inputs in this folder:** [MANUSCRIPT.json](MANUSCRIPT.json) (the exact
  V45 words), [CRITIQUE.md](CRITIQUE.md) (why each word changes) and
  [MANIFEST.json](MANIFEST.json) (every file this order needs, hashed).

## Owner request and decisions (2026-10-31)

The owner asked: "Next draft, critique, this time, focusing particularly on
the language, plotting, word choices, and age appropriate resolutions and
lessons. Let there be a clear moral conclusion and lesson to extract from
this, insure that there is a general relatability and story arc that all
children can identify with within the story".

Asked to choose, the owner answered:

- **Moral:** "Combination of 1 and 2. Empathetic representation of the dust
  bunnies, who cause problems, but just need help, is a critical element, and
  that through the power of friendship, larger jobs can be accomplished."
- **Page 21 bubbles:** "Sorry! We'll be gentle!"
- **Page 5:** "Door is stuck; she promises." The door is stuck, Roshan
  promises to come back, and on page 23 the sparkle trails already drawn
  from the clean rooms reach the door, it clicks open and she keeps her
  promise.

The new story facts listed in [CRITIQUE.md](CRITIQUE.md#decisions-and-open-items)
await the owner's yes on reading V45.

## Scope

- Change only the caption text on the 25 pages marked `changed` in
  MANUSCRIPT.json, and the two speech bubbles on page 21.
- Keep every picture, local patch and page placement; the front and rear
  covers (art and words); the page order, including the doublewide arrival;
  the title, font and type sizes.
- Every word and punctuation mark must match MANUSCRIPT.json exactly. A
  newline marks a line or pause break; you may re-wrap lines to fit.
- Move or resize a caption box only where the new words don't fit, staying in
  quiet space and off faces, hands, tails and the action. Page 17's narrow
  column will likely need widening.
- If the words can't fit at the book's sizes, report the page. Don't cut
  words or set body text smaller than the current minimum; Claude will
  shorten the line.
- No new art, no regenerated art and no change to DL-ASSET-08 permissions.

## Page 21 reading order

The page should read: "Baby Eagle was free!", then the bubbles "Sorry!" and
"We'll be gentle!", then "'Chirp, chirp!' he said happily." and "'Let's all
play gently,' said Roshan." If the renderer can place a second short caption
below Baby Eagle, put the last two lines there. If that needs new renderer
work, keep one caption at the top as in V44; the bubbles still work.

## Checks

1. **Words:** every caption and bubble equals MANUSCRIPT.json; every
   unchanged page equals V44 byte for byte.
2. **Art:** every art layer, patch and pixel outside the caption areas
   matches V44.
3. **Contrast:** run the composed-art caption gate that V37 introduced and
   V42's `verify_revision.py` still carries (V44's script does not): zero
   FAIL lines, and a heavier outline on every line that needs it.
4. **Read-aloud:** read the whole book aloud once and note any line that
   trips. Report it rather than rewording it.
5. **Project gates:** `python -X utf8 -B tools/audit_document_authority.py`,
   `python -X utf8 -B tools/audit_development.py --base auto` and the two
   audit unit-test modules.

## Delivery

- The V45 package: README, revision scope, `BOOK_CURRENT.json`, the reading
  PDF, an email PDF of 25 MB or less, the reader page, verification and a
  manifest.
- Update `book.json`, the book `README.md`, `PAGE_PLAN.md`, `REVIEW.md` and
  `STORY_COMPREHENSION_AUDIT.md`. Add ledger rows marking the V45 README
  current and the V44 README historical, and an impact record under
  `design/audit_impacts/`.
- Push to `codex/mermaid-roshan-picture-book` and verify every manifest file
  over anonymous HTTPS at the exact commit.

## Report back

- One line per changed page: done or held, and any caption box moved.
- Caption gate counts beside V44's.
- The remote verification receipt: commit, manifest SHA-256, check time and
  access mode.
- Any page where the words didn't fit.

## Still open

Unchanged by V45: V44's two art continuity findings (story 1's island
geography and the seahorse's forehead), owner acceptance of the
illustrations, the print edition (V41 Part 2), the doublewide arrival's
print layout, a read-aloud with Roshan, a speech-language review and a test
print. The grown-up question card on branch `claude/angry-roentgen-6a8f7b`
quotes captions and needs its anchors updated after V45.

## Files in this folder

- `README.md`: this work order.
- `CRITIQUE.md`: the story and language critique of V44 and the reasons for
  each change.
- `MANUSCRIPT.json`: the exact V44 and V45 words for all 32 pages, the page
  21 bubbles and reading order, and the unchanged rear text.
- `MANIFEST.json`: every file this order needs, with SHA-256.
