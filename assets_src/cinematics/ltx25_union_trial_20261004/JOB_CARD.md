# Roshan structural-control wave trial — V1

Reference-only study, owner commissioned 2026-10-04: "make a trial".
Template: [Animation job card V1](../../../design/templates/ANIMATION_JOB_CARD_V1.md).
Baseline `09f05e529ccaae606eab89d0a9029b968f2137d1`; no runtime/owner acceptance.

## Brief and limits

| Field | Value |
|---|---|
| Intention/action | Same gentle whole-figure wave as the earlier local study: rest0–3, rise7, above head17, mid-lowering22, chest27, settle36–40. Connected shoulder, bodice, hair and tail response. |
| Fixed elements | Camera, neutral background, approved 2D identity, world scale1; waist/root(216.5,485) on640×896. Pose-dependent rigid lean, shoulder response and tail/hair follow-through are declared. |
| Entry/exit | Same rest pose, no prop/contact event. Native loop boundary review required; identical guide endpoints are not proof of an output loop. |
| Reuse/gap | Approved gesture atlas through existing registered opening image; existing keys0/3/7/17/22/27/36/40 supply shape/motion references. Sparse-guide outputs still drift/blur. No new ImageGen key commissioned. |
| Method | Aseprite manually re-authored whole-figure structural outlines and smooth pose in-betweens, then official Union IC-LoRA conditioning on installed LTX-2.5 W4A8. Structural controls carry no appearance authority/delivery pixels. |
| Native timing/geometry |41 frames at24fps;320×448 stage1/160×224 control, learned2× upscale,640×896 refine/320×448 control. All control grids legal multiples32 and latent dimensions divisible2. |
| Source scale contract | Root fixed; eye separation68px and crown-to-waist distance fixed under body lean; shoulder/neck and tail-junction targets pose-dependent. Pixel/native output proportions still need measurement and visual review. |
| Limits |2 transformer takes including failures;20 minutes each;1.3GiB adapter cap, one654465352-byte public Union download;0 ImageGen/paid API calls;30 operator minutes for guide/repair preparation before diagnosing instead of adding another render. Prior five-take and decoder costs remain visible. |
| Stop/fallback | After2 nonviable takes, retain failures and diagnose control/quantized compatibility. Do not begin a per-frame still campaign. Refine Details is a separate gated/untested stage after geometry passes, outside this initial Union download/take plan. |

## Bound inputs and provenance

[Sources](sources.json) preserve the existing complete-pose paths and padded
opening. The original256-pixel source atlas and the larger named key22 retain
their prior acceptance scopes; pose/control references do not accept designs.
[Guide plan](guide_plan.json) records every structural frame's coordinates,
declared lean and `used_as_delivery_pixels:false`. [Editable master](structural_guide.aseprite)
and [renderer](scripts/guide.lua) preserve the complete drawing/in-between method.
Every guide frame is newly rasterized in Aseprite at its actual control grid;
no defective LTX output is edge-extracted, blended or copied into these controls.

The identity image has whole-canvas32px padding only. Structural outlines are
schematic shape/motion drawings, not appearance-bearing replacement keyframes.
They are excluded from runtime. Human correspondence to the source remains a
review criterion, even when mathematical anchor invariants pass.

Adapter: `Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control`, revision
`b4d1c4d8c9e544e9bbbd6811bb4363708b6093ff`, SHA-256
`a1b888a87f661d27f08b394ae559e8e1050be33900bcc36a5cdf659e48f88d18`.
The [official2.5 workflow](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/3bf3ca62595f1764c47d01c35c8e5dfe47e1a88f/example_workflows/2.5/LTX-2.5_ICLoRA_Union_Control_Distilled.json)
supports this2.3-trained adapter on2.5. Installed matched checkpoint hashes/node
pins remain in the previous8GB study; no model weight is redistributed here.

Actual workflow, prompt, seed, loaded patch count/GPU weight-application proof,
input hashes, outputs, time/memory and errors are stored per take. CFG1 ordinary
negatives are inactive. This trial retains the publisher-default VAE decode,
8-step Euler-ancestral first pass, learned upscale and3-step refine; it is a
declared minimal Comfy reproduction, not a claim of byte-identical publisher
pipeline execution. Full-frame regeneration supplies delivery candidates.

## Review lanes

| Lane | Required evidence |
|---|---|
| Machine | Actual adapter patch installation and GPU application, aligned complete control batches, finite native41-frame output, Aseprite pixel/timing roundtrips, same-index video comparison and source hashes. |
| Native visual | Identity, root/global size, head/torso/tail proportions, connected hands, facial/contour sharpness, no grain/checker/ghosting, complete action and both boundaries. |
| Runtime/device/child/owner | Not granted by this source trial; no runtime integration. |

`ARCHIVE_COMPLETE`, executable job readiness and `DELIVERY_ACCEPTED` remain
separate. A schematic source-guide/patch/hardware pass cannot accept footage.
