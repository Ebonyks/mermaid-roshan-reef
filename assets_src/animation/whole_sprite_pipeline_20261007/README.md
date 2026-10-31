# Reusable whole-sprite engine: pink-wave fixture

Status: `PROPOSED / CANDIDATE`, 2026-10-07; baseline
`92c9fe70319ef46bfaa8f61348a6f51512141ec3`. The owner directs an adaptation format
and engine above the fit of a single image. Pink outfit first; this is a test
fixture for the [reusable pipeline](../../../docs/animation/WHOLE_SPRITE_PIPELINE_V1.md),
building on the [W1–W6 wave handoff](../../../docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/README.md).

[catalog.json](catalog.json) separates character identity, outfit motifs, action
timing and concrete frame jobs. Add another named outfit/action and its pinned
art/frames to adapt through the same CLI. No image-specific fitting script or
new runtime wardrobe logic is needed for another preparation job.

The current clothing already appears as one composed texture at runtime;
`FashionParts.composed_path` flattens head/body/tail selections. This engine
does not alter that implementation or waive the owner's whole-drawing rule.
Authoring from separately warped limbs remains rejected even if later flattened.

## Actual source review

- Approved K0 and K2 references are exact complete-cell Aseprite crops from
  the unchanged gesture atlas. [source_inventory.json](source_inventory.json)
  records source path/hash, crop and acceptance scope.
- `native_context/` contains byte-identical copies of all 41 rejected Union
  take-1 native frames. The rejected study cannot be a generator appearance
  input. [source_frames.json](source_frames.json) pins every frame and ancestor.
- [frame_review.json](frame_review.json) records static diagnostic observations
  on all 41 frames. Pink sleeves/bodice, V waist trim, rainbow hair/fin and tiara
  motifs remain recognizable. Frames4–33 fail hand silhouette/detail review:
  raising4–11, raised12–23 and lowering24–33. These are continuous candidate
  repair spans, not permission for 30 independent still generations.
- [inspection.json](inspection.json) measures figure scale about0.114% and head
  scale about0.338% peak-to-peak. One pinned master layer passes. Native alpha,
  boundaries, missing arm annotations and incomplete human motion review block
  readiness. The native video does not have exact K0 cells at0/40.
- [aseprite_review/export_report.json](aseprite_review/export_report.json) proves
  all41 source/export RGBA frames are identical after save/reopen, on one layer,
  with phase tags and the1708ms clock. This preserves rejected pixels honestly;
  it is not a repair or art acceptance.

## Sparse corrective requests

[repair_plan.json](repair_plan.json) prepares one whole raising key at7 and one
whole lowering key at27. Both bind approved K0 identity/outfit and K2's
full-length arm reference. K0 governs head size. Bad K1/K3 guide proportions,
diagnostic boards and the rejected video are excluded from image bindings.

[attempts.json](attempts.json) is the shared action budget: at most two built-in
ImageGen calls, no new transformer takes or paid API jobs in this corrective
brief. Reservations are mandatory before calls; failures and rejects count.
Generated keys remain candidates until exact native/normalized geometry and
identity/topology/outfit review. None is silently substituted into runtime.

The local Union recipe is a retained next-stage reference, not newly executed
or automatically parameterized here. Corrected keys and measured structural
guides are required before requesting another temporal animation take.

## Evidence and remaining claims

The pipeline implementation and its failure tests are separate from visual
quality. The frozen native fixture correctly remains `REVIEW_BLOCKED`.
Full-speed transitions, corrected W3 joints, final alpha/entry/exit, Godot
sampling, actual device performance, child and owner review remain pending.
`MA-ROSHAN-003/005/006` lifecycles and game-wide `UNSATISFIED` are unchanged.

`ARCHIVE_COMPLETE` requires the published-revision verification receipt.
`GENERATION_READY` for final animation and `DELIVERY_ACCEPTED` are not granted
by source crops, a prepared key request, a one-layer export or passing tests.
See the [job card](JOB_CARD.md) and
[audit impact](../../../design/audit_impacts/whole-sprite-pipeline-20261007.json).

Two built-in key calls tested the reservation/receipt path. Both native1254×1254 outputs and exact prompts are preserved in `keys/`. Aseprite normalizes each whole square canvas uniformly to256×256 in a one-layer master. No crop, reposition, limb edit or guide pixels are applied. The first output contains detached matte flecks; both normalized samples fail border/framing and cannot establish calibrated tracking against K0. Both are rejected as production guides, the two-call cap is exhausted, and no video take is launched. This negative result tests the engine's gating rather than accepting a single-image fit. See `key_inspection.json`, `catalog_generation_revision_1.json` and `repair_plan_after_cap.json`.

The four [diagnostic boards](diagnostic_boards/provenance.json) cover every native frame. They are review layouts, excluded from generator bindings and delivery pixels. The [packet manifest](packet_manifest.json) pins this source archive and reusable code dependencies. Publication/access evidence is recorded separately.

The four [diagnostic boards](diagnostic_boards/provenance.json) cover every native frame. They are review layouts, excluded from generator bindings and delivery pixels. The [packet manifest](packet_manifest.json) pins this source archive and reusable code dependencies. Publication/access evidence is recorded separately.
