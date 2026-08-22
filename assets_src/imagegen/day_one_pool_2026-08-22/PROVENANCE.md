# Day One Mermaid Pool cleanup assets

Generated 2026-08-22 with the built-in OpenAI image-generation tool. The
approved Mermaid Pool plate and fixture cutouts were used as style/identity
references only; no approved source file was modified or overwritten. Rumi
uses the approved Roshan cutout only as an art-family and scale reference and
is deliberately a distinct character.

Selected native masters are retained in this directory. Runtime copies under
`assets/castle/day_one_pool/` were normalized non-destructively with FFmpeg
8.1.2 to a maximum 1024-pixel edge with RGBA preserved.

## Selected prompt set

### `pool_algae_trash_native.png`

Use case: stylized-concept. Asset type: production transparent Sprite2D
cutout for a preschool touch-cleaning minigame. Image 1 is the approved
Mermaid Pool room and sole style reference; do not edit or return the room.
Create one broad, child-readable removable cluster of dirty pool-surface
pollution: soft olive-green algae mats, three curled strands of seaweed, one
crumpled paper wrapper, one small tin cup, two harmless floating leaves, and a
few murky bubbles, grouped as one coherent tap target. Match the approved
rounded storybook forms, dark-violet variable outlines, broad painted value
bands, pearl highlights, and pastel toy-playset finish. Isolated wide low
cluster with genuine transparent alpha; no room, floor, character, animal,
text, logo, watermark, sharp glass, sewage, photorealism, or 3D rendering.

### `waterfall_growth_native.png`

Use case: stylized-concept, followed by background-extraction correction.
Image 1 is the approved rainbow-waterfall fixture; Image 2 is the room style
reference. Create one tall removable curtain of dirty fountain growth:
dangling olive seaweed ribbons, mossy algae clumps, dull brown-green mineral
grime, three stuck leaves, and murky droplets. Loosely echo a scallop-shell
fountain silhouette without including or repainting the fixture. Match the
approved polished 2D storybook style. The correction changed only the baked
checkerboard background to genuine alpha and preserved the complete growth
artwork. No fountain, rainbow stream, room, character, text, logo, watermark,
photorealism, or 3D rendering.

### `pool_rim_grime_native.png`

Use case: stylized-concept. Asset type: production transparent Sprite2D
cutout for a preschool touch-cleaning minigame. Image 1 is the approved room
style reference. Create one removable pool-rim trash and grime cluster: a soft
olive slime smear, two small soggy paper scraps, one harmless rounded bottle
cap, one faded ribbon loop, one tiny shell-shaped scrub sponge, dead seaweed
bits, and four dull bubbles. Keep it distinct from the floating algae mat and
match the approved rounded, dark-violet-outlined storybook finish. Isolated
low horizontal single tap target with genuine alpha; no room, floor, rim,
character, animal, text, logo, watermark, sharp glass, sewage, photorealism,
or 3D rendering.

### `seahorse_sick_native.png`

Use case: precise-object-edit. Image 1 is the exact approved seahorse fountain
identity reference; Image 2 is the room style reference. Create the same
lavender-aqua seahorse fountain in a clearly sick, clogged state. Preserve its
species, crest, snout, curled tail, proportions, identity colors,
pearl-and-coral pedestal, outline, and three-quarter pose. Remove the healthy
water stream. Add a gentle tired expression, muted color, olive seaweed around
belly and tail, soft algae on crest and pedestal, two leaves, and dull murky
bubbles. Keep the face visible, sympathetic, and child-safe. Full-body genuine
transparent cutout; no redesign, extra limbs, injury, medicine, text, logo,
watermark, photorealism, or 3D rendering.

### `rumi_violet_native.png`

Use case: stylized-concept. Image 1 is the approved Roshan cutout and only a
style/scale reference; Image 2 is the room palette reference. Create Rumi, a
new friendly young mermaid: long deep-violet hair with lavender highlights,
warm medium-brown skin, kind teal eyes, a pearl-and-violet-shell hair clip,
sea-glass-lavender top, and one violet-to-plum tail with restrained aqua
speckles and pale lavender fins. Grateful expression, one hand over her heart,
one hand waving. No crown or prop. Match the project's polished 2D storybook
character family while keeping her clearly distinct from Roshan. Exactly one
full-body character with genuine alpha; no room, pool, extra limbs, split
tail, legs, text, logo, watermark, photorealism, or 3D rendering.

## Runtime mapping

| Native master | Runtime asset | Normalization |
|---|---|---|
| `pool_algae_trash_native.png` | `assets/castle/day_one_pool/pool_algae_trash.png` | 1536×1024 to 1024×682 RGBA |
| `waterfall_growth_native.png` | `assets/castle/day_one_pool/waterfall_growth.png` | portrait to 1024px high RGBA |
| `pool_rim_grime_native.png` | `assets/castle/day_one_pool/pool_rim_grime.png` | 1536×1024 to 1024×682 RGBA |
| `seahorse_sick_native.png` | `assets/castle/day_one_pool/seahorse_sick.png` | 1104×1425 to 794×1024 RGBA |
| `rumi_violet_native.png` | `assets/castle/day_one_pool/rumi_violet.png` | 1024×1536 to 682×1024 RGBA |

The first waterfall-growth attempt returned an RGB checkerboard instead of
alpha. It was rejected and is not stored in the repository; the selected
master is the corrected background-extraction result.
