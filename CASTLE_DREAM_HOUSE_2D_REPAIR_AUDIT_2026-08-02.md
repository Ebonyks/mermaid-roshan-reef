# Castle Four-Room 2D Repair Audit — 2026-08-02

## Scope

Audited the four newest Castle destinations—Family Dining Room, Royal Bedroom, Sleepover Bedroom, and Cloud Movie Lounge—plus their Family Gallery doors and Main Hall wing entry. The audit compared them against the approved Royal Kitchen, Royal Library, Playroom, Opera Hall, current two-screen Main Hall, and the existing dining-room ImageGen reference.

## Finding

The implementation was structurally 2.5D but visually nonconforming. `castle_rooms_25d.gd` already created world art through `Sprite3D.new()`, yet the asset builder cropped most visible furniture directly from `assets_src/blender/qa_pearl_castle_kit/` and `assets_src/blender/qa_art_pass35/`. The four new room doors were identical copies of a painted perspective corridor with different floating plaques. The Main Hall entry placed that same corridor inside a large rectangular insert.

This produced the reported mismatch: 3D-rendered furnishings over flat procedural shells, inconsistent materials, picture-frame doors, scale drift, and weak continuity with the established hand-painted rooms.

## Before score

| Element | Score / 5 | Blocking issue |
| --- | ---: | --- |
| Gallery door architecture | 1.8 | repeated corridor pictures; floating plaque language |
| Main Hall wing entry | 2.0 | rectangular insert over painted architecture |
| Furnishing source compliance | 1.0 | Blender QA pixels loaded as room sprites |
| Furnishing style continuity | 1.7 | plastic/model render next to painted Castle art |
| Placement consistency | 2.8 | positions depended on old crop dimensions |
| Sprite3D structure | 5.0 | correct node type and real scene depth already present |

## Reuse decision

The five native 2048×2048 background masters, exact 1024×576 tile reconstruction, room topology, navigation, touch actions, audio, save state, family-picture loading, and Sprite3D depth pipeline were retained. The approved 1254×1254 dining-room reference was retained as a style/composition reference only because it is below the background-master requirement.

Repository search found no reusable approved 2D bedroom, sleepover, movie-lounge, or coherent five-door family. Regeneration was therefore limited to the two proven gaps requested by the owner:

1. doorway architecture;
2. visible furnishings.

No room identities or interactions were redesigned.

## Implemented intervention

- Generated one coherent five-door 2D architectural sheet.
- Generated one 4×4 2D furnishing sheet covering every loaded prop family.
- Preserved both native chroma sheets and transparent alpha derivatives.
- Extracted runtime cards deterministically without enlargement or warping.
- Replaced every loaded Blender-derived Dream House card.
- Removed the unused `shell_arch.png` and `shell_window.png` Blender derivatives from the runtime folder; their source renders remain preserved under `assets_src`.
- Removed the duplicate procedural frame behind the Movie Lounge screen.
- Re-anchored every replacement by its previous visual center and applied uniform scale only.
- Reduced the four door cards to a common scale and removed overlapping custom door hotspots; their full non-overlapping card bounds now define touch regions.
- Added the generated popcorn bowl as a small, tappable Movie Lounge interaction.
- Added a furnished four-room contact sheet and blocking geometry ledger.

## After score

| Element | Score / 5 | Evidence |
| --- | ---: | --- |
| Gallery door architecture | 4.7 | one base arch family; ornament-only identity variants |
| Main Hall wing entry | 4.6 | standalone architectural card; no rectangular wall patch |
| Furnishing source compliance | 5.0 | accepted 2D sheets only; Blender runtime flag false |
| Furnishing style continuity | 4.7 | common illustrated outline, palette, light, and material language |
| Placement consistency | 4.8 | 24 audited placements; all fully visible |
| Critical overlap control | 5.0 | zero gallery-door overlap; zero sleepover-bed overlap |
| Sprite3D structure | 5.0 | one Sprite3D world-art constructor; forbidden node list empty |

The retained procedural room shells are compliant native background masters and no longer contain readable Blender props. They remain less painterly than the older approved Kitchen/Library/Playroom backgrounds; a later full-background repaint would be a separate art-budget decision, not necessary to remove the two audited violations in this pass.

## Node-type inventory

| Scope | Allowed/current | Count or evidence |
| --- | --- | --- |
| World background tiles | Sprite3D | 4 exact cards per room × 5 rooms |
| Doors and furnishings | Sprite3D | built by `_new_card`; 22 extracted art files, 24 placed instances across the four furnished rooms |
| Player/world actors | Sprite3D | existing Castle controller path retained |
| Mesh/GLB world props | none | `MeshInstance3D.new()` absent |
| Flat 2D world nodes | none | Sprite2D, AnimatedSprite2D, TextureRect, and Polygon2D constructors absent |
| HUD/menu/touch | Control/CanvasItem | permitted interface exception |

## Blocking validation

`tools/audit_castle_dream_house.py` now checks:

- exactly two accepted production sheets and prompt-ledger hashes;
- alpha transparency and source hashes;
- no Blender source path or runtime-pixel flag;
- 2048×2048 masters and exact 20-tile reconstruction;
- 22-card source inventory and ≤1024 runtime dimensions;
- absence of the two retired Blender derivatives;
- furnished contact hash and 24 placement records;
- all placed cards at least 99.9% visible;
- exact runtime position/scale tokens;
- zero critical overlap;
- physical route/back-route contracts;
- Sprite3D construction and forbidden world-node absence;
- direct, unchanged protected family-picture paths.

Current result:

```text
rooms: 5
runtime_tiles: 20
props: 22
failures: 0
```
