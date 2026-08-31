# Fairy Conservatory — early Chapter 3 route

Status: `LOCATION_DECIDED`, `FAIRY_POND_ART_CORRECTED`,
`RUNTIME_IMPLEMENTED`, `LOCAL_VISUAL_PASS`, `SOL_VISUAL_PASS`; exact Godot
4.7.2 CI, target-device, child, owner, and release acceptance remain pending.
The current Sol pass covers the six-panel Lily-Pad Fairy World correction; the
earlier pass on the owner-rejected Sky Lagoon version remains superseded.

## Decision

The dormant wall relief in Pearl Castle's Main Hall opens onto the **Rainbow
Skyway**, a short walkable sky stage. The physical **Butterfly House** is
visible at the far end. Crossing the causeway and touching the house enters
the existing Butterfly World rescue. Its Fairy Fountain remains the route to
the Fairy Pond flower-bloom mission.

This replaces the earlier direct-door concept. The open castle door must not
show the Butterfly greenhouse or Fairy Pond immediately: that collapses three
places into one and makes the doorway perspective impossible. The final graph
is:

```text
Castle Main Hall
  → open Moonflower doorway
    → Rainbow Skyway walk-through
      → Butterfly House landmark
        → Butterfly World: rescue seven baby butterflies
          → Fairy Fountain
            → Fairy Pond: bloom the Fairy Flower
              → Butterfly World
                → Rainbow Skyway
                  → exact Castle Main Hall context
```

The route gives the fairies a believable hidden address inside the castle's
story geography while preserving the sense that Butterfly World is a separate
place reached through the sky.

## Progression and reveal authority

The intended story cause remains the Rainbow Candle: its light answers a
wing-chime in the Main Hall and wakes the moonflower relief. This branch does
not yet contain a persisted Rainbow Candle field, so runtime must not invent or
silently overload one. The current safe reveal gate is `opera_done`, the
earliest stable completion authority already present for the Chapter 2 castle
material. When the Candle director lands, it can replace that derived reveal
cause without changing the three additive Chapter 3 save keys.

On the first eligible return to Main Hall:

1. The dormant relief gives one restrained rainbow pulse.
2. A voiced line says, "The castle found a secret sky door!"
3. One large animated pointer identifies the central pearl/threshold.
4. A tap opens the petals permanently and saves immediately.

Before reveal, the relief is scenery only: no hotspot, pointer, locked label,
or false touch feedback. The child never needs to read.

Legacy saves with `galaxy`, `bwdone`, or `fairyskin` already established are
grandfathered to revealed and open. Existing access is never removed.

## Main Hall location and connectivity

The accepted Main Hall is a 3344×941 logical panorama. Its A/B screen join is
at `x = 1672`. The unused interval between Opera Hall and the Playroom is 765
logical pixels wide and contains no room entrance.

Use one whole `Sprite2D` card centered near `(1672, 385)`, with a 470-pixel
visual height and approach foot `(1672, 620)`. It spans the background join as
one object and is horizontally culled as one object; it must never be split or
independently regenerated into the hall tiles. The nearby standalone sconce at
about `x = 1476` is hidden while the doorway card owns the bay.

The doorway is a dedicated Chapter 3 route, not a fake castle room in
`HALL_PORTALS`. Its callback suspends Castle Main Hall and stores a return
context. Returning from Butterfly World must restore `main_hall` and the prior
hall camera offset; it must never fall through to Sky Lagoon promenade
reconstruction.

The old visible `court:galaxy` and first Rainbow Race direct handoffs are
compatibility entry points only. When invoked, they should enter this handoff
route rather than visibly bypassing the Rainbow Skyway and Butterfly House.

## Doorway before/after assets

### Dormant relief

- `assets/flats/castle/fairy_conservatory/moonflower_door_closed.png`
- Closed lavender petals, shell crown, pale-gold trim, and one central pearl.
- Warm castle ambient color only; no destination, character, particle, or
  glow.
- 1024×1024 RGBA, normalized as a whole card with transparent corners.

### Open sky route

- `assets/flats/castle/fairy_conservatory/moonflower_door_open.png`
- Same architectural shell and pivot; leaves hinge nearly edge-on.
- One crown pearl only. Bridge posts may carry their own architectural pearls,
  but there are no duplicate door handles or pearls mirrored on the door
  leaves.
- Eye-level Fairy Pond composition. The authored destination line is at
  `y = 389 / 1024` (38.0%), safely above the 50% maximum.
- The Rainbow Skyway converges on the Butterfly House at the horizon. No lily
  pad climbs into the sky, no top-down pond is mounted in the doorway, and the
  hall does not open directly into Butterfly World.
- The rainbow artwork overdraws 28 pixels behind the sill and is clipped at
  `y = 965`, the exact base of the architectural opening. Walkway alpha covers
  the complete opening width for rows 959–965, so no grass strip, water strip,
  matte, or empty band separates the stage from the threshold.

The shell-frame source is project-original built-in ImageGen art. Its obsolete
generated garden is fully removed by a deterministic opening mask. The view
uses the corrected upright Fairy Pond master, bound to the approved Lily-Pad
Fairy World art, plus the selected Chapter 3 walkway and Butterfly House
whole-sprite cutouts. Exact hashes and roles are recorded in the two source
manifests.

## Rainbow Skyway stage evaluation

The Rainbow Skyway is a transition stage, not another career or score screen.
Its job is to make the castle-to-fairy-world distance tangible in less than a
minute.

### Accepted interaction

- True 2D only: `CanvasLayer`, `Control`, `Node2D`, `Sprite2D`, and 2D input.
- Full 1280×720 composition using a continuous 3640×2048 upright Fairy Pond
  master, sliced into a non-overlapping 4×2 grid for runtime.
- The house stays visible at the vanishing point throughout; it is not revealed
  by a screen swap.
- Roshan advances from the broad foreground toward the centered horizon using
  three large, sequential one-finger targets. Exploratory taps do nothing
  harmful. Zero input cannot complete the route.
- No timer, score, penalty, health, fall, reset, or fail state.
- At the final point, one large Butterfly House hotspot becomes active. A tap
  starts the rescue. Back returns to the exact Main Hall context.
- Voice and animated pointer carry every objective without reading.

This deliberately does not reuse Opera `MelodyGame` or turn the route into a
new rhythm requirement. The existing Rainbow Stage song remains optional
castle play. Requiring a scored dance before the fairy rescue would lengthen
the handoff and compete with the actual mission.

### Stage art

- Background: one continuous eye-level Fairy Pond master guided by the
  approved V5 lily-pad panorama and V2 pond foliage/water plates. The full
  3640×2048 canvas is assembled from six independently generated 1254×1254
  panels at exact 1:1 scale. Their joins cross open sky or water only; top
  horizons are losslessly aligned, and broad low-frequency palette matching
  prevents a visible plate transition without moving or redrawing any painted
  form. No source image is enlarged. The master is then sliced into eight
  910×1024 cards; no runtime tile is generated independently. Sky Lagoon
  mountains, cabins, grass, and promenade imagery are excluded.
- `assets/flats/fairy_conservatory_handoff/rainbow_walkway.png`: one-point
  causeway in the established coral, peach, yellow, mint, aqua, and lavender
  order, with Pearl Castle shell/gold/lavender rails.
- `assets/flats/fairy_conservatory_handoff/butterfly_house.png`: a large
  butterfly-shaped stained-glass conservatory with a broad central entrance,
  readable purple contour, aqua glass, shell/gold trim, and restrained lily
  planters.

The house is both stage landmark and item: it supplies the visible destination,
the final oversized hit target, and the physical threshold into Butterfly
World. It is not a loose portal ring, menu tile, or label.

## Existing Butterfly World minigame evaluation

The current seven-baby rescue has the right preschool mission grammar:

- seven readable butterfly targets and persistent `_bwd_butterfly_%d` sticker
  keys;
- forgiving collection with no permanent failure;
- a clear Fairy Fountain escalation after rescue;
- one-time completion/reward protection through `bwdone`, `fairyskin`, and the
  existing pearl reward;
- replay safety and legacy-save continuity.

Its largest flaw is connectivity: direct Sky Lagoon/Rainbow Race entry makes
it feel detached from the castle and makes the fairies seem incidental. The
Rainbow Skyway/Butterfly House handoff fixes that narrative problem while
leaving authoritative butterfly progress and rewards intact.

The current Butterfly World renderer in `scripts/galaxy.gd` remains measured
3D migration debt (`Node3D`, meshes, lights, `Camera3D`, and `Sprite3D`). The
current Fairy Pond presentation in `scripts/games/fairy.gd` is the same. This
route adds no new 3D file or node and must not copy their implementation into
the new stage. A later mechanical conversion must preserve quest behavior
while replacing those presentations with true-2D Canvas art. The obsolete
`probe_fairy_art.gd` Sprite3D expectations are not acceptance evidence for the
new route.

## Fairy Pond evaluation

The flight/bloom mechanics are child-appropriate: slow pacing, forgiving hit
zones, clear helpful-versus-danger color language, auto-fire, auto-shield,
retry kindness, voice beats, and no hard fail. The seed→sprout→bud→opening→
bloom sequence gives the first Chapter 3 mission a visible climax.

The missing production requirements are presentation conversion and finer
checkpointing. Until converted, the eventual `flower` sticker, `bwdone`,
`fairyskin`, pearl reward, and return symmetry remain authoritative; the route
must not reset or repurpose them.

## Save compatibility

Add only:

- `chapter3_fairy_door_revealed`
- `chapter3_fairy_door_opened`
- `chapter3_fairy_mission_started`

Each transition saves immediately. Continue using `galaxy`, `bwdone`,
`fairyskin`, and `_bwd_butterfly_%d` for their existing meanings. Grandfather
legacy access from any of the three legacy booleans. Leaving at any point keeps
the door open and preserves collected babies.

## Blocking acceptance gates

- Fresh save before reveal: one closed relief card, no hotspot, no cue, no save
  mutation.
- Eligible reveal: exactly one voice cue, pointer, card, and child-sized target.
- Open: idempotent, immediately saved, same logical pivot/visual height as
  closed, stable across the Main Hall seam.
- Rainbow stage: continuous background seams; house visible throughout; three
  ordered touch targets; zero-input non-progression; no failure path.
- House: minimum 112×112 logical hotspot and correct mission-start save.
- Return: Galaxy quit/completion restores Rainbow Skyway/Main Hall context, not
  Sky Lagoon promenade. Fountain→Fairy Pond→Galaxy symmetry remains intact.
- Save/load: all new fields round-trip; `galaxy`, `bwdone`, and `fairyskin`
  grandfather access.
- Art: every runtime image is at most 1024 pixels on its longest side; the
  background has at least 2048×2048 native coverage per playable screen;
  transparent corners and source hashes pass; no protected original changes.
- Medium: new route contains no `Node3D`, `Sprite3D`, 3D camera/light/mesh,
  spatial material, `Vector3`, or `Transform3D`.
- Final visual approval: independent Sol review of the in-context door and
  1280×720 stage composition confirms perspective, scale hierarchy,
  child-readable target, approved rainbow/fairy language, and the larger
  castle→skyway→house→fairy-world vision. Any failed visual is rebuilt or
  regenerated only at the documented gap before acceptance.
