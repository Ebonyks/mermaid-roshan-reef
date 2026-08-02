# Decommission manifest — tranche 1

Compiled 2026-08-02. Read `README.md` in this directory first.

**Staleness measure.** "Last edit" is the date of the last *non-merge* commit
touching the file (`git log -1 --no-merges --format=%cs -- <path>`). Merge dates
are useless here: the graphics fork merges `dev` constantly, so `git log -1`
without `--no-merges` reports 2026-07-25 or 2026-08-01 for files nobody has
opened in three weeks.

**Cut line.** Tranche 1 quarantines work last edited **2026-07-22 or earlier**
(≥11 days; the bulk of it is the 2026-07-19 cohort at ≥14 days) **and** made
obsolete by a later owner decision. Age alone was not sufficient — several
untouched files are living specs and stayed put (see § Kept).

**Superseding decisions.**

| Date | Decision | Kills |
| --- | --- | --- |
| 2026-07-27 | Game redesigned as a 2.5D promenade world on the E2 SideScrollStage; Codex-painted background flats become the primary art channel (`GAME_REDESIGN_2P5D_2026-07-27.md`) | the 3D zone-art and Blender/Meshy world pipeline |
| 2026-07-27 | gen2 Meshy 3D character migration **PAUSED**; cutouts/billboards are the character medium again | the whole gen2 staging tree and its handoffs |
| 2026-07-11 | Renderer is "mobile" on every platform; Forward+-only effects dormant behind a guard | the cel post-grade plan |

---

## Group 1 — `docs/3d-character-pipeline/` (8 files)

The 2D-billboard → 3D character conversion, authored 2026-06-25 and extended
through July. Paused by the 2026-07-27 owner decision; cutouts are the shipped
medium again.

| File | Last edit |
| --- | --- |
| `CHARACTER_PIPELINE.md` | 2026-07-19 |
| `CHARACTER_RUNBOOK.md` | 2026-07-19 |
| `CHARACTER_CUSTOMIZATION.md` | 2026-07-19 |
| `ART_3D_BATCH_01.md` | 2026-07-19 |
| `ART_3D_BATCH_02.md` | 2026-07-19 |
| `NORTHERN_BLENDER_HANDOFF_FOR_CLAUDE_2026-07-20.md` | 2026-07-20 |
| `CLAUDE_SKY_LAGOON_BLENDER_CONTINUATION_2026-07-20.md` | 2026-07-21 |
| `CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md` | 2026-07-21 |

**Blast radius:** none. No `scripts/`, `scenes/`, or workflow reference.

**Left behind on purpose:** `NPC_3D_WORKORDER_2026-07-19.md` and
`ART_3D_CONVERSION_MANIFEST.md`. The first is cited by name in `CLAUDE.md`, the
second is the ledger of which `.glb`s actually landed — and `CLAUDE.md` says
landed `.glb`s stay until their zone migrates. Quarantining either needs an
owner-approved `CLAUDE.md` edit. **Tranche 2 candidates.**

## Group 2 — `docs/art-generation-passes/` (24 files)

One-shot generation, remediation, scoring, and texture-regen batch logs from the
2026-07-13 → 2026-07-19 Nano-Banana/pass-35 era. Each records a run that has
already landed or been rejected; none is a standing spec. Superseded as a
channel by `CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md`.

All 24 last edited **2026-07-19**.

`ART_AUDIT_2026-07-18.md`, `ART_GAME_WIDE_PASS35_AUDIT_2026-07-16.md`,
`ART_GAP_WORKORDER_2026-07-18.md`, `ART_GENERATION_BATCH_01.md`,
`ART_GENERATION_BATCH_02.md`, `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`,
`ART_LANDMARK_REBUILD.md`, `ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md`,
`ART_PASS35_PROMPTS.md`, `ART_REMEDIATION_BATCH_04.md`,
`ART_RESIDUAL_LOW_SCORE_AUDIT.md`, `ART_RUNTIME_REMEDIATION_BATCH_03.md`,
`ART_SCORE3_REBUILD_AUDIT.md`, `ART_SCORING_GOVERNANCE_2026-07-18.md`,
`ASSET_AUDIT.md`, `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md`,
`COLOR_CONSISTENCY_AUDIT.md`, `FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md`,
`FULL_TEXTURE_REGEN_IMPLEMENTATION_REVIEW_2026-07-18.md`,
`FULL_TEXTURE_REGEN_POST_STRESS_ANALYSIS_2026-07-18.md`,
`NB_AI_STUDIO_EXPORT.md`, `NB_TEXTURE_PLAN.md`,
`PARALLEL_ART_WORK_REVIEW_2026-07-16.md`, `TEXTURE_SOURCE_AUDIT.md`

**Blast radius:** none in shipped code. `tools/build_art_pass35.py` and
`tools/build_low_score_batch_01.py` implement these passes but read no path from
this wing — they write to `assets/props/gen2/`, which is **live shipped art** and
was not touched.

## Group 3 — `docs/zone-art-3d-era/` (18 files)

Per-zone art and quality audits written against the 3D diorama build. Every zone
named here is either already rebuilt as 2.5D flats or queued for it, and each has
a live successor.

| File | Last edit | Superseded by |
| --- | --- | --- |
| `NORTHERN_WORLD_ART_AUDIT_2026-07-17.md` | 2026-07-19 | 2.5D redesign charter |
| `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md` | 2026-07-20 | 2.5D redesign charter |
| `NORTHERN_ASSET_BATCH_02.md` | 2026-07-19 | 2.5D redesign charter |
| `DUNGEON_ART_REBUILD_AUDIT_2026-07-16.md` | 2026-07-19 | 2.5D redesign charter |
| `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` | 2026-07-20 | 2.5D redesign charter |
| `REEF_REDESIGN_AUDIT_2026-07-16.md` | 2026-07-19 | `WORLD_MAP_2026-07-27.md` |
| `OBJECT_PLACEMENT_AUDIT_2026-07-17.md` | 2026-07-19 | `LIVING_WORLD_STAGE_AUDIT_2026-07-27.md` |
| `CASTLE_PEARL_ART_AUDIT_2026-07-18.md` | 2026-07-19 | `FABLE_CASTLE_2P5D_LAYER_AUDIT_2026-07-26.md` |
| `EMBER_FORTRESS_GRAPHICS_AUDIT_2026-07-21.md` | 2026-07-21 | zone not yet migrated; audits predate the flats channel |
| `CLAUDE_EMBER_FORTRESS_GRAPHICS_HANDOFF_2026-07-21.md` | 2026-07-21 | as above |
| `EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22.md` | 2026-07-21 | as above |
| `EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md` | 2026-07-21 | as above |
| `SKY_LAGOON_ART_AUDIT_2026-07-19.md` | 2026-07-19 | `SKY_LAGOON_CONGRUENCY_REBUILD_2026-07-27.md` |
| `SKY_LAGOON_STYLE_COHESION_AUDIT_2026-07-19.md` | 2026-07-19 | as above |
| `CLAUDE_SKY_LAGOON_DESIGN_HANDOFF_2026-07-19.md` | 2026-07-19 | as above |
| `SKY_LAGOON_QUALITY_AUDIT_2026-07-20.md` | 2026-07-21 | as above |
| `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | 2026-07-21 | `SKY_LAGOON_REDUCTIVE_HANDOFF_2026-07-28.md` |
| `SKY_LAGOON_PNW_RUNTIME_IMPLEMENTATION_2026-07-21.md` | 2026-07-21 | as above |

**Blast radius:** none. `assets/ember_fortress/`, `assets/northern/`,
`assets/dungeon/`, `assets/sky_lagoon/` and their scripts were **not** moved —
only the prose about them. The Ember Fortress zone is stale (assets last touched
2026-07-21) but still built by `scripts/ember_fortress.gd`; it is a **tranche 2
gameplay question for the owner**, not an art-doc question.

## Group 4 — `docs/opera-3d-flat-era/` (7 files)

Opera is the most active area in the repo (work landing 2026-08-01/02), so only
the pre-2.5D lineage moved. The 2026-07-24/25 2P5D documents stayed live.

| File | Last edit | Superseded by |
| --- | --- | --- |
| `CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21.md` | 2026-07-21 | `CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md` (kept) |
| `CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md` | 2026-07-25 | as above |
| `OPERA_HOUSE_FLAT_ART_AUDIT_2026-07-21.md` | 2026-07-21 | `OPERA_2D_REBUILD_2026-08-01.md` |
| `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md` | 2026-07-21 | as above |
| `OPERA_JOB_FLAT_PROTOTYPE_PLAN_2026-07-21.md` | 2026-07-21 | as above |
| `OPERA_ASSET_REQUESTS_2026-07-19.md` | 2026-07-25 | `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` |
| `CODEX_ASSET_REQUESTS_2026-07-21.md` | 2026-07-21 | as above |

**Blast radius:** none.

## Group 5 — `docs/legacy-engine-audits/` (12 files)

Audits and workorders against build generations that no longer exist.

| File | Last edit | Why |
| --- | --- | --- |
| `AUDIT_3_0.md` | 2026-07-19 | 3.0 audit; its plan shipped as `DESIGN_3_0.md` |
| `DESIGN_3_0.md` | 2026-07-19 | 3.0 changelog, long since shipped |
| `AUDIT_REPAIR.md` | 2026-07-19 | repair pass, complete |
| `AUDIT_UPGRADE.md` | 2026-07-19 | upgrade pass, complete |
| `GAME_AUDIT_v3_49.md` | 2026-07-19 | audit of build v3_49 |
| `CONVERSATION_AUDIT.md` | 2026-07-19 | audited June 13 2026 against the old reef2 build |
| `CODE_AUDIT_2026_07.md` | 2026-07-19 | main.gd was ~8.9k lines at audit time; superseded by the Phase 7 extractions |
| `CAMERA_AUDIT_2026_07.md` | 2026-07-19 | 3D-orbit camera era; 2.5D stage uses the SideScrollStage rig |
| `JOLT_PHYSICS_AUDIT_2026-07-18.md` | 2026-07-19 | engine-choice audit; `PHYSICS_ENGINE.md` (kept) is the live spec |
| `CEL_SHADING.md` | 2026-07-19 | cel post-grade is dormant behind a rendering-method guard (mobile-renderer decision) |
| `ZELDA_GAMEPLAY_WORKORDER_2026-07-18.md` | 2026-07-19 | pre-redesign gameplay workorder |
| `CC0_REPLACEMENT_WORKORDER_2026-07-22.md` | 2026-07-22 | CC0 sweep complete; `ASSET_LICENSES.md` (kept, live) is the standing record |

**Blast radius:** none. `scripts/physics.gd` and `PHYSICS_ENGINE.md` stay live.

---

## Group 6 — `data/` (899 MB)

| Path | Was | Size | Last edit | Why |
| --- | --- | --- | --- | --- |
| `gen2-meshy-3d-pipeline/` | `gen2/` | 744 MB | 2026-07-19 | The paused Meshy 3D staging tree: raw Meshy output, turnarounds, prompts, NPC sources, UI prototypes. Migration PAUSED 2026-07-27. |
| `oceanfft-demo-scene/` | `example/` | 73 MB | 2026-07-19 | Upstream demo scene for the ocean-FFT addon, which is itself disabled. Zero references. |
| `audit-snapshots/` | `audit/{full_regen_2026-07-18, runtime_shots_2026-07-16, ember_runtime_2026-07-21}` | 28 MB | 2026-07-19 / 07-19 / 07-21 | Frozen render/ledger snapshots from completed audit passes. `audit/` is `.gitignore`d as a scratch dir; these were tracked historically. |
| `style_review_score3/` | `assets_src/style_review_score3/` | 21 MB | 2026-07-19 | One-off score-3 style review batch, resolved. |
| `art-rollback-snapshots/` | `backups/` | 18 MB | 2026-07-19 | Ten `art_pre_*` pre-change copies dated 2026-07-15 → 07-19. Git history plus the weekly CI backup bundle already cover rollback; these are a third copy. |
| `reference-pdfs/` | `tmp/pdfs/` | 7.3 MB | 2026-07-19 | Reference PDFs in a scratch dir. Zero references. |
| `style_review_batch_04/` | `assets_src/style_review_batch_04/` | 6.3 MB | 2026-07-19 | One-off batch-04 style review, resolved. |
| `tessarakkt.oceanfft/` | `disabled_addons/tessarakkt.oceanfft` | 2.2 MB | 2026-07-19 | Marked DISABLED in `CLAUDE.md` since Phase 0, dead code already removed. |

**Blast radius — read before deleting.**

- **Shipped code: none.** Confirmed no `scripts/`, `scenes/`, or `project.godot`
  reference. In particular the runtime `gen2` paths are `res://assets/props/gen2/…`
  (live shipped art, **not** moved) — not the top-level `gen2/` staging tree.
- **Probes: none.** `probe_art_audit_35.gd` and `probe_penguin_beak.gd` load
  `res://assets/props/gen2/*.glb` only.
- **Dev tools: 7 broken by the `gen2/` move.** These are pipeline tools for the
  paused migration and were deliberately left in `tools/` rather than moved:
  `meshy_pipeline.py`, `gen2_batch.py`, `gen2_turnaround.py`,
  `gen2_audit_aggregate.py`, `gen2_rainbow_road.py`, `prep_npc_sources.py`,
  `roshan_v2_retarget.py`. Also `stress_full_texture_regen.py` (globs `ROOT/gen2`).
  Repoint or decommission them in tranche 2.
  `build_art_inventory.py` mentions `gen2` only as a string in a classification
  table — cosmetic, not a break. `survey_aquatic.py` and `rig_animate_aquatic.py`
  point outside the repo entirely and are unaffected.
- **`.gitignore`:** `/tmp/fairy_v2/` still names a path under a now-absent `tmp/`.
  Harmless — `tools/audit_fairy_art_v2.py` recreates `tmp/fairy_v2/` on its next
  gate run and the ignore rule matches again. Fairy tooling is owner-protected and
  was not touched.
- **`export_presets.cfg`:** both presets gained `decommissioned/*`. Without it the
  wing would have shipped in the APK — the old filter matched `gen2/*`,
  `example/*`, `backups/*`, `tmp/*` by literal path.

---

## Cross-references from kept documents

27 kept documents mention a quarantined filename in prose. Nothing breaks —
these are bare filenames, not resolved links, and the files still exist under
`decommissioned/docs/<group>/`. They were **not** rewritten:

- **`ASSET_LICENSES.md`** accounts for most of them. It is the per-asset
  provenance record required by `CLAUDE.md`, and its "modifications" fields cite
  the audit that authorised each change. Those citations are historical fact;
  editing 170 KB of licensing provenance to chase a directory move would risk
  the record for no gain.
- `ART_STYLE_GUIDE.md`, `ART_STYLE_AUDIT.md`, `ART_3D_CONVERSION_MANIFEST.md`,
  `REEF_FLORA.md`, the 2026-07-24 opera documents, and two files under `docs/`
  hold the rest.

**Rule if you delete tranche 1:** resolve these mentions first, or the provenance
trail in `ASSET_LICENSES.md` starts pointing at nothing. That is the strongest
argument for auditing this wing rather than deleting it wholesale.

## Audio — nothing decommissioned

Audio was examined and **deliberately left entirely intact**.

- `assets/audio/voices/` (147 files) is irreplaceable recorded family voice per
  `CLAUDE.md`, and was last touched 2026-08-01 — it is live, not stale.
- `assets/audio/castle/` (14 files) last touched 2026-08-01. Live.
- `assets/audio/music/` (15 files) last touched 2026-07-19, which reads as stale,
  **but is not**: these are stable finished tracks, not work-in-progress.
- A naive by-basename reference scan reports 165 of 176 audio files as
  "unreferenced". **That result is wrong and must not be acted on.**
  `scripts/audio_director.gd` builds every path at runtime:

      var p1 := "res://assets/audio/voices/" + key + ".ogg"
      var mpath := "res://assets/audio/music/" + fname + ".ogg"

  A grep for `daddy1.ogg` finds nothing because no source file contains that
  string.

**Resolved 2026-08-02.** That audit has now been done properly — see
`AUDIO_AUDIT.md`, generated by `tools/audit_audio_usage.py` (re-runnable).
It reconstructs the vocabulary from call arguments, array-literal picks,
`_speaker_key` routing, the opera data tables and the friend roster, and labels
all 186 files by *why* they are or aren't reached.

Outcome: **169 of 186 files (91%) are reached by the running game** — the naive
scan's 94%-dead was inverted. Of the 17 that aren't:

- 3 are Daddy Mermaid recordings that exist but can never play because the
  filename (`daddy1/2/3.ogg`) is not a name the resolver can generate.
- 4 are Wacky lines shadowed by `_speaker_key` testing `"chuck"` before
  `"wacky"` against the roster entry `"Wacky and Chuck"`.
- 4 are minigame music tracks whose games never call `_play_music`.
- 4 are unused lines/base clips worth keeping as fallbacks.
- **2 are true orphans** (`buzz.ogg`, `fart.ogg`), a few KB in total.

So the deletable audio in this project is two sound effects. Everything else
labelled "unused" is a naming or routing defect — fixing it makes existing
recordings audible. No audio is quarantined and none should be.

## Kept despite being stale

Untouched for ≥2 weeks but **not** quarantined, with reasons:

| File | Last edit | Why kept |
| --- | --- | --- |
| `KART_FEEL.md`, `RACE_ENGINE.md`, `RACE_FEEL_WORKORDER.md` | 2026-07-19 | Owner-protected (kart racing). `RACE_FEEL_WORKORDER.md` is also cited by `.github/workflows/race-feel.yml`. |
| `assets/kart/`, `assets/fairy/`, `assets_src/fairy_v*` | 2026-07-19 / 07-27 | Owner-protected. |
| `MEDALS.md`, `STUFFIE_COMPANIONS.md` | 2026-07-19 / 07-22 | Cited by name in `CLAUDE.md`; describe shipped systems. |
| `NPC_3D_WORKORDER_2026-07-19.md`, `CODEX_NEXTGEN_OBJECTS_2026-07-25.md` | 2026-07-19 / 07-26 | Cited by name in `CLAUDE.md` / `AGENTS.md`. Tranche 2, needs a governing-file edit first. |
| `ART_STYLE_GUIDE.md` | 2026-07-19 | Declares itself the style authority. Superseding it is an owner call, not a cleanup call. |
| `ART_ASSET_LIBRARY.md` | 2026-07-19 | The index for finding art, including everything in this wing. Its paths now need a refresh — **tranche 2 fix**. |
| `PHYSICS_ENGINE.md`, `REEF_FLORA.md` | 2026-07-19 | Live specs for `scripts/physics.gd` and the shipped flora set. |
| `attic/gabby/` | 2026-07-19 | Already quarantined at the path `CLAUDE.md` names (IP hold). Moving it would break that pointer. |
| `art_library/candidates/` | 2026-07-19 | `ART_ASSET_LIBRARY.md` states art is never discarded merely for being unused; this is that library. |
| `assets/book/` | 2026-07-19 | Irreplaceable book art. |
| `assets/terrain/`, `assets/collectibles/`, `assets/icon/`, `assets/fable_kit/` | 2026-07-19 | Stale but shipped and referenced. |

## Tranche 2 — proposed, needs owner sign-off

1. Repoint or decommission the 8 `tools/*.py` broken by the `gen2/` move.
2. Refresh paths in `ART_ASSET_LIBRARY.md`.
3. Decide on `NPC_3D_WORKORDER_2026-07-19.md` + `ART_3D_CONVERSION_MANIFEST.md`
   (requires a `CLAUDE.md` edit, which `SECURITY.md` classes as high-risk).
4. **Gameplay question, not cleanup:** is the Ember Fortress zone still in the
   game? Its assets and scripts are live but untouched since 2026-07-21.
5. `assets_src/blender/` (562 MB, last edit 2026-07-29) — mostly the paused 3D
   pipeline, but recent enough that it needs an explicit owner call.
6. Delete tranche 1 outright once audited.
