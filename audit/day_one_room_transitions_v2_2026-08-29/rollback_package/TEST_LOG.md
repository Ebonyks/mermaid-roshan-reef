# Validation log

Engine: `C:\tmp\godot-4.7.2\Godot_v4.7.2-stable_win64_console.exe`

Version: `4.7.2.stable.official.ed1daf0bf`

Renderer/capture: Forward Mobile, D3D12, 1280×720.

## Static gates

- `python -m gdtoolkit.parser <all changed .gd files>` — PASS.
- `python tools/lint_inference.py <all changed .gd files>` — PASS.
- Exact-engine `--headless --import .` followed by editor/analyzer load — PASS
  after importing the correction v3 table assets; no current parse, compile,
  or import error.
- `git diff --check` — PASS after documentation reconciliation.

## Authoritative exact-Mobile capture probes

- `probe_day_one_pool_shots.gd` — PASS, 0 failures, Pool candidate v3.
- `probe_day_one_bathroom_shots.gd` — PASS, 0 failures, Bathroom candidate v5.
  It confirms the dirty plate is invisible when clean fixtures appear; the
  bathtub, sink, and toilet are not double-drawn during the reveal.
- `probe_day_one_stuffie_transition_v2.gd` — PASS, 0 failures, Stuffie
  correction v2. It confirms dirty banners hidden, ceiling bunny first and
  saved, ordered pin bunnies, exact purpose-built pinned/standing Eagle paths,
  clean banners restored, and full standing-Eagle card/preview contain fit.
- `probe_day_one_art_studio_shots.gd` — PASS, 0 failures, Art correction v3.
  It confirms eleven ordered interactions, exactly one responsive/cued target,
  one rainbow and palette owner, one table owner per side, zero target/table
  intersection with margins, cleared persistent glow, visible feedback, saved
  completion, reveal, and settled clean state.
- `probe_day_one_art_attack_state.gd` — PASS, 0 failures after the current
  ordering and save normalization.

The off-screen Windows display driver was used for capture because headless
Windows did not emit `frame_post_draw`; focused behavior probes remain
headless-compatible. All authoritative room captures were produced by exact
Godot 4.7.2 Mobile, not by image compositing.

## Proportionate regression probes

- `probe_day_one_director.gd` — PASS, 0 failures.
- `probe_day_one_castle_dressing.gd` — ALL OK.
- `probe_day_one_pool_cleanup.gd` — PASS, 0 failures.
- `probe_day_one_bathroom_cleanup.gd` — PASS, 0 failures.
- `probe_day_one_bathroom_integration.gd` — PASS, 0 failures.
- `probe_passive.gd` — ALL OK; zero-input play awards no reward/progress.
- `probe_load.gd` — exit 0; legacy save-restore checks printed successfully;
  pre-existing exit-time leak/resource diagnostics remain non-fatal.
- `probe_day_one_integration.gd` — one known base legacy assertion failure:
  `completion advances the physical castle route`. The stale probe invokes
  `complete_tutorial("bathroom")` although Bathroom no longer uses that legacy
  tutorial-kind route. All current wiring assertions and focused production
  paths pass; this correction does not alter that legacy assertion path.

## Visual rejection and acceptance record

- Stuffie correction v2 — accepted for current agent review: authored wall
  healing has no visible flat rectangle/seam; dirty banners are absent; ceiling
  bunny, purpose-built Eagle rescue, clean banner restoration, and full picker
  silhouette are visible.
- Art correction v1 — superseded.
- Art correction v2 — rejected: derived table masks produced severe
  torn/scalloped inner alpha edges.
- Generated table-edit candidate — rejected/excluded; not project-wired.
- Art correction v3 — accepted by primary inspection and both fresh Luna
  reviewers: approved design is preserved, table silhouettes are continuous,
  and no visible halo, hole, seam, rectangular floor pickup, duplicate palette,
  table overdraw, or persistent rainbow/glow remains.
- Exact v3 isolation evidence:
  `visuals/correction_v3/art_layer_isolation/01_table_ownership_isolation.png`.

## Fresh reviewer gates

- Child/non-reader Luna: Stuffie correction v2 **4.98**, Art correction v3
  **4.96**, scoped correction mean **4.97**; no hard sequence blocker.
- Visual/phone/performance Luna: Pool **4.96**, Bathroom **4.96**, Stuffie
  **4.96**, Art **4.95**, cumulative **4.96**; every room ≥4.75 and cumulative
  ≥4.85. Craft remains narrowly weakest only on dirty-entry density and narrow
  grime readability, not overdraw or ownership.

## External acceptance gates

Not run and not claimed: intended-child observation, owner art acceptance, and
Lenovo Tab M11 frame-time, thermal, memory, and touch acceptance.
