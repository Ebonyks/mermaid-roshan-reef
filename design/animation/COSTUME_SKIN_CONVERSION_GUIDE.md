# Convert existing costumes into reusable Roshan skins

Owner commission: 2026-11-01. This is the source-authoring recipe for the owner's one-character skin direction. The version 1 exchange format is a **proposed candidate**, not a shipped loader or an accepted Roshan rig. The [master planning entry](../../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry), [design rules](../06_COMPREHENSIVE_DESIGN_LANGUAGE.md), [production protocol](ANIMATION_PRODUCTION_PROTOCOL.md) and [ledger](../05_DOC_LEDGER.md) retain precedence. No production, finding, device, child, owner or release acceptance is supplied by this guide.

The output is garment artwork plus binding data for the existing character. It is not a new complete costumed character, skeleton, anatomy texture or animation controller. The [architecture workflow](../../assets_src/animation/laura_swim_costumes_20261101/SKIN_BINDING_WORKFLOW.md) explains the separation; this guide makes costume conversion repeatable.

## Choose the conversion lane

| Existing costume | Conversion | Reuse target |
|---|---|---|
| Same silhouette, different material/color/detail | Replace garment texture; keep the template geometry, UV, weights and joints | Existing bound garment template |
| New garment silhouette, same supported view | Isolate and register the garment; make a garment-only mesh; transfer/correct weights | Same canonical skeleton, anatomy and animation library |
| Missing profile/quarter view or unseen anatomical surface | Record the gap. The rig owner supplies the common Roshan view/pose once; then make only that garment's matching view | Shared view library and versioned binding contract |
| Whole costumed portrait or full-character sheet | Extract the clothing non-destructively; discard its face/body/hair pixels from garment delivery | Existing approved character master |
| Per-costume Godot project/character script | Salvage suitable garment images and attachment geometry; translate them into the shared data format | One character implementation, no per-outfit builder |

A new outfit should normally add artwork, a recipe and a skin data file. Character, skeleton and animation code should not change. A genuine shared-rig defect gets one central version change and explicit migrations, not a costume-specific workaround.

### Translate the existing studies

| Existing field or artifact | Destination |
|---|---|
| Per-family bones/rest and anatomy setup | Select the common master once; pin its skeleton/identity files in the rig contract. Do not copy these into each skin. |
| Costume body/tail/head/sleeve RGBA images | Garment texture references on the corresponding semantic slot/view, after garment-only review and registration |
| Garment polygon points | Mesh vertices in canonical canvas pixels; the canonical Body mesh remains unchanged |
| Existing polygon UV | Mesh UV in texture pixels; if the old code used polygon points as UV, declare that mapping explicitly and adjust for any image trim |
| Polygon triangles and per-bone arrays | Mesh triangles and weights; validate counts, known bones and normalized sums. Reuse the canonical template where equivalent. |
| Hard-coded per-outfit texture/material selection | Skin attachment/coverage data interpreted by the shared renderer |
| Per-family draw-order numbers | Canonical slot/view layer definitions, with front/back garment pieces where necessary |
| Per-costume animation or character constructor | Shared action/character implementation; do not include it in the skin package |
| Tool image and grip coordinates | Separate equipment attachment on a verified common socket, not a second costumed character |
| Whole-figure preview or sprite-loop master | Diagnostic/export evidence; retain editable garment parts as the authoring source |

Do not rename an old complete Body mesh or figure texture to “garment” and treat that as conversion. Its ownership and visible output must actually meet the garment-only contract. The source studies' visible/structural failures remain named repair work.

## Required input packet

Before conversion, record the exact costume source paths/SHA-256, rights, acceptance/rejection scope and existing editable masters. Inventory suitable painted pieces before generating anything. Old rejected output may be diagnostic input; it does not become approved by extraction.

The intended native Godot implementation uses a Canvas Skeleton2D/Bone2D hierarchy, Polygon2D garment meshes and rigid Node2D socket attachments. The skin package is the costume art/data consumed by that shared 2D character.

The rig owner must provide one verified binding contract containing:

- Rig ID/version and pinned canonical skeleton file, including its hierarchy/rest information.
- Immutable identity/anatomy asset hashes, approved source scale and pivots.
- Supported views, their canvas dimensions, semantic slots, required/optional status, permitted binding modes and draw order.
- Named bone/socket definitions and verified hand-contact offsets.
- Reusable garment mesh templates and their hashes; named neck/cuff/waist/fin interfaces where relevant.

Use an actual supplied contract. Do not invent a production-approved rig, copy bone names into a new character, or silently fall back to another view. There is currently no accepted data-only live-actor implementation from the swimming comparison; its one 14-bone definition is useful input, not final rig authority.

## Convert a costume

### 1. Make a part map

Map the visible clothing to semantic slots such as headwear_back, body_back, tail_cover, sleeve_left, sleeve_right, body_front and headwear_front. Use the actual contract's names. A sleeve-less look legitimately leaves optional sleeve slots null; it does not create replacement arms. A coat may require back/front pieces around the arms. Gloves use canonical hand-pose/view variants.

Write a small conversion record: source → isolated part → target view/slot → template or custom mesh → unresolved gap. This prevents repeated source discovery and makes another artist's handoff executable.

### 2. Isolate garment-only RGBA art

Use existing masters or irregular cutouts, preserving painted antialiasing and contours. Remove scene/background, anatomy, old clothing, face and hair from garment delivery. Do not constrain a new dress to the previous outfit's alpha. The shared base is clothes-erased in replaced regions; an outfit must not leave the old blouse or tail garment beneath it.

Use Aseprite with named garment layers and hidden registration guides. Keep the approved character reference separate. When art is truly missing, request only the named garment surface/view/joint repair, with the canonical template as registration/style reference. Do not regenerate complete costumed Roshans. Follow the existing job-card, attempt/time/cost and protected-original rules.

Whole-figure Aseprite loops and videos are useful QA exports, not the skin-authoring master. Preserve editable garment layers and binding data separately.

### 3. Register to the canonical view

Match the source canvas, scale, origin and approved neutral pose. Align neckline, shoulder, elbow/cuff, waist and fin-junction landmarks that the garment uses. Record the transform and any matte/local paint cleanup. Never resize Roshan's head/body or move the skeleton to make a costume fit.

Weighted mesh positions use **canonical canvas pixels**. UV coordinates use **pixels in the referenced garment texture**. A trimmed image therefore needs the corresponding UV/origin adjustment; trimming cannot silently change registration. Rigid parts use a named socket, texture pivot, socket-local offset, rotation in degrees and positive uniform scale.

Runtime garment textures must satisfy the existing ≤1024-longest-side or power-of-two rule. Keep higher-resolution source masters separately. Preserve originals; do not destructively shrink them.

### 4. Reuse or author the binding

For a matching silhouette, reference the rig's existing template by ID and exact file hash. Do not duplicate or repaint its weights. This is the fastest conversion lane.

For a new silhouette, author a garment-only Polygon2D mesh in the same space. Add internal vertices where shoulders, elbows, waist or cloth bends need support. Initial weights may be transferred from the registered canonical deformation field: within a known triangle, interpolate its three vertices' bone weights using barycentric coordinates, then normalize. Outside that domain, use an appropriate approved garment template or deliberate manual binding; do not guess the nearest bone and declare it finished.

Correct seams and deformation in the shared action poses. Keep each vertex's weights finite, nonnegative and normalized. Only canonical bone names are allowed. Hat/tool parts are generally rigid socket attachments; cloth that crosses joints needs weighted geometry. A skin cannot add bones or override the anatomical Body mesh.

### 5. Resolve joins, layering and views

At mixable neck, cuff, waist and fin interfaces, verify compatible boundary positions, deformation weights and coverage. Mesh seam maps name the canonical interface and ordered vertex indices. A valid index list is not proof that two pieces actually meet; inspect/measurably test their deformed boundaries.

Use the contract's draw order and front/back pieces for changing occlusion. Hands must remain visible and supported at real grips. A bone origin is not automatically a hand-contact socket. Leave unsupported views/combinations unexposed until they have real artwork and compatible bindings; no stretched frontal face or unreviewed mirror fallback.

## Package the binding data

The local schemas define the candidate interchange format:

- [Rig binding schema](skin_binding/rig_binding.schema.json): shared authority, skeleton/identity pins, views, slots, sockets and templates.
- [Skin package schema](skin_binding/skin_package.schema.json): costume ID, exact rig pin, attachments, explicit per-view slot coverage and derivation.
- [Garment mesh schema](skin_binding/attachment_mesh.schema.json): canonical positions, texture UV, triangles, normalized bone weights and optional seam indices.
- [Recipe template](skin_binding/skin.recipe.template.json): author-facing input to the packaging helper. Its placeholders are deliberately **not** a usable or accepted costume.

Version 1 packages rigid or weighted parts for declared views and slots. Pose-specific glove drawings, animated material variants or other attachment-state selectors need an explicit shared rig/format capability and migration if the existing common slot states cannot express them. Record that gap rather than inventing a costume-specific controller or claiming the initial format already implements every action variant.

All referenced asset paths are repository-relative POSIX paths. Hash actual file bytes. No absolute paths, parent traversal, scripts, skeleton instances, character scenes, animator definitions or per-costume shader code belong in a skin package. Material/visibility choices must use the shared renderer's declared data contract.

Save new binding JSON as UTF-8 with LF line endings before calculating hashes. At publication, compare referenced working-file bytes with the actual staged Git blobs, then verify the immutable remote bytes. If text normalization changed a JSON contract/template, normalize it deliberately and rebuild dependent hashes. Alternatively preserve the source package's exact bytes with its documented local .gitattributes policy. A successful local parse is not proof that published file hashes still match.

A typical source package contains skin.recipe.json, the generated skin.json, garment RGBA files or shared references, any new garment meshes, an editable Aseprite master, derivation records and scoped evidence. Shared geometry stays shared through a template reference. Do not precompose every head/body/tail combination or duplicate anatomy for each look.

Keep existing Fashion Designer look IDs and head/body/tail selection IDs in the shared catalog mapping. A new skin version changes the referenced art/binding package, not saved unlock or selection keys. Keep availability/unlock rules separate from binding data. Future integration preserves existing save keys and unknown fields, adds defaults where needed, and checks save/load and original-outfit restoration under DL-SAVE-01 and DL-SAVE-04.

### Repeatable preparation and checks

After replacing the template placeholders with real, reviewed assets and supplied bindings, run from the repository root:

```text
python -B tools/prepare_costume_skin.py --root . --rig assets_src/animation/shared_roshan_rig/rig_binding.json --recipe assets_src/animation/skins/chef_v1/skin.recipe.json --out assets_src/animation/skins/chef_v1/skin.json
python -B tools/validate_costume_skin.py --root . --rig assets_src/animation/shared_roshan_rig/rig_binding.json --skin assets_src/animation/skins/chef_v1/skin.json --report assets_src/animation/skins/chef_v1/evidence/format_validation.json
python -B -m unittest tools.tests.test_costume_skin_binding
```

The example rig/package paths above describe the intended directory layout; they do not claim those real character bindings already exist. Supply the verified current paths. The preparation helper refuses an existing output and writes only after successful format/binding validation. It fills hashes and template references, not missing artwork or weights. Re-run with a new versioned output after changes.

For example, a Chef tunic that already matches a supplied tunic_front_v1 template needs its isolated PNG, that template ID, its slot/view coverage and source/edit record. A different apron outline needs an explicitly authored garment mesh instead. Neither recipe needs a Chef character script or a copy of Roshan's skeleton. Record source acceptance_scope on every source: approved appearance-only, provisional or rejected-reference scope cannot disappear during conversion.

The validator checks code-free fields, exact rig/assets, known views/slots/sockets/bones, explicit required/optional coverage, RGBA/size requirements, mesh/UV/triangle integrity, normalized weights and exact shared-template references. It requires a pinned canonical skeleton and identity assets. It does **not** detect whether a PNG secretly contains a face, prove registration/seam closure, establish natural motion/contact, or verify a live runtime. Those remain the next evidence lane. Its report always keeps production acceptance false.

## Acceptance criteria carried into the master audit

| Criterion | Required evidence |
|---|---|
| Source/art ownership | Original hashes/rights and modifications; isolated garment-only pixel review; protected anatomy unchanged |
| Data-only conversion | Valid candidate format; no per-outfit actor, bones/rest override, alternate anatomy or animation code |
| Reuse/fit | Registered landmarks; shared template where appropriate; garment-only custom geometry where necessary; named compatible interfaces |
| Animation/outline | Full affected actions, views, extremes, entries/exits and loop seams at normal speed and frame step; actual per-material masks; original-clothing leakage controls; unchanged applicable geometry/motion floors |
| One live character | Two skins switch mid-swim and during arm/tail extremes; actor/skeleton/bone/animator IDs, anatomy hashes, animation phase, location and scale remain invariant |
| Equipment/contact | Correct socket/pivot, near/far layering, gripping/support/release where an action uses an object |
| Swap lifecycle | Atomic replacement; exact original restoration; invalid data rejected before changes; pause/resume/re-entry; no node/material/texture growth |
| Wardrobe/save compatibility | Existing look/slot IDs, unlocks and selections survive save/load; package version changes do not rename saved choices; no save key is removed |
| Complete wardrobe | Every exposed complete look and mixed slot combination passes its relevant fit/outline/view checks |
| Mobile/acceptance | Exact 4.7.2-stable Mobile evidence, target-device memory/30 fps/overdraw, and separate human/child/owner gates; no inference that a schema pass accepts them |
| Development record | New/updated impact, asset licenses, current master/ledger links, required gates and durable verified delivery for external handoffs |

Begin with two representative existing outfits on one actor. Only after that architecture proof passes should the rest of the studies be batch-converted. A comparison can show many instances of the same character implementation with different skins; independent character builders are not the reusable system.

## Repair and reuse loop

| Observed problem | Repair owner |
|---|---|
| Strain/tearing only in one sleeve/hem | That garment's topology/weights or missing paint; retain common anatomy |
| Old outfit visible | Garment ownership/base cleaning or shared slot replacement, not a sticker hiding the old clothes |
| Common anatomical/joint defect across looks | Shared master/rig version, then migrate/revalidate affected skins |
| Waist/cuff mismatch between pieces | Shared interface plus offending garment boundary; retest exposed combinations |
| Profile/perspective mismatch | Common view/pose if absent; otherwise that garment's registered view |
| Wrong hand/tool contact | Shared socket/hand-pose contract or prop pivot/occlusion binding |
| Outfit requires editing character code | Missing generic slot/format capability, or an invalid costume-specific fork |

Cache conversion work by source hash + rig contract hash + template/view ID. A source or binding change invalidates only affected garment outputs and their evidence; a common rig/identity/interface change invalidates all dependent skins. Record real generation calls, registration/cleanup time, manual binding time, failed attempts and validation time. This measures the efficiency gain without invented per-costume speed claims.

Adding a new costume should ultimately be a repeatable art/data conversion. The guide and checker make that boundary explicit; the reusable live skin loader and its measured two-costume proof are still required.
