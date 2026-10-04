# Codex handoff — what the loop review left for Codex (2026-10-03)

**Owner requests (2026-10-03):** *"audit, evaluate, and improve"* commit
[`4cb14feb`](https://github.com/Ebonyks/mermaid-roshan-reef/commit/4cb14febc2c5f0074d5ad8386ce66f19f940c84d),
then *"Refine and fix it."*

**From:** Claude. Claude fixed the loop's tooling, recipes, registers and
records in the same change as this handoff (see [REVIEW.md](REVIEW.md),
section 4, items LR-01 to LR-22). **To:** Codex, for the items that need game
code, Godot runs, CI captures or workflow changes. **Owner:** answers the
questions in the cycle `2026-10-03b` report once it is published.

**Status:** `PROPOSED / CANDIDATE`, revision 1. Tracking findings:
[`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008)
(CR2–CR4), [`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009)
(CR5, CR6) and [`MA-OPERA-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-001)
(CR1); lifecycles unchanged. Every package follows `CLAUDE.md`, `AGENTS.md`
and the master-audit development contract (`DL-AUTH-05` to `DL-AUTH-07`).

## Work packages

### CR1 — Chef's first step may never finish (child-facing; reproduce first)

The balance probe's three Chef personas all stop at
`time_cap:phase=0,mode=pourt,progress=5.000000,goal=5.000000`. A Python model of
`_pour_tick` (`scripts/opera_gesture_surface.gd`, lines 6107–6126) with a held,
on-target pitcher sums the poured amount to 4.999999999999999 at the probe's
step and 4.999999999999998 at 60 frames per second; once `pour_level` clamps to
1.0 nothing more is poured, and completion needs `phase_progress >= goal`
(`scripts/opera_career_world_2d.gd`, line 3521).

- Reproduce in Godot 4.7.2 with real input at 60 fps (a focused probe; no
  captures needed). If it reproduces, the child can fill the bowl and be stuck.
- Fix inside the existing design: complete when the bowl is full, or compare
  with a small tolerance; keep the step truthful (it must not finish while the
  pitcher is idle) and keep every Chef probe green.
- **Accept:** a probe holds the pitcher on target at 60 fps and reaches mixing;
  a passive control never does; the Chef persona runs report a finite time.

### CR2 — CI captures fail because the runner cannot render Mobile

On every run the Xvfb steps log "switching to OpenGL 3"; the Sky Lagoon probe
writes 20 of 20 frames and then reports `rendering_method|gl_compatibility` and
`RESULT|FAIL`; the Castle probe writes 13 of 13 and reports `RESULT|FAIL` with no
reason; the dust-boss arena capture reports `INCOMPLETE`.

- Either install a version-pinned Vulkan software driver (lavapipe) in the
  workflow so the probes render with the Mobile renderer, or make each capture
  report `NOT_MEASURED|renderer=gl_compatibility` instead of `FAIL` when the
  requested renderer is unavailable. The workflow is a high-risk file: it needs
  the owner's explicit task, named in the commit message, and new packages
  pinned to exact versions.
- Add the failure reason to the Castle `RESULT` line; finish or explain the
  dust-boss arena interruption.
- **Accept:** in one green run, every capture step reports `MEASURED`, or
  `NOT_MEASURED` with its reason, and the study lists no false FAIL.

### CR3 — Opera pacing measures 4 of 15 careers

`BALANCE|RESULT|CAPPED|measured=12|capped=3|not_measured=30|expected=45`. Ten
modes have no input policy (`ballet_pose`, `candy_sort`, `xray_scan`, `farm_lob`,
`boxing_guide`, `magic_cabinet`, `paint_reveal`, `pipe`, `kart_race`,
`geology_river`); `cancel()` sets the act state to `done`, which the probe
counts as finished (`scripts/probe_opera_2d_balance.gd`, line 298, and
`scripts/opera_act.gd`, line 182).

- Add an input policy per mode, or retire a mode from the sensor with a stated
  reason; count only `won` as finished.
- **Accept:** each live career reports a finite time for at least one persona,
  or a named retirement reason (`MA-CI-008` acceptance).

### CR4 — Smaller probe and workflow repairs

- The dust-boss step's "45–120 s fun band" is now described as unchecked, while
  `DUST_BUNNY_BOSS_STRESS_TEST_2026-08-02.md` still treats it as the target, and
  4 of 8 personas finish under 45 s. Ask the owner (one question in the next
  cycle) whether to check the band as an advisory verdict or retire it.
- The `--controls` rerun repeats the four control personas already in the
  default roster; the first call's `|| true` hides its status from the step.
- `scripts/probe_sky_lagoon_art.gd` (line 1444) and
  `scripts/probe_castle_shots_2d.gd` (line 124) hard-code engine patch 2; read
  `tools/godot_baseline.json` as `scripts/probe_opera_art.gd` does.
- The legacy human-art diagnostic still saves `01_reef_hub` and
  `02_reef_props`; drop the retired Reef shots.

### CR5 — Record corrections (append-only)

- Roshan decisions in `design/reference/owner_decisions.json` list
  `tools/tests/test_record_owner_decision.py` as their check, although that
  test exercises only a dummy entry; artistic decisions need human review, not
  a test. `ODR-ROSHAN-Q12` drops the owner's "no rule is enforced". The register
  is append-only, so add correction entries with new IDs through the intake
  tool; never edit the originals.
- Mojibake remains in
  `assets_src/cinematics/sky_lagoon_local_motion_v1_2026-09-30/README.md`; add a
  text-hygiene check (mojibake and run-together words such as "61openfindings")
  to the study's document sensor.

### CR6 — A real fresh-agent cold start

Give a fresh agent only the repository and the prompt "add a vet job" (a job
no planner test names). Keep the transcript. **Accept:** a complete plan per
`design/reference/recipes/add_job.md` with no question outside its owner
touchpoints and no other job's content; record the transcript path and hash
in the cycle evidence.

## Build order

CR1 first (it may affect the child), then CR2 and CR3 (they decide what the
next study can see), then CR4–CR6.

## Gates and delivery

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_study_game tools.tests.test_build_study_roadmap tools.tests.test_plan_prompt tools.tests.test_record_owner_decision tools.tests.test_run_advisory_sensor
```

plus `scripts/ci.sh` with the exact Godot 4.7.2 build for any probe or game
change. CI must be green at the exact head before merging into `dev`.

## Stop and escalate if

- A fix would change the Chef design, a rule, finding history or protected art.
- CR2 needs a workflow change the owner has not named.
- A probe would need data from the child's device.

## Report (per package)

Implemented, machine-verified (commands and results at the exact head), and
outstanding visual, device, child and owner gates, separately.
