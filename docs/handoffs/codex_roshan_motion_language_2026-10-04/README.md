# Codex handoff — Roshan's animation template (2026-10-04)

**Owner request (2026-10-04):** analyse the design language and artistic
direction of Roshan's animations, decide how she should move and which
animations make her consistent, and refine the Grok handoffs and Aseprite
work. After revision 1 the owner set the goal: a template for developing all
future Roshan animations from the game and its context.
**From:** Claude (written specification; no game change, no images).
**To:** Codex (every code change, image, board, capture, tool and Grok
packet). **Owner:** answers the questions in section 3 and accepts motion.

**Status:** `PROPOSED / CANDIDATE`, revision 2. Baseline: `dev`
`8a2f30cb0df44ece3b1172ed2dbcb9a55fc5d622`. Finding:
[`MA-ROSHAN-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-roshan-006)
(P2, `CONFIRMED_OPEN`). This packet requests no generation and binds no
image: `ARCHIVE_COMPLETE` after remote verification, `GENERATION_READY` not
applicable, `DELIVERY_ACCEPTED` false.

| Read | For |
|---|---|
| [TEMPLATE.md](TEMPLATE.md) | **The deliverable:** scene analysis, the per-interaction decision, routing to the right model, the card, the style rules, production and review, and the room-by-room pass |
| [templates/ROSHAN_ANIMATION_CARD_V1.json](templates/ROSHAN_ANIMATION_CARD_V1.json) | The card Codex fills for every clip |
| [examples/](examples/RAC-WATER-SWIM-STANDARD.json) | Three worked cards: water swim, Sky Lagoon gentle swim, Pool skimmer scoop |
| [SHOT_CARD_AUDIT.md](SHOT_CARD_AUDIT.md) | The V1 against V2 Grok shot-card audit the owner asked for |
| [ANALYSIS.md](ANALYSIS.md) | Evidence: what Roshan does today, measured defects, Grok and local-pipeline history |

## Owner answers (2026-10-04)

Verbatim, in answer to revision 1's questions:

| # | Question | Owner answer |
|---|---|---|
| Q1 | Is "left and right only" still the standard for gameplay swimming? | "Yes, from the perspective that sprites don't need a up/down orientation, only left/right." |
| Q2 | Does "the same final-action sequence everywhere" cover Day One jobs? | "what?" (re-asked in plain words as Q2 below) |
| Q3 | V1 or V2 shot card? | "I assume v2 is higher quality, but audit. These are not final references, but test documents that will be used in the process of forming our final animation, and will be digested to examine our workflow. The actual workflow will be through ltx locally, through a script run by codex, transferring frames through aesprite for ingame use." |
| Q4 | May gameplay animation be painted limited animation? | "No, our role is to make a rich, comprehensive set of animations for mermaid roshan. Once we develop our test animations, workflow and style, we will be analyzing every room, every game, to derermine what animations are right and wrong, and polish/refine overall product." |
| Q5 | How does Roshan travel on land in the Sky Lagoon? | "Swimming still, different animation than in sea though, slower, more modest travel." |
| Q6 | Does the 2026-10-03 policy still apply (an uncommitted note claimed a later restriction)? | "No, this is a WIP rule. Above describes process better." |
| Goal | — | "The final goal of this is to provide a template for developing all future animations for roshan, based on the game and context. The handoff should analyze the scene and interactions with mermaid roshan, determine if an animation should be generated, and hand it off to the appropriate model if so." |

What changed: the ten style rules keep left/right orientation (M1), replace
limited animation with rich, full motion (M5), and add the Sky Lagoon's
slower, more modest swim (M10). Production runs through LTX locally by a
Codex script, with Aseprite carrying frames into the game; Grok packets are
test documents. The template replaces revision 1's clip-by-clip plan.

## 1. Rules for every package

- Follow `AGENTS.md`, the master-audit contract and the
  [production protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md);
  fill one Roshan animation card per clip (it carries the
  [job card](../../../design/templates/ANIMATION_JOB_CARD_V1.md) fields); two
  generated takes per brief and backend; task caps never reset (`DL-MOT-16`).
- Identity anchor `assets/characters/roshan_25d/roshan_base.png`; name the
  tail light state of the exemplar (`ODR-ROSHAN-IDENTITY`,
  `ODR-ROSHAN-IRIDESCENT`, `ODR-ROSHAN-Q12`).
- Every clip meets the style rules M1–M10 in
  [TEMPLATE.md section 6](TEMPLATE.md#6-style-rules-every-card-meets-motion-locks-revision-2)
  before expressive judgement. Rerun
  [`tools/measure_roshan_motion.py`](tools/measure_roshan_motion.py) after any
  atlas or playback change.
- Originals stay untouched; new art goes to new paths with `ASSET_LICENSES.md`
  rows and editable Aseprite masters. No 3D, rig or skeleton. The Day One story
  clips stay untouched (`DL-CIN-16`).
- Report implementation, machine evidence and owner, device and child
  acceptance separately.

## 2. Packages, in order

### RM0 — Digest the test documents (no new spend)

The owner calls the Grok packets "test documents ... digested to examine our
workflow". Review the eight swimming auditions returned on 2026-09-22 (18
takes and 8 hero cuts on `grok/day-one-cinema-takes-20260922`), the last
core-loop takes (slow A005, dash A006 on
`codex/roshan-swim-start-loop-stop-20260914`) and the three local LTX study
packets with the audition README's review steps (neutral labels, normal speed,
timestamps). Write a workflow digest: failure classes per backend, prompt
phrases that held identity, timing that read well, time and cost per take.
Fold the lessons into TEMPLATE.md and the card. Nothing reviewed here becomes
a final reference.

### RM1 — Build the production tools

| Tool | Does | Done when |
|---|---|---|
| Card validator | Checks a card against the schema: required fields, hashes of existing files, right-facing orientation, home pose sides, every required prompt phrase present in the prompt, caps declared | Passes the three example cards once their keys exist; fails mutated copies |
| General LTX runner | Reads a card's `generation` block and runs LTX locally in ComfyUI, keeping receipts, caps and native frames; replaces the per-study scripts (start from `assets_src/cinematics/ltx_registered_wave_20261004/scripts/render_take.py`) | Reproduces one existing study's receipt format from a card |
| Aseprite bridge | Turns native frames into a master with hidden native and visible clean layers, phase tags, pivot and socket tracks; exports a lossless atlas and timing JSON; reopens and compares | Round-trips byte-identical pixels on a test clip |

### RM2 — Runtime repairs now, with existing art

| Part | Change | Done when |
|---|---|---|
| R1 | Stop the fin jumping sides when gestures start and end (the Grand Puff fight plays `boing`, `point`, `cheer`): in gesture contexts use a gesture-family home pose with the same fin side (for example `roshan_gesture_a.png` frame 0), or a drawn two- or three-frame fin swish. Do not mirror gestures (the ponytail would move). | Measured fin side at gesture entry and exit equals the home pose's; boss probes and the full suite pass |
| R2 | Measure the castle swim's cross-fade with `tools/measure_overdraw.py` and show the owner the swim with and without it at normal speed | Layer counts and the owner's verdict recorded; removal waits for the test swim or the owner's choice |
| R4 | Remove the `twirl` mid-spin mirror swap in `scripts/player.gd` | Probes pass |

Career pose loops (revision 1's R3) move to the Phase B census, where each
career's animations are judged and replaced with rich clips.

### RM3 — Phase A test animations

Run the template on five test clips, each from its own card, through the
RM1 tools:

| Test | Card | Notes |
|---|---|---|
| T1 Water swim, standard | [`RAC-WATER-SWIM-STANDARD`](examples/RAC-WATER-SWIM-STANDARD.json) | Needs two new keys (glide and opposite stroke extreme) |
| T2 Sky Lagoon swim, gentle | [`RAC-SKY-LAGOON-SWIM-GENTLE`](examples/RAC-SKY-LAGOON-SWIM-GENTLE.json) | Variant of T1: slower, more modest; new hover height and shadow |
| T3 Start, stop and turn | New cards | Joined to T1's phases; turn through the existing headings plus a fin swish |
| T4 Listening idle | New card | Authored breath, hair and fin motion on the home pose |
| T5 Pool skimmer scoop | [`RAC-POOL-SKIMMER-SCOOP`](examples/RAC-POOL-SKIMMER-SCOOP.json) | Three new grip keys; the skimmer stays its own card on a hand socket |

Each test: native frames inspected, Aseprite master, in-game A/B behind a
switch, probes, owner review at normal speed on the tablet, and recorded wall
time, cleanup minutes and accepted seconds. The tests settle the workflow and
the style before the census.

### RM4 — Adopt the template

After RM3, move TEMPLATE.md and the card schema into `design/templates/`,
revise the movement language to revision 2 with the style rules, link the
template from the master-audit Animation route and the `INT-ANIMATION` recipe,
and record the RM0 and RM3 lessons.

### RM5 — Phase B: every room and game

Fill a scene sheet and interaction table for every room, game and route where
Roshan appears; judge each existing animation right or wrong; decide; merge
clips across scenes; order the backlog by priority.

### RM6 — Phase C: polish

Produce and repair the backlog in priority order; re-measure after each
change; owner, device and child review.

## 3. Questions

| # | Question | Default |
|---|---|---|
| Q2 | On 3 October a Codex session recorded you choosing "Use the same final-action sequence everywhere, with Roshan visibly finishing each task (recommended)" for the career jobs. It means every job ends the same way: Roshan does the last step herself on screen (for example twists the candy wrapper shut), lets go, the finished result stays visible, and only then does she celebrate. Should the Day One jobs (bath, pool, craft room) end the same way? | Yes (template rule M8) |
| Q7 | In the castle rooms (indoors, out of the water), should she use the water swim or the slower, more modest Sky Lagoon swim? | The gentle swim |
| Q8 | May Codex change the shot-card line in `CLAUDE.md` and `AGENTS.md` from V1 to V2 ([audit](SHOT_CARD_AUDIT.md))? | No change until you say so; those files keep requiring V1 |

## 4. Files

| File | Purpose |
|---|---|
| [TEMPLATE.md](TEMPLATE.md) | The Roshan animation template |
| [templates/ROSHAN_ANIMATION_CARD_V1.json](templates/ROSHAN_ANIMATION_CARD_V1.json) | Card schema with placeholders |
| [examples/RAC-WATER-SWIM-STANDARD.json](examples/RAC-WATER-SWIM-STANDARD.json), [examples/RAC-SKY-LAGOON-SWIM-GENTLE.json](examples/RAC-SKY-LAGOON-SWIM-GENTLE.json), [examples/RAC-POOL-SKIMMER-SCOOP.json](examples/RAC-POOL-SKIMMER-SCOOP.json) | Worked cards |
| [SHOT_CARD_AUDIT.md](SHOT_CARD_AUDIT.md) | V1 against V2 audit |
| [ANALYSIS.md](ANALYSIS.md) | Evidence and revision-1 analysis with revision-2 notes |
| [data/motion_measurements.json](data/motion_measurements.json), [tools/measure_roshan_motion.py](tools/measure_roshan_motion.py) | Numbers-only measurements and the tool that reproduces them |
| [MANIFEST.json](MANIFEST.json), [REMOTE_VERIFICATION.json](REMOTE_VERIFICATION.json) | Hashes and the anonymous GitHub verification receipt |
