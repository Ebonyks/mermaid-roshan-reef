# Dust-bunny first-boss animation design

Generated with the OpenAI built-in image-generation tool on 2026-07-28.
The approved `dust_bunny_first_boss_concept_v2_teeth.png` is the identity
anchor. Every animation is a four-frame 2x2 atlas normalized to 1024x1024,
with four 512x512 cells. Runtime derivatives are transparent RGBA textures
under `assets/sprites/dust_bunnies/boss/` and remain entirely 2D art displayed
by `DustBunnyBossSprite` on an unshaded `AnimatedSprite3D` card.

Owner mechanic update, 2026-07-28: the generated art stays unchanged, but the
long-press idea used while prompting the sheets is superseded by three quick
taps. The exact prompts below are retained as generation provenance; their
long-press wording is historical, not the runtime interaction contract.

Owner mechanic update, 2026-07-29: boss health is three rounds of three taps.
After round two, the final round runs at 1.25x action speed with a 0.65-second
tap window. The replacement angry jump is assembled entirely from approved
frames, so this update uses no generation budget and adds no texture memory.

## Encounter motion contract

| State | Four-frame read | Suggested use |
| --- | --- | --- |
| Jump | low squash, dusty lift-off, airborne peak, ring landing | Primary travel across the octagonal arena; movement remains deterministic gameplay code. |
| Vulnerable laugh | smug wind-up, laugh, exposed glowing crest, breathless hold | Normal attacks are ignored. Frames 2-4 open one 0.75-second window for three quick taps; frame 4 holds between accepted taps. |
| Flinch | crest contact, side squash, dizzy rebound, low recovery | The atlas is sliced into three distinct two-frame reactions: contact/squash, squash/dizzy, then dizzy/recovery. One reaction and sound plays per accepted tap. |
| Angry | realization, ears rise, plum aura peak, jump crouch | Short readable transition from flinch or a missed window into the next jump. |
| Final angry jump | peak angry power, jump crouch, dusty lift-off, ring landing | Reuses angry frames 3-4 followed by jump frames 2 and 4. It replaces both angry recovery and normal jump during the last health round, with no redesign or dramatic transformation. |
| Implode | inward pull, dense compression, collapsing dust ring, three wisps | One-shot no-injury defeat. Hide the card only after the final wisp frame. |

Recommended state rhythm for the no-fail encounter:
`jump -> land -> laugh/vulnerable -> tap/flinch 1 -> tap/flinch 2 ->
tap/flinch 3 + damage -> angry -> jump`. The three reactions use, in order,
`ui_tap.ogg`, `hop_boing.ogg`, and `chime.ogg`, with rising pitch and emphasis.
If fewer than three taps arrive before the window closes, progress resets
through `angry -> jump`; it never harms the player or creates a fail state.
Three large non-reading-dependent pips should light with the taps, while the
head flash remains the primary visual cue.

Each three-tap sequence removes one of three boss-health rounds. The first two
rounds use the 0.75-second window at normal action speed. Completing round two
activates the final round: action playback becomes 1.25x, the tap window becomes
0.65 seconds, and `angry_jump_final` replaces normal anger and jump. Missing a
window resets only the current three taps. Completing the third round plays the
implosion automatically at normal readable speed.

Final angry-jump source mapping in runtime order:
`angry[2] -> angry[3] -> jump[1] -> jump[3]`. These are atlas-region references
to the existing approved runtime sheets, not copied or regenerated pixels.

## Jump atlas prompt

```text
Use case: identity-preserve
Asset type: production 2D game boss jump animation atlas for an AnimatedSprite3D card
Input image: Image 1 is the exact approved grey-purple toothed dust-bunny boss identity and rendering reference.
Primary request: Create exactly four sequential frames of this same boss performing one heavy forward-facing jump with a plume of dust, arranged in a strict 2 columns by 2 rows grid in reading order.
Sequence: Frame 1 anticipation--boss squashes very low and wide, pearl paws spread, giant spiral ears compress slightly, curls bunch downward. Frame 2 lift-off--boss stretches upward with paws leaving the ground, ears trailing, and one large opaque grey-purple spiral dust plume bursting directly beneath it. Frame 3 airborne peak--complete boss floats clearly above the anchor with paws tucked, round body slightly lifted, ears buoyant, and a smaller detached curling dust plume below. Frame 4 landing--boss lands in a dramatic wide squash while one low donut-shaped dust ring and two rounded dust curls kick outward along the bottom.
Scene/backdrop: perfectly flat uniform saturated #00ff00 chroma-key background in every cell for local alpha removal; no shadows, gradients, floor, scenery, texture, or lighting variation.
Style/medium: preserve the exact polished 2D children's storybook sprite style, smoky grey-lavender-to-deep-plum palette, navy-purple outlines, glossy pearl paws, spiral ears, curl crest, forehead sparkle, two small sharp teeth, eyes, blush, and soft cel-painted highlights from Image 1.
Composition: strict 2x2 grid, four equal square cells, one full boss pose per cell, same scale and front camera, same bottom-center anchor except the airborne height, generous padding, no overlap, no grid lines or labels. Keep every pose fully inside its cell.
Motion/readability: the boss must visibly leave the ground in frames 2 and 3; the plume and landing ring are opaque graphic dust shapes with crisp outlines, readable at phone size.
Constraints: exact same single boss in all four cells; exactly four frames; no extra character, weapon, attack, text, logo, watermark, floor shadow, injury, or fear; no 3D render; no realistic smoke; do not use #00ff00 anywhere in the boss or dust effects.
```

## Vulnerable-laugh atlas prompt

```text
Use case: identity-preserve
Asset type: production 2D game boss vulnerable-laugh animation atlas for an AnimatedSprite3D card
Input images: the single-character cream-background boss image is the authoritative identity reference; the green-background jump sheet is supporting animation-scale and rendering continuity only.
Primary request: Create exactly four sequential frames of this same grey-purple toothed dust-bunny boss laughing so hard that its magical forehead crest becomes visibly vulnerable to a long press, arranged in a strict 2 columns by 2 rows grid in reading order.
Sequence: Frame 1 smug wind-up--boss leans slightly forward with a mischievous two-fang grin and one paw lifting; forehead sparkle is normal size. Frame 2 laugh begins--eyes close into happy crescents, mouth opens in a compact cheerful laugh showing exactly two small pointed teeth, giant ears loosen outward, body rises; forehead sparkle brightens and gains a thin aqua-white ring. Frame 3 maximum laugh and vulnerability--boss tips back, eyes remain joyfully closed, body and ears spread open, paws lifted away from the center; the forehead curl sparkle expands into a large bold aqua-white four-point weak-point star with two concentric lavender pulse rings, unmistakably targetable. Frame 4 breathless vulnerable pause--boss slumps forward with eyes still closed and a happy grin, ears droop slightly, and the enlarged glowing forehead star remains exposed for the long-press window.
Scene/backdrop: perfectly flat uniform saturated #00ff00 chroma-key background in every cell for local alpha removal; no shadows, gradients, floor, scenery, texture, or lighting variation.
Style/medium: exact polished 2D children's storybook sprite style, smoky grey-lavender and deep-plum curls, navy-purple outlines, glossy pearl paws, spiral ears, curl crest, blush, cute sharp teeth, and soft cel-painted highlights.
Composition: strict 2x2 grid, four equal square cells, one complete boss per cell, same scale/front camera/bottom-center anchor, generous padding, no overlap, no borders, labels, or text.
Gameplay readability: frame 3 must be the clearest silhouette and weak-point frame. Laugh puffs may appear as two tiny rounded lavender curls beside the mouth, but never as letters or text.
Constraints: preserve the exact boss identity in all cells; exactly four frames; exactly two small teeth whenever the mouth is open; friendly laughter, not pain or fear; no extra characters, weapon, attack, text, logo, watermark, 3D render, or realistic smoke; do not use #00ff00 in the boss or effects.
```

## Flinch atlas prompt

```text
Use case: identity-preserve
Asset type: production 2D game boss flinch animation atlas for an AnimatedSprite3D card
Input images: the single-character warm-cream image is the authoritative boss identity; the green animation sheets are supporting scale, palette, and frame-layout continuity.
Primary request: Create exactly four sequential frames of the same grey-purple toothed dust-bunny boss reacting to one successful long-press hit with a brief, readable, harmless flinch, arranged in a strict 2 columns by 2 rows grid in reading order.
Sequence: Frame 1 contact--boss is upright as one bold aqua-white four-point impact sparkle touches the exposed forehead crest; eyes widen, no attacker or projectile is shown. Frame 2 sharp flinch--entire soft body squashes diagonally to one side, giant ears bend with the motion, pearl paws pull inward, eyes squeeze shut, and the two small teeth remain visible in a tiny surprised mouth. Frame 3 wobble--boss rebounds past center with ears and curl crest leaning the opposite direction; eyes are spiral-dizzy but cute; two small lavender motion curls show the wobble. Frame 4 recovery--boss settles into a low compact crouch, one eye reopened and one eye blinking, determined but not yet angry; forehead sparkle returns to normal size.
Scene/backdrop: perfectly flat uniform saturated #00ff00 chroma-key background in every cell for local alpha removal; no shadows, gradients, floor, scenery, texture, or lighting variation.
Style/medium: preserve the exact polished 2D children's storybook sprite style, smoky grey-lavender/deep-plum cloud curls, navy-purple outlines, glossy pearl paws, oversized spiral ears, curl crest, blush, two cute pointed teeth, and soft cel-painted highlights.
Composition: strict 2x2 grid, four equal square cells, one complete boss per cell, consistent scale/front camera/bottom-center anchor, generous padding, no overlap, no borders, labels, or text.
Motion/readability: use strong silhouette changes and curved motion lines only; the reaction should read instantly at small mobile size but contain no injury.
Constraints: same single boss in every cell; exactly four frames; one impact sparkle only in frame 1; no extra character, weapon, projectile, damage mark, bruise, tear, pain, fear, blood, text, logo, watermark, 3D render, or realistic smoke; do not use #00ff00 in the boss or effects.
```

## Angry atlas prompt

```text
Use case: identity-preserve
Asset type: production 2D game boss angry-recovery animation atlas for an AnimatedSprite3D card
Input images: the single-character warm-cream image is the authoritative boss identity; the green animation sheets are supporting identity, palette, scale, and grid continuity.
Primary request: Create exactly four sequential frames of this same grey-purple toothed dust-bunny boss becoming comically angry after a flinch and preparing its next jump, arranged in a strict 2 columns by 2 rows grid in reading order.
Sequence: Frame 1 realization--boss sits low after recovery, one eye narrowed, cheeks puffed, tiny two-fang mouth clenched, ears beginning to rise. Frame 2 building anger--both eyes narrow with determined brows, cheeks turn slightly deeper coral, giant spiral ears stand tall and rigid, curl crest tightens, and two small dark-lavender dust puffs vent harmlessly beside the ears. Frame 3 peak anger--boss expands taller and broader with bristling rounded cloud curls, paws planted wide, exactly two small pointed teeth visible in a compact growly pout, forehead sparkle glows saturated lavender, and one thick opaque plum dust aura ring hugs the silhouette. Frame 4 ready stance--anger compresses into a low forward-leaning jump crouch, ears swept back, eyes focused, paws braced; aura collapses into two small dust curls behind it, clearly telegraphing movement.
Scene/backdrop: perfectly flat uniform saturated #00ff00 chroma-key background in every cell for local alpha removal; no shadows, gradients, floor, scenery, texture, or lighting variation.
Style/medium: exact polished 2D children's storybook sprite style, smoky grey-lavender/deep-plum curls, navy-purple outlines, glossy pearl paws, oversized spiral ears, curl crest, blush, cute pointed teeth, and soft cel-painted highlights.
Composition: strict 2x2 grid, four equal square cells, one complete boss per cell, consistent scale/front camera/bottom-center anchor, generous padding, no overlap, no borders, labels, or text.
Mood/readability: comically annoyed and energetic, not frightening. Silhouette and ear changes should clearly telegraph the next action at phone size.
Constraints: same single boss in every cell; exactly four frames; no flames, lightning, weapon, attack projectile, extra character, scary snarl, large jaw, extra teeth, injury, fear, text, logo, watermark, 3D render, or realistic smoke; do not use #00ff00 in the boss or effects.
```

## Implosion atlas prompt

```text
Use case: identity-preserve
Asset type: production 2D game boss defeat-implosion animation atlas for an AnimatedSprite3D card
Input images: the single-character warm-cream image is the authoritative boss identity; the green sheets establish the same boss's animation palette, scale, and strict 2x2 layout.
Primary request: Create exactly four strongly contrasted sequential frames of this same grey-purple toothed dust-bunny boss harmlessly imploding inward and becoming a few curling wisps of dust, arranged in a strict 2 columns by 2 rows grid in reading order. This must look like a decisive magical defeat, not a slow fade.
Sequence: Frame 1 inward pull--complete boss remains recognizable but all outer cloud curls, giant ears, and pearl paws stretch slightly toward the glowing forehead crest; four short lavender suction arcs point inward; expression is startled but not afraid or hurt. Frame 2 compression--the entire boss collapses into one much smaller dense round grey-purple dust ball at the same bottom-center anchor, with both spiral ears curled tightly around it, pearl paws tucked in, and a bright aqua-white star at the center. Frame 3 implosion snap--the recognizable body is completely gone; show a bold hollow lavender dust ring collapsing inward toward a small dark-plum center with one sharp aqua-white four-point flash and several rounded spiral fragments being pulled toward it. Frame 4 aftermath--the ring and center are gone; only three or four separated opaque grey-lavender spiral wisps curl gently upward, joined by one small clean pale-lavender sparkle. No body, face, eyes, ears, paws, or teeth remain.
Scene/backdrop: perfectly flat uniform saturated #00ff00 chroma-key background in every cell for local alpha removal; no shadows, gradients, floor, scenery, texture, or lighting variation.
Style/medium: preserve the exact polished 2D children's storybook sprite style, grey-lavender/deep-plum palette, navy-purple outlines, rounded opaque graphic dust curls, glossy highlights, and phone-readable silhouette. The implosion effects are stylized solid shapes, not realistic translucent smoke.
Composition: strict 2x2 grid, four equal square cells, consistent bottom-center anchor, full effects inside each cell with generous padding, no overlap, no borders, labels, or text. Frame 2 must be less than half the area of frame 1; frame 3 must have a clearly empty outer area and strong inward motion.
Mood: decisive, magical, surprising, harmless, and satisfying for a four-year-old.
Constraints: exactly four frames; no slow sideways dissolve, no simple fade, no explosion outward, no injury, pain, fear, bones, debris, weapon, attacker, extra character, text, logo, watermark, 3D render, or realistic smoke; no recognizable boss remains after frame 2; do not use #00ff00 in any subject or effect.
```
