# Master design — document ledger

_Initial 149-document index: 2026-08-02. Targeted authority reconciliation:
2026-08-09. Merge synchronization: 2026-08-12. Exhaustive 316-document
classification and exact-head closure verification: 2026-08-13._

This ledger is exhaustive for the repository's current Git-declared inventory
of **316 tracked or intended-tracked Markdown paths**: the 315-path base at
`18b6150c01e1587100dca97c85ebad03f369825a` plus the newly unignored canonical
findings register in this audit candidate. Every path reported by the
fail-closed cached/unignored inventory appears exactly once in the first column
of a classification row. Grouped legacy rows were split without changing their
curated rulings; the additional rows deliberately bound stale, mixed,
generated, source-only, and rollback material so none can acquire
repository-wide authority by omission. The ledger-side classification gate
for `MA-DOC-002` is satisfied; the master audit remains the lifecycle owner.
Sealed document-authority source chain head
`7eb945957776ab3458a9de71c8be9937e2354720` preserves the classification.
CHG-023 maintenance parent `e6edf559af219edd4e5ce38cab0c5094483be5c6`
passes integrated dev Probe Suite run `31722047536`: probes 34m25s/63-of-63,
36 focused document tests, six/six stress, 316/316 inventory/ledger, 34 active/
36 retained records, and music 3m33s/42-of-42. Earlier branch run `31719143975`
is corroborating e6 history. Current Sky source `51d0abc0`, exact parent
`1b7d6bda`, is the 19-path true-Canvas repair (+3,318/-3,517) and passes
official Godot 4.7.1 full local CI in 1,404.5 seconds/all 64. Run-14 is local
Mobile/Speedy 20/20 with manifest/PNG/probe hashes `AEAC7C72…DE34` and
`B9EAF5E0…9C6C`, while its source revision remains unknown.
Integrated evidence head `441adf35f7dbdeb67d36fbf1a2217b87d3040d47` is
governance-only over unchanged source `51d0abc0`; exact local CI exits 0 in
1,391.5 seconds/all 64. Topic Probe `31760207048` and dev Probe `31762132976`
succeed at exact `441adf35` with 63/63 unique remote headings, the 36-test/
six-stress/316/316/34-active/36-record document gate, and music 42/42. Their
nonblocking Sky diagnostics each emit 20 PASS rows but fall back to
llvmpipe/`gl_compatibility` after missing `VK_KHR_surface`, then exit 1 on the
renderer `GLOBAL`/`RESULT`; only PNGs upload, with no remote JSON or Mobile
PASS. Android run `31763879294` publishes the exact-head dev APK. Historical
`7391c53c` run `31728755204` retains its earlier failed remote Sky renderer
subprocess.
Future tracked or unignored Markdown is
unclassified until this ledger gains one new scoped row for it.

**Legend**

| | Meaning |
|---|---|
| 🟢 | **BINDING/CURRENT** — `BINDING_OPERATIONAL`, `BINDING_DOMAIN`, or current canonical scope; the note names it. |
| 🟣 | **PROPOSED / CANDIDATE** — tracked and recognized, but still pending its declared canonical, runtime-context, human, or owner gate; the note names which. |
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
| `ASSET_LICENSES.md` | 🟢 | `BINDING_LEDGER`; one provenance/licence entry per new asset in the same commit, including the merged Opera/minigame/atlas and 42-cue music deliveries. Provenance does not grant art acceptance. Row count not asserted here. |
| `WORKFLOW_BRANCHING_2026-07-18.md` | 🟢 | `BINDING_OPERATIONAL`; the dev/master promotion rule. Summarized in 03 §6. |
| `docs/ANDROID_RELEASE.md` | 🟢 | `BINDING_OPERATIONAL`; signing-key safety — a key change destroys the child's save. |
| `design/00_MASTER_INDEX.md` | 🔵 | `SUPPORTING_CURRENT`; authority navigation and precedence, explicitly not an exhaustive ledger. |
| `design/01_GAME_DESIGN.md` | 🟢 | `BINDING_DOMAIN` within the newer owner decision/design-language scope; 2.5D/3D history explicitly superseded. |
| `design/02_ART_DIRECTION.md` | 🟢 | `BINDING_DOMAIN`; true-2D visual medium plus the protected-content and absolute cinematic rules. |
| `design/03_TECHNICAL_ARCHITECTURE.md` | 🟢 | `BINDING_DOMAIN`; exact engine/build/save/security/release rules plus explicitly measured 3D debt. |
| `design/04_OPEN_WORK.md` | 🔵 | `SUPPORTING_CURRENT`; current lifecycle crosswalk, not canonical finding records. |
| `design/05_DOC_LEDGER.md` | 🔵 | `SUPPORTING_CURRENT`; this exhaustive 327-path Git-declared authority index. It classifies documents but cannot override the higher-precedence operational/domain authorities it identifies. |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` | 🟢 | `CANONICAL_CURRENT`; tracked, indexed, and document-authority verified through exact parent `e6edf559`. Stable `DL-*` rule authority remains subordinate to direct owner, operational, security, protected-asset, and save rules. |
| `design/07_CASTLE_DOOR_LANGUAGE.md` | 🟢 | `BINDING_DOMAIN`; Act One castle door states, single-highlight sequencing, arch-following cue treatment, and Baby Eagle plot-priority ownership. |
| `audit/MASTER_AUDIT_2026-08-09.md` | 🟢 | `CANONICAL_CURRENT`; synchronized audit-cycle/evidence/lifecycle record. Overall state remains `REPAIRING`, satisfaction `UNSATISFIED`. Unchanged product source `51d0abc0` passes exact local CI in 1,404.5 seconds/all 64; governance-only integrated head `441adf35` passes exact local CI in 1,391.5 seconds/all 64, topic/dev Probe runs `31760207048`/`31762132976`, and exact-head Android `31763879294`. Separate run-14 20/20 local Mobile/Speedy evidence has manifest/PNG/probe hashes but an unknown source revision. Both current remote Sky diagnostics remain non-authoritative renderer failures after their 20 PASS rows, with PNG-only upload and no remote JSON/Mobile PASS. No device/child/owner/accepted-visual evidence exists. Historical `7391c53c` run `31728755204` retains its earlier failed remote Sky renderer subprocess. `MA-VIS-002` is `FIXED_PENDING_VERIFICATION`; `MA-VIS-006` remains `CONFIRMED_OPEN`; global visual remains 16/17/2/86/32/94. |
| `audit/DAY_ONE_DIRTY_POOL_STYLE_AUDIT_2026-08-22.md` | 🔵 | `SUPPORTING_CURRENT`; scoped master-rubric comparison for the three bespoke Day One pool-cleanup activities. Its revised 4/5 strong-candidate verdict and exact desktop Mobile evidence cannot override the canonical master audit, close any master finding, or substitute for device/child/owner acceptance. |
| `audit/DAY_ONE_POOL_NATURAL_INTEGRATION_SPEC_2026-08-23.md` | 🔵 | `SUPPORTING_CURRENT`; records the accepted runtime composition criteria and exact Mobile evidence for naturalizing the pool activities. The generated plate is reference-only, and this spec cannot grant device, child, voice, or owner acceptance. |
| `design/HANDOFF_GROK_DAY_ONE_POOL_NEXT_ANIMATION_2026-08-23.md` | 🟠 | `SUPPORTING_CURRENT` visual-only owner-run Grok handoff for the follow-on pool animation. Its room/fixture/Roshan/Rumi continuity and required beat order are binding for that handoff, while Codex/Luna review and owner acceptance remain authoritative; it grants Grok no audio, editorial, upload, or approval authority. `SUPERSEDED` scope: replaces only the older generic dirty-pool beat order embedded in the scoped pool audit; it does not supersede the design language, master audit, cinematic rules, audio authority, or owner acceptance. |
| `audit/day_one_pool_lighting_image_audit_2026-08-22.md` | 🔵 | `GENERATED_REPORT`; five-file pixel-statistics summary for the Day One dirty-pool runtime textures. It supports the scoped style audit but is not an aesthetic, runtime-context, device, child, owner, or accepted-visual pass. Regenerate with `tools/audit_lighting_images.py`; do not hand-edit. |
| `audit/findings/ACTIVE_FINDINGS_2026-08-13.md` | 🟢 | `BINDING_AUDIT_RECORD` for 36 complete field-level P1/P2 records, linked from section 5 and retained through terminal transitions. Exact integrated head `441adf35` preserves the green 36-test/six-stress/316-parity document gate and 34 active/36 retained records in both topic/dev remote runs; `MA-DOC-005` is `VERIFIED_FIXED`. The file cannot silently add an item or change master severity/lifecycle. |
| `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` | 🟢 | `BINDING_OPERATIONAL` for stable `CHG-*` scope and rollback. Current inventory is 31 IDs, 79 uniquely owned commit references, four guarded-script emitters, 25 planner tests, and 27 manual/refusal groups. Manual/non-emitting CHG-031 owns exact 19-path source `51d0abc0`, including `scripts/probe_northern.gd`, at +3,318/-3,517. The ledger never authorizes rollback that violates protected-asset, security, save, or final-medium rules. |
| `ASSET_AUDIT.md` | ⚪ | `HISTORICAL_EVIDENCE`; 2026-06-25 CC0 audit/network decision. Current named-defect discipline comes from design 06; its stale music inventory is superseded by `MUSIC_AUDIT_2026-08-09.md`. |

## Game design lineage

| Doc | | Note |
|---|---|---|
| `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` | 🟠 | **Mixed authority / `PARTIALLY SUPERSEDED`.** `OWNER_DECISION` in §10 / `7426c187`: distribute all thirteen careers through thematic Castle rooms and make Opera Hall one venue, not the all-career hub. `OWNER_DECISION` in §16 / `3d1236fe`: cut Curtain Dragon, Shadow Phantom, and Midnight Maestro and keep save slots 4/9/14 as inert tombstones. Section 17 / `ef2fd982` clarifies that later boss fights belong to Ember-aligned henchmen and do not revive the Opera bosses. §17 supersedes §16 only on whether boss fights exist at all, while §16 supersedes §10's earlier Opera boss/finale-card language. Remaining chapter plot/system proposals are `PROPOSAL_DEFERRED` unless separately adopted. Boss retirement is `MA-OPERA-011` `FIXED_PENDING_VERIFICATION`; commit `09e5e356` implements the room distribution and moves `MA-OPERA-012` to `FIXED_PENDING_VERIFICATION`, with external/visual closure open. |
| `GAME_REDESIGN_2P5D_2026-07-27.md` | 🟠 | `HISTORICAL_EVIDENCE` for child-readable linear navigation, touch-the-world, independent cards and differential layers. Its 2.5D/SideScrollStage/depth-buffer/reversibility/migration-order prescriptions are `SUPERSEDED`. |
| `WORLD_MAP_2026-07-27.md` | ⚪ | `PROPOSAL_DEFERRED`; geography is unapproved. Its old reachability report is historical; current `MA-PLAY-001` requires fresh enumeration. |
| `MINIGAME_ENGINES.md` | 🟠 | `SUPPORTING_CURRENT` for lifecycle/input/reward/mercy/voice/probe contracts. E1 expansion is deferred; E2/E4 spatial, Jolt-standee and Spline3 prescriptions are `SUPERSEDED`. |
| `MEDALS.md` | 🟠 | `BINDING_DOMAIN` for bronze/silver/gold, upgrade-only and passive-no-award rules. Its “3D play place” venue label is `HISTORICAL_EVIDENCE`, not medium authority. |
| `STUFFIE_COMPANIONS.md` | 🟠 | `BINDING_DOMAIN` for roster, unlock, care, control and no-fail behavior. GLB bodies, Meshy creation and 3D arena prescriptions are `SUPERSEDED`. |
| `STUFFIE_PLAYROOM_RESCUE_GUIDE_2026-07-29.md` | 🟠 | `BINDING_DOMAIN` for wordless tutorial intent/no-fail flow. Sprite3D/depth/effect implementation is `SUPERSEDED`. |
| `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` | ⚪ | `PROPOSAL_DEFERRED`; age-4 analysis is historical evidence, lock/key expansion is not current work. |
| `ZELDA_GAMEPLAY_WORKORDER_2026-07-18.md` | ⚪ | `PROPOSAL_DEFERRED`; verb/structure expansion is not current work or 3D authorization. |
| `FABLE_INTERACTION_HANDOFF_2026-07-25.md` | 🟠 | `BINDING_DOMAIN` only for touch ownership, explicit activation, cancel/teardown and semantic interaction. Every 2.5D/Sprite3D/Camera3D/light/depth contract is `SUPERSEDED`. |
| `TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25.md` | 🟠 | `BINDING_DOMAIN` for retained Hybrid/Classic input grammar and cancellation. Keeping a 3D world or dimensional rollback is `SUPERSEDED`; ordinary input fallback is not. |
| `RACE_FEEL_WORKORDER.md` | 🟠 | `SUPPORTING_CURRENT` only for measured feel criteria; any spatial implementation prescription is `SUPERSEDED`. |
| `KART_FEEL.md` | 🟠 | `SUPPORTING_CURRENT` comparative feel rubric; spline/3D implementation is `SUPERSEDED`. |
| `AUDIT_UPGRADE.md` | 🟠 | `SUPPORTING_CURRENT` for evidence quality/device gaps, including [OW-21](04_OPEN_WORK.md#ow-21). Its 3D product framing and generic rollback link are `HISTORICAL_EVIDENCE`. |
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
| `PHYSICS_ENGINE.md` | 🟠 | `SUPPORTING_CURRENT` for tested feel/analytic behavior; `Vector3`, heightfield and spatial-solid contracts are `SUPERSEDED` migration debt. |
| `HIT_ENGINE.md` | 🟢 | The shared enemies-get-hit pipeline. |
| `RACE_ENGINE.md` | 🟠 | `SUPPORTING_CURRENT` for config/assist/reward behavior; spline/spatial presentation is `SUPERSEDED`. |
| `VISUAL_AUDIT_TOOL.md` | 🟠 | `SUPPORTING_CURRENT` only for stress-first falsifiability, honest evidence/lifecycle states, complete-evidence gating and reproducible visual provenance. Its Sprite3D-as-2D allowance is `SUPERSEDED` by the current true-Canvas reconciliation. All 3D/Blender/Meshy/rig/model-conversion prescriptions are non-executable history. |

## Audio and music

| Doc | | Note |
|---|---|---|
| `MUSIC_AUDIT_2026-08-09.md` | 🟢 | `BINDING_DOMAIN` for the 15-file legacy inventory, 42 deterministic new cues, shared musical language, one-player/hard-cut ownership, voice ducking, loop/mix targets, transition restoration and machine evidence. Exact authority-head run `31686380560` passes Windows from 09:24:08–09:27:55 UTC (3m47s) and ends `MUSIC\|check 42/42\|picture_xmas`. Human two-wrap listening, voice intelligibility, mono fold-down and Lenovo Tab M11 review remain open. Its dated nested-real-kart routing is superseded as direction; commit `e2c25878` removes the ordinary-headless Opera kart source present at `f3b0de07`, and `MA-OPERA-010` remains `FIXED_PENDING_VERIFICATION`, not audio authority. |
| `assets_src/audio/music/area_music_scores.json` | 🟢 | `BINDING_MACHINE_DATA` for the 42 declarative compositions; it cannot certify subjective listening. |
| `assets/audio/music/area_music_manifest.json` | 🟢 | `BINDING_MACHINE_EVIDENCE` for rendered hashes, codec, duration, loudness, peak and loop measurements of the 42 new cues. |

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
| `ART_REMEDIATION_BATCH_04.md` | ⚪ | Completed 2026-07-14/15 remediation-pass evidence. |
| `ART_RUNTIME_REMEDIATION_BATCH_03.md` | ⚪ | Completed 2026-07-14/15 remediation-pass evidence. |
| `ART_SCORE3_REBUILD_AUDIT.md` | ⚪ | Completed 2026-07-14/15 remediation-pass evidence. |
| `ART_LANDMARK_REBUILD.md` | ⚪ | Completed 2026-07-14/15 remediation-pass evidence. |
| `ART_3D_BATCH_01.md` | 🟡 | `HISTORICAL_EVIDENCE`; every Blender/model conversion direction is `SUPERSEDED`, not merely deprioritized. |
| `ART_3D_BATCH_02.md` | 🟡 | `HISTORICAL_EVIDENCE`; every Blender/model conversion direction is `SUPERSEDED`, not merely deprioritized. |
| `ART_3D_CONVERSION_MANIFEST.md` | 🟡 | `HISTORICAL_EVIDENCE`; every Blender/model conversion direction is `SUPERSEDED`, not merely deprioritized. |
| `ART_GENERATION_BATCH_01.md` | ⚪ | Historical review block, never automatic runtime replacement authority. |
| `ART_GENERATION_BATCH_02.md` | ⚪ | Historical review block, never automatic runtime replacement authority. |
| `ART_AUDIT_2026-07-18.md` | ⚪ | Four-day-window repeat audit. |
| `ART_GAP_WORKORDER_2026-07-18.md` | ⚪ | `HISTORICAL_EVIDENCE`; gap claims and line references require fresh reproduction before becoming work. |
| `ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md` | ⚪ | Cross-history critique of everything below 5/5. |
| `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md` | ⚪ | Directive audit for the regen-pack iteration; P0 was a QA-integrity fix. |
| `FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md` | ⚪ | Historical baseline for the isolated 167-candidate regeneration pack. |
| `FULL_TEXTURE_REGEN_IMPLEMENTATION_REVIEW_2026-07-18.md` | ⚪ | Historical independent review of the isolated 167-candidate regeneration pack. |
| `FULL_TEXTURE_REGEN_POST_STRESS_ANALYSIS_2026-07-18.md` | ⚪ | Historical post-stress result for the isolated 167-candidate regeneration pack. |
| `NB_AI_STUDIO_EXPORT.md` | ⚪ | `HISTORICAL_EVIDENCE` from the nano-banana texture era; that generation channel is superseded by current Codex flats. |
| `NB_TEXTURE_PLAN.md` | ⚪ | `HISTORICAL_EVIDENCE` from the nano-banana texture era; that generation channel is superseded by current Codex flats. |
| `TEXTURE_SOURCE_AUDIT.md` | ⚪ | `HISTORICAL_EVIDENCE` from the nano-banana texture era; that generation channel is superseded by current Codex flats. |
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
| `FABLE_CASTLE_2K_REGEN_HANDOFF_2026-07-26.md` | 🟠 | `SUPPORTING_CURRENT` only for native-per-screen resolution and approved source continuity; spatial staging is `SUPERSEDED`. |
| `FABLE_CASTLE_MAIN_HALL_PROP_COMPATIBILITY_AUDIT_2026-07-28.md` | ⚪ | Rejects the doorway-vignette pass; one hub vocabulary. |
| `FABLE_CASTLE_VISUAL_POLISH_INTERVENTION_2026-07-28.md` | ⚪ | Hierarchy-not-topology polish direction. |
| `CASTLE_PEARL_ART_AUDIT_2026-07-18.md` | ⚪ | `HISTORICAL_EVIDENCE`; the 3D-era castle rebuild cannot direct final Canvas work. |
| `audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md` | 🟠 | `SUPPORTING_CURRENT` for source seam/tone/registration evidence; Sprite3D delivery structure is `SUPERSEDED`. |
| `audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md` | 🟡 | `HISTORICAL_EVIDENCE`; superseded by the seam/tone evidence for fixtures/junctions/tone and by true 2D for runtime structure. |

## Zone: Sky Lagoon

| Doc | | Note |
|---|---|---|
| `SKY_LAGOON_CONGRUENCY_REBUILD_2026-07-27.md` | 🟠 | `SUPPORTING_CURRENT` for approved 3×1 source composition/congruency; promenade/spatial runtime structure is `SUPERSEDED`. |
| `SKY_LAGOON_REDUCTIVE_HANDOFF_2026-07-28.md` | 🟠 | `BINDING_DOMAIN` for the 6144×2048 clean plate, unique object ownership and 6×2 slicing; the old Sprite3D assembly is `SUPERSEDED`, and final reconstruction uses Canvas/`Sprite2D`. |
| `SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27.md` | 🟠 | `BINDING_DOMAIN` for native-master preservation/resolution. Sprite3D/camera/touch validation is `HISTORICAL_EVIDENCE`, not final structure. |
| `SKY_LAGOON_LIVING_CARD_V3_IMPLEMENTATION_AUDIT_2026-07-29.md` | 🟠 | `HISTORICAL_EVIDENCE` for the pilot and durable card lessons; Sprite3D/depth implementation is `SUPERSEDED`. |
| `docs/audits/SKY_LAGOON_ANIMALS_2026-08-01.md` | 🟠 | `SUPPORTING_CURRENT` for habitat, continuity and scene-complete evidence; Sprite3D/shadow staging is `SUPERSEDED`. |
| `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | ⚪ | **Rejects** the realistic/procedural PNW attempts; sets flat art as the source. |
| `SKY_LAGOON_PNW_RUNTIME_IMPLEMENTATION_2026-07-21.md` | ⚪ | Why the accepted 2D set stalled before runtime. |
| `SKY_LAGOON_QUALITY_AUDIT_2026-07-20.md` | 🟠 | `HISTORICAL_EVIDENCE`; 3D prescriptions are `SUPERSEDED`. The detached-leaf botanical rule survives as current art doctrine. |
| `SKY_LAGOON_ART_AUDIT_2026-07-19.md` | 🟠 | `HISTORICAL_EVIDENCE`; 3D prescriptions are `SUPERSEDED`. The detached-leaf botanical rule survives as current art doctrine. |
| `SKY_LAGOON_STYLE_COHESION_AUDIT_2026-07-19.md` | 🟠 | `HISTORICAL_EVIDENCE`; 3D prescriptions are `SUPERSEDED`. The detached-leaf botanical rule survives as current art doctrine. |
| `CLAUDE_SKY_LAGOON_DESIGN_HANDOFF_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender/3D directions are `SUPERSEDED` by final true 2D. |
| `CLAUDE_SKY_LAGOON_BLENDER_CONTINUATION_2026-07-20.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender/3D directions are `SUPERSEDED` by final true 2D. |

## Zone: Pearl Opera (the largest chain — read top to bottom)

| Doc | | Note |
|---|---|---|
| `BALLERINA_PARTY_REBUILD_2026-08-09.md` | 🟢 | `BINDING_DOMAIN`, latest integrated Ballerina authority: three-act full-stage Pearl Mirror / Ribbon Trail / Grand Twirl, monotonic 5/10-second assistance, held pose keys and one-shot curtain call. It supersedes every older Ballerina phase/playback section and old atlas recommendation. Runtime `09e5e356` and probe-readiness/full-local checkpoint `ff068db` are green; exact authority head `9befc0f8` passes run `31686380560`. Its capture pairs remain diagnostic/non-authoritative, so accepted capture, device, child and owner review remain open. |
| `design/BOXING_GAME_PROJECT_2026-08-09.md` | 🟠 | `BINDING_DOMAIN` for the integrated Boxer's five one-finger Canvas phases, touch ownership, friendly/no-loss behavior, save/reward ownership and probe contract. Its three retained GLBs are `SUPERSEDED` measured debt, never fallback or implementation resources. Runtime `09e5e356` and probe-readiness/full-local checkpoint `ff068db` are green; exact authority head `9befc0f8` passes run `31686380560`. Its capture pairs remain diagnostic/non-authoritative, so accepted capture, device, child and owner review remain open under `MA-OPERA-009`. A newer Boxer V2 document exists only on a separate docs branch and has not superseded this authority. |
| Painter-purpose worktree | ⚪ | `UNCOMMITTED_CANDIDATE`; purpose-focused Painter edits are not part of current product/audit commit `09e5e356` and grant no current runtime or design authority. |
| Arborist worktree | ⚪ | `UNCOMMITTED_CANDIDATE`; proposed art, career surface, save/lobby/probe changes are not part of current product/audit commit `09e5e356`; Arborist is not a current fourteenth career or integrated base model. |
| `OPERA_QUALITY_OVERHAUL_2026-08-09.md` | 🟠 | `SUPPORTING_CURRENT` for career-specific causal verbs, Canvas layout/input corrections and the 13-atlas/208-frame audit. Its 52-phase count, universal descriptions of the later Ballerina/Boxer specialists, and real-kart Racer payoff are historical and `SUPERSEDED`. |
| `OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md` | 🟠 | `SUPPORTING_CURRENT` for the seven-part quality rubric, reuse discipline and non-overridden career/art corrections. Its 52-phase baseline plus Ballerina, Boxer and nested-kart prescriptions are `SUPERSEDED` by the later scoped authorities and Canvas Racer reconciliation. |
| `assets_src/imagegen/opera_minigame_quality_2026-08-09/REVIEW.md` | 🔵 | `PROVENANCE_ONLY` / `SUPPORTING_CURRENT` for minigame-sheet derivation and review notes. It grants no 5/5 or runtime acceptance; owner/context/device review remains separate. |
| `assets_src/imagegen/opera_roshan_animation_2026-08-09/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY`; accepted-generation IDs, prompt hashes and derivation commands for the 13 atlases. It cannot override the review JSON, runtime hashes, specialist documents or owner acceptance. |
| `OPERA_STAGE_INTERACTION_2026-08-02.md` | 🟠 | `BINDING_DOMAIN` for paintings-as-Canvas-stages, routes, stations, magnifier and Storybook task cards where the current career table uses them. Ballerina/Boxer specialist surfaces override those defaults; generic roaming combat is not universal. Older conflicting implementation details are `SUPERSEDED`; later current defects are owned by `MA-OPERA-*`. |
| `OPERA_2D_REBUILD_2026-08-01.md` | 🟠 | `BINDING_DOMAIN` for the shared Canvas career shell and dated owner corrections, not a universal five-beat template. “3D floor bosses unchanged” is superseded by the explicit boss cut, while rival GLBs and legacy-3D fallback are also `SUPERSEDED`; later specialist documents control their careers. |
| `OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md` | 🟠 | `BINDING_DOMAIN` for `OperaCareerWorld2D` and scoped competition behavior. Its lobby information architecture is superseded and the runtime source is deleted at `09e5e356`; `7426c187` distributes careers through Castle rooms and Opera Hall keeps only Ballerina/Pop Star/Magician. It does not force rivals/meters into cooperative or specialist careers; 3D boss/outfit/presentation prescriptions are `SUPERSEDED`. Commit `e2c25878` removes the earlier lobby/kart split and reachable cut bosses; commit `09e5e356` implements exact room routing and moves `MA-OPERA-012` to `FIXED_PENDING_VERIFICATION`. |
| `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` | 🟡 | `HISTORICAL_EVIDENCE`; its request-list scope is superseded by the later August 3–9 audits/current `MA-OPERA-*` index. |
| `CODEX_OPERA_STAGE_COMPLETION_HANDOFF_2026-08-02.md` | 🟠 | `HISTORICAL_EVIDENCE` for source gaps/consumer paths; reproduce against current `MA-OPERA-*` items before generating or wiring art. |
| `OPERA_NURSERY_JOB_12_2026-08-01.md` | 🟠 | `BINDING_DOMAIN` for Job 13's cooperative Canvas behavior and save migration; its 3D player/SideScroll parent description is `HISTORICAL_EVIDENCE`. |
| `FABLE_OPERA_LAMBA_TAKEOVER_HANDOFF_2026-08-01.md` | 🟠 | `SUPPORTING_CURRENT` for the approved Lamba semantic role; the old implementation queue is `HISTORICAL_EVIDENCE`. Protected recording gap remains `MA-ACCESS-002`. |
| `FABLE_OPERA_LAMBA_TAKEOVER_STATUS_2026-08-01.md` | 🟠 | `SUPPORTING_CURRENT` for the approved Lamba semantic role; the old implementation queue is `HISTORICAL_EVIDENCE`. Protected recording gap remains `MA-ACCESS-002`. |
| `OPERA_ACT_PACING_2026-07-25.md` | 🟢 | The 2–4 minute standard and "longer must not mean more of the same". |
| `OPERA_ACT_REDESIGN_2026-07-25.md` | 🟡 | Superseded first by the five-beat rebuild and now by the career-specific 53-phase table; its *standard* (design the game the career implies) survives. |
| `OPERA_JOB_GIMMICKS_2026-07-25.md` | 🟡 | Superseded by `OPERA_ACT_REDESIGN`. Its finding — nine of twelve acts were the same verb — is why the arc exists. |
| `CODEX_ART_WORKORDER_2026-07-25.md` | 🟡 | Superseded by `CODEX_NEXTGEN_OBJECTS_2026-07-25.md`. |
| `CODEX_NEXTGEN_OBJECTS_2026-07-25.md` | 🟡 | `HISTORICAL_EVIDENCE`; its generated-file discipline may explain provenance, but all one-object-per-GLB/model construction is `SUPERSEDED`. |
| `CODEX_ASSET_REQUESTS_2026-07-21.md` | 🟡 | Early prop list, superseded by the later work orders above. |
| `OPERA_ASSET_REQUESTS_2026-07-19.md` | 🟡 | Early prop list, superseded by the later work orders above. |
| `CLAUDE_OPERA_HYBRID_LEVELS_2026-07-24.md` | 🟡 | The two-act hybrid design; superseded by the shared Canvas career shell and current specialist documents. |
| `CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md` | 🟡 | `HISTORICAL_EVIDENCE`; all 3D/hybrid runtime directions are `SUPERSEDED` by true 2D. |
| `CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md` | 🟡 | `HISTORICAL_EVIDENCE`; all 3D/hybrid runtime directions are `SUPERSEDED` by true 2D. |
| `CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21.md` | 🟡 | `HISTORICAL_EVIDENCE`; all 3D/hybrid runtime directions are `SUPERSEDED` by true 2D. |
| `CLAUDE_START_HERE_OPERA_JOB_ASSET_REGENERATION_2026-07-24.md` | 🟡 | `HISTORICAL_EVIDENCE`; all 3D/hybrid runtime directions are `SUPERSEDED` by true 2D. |
| `OPERA_JOB_FLAT_PROTOTYPE_PLAN_2026-07-21.md` | ⚪ | The 36-sheet / 576-card plan. |
| `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md` | ⚪ | Historical acceptance audit for that package; approved source art may remain in use, but its runtime structure is not current authority. |
| `OPERA_HOUSE_FLAT_ART_AUDIT_2026-07-21.md` | ⚪ | Historical acceptance audit for that package; approved source art may remain in use, but its runtime structure is not current authority. |
| `OPERA_JOB_2P5D_ART_AUDIT_2026-07-24.md` | ⚪ | Historical acceptance audit for that package; approved source art may remain in use, but its runtime structure is not current authority. |
| `OPERA_JOB_HYBRID_FINALE_ART_AUDIT_2026-07-24.md` | ⚪ | Historical acceptance audit for that package; approved source art may remain in use, but its runtime structure is not current authority. |
| `audit/opera_regeneration_audit_2026-08-01.md` | 🔵 | 74 accepted / 8 rejected candidates with SHA evidence. |

## Zone: Northern Kingdom, Ember Fortress, dungeon, reef

| Doc | | Note |
|---|---|---|
| `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; its 3D/GLB kit and build directions are `SUPERSEDED`. Dated style measurements may inform review but cannot authorize model work. |
| `NORTHERN_BLENDER_HANDOFF_FOR_CLAUDE_2026-07-20.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender/model continuation is `SUPERSEDED`. Its rejected-primitive history does not authorize rebuilding them in 2D. |
| `NORTHERN_WORLD_ART_AUDIT_2026-07-17.md` | ⚪ | Earlier northern audit; historical evidence only. |
| `NORTHERN_ASSET_BATCH_02.md` | ⚪ | Earlier northern request list; proposal history only. |
| `EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22.md` | 🟠 | `SUPPORTING_CURRENT` for the six approved 2D boards and rejection evidence; later mesh-conversion directions are `SUPERSEDED`. |
| `EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md` | 🟠 | `SUPPORTING_CURRENT` for accepted 2D concept-card evidence only; `.blend`/GLB conversion and measured-model output are `SUPERSEDED`. |
| `CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md` | 🟡 | `HISTORICAL_EVIDENCE`; Blender build order is `SUPERSEDED`. Independently binding IP-safety rules remain in current authority docs. |
| `EMBER_FORTRESS_GRAPHICS_AUDIT_2026-07-21.md` | 🟡 | Rejected earlier chain; retained only for its IP-safety framing. |
| `CLAUDE_EMBER_FORTRESS_GRAPHICS_HANDOFF_2026-07-21.md` | 🟡 | Rejected earlier chain; retained only for its IP-safety framing. |
| `DUNGEON_ART_REBUILD_AUDIT_2026-07-16.md` | ⚪ | Ten authored dungeon assets replacing primitives. |
| `REEF_REDESIGN_AUDIT_2026-07-16.md` | ⚪ | Records the **failed** first district redesign — read before redesigning the reef. |
| `LIVING_WORLD_STAGE_AUDIT_2026-07-27.md` | 🟠 | `HISTORICAL_EVIDENCE` for its dated stage inventory. Screen-space overlay claims require fresh reproduction; its dimensional rollback prescription is dismissed. |

## Characters and retired model history

| Doc | | Note |
|---|---|---|
| `assets/characters/roshan_25d/README.md` | 🟢 | `BINDING_DOMAIN`; approved RGBA atlas ownership and true Canvas/`Sprite2D` target. Its current `Sprite3D` implementation note is explicitly migration debt. |
| `CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` for approved atlas/source-gap evidence. Atlas repacking is deferred and its 3D-standee staging is `SUPERSEDED`. |
| `ROSHAN_SPRITE_CUTOFF_AUDIT_2026-08-02.md` | 🟠 | `HISTORICAL_EVIDENCE` for clipping diagnosis/verified replacements; Sprite3D sampling implementation is migration history, not final structure. |
| `CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md` | 🟡 | `HISTORICAL_EVIDENCE`; its earlier 2D frames and “2.5D” staging are superseded by the 13 current hash-audited atlases and true-Canvas runtime. |
| `assets_src/imagegen/seek_animated_2026-08-09/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the accepted-generation IDs, prompt hashes and derivation commands behind the animated Evie/Lamb-a' kit. Current runtime authority/evidence is `MA-SEEK-001`; the prompt cannot modify protected friend sources or close `MA-ACCESS-003`. |
| `NPC_3D_WORKORDER_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; Meshy/3D batch is `SUPERSEDED`, removed rather than paused. Never submit it; the missing key is not a blocker. |
| `CHARACTER_PIPELINE.md` | 🟡 | `HISTORICAL_EVIDENCE`; all model/rig/skeleton/cosmetics prescriptions are `SUPERSEDED`. |
| `CHARACTER_CUSTOMIZATION.md` | 🟡 | `HISTORICAL_EVIDENCE`; all model/rig/skeleton/cosmetics prescriptions are `SUPERSEDED`. |
| `CHARACTER_RUNBOOK.md` | 🟡 | `HISTORICAL_EVIDENCE`; all model/rig/skeleton/cosmetics prescriptions are `SUPERSEDED`. |
| `gen2/ROSHAN_V2_WORKORDER.md` | 🟡 | `HISTORICAL_EVIDENCE`; true-3D Roshan, Meshy submission, rig reuse and model fallback hierarchy are `SUPERSEDED`. |
| `docs/ROSHAN_RIG_AUDIT.md` | 🟡 | `HISTORICAL_EVIDENCE`; v4 rig measurements are retained only to explain retired work. No later rig work is authorized. |
| `docs/ROSHAN_FINAL_MODEL_2026-07-18.md` | 🟡 | `HISTORICAL_EVIDENCE`; shipping-model recommendation is `SUPERSEDED` by the 2026-08-09 2D-only decision. |
| `docs/ROSHAN_POSE_STRESS_2026-07-18.md` | 🟡 | `HISTORICAL_EVIDENCE`; model held-pose/harness work is `SUPERSEDED`, not an active QA requirement. |
| `gen2/generated/MEASURED_INTERFACE_SHEET_2026-07-19.md` | 🟡 | `HISTORICAL_EVIDENCE`; GLB/model interface measurements cannot direct current runtime work. |
| `CLAUDE_FABLE_ORNATE_SHELL_UI_HANDOFF_2026-07-29.md` | 🔵 | `HISTORICAL_EVIDENCE` for the UI lineage that produced `StorybookUI`; current UI rules live in design 06 and current runtime evidence. |
| `CLAUDE_FABLE_UI_HANDOFF_2026-07-21.md` | 🔵 | `HISTORICAL_EVIDENCE` for the UI lineage that produced `StorybookUI`; current UI rules live in design 06 and current runtime evidence. |

## Cinematics

| Doc | | Note |
|---|---|---|
| `docs/TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md` | 🟢 | The blocking production gate. Full-frame regeneration only. |
| `docs/CINEMATIC_DIRECTION_AND_INTENT_PROTOCOL.md` | 🟢 | The pre-generation intent process. Its companion. |
| `docs/OPENING_CINEMATIC_ART_DIRECTION_BRIEF_V2.md` | 🔵 | The cinematography/script brief for the opening. |
| `docs/OPENING_CINEMATIC_FULL_FRAME_PROCESS_AUDIT_2026-07-29.md` | 🔵 | The full-frame trial, including what the position-guide modes actually measured. |
| `docs/OPENING_CINEMATIC_REGENERATION_AUDIT_2026-07-28.md` | 🟡 | Explicitly marked historical: its pose-reuse/compositing methods are now forbidden. |
| `docs/CARTOON_VIDEO_PIPELINE.md` | 🔵 | The `.ogv` encoder runbook. |

## August system, Castle, combat, and Opera records

These rows close previously omitted root-level documents. A dated audit or a
document that calls itself “binding” is still bounded by the precedence in
design 00 and by later owner decisions.

| Doc | | Note |
|---|---|---|
| `ALPHA_POLISH_AUDIT_2026-08-05.md` | ⚪ | `HISTORICAL_EVIDENCE`; pre-alpha branch snapshot and change record. Its fixed/open claims require reproduction against the current head and cannot close a master-audit item. |
| `BOSS_ART_INTEGRATION_2026-08-02.md` | 🔵 | `PROVENANCE_ONLY` for the Grand Puff sheet-to-runtime mapping. It neither proves current reachability/quality nor authorizes a return to spatial boss presentation. |
| `BOSS_CONVERGENCE_DECISION_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` only for the decision to treat the authored and procedural dust-bunny work as one Grand Puff encounter. Dated placement/topology is `HISTORICAL_EVIDENCE`; current boss medium and lifecycle remain controlled by later owner decisions and the master audit. |
| `CASTLE_DREAM_HOUSE_2026-08-01.md` | 🟠 | `BINDING_DOMAIN` only for the one-finger, no-fail gallery/room route and Back behavior where those rooms still exist. Spatial-gallery construction and dated inventories are `SUPERSEDED`. |
| `CASTLE_DREAM_HOUSE_2D_REPAIR_AUDIT_2026-08-02.md` | 🟡 | `HISTORICAL_EVIDENCE`; it repaired cropped source use inside a Sprite3D implementation. Source-composition observations may be reused, but the 2.5D runtime structure is `SUPERSEDED`. |
| `CASTLE_INTERACTIONS_V2_AUDIT_2026-08-01.md` | 🟡 | `HISTORICAL_EVIDENCE`; superseded by V3/V4 and the current semantic-interaction audit. Archived-fixture and old count conclusions are not current authority. |
| `CASTLE_INTERACTION_V3_CHANGES_2026-08-02.md` | 🟡 | `HISTORICAL_EVIDENCE`; V3 inventory/change ledger superseded by V4. Asset provenance survives through the central licence ledger only. |
| `CASTLE_NATIVE_INTERACTIONS_V4_AUDIT_2026-08-04.md` | 🟠 | `SUPPORTING_CURRENT` for fixture semantics, duplicate ownership, child-interest checks, and rejection evidence. Its 2.5D/Sprite3D placement and dated exact counts are `SUPERSEDED` or must be freshly enumerated. |
| `CASTLE_PERSONAL_BANNER_STYLE_AUDIT_2026-08-10.md` | 🟠 | `PROPOSED_CANDIDATE`; authored shell-banner components and the 48-choice readability review are useful. Its Sprite3D delivery is `SUPERSEDED` by the final Canvas medium, and device/owner acceptance is explicitly still open. |
| `CHAPTER2_BIBLE_ACT_SCRIPTS_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED` / `HISTORICAL_EVIDENCE`; scripts were derived from an older all-Opera programme and dated shipped lines. They cannot add dialogue, plot dependencies, or career order without a current owner decision and exact-voice gate. |
| `CHAPTER2_BIBLE_ARC_2026-08-03.md` | 🟡 | `PARTIALLY_SUPERSEDED`; its birthday-story intent is design history, while later owner rulings in `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` control career distribution, cut bosses, and Ember-aligned future conflict. Self-declared “binding canon” does not outrank those rulings. |
| `CHAPTER2_BIBLE_SYSTEMS_2026-08-03.md` | 🟡 | `HISTORICAL_EVIDENCE`; exact build plan targets deleted/changed lobby and Opera sources. No code surface, save change, caption rule, or story trigger is authorized by this stale plan. |
| `CHAPTER2_PARTY_ROLES_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; working papers explicitly predate later role rulings. Dependency, shelf-order, and finale proposals are not current runtime authority. |
| `CHAPTER2_PLOT_DRAFT_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; rough discussion draft plus adversarial appendices. It records questions/evidence, not approved canon or implementation work. |
| `CODEX_BOSS_ART_HANDOFF_2026-08-02.md` | ⚪ | `PROPOSAL_DEFERRED`; dated art-production request. Existing accepted source provenance may be consulted, but no generation, promotion, or boss topology is authorized. |
| `CODEX_COMBAT_ART_HANDOFF_2026-08-04.md` | ⚪ | `PROPOSAL_DEFERRED`; combat-feedback asset request. Revalidate every gap against current Canvas runtime and reuse inventory before generating anything. |
| `CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md` | 🟡 | `HISTORICAL_EVIDENCE`; the old animation-state order and runtime claims are superseded by later clip work/current medium. Identity/readability observations may inform a fresh Canvas audit only. |
| `CODEX_IMP_CLIP_ART_HANDOFF_2026-08-03.md` | 🟡 | `SUPERSEDED`; the document itself marks its art order obsolete. Retained solely to explain why that order must not be actioned. |
| `CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; draft review handoff superseded for Roshan/career animation by the 13 current atlases and the Ballerina/Boxer specialists. |
| `CODEX_OPERA_EXPLORATION_HANDOFF_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; image-generation/runtime request for the former career-world exploration layer. Current Castle-room distribution and true Canvas rules require a new scoped need before reuse. |
| `CODEX_OPERA_LOGICAL_REBUILD_HANDOFF_2026-08-04.md` | 🟡 | `HISTORICAL_EVIDENCE`; asset delta for the August 4 logical rebuild. Current specialist documents and `MA-OPERA-*` defects supersede its queue and exact ledger counts. |
| `CODEX_OPERA_WIDGET_ART_FULL_AMBITION_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; broad widget-regeneration request. The current reuse-first budget, later minigame audit, and accepted hotspot/source records govern any named gap. |
| `CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md` | 🟡 | `HISTORICAL_EVIDENCE`; earlier widget transition request superseded by the August 3–9 Opera art and quality chain. It grants no current generation authority. |
| `CODEX_SKY_LAGOON_ANIMAL_ART_WORKORDER_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` only for species identity, readable silhouette, habitat, and reuse checks tied to its parent audit. Sprite3D/shadow placement and any unverified art queue are `SUPERSEDED`. |
| `CODEX_WATER_FX_WORKORDER_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` for a shared, child-readable 2D water-FX vocabulary and provenance discipline. Jolt/spatial consumers and the dated production queue are `SUPERSEDED` or deferred. |
| `COMBAT_DIFFICULTY_AUDIT_2026-08-04.md` | 🟠 | `SUPPORTING_CURRENT` for no-fail difficulty analysis, mercy separation, and the need for meaningful input. Numeric tuning, line references, and closure claims are `HISTORICAL_EVIDENCE` requiring current probes/play evidence. |
| `COMBAT_TUTORIAL_CODEX_ASSETS_2026-08-01.md` | 🟠 | `SUPPORTING_CURRENT` for wordless, one-finger, no-fail tutorial intent and source provenance. Spatial presentation is `SUPERSEDED`; dated runtime reachability must be reverified under the current audit. |
| `COMBO_SYSTEM.md` | 🟠 | `BINDING_DOMAIN` for the owner-approved, encounter-focus-only horizontal swipe exception and the no-fail/mercy/visual-demonstration grammar. Boss clients, exact timings, spatial camera behavior, and implementation status are `HISTORICAL_EVIDENCE` subordinate to current runtime evidence. |
| `COZY_GAP_AUDIT_2026-08-03.md` | ⚪ | `HISTORICAL_EVIDENCE`; useful pre-alpha cozy-design questions and proposals, not a current defect list. Reproduce any claimed gap before opening work. |
| `DUST_BUNNY_BOSS_2026-08-02.md` | 🟠 | `BINDING_DOMAIN` only for the owner-directed Grand Puff identity, gentle no-loss behavior, obvious prompting, and distinct encounter semantics. Generic 3D arena/model details and dated code contracts are `SUPERSEDED` or must be reverified. |
| `DUST_BUNNY_BOSS_STRESS_TEST_2026-08-02.md` | 🔵 | `HISTORICAL_EVIDENCE` for its simulated timing/fun review. It is not current child/device evidence and cannot establish reachability, visual acceptance, or present tuning. |
| `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/README.md` | ⚪ | `HISTORICAL_EVIDENCE`; portable companion to the superseded draft animation handoff. Its previews do not supersede current atlas hashes or specialist reviews. |
| `HOURLY_INTEGRATION_AGENT.md` | 🟠 | `SUPPORTING_CURRENT` only where it restates the protected dev/master, green-probe, and no-force-push rules. Its scheduled branch enumeration and autonomous integration procedure is `HISTORICAL_EVIDENCE`, not authority to operate or promote; current `AGENTS.md` and workflow policy control. |
| `IMP_AI.md` | 🟠 | `BINDING_DOMAIN` for the shared imp decision vocabulary, generous telegraphs, mercy, and no-fail behavior where `ImpAI` is still a client. Spatial steering/arena details and exact implementation claims are `HISTORICAL_EVIDENCE` subject to current probes. |
| `LIGHTING_2P5D_AUDIT_2026-08-02.md` | 🟡 | `HISTORICAL_EVIDENCE`; its 2.5D lighting system and Forward/3D prescriptions are `SUPERSEDED`. Mobile readability observations may inform a fresh Canvas audit. |
| `MENU_UI_SYSTEM_AUDIT_2026-08-01.md` | 🔵 | `SUPPORTING_CURRENT` for menu taxonomy, non-reader checks, cancellation, and input-ownership questions. Screen counts and pass/fail findings are dated and require a current census. |
| `MIC_SPELLS.md` | ⚪ | `PROPOSAL_DEFERRED`; landed microphone prototype and owner-signoff record, not approval of a default-on permission/privacy surface. Current runtime, device, privacy, accessibility, and owner gates must precede any authority claim. |
| `OPERA_EXPLORATION_DESIGN_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; former career-world exploration design. The Castle-room distribution and current per-career implementations supersede its universal world structure. |
| `OPERA_FEEDBACK_AUDIT_2026-08-03.md` | 🟠 | `HISTORICAL_EVIDENCE` for per-game causal-feedback defects and a useful audit method. Treat each finding as stale until reproduced against the current specialist/runtime version. |
| `OPERA_FRAMING_PACING_ANIMATION_AUDIT_2026-08-03.md` | 🟠 | `HISTORICAL_EVIDENCE`; framing, stiffness, low-resolution, and pacing observations predate current atlases/specialists. Its “explore the background” solution is superseded by exact Castle-room distribution; reproduce residual defects. |
| `OPERA_INGREDIENT_INTERACTION_DIRECTION_2026-08-03.md` | 🟠 | `BINDING_DOMAIN` for the owner-directed causal principle that represented ingredients must receive meaningful, visceral one-finger interaction. Older beat examples are `HISTORICAL_EVIDENCE`; later career-specific authorities control exact beats, and the document is not a universal recipe template. |
| `OPERA_LOGICAL_REBUILD_SPEC_2026-08-04.md` | 🟠 | `SUPPORTING_CURRENT` for non-overridden cause/effect, uniqueness, curiosity, mercy, and child-readable interaction principles. Coordinates, counts, old career-world/lobby structure, and self-declared binding rulings are `SUPERSEDED` by August 9–13 authorities. |
| `OPERA_MASTER_PACKAGE_2026-08-04.md` | 🟠 | `HISTORICAL_EVIDENCE` / `SUPPORTING_CURRENT` only for non-overridden causal-gameplay and narrative questions. Current distribution, specialists, phase inventories, boss cuts, and `MA-OPERA-*` states supersede its programme-wide plan. |
| `OPERA_NARRATIVE_AUDIT_2026-08-02.md` | ⚪ | `HISTORICAL_EVIDENCE`; analysis-only diagnosis of the older Opera narrative. It asks useful questions but cannot supply canon, voice lines, or current career order. |
| `OPERA_QUALITY_PLAYABILITY_AUDIT_2026-08-05.md` | 🟠 | `HISTORICAL_EVIDENCE`; version-specific 13-act ratings and child-playability critique. Current versions must be scored in the master audit; no old pass/fail conclusion transfers automatically. |
| `OPERA_WIDGET_ART_CONCEPTS_2026-08-03.md` | ⚪ | `PROPOSAL_DEFERRED`; ambitious concept inventory for an older widget implementation. Reuse only after a current named gap and provenance/runtime review. |
| `OPERA_WIDGET_INPUT_AUDIT_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` for one-finger hit-area, drag ownership, visible causality, and mercy criteria. Every coordinate and defect claim is `HISTORICAL_EVIDENCE` requiring current reproduction. |
| `OPERA_WORLD_OBJECT_CENSUS_2026-08-03.md` | 🟡 | `HISTORICAL_EVIDENCE`; old four-tile career-world inventory and coordinate rulings were superseded by the master package and then the current Castle-room/specialist chain. |
| `RELEASE_GATE_VERDICT_2026-08-05.md` | ⚪ | `HISTORICAL_EVIDENCE`; do-not-promote verdict for a named 2026-08-05 branch, not the current head. Its escape/reachability failures remain lessons, not current failures unless reproduced. |
| `TOUCH_AUDIT_2026-08-03.md` | 🟠 | `HISTORICAL_EVIDENCE` for the reported wrong-direction Sky Lagoon symptom and touch-method review. Current touch rating/evidence lives in the master audit; reproduce before assigning a present defect. |
| `WATER_PHYSICS_EVALUATION_2026-08-02.md` | 🟡 | `HISTORICAL_EVIDENCE`; Jolt water-transition census and spatial rollout plan are `SUPERSEDED` by true Canvas and removal of 3D physics debt. |

## Asset policy, protected-audio notes, and source provenance

Source-package records establish lineage at most. They do not prove that an
asset is reachable, current, visually accepted, or safe to promote.

| Doc | | Note |
|---|---|---|
| `art_library/candidates/castle_differentiation_2026-07-17/README.md` | ⚪ | `UNAPPROVED_CANDIDATE_EVIDENCE`; preserves nine studies byte-for-byte and explicitly denies runtime approval. No current generation or promotion authority. |
| `assets/ART_GENERATION_CONTRACT.md` | 🟠 | `PARTIALLY_SUPERSEDED`; protected-source, runtime-context scoring, reuse, palette, motif, Mobile, provenance, and placement principles survive. Its Blender/Meshy/GLB pipelines, 3D budgets, named active queue, and claim of self-contained current authority are `SUPERSEDED` by the final Canvas medium and August reuse decision. |
| `assets/OBJECT_GENERATION_AUDIT_LOG.md` | 🟠 | `SUPPORTING_CURRENT` for evidence classes, recurring generator-failure taxonomy, object completeness, runtime-context review, and no-bulk-generation caution. Blender/model rules, old work queue, dated counts, and any promotion state are `SUPERSEDED` or historical. |
| `assets/audio/voices/VOICE_MANIFEST.md` | 🟠 | `SUPPORTING_CURRENT` only for filename/fallback history and identification of irreplaceable family recordings. Its dated TTS roster, Gabby entry, regeneration/enhancement directions, and inventory are `HISTORICAL_EVIDENCE`, not authority to modify protected audio; current `AGENTS.md`, exact-voice findings, licences, and runtime evidence control. |
| `assets/characters/roshan_25d/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the original Roshan atlas generation. “2.5D” and any standee use are historical; current runtime authority is the sibling README plus current atlas/audit records. |
| `assets/characters/roshan_25d/PROMPTS_4X.md` | 🔵 | `PROVENANCE_ONLY` for the quadrupled animation expansion. It cannot grant identity, runtime, visual, or owner acceptance and does not authorize regeneration. |
| `assets/props/story/play_swing_PROMPT.md` | 🔵 | `PROVENANCE_ONLY` for the playground swing sprite. The owner image was a style reference only; this record grants no runtime acceptance or permission to alter protected Roshan art. |
| `assets_src/blender/qa_outfits_floor2/ASSET_LICENSES.md` | 🟡 | `SOURCE_SCOPED_PROVENANCE`; records retired GLB/outfit sources only. The root `ASSET_LICENSES.md` is the binding ledger, and the model pipeline is `SUPERSEDED`. |
| `assets_src/blender/qa_pearl_castle_kit/RUNTIME_EVIDENCE.md` | ⚪ | `HISTORICAL_EVIDENCE`; review screenshots for rejected/retired Castle kit work, explicitly not runtime textures. They cannot satisfy current exact-engine or visual gates. |
| `assets_src/castle/logo_studio_v2/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the personalized-banner V2 source family. Candidate/owner/device/Canvas acceptance remains open under the banner audit and master rules. |
| `assets_src/castle/room_regenerations/room_kitchen_fullframe_v2_provenance.md` | 🔵 | `PROVENANCE_ONLY`; records a dated accepted Kitchen candidate and source correction. Old-branch integration language is not current runtime or owner acceptance. |
| `assets_src/castle/room_regenerations/room_kitchen_fullframe_v3_provenance.md` | 🔵 | `PROVENANCE_ONLY`; records the v3 kettle correction and source lineage. Current reachability, medium, and visual status require current evidence. |
| `assets_src/concepts/cc0_ocean_replacements_2026-07-22/ECOLOGY_SOURCES.md` | 🔵 | `SOURCE_PROVENANCE_ONLY`; ecological references informed context boards and supplied no delivery pixels. It cannot authorize assets, placement, or current habitat claims. |
| `assets_src/concepts/cc0_ocean_replacements_2026-07-22/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the old CC0 replacement concept generation; no current batch, 3D conversion, or promotion authority. |
| `assets_src/concepts/cc0_ocean_replacements_2026-07-22/README.md` | 🟡 | `HISTORICAL_EVIDENCE`; concept-only 2D-to-3D handoff. Source inventory/provenance may be consulted, while all model conversion and “live addendum” work status is `SUPERSEDED`. |
| `assets_src/concepts/cc0_ocean_replacements_2026-07-22/REGEN_35_PROMPT_PLAN.md` | ⚪ | `PROPOSAL_DEFERRED`; corrected historical prompt scope, not permission to run the batch. Reuse-first and named-current-gap gates apply. |
| `assets_src/concepts/dust_bunny_animated_2026-07-27/BOSS_ANIMATION_DESIGN.md` | 🔵 | `PROVENANCE_ONLY` / historical motion-design evidence for the 2D dust-bunny sheet. Current encounter behavior and accepted delivery frames must be verified separately. |
| `assets_src/concepts/dust_bunny_animated_2026-07-27/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for dust-bunny image generation; cannot authorize regeneration, identity acceptance, or runtime use. |
| `assets_src/concepts/dust_bunny_animated_2026-07-27/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` for the animated dust-bunny sprite-card lineage. Its dated project ordering/status is not a current runtime conclusion. |
| `assets_src/concepts/ember_fortress_claude_2026-07-22/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the six Ember concept boards; later true-Canvas and current Ember audits control use. |
| `assets_src/concepts/ember_fortress_claude_2026-07-22/expansion_40/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for expansion-40 concepts; any Blender/GLB conversion path is `SUPERSEDED`, and acceptance does not transfer to runtime. |
| `assets_src/concepts/ocean_kingdoms_2026-07-22/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for untouched reference-sheet generations; no runtime or design authority. |
| `assets_src/concepts/ocean_kingdoms_2026-07-22/README.md` | 🟡 | `HISTORICAL_EVIDENCE`; explicitly reference-only and formerly a 3D reconstruction handoff. The reconstruction direction is `SUPERSEDED`. |
| `assets_src/concepts/opera_house_flat/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for Pearl Opera flat-art sources. Later current Opera authorities determine which art remains used and accepted. |
| `assets_src/concepts/opera_jobs_2p5d_2026-07-24/PROMPTS.md` | 🟡 | `PROVENANCE_ONLY` for accepted source images; the 2.5D/hybrid Act-I structure is `SUPERSEDED`. |
| `assets_src/concepts/opera_jobs_flat_2026-07-21/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the flat-prototype source batch; it cannot revive the old universal career plan. |
| `assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/PROMPTS.md` | 🟡 | `PROVENANCE_ONLY` for wide finale keys; the hybrid two-act runtime structure is `SUPERSEDED`. |
| `assets_src/concepts/opera_nursery_2026-08-01/GENERATED_ART.md` | 🔵 | `PROVENANCE_ONLY` for Nursery source generation and alpha conversion. Current Job 13 behavior, runtime hashes, and visual acceptance are separate. |
| `assets_src/concepts/opera_regeneration_2026-08-01/OPERA_CODEX_QA_2026-08-02.md` | ⚪ | `HISTORICAL_MACHINE_EVIDENCE`; a PASS over that source batch and its dated 60/60 census, not current runtime, context, device, or owner acceptance. |
| `assets_src/concepts/opera_regeneration_2026-08-01/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the August 1 Opera regeneration package; later current atlases/specialists and reuse rules control all use. |
| `assets_src/concepts/opera_rivals_2026-07-29/README.md` | 🟡 | `PROVENANCE_ONLY` for rival artwork sources. Rival GLB/presentation directions are `SUPERSEDED`; no requirement to expose rivals transfers from this record. |
| `assets_src/concepts/opera_stage_completion_2026-08-02/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for stage-completion sprites and deterministic alpha work. Current source gaps and runtime consumers must be re-enumerated. |

## Generated-art package records

| Doc | | Note |
|---|---|---|
| `assets_src/fairy_v2/GENERATED_ART.md` | 🟡 | `PROVENANCE_ONLY`; V2 sources are explicitly historical and its runtime pond plates were superseded by V5. |
| `assets_src/fairy_v4/GENERATED_ART.md` | 🔵 | `PROVENANCE_ONLY` for the V4 readability-cue sources. It does not prove current use or visual acceptance. |
| `assets_src/fairy_v5/GENERATED_ART.md` | 🔵 | `PROVENANCE_ONLY` for the single-canvas V5 panorama and protected-source declaration. Current Fairy runtime/quality gates remain separate. |
| `assets_src/imagegen/boot_splash_2026-08-01/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the boot-splash generation and its non-deterministic-tool disclosure. |
| `assets_src/imagegen/boot_splash_2026-08-01/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` for the intended splash-to-intro continuity and file lineage; current boot behavior and device evidence must be verified elsewhere. |
| `assets_src/imagegen/castle_dream_house_2026-08-01/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY`; reference-only Dream House outputs, explicitly not runtime backgrounds or automatic approval. |
| `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for Dream House repair sources. Its then-current Sprite3D consumer is `SUPERSEDED`; Canvas integration/acceptance requires current evidence. |
| `assets_src/imagegen/castle_interactions_2026-08-01/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for preservation-focused Castle prop extractions. It cannot establish current fixture inventory or semantic correctness. |
| `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for Main Hall redraw masters and hashes. Runtime selection, true-Canvas composition, and owner acceptance are separate. |
| `assets_src/imagegen/castle_room_buttons_2026-08-01/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for room-button masters and derivation. It does not authorize text-dependent navigation or certify current touch use. |
| `assets_src/imagegen/combat_tutorial_2026-08-01/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the combat-tutorial generated batch; source QA does not prove current reachability or child comprehension. |
| `assets_src/imagegen/day_one_pool_2026-08-22/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the five selected Day One Mermaid Pool cleanup masters, exact prompt set, alpha correction, and runtime normalization. Runtime selection, child readability, save behavior, and visual acceptance require current code and probe evidence. |
| `assets_src/imagegen/day_one_pool_activities_2026-08-23/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the seven selected skimmer, debris, basket, corrected waterfall, scrubber, mouth-clear seahorse, and separable mouth-plug generations, including hashes, rejected attempts, and whole-canvas runtime derivation. It grants no device, child, owner, or cinematic-frame acceptance. |
| `assets_src/imagegen/day_one_art_studio_2026-08-23/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the Day One Art Studio loose-supply, grime, and cleaning-brush generations, rejected attempts, deterministic alpha preparation, world-depth integration record, and Codex runtime review. It grants no target-device, child, or owner acceptance. |
| `assets_src/imagegen/day_one_pool_natural_integration_2026-08-23/PROMPT.md` | 🔵 | `PROVENANCE_ONLY`; exact prompt for the natural-integration reference plate. It grants no runtime, geometry, identity, device, child, or owner authority. |
| `assets_src/imagegen/day_one_pool_natural_integration_2026-08-23/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY`; records the native reference plate hash, built-in ImageGen method, and reference-only disposition. The plate must not replace the approved V4 room or fixture art. |
| `assets_src/imagegen/day_one_pool_dust_bunny_swimmer_2026-08-24/PROMPT_AND_PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the accepted diagonal swimming dust-bunny generation, transparent-alpha correction, normalized runtime derivative, hashes, exact prompts, rejected attempt, and Luna review. Runtime placement, water confinement, filled-bathtub reuse, device readability, and owner acceptance require current code, probes, and visual evidence. |
| `assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for imp animation-state art and the dated 179-file delivery. Current clip routing/medium/identity acceptance requires current evidence. |
| `assets_src/imagegen/mermaid_pool_room_2026-08-02/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the accepted Mermaid Pool v3 source. Old-branch “production” status does not by itself prove current runtime selection or visual acceptance. |
| `assets_src/imagegen/opera_borderless_doctor_2026-08-10/PROMPT.md` | 🔵 | `PROVENANCE_ONLY` for the borderless Doctor patient candidate and reference role; no runtime or owner acceptance. |
| `assets_src/imagegen/opera_borderless_doctor_2026-08-10/REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; Codex visual QA accepted the isolated candidate while owner/human review remains explicitly pending. It cannot award 5/5 or prove runtime context. |
| `assets_src/imagegen/opera_borderless_pitstop_2026-08-10/PROMPT.md` | 🔵 | `PROVENANCE_ONLY` for the borderless Racer pit-stop candidate and reference role; no runtime or owner acceptance. |
| `assets_src/imagegen/opera_borderless_pitstop_2026-08-10/REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; Codex visual QA accepted the isolated candidate while owner/human review remains explicitly pending. It cannot award 5/5 or prove runtime context. |
| `assets_src/imagegen/opera_codex_2026-08-02/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the August 2 Opera source batch. Its “binding style” phrase is package-scoped historical direction, not higher authority than design 02/06 or later Opera reviews. |
| `assets_src/imagegen/opera_diegetic_hotspots_2026-08-09/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the named Magician rope hotspot gap and generation. It cannot certify integration or owner acceptance. |
| `assets_src/imagegen/opera_diegetic_hotspots_2026-08-09/REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; isolated Magician rope attempt passed Codex review with owner/human review pending. Runtime context and exact consumer remain separate gates. |
| `assets_src/imagegen/roshan_playground_cutoff_2026-08-09/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` / `SUPPORTING_CURRENT` for the named 2D cutoff repair, accepted generation path, and uniform whole-asset processing. It does not independently prove current runtime routing, identity, device, child, or owner acceptance. |
| `assets_src/imagegen/water_fx_2026-08-02/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for six shared 2D water-FX sources and alpha conversion. Spatial/Jolt consumers are historical; current Canvas use must be verified. |

## Sky Lagoon source and candidate ledgers

| Doc | | Note |
|---|---|---|
| `assets_src/sky_lagoon/ambient_animals_2026-07-29/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for project-original ambient-animal generations; no runtime, habitat, identity, or owner acceptance. |
| `assets_src/sky_lagoon/ambient_animals_2026-07-29/README.md` | 🟠 | `SOURCE_PACKAGE_EVIDENCE` for provenance, protected-source separation, and intended ambient roles. Sprite3D/shadow placement and dated integration status are `SUPERSEDED` or unverified. |
| `assets_src/sky_lagoon/castle_symmetry_2026-07-29/README.md` | 🔵 | `PROVENANCE_ONLY` for the balanced-castle source correction. Current source selection and full-scene acceptance require current evidence. |
| `assets_src/sky_lagoon/cohesion_pass_2026-07-19/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for review-only cohesion sheets; no deterministic seed or runtime authority. |
| `assets_src/sky_lagoon/cohesion_pass_2026-07-19/README.md` | ⚪ | `HISTORICAL_EVIDENCE`; explicitly review-only model direction with no runtime replacement. Any 3D/model implication is `SUPERSEDED`. |
| `assets_src/sky_lagoon/congruency_rebuild_2026-07-27/README.md` | 🔵 | `PROVENANCE_ONLY` for the approved 3:1 mural and subject-source continuity. Runtime promenade/spatial structure is not current authority. |
| `assets_src/sky_lagoon/hd_grid_2026-07-28/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the 6144×2048 twelve-edit generation record. Current clean-plate integrity and Canvas slicing are governed by the reductive handoff and audit evidence. |
| `assets_src/sky_lagoon/living_card_v2_2026-07-29/README.md` | 🟡 | `PROVENANCE_ONLY`; records fireplace-smoke source work. Living-card/Sprite3D delivery is `SUPERSEDED`; no current runtime acceptance. |
| `assets_src/sky_lagoon/playground_revision_2026-07-29/README.md` | 🔵 | `PROVENANCE_ONLY` for the playground raster revision and non-model method. Current play-space readability and Roshan overlap require current captures. |
| `assets_src/sky_lagoon/reductive_rebuild_2026-07-28/README.md` | 🔵 | `PROVENANCE_ONLY` / `SUPPORTING_CURRENT` for the clean-plate, unique-object, 6×2 source lineage. Old Sprite3D assembly is superseded by Canvas reconstruction. |
| `assets_src/sky_lagoon/runtime_candidate_046fbcf/README.md` | ⚪ | `HISTORICAL_EVIDENCE`; candidate captured on Godot 4.4, not the exact 4.7.1 baseline. Its then-green technical result and review status cannot close current Sky gates. |
| `assets_src/sky_lagoon/runtime_rejected_1e2412a/README.md` | ⚪ | `REJECTION_EVIDENCE`; preserves why candidate `1e2412a` failed human visual review. Never promote or treat green gameplay probes as visual acceptance. |
| `assets_src/sky_lagoon/runtime_rejected_584d3a0/README.md` | ⚪ | `REJECTION_EVIDENCE`; preserves why candidate `584d3a0` failed human visual review. Never promote or treat technical validity as visual acceptance. |
| `assets_src/sky_lagoon/runtime_rejected_9da8457/README.md` | ⚪ | `REJECTION_EVIDENCE`; preserves why candidate `9da8457` failed human visual review. Never revive without a newly scoped audit and accepted full-scene evidence. |
| `assets_src/sky_lagoon/tree_card_rebuild_2026-07-28/README.md` | 🟡 | `PROVENANCE_ONLY` for tree-card raster sources. Sprite3D card delivery is `SUPERSEDED`; background/object ownership must follow current Canvas rules. |

## Retired content, visual reviews, and rollback archives

| Doc | | Note |
|---|---|---|
| `attic/gabby/README.md` | 🟢 | `BINDING_DOMAIN`; records the owner-directed IP hold. Gabby remains out of the build and preserved only in the attic; do not reintroduce her without an owner-approved original redesign. |
| `audit/combat_tutorial_2026-08-01/README.md` | ⚪ | `HISTORICAL_VISUAL_EVIDENCE`; records one phone-profile capture/review artifact. It is not Lenovo device, child, owner, reachability, or current-head acceptance. |
| `backups/art_pre_castle_final_polish_2026-07-18/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; identifies a byte-preserved pre-polish snapshot. Never restore it wholesale over current Canvas/protected/save work; use the dependency-aware rollback process. |
| `backups/art_pre_castle_opera_2026-07-18/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; preserves the earlier Opera-gate blockout. Its old master references and 3D/blockout content are history, not a recommended current state. |
| `backups/art_pre_castle_pearl_2026-07-18/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; documents a pre-Pearl archive. Restoration requires exact target/dependency review and cannot override later owner decisions. |
| `backups/art_pre_castle_visibility_2026-07-18/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; source/runtime snapshot for an old material-visibility pass. Retired GLBs are not current fallback assets. |
| `backups/art_pre_dungeon_v2_2026-07-16/MANIFEST.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; manifest for pre-V2 dungeon scripts/assets. Its restore recipe is historical and must pass current medium, dependency, and probe gates before any selective use. |
| `backups/art_pre_landmarks_2026-07-15/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; records pre-landmark external assets and procedural state. It grants no present licence, visual, or runtime acceptance. |
| `backups/art_pre_pass35_2026-07-16/MANIFEST.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; byte-preserved pre-pass files. Do not copy the set wholesale; select only through the current `CHG-*`/dependency-aware rollback workflow. |
| `backups/art_pre_remediation_2026-07-15/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; pre-remediation raster/model snapshot. Current protected, licence, Canvas, and acceptance rules still apply to any selective recovery. |
| `backups/art_pre_score3_2026-07-15/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; pre-score-3 raster snapshot. It is not a quality recommendation and cannot reverse later accepted work by directory copy. |
| `backups/art_pre_sky_lagoon_5of5_2026-07-19/README.md` | ⚪ | `ROLLBACK_EVIDENCE_ONLY`; pre-candidate Sky snapshot. The “5/5” filename is not an owner score, and its direct-copy recipe is subordinate to current Canvas and rollback gates. |
| `docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02.md` | 🟠 | `SUPPORTING_CURRENT` for species anatomy, footing, habitat, silhouette, and full-scene comparison criteria. Its five-card census, Sprite3D/shadow fixes, old line references, and acceptance state are `SUPERSEDED` or require current reproduction. |

## Retired generation-two programme and generated tooling

| Doc | | Note |
|---|---|---|
| `gen2/CODEX_IMPROVEMENT_PROTOTYPE_BATCH_2026-07-18.md` | ⚪ | `HISTORICAL_EVIDENCE`; explicitly E1 review-only prototypes that must not be wired or promoted. Current reuse-first and true-Canvas decisions supersede its programme context. |
| `gen2/GEN2_REBUILD_WORKORDER.md` | 🟡 | `HISTORICAL_EVIDENCE`; the gen-2 strangler/model rebuild programme, Meshy/Blender/GLB hierarchy, and staged 3D replacement are `SUPERSEDED`. It grants no current fallback or generation authority. |
| `gen2/UI_PROTOTYPE_REVISIONS_2026-07-19.md` | ⚪ | `HISTORICAL_EVIDENCE`; E1 review-only UI prototypes. Useful isolated critique cannot establish current runtime or owner acceptance. |
| `gen2/generated/ANALYSIS.md` | 🔵 | `HISTORICAL_MACHINE/HUMAN_EVIDENCE` for 123 isolated roles and recorded generator flaws. KEEP/REGEN calls are not runtime scores or current promotion decisions; the recurring flaw taxonomy survives through the object audit log. |
| `gen2/generated/FABLE_KIT_RUNTIME_AUDIT_2026-07-19.md` | ⚪ | `HISTORICAL_EVIDENCE`; constructor self-audit of a retired 3D kit on an old runtime. It cannot satisfy independent, exact-engine, current-medium, or owner gates. |
| `gen2/prompts/stickerify_isolator_v1.md` | ⚪ | `PROMPT_ARCHIVE_ONLY`; owner-supplied generic isolation prompt. It is not a current asset request and cannot bypass protected-source, provenance, reuse, or full-frame rules. |
| `gen2/prompts/style_transfer_v10.14.md` | ⚪ | `PROMPT_ARCHIVE_ONLY`; owner-supplied historical style-transfer prompt. It does not override the current design language or authorize generation from protected material. |
| `gen2/ui_prototypes_2026-07-19/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for review-only UI prototype generations; no current runtime, accessibility, or owner acceptance. |
| `tools/CHUCK_ANIMATION_SPEC.md` | 🟡 | `HISTORICAL_EVIDENCE`; GLB/clip acceptance specification is `SUPERSEDED` by the final Canvas medium. It is not authority to alter protected Chuck assets or resume model work. |
| `tools/out/lighting_image_audit.md` | 🔵 | `GENERATED_REPORT`; regenerate from the current tree, never hand-edit or treat its dated 748-file result as current visual acceptance. |

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
| Seek uses animated Evie/Lamb-a' and high-grade Canvas meadow art, never its superseded vinyl/preview pair | `MA-SEEK-001`, design 01/02/04/05/06, `assets_src/imagegen/seek_animated_2026-08-09/PROMPTS.md` for provenance only |
| Current Ballerina/Boxer specialist authority | `BALLERINA_PARTY_REBUILD_2026-08-09.md`, `design/BOXING_GAME_PROJECT_2026-08-09.md`, design 01–05, `audit/MASTER_AUDIT_2026-08-09.md` |
| Thirteen careers belong in Castle rooms; Opera Hall is one three-career venue | owner direction `7426c187`, `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` §10, `DL-INT-12`, `MA-OPERA-012`, design 00/01/04/06 |
| Curtain Dragon/Shadow Phantom/Midnight Maestro are cut; save slots 4/9/14 are tombstones | owner cut `3d1236fe`, section-17 clarification `ef2fd982`, `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` §§16–17, `DL-INT-13`, `DL-SAVE-06`, `MA-OPERA-011`, design 00/01/03/04/06 |
| Music inventory, authorship, routing and open listening gates | `MUSIC_AUDIT_2026-08-09.md`, design 01/03/05, `ASSET_LICENSES.md`, score and manifest machine data |
