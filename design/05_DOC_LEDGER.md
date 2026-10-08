# Master design — document ledger

_Initial 149-document index: 2026-08-02. Targeted authority reconciliation:
2026-08-09. Merge synchronization: 2026-08-12. Exhaustive 316-document
classification and exact-head closure verification: 2026-08-13._

This ledger is exhaustive for the repository's current Git-declared inventory
of tracked or intended-tracked Markdown paths. Obtain current counts from
`python -B tools/audit_document_authority.py`; the 315/316-path checkpoints
below are historical measurements, not a fixed inventory requirement.
Every path reported by the
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

Scoped owner direction 2026-09-30 is recorded in design 06's `DL-INT-12`
exception and the master task index: temporary Opera left-elevator access to
all live jobs for development review, with fresh runs and isolated child
progress/rewards/checkpoints. The structured
[impact](audit_impacts/opera-job-playtest-20260930.json) records implementation
and evidence; this does not grant device, child, owner or whole-game acceptance.

**Legend**

| Doc | | Note |
|---|---|---|
| `design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md` | 🟣 | `PROPOSED / CANDIDATE`; owner-commissioned isolated true-2D faerie-half magic restoration prototype: arborist tree care, harvest, chef slices, butterfly picnic and flower shooter using existing art and additive synthetic cues. Production Chapter 3 route/rescue/save/rewards are unchanged; device/child/owner and final art/audio acceptance remain pending. Includes the scoped stale Chapter Two/exact Opera voice integration repair; no audio bytes or finding closure. |
| `design/VISUAL_REPAIR_PLAN_2026-09-26.md` | 🔵 | `SUPPORTING_CURRENT`; owner-requested repair register, four-panel Opera production plan, replay safeguards and native Aseprite/aesthetic methods. September 30 follow-up records Rumi tail recovery and craft-board backing repair, with kitchen/Eagle alpha investigation. Partial implementation and pending native-art/runtime/device gates are explicit; no release or finding closure. |
| `design/PAINTER_ENGINE_PROTOTYPE_2026-09-16.md` | 🟣 | `PROPOSED / CANDIDATE`; owner-commissioned single standalone Painter prototype with a pinned Pixelorama fill import, unchanged Roshan graphics and isolated artwork persistence. No career/chapter integration, device/child/owner acceptance or master-audit closure. |
| `audit/OVERNIGHT_RECUT_FRAME_AUDIT_2026-09-12.md` | 🔵 | `SUPPORTING_CURRENT`; fresh sampled/native-frame review of the 3150-frame overnight Resolve render and eighteen bounded repair/conditional cards. Owner direction: recognizable big bunny, soapy scrubbing obscures form, concept friend jumps while casing collapses and dust scatters. Includes original-book Eagle correction and exact Daddy/attic locks. No generated-frame, human, runtime, device or delivery acceptance. |
| `assets_src/cinematics/grok_builder_2026-09-14/README.md` | 🔵 | `SUPPORTING_CURRENT`; single builder import/navigation for the shared character, location, prop, event, shot and reference database. Consolidates scoped Day One corrections and Chapter 2 planning; historical boards retain explicit conflicts. Does not grant generation, delivery, runtime, device, child or whole-game acceptance. |
| `assets_src/cinematics/overnight_recut_repairs_2026-09-12/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; operator index for the overnight-cut repair archive, exact source-frame mappings, new beat boards and draft Grok shot cards. The newer two-window stone attic governs this packet instead of the older wooden arena. Remote archive completeness, opening readiness and delivery acceptance remain separate. |

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
| `CLAUDE.md` | 🟢 | `BINDING_OPERATIONAL`; mirrors 2026-10-03 animation/Aseprite/budget controls. Exact-engine, true Canvas, security, protected sources, save/release and GitHub handoff delivery remain. DL-ASSET-08 and DL-CIN-16 retain source-specific limits; the 2026-09-30 Claude written-handoff-only role rule remains binding. |
| `AGENTS.md` | 🟢 | `BINDING_OPERATIONAL`; owner revision 2026-10-03 supersedes compulsory per-frame still generation and permits final 2D/video animation with identity/motion/provenance/device checks, preferring Aseprite and bounded retries. Security, protected sources, save/release, GitHub handoff delivery, DL-ASSET-08 book and DL-CIN-16 selected-cut restrictions retain their scopes. No historical pixel acceptance. |
| `SECURITY.md` | 🟢 | `BINDING_OPERATIONAL`; threat model and agent rules. A content/design decision cannot weaken it. Summarized in 03 §8. |
| `BACKUP.md` | 🟢 | `BINDING_OPERATIONAL`; four backup layers and restore recipes. |
| `ASSET_LICENSES.md` | 🟢 | `BINDING_LEDGER`; one provenance/licence entry per new asset in the same commit, including the merged Opera/minigame/atlas and 42-cue music deliveries. Provenance does not grant art acceptance. Row count not asserted here; 2026-09-30 append-only Chapter Two synthetic speech and source-bound Mobile review captures; protected originals unchanged. |
| `WORKFLOW_BRANCHING_2026-07-18.md` | 🟢 | `BINDING_OPERATIONAL`; the dev/master promotion rule. Summarized in 03 §6. |
| `docs/ANDROID_RELEASE.md` | 🟢 | `BINDING_OPERATIONAL`; signing-key safety — a key change destroys the child's save. |
| `design/00_MASTER_INDEX.md` | 🔵 | `SUPPORTING_CURRENT`; authority navigation and precedence, explicitly not an exhaustive ledger. |
| `design/01_GAME_DESIGN.md` | 🟢 | `BINDING_DOMAIN` within the newer owner decision/design-language scope; 2.5D/3D history explicitly superseded. Its Roshan identity-anchor sentence ("lavender clothing, green-right / pink-left tail") is superseded by the 2026-09-30 owner decision recorded in `MA-DOC-008`: the approved atlases are Roshan's primary identity authority, and her tail is iridescent, lavender-pink-purple or rainbow depending on the light. |
| `design/02_ART_DIRECTION.md` | 🟢 | `BINDING_DOMAIN`; true-2D visual medium plus the protected-content and absolute cinematic rules. Its Roshan anchor sentence in section 5 is superseded by the 2026-09-30 owner decision recorded in `MA-DOC-008`: the approved atlases are Roshan's primary identity authority, and her tail is iridescent, lavender-pink-purple or rainbow depending on the light. |
| `design/03_TECHNICAL_ARCHITECTURE.md` | 🟢 | `BINDING_DOMAIN`; exact engine/build/save/security/release rules plus explicitly measured 3D debt. |
| `design/04_OPEN_WORK.md` | 🔵 | `SUPPORTING_CURRENT`; current lifecycle crosswalk, not canonical finding records. |
| `design/05_DOC_LEDGER.md` | 🔵 | `SUPPORTING_CURRENT`; exhaustive Git-declared authority index with live counts supplied by the validator. It classifies documents but cannot override the higher-precedence operational/domain authorities it identifies. |
| `design/09_CHAPTER_DEVELOPMENT_GUIDE.md` | 🟢 | `BINDING_DOMAIN` for owner-directed 2026-09-05 chapter planning/delegation, strategic unused-asset selection, free mechanic reuse/modification/combination within scope, production method, and evidence boundaries under the canonical planning rules. No new chapter commission or product acceptance is granted. |
| `design/templates/CHAPTER_BRIEF_V1.md` | 🟢 | `BINDING_DOMAIN` for required chapter-planning fields only. An unfilled template grants no creative commission, runtime authorization, or acceptance. |
| `design/10_CHAPTER_REFERENCE_LIBRARY.md` | 🔵 | `SUPPORTING_CURRENT` continuity/source navigation, seed experience catalog, unused-asset discovery, and dated implementation availability. Scoped sources and actual evidence control; no new visual/device/child/owner acceptance is claimed. |
| `design/chapters/NORTHERN_ICE_WORLD.md` | 🟠 | `BINDING_DOMAIN` only for the owner's 2026-09-05 Northern future-chapter planning direction and restaurant/customer-order opportunity. `PROPOSAL_DEFERRED` scope: detailed activity choices, unbound artwork candidates, full chapter plot, and runtime implementation. Old spatial asset work orders remain superseded; this record grants no product acceptance. |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` | 🟢 | `CANONICAL_CURRENT`; stable DL-* rule authority. Owner revision 2026-10-03 updates DL-CIN-01–15 and adds DL-MOT-14–16 for eligible 2D/video methods, Aseprite, provenance and bounded iteration. Earlier method bans are superseded; identity/contact/temporal/human/device/child/owner and operational gates remain. DL-ASSET-08 and DL-CIN-16 retain their source-specific limits. |
| `design/animation/ROSHAN_MOVEMENT_LANGUAGE.md` | 🟢 | `BINDING_DOMAIN` for the owner-commissioned 2026-09-11 Roshan acting language and briefing criteria. Ribbon Glide/Playful Dolphin are working direction; numerical targets and pilot selection remain candidates, with no accepted clips, runtime, device, child or owner acceptance implied. Subordinate to canonical medium, motion, contact, protected-asset and cinematic rules; its cinematic method paragraph follows the 2026-10-03 declared-workflow/Aseprite revision without changing acting targets. |
| `design/animation/ANIMATION_PRODUCTION_PROTOCOL.md` | 🟢 | `BINDING_DOMAIN` for briefs, sources, contact/interrupt contracts, eligible final animation methods, Aseprite, budgets and separate machine/human/device evidence under `DL-MOT-10` through `DL-MOT-16` and `DL-CIN-01` through `DL-CIN-16`. No routine extra planning checkpoint or output acceptance; 2026-10-04 crisp contours, figure-wide continuity, multi-anchor Aseprite source/submission/decoded scale gates, actual negative-guidance proof and separate latent/decoded preservation evidence. Later owner correction adds pose-aware internal proportions, native temporal-detail/noise review and geometry-first video-conditioned repair; more decoder steps are experimental, with new explicitly authorized corrective briefs and retained cumulative costs; 2026-10-05 owner correction: whole-figure frames, no separately moving limb; 2026-10-07: one size including head, arms and hands, sprites drawn whole as a single unit |
| `design/templates/CHARACTER_MOVEMENT_PROFILE_V1.md` | 🟢 | `BINDING_DOMAIN` for required per-character movement-profile fields. An unfilled template grants no new canon, animation commission, source approval or runtime/visual/device/child/owner acceptance. |
| `audit/animation/README.md` | 🔵 | `SUPPORTING_CURRENT` master-linked character animation coverage, Roshan-first production sequence and separate evidence claims. It owns no canonical finding lifecycle and grants no master-audit satisfaction, clip or external cinematic delivery acceptance. |
| `assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; eight Grok motion-reference auditions, revised 2026-09-13 to require actual video-tool/input binding and one returned/reviewed pilot before expansion, with no still-board fallback. Preserved source art and a committed publication envelope remain separate from exact-opening approval, generation readiness and motion/runtime acceptance. No generated clip, new design or finding closure is claimed. |
| `design/BOSS_SPLASH_DESIGN_LANGUAGE.md` | 🟢 | `BINDING_DOMAIN` for short true-2D gameplay boss introductions: the action/identity/tell sentence, integrated display composition, exact live-tell reuse, automatic input-blocking timeline, and five-lane 4.5/5 review floor. Its scoped Grand Puff and Day Two scores do not grant game-wide, device, child, cinematic, or release acceptance and remain subordinate to direct owner, protected-asset, performance, and canonical design-language rules. Grand Puff-specific September 12 owner revision replaces the fake rehearsal with real assisted movement/dodge/counter; generic boss defaults remain. Subsequent owner-directed storybook cues replace the panel/fingers/geometric HUD with animated dust, bubble and gold-star artwork; mechanics remain unchanged. September 13 owner direction establishes enemy-origin aiming animation, three fixed lock flashes, then launch as the shared boss convention; Grand Puff v3 supersedes its v2 dust warning; the owner accepts its choreography as a rough draft and commissions a 4.75/5 painted restyle. Subsequent owner feedback removes the charge-end swirl in favour of unfolding painted dust crests and a broad dust front, with a coral-peach third flash announcing launch. The score is a target, not acceptance. The September 13 Grok character inventory recovers existing identity/pose sources and records runtime disagreements; it grants no identity signature or production approval. Device/child acceptance pending. |
| `design/07_CASTLE_DOOR_LANGUAGE.md` | 🟢 | `BINDING_DOMAIN`; Act One castle door states, single-highlight sequencing, arch-following cue treatment, and Baby Eagle plot-priority ownership. |
| `design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md` | 🟠 | `SUPPORTING_CURRENT` implementation/design record for the early Chapter 3 Moonflower doorway, Rainbow Skyway, Butterfly House handoff, save migration, existing minigame evaluation, and route acceptance gates. `SUPERSEDED` scope: replaces only this task's earlier direct-door-to-Fairy-Pond concept; it does not supersede the design language, save rules, true-2D debt authority, protected-asset rules, or owner acceptance. It grants no owner, child, device, full Butterfly World 2D-conversion, or release acceptance by itself. |
| `audit/MASTER_AUDIT_2026-08-09.md` | 🟢 | `CANONICAL_CURRENT`; synchronized audit-cycle/evidence/lifecycle record. Overall state remains `IN_PROGRESS`, satisfaction `UNSATISFIED`. It now indexes the 2026-09-05 boss-encounter report as scoped `SUPPORTING_CURRENT` evidence without changing canonical lifecycle or baseline counts. Earlier exact local/remote/APK and Sky evidence remains bound to its recorded source heads. Device, child, owner, accepted-visual, strict-2D and exact tutorial-voice gates remain open. The 2026-09-30 alpha impact is scoped repair evidence, with exact machine/source/APK and physical acceptance reported separately. Its objective-handoff follow-up records the failed dev Racer speech expectation and deterministic overlap repair; external acceptance remains open. The 2026-09-30 main cleanup records the bounded candidate, keeps MA-CODE-001 open and marks MA-CODE-005 VERIFIED_FIXED for exact-source local machine evidence; topic CI/integration remains required. Its shrink-only medium inventory preserves the immutable ceiling and leaves MA-2D-002 IN_PROGRESS. |
| `audit/DAY_ONE_DIRTY_POOL_STYLE_AUDIT_2026-08-22.md` | 🔵 | `SUPPORTING_CURRENT`; scoped master-rubric comparison for the three bespoke Day One pool-cleanup activities. Its revised 4/5 strong-candidate verdict and exact desktop Mobile evidence cannot override the canonical master audit, close any master finding, or substitute for device/child/owner acceptance. |
| `audit/DAY_ONE_POOL_NATURAL_INTEGRATION_SPEC_2026-08-23.md` | 🔵 | `SUPPORTING_CURRENT`; records the accepted runtime composition criteria and exact Mobile evidence for naturalizing the pool activities. The generated plate is reference-only, and this spec cannot grant device, child, voice, or owner acceptance. |
| `design/HANDOFF_GROK_DAY_ONE_POOL_NEXT_ANIMATION_2026-08-23.md` | 🟠 | `SUPPORTING_CURRENT` visual-only owner-run Grok handoff for the follow-on pool animation. Its room/fixture/Roshan/Rumi continuity and required beat order are binding for that handoff, while Codex/Luna review and owner acceptance remain authoritative; it grants Grok no audio, editorial, upload, or approval authority. `SUPERSEDED` scope: replaces only the older generic dirty-pool beat order embedded in the scoped pool audit; it does not supersede the design language, master audit, cinematic rules, audio authority, or owner acceptance. |
| `design/GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md` | 🟢 | `BINDING_OPERATIONAL` for external Grok scene handoffs: MASTER formula, archive-generator separation, reference budget, identity/endpoint locks and one-shot jobs. Stage 9 incorporates the 2026-09-16 automatic publication/recipient-access contract for every revision, including blocked-generation review drafts. It does not grant generated footage delivery acceptance. |
| `design/ASTRONAUT_THREE_ENGINEERING_DEVICES_2026-10-07.md` | 🟢 | `BINDING_DOMAIN` for the scoped owner-approved pipes/gears/pressure correction and painted green fluid. Refines the existing Astronaut verbs while preserving career/save identity, four birthday submilestone keys and parked/unlaunched canon; candidate implementation and all machine/native/device/child/owner evidence remain separate. |
| `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md` | 🟢 | `BINDING_DOMAIN` for the current Chapter 2 birthday-preparation implementation: exact eight stable Opera bits/mask/order, four-door visibility wave without a duplicate tutorial prelude, Farmer→Chef→Candy Maker persistent cake dependency, late Detective candle discovery, post-Detective rocket ignition, Ember King's candle motive, additive submilestone saves, and blocking acceptance limits. It supersedes only the conflicting sequence/checklist/result assumptions in the dated Chapter 2 option/staged-implementation records; global Opera freeplay and master audit remain separate authorities. |
| `design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md` | 🟢 | `BINDING_DOMAIN` for the persistent cake's picture-state semantics only: Farmer ingredients, five ordered Chef results, Candy Maker glaze/placement, and the separate Detective/Astronaut/Ember candle layer. It refines the cake dependency already selected by the eight-career production spine without changing career order, unlocks, global Opera, save-key ownership, or acceptance gates. |
| `design/CHAPTER2_BIRTHDAY_IMPLEMENTATION_2026-08-30.md` | 🟡 | `HISTORICAL_EVIDENCE` / `SUPERSEDED` for implementation staging explored before the exact eight-career production spine. It cannot override the current career order, unlock masks, cake-state semantics, Detective timing, rocket ignition, Ember motive, or acceptance gates in `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md`. |
| `design/CHAPTER2_EIGHT_CAREER_STORY_OPTIONS_2026-08-30.md` | 🟡 | `HISTORICAL_EVIDENCE` / `SUPERSEDED` option analysis. Its alternatives preserve design rationale only; the selected sequence, scene roles, dependencies, and party arc are controlled by `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md`. |
| `design/templates/IMAGINE_SHOT_CARD_V2.md` | 🟢 | `BINDING_OPERATIONAL` machine-readable V2 shot-card contract for exact cast, character identity/anatomy, location topology, causality, continuity, immutable reference links, and prompt locks. V1 remains historical/backward-compatible for existing packets; new ready jobs use V2. |
| `audit/GROK_HANDOFF_RETROSPECTIVE_2026-08-30.md` | 🔵 | `SUPPORTING_CURRENT` evidence review of the pool, bathroom, Stuffie Room, opening-flight, and Ember animation handoffs. It explains the V2 formula's failure model but cannot accept a frame, clip, character, device result, or release. |
| `audit/CINEMATIC_MEDIA_INVENTORY_2026-08-30.md` | 🔵 | `SUPPORTING_CURRENT` reproducible inventory and review of existing Day One edited movies, opening proofs, motion studies, room storyboards, and historical dirty-castle material. Its editorial/board/rejection classifications cannot grant frame, clip, device, child, owner, or delivery acceptance. |
| `design/DAY_ONE_CINEMATIC_LOCAL_PRODUCTION_PLAN_2026-08-30.md` | 🟣 | `PROPOSED_CURRENT` local Day One cinematic slate: 13 discrete movies/70 one-shot Grok jobs, paired dirty-entry and restoration grammar for all four rooms, character/location authority matrix, and production order. It is subordinate to the runtime, master handoff formula, cinematic rules, owner decisions, and independent delivery gates; it authorizes no media upload, runtime seam, or generated-footage acceptance by itself. |
| `design/grok_day_one_video_handoffs_2026-08-30/README.md` | 🟣 | `PROPOSED_CURRENT` operator index for one shared continuity block and 13 separated Day One Grok video direction files containing 70 one-shot copy blocks. It operationalizes the local slate and master handoff formula but is not a substitute for approved visual packets, immutable links, V2 readiness validation, full-frame regeneration evidence, or delivery acceptance. |
| `design/GROK_FOOTAGE_ANALYSIS_AND_ENDPOINT_HANDOFF_2026-09-02.md` | 🔵 | `SUPPORTING_CURRENT` analysis and endpoint-review record for the Day One Grok footage lane. It preserves dependency, measurement, promotion, and completion-claim distinctions but cannot grant archive completeness, generation readiness, full-frame delivery acceptance, runtime integration, device, child, or owner acceptance. |
| `design/GROK_LOCATION_GEOMETRY_AUTHORITY_AUDIT_2026-09-02.md` | 🔵 | `SUPPORTING_CURRENT` location-topology audit for D1-C00 through D1-C12 and the Main Hall lock. It constrains the scoped handoff packets but cannot replace protected source authority or grant generation, delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/day_one_grok_visual_handoffs_2026-09-02/README.md` | 🔵 | `SUPPORTING_CURRENT` operator index for the versioned Day One Grok visual-reference packets. Archive and generator claims remain packet-specific; this index grants no full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c00_opening_flight_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C00 Opening Flight visual handoff. Its immutable archive links, reference roles, shot board, and generator cards do not make generated footage accepted delivery pixels or grant runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c01_lagoon_landing_castle_approach_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C01 Lagoon Landing visual handoff. Its immutable archive links, reference roles, shot board, and generator cards do not make generated footage accepted delivery pixels or grant runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c02_first_dirty_castle_discovery_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C02 first dirty-castle discovery visual handoff, including its geometry-locked first-frame candidates. Those candidates and packet links remain continuity inputs and grant no delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c03_bathroom_dirty_entry_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C03 dirty Bathroom visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c04_bathroom_restored_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C04 restored Bathroom visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c05_pool_dirty_discovery_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C05 dirty Pool visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c06_pool_purification_rumi_hug_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C06 Pool purification, Rumi, and hug visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c07_stuffie_dirty_discovery_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C07 dirty Stuffie Room visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c08_stuffie_restoration_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C08 Stuffie Room restoration visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C09 dirty Art Room visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c09_art_room_dirty_discovery_visual_v1/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; records scoped Sol visual review of D1-C09 generation inputs. That review does not grant owner review, full-frame delivery, runtime, device, or child acceptance. |
| `assets_src/cinematics/d1_c10_art_room_restored_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C10 restored Art Room visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c10_art_room_restored_visual_v1/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; records scoped Sol visual review of D1-C10 generation inputs. That review does not grant owner review, full-frame delivery, runtime, device, or child acceptance. |
| `assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C11 Grand Puff reveal visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c11_grand_puff_reveal_visual_v1/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; records scoped Sol visual review of D1-C11 generation inputs. That review does not grant owner review, full-frame delivery, runtime, device, or child acceptance. |
| `assets_src/cinematics/d1_c12_restored_castle_finale_visual_v1/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` and operator index for the D1-C12 restored Castle finale visual handoff. Its references, board, and generator cards cannot grant full-frame delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c12_restored_castle_finale_visual_v1/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; records scoped Sol visual review of D1-C12 generation inputs. That review does not grant owner review, full-frame delivery, runtime, device, or child acceptance. |
| `assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/README.md` | 🟣 | `PROPOSED_CURRENT` operator index for the D1-C13 Grand Puff friendship-completion handoff. The packet remains blocked pending owner decisions and grants no generation-ready, delivery, runtime, device, child, or owner acceptance. |
| `assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_REVIEW`; explicitly `BLOCKED_PENDING_OWNER_REVIEW` for D1-C13. Its findings and required per-shot evidence prevent any delivery, runtime, device, child, or owner acceptance claim. |
| `assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/SOURCE_DOCUMENTS.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` inventory for D1-C13 written authorities and pending immutable links. It is provenance/navigation only and cannot resolve the pending owner decisions or grant generation or delivery acceptance. |
| `assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/STATUS.md` | 🟣 | `PROPOSED_CURRENT` packet-status record for D1-C13. Its explicit pending owner decisions and do-not-promote boundary remain blocking; it grants no generation, delivery, runtime, device, child, or owner acceptance. |
| `audit/day_one_pool_lighting_image_audit_2026-08-22.md` | 🔵 | `GENERATED_REPORT`; five-file pixel-statistics summary for the Day One dirty-pool runtime textures. It supports the scoped style audit but is not an aesthetic, runtime-context, device, child, owner, or accepted-visual pass. Regenerate with `tools/audit_lighting_images.py`; do not hand-edit. |
| `audit/findings/ACTIVE_FINDINGS_2026-08-13.md` | 🟢 | `BINDING_AUDIT_RECORD` for the complete field-level finding records, linked from section 5 and retained through terminal transitions — 36 records (34 active) at exact integrated head `441adf35`, whose topic/dev remote runs preserved the green 36-test/six-stress/316-parity document gate with `MA-DOC-005` `VERIFIED_FIXED`; 48 records (46 active) after the 2026-08-26 code-refinement round appended twelve new records and three history updates. The file cannot silently add an item or change master severity/lifecycle. The 2026-09-30 histories reconcile current Day One/Chapter Two coverage and bounded alpha repairs without changing unresolved lifecycle authority. The 2026-09-30 main cleanup records the bounded candidate, keeps MA-CODE-001 open and marks MA-CODE-005 VERIFIED_FIXED for exact-source local machine evidence; topic CI/integration remains required. Its shrink-only medium inventory preserves the immutable ceiling and leaves MA-2D-002 IN_PROGRESS. The 2026-10-07 Astronaut clearance opened `MA-SAVE-002` as `CONFIRMED_OPEN` from the bound genuine-input save-loss baseline, then moved it to `IN_PROGRESS` after implementing versioned checkpoints with scoped ordinary lifecycle and schema proof. Pre-contact source-bound ordinary71 and birthday83 genuine-input lifecycle checks passed from explicit prior-story fixtures, with 12 schema and 320 gesture checks. READY PARK reuses the unchanged licensed rocket and floor cue while preserving its saved context and unlit canon; full trusted suite, complete natural Chapter 2 progression, native visual, device/child/owner acceptance and closure remain pending. The scoped default-phase/Astronaut station dependency repair moves `MA-PLAY-005` to `IN_PROGRESS`, with other careers and its wider eight-job criteria still open. Astronaut genuine-input contact review additionally retains four actor/action-envelope failures while83 route/save checks pass, extending `MA-PLAY-004` evidence without changing its `IN_PROGRESS` lifecycle or granting visual acceptance. The later scoped pipe-contact candidate defers placement until approach/whole-figure work/live owner eligibility:73current route/save checks and17live position/pose negatives pass. The earlier broad runtime receipts are now historical at their recorded sources; ten candidate jaw samples do not accept animation, anatomy, full lifecycle or native>=4.6. Other phases and independent/device/child/owner/full-suite gates remain open. Standalone tutorials are retired; historical counts are unchanged. Current contact-source full-mechanic route refresh passes91ordinary/103birthday, retaining all71/83previous assertions and20extra actual pending/contact checks pervariant. Headless behavior/save currency is refreshed; source schema12/gesture320 remain historical, no native acting/visual/device/child/fullsuite/freshChapter2 or lifecycle closure. Further current-source57+57headless checks at1280x720and1600x720 prove fueled wrong-plan/source-save/pause/selectedtap recovery and sampled viewport bounds, with no production/art/lifecycle or native score change.  Native Astronaut birthdayV3 diagnostic107/221 at pre-guard owned localcandidate adds actual Mobile pixels and primary per-action failures; release tween ownership, remote PATCH/VALVE/READY PARK and faded return remain open. Findings stay `IN_PROGRESS`; no strict fresh-runtime or4.6acceptance.  Current release-guard evidence117/84native with settled return and205corrective headless plus90named passing subruns from retained failed setup parent; primary action scores stay below4.6. Lifecycle unchanged, no strictfresh-runtime/fulltrusted/independent/device/child/owner acceptance. Current Astronaut helperf6cd174b facing correction: two-aspect nativeV5birthday121each/168PNG and17negative diagnostics pass, older helper65450443 receipts explicitly historical. Primary4action grades still below4.6; no lifecycle/master/independent/device/child/owner/fullsuite/integration acceptance. Historical valve world9368b7f3/surfacea8b1e12c candidate:121headless/126+126native/17pipe-negative diagnostics and211PNG pass with genuine local contact; older world/surface receipts now historical, before-source bytes preserved. Primary VALVE3.8and other action grades remain below4.6; nativeV1prelaunch guard failure/cost retained. No lifecycle, authority, fullsuite or external acceptance change. Historical PATCH worldb567bb47/surface4c6f460f candidate:141headless/127+127native/17pipe-negative diagnostics and257PNG pass with5live whole-figure patch commits perpositive run; previousVALVEworld/surface bytes preserved as historical. Primary PATCH3.6and allothercompleteactions remainbelow4.6; target/consequence readability, fulltemporal, independent/device/child/owner/fullsuite/currentordinary/integration remain open. Lifecycle/authority unchanged. Current PATCH readability worldb567bb47/surface5685ab40:143headless PASS,127+127native reports/17missed negatives and258PNG reconciled; original native monitor parentFAIL and missing second exit/continuous-resource evidence remain explicit. Leaks/fixed earned plates clearer, primary PATCH4.0and allothercompleteactions below4.6. Fulltrusted/currentordinary/fullnatural/fulltemporal/strictQA11/independent/device/child/owner/integration remain open; lifecycle/authority unchanged. |
| `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` | 🟢 | `BINDING_OPERATIONAL` for stable `CHG-*` scope and rollback. Current inventory is 31 IDs, 79 uniquely owned commit references, four guarded-script emitters, 25 planner tests, and 27 manual/refusal groups. Manual/non-emitting CHG-031 owns exact 19-path source `51d0abc0`, including `scripts/probe_northern.gd`, at +3,318/-3,517. The ledger never authorizes rollback that violates protected-asset, security, save, or final-medium rules. |
| `audit/MASTER_AUDIT_2026-08-26.md` | 🔵 | `SUPPORTING_CURRENT`; the 2026-08-26 code-refinement round record — comprehensive analysis at integration head `9a1754c1`, standing-metrics delta, scorecard movement, twelve V1 findings, goal set G1–G12, and orchestration rationale. Its normative deltas live in the canonical master audit (sections 5, 12, 13, 14) and design 06 section 18; this record cannot redefine canonical rules or lifecycles. |
| `audit/FONT_TYPOGRAPHY_AUDIT_2026-08-30.md` | 🔵 | `SUPPORTING_CURRENT`; V1 source audit of runtime font authority, typography helpers, size/read-dependency, Unicode semantics, layout expansion, and 45 `Label3D` instances. Stable rules are `DL-TYPE-01`–`DL-TYPE-12`; lifecycle authority remains the linked `MA-TYPE-001`–`007` records. It grants no runtime, font-selection, device, child, or owner acceptance. |
| `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` | 🔵 | `SUPPORTING_CURRENT`; Codex implementation work packages for the 2026-08-26 round — Stage A (WP-A1–A6, gate hardening and bounded repairs), Stage C (WP-C0–C6, the Mode Platform migration M0–M6 from design 07), and the remaining Stage B cleanups (WP-B2/B3/B5/B6; B1 and B4 execute inside Stage C) — with per-package scope boundaries, acceptance gates, escalation triggers, and reporting format. Subordinate to the canonical audit's section-9 protocol and section-12 gates; grants no authority beyond section 13 item 11. |
| `CODEX_DOOR_HIGHLIGHT_REWRITE_HANDOFF_2026-09-30.md` | 🔵 | `SUPPORTING_CURRENT`; owner-requested 2026-09-30 Codex work order for the Pearl Castle door highlighting rewrite (Door Guidance v2): 13 defects verified at dev `e7899cc0`, led by the root cause that cues are shaped from each door's touch box instead of its painted visual geometry; the visual-box/touch-box split, one-highlight arbiter, lit-doorway Plot treatment, static resting doors, guide star and tappable edge beacon, seen beat transfer, exact-voice map, measured door geometry, work packages WP-D0–WP-D9, acceptance AC-1–AC-21 and owner decisions OD-1–OD-6. `design/07_CASTLE_DOOR_LANGUAGE.md` stays the binding door language until the implementation rewrites it; review composites under `audit/door_highlight_rewrite_2026-09-30/` are diagnostic, not runtime evidence. Grants no implementation, visual, device, child, or owner acceptance. |
| `design/08_TARGET_ARCHITECTURE.md` | 🟢 | `BINDING_DOMAIN` for game-code structure, produced on direct owner request 2026-08-26: the Mode Platform remodel — the growth law (`DL-CODE-11`: migrated families add content as a mode script plus a registry row with `main.gd` untouched), the GameMode/ModeContext/ModeRegistry/ModeDirector/Services contracts, the sharpened durable-vs-ephemeral state line, the append-only structure ratchet (`DL-CODE-12`, `tools/audit_structure.py`), migration plan M0–M6, the growth-law acceptance test, and section 9's four owner review points. Subordinate to security/save/protected-content rules and direct owner decisions; keeps the rejected-universal-engine ruling. |
| `audit/LENOVO_TAB_M11_EMULATION_PROTOCOL_2026-08-30.md` | 🔵 | `SUPPORTING_CURRENT`; the tablet-performance emulation runbook for the confirmed Lenovo Tab M11 unit (4 GB RAM / 64 GB, Best Buy SKU 6572176) — quantified Speedy-tier working budgets and measurement lanes A–D, from desktop geometry emulation to the on-device matrix that services `MA-PERF-001`. Estimated budgets bind only after Lane D device calibration; the runbook cannot redefine `AGENTS.md`/design 06 rules or grant device, child, or owner acceptance. |
| `audit/TABLET_PERF_EVALUATION_2026-08-30.md` | 🔵 | `SUPPORTING_CURRENT`; the 2026-08-30 five-lane tablet-performance evaluation of the dev head against the Tab M11 emulation standard — ranked weaknesses W1–W10 (frame pacing, dual-world render/tick, Speedy gate gaps, ambient churn, APK/import-sidecar pipeline defects, 16:10 blindness) with a priority sequence. Evidence and recommendations only; the master audit remains the lifecycle owner and no device, child, owner, or accepted-visual gate is granted. |
| `ASSET_AUDIT.md` | ⚪ | `HISTORICAL_EVIDENCE`; 2026-06-25 CC0 audit/network decision. Current named-defect discipline comes from design 06; its stale music inventory is superseded by `MUSIC_AUDIT_2026-08-09.md`. |

## Game design lineage

| Doc | | Note |
|---|---|---|
| `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` | 🟠 | **Mixed authority / `PARTIALLY SUPERSEDED`.** `OWNER_DECISION` in §10 / `7426c187`: distribute all thirteen careers through thematic Castle rooms and make Opera Hall one venue, not the all-career hub. `OWNER_DECISION` in §16 / `3d1236fe`: cut Curtain Dragon, Shadow Phantom, and Midnight Maestro and keep save slots 4/9/14 as inert tombstones. Section 17 / `ef2fd982` clarifies that later boss fights belong to Ember-aligned henchmen and do not revive the Opera bosses. §17 supersedes §16 only on whether boss fights exist at all, while §16 supersedes §10's earlier Opera boss/finale-card language. Remaining chapter plot/system proposals are `PROPOSAL_DEFERRED` unless separately adopted. Boss retirement is `MA-OPERA-011` `FIXED_PENDING_VERIFICATION`; commit `09e5e356` implements the room distribution and moves `MA-OPERA-012` to `FIXED_PENDING_VERIFICATION`, with external/visual closure open. |
| `GAME_REDESIGN_2P5D_2026-07-27.md` | 🟠 | `HISTORICAL_EVIDENCE` for child-readable linear navigation, touch-the-world, independent cards and differential layers. Its 2.5D/SideScrollStage/depth-buffer/reversibility/migration-order prescriptions are `SUPERSEDED`. |
| `WORLD_MAP_2026-07-27.md` | ⚪ | `PROPOSAL_DEFERRED`; geography is unapproved. Its old reachability report is historical; current `MA-PLAY-001` requires fresh enumeration. |
| `MINIGAME_ENGINES.md` | 🟠 | `SUPPORTING_CURRENT` for lifecycle/input/reward/mercy/voice/probe contracts. E1 expansion is deferred; E2/E4 spatial, Jolt-standee and Spline3 prescriptions are `SUPERSEDED`. |
| `MEDALS.md` | 🟠 | `BINDING_DOMAIN` for bronze/silver/gold, upgrade-only and passive-no-award rules. Its “3D play place” venue label is `HISTORICAL_EVIDENCE`, not medium authority. |
| `STUFFIE_COMPANIONS.md` | 🟠 | `BINDING_DOMAIN` for roster, unlock, care, control and no-fail behavior, including the 2026-09-09 Canvas Menu care clarification and the 2026-09-23 reef sparring-den retirement. GLB bodies, Meshy creation, the reef den entrance and 3D arena prescriptions are `SUPERSEDED`. |
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
| `ART_STYLE_GUIDE.md` | 🟠 | `BINDING_DOMAIN` only for shape/line/value/colour, sampled palette, identity/protected-source rules, child readability, complete anatomy/silhouette, and licence/provenance discipline. Its 2D-to-3D translation, Blender, Meshy, GLB, rig, model-texture, turnaround and conversion-contract prescriptions are `SUPERSEDED`. Its Roshan anchors (forelock, lavender clothing, green-right / pink-left tail) are superseded by the 2026-09-30 owner decision recorded in `MA-DOC-008`: the approved atlases are Roshan's primary identity authority, and her tail is iridescent, lavender-pink-purple or rainbow depending on the light. |
| `ART_SCORING_GOVERNANCE_2026-07-18.md` | 🟠 | `BINDING_DOMAIN` only for runtime-context scoring, stress/rejection iteration, explicit owner acceptance for 5/5, no automatic score from provenance, protected originals, and recorded provenance. Its 3D-diorama, deterministic-Blender, Meshy, rig/model and image-to-3D workflow prescriptions are `SUPERSEDED`. Its Roshan anchors (forelock, lavender clothing, green-right / pink-left tail) are superseded by the 2026-09-30 owner decision recorded in `MA-DOC-008`: the approved atlases are Roshan's primary identity authority, and her tail is iridescent, lavender-pink-purple or rainbow depending on the light. |
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
| Arborist worktree | ⚪ | Historical runtime remains `UNCOMMITTED_CANDIDATE`; 2026-09-29 art-only recovery is archived in the Tree Book handoff. No game code, save or career integration accepted. |
| `OPERA_QUALITY_OVERHAUL_2026-08-09.md` | 🟠 | `SUPPORTING_CURRENT` for career-specific causal verbs, Canvas layout/input corrections and the 13-atlas/208-frame audit. Its 52-phase count, universal descriptions of the later Ballerina/Boxer specialists, and real-kart Racer payoff are historical and `SUPERSEDED`. |
| `OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md` | 🟠 | `SUPPORTING_CURRENT` for the seven-part quality rubric, reuse discipline and non-overridden career/art corrections. Its 52-phase baseline plus Ballerina, Boxer and nested-kart prescriptions are `SUPERSEDED` by the later scoped authorities and Canvas Racer reconciliation. |
| `assets_src/imagegen/opera_minigame_quality_2026-08-09/REVIEW.md` | 🔵 | `PROVENANCE_ONLY` / `SUPPORTING_CURRENT` for minigame-sheet derivation and review notes. It grants no 5/5 or runtime acceptance; owner/context/device review remains separate. |
| `assets_src/imagegen/opera_roshan_animation_2026-08-09/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY`; accepted-generation IDs, prompt hashes and derivation commands for the 13 atlases. It cannot override the review JSON, runtime hashes, specialist documents or owner acceptance. |
| `assets_src/imagegen/chapter2_birthday_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the selected Chapter 2 Sky Lagoon strawberry assets and the preserved superseded ten-strawberry six-tier cake test, including rejected/superseded iterations, generation IDs, exact prompts, hashes, deterministic checker-matte repair, and runtime derivation. It grants no device, child, final owner, voice, or in-scene visual acceptance. |
| `assets_src/imagegen/chapter2_cake_progression_2026-08-31/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the seven active cake-preparation/end-state candidates, their exact prompts/result IDs/hashes, rejected Bake corrections, strict diameter audit, five-berry endpoint continuity, and deterministic runtime derivation. It grants no device, child, final owner, voice, or in-scene visual acceptance; cake-state semantics remain controlled by the Chapter 2 cake visual progression contract. |
| `assets_src/imagegen/chapter_two_ember_family_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the Chapter 2 Ember-son concept reference and its generation record. It grants no runtime selection, cinematic delivery, character-final, device, child, or owner acceptance. |
| `assets_src/imagegen/chapter_two_rainbow_candle_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the unlit discovery candle and later large rainbow-flame reference sources, hashes, and non-destructive runtime derivatives. Plot timing and state authority remain in the Chapter 2 production spine; device, child, voice, and final owner acceptance remain open. |
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
| `docs/TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md` | 🟢 | `BINDING_DOMAIN` temporal production gate. Owner revision 2026-10-03 permits declared 2D/video workflows, preserving identity/topology/contact/motion and human/device acceptance. Production scene audit and separate derivation review are required; strict per-frame generation evidence applies only to that selected method. |
| `docs/CINEMATIC_DIRECTION_AND_INTENT_PROTOCOL.md` | 🟢 | `BINDING_DOMAIN` pre-generation intent/rhythm process under current workflow policy; appearance, shot authority, temporal and human/device acceptance remain required. |
| `docs/OPENING_CINEMATIC_ART_DIRECTION_BRIEF_V2.md` | 🔵 | The cinematography/script brief for the opening. |
| `docs/OPENING_CINEMATIC_FULL_FRAME_PROCESS_AUDIT_2026-07-29.md` | 🔵 | The full-frame trial, including what the position-guide modes actually measured. |
| `docs/OPENING_CINEMATIC_REGENERATION_AUDIT_2026-07-28.md` | 🟡 | Explicitly marked historical: its pose-reuse/compositing methods are now forbidden. |
| `docs/CARTOON_VIDEO_PIPELINE.md` | 🔵 | The `.ogv` encoder runbook. |
| `audit/cinematics/day_one_voice_timelines/README.md` | 🔵 | `SUPPORTING_CURRENT`; review-only Day One voice-timeline intake and editorial cue-planning notes. Runtime voice routing and acceptance remain governed by the current audio/runtime authorities and their independent gates. |

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
| `design/BUNNY_BOSS_REBUILD_2026-09-05.md` | 🟢 | `BINDING_DOMAIN` for the September 5 owner-requested movement/counter mechanics rebuild; replaces the old triple-tap and random-contact encounter contract while retaining approved art, no-death behavior, and later game-wide medium requirements. Its final local V4 packet binds 17 source hashes and 13 unmodified Mobile captures; remote commit, Android/device, child and owner acceptance remain pending. |
| `assets_src/imagegen/dust_bunny_boss_arena_2026-08-30/PROMPT_AND_PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the August 30 authored Dusty Attic image and its preserved native source. Restored unchanged from `0243d929` for the September 5 owner-requested background correction; current runtime, probes and device review own delivery acceptance. |
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

## Day One player-experience round (2026-09-02)

Code-traced playthrough evidence and its Codex handoff. No run was executed
on a device or with a Godot binary; every timing is modelled from the code
and the protocol's child model, so none of these rows grants device, child,
owner or release acceptance.

| Doc | | Note |
|---|---|---|
| `CODEX_DAY_ONE_PLAYER_EXPERIENCE_HANDOFF_2026-09-02.md` | 🔵 | `SUPPORTING_CURRENT`; Codex work packages WP-D1–WP-D9 for the Day One entry arc (arrival routing, spoken objectives, room hand-offs, bathroom gesture forgiveness, Grand Puff pacing and resumability, save/start-menu safety, stuffie and art payoffs, revisit polish, probe rosters), a 23-item findings register `DO-01`–`DO-23`, the attention-budget contract, owner escalation triggers and the voice-key list. Subordinate to the canonical audit, design 06 and owner decisions; closes nothing until probes and device evidence exist. |
| `CODEX_DAY_ONE_REBUILD_HANDOFF_2026-09-23.md` | 🟣 | `PROPOSED / CANDIDATE`; DRAFT Codex rebuild handoff for Day One and the Grand Puff finale: per-part focal goals and playtest questions, handoff-local findings `D1R-01`–`D1R-23`, measured Grand Puff persona runs, a pacing/timing/fun analysis with a redesign and help ladder, an art regeneration queue, a voice/pointer/touch contract, a target Day One mode architecture and work packages WP-R0–WP-R8. Pending the owner decisions OD-1–OD-9 it lists; grants no generation, recording, lifecycle or implementation authority until they are answered. Subordinate to the canonical audit, design 06 and owner decisions; re-baselines the 2026-09-02 handoff without superseding its evidence. Records the owner answers of 2026-09-23 (story clips between scenes under `DL-CIN-16`, Grand Puff canon, rainbow-bunny follower); OD-1 gameplay and OD-2/OD-4–OD-9 stay open. |
| `audit/day_one_playthroughs_2026-09-02/README.md` | 🔵 | `SUPPORTING_CURRENT` index of the sixteen-persona bundle at head `ff68f955` with the per-finding convergence table. Evidence only. |
| `audit/day_one_playthroughs_2026-09-02/PROTOCOL.md` | 🔵 | `SUPPORTING_CURRENT` shared playthrough protocol: child model, Day One flow map with code pointers, and the fixed report shape every run used. A method record, not a design rule. |
| `audit/day_one_playthroughs_2026-09-02/run_01_golden_path.md` | 🔵 | `SUPPORTING_CURRENT` baseline run (attentive golden path): 34-beat log with measured clip lengths, time budget 2.6/5.7/15.7 min, hazards and six proposals. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_02_tap_everything.md` | 🔵 | `SUPPORTING_CURRENT` tap-everything toddler run: input-routing trace, reef and attic sequence break, bathroom tap stall. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_03_passive_watcher.md` | 🔵 | `SUPPORTING_CURRENT` passive watcher run: idle-nudge table and silence durations per beat. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_04_impatient_skipper.md` | 🔵 | `SUPPORTING_CURRENT` impatient skipper run: forced-wait versus agency accounting (79 s / 120 s typical; boss 96 % forced). Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_05_door_explorer.md` | 🔵 | `SUPPORTING_CURRENT` door explorer run: blocked-door feedback chain, elevator, mid-room exits, courtyard hops. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_06_quit_and_resume.md` | 🔵 | `SUPPORTING_CURRENT` quit-and-resume run: nineteen kill points with a last-write / restore / lost ledger. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_07_sloppy_gestures.md` | 🔵 | `SUPPORTING_CURRENT` weak-fine-motor run: every recognizer's thresholds, the per-touch motion-clock reset, button release-mode misses. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_08_speedrunner.md` | 🔵 | `SUPPORTING_CURRENT` speedrunner run: 80 s hard floor, ceremony verdicts, fast-input breakage. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_09_repeat_visitor.md` | 🔵 | `SUPPORTING_CURRENT` repeat-visitor run: revisit answers, replayability, post-boss reef placement. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_10_audio_first.md` | 🔵 | `SUPPORTING_CURRENT` ears-first run: per-beat audio contract table, clip resolution, eight collisions. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_11_non_reader.md` | 🔵 | `SUPPORTING_CURRENT` non-reader run: 51-string text-carrier inventory with non-text backups. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_12_save_routing.md` | 🔵 | `SUPPORTING_CURRENT` family-phone run: legacy, mid-Day-One, finished and corrupt save openings; New Game confirm path. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_13_boss_struggler.md` | 🔵 | `SUPPORTING_CURRENT` boss-struggler run: Grand Puff second by second for a 1.5–3 s reaction, assist and mercy arithmetic. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_14_stuffie_room.md` | 🔵 | `SUPPORTING_CURRENT` stuffie-lover run: playroom rescue geometry, picker tutorial, companion visibility, remaining 3D magnitudes. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_15_art_room.md` | 🔵 | `SUPPORTING_CURRENT` little-artist run: art studio hit boxes, logo-studio launch chain, customizer modal, attack-profile consumers. Modelled, not executed. |
| `audit/day_one_playthroughs_2026-09-02/run_16_session_budget.md` | 🔵 | `SUPPORTING_CURRENT` three-sessions run: attention-reservoir model, safe versus unsafe stops, Continue re-orientation, session fit. Modelled, not executed. |

## Visual polish and sprite QA handoff (2026-09-25)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_visual_polish_2026-09-25/README.md` | 🟣 | `PROPOSED / CANDIDATE` Codex handoff entry prepared by Claude (analysis only, no game change): packet contents and SHA-256 manifest, the owner-approved 2026-09-24 work queue (Baby Eagle backpack-free cutout everywhere; library magic-book day-replay menu; four-floor Opera House with the `DL-INT-12` retirement), and audit rerun steps. Grants no acceptance. |
| `docs/handoffs/codex_visual_polish_2026-09-25/AESTHETICS_PLAN.md` | 🟣 | `PROPOSED / CANDIDATE` visual-polish recommendations at dev `f76a8ba5`: full-frame current-state captures, two scratch prototypes (living pool water, warm bathroom light), ten engine-side interventions on existing art, the art that needs Codex image generation, a style-matching protocol and a suggested order. Owner acceptance required per room. |
| `docs/handoffs/codex_visual_polish_2026-09-25/TRANSPARENCY_AUDIT.md` | 🔵 | `SUPPORTING_CURRENT` castle sprite transparency and cut-off audit at dev `f76a8ba5`, revision 2: 345 runtime draws (217 unique images), 53 sprite sheets and a same-frame visibility pass over 301 objects; a cut-off analysis of every image touching its edge; eye-confirmed findings T1–T16 and interface overlap O1 (Rumi neighbouring-frame bleed, Baby Eagle cut-off book crop, Movie Lounge screen hiding the family home movie, hidden Day One rescue star, see-through settee and bed, interaction-sheet slivers and sliced blocks) with evidence and fixes. Evidence only. |

## Opera imp contest handoff (2026-09-30)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_opera_imp_contest_2026-09-30/README.md` | 🟣 | `PROPOSED / CANDIDATE` Codex handoff entry prepared by Claude as written material only (no game change, no images): the owner's 2026-09-30 and 2026-10-04 direction that each career's imp stays hidden until the final act, which ends in one job-skill contest he can win with an immediate contest-only restart and a radical slowdown after two failures; the Teacher's contest inverts, is always silly and cannot be lost; the Chef (by default) and Nursery defend against gross things and noisy imps; the Geologist races for the same geode (`DL-INT-14`, target; revisions 2, 4 and 5), the packet contents and SHA-256 manifest, the W0–W8 work queue and the open owner decisions. Publication grants no visual, device, child or owner acceptance. |
| `docs/handoffs/codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md` | 🟣 | `PROPOSED / CANDIDATE` specification for `DL-INT-14` at dev `55032e88`: contest contract C1–C16, shared pacing, idle pause, flub, contest-only rematch with the radical mercy after two failures, cheer tier, save and layout rules, the inverted and defense formats, code integration, twelve costumed contests (the Chef's YUCKY RECIPE as a defense contest) plus the Teacher's IMP'S LESSON, the Geologist's GEODE RACE and the Nursery's QUIET TIME described in words, owner decisions (decided by OD-E; still open: the recipe interpretation, imp costumes, silly icon style, Hall stage-long race), retirements, tests and acceptance. Revision 3 adds the art-reuse and imp-contact rules from the Day Two art review; revision 4 the owner's silly questions (such as which smells the worst); revision 5 the owner's 2026-10-04 decision. Related findings `MA-OPERA-001`, `MA-OPERA-005`, `MA-OPERA-009` and `MA-PLAY-004` stay open. |
| `docs/handoffs/codex_opera_imp_contest_2026-09-30/CURRENT_STATE_ANALYSIS.md` | 🔵 | `SUPPORTING_CURRENT` analysis of the Opera career formula at dev `55032e88`: rival pacer, Hall two-act, strengths and weaknesses, handoff-local findings H1–H10 with code anchors (not master-audit register entries), and imp use (41 of 178 pose files shown today, all 178 after the specified contests; 2 of 56 imp lines routed today, 39 after); revision 2 marks H2 absorbed by the Teacher contest. It grants no acceptance and cannot redefine design 06 rules. |

## Asset policy, protected-audio notes, and source provenance

Source-package records establish lineage at most. They do not prove that an
asset is reachable, current, visually accepted, or safe to promote.

| Doc | | Note |
|---|---|---|
| `art_library/candidates/castle_differentiation_2026-07-17/README.md` | ⚪ | `UNAPPROVED_CANDIDATE_EVIDENCE`; preserves nine studies byte-for-byte and explicitly denies runtime approval. No current generation or promotion authority. |
| `assets/ART_GENERATION_CONTRACT.md` | 🟠 | `PARTIALLY_SUPERSEDED`; protected-source, runtime-context scoring, reuse, palette, motif, Mobile, provenance, and placement principles survive. Its Blender/Meshy/GLB pipelines, 3D budgets, named active queue, and claim of self-contained current authority are `SUPERSEDED` by the final Canvas medium and August reuse decision. Its Roshan anchors (forelock, lavender clothing, green-right / pink-left tail) are superseded by the 2026-09-30 owner decision recorded in `MA-DOC-008`: the approved atlases are Roshan's primary identity authority, and her tail is iridescent, lavender-pink-purple or rainbow depending on the light. |
| `assets/OBJECT_GENERATION_AUDIT_LOG.md` | 🟠 | `SUPPORTING_CURRENT` for evidence classes, recurring generator-failure taxonomy, object completeness, runtime-context review, and no-bulk-generation caution. Blender/model rules, old work queue, dated counts, and any promotion state are `SUPERSEDED` or historical. |
| `assets/audio/voices/VOICE_MANIFEST.md` | 🟠 | `SUPPORTING_CURRENT` only for filename/fallback history and identification of irreplaceable family recordings. Its dated TTS roster, Gabby entry, regeneration/enhancement directions, and inventory are `HISTORICAL_EVIDENCE`, not authority to modify protected audio; current `AGENTS.md`, exact-voice findings, licences, and runtime evidence control. |
| `assets_src/audio/roshan_voice_auditions_2026-08-31/README.md` | 🔵 | `PROVENANCE_ONLY` for the temporary synthetic Roshan audition procedure and review set. It does not grant runtime acceptance, talent identity, or authority to modify protected family/Faron recordings. |
| `assets/characters/roshan_25d/PROMPTS.md` | 🔵 | `PROVENANCE_ONLY` for the original Roshan atlas generation. “2.5D” and any standee use are historical; current runtime authority is the sibling README plus current atlas/audit records. |
| `assets/characters/roshan_25d/PROMPTS_4X.md` | 🔵 | `PROVENANCE_ONLY` for the quadrupled animation expansion. It cannot grant identity, runtime, visual, or owner acceptance and does not authorize regeneration. |
| `assets/props/story/play_swing_PROMPT.md` | 🔵 | `PROVENANCE_ONLY` for the playground swing sprite. The owner image was a style reference only; this record grants no runtime acceptance or permission to alter protected Roshan art. |
| `assets_src/blender/qa_outfits_floor2/ASSET_LICENSES.md` | 🟡 | `SOURCE_SCOPED_PROVENANCE`; records retired GLB/outfit sources only. The root `ASSET_LICENSES.md` is the binding ledger, and the model pipeline is `SUPERSEDED`. |
| `assets_src/blender/qa_pearl_castle_kit/RUNTIME_EVIDENCE.md` | ⚪ | `HISTORICAL_EVIDENCE`; review screenshots for rejected/retired Castle kit work, explicitly not runtime textures. They cannot satisfy current exact-engine or visual gates. |
| `assets_src/castle/day_one_bathroom_dirty/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the selected Day One bathroom grime and cleaner sources, rejected attempts, hashes, and whole-canvas runtime derivations. It grants no target-device, child, owner, cinematic-frame, or final visual acceptance. |
| `assets_src/castle/bathroom_single_bathtub_2026-08-29/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the two Bubble Bath shell-basket removals and the superseded localized-heal investigation. Current runtime authority is the full-frame interactive-background ownership manifest and generated clean plate; this record grants no target-device, child, owner, cinematic-frame, or final visual acceptance. |
| `assets_src/castle/fairy_conservatory_chapter3_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the selected Moonflower doorway architecture, rejected perspective iterations, deterministic opening-mask rebuild, source/runtime hashes, and delivery-pixel limits. Runtime placement and final visual acceptance require current code and audit evidence. |
| `assets_src/castle/fairy_conservatory_gate_available_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the corrected dormant-to-available castle state mapping, approved Butterfly Gate and sunrise Lily-Pad Fairy World reuse, threshold placement, source/runtime hashes, rejected generated closed-gate exploration, and delivery-pixel exclusions. Runtime behavior, device readability, owner acceptance, and release status require current code, focused audits, probes, and visual evidence. |
| `assets_src/castle/logo_studio_v2/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the personalized-banner V2 source family. Candidate/owner/device/Canvas acceptance remains open under the banner audit and master rules. |
| `assets_src/castle/room_regenerations/room_kitchen_fullframe_v2_provenance.md` | 🔵 | `PROVENANCE_ONLY`; records a dated accepted Kitchen candidate and source correction. Old-branch integration language is not current runtime or owner acceptance. |
| `assets_src/castle/room_regenerations/room_kitchen_fullframe_v3_provenance.md` | 🔵 | `PROVENANCE_ONLY`; records the v3 kettle correction and source lineage. Current reachability, medium, and visual status require current evidence. |
| `assets_src/cinematics/day_one_bathroom_finale/CONTRACT.md` | 🔵 | `SUPPORTING_CURRENT` for the optional Day One bathroom finale movie's exact Ogg Theora path, clean-room first-frame seam, once-only saved handoff, and missing-movie fallback. It is subordinate to the binding full-frame cinematic rule and grants no frame, identity, topology, style, device, child, or owner acceptance. |
| `design/HANDOFF_GROK_DAY_ONE_BATHROOM_MOVIES_2026-08-28.md` | 🔵 | `SUPPORTING_CURRENT` production handoff for the two optional Day One bathroom movies: locked runtime seams, storyboards, Grok-facing direction, full-frame regeneration and quality-manifest contracts, and blocking audit procedure. It grants no frame, movie, identity, device, child, or owner acceptance until the recorded gates pass. |
| `design/templates/IMAGINE_SHOT_CARD_V1.md` | 🔵 | `CANONICAL_CURRENT` executable external-generator interface template under `DL-CIN-14`: one shot/job, two-to-four role-bound approved images, one camera move maximum, action-first timeline, fixed/moving elements, end state, negatives, and sound. The 2026-10-03 declared-workflow policy allows separately audited final I2V candidates; initial readiness remains motion-reference status. It grants no generation or delivery acceptance by itself. |
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
| `assets_src/imagegen/geologist_roshan_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the selected Geologist Mermaid Roshan atlas generation, rejected transparency-repair attempt, deterministic neutral-field removal, source/runtime hashes, and prompt summary. Runtime selection, identity continuity, child readability, target-device performance, and owner acceptance require current code, probes, and visual evidence. |
| `assets_src/imagegen/teacher_roshan_2026-09-03/GAME_SEED.md` | 🔵 | `PROVENANCE_ONLY` for the Teacher Roshan generation seed and design intent. It grants no runtime, identity, device, child, or owner acceptance. |
| `assets_src/imagegen/teacher_roshan_2026-09-03/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the Teacher Roshan source, rejected attempt, deterministic alpha/atlas derivation, hashes, and runtime asset lineage. It grants no runtime, identity, device, child, or owner acceptance. |
| `assets_src/fairy_conservatory_handoff_2026-08-30/PROVENANCE.md` | 🔵 | `PROVENANCE_ONLY` for the targeted rainbow-walkway and Butterfly House generations, approved Sky Lagoon background reuse, reference-role limits, alpha preparation, runtime hashes, and review-only placement composite. It grants no owner, child, device, legacy-minigame 2D-conversion, or release acceptance. |
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

## Day One selective-regeneration handoff records

| Doc | | Note |
|---|---|---|
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/NEW_DRAFT_AUDIT.md` | 🟣 | `CANDIDATE_REVIEW`; review evidence for regenerated motion-reference drafts, pending human continuity and delivery-frame acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; package index for selective Day One regeneration jobs; it grants no runtime, device, child, owner, or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/SOL_MASTER_AUDIT.md` | 🟣 | `CANDIDATE_REVIEW`; scoped audit evidence for the selective regeneration packet, pending independent full-frame and human review gates. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C00/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C00, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C01/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C01, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C01/shots/D1-C01-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C02/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C02, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C02/shots/D1-C02-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C03/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C03, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C03/shots/D1-C03-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C03/shots/D1-C03-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C03/shots/D1-C03-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C04/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C04, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C05/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C05, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C05/shots/D1-C05-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C05/shots/D1-C05-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C06/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C06, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C06/shots/D1-C06-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C06/shots/D1-C06-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C06/shots/D1-C06-S06/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C06/shots/D1-C06-S09/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C07/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C07, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C07/shots/D1-C07-S06/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C08/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C08, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C08/shots/D1-C08-S01/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C08/shots/D1-C08-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C08/shots/D1-C08-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C08/shots/D1-C08-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C08/shots/D1-C08-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C09/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C09, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C09/shots/D1-C09-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C10/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C10, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C10/shots/D1-C10-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C10/shots/D1-C10-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C11/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C11, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C11/shots/D1-C11-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C12/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C12, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C13/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index for D1-C13, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C13/shots/D1-C13-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_regeneration_handoffs_2026-09-03/scenes/D1-C13/shots/D1-C13-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |

## Day One Grok handoff v3 candidate records

| Doc | | Note |
|---|---|---|
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; Day One third-pass archive/generator packet index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C00/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C00/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C01/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C01/shots/D1-C01-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C01/shots/D1-C01-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C01/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C02/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C02/shots/D1-C02-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C02/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C03/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C03/shots/D1-C03-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C03/shots/D1-C03-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C03/shots/D1-C03-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C03/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C04/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C04/shots/D1-C04-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C04/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C05/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C05/shots/D1-C05-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C05/shots/D1-C05-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C05/shots/D1-C05-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C05/shots/D1-C05-S06/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C05/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/shots/D1-C06-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/shots/D1-C06-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/shots/D1-C06-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/shots/D1-C06-S06/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/shots/D1-C06-S07/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/shots/D1-C06-S09/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C06/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C07/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C07/shots/D1-C07-S06/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C07/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/shots/D1-C08-S01/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/shots/D1-C08-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/shots/D1-C08-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/shots/D1-C08-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/shots/D1-C08-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C08/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C09/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C09/shots/D1-C09-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C09/shots/D1-C09-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C09/visuals/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_VISUAL_REVIEW_EVIDENCE`; generator-side review record only, unable to grant human identity, topology, style, continuity, or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C09/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C10/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C10/shots/D1-C10-S01/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C10/shots/D1-C10-S02/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C10/shots/D1-C10-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C10/visuals/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_VISUAL_REVIEW_EVIDENCE`; generator-side review record only, unable to grant human identity, topology, style, continuity, or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C10/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C11/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C11/shots/D1-C11-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C11/visuals/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_VISUAL_REVIEW_EVIDENCE`; generator-side review record only, unable to grant human identity, topology, style, continuity, or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C11/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C12/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C12/visuals/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_VISUAL_REVIEW_EVIDENCE`; generator-side review record only, unable to grant human identity, topology, style, continuity, or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C12/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/README.md` | 🟣 | `CANDIDATE_HANDOFF_EVIDENCE`; scene-local job index, unable to grant generated footage or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/shots/D1-C13-S03/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/shots/D1-C13-S04/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/shots/D1-C13-S05/RECONSTRUCTION.md` | 🟣 | `CANDIDATE_RECONSTRUCTION_EVIDENCE`; shot-specific motion-reference reconstruction notes, pending full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/visuals/GENERATION_REVIEW.md` | 🟣 | `CANDIDATE_VISUAL_REVIEW_EVIDENCE`; generator-side review record only, unable to grant human identity, topology, style, continuity, or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/visuals/README.md` | 🟣 | `CANDIDATE_GENERATION_EVIDENCE`; scene visual-packet guide, pending independent full-frame continuity and human acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/visuals/SOURCE_DOCUMENTS.md` | 🟣 | `SUPPORTING_SOURCE_INDEX`; source-document pointer for the candidate packet, unable to grant runtime, generation, or delivery authority. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C13/visuals/STATUS.md` | 🟣 | `CANDIDATE_STATUS_EVIDENCE`; generated packet status snapshot, not current runtime or delivery acceptance. |
| `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/SOL_MASTER_AUDIT.md` | 🟣 | `CANDIDATE_AUDIT_EVIDENCE`; third-pass packet audit record, unable to grant generated-footage or full-frame delivery acceptance. |

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

| `audit/BOSS_ENCOUNTER_VISUAL_AUDIT_2026-09-05.md` | 🟠 | `SUPPORTING_CURRENT`; scoped Grand Puff/shared-cue/CombatTutorial evidence. Focused exact-4.7.2 runtime is green. A tracked local packet binds 17 source hashes and 13 unmodified Mobile PNGs: selected final Dust states at 1280×720/1560×720 and five root3 tutorial states with the corrected framed bunny, floor targets, suppressed JUMP medallion and shared TAP/HOLD guide above the partner portrait. `SUPERSEDED` scope: repaired-state facts replace only this report's own before-repair observations; they do not supersede canonical `MA-*` lifecycle, design language, strict-2D inventory, voice ledger, or device/child/owner acceptance. Durable remote commit, combined CI, residual 3D, exact tutorial voice, device, child and owner gates remain open. |

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

## Day One DaVinci editorial drafts — 2026-09-04

| Document | State | Scope |
| --- | --- | --- |
| `design/DAY_ONE_DAVINCI_COHESION_2026-09-04.md` | 🔵 | `SUPPORTING_CURRENT`; draft editing and game-seam recommendations, not cinematic delivery acceptance. Its game seams now carry the 2026-09-23 `DL-CIN-16` story clips instead of the V03 drafts. |
| `design/DAY_ONE_DRAFT_BOUNDARY_EVIDENCE_2026-09-04.md` | 🔵 | `SUPPORTING_CURRENT`; scoped runtime capture and diagnostic evidence, including unresolved checks; not device or final-art acceptance. |
| `assets_src/cinematics/day_one_davinci_draft_2026-09-04/README.md` | 🟠 | `MIXED`; local DaVinci editorial project and source provenance. Its C04-S04 clean-bathroom source still feeds the `DL-CIN-16` story clip `d1_bath_clean`; its opt-in `--day-one-draft-movies` preview hook and V03 exports are `SUPERSEDED` by the 2026-09-23 story clips from the owner-selected 2026-09-20 cut. Not full-frame delivery acceptance. |
| `assets_src/cinematics/day_one_davinci_draft_2026-09-04/DOWNLOADS_INVENTORY.md` | 🔵 | `SUPPORTING_CURRENT`; project-relevant local source inventory only, not footage approval. |
| `assets_src/cinematics/day_one_davinci_draft_2026-09-04/RENDER_REVIEW.md` | 🔵 | `SUPPORTING_CURRENT`; sampled rendered-draft visual review and integration risks, not human or device acceptance. |
| `assets_src/cinematics/day_one_davinci_draft_2026-09-04/review/README.md` | 🔵 | `SUPPORTING_CURRENT`; diagnostic cut-contact image provenance only, never generation or delivery pixels. |

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

## Teacher learning engine candidate — 2026-09-05

| Document | State | Scope |
|---|---|---|
| `design/TEACHER_LEARNING_ENGINE_2026-09-05.md` | 🟣 | Local implementation and educational progression evidence; device, child, and integration acceptance remain open. |
## Geologist mechanics rebuild — 2026-09-05

| Document | State | Scope |
| --- | --- | --- |
| `design/GEOLOGIST_REBUILD_2026-09-05.md` | 🔵 | `SUPPORTING_CURRENT`; scoped Geologist research, mechanics implementation and diagnostic evidence; not release, final-art, device or child acceptance. |
| `design/OPERA_RACER_ENGINE_INTEGRATION_2026-09-05.md` | 🔵 | `SUPPORTING_CURRENT`; local Racer engine integration, diagnostic validation and visual evidence; not merged, released, device accepted, or master-audit closure. |

## Opera two-part performances — 2026-09-05

| Document | State | Scope |
|---|---|---|
| `design/OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md` | 🟣 | Local candidate for the three Opera Hall games only; mechanic and asset review, medal/token policy, pending integration and child/device gates. |

## Minigame art review — 2026-09-05

| Document | State | Scope |
|---|---|---|
| `design/MINIGAME_ART_AUDIT_2026-09-05.md` | 🔵 | `SUPPORTING_CURRENT`; local incomplete art/animation review and repair process. No release, owner/device/child acceptance or master-audit closure. |
| `audit/minigame_art_quality_2026-09-05/animation_review.md` | 🔵 | `SUPPORTING_CURRENT`; local incomplete art/animation review and repair process. No release, owner/device/child acceptance or master-audit closure. |
| `audit/minigame_art_quality_2026-09-05/nonopera_review.md` | 🔵 | `SUPPORTING_CURRENT`; local incomplete art/animation review and repair process. No release, owner/device/child acceptance or master-audit closure. |
| `audit/minigame_art_quality_2026-09-05/opera_review.md` | 🔵 | `SUPPORTING_CURRENT`; local incomplete art/animation review and repair process. No release, owner/device/child acceptance or master-audit closure. |
| `audit/minigame_art_quality_2026-09-05/protocol.md` | 🔵 | `SUPPORTING_CURRENT`; local incomplete art/animation review and repair process. No release, owner/device/child acceptance or master-audit closure. |
| `audit/minigame_art_quality_2026-09-05/racer_reaudit.md` | 🔵 | `SUPPORTING_CURRENT`; local incomplete art/animation review and repair process. No release, owner/device/child acceptance or master-audit closure. |
| `audit/minigame_art_quality_2026-09-05/current_scope_addendum.md` | 🔵 | `SUPPORTING_CURRENT`; reconciles historical capture authority with the current dev-based source candidate and keeps game-wide 4.5 acceptance open. |
| `audit/minigame_art_quality_2026-09-05/missing_coverage.md` | 🔵 | `SOURCE_INVENTORY`; unresolved source and dynamic-loader coverage leads only; no reachability or quality claim. |
| `audit/minigame_art_quality_2026-09-05/reuse_candidates.md` | 🔵 | `SUPPORTING_CURRENT`; bounded visual reuse screen for weak PictureGames assets; no runtime acceptance. |
| `audit/minigame_art_quality_2026-09-05/art_repair_backlog.md` | 🔵 | `SUPPORTING_CURRENT`; ordered repair and evidence backlog under the eight-dimension gate; no new scores or acceptance. |
| `audit/minigame_art_quality_2026-09-05/parent_art_crosscheck.md` | 🔵 | `HISTORICAL_VISUAL_EVIDENCE`; independent corroboration of three historical captures; no current-source or acceptance claim. |
| `audit/minigame_art_quality_2026-09-05/watering_can_attempt02_independent_review.md` | 🔵 | `REJECTED_SOURCE_REVIEW`; records the RGB fake-alpha blocker and bounded proportion/orientation differences; never runtime acceptance. |
| `audit/minigame_art_quality_2026-09-05/opera_native_coverage_followup.md` | 🔵 | `SOURCE_INVENTORY`; traces current room sources and derivatives, distinguishes fixed-scene review from multi-screen native coverage, and preserves reuse authorities; no current acceptance. |
| `audit/OPERA_MECHANICS_REAUDIT_2026-09-05.md` | ⚪ | `HISTORICAL_VISUAL_EVIDENCE`; 14-career mechanics and scene review at its recorded pre-reconciliation revisions. Later Racer, Geologist, Teacher and Opera Hall work supersedes affected current-status claims; scores remain historical and grant no current, master, device, child, or owner acceptance. |
| `assets_src/minigame_art_quality_2026-09-05/watering-can-attempt02/review.md` | 🔵 | `REJECTED_SOURCE_REVIEW`; generated RGB checkerboard candidate preserved outside runtime; no source or scene acceptance. |
| `audit/minigame_art_quality_2026-09-05/phase_pose_followup.md` | 🔵 | `SUPPORTING_CURRENT`; eleven phase-specific pose-containment repairs with source-bound desktop diagnostics; no authored-motion, device, child, or game-wide acceptance. |
| `audit/minigame_art_quality_2026-09-05/garden_realtime_followup.md` | 🔵 | `SUPPORTING_CURRENT`; eight 9df desktop stills verify completed-flower visibility and document remaining finish defects; no animation, device or game-wide acceptance. |
| `audit/minigame_art_quality_2026-09-05/current_mechanics_followup.md` | 🔵 | `SOURCE_REVIEW`; current61-base/70-runtime phase distinction, rebuilt lessons and Hall-only medal calibration; no measured child timing or new visual acceptance. |
| `audit/minigame_art_quality_2026-09-05/pool_runtime_followup.md` | 🔵 | `SUPPORTING_CURRENT`; real-room desktop diagnostic art review and four-target handoff sizing repair; no animation, device, child, or game-wide acceptance. |
| `audit/minigame_art_quality_2026-09-05/carrot_runtime_followup.md` | 🔵 | `SUPPORTING_CURRENT`; approved carrot reuse with configured Snowman/kitchen desktop diagnostics; complete motion and scene acceptance remain open. |
| `audit/minigame_art_quality_2026-09-05/hall_visual_comparison.md` | 🔵 | `SUPPORTING_CURRENT`; exact Hall PNG comparison for Ballerina, Magician and Pop Star plus rejected/neutral Magician ROPE/PORTAL mappings; sparse configured still evidence only, no animation, device, child or game-wide acceptance. |
| `design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md` | 🟣 | `CANDIDATE` rough story and implemented alpha draft following the owner-selected lawn celebration, protection victory then cheating candle theft, and sincerely conflicted Prince. King identity is owner-confirmed V4; Prince identity is recovered from the approved Git history package. The owner-authorized V4 cutout and recovered thin Prince are implemented in the gameplay draft; final visual/device review and cinematic delivery remain open. It does not accept character pixels, cinematics, runtime integration, device performance, or release. |

## Stage pathfinding audit — 2026-09-06

| Document | State | Scope |
|---|---|---|
| `audit/stage_pathfinding/README.md` | 🔵 | `SUPPORTING_CURRENT`; explains the 65-entry catalog/supporting inventory categories and status semantics; grouped legacy modes are not an exhaustive sublevel geometry claim. It grants no runtime, device, child, or owner acceptance. |
| `audit/stage_pathfinding/stage_inventory.json` | 🔵 | `SUPPORTING_CURRENT`; machine-readable inventory of concrete Reef/Lagoon/Castle/Day-One/Northern/Opera/minigame variants and spatial debt. It records gaps and reproduction sources; it is not a runtime catalog authority. |
| `audit/stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md` | 🟢 | `BINDING_DOMAIN`; owner-commissioned 2026-09-06 approach, arrival, door, cancellation, OOB, seam and zero-input protocol. Bounded Castle/Opera implementation and focused machine evidence exist; whole-game geometry and external acceptance remain open. |

## Development audit contract — 2026-09-06

| Document | State | Scope |
|---|---|---|
| `design/AUDIT_DEVELOPMENT_CONTRACT.md` | 🟢 | `BINDING_OPERATIONAL`; required reading, change traceability and evidence reporting under `DL-AUTH-05` through `DL-AUTH-07`; preserves existing security, owner and release precedence. |

| `assets_src/cinematics/chapter2_lawn_scale_v2_2026-09-06/README.md` | 🟣 | `CANDIDATE` owner-run Chapter 2 visual planning archive after scale refinement; approved identities retained, new staging pending owner/device/child review. No generation or cinematic delivery acceptance. |

| `docs/grok_animation_series_project/README_FIRST.md` | 🟣 | `SUPPORTING_CURRENT` navigation to the unified builder database plus preserved Chapter 2 owner-run planning; links the preserved private-series guide and revised visual archive. No generation, cinematic, owner, device or child acceptance is granted. |

| `docs/grok_animation_series_project/modules/chapter2_birthday_lawn/README.md` | 🟣 | `SUPPORTING_CURRENT` navigation to the unified builder database plus preserved Chapter 2 owner-run planning; links the preserved private-series guide and revised visual archive. No generation, cinematic, owner, device or child acceptance is granted. |

## Grok Handoff 2 continuity repair commission

| Doc | | Note |
|---|---|---|
| `design/GROK_HANDOFF_2_CONTINUITY_PROTOCOL_2026-09-09.md` | 🔵 | `SUPPORTING_CURRENT`; sequence continuity controls implementing existing cinematic rules; grants no opening, motion or delivery acceptance. |
| `audit/GROK_HANDOFF_2_FOOTAGE_AUDIT_2026-09-09.md` | 🔵 | `SUPPORTING_CURRENT`; scoped 73-file inventory, selected-cut/native-sample review and 74-shot reconciliation; historical evidence is distinguished from fresh observations. |
| `assets_src/cinematics/day_one_grok_handoff_2_2026-09-09/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; versioned repair archive operator index; 47 draft jobs remain generation-blocked and delivery-unaccepted. |

| `design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md` | 🔵 | `SUPPORTING_CURRENT`; recovered art and owner-corrected three-decision/four-choice split-screen Tree Book handoff; Candy Maker reserved for later outside Kitchen; no runtime acceptance. |
| `assets_src/handoffs/arborist_tree_book_20260929/README.md` | 🔵 | `SUPPORTING_CURRENT`; public art packet entry and selected review images; model-tested layout study, browser and production review pending. |
| `assets_src/handoffs/arborist_tree_book_20260929/recovered/assets_src/imagegen/opera_arborist_2026-08-09/PROMPTS.md` | ⚪ | `HISTORICAL_ARCHIVE`; byte-preserved 2026-08-09 provenance/review record; no current art, runtime or owner acceptance. |
| `assets_src/handoffs/arborist_tree_book_20260929/recovered/assets_src/imagegen/opera_arborist_2026-08-09/REVIEW.md` | ⚪ | `HISTORICAL_ARCHIVE`; byte-preserved 2026-08-09 provenance/review record; no current art, runtime or owner acceptance. |

| `design/OPERA_TREE_BOOK_TEST_2026-09-30.md` | 🔵 | `SUPPORTING_CURRENT`; scoped single-patient Opera House practice implementation and review evidence; no career/star or Day Two integration acceptance. |

| `audit/day2_art_library_2026-09-30/REPORT.md` | 🟣 | `CANDIDATE`; owner-commissioned first-pass illustrated Day Two source-art and phase/sequence review. Includes individual drafting scores, explicit historical capture limits and a source-change refresh trigger; no runtime, device, child, owner or finding acceptance. |

## Master-audit refinement handoff (2026-09-30)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_master_audit_refinement_2026-09-30/README.md` | 🟣 | `PROPOSED / CANDIDATE` Codex handoff prepared by Claude (analysis only, no game change) at dev `55032e88`: measured diagnosis of the master audit and design 06 as a design reference (evidence density, copied evidence, stale hand-copied counts, stale findings, scattered owner decisions, missing canon register, unrouted patterns), and the recommended three-shelf refinement — a design reference front door with canon, pattern, token, engine and owner-decision registers, an evidence archive, generated live status and a findings re-baseline — as staged work packages with acceptance criteria and owner questions. Revision 3 (2026-09-30) adds owner-critical Stage J — job-game playbook, job catalogue checker, takeover kit and cold-start dry run — to close `MA-DOC-006`. Revision 4 points WP-J1's catalogue at the Job Platform architecture's compiled content layer. Grants no runtime, visual, device, child or owner acceptance and changes no finding lifecycle. |
| `audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested job-game development and takeover readiness audit at dev `5d9668a9` (V1 static and Git history): no master-audit route or recipe exists for a new job game; an interim recipe reconstructed from the Teacher, Geologist and Tree Book builds (decide, 15 build steps, verify and accept), extension paths, voice, music, art and save pipelines, a capability coverage matrix, facts the documents get wrong (15 careers, 18-bit star namespace with the bit-18 clamp trap), takeover hazards (no backup has succeeded), and closure criteria for `MA-DOC-006`. Grants no runtime, visual, device, child or owner acceptance. |

## Job Platform architecture handoff (2026-09-30)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_job_platform_architecture_2026-09-30/README.md` | 🟣 | `PROPOSED / CANDIDATE` owner-requested Codex handoff prepared by Claude (specification only, no game change) at dev `7f068cb8`: work packages JP0–JP8 for a catalogue-driven Job Platform (content model and proof, save bounds first, consumer switch-over, derived probe expectations, tools on the catalogue, JobKit and capabilities, generated documents, owner-gated job-ID completion, Mode Platform alignment), acceptance criteria, owner questions and sequencing with Stage J, imp contests and design 08. Grants no runtime, visual, device, child or owner acceptance. |
| `docs/handoffs/codex_job_platform_architecture_2026-09-30/ARCHITECTURE.md` | 🟣 | `PROPOSED / CANDIDATE` architecture specializing the design 08 Mode Platform for job games: one record per job in `content/jobs/`, compiled to typed constants by `tools/content_build.py`, with masks, save bounds, room tables, phase totals and probe expectations derived; a shared JobKit replacing per-job plumbing and literal career-ID branches; strangler migration with equality proofs; a read-only extractor reproducing eleven of eleven hard-coded values from per-job records. Pending owner answers and Codex implementation; no acceptance claimed. |

## Reference consolidation handoff (2026-09-30)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_reference_consolidation_2026-09-30/README.md` | 🟣 | `PROPOSED / CANDIDATE` owner-requested Codex handoff prepared by Claude (analysis only, no game change) at dev `6fc2f48e`: waves W0–W7 to clean the master audit element by element, refresh stale finding text through dated history entries, save rules that live only in documents marked for archive, archive outdated documents with their file names, build fourteen reference documents and keep them fresh; coordinated with refinement WP-1, WP-2, WP-3 and WP-10. Tracked by `MA-DOC-007`. Grants no acceptance and changes no other lifecycle. |
| `docs/handoffs/codex_reference_consolidation_2026-09-30/STALENESS_AUDIT.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested staleness audit at dev `6fc2f48e` (V1 static and Git history): 19 of the master audit's 65 elements are current; 24 open findings and the register preamble state stale facts; 354 documents classified (119 archive now, 85 absorb, 72 evidence, 76 keep, 2 delete candidates); 47 contradictions with suggested resolutions; nine rules found only in documents marked for archive; hash-recorded and tool-read files that cannot move freely. Counts are dated measurements, not live status. |
| `docs/handoffs/codex_reference_consolidation_2026-09-30/REFERENCE_PLAN.md` | 🟣 | `PROPOSED / CANDIDATE` plan for fourteen domain reference documents (Opera careers, castle, Day One, chapters, worlds, art, animation, canon, audio, interface, engines, cinematics, performance, process): rules for what a reference may hold, outlines with source line ranges, the per-document classification and the root cleanup from 196 Markdown files to about six. Line ranges are guides measured at dev `6fc2f48e`. |

## Visual design language handoff (2026-09-30)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_visual_design_language_2026-09-30/README.md` | 🟣 | `PROPOSED / CANDIDATE` owner-requested Codex handoff prepared by Claude (analysis and written specification only; no game change, no images) at dev `b65c21fd`: work packages VL0–VL9 for one visual-language kit (routed reference, identity sheets, exemplar and rejection registries, one style card, one review card, one token and threshold set, a measurement tool with a blocking registry check, a cold-start art dry run). Tracked by `MA-DOC-008`. Grants no acceptance and changes no other lifecycle. Revision 2 records the owner's identity decisions (atlases primary; iridescent tail, lavender and rainbow both correct) and adds the Roshan appearance analysis, VL2a variance review and questions Q12–Q16. Revision 3 records the owner's answers to Q12–Q16 and links the Roshan art repair handoff. |
| `docs/handoffs/codex_visual_design_language_2026-09-30/VISUAL_LANGUAGE_AUDIT.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested audit at dev `b65c21fd` (V1 static, direct inspection of approved images, read-only source-file measurements): the master audit only routes; one of ten `DL-VIS-*` rules has numbers; Roshan's approved atlases show two tails while design 01 and 02 describe a third; contour colour named seven ways; nine rubrics; no exemplar registry. Measurements are indicators under `DL-VIS-08`, not acceptance. |
| `docs/handoffs/codex_visual_design_language_2026-09-30/ROSHAN_APPEARANCE_ANALYSIS.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested analysis at dev `b65c21fd` (measured frame by frame and reviewed by eye; source-file indicators under `DL-VIS-08`): all 53 runtime Roshan images; the tail is consistent under the owner's iridescence decision; a second design (older, loose rainbow lock, no tiara, muted finish) in 13 career cards, 13 career atlases and the playground sprites, traced to the identity reference `roshan_sprite.png`; a 21-item variance register (RV-01 to RV-21), answered by the owner on 2026-09-30. No image changed. |
| `docs/handoffs/codex_visual_design_language_2026-09-30/VISUAL_LANGUAGE_DRAFT.md` | 🟣 | `PROPOSED / CANDIDATE` draft of `design/reference/VISUAL_LANGUAGE.md`: pillars, families, Roshan's owner-settled identity (iridescent tail with three light states, base outfit, measured palette), cast identity seeds, tokens with sources, composition, layers and motion, technical rules, making and reviewing art, learning loop and open owner questions (Roshan's identity answered 2026-09-30). Not authority until landed. |
| `docs/handoffs/codex_visual_design_language_2026-09-30/templates/ART_STYLE_CARD_V1.md` | 🟣 | `PROPOSED / CANDIDATE` template: one card per still-art job with two to four bound exemplars, the proven prompt order, post-processing and checks. |
| `docs/handoffs/codex_visual_design_language_2026-09-30/templates/ART_REVIEW_CARD_V1.md` | 🟣 | `PROPOSED / CANDIDATE` template: one art review with vetoes, six axes and weakest-axis scoring; runtime pass needs an in-scene phone-size capture; only the owner gives 5/5. |

## Roshan art repair handoff (2026-09-30)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_roshan_art_repairs_2026-09-30/README.md` | 🟣 | `PROPOSED / CANDIDATE` owner-commissioned Codex handoff prepared by Claude (written specification; no game change, no images) at dev `b65c21fd`: delete the retired backpack art outright (D-01, owner decision) and repair Roshan frame defects inside each image's own design (R-01 to R-11: Geologist fins, Pop Star ribbon, Magician baked effects, Astronaut hair, Farmer and Candy Maker flicker, a base-world tail flip, Racer halo, Nursery scale, checks). Tracked by `MA-ROSHAN-005`. Grants no acceptance. |

## Sky Lagoon motion references (2026-09-30)

| Doc | | Note |
|---|---|---|
| `assets_src/cinematics/sky_lagoon_local_motion_v1_2026-09-30/README.md` | 🟣 | `OWNER_REJECTED_AS_ANIMATION_REPLACEMENT / MOTION_REFERENCE_ONLY`; owner rejected source transformations and the swing lateral axis. Archive includes a new unaccepted eight-pose swing direction trial plus the historical source studies and rejected Wan takes. Spatial resampling/articulation is explicit; no fresh hand-painted frame redraw, AI motion-set, runtime, cinematic, device, child, owner or finding acceptance. Remote delivery depends on its immutable verification receipt. |
| `assets_src/cinematics/sky_lagoon_moderate_motion_v2_2026-09-30/README.md` | 🟣 | `CANDIDATE / MOTION_REFERENCE_ONLY`; owner-requested ten moderate-resolution object samples, native generated pose sheets, Aseprite cleanup/masters and a layered Sky Lagoon context study. Source pixels/provenance preserved; six-key polish and owner/runtime/device/child/cinematic acceptance remain open. Exact remote byte verification is separate. |
| `assets_src/cinematics/sky_lagoon_review_v3_2026-10-01/README.md` | 🟣 | `AGENT_REVIEWED_REFERENCE_CANDIDATE`; two correction/review passes on ten object studies and a layered Sky Lagoon sample. Preserved sources, 72 states, attached ropes and stationary berries. No runtime, owner, device, child, cinematic or finding acceptance. |

## Self-improvement loop handoff (2026-10-03)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_self_improvement_loop_2026-10-03/README.md` | 🟣 | `PROPOSED / CANDIDATE` owner-requested Codex handoff prepared by Claude (analysis, written specification, templates, seeds and a read-only measurement tool; no game change, no images) at dev `f2140465`: the loop study, keep, find, plan, prompt, build, check, learn; work packages LP0–LP11 (cycle home, study runner, strengths register, lesson fields, decision-register intake, living roadmap, prompt catalogue and recipes, monthly verification sweep, master-audit refinements, loop health, owner-gated cadence); a build order across all outstanding handoffs; owner questions Q1–Q8. Tracked by `MA-DOC-009`. Grants no acceptance. Implemented in part by Codex at `4cb14feb`; reviewed and repaired on 2026-10-03 (`docs/handoffs/codex_loop_review_2026-10-03/`). |
| `docs/handoffs/codex_self_improvement_loop_2026-10-03/LOOP_AUDIT.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested audit at dev `f2140465` (V1 static, read-only sweeps and measurement): the parts of the loop exist but it does not turn; twelve feedback loops with what breaks each; two advisory sensors that fail silently (`MA-CI-008`); strengths, weaknesses, roadmap, prompts and learning. Counts are dated measurements, not live status. |
| `docs/handoffs/codex_self_improvement_loop_2026-10-03/CYCLE_0_STUDY_REPORT.md` | 🔵 | `SUPPORTING_CURRENT` worked example of the cycle report at dev `f2140465`, written by hand with existing tools: changes since 2026-09-30, strengths and weaknesses observed, loop health baseline, roadmap delta, five ready-to-say prompts, five owner questions and the lessons this cycle wrote back. |
| `docs/handoffs/codex_self_improvement_loop_2026-10-03/templates/STUDY_REPORT_V1.md` | 🟣 | `PROPOSED / CANDIDATE` template: one short report per loop cycle with numbers from the study runner. |
| `docs/handoffs/codex_self_improvement_loop_2026-10-03/templates/PROMPT_RECIPE_V1.md` | 🟣 | `PROPOSED / CANDIDATE` template: how one short owner prompt expands into a complete plan (intent, read-first references, expansion with variety rules, owner touchpoints, build and check, learn). |

## Self-improvement loop implementation — 2026-10-03

| Doc | | Note |
|---|---|---|
| `audit/cycles/2026-10-03/CURRENT_SURFACES.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); generated list of fourteen shipping surfaces at the 2026-10-03 infrastructure study (source presence only); later cycles add probes, captures and findings per surface. |
| `audit/cycles/2026-10-03/DEVICE_SESSION.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); generated at the infrastructure study; identical to the technical sweep and superseded for phone use by later cycles' plain device scripts. |
| `audit/cycles/2026-10-03/GENERATED_CHANGE_HISTORY.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); impact records in date order with their declared validation, generated at the infrastructure study; records stay authoritative. |
| `audit/cycles/2026-10-03/IMPLEMENTATION.md` | 🔵 | `SUPPORTING_CURRENT`; Codex's implementation notes for LP0–LP11 at `4cb14feb` and the owner's 2026-10-03 latest-Godot direction; reviewed in the loop review. |
| `audit/cycles/2026-10-03/OWNER_REVIEW.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); generated owner page at the infrastructure study; copied developer steps (an older APK, Godot 4.7.1); superseded for owner use by later cycles' plain checklists. |
| `audit/cycles/2026-10-03/ROADMAP.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); the roadmap as generated at the infrastructure study (all open findings, one template prompt); kept as the record of that cycle; `audit/ROADMAP.md` is current. |
| `audit/cycles/2026-10-03/STUDY_REPORT.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); infrastructure study of `30d82725` plus uncommitted implementation changes, with CI from before the sensor repair; not reproducible from git; reviewed in the loop review. |
| `audit/cycles/2026-10-03/VERIFICATION_SWEEP.md` | ⚪ | `HISTORICAL_EVIDENCE` (superseded for current use by cycle `2026-10-03b`); technical list of the twelve fixes awaiting verification with canonical wording, generated at the infrastructure study. |
| `audit/cycles/2026-10-03-baseline/PLANNING_HISTORY.md` | ⚪ | `HISTORICAL_EVIDENCE`; verbatim dated planning/repair evidence at loop intake; relocation of links does not renew its old acceptance. |
| `audit/cycles/2026-10-03-baseline/REPAIR_ORDER_HISTORY.md` | ⚪ | `HISTORICAL_EVIDENCE`; verbatim dated planning/repair evidence at loop intake; relocation of links does not renew its old acceptance. |
| `audit/cycles/README.md` | 🔵 | `SUPPORTING_CURRENT`; how to run a study cycle (committed heads, Claude's judgement file, recipes rendered from the catalogue, append-only decisions, plain verification pages) and the cycle index. |
| `audit/ROADMAP.md` | 🔵 | `SUPPORTING_CURRENT`; the living roadmap, regenerated each cycle: lanes by lifecycle (Repair, Verify, Decide, Waiting, Parked, Strengthen, Grow), recorded owner priority and severity first, every line sayable as a prompt. |
| `design/reference/OWNER_DECISIONS.md` | 🔵 | `SUPPORTING_CURRENT`; generated view of evidence-backed owner answers and separately labelled operating defaults. Original decision dates/sources and scope control;2026-10-04 adds whole-figure retake and multi-anchor Aseprite scale correction with executable checks. Defaults are not owner answers. |
| `design/reference/recipes/add_job.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/art.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/character_animation.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/companion.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/event.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/gold_star.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/new_chapter.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/polish.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/publish_handoff.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/release.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/repair.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/retire.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/room_activity.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/story_clip.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/study.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/recipes/voice_lines.md` | 🔵 | `SUPPORTING_CURRENT`; source-bound prompt expansion and reserved owner touchpoints; a recipe grants no runtime, art, device, child, owner or release acceptance. |
| `design/reference/GOLD_STAR.md` | 🔵 | `SUPPORTING_CURRENT`; generated gold-star scorecard and reference model from design/reference/games.json and gold_star.json (tools/gold_star.py --render): twelve DL-bound criteria, a deterministic 1-5 rating, hash-bound scores and reference patterns. Evidence for development choices, never visual, device, child or owner acceptance; C12 stays 0 until those results are recorded. |
| `design/reference/STRENGTHS.md` | 🔵 | `SUPPORTING_CURRENT`; generated source-hash-bound strengths; candidate evidence and narrowly accepted owner constraints remain distinct from visual/exemplar/product acceptance. |
| `design/templates/PROMPT_RECIPE_V1.md` | 🔵 | `SUPPORTING_CURRENT`; operational loop template from the commissioned handoff; numbers must derive from study.json and actual acceptance evidence remains required. |
| `design/templates/STUDY_REPORT_V1.md` | 🔵 | `SUPPORTING_CURRENT`; operational loop template from the commissioned handoff; numbers must derive from study.json and actual acceptance evidence remains required. |

Latest stable Godot reverified 2026-10-03 at the owner’s request: 4.7.2-stable, as listed by the official download page. Active Opera capture validators and default local CI selection now use tools/godot_baseline.json; historical engine evidence retains its recorded versions.

## Loop review and repair — 2026-10-03

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_loop_review_2026-10-03/REVIEW.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested audit, evaluation and repair record of the loop implementation at `4cb14feb` (findings LR-01 to LR-27, scorecards against LP0–LP11 and AC-1 to AC-10, the owner's four asks before and after). Claude fixed LR-01 to LR-22 in the same change; no game file, image or lifecycle closure. |
| `docs/handoffs/codex_loop_review_2026-10-03/README.md` | 🟣 | `PROPOSED / CANDIDATE` Codex handoff for what the review left: CR0 the owner's Chef verdict (backwards pour and overdraw; revision 2), CR1 a possible Chef first-step stall (reproduce first), CR2 CI captures on the fallback renderer, CR3 Opera pacing coverage, CR4 probe and workflow repairs, CR5 register corrections and a text-hygiene check, CR6 a fresh-agent cold start. Grants no acceptance. |

## Study cycle 2026-10-03b

| Doc | | Note |
|---|---|---|
| `audit/cycles/2026-10-03b/STUDY_REPORT.md` | 🔵 | `SUPPORTING_CURRENT`; owner report of the first reproducible cycle at the repair head: numbers from study.json, Claude's judgement from judgement.json (strengths, weaknesses, five prompts, numbered questions). Machine evidence only. |
| `audit/cycles/2026-10-03b/ROADMAP.md` | 🔵 | `SUPPORTING_CURRENT`; roadmap as generated this cycle (lanes by lifecycle, owner priority and severity first); `audit/ROADMAP.md` holds the same render. |
| `audit/cycles/2026-10-03b/OWNER_REVIEW.md` | 🔵 | `SUPPORTING_CURRENT`; plain owner checklist for the twelve fixes awaiting verification, from design/reference/verification_checks.json; no session booked. |
| `audit/cycles/2026-10-03b/DEVICE_SESSION.md` | 🔵 | `SUPPORTING_CURRENT`; thirty-minute phone script for the same fixes (includes the possible Chef first-step stall check); no session booked. |
| `audit/cycles/2026-10-03b/VERIFICATION_SWEEP.md` | 🔵 | `SUPPORTING_CURRENT`; technical list of the twelve fixes awaiting verification with canonical wording. |
| `audit/cycles/2026-10-03b/CURRENT_SURFACES.md` | 🔵 | `SUPPORTING_CURRENT`; machine evidence per shipping surface: last source change, trusted probes at the head, review captures, open findings. Not visual, device, child or owner acceptance. |
| `audit/cycles/2026-10-03b/GENERATED_CHANGE_HISTORY.md` | 🔵 | `SUPPORTING_CURRENT`; impact records in date order with their declared validation; records stay authoritative. |

## Gold-star audit and tool — 2026-10-03

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_gold_star_2026-10-03/README.md` | 🟣 | `PROPOSED / CANDIDATE` Codex handoff entry point: GS0 repair the P0 `MA-PLAY-005` (Chapter 2 story careers cannot start), GS1 repair `MA-OPERA-013`, GS2 Pool art and voice, GS3 gold-star lines for the protected workflow (owner authority), GS4 scorecard upkeep, GS5 the measured overdraw repairs (`MA-VIS-008`); six owner questions with defaults. Grants no acceptance. Revision 5 (2026-10-04): GS2 and GS5 carry status notes pointing to the Pool five-star packet, which completes GS5's Pool items. |
| `docs/handoffs/codex_gold_star_2026-10-03/POOL_FIVE_STAR.md` | 🟣 | `PROPOSED / CANDIDATE` Mermaid Pool five-star proposal: Claude's code changes by criterion (truthful lines, approved guide and effect art, queued taps and pulls, lane retarget, Roshan's colours under the room tint, real-input probe legs), machine verification, the three human checks for a gold star, and the embedded Codex art and voice handoff GS2; corrected 2026-10-04: the refined overdraw criteria hold the Pool at 3/5 until GS5. Machine evidence only. Updated later on 2026-10-04: the Pool's overdraw is repaired (`MA-VIS-009`) and the current plan is the Pool five-star framework. |
| `docs/handoffs/codex_gold_star_2026-10-03/AUDIT.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested game-wide audit at dev `87f99268`: strongest and weakest games on the gold-star rubric, what a child can reach from a fresh save, new findings `MA-PLAY-005` (P0) and `MA-OPERA-013` (P1), and the choice of the Mermaid Pool as the reference model. Code reading plus one scratch runtime check; no device, child or owner acceptance. |

## Mermaid Pool five-star round — 2026-10-04

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_pool_five_star_2026-10-04/FRAMEWORK.md` | 🟣 | `PROPOSED / CANDIDATE` owner-requested five-star framework for the master audit's first refined area, the Day One Mermaid Pool: the definition by pillar and rule, the beat-by-beat sequence, Claude's code repairs (`MA-VIS-009`, `MA-PLAY-006`, `MA-TOUCH-003`, all fixed pending verification), the corrected overdraw meter, before and after measurements, the gap register, the ordered path to 4/5 and 5/5, and the phone, child and owner sessions. Machine evidence only. Revision 2 (2026-10-05): section 11 records the owner's answers to QP-1 to QP-3. Rumi rises once, in the clip; the castle stops drawing under story clips; the QP-2 dirty-look scope is open as QP-2a. |
| `docs/handoffs/codex_pool_five_star_2026-10-04/README.md` | 🟣 | `PROPOSED / CANDIDATE` Codex handoff for the Pool: P1 phone-size review captures for OD2, P2 Roshan's authored scoop, scrub and tug (scoop pilot), P3 room-lit prop family, P4 Rumi's rise (after owner QP-1), P5 swimmer paddle loop and ripple review, P6 water-true catch feedback, P7 voice, P8 device evidence; three owner questions. Grants no acceptance. Revision 2 (2026-10-05): the owner's answers are recorded, P4 is withdrawn (the clip owns Rumi's one rise), P6 waits for QP-2a, and P1's capture list follows the new finale. |

## Animation workflow policy — 2026-10-03

| Document | State | Scope |
|---|---|---|
| `design/animation/WORKFLOW_OPTIONS_2026-10-03.md` | 🔵 | `SUPPORTING_CURRENT`; dated source/receipt research for RTX 3060 Ti 8 GB, Aseprite, Wan/LTX/Kling costs and a bounded pilot. Includes linked source-only local benchmarks, measured2.5 W4A8 fit and blur failures; no paid job, runtime/device/child/owner acceptance or finding closure. Prices require recheck before spending. |
| `design/templates/ANIMATION_JOB_CARD_V1.md` | 🔵 | `CANONICAL_CURRENT` production/derivation sidecar under DL-MOT-14–16 and DL-CIN-11: inputs/method, limits, attempts, native/master/edit/export provenance and independent reviews. Does not replace the Grok executable V1 card or accept output. |

For new production, the 2026-10-03 owner decision supersedes older compulsory
independent-still/method-ban summaries, including preserved packet/archive prose.
Historical hashes, candidate rejections and acceptance claims are not upgraded.
Security, source-specific book/selected-cut rules, canon, true Canvas and
release/device/child/owner authority retain precedence.

## Registered whole-figure wave study (2026-10-04)

| Doc | | Note |
|---|---|---|
| `assets_src/cinematics/ltx_registered_wave_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; owner-commissioned whole-figure Roshan wave study, native LTX-Video 2B blur failures, owner-rejected limb-only correction, root-registered inputs and full-frame Aseprite/editable master/hash receipts. Reference only; no runtime, production/device/child/owner acceptance or finding closure. |

| `assets_src/cinematics/ltx_retake_repair_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; owner-commissioned bounded whole-figure Aseprite/keyframe and quantized LTX-2.3 temporal-retake hardware study on RTX 3060 Ti 8 GB. Native outputs, rejected candidates and execution/visual limits remain explicit; no runtime, production, device, child or owner acceptance. |

| `assets_src/cinematics/ltx_two_pass_wave_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; owner-directed native two-pass 2B portrait refinement and conditional 8 GB LTX-2.3 comparison, complete-figure Aseprite guides, one missing lowering key, preserved failures and actual cost/execution receipts. No production/runtime/device/child/owner acceptance. |

| `assets_src/cinematics/ltx_two_pass_wave_20261004/briefs/LTX25_PREFLIGHT.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; pinned next-candidate research and exact2.5 component/access preflight, no installation or measured2.5 footage. |
| `assets_src/cinematics/ltx_two_pass_wave_20261004/comparison/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; native1:1 same-content comparison layout and failure limits, no production acceptance. |

| `assets_src/cinematics/ltx25_8gb_wave_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; Five actual8GB W4A8 two-pass/retake/NAG/48fps/multi-anchor Roshan tests, one named whole-figure key redraw, native failures, Aseprite scale filtering and costs; no production/runtime/device/child/owner acceptance or finding closure. |

| `assets_src/cinematics/ltx25_8gb_wave_20261004/briefs/BLUR_REPAIR_METHODS.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; Pinned official detail-adapter/DFR and community de-rope research; measured NAG/48fps limits, separate adapter access pending. |
## Roshan motion language analysis and handoff (2026-10-04)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_roshan_motion_language_2026-10-04/README.md` | 🟣 | `PROPOSED / CANDIDATE` owner-requested Codex handoff prepared by Claude (written specification; no game change, no images) at dev `8a2f30cb`: RM0 review the unreviewed Grok swim returns, RM1 record decisions and adopt the motion locks, RM2 runtime repairs with existing art (fin side in gesture contexts, held career keys, authored holds, cross-fade measurement), RM3–RM8 authored side-view swim, start/stop/turn, idle and work contact clips, gesture family, careers and land travel; Grok and local-pipeline refinements; owner questions Q1–Q6. Tracked by `MA-ROSHAN-006`. Grants no acceptance. Revision 2 records the owner's 2026-10-04 answers and replaces the clip-by-clip plan with the Roshan animation template: RM0 digest the Grok and local test documents, RM1 card validator, general LTX runner and Aseprite bridge, RM2 runtime repairs, RM3 five Phase A test clips, RM4 adopt the template, RM5 every room and game, RM6 polish; questions Q2, Q7, Q8. |
| `docs/handoffs/codex_roshan_motion_language_2026-10-04/ANALYSIS.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested analysis of Roshan's motion at dev `8a2f30cb`: runtime playback by location, measured fin and ponytail sides and frame-to-frame change (numbers only), Grok and local-pipeline history with owner verdicts, ten proposed motion locks M1–M10 and a fourteen-clip canonical set. The locks are proposals until the owner answers Q1, Q2 and Q4; the 2026-09-11 movement language remains the binding acting direction. Revision 2 updates the style rules (left/right orientation, rich motion, Sky Lagoon gentle swim) and records the answered questions. |
| `docs/handoffs/codex_roshan_motion_language_2026-10-04/TEMPLATE.md` | 🟣 | `PROPOSED / CANDIDATE` Roshan animation template V1 at the owner's direction (2026-10-04): scene sheet, interaction table, ordered per-interaction decision (none, cinematic, reuse, code fix, variant, generate, keys then generate), routing to LTX locally through Codex's runner with Aseprite into the game, the animation card, style rules M1–M10, production and review, and the room-by-room pass. Becomes the standing template after the Phase A tests (RM4). Grants no acceptance. |
| `docs/handoffs/codex_roshan_motion_language_2026-10-04/SHOT_CARD_AUDIT.md` | 🔵 | `SUPPORTING_CURRENT` owner-requested audit of the Grok Imagine shot-card templates: V2 is the better template for new Grok jobs; neither covers sprite production; `CLAUDE.md` and `AGENTS.md` still name V1 and change only on the owner's instruction. |

## Claude wave studies: 2D deformation (rejected) and whole-frame revision (2026-10-05)

| Doc | | Note |
|---|---|---|
| `assets_src/cinematics/claude_2d_deform_wave_20261005/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` / `OWNER_REJECTED` 2026-10-05 (cut-out arm over another drawing's body; owner requires whole-figure frames); owner-commissioned replication of Codex's 41-frame Roshan wave without a video model: approved `roshan_gesture_a.png` keys only, layered whole-figure MLS/per-segment 2D deformation with drawing switches (no blends, no generated pixels), layered Aseprite master, same-index comparison with Codex's LTX-2.5 Union take 1 and 21 machine checks. Reference only; no runtime, production, device, child or owner acceptance or finding closure. |
| `assets_src/cinematics/claude_2d_deform_wave_20261005/JOB_CARD.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; animation job card V1 for the same study: bound inputs, method/routing exception, limits, tolerances and pending human/device/child/owner lanes. |
| `assets_src/cinematics/claude_whole_frame_wave_20261005/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE` / `OWNER_REJECTED` 2026-10-07 (size changes and frames built from pieces); revision 2 after the owner's 2026-10-05 correction: every frame is one complete approved `roshan_gesture_a.png` key bent as one figure, the whole body on one timing curve, one drawing change per beat, a one-layer Aseprite master and 20 machine checks. Reference only; no runtime, production, device, child or owner acceptance or finding closure. |
| `assets_src/cinematics/claude_whole_frame_wave_20261005/JOB_CARD.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; animation job card V1 for revision 2: owner direction, bound inputs, method, named arm-out key gap, tolerances and pending human/device/child/owner lanes. |

## Codex wave handoff: whole sprites at one size (2026-10-07)

| Doc | | Note |
|---|---|---|
| `docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/README.md` | 🟣 | `PROPOSED / CANDIDATE` written Claude-to-Codex specification after the owner's 2026-10-07 corrections: measured size and overdraw causes in three wave candidates, requirements W1–W6 (whole one-layer sprite, one size, fixed arm proportions, whole body at once, clip contract, numbers before review), the recommended Union route with a corrected guide family, and a numbers-only check (`tools/measure_wave.py`). Grants no acceptance. |

| `assets_src/cinematics/ltx25_scale_filter_v2_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; zero-generation deterministic repair of v1 bypass/scale-quantization bugs using existing fifth take; all41 frames registered, seven internal geometry failures retained, original timeline and Aseprite roundtrip verified. Grok shared-stage lessons, no runtime/device/child/owner acceptance. |

| `assets_src/cinematics/ltx25_focus_repair_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; owner-reported subtle size/focus errors, native detail diagnostics and actual same-latent1-vs2 decoder comparison. Default pixels reproduce exactly;2-step decode rejected for added grain/persistent defects. Whole-figure Aseprite structural-video conditioning then temporal detail repair is preferred but adapters remain untested on8GB; no new transformer/ImageGen jobs, runtime/finding/owner acceptance. |

| `assets_src/cinematics/ltx25_union_trial_20261004/README.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; actual two-take Union IC-LoRA structural-control study on LTX-2.5 W4A8/8GB. GPU patch application and complete two-pass outputs verified; shape stability improves in inspected native poses, but hands/focus/strict guide-root remain rejected. No runtime/device/child/owner acceptance or finding closure. |

| `assets_src/cinematics/ltx25_union_trial_20261004/JOB_CARD.md` | 🔵 | `SOURCE_PACKAGE_EVIDENCE`; bounded owner-commissioned structural-control job, schematic whole-figure Aseprite guide provenance/limits, exact pins, stage geometry and separate execution/quality gates; no artwork/runtime acceptance. |

| `audit/astronaut_walkthrough_20261007/README.md` | 🟣 | `SUPPORTING_CURRENT / DIAGNOSTIC_REVIEW` owner-requested illustrated Astronaut steps at dirty candidate96274aab with exact source hashes; historical V8 native PNGs at surface5685 (PIPE rendering changed to856b; current native refresh pending) and separate SVG annotations, source/API versus real-input distinctions, route/board/park/ordinary/audio/replay gaps and native supervisor failure preserved. No4.6, DL-QA-11, full-speed, independent/device/child/owner or release acceptance; GitHub publication pending full trusted suite and branch gates. |
