# Minigame art coverage gaps — 2026-09-05

This is a source-bound gap inventory, not an exhaustive runtime audit and contains no quality scores. It compares the 56-record audit registry with current source references.

The registry has 56 records. The scan found 45 candidate minigame/adaptor source files, 259 literal resource paths, and 97 dynamic loader sites.

## Unregistered source candidates

- `scripts/castle_career_routes.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_career_scene_adapter.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_director.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_giant_cake_2d.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_party_plan.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_party_table_2d.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_rainbow_candle_2d.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/chapter_two_room_plot.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/games/day_one_bathroom_cleaning.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/games/octagon_stage.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/games/pool_seahorse_rescue_activity.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/games/pool_skimmer_activity.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/games/pool_waterfall_activity.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/kart.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_act.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_competition.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_hotspot_catalog.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_house.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_house_venue_2d.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_imp_clips.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_roshan_actor.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_stage_paths.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_world_backdrop_2d.gd` — no exact registry source record; triage live reachability and capture before grading.
- `scripts/opera_world_hotspot_2d.gd` — no exact registry source record; triage live reachability and capture before grading.

## Dynamic-reference blind spots

- `scripts/games/picture_games.gd`: mature flowers are selected from an array and loaded by concatenated `res://assets/mg/` path; per-state assets are easy to miss in literal-only scans.
- `scripts/games/dust_boss.gd`: Grand Puff art is directory/catalog driven and uses runtime Sprite3D carriers plus state-dependent art; inspect the current origin/dev source and `.worktrees/bunny-battle-rebuild` candidate before any score.
- Pool cleanup families use AtlasTexture subframes (`floating_trash_atlas.png`, Rumi atlases); the atlas file alone does not represent every live frame/contact state.
- Opera career surfaces use catalog-driven and procedural construction across adapters; a script-level record does not prove each asset/state is captured.
- Any `load(path)`/`preload(path)` without a literal `res://` path remains unresolved until the caller’s path construction is traced.

## Highest-priority missing coverage

- Grand Puff boss: current dev has moved beyond the registry revision; refresh source hashes and runtime state inventory before relying on the old “legacy boss” record.
- Day One bathroom/pool cleanup satellites: multiple live art-bearing scripts are not represented as exact registry records or current state captures.
- Fairy, melody, seek, fetch, dolls, treasure, shop, side-scroll and dance families: source satellites and/or atlas/background references need reachability confirmation before scoring.
- Opera adapters and career surfaces: separate dynamic/catalog audit is needed; do not merge their records with non-Opera picture-game evidence.

## Handling

Treat every listed item as `uncaptured/unscored` until current Mobile runtime evidence binds the exact asset and state. The inventory intentionally avoids declaring any item below or above 4.5.
