# Day One Mermaid Pool cleanup assets

Generated 2026-08-22 with the built-in OpenAI image-generation tool. The
approved Mermaid Pool plate and fixture cutouts were used as style/identity
references only; no approved source file was modified or overwritten. The
Rumi candidate from this batch was later rejected as the wrong character and
is not present in runtime.

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

Use case: precise-object-edit. Image 1 is the sole identity, silhouette,
proportions, palette, material, outline, viewing-angle, pedestal, and
character-design authority for the existing Mermaid Pool seahorse fountain;
Image 2 supplies only its larger room context and diffuse storybook lighting.
Render that exact established lavender-and-aqua fountain in one dirty, clogged,
sick-looking state. Preserve the long narrow snout, round black eye placement,
lavender scalloped crest, small side fin, aqua-lavender body, cream segmented
belly, tightly curled tail, pink-and-aqua coral base, pearl-paver pedestal,
proportions, and upright three-quarter pose. Remove only the clean water stream.
One clearly visible soggy crumpled pink paper wrapper is wedged sideways in and
protrudes from the mouth/nozzle, with a short soft olive seaweed strand tangled
around it; the trash must read instantly at phone size as the cause of the clog
and not as a tongue, wound, food, sharp object, cigarette, or body part. Limit
growth to three calm clusters: algae on part of the crest/back, two broad
seaweed ribbons around belly/tail, and grime on the pedestal. Preserve the
face, full silhouette, belly, curl, coral base, and pedestal. Match the approved
matte high-key 2D storybook/cel painting: broad rounded masses, two or three
broad value bands, clean deep-indigo/plum contours, sparse interior lines,
diffuse front-above lighting, and restrained wet accents. Exactly one complete
cutout on genuine alpha; no redesigned living seahorse, water stream, extra
animal/limbs/horn/eyelashes/jewelry, background, floor, shadow, glow, aura,
vignette, text, logo, watermark, PBR texture, photographic algae, horror, or
injury.

The initial 2026-08-22 sick-state master redesigned the fountain as a different
living seahorse and omitted the required mouth blockage. It is rejected and
retained only as evidence at
`rejected/seahorse_sick_wrong_identity_native.png`; it is not a runtime
fallback. The corrected generation initially returned a baked checkerboard, so
a background-extraction-only pass removed that checkerboard while preserving
the accepted subject pixels. A later candidate preserved the mouth blockage but
invented a small forehead horn; that candidate was rejected, the horn alone was
removed against the canonical clean fountain, and the resulting checkerboard
was again extracted without admitting it to runtime. The selected hornless
master is verified RGBA with alpha extrema 0–255.

### Rejected `rumi_wrong_identity_native.png`

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

This generation did not match the owner's established Rumi/Violet identity.
It is retained only as rejected evidence at
`rejected/rumi_wrong_identity_native.png` and is never a runtime fallback.
The pool now reuses the approved private-canon Rumi identity and authored
animation family recorded in
`assets_src/characters/rumi_2026-08-22/PROVENANCE.json`.

## Runtime mapping

| Native master | Runtime asset | Normalization |
|---|---|---|
| `pool_algae_trash_native.png` | `assets/castle/day_one_pool/pool_algae_trash.png` | 1536×1024 to 1024×682 RGBA |
| `waterfall_growth_native.png` | `assets/castle/day_one_pool/waterfall_growth.png` | portrait to 1024px high RGBA |
| `pool_rim_grime_native.png` | `assets/castle/day_one_pool/pool_rim_grime.png` | 1536×1024 to 1024×682 RGBA |
| `seahorse_sick_native.png` | `assets/castle/day_one_pool/seahorse_sick.png` | 1199×1312 to 936×1024 RGBA |

The first waterfall-growth attempt returned an RGB checkerboard instead of
alpha. It was rejected and is not stored in the repository; the selected
master is the corrected background-extraction result.
