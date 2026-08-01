# Sky Lagoon ambient animals - generation ledger

## Gap and scope

The three-screen promenade had fish, insects, and birds in its collection roster but no terrestrial ambient animals. The owner explicitly requested newly generated fauna rather than reuse. This batch adds every audited candidate except ranked option 3, the black-tailed deer fawn: summer-coat snowshoe hare, Douglas squirrel, Pacific Northwest raccoon, North American river otter, and Pacific tree frog.

No protected art under `assets/book/`, `assets/audio/voices/`, or `assets/characters/friends/` was modified or used as delivery pixels. The assets are ambient interactions, not objectives, collectibles, or save-state rewards.

## Generation and processing

- Generation mode: OpenAI built-in image generation, project-original bitmap output.
- Layout: one 2x2 idle sheet and one 2x2 startle/exit sheet per animal.
- Source canvas: 1254x1254 flat magenta chroma background.
- Background removal: installed `remove_chroma_key.py` with `--auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill`.
- Runtime normalization: whole-canvas Pillow Lanczos resize to 512x512 RGBA; no pose was individually moved, warped, masked, or composited.
- Runtime atlases: ten POT textures under `assets/sprites/sky_lagoon/animals/`, each read as a 2x2 grid by `Sprite3D`.
- Prompt ledger: `PROMPTS.md`, SHA-256 `cbc0c731c5fcd1ed86e33f796d3c0b84220257e33fbaa5e39e470d5da831663f`.
- File manifest: `manifest.csv`, SHA-256 `3be8a6504099c0b73e10b95746e4e54befae77d47409f989b3d2aff3ccc34129`.
- Review contact sheet: `contact_sheet_runtime.png`, SHA-256 `04a665f7f4b084bfdabaefb9ad24494011b0da9a1075e8499437d61336465834`; review-only and not loaded by the game.

## Human review

All ten runtime atlases were reviewed at source and runtime scale against the established Sky Lagoon audit:

- identity remains stable between idle and activation sheets;
- each sheet contains exactly four complete, separated poses;
- silhouettes and deep plum contours remain readable against cyan sky, aqua water, and green foliage;
- startles read as playful surprise without tears, trembling, threatening teeth, or distress;
- hare, squirrel, raccoon, and otter retain readable terrestrial anatomy;
- the frog retains four limbs and toe-pad silhouettes in its crouch and hop poses;
- magenta removal leaves transparent corners and useful subject coverage in all four atlas cells;
- runtime textures are 512x512 POT and collectively add under 1.8 MB of PNG payload.

## Runtime behavior

The five-species roster uses one pooled `Sprite3D` card and one pooled contact shadow. Only the current page's animal is instantiated visually, keeping transparent overdraw inside the Speedy-tier budget. Each page has an ecological roster and authored three-point habitat paths:

- arrival shore: otter and frog at the pond edge, unavailable until the pearl plane departs;
- west meadow edge: hare and squirrel behind the navigation lane and west of the slide;
- castle shrub edge: raccoon west of the castle, outside the drawbridge and door approach.

Every path is rejected at runtime if a waypoint enters a toy, screen-seam, drawbridge, or door exclusion rectangle, or comes within 3.2 world units of the painted player route. Species-specific cadence, pauses, bob amplitude, and idle atlas frames produce hops, waddles, scampers, and ambles instead of a shared lateral slide.

A single tap switches to the activation sheet: alert, squash, hop, then a looping two-pose run or hop through the authored safe edge. Animals exit toward cover rather than across the player route, playground equipment, or castle entrance. After a short cooldown the page advances to its next species. No animal can block travel, alter progression, or be lost permanently.

The cards remain unshaded to match the flattened storybook mural, but each species has audited day/night modulation and habitat-colored contact shadows. The reproducible in-game lighting audit is documented in `docs/audits/SKY_LAGOON_ANIMALS_2026-08-01.md`.
