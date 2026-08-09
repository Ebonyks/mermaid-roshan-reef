# Animated dust bunny prompts

Generated with the OpenAI built-in image-generation tool on 2026-07-27.

## Shared references

- Image 1: approved `dust_bunny_curl_ears.png`, exact identity and neutral pose.
- Image 2: approved `dust_bunny_hop.png`, exact identity and airborne pose.

## Hop atlas

```text
Use case: identity-preserve
Asset type: production 2D game sprite animation atlas source for Godot AnimatedSprite3D
Input images: Image 1 is the exact approved dust-bunny identity and neutral curl-ear pose; Image 2 is the exact approved airborne hop pose and motion-tail design.
Primary request: create exactly six sequential frames of this same single lavender dust bunny performing one cheerful hop, arranged in a strict 3 columns by 2 rows grid in reading order. Frame 1 neutral curl-ear stance matching Image 1; frame 2 low squash and anticipation; frame 3 springing upward with ears lifting; frame 4 airborne peak matching Image 2 including one separate curled lavender motion tail; frame 5 soft landing squash; frame 6 recovered neutral stance ready to loop.
Scene/backdrop: perfectly flat solid saturated #00ff00 chroma-key background for local removal, identical in every cell.
Subject: the exact same single friendly lavender spiral-eared dust bunny in all six cells, with pearl paws, warm brown-purple eyes, coral blush, rounded lavender cloud curls, tiny cheerful mouth, and fine navy-purple outline.
Style/medium: preserve the supplied polished pastel cel-painted storybook sprite style exactly; crisp phone-readable silhouette.
Composition/framing: strict evenly spaced 3-by-2 sprite grid, one complete centered bunny pose per cell, generous padding, no overlap between cells, consistent character scale and camera angle.
Constraints: preserve character identity, colors, proportions, face, pearl paws, spiral ears, outline weight, lighting, and rendering from the supplied images; exactly six poses and exactly one bunny per cell; the curled motion tail appears only in the airborne peak cell; no redesign, no extra characters, no scenery, no floor plane, no cast shadow, no contact shadow, no gradients, no texture or lighting variation in the green background, no cell borders, no labels, no text, no logo, no watermark; do not use #00ff00 anywhere in the bunny.
```

## Idle atlas

```text
Use case: identity-preserve
Asset type: production 2D game sprite animation atlas source for Godot AnimatedSprite3D
Input images: Image 1 is the exact approved dust-bunny identity and neutral curl-ear pose; Image 2 is a supporting identity reference for the same bunny's side curls and cheerful expression.
Primary request: create exactly six sequential frames of this same single lavender dust bunny performing a gentle living idle loop, arranged in a strict 3 columns by 2 rows grid in reading order. Frame 1 neutral curl-ear stance matching Image 1; frame 2 tiny inhale with body subtly taller; frame 3 ears softly leaning inward and one friendly blink; frame 4 smallest buoyant upward bob with paws lifting slightly; frame 5 soft settle with ears relaxing outward; frame 6 neutral stance matching frame 1 for a seamless loop. Keep motion subtle and calm, with no locomotion and no motion tail.
Scene/backdrop: perfectly flat solid saturated #00ff00 chroma-key background for local removal, identical in every cell.
Subject: the exact same single friendly lavender spiral-eared dust bunny in all six cells, with pearl paws, warm brown-purple eyes, coral blush, rounded lavender cloud curls, tiny cheerful mouth, and fine navy-purple outline.
Style/medium: preserve the supplied polished pastel cel-painted storybook sprite style exactly; crisp phone-readable silhouette.
Composition/framing: strict evenly spaced 3-by-2 sprite grid, one complete centered bunny pose per cell, generous padding, no overlap between cells, consistent character scale and front camera angle.
Constraints: preserve character identity, colors, proportions, face, pearl paws, spiral ears, outline weight, lighting, and rendering from the supplied images; exactly six poses and exactly one bunny per cell; no running, no hopping away, no motion tail, no redesign, no extra characters, no scenery, no floor plane, no cast shadow, no contact shadow, no gradients, no texture or lighting variation in the green background, no cell borders, no labels, no text, no logo, no watermark; do not use #00ff00 anywhere in the bunny.
```

## Rejected defeat wisp atlas v1

Rejected 2026-07-28 because the gradual sideways dissolve looked like the
bunny simply vanished instead of being cleaned. The chroma source is retained
at `rejected/dust_bunny_defeat_v1_soft_dissolve.png`.

```text
Use case: stylized-concept
Asset type: 2D game character animation sprite sheet
Input images: Image 1 is the authoritative idle-sheet character and style reference; Image 2 is the authoritative hop-sheet motion and proportions reference.
Primary request: Create one 3-column by 2-row sprite sheet containing exactly six sequential defeat/dispersal animation frames for this exact lavender dust bunny. The bunny is gently blown away into a whimsical wisp of dust smoke, suitable for a kind game for a four-year-old.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal. Every cell must have the same uniform green background.
Subject and sequence, reading left-to-right across the top row then the bottom row: frame 1 intact bunny in its familiar neutral pose as a breeze begins; frame 2 curled ears and fluffy body lean with the breeze and release a few small lavender curls; frame 3 about two-thirds of the bunny remains while soft opaque lavender dust curls stream sideways; frame 4 only the lower half and one curled ear remain, becoming rounded smoke curls; frame 5 the bunny is gone and three cute pale-lavender spiral dust puffs drift sideways; frame 6 one small fading lavender spiral wisp remains, almost vanished. Wind direction is consistently left-to-right. Keep the character anchored at the same bottom-center point in every cell while the wisps trail rightward within the cell.
Style/medium: exact same polished 2D children's storybook sprite style, lavender palette, navy-purple outline, rounded cloud curls, soft cel-painted highlights, and cute proportions as the input images. The dust/smoke must be stylized as opaque rounded lavender curls with crisp outlined silhouettes, not realistic translucent smoke.
Composition/framing: exact 3x2 grid, six equal cells, one frame per cell, generous padding, no overlap between cells, full effect visible inside every cell, consistent character scale and ground anchor. No grid lines or panel borders.
Mood: gentle, magical, harmless, readable at small mobile size.
Constraints: preserve the exact dust-bunny identity, spiral ears, facial design, palette, line weight, and rendering style. Background must be one uniform #00ff00 color with no shadows, gradients, texture, reflections, floor plane, or lighting variation. Do not use #00ff00 in the subject. No cast shadow, contact shadow, text, labels, watermark, extra characters, debris, impact star, injury, fear, pain, bones, or violence. Exactly six frames and no more.
```

## Cleaning-poof defeat atlas v2

```text
Use case: identity-preserve
Asset type: production 2D game character defeat animation atlas for a four-year-old's mobile game
Input images: Image 1 is the authoritative dust-bunny identity and rendering-style reference. Image 2 is the authoritative motion, scale, and outline reference. Image 3 is the edit target whose gradual dissolve timing must be replaced; preserve its 3-column by 2-row atlas format but make the action much punchier and unmistakably read as the dust bunny being magically cleaned away.
Primary request: Replace the soft vanish with exactly six strongly contrasted sequential frames of one energetic CLEANING POOF animation. It must have a sharp anticipation, one very large readable pop frame, an expanding dust ring, and a sparkling clean finish. The bunny does not slowly fade or blow sideways.
Sequence in reading order, left-to-right top row then left-to-right bottom row: Frame 1: intact familiar bunny with a bright aqua-white cleaning sparkle touching its lower curl and a few tiny soap bubbles, clearly triggering the effect. Frame 2: dramatic squash anticipation—the entire bunny compresses into a small round dusty puff, spiral ears curl inward, and a thick aqua-white crescent cleaning swish wraps around it. Frame 3: the biggest impact frame—a large round lavender-and-cream cartoon POOF cloud fills most of the cell, with a bold aqua-white four-point starburst at its center, an outlined expanding smoke ring, spiral dust curls, and small soap bubbles; no recognizable bunny body remains. Frame 4: the cloud snaps outward into a wide donut-shaped lavender dust ring with a clearly empty clean center, several rounded outward puffs, and bright aqua-white sparkles. Frame 5: the ring breaks into only a few small separated lavender dust curls while one large crisp aqua-white cleanliness twinkle dominates the center and two bubbles float upward. Frame 6: all dust is gone; show one bold aqua-white four-point clean sparkle plus two tiny bubbles, a decisive sparkling-clean endpoint.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background in every cell for local removal.
Style/medium: preserve the exact polished pastel 2D children's storybook sprite style, navy-purple outlines, lavender dust palette, soft cel-painted highlights, rounded shapes, and phone-readable silhouettes from Images 1 and 2. Effects are opaque stylized graphic shapes with crisp outlines, not realistic or translucent smoke.
Composition/framing: strict 3 columns by 2 rows, six equal 256-style cells, one frame per cell, same bottom-center anchor, generous padding, no overlaps between cells, no grid lines or panel borders. Frames 2 and 3 must change silhouette dramatically. Frame 3 is the visual peak and should use roughly twice the area of the final sparkle.
Color palette: lavender and cream dust cloud, navy-purple outlines, bright aqua and white cleaning swishes/sparkles, a few pale blue soap bubbles. Keep all colors clearly separate from chroma green.
Mood: punchy, satisfying, magical, obviously cleaned, harmless, funny, and readable at small mobile size.
Constraints: change only the defeat/dispersal action; preserve the dust-bunny identity before the pop. Exactly six frames. No gradual sideways dissolve, no long wind trail, no simple shrink-fade, and no final lavender wisp. No text, letters, logos, watermark, broom, vacuum, hands, extra character, scenery, floor, cast shadow, contact shadow, injury, pain, fear, bones, debris, or violence. Background must be perfectly uniform #00ff00 with no gradients, shadows, lighting variation, or texture; do not use #00ff00 inside any subject or effect.
```

## Rainbow dust-bunny concept

Generated with the OpenAI built-in image-generation tool on 2026-07-28,
using `references/dust_bunny_curl_ears.png` as the edit target. The generated
square concept was locally resized to the mobile-safe 1024x1024 source stored
as `rainbow_dust_bunny_concept.png`.

```text
Use case: precise-object-edit
Asset type: 2D game enemy character design concept for Mermaid Roshan: Reef of Light
Input image: Image 1 is the edit target and identity reference.
Primary request: Create a rainbow-colored version of this exact dust bunny. Change only the fur coloration and small accent highlights; preserve the character's silhouette, curled spiral ears, cloud-like body, front-facing seated pose, proportions, face, paws, glossy storybook rendering, and dark violet/navy outlines.
Color design: Arrange a clear pastel rainbow rhythm across the fluffy dust curls—coral pink, warm peach, butter yellow, mint/aqua, sky blue, lavender—blended curl-to-curl rather than as hard horizontal stripes. Keep the face area light enough for strong eye readability. Make the two large spiral ears complementary rainbow gradients, with pearl-like ear beads. Add a very small prismatic sparkle accent on the central forehead curl to distinguish this as a special enemy variant.
Style/medium: polished hand-painted 2D children's storybook sprite, soft cel shading, rounded toy-like forms, glossy highlights, cohesive with the source image.
Composition: one complete character centered with generous padding, fully visible, square sprite presentation.
Lighting/mood: cheerful, magical, gentle, highly readable for a four-year-old.
Constraints: preserve the exact appealing identity and curl-ear design of Image 1; no anatomy changes; no extra limbs or ears; no costume; no text; no watermark; no environment; no floor or cast shadow. Keep the background transparent if possible, otherwise use a plain neutral preview background. Avoid neon saturation, muddy color blending, realistic fur, or horizontal flag-like stripes.
```

## Grey-purple first-boss concept

Generated with the OpenAI built-in image-generation tool on 2026-07-28,
using `references/dust_bunny_curl_ears.png` as the authoritative family
identity. The generated square concept was locally resized to the mobile-safe
1024x1024 source stored as `dust_bunny_first_boss_concept.png`.

```text
Use case: identity-preserve
Asset type: 2D first-boss character design concept for Mermaid Roshan: Reef of Light
Input image: Image 1 is the authoritative dust-bunny family identity and rendering-style reference.
Primary request: Design a much bigger, unmistakably boss-scale grey-and-purple dust bunny descended from this exact curl-eared creature. Preserve the same species identity, face language, cloud curls, spiral motifs, pearl paws, storybook rendering, and dark violet/navy outline, while expanding it into a broad, imposing but child-friendly first boss.
Boss silhouette: roughly two-and-a-half times the apparent body mass of a normal dust bunny; a wide three-tier storm-cloud body with many large rounded curls; two enormous spiral ears sweeping high and outward like soft ram-horn shapes; a thick central forehead curl rising into a natural three-point curl crest, made from dust fluff rather than a separate crown; two large side curls anchoring the base. Keep one coherent creature with four visible pearl-like paws set wider apart for a sturdy stance.
Expression: confident and mischievous with slightly lowered upper eyelids and a small determined smile, but still cute, gentle, and safe for a four-year-old. No anger, fangs, claws, injury, or menace.
Color palette: dominant warm charcoal-grey and smoky lavender; deep plum in the shadowed lower curls; medium slate-purple in the body; pale lilac-grey highlights across the face and ears; pearly cream paws with lavender reflections; small cool aqua-white glints in the eyes. Keep strong tonal separation and avoid nearly black fills.
Boss accents: a subtle halo of three small opaque lavender dust curls close behind the silhouette and one bold pale-lavender four-point sparkle embedded in the central curl crest. These are graphic sprite accents, not an environment.
Style/medium: polished hand-painted 2D children's storybook game sprite, soft cel shading, rounded toy-like forms, glossy highlights, crisp phone-readable silhouette, cohesive with Image 1.
Composition/framing: one complete front-facing boss centered in a square design sheet, fully visible with generous padding; the body occupies most of the frame and feels massive without cropping.
Scene/backdrop: perfectly flat pale warm-cream concept-sheet background, with no floor, horizon, scenery, gradient, texture, cast shadow, or contact shadow.
Constraints: preserve the curl-eared dust-bunny identity; exactly one character; no extra limbs beyond four pearl paws; no armor, clothing, cape, jewelry, weapon, throne, text, logo, or watermark; no 3D render; no photorealistic fur; no scary expression. The boss quality must come from scale, layered cloud mass, stronger grey-purple values, ear shape, and curl crest—not accessories.
```

## Grey-purple first-boss concept v2: playful sharp teeth

Generated with the OpenAI built-in image-generation tool on 2026-07-28,
using `dust_bunny_first_boss_concept.png` as the exact edit target. The
generated square concept was locally resized to the mobile-safe 1024x1024
source stored as `dust_bunny_first_boss_concept_v2_teeth.png`.

```text
Use case: precise-object-edit
Asset type: revised 2D first-boss character design concept for Mermaid Roshan: Reef of Light
Input image: Image 1 is the exact edit target.
Primary request: Change only the boss dust bunny's tiny mouth. Turn the current closed cat-like smile into a small playful open grin with exactly two visible sharp teeth—one short pearly ivory triangular fang at each upper corner of the mouth. The teeth should have clear pointed tips, but be small, rounded at the edges, glossy, and cute rather than threatening. Keep the mouth compact and centered; use a muted plum interior with no tongue.
Expression: mischievous first-boss confidence suitable for a four-year-old. The teeth should be noticeable at phone size but occupy much less visual area than either eye.
Invariants: preserve every other part of Image 1 unchanged—the exact 1024-square composition, huge spiral ears, curl crest, forehead sparkle, eyes, eyelids, blush, grey-purple palette, cloud body, pearl paws, floating dust curls, outlines, highlights, scale, warm-cream background, and storybook rendering.
Constraints: exactly two pointed teeth; no additional teeth, no large open jaw, no snarl, no gums, no blood, no tongue, no drool, no wrinkles, no scary expression, no text, no watermark, and no other redesign.
```
