# Codex handoff — Roshan's motion language (2026-10-04)

**Owner request (2026-10-04):** analyse the design language and artistic
direction of Roshan's animations, decide how she should move and which
animations make her consistent, and refine the Grok handoffs and Aseprite
work. **From:** Claude (written specification; no game change, no images).
**To:** Codex (every code change, image, board, capture and Grok packet).
**Owner:** answers Q1–Q6 and accepts motion.

**Status:** `PROPOSED / CANDIDATE`, revision 1. Analysis and evidence:
[ANALYSIS.md](ANALYSIS.md). Finding:
[`MA-ROSHAN-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-roshan-006)
(P2, `CONFIRMED_OPEN`). Baseline: `dev`
`8a2f30cb0df44ece3b1172ed2dbcb9a55fc5d622`.

This packet requests no generation and binds no image, so it is a written
Codex handoff, not an external animation packet. `ARCHIVE_COMPLETE` applies
to this packet's files after remote verification; `GENERATION_READY` is not
applicable; `DELIVERY_ACCEPTED` is false. Any Grok job Codex sends under these
packages needs its own complete visual-reference packet (`AGENTS.md`).

## 0. Rules for every package

- Follow `AGENTS.md`, the master-audit contract and the
  [production protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md);
  one [job card](../../../design/templates/ANIMATION_JOB_CARD_V1.md) per clip,
  two generated takes per brief and backend, task caps that never reset
  (`DL-MOT-16`).
- Identity anchor: `assets/characters/roshan_25d/roshan_base.png` or a
  base-world atlas; name the tail light state of the exemplar
  (`ODR-ROSHAN-IDENTITY`, `ODR-ROSHAN-IRIDESCENT`, `ODR-ROSHAN-Q12`).
- Judge every candidate against the ten motion locks M1–M10 in
  [ANALYSIS.md section 9](ANALYSIS.md#9-how-roshan-should-move-ten-motion-locks)
  before expressive quality. Rerun
  [`tools/measure_roshan_motion.py`](tools/measure_roshan_motion.py) after any
  atlas or playback change and record its numbers.
- Preserve originals; new drawings go to new paths with `ASSET_LICENSES.md`
  rows and editable Aseprite masters. No 3D, rig or skeleton.
- The Day One story clips stay untouched (`DL-CIN-16`).
- Report implementation, machine evidence and owner/device/child acceptance
  separately.

## 1. Packages, in order

### RM0 — Review what Grok already returned (no new spend)

**Why:** 26 returned files from the eight swimming auditions
(`grok/day-one-cinema-takes-20260922`,
`assets_src/cinematics/grok_builder_return_2026-09-22/takes/RSW-0*.mp4` and
`movies/RSW-0*.mp4`) and the last core-loop takes (slow A005, dash A006 on
`codex/roshan-swim-start-loop-stop-20260914`) have no review record.

**Do:** apply the review protocol in
`assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/README.md`
("Review and choose"): neutral labels, normal speed then frame-step,
timestamps, identity and topology vetoes, the six expressive dimensions.
Add the M1–M6 checks. Nominate one timing spine for clip 1 (slow swim) and
fragments for clips 2, 3, 9 and 11.

**Done when:** a published review record names each take's verdict with
reasons, the shortlist and the nominated in/out times, and the owner has seen
the shortlist. No take is accepted by this review.

### RM1 — Record the decisions and adopt the locks (after Q1, Q2, Q4)

**Do:** record the confirmed answers in the owner decision register with
`tools/record_owner_decision.py` (sources: `056e668f` for the two-view swim,
`cfcadc96` for the shared final-action sequence). Write revision 2 of
`design/animation/ROSHAN_MOVEMENT_LANGUAGE.md` from ANALYSIS sections 9–10,
keeping v1's acting language. Add one clip contract per canonical clip in the
Grand Puff format (`design/animation/grand_puff_encounter_clips_v1.json`).
Claude can draft the documents if the owner asks; register entries need the
owner's answers first.

**Done when:** the register check passes against `origin/dev`, the document
gates pass, and each clip has a contract with view, home pose, fin side,
timing chart, events and exits.

### RM2 — Runtime repairs with existing art

| Part | Change | Acceptance |
|---|---|---|
| R1 | In gesture contexts (Grand Puff fight, toys, trophy), stop the fin jumping: use a gesture-family home pose with the fin on the same side (for example `roshan_gesture_a.png` frame 0), or add an authored two- or three-drawing fin swish between the directional home pose and the gesture. Pick one after a side-by-side owner review. Do not mirror gestures (the ponytail would move). | Measured fin side at gesture entry and exit equals the home pose's; boss fight probes and the full suite pass |
| R3 | Hold career pose keys instead of looping them: one idle key, travel held, work and cheer as one-shot sequences (the Ballerina, Geologist and Teacher policy in `scripts/opera_roshan_actor.gd`). | No career row loops; Opera probes pass; owner sees each career before and after |
| R4 | Give gesture keys authored, unequal holds from their clip contracts instead of `len / 4` in `scripts/player.gd`; remove the `twirl` mid-spin mirror swap. | Clip timing matches the contract; probes pass |
| R2 (measure only) | Measure the castle swim with and without the cross-fade (`SMOOTHNESS_MULTIPLIER`) using `tools/measure_overdraw.py`, and show the owner both at normal speed. Do not remove it until clip 1 replaces the art or the owner prefers crisp holds. | Layer counts recorded; owner verdict recorded |

### RM3 — Pilot clip 1: the side-view slow swim

**Do:** from the RM0 spine (or, if nothing passes, one new Grok or local take
under G2–G5 below): pick 8–12 drawings that give a 0.8–1.2 s stroke with even
spacing (A1); register each to the side-view home pose (A3); repair at most
one or two drawings locally in Aseprite; write the timing chart in the job
card (A2); export a lossless atlas and timing JSON. Wire it into one castle
room behind a switch for an A/B against the current swim.

**Done when:** M1–M6 checks pass (right-facing side view; the tail drives;
fin and ponytail sides constant; follow-through visible; no blend or smear;
measured cycle length), the loop seam matches pose and direction, actual
Godot sampling is proven, the full probe suite passes and the owner has
reviewed the A/B at normal speed on the tablet. Device and child sessions
remain separate.

### RM4 — Clips 2, 3 and 11: start, stop, turn and dash

Build start and stop drawings that join the RM3 cycle at named phases, the
turn from directional headings 6, 7, 0, 1, 2 plus two breakdowns and a fin
swish, then the dash (0.4–0.6 s) under the same locks.

### RM5 — Clips 4–6: listening idle and work contact

Author the two- or three-drawing breath for the home pose (M7). Build a hand
and socket reference per view from existing frames (A4), then whole-figure
contact keys for scrub/wipe and scoop/carry/place with measured sockets. Then
make the Day One contact action, Pool skimmer and toilet travel with clips 1–3
and work with these keys instead of sliding a still cutout (R6, `MA-PLAY-004`).

### RM6 — Clips 7–10, 12, 13: the gesture family

Bring each gesture row to its view's home pose and fin side (M3), add one
breakdown per fast arc (M6), and set holds from the contracts.

### RM7 — Careers

After RM2's holds, propose to the owner whether costume travel rows should be
redrawn to the M1–M2 side swim (15 career atlases) or whether careers keep held
travel poses. No redraw before that answer.

### RM8 — Land travel (after Q5)

Design the Sky Lagoon land mode the owner chooses and replace the still
sliding card.

## 2. Grok handoff refinements (apply to any new Roshan job)

| ID | Refinement |
|---|---|
| G1 | Review the existing returns first (RM0). |
| G2 | Ask Grok for performances and timing reference (entries, exits, turns, delight beats), not seamless short loops; loops are assembled from picked drawings. |
| G3 | Extraction-ready backgrounds: a flat colour absent from Roshan's palette and tested with the cleanup path that produced the approved atlases; pilot once before adopting. |
| G4 | Bind `roshan_base.png` (or the side-profile directional cell) as identity; name brown hair, tied rainbow ponytail and tiara; add "fin root stays connected, curls follow through, arms stay near the chest, no water or sparkle effects". |
| G5 | Right-facing side view for every swim job (the game mirrors for left). |
| G6 | Use the shot-card template the owner confirms in Q3. |

## 3. Local pipeline refinements

| ID | Refinement |
|---|---|
| A1 | Pick, don't keep: select the drawings that give the M5 spacing and discard smeared transition frames instead of cleaning every native frame. Keep all native frames for provenance. |
| A2 | Timing chart (keys, breakdowns, holds, drawings per second) in the job card before generating; guides come from it. |
| A3 | Register to the home pose and check fin and ponytail side before generation. |
| A4 | Hand and socket reference per view, used when drawing whole-figure contact keys, never pasted onto a still body. |
| A5 | Move the pilot from the wave to clip 1. |
| A6 | Close the wave line unless a new method is chosen. |

## 4. Owner questions

The six questions and their defaults are in
[ANALYSIS.md section 12](ANALYSIS.md#12-owner-questions). RM0, R1, R3 and R4
can start on the defaults; RM1 waits for Q1, Q2 and Q4; RM8 waits for Q5.

## 5. Files

| File | Purpose |
|---|---|
| [ANALYSIS.md](ANALYSIS.md) | Findings, evidence, motion locks, clip set, refinements, questions |
| [data/motion_measurements.json](data/motion_measurements.json) | Measured fin and ponytail sides, frame-to-frame change, playback constants (numbers only) |
| [tools/measure_roshan_motion.py](tools/measure_roshan_motion.py) | Reproduces the measurements; writes no images |
| [MANIFEST.json](MANIFEST.json) | SHA-256 of every packet file |
