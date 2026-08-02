# Imp combat animation art — prompt and review ledger (2026-08-02)

## Generation mode and record scope

- Generator: **OpenAI built-in ImageGen**, invoked from Codex.
- Runtime delivery: 179 PNG files (173 actor-state files and 6 shared FX).
- Native tool outputs are copied byte-for-byte into `candidates/`; none of the originals in Codex's generated-image store were deleted.
- `GENERATION_RUNS.json` binds every native copy to its ImageGen execution ID, SHA-256 hash, native canvas, prompt key, disposition, and rejection note.
- `DELIVERY_MANIFEST.json` binds every runtime file to its accepted source, output/report/reference hashes, QA evidence, and Mobile-renderer captures.
- Original identity references from the task's starting commit are preserved byte-for-byte in `references/*_source_idle.png`, including idles that were repaired during this work.

The Popstar and FX prompts below are the exact tool prompts. The earlier base-imp and first eleven costume-family prompts are normalized reconstructions from the active Codex session record after the wording was no longer available verbatim. They preserve the generator, reference, required state, layout, identity/prop locks, background, exclusions, and acceptance intent, but are deliberately labeled `RECOVERED` rather than falsely presented as exact. The native execution IDs and hashes remain exact.

## Shared constraints used in every actor prompt

`IDENTITY_LOCK` means: use the attached `references/<family>_source_idle.png` as the exact character identity, costume, palette, proportions, face, horn/ear/tail shapes, footwear, and held-prop reference. Every visible held prop remains present in the same hand in every state. No character redesign or costume substitution is allowed.

All actor requests also required:

- polished soft cel-shaded 2D children's storybook/game art matching the approved imp set;
- clean navy/indigo contours, never black;
- a perfectly flat `#00FF00` chroma field, with no transparency in the native request;
- one complete, non-cropped, non-overlapping full-body character per occupied cell;
- no labels, panels, ground, shadows, scenery, particles, detached stars, speed lines, dust, glow, or other baked FX;
- similar scale and generous green space in each cell;
- `bopped` alone has two readable spiral eyes, painted into the face, and never baked stars.

## Recovered actor prompt keys

### `BASE_STATE_RECOVERED`

> Create one square 1024×1024 production sprite on a perfectly flat solid `#00FF00` chroma-green background. Use the attached approved base-imp idle as `IDENTITY_LOCK`. Draw exactly one complete full-body `[STATE]` pose matching the handoff's timing silhouette: `[STATE_DIRECTION]`. Preserve every identity and garment detail. Center the whole character with generous green margin. No crop, labels, duplicate character, ground, shadow, scenery, particles, detached pieces, or baked FX. Polished soft painterly/cel-shaded children's storybook game sprite with navy/indigo contours.

`[STATE_DIRECTION]` was the corresponding direction in `CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md` §3: crouched anticipation for windup; forward launch for charge; neutral-upright swept follow-through for slash; harmless exhausted slump for recover; crossed-arm brace for guard; surprised backward reel for stagger; three-quarter-back retreat for flee; and cheeky standing showboat for taunt.

### `BASE_BOW_RECOVERED`

> Regenerate the attached imp captain as one complete 512-ready curtain-call bow on flat `#00FF00`, preserving `IDENTITY_LOCK` and slimmer approved proportions. Deep stage bow to viewer-left, one arm swept outward, feet planted. Repair the rejected shorts/alpha-hole topology by returning a newly generated complete character, not by painting over the old pixels. No crop, ground, shadow, labels, duplicate, detached elements, or baked FX.

### `COSTUME_SHEET_A_RECOVERED`

> Create one square production sprite sheet on flat `#00FF00`, using the attached rival idle as `IDENTITY_LOCK`. Exactly six separate full-body poses in a strict 3×2 grid, row-major: idle repair, windup, charge, slash, recover, guard. Preserve face, costume and held prop in the same hand across every cell. Each pose must match the handoff silhouette, remain complete and non-overlapping, and contain no baked FX. No labels, borders, panels, shadows, ground, scenery, particles, duplicates, or extra props.

### `COSTUME_SHEET_B_RECOVERED`

> Create one square production sprite sheet on flat `#00FF00`, using the attached approved rival idle and accepted Sheet A as `IDENTITY_LOCK`. Strict 3×3 grid with exactly seven occupied cells in row-major order: stagger, flee, bopped, bow, hop_a, hop_b, taunt. Leave cells 8 and 9 completely empty green. Preserve all identity/costume/prop details and hand assignment. `bopped` has two clear matching spiral eyes but no stars. No crop, labels, panels, ground, shadows, scenery, particles, motion trails, detached pieces, duplicates, or baked FX.

### `SINGLE_REPAIR_RECOVERED`

> Regenerate only the rejected `[STATE]` for the attached approved rival, using the original idle and accepted adjacent sheet poses as `IDENTITY_LOCK`. Return one complete full-body `[STATE]` cutout on flat `#00FF00` with the same costume and same-hand prop continuity. Correct `[REJECT_CAUSE]`; do not alter the character design. No baked FX, crop, labels, ground, shadow, scenery, duplicate, or detached elements.

### `REPAIR_SHEET_RECOVERED`

> Regenerate exactly the listed rejected states for the attached approved rival as a small ordered pose sheet on flat `#00FF00`. Keep `IDENTITY_LOCK`, same-hand held props, full-body framing, and the handoff silhouettes. Empty cells remain pure green. No labels, panels, crop, ground, shadows, scenery, particles, duplicates, detached elements, or baked FX.

### `APPROVED_WINDUP_REUSE`

No generation call. Each costume's accepted windup art was uniformly re-normalized as `hop_a`, because both handoff states explicitly share the same crouched anticipation silhouette. Output paths and hashes remain distinct.

### `APPROVED_STAR_REUSE`

No generation call. `assets/mg/star.png` already met the child-readable gold-star design and licensing requirements, so it was uniformly resized and padded as `fx_stolen_sparkle.png` without adding pixels.

## Exact Popstar prompts

### `POPSTAR_SHEET_A_EXACT`

> Create one square 1024×1024 production sprite sheet on a perfectly flat, solid bright chroma-green background (`#00FF00`), using the attached `rival_popstar.png` only as the exact character identity, costume, prop, palette, and polished 2D storybook rendering reference.
>
> This is the same young friendly lavender imp rival in all six cells: large warm amber-brown eyes, tiny white fangs, pointed ears, small dark-purple forehead horns, curled lavender tail; sparkly purple jacket with silver-lavender lapels/cuffs, aqua shirt, lavender jeans and belt, purple shoes. Preserve the same shell-shaped microphone with its short pearl strand in the character's RIGHT hand in every pose where visible. Keep face, proportions, outfit design, colors, shell microphone design, and hand assignment consistent.
>
> Lay out EXACTLY SIX separate full-body poses in a strict 3-column × 2-row grid, read left-to-right, top-to-bottom: (1) WINDUP — crouched slightly, body pulled back, microphone hand drawn behind, eager focused face, clearly preparing to dash. (2) CHARGE — running rapidly toward screen-right, torso leaning forward, one leg extended behind, microphone held securely, determined but playful face. (3) SLASH — broad theatrical sweeping attack toward screen-right using the microphone arm, strong readable follow-through; NO slash trail or separate effects. (4) RECOVER — off-balance immediately after the sweep, torso twisted, one foot planted and the other catching balance, surprised friendly face. (5) GUARD — braced defensive stance, forearms and microphone held protectively across the torso, feet wide, alert face. (6) WINDUP VARIANT — compact springy preparation pose, knees bent and shoulders lowered, microphone secured, ready to hop.
>
> Exactly six characters, no seventh pose, no labels, words, borders, panels, guides, shadows, ground, scenery, particles, detached stars, glitter clouds, motion trails, props, or accessories beyond the character's own shell microphone and attached pearl strand. Each cell must contain exactly one complete, non-overlapping character with generous green space on all sides. Do not crop horns, ears, shoes, tail, microphone, or pearl strand. Keep all six poses similar in visual scale and centered within their own cells. The jacket's painted sparkle texture may remain, but do not add loose sparkles. Polished soft cel-shaded 2D children's storybook/game sprite, clean navy-purple outlines, soft lavender/aqua shading, identical to the attached approved art style. Solid chroma green must show through every empty area and between every pose; no transparency and no green reflected onto the character.

### `POPSTAR_SHEET_B_EXACT`

> Create one square 1024×1024 production sprite sheet on a perfectly flat, solid bright chroma-green background (`#00FF00`). Use the first attached `rival_popstar.png` as the exact approved identity/costume reference and the second attached six-pose sheet as the exact same-character continuity reference.
>
> The same young friendly lavender imp rival appears in every occupied cell: large warm amber-brown eyes, tiny white fangs, pointed ears, two small dark-purple forehead horns, curled lavender tail; sparkly purple jacket with silver-lavender lapels/cuffs, aqua shirt, lavender jeans and belt, purple shoes. Preserve the same shell-shaped microphone with its short pearl strand in the character's RIGHT hand whenever visible. Keep face, proportions, outfit, palette, shell microphone design, and hand assignment identical.
>
> Use a strict 3-column × 3-row grid. Place EXACTLY SEVEN full-body poses in cells 1–7, read left-to-right and top-to-bottom. Leave cells 8 and 9 completely empty solid green: (1) STAGGER — recoiling backward from a harmless bump, knees buckled, microphone secured, eyes open wide, surprised but not hurt. (2) FLEE — running quickly toward screen-right while glancing back, microphone held securely, energetic playful retreat. (3) BOPPED — comic dazed pose, knees bent and body wobbling, both eyes clearly readable as matching spiral/swirl eyes, microphone still secure; NO detached stars or effects. (4) BOW — deep theatrical curtain-call bow from the waist, one arm sweeping outward and microphone hand tucked close, warm proud smile. (5) HOP_A — compact crouched launch pose, both knees bent, heels ready to spring, microphone secure. (6) HOP_B — airborne joyful hop, both feet visibly off the ground, knees tucked differently from HOP_A, microphone secure. (7) TAUNT — playful child-safe showboat pose facing screen-left, one hand beckoning or making a cheeky gesture while holding the microphone securely in the other, friendly mischievous grin.
>
> Exactly seven characters; cells 8 and 9 must contain nothing but flat green. No labels, words, borders, panels, guides, shadows, ground, scenery, particles, detached stars, glitter clouds, motion trails, or extra props. Each occupied cell has exactly one complete, non-overlapping character with generous green space. Do not crop horns, ears, shoes, tail, microphone, or pearl strand. Keep all poses similar in scale and centered within their cells. Jacket painted sparkle texture may remain, but no loose sparkles. BOPPED must have two unmistakable matching spiral eyes painted as part of the face, not floating symbols. Polished soft cel-shaded 2D children's storybook/game sprite, clean navy-purple outlines, soft lavender/aqua shading, matching the references. Solid chroma green in all empty space, no transparency and no green reflected onto the character.

## Exact FX prompts

### `FX_RING_EXACT`

> Create a single production game FX sprite on a perfectly flat solid bright chroma-green background (`#00FF00`), using the attached approved gold star only as the painterly gold palette and soft children's-storybook rendering reference. Subject: one chunky GOLD ALARM / TELEGRAPH RING that will sit flat on the ground beneath a small mischievous imp during attack windup. Show the ring as a broad, slightly foreshortened oval viewed from above at a shallow angle, with a fully open transparent-intended center. The ring should feel energetic and magical: warm golden-yellow body, creamy highlights, a subtle pale-aqua glint, and a deep indigo-purple outer contour rather than black. Make the ring continuous and visually connected all the way around, thick enough to read at phone size, with a few integrated short triangular alarm ticks on the OUTSIDE edge that remain connected to the ring. Exactly one centered ring filling about 85% of the square with generous green margin. No character, star, exclamation mark, words, labels, ground, shadow, glow haze, particles, scenery, second ring, or detached pieces. The center and every area around it must be pure flat chroma green. No transparency in source and no green reflected onto the art.

### `FX_BANG_EXACT`

> Create a single production game FX sprite on a perfectly flat solid bright chroma-green background (`#00FF00`). Match the attached approved gold telegraph ring's exact warm gold, creamy highlight, pale-aqua glint, soft painterly storybook finish, and deep indigo-purple contour. Subject: one large chunky exclamation-mark alarm glyph, an upright “!” shape for a friendly mischievous imp's attack telegraph. The top stroke and round dot should be visually bold and highly readable at phone size. Gold body with creamy painted highlight and tiny aqua glint; deep indigo-purple contour, never black. The dot may be a separate component below the stroke, but there must be no other detached marks. Exactly one centered upright glyph with generous green margin. No words, labels, characters, ring, star, ground, shadow, glow haze, particles, scenery, duplicate glyphs, or extra punctuation. Pure flat chroma green everywhere outside the two glyph parts.

### `FX_SLASH_TRANSPARENCY_REJECTED_EXACT`

> Create a single production combat FX sprite with a TRUE TRANSPARENT BACKGROUND and alpha transparency. Match the attached gold telegraph ring's soft painterly children's-storybook finish and deep indigo-purple accent language, but this effect is WHITE and PALE AQUA, not gold. Subject: one broad SWIPE / SLASH CRESCENT sweeping from lower-left toward upper-right, a single clean curved brushstroke thickest through the middle and tapering to both ends. The inner/core body is translucent pale aqua-white at approximately 25% opacity; the leading outer edge is a narrow bright opaque creamy-white highlight with a small aqua glint. Exactly one connected wide horizontal 2:1 crescent with generous transparent margin and no other marks.

Rejected because the tool returned an RGB checkerboard painted into the pixels rather than an alpha-bearing transparent PNG. The native rejected file is retained and hash-bound; none of its pixels entered delivery art.

### `FX_SLASH_EXACT`

> Create a single production combat FX sprite on a perfectly flat solid bright chroma-green background (`#00FF00`). Match the attached telegraph ring's soft painterly children's-storybook finish and deep indigo-purple accent language, but this effect is WHITE and PALE AQUA rather than gold. Subject: one broad SWIPE / SLASH CRESCENT sweeping from lower-left toward upper-right. It is a single connected clean curved brushstroke, thickest through the middle and tapering smoothly to a point at both ends. Paint the broad core pale aqua-white, with a narrow brilliant creamy-white leading edge, a small aqua highlight, and a very subtle lavender-indigo trailing rim. Make it feel like harmless magical stage motion, never a weapon blade and never jagged. Exactly one connected crescent with a strongly wide horizontal 2:1 silhouette, centered with green margin. No characters, star, ring, exclamation mark, dust, words, labels, checkerboard, transparency preview, ground, shadow, glow haze, particles, extra strokes, speed lines, duplicate arc, or detached pieces.

### `FX_DUST_EXACT`

> Create a single production game FX sprite on a perfectly flat solid bright chroma-green background (`#00FF00`). Use the attached approved puff only as the soft clustered-cloud construction, painterly children's-storybook shading, highlight placement, and outline-weight reference. Subject: one friendly LAVENDER-WHITE GROUND DUST PUFF kicked up when a tiny imp launches into a charge. Recolor and redesign it as pale lavender, pearly white, and a small hint of aqua, with a deep indigo-purple contour rather than black. Build a single visually connected low cloud from rounded overlapping lobes; the base should be wider than the height, with two or three buoyant top lobes. Magical and harmless, not dirty smoke. Keep all tiny wisps connected to the main puff. Exactly one puff, centered low with generous green margin. No character, ring, exclamation mark, stars, debris, dirt specks, ground, shadow, glow haze, text, labels, duplicate puff, or detached droplets.

### `FX_DIZZY_EXACT`

> Create a single production game FX overlay on a perfectly flat solid bright chroma-green background (`#00FF00`), using the attached approved star as the exact warm gold palette, creamy painted highlights, rounded five-point construction, deep indigo-purple contour, and soft children's-storybook rendering reference. Subject: a DIZZY STARS OVERLAY made of EXACTLY THREE small gold stars orbiting around one thin open swirl ring. Arrange the three stars at distinct points around a loose horizontal oval orbit, vary their sizes slightly, and retain the approved friendly rounded five-point design. Add one thin continuous pale-gold/lavender swirl curve behind them that suggests rotation and leaves a large completely open center. Exactly three stars and one thin swirl ring with generous green margin. No character, extra stars, sparkles, dots, words, labels, ground, shadow, glow haze, scenery, extra motion streaks, or duplicate rings.

## Rejection and repair ledger

| Family/run | Rejected content | Resolution |
|---|---|---|
| Detective Sheet A | recover cell | regenerated as `rival_detective_recover_attempt02`; original other cells kept |
| Ballerina Sheet B | flee cell | regenerated as `rival_ballerina_flee_attempt02` |
| Farmer Sheets A/B | slash and bopped cells | regenerated individually as attempt 02 |
| Boxer Sheet B | bopped cell | regenerated individually as attempt 02 |
| Magician Sheet A | charge had a detached shoe | sheet cell rejected; regenerated as `rival_magician_charge_attempt02` |
| Magician Sheet B | flee cell | regenerated as `rival_magician_flee_attempt02` |
| Painter Sheet B | stagger, bopped, bow | regenerated together in accepted repair Sheet C |
| Astronaut Sheet B | stagger, flee, bopped | flee/bopped replaced by repair Sheet D; stagger received a final individual replacement |
| Slash FX transparent attempt | RGB checkerboard baked into pixels | rejected entirely; regenerated on chroma as attempt 02 |

Uniform target-height or centroid adjustments recorded in each accepted JSON report are whole-subject normalization only; they do not repaint, warp, isolate, or repair body parts. `hop_a` reuse and `fx_stolen_sparkle` reuse are explicit budget-conserving exceptions recorded above.
