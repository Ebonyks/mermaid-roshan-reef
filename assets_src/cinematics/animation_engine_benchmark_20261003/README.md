# Animation engine comparison — 2026-10-03

Status: `REFERENCE_ONLY / LOCAL_COMPARISON_COMPLETE / PARTIAL_DELIVERY`.
Commission: same-content engine tests, evaluation and published footage.
Source baseline: `ecb68651c67e66501eeab2c719b152d8982023c2`.
Executed October 3–4, 2026. **Zero accepted production seconds.** Eight public
native takes and their Aseprite studies are included. Three Hunyuan takes ran
locally; their pixels are withheld from worldwide publication under the model's
territorial output terms. API tests await configured authentication and an
authorized funded cap. The unsupported/deferred rows below have no test footage.

## Recommendation from this PC

For character pilots, use **Aseprite pose and socket preflight → ComfyUI LTX
Video 2B pose-guided generation → Aseprite isolation, review and atlas export**.
The controlled LTX take is the strongest character candidate: it keeps Roshan's
tail and completes a raise/lower/return in 96.721 seconds. It still changes body,
head and hand details, so it is not a production winner. The source guides were
not registered: the crown colour centroid shifts about 82 px across the authored
keys. Equal atlas cells did not establish a fixed body. Register real landmarks
in Aseprite before another bounded generation study.

For small anchored objects, prefer authored 2D parts or painted view keys in
Aseprite. None of the tested generative object recipes cleared the root, socket,
topology and return requirements. Hunyuan produced the clearest seating-surface
change and the most stable plant identity, but the swing shape/return and plant
direction remain unaccepted; its public-output restriction also prevents it
from being the default project exchange workflow.

Keep APIs for CGI scene trials as directed by the owner. This local study does
not select an API quality winner. Do not purchase runs without the pending cap
and authentication. Do not spend ImageGen calls independently recreating every
motion frame; use existing identity art and only commission a named missing key.

## Inspect the actual footage

- Roshan: [Wan vs LTX baseline](comparison/wave_wan_ltx.mp4),
  [LTX first-frame vs owned-pose controls](comparison/wave_controlled.mp4).
- Objects: [plant](comparison/plant_wan_ltx.mp4),
  [swing](comparison/swing_wan_ltx.mp4).
- [Controlled LTX native](results/ltx_2b_guided/wave/native.webm),
  [MP4 preview](results/ltx_2b_guided/wave/preview.mp4),
  [direct-native Aseprite master](results/ltx_2b_guided/wave/aseprite_native/bridge.aseprite),
  [bridge preview](results/ltx_2b_guided/wave/aseprite_native/bridge_preview.mp4).
- [SCAIL low-resolution native](results/scail2_lowres/wave/native_0.mp4),
  [Aseprite master](results/scail2_lowres/wave/aseprite/bridge.aseprite).
- [All results](results/), [machine matrix](matrix.json),
  [summary](summary.json), [job cards](briefs/), [inputs](inputs/),
  [payload manifest](manifest.json). Every public take has an indexed
  all-frame diagnostic board and a separate review receipt.

| Recipe | Wave / plant / swing seconds | Observed result | Footage |
|---|---:|---|---|
| Existing Wan2.2 TI2V 5B Q4_K_S, 24 steps | 372.545 / 352.769 / 371.291 | Wave does not settle; plant adds a stalk; swing supports deform | Public, three native takes |
| LTX Video 2B 0.9.8 distilled, 7-step first pass | 101.583 / 96.276 / 110.768 | Wave splits anatomy; plant changes root; swing motion insufficient | Public, three native takes |
| LTX 2B with four owned pose keys, take 2 | 96.721 / — / — | Best character candidate; body/hand/anchor checks unresolved | Public, one native take |
| SCAIL-2 14B, 896×512, 40 steps | Cancelled at 953.828 / — / — | First sample took 202 s; projected run exceeded 1,800 s cap | Failure receipt; no clip |
| SCAIL-2 14B, 448×256, 20 steps, take 2 | 680.516 / — / — | Low apex, missing return and ghosting | Public, one native take |
| Hunyuan 1.5 480p step-distilled, 8 steps | 947.797 / 400.422 / 398.032 | Wave misses endpoint; plant identity stable but nod unproven; swing motion promising but shape/return fail | Three local owner clips; public metadata only |
| MiniMax H3 / FreeVideo VDN | — | Model license excludes the US; not downloaded or run | `BLOCKED_LICENSE` |
| FramePack | — | Source inspected; 39.91 GiB CPU weight inventory vs 5.5–15.2 GiB available RAM, plus output territory restrictions | Preflight deferred; no measured render/peak |
| Current LTX Desktop native | — | Official native requirement ≥16 GB VRAM; this GPU has 8 GB | `UNSUPPORTED_NATIVE` |
| LightX2V | — | Optional alternate runner for a model; no installation or speed test here | Not tested |
| fal Wan Turbo / LTX Fast / Kling Turbo API | — | Authentication absent and funded cap unanswered | Not submitted or billed |

The three baseline LTX pilot jobs averaged 102.876 s versus Wan's 365.535 s:
about 3.55× faster **for these operational recipes**. This is not accepted-output
throughput, a same-step model comparison or a latest-LTX claim. Seven-step
single-pass 0.9.8 is an older compact model and omits the official two-pass
refinement; it is distinct from current LTX Desktop/2.5.

## Fairness, provenance and limits

The wave, hydrangea nod and fore/aft shell swing use the same hashed first-frame
bytes and identical action text in each baseline. Seed 20261003, 41 frames at
24 fps (1.708333 s), 896×512, fixed camera. SCAIL's second take explicitly uses
448×256 and 20 steps. SCAIL adds an owned pose-video/mask; controlled LTX adds
four owned pose images at indices 7/17/27/36. These are extra-control lanes,
not equal-input baseline wins. No retiming, interpolation or repeated frames
conceal failed action. The driver has four authored keys plus a return hold at
0.3/0.4/0.4/0.4/0.5 s; it is neither fresh generated motion nor an accepted loop.

Hardware: RTX 3060 Ti 8 GB, Ryzen 5 3600, 47.91 GiB RAM, driver 591.86.
Other desktop applications remained open. One task-owned inference worker ran
at a time. The idle Comfy server was stopped before Hunyuan; its residency and
this environmental difference are recorded. Hunyuan's first job includes
auxiliary downloads. Runner initialization is separate. No isolated speed ratio,
Android bottleneck diagnosis or exact peak-memory comparison is asserted.
See [environment receipts](environment/), model byte/commit pins and resolved
requirements. SCAIL's automatic reference segmentation uses **Meta SAM3.1 under
the SAM License**, acknowledged in its saved license sidecar; it is not covered
by the model's Apache license. Hunyuan's code license and output terms differ.

Aseprite preserved raw layers and editable masters, removed only connected gray
backdrop pixels, and exported six POT atlas pages with exactly 41 unique native
indices per take. All eight comparison masters passed reopen/pixel equality.
The initial atlas packing failure and corrected export receipts are retained.
Those eight bridges decoded the comparison MP4s; Comfy MP4s add a lossy encode.
The strongest LTX take also has a separately verified **direct-native WebM**
bridge under `aseprite_native/`, and the reusable helper now prefers native input.
Technical coverage is not visual acceptance: background shading, fringe/shadow,
hand details and filtering need review. No crop/registration/motion repair was
silently performed. Automated bridge time is not measured artist cleanup time.

## Delivery and acceptance claims

`ARCHIVE_COMPLETE` applies only to the hashed public payload in the manifest,
after its exact GitHub bytes are remotely verified. The entire all-engine
commission is **PARTIAL_DELIVERY**: Hunyuan pixels are
`HANDOFF_BLOCKED_LICENSE`; H3 is ineligible, FramePack is deferred, current LTX
Desktop is unsupported, and hosted runs are awaiting inputs. No generator handoff
is being asserted. `DELIVERY_ACCEPTED`, device, child and owner acceptance remain
false/pending. Accepted production seconds are zero. Historical rejects stay
rejected; protected originals, runtime assets, game code and Day One clips are
unchanged. Related master findings are not closed.

Machine regression evidence is separate: the full local shell run hit two
Windows launch failures before their verdicts. Both unchanged probes passed
native retries with fresh profiles; the aggregate covers all 82 required probes.
The original red log and retry logs are retained in
[project validation](environment/project_validation.json). Exact published-head
CI is recorded in the later verification receipt, not inferred from this local run.

See the [audit impact](../../../design/audit_impacts/animation-engine-benchmark-20261003.json)
and [production protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md).
