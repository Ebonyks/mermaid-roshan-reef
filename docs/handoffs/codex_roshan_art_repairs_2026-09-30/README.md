# Codex handoff — Roshan art repairs and retired-art deletion (2026-09-30)

**Owner direction (2026-09-30), answering the visual language handoff's
questions Q12 to Q16:** *"1 - no clear protocols exist yet for why. 2. yes.
3. yes. 4. prepare handoff, 5. delete outright, this art is retired in this
draft, existed in previous mermaid roshan wisconsia book"*.

**From:** Claude (written specification; no game change and no images).
**To:** Codex (every edit, image, overlay and board). **Owner:** accepts the
repaired frames.

**Status:** `PROPOSED / CANDIDATE`, revision 1, commissioned by the owner
(answers 4 and 5 above). Tracking finding:
[`MA-ROSHAN-005`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-roshan-005)
(P2, `CONFIRMED_OPEN`). Evidence: the
[Roshan appearance analysis](../codex_visual_design_language_2026-09-30/ROSHAN_APPEARANCE_ANALYSIS.md)
in the visual design language handoff. Every package follows `CLAUDE.md`,
`AGENTS.md` and the master-audit development contract (`DL-AUTH-05`,
`DL-AUTH-06`, `DL-AUTH-07`).

**Evidence baseline:** `dev` `b65c21fdddd79f272a6854f241faa1441abe6616`.
Exact targets, frame rectangles, hashes, consumers and pins:
[`data/repair_targets.json`](data/repair_targets.json) and
[`data/deletion_inventory.json`](data/deletion_inventory.json).

## 0. Rules for every repair

- **Repair inside each image's own design.** The owner kept the older career
  and playground Roshan (answer 2). A repair fixes the named defect only; it
  never moves an image toward the base-world design.
- **Change nothing else:** same pose, costume, props, tail light state, line
  colour and weight, palette, cell grid, pivot and baseline.
- **Reuse pixels from the same sheet first** (for example fins from the
  neighbouring frames). Make pixel corrections in native `.aseprite` sources
  (`design/VISUAL_REPAIR_PLAN_2026-09-26.md` section 7). Generate only when no
  source pixels exist, binding the image itself as identity and style anchor
  (`ART_STYLE_CARD_V1` in the visual language handoff).
- **No protected art changes;** no change to the base-world identity beyond
  the one frame in R-07.
- **Every changed file** gets its provenance updated (pack report, review
  JSON, `PROVENANCE.md`, generation manifest, `ROSHAN_REPACK.json`), an
  `ASSET_LICENSES.md` modification note, a Day Two library refresh (its
  source-change trigger), and re-pinned hashes in the tools that pin it, each
  with the reason.
- **Codex builds the before-and-after boards** for the owner. Claude builds
  no images.

## 1. D-01: delete the retired art (owner: "delete outright")

The owner retired these images from the earlier Mermaid Roshan Wisconsin book;
they show a backpack printed with third-party cartoon characters. No game
script, scene or `project.godot` loads them.

| File | SHA-256 |
|---|---|
| `assets/characters/roshan_sprite.png` and its `.import` | `cf38c4a6…0c901f04d` |
| `assets/sprites/sky_lagoon/sky_lagoon_roshan.png` | `abf0a3ec…5e3347fe4e52` |
| `assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png` | `666fe66f…48c602c97f` |

Update in the same commit: `tools/audit_sky_lagoon_kit.py:30`,
`tools/build_sky_lagoon_preview.py:117` (use `roshan_base.png` or drop the
placement), `tools/tests/test_audit_visual_design.py:120`, the
`ASSET_LICENSES.md` rows at lines 47, 426 and 558 (mark the removals with the
date and the owner decision), three rows of `art_library/ART_INVENTORY.csv`,
and `audit/congruency_sky_lagoon.json` (regenerate with its tool). Leave logs,
archived documents, `gen2/`, `backups/` (excluded from Godot) and evidence
snapshots as history. The files stay in Git history; rewriting the public
repository's history is not part of this decision.

## 2. Repairs, in priority order

Frames are 256 px cells numbered left to right, top to bottom from 0. Career
atlas rows: idle 0–3, travel 4–7, work 8–11, cheer 12–15.

| ID | File | Frames | Defect | Change | Where the child sees it |
|---|---|---|---|---|---|
| R-01a | Geologist atlas | 0–1 (idle) | Tail ends in a point with no fins | Fit the rainbow fins of frames 2–3 | Castle route card and Opera stage idle |
| R-01b | Geologist atlas | 12, 14 (cheer) | White leftover background in the tail loop | Make it transparent | Cheer |
| R-02a/b | Pop Star atlas (all frames) and card | — | Ribbon from the waist reads as a second tail | Shorten or restyle it to end at the hip as costume | Stage; Melody draws the card |
| R-03 | Magician atlas | 8–11 (work) | Spell rings and portals baked in, floating apart | Move them to an overlay sheet drawn at the same positions; clean frames | Stage work animation |
| R-04 | Astronaut atlas | All | Hair hangs outside the sealed helmet | Keep the hair inside the helmet | Stage |
| R-05a | Farmer atlas | 3 (idle) | Apron turns coral and loses its pocket | Match frames 0–2 | Stage idle (flicker) |
| R-06 | Candy Maker atlas | 14 (cheer) | Rainbow lock and sash bow on the wrong side | Match frames 12, 13, 15 | Cheer (flicker) |
| R-07 | `roshan_gesture_b.png` (base world) | 2 ("look") | Tail curls the wrong way | Match frames 1 and 3; pivots unchanged | Exploring "look" gesture |
| R-08 | Racer card | — | White glow along inner outlines | Remove the halo | Racer driver |
| R-09 | Nursery atlas | All | Drawn at about 76% of canon height | Per-career display scale in code, as Ballerina has; no resampling | Stage and route card |
| R-01c, R-05b | Geologist 10; Farmer 9 | — | Sand and soil patches | Keep if intended work dirt; remove if leftover | Work animation |
| R-10 | Magician card; `play_a` 2–3; `gesture_c` 2; Teacher atlas 4 | — | Possible specks or pale patches | Verify in an alpha-aware view; clean if real | Mixed |
| R-11 | Boxer, Chef, Candy Maker cards (Astronaut, Ballerina touch the edge) | — | Cropped tails | Optional: these draw only if an atlas fails; add a probe assertion that atlas frames are used | Fallback only |

Not in this batch (the owner kept the second design): the playground colour
jump (`slide_3_v2`, `swing_3_v2`), the boot splash's hidden rainbow hair, the
Tree Book test's heavy line and green hair patch, and the swim atlases'
ponytail side.

## 3. Acceptance for each repair

- The defect is gone in every listed frame, and a pixel diff shows changes only
  inside the repair region (Codex reports the changed bounding box per frame).
- Image size, cell grid and anchors are unchanged; the Roshan and Opera
  animation tools pass after re-pinning, with each new pin's reason recorded.
- The repaired frame's `cells` measurement stays within its own sheet's range
  (no colour drift).
- Runtime Mobile captures show the fix where the child sees it (table
  column 6).
- Codex publishes one before-and-after board per repair for the owner.
  `MA-ROSHAN-005` moves to `FIXED_PENDING_VERIFICATION` after integration and
  to `VERIFIED_FIXED` when the owner accepts the boards.

## 4. Gates and delivery

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
GODOT=<official 4.7.2> scripts/ci.sh
```

CI on the branch must be green at its exact head before merging into `dev`.
One impact record per batch names every changed file, the old and new
hashes, and `MA-ROSHAN-005`.

## 5. Stop and escalate if

- A repair needs new painted content that changes how the character looks
  (most likely R-04): show the owner a candidate first.
- A sand, soil or speck check is ambiguous.
- A pinned hash belongs to a published handoff packet: republishing is a
  full handoff cycle.
- A step would touch protected art, or the owner asks to purge files from Git
  history (a separate, owner-only operation).

## 6. Report

- **Implemented:** files changed or deleted, old and new hashes, overlay and
  code changes.
- **Machine-verified:** commands and results at the exact head.
- **Outstanding:** owner acceptance of each before-and-after board.
