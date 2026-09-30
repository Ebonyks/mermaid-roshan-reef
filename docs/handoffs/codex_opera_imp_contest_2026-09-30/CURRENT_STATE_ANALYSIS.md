# Opera careers today: formula, strengths, weaknesses and imp use

- **Baseline:** `dev` at `55032e88936b22723fd9af5282c61ba6696b3d43` (2026-09-29).
  Every `file:line` anchor below refers to that commit.
- **Prepared by:** Claude, from reading the code, data and design documents.
- **What this is:** written analysis only. No game changes, no images and no runtime
  captures. Owner, device and child acceptance are not claimed.

This is the "before" picture for [CONTEST_DESIGN.md](CONTEST_DESIGN.md).

## 1. The formula

### 1.1 One act, one career, one room

The Opera is a chain of three layers:
- `OperaHouse` (`scripts/opera_house.gd`) holds the act table;
- `OperaAct` (`scripts/opera_act.gd`) runs one act;
- `OperaCareerWorld2D` (`scripts/opera_career_world_2d.gd`) is the playable career room.

Fifteen acts are live: `ACTIVE_STAR_MASK` is `0x3BDEF`, which has 15 bits set.

Each act is one career in one painted room. The room is a 2×2 tile backdrop drawn by
`OperaWorldBackdrop2D`. A career runs like this:
1. Roshan walks the room's route to a real object (a **station**). `PHASE_STATIONS`
   (`scripts/opera_career_world_2d.gd:407`) names the station for every phase.
2. Touching the object opens that phase's activity.
3. The activity is one one-finger verb on a gesture surface: `OperaGestureSurface`, or a
   specialist surface (boxing, ballet, racer, geology).
4. When the phase goal fills, the next phase arms at its own station.

The career phase table is `PHASES` (`:262`): 3 to 5 phases per career, **61 in all**. The
three Opera Hall careers add practice copies, which makes 70 phase runs.

Winning works like this:
- `OperaAct._win` (`scripts/opera_act.gd:116`) calls `OperaCompetition.complete`
  (`scripts/opera_competition.gd:251`).
- That computes `quality = speed × 0.58 + care × 0.42` (`:273`), which gives a cheer tier
  of 1, 2 or 3.
- `celebrate()` then plays the curtain call on the proscenium: confetti, Roshan bounces
  and the imp bows (`scripts/opera_career_world_2d.gd:3720-3830`).

### 1.2 The rival today

`OperaCompetition` gives every career a rival pacer: a hidden meter that fills with time.

| Career | Par (s) | Rival cap | Special |
|---|---|---|---|
| chef, candymaker, farmer, astronaut | 38 to 40 | 0.82 to 0.83 | none |
| doctor | 40 | 0.80 | none |
| ballerina, magician, popstar | Hall: mastery silver time | Hall: 1.0 | Hall two-act, `honest_stage` |
| boxer | 34 | 0.86 | own surface draws the imp |
| painter | 38 | 0.84 | none |
| racer | 70 | 0.94 | kart surface draws the rival kart |
| detective | 40 | 1.0 | `timed_retry` (see H1) |
| nursery | 44 | 0.82 | cooperative, partner Nurse Faron |
| geologist | 120 | 0.82 | cooperative, partner "Field Guide Imp" |
| teacher | 40 | 0.82 | cooperative, partner "Learning Buddy Imp" |

How the rival behaves today:
- **He cannot finish.** Outside the Hall and the Detective, the cap is below 1.0, so he can
  never win. `tick` (`scripts/opera_competition.gd:210`) grows his meter towards the cap.
  Each sixth of it emits `rival_step`, which flashes his `taunt` pose with a small bounce
  (`scripts/opera_career_world_2d.gd:3689-3693`).
- **He is hidden until the finale.** He and the two header bars appear only from
  `FINALE_START` (`:386`, via `_set_finale_visible` at `:3196`). The design already says so:
  "Competition is scoped, not assumed. Where a career retains a rival or finale meter, it
  stays hidden until its declared finale and cannot create a loss."
  (`design/01_GAME_DESIGN.md:342-344`).
- **In the room he just stands.** The shipping room shows one static costumed imp at a
  route rest. `_stage_room_finale_partner` (`:1786-1850`) puts him at the clear route
  point farthest from Roshan, facing her. He does not do the job; only a bar shows his
  "work".
- **The Hall is the exception.** For Ballerina, Magician and Pop Star, `OperaPerformancePlan`
  (`scripts/opera_performance_plan.gd`) runs practice copies, then the full stage act.
  - `setup` sets `honest_stage`, cap 1.0, no timed retry, and par = the mastery silver
    time (`scripts/opera_career_world_2d.gd:724-732`).
  - He is visible for the whole stage act. A small input-transparent copy of each stage
    activity shows his work (`performance_rival_surface`, `:769-777` and `:5026-5046`).
  - He *can* finish first. `complete()` records `player_first`, but "finishing second is
    still a complete performance" (`scripts/opera_competition.gd:257-262`).
  - `OperaMastery` then awards Bronze, Silver or Gold with 1, 3 or 6 Encore tokens.
- **The detective is the one timed rival** (H1).
- **Co-op careers keep a partner, not a rival.** Teacher's buddy is hidden; the geologist's
  guide borrows the detective imp; the nursery keeps Faron. Faron's lines are protected
  family recordings.
- **Chapter 2 story runs opt out.** They use `reward_policy chapter2_story` and their
  antagonist is the Ember King, not the imps.

## 2. Strengths to keep

1. **Real job verbs.**
   - The activities are the job itself: decorating a cake, wrapping a bandage, sweeping
     a magnifier, tossing veggies, painting.
   - Each is one finger and wordless, and each has an exact voice cue.
2. **Embodied travel.** Roshan walks to the real object before anything counts, as
   `DL-INT-02` requires.
3. **Safe by construction.**
   - There are no fail screens.
   - The passive probe proves that zero input never wins.
   - Demonstrations never pay (`DL-INT-06`).
4. **Excellent imp art, ready to use.** Twelve costumed imp families each have the same 13
   poses, drawn to one model sheet: idle, windup, charge, slash, recover, guard, stagger,
   flee, bopped, bow, hop_a, hop_b and taunt. Two plain families (mischief, captain) have
   11 each. That is **178 files** in `assets/opera/worlds/actors/`, listed with hashes in
   [data/imp_art_inventory.json](data/imp_art_inventory.json).
5. **Imp lines already recorded.** Each of the 13 costumed careers has four imp lines
   (arrive, copy, bop, steal). There are also three captain lines and one retry line:
   **56 keys**, all present as filler clips with the imp's consistent "Mike" preset.
6. **A working head-to-head seam in the Hall.**
   - `performance_rival_surface` already mirrors any gesture activity as the imp's own
     input-transparent copy.
   - Checkpoints (`opera_performance_checkpoints`) already survive leaving mid-act.

## 3. Weaknesses

1. **The rival is abstract.** Outside the Hall he is a bar and a statue. A four-year-old
   who cannot read the bar never sees him *doing* the job, so there is no contest to feel.
2. **No stakes, no beat.** With a cap below 1.0 he can never win, so the finale has no
   moment of "I beat him". The cheer tier that should reward doing well is invisible and
   silent (H6).
3. **The art is barely used.**
   - The shipping game shows **41 of 178** imp files.
   - Ten costumed families appear only as idle, taunt and bow. The Boxer shows 9 poses and
     the Racer 2. The plain mischief and captain imps never appear.
   - Windup, charge, slash, flee, hop_a and hop_b never appear outside the boxing ring.
4. **His personality is silent.**
   - Only **2 of 56** imp lines are routed: `op_detective_steal` and `op_retry`.
   - The funny "copy" lines ("Flour goes in the bowl... or on my head.") and the "bop"
     lines never play.
5. **The Detective's retry is harsh** (H1). It is the only place the rival changes the
   outcome, and it takes finished work away.
6. **Loose ends** around co-op partners, saves, probes and canon counts (H2 to H10).

## 4. Findings recorded for this handoff (H1 to H10)

These are handoff-local findings, not entries in the master-audit register. The contest
design retires or absorbs the ones marked **retired**; Codex fixes the others in the same
work or queues them.

### H1 (P1): the Detective timed retry takes finished work away

- **Trigger.** The Detective pacer has cap 1.0, par 40 s and `timed_retry`
  (`scripts/opera_competition.gd:21-29`). When the rival meter reaches 0.999 during CASE
  BOARD or CROWN, `tick` emits `rival_solved` (`:232-234`).
- **The reveal.** `OperaAct._tick_competition` (`scripts/opera_act.gd:105-114`) calls
  `begin_guided_retry` (`scripts/opera_career_world_2d.gd:3696-3710`). That starts a
  3.6 s "reveal".
  - The reveal forces `choice_flash` on a surface that is not in choice mode (clue board or
    crown chest), so it shows nothing but the ghost demo (`:4618-4623`).
- **The loss.** When the reveal ends:
  - `phase_index = _finale_start()` sends her back to CASE BOARD, even if she had already
    finished it and was at CROWN (`:4624-4633`).
  - `configure` restarts the board from clue 0 (`scripts/opera_gesture_surface.gd:552`).
  - The "head start" branch for choice mode is dead code for this career (`:4634-4638`).
- **Stale text.** The caption ("The rival detective corners him first — watch, then trap
  him together!") no longer matches the clip `imp_op_retry` ("I found it first! Watch the
  glowing answer, then solve the same mystery with your sparkle memory!"). The Opera hides
  captions when an exact clip exists (`scripts/audio_director.gd:493`), so only adults ever
  see the stale caption.
- **Status: retired** by SPARKLE RACE (`CONTEST_DESIGN.md` §6.2). Remove `timed_retry`, the
  `rival_solved` event, `begin_guided_retry`, the reveal branch and the stale caption.

### H2: Teacher credits a buddy the child never sees

- The Teacher's "Learning Buddy Imp" is hidden throughout
  (`scripts/opera_career_world_2d.gd:1787-1792` and the teacher branch of
  `_set_finale_visible`). The probe asserts it stays hidden (`scripts/probe_opera_2d.gd:1246-1248`).
- Yet the win line thanks "her learning buddy" (`scripts/opera_house.gd:149`).
- **Recommendation:** drop the buddy wording from the win line, or show the buddy. The owner
  decides the Teacher's contest question (`CONTEST_DESIGN.md` §7).

### H3: co-op partners are frozen in one pose

- `_set_rival_pose` refuses cooperative careers (`:3669-3671`). The geologist's field guide
  therefore never changes pose, and the curtain call falls back to a 0.045 rad tilt
  (`:3816-3818`).
- **Status:** the contest design gives every competitive imp a pose script. A co-op partner
  that stays co-op should get at least hop_b on her successes and a bow at the curtain.

### H4: the balance probes measure nothing

- `scripts/probe_opera_2d_balance.gd` and `scripts/probe_opera_balance.gd` never walk to a
  station or open a task.
- CI run `36669767074` (job `109742055576`) prints "300.0 capped" for every career.
- **Recommendation:** make the balance probe walk to each station and drive each activity at
  a scripted child pace. Its timings are needed to tune the contest `base_seconds`
  (`CONTEST_DESIGN.md` §4.3).

### H5: ten careers restart from the first activity after leaving

- Only the Hall careers (`opera_performance_checkpoints`), the geologist
  (`opera_geology_checkpoint`) and the teacher (`teacher_lesson_checkpoint`) resume mid-act.
- Chef, detective, candymaker, doctor, farmer, boxer, painter, astronaut, racer and nursery
  start again from phase 0.
- **Status:** absorbed. The contest design adds an additive `opera_phase_checkpoints` key so
  leaving during the final act never replays earlier activities (`CONTEST_DESIGN.md` §4.9).

### H6: the cheer tier cannot be heard or seen

- Outside the Hall, `_win` speaks the generic `roshan_win` clip, which hides the tier
  caption (`scripts/opera_act.gd:150-159`).
- The tier only changes Roshan's bounce height by 4 px per tier
  (`scripts/opera_career_world_2d.gd:3814`).
- **Status:** absorbed. The contest sets the tier from her winning margin and makes it
  audible and visible (`CONTEST_DESIGN.md` §4.8).

### H7: every act preloads 35 imp textures for a mode no phase uses

- `_prewarm_imp_textures` (`scripts/opera_career_world_2d.gd:4025`, called at `:1380`) loads
  the career family, the mischief imp and the captain: 13 + 11 + 11 = 35 textures.
- They serve the dormant bop crew, which is used only by `LEGACY_PHASES`.
- **Recommendation:** prewarm only the career family (13), plus the mischief imp where Nursery
  option B ships. The contest needs every state of that one family, promptly.

### H8: canon counts disagree

- `DL-INT-07` says 13 careers, 53 phases and 27 modes (`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md:587`).
- `design/01_GAME_DESIGN.md` and `design/00_MASTER_INDEX.md` say 14, 57 and 28.
- The code has 15 live careers and 61 phases, or 70 with Hall practice copies.
- The contests change the phase count again (+4 inserted phases).
- **Recommendation:** update all three counts together when the contests land. Record the
  count change with its routing, voice, passive, teardown, save, capture and document
  evidence, as `DL-INT-07` requires.

### H9: the Magician's TRACK scores taps during the shuffle and pays for wrong hats

- The choice press path (`scripts/opera_gesture_surface.gd:957-962`) checks neither
  `shuffle_t`, so taps during the 1.5 s glide are scored, nor the result: a wrong pick pays
  `_miss_pay()`, a 0.05 crumb once per 0.6 s cooldown (`:395-400`, `:384`).
- **Status:** retired inside HAT DUEL, where shuffle taps are ignored and a wrong pick scores
  for the imp (`CONTEST_DESIGN.md` §6.8). Practice TRACK should also ignore taps during the
  glide.

### H10 (note, not a defect): the Pop Star stars are code-drawn

- `popstar_star_note_unlit.png` and `popstar_star_note_lit.png` are P2 art that was
  specified but never delivered (`scripts/opera_career_world_2d.gd:2345-2347`).
- `_draw_echo_star` therefore draws a 10-point polygon (`scripts/opera_gesture_surface.gd:5914-5923`).
- The SING-OFF mirrors the same drawing in imp purple. No art is required.

## 5. Imp use in numbers

### 5.1 Art (178 files)

| Family | Files | Shown today | Shown after the twelve contests |
|---|---|---|---|
| each of 10 costumed world families | 13 | 3 (idle, taunt, bow) | 13 |
| rival_boxer | 13 | 9 | 13 |
| rival_racer | 13 | 2 (idle, bow) | 13 |
| imp_mischief | 11 | 0 | 0 (11 with Nursery option B) |
| imp_captain | 11 | 0 | 0 |
| **Total** | **178** | **41** | **156 (167 with option B)** |

Per-file evidence, hashes and planned roles are in
[data/imp_art_inventory.json](data/imp_art_inventory.json).

### 5.2 Voice (56 imp keys)

- **Today:** 2 of 56 are routed (`op_detective_steal` at the Detective intro, and `op_retry`,
  which H1 retires).
- **After the contests:** 36 would play, or 39 with Nursery option B. For each costumed
  career, the arrive line becomes his entrance, the copy line his flub and the bop line his
  defeat. The Farmer swaps copy and bop; see `CONTEST_DESIGN.md` §6.6.
- **New lines:** 25 are needed, plus 2 more if Nursery option B is chosen. Per-key detail is in
  [data/imp_voice_inventory.json](data/imp_voice_inventory.json).

## 6. What this means for the design

- **Visible and embodied.** The imp should be visible exactly when he matters (the final
  act), should do the job with his own hands, and should be able to win.
- **Nothing lost when he wins.** An imp win must cost nothing earned (OD-B, contest-only
  restart).
- **Use what exists.** Every beat can be told with poses and lines that already exist. Only
  the challenge and instruction lines are new.
- **Reuse the seams.** `performance_rival_surface` already turns any gesture activity into
  the imp's mirror station, and `_stage_room_finale_partner` already finds him a clear place
  in every room.
