# LTX-2.5 Roshan wave on RTX 3060 Ti 8 GB

Status: **REJECTED_REFERENCE_ONLY**. Five actual takes and native Aseprite masters
are published for inspection. Execution passes; painted motion/anatomy fails.
No runtime, owner, device or child acceptance.

## Same-action comparison

[Native side-by-side review](comparison/native_four_takes.mp4), left to right:
base two-pass, temporal retake, active NAG, and 48 fps sampled every second frame
at identical action timestamps. Each column is native 576x832, no resizing.
[Frame mapping](comparison/mapping.json) discloses the final-frame display
difference; original 41/81-frame sequences remain in per-take folders.

| Take | Actual wall seconds | Sampled whole-card peak MiB | Native outcome |
|---|---:|---:|---|
| [Two-pass base](results/base_two_pass/native.mp4) | 158.608 | 7381 | Better lowering timing than 2B; torn/duplicated fingers 22–25 remain. |
| [Temporal retake](results/temporal_retake/native.mp4) | 86.558 | 7197 | Same finger defect; frozen latents do not prove untouched decoded frames. |
| [Active NAG](results/anti_blur_nag/native.mp4) | 157.856 | 7568 | Negative attention really executed 528 times; hand tearing persists. |
| [48fps temporal-density test](results/temporal_48fps/native.mp4) | 173.680 | 7292 | Equivalent frame22 clearer; neighboring whole-figure smear remains. |
| [Aseprite multi-anchor source correction](results/scale_registered/native.mp4) | 158.501 | 7406 | Registered source guides pass; native scale drift and torn fingers remain. Post-export filter passes32/41 frames; nine remain marked for redraw. |

These are full job times, not sampler-only speed. Base and 48 fps include fresh
process/model loads; later takes reuse some warm state. Memory samples every 5 s
are whole-card observations, not exact allocator maxima. Generation total:
735.203s across five takes; decoder-only preflight10.184s separate. Cleanup wall
time was not fully metered. No paid API job. One new named complete-figure
ImageGen key22 redraw; its dollar/token usage is not exposed. Earlier costs
remain in the preceding packets. Five-take and one-new-key limits are exhausted.

## Constant figure size and Aseprite continuity filter

Owner correction: “She should be a static size”; “Aesprite is meant to filter
out these continuity errors, anchor the figure at multiples places per redraw
for scaling.” This changes the source and output gates, not the accepted design.

The original atlas-derived resting figure measures731px high, while the
independently generated mid-lowering key measures761px by the same alpha-bound
method. Silhouette height alone is not a scale test because poses change it.
The old key also fails the distributed landmark proportions after a single
whole-figure fit. Its waist pivot was Aseprite metadata, while LTX received only
PNG pixels; neither the pivot nor “consistent scale” text locked the figure.

Five corresponding landmarks now constrain the redraw: crown gem, both eyes,
neckline and waist. The waist target is(184.5,453) in the576x832 canvas, with
pose-specific head/neck targets preserving acting. Mid-lowering targets use
neighboring pose coordinates, with no pixel blending. The preliminary upper
bodice color-edge proxy was replaced by the neckline because a moving sleeve
is unsuitable as a rigid size anchor; the original generator guide is retained.

[Source Aseprite master](scale_continuity/registered_guides.aseprite) and
[export preflight](scale_continuity/registered_preflight.json): all eight guides
pass6px maximum anchor error,1px waist error and3% pair-distance tolerance.
One named whole-figure ImageGen replacement is preserved at its native1043x1508.
Aseprite normalizes its complete canvas, applies one aspect-preserving scale and
translation, and rechecks exported pixels. Key22's maximum error is5.259px and
waist error0.839px; this machine check does not accept its artistic identity.
The [renderer](scripts/render_scale_registered.py) runs this gate before queue
submission and records exact exported guide hashes in both sampling passes.

[Three-column comparison](scale_continuity/scale_comparison.mp4): original base,
new registered-input take, then Aseprite whole-figure registration review.
Each column stays at native576x832 and all41 timestamps are retained. Six native
new frames initially meet the absolute anchor gate. Thirty-three permit a
uniform fit;32 pass the actual post-export gate. Nine are marked for redraw:
8,12–15,22–24,29. Failed proportion fits retain their original native RGB pixels,
with only opaque alpha added by Aseprite; no held frames, isolated limbs or
nonuniform body warps conceal them. Frame8 fails the final raster check.
The editable [output review](scale_continuity/decoded_filtered_review.aseprite)
retains five anchor slices and per-frame pass/redraw tags.

[Filter verification](scale_continuity/filter_verification.json) checks real
exports, old-key rejection, zoom/root/torso-stretch defects and lossless Aseprite
round trips. [Actual transforms](scale_continuity/decoded_registration_plan.json)
disclose every frame. Scale filtering is working; this complete loop still
fails geometry and visual gates. Finger tearing, blurred frames and the
unreviewed seam/identity require coherent redraw or retake spans. Do not turn
this review into runtime art. The five-take cap prevents another speculative
model run under this brief.

## Actual recipe

ComfyUI 0.34.3 at 87465b8f1f64a27a46f16f22b13b410494dca66d; matched W4A8
distilled transformer/Gemma4 encoder, official 2.5 BF16 diffusion video VAE,
audio VAE and learned x2 upscaler. Five size/SHA checks pass: 25,957,484,024bytes.
Weights are not redistributed. [Environment receipts](environment/) retain
pins, dependencies and actual dynamic-offload/BF16/CUDA configuration.

Base/NAG/48fps run 8 Euler-ancestral steps at 288x416, learned 2x upscale, then
3 refine steps at 576x832. Both stages' native PNGs and latents are preserved.
Eight full-figure guide indices 0/3/7/17/22/27/36/40, same source images and
seed 20261004 as the earlier wave. Shoulder/bodice/hair/tail stay in the generated
figure; no limb composite.48fps doubles indices and uses 81 frames over the same
action time 0..80/48. Its 24 fps comparison selects 0,2,...,80, no interpolation;
the final display interval differs by 1/48 s. All 81 native frames are retained.

Retake is a Comfy full-canvas temporal-noise-mask implementation, not an
executed official Python RetakePipeline. It reuses refined video/audio latents,
regenerating video latent indices 3–4 (nominal frames 17–32). [Preservation check](environment/retake_preservation_check.json):
0/1/2/5 are bit-exact, yet zero decoded frames are identical and differences
outside the nominal window reach 53/255. No original-frame splice was applied.

NAG is the pinned LTX-specific KJ implementation, CFG 1, scale 5, alpha 0.15,
tau 2.5. [GPU proof](results/anti_blur_nag/nag_hook_proof.json): 528 calls,
nonzero positive/negative attention difference. Explicit negatives name blur,
smeared fingers, ghost contours, tearing and disconnected joints. This is an
active request, not a guaranteed blur-disable switch. Standard CFG 1 base/retake
do not have active ordinary negatives. NAG failed this clip's quality check.

## Sources and acceptance

[Native agent review](environment/review.json) names inspected indices and
defects. Key 22 and its single-image VAE reconstruction have readable fingers;
moving outputs fail. Some gray tail marks already exist in the unaccepted
source key. This does not rule out temporal decoder effects or accept topology.

Inputs are exact Aseprite full-figure guides from the earlier
[two-pass packet](../ltx_two_pass_wave_20261004/README.md), including its one
named missing ImageGen pose, still owner-review pending. Protected atlas pixels
did not change. Earlier 2B native frames were 704x1088 although normalized request
was 576x832; speed/quality comparisons disclose this difference. Larger 2.3
eight-guide graph stalled; its earlier small retake is a different hardware test.

2.5 is the preferred **tested local motion pilot for this wave**: it completes
the graph and improves lowering timing. It is not a production-quality winner.
Objects still need separate same-content root/support/loop tests.

## Repair workflow and reproduction

[Blur-method research and next test](briefs/BLUR_REPAIR_METHODS.md) distinguishes
Refine Details, full DFR, community de-rope and ordinary latent refinement.
Separate adapter access is pending; no adapter output is invented.
Use Aseprite to mark coherent defective spans and correct complete-figure keys,
preserving contact/root registration with shoulder/dress/hair/tail response.
Follow the [binding protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md).
Do not hide bad motion with clean holds or commission one still per frame.

Download scripts take credentials through hidden getpass for one process; no
token is persisted. Keep credentials out of source/Git/arguments. Original
renderer variants are preserved because their actual source hashes differ.
[Verification](environment/trial_verification.json), [manifest](manifest.json),
license rows and [impact](../../../design/audit_impacts/ltx25-8gb-wave-20261004.json)
separate execution from acceptance. All files are nonruntime under .gdignore.
Only the separately committed anonymous remote-byte receipt establishes
ARCHIVE_COMPLETE. These rejected studies are not GENERATION_READY jobs or
DELIVERY_ACCEPTED footage.
