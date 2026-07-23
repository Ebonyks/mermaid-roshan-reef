# Royal Natatorium and PNW marsh 2D atlases

Generated 2026-07-22 with the OpenAI built-in image-generation tool. The two
accepted outputs were normalized from 1254 x 1254 to 1024 x 1024 with
`tools/prepare_generated_art.py`, then converted to alpha with the installed
imagegen `remove_chroma_key.py` helper using border sampling, soft matte,
thresholds 12/220, and despill.

The chroma-key source sheets in this folder are review/provenance art. Runtime
alpha atlases live at:

- `assets/castle/pool_2d/mermaid_pool_atlas.png`
- `assets/sky_lagoon/pnw_marsh_2d/pnw_marsh_atlas.png`

## Mermaid pool atlas

Reference images:

- `assets_src/concepts/sky_lagoon_quality_2026-07-20.png` — primary
  shape/palette/toy-playset style reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_01_hall_overview.png`
  — secondary Pearl Castle Mobile-render palette and cel-outline reference.

Final prompt:

> Use case: stylized-concept  
> Asset type: 4-by-4 game sprite atlas for Mermaid Roshan's Olympic swimming
> pool; 16 independently usable ambient reef and sea-creature cutouts  
> Input images: Image 1 is the primary Sky Lagoon shape, palette, and
> toy-playset style reference; Image 2 is a secondary Pearl Castle
> Mobile-render palette and cel-outline reference. Use both as style references
> only; do not copy or edit either image.  
> Primary request: create exactly sixteen original, child-friendly underwater
> pool decorations in a strict four-column by four-row grid. Row 1: branching
> coral cluster, lavender fan coral, aqua-and-gold tube coral, peach brain coral
> with shells. Row 2: orange clownfish, golden seahorse, turquoise-blue sea
> turtle, lavender manta ray. Row 3: lilac jellyfish, coral starfish with tiny
> shells, coral-red crab, violet octopus. Row 4: blue-and-gold angelfish, peach
> pufferfish, pearl oyster garden, shell-and-coral arch with bubble accents.  
> Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local
> removal; visible gutters between all sixteen cells.  
> Style/medium: polished storybook game cutouts, rounded toy-like volumes, broad
> cel bands, thin navy-purple outlines, pastel aqua/lavender/coral/gold palette,
> matte-to-satin finish, readable at phone size.  
> Composition/framing: exact 4x4 grid; one complete isolated subject centered
> in each equal square cell; consistent apparent scale; generous padding; every
> silhouette fully contained; nothing crosses a cell boundary.  
> Constraints: background must be one perfectly uniform #00ff00 with no
> shadows, gradients, texture, reflections, floor plane, vignette, or lighting
> variation. Do not use #00ff00 or bright green anywhere in any subject. No
> cast shadows, contact shadows, labels, grid lines, text, logos, watermark,
> extra subjects, human or mermaid characters. No photorealism, no black
> shadows, no white sticker borders. Keep anatomy gentle and plausible; no
> sharp teeth or scary expressions.

Cell order is row-major, indices 0 through 15 in the order listed above.

## PNW marsh atlas

Reference images:

- `assets_src/concepts/sky_lagoon_quality_2026-07-20.png` — primary
  Sky Lagoon palette/material/shape-language reference.
- `assets_src/concepts/sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png`
  — accepted planted-base and PNW silhouette reference.

Final prompt:

> Use case: stylized-concept  
> Asset type: 4-by-4 game sprite atlas for ambient Pacific Northwest marsh
> flora and wet-bank details in Sky Lagoon; 16 independently usable cutouts  
> Input images: Image 1 is the primary Sky Lagoon toy-playset palette,
> material, and shape-language reference; Image 2 is the accepted PNW
> flat-prototype silhouette and planted-base reference. Use both as style
> references only; do not copy or edit either image.  
> Primary request: create exactly sixteen original, child-friendly PNW wetland
> decorations in a strict four-column by four-row grid. Row 1: cattail clump,
> slough-sedge mound, tufted hairgrass, softstem bulrush cluster. Row 2: western
> sword fern, deer fern, horsetail cluster, yellow skunk-cabbage rosette. Row 3:
> water-lily pads with white blossoms, golden marsh-marigold cluster, mossy
> nurse log, mossy cedar stump. Row 4: rounded river stones with moss, reed
> seed-head cluster, low bog-cranberry groundcover with red berries, blue
> western iris cluster.  
> Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local
> removal; visible gutters between all sixteen cells.  
> Style/medium: polished storybook game cutouts, rounded toy-like volumes, broad
> cel bands, thin navy-purple outlines, cool jade/teal/sage foliage with warm
> coral/gold botanical accents, matte-to-satin finish, readable at phone size
> and coherent with the accepted Sky Lagoon family.  
> Composition/framing: exact 4x4 grid; one complete isolated subject centered
> in each equal square cell; consistent apparent scale; compact grounded bases;
> generous padding; every silhouette fully contained; nothing crosses a cell
> boundary.  
> Constraints: background must be one perfectly uniform #ff00ff with no
> shadows, gradients, texture, reflections, floor plane, vignette, or lighting
> variation. Do not use #ff00ff or hot magenta anywhere in any subject. No cast
> shadows, contact shadows, labels, grid lines, text, logos, watermark, extra
> subjects, faces, eyes, or mouths. No photorealism, no black shadows, no white
> sticker borders. Plants must look rooted rather than floating; no tropical
> palms, cacti, or desert species.

Cell order is row-major, indices 0 through 15 in the order listed above.
