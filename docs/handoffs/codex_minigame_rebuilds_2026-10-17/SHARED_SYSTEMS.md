# Shared systems for the three rebuilds

- **Status:** `PROPOSED / CANDIDATE` engineering specification for Codex.
  Written by Claude; no game file is changed by this document.
- **Used by:** [POP_STAR.md](POP_STAR.md) (all of it),
  [BALLERINA.md](BALLERINA.md) (clock, section player, move reader, contest),
  [RACER.md](RACER.md) (contest, staging, saves, probes).
- **Rules:** `DL-AGE-01` to `DL-AGE-07`, `DL-INT-01`, `DL-INT-02`,
  `DL-INT-04`, `DL-INT-06`, `DL-INT-07`, `DL-INT-14`, `DL-UI-01` to `DL-UI-05`,
  `DL-MOT-03` to `DL-MOT-05`, `DL-MOT-12`, `DL-SND-01`, `DL-SND-04`,
  `DL-SND-05`, `DL-SAVE-01`, `DL-SAVE-03`, `DL-SAVE-06`, `DL-CODE-10`.

## 1. Principles all three keep

1. **One real skill that belongs to the job:** answering and playing drums,
   dancing steps, choosing a lane.
2. **Roshan performs it, at the place, visibly** (`DL-INT-02`, `MA-PLAY-004`):
   no widget panel stands in for her.
3. **The world object changes:** a drum head dips, a pose lands, a kart swerves.
4. **Mercy widens, slows or waits; it never plays for her** (`DL-AGE-04`).
   Zero input never progresses and never wins or loses a contest.
5. **Intentional play beats random or held input** (`DL-AGE-05`). No wrong
   input pays a crumb (the current `_miss_pay` crumbs do not carry over).
6. **Touch-down is the moment** (Sesame Workshop 2012): every touch gets sound
   and motion within two frames (`DL-AGE-07`).
7. **One touch owns one route** until release; a palm or several fingers are
   one touch; pause, focus loss, Back and close cancel held input
   (`DL-UI-04`, `DL-UI-05`).
8. **Wordless:** exact spoken cues for every objective (`DL-SND-01`), pictured
   cues, no digits or text the child must read.
9. **Painted art, not code shapes** (`MA-VIS-008`, the owner's 2026-10-17
   art-quality correction being integrated by another session): use ImageGen
   or reuse, whichever gives polished storybook art; no flat code-drawn
   substitutes.

## 2. BeatKit: music clock and cue judge

One small Canvas-side component, owned by the activity, with no reward
authority. It reports intentions (credited, wrong, offbeat, damped); the
career world decides progress, as today.

**Clock.** Use Godot's hardware-clock method from "Sync the gameplay with audio
and music": `time = get_playback_position() + AudioServer.get_time_since_last_mix() - AudioServer.get_output_latency()`,
discarding any value lower than the previous frame's. Each start, pause and
resume opens a new epoch with a generation number; stale callbacks from an old
epoch are ignored. The documentation page says it is not yet updated for 4.7,
so prove the formula on the exact 4.7.2 build and the target phone before
tuning windows.

**Sections.** Each song is a list of sections, each a whole number of bars,
rendered as its own clip. Use `AudioStreamInteractive` (clips with transitions
at the next beat or next bar, and auto-advance) to move to the next section or
repeat the current one, and `AudioStreamSynchronized` when a section has
layers (for example a fuller band layer that joins when she is in the groove).
Set `bpm`, `beat_count` and `bar_beats` on each Ogg clip. If the clock cannot
read the interactive stream's position reliably, play one Ogg per section and
switch on bar boundaries computed from the clock instead. Spike both and
record the choice.

**Chart.** Generate it, never hand-place it: `tools/build_area_music.py`
already renders each cue from a declarative score, so it can also emit the
chart for an arrangement. One JSON per song:

```json
{
  "song_id": "opera_popstar_concert",
  "score_sha256": "<hash of the score entry>",
  "audio_sha256": {"verse": "<hash>", "chorus": "<hash>"},
  "bpm": 118,
  "meter": [4, 4],
  "sections": [
    {"id": "verse_1", "kind": "echo", "bars": 4, "loopable": true}
  ],
  "cues": [
    {"id": "v1_c1_n1", "section": "verse_1", "beat": 0.0,
     "target": 1, "role": "call"},
    {"id": "v1_a1_n1", "section": "verse_1", "beat": 4.0,
     "target": 1, "role": "answer"}
  ]
}
```

Roles: `call` (the band plays it), `answer` and `play` (hers), `lead` (crowd
break), `finish` (the last crash). Validation fails the build when: a cue is
off its section's grid; two child cues are closer than the sum of the early
and late windows; a child cue falls in the first two beats after a count-in;
a call bar lacks its answer bar; a target index is unknown; or a hash does
not match the file.

**Judge.** Adopt the semantics of Codex's uncommitted
`scripts/popstar_rhythm_phrase.gd` (in the `popstar-rhythm-20261017`
worktree): the first tap inside a cue's window owns that cue; a wrong target
consumes it; taps outside every window are "offbeat"; results carry the epoch
generation and never award progress themselves. Fold that helper into BeatKit
rather than shipping two judges. Add:

| Addition | Starting value | Why |
|---|---|---|
| Asymmetric window | 0.20 s early, 0.32 s late | Young children rarely tap ahead of the beat (Bobin-Bègue et al. 2014) |
| Well-timed band | 0.12 s early, 0.18 s late | A brighter sparkle; never a gate |
| Finger-bounce debounce | Ignore a second trigger on the same target within 0.12 s | 4–5-year-olds' fastest taps were about 0.26 s apart (McAuley et al. 2006) |
| Anti-mash damper | No credit for a tap that has 3 or more taps in the previous 0.75 s | Lets a natural 2–2.5 taps per second through and stops 4 Hz and faster mashing |
| Mercy 1 | Half the cues; 0.30 s early, 0.45 s late | After two vamps of clear play |
| Mercy 2, "wait" | No timing; each cue waits on its target; a wrong target makes it rest one beat | After two more vamps; the floor for a child who cannot yet keep a beat (Woodruff Carr et al. 2014) |
| Latency offset | `get_output_latency()` plus a learned offset: the median signed error of at least 6 credited rehearsal taps, clamped to ±0.12 s | Phones differ; a child should not need a calibration screen |

**Scaffold controller.** Per skill (for example "echo answer"): level 1
ribbons, level 2 glow, level 3 memory; up after two clean results, down after
one miss. Persist it (section 8).

**Section controller.** A section is met when at least 60% of its child cues
are credited. An echo answer is credited when all its notes are, or all but
one of a three-note phrase. If a section is not met the band vamps it with
one help level more; mercy escalates as in POP_STAR §5. "Clear play" for
escalation means at least two undamped taps on a cue's own drum, in time or
not. Idle for about 7 s triggers a spoken re-invitation and a ghost hand on
the next target.

**Sound.** Every tap plays its instrument at once, with no quantizing delay.
The child's part is absent from the backing so that her hits are the part.

## 3. Move reader (Ballerina)

The reader verifies the one gesture the current step asks for; it never
classifies among all gestures, which keeps misreads rare. Parameters are in
BALLERINA §4: tap anywhere on Roshan; a circle of at least 270° around her
centre within 2 s; a drag released in a glide spot, or a tap on it; a press
of 1.5 s with one forgiven lift under 0.25 s; a downward drag of 60 px.
Attempts count only for the cued gesture's own kind, so taps never unlock a
fallback. The reader also tells the animation player when to start
anticipation (touch-down) and the beat on which the action should land
(BeatKit's clock, next beat).

## 4. Imp contest adapter

All three contests follow `DL-INT-14` and contract C1–C16 in
[the imp contest specification](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md):

- he is hidden until the final act and enters when it begins;
- one contest at the end, using the job's own skill;
- he can win, and then only the contest restarts, after a beat of at most
  2 s;
- he slows radically after two failures;
- zero input decides nothing;
- story runs opt out.

| Career | Contest | Kind | Changes to the contest specification |
|---|---|---|---|
| Pop Star | Drum-off (replaces §6.12 Sing-off) | Points, first to 3 | Phrases on drums with ghost ribbons; his slow mode is half-time |
| Ballerina | Twirl-off (§6.3) | Race, 3 turns | Turns are circles around Roshan with her pirouette; one turn at most per 2 s |
| Racer | Grand Prix (§6.11) | Race | The lane race in RACER.md; his kart finishing first is his win; half speed after two failures |

Retire the Hall stage-long rival race for Pop Star and Ballerina (the contest
packet's open question 4 recommends retiring it everywhere). Update
`CONTEST_DESIGN.md` §6.3, §6.11 and §6.12 in the same change that implements
these contests.

## 5. Opera Hall plan

Remove `popstar` and `ballerina` from `OperaPerformancePlan.ENABLED`
(`scripts/opera_performance_plan.gd:8`); their built-in rehearsals replace the
copied practice part. Magician keeps its current plan. Racer was never enabled.

## 6. Staging rules

- Full-stage composition; no 500×376 action panel or other widget card over
  the stage.
- Roshan always visible at performance size; no cue path or effect crosses
  her face (`DL-READ-05`).
- Each touchable thing is its own owned card (`DL-LAY-03`); foreground is
  sparse (`DL-LAY-08`).
- Measure overdraw for every new state with `tools/measure_overdraw.py` and
  pass OD1–OD6 before claiming the gold-star C7 criterion.
- A phone-size squint test with the HUD present (`DL-READ-02`).

## 7. Voice and audio

- **Exact cues.** Every new objective has an exact spoken cue, made with the
  existing local synthetic Roshan workflow, as in the 2026-10-14 Guide
  decision. Captions stay for the adult (`DL-SND-02`).
- **Protected recordings.** Family recordings are never edited or imitated
  (`DL-SND-05`); Daddy's lines, if any, use the existing Daddy-only filler
  preset after owner listening.
- **Music.** Music ducks under speech (`DL-SND-04`). New arrangements follow
  the area-music rules (`DL-SND-07`, `DL-SND-08`): Ogg, 48 kHz stereo, a whole
  number of bars, loop-tagged where they loop.

## 8. Saves and lifecycle

- **Add keys, never remove** (`DL-SAVE-01`). Additive keys with defaults:
  - per-career part checkpoint;
  - per-skill scaffold levels;
  - the learned rhythm offset;
  - the Racer's chosen kart colour.
- **Career bits** keep the stable `opera_stars` namespace (`DL-SAVE-06`).
- **Resume and teardown.** Re-entry resumes at the start of the last
  unfinished part with a count-in or countdown. Every timer, tween, queued
  voice and audio clip belongs to the activity and stops on teardown
  (`DL-SAVE-03`).

## 9. Counts and rules that change when this lands

- `DL-INT-07` counts change: careers stay 13, but phases and modes do not.
- `DL-INT-08` (Ballerina) and `DL-INT-10` (Racer) are rewritten to the new
  contracts.
- `DL-INT-14` and its contest table follow §4 above.
- Also update `DL-QA-12`, `probe_opera_2d`'s structure checks, the gold-star
  catalogue entries for the three games (`--rebind` after re-assessment), and
  the Chapter 2 adapter phase sets.
- Follow the job-platform plan if its content layer has landed by then.

## 10. Probes

Ship probe-first (`DL-CODE-10`). New trusted probes:

| Probe | What it covers |
|---|---|
| `probe_beatkit.gd` | Clock monotonic per epoch, new epoch on resume; windows; debounce; damper; mercy 1 and 2; chart validation failures; latency offset clamp |
| `probe_popstar_band.gd` | POP_STAR §11 legs |
| `probe_ballet_show.gd` | BALLERINA §11 legs |
| `probe_racer_lanes.gd` | RACER §11 legs |

Each drives real touch events through `_gui_input`, as the Boxer and Racer
legs of `probe_opera_2d` already do. Add them to the trusted roster in
`scripts/ci.sh`. A change to `.github/workflows/` is high-risk and
explicit-task-only.

## 11. Art and animation order

1. **Pilot one action per game:** the bass-drum strike, the pirouette, the
   kart lane-change lean.
2. **Review.** Each pilot goes through the animation protocol and its job card
   (`DL-MOT-12`, `DL-MOT-14` to `DL-MOT-16`) and gets an owner look before the
   full set.
3. **Expand to the full set** once the pilot passes.

Owner rules that apply throughout:
- whole-frame sprites;
- constant size;
- left and right travel only;
- a rich set, not a limited one (owner decisions 2026-10-04 to 2026-10-07).
