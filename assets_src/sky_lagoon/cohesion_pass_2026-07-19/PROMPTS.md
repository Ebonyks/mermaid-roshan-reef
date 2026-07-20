# Generation prompts

All new sheets used the built-in OpenAI image-generation tool. No deterministic
seed or model build identifier was exposed. Prompts were run separately by
asset family. The locomotive sheet used as the companion-car style reference is
`gen2/generated/r021_locomotive_identity/turnaround_v1_repair_1024.png`.

## Butterfly World gate

```text
Use case: stylized-concept
Asset type: production turnaround sheet for a low-poly Godot 4 mobile 3D gateway
Primary request: design a complete Butterfly World swim-through gate for Mermaid Roshan Sky Lagoon. It must read immediately as one butterfly, not disconnected rings: one rounded navy-purple body, clear head, two curled antennae, and four broad open wing frames. The empty center is a generous playable passage and all decoration stays outside the opening.
Style/medium: polished cel-shaded 3D toy-playset model reference, rounded low-poly geometry, strong navy-purple contour language, simple large color blocks, aqua and lavender shadows, matching a pastel storybook diorama for a non-reading four-year-old
Composition/framing: four consistent orthographic views on one clean light neutral sheet: front, side, rear, and three-quarter. Keep identical topology and proportions in every view. No labels or text.
Color palette: coral-pink upper wings, aqua lower wings, lavender secondary panels, warm gold shell/rainbow accents, navy-purple structural rims
Materials/textures: matte painted wood/resin toy, subtle facet planes, no realistic metal, no noisy textures
Functional constraints: passage at least half the total width and about two-thirds total height; thick readable wing rims; rooted plinths at both sides; compact shell motifs only at the bases; no opaque membrane crossing the passage; silhouette legible at phone scale; practical for a low-poly mesh under 3000 triangles
Avoid: separate hoops, thin wire loops, butterfly half-drawing, insect anatomy errors, wing clipping, giant opaque panels, tiny filigree, black background, cast shadow, scene environment, characters, words, logos, watermark
```

## Pearl Castle exterior

The first output used this prompt and was rejected because its central recess
was near-square:

```text
Use case: stylized-concept
Asset type: production turnaround sheet for a low-poly Godot 4 mobile castle exterior shell
Primary request: design one cohesive Pearl Castle exterior for Mermaid Roshan Sky Lagoon, replacing a facade assembled from generic cubes. It is a compact child-readable fairy-tale castle with one broad central keep, two rounded corner towers, one unmistakable arched front door, a deep protected central stained-glass recess, shell crowns, restrained rainbow inlay, and large clean architectural masses.
Style/medium: polished cel-shaded 3D toy-playset model reference, rounded low-poly geometry, navy-purple contour language, pastel storybook diorama, simple readable silhouettes matching aqua/coral/lavender playground and plant assets
Composition/framing: four consistent orthographic views on one clean light neutral sheet: front, side, rear, and three-quarter. Identical architecture in every view. No labels or text.
Color palette: pearl lavender masonry, deeper violet roofs and shadow bands, aqua window glass, warm coral door accents, restrained gold trim, small rainbow and scallop-shell motifs integrated into cornices and tower crowns
Materials/textures: matte painted resin and softly faceted pearl stone; large stone courses only, no photoreal brick
Functional constraints: wide rectangular collision-friendly body; central doorway clearly openable and large enough for child navigation; central stained-glass recess must accept the existing protected book image without changing it; no baked image or character in the recess; architecture practical under roughly 6000 triangles; front silhouette readable from far across the island
Avoid: generic stacked boxes, overly tall thin towers, dense crenellation pickets, tiny windows, realistic medieval grime, princess character art, copied franchise symbols, text, logos, watermark, environment, cast shadow
```

The selected v2 was a targeted edit:

```text
Keep the castle architecture, palette, materials, motifs, camera views, proportions, and all four-view layout unchanged. Change only the large central front window/recess in the front and three-quarter views: replace its near-square shell window with a tall vertical pointed-arch portrait recess, approximately 2:1 height-to-width, deep enough to accept the existing protected Mermaid Roshan book-art stained-glass portrait without cropping or alteration. Use a broad gold and navy-purple surround with a small shell crest above it. The rear and side views should remain structurally consistent with that taller front recess. No character image inside the recess; use plain aqua placeholder glass only. Preserve the large coral arched door below.
```

## Alpine chalet family

```text
Design a coherent family of three small snowy Sky Lagoon chalets: a compact cottage, a slightly taller workshop, and a tiny station-adjacent lodge. They share one construction language but have distinct silhouettes. Each has a real doorway, broad windows, visible wall thickness, snow loaded onto a pitched roof, and a grounded stone or lavender plinth. Use polished cel-shaded rounded low-poly toy geometry, navy-purple outlines, icy aqua, pale lavender, soft coral, snowy white, restrained warm gold trim, and one naturally integrated shell vent or rainbow muntin per building. No primitive box-plus-cone construction, random Christmas bulbs, warm-weather flowers, isolated leaves, floating snow slabs, text, characters, logos, or watermark.
```

## Alpine mountain and cave kit

```text
Design a coherent Sky Lagoon Alpine terrain kit that replaces stacked primitive crags: one broad asymmetrical mountain crown, two rounded foothill rocks, one playable cave-mouth shell with believable side walls and roof, one low snowbank cluster, and one child-readable glowing trail cairn. Use rounded low-poly lavender-gray rock, aqua shadow planes, supported white snow, and a clean production sheet with one assembled example. Only complete rooted multi-tier snowy pine saplings are allowed. No tropical plants, mushrooms, flowers, single leaves, giant black boulders, stacked cubes, floating roofs, text, characters, logos, or watermark.
```

## Story lantern

```text
Design a stout Sky Lagoon story lantern with a broad grounded plinth, one tapered navy-purple post, a large warm glowing pearl protected by a simple scallop-shell hood, and a small rainbow inlay around the base. Use polished cel-shaded rounded low-poly toy geometry and four consistent views. Keep the silhouette readable at distance and under 1500 triangles. Avoid thin poles, realistic Victorian lamps, chains, tiny filigree, isolated leaves, multiple bulbs, text, logos, watermark, environment, or cast shadow.
```

## Protected-memory frame

```text
Design a freestanding Sky Lagoon story-memory frame that holds an existing vertical protected book image without altering, recoloring, cropping, relighting, or covering it. Use a deep 2:3 portrait recess, broad navy-purple structural sides, grounded feet, a scallop-shell crown, and restrained rainbow sill. The image opening stays empty, remains a separate unshaded runtime plane, and has no overlapping ornament. Four consistent views; under 1800 triangles; no generated picture, text plaque, floating support, isolated leaf, logo, or watermark.
```

## Train companion cars

```text
Using the accepted teal/navy/gold/coral locomotive sheet as a style and mechanical-proportion reference, design four companion cars: a compact tender, an open-sided passenger coach with a broad bench and generous doorway, a low open-top gondola, and a cheerful caboose. Use one shared wheel, coupler, chassis-height, roof-curve, and trim system. Show side and three-quarter views on one production sheet. All wheel centers and couplers align; no characters or cargo; under 2500 triangles per car; no mismatched wheel sizes, sealed passenger coach, realistic grime, text, logos, or watermark.
```

## Path, bridge, and water edge kit

```text
Design a coherent Sky Lagoon path-and-water-edge family: one pearl-cobble path strip, one low child-safe bridge, one varied riverbank stone cluster, and one pond-edge stone/reed socket. Use rounded low-poly pearl lavender and aqua stone, deeper violet undersides, restrained shell fasteners, broad shell-shaped bridge curbs, and large simple facets. Riverbank clusters need 5-8 varied grounded stones; the pond socket supports a complete multi-stem reed clump, not a single leaf. Avoid generic gray rocks, repeated stone lines, floating slabs, thin rails, isolated leaves, dense noise, text, characters, logos, or watermark.
```
