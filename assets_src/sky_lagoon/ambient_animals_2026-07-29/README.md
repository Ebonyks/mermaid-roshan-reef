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

Each animal wanders inside a short habitat corridor at real `Sprite3D` depth with a contact shadow. A single tap immediately switches to its activation sheet: alert, squash, hop, then a looping two-pose run or hop toward the nearest screen edge. It remains absent for a cooldown and respawns only after its habitat is offscreen, except the otter's initial eight-second delay, which lets the arrival plane clear the western shore. No animal can block travel, alter progression, or be lost permanently.