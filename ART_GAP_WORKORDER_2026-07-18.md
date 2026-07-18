# Missing-Asset Work Order — Path to 5/5 Stage Aesthetics (2026-07-18)

Companion to `ART_AUDIT_2026-07-18.md`. This inventories what does NOT yet
exist — the visual roles still built from engine primitives, photo-derived
tiles, or flat fills in code — and names the authored asset that would close
each gap. Line references are current master.

Governance reminder: on the repo scale, 5/5 is reserved for book-source art or
owner-validated exceptional assets. "5/5 aesthetics" for a stage therefore
means every visible role at 4+, with the protected book art featured as
anchors. The lists below are ordered by aesthetic lift per stage.

## Quick wins — assets that already exist, zero modeling required

1. `assets/art35/kart/soft_barrier.glb` — built, licensed, never placed. Wire
   it as the kart track edge (edges are emissive extruded strips,
   kart.gd:1018).
2. `assets/art35/arena/treasure_chest.glb` — the castle throne back-room
   "golden stand" is still flat gold boxes (castle_hall.gd:305); reuse the
   existing chest.
3. `assets/art35/landmarks/dream_star.glb` — Dream Star platforms in Sky
   Lagoon are emissive code-geometry stars (sky_lagoon.gd:687); the authored
   star exists.
4. `assets/galaxy/crystal1-3.glb` — kart rainbow-track "crystals" are flat
   emissive boxes (kart.gd:1059); authored crystals already ship in the
   Butterfly World variant.
5. **The book art itself**: the castle gallery doorway exists but portraits
   were removed (castle_hall.gd:70-75). Re-hanging the protected story
   portraits/family art is the only change in this document that adds literal
   5/5 assets to a stage.
6. Cleanup: the four orphaned fairy GLBs, six superseded `art35/northern`
   GLBs, and the two retired photoreal HDRs (`assets/sky/lagoon_*_2k.hdr`,
   scored 2/5 and deliberately unwired — do NOT re-wire; delete or replace
   with painted panoramas).

## Castle interior — largest primitive surface area in the game

Furniture is now authored; the architecture is not. Every wall, stair,
column, arch, and ceiling is a textured BoxMesh, and ~6 texture canvases
cover the entire castle.

**Missing GLB kit (architecture):**
- Fluted column with capital/base (currently CylinderMesh + gold boxes,
  castle_hall.gd:164-179)
- Archway/doorframe/lintel trim pieces (arches are box gaps, :72-96)
- Balustrade sections (box pickets, :439)
- Chandelier (TorusMesh, :250)
- Banner/tapestry with painted cloth (flat maroon/blue QuadMesh, :206)
- Stair kit with molded steps (carpet-textured boxes)
- Stained-glass or shuttered window (flat emissive boxes, :484)

**Missing texture canvases (room identity — everything reuses
`up_castle_col` + `castle_floor_col`):**
- Throne-room floor medallion; library parquet; toy-room play mat;
  star-chamber midnight rug; ballroom/hall variants

**Missing clutter props:** barrels/crates/jam jars (undercroft, :578-583,
831), toy blocks + toy chest (toy room, :536), easel/paint pots/craft table
(craft room, :990), rubber duck (SphereMesh in the bubble bath, :950),
cradle + keepsake props (dreaming floor, :706), bedside lamps.

## Reef open world — hub composition is the blocker

- **Painted backdrop panorama** replacing the photo `backdrop_seamounts.jpg`
  cylinder (main.gd:1208) — the single biggest tonal fix.
- **Cliff/reef-wall rim kit**: the world rim is a raised heightfield with a
  photo cliff texture (main.gd:518, 1197), not geometry.
- **Pastel seabed canvases** per district replacing photo `up_sand`/
  `up_cliffwall` tiles (currently only tint-zoned, main.gd:1131-1202).
- **Hero portal-shell GLB** for the rainbow hub (six TorusMesh rings +
  cylinder beam, main.gd:3037) and a **race-gateway arch** (TorusMesh,
  :2203).
- **Friend-gateway markers** (five billboard cutouts with primitive light
  pillars/orbs, main.gd:2147).
- **Softer authored caustics sheet** (two additive procedural passes flagged
  as intrusive, main.gd:1067, 1246).

## Sky Lagoon — most missing authored architecture of any stage

- **Fairy-castle exterior kit**: towers, crown roofs, keep, merlons are all
  Cylinder/BoxMesh with flat fills (sky_lagoon.gd:45-120, 491-660); only the
  gatehouse uses an authored kit.
- **Courtyard train set**: engine, tender, coach, gondola, caboose, station,
  and track are 100% primitives (courtyard_train.gd:165-459). A five-car
  train + station + track kit is the stage's biggest single win.
- **Chalet + alpine crag kit** (BoxMesh chalets, primitive crags,
  sky_lagoon.gd:775-1127).
- **Painted meadow/terrain canvas** replacing the four photo splats
  (:1359-1466).
- **Framed-painting set**: the gallery is empty since portraits were removed —
  pairs with quick-win 5.
- **Illustrated sky panorama** replacing procedural bands; rainbow-road arc
  and star-platform props (see quick win 3).

## Kart world — two roles are absent, not just primitive

- **Grandstands, crowd, and pit garage: entirely absent** — nothing frames
  the track or gives it an audience.
- **Road-panel/trim-sheet texture** for the procedural track ribbon
  (kart.gd:944-1016).
- **Boost-pad prop/decal set** (PrismMesh ramps, :1415) and **start-grid
  decal + starting-lights gantry** (:1226).
- Wire quick wins 1 and 4 (soft barrier, crystals).

## Butterfly World / Galaxy

- **Painted planet-surface canvas** (meadow + paths + flowerbeds): the
  surface is a procedural shader with flower confetti noise (galaxy.gd:288),
  flagged "sparse/noisy".
- **Crystal wall-panel GLB** for the hall (flat translucent boxes, :1477)
  and **orrery planet GLBs** (SphereMesh, :1543).
- Verify the primitive stacked fountain (:675) is fully superseded by the
  existing `wish_fountain.glb`.
- Optional: authored nebula panorama for the shader sky dome.

## Shop, treasure vault, minigames, dungeon — short lists

- **Shop**: bean cans (CylinderMesh, main.gd:6357), aquarium tanks + shelves
  (BoxMesh, :6403), authored door.
- **Treasure vault**: loot-pile kit — gem clusters, coin stacks, pearls are
  all Sphere/CylinderMesh (:6230-6248) inside an otherwise authored cavern.
- **Penguin slide**: authored chute segments (procedural planks, :6604).
- **Fetch**: painted snowfield canvas (flat photo-tiled box, fetch.gd:18).
- **Seek**: sky/backdrop plate (flat background color).
- **Dungeon**: essentially complete — only impact/burst VFX remain spheres
  (combat_arena.gd:359, 447); wants a particle sheet.

## Northern Kingdom

Complete per `NORTHERN_WORLD_ART_AUDIT_2026-07-17.md`; nothing missing except
owner review to lift the administrative 3/5 cap.

## Suggested build order (aesthetic lift per effort)

1. Quick wins 1-5 (wiring + reuse, no modeling)
2. Sky Lagoon train set + castle exterior kit (highest-traffic primitives)
3. Castle architecture kit + per-room canvases (largest surface area)
4. Reef painted backdrop + portal hero prop (first thing seen every session)
5. Kart grandstand/garage + track texture
6. Clutter/loot props and minigame canvases
7. VFX sheets
