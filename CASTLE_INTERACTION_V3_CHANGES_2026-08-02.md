# Pearl Castle interaction v3 change ledger - 2026-08-02

## Delivered scope

- Doubled the physical fixture inventory in every playable castle room: Main Hall and Royal Kitchen now have 14 each; Opera Hall, Library, Playroom, Craft Room, Mermaid Pool, and Bubble Bath now have 8 each.
- Overall castle delivery: 71 unique interactive visuals and 76 physical fixtures (9.5 fixtures per room). The active v3 manifest contains 67 assets / 72 instances: 29 active v2-base assets plus 38 v3 additions. Four approved room-derived Mermaid Pool base animations are validated separately; retired pool v2 sheets remain retired.
- Every new fixture uses eight individually authored complete-object states in a 4 x 2 sheet. Timelines are 8 steps except the kettle and shower, whose 10-step sequences intentionally hold their fully deployed dry object state while runtime water flows.
- All primary actions animate the complete object. Water remains bounded, shader-backed Sprite3D material attached to the fixture; no generic full-room overlay or modeled water is used.
- Active water-oriented delivery is split truthfully: 10 shader-backed fixture interactions (5 active v2 plus 5 v3) and 4 approved room-derived Mermaid Pool water animations, for 14 overall.
- Active cosmetic Jolt delivery is 8 fixtures (6 active v2 plus the new rocking horse and sailboat), with hard caps of 12 allocated / 8 awake. Jolt remains visual garnish and never owns game logic.

## New fixtures and normalized-use actions

### Main Hall (7 -> 14)

- `shell_clock` - Royal shell clock: `open_clock_and_chime` (8 timeline steps; 8 authored states).
- `visitor_bell` - Pearl visitor bell: `pull_bell_cord_and_ring` (8 timeline steps; 8 authored states).
- `left_pearl_vitrine` - Crown pearl vitrine: `open_vitrine_and_raise_crown` (8 timeline steps; 8 authored states).
- `right_pearl_vitrine` - Compass pearl vitrine: `open_vitrine_and_reveal_compass` (8 timeline steps; 8 authored states).
- `banner_left` - Royal pearl banner: `unroll_and_rewind_banner` (8 timeline steps; 8 authored states).
- `fern_planter` - Pearl fern planter: `unfurl_and_fold_fern_fronds` (8 timeline steps; 8 authored states).
- `chest_bench` - Royal chest bench: `unlock_open_and_close_bench` (8 timeline steps; 8 authored states).

### Opera Hall (4 -> 8)

- `shell_piano` - Shell piano: `open_piano_lid_and_play_keys` (8 timeline steps; 8 authored states).
- `coral_harp` - Coral concert harp: `pluck_harp_strings_and_rebound` (8 timeline steps; 8 authored states).
- `conductor_podium` - Conductor podium: `lift_baton_and_turn_score_page` (8 timeline steps; 8 authored states).
- `costume_trunk` - Shell costume trunk: `unlatch_trunk_and_lift_costume` (8 timeline steps; 8 authored states).

### Royal Kitchen (7 -> 14)

- `seafoam_kettle` - Seafoam kettle: `tilt_kettle_and_pour_into_cup` (10 timeline steps; 8 authored states).
- `soup_pot` - Shell soup pot: `lift_pot_lid_and_reveal_soup` (8 timeline steps; 8 authored states).
- `cookie_jar` - Pearl cookie jar: `twist_jar_lid_and_raise_cookie` (8 timeline steps; 8 authored states).
- `cutlery_drawer` - Pearl cutlery drawer: `pull_drawer_and_rock_spoon` (8 timeline steps; 8 authored states).
- `ladle_rack` - Shell ladle rack: `swing_ladles_on_hooks` (8 timeline steps; 8 authored states).
- `serving_tureen` - Royal serving tureen: `lift_tureen_lid_and_reveal_soup` (8 timeline steps; 8 authored states).
- `shell_cupboard` - Shell cup cupboard: `open_cupboard_and_settle_cups` (8 timeline steps; 8 authored states).

### Library (4 -> 8)

- `rolling_ladder` - Rolling library ladder: `release_brake_and_roll_ladder` (8 timeline steps; 8 authored states).
- `secret_panel` - Secret story panel: `pull_book_and_open_secret_panel` (8 timeline steps; 8 authored states).
- `quill_set` - Pearl quill set: `dip_quill_write_and_return` (8 timeline steps; 8 authored states).
- `telescope` - Shell telescope: `unclasp_extend_and_focus_telescope` (8 timeline steps; 8 authored states).

### Playroom (4 -> 8)

- `toy_chest` - Stuffie toy chest: `unlatch_chest_and_peek_stuffie` (8 timeline steps; 8 authored states).
- `rocking_horse` - Pearl rocking horse: `rock_horse_forward_and_back` (8 timeline steps; 8 authored states).
- `xylophone` - Rainbow shell xylophone: `press_xylophone_keys_in_sequence` (8 timeline steps; 8 authored states).
- `dollhouse` - Pearl dollhouse: `unlatch_and_open_dollhouse` (8 timeline steps; 8 authored states).

### Craft Room (4 -> 8)

- `sewing_machine` - Shell sewing machine: `turn_wheel_stitch_and_feed_cloth` (8 timeline steps; 8 authored states).
- `scissors` - Pearl craft scissors: `open_scissors_and_cut_ribbon` (8 timeline steps; 8 authored states).
- `stamp_press` - Shell stamp press: `lower_stamp_and_emboss_card` (8 timeline steps; 8 authored states).
- `bead_jar` - Pearl bead jar: `open_bead_jar_and_lift_strand` (8 timeline steps; 8 authored states).

### Mermaid Pool (4 -> 8)

- `waterwheel` - Pearl pool waterwheel: `open_gate_and_turn_waterwheel` (8 timeline steps; 8 authored states).
- `sailboat` - Pearl pool sailboat: `raise_sail_and_float_boat` (8 timeline steps; 8 authored states).
- `buoy_bell` - Pearl buoy bell: `bob_buoy_and_ring_bell` (8 timeline steps; 8 authored states).
- `dock_chest` - Pool dock chest: `unlatch_chest_and_unroll_map` (8 timeline steps; 8 authored states).

### Bubble Bath (4 -> 8)

- `shell_shower` - Shell bath shower: `turn_shower_control_and_run_water` (10 timeline steps; 8 authored states).
- `vanity_cupboard` - Pearl vanity cupboard: `open_vanity_and_reveal_towels` (8 timeline steps; 8 authored states).
- `soap_pump` - Pearl soap pump: `press_soap_pump_and_dispense_bead` (8 timeline steps; 8 authored states).
- `towel_spool` - Shell towel spool: `turn_spool_unroll_and_rewind_towel` (8 timeline steps; 8 authored states).

## Water and physics corrections

- Seafoam kettle: frames draw the kettle and cup dry. At authored atlas frame 4, the bounded runtime stream begins at the current spout coordinates and terminates inside the cup; a separate cup-fill mask remains inside the cup. Eight per-frame stream geometries track the actual spout.
- Shell shower: frames draw the shower and basin dry. At authored atlas frame 4, the bounded runtime stream begins at the current nozzle and terminates inside its own basin; a separate tub-entry mask remains inside that basin. Eight per-frame stream geometries track the actual nozzle.
- Pool waterwheel: bounded wheel-feed and paddle-splash masks support the authored gate/wheel motion.
- Pool sailboat and buoy bell: bounded local ripple masks follow their water contacts. Only the free sailboat receives buoyant Jolt garnish; the tethered buoy anchor remains fixed.
- Rocking horse: a very small bounded hinge response supplements its authored rocking states without replacing them (`max_angle_radians = 0.035`, impulse scale `0.28`).

## Cutout, frame, and mobile QA

- Source preparation is transactional and one-shot guarded. Each source becomes 1024 x 512 with an exact four-pixel chroma inset around every conceptual cell before keying.
- Runtime normalization keys chroma to RGBA, removes only tiny isolated subject specks, applies one uniform scale per full sheet, preserves the chosen fixed anchor, and requires at least six transparent pixels around every runtime cell.
- Every v3 sheet must have eight distinct state rasters, a clear alpha border, no visible key color, anchor spread no greater than 1.5 pixels, and a longest edge no greater than 1024 pixels.
- Per-room decoded interaction textures are capped at 24 MiB RGBA. The Speedy-tier visible Sprite3D ceiling is 33 cards after the doubled fixture inventory.
- Runtime inventories are gated at: Main Hall 14 fixtures plus 3 dust-bunny gameplay cards / 14 hotspots; Kitchen 14 fixtures / 11 hotspots (the four pans share one); Playroom 8 fixtures plus 3 temporary rescue cards / 8 hotspots; every other room 8 fixtures / 8 hotspots.
- Codex visual review is recorded as accepted for integration. Owner/human art review and phone play-testing remain pending; the records do not claim otherwise.

## Validation and export changes

- Runtime probe now verifies the 67/72 active-manifest split, four approved legacy pool bases, 71/76 overall inventory, 38 v3 additions, exact room and hotspot counts, dynamic water frame binding, active water/Jolt counts, caps, card ceiling, and decoded texture budget.
- Focused Crown, Bubble Bath, and Stuffie probes now assert the doubled inventories and all four new bathroom semantics/audio paths.
- CI preserves every v2 gate and additionally checks source preparation, v3 normalization, and the complete v3 delivery audit before Godot import/probes.
- Android and Windows exports explicitly retain the approved room-derived pool manifest plus the v2 and v3 JSON manifests.
