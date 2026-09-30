# Opera imp contests: design and implementation specification

- **Status:** `PROPOSED / CANDIDATE`. The owner direction is recorded. Implementation,
  probes and acceptance are pending.
- **Baseline:** `dev` at `55032e88936b22723fd9af5282c61ba6696b3d43`. Every `file:line`
  anchor refers to that commit.
- **Revisions:**
  - 1 (`7ec82d46`): the twelve costumed contests;
  - 2 (`df01b7ce`): owner decision OD-C and the inverted Teacher and Geologist contests;
  - 3: the Day Two art review's corrections on reusing current art and on the imp touching
    his work (§4.16).
- **Prepared by:** Claude. Written specification only, with no images, per the CLAUDE.md
  rule "Codex handoffs: Claude writes, Codex builds images". Codex implements.
- **Machine-readable twin:** [data/contest_spec.json](data/contest_spec.json). The prose and
  the JSON agree. If Codex finds a conflict, the owner decisions in §1 win, then this
  document, then the JSON.
- **Before picture:** [CURRENT_STATE_ANALYSIS.md](CURRENT_STATE_ANALYSIS.md).

## 1. Owner decisions (2026-09-30)

- **OD-A:** "No, I think imp comes in during the final act, there should be a contest at
  the end that reflects part of the skill of the job that's a challenge against the imp"
- **OD-B:** "If imp wins, the game restarts immediately afterwards."
- **OD-C:** "The teacher should have an imp, but the game inverts, he teaches information
  that's wrong and it's your job to figure it out, which beats the imp. Similar
  educational type games"

What they mean for the game:
1. The career's costumed imp is **not seen** before the final act. He **enters** when the
   final act begins.
2. The final act **ends in one head-to-head contest** against him. The contest uses a real
   skill of that job.
3. **He can win.** When he does, the contest **restarts at once**.
4. **Learning careers invert.** The Teacher gets a visible imp who teaches with deliberate
   mistakes. The child beats him by finding each mistake and showing the right answer
   (§4.15, §6.13).

**Interpretation to confirm with the owner (restart scope).**
- This design restarts **the contest only**: both sides go back to zero and play again
  straight away.
- Earlier activities, stars, pearls, stickers and saves are kept.
- If the owner meant the whole career, change `restart_scope` to `career` in the JSON and
  §4.7. Nothing else in this design depends on it.

**Interpretation to confirm with the owner (educational scope).**
- The Teacher's wrong lessons reuse its own four lesson kinds: pattern, count, add and
  match.
- "Similar educational type games" is also read as covering the Geologist, the other
  learning career, which gets the same inverted format (§6.14).
- If the owner did not mean the Geologist, it stays cooperative and §6.14 is dropped.

The new binding rule `DL-INT-14`, in
[design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
records these decisions as the target contract.

## 2. Terms

| Term | Meaning |
|---|---|
| final act | The phases from `FINALE_START` to the end (room careers), or the Hall stage act |
| contest | The one head-to-head phase at the end of the final act |
| attempt | One run of the contest from zero; a restart begins a new attempt |
| rematch | An attempt after the imp has won; the count sets the mercy |
| race contest | Both work through the same number of units; first to finish wins |
| points contest | Turns or rounds; each round gives a point to one side; first to the target wins |
| unit | One countable piece of work: a topping, a sparkle, a turn, a paw, a landing |
| mirror station | The imp's own small copy of the activity, showing his units; input-transparent |
| flub | His one scripted mistake per attempt, which is her comeback moment |
| flourish | An existing victory activity after the contest, such as CROWN, BELT, PORTAL or ENCORE |
| inverted contest | A points contest in rounds: the imp teaches with one deliberate mistake per round, and she scores by fixing it (Teacher, Geologist) |
| round | One lesson or specimen in an inverted contest; it always ends with the right answer placed by her |

## 3. The contest contract

Each rule has an ID (C1 to C15) so probes and reviews can cite it.

- **C1. Hidden until the final act.** Before the final act there is no imp sprite, mirror
  station, score row, clock or imp voice. The one exception is the offscreen Detective
  steal line that opens the case, which already ships.
- **C2. He enters when the final act begins.** He has a short entrance (§4.1) and stays
  present, without competing, until the contest.
- **C3. One contest, at the end.** Exactly one contest per career, as the last scored
  activity of the final act. It may be followed only by an existing victory flourish or the
  curtain call.
- **C4. The job's own skill.** The contest reuses one of the career's existing verbs and
  objects (§6). It is never a generic tap race.
- **C5. Embodied.** Roshan performs the contest at the real room object she walked to, as
  `DL-INT-02` requires. Only the three Hall careers compete on the stage, which is already
  their playable venue.
- **C6. He can win.** In a race contest he wins by finishing his units first. In a points
  contest he wins by reaching his target first. Ties go to Roshan. In an inverted contest
  he scores only when her first pick in a round is wrong; he never scores by time.
- **C7. Instant, friendly restart.**
  - When he wins there is a win beat of at most 2 s, then the contest resets and she can
    play again immediately.
  - There is no fail screen, text, sad sting, life counter or wait.
  - Nothing earned is lost: stars, pearls, stickers, saves and every finished activity stay.
  - Only the attempt's own units reset. `DL-INT-14` records that this reset is the
    owner-directed rematch, not a punitive fail state (`DL-AGE-03`).
- **C8. Zero input never decides.** He works only while she is playing. With no input he
  freezes (§4.5). No input can produce a win or a loss (`DL-AGE-04`), and demonstrations
  never move either side (`DL-INT-06`). Inverted contests have no clock at all.
- **C9. Mercy on every rematch.** Each rematch makes him slower, makes him need more points,
  or makes his mistakes easier to spot, down to a floor (§4.3, §4.4, §4.15). An engaged
  child always wins eventually.
- **C10. Wordless and readable.**
  - Progress shows as two rows of pearls or bars with a face icon each. The score rows
    carry no numbers or words. Lesson content keeps its own existing symbols, such as the
    Teacher's numeral labels.
  - Every beat also has an exact voice line (`DL-SND-13`).
- **C11. One finger.** Every contest can be finished with one finger, using the same verb
  as the activity it comes from.
- **C12. No payment for misses.** Inside a contest, wrong input pays nothing. In points and
  inverted contests a wrong answer is the imp's point.
- **C13. Story runs opt out.** Chapter 2 story runs (`reward_policy chapter2_story`), tutorial
  runs, and configs with `phase_overrides` or `scene_adapter` get no imp and no contest. The
  test is the same as `OperaPerformancePlan.enabled`
  (`scripts/opera_performance_plan.gd:15-19`).
- **C14. Clean teardown.** Close, Back, pause-leave and focus loss stop every contest timer,
  tween and queued imp line. Re-entering resumes at the contest phase with a fresh attempt
  (§4.9).
- **C15. Truth last.** In an inverted contest every round ends with the correct answer on
  the board, placed by her. The imp's wrong answer is never left standing (§4.15).

## 4. Shared mechanics

### 4.1 Entrance (when the final act arms)

- **When:** the first final-act phase arms. For room careers that is `FINALE_START`
  (`scripts/opera_career_world_2d.gd:386`); for Hall careers it is the stage start.
- **Where he goes:** his mark.
  - Room careers: the route rest that `_stage_room_finale_partner` already chooses
    (`:1786-1850`), which is the clear point farthest from Roshan. He faces her.
  - Hall careers: the Hall stage mark (§4.11).
- **The run-in:** he runs in from the nearer screen edge in `flee` (about 0.8 s, flipped to
  face his direction of travel), crouches in `hop_a` (0.25 s), jumps onto the mark in
  `hop_b` (0.35 s), then rests in `idle`.
- **Line and timing:** his existing arrive line plays once per act (`imp_op_<career>_arrive`).
  The whole entrance takes at most 3 s.
- **Input is never blocked.** If she opens the first final-act activity during the entrance,
  he finishes the entrance without taking focus.

### 4.2 Between final-act phases

- He is present at his mark and does not compete. There is no mirror station, score row or
  clock.
- When she completes a final-act activity before the contest, he reacts: `stagger` (0.3 s),
  then `hop_b` (0.3 s), then `idle`. No line; he is impressed, not competing.
- Careers whose contest is the first final-act phase (candymaker, painter, astronaut, boxer
  and racer) go straight from the entrance to the challenge.

### 4.3 Race pacing

- His units grow while he is active:
  `imp_units += delta × units_total / base_seconds × rate`.
- `rate = 0.8 ^ rematches`, never below 0.55. The Racer uses its own curve (§6.11).
- **Start:** he is active only after her first touch on her activity in this attempt.
  Listening, looking and demo time never count.
- **When he is inactive:** while he is idle-paused (§4.5), during his flub (§4.6), and during
  any beat longer than 0.3 s that is not his work, he does not move.
- **Finish and ties:** she wins the moment her last unit is accepted. He wins the moment his
  last unit completes. If both happen in the same frame, she wins.
- **Provisional numbers.** The `base_seconds` values in §6 are provisional. Tune each one
  once the balance probe is fixed (H4 in the analysis):
  - measure a scripted steady child (one valid action every 1.2 s, or a steady drag for the
    continuous verbs) on that activity, giving `T_child`;
  - set `base_seconds ≈ 1.35 × T_child`;
  - target: an engaged child wins the first attempt about three times in four, and almost
    always by the second rematch.
  - Owner play-testing overrides the probe.

### 4.4 Points contests (Boxer, Magician, Pop Star)

- Each round ends in exactly one point, for her or for him (§6.7, §6.8, §6.12).
- **Targets:** her target is the career's `points_to_win`. His target is the same, plus 1 per
  rematch, at most plus 2.
- **Slower cues after a lost attempt:** shuffles, song cues and imp wind-ups run 25 % slower
  per rematch, at most 50 % slower.
- **Ties:** if both reach their targets on the same event, she wins.

### 4.5 Idle pause

- **Trigger:** she has not touched her activity surface for 4.0 s during the contest.
- **What he does:** he freezes, alternating `taunt` (0.6 s) and `guard` (0.6 s). The
  activity's existing re-hint or assistance plays.
- **Resume:** he resumes on her next touch.
- **Rule:** the pause never ends by itself. A contest with no input stays unresolved
  forever, and the passive probe must prove it.
- **Inverted contests** have no idle pause, because he never acts on time (§4.15).

### 4.6 The flub

- **Exactly one flub per attempt**, at a fixed point: a unit count, a coverage fraction, or
  in points contests "when he leads or is level at 2".
- **What happens:**
  - He stops for the listed `flub_seconds` (about 2 s) and plays the career's flub poses.
  - His existing copy line plays (the Farmer uses its bop line; §6.6).
  - A small existing effect or prop shows what went wrong.
- **What it is for:** it is her comeback moment. His row visibly pauses while hers can keep
  growing.
- **Rematches:** the flub resets with each rematch, so every attempt has one.
- **Inverted contests** have no flub: every round is already his mistake (§4.15).

### 4.7 He wins: instant rematch (contest-only restart)

- **The win beat (at most 2 s).**
  - Her activity stops accepting input, so a finish after his win cannot count.
  - He plays `hop_b` (0.6 s), then `taunt` (0.8 s), with the new shared line
    `imp_op_contest_win`: "I won! I won! Let's play again!"
- **The reset.**
  - Both rows empty. Her placed pieces lift away with a soft puff (`fx_dust_puff.png`), and
    his mirror station clears.
  - `rematches += 1`, his rate or target mercy applies (§4.3, §4.4), and the flub is
    available again.
- **Straight back in.**
  - She stays at her station, with her activity open and accepting input at once. She never
    walks back to a room object and never replays an earlier activity.
  - The new shared Roshan line `roshan_op_contest_again` plays over the reset: "Again! I
    can do it this time!"
  - He waits in `windup` for her first touch.
- **Demo:** the challenge lines do not repeat. The ghost demo replays only if she scored no
  unit or point in the lost attempt.
- **Records and saves:** mastery counts each rematch as one assist (§4.14). Nothing is
  written to the save.

### 4.8 She wins: defeat beat, flourish, cheer tier

- **Defeat beat:** he plays `stagger` (0.4 s), then `bopped` (1.0 s), then `recover` (0.6 s),
  with his existing bop line. At the same time Roshan plays her existing `cheer` animation
  (`_play_roshan_animation("cheer")`).
- **What comes next:**
  - If the career has a flourish (Detective CROWN, Boxer BELT, Magician PORTAL, Pop Star
    ENCORE, Painter GALLERY), it arms as the next phase. He watches from his mark and does
    not compete.
  - Otherwise the curtain call plays, and he bows as today.
- **Cheer tier.** It comes from her winning margin, not from time.
  - The margin is her lead when she finishes, as a share of the contest: units for a race,
    points for a points contest.
  - Tier 3 if the margin is at least 0.35, tier 2 if at least 0.15, otherwise tier 1.
  - Any rematch caps the tier at 2.
- **Making the tier heard and seen** (this fixes H6):
  - tier 1: one confetti burst and one `assets/audio/chime.ogg`;
  - tier 2: two bursts and two rising chimes;
  - tier 3: three bursts, three rising chimes and `assets/audio/voices/filler_v1/yay.ogg`,
    with the imp bowing twice;
  - never text only.
- **Feeding the result on:** pass the tier into `OperaCompetition.complete()` so rewards,
  mastery and the curtain call use one result.

### 4.9 Save and resume

- **Attempts are never saved.** Resuming always starts the contest from zero, with the
  rematch count reset.
- **Hall careers** already checkpoint the phase index in `opera_performance_checkpoints`
  (`scripts/opera_career_world_2d.gd:5149-5160`). Save the contest phase with an empty
  `current` snapshot.
- **Every other contest career** gets a new additive dictionary key:
  - `opera_phase_checkpoints = {career: {version: 1, phase_index: n}}`, default `{}`;
  - registered in `DICTIONARY_KEYS` and `KNOWN_KEYS` in `scripts/save_state.gd`, with a
    loader default;
  - written when each final-act phase arms;
  - erased with the career's other checkpoints when the act is won (`scripts/opera_house.gd:275-286`).
- **Result:** leaving during the final act resumes at the first unfinished final-act phase,
  with the imp already present (no second entrance). This absorbs H5 for the final act. The
  earlier phases of those ten careers stay as they are unless the owner asks otherwise.
- **Teacher and Geologist** keep their existing checkpoints (`teacher_lesson_checkpoint`,
  `opera_geology_checkpoint`) for the phase index, with an empty mechanic snapshot on the
  contest phase. They do not use `opera_phase_checkpoints`.
- **Save rules:** never remove a save key (`DL-SAVE-01`). Flushes on pause and focus loss
  follow `DL-SAVE-02`.

### 4.10 Score rows

- **Where:** the existing header's two rows (`player_bar` and `rival_bar`) become the contest
  rows. Hers is on top with a Roshan face icon; his is below with his costume's face icon.
- **Discrete contests:** one pearl per unit or point. Hers are in the career accent (the
  `accent` in `scripts/opera_competition.gd`). His are imp purple, a deeper shade of
  `#c5a4ef` so they read on white.
- **Continuous contests** (painter coverage, racer distance) keep the existing bar style.
- **Rule:** no numbers and no words. The rows appear at the challenge and hide at the defeat
  beat or the reset.

### 4.11 Where everyone stands

**Room careers**
- **Roshan:** at the station she walked to, as today.
- **Her activity card:** placed by `_card_position_near_station` (416 × 292 card, 392 × 232
  surface; `:2822-2844`).
- **The imp:** at the `_stage_room_finale_partner` mark, facing her.
- **His mirror station:** the same kind of input-transparent `OperaGestureSurface` the Hall
  already uses (`:769-777`), at scale 0.6 (about 235 × 139). It is his job object, so it
  sits at his hands on his reach side, never floating above him (§4.16).
  - If that spot overlaps her card, Roshan or the header, he takes the next clear route rest
    instead, using the `_safer_panel_rect` candidate search (`:2847-2870`).
  - It never covers her card or her body.

**Hall careers**
- Magician and Pop Star keep `_performance_stage_layout`:
  - Roshan at (48, 264), size 300;
  - her activity at (390, 204), 500 × 376;
  - the imp at (974, 294), size 220;
  - his mirror at (916, 144), 392 × 232, scale 0.7. That spot floats above his head: for
    the contest, move it down to his hands (§4.16) and confirm the contact in captures.
- The Ballerina keeps its exception: Roshan at (12, 372), size 300; the imp at (238, 350),
  size 150; the ballet canvas at (382, 20), 874 × 680. His small music box sits by his mark
  (§6.3).

**Specialists**
- **Boxer:** the full-screen boxing surface already draws the imp as the opponent, and Roshan
  is first-person gloves.
- **Racer:** the full-screen circuit already draws both karts.

**Inverted contests** have no mirror station: he teaches on her own board.
- **Teacher:** he stands at the right end of the board, about 150 px tall with his feet near
  (1205, 640). He stays clear of every choice card (the right-most card ends at x = 1133)
  and of the hint button at (1115, 150).
- **Geologist:** he stands at the existing field-guide spot, (78, 218) at 176 px
  (`_stage_room_finale_partner`, `:1793-1799`).

**Curtain call:** stays on the proscenium for everyone (`_position_curtain_call_cast`, `:1852`).

### 4.12 Voice rules

- **One voice at a time** (`DL-SND-14`). When two lines collide, the higher priority plays and
  the lower one is dropped, but its poses still play. Priority, highest first:
  1. her instruction line and "Again!";
  2. the imp's challenge;
  3. the imp's win line;
  4. the imp's flub and defeat lines;
  5. the imp's arrive line.
- **Limit:** at most one imp line every 3 s.
- **Skipping:** lines are touch-skippable and clear on teardown (`DL-SND-03`).
- **Routing:** `show_msg(who, text, vo)` plays `<speaker>_<vo>.ogg`, preferring `filler_v1`.
  In the Opera the caption hides when an exact clip exists (`scripts/audio_director.gd:493`),
  so every caption text must match its clip.
- **New lines:** 25 lines (27 with Nursery option B) are added through the existing filler
  pipeline, as provisional synthetic filler: imp preset "Mike", Roshan preset "Joy". See
  [data/imp_voice_inventory.json](data/imp_voice_inventory.json) for the list.
  - Existing clips and protected family recordings are never modified (`DL-SND-05`,
    `DL-SND-11`).
  - Each new file gets its all-audio ledger row (`DL-SND-10`) and meets `DL-SND-12`.

### 4.13 Pose meanings

Every costumed family has the same 13 states. Each state means the same thing in every
contest.

| State | Meaning in a contest |
|---|---|
| idle | At rest at his mark between beats |
| windup | Ready: watching her before and at the start of an attempt |
| charge | Working, first half of a unit: reaching for the next piece |
| slash | Working, second half of a unit: placing it or swinging the tool |
| recover | After his flub, and the last step of his defeat |
| guard | Worried when she is near her finish; frozen during the idle pause; Boxer guard |
| stagger | Surprised when she overtakes him; first step of his defeat |
| flee | Running in at his entrance, or chasing a runaway object |
| bopped | The dizzy flop in his flub and in his defeat |
| bow | Curtain call |
| hop_a | Entrance crouch |
| hop_b | Entrance jump, and his victory jump when he wins |
| taunt | Challenge, when he is ahead, his "ta-da", and during the idle pause |

- **While working:** he alternates `charge` for the first half of each unit and `slash` for
  the second.
- **Reactions:** he plays `stagger` at most once every 3 s when she overtakes him. He holds
  `guard` while she has at least 80 % of her units and leads.
- **Show every step.** The runtime shows the authored poses; it never tweens between them
  to fake frames (`DL-MOT-07`).
- **Inverted contests** use the same states differently: `charge` and `slash` point at the
  board and place his wrong answer; `taunt` is his proud claim; `stagger` then `recover`
  when she fixes it; `hop_b` then `taunt` when he tricks her. Defeat and bow are as usual.
- **Contact:** each of his units lands on the contact moment of his `slash` pose, where his
  hand or tool meets his job object (§4.16).
- **Preload:** only the career's family, 13 textures (fixes H7).

### 4.14 Hall careers (Ballerina, Magician, Pop Star)

- **Practice** keeps its activities unchanged. Contest phases are stage-only, so
  `OperaPerformancePlan.build` must not copy them into practice.
- **The stage-long race.** Today the imp also races through every stage activity
  (`honest_stage`, `_performance_rival_work`).
  - **Recommended:** retire it. He enters at the stage start (§4.1), watches between stage
    activities (§4.2), and competes only in the contest. That matches OD-A's "a contest at
    the end", and a four-year-old then meets one clear challenge instead of two overlapping
    races.
  - This is an open owner question (§7.5). If the owner keeps it, the stage-long race must
    stay no-loss, and only the contest can restart.
- **Mastery** (`scripts/opera_mastery.gd`): medal times still use the stage's active seconds.
  Each rematch counts as one assist. A won contest earns at least Bronze.

### 4.15 Inverted contests (Teacher; Geologist pending confirmation)

OD-C turns the contest around for learning careers. The imp is the teacher, and he gets
things wrong on purpose.

**A round**
1. The board shows one lesson (Teacher) or one specimen (Geologist).
2. He presents it with exactly one deliberate mistake. He points and places his wrong
   answer (`charge`, `slash`), marks it with a purple outline, and claims it proudly
   (`taunt`) with his claim line.
3. She checks it. Where the lesson already asks her to count, she counts first, exactly as
   in her lessons.
4. Her **first pick** decides the round:
   - **Right** (the right answer, or the wrong part): his mistake pops off with a soft puff
     (`fx_dust_puff.png`), the right answer settles in, and he plays `stagger` then
     `recover` with "Oops! You fixed it!". Her pearl.
   - **Wrong** (his answer, or another wrong one): he plays `hop_b` then `taunt` with "Hee
     hee! I tricked you!". His pearl. The golden help then shows the right answer, with the
     existing Teacher help clip ("Look at the golden sparkle. You can try again."), and she
     taps it to finish the round. That tap scores nothing.
   - **Hint:** the hint button stays available. A hinted round scores for nobody, and she
     still finishes it by placing the right answer.
5. The next round starts with the next lesson kind or specimen.

**Rules**
- **Truth last (C15):** every round ends with the correct answer on the board, placed by
  her.
- **No clock:** he never scores by time, so there is no idle pause and no flub. Zero input
  leaves the round waiting forever.
- **Points:** first to 3. His target is 3, plus 1 per rematch, at most plus 2.
- **Rematch mercy:** rounds step down one difficulty tier (never below 0), and his wrong
  answer becomes the most obviously wrong choice: for three pearls he claims five, not four.
- **Restart:** when he wins, the win beat and "Again!" play as in §4.7. Points reset; the
  round rotation continues where it was, so she never repeats the round she just lost.
- **Cheer tier** uses the points margin (§4.8).

**Why this suits a four-year-old.** Early-maths research has long used a "puppet paradigm":
a puppet counts, sometimes wrongly, and the child says whether it was right. Preschoolers
catch a puppet's counting errors even before their own counting is reliable (Gelman and
Meck, 1983, *Cognition* 13, 343–359). Spotting the imp's mistake is therefore
age-appropriate. That is design rationale, not evidence about this game; the child session
in §12 checks it.

### 4.16 Art reuse and the imp's contact

These rules come from the Day Two art review's reading of revision 1
([REPORT.md, "Planned final act contests"](../../../audit/day2_art_library_2026-09-30/REPORT.md)).

**Reuse the current art routes only.**
- Never draw the retired family bases `widget_<context>.png`. They are the pale clipboard or
  easel cards the surface keeps only as `retired_widget_backdrop_path`
  (`scripts/opera_gesture_surface.gd:758-764`).
- Never draw the static `roshan_<career>.png` cards, which crop her tail. Use the full-tail
  atlases `assets/opera/worlds/actors/animation/roshan_<career>_sheet_a.png`.
- Use the borderless routes the surfaces already draw: `_mover`, `_mark`, `_lit`,
  `_success` and the code-drawn surfaces. `data/contest_spec.json` names the exact file for
  each career.
- The Racer keeps its in-kart driver art (`roshan_racer.png` inside the kart), which is its
  existing route.

**The imp touches his work.** Each of his units must show readable contact with his own job
object:
- the object sits at his hands, facing him, not floating above him;
- the unit lands on his `slash` contact moment, with a small puff;
- alternating `charge` and `slash` beside a miniature picture is not enough;
- captures must show his hand or tool touching the object.

**Optional art stays optional.** The Doctor's bandage overlay and the new teacher, geologist
or nursery imp costumes are owner-dependent options, not generation orders.

## 5. How to build it

### 5.1 A new logic class

Add `scripts/opera_imp_contest.gd` (`class_name OperaImpContest`, `RefCounted`), modelled on
`OperaPerformancePlan` and `OperaMastery`: pure logic, no nodes, testable headless.

It holds:
- `CONTESTS`: the per-career table from §6 and the JSON (archetype, units or points, base
  seconds, flub point and seconds, flub poses, flourish, venue, voice keys);
- `enabled(career, config)`: the C13 opt-out, using the same test as
  `OperaPerformancePlan.enabled`;
- `apply(career, phases, two_act)`: returns the phase list with the contest in place.
  - A **replaced** activity keeps its phase `name` and gains a `contest` dictionary.
  - An **inserted** contest is a new phase with its own `name`.
  - For Hall runs it touches only the stage copies;
- the attempt state: `state`, `attempt`, `rematches`, `her_units`, `his_units`, `his_rate`,
  `flub_done`, `idle_t`, `beat_t` and `margin`;
- `tick(delta, her_units, her_touched) -> Array[String]`. The events are `imp_unit`,
  `imp_overtaken`, `imp_worried`, `idle_pause`, `idle_resume`, `flub_start`, `flub_end`,
  `imp_won` and `player_won`;
- for the `inverted` archetype, no pacing at all: `score_round(result)` takes `fixed`,
  `tricked` or `hinted` from the surface and returns `imp_won`, `player_won` or nothing;
- `reset_attempt()` and `result() -> {margin, tier, rematches}`.

### 5.2 Phase naming

- **Replaced activities keep their internal names:** TOP, SHARE, BANDAGE, PICNIC, TITLE IMP,
  LAUNCH, RACE, and the stage copy of GRAND TWIRL. `PHASE_STATIONS`,
  `HOTSPOT_PHASE_ALIASES`, the hotspot catalog, voice keys and probes all key on those names.
- **Inserted contests are new phases:** SPARKLE RACE, PAINT-OFF, HAT DUEL, SING-OFF, IMP'S
  LESSON and FIELD GUIDE MIX-UP. Each needs a `PHASE_STATIONS` entry (§6), a hotspot entry,
  voice keys and probe coverage.
- **Contest names are design names only.** The child never sees them.

### 5.3 Career world (`scripts/opera_career_world_2d.gd`)

**Contest presentation** (new functions):
- `_contest_entrance()`, `_contest_open()` (challenge sequence) and `_contest_tick(delta)`;
- `_contest_apply(events)`, which maps events to poses, lines and mirror units;
- `_contest_imp_won()` (§4.7) and `_contest_player_won()` (§4.8).

**Changes to existing code:**
- **Mirror station.** Build it for room careers the same way `performance_rival_surface` is
  built (`:769-777`): `armed_only = true`, input ignored, processing off.
- **`_set_finale_visible`.** Contest careers show the imp from the final act, but the score
  rows only from the challenge.
- **`_set_rival_pose`.** Use it for every contest pose. Its guard for co-op careers stays.
- **Teacher and Geologist stop being co-op.** Their special branches must show the imp from
  the final act and hide him before it:
  - the Teacher hides its buddy in `_stage_room_finale_partner` (`:1787-1792`),
    `_set_finale_visible` (`:3202-3208`) and the curtain call (`:3778`, `:3792`);
  - the Geologist shows its guide from the first beat (`:1793-1799` and the Geologist branch
    of `_set_finale_visible`).
- **Prewarm.** `_prewarm_imp_textures`: the career family only (H7).
- **Remove the Detective retry path (H1):**
  - `begin_guided_retry` (`:3696-3710`);
  - the `reveal_t` branch in `_process` (`:4618-4638`);
  - the `guided` flag, if nothing else reads it.

### 5.4 Competition and act

- **`OperaCompetition` (`scripts/opera_competition.gd`):**
  - For contest careers, stop the background pacer outside the contest. The rival meter no
    longer fills during earlier phases.
  - Remove `timed_retry`, the `rival_solved` event and `guided_retry()`.
  - Drop `cooperative` from the Teacher and Geologist entries in `CAREERS`. Their partner
    names ("Learning Buddy Imp", "Field Guide Imp") become the imps' names.
  - Let `complete()` accept the contest result (tier and rematches) instead of the time-based
    quality.
  - Co-op careers keep today's behaviour.
- **`OperaAct` (`scripts/opera_act.gd`):**
  - `_tick_competition` drops the `rival_solved` branch.
  - `_win` plays the tier cue (§4.8) before Roshan's win line, so the tier is audible (H6).

### 5.5 Surfaces

**Every surface:**
- `contest_mode` — while on, `_miss_pay()` returns 0 and the §6 contest contracts apply.
- `set_mirror_units(units)` for the input-transparent mirror copy. It must draw what his
  units mean in each mode:
  - anchored targets: the first N sockets filled, in socket order;
  - `farm_lob`: landings;
  - `paint_reveal`: covered cells in a fixed stroke order;
  - `echo`: lit stars;
  - ballet: orbit fraction;
  - trace: passes.
- Today's `set_fill` only moves a generic fill (`scripts/opera_gesture_surface.gd:927-933`).

**Per-mode contest contracts:**

| Mode | Contest change |
|---|---|
| choice (HAT DUEL) | Presses during the shuffle glide (`shuffle_t > 0`) are ignored; a wrong hat after the shuffle pays nothing and emits a wrong-answer event for the imp's point |
| echo (SING-OFF) | A wrong note pays nothing, gives the imp a point and starts the next round instead of replaying |
| ballet_twirl (TWIRL-OFF) | `turns_required = 3`; progress is normalised over three orbits with the same either-direction monotonic rules; today one orbit caps `twirl_progress` (`scripts/opera_ballet_surface.gd:508-549`) |
| swipe trace (BANDAGE RACE) | `passes_required = 3`; after each finished pass the authored corridor re-arms on the next paw; each pass banks once |
| boxing_imp (TITLE BOUT) | Her landed punches are her points; his point is a counter that lands unblocked, counted only if she touched in the last 4 s; friendly contact never removes her points |
| kart_race (GRAND PRIX) | Emit `rival_finished` when his kart completes two laps first; reset both karts on a rematch; his kart waits while she is idle |
| tap then hold (LAUNCH RACE) | One phase: five leak sockets, then a 1.2 s hold, which is the sixth unit |
| teacher_imp_lesson (IMP'S LESSON) | New mode on `OperaTeacherSurface`: the lesson comes from `TeacherLessonPlan`, plus the imp's wrong answer drawn with a purple outline and his pointer mark; her first pick decides the round and emits `fixed`, `tricked` or `hinted`; golden help follows a wrong pick; one `record_result(kind, assisted)` per round |
| geology_mixup (FIELD GUIDE MIX-UP) | New mode on `OperaGeologySurface`: fossil rounds (three strips of `geologist_fossil.svg`, one upside down, her finished fossil small beside it) and rocks rounds (three `_draw_mineral` rocks, one different); her first tap decides the round |

**Teacher lesson plan:** add `TeacherLessonPlan.imp_answer(lesson, mercy) -> int`, which is
deterministic and never returns the correct choice.
- It normally picks the nearest wrong choice: the closest wrong number for count and add,
  the first distractor for pattern and match.
- With mercy it picks the farthest wrong choice.
- Keep `make_lesson` unchanged, so ordinary lessons and saved progress behave exactly as
  today.

### 5.6 Other systems

- **Performance plan:** exclude contest phases from practice copies.
- **Mastery:** each rematch adds one assist.
- **Save state:** the new `opera_phase_checkpoints` key (§4.9).
- **Chapter 2 adapter:** untouched. `enabled()` keeps story runs out (C13).

## 6. The specified contests

Every contest follows §3 and §4. Each entry lists only what is specific to the career. The
line texts are exact. "New" lines do not exist yet; every other line is an existing clip.
§6.1 to §6.12 are the costumed careers. §6.13 (Teacher) and §6.14 (Geologist, pending
confirmation) are the inverted contests from OD-C.

### 6.1 Chef — TOPPING RACE (race; replaces TOP)

- **Final act:** FROST, then the contest. Both are at `grand_cake_stage`.
- **Skill:** decorating. Her cake shows seven glowing sockets
  (`TARGET_ANCHORS.target_chef`). Each tap on an empty socket places one topping; each socket
  takes one.
- **His side:** at his hands, a small copy of the same borderless cake
  (`widget_target_chef_mover.png`) fills its sockets in the same order. He reaches
  (`charge`) and places (`slash`); each topping lands as his hand touches the cake.
- **Pace:** 7 units, `base_seconds` 13.0.
- **Flub:** at his 4th topping.
  - He staggers, a cherry topping (`widget_target_chef_piece_1.png`) lands on his chef's
    hat, and he flops (`bopped`, 1.0 s), then recovers.
  - Line: "Flour goes in the bowl... or on my head. Either way!"
  - His row pauses 1.8 s.
- **What the child sees:** her big cake is filling with toppings. Across the room a little
  purple chef-imp hurries to top the small cake in his hands; the two pearl rows at the top
  show who is ahead.
- **Lines:**
  - his challenge (new `imp_op_chef_challenge`): "Bake-off! Whoever tops their cake first
    wins!";
  - her instruction (new `roshan_op_chef_contest`): "Put the toppings on my cake before the
    imp finishes his!";
  - his defeat line: "Fine! The cake needed more sugar anyway!"
- **After she wins:** the curtain call.

### 6.2 Detective — SPARKLE RACE (race; inserted before CROWN)

- **Final act:** CASE BOARD (`evidence_shelves`), then the contest, then the CROWN flourish
  (`treasure_dais`).
- **Where it starts:** new `PHASE_STATIONS` entry `"SPARKLE RACE": "magnifier_tower"`. After
  she reaches it, the lens beat plays on the painting itself, with no card.
- **Skill:** searching. She sweeps her magnifier and holds it still on each hidden gold
  sparkle (existing lens engine: 0.45 s dwell, room-object reactions, 12 s glisten hint).
  - Her three sparkles are at clue spots 3, 4 and 5 of `StagePaths` for the detective.
  - Pass these indices explicitly. The default rotation `(index + phase_index × 3) % 8`
    (`scripts/opera_career_world_2d.gd:4253-4258`) would pick 6, 7 and 0, and SEARCH already
    uses 0, 1 and 2.
- **His side:** his own magnifier (the same `ui/magnifier.png` art, with a purple ring drawn
  around it, not recoloured) travels between his three purple sparkles at clue spots 6, 7
  and 1. It never zooms. Each sparkle he reaches lights purple and adds a pearl to his row.
- **Pace:** 3 units, `base_seconds` 21.0.
- **Flub:** after his 2nd sparkle.
  - His lens wanders to a decoy room object (the moon or a lantern from
    `DETECTIVE_ROOM_OBJECTS`) and finds nothing. He plays `guard`, then `recover`, then
    `idle`.
  - Line: "I looked under here. And here. Nothing! Detecting is hard."
- **Story:**
  - The offscreen steal line at the start ("The sparkly crown! Now everyone will look at
    ME!") is his voice: this imp is the thief pretending to investigate.
  - His defeat line pays it off: "Aww. It didn't even fit on my horns."
- **Lines:** his challenge (new): "Race you to the sparkles! Mine are purple!"; her
  instruction (new): "Find my gold sparkles before the imp finds his purple ones!"
- **After she wins:** CROWN (tap the chest handle, existing `crown_chest`). He watches, then
  bows at the curtain.
- **Retires H1:** `timed_retry`, `rival_solved`, `begin_guided_retry`, the reveal branch and
  the stale retry caption all go.

### 6.3 Ballerina — TWIRL-OFF (race; replaces the stage copy of GRAND TWIRL)

- **Final act:** the Hall stage (PEARL MIRROR, RIBBON TRAIL), then the contest. Practice keeps
  GRAND TWIRL unchanged.
- **Skill:** turning. She guides the pearl around the shell music box three times, either
  direction, with the same monotonic rules (multi-turn contract, §5.5).
- **His side:** at his mark, within reach, a small copy of the music box (`props/goal_ballerina.png`)
  with a purple arc that grows turn by turn. He spins in place, alternating `charge` and
  `slash`.
- **Pace:** 3 turns, `base_seconds` 10.5.
- **Flub:** after his 2nd turn.
  - He jumps (`hop_b`), wobbles (`stagger`) and flops (`bopped`, 1.3 s), with
    `props/fx_dizzy_stars.png` over his head.
  - Line: "Spin, spin, spin, FALL. That's the hard part."
- **Lines:**
  - his challenge (new): "Twirl-off! Three big spins. Ready? Spin!";
  - her instruction (new): "Twirl around the music box three times!";
  - his defeat line: "Whoops! I'm dizzy. Dizzy is a kind of dancing."
- **Rule note:** `DL-INT-08` says the Ballerina "is not a race". `DL-INT-14` supersedes that
  clause for this final contest only.

### 6.4 Candymaker — SHARING RACE (race; replaces SHARE)

- **Final act:** the contest only, at `candy_cart`.
- **Skill:** sharing one-to-one. Six waving friends (`TARGET_ANCHORS.target_candymaker` with
  the existing `_draw_candymaker_recipients`); each tap gives one friend one candy.
- **His side:** a small copy of the same waving friends at his hands; he serves them in
  order, each candy leaving his hand on his contact frame.
- **Pace:** 6 units, `base_seconds` 11.0.
- **Flub:** at his 3rd candy.
  - He eats it instead of giving it: `hop_b`, `taunt` with a candy piece at his mouth, then
    `recover`. His count does not advance.
  - Line: "One for the bag, two for me. That's how it works!"
- **Lines:**
  - his challenge (new): "Candy race! First to give every friend a sweet wins!";
  - her instruction (new): "Give a candy to every friend before the imp does!";
  - his defeat line: "Oof! My tummy hurts anyway. Too many gumdrops."

### 6.5 Doctor — BANDAGE RACE (race; replaces BANDAGE)

- **Final act:** CAST (`exam_booth`), then the contest at `recovery_bed`.
- **Skill:** bandaging. She traces the glowing authored bandage corridor (`trace_doctor`)
  three times, once per sore paw (multi-pass contract, §5.5).
- **His side:** a small copy of the same authored bandage trace (the
  `widget_trace_doctor_lit.png` route) at his hands; his wrap advances pass by pass on his
  contact frames.
- **Pace:** 3 passes, `base_seconds` 14.0.
- **Flub:** after his 2nd pass.
  - He wraps his own head instead of the paw: `stagger`, `guard` (1.0 s), `recover`.
  - Line: "Bandage on... bandage off. Bandage on my nose?"
- **Optional flourish:** after she wins, she may tap him to give him a bandage too. He plays
  `hop_b`. It is never required, continues by itself after 3 s and pays nothing.
- **Lines:**
  - his challenge (new): "Bandage race! Wrap all three paws!";
  - her instruction (new): "Wrap every sore paw, gentle and quick!";
  - his defeat line: "Ouch! Can you fix ME after?"

### 6.6 Farmer — FEEDING RACE (race; replaces PICNIC)

- **Final act:** HERD (`barn_doors`), then the contest at `blossom_arch`.
- **Skill:** aiming.
  - She pulls a veggie back from the basket and tosses it into the hungry piggy's picnic,
    four landings in all. This is the existing `farm_lob` verb (`FARM_LOB_GOAL` 4, cycling
    foods, pig munch reaction), which TOSS taught.
  - PICNIC's tap activity is replaced by this lob contest.
- **His side:** a small copy of the piggy picnic (`widget_target_farmer_mover.png`) just in
  front of him; each veggie leaves his hand, and his four landing dots fill.
- **Pace:** 4 units, `base_seconds` 17.0.
- **Flub:** after his 2nd landing.
  - His veggie bonks his own hat and he slips in mud: `charge`, `bopped` (1.1 s), `recover`.
    Use `props/fx_dust_puff.png` drawn with a brown modulate; the art itself is not
    recoloured.
- **Swapped lines:** the Farmer's lines fit best swapped.
  - The mud line is his flub: "Blegh! I got mud in my mouth."
  - The rock line is his defeat: "I planted a rock. Nothing grew. Farming is tricky!"
- **Lines:** his challenge (new): "Feeding race! My piggies eat first!"; her instruction
  (new): "Pull back and toss four veggies to the hungry piggy!"
- **Optional:** after she wins, his piggies trot over to her side.

### 6.7 Boxer — TITLE BOUT (points; converts TITLE IMP)

- **Final act:** the contest, then the BELT flourish, both at `shell_pavilion_stage`. The
  phase keeps its internal name TITLE IMP; TITLE BOUT is only the design name (§5.2).
- **Skill:** timing. She punches in the open window and guards his counter, using the
  existing wind-up, charge, recover and guard cycle (`scripts/opera_boxing_surface.gd:366-420`).
- **Points:** first to 6.
  - Her point: each landed punch.
  - His point: a counter that lands unblocked (`receive_friendly_hit`, `:167`), counted only
    if she touched in the last 4 s.
- **Flub:** at his 3rd point.
  - He mixes up left and right and leaves a long open window: `stagger` (0.8 s), then
    `recover` (1.2 s).
  - Line: "Left! Right! ...which one is left again?"
- **Lines:**
  - his challenge (new): "First to six! Put 'em up!";
  - her instruction (new): "Punch when the star shines, and guard when he winds up!";
  - his defeat line: "Good one! Best two out of three? No? Okay."
- **Rule note:** `DL-INT-09` and the `MA-OPERA-009` owner note describe friendly boxing with
  no loss. `DL-INT-14` supersedes the no-loss clause for the title bout only. Contact stays
  friendly and never removes her points.

### 6.8 Magician — HAT DUEL (points; inserted before PORTAL, stage only)

- **Final act:** the Hall stage (VANISH, TRACK, ROPE, CABINET), then the contest, then the
  PORTAL flourish.
- **Skill:** tracking. The imp performs the shuffle and Lamb-a' hides under one hat.
  - `windup` before the shuffle, `charge` and `slash` while the hats glide.
  - She taps the hat when it stops.
  - Taps during the glide are ignored (H9).
- **Points:** first to 3.
  - Her point: the right hat.
  - His point: the wrong hat. A wrong pick pays nothing.
  - He plays `stagger` when she is right and `taunt` when she is wrong.
- **Flub:** when he leads or is level at 2.
  - His trick backfires: `taunt`, `stagger`, `recover`. Lamb-a' pops up visibly on the right
    hat for one round.
  - Line: "I made it disappear! ...where did it go? Uh oh."
- **Lines:**
  - his challenge (new): "Watch my hats! Can you find Lamb-a'?";
  - her instruction (new): "Watch the hat with Lamb-a', then tap it when it stops!";
  - his defeat line: "Ta-daa! That was supposed to happen. Really."

### 6.9 Painter — PAINT-OFF (race; inserted before GALLERY)

- **Final act:** the contest, then the GALLERY flourish (`arch_easel`).
- **Where it plays:** new `PHASE_STATIONS` entry `"PAINT-OFF": "gazebo_easel"`, the easel where
  she painted. `FINALE_START` stays 2, so the imp enters and challenges at once.
- **Skill:** painting. She brushes across her canvas until the picture shows, using the
  existing coverage brush (`PAINT_REQUIRED_COVERAGE` 0.62 of the 10 × 6 grid) and the
  `goal_painter.png` reveal.
- **His side:** a small canvas on an easel at his brush hand, revealing the same picture in
  a fixed stroke order as his brush touches it.
- **Pace:** coverage 0 to 1, `base_seconds` 16.0.
- **Flub:** at 0.55 coverage.
  - He paints himself: painter stamp marks (`widget_target_painter_mark.png`) splat on his
    sprite. He plays `slash`, `stagger`, then `recover` (1.2 s).
  - Line: "I painted my hands. And the wall. And a bit of the floor."
- **Lines:**
  - his challenge (new): "Paint-off! First to finish their picture wins!";
  - her instruction (new): "Paint the whole picture before the imp finishes his!";
  - his defeat line: "Bonk! Now I'm a different colour."

### 6.10 Astronaut — LAUNCH RACE (race; replaces LAUNCH)

- **Final act:** the contest only, at `rocket_launch_dais`.
- **Skill:** repairing, then launching. PATCH taught the patching; the race repeats it at
  speed on the launch-pad rocket and adds the launch.
  - She taps the five leak sockets on her rocket (`TARGET_ANCHORS.target_astronaut`).
  - Then she holds for 1.2 s to blast off. The hold is the sixth unit.
- **His side:** a small copy of the same rocket (`widget_target_astronaut_mover.png`) at his
  hands; he presses each patch on, then his rocket rises.
- **Pace:** 6 units, `base_seconds` 12.0.
- **Flub:** at his 3rd patch.
  - His rocket hops sideways and bumps down (`props/fx_dust_puff.png`). He plays `stagger`,
    `bopped`, then `recover`.
  - Line: "My rocket went sideways. Into a wall. Twice."
- **Lines:**
  - his challenge (new): "Rocket race! Patch the leaks and blast off first!";
  - her instruction (new): "Patch every leak, then hold to blast off!";
  - his defeat line: "Wheee — oh. I landed. That's the hard bit."

### 6.11 Racer — GRAND PRIX (race; converts RACE)

- **Final act:** the contest, on the Canvas circuit after she reaches `ribbon_finish_arch`
  (`DL-INT-10`).
- **Skill:** steering. She stays on the ribbon track and grabs zoom strips for two laps
  (existing `KartDriving` kernel and lap dials).
- **His side:** his kart on the same track, as today (`rival_racer.png` on the kart).
  - Today he runs at 0.94 × nominal with a rubber band (`scripts/opera_racer_surface.gd:298-306`).
  - He slows by × 0.9 per rematch, never below × 0.75.
  - He waits while she is idle.
- **Finish rule:** today the race ends only when she finishes, and she wins regardless of
  place (`:311`). Now his kart finishing two laps first is his win (§5.5).
- **Flub:** at the first bend of lap two, a 1.5 s spin-out: his kart turns once and stops.
  Line: "Whoa whoa WHOA — how do you stop this thing?"
- **Lines:**
  - his challenge (new): "Two laps! First one home wins! Go, go, go!";
  - her instruction: the existing `roshan_op_racer_steer`, "Swipe to steer through the coral
    gates!";
  - his defeat line: "Pit stop! Pit stop! I need a pit stop!"

### 6.12 Pop Star — SING-OFF (points; inserted before ENCORE, stage only)

- **Final act:** the Hall stage (SOUND CHECK, DANCE, RHYTHM), then the contest, then the
  ENCORE flourish.
- **Skill:** listening. The imp sings a phrase on his three stars (`taunt` and `hop_b` as
  each star lights), then she sings it back on hers (existing `echo` verses).
- **Stars are code-drawn.** Her stars and his use the existing 10-point polygon. His are
  drawn in imp purple; no star art exists or is needed (H10).
- **Points:** first to 3.
  - Her point: a phrase sung back correctly.
  - His point: a wrong note, which pays nothing and starts the next round.
- **Flub:** when he leads or is level at 2.
  - His next phrase goes off-key and he sings it again as an easy two-note phrase. He plays
    `taunt`, `stagger`, then `recover`.
  - Line: "Was that the right note? It felt like a note."
- **Lines:**
  - his challenge (new): "Sing-off! Sing my song back to me!";
  - her instruction (new): "Listen to the imp's song, then sing it back!";
  - his defeat line: "My ears! Okay okay, you sing it."

### 6.13 Teacher — IMP'S LESSON (inverted; inserted after MATCH)

- **Final act:** MATCH, then the contest, both at `lesson_desk` on the same lesson board. New
  `PHASE_STATIONS` entry `"IMP'S LESSON": "lesson_desk"`.
- **Entrance:** when MATCH arms, he runs in and takes his place at the right end of the board
  (§4.11). Line (new): "Hello, class! I'm the new teacher!" He watches her MATCH lesson and
  bounces (`stagger`, `hop_b`) when she gets it right.
- **Challenge:** he taps the board with his pointer.
  - His line (new): "My turn to be the teacher! Can you catch my mistakes?"
  - Her line (new): "The imp is teaching it wrong! Tap the right answer to fix it!"
- **Rounds:** pattern, count, add, match, pattern, and so on.
  - Each lesson comes from `TeacherLessonPlan.make_lesson` at her current tier for that kind.
  - His wrong answer comes from `imp_answer` (§5.5).
- **His four kinds of mistake** (every line new):
  - **Pattern:** the row shows the pattern with its blank. He fills the blank with the wrong
    shape inside a purple outline: "Easy! This one comes next!" She taps the shape card that
    really comes next.
  - **Count:** his pointer hops across the pearls and visibly lands twice on one of them.
    Then he marks the wrong group card: "I counted them all! It's this many!" She touches
    each pearl herself and hears each number, as in her lesson; the answer cards wake only
    after every pearl is touched. Then she taps the right group.
  - **Add:** he presses the plus himself and the two groups join. He marks the wrong total:
    "Put them together, and it makes this many!" She counts each pearl, then taps the right
    total.
  - **Match:** he lifts the wrong shape card up beside the model: "Look! These two are the
    same!" She taps the shape that really matches.
- **Scoring:** as §4.15.
  - First pick right: "Oops! You fixed it!", her pearl.
  - First pick wrong: "Hee hee! I tricked you!", his pearl, then the golden help and her
    fix.
  - Hint: nobody scores.
  - First to 3.
- **Mercy after a lost attempt:** one tier easier per kind, and his most obviously wrong
  answer.
- **Mastery:** every round calls `TeacherLessonPlan.record_result(kind, assisted)` exactly
  like a lesson. `assisted` is true when her first pick was wrong or she used the hint. The
  contest counts as practice, and her later lessons adapt to it.
- **What the child sees:**
  - her familiar cream board, with the purple imp at its right end in his costume, pointing
    proudly at an answer outlined in purple;
  - she thinks, counts where needed, and taps the real answer;
  - his answer puffs away, the right one glows gold, and he wobbles and rubs his head;
  - two pearl rows at the top of the screen show who is ahead.
- **What stays true to the Teacher engine:**
  - time never answers;
  - counting stays one-to-one;
  - a wrong pick still gets immediate golden help;
  - nothing earned is lost.
  - The one change: inside the contest, her wrong first pick is his point (OD-B, OD-C).
- **Defeat and curtain:** his defeat line (new) is "You're the real teacher! I'll sit down
  now." He bows at the curtain call.
- **H2 is absorbed:** the imp is now visible in the final act, so the win line's "learning
  buddy" no longer credits someone the child never saw.
- **Art (no new art is required to ship):**
  - **Interim:** the plain mischief imp (`imp_mischief`). He has no `hop_a` or `hop_b`, so his
    entrance is `flee` then `idle`, and his win beat is `taunt` only. Do not use the doctor
    costume that the hidden buddy borrows today: a doctor teaching sums muddles the job.
  - **Recommended:** a new `rival_teacher` family with the same 13 states as the others. His
    costume:
    - round glasses slipping down his nose;
    - a small mortarboard cap tilted over one horn;
    - a cream cardigan with a coral bow tie;
    - a wooden pointer with a star tip as his held prop in every pose;
    - colours from the Teacher board: cream, navy outline, aqua and coral.
  - **How Codex makes it:** through the existing costume-family process.
    1. The owner approves the new idle.
    2. Codex generates Sheets A and B, with the identity locked to that idle, in the style of
       `assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md`.
    3. `tools/build_imp_costume_family.py` extracts the states (`--reuse-windup-hop-a`, as the
       other families did).
    4. `tools/build_imp_animation_delivery_manifest.py` records them, and every file gets its
       `ASSET_LICENSES.md` row.

### 6.14 Geologist — FIELD GUIDE MIX-UP (inverted; inserted before GEODE; pending confirmation)

- **Final act:** the contest, then the GEODE flourish (`crystal_gallery`, unchanged).
  - New `PHASE_STATIONS` entry `"FIELD GUIDE MIX-UP": "fossil_table"`.
  - `FINALE_START` stays 3, so the imp enters and challenges at once.
- **What changes today:** the field-guide imp is a co-op partner beside her from the first
  beat. Under OD-A he now appears only in the final act.
- **Entrance and challenge** (all lines new):
  - arrive: "Hello! I'm the field guide. I know everything about rocks!";
  - his challenge: "My turn to teach! Can you spot my mistakes?";
  - her instruction: "The imp is teaching it wrong! Tap his mistake to fix it!"
- **Rounds:** fossil, rocks, fossil, rocks, fossil.
  - **Fossil:** his fossil is built from the same three vertical strips of
    `geologist_fossil.svg` that she snapped together in FOSSIL, with one strip upside down.
    Her finished fossil sits small beside it as the model. His claim (new): "Look at my
    perfect fossil!" She taps the upside-down strip and it flips the right way up.
  - **Rocks:** three rocks lie on the pan (code-drawn with `_draw_mineral`), two the same and
    one different. His claim (new): "These rocks are all the same!" She taps the different
    one; it hops aside and sparkles.
- **Difficulty:** the Geologist has no mastery record, so the tier inside an attempt is her
  clean fixes so far, at most 2.
  - Rocks: tier 0 differs in colour and shape; tier 1 in colour only; tier 2 in shape only (a
    round pebble among faceted crystals, drawn in the same style).
  - Fossil: tier 0 flips the middle strip; later tiers an end strip.
  - A rematch starts again from tier 0.
- **Scoring:** as §4.15.
  - First tap on the wrong part: fixed, her pearl.
  - First tap on a right part: tricked, his pearl; the golden sparkle then marks the wrong
    part and she fixes it.
  - First to 3.
- **What the child sees:**
  - the grotto work surface, with his big fossil (one piece upside down) next to her small
    correct one, or three rocks on the pan;
  - the field-guide imp at the upper left, pointing proudly;
  - she taps the odd piece and it flips or hops, and he wobbles.
- **After she wins:** the GEODE flourish plays as today, with him watching; his defeat line
  (new) is "You know more about rocks than me!"; he bows at the curtain.
- **Art:**
  - **Interim:** `rival_detective`, which already ships as the field guide.
  - **Recommended:** a `rival_geologist` family: a yellow hard hat with a small lamp, a khaki
    vest with pockets, and a small rock hammer as his held prop. Codex makes it through the
    same process as §6.13.
  - No other new art.

## 7. Owner decisions still needed

### 7.1 Nursery (no costumed imp exists)

Today the Nursery is co-op with Nurse Faron, whose recordings are protected.

- **Option A:** keep it co-op, with no contest.
- **Option B:** QUIET TUCK-IN against the plain mischief imp (`imp_mischief`).
  - She swipes three blankets down at `moon_bed`; he tucks three cribs beside it.
  - Pace: `base_seconds` 12.0. Flub: his babies giggle awake and he re-tucks one.
  - He has no `hop_a` or `hop_b`, so his entrance is `flee` then `idle`, and his win beat is
    `taunt` only.
  - Two new lines: "Tuck-in race! Shh... I'll be quiet this time!" and "Tuck in every baby,
    slow and gentle!"
  - Faron stays beside Roshan.
  - *Recommended if contests should be universal.*
- **Option C:** B plus a commissioned `rival_nursery` family, which Codex would generate.

### 7.2 Geologist (specified by interpretation)

§6.14 applies OD-C's "similar educational type games" to the Geologist. Confirm it.
- If not, the Geologist stays co-op and §6.14 is dropped.
- Also say whether to commission `rival_geologist` or keep the borrowed detective costume.

### 7.3 Teacher (decided 2026-09-30)

OD-C decided it: the inverted IMP'S LESSON (§6.13). Still open: approve a `rival_teacher`
costume (recommended), or keep the plain mischief imp.

### 7.4 Restart scope

Confirm contest-only (this design) or the whole career (§1).

### 7.5 The Hall stage-long race

Retire it (recommended), or keep it as a no-loss race beside the contest (§4.14).

### 7.6 Rematch mercy

Confirm the curves: 0.8 per rematch with a floor of 0.55 for races; +1 point, capped at +2,
for points contests. Or, stronger: from the third rematch on, the imp flubs twice.

### 7.7 Chapter 2 story runs

They stay without the imp (C13). The owner may later want Ember-aligned story contests; that
would be separate work.

## 8. What this retires

| Retired | Where | Why |
|---|---|---|
| Detective timed retry, reveal and head-start branch | `scripts/opera_competition.gd:232-249`, `scripts/opera_career_world_2d.gd:3696-3710` and `:4618-4638` | H1; SPARKLE RACE replaces it |
| Stale retry caption and `op_retry` routing | `scripts/opera_career_world_2d.gd:3710` | H1; the clip stays on disk, unrouted |
| Background rival meter before the contest | `scripts/opera_competition.gd:210-236` for contest careers | C1; the imp competes only in the contest |
| "Rival hidden, cannot create a loss" as the final-act contract | `design/01_GAME_DESIGN.md:342-344` | superseded for the contest by `DL-INT-14` |
| Hall stage-long race (if the owner agrees) | `_performance_rival_work` | §4.14 |
| Crumb pay on misses inside a contest | `_miss_pay()` under `contest_mode` | C12 |
| Prewarming the plain crew families | `_prewarm_imp_textures` | H7 |

## 9. Tests

### 9.1 New probe: `scripts/probe_opera_imp_contest.gd`

Add it to `scripts/ci.sh` and to the probe workflow's trusted list. For every specified
career it checks:

1. **C1:** before the final act, the imp is not visible, no mirror station exists and no
   contest row shows.
2. **Entrance:** it completes within 3 s of the final act arming. Its poses run `flee`,
   `hop_a`, `hop_b`, `idle`, and input is accepted throughout.
3. **C8, passive:** with the contest open and zero input for 60 s, his units stay 0, and no
   `imp_won` or `player_won` fires.
4. **Idle pause:** after one touch followed by silence, his units stop growing within 4.1 s
   and resume on the next touch.
5. **Fast child:** a scripted fast child wins the first attempt. The defeat poses run
   `stagger`, `bopped`, `recover`; the tier follows the margin; the flourish or curtain
   follows.
6. **Slow child:** a scripted slow but active child loses. Then:
   - `imp_won` fires once, and her input is ignored during the win beat;
   - within 2.2 s both rows are 0, her activity is open and accepting input, and she has not
     moved;
   - earlier phases are still complete; stars, pearls and the save are unchanged;
   - his rate is 0.8 of before, or his target is plus 1.
7. **Flub:** it fires exactly once per attempt and again after a reset.
8. **Points contests:**
   - shuffle taps are ignored, a wrong hat or note scores for him and pays 0;
   - Boxer counters score only after recent input.
9. **Save:** leaving during the contest resumes at the contest phase with zero units, the imp
   present and no earlier activity replayed. The Hall resumes through
   `opera_performance_checkpoints`, the Teacher and Geologist through their own checkpoints,
   and the others through `opera_phase_checkpoints`.
10. **C13:** Chapter 2 story, tutorial and adapter configs contain no contest phase and never
    show the imp.
11. **Demos:** a demonstration never moves either row (`DL-INT-06`).
12. **Voice:** every contest line resolves to an existing exact clip, and each caption equals
    its clip's text.
13. **Teardown:** close, Back, pause-leave and focus loss mid-contest leave no running timer,
    tween or queued imp line.

**Inverted contests** (Teacher; Geologist if confirmed) replace checks 4 and 7, and add:

14. **No clock:** with a round open and zero input for 60 s, neither side scores.
15. **Truth last (C15):**
    - his marked answer is never the correct choice;
    - every round ends with the correct answer placed by her;
    - a wrong first pick scores his point, and the golden help follows at once.
16. **Hint:** a hinted round scores for nobody and still ends with her placing the right
    answer.
17. **Teacher lessons:**
    - rounds rotate pattern, count, add and match at her current tier per kind;
    - count and add answers stay locked until every pearl is touched;
    - each round writes `record_result` with the right `assisted` flag;
    - ordinary lessons from `make_lesson` are unchanged.
18. **Geologist rounds:** exactly one strip is upside down, or exactly one rock differs.
19. **Mercy:** after a lost attempt, the tier drops one step (never below 0), his answer is
    the farthest wrong choice, and his target rises by 1.

### 9.2 Probes to update deliberately (behaviour changes are the goal)

- `scripts/probe_opera_2d.gd`:
  - update phase names and counts for inserted contests;
  - remove the Detective reveal expectations (`:1178-1179` and the `reveal_t` resets);
  - keep "rival hidden during earlier minigames" (`:408-409`).
- `scripts/probe_opera_performance.gd:192` asserts "the imp may finish first without forcing
  a loss, retry, or award". Scope it to the stage-long race if the owner keeps that race;
  otherwise replace it with the contest's rematch assertions.
- `scripts/probe_opera_detective.gd`: SPARKLE RACE replaces the timed-retry path.
- `scripts/probe_passive.gd`: add the zero-input contest case.
- `scripts/probe_imp_animation_art.gd`: every pose a contest names resolves to a file of its
  family, after substitutions.
- `scripts/probe_opera_2d_balance.gd` and `scripts/probe_opera_balance.gd`: walk to stations
  and drive activities (H4). Report `T_child` per contest.
- `scripts/probe_opera_2d.gd`, Teacher and Geologist:
  - "teacher keeps the borrowed doctor buddy hidden through its lesson finale"
    (`:1246-1248`) becomes "hidden before the final act, visible from MATCH";
  - the Geologist's "care partner beside Roshan from the first beat" becomes "hidden before
    the final act" if §6.14 is confirmed.
- `scripts/probe_save_recovery.gd`: Teacher and Geologist checkpoints restore the contest
  phase with an empty mechanic snapshot.

### 9.3 Gates

Run the full trusted suite (`scripts/ci.sh`) green on CI for the work branch, plus the two
audit tools in `CLAUDE.md`. Green probes do not establish owner, device or child acceptance.

## 10. Governance

**Already in this handoff change:**
- `DL-INT-14`, added to design/06 as the target contract;
- pointer sentences on `DL-INT-08`, `DL-INT-09` and `DL-INT-10`;
- the amended "Competition is scoped" bullet in `design/01_GAME_DESIGN.md`;
- notes in the master index and in the master-audit planning entry;
- ledger rows for this packet.

**Codex's implementation change must also:**
- update the phase counts in `DL-INT-07`, `DL-QA-12`, `design/01_GAME_DESIGN.md` and
  `design/00_MASTER_INDEX.md` together (H8);
- add `ASSET_LICENSES.md` rows and all-audio ledger rows for the new voice files;
- carry an audit-impact record naming `DL-INT-14`, the updated rules, and evidence per rule;
- rewrite the "Geologist is cooperative" bullet in `design/01_GAME_DESIGN.md` if §6.14 is
  confirmed;
- add `ASSET_LICENSES.md` rows and delivery-manifest entries for any `rival_teacher` or
  `rival_geologist` family the owner approves;
- report implementation, machine verification, and outstanding visual, device, child and
  owner acceptance separately.

## 11. Work order

| Step | Work | Gate |
|---|---|---|
| W0 | Owner answers §7.4 to §7.6 (defaults above apply if unanswered) | none |
| W1 | `OperaImpContest` logic class, save key, opt-out, and the new probe's logic checks | probe logic green |
| W2 | Shared presentation: entrance, presence, rows, mirror station, rematch, defeat, tier | Chef pilot green |
| W3 | Pilot contests: Chef (tap race), Detective (lens race; retires H1) and Magician (points; fixes H9) | pilots green; owner plays them on the phone |
| W4 | Surface contracts: multi-turn twirl, multi-pass trace, lob, paint mirror, tap then hold | focused probes green |
| W5 | Remaining contests: Ballerina, Candymaker, Doctor, Farmer, Painter, Astronaut, Pop Star | full suite green |
| W6 | Specialists: Boxer points and Racer finish | boxing and racer probes green |
| W6b | Inverted contests: Teacher IMP'S LESSON, then Geologist FIELD GUIDE MIX-UP once the owner confirms it | inverted checks 14 to 19 green; owner plays the Teacher contest |
| W7 | New voice lines through the filler pipeline, ledger rows and licences; any approved `rival_teacher` or `rival_geologist` family | voice and imp-art probes green |
| W8 | Balance probe fix and `base_seconds` tuning, then the count and canon updates (H4, H8) | full suite green; merge to `dev` |

## 12. Acceptance

Report four things separately:

1. **Implementation:** what changed, file by file.
2. **Machine verification:** the new and updated probes, the full suite, and the two audit
   tools.
3. **Visual, device and child checks** (outstanding until done):
   - Mobile captures at two supported aspects;
   - the target phone;
   - an observed child session: can she tell who is winning, does she want the rematch,
     does an imp win upset her;
   - for the Teacher: does she understand that she is correcting the imp, and does she still
     answer her ordinary lessons correctly afterwards (no mistakes learned from him);
   - the owner playing each pilot.
4. **Owner acceptance of the decisions in §7.**

Publication of this handoff is not acceptance of any of them.
