# Comparative playthrough rubric (Reef of Light Opera job games)

Audience constraints (binding, from CLAUDE.md): one specific 4-year-old, non-reader,
one finger on a 3-4-year-old Android tablet, short sessions, no fail states,
no reading-dependent objectives, progress never lost.

Score every game (ours and each reference) 0-5 on each dimension, with a one-line
evidence note that points to a log line, a timing, or a frame file. 5 = best
practice for a 4-year-old; 0 = absent. Scores for references are judged against
the same 4-year-old audience, not against the reference's own audience.

| Code | Dimension | What to measure across the 10 playthroughs |
|---|---|---|
| D1 | Core verb fidelity | Does the main touch action feel like doing the job (stir, punch, steer, dig)? Name the verb. |
| D2 | Agency | Does input change the outcome? Idle run must not win; expert vs. sloppy runs must differ visibly. Report idle-run result and expert vs. child-sim delta (time, quality, outcome). |
| D3 | Feedback per touch | Every touch gets sound + motion within ~100 ms; contact effect at the touch point; distinct good/better/best response. Count silent or dead touches. |
| D4 | Onboarding without reading | Show-then-do demo, voice prompt, idle re-hint timing (target 6-8 s), hand/ghost clarity. Time from screen open to first possible meaningful input. |
| D5 | Mercy without autopilot | How struggle is handled: widened windows, slowed cues, skip after N tries, vs. the game playing itself. |
| D6 | Pacing | Session length, dead time (no input possible) as % of session, longest wait, phase count. |
| D7 | Variety and replay | Across 10 runs: what changes (layouts, outcomes, characters, emergent events)? Count distinct states seen. |
| D8 | Payoff and persistence | Celebration quality, a made artifact the child keeps or sees again, collection/customization hooks. |
| D9 | Readability and touch targets | Target size (>= ~2 cm on a tablet, about 120 px at 1280x720 on an 11-inch tablet), contrast, one obvious next action. |
| D10 | Gesture suitability | Uses tap / one-finger drag (high success at 3-6); avoids long press, double tap, multi-finger, rapid mashing, continuous holds. |

## Playthrough protocol (10 per game)

Use a spread of input policies so the 10 runs test robustness, not just the happy path:

1. expert-1, expert-2: fastest correct play.
2. child-sim-1..4: 500-900 ms reaction latency, ~25% of taps off-target by 40-120 px,
   occasional wrong choice, drags that wobble.
3. slow-1: long pauses (10-20 s) between actions, to observe re-hints.
4. random-tapper-1: taps anywhere at ~2 Hz.
5. idle-1: no input for 60 s (or the game's natural length), observe whether it wins or helps.
6. replay-1: a second full run after a completed one, to observe variety and persistence.

For real-time reference games an agent cannot react at human speed, so use the
game's own settings (easiest difficulty, assists, auto modes) and scripted input
timelines, and record video/frames to judge. Say plainly which runs were scripted.

## Per-run log (JSON lines)

{"game": "...", "build": "ours|reference", "run": 1, "policy": "expert-1",
 "seconds": 0.0, "completed": true, "inputs": 0, "dead_touches": 0,
 "longest_wait_s": 0.0, "hints_seen": 0, "events": ["..."], "frames": ["path.png"],
 "notes": "..."}

## Findings format (findings.md per career)

1. Scores table: rows = ours + each reference, columns D1-D10, plus a short evidence column.
2. "Where the reference is objectively better": numbered, each with the measurement
   that proves it (a time, a count, a frame), not a taste claim.
3. "Where ours is better" (keep these).
4. Redesign recommendations: concrete, buildable in Godot 2D under the hard rules,
   each with an acceptance check a probe or a person can run.
5. Limits: what could not be played or measured and why.
