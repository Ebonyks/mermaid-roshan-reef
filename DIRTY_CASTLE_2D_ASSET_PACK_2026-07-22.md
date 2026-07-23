# Dirty Castle 2D Asset Pack

## Outcome

This pass establishes a full visual vocabulary for the game's new opening:
Mermaid Roshan arrives at the Pearl Castle, discovers that it needs cleaning,
and works with Daddy Mermaid, Baby Eagle, and a friendly family of dust bunnies
to make it shine.

The mess remains part of the same upbeat cartoon world as the castle. Dust
bunnies are the only living mess motif. They are helpers and neighbors, never
enemies, hazards, or things the child is asked to destroy.

The deliverable is asset-only. It does not change startup flow, progression,
save data, voices, or castle scripts. Runtime wiring can land as a separate
mechanically tested change.

The completed pack contains 132 production images:

- 18 small and medium dirty-target sprites;
- 6 large object/room mess vignettes;
- 6 reusable dust-bunny character poses;
- 12 castle-specific cleaning and sorting tools;
- 12 cleanup, bunny-motion, and friendship effects;
- 6 non-reading-dependent progress and completion badges;
- 30 high-detail object skins made for the existing Playroom, Royal Library,
  Royal Kitchen, Bubble Bath, hidden Royal Loo, and undercroft;
- 6 large before-cleaning room vignettes for those same existing spaces;
- 5 additional exact-model targets in the Hall and shared castle set, bringing
  the scene-bound skin total to 41;
- 36 coherent 16:9 cinematic frames;
- one machine-readable reuse and sequencing manifest;
- a room-accurate Godot and Claude implementation handoff;
- preserved full-resolution generation masters, exact prompts, and QA sheets;
- a deterministic processing script for regenerating every runtime image.

The room object skins were completed and reviewed before the 36-frame cinematic
expansion began. A later strict resemblance pass rejected all 41 scene-bound
concept redraws, regenerated them from exact transparent renders of the shipped
GLBs, and passed all 41 at 5/5. The other 55 runtime sprites are tools,
characters, grime-only targets, effects, and progress art, so clean-object
resemblance is not applicable to them.

## Pool decision

The pool was not included. At the generation baseline, `origin/dev` was
`6de38d15c7ecd58b61b4898201b74d5c1f926512`; it contained no Roshan-pool
feature file or pool callsite. The local `codex/roshan-pool-pnw` worktree
pointed at that same commit, so it had not landed on `dev`.

This follows the owner's condition to include the pool only after it reaches
`dev`. The target, tool, effect, and dust-bunny families are modular, so a
future pool-cleaning beat can reuse the suds, sponge, squeegee, cloths, bubbles,
swoosh, clean ring, pearl progress, and bunny celebration poses.

## Runtime art inventory

All 96 interactive/reusable sprites are transparent 512×512 RGBA PNGs. Every
asset has a large silhouette, phone-readable value grouping, and transparent
margin for a pointer pulse or tap-scale tween.

For the 41 scene-bound skins, the clean pixels now come directly from 30 shipped
Godot GLBs rendered by `tools/render_dirty_castle_references.py`. The processor
adds only a removable grime layer. Legacy filenames remain stable for future
callers, but the image and `scene_resemblance_ledger.json` are authoritative.
For example, `playroom_shell_tea_set.png` depicts the real shell drum,
`playroom_wheeled_shell_toy.png` depicts the real sailboat, and
`kitchen_tipped_cups.png` depicts the real teapot and kettle.

| Family | Runtime location | Assets | Intended use |
| --- | --- | ---: | --- |
| Dust-bunny cast | `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/` | 6 | Living mess, ambient helpers, reaction poses, cinematic inserts |
| Dirt and clutter targets | `assets/castle/dirty_cleanup_2d/targets/` | 18 | Hall and room-specific cleanup/sorting targets |
| Large mess vignettes | `assets/castle/dirty_cleanup_2d/targets/vignettes/` | 6 | Chandelier, banner, throne, pantry, craft table, toy chest |
| Cleaning and sorting tools | `assets/castle/dirty_cleanup_2d/tools/` | 12 | Tool choice, HUD cards, Sprite3D props, cinematic inserts |
| Cleanup and bunny effects | `assets/castle/dirty_cleanup_2d/effects/` | 12 | Pointer, progress, motion, friendship, target and section completion |
| Progress and reward badges | `assets/castle/dirty_cleanup_2d/progress/` | 6 | One/two/three-step feedback, tidy stack, bunny home/helper rewards |
| Playroom object skins | `assets/castle/dirty_cleanup_2d/rooms/playroom/` | 6 | Puzzle, stacking, tea set, dress-up, balls/cushion, wheeled-toy sorting |
| Library object skins | `assets/castle/dirty_cleanup_2d/rooms/library/` | 6 | Books, ribbons, scrolls, cart, cushions, and icon-only picture cards |
| Royal Kitchen object skins | `assets/castle/dirty_cleanup_2d/rooms/royal_kitchen/` | 6 | Existing sink, counter, stove, cups, pan, and cabinet dirty states |
| Bubble Bath object skins | `assets/castle/dirty_cleanup_2d/rooms/bubble_bath/` | 6 | Existing tub, mirror, vanity, towels, toys, and water-droplet states |
| Royal Loo and undercroft skins | `assets/castle/dirty_cleanup_2d/rooms/basement/` | 6 | Safe loo soap/water states plus storage and stair dust |
| Room before-cleaning vignettes | `assets/castle/dirty_cleanup_2d/targets/room_vignettes/` | 6 | Large section-intro skins for six existing castle areas |
| Cinematic | `assets/cinematics/dirty_castle/` | 36 | Expanded room-by-room discovery, teamwork, and victory sequence |
| Manifest | `assets/castle/dirty_cleanup_2d/manifest.json` | 1 | Exact paths, room reuse, sequence, voice intent, interaction contract |
| Godot / Claude handoff | `DIRTY_CASTLE_2D_GODOT_HANDOFF_2026-07-23.md` | 1 | Rendering modes, room anchors, interaction, save, and probe direction |

The cinematic frames are 1024×576 RGB PNGs. That is a native 16:9 composition
under the 1024px runtime texture limit and scales cleanly to the project's
1280×720 canvas.

## Dust-bunny cast

The six poses support gameplay and story reuse rather than one baked scene:

1. curl-eared front pose for target discovery and idle bob;
2. sibling pair for cooperative pushing or sorting;
3. hopping pose with a separate curled motion tail;
4. shell-hide pose for peekaboo and room discovery;
5. sleepy pose for beds, cushions, and quiet rooms;
6. family pose for the final cozy-home payoff.

The related motion/effect family adds a bunny hop, lavender poof, curled trail,
peek eyes, friendship heart, and cloud-and-shell nest. No dark puff or
soot-creature character remains in the source or runtime pack.

## Story sequence

| Frames | Act | Narrative purpose |
| ---: | --- | --- |
| 01–08 | Grand Hall | Discover the mess and dust bunnies, choose roles, give each family member a hero beat, reveal the clean Hall |
| 09–13 | Playroom | See six toy groups, sort big and small objects, show an unmistakably open and tidy room |
| 14–18 | Royal Library | Plan shelf/cart/rug jobs, return the last book/ribbon/scroll, settle into wordless storytime |
| 19–20 | Basement descent and Pantry | Follow the bunnies downstairs and establish the existing basement room sequence |
| 21–25 | Existing Royal Kitchen | Assign safe sink/counter/cool-stove jobs and restore plates, cups, pans, and jars |
| 26–29 | Existing Bubble Bath | Clear fog, soap, towels, toys, and clean droplets; reveal the hidden arch |
| 30–32 | Hidden Royal Loo | Treat soap, rolls, holder, and clean water matter-of-factly; open the way to storage |
| 33–34 | Undercroft | Organize storage and clear the stair, then carry the bunnies toward the Hall |
| 35–36 | Finale | Inspect every clean area, settle the bunny family, and high-five |

No frame uses captions or reading-dependent information. The manifest records a
short voice intention for each beat; implementation should route equivalent
recorded or existing voice through `_say()` rather than display text alone.
The complete 36-row beat sheet, character actions, continuity rules, and
rejection history are in `DIRTY_CASTLE_CINEMATIC_36_2026-07-23.md`.

## Room-by-room reuse

### Grand Hall

- dust-bunny pile and character poses;
- corner cobweb, footprints, scuff, sticky spill, and window smudge;
- dusty chandelier, crooked banner, and smudged throne vignettes;
- mop, bucket, sponge, brush, broom, duster, bubbles, wipe, clean ring, and
  three-pearl progress.

### Playroom

- shell-and-star puzzle pieces, knocked stacking rings, shell tea set,
  dress-up pile, balls/beanbag, wheeled shell toy, and a large room vignette;
- sorting basket, folded cloths, dusting mitt, tidy-stack badge;
- sibling, sleepy, hopping, and cloud-nest bunny poses.

### Royal Library

- fallen picture books, bookmark ribbons, scrolls, book cart, reading
  cushions, icon-only picture cards, and a large room vignette;
- ribbon duster, cleaning cloths, shell dish/basket;
- sibling and helper bunnies, bunny trail, helper badge.

### Pantry

- flour spill, leaf trail, untidy shelf and pantry vignette;
- star sponge, cloths, basket, shell broom;
- bunny carrying cloth and bunny rolling a lost bead.

### Craft Room

- craft scraps, buttons/beads, paint splats, and messy craft-table vignette;
- sorting basket, cloths, mitt, tidy-stack badge;
- bunny hop, trail, and friendship-heart effects.

### Existing Royal Kitchen

- sink-and-plates, counter flour, cool stove drips, tipped cups, crooked pan,
  cabinet jars, and a large room vignette;
- these skins overlay the basement kitchen already built in
  `CastleHall.build_basement_wing()`; no second kitchen is introduced.

### Existing Bubble Bath, hidden Royal Loo, and undercroft

- tub soap ring, foggy mirror, vanity droplets, towels, bath-toy basket, and
  water-droplet trail;
- safe toilet soap ring, crooked paper rolls, brush holder, and clean splash;
- dusty storage and stair cobweb, plus one room vignette for each area;
- no waste, mold, rot, frightening darkness, or living grime.

### Bedrooms

- cloudy mirror, soap ring, window smudge, cloud cushions;
- squeegee, cloths, scrub brush, spray bottle;
- shell-hide, sleepy, family, and cloud-nest bunny poses.

## Recommended play loop

1. Show one large target at a time with `fx_clean_ring`.
2. Speak the objective and point at the target.
3. Accept repeated taps or a very forgiving short swipe.
4. Show `fx_soap_bubbles`, `fx_soap_foam`, or a bunny reaction on every
   successful input.
5. Dissolve or sort the target, show `fx_gold_sparkle`, and save immediately.
6. Fill one, two, then three gold pearls for a short room section.
7. End with a tidy badge or bunny-helper badge and one cinematic transition.

There is no timeout, penalty, health, wrong tool, or restart. Daddy, Baby Eagle,
and the dust bunnies may animate beside the child, but they must not finish a
section while Roshan is idle.

## Visual and technical contract

- Current Pearl Castle geometry and palette are preserved: cream shell capitals,
  lavender stone, burgundy carpet, aqua, coral, restrained gold, and deep
  navy-purple contour.
- Scene-bound dirty skins preserve the exact rendered silhouette, materials,
  proportions, orientation, and clean RGBA pixels of their shipped GLB source.
  Dirt may add pixels, but it may not repaint or redesign the clean object.
- Dirt is playful and sparse. There is no mold, rot, garbage, insect, or
  frightening grime.
- Dust bunnies use lavender spiral curls, pearl paws, round eyes, blush, and
  shell/cloud homes. They remain visually distinct from generic smoke puffs.
- Character generations use protected art only as identity reference. No file
  under `assets/book/` or `assets/characters/friends/` was changed,
  recompressed, replaced, or moved.
- Baby Eagle keeps the turquoise, yellow, pink, black-gray, and large-eye
  identity of the book art; the unrelated backpack is absent.
- Runtime sprites use sampled-border chroma removal, a soft matte, despill, and
  connected-component assignment to prevent neighboring atlas cells from
  leaking into a cutout.
- Cinematic masters use a centered 16:9 crop and 1024×576 Lanczos resize.
- The pack adds no lights, particles, physics bodies, audio, or
  renderer-specific effect. All feedback can be implemented as one or two
  unshaded sprites.
- Exact prompt and edit records live in
  `assets_src/concepts/dirty_castle_cleanup_2026-07-22/PROMPTS.md`.
- Skin placement and runtime direction for Godot/Claude live in
  `DIRTY_CASTLE_2D_GODOT_HANDOFF_2026-07-23.md`.
- Rebuild with `python tools/process_dirty_castle_2d.py`.

## Review evidence

- `audit/dirty_castle_2d_2026-07-22/sprites_contact.png` shows all 96 runtime
  sprites against a checkerboard.
- `audit/dirty_castle_2d_2026-07-22/cinematic_contact.png` shows all 36
  normalized runtime frames in story order.
- `audit/dirty_castle_2d_2026-07-22/scene_reference_objects.png` shows the 30
  exact transparent renders made from the live GLBs.
- `audit/dirty_castle_2d_2026-07-22/scene_resemblance_pairs.png` shows every
  audited clean/dirty pair.
- `audit/dirty_castle_2d_2026-07-22/scene_resemblance_ledger.json` and `.csv`
  record the live resource path, dirt style, silhouette recall, changed-pixel
  ratio, padding check, initial failure, and final 5/5 score for all 41 skins.
- `DIRTY_CASTLE_SCENE_RESEMBLANCE_AUDIT_2026-07-23.md` defines the five-point
  gate and the reject/regenerate/re-audit history.
- The processor validates 512×512 RGBA output, nonempty alpha coverage, and
  transparent corners for every interactive sprite.
- The processor additionally enforces 100% clean-silhouette recall, unchanged
  clean pixels outside the recorded grime mask, exact source provenance, and
  24-pixel transparent padding for every scene-bound skin.
- The manifest enumerates all 96 sprites and all 36 cinematic frames and may
  claim skin readiness only while the scene-resemblance result remains 5/5.

These assets form a coherent implementation pack, but the gameplay section
itself remains unimplemented until a separate runtime change wires the
cinematic, interaction, voice, pointer, agency, and save contracts.
