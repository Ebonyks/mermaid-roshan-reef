# Master design — document ledger

_Initial 149-document index: 2026-08-02. Targeted authority reconciliation:
2026-08-09._

This ledger is **not exhaustive** for the repository's current Markdown set.
It preserves the original index and adds the documents/partial-supersession
decisions needed for the 2026-08-09 medium ruling. `MA-DOC-002` remains
`CONFIRMED_OPEN` until a gate proves exactly one scoped authority row for every
tracked Markdown path. Absence from this file grants no authority.

**Legend**

| | Meaning |
|---|---|
| 🟢 | **BINDING/CURRENT** — `BINDING_OPERATIONAL`, `BINDING_DOMAIN`, or current canonical scope; the note names it. |
| 🟣 | **PROPOSED_CANONICAL** — tracked and recognized, but still pending its declared gate. |
| 🔵 | **SUPPORTING_CURRENT** — useful detail/runbook, unable to redefine the canonical rule. |
| 🟠 | **MIXED / PARTIALLY SUPERSEDED** — the note states exactly what survives and what is history. |
| 🟡 | **SUPERSEDED** — a later decision replaced the relevant conclusion; evidence only. |
| ⚪ | **HISTORICAL_EVIDENCE** or **PROPOSAL_DEFERRED** — the note names which; never take it as current implementation authority. |

---

## Authority and operations

| Doc | | Note |
|---|---|---|
| `CLAUDE.md` | 🟢 | `BINDING_OPERATIONAL`; reconciled 2026-08-09 to exact Godot 4.7.1 and true-2D medium. The complete `AGENTS.md` cinematic rule remains controlling. |
| `AGENTS.md` | 🟢 | `BINDING_OPERATIONAL`; security/protected/save/release workflow and full-frame cinematic rules remain binding; 3D direction replaced by the 2026-08-09 true-2D decision. |
| `SECURITY.md` | 🟢 | `BINDING_OPERATIONAL`; threat model and agent rules. A content/design decision cannot weaken it. Summarized in 03 §8. |
| `BACKUP.md` | 🟢 | `BINDING_OPERATIONAL`; four backup layers and restore recipes. |
| `ASSET_LICENSES.md` | 🟢 | `BINDING_LEDGER`; one provenance/licence entry per new asset in the same commit. Row count not asserted here. |
| `WORKFLOW_BRANCHING_2026-07-18.md` | 🟢 | `BINDING_OPERATIONAL`; the dev/master promotion rule. Summarized in 03 §6. |
| `docs/ANDROID_RELEASE.md` | 🟢 | `BINDING_OPERATIONAL`; signing-key safety — a key change destroys the child's save. |
| `design/00_MASTER_INDEX.md` | 🔵 | `SUPPORTING_CURRENT`; authority navigation and precedence, explicitly not an exhaustive ledger. |
| `design/01_GAME_DESIGN.md` | 🟢 | `BINDING_DOMAIN` within the newer owner decision/design-language scope; 2.5D/3D history explicitly superseded. |
| `design/02_ART_DIRECTION.md` | 🟢 | `BINDING_DOMAIN`; true-2D visual medium plus the protected-content and absolute cinematic rules. |
| `design/03_TECHNICAL_ARCHITECTURE.md` | 🟢 | `BINDING_DOMAIN`; exact engine/build/save/security/release rules plus explicitly measured 3D debt. |
| `design/04_OPEN_WORK.md` | 🔵 | `SUPPORTING_CURRENT`; current lifecycle crosswalk, not canonical finding records. |
| `design/05_DOC_LEDGER.md` | 🔵 | `SUPPORTING_CURRENT`; this partial index. Exhaustive ledger closure remains `MA-DOC-002`. |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` | 🟣 | `PROPOSED_CANONICAL`; tracked and indexed, pending the remaining documentation gate. Stable `DL-*` rule authority within its declared state. |
| `audit/MASTER_AUDIT_2026-08-09.md` | 🟣 | `PROPOSED_CANONICAL`; synchronized audit-cycle/evidence/lifecycle record. Overall state `REPAIRING`, satisfaction `NOT SATISFIED`. |
| `ASSET_AUDIT.md` | ⚪ | `HISTORICAL_EVIDENCE`; 2026-06-25 CC0 audit/network decision. Current named-defect discipline comes from design 06; the later broad replacement campaign is deferred. |

## Game design lineage

| Doc | | Note |
|---|---|---|
| `GAME_REDESIGN_2P5D_2026-07-27.md` | 🟠 | `HISTORICAL_EVIDENCE` for child-readable linear navigation, touch-the-world, independent cards and differential layers. Its 2.5D/SideScrollStage/depth-buffer/reversibility/migration-order prescriptions are `SUPERSEDED`. |
| `WORLD_MAP_2026-07-27.md` | ⚪ | `PROPOSAL_DEFERRED`; geography is unapproved. Its old reachability report is historical; current `MA-PLAY-001` requires fresh enumeration. |
| `MINIGAME_ENGINES.md` | 🟠 | `SUPPORTING_CURRENT` for lifecycle/input/reward/mercy/voice/probe contracts. E1 expansion is deferred; E2/E4 spatial, Jolt-standee and Spline3 prescriptions are `SUPERSEDED`. |
| `MEDALS.md` | 🟠 | `BINDING_DOMAIN` for bronze/silver/gold, upgrade-only and passive-no-award rules. Its “3D play place” venue label is historical debt, not medium authority. |
| `STUFFIE_COMPANIONS.md` | 🟠 | `BINDING_DOMAIN` for roster, unlock, care, control and no-fail behavior. GLB bodies, Meshy creation and 3D arena prescriptions are `SUPERSEDED`. |
| `STUFFIE_PLAYROOM_RESCUE_GUIDE_2026-07-29.md` | 🟠 | `BINDING_DOMAIN` for wordless tutorial intent/no-fail flow. Sprite3D/depth/effect implementation is `SUPERSEDED`. |
| `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` | ⚪ | `PROPOSAL_DEFERRED`; age-4 analysis is historical evidence, lock/key expansion is not current work. |
| `ZELDA_GAMEPLAY_WORKORDER_2026-07-18.md` | ⚪ | `PROPOSAL_DEFERRED`; verb/structure expansion is not current work or 3D authorization. |
| `FABLE_INTERACTION_HANDOFF_2026-07-25.md` | 🟠 | `BINDING_DOMAIN` only for touch ownership, explicit activation, cancel/teardown and semantic interaction. Every 2.5D/Sprite3D/Camera3D/light/depth contract is `SUPERSEDED`. |
| `TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25.md` | 🟠 | `BINDING_DOMAIN` for retained Hybrid/Classic input grammar and cancellation. Keeping a 3D world or dimensional rollback is `SUPERSEDED`; ordinary input fallback is not. |
| `RACE_FEEL_WORKORDER.md` | 🟠 | `SUPPORTING_CURRENT` only for measured feel criteria; any spatial implementation prescription is `SUPERSEDED`. |
| `KART_FEEL.md` | 🟠 | `SUPPORTING_CURRENT` comparative feel rubric; spline/3D implementation is `SUPERSEDED`. |
| `AUDIT_UPGRADE.md` | 🟠 | `SUPPORTING_CURRENT` for evidence quality/device gaps, including [OW-21](04_OPEN_WORK.md#ow-21). Its 3D product framing and generic rollback link are historical. |
| `AUDIT_3_0.md` | ⚪ | June 2026 pre-3.0 critical audit. Its criticals (no save, no ending) are long fixed. |
| `DESIGN_3_0.md` | ⚪ | What 3.0 changed and why. Origin of the Mobile-renderer and stretch decisions. |
| `CONVERSATION_AUDIT.md` | ⚪ | June 2026 discussed-vs-shipped checklist. |
| `GAME_AUDIT_v3_49.md` | ⚪ | Comprehensive v3_49 design+code audit with an emulated playthrough. |
| `AUDIT_REPAIR.md` | ⚪ | Closes the 2026-07-15 repair phase (agency, no-fail, touch, save safety). |
| `CODE_AUDIT_2026_07.md` | ⚪ | `HISTORICAL_EVIDENCE`; B1–B9 are closed. Current structural debt is re-owned by `MA-CODE-001`/`MA-CODE-002`, not imported wholesale from §4. |
| `CAMERA_AUDIT_2026_07.md` | 🟡 | `HISTORICAL_EVIDENCE`; its 3D boom/Vector3 resolver explains legacy behavior but is `SUPERSEDED` by final `Camera2D` composition. |
| `JOLT_PHYSICS_AUDIT_2026-07-18.md` | 🟡 | `HISTORICAL_EVIDENCE`; the former garnish-only rationale is superseded because all 3D physics is removal debt. |
| `LIGHTING_SHADER_AUDIT_2026-07-18.md` | 🟠 | `SUPPORTING_CURRENT` for Mobile-renderer evidence only; 3D light/spatial-shader growth and Lighting Lab direction are `SUPERSEDED`. |
| `COLOR_CONSISTENCY_AUDIT.md` | ⚪ | 2026-07-15 overexposure findings in six bright contexts. |

## Engine references

| Doc | | Note |
|---|---|---|
| `PHYSICS_ENGINE.md` | 🟠 | `SUPPORTING_CURRENT` for tested feel/analytic behavior; `Vector3`, heightfield and spatial-solid contracts are migration debt. |
| `HIT_ENGINE.md` | 🟢 | The shared enemies-get-hit pipeline. |
| `RACE_ENGINE.md` | 🟠 | `SUPPORTING_CURRENT` for config/assist/reward behavior; spline/spatial presentation is `SUPERSEDED`. |
| `VISUAL_AUDIT_TOOL.md` | 🟠 | `SUPPORTING_CURRENT` only for stress-first falsifiability, honest evidence/lifecycle states, complete-evidence gating and reproducible visual provenance. At committed HEAD its Sprite3D-as-2D allowance is `SUPERSEDED`; a concurrent true-Canvas reconciliation is uncommitted/pending and has no authority until committed and gated. All 3D/Blender/Meshy/rig/model-conversion prescriptions are non-executable history. |

## Art doctrine

| Doc | | Note |
|---|---|---|
| `ART_STYLE_GUIDE.md` | 🟠 | `BINDING_DOMAIN` only for shape/line/value/colour, sampled palette, identity/protected-source rules, child readability, complete anatomy/silhouette, and licence/provenance discipline. Its 2D-to-3D translation, Blender, Meshy, GLB, rig, model-texture, turnaround and conversion-contract prescriptions are `SUPERSEDED`. |
| `ART_SCORING_GOVERNANCE_2026-07-18.md` | 🟠 | `BINDING_DOMAIN` only for runtime-context scoring, stress/rejection iteration, explicit owner acceptance for 5/5, no automatic score from provenance, protected originals, and recorded provenance. Its 3D-diorama, deterministic-Blender, Meshy, rig/model and image-to-3D workflow prescriptions are `SUPERSEDED`. |
| `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` | 🟠 | `SUPPORTING_CURRENT` for stable pivots, unique pixel ownership, motion budgets and card roles. Its exclusive Sprite3D/depth-buffer structure is `SUPERSEDED`. |
| `CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md` | 🟠 | `SUPPORTING_CURRENT` for approved source art, layer intent and shot evidence. Sprite3D/2.5D formats and speculative batch queue are `SUPERSEDED`/deferred. |
| `ART_ASSET_LIBRARY.md` | 🟠 | `SUPPORTING_CURRENT` for protected/current 2D paths and provenance. Any `gen2` model or active-3D placement direction is `SUPERSEDED`. |
| `CC0_REPLACEMENT_WORKORDER_2026-07-22.md` | 🟠 | `PROPOSAL_DEFERRED` as a broad campaign; reuse/provenance and one-at-a-time proof survive for named current defects ([OW-18](04_OPEN_WORK.md#ow-18)). |
| `VISUAL_DESIGN_AUDIT_2026-07-28.md` | 🟠 | `HISTORICAL_EVIDENCE`: Lagoon one-layer report survives as `MA-VIS-002`; rollback/pilot premises are dismissed and palette reports require new state-local evidence. |
| `CEL_SHADING.md` | ⚪ | The 2026-06-26 Wind Waker decision that set the rendering register. |
| `ART_STYLE_AUDIT.md` | ⚪ | 2026-07-13 baseline style audit ("strong heart, uneven perimeter"). |
| `ART_FULL_INVENTORY.md` | ⚪ | 2026-07-14 directory-level inventory of 487 visual files. |
| `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md` | 🟡 | Rubric superseded by `ART_SCORING_GOVERNANCE_2026-07-18.md`. Its 0–4 caps survive. |
| `ART_GAME_WIDE_PASS35_AUDIT_2026-07-16.md` | ⚪ | The 110-asset pass-3.5 rebuild with runtime evidence. |
| `ART_PASS35_PROMPTS.md` | ⚪ | Generation provenance for that pass. |
| `ART_RESIDUAL_LOW_SCORE_AUDIT.md` | 🟡 | Its "no remaining 0–2/5 roles" conclusion was corrected by `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`. |
| `ART_REMEDIATION_BATCH_04.md`, `ART_RUNTIME_REMEDIATION_BATCH_03.md`, `ART_SCORE3_REBUILD_AUDIT.md`, `ART_LANDMARK_REBUILD.md` | ⚪ | Completed 2026-07-14/15 remediation passes. |
| `ART_3D_BATCH_01.md`, `ART_3D_BATCH_02.md`, `ART_3D_CONVERSION_MANIFEST.md` | 🟡 | `HISTORICAL_EVIDENCE`; every Blender/model conversion direction is `SUPERSEDED`, not merely deprioritized. |
| `ART_GENERATION_BATCH_01.md`, `ART_GENERATION_BATCH_02.md` | ⚪ | Review blocks, never automatic runtime replacements. |
| `ART_AUDIT_2026-07-18.md` | ⚪ | Four-day-window repeat audit. |
| `ART_GAP_WORKORDER_2026-07-18.md` | ⚪ | `HISTORICAL_EVIDENCE`; gap claims and line references require fresh reproduction before becoming work. |
| `ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md` | ⚪ | Cross-history critique of everything below 5/5. |
| `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md` | ⚪ | Directive audit for the regen-pack iteration; P0 was a QA-integrity fix. |
| `FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md`, `FULL_TEXTURE_REGEN_IMPLEMENTATION_REVIEW_2026-07-18.md`, `FULL_TEXTURE_REGEN_POST_STRESS_ANALYSIS_2026-07-18.md` | ⚪ | The isolated 167-candidate regeneration pack: baseline, independent review, post-stress result. |
| `NB_AI_STUDIO_EXPORT.md`, `NB_TEXTURE_PLAN.md`, `TEXTURE_SOURCE_AUDIT.md` | ⚪ | The nano-banana texture era. Superseded as a channel by Codex flats. |
| `OBJECT_PLACEMENT_AUDIT_2026-07-17.md` | 🔵 | Ecosystem placement rules (right biome, believable support, reserved footprints). Still a good check. |
| `PARALLEL_ART_WORK_REVIEW_2026-07-16.md` | ⚪ | One-time overlap arbitration between concurrent art branches. |
| `REEF_FLORA.md` | 🔵 | The marine-first flora roster and its licensing record. |

## Zone: Pearl Castle

| Doc | | Note |
|---|---|---|
| `CASTLE_INTERACTION_AUDIT_2026-08-01.md` | 🟠 | `BINDING_DOMAIN` for truthful semantic interactions and owned alpha; Sprite3D/depth implementation is `SUPERSEDED` and must migrate to Canvas ordering. |
| `CASTLE_ROOM_LED_CODEX_IMPLEMENTATION_2026-07-28.md` | 🟠 | `SUPPORTING_CURRENT` for room/door narrative and approved art; 2.5D/Sprite3D structure is `SUPERSEDED`. The 2026-08-01 elevator removal remains current. |
| `FABLE_CASTLE_ANIMATION_INTERACTIVITY_HANDOFF_2026-07-29.md` | 🟠 | `SUPPORTING_CURRENT` for authored motion/interaction intent; spatial-card implementation is `SUPERSEDED`. |
| `CASTLE_DUST_BUNNY_SPAWN_GUIDE_2026-07-29.md` | 🟠 | `BINDING_DOMAIN` for distinct bunnies, contact/no-fail behavior and cleanup; Sprite3D/Camera3D/depth/effect directions are `SUPERSEDED`. |
| `FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md` | 🟠 | `SUPPORTING_CURRENT` for approved source-pixel/style evidence; Sprite3D inventory/presentation is `SUPERSEDED`. Its dated item count is historical. |
| `FABLE_CASTLE_2P5D_LAYER_AUDIT_2026-07-26.md` | ⚪ | `HISTORICAL_EVIDENCE`; source-layer/navigation observations may inform 2D work, but 2.5D structure is superseded and the set was resolution-nonconforming. |
| `FABLE_CASTLE_2K_REGEN_HANDOFF_2026-07-26.md` | 🟠 | `SUPPORTING_CURRENT` only for native-per-screen resolution and approved source continuity; spatial staging is superseded. |
| `FABLE_CASTLE_MAIN_HALL_PROP_COMPATIBILITY_AUDIT_2026-07-28.md` | ⚪ | Rejects the doorway-vignette pass; one hub vocabulary. |
| `FABLE_CASTLE_VISUAL_POLISH_INTERVENTION_2026-07-28.md` | ⚪ | Hierarchy-not-topology polish direction. |
| `CASTLE_PEARL_ART_AUDIT_2026-07-18.md` | ⚪ | `HISTORICAL_EVIDENCE`; the 3D-era castle rebuild cannot direct final Canvas work. |
| `audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md` | 🟠 | `SUPPORTING_CURRENT` for source seam/tone/registration evidence; Sprite3D delivery structure is `SUPERSEDED`. |
| `audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md` | 🟡 | `HISTORICAL_EVIDENCE`; superseded by the seam/tone evidence for fixtures/junctions/tone and by true 2D for runtime structure. |

## Zone: Sky Lagoon

| Doc | | Note |
|---|---|---|
| `SKY_LAGOON_CONGRUENCY_REBUILD_2026-07-27.md` | 🟠 | `SUPPORTING_CURRENT` for approved 3×1 source composition/congruency; promenade/spatial runtime structure is `SUPERSEDED`. |
| `SKY_LAGOON_REDUCTIVE_HANDOFF_2026-07-28.md` | 🟠 | `BINDING_DOMAIN` for the 6144×2048 clean plate, unique object ownership and 6×2 slicing; final reconstruction uses Canvas/`Sprite2D`, not Sprite3D. |
| `SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27.md` | 🟠 | `BINDING_DOMAIN` for native-master preservation/resolution. Sprite3D/camera/touch validation is `HISTORICAL_EVIDENCE`, not final structure. |
| `SKY_LAGOON_LIVING_CARD_V3_IMPLEMENTATION_AUDIT_2026-07-29.md` | 🟠 | `HISTORICAL_EVIDENCE` for the pilot and durable card lessons; Sprite3D/depth implementation is `SUPERSEDED`. |
| `docs/audits/SKY_LAGOON_ANIMALS_2026-08-01.md` | 🟠 | `SUPPORTING_CURRENT` for habitat, continuity and scene-complete evidence; Sprite3D/shadow staging is `SUPERSEDED`. |
| `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | ⚪ | **Rejects** the realistic/procedural PNW attempts; sets flat art as the source. |
| `SKY_LAGOON_PNW_RUNTIME_IMPLEMENTATION_2026-07-21.md` | ⚪ | Why the accepted 2D set stalled before runtime. |
| `SKY_LAGOON_QUALITY_AUDIT_2026-07-20.md`, `SKY_LAGOON_ART_AUDIT_2026-07-19.md`, `SKY_LAGOON_STYLE_COHESION_AUDIT_2026-07-19.md` | 🟠 | `HISTORICAL_EVIDENCE`; 3D prescriptions are `SUPERSEDED`. The detached-leaf botanical rule survives as current art doctrine. |
| `CLAUDE_SKY_LAGOON_DESIGN_HANDOFF_2026-07-19.md`, `CLAUDE_SKY_LAGOON_BLENDER_CONTINUATION_2026-07-20.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender/3D directions are `SUPERSEDED` by final true 2D. |

## Zone: Pearl Opera (the largest chain — read top to bottom)

| Doc | | Note |
|---|---|---|
| `OPERA_STAGE_INTERACTION_2026-08-02.md` | 🟢 | `BINDING_DOMAIN` for paintings-as-Canvas-stages, routes, stations, roaming combat, magnifier and Storybook task cards. Later current defects are owned by `MA-OPERA-*`. |
| `OPERA_2D_REBUILD_2026-08-01.md` | 🟠 | `BINDING_DOMAIN` for the five-beat Canvas career arc and dated owner corrections. “3D floor bosses unchanged,” rival GLBs and legacy-3D fallback are `SUPERSEDED`. |
| `OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md` | 🟠 | `BINDING_DOMAIN` for 2D lobby, `OperaCareerWorld2D`, hidden rival and competition behavior; 3D boss/outfit/presentation prescriptions are `SUPERSEDED`. |
| `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` | 🟡 | `HISTORICAL_EVIDENCE`; its request-list scope is superseded by the later August 3–5 audits/current `MA-OPERA-*` index. |
| `CODEX_OPERA_STAGE_COMPLETION_HANDOFF_2026-08-02.md` | 🟠 | `HISTORICAL_EVIDENCE` for source gaps/consumer paths; reproduce against current `MA-OPERA-*` items before generating or wiring art. |
| `OPERA_NURSERY_JOB_12_2026-08-01.md` | 🟠 | `BINDING_DOMAIN` for Job 13's cooperative Canvas behavior and save migration; its 3D player/SideScroll parent description is migration history. |
| `FABLE_OPERA_LAMBA_TAKEOVER_HANDOFF_2026-08-01.md`, `FABLE_OPERA_LAMBA_TAKEOVER_STATUS_2026-08-01.md` | 🟠 | `SUPPORTING_CURRENT` for the approved Lamba semantic role; old implementation queue is historical. Protected recording gap remains `MA-ACCESS-002`. |
| `OPERA_ACT_PACING_2026-07-25.md` | 🟢 | The 2–4 minute standard and "longer must not mean more of the same". |
| `OPERA_ACT_REDESIGN_2026-07-25.md` | 🟡 | Superseded by the five-beat rebuild; its *standard* (design the game the career implies) survives. |
| `OPERA_JOB_GIMMICKS_2026-07-25.md` | 🟡 | Superseded by `OPERA_ACT_REDESIGN`. Its finding — nine of twelve acts were the same verb — is why the arc exists. |
| `CODEX_ART_WORKORDER_2026-07-25.md` | 🟡 | Superseded by `CODEX_NEXTGEN_OBJECTS_2026-07-25.md`. |
| `CODEX_NEXTGEN_OBJECTS_2026-07-25.md` | 🟡 | `HISTORICAL_EVIDENCE`; its generated-file discipline may explain provenance, but all one-object-per-GLB/model construction is `SUPERSEDED`. |
| `CODEX_ASSET_REQUESTS_2026-07-21.md`, `OPERA_ASSET_REQUESTS_2026-07-19.md` | 🟡 | Early prop lists; superseded by the work orders above. |
| `CLAUDE_OPERA_HYBRID_LEVELS_2026-07-24.md` | 🟡 | The two-act hybrid design; superseded by the 2D five-beat rebuild. |
| `CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md`, `CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md`, `CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21.md`, `CLAUDE_START_HERE_OPERA_JOB_ASSET_REGENERATION_2026-07-24.md` | 🟡 | `HISTORICAL_EVIDENCE`; all 3D/hybrid runtime directions are `SUPERSEDED` by true 2D. |
| `OPERA_JOB_FLAT_PROTOTYPE_PLAN_2026-07-21.md` | ⚪ | The 36-sheet / 576-card plan. |
| `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md`, `OPERA_HOUSE_FLAT_ART_AUDIT_2026-07-21.md`, `OPERA_JOB_2P5D_ART_AUDIT_2026-07-24.md`, `OPERA_JOB_HYBRID_FINALE_ART_AUDIT_2026-07-24.md` | ⚪ | Acceptance audits for those packages. The art they accepted is still in use. |
| `audit/opera_regeneration_audit_2026-08-01.md` | 🔵 | 74 accepted / 8 rejected candidates with SHA evidence. |

## Zone: Northern Kingdom, Ember Fortress, dungeon, reef

| Doc | | Note |
|---|---|---|
| `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; its 3D/GLB kit and build directions are `SUPERSEDED`. Dated style measurements may inform review but cannot authorize model work. |
| `NORTHERN_BLENDER_HANDOFF_FOR_CLAUDE_2026-07-20.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender/model continuation is `SUPERSEDED`. Its rejected-primitive history does not authorize rebuilding them in 2D. |
| `NORTHERN_WORLD_ART_AUDIT_2026-07-17.md`, `NORTHERN_ASSET_BATCH_02.md` | ⚪ | Earlier northern audit and request list. |
| `EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22.md` | 🟠 | `SUPPORTING_CURRENT` for the six approved 2D boards and rejection evidence; it does not authorize a later mesh conversion. |
| `EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md` | 🟠 | `SUPPORTING_CURRENT` for accepted 2D concept-card evidence only; `.blend`/GLB conversion and measured-model output are `SUPERSEDED`. |
| `CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender build order is `SUPERSEDED`. Independently binding IP-safety rules remain in current authority docs. |
| `EMBER_FORTRESS_GRAPHICS_AUDIT_2026-07-21.md`, `CLAUDE_EMBER_FORTRESS_GRAPHICS_HANDOFF_2026-07-21.md` | 🟡 | The rejected earlier chain. Keep for the IP-safety framing only. |
| `DUNGEON_ART_REBUILD_AUDIT_2026-07-16.md` | ⚪ | Ten authored dungeon assets replacing primitives. |
| `REEF_REDESIGN_AUDIT_2026-07-16.md` | ⚪ | Records the **failed** first district redesign — read before redesigning the reef. |
| `LIVING_WORLD_STAGE_AUDIT_2026-07-27.md` | 🟠 | `HISTORICAL_EVIDENCE` for its dated stage inventory. Screen-space overlay claims require fresh reproduction; its dimensional rollback prescription is dismissed. |

## Characters and retired model history

| Doc | | Note |
|---|---|---|
| `assets/characters/roshan_25d/README.md` | 🟢 | `BINDING_DOMAIN`; approved RGBA atlas ownership and true Canvas/`Sprite2D` target. Its current `Sprite3D` implementation note is explicitly migration debt. |
| `CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` for approved atlas/source-gap evidence. Atlas repacking is deferred and its 3D-standee staging is `SUPERSEDED`. |
| `ROSHAN_SPRITE_CUTOFF_AUDIT_2026-08-02.md` | 🟠 | `HISTORICAL_EVIDENCE` for clipping diagnosis/verified replacements; Sprite3D sampling implementation is migration history, not final structure. |
| `CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md` | 🟠 | `SUPPORTING_CURRENT` for approved 2D frames/acting intent; “2.5D” staging language is `SUPERSEDED`. |
| `NPC_3D_WORKORDER_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; Meshy/3D batch is `SUPERSEDED`, removed rather than paused. Never submit it; the missing key is not a blocker. |
| `CHARACTER_PIPELINE.md`, `CHARACTER_CUSTOMIZATION.md`, `CHARACTER_RUNBOOK.md` | 🟡 | `HISTORICAL_EVIDENCE`; all model/rig/skeleton/cosmetics prescriptions are `SUPERSEDED`. |
| `gen2/ROSHAN_V2_WORKORDER.md` | 🟡 | `HISTORICAL_EVIDENCE`; true-3D Roshan, Meshy submission, rig reuse and model fallback hierarchy are `SUPERSEDED`. |
| `docs/ROSHAN_RIG_AUDIT.md` | 🟡 | `HISTORICAL_EVIDENCE`; v4 rig measurements are retained only to explain retired work. No later rig work is authorized. |
| `docs/ROSHAN_FINAL_MODEL_2026-07-18.md` | 🟡 | `HISTORICAL_EVIDENCE`; shipping-model recommendation is `SUPERSEDED` by the 2026-08-09 2D-only decision. |
| `docs/ROSHAN_POSE_STRESS_2026-07-18.md` | 🟡 | `HISTORICAL_EVIDENCE`; model held-pose/harness work is `SUPERSEDED`, not an active QA requirement. |
| `gen2/generated/MEASURED_INTERFACE_SHEET_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; GLB/model interface measurements cannot direct current runtime work. |
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
| True Canvas/Node2D medium; all remaining 3D is shrinking debt | owner decision 2026-08-09, `AGENTS.md`, `CLAUDE.md`, design 00–06, `audit/MASTER_AUDIT_2026-08-09.md`, `assets/characters/roshan_25d/README.md` |
