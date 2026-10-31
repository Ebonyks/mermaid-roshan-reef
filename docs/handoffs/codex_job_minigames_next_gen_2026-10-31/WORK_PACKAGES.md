# Work packages: the next generation of job minigames

- **Status:** `PROPOSED / CANDIDATE` work order for Codex, prepared by Claude
  as written specification only. It grants no implementation, art, voice,
  release or acceptance authority beyond the owner's answers.
- **Baseline:** dev `a0bb2cf4691631a534e210a5fb60fd227213322f`.
- **Freeze:** nothing here starts on dev before the demo build is promoted
  (`ODR-DEMO-FREEZE-20261031`; demo on Saturday 7 November). Two exceptions
  write no game code: NG0 (owner answers) and NG1 (two checks inside the demo's
  device rehearsal, DR6).
- **Every package:** its own branch from current dev, its own impact record and
  a green Probe Suite (`ODR-JOBART-PROCESS-20261018`); the gates and traps in
  [the demo handoff, section 8](../codex_demo_readiness_2026-10-31/README.md#8-gates-for-every-package);
  no change to `assets/book/`, `assets/audio/voices/` or
  `assets/characters/friends/`; no 3D resource; the Mobile renderer; one
  finger; a spoken line and a pointer for every objective; no fail state; save
  keys only added. Every new asset gets its `ASSET_LICENSES.md` line in the same
  commit. Report each package as three claims: implemented; machine-verified at
  an exact commit; acceptance still open.
- **Weakness IDs** (`JW-*`, `JX-*`) are in [WEAKNESS_REGISTER.md](WEAKNESS_REGISTER.md).

## 1. Order

| ID | Package | When | Depends on | Done when |
|---|---|---|---|---|
| NG0 | Owner answers and one decision record | Now; no code | – | The register's `--check` passes and the README's answers table matches it |
| NG1 | Two demo-route checks | Demo week, inside DR6; check only | Q1 | The rehearsal notes record pass or fail for both |
| NG2 | Land or close the parked career branches | After promotion, then weekly | – | Each branch merged with green CI or closed with a recorded reason |
| NG3 | Racer R1 | After NG2 | Q2, Q3, Q4 | [RACER_VERSIONS.md §7](RACER_VERSIONS.md#7-r1-acceptance) machine legs green |
| NG4 | Pop Star: BeatKit, then Roshan's Rainbow Band | After NG2 | Generation 1 answers | [POP_STAR.md](../codex_minigame_rebuilds_2026-10-17/POP_STAR.md) section 11 machine legs green |
| NG5 | Ballerina: Lamma's Music-Box Ballet | After NG4's BeatKit | Generation 1 answers | [BALLERINA.md](../codex_minigame_rebuilds_2026-10-17/BALLERINA.md) section 11 machine legs green |
| NG6 | Chef: the owner's look, then repairs | Look in demo week; repairs after promotion | – | Verdict recorded; repairs green |
| NG7 | Part 2 story-job repairs, in play order | After promotion | NG1 results | Each job's legs below green |
| NG8 | Free-play career repairs | After NG7 starts | – | Each career's legs below green |
| NG9 | The shared career shell | Alongside NG7 and NG8 | – | Legs below green |
| NG10 | Records, rule facts and fresh scores | After NG2 | – | `python -B tools/gold_star.py --check --strict` passes |
| NG11 | Tooling for the job cycle | After promotion | Q7, Q8 | Each tool's check runs in `scripts/ci.sh` |
| NG12 | Acceptance lanes | After each landing | – | Device, child and owner results recorded separately |

Suggested order after promotion: NG2, then the cheap story-route repairs in NG7
(no new art for most) and NG9a, then NG4, NG3 and NG5, then NG8 by lens score
(README Q5). The demo-day notes may reorder it; JC1 in
[SELF_IMPROVEMENT_AUDIT.md](SELF_IMPROVEMENT_AUDIT.md#3-one-cycle-jcn) decides.

## 2. Packages

### NG0. Owner answers and one decision record (now, no code)

- Ask README Q1 to Q8. Record the answers with
  `python -B tools/record_owner_decision.py --answers PATH --cycle job-next-gen-20261031 --answered-on DATE`,
  which writes `design/reference/owner_decisions.json`, its view
  `design/reference/OWNER_DECISIONS.md` and
  `audit/cycles/job-next-gen-20261031/owner_answers.json`.
- For Q2, record one Racer decision that names what it supersedes:
  `ODR-RACER-VIEW-20261018`, or the 2026-10-22 direction that exists only on
  `codex/racer-castle-integration-20261022`. Either way the register ends with a
  single current Racer direction.
- Publish handoff revision 2 with the answers table filled in. Under the
  freeze, the answers live on this packet's branch and reach dev with it after
  promotion.

### NG1. Two demo-route checks (inside DR6; check only)

The demo plays the whole Part 2 story (`ODR-DEMO-PART2-SCOPE-20261031`), and
two of its steps may not be finishable by an untrained finger
([`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015)):

1. **Candy Maker story SORT (party job 3).** On the demo device, a grown-up
   who has not seen the code finishes the step using only what is drawn. Note
   whether they could find where to touch and how long it took.
2. **Detective story candle (party job 8).** Tap the middle and then the lower
   half of the drawn candle. Note which taps reveal the clue.

Record pass or fail in the rehearsal notes. A failure is a demo blocker only if
the owner says so (Q1). If he asks for a fix, the smallest truthful one for
the candle is to set the touch box to the candle art's drawn rectangle; for
SORT, to bind the drag to the drawn berries and tray. Each would be a DR5
change, with its own probe leg using the drawn positions rather than the hidden
ones.

### NG2. Land or close the parked career branches (after promotion, then weekly)

| Branch (tip) | Recommendation |
|---|---|
| `codex/popstar-rhythm-rebuild-20261022` (`7eada836`) | Bring current dev in; land `beat_kit.gd` and its probes as generation 1's MR1; keep the band preview isolated; the rejected pilot takes stay out. Feeds NG4 |
| `codex/racer-castle-integration-20261022` (`96d6ef9e`) | If Q2 is R1, it becomes NG3's base (NG3a). Otherwise keep it parked as history |
| `codex/opera-imp-contests-20260930` (`66420ae7`, pull request #17) | Twelve built job contests, green on 2026-10-01 against older code. Refresh onto dev or mine for NG9c. Its commit also edits `.github/workflows/probes.yml`, a high-risk path that needs the owner's explicit yes |
| `codex/arborist-spray-20261015` (`941cb76d`) | Land: the owner-reported spray fix (JW-ARB-2) |
| `codex/opera-foyer-movement-20261017` (`2668ad75`) | Land: the owner chose it for after the demo (demo Q3) |
| `codex/racer-existing-engine-2d-20261003` (`fcee911c`, pull request #21) | Close as superseded by V3; keep `assets/kart/canvas/*` available for R2 |
| `codex/astronaut-clearance-20261006`, `codex/doctor-clearance-20261006`, `codex/magician-clearance-20261006`, `codex/nursery-clearance-20261006`, `codex/candymaker-walkthrough-20261007` | Review documents only: land the documents that are still true or close the branches with a reason |

### NG3. Racer R1 (after NG2; Q2 to Q4)

Specification: [RACER_VERSIONS.md §6](RACER_VERSIONS.md#6-the-recommended-combination-r1).
If the owner chooses R2 instead, build
[RACER.md](../codex_minigame_rebuilds_2026-10-17/RACER.md) with the donor parts
in [RACER_VERSIONS.md §8](RACER_VERSIONS.md#8-the-alternative-r2-if-the-owner-keeps-the-side-scroller).

| Step | Work | Proves it |
|---|---|---|
| NG3a | Bring V3 onto current dev (128 files changed against its base `9c78f6aa`); full suite green; no behaviour change | Existing `probe_racer_integration`, `probe_opera_2d` and the full suite |
| NG3b | Head to head: Roshan and the imp only; the protected friend portrait and the book dolls leave the race (Q3) | Roster assertion |
| NG3c | Lanes and the driving rule: three lane positions; a tap on a half moves one lane; drag also works; a 0.4 s glide; the lane holds through curves; a held finger drives but cannot change lane; the turbo button goes | Legs 1, 2 and 5 |
| NG3d | The pit stop replaces TUNE and TO THE LINE (Q4): one of three colours, remembered; two glowing wheel spots; each wheel counts only after Roshan's hand has been in contact (pattern GS-01) | Contact assertion; additive save key with a default |
| NG3e | The imp contest from V6's logic: his two-lap finish is his win; a beat of at most 2 s; restart with everything kept; the first restart at his pace; half speed after two of his wins for the rest of the visit; ties to her; he moves only while she plays | Legs 3 and 4 |
| NG3f | Finish: photo flash, podium, trophy; medals from honest play (pattern GS-13) | Medal assertions from play statistics |
| NG3g | Voice, after the freeze, with the existing synthetic workflow: proposed lines "Tap a lane to drive!", "Pick a color for your kart!", "Tap a glowing wheel!", the imp's "Race you! First one home wins!", "Lap two! Keep going!", his short win line and "Rematch! Go, go, go!", and "We won the race!" | Exact-key coverage; no generic fallback |
| NG3h | Art, by Codex, after the freeze: pilot the Movie Lounge stretch of road and one whole-frame Roshan driving set; the owner looks; then the other rooms, the imp's kart and three kart colours from `assets/kart/chase/*` | Provenance, licences and hashes; overdraw OD1 to OD6 |
| NG3i | Records: rewrite `DL-INT-10`; update `MA-OPERA-014` (Racer part) and `MA-OPERA-010`; re-assess the Racer's gold-star entry and lens; retire V1 | `python -B tools/gold_star.py --check --strict` |

### NG4. Pop Star (generation 1's MR1 and MR2)

- Land BeatKit from the parked branch (NG2) with `probe_beatkit`; MR1's done
  condition includes proving the clock on the target device.
- Build Roshan's Rainbow Band as
  [POP_STAR.md](../codex_minigame_rebuilds_2026-10-17/POP_STAR.md) specifies,
  inside the owner-accepted direction: the timed echo plus play-along, the
  original song first, Daddy and Baby Eagle as the band.
- The story (party job 6) keeps Rumi; its STAGE RUMI line gets a true recording
  (NG9a).

### NG5. Ballerina (generation 1's MR3)

- DR5 removes the stuffie picker from the ballet for the demo.
- Build Lamma's Music-Box Ballet as
  [BALLERINA.md](../codex_minigame_rebuilds_2026-10-17/BALLERINA.md) specifies,
  on BeatKit's clock. The story version (party job 5) keeps the record that
  the show has no star until Lamma joins.
- Its PEARL MIRROR, TWIRL and BOW lines are replaced by the rebuild's own exact
  lines.

### NG6. Chef

- The owner looks at the painted Chef on the demo tablet; this needs no build.
  Record his verdict with `tools/record_owner_decision.py`; it confirms or
  replaces `ODR-CHEF-VERDICT-20261003`.
- Then, following his words: the approved guide hand at each story station in
  place of the 5 px dot (GS-04); frosting start and topping anchors at least
  110 px (C4); a held pour released on focus loss (GS-10); the pour direction
  checked against "pours backwards"; a per-phase checkpoint (GS-12).

### NG7. Part 2 story-job repairs, in play order

| Step | Job | Work | Proves it |
|---|---|---|---|
| NG7a | Farmer | After DR5's next-door marker: show the meadow rows so Roshan's path runs on ground (JW-FARM-2); picked berries go into the basket instead of staying as ghosts (JW-FARM-3) | Crop assertion on the story backdrop; berry visibility per pick |
| NG7b | Candy Maker | Bind each story step's touches to the drawn berries, tray and cake, so the visible object is the hit region (GS-05; JW-CANDY-1); story SORT either uses berries that really differ, from existing art, or stops asking for colours (JW-CANDY-2). Its place in the story waits on Q6 | A real-touch leg at the drawn positions; a far touch earns nothing |
| NG7c | Painter | Keep her marks: the prototype's closed-region fill, or her stamps kept on the banner she hangs (JW-PAINT-1); story STAMP places birthday stars; story PAINT shows the Main Hall banner (JW-PAINT-3) | The hung banner carries her stamps after re-entry |
| NG7d | Astronaut | A two-finger probe across every pipe round with cancel and re-entry, closing `MA-OPERA-013`'s open scope (JW-ASTRO-1); a countdown that exists (three painted lights with the existing chime) or a line that does not promise one (JW-ASTRO-2) | Second-finger legs on all three boards |
| NG7e | Detective | Remove the timed retry's progress reset (JW-DET-1); keep the rival race out of story runs by fixing the finale clamp (JW-DET-4); set the candle's touch box to the drawn candle (JW-DET-2); draw the story board's targets (JW-DET-3); pause the rival clock on focus loss (JW-DET-7); paint out the "missing" crown (`MA-OPERA-002`) | Legs: no progress loss after 40 s; a tap on the candle's lower half reveals the clue; no rival line in a story run |

### NG8. Free-play career repairs

| Step | Career | Work |
|---|---|---|
| NG8a | Boxer | The true GLOVE GUIDE instruction: no recording until a new exact line exists (NG9a), then the line; a distance cutoff for claiming a glove (JW-BOX-2); Roshan visible at the start and at the belt (JW-BOX-3) |
| NG8b | Magician | Ignore TRACK taps while the hats glide and pay no crumbs for wrong hats (JW-MAG-1); extend generation 1's retirement of the practice copies and the time-paced stage race to the Magician (JW-MAG-2) |
| NG8c | Stuffie Doctor | FIND pays nothing for a wrong plushy, and the right one reacts (JW-DOC-1); the scan and the cast happen on the patient Roshan reached (JW-DOC-3) |
| NG8d | Nursery Nurse | Faron reaction poses from existing art, or new art after the freeze; the pat lands on the baby; held WASH and FEED cancel on focus loss (JW-NURSE-1, JW-NURSE-3) |
| NG8e | Geologist | No recording for RIVER, PAN and GEODE until four exact lines exist (NG9a), then the lines; the cooperative win caption names the Geologist's team, not the nursery; its music cue in `tools/build_area_music.py`; its sheet in the atlas gate (JW-GEO-1, JW-GEO-3, JW-GEO-5) |
| NG8f | Teacher | A pearl layout with non-overlapping hit regions of at least 110 px (JW-TEACH-1); either show the learning buddy or stop thanking one (JW-TEACH-3); speak the idle help line (JW-TEACH-4) |
| NG8g | Arborist Tree Book | Alpha on the tree choices, so no navy box gives the answer away (JW-ARB-1), after NG2 lands the spray fix |

Each step adds a real-touch probe leg for its change, a zero-input leg, and a
re-score of the criteria it touched.

### NG9. The shared career shell

| Step | Work | Proves it |
|---|---|---|
| NG9a | **Voice truth.** For every phase in [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004), play no recording until a true one exists, so nothing wrong is said and the caption returns for the grown-up; this is the audio director's own rule, "play only the exact semantic recording". Then record the true lines after the freeze with the existing synthetic workflow (status `MA-AUDIO-001`) | The voice-truth check (NG11, item 4) reports no mismatch |
| NG9b | **Curtain call.** Each career's own win line spoken (exact recordings after the freeze); the finished job object shown at the curtain; no digit overlay for a non-reader; a cheer tier she can see | Win-line keys exact; overlay has no digits |
| NG9c | **From pacer to contests.** Retire the wall-clock pacer; keep story runs free of imps and race bars (`DL-INT-14` and the contest design's rule C13); build each career's contest, mining V6's twelve contests after refreshing them onto dev | No rival in any story run; each contest's own legs |
| NG9d | **Input pay and focus.** Wrong taps in choice, timing, echo and oven modes pay nothing, or so little that correct play is always faster (`DL-AGE-05`); the shared surface cancels held input on focus loss (GS-10) | Masher legs slower than correct play; focus-loss legs |
| NG9e | **Resume.** Per-phase checkpoints for the ten careers without one (GS-12); the checkpoint validators accept each career's real phase count instead of capping at 4; leave the 262143 star clamp alone unless an 18th bit is added, and then follow the takeover audit's save-clamp procedure | Save and re-entry legs per career |

### NG10. Records, rule facts and fresh scores

- Rewrite `DL-INT-07` with counts taken from the code at the landing head (15
  careers, 61 phases and 36 modes at this baseline), `DL-INT-12` (the Library
  hosts the Detective, Geologist and Teacher), the slot count in `DL-SAVE-06`
  and the `DL-QA-12` table, each as a rule change with its evidence.
- Re-assess all 15 careers on the gold star (its recipe, steps 1 to 5),
  `--rebind` each, and re-measure overdraw (needs a display).
- Listen to the Magician's current route and update `MA-ACCESS-002`.
- Correct the job-art ledger row's revision number and the demo receipt's
  status note; record the rebuild handoff's revision-2 verification or mark it
  not done.

### NG11. Tooling for the job cycle

The eight items in
[SELF_IMPROVEMENT_AUDIT.md §5](SELF_IMPROVEMENT_AUDIT.md#5-tooling-the-cycle-needs-codex-after-the-freeze),
each with a unit test in `tools/tests/` and a check in `scripts/ci.sh`. Item 6
(the lens as data) waits on Q7; item 8 (`gold_star.py --check` in remote CI)
changes `.github/workflows/` and waits on the owner's explicit yes (Q8).

### NG12. Acceptance lanes

For each landed career change: a session on the Lenovo Tab M11 (frame pacing
and touch), one observed child session and the owner's verdict, recorded under
[`MA-PERF-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-001),
[`MA-CHILD-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-child-001)
and `DL-QA-06`. Machine success never stands in for any of them (`DL-QA-07`).
