# Roshan size and focus repair analysis — 2026-10-04

**REJECTED_REFERENCE_ONLY.** The owner still sees size changes and fluctuating
focus. Global registration is improved, but the drawing changes internally.
The two-step decoder experiment below is rejected. No new transformer take,
ImageGen call, adapter download, runtime integration or artwork acceptance is
claimed. GitHub publication and machine checks do not grant creative acceptance.

## Owner correction

The owner reports that the problem is still present, although subtle, and that
the figure shifts in and out of focus. The owner permits regeneration through
a different workflow to correct these errors. Earlier directions remain:
constant world size, coordinated whole-figure motion, and Aseprite as the bridge
for multiple anatomical anchors and frame repair. This does not approve the
existing footage, a replacement design or a partial-limb repair.

This is a new corrective brief after the five-take study and zero-generation
scale-filter correction. Their costs and rejected results remain recorded.
See [prospective job](corrective_job.json) for new limits; it is not a queued job.

## What is still wrong

The [v2 registration](../ltx25_scale_filter_v2_20261004/README.md) fixes the
deterministic bypass and coarse scale steps. All 41 frames meet its global
root/scale tolerances. That fit uses five upper-body landmarks; it does not prove
a stable head-to-torso ratio, shoulder width, pelvis or tail junction. Internal
geometry fails at 12–15 and 22–24. Scaling the complete frame again cannot make
those proportions agree without changing already-correct parts.

The native model PNGs already change in detail before Aseprite or MP4 encoding.
This resembles changing focus, but the test does not establish optical lens
defocus. Generative loss/reconstruction of facial and contour detail is another
explanation. The guides also mix enlarged 256-pixel art with one much larger
new redraw. The measured detail mismatch is a plausible contributor, not an
isolated causal proof. Sparse soft keys, temporal compression, changing poses
and resampling can contribute simultaneously.

[Focus metrics](focus_metrics.json) measure an unchanged face-region rectangle
and empty-background region without making resized/cropped review images.
They are diagnostics: pose, painted values, slight motion and edge content
confound them. Native face Laplacian variance ranges 51.57–726.44; registered
v2 ranges 48.48–531.77. The higher-resolution key 22 measures about 1202 in the
same guide region, versus about 112–124 in the older keys. These are edge-energy
measurements, not a claim that key 22 is ten times sharper or that a metric can
accept the artwork.

## Controlled decoder test

The fifth take's saved refined latent was decoded twice with the same matched
LTX-2.5 CausalDiffusionVAE, tile settings and decoder RNG. Publisher default:
one timestep `[1.0]`. Experimental setting: `[1.0, 0.5]`. This is not DFR, Refine
Details or an omitted required diffusion pass. The temporary decoder setting
was restored in `finally`; no pinned vendor code or model weights were edited.

All 41 default re-decodes reproduce the original source pixels exactly. The
experiment took 38.51 seconds; sampled total-card peak was 4229 MiB. Actual
decode times were 10.39 seconds for one step and 16.61 seconds for two.
[Receipt](receipt.json), [one-step proof](decoder_1_proof.json),
[two-step proof](decoder_2_proof.json) and [workflow](workflow.api.json) preserve
execution evidence. Sampling memory every three seconds is not an instantaneous
hardware maximum.

**Reject the two-step setting.** Native review at indices 14, 22 and 40 finds
added grain/checker texture, persistent soft contours/face and torn fingers.
Empty-background median Laplacian variance rises from 1.23 to 91.49. The higher
face edge score partly rewards that noise; it does not prove recovered painted
detail. Internal shape drift remains in the same latent.

The [comparison video](decoder_1_vs_2.mp4) shows **native default left,
experimental two-step right**, on identical timeline indices, at 1:1 column
dimensions. It does not compare registered v2 against raw output. All 41 new
native PNGs and the [editable Aseprite master](decoder_2_review.aseprite) are
retained; failures are not replaced with holds. Aseprite performs comparison
assembly and master export. MP4 is a lossy viewing copy.

## Preferred corrective workflow

1. **Make one coherent whole-figure guide sequence in Aseprite.** Use the
   established design at a consistent detail level. Establish pose-aware crown,
   eye, neck, shoulder, waist/pelvis and tail-junction relationships, fixed world
   size and root. Repaint geometry-failing spans with clean entry/exit context;
   shoulder, torso/dress, hair and tail must respond to the action. Correct the
   loop seam and clipped hand at source. Do not edge-extract the flawed model
   footage and call it a corrected guide. Guides and metadata are separate from
   accepted final pixels.
2. **Regenerate with structural video conditioning on LTX-2.5.** The official
   [2.5 Union Control workflow](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/3bf3ca62595f1764c47d01c35c8e5dfe47e1a88f/example_workflows/2.5/LTX-2.5_ICLoRA_Union_Control_Distilled.json)
   loads the [2.3-trained Union adapter](https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control)
   on a 2.5 distilled transformer. This keeps the 2.5 engine. Union supports
   Canny, depth and pose; Canny is our first candidate because a mermaid's
   silhouette, tail and cloth are poorly represented by a human pose skeleton.
   That choice is an inference, not a successful Roshan test. Bind the actual
   aligned structural video and approved identity/style reference, rather than
   relying on a few soft pose keys. Control remains probabilistic.
3. **Only after geometry passes, reconstruct detail temporally.** Official
   [Refine Details](https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Refine-Details)
   uses aligned video conditioning to reconstruct fine detail while retaining
   input geometry, with an optional identity reference. It therefore cannot be
   trusted to repair breathing proportions in a defective input. Its joint
   sequence/tile processing is a better candidate for changing sharpness than
   independent still sharpening. Preserve painted bands/contours; do not import
   photographic grain or prompts that reject painting.
4. **Reopen/export in Aseprite and review all native frames.** Verify root,
   global size and internal proportions separately. Review facial detail in
   quiet regions, fingers, all moving contours, background noise and both loop
   boundaries. Also inspect at intended 256-pixel delivery size and full speed.
   Metrics and export checks do not override visible size/focus errors.

This route addresses the two defects in order: structure, then consistent
detail. It is the preferred next experiment, not a demonstrated production fix.

## Local feasibility and alternatives

| Method | Evidence and suitability | Decision |
|---|---|---|
| Union Control on installed 2.5 | Official 2.5 graph; public 654,465,352-byte adapter. Base W4A8 already ran on this 8 GB card; LoRA patches, guide/context memory and quality are untested. | First structural trial after corrected Aseprite guides and quantized-loader preflight. |
| Refine Details | 1,308,787,534-byte adapter; aligned temporal detail reconstruction. Its separate access gate remains pending. 8 GB execution untested. | Follow geometry acceptance; no automatic gate consent inferred. |
| Low-denoise video-to-video | Strong source preservation can also preserve the original shape errors. | Alternative for an already-correct guide, not a proven correction. |
| Complete DFR | Official pipeline generates keyframes and details the sequence; key-aware decoding needs matching checkpoint support. Current Comfy/W4A8/8 GB route is unverified. | Later fallback; extra ordinary decode steps are not DFR. |
| Deblur adapter | [Official card](https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Deblur/blob/7d0cf41dcc6c93d763346e17f76d5f8d64d0e2ff/README.md) excludes motion blur and targets spatial defocus. | Do not use it as a torn-hand/motion-smear fix. |
| Two-step decoder | Actual same-latent test adds grain and retains defects. | Rejected; retain publisher default. |
| Per-frame sharpen/upscale or more free I2V | Can amplify noise and retain temporal inconsistencies; no structural constraint. | Not the preferred next spend. |
| Authored whole-figure 2D cels | Exact drawn proportions and contours; more drawing work and temporal review. | Reliable structural authority/fallback if controlled regeneration fails; no frozen-body limb workaround. |

Do not revive a Roshan 3D rig for Layout-to-Render or use archival Restore as
the first route for clean painted sprites. Their input/task domains differ.
At CFG 1 ordinary negatives are inactive; a prompt is not a blur-disable switch.
The previously executed NAG test already showed active negative guidance does
not guarantee correct fingers.

The candidate Union geometry is **640×896 output**, padding the existing
576×832 canvas by 32 pixels per side, with a **320×448 first pass** and legal
**160×224 half-size control guide**. All are multiples of 32. These are a
proposal; confirm the exact nodes/guide scaling before submission. No resize
or subject warp is implied by padding. Test LoRA loading on the quantized model
and a short legal clip before spending a full take; include failures in the cap.

For a native 576×832 detail input, whole-canvas padding to **576×1024** matches
the published portrait tile without upscaling to 4K. The card warns of reduced
detail in its final 1–2 frames; optional eight context frames beyond the delivered
action would give 49 input frames and 41 delivered frames, with explicit mapping.
They cannot conceal a failed action or insert undocumented holds. See the
[official refine guide](https://docs.ltx.io/open-source-model/vfx-post-production/refine-and-restore)
and [DFR documentation](https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-pipelines/docs/pipelines.md).

[Method preflight](method_preflight.json) pins upstream graph/adapter revisions,
public/gated status and Union hash/size. No weight files are redistributed.
The new brief permits one saved-latent ablation, at most two transformer takes,
zero ImageGen calls, at most 1.3 GiB of adapter downloads and 20 minutes per
transformer take. A decoder success does not establish adapter VRAM fit.
The two adapters together require about 1.83 GiB, exceeding this initial download
cap. This brief prioritizes Union; a later detail pass needs a recorded budget
extension/new bounded brief. A short transformer preflight counts as a take,
so two takes do not silently authorize a short test plus both full stages.

## Evidence and acceptance

[Verification](verification.json) covers native dimensions, exact default
parity evidence, all 41 Aseprite pixel/timing roundtrips and 82 comparison
columns, plus 41-frame/24-fps video metadata. [Manifest](manifest.json) binds
payload and declared source hashes; [remote receipt](remote_verification.json)
records anonymous immutable GitHub access after publication. The
[impact](../../../design/audit_impacts/ltx25-focus-repair-20261004.json) covers
the protocol/ledger/planning updates. Native visual review remains rejected;
runtime, device, child and owner acceptance are outstanding. MA-ROSHAN-003,
MA-ROSHAN-005 and MA-ROSHAN-006 lifecycles are unchanged.
