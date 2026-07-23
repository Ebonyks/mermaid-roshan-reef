# Dirty Castle Cleanup 2D Generation Prompts

Generated 2026-07-22 with the OpenAI built-in image-generation tool. The tool
was used in its default built-in mode. Runtime transparency was produced by
local chroma-key removal; no CLI/API fallback or native-transparency model was
used. Expanded atlases used sampled-border chroma removal, soft matte, and
despill; the feedback, bunny-action, and progress sheets also used a one-pixel
edge contraction after edge QA.

Protected project art was supplied only as an identity, palette, or environment
reference. The originals were not edited.

## 2026-07-23 exact-scene resemblance correction

The six original room-skin atlases remain in this folder as rejected concept
history. They were useful for story and mess vocabulary, but every one of the
41 scene-bound outputs failed the strict object-resemblance gate because the
objects had been redrawn from prose.

Their runtime replacements are not image-generation redraws. Blender renders
the exact shipped GLBs into `scene_references/objects/*.png` with
`tools/render_dirty_castle_references.py`; `tools/process_dirty_castle_2d.py`
then preserves those clean pixels and composites a separate grime decal. This
keeps 55 auxiliary sprites from the original generation while ensuring all 41
skin candidates use the actual game object as their base.

### Reusable grime decal

Built-in image-generation output:
`scene_references/overlays/grime_cluster_chroma.png`

Locally keyed transparent derivative:
`scene_references/overlays/grime_cluster_alpha.png`

```text
Create one square 2D game-art decal sheet containing only cheerful, harmless
castle-cleaning mess marks on a perfectly flat solid #00ff00 chroma-key
background. Include exactly three separate soft lavender dust curls, two small
cream flour-or-soap wipe streaks, and a loose handful of tiny coral, aqua, and
cream crumbs. Keep every mark isolated with generous clear space, broad
phone-readable shapes, soft cel-painted pastel shading, and fine navy-purple
accents matching a cute Mermaid Roshan storybook castle. Mess only: no object,
furniture, room, tool, character, face, dust bunny, soot sprite, text, logo,
frame, floor, shadow, glow, transparency, or background variation. Do not use
#00ff00 inside any mark.
```

The decal is intentionally not a source of object geometry. Its alpha pixels
are resized and positioned over the exact GLB render, and the resulting
difference mask is retained in the audit output.

## Reference roles

- `gen2/turnarounds/roshan_v2/front.png`: Mermaid Roshan identity reference.
- `assets_src/daddy_master.png`: Daddy Mermaid identity reference.
- `assets/book/baby_eagle.png`: Baby Eagle identity reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_01_hall_overview.png`:
  current Pearl Castle Grand Hall environment and material reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_02_throne_focal.png`:
  current throne focal environment reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_05_toy_room.png`:
  current Toy Room layout reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_12_royal_library.png`:
  current Royal Library layout reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_15_pantry.png`:
  current Pantry layout reference.
- Earlier generated cinematic frames: continuity references only.

## Sprite atlas 01 — dirty targets

Output:
`raw/dirty_targets_atlas_chroma.png`

```text
Use case: stylized-concept
Asset type: 2D game sprite atlas source for Mermaid Roshan's Pearl Castle cleanup play section
Input images: Image 1 is a style and material reference for the current Pearl Castle only; do not copy its camera or render it as a scene
Primary request: create exactly six separate child-friendly DIRTY TARGET sprites arranged in a strict 3 columns by 2 rows grid: (1) a low lavender-gray dust-bunny pile with three curled puffs, (2) one triangular corner cobweb with a few pearl-like dust beads, (3) a short trail of three muddy shoe or fin-shaped footprints, (4) a broad chalky gray-purple floor scuff smear, (5) one small coral-pink sticky juice spill with two droplets, (6) one dull cloudy window-smudge patch drawn as opaque pale streaks. Every cell contains exactly one isolated target and no cleaning tool.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal; no dividers, labels, frames, floor plane, shadows, gradients, texture, reflections, or lighting variation in the background
Style/medium: polished flat-color storybook game illustration; broad cel-shaded shapes; fine navy-purple contour; matches the Pearl Castle's pearl, lavender, aqua, coral and restrained gold language; immediately readable on a small phone
Composition/framing: square atlas, strict evenly spaced 3x2 grid, each target centered inside its own equal cell with generous padding and no overlap; full silhouette visible
Lighting/mood: gentle, playful, safe, mildly messy rather than disgusting
Constraints: one target per cell; no characters; no faces; no text; no watermark; no logo; crisp opaque edges; no cast shadows; do not use #00ff00 anywhere in the subjects
Avoid: insects, mold, garbage, food rot, photoreal dirt, scary grime, dense texture, tiny details, extra objects, room scenery, shadows touching the key background
```

## Sprite atlas 02 — cleaning tools

Output:
`raw/cleanup_tools_atlas_chroma.png`

```text
Use case: stylized-concept
Asset type: 2D game sprite atlas source for Mermaid Roshan's Pearl Castle cleanup play section
Input images: Image 1 is a style and material reference for the current Pearl Castle only; do not copy its camera or render it as a scene
Primary request: create exactly six separate child-friendly CLEANING TOOL sprites arranged in a strict 3 columns by 2 rows grid: (1) a pearl fan-shell bucket filled with pale aqua soap suds and a gold handle, (2) a chunky coral-pink star-shaped sponge, (3) a short rainbow-fiber mop with a lavender shell handle, (4) a small round shell-handled scrub brush with aqua bristles, (5) a friendly rounded aqua spray bottle with a simple embossed shell mark and no writing, (6) a matching pearl dustpan and short lavender broom presented together as one tool set. Every cell contains exactly one tool or paired tool set and no dirt target.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal; no dividers, labels, frames, floor plane, shadows, gradients, texture, reflections, or lighting variation in the background
Style/medium: polished flat-color storybook game illustration; broad cel-shaded shapes; fine navy-purple contour; matches the Pearl Castle's pearl, lavender, aqua, coral and restrained gold language; immediately readable on a small phone
Composition/framing: square atlas, strict evenly spaced 3x2 grid, each tool centered inside its own equal cell with generous padding and no overlap; full silhouette visible; handles kept inside cells
Lighting/mood: cheerful, inviting, safe collaborative cleanup play
Constraints: one tool per cell; no characters; no faces; no text; no watermark; no logo; crisp opaque edges; no cast shadows; do not use #00ff00 anywhere in the subjects
Avoid: branded cleaners, hazardous warning symbols, realistic chemicals, sharp objects, clutter, tiny details, extra objects, room scenery, shadows touching the key background
```

## Sprite atlas 03 — cleanup feedback

Output:
`raw/cleanup_feedback_atlas_chroma.png`

```text
Use case: stylized-concept
Asset type: 2D game sprite atlas source for Mermaid Roshan's Pearl Castle cleanup feedback effects
Input images: Image 1 is a palette and graphic-shape reference for the current Pearl Castle only; do not copy its camera or render it as a scene
Primary request: create exactly six separate opaque flat-graphic CLEANUP FEEDBACK sprites arranged in a strict 3 columns by 2 rows grid: (1) a cluster of five pale-aqua soap bubbles with thick readable rims, (2) a four-point restrained-gold sparkle burst with two tiny companion twinkles, (3) one broad coral-and-aqua curved wipe swoosh, (4) a low pile of pearl-white soap foam made of countable rounded lobes, (5) a circular lavender-aqua clean-shine ring with four stars, (6) a celebratory pearl fan-shell badge topped by a small gold crown and surrounded by three twinkles. Every cell contains exactly one feedback symbol and no text.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal; no dividers, labels, frames, floor plane, shadows, gradients, texture, reflections, glow haze, or lighting variation in the background
Style/medium: polished flat-color storybook game illustration; bold opaque cel-shaded shapes; fine navy-purple contour; Pearl Castle pearl, lavender, aqua, coral and restrained gold palette; immediately readable on a small phone
Composition/framing: square atlas, strict evenly spaced 3x2 grid, each effect centered inside its own equal cell with generous padding and no overlap; full silhouette visible
Lighting/mood: bright, magical, satisfying, gentle celebration
Constraints: one symbol per cell; keep all effects opaque and graphic rather than translucent or smoky; no characters; no faces; no text; no watermark; no logo; crisp edges; no cast shadows; do not use #00ff00 anywhere in the subjects
Avoid: bloom haze, transparent mist, realistic liquid, lens flare, particles crossing cells, clutter, tiny details, extra objects, room scenery
```

## Cinematic 01 — arrival and discovery

Output:
`cinematic_raw/frame_01_arrival_dirty.png`

```text
Use case: illustration-story
Asset type: opening 2D cinematic frame and character-consistency anchor for Mermaid Roshan: Reef of Light
Input images: Image 1 is Mermaid Roshan's identity reference; Image 2 is Daddy Mermaid's identity reference; Image 3 is Baby Eagle's identity reference (preserve the bird's turquoise, yellow and pink plumage, big eyes and black-gray beak, but the backpack is not part of this scene); Image 4 is the current Pearl Castle Grand Hall environment reference
Primary request: a warm wide storybook cinematic frame showing Mermaid Roshan arriving inside her castle with Daddy Mermaid and Baby Eagle and all three gently surprised to find that the hall needs cleaning
Scene/backdrop: recognizable Pearl Castle Grand Hall from Image 4, with cream shell-capital columns, lavender stone walls, burgundy central carpet, gold trim, shell fixtures, staircase and rainbow throne arch; add only playful readable mess: a few lavender dust bunnies, one corner cobweb, three muddy footprints, a chalky floor scuff and one small coral-pink sticky spill
Subject: Mermaid Roshan is the clear central child hero, full body and rainbow tail visible, matching Image 1's face, brown hair with rainbow forelock, tiara, pink bodice and lavender-rainbow tail; Daddy Mermaid is beside her matching Image 2's long brown-and-teal hair, glasses, pointed ears, crown, navy-gold jacket, turquoise cape and rainbow tail; Baby Eagle flies at Roshan's shoulder matching Image 3's plumage and facial design but without backpack; all look concerned-but-hopeful, never upset
Style/medium: polished modern flat-color anime storybook illustration, soft painterly cel bands, fine navy-purple outlines, consistent with the game's book-derived character art and pastel toy-diorama castle
Composition/framing: wide 16:9 cinematic composition; camera just inside the entrance looking toward the throne; trio grouped in the lower foreground with faces and full silhouettes readable; dirty targets clearly distributed in midground; generous clear upper space; no panel borders
Lighting/mood: high-key aqua-lavender morning light, family warmth, gentle discovery, emotionally safe and inviting
Constraints: exactly these three characters and no others; preserve character identities, facial features, hair, crowns, clothing, tail colors and proportions from their references; Baby Eagle has two wings and two legs, no backpack; Roshan remains a mermaid child; Daddy remains a mermaid; no dialogue text, captions, logos, watermark or UI; no pool
Avoid: redesigns, duplicated characters, extra limbs, human legs, frightened expressions, disgusting grime, garbage, mold, insects, gloomy horror light, photorealism, dense clutter, Zelda symbols or copyrighted game motifs
```

## Cinematic 02 — choose tools

Output:
`cinematic_raw/frame_02_choose_tools.png`

```text
Use case: illustration-story
Asset type: 2D cinematic frame 02 of 06 for Mermaid Roshan: Reef of Light
Input images: Image 1 is the approved cinematic continuity anchor and must control character rendering, palette and castle treatment; Images 2, 3 and 4 are identity references for Mermaid Roshan, Daddy Mermaid and Baby Eagle; Image 5 is the current Pearl Castle Grand Hall environment reference
Primary request: continue the same story moments later as the family makes a cheerful cleanup plan and shares the tools
Scene/backdrop: the same recognizable dirty Pearl Castle Grand Hall as Image 1, cream shell-capital columns, lavender stone walls, burgundy carpet, gold trim, staircase and rainbow throne arch; the playful dirt targets remain visible but secondary
Subject: Mermaid Roshan at center happily lifts the coral-pink star sponge; Daddy Mermaid beside her holds the rainbow mop upright and steadies the pearl shell bucket of aqua suds; Baby Eagle hovers close and proudly carries the small shell scrub brush in both feet; all three exchange confident warm smiles, ready to work together
Style/medium: exactly the same polished modern flat-color anime storybook illustration, soft painterly cel bands and fine navy-purple outlines as Image 1
Composition/framing: wide 16:9 cinematic composition, medium-wide group shot from slightly below eye level; full upper bodies and mermaid tails readable; cleaning tools large and unmistakable; clear depth back to the staircase; no panel borders
Lighting/mood: high-key aqua-lavender morning light, family teamwork, upbeat and emotionally safe
Constraints: exactly these three characters and no others; preserve Image 1 character faces, hair, crowns, clothing, plumage, tail colors, proportions and castle palette; Baby Eagle has two wings and two legs and no backpack; Roshan remains a mermaid child; Daddy remains a mermaid; no dialogue text, captions, logos, watermark, UI or pool
Avoid: character redesigns, duplicated characters or tools, extra limbs, human legs, arguments, dangerous chemicals, scary grime, photorealism, dense clutter, Zelda symbols or copyrighted game motifs
```

## Cinematic 03 — Roshan cleans the rainbow

Output:
`cinematic_raw/frame_03_roshan_window.png`

```text
Use case: illustration-story
Asset type: 2D cinematic frame 03 of 06 for Mermaid Roshan: Reef of Light
Input images: Image 1 is the approved cinematic continuity anchor; Image 2 fixes the cleanup tools and current character rendering; Image 3 is Mermaid Roshan's identity reference; Image 4 is Baby Eagle's identity reference; Image 5 is the current Pearl Castle throne focal environment reference
Primary request: continue the same story with a joyful action close-up of Mermaid Roshan cleaning the castle's rainbow throne window while Baby Eagle helps
Scene/backdrop: the Pearl Castle throne landing, with cream shell columns, lavender stone, restrained gold, the rainbow arch and shell throne; the left half of the rainbow window is still dull with pale chalky smudges while the right half Roshan has wiped is bright and clean, creating one instantly readable before-and-after surface
Subject: Mermaid Roshan floats beside the window, matching the prior frames, making one broad circular wipe with the coral-pink star sponge; her brown hair and rainbow forelock sweep with the motion, and she smiles with concentration; Baby Eagle hovers lower beside the pearl shell bucket and tips one harmless soap bubble toward her; both are actively helping
Style/medium: exactly the same polished modern flat-color anime storybook illustration, soft painterly cel bands and fine navy-purple outlines as Images 1 and 2
Composition/framing: wide 16:9 cinematic composition, dynamic medium shot angled slightly upward; Roshan is the large clear focal hero, full upper body and most of her tail visible; rainbow window fills the background; Baby Eagle and bucket remain fully readable; no panel borders
Lighting/mood: bright aqua-lavender light, sparkling progress, playful focus and satisfaction
Constraints: exactly Mermaid Roshan and Baby Eagle, no Daddy in this focused shot and no other characters; preserve faces, hair, crowns, clothing, plumage, tail colors and proportions from the continuity references; Baby Eagle has two wings and two legs and no backpack; no dialogue text, captions, logos, watermark, UI or pool
Avoid: character redesigns, duplicates, extra limbs, human legs, falling or danger, hazardous chemicals, disgusting grime, photorealism, dense clutter, glow haze obscuring faces, Zelda symbols or copyrighted game motifs
```

## Cinematic 04 — Daddy cleans the floor

Output:
`cinematic_raw/frame_04_daddy_floor.png`

```text
Use case: illustration-story
Asset type: 2D cinematic frame 04 of 06 for Mermaid Roshan: Reef of Light
Input images: Image 1 is the approved cinematic continuity anchor; Image 2 fixes the cleanup tools and character rendering; Image 3 is Daddy Mermaid's identity reference; Image 4 is the current Pearl Castle Grand Hall environment reference
Primary request: continue the same story with a lively focused shot of Daddy Mermaid mopping the Pearl Castle floor
Scene/backdrop: the lower Grand Hall beside the burgundy carpet, with cream shell-capital columns, lavender stone floor and restrained gold; a small remaining trail of three muddy footprints and a chalky scuff are clearly visible ahead of the mop; behind it the floor is clean with one restrained four-point sparkle and a soft readable reflection
Subject: Daddy Mermaid, matching prior frames, leans into one broad sweeping mop stroke with both hands on the lavender shell handle and rainbow-fiber mop head; his long brown-and-teal hair, turquoise cape and rainbow tail curve with the movement; his glasses, crown, pointed ears, navy-gold jacket and warm determined smile remain exact and readable; the pearl shell suds bucket sits safely nearby
Style/medium: exactly the same polished modern flat-color anime storybook illustration, soft painterly cel bands and fine navy-purple outlines as Images 1 and 2
Composition/framing: wide 16:9 cinematic composition, energetic three-quarter low angle; Daddy is the single full-body hero crossing the frame diagonally; mop stroke and clean-versus-dirty floor path are unmistakable; no panel borders
Lighting/mood: bright aqua-lavender light, capable caring parent, fun teamwork and satisfying progress
Constraints: exactly Daddy Mermaid and no other characters in this focused shot; preserve his face, glasses, pointed ears, hair, crown, jacket, cape, rainbow tail colors and proportions from the continuity references; he remains a mermaid with no human legs; no dialogue text, captions, logos, watermark, UI or pool
Avoid: character redesigns, duplicates, extra limbs, human feet, slipping or danger, angry expression, hazardous chemicals, disgusting grime, photorealism, dense clutter, glow haze, Zelda symbols or copyrighted game motifs
```

## Cinematic 05 — Baby Eagle clears the corner

Output:
`cinematic_raw/frame_05_eagle_dust.png`

```text
Use case: illustration-story
Asset type: 2D cinematic frame 05 of 06 for Mermaid Roshan: Reef of Light
Input images: Image 1 is the approved cinematic continuity anchor; Image 2 fixes the cleanup tools and character rendering; Image 3 is Baby Eagle's identity reference; Image 4 is the current Pearl Castle Grand Hall environment reference
Primary request: continue the same story with Baby Eagle's delightful solo cleanup hero moment
Scene/backdrop: an upper corner of the same Pearl Castle Grand Hall with cream shell-capital column, lavender stone, gold-trimmed balcony rail and one last triangular cobweb; below, two small lavender dust-bunny curls sit beside the pearl dustpan
Subject: Baby Eagle, matching the prior frames, hovers in a stable cheerful pose; one foot holds the little lavender shell scrub brush as the bird sweeps the final cobweb from the corner, while the breeze from two fully spread pink-and-black wings gently nudges the dust bunnies toward the pearl dustpan; the turquoise-yellow-pink plumage, big eyes, black-gray beak and pink crest remain exact; the expression is proud and helpful
Style/medium: exactly the same polished modern flat-color anime storybook illustration, soft painterly cel bands and fine navy-purple outlines as Images 1 and 2
Composition/framing: wide 16:9 cinematic composition, playful medium action shot; Baby Eagle large and centered with complete silhouette, two wings and both feet visible; cobweb, dust bunnies, brush and dustpan form one simple readable action path; no panel borders
Lighting/mood: bright aqua-lavender light, small helper making a big contribution, joyful and emotionally safe
Constraints: exactly Baby Eagle and no other characters in this focused shot; preserve the bird's face, plumage placement, crest, beak and proportions; no backpack; exactly two wings and two legs; no dialogue text, captions, logos, watermark, UI or pool
Avoid: character redesigns, duplicates, extra wings or legs, feather loss, falling, fear, insects or spiders, disgusting grime, photorealism, dense clutter, smoke, glow haze, Zelda symbols or copyrighted game motifs
```

## Cinematic 06 — all clean

Output:
`cinematic_raw/frame_06_all_clean.png`

```text
Use case: illustration-story
Asset type: 2D cinematic frame 06 of 06, the clean-castle finale for Mermaid Roshan: Reef of Light
Input images: Image 1 is the approved cinematic continuity anchor; Images 2, 3 and 4 fix Mermaid Roshan, Daddy Mermaid and Baby Eagle in their cleaning action rendering; Image 5 is the current Pearl Castle Grand Hall environment reference
Primary request: finish the story with the three helpers together in the fully clean Pearl Castle, celebrating what they accomplished as a family
Scene/backdrop: the recognizable Pearl Castle Grand Hall from Image 1, now completely clean and bright: cream shell-capital columns, lavender stone walls, polished floor, burgundy carpet, gold trim, staircase, shell fixtures and radiant rainbow throne arch; no dirt targets remain; a few restrained gold and aqua four-point twinkles mark the clean surfaces
Subject: Mermaid Roshan is the central child hero, matching continuity, joyfully giving Daddy Mermaid a high-five; Daddy bends slightly to meet her hand, smiling warmly, matching continuity; Baby Eagle loops above them with two wings spread and a tiny pearl-shell victory badge dangling safely from one foot; the pearl bucket, coral sponge and rainbow mop rest neatly together at the edge of the carpet as completed tools
Style/medium: exactly the same polished modern flat-color anime storybook illustration, soft painterly cel bands and fine navy-purple outlines as the continuity images
Composition/framing: wide 16:9 cinematic composition, grand symmetrical ending shot facing the throne; trio centered in the lower-middle foreground with full silhouettes and faces readable; clean hall opens behind them; modest negative space above; no panel borders
Lighting/mood: luminous aqua-lavender and warm pearl-gold light, proud family affection, relief, belonging and gentle celebration
Constraints: exactly Mermaid Roshan, Daddy Mermaid and Baby Eagle and no other characters; preserve continuity faces, hair, crowns, clothing, plumage, tail colors and proportions; Baby Eagle has exactly two wings and two legs and no backpack; Roshan remains a mermaid child; Daddy remains a mermaid; no dialogue text, captions, logos, watermark, UI or pool
Avoid: character redesigns, duplicates, extra limbs, human legs, romantic posing, royal crowd, confetti clutter, excessive bloom, dirty patches, photorealism, Zelda symbols or copyrighted game motifs
```

## Expansion pass

The following sources expanded the runtime pack from 18 to 60 sprites and the
cinematic from 6 to 12 frames. The dust-bunny-only action and badge prompts are
the final replacement edits; superseded dark-puff artwork was deleted from the
pack and is not processed or shipped.

## Sprite atlas 04 — dust-bunny cast

Output:
`raw/dust_bunny_cast_atlas_chroma.png`

```text
Create a square 2D game sprite atlas for Mermaid Roshan's Pearl Castle cleanup section with exactly six separate cute lavender dust-bunny character poses in a strict 3 columns by 2 rows grid: a round front-facing bunny with tall spiral curl ears and pearl paws; a happy sibling pair; a hopping bunny with one curled lavender motion tail; a bunny peeking from beneath a pearl shell; a sleepy curled bunny with one soap-bubble breath; and a smiling family of three. Use pearl paws, big warm brown-purple eyes, tiny smiles, coral blush, rounded lavender cloud curls, and fine navy-purple outlines. Match the castle's polished pastel cel-painted storybook style. Every pose must be child-friendly, cheerful, and readable on a small phone. Use a uniform saturated #00ff00 chroma-key background with no floor, cast shadow, gradient, labels, dividers, text, logo, or overlap between cells. Generous padding and complete silhouettes. Dust bunnies are friendly helpers, not pests, monsters, smoke, or realistic dirt.
```

## Sprite atlas 05 — loose clutter targets

Output:
`raw/clutter_targets_atlas_chroma.png`

```text
Create a square 2D game sprite atlas with exactly six separate upbeat Pearl Castle clutter targets in a strict 3 columns by 2 rows grid: pastel toy blocks with one loose pearl ball; crumpled craft paper and coral/aqua ribbon scraps; a short tipped stack of picture books; scattered oversized buttons and pearl beads; a playful trail of two leaves, a twig, and three harmless mud crumbs; and two cloud cushions with a pearl shell pillow out of place. Polished flat-color cel-painted storybook game art, fine navy-purple contour, pearl/lavender/aqua/coral/restrained-gold palette, broad phone-readable silhouettes. Uniform saturated #00ff00 chroma-key background, one isolated target per cell, generous padding, no characters, no faces, no text, no logos, no cast shadows, no mold, rot, insects, garbage, or scary grime.
```

## Sprite atlas 06 — room grime targets

Output:
`raw/room_grime_targets_atlas_chroma.png`

```text
Create a square 2D game sprite atlas with exactly six separate child-friendly Pearl Castle room-grime targets in a strict 3 columns by 2 rows grid: a broad lavender dusty-shelf streak; one oval cloudy mirror patch; a bubbly pearl-and-lavender bath soap ring; a small pale-gold flour spill with a shell scoop mark; one dark purple fireplace smudge drawn as an inanimate wipeable mark; and three coral, aqua, and lavender washable paint splats. Polished flat-color storybook illustration, broad cel bands, fine navy-purple outline, oversized readable shapes for a small phone. Uniform saturated #00ff00 chroma-key background, no floor or scenery, one target per cell, no faces, no living smoke, no characters, no text, no labels, no logos, no cast shadows, no disgusting or frightening dirt.
```

## Sprite atlas 07 — expanded cleaning tools

Output:
`raw/expanded_tools_atlas_chroma.png`

```text
Create a square 2D game sprite atlas with exactly six separate Pearl Castle cleaning and sorting tools in a strict 3 columns by 2 rows grid: a soft coral-and-aqua ribbon duster with shell handle; a chunky lavender shell-handled window squeegee; a neat stack of three coral, aqua, and lavender cleaning cloths; an empty pearl fan-shell sorting basket with restrained-gold handle; a short lavender shell broom; and a plush cream dusting mitt with aqua shell badge. Polished pastel cel-painted storybook game art with fine navy-purple outlines, broad readable silhouettes, pearl/lavender/aqua/coral/restrained-gold palette. Uniform saturated #00ff00 chroma-key background, generous gutters, complete handles and silhouettes, no characters, no faces, no writing, no branded chemicals, no dangerous tools, no cast shadows, no logos, no cell borders.
```

## Sprite atlas 08 — dust-bunny action effects

Final replacement output:
`raw/mess_action_fx_atlas_chroma.png`

```text
Edit the supplied Mermaid Roshan cleanup effects atlas into a DUST-BUNNY-ONLY production sprite sheet. Preserve the exact square canvas, strict 3 columns by 2 rows grid, saturated uniform chroma green background, navy-purple outlines, pastel cel-painted rendering, scale, margins, and six isolated readable cells. Match the supplied lavender spiral-eared dust bunny design. Remove every dark soot-puff creature and every black or charcoal living puff. The six cells must be: top-left a lavender dust bunny hop effect with one curled motion swoosh; top-center a soft lavender dust-poof burst with two tiny spiral ear curls but no face; top-right a short trail of three lavender curled paw-puffs; bottom-left a cute pair of pearl eyes peeking from a pale lavender dust cloud; bottom-center a coral heart-shaped friendship swirl with two lavender curl accents; bottom-right a cozy aqua cloud-and-shell dust bunny nest. Exactly one effect vignette per cell, no cell borders, no text, no labels, no UI, no soot sprites, no dark creatures, no shadows extending between cells.
```

## Sprite atlas 09 — progress and friendship badges

Final replacement output:
`raw/progress_badges_atlas_chroma.png`

```text
Edit the supplied Mermaid Roshan progress-badge atlas while preserving its exact square canvas, strict 3 columns by 2 rows grid, saturated uniform chroma green background, pastel cel-painted rendering, navy-purple outlines, pearl-and-shell motif, scale, spacing, and first five cells. Replace ONLY the bottom-right dark soot-puff helper badge with a new DUST BUNNY HELPER badge: a smiling lavender spiral-eared dust bunny holding a tiny folded aqua cleaning cloth inside the same pearl-studded restrained-gold circular frame. Match the supplied dust bunny design exactly. There must be no dark soot creature, no black or charcoal living puff, and no trace of the removed character. Keep exactly six isolated readable badge cells, no text, no labels, no UI, no cell borders.
```

The six final cells are one-gold-pearl progress, two-gold-pearl progress,
three-gold-pearl completion, tidy book-and-cloth stack, dust-bunny cloud home,
and dust-bunny helper.

## Sprite atlas 10 — large object mess vignettes

Output:
`raw/object_mess_vignettes_atlas_chroma.png`

```text
Create a square 2D game sprite atlas with exactly six separate large Pearl Castle mess vignettes in a strict 3 columns by 2 rows grid: a shell-and-pearl chandelier with soft dust curls and one tiny lavender dust bunny; a navy-lavender royal banner hanging crooked with a bunny peeking near the hem; a lavender shell throne with one dull smudge and coral cloth; a pastel pantry shelf with a tipped jar and flour below; a shell-trim craft table covered with paper and washable paint scraps; and a pearl-gold toy chest open with a few blocks outside. Polished pastel cel-painted storybook art, navy-purple contour, simplified mobile-readable shapes, pearl/lavender/aqua/coral/restrained-gold palette. Uniform saturated #00ff00 chroma-key background, one complete vignette per cell, no room backgrounds, no text, no labels, no logos, no cast shadows, no dangerous clutter, no scary or disgusting dirt.
```

## Added cinematic 02 — dust-bunny reveal

Output:
`cinematic_raw/frame_02_dust_bunnies_reveal.png`

```text
Create one polished 16:9 storybook cinematic frame for Mermaid Roshan: Reef of Light, continuing directly from the supplied dirty-castle arrival frame. Preserve the exact designs, proportions, colors, crown, clothing, rainbow tails, faces, and rendering style of Mermaid Roshan, Daddy Mermaid, and Baby Eagle from that frame. Inside the same pastel lavender pearl castle hall, reveal that the mess itself is cute and playful: several lavender spiral-eared DUST BUNNIES matching the supplied design sheet hop out from under benches, behind shells, and from soft dusty corners. One sleepy bunny peeks from beneath a pearl shell and two siblings tumble together. The trio is visible together in the middle distance, surprised and delighted rather than afraid. Show cobwebs, dusty swirls, little muddy prints, one pink spill, and crooked decor, but keep the mood upbeat, cozy, funny, and safe for a four-year-old. Strong readable silhouettes, navy-purple outlines, aqua and lavender shadows, pearl and shell accents, warm child-friendly expressions, cinematic composition with clear foreground bunny reveal and background family. Dust bunnies are the only living mess creatures. No text, no labels, no UI, no logos, no pool, no danger, no weapons, no soot sprites, no dark puff creatures, and no extra human or mermaid characters.
```

## Added cinematic 04 — dust-bunny roundup

Output:
`cinematic_raw/frame_04_dust_bunny_roundup.png`

```text
Create one polished 16:9 storybook cinematic frame for Mermaid Roshan: Reef of Light, continuing the exact character continuity and pastel cel-painted castle style of the supplied cleanup frames. Mermaid Roshan is the clear hero in the foreground, smiling as she gently guides two cute lavender spiral-eared dust bunnies toward an open pearly shell sorting basket and a soft aqua cloud nest. She holds the coral-pink star dusting mitt or ribbon duster from the supplied tool sheet; the dust bunnies are eager helpers, not pests. Daddy Mermaid steadies the basket in the background and Baby Eagle carries a tiny ribbon overhead, so all three family members participate. Preserve their exact costumes, crowns, faces, rainbow tails, and Baby Eagle colors. The dirty hall still has a few playful lavender dust swirls and clutter patches, but a visibly clean sparkling path is opening behind Roshan. Upbeat teamwork, soft motion arcs, oversized readable props, navy-purple outlines, aqua/lavender shadows, shell and pearl motifs. Dust bunnies are the only living mess creatures. No text, no labels, no UI, no logos, no pool, no danger, no punishment, no soot sprites, no dark puff creatures, no extra characters.
```

## Added cinematic 08 — pantry team

Output:
`cinematic_raw/frame_08_pantry_team.png`

```text
Create one polished 16:9 storybook cinematic frame for Mermaid Roshan: Reef of Light in the castle pantry, using the supplied pantry image for room architecture and the supplied arrival frame for exact character designs and rendering continuity. Show Mermaid Roshan, Daddy Mermaid, and Baby Eagle all cleaning together: Roshan wipes a harmless floury spill with a coral star cloth, Daddy Mermaid straightens the pastel jars on the shell-trim shelf, and Baby Eagle carries a small ribbon-tied packet back into place. Add two cute lavender spiral-eared dust bunnies matching the supplied design sheet: one carries a folded aqua cloth and the other rolls a lost golden bead toward its jar. Everyone is smiling and cooperating. Include one before/after contrast within the scene: a messy flour patch and tipped jar on one side, a clean sparkling shelf and sorted containers on the other. Pastel toy-diorama castle, soft cel-painted storybook rendering, navy-purple outlines, aqua/lavender shadows, warm coral accents, readable silhouettes for a four-year-old. Preserve exact character faces, clothing, crowns, tails, and Baby Eagle design. Dust bunnies are the only living mess creatures. No text, no labels, no UI, no logos, no pool, no danger, no rotten food, no soot sprites, no dark puff creatures, and no extra characters.
```

## Added cinematic 09 — toy-room sorting

Output:
`cinematic_raw/frame_09_toy_room_sort.png`

```text
Create one polished 16:9 storybook cinematic frame for Mermaid Roshan: Reef of Light in the Pearl Castle toy room, using the supplied toy-room capture for architecture and the supplied arrival frame for exact character designs and rendering continuity. Show joyful cooperative sorting: Mermaid Roshan places pastel blocks into a large aqua shell-mark toy chest, Daddy Mermaid stacks two oversized picture books and straightens cloud cushions, and Baby Eagle flies a ribbon scrap toward a coral sorting basket. Add three cute lavender spiral-eared dust bunnies matching the supplied design sheet: one nudges a block, the sibling pair pushes a tiny book together, and a sleepy bunny peeks from a cushion pile. The room begins cluttered at the foreground edge but is clearly becoming organized behind the family. Preserve exact faces, costumes, crowns, rainbow tails, and Baby Eagle colors. Pastel toy-diorama castle, soft cel-painted storybook rendering, navy-purple outlines, aqua/lavender shadows, coral and restrained-gold accents, oversized readable props and actions for a four-year-old. Dust bunnies are the only living mess creatures. No text, no labels, no UI, no logos, no pool, no danger, no broken toys, no soot sprites, no dark puff creatures, and no extra characters.
```

## Added cinematic 10 — library bunny helpers

Output:
`cinematic_raw/frame_10_library_bunny_helpers.png`

```text
Create one polished 16:9 storybook cinematic frame for Mermaid Roshan: Reef of Light in the Pearl Castle royal library, using the supplied library capture for architecture and the supplied arrival frame for exact character designs and rendering continuity. Show all three family members cleaning together: Daddy Mermaid uses a soft lavender ribbon duster along a low bookshelf, Mermaid Roshan stacks pastel picture books on the round shell-trim table, and Baby Eagle carries one bookmark ribbon back to the shelf. Add two cute lavender spiral-eared dust bunnies matching the supplied design sheet; they proudly roll a small book into line and gather loose pearl beads into a tiny shell dish. Include a few remaining dust curls on the left and sparkling clean ordered shelves on the right, making progress instantly readable. Preserve exact faces, clothing, crowns, rainbow tails, and Baby Eagle colors. Pastel cel-painted storybook castle, navy-purple outlines, aqua/lavender shadows, warm coral and restrained-gold accents, safe upbeat teamwork for a four-year-old. Dust bunnies are the only living mess creatures. No text on books, no labels, no UI, no logos, no pool, no danger, no soot sprites, no dark puff creatures, and no extra characters.
```

## Added cinematic 11 — final inspection and bunny home

Output:
`cinematic_raw/frame_11_final_inspection.png`

```text
Create one polished 16:9 storybook cinematic frame for Mermaid Roshan: Reef of Light immediately before the supplied final high-five frame. Use the arrival and clean-finale images for exact character, castle, lighting, and costume continuity. The Pearl Castle great hall is now gleaming and orderly. Mermaid Roshan, Daddy Mermaid, and Baby Eagle stand together inspecting their work with proud delighted smiles: Roshan points to the polished floor, Daddy Mermaid holds the empty shell bucket, and Baby Eagle presents a final sparkle. Nearby, the lavender spiral-eared dust bunnies are not thrown away: a happy family of bunnies rests in a cozy aqua cloud-and-pearl-shell home beside a neat bench, while one bunny gives Roshan a tiny wave. Show only one small last lavender dust curl turning into a sparkle, establishing that cleaning transformed the mess into friendship. Strong cinematic composition, soft cel-painted pastel storybook rendering, navy-purple outlines, aqua/lavender shadows, pearl and shell motifs, clean readable silhouettes for a four-year-old. Preserve exact faces, crowns, clothing, rainbow tails, and Baby Eagle design. Dust bunnies are the only living mess creatures. No text, no labels, no UI, no logos, no pool, no danger, no soot sprites, no dark puff creatures, no extra characters.
```

## Room skin atlas 11 — Playroom objects

Output:
`raw/playroom_clutter_atlas_chroma.png`

```text
Create a square production sprite atlas for Mermaid Roshan's existing Pearl Castle PLAYROOM cleanup section. Use the supplied in-game Playroom capture only for its established toy vocabulary and the supplied cleanup atlas for exact pastel cel-painted rendering style. Exactly six separate put-away targets in a strict 3 columns by 2 rows grid: top-left scattered oversized shell-and-star puzzle tiles; top-center knocked pastel stacking rings with the peg beside them; top-right a pearl shell tea set with a tipped tray, cup, and saucer; bottom-left a dress-up pile with small pearl tiara, folded aqua cape, and coral ribbon; bottom-center two pastel play balls beside a soft cloud beanbag; bottom-right one rounded wheeled shell toy with three chunky blocks. Fine navy-purple outlines, cream/pearl/lavender/aqua/coral/restrained-gold palette, broad phone-readable silhouettes, upbeat and safe for a four-year-old. Uniform saturated chroma green background, generous gutters, no floor or room background, no gradients, no cast shadows, no cell borders, no labels, no text, no logos, no characters, no faces, no living grime, no soot sprites. Exactly one complete isolated target vignette per cell.
```

## Room skin atlas 12 — Royal Library objects

Output:
`raw/library_clutter_atlas_chroma.png`

```text
Create a square production sprite atlas for Mermaid Roshan's existing Pearl Castle ROYAL LIBRARY cleanup section. Use the supplied in-game Royal Library capture only for its established furniture and book vocabulary and the supplied cleanup atlas for exact pastel cel-painted rendering style. Exactly six separate put-away targets in a strict 3 columns by 2 rows grid: top-left a small tumble of oversized pastel picture books with blank shell-icon covers; top-center loose coral, aqua, and lavender bookmark ribbons with pearl clips; top-right three rolled story scrolls tied with shell ribbons and no writing; bottom-left a low pearl-and-gold book cart with several leaning books; bottom-center two round reading cushions and one shell pillow out of place; bottom-right four large blank picture cards showing only simple shell, star, fish, and rainbow icons. Fine navy-purple outlines, cream/pearl/lavender/aqua/coral/restrained-gold palette, broad phone-readable silhouettes, playful and non-reading-dependent. Uniform saturated chroma green background, generous gutters, no floor or room background, no gradients, no cast shadows, no cell borders, no labels, no text, no logos, no characters, no faces, no living grime, no soot sprites. Exactly one complete isolated target vignette per cell.
```

## Room skin atlas 13 — Existing Royal Kitchen objects

Output:
`raw/royal_kitchen_targets_atlas_chroma.png`

```text
Create a square production sprite atlas for Mermaid Roshan's EXISTING ROYAL KITCHEN in the Pearl Castle basement. Use the supplied in-game kitchen capture only for fixture vocabulary and the supplied cleanup atlas for exact pastel cel-painted rendering style. Exactly six separate safe kitchen cleanup targets in a strict 3 columns by 2 rows grid: top-left the existing shell sink with three pastel plates and harmless pale-aqua soap film; top-center the existing white counter with a small flour patch, crumbs, and one wooden spoon; top-right the existing rounded stove shown cool with one coral soup drip beside a burner ring; bottom-left two tipped pastel cups with a small aqua tea puddle; bottom-center a crooked lavender pan and lid with a pale-lavender smudge; bottom-right a short pearl cabinet with three rounded pantry jars out of line. Fine navy-purple outlines, cream/pearl/lavender/aqua/coral/restrained-gold palette, broad phone-readable silhouettes, cheerful rather than gross. Uniform saturated chroma green background, generous gutters, no floor or room background, no gradients, no cast shadows, no cell borders, no labels, no text, no logos, no characters, no faces, no living grime, no mold, no rotten food, no hot flames, no soot sprites. Exactly one complete isolated target vignette per cell.
```

## Room skin atlas 14 — Existing Bubble Bath objects

Output:
`raw/bubble_bath_targets_atlas_chroma.png`

```text
Create a square production sprite atlas for Mermaid Roshan's EXISTING BUBBLE BATH room in the Pearl Castle basement. Use the supplied in-game bath capture only for fixture vocabulary and the supplied cleanup atlas for exact pastel cel-painted rendering style. Exactly six separate upbeat bathroom cleanup targets in a strict 3 columns by 2 rows grid: top-left a pearl bathtub edge with a pale lavender soap ring and a few aqua foam bubbles; top-center an oval shell mirror with gentle fog and two child-sized wipe swirls; top-right the shell vanity sink with one harmless coral soap dab and three water droplets; bottom-left a rumpled pile of three clean pastel towels; bottom-center a tipped pearl bath-toy basket with shell, star, and seahorse toys; bottom-right a short trail of four clear-aqua water droplets on pastel tile. Fine navy-purple outlines, cream/pearl/lavender/aqua/coral/restrained-gold palette, broad phone-readable silhouettes, fresh and funny rather than gross. Uniform saturated chroma green background, generous gutters, no floor or room background, no gradients, no cast shadows, no cell borders, no labels, no text, no logos, no characters, no faces, no living grime, no mold, no hair, no bodily waste. Exactly one complete isolated target vignette per cell.
```

## Room skin atlas 15 — Existing Royal Loo and undercroft objects

Output:
`raw/royal_loo_undercroft_targets_atlas_chroma.png`

```text
Create a square production sprite atlas for Mermaid Roshan's EXISTING HIDDEN ROYAL LOO and nearby UNDERCROFT in the Pearl Castle basement. Use the supplied in-game Royal Loo and undercroft captures only for fixture vocabulary and the supplied cleanup atlas for exact pastel cel-painted rendering style. Exactly six separate safe cleanup targets in a strict 3 columns by 2 rows grid: top-left the rounded pearl toilet with a pale-aqua soap ring and a few clean water spots, no waste; top-center three pearl toilet-paper rolls stacked crooked with lavender bands and no writing; top-right a lavender shell toilet brush and pearl holder sitting out of place; bottom-left a small clear-aqua splash and four clean droplets on pastel tile; bottom-center two dusty shell-stamped storage barrels and one pearl crate; bottom-right a triangular basement stair cobweb beside a short lavender dust trail. Fine navy-purple outlines, cream/pearl/lavender/aqua/coral/restrained-gold palette, broad phone-readable silhouettes, cheerful and non-gross for a four-year-old. Uniform saturated chroma green background, generous gutters, no floor or room background, no gradients, no cast shadows, no cell borders, no labels, no text, no logos, no characters, no faces, no living smoke, no insects, no mold, no brown stains, no bodily waste, no frightening basement. Exactly one complete isolated target vignette per cell.
```

## Room skin atlas 16 — Six room-level before-cleaning vignettes

Output:
`raw/castle_rooms_vignettes_atlas_chroma.png`

```text
Create a square production sprite atlas of six LARGE BEFORE-CLEANING ROOM VIGNETTES for Mermaid Roshan's EXISTING Pearl Castle rooms. Use the supplied playroom, library, Royal Kitchen counter, Bubble Bath, Royal Loo, and undercroft captures only for their established fixtures and layout vocabulary; use the supplied cleanup atlas for exact pastel cel-painted rendering. Strict 3 columns by 2 rows grid: top-left messy Playroom with open aqua shell toy chest, blocks, stacking rings, and cushions; top-center messy Royal Library with tilted pastel shelves, fallen books, ribbons, and reading cushions; top-right messy basement Royal Kitchen vignette combining its white counter, shell sink, rounded stove, cups, and flour crumbs; bottom-left messy Bubble Bath with pearl tub, shell vanity, towels, foggy mirror, and water droplets; bottom-center messy hidden Royal Loo with rounded pearl toilet, crooked paper rolls, brush caddy, and clean water spots only; bottom-right dusty undercroft with shell barrels, pearl crate, little cart, shelf, cobweb, and lavender dust curls. Each is one compact isolated cutout with complete silhouette, simplified mobile-readable detail, fine navy-purple outlines, pearl/lavender/aqua/coral/restrained-gold palette. Uniform saturated chroma green background with generous gutters, no full room background, no gradients, no cast shadows, no borders, no labels, no text, no logos, no characters, no faces, no living grime, no mold, no rot, no bodily waste, no frightening darkness.
```

## 36-frame cinematic expansion

The 24 added cinematic prompts, reference roles, three rejection/correction
records, accepted full-resolution source mapping, and final sequencing notes are
recorded in `STORYBOARD_36_PROMPTS.md`.
