# Day One: Arrival and Cleaning

## Locked player sequence

1. **Stage 1 - Flight cinematic.** On the first launch, play
   `assets/cinematics/opening/daddy_roshan_flight.ogv`: Daddy Mermaid and
   Mermaid Roshan fly to their new kingdom. A missing development edit uses a
   neutral black fallback, not a stretched background plate. Tap skips; replay
   remains available.
2. **Stage 2 - Arrival promenade.** Gameplay begins in the Sky Lagoon
   promenade. Its approved 2172x724 panorama is preserved at its exact 3:1
   ratio. Three lossless 724x724 crops reconstruct it as adjacent unshaded
   Sprite3D cards at z=-18. Objects, Roshan, and the first-arrival imp remain
   separate unshaded Sprite3D cards at audited depths. Touch selection and
   walking both use camera rays.
3. **Stage 3 - Dirty-castle reveal.** Tapping the castle gate plays
   `assets/cinematics/dirty_castle/dirty_castle_reveal.ogv` once. Until a
   compliant approved-ratio >=2K plate exists, a missing edit uses neutral
   black rather than altered art. Completion cuts to a full-screen Control
   cleaning minigame, not the retired 3D castle hall.
4. **Cleaning layer.** Seven rooms unlock in a fixed, child-readable order:
   Grand Hall, Playroom, Library, Royal Kitchen, Bubble Bath, Royal Loo, and
   Undercroft. One glowing target is active at a time. Three taps clean it,
   every tap answers immediately, and every completed object saves. The UI
   uses code-native room colors behind its transparent cutouts; no generated
   castle background plate is loaded.

## Day-one production schedule

### Morning - establish the spine

- Lock both OGV filenames and the skip/replay behavior.
- Validate first-launch save migration with all new keys defaulting safely.
- Play the Stage 2 imp escape once and persist its completion.
- Gate the castle entrance through the Stage 3 reveal.
- Lock native master, runtime tile rectangles, and hashes.

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
- The 2172x724 master retains the exact approved 3:1 composition. It is never
  imported as one oversized runtime texture.
- Three non-overlapping 724x724 crops reconstruct all 2172 source columns at
  one coherent depth, with no resize, crop loss, padding, or canvas extension.
- Camera rays drive Stage 2 card selection and walking-plane navigation;
  nearest card depth determines occlusion selection.
- Cleaning is explicitly a non-navigable full-screen Control minigame. It has
  no Node3D child, physics body, light, passive completion path, or generated
  background plate.
- Generated background masters must retain approved source ratio and have a
  native long edge >=2048. Noncompliant outputs stay rejected and outside the
  repository; no upscaling or CLI/API fallback is permitted.
- No Blender, GLB, model, procedural mesh, Sprite2D, AnimatedSprite2D, or
  Polygon2D is introduced.
- The child cannot fail, choose a wrong tool, lose cleaning progress, or get
  trapped inside the castle.
- Every room objective has a voice cue and a pulsing visual pointer.
- Opening, imp, castle reveal, and per-object cleaning state survive relaunch.
- Node inventory, dimensions, ratios, hashes, tile rectangles, invariance, and
  seam evidence live in `DAY_ONE_2D_RUNTIME_AUDIT_2026-07-26.md` and
  `audit/day_one_background_ratio_2026-07-27/`.
