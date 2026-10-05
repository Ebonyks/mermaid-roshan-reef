# LTX-2.5 next-candidate preflight

The owner asks why the fallback is 2.3 when 2.5 is available. 2.3 was already
installed and had completed a smaller temporal retake; it is a baseline,
not a finding that 2.3 is visually superior.

Lightricks reports improved distilled consistency, a new diffusion decoder
and a matching custom Gemma 4 encoder. These are relevant to the current
smear/detail problem, so 2.5 is the next quality candidate.
[Official model card](https://huggingface.co/Lightricks/LTX-2.5).
Lightricks' current pipeline docs explicitly show a single-stage 2.5 retake
with matching split components. The Desktop sources conflict: release v1.2.5
claims local 2.5 Retake/Extend, while current pinned capability flags and tests
still reject both for 2.5. Treat the Desktop integration as unresolved; this
is not a model-wide reason to prefer 2.3. The framework retake path and our
quantized Comfy implementation still need an actual 8 GB execution test.
[Official retake example](https://github.com/Lightricks/LTX-2/blob/9ec55f9f22798a3198d9c923856824821bc3317e/packages/ltx-pipelines/docs/hdr.md),
[release claim](https://github.com/Lightricks/LTX-Desktop/releases/tag/v1.2.5),
[pinned capability flags](https://github.com/Lightricks/LTX-Desktop/blob/68cd86c15e5fd25f56229ea63c0dbcb0338f7812/backend/runtime_config/ltx_capabilities.py).

The 2.5 pipeline also offers generated interior keyframe slots, each allocating
one latent frame of tokens to one pixel frame instead of eight. This is a
relevant refinement experiment for fast hand travel after the base graph fits.
It generates extra detail-bearing frames; it does not make supplied pose guides
hard locks. Additional slots increase tokens/attention cost and are not yet
implemented or benchmarked in this project's Comfy graph.
[Official slot semantics](https://github.com/Lightricks/LTX-2/blob/9ec55f9f22798a3198d9c923856824821bc3317e/packages/ltx-pipelines/docs/conditioning.md).

A community 8 GB baseline is now published, narrowing the earlier claim to
"untested on this PC." It uses W4A8 ConvRot transformer and matching Gemma 4,
BF16 DiffVAE, learned spatial upscale, 8+3 steps and dynamic/asynchronous
offload on Comfy 0.34.3 / RTX 4060 Laptop. The reported 84.58 s run is
512×256/73 frames; it is not a portrait or Roshan benchmark and has no valid
peak-VRAM receipt. Its authors explicitly distinguish it from the unsuccessful
FP16 decode and disabled-offload configuration.
[Immutable baseline](https://github.com/reventadirecta/LTX-2.5-I2V-8GB-VRAM/tree/ab9b61ef01af3c5f43d8b530ded87a66337c5afe).

The four exact files total 23.835 GiB. The two official decoder/upscaler
HEAD requests returned 401 GatedRepo without authentication. No 2.5 weights
were downloaded and no contact-sharing/access terms were accepted for the
owner. Current Comfy has Gemma 4 code. A tiny synthetic W4A8 INT8-activation
linear ran successfully through the installed native CUDA backend on this
RTX 3060 Ti (SM 8.6); full model loading, memory, speed, motion and retake
compatibility still need validation.
The installed 2.3 Gemma 3 encoder and decoder cannot substitute for this pack.

Next bounded test: resolve official access; pin a separate compatible runner
and exact four components; first validate the published small two-pass recipe
without its disabled prompt enhancer/audio export. Then bind this packet's
same complete-figure guides, action timing and seed at the matched comparison
canvas. Preserve native first/refined frames and Aseprite masters; separately
test temporal retake masks and boundary preservation. Never infer crisp
hands or a usable retake from the version number or a different GPU's speed.
The current trial's 1 GB new-model-download cap is unchanged; no silent
25 GB installation or additional inference batch is commissioned by a question.
