# Codex handoff — diegetic minigame widget art (2026-08-02)

**Audience:** Codex — image generation + deterministic promotion.
**Purpose:** complete the minigame art transition. Every task widget
currently draws abstract vector affordances (rings, lanes, a literal
progress bar) while the voice lines promise real things ("Tap when the
oven marker is green!", "Hold the sparkling syrup bottle!"). This file
specifies the themed art that makes every instruction TRUE, for all 60
non-combat phases across the 13 careers, registered to the engine's
exact geometry. The companion audit (mode rankings, input fixes already
shipped, REPLACE grammar prescriptions that consume this art) is
OPERA_WIDGET_INPUT_AUDIT_2026-08-02.md.

Conventions by reference: the weighted acceptance gate, auto-rejection
list, STYLE-JOBS / STYLE-HOUSE contracts, P2-09 canonical prop locks,
and the staging protocol are as written in
OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md (this content also
appears there as PRIORITY 8; this standalone file is the canonical
working copy for the widget-art delivery).

---

# PRIORITY 8 — Diegetic widget art for every non-bop/non-lens phase (codex handoff, 2026-08-02)

Sources audited: `scripts/opera_career_world_2d.gd` PHASES tables (13 careers, 86 phases), `scripts/opera_gesture_surface.gd` (draw code, engine state vars, the four proven nursery contexts), `scripts/opera_nursery_catch.gd` (catch engine geometry), `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` (P7 conventions, STYLE-JOBS/STYLE-HOUSE contracts, P2-09 canonical prop locks, staging protocol), and the 380-card inventory in `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`.

## 0. Scope and census

Excluding bop (plays on the painted stage, no card) and lens (stage-wide magnifier layer; its prop art is already covered by P7 Request C), exactly **60 phases** need themed widget art. Every career-template pair below is unique, so one backdrop per phase maps cleanly to `widget_<template>_<career>.png` with zero collisions:

| Template | Mode | Phases (career: PHASE) | n |
|---|---|---|---|
| T1 gauge | timing | chef: BAKE, astronaut: BOOST, racer: TURBO | 3 |
| T2 track | timing | detective: NAME, ballerina: DUET, candymaker: PARADE, farmer: FEED, boxer: JAB, magician: CABINET, popstar: RHYTHM, nursery: BURP | 8 |
| T3 pour | hold | chef: POUR, candymaker: SYRUP, painter: FILL, nursery: FEED | 4 |
| T4 basin | hold | doctor: WASH, nursery: WASH HANDS | 2 |
| T5 charge | hold | ballerina: WATCH, farmer: MUD HOP, magician: VANISH, astronaut: LAUNCH, popstar: SOUND CHECK | 5 |
| T6 crank | circle | chef: STIR, ballerina: TWIRL, candymaker: WRAP, doctor: CAST, magician: PORTAL, painter: STROKES, astronaut: VALVE, racer: LAP TWO, popstar: ENCORE | 9 |
| T7 trace | swipe | chef: PIPE, detective: TRAIL, ballerina: RIBBON, doctor: BANDAGE, magician: ROPE, painter: SKETCH | 6 |
| T8 push | swipe (directional) | farmer: HERD, boxer: DUCK, racer: STEER, nursery: BEDTIME | 4 |
| T9 target | tap | chef: TOP, candymaker: SHARE, doctor: X-RAY, farmer: PICNIC, boxer: BELT, painter: SPLAT, astronaut: PATCH, racer: FINISH | 8 |
| T10 lanes | choice | detective: MATCH, ballerina: STEPS, candymaker: SORT, doctor: FIND, farmer: PLANT, boxer: ROUND, magician: TRACK, painter: REVEAL, astronaut: PIPES, popstar: DANCE | 10 |
| T11 catch | catch | nursery: CATCH BABIES | 1 |

Total 60. The nursery already proves the pattern in shipping code (section 13).

## 1. Shared delivery contract (binds every request below)

- **Canvas — backdrops:** 1024x608 RGBA, authored at the gesture-surface aspect (runtime rect 392x232 ≈ 1.69:1; 1024x608 = 1.684:1). Satisfies `assets/ART_GENERATION_CONTRACT.md` via the "≤1024 px longest side" clause. Engine stretch-fits; full-bleed rectangle, no rounded corners (the storybook card border overdraws the edge).
- **Canvas — movers and stamps:** 256x256 RGBA POT, transparent, subject centered with ≥12 px margin. **Lane-lit strips:** 768x256 POT (three 256x256 sub-cells, lane order left/mid/right). **Full-frame state overlays:** 1024x608 registered 1:1 to their backdrop.
- **Style:** STYLE-JOBS finish (quote by name), plus the P7 Request A harmonization wording: navy/indigo contour lines #4a4f78–#1a1238 never black; aqua/lavender shadows; high-key; flat broad color fields; child-readable at 50% scale. No baked spotlights or vignettes (sole exception: T2-detective, where the spotlight IS the mover sprite). Backdrop centers stay low-contrast/low-clutter so the white ghost-finger demo and white marker/center dots read on top.
- **Green is reserved.** The success zone green (house value ≈ RGB 117,240,158) appears ONLY in the baked go-zone of T1/T2. No other green anywhere in widget art. This is the one channel that tells a pre-reader "wait for THIS" — it directly supports the owner's anti-mashing concern (the reward tuning itself was fixed engine-side on 2026-08-02: misses now trickle-by-assist behind cooldowns, so waiting for green strictly beats mashing).
- **Content locks (all 60):** no words/letters/numerals; no baked characters (Roshan, Faron, rivals, imps are runtime sprites — creature subjects that ARE the task, e.g. piggies/starfish plushies/babies, are allowed as props/patients); every P2-09 canonical prop design binds where its prop appears; bubbles never flame; stars only as effects; automatic-rejection list applies.
- **Filenames:** `widget_<template>_<career>.png` (backdrop), `widget_<template>_<career>_mover.png`, `_fill.png`, `_lit.png` (lane strip), `_mark.png`, shared elements `widget_<template>_shared_<element>.png`.
- **Target runtime path:** `assets/opera/worlds/widgets/` (new). Placed by generalizing `OperaGestureSurface.visual_context` (already plumbed: `configure(mode, accent, choice, context)`; contexts currently only `nursery_*`) — context string becomes `<template>_<career>`. Per the P7 contract, assets must be PLACED by runtime code in the same workstream: the engine work items are listed in section 14.
- **Staging:** `assets_src/concepts/opera_regeneration_2026-08-01/cards/` + contact sheets + PROMPTS.md + REGENERATION_LEDGER.csv rows, weighted gate pass ≥4.5 / target ≥4.7, one controlled promotion commit, one ASSET_LICENSES.md line per accepted asset, QA renders at gameplay scale on the Mobile renderer (candidates without runtime captures cap at 2/5 and must not ship).

**Registration geometry (in 1024x608 backdrop space, mirrors the engine constants):**
- T1/T2 timing run: 12%→88% of width = x 123→901; `timing_zone` is the constant `Vector2(0.30, 0.72)`, so the green go-zone is BAKED at x 356→683 of the run. Default track centerline y = 400 (skins may move it; record the y in the ledger row).
- T1 gauge: needle pivot (512, 500), needle reach 300 px, sweep 150°→30° (left-up to right-up); green wedge baked at 30%–72% of the sweep.
- T10 lanes: lane centers x = 171 / 512 / 853 (engine: `(i+0.5)/3`), lane subject ≤300 px wide, baseline y ≈ 430.
- T9 target roam field (engine `_relocate_tap_point`: ±0.30 w, ±0.26 h around center): x 205–819, y 146–462. Keep that region readable; mover renders at ~224 px.
- T5 charge meter rail: x 940–1000, y 90–540 (vertical).
- T11 catch: mobile band y ≈ 73 (0.12 h), catch line y = 450 (CATCH_Y 0.74), pillow line y = 553 (PILLOW_Y 0.91).

## 2. T1 `gauge` — timing: sweeping needle over an arc gauge (3 skins)

**Makes true:** "Tap when the marker is green" — the marker is a real gauge needle on a real machine.
**Engine binding:** `set_timing_position()` rotates the needle sprite across the marked sweep (ping-pong). Green wedge baked (zone is constant).
**Layers:** backdrop (machine + gauge face + baked green wedge) / mover: `widget_gauge_shared_needle.png` (one pearl-tipped needle serves all three — the P2-09i canonical candymaker fan-gauge pearl-pointer design, drawn BIG and phone-readable per that row's fix note) / overlay: `widget_gauge_<career>_success.png` full-frame glow flash.
**Content lock:** gauge face large (≥45% of width); needle must be readable at 50% scale — this is precisely the P2-09i "pointer states nearly indistinguishable at phone size" lesson.

| Career | Skin | Card references |
|---|---|---|
| chef (BAKE) | The canonical pink arch-with-shell oven (P2-09a lock), porthole showing the rising cake, fan gauge on the oven face; green wedge = the golden-bake moment | `opera_job_pastry_chef_gameplay_oven_closed.png`, `_oven_open.png`, `opera_job_pastry_chef_stage_states_oven_success.png` |
| astronaut (BOOST) | Booster console beside the rocket, thrust gauge, three pressure lamps that echo the sweep | `opera_job_astronaut_engineer_gameplay_rocket_side.png`, `opera_job_astronaut_engineer_stage_states_prelaunch_glow.png`, `_pressure_lamps.png` |
| racer (TURBO) | Kart dashboard: canonical two-tone steering wheel (P2-09o) at the edges, big turbo button under the gauge; green wedge = boost window | `opera_job_racecar_driver_gameplay_turbo_button.png`, `_steering_wheel.png`, `_bubble_turbo_trail.png` |

## 3. T2 `track` — timing: career subject travels a horizontal run through a baked green glow zone (8 skins)

**Makes true:** the moving thing named in the voice line is the thing that moves.
**Engine binding:** `set_timing_position()` translates the mover sprite along x 123→901; green glow zone baked at x 419→652 (a diegetic feature per skin — arch, spotlight pool, glowing tile — not a bare bar).
**Layers:** backdrop (scene + run + baked green feature) / mover: `widget_track_<career>_mover.png` 256x256 / shared success sparkle `widget_track_shared_hit.png`.

| Career | Backdrop | Mover | Green zone as | Card references |
|---|---|---|---|---|
| detective (NAME) | Lineup shelf of three distinct clue boxes; dim stage | sweeping spotlight pool | glow floor pool under the answer box (center) | `opera_job_detective_stage_states_searchlight_pool.png`, `_six_box_display.png`, `opera_job_detective_gameplay_coral_mystery_box.png`, `_teal_mystery_box.png`, `_plum_hatbox.png` |
| ballerina (DUET) | Recital floor ribbon of dance tiles | pearl beat-marker / slipper glow | glowing center tile | `opera_job_ballerina_gameplay_four_tile_floor.png`, `_coral_shell_tile.png`, `_teal_wave_tile.png`, `_plum_ribbon_tile.png`, `_pressed_tile_ripple.png` |
| candymaker (PARADE) | Candy-district street with confetti arch mid-run | parade cart | the arch glow | `opera_job_candy_maker_stage_states_parade_cart.png`, `_parade_arch.png`, `_parade_tableau.png` |
| farmer (FEED) | Meadow with toss arc; piggy waiting mid-run, mouth open | flying veggie (carrot) | glow ring at the piggy's mouth | `opera_job_farmer_gameplay_toss_arc.png`, `_carrot.png`, `_piggy_munch.png`, `opera_job_farmer_stage_states_toss_pointer.png` — STYLE from outfit/stage sheets until P2-08 painterly repaint promotes |
| boxer (JAB) | Ring ropes and posts; punch run at glove height | swinging padded focus mitt | glowing punch medallion center | `opera_job_boxer_gameplay_focus_mitt.png`, `_punch_medallion.png`, `_ring_post_ropes.png`, `_padded_gloves.png` |
| magician (CABINET) | Trick cabinet, star trail arcing across its doors | shooting-star sparkle (star-as-effect, allowed) | glow burst at the cabinet's pearl lock | `opera_job_magician_stage_states_trick_cabinet.png`, `opera_job_magician_gameplay_selector_glow.png` |
| popstar (RHYTHM) | Rainbow rhythm ribbon across the stage | rainbow music note | glowing pearl frame on the ribbon | `opera_job_pop_star_gameplay_rainbow_rhythm_ribbon.png`, `_beat_pulse.png`, `opera_job_pop_star_stage_states_rainbow_rhythm_state.png`, `_pearl_light_frame.png` |
| nursery (BURP) | **PROVEN** (`nursery_burp` context): baby over shoulder + patting hand + bar — art replacement at the same geometry; keep the bar as a blanket-trimmed track low in frame | existing `assets/opera/worlds/nursery/baby_1.png` stays runtime; hand-pat mover; P3-05 nursery palette |

## 4. T3 `pour` — hold: vessel pours while held, receiver visibly fills (4 skins)

**Makes true:** "Hold to pour" — a stream flows while the finger is down and the receiver fills.
**Engine binding:** `held` toggles the mover (stream/tilted vessel) visible; a new `set_fill(progress)` feed (section 14) reveals `_fill.png` bottom-up via `draw_texture_rect_region` crop.
**Layers:** backdrop (receiver empty + vessel at rest) / mover: `widget_pour_<career>_mover.png` (tilted vessel + stream, one sprite) / overlay: `widget_pour_<career>_fill.png` full-frame, drawn as the COMPLETE full state, engine crops by progress.
**Content lock:** the fill overlay must register pixel-perfect on the backdrop receiver; fill rises monotonically (no floating islands of fill above the crop line).

| Career | Skin | Card references |
|---|---|---|
| chef (POUR) | Sparkling batter pitcher over the big mixing bowl on the work counter; bowl fills with pale batter | `opera_job_pastry_chef_gameplay_bowl_empty.png`, `_bowl_calm.png`, `opera_job_pastry_chef_stage_states_work_counter.png` |
| candymaker (SYRUP) | Sparkling syrup bottle over the mold plates; molds fill one by one (canonical 7-candy roster shapes only, P2-09g) | `opera_job_candy_maker_gameplay_mold_plates.png`, candy roster cards (`_coral_flower_candy.png` … `_teal_spiral_candy.png`) |
| painter (FILL) | Big canvas with the glowing sunrise shape outlined; canonical red-handle rainbow-mop brush (P2-09l) held on the shape; shape floods with coral | the exact fill chain `opera_job_painter_gameplay_canvas_blank.png` → `_canvas_plum.png` → `_canvas_plum_coral.png`, `_coral_paint_pot.png`, `_coral_loaded_brush.png` |
| nursery (FEED) | **PROVEN** (`nursery_feed` context): warm bottle above the three babies — art replacement; milk level drains (reverse crop) while babies' cheeks rosy up | existing `baby_0..2.png` runtime; bottle card new; P3-05 palette |

## 5. T4 `basin` — hold: bubbly basin, bubbles multiply while held (2 skins)

**Engine binding:** `held` + fill feed scales/uncovers the bubble overlay stages.
**Layers:** backdrop (basin, water line) / overlay: `widget_basin_<career>_bubbles.png` full-frame full-suds state, cropped/faded in by progress / shared sparkle `widget_basin_shared_shine.png` at completion.

| Career | Skin | Card references |
|---|---|---|
| doctor (WASH) | The clinic handwashing basin — an exact accepted card exists | `opera_job_doctor_stage_states_handwashing_basin.png`; bubble grammar from `opera_house_flat/cards/opera_lobby_services_handwashing_bubble_markers.png` |
| nursery (WASH HANDS) | **PROVEN** (`nursery_wash` context): pearl basin + rising bubbles — art replacement at same geometry, moonlit P3-05 palette | — |

## 6. T5 `charge` — hold: energy builds on a subject, vertical meter on the right rail, release burst (5 skins)

**Makes true:** "Hold through the countdown…" — the held thing visibly gathers power.
**Engine binding:** `held` pulses the glow mover; fill feed drives the meter rail (x 940–1000) and steps discrete lamps where the skin has them; at 100% the world advances (release burst is the phase-transition flash).
**Layers:** backdrop / mover: `widget_charge_<career>_glow.png` 256x256 additive-style glow scaled by progress / overlay: `widget_charge_<career>_full.png` (full-charge state, e.g. lamps all lit).

| Career | Skin | Card references |
|---|---|---|
| ballerina (WATCH) | "Hold still and watch the glowing dance" — the demo ribbon-dancer glow trail completes across the recital floor under the mirror ball (exact watch-state card exists) | `opera_job_ballerina_stage_states_watch_state.png`, `_spotlight_pool.png`, `opera_job_ballerina_gameplay_mirror_ball.png`, `_twirl_ribbon.png` |
| farmer (MUD HOP) | Piggy in crouch wind-up beside the mud puddle; spring-squash deepens; full = pre-splash wobble (release = mud splash) | `opera_job_farmer_gameplay_piggy_hop.png`, `_mud_splash.png`, `opera_job_farmer_stage_states_mud_puddle.png` — P2-08 style caveat as above |
| magician (VANISH) | Lamba the bunny-fish (SPECIES LOCK: finned bunny-fish, never a land rabbit) under a thickening sparkle shroud; canonical pearl-tip wand (P2-09k) at frame edge | `opera_job_magician_gameplay_bunny_fish_peek.png`, `_bunny_fish_swim.png`, `_pearl_wand.png`, `_decoy_bubble_puff.png` |
| astronaut (LAUNCH) | Little rocket on the launch pad, engine glow building, three countdown lamps; bubbles never flame | `opera_job_astronaut_engineer_gameplay_rocket_front.png` (also the P4-05 goal-prop card), `opera_job_astronaut_engineer_stage_states_launch_pad.png`, `_prelaunch_glow.png`, `_pressure_lamps.png` |
| popstar (SOUND CHECK) | Canonical pearl/shell/coral microphone on its stand (the P2-01 popstar-cell reference design); level pearls climb the stand as the meter | `opera_job_pop_star_gameplay_microphone_idle.png`, `_microphone_active.png`, `_microphone_stand.png`; speakers per P2-09n (`opera_job_pop_star_stage_states_speaker_stacks.png`) |

## 7. T6 `crank` — circle: the circle affordance IS a rotating object (9 skins)

**Makes true:** "Draw circles to stir/turn/wrap" — drawing the circle turns the actual thing.
**Engine binding:** the existing angle-delta code (`previous_angle`) rotates the mover to the current finger angle around center; fill feed drives the progress overlay.
**Layers:** backdrop (the ring subject centered, radius ≈ 0.26·min-dim per the engine draw, i.e. ~158 px on the runtime rect — author the ring at 45–55% of backdrop height) / mover: `widget_crank_<career>_mover.png` 256x256, rotated by engine (pivot = sprite center; author the handle/subject pointing UP as 0°) / overlay: `widget_crank_<career>_progress.png` (deepening swirl / arc trail, cropped radially or alpha-stepped by progress — three-step alpha bands acceptable).

| Career | Ring subject | Mover | Card references |
|---|---|---|---|
| chef (STIR) | Batter bowl from above, swirl deepens | whisk (handle out) | `opera_job_pastry_chef_gameplay_bowl_stirring.png`, `_whisk.png`, `opera_job_pastry_chef_stage_states_stir_effect.png` |
| ballerina (TWIRL) | Twirl ribbon circle on the floor | ribbon-end comet | `opera_job_ballerina_gameplay_twirl_ribbon.png`, `opera_job_ballerina_stage_states_twirl_effect.png` |
| candymaker (WRAP) | Wrapped candy (canonical roster), wrapper twist-ends | twisting wrapper end | `opera_job_candy_maker_gameplay_plum_wrapped_candy.png`, `_wrapped_candy_reward.png`, `opera_job_candy_maker_stage_states_wrapping_swirl.png`, `_wrapping_station.png` |
| doctor (CAST) | Plushy starfish arm (coral, five-armed — species lock), soft cast winding around | bandage roll | `opera_job_doctor_gameplay_bandage_roll.png`, `_bandage_wrap.png`, `_starfish_calm.png`, `opera_job_doctor_stage_states_bandage_state.png` |
| magician (PORTAL) | Giant star portal ring of sparkles, opens with progress | sparkle comet on the rim | `opera_job_magician_stage_states_final_reveal.png`, `opera_job_magician_gameplay_selector_glow.png` |
| painter (STROKES) | Big canvas, grand circular rainbow stroke builds | canonical red-handle rainbow-mop brush (P2-09l) | `opera_job_painter_gameplay_palette.png`, `_plum_loaded_brush.png`/`_coral_`/`_cream_loaded_brush.png`, `_canvas_finished.png` |
| astronaut (VALVE) | The launch valve wheel — exact card exists; whole wheel rotates | the wheel itself (mover = wheel, backdrop = pedestal + pipe) | `opera_job_astronaut_engineer_gameplay_valve_wheel.png`, `_valve_spin_bubbles.png`, `opera_job_astronaut_engineer_stage_states_valve_pedestal.png`, `_valve_spin.png` |
| racer (LAP TWO) | Mini loop track (banked oval from above) | kart (side view) orbiting | `opera_job_racecar_driver_gameplay_opera_kart_side.png`, `opera_job_racecar_driver_stage_states_banked_curve.png`, `_lap_complete.png` |
| popstar (ENCORE) | Encore sparkle circle on the catwalk, glow-stick rail behind | sparkle mic-trail comet | `opera_job_pop_star_stage_states_encore_reveal.png`, `_glow_stick_rail.png`, `opera_job_pop_star_gameplay_shell_tambourine.png` |

## 8. T7 `trace` — swipe: a path that visibly fills stroke-by-stroke (6 skins)

**Engine binding:** swipe distance accumulates progress; fill feed reveals the lit-path overlay left-to-right by x-crop.
**Layers:** backdrop (scene + DIM guide path) / overlay: `widget_trace_<career>_lit.png` full-frame COMPLETE lit path, engine crops left→right.
**Content lock:** the path must be monotonic in x (never doubles back left) so the crop-reveal reads as continuous drawing. Left-to-right matches the P3-04 detective-stage trail direction note.

| Career | Path | Card references |
|---|---|---|
| chef (PIPE) | Frosting ribbon piped across the cake top (canonical 3-layer cake, P2-09b) | `opera_job_pastry_chef_gameplay_piping_ribbon.png`, `opera_job_pastry_chef_stage_states_frosting_ribbon.png`, `_frosting_pointer.png` |
| detective (TRAIL) | Glowing paw/footprint trail across the prop-library floor | `opera_job_detective_gameplay_paw_clue.png`, `opera_job_detective_stage_states_clue_glows.png` |
| ballerina (RIBBON) | Ribbon arcing across the recital floor | `opera_job_ballerina_gameplay_twirl_ribbon.png`, `opera_job_ballerina_stage_states_dance_floor.png` |
| doctor (BANDAGE) | Stretchy bandage unrolling across the plushy starfish; end state = starfish happy | `opera_job_doctor_gameplay_bandage_unrolled.png`, `_bandage_wrap.png`, `_starfish_calm.png` → `_starfish_happy.png` |
| magician (ROPE) | Magic rope straightening into one long glowing ribbon — NOTE: no accepted rope card exists; nearest style refs are the swap-trail family | `opera_job_magician_gameplay_swap_trail.png`, `_crossed_swap_trails.png`, `_feint_arc.png` |
| painter (SKETCH) | Sunrise sketch line across the blank canvas | `opera_job_painter_gameplay_canvas_blank.png`, `_swipe_ribbon.png` (exact), `_canvas_finished.png`, `opera_job_painter_stage_states_before_after.png` |

## 9. T8 `push` — swipe: big directional gesture, subjects respond (4 skins)

**Engine binding:** `swipe_dir` (already settable per-phase via the `dir` key — boxer DUCK sets DOWN); the glow-arrow stays as a soft baked affordance in the skin's fiction; responding subjects are movers nudged along the swipe axis.
**Layers:** backdrop / mover: `widget_push_<career>_mover.png` / shared soft glow arrows `widget_push_shared_arrow_down.png`, `_arrow_lr.png` (256x256, drawn by engine at the skin's marked arrow anchor).

| Career | Skin | Card references |
|---|---|---|
| farmer (HERD) | Meadow lane between fence segments; piggy trio (trot cycle) shuffles the direction swiped, toward the stage gate right | `opera_job_farmer_gameplay_piggy_trot_a.png`, `_piggy_trot_b.png`, `_happy_piggy_group.png`, `opera_job_farmer_stage_states_fence_segment.png` — P2-08 style caveat |
| boxer (DUCK) | Padded glove swings overhead between the ring posts; swipe DOWN ducks under it to the safe corner stool | `opera_job_boxer_gameplay_padded_gloves.png`, `_recoil_arcs.png`, `_ring_post_ropes.png`, `opera_job_boxer_stage_states_coral_corner_stool.png` |
| racer (STEER) | Kart REAR view on the straight track between coral gates; swipe slides the kart across lanes | `opera_job_racecar_driver_gameplay_opera_kart_rear.png` (exact rear view), `_safety_barrier.png`, `_course_flag.png`, `opera_job_racecar_driver_stage_states_straight_track.png` |
| nursery (BEDTIME) | **PROVEN** (`nursery_bedtime` context): three cribs + blankets + down arrow — art replacement; blanket per crib slides down via crop-reveal; stars overhead | existing `baby_0..2.png` runtime; crib/blanket cards new; P3-05 palette |

## 10. T9 `target` — tap: the target object sits at the engine-moved tap point; hits accumulate placed marks (8 skins)

**Engine binding:** mover drawn at `tap_point` (engine relocates after each hit within x 205–819, y 146–462); `tap_marks` positions get the `_mark.png` stamp — the accumulation is what makes "a candy for every friend" literally true.
**Layers:** backdrop (receiving scene) / mover: `widget_target_<career>_mover.png` 224–256 px glowing target object / stamp: `widget_target_<career>_mark.png` 128x128 placed-object.

| Career | Backdrop | Target mover | Mark | Card references |
|---|---|---|---|---|
| chef (TOP) | Canonical 3-layer cake top, three-quarter view (P2-09b/c toppings lock: cherry/cream/chocolate only) | sparkling cherry | placed topping (art may alternate the three canonical toppings within the stamp) | `opera_job_pastry_chef_gameplay_topping_targets.png` (exact), `_cherry_topping.png`, `_cream_topping.png`, `_chocolate_topping.png`, `_finished_cake.png` |
| candymaker (SHARE) | Parade crowd of friendly creatures | glowing wrapped candy (canonical roster) | candy-in-hands + heart sparkle | `opera_job_candy_maker_gameplay_wrapped_candy_reward.png`, roster cards, `opera_job_candy_maker_stage_states_parade_tableau.png` |
| doctor (X-RAY) | Soft-cartoon x-ray viewer over the plushy starfish silhouette (species lock; keep it cozy, zero spook) — NOTE: no x-ray card exists, new subject | glowing crack sparkle | mended-bone pearl glint | `opera_job_doctor_gameplay_checkup_tray.png`, `_care_complete_medallion.png` (style anchors) |
| farmer (PICNIC) | Piggies around the picnic blanket | glowing snack (apple/berries/corn/pumpkin) | snack placed before a piggy | `opera_job_farmer_stage_states_piggy_picnic.png` (exact), `_picnic_blanket.png`, `opera_job_farmer_gameplay_apple.png`, `_berries.png`, `_corn.png`, `_pumpkin.png` — P2-08 style caveat |
| boxer (BELT) | goal=1.0 single tap: championship belt (canonical design, P4-05 edge fix) on its pedestal, one big sparkle ring | the belt glow ring itself | none — success overlay `widget_target_boxer_success.png` confetti | `opera_job_boxer_gameplay_championship_belt.png`, `_belt_pedestal.png`, `opera_job_boxer_stage_states_belt_reward.png`, `_victory_podium.png` |
| painter (SPLAT) | Big canvas on the easel platform | glowing paint blob | splat stamp (rotate coral/plum/cream — exact stamp-set card exists) | `opera_job_painter_gameplay_splat_stamp_set.png` (exact), `opera_job_painter_stage_states_splat_state.png`, `_easel_platform.png` |
| astronaut (PATCH) | Rocket hull side with pipe runs | sparkle-leak bubble jet (bubbles never flame) | pearl rivet patch plate | `opera_job_astronaut_engineer_gameplay_rocket_side.png`, `opera_job_astronaut_engineer_stage_states_pipe_wall.png` |
| racer (FINISH) | Track run to the finish flag/ribbon | idle zoom strip (P2-09r lock: same teal strip both states) | lit zoom strip (active = glowing version of the SAME strip) | `opera_job_racecar_driver_gameplay_zoom_strip_idle.png`, `_zoom_strip_active.png`, `_finish_flag.png`, `_finish_ribbon.png`, `opera_job_racecar_driver_stage_states_finish_state.png` |

## 11. T10 `lanes` — choice: three distinct lane objects, flash-then-dim memory (10 skins)

**Engine binding:** three lane subjects baked in the backdrop at x 171/512/853 in NEUTRAL/dim state; during `choice_flash`/demo the engine draws the target lane's cell from the `_lit.png` strip; wrong picks kindly re-flash (existing behavior). Shared pick sparkle `widget_lanes_shared_pick.png`.
**Layers:** backdrop / per-career lit strip: `widget_lanes_<career>_lit.png` 768x256 (three lit-state cells, registered to lane centers, baseline y 430).
**Content lock:** the three lane objects must be visually DISTINCT tokens of equal attractiveness (recognition memory needs re-findable identity — the P2-09j "which hat" lesson), while the LIT state is the only brightness difference.

| Career | Three lane objects (left/mid/right) | Lit state | Card references |
|---|---|---|---|
| detective (MATCH) | coral mystery box / teal mystery box / plum hatbox — three exact distinct cards | clue glow halo + lid crack of light | `opera_job_detective_gameplay_coral_mystery_box.png`, `_teal_mystery_box.png`, `_plum_hatbox.png`, `opera_job_detective_stage_states_clue_glows.png` |
| ballerina (STEPS) | coral shell tile / teal wave tile / plum ribbon tile | the color's demo-glow (exact per-color cards exist) | `opera_job_ballerina_gameplay_coral_shell_tile.png`, `_teal_wave_tile.png`, `_plum_ribbon_tile.png`, `_coral_demo_glow.png`, `_teal_demo_glow.png`, `_plum_demo_glow.png` |
| candymaker (SORT) | three candy chutes color-coded coral/teal/plum feeding jars — NOTE: no chute card; build from hopper + conveyor language | chute mouth glow + candy peeking | `opera_job_candy_maker_stage_states_candy_hopper.png`, `_conveyor.png`, roster candies |
| doctor (FIND) | three plushy patients on the waiting bench (starfish + two friends from the checkup fiction; starfish cards exact) | glowing "ouch" spot | `opera_job_doctor_gameplay_starfish_worried.png`, `_starfish_calm.png`, `opera_job_doctor_stage_states_waiting_bench.png`, `_guidance_shell.png` |
| farmer (PLANT) | three garden soil rows with distinct row-markers (carrot/corn/pumpkin sticks) | row glow + seed sparkle | `opera_job_farmer_gameplay_vegetable_basket.png`, veggie cards — P2-08 style caveat |
| boxer (ROUND) | three focus pads on posts, left/middle/right | pad glow (glove-pointer language) | `opera_job_boxer_gameplay_focus_mitt.png`, `opera_job_boxer_stage_states_glove_pointer.png`, `_ring_corner.png` |
| magician (TRACK) | THE canonical three band hats: coral-band / cream-band / teal-band (P2-09j lock — the 3-distinct-token system, exact cards) | selector glow + hat hover | `opera_job_magician_gameplay_coral_band_hat.png`, `_cream_band_hat.png`, `_teal_band_hat.png`, `_selector_glow.png` |
| painter (REVEAL) | three empty gallery frames on the wall (goal=1.0, one pick) | frame glow; lit cell shows the sunrise inside | `opera_job_painter_stage_states_blank_gallery_wall.png`, `_gallery_reveal.png`, `opera_job_painter_gameplay_framed_sunrise.png` |
| astronaut (PIPES) | three ghost slots: straight / elbow / ring — the exact accepted slot system | fitted-pipe glow (exact fitted cards) | `opera_job_astronaut_engineer_gameplay_straight_ghost_slot.png`, `_elbow_ghost_slot.png`, `_ring_ghost_slot.png`, `_straight_fitted.png`, `_elbow_fitted.png`, `_ring_fitted.png`, `_wrong_shape_hover.png` |
| popstar (DANCE) | arrow pads under the CANONICAL P2-09m mapping — three lanes: coral LEFT-arrow (left lane) / plum UP-arrow (middle) / teal RIGHT-arrow (right lane); spatially congruent and mapping-true | pressed-arrow glow | `opera_job_pop_star_gameplay_left_arrow.png`, `_up_arrow.png`, `_right_arrow.png`, `_pressed_arrow.png`, `opera_job_pop_star_stage_states_arrow_lane.png` (dance_floor pending P2-09m regen) |

## 12. T11 `catch` — nursery cradle engine (1 skin, art replacement only)

The engine (`opera_nursery_catch.gd`) is proven and fully data-driven; babies already load real textures (`assets/opera/worlds/nursery/baby_0..2.png`). Replace only the procedural draws, at the engine's normalized geometry:
- `widget_catch_nursery.png` backdrop — moonlit nursery interior, star-mobile band at y ≈ 0.12 h (engine animates the bob; deliver mobile arms as part of backdrop, or optionally `widget_catch_nursery_mobile.png` 768x256 strip if animated arms are wanted).
- `widget_catch_nursery_cradle.png` 256x256 mover — Roshan's soft cradle/arms basket (replaces the arc+lines draw), pivot bottom-center; engine slides it at y = 0.80 h under the finger.
- `widget_catch_nursery_pillows.png` 1024x160 overlay — the pillow-safe floor row at y ≈ 0.91 h (replaces the five circles); must read soft/cozy, misses land here safely.
- P3-05 palette (seafoam teal, cream, soft lavender, pearl gold; night-calm). Content lock: babies match the existing three sprites; no text; the golden call-down arrow remains engine-drawn.

## 13. Nursery contexts that already PROVE the pattern

`opera_gesture_surface.gd` `_draw_nursery_context()` ships four diegetic scenes drawn BEHIND the affordance — basin+bubbles (`nursery_wash` → T4), bottle+babies (`nursery_feed` → T3), baby+patting hand+timing bar (`nursery_burp` → T2), cribs+blankets+down arrow (`nursery_bedtime` → T8) — plus the catch engine (T11). These prove, in shipping code, that the instruction can be literally true on the widget with zero engine redesign. They need only raster art replacement at the same registered geometry; their vector draw code retires when the textures land. Every other career simply adopts the same context mechanism.

## 14. Runtime integration items (same workstream — the P7 no-orphans rule)

1. Generalize `visual_context` beyond `nursery_*`: `opera_career_world_2d.gd` `_show_phase()` sets `context = "%s_%s" % [template, career_id]` from a phase→template map (the census in section 0 is that map); `opera_gesture_surface.gd` loads `assets/opera/worlds/widgets/widget_<context>*.png` and draws backdrop → movers → overlays → affordance accents → demo finger, falling back to today's vector affordances when files are absent (graceful-degrade, same as the goal props).
2. Add a `set_fill(progress: float)` feed from the world (it already computes `phase_progress/goal` for `phase_fill`) so T3/T4/T5/T6/T7 overlays can crop-reveal.
3. T1/T2 reuse `set_timing_position()` unchanged; T9 reuses `tap_point`/`tap_marks`; T10 reuses `target_choice`/`choice_flash`; T8 reuses `swipe_dir`.
4. Ledger requirement: each backdrop's ledger row records its registration values (track y, gauge pivot, lane baseline, fill-region bounds) so the engine mapping is data, not guesswork.

## 15. Manifest summary

60 backdrops (one per phase, `widget_<template>_<career>.png`) + ~52 movers/stamps/lit-strips/fill-overlays + 7 shared elements (gauge needle, track hit-sparkle, basin shine, push arrows x2, lanes pick-sparkle, target confetti) ≈ **119 files**. Three subjects have no accepted card and are flagged as genuinely new art (Path B): magician rope, doctor x-ray viewer, candymaker chutes. Everything else is Path-A-adjacent: composed from the named accepted cards under STYLE-JOBS, with the P2-09 canonical-design locks binding wherever their props appear, and the P2-08 farmer painterly caveat on all four farmer skins.

Files referenced (absolute): `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_career_world_2d.gd`, `.../scripts/opera_gesture_surface.gd`, `.../scripts/opera_nursery_catch.gd`, `.../OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md`, `.../assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`, `.../assets/opera/worlds/nursery/baby_0..2.png`.
