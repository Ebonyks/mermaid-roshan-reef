# Minigame art acceptance backlog — 2026-09-05

This backlog translates the current audit evidence into repair and acceptance work. It does not replace the master audit, assign new scores, or claim game-wide coverage. Existing scores below are dated observations from the audit packet; families marked unscored remain unscored until their exact runtime states are captured.

## Acceptance gate applied to every item

A candidate passes only when every applicable dimension is at least 4.5/5 in current Mobile runtime evidence, with no blocking defect:

1. **Identity/semantic function:** the object, pose, and state mean the intended action.
2. **Painted finish/material:** shading, texture, value, and palette belong to the established storybook language.
3. **Contour/alpha integrity:** clean authored silhouette, no background contamination, checkerboard, hard crop, or broken anatomy.
4. **Child readability:** recognizable at phone size, clear target/action, adequate contrast, one-finger legibility.
5. **Animation/contact:** authored state progression, stable pivot/anchor, believable contact, return/settle, and natural cadence for anything that moves.
6. **Scene ownership/composition:** the prop owns its action area, does not collide with HUD/reward layers, and preserves touch geometry.
7. **Family consistency:** adjacent states share scale, lighting, outline, material language, and intentional role differences.
8. **Technical integrity:** Mobile renderer, correct aspect/alpha/import, performance, provenance, and reproducible source hash.

Static props may mark animation inapplicable only with a reason. A clean isolated image never proves runtime acceptance or 5/5.

## P0 — direct blockers and high-value repairs

### 1. PictureGames / Garden — watering can

- **Observed problem:** live `assets/mg/wateringcan.png`, bound in `scripts/games/picture_games.gd:596`, is a 272×286 crop containing plant/background pixels and a hard boundary. It is displayed at `(1022,362)`, `130×137`, rotated about `0.32` radians. Current garden presentation is improved but remains below the target because this prop is visibly contaminated and materially weaker than the painted sun, butterflies, seed, and Roshan.
- **Repair type:** new generation or approved exact-purpose reuse; no suitable reuse was found. Preserve the current display/touch role unless an intentional spout-angle change is documented.
- **Candidates:** none direct. `assets/art35/cards/mg/wateringcan_wateringcan.png` is a flat icon and rejected. Keep current source out of acceptance after replacement; preserve it as baseline evidence.
- **Required Mobile states:** garden ready with five seeds; watering action/visible can; at least one sprout transition; all five mature; completion/reward; settle/re-entry. Capture 1280×720 and representative phone ratio with real processing cadence.
- **4.5 gates:** clean RGBA edges and no scene pixels; unmistakable handle/body/spout; spout points consistently with action; child-readable at 130×137; stable anchor through watering; no HUD/reward occlusion; matches garden lighting and outline; imported/hash/provenance recorded.
- **Acceptance gap:** current capture used manual ticking, so animation cadence remains unqualified even after a source replacement.

### 2. PictureGames / Garden — coordinated growth family

- **Observed problem:** live `k_sprout.png` and five mature files (`k_flower1`, `flower`, `flower2`, `k_flower2`, `flower3`) are a flat pastel/vector-like family, visibly below neighboring painted assets. The current live list is five distinct mature roles; `flower4.png` is not proven live.
- **Repair type:** coordinated new six-asset family (one sprout plus five distinct mature results), or a complete approved equivalent. Do not fill roles with two reused flowers.
- **Candidates:** `assets/props/story/flower_coral.png`, `flower_lavender.png`, `assets/terrain/flower.png`, and `flower2.png` are visual references/single-state candidates only. Their full-plant geometry does not directly fit the existing 228×228 slots.
- **Required Mobile states:** all seeds ready; each of five real tap transitions through sprout; each mature result individually; all five mature together; completion/reward; settle and re-entry. Record exact slot-to-source mapping.
- **4.5 gates:** distinct semantic silhouettes/colors; clear seed→sprout→mature progression; roots/stem bottom anchor remains grounded; consistent painterly finish and lighting; readable at phone size; no overlap/crowding; stable touch bounds; clean alpha/import/provenance; no state may be averaged away by family score.
- **Acceptance gap:** source replacement and natural animation cadence are both open.

### 3. PictureGames / Snowman — carrot and scene integration

- **Historical defect:** `assets/mg/carrot.png` was a tiny flat orange silhouette. The current candidate now directly reuses approved `assets/opera/worlds/widgets/widget_target_farmer_piece_0.png` in the selector, Snowman nose and family dinner; no pixels were changed. Do not commission another carrot merely because the surrounding scene remains weak.
- **Repair made:** nose artwork retains its -135-degree base orientation through chase waddle. The focused picture probe requires both travel and the intended angle. A visible configured cutaway diagnostic records matching runner/nose travel; failed and obscured capture attempts remain archived.
- **Current weak states:** independent run07 still review puts scene consistency at 3.6 and ownership/contact at 3.9. Plain snowballs and gray diagram-like terrain mismatch painted Roshan/carrot; header, back control and premature sticker banner compete; small Roshan weakens phone-scale contact clarity.
- **Next repair:** inventory approved snowy ground/background and coherent snowball materials, then repair ground contact and HUD/reward composition while preserving touch and chase behavior. Reuse the accepted carrot source, and review at both selector and nose scales.
- **Required states:** face-ready, each placed feature, moving chase, bite/drop, carrot collection, payoff, settle and re-entry. Bind natural launch separately from the configured Castle cutaway.
- **Gate:** every applicable master dimension at least 4.5 in current evidence. Animation cadence, complete action sequence and target-device readability remain unassessed. [Review and rejected-attempt history](carrot_runtime_followup.md).

### 4. Dust Boss / Grand Puff

- **Observed problem:** the registry’s old record is source-bound to revision `775ceee1`; Grand Puff's rebuild is already integrated in the current development base. The old surface record cannot establish the rebuilt encounter's art, medium, or state quality.
- **Repair type:** capture the integrated rebuild and reconcile its actual source/hash and runtime ownership before deciding whether any art repair is required.
- **Candidates:** the integrated boss art; no reuse or regeneration decision may be made from the stale registry.
- **Required Mobile states:** idle/puffy; chase; attack tell; contact/bonk; dizzy/angry progression; payoff/friend; settle/re-entry, with current source revision and renderer recorded.
- **4.5 gates:** DL-MED-01/04/05 compliance; identity across states; stable anatomy/pivot; authored contact and feedback agreement; child-readable tell; scene ownership; family consistency; technical/source hash and no duplicate candidate path.
- **Acceptance gap:** no current score until the integrated encounter's runtime states and exact sources are captured and independently reviewed.

## P1 — observed below-target scene repairs

### 5. PictureGames / Trampoline

- **Observed problem:** current observed runtime score 3.2. Roshan/star read, but the oversized star clips into the HUD/instruction card; trampoline is a broad procedural blue bar; reward overlay obscures the action.
- **Repair type:** composition/layout repair first; replace art only if the trampoline material remains weak after framing.
- **Candidates:** retain existing star and Roshan while testing layout. No approved replacement is identified.
- **Required Mobile states:** ready; bounce contact; mid-bounce; landing/settle; completion/reward with unobscured final action. Natural cadence required.
- **4.5 gates:** star and trampoline contact are obvious; star never collides with HUD; trampoline has authored material/edge treatment; bounce pivot and landing agree; feedback matches contact; phone readability; consistent composition; Mobile performance/import.

### 6. PictureGames / Xmas

- **Observed problem:** current observed runtime score 4.1. Tree and five ornaments are cohesive; final reward card covers the tree center, and there is no clean post-finale tree-only frame. Filename `all_ornaments_no_flower_button` is not evidence of a missing button.
- **Repair type:** evidence/composition capture first; retain art unless a clean runtime view exposes a separate defect.
- **Candidates:** existing tree, five ornaments, and friendship flower remain in place.
- **Required Mobile states:** empty tree; each placement; fifth placement; flower placement/reward sequence; clean finale; settle/re-entry.
- **4.5 gates:** ornament identity and placement contact; no reward occlusion in acceptance frame; cohesive scale/light/outline; completion feedback agrees with fifth/flower action; natural effect cadence; Mobile/phone readability and technical provenance.

### 7. Geologist

- **Observed problem:** isolated brush reuse is strong, but current contact presentation remains open: workbench/context, excavation contact, striped fallback backdrop, pan/geode/fossil materials and scene ownership are not all resolved. Existing score notes separate isolated brush quality from scene quality.
- **Repair type:** composition and action-kit repair; reuse approved brush; generate only named missing props/states.
- **Candidates:** approved `magic_cleaning_brush.png` remains reusable. Rejected checkerboard RGB pan remains out of runtime.
- **Required Mobile states:** idle/workbench; pan contact; excavation; geode/fossil reveal; completion/settle.
- **4.5 gates:** real excavation/contact; coherent cave/workbench material; clean alpha; tool-to-hand anchor; authored reveal states; child-readable target; no fallback stripes; technical Mobile evidence.

### 8. Opera careers with observed baseline under 4.5

These are separate per-career work orders, not one mass replacement:

- **Chef (3.6):** bowl/fill/contact are diagrammatic. Repair actual vessel/pitcher pour and filled/settled states.
- **Detective (4.1):** improve slot contrast and reduce vignette/cursor dominance; capture clue selection, lens reveal, settle.
- **Ballerina (4.0):** replace instrumentation-like ribbon/twirl guides with fabric progression while retaining pose restriction; capture held/action/checkpoint states.
- **Candy Maker (3.4):** create one factory-compatible mold/pour/wrapper family with transparent boundaries; capture each contact/payoff.
- **Stuffie Doctor (3.8):** make patient/contact own the scene over diagnostic widgets; capture scan/wash/bandage/settle.
- **Boxer (4.2):** match glove anticipation/contact/recoil and local telegraphs; capture all three states.
- **Magician (4.1):** enlarge object-specific choices and capture cabinet/reveal states.
- **Painter (3.3):** anchor canvas to easel and show truthful progressive paint coverage.
- **Astronaut (2.8):** replace diagrammatic pipes/grid with coherent pipe/socket/flow/valve kit.
- **Racer (4.1 observed scene):** retain the clearer prior control; improve cockpit/control framing and feedback. The tire-thumb experiment was rejected for semantic failure.
- **Pop Star (3.8):** replace oversized flat pads with painted shell-note pads tied to actual note contact.
- **Nursery (3.1):** clarify baby/cradle ownership and authored catch/contact/settle states.
- **Teacher (3.5):** improve the worksheet-like board material, framing and pointer target while preserving the exact, uncluttered circles, triangles, numerals and counts that make the lesson mathematically readable. Do not replace those semantic shapes with decorative shells. Repair jumping pointer poses through stable target staging.

Each Opera item requires exact career route captures for idle, anticipation, active contact, payoff, settle, and retry/re-entry, plus independent Sol/Luna review. Existing baseline numbers are historical observations and cannot be treated as acceptance.

## P2 — unscored families requiring evidence before repair decisions

Do not commission or score these from filenames, source comments, or historical area scores:

- Dolls
- Melody
- SlideRace runtime framing
- Bathroom Cleanup composition
- Fairy runtime staging
- Fetch
- Treasure
- Shop
- Brawl imp animation
- DanceEngine procedural surface
- SideScroll modes
- inactive `k_*`, cat, and bird assets
- Day One pool cleanup satellites: initial current diagnostic review now exists; the [Pool follow-up](pool_runtime_followup.md) identifies below-target contact, clipped/rectangular waterfall staging and finale occlusion. Full animation/device evidence remains open.
- current Grand Puff source after dev reconciliation
- catalog-driven Opera adapters and indirect asset families

Required first step is a current Mobile capture packet binding exact assets and states. At minimum capture ready/idle, active contact, changed state, payoff, settle/re-entry, and any required animation loop. Dynamic/catalog paths, AtlasTexture subframes, and concatenated resource paths must be recorded individually.

## Minimal acceptance sequence

1. Freeze exact caller, source hash, touch/display rect, anchor, and failing state.
2. Apply layout/routing fixes before art generation.
3. Sol/Luna independently inspect candidate isolated art and reject contaminated or semantically wrong reuse.
4. Import and capture current Mobile runtime states at 1280×720 plus phone ratio with natural processing cadence.
5. Reaudit all eight dimensions per item; one failed dimension keeps the item open.
6. Run focused gameplay/provenance/technical gates and then the full repository gate. Keep rejected candidates and provenance outside runtime.
7. Refresh the dependency inventory after each batch; no game-wide completion claim is valid while P2 families remain uncaptured.

Watering-can attempt03 used built-in ImageGen for the single requested background-extraction correction. It again returned 1254×1254 RGB with a painted checkerboard, despite a genuine RGBA/1024×1024 request. Native candidate, exact prompt and rejection provenance are preserved in assets_src/minigame_art_quality_2026-09-05/watering-can-attempt03/. No runtime asset was replaced. Do not spend another generation on the same ineffective extraction prompt. The requested non-destructive Python cleanup is still awaiting explicit user authorization; acceptance would additionally require clean exterior and handle-hole alpha, preserved contour/material, runtime size compliance and contact-state review.

## Reuse discovery after the family-evening source review

Sol's bounded eight-file reuse search found the approved painted carrot at `assets/opera/worlds/widgets/widget_target_farmer_piece_0.png` (256×256 RGBA; SHA-256 `9ec02fdd3e0ea6888ab3e3dce7f3a6436b752974798fd46fddf545a70f3e93dd`; existing license at ASSET_LICENSES.md). Parent visually confirmed its leafy silhouette and painted orange volume. The current candidate binds these exact unchanged bytes in Comfy dinner and both Snowman carrot roles. The nose keeps its existing center/bounds/collection anchor and rotates -135 degrees to face outward. Runtime captures and independent review remain mandatory; this does not certify the full Snowman scene or its animation. The earlier no-reuse finding is superseded for carrot only.

No inspected asset truthfully supplies an isolated painted open soup pot. The polished single-spout gold kettle, popcorn bowl, full kitchen crop and flat Blender QA pot do not fill that role. Preserve all originals and generate only the missing pot if needed; do not rename a kettle or bowl to pass a semantic gate.

## Snowfield generation follow-up — 6 September

The [six-candidate reuse inventory](snowman_scene_reuse.json) found no complete suitable native playfield. One built-in ImageGen candidate was generated using the protected book scene as a style/setting reference only; no protected original was modified. Its native output is 1672x941 RGB, so it fails the requested native coverage. [Independent source review](snowfield_attempt01_review.json) also rates readability 3.9 and contact 4.0: dense caustics make the snowy ground read as shallow water and may lose the plain white Snowman silhouette. Painted finish 4.5 does not override these failures. The exact candidate and prompt remain under `assets_src/minigame_art_quality_2026-09-05/snowfield-attempt01/`, outside runtime. No enlargement or pixel cleanup was performed.

A next candidate must quiet the caustic network into broad blue/lavender snow bands, strengthen contact contrast for white snowballs, preserve the clear lane/right-distance cottage, and originate at the required native size. Repeating the same limited-resolution request is not an accepted repair.
