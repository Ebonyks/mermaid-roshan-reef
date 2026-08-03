# Shared water-FX atlas provenance — 2026-08-02

This directory preserves the native OpenAI built-in ImageGen chroma masters
and accepted local alpha conversions for the six project-original assets in
`CODEX_WATER_FX_WORKORDER_2026-08-02.md`. No downloaded or external art was
used. The reference audit found no reusable free-standing splash, ripple, or
bubble-burst motion; extracting one from approved room art would have been
destructive and would not supply the required action frames.

Generation happened on 2026-08-01 in the America/Los_Angeles timezone. The
work-order date is retained in the directory and runtime asset provenance.

## Approved project-local references

- `assets/flats/castle/interactions/bubble_bath_bathtub_atlas.png`, SHA-256
  `e91f83d08ea38924e45ee90512d8cb0b9efdf9eefda595220ea92b92b5ba5b4e`
- `assets/flats/castle/interactions/bubble_bath_sink_atlas.png`, SHA-256
  `98f58234de49cd168d3a5bf2d5955f92c4474b997df050b8b1240cbeffed4b22`
- `assets/flats/castle/interactions/mermaid_pool_bubble_fountain_atlas.png`,
  SHA-256
  `b28f7bcbb10bd99610547cfc8c33c11a286fe16860e640619cd0e8a9adb5f186`

The three files above were inspected as one disposable contact sheet because
the Windows local-path image handoff was unavailable. The sheet was a
reference-only view and contributed no delivery pixels. Later calls used
accepted generated candidates as continuity references through recent-image
context.

## Shared execution and constraints

All six prompts used `Use case: stylized-concept` and identified the asset as a
production 2D game VFX atlas/strip for Godot. Every prompt required polished
traditional frame-by-frame storybook painting, graphic cel shapes, hard
alpha-scissor-ready silhouettes, dark navy/purple outlines, and soft gradients
only inside opaque water marks. The locked palette was deep aqua near
`#3389CC`, light aqua near `#80D1E6`, foam near-white `#F2FBFF`, sparkle white,
and the established pale-lavender/navy shadows. Every prompt prohibited words,
letters, digits, labels, symbols, arrows, grid lines, borders, watermarks,
signatures, characters, props, scenes, cast shadows, directional lighting, and
use of `#ff00ff` inside an effect. Empty pixels were requested as a perfectly
flat solid `#ff00ff` chroma field with no texture, gradient, floor, or shadow.

Chroma removal command for every accepted native candidate:

```text
python C:/Users/Peter/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py
  --input <chroma_native.png> --out <alpha_native.png>
  --auto-key border --soft-matte --transparent-threshold 12
  --opaque-threshold 220 --despill
```

Runtime atlases are deterministic derivatives made by
`tools/build_water_fx_atlases.py`. The builder resamples whole cells, aligns
bottom-center splash pivots, centers ripple pivots, preserves bubble rise
relative to each fixed cell center, and normalizes the foamline as one whole
strip. It does not tween, interpolate, duplicate, or synthesize motion. The
medium runtime selects generated cells `0,1,2,3,4,5,6,8`; native cell 7 is a
redundant foam hold. The ripple uses one uniform 0.94 whole-cell scale so every
cell retains a clear filtering border.
A uniform 0.70 saturation transform is applied to each complete runtime sheet;
the resulting opaque-pixel means are 0.3547?0.4274, at or below the strictest
0.428 standee foreground band.

## 1. Small splash — prompt-specific request

```text
Input images: the supplied contact sheet is a style, palette, outline, bubble, and rendering reference only; do not copy its bathroom fixtures or props.
Primary request: Create one traditional hand-drawn eight-frame animation atlas for a SMALL WATER SPLASH, a gentle "plink" from a toy prop or fetch ball touching water.
Subject/action sequence: exactly eight distinct sequential animation frames. Frame order is left-to-right across the top row, then left-to-right across the bottom row. Start with a tiny water dimple; grow into the same compact crown splash with 2–3 droplets; droplets descend; crown collapses into a low ring; finish with a sparse settling ring. Every frame must visibly advance the action; no duplicated holds.
Composition/framing: exact 2:1 atlas layout, four equal columns by two equal rows, eight cells total, no gutters or visible cell borders. Keep every frame inside its cell with generous clearance. The fixed waterline contact pivot is the exact same point in every cell: horizontal center at 50% of the cell and vertical position at 84% of the cell. Splash art rises above that point and the settling ring stays centered on it.
Family constraint: the three splash sizes must share this crown, droplet, and foam language, so make this a clean reusable family anchor.
```

- Chroma master: `fx_water_splash_small_chroma_native.png`, 1774×887,
  SHA-256 `32909592f5a84416901270d381487b069eaf79328953e8b2ec6033a1a3204a8d`.
- Alpha master: `fx_water_splash_small_alpha_native.png`, 1774×887,
  SHA-256 `a3c95b767c6e3c3c7eb6f9af66cf8a6c582c564e64ab934fc23a6d02e1850aad`.
- Sampled key `#fb03f9`; 1,426,512 transparent and 7,759 partially
  transparent pixels after conversion.

## 2. Medium splash — prompt-specific request

```text
Input images: Image 1 is the accepted SMALL WATER SPLASH family anchor and the authority for crown silhouette, droplet language, foam treatment, palette, outline, and storybook rendering. Create the same splash family at medium scale; do not redesign it.
Primary request: Create one traditional hand-drawn eight-frame animation atlas for a MEDIUM WATER SPLASH: a real splash from Chuck landing in the fetch lake or a heavier toy prop.
Subject/action sequence: exactly eight distinct sequential animation frames packed into the first eight cells of a 3×3 grid, read left-to-right, top-to-bottom. The ninth bottom-right cell must be completely empty flat #ff00ff. Start with a compact impact dimple; rapidly form the same family crown; throw several rounded droplets; peak with a fuller foam burst; then fall and collapse into the same low settling ring. Every frame must visibly advance; no duplicate holds.
Composition/framing: exact square atlas layout, three equal columns by three equal rows, no gutters or visible cell borders. Keep each frame fully inside its cell with clearance. The fixed waterline contact pivot is the exact same point in every occupied cell: horizontal center at 50% of the cell and vertical position at 86% of the cell. Splash art rises above that point and the final ring remains centered on it. Use more vertical energy than the small tier while preserving the same recognizable crown anatomy.
```

- Chroma master: `fx_water_splash_medium_chroma_native.png`, 1254×1254,
  SHA-256 `936e6ca36e3612748dcb7ab21a3b05fef03c1db793633b8cd5e3b4a271d36464`.
- Alpha master: `fx_water_splash_medium_alpha_native.png`, 1254×1254,
  SHA-256 `3fa47b0dc76a5f4f00bca5944f8f785474e57dc21c145447372f0a17ef330b3c`.
- Sampled key `#f703f3`; 1,332,326 transparent and 11,965 partially
  transparent pixels after conversion.

## 3. Hero breach splash — prompt-specific request

```text
Input images: Images 1 and 2 are the accepted SMALL and MEDIUM WATER SPLASH family anchors. They are the authority for crown anatomy, rounded droplets, foam, palette, dark outline, and storybook rendering. Create the same splash family at hero breach scale; do not redesign it.
Primary request: Create one traditional hand-drawn eight-frame animation atlas for a HERO WATER BREACH SPLASH: a Roshan-scale burst readable around 300 pixels tall on a 1280×720 phone screen, used when the mermaid crosses the reef surface in either direction.
Subject/action sequence: exactly eight distinct sequential animation frames packed into the first eight cells of a 3×3 grid, read left-to-right, top-to-bottom. The ninth bottom-right cell must be completely empty flat #ff00ff. Start with a broad compressed surface dimple; erupt into the same recognizable family crown; drive two graceful arcing sprays upward and outward; add rounded droplets and a few small white sparkle dots at peak; fall into a generous foam burst; collapse into a broad ring. Every frame must visibly advance; no duplicate holds.
Composition/framing: exact square atlas layout, three equal columns by three equal rows, no gutters or visible cell borders. Keep each frame fully inside its cell with clearance. The fixed waterline contact pivot is the exact same point in every occupied cell: horizontal center at 50% of the cell and vertical position at 88% of the cell. The arcing spray rises above that point but never crosses cell edges. Preserve the smaller tiers' crown silhouette and droplet language with larger vertical arcs and stronger foam readability.
```

- Chroma master: `fx_water_splash_breach_chroma_native.png`, 1254×1254,
  SHA-256 `377b74100d63876837c4fd9f233244bd1867e878873284c743ab5ca773dea588`.
- Alpha master: `fx_water_splash_breach_alpha_native.png`, 1254×1254,
  SHA-256 `734f4ba359c93e1d7e8409990e0774c650377c412eda8f0c227f021ce80cbff6`.
- Sampled key `#f204ed`; 1,298,445 transparent and 14,065 partially
  transparent pixels after conversion.

## 4. Ripple ring — prompt-specific request

```text
Input images: the supplied small, medium, and breach splash atlases are the accepted water-FX family authority for palette, outline, rounded marks, and storybook cel rendering. Extend that exact vocabulary into a ripple.
Primary request: Create one traditional hand-drawn eight-frame animation atlas for a FLAT EXPANDING WATER RIPPLE RING used for settle-on-water, wet footfalls, and taps.
Subject/action sequence: exactly eight distinct sequential frames, read left-to-right across the top row and then the bottom row. Begin with a small tight oval dimple; expand into one broad flat elliptical ring; allow a subtle secondary inner echo; scatter only a few tiny foam flecks; thin and fade the ring by the last frame. Every frame must visibly expand or dissipate; no duplicated holds.
Composition/framing: exact 2:1 atlas layout, four equal columns by two equal rows, eight cells total, no gutters or visible cell borders. Draw every ripple face-on as a low top-down oval so the engine can later tilt the quad onto a water surface. The fixed pivot is the exact center of every cell; every oval is centered on that same point while increasing in diameter. Keep all strokes and flecks inside each cell with clear margins.
Additional constraint: ring/ripple only; no vertical splash crown, fountain, wave wall, or droplets flying upward.
```

- Chroma master: `fx_water_ripple_ring_chroma_native.png`, 1774×887,
  SHA-256 `e71ab17d63bf427b1b815e118de24dc797072b15f0c37549c50657b23109e4dc`.
- Alpha master: `fx_water_ripple_ring_alpha_native.png`, 1774×887,
  SHA-256 `80dcc76f386ce5dc237bcaf076e98abbe094d2bfa16cd6411741e7945f8d5f7e`.
- Sampled key `#f505ee`; 1,438,179 transparent and 25,746 partially
  transparent pixels after conversion.

## 5. Bubble burst — prompt-specific request

```text
Input images: the first supplied contact-sheet image is the accepted castle bubble style reference; the later supplied images are the accepted shared water-FX family authority for palette, outlines, rounded marks, and storybook cel rendering. Do not copy any bathroom fixture or splash crown.
Primary request: Create one traditional hand-drawn eight-frame animation atlas for an UNDERWATER BUBBLE BURST, the splash counterpart that appears when something plunges below a water surface.
Subject/action sequence: exactly eight distinct sequential frames, read left-to-right across the top row and then the bottom row. Begin with 4–6 compact pastel bubbles emerging around the center pivot; bubbles rise and spread upward with staggered sizes; one or two swell slightly; then pop in sequence into tiny four-point sparkle marks and a few small circular droplets; finish with only two or three fading sparkles. Every frame must visibly advance; no duplicated holds.
Composition/framing: exact 2:1 atlas layout, four equal columns by two equal rows, eight cells total, no gutters or visible cell borders. The fixed pivot is the exact center of every cell. Keep the initial cluster centered on that point; subsequent bubbles rise above it while the cluster's horizontal balance remains centered. Keep every bubble and sparkle inside its cell with clear margins.
Additional constraint: 4–6 bubbles as the core effect, not a fountain, foam pile, splash crown, wave, or water ring.
```

- Chroma master: `fx_water_bubble_burst_chroma_native.png`, 1774×887,
  SHA-256 `f3da4dcc5731eb4529b1bb0ced7b881a536787b034c221b7205691c93b95be9f`.
- Alpha master: `fx_water_bubble_burst_alpha_native.png`, 1774×887,
  SHA-256 `6df638cfefb8356865f92f64e9248fb312cda2eec52390661eba5572e8857570`.
- Sampled key `#f010e2`; 1,515,809 transparent and 6,084 partially
  transparent pixels after conversion.

## 6. Foamline strip — prompt-specific request

```text
Input images: the supplied shared water-FX atlases are the accepted authority for palette, outline, rounded foam marks, and polished storybook cel rendering.
Primary request: Create one STATIC HORIZONTAL FOAMLINE / MENISCUS BAND for dressing waterlines on promenade murals and floating standees. It must be sparse, quiet, and horizontally repeatable. Do not depict motion or an animation grid.
Subject: one long, thin, broken horizontal band made from intermittent low aqua meniscus arcs, small near-white foam scallops, and a few tiny foam flecks. Maintain a consistent average thickness and rhythm across the width. Leave natural short gaps between marks. Keep both far left and far right ends fully empty for a distance comparable to the internal gaps so repeated copies meet invisibly with no clipped stroke.
Composition/framing: exact 4:1 ultra-wide strip, one static frame only, no cells, gutters, or border. The foamline runs straight horizontally across the upper portion of the strip, with ample transparent/chroma room below for droplets and scallops. No large focal crest or unique center ornament. Keep all content within the canvas. The eventual runtime sprite uses its top edge as the waterline.
Additional constraint: static sparse foamline only; no painted animation, directional streaks, arrows, speed lines, full water surface, wave wall, splash crown, ripple ellipse, or bubble cluster.
```

- Chroma master: `fx_water_foamline_chroma_native.png`, 1774×887,
  SHA-256 `c7f19a8d9c45fc9753435a3be944f03e91a506c7c9f5a188789d217cc2be8c59`.
- Alpha master: `fx_water_foamline_alpha_native.png`, 1774×887,
  SHA-256 `6942526aef6cb543fa44fd4a54c95e6762c28386f2a510662e3e26d4baaa0598`.
- Sampled key `#f108e9`; 1,545,234 transparent and 4,055 partially
  transparent pixels after conversion.

## Runtime delivery hashes and review

| Runtime file | Size / grid | SHA-256 |
|---|---|---|
| `fx_water_splash_small_atlas.png` | 1024×512 / 4×2 | `bdd9233b6b0afa22374777ae2aaf7fc52b907ae631f61c6f3a3d02dd1c03551f` |
| `fx_water_splash_medium_atlas.png` | 1024×1024 / 3×3, 8 used | `32c5f33cdaedbc0d624002eed596bf538f97c3a99bb77206818c19545b66bbce` |
| `fx_water_splash_breach_atlas.png` | 1024×1024 / 3×3, 8 used | `12ffe29bf3e9b0a1c48c72c56d05b3f09849ba4ee1669d1b485f7fdc020e2290` |
| `fx_water_ripple_ring_atlas.png` | 1024×512 / 4×2 | `5fbfa30a61fb0275274e7eef70a4d6df7f46a8cd9f7c209d2cd2305710a9700c` |
| `fx_water_bubble_burst_atlas.png` | 1024×512 / 4×2 | `4c98dd531d6869a2137d210c161efab86dff03c08ce2378e855d1d46c9c2896c` |
| `fx_water_foamline_strip.png` | 1024×256 / static | `582ef6632763c96bb1292d0d6a62d7d5b75120e18d507f3782373d7aec60a953` |

Human review: accepted. All 40 animated delivery cells contain distinct drawn
beats; both 3×3 trailing cells are transparent. Onion-skin geometry keeps the
three splash contact baselines fixed and the ripple center fixed. The three
splash tiers use the same crown, rounded droplet, foam, aqua, and outline
language. At a 1280×720 review canvas, the small peak remained clear at 90 px
tall and the breach peak remained clear at 300 px tall. The bubble burst reads
as an underwater event, the ripple remains a flat surface mark, and the quiet
foamline has clear horizontal ends. No frame contains a character, prop,
scene, word, letter, digit, label, watermark, or directional baked lighting.
