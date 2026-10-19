# Feelings with Puff (package FP)

Part of the [learning-sessions work order](README.md). Owner choices:
`ODR-LEARNING-SCOPE-20261018` (build it) and `ODR-GUIDE-VOICE-20261019`
(new narrator voice). Written by Claude; Codex implements, paints the face
cards and generates the voice lines.

## 1. Goal

One learning goal: **name feelings**. In the Grand Puff care encounter she
names how Puff feels when he is sick (sad), hears why (his cold), is asked
what would help (the cleaning she is about to do), and names the change when
he is well (happy). Four feeling words only: happy, sad, scared, angry.

Why here: the learning-value review found that nothing in the game names
feelings, and the 2026-10-17 recast made Puff a friend with a cold, a natural
moment for it. The Head Start framework lists naming her own feelings as a
goal at this age. The picture book shares the same story (pages 24 to 29),
and the [question card](QUESTION_CARD.md) asks the same questions at bedtime,
so the book and the game use one vocabulary.

Off-screen bridge: at bedtime the grown-up asks "How do you feel today?"
(card opening Q). The game never asks for or stores her own feelings.

## 2. Before you start (FP0)

1. **Land the care recast first.** The encounter exists only on local branch
   `codex/grand-puff-care-20261017`, tip
   `e0abe9c9643e44a85c262683c75b6ac1fb04b5e3` (`ee5a9cecd78c27e9897f7c5e2eeb62385506a572`
   CHG-098 plus two dev reconciliations), in the Codex worktree
   `C:/Users/Peter/.codex/worktrees/grand-puff-crash-20261017/mermaid-roshan-reef`.
   On 2026-10-19 it was on no remote branch (`git ls-remote` and
   `git branch -r --contains ee5a9cec` found nothing). Push it, pass its CI
   and integrate it into `dev` normally. Never build FP on the older
   dev encounter.
2. **Keep its contract.** Read `design/GRAND_PUFF_CARE_2026-10-17.md`
   (blob SHA-256 `1bf9d6bbfa39f3b15628f4b431e42380e51a878165520d2783f70a9ca6ffc8a1`
   at `e0abe9c9`). The five attack steps, warning times, counters, three
   saved rounds, rewards, restore path and the `d1_puff_transformation`
   clip stay exactly as they are (`DL-CIN-16`). FP only adds beats before the
   first sneeze and before the clip.
3. **Voice first.** Package VG (README section 6) supplies the new narrator.
   Code and probes may run on the semantic keys before the recordings
   exist, but FP is not complete without the exact recordings (`DL-SND-01`,
   `DL-SND-13`).
4. **Check the story words.** The care branch still lists the retired cues
   `dustboss_angry` and `dustboss_win` ("POOF! The great dust bunny bursts
   into stars!") among the Day One required events. Confirm neither can play
   in the care encounter, so no line calls Puff angry or burst while the game
   is teaching that he feels sad and then happy.

## 3. Player flow, step by step

Existing states on the care branch, for orientation: `splash` → `showing`
(she learns to move) → rounds of `tell` → `strike` → `vuln` → `struck`,
three times → `friends` → win, clip and Day Two. FP adds two choice beats
and one spoken bridge. Each beat is its own state, so probes and the pose
map can see it.

### Beat 1: "How does Grand Puff feel?" (new state, after `showing`, before the first `tell`)

1. The splash and its line play as now ("Grand Puff has a cold. Let's
   help!"), then the `showing` lesson as now ("Touch the floor where you want
   to go!"). When `showing` would start the first sneeze, enter beat 1
   instead. No danger shape is drawn and no sneeze cloud can reach her.
2. Puff holds his sniffly pose (atlas cell 0) and does one harmless
   breath-in and achoo (cells 1 and 2) with no telegraph.
3. The face cards rise into a row in the lower middle of the screen, between
   Roshan and Puff, without covering either face (`DL-READ-05`).
4. The narrator asks the question (lines in section 4) while the pointer
   moves (section 5). At level 0 the question names both choices and the
   pointer touches each card as it is named.
5. She taps a card:
   - **Sad (matching):** the card presses in and glows; Puff sniffles; the
     narrator says "Sad. Grand Puff feels sad. His nose is all stuffy." At
     level 2 the narrator then asks "Why does he feel sad?", waits two
     seconds for her to answer aloud, and says "Because he has a cold."
   - **Another face:** the card wobbles gently (no buzzer, no red, no X);
     the narrator names the face she chose and says how Puff feels instead,
     for example "That's an angry face. Grand Puff isn't angry. He has a
     cold, so he feels sad." The pointer then settles on the sad card. She
     taps it to go on. That pick counts as helped.
   - **No tap for 6 seconds:** the question repeats once. **No tap for 12
     seconds:** help: the pointer settles on the sad card and the narrator
     says "He feels sad. Can you tap the sad face?" Then wait; repeat the
     help at most every 15 seconds, three times, then keep only the silent
     pointer pulse. Nothing advances without her tap (`DL-AGE-04`).
6. **"What would help?"** The narrator asks "What would help Grand Puff
   feel better?", waits two seconds with no choice on screen (room for her
   or a grown-up to answer aloud), then says "Let's wash his dusty coat!"
   The cards sink away, their touch areas are removed, and the first `tell`
   starts exactly as it does today.

### Rounds 1 to 3: unchanged

Same patterns, timings, counters, lines, checkpoints and rewards as the care
branch.

### Beat 3: "How does he feel now?" (new state, after the third clean, before the ending)

1. After the third clean the care branch says "All clean! Feeling better!"
   and Puff takes his grateful pose (cell 3). The rounds are already saved.
2. The cards rise again. The narrator asks "How does Grand Puff feel now?"
   (level 0: "How does Grand Puff feel now? Happy, or sad?").
3. **Happy (matching):** "Happy! Grand Puff feels happy. You helped him feel
   better." At level 2 the narrator adds "Why does he feel happy?", a
   two-second wait, then "Because you helped wash him clean!"
   **Another face:** the face is named kindly and the pointer settles on
   happy, for example "That's a sad face. Grand Puff was sad when he was
   sick. Now he feels happy!" **No tap:** same timing and help as beat 1,
   with "He feels happy. Can you tap the happy face?"
4. **Bridge (spoken, no choice):** "How do you feel today? Tell a grown-up!"
   Nothing is shown, recorded or saved.
5. The cards sink away and the existing ending runs unchanged: the
   `friends` hold, the transformation clip, the win and Day Two.

### Restored and repeat visits

- **Restored checkpoint** (three rounds saved, then the app was closed): the
  care branch shows the healthy pose and says "All clean! Feeling better!",
  then resumes the ending. Beat 3 plays there too, before the clip. It never
  asks her to clean again.
- **Leaving mid-beat** (Back, pause, focus loss): cancel the beat, its audio
  and its touch areas (`DL-UI-05`, `DL-SAVE-03`). Saved rounds are kept.
  Re-entry starts the same beat from its beginning.
- **Replays after completion:** both beats play on every visit, at the
  current level, so practice continues and the level keeps moving.
- Beats add about 20 to 30 seconds to an encounter. Keep every spoken line
  short and touch-skippable (`DL-SND-03`).

## 4. Voice lines

All lines are new synthetic lines in the new narrator voice (package VG).
No family recording is used, changed or imitated (`DL-SND-05`,
`DL-SND-11`). Route them the way the care branch routes its cold lines: as
`OBJECTIVE_GUIDES` entries with mode `dustboss` in
`scripts/audio_director.gd`, files `guide_<key>.ogg` in
`assets/audio/objective_guides/`, and the same required-event treatment.
Each line shows its words as an adult caption (`DL-SND-02`).

| Key | When | Exact line |
|---|---|---|
| `puff_feel_ask_l0` | Beat 1 question, level 0 | Achoo! Grand Puff has a cold. Is he happy, or sad? |
| `puff_feel_ask` | Beat 1 question, levels 1 and 2 | Achoo! Grand Puff has a cold. How does he feel? |
| `puff_feel_sad_yes` | Beat 1, sad tapped | Sad. Grand Puff feels sad. His nose is all stuffy. |
| `puff_feel_not_happy` | Beat 1, happy tapped | That's a happy face. Grand Puff isn't happy right now. He feels sad. |
| `puff_feel_not_angry` | Beat 1, angry tapped | That's an angry face. Grand Puff isn't angry. He has a cold, so he feels sad. |
| `puff_feel_not_scared` | Beat 1, scared tapped | That's a scared face. Grand Puff isn't scared. He has a cold, so he feels sad. |
| `puff_feel_find_sad` | Beat 1 help | He feels sad. Can you tap the sad face? |
| `puff_feel_why_sad` | Beat 1, level 2, after sad | Why does he feel sad? |
| `puff_feel_because_cold` | After the two-second wait | Because he has a cold. |
| `puff_feel_what_helps` | Beat 1, end | What would help Grand Puff feel better? |
| `puff_feel_lets_wash` | After the two-second wait | Let's wash his dusty coat! |
| `puff_feel_now_ask_l0` | Beat 3 question, level 0 | How does Grand Puff feel now? Happy, or sad? |
| `puff_feel_now_ask` | Beat 3 question, levels 1 and 2 | How does Grand Puff feel now? |
| `puff_feel_happy_yes` | Beat 3, happy tapped | Happy! Grand Puff feels happy. You helped him feel better. |
| `puff_feel_not_sad_now` | Beat 3, sad tapped | That's a sad face. Grand Puff was sad when he was sick. Now he feels happy! |
| `puff_feel_not_angry_now` | Beat 3, angry tapped | That's an angry face. Grand Puff isn't angry. He feels happy! |
| `puff_feel_not_scared_now` | Beat 3, scared tapped | That's a scared face. Grand Puff isn't scared. He feels happy! |
| `puff_feel_find_happy` | Beat 3 help | He feels happy. Can you tap the happy face? |
| `puff_feel_why_happy` | Beat 3, level 2, after happy | Why does he feel happy? |
| `puff_feel_because_helped` | After the two-second wait | Because you helped wash him clean! |
| `puff_feel_you` | Beat 3 bridge | How do you feel today? Tell a grown-up! |

Rules for these lines: never say "wrong", "no" or "try again"; always name
the face she chose before naming Puff's feeling; never use speed, score or
"good girl" words. A repeated tap on the same card replays its line at most
once every three seconds and never pays progress (`DL-AGE-05`).

## 5. Visual pointers and staging

- **Pointer:** one reusable helper (`DL-CODE-05`). The game has no shared
  objective-pointer helper yet; its `▼` pointer is still copied file by
  file (`MA-CODE-003`). Build the card pointer as a small helper other
  activities can adopt, never as one more copy; this work need not replace
  the old copies. It always points at a live card (`DL-READ-06`).
  - While a question plays at level 0, it touches each card as its feeling
    is named.
  - At levels 1 and 2, all cards pulse together while she decides, so the
    pointer shows where to choose without giving away the answer.
  - After help starts, it settles on the matching card and pulses there.
  - It starts in the same frame as its line (`DL-SND-13`) and disappears
    with the cards.
- **Face cards:** a row of 2, 3 or 4 large cards, each at least 180 × 180
  base-canvas pixels with 40 pixels or more between them (`DL-UI-03`),
  in the shared Storybook card style: cream shell or paper surface, navy or
  violet outline, a visible pressed state (`DL-UI-06`). Each card holds one
  face and nothing else: no words, letters or numbers (`DL-READ-04`,
  `DL-AGE-01`). Card order rotates by a fixed rule (section 6), never at
  random.
- **Face art (new, Codex):** four faces of the small lavender dust bunny,
  happy, sad, scared and angry, painted to match the game's existing little
  bunny (`assets/sprites/dust_bunnies/dust_bunny_idle.png`, blob SHA-256
  `0be27cef5fc32ada5489da287f4dce0397008d1be0c8d1680229133ddc0539b4`:
  spiral ears with pearl tips, swirl on the head, pearl paws, purple outline,
  big glossy eyes, pink cheeks). Expressions must read at phone size:
  happy, a wide smile and lifted cheeks; sad, a downturned mouth, droopy
  ears and one tear; scared, wide eyes, a small open "o" mouth and ears
  pulled back; angry, lowered brows and a pout, kept mild and cute
  (`DL-AGE-08`). Inventory existing art first (`DL-ASSET-01`); no current
  file shows these feelings, so generate one sheet for that named gap
  (`DL-ASSET-02`): 1024 × 1024, four 512 × 512 cells, the same layout as
  Puff's cold sheet. Record prompt, references, rejects and hashes, and add
  an `ASSET_LICENSES.md` line in the same change. These are bunny faces,
  not Puff, so she judges Puff's situation rather than matching his picture.
- **Puff:** existing cold atlas only
  (`assets/sprites/dust_bunnies/boss/grand_puff_cold_keys_v1.png` on the
  care branch, blob SHA-256
  `6fef220e68dbc2cb4c4cbc0d8cc158c2be601a0209a171c6038b98a745ba527c`):
  sniffly cell 0, breath-in cell 1, achoo cell 2 and grateful cell 3. No new
  Puff art.
- **Feedback:** a valid tap shows a pressed state within two rendered frames
  (`DL-AGE-07`). A matching pick gets a soft warm glow ring and Puff's
  reaction (a sniffle in beat 1, a small happy hop in beat 3). Another face
  gets a gentle side-to-side wobble. Glow, sound and voice describe the same
  event (`DL-MOT-04`). Nothing sparkles before she has chosen.
- **Controls during a beat:** only the cards take touches. World taps do not
  move Roshan, and the action button reads "WAIT", never "CLEAN!"
  (`DL-INT-01`, `DL-UI-04`).

## 6. Steps up and down

The beats keep a small skill level that follows the Teacher's engine
(`scripts/teacher_lesson_plan.gd`, blob SHA-256
`d82e5b7a817335b4da2d0d7b55706a5cde1ff1954c2b33d8ba34d891dac5778e` at dev
`e1dc3e21`): levels 0 to 2 (`MAX_TIER`), up after three clean wins
(`WINS_TO_PROMOTE`). Unlike the Teacher today, it also steps down after
repeated help.

| Level | Cards | Question | Extra |
|---|---|---|---|
| 0 | 2: happy, sad | Names both choices ("Is he happy, or sad?"); the pointer touches each card | none |
| 1 | 3: happy, sad, and scared or angry (alternating by visit) | Does not name the choices | none |
| 2 | 4: happy, sad, scared, angry | Does not name the choices | the "why" question and answer |

- **Clean pick:** her first tap in a beat is the matching card, with no help
  given. Thinking time and the single 6-second repeat are not help.
- **Helped pick:** the matching card is reached only after another face was
  tapped or after the 12-second help.
- **Up:** three clean picks at the current level move it up one, to at most
  2, and reset the counts.
- **Down:** two helped picks in a row move it down one, to at least 0, and
  reset the counts.
- Beat 1 and beat 3 each count as one pick. The bridge counts for nothing.
- The level is invisible: no stars, sounds, words or numbers mark a change.
- **Code:** put the ladder in a new pure satellite,
  `scripts/feelings_lesson_plan.gd`, built like `TeacherLessonPlan`: static
  functions, JSON-safe dictionaries, `normalise_progress()` with safe
  defaults, `record_result(saved, clean, helped)` and `make_choices(level,
  sequence)`. Reuse the Teacher's constants and its fixed choice rotation
  rather than copying them. If that means making the Teacher's
  `_arrange_choices` public, keep the old name working and the Teacher's
  behaviour byte-identical, proven by its existing probe. The Teacher
  itself gains no step-down in this work.
- **Save:** one new key, `feelings_learning_progress`, defaulting to an
  empty dictionary and normalised on load like `teacher_learning_progress`
  (`DL-SAVE-01`, `DL-CODE-03`). It records only level, clean count, help
  streak and number of beats. It never records which face she chose.

## 7. What counts as done, and no fail state

- Beat 1 is done when she taps the sad card; beat 3 when she taps the happy
  card. Either a clean or a helped pick completes the beat.
- The encounter is complete exactly as on the care branch: three cleans,
  saved round by round. Beat 3 comes after those saves, so nothing she
  earned can be lost there.
- Nothing fails. There is no timer, buzzer, lost round, "wrong" word or
  ending early. Every other face is named kindly and the way on stays open
  (`DL-AGE-03`, `DL-INT-05`).
- A child who does nothing never gets past beat 1 and wins nothing
  (`DL-AGE-04`). Help shows the answer but never taps it for her
  (`DL-INT-06`).
- Random tapping is never faster than choosing: other faces only replay
  their naming line and move the pointer (`DL-AGE-05`).

## 8. Files that change

On top of the integrated care branch:

- `scripts/games/dust_boss.gd`: two beat states, entered from `showing`
  (beat 1) and from the third-clean path and the restored-checkpoint path
  (beat 3); `pose_for_state()` for both; `action_label()` returns "WAIT"
  during beats; `stage_close()` clears beat audio, cards and pointer.
- `scripts/feelings_lesson_plan.gd` (new): the pure ladder.
- `scripts/feelings_choice_2d.gd` (new): the face-card row on the attic
  Canvas layer, using the shared Storybook UI and pointer helpers.
- `scripts/audio_director.gd`: the 21 new `OBJECTIVE_GUIDES` keys and their
  required-event entries.
- `scripts/save_state.gd`: the additive `feelings_learning_progress` key.
- `scripts/teacher_lesson_plan.gd`: only if the choice rotation is made
  public, behaviour unchanged.
- `scripts/probe_dust_boss.gd`, `scripts/probe_audio.gd`,
  `scripts/probe_passive.gd`, and `scripts/probe_opera.gd` only if the
  Teacher file changes.
- New art: the face sheet under `assets/sprites/dust_bunnies/` with its
  `.import`, sources under `assets_src/`, and an `ASSET_LICENSES.md` line.
- New audio: 21 files under `assets/audio/objective_guides/`, the guide
  manifest, provenance under `assets_src/audio/`, ledger rows and
  `ASSET_LICENSES.md` lines (package VG).
- `design/GRAND_PUFF_CARE_2026-10-17.md`: a "Feelings beats" section that
  links this file; an impact record and ledger rows for anything new.

Keep new logic out of `scripts/main.gd` (`MA-CODE-001`). Add probe cases to
the existing `probe_dust_boss.gd`, which already runs in both rosters, so no
workflow file has to change.

## 9. Probes and checks (probe-first, `DL-CODE-10`, `DL-QA-02`)

Through real touch input, not by writing state:

1. Zero input: the encounter stops at beat 1; no round, pearl, medal,
   level or completion changes (extend the passive snapshot to
   `feelings_learning_progress`, in the spirit of `MA-CI-005`).
2. Level 0 clean path: tap sad, play three rounds, tap happy; clean count
   +2; the clip and Day Two follow as before.
3. Other face first in each beat: its naming line plays, the pointer
   settles on the matching card, progress waits for that card, and the pick
   counts as helped.
4. Idle: the 6-second repeat, the 12-second help and the capped repeats,
   with no progress until a tap.
5. Ladder: three clean picks go up, two helped picks in a row go down,
   never below 0 or above 2; card counts 2, 3 and 4; fixed rotation.
6. Interruptions: Back, pause and focus loss during each beat cancel audio,
   cards and touch, keep saved rounds, and restart the beat on re-entry.
   The restored three-round checkpoint plays beat 3 before the clip.
7. The original pattern, cadence and Canvas assertions in
   `probe_dust_boss.gd` pass unchanged.
8. Audio: every new key resolves to its file; each line starts within
   150 ms of its trigger with its pointer; nothing plays after teardown
   (`DL-SND-13`).
9. Full `scripts/ci.sh` at exact Godot 4.7.2-stable, then green branch CI
   before integration.

## 10. Acceptance

Report three claims separately: implemented, machine-verified at the named
commit, and still open.

- **Machine:** sections 9.1 to 9.9 pass; document, development and 2D gates
  pass.
- **Visual:** displayed Mobile captures at 1280×720 and a wide phone of both
  beats at every level, showing Puff, Roshan, cards and pointer all visible.
- **Audio:** human review of all 21 lines at 4/5 or better for
  intelligibility and child-safety (`DL-SND-15`); device timing on the
  Lenovo Tab M11 and the older phone (`DL-SND-16`).
- **Owner:** approves the four faces and the lines (`DL-QA-06`).
- **Child, two weeks** (log in [PARENT_LOG.md](PARENT_LOG.md)):
  - Off-screen use: she names a feeling without being asked ("I'm sad like
    Puff"), or answers "How do you feel today?" at bedtime with a feeling
    word.
  - Chooses it again: she goes back to Grand Puff, or asks about him.
  - Frustration: she taps faces at random to get past the beat, turns away
    when the cards appear, or gets upset by the questions. Twice in two
    weeks means the beat is too long or too hard; report it so the level-0
    question can be shortened.
- Child evidence stays private and does not close `MA-CHILD-001`.
