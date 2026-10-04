# Opera imp contests: design and implementation specification

- **Status:** `PROPOSED / CANDIDATE`. The owner direction is recorded. Implementation,
  probes and acceptance are pending.
- **Baseline:** `dev` at `55032e88936b22723fd9af5282c61ba6696b3d43`. Every `file:line`
  anchor refers to that commit.
- **Revisions:**
  - 1 (`7ec82d46`): the twelve costumed contests;
  - 2 (`df01b7ce`): owner decision OD-C and the inverted Teacher and Geologist contests
    (the Geologist's became a race in revision 5);
  - 3 (`86732a47`): the Day Two art review's corrections on reusing current art and on the
    imp touching his work (§4.16);
  - 4 (`1fbcc9db`): owner decision OD-D, silly questions and sillier imp lines (§4.15,
    §6.13);
  - 5: owner decision OD-E: the Teacher's game cannot be lost and is always silly (§4.15,
    §6.13); defense contests for the Chef and the Nursery (§4.17, §6.1, §6.15); the
    Geologist races her for the same geode (§6.14); a radical slowdown after two failures
    (§4.3, §4.4, §4.7). Aligned at the `dev` merge with the owner's 2026-10-03
    animation-workflow policy for any new imp costume (§4.16, §6.13).
- **Prepared by:** Claude. Written specification only, with no images, per the CLAUDE.md
  rule "Codex handoffs: Claude writes, Codex builds images". Codex implements.
- **Machine-readable twin:** [data/contest_spec.json](data/contest_spec.json). The prose and
  the JSON agree. If Codex finds a conflict, the owner decisions in §1 win, then this
  document, then the JSON.
- **Before picture:** [CURRENT_STATE_ANALYSIS.md](CURRENT_STATE_ANALYSIS.md).

## 1. Owner decisions (2026-09-30 and 2026-10-04)

- **OD-A:** "No, I think imp comes in during the final act, there should be a contest at
  the end that reflects part of the skill of the job that's a challenge against the imp"
- **OD-B:** "If imp wins, the game restarts immediately afterwards."
- **OD-C:** "The teacher should have an imp, but the game inverts, he teaches information
  that's wrong and it's your job to figure it out, which beats the imp. Similar
  educational type games"
- **OD-D:** "Lean into silly humor here, questions like, which smells the worst, farts,
  garbage, old diapers or rotten cheese?"
- **OD-E (2026-10-04):** "The imp teacher games can't be lost by design, and should always
  be silly. Imp maybe tries to mess up your recipes and put gross things in the food?
  Geologist should be competing for time with Roshan for the same goal. You should stop
  the imps from being too noisy when the babies are sleeping. Imp just restarts contest at
  end, after two failures, imp should radically slow down."

What they mean for the game:
1. The career's costumed imp is **not seen** before the final act. He **enters** when the
   final act begins.
2. The final act **ends in one head-to-head contest** against him. The contest uses a real
   skill of that job.
3. **He can win** everywhere except the Teacher. When he does, **only the contest restarts**,
   at once. The first restart keeps his pace; **after two failures he slows down
   radically** (§4.3, §4.4, §4.7, §4.17).
4. **The Teacher inverts and cannot be lost.** Her imp teaches with silly mistakes and she
   fixes each one. Every round ends with her pearl; he never scores (§4.15, §6.13).
5. **Silly and gross-funny.** Every Teacher round is silly: silly questions like the
   owner's smell question alternate with silly versions of her lessons, and all his lines
   are silly (§6.13).
6. **Defense contests.** The Chef's imp sneaks gross things onto her cake, and noisy imps
   try to wake the Nursery's sleeping babies. She keeps them away while she finishes her
   job (§4.17, §6.1, §6.15).
7. **The Geologist races her for the same goal:** one geode, two diggers (§6.14).

**Settled by OD-E** (these were open questions in revisions 1 to 4):
- **Restart scope:** the contest only. Earlier activities, stars, pearls, stickers and
  saves are kept.
- **Educational scope:** the inverted format is the Teacher's alone. The Geologist races.
- **Silly scope:** every Teacher round is silly.
- **Rematch mercy:** the first restart is just a restart. After two failures the imp slows
  down radically and stays slow for the rest of the visit.
- **Nursery:** it gets a contest, QUIET TIME, against the plain imps; Faron stays
  Roshan's teammate.

**Interpretation to confirm with the owner (the recipe idea).**
- OD-E's "Imp maybe tries to mess up your recipes and put gross things in the food?" is
  applied to the Chef by default. YUCKY RECIPE replaces the topping race (§6.1); the
  Candymaker keeps its sharing race.
- If the owner meant the Teacher's silly lessons instead, the Chef keeps the revision 1 to
  4 topping race and the Teacher gains a silly recipe round. The default applies until the
  owner says otherwise.

The new binding rule `DL-INT-14`, in
[design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
records these decisions as the target contract.

## 2. Terms

| Term | Meaning |
|---|---|
| final act | The phases from `FINALE_START` to the end (room careers), or the Hall stage act |
| contest | The one head-to-head phase at the end of the final act |
| attempt | One run of the contest from zero; a restart begins a new attempt |
| rematch | An attempt after the imp has won |
| failures | How many times the imp has won in this visit; from 2 the radical mercy applies |
| race contest | Both work through the same number of units; first to finish wins |
| points contest | Turns or rounds; each round gives a point to one side; first to the target wins |
| defense contest | The imp sends hazards while she does her job; she removes each with one tap and wins by finishing; he wins only if three hazards count against her at once (Chef, Nursery) |
| hazard | One gross thing tossed onto her cake, or one noisy imp at a crib; always telegraphed first |
| unit | One countable piece of work: a topping, a sparkle, a turn, a paw, a landing, a seam |
| mirror station | The imp's own small copy of the activity, showing his units; input-transparent |
| flub | His one scripted mistake per attempt, which is her comeback moment |
| flourish | An existing victory activity after the contest, such as CROWN, BELT, PORTAL or ENCORE |
| inverted contest | The Teacher's silly lesson game: the imp teaches with one silly mistake per round and she fixes it; it cannot be lost |
| round | One silly question or silly lesson in the inverted contest; it always ends with the right answer placed by her and her pearl |

## 3. The contest contract

Each rule has an ID (C1 to C16) so probes and reviews can cite it.

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
- **C6. He can win, except in the Teacher's game.** In a race contest he wins by finishing
  his units first. In a points contest he wins by reaching his target first. In a defense
  contest he wins when three hazards count against her at once. Ties go to Roshan. The
  inverted Teacher contest cannot be lost: he never scores (OD-E).
- **C7. Instant, friendly restart of the contest only.**
  - When he wins there is a win beat of at most 2 s, then the contest resets and she can
    play again immediately (OD-B, confirmed by OD-E).
  - There is no fail screen, text, sad sting, life counter or wait.
  - Nothing earned is lost: stars, pearls, stickers, saves and every finished activity stay.
  - Only the attempt's own units reset. `DL-INT-14` records that this reset is the
    owner-directed rematch, not a punitive fail state (`DL-AGE-03`).
- **C8. Zero input never decides.** He works only while she is playing. With no input he
  freezes (§4.5). No input can produce a win or a loss (`DL-AGE-04`), and demonstrations
  never move either side (`DL-INT-06`). In defense contests the first hazard waits for her
  first touch and every hazard holds still while she is idle (§4.17). The inverted contest
  has no clock at all.
- **C9. Radical mercy after two failures (OD-E).** The first restart is just a restart, at
  the same pace. From the third attempt he slows down radically: races at 0.4 of his pace,
  points contests with half-speed cues and a target 3 higher, defense contests with far
  fewer hazards, and the Racer at half speed (§4.3, §4.4, §4.17, §6.11). He stays slow for
  the rest of the visit, so an engaged child wins soon after.
- **C10. Wordless and readable.**
  - Progress shows as two rows of pearls or bars with a face icon each; the Teacher's game
    shows only hers. The score rows carry no numbers or words. Lesson content keeps its own existing symbols, such as the
    Teacher's numeral labels.
  - Every beat also has an exact voice line (`DL-SND-13`).
- **C11. One finger.** Every contest can be finished with one finger, using the same verb
  as the activity it comes from.
- **C12. No payment for misses.** Inside a contest, wrong input pays nothing. In points
  contests a wrong answer is the imp's point. In the Teacher's game a wrong pick earns
  only his silly gloat, never a point.
- **C13. Story runs opt out.** Chapter 2 story runs (`reward_policy chapter2_story`), tutorial
  runs, and configs with `phase_overrides` or `scene_adapter` get no imp and no contest. The
  test is the same as `OperaPerformancePlan.enabled`
  (`scripts/opera_performance_plan.gd:15-19`).
- **C14. Clean teardown.** Close, Back, pause-leave and focus loss stop every contest timer,
  tween and queued imp line. Re-entering resumes at the contest phase with a fresh attempt
  (§4.9).
- **C15. Truth last.** In the inverted contest every round ends with the correct answer on
  the board, placed by her. The imp's wrong answer is never left standing (§4.15).
- **C16. Fair hazards.** In a defense contest every hazard is telegraphed before it lands
  or sounds, is removed by one tap, stays cartoony and gentle (never a startling bang), and
  never destroys finished work: a gross thing on a topping only hides it until flicked off
  (§4.17).

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
  `hop_b` (0.35 s), then rests in `idle`. The plain imps have no hop poses, so they run in
  with `flee`, then rest in `idle`.
- **Line and timing:** his arrive line plays once per act (`imp_op_<career>_arrive`; existing
  for the twelve costumed careers and the Nursery, new for the Teacher and Geologist). The
  whole entrance takes at most 3 s.
- **Input is never blocked.** If she opens the first final-act activity during the entrance,
  he finishes the entrance without taking focus.

### 4.2 Between final-act phases

- He is present at his mark and does not compete. There is no mirror station, score row or
  clock.
- When she completes a final-act activity before the contest, he reacts: `stagger` (0.3 s),
  then `hop_b` (0.3 s), then `idle`. No line; he is impressed, not competing.
- Careers whose contest is the first final-act phase (candymaker, painter, astronaut, boxer,
  racer and geologist) go straight from the entrance to the challenge.

### 4.3 Race pacing

- His units grow while he is active:
  `imp_units += delta × units_total / base_seconds × mercy_rate`.
- `mercy_rate` is 1.0 for the first and second attempts and 0.4 from the third, after two
  failures (OD-E). The Racer uses its own setting (§6.11).
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
  - target: an engaged child wins the first attempt about three times in four, and every
    time once the radical mercy applies.
  - Owner play-testing overrides the probe.

### 4.4 Points contests (Boxer, Magician, Pop Star)

- Each round ends in exactly one point, for her or for him (§6.7, §6.8, §6.12).
- **Targets:** her target is the career's `points_to_win`. His target is the same; after two
  failures it rises by 3.
- **Slower cues after two failures:** shuffles, song phrases and his wind-ups run at half
  speed. The first restart keeps the normal speed (OD-E).
- **Ties:** if both reach their targets on the same event, she wins.

### 4.5 Idle pause

- **Trigger:** she has not touched her activity surface for 4.0 s during the contest.
- **What he does:** he freezes, alternating `taunt` (0.6 s) and `guard` (0.6 s). The
  activity's existing re-hint or assistance plays.
- **Resume:** he resumes on her next touch.
- **Rule:** the pause never ends by itself. A contest with no input stays unresolved
  forever, and the passive probe must prove it.
- **The Teacher's contest** has no idle pause, because he never acts on time (§4.15).
- **Defense contests** hold every hazard still instead, and the first hazard waits for her
  first touch (§4.17).

### 4.6 The flub

- **Exactly one flub per attempt**, at a fixed point: a unit count, a coverage fraction, a
  hazard count (defense contests), or in points contests "when he leads or is level at 2".
- **What happens:**
  - He stops for the listed `flub_seconds` (about 2 s) and plays the career's flub poses.
  - His existing copy line plays (the Farmer uses its bop line; §6.6).
  - A small existing effect or prop shows what went wrong.
- **What it is for:** it is her comeback moment. His row visibly pauses while hers can keep
  growing.
- **Rematches:** the flub resets with each rematch, so every attempt has one.
- **Defense contests:** the flub replaces one hazard. The Chef's toss lands on his own hat;
  a Nursery imp trips over his toy and falls asleep (§6.1, §6.15).
- **The Teacher's contest** has no flub: every round is already his mistake (§4.15).

### 4.7 He wins: instant rematch (contest-only restart)

- **The win beat (at most 2 s).**
  - Her activity stops accepting input, so a finish after his win cannot count.
  - He plays `hop_b` (0.6 s), then `taunt` (0.8 s), with the new shared line
    `imp_op_contest_win`: "I won! I won! Let's play again!"
- **The reset.**
  - Both rows empty. Her placed pieces lift away with a soft puff (`fx_dust_puff.png`), and
    his mirror station clears.
  - `failures += 1`. From the second failure on, the radical mercy applies (§4.3, §4.4,
    §4.17, §6.11) and stays for the rest of the visit. The first restart keeps his pace.
  - The flub is available again.
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
- **The Teacher's game never reaches this section:** it cannot be lost (§4.15).

### 4.8 She wins: defeat beat, flourish, cheer tier

- **Defeat beat:** he plays `stagger` (0.4 s), then `bopped` (1.0 s), then `recover` (0.6 s),
  with his defeat line (the existing bop line, except for the Teacher and Geologist, whose
  defeat lines are new). At the same time Roshan plays her existing `cheer` animation
  (`_play_roshan_animation("cheer")`).
- **What comes next:**
  - If the career has a flourish (Detective CROWN, Boxer BELT, Magician PORTAL, Pop Star
    ENCORE, Painter GALLERY), it arms as the next phase. He watches from his mark and does
    not compete.
  - Otherwise the curtain call plays, and he bows as today.
- **Cheer tier.** It comes from how she played, never from time.
  - Race and points contests: her lead when she finishes, as a share of the contest (units
    for a race, points for a points contest). Tier 3 if the margin is at least 0.35, tier 2
    if at least 0.15, otherwise tier 1.
  - Defense contests: the worst moment of the attempt. Chef: never more than one gross
    thing on the cake at once is tier 3, two is tier 2. Nursery: no noise is tier 3, one
    noise tier 2, two noises tier 1.
  - Teacher: tier 3 when she fixed both lessons on her first pick without the hint,
    otherwise tier 2. Silly-question picks never lower it.
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
  failure count reset, so the normal pace returns.
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
- **Defense contests:** her row counts her units. His row shows up to three purple pearls
  for the hazards that count against her: gross things on the cake right now (the row
  drops when she flicks one off), or noises so far.
- **The Teacher** shows her row only: four pearls, one per round. He never scores.
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

**Contests on her own object** have no mirror station:
- **Teacher:** he teaches on her board, at its right end, about 150 px tall with his feet
  near (1205, 640). He stays clear of every choice card (the right-most card ends at
  x = 1133) and of the hint button at (1115, 150).
- **Geologist:** he leaves the field-guide spot at (78, 218) (`_stage_room_finale_partner`,
  `:1793-1799`) and works the same geode from its lower right (§6.14).
- **Chef:** he stands by the cake stand and tosses onto her own cake (§6.1).
- **Nursery:** the imps come to the cribs inside her own, enlarged panel (§6.15).

**Curtain call:** stays on the proscenium for everyone (`_position_curtain_call_cast`, `:1852`).

### 4.12 Voice rules

- **One voice at a time** (`DL-SND-14`). When two lines collide, the higher priority plays and
  the lower one is dropped, but its poses still play. Priority, highest first:
  1. her instruction line and "Again!";
  2. the imp's challenge;
  3. the imp's win line;
  4. the imp's flub and defeat lines;
  5. the imp's arrive line;
  6. Roshan's shush (Nursery) and the imp's toss line (Chef), which are simply skipped when
     anything else is playing.
- **Limit:** at most one imp line every 3 s.
- **Skipping:** lines are touch-skippable and clear on teardown (`DL-SND-03`).
- **Routing:** `show_msg(who, text, vo)` plays `<speaker>_<vo>.ogg`, preferring `filler_v1`.
  In the Opera the caption hides when an exact clip exists (`scripts/audio_director.gd:493`),
  so every caption text must match its clip.
- **New lines:** 77 lines (61 imp, 16 Roshan; 32 of them for the silly questions) are added
  through the existing filler pipeline, as provisional synthetic filler: imp preset
  "Mike", Roshan preset "Joy". See
  [data/imp_voice_inventory.json](data/imp_voice_inventory.json) for the list. One more
  instruction reuses an existing clip (the Racer's).
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
- **The inverted contest** uses the same states differently: `charge` and `slash` point at
  the board and place his wrong answer; `taunt` is his proud claim; `stagger` then `recover`
  when she fixes it; `hop_b` then `taunt` for his silly gloat after a wrong pick. Defeat and
  bow are as usual.
- **Defense contests:** `windup` is his telegraph, the hazard at his hands; `slash` is the
  toss or the noise; `stagger` is a flicked-back gross thing bonking him; a shushed Nursery
  imp covers his face (`guard`), then tiptoes off (`flee`).
- **Contact:** each of his units lands on the contact moment of his `slash` pose, where his
  hand or tool meets his job object (§4.16).
- **Preload:** only the career's family, 13 textures (fixes H7). The Nursery preloads its
  two plain families, 22 textures.

### 4.14 Hall careers (Ballerina, Magician, Pop Star)

- **Practice** keeps its activities unchanged. Contest phases are stage-only, so
  `OperaPerformancePlan.build` must not copy them into practice.
- **The stage-long race.** Today the imp also races through every stage activity
  (`honest_stage`, `_performance_rival_work`).
  - **Recommended:** retire it. He enters at the stage start (§4.1), watches between stage
    activities (§4.2), and competes only in the contest. That matches OD-A's "a contest at
    the end", and a four-year-old then meets one clear challenge instead of two overlapping
    races.
  - This is an open owner question (§7.2). If the owner keeps it, the stage-long race must
    stay no-loss, and only the contest can restart.
- **Mastery** (`scripts/opera_mastery.gd`): medal times still use the stage's active seconds.
  Each rematch counts as one assist. A won contest earns at least Bronze.

### 4.15 The inverted contest (Teacher)

OD-C turns the Teacher's contest around, OD-D makes it silly, and OD-E makes it impossible
to lose. The imp is the teacher, and he gets things wrong on purpose, in silly ways.

**A round**
1. The board shows one silly question or one lesson (§6.13).
2. He presents it with exactly one silly mistake. He points and places his wrong answer
   (`charge`, `slash`), marks it with a purple outline, and claims it proudly (`taunt`) with
   his claim line.
3. She checks it. Where the lesson already asks her to count, she counts first, exactly as
   in her lessons.
4. Her **first pick**:
   - **Right:** his mistake pops off with a soft puff (`fx_dust_puff.png`), the right answer
     settles in, and he plays `stagger` then `recover` with "Oops! You fixed it! My brain is
     full of bubbles!" (lesson rounds) or his reaction line (silly questions).
   - **Wrong:** only his silly gloat. He plays `hop_b` then `taunt` with "Hee hee! Tricked
     you!" (silly questions use their own tricked lines). There is no imp point. The golden
     help then shows the right answer, with the existing Teacher help clip ("Look at the
     golden sparkle. You can try again."), and she taps it.
   - **Hint:** the hint button stays available, and she still finishes the round by placing
     the right answer.
   - Either way the round ends with one pearl in her row.
5. After the fourth round he is defeated (§6.13).

**Rules**
- **It cannot be lost (OD-E).** He never scores and never wins, so the contest never
  restarts. Her row is the only row on screen (§4.10).
- **Always silly (OD-E).** Every round is a silly question or a silly lesson.
- **Truth last (C15):** every round ends with the correct answer on the board, placed by
  her.
- **No clock:** there is no idle pause and no flub. Zero input leaves the round waiting
  forever.
- **Four rounds:** silly question, silly lesson, silly question, silly lesson. The first is
  always the owner's smell question.
- **Cheer tier:** §4.8.
- **Silly questions** (§6.13) show five pictures: four that fit the question and one that
  obviously does not, which he picks. Any fitting picture is right, because the child's
  choice among them is her opinion. Picking his card only earns his gloat.
- **Humor rule (OD-D):** silly and gross-funny, never mean.
  - The joke is always on the imp or on the thing, never on the child or her family.
  - He never calls her names and never says she smells.
  - Gross pictures stay cartoony.

**Why this suits a four-year-old.** Early-maths research has long used a "puppet paradigm":
a puppet counts, sometimes wrongly, and the child says whether it was right. Preschoolers
catch a puppet's counting errors even before their own counting is reliable (Gelman and
Meck, 1983, *Cognition* 13, 343–359). Spotting the imp's mistake is therefore
age-appropriate. Because he never scores, a wrong pick costs her nothing but a giggle. That
is design rationale, not evidence about this game; the child session in §12 checks it.

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

**Optional art stays optional.** The Doctor's bandage overlay and the new teacher or
geologist imp costumes are owner-dependent options, not generation orders. Any new imp art
follows the owner's 2026-10-03 animation-workflow policy (§6.13).

**One shared silly icon set** supplies the Teacher's silly pictures, the Chef's gross things
and the Nursery's noisy toys (§6.13). Codex checks existing approved art first
(`DL-PLAN-03`); two existing candidates are `assets/props/story/fruit_banana.png` and
`assets/flats/castle/rooms/room_bubble_bath_item_rubber_duck.png`.

### 4.17 Defense contests (Chef, Nursery)

OD-E gives two careers a new kind of contest: the imp tries to spoil her work, and she stops
him while she finishes it.

**Shape**
- She does her job: topping the cake (Chef), or keeping the babies asleep (Nursery).
- He sends hazards: gross things tossed onto her cake, or noisy imps tiptoeing up to the
  cribs.
- She removes each hazard with one tap.
- She wins when her job is done. He wins only when three hazards count against her at
  once: three gross things on the cake, or three noises that pop all three sleep bubbles.
  His win plays the win beat and restarts the contest (§4.7).

**Fair hazards (C16)**
- **Telegraph:** every hazard shows first. He holds it at his hands in `windup` for about
  0.8 s (Chef) or 2.5 s (Nursery, with the existing `fx_telegraph_ring.png` pulsing) before
  it lands or sounds.
- **One tap** removes a hazard. Missed taps are harmless.
- **Gentle:** gross things are cartoony icons; noises are short, soft, comic existing sounds
  at reduced volume, checked against the all-audio rules (`DL-SND-12`, `DL-SND-14`); never a
  startling bang.
- **Nothing finished is lost:** a gross thing may land on a topping and hide it, but
  flicking it off shows the topping again.

**Zero input never decides (C8)**
- The first hazard of each attempt waits until her first touch on the contest surface.
- After that, hazard timers run only while she is active. Once she has not touched the
  contest surface for 4.0 s, every imp holds still in his telegraph pose, the existing
  rehint plays, and he resumes on her next touch. Missed taps count as touches.
- In the Nursery, imps still tiptoe in while she is idle, so there is always one to tap,
  but none counts down.

**Flub:** one per attempt (§4.6).

**Mercy (OD-E):** the first restart keeps the same pace. After two failures the Chef tosses
a third as often (every 12 s) with a 1.6 s windup, and the Nursery sends one imp at a time
with a 6.0 s windup, in a wave of four instead of six.

**Rows and cheer tier:** §4.10 and §4.8.

## 5. How to build it

### 5.1 A new logic class

Add `scripts/opera_imp_contest.gd` (`class_name OperaImpContest`, `RefCounted`), modelled on
`OperaPerformancePlan` and `OperaMastery`: pure logic, no nodes, testable headless.

It holds:
- `CONTESTS`: the per-career table from §6 and the JSON (archetype, units or points, base
  seconds, hazard timings, flub point and seconds, flub poses, flourish, venue, voice keys);
- `enabled(career, config)`: the C13 opt-out, using the same test as
  `OperaPerformancePlan.enabled`;
- `apply(career, phases, two_act)`: returns the phase list with the contest in place.
  - A **replaced** activity keeps its phase `name` and gains a `contest` dictionary.
  - An **inserted** contest is a new phase with its own `name`.
  - For Hall runs it touches only the stage copies;
- the attempt state: `state`, `attempt`, `failures`, `her_units`, `his_units`,
  `mercy_rate`, `hazards`, `flub_done`, `idle_t`, `beat_t` and `margin`;
- `tick(delta, her_units, her_touched) -> Array[String]`. The events are `imp_unit`,
  `imp_overtaken`, `imp_worried`, `idle_pause`, `idle_resume`, `flub_start`, `flub_end`,
  `imp_won` and `player_won`;
- for the `defense` archetype, the same `tick` also schedules hazards and emits
  `hazard_telegraph`, `hazard_landed` and `hazard_noise`; `clear_hazard(id)` takes her tap
  from the surface. The first hazard waits for her first touch, and no hazard timer runs
  while she is idle (§4.17);
- for the `inverted` archetype (Teacher), no pacing at all: `finish_round(result)` takes
  `fixed`, `tricked` or `hinted` from the surface, records it for the cheer tier, and
  returns `player_won` after the fourth round. It never returns `imp_won`;
- `reset_attempt()` and `result() -> {margin, tier, failures}`.

### 5.2 Phase naming

- **Replaced activities keep their internal names:** TOP, SHARE, BANDAGE, PICNIC, TITLE IMP,
  LAUNCH, RACE, GEODE, and the stage copy of GRAND TWIRL. `PHASE_STATIONS`,
  `HOTSPOT_PHASE_ALIASES`, the hotspot catalog, voice keys and probes all key on those names.
- **Inserted contests are new phases:** SPARKLE RACE, PAINT-OFF, HAT DUEL, SING-OFF, IMP'S
  LESSON and QUIET TIME. Each needs a `PHASE_STATIONS` entry (§6), a hotspot entry, voice
  keys and probe coverage.
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
    of `_set_finale_visible`). Under OD-A he appears only when GEODE arms, and he works
    the geode from its lower right (§6.14).
- **Nursery.** Faron keeps the partner slot (`rival_actor` loads `faron_nursery.png`,
  `:1222`). The lead mischief imp who enters at BEDTIME is a separate actor, and the QUIET
  TIME imps are drawn by the new `nursery_quiet` surface mode (§5.5).
- **Prewarm.** `_prewarm_imp_textures`: the career family only (H7); the Nursery's two plain
  families.
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
  - The Nursery keeps Faron as its partner, but its final contest is against the noisy
    imps: drop `cooperative` for the contest result so QUIET TIME can be lost and restarted
    (the team-finale branch, `scripts/opera_competition.gd:263-267`).
  - Let `complete()` accept the contest result (tier and failures) instead of the
    time-based quality.
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
| tap on target_chef (YUCKY RECIPE) | A gross thing occupies an empty socket, or covers one of her toppings; a blocked socket refuses toppings; one tap on the gross thing flicks it back toward him and emits `hazard_cleared`; a covered topping shows again |
| nursery_quiet (QUIET TIME) | New mode built on the dormant `bop` code (`bop_targets` `scripts/opera_gesture_surface.gd:33`, `set_bop_targets` `:908`, `_bop_press` `:1070`, `_draw_imp` `:5194`, bop demo `:4053`): each target gains a state (arriving, windup, noise, shushed, leaving) and draws its family's pose file; one tap on an arriving or winding-up imp shushes him; three Zzz bubbles; emits `shushed` and `noise` |
| geology_geode (GEODE RACE) | Six purple chip marks on the right half, filled from his units; his sixth unit opens the geode toward him; her five seam taps and 120 px pull are unchanged; a reset clears seams, pull and marks |
| teacher_imp_lesson (IMP'S LESSON) | New mode on `OperaTeacherSurface`: the lesson comes from `TeacherLessonPlan`, plus the imp's silly wrong answer (a silly object in the blank or beside the model for pattern and match; a marked wrong card for count and add) with a purple outline and his pointer mark; her first pick emits `fixed`, `tricked` or `hinted`; golden help follows a wrong pick; every round ends with her placing the right answer; one `record_result(kind, assisted)` per lesson round; a new five-card branch in `choice_rect` (`scripts/opera_teacher_surface.gd:64`) for silly questions |

**Teacher lesson plan:** add `TeacherLessonPlan.imp_answer(lesson) -> int`, which is
deterministic and never returns the correct choice.
- Count and add: the nearest wrong choice. When it is one more than the answer, his pointer
  counts his own nose; when it is one fewer, he skips a pearl while he sneezes (§6.13).
- Pattern and match: -1, because his answer is a silly object, not one of her choices.
- There is no mercy parameter: the game cannot be lost.
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
§6.1 to §6.12 are the costumed careers; the Chef's (§6.1) is a defense contest. §6.13 is the
Teacher's inverted contest, §6.14 the Geologist's race and §6.15 the Nursery's defense
contest.

### 6.1 Chef — YUCKY RECIPE (defense; replaces TOP)

*This applies OD-E's recipe idea by default (§1). If the owner meant the Teacher, the
revision 1 to 4 topping race returns here instead.*

- **Final act:** FROST, then the contest. Both are at `grand_cake_stage`. The phase keeps its
  internal name TOP.
- **Depends on the Chef repair.** The owner has not accepted the Chef's look and pour
  (`ODR-CHEF-VERDICT-20261003`; `MA-OPERA-001` reopened 2026-10-03). Build this contest after
  that repair lands, on the repaired cake: no dark bloom, and no code-drawn duplicate of the
  painted cake. Until then the Chef is not a pilot (§11).
- **Skill:** decorating and keeping food clean. Her cake shows seven glowing sockets
  (`TARGET_ANCHORS.target_chef`) on the borderless cake (`widget_target_chef_mover.png`).
  Each tap on an empty socket places one topping.
- **His mischief:** he stands by the cake stand with a little basket of gross things at his
  feet: a stinky sock, a wiggly worm, a fish skeleton and an old boot.
  - Every 4.0 s while she is active he winds up (`windup`, 0.8 s) with a gross thing in his
    free hand, the fist opposite his whisk. Then he tosses it (`slash`): it leaves his open
    hand and lands on her cake with a small puff.
  - It lands on an empty socket if one is free, otherwise on top of one of her toppings, and
    sits there wiggling. A blocked socket takes no topping.
  - One tap flicks it off. It sails back and bonks him (`stagger`, his hat wobbles), and the
    socket is free again, or her topping shows again.
  - His first toss starts after her first topping. At most once every 6 s he says (new):
    "Special delivery! Yum yum!"
- **She wins** when all seven sockets hold her toppings.
- **He wins** when three gross things sit on the cake at the same moment. That takes several
  ignored tosses while she is active; most children never let it happen. The win beat
  plays, the gross things and her toppings pop off with a soft puff, and the clean cake
  waits (§4.7).
- **Flub:** his third toss goes straight up, and the stinky sock lands on his own chef's
  hat. He staggers, flops (`bopped`, 1.0 s) and recovers, 1.8 s in all. Line: "Flour goes in
  the bowl... or on my head. Either way!"
- **Mercy after two failures:** a toss every 12 s, with a 1.6 s windup (§4.17).
- **What the child sees:** her big cake filling with toppings. Beside the stand, the purple
  chef-imp giggles and lobs a stinky sock onto it. She taps the sock and it sails back and
  bonks his hat.
- **Lines:**
  - his challenge (new `imp_op_chef_challenge`): "Your cake needs my special ingredients!
    Socks and worms! Hee hee!";
  - her instruction (new `roshan_op_chef_contest`): "The imp is putting yucky things on my
    cake! Tap them off and finish the toppings!";
  - his defeat line: "Fine! The cake needed more sugar anyway!"
- **Art:** the gross things come from the shared silly icon set (§6.13). The sock and the
  worm are already among the silly-question pictures; add a fish skeleton and an old boot.
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
  - The first restart keeps his speed. After two failures he runs at half speed (× 0.5).
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

### 6.13 Teacher — IMP'S LESSON (inverted, cannot be lost; inserted after MATCH)

- **Final act:** MATCH, then the contest, both at `lesson_desk` on the same lesson board. New
  `PHASE_STATIONS` entry `"IMP'S LESSON": "lesson_desk"`.
- **Entrance:** when MATCH arms, he runs in and takes his place at the right end of the board
  (§4.11). Line (new): "Hello, class! I'm the new teacher! I know everything! I think." He
  watches her MATCH lesson and bounces (`stagger`, `hop_b`) when she gets it right.
- **Challenge:** he taps the board with his pointer.
  - His line (new): "My turn to be the teacher! Can you catch my silly mistakes?"
  - Her line (new): "The imp is teaching it wrong! Tap the right answer to fix it!"
- **Rounds:** four, every one silly (OD-E): silly question, silly lesson, silly question,
  silly lesson.
  - Each lesson round comes from `TeacherLessonPlan.make_lesson` at her current tier for that
    kind, with his silly wrong answer (§5.5).
  - The first round is always the owner's smell question. After that the silly questions
    and the lesson kinds (pattern, count, add, match) rotate from the total of
    `teacher_learning_progress` rounds, so visits vary without a new save key.
- **His four silly lesson mistakes** (every line new):
  - **Pattern:** the row shows the pattern with its blank. He fills the blank with a silly
    object inside a purple outline, a sock, a banana, a rubber duck or a pizza slice: "Easy
    peasy, lemon squeezy! This one comes next!" She taps the shape card that really comes
    next.
  - **Count:** his pointer counts the pearls silly. When his card is one too many it lands
    on his own nose as the last one; when it is one too few he skips a pearl while he
    sneezes. Then he marks the wrong group card: "One, two, three... eleventy-twelve! It's
    this many!" She touches each pearl herself and hears each number, as in her lesson; the
    answer cards wake only after every pearl is touched. Then she taps the right group.
  - **Add:** he presses the plus himself, the two groups join, and he plonks a banana on his
    wrong total: "Two plus one makes... a banana! No wait. This many!" She counts each
    pearl, then taps the right total.
  - **Match:** he lifts a silly object card, a pizza slice, up beside the model: "Look! These
    two are twins! Same, same, same!" She taps the shape that really matches.
- **Silly questions (OD-D).** Each shows five picture cards in one row, in shuffled
  positions: four that fit and his misfit.
  1. He asks the question, naming the four fitting pictures as each one wiggles.
  2. He proudly picks the misfit (purple outline, `taunt`).
  3. When she taps a fitting picture he tests it (sniffs, listens, stretches up, touches,
     shivers, yawns, squeezes or tastes) with his reaction line and poses.
  4. If she taps his misfit, his tricked line and gloat play; he gets no point. The golden
     sparkle then marks the fitting cards and she taps one to see his reaction.
  5. Either way the round ends with her pearl.

  The fart cloud and the whoopee cushion also play the existing `assets/audio/fart.ogg`.

| He asks | Right answers (any of the four) | His pick and claim | His reaction to a right pick | If she picks his |
|---|---|---|---|---|
| Which smells the worst? Farts, garbage, old diapers, or rotten cheese? | a green fart cloud with stink lines, an overflowing garbage can, an old droopy diaper with stink lines, a moldy wedge of rotten cheese with two cartoon flies | a pretty red rose: "I know! This pretty rose! Pee-yew!" | "Pee-yew! That's so stinky! I'm gonna faint!" | "Hee hee! Tricked you! Roses smell nice!" |
| Which is the loudest? A burp, a big drum, a roaring lion, or a fire truck? | a frog with puffed cheeks mid-burp, a big drum, a roaring lion, a red fire truck with its siren flashing | a teeny tiny mouse: "Easy! This teeny tiny mouse! Squeak!" | "Ow, my ears! That's so loud!" | "Hee hee! Tricked you! Mice are super quiet!" |
| Which is the biggest? A whale, an elephant, a dinosaur, or a castle? | a whale, an elephant, a friendly long-neck dinosaur, a castle | an itty bitty ant: "I know! This itty bitty ant! Look at its muscles!" | "Whoa! That's so big! I feel teeny!" | "Hee hee! Tricked you! Ants are tiny!" |
| Which is the stickiest? Honey, bubble gum, a booger, or slime? | a dripping honey pot, a big pink bubble-gum bubble, a green cartoon booger on a tissue, a blob of green slime | a fluffy feather: "This fluffy feather! It sticks to everything!" | "Eww! My fingers are stuck together!" | "Hee hee! Tricked you! Feathers float away!" |
| Which is the coldest? Ice cream, a snowman, an ice cube, or a penguin? | an ice-cream cone, a snowman, an ice cube, a penguin | the bright hot sun: "Brrr! The sun! It's freezing!" | "Brrr! My toes are frozen!" | "Hee hee! Tricked you! The sun is hot!" |
| Which is the slowest? A snail, a turtle, a sloth, or a slug? | a snail, a turtle, a sleepy sloth, a slug | a zooming rocket: "Zoom! This rocket is soooo slow!" | "Sooo... slooow... Yaaawn!" | "Hee hee! Tricked you! Rockets go zoom!" |
| Which is the squishiest? Jelly, a marshmallow, mud, or a whoopee cushion? | a wobbly jelly, a marshmallow, a mud puddle, a whoopee cushion | a hard grey rock: "This hard rock! Squishy squishy!" | "Squish! So squishy!" | "Hee hee! Tricked you! Rocks are hard!" |
| Which is the yuckiest to eat? A mud pie, a wiggly worm, a stinky sock, or soap? | a mud pie, a wiggly worm, a stinky sock with stink lines, a bar of soap | a pink cupcake: "Yuck! This cupcake!" | "Bleh! Yucky yucky yuck!" | "Hee hee! Tricked you! Cupcakes are yummy!" |

  Reaction poses:
  - smell and yucky: `stagger`, `bopped` (a faint), `recover`;
  - loud and cold: `guard` (covering his ears, or shivering), then `recover`;
  - big: `hop_b` (stretching up), then `stagger`;
  - sticky: `recover` (stuck fingers), then `stagger`;
  - slow: `idle` (a yawn), then `recover`;
  - squishy: `charge` (a squeeze), then `stagger`.

  Silly rounds do not call `record_result`, because they are not `TeacherLessonPlan`
  lessons. Random tapping picks a right answer four times in five, and correct play always
  does (`DL-AGE-05`). They are the laughs; the lesson rounds carry the learning.
- **Scoring:** as §4.15. Every round ends with her pearl, and four pearls win.
  - First pick right: "Oops! You fixed it! My brain is full of bubbles!" (lesson rounds) or
    his reaction line (silly questions).
  - First pick wrong: "Hee hee! Tricked you!" (silly questions use their own tricked line),
    then the golden help and her fix. No point for him.
  - **It cannot be lost (OD-E):** he never scores, so there is no restart and no mercy table.
- **Mastery:** each lesson round calls `TeacherLessonPlan.record_result(kind, assisted)`
  exactly like a lesson. `assisted` is true when her first pick was wrong or she used the
  hint. Silly-question rounds do not call it. The contest counts as practice, and her later
  lessons adapt to it.
- **What the child sees:**
  - her familiar cream board, with the purple imp at its right end in his costume, pointing
    proudly at an answer outlined in purple;
  - she thinks, counts where needed, and taps the real answer;
  - his answer puffs away, the right one glows gold, and he wobbles and rubs his head;
  - her pearl row at the top of the screen fills, one pearl per round.
- **What stays true to the Teacher engine:**
  - time never answers;
  - counting stays one-to-one;
  - a wrong pick still gets immediate golden help;
  - nothing earned is lost;
  - a wrong first pick costs her nothing but his giggle (OD-E).
- **Defeat and curtain:** his defeat line (new) is "You're the real teacher! I'll go sit in
  the silly corner." He bows at the curtain call.
- **H2 is absorbed:** the imp is now visible in the final act, so the win line's "learning
  buddy" no longer credits someone the child never saw.
- **Art:**
  - **Required: the shared silly icon set**, one consistent style:
    - the 40 silly-question pictures, five per question;
    - the silly lesson objects not among them: a banana, a rubber duck and a pizza slice
      (the sock is already there);
    - the Chef's fish skeleton and old boot (§6.1), and the Nursery's trumpet and crashing
      cymbals (§6.15);
    - up to 47 pictures in all.
    - Codex makes them after first checking existing approved art (`DL-PLAN-03`); check
      `assets/props/story/fruit_banana.png` and
      `assets/flats/castle/rooms/room_bubble_bath_item_rubber_duck.png` first.
    - One object per icon, transparent, at most 512 px.
    - Broad pastel fills with navy outlines, to match the lesson board.
    - Cartoon-gross, never realistic: the "farts" card is a green cloud with stink lines,
      and the diaper and the booger stay cartoony.
    - The owner approves the first five (the smell question) before the rest.
  - The lesson rounds need no other new art.
  - **Interim:** the plain mischief imp (`imp_mischief`). He has no `hop_a` or `hop_b`, so his
    entrance is `flee` then `idle`, and his gloat is `taunt` only. Do not use the doctor
    costume that the hidden buddy borrows today: a doctor teaching sums muddles the job.
  - **Recommended:** a new `rival_teacher` family with the same 13 states as the others. His
    costume:
    - round glasses slipping down his nose;
    - a small mortarboard cap tilted over one horn;
    - a cream cardigan with a coral bow tie;
    - a wooden pointer with a star tip as his held prop in every pose;
    - colours from the Teacher board: cream, navy outline, aqua and coral.
  - **How Codex makes it:** under the owner's 2026-10-03 animation-workflow policy in
    `AGENTS.md` (`DL-MOT-14` to `DL-MOT-16`, the
    [production protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md) and its
    [job card](../../../design/templates/ANIMATION_JOB_CARD_V1.md)): set the attempt, time and
    cost caps first, pilot the idle before the other states, prefer Aseprite for cleanup and
    export where practical, and record provenance. Within that policy the existing
    costume-family process applies:
    1. The owner approves the new idle.
    2. Codex generates Sheets A and B, with the identity locked to that idle, in the style of
       `assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md`.
    3. `tools/build_imp_costume_family.py` extracts the states (`--reuse-windup-hop-a`, as the
       other families did).
    4. `tools/build_imp_animation_delivery_manifest.py` records them, and every file gets its
       `ASSET_LICENSES.md` row.

### 6.14 Geologist — GEODE RACE (race; replaces GEODE)

- **Final act:** the contest only, at `crystal_gallery` on the full-screen geology surface.
  `FINALE_START` stays 3, so the imp enters and challenges at once. The phase keeps its
  internal name GEODE.
- **What changes today:** the field-guide imp is a co-op partner beside her from the first
  beat. Under OD-A he now appears only when GEODE arms.
- **The same goal (OD-E):** one geode, two diggers. Whoever opens it first gets the
  crystals.
  - **Her side:** exactly the GEODE she knows. She taps the five yellow seam spots along the
    geode's middle crack (`GEODE_SEAM_SPOTS`, `scripts/opera_geology_surface.gd:36-39`), then
    drags the right half open by 120 px (`GEODE_PULL_DISTANCE`, `:34`). Six units.
  - **His side:** six small purple chip marks drawn inside the right half near its rim, for
    example the geode centre (770, 340) plus (190 cos a, 112 sin a) for a = −60°, −36°,
    −12°, 12°, 36° and 60°. He taps them one by one; each fills solid purple. His sixth chip
    pops the geode open toward him.
- **Where he stands:** at the geode's lower right, about 190 px tall, facing it, clear of her
  seam spots and of the 120 px opening path. Each chip lands on his `slash` contact frame
  with a small chip puff (§4.16).
- **His tool:** the interim field guide wears the detective costume, so he taps each mark
  with the rim of his magnifier, his held prop: a silly tool for the job. The recommended
  `rival_geologist` family brings a small rock hammer.
- **Pace:** 6 units, `base_seconds` 14.0. Tune it in W8; a steady child takes about 8 s.
- **Flub:** at his 3rd chip. His tool slips off the geode and drops on his own toe; he hops
  about holding it (`slash`, `stagger`, `bopped`), 2.0 s in all. Line (new): "Ow! My toe! Who
  put a toe there?"
- **She wins** when her pull opens the geode. The right half slides toward him and gently
  bumps him into his defeat beat, and the crystals (`goal_geologist.svg`, as drawn today)
  sparkle on her side.
- **He wins** when his sixth chip opens it: he hugs the crystals (`taunt`) with the win line.
  Then the halves close with a soft puff, every seam spot and chip mark resets, and both
  start again (§4.7).
- **Mercy after two failures:** `mercy_rate` 0.4 (§4.3).
- **What the child sees:** the big geode in the grotto, her yellow seam spots down its
  middle, and the field-guide imp at its right side tapping purple marks. Two pearl rows at
  the top show who is closer. When she pulls it open, the crystals glitter and the imp gets
  a gentle bonk.
- **Lines** (all new):
  - arrive: "Hello! I'm the field guide! Rocks are my favourite snack!";
  - his challenge: "That geode is mine! Race you to the crystals!";
  - her instruction: "Tap the cracks on your side, then pull it open before the imp does!";
  - his defeat line: "Aww! Can I just look at the sparkly crystals?"
- **After she wins:** the curtain call, where he bows.
- **Art:**
  - **Interim:** `rival_detective`, which already ships as the field guide.
  - **Recommended:** a `rival_geologist` family: a yellow hard hat with a small lamp, a khaki
    vest with pockets, and a small rock hammer as his held prop. Codex makes it through the
    same process as §6.13, after owner approval.
  - The chip marks are code-drawn. No other new art.

### 6.15 Nursery — QUIET TIME (defense; inserted after BEDTIME)

- **Final act:** BEDTIME, then the contest, both at `moon_bed`. New `PHASE_STATIONS` entry
  `"QUIET TIME": "moon_bed"`. `FINALE_START` stays 4.
- **The imps:** the two plain families, `imp_mischief` and `imp_captain`, which no shipping
  phase shows today. Neither has `hop_a` or `hop_b`: the entrance is `flee` then `idle`, and
  the win beat is `taunt` only.
  - When BEDTIME arms, one mischief imp runs in and rests at a clear spot away from Roshan,
    Faron and the card. Line (existing): "I was sent to learn the QUIET. I am bad at quiet."
    He watches her tuck the babies in.
- **Faron stays Roshan's teammate.** She keeps her place beside Roshan. Her lines are
  protected family recordings, so she uses only her existing clips (for example
  `faron_win.ogg` at the end); no new Faron line is made.
- **Where it plays:** the finished BEDTIME crib scene stays open and grows into a large panel
  beside the bed, placed with the `_safer_panel_rect` candidate search. Three cribs read
  large; each imp beside a crib is at least 140 px tall with a touch area of at least
  120 px. Roshan and Faron stay visible beside it. Three sleepy Zzz bubbles float over the
  cribs.
- **Challenge:**
  - his line (new): "Hee hee! Party time! Let's make some noise!";
  - her line (new): "Shh! Tap the noisy imps before they wake the babies!"
- **The wave:** six imps per attempt. The mischief imp who entered comes first; after him,
  captain and mischief imps alternate.
  - Each tiptoes in from the panel's left or right edge (`flee`, flipped to face his way,
    about 1.2 s) and stops beside a crib.
  - He crouches with a mischievous grin and his noisy toy at his hands (`windup`, with the
    existing `fx_telegraph_ring.png` pulsing) for 2.5 s.
  - Unless she shushes him first, he makes his noise (`slash`, the existing
    `fx_telegraph_bang.png` and one gentle sound), giggles (`taunt`) and tiptoes off. The
    noise pops one Zzz bubble.
  - A new imp starts in every 3.0 s; at most two are in the panel at once.
- **Her job:** tap an imp while he tiptoes in or winds up. He freezes and covers his face
  (`guard`), then tiptoes away (`flee`). At most once every 4 s she whispers (new): "Shhh!
  Babies are sleeping!"
- **The noisy toys and their sounds** (existing sounds, at reduced volume; never a startling
  bang; Codex checks each against the all-audio rules):
  - a big drum: `assets/audio/sfx/combat_bonk.wav`;
  - a trumpet: `assets/audio/fart.ogg`, as a rude toot;
  - crashing cymbals: `assets/audio/hop_boing.ogg`;
  - a squeaky rubber duck: `assets/audio/castle/duck_squeak.ogg`.
- **She wins** when the wave is over (six imps shushed, asleep or gone) and at least one
  sleep bubble is left. The babies sleep on, and the last imps tiptoe off yawning.
- **He wins** when three noises pop all three bubbles and the babies sit up awake. The lead
  imp says (new) "Hee hee! Wake-up party! Again, again!" in place of the shared win line.
  Then the babies yawn and lie back down, the bubbles float back, and the imps sneak out to
  try again (§4.7).
- **Flub:** the fourth imp trips over his own toy, falls asleep on the spot snoring softly,
  and floats away (`windup`, then `bopped`, 2.0 s in all); he counts as handled. Line
  (existing): "I tried to be quiet. Sorry! Sorry!"
- **Mercy after two failures:** one imp at a time, a 6.0 s windup, and a wave of four
  (§4.17).
- **Defeat and curtain:** the lead imp plays `stagger`, `bopped`, `recover` with his existing
  bop line, "Sorry! Was that too loud? Was it?". Any imps still in the panel yawn and tiptoe
  off, and Faron's existing `faron_win.ogg` may follow. He bows at the curtain call.
- **What the child sees:** three babies asleep in big cribs, Zzz bubbles floating over them.
  Purple imps tiptoe in with a drum, a trumpet, cymbals or a squeaky duck. She taps each one
  and he freezes, hides his face and tiptoes away. If one gets a noise out, a bubble pops.
- **Code:** a new `nursery_quiet` mode built on the dormant `bop` code (§5.5).
- **Art:** the noisy toys come from the shared silly icon set (§6.13). The big drum is
  already among the silly-question pictures and the rubber duck is shared with the
  Teacher's silly lesson objects; add a trumpet and crashing cymbals.

## 7. Owner decisions

### 7.1 Decided by OD-E (2026-10-04)

- **Teacher:** the inverted IMP'S LESSON, which cannot be lost and is always silly (§6.13).
- **Nursery:** QUIET TIME against the plain imps, with Faron at Roshan's side (§6.15).
- **Geologist:** GEODE RACE for the same geode (§6.14). The revision 2 to 4 FIELD GUIDE
  MIX-UP is retired.
- **Restart scope:** the contest only.
- **Mercy:** the first restart is just a restart; after two failures the imp slows down
  radically (§4.3, §4.4, §4.17, §6.11).
- **Silly scope:** every Teacher round is silly.

### 7.2 Still open

1. **The recipe idea.** Default: the Chef's YUCKY RECIPE (§6.1). Alternative: a silly
   recipe round for the Teacher, with the Chef keeping the topping race.
2. **Imp costumes.** Approve a `rival_teacher` family (recommended) and optionally a
   `rival_geologist` family, or keep the stand-ins: the plain mischief imp and the detective
   costume. The Nursery's plain imps need no costume.
3. **Silly icons.** Approve the style of the first five pictures (the smell question) before
   Codex makes the rest of the shared set.
4. **The Hall stage-long race.** Retire it (recommended), or keep it as a no-loss race beside
   the contest (§4.14).

### 7.3 Chapter 2 story runs

They stay without the imp (C13). The owner may later want Ember-aligned story contests; that
would be separate work.

## 8. What this retires

| Retired | Where | Why |
|---|---|---|
| Detective timed retry, reveal and head-start branch | `scripts/opera_competition.gd:232-249`, `scripts/opera_career_world_2d.gd:3696-3710` and `:4618-4638` | H1; SPARKLE RACE replaces it |
| Stale retry caption and `op_retry` routing | `scripts/opera_career_world_2d.gd:3710` | H1; the clip stays on disk, unrouted |
| Background rival meter before the contest | `scripts/opera_competition.gd:210-236` for contest careers | C1; the imp competes only in the contest |
| "Rival hidden, cannot create a loss" as the final-act contract | `design/01_GAME_DESIGN.md:342-344` | superseded for the contest by `DL-INT-14` |
| Geologist partner beside her from the first beat | `scripts/opera_career_world_2d.gd:1793-1799` | C1; the field guide appears when GEODE arms (§6.14) |
| Nursery team finale as its final-act result | `scripts/opera_competition.gd:263-267` for the Nursery | QUIET TIME can be lost and restarted; Faron stays a teammate (§6.15) |
| Hall stage-long race (if the owner agrees) | `_performance_rival_work` | §4.14 |
| Crumb pay on misses inside a contest | `_miss_pay()` under `contest_mode` | C12 |
| Prewarming the plain crew families outside the Nursery | `_prewarm_imp_textures` | H7 |

**Designs retired by revision 5.** Do not build these from earlier revisions of this
packet:
- the Chef's TOPPING RACE (revisions 1 to 4); it returns only if the owner moves the recipe
  idea to the Teacher (§7.2);
- the Geologist's FIELD GUIDE MIX-UP (revisions 2 to 4);
- the Nursery's option B QUIET TUCK-IN race (revisions 1 to 4);
- imp points in the Teacher's game (revisions 2 to 4);
- the progressive rematch mercy of revisions 1 to 4 (0.8 per rematch, +1 point per
  rematch).

## 9. Tests

### 9.1 New probe: `scripts/probe_opera_imp_contest.gd`

Add it to `scripts/ci.sh` and to the probe workflow's trusted list. For every specified
career it checks:

1. **C1:** before the final act, the imp is not visible, no mirror station exists and no
   contest row shows.
2. **Entrance:** it completes within 3 s of the final act arming. Its poses run `flee`,
   `hop_a`, `hop_b`, `idle` (plain imps: `flee`, `idle`), and input is accepted throughout.
3. **C8, passive:** with the contest open and zero input for 60 s, his units stay 0, no
   hazard lands or sounds, and no `imp_won` or `player_won` fires.
4. **Idle pause:** after one touch followed by silence, his units stop growing within 4.1 s
   and resume on the next touch.
5. **Fast child:** a scripted fast child wins the first attempt. The defeat poses run
   `stagger`, `bopped`, `recover`; the tier follows §4.8; the flourish or curtain follows.
6. **Slow child:** a scripted slow but active child loses. Then:
   - `imp_won` fires once, and her input is ignored during the win beat;
   - within 2.2 s both rows are 0, her activity is open and accepting input, and she has not
     moved;
   - earlier phases are still complete; stars, pearls and the save are unchanged;
   - after the first loss his pace is unchanged; after the second loss the radical mercy
     applies (race rate 0.4; points target +3 with half-speed cues; a third of the Chef's
     tosses; one Nursery imp at a time with a 6.0 s windup and a wave of four; the Racer at
     half speed) and stays for every later attempt; a resume resets it.
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

**The inverted Teacher contest** replaces checks 4, 6 and 7, and adds:

14. **No clock:** with a round open and zero input for 60 s, nothing happens.
15. **Truth last (C15):**
    - his marked answer is never the correct choice;
    - every round ends with the correct answer placed by her;
    - a wrong first pick gives him no point; his gloat and the golden help follow at once,
      and the round still ends with her pearl.
16. **Hint:** a hinted round still ends with her placing the right answer and her pearl, and
    a lesson round is recorded as assisted.
17. **Cannot be lost (OD-E):** across scripted attempts with every first pick wrong, he never
    scores, `imp_won` never fires, the contest never restarts, his row never shows, and four
    rounds always end in her win.
18. **Teacher lessons:**
    - rounds run silly question, silly lesson, silly question, silly lesson;
    - lesson rounds rotate pattern, count, add and match at her current tier per kind, each
      with its silly mistake (a silly object for pattern and match, the nose or sneeze count,
      the banana total);
    - count and add answers stay locked until every pearl is touched;
    - each lesson round writes `record_result` with the right `assisted` flag;
    - ordinary lessons from `make_lesson` are unchanged.
19. **Silly questions:**
    - each shows exactly five cards: four fitting and his misfit;
    - a fitting first pick plays his reaction; his misfit plays his gloat; every round ends
      with her pearl;
    - the question line names the four fitting pictures while each wiggles;
    - the reaction poses and any fart sound play for the picked card;
    - the first round is the smell question;
    - silly rounds never call `record_result`.
20. **Humor rule:** no imp line names or teases the child (a text check over the new line
    list).

**Defense contests** (Chef, Nursery) replace check 4, and add:

21. **Telegraph (C16):** every hazard shows its `windup` for at least 0.8 s (Chef) or 2.5 s
    (Nursery) before it lands or sounds.
22. **Idle hold:** after one touch then silence, only hazards whose telegraph ends within
    4 s of that touch complete; then nothing lands or sounds until her next touch. In the
    Nursery an imp may still arrive, but none counts down.
23. **One tap:** one tap removes one hazard. A blocked socket refuses toppings, and a covered
    topping shows again when cleared.
24. **His win:** three hazards counting against her at once fire `imp_won` once; the reset
    clears hazards and toppings, or restores the three bubbles.
25. **Gentle sound:** each Nursery noise plays one of the listed existing sounds at reduced
    volume, within the all-audio rules.

**The Geologist's race** uses checks 1 to 13, plus:

26. **One geode:** her seam spots and pull and his chip marks belong to one geode; her pull
    or his sixth chip opens it, never both; a reset closes it and clears every mark; his
    tool touches each chip mark on his `slash` frame in captures.

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
- `scripts/probe_opera_2d.gd`, Teacher, Geologist and Nursery:
  - "teacher keeps the borrowed doctor buddy hidden through its lesson finale"
    (`:1246-1248`) becomes "hidden before the final act, visible from MATCH";
  - the Geologist's "care partner beside Roshan from the first beat" (`:403-406`) becomes
    "hidden before GEODE";
  - the Nursery keeps Faron "beside Roshan from the first beat" (`:403-406`), even though
    its contest is no longer cooperative, and adds "no imp before BEDTIME";
  - "nursery curtain call records cooperative care" (`:1264-1266`) becomes "records
    Faron's teamwork and the QUIET TIME result".
- `scripts/probe_save_recovery.gd`: Teacher and Geologist checkpoints restore the contest
  phase with an empty mechanic snapshot.

### 9.3 Gates

Run the full trusted suite (`scripts/ci.sh`) green on CI for the work branch, plus the two
audit tools in `CLAUDE.md`. Green probes do not establish owner, device or child acceptance.

## 10. Governance

**Already in this handoff change:**
- `DL-INT-14`, added to design/06 as the target contract, and amended by each revision
  (revision 5: OD-E);
- pointer sentences on `DL-INT-08`, `DL-INT-09` and `DL-INT-10`;
- the amended "Competition is scoped" bullet and pointers on the Geologist and Nursery
  bullets in `design/01_GAME_DESIGN.md`;
- notes in the master index and in the master-audit planning entry;
- ledger rows for this packet.

**Codex's implementation change must also:**
- update the phase counts in `DL-INT-07`, `DL-QA-12`, `design/01_GAME_DESIGN.md` and
  `design/00_MASTER_INDEX.md` together (H8);
- add `ASSET_LICENSES.md` rows and all-audio ledger rows for the new voice files;
- carry an audit-impact record naming `DL-INT-14`, the updated rules, and evidence per rule;
- rewrite the "Geologist is cooperative" and Nursery bullets in `design/01_GAME_DESIGN.md`
  when the contests land;
- add `ASSET_LICENSES.md` rows for the shared silly icon set, and delivery-manifest entries
  for any `rival_teacher` or `rival_geologist` family the owner approves;
- report implementation, machine verification, and outstanding visual, device, child and
  owner acceptance separately.

## 11. Work order

| Step | Work | Gate |
|---|---|---|
| W0 | Owner answers §7.2 (defaults apply if unanswered) | none |
| W1 | `OperaImpContest` logic class (race, points, defense and inverted archetypes, the mercy table), save key, opt-out, and the new probe's logic checks | probe logic green |
| W2 | Shared presentation: entrance, presence, rows, mirror station, rematch, defeat, tier | Detective pilot green |
| W3 | Pilot contests, one per archetype: Detective (race; retires H1), Magician (points; fixes H9) and Nursery QUIET TIME (defense, on the plain imps) | pilots green; owner plays them on the phone |
| W4 | Surface contracts: multi-turn twirl, multi-pass trace, lob, paint mirror, tap then hold, gross-thing hazards on the cake, geode chip marks | focused probes green |
| W5 | Remaining contests: Ballerina, Candymaker, Doctor, Farmer, Painter, Astronaut, Pop Star, Geologist GEODE RACE, and Chef YUCKY RECIPE once the Chef repair has landed | full suite green |
| W6 | Specialists: Boxer points and Racer finish | boxing and racer probes green |
| W6b | Teacher IMP'S LESSON, piloted with the owner's smell question as soon as its five icons are approved, then the other silly questions and silly lessons | inverted checks 14 to 20 green; owner plays the Teacher contest |
| W7 | New voice lines through the filler pipeline, ledger rows and licences; the shared silly icon set; any approved `rival_teacher` or `rival_geologist` family | voice and imp-art probes green |
| W8 | Balance probe fix and tuning (`base_seconds`, hazard timings), then the count and canon updates (H4, H8) | full suite green; merge to `dev` |

## 12. Acceptance

Report four things separately:

1. **Implementation:** what changed, file by file.
2. **Machine verification:** the new and updated probes, the full suite, and the two audit
   tools.
3. **Visual, device and child checks** (outstanding until done):
   - Mobile captures at two supported aspects;
   - the target phone;
   - an observed child session: can she tell who is winning, does she want the rematch,
     does an imp win upset her, and does the slowdown after two failures let her win;
   - for the Teacher: does she understand that she is correcting the imp, does a wrong pick
     stay funny rather than upsetting, and does she still answer her ordinary lessons
     correctly afterwards (no mistakes learned from him);
   - for the silly questions and the gross things: does she laugh, and does the gross humor
     stay fun rather than upsetting;
   - for the Nursery: can she see each imp coming in time, and are the noises gentle enough;
   - the owner playing each pilot.
4. **Owner acceptance of the decisions in §7.2.**

Publication of this handoff is not acceptance of any of them.
