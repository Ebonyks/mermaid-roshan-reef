# Animation workflow options — 2026-10-03

Status: `SUPPORTING_CURRENT` research and production guidance. The owner authorizes
final animation workflows with identity, motion, provenance and device checks,
and requests Aseprite as the bridge when possible. The binding rules are
[design 06](../06_COMPREHENSIVE_DESIGN_LANGUAGE.md#11-cinematic-exception) and
[AGENTS.md](../../AGENTS.md#animation-production-owner-decision-2026-10-03).
The initial policy review submitted no paid job, installed nothing and accepted
no candidate. The separately commissioned [execution packet](../../assets_src/cinematics/animation_engine_benchmark_20261003/README.md)
now records installed local tools, same-content footage and Aseprite derivatives;
these reference studies change no runtime and accept no previous candidate. Prices are observations on 2026-10-03;
recheck exact endpoint, supported settings and billing before spending.

## Owner-directed production split

Recorded from this owner's 2026-10-03 conversation:

- Final animation: “Allow final animation with identity, motion, provenance and device checks”.
- Cleanup: “Use aesprite as the bridge when possible though, it cleans up results”. The tool is Aseprite.
- Routing: “local setup is the goal for the character design animation and the object animations, while api is best for cgi scenes”.

Default local character/object production and API cinematic scenes. “CGI” here
names the cinematic production lane; no change to the approved 2D storybook
medium is inferred. Preserve approved identities rather than commissioning
character redesign. A bounded local failure can justify an exception, recorded
with its actual time/cost and existing spending authority. These are owner
preferences and method permission, not acceptance of a model, clip or device.
The source-bound [decision register](../reference/OWNER_DECISIONS.md) preserves
these instructions separately from operating defaults.

## What the project evidence establishes

The old rule required an individually generated still for every changed action
frame, then separately required temporal continuity. Five seconds at 24 fps
means 120 displayed frames. Still-image quality cannot establish coherent motion;
repeated independent image jobs multiply coordination, review and generation
cost. This is a production diagnosis, not a measured token invoice.

The [local Wan receipt](../../assets_src/cinematics/sky_lagoon_local_motion_v1_2026-09-30/README.md#local-ai-result)
records Wan 2.2 TI2V 5B hydrangea/fir takes at 561.49/481.00 seconds. Both
moved their upper silhouettes less than one pixel at 256px review scale and
were rejected as static/flickering. Attempts also record unsuitable latent
geometry, FP8/loading failures, CPU text-encoding stalls and VAE memory pressure.
Completing an encode did not produce usable acting. The
[later Aseprite study](../../assets_src/cinematics/sky_lagoon_review_v3_2026-10-01/README.md)
contains 72 distinct states and remains an agent-reviewed reference candidate.
Its three new ImageGen sheets and two correction passes demonstrate a cleanup
bridge, not owner or runtime acceptance.

Read-only workstation inspection confirms RTX 3060 Ti, 8192 MiB VRAM, Ryzen 5
3600 and approximately 48 GiB RAM; the NVIDIA driver reports 591.86. The model
drive H: is an ADATA SX8200PNP NVMe SSD, with about 60.4 GiB free at inspection.
That space must cover a selected checkpoint, encoder, environment and outputs;
recheck before a large H3/14B download and avoid duplicate model libraries. VRAM usage
changes with other work; do not terminate another client's renderer. System RAM
helps offloading but does not provide the bandwidth of additional VRAM.

At the initial inspection the installed setup was ComfyUI with Wan 2.2 TI2V
5B. The follow-up benchmark installs Wan2GP 13.141 at pinned revision
`b8b18f8114e432eea8f3d7e853a51dd91fa99571` in a separate Python 3.11 environment;
the existing Comfy installation remains the baseline. Recent existing receipts establish a newer baseline: Q4_K_S model
and text encoder, 896×512, 41 frames, 24 steps; nursery scrub A4 took 165.68 s
and candy-neck twist A1 took 191.13 s. Both declare
`LOCAL_MOTION_REFERENCE_ONLY`: execution PASS is not visual acceptance. The
[impact record](../audit_impacts/animation-workflow-policy-20261003.json)
retains their paths, hashes and settings. These different jobs are not a
controlled speed comparison with the earlier 481–561 s full-precision trials.
The GGUF download receipt's older “not yet render verified” status is stale
for these exact outputs; retain its history rather than relying on it alone.

Comfy's [native 5B workflow](https://docs.comfy.org/tutorials/video/wan/wan2_2)
can use 8 GB through offloading; [Wan's standalone recipe](https://github.com/Wan-Video/Wan2.2)
requires more. Model architecture, precision, runner and workflow geometry all
matter. None promises useful speed or faithful motion on this workstation.

## Choose the method from the action

| Need | First choice | Why and limits |
|---|---|---|
| Timing, alpha edges, pivot jitter, rope attachment, isolated bad drawing | Aseprite cleanup of reusable states | Preserve identity; fix the actual defect without regenerating unrelated art. |
| Gate hinge, seesaw, modest glint, sparse smoke/effects | Keyed 2D parts or effects, edited/reviewed through Aseprite where practical | Controlled support and endpoints. These cannot stand in for missing character acting or perspective changes. |
| Fore-and-aft swing or another changing visible surface | Approved view keys plus authored in-betweens; compare a video-model take if keys are missing | Requires changing seat inclination, surfaces and occlusion about the horizontal beam. Lateral wobble of one seat image fails the action. |
| Roshan swimming, turning, helping or expressive contact | Existing authored action coverage, then short image-to-video or guided video-to-video take | Preserve the atlas identity. Contacts and new viewpoints need whole-sequence review; an attractive opening cannot accept the motion. |
| Short story shot | Approved clean first frame plus an API temporal video backend; edit in a video editor | One shot/action at a time. Keep the child's performed action in gameplay. |
| Missing identity sheet, view or local damaged detail | One bounded still-art job | ImageGen supplies visual material, not an automatic 24-fps production assignment. |

Prior owner rejections remain in force. Allowing a method does not accept the
rejected source-warp set, its wrong swing axis, a generic sticker wobble, or a
new interpretation of the approved characters. A proposed keyed approach earns
acceptance from its exact motion, not from this table.

## Aseprite is the sprite bridge

Use this path where raster sprite output is appropriate:

1. Inventory reusable sources and write one
   [job card](../templates/ANIMATION_JOB_CARD_V1.md). Lock identity, action, pivot,
   contact, fixed parts, endpoints, required view and native/runtime scale.
2. Produce the smallest useful motion take or authored state sequence. Keep its
   native output and source hash. Extract a lossless PNG sequence when the source
   is video; video is not presumed to contain alpha.
3. Import into an RGBA Aseprite master, preserving the polished painted look.
   Keep source/reference material on excluded layers and cleaned export art on
   separate layers. Tag anticipation/action/settle or loop/one-shot ranges.
4. Clean mattes, fringe, topology and local details. Register a consistent pivot
   and intentional sockets, rather than recentering each visible bounding box.
   A neutral backdrop is an isolation aid, not reliable automatic segmentation.
   Avoid fake checkerboard alpha, palette reduction, jagged pixel-art conversion,
   or erasing required hair/ropes/translucent details.
5. Edit timing, contacts and transitions. Use onion-skin/frame-step for defects,
   normal-speed playback for performance, and the exact runtime scale for
   readability. A loop needs a matching pose and velocity across its seam.
   Ping-pong suits reversible mechanical motion; it does not reverse smoke,
   a walk, object transfer, cleaning or irreversible action.
6. Export lossless RGBA atlases and timing JSON. Use stable frame IDs, per-frame
   durations, pivot/socket tables, trim offsets, tags and nonbleeding padding.
   Keep the editable `.aseprite`, input/output hashes and an edit/derivation log.
   Reopen/export once to verify the cleaned master reproduces the delivered pixels.
7. Prove actual Godot sampling, contact, looping/cancellation and scene draw order;
   then run required Mobile/Speedy/device/child/owner gates. Disk export alone
   does not establish good playback.

Aseprite's [CLI](https://www.aseprite.org/docs/cli/) can export sheets and JSON,
and its [animation tools](https://www.aseprite.org/docs/animation/) support frame
timing and tags. Project scripts must also preserve the game's custom sockets
and state contract; CLI output does not supply those automatically. Frame
durations in an 8–12 fps painted loop are a starting artistic choice, not a
mandate to reduce every action to six keys or to upscale to 30 fps. Godot still
renders at the device target rate.

For long full-scene footage, use the existing video editor for cuts/audio and
encoding. Use Aseprite on extracted repair windows, sprites or isolated effects
when useful; forcing an entire large movie through it adds memory and labor.
Retain exact source frame mapping when reinserting edits. The existing Day One
selected-cut clips keep their separate straight-cut restrictions under `DL-CIN-16`.

Pre-bake sprite animation; no AI inference runs on the phone. Export only useful
frames at their required screen scale and avoid simultaneous large transparent
atlases. Twelve 256×256 RGBA frames occupy about 3 MiB uncompressed; forty-eight
512×512 frames occupy about 48 MiB before padding/mipmaps. These are arithmetic
examples, not measured project memory. Actual atlas packing/import compression,
decoded memory, GPU memory and overdraw need separate measurements. A lower art
cadence does not lower the game's 30-fps responsiveness target.

## Local models and runners for this PC

The table preserves the candidate rationale; the [execution packet](../../assets_src/cinematics/animation_engine_benchmark_20261003/README.md)
owns actual installed/tested/unavailable states and comparisons. None is an
accepted production replacement. “Fits”
means a documented or plausible optimized execution path; it does not promise
short turnaround or correct anatomy. Godot remains the runtime, ComfyUI/Wan2GP
are inference runners, and Wan/LTX/Hunyuan/SCAIL/H3 are different motion models.

| Candidate | 8 GB workstation fit | Appropriate comparison |
|---|---|---|
| [LTX-Video 2B 0.9.8 distilled](https://github.com/Lightricks/LTX-Video) | Best small-model pilot; infer feasibility from its published low-VRAM 2B design, then measure encoder/VAE peaks at bounded dimensions. This is the older LTXV line, distinct from LTX-2. | Fast short organic/object motion. It may lose painted detail or exact contacts; no guaranteed identity improvement. The official 0.9.8 multiscale [configuration](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-2b-0.9.8-distilled.yaml) has 7 first-pass and 3 second-pass timesteps, not a universal 8-step recipe. |
| [SCAIL-2](https://github.com/zai-org/SCAIL-2), through a pinned low-memory runner | Conditional quantized/offloaded pilot; its 14B native example is not an 8 GB guarantee. [Wan2GP](https://github.com/deepbeepmeep/Wan2GP) supports it, but exact checkpoint/peak memory must pass locally. | Newer June 2026 character specialist: supplied driving video plus masks/reference identity, with end-to-end and pose-driven modes. Can test source-bound performance instead of prompt-only acting. Roshan's tail and contact choreography require matching driving material; generic human skeletons do not establish mermaid motion. |
| [HunyuanVideo 1.5 480p I2V step-distilled](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5), through Wan2GP | Tencent's native Linux recipe needs 14 GB even with offload. Tencent separately links Wan2GP's optimized path reporting as low as 6 GB. Use that path, not the native recipe, for an 8 GB trial. | Independent general motion alternative. Official distilled settings recommend 8 or 12 steps. Local US testing and worldwide public footage are different: the [weight/output terms](https://huggingface.co/tencent/HunyuanVideo-1.5/blob/main/LICENSE) exclude EU/UK/South Korea use/display/distribution, so public posting is withheld pending a compliant route or separate grant. Its 4090 speed result does not predict 3060 Ti turnaround or Roshan identity. |
| [FreeVideo / VDN MiniMax H3](https://github.com/FlashML-org/FreeVideo) | Developers explicitly claim 8 GB VRAM + 16 GB RAM through streaming/offload; Windows launcher and ComfyUI plugin. Host/disk transfer can dominate latency. The current H3 weight license excludes the United States, so this US workstation cannot run the candidate under that grant. | Current experimental inference work using an 8-step VDN-H3 derivative. First/end images and reference inputs are relevant capabilities, but the [H3 terms](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) block this local test; no download/run/footage is claimed. On this Ampere GPU its FP8 storage can use BF16 computation; newer-card FP8 speed claims do not transfer. |
| [FramePack](https://github.com/lllyasviel/FramePack) | Official Windows/RTX 30-series support and minimum 6 GB VRAM. The pinned startup loads approximately 39.91 GiB of CPU component weights before overhead, exceeding available RAM in this active session; this is a preflight estimate, not measured peak usage. | Potentially feasible on a suitably idle host, but blocked in this active-session RAM preflight; base Hunyuan territorial output restrictions also prevent an unrestricted public-footage packet. Weak first choice for rapid short sprite trials; not evidence of a faster replacement. |
| [LTX Desktop / current LTX 2.5](https://github.com/Lightricks/ltx-desktop) | Official Windows local mode requires at least 16 GB VRAM; below that the app uses API-only mode. Other community offload paths may fit, but are untested here. | Keep in the API cinematic lane. The newest model is not automatically the best local fit. |

Wan2GP is the most useful optional multi-model runner for this comparison: it
supports Windows/Ampere, low-memory offloading, quantization and selected
motion/control inputs. Pin its revision and exact Python/PyTorch/kernels in a
separate environment; preserve the known working ComfyUI installation. Its
[installation guide](https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/INSTALLATION.md)
distinguishes RTX 30-series kernels from newer hardware. Do not install every
optional module, prompt enhancer, audio generator or upsampler by default.

[LightX2V](https://github.com/ModelTC/LightX2V) is another inference accelerator,
not another motion model. Its [low-resource guide](https://github.com/ModelTC/LightX2V/blob/main/docs/EN/source/deploy_guides/for_low_resource.md)
explicitly covers 8 GB cards with offloading and distilled Wan paths. It is a
follow-up speed comparison if runner overhead dominates, not the first new
stack to install alongside everything else. INT8 is the broad compatibility
path in that guide; Ada/Blackwell-specific kernels do not establish Ampere
acceleration. Large advertised gains come from other hardware/settings.

MiniMax's [H3 release](https://www.minimax.io/news/minimax-h3-open-source) also
makes a scope distinction: its hosted context orchestration and 2K regeneration
are not all included in the local base. A local H3 derivative does not reproduce
the full hosted system automatically. Check the actual model license and
territorial restrictions before model acquisition/use; record the derivative,
not just “H3”. Keep family recordings out of benchmark inputs and use silent
review exports.

Recommended sequence: keep the recent Wan GGUF take as the measured baseline;
pilot LTX 2B on one organic object, then SCAIL-2 on one character action only
when a suitable owned/approved driving clip exists. Hunyuan 1.5 is the next
general-motion comparison when no driver exists. FreeVideo/H3 is excluded on this US workstation under its current terms;
a separate applicable license would be necessary before acquisition/use. Select only one new runner/model at a time. Exact identities,
geometry, contacts and Aseprite cleanup burden decide whether it stays.

## Local setup and measurements

1. Inventory installed checkpoints, runner versions and model receipts. Preserve
   the existing Comfy/GGUF environment and protected source art. Check free
   VRAM/RAM/disk and SSD throughput; fitting via disk streaming can be slow.
2. Pin a separate selected runner/checkpoint/license and record download sizes,
   revisions/hashes, dependencies, driver and GPU. Verify one tiny supported
   smoke test before expanding resolution, duration or jobs. This research
   itself downloads/installs no model and submits no new generation.
3. Use one task-owned queue. Measure cold load, warm load, text encoding,
   denoising, VAE decoding, export and Aseprite cleanup separately. Reuse
   unchanged encoder/model work where supported. Do not add a large prompt LLM
   to every short action job.
4. Use the exact model's supported geometry and temporal count. The known GGUF
   job uses 896×512/41 frames; the native 5B reference used 1280×704. Neither is
   a native 1280×720 cinematic output. Record crop/pad/scale mapping; arbitrary
   low-resolution values that failed an older path are not a reusable preset.
5. Test compatible quantization/distillation/cache settings against an unchanged
   source and required action. Step counts, LoRAs, VAEs and latent geometry do
   not transfer freely between models. Tiled decode/offload reduces memory but
   can add time. Preserve the demonstrated `--disable-mmap` workaround for its
   specific Windows crash, not as a universal acceleration claim.
6. Compare one contact action and one object motion, including rejected takes
   and Aseprite cleanup. Keep the source-bound exact identity, contour, pivot,
   support and loop seam; a model with shorter sampling time can still lose.

For mechanical props, local authored 2D transforms/painted view keys and
Aseprite often provide tighter constraints than generative video. They still
must perform the actual intended action; rejected wobble studies are not
promoted by this recommendation. No diffusion model or new local GPU workload
runs on the child's device. Baking a loop is separate from Godot's playback
performance and its Mobile/Speedy/30-fps device gates.

## Low-cost API shortlist

These are candidates, not rankings for this artwork. Providers' endpoint pages
are primary billing documentation; none establishes Roshan identity or motion
quality. Keep source artwork private unless its existing sharing authority
permits upload. API jobs use sanitized generation inputs and retained request
IDs/receipts; an API response URL is not the durable GitHub handoff/archive.

| Exact endpoint/model | Observed charge | Suggested test |
|---|---|---|
| [fal Wan 2.2 A14B I2V Turbo](https://fal.ai/models/fal-ai/wan/v2.2-a14b/image-to-video/turbo) | $0.05/request at 480p; $0.075 at 580p; $0.10 at 720p | Cheap temporal comparison against local 5B. Confirm frame count/duration and settings before submission; the page quotes per-video pricing. |
| [LTX `ltx-2-3-fast`](https://ltx.io/model/api/pricing) | 720p $0.03/sec; minimum 6-second request $0.18 | Independent low-cost backend. [Supported durations](https://docs.ltx.io/models/ltx-2-3) start at six seconds; do not budget a fictitious two-second request. |
| [LTX `ltx-2-3-pro`](https://ltx.io/model/api/pricing) | 720p $0.04/sec; six seconds $0.24 | Small quality escalation if Fast loses contours/contact. Same artwork comparison required. |
| [fal Kling 2.5 Turbo Pro I2V](https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video) | $0.35 for five seconds; $0.07/additional second | Compare articulated motion or acting; higher cost is not proof of a better mermaid or mechanical constraint. |

The LTX [I2V schema](https://docs.ltx.io/api-documentation/api-reference/async-video-generation/submit-image-to-video)
supports `generate_audio: false`; use silent object/character studies and retain
family voice/music authority. Newer LTX 2.5 Fast lists $0.09/sec at 720p, so
the newest default is not this review's least-cost choice. API responses and
service identities can change; record the observed model version and date.

Renting a GPU can make sense for an already-working batch, but adds setup,
idle time, storage and shutdown responsibility. For a few sub-dollar tests,
managed inference is the first comparison. Revisit rental only with measured
volume and a pinned reproducible workflow; do not assume it is cheaper.

## One bounded comparison before expansion

Local comparison uses three action briefs: a fore-and-aft swing, one visibly
flexing plant, and one Roshan action with an actual contact. API comparison
uses separately commissioned cinematic shots with approved first frames; a
sprite/object API take is an explicitly recorded fallback, not the default. Compare the same approved sources,
camera, intended duration and observable endpoints. Begin with the first brief;
do not submit all three while the setup is still failing.

Proposed research envelope: at most two takes per shot/backend and $5 total API
spend, only within an owner-authorized funded budget. This is a planning cap,
not permission to bill an account. Three commissioned cinematic briefs × two takes on Wan 720p, LTX
2.3 Fast six-second and Kling five-second would total about $3.78 before any
additional fees or setting-dependent billing. Generate native allowed durations,
then compare a shared action interval; do not retime the benchmark to favor a model.

After the first take, classify failures before retrying. Stop a backend after
two nonviable takes for the same brief. Also stop when its declared time/cost
cap is reached. Change a diagnosed input/constraint or switch method; do not
automatically move to hundreds of still generations. Task caps do not reset
when changing backend or dividing the same action into separate frame briefs.
Record reported usage when available, otherwise count generation calls. Reduce shot complexity
without erasing the required action. Failed jobs and discarded takes count.

Select using identity/topology vetoes, correct axis/action/contact, loop/endpoint
quality, native detail, cleanup minutes, wall time and total cost. Record cost
and operator minutes per accepted second, including rejects. Aseprite cleanup
should resolve a bounded defect; rebuilding most frames by hand means the take
failed the economical route. Keep rejected takes and their specific reason.

## Evidence and remaining work

The initial review was source/receipt research. The [same-content execution
packet](../../assets_src/cinematics/animation_engine_benchmark_20261003/README.md)
now owns native test footage, timings, failures, installed versions and exact
publication evidence. Its controlled LTX wave demonstrates useful action/return
improvement over first-frame-only generation while retaining source-key anchor
limitations; it is a candidate, not an accepted loop. No API quality, configured
credentials, funded budget or Android speed diagnosis is claimed. Use the
[production protocol](ANIMATION_PRODUCTION_PROTOCOL.md) for final gate lanes,
the [job card](../templates/ANIMATION_JOB_CARD_V1.md) for the production/derivation
sidecar and the [impact record](../audit_impacts/animation-workflow-policy-20261003.json)
for this policy's source and machine evidence. `MA-VIS-006`, `MA-PLAY-004` and
`MA-PERF-001` stay open in their existing lifecycle states.
