# Job minigames, next generation: Codex handoff

- **Status:** `PROPOSED / CANDIDATE`, revision 1 (2026-10-31). Eight owner
  questions are open with stated defaults (section 7). Publication grants no
  visual, device, child or owner acceptance of any game.
- **Prepared by:** Claude, as written analysis and specification only: no game
  change and no image (CLAUDE.md "Claude writes, Codex builds images"). Codex
  implements.
- **Recipient:** Codex.
- **Generation:** 2. Generation 1 is the
  [2026-10-17 rebuild handoff](../codex_minigame_rebuilds_2026-10-17/README.md)
  for Pop Star, Ballerina and Racer. This packet keeps its owner-accepted Pop
  Star and Ballerina directions, reopens the Racer's because of the owner's
  later words, and extends the work to every career.
- **Evidence baseline:** dev `a0bb2cf4691631a534e210a5fb60fd227213322f`
  (2026-10-31). The work branch head `511b0690` adds only Day Two documents.
- **Freeze:** under `ODR-DEMO-FREEZE-20261031` nothing here starts on dev, and
  this packet does not merge into dev, until the demo build is promoted (demo
  on Saturday 7 November). NG0 (answers) and NG1 (two checks inside the demo
  rehearsal) write no game code.
- **Delivery:** this folder on branch `ccr-ba906acd-1aepcb` of the project's
  GitHub repository, with a SHA-256 manifest ([MANIFEST.json](MANIFEST.json))
  and an anonymous remote-verification receipt.
- **Records:** opens
  [`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015)
  and
  [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004);
  adds history to
  [`MA-OPERA-014`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-014)
  and
  [`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009);
  [impact record](../../../design/audit_impacts/job-minigames-next-gen-handoff-20261031.json).

## 1. The request

The owner, 2026-10-31: "Use this as a guide for next generation iterative
deisgn handoff. Identify the weaknesses of each individual game, giving the
racing game particular focus of going through all of the comprehensive
versions of this to determine which version (or combination of versions) is
best for the final game. Create a hand off to update these games, as well as a
self-improvement audit to analyze and continue to develop the existing job
minigames".

How this packet reads it:

- **"Use this as a guide"** points at the correction just before it, when the
  owner said the Day Two job fits were wrong and "this information should be
  on record". The method is the same: search every branch and record first,
  quote the owner's words beside each claim, keep owner decisions apart from
  proposals, and never invent a fit.
- **"Each individual game"** is the 15 live careers plus the Arborist Tree Book
  practice.
- **"Next generation"** follows generation 1. Its owner answers stand except
  where later owner words conflict, and those are put back to the owner.

## 2. The verdict for every game

Weakest first by the job lens (JL1 to JL6, 0 to 12; defined in
[SELF_IMPROVEMENT_AUDIT.md](SELF_IMPROVEMENT_AUDIT.md#2-the-job-lens)). Gold-star
points are the stale 2026-10-03 values. Evidence is in
[WEAKNESS_REGISTER.md](WEAKNESS_REGISTER.md).

| Career | Lens | Gold star | What is weakest | Next change | Package |
|---|---|---|---|---|---|
| Racecar Driver | 2 | 15 | Holding a bar wins; steering moves 19 px; she always wins; the line names gates that do not exist | R1, the combination in section 3 | NG3 |
| Pop Star | 2 | 13 | No beat; seven chores, three twice; Roshan never sings or plays; the lane shows the answer | BeatKit, then Roshan's Rainbow Band (generation 1) | NG4 |
| Ballerina | 3 | 14 | The demonstration taps the answer first; nothing follows the waltz; the first line says "watch", not "tap"; the story's picker covers the ballet | DR5 picker fix; then Lamma's Music-Box Ballet (generation 1) | NG5 |
| Candy Maker | 4 | 10 | Story steps take touches on an invisible surface; "matching color" for identical berries; placed in the Kitchen against the owner's 2026-09-29 ruling | Bind story touches to the drawn berries; place per Q6 | NG1, NG7b |
| Painter | 5 | 11 | Nothing she makes is kept; stamps are any five taps | Keep her marks on the banner | NG7c |
| Detective | 6 | 9 | A timed rival wipes finished work; the story candle's touch box misses half the candle; an invisible story board | No reset; fit the candle box; draw the board | NG1, NG7e |
| Farmer | 6 | 11 | Her first Part 2 step is two doors away behind a door that does not glow; a sky seam under her path | DR5 door; crop and ghost berries | NG7a |
| Astronaut Engineer | 6 | 10 | Second-finger tile loss unproven on every round; a promised countdown that never comes | Two-finger proof; a real countdown or a true line | NG7d |
| Magician | 6 | 15 | Taps score while the hats glide; wrong hats pay; practice copies | Ignore glide taps; drop the copies | NG8b |
| Pastry Chef | 7 | 10 | Not accepted by the owner ("pours backwards", "overdraw"); 5 px story pointers | The owner's look at the painted Chef, then repairs | NG6 |
| Stuffie Doctor | 7 | 11 | Mashing pays in FIND; play on a side panel | Care pays; act on the patient | NG8c |
| Boxer | 7 | 16 | The first line is wrong and is the only instruction; Roshan hidden | A true first line | NG8a, NG9a |
| Geologist | 7 | 11 | Three steps say "A secret grotto!" and nothing else; the win thanks the nursery | True lines; a true win caption | NG8e, NG9a |
| Arborist Tree Book | 7 | – | Navy boxes give the answer away; spraying without hand contact | Land the spray fix; alpha | NG2, NG8g |
| Teacher | 8 | 15 | 72 px pearls 88 px apart; she is the pupil, not the teacher | Larger pearl targets | NG8f |
| Nursery Nurse | 9 | 14 | Faron frozen; the pat lands anywhere | Faron reactions; pat on the baby | NG8d |

What every career shares (register section 4): a wrong recording becomes the
only instruction, because the Opera hides the caption whenever a recording
exists; one shell for every job; a wall-clock rival instead of the owner's imp
contests; a generic "Yay! I did it!" payoff; wrong taps that pay; held input
that survives focus loss; ten careers that restart from the beginning; records
that count 13 careers where the code has 15.

## 3. The racing decision

Ten racing builds exist in four families
([RACER_VERSIONS.md](RACER_VERSIONS.md)). **Recommended: R1, a combination.**
The engine, road view and castle-room course come from the restored Canvas
racer on `codex/racer-castle-integration-20261022` (`96d6ef9e`). The child
rules come from the Reef Grand Prix specification: three lanes chosen by a tap,
holding as the slowest way, and a pit stop instead of the chores. The contest
comes from the imp-contest branch: the imp can win, the race restarts with
everything kept, and he slows to half speed after two wins. The race is head
to head.

Why: the owner's own words point at the existing game three times in October
(2026-10-03: "Converting this engine to our racing engine, versus any others,
is a priority"; 2026-10-17: "the racer (there are several games build in this
minigame that are superior)"; 2026-10-22: "Integrate thei superior game ... Use
the tracks that were generated from the various rooms in the castle"). The
2026-10-18 answer chose between two options that left that game out. The
built game keeps V1's flaws (holding drives, the imp cannot win, the chores),
which the Reef Grand Prix rules and the contest remove. If the owner keeps the
side-scroller, R2 builds it with donor parts from the built versions. The
choice is Q2.

## 4. What this audit found that changes earlier plans

1. **Two racing directions conflict, and two owner directions live only on
   branches.** The 2026-10-03 priority and the 2026-10-22 direction are absent
   from dev's decision register; the 2026-10-22 row would vanish if the
   register's view were regenerated.
2. **The gold star does not predict the owner.** It ranks the three careers he
   rejected mid-table. The job lens adds the missing judgement and is
   calibrated against every recorded verdict.
3. **Wrong recordings are the only instruction** on eight free-play and story
   phases in five careers
   ([`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004),
   new).
4. **Two Part 2 steps on the demo route may not be finishable by an untrained
   finger**: the Candy Maker's story SORT and the Detective's candle
   ([`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015),
   new). NG1 checks them during the rehearsal.
5. **Much is built and parked:** BeatKit, the castle-room racer, twelve imp
   contests (pull request #17), the Arborist spray fix and the foyer movement.
6. **The improvement loop stopped on 2026-10-03,** and every career's gold-star
   score is stale.

## 5. Files

| File | Role |
|---|---|
| `README.md` | Entry point: request, verdicts, racing decision, work order, owner questions |
| [`WEAKNESS_REGISTER.md`](WEAKNESS_REGISTER.md) | Every career's weaknesses with code anchors, severities, plans and next changes; shared weaknesses; stale records |
| [`RACER_VERSIONS.md`](RACER_VERSIONS.md) | All ten racing builds, the owner's words on racing, the comparison, R1, its acceptance and the R2 alternative |
| [`WORK_PACKAGES.md`](WORK_PACKAGES.md) | Packages NG0 to NG12 with steps and proofs |
| [`SELF_IMPROVEMENT_AUDIT.md`](SELF_IMPROVEMENT_AUDIT.md) | The job lens, the repeatable job cycle, lessons, tooling and the JC0 baseline |
| [`data/job_lens_jc0.json`](data/job_lens_jc0.json) | The JC0 lens scores and gold-star snapshot as data for the next cycle |
| `MANIFEST.json` | Byte sizes and SHA-256 of every file |
| `REMOTE_VERIFICATION.json` | The anonymous fetch receipt for the published revision (added in the commit after it) |
| `.gdignore` | Keeps Godot from importing this folder |

## 6. Work order for Codex

| ID | Package | When |
|---|---|---|
| NG0 | Owner answers and one decision record | Now; no code |
| NG1 | Two demo-route checks inside DR6 | Demo week; check only |
| NG2 | Land or close the parked career branches | After promotion, weekly |
| NG3 | Racer R1 (or R2) | After NG2 |
| NG4 | Pop Star: BeatKit, then Roshan's Rainbow Band | After NG2 |
| NG5 | Ballerina: Lamma's Music-Box Ballet | After BeatKit |
| NG6 | Chef: the owner's look, then repairs | Look in demo week |
| NG7 | Part 2 story-job repairs in play order | After promotion |
| NG8 | Free-play career repairs | After NG7 starts |
| NG9 | The shared career shell (voice truth, curtain call, contests, input pay, resume) | Alongside NG7 and NG8 |
| NG10 | Records, rule facts and fresh scores | After NG2 |
| NG11 | Tooling for the job cycle | After promotion |
| NG12 | Device, child and owner acceptance | After each landing |

Steps, proofs and dependencies are in [WORK_PACKAGES.md](WORK_PACKAGES.md). The
first job cycle (JC1) runs the week after the demo and re-orders this list from
the demo notes.

## 7. Owner questions

Each has a default. Defaults are not recorded as answers until the owner gives
them.

| # | Question | Default |
|---|---|---|
| Q1 | Demo week: add the two Part 2 checks (the Candy Maker's story SORT and the Detective's candle) to the DR6 rehearsal? | Yes, check only; a fix enters DR5 only on a separate yes |
| Q2 | Racer: (a) R1, the castle-room game you asked for on 2026-10-22 with lanes, a pit stop and an imp who can win; (b) R2, the side-scrolling Reef Grand Prix from 2026-10-18, built new with parts of the existing game; or (c) the castle-room game as built, adding only the imp contest? | (a) R1. The answer becomes the one current Racer decision |
| Q3 | Racer field: Roshan against the imp only, or keep the eight-kart pack that races Princess Huluu's portrait, five book dolls and Baby Eagle as "Sparkle"? | The imp only (`DL-INT-14`'s head-to-head contest) |
| Q4 | Racer warm-up: replace TUNE and TO THE LINE with the pit stop (pick a colour, fit the wheels)? | Yes |
| Q5 | Order after the demo: the demo notes, then the cheap Part 2 repairs and the voice-truth fix, then Pop Star, Racer and Ballerina, then the free-play careers by lens score; or the three rebuilds first? | The cheap Part 2 repairs first |
| Q6 | Candy Maker: your 2026-09-29 ruling keeps it out of the Kitchen, but the build has it there as party job 3. Move it now, or decide with the Day Two draft's job list (which replaces it with the Arborist) and only fix its story input until then? | Decide with the Day Two list; fix the input now |
| Q7 | Keep the job lens as advisory evidence beside the gold star, or fold it into the gold-star rubric for careers, which changes every career's score? | Advisory |
| Q8 | Add `gold_star.py --check` to the remote Probe Suite? It changes `.github/workflows/`, which needs your explicit yes | Not now; ask again after two job cycles |

## 8. Relationship to other work

- **Generation 1** ([rebuild handoff](../codex_minigame_rebuilds_2026-10-17/README.md)):
  POP_STAR.md and BALLERINA.md stand as specified; RACER.md becomes R2 unless
  Q2 chooses it; SHARED_SYSTEMS.md's BeatKit and contest adapter are reused.
- **Demo readiness** ([demo handoff](../codex_demo_readiness_2026-10-31/README.md)):
  the freeze, DR5 (picker and door) and DR6 (rehearsal, where NG1 adds two
  checks). Its parked list includes "the minigame review"; this packet is
  written work and waits the same way.
- **Job art** ([job-art handoff](../codex_job_art_imagegen_2026-10-17/README.md),
  [`MA-VIS-010`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-010)):
  P7 (Detective and Candy Maker) and P8 (shared layers) continue; R1's art is
  new work under the same process.
- **Imp contests** ([contest design](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md),
  `DL-INT-14`): the twelve built contests on pull request #17 feed NG9c; R1's
  contest follows OD-E's "radically slow down".
- **Day Two draft** (`design/day_two_story_v2/`, `CANDIDATE` on this branch):
  the job canon on record (the Astronaut's invitations, Lamma as the star, the
  Pop Star's band, the Detective's candle). Q6 and JW-ASTRO-6 wait on its
  owner decisions.
- **Job Platform** ([architecture](../codex_job_platform_architecture_2026-09-30/ARCHITECTURE.md),
  [`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006)):
  if its content layer lands first, express these careers in it.
- **Improvement loop** ([`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009)):
  the job cycle is its job lane; it adds no schedule (`ODR-LOOP-Q3`).

## 9. Three separate claims

- **Implemented:** nothing in the game. This packet is analysis,
  specification, two new findings and record updates.
- **Machine-verified:** the document-authority and development-coverage gates
  for this change, and the anonymous byte check of the published files
  (`REMOTE_VERIFICATION.json`).
- **Outstanding:** the owner's answers to Q1 to Q8, and every runtime, art,
  voice, device, child and owner gate for every package.
