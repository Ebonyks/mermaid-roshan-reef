# Pearl Castle Dream House Wing

The Dream House Wing remains one physical gallery plus four casual role-play rooms for one-finger, non-reading play:

| Gallery ornament | Room | Casual play |
| --- | --- | --- |
| plate, spoon, and fruit | Family Dining Room | serve six places and eat |
| moon, pearl, and crown | Royal Bedroom | sleep, use the pearl light, dress up, and read |
| three stars and pillow | Sleepover Bedroom | choose one of three dream beds |
| curtain and play symbol | Cloud Movie Lounge | watch family pictures, sit, bounce, and tap popcorn |

Back from each role-play room returns to the gallery. Back from the gallery returns to Main Hall. No route depends on text, and there is no failure state.

## 2026-08-02 2D repair

The four-room expansion had a correct Sprite3D runtime structure but the wrong visible source medium:

- furnishings were transparent crops of Blender QA renders;
- all four gallery doors reused the same perspective-corridor picture;
- the family-wing Main Hall entry added a rectangular wall insert;
- the generated cards had different dimensions, so a texture-only swap would have shifted and shrunk the rooms.

The repair uses exactly two accepted ImageGen sheets:

1. one five-door architectural family, without corridor pictures or UI-button plaques;
2. one 4×4 furnishing family covering every loaded dining, royal-bedroom, sleepover, and movie-lounge prop plus a tappable popcorn bowl.

The full chroma and alpha sheets, exact prompts, hashes, and reference roles are under `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/`. Runtime cards are deterministic crops made by `tools/build_castle_dream_house_rooms.py`.

## Runtime and depth contract

- Every visible wing background, door, furnishing, family movie, and player remains a real-depth Sprite3D card.
- There are no Sprite2D, AnimatedSprite2D, TextureRect, Polygon2D, CanvasItem-drawn world objects, MeshInstance3D props, GLBs, or procedural runtime meshes in this room pipeline.
- HUD and controls remain permitted Control/CanvasItem elements.
- Five 2048×2048 background masters remain preserved. Each centered 2048×1152 gameplay band reconstructs from four exact, non-overlapping 1024×576 cards.
- Furnishings are independent transparent cards with uniform scaling and audited source positions. The gallery doors and sleepover beds have zero geometric overlap.
- The movie background no longer paints a second screen frame behind the generated 2D screen.
- Protected family pictures are loaded directly and unchanged from `assets/book/hall/`; none is copied into the placement contact.

## Audit evidence

- `audit/castle_dream_house/dream_house_room_art_manifest.json`: sources, hashes, cell rectangles, node inventory, placement rectangles, tile reconstruction, and zero-overlap result.
- `audit/castle_dream_house/dream_house_layout_contact.png`: physical gallery doors and Main Hall wing entry.
- `audit/castle_dream_house/dream_house_furnished_rooms_contact.png`: all four furnished room compositions, omitting protected family picture pixels.
- `CASTLE_DREAM_HOUSE_2D_REPAIR_AUDIT_2026-08-02.md`: before/after audit and intervention decision.

Rebuild and block regressions with:

```powershell
python tools/build_castle_dream_house_rooms.py
python tools/audit_castle_dream_house.py
```
