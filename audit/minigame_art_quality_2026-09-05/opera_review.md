# Opera minigame visual review — 2026-09-05

Threshold: 4.5/5. Scores are subjective observations of dated runtime composites, not an eight-dimension verification result and not owner acceptance. A family does not pass from isolated source art.

## Evidence authority

- Integrated three-act states: `audit/evidence/opera-two-act-20260905/*.png`.
- Shared 14-family states: `C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/opera-reaudit-20260905/{activities,phase-rooms,widgets}/*.png`. These are representative historical captures; they support the observed composition only where the visual implementation is unchanged.
- Teacher: fourteen Godot 4.7.2 Mobile captures in `.worktrees/teacher-learning-engine-20260905/tmp/teacher-engine/*.png`, captured from candidate `775ceee1`. `scripts/opera_teacher_surface.gd` is byte-equivalent to this worktree's integrated file.
- Racer: six PNGs in `audit/evidence/opera-racer-integration-20260905/`, captured from candidate `775ceee1`. `scripts/opera_racer_surface.gd` was byte-equivalent before this art pass; the retained lap flags now differ. The baseline score and old captures do not describe the rejected tire experiment or certify the retained candidate. Historical manifest hashes remain historical hashes.
- Geologist: current rebuilt states are `.worktrees/geologist-rebuild-20260905/tmp/geologist-rebuild/phase-{0..3}-{ready,progress}.png`. The old `geologist_03_geology_sort.png` quiz is stale and excluded.

Static frames cannot verify cadence, stable pivots, contact or settle. No family receives 5/5 without owner runtime acceptance under `DL-VIS-07`.

## Scores and weak live owners

| Family | Score | Observed weakness | Live owner / assets |
|---|---:|---|---|
| Chef | 3.6 | Painted kitchen is strong; bowl, sweep and progress treatment remain flatter and more diagrammatic. | `OperaGestureSurface._draw_widget_family_ground/_draw_widget_layers`; `widget_pour_chef_{mover,fill}.png`, `widget_crank_chef_{mover,progress}.png`, `widget_trace_chef_lit.png`, target family. |
| Detective | 4.1 | Painted clue board is readable; slot contrast, cursor and broad vignette weaken it. | `_draw_clue_board`, `OperaCareerWorld2D._draw_lens_layer`; `widget_clue_board_{empty,tokens,complete}.png`, `assets/opera/worlds/ui/magnifier.png`. |
| Ballerina | 4.0 | Accepted actor poses are strong; ribbon/twirl tracks dominate as translucent instrumentation. | `OperaBalletSurface._draw_ribbon_game/_draw_twirl_game/_draw_ghost_finger`; accepted ballerina atlas and `goal_ballerina.png`. |
| Candy Maker | 3.4 | Excellent factory; SYRUP inset/base has a foreign rectangular composition and other layers remain widget-like. | `_load_widget_set` pour branch, `_draw_widget_family_ground/_draw_widget_layers`; `widget_pour_candymaker{,_mover,_mover_empty,_fill}.png`, `widget_crank_candymaker_{mover,progress}.png`, lanes/target families. |
| Stuffie Doctor | 3.8 | Strong clinic; scan and generic family layers are small or visually detached from the patient. | `OperaGestureSurface` basin/lanes/target/crank/trace branches; `widget_basin_doctor_bubbles.png`, `widget_basin_shared_shine.png`, `widget_lanes_doctor_lit.png`, `widget_target_doctor_*`, `widget_crank_doctor_{mover,patient,progress}.png`, `widget_trace_doctor_lit.png`. |
| Farmer | 3.1 | Seed/work panels and repeated affordance chrome are much flatter than the garden. | `_draw_garden_plant`, `_draw_long_push`, target branch; `assets/mg/seed.png`, `widget_push_farmer_mover.png`, shared arrow, `widget_target_farmer_{mover,mark,piece_*}.png`. |
| Boxer | 4.2 | Room/imp/mitts work; foreground gloves and circular telegraphs are markedly flatter. | `OperaBoxingSurface._draw_glove/_draw_target/_draw_counter/_draw_impact`; boxing target/telegraph assets. |
| Magician | 4.1 | Cabinet and actors work; small objects, schematic choice layers and broad focus treatment remain. | specialist magic routines plus lanes/trace/crank assets: `widget_lanes_magician_lit.png`, `widget_trace_magician_lit.png`, `widget_crank_magician_*`, portal layers. |
| Painter | 3.3 | Blank rectangular live canvas/cursor does not inherit the painted garden's material quality. | `_draw_paint_reveal`, `_draw_trace_patches`, target/lanes branches; `widget_trace_painter_lit.png`, `widget_target_painter_{mover,mark}.png`, `widget_lanes_painter_lit.png`. |
| Astronaut | 2.8 | Pipe grid/blocks and controls read as placeholder diagrams over the lab. | `_draw_pipe_tile/_draw_pipe`; `widget_pipe_{tile_h,tile_v,elbow_*,tank,intake}.png`; target/crank/charge/push families. |
| Racer | 4.1 | Circuit/cars/finish are polished; cream steering capsule, empty top circles and busy combined kart/driver silhouette remain below bar. | `OperaRacerSurface._draw/_draw_car/_draw_race_controls`; `widget_crank_racer_{kart,wheel}.png`, `widget_push_racer_mover.png`. |
| Pop Star | 3.8 | Singer Roshan and costumed imp are strong; oversized flat echo stars and schematic practice panel compete. | `_draw_echo/_draw_echo_star`, charge/lanes/crank branches; popstar star-note, charge, lanes and crank assets. |
| Nursery | 3.1 | Painted room/characters clash with diagrammatic mobile, pillows and ellipses. | `OperaNurseryCatch._draw/_draw_baby`; nursery specialist scenes; `widget_catch_nursery_{cradle,pillows}.png`, basin/pour/push nursery assets. |
| Geologist | 2.7 | Rebuild has four clear physical verbs, but flat sandstone board, navy zigzags, sparse ready states and geometric objects remain far below adjacent character art. | `OperaGeologySurface._draw_river/_draw_fossil/_draw_brush/_draw_pan/_draw_geode/_draw_work_surface`; geology prop textures. |
| Teacher | 3.5 | Polished library and Roshan surround a dominant cream worksheet with flat shapes, numerals and long written instructions. | `OperaTeacherSurface._draw/_draw_pattern/_draw_counting/_draw_group/_draw_shape/_draw_demo`. |

Result: 0/15 are evidenced at 4.5. Highest priorities are Geologist, Astronaut, Farmer, Nursery, Painter, Candy Maker and Teacher.

## Corrected shared-widget diagnosis

The live-route audit proves that shipping hold/circle/swipe phases do **not** use the raw `_draw()` fallback. `_widget_template()` maps hold to basin/pour/charge, circle to crank, and swipe to push/trace; explicit nursery and magic contexts use specialist scenes. `_bind_widget()` resolves `<template>_<career>` or the explicit override. The fallback is retained for unknown/direct diagnostic callers.

The reviewed pixels are owned by `_load_widget_set()`, `_draw_widget_family_ground()`, and `_draw_widget_layers()`. Exact loader mapping:

- gauge: code arc/ticks + `widget_gauge_shared_needle.png` + `<prefix>_success.png`
- track: code band + `<prefix>_mover.png` + `widget_track_shared_hit.png`
- pour: code bowl + `<prefix>_mover.png` + `<prefix>_fill.png`; Candy Maker also loads its base, empty mover and ghost hand
- basin: `_draw_doctor_basin_subject()` + `<prefix>_bubbles.png` + `widget_basin_shared_shine.png`
- charge: contextual scene or code ring + `<prefix>_glow.png` + `<prefix>_full.png`
- crank: contextual scene or code arc + `<prefix>_mover.png` + `<prefix>_progress.png`
- trace: authored corridor or `_draw_trace_patches(<prefix>_lit.png)`
- push: `_draw_long_push()` or code line + `<prefix>_mover.png` + `widget_push_shared_arrow_{lr,down}.png`
- target: anchored/object routine or code circle + `<prefix>_{mover,mark,success,piece_*}.png`
- lanes: code lane placement/rings + `<prefix>_lit.png` + `widget_lanes_shared_pick.png`

Repairs must target a rendered family asset and the corresponding ground/layer branch. Removing the dead fallback is not a visual repair.

## Brush review

Evidence: `tmp/art-quality/phase-1-brush-contact.png` (2026-09-05). Source: `assets/castle/day_one_art_studio/magic_cleaning_brush.png`.

The brush source scores **4.7/5**: strong feather silhouette, clean deep-purple contour, polished gold/wood/lavender/aqua material bands, clean transparency and stable identity. Keep it unchanged.

Its runtime contact presentation scores **3.5/5**. At roughly 150 px it remains recognizable, but much of its painted detail is lost. It floats over an almost empty brown work area without visible bristle compression, fossil contact, dust displacement, grounded shadow or clear before/after material change. Repair scale and contact animation around the brush; do not replace the brush pixels.

## Replacement gate

Reuse approved art first. For each failed phase capture idle, anticipation, active contact, near-complete, payoff and settle at 1280×720 Mobile/Speedy plus wide aspect. Validate phone-size hierarchy, stable pivot/identity, truthful object change, hitbox alignment and importer/probe performance. A different auditor rescoring below 4.5 returns the item to repair; no averaging can hide a failed state.
