# Fable handoff — room-led Castle visual polish intervention

**Date:** 2026-07-28  
**Scope:** current two-screen Pearl Castle Main Hall  
**Decision:** retain the two-screen hub, door order, double-width Opera
entrance, far-left courtyard exit, far-right Huluu throne, and omnipresent
Storybook elevator. Replace the hall's visual hierarchy, not its topology.

## Reference authority

The Castle's own finished rooms are now the primary art-direction source:

1. Royal Kitchen
2. Royal Library
3. Stuffie Playroom
4. Craft Room
5. Mermaid Pool
6. Bubble Bath
7. Opera Hall

Sky Lagoon and the Northern promenade are secondary references only. They
demonstrate successful depth staging, clustered detail, landmark rhythm, and
environmental progression. They must not donate their palette, vegetation,
architecture, or props to the Castle.

The current Main Hall Screen A and Screen B proofs remain authoritative for
layout and accessibility. They are rejected as final visual-polish targets.
Their evenly spaced wishing-star/fountain/chime foreground row is also
rejected. It proves hit-size and clearance, but reads as pickups placed on a
flat floor instead of a lived-in castle.

## Diagnosis

The quality loss is not primarily caused by texture resolution. Sharper
versions of the current wall would preserve the same problems.

| Dimension | Successful Castle rooms | Current Main Hall | Required correction |
|---|---|---|---|
| Materials | Five to seven coordinated materials per view: shell cream, lavender/amethyst stone, aqua glass/water, coral pink, teal cabinetry, muted gold, deep plum | Lavender brick and white columns dominate nearly the whole frame | Create broad material zones and reserve brick as one supporting surface |
| Architecture | Scalloped arches, shell coves, built-in shelves, window bays, niches, curved counters, coral framing | Repeated identical column-and-door module | Alternate three coherent bay types while keeping every door in place |
| Value | Dark plum anchors frame luminous aqua and warm gold focal areas | Most walls, floor, and doors sit in one light mid-violet range | Add dark recesses and bright window/niche focal zones |
| Depth | Far windows/reef, middle furniture or pool, near tables/coral/soft seating | One frontal wall plus one line of floor objects | Stage far architecture, middle fixtures, player lane, and near interaction clusters at real Z |
| Density | Objects form readable activity islands with breathing space | Large bare surfaces plus isolated sticker-like objects | Use two or three clustered activity islands per screen |
| Silhouette | Large shell/coral/furniture masses are readable to a preschooler | Thin lamps, small logos, narrow columns, repeated arches | Use fewer, larger, rounder castle-native masses |
| Story | Each room communicates its purpose immediately | The hub communicates only “corridor” | Make Screen A ceremonial and Screen B familial/royal without borrowing destination-room furniture |

The machine audit supports the visual reading without pretending to replace
human review. Mean saturation is close (`0.2792` for the six room references
versus `0.2658` for the hall), so a global saturation boost is not the answer.
The room references have higher luminance entropy (`7.1723` bits versus
`6.6378`), while the hall actually has the wider raw 10th-to-90th percentile
luminance span because of its dark carpet, bright HUD, and yellow stars. The
problem is organized variety and focal distribution, not a missing contrast
slider.

## The intervention

### Shared architecture grammar

Both screens use the same continuous red carpet, floor baseline, cornice,
column scale, pixels-per-meter, and lavender shell-stone structure. Between
the existing doors, alternate these castle-native bay types:

- **Aqua window bay:** a tall shell-framed window derived from the Kitchen,
  Pool, and Bath window grammar. It is a far-depth light source, not a pasted
  room picture.
- **Pearl display niche:** a deep plum scalloped recess derived from the
  Library focal alcove and Playroom stuffie nook. It holds one neutral
  Main-Hall object group.
- **Textile light bay:** layered drape, chandelier, and shell-sconce rhythm
  derived from Opera and Craft. Banners use the approved open-shell and three
  aqua-wave mark only.

Brick remains visible between these bays, but it no longer fills every
negative space. Shell cream, teal/aqua, coral, muted gold, and deep plum are
distributed in large masses before any small decoration is added.

### Screen A — ceremonial gallery

- Preserve the courtyard opening at far left.
- Preserve the double-width Opera opening and its masks.
- Preserve the Library and Kitchen door positions and protected approaches.
- Give Opera the strongest ceiling/drape treatment and deepest corridor cap.
- Put one aqua window bay near the exterior side and one pearl display niche
  between destinations where it does not narrow an approach.
- Replace the row of stars with two asymmetric activity islands:
  a shell-fountain/dust-bunny cluster and a soft pearl-seating/sparkle cluster.
- Keep the middle of the carpet and each threshold visually quiet.

### Screen B — family and throne gallery

- Preserve all four door positions and protected approaches.
- Preserve the existing throne art and its far-right stair exactly.
- Use warmer coral/teal accents than Screen A while keeping the same shell
  architecture.
- Increase visual emphasis gradually toward the throne with one stronger
  window/niche and a richer canopy transition; do not change the throne.
- Use two asymmetric foreground islands: a gentle dust-bunny play cluster and
  a shell-percussion/bubble cluster. Neither may project across a door landing
  or the elevator HUD.
- Leave a calm visual buffer around the throne stair so it remains the final
  landmark.

### Foreground use

The bottom third is a playable near-depth apron, not an inventory shelf.
Objects appear in groups of two to four with overlapping contact shadows,
shared response effects, and a clear relationship:

- fountain + bubbles + peeking dust bunny;
- cloud pouf/settee + sleepy dust bunny + sparkle;
- shell drum/chime + two response notes/bubbles;
- pearl floor motif + hopping dust bunny trail.

Each island supplies one large primary touch target and optional secondary
reactions. The islands are separated by open swim/walk space. No repeated
star row, equally spaced pickups, destination-room furniture, text label, or
entrance obstruction is allowed.

## Reuse inventory

### Approved and already in the active Castle branch

- `assets/flats/castle/rooms/room_kitchen.png`
- `assets/flats/castle/rooms/room_library.png`
- `assets/flats/castle/rooms/room_playroom.png`
- `assets/flats/castle/rooms/room_craft_room.png`
- `assets/flats/castle/rooms/room_mermaid_pool.png`
- `assets/flats/castle/rooms/room_bubble_bath.png`
- `assets/flats/castle/rooms/room_opera_hall.png`
- all corresponding `*_background`, `*_front_left`, `*_front_right`,
  `*_mid_pool`, and `*_item_*` layers;
- `room_main_hall_item_throne.png` unchanged;
- the accepted Main Hall fountain, column, chandelier, banner, sconce,
  corridor, and sign art already used by the two-screen proof.

The complete room images are references, not doorway cards. Their existing
separated layers may be reused only where ownership, perspective, and scale
are valid.

### Recent Castle portfolio, evaluated

Commit `95132b6b310c34aa1d7fba5330d72f36fed9d4d7` on
`codex/day-one-opening-final` contains the recent 2D day-one pack. Its strongest
Main-Hall-compatible pieces are:

- the six dust-bunny character cards;
- `fx_dust_bunny_*`, `fx_gold_sparkle`, `fx_soap_bubbles`, and
  `fx_clean_ring`;
- the shell cleaning tools for the explicit cleanup sequence only;
- the pearl progress badges for HUD/story overlays only.

Mud, grime, spills, cobwebs, and cleaning tools must not become permanent
decor in the restored hall. The dust bunnies and response effects can supply
life without changing the room identity.

The richer illustrated object skins visible in the
`codex/dirty-castle-2d` worktree are promising, especially the shell
chandelier, cloud pouf/settee, shell drum, and story cushion. They are not
safe runtime dependencies yet: that worktree is dirty and the illustrated
skins are not all present in its recorded `6d8aa7a` commit. They remain
portfolio candidates until committed on their owner branch, provenance is
recorded, and the 4.5/5 style plus Sprite3D-card audit is rerun.

## Minimal-generation boundary

This pass creates no new runtime art. Reuse and recomposition come first.
After the layout proof, generation is permitted only for connective
architecture that cannot be constructed cleanly from existing layers:

- the two room-led wall/background masters;
- missing shell window/niche connective surfaces;
- no new throne, doors, destination signs, room furniture, character, or
  child-interaction prop.

Any generated master must preserve the exact accepted screen aspect ratio,
have a native long edge of at least 2048 pixels, pass invariance against the
door/throne masks, and be losslessly tiled into cards no larger than 1024
pixels on the long edge.

## 2.5D implementation contract

| Band | Approximate Z | Content | Behavior |
|---|---:|---|---|
| Far | `-18` to `-12` | wall plates, window views, deep niche/corridor caps | subtle camera parallax; never a screen-locked background |
| Scenic middle | `-9` to `-4` | recessed shelves, drapes, rear furniture, far fountain elements | slower parallax; can be occluded by doors/columns |
| Architecture/player | `-2` to `+1` | arches, columns, door leaves, carpet, Roshan | thresholds and navigation stay authoritative |
| Near interaction | `+2` to `+4.5` | activity-island props, dust bunnies, shadows, foreground trim | can occlude Roshan locally; never blocks an entrance |

All world art remains unshaded `Sprite3D`. HUD elevator, pause, and menu
elements remain `Control`. No model, GLB, procedural mesh, `Sprite2D`,
`AnimatedSprite2D`, `TextureRect`, or custom CanvasItem world art is allowed.

## Acceptance gates

1. Side-by-side review must identify the room references without showing a
   pasted room screenshot or mixed asset set.
2. Every door protected rectangle remains clear in projected screen space.
3. The Opera opening remains approximately twice a standard door.
4. The unchanged throne remains at the far right.
5. At least three distinct depth bands show measurable parallax and correct
   occlusion.
6. The foreground uses two or three clusters per screen, not an evenly spaced
   object row.
7. Every reused card passes the 4.5/5 Castle style gate and has a recorded
   source/hash.
8. Native master, ratio, tiling, seam, touch, navigation, node-type, and
   Speedy-tier overdraw evidence all pass before runtime acceptance.

## Audit evidence

- `audit/castle_sprite3d/castle_room_led_reference_board.png`
- `audit/castle_sprite3d/castle_room_led_visual_audit.json`
- `tools/build_castle_room_led_reference_board.py`

The reference board is a montage and implementation blueprint made entirely
from existing approved images. It is not a runtime texture and does not claim
to be a new background master.
