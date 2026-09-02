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
executed on a device. Line numbers are pinned to `ff68f955` and will drift.

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
