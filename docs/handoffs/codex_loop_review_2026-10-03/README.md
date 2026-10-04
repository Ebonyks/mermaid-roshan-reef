# Codex handoff — what the loop review left for Codex (2026-10-03)

**Owner requests (2026-10-03):** *"audit, evaluate, and improve"* commit
[`4cb14feb`](https://github.com/Ebonyks/mermaid-roshan-reef/commit/4cb14febc2c5f0074d5ad8386ce66f19f940c84d),
then *"Refine and fix it."*

**From:** Claude. Claude fixed the loop's tooling, recipes, registers and
records in the same change as this handoff (see [REVIEW.md](REVIEW.md),
section 4, items LR-01 to LR-22). **To:** Codex, for the items that need game
code, Godot runs, CI captures or workflow changes. **Owner:** answers the
questions in the cycle `2026-10-03b` report once it is published.

**Status:** `PROPOSED / CANDIDATE`, revision 2 (adds CR0 after the owner's
Chef report; revision 1 was `5374e89c`). Tracking findings:
[`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008)
(CR2–CR4), [`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009)
(CR5, CR6) and [`MA-OPERA-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-001)
(CR0, CR1; reopened to `CONFIRMED_OPEN` on the owner's report). Every package follows `CLAUDE.md`, `AGENTS.md`
and the master-audit development contract (`DL-AUTH-05` to `DL-AUTH-07`).

## Work packages

### CR0 — Chef: the owner's verdict (do first)

The owner, 2026-10-03: *"Chef pours backwards still"* and *"Chef still looks
bad, lots of overdraw"*. Recorded as `ODR-CHEF-VERDICT-20261003`;
`MA-OPERA-001` is reopened. Both causes are in the code and the art.

**Backwards pour.** `assets/opera/worlds/widgets/widget_pour_chef_mover.png`
(256x256) has its spout at the far left (opaque tip at x=22, rows 78–82, about
UV 0.086, 0.312) and its handle at the far right (x=233). `_draw_pour_scene` in
`scripts/opera_gesture_surface.gd` draws it unmirrored into a 140x120 rect,
`_pour_pitcher_rotation()` turns it clockwise (+1.05 rad at full tilt) and
`_pour_spout_point()` starts the stream right of centre (x + 52 + 26t). The jug
tips over its handle with the spout up, and the batter leaves the handle side.

- Draw the Chef jug mirrored (x scale −1 in its transform) so the spout faces
  the bowl, and take the spout from the measured anchor transformed with the
  jug: after mirroring it sits about (+58, −23) px from the centre of the
  140x120 rect, about (+49, +39) at full tilt. Or re-stage the jug to the right
  of the bowl with a counter-clockwise tilt; either way the spout leads.
- **Check:** a probe asserts that at full tilt the stream starts within 6 px of
  the transformed spout anchor and that the spout is the lowest point of the
  rim; a passive control never pours.

**Overdraw.** Every Chef step draws a translucent dark bloom
(`_draw_activity_focus` in `scripts/opera_career_world_2d.gd`: a 416x292 panel
with a 32% navy ellipse, a 12% blue ellipse and an arc) over the painted
kitchen, then code-drawn primitives that duplicate objects the `world_chef`
painting already shows (a big mixing bowl with a whisk, an oven, cake tiers,
a finished cake, frosting bags):

| Step | What is drawn over the painting |
|---|---|
| MIX (`pourt`) | A flat two-colour ellipse bowl, the backwards jug and a two-line stream |
| STIR (`crank_chef`) | A cream playfield rectangle and an ellipse bowl drawn to cover a whisk painted into the old base (`_draw_chef_crank`) |
| BAKE (`oven`) | A brown rectangle oven with a window and a rectangle cake (`_draw_oven`) |
| FROST (`trace_chef`) | An ellipse-and-rectangle cake and a polygon piping bag (`_draw_trace_chef_subject`) |
| TOP (`target_chef`) | Target widget pieces |

- Drop the Chef bloom and the code-drawn duplicates. Make the painted bowl,
  oven and cake the objects each step changes, using isolated cutouts of the
  existing approved art for the changing states (batter level, stirring, baking
  colour, frosting, toppings). Reuse first: the approved cake-state art in
  `assets/chapter2/birthday/` (`chapter2_chef_batter_unstirred.png`,
  `chapter2_chef_batter_stirred.png`, `chapter2_chef_baked_tiers_unstacked.png`,
  `chapter2_chef_stacked_unfrosted_cake.png`,
  `chapter2_chef_frosted_rainbow_cake.png`) and the existing whisk and jug
  movers are candidates. One copy of each object on screen, no new style, no
  redraw for novelty, true Canvas 2D only.
- The same bloom sits behind other careers' cards. Change it only for Chef
  until the owner answers whether to remove it everywhere (one question in the
  next cycle).
- **Check:** the Chef probe counts drawn objects per step (no duplicate bowl,
  oven or cake; no full-panel translucent fill). Codex builds before-and-after
  boards at two aspects for the owner.
- **Accept:** the owner accepts Chef in context on the phone (DL-QA-06), and the
  pour checks in CR0 and CR1 pass.

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

CR0 and CR1 first (the owner's Chef report; they share the pour code), then
CR2 and CR3 (they decide what the next study can see), then CR4–CR6.

## Gates and delivery

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_study_game tools.tests.test_build_study_roadmap tools.tests.test_plan_prompt tools.tests.test_record_owner_decision tools.tests.test_run_advisory_sensor
```

plus `scripts/ci.sh` with the exact Godot 4.7.2 build for any probe or game
change. CI must be green at the exact head before merging into `dev`.

## Stop and escalate if

- A fix would change Chef's steps or story, a rule, finding history or protected
  art, or would need new painted art beyond isolated cutouts of approved art.
- CR2 needs a workflow change the owner has not named.
- A probe would need data from the child's device.

## Report (per package)

Implemented, machine-verified (commands and results at the exact head), and
outstanding visual, device, child and owner gates, separately.
