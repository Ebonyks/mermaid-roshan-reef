# Mermaid Roshan: Color and Contrast Audit

Date: 2026-07-15
Branch: `codex/audit-easy-repairs`
Game commit evaluated: `287353e`
Renderer: Godot 4.4 Forward Mobile, 1280x720, Speedy quality

## Outcome

The game does not have a universal color problem. The reef, dark/neon games,
picture games, castle interiors, utility screens, combat, dungeon, and kart
have usable tonal separation and strong UI readability. However, six bright
contexts remain visibly overexposed or washed out:

1. Lamb-a' sunny meadow / seek
2. Sunset play-place / race
3. Snow fetch yard
4. Penguin ice slide
5. Rainbow slide
6. Butterfly World / Galaxy

Sky Lagoon's daytime exterior is readable but still too pale, and the dolls
nursery is intentionally quiet but flatter than the rest of the game.

This is a profile-consistency problem rather than an asset problem. Bright
scenes independently combine high ambient energy, near-white or greater-than-
white albedo, the global bright ACES grade, and sometimes large emissive
surfaces. Speedy mode limits bloom but does not constrain the other contributors.

## Method

Twenty-eight representative frames were captured from the production Mobile
renderer with an isolated save directory. Coverage included:

- reef day and night;
- every friend-game lighting family;
- snow, meadow, nursery, concert, sunset play-place, shop, cavern, both slides,
  and Fairy Pond;
- all four active 2D picture-game palettes;
- Sky Lagoon, the castle hall, music room, bedroom, and basement;
- wardrobe, craft studio, and pause screens;
- ice combat, dungeon, Rainbow Kart, and Butterfly World.

Frames were inspected visually and sampled every four pixels for white clipping,
channel clipping, black crush, average luminance, luminance deviation, 5th-to-
95th percentile range, and average chroma. Channel clipping alone was not used
as a failure signal because flat saturated illustration colors legitimately put
one channel at 1.0. Visual loss of form and luminance compression determined the
result.

Suggested full-frame acceptance envelope for bright gameplay scenes:

- mean luminance: 0.55-0.80;
- luminance standard deviation: at least 0.12;
- 5th-to-95th percentile range: at least 0.28;
- pure-white coverage: below 5%, excluding short victory flashes;
- broad gameplay surfaces must retain visible texture and silhouette edges.

Dark neon scenes are evaluated by target visibility rather than the bright-scene
mean. Their interactive objects must remain separated from the background even
when large areas are intentionally dark.

## Findings by state

| State | Result | Evidence | Assessment |
|---|---|---:|---|
| Reef day | Pass | mean 0.56, range 0.67 | Saturated but coherent; characters, terrain, and flora separate. |
| Reef night | Pass | mean 0.45, range 0.71 | Stronger hierarchy than day; bioluminescence remains localized. |
| Snow fetch | Repair | mean 0.81, 34% channel clip | Snow texture is present but most broad surfaces read nearly white. |
| Seek meadow | Critical | mean 0.96, range 0.06, 15.5% pure white | Severe washout; bushes, Lamb-a', Roshan, and terrain lose form. |
| Dolls nursery | Watch | mean 0.70, range 0.05 | Targets remain readable through outlines, but the background is unusually flat. |
| Melody stage | Pass | mean 0.47, range 0.95 | Excellent dark-to-bright separation. |
| Sunset play-place | Critical | mean 0.87, range 0.19 | Orange wash compresses floor, structures, props, and characters together. |
| Pearl Shop | Pass | mean 0.78, range 0.51 | Warm and bright, but material and silhouette separation remain usable. |
| Treasure cavern | Pass | mean 0.36, range 0.95 | Dark surround and clipped treasure sparkles create an intentional focal hierarchy. |
| Penguin ice slide | Critical | mean 0.93, range 0.10 | Track, snowbanks, and sky merge into a pale blue-white field. |
| Rainbow slide | Critical | mean 0.90, range 0.22 | Colored bands survive, but the track and rails lose depth and texture. |
| Fairy Pond | Pass | mean 0.29, range 0.56 | Neon targets are distinct against the dark pond. |
| Picture: snowman | Pass | mean 0.75, range 0.24 | Low-key snow palette remains readable through rims and shadows. |
| Picture: garden | Pass | mean 0.72, range 0.40 | Clear target/background separation and consistent pastel saturation. |
| Picture: trampoline | Pass | mean 0.78, range 0.37 | High blue-channel use is intentional, not white clipping. |
| Picture: Christmas | Pass | mean 0.29, range 0.21 | Dark palette has sufficient object contrast. |
| Sky Lagoon day | Watch | mean 0.84, range 0.46 | Castle and path read, but snowfields and white sparkles are too pale. |
| Castle hall | Pass | mean 0.72, range 0.48 | Pale by design, with adequate lavender/gold edge separation. |
| Castle side rooms | Pass | means 0.61-0.65 | Music and bedroom palettes are coherent and more grounded than the hall. |
| Castle basement | Pass | mean 0.67, range 0.44 | Adequate warm/cool and floor/prop separation. |
| Wardrobe, craft, pause | Pass | ranges 0.60-0.78 | Strong overlays, dark backplates, and readable buttons. |
| Combat and dungeon | Pass | ranges 0.83-0.86 | Saturated action colors retain excellent silhouette contrast. |
| Rainbow Kart | Pass | mean 0.58, range 0.60 | Soft galaxy palette remains legible without broad clipping. |
| Butterfly World | Critical | mean 0.70, 15.3% pure white | Broad white panels and the pale planet overwhelm character and prop color. |

## Root causes

### 1. Bright scenes stack independent exposure sources

The shared grade uses ACES with exposure `1.15` and white point `1.2`. Several
bright arenas then add ambient energy between `0.9` and `1.2`, pale backgrounds,
and near-white materials. The sunset floor even starts with a red component of
`1.05`. ACES cannot recover surface detail that has already converged near white.

### 2. Speedy mode clamps only glow

`_speedy_glow_clamp()` limits glow intensity and bloom, which is useful, but it
does not cap:

- tonemap exposure;
- ambient-light energy;
- directional-light contribution;
- material albedo above 1.0;
- emission on broad geometry.

This explains why snow remains washed out even with bloom reduced to `0.05`.

### 3. Lighting profiles are decentralized

The reef, generic arenas, Sky Lagoon, Butterfly World, kart, and combat construct
their own environments. Some use the shared grade and Speedy clamp, while others
do not. Visually similar white surfaces therefore receive materially different
exposure treatment.

### 4. UI treatment is more consistent than world treatment

Most gameplay text uses white fill, a dark navy outline, and large type. Modal
screens use dark translucent backplates. This remains readable across nearly
every captured palette. The visual repair should preserve this UI system and
focus on world exposure beneath it.

## Intervention plan

### Phase 1: centralize bright-scene grading

Add a small shared scene-grade helper with named profiles instead of editing the
global reef grade:

- `underwater`: current reef behavior;
- `bright_pastel`: snow, meadow, slides, and Sky Lagoon;
- `warm_pastel`: sunset play-place and shop;
- `dark_neon`: cavern, fairy, concert, combat, and dungeon;
- `galaxy`: Butterfly World and floating kart.

Each profile should set ACES exposure and white point, brightness/contrast,
glow threshold/intensity/bloom, and an ambient-energy ceiling. Speedy should
select a complete profile variant rather than only changing bloom.

### Phase 2: repair the six outliers

Starting ranges for capture-driven tuning, not final locked values:

1. **Seek meadow:** reduce ambient energy from `1.2` toward `0.65-0.75`; tint the
   near-white grass floor into a mid pastel green; use bright-profile exposure
   around `0.75-0.85` and white point around `1.3-1.45`.
2. **Sunset play-place:** remove albedo components above `1.0`; reduce ambient
   energy toward `0.7-0.8`; darken the orange ground and sky enough for pink,
   lavender, yellow, and aqua props to remain distinct.
3. **Snow fetch:** retain the authored snow texture but lower the broad snow
   response through exposure and sun/ambient balance. Do not solve this by
   removing texture or making snow gray.
4. **Ice and rainbow slides:** apply the same bright-pastel profile, lower broad
   rail/track emission, and introduce lavender/aqua shadow values so bank, track,
   fish, penguin, and sky have separate bands.
5. **Butterfly World:** apply ACES plus a Speedy-aware galaxy profile; replace
   broad pure-white panels with pale lavender/aqua values and reserve true white
   for small stars, UI, and momentary effects.

### Phase 3: tune the two watch states

- Give the dolls nursery a slightly darker blue-lavender lower field or soft
  vignette, preserving its calm tone while increasing doll/catcher depth.
- Lower Sky Lagoon's snowfield response slightly while preserving the readable
  castle and pastel path.

### Phase 4: make color regression testable

Keep a lightweight screenshot probe for the representative states and fail only
on strong signals:

- pure-white coverage above 8% in a stable gameplay frame;
- bright-scene mean above 0.88;
- bright-scene percentile range below 0.18;
- missing capture or invalid environment.

Numeric thresholds should flag review, not replace visual approval. Saturated
cartoon colors can legitimately clip a single channel.

## Recommended order

1. Seek meadow
2. Ice and rainbow slides
3. Sunset play-place
4. Butterfly World
5. Snow fetch
6. Sky Lagoon and dolls nursery refinement

This order addresses the scenes where a child is currently most likely to lose
the player character or objective against the background. It does not require
changes to protected book art, family voices, friend art, or the snowman/carrot
plot.
