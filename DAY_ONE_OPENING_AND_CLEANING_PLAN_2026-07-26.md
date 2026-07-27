# Day One: Arrival and Cleaning

## Locked player sequence

1. **Stage 1 - Flight cinematic.** On the first launch, play
   `assets/cinematics/opening/daddy_roshan_flight.ogv`: Daddy Mermaid and
   Mermaid Roshan fly to their new kingdom. A missing development edit uses
   the exact native 2048x1024 promenade master instead of a black screen. Tap
   skips; replay is always visible.
2. **Stage 2 - Arrival promenade.** Gameplay begins in the Sky Lagoon
   promenade. Its environment, objects, Roshan, and the first-arrival imp are
   unshaded Sprite3D cards at distinct depths. The imp runs toward the castle
   while cackling, and the beat saves when it finishes. Touch selection and
   walking both use camera rays.
3. **Stage 3 - Dirty-castle reveal.** Tapping the castle gate plays
   `assets/cinematics/dirty_castle/dirty_castle_reveal.ogv` once. The exact
   native 2048x1024 `day_one_dirty_castle_2048x1024.svg` master is the
   development fallback. Completion cuts to a full-screen Control cleaning
   minigame, not the retired 3D castle hall.
4. **Cleaning layer.** Seven rooms unlock in a fixed, child-readable order:
   Grand Hall, Playroom, Library, Royal Kitchen, Bubble Bath, Royal Loo, and
   Undercroft. One glowing target is active at a time. Three taps clean it,
   every tap answers immediately, and every completed object saves.

## Day-one production schedule

### Morning - establish the spine

- Lock both OGV filenames and the skip/replay behavior.
- Validate first-launch save migration with all new keys defaulting safely.
- Play the Stage 2 imp escape once and persist its completion.
- Gate the castle entrance through the Stage 3 reveal.
- Lock the two native 2048x1024 masters by SHA-256.

### Afternoon - prove the gameplay loop

- Finish the Grand Hall's three-target cleaning loop.
- Confirm the same data-driven loop loads every later room.
- Verify zero input never cleans anything.
- Verify a quit after any object keeps that object clean.
- Keep the developer look lab available in every display build for rapid
  tuning; its panel remains closed until the adult opens it.

## Non-negotiable acceptance checks

- Stage 2 world art is unshaded Sprite3D cards at real depth; it contains no
  MeshInstance3D or CanvasItem world art.
- Camera rays drive Stage 2 card selection and walking-plane navigation;
  nearest card depth determines occlusion selection.
- Cleaning is explicitly a non-navigable full-screen Control minigame. It has
  no Node3D child, physics body, light, or passive completion path.
- The only generated environment masters are exact native 2048x1024 SVGs;
  runtime loads those same files with no resize, pad, crop, or rewritten copy.
- No Blender, GLB, model, procedural mesh, Sprite2D, AnimatedSprite2D, or
  Polygon2D is introduced.
- The child cannot fail, choose a wrong tool, lose cleaning progress, or get
  trapped inside the castle.
- Every room objective has a voice cue and a pulsing visual pointer.
- Touch targets are at least 110 px on the 1280x720 design canvas.
- Opening, imp, castle reveal, and per-object cleaning state survive relaunch.
- The final OGV assets may be dropped in without a code change.
- Node inventory, dimensions, hashes, and invariance evidence live in
  `DAY_ONE_2D_RUNTIME_AUDIT_2026-07-26.md` and its JSON manifest.