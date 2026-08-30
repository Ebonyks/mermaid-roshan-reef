# Validation log

Engine: `C:\tmp\godot-4.7.2\Godot_v4.7.2-stable_win64_console.exe`
Version: `4.7.2.stable.official.ed1daf0bf`

## Static gates

- `python -m gdtoolkit.parser <all changed .gd files>` — PASS.
- `python tools/lint_inference.py <all changed .gd files>` — PASS.
- `git diff --check` — PASS; line-ending warnings only.
- Exact-engine editor load/check — PASS after correcting one development-time
  misplaced filter; no current parse/compile error.

## Exact Mobile focused probes

- `probe_day_one_pool_shots.gd` — PASS, 0 failures, candidate v3.
- `probe_day_one_bathroom_shots.gd` — PASS, 0 failures, candidate v5.
  Confirms the full dirty plate is invisible when clean fixture layers appear;
  the bathtub is not double-drawn during the reveal.
- `probe_day_one_art_studio_shots.gd` — PASS, 0 failures, candidate v7.
  Confirms entry-visible grime, rejected out-of-order taps, exactly one active
  target after each state change, saved completion, sparkle, no delayed Castle
  Logo overlay, and a true settled clean-room frame.
- `probe_day_one_stuffie_transition_v2.gd` — PASS, 0 failures, candidate v6.
  Confirms ordered pins, immediate saves, purpose-built pinned/standing assets,
  settled bright room, same-identity rescue picker, and two measured contain
  fits: 150×199.48 within 150×200 and 227.09×302 within 302×302.

## Proportionate regression probes

- `probe_day_one_director.gd` — PASS, 0 failures.
- `probe_day_one_castle_dressing.gd` — ALL OK.
- `probe_day_one_pool_cleanup.gd` — PASS, 0 failures.
- `probe_day_one_bathroom_cleanup.gd` — PASS, 0 failures. The shared swimmer
  audit snapshot and focused assertion now match the visible success reaction:
  one bounded spin with `WHEE!`, without advancing before the drain finishes.
- `probe_day_one_bathroom_integration.gd` — PASS, 0 failures.
- `probe_passive.gd` — ALL OK; no passive reward/progress.
- `probe_load.gd` — exit 0; legacy save restore checks printed successfully;
  pre-existing exit-time leak/resource diagnostics remain non-fatal.
- `probe_day_one_integration.gd` — one known base legacy assertion failure:
  `completion advances the physical castle route`; it calls
  `complete_tutorial("bathroom")` even though Bathroom is no longer represented
  by that legacy tutorial-kind path. All wiring assertions pass.
- `probe_day_one_art_attack_state.gd` — the same unchanged legacy setup produces
  one failure at `art completion uses the existing room order`: its setup also
  calls `complete_tutorial("bathroom")`. The candidate's director diff adds only
  the saved room-polish map and does not change route advancement; all Art
  cleanup/customizer, JSON-safety, malformed-save, and large-target checks pass.

The final Art v7 visual probe used Godot `4.7.2.stable.official.ed1daf0bf`,
Forward Mobile, D3D12, 1280×720. The equivalent headless capture process did
not emit `frame_post_draw`, so the off-screen Windows display driver was used;
the behavior probes remain headless.

## External acceptance gates

Not run and not claimed: intended-child observation, Lenovo Tab M11 frame-time,
thermal, memory, or touch acceptance, and owner art acceptance.
