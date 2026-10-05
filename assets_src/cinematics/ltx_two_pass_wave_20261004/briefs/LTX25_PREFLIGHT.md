# LTX-2.5 next-candidate preflight

The owner asks why the fallback is 2.3 when 2.5 is available. 2.3 was already
installed and had completed a smaller temporal retake; it is a baseline,
not a finding that 2.3 is visually superior.

Lightricks reports improved distilled consistency, a new diffusion decoder
and a matching custom Gemma 4 encoder. These are relevant to the current
smear/detail problem, so 2.5 is the next quality candidate.
[Official model card](https://huggingface.co/Lightricks/LTX-2.5).
The official Desktop feature table offers local Retake/Extend with 2.3 but
not its 2.5 integration. That app limitation does not establish a model-wide
ban on Comfy temporal masking.
[Official Desktop](https://github.com/Lightricks/LTX-Desktop).

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
owner. Current Comfy has Gemma 4 code, but the workflow/runtime and
RTX 3060 Ti W4A8 kernel compatibility still need validation.
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
