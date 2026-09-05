# Day One playthrough protocol (shared by every run agent)

You are simulating ONE playthrough of "Day One" (stage one) of *Mermaid Roshan:
Reef of Light*, a Godot 4.7.2 touch game for one specific 4-year-old
(non-reader, one finger, short sessions, no fail states, no lost progress).
Repo root: `/home/user/mermaid-roshan-reef`. **There is no Godot binary in this
container**, so you cannot run the game. You "play" by tracing the code path
the child's inputs would take, beat by beat, and you estimate wall-clock time
per beat from the constants, tweens, timers, gesture thresholds, message
durations and voice gaps you find in the code. Every claim must cite
`file:line`. Separate what the code PROVES from what you INFER.

Rules:
- Read-only. Do not edit, create or delete anything under the repo. Do not run
  Godot, do not try to download it. Do not commit.
- Read the whole activity script for the rooms you enter (they are 200–900
  lines each). Do not skim the constants and guess; follow the tick/input
  functions to see what actually advances state, what plays a voice line, what
  shows a pointer, what fires a message and for how long.
- Time model: `show_msg()` banners hold for 5.0 s (`scripts/main.gd:2615`
  comment; `msg_timer`). `_say(speaker, event, min_gap)` plays a recorded
  family voice clip (assets/audio/voices; typical clip 1–3 s; `min_gap` is
  the minimum seconds since the last line, not the clip length). Tweens and
  `create_timer` calls are exact. Gesture activities carry explicit min/max
  seconds. For child input time use the child model below.
- Be honest about uncertainty: if a duration depends on an asset you cannot
  measure (voice clip length, an absent movie), say so and give a range.
- Your report goes to ONE file (path given in your task). Nothing else.

## The child model (use these numbers unless the persona overrides them)

- Age 4, cannot read. Any text-only instruction is invisible to her; only
  voice, pointers (ghost hand / pulsing star), motion, glow and sound count.
- One finger. Taps are ~1.0–1.5 s apart when engaged; ~0.3 s apart when
  excited/spamming; ~50–120 px accuracy on a 1280×720 canvas held at phone
  distance. Drags are wobbly; circles are lumpy ovals; back-and-forth strokes
  are ~180–260 px long.
- Reaction to a new prompt: 1.5–3 s. Reaction to a timed window (boss
  flash): 0.9–1.6 s typical, sometimes 2–4 s.
- Attention: an activity beat that gives her agency holds ~60–120 s. A passive
  span (no input accepted, nothing she caused) reads as "fine" up to ~4 s,
  "restless" 4–8 s, "taps the screen / looks away" beyond ~8–10 s. After a
  prompt, silence with no pointer for >5 s means she taps something else or
  asks an adult. Whole-session interest is ~8–15 min before she wants a
  natural stop; a stop must lose nothing.
- She repeats what worked. If tapping made something happen, she taps it
  again. If a door said no, she tries the same door again 1–2 times.

## Day One flow map (code pointers — verify, do not trust blindly)

State owner: `scripts/day_one_director.gd` (763 lines, RefCounted; ALL state
lives on `ReefMain` in `scripts/main.gd:324-362`). Room order is fixed:
`bathroom → pool → stuffie → art` (`ROOM_ORDER`), then the boss door glows,
then the Grand Puff boss, then Day Two. Save keys are additive; restore is via
`normalise_save_patch()` (director ~line 470) which re-derives the room order.

1. **Start menu** — `scripts/start_menu.gd`. New Game → `_launch_from_start_menu(true)`
   (`main.gd:3966`); Continue derives Day One from the save flag. `START_AT_CASTLE_GATE`
   is `true` (`main.gd:44`) so New Game drops the child straight into Sky Lagoon
   at the ocean-gate hub: `_enter_level2_now(false,false,true)` (`main.gd:5748`).
2. **Sky Lagoon arrival** — `scripts/arena/sky_lagoon_promenade.gd`: `build()` ~line 179,
   the arrival plane `_tick_plane_arrival` ~line 310/500, first-session message at
   ~line 266, castle gate target ~line 556-577, tap-to-enter castle ~line 796-807 and
   ~1029-1036. `_day_one_begin_arrival()` fires from `main.gd:5801`
   (event `arrival_plane_media`; the Grok movie is NOT present — `main.gd:7778`
   just records a request; the in-engine plane animation is the fallback).
3. **Castle main hall, dirty discovery** — `main.gd:6816-6858` `_enter_castle_interior_now`
   → `castle_rooms.open("main_hall")` (`scripts/arena/castle_rooms_25d.gd:907`) →
   `_day_one_discover_dirty_castle()` (`main.gd:7339`) attaches
   `scripts/arena/day_one_castle_dressing.gd` and fires the `grok_video_2` event
   whose only runtime effect is a banner (`main.gd:7783-7786`). Door language:
   `scripts/castle_door_language.gd`, `castle_door_cue.gd`; the one "golden rainbow
   door" is the current room, others are foggy/"resting" (`castle_rooms_25d.gd:1640-1720`,
   `1772-1870` `show_room`). Blocked doors answer with a banner + `_say`
   (`main.gd:7125-7132`, `castle_rooms_25d.gd:1700-1718`). Elevator menu:
   `castle_rooms_25d.gd:1248-1271`, `1565-1770`. Room ids map:
   `DAY_ONE_CASTLE_ROOM_IDS` in main.gd (bubble_bath→bathroom, mermaid_pool→pool,
   playroom→stuffie, craft_room→art).
4. **Bathroom tutorial (bubble_bath)** — entry: `main.gd:7134-7152` →
   `_sync_day_one_bathroom_cleanup()` (`main.gd:7380-7430`). Optional entry movie seam
   `scripts/day_one_bathroom_movie_handoff.gd` (fails open when the movie is absent —
   it is absent; no video files exist in assets). Basket hunt owner:
   `scripts/games/day_one_bathroom_cleanup.gd` (804 lines: one basket tap at
   (940,575), then sponge/brush demo). Gesture owner:
   `scripts/games/day_one_bathroom_cleaning.gd` (870 lines: sink circular scrub —
   arc ≥ 1.05·TAU, distance ≥ 520 px, 2–5 s live motion; then a tub TAP that triggers
   the swimming dust-bunny comic "No!" (`day_one_dust_bunny_swimmer.gd`, 0.68 s) and
   drain, then tub back-and-forth brush — 520 px, 2 reversals, 2–5 s). Completion:
   `main.gd:7231-7252` → cleanup movie seam (absent → fallback) → pool route picture
   button appears at (1035,455) (`main.gd:7530-7605`, banner "Tap the pool picture!").
5. **Pool (mermaid_pool)** — `castle_rooms_25d.gd:1886-1925` mounts
   `scripts/games/day_one_pool_cleanup.gd` (596 lines) which runs three ordered
   one-finger activities: `pool_skimmer_activity.gd` (6 trash, catch radius 118 px,
   basket at (980,560)), `pool_waterfall_activity.gd` (3 lanes, tap-assist 0.22),
   `pool_seahorse_rescue_activity.gd` (8 taps). Then Rumi reveal/wave/idle
   (`day_one_pool_cleanup.gd` ~300-360, timers 0.58/0.42). Completion
   `main.gd:7304-7320`. Progress masks persist on main (`main.gd:7294-7302`).
6. **Stuffie room (playroom)** — `main.gd:7156-7164`: requires
   `stuffie_wins["rescued_eagle"]`. The rescue is inside the castle room itself:
   two pinning dust bunnies, Roshan walks (tap-to-move) to each bunny's contact
   area and bumps it (`castle_rooms_25d.gd:4140-4215` `_check_playroom_rescue_complete`,
   `_add_playroom_rescue_pointer`; walk/route code earlier in that file — search
   `eagle_pin_left`, `_on_room_input`, `walk`, `route`). Then the stuffie picker
   opens (`scripts/companion.gd`, STUFFIE_COMPANIONS.md). Room completion:
   `main.gd:7322-7333` `day_one_complete_stuffie_rescue`. Note that the cleared
   pins live in `m.g["castle_dust_bunnies_cleared"]` (scratch) and only
   `stuffie_wins["rescued_eagle_pin_*"]` persists — check what survives an app kill.
7. **Art room (craft_room)** — `scripts/day_one_art_studio.gd` (438 lines): 4 loose
   materials + 3 counter grime (7 actions), desk unlock, then the attack customizer
   `scripts/attack_customizer.gd` (5 colours, 2 effects, picture confirm) →
   `day_one_complete_art_customization` → `day_one_complete_art_scene`
   (`main.gd:7255-7284`). Room order means `record_art_cleanup` is rejected unless
   `current_room_id == "art"`.
8. **Boss door + Grand Puff** — all four rooms done → `boss_door_glow` →
   `_day_one_arm_boss_door()` (`main.gd:7761`) arms a royal-hall event; triggering it
   closes the castle and `_start_game(dust_boss_fr)` (`main.gd:7794-7798`,
   `dust_boss_fr` at `main.gd:703`). Fight: `scripts/games/dust_boss.gd` (1244 lines;
   constants at lines 55-90: SHOW_T 6.4, WINDUP 0.7, STRUCK 1.8, DIZZY 3.2, ANGRY 2.1,
   PHASE_BEAT 2.8, CELEBRATION 1.8, WIN 3.4, POSITIVE_PACING_FLOOR 38 s, mercy after 5
   missed windows) + `scripts/dust_bunny_boss_sprite.gd` (3 rounds × 3 taps, 0.75 s
   window, 0.65 s final) + `scripts/boss_splash_2d.gd` + `scripts/games/octagon_stage.gd`.
   Find the win → `day_one_complete_boss_and_begin_day_two()` (`main.gd:7075`) call.
9. **Day Two transition** — `scripts/day_two_transition_2d.gd` (4.18 s, exit at 3.70)
   + banner (`main.gd:7086-7108`). Jobs/opera unlock.

Saves: `_write_save()` `main.gd:3949` (synchronous, milestones);
`_queue_save()` `main.gd:3983` (1.5 s debounce). `scripts/save_state.gd` restores
via `DayOneDirector.normalise_save_patch`. Existing probes are useful maps of
intended behaviour: `scripts/probe_day_one_*.gd`, `probe_start_menu_routing.gd`,
`probe_dust_boss_balance.gd`, `probe_stuffie.gd`.

Hard project rules you are grading against (from CLAUDE.md/AGENTS.md):
no fail states; no reading-dependent objectives (every objective must fire a
`_say()` voice line AND a visual pointer); one finger; never lose progress;
touch targets child-sized; sessions short (`DL-AGE-06`).

## Report format (write exactly this structure, markdown)

```
# Run NN — <persona name>
Persona: <2-3 sentences: who she is today, how she plays, what she wants>
Path taken: <one paragraph, in order>

## Beat log
| # | Beat | What she sees | What she hears | Input needed | Est. seconds (min / typical / max) | Evidence | Attention (G/Y/R) |
(one row per beat, from the New Game tap to the Day Two banner or wherever this
persona stops; include waits, banners, demos, transitions, blocked-door
detours, re-entries. Attention: G = engaged, Y = restless, R = likely to
disengage or tap away)

## Time budget
- Total: min / typical / max seconds (and minutes)
- Longest passive span: <beat, seconds, why>
- Longest input-required span with no new feedback: <beat, seconds>
- Natural stopping points that lose nothing: <list>

## Pros (as this player experienced it)
- ...

## Cons / friction (as this player experienced it)
- ...

## Invariant hazards found
| Invariant | Beat | What happens | Evidence | Severity (P1/P2/P3) |
(no-fail, non-reader, one-finger, lost-progress, dead-air/silence, dead-end,
touch-target size, confusing-feedback, other)

## Tuning proposals (max 6, concrete, numeric where possible)
| # | Change | File:line | Current value → proposed | Why it helps a 4-year-old |

## Confidence
- What is proven by code vs inferred; what you could not determine.
```
