# Claude handoff — Opera job 2.5D story worlds

Date: 2026-07-24

## Binding design correction

The twelve regular Opera jobs are not performances confined to twelve literal
stages. Each job is a short, highly readable 2.5D side-scrolling story world
entered through its career door in the Opera lobby.

The correct spatial language is:

```text
small entry portal -> traversable job district -> mechanic clearings ->
large scenic landmark -> completion overlook -> return to lobby
```

Curtains, footlights, painted flats, and theatrical transitions may connect
the Opera to each world. They must not enclose every job on one proscenium
deck.

Reserve literal Opera stages for the later boss-fight phase:

- Curtain Dragon;
- Shadow Phantom;
- Midnight Maestro.

This reserves those spaces; it does not authorize boss asset work now.

This file supersedes the "shared show-room shell", "job stage package", and
"small theatrical environment" spatial language in
`CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md`. The older guide remains
useful for outfits, mechanic-critical implements, state names, touch targets,
continuity locks, and performance budgets.

## Repository-visible visual sources

| Purpose | Path |
| --- | --- |
| 2.5D world panoramas and environment kits | `assets_src/concepts/opera_jobs_2p5d_2026-07-24/` |
| Generation prompts and provenance | `assets_src/concepts/opera_jobs_2p5d_2026-07-24/PROMPTS.md` |
| 24-asset environment ledger | `audit/opera_job_2p5d_environment_ledger_2026-07-24.csv` |
| Combined environment contact sheet | `audit/opera_job_2p5d_contact_sheet_2026-07-24.png` |
| Environment 4.5/5 audit | `OPERA_JOB_2P5D_ART_AUDIT_2026-07-24.md` |
| Accepted outfit, implement, and state cards | `assets_src/concepts/opera_jobs_flat_2026-07-21/` |
| Exact older card manifest | `audit/opera_job_flat_prototype_ledger_2026-07-21.csv` |

Every job has one `1024 x 576` environment panorama and one `1024 x 1024`
sixteen-cell environment kit. The new environment art controls world layout.
The older stage/state sheets control mechanic state, guidance, retry, reveal,
and completion timing only. Do not reconstruct their proscenium compositions
as the whole level.

## Shared 2.5D construction contract

### Player and camera

- Roshan moves left and right on one dominant gameplay plane.
- Use shallow Z only for readable interaction bays and overlap avoidance.
- Keep the camera mostly side-on with gentle three-quarter presentation.
- Use stable orthographic or long-lens perspective; avoid wide-angle
  distortion and camera rotation during touch interactions.
- A landmark enters view before its interaction becomes active.
- Keep Roshan, the active target, and the next route cue visible together.
- Preserve a broad, uncluttered strip around the touch plane.

### Required world depth

1. **Foreground dressing** — sparse shells, coral, ropes, planters, and soft
   occluders that never cover Roshan or targets.
2. **Playable midground** — continuous collision route, large implements,
   interaction clearings, bridges, ramps, and completion space.
3. **Scenic midground** — rounded facades and landmarks with simplified or no
   collision.
4. **Far parallax** — low-contrast city, landscape, sky, water, or district
   silhouettes.
5. **Atmosphere** — very sparse bubbles, dust, or light ribbons on Speedy.

Parallax must remain slow and must not compete with the playable plane.

### Entry, exit, and theatre language

- One small shell-and-curtain portal may mark the far-left entrance.
- A completion overlook, garden, plaza, or reveal space marks the far-right
  destination.
- A curtain wipe can transition between lobby and world.
- Do not wrap a regular job in a proscenium, audience, orchestra pit, or
  visible stage deck.
- Do not place a second literal stage at the destination.

### Large modules, textures, and backgrounds

Build reusable modules rather than one fused environment mesh:

- straight floor sections, shallow ramps, short bridges, and low guardrails;
- one entry portal, two to five job landmarks, and one completion module;
- a small family of planters, lamps, posts, and route trims;
- separate scenic-mid and far-background bands.

Treat the texture-kit cells as design references. Rebuild them as small
tileable albedos, flat toon materials, decals/trim atlases, or camera-facing
background bands as appropriate.

- Maximum 1024px longest side unless power-of-two.
- No realistic normal noise, dirt, grunge, or photographic roughness.
- Preserve navy-purple separation and aqua/lavender shadows.
- Reduce contrast and saturation with depth.
- No text, letters, numbers, or logos in signs or trims.
- Use alpha sparingly because transparent overdraw is expensive.
- Prefer two or three repeatable background bands over one giant unique map.
- Hide background seams behind towers, coral, bridges, or light changes.

Primary landmarks need rounded, phone-readable silhouettes and broad material
regions. Brass, pearl, rope, and shell details remain accents.

## Per-job world plans

### Floor 1

#### Pastry Chef — pastry district

Frosting-tile promenade -> giant mixing bowl -> oven bridge -> layered-cake
lift/rack -> cake-reveal destination. Keep hot surfaces friendly and separated
from the route. Use cream frosting, coral wood, teal tile, plum fabric, and
brass/frosting guidance trim.

#### Detective — moonlit archive district

Archive promenade -> clue alcoves -> magnifier tower -> bookcase/drawer
passage -> chest vault. Keep clues on the playable plane and backgrounds
quieter; never hide required clues in decorative clutter.

#### Ballerina — rhythm garden

Shell-tile garden -> music-box pavilion -> mirror promenade -> rhythm
causeway -> twirl overlook. Preserve the exact pairs: coral shell, teal wave,
plum ribbon, cream pearl. Use stylized aqua reflections, not real-time mirror
surfaces.

#### Candy Maker — candy works

Ingredient hopper -> press/gauge -> conveyor causeway -> wrapper village ->
display-cart destination. Keep candy silhouettes distinct. Conveyors are
shallow route elements, never physics-driven bodies.

### Floor 2

#### Doctor — care garden

One patient arrival bay -> stethoscope pavilion -> bubble fountain ->
thermometer garden -> five-heart alcoves -> bandage bridge -> recovery garden.
Only the same coral five-armed starfish plush is the patient. Later stations
stay empty so the runtime patient can move through the sequence.

#### Farmer — meadow and orchard

Flower meadow -> orchard -> barn -> hay stairs -> safe mud lane -> picnic
clearing. The clearing has exactly nine empty piggy pads. Piggies and the five
food baskets are runtime objects; never bake them into scenery. Retain the
tested 2D timing mechanic.

#### Boxer — friendly training district

Padded promenade -> focus-mitt tunnel -> soft hanging bags -> exactly three
practice pads -> cushion bridge -> bell tower -> belt-victory plaza. The tone
is exercise and confidence, not injury. Training imps remain friendly runtime
actors. Do not add a boxing ring or audience.

#### Magician — twilight illusion boulevard

Exactly three giant hats in plum/teal/coral order -> mirror bridge/gate ->
harmless cabinet passage -> paired coral/teal swap trail -> empty moonlit
reveal lagoon. The bunny-fish remains a runtime reveal actor. Avoid
playing-card suits and copied magic-franchise symbols.

### Floor 3

#### Painter — sunrise pigment district

Exactly three paint stations in plum/coral/cream order -> paint-stream ramp ->
canvas bridge -> rinse creek -> splat garden -> gallery overlook. Plum first,
coral second, cream third is binding in environment, guidance, interaction,
and recap.

#### Astronaut Engineer — bubble spaceport

Straight/elbow/ring pipe matching and sockets -> valve tower -> zero-gravity
bubble garden -> bubble-tank causeway -> rocket overlook. Keep all three
shapes distinct. Rocket propulsion is bubbles only: no flame or smoke. Do not
use real-world space-agency marks.

#### Racecar Driver — Opera racetrack city

Pit-lane workshop -> broad straight -> safe banked curve -> bubble-boost track
bridge -> empty grandstand -> finish plaza. The live kart retains its open
mermaid-tail-safe channel and bubble exhaust. Use high rounded guardrails; no
brands, numbers, flame, or smoke.

#### Pop Star — rhythm-light district

Microphone promenade -> exactly four direction tiles -> speaker rooftops ->
rainbow bridge -> illuminated city catwalk -> encore overlook. Mapping is
plum-left, teal-up, cream-down, coral-right. The catwalk is a traversable city
street, not a stage. Retain the live `DanceEngine`.

## Lobby and future boss stages

The lobby remains the primary navigation set. Four career doors belong to
each floor; upper floors stay visibly desirable but physically locked until
progression unlocks them.

The lobby may foreshadow three larger formal stage entrances. Until the boss
phase begins:

- keep them closed or inaccessible;
- do not create boss silhouettes, props, attacks, or hazards;
- do not reuse a boss stage as a regular job world;
- do not move regular mechanics onto those stages.

## Blender and Godot implementation

Suggested collection structure:

```text
OPERA_<JOB>_WORLD
  GEO_Playable
  GEO_Landmarks
  GEO_Scenic
  GEO_Foreground
  BG_Mid
  BG_Far
  FX_ReferenceOnly
  COLLISION
  ANCHORS
```

Required anchors:

```text
Anchor_Entry
Anchor_PlayerStart
Anchor_CameraStart
Anchor_Interaction_01...
Anchor_Completion
Anchor_Exit
```

Use one static collision strip for most traversal, simple boxes/capsules/ramps,
and separate nodes with stable pivots for interactive objects. Do not create
rigid-body foliage, conveyors, or background pieces. Use named
visibility/material states instead of duplicate full sets. Foreground
occluders need a Speedy cull path.

Review every world in the Mobile renderer at the actual 1280 x 720 gameplay
camera and at phone-thumbnail size. Preserve existing logic and save keys
unless a separate implementation task explicitly changes them.

Complete one Pastry Chef vertical slice before mass modeling:

1. full route blockout with depth layers;
2. Roshan-scale gameplay-camera test;
3. one live mechanic clearing;
4. entry and completion transition;
5. Speedy-tier profiling;
6. owner review;
7. propagation of the accepted construction language.

## Acceptance gate

Each world must demonstrate:

- continuous left-to-right traversal, not one stage deck;
- readable foreground, playable midground, scenic midground, and far
  background;
- at least three large job-specific landmarks;
- exact continuity counts, orders, species, and states;
- no boss content;
- clear entry and completion destinations;
- phone-readable touch targets and nonverbal guidance;
- no fail state or reading-dependent objective;
- Mobile-renderer evidence and 30 fps Speedy viability;
- license and provenance entries for every new asset.

If a world reads as "props arranged on a theatre stage", it fails this handoff
even when the individual props are attractive.
