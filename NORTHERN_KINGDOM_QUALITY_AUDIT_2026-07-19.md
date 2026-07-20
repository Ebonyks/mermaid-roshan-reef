# Northern Kingdom 4.5/5 Quality and Continuity Audit — 2026-07-19

## Decision

The previous 17-family Northern kit did not satisfy the new threshold. Every
existing family scored below 4.5/5 under the stricter rubric, so none was
grandfathered. The kit was regenerated through six deterministic review
passes, obvious defects were rejected, and eight previously procedural
landmark/furniture families were added. The runtime now uses 25 authored
Northern families.

The audit ceiling is **4.9**, as requested. A score of **4.50** is the release
floor; a score below 4.00 is not acceptable even as background dressing.

## Computer rubric (4.90 maximum)

Each dimension is capped at 0.98:

1. silhouette and child-scale readability;
2. authored form, contact, and broad modeled detail;
3. palette, material separation, and lighting response;
4. ecological/functional placement continuity;
5. Mobile-render polish, repetition control, and performance fitness.

Isolated Blender Eevee renders are the first gate. The fixed 24-view Godot
Mobile-render set from `scripts/probe_northern_art_audit.gd` is the final gate.
No score may be raised merely because an asset is new.

## Individual authored-family ledger

| Family | Baseline | Final candidate | Result | Material change |
|---|---:|---:|---|---|
| pass arch | 3.40 | 4.58 | pass | planted snow base, layered stones, modeled ice rune, crystals and icicles |
| peak A | 3.20 | 4.50 | pass | three-crag silhouette, lavender/blue facets, snow crown and ledges |
| peak B | 3.30 | 4.51 | pass | distinct lean, three-crag silhouette, snow crown and ledges |
| pine A | 3.55 | 4.52 | pass | four branch tiers, broad branch pads, planted litter base and cones |
| pine B | 3.65 | 4.55 | pass | distinct height/palette rhythm, four tiers and planted base |
| pine C | 3.70 | 4.58 | pass | snow-bearing variant, four tiers and planted snow base |
| red mushrooms | 3.20 | 4.54 | pass | leaf-litter vignette, cap variation, gills, spots, rocks and ferns |
| tan mushrooms | 3.10 | 4.52 | pass | leaf-litter vignette, cap variation, gills, rocks and ferns |
| red inn | 3.75 | 4.62 | pass | roof courses, Nordic frame, stone footing, arch/step and inn sign |
| amber cottage | 3.60 | 4.56 | pass | cream gable, flower porch, warm framed window and roof courses |
| aqua cottage | 3.65 | 4.59 | pass | side wing, crystal motif, warm framed window and roof courses |
| rose cottage | 3.55 | 4.55 | pass | cream gable, heart crest, warm framed window and roof courses |
| blue cottage | 3.70 | 4.60 | pass | snow balcony, framed entry/window and roof courses |
| orange cottage | 3.60 | 4.57 | pass | side wing, wood rack, framed entry/window and roof courses |
| fjord dock | 4.12 | 4.72 | pass | individual planks, cross-bracing, stone feet, rope knots, ladder and bumpers |
| center castle | 4.08 | 4.73 | pass | open doorway, hollow keep shell, banners, stone courses, courtyard and crystals |
| wisp | 3.72 | 4.74 | pass | faceted crossed flame, orbit ring, modeled star, core and asymmetric motes |
| spirit stone | 2.80 | 4.72 | pass | tall tapered menhir, two-tier plinth, oversized modeled halo/crest and crystal crown |
| log bridge | 2.90 | 4.59 | pass | individual planks, six posts, sagging rope, knots and bank stones |
| mill house | 3.00 | 4.55 | pass | timber frame, gable, roof courses, warm windows, deck, logs and saw sign |
| mill wheel | 3.10 | 4.64 | pass | double rim, hub, eight spokes and eight functional paddles |
| forge | 2.70 | 4.52 | pass | gabled canopy, chimney, stone hearth, coals, horned anvil, tools and sign |
| street lantern | 2.90 | 4.58 | pass | stone foot, curved iron hook, cage, cap and warm modeled lamp core |
| hall centerpiece | 2.80 | 4.55 | pass | six based/capped pillars, linking ice arches, tiered fountain, jets and crystals |
| bedroom set | 2.85 | 4.68 | pass | crowned snowflake headboard, framed bed, layered quilt, pillows, braided rug, lantern and story shelf |

The lowest final candidate is 4.50; the highest is 4.74. Scores remain below
the 4.9 ceiling and reflect visible limitations of a low-poly Mobile kit.

## Runtime composition and small-item disposition

| Runtime group | Decision |
|---|---|
| sky, sunlight, lavender distance fog | retain; coherent cool daylight and depth separation |
| grass/leaf-litter terrain | retain; fungi and autumn plants only occur in the forest belt |
| dirt path and town cobble | retain; reserved corridors reject plant scatter |
| stream, fjords and stepping-stone ford | retain; water remains plant-free and both crossings stay dry/usable |
| translucent pass veil and forest mist | retain as magical effects, not physical vegetation |
| generic autumn tree/brush library | retain below snowline only; complements the authored pine family |
| town benches and garden flowers | retain; existing modeled assets are grounded on town soil beds |
| box palisades and pennant | **removed**; redundant, visually weak clutter |
| box firewood pile | **removed**; replaced narratively by modeled mill/house logs |
| box drying rack and fish | **removed**; did not clear 4.5 and was nonessential |
| text snowflake, spirit glyphs, crown and star | **removed**; replaced by modeled crests/runes |
| procedural bridge, mill, wheel, forge and lanterns | **removed from runtime**; replaced by authored GLBs |
| grand-hall structural shell, stairs and mezzanine | retain as a single architectural composition; authored centerpiece supplies the hero detail |
| box beds, cylinder rugs and generic bedroom shelves | **removed**; replaced by three instances of the authored royal-bedroom set |

## Ecological and logical continuity rules

`_north_flora_allowed()` now enforces the expanded placement contract:

- no palm, tropical, cactus, coral, kelp, seagrass, anemone, or mangrove role
  can spawn anywhere in the Northern Kingdom;
- only pine roles may spawn above the high-pass snowline;
- mushrooms/fungi may spawn only in the damp forest belt;
- no scatter may occupy the road, stream/river, spirit clearings, town street
  frontage, castle plateau, or outer terrain rim;
- explicit garden flowers remain on modeled soil beds rather than snow/stone;
- pines remain legal on snow, matching the owner rule.

Standing-stone positions also use the Northern world's Y offset before adding
local terrain height. The functional probe stores all ten positions and checks
each against the actual walk surface, preventing buried or floating ritual
stones from passing a count-only test.

The functional probe tests representative positive and negative cases so later
shared-library additions cannot silently reintroduce tropical or aquatic life.

## Generated base-art provenance

- Mode: built-in OpenAI image generation, new image.
- Output: `assets_src/concepts/northern_kingdom_quality_2026-07-19.png`
- Purpose: non-runtime shape/material reference for the deterministic Blender
  reconstruction; it does not replace protected book, voice, friend, or
  character art.
- Prompt:

> Use case: stylized-concept. Asset type: game environment and modular 3D prop
> concept sheet for a mobile Godot game. Input images: current pass arch,
> house, castle and wisp QA renders as style/subject references, not edit
> targets. Redesign the complete Northern Kingdom kit at a substantially higher
> authored-art quality while preserving these friendly storybook roles:
> magical stacked-stone snowflake pass arch, craggy snow mountains, three pine
> silhouettes, red and tan mushroom clusters, six distinct timber cottages,
> rope-and-plank fjord dock, open four-tower courtyard castle, and guiding
> wisps. Clean dark navy studio sheet; polished stylized 3D toy-diorama art;
> rounded low-poly geometry with hand-crafted asymmetry; navy/plum edge
> language; pastel aqua, lavender, berry, pine, cream, warm wood, snow and gold;
> broad modeled details practical for Mobile GLBs; every item has a distinctive
> silhouette and memorable child-readable motif. No characters, text, logos,
> trademarks, watermark, franchise symbols, primitive blockouts, plain boxes,
> palette-swap-only houses, photorealism, grim mood, microdetail or clutter.

The first live-node bedroom view then exposed the remaining primitive furniture
at roughly 3/5, so that set was rejected and regenerated as a separate authored
family.

- Mode: built-in OpenAI image generation, new image.
- Output: `assets_src/concepts/northern_bedroom_quality_2026-07-20.png`
- Purpose: non-runtime shape/material reference for
  `assets/northern/northern_bedroom_set.glb`.
- Prompt:

> Use case: stylized-concept. Asset type: isolated 3D game-prop concept sheet
> for a mobile Godot storybook game. Create a polished Northern Kingdom royal
> ice-castle bedroom set as one coherent low-poly toy-diorama asset:
> child-sized carved bed with a distinctive snowflake-and-crown headboard,
> visibly soft layered quilt with broad sculpted folds, two plump pillows,
> rounded timber/ice frame, warm bedside lantern on a tiny table, oval braided
> rug, and a compact storybook shelf. Friendly magical Nordic design, premium
> authored silhouette, rounded shapes, hand-crafted asymmetry, navy/plum
> outlines, pastel aqua/lavender/rose/cream/gold palette, warm light accents,
> clear material separation, practical broad modeled detail suitable for a
> low-draw-call Mobile GLB. Show one hero three-quarter view plus small
> front/top callouts on a dark navy studio background. No characters, no text,
> no logos, no franchise symbols, no photorealism, no flat primitive box bed,
> no microdetail, no clutter, no watermark.

## Evidence and validation

- Editable source: `assets_src/blender/northern_kingdom_kit.blend`
- Deterministic builder: `tools/build_northern_kingdom_kit.py`
- Isolated renders: `assets_src/blender/qa_northern_kingdom_kit/`
- Machine-readable ledger: `audit/northern_quality_ledger_2026-07-19.csv`
- Runtime evidence: `northern-world-review` CI artifact (24 Mobile-render PNGs)
- Functional evidence: `scripts/probe_northern.gd`

The runtime loop rejected blank/rear castle framing, exterior-fountain
occlusion, a buried standing-stone family, five bedroom-camera framings, and the
primitive bedroom set itself before acceptance. The final exact-HEAD CI run and
artifact are linked in the task handoff; the stable evidence name remains
`northern-world-review`.
