# Day One room transitions v2 — review and rollback manifest

Status: manual-review candidate; not integrated or pushed

- Branch: `codex/day-one-room-transitions-v2-20260829`
- Worktree: `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\day-one-room-transitions-v2-20260829`
- Exact original base: `12ef10080a76609cd116434a790e776053e456c3` (`origin/dev` at branch creation)
- Reviewed four-room candidate: `dfbba60726be608a21a0563cc17a32b1296c9e00`
- Independent manual-review correction commit: `280b7970`
- Engine: Godot `4.7.2.stable.official.ed1daf0bf`, Mobile renderer,
  1280×720 capture viewport

## Original reviewed layer map (`dfbba607`)

1. Purpose-built Eagle restoration
   - `assets/castle/day_one_stuffie/baby_eagle_pinned.png`
   - `assets/castle/day_one_stuffie/baby_eagle_standing_idle.png`
   - corresponding preserved `assets_src/imagegen/day_one_stuffie*` sources
2. Shared saved transition framework
   - `scripts/day_one_director.gd`, `scripts/main.gd`
   - `scripts/games/day_one_room_polish.gd`
   - `scripts/arena/day_one_castle_dressing.gd`
3. Generated room-target masters/runtime/provenance/licenses
   - `assets_src/imagegen/day_one_room_polish_v2_2026-08-29/`
   - `assets/castle/day_one_polish_v2/`, `ASSET_LICENSES.md`
4. Bathroom, Pool, Stuffie, and Art room-specific runtime/task layers
5. Focused probes and audit report evidence

## Independent manual-review correction layer

This layer applies only on top of `dfbba607`; it does not rewrite that commit.

### Stuffie

- `scripts/castle_logo_studio.gd` — hides both baked room banners behind
  authored wall patches only while dirty; restores personalized banners only
  after settled clean.
- `scripts/arena/castle_rooms_25d.gd` — adds the approved-art ceiling bunny as
  the first ordered, voiced, pointed, immediately saved rescue beat; preserves
  the two pin bunnies and purpose-built pinned/standing Eagle.
- `scripts/probe_day_one_stuffie_transition_v2.gd` — asserts banner state,
  ceiling-bunny presence/removal/save, order, exact Eagle textures, and picker
  contain-fit bounds.
- `assets/castle/day_one_room_corrections_2026-08-30/playroom_banner_cover_{left,right}.png`
- `assets_src/castle/day_one_room_corrections_2026-08-30/playroom_banner_free_generated_source.png`
  plus exact prompt/provenance.

### Craft/Art

- `scripts/day_one_director.gd`, `scripts/main.gd`, and
  `scripts/day_one_art_studio.gd` — eleven ordered saved interactions, one
  responsive/cued target, entry-visible clutter/grime, floor-only rainbow,
  immediate feedback, and stronger settled clean reveal.
- `scripts/arena/castle_rooms_25d.gd` — removes the legacy palette duplicate,
  makes the two foreground table cards the sole owners, and loads conservative
  alpha-clean approved-pixel variants.
- `scripts/probe_day_one_art_studio_shots.gd` and
  `scripts/probe_day_one_art_attack_state.gd` — assert ordered gating, one
  rainbow owner, one palette owner, one table owner per side, zero target/table
  intersection with margins, pointer clearance, saved progression, and clean
  settling.
- `assets/castle/day_one_room_corrections_2026-08-30/craft_table_front_{left,right}_alpha_clean.png`
- `assets_src/castle/day_one_room_corrections_2026-08-30/build_craft_table_alpha_clean.py`
  and `craft_table_alpha_cleanup_manifest.json`.

### Provenance and review package

- `ASSET_LICENSES.md`
- `assets_src/castle/day_one_room_corrections_2026-08-30/PROVENANCE.md`
- `audit/day_one_room_transitions_v2_2026-08-29/{FINAL_REPORT,RUBRIC}.md`
- this manifest, `TEST_LOG.md`, and `CORRECTION_LAYER_2026-08-30.md`

## Dependency graph

```text
dfbba607 reviewed Day One framework
  -> additive save maps in DayOneDirector / ReefMain
    -> Stuffie: banner wall patches -> ceiling bunny -> two pin bunnies
       -> purpose-built standing Eagle -> settled clean banner restoration
       -> same-identity adoption preview
    -> Art: floor rainbow -> six supplies -> three grime targets -> desk
       -> customizer -> bright settled clean
       -> sole table owners use approved-pixel alpha-clean derivatives
```

All new save state is additive and defaulted. Each required interaction saves
before celebration. No protected original is overwritten.

## Craft table provenance authority

No generated table art is accepted or wired.

- Original left card: `assets/flats/castle/rooms/room_craft_room_front_left.png`,
  SHA-256 `466d88d72a245fabe0ef6810796aca8eb7aba6c66cbac031eb2e5ddf5aa68d9a`.
- Original right card: `assets/flats/castle/rooms/room_craft_room_front_right.png`,
  SHA-256 `41167d28ce5a519e0aee05239f782accf8f4137cf0c002189e8d1456a6c17871`.
- Exact approved RGB source: `assets/flats/castle/rooms/room_craft_room.png`,
  SHA-256 `916522a6fab6691866e8ff768056a5725bfbb76044dba869935eb7b585420eae`.
- Reviewed polygon authority:
  `assets_src/castle/depth_cards/static_depth_card_refinement.json`, SHA-256
  `64dff9ee9ff1801b49bea9a242c2c6b2c041115c6dbc872a046a36e8c62b0a58`.
- V3 left runtime: SHA-256
  `7719f14fd566179f9175e3cfaea80371235aea1ba5fb6e32cda405a1b81f663c`.
- V3 right runtime: SHA-256
  `0edb1e06cee535887ceea4e3e449f6bfe08d7919a806fe333b67b28ab19ef104`.

The deterministic method recovers RGB only from the exact approved room crop,
preserves the source alpha core and two-pixel antialias fringe, unions only the
already reviewed broad body polygons, and zeros unintended peripheral alpha
and hidden RGB. The originals remain unchanged.

## Apply and exact rollback

Review in place requires no operation on `dev` or `master`.

Apply after owner acceptance:

1. Create a branch at `dfbba60726be608a21a0563cc17a32b1296c9e00`.
2. `git cherry-pick 280b7970`
3. Run the gates in `TEST_LOG.md`.

Revert only this independent correction layer after a later cherry-pick:

`git revert 280b7970`

Never reset or directly modify `dev` or `master` for rollback.

## Evidence map

- Baseline: `C:\Users\Peter\Documents\mermaid-roshan-reef\audit\day_one_gameplay_2026-08-29\visuals\current_4_7_2`
- Pool authoritative: `visuals/candidate_v3/pool/`
- Bathroom authoritative: `visuals/candidate_v5/bathroom/`
- Stuffie authoritative: `visuals/correction_v2/stuffie/`
- Art authoritative: `visuals/correction_v3/art/`
- Art table isolation: `visuals/correction_v3/art_layer_isolation/01_table_ownership_isolation.png`

Art correction v1 and v2 are rejected. V2 exhibited torn/scalloped derived
table alpha edges. The generated table-edit candidate is excluded and was
never wired. Stuffie candidate v5 is rejected for cropped Eagle contain-fit;
only correction v2 is authoritative.

## Known limitations and external gates

- Owner/manual art and interaction review is pending.
- Intended-child observation is pending and not claimed.
- Lenovo Tab M11 frame-time, thermal, memory, and touch acceptance are pending.
- The canonical legacy `probe_day_one_integration.gd` retains one unrelated
  stale `complete_tutorial("bathroom")` route assertion; focused paths pass.
- Exact-engine import creates tracked `.import` line-ending/importer churn.
  Those tracked paths are excluded and restored to `HEAD` before commit; only
  new correction-asset import metadata belongs to the correction layer.
