# Roshan wave: omitted refinement tested

The corrected installed 2B multiscale recipe completed twice on the RTX 3060 Ti
8 GB. It sharpens some contours but still tears the shoulder and misses the
lowering beat. Neither take is acceptable production animation.
The enlarged eight-guide 2.3 baseline was stopped before its first sampling
step completed; 2.5 is the next quality candidate, not a tested winner here.

## Footage and editable sources

- [Native side-by-side comparison](comparison/native_two_pass.mp4): standard first pass, its refined result, stronger-mid-key refined result; pixels padded at 1:1.
- Standard take: [native refined footage](results/official_standard/refined_native.mp4), [native Aseprite master](results/official_standard/native_review.aseprite), [on twos](results/official_standard/on_twos.mp4), [cadence/master](results/official_standard/on_twos.aseprite).
- Strong-mid take: [native refined footage](results/official_mid_strong/refined_native.mp4), [native Aseprite master](results/official_mid_strong/native_review.aseprite), [on twos](results/official_mid_strong/on_twos.mp4), [cadence/master](results/official_mid_strong/on_twos.aseprite).
- [Aseprite complete-figure guides](inputs/wave_guides.aseprite), [one new missing native pose](inputs/missing_lowering_native.png), [exact pose prompt](briefs/missing_lowering_key_prompt.txt).
- Native frame 19/22/25 contacts: [standard](results/official_standard/lowering_native_contact.png), [strong mid](results/official_mid_strong/lowering_native_contact.png); no resized QA thumbnails.
- [2.3 actual failed receipt](results/ltx23_chunked/receipt.json), [history](results/ltx23_chunked/history.json), [owned-job interruption](environment/fallback_interrupt.json). No 2.3 footage was returned by this job.

## Same-content trial

Every take binds the same eight complete-frame guide PNG hashes at 0, 3, 7, 17, 22,
27, 36, 40, with the same action prompt, seed 20261004, 41 frames and 24 fps.
Only the declared settings below differ. The second 2B take strengthens key 22
to 1.25 with a whole-frame white attention mask.

| Take | Actual native canvas | Recipe | Wall time | Sampled total-card peak | Result |
|---|---|---|---:|---:|---|
|2B standard, cold |352×544 ->704×1088 |7 steps, learned 2x, AdaIN, 3 steps |70.150 s |7011 MiB |Execution pass; shoulder tear, ghost lowering hand and early rest |
|2B stronger key 22, warm |352×544 ->704×1088 |Same, stronger mid guide |37.570 s |7146 MiB |Execution pass; early rest and detail failures persist |
|2.3 chunked baseline |352×544 |8 steps planned; 512-token FF chunks; no upscaler |638.568 s |7909 MiB |Interrupted at sampler 0/8; no returned footage |

The peaks are five-second samples including desktop/other processes, not
model-allocator peaks. No owner apps were closed. These are measured times
on this workstation, not estimates or community benchmark reproductions.

The previous [25-frame small 2.3 temporal-retake pass](../ltx_retake_repair_20261004/README.md)
remains separate evidence: 598.178 s cold, 448×256, returned footage with
visual defects. Its successful execution does not establish that this larger
eight-guide wave fits efficiently. Prior rejects and the earlier 7/6 attempt
overrun remain published; this changed brief does not erase them.

## What changed

The official matching 2B 0.9.8 config specifies multiscale rendering. We
reproduced its 7-step first pass, learned spatial upscale, per-channel AdaIN
mean/std match and 3-step refine in ComfyUI. This is a Comfy reproduction,
not execution of the publisher's Python pipeline. FP8 T5 stored weights with
CPU FP16 text processing, tiled decoding and independently reset sampler
noise streams are declared differences. The official decode-noise defaults
are 0.025/0.05.

The official literal 0.6666666 plus integer/32-pixel flooring maps requested
576×832 to 352×544; 2x refinement decodes 704×1088. We retain all native
frames, plus the recipe's declared whole-canvas 576×832 output resize. That
output normalization is not the native QA image or a subject repair.
[Official settings/source pin](environment/official_multiscale_source_reference.json),
[saved config](environment/ltx_official_config.yaml),
[actual graph](results/official_standard/workflow.api.json).

Aseprite uniformly reframes the four existing whole-figure pose sources into
a portrait. The figure occupies about 757 px in the 576×832 guide canvas;
the waist is a registration landmark, not a frozen shoulder/body. Source
256 px cells remain soft: enlargement adds no original detail.
Frame 3 reuses rest as an explicit initial hold. Exactly one ImageGen call
fills the missing complete-figure mid-lowering key 22, with native transparent
1024×1536 output preserved and Aseprite normalization separately recorded.
Shoulder, bodice, torso, hair and tail remain part of every generated frame.
[Geometry](environment/portrait_geometry.json),
[ImageGen receipt](environment/imagegen_receipt.json),
[registration](environment/missing_key_registration.json).

The first-pass frame 22 already rests, and refinement retains that timing
failure. Refined frames 6/7 tear at the shoulder, frame 20 loses the lowering
hand, and 22/23 already rest. Sampling on twos cannot repair pairs in which
both complete frames fail. The cadence test therefore retains even indices
and marks failure; no unrelated clean pose conceals missing action. Its
21-frame 12 fps MP 4 ends with an extra 1/24 s hold; the Aseprite master uses
rounded 1708ms matching the canonical 41/24 s timeline.
[Native review](environment/review.json), [cadence](results/official_standard/cadence.json).

At CFG 1, ordinary negative conditioning is skipped. Positive anti-blur wording
can influence generation but does not guarantee sharp anatomy. The generic
NAG node's attention hooks are absent from installed LTX attention. We pinned
a dedicated KJ LTX cross-attention implementation and verified CPU arithmetic
and stock-scale identity. The planned GPU NAG variant was not submitted
after the baseline stalled: no claim of effective GPU negative guidance or
motion repair is made. SageAttention is not installed.
[Adapter check](environment/adapter_math_verification.json),
[pinned NAG source/license](environment/nag_source_reference.json),
[actual software/profile](environment/software_hardware.json).

## Method choice and 2.5

Aseprite remains the best editable source, timing and defect-review bridge.
Corrected 2B two-pass is fast enough for auditions but failed this wave's
finishing quality. The already-tested small 2.3 retake can remain a bounded
repair experiment; this larger configuration is impractical.

Prioritize a matched 2.5 test for the next quality comparison. It brings a
matching Gemma 4 encoder and new decoder; substituting only its transformer
into the 2.3 graph is invalid. A published community 8 GB two-pass baseline
uses W4A8 ConvRot, BF16 DiffVAE and dynamic offload on Comfy 0.34.3 / RTX 4060
Laptop. Its 84.58 s small 512×256 result does not establish portrait performance
on this 3060Ti. The exact four components total 23.835 GiB; official decoder
and upscaler HEAD requests returned 401 GatedRepo anonymously. No 2.5 weights
were downloaded or access/contact-sharing terms accepted.
A small native CUDA W4A8 probe now passes on this SM8.6 card, without proving
full-model fit or speed. Official pipeline docs support 2.5 temporal retake;
Desktop release claims conflict with its pinned capability flags/tests.
Generated interior keyframe slots are a further2.5 temporal-detail experiment,
with added token cost and no implementation or benchmark here.
[Concrete next-test preflight](briefs/LTX25_PREFLIGHT.md),
[pinned components/workflow/access probe](environment/ltx25_pinned_workflow_preflight.json).

## Cost, verification and acceptance

[Job card](briefs/job_card.json), [actual usage](environment/usage.json):
three queued model jobs, two completed takes, one interrupted job, one
ImageGen call, 505024432 new model bytes andUSD 0 paid APIs. Three startup
failures occurred before inference and remain separately recorded. No second
22B take or 2.5 download was silently added. Automated cleanup wall time was
not fully metered; per-subprocess timeouts and actual verification remain
recorded, so no fabricated cleanup-time PASS is claimed.

[Machine verification](environment/trial_verification.json) checks actual
recipe inputs, all native Aseprite pixel round trips and video frame/fps
metadata. [Adapter math](environment/adapter_math_verification.json) checks
installed small CPU tensors; it does not benchmark GGUF motion.
The prior full game suite passed in this continuing task; exact runtime
Git objects remain identical at the new baseline.
[Runtime baseline receipt](environment/runtime_baseline_verification.json).
New document-authority/development gates and exact branch CI remain separate.

These are source-only studies under the owner-revised animation rules.
No production, runtime, device, child or owner acceptance; no audit finding
is closed and game-wide audit satisfaction remains UNSATISFIED.
GitHub publication and anonymous exact-revision hash verification establish
archive delivery only, never creative acceptance.
