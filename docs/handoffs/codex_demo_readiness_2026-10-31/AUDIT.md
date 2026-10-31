# Demo readiness audit (dev `218ae766`, 2026-10-31)

Status: `SUPPORTING_CURRENT` analysis prepared by Claude for Codex. Written
material only: no game, art or audio change, no images, no probe run.
Baseline: dev `218ae766f8e60afb3f6338b8fafce28ec9fab7f2`. Line numbers refer
to that commit. Entry point and work packages: [README.md](README.md).

Revision 2 (2026-10-31) records the owner's answers ("Use the defaults");
the analysis is unchanged.

Method: read-only code review of the Day One route, Part 2 (Day Two)
reachability and the release pipeline, plus `git` and `gh` queries. Nothing
here is runtime, device, child or owner evidence. Each item says whether it
was verified by reading the code or inferred.

Classification: **BLOCKER** (the child gets stuck, loses progress, sees a
crash, a grown-up surface or a permission pop-up, or the install loses her
save), **SHOULD** (confusing, silent or broken-looking), **POLISH**, **OK**
(checked and fine).

---

## A. Release state

| Fact | Value | Source |
|---|---|---|
| Stable (`master`) | `ff68f9550c28f7d979896d5c84d1214264c29165`, promoted 2026-08-31 by run 33356532501 | `gh run list --workflow promote.yml` |
| Integration (`dev`) | `218ae766f8e60afb3f6338b8fafce28ec9fab7f2`, Probe Suite run 41215786419 passed in 57.0 minutes | `gh run list --branch dev` |
| Distance | 548 commits; `master` is an ancestor of `dev`, so promotion can fast-forward | `git rev-list --count origin/master..origin/dev`; `git merge-base --is-ancestor` |
| Probe Suite duration | 46.1-61.9 minutes over the last eight `dev` runs | `gh run list` created/updated times |
| `android-test` APK | 604,039,545 bytes, 2026-08-31 | `gh release view android-test` |
| `android-dev` APK | 817,288,640 bytes, refreshed 2026-10-31T12:51Z | `gh release view android-dev` |
| Target device | Lenovo Tab M11, 4 GB RAM, 64 GB, Helio G88, Mali-G52 MC2, 1920×1200 | `audit/LENOVO_TAB_M11_EMULATION_PROTOCOL_2026-08-30.md` section 2 |
| Device sessions | None recorded; the generated checklist says "No session is scheduled" | `audit/cycles/2026-10-03b/DEVICE_SESSION.md` |
| Recent `dev` work | All 17 commits that reached `dev` since 2026-10-28 replace flat art in Geologist and Dolls | `git log --since=2026-10-28 origin/dev` |

Consequences for the demo:

- Every CI cycle costs about an hour. A week allows roughly three
  merge-and-verify cycles a day if nothing fails, so packages must be few and
  self-contained.
- The release has never been checked on the device. The adult rehearsal in
  [DEMO_RUNBOOK.md R4](DEMO_RUNBOOK.md#r4-adult-rehearsal-on-the-demo-device-about-40-minutes)
  is the first device evidence; budget a day after it for fixes.

---

## B. Finished repairs stranded off `dev`

`git cherry -v origin/dev <branch>` marks every commit listed here with `+`
(no equivalent patch on `dev`). "Overlap" lists scripts changed both on the
branch and on `dev` since the merge base, which is where conflicts can occur.

| Branch | Tip (full) | Merge base | `dev` commits since base | Files | Overlap with `dev` |
|---|---|---|---|---|---|
| `codex/pool-visual-repair-20261017` | `8c4069c2652e196198f0488e838350a1674a522f` | `a9875690` (2026-10-17) | 61 | 121 | `scripts/arena/castle_rooms_25d.gd` (`dev` added 16 lines for the Merfolk Embrace painting; the branch +40/-6) |
| `codex/studio-scene-integration` | `b5f78e3a5f9c2c50f86922ac1b0da36bd926ef91` | `5120b6d5` (2026-10-14) | 71 | 44 | none |
| `codex/grand-puff-care-20261017` (local only) | `e0abe9c9643e44a85c262683c75b6ac1fb04b5e3` | `1549c377` (2026-10-17) | 59 | 411 | no scripts; shared docs and data: `ASSET_LICENSES.md`, master audit and changelog, findings, ledger, design language, owner decision register, audio quality ledger CSV and summary, `.gitattributes` |
| `codex/opera-foyer-movement-20261017` | `2668ad75dfc9a19e60befeb005ef7d9b98ec876a` | `39b0e158` (2026-10-17) | 66 | 100 | `castle_career_routes.gd`, `opera_house_venue_2d.gd`, `probe_opera.gd`, `probe_opera_2d.gd` |
| `codex/racer-castle-integration-20261022` | `96d6ef9ef8536f9ebf01f6f2ba9ff61c7564e70c` | `9c78f6aa` (2026-10-19) | 24 | 128 | not measured (parked) |
| `codex/arborist-spray-20261015` | `941cb76d548607cc314d285708634b9138ed3535` | `dd799b2d` (2026-10-15) | 70 | 31 | not measured (parked) |

### B1. Pool repair (`6ac82b4e`, reconciled at `8c4069c2`)

- Scope from its impact record `design/audit_impacts/pool-visual-repair-20261017.json`
  (on the branch only): "Owner-requested Pool repair: water-contact debris,
  stable missed-target hand, local active/passive color continuity, purposeful
  bunny route and shore support, bag/nozzle/grip contact and bounded rapid
  tugs, stationary registered Rumi greeting, unobscured pink central float ...
  continuous clean painted fixture water."
- It repairs `MA-TOUCH-004`. On `dev`, `scripts/games/pool_seahorse_rescue_activity.gd:41`
  still caps waiting taps at `MAX_QUEUED_TUGS := 3`, and `_register_tap`
  (`:311-317`) discards the rest, so eight quick on-target taps finish only
  six tugs (the finding's reproduction). The branch sets
  `MAX_QUEUED_TUGS := TAP_TOTAL - 1`, stops queuing beyond the remaining
  tugs and moves Roshan's grip to the bag (`_grip_position()`). Verified by
  reading both versions.
- Integration notes: rebuild the castle v3 manifest after the
  `castle_rooms_25d.gd` and `castle_fixture_rigs.gd` merge; re-merge
  `design/reference/overdraw.json` rather than taking either side whole;
  keep both licence and changelog tails.

### B2. Art Room furniture (`b5f78e3a`)

- Scope from `design/audit_impacts/studio-dirty-furniture-20261015.json`
  (branch only): clearly dirty and clean furniture as whole cards instead of
  thin grime over clean tables, transparency and cleanup/picker lifecycle
  repairs, and "a reproduced orphan-smoother alpha/ghost leak during
  saved-outfit reload; controller exit now restores alpha and frees its owned
  smoothing draw."
- No new image files; changes `day_one_art_studio.gd`,
  `day_one_art_furniture_2d.gd` (new), `day_one_contact_action_2d.gd`,
  `attack_customizer.gd`, `roshan_sprite_loop.gd`, `sprite_transition_2d.gd`
  and two probes. No script overlap with `dev`.

### B3. Grand Puff care recast (`ee5a9cec`, reconciled at `e0abe9c9`)

- The owner decision is recorded only on this branch, in
  `audit/grand_puff_care_20261017/owner_answers.json` and the branch's
  decision register: `ODR-GRAND-PUFF-COLD-20261017`, "Grand Puff is a friend
  sick with a cold, never bad or evil. Roshan cleans his dusty coat, he
  becomes happy and healthy, and the rainbow dust bunny jumps out of his old
  shell. Preserve the original attack patterns, shapes and as much of the
  existing encounter as possible".
- `dev` still ships the earlier canon in `CLAUDE.md` ("a friend trapped under
  a big layer of dirt that made him grumpy and scary"). The picture book's V39
  pages already show sick bunnies with tissue boxes.
- The commit message reports all 82 trusted local probes passing on
  2026-10-17 and displayed checks at 1280×720 and 1560×720 through the saved
  interruption, transformation and Day Two. It changes `dust_boss.gd`,
  `dust_boss_lesson_2d.gd`, `dust_bunny_boss_sprite.gd`,
  `grand_puff_care_2d.gd` (new), `audio_director.gd`, `main.gd` and three
  probes.
- Risk today: the branch exists in one local worktree only. Push it before
  anything else happens there (DR0).
- If the owner wants it in the demo, the reconciliation is mostly
  append-only documents plus regenerating the audio ledger; no script that
  `dev` changed since the base is touched.

### B4. Opera foyer movement (`14cf8ed9`, docs `2668ad75`)

- Scope from `design/audit_impacts/opera-foyer-movement-20261017.json`
  (branch only): "Owner-reported immobile foyer Roshan, unresponsive games and
  requested four-bottom/four-next unlock. Add floor/stair/lift travel,
  pictured eight-career foyer entry, arrival-gated games and persisted-mask
  unlock".
- `dev` merged the related antechamber removal (`77f72a7c` and reconciles) but
  not this movement fix: `scripts/opera_house_venue_2d.gd` on `dev` still
  places Roshan at fixed `FLOOR_ACTOR_POSITIONS` (`:32`) with no travel code,
  while the branch adds `travel_to`, walk lanes and arrival gating.
- Overlaps four files with `dev`'s later foyer icon and melody work, so
  merging it is a real reconciliation, not a fast-forward.

### B5. Other branches checked

- `codex/flat-vector-r6-20261012` is the art campaign's working branch: 287
  commits not on `dev`, mostly verification receipts. Its runtime differences
  from `dev` (start menu sheen retirement R32, CHG-037 launch ambience,
  Geology surface) are polish. Do not merge it wholesale.
- `codex/popstar-rhythm-rebuild-20261022` (`7eada836`) is new development
  for `MA-OPERA-014`. Park it.
- `claude/angry-roentgen-6a8f7b` (`7b851b3d`) is the learning-sessions packet,
  documentation only. Park it.

---

## C. Day One golden path

Route in code: start menu, New Game (press and hold) or Continue, Sky Lagoon
with the `d1_opening` clip, the castle gate, Main Hall with `d1_castle`,
Bubble Bath (basket, sink, tub drain, tub brush, toilet), Mermaid Pool
(skimmer, waterfall, seahorse), Playroom (two pins free Baby Eagle, then a
stuffie), Craft Room (supplies, grime, desk, attack customizer), the Royal
Hall door, `d1_puff_arrival`, Grand Puff, `d1_puff_transformation`,
`d1_epilogue`, then the Day Two card over Sky Lagoon (4.18 s,
`day_two_transition_2d.gd:13`). Room order: `day_one_director.gd:13`.

No soft-lock, crash or progress loss was found on this route. The items
below are what a child would notice.

### C1. Three story clips play under a black screen — BLOCKER (`MA-VIS-011`)

Verified by reading; one desktop run confirms it in minutes.

- **What she sees:** the castle reveal (`d1_castle`, about 8 s) and the
  climax (`d1_puff_transformation` 12.5 s, then `d1_epilogue` 15 s) play as a
  black screen with sound. Taps do nothing except the clip skip.
- **Mechanism:**
  1. `_fade_cut` (`main.gd:3033-3052`) snaps the black cover on canvas layer
     30 (`main.gd:3020-3031`) to full opacity, runs the rebuild callback, and
     only then creates the 0.25 s reveal tween with `create_tween()`, bound to
     the main node.
  2. Inside the castle callback, `_enter_castle_interior_now`
     (`main.gd:5768-5794`) calls `_day_one_discover_dirty_castle()`
     (`day_one_flow.gd:230-235`), which emits `EVENT_DIRTY_CASTLE_DISCOVERY`
     synchronously (`day_one_director.gd:422-434`, `:836`). The hook plays
     `d1_castle` (`main.gd:6721-6723`).
  3. A clip pauses the whole tree at setup
     (`day_one_story_clips.gd:115-118`); only the clip node and its timeout
     run during the pause (`:88`, `:111`). The clip layer is 28
     (`main.gd:6789-6793`), below the cover.
  4. The main node has no process-mode override (`scenes/main.tscn`; no
     assignment in `main.gd`), so a tween bound to it stops while the tree
     is paused. The cover stays black until the clip ends.
  5. Climax: the win calls `day_one_complete_boss_and_begin_day_two()`
     (`dust_boss.gd:598`), whose hooks start the transformation clip and
     queue the epilogue (`main.gd:6755-6763`). The next line, `_end_game`
     (`dust_boss.gd:599`), calls `_leave_arena()` (`main.gd:7701`), which runs
     `_fade_cut` (`main.gd:8810-8813`) after the clip has already paused the
     tree. Both clips play under the cover.
- **Smallest fix:** let the reveal finish while the tree is paused, in both
  orders: create the reveal with
  `create_tween().set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` in `_fade_cut`.
  The callback `_finish_touch_transition` (`main.gd:4695-4698`) only clears
  the cover's mouse filter and rebuilds touch targets, so running it during
  the pause is safe. Do not move `cb.call()` into the tween; the probe-safety
  comment at `main.gd:3034-3038` relies on synchronous rebuilds.
- **Regression guard:** in `probe_day_one_story_clips.gd`, enter the castle
  with Day One active, wait a few frames while `d1_castle` is active, and
  check `fade_rect.modulate.a <= 0.02`. Repeat after a Grand Puff win with the
  transformation clip active. Keep every existing check.
- **Verify:** desktop display run, New Game to the castle: the clip is
  visible. Win Grand Puff: the transformation and epilogue are visible. Then
  the device rehearsal (runbook R4).

### C2. The first gameplay line is a pitched "yay" — SHOULD

Verified by reading.

- `sky_lagoon_promenade.gd:288` speaks "Let's go to the castle!" with voice
  key `roshan_day1_castle`. None of the four candidate files that
  `_voice_path` tries exists (`audio_director.gd:201-250`: two exact paths
  and two generic `roshan.ogg` paths), so the fallback plays the recorded
  "yay" at Roshan's pitch (`audio_director.gd:374-380`).
- The catalog already has the line with audio:
  `d1_c01_s03_roshan_walk_castle`, "Let's walk to the castle!", file
  `assets/audio/voices/filler_v1/roshan_d1_c01_s03_roshan_walk_castle.ogg`
  (`day_one_contextual_voice_catalog.gd:17`).
- **Fix:** speak it through `say_day_one_context` with that cue. No new audio.

### C3. Nothing tells her to leave a finished room — SHOULD

Verified by reading.

- `_show_day_one_room_handoff` (`main.gd:6579-6597`) shows the caption "Back
  to the hall, then follow the glowing door!" but plays `day_one_pool_ready`
  or `day_one_room_clean`, which say other things. The only exit is the
  upper-left Back control, and nothing points at it. A non-reader can sit in
  a clean room with nothing to do (`DL-AGE-01`, `DL-SND-01`).
- The Day One catalog has no "back to the hall" cue (`grep` over the 118
  catalog rows).
- **Fix:** while `_day_one_room_handoff_target != ""`, show the existing
  `assets/castle/training/ghost_hand.png` pointer over the global Back
  control, and remove it on leaving the room. The owner chose no new audio
  for the demo (Q6, `ODR-DEMO-NO-NEW-AUDIO-20261031`), so the pointer
  carries the cue.

### C4. Bathroom reminders are silent — SHOULD

Verified by reading. The idle reprompts (`day_one_bathroom_cleaning.gd:421-430`)
call `_announce_stage`, which reuses fixed session ids such as
`bathroom_sink_start` (`:981-995`). The voice catalog plays a cue once per
session id (`audio_director.gd:146-155`), so every repeat is silent; only the
hand pulses. The Pool does it correctly with a fresh id per reprompt
(`day_one_pool_cleanup.gd:280-286`). Copy that.

### C5. "FPS" text in the pause menu — SHOULD

Verified by reading. The pause sheet adds `fps_lbl` (`pause_menu.gd:62-65`)
and `main.gd:8241-8242` writes "FPS: N (speedy)" whenever the sheet is open.
Hide it unless `OS.has_feature("editor")`. Do not gate on
`OS.is_debug_build()`: the APK on her device is a debug build.

### C6. Fast taps dropped in the seahorse rescue — SHOULD (`MA-TOUCH-004`)

Verified by reading; see [B1](#b1-pool-repair-6ac82b4e-reconciled-at-8c4069c2).
Still present on `dev` (`pool_seahorse_rescue_activity.gd:41`, `:311-317`).
It does not stall: eight accepted tugs still finish the activity. Landing the
Pool repair fixes it.

### C7. Grand Puff — OK

From the review (not re-checked line by line here): hits cost only medal
stars (`dust_boss.gd:218-226`); after two hits the warning clock waits while
she is inside the shape and each miss adds warning time
(`boss_encounter_2d.gd:75-81`); after two missed openings the counter window
becomes unlimited (`boss_encounter_2d.gd:84-90`). The 2026-09-23 measurement
("dodge reaction ≥ 3.5 s or star tap ≥ 6 s never finishes") no longer holds:
the trusted `probe_dust_boss_balance.gd` runs those personas. Zero input does
not win (`DL-AGE-04`). Instructions are spoken once per visit
(`dust_boss.gd:394`, `:506`); later warnings rely on the glowing shape and
star (POLISH).

### C8. Interruptions, Back and Continue — OK, with notes

- Saves flush on focus loss, pause and close (`main.gd:3735-3742`;
  `touch_ui.gd:651-665` per the review). Each Day One step saves as it
  completes. The two Baby Eagle pins persist; only optional pearl bunnies live
  in unsaved scratch (`MA-SAVE-001` no longer touches the required route).
- Android Back: nothing at the start menu, returns to the hall from a room,
  skips a clip, opens the pause menu in the fight (from the review).
- Continue enters the game directly even for a save that predates Day One
  (`main.gd:3318-3337`, `start_menu.gd:29-31`). See E2 for what that means for
  her save.
- POLISH: a clip is marked seen when it starts, so a clip interrupted half
  way never replays; killing the app between the boss win and the Day Two
  card skips the transformation, epilogue and card on Continue (from the
  review).

### C9. Microphone permission pop-up — conditional, OK for the demo route

Verified by reading. The microphone defaults to on (`main.gd:647-652`) and
the APK declares `RECORD_AUDIO` (`export_presets.cfg:64`). The device is
opened only by `CombatArena._arm_mic` (`combat_arena.gd:481-486`), which asks
Android for the permission up to twice (`mic_input.gd:197-213`). `CombatArena`
is reached only from the dungeon, the Ember fortress and the Galaxy ice
battle. None is on the Day One route, and the review found no visible entry
to them after the Day Two card, although post-story Galaxy and Fairy
Conservatory access was not reached (section D). Zero-code mitigation: switch Mic off in Options during the
adult setup (runbook R4 step 2), which is the owner's choice (Q4,
`ODR-DEMO-MIC-20261031`).

---

## D. Part 2 (Day Two)

Route in code: after the Day Two card she is outside in Sky Lagoon (four
targets: slide, swing, seesaw, castle door); walking right or tapping the
door enters the castle. Every main-hall door is open. The party story is
eight jobs in order (`chapter_two_party_plan.gd:20`):

| # | Job | Started from |
|---|---|---|
| 1 | Farmer | Dream House Wing, then the Dining Room card |
| 2 | Chef | Kitchen card |
| 3 | Candy Maker | Kitchen card |
| 4 | Painter | Craft Room card |
| 5 | Ballerina | Playroom stuffie nook |
| 6 | Pop Star | Opera Hall venue door |
| 7 | Astronaut | Mermaid Pool card |
| 8 | Detective | Library magic book |

Then the party table opens the party dress, then the lawn finale with a
three-round dodge, which ends with "The Ember King took our glowing candle.
Follow the north star!" (`chapter_two_voice_catalog.gd:28`), a line with no
destination yet. All careers then open as free play.

**`MA-PLAY-005`'s two root causes are fixed in code.** An absent phase
override is no longer turned into an empty list
(`opera_career_world_2d.gd:676-679`, `:709-710`), and story stations bind to
room objects (from the review: adapter `:81-214`, stations `:1571-1617`).
Every link of the chain exists in normal-play code; progress saves after each
phase. Fresh-save door travel and device play are still unproven.

### D1. One tap opens a "DEV MODE" job menu — BLOCKER for a child build

Verified by reading.

- The painted left elevator in the Opera Hall venue is a 136×134 button
  (`opera_house_venue_2d.gd:531-548`, built at `:106`) that opens
  `OperaJobPlaytestMenu`: a grid of all careers titled "Job playtesting" with
  the caption "DEV MODE - Fresh runs. Saved progress and rewards stay safe."
  (`opera_job_playtest_menu.gd:140-150`).
- The only switch is `const ENABLED := true` (`opera_job_playtest_menu.gd:6`);
  no debug or hold gate. The venue exists from Day Two on.
- It was added on 2026-09-30 (`b9b44fb6`) as an "Owner-requested temporary
  elevator launcher" (`opera_job_playtest_menu.gd:3`). Its runs write no save
  or reward, so it is safe, but it is a grown-up screen of words.
- **Fix (Q5, answered: hide it, `ODR-DEMO-PLAYTEST-ELEVATOR-20261031`):**
  `ENABLED := false` for the demo build;
  `_build_playtest_elevator` already returns early (`:532`).
  `probe_opera.gd` audits the elevator (`:80`, `:368-438`); change that leg to
  assert the elevator is absent while `ENABLED` is false. This is an explicit
  behavior change, so the probe edit is allowed. Re-enable after the demo if
  the owner still wants it.

### D2. The Ballerina step opens the stuffie picker over the ballet — SHOULD

Verified by reading; runtime not observed.

- `ACTION_STUFFIE_BALLET` (`main.gd:6011-6017`) first calls
  `activate_chapter2_plot_prop("playroom", "stuffie_nook")`, which calls
  `_activate_room_item(item_id, false)` (`castle_rooms_25d.gd:3675-3687`).
  With the plot route disabled, the nook falls through to
  `activate_current_room()` (`:3586-3589`), and for the Playroom that opens
  the companion picker whenever a stuffie is already adopted
  (`:5729-5734`). Day One makes her adopt one. Then `main.gd` starts the
  ballet as well.
- **Fix:** in `main.gd`, keep the room guard (Playroom open, nook present) but
  start `_start_chapter2_plot_opera(ACT_BALLERINA, ...)` without activating
  the nook item. Do not edit `castle_rooms_25d.gd` for this; any edit there
  needs the castle v3 manifest rebuilt.

### D3. The voice says "Tap the glowing ... door", but no door glows — SHOULD

Verified by reading.

- The route lines (`chapter_two_voice_catalog.gd:19-27`) all promise a
  glowing door. In free play every destination except the Royal Hall
  resolves to `OPEN` (`castle_door_language.gd:58-64`), and the door cue is
  drawn only for non-open doors (`castle_rooms_25d.gd:5357`). Nothing marks
  the next room. The first job's room, the Dining Room, is inside the Dream
  House Wing, so it is two doors away.
- In the Opera venue the hand pointer appears only in a tutorial mode that no
  longer occurs, and the door buttons are transparent (from the review:
  `opera_house_venue_2d.gd:436`).
- She cannot get stuck (every door is open), but without an adult she will
  wander. `DL-AGE-01` asks for a moving pointer.
- **Fix:** reuse Day One's existing "golden rainbow door" state for the door
  that leads to the next party job (the Dream House Wing door for the Farmer,
  then the Dining Room door inside it), and show the venue's existing guide
  pointer on the current job's door. No new art.

### D4. The first job is announced once, under another line — SHOULD

From the review (timing inferred, not observed). The first job line is
queued at `main.gd:6873` and cut by the Day Two card's line, because a new
semantic line stops the active one (`audio_director.gd:131-173`). After that
the current job is spoken again only when a job finishes. **Fix:** call the
existing `_chapter_two_announce_start()` after the Day Two card finishes and
on castle entry while a job is pending.

### D5. Owner-rejected minigames in the chain — owner decision

Jobs 5 and 6 (Ballerina, Pop Star) are the owner-rejected designs of
`MA-OPERA-014`; their rebuilds are not in code. They are playable and have no
fail state. The owner chose to show the whole story (Q3,
`ODR-DEMO-PART2-SCOPE-20261031`).

### D6. Smaller Part 2 items — POLISH

From the review, not re-checked: story room messages with an empty speaker
are text only (`chapter_two_room_plot.gd:159-169`); a waiting Detective can
hear a free-play rival line (`opera_career_world_2d.gd:3877-3891`); disabled
job cards and doors give no feedback when tapped; the dormant Fairy door can
be tapped with no response; the Day Two card pictures the Opera, Craft Room
and Kitchen while the first job is in the Dining Room
(`day_two_transition_2d.gd:31-36`); after the story a 710×238 party touch
area keeps catching floor taps in the main hall
(`chapter_two_room_plot.gd:134-144`).

Not reached by the review: post-story Galaxy and Fairy Conservatory
completeness and each free-play career after the story.

---

## E. Release, save and performance

### E1. Installing over the old app keeps her save — OK

- `versionCode` is the commit count (`android.yml:160-168`), so the demo
  build's code is higher than the August build's (the review read 1575 in the
  August run log and 2123 for `218ae766`).
- The signing key comes from one repository secret, and the build fails
  rather than inventing a key (from the review, `android.yml:85-147`; the
  same certificate fingerprint appears in the August and current run logs).
- Promotion copies the checksum-verified `android-dev` APK; it does not
  rebuild (`promote.yml:104-123`).
- Consequence: once upgraded, going back needs `adb install -r -d` (runbook
  R6).

### E2. Her save in the new build — check before choosing Continue

- From the review: no save key is removed between `ff68f955` and `218ae766`;
  the schema version stays 1; unknown keys survive; legacy saves are
  normalised and written back on first load.
- A legacy save that finished Day One is migrated to "boss defeated" and
  Chapter 2 starts (`DayOneDirector.normalise_save_patch`,
  `ChapterTwoDirector.normalise_save_patch`, from the review).
- **`MA-SAVE-002` (verified by reading):** once Chapter 2 is active, the career
  pearls show only the Chapter 2 mask (`castle_career_routes.gd:298-321`),
  only the next party job can start (`chapter_two_director.gd:236-246`) and the
  free-play career routes are hidden (`main.gd:5981-5982`). Career stars she
  earned in August stay in the save but look un-earned and locked. If she has
  any, either start the demo with New Game (her save is archived and backed
  up) or fix the display first: colour a pearl gold when either mask has the
  bit, but keep `button.disabled` on the Chapter 2 chain only, or the next job
  could lock itself.
- Edge cases from the review, not verified: saves that finished the old fight
  some other way, or predate Day One, never start Chapter 2, so only New Game
  reaches the new story.
- **Action:** read her real save first (runbook R0 and R2): `day_one_active`,
  `day_one_completed_rooms`, `day_one_giant_dust_bunny_boss_triggered`,
  `opera_stars`. The answer decides Q1.

### E3. APK size — not a demo blocker; post-demo work

The review modelled the export from the preset's filters and the Git tree
(model 866 MB against the real 817 MB APK). PNG files are about 721 MB of it,
story clips 57 MB, OGG audio 48 MB. Growth since August is about 251 MB,
largest in the Fashion folders (about 96 MB), the Day One clips (57 MB), Opera
worlds (36 MB) and voices (26 MB). JSON under `design/` and `docs/` is
exported too (the impact records alone are about 3 MB). The 64 GB device can
hold it; install time and storage are the cost. Levers for after the demo are
in [G](#f-areas-of-needed-improvement-after-the-demo).

### E4. Performance risks — rehearsal items

Verified: no `max_fps` or vsync setting in `project.godot`; zero
`load_threaded_request` calls in game scripts, so every room change loads
synchronously behind the black cover; the main scene's root is a 3D node
(`scenes/main.tscn`). From the review: the start menu still renders the 3D
sky, fog, glow and sun built at `main.gd:1468-1517` until the castle turns them
off; `MA-PERF-002` and `MA-PERF-003` stay open. None of this is measured on
the device. The runbook's 20-minute session (R4 step 9) is the first check.

### E5. Promotion timing — follow the runbook order

Verified by reading `promote.yml`:

- It waits at most 100 × 20 s (about 33 minutes) for a green Probe Suite on
  the current `dev` head (`:42-80`), but the suite takes 46-62 minutes. A
  promotion dispatched right after a `dev` push times out and fails.
- It waits up to 30 minutes for the matching `android-dev` APK (`:113-123`).
  `android.yml` cancels an in-progress build when `dev` moves
  (`android.yml:15-17`), so a push during promotion can leave `master` moved
  with the stable APK not updated.
- **Rule:** freeze `dev`, wait until the RC's Probe Suite is green and the
  `android-dev` release names the RC SHA, then dispatch promotion.
- `MA-CI-006` still applies: any successful run for the SHA is accepted.

### E6. Backups

- Nothing pulls her save before an install: `pull-apk.sh:53-56` runs
  `adb install -r` directly, and the bookmark route has no backup. Only
  `./backup.sh` copies the save (`backup.sh:60-70`). Runbook R0 makes it the
  first step.
- The weekly repository backup has failed every week; the latest run,
  40352927192 on 2026-10-26, failed with "error: need a repository to verify
  a bundle", and the `project-backup` release does not exist.
- `assets/book/baby_eagle.png`, a protected book file, was deleted on `dev` in
  `d652d5a7` (2026-09-27, "Repair Castle sprite clipping and remove backpack
  Eagle"). No game script uses it; it is still in `master` (blob `bea3d685`)
  and in history. Promotion will remove it from `master`'s tree too. Q7: no
  change during the demo week (`ODR-DEMO-BOOK-FILE-20261031`).

---

## F. Areas of needed improvement after the demo

Ranked by child impact, then by how much each unblocks.

1. **Land or close finished work every week.** Six owner-requested repairs
   sat off `dev` for two to three weeks, and one owner decision lived only on
   an unpushed branch. A weekly pass should merge each green branch or
   record why it waits, and nothing should stay unpushed overnight.
2. **Make device and child checks routine.** The demo is the first device
   session. A 15-minute weekly check on the demo device, using the existing
   `DEVICE_SESSION.md` format, would turn `MA-PERF-001` and `MA-CHILD-001`
   into evidence.
3. **Finish Part 2.** Next-room guidance if not done for the demo (D3),
   the Pop Star, Ballerina and Racer rebuilds (`MA-OPERA-014`), Chef
   (`MA-OPERA-001`), a destination for "Follow the north star", and a
   reachability check of every free-play career, Galaxy and the Fairy
   Conservatory.
4. **Test upgrades with real saves.** Keep anonymised copies of each
   promoted build's save shapes as probe fixtures and load them into every
   release candidate. Fix `MA-SAVE-002` properly and persist the optional
   castle progress of `MA-SAVE-001`.
5. **Size and speed.** Exclude `design/` and `docs/` JSON from export;
   remove superseded Fashion folders and 3D-era textures after a load trace;
   re-encode the clips at a lower bitrate (`DL-CIN-16` allows whole-frame
   re-encoding); compress large lossless backdrops; add a frame cap; load
   rooms in the background; drop the 3D environment under the start menu;
   close `MA-PERF-002` and `MA-PERF-003`. Measure first (`DL-PERF-07`).
6. **Release pipeline.** Fix `MA-CI-006`; lengthen or restructure the
   promotion wait so it outlasts a Probe Suite run; keep the stable APK build
   from being cancelled by a `dev` push; let `pull-apk.sh` fetch the
   `android-dev` channel.
7. **Backups.** Repair `backup.yml` (run `git bundle verify` inside a
   repository) and confirm one restore; settle the deleted protected file.
8. **Voice.** Sweep every `show_msg` key for pitched-"yay" fallbacks and
   once-per-session cues that need to repeat; give the Part 2 room messages a
   speaker.
9. **Aim the art campaign at what she reaches first.** Since 2026-10-28 every
   `dev` commit has gone to Geologist and Dolls art. Rank the remaining
   art work by how early in her route it appears.
10. **Structure.** `main.gd` is 8,865 lines; probe scaffolding is copied
    (`MA-CI-007`). Continue mechanical extraction only after the demo.
