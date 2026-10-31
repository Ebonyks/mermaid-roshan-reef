# Codex handoff — visual design language: one measurable, example-backed reference the game learns from (2026-09-30)

**Owner request (2026-09-30):** *"Is the visual design language of the mermaid
roshan articulated in the master audit in a way that it is easy for the game to
reference and learn from itself how to develop future art? If not, implement a
plan to refine it."*

**From:** Claude (analysis, written specifications and a draft reference; no
game change and no images). **To:** Codex (implementation, tools and every
image). **Owner:** answers the questions in section 6 and accepts the result.

**Status:** `PROPOSED / CANDIDATE`, revision 3 (2026-09-30). Revision 3 records
the owner's answers to Q12–Q16; the repairs and the deletion they commissioned
are specified in the [Roshan art repair handoff](../codex_roshan_art_repairs_2026-09-30/README.md). Revision 2
records the owner's identity decisions (section 6) and adds a frame-by-frame
[appearance analysis](ROSHAN_APPEARANCE_ANALYSIS.md) of every runtime Roshan
image, which the owner asked to receive as part of this handoff. This packet
recommends; it grants no visual, device, child or owner acceptance and changes
no existing finding lifecycle. The one register change made with it is the new tracking
finding
[`MA-DOC-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-008)
(P2, `CONFIRMED_OPEN`). Every work package still follows `CLAUDE.md`,
`AGENTS.md` and the master-audit development contract (`DL-AUTH-05`,
`DL-AUTH-06`, `DL-AUTH-07`): impact record, ledger rows, gates, CI, then
integration into `dev`.

**Evidence baseline:** `dev` `b65c21fdddd79f272a6854f241faa1441abe6616`.
Measurements are reproducible with
[`tools/measure_visual_profile.py`](tools/measure_visual_profile.py), which
reads tracked files and writes numbers only.

Authority: subordinate to the [design language](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
the [master audit](../../../audit/MASTER_AUDIT_2026-08-09.md) (sections 9–13),
the [development contract](../../../design/AUDIT_DEVELOPMENT_CONTRACT.md) and
the [document ledger](../../../design/05_DOC_LEDGER.md). Where they disagree
with this packet, they win until the owner changes them.

## What is in this folder

| Path | What it is |
|---|---|
| `README.md` | This handoff: target, work packages, acceptance, owner questions |
| `VISUAL_LANGUAGE_AUDIT.md` | The answer and its evidence: routing, sources, measurements, contradictions |
| `VISUAL_LANGUAGE_DRAFT.md` | Claude's draft of the reference text, to land as `design/reference/VISUAL_LANGUAGE.md` |
| `ROSHAN_APPEARANCE_ANALYSIS.md` | Revision 2: every runtime Roshan image measured frame by frame and reviewed by eye; what is light, what is costume and what is drift |
| `templates/ART_STYLE_CARD_V1.md` | One card per still-art job: bound exemplars, prompt fields, post-processing, checks |
| `templates/ART_REVIEW_CARD_V1.md` | One review card: vetoes, six axes, weakest axis decides |
| `data/visual_tokens_seed.json` | 22 visual tokens with value, strength, rule and source |
| `data/identity_sheets_seed.json` | Identity sheets for Roshan (iridescent tail with two light states, per the owner) and seven more characters |
| `data/registry_seed.json` | 25 hashed Roshan exemplars, exemplar candidate sources, rejection reason sources, today's nine rubrics |
| `data/visual_contradictions.json` | 15 contradictions with a suggested resolution |
| `data/contour_profile.json`, `castle_room_shadow_profile.json`, `roshan_identity_palette.json`, `roshan_identity_presence.json` | Measurements behind the audit |
| `data/roshan_atlas_frames.json`, `data/roshan_single_images.json` | Revision 2: per-frame measurements of 24 atlases (368 frames) and 31 single images |
| `tools/measure_visual_profile.py` | The read-only measurement script (Pillow; never writes images) |
| `MANIFEST.json` | SHA-256 of every file in this folder |

Nothing here is loaded by the game; `.gdignore` keeps Godot from importing it.

## 0. Summary

The answer is **no** ([audit](VISUAL_LANGUAGE_AUDIT.md)). The master audit
only routes, the rules are mostly adjectives, the approved art disagrees about
what Roshan looks like, and nothing records which images are the examples to
follow.

| Today | When this handoff is done |
|---|---|
| The language is scattered over design 06, design 02, a partly superseded style guide, a generation contract, scoring documents, an archived lighting audit and 42 copies of a cinematic text | One reference, `design/reference/VISUAL_LANGUAGE.md`, one link from the master audit's Art row |
| One of ten `DL-VIS-*` rules has numbers; no colour values in governed documents | Tokens with values, tolerances and sources in one data file that tools read |
| One image named by any rule | Exemplar and anti-exemplar registries with hashes and the lesson each teaches |
| Roshan described four ways | Identity sheets for every recurring character; Roshan's records the owner's decision (atlases primary; iridescent tail) and a reviewed list of the remaining variance |
| Ten partial generation protocols; nine rubrics | One style card and one review card |
| Nothing learns | Family profiles are computed from the exemplars; every review adds to the registries |

## 1. Target: the visual language kit

| Piece | Path | Holds |
|---|---|---|
| Reference | `design/reference/VISUAL_LANGUAGE.md` | Pillars, families, identity, tokens table (generated), composition, layers and motion, technical rules, making art, reviewing art, open questions |
| Data | `design/reference/visual_language.json` | Tokens, families with style lines, one palette with tolerances, one set of tool thresholds |
| Identity sheets | `design/reference/identity/ID-*.json` | Grand Puff lock format: authority, traits, part counts, forbidden changes, sampled colours, scale against Roshan, variants |
| Registry | `design/reference/art_registry.json` | `EX-*` exemplars, `AX-*` anti-exemplars, `RC-*` reason codes |
| Templates | `design/templates/ART_STYLE_CARD_V1.md`, `ART_REVIEW_CARD_V1.md` | The two cards from this packet |
| Completed cards | `assets_src/art_cards/<card_id>/` | One folder per job: style card, review card, provenance |
| Tool | `tools/visual_language.py` | `profile`, `check`, `registry --check`, `render` (built from `measure_visual_profile.py`) |

How the game draws from it:

1. **Authoring now.** Anyone making art follows section 0 of the reference:
   family, identity sheet, style card with bound exemplars, Codex builds,
   review card.
2. **Checks now.** The tool recomputes each family's profile from its
   exemplars, reports how far a candidate sits from it, and fails the
   registry check if a path, hash or ID is broken. The profile report is
   advisory (`DL-VIS-08`).
3. **Learning.** Every accepted image becomes an exemplar and every rejected
   one an anti-exemplar with reason codes, in the same commit as the review
   card. Profiles and the tokens table regenerate from the registry.
4. **Runtime later.** Code reads palette and interface tokens from the data
   file (refinement handoff WP-13; owner-gated).

## 2. Invariants

- **Never recolour or regenerate approved art to satisfy a measurement**
  (`DL-VIS-08`). The profile tool reports; people decide.
- **Protected art is never edited** (`assets/book/`,
  `assets/characters/friends/`, `assets/audio/voices/`); book images are
  identity references only (`DL-ASSET-08` for the picture book).
- **Claude writes; Codex builds every image** (`CLAUDE.md`, 2026-09-30).
  Claude does not run `tools/audit_castle_card_alpha.py` or
  `tools/audit_fairy_art_v2.py`, which write contact sheets.
- **No Roshan art changes in this handoff.** The owner settled her identity
  (section 6, Q1 and Q2); every remaining variance item goes to the owner as a
  review list before any art changes.
- **Rules stay in design 06.** The reference links to `DL-*` IDs and does
  not restate them. New rules need the owner (section 6, Q8).
- **No runtime file, protected path or high-risk file changes** unless the
  owner names them.

## 3. Coordination

| Other work | Relationship |
|---|---|
| [Refinement handoff](../codex_master_audit_refinement_2026-09-30/README.md) WP-4 (canon) | Identity sheets are the visual half of canon; settle `CANON-C01` and `CANON-C09` here |
| Refinement WP-5 (patterns), WP-6 (tokens) | Move `TOK-OUTLINE-MAJOR-PX`, `TOK-OUTLINE-INTERIOR-PX`, `TOK-SHADOW-HUES` and `TOK-BACKGROUND-NATIVE-PX` into the `TOK-VIS-*` set; one ID per value |
| Refinement WP-11 (checks), WP-13 (runtime tokens) | `registry --check` joins WP-11's checks; runtime tokens stay owner-gated |
| [Consolidation handoff](../codex_reference_consolidation_2026-09-30/README.md) R06 and W1 | This packet is R06's detailed plan. Absorb the style guide, generation contract, scoring documents, `LIGHTING_2P5D_AUDIT_2026-08-02.md` and `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` before W4 archives them |
| [Visual polish handoff](../codex_visual_polish_2026-09-25/README.md) | Its repairs continue; its style-matching protocol becomes the style card; its line letting Claude build reference packs is superseded |
| Door highlight and imp contest handoffs | Their colours and reuse rules feed the tokens and the registry; the imp contest already forbids drawing the tail-cropping career cards as full-body actors (analysis RV-15) |
| `MA-VIS-003`, `MA-VIS-004` | Stay under `DL-VIS-08`; source averages are not evidence |

## 4. Work packages

### VL0 — Stage 0: re-measure and coordinate (read-only)

Run the four measurements in `tools/measure_visual_profile.py` at your head
and note what moved. Check which refinement and consolidation packages have
landed and adjust. Collect the owner's answers to section 6. **Gate:** a short
note in the impact record.

### VL1 — Land the reference text

Move `VISUAL_LANGUAGE_DRAFT.md` to `design/reference/VISUAL_LANGUAGE.md`,
re-checking every statement against its source at your head. Replace the
retired Roshan wording in `design/01_GAME_DESIGN.md` and
`design/02_ART_DIRECTION.md` with a pointer to `ID-ROSHAN`. Correct design
02's list of hard CI gates. Route the master audit's Art row and design 06
section 4's opening paragraph to the reference. **Gate:** both governance
gates ALL OK; every `DL-*`, `EX-*`, `ID-*` and token ID cited resolves.

### VL2 — Identity sheets (Roshan settled by the owner)

Write `ID-ROSHAN` from section 8 of the
[appearance analysis](ROSHAN_APPEARANCE_ANALYSIS.md): identity anchor is a
base-world atlas or `roshan_base.png`; the tail is iridescent with a named
light state; base outfit; age and build; line and finish; forbidden changes;
the measured base-world ranges of section 5.1. Sample colours with pixel
coordinates and record scale against props from runtime captures, as Grand
Puff's lock does. Then Daddy, Rumi, Baby Eagle, dust bunnies, Grand Puff (link
its lock), the pearl plane and the rival imps. **Gate:** each sheet cites
approved images by hash; no protected file changes.

### VL2a — Roshan variance decisions

The owner answered the variance review on 2026-09-30. Record the answers in
`ID-ROSHAN` and the registry: no light-state protocol yet (RV-01); the older
career and playground design is kept (RV-03, RV-04, RV-06); new base-outfit art
wears the tiara (RV-05). The defects (RV-07 to RV-20) and the deletion of the
retired art (RV-21) are specified in the [repair handoff](../codex_roshan_art_repairs_2026-09-30/README.md).
**Gate:** the answers appear in `ID-ROSHAN`; no approved image changes in this
handoff.

### VL3 — Registries

Load the 25 Roshan exemplars from `data/registry_seed.json`, by role:
base-world atlases are identity exemplars; career atlases are costume and pose
exemplars only; `roshan_sprite.png` and the 13 career cards generated from it
are "never bind as identity" anti-exemplars (reason code
`RC-IDENTITY-SOURCE`, analysis section 6). Promote
candidates from the existing approval ledgers only with approval evidence,
and say what each teaches. Merge the rejection sources into one `RC-*`
taxonomy and add anti-exemplars with reason codes. Link existing ledgers
rather than copying them. **Gate:** every family has at least three
exemplars or a recorded gap.

### VL4 — Tokens, palette and thresholds

Build `visual_language.json` from `data/visual_tokens_seed.json`. Make one
palette: the style guide's named anchors where they fall inside measured
family ranges, plus measured family palettes, each with a colour-difference
tolerance (Q7). Choose one definition each for green spill, visible alpha,
plausible coverage and crushed pixels, and record which tool used what
before. Generate the tokens table in the reference from the data. **Gate:**
no token typed in two places.

### VL5 — Cards

Land both templates in `design/templates/`. Write two completed cards
retrospectively from existing provenance as worked examples (one prop, one
character sheet), without generating anything. **Gate:** both examples
validate against the templates' required fields.

### VL6 — Tool and checks

Build `tools/visual_language.py` from `measure_visual_profile.py`:
`profile` (family statistics from exemplars), `check FILE --family F`
(distance from the profile), `check FILE --identity ID-ROSHAN` (light state,
hair and finish indicators against the base-world ranges, from the `cells`
measurements), `registry --check` (paths, hashes, unique IDs,
family coverage) and `render` (tokens table). Add unit tests with fixture
images built in the test, a stress case that must fail, and run `profile` and
`check` as advisory steps in `scripts/ci.sh`; `registry --check` blocks.
The tool never writes images. **Gate:** tests green; the stress case fails as
intended.

### VL7 — Rules

With the owner's answer to Q8, promote into design 06 the visual rules that
now live only outside it: one shadow hue per zone, the light headroom, the
overdraw and motion budgets, the review vetoes with weakest-axis scoring, and
the requirement that new art uses a style card with bound exemplars and that
characters match their identity sheets. Coordinate with consolidation W1.
**Gate:** document gate ALL OK; each new rule cites its source.

### VL8 — Cold-start art dry run (the learning test)

Give a fresh agent session only the repository and ask for two jobs: a new
interactive prop for an existing room, and a new four-pose sheet for an
existing character. It must find the family, identity sheet, exemplars and
tokens, and write both style cards without help. Generating the images is
owner-gated (Q9); without approval the run stops at the cards and a review
of the cards. **Gate:** no step needed knowledge outside the kit; the owner
accepts the result.

### VL9 — Keep it fresh

Every accepted or rejected image updates the registry in the same commit as
its review card. Profiles regenerate when exemplars change. Each identity
sheet and the reference record their last re-verification date. Write this
into the development contract only if the owner accepts it (Q10).

## 5. Acceptance criteria

| ID | Criterion | How to show it |
|---|---|---|
| AC-1 | The Art row reaches the reference in one link, and the reference reaches every visual token, identity sheet and template in one more | Link check |
| AC-2 | Every token in the reference comes from `visual_language.json`; no value typed twice | `render --check` |
| AC-3 | `ID-ROSHAN` records the owner's decisions (atlases primary; iridescent tail with named light states); no governed document keeps the retired wording; every new Roshan card binds a base-world identity anchor | Grep and card check |
| AC-4 | Every recurring character has an identity sheet citing hashed approved images | Registry check |
| AC-5 | Every family has at least three exemplars or a recorded gap; every anti-exemplar has reason codes | Registry check |
| AC-6 | One threshold each for spill, visible alpha, coverage and crushed pixels, used by the tool | Tool tests |
| AC-7 | `registry --check` blocks in CI; `profile` and `check` run advisory; the stress case fails | CI log |
| AC-8 | Both templates landed with one worked example each | Files |
| AC-9 | The cold-start dry run passes and the owner accepts it | Dry-run record |
| AC-10 | No approved or protected image changed; no image written by Claude | `git diff` and the impact record |
| AC-11 | `MA-DOC-008` acceptance met and recorded in its history | The finding record |
| AC-12 | The owner's answers to Q12–Q16 are recorded in `ID-ROSHAN` and the registry, and the repair handoff is linked; no approved image changes in this handoff | Sheet, registry and `git diff` |

## 6. Owner questions (Codex proceeds on the default and reports it)

| # | Question | Default |
|---|---|---|
| Q1 | Which Roshan do new pictures continue (`OQ-VIS-ROSHAN`)? | **Answered 2026-09-30:** her tail is iridescent; the lavender and rainbow renderings are both correct |
| Q2 | Is Roshan's identity authority the book (`DL-VIS-06`) or the approved atlas family (`DL-MED-02`) (`OQ-VIS-AUTHORITY`)? | **Answered 2026-09-30:** the approved atlases are primary; the book is a likeness reference |
| Q3 | Keep the imps' heavy near-black line as their deliberate look (`OQ-VIS-RIVAL-LINE`)? | Yes, recorded as the rival family trait |
| Q4 | Are the four flat-shell rooms placeholders to repaint (`OQ-VIS-FLAT-ROOMS`)? | Yes, as backlog outside this handoff |
| Q5 | May warm-floored rooms keep warm dark local colour (`OQ-VIS-WARM-ROOMS`)? | Yes for local colour; shading stays cool |
| Q6 | New sprite frames: image generation from bound exemplars, or Aseprite cel authoring (`OQ-VIS-SPRITE-CHANNEL`)? | Generation for new sheets; Aseprite for corrections and in-betweens |
| Q7 | Replace the 20 typed swatches with measured family palettes plus named anchors (`OQ-VIS-PALETTE`)? | Yes |
| Q8 | Promote the visual rules in VL7 into design 06? | Yes, as new `DL-VIS-*` IDs citing their sources |
| Q9 | May the cold-start dry run generate its two images (kept as candidates, not placed in the game)? | No; stop at the cards |
| Q10 | Add the keep-fresh step to the development contract? | Recommendation only until accepted |
| Q11 | May Codex update the art-direction paragraphs of `CLAUDE.md` and `AGENTS.md` to point to the reference (high-risk files)? | No, unless the owner names it |
| Q12 | Does the tail's light state follow the scene light (`OQ-VIS-LIGHT-STATE`)? | **Answered 2026-09-30:** no protocol yet explains why; new art continues the state of the exemplar it extends and names it; no rule is enforced |
| Q13 | Keep the older career and playground Roshan, or regenerate it (RV-03, RV-04, RV-06)? | **Answered 2026-09-30:** keep it; all new art follows the base-world child |
| Q14 | Does Roshan wear the tiara whenever she is not in a career costume (RV-05)? | **Answered 2026-09-30:** yes |
| Q15 | Repair the defects in RV-07 to RV-20? | **Answered 2026-09-30:** prepare the handoff; see the [repair handoff](../codex_roshan_art_repairs_2026-09-30/README.md) |
| Q16 | The unused images with a third-party cartoon backpack (RV-21)? | **Answered 2026-09-30:** delete outright; the art is retired from the earlier Mermaid Roshan Wisconsin book (repair handoff D-01) |

## 7. Gates and delivery

Before every push, from the repository root:

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
```

plus the new tool's tests and `scripts/ci.sh` when a tool or `ci.sh` changes.
CI on the branch must be green at its exact head before merging into `dev`.
Report implementation, machine verification and outstanding acceptance
separately.

## 8. Stop and escalate if

- A step would change an approved, protected or runtime image.
- Recording an identity requires choosing between conflicting approved
  images that the owner has not settled.
- A threshold change would turn a currently green blocking gate red; record
  it and ask before tightening.
- A step needs `CLAUDE.md`, `AGENTS.md`, `SECURITY.md`, `.claude/`, `.codex/`
  or `.github/workflows/` and the owner has not named it.
- Another branch has edited design 06, the master audit, the ledger or the
  finding register since you started: rebase and re-verify.
- Disk space is below what a checkout or import needs.

## 9. Report (per package, in the pull request and the impact record)

- **Implemented:** files, IDs created, sources absorbed.
- **Machine-verified:** exact commands and results at the named head.
- **Outstanding:** owner questions answered or pending, families without
  exemplars, and every visual, device, child and owner gate that remains open.
