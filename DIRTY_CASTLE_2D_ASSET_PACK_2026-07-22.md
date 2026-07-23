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

The expanded pack contains 72 production images:

- 18 small and medium dirty-target sprites;
- 6 large object/room mess vignettes;
- 6 reusable dust-bunny character poses;
- 12 castle-specific cleaning and sorting tools;
- 12 cleanup, bunny-motion, and friendship effects;
- 6 non-reading-dependent progress and completion badges;
- 12 coherent 16:9 cinematic frames;
- one machine-readable reuse and sequencing manifest;
- preserved full-resolution generation masters, exact prompts, and QA sheets;
- a deterministic processing script for regenerating every runtime image.

This is exactly three times the original 24-image pass.

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

All 60 interactive/reusable sprites are transparent 512×512 RGBA PNGs. Every
asset has a large silhouette, phone-readable value grouping, and transparent
margin for a pointer pulse or tap-scale tween.

| Family | Runtime location | Assets | Intended use |
| --- | --- | ---: | --- |
| Dust-bunny cast | `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/` | 6 | Living mess, ambient helpers, reaction poses, cinematic inserts |
| Dirt and clutter targets | `assets/castle/dirty_cleanup_2d/targets/` | 18 | Hall and room-specific cleanup/sorting targets |
| Large mess vignettes | `assets/castle/dirty_cleanup_2d/targets/vignettes/` | 6 | Chandelier, banner, throne, pantry, craft table, toy chest |
| Cleaning and sorting tools | `assets/castle/dirty_cleanup_2d/tools/` | 12 | Tool choice, HUD cards, Sprite3D props, cinematic inserts |
| Cleanup and bunny effects | `assets/castle/dirty_cleanup_2d/effects/` | 12 | Pointer, progress, motion, friendship, target and section completion |
| Progress and reward badges | `assets/castle/dirty_cleanup_2d/progress/` | 6 | One/two/three-step feedback, tidy stack, bunny home/helper rewards |
| Cinematic | `assets/cinematics/dirty_castle/` | 12 | Opening discovery-to-victory sequence |
| Manifest | `assets/castle/dirty_cleanup_2d/manifest.json` | 1 | Exact paths, room reuse, sequence, voice intent, interaction contract |

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

| Frame | Beat | Character purpose |
| ---: | --- | --- |
| 01 | Roshan, Daddy, and Baby Eagle discover the gentle mess | Establish the problem without fear or blame |
| 02 | Dust bunnies hop out from shells and dusty corners | Turn “mess” into a cute, surprising part of Roshan's world |
| 03 | The family shares castle-specific tools | Make cooperation and each role instantly legible |
| 04 | Roshan guides bunnies toward a cozy shell-and-cloud home | Show care, sorting, and friendship instead of disposal |
| 05 | Roshan wipes the rainbow throne window | Child hero creates the first dramatic before/after |
| 06 | Daddy mops footprints and the floor scuff | Caring parent models work as play |
| 07 | Baby Eagle clears the high cobweb | Small helper gets a complete solo hero beat |
| 08 | Everyone cleans and restacks the pantry | Add a room-specific three-person teamwork scene |
| 09 | Family and bunnies sort the toy room | Make organization playful and visually countable |
| 10 | Family and bunnies tidy the royal library | Reuse book, shelf, pearl, and duster assets in a second room |
| 11 | The trio inspects the clean hall and bunny home | Confirm completion and give the bunnies a warm resolution |
| 12 | High-five in the fully clean Grand Hall | Family payoff and clear transition into play |

No frame uses captions or reading-dependent information. The manifest records a
short voice intention for each beat; implementation should route equivalent
recorded or existing voice through `_say()` rather than display text alone.

## Room-by-room reuse

### Grand Hall

- dust-bunny pile and character poses;
- corner cobweb, footprints, scuff, sticky spill, and window smudge;
- dusty chandelier, crooked banner, and smudged throne vignettes;
- mop, bucket, sponge, brush, broom, duster, bubbles, wipe, clean ring, and
  three-pearl progress.

### Toy Room

- blocks, tipped books, buttons/beads, cloud cushions, and messy toy chest;
- sorting basket, folded cloths, dusting mitt, tidy-stack badge;
- sibling, sleepy, hopping, and cloud-nest bunny poses.

### Royal Library

- tipped books, dusty shelf, cloudy window, loose pearl beads;
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

### Bath, loo, and bedrooms

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
- Rebuild with `python tools/process_dirty_castle_2d.py`.

## Review evidence

- `audit/dirty_castle_2d_2026-07-22/sprites_contact.png` shows all 60 runtime
  sprites against a checkerboard.
- `audit/dirty_castle_2d_2026-07-22/cinematic_contact.png` shows all 12
  normalized runtime frames in story order.
- The processor validates 512×512 RGBA output, nonempty alpha coverage, and
  transparent corners for every interactive sprite.
- The manifest enumerates all 60 sprites and all 12 cinematic frames.

These assets form a coherent implementation pack, but the gameplay section
itself remains unimplemented until a separate runtime change wires the
cinematic, interaction, voice, pointer, agency, and save contracts.
