# Teacher Learning Engine — implementation and research review

> Historical individual-candidate report on base `775ceee1`. For the combined candidate reconciled onto `8aab459c` and current validation status, see [Opera reconciliation](OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md#reconciliation-onto-current-dev--2026-09-05). Earlier green probes and typography blockers below retain their original scope.

**Review date:** 2026-09-05
**Status:** local candidate for integration; not committed or integrated. The
full Opera 2D exact-Godot-4.7.2 run is currently green for 15 careers and 61
phases, with final route, save, voice, living-world, and Nursery regressions recorded below. Device audio listening and child observation remain open. This document is an implementation
review and design recommendation, not a child-study approval.

## Provisional quality score: 3.5 / 5

The candidate has a useful four-skill structure, deterministic progression,
saveable mastery, a child-readable Teacher actor, and a concrete visual board.
It is much closer to a coherent learning activity than a collection of
minigame prompts. The score stays provisional because no child or device
listening session has yet verified the speech, first-touch timing, counter
legibility, or phone-scale target sizes. The current pattern mechanic only asks
for the next item, there is no parent lesson selector, and learners currently revisit the four lessons in a fixed sequence. Those are product
limits rather than engine failures.

## Four mechanics and their current model

The source of truth is `scripts/teacher_lesson_plan.gd`. It exposes four kinds:
`pattern`, `count`, `add`, and `match` (`:7`). Every kind has tiers 0–2 and
promotes after three clean, unassisted successes (`MAX_TIER := 2`,
`WINS_TO_PROMOTE := 3`, `:8-9`). Assisted retries remain encouraging and do
not consume a fail state.

| Skill | Tier 0 | Tier 1 | Tier 2 | Touch loop and review |
|---|---|---|---|---|
| Pattern | `A B A B`, two choices | `A A B A A B`, three choices | `A B C A B C`, three choices | Teacher points to the empty next slot, the child taps the completing shape, and the board celebrates the completed row. This is a clear introduction, but it tests continuation only; it does not yet ask the child to build, copy in a new location, or explain a pattern. |
| Count | Quantity 1–3, two choices | Quantity 1–5, three choices | Quantity 1–10, three choices | Teacher highlights one pearl at a time, then the child chooses the group with the same quantity. Each pearl registers once and stays visibly marked; wrong choices preserve the counted set. The current quantity ceilings are explicit at `:112-120`. |
| Add | `1+1` or `1+2`, total ≤3 | `1+2`, `1+3`, `2+2`, or `2+3`, total ≤5 | Pairs from `2+3` through `5+5`, total ≤10 | Tapping the plus combines two separate colored groups into a countable arrangement over 0.4 seconds. The child touches each pearl in the joined group and chooses the matching total. The data already carries `operands` (`:125-143`); the renderer keeps both addends visible until the child deliberately joins them. |
| Match | Two choices | Three choices | Four choices | A displayed shape is the model; the child taps the identical shape card. The five data symbols are circle, triangle, square, star, and heart (`:11-15`). Later work should vary size and orientation so matching is about shape identity rather than pixel position. |

The lesson generator rotates the target and distractor order by sequence, which
prevents the correct answer from living in one fixed slot. `record_result()`
increments rounds and only increments clean successes when `assisted` is false;
three clean wins promote that skill independently. `teacher_learning_progress`
stores each skill's tier, rounds, and clean-success count. Helped answers advance
the question sequence without earning mastery. A separate `teacher_lesson_checkpoint`
stores the current phase, joined state, touched pearls, and assistance status.
Writes are coalesced with a one-second retry interval, with immediate flushes at
phase completion, exit, application pause, and focus loss. Existing save keys and
slots remain intact; new Teacher is slot 17, while 4/9/14 stay retired.

## Mechanic-by-mechanic assessment

Scores are subjective implementation reviews, not measured learning outcomes.

| Lesson | Score / 5 | Strength | Limitation | Specific next improvement |
|---|---:|---|---|---|
| Pattern | 3.5 | Large consistent symbols; AB starts with two choices; scan points through the sequence. | Every pattern currently ends at the first element of its repeating unit. | Add different stopping points, then copying and building patterns after child testing. |
| Count | 3.5 | One-to-one touches, spoken numbers, stable five-column groups; no double count. | Fixed spatial groupings can encourage picture matching; marked pearls cannot yet replay their number. | Add an optional recount gesture and varied arrangements once cardinality is comfortable. |
| Add | 3.5 | A deliberate join makes addition visible; begins at 1+1; the child counts the result. | Does not yet teach splitting a number or counting on; no story problem variants. | Add sharing/splitting stories and alternative combinations of the same total. |
| Match | 3.0 | The easiest success path; same shape and color with generous cards. | Color also identifies the answer; size/orientation reasoning remains shallow. | Introduce controlled size and orientation changes, then same-color distractors. |

## Introduction, tutorial, and timing contract

Teacher launches from the Library picture route. A pulsing desk invites a
single tap; reaching it opens the lesson. Speech and visual guidance work
without reading. A small reading-aid panel sits above the board so the shared
bottom dialogue box cannot cover choices or numerals.

The implemented timings are:

- Welcome speech: 1.58 seconds. Lesson prompts range from about 0.99 seconds
  for matching to 3.95 seconds for counting. There is no separate tutorial movie.
- Addition join: 0.4 seconds, then individual counters become active.
- Correct-answer picture hold: 2.2 seconds using the shared Opera transition.
- Wrong choices: immediate golden help, a 0.4-second feedback pulse, no penalty.
- Idle help: the existing nine-second reminder offers a pointer. Help marks the
  result assisted and never taps an answer or awards progress on its own.
- Counting is child-paced. Each unique touch highlights a pearl and queues its
  spoken number. A bounded FIFO retains fast taps in order on the shared voice
  channel, followed by the choose-total prompt. New lesson prompts clear stale
  queued cues; exit stops dialogue. Speech duration does not gate success.

A suggested device-test target is 15–35 seconds per introductory question,
with no enforced clock. That target is a design hypothesis, not a measured
session length. Listen for number intelligibility, whether very quick touches
outrun the spoken sequence, and whether idle help arrives too soon for thought.

## Art and scene assembly

The approved Teacher actor remains unchanged at
`assets/opera/worlds/actors/animation/roshan_teacher_sheet_a.png`. Its 4x4
atlas provides idle, travel, pointer/work, and cheer rows, with complete tails
and fins and a consistent aqua/lavender/coral costume. Learning symbols stay
outside the actor as required by
`assets_src/imagegen/teacher_roshan_2026-09-03/GAME_SEED.md`.

The scene reuses the existing Library background tile family:
`assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c0.png`
through `r1_c3.png`, with the existing background-only logical plate and its
native 2K source. The eight tiles give the lesson a calm storybook room with a
large open central floor. The lesson uses the background-only room and a single desk hotspot; it does not add duplicate painted furniture.

The new board asset is the small true-2D SVG
`assets/opera/worlds/hotspots/teacher_lesson_board.svg`. Its cream board,
navy outline, aqua circles, coral/gold triangle, and lavender counters match
the existing Opera language. The SVG is the discoverable desk hotspot. The opened board uses shared Canvas shape functions for prompt tokens and answer cards, so no generated symbol can drift between questions. Broad fills and navy outlines keep the educational symbols distinct from the detailed room.

The 17 new isolated OGGs live under `assets/audio/teacher/`; they do not touch
`assets/audio/voices/` or protected family recordings. The requested lines are:

- `roshan_teacher_start`: “Let's play with shapes and pearls!”
- `teacher_pattern`: “What comes next? Tap the shape that finishes the pattern.”
- `teacher_count`: “Touch each pearl, one at a time. Then find the group with the same number.”
- `teacher_add`: “Put the two groups together. Touch each pearl to count them all.”
- `teacher_match`: “Find the same shape.”
- `teacher_choose`: “How many altogether? Tap the matching group.”
- `teacher_help`: “Look at the golden sparkle. You can try again.”
- `teacher_number_1` through `teacher_number_10`: “One.” through “Ten.”

`teacher_number_1` was rechecked after generation because the short-program
ebur128 analyzer returned its −70 LUFS sentinel and decoded the first pass at
an unsafe peak. A bounded postpass brought it to zero clipped samples, −10.2
dBTP, and −17.35 dBFS RMS; this limitation is recorded in the manifest.

## Research basis and limits

Head Start's official preschool math progression describes 36–48-month
children beginning one-to-one counting in small groups, recognizing small
sets, filling a missing element in a simple pattern with adult help, and
beginning very small addition with adult support. Its 48–60-month progression
adds joining objects for addition, extending simple patterns, and associating
written numerals with quantities. See [Head Start Math Preschool](https://headstart.gov/school-readiness/article/math-preschool).

Head Start's curriculum guidance recommends an organized sequence that moves
from identifying the next item in a simple pattern to copying, extending, and
creating patterns, while adapting experiences to different developmental
levels. See [Head Start Curriculum Scope and Sequence](https://headstart.gov/publication/curriculum-scope-sequence).

NAEYC's early mathematics position statement describes a progression from
non-verbal addition of very low numbers toward counting-on when totals stay
within 10, and from matching basic shapes in the same orientation toward
matching shapes that vary in size or orientation. It recommends objects,
fingers, counting on, guessing, and checking. See [NAEYC Early Childhood Mathematics](https://www.naeyc.org/positionstatements/mathematics).

NAEYC's number-composition guidance frames early addition through concrete
objects and joining/separating stories before more formal number problems. See
[Playing Around with Number Composition](https://www.naeyc.org/resources/pubs/tyc/spring2022/number-composition).

These sources support the proposed progression and concrete materials. They do
not establish that every four-year-old will master every tier on the same day,
nor do they validate this game's timing, speech intelligibility, or touch
targets. Those are design hypotheses requiring child observation and device
listening.

## Specific limitations and next review gates

The current pattern model ends at selecting the next item. A stronger later
tier would let the child copy an AB pattern into a new location, then create a
short pattern with teacher guidance, matching the progression described by Head
Start. The current match model also needs a tested orientation/size variation
before it can claim shape reasoning beyond visual sameness.

There is no parent lesson selector yet. The engine presents all four kinds in order; a future parent control could offer a simple picture choice to replay counting, pattern, add, or
match without navigating a reading-heavy menu. That selector should write no
new save semantics beyond selecting the current skill.

The current join, counting, touch, and save behavior is implemented and covered
by connected probes. Real phone listening, a child session, and sustained
30-fps testing on the Lenovo Tab M11 remain required before final acceptance.
The new lesson is a true 2D Canvas scene; the wider project's existing 3D debt
is still open and is not solved by this addition.

## Validation and delivery record

The exact Godot 4.7.2 Mobile renderer captured Library entry, all four
introductory lessons, tier-2 previews, separate and joined addition, wide
layout, and finale. These are deterministic diagnostic previews; the higher
tiers were deliberately set for inspection and are not evidence of child-earned
progress. The final answer-card geometry and numeral visibility were visually
inspected. No original Teacher or Library image was changed.

Full `scripts/ci.sh` currently stops on two inherited typography fixtures:
`stale glyph allowlist entries: U+2019` and a stale exact-line expectation at
`scripts/games/dust_boss.gd:1118`. These failures also occur at the starting
`origin/dev` baseline `775ceee1`; no typography test, glyph allowlist, or dust-boss
source was changed. The branch is therefore a local review candidate, not
committed, pushed, or merged into `dev`. No APK was published.

The game-wide 2D regression gate reports `NO_REGRESSION`, with 56 existing
production 3D files and zero model files. Its strict status remains
`UNSATISFIED`. This result is not a complete 2D migration claim.

Exact commands, focused regression outcomes, capture hashes, and the portable
change bundle are recorded in `tmp/teacher-engine/` alongside this candidate.

### Final focused checks

All six checks ran sequentially with separate disposable user-data profiles
under exact Godot 4.7.2-stable, and each returned exit 0 / ALL OK:

| Probe | Result and coverage |
|---|---|
| `probe_opera.gd` | Library routes, raw viewport touch entry, reward and return paths. |
| `probe_save_recovery.gd` | Legacy compatibility, new bit 17, normalized Teacher progress/checkpoints, recovery. |
| `probe_voice.gd` | Existing shared voice channel, fallback, cooldown and queue regressions. |
| `probe_living_world.gd` | Exact 100-stage catalog including Teacher; bounded idle and no passive rewards. |
| `probe_opera_nursery.gd` | Existing cooperative Nursery remains intact. |
| `probe_opera_2d.gd` | 15 careers / 61 phases; Teacher's four real-touch lessons, tiers, assistance, duplicate/cancel/restore guards, 17 exact voice events, number FIFO, and hidden doctor through finale. |

Changed GDScript parser, inference lint, whitespace check, and document-authority
gate pass. The audio manifest independently records successful decoding and
zero clipped samples in all 17 files. A second Sol review found no actionable
issue in mastery resume, final checkpoint clearing, slot bounds, or voice
serialization. These checks do not substitute for a child or target-device test.

The portable review bundle contains the binary Git patch, final changed/new
files, asset provenance, test logs, and Mobile-render screenshots, plus SHA-256
hashes. It excludes probe saves, user profiles, protected originals, and
import-cache churn. Apply it only against its declared base in a separate work
branch; Racer and Geologist candidates remain separate worktrees.
