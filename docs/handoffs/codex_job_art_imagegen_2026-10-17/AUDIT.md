# Job-game art audit: flat vector art, and painted art that never reached the game (2026-10-17)

**Requested by the owner, 2026-10-17:** find the weak artwork in the game,
particularly in the jobs; find where ImageGen versions were made but are not
properly in the game; find where ImageGen art is still needed; the aim is to
eliminate flat vector art.
**By:** Claude. This is a written audit: no game file was changed and no
image was made.
**Baseline:** `dev` `7a65b9f0abacddeee70230f220955f4d18d551b5`.
**Method:**
- Code reading of every job script, done in four read-only sweeps. Every
  claim used below was spot-checked against the source.
- The numbers-only tool [`tools/measure_job_art.py`](tools/measure_job_art.py).
  Its output is in [`data/measure_baseline.json`](data/measure_baseline.json).
- Git history of every unmerged branch.
- Viewing existing image files by eye. No image was created, edited or
  composited.

**Not covered:**
- No runtime capture, phone session, child session or owner review. Every
  visual statement comes from code and source images.
- Opera venue art outside the careers, Sky Lagoon and the dormant minigames
  are out of scope.

Line references are `file:line` at the baseline. Short names:

| Short name | File |
|---|---|
| `gesture` | `scripts/opera_gesture_surface.gd` |
| `world` | `scripts/opera_career_world_2d.gd` |
| `backdrop` | `scripts/opera_world_backdrop_2d.gd` |
| `hotspot` | `scripts/opera_world_hotspot_2d.gd` |
| `catalog` | `scripts/opera_hotspot_catalog.gd` |

## 1. The answer in brief

**1. Weak art in the jobs.** In the Opera career code, code-drawn shapes
outnumber painted pictures about nine to one: 972 primitive draw calls against
107 texture draws.

- **Code-drawn games.** 28 of the 61 career phases have no painted widget
  family and draw their own picture. Three careers are almost entirely code:
  - Geologist: the whole room and every work object.
  - Teacher: no texture at all.
  - Astronaut's pipe board.
- **Code-drawn objects the child acts on.** In nine more careers the central
  object is drawn in code:
  - Chef: the oven and cake, bowl, frosting cake and piping bag.
  - Boxer: both gloves.
  - Candymaker: the candies the child sorts and the friends who receive them.
  - Doctor: the sink and hands, plus the bandage patient, which is a brown
    blob instead of the starfish.
  - Farmer: the seed bed, sprouts and barn gate.
  - Magician: the rope and portal.
  - Painter: the cloudy cover.
  - Nursery: the cribs, blanket and patting hand.
  - Pop Star: the rhythm stars.
- **Decoration over every career.** Spotlight wedges, halos, sparkles and
  progress dots are drawn over every career. Ambient doodles are drawn over
  every career and every Day One room except the Pool.
- **Live vector files.** Five SVG files are still in use: four for the
  Geologist and one for the Teacher.

**2. Painted art made but not in the game.**

- **74 painted runtime images sit on four unmerged branches.** Their bytes
  exist nowhere on `dev`. They include:
  - the whole Geologist work set: fossil, strata rock, crystals, pan, work
    slab, a six-state geode opening and river channel tiles;
  - the Nursery wash and care frames, cradle hands and pillows;
  - the Boxer's painted gloves;
  - 25 kart views.
- **A complete painted Geologist grotto** has sat in `assets_src` since
  2026-09-05.
- **Three code paths ask for art that was never made:**
  - the Astronaut pipe tiles, tank and intake;
  - the Pop Star star notes;
  - the Magician portal ring.
- **Two Geologist paths are set to empty strings,** so painted pan and geode
  art can never load even if it is added.
- **Much painted art is loaded but never drawn, or is drawn badly:**
  stretched, ghosted at 60%, covered by flat gold slabs, or tinted.

**3. ImageGen still needed.** In outline:

- the Teacher lesson set;
- the Astronaut pipe set and launch flame;
- the Chef oven and frosting cake;
- the Doctor sink and the hands;
- the Farmer seed bed, sprouts and barn gate;
- the Magician portal;
- the Pop Star stars;
- the Nursery crib and blanket;
- the Racer steering wheel and turbo button;
- the Ballerina shell frame and ribbon;
- one shared painted family for medals, pearls, invitation rings, sparkles
  and confetti;
- the Geologist crest and native-resolution grotto;
- Chapter Two party hats and story props.

Every item is listed with its source in
[`data/job_art_register.json`](data/job_art_register.json) and described for
generation in [BRIEFS.md](BRIEFS.md).

## 2. Measurements

From `tools/measure_job_art.py` at the baseline.

| Group (scripts) | Primitive draw calls | Primitive nodes/styles | Texture draw calls |
|---|---:|---:|---:|
| Shared gesture surface (`gesture`), nine careers | 439 | 0 | 61 |
| Shared career world (`world`, `backdrop`, `hotspot`, `living_world_canvas.gd`, venue) | 288 | 11 | 17 |
| Shared Hall HUD (`opera_performance_overlay.gd`) | 23 | 0 | 0 |
| Geologist surface | 49 | 0 | 5 |
| Boxer surface | 41 | 0 | 7 |
| Ballerina surface | 40 | 0 | 2 |
| Teacher surface | 32 | 0 | 0 |
| Racer surface | 28 | 1 | 4 |
| Arborist tree-book prototype | 14 | 1 | 1 |
| Nursery catch | 10 | 0 | 3 |
| Chef surface (Chapter Two) | 8 | 0 | 7 |
| **Opera careers, total** | **972** | **13** | **107** |
| Chapter Two job scenes (cake, candle, lawn, party table) | 47 | 5 | 0 |
| Day One job scripts (grime, bathroom, studio, Grand Puff telegraph) | 28 | 3 | 1 |
| All 70 runtime scripts that draw primitives | 1,169 | 118 | 113 |

**Career phases.** `world` `PHASES` defines 61 phases in 15 careers.
- 33 resolve to a painted widget family; 99 of the 181 widget PNGs match a
  current phase.
- 28 resolve to no family and draw their own picture: Teacher 4, Boxer 5,
  Ballerina 3, Geologist 4, Detective 3, Nursery WASH HANDS, FEED, BURP and
  BEDTIME, Magician CABINET, Farmer PLANT, Astronaut PIPES, Racer RACE and
  Pop Star RHYTHM.
- A few of those 28 still load painted props by exact path: clue board, crown
  chest, magic cabinet, vanish hat and wand.

**Live SVG files.** All five are hand-written vector paths:

| File | Used at | Uses |
|---|---|---|
| `assets/opera/worlds/hotspots/geologist_fossil.svg` | `opera_geology_surface.gd:42`, `catalog:135` | 3 |
| `assets/opera/worlds/hotspots/geologist_layered_rock.svg` | `opera_geology_surface.gd:44`, `catalog:134`, `catalog:136` | 4 |
| `assets/opera/worlds/props/goal_geologist.svg` | `opera_geology_surface.gd:47`, `catalog:137`, `world:463` | 4 |
| `assets/opera/worlds/ui/crests/opera_crest_geologist.svg` | `scripts/castle_career_routes.gd:48` | 1 |
| `assets/opera/worlds/hotspots/teacher_lesson_board.svg` | `catalog:48-51`, `world:449` | 6 |

**Gold-star C7 (authored art), as scored 2026-10-03.** 13 careers score 1,
Nursery 2 and Geologist 0. Source: `design/reference/games.json`.

## 3. Painted art that exists but is not in the game

### 3.1 Stranded on unmerged branches: 74 images, none on `dev`

Bytes were checked by git blob against every path on `dev`; no copy exists.

The alpha check (tool `cutout`) reads pixels only and writes nothing.
- All 73 RGBA files pass: the visible pixels are at least 80% near-opaque,
  with no opaque background.
- The one RGB file fails.

| Branch (head) | Images | Contents | By eye (files viewed) | Verdict |
|---|---:|---|---|---|
| `codex/job-art-review-v2-20261001` (`cfcadc96`; 55 ahead of dev, 139 behind) | 40 | Geologist `painted_work_v1_20261001/`: fossil, fossil_soil, grain, layered_rock, mineral, pan, work_slab. `painted_geode_v1_20261001/`: closed, early_crack, middle_open, open_embedded. `coherent_geode_v1_20261002/`: opening_six_states, opening_bridge. `painted_river_v1_20261002/`: dry and wet straight and junctions, earth_bed, nodes. Nursery `refinement_v1/`: cradle (two cupped hands), pillows. `refinement_v2/`: care_00-07 (Roshan in the nursery apron, eight care poses). `wash_connected_v1_20261002/`: ready, wet, rub_palm, rub_palm02, rub_back, rinse, clean. Boxing gloves left and right. Pool skimmer and floating trash. | Good pastel storybook finish, navy-plum contours, broad value bands: fossil, layered_rock, mineral, pan, work_slab, open geode, six-state geode sheet, river junctions and nodes, care_00, wash `ready`, cradle hands, boxing glove. The Pool skimmer has a baked dark glow around the net. | **Ready to wire** after an in-context check. Roshan-bearing frames (care, wash) follow the older career design, which the owner keeps for careers (`ODR-ROSHAN-Q13`), so check them against `roshan_nursery_sheet_a.png`. |
| `codex/racer-existing-engine-2d-20261003` (`fcee911c`) | 25 | `assets/kart/canvas/` kart and moto front, quarter, rear, side, top. `assets/kart/chase/` kart, moto and truck: straight, left, right, boost, empty. | Good: the side view and chase straight were viewed. | **Optional.** The current Racer uses a painted kart already; this set belongs to an unadopted chase-camera race. Keep it on the branch unless the owner wants that race. |
| `codex/astronaut-clearance-20261006` (`ec533a5f`) | 3 | `astronaut_gear_v1.png`, `astronaut_pipe_straight_candidate_v1.png`, `astronaut_radioactive_fluid_v1.png` | The gear is realistic scratched brass, not the pastel style (`DL-VIS-05`). The fluid is a full-bleed neon-green texture with no alpha (`DL-VIS-04`), and "radioactive" is wrong for a four-year-old. The pipe is acceptable but glossier than the set. | **Do not wire** the gear or the fluid. The pipe serves only as a style reference for the pipe brief. |
| `codex/studio-scene-integration` (`b5f78e3a`) | 6 | Day One studio counters and paint table, clean and dirty | not viewed | **In flight** today in Codex's `studio-room-repair` work; not this packet's. |

Codex's runtime branch `codex/flat-vector-geologist-pan-runtime-20261017`
(`2d91d85f`) also carries `assets/opera/worlds/props/geologist_washing_pan_painted.png`.
That is a 2026-09-05 pan whose bytes are on `dev` only in
`assets_src/minigame_art_quality_2026-09-05/pan-alpha-attempt02/native.png`.
Its CI was running at the time of this audit.

### 3.2 Painted sources that were never prepared for the game

| Source | What it is | Why it stopped | Use now |
|---|---|---|---|
| `assets_src/geologist_rebuild_2026-09-05/geology_grotto_candidate.png` (sha256 `e60684278d33e43a51eea3534b99aa8c70e90b2ef3f11004f4d04154273fbd4b`, 1672×941, RGB) | A full painted geology grotto with a stepped spring and pool (left), a stone work dais (centre), a shell-rimmed washing basin (right centre) and a crystal cave arch (right). These match the four Geologist stations. | "REFERENCE_ONLY": below the 2048×2048 native coverage each career room has (`generation_manifest.json`) | Composition and style reference for a native 2048×2048 regeneration (brief JB-GEO-01). |
| `assets_src/geologist_rebuild_2026-09-05/geology_props_candidate.png`, `geology_props_alpha_retry.png` | Fossil, geode, brush, pan and mineral atlas | Baked checkerboard instead of alpha. The rejection left the SVGs in place (`opera_geology_surface.gd:40-47`). | Superseded by the stranded `painted_work_v1` set in 3.1. |
| `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/` (576 RGB 1024² cards, 16 gameplay + 16 outfit + 16 stage-state cards for each of 12 careers) | Concept props for nearly every code-drawn object: pastry chef bowls, ovens and piping ribbon; candy molds and candies; doctor bandage and stethoscope; farmer piggies, vegetables and hay; magician hats and wand; painter canvases and stamps; pop-star arrows, microphones and rhythm ribbon; racer steering wheel, turbo button and zoom strips; boxer gloves and round lamps; ballerina shell and pearl tiles and ribbon; astronaut elbow, ring and straight pipes, bubble tank and valve. | These are 4×4 concept-sheet cells on a navy presentation background, upscaled from roughly 256 px. Their Roshan identity was bound to the retired `roshan_sprite.png`. | **Design references only** for ImageGen briefs (prop cards, never Roshan cards). They are not runtime art. |

### 3.3 Code that asks for painted art that was never made

| Texture path(s) requested | Requested at | What the child sees instead |
|---|---|---|
| `assets/opera/worlds/widgets/widget_pipe_{tile_h,tile_v,elbow_ne,elbow_nw,elbow_se,elbow_sw}.png`, `widget_pipe_tank.png`, `widget_pipe_intake.png` | `gesture:708-722` | The whole Astronaut PIPES board in code: tan rectangles, thick lines, circle mouths, flat grid plates, and napping imps made of circles (`gesture:5816-5900`) |
| `assets/opera/worlds/widgets/popstar_star_note_{unlit,lit}.png` | `gesture:723-725` | Ten-point polygon stars as the only tap targets (`gesture:5974-5999`) |
| `widget_portal_magician_{ring,overlay}.png` and `widget_crank_magician_portal_{ring,overlay}.png` | `gesture:657-677` | Code arcs and rotating dots for the star portal (`gesture:2081-2096`); flat ring art as a stand-in overlay (`gesture:680-681`) |
| `widget_target_{chef,candymaker,doctor,farmer,painter,astronaut}_success.png` | `gesture:810` | Code success rings |

### 3.4 Paths switched off, never assigned, or never reached

- **Geologist pan and geode paths are empty strings.**
  - Lines: `opera_geology_surface.gd:43` (`GEODE_PATH := ""`) and `:46`
    (`PAN_PATH := ""`).
  - The comment at `:40-41` keeps "approved vectors" as runtime authority
    "until the new raster candidates pass alpha/native-resolution review".
  - The candidates that would pass are the stranded set in 3.1.
- **The Nursery WASH HANDS phase draws nothing but the ghost finger.**
  - Its widget template is `nursery`, which no drawing branch handles.
  - The old code basin (`gesture:4006-4052`) is unreachable.
  - `widget_basin_nursery*.png` is never loaded.
  - The stranded `wash_connected_v1_20261002` frames were made for this phase.
- **The painted station marker is dead code.**
  - `world:2335-2348` `_draw_station_marker` has not been called since commit
    `9427f3b0` (2026-08-10).
  - `assets/opera/worlds/ui/station_marker.png` and `task_card_frame.png` are
    unreferenced. Clean-up only; there is no live defect.

### 3.5 Loaded but never drawn

- `widget_gauge_chef_success.png`, a painted finished cake.
  - Loaded at `gesture:776`.
  - The code oven draws a rectangle-and-circle cake instead
    (`gesture:5358-5381`).
  - The comment at `gesture:5359-5361` promises an "authored oven backdrop
    when present", but no branch draws one.
- `widget_lanes_candymaker_lit.png`, painted dispensers and jars (loaded at
  `gesture:812`).
- `widget_crank_candymaker_mover.png`, a painted wrapped candy (loaded at
  `gesture:798`).
- `widget_pour_chef_fill.png` (`gesture:782`) and all `widget_crank_*_progress.png`
  except the magician fallback (`gesture:799`).
- `widget_trace_{chef,doctor,magician,painter}_lit.png` (`gesture:801`).
- `widget_charge_{astronaut,popstar}_{glow,full}.png` (`gesture:795-796`).
- `widget_gauge_shared_needle.png` and `widget_push_shared_arrow_lr.png`
  (`gesture:775`, `806`).
- `props/goal_farmer.png` (`gesture:706-707`).
- `geologist_layered_rock.svg` (`opera_geology_surface.gd:250`).
- `chapter2_candied_strawberries_tray.png` and the cake-stage art. These are
  passed only as surface metadata (`world:2634-2643`) that no drawing code
  reads.
- Day One:
  - `fx_soap_bubbles.png`, `target_bath_soap_ring.png` and
    `fx_wipe_swoosh.png` are hidden at every state
    (`scripts/games/day_one_bathroom_cleaning.gd:38-42`, `484-491`), while
    code arrows and a bullseye guide the bathroom job (`:68-94`).
  - `fx_stolen_sparkle.png` via `_spawn_sparkle`, which is never called
    (`scripts/games/day_one_bathroom_cleanup.gd:62`, `816-832`).

### 3.6 Retired widget cards that still hold painted objects

Each retired whole-card `widget_<context>.png` is kept for provenance and not
loaded (`gesture:766-772`). Several contain painted objects that the code now
redraws as flat shapes. Cutting them out is a quick win that needs no
generation:

| Card | Object it holds |
|---|---|
| `widget_gauge_chef.png` | oven |
| `widget_pour_chef.png` | bowl |
| `widget_crank_chef.png` | bowl of batter |
| `widget_trace_chef.png` | piping bag and frosting |
| `widget_basin_doctor.png` | shell sink, faucet, soap, towel |
| `widget_crank_doctor.png` | cast and cushion |
| `widget_trace_doctor.png` | bandage strip |
| `widget_trace_magician.png` | rope |
| `widget_crank_astronaut.png` | valve column |
| `widget_lanes_candymaker.png` | candy dispensers |

## 4. Each job: what the child sees now

Rows marked **painted exists** have finished painted art available; the
others need ImageGen. Item IDs refer to the register, and brief IDs to
[BRIEFS.md](BRIEFS.md).

### Geologist: the worst case (C7 0)

The room, tray, river, fossil dirt, pan and geode are all code. The
remaining objects are flat SVGs.

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| Room: sky, floor, hill, strata, crystals; vector curtain-call proscenium | `backdrop:274-284`, `587-622`, `319-347` | code shapes. No `world_geologist*` art exists. | Grotto candidate (3.2); shared `assets/opera/worlds/stage/finale_stage_c*r*.png` for the curtain call | JA-GEO-01 / JB-GEO-01 |
| Work tray | `opera_geology_surface.gd:837-880` | tan code rectangle 860×560 | **painted exists**: `painted_work_v1/work_slab.png` | JA-GEO-02 |
| River channel, spring and pool | `:631-657` | code circles and lines | **painted exists**: `painted_river_v1` (6 files) | JA-GEO-03 |
| Fossil dirt grid and fossil | `:682-723` | 8×5 flat squares over a stretched SVG (~2:1) | **painted exists**: `fossil_soil.png`, `fossil.png` | JA-GEO-04 |
| Gold pan, water, grains, minerals | `:762-794` | code ellipse, waves, pentagons. `PAN_PATH = ""`. | **painted exists**: `pan.png`, `grain.png`, `mineral.png` (and Codex's in-flight pan) | JA-GEO-05 |
| Geode | `:797-834` | code half-shells and dots; SVG crystals | **painted exists**: `painted_geode_v1` 4 states and the six-state sheet | JA-GEO-06 |
| Hotspots and goal prop | `catalog:134-137`, `world:463` | SVG | **painted exists**: `layered_rock.png`, `fossil.png`, `mineral.png` | JA-GEO-07 |
| Career crest | `scripts/castle_career_routes.gd:48` | SVG | — | JA-GEO-08 / JB-GEO-02 |

### Teacher: no textures at all (C7 1)

| What the child sees | Where | Now | Item / brief |
|---|---|---|---|
| Lesson board covering the painted library | `opera_teacher_surface.gd:266-267` | 850×555 StyleBox panel and line | JA-TEA-01 / JB-TEA-01 |
| Pattern and match shapes (circle, triangle, square, star, heart) and the blank slot | `:308-323`, `:378-404` | code shapes and StyleBox | JA-TEA-02 / JB-TEA-02 |
| Counting pearls, the two group trays, the "+" join button, tick marks | `:325-354`, `:366-376` | circles, StyleBox, lines | JA-TEA-03 / JB-TEA-03 |
| Answer cards | `:276-291` | StyleBox in state colours | JA-TEA-04 / JB-TEA-04 |
| Hint button, solved star orbit, demo ring | `:300-306`, `:292-298`, `:406-420` | code; the hint shape is unclear | JA-TEA-05 (hand: reuse `ghost_hand.png`) |
| Lesson-board hotspot and goal prop | `catalog:47-52`, `world:449` | SVG | JA-TEA-06 / JB-TEA-01 |
| Crest slot | `scripts/castle_career_routes.gd:49` | Roshan's sprite shown as the crest | JA-TEA-07 / JB-TEA-05 |
| Caption panel | `world:1305-1315` | flat StyleBox text box | covered by shared UI JA-SHR-10 |

### Astronaut (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| PIPES tiles, grid plates, tray | `gesture:5816-5900` | code (art never made, 3.3) | concept cards (elbow, straight, ring pipe; bubble tank) as reference | JA-AST-01 / JB-AST-01 |
| Napping imps on the board | `gesture:5853-5859` | four circles | imp art exists but has no sleeping pose | JA-AST-02 / JB-AST-02 |
| Fuel tank, outlet, rocket intake | `gesture:5871-5891` | circles and rectangle | crop `coolant_tank_pad` from `world_astronaut` tiles, or generate | JA-AST-03 / JB-AST-01 |
| PATCH pieces | `widget_target_astronaut_piece_0..2.png` | flat-fill PNGs with uniform outline | — | JA-AST-04 / JB-AST-03 |
| LAUNCH flame and exhaust | `gesture:2599-2627` | orange triangle, circles | — | JA-AST-05 / JB-AST-04 |
| VALVE backing disc | `gesture:2461`, `2467` | dark navy disc hiding nothing | valve column in retired `widget_crank_astronaut.png` | JA-AST-06 |

### Chef (C7 1; owner rejected its look, `MA-OPERA-001`)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| BAKE oven, window, cake, door and mitt handle (the tap target), thermometer | `gesture:5358-5426` | brown rectangles; rectangle-and-circle cake | oven in retired `widget_gauge_chef.png`; **painted exists**: cake `widget_gauge_chef_success.png` (loaded, never drawn); `room_kitchen_item_oven.png` | JA-CHF-01 / JB-CHF-01 |
| MIX bowl and batter level | `gesture:6248-6254` | ovals | **painted exists**: `assets/chapter2/birthday/chef_empty_shell_bowl_v1.png`, `chapter2_chef_batter_unstirred.png` | JA-CHF-02 |
| MIX stream, beads, splash | `gesture:6281-6296` | lines and circles | — | JA-CHF-03 / JB-SHR-05 |
| MIX jug | `gesture:6075`, `6269-6270` | painted jug squeezed ~17% wide, never empties | — | JA-CHF-04 (fix use) |
| STIR bowl and batter, swirls | `gesture:2313-2333` | ovals, arcs | **painted exists**: `chapter2_chef_batter_unstirred.png` / `_stirred.png` | JA-CHF-05 |
| STIR whisk | `gesture:2317-2321` | painted whisk spun like a propeller round its own centre | — | JA-CHF-06 (fix use) |
| FROST cake, plate, piping bag, frosting | `gesture:1929-1946`, `1855-1866` | rectangle cake, polygon bag, polylines | **painted exists**: `chapter2_chef_stacked_unfrosted_cake.png` → `chapter2_chef_frosted_rainbow_cake.png`; bag in retired `widget_trace_chef.png` | JA-CHF-07 / JB-CHF-02 (frosting stroke) |
| TOP | `gesture:3043-3096` | painted; `widget_target_chef_piece_2.png` reads like a poop emoji | — | JA-CHF-08 / JB-CHF-03 |
| Chapter Two stack cap | `scripts/opera_chef_surface.gd:166-177` | painted tier warped ~2.1× wide | — | JA-CHF-09 (fix use) |

### Candymaker (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| SORT candies being dragged and the bins | `gesture:4690-4752` | polygons; flat bins; line belt | **painted exists**: identical candies `widget_target_candymaker_piece_0..2.png`; jars in `widget_lanes_candymaker_lit.png`. Codex's in-flight `candymaker_sort_boxes_v2.png` | JA-CDY-01 (coordinate) |
| WRAP candy and twisting ends | `gesture:2373-2392` | oval and polygons | **painted exists**: candy inside `widget_crank_candymaker_mover.png` | JA-CDY-02 / JB-CDY-01 (wrapper twist states) |
| SHARE: six waving friends | `gesture:2988-3014` | stick-figure circles and lines | none. The protected friend portraits are not to be altered. | JA-CDY-03 / JB-CDY-02 |
| SYRUP stream | `gesture:6200-6222` | polylines | scene, fill and ladle painted | JA-CDY-04 / JB-SHR-05 |
| Chapter Two COAT, SORT, GLAZE, PLACE | `world:2164-2253`; surface hidden at `world:2747-2750` on purpose | flat StyleBox pitcher, stream, lane boxes, crank disc, trays; code candies where the voice says strawberries | **painted exists**: `chapter2_candied_strawberries_tray.png`, `sky_lagoon_strawberry_single.png` | JA-CH2-01 / JB-CH2-01 |

### Doctor (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| WASH sink, faucet, water, Roshan's hands | `gesture:2770-2797` | ovals and lines | sink in retired `widget_basin_doctor.png`; `assets/flats/castle/rooms/room_bubble_bath_item_sink.png`; hands: none | JA-DOC-01 / JB-DOC-01 |
| WASH "bubbles" | `widget_basin_doctor_bubbles.png` | flat rings passing as bubbles | `assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png` | JA-DOC-02 |
| X-RAY scan plate the child drags | `gesture:4396-4409` | cyan rectangle; gold card border | — | JA-DOC-03 / JB-DOC-02 |
| CAST bed, cushion, cast strips | `gesture:2401-2443` | nine ovals; six lines | cast and cushion in retired `widget_crank_doctor.png` | JA-DOC-04 / JB-DOC-03 |
| BANDAGE patient, roll, strip | `gesture:1961-1975`, `1855-1866` | a brown round plush with dot eyes, not the coral starfish used everywhere else | **painted exists**: `widget_crank_doctor_patient.png`; roll `widget_crank_doctor_mover.png` | JA-DOC-05 / JB-DOC-03 |
| FIND choices | lanes row `gesture:2732-2745` | painted starfish drawn at 60% alpha | — | JA-SHR-06 (fix use) |

### Farmer (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| PLANT bed, holes, sprouts, flowers | `gesture:3823-3845` | flat brown rectangle, dark holes, stick sprouts | crop the tilled bed from `world_farmer` tiles (`scripts/opera_stage_paths.gd:113`); sprouts: none | JA-FRM-01 / JB-FRM-01 |
| TOSS: munch face pasted over the painted piglet | `gesture:5021-5045` | pink circles | none (a chewing pose) | JA-FRM-02 / JB-FRM-02 |
| TOSS basket, target ring, sling, arc guide | `gesture:5048-5094`, `4992-4996` | ovals, rings, dots, arrow; the basket duplicates the painted one | painted basket in `widget_target_farmer_mover.png` | JA-FRM-03 (remove duplicate) |
| HERD barn gate (the destination) | `gesture:1631-1655` | lines, circles, arc | crop the barn doors from `world_farmer` tiles (`opera_stage_paths.gd:110`) | JA-FRM-04 / JB-FRM-03 |
| PLANT seed | `gesture:3849-3851` | `assets/mg/seed.png` (512×469) squeezed into a square | — | JA-FRM-05 (fix use) |

### Magician (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| ROPE rope and knots | `gesture:1855-1866`, `1981-1990` | polylines and circles | **painted exists**: `assets/opera/worlds/hotspots/magician_rope.png` (shell knots) | JA-MAG-01 |
| PORTAL swirl | `gesture:2040-2096` | arcs and rotating dots; ring art never made | — | JA-MAG-02 / JB-MAG-01 |
| TRACK: hats never move; a dot glides instead | `gesture:5313-5327` | code dots | painted hats in `widget_lanes_magician_lit.png` (they have white scratch marks) | JA-MAG-03 (move the painted hats) |
| CABINET flat gold slab over the painted knob | `gesture:3980-3988` | rectangle | painted knob on `widget_magic_cabinet_closed.png`; `_reveal.png` has a white box round Lamba | JA-MAG-04 (fix use + alpha) |

### Painter (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| PAINT cloudy veil | `gesture:4844-4852` | up to 60 flat off-white squares | painted cloud `assets/opera/worlds/props/fx_dust_puff.png` | JA-PNT-01 / JB-PNT-01 |
| Frame slab around a painting that has its own frame | `gesture:4834`, `4853-4854` | rectangle and border | the painting's own frame | JA-PNT-02 (remove) |
| Chapter Two banner squashed into squares and cut into lane frames | `gesture:4836`, `1526`, `2738-2741`; `hotspot:304-307` | `castle_banner_rainbow.png` (256×512) distorted | — | JA-PNT-03 (fix use) |

### Detective (C7 1; scene investigation in flight in Codex's `detective-scene-investigation`)

| What the child sees | Where | Now | Available | Item |
|---|---|---|---|---|
| SEARCH clues are gold dots and rings under the lens | `world:4650-4660` | code | **painted exists**: `widget_clue_board_tokens.png` (paw, feather, bow) | JA-DET-01 |
| CASE BOARD drop boxes and tokens about 30 px above the painted silhouettes; tokens drawn twice | `gesture:3631-3639` | rectangles | the painted silhouettes | JA-DET-02 (fix use) |
| CROWN flat gold "handle" slab over the painted shell lock | `gesture:3727-3728` | rectangle | the painted lock | JA-DET-03 (fix use) |
| Chapter Two "magic storybook" | `world:2272-2285` | lavender rectangle with dots | none (an open storybook spread) | JA-CH2-02 / JB-CH2-02 |

### Boxer (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| Both gloves the child drags | `scripts/opera_boxing_surface.gd:761-802` | compound circles, cuff rectangles. The comment at `:776-777` avoids glove art "without deriving or regenerating the approved fused glove bitmap". | **painted exists**: stranded `boxing_glove_left.png` / `_right.png` | JA-BOX-01 |
| Incoming counter-punch glove | `:698-720` | coral disc and arrow | the same gloves | JA-BOX-02 |
| Target rings over the painted mitts and belt | `:682-695`, `855-861` | circles; `widget_target_boxer_mark.png` is itself a flat ring | — | JA-BOX-03 / JB-SHR-02 |
| Round progress lights | `:645-655` | circles | concept `boxer_gameplay_round_lamps` | JA-BOX-04 / JB-SHR-03 |
| Stage wash | `:616` | 6% navy over the painted ring | — | JA-BOX-05 (remove) |

### Ballerina (C7 1)

| What the child sees | Where | Now | Item / brief |
|---|---|---|---|
| Pearl-mirror shell frames the child taps | `scripts/opera_ballet_surface.gd:592-610` | nine petal circles and rings | JA-BAL-01 / JB-BAL-01 |
| Ribbon trail and draggable pearl | `:639-680` | three-pass lines, circles | JA-BAL-02 / JB-BAL-02 |
| Twirl ring, progress arc, handle | `:683-717` | circles and arcs | JA-BAL-03 / JB-BAL-02 |
| Pose portraits | `:613-623` | straight cut through the tail on row 2 | JA-BAL-04 (fix crop) |
| Dimmer disc over wrong poses | `:586-588` | 44% navy | JA-BAL-05 (remove) |

### Racer (C7 1)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| RACE steering bar and knob, turbo button | `scripts/opera_racer_surface.gd:87-91`, `439-464` | StyleBox pill, chevrons, circles, lightning polygon | concept `racecar_driver_gameplay_steering_wheel`, `_turbo_button` | JA-RAC-01 / JB-RAC-01 |
| Lap dials and start lights | `:420-438`, `465-469` | circles and polygons | concept `racecar_driver_stage_states_progress_lamps` | JA-RAC-02 / JB-RAC-01 |
| Track pearls | `:354-361` | circles | shared pearl (JB-SHR-03) | JA-RAC-03 |
| Boost strips | `:348-353` | flat `assets/kart/boost_ribbon.png` squashed to ~55% | concept `zoom_strip_active` | JA-RAC-04 / JB-RAC-01 |
| Driver crops | `:385-392` | mid-thigh cut showing above the seat | — | JA-RAC-05 (fix crop) |
| TO THE LINE start arch | `gesture:1656-1665` | small gold arch of lines | crop the shell start arch from `world_racer` tiles (`opera_stage_paths.gd:165`); `assets/kart/finish_banner.png` | JA-RAC-06 |

### Nursery (C7 2: the best career, still with flat central objects)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| CATCH cradle and pillows | `scripts/opera_nursery_catch.gd:242-270` | `widget_catch_nursery_cradle.png` and `_pillows.png` are flat-vector PNGs | **painted exists**: stranded `refinement_v1/cradle.png` (hands) and `pillows.png` | JA-NUR-01 |
| WASH HANDS | (3.4) | nothing but the ghost finger | **painted exists**: stranded `wash_connected_v1_20261002` 7 frames | JA-NUR-02 |
| FEED drain meter over the bottle; peach slabs | `gesture:3191-3227` | bar gauge, rectangles; the bottle nipple faces away from the mouth | stranded `care_00-07`; empty the painted bottle | JA-NUR-03 / JB-NUR-01 |
| BURP patting hand | `gesture:3366-3384` | a peach disc | stranded care frames, or `ghost_hand.png` | JA-NUR-04 |
| BEDTIME cribs and the blanket the child swipes | `gesture:3334-3356` | teal rectangle over babies who are already swaddled; flat cribs | `assets/flats/castle/dream_house/dream_bed_0..2.png` as reference | JA-NUR-05 / JB-NUR-02 |
| Crib mobile | `opera_nursery_catch.gd:233-239` | strings and dots | **painted exists**: `assets/opera/worlds/props/goal_nursery.png` | JA-NUR-06 |

### Pop Star (C7 1; rhythm redesign in flight in Codex's `popstar-rhythm`)

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| RHYTHM: three singing stars the child taps | `gesture:5974-5999` | ten-point polygons (art never made) | `assets/mg/star.png`, `fx_stolen_sparkle.png` | JA-POP-01 / JB-POP-01 |
| SOUND CHECK mic tilted -0.32 rad and floating; code notes | `gesture:2644-2678` | painted stand mic leaning; circles and lines | — | JA-POP-02 (fix) / JB-POP-02 (notes) |
| ENCORE code sound arcs doubling the painted arcs | `gesture:2501-2510` | arcs | — | JA-POP-03 (remove) |
| DANCE arrows ghosted | `gesture:2741` | 60% alpha | — | JA-SHR-06 |

### Arborist tree-book prototype

The child can reach it from the practice book in the foyer
(`scripts/opera_house_venue_2d.gd:507-528`). The Arborist spray work is in
flight on `codex/arborist-spray-20261015`.

| What the child sees | Where | Now | Item |
|---|---|---|---|
| Flat mint screen, cream panel, hill | `scripts/opera_tree_book_test.gd:330-343` | code | JA-ARB-01 (with that work) |
| Tree choices | `lagoon_tree_bigleaf_maple.png`, `lagoon_tree_pacific_dogwood.png` | no alpha: navy boxes that give the answer away | JA-ARB-02 (cut alpha) |

### Fashion Designer

| What the child sees | Where | Now | Item / brief |
|---|---|---|---|
| Lock, check, pointer and arrow icons | `scripts/fashion_wardrobe.gd:196`, `213-227` | emoji and font glyphs (`MA-TYPE-004`) | JA-FSH-01 / JB-SHR-08 |
| Equip burst | `scripts/wardrobe_ui.gd:161-214` | flat Polygon2D star burst | JA-FSH-02 / JB-SHR-04 |

### Chapter Two story jobs

| What the child sees | Where | Now | Available | Item / brief |
|---|---|---|---|---|
| Candymaker and Detective story props | see Candymaker and Detective above | flat StyleBox props | tray and berries painted | JA-CH2-01 / -02 |
| Cake first stage (Farmer done, Chef not started): tray, empty bowl, shadow | `scripts/chapter_two_giant_cake_2d.gd:512-527`, `555-561`, `596-598` | rounded rectangles and ellipses | **painted exists**: `chef_empty_shell_bowl_v1.png`, `chapter2_candied_strawberries_tray.png`, `sky_lagoon_strawberry_cluster.png` | JA-CH2-03 |
| Table glow slab (710×238) around a ~270×206 painted table | `scripts/chapter_two_party_table_2d.gd:363-369` | flat panel | — | JA-CH2-04 (remove) |
| Rainbow banner forced into a wide slot | `chapter_two_party_table_2d.gd:347-360` | 256×512 shown ~59×118 | — | JA-CH2-05 (fix use) |
| Eleven party hats on the protected friend portraits and Rumi | `scripts/chapter_two_lawn_finale_2d.gd:202-223` | Polygon2D triangles and lines | none; the portraits must not change (`DL-ASSET-03`) | JA-CH2-06 / JB-CH2-03 |
| King's danger zone, safe ring, the "opening" the child taps | `chapter_two_lawn_finale_2d.gd:580-623` | orange polygon, rings, dots | `fx_telegraph_ring.png`, `fx_telegraph_bang.png` as references | JA-CH2-07 / JB-SHR-07 |
| Rainbow protection arcs, Continue chevron | `:568-574` | arcs, flat panel | `castle_banner_motif_rainbow.png` | JA-CH2-08 / JB-SHR-10 |

### Day One cleaning jobs and Grand Puff

| What the child sees | Where | Now | Item / brief |
|---|---|---|---|
| Purple full-frame wash and cracks over the Playroom and Craft room and over Roshan; edge bands and drips over the Bathroom and every cleaned room | `scripts/arena/day_one_castle_grime.gd:39-60`; the Pool is exempt via `day_one_castle_dressing.gd:43`, `296` | code (`MA-VIS-008`). The owner's answer of 2026-10-05: a dirty look only "when dirty objects are specifically being cleaned". | JA-D1-01 (remove) |
| Bathroom guides: aqua arrows and bullseye; the painted soap art stays hidden | `scripts/games/day_one_bathroom_cleaning.gd:68-94`, `day_one_bathroom_toilet.gd:220-223` | code | JA-D1-02 (show the painted guides) |
| Craft room: emoji hand, font-glyph stars, gold rings; grime squashed 2.7-3.6× and tinted | `scripts/day_one_art_studio.gd:173-296`, `240-262`, `542-562` | glyphs and code | JA-D1-03 (`ghost_hand.png`, `fx_stolen_sparkle.png`, fix the grime) |
| Craft finale: flat paint-colour circles on a dark card | `scripts/attack_customizer.gd:72-73`, `185-192` | code | JA-D1-04 / JB-D1-01 |
| Grand Puff dodge warning: flat lilac zone and lane; stretched vortex strip | `scripts/dust_boss_telegraph_2d.gd:104-205` | code polygons | JA-D1-05 / JB-SHR-07 |
| Grand Puff "sparkles": 36 flat-coloured 3D cubes | `scripts/main.gd:7446-7471` (called from `dust_boss.gd:692`, `700`, `1026`) | code, and 3D debt (`MA-2D-002`) | JA-D1-06 (`fx_stolen_sparkle.png`) |

## 5. Layers drawn over every career

| Layer | Where | Now | Recommendation |
|---|---|---|---|
| Spotlight wedges pulsing over all 13 painted rooms | `backdrop:350-361`, called at `:258-263` | two translucent polygons. The comment at `:266-268` says beams "fight the art's own light sources", yet the tile path draws them anyway. | remove (JA-SHR-01) |
| Invitation halo, rotating arc, plus-sparkles | `hotspot:234-283`, `350-363` | circles, arcs, lines | one painted invitation ring family (JB-SHR-02) |
| "Causal backdrop": translucent oval, flat floor stripe, sparkle dots under seven scenes | `gesture:3131-3149` | code | remove (JA-SHR-04) |
| Glow oval and ground stripe under five crank scenes | `gesture:2003-2019` | code | remove (JA-SHR-04) |
| Seven progress pearls; progress dots on cards | `world:2111-2124`; `gesture:4403-4406` and similar | circles | painted pearl progress (JB-SHR-03) |
| Success bursts and curtain-call confetti | `world:3749-3761`, `3974-3983` | ColorRect squares and strips | painted confetti and sparkle family (JB-SHR-04) |
| Finale race bars | `world:1217-1228` | ProgressBars with the engine-default theme | painted bar (JB-SHR-09) |
| Hall HUD: medals, pearls, progress bars, practice/stage icons, status and result panels | `scripts/opera_performance_overlay.gd:110-215` (shown in two-act mode, `world:782-786`) | all code; no painted medal exists anywhere | painted HUD family (JB-SHR-09) |
| Ghost finger demo on every card except SYRUP | `gesture:4290-4296` | circles | `assets/castle/training/ghost_hand.png`, already used by SYRUP (JA-SHR-05) |
| Choice lanes ghosted | `gesture:2741` | painted choices drawn at 60% alpha | full opacity (JA-SHR-06) |
| Ambient "living world" doodles above every career (layer 11) and over the Day One rooms except the Pool | `scripts/living_world_canvas.gd:114-349`: 25 motif kinds, from bubbles and hearts to rockets and gears | code, anchored to the viewport, so they land on the letterbox bars on wide phones | remove from jobs, or a painted motif atlas (owner Q2) |
| Letterbox | `world:1155-1159` | flat navy bars about 160 px each side on 1600×720 | outpaint backdrops later (low) |
| Vector-room fallbacks | `backdrop:364-622` | dead in 13 careers; live for Geologist only | delete after JA-GEO-01 (JA-CLN-01) |

## 6. Painted art drawn badly

These need no new art; each is a fix in code or import.

- **Stretched:**
  - Chef jug, squeezed ~17% (`gesture:6075`).
  - Chef Chapter Two stack cap, ~2.1× wide (`opera_chef_surface.gd:166-177`).
  - Geology fossil SVG (`opera_geology_surface.gd:682-701`).
  - Farmer seed (`gesture:3849-3851`).
  - Painter banner (`gesture:4836`, `hotspot:304-307`) and party-table banner
    (`chapter_two_party_table_2d.gd:347-360`).
  - Racer boost strip (`opera_racer_surface.gd:351`).
  - Nursery pillows (`opera_nursery_catch.gd:243`).
  - Craft-room grime, 2.7-3.6× (`day_one_art_studio.gd:240-248`).
  - Chapter Two magic book, ~23% (`hotspot:304-307`).
- **Covered or ghosted:**
  - Crown lock and cabinet knob under gold slabs (`gesture:3727-3728`,
    `3984-3985`).
  - Farmer piglet under a code face (`gesture:5021-5045`).
  - Nursery bottle under the meter (`gesture:3220-3227`).
  - Choice lanes at 60% (`gesture:2741`).
  - Portal doorway semi-transparent (`gesture:2059-2061`).
  - Boxer stage under a 6% wash (`opera_boxing_surface.gd:616`).
  - Ballet poses under a 44% disc (`opera_ballet_surface.gd:586-588`).
- **Wrong motion or orientation:**
  - Chef whisk spun on its own centre (`gesture:2317-2321`).
  - Pop Star stand mic tilted (`gesture:2657`).
  - Racer kart rear view slid sideways (`gesture:1670-1674`).
  - Magician hats never move (`gesture:5313-5327`).
- **Bad crops or alpha:**
  - Ballet tail cut (`opera_ballet_surface.gd:613-623`).
  - Racer drivers (`opera_racer_surface.gd:385-392`).
  - `fx_bop_puff.png` has opaque frame bars at x≈12 and x 490-498.
  - `widget_magic_cabinet_reveal.png` has a white box round Lamba.
  - The tree-book trees have no alpha.
- **Tinted flat:**
  - Picked Chapter Two strawberries turn purple ghosts (`world:1049-1050`,
    `1068`).
  - Castle star motes are tinted brown or olive
    (`scripts/arena/castle_rooms_25d.gd:4504`, `4884-4890`).
  - Stacked tints in the Pool (`day_one_pool_cleanup.gd:625-656`).
- **Flat-vector PNGs passing as painted:**
  - `widget_catch_nursery_cradle.png`, `widget_catch_nursery_pillows.png`.
  - `widget_target_astronaut_piece_0..2.png`.
  - `widget_target_boxer_mark.png`, `widget_lanes_shared_pick.png`.
  - `widget_basin_doctor_bubbles.png`, `widget_basin_shared_shine.png`.
  - `assets/kart/boost_ribbon.png`.

## 7. Why the art keeps not reaching the game

1. **The written rules still say "reuse first, generate only for a named
   gap".** `DL-ASSET-01`, `DL-ASSET-02` and `DL-ASSET-06` in
   `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`, and the "Art reuse and
   generation budget" section of `AGENTS.md` on `dev`, still say this.
   - The owner removed that restriction on 2026-10-17. The new text exists
     only as an uncommitted edit in the main checkout and in rescue snapshot
     `e3aefde2`.
   - The code shows the old rule at work, for example:
     - the Boxer glove comment (`opera_boxing_surface.gd:776-777`);
     - the Geologist comment keeping "approved vectors" as runtime authority
       (`opera_geology_surface.gd:40-41`);
     - the 2026-09-05 Geologist manifest recording "No budget spent on
       further identical retries".
2. **Finished art was left on topic branches.** Examples:
   - `codex/job-art-review-v2-20261001` is 55 commits ahead of `dev` and 139
     behind, with 40 painted job images;
   - the Racer and Astronaut branches.
3. **The flat-vector program measures far more than it changes.** Codex's
   canonical branch `codex/flat-vector-r6-20261012` has 243 non-merge
   commits since 2026-10-12.
   - Only 3 of them change `scripts/`, `assets/` or `scenes/`, and none of
     the three is job art (two startup-menu retirements and one geode clamp
     fix).
   - Its own tally at revision R100 reads replaced 0, integrated 0, accepted
     removals 0, against 224 named items (128 still "needs context review").
   - Two partial integrations reached `dev`: the Critter Book frames
     (CHG-096) and the insect tab (CHG-099). Neither is a job game.
   - It is now generating a new Geologist mineral while
     `painted_work_v1/mineral.png` sits finished on the stranded branch.
4. **Fallback code hides missing art.** Most surfaces draw a code shape when
   a texture is missing. Missing pipe tiles, star notes and portal rings
   therefore never failed a check.

## 8. What this audit does not establish

- No item has been seen on the phone or by the owner; all visual judgements
  come from code and source images. `DL-VIS-07` reserves a top score for the
  owner in runtime context.
- **By-eye verdicts cover only the files named in 3.1.** The other stranded
  frames of the same families (other geode states, wet river tiles,
  care_01-07, other wash frames, moto and truck views) were not viewed. They
  need Codex's in-context check.
- **Counts of code drawing measure source call sites, not on-screen
  pixels.** The overdraw meter (`tools/measure_overdraw.py`) measures what is
  drawn.
