# Roshan whole-figure repair and 8 GB retake trial

Status: **TRIAL_COMPLETED / REFERENCE_ONLY**. Owner commissioned 2026-10-04. No runtime or production footage is accepted.

**The RTX 3060 Ti 8 GB can execute the tested LTX-2.3 temporal retake at 448×256.** Its 25 frames took 598.178 seconds cold, with about 46 seconds in the eight sampling steps and a sampled total-card peak of 7,500 MiB including the desktop. The remaining time includes CPU encoding, model loads and VAE work; this was not a per-stage profiler. Full-size 896×512 did not complete a first sampling step before a diagnostic stop at 669.775 seconds. These results apply to the exact quantization, software, settings and card here, not all LTX configurations.

The smaller retake reproduces a readable open hand in the middle pose, but has an early pose jump and a ghosted raised arm around global frames 50–55. It **fails production quality**. Both older-model guide trials also fail hand detail/timing. Model execution and correct masking do not establish successful motion repair.

## Matched trial results

| Take | Native pixels | Client elapsed | Result |
|---|---|---|---|
| [LTX-Video 2B standard guide](results/ltxv_guide_standard/assembled.mp4) | 896×512 | 174.911 s | Detached/smeared hand, early lowering; rejected |
| [LTX-Video 2B stronger guide](results/ltxv_guide_strong/assembled.mp4) | 896×512 | 35.533 s, warm cache | More connected arm, still smeared fingers and early lowering; rejected |
| [LTX-2.3 full-size retake receipt](results/ltx23_retake_standard/receipt.json) | Requested 896×512 | 669.775 s | Interrupted before a complete sampling step; no footage |
| [LTX-2.3 low-memory retake](results/ltx23_retake_lowmem/assembled.mp4) | 448×256; review upscaled to 896×512 | 598.178 s, cold | Temporal retake executes; ghost arm and timing fail; rejected |

[Side-by-side footage](comparison/completed_takes.mp4) compares the original rejected take and all three completed trials at the same 81-frame, 24 fps timeline. Failed attempts have receipts, not invented footage. The newer low-memory take changes resolution and server profile, so it is a hardware troubleshooting comparison rather than a controlled model-speed benchmark. Native frames and native-resolution window previews remain available in each result directory.

## Aseprite correction bridge

The [editable guide master](inputs/repair_keys.aseprite) contains complete entry/frame-40, corrected intermediate/frame-48 and exit/frame-64 images. One complete-figure ImageGen redraw supplies the corrected intermediate; Aseprite normalizes its whole canvas and exports complete guides. This is not a hand-painted Aseprite redraw. The [exact ImageGen prompt and reference hashes](environment/imagegen_receipt.json) distinguish the executed request from its earlier draft. Identity/style acceptance of the redraw remains pending.

The [native 25-frame inspection master](results/ltx23_retake_lowmem/repair_window.aseprite) includes original/guide comparison layers, registration landmarks and tags marking the newly observed ghost-arm and boundary defects. Registration permits shoulder, torso/dress, hair and tail movement; no fixed-body or isolated-limb overlay is used.

Use single-frame Aseprite tags `repair_key_0048` or `native_frame_48` to identify a corrected complete-canvas key. Export visible complete-figure layers with:

```text
python -B assets_src/cinematics/ltx_retake_repair_20261004/scripts/export_tagged_keys.py --master inputs/repair_keys.aseprite --output inputs/tagged_exports
python -B assets_src/cinematics/ltx_retake_repair_20261004/scripts/sync_aseprite_keys.py
```

The [actual tagged export](inputs/tagged_exports/tagged_keys.json) records original timeline indices, editable-parent/output hashes and timing. Three guides round-trip with identical RGBA pixels. Create tags after adding frames: Aseprite can extend an existing end tag when appending a frame. The initial tag/export failures and their correction remain in the environment evidence. Edits must express coherent figure-wide motion; a complete-canvas export alone cannot prove that artistic requirement. Extra key tags require bounded selection, not an automatic generation request per key.

## What the temporal retake proves

The job uses source frames 40–64, original defects 44–52, the same midpoint/exit guides, text, seed and cadence. LTX-Video regenerates a guided window from an entry image. LTX-2.3 instead encodes all 25 source frames and regenerates its two middle temporal latent blocks across the whole canvas. This ComfyUI mask-and-guide graph is **not execution of the separate official Python RetakePipeline**. The official [retake source](https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-pipelines/src/ltx_pipelines/retake.py) uses a source-video temporal mask and decodes the full video; its direct signature does not provide this corrected-keyframe guide interface.

The [latent check](results/ltx23_retake_lowmem/latent_mask_verification.json) finds four native temporal blocks. The first/last differ only by at most 2.39×10⁻⁷, while both interior blocks change substantially. Decoded pixels are not guaranteed identical. The review splice therefore retains original complete PNGs outside global 41–63, including frames 40/64; all 58 outside frames remain byte-identical. The splice is explicitly a review derivative, with boundary failures retained. There are no dissolves, interpolation, repeated frames or subject warps.

The first guide jobs and failed full-size newer-model attempt used legacy local input filenames. Aseprite re-export later changed PNG container hashes while preserving decoded RGBA, as [checked](environment/guide_roundtrip.json). The exact container loaded by the overlapping failed attempt is not known; its original and re-export hashes are retained as a provenance limit. The successful low-memory take records per-take immutable [bindings](results/ltx23_retake_lowmem/bindings.json); future bindings are content-addressed. This ambiguity is not presented as accepted production evidence.

The [machine receipt](environment/trial_verification.json) verifies 75 native-frame Aseprite round-trips, original/native hashes, tagged guide exports, exact 24 fps video counts and the outside-window splice. The [visual inspection](environment/review.json) rejects the outputs independently. Owner, normal-speed temporal, device and child acceptance remain outstanding. Native low-resolution softness is separate from the visible transition ghosting; preview upscaling repairs neither.

## Selected next refinement

Keep **Aseprite → complete corrected poses/motion guide → bounded temporal retake → Aseprite inspection** as the preferred repair structure. LTX-2.3 at 448×256 is now a demonstrated 8 GB experimental retake backend, not an accepted final animation engine. LTX-Video 2B remains the faster full-resolution drafting option in this comparison; its source-video temporal-mask [draft graph](briefs/ltxv_temporal_retake_proposed.json) is explicitly unexecuted. No third older-model or third newer-model take was submitted.

The next bounded test should expand clean context to cover temporal VAE blocks (for example source 32–72, 41 frames), with a complete-figure authored guide that shows entry, lowering and follow-through rather than one midpoint plateau. Repair the neighboring contaminated blocks as needed, then inspect exact pose/velocity at both splice boundaries. Broader context is a hypothesis for the observed tearing, not a proved cure. Compare controlled source strength and guide timing; do not retain a bad source merely to preserve its latent block.

For character/object work, also test a measured complete-figure canvas: for example 448×512 around this entire mermaid instead of 896×512 with large empty margins. Preserve every hand, shoulder, dress, hair and tail pose plus a motion margin; use the same declared source crop on all frames and guides, recalculate registration coordinates, and preserve original full canvases. The footprint spends pixels on character detail while retaining figure-wide animation. This proposed portrait-size configuration has not been tested for VRAM, timing or quality; a crop of an isolated limb is excluded. Compare it as a separately declared preparation/profile, not a claimed resolution-equivalent speed result.

Cache unchanged prompt conditioning and encoded source/context by model/VAE/source/prompt/dimension hashes. Future input copies are content-addressed to permit cache reuse without mutable source pixels. A CFG=1 distilled graph can reuse positive conditioning for its zeroed negative input instead of paying for a separate negative text encode; this optimization is proposed, not measured here. The successful trial deliberately used cache-disabled CPU text/VAE and synchronous offload. A warm optimized repeat may be faster, but has not been timed.

The newer [LTX-2.5 8 GB workflow author's benchmark](https://github.com/reventadirecta/LTX-2.5-I2V-8GB-VRAM) uses RTX 4060 Laptop, W4A8 ConvRot, dynamic/asynchronous offload and BF16 VAE. Its 84.58-second report is a different GPU/runtime/quantization and lacks definitive peak-VRAM measurement. Gated weights were not installed or tested here. It remains a separate candidate, not evidence that this PC reaches that speed.

## Cost, provenance and publication

The [job card](briefs/job_card.json) caps four additional generated-take requests, two per backend, six model submissions including diagnostics, one ImageGen call and zero paid API spend. Four generated takes and six queued model requests are used. One additional failed diagnostic-client preflight makes seven model-job attempts under the literal six-attempt field: the cap was exceeded by one, without GPU inference for that failed preflight. Two separate server startup failures/diagnostic aborts are also logged. This process failure is preserved in usage evidence, with no owner exception or budget reset; the runner now blocks diagnostics/client preflights as well as takes. Failed/rejected attempts count. Downloads total 24,185,844,102 bytes, with [pinned revisions and publisher SHA-256](environment/download_receipt.json). Model weights stay in the local tool installation. LTX Community License and [Gemma terms](https://ai.google.dev/gemma/terms) apply; original project-art provenance is inherited.

[Actual usage](environment/usage.json), [environment pins](environment/software_hardware.json), [payload manifest](manifest.json) and [audit impact](../../../design/audit_impacts/ltx-retake-repair-20261004.json) preserve the trial. Cost per accepted second is undefined because accepted production seconds are zero. No runtime finding lifecycle changes; MA-ROSHAN-003 remains deferred and MA-ROSHAN-005 remains open. GitHub publication and anonymous immutable-file verification establish archive delivery only.
