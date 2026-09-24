# Codex handoff — Day One rebuild and the Grand Puff finale (2026-09-23)

**Status: DRAFT for owner review.** Publication is not approval. Nothing here
authorizes new art, new voice recordings, lifecycle changes or a boss redesign
until the owner answers the decisions in [Owner decisions](#owner-decisions).
The document is subordinate to the canonical audit
(`audit/MASTER_AUDIT_2026-08-09.md`), the design language
(`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`) and owner decisions. It
re-baselines, but does not delete, the 2026-09-02 handoff
(`CODEX_DAY_ONE_PLAYER_EXPERIENCE_HANDOFF_2026-09-02.md`); its `DO-*` statuses
are carried in [Appendix D](#appendix-d--status-of-the-2026-09-02-do-findings).

| | |
|---|---|
| Code baseline | `dev` `7cb2c399` (2026-09-23). Line anchors are at this commit; `main.gd` anchors are approximate (±5 lines) and move after the reef removal, so resolve them by symbol. |
| Landing on top | `claude/remove-3d-reef-20260923` (3D reef removed; `scripts/main.gd` shrinks by ~2,100 lines, so resolve `main.gd` anchors by symbol) and `claude/day-one-continue-fix-20260923` (WP-R0 below). |
| Author | Claude review session for the owner, 2026-09-23 |
| Recipient | Codex, working in this repository on a `codex/*` branch per `CLAUDE.md`/`AGENTS.md` |
| Scope | Day One end to end: start menu → Sky Lagoon → Main Hall → Bathroom → Pool → Playroom → Art Room → Royal Hall → Grand Puff → Day Two card |

## Contents

- [Mission](#mission)
- [Evidence levels](#evidence-levels)
- [Owner decisions](#owner-decisions)
- [Day One as she plays it today](#day-one-as-she-plays-it-today)
- [Parts, focal goals and feedback](#parts-focal-goals-and-feedback)
- [Findings register](#findings-register)
- [Grand Puff: pacing, timing and fun](#grand-puff-pacing-timing-and-fun)
- [Art: regenerate, repair, restage](#art-regenerate-repair-restage)
- [Voice, pointer and touch contract](#voice-pointer-and-touch-contract)
- [Target architecture](#target-architecture)
- [Work packages](#work-packages)
- [Order, escalation and reporting](#order-escalation-and-reporting)
- Appendices: [A persona runs](#appendix-a--measured-grand-puff-persona-runs) ·
  [B voice script](#appendix-b--voice-script-for-the-rebuild) ·
  [C parameters](#appendix-c--grand-puff-parameters-current-to-proposed) ·
  [D DO status](#appendix-d--status-of-the-2026-09-02-do-findings) ·
  [E Continue reproduction](#appendix-e--continue-soft-lock-reproduction)

## Mission

Rebuild Day One so a four-year-old non-reader can play it from New Game to the
Day Two card, alone, in short sittings, without getting stuck:

1. **Every required action is spoken and pointed at** (`DL-AGE-01`), including
   the way out of each room and back to the next door.
2. **Resume is exact.** Continue lands in the same live room with its activity
   mounted, whatever moment the app was closed at (`DL-SAVE-04`).
3. **One touch grammar.** Tap, circle-scrub and swipe only; no double taps,
   select-then-confirm or precision timing (`DL-AGE-02`, `DL-UI-01`).
4. **Grand Puff is a warm, funny finale that every child finishes**, with a
   help ladder that never plays for her (`DL-AGE-03`, `DL-AGE-04`,
   `DL-AGE-05`) and an ending where he becomes a friend.
5. **Day One has one owner in code**: a data-driven Day One mode replacing the
   seven castle entry paths and the ~40 `day_one_*` helpers in `main.gd`
   (`DL-CODE-01`, `DL-CODE-02`, `DL-CODE-03`).

## Evidence levels

- **[R]** reproduced at runtime in this review with exact Godot 4.7.2
  (scripts and logs named in the item).
- **[V]** read in code at `7cb2c399`; the consequential ones were re-read
  directly by the author.
- **[E]** estimate or model (timings for a typical child, simulations, pixel
  sizes). Treat as hypotheses to measure.

Nothing here is device, child or owner acceptance. `MA-CHILD-001`,
`MA-PLAY-001` and `MA-AUDIO-001` stay open until that evidence exists.

## Owner decisions

Codex must not start a package marked with an OD until the owner answers it.
Recommended defaults are in bold.

| ID | Decision | Options | Blocks |
|---|---|---|---|
| OD-1 | Grand Puff direction | A: polish only · **B: Hop → Sneeze → Roll → Big Tickle, after A's fixes** · C: no dodging, cleanup only | WP-R5 |
| OD-2 | New voice lines (~25, see Appendix B) | **Provisional synthetic `filler_v1` lines through the existing Parler pipeline, owner-reviewed** · family recordings (never synthetic imitation, `DL-SND-05`) · both | WP-R2, WP-R5 |
| OD-3 | New Grand Puff art | **Commission a "friend" pose sheet and four missing loops (idle breath, hop, not-yet giggle, dizzy) from the locked design; sign the design lock first** · keep the implode ending | WP-R5, WP-R6 |
| OD-4 | Friend picker eagle | **Show the protected book eagle in the picker without a paint palette** · approve a paintable derivative of the book art | WP-R6 |
| OD-5 | Android Back | **Back never quits; at the Day One root it opens Pause** · keep the engine default (quits) | WP-R8 |
| OD-6 | App loses focus during Grand Puff | **Pause the fight in place** · keep today's abort-to-hall | WP-R8 |
| OD-7 | Toilet step (second circle scrub, owner request 2026-09-09) | **Keep, with its own spoken line** · replace with a different verb | WP-R3 |
| OD-8 | A natural break | **Offer a gentle "come back later" moment after the Pool** · no break | WP-R2 |
| OD-9 | Where Day Two starts | Sky Lagoon (today) · Main Hall | WP-R7 |

### Owner answers (2026-09-23)

The owner answered part of the follow-up discussion and set the story direction:

- **Story clips between scenes (`DL-CIN-16`).** Day One now plays 13 straight-cut clips from the owner-selected 2026-09-20 cut between gameplay scenes:
  - the 30-second opening that introduces the game;
  - first room arrivals and room completions;
  - the all-rooms-clean rainbow route;
  - Grand Puff's arrival, his transformation and the epilogue.

  The runtime is `scripts/day_one_story_clips.gd`, built by `tools/build_day_one_story_clips.py` and guarded by `scripts/probe_day_one_story_clips.gd`. This fills the story gaps in the beat map below: the arrival, Rumi rising, Baby Eagle's rescue and the Grand Puff ending.
- **Grand Puff canon.** He is a friend trapped under a big layer of dirt that made him grumpy and scary. Roshan faces him alone and still beats him in play. Daddy, Rumi and Baby Eagle join only in the transformation clip, where the rainbow dust bunny jumps out of the dusty shell. He stays whole instead of imploding, which addresses D1R-12.
- **The rainbow dust bunny then follows Roshan like Baby Eagle.** This is new follower work; its art is the remaining Grand Puff art need from OD-3.
- **OD-1 stays open for the fight's gameplay.** Whichever option is chosen, the fight ends with the transformation clip and the family appears only there.
- OD-2 and OD-4 to OD-9 remain open.

## Day One as she plays it today

Times are **[E]** for an attentive (A) and a slow (S) child; they come from code
constants plus the 2026-09-02 child model (1.5–3 s to react, taps 1–1.5 s
apart). Voice codes: **E** exact line heard; **E✂** line cut off within 1 s by
the next line; **D** dropped because Roshan is already speaking; **M** words do
not match the task; **G** generic line or pitched "Yay!".

| # | Beat | A/S s | Voice | Pointer | Anchor |
|---|---|---|---|---|---|
| 0 | Start menu: gold ★ NEW GAME (hold-gated) or Continue | 6/15 | — | gold button | `start_menu.gd` |
| 1 | Sky Lagoon: tap the castle door | 3/10 | **G**: `roshan_day1_castle` has no clip, so a pitched yay plays | ring on door | `sky_lagoon_promenade.gd:278-288` |
| 2 | Main Hall, first visit: tap the golden Bathroom door | 8/20 | E✂ then D then E | gold arch; no hand | `castle_rooms_25d.gd:1057-1059` |
| 3 | Bathroom: tap the basket | 5/10 | E (never repeated) | ghost hand | `day_one_bathroom_cleanup.gd:767-806` |
| 4 | Sink: circle-scrub | 6/20 | E, silent reminders | hand demo | `day_one_bathroom_cleaning.gd:403-429` |
| 5 | Tub: tap, then brush back and forth; the bunny's "NO!" is text only | 10/28 | E, E✂ | hand, ring | `day_one_bathroom_cleaning.gd:779-849` |
| 6 | Toilet: circle-scrub within 145 px | 7/20 | reuses the sink line | orbiting hand | `day_one_bathroom_toilet.gd:155-229` |
| 7 | Room sparkles 0.92 s and saves (each room) | 2 | "Sparkling" E✂, then the next-room line; "Back to the hall…" D (text only) | none | `day_one_bathroom_cleaning.gd:909-930`; `main.gd:7723-7745` |
| H | **Leave a room (×4)**: find ↩ top-left, then the next golden door | 10/45 | **M** every time | nothing on ↩ | `main.gd:8089-8107`; `castle_rooms_25d.gd:1926-1928` |
| 8 | Pool: skim 6 pieces of trash | 15/43 | E✂ chain | demo hand | `day_one_pool_cleanup.gd:333-356` |
| 9 | Waterfall (3 swipes) and seahorse (8 taps anywhere) | 18/45 | E; completions E✂ | chevrons; none | `pool_seahorse_rescue_activity.gd:211-220` |
| 10 | Rumi rises and waves | 5 | E✂ then E | none | `day_one_pool_cleanup.gd:524-573` |
| 11 | Playroom: bump two dust bunnies off Baby Eagle | 7/17 | E | 53 px star on the eagle, not the bunnies | `castle_rooms_25d.gd:4732-4928` |
| 12 | Friend picker: part → colour → ♥ | 15/40 | **G**/D | gold frame | `companion.gd:627-730` |
| 13 | Art Room: tap 4 supplies | 11/23 | E for the first only | 👇 emoji | `day_one_art_studio.gd:279-305` |
| 14 | Three "scrubs" that are single taps | 6/20 | **M** | 👇 | `day_one_art_studio.gd:321-333,461-479` |
| 15 | Desk → attack-colour picker → ✦ | 13/32 | D, **M** | 👇 on ✦ | `attack_customizer.gd:103-134` |
| 16 | Back to the hall, tap the Royal Hall door | — | **M**; the "all rooms clean" line is unreachable | gold arch | `main.gd:7659-7675` |
| 17 | Grand Puff | 35/70+ | see below | trail, star | `games/dust_boss.gd` |
| 18 | Back to the Sky Lagoon + 4.18 s Day Two card | 6 | G cut, then E | card | `main.gd:7539-7580` |

**Totals [E]:** 4–6 minutes attentive, 11–15 minutes slow. Leaving rooms costs
~40 s attentive and ~180 s slow, and with no adult it can go on indefinitely,
because nothing speaks about or points at ↩. About 65 lines play before the
boss; roughly 18 are cut off within a second and about 7 are dropped.

**Spoken-instruction coverage [V]:** an exact, audible instruction plays at
46% of the moments where she must act (16.5 of 36 scored beats): arrival and
hall 30%, bathroom 75%, pool 75%, playroom 10%, art room 15%, boss 92%.

## Parts, focal goals and feedback

For each part: what it is for, the feedback the child must get, and what the
owner should watch for in a playtest. "Pass" is the observable signal that the
part works without an adult.

| Part | Focal goal | Child-facing feedback it needs | Watch in a playtest | Pass |
|---|---|---|---|---|
| Start menu | Start or resume safely | Spoken "Keep playing?" (today a pitched yay, `start_menu.gd:301`) | Does she press Continue on her own? Does Continue put her back where she was? | She resumes into a live room within 3 s |
| Sky Lagoon | "We're here — go to the castle" | Spoken instruction, pulsing door, walk sound | Does she tap the door first try? | Castle entered in ≤10 s with no adult |
| Main Hall | Learn "follow the golden door" | Line on every entry that matches the castle's state; hand on the golden door; edge arrow if it is off-screen | After each room, does she find the next door? Does the roving prop highlight distract her? | Next door found in ≤20 s every time |
| Bathroom | First success at cleaning; learn tap, circle, swipe | Verb sound per stroke, step chime, praise that is not cut off | Can her real circles fit the 145 px toilet area? Does she stall between steps? | Room done in ≤90 s with ≤1 reminder per step |
| Pool | Variety and meeting Rumi | Room brightens per action (exists); seahorse must need the seahorse | Does she tap the seahorse or just anywhere? Is Rumi's reveal visible behind Roshan? | Each activity started without help |
| Playroom | A rescue that becomes a friendship | Pointer on the bunnies; "Poof!" per bunny; picker lines that name the choice | Does she understand the eagle is trapped? Does she close the picker by accident? | Eagle adopted in ≤60 s |
| Art Room | Tidy up, then make something that matters later | Lines that match the task; say the colour is for Grand Puff | Does "scrub" mean anything here? Does the chosen colour appear later? | Colour chosen and recognised at the boss |
| Royal Hall | The big door: anticipation | "The big royal door is glowing!" with a hand | Does she go straight to it? | Found in ≤15 s |
| Grand Puff | A funny, winnable finale | Wind-up, dodge whoosh, tickle giggle, visible shrinking, befriending | Does she understand "swim out of the purple"? Does she ever get stuck? | Finishes; laughs; ≤2 bumps per attack on average |
| Day Two card | Closure and a new day | One message, the characters she met | Does she know the day is over? | She moves on without asking an adult |

## Findings register

`D1R-*` IDs are handoff-local, not canonical `MA-*` findings. Severity: P0
blocks promotion; P1 strands or confuses the child; P2 weakens the experience;
P3 polish.

| ID | Sev | Ev | Finding | Anchor | WP |
|---|---|---|---|---|---|
| D1R-01 | P0 | R | Continue on a Day One save made after the first castle entry opens the castle with an empty world ID; the empty-world watchdog re-resumes the room **every frame** and the room activity never mounts (dark, rebuilding room, no basket). Dev-only: introduced by `940e4f0e` + `7f49f14e`; master `ff68f955` predates both. | `main.gd` `_launch_from_start_menu`, `_day_one_reorient_after_exit_now`, `_process` watchdog | R0 (landed) |
| D1R-02 | P1 | R | Grand Puff has **no guaranteed progress** after the one-time lessons. Measured: a child who needs 3.5 s to start dodging is bumped 58 times in 5 minutes and never finishes; one who needs 6 s to tap the star never finishes. | `games/dust_boss.gd:392-394,523-532`; `encounter_profile_2d.gd` | R4 |
| D1R-03 | P1 | V | A bump **or** a missed star restarts the whole round from its first attack (`begin_phase` resets `step_index = 0`), so cleared work is replayed. | `encounter_patterns_2d.gd:25-35`; `boss_encounter_2d.gd:40-46` | R4 |
| D1R-04 | P1 | V | Rooms are left through an unspoken, unpointed ↩; the caption "Back to the hall, then follow the glowing door!" is paired with a clip saying something else and is often dropped. Every return to the hall says "This castle is so dusty!"; the boss door is never announced. | `main.gd:8089-8107`; `castle_rooms_25d.gd:1926-1928` | R2 |
| D1R-05 | P1 | V | Voice lines are cut or dropped depending on the call path: Day One cues stop the current line (`audio_director.gd:165`), generic `_say` drops a new line while the same speaker talks (`:284-285`). Reminders use once-per-session dedupe and are silent (`:140-148`). | `audio_director.gd` | R2 |
| D1R-06 | P1 | V | Android Back uses the engine default and probably quits the app; nothing flushes the save on Back. | `project.godot` (no `quit_on_go_back`); `touch_ui.gd:656` | R8 (OD-5) |
| D1R-07 | P1 | V | Focus loss, pause or close aborts the Grand Puff fight back to the hall (rounds kept, current round and splash replayed); conflicts with `DL-SAVE-02`. | `main.gd:4539-4564,8414-8439` | R8 (OD-6) |
| D1R-08 | P2 | V | `roshan_day1_castle` (arrival instruction) has no clip; a pitched "Yay!" plays instead. | `audio_director.gd:314-319` | R2 |
| D1R-09 | P2 | V | Seahorse: 8 taps **anywhere** complete it, so random tapping is as fast as intentional play (`DL-AGE-05`). | `pool_seahorse_rescue_activity.gd:211-220` | R3 |
| D1R-10 | P2 | V | Picker: a tap on the dim margin closes it; its step lines are generic; the picker shows a washed-out bird because `assets/mg/bird_line.png` is an empty 8×8 image [R], while the reward is the book eagle. | `companion.gd:619-637,674-686` | R3, R6 |
| D1R-11 | P2 | V | Art room: completion lines sound like new instructions; "scrubs" are single taps; emoji pointers (👇) carry objectives (`DL-TYPE-07`, `MA-TYPE-004`); the colour's purpose is never said. | `day_one_art_studio.gd:411-479` | R2, R3 |
| D1R-12 | P2 | V | Grand Puff ending: the implode animation hides his sprite (`sprite.visible = false`) and no befriending moment exists. | `dust_bunny_boss_sprite.gd:397-401` | R5 |
| D1R-13 | P2 | V | Tapping Grand Puff during an attack steers Roshan to the floor behind his cutout (deliberate, `dust_boss.gd:597-608`), the opposite of the Day One "touch a dust bunny to pop it" rule. | `dust_boss.gd:597-632` | R4 |
| D1R-14 | P2 | V | The lane attack is never taught; it starts the instant the circle lands; a lane bump replays the circle. | `encounter_patterns_2d.gd:143-164`; `dust_boss.gd:455-467` | R4 |
| D1R-15 | P2 | V | Music re-seeks on every warning and again when the star opens if it drifted (`_sync_music_for_state`, `_on_vulnerability_changed`); the reviewer expects an audible double downbeat each round — confirm by ear. | `dust_boss.gd:341-363` | R4 |
| D1R-16 | P2 | V | The dash lesson adds a 4.6 s hold after the first tickle and teaches a precise double tap (≤0.36 s, ≤64 px) the fight never needs (`DL-AGE-02`). | `dust_boss.gd:534-548,609-615` | R4 |
| D1R-17 | P2 | R | Mashing is as fast as intentional play: the moving-masher persona wins in 30.3 s vs 31.4 s attentive (194 taps). | Appendix A | R4 |
| D1R-18 | P2 | V | The balance probe's negative controls pass trivially (they never leave the "showing" step) and its personas steer with the stick and action button, not touch. | `probe_dust_boss_balance.gd:49-96` | R1 |
| D1R-19 | P2 | V | Room-entry flavour lines contradict what she sees (for example "wiggly-blue" for a dirty pool); praise is cut 0–0.5 s in. | `castle_rooms_25d.gd:1917-1925`; pool/bath praise | R2 |
| D1R-20 | P3 | V | Every loaded save is normalized to `day_one_active = true`, so the "legacy Continue" branch cannot happen and its probe tests a shape that never occurs. | `save_state.gd:514-524`; `start_menu.gd:24-26` | R7 |
| D1R-21 | P3 | V | The friend adoption can be skipped (margin tap closes the picker; the Craft Room door opens after the rescue). | `companion.gd:635-637`; `day_one_director.gd:400-403` | R3 |
| D1R-22 | P3 | V | Continue into a later room still plays the Main Hall entry line. | `main.gd` `_enter_castle_interior_now` | R2 |
| D1R-23 | P2 | V | Structure: `main.gd` 11,910 lines/569 functions with 41 `day_one*` functions at `7cb2c399`; `castle_rooms_25d.gd` 5,731 lines with 196 `day_one` references; 11 Day One scripts total 5,310 lines; seven different paths open the castle; progress is split across director fields, `save_data` keys, `g` scratch and `db_*` keys. | see [Target architecture](#target-architecture) | R7 |

## Grand Puff: pacing, timing and fun

**Is dodging required? Yes [V][R].** Each round's gold-star opening only
follows an attack that misses Roshan; a hit loops to a new attack
(`boss_encounter_2d.gd` `resolve_impact`). The first-ever dodge waits until she
leaves the shape, so it cannot be failed, but it still needs her to move.
Dodging means touching the floor outside the glowing shape (tap-to-travel); a
double tap dashes. Standing still or only tapping never completes a round.

### How the fight runs today

The fight has three rounds with three hit points (`HP = 3`):
- **Round 1:** one hop onto a circle, radius 5.2, 2.35 s warning.
- **Round 2:** two circles at 2.2 s each.
- **Round 3:** a circle at 2.2 s, then a lane (half-width 4.4) at 2.7 s.

After each attack she avoids, a gold star opens for a tap:
- 8.0 s the first time, then 3.2 s, plus 0.45 s per miss up to +2.4 s.
- Failures lengthen warnings by 0.18 s each, capped at +0.9 s.
- A bump costs 1.05 s of recovery.

Round 3 animations run 1.25× faster.

| Timeline [E] | Attentive | Struggling |
|---|---|---|
| Splash (input blocked) | 3.2 s | 3.2 s |
| Splash to win / to end of Day Two card | 35 / 39 s | 69 / 73 s |
| Share of time waiting on her decision | 38% | 63% |
| Longest dead stretch inside the fight | 4.6 s (the dash-lesson hold) | 4.6 s |
| Ending: implode + card (input blocked) | 7.6 s | 7.6 s |

**Measured [R]** with the repository's balance probe and slower variants (exact
Godot 4.7.2, live encounter clocks, Appendix A): attentive 31 s, learning
34 s, slow 40 s, slow-to-tap 63 s. At a 3.0 s dodge reaction she finishes in
102 s with 4 bumps. **At 3.5 s or 4.0 s she never finishes** (58 bumps in 300
s). At a 5 s star delay she finishes in 103 s. **At 6 s she never finishes**
(21 misses, still round 1 after 300 s).

### Timing analysis

- **Travel is not the limit [V][E].** The circle locks where she stood when the
  warning began; escaping takes ~0.2 s at full speed. Noticing and deciding is
  the limit.
- **Latest safe start [E]:** 2.80 s (round 1), 2.65 s (round 2), 2.48 s
  (circle, round 3), 3.02 s (lane), plus at most 0.9 s of assist. The first
  ~35% of each warning is the swirl travelling to her, leaving ~1.7–2.1 s after
  it arrives. A typical four-year-old needs ~1.2–2 s to see, choose and point,
  and 3 s or more when tired: fine when attentive, failing when tired.
- **A miss costs a whole round [V]:** replaying ~6 s of dodging for one late tap
  is the main pacing penalty for a slow child.
- **The help runs out [V][R]:** the "wait for her" hold only exists before the
  dodge lesson is saved (permanently); both assists are capped. Past the caps
  the fight can loop forever (D1R-02).

### Fun scorecard (reviewer judgement, 1–5)

| Criterion | Score | Why |
|---|---|---|
| One clear rule | 2 | Move away, then tap toward him, plus an optional dash; tapping him means different things at different moments |
| Agency | 3 | Always steerable, but outcomes are pass/fail |
| Variety across rounds | 2 | Hop, two hops, hop + lane — the same idea three times |
| Escalation | 2 | Warnings shrink 2.35 → 2.2 s; "speedy" is faster animation |
| Spectacle | 2.5 | Nice swirl and flashes, but he is a single still frame during warnings (`dust_bunny_boss_sprite.gd:32-37`) |
| Success feedback | 3 | Reaction frames and her chosen attack effect; a successful dodge is silent |
| Bump feedback | 2 | A boing and a once-per-visit line while he still sits on her |
| Humour and character | 2.5 | Charming laugh/dizzy art; he never reacts to her |
| Ending | 1.5 | He vanishes; no befriending |
| Length fit | 3 / 1.5 | ~35 s is right; a struggling child has no upper limit |
| **Overall** | **≈2.3** | |

### Recommended redesign (OD-1 option B): Hop → Sneeze → Roll → Big Tickle

Keep the locked Grand Puff identity, the locked-shape warnings, no-damage saves
and the aim → lock → launch warning language
(`design/BOSS_SPLASH_DESIGN_LANGUAGE.md`). One spoken rule every round:
**"Swim out of the purple, then tickle his star!"**

| Round | New idea | What she does | Art |
|---|---|---|---|
| Intro | "It's Grand Puff! He's SO dusty!" + first-move lesson, re-prompted after 6 s idle | Move | existing |
| 1 Hop | One hop; the warning waits the first time until she is out | Swim out; tickle (star stays open the first time) | existing jump/laugh/flinch |
| 2 Sneeze | He sneezes 3 mini dust bunnies ≥8 units away; she pops them by tap or by swimming into them (the Day One rule), then dodges one hop | Pop ×3, swim out, tickle | existing small dust-bunny sprites |
| 3 Roll | He rolls along a lane; the first roll waits for her with a sideways bubble pointer; then a quick hop; the finale star needs 3 tickles (existing 3-step reaction) | Swim sideways, swim out, tickle ×3 | temporary: squashed-ball frame spinning (owner review) |
| Befriend | He shrinks, hops to Roshan, hands over the pearls, giggles when tapped | Optional taps | **new "friend" pose sheet (OD-3)**; temporary: laugh frame at 45% |

He visibly shrinks 100% → 85% → 72% with a dust burst per tickle (hit area
shrinks with him). Proposed parameters are in
[Appendix C](#appendix-c--grand-puff-parameters-current-to-proposed).

**Help ladder** (per visit; never acts for her, `DL-AGE-04`):

| Level | When | Help |
|---|---|---|
| 0 | default | normal timing |
| 1 | after 1 failure on an attack | +0.5 s, bubble trail to the nearest safe side, instruction repeated |
| 2 | after 2 failures on one attack or 3 in the visit | the warning pauses once it locks until she is outside; ghost hand (`assets/castle/training/ghost_hand.png`) taps outside the shape; Grand Puff wiggles while waiting |
| Star | same ladder | ends with the star staying open and the hand on it |
| Ease off | 2 clean attacks | drop one level |

**Feedback moments:**
- **Wind-up** while the warning flashes: squash and wiggle.
- **Jump:** stretch at takeoff; on landing, a squash, a 3 px shake, a dust ring and a thump.
- **Dodge:** whoosh, sparkle trail and a "missed me!" giggle.
- **Tickle:** star, sparkle beam and her art-room effect, plus a giggle, a burst and the shrink.
- **Bump:** an "achoo" dust puff on Roshan while he hops ≥8 units away. Never visibly take progress away.

**Alternatives:**
- **A (polish only):** fix D1R-02/03/13–17 and add squash, shrink and a befriending ending. Lowest risk, but still the same idea three times.
- **C (no dodging, cleanup only):** calmest. It becomes a fifth chore with no climax and drops the warning language the owner refined.
- **Helper stuffie:** can be added to A or B at help level 2, but must never move, pop or tickle for her.

### Acceptance tests for the fight

1. **Real negative controls:** run from a save with every lesson learned, so bots reach the attacks. Idle, button-masher, held action, tap-one-spot and movement-only players all complete **0 rounds in 120 s**. Each gets ≤3 bumps before the soft hold, then none.
2. **Random tapping** (2 Hz) finishes, but takes ≥1.3× the attentive time (`DL-AGE-05`).
3. **Real touch:** bots use screen taps on the floor and on Grand Puff, not the stick.
4. **Slow children always finish:** 3.5–4.5 s reactions within 150 s; 6–8 s reactions within 240 s.
5. **No lost work:** after a bump or a miss, no already-cleared attack is replayed, except the single hop after a missed star.
6. **Warnings:** every warning leaves ≥2.9 s to react; the first hop and the first roll wait for her.
7. **Music:** the downbeat lands on the star within 0.08 s, with no backward jump over 0.1 s.
8. **Voice:** no line is cut within 1 s by a less urgent one; every failure gets an instruction.
9. **Taps on Grand Puff:** during an attack, a tap on him moves Roshan to his feet side and dodges the circle.
10. **Saves:** interrupting at any moment resumes the same round and attack. The reward and the Day Two start fire exactly once (keep the `probe_dust_boss.gd` checks).
11. **Captures:** wind-up, shrink, bump and befriending at 1280×720 and 1560×720. Device, child and owner sign-off are reported separately.

## Art: regenerate, repair, restage

**Ground rules:**
- Reuse approved art first (`CLAUDE.md` art direction).
- New textures are ≤1024 px on the longest side or power-of-two (`DL-PERF-04`), and every cutout is RGBA.
- Room plates follow the existing 3640×2048 master split into 4×2 tiles of 910×1024.
- Every new asset gets an `ASSET_LICENSES.md` row.
- Never touch `assets/book/`, `assets/audio/voices/` or `assets/characters/friends/`.
- Rumi is on IP hold: do not regenerate her.
- Regenerating Roshan needs owner approval.

"✓" marks items the author re-measured.

| # | Pri | Action | Asset | Problem → brief | Size |
|---|---|---|---|---|---|
| 1 | High | REGENERATE (OD-3) | new `assets/sprites/dust_bunnies/boss/dust_bunny_boss_friend.png`; retire `implode` | Ending contradicts "friend". Same locked Puff settles, smiles, waves or hugs Roshan, shrinks to a small whole buddy; no vortex or darkness | 1024², 4 cells of 512, shared baseline and pivot |
| 2 | High | REGENERATE + REPAIR (OD-3) | boss sheets | Missing idle breath, hop, "not yet" giggle and dizzy loops; vulnerable-laugh frames 2–3 flatten his spiral ears (the splash uses that frame) | same |
| 3 | High | REGENERATE | `assets/flats/castle/rooms/room_bubble_bath_dirty_day_one.png`, `…_dirty_drained_day_one.png` | ✓ 1024×576 against a 3640×2048 clean plate, misaligned fixtures, basket and towel clutter. Masked inpaint of the approved clean plate (fixtures and floor grime only) | 3640×2048 as 4×2 tiles |
| 4 | High | REGENERATE | `rooms/room_craft_room_front_left/right.png` | Counter cards have holes, torn edges and floating fragments; they are also the cleaning targets | ≤1024 |
| 5 | High | RESTAGE | boss arena | Roshan ~50 px and Grand Puff ~255×150 px on screen, hard alpha and no mipmaps; stage both as Canvas sprites, zoom ~1.5×, enable mipmaps, one target star on his forehead, hide the companion's emoji bubble | import + staging |
| 6 | High | DECISION (OD-4) | `assets/mg/bird_*` picker layers | ✓ `bird_line.png` is an empty 8×8 image, so the picker shows an outline-less tinted bird unlike the reward | derivative files only |
| 7 | Med | REGENERATE + RESTAGE | new `dirty_cleanup_2d/decals/` | Replace code-drawn edge bands, drips, purple tint and 3 px "cracks" (`day_one_castle_dressing.gd`) with painted cobwebs, dust drifts and tarnish | 512² each |
| 8 | Med | REGENERATE | `assets/flats/castle/boss/dusty_attic_arena_2048.png` | ✓ Lanczos upscale of a 1254 px original; also reads as the Art Room re-dressed. True high-resolution original with rafters | ≥2048 original |
| 9 | Med | REGENERATE | `signs/sign_bubble_bath.png`, `sign_mermaid_pool.png` | Emblems hard to read (grey pearls; a generic drop). Tub with bubbles or a duck; a tail or a seahorse | 256², emblem ≥80% |
| 10 | Med | REGENERATE | `day_one_art_studio/grime_{left,desk,right}.png` | Reads as white fog, not paint | 512×~320 |
| 11 | Med | REPAIR | `assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png` (byte-identical to `dust_bunny_clean_bubbles.png`) | ✓ Every bubble rim carries a baked blotchy checkerboard and the interiors are opaque grey; re-matte to clear bubbles | 512² |
| 12 | Med | RESTAGE + small REGENERATE | Sky Lagoon door focus | A flat opaque red arch hides the painted door; red also clashes with the gold "go here" colour indoors. Warm-gold painted glow fitted to the door | ≤512 |
| 13 | Med | RESTAGE | pointers, door highlights, stray glyphs | Use `ghost_hand` everywhere; fit highlights to the arches; remove the pale pennant/fan glyphs (source node unidentified); dim non-Day-One doors | — |
| 14 | Med | RESTAGE | Pool actors | Roshan stands on the water with a floor shadow; use swim frames with a waterline; stand Rumi beside her for the reveal | — |
| 15 | Med | REPAIR | `magic_cleaning_brush.png` | Split into base + tintable feather mask so the chosen colour shows | 936×1024 |
| 16 | Low | REGENERATE or retire | `playroom_shelf_sailboat_rest.png` and sheet; front bins | ✓ 49×45 broken rest card; stray fragments | ≤1024 |
| 17 | Low | REGENERATE | older 256-px object sheets | Soft beside the high-resolution plates; redo when those rooms are touched | 2048×1024 or 1024² |
| 18 | Low | REPAIR | `assets/ui/boot_splash_mermaid_roshan.png` | 1024×576 stretched 1.25–1.9×; faithful 2× copy of the same picture, tiled | 4 × 1024×576 |
| 19 | Low | RESTAGE | Day Two card | Add Roshan, the befriended Puff and Baby Eagle from existing cutouts; hide the bridge end | reuse only |
| 20 | Low | REPAIR | import settings | Mipmaps for sprites shown below 50%; lossless for Roshan's atlases | — |

**Keep:**
- the Main Hall tiles
- the Pool plate and its activity art
- the Bathroom tools and grime targets
- the dust-bunny family
- `ghost_hand` and the verb chips
- the vortex and dust-puff effects
- Grand Puff's identity
- the castle facade
- the Sky Lagoon (still under owner review)

## Voice, pointer and touch contract

These rules apply to every package that touches Day One.

1. **One voice queue** with priorities: instruction > praise > flavour.
   - Praise is never cut before ~90% of its length; the next instruction waits for it.
   - Reminders use a separate path that bypasses dedupe, capped at 3 per step.
   - No objective uses the generic `talk` line or the pitched yay.
   - Ducking reaches −14 dB within 250 ms (`DL-SND-14`).
2. **Idle ladder, the same everywhere:**
   - 0 s: voice + hand.
   - 5 s: repeat the instruction.
   - 12 s: demonstrate on the target.
   - 25 s: gentle assist that points and waits.

   It never completes the task.
3. **One pointer:** the painted ghost hand, demonstrating the verb. No emoji or text-glyph pointers (`DL-TYPE-07`, `MA-TYPE-004`). Every touch shows a ripple within 2 frames.
4. **Touch grammar:**
   - Only tap, circle-scrub (one shared recognizer) and swipe.
   - No double tap or select-then-confirm in Day One.
   - Hit areas ≥128×128 px (waterfall lanes and customizer buttons measure ~54–104 px today [E]).
   - Targets must be the thing itself: the seahorse, not anywhere.
5. **Room exits:** on completion, a spoken line + a hand on ↩ + a ↩ pulse.
   - On return to the hall: "Let's find the next golden door!", a hand on the door, and an edge arrow when it is off-screen.
   - Announce the boss door.
   - Back always means one press to the hall.
6. **Truthful lines:** every line matches what she sees and what she must do next (D1R-19, D1R-22).

## Target architecture

The aim is `DL-CODE-01`–`DL-CODE-03` and `DL-CODE-07`, in the Mode Platform
shape of `design/07`/`design/08` (Day One is scheduled there as M6/WP-C6).

1. **`DayOneMode`** owns progression, resume, lifecycle and its save namespace.
   - One `resume_from_save()` replaces the seven castle entry paths: `_launch_from_start_menu`, `_day_one_reorient_after_exit_now` plus the watchdog, `_return_day_one_boss_to_castle`, `_tick_castle_rooms` reopening, the two promenade entries and `_show_day_two_transition`.
   - It sets the world, builds the room once and shows it once.
   - The watchdog becomes a one-shot assertion.
2. **A const step table:** arrival, bathroom, pool, rescue, adoption (its own step), art, boss, Day Two.
   - Each row carries room, activity, checkpoint fields, voice and pointer cue, and resume policy.
   - Add a `day_one_step` key with a default and keep writing every legacy key (`DL-SAVE-01`). Derive the step for old saves.
3. **Activities as children of the mode** with one contract: `setup` / `teardown` / `progress` / `completed`.
   - Durable checkpoints (boss rounds, pins, adoption) go through the mode's serializer, never only `m.g` (`DL-CODE-03`, `MA-SAVE-001`).
   - `castle_rooms_25d.gd` becomes a renderer with a typed door/spawn API; the `m.call("...")` strings go away.
4. **Save discipline:**
   - Write at every checkpoint.
   - Flush on focus, pause, close and Back.
   - "Already happened" is decided from saved state; event handlers never navigate.
5. **Lifecycle** (after OD-5/OD-6): `quit_on_go_back = false`; Back at the Day One root opens Pause; focus-out pauses Grand Puff.

## Work packages

Each package lands on its own `codex/*` branch with a `design/audit_impacts/*.json`
record, both document gates, `scripts/ci.sh` and a green remote Probe Suite
before `dev` (`CLAUDE.md`). Every package keeps save keys, protected assets,
true-2D Canvas staging (`DL-MED-01`) and the Mobile renderer.

| WP | Scope | Acceptance (machine) | Gate |
|---|---|---|---|
| **R0** | Continue soft-lock hotfix (D1R-01) | `probe_load` Day One Continue + empty-world convergence legs, negative-controlled | **Landed by Claude** on `claude/day-one-continue-fix-20260923`; integrates after its remote Probe Suite |
| **R1** | Test oracle first | New trusted probes in both rosters:<br>• **Continue matrix:** one on-disk save per resume state (bathroom sub-steps, pool, Rumi, pins, picker, art, customizer, boss door, mid-fight) → real Continue → live room, non-empty world, no rebuild storm, pointer + voice, one action progresses.<br>• **Lifecycle matrix:** focus/pause/close/Back at each state.<br>• **Idle Day One:** every room, picker, customizer and boss earn nothing (`MA-CI-005`).<br>• **Display golden path:** real touches on visible pointers only (`MA-PLAY-001`, `DL-QA-02`).<br>• **Real boss negative controls** (fight test 1). | none |
| R2 | Voice scheduler + spoken routing | Probe asserts the clip playing at each beat, 5 s/12 s reminders audible, praise ≥90% played, no `talk`/yay objective, room exits spoken with the hand on ↩, hall line matches castle state | OD-2, OD-8 |
| R3 | Touch grammar, pointer, idle ladder | Hit areas ≥128 px; random-tap probe never faster than intent; seahorse needs the seahorse; picker margin cannot dismiss adoption; one circle recognizer | OD-7 |
| R4 | Grand Puff A-fixes (D1R-02, 03, 13–17) | Fight tests 1–10 with today's rounds | none |
| R5 | Grand Puff redesign B | Fight tests 1–11; ≤2.2 s of dead time between her actions outside the splash | OD-1, OD-2, OD-3 |
| R6 | Art queue (table above, by priority) | Import/texture/license gates; captures at 1280×720 and 1560×720; owner review of each generated asset | OD-3, OD-4 and per-asset owner review |
| R7 | `DayOneMode` migration | All R1 probes green before and after; `day_one*` in `main.gd` reduced to ≤10 thin forwards; `castle_rooms_25d.gd` Day One blocks moved into activities; `DL-CODE-12` ratchet armed | OD-9 |
| R8 | Lifecycle | Back never quits; focus-out pauses the fight in place; lifecycle matrix green | OD-5, OD-6 |

## Order, escalation and reporting

**Order.**
1. R0 (landed).
2. R1.
3. R2, R3 and R4 in parallel.
4. R7, after R1 is green and before large content changes.
5. R5 and R6 as owner decisions arrive.
6. R8 once OD-5 and OD-6 are answered.

Do not promote `dev` to `master` while R0 is unintegrated.

**Stop and ask the owner when:**
- A change would remove or rename a save key.
- A change touches protected art or voices.
- It would add a 3D node or resource.
- It would weaken a probe instead of fixing behaviour.
- It needs a new voice recording or generated art without the matching OD.
- It changes the story canon: Baby Eagle is trapped under two dust bunnies; Grand Puff becomes a friend.
- It would lengthen Day One beyond ~6 minutes for an attentive child.

**Report per package:**
- Implementation (files, commits).
- Machine verification: exact probe names and results, and the negative control that failed before the change.
- Outstanding visual, device, child and owner acceptance, reported separately (`CLAUDE.md` contract).

## Appendix A — measured Grand Puff persona runs

Exact Godot 4.7.2, headless, `scripts/probe_dust_boss_balance.gd` and two
variants with slower personas (time scale 3, cap 300 s), dev `7cb2c399`.
Columns: seconds, rounds won, bumps, avoids, star misses, taps. "reaction" is
seconds into a warning before moving; "counter" is seconds after the star opens
before tapping.

| Persona | reaction / speed / counter | Result |
|---|---|---|
| attentive | 0.45 / 0.85 / 0.6 | 31.4 s, 3 rounds, 0 bumps |
| learning | 1.15 / 0.65 / 1.2 | 34.2 s, 0 bumps |
| slow | 2.0 / 0.4 / 2.4 | 39.7 s, 0 bumps |
| slow_counter | 1.0 / 0.6 / 4.0 | 62.9 s, 2 misses |
| moving_masher | 0.9 / 0.7 / mash | 30.3 s, 194 taps |
| tired | 2.6 / 0.45 / 3.0 | 56.6 s, 3 bumps |
| very_slow | 3.0 / 0.4 / 4.5 | 102.4 s, 4 bumps, 3 misses |
| slow_tapper_5_0 | 1.2 / 0.6 / 5.0 | 103.4 s, 5 misses |
| **slow_dodger_3_5** | 3.5 / 0.4 / 2.0 | **300 s cap, 1 round, 58 bumps — never finishes** |
| **slow_dodger_4_0** | 4.0 / 0.4 / 2.0 | **300 s cap, 1 round, 58 bumps — never finishes** |
| **very_slow_tapper** | 2.2 / 0.5 / 6.0 | **300 s cap, 1 round, 21 misses — never finishes** |
| controls: idle, stationary masher, held action | — | 0 rounds in 60 s (they never leave "showing") |
| control: movement only | 0.6 / 0.8 / never | 0 rounds, 5 avoids, 4 misses |

## Appendix B — voice script for the rebuild

Lines are ≤8 words.

**Status codes:**
- **E:** exists and exact.
- **W:** exists; needs wiring or timing.
- **N:** new provisional line (OD-2).
- **F:** family recording only.

| When | Speaker | Line | Status |
|---|---|---|---|
| Lagoon arrival | Roshan | "Let's walk to the castle!" (`d1_c01_s03_roshan_walk_castle`, unused) | W |
| Gate idle | Roshan | "Tap the big castle door!" | N |
| Hall, first entry | Roshan | "Oh! This castle is so dusty!" | W (let it finish) |
| Golden door | Roshan | "Follow the golden rainbow door!" | N |
| Each hall return | Roshan | "Let's find the next golden door!" | N |
| Boss door ready | Roshan | "We cleaned the whole castle! Big door, please glow!" (`roshan_day_one_all_rooms_clean`; its only call site is unreachable) | W |
| Any room finished | Roshan | "We cleaned it! A new picture door is glowing!" (`day1_boss_door_glow`, catalogued but never triggered), then "Tap the arrow to go back!" | W + N |
| Toilet | Roshan | "Scrub the potty in little circles!" | N |
| Tub splash | Dust bunny | "Nooo! Splash!" (retire the "NO!" caption) | N |
| Waterfall | Roshan | "Swipe the waterfall trash down!" | N |
| Seahorse | Roshan | "Tap the trash in its mouth!" | N |
| Rescue | Roshan | "Bump the dust bunnies off Baby Eagle!" | N |
| Bunny popped | Roshan | "Poof! One bunny gone!" | N |
| Picker | Roshan | "Pick a color for Baby Eagle!" / "Tap the big heart!" | N |
| Grime cleaned | Roshan | "Sparkly clean!" / "All the counters sparkle!" | N |
| Customizer | Roshan | "Pick a color, then tap the star!" | N |
| Boss intro | Roshan | "Uh-oh! A giant dust bunny!" | N |
| Warning / bump | Roshan | "Swim out of the purple!" / "Achoo! Dusty! Try again!" | N |
| Dodge | Grand Puff | "Missed me! Hee hee!" | N |
| Star | Roshan | "Tickle his sparkly star!" | N |
| Befriend | Roshan | "Grand Puff is our friend now!" | N |
| Day Two | Roshan | "Day Two! Let's explore the castle!" | N |
| Optional cheer | Daddy | "You did it, Roshan!" | F only (`DL-SND-05`) |

## Appendix C — Grand Puff parameters, current to proposed

| Parameter | Current (`7cb2c399`) | Proposed (B) |
|---|---|---|
| Circle radius | 5.2 | 6.0 (ring stays visible around Roshan) |
| Hop warning | 2.35 / 2.2 / 2.2 s | 2.8 / 2.8 / 2.5 s |
| Lane/roll warning | 2.7 s | 2.8 s; first roll waits for her |
| Failure assist | +0.18 s each, max +0.9 s | +0.5 s each, max +1.0 s, then the level-2 hold |
| Bump | 1.05 s recovery; round restarts | 1.6 s "achoo"; he hops ≥8 units away; retry only that attack |
| Star window | 8 s first time, then 3.2 s +0.45 s/miss (max +2.4) | first time: open until tapped; then 4.0 s +1.5 s/miss; stays open after 2 misses |
| Miss cost | whole round replayed | one giggle and one hop |
| Pause after a tickle | 4.6 s first time (dash lesson), then 1.8 s | 2.2 s dizzy wobble while he shrinks |
| Dash | taught after round 1 | not used in this fight |
| Ending | 3.4 s implode, sprite hidden | ~6.5 s interactive befriending |
| Music | seek on warning; re-seek on star | seek at launch for jump + star timing; loop the build-up bar while waiting |

## Appendix D — status of the 2026-09-02 DO findings

| Status [V] | IDs |
|---|---|
| Fixed in code (not device-verified) | DO-04, DO-07, DO-08, DO-11, DO-14, DO-15, DO-18, DO-21, DO-22 |
| No longer apply (reef retired; boss redesigned) | DO-02, DO-12, DO-20 |
| Partly fixed | DO-01 (voice missing, D1R-08), DO-03 (generic/yay lines remain), DO-06 (nothing points at ↩), DO-09 (Day Two start is OD-9), DO-13 (routing fixed; Continue soft-lock was D1R-01), DO-16 (voice dropped/wrong), DO-17 (lines still cut), DO-19 (only via the playroom nook) |
| Still open | DO-05 (**worse**: the next-room cards and the pulsing back arrow were removed; the "back to the hall" line is dropped), DO-10 (D1R-20), DO-23 |

## Appendix E — Continue soft-lock reproduction

Throwaway reproduction (not committed) at `7cb2c399`:
1. Boot `main.tscn` with an isolated save path.
2. Set `day_one_active`, call `discover_dirty_castle()`, and write the save.
3. Free the scene, boot again from that save, and call the real `StartMenu._continue_game()`.
4. Run 60 live frames.

| Run | World ID | Room rebuilds | Bathroom activity mounted |
|---|---|---|---|
| Continue (before) | empty in 60/60 frames | 60 in 60 frames | 0/60 frames |
| Candidate sequence (`_enter_level2_now(true)` then `_enter_castle_interior_now()`) | `level2` in 60/60 | 0 | 60/60 |

The committed guard is the Day One leg of `scripts/probe_load.gd`. It fails
against the unrepaired code with `world_frames=0 rebuilds=60 activity_frames=0`
and passes with the repair. The evidence is in
`design/audit_impacts/day-one-continue-softlock-20260923.json`.
