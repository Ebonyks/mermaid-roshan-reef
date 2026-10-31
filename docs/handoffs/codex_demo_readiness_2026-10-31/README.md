# Demo readiness work order (November 2026 demo)

Status: `PROPOSED / CANDIDATE`. Prepared by Claude for Codex: written
analysis, priorities and acceptance criteria only. No game, art or audio
change and no images. Evidence baseline: dev
`218ae766f8e60afb3f6338b8fafce28ec9fab7f2` (2026-10-31), whose Probe Suite
run 41215786419 passed.

Files: this README (priorities and work packages), [AUDIT.md](AUDIT.md)
(analysis of each high-priority fix, with code references),
[DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) (release candidate, device rehearsal,
promotion, rollback and demo day) and `MANIFEST.json`.

## 0. The request

Owner, 2026-10-31: "We're seeking to publish a demo of this game next week
for Roshan. We're going to place a cap on new development, it's okay if part
2 doesn't completely resolve at this point. With that said, identify
priorities to work through before a demo, identify areas of needed
improvement and work to develop plan to implement these changes. Provide
analysis of high priority fixes in handoff for codex".

How this packet reads it:

- **Publish a demo** means promoting `dev` to `master` through
  `promote.yml`, so the stable `android-test` bookmark on her device gets the
  demo build.
- **Part 2** is Day Two: everything after the Grand Puff fight and the Day Two
  card (the Chapter 2 party careers, the Opera venue, the lawn finale and the
  other castle destinations).
- **A cap on new development** is a feature freeze: from now until the demo
  build is promoted, `dev` takes only the packages below.

## 1. Where things stand

Verified on 2026-10-31 unless stated otherwise. Details and commands are in
[AUDIT.md section A](AUDIT.md#a-release-state).

- Her device runs the stable build of `master` `ff68f955`, promoted
  2026-08-31. `dev` is 548 commits ahead and can fast-forward.
- The `android-dev` APK is 817,288,640 bytes; the stable APK is 604,039,545.
- No device session or child session has been recorded for the current line
  (`MA-PERF-001` and `MA-CHILD-001` are `BLOCKED_EXTERNAL`). The demo is the
  first one.
- Six finished owner-requested repairs are not on `dev` (section 4), and one
  owner decision, `ODR-GRAND-PUFF-COLD-20261017`, exists only on a branch that
  was never pushed.
- All 17 commits that reached `dev` since 2026-10-28 replace flat art in the
  Geologist and Dolls activities. Four new Codex sessions started on
  2026-10-31.
- The code review found two blockers on what she will see: three story clips
  play under a black screen (`MA-VIS-011`), and one tap in the Opera Hall
  opens a "DEV MODE" job menu. It found no soft-lock, crash or progress loss
  on the Day One route, and every Part 2 story link exists in code.

## 2. What "demo ready" means

One promoted build, rehearsed on the demo device, in which:

1. Day One plays from a fresh save and from her existing save to the Day Two
   card without getting stuck, without losing anything and without a crash.
2. Every objective on that route has a spoken line and a moving pointer
   (`DL-AGE-01`, `DL-SND-01`).
3. After the Day Two card, every visible destination either works to its end
   and back or is visibly closed with a spoken reason. Part 2 does not need to
   finish, but it must not open onto an empty screen, a soft-lock or a grown-up
   menu (`DL-AGE-06`).
4. No grown-up surface, permission pop-up or debug text reaches the child.
5. Installing over the old app keeps her save, and her save routes correctly
   in the new build (`DL-SAVE-01`, `DL-SAVE-05`).
6. Twenty minutes of play on the device without stutter that she notices,
   heat or a long freeze (`DL-PERF-02` is the target, the demo check is the
   adult's notes).

## 3. Freeze rules

Until the demo build is promoted:

- Merge into `dev` only the packages in section 5, each on its own branch
  with one impact record and a green Probe Suite (`ODR-JOBART-PROCESS-20261018`
  already asks for one branch per package).
- Park, do not merge: the flat-vector art campaign after R118, the Pop Star
  rhythm foundation, the Racer integration (unless the owner keeps it in scope,
  Q3), the Fashion work, the Opera exploration prototype, the minigame review,
  the rig stress test, the audit self-refinement, the learning-sessions
  packet, the Rumi book and the picture book. Parked work loses nothing; it
  resumes after the demo.
- No new art, voice or music, except what a package below names.
- No change to protected paths (`assets/book/`, `assets/audio/voices/`,
  `assets/characters/friends/`) or to the Day One story clips (`DL-CIN-16`).
- Do not add 3D resources; do not patch a probe to accept a regression.
- High-risk files (`.github/workflows/`, `CLAUDE.md`, `AGENTS.md`,
  `SECURITY.md`, `.claude/`, `.codex/`) need an explicit owner request. The
  only package that could touch one is DR3c's canon text, and only on an
  explicit yes to Q2.

## 4. Finished work that is not on `dev`

`git cherry origin/dev <branch>` lists every commit below as missing from
`dev`. Full SHAs and overlap checks are in
[AUDIT.md section B](AUDIT.md#b-finished-repairs-stranded-off-dev).

| Branch (tip) | What it fixes | For the demo |
|---|---|---|
| `codex/pool-visual-repair-20261017` (`8c4069c2`) | Owner-requested Pool repair; also fixes `MA-TOUCH-004`, the dropped fast taps in the seahorse rescue | Land (DR3) |
| `codex/studio-scene-integration` (`b5f78e3a`) | Owner-requested Art Room furniture states and a ghost/alpha leak after reload | Land (DR3) |
| `codex/grand-puff-care-20261017` (`e0abe9c9`, never pushed) | Owner decision `ODR-GRAND-PUFF-COLD-20261017`: Grand Puff is a friend with a cold | Push now (DR0); land if the owner says yes (Q2) |
| `codex/opera-foyer-movement-20261017` (`2668ad75`) | Owner-reported immobile Roshan and unresponsive games in the Opera foyer | Park; the venue's doors still launch the story job without it (AUDIT D). Land after the demo unless the owner asks for it now (Q3) |
| `codex/racer-castle-integration-20261022` (`96d6ef9e`) | Owner-directed restore of the full Canvas Racer | Park unless the owner keeps it (Q3) |
| `codex/arborist-spray-20261015` (`941cb76d`) | Owner-reported spraying fix in the optional Tree Book practice | Park unless Part 2 shows it (Q3) |

## 5. Priorities and work packages

Priority order. **Must** items are the demo; **should** items make it
understandable without an adult; **after the demo** items wait without harm.

| Priority | Package | Why |
|---|---|---|
| Must | DR0 Protect and freeze | Her save and an unpushed owner decision exist in one place each |
| Must | DR1 Story clips visible | The castle reveal and the climax play as a black screen |
| Must | DR2 No grown-up surfaces | A "DEV MODE" menu is one tap away in Part 2 |
| Must | DR6-DR7 Rehearse, then promote | The build has never run on her device |
| Should | DR3 Land the finished Day One repairs | Owner-requested, already built, one fixes dropped taps |
| Should | DR4 Day One guidance | A silent or wrong line at four Day One moments |
| Should | DR5 Part 2 shaping | Picker over the ballet; voice promises a glowing door that never glows |
| After the demo | [AUDIT F](AUDIT.md#f-areas-of-needed-improvement-after-the-demo) | Size, speed, pipeline, backups, voice sweep, Part 2 completion |

Merge order: DR1+DR2 (one branch), DR3a, DR3b, DR3c (if Q2 is yes), DR4,
DR5, then the release candidate. Each branch starts from current `dev`.

### DR0. Protect and freeze (Day 0, no game code)

- Push `codex/grand-puff-care-20261017` (`e0abe9c9`) to `origin` exactly as it
  is, before anything else happens in its worktree. The repository is public:
  first confirm the branch holds no save file or other private data.
- The owner or an adult follows [runbook R0](DEMO_RUNBOOK.md#r0-protect-what-cannot-be-rebuilt-before-anything-else):
  copy her save off the device, read the four keys listed in
  [AUDIT E2](AUDIT.md#e2-her-save-in-the-new-build--check-before-choosing-continue),
  keep today's stable APK.
- Codex parks the sessions listed in section 3 and merges nothing else.
- Done when: the branch is on `origin`; the save copy exists and opens as
  JSON; the stable APK and its `.sha256` are kept; Q1-Q8 have answers or
  defaults.

### DR1. Story clips visible (must) — [AUDIT C1](AUDIT.md#c1-three-story-clips-play-under-a-black-screen--blocker-ma-vis-011), `MA-VIS-011`

- In `_fade_cut` (`scripts/main.gd:3033-3052`), create the reveal tween with
  `set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` so the cover clears while a
  story clip has paused the tree. Keep `cb.call()` synchronous.
- Add a leg to `scripts/probe_day_one_story_clips.gd`: with `d1_castle`
  playing after castle entry, and again with `d1_puff_transformation` playing
  after a win, `fade_rect.modulate.a` reaches at most 0.02 within a few
  frames.
- Done when: a desktop display run shows the castle, transformation and
  epilogue clips; the new leg passes and fails when the pause-mode line is
  removed; all trusted probes pass; `MA-VIS-011` moves to
  `FIXED_PENDING_VERIFICATION` with that evidence.

### DR2. No grown-up surfaces (must) — [AUDIT D1, C5, C9](AUDIT.md#d1-one-tap-opens-a-dev-mode-job-menu--blocker-for-a-child-build)

- If Q5 keeps the default: `OperaJobPlaytestMenu.ENABLED := false`
  (`scripts/opera_job_playtest_menu.gd:6`), and change
  `probe_opera.gd`'s `_audit_job_playtest_menu` leg (`:368-438`) to assert
  that `OperaLeftElevatorPlaytest` is absent while disabled.
- Show the pause menu's FPS text only when `OS.has_feature("editor")`
  (`scripts/pause_menu.gd:62-65`, `scripts/main.gd:8241-8242`).
- Microphone per Q4 (default: no code; the adult switches Mic off in
  Options).
- Done when: no "DEV", "playtest" or "FPS" text can be reached by touch in the
  demo build; probes pass.

DR1 and DR2 are small and touch different code; ship them as one branch with
one impact record to save a CI cycle.

### DR3. Land the finished Day One repairs (should) — [AUDIT B](AUDIT.md#b-finished-repairs-stranded-off-dev)

Merge each source branch into a fresh branch from current `dev` (no rebase,
no history rewrite), resolve, update its existing impact record with a
reconciliation note, run the full local suite, then CI, then merge into
`dev`. One at a time, in this order:

- **DR3a Art Room furniture** (`b5f78e3a`). No script overlap.
- **DR3b Pool repair** (`8c4069c2`). Overlaps `castle_rooms_25d.gd`: rebuild
  the castle v3 manifest; re-merge `design/reference/overdraw.json` by hand.
  Fixes `MA-TOUCH-004`: move it to `FIXED_PENDING_VERIFICATION` with the
  fast-tap fixture result.
- **DR3c Grand Puff care** (`e0abe9c9`), only if Q2 is yes. No script
  overlap; merge the append-only documents, regenerate the audio quality
  ledger, and bring `ODR-GRAND-PUFF-COLD-20261017` into `dev`'s decision
  register. `CLAUDE.md` and `AGENTS.md` still state the earlier canon; change
  them only if Q2 explicitly approves that high-risk edit.
- Done when: each branch's own acceptance list passes again on the merged
  head, with no new probe failure.

### DR4. Day One guidance (should) — [AUDIT C2-C4](AUDIT.md#c2-the-first-gameplay-line-is-a-pitched-yay--should)

- Speak the castle line with the existing cue `d1_c01_s03_roshan_walk_castle`
  instead of `roshan_day1_castle` (`sky_lagoon_promenade.gd:288`).
- While a finished room waits for her to leave
  (`_day_one_room_handoff_target != ""`), show the existing
  `ghost_hand.png` on the global Back control.
- Give each bathroom reprompt a fresh voice session id, as the Pool does.
- Optional new line per Q6.
- Done when: the real take plays for the castle line; the hand shows on Back
  only in finished rooms; repeated bathroom reminders are audible; probe legs
  cover all three.

### DR5. Part 2 shaping (should) — [AUDIT D](AUDIT.md#d-part-2-day-two)

Default (Q3 option a, the whole party story):

- Ballerina: start the ballet without activating the nook item, so the
  stuffie picker does not open over it (`main.gd:6011-6017`; no edit to
  `castle_rooms_25d.gd`).
- Mark the door that leads to the next party job with Day One's existing
  golden door state, two hops for the Dining Room; show the venue's existing
  guide pointer on the current job's door.
- Announce the current job after the Day Two card and on castle entry
  (`_chapter_two_announce_start`, `main.gd:6966`).

If Q3 is option b (stop after the Painter): refuse acts outside
`FIRST_WAVE_UNLOCK_MASK` (`0x0449`: Farmer, Chef, Candy Maker, Painter) in
`ChapterTwoDirector.can_start_chapter2_act`
(`chapter_two_director.gd:236-246`), return no plot action for the Ballerina
and Detective in `room_plot_action` (`:520`), and stop the next-job prompt
after the Painter. Saves and masks stay unchanged.

Done when: from a post-boss save, a probe completes the chosen jobs through
room objects with real touches; the pointer marks each next door; no picker
opens over the ballet.

### DR6. Release candidate and rehearsal (must) — [runbook R1-R4](DEMO_RUNBOOK.md#r1-release-candidate-rc)

Codex cuts the RC once everything in scope is on `dev` and green. The adult
runs the save rehearsal on a computer and the device rehearsal. Only
blockers found there are fixed, each producing a new RC.

### DR7. Promote and verify (must) — [runbook R5](DEMO_RUNBOOK.md#r5-promote-and-verify)

After the owner's release instruction, dispatch `promote.yml` only once the
RC's Probe Suite is green and the `android-dev` release names the RC SHA
([AUDIT E5](AUDIT.md#e5-promotion-timing--follow-the-runbook-order)).

## 6. Schedule

Proposed; the owner sets the date (Q8). One Probe Suite run takes about an
hour, so plan about three merges a day.

| Day | Date | Work |
|---|---|---|
| 0 | Sat 31 Oct - Sun 1 Nov | DR0; owner answers or accepts defaults; save backup and reading |
| 1 | Mon 2 Nov | DR1+DR2 branch through CI into `dev`; start DR3a |
| 2 | Tue 3 Nov | DR3a and DR3b into `dev`; DR3c if Q2 is yes |
| 3 | Wed 4 Nov | DR4 and DR5 into `dev`; cut the RC in the evening |
| 4 | Thu 5 Nov | Save rehearsal on a computer; device rehearsal; triage |
| 5 | Fri 6 Nov | Fix rehearsal blockers only; promote; verify on the device |
| 6 | Sat 7 Nov | Demo |

If the schedule slips, drop work in this order: DR5's pointer and
announcement items, DR3c, DR4, DR3a. DR0, DR1, DR2, DR6 and DR7 stay. If the
device rehearsal fails on Thursday and Friday's fix also fails, move the demo
rather than promote an unrehearsed build.

## 7. Owner questions

Each has a default that Codex may use if there is no answer by the end of
Day 0, except where a default says "only on an explicit yes" (high-risk or
protected files).

| # | Question | Default |
|---|---|---|
| Q1 | Start the demo with New Game or Continue? | Decide from her save (runbook R0, R2). Use New Game if her save predates Day One, finished the old fight another way, or holds career stars that Chapter 2 would hide (`MA-SAVE-002`); her save is archived as `.before_new_game` and backed up. Otherwise Continue. |
| Q2 | Put the "friend with a cold" Grand Puff (`ODR-GRAND-PUFF-COLD-20261017`) in the demo, and update the canon lines in `CLAUDE.md` and `AGENTS.md`? | Yes if DR3c is green by Tuesday; otherwise demo the current Puff and land the recast afterwards. Canon text: only on an explicit yes; otherwise leave both files unchanged and note the mismatch in the impact record. |
| Q3 | How much of Part 2? (a) the whole party story with the DR5 fixes, ending on the Ember King cliffhanger; (b) stop after the Painter; (c) Day One only. Also: land the Opera foyer movement repair now? | (a); foyer movement after the demo. |
| Q4 | Microphone? | Switch Mic off in Options on her device during setup; no code change. |
| Q5 | Hide the playtest elevator for the demo build? | Yes (`ENABLED := false`); re-enable afterwards if still wanted. |
| Q6 | Record one new synthetic line, "Let's go back to the hall!", for finished rooms? | No new audio for the demo; the hand on Back carries it. |
| Q7 | Restore the deleted protected file `assets/book/baby_eagle.png`? | No change during the demo week. Restore the exact original from `master` only on an explicit yes; nothing uses it at runtime and it stays in history. |
| Q8 | Demo date and device? | Saturday 7 November on the Lenovo Tab M11 named in the device protocol. |

## 8. Gates for every package

Run in the package's own worktree, never in the shared checkout:

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B tools/audit_development.py --base <previous pushed SHA>   # follow-up pushes
python -B tools/audit_game_2d.py --regression-gate                  # after the last JSON edit
GODOT="$(python -B tools/resolve_godot.py)" scripts/ci.sh            # full local suite
```

Known traps that cost a CI cycle each:

- Any edit to `scripts/arena/castle_rooms_25d.gd` or
  `scripts/arena/castle_fixture_rigs.gd` needs
  `python tools/build_castle_interaction_v3_manifest.py` before the castle
  audits pass.
- Removing code can trip pinned counts: the typography `Label3D` total, the
  audio ledger reference counts (`python tools/audit_audio_quality.py`), the
  2D manifest and probe parity. Run the `ci.sh` static section first.
- JSON under `design/` is scanned by the 2D gate: write "3D nodes", never an
  engine class name, in impact records.
- CI checks only the pushed range, so touch the impact record in every push.
- Run probes with an isolated user-data folder (as `ci.sh` does); a direct run
  writes the desktop's real save.

Report each package in three parts: what was implemented, what was
machine-verified at which exact commit, and what visual, device, child or
owner acceptance is still open.

## 9. After the demo

The demo is the first device and child evidence this line has had. Turn the
notes from [runbook R7](DEMO_RUNBOOK.md#r7-demo-day-watching-without-helping)
into the next backlog, then work through the ten areas in
[AUDIT F](AUDIT.md#f-areas-of-needed-improvement-after-the-demo). In short:
land or close finished branches every week; make a short device check
routine; finish Part 2 (guidance, the three rebuilds, Chef, the north-star
destination); test upgrades with real save shapes; shrink the APK and load
rooms in the background; harden promotion and backups; sweep voice
fallbacks; aim the art campaign at what she reaches first.
