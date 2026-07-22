# CC0 Ocean Replacement Prompts — 2026-07-22

Mode: OpenAI built-in image generation. No external or protected reference
images were supplied. The prompts use `ART_STYLE_GUIDE.md` as written direction.

Scope correction: the initial two sheets covered only `8/35` of the numbered
Regen list plus the separate three-file live-SeaWeed addendum. Subsequent
family calls now cover `35/35` plus `3/3`. `REGEN_35_PROMPT_PLAN.md` is the
numbered manifest and reusable corrected prompt set.

## Accepted Caribbean nautical sheet

```text
Use case: stylized-concept
Asset type: high-resolution 2D-to-3D model-reference sheet for a tightly scoped CC0 replacement family in a preschool Mobile game
Primary request: create exactly five original Caribbean nautical replacement props for Mermaid Roshan: Reef of Light, to replace the live non-original Kenney Pirate Kit roles barrel, chest, cliff_cave_rock, ship-ghost, and ship-wreck; this sheet will be handed to Claude for separate low-poly 3D reconstruction
Scene/backdrop: perfectly plain warm shell-cream studio board, no ocean scene, floor plane or decorative environment
Subject: (1) one squat rope-banded wooden barrel with broad staves; (2) one closed treasure chest with oversized readable lid, hinge and latch; (3) one broad stable limestone cave-mouth rock with a child-sized swim-through opening; (4) one complete friendly ghost ship with intact readable hull, two simple masts and soft pearl-lavender spectral color blocks; (5) one grounded broken shipwreck section with a readable hull rib, snapped mast and broad safe plank shapes; each is a separate reusable asset
Style/medium: Mermaid Roshan children's game asset design, clean flat-color anime cel illustration, rounded readable toy-playset geometry, thin dark-indigo contour, two or three broad value bands, high-key underwater cyan fill, aqua and lavender shadows, warm coral and brass focal accents, extremely restrained surface grain, completely original
Composition/framing: 1536x1024 landscape model sheet; exactly five horizontal rows, one replacement role per row; every row contains matching front, side, back and three-quarter orthographic-style views with identical proportions and colors; generous whitespace; no cropped geometry
Lighting/mood: even diffuse studio lighting, gentle adventurous Caribbean warmth, emotionally safe
Materials/textures: matte hand-painted honey wood, muted brass, rope cream, pearl-lavender spectral wood, broad pale limestone planes; no glossy plastic
Constraints: only these five replacement roles; absolutely no display bases, plinths, pedestals, floor discs, ground patches or contact-shadow ovals; show each object's natural bottom/contact geometry directly against the plain background; no characters, animals, coral, plants, shells, sand, water, particles, cast shadows or scenic dressing; no text or labels; no logos, trademarks, watermark or copyrighted franchise symbols; no photorealism, gritty damage, horror, skulls, weapons, black shadows, tiny greebles, sharp splinters or thin fragile parts; recognizable at phone thumbnail size and suitable for independent Mobile-safe 3D modeling
```

## Accepted Norwegian rock and kelp sheet

```text
Use case: stylized-concept
Asset type: high-resolution 2D-to-3D model-reference sheet for a tightly scoped CC0/non-original replacement family in a preschool Mobile game
Primary request: create exactly six original Norwegian cold-water replacement props for Mermaid Roshan: Reef of Light, to replace the live non-original roles cliff_block_rock, cliff_large_rock, rock_largeA, SeaWeed, SeaWeed1, and SeaWeed2; this sheet will be handed to Claude for separate low-poly 3D reconstruction
Scene/backdrop: plain cool shell-cream studio board, no ocean scene and no decorative environment
Subject: three independent broad Norwegian fjord-rock forms—one low interlocking block-rock cluster, one tall asymmetrical cliff rock with broad stable ledges, one large rounded boulder with readable teal/lavender facets—and three independent rooted cold-water macroalgae forms—one broad sugar-kelp clump, one finger-kelp clump, one bladderwrack-like branching clump; each plant has a single believable holdfast and thick countable S-curved blades; each role is a separate reusable asset
Style/medium: Mermaid Roshan children's game asset design, clean flat-color anime cel illustration, rounded readable toy-playset geometry, thin clean dark-indigo contour, two or three broad flat value bands, high-key underwater cyan fill, aqua and lavender shadows, restrained leaf green and cool gold accents, extremely restrained surface grain, completely original
Composition/framing: 1536x1024 landscape model sheet; organize exactly six clearly separated rows or cells; every asset gets matching front, side, back and three-quarter orthographic-style views with identical proportions and colors; show each object's natural contact edge or plant holdfast; generous whitespace; no cropped geometry
Lighting/mood: even diffuse studio lighting, clear welcoming cold-fjord identity, never dark
Materials/textures: matte broad grey-teal stone planes with cream/cyan top highlights; thick sculptural kelp blades with simple painted value bands; no glossy plastic and no transparent alpha cards
Constraints: only these six replacement roles; no display bases, pedestals, floor discs, ground patches, snow caps, ice crystals, coral, tropical sponges, shells, animals, ships, water, particles, cast shadows or scenic dressing; no text or labels; no logos, trademarks, watermark or copyrighted franchise symbols; no photorealism, scanned crags, noisy displacement, black shadows, tiny greebles, detached single leaves, thin fragile blades or mixed-biome decoration; recognizable at phone thumbnail size and suitable for independent Mobile-safe 3D modeling
```

## Rejected Caribbean iteration

The initial Caribbean prompt asked for support bases while also prohibiting
ground patches. The output resolved that contradiction as turquoise display
plinths under every prop, so it was rejected and regenerated with the explicit
no-plinth contract above. The rejected PNG is retained; it is not an accepted
modeling reference.

## Completed family-call evidence

The accepted output filenames and their numbered rows are recorded in
`REGEN_35_PROMPT_PLAN.md`. Its shared production block plus family blocks A–L
form the corrected prompt set used for the complete handoff.

- The first item-07 crystal-castle generation was rejected because it added
  freestanding crystal clutter around the foundation. The corrected call
  required exactly three attached architectural crystal roofs and prohibited
  every loose crystal cluster.
- The first items-09–10 butterfly generation was rejected because its closed-
  wing state and leg anatomy were unreliable. The corrected call required,
  for each species, open, half-folded, strict closed-profile and three-quarter
  poses plus the `four wings / six legs / two antennae` anatomy contract.
- All other new family sheets passed their recorded role-count, silhouette and
  support-geometry checks on their first retained iteration.

## Ecosystem context prompt set

The Caribbean context prompt requests a wide gameplay-distance reef with an
open central swim route and abundant independent elkhorn-like, staghorn-like,
massive star/boulder-coral, sea-fan, tube-sponge and rooted-seagrass families.
It prohibits Norwegian kelp and forbids fusing habitat to any Regen prop.

The Norwegian context prompt requests two distinct depth panels: shallow rooted
forests of tangle/stortare, sugar kelp, finger kelp and winged kelp; and deep
cold-water branching coral, horn-coral/sea-tree and sponge gardens. It prohibits
tropical coral and forbids mixing shallow kelp with the deep coral families.

Both outputs are context-only density and placement references. They do not add
Regen IDs or authorize combined habitat meshes.
