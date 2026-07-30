# Stuffie Playroom — Baby Eagle Rescue Guide

## Scope

The Stuffie Playroom now introduces the stuffie system through a short,
non-failing rescue. Two dust bunnies hold Baby Eagle down in the navigable
room. Mermaid Roshan clears each bunny by reaching its world-space contact
area. Clearing the second bunny frees Baby Eagle and opens the existing
full-screen stuffie picker as a focused, picture-first tutorial.

No OGV or other video file is generated, edited, transcoded, or loaded by
this feature.

## Reused source assets

No new bitmap art was generated.

| Runtime role | Asset | Native dimensions | SHA-256 |
| --- | --- | ---: | --- |
| Baby Eagle rescue card | `assets/book/baby_eagle.png` | 290×512 RGBA | `da8ead4677192ef404ed7b252fdb281cfb0234beb8064cfe7abdac2f8aade19b` |
| Left and right pinning bunny cards | `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_hop.png` | 512×512 RGBA | `677cda8c5de1d3aaf1d8960b089d48fab27106429bc221b4c26c14775b382752` |
| World tutorial pointer and rescue burst | `assets/mg/star.png` | 1024×1008 RGBA | `3cc5d5cbc5d6e0df0540cdc00ef557b0c7ed6e566331035c4e75d5d971ef3b98` |

The right bunny mirrors the same approved bunny texture through
`Sprite3D.flip_h`; no source pixels are altered.

## Authored playroom placement

Coordinates below use the playroom's 1024×576 logical art plane. Contact
points are converted to the 1280×720 stage before navigation and collision.

| ID | Logical center | Depth Z | Visual scale | Contact foot | Contact radius | Role |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `baby_eagle_rescue` | (512, 341) | 1.55 | 0.42 | n/a | n/a | restrained friend |
| `eagle_pin_left` | (445, 365) | 2.45 | 0.26 | (445, 450) | (82, 62) | left pinning bunny |
| `eagle_pin_right` | (579, 365) | 2.50 | 0.26 | (579, 450) | (82, 62) | right pinning bunny |

Both bunnies sit in front of Baby Eagle at genuine scene depth. Their stage
contact points are inside the playroom walk rectangle. A touch ray through
either visible bunny card intersects that card's actual plane and routes
Roshan to the corresponding live floor contact.

## Runtime node inventory

Before rescue, the playroom adds the following to the established room:

| Layer | Node type | Count | Shaded | Depth tested | Purpose |
| --- | --- | ---: | --- | --- | --- |
| `CastleItemVisualLayer` | `Sprite3D` | 3 | no | yes | Baby Eagle plus two pinning bunnies |
| `CastleItemEffectLayer` | `Sprite3D` | 1 | no | yes | pulsing gold rescue pointer |
| `CastleItemHotspotLayer` | `Button`/`Control` rescue hotspots | 0 | n/a | n/a | none; rescue uses camera rays and player contact |

The normal three playroom props and their three UI hotspots remain unchanged.
The stuffie room action button is hidden until the rescue is complete.

Each cleared bunny creates twelve transient unshaded `Sprite3D` star cards.
The completed rescue creates sixteen more around Baby Eagle, then the Eagle
card lifts and fades into the tutorial transition.

## Rescue and tutorial flow

1. Entering the unresolved playroom voices the rescue objective while the
   gold world-space pointer marks Baby Eagle.
2. Roshan reaches either bunny. That bunny bursts and disappears exactly
   once; the other bunny remains. Each individual clear is saved under
   `stuffie_wins["rescued_eagle_pin_left"]` or
   `stuffie_wins["rescued_eagle_pin_right"]`, so closing the game cannot
   erase half-finished rescue progress.
3. Reaching the second bunny writes
   `stuffie_wins["rescued_eagle"] = true` through the existing save path.
4. Baby Eagle celebrates and the picker opens preselected to Baby Eagle.
5. The genuine full-screen picker overlay uses `Control` UI and advances a
   gold focus frame and pointer through three steps: body part, large color,
   and the confirmation heart. Each transition also voices the next action.
6. Confirming makes Baby Eagle the active stuffie friend and clears the
   tutorial scratch state.

There is no timer, damage, loss, reading dependency, or fail state. Closing
the tutorial is harmless: the rescue remains saved and the playroom action
reopens the focused tutorial until a first stuffie is chosen.

Existing saves that already have any active stuffie skip the introductory
rescue, preserving their prior progression.

## Acceptance probes

`scripts/probe_stuffie.gd` verifies:

- Baby Eagle and exactly two pinning bunnies appear as unshaded,
  depth-tested `Sprite3D` cards;
- rescue cards have no flat UI hotspots and the normal stuffie action stays
  locked before rescue;
- clearing only one bunny cannot complete the rescue;
- an individual bunny clear reaches the normal save document immediately;
- clearing the second bunny persists rescue state and opens the picker with
  Baby Eagle as the sole tutorial choice;
- the tutorial focus advances from part to color to confirmation heart;
- confirming makes Baby Eagle the active friend and clears tutorial state.

`scripts/probe_castle_pearl_art.gd` and `scripts/probe_crown.gd` verify the
combined playroom node inventory, card depth order, camera-ray mapping,
navigation bounds, Sprite3D-only world structure, and mobile card budget.
