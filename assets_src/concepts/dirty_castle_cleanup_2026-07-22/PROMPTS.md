# Dirty Castle Cleanup 2D Generation Prompts

Generated 2026-07-22 with the OpenAI built-in image-generation tool. The tool
was used in its default built-in mode. Runtime transparency was produced by
local chroma-key removal; no CLI/API fallback or native-transparency model was
used. All atlases used soft matte plus despill; the feedback atlas also used the
prescribed one-pixel edge contraction after edge QA.

Protected project art was supplied only as an identity, palette, or environment
reference. The originals were not edited.

## Reference roles

- `gen2/turnarounds/roshan_v2/front.png`: Mermaid Roshan identity reference.
- `assets_src/daddy_master.png`: Daddy Mermaid identity reference.
- `assets/book/baby_eagle.png`: Baby Eagle identity reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_01_hall_overview.png`:
  current Pearl Castle Grand Hall environment and material reference.
- `assets_src/blender/qa_pearl_castle_kit/runtime_candidate_ffae3fe/castle_02_throne_focal.png`:
  current throne focal environment reference.
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
