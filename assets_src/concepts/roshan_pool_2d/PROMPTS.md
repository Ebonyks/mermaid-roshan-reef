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

## Pool-rescue companion sheets

Generated 2026-07-22 with the OpenAI built-in image-generation tool. No input
or reference images were supplied to any of these three calls.

The accepted outputs were processed with
`tools/process_pool_story_sheets.py`:

- the 1448 x 1086 ornament output was normalized to a 1024 x 768 chroma
  provenance sheet and rebuilt as twelve exact 256 x 256 runtime cells;
- the 1717 x 916 whale output was normalized to a 1024 x 512 chroma provenance
  sheet and rebuilt as eight exact 256 x 256 runtime cells;
- the 1254 x 1254 storyboard output was normalized to a 768 x 768 provenance
  sheet and rebuilt as nine exact 256 x 256 opaque runtime cells.

The processor crops six source pixels inside each generated cell to remove the
white grid gutters before resampling. For the ornament and whale runtime
atlases, it then uses the installed imagegen `remove_chroma_key.py` helper with
border sampling, soft matte, thresholds 12/220, and despill, then clears a
three-pixel transparent guard band inside every runtime cell. The opaque
storyboard keeps the untouched normalized sheet here for review while its
runtime copy uses the gutter-cropped exact cells.

Runtime atlases live at:

- `assets/castle/pool_2d/poolside_ornaments_atlas.png`
- `assets/castle/pool_2d/whale_states_atlas.png`
- `assets/castle/pool_2d/whale_rescue_storyboard.png`

### Poolside ornament atlas

Input/reference images: none.

Final prompt (verbatim):

```text
Use case: stylized-concept
Asset type: one 4-column by 3-row game sprite atlas containing exactly twelve independently usable poolside ornament cutouts for Mermaid Roshan’s enormous royal swimming pool
Primary request: create exactly twelve original, child-friendly poolside objects in a strict four-column by three-row grid. Row 1: pearl-shell bubble pump with a large star-shaped hand valve and loose hose; coral-and-gold valve pump with a big round gauge and crank; seahorse-shaped filter pump with a large wheel handle and bubble pipe; giant lavender clam-shell bench. Row 2: scallop-shell towel rack with folded aqua and coral towels; pearl life-ring stand with a shell-shaped safety float; coral-and-pearl shade umbrella; stack of starfish-shaped kickboards and shell swim toys. Row 3: conch-shell drinking fountain; woven shell toy basket; tall bubble-lantern post; large coral diving hoop on a weighted pearl base.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background; clearly visible gutters between all twelve cells.
Style/medium: polished storybook game cutouts, rounded toy-like volumes, broad cel bands, thin navy-purple outlines, pastel aqua/lavender/coral/pearl/gold palette, matte-to-satin finish, readable at phone size, coherent with a Wind-Waker-inspired pastel Pearl Castle playset without copying any franchise design.
Composition/framing: exact 4x3 grid; one complete isolated object centered in each equal rectangular cell; consistent apparent scale; generous padding; every silhouette fully contained; nothing crosses a cell boundary. The three pumps must read as friendly fixable machines from silhouette alone, each visibly different, with oversized touch-readable handles or valves and no text.
Constraints: background must be one perfectly uniform #00ff00 with no shadows, gradients, texture, reflections, floor plane, vignette, or lighting variation. Do not use #00ff00 or bright green in any object. No cast shadows, contact shadows, labels, grid lines, text, logos, watermark, extra objects, people, mermaids, faces on objects, realistic electrical hazards, sharp edges, or scary damage. No photorealism, black shadows, or white sticker borders.
```

Cell order is row-major: pearl-shell pump, coral gauge pump, seahorse pump,
clam bench, towel rack, life-ring stand, shade umbrella, swim toys, drinking
fountain, toy basket, bubble lantern, and diving hoop.

### Whale state atlas

Input/reference images: none.

Final prompt (verbatim):

```text
Use case: stylized-concept
Asset type: one 4-column by 2-row game sprite atlas containing exactly eight independently usable state cutouts of the same original young whale character for Mermaid Roshan’s royal swimming-pool rescue story
Primary request: create exactly eight chronological states of one consistent gentle young humpback whale in a strict four-column by two-row grid. Row 1: (1) dirty and unwell, resting on its side with droopy eyelids, harmless brown silt and a little soft seaweed on its back; (2) weakly lifting its head and blowing two tiny bubbles; (3) noticing help and looking hopefully toward an unseen pool pump; (4) being gently washed by clear aqua bubbles and swirling clean water. Row 2: (5) recovering with bright open eyes and most grime gone; (6) completely clean, smiling and swimming steadily; (7) affectionate friendship pose with one fin reaching forward and two heart-shaped bubbles; (8) joyful celebration pose, arcing upward with a sparkling blowhole fountain. The whale must be recognizably the same individual in every cell: rounded child-friendly body, deep periwinkle-blue back, pale lavender belly, small cream star marking near the left eye, broad flippers, soft navy-purple outline.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background; clearly visible gutters between all eight cells.
Style/medium: polished storybook game cutouts, rounded toy-like anatomy, broad cel-shaded color bands, thin navy-purple outlines, pastel aqua/lavender/periwinkle palette, matte-to-satin finish, readable at phone size, coherent with a pastel Pearl Castle playset and an adventurous cel-shaded ocean story without copying any existing franchise.
Composition/framing: exact 4x2 grid; one complete isolated whale state centered in each equal rectangular cell; consistent apparent scale and character proportions; generous padding; every silhouette, fin, tail, bubble, and water flourish fully contained; nothing crosses a cell boundary. Side-on three-quarter view with the head generally facing left for gameplay readability.
Safety and emotional tone: the first state should clearly look tired and dirty but never injured, frightening, dead, trapped, or in pain; recovery should feel warm and reassuring.
Constraints: background must be one perfectly uniform #00ff00 with no shadows, gradients, texture, reflections, floor plane, vignette, or lighting variation. Do not use #00ff00 or bright green in the whale or effects. No cast shadows, contact shadows, labels, grid text, numbers, logos, watermark, extra animals, people, mermaids, pumps, needles, wounds, bandages, tears, sharp teeth, or medical equipment. No photorealism, black shadows, or white sticker borders.
```

Cell order is row-major and chronological, indices 0 through 7 in the order
listed in the prompt.

### Whale rescue storyboard

Input/reference images: none.

Final prompt (verbatim):

```text
Use case: storyboarding
Asset type: one finished 3-column by 3-row storybook storyboard sheet containing exactly nine chronological, wordless illustrations for a preschool game story
Primary request: tell one clear nine-beat story, left-to-right and top-to-bottom, about Mermaid Roshan rescuing a gentle young whale in her enormous royal castle swimming pool. Panel 1: Roshan enters a grand shell-arched indoor pool and discovers that the water is cloudy brown-aqua with floating leaves and harmless silt. Panel 2: she sees a tired, dirty young whale resting in the pool and reacts with kind concern. Panel 3: Roshan gently reassures the whale, then notices three broken pool pumps around the deck, each indicated by a large friendly golden sparkle. Panel 4: she turns the oversized coral star valve on a pearl-shell pump and clean bubbles begin. Panel 5: she turns the big wheel on a coral gauge pump and a second clear-water jet starts. Panel 6: she pushes the large lever on a seahorse-shaped pump and all three pumps glow and run. Panel 7: clear aqua water and soft bubbles sweep the harmless silt away while Roshan watches the whale brighten. Panel 8: the now-clean, healthy whale rises and affectionately touches its nose to Roshan’s hand, with heart-shaped bubbles. Panel 9: Roshan and her new whale friend happily swim together through a sparkling clean Olympic-sized pool beneath coral decorations.
Character continuity: Roshan is the same child mermaid in every panel: warm medium skin, large brown eyes, long wavy chestnut hair with one flowing rainbow streak, lavender ruffled swim top, iridescent pastel rainbow-scaled mermaid tail, no backpack, no crown, kind expressive face. The whale is exactly consistent in every panel: rounded young humpback, deep periwinkle-blue back, pale lavender belly, small cream star marking near the left eye, broad flippers, soft navy-purple outline. Early panels show harmless brown silt and a little seaweed on the whale, never injury; late panels show it clean and joyful.
Environment continuity: one coherent Pearl Castle natatorium with a vast rectangular pool, lavender-and-pearl shell arches, aqua/coral lane accents, dry pool deck, oversized rounded toy-like pump controls, and pastel coral ornamentation. Keep the three pump designs consistent in every panel where they appear: pearl shell with coral star valve, coral-and-gold gauge with big wheel, and friendly seahorse pump with large lever.
Style/medium: polished preschool storybook storyboard, finished 2D digital illustration, broad cel-shaded bands, thin navy-purple outlines, pastel aqua/lavender/coral/pearl/gold palette, warm readable facial acting, graphic water, rounded toy-playset forms, cinematic but uncluttered, coherent with an adventurous cel-shaded ocean tale without copying any existing franchise.
Composition/framing: exact 3x3 grid of equal square panels, strong clean white gutters, one distinct story beat per panel, obvious visual cause-and-effect, alternating wide and medium shots, large readable silhouettes, no object or character crossing a panel boundary. All nine panels must be fully illustrated, unique, and clearly ordered solely by position.
Safety and emotional tone: gentle concern followed by helpful action and joyful friendship; the whale may look tired and dirty but never injured, frightening, dead, trapped, crying, or in pain. Cleaning is magical-mechanical and safe, with no chemicals or electrical hazard.
Constraints: no captions, speech balloons, letters, words, panel numbers, logos, watermark, UI, photorealism, black shadows, weapons, needles, wounds, bandages, cages, trash bags, scary grime, or copyrighted character designs. Exactly nine panels, exactly one Roshan, one whale, and at most the three specified pumps per panel.
```

Panel order is row-major and chronological, indices 0 through 8 in the order
listed in the prompt.

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
