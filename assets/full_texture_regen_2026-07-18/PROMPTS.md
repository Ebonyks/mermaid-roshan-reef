# Generation Direction and Prompt Contract

All raster generations used the book-derived family guidance in
`ART_STYLE_GUIDE.md`, the failure analysis in
`FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md`, and the user's accumulated
human-review notes.

## Shared Raster Direction

> Mermaid Roshan storybook game asset; confident cel-shaded painted shape;
> broad pastel color blocks; dark navy or purple contour; aqua and lavender
> shadow accents; matte surface; child-readable silhouette at phone size;
> orthographic or flat presentation; no text, logos, photorealism, glossy 3D,
> stock clip-art styling, cast shadow, unrelated prop, baked ground island, or
> mixed above-water/underwater biome.

Tileable material prompts also required matched opposite edges, low-frequency
variation, and a repetition test. Isolated sprites required complete anatomy
and transparent-background extraction without colored matte spill.

## Role-Specific Constraints

| Roles | Required direction |
|---|---|
| R007-R008 | Graphic underwater caustics and distant seamount bands; no foreground objects |
| R032-R034 | Broad castle-kitchen stone, floor, and painted wood materials; rounded hand-painted marks |
| R044 | Butterfly meadow surface only; no flowers from another biome; three deployment variants |
| R050 | Dark indigo dungeon paving with readable lavender joints and restrained star marks |
| R066-R067 | Separate functional kart boost and finish signals; no Christmas or gate motifs |
| R071-R077 | Complete, isolated picture-game objects with matching contour weight |
| R075 | Empty Christmas tree with no ornaments |
| R076 | Completed version of R075 with exactly five ornaments |
| R078-R079 | One fish body plus five independent, anatomically placed fin categories |
| R080 | Complete butterfly: four wings, six legs, two antennae; no cropped or half-drawn anatomy |
| R084 | Five independent ornaments, including a distinct star topper |

## Iteration 2 Development Prompt - R044 Calm Mass-Placement Base

The following built-in image-generation edit used
`source_generations/accepted/R044_BUTTERFLY_WORLD_PLANET_SURFACE__ground_source.png`
as its edit target and style anchor. The raw result is retained as
`source_generations/accepted/R044_BUTTERFLY_WORLD_PLANET_SURFACE__calm_ground_source.png`;
the mobile-normalized candidate is
`textures/R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground_calm.png`.
It is unscored development art and is not included in the original review
ledger.

> Use case: stylized-concept. Asset type: seamless tileable game texture for a
> mobile children's storybook meadow. Create a calmer low-flower base variant
> of the R044 ground for repeated Butterfly World placement. Paint an
> orthographic lavender meadow with soft aqua and mint mossy patches, a few
> tiny gold pebble marks, and restrained navy curved accents. Limit coral-pink
> flowers to no more than eight percent of the image, using only small widely
> separated petal motifs; cool colors must occupy at least two thirds. Preserve
> the source's hand-painted gouache texture, rounded shapes, matte pastel
> finish, contour weight, and child-friendly visual language. Distribute detail
> evenly with no focal point or horizon, and match both opposite edge pairs for
> seamless tiling. Use lavender `#a87dd6`, aqua `#45c4c7`, mint `#80d48f`,
> cream `#f5ebd1`, restrained gold `#f5b838`, navy/purple `#4a4f78` and
> `#1a1238`, with coral `#ffa399` used sparingly. No butterflies, characters,
> buildings, text, logos, watermark, shadows, lighting gradients,
> photorealism, noisy micro-detail, giant cropped flowers, or warm-color
> dominance.

## Procedural 3D Direction

The Blender generator uses deterministic authored geometry rather than image
generation. Every family follows these rules:

1. Model the silhouette and gameplay function before surface decoration.
2. Use rounded low-poly forms and embedded matte materials; no external PBR maps.
3. Separate interactive pieces and keep family variants asymmetric.
4. Give creatures explicit named anatomy for automated validation.
5. Add navy/lavender geometric edge accents where bright Mobile-renderer scenes
   would otherwise erase the silhouette.
6. Keep every candidate below the mobile triangle and material budgets.

The first R080 butterfly generation was rejected because only four legs were
visible. It remains in `source_generations/rejected/`; the corrected accepted
source visibly contains six legs.
