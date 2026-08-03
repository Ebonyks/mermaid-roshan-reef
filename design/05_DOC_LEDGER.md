# Master design — document ledger

_Status of all 149 markdown documents, 2026-08-02. No file was moved,
renamed or deleted; this table is the index that makes them navigable._

**Legend**

| | Meaning |
|---|---|
| 🟢 | **AUTHORITATIVE** — still binding. Read it before acting in its area. |
| 🔵 | **SUPPORTING** — a living reference, ledger or runbook. Not a design decision. |
| 🟡 | **SUPERSEDED** — a later document replaced its conclusions. Named. |
| ⚪ | **HISTORICAL RECORD** — a completed pass, inventory or one-time analysis. Read for *why*, never for *what to do next*. |

---

## Authority and operations

| Doc | | Note |
|---|---|---|
| `CLAUDE.md` | 🟢 | Session contract. **Conflicts with `AGENTS.md` — [OW-1](04_OPEN_WORK.md#ow-1).** |
| `AGENTS.md` | 🟢 | Session contract. Newer layout/build sections, **stale art direction**. |
| `SECURITY.md` | 🟢 | Threat model and binding agent rules. Summarized in 03 §8. |
| `BACKUP.md` | 🟢 | Four backup layers and every restore recipe. |
| `ASSET_LICENSES.md` | 🟢 | The licence ledger. One line per asset, same commit. 1,035 rows. |
| `WORKFLOW_BRANCHING_2026-07-18.md` | 🟢 | The dev/master promotion rule. Summarized in 03 §6. |
| `docs/ANDROID_RELEASE.md` | 🟢 | Signing key safety — a key change destroys the child's save. |
| `ASSET_AUDIT.md` | ⚪ | 2026-06-25 CC0 audit + the network-blocker decision. Superseded in direction by `CC0_REPLACEMENT_WORKORDER_2026-07-22.md`. |

## Game design lineage

| Doc | | Note |
|---|---|---|
| `GAME_REDESIGN_2P5D_2026-07-27.md` | 🟢 | **The current charter.** Everything in 01 §2 comes from here. |
| `WORLD_MAP_2026-07-27.md` | 🟢 | Geography **proposal**; four owner decisions open ([OW-13](04_OPEN_WORK.md#ow-13)). Its "the world is not stitched" finding stands regardless. |
| `MINIGAME_ENGINES.md` | 🟢 | The MiniGame contract + engine set E1–E4/K1/K2. Steps 2–7 open. |
| `MEDALS.md` | 🟢 | Bronze/silver/gold rules and the full tier table. |
| `STUFFIE_COMPANIONS.md` | 🟢 | The companion wing: roster, unlock, care loop, battles. |
| `STUFFIE_PLAYROOM_RESCUE_GUIDE_2026-07-29.md` | 🟢 | The wordless stuffie tutorial (Baby Eagle rescue). |
| `DAY_ONE_CASTLE_INTRO_PLAN_2026-08-03.md` | 🟢 | **The Day One plan** — arrival, the dirty castle, the per-room encounter table, purposes for the six stub rooms, the eight build phases, and the deactivation contract for the Codex art landed with it. Supersedes the Codex `dirty_castle_stage.gd` runtime shell (art and narrative kept, §2.3). |
| `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` | 🟢 | Age-4 difficulty read + the unbuilt lock-and-key design ([OW-16](04_OPEN_WORK.md#ow-16)). |
| `ZELDA_GAMEPLAY_WORKORDER_2026-07-18.md` | 🟢 | Unbuilt verb/structure roadmap ([OW-17](04_OPEN_WORK.md#ow-17)). |
| `FABLE_INTERACTION_HANDOFF_2026-07-25.md` | 🟢 | The interactable state machine and data contract. Long but current. |
| `TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25.md` | 🟢 | Hybrid/Classic touch modes; the grammar the charter kept. |
| `RACE_FEEL_WORKORDER.md` | 🟢 | Slide-racer feel diagnosis + iterate-until-green protocol. |
| `KART_FEEL.md` | 🟢 | Kart-class comparative rubric; gated by `probe_kart_feel`. |
| `AUDIT_UPGRADE.md` | 🟢 | The production-quality intervention plan. Its finding #1 is [OW-21](04_OPEN_WORK.md#ow-21). |
| `AUDIT_3_0.md` | ⚪ | June 2026 pre-3.0 critical audit. Its criticals (no save, no ending) are long fixed. |
| `DESIGN_3_0.md` | ⚪ | What 3.0 changed and why. Origin of the Mobile-renderer and stretch decisions. |
| `CONVERSATION_AUDIT.md` | ⚪ | June 2026 discussed-vs-shipped checklist. |
| `GAME_AUDIT_v3_49.md` | ⚪ | Comprehensive v3_49 design+code audit with an emulated playthrough. |
| `AUDIT_REPAIR.md` | ⚪ | Closes the 2026-07-15 repair phase (agency, no-fail, touch, save safety). |
| `CODE_AUDIT_2026_07.md` | 🔵 | Bugs B1–B9 all closed; **§4 structural debt is still live** (03 §9). |
| `CAMERA_AUDIT_2026_07.md` | 🔵 | Camera inventory + the `camera_kit.gd` redesign. Largely landed. |
| `JOLT_PHYSICS_AUDIT_2026-07-18.md` | 🔵 | Why Jolt stays garnish-only; overworld feel tiers. |
| `LIGHTING_SHADER_AUDIT_2026-07-18.md` | 🔵 | Mobile-renderer shader inventory + the Lighting Lab; ranked look shifts. |
| `COLOR_CONSISTENCY_AUDIT.md` | ⚪ | 2026-07-15 overexposure findings in six bright contexts. |

## Engine references

| Doc | | Note |
|---|---|---|
| `PHYSICS_ENGINE.md` | 🟢 | `ReefPhysics` — the analytic engine everything moves through. |
| `HIT_ENGINE.md` | 🟢 | The shared enemies-get-hit pipeline. |
| `RACE_ENGINE.md` | 🟢 | `kart.gd` as a reusable config-driven racer (E4). |
| `VISUAL_AUDIT_TOOL.md` | 🟢 | The audit tool's contract, expansion rules and stress protocol. |
| `MEDALS.md`, `MINIGAME_ENGINES.md` | 🟢 | (listed above) |

## Art doctrine

| Doc | | Note |
|---|---|---|
| `ART_STYLE_GUIDE.md` | 🟢 | **The style law.** Shape/line/value/colour language + the sampled palette. |
| `ART_SCORING_GOVERNANCE_2026-07-18.md` | 🟢 | What a score means; supersedes "book art = automatic 5/5". |
| `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` | 🟢 | The Sprite3D structural contract and motion budget. |
| `CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md` | 🟢 | The layer format and per-zone shot lists. Batches 3–6 not yet started. |
| `ART_ASSET_LIBRARY.md` | 🔵 | Where art lives: `assets/`, `assets_src/`, `gen2/`, `attic/`. |
| `CC0_REPLACEMENT_WORKORDER_2026-07-22.md` | 🟢 | The one-at-a-time original-art replacement handoff ([OW-18](04_OPEN_WORK.md#ow-18)). |
| `VISUAL_DESIGN_AUDIT_2026-07-28.md` | 🟢 | The redesign's first-48-hours audit. Its four ERRORs are OW-2..OW-5. |
| `CEL_SHADING.md` | ⚪ | The 2026-06-26 Wind Waker decision that set the rendering register. |
| `ART_STYLE_AUDIT.md` | ⚪ | 2026-07-13 baseline style audit ("strong heart, uneven perimeter"). |
| `ART_FULL_INVENTORY.md` | ⚪ | 2026-07-14 directory-level inventory of 487 visual files. |
| `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md` | 🟡 | Rubric superseded by `ART_SCORING_GOVERNANCE_2026-07-18.md`. Its 0–4 caps survive. |
| `ART_GAME_WIDE_PASS35_AUDIT_2026-07-16.md` | ⚪ | The 110-asset pass-3.5 rebuild with runtime evidence. |
| `ART_PASS35_PROMPTS.md` | ⚪ | Generation provenance for that pass. |
| `ART_RESIDUAL_LOW_SCORE_AUDIT.md` | 🟡 | Its "no remaining 0–2/5 roles" conclusion was corrected by `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`. |
| `ART_REMEDIATION_BATCH_04.md`, `ART_RUNTIME_REMEDIATION_BATCH_03.md`, `ART_SCORE3_REBUILD_AUDIT.md`, `ART_LANDMARK_REBUILD.md` | ⚪ | Completed 2026-07-14/15 remediation passes. |
| `ART_3D_BATCH_01.md`, `ART_3D_BATCH_02.md`, `ART_3D_CONVERSION_MANIFEST.md` | ⚪ | Blender mesh passes. Channel deprioritized by the 2026-07-27 decision. |
| `ART_GENERATION_BATCH_01.md`, `ART_GENERATION_BATCH_02.md` | ⚪ | Review blocks, never automatic runtime replacements. |
| `ART_AUDIT_2026-07-18.md` | ⚪ | Four-day-window repeat audit. |
| `ART_GAP_WORKORDER_2026-07-18.md` | 🔵 | What does NOT exist yet — still a useful gap list, line refs stale. |
| `ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md` | ⚪ | Cross-history critique of everything below 5/5. |
| `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md` | ⚪ | Directive audit for the regen-pack iteration; P0 was a QA-integrity fix. |
| `FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md`, `FULL_TEXTURE_REGEN_IMPLEMENTATION_REVIEW_2026-07-18.md`, `FULL_TEXTURE_REGEN_POST_STRESS_ANALYSIS_2026-07-18.md` | ⚪ | The isolated 167-candidate regeneration pack: baseline, independent review, post-stress result. |
| `NB_AI_STUDIO_EXPORT.md`, `NB_TEXTURE_PLAN.md`, `TEXTURE_SOURCE_AUDIT.md` | ⚪ | The nano-banana texture era. Superseded as a channel by Codex flats. |
| `OBJECT_PLACEMENT_AUDIT_2026-07-17.md` | 🔵 | Ecosystem placement rules (right biome, believable support, reserved footprints). Still a good check. |
| `PARALLEL_ART_WORK_REVIEW_2026-07-16.md` | ⚪ | One-time overlap arbitration between concurrent art branches. |
| `REEF_FLORA.md` | 🔵 | The marine-first flora roster and its licensing record. |
| `COLOR_CONSISTENCY_AUDIT.md` | ⚪ | (listed above) |

## Zone: Pearl Castle

| Doc | | Note |
|---|---|---|
| `CASTLE_INTERACTION_AUDIT_2026-08-01.md` | 🟢 | **Current castle interaction authority.** 38 props, 8 rooms, semantic (not whole-card) interactions, alpha/depth repair, blocking audit contract. |
| `CASTLE_ROOM_LED_CODEX_IMPLEMENTATION_2026-07-28.md` | 🟢 | Room-led hub; **2026-08-01 correction: storybook doors are the sole room route, the elevator is removed.** |
| `FABLE_CASTLE_ANIMATION_INTERACTIVITY_HANDOFF_2026-07-29.md` | 🟢 | The ambient-motion + interactivity brief the castle work executes. |
| `CASTLE_DUST_BUNNY_SPAWN_GUIDE_2026-07-29.md` | 🟢 | The Main Hall dust-bunny spawn table and clear rules. |
| `FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md` | 🔵 | The 4.5/5 item-style gate and the 28-item inventory. |
| `FABLE_CASTLE_2P5D_LAYER_AUDIT_2026-07-26.md` | 🔵 | Layer/navigation audit; **resolution-nonconforming** under the native-2K amendment. |
| `FABLE_CASTLE_2K_REGEN_HANDOFF_2026-07-26.md` | 🔵 | The native-2K regeneration contract; **blocked at the generator's long-edge gate.** |
| `FABLE_CASTLE_MAIN_HALL_PROP_COMPATIBILITY_AUDIT_2026-07-28.md` | ⚪ | Rejects the doorway-vignette pass; one hub vocabulary. |
| `FABLE_CASTLE_VISUAL_POLISH_INTERVENTION_2026-07-28.md` | ⚪ | Hierarchy-not-topology polish direction. |
| `CASTLE_PEARL_ART_AUDIT_2026-07-18.md` | ⚪ | The 3D-era castle art rebuild. Predates the 2.5D castle. |
| `audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md` | 🔵 | Corrected 2026-08-01: seam/tone/registration evidence for the Main Hall tiles. |
| `audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md` | 🟡 | Superseded by the seam/tone audit above for fixtures, junctions and tone. |

## Zone: Sky Lagoon

| Doc | | Note |
|---|---|---|
| `SKY_LAGOON_CONGRUENCY_REBUILD_2026-07-27.md` | 🟢 | The 3×1 promenade rebuild; `SCENE_CONGRUENCY 10/10` gate. |
| `SKY_LAGOON_REDUCTIVE_HANDOFF_2026-07-28.md` | 🟢 | The 6144×2048 clean plate reconstructed as a 6×2 card grid — the per-screen resolution rule in practice. |
| `SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27.md` | 🟢 | Why the 1024×341 downscale was removed; native-master preservation. |
| `SKY_LAGOON_LIVING_CARD_V3_IMPLEMENTATION_AUDIT_2026-07-29.md` | 🔵 | The living-card pilot that produced the design language. |
| `docs/audits/SKY_LAGOON_ANIMALS_2026-08-01.md` | 🔵 | Ambient-animal implementation; a good worked example of *scene*-complete vs *asset*-complete. |
| `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | ⚪ | **Rejects** the realistic/procedural PNW attempts; sets flat art as the source. |
| `SKY_LAGOON_PNW_RUNTIME_IMPLEMENTATION_2026-07-21.md` | ⚪ | Why the accepted 2D set stalled before runtime. |
| `SKY_LAGOON_QUALITY_AUDIT_2026-07-20.md`, `SKY_LAGOON_ART_AUDIT_2026-07-19.md`, `SKY_LAGOON_STYLE_COHESION_AUDIT_2026-07-19.md` | ⚪ | The 3D-era lagoon audits. Contains the **binding botanical rule** (a detached leaf may never represent a whole plant). |
| `CLAUDE_SKY_LAGOON_DESIGN_HANDOFF_2026-07-19.md`, `CLAUDE_SKY_LAGOON_BLENDER_CONTINUATION_2026-07-20.md` | 🟡 | Blender-era handoffs; superseded by the flat/2.5D direction. |

## Zone: Pearl Opera (the largest chain — read top to bottom)

| Doc | | Note |
|---|---|---|
| `OPERA_STAGE_INTERACTION_2026-08-02.md` | 🟢 | **Newest.** The paintings ARE the stages: routes, stations, roaming combat, the magnifier, Storybook task cards. |
| `OPERA_2D_REBUILD_2026-08-01.md` | 🟢 | The five-beat arc for all 12 careers + the four same-day owner corrections. |
| `OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md` | 🟢 | Architecture authority: 2D lobby, `OperaCareerWorld2D`, hidden rival, 3D floor bosses. |
| `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` | 🟢 | The live art request queue (P1–P7). P3-04/05, P6, P7 open. |
| `CODEX_OPERA_STAGE_COMPLETION_HANDOFF_2026-08-02.md` | 🟢 | The five art sets that complete the stage build. |
| `OPERA_NURSERY_JOB_12_2026-08-01.md` | 🟢 | Job 13 (Moonbeam Nursery), cooperative, save-migration guarded. |
| `FABLE_OPERA_LAMBA_TAKEOVER_HANDOFF_2026-08-01.md`, `FABLE_OPERA_LAMBA_TAKEOVER_STATUS_2026-08-01.md` | 🟢 | Lamba replaces the rabbit-fish. Two owner-gated tasks remain ([OW-15](04_OPEN_WORK.md#ow-15)). |
| `OPERA_ACT_PACING_2026-07-25.md` | 🟢 | The 2–4 minute standard and "longer must not mean more of the same". |
| `OPERA_ACT_REDESIGN_2026-07-25.md` | 🟡 | Superseded by the five-beat rebuild; its *standard* (design the game the career implies) survives. |
| `OPERA_JOB_GIMMICKS_2026-07-25.md` | 🟡 | Superseded by `OPERA_ACT_REDESIGN`. Its finding — nine of twelve acts were the same verb — is why the arc exists. |
| `CODEX_ART_WORKORDER_2026-07-25.md` | 🟡 | Superseded by `CODEX_NEXTGEN_OBJECTS_2026-07-25.md`. |
| `CODEX_NEXTGEN_OBJECTS_2026-07-25.md` | 🔵 | *How* an opera object is constructed, driven by a regenerated file rather than a hand-typed list. |
| `CODEX_ASSET_REQUESTS_2026-07-21.md`, `OPERA_ASSET_REQUESTS_2026-07-19.md` | 🟡 | Early prop lists; superseded by the work orders above. |
| `CLAUDE_OPERA_HYBRID_LEVELS_2026-07-24.md` | 🟡 | The two-act hybrid design; superseded by the 2D five-beat rebuild. |
| `CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md`, `CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md`, `CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21.md`, `CLAUDE_START_HERE_OPERA_JOB_ASSET_REGENERATION_2026-07-24.md` | 🟡 | The 3D/hybrid era. Superseded by the 2D shipping path. |
| `OPERA_JOB_FLAT_PROTOTYPE_PLAN_2026-07-21.md` | ⚪ | The 36-sheet / 576-card plan. |
| `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md`, `OPERA_HOUSE_FLAT_ART_AUDIT_2026-07-21.md`, `OPERA_JOB_2P5D_ART_AUDIT_2026-07-24.md`, `OPERA_JOB_HYBRID_FINALE_ART_AUDIT_2026-07-24.md` | ⚪ | Acceptance audits for those packages. The art they accepted is still in use. |
| `audit/opera_regeneration_audit_2026-08-01.md` | 🔵 | 74 accepted / 8 rejected candidates with SHA evidence. |

## Zone: Northern Kingdom, Ember Fortress, dungeon, reef

| Doc | | Note |
|---|---|---|
| `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md` | 🔵 | The 25-family authored kit at a 4.5 floor / 4.9 ceiling. |
| `NORTHERN_BLENDER_HANDOFF_FOR_CLAUDE_2026-07-20.md` | 🔵 | Continuation rules; do not restore removed primitives. |
| `NORTHERN_WORLD_ART_AUDIT_2026-07-17.md`, `NORTHERN_ASSET_BATCH_02.md` | ⚪ | Earlier northern audit and request list. |
| `EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22.md` | 🟢 | **Rejects the procedural mesh chain**; the six 2D boards are the design input. |
| `EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md` | 🔵 | 40 further concept cards (39 → 79 exports). |
| `CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md` | 🔵 | The Blender build order from those boards. IP-safety rules restated. |
| `EMBER_FORTRESS_GRAPHICS_AUDIT_2026-07-21.md`, `CLAUDE_EMBER_FORTRESS_GRAPHICS_HANDOFF_2026-07-21.md` | 🟡 | The rejected earlier chain. Keep for the IP-safety framing only. |
| `DUNGEON_ART_REBUILD_AUDIT_2026-07-16.md` | ⚪ | Ten authored dungeon assets replacing primitives. |
| `REEF_REDESIGN_AUDIT_2026-07-16.md` | ⚪ | Records the **failed** first district redesign — read before redesigning the reef. |
| `LIVING_WORLD_STAGE_AUDIT_2026-07-27.md` | 🔵 | The 111-stage inventory. Its overlay is critiqued in [OW-11](04_OPEN_WORK.md#ow-11); its **stranded-legacy-stage list** is the evidence for [OW-2](04_OPEN_WORK.md#ow-2). |

## Characters and models

| Doc | | Note |
|---|---|---|
| `NPC_3D_WORKORDER_2026-07-19.md` | 🟡 | **PAUSED** by the 2026-07-27 charter. Batch stays staged; key never lives in-repo. |
| `CHARACTER_PIPELINE.md`, `CHARACTER_CUSTOMIZATION.md`, `CHARACTER_RUNBOOK.md` | ⚪ | The June 2026 3D-character/cosmetics plan. Cutouts are the medium again. |
| `docs/ROSHAN_RIG_AUDIT.md` | 🔵 | v4 rig defects (the underbound +X arm). Method for all later rig checks. |
| `docs/ROSHAN_FINAL_MODEL_2026-07-18.md` | 🟢 | The shipping-model recommendation. |
| `docs/ROSHAN_POSE_STRESS_2026-07-18.md` | 🔵 | Held-pose range-of-motion results; harness `tools/audit_pose_stress.py`. |
| `CLAUDE_FABLE_ORNATE_SHELL_UI_HANDOFF_2026-07-29.md`, `CLAUDE_FABLE_UI_HANDOFF_2026-07-21.md` | 🔵 | The UI lineage that produced `StorybookUI`. |

## Cinematics

| Doc | | Note |
|---|---|---|
| `docs/TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md` | 🟢 | The blocking production gate. Full-frame regeneration only. |
| `docs/CINEMATIC_DIRECTION_AND_INTENT_PROTOCOL.md` | 🟢 | The pre-generation intent process. Its companion. |
| `docs/OPENING_CINEMATIC_ART_DIRECTION_BRIEF_V2.md` | 🔵 | The cinematography/script brief for the opening. |
| `docs/OPENING_CINEMATIC_FULL_FRAME_PROCESS_AUDIT_2026-07-29.md` | 🔵 | The full-frame trial, including what the position-guide modes actually measured. |
| `docs/OPENING_CINEMATIC_REGENERATION_AUDIT_2026-07-28.md` | 🟡 | Explicitly marked historical: its pose-reuse/compositing methods are now forbidden. |
| `docs/CARTOON_VIDEO_PIPELINE.md` | 🔵 | The `.ogv` encoder runbook. |

## Tooling and generated reports

| Doc | | Note |
|---|---|---|
| `VISUAL_AUDIT_TOOL.md` | 🟢 | (listed above) |
| `audit/visual_design_report.md` | 🔵 | Generated output — regenerate, never hand-edit. |

---

## Where the same rule is stated more than once

Kept as-is; noted so a future edit updates every copy.

| Rule | Also stated in |
|---|---|
| Protected book art / voices / friend cutouts | `CLAUDE.md`, `AGENTS.md`, `ART_STYLE_GUIDE`, `ART_SCORING_GOVERNANCE`, and the preamble of ~20 art audits |
| Texture ≤1024 px or POT, OGG audio, one licence line | `CLAUDE.md`, `AGENTS.md`, every Codex work order |
| No fail states / voice + pointer objectives | `CLAUDE.md`, `AGENTS.md`, `MEDALS`, `MINIGAME_ENGINES`, `STUFFIE_COMPANIONS`, the charter |
| Wind Waker / Zelda is a rendering reference only | `CLAUDE.md`, `AGENTS.md`, `CEL_SHADING`, `ZELDA_GAMEPLAY_WORKORDER`, both Ember handoffs |
| Mobile renderer everywhere | `CLAUDE.md`, `AGENTS.md`, `DESIGN_3_0`, `LIGHTING_SHADER_AUDIT`, `ART_SCORING_GOVERNANCE` |
| 2048 px native background per playable screen | `AGENTS.md`, `SKY_LAGOON_REDUCTIVE_HANDOFF`, `FABLE_CASTLE_2K_REGEN_HANDOFF`, `OPERA_CAREER_COMPETITION_SYSTEM`, `FABLE_INTERACTION_HANDOFF` |
