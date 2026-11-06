# The Pearl Canal Circuit: track reading and floor recipe

Owner rule, 2026-11-03: "the tracks themselves must resemble the in game
settings with high accuracy." The race is driven on the Racer career's own
in-game world.

## 0. Which painting is the in-game setting

There are two Racer paintings in the repository. Only one is shown in game.

| Painting | Shown in game? | What it shows |
|---|---|---|
| POT tiles `assets/opera/worlds/backdrops/world_racer_c{0,1}r{0,1}.png` = native `assets_src/imagegen/opera_codex_2026-08-02/native/world_racer_native.png` (1672 x 941, SHA-256 `d7a7cba283c0f06c7159949d63f1ca345ee4938c63374ec43bebc7c78e13deda`) inside master `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_racer.png` (2048 x 2048, `deb79c0b95bb32410bbfa4fe56fffb15e860736a72b4aaa533005efcb83cc08e`) at `Rect2(188, 553, 1672, 941)` | **Yes.** `opera_world_backdrop_2d.gd` draws these tiles whenever they exist (`_draw_racer_circuit` while driving, `_draw_tile_set` otherwise) | The water-canal circuit used below |
| `assets/opera/worlds/backdrops/world_racer.png` (1024 x 576, `1ea63f73c362b38c53a644384a5a7d31472d0ae1b28a518e9d640246268a3b51`), identical to the 2026-07-24 scene key | No (only a fallback when the tiles are missing) | A cream road, garage, grandstand, glass tube and palace. Do not use it as the setting. |

Tile SHA-256 values: c0r0 `920b4df91bad73d288ff2cd39fe8cdccc2dfe8743bb64d65a691343b7630bf66`,
c1r0 `07e7ad658427ed5cac40f1668521b4c59c54fba8bb428edb5acd36db25fbf3b7`,
c0r1 `95fa81b0f29ebee87ae6d4121334a46cac4c2545eb3b37660f002462e9b29585`,
c1r1 `359b2bdd82519239ce7de69bb50d4555c6d1e15a50407bfd008210de32ab66d5`.
Native pixel (x, y) is tile-grid pixel (x + 188, y + 553).

The earlier written handoff
`docs/handoffs/codex_minigame_rebuilds_2026-10-17/RACER.md` describes the
wrong (07-24) painting. This packet replaces it for the Racer.

The geometry source of truth is `scripts/racer/reef_kart_track.gd`
(`ReefKartTrack`). Sample the script; never re-measure from this page.

## 1. What the painting shows (native pixel boxes)

| Element | Native box | Role on the course |
|---|---|---|
| Water lane: clear aqua channel with pale lane lines, tan stone curbs, lilac stone foundations | front straight 132,531-1536,671 | The road (`ROAD_HALF` 112), curb apron (112-140), wall (`RAIL` 140) |
| Pearl-studded lilac railing | back straight about 330,180-1180,330 | The wall along the back straight |
| Pearl starting arch: cream scallop-shell arch covered in pearls | 45,280-285,600 | Start/finish line at point 0 ("Push the kart to the pearl starting arch!") |
| Three gem buoys (teal, lavender, pink orbs on pearl-ringed floats) | x 432-572, 762-905, 1066-1206; y 450-640 | Item sources on the front straight |
| Checkered-ribbon arch: pink checker ribbon with a bow, ornate shell arch | 1386,252-1640,640 | Gate at the east end of the front straight |
| Two pearl arches (lilac, pearl rims) | 367,187-532,317 and 1151,162-1291,317 | Gates at each end of the back straight, with item bubbles beneath |
| Pearl-dome pavilion with steps | 727,192-1000,455 | Infield landmark behind the back straight |
| Pennants (teal and pink, shell emblems, gold poles) | 212,57-312,197; 427,47-532,207; 1136,57-1231,197; 1346,47-1476,207 | Outside the back straight and in the skyline |
| Coral clusters | 0,600-245,935; 1496,771-1646,931 | Outside the corners |
| Pearl clams | 202,771-377,901; 1416,686-1586,761 | Infield and outside |
| Sandy infield with coral, scallops and stones | centre of the picture | Painted floor inside the loop |
| Deep blue water with light rays and rising bubbles; purple rock ledges top left and right; scallop crown ornament at top centre | top band | Skyline |

The painting has no boost pads, ramps, jumps or painted start line, so the
course has none. Pearls and the zoom item do the speeding up; the arch marks
the line.

## 2. Course layout (written map)

World: a 2048 x 2048 unit square, x to the right, y down. The centre line is
built from exact pieces and sampled into 64 control points about 67 units
apart (`ReefKartTrack.POINTS`), driven counter-clockwise on the map:

1. **Front straight** at y = 1650 from x = 700 to 1580, heading east. The
   start/finish line (point 0, x = 760) lies under the pearl starting arch.
   Gem buoys at points 4, 6 and 8 (x 1029, 1164, 1299), lateral +40. The
   checkered-ribbon arch at point 12 (x 1569).
2. **East corner** (radius 180) turning north.
3. **East S-bend** up x = 1760 (amplitude 50, flat at both ends).
4. **North-east corner** (radius 180) turning west; the east pearl arch at
   point 31.
5. **Back straight** at y = 600 bowing 40 units north at its middle, heading
   west; pavilion in the infield beside point 38; pennants outside at points
   35 and 41.
6. **North-west corner** (radius 180); the west pearl arch at point 44.
7. **West S-bend** down x = 520.
8. **South-west corner** (radius 180) back onto the front straight.

Measured: length 4,318 units; tightest bend radius about 131 (where the
spline joins the S-bends); distant parts of the course stay at least 533
units apart. Lateral offset convention: positive is right of travel, so on
this counter-clockwise course the infield is always negative (left).

## 3. Gameplay furniture (drawn by the engine)

- **Pearls:** six rows of 4-5 pearls, 52 units apart, on straights, on the
  S-bends' crossover points or on the outside of a corner (lanes a kart can
  hold at full speed). None lies within 55 units of Roshan's starting lane
  (lateral -36). The first row sits on the left of the front straight,
  facing the gem buoys on the right: pearls one side, items the other.
- **Item bubbles:** a row of three (laterals -64, 0, +64) under each pearl
  arch. The recorded instruction says "Swipe to steer through the coral
  gates!"; the arches are those gates.
- **Gem buoys:** three on the front straight. Driving into an orb pops it and
  deals an item; it returns after 3 s.

## 4. Landmark cards (positions in `ReefKartTrack.LANDMARKS`)

| id | control point | lateral | world w x h | spans the lane |
|---|---|---|---|---|
| pearl_start_arch | 0 | 0 | 330 x 250 | yes |
| coral_cluster | 6 | +230 | 200 x 150 | no |
| pearl_clam | 8 | -250 | 170 x 110 | no |
| ribbon_arch | 12 | 0 | 330 x 250 | yes |
| coral_cluster | 22 | +230 | 200 x 150 | no |
| pearl_arch | 31 | 0 | 330 x 260 | yes |
| pennant | 35 | +250 | 110 x 190 | no |
| pavilion | 38 | -330 | 340 x 320 | no |
| pennant | 41 | +250 | 110 x 190 | no |
| pearl_arch | 44 | 0 | 330 x 260 | yes |
| coral_cluster | 54 | +230 | 200 x 150 | no |
| pearl_clam | 61 | +230 | 170 x 110 | no |

A standing card's lower edge stands on the ground at its point. A spanning
arch is stretched between the two points `w / 2` either side of the lane's
centre; its opening must be transparent so the kart drives through it. The
image aspect must equal w:h.

## 5. Floor recipe (deliverable A1)

`assets/racer/tracks/pearl_canal/floor.png`: 2048 x 2048, one pixel per world
unit, top-left = world (0, 0). It re-projects the painting's own surfaces onto
the course shape. Nothing new is painted:

1. Rasterise the bands from `ReefKartTrack` (call `project()` per pixel, or
   reuse the distance convention in `floor_field()`):
   - water lane at |lateral| < 106.4, foam edge 106.4-112;
   - tan stone curb 112-140, with joints every 40 units;
   - lilac wall top 140-151, with pearl studs every 34 units along the back
     straight (the painted railing);
   - outside ground beyond 151.
2. Fill every band only with texture rectified from the matching region of
   the native painting:
   - aqua water with its pale lane lines (lines at lateral ±40);
   - tan curb stone and lilac foundation stone;
   - sand with stones.
   Inverse-perspective rectify the swatches, then tile or mirror them; keep the
   painted grain and palette.
3. Scatter the outside and the infield with top-down silhouettes of the
   painting's own coral, scallops, clams, stones and starfish. No new species
   or colours.
4. Keep pearls, item bubbles, buoys, arches, landmarks and karts out of the
   floor; the engine draws them.

Import: mipmaps on (the shader samples with `filter_linear_mipmap`), repeat
off. It is POT, so VRAM compression is allowed.

Acceptance:
- Overlaying the engine's interim field shows every band edge within 4 units.
- The floor carries nothing the painting lacks.

## 6. Skyline recipe (deliverable A2)

`assets/racer/tracks/pearl_canal/skyline.png`: 4096 x 256 RGBA.

- **Layout.** The band occupies rows 28-256; the engine samples
  `Rect2(0, 28, 4096, 228)`. Rows 0-27 are transparent padding that keeps the
  texture POT.
- **Scroll.** One full camera turn scrolls the whole width once
  (`SKY_LOOP` = 2π x 560 ≈ 3519 screen px).
- **Content.** Compose it only from the painting's top band: deep blue water
  with light rays and bubbles, the four pennants, the coral silhouettes, the
  purple rock ledges and the scallop crown. Lay crops side by side and mirror
  them so the left and right edges join seamlessly.
- **Edges.** The bottom row is the distant reef line meeting the haze colour
  `#79c9e6`; the top fades into the water colour `#2f8fcf`.

The engine's interim skyline already draws this band straight from the tiles
(native rows 0-286, alternate copies mirrored).

## 7. Other in-game settings (not in this packet)

The engine can take more courses. Each would need its own reading like this
page and an owner decision first. Two candidates:

- The castle-room course of the earlier kart game (`scripts/kart_course_worlds.gd`:
  Movie Lounge, Family Gallery and Royal Bedroom tiles under
  `assets/flats/castle/rooms/`).
- The Sky Lagoon panorama (`assets/flats/sky_lagoon/main/`).
