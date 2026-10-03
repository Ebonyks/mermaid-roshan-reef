# Animation workflow options — 2026-10-03

Status: `SUPPORTING_CURRENT` research and production guidance. The owner authorizes
final animation workflows with identity, motion, provenance and device checks,
and requests Aseprite as the bridge when possible. The binding rules are
[design 06](../06_COMPREHENSIVE_DESIGN_LANGUAGE.md#11-cinematic-exception) and
[AGENTS.md](../../AGENTS.md#animation-production-owner-decision-2026-10-03).
This review submits no paid job, installs nothing, changes no runtime or artwork,
and accepts no previous candidate. Prices are observations on 2026-10-03;
recheck exact endpoint, supported settings and billing before spending.

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
3600 and approximately 48 GiB RAM. The inspection also found about 4471 MiB VRAM
already occupied; that is a momentary observation, not a resource reservation.
Do not stop another client's renderer. Comfy's official workflow says its
5B model can fit 8 GB through native offloading; Wan's standalone recipe instead
specifies at least 24 GB. These are different execution paths. Neither claim
promises useful speed on this workstation. See
[Comfy's native workflow](https://docs.comfy.org/tutorials/video/wan/wan2_2) and
[Wan's official implementation](https://github.com/Wan-Video/Wan2.2).

## Choose the method from the action

| Need | First choice | Why and limits |
|---|---|---|
| Timing, alpha edges, pivot jitter, rope attachment, isolated bad drawing | Aseprite cleanup of reusable states | Preserve identity; fix the actual defect without regenerating unrelated art. |
| Gate hinge, seesaw, modest glint, sparse smoke/effects | Keyed 2D parts or effects, edited/reviewed through Aseprite where practical | Controlled support and endpoints. These cannot stand in for missing character acting or perspective changes. |
| Fore-and-aft swing or another changing visible surface | Approved view keys plus authored in-betweens; compare a video-model take if keys are missing | Requires changing seat inclination, surfaces and occlusion about the horizontal beam. Lateral wobble of one seat image fails the action. |
| Roshan swimming, turning, helping or expressive contact | Existing authored action coverage, then short image-to-video or guided video-to-video take | Preserve the atlas identity. Contacts and new viewpoints need whole-sequence review; an attractive opening cannot accept the motion. |
| Short story shot | Approved clean first frame plus a temporal video backend; edit in a video editor | One shot/action at a time. Keep the child's performed action in gameplay. |
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

## Improve local inference without an installation spiral

Keep one task-owned queue and reuse the installed native Comfy workflow. Start
with one expressive object, not a ten-object batch or a plant barely moving.
Lock the camera; state a measurable excursion, what stays fixed and the settle.
Use a supported latent geometry/frame count and record crop/pad mapping.
The 5B recipe's 1280×704 native canvas must not be misreported as 1280×720.
Do not repeat the failed arbitrary low-resolution recipe. Final landscape
normalization preserves aspect and is reviewed separately.

Record load, text encoding, denoising, VAE decode and export times individually.
Cache unchanged encoder/model work where supported; do not launch a second large
model just to expand a short action prompt. Use tiled decode/offloading only
when supported by the pinned installed workflow. Keep the already demonstrated
`--disable-mmap` workaround for its specific Windows loading issue, rather than
treating it as a universal speed improvement.

Two optional local comparisons deserve a small pilot rather than a full
migration. [Wan2GP](https://github.com/deepbeepmeep/Wan2GP) specializes in
consumer-GPU video inference and supports Wan/LTX families; it is a different
inference manager, not a new motion model or a proven improvement on this
machine. The official [older LTX-Video line](https://github.com/Lightricks/LTX-Video)
also offers `ltxv-2b-0.9.8-distilled`, a smaller alternative to the current
22B LTX model. Test its I2V identity/detail and actual load/sample/decode time
before calling it useful. Neither has been run here; pin a separate environment
and checkpoint, preserve the working Comfy setup and stop the pilot at its cap.
The older model's behavior/weights are distinct from the current LTX API.

Test one compatible quantized or distilled recipe only if its exact checkpoint,
license and runtime path are verified. Different models/LoRAs do not inherit
each other's step counts, latent geometry or acceptable outputs. FP8 storage
does not guarantee native FP8 compute speed on a 3060 Ti. An unsupported custom
node stack is a new maintenance cost; no wholesale Comfy rebuild is recommended.

[Current LTX-2](https://github.com/Lightricks/LTX-2) offers distilled and CPU/disk
offload paths, but the official current model is 22B with a substantial text
encoder. It is not a verified fast 8 GB replacement here. Prefer its API pilot
before downloading and debugging that full local stack. A local alternative
must earn its place through minutes per accepted second, including cleanup,
rather than a datacenter speed claim or merely fitting in memory.

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

Use three action briefs: a fore-and-aft swing, one visibly flexing plant, and
one Roshan action with an actual contact. Compare the same approved sources,
camera, intended duration and observable endpoints. Begin with the first brief;
do not submit all three while the setup is still failing.

Proposed research envelope: at most two takes per shot/backend and $5 total API
spend, only within an owner-authorized funded budget. This is a planning cap,
not permission to bill an account. Three briefs × two takes on Wan 720p, LTX
2.3 Fast six-second and Kling five-second would total about $3.78 before any
additional fees or setting-dependent billing. Generate native allowed durations,
then compare a shared action interval; do not retime the benchmark to favor a model.

After the first take, classify failures before retrying. Stop a backend after
two nonviable takes for the same brief. Also stop when its declared time/cost
cap is reached. Change a diagnosed input/constraint or switch method; do not
automatically move to hundreds of still generations. Reduce shot complexity
without erasing the required action. Failed jobs and discarded takes count.

Select using identity/topology vetoes, correct axis/action/contact, loop/endpoint
quality, native detail, cleanup minutes, wall time and total cost. Record cost
and operator minutes per accepted second, including rejects. Aseprite cleanup
should resolve a bounded defect; rebuilding most frames by hand means the take
failed the economical route. Keep rejected takes and their specific reason.

## Evidence and remaining work

This research is source/receipt review, not a fresh animation benchmark or an
Android speed diagnosis. No API quality, setup credentials, account-funded
budget or new local completion is claimed. Use the
[production protocol](ANIMATION_PRODUCTION_PROTOCOL.md) for final gate lanes,
the [job card](../templates/ANIMATION_JOB_CARD_V1.md) for the production/derivation
sidecar and the [impact record](../audit_impacts/animation-workflow-policy-20261003.json)
for this policy's source and machine evidence. `MA-VIS-006`, `MA-PLAY-004` and
`MA-PERF-001` stay open in their existing lifecycle states.
