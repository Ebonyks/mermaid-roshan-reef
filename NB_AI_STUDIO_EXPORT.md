# Nano Banana Batch Export — Google AI Studio
_2026-07-13 · companion to `ART_STYLE_GUIDE.md`, `ART_GENERATION_BATCH_01.md`,
`TEXTURE_SOURCE_AUDIT.md`, `ART_STYLE_AUDIT.md`_

Every prompt below is **self-contained**: copy one code block, paste it as a
single message in Google AI Studio, generate, download. No shared system
prompt is needed.

## How to run the batch

1. In Google AI Studio pick the image model (**Nano Banana / Gemini 2.5 Flash
   Image**). Set output aspect **1:1** for everything except the sky panorama
   (16:9 or 2:1).
2. One prompt = one asset. Use a **fresh chat per asset** so styles don't
   drift — EXCEPT matched animation frames (butterflies): generate the
   wings-open frame first, then in the SAME chat ask for the half-folded frame
   so registration, colors and species stay identical.
3. Save each result to **Downloads** named as the `File:` line says. Claude
   picks new art up from Downloads automatically (project file-search rule),
   verifies it against the style guide, keys out the background / checks tile
   seams, and installs it.
4. This is a **review batch**: nothing overwrites a runtime asset until the
   owner approves it side-by-side at in-game size.
5. Character / family art is **excluded** — that pipeline requires the owner
   reference images plus `gen2/prompts/style_transfer_v10.14.md` and is not a
   text-only batch.

## Formatting + styling rules distilled (what worked, what didn't)

**Winning style language** (from the successful gen2 generations and the
2026-07-13 `ART_STYLE_GUIDE.md`): *flat-color anime cel* — thin dark-indigo
contour, two or three broad flat value bands, high-key colors, aqua/lavender
shadows. This is the block baked into every prop prompt below.

**Retired style language**: the older `NB_TEXTURE_PLAN.md` "children's
storybook watercolor" block. It produced sand that read as cracked dirt and
soft mush that fought the cel look. Tiles below use *painted flat regions with
restrained grain*, not watercolor.

**Hard format contracts** (each encoded in the prompts):

- **Props/creatures**: ONE object, solid flat chroma-key background, complete
  anatomy, no ground island, no cast shadow, no neighbors, no particles, no
  frame. Key color is chosen per asset to avoid its own palette (magenta for
  green/plant assets, green for pink/lavender assets).
- **Surface tiles**: seamless four-edge tiling, square, orthographic, flat even
  light, and the owner's **blank-canvas rule** — no corals, moss, flowers,
  shells, pebble clusters or creatures baked into a surface that the game
  dresses with real 3D props.
- **Wrap sheets** (for baking onto GLBs): edge-to-edge material close-up,
  evenly lit, no perspective, seamless preferred.
- **Everything**: no photorealism, no black shadows, no white sticker rim, no
  glossy plastic, no text/watermark/vignette. Max useful side 1024px.

---

# SECTION A — Isolated props & creatures (Batch 01, prompts written)

The 36 review assets planned in `ART_GENERATION_BATCH_01.md`.

### A01 — Monarch butterfly, wings open
File: `monarch_open.png` · Role: dorsal animation frame · Key: magenta
```
A monarch butterfly with wings fully open, seen from directly above (dorsal view). Complete anatomy: four wings — longer triangular forewings, rounder hindwings — with the thorax, abdomen and two antennae visible between them. Warm orange wing cells, deep-brown veins, cream spots along dark wing margins; vein pattern sparse and loosely mirrored, not mechanical. An elegant natural animal, not a mascot: no face, no smile, no rainbow panels. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, fine thin dark-indigo contour, two or three broad flat value bands, high-key colors, gentle friendly mood. One single isolated butterfly centered on a solid flat pure magenta background (#FF00FF), no ground, no cast shadow, no plants, no particles, no frame. Square 1:1. No photorealism, no gritty detail, no dramatic dark shadows, no thick white sticker outline, no glossy plastic, no watercolor wash shading, no text, no watermark, no vignette.
```

### A02 — Monarch butterfly, wings half-folded
File: `monarch_half.png` · Generate in the SAME chat as A01
```
The exact same monarch butterfly, same colors, same size, same dorsal camera — now with both wing pairs half-folded, raised at roughly 45 degrees. The complete body, both left and right wings, and both antennae must still be fully visible (do not imply the far wing by mirroring). Same flat-color anime cel style, thin dark-indigo contour, flat value bands. Single isolated butterfly centered on a solid flat pure magenta background (#FF00FF), no shadow, no scenery, square 1:1. No photorealism, no soft airbrushing, no text, no vignette.
```

### A03 — Blue butterfly, wings open
File: `bluemorpho_open.png` · Key: magenta
```
A blue morpho-style butterfly with wings fully open, seen from directly above (dorsal view). Complete anatomy: four wings, thorax, abdomen and two antennae visible. Saturated blue-violet wing fields with dark margins and a few pale edge spots; sparse loosely mirrored vein pattern. An elegant natural animal, not a mascot: no face, no smile. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, fine thin dark-indigo contour, two or three broad flat value bands, high-key colors, gentle friendly mood. One single isolated butterfly centered on a solid flat pure magenta background (#FF00FF), no ground, no cast shadow, no plants, no particles, no frame. Square 1:1. No photorealism, no dramatic dark shadows, no white sticker outline, no glossy plastic, no watercolor wash shading, no text, no vignette.
```

### A04 — Blue butterfly, wings half-folded
File: `bluemorpho_half.png` · Generate in the SAME chat as A03
```
The exact same blue butterfly, same colors, same size, same dorsal camera — now with both wing pairs half-folded, raised at roughly 45 degrees. Complete body, both wings and both antennae fully visible. Same flat-color anime cel style, thin dark-indigo contour. Single isolated butterfly centered on a solid flat pure magenta background (#FF00FF), no shadow, no scenery, square 1:1. No photorealism, no soft airbrushing, no text, no vignette.
```

### A05 — Stag beetle
File: `beetle_stag.png` · Key: magenta
```
A stag beetle in top-down view: head, thorax and wing-case abdomen as three clearly readable masses, broad branched mandibles, six legs, two antennae. Dark warm brown with restrained bronze accents; highlights are narrow cel shapes, never chrome. Museum-observational but simplified for a phone screen: thin dark-brown contour, a few anatomical joint lines, no eyes with pupils, no smile, no cartoon face. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, two or three broad flat value bands, friendly non-threatening presence. One single isolated beetle centered on a solid flat pure magenta background (#FF00FF), no ground, no shadow, no scenery. Square 1:1. No photorealism, no gritty microtexture, no horror, no glossy plastic, no text, no vignette.
```

### A06 — Ladybird beetle
File: `beetle_ladybird.png` · Key: magenta
```
A ladybird beetle in top-down view: small black head, domed red wing case with a visible center split and a few black spots, six short legs, two short antennae. Complete readable anatomy, simplified for a phone screen: thin dark contour, narrow cel highlight, no cartoon face, no pupils, no smile. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, two or three broad flat value bands, friendly non-threatening presence. One single isolated beetle centered on a solid flat pure magenta background (#FF00FF), no ground, no shadow, no scenery. Square 1:1. No photorealism, no glossy plastic shine, no text, no vignette.
```

### A07 — Green jewel beetle
File: `beetle_jewel.png` · Key: magenta
```
A jewel beetle in top-down view: compact oval bottle-green wing case with restrained blue iridescent accents, small head, six legs, two antennae. Iridescence rendered as two or three flat cel color bands, not chrome reflections. Thin dark-indigo contour, no cartoon face, no pupils, no smile. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, museum-specimen accuracy simplified for a phone screen. One single isolated beetle centered on a solid flat pure magenta background (#FF00FF), no ground, no shadow, no scenery. Square 1:1. No photorealism, no metallic gloss, no text, no vignette.
```

### A08 — Pale mint border coral
File: `coral_border_mint.png` · Key: magenta
```
A single isolated branching coral silhouette with rounded finger ends, in muted mint-grey with a fine blue-grey contour. This is quiet graphic page-framing art: flat, low-saturation, calm, with at most two soft value bands — flatter and quieter than an interactive prop. One coral only: no shells, no pebbles, no seabed, no second species, no scene. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no ground patch, no cast shadow. Square 1:1. No photorealism, no painterly bouquet, no gradients, no text, no vignette.
```

### A09 — Coral-blush border coral
File: `coral_border_blush.png` · Key: green
```
A single isolated branching coral silhouette with rounded finger ends, in soft coral blush with a fine muted plum contour. Quiet graphic page-framing art: flat, low-saturation, calm, at most two soft value bands. One coral only: no shells, no pebbles, no seabed, no second species. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure green background (#00FF00), no ground patch, no cast shadow. Square 1:1. No photorealism, no gradients, no text, no vignette.
```

### A10 — Lavender branching scene coral
File: `coral_scene_lavender.png` · Key: green
```
A branching coral for an immersive reef scene, dominant dusty-lavender hue, built from layered flat silhouettes: a clear front branch group, one cool blue-grey shadow plane, and a restrained rear mass. Rounded finger ends, thin dark-indigo contour, three broad cel value bands, richer than page-border coral but still calm. One coral specimen only: no rocks, no sand island, no shells, no kelp, no fish. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, high-key underwater colors. Centered on a solid flat pure green background (#00FF00), no ground, no cast shadow. Square 1:1. No photorealism, no dense painterly bouquet, no text, no vignette.
```

### A11 — Coral-pink mound coral
File: `coral_scene_pinkmound.png` · Key: green
```
A low mound coral for an immersive reef scene, dominant warm coral-pink hue, built from broad rounded cel planes with a soft aqua shadow side and a pale cream top light. Simple bumpy dome silhouette with grouped, countable lobes — not noisy. One coral specimen only: no rocks, no sand, no shells, no neighbors. Thin dark-indigo contour, three broad flat value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, high-key underwater colors. Centered on a solid flat pure green background (#00FF00), no ground, no cast shadow. Square 1:1. No photorealism, no microtexture, no text, no vignette.
```

### A12 — Rounded leafy garden bush
File: `bush_round.png` · Key: magenta
```
A rounded leafy garden bush with a clear readable outer silhouette built from grouped leaf clusters, fresh spring green with a cool sage shadow plane and a pale top light. Leaves grouped into broad clumps, not evenly scattered noise. A terrestrial garden plant: absolutely no coral, no shells, no seabed stones, no pot. One bush only, growing from a single base point so it can be reused and mirrored. Thin dark-indigo contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, gentle friendly mood. Centered on a solid flat pure magenta background (#FF00FF), no ground patch, no cast shadow. Square 1:1. No photorealism, no watercolor wash, no text, no vignette.
```

### A13 — Woody leafy shrub
File: `bush_woody.png` · Key: magenta
```
A woody garden shrub with a visible trunk and readable branch fork pattern, leaves attached in distinct clusters along the branches — not one undifferentiated blob. Warm chestnut-brown wood, fresh green leaf clusters with a cool shadow plane each. Terrestrial garden plant: no coral, no shells, no pot, no ground. One shrub only, single base point. Thin dark-indigo contour, flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no watercolor wash, no text, no vignette.
```

### A14 — Orange flowering shrub
File: `shrub_flower_orange.png` · Key: magenta
```
A garden shrub in bloom with sparse apricot-orange blossoms — few enough that the green leaf clusters and branch structure still read clearly. Blossoms are simple five-petal shapes in small deliberate groups. Terrestrial garden plant: no coral, no shells, no pot, no butterflies, no ground. One shrub only, single base point. Thin dark-indigo contour, two or three flat cel value bands, high-key colors. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no dense flower carpet, no text, no vignette.
```

### A15 — Coral-red flowering shrub
File: `shrub_flower_coralred.png` · Key: magenta
```
A garden shrub in bloom with sparse coral-red blossoms in small deliberate groups, green leaf clusters and branch structure still clearly readable. Simple rounded five-petal flower shapes. Terrestrial garden plant: no coral animals, no shells, no pot, no ground. One shrub only, single base point. Thin dark-indigo contour, two or three flat cel value bands, high-key colors. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no dense flower carpet, no text, no vignette.
```

### A16 — Rosette succulent
File: `succulent_rosette.png` · Key: magenta
```
A rosette succulent viewed from a slight three-quarter angle: thick overlapping fleshy leaves arranged around a clear center rosette, sea-glass mint green with a soft blue-grey shadow band and pale leaf-tip accents. Terrestrial plant: no pot, no coral, no pebbles, no soil island. One plant only. Thin dark-indigo contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no waxy gloss, no text, no vignette.
```

### A17 — Paddle cactus with sparse buds
File: `cactus_paddle.png` · Key: magenta
```
A paddle cactus (prickly-pear habit) built from a few broad flat oval pads stacked with mild asymmetry, muted leaf-sage green with a cool shadow plane per pad, tiny restrained dot marks instead of sharp spines, and two or three small coral-blush buds along the top edges. Friendly and non-threatening. Terrestrial plant: no pot, no sand, no coral, no ground. One cactus only, single base point. Thin dark-indigo contour, flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no sharp needles, no text, no vignette.
```

### A18 — Aloe plant
File: `aloe.png` · Key: magenta
```
An aloe plant: long thick tapered blades rising from a central rosette, gentle outward S-curves, sea-glass green with a cooler shadow side per blade and very restrained pale edge marks. Terrestrial plant: no pot, no soil island, no coral, no shells. One plant only, single base point. Thin dark-indigo contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no spiky threat, no text, no vignette.
```

### A19 — Snake plant
File: `snakeplant.png` · Key: magenta
```
A snake plant (sansevieria habit): upright sword-shaped leaves with gentle taper and slight lean, deep leaf-green with quiet pale banding rendered as two or three flat tones per leaf and a soft cream edge accent. Terrestrial plant: no pot, no soil, no coral. One plant only, single base point, countable leaves (five to seven). Thin dark-indigo contour, flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no busy stripe noise, no text, no vignette.
```

### A20 — Small broadleaf tree
File: `tree_broadleaf.png` · Key: magenta
```
A small broadleaf garden tree: visible chestnut-brown trunk with a readable fork pattern, foliage built from a few broad grouped leaf clusters along the branches — a clear silhouette, not a green lollipop and not an undifferentiated blob. Fresh green canopy with one cool sage shadow plane per cluster and a pale top light. Terrestrial plant: no coral, no shells, no ground island. One tree only, single trunk base. Thin dark-indigo contour, flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no watercolor wash, no text, no vignette.
```

### A21 — Small pine tree
File: `pine_small.png` · Key: magenta
```
A small pine tree with a readable warm-brown trunk and a tiered branch silhouette — distinct overlapping branch layers with soft rounded tips, not a perfect smooth cone. Deep reef-green needles rendered as broad flat clusters with a cool blue-green shadow plane per tier. No snow on this version. One tree only, single trunk base, no ground. Thin dark-indigo contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no needle-level detail, no text, no vignette.
```

### A22 — New seedling
File: `seedling.png` · Key: magenta
```
A tiny new seedling: one slim pale-green stem with two simple rounded leaves just unfurling, and one smaller center sprout leaf. Fresh hopeful spring green with a single soft shadow tone. No pot, no soil mound, no ground patch — the sprout alone, single base point. Thin dark-indigo contour, two flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, gentle friendly mood. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no text, no vignette.
```

### A23 — Pink watering can
File: `wateringcan_pink.png` · Key: green
```
A garden watering can in soft rose pink: classic functional silhouette with a round body, curved spout ending in a sprinkler rose head, top handle and side handle. Simplified real object — one or two construction details (a body seam, a rim band), matte painted finish. No face, no water, no plants, no ground. One object only. Thin dark-indigo contour, two or three flat cel value bands, small pale cream highlight. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure green background (#00FF00), no cast shadow. Square 1:1. No photorealism, no metallic chrome, no glossy plastic, no text, no vignette.
```

### A24 — Lamb plush (toy-family calibration)
File: `plush_lamb.png` · Key: magenta
```
A soft lamb plush toy sitting in a resting pose: large head-to-body ratio, short stubby limbs, drooping soft ears, cream fleece rendered as a few broad rounded clumps with a quiet soft edge — never photoreal fur strands. Only the seams needed to explain its construction, simple stitched face with tiny closed-content eyes, warm blush cheeks. A toy, cozy and huggable. One plush only, no blanket, no other toys, no ground. Thin warm brown-black contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no felt microtexture, no text, no vignette.
```

### A25 — Bear plush (toy-family calibration)
File: `plush_bear.png` · Key: magenta
```
A soft teddy bear plush sitting in a resting pose: large head-to-body ratio, short stubby limbs, round ears, warm honey-brown fabric with a cream muzzle and belly patch, fur grouped into broad soft clumps — never photoreal strands. Minimal construction seams, simple stitched nose and small friendly eyes. One plush only, no other toys, no ground. Thin warm brown-black contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no felt microtexture, no text, no vignette.
```

### A26 — Child-made paper cat craft (craft-family calibration)
File: `craft_paper_cat.png` · Key: magenta
```
A child-made paper craft of a cat: cut colored paper shapes glued together with charming imperfect symmetry, slightly uneven scissor edges, visible glued-on pieces (round paper eyes, a triangle nose, strip whiskers), one small pom-pom detail, and a hint of uneven pencil mark. Its charm comes from handmade construction, not professional vector polish. One craft object only, flat-on view, no table, no scissors, no glue bottle, no scattered supplies. Soft warm paper colors in small deliberate groups. Mermaid Roshan children's game asset, clean flat-color illustration with a thin warm contour. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no perfect vector symmetry, no text, no vignette.
```

### A27 — Matte purple round ornament
File: `orn1_purple_round.png` · Key: green
```
A round Christmas ornament in matte jewel violet with a small simple silver cap and loop: one crisp pale highlight shape and one cool lavender shadow band — painted glass, not chrome, not airbrushed gloss. One ornament only, hanging straight, no ribbon, no tree, no snow. Thin dark-indigo contour, broad flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure green background (#00FF00), no cast shadow. Square 1:1. No photorealism, no mirror reflections, no text, no vignette.
```

### A28 — Rose ribbed finial ornament
File: `orn2_rose_finial.png` · Key: green
```
A vintage ribbed finial Christmas ornament in soft rose berry: a ribbed onion-dome body tapering to an elegant point, small simple cap and loop. Ribs rendered as a few broad alternating value bands, one crisp pale highlight, one cool shadow band — painted glass, not chrome. One ornament only, hanging straight, no ribbon, no tree. Thin dark-indigo contour, flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure green background (#00FF00), no cast shadow. Square 1:1. No photorealism, no mirror reflections, no text, no vignette.
```

### A29 — Pearl-blue round ornament
File: `orn3_pearlblue_round.png` · Key: magenta
```
A round Christmas ornament in soft pearl blue with a gentle two-tone sheen rendered as flat cel bands, small simple cap and loop: one crisp pale highlight shape and one cool deeper-blue shadow band — painted pearl finish, not chrome. One ornament only, hanging straight, no ribbon, no tree, no snow. Thin dark-indigo contour. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no mirror reflections, no text, no vignette.
```

### A30 — Warm-gold five-point star ornament
File: `orn4_gold_star.png` · Key: magenta
```
A five-point star Christmas ornament in warm restrained gold with a small loop at the top point: painted matte-to-satin gold with one warm cream highlight plane and one deeper amber shadow plane per arm — flat cel bands, never chrome or metallic glare. Slightly rounded point tips, friendly not sharp. One star only, no ribbon, no tree, no sparkle field. Thin warm brown contour. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no lens flare, no text, no vignette.
```

### A31 — Lavender teardrop ornament
File: `orn5_lavender_teardrop.png` · Key: green
```
A teardrop-shaped Christmas ornament in soft lavender, tapering gently to a rounded lower point, small simple cap and loop: one crisp pale highlight shape and one cool violet shadow band — painted glass, not chrome. One ornament only, hanging straight, no ribbon, no tree, no snow. Thin dark-indigo contour, broad flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure green background (#00FF00), no cast shadow. Square 1:1. No photorealism, no mirror reflections, no text, no vignette.
```

### A32 — Snow-covered Christmas tree
File: `xmastree_snow.png` · Key: magenta
```
A snow-covered Christmas tree: readable warm-brown trunk and tiered pine branch silhouette clearly visible beneath broad rounded snow caps. Snow caps have soft pale blue-grey undersides; deep reef-green branch layers show between them. No ornaments, no lights, no star, no gifts, no ground snow — the tree alone, single trunk base. Thin dark-indigo contour, two or three flat cel value bands, high-key winter colors. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, gentle cozy mood. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no snowfall particles, no text, no vignette.
```

### A33 — Friendly snowman coal piece
File: `coal_piece.png` · Key: magenta
```
A single rounded lump of coal for building a friendly snowman's face: a soft matte charcoal pebble shape with gently rounded facets, one cool blue-grey highlight plane and a deep indigo shadow plane — matte and friendly, never sharp, glossy or threatening. One piece only, no snowman, no snow, no other pieces. Thin indigo contour, two or three flat cel value bands. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no crushed black, no text, no vignette.
```

### A34 — Glow-tip anemone
File: `anemone_glowtip.png` · Key: magenta
```
A sea anemone with one low rounded base and a countable ring of thick tapered tentacles (roughly nine to thirteen), rose-berry to lavender body with softly glowing pale-cyan tentacle tips rendered as a flat pale cap tone, not a bloom effect. Gentle upward S-curves in the tentacles. One anemone only: no rock, no sand island, no fish, no bubbles. Thin dark-indigo contour, two or three flat cel value bands, high-key underwater colors. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, friendly mood. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no emissive glow halo, no text, no vignette.
```

### A35 — Rounded sea urchin
File: `urchin_round.png` · Key: magenta
```
A friendly rounded sea urchin: a plum-violet dome body with countable short blunt rounded spines (never sharp needles), a pale lavender highlight plane on top and a deep indigo shadow plane below. Simple, calm, non-threatening. One urchin only: no rock, no sand, no neighbors. Thin dark-indigo contour, two or three flat cel value bands, high-key underwater colors. Mermaid Roshan children's game asset, clean flat-color anime cel illustration. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1. No photorealism, no spiky threat, no text, no vignette.
```

### A36 — Giant gentle fish silhouette
File: `fish_giant_silhouette.png` · Key: magenta
```
A giant gentle fish in full side view, designed as a soft distant ambient silhouette: one large rounded friendly fish shape in deep teal with a slightly lighter belly band and one broad soft fin plane, small calm eye, mouth closed, no teeth. Very simplified — reads as two or three flat tones, softened edges appropriate for a far-away background animal. Complete fish visible nose to tail. One fish only: no school, no bubbles, no water, no reef. Mermaid Roshan children's game asset, clean flat-color anime cel illustration, gentle friendly mood. Centered on a solid flat pure magenta background (#FF00FF), no cast shadow. Square 1:1, fish spanning most of the width. No photorealism, no scary silhouette, no text, no vignette.
```

---

# SECTION B — Material & wrap sheets (Batch 02: the ranked texture gaps)

From `TEXTURE_SOURCE_AUDIT.md` weaknesses list, highest visible value first.
These are baked onto existing 3D models by `bake_nano_wrap.py` or installed as
`assets/terrain/` sheets. **Blank-canvas rule applies: material only, nothing
that also exists as a 3D prop.**

### B01 — Tropical leaf/frond sheet (HIGHEST VALUE — rebakes 6 plants)
File: `sheet_leaf_tropical.png`
```
A seamless repeating texture sheet of painted tropical leaf surface: broad overlapping leaf blades filling the frame edge-to-edge, each with a simple painted midrib and a few sparse secondary veins, in two flat greens (fresh leaf green and deeper reef green) plus one cool blue-green shadow tone per blade. Perfectly tileable on all four edges, square 1:1, flat even diffuse lighting, no shadows cast between leaves, no vignette, no border, no perspective. Children's storybook game texture: broad flat cel color regions with very restrained painterly grain inside each region. Leaves only — no flowers, no fruit, no insects, no coral, no branches, no sky gaps. No photorealism, no lawn grass, no text, no watermark.
```

### B02 — Amethyst crystal facet sheet (translucent-friendly)
File: `sheet_crystal_amethyst.png`
```
A seamless repeating texture sheet of painted crystal facets: large angular interlocking facet planes in pale lavender-violet amethyst, each facet a single flat tone from a small set (pale lilac, mid violet, soft periwinkle) with thin pale-cyan edge highlights between planes. High-key and luminous, designed to remain readable when rendered translucent like glass. Perfectly tileable on all four edges, square 1:1, flat even lighting, no vignette, no border, no perspective, no dark facets. Children's storybook game texture, broad flat cel regions, minimal grain. Crystal surface only — no rocks, no coral, no sparkle particles, no stars. No photorealism, no chrome, no lens flare, no text, no watermark.
```

### B03 — Orange peel sheet
File: `sheet_fruit_orange.png`
```
A seamless repeating texture sheet of painted orange peel: warm apricot-orange surface with a very gentle dimple pattern rendered as sparse soft slightly-darker dots, plus one broad subtle value shift for softness. Perfectly tileable on all four edges, square 1:1, flat even lighting, no shadows, no vignette, no border. Children's storybook game texture: broad flat cel color regions with restrained painterly grain, matte fruit skin, appealing but not glossy or hyperreal. Peel surface only — no whole fruit outline, no leaves, no stem, no slices. No photorealism, no wax shine, no text, no watermark.
```

### B04 — Melon rind sheet
File: `sheet_fruit_melon.png`
```
A seamless repeating texture sheet of painted melon rind: fresh green surface with broad soft darker-green stripes running in one direction, stripes slightly irregular and hand-painted, two or three flat green tones total. Perfectly tileable on all four edges, square 1:1, flat even lighting, no shadows, no vignette, no border. Children's storybook game texture: broad flat cel color regions with restrained painterly grain, matte fruit skin. Rind surface only — no whole melon outline, no slices, no seeds, no leaves. No photorealism, no gloss, no text, no watermark.
```

### B05 — Banana skin sheet
File: `sheet_fruit_banana.png`
```
A seamless repeating texture sheet of painted banana skin: warm sun-yellow surface with a few very subtle lengthwise ridge lines rendered as soft slightly-deeper yellow bands, and sparse tiny freckle specks kept minimal. Two or three flat yellow tones total. Perfectly tileable on all four edges, square 1:1, flat even lighting, no shadows, no vignette, no border. Children's storybook game texture: broad flat cel color regions, matte fruit skin, restrained grain. Skin surface only — no whole banana outline, no stem, no peel flaps. No photorealism, no brown bruising, no gloss, no text, no watermark.
```

### B06 — Flower petal sheet
File: `sheet_petal.png`
```
A seamless repeating texture sheet of painted flower petal surface: soft overlapping broad petals filling the frame edge-to-edge in coral blush and rose berry pinks, each petal one flat tone with a paler base and one soft lavender shadow edge — two or three tones total. Perfectly tileable on all four edges, square 1:1, flat even lighting, no vignette, no border, no perspective. Children's storybook game texture: broad flat cel regions with very restrained painterly grain. Petals only — no flower centers, no stems, no leaves, no insects. No photorealism, no watercolor bleed, no text, no watermark.
```

### B07 — Red mushroom cap sheet
File: `sheet_mushroom_red.png`
```
A seamless repeating texture sheet of painted mushroom cap surface: warm coral-red matte surface with sparse soft cream rounded spots of gently varied size, spots grouped naturally rather than in a grid. Two or three flat tones total. Perfectly tileable on all four edges, square 1:1, flat even lighting, no shadows, no vignette, no border. Children's storybook game texture: broad flat cel regions with restrained grain, friendly and non-toxic-looking. Cap surface only — no whole mushroom outline, no stem, no gills, no grass. No photorealism, no slime or gloss, no text, no watermark.
```

### B08 — Painted gold metal sheet (throne / gate / lantern hardware)
File: `sheet_metal_gold.png`
```
A seamless repeating texture sheet of painted storybook gold metal: warm restrained gold surface in matte-to-satin finish, rendered as broad flat tone regions (honey gold base, warm cream highlight band, deeper amber shadow band) with very gentle brushed variation inside each region. Perfectly tileable on all four edges, square 1:1, flat even lighting, no mirror reflections, no vignette, no border. Children's storybook game texture: painted metal that supports an illustration, never chrome or photoreal metal. Metal surface only — no rivets grid, no engraving, no gems, no ornament shapes. No photorealism, no lens flare, no text, no watermark.
```

### B09 — Painted sand retry (replaces the ambientCG readability exception)
File: `nb_sand_v2.png`
```
A seamless repeating texture tile of smooth pale ocean-floor sand, top-down orthographic view: very low contrast, soft pale aqua-beige field with only faint, widely spaced, gently curved ripple bands rendered as a barely darker warm tone — calm and quiet so characters and props stay readable on top of it. Absolutely no cracks, no dried-mud pattern, no pebbles, no shells, no starfish, no footprints. Perfectly tileable on all four edges, square 1:1, flat even lighting, no shadows, no vignette, no border. Children's storybook game texture: broad soft flat color regions with the gentlest painterly grain. No photorealism, no noise, no text, no watermark.
```

---

# SECTION C — Backdrops (paintings, exempt from the blank-canvas rule)

### C01 — Painted day sky panorama (replaces the photoreal HDR sky, P0 item)
File: `backdrop_sky_day.png` · Aspect: 16:9 or wider; must tile horizontally
```
A wide painted sky panorama for a children's storybook game, designed to wrap seamlessly left edge to right edge (the left and right borders must match perfectly for a 360-degree sky). High-key gradient from pale paper-aqua at the horizon up to soft lagoon cyan overhead, with gentle rounded cumulus clouds in foam white with the faintest lavender undersides, clouds grouped in calm clusters with plenty of open sky between them. Flat-color anime cel style with soft edges: two or three flat tones per cloud, no dramatic lighting, no sun disc, no god rays, no birds. Horizon band stays simple and even. No photorealism, no HDR look, no vignette, no text, no watermark.
```

---

## Review + install checklist (Claude-side, after Downloads pickup)

1. Compare each result at intended in-game size beside its book pages
   (`ART_STYLE_GUIDE.md` source reference map) — reject watercolor volume,
   mascot faces on natural animals, baked dressing, gradients-as-shading.
2. Props: key out background, trim to alpha, normalize to max 1024px,
   verify complete anatomy and single-object contract.
3. Tiles/sheets: 3x3 repeat + mirrored-seam inspection; verify blank-canvas
   rule; derive `_nrm`/`_rgh` maps programmatically where a slot needs them.
4. Approved installs update `ASSET_LICENSES.md` in the same commit, then run
   the trusted probes and screenshot verification before merge.
