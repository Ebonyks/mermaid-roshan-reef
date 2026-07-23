# Dirty Castle 2D Asset Pack

## Outcome

This pass establishes the complete visual vocabulary for the game's new opening:
Mermaid Roshan arrives at the Pearl Castle, discovers that it needs cleaning,
and works with Daddy Mermaid and Baby Eagle to make it shine.

The deliverable is intentionally asset-only. It does not change the current
startup flow, progression, save data, voices, or castle scripts. Runtime wiring
can therefore land as a separate mechanically tested change.

The pack contains:

- 6 child-friendly dirty-target sprites;
- 6 castle-specific cleaning-tool sprites;
- 6 opaque graphic cleanup-feedback sprites;
- 6 coherent 16:9 cinematic frames;
- one machine-readable reuse and sequencing manifest;
- preserved full-resolution generation masters, exact prompts, and QA sheets;
- a deterministic processing script for regenerating every runtime image.

## Pool decision

The pool was not included. At the generation baseline,
`origin/dev` was `6de38d15c7ecd58b61b4898201b74d5c1f926512`; it contained no
Roshan-pool feature file or pool callsite. The local
`codex/roshan-pool-pnw` worktree pointed at that same commit, so it had not
landed on `dev`.

This follows the owner's condition to include the pool only after it reaches
`dev`. The target/tool/effect families are modular, so a later pool-cleaning
beat can reuse the suds, sponge, mop, bubbles, swoosh, clean ring, and badge.

## Runtime art inventory

All interactive sprites are transparent 512×512 RGBA PNGs. Every asset has a
large silhouette, phone-readable value grouping, and enough transparent margin
for a pointer pulse or tap-scale tween.

| Family | Runtime location | Assets | Intended use |
| --- | --- | ---: | --- |
| Dirt targets | `assets/castle/dirty_cleanup_2d/targets/` | 6 | Grand Hall and room-specific cleanup targets |
| Cleaning tools | `assets/castle/dirty_cleanup_2d/tools/` | 6 | Tool choice, HUD cards, Sprite3D props, cinematic inserts |
| Feedback effects | `assets/castle/dirty_cleanup_2d/effects/` | 6 | Pointer, progress, target complete, section complete |
| Cinematic | `assets/cinematics/dirty_castle/` | 6 | Opening discovery-to-victory sequence |
| Manifest | `assets/castle/dirty_cleanup_2d/manifest.json` | 1 | Exact paths, roles, sequence, voice intent, interaction contract |

The cinematic frames are 1024×576 RGB PNGs. That is a native 16:9 composition
under the 1024px runtime texture limit and scales cleanly to the project's
1280×720 canvas.

## Story sequence

| Frame | Beat | Character purpose |
| ---: | --- | --- |
| 01 | Roshan, Daddy, and Baby Eagle discover the gentle mess | Establish problem without fear or blame |
| 02 | The family shares castle-specific tools | Make cooperation and each role instantly legible |
| 03 | Roshan wipes the rainbow throne window | Child hero creates the first dramatic before/after |
| 04 | Daddy mops footprints and the floor scuff | Caring parent models work as play |
| 05 | Baby Eagle brushes the cobweb and herds dust bunnies | Small helper gets a complete hero beat |
| 06 | High-five in the fully clean Grand Hall | Warm payoff and clear transition into play |

No frame uses captions or reading-dependent information. The manifest records a
short voice intention for each beat; implementation should route equivalent
recorded or existing voice through `_say()` rather than display text alone.

## Gameplay reuse plan

The sprites are not baked into one background. Each target can be placed as an
unshaded `Sprite3D`, a 2D overlay, or an `AtlasTexture`-style UI card:

- dust bunnies: Grand Hall, Royal Library, Toy Room, bedroom;
- cobweb: upper hall corners, library, undercroft;
- muddy footprints: entrance threshold, pantry, undercroft;
- floor scuff: hall, craft room, music room;
- sticky spill: hall, pantry, craft room;
- window smudge: throne rainbow, bedroom window, library window.

Recommended play loop for this four-year-old:

1. Show one large target at a time with the pulsing `fx_clean_ring`.
2. Speak the objective and point at the target.
3. Accept repeated taps or a very forgiving short swipe.
4. Show `fx_soap_bubbles` or `fx_soap_foam` on every successful input.
5. Dissolve the dirt, show `fx_gold_sparkle`, and save that target immediately.
6. After the last target, show `fx_all_clean_badge` and play the finale frame.

There is no timeout, penalty, health, wrong tool, or restart. Daddy and Baby
Eagle may animate beside the child, but they must not finish the section while
Roshan is idle.

## Visual and technical contract

- Current Pearl Castle geometry and palette are preserved: cream shell capitals,
  lavender stone, burgundy carpet, aqua, coral, restrained gold, and deep
  navy-purple contour.
- Dirt is playful and sparse. There is no mold, rot, garbage, insect, or
  frightening grime.
- Character generations use the existing protected art only as identity
  reference. No file under `assets/book/` or `assets/characters/friends/` was
  changed, recompressed, replaced, or moved.
- Baby Eagle keeps the turquoise, yellow, pink, black-gray, and large-eye
  identity of the book art, but the unrelated backpack is absent from the
  cleaning story.
- The runtime sprites use chroma-key removal with soft matte and despill, then a
  deterministic 512×512 crop. Cinematic masters use a centered 16:9 crop and
  1024×576 Lanczos resize.
- The pack adds no lights, particles, physics bodies, audio, or renderer-specific
  effect. All feedback can be implemented as one or two unshaded sprites.
- The exact prompt set and source-role labels live in
  `assets_src/concepts/dirty_castle_cleanup_2026-07-22/PROMPTS.md`.
- Rebuild with `python tools/process_dirty_castle_2d.py`.

## Review evidence

- `audit/dirty_castle_2d_2026-07-22/sprites_contact.png` shows all 18 runtime
  sprites against a checkerboard.
- `audit/dirty_castle_2d_2026-07-22/cinematic_contact.png` shows all six
  normalized runtime frames in order.
- The processor validates 512×512 RGBA output, nonempty alpha coverage, and
  transparent corners for every interactive sprite.

These assets are approved as a coherent implementation pack, but the gameplay
section itself remains unimplemented until a separate runtime change wires the
cinematic, interaction, voice, pointer, agency, and save contracts.
