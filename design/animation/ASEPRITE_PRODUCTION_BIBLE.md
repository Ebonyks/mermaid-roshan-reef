# Faithful Aseprite production bible

Status: `BINDING_DOMAIN` under `DL-MOT-10` through `DL-MOT-13` and `DL-CIN-15`.
Owner decision 2026-09-15: extend the approved Grand Puff workflow to all
characters and gameplay assets **when the task dictates it**. Read the
[production protocol](ANIMATION_PRODUCTION_PROTOCOL.md) and
[operational exception](../../AGENTS.md#character-and-gameplay-video-cel-exception-owner-decision-2026-09-15).

## Why the Puff benchmark worked

The commissioned moving source supplied expressive poses, rhythm, squash,
secondary motion and transitions. Faithful cel transfer preserved that acting
instead of approximating it with a few still parts. Aseprite made the entire
performance editable; it did not invent the performance. The owner praised the
three-clip benchmark at `978a79d5127beafdf543a2640d58ddb69e55b909`.
See the [Puff profile](GRAND_PUFF_MOVEMENT_PROFILE.md) for exact sources and limits.
The later five-clip batch contains review and repair drafts, not five additional
accepted exemplars. More handoffs or more frames alone do not establish quality.

## Production sequence

1. **Inventory before production.** Find the approved identity, actual action
   contract, existing art and chronological footage. Reuse suitable approved
   assets. Name the missing motion or repair; do not redesign for novelty.
2. **Choose a convincing performance.** Inspect actual playback and dense
   contact sheets, including starts, exits and peak deformation. Review anatomy,
   silhouette, intention, contact and identity against approved references.
   Source-review prose is evidence to check, not proof. For new commissions,
   prefer one clear action, fixed framing, full silhouette clearance and a
   separable background. Record source defects before conversion.
3. **Preserve the acting.** Decode chronological source frames at native timing.
   Keep a constant recorded canvas transform. Avoid per-frame fitting, arbitrary
   downsampling, interpolated poses and duplicate frames concealing missing
   action. Document source-frame selections and intentional holds explicitly.
4. **Isolate for the subject.** Extraction, tracing, raster redrawing and local
   cleanup are permitted. Inspect hair, translucent fins, pearls, holes, contact
   edges and embedded effects. Puff's purple mask cannot be assumed correct for
   Roshan. Flattened footage cannot recover original alpha exactly. Preserve
   source masters and keep repairs on separate editable layers where possible.
5. **Build editable native files.** Retain individual cels, action tags, timing,
   a source reference and cleanup layers. Record source commit/path/hash, frame
   index/time, masks, transforms, derived RGBA hashes and duration. Identify
   automated pixel transfer honestly; never label it a hand redraw. Record any
   raster repairs separately from exact transferred pixels.
6. **Verify the saved result.** Reopen native files and compare every cel's RGBA
   and duration against recorded derived inputs. Review source/native playback,
   dense boards and intended gameplay scale. Byte equality proves transfer
   fidelity, not visual quality. If splitting large native files, retain global
   source indices and continuous timing and verify every split cel again.
7. **Review before integration.** Publish versioned review sources, native files,
   previews, provenance and licenses. Record accepted spans and unresolved issues
   precisely. Keep full quality masters; optimize runtime exports only after
   performance review, with target-device memory/overdraw/frame-time evidence.

## Acceptance and boundaries

Method approval is project-wide within the stated scope. It is not automatic
acceptance of anatomy, colour, alpha, acting, loops or gameplay behavior. Keep
source review, machine verification, owner visual review, runtime verification,
device and child acceptance distinct. Expressive closed eyes can be intentional;
repair defects without flattening the personality that made the source useful.

Preserve protected originals. Review output uses new non-runtime paths. This
commission does not automatically replace live renderers or endings. Gameplay
continues to own navigation, contact validation and saved progress; clip endings
never award progress by themselves. Complete cinematic scene delivery retains
its full-frame contract. No new 3D assets, automatic release or wholesale art
regeneration follows from this workflow.

Track production in the [source queue](../../audit/animation/PROJECT_ASEPRITE_PRODUCTION_QUEUE.json).
It is a starting inventory, not exhaustive completion or acceptance evidence.
