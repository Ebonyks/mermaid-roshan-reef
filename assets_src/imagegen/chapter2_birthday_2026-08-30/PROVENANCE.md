# Chapter 2 birthday cake and Sky Lagoon strawberries — provenance

Status: `SELECTED_RUNTIME_CANDIDATES`; owner/device/child acceptance remains open.
Date: 2026-08-30
Method: OpenAI built-in `image_gen.imagegen`; project-original art; no external URL.

## Authority and intended use

- `assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png` is the exact cake-image candidate shared by the Candy Maker completion and later Main Hall party presentation. It intentionally contains no candle or flame; those remain separate plot-owned layers.
- `assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png` is the fresh ingredient candidate collected during Farmer Roshan's Sky Lagoon preparation beat.
- `assets/chapter2/birthday/sky_lagoon_strawberry_single.png` is the exact one-fruit pickup cutout used for each of the five independently saved Farmer pickups. It replaces the rejected Atlas crop that retained visible pieces of the two neighboring berries.
- Both outputs are ordinary runtime cutouts, not cinematic delivery frames and not owner-accepted final art.
- The selected cake was generated after the owner rejected the first, shorter edit as not pretty enough, then required a strict rainbow-tier order and a 4.9/5 critical-prop audit bar. The selected six-tier master passed an independent Luna visual review at 4.9/5; owner/device/child final acceptance remains open.
- Existing project art was inventoried before generation. The Chef cake and worlds were reusable structural/style references, but the repository contained no strawberry-specific art and no sufficiently grand persistent party-cake cutout.

## Selected grand cake

- Result ID: `exec-85a4d695-63ee-4816-b0a3-050cfed86542`
- Native: `native/chapter2_grand_candied_strawberry_cake_native.png`
- Native SHA-256: `52ec69c54333244a16483755f1852211059a2d70cbd1b4d16fe31d0e15a46651`
- Native geometry: 1254×1254 opaque RGB with a baked pale checkerboard; preserved as the selected generated master, not used directly at runtime.
- Runtime: `assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png`
- Runtime SHA-256: `4c6eca9e9c96041c79841813c37b1f8a502d5e654b1ed6c7af7783e034ff0d14`
- Runtime geometry: 1024×1024 RGBA; alpha extrema 0–255; transparent corner `(0,0,0,0)`.
- Runtime derivation: `tools/prepare_chapter2_birthday_art.py` removes only near-neutral pale pixels connected to the native canvas border, reconstructs the two-pixel antialiased edge from the nearest interior outline/checker matte equation, and uniformly resizes the complete canvas to 1024×1024 in premultiplied-alpha space. No crop, subject translation, compositing, repainting, relighting, or local geometry repair occurs.
- Reference 1: `assets/opera/worlds/props/goal_chef.png`, SHA-256 `cb28da49b252769ef143d75ddb890d2350cebf6e12aca33a875c88b04ff33467`, palette/style role only.
- Reference 2: prior clean six-tier layout candidate `exec-9a313d14-0697-4e0a-856a-ee8990c2ff65`, layout/defect-correction role only; not preserved as runtime authority.

Prompt:

> Re-illustrate the supplied six-tier rainbow birthday cake as a meticulous final clean master, preserving its successful elegant silhouette, exact top-to-bottom red/orange/yellow/green/blue/violet tier order, shell crest, candied-strawberry arrangement, scalloped shell platter and full pedestal. Keep the whole cake centered and reduce it slightly so the entire crest, platter, pedestal, and transparent padding fit safely inside the square; cake occupies about 82 percent of canvas height. Maintain rich polished undersea storybook beauty, not a plain diagram. Correct the last expert-level defects only: perfectly centered common axis; smooth complete elliptical tier lips; uniform navy-purple contour weight with no cyan fringe; consistent restrained warm-gold edging; identically formed strawberries with intact leaves and no edge-merging; perfectly even pearl spacing; no tiny accidental beads; no muddy pixels or broken piping. Use broad cream shell-scallop piping and subtle consistent embossed wave texture for sophistication, with exactly one centered shell medallion on every tier. Preserve one balanced strawberry pair on each of the upper five tiers and no fruit on the violet base. One coherent upper-left light. Do not crop or hide any stand part. No candle, flame, text, number, character, utensil, table, room, floating decoration, random coral/seaweed, checkerboard, black/white/gray/color matte, border, or cast shadow. Output a true 1024×1024 RGBA cutout with alpha exactly 0 outside the cake and clean antialiasing. 4.9/5 critical hero-prop quality; every line and repeated motif intentional and internally consistent.

## Selected fresh strawberry cluster

- Result ID: `exec-fadbf684-20b1-49ff-8513-5cb95bdf99dd`
- Native: `native/sky_lagoon_strawberry_cluster_native.png`
- Native SHA-256: `27b6b217137045d05e45cf2c2d6132ed59c933e92db34a1a3fd60dbaff723ec8`
- Native geometry: 1254×1254 RGBA; alpha extrema 0–255.
- Runtime: `assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png`
- Runtime SHA-256: `c28ff9ab18a20488cd78d2cc11000c97a3838879870a5d368fa68ee17c97acf6`
- Runtime derivation: uniform whole-canvas Lanczos resize to 1024×1024 RGBA with Pillow 12.3.0; no crop, mask, subject translation, compositing, repainting, or relighting.

Prompt:

> Create one isolated Chapter 2 Sky Lagoon strawberry ingredient cutout for Mermaid Roshan: a child-readable cluster of three ripe coral-red strawberries growing together beneath a small crown of soft sea-green leaves, with rounded navy-purple painted contours, broad pastel storybook value bands, aqua-lavender shadows, warm highlights, and polished 2D toy-playset rendering matching a whimsical undersea castle game. The berries are fresh and uncoated here—no candy glaze, sugar shell, sparkles, frosting, candle, flame, basket, character, text, ground, or background. Make the three strawberry silhouettes and green leafy crowns unmistakable at phone size. Return one complete isolated RGBA PNG on fully transparent background, centered with generous padding, no cast shadow outside the cutout, 1024 by 1024.

## Selected single strawberry pickup

- Generation method: OpenAI built-in ImageGen, reference edit from the approved cluster runtime cutout.
- Result ID: `exec-4e6a8283-1ce6-45e4-b929-5e3a41cddb31`.
- Native: `native/sky_lagoon_strawberry_single_native.png`.
- Native SHA-256: `e1ea98381c54a5ac34cc6b4d6e0fee43155f3f1d094c790b548299953e198e22`.
- Native dimensions/mode: 1254×1254 RGB with a baked checker matte.
- Runtime: `assets/chapter2/birthday/sky_lagoon_strawberry_single.png`.
- Runtime SHA-256: `3bef406012e9a5ec90e18d3709b361f0ad0f9926f0961e05aac67e3e0c454c5f`.
- Runtime dimensions/mode: 1024×1024 RGBA, alpha extrema 0–255.
- Runtime derivation: the same border-connected checker removal, matte reconstruction, and uniform whole-canvas premultiplied-alpha resize implemented by `tools/prepare_chapter2_birthday_art.py`; no subject crop, translation, compositing, repainting, or geometry repair.

Prompt:

> Using the referenced approved three-strawberry cluster only as the exact visual-style and material reference, create ONE isolated ripe strawberry gameplay token for Mermaid Roshan Chapter 2. Exactly one coral-red strawberry fruit with one compact sea-green leafy crown, matching the reference's polished 2D undersea storybook rendering, rounded navy-purple painted contour, broad coral/red value bands, aqua-lavender shadow, warm glossy highlight, and golden seeds. The entire single fruit and all leaves must be fully visible, centered, upright, and unmistakable at small Android-phone size. Generous transparent padding. True RGBA transparent background with alpha 0 outside the one strawberry. No second berry, no partial berry, no cluster, no stem vine, no basket, no ground, no backdrop, no text, no flame, no cake, no cast shadow, no checkerboard or matte. Clean production cutout, 1024x1024.

Selection rationale: the prior non-destructive Atlas crop of the three-berry cluster failed independent Sol visual audit because it retained large inner portions of both side berries. A separate one-fruit source was therefore the smallest asset gap that could truthfully render five individual collectibles. Final owner/device/child acceptance remains open.

## Superseded and rejected cake attempts

- `native/superseded/chapter2_four_tier_pre_rainbow_native.png`, result ID `exec-6e701de7-222c-45ef-8f08-ef80e3c8803a`, SHA-256 `f67dce6099de222f60305618ad94ab612a550c3bedecb32f0b92e9266738b008` — `SUPERSEDED_BY_OWNER_DIRECTION`; visually much better than the first attempt but only four tiers and therefore unable to express the required full rainbow order. Preserved for provenance only; no runtime authority.

- Result ID: `exec-460e3ae5-d126-4b77-8880-8e075f6a38c0`
- SHA-256: `ee88f08e8a3dc25a778edc96f7fdc82c14b68b8edd183fa39637037ed129b02b`
- Disposition: `REJECTED_BY_OWNER`; too short and visually ordinary for the birthday centerpiece. It is not preserved in runtime or source assets and must not be selected by code.

## Review limits

Codex verified runtime RGBA alpha, dimensions, hashes, candle absence, strawberry readability, and shared-cake suitability. A separate Luna audit rated the selected generated master 4.9/5 visually, with only non-blocking natural variation in bead spacing, frosting curvature, seeds/leaves, and top dollop symmetry. This record grants provenance and implementation authority only. Target-device composition, four-year-old comprehension, owner final-art acceptance, and party-scene visual acceptance remain separate master-audit gates.
