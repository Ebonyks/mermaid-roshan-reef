# Roshan Union structural-control trial — 2026-10-04

**EXECUTION_PASS / REJECTED_REFERENCE_ONLY.** Two actual LTX-2.5 Union IC-LoRA
takes run on the RTX3060Ti8GB. Whole-figure shape is steadier in inspected
native frames, but fingers still smear and the opening is softer than later
frames. Weaker opening-image conditioning does not fix focus and adds visible
texture. Prefer take1 as a review candidate; neither is accepted production.

## Owner-commissioned trial

The owner says "make a trial" after the [size/focus analysis](../ltx25_focus_repair_20261004/README.md).
This executes its first structural stage. Existing directions remain: constant
world size, complete-figure motion, Aseprite continuity/cleanup, and bounded local
regeneration. No new ImageGen or paid API call, protected-original edit, runtime
change, owner acceptance or finding closure. Refine Details was not run; its
separate access/hardware stage remains pending. See [job card](JOB_CARD.md).

## Watch the actual footage

| Take | Native wave | Same-timeline comparison | Editable master |
|---|---|---|---|
|1, opening-image strength1 | [Video](take_1/native_review.mp4) | [Prior v2 / structural guide / Union](take_1/comparison.mp4) | [Aseprite](take_1/native_review.aseprite) |
|2, opening-image strength0.65 | [Video](take_2/native_review.mp4) | [Prior v2 / structural guide / Union](take_2/comparison.mp4) | [Aseprite](take_2/native_review.aseprite) |

Every video has41 frames at24fps. Comparison columns are: prior registered v2
left, authored outline middle, native Union output right. Aseprite pads prior v2
by8px left/32px top to account for its earlier constant24px layout offset; no
scale, crop or temporal replacement is applied. The other columns are640×896.
PNG/master pixels are authoritative; H264 CRF15/yuv420p is a lossy viewing copy.

## Executed method

Aseprite redraws a complete schematic figure at every index: hair/head/crown,
face landmarks, shoulder/sleeves/bodice, connected arms/hands and complete tail.
Fixed root, rigid body lean and pose-aware shoulder/hair/tail response are
declared in the [guide plan](guide_plan.json). Smooth pose in-betweens and
Catmull-Rom contours are **control authoring**, not generated delivery pixels.
They carry no appearance authority. The colored approved opening supplies that
reference through whole-canvas32px padding. No defective LTX clip is traced or
edge-extracted. These are authored Canny-like outlines fed directly; no Canny
detector, human pose estimator or depth model was executed.

The outlines are an approximation of existing complete poses, not accepted
painted replacements. Occlusion/hand geometry can limit their usefulness even
when coordinate invariants pass. [Runtime input proof](runtime_input_binding.json)
checks all82 actual control PNGs plus the identity image against the source.
[Editable guide](structural_guide.aseprite) and [renderer](scripts/guide.lua)
preserve the complete method; all123 full/half/quarter guide frames are retained.

The [official2.5 graph](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/3bf3ca62595f1764c47d01c35c8e5dfe47e1a88f/example_workflows/2.5/LTX-2.5_ICLoRA_Union_Control_Distilled.json)
loads the [Union adapter](https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control)
on2.5. The adapter is2.3-trained; this trial retains the installed2.5 W4A8
transformer/encoder and matched2.5 VAE/upscaler. Adapter download is anonymous,
revision-pinned and SHA-256 verified:654465352bytes,22.83seconds. No weights are
redistributed. [Download receipt](adapter_download.json) records the pin/hash.

Actual recipe:41 frames,24fps,seed20261004,320×448 eight-step first pass with
160×224 aligned control, learned2× latent upscale,640×896 three-step refine
with320×448 aligned control, tiled publisher-default diffusion-VAE decode.
CFG1 ordinary negatives are inactive. LoRA/control strengths remain1; only
opening-image strength changes1→0.65 in take2, plus filenames/runtime label.
[Controlled settings](controlled_settings_comparison.json) verify that difference.
This minimal Comfy reproduction declares Euler-ancestral sampling and explicit
sigmas; it is not claimed byte-identical to the publisher executable pipeline.

## Hardware and cost

| Take | Elapsed | Sampled total-card peak | New GPU LoRA weight-application calls |
|---|---|---|---|
|1, first model initialization in this process |172.97s |7152MiB |4377 |
|2, cached model/conditioning available |71.44s |7470MiB |4303 |

Both install480 weight patches and actually apply them on GPU. The second node
proof is process-cumulative8680 calls; subtract the first4377, as recorded in
[application summary](patch_application_summary.json). This proves execution,
not useful control or artwork acceptance. Five-second memory sampling can miss
instantaneous peaks. Different cache states prevent attributing the speed
difference to weaker image strength. Dynamic VRAM, two offload streams and
BF16 VAE were actually checked. The owned server was stopped after an empty queue.

Total:2 new transformer takes,244.41s render wall time,1 verified654MB adapter,
0 ImageGen/paid calls. The two-take cap is exhausted. Prior five-take/one-key,
zero-generation registration and decoder experiments remain preserved; costs
are not silently reset by naming this control trial a new method.

## Results and limits

[Native diagnostics](native_diagnostics.json) measure all41 frames per take
before post-registration. They read numerical regions only, with no Python
image editing, resized review images or saved crops. Dark-eye/color detectors
and fixed face-region edge metrics are supporting measurements: painted value,
pose, correspondence and noise can change them. They cannot accept the figure.

| Diagnostic | Take1 | Take2 |
|---|---|---|
| Eye-spacing peak-to-peak / first frame |0.86% |1.51% |
| Gem-to-waist distance peak-to-peak / first |0.42% |1.89% |
| Neck-to-waist distance peak-to-peak / first |2.26% |0.22% |
| Maximum root displacement from own first |1.71px |0.25px |
| Maximum root distance from declared guide |1.26px |1.02px |
| Fixed face-region edge-variance max/min |4.93 |5.39 |

Relative stability and absolute placement are separate: neither native take
clears the strict1px guide-root limit across the entire clip. No post-generation
registration, hand replacement, sharpening, matte repair, hold insertion or
frame selection was applied. Small numbers do not remove visible hand/focus
failures. Native inspected take1 indices0/13/22/40 and take2 indices0/22/40 show:

- Less obvious whole-figure breathing in these poses, preserving recognizable
  approved colors/design and coordinated generated body response.
- Persistent streaked/fused fingers, especially around the raised/lowering hand.
- Softer opening followed by sharper contours/details; loop focus remains poor.
  Face-region edge variance grows almost monotonically from88 to427 in take1
  and100 to528 in take2. This supports progressive detail growth across the
  clip; it does not prove a cause or equate edge variance with perceived focus.
- Take2 adds more texture/noise and does not improve the focus diagnostic.

[Visual review](native_review.json) rejects both for production and prefers
take1 for owner comparison. Full-speed/human seam acceptance is pending.
Refine Details is still the next temporal-detail candidate after geometry review;
this trial does not claim that adapter ran or that it will cure the hand. A
consistent-detail source family and, if needed, a corrected complete painted
control sequence remain preferable to another unconstrained take. The weaker
opening-lock hypothesis failed; do not spend a third take repeating it.

## Verification and publication

Each take retains both native stages, saved video latents, exact workflow,
prompt/inputs/adapter hashes, queue ID, history, time/memory and GPU application
proof. [Take1 checks](take_1/verification.json) and [take2 checks](take_2/verification.json)
prove82 native Aseprite pixel roundtrips,246 exact comparison columns, original
41-frame/24fps clocks and correct native dimensions. Aseprite timing is1708ms
per41-frame master. Guide/root mathematical preflight and actual runtime-byte
checks are separate from native output acceptance.

[Manifest](manifest.json) binds payload/source ancestry; [remote receipt](remote_verification.json)
records exact immutable public GitHub SHA-256 access after publication.
[Impact](../../../design/audit_impacts/ltx25-union-trial-20261004.json) records
rules, baseline, files and gates. `ARCHIVE_COMPLETE` does not grant
`DELIVERY_ACCEPTED`, runtime, device, child or owner acceptance. MA-ROSHAN-003,
MA-ROSHAN-005 and MA-ROSHAN-006 lifecycles remain unchanged.
