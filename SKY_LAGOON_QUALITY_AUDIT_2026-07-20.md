# Sky Lagoon Quality Audit — 2026-07-20

## Scope and score contract

This audit covers the complete Sky Lagoon courtyard presentation in the Godot 4.4 Mobile renderer: terrain/ecology, meadow plants and trees, river and pond edges, paths and gates, playground and park, five-car train and station, Pearl Castle and bridge, and the Alpine village/cave corner. Protected book art, family voices, and friend character art are outside the regeneration scope.

The computer rubric scores silhouette authorship, modeled detail, palette/material coherence, habitat continuity, scale/readability, composition, and family repetition. The user-set automatic acceptance threshold is 4.5/5 and the computer may award at most 4.9/5. Isolated Blender renders are an iteration gate only; final scores require fixed Mobile-render runtime views. Any role below 4.5 is rejected and regenerated.

## Baseline audit

The first 38-view run (`29798773368`) completed its Sky Lagoon artifact before being superseded. It exposed a saved-night-state review defect and established these visual failures:

| Family | Baseline | Failure |
|---|---:|---|
| Train and track | 1.5/5 | Runtime boxes/cylinders, coal spheres, and unrelated carriage palettes read as a blockout rather than one authored toy consist. |
| Alpine village/cave | 1.5/5 | Near-black cave boxes, floating or repeated chalet silhouettes, generic pine reuse, and isolated festive primitives did not share the Lagoon language. |
| Pearl Castle and bridge | 2.8/5 | Stock construction pieces and dark rails weakened the focal destination; the new shell also had to preserve the Mermaid Roshan glass exactly. |
| Meadow tree family | 2.0/5 | Five imported roles included a tropical palm and palette/shape families unrelated to the Lagoon. |
| Gates, playground, and park | 2.0/5 | Thin hoops and mixed CC0 kits used unrelated proportions, colors, and edge languages. |
| Ground plants and water edges | 3.0/5 | Complete plants existed, but the old night-only evidence hid palette separation and several placed families lacked coherent modeled bases. |

Commit `572b844` forced the audit to daylight before entering level 2. GitHub Actions run `29799708746` passed import, the full analyzer, all trusted probes, and all 38 daylight captures, proving the audit itself deterministic before the rebuild.

## Ecology and continuity rules

The placement audit now uses the existing ground/water/path/landmark clearance rules and expands the art-specific habitat contract:

- Meadow grass permits the four retained GEN2 anchors plus six structurally new temperate trees, shrubs, rosettes, coral/lavender flowers, and mushrooms. Tropical palms are excluded from the Lagoon roster.
- The pond edge alone receives the weeping willow. Its modeled curtain crown frames the shoreline without entering the carved water ribbon. Reeds remain rooted at the pond and river stones remain outside the water.
- Alpine snow permits the retained rounded pine and the celebration snow pine. Meadow broadleaves, tropical trees, flowers, and mushrooms do not enter the snow field.
- Deterministic hero specimens guarantee all ten meadow-compatible tree assets occur and remain individually auditable; random groves reuse the same approved family while respecting paths, water, castle/moat, landmarks, Alpine reserve, island rim, and train clearance.
- Park, playground, station, bridge, castle, chalets, and cave are authored placements rather than random scatter. Established analytic collision and child-readable openings remain unchanged.

## Rebuild

The deterministic Blender builders create 46 Lagoon-kit GLBs plus three cloud-family GLBs and editable `.blend` sources. The palette is shared across every family: navy/plum structure, pearl/cream architecture, lavender and aqua shadows, teal, coral, butter-gold, warm wood, and restrained berry accents. The non-tree kit remains matte and texture-free. The GEN5 tree extensions reuse the approved GEN2 sculpt/UV language with one embedded 1024px texture sheet per textured role and no new external texture files. No new OmniLights are introduced. The sixteen legacy kit roles retain their semantic glTF extras and pass the existing 3,000-triangle/12-material Mobile gate; denser editable construction geometry is reduced only on the runtime export copy, with the current optimized roles at 2,776–2,880 triangles.

The final tree roster contains exactly twelve designs: the four older models the owner identified as the quality anchors, retained unchanged, plus eight new structures:

1. original rounded pine (`tree_pineRoundF`);
2. original autumn oak (`tree_default_fall`);
3. original airy fall tree (`tree_simple_fall`);
4. original round-canopy tree (`tree_fat`);
5. ancient spreading oak;
6. dancing birch grove;
7. low umbrella tree;
8. airy blossom-cloud tree;
9. dramatic windswept tree;
10. twin-trunk heart orchard;
11. domed weeping willow;
12. tiered celebration snow pine.

Four procedural/model families, including GEN4, were rejected after direct owner review because they looked assembled, repeated, primitive, or weaker than the older GEN2 sculpts. GEN5 preserves the useful authored botanical graphs but eliminates whole-tree mesh warps and simple procedural crowns. Each extension now has tapered trunks, explicit branch forks, root flares, and a different crown arrangement; the leaf masses are independently posed and Mobile-decimated fragments of the approved volumetric GEN2 sculpts, while the celebration tree returns to the approved Northern pine base. These are modeled derivatives rather than palette swaps. The eight extensions range from 1,618 to 5,597 triangles and 4–12 materials. Every textured role embeds one 1024×1024 sheet; the celebration pine is texture-free. Fixed 0°, 45°, and 135° reviews score 4.6–4.8/5 at the isolated iteration gate. Runtime acceptance still requires the fixed Mobile-render scene captures.

## Mermaid Roshan stained glass preservation

The focal glass remains the original runtime call:

`m._glass_window(c + Vector3(0, 38.0, 13.05), Vector3(0, 0, 0), 25.0)`

It still loads `res://assets/book/hall/glass_mermaid.png`. The new `lagoon_pearl_castle.glb` contains a full-depth central facade aperture and modeled gold/plum surround at that exact position; it does not contain, copy, edit, recompress, or replace the illustration. SHA-256 before integration: `94952B4C13455F7A3966DB32D7FC49F652DD5B933325AD9C3D37DE9B93C3D4A0`. The final fixed audit includes a dedicated close view of the glass.

## Image-generation provenance

The concept sheets were made with OpenAI built-in image generation and are review/design references only. Runtime geometry is reconstructed deterministically in Blender and contains no protected illustration.

### Comprehensive kit prompt

> Use case: stylized-concept. Asset type: one comprehensive 3D game-environment art-bible sheet for a mobile Godot storybook game. The first input is the current Sky Lagoon runtime and must be redesigned; the other inputs are quality and shape-language references, not edit targets. Create a polished unified Sky Lagoon modular kit showing: pearl castle exterior with an open child-readable entrance; gently arched bridge and pearl-cobble path; shell story lantern and memory-frame surround; butterfly world gate; coherent meadow plants, flowers, mushrooms, reeds, river stones, three rounded meadow tree silhouettes, park bench, hedge and fountain; six playground toys; whimsical teal/navy/gold locomotive with tender, open coach, gondola and caboose; shell-canopy station and chunky toy railway sleepers/rails; Alpine sub-biome with three varied chalets, lavender rock cave/mountain, snow-bearing pines, snowbanks, gifts, snowman and glowing cairns. Everything belongs to one premium hand-authored pastel toy-diorama world: rounded low-poly geometry, broad modeled detail, gentle asymmetry, navy/plum contour language, pearl cream, lavender, aqua/teal, coral, butter-gold, warm wood, restrained berry accents, aqua/lavender shadows, matte materials, oversized child-readable motifs, and consistent gold/shell/rainbow accents. Distinct silhouettes but one palette. Practical shapes for low-draw-call Mobile GLBs. Present organized family groups with hero three-quarter views and a few small turnarounds on a clean dark navy studio background. No characters, no protected illustrations, no text, no labels, no logos, no trademarked or franchise symbols, no photorealism, no primitive blockouts, no plain boxes, no thin wire hoops, no black silhouette objects, no neon, no microdetail, no clutter, no watermark.

### Rejected repeated-family tree prompt

> Use case: stylized-concept. Asset type: isolated 3D game-tree family concept sheet for a mobile Godot storybook game. Expand the exact Sky Lagoon shape language and palette from the input into TWELVE clearly distinct, premium authored tree assets: three rounded green meadow broadleaf trees with different trunk gestures and crown rhythms; three coral/rose flowering or sunset-canopy meadow trees with different silhouettes; two aqua-teal shoreline willows with low sweeping boughs but no mangrove roots; one compact layered lagoon evergreen; two distinct snow-bearing Alpine pines with different tier rhythm and lean; and one decorated Alpine celebration pine with restrained gold, coral, aqua and lavender ornaments. Every tree must be a complete planted asset with a modeled root/stone/leaf-litter or snow base, broad low-poly branch structure, gentle asymmetry, matte pastel materials, navy/plum contour language, warm wood trunks, and readable child-scale silhouettes. The family must feel cohesive with the pearl castle/train kit yet contain real structural variation, not recolors. Show all twelve as equally important isolated hero three-quarter views, plus a few small side callouts, organized on a clean dark navy studio background. No characters, no text, no labels, no logos, no photorealism, no flat cards, no crossed planes, no primitive lollipop trees, no black silhouettes, no tropical palms, no microdetail, no clutter, no watermark.

This sheet was rejected because it still resolved into approximately four structures repeated in three palettes.

### Rejected twelve-structure correction prompt

> Edit this Sky Lagoon tree-family concept sheet into a corrected roster of TWELVE unmistakably different tree assets, all equally important hero views. Preserve the premium pastel toy-diorama rendering, navy studio background, matte low-poly materials, warm modeled wood, navy/plum contour language, pearl/lavender planted bases, and cohesive lagoon palette. Replace the current repeated four-family/recolor pattern with twelve truly distinct botanical silhouettes and branch architectures: (1) huge ancient hollow oak with broad asymmetrical crown and exposed radial roots; (2) tall slim dancing birch with a forked pale trunk and high oval leaf cloud; (3) low umbrella meadow acacia with long lateral limbs and flat crown; (4) airy flowering cherry with many fine upward forks and separated coral blossom clouds; (5) dramatic windswept rose tree leaning sideways with a flag-shaped crown; (6) twin-trunk heart-shaped coral orchard tree with a visible central cleft; (7) full domed shoreline weeping willow with curtain boughs reaching water; (8) crooked crescent shoreline willow with one long sweeping branch and open negative space; (9) narrow layered lagoon cypress/evergreen with an irregular pagoda silhouette; (10) broad dense Alpine spruce with low snow-loaded skirts and a straight stout trunk; (11) tall crooked Alpine fir with sparse tiered arms, clear lean, and uneven snow shelves; (12) spiral celebration pine with an open helical branch rhythm, restrained ornaments and small gifts. Make height, width, trunk count, trunk gesture, crown outline, branch exposure, and base treatment clearly different in every one. Show exactly twelve main trees in a clean 4-by-3 or similarly clear gallery; do not add miniature duplicates or turnarounds. No labels, no text, no characters, no logos, no palms, no flat cards, no crossed planes, no primitive lollipops, no repeated silhouettes, no recolor variants, no black silhouettes, no photorealism, no microdetail, no clutter, no watermark.

This correction improved the concept silhouettes, but the resulting procedural models remained below the older four GEN2 assets in owner review and were rejected with their runtime roles.

### Accepted eight-extension source prompt

> Use the four approved GEN2 tree renders as the non-negotiable quality and shape-language references. Create eight genuinely different Sky Lagoon trees to join those originals rather than replace or imitate them: an ancient hollow oak with broad root arches and a layered mint crown; a dancing birch grove with three pale trunks and sparse high oval leaves; a low umbrella tree with a bent trunk and flat lateral canopy; an airy blossom-cloud tree with separated coral/rose crowns; a strongly leaning windswept tree with a flag-shaped aqua/lavender crown; a twin-trunk heart orchard with a clear central heart opening; a domed weeping willow with long tapered curtain foliage; and a tiered celebration snow pine with restrained snow, pastel ornaments, and one small gold star. Every design needs a different trunk graph, height/width ratio, crown rhythm, negative-space pattern, and habitat read while sharing warm modeled wood, matte pastel mint/aqua/lavender/coral/butter materials, and navy/plum contour language. Isolated premium 3D concept art on a clean white or studio background; no text, no characters, no palms, no flat cards, no crossed planes, no lollipop primitives, no repeated silhouettes, no photorealism, no clutter, no watermark.

The GEN3 runtime meshes made from this source were rejected by the owner. GEN4 also failed the subsequent Mobile scene audit: several silhouettes collapsed edge-on, the birch read as three flat saplings, and the ancient-oak crown overwhelmed its trunk. Its source and QA files were removed rather than retained as production assets.

### Accepted GEN5 correction prompt

> Create a clean professional concept sheet for eight NEW, genuinely distinct stylized 3D tree assets for the Sky Lagoon of a pastel storybook game. The attached sheet contains the four APPROVED existing GEN2 trees; use their high-quality sculpted branch forks, faceted hand-cut planes, thick readable outlines, soft pastel toy-diorama color blocking, and child-readable proportions as the quality anchor, but do not duplicate their silhouettes. Show exactly eight additional tree designs in a 4x2 grid on a neutral pale blue background, each fully visible from roots to crown, primarily front/three-quarter view, with a small clear label beneath: Ancient Spreading Oak — massive visible bifurcating trunk, broad asymmetrical crown with negative spaces; Dancing Birch Grove — three curved white-barked trunks sharing one root mound, separate airy leaf crowns, never flat lollipops; Low Umbrella Tree — short thick trunk, wide layered parasol canopy; Blossom Cloud Tree — gnarled branching visible through multiple rounded blossom clusters, broad in both front and side silhouette; Windswept Cliff Tree — visibly bent trunk and long flag-shaped canopy, strong directional silhouette but substantial depth; Twin-Heart Orchard — two intertwined trunks and two clearly separated heart-like crowns, restrained color; Weeping Willow — wide branching crown with irregular hanging curtains and visible trunk gaps; Celebration Snow Pine — layered conifer with sculpted snow shelves, subtle ornaments, star, still clearly a tree. Make every botanical graph and silhouette unmistakably different. Avoid pebble/blob crowns, thin edge-on foliage, coral-like leaf spikes, repeated copies, flat cutouts, excessive rainbow noise, and primitive cylinders. Present them as believable modeled asset concepts with visible trunk-to-branch logic, broad multi-angle volume, faceted cel-shaded forms, navy-purple outlines, aqua/lavender shadows, and a consistent lagoon palette of coral, mint, aqua, lavender, butter yellow, and warm bark. No characters, buildings, UI, watermarks, logos, or extra trees.

The corresponding runtime models are rebuilt by `tools/build_sky_lagoon_tree_gen5.py`. The builder combines new branch/root graphs with decimated GEN2 crown sculpt stock and the approved Northern pine, then exports deterministic Mobile GLBs. `tools/render_glb_turntable_batch.py` preserves embedded base-color textures while producing the fixed three-angle review evidence in one Blender session.

## Final evidence

Run `29806506063` proved the GEN3 branch technically green but visually rejected. Run `29810144363` likewise proved GEN4 technically green while its 51-view artifact exposed an empty lavender-flower close-up, a castle-blocked race-gate view, and tree silhouettes that still failed owner review. GEN5 retains bounds-fitted role cameras, deterministic meadow hero anchors, tree-only close-up isolation, and transient-particle suppression; it also gives all ground-flora roles deterministic audit anchors and uses adaptive framing for both race arches. Pending the new exact-HEAD Mobile-render audit. Scores and any further reject/regenerate decisions are tracked in `audit/sky_lagoon_quality_ledger_2026-07-20.csv`.
