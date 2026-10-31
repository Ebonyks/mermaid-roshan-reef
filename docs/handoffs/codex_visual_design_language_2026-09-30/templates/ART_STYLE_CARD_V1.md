# Art style card v1 (draft template)

Use one completed card for one still-art job: one image, one cutout or one
sheet. Anyone may write the card in words; Codex runs the generator, does the
post-processing and records the outcome. Keep hashes, licences and review
scores in the provenance record beside the card, not in the generator prompt.
For video, use `design/templates/IMAGINE_SHOT_CARD_V1.md` instead.

The prompt order below is the one proven by the approved Roshan atlases
(`assets/characters/roshan_25d/PROMPTS.md`).

## 1. Readiness fields

```text
card_id:        SC-<CLASS>-<name>-<yyyymmdd>
asset_class:    CHAR-HERO | CHAR-CAST | CHAR-RIVAL | PROP-CUTOUT | PROP-STATES |
                ENV-ROOM | ENV-STAGE | FX | UI
style_family:   <family id from the visual language>
target_path:    <final repository path>
status:         DRAFT | GENERATION_READY | GENERATED_PENDING_REVIEW | ACCEPTED | REJECTED
gap:            <the game moment that needs this and why existing art cannot be reused>
identity_sheet: <ID-... for every character shown, or "none">
```

`GENERATION_READY` requires every bound image to exist at its recorded SHA-256,
an identity sheet for every character shown, and family token values copied
from the visual-language data file rather than typed.

## 2. Bound images (two to four)

```text
IMAGE_1: <EX-id> <path> sha256:<...>   job: identity anchor (the exact character or object continued)
IMAGE_2: <EX-id> <path> sha256:<...>   job: style anchor (line, shading and palette of the family)
IMAGE_3: <EX-id> <path> sha256:<...>   job: scale or neighbour anchor (optional)
IMAGE_4: <EX-id> <path> sha256:<...>   job: previous state, for a state sheet (optional)
```

Never bind an anti-exemplar (`AX-`), a runtime capture with interface on it,
a generated board, or third-party art. Protected art (`assets/book/`,
`assets/characters/friends/`) may be bound only as an identity reference and is
never edited.

## 3. Prompt fields (paste-ready text is assembled from these)

1. **Use case and asset type.** For example "children's storybook game prop,
   one transparent cutout".
2. **Input images.** One sentence per bound image naming its job.
3. **Primary request.** What to draw. For sheets: the grid (columns by rows),
   then each cell in reading order.
4. **Subject invariants.** Copied from the identity sheet: face, age,
   proportions, hair, outfit, tail, accessories, colours.
5. **Backdrop.** Cutouts: perfectly flat `#00ff00` chroma background, with
   `#00ff00` used nowhere in the subject. Backgrounds: the full scene at the
   family's native size.
6. **Style and medium.** The family's style line, word for word.
7. **Composition and framing.** Cell size, baseline, padding, apparent height
   and scale relative to the neighbour anchor; one readable silhouette.
8. **Constraints.** The family's token values in words: contour colour and
   width, shadow hue, number of value bands, saturation ceiling. Always:
   no text, labels, watermarks, grid lines, checkerboard or cast shadows on
   cutouts; no third-party characters, brands or logos; no Zelda or other
   game assets.
9. **Avoid.** The family's rejection reason codes, written as plain
   words (for example "fused hands, cropped fins, costume drift").

## 4. Post-processing (Codex)

- Remove the chroma background: border auto-sampling, soft matte, thresholds
  12/220, despill (the Roshan atlas recipe), then confirm no `#00ff00` fringe.
- Resample with Lanczos to the target size: at most 1024 px on the longest
  side or power-of-two (`DL-PERF-04`); room backgrounds keep at least 2048 px
  native coverage per playable screen (`DL-LAY-07`).
- Record provenance: prompt text, bound image hashes, generator, output hash
  and every manual edit; add the `ASSET_LICENSES.md` row in the same commit.

## 5. Checks before review

- Family profile check (advisory): contour colour band, identity colour
  presence, edge alpha and size against the family's exemplars.
- Characters: compare with the identity sheet frame by frame.
- Anything placed in a scene: review the state-local runtime composite at
  phone size, not the isolated file (`DL-VIS-08`).

## 6. Outcome

```text
review_card:  <ART_REVIEW_CARD id>
result:       ACCEPTED -> new exemplar EX-<id>: what it teaches
              REJECTED -> new anti-exemplar AX-<id>: reason codes
```

Every outcome updates the registry, so the next card starts from it.
