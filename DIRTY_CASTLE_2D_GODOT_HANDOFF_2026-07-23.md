# Dirty Castle 2D Godot / Claude Handoff

## Scope and state

This is the implementation direction for the reusable dirty-object skins in
`assets/castle/dirty_cleanup_2d/`. The art pack is deliberately separate from
gameplay code so the opening, save flow, voice timing, and castle navigation can
be wired and probed in a focused follow-up.

The Royal Kitchen is not a new room. It is the existing basement kitchen built
in `CastleHall.build_basement_wing()` beside the Pantry. The Bubble Bath and
hidden Royal Loo are also existing basement rooms. Do not create duplicate room
geometry for this sequence.

`manifest.json` is the source of truth for resource paths. The current skin
library contains 96 transparent 512x512 runtime sprites, including 30
room-specific object skins and six room-level before-cleaning vignettes.

## Rendering contract

Use the PNGs as unshaded 2D skins inside the existing 3D castle. Do not relight
or color-grade them.

### Upright prop and clutter skins

- Use `Sprite3D`.
- Set `billboard = BaseMaterial3D.BILLBOARD_ENABLED`.
- Start with `pixel_size` in the `0.0045` to `0.0075` range and tune once on the
  1280x720 Mobile-renderer view.
- Place the sprite center above the floor so the visible silhouette, not the
  transparent 512x512 canvas, appears to rest on the surface.
- Keep depth testing on for ordinary clutter. Use a small position offset
  toward the room interior if a counter or wall causes z-fighting.
- Do not add an OmniLight. The painted highlights are already part of the skin.

### Flat floor or counter marks

- Use a `Sprite3D` with billboard disabled and rotate it onto the receiving
  surface, or use a single unshaded transparent `QuadMesh`.
- Suitable assets include spills, footprint trails, scuffs, flour, water
  droplets, and dust trails.
- Keep the quad 1-2 cm above the receiving surface in world scale to avoid
  z-fighting on the Mobile renderer.
- Never set `no_depth_test` for room grime; it must not draw through furniture
  or walls.

### Fixture-specific skins

- Use a non-billboard `Sprite3D` facing the normal room camera direction when
  the illustration includes the fixture itself, such as the kitchen sink,
  stove, bath, vanity, or Royal Loo.
- Treat these as temporary dirty-state overlays. Fade or scale them away when
  cleaned and reveal the existing 3D fixture beneath.
- The skin must not replace, hide permanently, or duplicate the interactive
  fixture node.

### Effects and UI

- `effects/fx_clean_ring.png` is the visual pointer around the current target.
- Bubbles, wipe swooshes, dust-bunny motion, and sparkles may use billboard
  sprites with a short tween, but cap the active feedback layers at two on
  Speedy tier.
- Progress shells are non-reading feedback. They can be CanvasLayer sprites or
  billboard reward cards.
- Import filtering should remain linear, repeat disabled, and mipmaps enabled
  only where a Sprite3D materially shrinks in the scene.

## Existing-room anchors

All positions below are relative to the `o` origin already passed through
`CastleHall`; preserve that convention.

| Section | Existing code anchor | Existing center / fixture vocabulary |
| --- | --- | --- |
| Royal Library | `build_expansion()` left-wing gallery | shelves near `o + (-51, 33.5, z)`, reading table near `o + (-44, 34, 2)` |
| Playroom | `build_expansion()` right-wing gallery | rug near `o + (44, 33.9, 2)`, toys around `o + (40..49, 34, -20..8)` |
| Undercroft | `build_expansion()` | floor near y `-18`, storage across z `31..39` |
| Royal Kitchen | `build_basement_wing()` | room center `o + (17, 0, -2)`; existing counter, sink, stove, table |
| Bubble Bath | `build_basement_wing()` | room center `o + (-17, 0, -28)`; existing tub, vanity, towels |
| Royal Loo | `build_basement_wing()` | hidden room center `o + (-30.25, 0, -28)`; existing `build_toilet()` |

Do not place skins into the hall corridors or doors in a way that narrows the
child's route. Visual skins need no physics body.

## Room skin assignments

### Playroom

Use all six files under `rooms/playroom/`. Put puzzle tiles and the wheeled
shell toy on the play rug; place stacking rings and the tea set near the
existing toy-chest/stacker cluster; put the dress-up pile and balls/beanbag at
the rug edge. The action is sorting and putting away, not scrubbing.

### Royal Library

Use all six files under `rooms/library/`. Fallen books and picture cards belong
on the floor/table; bookmark ribbons and scrolls can sit near the low shelves;
the book cart and reading cushions should remain large, obvious touch targets.
Book covers must stay icon-only with no reading requirement.

### Royal Kitchen

Use all six files under `rooms/royal_kitchen/` on the existing basement
fixtures. The sink/plates skin belongs over the existing sink, the flour skin
over the counter, and the stove-drips skin in front of the existing rounded
stove. Cups, pan, and cabinet-jars are sorting targets. Keep the stove visually
cool during cleaning and do not imply the child handles heat.

### Bubble Bath

Use all six files under `rooms/bubble_bath/`. The bath, mirror, and vanity
skins overlay their matching existing fixtures; towels and toy basket are
sorting targets; the water-droplet trail lies on the floor. The room is soapy
and splashy, never gross.

### Royal Loo and undercroft

Use the first four files under `rooms/basement/` only inside the hidden Royal
Loo. The soap-ring and water marks are clean bathroom mess with no waste. Use
the final two files in the existing undercroft storage/stair area.

### Room vignettes

The six files under `targets/room_vignettes/` are section-intro cards or broad
room overlays. Do not display a full-room vignette at the same time as every
individual object skin. Suggested use: show the vignette during the voiced room
introduction, dissolve it, then reveal three large individual targets.

## Forgiving interaction recipe

1. Enter a room and speak the objective through the existing `_say()` path.
2. Show the room vignette briefly, then pulse one individual skin with
   `fx_clean_ring`.
3. Give each target an invisible touch radius at least as large as the visible
   sprite and never smaller than the project's established 3.5-world-unit
   castle touch zones.
4. Accept repeated taps or any short swipe crossing the target. Tool choice is
   expressive only; there is no wrong tool.
5. On every accepted input, show immediate bubbles, a wipe, or a friendly
   dust-bunny reaction.
6. After two or three inputs, tween the dirty skin out, show a sparkle, and save
   the target state immediately.
7. Do not let Daddy Mermaid, Baby Eagle, or an ambient timer complete a target
   while Roshan is idle. Their actions support the child; they do not take
   agency away.
8. Award one, two, then three pearl progress marks and finish the room with a
   voiced celebration. There is no timeout, fail state, or lost progress.

## Save and probe direction

- Add new save keys with defaults; never remove or rename existing keys.
- Save after every completed object, not only at the end of a room.
- A load probe must restore the exact room and completed-target set.
- The passive probe must confirm that no target or room completes without
  input.
- The active probe should cover at least one tap target, one swipe target, a
  room completion, a save/reload, and the final 36-frame story transition.
- Run `scripts/ci.sh` (or the exact-head CI equivalent) before integration.
