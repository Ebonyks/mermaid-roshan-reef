# ImageGen briefs for the job games (written descriptions for Codex)

Claude describes each picture in words; Codex builds every image (CLAUDE.md,
"Codex handoffs: Claude writes, Codex builds images"). Each brief names the
code it replaces, what the child sees change, the states needed, the canvas,
the references to bind and the checks that close it. Item IDs (`JA-…`) refer
to [data/job_art_register.json](data/job_art_register.json); evidence is in
[AUDIT.md](AUDIT.md).

## 0. Rules for every brief

**Choosing the method.** The owner's decision of 2026-10-17 (the "Art quality
and ImageGen" text, see README) sets the order:

1. Use ImageGen when it is the right tool. Owner, to Codex, 2026-10-17: "use
   image-gen 2.5 when art is sub optimal". Record the provider and model
   revision that actually returned; do not invent a label.
2. Reuse existing painted art only where it meets the brief. No proof of a
   failed reuse is required.
3. Never replace a painted object with code-drawn shapes to avoid generation.

**C1 Style.** The pastel toy-playset storybook finish (`DL-VIS-01` to
`DL-VIS-05`):
- rounded, slightly handmade masses;
- two or three broad painted value bands per form, no PBR noise or
  photographic texture;
- clean deep-indigo, plum or warm-brown contours, about 2-4 px at the size
  the object is shown, with 1-2 px interior marks;
- aqua and lavender shadows, high-key values, light from the upper left;
- warm colour only where the child should act.

Match the style anchors in section 0.1. A metallic, neon, glossy-icon or
realistic finish fails. Two stranded examples fail for this reason: the brass
`astronaut_gear_v1.png` and the full-bleed neon `astronaut_radioactive_fluid_v1.png`.

**C2 Cutouts.**
- Transparent RGBA with no baked checkerboard, no white sticker rim, no
  cast shadow outside the object and no baked glow or halo. Effects are
  separate files.
- Run `python -B docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py`
  and add the file to a `--branch` run, or call `cutout_profile` on it. It
  must report `CUTOUT_OK`.
- Keep about 8% transparent margin on every side.

**C3 Size.**
- At most 1024 px on the longest side, or a power of two (`DL-PERF-04`).
- Objects shown under 300 px on the 1280×720 canvas use a 512² canvas.
- Room backdrops are 2×2 tiles of 1024², the same layout as `world_<career>_c{0,1}r{0,1}.png`.

**C4 No words.** No letters, digits or symbols that read as instructions
(`DL-READ-04`).

**C5 States.** Where an object changes (empty, filling or full; closed,
cracking or open), deliver every state as a whole picture on the same canvas
with the same registration, so they swap without drifting (`DL-INT-03`; owner
`ODR-SPRITE-WHOLE-UNIT-20261007`, "sprites need to be drawn whole, as a single
unit"). Code may not cross-fade two copies or draw parts of the object.

**C6 Identity.** Roshan:
- Bind `assets/characters/roshan_25d/roshan_base.png` for identity and name
  the tail light state of the exemplar (`ODR-ROSHAN-IDENTITY`,
  `ODR-ROSHAN-IRIDESCENT`, `ODR-ROSHAN-Q12`).
- Inside a career, the costume comes from that career's atlas
  `assets/opera/worlds/actors/animation/roshan_<career>_sheet_a.png`.
- New art follows the base-world child (`ODR-ROSHAN-Q13`).
- Never bind `assets/characters/roshan_sprite.png`.

Protected art:
- Never alter `assets/characters/friends/`, `assets/book/` or family voices
  (`DL-ASSET-03`).
- New layers may sit beside or over them only as separate files.

**C7 Provenance.**
- Keep the prompt, the inputs with their SHA-256, the takes (default two per
  brief, owner animation-cap rules aside), the rejects and the hashes under
  `assets_src/imagegen/<brief-id>_<date>/`.
- Add an `ASSET_LICENSES.md` row in the same commit (`DL-ASSET-04`).

**C8 Context check.** Before integration, Codex captures the phase at 1280×720
and 1600×720 with the HUD and checks the art against its room for:
- contour, palette, light, perspective and scale;
- contact, occlusion and readability at phone size (`DL-READ-02`).

These captures are review evidence only. Acceptance stays with the owner
(`DL-VIS-07`).

**C9 No flat fallback.**
- When the painted file lands, delete the code drawing it replaces, including
  the `if texture == null` fallback.
- Make the load fail loudly in the job's probe instead.
- Hit areas and touch geometry stay as they are.

**C10 One branch per job batch.**
- Integrate the job's briefs and register items together.
- Write one impact record, run green CI and merge to `dev`.
- Re-run the measurement tool: the job's primitive draw count must fall.

### 0.1 Style anchors (approved runtime art)

| Anchor | Path | SHA-256 |
|---|---|---|
| A1 painted prop finish | `assets/opera/worlds/props/goal_chef.png` (512²) | `cb28da49b252769ef143d75ddb890d2350cebf6e12aca33a875c88b04ff33467` |
| A2 painted furniture finish | `assets/opera/worlds/widgets/widget_magic_cabinet_closed.png` (512²) | `f0829a82157b1e1671fdca165dac68a8385645d648ec77604287e95a59796fcf` |
| A3 character-prop finish | `assets/opera/worlds/widgets/widget_crank_doctor_patient.png` (512²) | `ecf354fd812decbae250078cc2dc7bce8b8bb5c403afe5016bdabedbe0c8ffc9` |
| A4 soft pastel prop finish | `assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png` on `codex/job-art-review-v2-20261001` (`cfcadc96`) | `22c9fecd42db41e0f138749ff2468b2f76a8ca1ef6b305ab4afbcfe785d8a96e` |
| A5 Roshan identity | `assets/characters/roshan_25d/roshan_base.png` | `69827625a8a795f1303c90a465454dd8529f10d5401c78911d00b90be8d1e1ab` |
| A6 guide hand | `assets/castle/training/ghost_hand.png` | `e484d14899d8137448128314536132dbd16f970cb1f0fabea006e9d51b5435b9` |

The room palette for each career comes from its backdrop tile
`assets/opera/worlds/backdrops/world_<career>_c0r0.png`; the hashes are in
`data/job_art_register.json`.

**Design references.** These are the prop cards in
`assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`, July concept cells
on navy that were upscaled from about 256 px.
- Use them for what the object is and how it reads, never as pixels.
- Never use the cards that show Roshan: they were bound to the retired
  `roshan_sprite.png`.

## 1. Geologist

### JB-GEO-01 Geology grotto backdrop (register JA-GEO-01)

**Replaces.** The code room at `backdrop:274-284` and `587-622`: navy sky,
ground band, hill, strata polylines and crystal shapes. It is the only career
without a painted room.

**What the child sees.** A painted underwater grotto replaces the flat shapes.
The four stations sit in it, left to right:
- a stepped stone spring with a small pool (RIVER);
- a broad pale stone work dais (FOSSIL);
- a shell-rimmed washing basin (PAN);
- a crystal cave arch (GEODE).

**Picture.** Use the composition of
`assets_src/geologist_rebuild_2026-09-05/geology_grotto_candidate.png`
(sha256 `e60684278d33e43a51eea3534b99aa8c70e90b2ef3f11004f4d04154273fbd4b`)
as the image input, keeping its layout, stations, pale sandy floor and
lavender rock arches.
- Leave the floor between stations open and quiet: low detail and lower
  saturation than the props (`DL-READ-01`).
- Keep the water light gentle. The sunbeams must not become strong stripes
  across the walk band.

**Deliver.**
- `assets/opera/worlds/backdrops/world_geologist_c{0,1}r{0,1}.png`, 4 tiles
  of 1024² cut from one 2048×2048 master, the same layout as the other
  careers.
- Keep the master in `assets_src`.
- Stations stay painted into the room only as surroundings. The objects the
  child touches remain separate cutouts (`DL-LAY-03`, `DL-LAY-05`).

**Curtain call.** Reuse the shared `assets/opera/worlds/stage/finale_stage_c*r*.png`
instead of the vector proscenium at `backdrop:319-347`.

**Done when:**
- `backdrop.gd` loads the tiles;
- the vector room and proscenium code paths are deleted (JA-CLN-01);
- captures show the walk band clear and the four stations where
  `scripts/opera_stage_paths.gd` places them.

### JB-GEO-02 Geologist crest (JA-GEO-08)

**Replaces.** `assets/opera/worlds/ui/crests/opera_crest_geologist.svg`. It is
byte-identical to `goal_geologist.svg`: five flat paths.

**Picture.** A round painted crest medallion in the family of the other
256² crests (for example `assets/opera/worlds/ui/crests/opera_crest_chef.png`,
sha256 `55ab3093ca9f7e9df0bfb5011980727b140648ce0f10974c6ee8392928f77288`).
Centre it on one aqua-and-lilac crystal cluster with a small ammonite.

**Deliver.** `opera_crest_geologist.png`, 256² RGBA. Change
`scripts/castle_career_routes.gd:48` to load it and delete the SVG.

### Stranded art to wire, no generation (JA-GEO-02 to JA-GEO-07)

From `codex/job-art-review-v2-20261001` (`cfcadc96`; full hashes in the
register):

| Stranded files | Replace |
|---|---|
| `painted_work_v1_20261001/work_slab.png` | the code tray |
| `fossil_soil.png` and `fossil.png` | the dirt grid and the stretched SVG fossil |
| `pan.png`, `grain.png` and `mineral.png` | the code pan. Set `PAN_PATH`. |
| `painted_geode_v1_20261001/*` or the `coherent_geode_v1_20261002` six-state sheet | the code geode. Set `GEODE_PATH`. The six-state sheet is preferred because it opens in registered steps. |
| `painted_river_v1_20261002/*` | the river cells |
| `layered_rock.png`, `fossil.png` and `mineral.png` | the three hotspot and goal SVGs |

Coordinate the pan with Codex's in-flight `codex/flat-vector-geologist-pan-runtime-20261017`.
- Keep whichever pan the owner prefers in context.
- Do not ship two pan designs.

## 2. Teacher

The whole lesson is code (`opera_teacher_surface.gd:263-420`). Bind the
library tile `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c0.png`
(sha256 `d42f48eeb5d0177e1316043eee94e1a096614f45e1f42ce7205ecd573b4c4e74`)
for palette. Everything sits in that painted library.

### JB-TEA-01 Lesson board (JA-TEA-01, JA-TEA-06)

**Picture.** A wide easel board: a cream slate in a pale wood frame with
small shell corners and two stubby legs. It must stand in the library, not
float over it.

**Deliver two files:**
- `assets/opera/worlds/teacher/lesson_board.png`, 1024×676 or 1024×768,
  with an empty face where the shapes will sit;
- `assets/opera/worlds/hotspots/teacher_lesson_board.png`, 512², the same
  board small and closed, for the walk-up hotspot and goal prop. It replaces
  the SVG at `catalog:48-51` and `world:449`.

### JB-TEA-02 Shape tiles (JA-TEA-02)

**Picture.** Five chunky painted toy shapes, like wooden or shell blocks:
circle (teal pearl disc), triangle (coral), square (lilac), star (gold),
heart (pink). Each needs two states: rest, and lit with a soft rim of light
painted inside the contour, not a halo.

**Also.** One empty "missing piece" slot: a recessed shell outline in the
board material.

**Deliver.** `assets/opera/worlds/teacher/shape_<name>_{rest,lit}.png` and
`shape_slot.png`, each 256².

### JB-TEA-03 Counting pearls and trays (JA-TEA-03)

**Picture:**
- a pearl in two states: uncounted (pearly cream) and counted (cream with a
  painted gold shine and a small check-shaped shell mark, not a written tick);
- two shallow shell trays, aqua and pink, that hold up to six pearls;
- a round "join" shell button showing two pearls coming together. Do not
  use a "+" glyph (`DL-READ-04`).

**Deliver.** `pearl_{uncounted,counted}.png` at 128², `tray_{aqua,pink}.png`
at 512×384, `join_shell.png` at 256².

### JB-TEA-04 Answer cards (JA-TEA-04)

**Picture.** A cream shell-edged card that holds a shape or a pearl group,
in three states: rest, chosen (lilac rim) and right (gold rim with small
painted sparkles inside the card edge).

**Deliver.** `answer_card_{rest,chosen,right}.png`, 512².

### JB-TEA-05 Teacher crest (JA-TEA-07)

**Picture.** A 256² crest medallion like JB-GEO-02 with a small slate and
three pearls.

**Deliver.** `opera_crest_teacher.png`, replacing the Roshan sprite at
`scripts/castle_career_routes.gd:49`.

The hint button and the demo use the guide hand A6, so no new art is needed
for them. For the lesson panels:
- Remove the StyleBox board at `:266-267`.
- Keep `teacher_lesson_plan.gd` geometry unchanged so the answers stay where
  the voice expects them.

## 3. Astronaut

### JB-AST-01 Pipe board set (JA-AST-01, JA-AST-03)

**Replaces.** The code tiles, plates, tank and intake at `gesture:5816-5900`.
The code already asks for these exact files (`gesture:708-722`).

**Picture.** Chunky toy pipes in teal glass, with cream-gold shell collars
and two rivets per collar.
- Pipe arms run from the centre of the tile to the middle of each edge,
  ending in an open mouth so orientation reads without words.
- Light must work under rotation. Use soft top light, or paint each
  orientation separately; never rotate a lit tile in code.
- A fuelled state is a second picture with the glass filled with sparkly
  aqua fuel. It replaces the code tint double draw at `gesture:5820-5822`.
- The tank is a round bubble tank on a small pedestal. The intake is a
  rocket port ring.
- Optional: a grid plate as one soft stone tile, if the plates stay at all.

**Design references.** These cards are references only:
`opera_job_astronaut_engineer_gameplay_{elbow_pipe,straight_pipe,ring_pipe,bubble_tank,elbow_fitted,straight_ghost_slot}.png`.
The stranded `astronaut_pipe_straight_candidate_v1.png` is a style reference;
paint softer and less glossy than it.

**Deliver** in `assets/opera/worlds/widgets/`:
- `widget_pipe_{tile_h,tile_v,elbow_ne,elbow_nw,elbow_se,elbow_sw}.png` and
  the `_fueled` variant of each, 256²;
- `widget_pipe_tank.png` and `widget_pipe_intake.png`, 256².

### JB-AST-02 Napping imp (JA-AST-02)

**Picture.** The mischief imp from `assets/opera/worlds/actors/imp_mischief.png`,
curled up asleep with closed eyes and small painted "z" bubbles. The bubbles
are round shapes, not letters.

**Deliver.** `assets/opera/worlds/actors/imp_mischief_napping.png`, 256².

### JB-AST-03 Patch pieces (JA-AST-04)

**Replaces.** `widget_target_astronaut_piece_0..2.png`, which are flat fills.

**Picture.** Three painted rocket patches: a rounded square plate, a round
plate and a star-shaped plate. Each has soft metal value bands in pastel
coral, lilac and teal, with rivets.

**Deliver.** Three files at 256², the same names, replacing the old ones.

### JB-AST-04 Launch flame and exhaust (JA-AST-05)

**Replaces.** The orange triangle and circles at `gesture:2599-2627`.

**Picture.** A soft storybook rocket flame in four growth states, small to
full. The flame is pale gold at the core, coral at the edge and rounded, not
spiky. Separate puffy exhaust clouds in cream and lilac.

**Deliver.** `widget_launch_flame_{0..3}.png` at 256×512, and
`widget_launch_cloud.png` at 256².

## 4. Chef (`MA-OPERA-001`)

### JB-CHF-01 Oven, three states (JA-CHF-01)

**Replaces.** The brown rectangles at `gesture:5358-5426`.

**Picture.** A rounded storybook oven in the kitchen palette (bind
`world_chef_c0r0.png`), with a big round window and a shell-handled door. The
door handle must be large and obvious because it is the tap target.

States:
1. closed, cool, window dim;
2. closed, warm, a golden glow inside the window;
3. open, door down.

The cake inside is a separate cutout layer. Use the painted
`widget_gauge_chef_success.png`, which is already loaded and never drawn, for
the done state, and a raw-batter version for the start. The rise is shown by
swapping pictures, not by code shapes.

**Design references.** `opera_job_pastry_chef_gameplay_oven_closed.png` and
`_oven_open.png`; the oven in the retired `widget_gauge_chef.png`.

**Deliver.** `widget_oven_chef_{cool,warm,open}.png` at 512², and
`widget_oven_cake_{raw,risen}.png` at 256².

### JB-CHF-02 Frosting stroke (JA-CHF-07)

**Replaces.** The polyline frosting at `gesture:1855-1866`.

**Picture.** A pink piped-frosting ribbon tile that repeats along a path,
drawn as stamped painted segments. Add a start cap and an end cap.

**Pair it with:**
- the painted Chapter Two cakes `chapter2_chef_stacked_unfrosted_cake.png`
  and `chapter2_chef_frosted_rainbow_cake.png`, which replace the rectangle
  cake;
- the piping bag cut from the retired `widget_trace_chef.png`.

**Deliver.** `widget_frosting_{segment,cap_start,cap_end}.png`, 128².

### JB-CHF-03 Chocolate topping (JA-CHF-08)

**Replaces.** `widget_target_chef_piece_2.png`, which reads like a poop
emoji.

**Picture.** A chocolate-dipped strawberry or a chocolate shell curl, clearly
food.

**Deliver.** Replace the file at the same size.

Most of the Chef can be fixed without generation:
- bowl and batter from Chapter Two art (JA-CHF-02, JA-CHF-05);
- jug aspect and emptying (JA-CHF-04);
- whisk pivot at its handle (JA-CHF-06);
- the stack cap warp (JA-CHF-09).

## 5. Candymaker

### JB-CDY-01 Wrapper twist (JA-CDY-02)

**Picture.** The wrapped candy from `widget_crank_candymaker_mover.png` in
four twist states, untwisted to fully twisted. Each state is a whole picture
(C5).

**Deliver.** `widget_wrap_candy_{0..3}.png`, 256².

### JB-CDY-02 Waving sea friends for SHARE (JA-CDY-03; owner Q4)

**Replaces.** The six stick figures at `gesture:2988-3014`.

**Picture.** Six small painted sea friends: a seahorse, a pufferfish, a crab,
a turtle, an octopus and a starfish. They are new characters, in the finish
of A3. Each has two states: waving with an open fin or claw, and holding a
candy with a happy face. They must not copy or alter the protected friend
portraits.

**Deliver.** `assets/opera/worlds/actors/candy_friend_<name>_{wave,happy}.png`,
256².

Two Candymaker items are in flight in Codex's `candymaker-boxes-friends-20261017`:
SORT (JA-CDY-01) and the sort boxes. Finish them there.

## 6. Doctor

### JB-DOC-01 Wash basin and hands (JA-DOC-01)

**Replaces.** The ovals and lines at `gesture:2770-2797`.

**Picture.** A shell sink with a pearl faucet, painted water in three states
(off, running, foamy) and painted bubbles. Roshan's hands washing are drawn
in the nursery wash style of the stranded `wash_connected_v1_20261002` frames,
in the Doctor costume.

**Design references.** The sink in the retired `widget_basin_doctor.png`.
For hand anatomy and the career design, the stranded `wash_connected_v1_20261002/ready.png`
(sha256 `a4145ed7673b937f49a54e4ebd0fb02efe1b2c4bd76315f325948a8f33740cd8`).

**Deliver.** `widget_basin_doctor_{off,running,foamy}.png` at 512², and
`widget_hands_doctor_{0..3}.png` at 512² (a scrub loop).

### JB-DOC-02 X-ray scanner (JA-DOC-03)

**Replaces.** The cyan rectangle at `gesture:4396-4409`.

**Picture.** A handheld round shell scanner with a glowing pale-aqua glass
plate. Use the painted machine `widget_target_doctor_mover.png` as a family
reference.

**Deliver.** `widget_xray_scanner_{idle,found}.png`, 256².

### JB-DOC-03 Cast and bandage on the starfish (JA-DOC-04, JA-DOC-05)

**Replaces.** The cast lines, the cushion ovals and the brown blob patient.

**Picture.** The approved starfish patient `widget_crank_doctor_patient.png`
(A3), in this order:
- for CAST, the starfish on a clamshell cushion with a soft cream cast
  appearing in three steps;
- for BANDAGE, the same starfish with a stretchy bandage wrapping in three
  steps.

**Design references.** `opera_job_doctor_gameplay_bandage_roll.png` and
`_bandage_wrap.png`.

**Deliver.** `widget_cast_doctor_{0..3}.png` and `widget_bandage_doctor_{0..3}.png`,
512².

## 7. Farmer

### JB-FRM-01 Seed bed and sprouts (JA-FRM-01)

**Replaces.** The flat brown rectangle and stick sprouts at `gesture:3823-3845`.

**Picture.** A painted raised seed bed with five planting holes that matches
the tilled bed in the farmer room (`world_farmer` tiles,
`scripts/opera_stage_paths.gd:113`). Each hole has these states:
1. empty;
2. seed in;
3. sprout;
4. small flower (a different pastel flower in each hole).

**Deliver.** `widget_seed_bed.png` at 1024×512, and
`widget_sprout_{seed,sprout,flower_0..4}.png` at 128².

### JB-FRM-02 Piglet munch (JA-FRM-02)

**Replaces.** The pink code face stamped over the painted piglet at
`gesture:5021-5045`.

**Picture.** The piglet from `widget_target_farmer_mover.png` in three
whole-body states: open-mouth catch, chewing with cheeks puffed, and happy
with eyes closed. Use the same registration as the mover.

**Deliver.** `widget_target_farmer_mover_{catch,chew,happy}.png`.

### JB-FRM-03 Barn gate (JA-FRM-04)

**Replaces.** The lines and arc at `gesture:1631-1655`.

**Picture.** A painted barn gate matching the barn doors in the farmer room
(`opera_stage_paths.gd:110`), in two states: closed and swung open.

**Deliver.** `widget_barn_gate_{closed,open}.png`, 512².

## 8. Magician

### JB-MAG-01 Star portal (JA-MAG-02)

**Replaces.** The code arcs and dots at `gesture:2040-2096`. The code already
asks for this ring art (`gesture:657-677`).

**Picture.** A round swirling portal of lilac and aqua starry mist with a
gold shell rim. Deliver four opening states, closed to open, as whole
pictures; the overlay sparkle is separate.

**Deliver.** `widget_portal_magician_ring_{0..3}.png` at 512², and
`widget_portal_magician_overlay.png` at 512².

## 9. Painter

### JB-PNT-01 Cloudy cover (JA-PNT-01)

**Replaces.** The grid of up to 60 flat squares at `gesture:4844-4852`.

**Picture.** Soft painted cloud puffs that sit over the sunrise painting and
melt away in patches. Use `assets/opera/worlds/props/fx_dust_puff.png` as the
family reference. Deliver a set of six puffs that tile irregularly over the
canvas.

**Deliver.** `widget_paint_cloud_{0..5}.png`, 256².

## 10. Ballerina

### JB-BAL-01 Pearl-mirror shell frame (JA-BAL-01)

**Replaces.** The petal circles at `opera_ballet_surface.gd:592-610`.

**Picture.** A scalloped coral and cream shell frame with an open pearly
centre that holds a pose portrait. Three states: rest, chosen and right.

**Design reference.** `opera_job_ballerina_gameplay_coral_shell_tile.png`.

**Deliver.** `assets/opera/worlds/ballet/shell_frame_{rest,chosen,right}.png`,
512².

### JB-BAL-02 Ribbon trail and twirl ring (JA-BAL-02, JA-BAL-03)

**Replaces.** The line passes and circles at `:639-717`.

**Picture:**
- a satin rainbow ribbon segment that repeats along a curve, with start and
  end caps;
- a pearl the child drags;
- for the twirl, a round shell track ring with a painted pearl handle.

**Design reference.** `opera_job_ballerina_gameplay_twirl_ribbon.png`.

**Deliver.** `ribbon_{segment,cap_start,cap_end}.png` at 128²,
`pearl_handle.png` at 128², and `twirl_ring.png` at 512².

## 11. Racer

### JB-RAC-01 Race controls (JA-RAC-01, JA-RAC-02, JA-RAC-04)

**Replaces.** The StyleBox pill, chevrons, knob, turbo circle and lightning
polygon at `opera_racer_surface.gd:87-91` and `420-469`, and the flat
`assets/kart/boost_ribbon.png`.

**Picture:**
- a painted shell steering wheel the child slides left and right;
- a big round coral turbo button, in two states: ready (glowing) and
  recharging (dim with a painted fill level);
- start lights as three pearl lamps: off, lit and go;
- a zoom strip as soft aqua chevron ripples painted on the road. These are
  ripples, not arrows with text.

**Design references.** `opera_job_racecar_driver_gameplay_{steering_wheel,turbo_button,zoom_strip_active}.png`.

**Deliver.** `assets/kart/ui/steering_wheel.png` at 256², `turbo_{ready,recharge}.png`
at 256², `start_lamp_{off,lit,go}.png` at 128², and `zoom_strip.png` at
512×128.

## 12. Nursery

Wire the stranded art first:
- `refinement_v1/cradle.png` and `pillows.png` replace the flat
  `widget_catch_nursery_cradle.png` and `_pillows.png`;
- `wash_connected_v1_20261002/*` gives WASH HANDS a picture;
- `refinement_v2/care_00..07` covers FEED and BURP.

Owner Q3 covers their design.

### JB-NUR-01 Bottle states (JA-NUR-03)

**Replaces.** The drain meter at `gesture:3220-3227`.

**Picture.** The painted bottle `widget_pour_nursery_mover.png` in three fill
states: full, half and empty. The nipple must point toward the baby when
tilted.

**Deliver.** `widget_pour_nursery_mover_{full,half,empty}.png`.

### JB-NUR-02 Cribs and blanket (JA-NUR-05)

**Replaces.** The rectangles at `gesture:3334-3356`.

**Picture.** A round painted moon crib matching the moon bed in the nursery
room (`opera_stage_paths.gd:190`). Use `assets/flats/castle/dream_house/dream_bed_0.png`
as the reference.

The quilt the child swipes down has three states: folded at the foot, half
over and tucked. The babies under it stay the painted `baby_0..2.png`.

**Deliver.** `widget_nursery_crib.png` at 512², and
`widget_nursery_quilt_{folded,half,tucked}.png` at 512×256.

## 13. Pop Star (rhythm redesign in flight in Codex's `popstar-rhythm-20261017`)

### JB-POP-01 Singing stars (JA-POP-01)

**Replaces.** The ten-point polygons at `gesture:5974-5999`. The code already
asks for these files (`gesture:723-725`).

**Picture.** Three plump painted stars with soft faces, in gold, pink and
aqua. Each has two states: unlit (pastel and quiet) and lit (bright with an
open singing mouth). Light is painted inside the contour.

**Deliver.** `popstar_star_note_{unlit,lit}_{gold,pink,aqua}.png`, 256².
The current code tints one pair (`gesture:5977`), so either draw three
colours or change the code to pick by colour.

If the rhythm redesign removes the stars, close this brief as not needed.

### JB-POP-02 Music notes (JA-POP-02)

**Replaces.** The circle-and-line notes at `gesture:2667-2678` and
`2501-2510`.

**Picture.** Four painted pastel music notes, rounded and toy-like, in two
sizes.

**Deliver.** `assets/opera/worlds/props/fx_music_note_{0..3}.png`, 128².

## 14. Chapter Two story jobs

### JB-CH2-01 Strawberry candy station (JA-CH2-01)

**Replaces.** The flat StyleBox pitcher, stream, lane boxes, crank disc and
trays at `world:2164-2253`.

**Picture:**
- a small painted syrup pitcher;
- a glaze swirl crank shaped like a spoon in a bowl, in four states;
- three painted sorting baskets for small, middle and big strawberries.

Use the painted tray `assets/chapter2/birthday/chapter2_candied_strawberries_tray.png`
(already shipped) and `sky_lagoon_strawberry_single.png` as given; do not
redraw them.

**Deliver.** In `assets/chapter2/birthday/`: `ch2_syrup_pitcher.png` at 512²,
`ch2_glaze_bowl_{0..3}.png` at 512², and `ch2_berry_basket_{small,middle,big}.png`
at 256².

### JB-CH2-02 Magic storybook spread (JA-CH2-02)

**Replaces.** The lavender rectangle with dots at `world:2272-2285`.

**Picture.** An open storybook spread with soft page curls and painted
pictures of the birthday plan on the pages, with no text. Two states: closed
and open.

**Deliver.** `ch2_storybook_{closed,open}.png`, 1024×640.

### JB-CH2-03 Party hats (JA-CH2-06)

**Replaces.** Eleven Polygon2D triangles at `chapter_two_lawn_finale_2d.gd:202-223`.

**Picture.** Three painted cone party hats (striped pastel, polka-dot,
shell-topped), each with a soft pom-pom. They are separate cutouts placed on
the protected portraits; the portraits are never edited.

**Deliver.** `ch2_party_hat_{0..2}.png`, 256².

## 15. Day One

### JB-D1-01 Paint pots for the craft finale (JA-D1-04)

**Replaces.** The flat colour circles at `scripts/attack_customizer.gd:185-192`.

**Picture.** Five painted paint pots: red, orange, yellow, aqua and lilac.
They match `assets/castle/day_one_art_studio/paint_bottle_pink.png` and
`paint_bottle_blue.png`. Two states: rest and chosen.

**Deliver.** `assets/castle/day_one_art_studio/paint_pot_<colour>_{rest,chosen}.png`,
256².

## 16. Shared families

### JB-SHR-01 Ambient motifs (owner Q2 only)

Only if the owner keeps ambient motifs in jobs. Paint the motif set of
`scripts/living_world_canvas.gd:114-349` (bubble, leaf, flower, fish,
butterfly, note, heart, shell, star and the rest) as a 128² atlas.

Default: remove the motifs from job scenes instead (JA-SHR-07).

### JB-SHR-02 Invitation ring (JA-SHR-02, JA-BOX-03)

**Replaces:**
- the halo, rotating arc and plus-sparkles at `hotspot:234-283` and `350-363`;
- the flat `widget_target_boxer_mark.png` and `widget_lanes_shared_pick.png`;
- the code drop-target markers at `gesture:3065-3096`.

**Picture.** A soft pearl-and-gold ring of light that lies on the ground under
an object. Four breathing frames and one "opening" burst frame. It sits under
the object and never over it.

**Deliver.** `assets/opera/worlds/props/fx_invite_ring_{0..3}.png` and
`fx_invite_open.png`, 256².

### JB-SHR-03 Pearl progress (JA-SHR-03, JA-RAC-03, JA-BOX-04)

**Replaces.** The progress pearls at `world:2111-2124`, the card progress dots
and the boxer round lights.

**Picture.** A pearl in three states: empty (a pale shell dimple), filling and
full (lustrous cream with a gold glint). Add a collectible track pearl for the
Racer.

**Deliver.** `assets/ui/pearl_{empty,filling,full}.png` and
`pearl_collectible.png`, 128².

### JB-SHR-04 Celebration (JA-SHR-08, JA-FSH-02)

**Replaces.** The ColorRect burst squares at `world:3749-3761`, the confetti
strips at `world:3974-3983` and the Fashion equip burst at
`wardrobe_ui.gd:161-214`.

**Picture.** Painted confetti ribbons and shell sequins (eight pieces) and a
three-frame sparkle burst, in the family of `fx_stolen_sparkle.png`.

**Deliver.** `assets/opera/worlds/props/fx_confetti_{0..7}.png` at 64², and
`fx_sparkle_burst_{0..2}.png` at 256².

Also fix the crop of `fx_bop_puff.png` (its opaque bars at x≈12 and x 490-498).

### JB-SHR-05 Pour streams (JA-CHF-03, JA-CDY-04)

**Replaces.** The code streams, beads and splashes at `gesture:6200-6222` and
`6281-6296`.

**Picture.** A painted liquid stream segment and a splash, in three liquids:
batter (cream-gold), syrup (rose-amber) and water (pale aqua). Each has a
start lip, a repeating body, an end splash and three bead drops.

**Deliver.** `assets/opera/worlds/props/fx_stream_<liquid>_{lip,body,splash,bead}.png`,
128² (body 128×256).

### JB-SHR-06 Guide-hand poses (JA-SHR-05, JA-NUR-04)

**Picture.** The approved guide hand A6 in two more poses: an open patting
hand and a pinch-and-drag hand. Same finish and outline as A6.

**Deliver.** `assets/castle/training/ghost_hand_{pat,drag}.png`, 512².

### JB-SHR-07 Danger and safe ground marks (JA-CH2-07, JA-D1-05)

**Replaces.** The flat lilac and orange polygons at `dust_boss_telegraph_2d.gd:145-167`
and `chapter_two_lawn_finale_2d.gd:580-623`.

**Picture:**
- a soft painted dust-storm patch for "move away", in lilac and grey with
  swirling dust, that scales to an ellipse;
- a pearl-ringed safe spot for "come here";
- a gold "opening" target ring.

Use `fx_telegraph_ring.png` (sha256 `12077afe02fa842d7e257d22110cc64df13a63510d2cd8c86fd4c7a06062572e`)
as the family reference.

**Deliver.** `fx_danger_patch.png` at 512×256, `fx_safe_spot.png` at 256²,
and `fx_opening_ring.png` at 256².

### JB-SHR-08 Small UI icons (JA-FSH-01, `MA-TYPE-004`)

**Replaces.** The 🔒 ✔ 👇 ◀ ▶ glyphs at `fashion_wardrobe.gd:196` and
`213-227`.

**Picture.** Painted shell lock, painted gold check-shell and two pearl arrow
buttons. The pointer uses A6.

**Deliver.** `assets/ui/icons/{lock,check,arrow_left,arrow_right}.png`, 128².

### JB-SHR-09 Hall HUD (JA-SHR-09)

**Replaces.** Everything drawn in code by `opera_performance_overlay.gd:110-215`:
- bronze, silver and gold medals with ribbons;
- the practice-book and stage-curtain icons;
- the status pill and result card;
- the progress bars.

It also replaces the default ProgressBars at `world:1217-1228`.

**Picture:**
- three painted shell medals with ribbons;
- a small painted open book and a small painted curtain;
- a cream shell-edged status pill frame and result card frame;
- a painted pearl-bead progress bar frame and fill.

**Deliver** in `assets/ui/hall/`:
- `medal_{bronze,silver,gold}.png` at 256²;
- `icon_{practice,stage}.png` at 128²;
- `panel_{status,result}.png` as 9-slice friendly 512² frames;
- `bar_{frame,fill}.png` at 512×64.

### JB-SHR-10 Storybook UI frames (JA-CH2-08, JA-SHR-10)

**Replaces.** The flat panel and chevron Continue button at
`chapter_two_lawn_finale_2d.gd:568-571`, and the Teacher caption box at
`world:1305-1315`.

**Picture.** A painted shell "next" button with a pearl arrow (no glyph) and
a soft paper caption frame, in the existing Storybook UI grammar (`DL-UI-06`).

**Deliver.** `assets/ui/storybook_next.png` at 256², and
`assets/ui/caption_frame.png` at 1024×128, 9-slice friendly.
