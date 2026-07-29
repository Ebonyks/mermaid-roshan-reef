# Sky Lagoon fireplace-smoke generation ledger

All art in this folder is project-original output from OpenAI built-in image
generation. No external reference assets were used. Runtime processing used
`tools/extract_connected_chroma.py` for border-connected background removal
and FFmpeg Lanczos scaling for the accepted 46×256 RGBA card.

## Attempt 1 — rejected puff prototype

Mode: built-in image generation, new bitmap.

Prompt:

> Use case: stylized-concept. Asset type: transparent Sprite3D smoke-puff
> card for the Mermaid Roshan Sky Lagoon game. Create one small discrete
> storybook chimney-smoke puff, suitable for three staggered copies rising
> above a distant cozy mountain cabin. Use a perfectly flat solid #ff00ff
> chroma-key background. The subject is a compact rounded puff made from
> three to five soft cloudlike lobes, readable at phone scale, in the
> hand-painted Sky Lagoon palette with warm-grey body and lavender-grey
> underside. No chimney, cabin, scenery, shadow, glow, text, particles,
> duplicate puffs, or border-touching marks.

Rejected because the in-engine result read as a detached cloud/thick puff.

- chroma 1254×1254:
  `84886ebb37dab5d1d44070dae6362d48beab1b67e14959df1a62390f190f63d9`
- alpha 1254×1254:
  `1f65ba9fd936d2896224102e610086adc85d4a7fb25b246b6dee930314696ebe`

## Attempt 2/3 — rejected pale wisp v1

Mode: built-in image generation, new bitmap.

Prompt:

> Use case: stylized-concept. Create a narrow transparent Sprite3D
> chimney-smoke wisp: very thin and tall, beginning at a tiny base, rising
> through two gentle S-shaped curls, and breaking finer at the top. Maximum
> width about 18 percent of the canvas and height about 75 percent. Use
> hand-painted storybook lavender-grey/warm-grey cel color on a uniform
> #ff00ff chroma background. No detached puff, broad mass, chimney, cabin,
> landscape, cloud, shadow, glow, text, or extra particles.

Rejected in context because the value edge disappeared against the bright sky.

- chroma 1024×1536:
  `de85388498d4b9140797112445c1fa6c78c1e55c66531454356ee953b8a11958`
- alpha 1024×1536:
  `e850a41ae6ad18383860d58145101200f775b476bdc85f992d46401cf860b221`

## Attempt 4 — accepted wisp v2

Mode: built-in image generation, image edit using v1 as the sole reference.

Prompt:

> Preserve the provided tall, narrow, graceful S-ribbon and uniform #ff00ff
> chroma background. Keep it a thin fireplace wisp, never a cloud, broad
> plume, puff, explosion, steam column, or fog. Strengthen readability against
> cyan sky with a medium lavender-grey interior, narrow deep blue-lavender
> baked edge, and restrained warm-grey highlight below #e8e1dd. Preserve the
> hair-thin bottom attachment, two curls, broken top taper, generous padding,
> and mostly negative space. No transparency effects, glow, shadow, chimney,
> cabin, scenery, text, watermark, duplicates, or border marks.

- chroma 1024×1536:
  `6306b2e2e26498321970e316baeefb803ecd76917d9e6f5d0151d5d3a6a4665f`
- alpha crop 246×1363:
  `ae841d7e3c2d2ec72949409d2067b45c37c6785f3043646dd234c5f46561d42d`
- runtime 46×256:
  `ff0c49869ff0152323282b0228c2f76494ad2381ba64c0e535a68c8bc229e007`

The accepted runtime path is
`assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png`.
