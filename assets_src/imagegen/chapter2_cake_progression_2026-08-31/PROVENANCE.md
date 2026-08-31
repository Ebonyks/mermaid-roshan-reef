# Chapter 2 cake progression — provenance

Status: `SELECTED_RUNTIME_CANDIDATES`; owner/device/child acceptance remains open.
Date: 2026-08-31
Method: OpenAI built-in `image_gen.imagegen`; project-original art; no external URL.

## Purpose and authority

This packet owns the complete active cake progression: mixed batter, stirred
batter, baked loose tiers, stacked bare tiers, frosted undecorated cake, five
candied strawberries waiting on a tray, and the finished cake carrying exactly
those five strawberries. The earlier ten-strawberry test model is preserved in
its original packet but is superseded as the active endpoint. The existing
unlit and lit rainbow candle assets remain separate plot-owned layers.

All seven selected masters are 1254×1254 opaque RGB with a baked pale checker
matte. `tools/prepare_chapter2_cake_progression_art.py` reuses the audited
border-connected checker removal and whole-canvas premultiplied-alpha resize
from `tools/prepare_chapter2_birthday_art.py`. Every runtime result is
1024×1024 RGBA with alpha extrema 0–255. No protected original was modified.
The wide Bake-tray, Candy-tray, and final-cake canvases receive one additional
uniform whole-canvas 1024→960 scale and centered transparent pad, producing
safe outer padding without cropping, masking, local movement, or repair.

## Selected stages

| Runtime role | Result ID | Native file / SHA-256 | Runtime file / SHA-256 |
|---|---|---|---|
| Chef Mix complete | `exec-4ee4a58a-52c4-41c9-8ee3-885fb0227ce9` | `native/chapter2_chef_batter_unstirred_native.png` / `2e4e7c26c7a9e2db3ca19d427d043d487199d9e4dbc8341d39f732a4ec65e879` | `assets/chapter2/birthday/chapter2_chef_batter_unstirred.png` / `f259c77205dfeee8ad3fe5f9a316eb9e433d4cc6a685cfb1d8e44daacfd6aca9` |
| Chef Stir complete | `exec-0fe2885d-e9e3-42a7-b38d-eb3f19dddc4f` | `native/chapter2_chef_batter_stirred_native.png` / `d53229bddd90c456b1fc06f507546fc0765070432f3b89765248c6e83688cbf3` | `assets/chapter2/birthday/chapter2_chef_batter_stirred.png` / `065c85cb7af69abc2c59780b515579762488b9072d0fbe32e976facc3381bc56` |
| Chef Bake complete | `exec-c1a602f1-b913-4780-bc76-0d3a957e397e` | `native/chapter2_chef_baked_tiers_unstacked_native.png` / `a13b3fcb69db683459df557fcf6861b4a4c12a3b9211d8ac6f9c39a2e0e52dec` | `assets/chapter2/birthday/chapter2_chef_baked_tiers_unstacked.png` / `74b68d65ac3966cf1a2f9ad8aada8d17b8210342f32e2426ceab5b7164ba2cdd` |
| Chef Stack complete | `exec-d3197f71-2522-4e38-96bf-0522af1e1538` | `native/chapter2_chef_stacked_unfrosted_cake_native.png` / `78ea689fe79d20c5d1ea5b9b44da62f2f64ea014d8149bd32a263a647792e560` | `assets/chapter2/birthday/chapter2_chef_stacked_unfrosted_cake.png` / `b3741c02402693637dfd6367e98f41ce6380d2641ffe04b061f00bade1050a37` |
| Chef Frost complete | `exec-0e6eeed5-e803-46c4-a442-05f59f57eedc` | `native/chapter2_chef_frosted_rainbow_cake_native.png` / `413131f47cc8bd4cca3ff58c61e050db2e89ec2028e499c9e9233cc7393451e0` | `assets/chapter2/birthday/chapter2_chef_frosted_rainbow_cake.png` / `6937204494c98147552cb463b65c11104ffc43c85d9ca7bc907865601f2efc46` |
| Candy Maker Glaze complete | `exec-055a4c5e-1c00-45e5-8e61-d85748c481b3` | `native/chapter2_candied_strawberries_tray_native.png` / `56564fbf23282b250d140007de8a4c00ab36715416787eb7536fdfb7141aae45` | `assets/chapter2/birthday/chapter2_candied_strawberries_tray.png` / `67caf1c52179a25407344905bdd5d83936721bdcfdc3b5bd274cf18663136839` |
| Candy Maker Place complete | `exec-b477626b-5953-413c-900b-379c958e0551` | `native/chapter2_grand_five_strawberry_cake_native.png` / `85b0ec1e125f2ed50ff69eaaff8dcc5b4b17fb1fca8c489dde709d48cc2af003` | `assets/chapter2/birthday/chapter2_grand_five_strawberry_cake.png` / `91dbeb1f9c634eebac04cd61f29318a3f4da6c2486fcab1182cdbf93668cad59` |

## Prompt record

### Chef Frost complete

> Edit the referenced approved Chapter 2 birthday cake into its immediately earlier CHEF FROSTING COMPLETE state. Preserve the exact same six-tier centered silhouette, exact tier sizes and top-to-bottom order red, orange, yellow, green, blue, violet, the same scalloped platter and pedestal, shell crest, pearl piping, cream swags, shell medallions, gold edging, navy-purple outline, lighting, storybook rendering, camera, scale, and transparent canvas. Remove every strawberry and every strawberry leaf cleanly, reconstructing the frosting and piping beneath them so no gaps, scars, red fragments, green fragments, floating seeds, or asymmetry remain. Do not add candy, fruit, candle, flame, text, character, utensil, room, backdrop, shadow, or new ornament. This must read as the exact same physical cake one step before Candy Maker decoration, not a redesign. Return one complete isolated RGBA PNG with fully transparent background and generous uncropped padding, 1024x1024.

### Chef Stack complete

> Create the immediately earlier CHEF STACK COMPLETE state of the same Chapter 2 hero cake, using the references as strict identity, proportion, palette, camera, and style guides. Show the same six physical cake tiers centered and vertically stacked in the exact same top-to-bottom rainbow order red, orange, yellow, green, blue, violet, with the same tier widths, heights, common axis, and same pink scalloped stand/pedestal. The cake is baked but NOT frosted or decorated yet: each tier is a clean child-readable colored sponge round with a soft baked crumb texture and smooth complete elliptical lip. Remove all cream swags, pearls, piping, shell medallions, top shell crest, strawberries, candy glaze, gold decoration, candle, and flame. Keep only a restrained navy-purple storybook contour and the existing soft upper-left light so it unmistakably reads as the same cake one construction step earlier. No loose tiers: all six are stacked. No text, character, utensil, room, background, cast shadow, checkerboard, or matte. Complete isolated RGBA cutout, transparent outside the stand, generous uncropped padding, 1024x1024.

### Chef Bake complete

The selected result uses a three-tray layout because repeated two-tray attempts
visually reset the diameter scale at the row boundary. Its generation used the
stacked bare cake as size/style authority, followed by one surgical correction:

> Regenerate the Chef Bake result as ONE isolated transparent 2D game prop. IMAGE_1 gives the approved loose baked-round material and tray styling. IMAGE_2 gives the exact final cake’s six tier colors and size hierarchy. Show exactly SIX unfrosted baked cake rounds, all separate and clearly not stacked, arranged on THREE vertically separated cream scalloped baking trays with TWO rounds per tray so the global size order is unmistakable. Top tray: a tiny RED round at left and a slightly larger ORANGE round at right. Middle tray: a clearly larger YELLOW round at left and a still larger GREEN round at right. Bottom tray: a clearly larger BLUE round at left and the largest VIOLET round at right. CRITICAL: compare every adjacent pair across the whole image—red < orange < yellow < green < blue < violet in visible horizontal diameter, with each round at least 12% wider than the preceding round. Do not reset scale on a new tray. Suggested diameters on a 1024 canvas: red 105 px, orange 125 px, yellow 150 px, green 180 px, blue 215 px, violet 260 px. Keep similar tier thickness and circular perspective. Every round must fit fully inside its tray with clear separation and padding. Preserve pastel underwater storybook polish, navy-purple contours, warm baked texture, and cream/purple scalloped trays. No frosting, fruit, strawberries, pearls, shells, candle, flame, bowl, spoon, character, room, backdrop, checkerboard, matte, text, shadow, cropped edge, extra round, duplicate, fused object, or stack. Fully transparent outside area, at least 32 transparent pixels clear around the entire silhouette, uncropped, 1024x1024 RGBA. Exact six-count and exact color order are blocking.

> Surgical correction only: preserve this exact three-tray, six-round Chef Bake prop, but enlarge the GREEN round on the middle tray until its horizontal diameter is unmistakably larger than the YELLOW round immediately to its left and unmistakably smaller than the BLUE round below. The current green is too small. Target visible widths: yellow about 255 px, green about 290 px, blue about 330 px. Keep red < orange < yellow unchanged; keep blue < violet unchanged. The final strict sequence must be red < orange < yellow < green < blue < violet, with no ties or reversals. Center the enlarged green on its existing plate, keep it fully within the middle tray, and reconstruct only the directly affected cream plate pixels cleanly. Do not alter any other round, tray, position, color, texture, outline, lighting, scale, count, transparency, or composition. Exactly six separate unfrosted baked rounds. No frosting, fruit, candle, extra objects, text, backdrop, checkerboard, matte, or crop. One complete 1024x1024 transparent RGBA cutout with clear outer padding.

Pixel-semantic review of the selected runtime measures colored-body widths
approximately `145, 170, 194, 233, 251, 308` pixels, so every adjacent pair
increases strictly.

Superseded Bake attempts are preserved as provenance evidence:

| Result ID | File / SHA-256 | Rejection |
|---|---|---|
| `exec-1433ac26-e1f4-4a6f-9c6f-be8b330ddcce` | `native/superseded/chapter2_chef_baked_tiers_inconsistent_native.png` / `ec8de533107741ce0ab70decb820ef110b5c131a18d55d727177fd120e7d2072` | Multiple reversed/tied diameters. |
| `exec-4f2f1cf2-4da7-45ec-a472-fbf7b23f199f` | `native/superseded/chapter2_chef_baked_tiers_two_trays_global_reversal_native.png` / `7691e871f799f48451134b6db89ad69acbfda47620e57dec93362f931096784c` | Yellow wider than green. |
| `exec-403f9442-28b3-4975-84c5-34ad64127eb9` | `native/superseded/chapter2_chef_baked_tiers_two_trays_second_reversal_native.png` / `6169c25d57fd422033b147927eb39820b290bb37991e3bade7f7d3873dec9a5d` | Two-tray row reset persisted. |
| `exec-c7d780cf-473f-4854-81ad-7ca9818611cd` | `native/superseded/chapter2_chef_baked_tiers_green_blue_near_tie_native.png` / `50ff2f299d6f9e9bb0f99c13b9c53629a0088f7ef73eb6039f546a953e4dc929` | Green and blue were not reliably increasing. |
| `exec-a3d36a47-ae3f-4dbe-9a92-d60a7f3344ca` | `native/superseded/chapter2_chef_baked_tiers_green_too_small_native.png` / `fa67f36ffc9436a116d55788ca68b0debc109d1dfff6033a667b9726b2e0f200` | Green became smaller than yellow. |

### Chef Mix complete

> Create the CHEF MIX COMPLETE stage prop for Mermaid Roshan Chapter 2, matching the polished 2D undersea storybook materials, navy-purple contour, pastel value bands, and upper-left lighting of the referenced rainbow cake stages. Show one large child-readable lavender mixing bowl shaped like a scallop shell, centered, with six visibly separate thick batter pours inside it in rainbow order red, orange, yellow, green, blue, violet. The colored batter has been tipped into the bowl but has NOT been stirred together: six distinct adjacent glossy ribbons remain easy to count. Include one small gold-handled spoon resting beside the bowl, not inside it. No baked cake, cake tier, tray, frosting, candy, strawberry, candle, flame, text, character, room, background, cast shadow, checkerboard, or matte. One complete isolated RGBA prop cutout on fully transparent background, generous uncropped padding, 1024x1024, unmistakable at Android phone size.

### Chef Stir complete

> Edit the referenced CHEF MIX COMPLETE bowl into the immediately later CHEF STIR COMPLETE state. Preserve the exact same lavender scallop-shell bowl, camera, scale, spoon identity, navy-purple outline, lighting, transparent square canvas, and polished undersea storybook style. The six previously separate red, orange, yellow, green, blue, and violet batter pours are now visibly stirred together into one smooth clockwise rainbow spiral with all six colors still distinct and readable; add one clear central swirl and a small ribbon of batter on the spoon to show the action is finished. Keep the batter inside the bowl with no spill. No baked cake, tier, tray, frosting, candy, strawberry, candle, flame, text, character, room, background, cast shadow, checkerboard, or matte. This must read as the same physical bowl one step later, not a new design. Complete isolated RGBA cutout, fully transparent outside the bowl and spoon, generous uncropped padding, 1024x1024.

### Candy Maker Glaze complete

> Create the CANDY MAKER GLAZE COMPLETE prop for Mermaid Roshan Chapter 2, using the referenced fresh Sky Lagoon strawberries for fruit identity and the referenced finished cake for the exact candied-strawberry finish and storybook style. Show exactly FIVE complete coral-red strawberries with intact sea-green leafy crowns, neatly arranged in one row on a small lavender scallop-shell candy tray. These are the same gathered berries after coating and glazing: each has a clear glossy sugar shell, bright warm highlight, visible golden seeds, and one restrained magical sparkle, while remaining unmistakably a strawberry. All five fruits are still on the tray and NONE are on a cake yet. No cake, frosting, batter, bowl, candle, flame, text, character, utensil, room, backdrop, loose extra berry, partial berry, checkerboard, matte, or cast shadow outside the cutout. Polished 2D undersea storybook rendering with rounded navy-purple contour, broad pastel value bands, aqua-lavender shadows, upper-left light. One complete isolated RGBA cutout, fully transparent outside tray and berries, centered with generous uncropped padding, 1024x1024, readable at phone size.

### Candy Maker Place complete

> Edit the referenced approved six-tier Chapter 2 cake into the exact causal endpoint for FIVE gathered strawberries. Preserve the same physical cake: exact centered six-tier silhouette and tier proportions; exact top-to-bottom red, orange, yellow, green, blue, violet order; same scalloped pink stand and pedestal; shell crest; cream swags; pearl piping; shell medallions; gold edging; navy-purple storybook contour; texture; camera; lighting; scale; and transparent square canvas. The current cake has ten strawberries in five pairs. Replace them with EXACTLY FIVE complete whole candied strawberries total, one strawberry on each of the upper five tiers and zero on the violet base. Arrange the five intentionally in a readable alternating path to avoid the centered shell decorations: red tier left, orange tier right, yellow tier left, green tier right, blue tier left. Remove every other strawberry and leaf completely and reconstruct the frosting, pearls, swags, and tier surface beneath with no scars, fragments, gaps, duplicates, partial fruit, stray seeds, or asymmetry glitches. Each retained fruit has one intact leafy crown and matches the five-berry Candy Maker tray. Count exactly five fruits. No candle, flame, text, character, utensil, room, backdrop, checkerboard, matte, border, or cast shadow. One complete isolated RGBA cutout with fully transparent outside area, at least 24 pixels clear padding on every side, uncropped, 1024x1024, critical hero-prop quality.

## Review limits

Codex verified source hashes, runtime alpha/dimensions and safe padding, the
strict six-round diameter progression, exactly five berries on the Candy Maker
tray and exactly five on the endpoint cake, candle absence, and runtime mask
binding. Target-device composition, four-year-old comprehension, owner
final-art acceptance, and party-scene visual acceptance remain separate
master-audit gates.
