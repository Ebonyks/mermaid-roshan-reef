# Blur repair methods checked 2026-10-04

Supporting source-study research; no new output acceptance. Owner requested
more resources and continued testing.

| Method | Evidence and disposition |
|---|---|
| LTX-specific NAG | Executed locally with actual negative attention; finger tearing remains. Optional, not default for this wave. |
| Higher temporal density | 81 frames at 48 fps, same action duration/poses/seed. Mid-lowering key clearer, neighboring figure still smeared. |
| Official Refine Details IC-LoRA | Best next bounded repair candidate: frame-aligned video detail reconstruction. Separate gate pending; quantized execution unproven. |
| Full DFR | Official generated-keyframe plus spatial-detailing pipeline; extra compute/VRAM. Ordinary 8+3 is not full DFR. Not run. |
| Community de-rope | Slow repeated inputs, regeneration, exact clock recovery. Alpha large LTX tests peak 59–60 GiB. No local or 8 GB execution claim. |
| Decoder/export diagnosis | 2.5 diffusion decoder confirmed; single-image key fingers readable. Native moving PNGs already fail before MP4. No decoder-multistep test claimed. |

Primary sources and executable pins:

- [Refine Details checkpoint](https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Refine-Details/tree/4912c478b35dd96b6cdcc5f7c7ff9d72c2c57929):
1,308,787,534 bytes; SHA 771a84f70e143af89867fc714ebbf7bd6edcaa4974c0360cba4a2d292a99f0e6.
Portrait 576x1024 (landscape 1024x576) training tile; 8 distilled steps, Euler,
CFG 1, LoRA 1, aligned clip reference downscale 1. Keep painted direction; do not
copy the photographic grain or negative 'painting' from its examples.
- [Official refinement guide](https://docs.ltx.io/open-source-model/vfx-post-production/refine-and-restore):
rebuilt detail is generative, not guaranteed source identity/anatomy recovery.
- [Official node source](https://github.com/Lightricks/ComfyUI-LTXVideo/tree/3bf3ca62595f1764c47d01c35c8e5dfe47e1a88f):
six required modules/license and a declared minimal initializer only;
no HDR/API/prompt-enhancer imports or additional dependencies.
- [Official DFR](https://github.com/Lightricks/LTX-2/tree/9ec55f9f22798a3198d9c923856824821bc3317e):
extra generated keys plus detailing IC-LoRA; optional temporal upscaler.
- [Community de-rope](https://github.com/matlowai/ComfyUI-MAINodes/blob/91311b3db6f10cac399ba05c71ce1e6c81f28064/DEROPE_ANY_MODEL.md):
8/16-frame holds respond to LTX's temporal compression in the pinned flat-clock
experiments. Its large-memory recipe is not an 8 GB solution.

## Prepared adapter test

One candidate after access approval: use all 41 native base frames unchanged,
add 96 pixels above and below through Aseprite to 576x1024, no resize; trained portrait tile,
whole-clip guide at downscale 1, 8 official distilled steps, Euler, CFG 1, LoRA 1.
Keep padded source mapping and every output. No isolated limb mask, sharpening
prefilter, photographic grain or 4K expansion. Proposed until queue/receipt
prove execution.

Total generation cap 5 includes the earlier 3, one temporal-density take and at
most one named official detail test. Gated download failures remain recorded.
Existing 28 GB download/wall caps remain; base plus adapter 27,266,271,558bytes.
