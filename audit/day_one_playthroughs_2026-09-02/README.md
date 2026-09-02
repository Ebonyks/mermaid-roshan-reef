# Day One playthrough bundle — 2026-09-02

Sixteen independent, code-traced playthroughs of Day One (the fresh-save
entry arc) at integration head `ff68f955`, one persona each, produced as
evidence for `CODEX_DAY_ONE_PLAYER_EXPERIENCE_HANDOFF_2026-09-02.md`. Each
run followed `PROTOCOL.md` in this directory: read-only on the repository,
no Godot execution (none is available in the analysis container), every
claim cited to `file:line`, timings derived from constants, tweens, timers
and gesture thresholds plus the protocol's child model, and a fixed report
shape (beat log, time budget, pros, cons, invariant hazards, at most six
numeric tuning proposals, confidence split into proven / inferred / could
not determine).

These reports are `SUPPORTING_CURRENT` evidence for the handoff. They
cannot grant device, child, owner or release acceptance; nothing here was
executed on a device. Original line numbers are pinned to `ff68f955` and will
drift. The current-head reconciliation is `db4bcf76` below and in the handoff.

## Persona matrix

| Run | File | Persona | Angle |
|---|---|---|---|
| 01 | `run_01_golden_path.md` | Golden path, attentive | full baseline beat log with measured clip lengths |
| 02 | `run_02_tap_everything.md` | Tap-everything toddler | input routing, spam, hidden controls, sequence breaks |
| 03 | `run_03_passive_watcher.md` | Passive, distracted watcher | idle nudges, silence table, phone-down episodes |
| 04 | `run_04_impatient_skipper.md` | Impatient skipper | forced-wait vs agency accounting, skippability |
| 05 | `run_05_door_explorer.md` | Door explorer | blocked doors, elevator, leaving mid-room, courtyard |
| 06 | `run_06_quit_and_resume.md` | Quit-and-resume | 19 kill points, kill-point ledger, Continue routing |
| 07 | `run_07_sloppy_gestures.md` | Sloppy gestures, weak fine-motor | every recognizer's tolerance and failure feedback |
| 08 | `run_08_speedrunner.md` | Fast, skilled, second time through | hard floor, ceremony verdicts, fast-input breakage |
| 09 | `run_09_repeat_visitor.md` | Repeat visitor | revisits, replays, post-boss placement |
| 10 | `run_10_audio_first.md` | Ears first | audio contract per beat, clip resolution, collisions |
| 11 | `run_11_non_reader.md` | Non-reader, no adult | 51-string text-carrier inventory |
| 12 | `run_12_save_routing.md` | The family phone | four save openings, New Game wipe, corrupt saves |
| 13 | `run_13_boss_struggler.md` | Boss struggler | Grand Puff second by second, mercy ramp |
| 14 | `run_14_stuffie_room.md` | Stuffie lover | playroom rescue, picker, companion, 2D staging |
| 15 | `run_15_art_room.md` | Little artist | art studio, customizer, logo-studio hijack |
| 16 | `run_16_session_budget.md` | Three short sessions | attention reservoir, safe stops, session fit |

## Convergence — which runs found what

| Handoff finding | Runs reporting it independently |
|---|---|
| DO-01 arrival guidance exits Day One | 01 02 03 04 05 06 07 08 09 10 11 12 16 |
| DO-02 reef Dusty Attic ungated | 02 09 12 |
| DO-03 no objective clip; generic "talk"/"win"/yay | all sixteen |
| DO-04 castle hides captions | 02 03 08 10 11 14 15 |
| DO-05 silent hand-offs; boss-door line unreachable | 01 02 03 04 05 07 08 09 10 11 13 14 15 16 |
| DO-06 golden door off-screen; ▼ hidden forever | 01 02 03 05 06 07 08 11 12 14 15 16 |
| DO-07 boss flag saved before the fight | 01 02 03 04 06 08 09 11 12 13 16 |
| DO-08 bathroom motion clock resets per touch | 01 02 07 08 |
| DO-09 post-boss landing in the 3D reef | 01 03 04 05 07 08 09 11 16 |
| DO-10 legacy saves normalised into Day One | 12 |
| DO-11 NEW GAME two-tap wipe | 02 07 11 12 16 |
| DO-12 boss windows, holds, angry puff, live star loss | 01 03 04 07 08 10 11 13 16 |
| DO-13 Continue lands at the plane | 06 12 16 |
| DO-14 stuffie picker unreachable after close | 04 06 09 14 |
| DO-15 art tutorial launches the logo studio | 09 15 |
| DO-16 customizer silent modal; choice unused | 01 03 07 10 11 15 |
| DO-17 wacky_fail on tub success; sink line silenced; collisions | 01 03 04 05 10 11 13 16 |
| DO-18 skimmer/seahorse restore without emitting | 16 |
| DO-19 sparkly-clean spam; one-way bathroom; Rumi one-shot | 05 09 16 |
| DO-20 pause REEF tile | 02 05 11 |
| DO-21 SFX spam, colliding banners, label typo | 02 04 05 09 10 12 |
| DO-22 debounce starvation | 06 16 |
| DO-23 leftover 3D magnitudes; 3D companion | 14 |

## Stage 0 reconciliation at `db4bcf76`

The run claims remain historical evidence. At the current branch head,
`REPRODUCED` still exists, `NARROWED` remains actionable but was too broad or
stale, `SUPERSEDED` no longer describes current code, and
`INFERRED_PENDING_RUNTIME` requires a device/headless observation. Current
file:line evidence and package consequences are authoritative in the
handoff's full register; this compact index prevents the old run wording from
being mistaken for current truth.

| ID | Status | Current evidence |
|---|---|---|
| DO-01 | REPRODUCED | `scripts/main.gd:4063-4078`; `scripts/arena/sky_lagoon_promenade.gd:278-286,1143-1149` |
| DO-02 | NARROWED | `scripts/day_one_director.gd:434-454` blocks zero-room boss completion; `scripts/main.gd:5470-5471,10418-10419` leaves reef route exposed |
| DO-03 | NARROWED | `assets/audio/voices/VOICE_MANIFEST.md:3-21,53-63`; `scripts/audio_director.gd:10-35` establish current Parler `filler_v1` authority |
| DO-04 | REPRODUCED | `scripts/arena/castle_rooms_25d.gd:960-993,1033-1116` hides shared HUD while open |
| DO-05 | REPRODUCED | `scripts/main.gd:7421-7472,7555-7602`; `scripts/arena/castle_rooms_25d.gd:299-305` |
| DO-06 | REPRODUCED | `scripts/arena/castle_rooms_25d.gd:152-190,1719-1735` |
| DO-07 | REPRODUCED | `scripts/main.gd:8043-8080`; `scripts/day_one_director.gd:434-440` |
| DO-08 | NARROWED | `scripts/games/day_one_bathroom_cleaning.gd:25-27,299,494-513,822-862` |
| DO-09 | INFERRED_PENDING_RUNTIME | `scripts/main.gd:9410-9455,11358-11487`; post-boss visual/recoverability needs runtime evidence |
| DO-10 | NARROWED | `scripts/save_state.gd:431-471,557-566`; legacy policy is owner-blocked |
| DO-11 | NARROWED | `scripts/start_menu.gd:201-240,261-280`; current KEEP GAME/START NEW styling supersedes gold-then-gold wording |
| DO-12 | NARROWED | `scripts/games/dust_boss.gd:60-68,419-435,570-587,711-730,956-960`; pips remain undelivered while `hud_game` is hidden |
| DO-13 | REPRODUCED | `scripts/main.gd:4063-4070`; `scripts/start_menu.gd:242-249`; `scripts/arena/sky_lagoon_promenade.gd:278-286` |
| DO-14 | REPRODUCED | `scripts/main.gd:7421-7449`; `scripts/arena/castle_rooms_25d.gd:4187-4201,4811-4820` |
| DO-15 | REPRODUCED | `scripts/main.gd:7421-7455`; `scripts/arena/castle_rooms_25d.gd:498-501` |
| DO-16 | REPRODUCED | `scripts/attack_customizer.gd:99-121,182-193,257-261` |
| DO-17 | NARROWED | `scripts/games/day_one_bathroom_cleaning.gd:186,583,599,669-670,811-816`; current filler resolution changes old yay claim |
| DO-18 | REPRODUCED | `scripts/games/pool_skimmer_activity.gd:92-100`; `scripts/games/pool_seahorse_rescue_activity.gd:100-106` |
| DO-19 | NARROWED | `scripts/main.gd:7421-7435,7555-7602`; current completed-room answer is one clip |
| DO-20 | REPRODUCED | `scripts/pause_menu.gd:211-262` |
| DO-21 | NARROWED | `scripts/arena/castle_rooms_25d.gd:1695-1717`; old duplicated-label claim no longer carries |
| DO-22 | REPRODUCED | `scripts/main.gd:4080-4088,10141-10148` |
| DO-23 | NARROWED | `scripts/arena/castle_rooms_25d.gd:4203-4228,4255-4274`; companion 3D debt is outside D7b |

Package corrections: WP-D9 is first; D5 is split into safety/resumability and
pacing/tell packages and includes `scripts/pause_menu.gd`; D1 reuses
`day_one_current_room_id`; D6 legacy policy is owner-blocked; D7 is split and
DO-23 is partial only. Use the existing Parler `filler_v1` cohort, re-prompt
at 5 s then 12 s, target a 5.4 s boss hold with typical ≤90 s / mercy ≤120 s,
keep pips explicitly unimplemented until built, avoid a permanent thirteenth
elevator card, and place the caption above the picker. All owner decisions
remain binding.

## Reading the reports

- The beat logs are the timing source. Where a run says "flow map, not
  re-traced" for a room outside its focus, use run 01 for that room.
- Every run separates proven-by-code from inferred in its Confidence
  section; inferred items (device timings, the visual result of the
  post-boss anchor, GUI hit-test ordering) need a probe or a device capture
  before they are relied on.
- Runs disagree occasionally on secondary estimates (for example whether
  the Rumi line is 3 s or 4 s); the handoff uses run 01 as the tie-break
  and marks contested numbers as ranges.
