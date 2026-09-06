# Pearl Stage UI concept review — 2026-09-05

**Historical review; world-style verdict superseded 2026-09-06.** The
[non-UI world re-audit](UI_WORLD_CONGRUENCE_REAUDIT_2026-09-06.md) finds the
v1 concepts unsuitable as a reusable game-world style/material baseline.
Readability and proposed target results below retain their narrow scopes;
matching these menus to each other did not prove world congruence. Use the
[revision-2 specification](../design/11_UI_PEARL_STAGE_LANGUAGE.md) for future
work. Original images, prompts and the earlier reasoning below are preserved
as history, not continuing style approval.

Authority: `SUPPORTING_CURRENT`, bounded concept review. Reviewer: Astra agent, independent of concept generation. This is an AI visual review, not a human or owner approval. Source baseline: `aad0d450d8b8f1381badeeb4bcb939181115ab00`, branch `codex/ui-opera-design-language-20260905`.

## Scope and authority

The owner requests a slightly maximalist, bright, cartoony, crafted and painterly shell/pearl/rainbow UI taking its visual cues from the Opera stage worlds. Richness must coexist with one-finger, non-reader use. This review evaluates generated concepts; it neither implements UI nor accepts runtime assets.

Binding sources read: `AGENTS.md`, `SECURITY.md`, `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` sections 2, 4, 5, 8, 16, 19 and the new section 21; `design/11_UI_PEARL_STAGE_LANGUAGE.md`; and `audit/MASTER_AUDIT_2026-08-09.md` sections 2–3. `MENU_UI_SYSTEM_AUDIT_2026-08-01.md` is historical evidence: its shared-component census is useful, but its 15/15 upgrade claim does not prove current visual acceptance; the live 3D vehicle and old Opera lobby premises are superseded.

The newer owner style request controls the exact aesthetic scope. No concept score weakens protected art, save, true-2D, touch, typography, evidence, or release rules. No 5/5 score is granted (`DL-VIS-07`).

## Existing art inspected before concept review

All paths below are relative to the repository. Files were opened with `view_image`; hashes are SHA-256 of their unchanged native bytes.

| Reference | SHA-256 | Visual evidence and limited role |
|---|---|---|
| `assets_src/imagegen/opera_codex_2026-08-02/native/world_ballerina_native.png` | `f28231f936b9e63e0697a14122a354ee4c0bad1864538fddbdf16147a311f544` | Painted coral shell pavilions, creamy pearls and gold trim, lilac/aqua shaded bands, rounded carved forms and grouped garden ornament. Material/style reference, not a menu layout or current runtime acceptance. |
| `assets_src/imagegen/opera_codex_2026-08-02/native/world_candymaker_native.png` | `e40eb603a6c1e8f2c57be2e704ae0017426f11366de847afad91d57fbd93b017` | Chunky crafted coral/aqua machinery, restrained satin highlights, soft lavender distance and broad quiet floor. Material and hierarchy reference, not approval of every painted hotspot. |
| `assets_src/imagegen/opera_codex_2026-08-02/native/task_card_frame_alpha_native.png` | `102818a827bdbb7b26680c6abbf06da2940f14162d1e09bdf4bd71fc7e404f0b` | Existing shell/pearl frame with dark contour, lilac band and gold trim. Reuse evidence; its evenly repeated small beads need not be copied into every new control. |

## Bounded pass/fail rubric

Every applicable concept gate must pass for `CONCEPT_VISUAL_PASS`. A failed mandatory gate makes that image `CONCEPT_VISUAL_FAIL`; an uninspected or unbound image is `NOT_REVIEWED`. Non-applicable fields must state why. These labels are local concept dispositions, not canonical finding lifecycle or verification-level upgrades.

| Gate | PASS condition | Failure condition / authority |
|---|---|---|
| PS-01 Craft and medium | Rounded hand-shaped painted masses, broad value bands, materially specific shells/pearls, consistent contour and satin restraint. | Cheap default-panel appearance, flat generic vector-like geometry as the dominant material, noisy photographic/PBR rendering, or redesign of protected identity. Owner brief; `DL-VIS-01–06`. |
| PS-02 Controlled abundance | Rich shell, pearl, rainbow and stage ornament forms two or three quiet clusters; broad action wells remain clear. | Evenly scattered glitter/detail, full-screen neon, decoration more salient than action, or ornate silhouette confused with extra controls. `DL-VIS-01`, `03–05`; `DL-READ-01`, `03`. |
| PS-03 Phone proxy | At an explicitly labelled whole-image phone-size review reduction, required pictograms and action grouping remain distinguishable without zoom. | Icon collapse, muddy figure/ground, cutoff, or reliance on tiny details. `DL-READ-02`. A proxy does not satisfy the actual device gate. |
| PS-04 Focal action | Pause has a clearly dominant resume; a chooser presents one coherent choice task; only one neutral back/close is apparent. | Multiple equally dominant competing actions, ambiguous exit duplication, or ornamental fake affordances. `DL-READ-03`; `DL-UI-06`. |
| PS-05 Picture semantics | Every intended required route has a legible authored pictogram/picture; no text, emoji fallback, number or color alone carries meaning. | Text-only controls, indecipherable symbols, unexplained modes or decorative text that looks instructional. `DL-UI-07`; `DL-TYPE-06–07`; `DL-READ-04`. Exact voice comprehension remains untested. |
| PS-06 Touch allocation | A proposed 1280×720 mapping reserves at least 110×110 for each required child action or documents an equivalently generous region, with separated neighbors. | Required target region is visibly too small or crowded without an explicit equivalent allocation. `DL-UI-03` is SHOULD; a justified alternative is evidence, not an automatic waiver. Artwork bounds are not runtime hitboxes. |
| PS-07 Family and states | Screens share surface, contour, icon-well and back grammar. Any represented pressed/focus/selected/locked state differs through visible shape/value/pictogram cues, not just hue. | Inconsistent family, focus lost in bead trim, ambiguous selected/disabled affordance or accidental child-facing settings. `DL-UI-06`; `DL-TYPE-03–04`. Missing live-state evidence remains NOT TESTED. |
| PS-08 Supplemental type | Any child action/choice/state type is proposed at >=28px at base canvas; required meaning survives ignoring all words. Board-only annotations are explicitly adult review labels. | Undersized semantic text or lettering used to repair unclear pictures. `DL-TYPE-05–06`. Generated lettering is not an approved font. |
| PS-09 Evidence integrity | Exact native path, dimensions, SHA-256, generation provenance and clearly named review derivatives; rejected attempts retained as evidence. | Missing binding, a review resize passed off as generated art, unrecorded edits or an acceptance claim unsupported by evidence. `DL-QA-01`, `03`, `07`; protected-source rules. |

Canonical section-21 mapping: PS-01 → `DL-UI-VIS-01`; PS-02 → `02`; PS-04/05/08 → `04`; PS-03/06 → `05`; PS-07 → `03` and `06`; pointer-specific PS-03/05 → `07`; PS-09 → `08` and `09`. `DL-UI-VIS-10` is the outstanding rollout evidence boundary. Full rule results below distinguish visible subclauses from absent runtime evidence. The design-11 spec has no observed conflict with the prior canonical contract; its candidate palette/layout tokens are proposals, not owner-approved runtime values.

## Evidence boundary and outstanding gates

Concept inspection is static artifact evidence (`V1 STATIC`) plus an explicitly scoped AI visual opinion. It is not `V4 CAPTURE`: no screenshot here is bound to an executing Godot state. Whole-image phone review reductions are inspection aids, not `V5 DEVICE`, runtime textures, or new image generations.

Runtime, actual hit geometry, input cancellation/one-touch ownership, save preservation, narration/pointers, focus/press behavior, supported aspect ratios, font selection/licensing/fallbacks, longest-string/130% expansion, Mobile/Speedy performance, exact Godot 4.7.2 probes, APK/device, observed child and owner style acceptance are **NOT TESTED / NOT GRANTED** by this review. No existing canonical finding closes from this document.

## Image findings

### Pause concept v1

- File: `assets_src/ui/pearl_stage_v1/concepts/pause_menu_pearl_stage_concept_v1.png`.
- Native dimensions: 1672×941. SHA-256: `cb3dd0824943562ffc4d2eb9729dbbaf42fbd71d508421066950d8ffed427b3f`.
- Inspected unchanged native image and `build/ui_pearl_stage_review_2026-09-05/pause_v1_review_only_640.png`, 640×360, SHA-256 `3ce02098faf8a369ae379b5be7a7319a8b5c39fcaf4ec00ed6caf62b8d162f4a`. The latter is a whole-canvas Lanczos inspection reduction, not new art, source material, runtime texture or device evidence.
- Generator's intended map: resume centered, approximately 240×240 at 1280×720; lower three controls approximately 120–140 square each. Lower controls are one activity-chooser medallion, sound and teddy. Resume closes pause and is its single neutral exit.

| Gate | Result | Exact observation |
|---|---|---|
| PS-01 | PASS | Warm coral crown, creamy iridescent pearls, broad aqua/lilac folds and sculpted gold bands read as coherent painted craft. No protected character is shown or substituted. |
| PS-02 | PASS | Richness groups at crown and lower outside corners. Cream panel interior and separate lilac icon wells give actions quieter grounds. Outside stage stays darker and lower-priority. |
| PS-03 | PASS, proxy only | At 640×360, resume triangle, speaker and teddy remain identifiable. Four small chooser symbols remain a recognizable category cluster; their exact meanings need not each carry an action. |
| PS-04 | PASS | Resume is substantially larger and centrally isolated; it is the pause-close route. No competing back/X is drawn. Lower three controls share subordinate weight. |
| PS-05 | PASS, depiction only | All four intended actions have pictures; there is no reading route. The grid is a chooser pictogram, not four required actions. Exact voice and child comprehension remain untested. |
| PS-06 | PASS, allocation only | Proposed >=120-square secondary targets and 240-square resume allow the 110-square expectation without crowding. Visible medallions support that allocation. Runtime hit regions are untested. |
| PS-07 | PASS for shown default family | Common gold/plum contours, lilac wells and pearl bases unify controls. Pressed, focus, selected and muted states are absent and NOT TESTED, not silently passed. |
| PS-08 | PASS / no text | No lettering carries a child meaning. No font is selected or approved. |
| PS-09 | PENDING SIDECAR | Native path/dimensions/hash and review derivative are bound. Generation prompt/reference provenance is still being written by the generator agent. |

**Visual disposition: PASS for the inspected default concept. Packet disposition: PENDING until the generation sidecar is verified.** This is not a runtime, device, child or owner approval.

Implementation guardrail `PS-P01` (P2, proposed-state risk): the chooser pictogram has four separately framed colored squares. These must remain one medallion action, with a single generous hit region and unified pressed/focus feedback. They must not become four small buttons. An actual four-action interpretation fails PS-05/06 and requires a redesign. The exact narration should introduce the chooser. No regeneration is required for the current one-target interpretation.

Scope guardrail `PS-P02`: this simplified image is a material/layout study. Its chooser/sound/teddy pictures do not prove that stickers, critters, Stuffie and contextual activity leave have been retained. A runtime rollout must preserve those routes; a simplified concept grants no permission to delete them.

### Activity chooser concept v1

- File: `assets_src/ui/pearl_stage_v1/concepts/activity_chooser_pearl_stage_concept_v1.png`.
- Native dimensions: 1672×941. SHA-256: `28c8308a561b1088cc559fcb0cb9ae601a2d033f55d9cd7dd685823fd3fd6460`.
- Inspected unchanged native image and `build/ui_pearl_stage_review_2026-09-05/chooser_v1_review_only_640.png`, 640×360, SHA-256 `f8edc1a8b1610a97c284455d0f2c54618d1dc8a4ef2ff4386a09231a2b8c97bd`. Whole-canvas Lanczos review reduction only, with the same limits as the pause proxy.
- Proposed map: central sticker book approximately 190 square; seahorse, teddy, palette/brush and music/microphone approximately 145–160 square; upper-left neutral close approximately 120 square, all at 1280×720 base. Exact rectangles are pending.

| Gate | Result | Exact observation |
|---|---|---|
| PS-01 | PASS | Same broad pearl/aqua shell plane, lilac fold bands, coral crown and painted gold edging as pause. The illustrative symbols remain specific and rounded. |
| PS-02 | PASS | Most fine ornament is outside the action wells. Large quiet aqua/cream gaps separate the five pictures. Warm highlights do not turn the whole screen into neon. |
| PS-03 | PASS, proxy only | Seahorse, star book, teddy, paint palette, music note/microphone and close X all survive the 640×360 view without zoom. |
| PS-04 | PASS | Book owns the central focal position and scale. Remaining choices form one subordinate choice group. One upper-left close is clearly separate and non-punitive. |
| PS-05 | PASS, depiction only | Direct pictures need no labels or separate confirmation. Seahorse must map to the intended existing route through its contextual voice; no new activity is authorized. |
| PS-06 | PASS, size allocation only | All proposed controls allow >=110-square hit regions; separate medallions leave workable gutters. Exact rectangles, margins and hit ownership are pending. |
| PS-07 | PASS for shown default family | Frame/crown/contour/icon-well treatment matches pause. Other states are absent and NOT TESTED. |
| PS-08 | PASS / no text | No generated words, numbers or font claims. |
| PS-09 | PENDING SIDECAR | Exact inspected image and derivative are hashed; prompt/reference provenance is being prepared. |

**Visual disposition: PASS for the inspected default concept. Packet disposition: PENDING sidecar and exact target-allocation record.** The generic concept teddy is a navigation symbol, not an accepted replacement for a protected friend portrait. The seahorse must not silently create or rename a route.

### Section-21 rule ledger: pause v1 and chooser v1

| Canonical rule | Pause v1 | Chooser v1 | Evidence boundary / concrete requirement |
|---|---|---|---|
| `DL-UI-VIS-01` | PASS visible material | PASS visible material | Custom shell form and broad painted surfaces; no runtime consumer claim. |
| `DL-UI-VIS-02` | PASS visible hierarchy | PASS visible hierarchy | Quiet wells survive grouped ornament; pause grid is one pictogram under PS-P01. |
| `DL-UI-VIS-03` | PASS visual family | PASS visual family | Actual shared StorybookUI/theme integration NOT TESTED. |
| `DL-UI-VIS-04` | PASS shown picture/exit semantics | PASS shown picture/exit semantics | Actual voice, pointer, preserved routes, save and comprehension NOT TESTED. Pause route completeness remains PS-P02. |
| `DL-UI-VIS-05` | FAIL packet completeness, repair pending | FAIL packet completeness, repair pending | Phone proxies inspected; approximate target sizes supplied, but exact rectangles/separation/safe areas not yet recorded. No visual regeneration needed for this evidence gap. |
| `DL-UI-VIS-06` | NOT TESTED | NOT TESTED | Both images depict rest only; no press/focus/selected/cancel or stable runtime geometry proof. |
| `DL-UI-VIS-07` | N/A to static menu | N/A to static menu | Neither image contains a tutorial pointer. Live cue behavior remains NOT TESTED. |
| `DL-UI-VIS-08` | FAIL sidecar completeness, repair pending | FAIL sidecar completeness, repair pending | Existing references inspected and image hashes bound; exact prompt/reference sidecars pending. Concepts are non-runtime. |
| `DL-UI-VIS-09` | PASS for this bounded review | PASS for this bounded review | Independent native/proxy inspection and rule results recorded; missing evidence remains explicit. |
| `DL-UI-VIS-10` | NOT TESTED | NOT TESTED | No rollout/runtime/device/child/owner acceptance claimed. |

### Menu packet re-audit: evidence repairs

The preceding pending/fail rows preserve the initial evidence history. Sol subsequently supplied `assets_src/ui/pearl_stage_v1/provenance/generation_provenance.json`, the two executed prompt text files and exact proposed target rectangles. The repaired manifest inspected here has SHA-256 `965a40f34de1b28d66d8f11fcb86ed41ac24583d36494285040dbfd725b013ca`. Independent Python verification re-read the actual bytes: native outputs equal their project copies; both image dimensions match; every prompt and bound-reference SHA-256 matches; every reference dimension matches.

Initial pairwise rectangle inspection found pause's nearest gap was 20 px, below design 11's preferred 24 px, and chooser's true nearest gap was 35 px while its metadata reported 15 px (an axis projection between diagonally separated controls). Sol then moved only the pause *proposed target allocations* down by 5 px and corrected chooser metadata. No generated pixels were edited. A second independent check proves every proposed target is >=110×110, every target lies inside the stated `[64,64,1152,592]` base-canvas safe area, no pair overlaps, and the measured minimum Euclidean rectangle-edge distances exactly equal the repaired declarations: pause **25 px**, chooser **35 px**.

| Image | `DL-UI-VIS-05` re-audit | `DL-UI-VIS-08` re-audit | Final bounded concept packet result |
|---|---|---|---|
| Pause v1, unchanged SHA `cb3dd082…427b3f` | PASS proposed allocation and proxy evidence | PASS native/prompt/reference binding and reuse-gap record | **CONCEPT_VISUAL_PASS** for default material/layout study; runtime and complete route mapping untested |
| Chooser v1, unchanged SHA `28c8308a…3fd6460` | PASS proposed allocation and proxy evidence | PASS native/prompt/reference binding and reuse-gap record | **CONCEPT_VISUAL_PASS** for default material/layout study; actual route/voice/state behavior untested |

The repaired sidecar identifies speaker as **narration replay**, grid as one chooser action, seahorse as a sample Critter Book picture, and the teddy as a generic sample Stuffie/care symbol. It explicitly preserves the existing pause route inventory and denies new-route/owner/runtime/device claims. Its note restricts the executed prompt phrase “approved visual anchor” to a selected concept reference; that phrase is not evidence of owner approval.

### Navigation/tutorial component board v1

- File: `assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.png`.
- Native dimensions: 1672×941. SHA-256: `1e0a1018149917ab5f6f3b6edd187c2da8a1297f2585d287dcc4ff50d8008f7a`.
- Inspected unchanged native and `build/ui_pearl_stage_review_2026-09-05/board_v1_review_only_640.png`, 640×360, SHA-256 `9e0fa0ad15a555b67a5c1a53d835ebd084815dcff7ed21b5b5b8190a246244cc`. Whole-board Lanczos review reduction only; not device evidence or a child-facing simultaneous-screen layout.
- Role: adult component study. REST/PRESSED/SELECTED/REPLAY/BACK are review annotations, not a chosen runtime font or required child instruction. Rest/pressed/selected examples are compared side by side for adults; they are not three simultaneous child actions.

| Gate / canonical rule | Result | Exact observation or gap |
|---|---|---|
| PS-01 / `DL-UI-VIS-01` | PASS depicted material | Pearl crown, broad aqua/cream panel, gold/plum contour and lilac wells match both menu concepts. |
| PS-02 / `DL-UI-VIS-02` | PASS as adult comparison board | Grouped perimeter ornament leaves readable sample wells; multiple book pictures serve comparison, not competing child objectives. |
| PS-03 / `DL-UI-VIS-05` proxy clause | PASS, proxy only | At 640×360, book, helping hand, audio and doorway/return remain recognizable. Pressed sample is visibly inset/darker; selected check seal survives reduction. |
| PS-04/05 / `DL-UI-VIS-04` pictured semantics | PASS depicted samples | Helping hand points to book; audio and doorway/return pictures convey different roles. Text is supplemental board annotation. Actual contextual destination and narration remain untested. |
| PS-06 / `DL-UI-VIS-05` allocation clause | FAIL initial packet, repair pending | Initial sidecar has no target rectangles, separation or safe-area allocation. Adult state examples are not target-size proof. |
| PS-07 / `DL-UI-VIS-03` | PASS visual family | Same menu surfaces and contours, including matched star-book identity. Actual shared-helper implementation remains untested. |
| PS-07 / `DL-UI-VIS-06` | PASS shown rest/press/selected distinction; focus NOT TESTED | Press has reduced shell profile, inset shadow and contact outline. Selected adds persistent check seal and extra contour/crown beyond hue. No distinct focus sample or cancellation sequence is shown; stable runtime hit geometry is untested. |
| Pointer clause / `DL-UI-VIS-07` | FAIL arrow coverage; hand depiction PASS | The left sample contains a pointing hand whose fingertip reaches the lower-right book region. It contains no dedicated tutorial arrow with a tip aimed at a target. Doorway return is navigation, not a substitute for tutorial-arrow evidence. Live-target alignment, occlusion across motion, removal after success and passive/no-award behavior are untested. |
| PS-08 / `DL-TYPE-05–07` | PASS as labelled adult board | Readable review annotations carry no child-required meaning. They do not approve a runtime font, fallback or text size. |
| PS-09 / `DL-UI-VIS-08` | FAIL initial prompt binding, repair pending | Initial sidecar contains a prompt-intent summary, not a hashed exact executed prompt. Native/project equality and target record were requested. |
| PS-09 / `DL-UI-VIS-09` | PASS bounded review | Independent native/proxy inspection, exact image hash and per-rule gaps recorded. |
| `DL-UI-VIS-10` | NOT TESTED | No runtime, device, child or owner claim. |

Initial scope result: **visual PASS for shown component samples; incomplete for a complete navigation/tutorial family**. `PS-B01` records missing dedicated tutorial-arrow art; `PS-B02` records absent focus evidence. Neither is silently cleared by good rest/press/selected samples. Initial sidecar statement that the fingertip reaches the card “center” is inaccurate: it reaches the lower-right book region; a documentation correction was requested, with no pixel edit required.

### Component board re-audit: evidence repairs

Luna supplied the exact executed prompt at `assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.prompt.txt`, SHA-256 `0e5c08c42a2bf13cb45af989247971caa4102161d093ff48e84ad03661204eb5`, and updated the adjacent `.provenance.md`. Independent verification proves the native output and project image are byte-identical with the unchanged `1e0a1018…008f7a` hash. Its two references are the exact hashed menu images already inspected in this review. The fingertip-location statement now correctly names the lower-right book region and makes no live-runtime claim.

The sidecar proposes a future 1280×720 reconstruction: teaching target `[184,174,300,300]`, replay `[500,496,170,170]`, back `[738,496,170,170]`, all inside `[48,32,1184,656]` safe area. Independent rectangle checks pass >=110 dimensions, complete safe-area containment and zero overlap. Teaching-to-replay has 16 px horizontal and 22 px vertical separation, hence **27.203 px nearest Euclidean edge distance**; replay-to-back is **68 px**. The initial table's “22 px from teaching target” describes only the vertical gap, not the full nearest-edge distance. These are implementation allocations, not coordinates proven in the generated board or runtime.

`DL-UI-VIS-05` packet evidence now **PASS** for the explicit proposal/proxy scope and `DL-UI-VIS-08` prompt/native/reference binding now **PASS**. No pixels were repaired and neither missing-arrow nor missing-focus evidence is changed. **CONCEPT_VISUAL_PASS for the shown hand, book-state, replay and doorway-return samples; full arrow/tutorial/focus coverage remains incomplete.**

## Final bounded disposition

| Artifact | Concept result | Outstanding limits |
|---|---|---|
| Pause v1 | **PASS** default material/layout study | Complete live route inventory, pressed/focus states, voice and runtime geometry remain untested; four grid cells remain one pictogram. |
| Activity chooser v1 | **PASS** default material/layout study | Pictures are route samples; no new route/character approval. Live state, voice and runtime geometry remain untested. |
| Component board v1 | **PASS** shown component samples; **INCOMPLETE** full tutorial/navigation family | Dedicated tutorial-arrow coverage fails `DL-UI-VIS-07` scope; focus evidence absent. Three side-by-side state samples are adult review, not a child menu. |

All native files remain non-runtime concept references. This document grants no owner identity/style approval, runtime visual 5/5, Godot capture status, actual phone squint/touch evidence, child comprehension, release authorization, or master-audit closure. The independent reviewer edited only this audit Markdown and disposable ignored whole-image review reductions; no runtime, protected original, save, release or git state was changed.
