# Day One room transitions v2 — review and rollback manifest

Status: manual-review candidate; not integrated or pushed
Branch: `codex/day-one-room-transitions-v2-20260829`
Worktree: `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\day-one-room-transitions-v2-20260829`
Exact base: `12ef10080a76609cd116434a790e776053e456c3` (`origin/dev`)
Engine evidence: Godot `4.7.2.stable.official.ed1daf0bf`, Mobile renderer,
1280×720 capture viewport

## Layer map

1. Purpose-built Eagle restoration
   - `assets/castle/day_one_stuffie/baby_eagle_pinned.png`
   - `assets/castle/day_one_stuffie/baby_eagle_standing_idle.png`
   - `assets_src/imagegen/day_one_stuffie_2026-08-22/`
   - `assets_src/imagegen/day_one_stuffie_eagle_idle_2026-08-28/`
2. Shared saved transition framework
   - `scripts/day_one_director.gd`
   - `scripts/main.gd`
   - `scripts/games/day_one_room_polish.gd`
   - `scripts/arena/day_one_castle_dressing.gd`
3. Generated masters, runtime targets, provenance, licenses
   - `assets_src/imagegen/day_one_room_polish_v2_2026-08-29/`
   - `assets/castle/day_one_polish_v2/`
   - `ASSET_LICENSES.md`
4. Bathroom runtime
   - `scripts/games/day_one_bathroom_cleanup.gd`
   - `scripts/games/day_one_bathroom_cleaning.gd`
   - `scripts/games/day_one_dust_bunny_swimmer.gd`
5. Pool runtime/task
   - shared task definition in `scripts/games/day_one_room_polish.gd`
   - existing ordered Pool runtime preserved; timing-only evidence update in
     `scripts/probe_day_one_pool_shots.gd`
6. Stuffie runtime/task
   - `scripts/arena/castle_rooms_25d.gd`
   - `scripts/companion.gd`
7. Art runtime/task
   - `scripts/day_one_art_studio.gd`
8. Probes and reports
   - `scripts/probe_day_one_bathroom_shots.gd`
   - `scripts/probe_day_one_pool_shots.gd`
   - `scripts/probe_day_one_art_studio_shots.gd`
   - `scripts/probe_day_one_stuffie_transition_v2.gd`
   - `audit/day_one_room_transitions_v2_2026-08-29/`

Several production files contain more than one logical layer (`main.gd`, the
shared polish task table, and `ASSET_LICENSES.md`). Literal per-layer commits
would require unsafe partial-hunk staging across state/runtime/provenance
dependencies. The file map above is therefore the reversible layer authority;
the final candidate commit, if created after scoring gates, must remain one
review commit rather than pretending those mixed hunks are independent.

## Dependency graph

```text
DayOneDirector additive save state
  -> ReefMain mount/save callbacks
    -> DayOneRoomPolish one-target overlay
      -> four generated transparent target textures
      -> existing cleaner/wipe/ring/bubble assets
      -> room-specific established activity

Bathroom cleanup -> hidden dirty plate swap -> clean fixtures + reveal
Pool task -> skimmer -> waterfall -> seahorse -> rainbow/Rumi payoff
Stuffie task -> left pin -> right pin -> standing Eagle -> clean room
             -> rescue-only same-identity adoption preview
Art task -> ordered supplies -> ordered visible grime -> paint desk
         -> customizer confirm -> clean room
```

## Apply and revert

The branch/worktree is already the assembled review candidate. No operation on
`dev` or `master` is required for review.

Apply elsewhere only after manual acceptance:

1. Fetch the eventual candidate commit by SHA.
2. Create a new review branch from exact base
   `12ef10080a76609cd116434a790e776053e456c3`.
3. Cherry-pick the candidate commit.
4. Run import, parser/lint, all four focused probes, passive, load, and the
   proportionate Day One probes listed in `TEST_LOG.md`.

Revert after a later cherry-pick:

1. Create a new rollback branch from the integration head.
2. `git revert <candidate-sha>`; never reset `dev` or `master`.
3. Re-import and rerun the same gates.

For the current unintegrated worktree, rollback is simply removal of this
isolated worktree after the owner has preserved any desired captures. No base
branch has been modified.

## Evidence map

Baseline captures:
`C:\Users\Peter\Documents\mermaid-roshan-reef\audit\day_one_gameplay_2026-08-29\visuals\current_4_7_2`

Authoritative candidate captures:

- Pool: `...\visuals\candidate_v3\pool\`
- Bathroom: `...\visuals\candidate_v5\bathroom\`
- Art Studio: `...\visuals\candidate_v7\art\`
- Stuffie Playroom: `...\visuals\candidate_v6\stuffie\`

Superseded candidate folders are rejection evidence only. In particular,
Stuffie v5 contains a cropped picker preview, and Art v6 lets the delayed
Castle Logo activity cover the settled clean frame; neither is final evidence.

## Generated asset integrity

The complete master/runtime hash table, exact prompts, result IDs, reference
roles, normalization, and review status are in
`assets_src/imagegen/day_one_room_polish_v2_2026-08-29/PROVENANCE.md`.
Runtime dimensions are 1024×592, 1024×758, 1024×614, and 1024×614 RGBA;
all meet the project texture constraint.

## Known limitations and external gates

- Owner/manual art and interaction review is pending.
- Intended-child observation is pending and is not represented as completed.
- Lenovo Tab M11 performance/thermal acceptance is pending; desktop Mobile
  rendering does not certify the device.
- `probe_day_one_integration.gd` retains its base legacy failure at
  `complete_tutorial("bathroom")`; the production Bathroom path and focused
  probes pass, and this candidate does not modify that legacy assertion path.
- Exact-engine import produced unrelated tracked `.import` line-ending churn
  in this isolated worktree. It is excluded from the candidate file map and
  must not be staged. A broad restore was deliberately not performed without
  owner authorization.
