class_name OperaGestureSurface
extends Control
## One-finger input surface shared by all thirteen 2D Opera career worlds.
##
## The surrounding world chooses a gesture mode; this node turns mouse and
## touchscreen input into normalized progress without owning career state.
## Incorrect timing/choices report lower quality but still make a little
## progress, so there is no dead end for a non-reader.

signal gesture(kind: String, amount: float, quality: float)

var mode := "tap"
var accent := Color(1.0, 0.62, 0.8)
var target_choice := 1
var choice_count := 3
var timing_position := 0.0
var timing_zone := Vector2(0.30, 0.72)
var held := false
var pointer_pos := Vector2.ZERO
var previous_pos := Vector2.ZERO
var previous_angle := 0.0
var have_angle := false
var _last_spin := 0.0
## Friendly imp-scuffle targets for the "bop" combat beats. Each entry:
## {home: Vector2, pos: Vector2, r: float, hp: int, captain: bool, popped: bool}
var bop_targets: Array = []
var bop_texture: Texture2D = null
var bop_captain_texture: Texture2D = null
var last_bop_pos := Vector2.ZERO


## Ghost-finger demo: until the child touches, a glowing dot acts out the
## expected gesture so no phase ever needs reading to understand.
var demo_active := true
var demo_t := 0.0
var _demo_redraw := 0.0
var input_started := false
var feedback_t := 0.0
var feedback_positive := false
var feedback_position := 0.0
var feedback_anchor := Vector2.ZERO
var completion_accepted := false
## Choice lanes flash gold briefly, then dim so the pick uses recognition
## memory instead of tap-the-highlight; wrong picks kindly re-flash.
var choice_flash := 1.4
## Shell-game glide (magician TRACK): after the flash, the glow visibly
## slides from the flashed lane into the target lane before dimming.
var shuffle_from := -1
var shuffle_t := 0.0
## Oven bake (chef BAKE, owner 2026-08-04): heat RISES AT A STATIC RATE and
## the child REMOVES the cake by tapping the big mitt handle. Bands: pale ->
## golden window -> toasty cap, where it waits indefinitely for the mitt tap.
## still a cake — there is no burn state and no fail branch anywhere.
var oven_t := 0.0
var oven_peek := 0.0
var oven_done := false
var oven_redraw := 0.0
## Bubble-fuel pipes (astronaut PIPES; owner-mandated mini Pipe Dream).
## Place or slide PRE-ROTATED tiles — no rotation control exists anywhere,
## no timer, no failure: fuel WAITS kindly at a gap, and after 8s a gold
## twinkle marks the cell that needs a tile. Three rounds, each one pipe
## longer, with napping imps as the routing puzzle (they never touch tiles
## the child has placed — escalation is routing, not sabotage).
const PIPE_COLS := 4
const PIPE_ROWS := 3
const PIPE_CELL := 112.0
const PIPE_ORIGIN := Vector2(124.0, 114.0)
const PIPE_TRAY_SIDE := 84.0
const PIPE_TRAY_STEP := 94.0
const PIPE_TRAY_START_X := 76.0
const PIPE_TRAY_GAP_Y := 12.0
const PIPE_TANK_SIDE := 116.0
const PIPE_INTAKE_SIDE := 112.0
const PIPE_ENDPOINT_GAP := 58.0
const PIPE_MOUTHS := {
	"H": [Vector2i(-1, 0), Vector2i(1, 0)],
	"V": [Vector2i(0, -1), Vector2i(0, 1)],
	"NE": [Vector2i(0, -1), Vector2i(1, 0)],
	"NW": [Vector2i(0, -1), Vector2i(-1, 0)],
	"SE": [Vector2i(0, 1), Vector2i(1, 0)],
	"SW": [Vector2i(0, 1), Vector2i(-1, 0)],
}
## rounds: fixed stubs are pre-placed and never liftable; imps nap on their
## cells and giggle when tapped, but stay (tray = needed tiles + at most one)
const PIPE_ROUNDS := [
	{"entry": 4, "exit": 7, "exit_dir": Vector2i(1, 0), "fixed": {4: "H", 7: "H"}, "imps": [], "tray": ["H", "H"]},
	{"entry": 4, "exit": 7, "exit_dir": Vector2i(1, 0), "fixed": {4: "NW", 7: "H"}, "imps": [5], "tray": ["SE", "H", "SW", "NE", "H"]},
	{"entry": 4, "exit": 3, "exit_dir": Vector2i(0, -1), "fixed": {4: "H"}, "imps": [0, 6], "tray": ["H", "NW", "SE", "H", "NW", "V"]},
]
var pipe_round := 0
var pipe_grid: Array = []
var pipe_fixed: Array = []
var pipe_tray: Array = []
var pipe_tray_sel := -1
var pipe_drag_tile := ""
var pipe_drag_from := -1
var pipe_flow: Array = []
var pipe_flow_t := 0.0
var pipe_wait_t := 0.0
var pipe_pause := 0.0
var pipe_redraw := 0.0

## Echo Song (popstar RHYTHM rebuild): three stage stars light in order
## with pitched notes; the child taps them back in ANY tempo — order
## matters, speed never does. Wrong star kindly replays the verse.
const ECHO_VERSES := [[0, 2], [0, 1, 2], [2, 1, 0]]
var echo_verse := 0
var echo_show_i := -1
var echo_show_t := 0.0
var echo_input_i := 0
var echo_listening := false
var echo_last_note := 0
var echo_glow := 0.0
## Tilt-pour (chef POUR / candymaker SYRUP): grab the pitcher and it TILTS;
## the stream follows, the bowl fills only while the stream lands in it,
## and the pitcher visibly drains. The child controls the pour, not a clock.
const CANDYMAKER_POUR_SECONDS := 3.0
const CANDYMAKER_PITCHER_SPOUT_UV := Vector2(0.125, 0.2421875)
const CANDYMAKER_MOLD_PATH := \
	"res://assets/opera/worlds/widgets/widget_target_candymaker_piece_1.png"
var pour_tilt := 0.0
var pour_x := 0.0
var pour_level := 0.0
var pour_reserve := 1.2
var pour_hold := false
var pour_emit_acc := 0.0
var pour_redraw := 0.0
var pour_mold_texture: Texture2D = null

## Plushy Doctor X-ray: drag one scanner beam over two deterministic sore
## spots on the approved X-ray-machine card. A stationary tap cannot diagnose;
## only a real sweep crossing the current spot changes state. There is no
## timer, miss, or reset, and the same wordless sweep replays after release.
const XRAY_SPOTS: Array[Vector2] = [Vector2(0.65, 0.50), Vector2(0.48, 0.40)]
var xray_scanner_pos := Vector2.ZERO
var xray_dragging := false
var xray_found: Array[bool] = []
var xray_found_count := 0
var xray_complete := false
var xray_glow := 0.0
var xray_redraw := 0.0

## Ballerina call-and-response: four floor pads perform one short phrase,
## then wait without a clock for the child to dance it back. Progress is
## emitted only after the whole phrase is reproduced in order; a wrong pad
## preserves the correct prefix and replays only the remaining suffix.
const DANCE_SEQUENCE: Array[int] = [0, 2, 3, 1]
const DANCE_SHOW_STEP := 0.58
var dance_show_index: int = -1
var dance_show_start: int = 0
var dance_show_t := 0.0
var dance_input_index: int = 0
var dance_listening := false
var dance_complete := false
var dance_last_pad: int = -1
var dance_glow := 0.0
var dance_redraw := 0.0

## Candymaker sorting: one slow, deterministic conveyor piece at a time.
## Missed pieces loop; a wrong bin returns the same piece to the belt. Only a
## correctly matched silhouette advances the queue.
const CANDY_SEQUENCE: Array[int] = [0, 1, 2, 2, 0, 1]
var candy_piece_index: int = 0
var candy_type: int = 0
var candy_position := Vector2.ZERO
var candy_drag_offset := Vector2.ZERO
var candy_dragging := false
var candy_sorted: int = 0
var candy_complete := false
var candy_loops: int = 0
var candy_last_bin: int = -1
var candy_glow := 0.0
var candy_redraw := 0.0

## Painter reveal: coverage belongs to a coarse grid, not the career's scalar
## fill meter. Stationary taps uncover nothing; actual strokes claim cells and
## the completed painting emits exactly one progress event at the threshold.
const PAINT_GRID_COLS := 10
const PAINT_GRID_ROWS := 6
const PAINT_REQUIRED_COVERAGE := 0.62
var paint_cells: Array[bool] = []
var paint_covered: int = 0
var paint_dragging := false
var paint_last_point := Vector2.ZERO
var paint_complete := false
var paint_reveal_texture: Texture2D = null

## Farmer feed: pull one vegetable back from the basket and let go. A valid
## pull follows a deterministic arc to the pig; every other release loops the
## same vegetable gently home. The landing, never the release, pays progress.
const FARM_LOB_GOAL := 4
const FARM_FLIGHT_DURATION := 0.90
var farm_piece_position := Vector2.ZERO
var farm_drag_offset := Vector2.ZERO
var farm_dragging := false
var farm_flying := false
var farm_will_land := false
var farm_flight_t := 0.0
var farm_flight_start := Vector2.ZERO
var farm_flight_end := Vector2.ZERO
var farm_pause := 0.0
var farm_landed: int = 0
var farm_loops: int = 0
var farm_complete := false
var farm_land_glow := 0.0
var farm_redraw := 0.0
var farm_vegetable_texture: Texture2D = null
var farm_vegetable_textures: Array[Texture2D] = []
var farm_food_index := 0
var farm_last_landed_food := -1
var farm_munch_t := 0.0

## Boxer mitt phrase: left/right alternate without a clock. After the third
## correct mitt a single, wordlessly demonstrated downward swipe ducks the
## counter, then the remaining three mitts continue. The duck is state, not
## scalar payout, so the phase contract remains six landed mitt taps.
const BOXER_SEQUENCE: Array[int] = [0, 1, 0, 1, 0, 1]
const BOXER_DUCK_AFTER := 3
var boxer_hit_index: int = 0
var boxer_expected: int = 0
var boxer_last_mitt: int = -1
var boxer_flash := 0.0
var boxer_hit_glow := 0.0
var boxer_duck_pending := false
var boxer_duck_done := false
var boxer_duck_distance := 0.0
var boxer_complete := false
var boxer_redraw := 0.0

## Detective case board: carry the next found clue from the evidence tray to
## its matching silhouette.  The three accepted clues remain on the board;
## a miss returns the live token and replays the same wordless demonstration.
const CLUE_BOARD_COUNT := 3
var clue_index := 0
var clue_token_pos := Vector2.ZERO
var clue_dragging := false
var clue_drag_offset := Vector2.ZERO
var clue_return_from := Vector2.ZERO
var clue_return_t := 0.0
var clue_glow := 0.0
var clue_complete := false
var clue_board_empty_texture: Texture2D = null
var clue_board_complete_texture: Texture2D = null
var clue_board_tokens_texture: Texture2D = null

## Detective crown chest: one generous handle is the whole verb.  Opening is
## stateful so the crown keeps rising during the completion hold.
var crown_opened := false
var crown_open_t := 0.0
var crown_chest_closed_texture: Texture2D = null
var crown_chest_open_texture: Texture2D = null

## Farmer planting: five deterministic holes, one live seed, and one sprout
## growth value per planted hole.  Directly tapping the glowing hole is an
## equally valid one-finger shortcut to dragging the seed there.
const GARDEN_HOLES: Array[Vector2] = [
	Vector2(0.25, 0.38), Vector2(0.50, 0.31), Vector2(0.75, 0.38),
	Vector2(0.36, 0.65), Vector2(0.64, 0.65),
]
var garden_seed_pos := Vector2.ZERO
var garden_seed_dragging := false
var garden_seed_offset := Vector2.ZERO
var garden_planted := 0
var garden_growth: Array[float] = []
var garden_seed_texture: Texture2D = null

## Magician cabinet: a direct downward handle pull opens the doors.  Sideways
## or stationary motion never pays and simply restores the same demonstration.
var cabinet_dragging := false
var cabinet_drag_start := Vector2.ZERO
var cabinet_travel := 0.0
var cabinet_open_t := 0.0
var cabinet_complete := false
var magic_cabinet_closed_texture: Texture2D = null
var magic_cabinet_reveal_texture: Texture2D = null

## Placement targets are authored anchors, not arbitrary screen stamps, for
## the five phases whose spoken fiction names distinct recipients/locations.
const TARGET_ANCHORS := {
	"target_chef": [Vector2(0.31, 0.40), Vector2(0.50, 0.34), Vector2(0.69, 0.40),
		Vector2(0.36, 0.58), Vector2(0.50, 0.54), Vector2(0.64, 0.58), Vector2(0.50, 0.70)],
	"target_candymaker": [Vector2(0.22, 0.34), Vector2(0.50, 0.31), Vector2(0.78, 0.34),
		Vector2(0.27, 0.66), Vector2(0.50, 0.70), Vector2(0.73, 0.66)],
	"target_farmer": [
		Vector2(0.37, 0.58), Vector2(0.50, 0.54), Vector2(0.63, 0.58),
	],
	"target_astronaut": [Vector2(0.31, 0.38), Vector2(0.52, 0.29), Vector2(0.70, 0.43),
		Vector2(0.43, 0.61), Vector2(0.65, 0.68)],
	"target_boxer": [Vector2(0.50, 0.52)],
}
var target_placed: Array[bool] = []
var target_piece_anim: Array[float] = []
var target_piece_textures: Array[Texture2D] = []

## Causal custom-card motion.  These values are deliberately independent of
## the career world so asset delivery can replace the fallback drawings without
## changing the one-finger contract.
const NURSERY_BOTTLE_PATH := \
	"res://assets/opera/worlds/widgets/widget_pour_nursery_mover.png"
var nursery_bottle_texture: Texture2D = null
var nursery_bottle_art_valid := false
var nursery_burp_pat_t := 0.0
var nursery_blankets_tucked: Array[bool] = []
var nursery_blanket_progress: Array[float] = []
var nursery_blanket_active := 0
var nursery_blanket_dragging := false
var nursery_blanket_drag_start := Vector2.ZERO
var magic_vanish_hat_texture: Texture2D = null
var magic_vanish_wand_texture: Texture2D = null
var magic_vanish_reveal_texture: Texture2D = null

## Directional hint for swipe phases (DUCK draws a downward arrow).
var swipe_dir := Vector2.RIGHT
## Tap phases stamp a happy mark AT THE FINGER (owner 2026-08-04: free
## placement is the game — decorating, splatting, pearl-setting; the old
## wandering hotspot rewarded chasing a dot instead of making a thing).
var tap_marks: Array = []
## Finger trail for trace phases: the reveal follows the child's own path.
var trace_points: Array = []
var trace_engaged := false
var trace_journey := 0.0
## Diegetic scene painted behind the affordance (nursery basin/bottle/cribs).
var visual_context := ""
var nursery_textures: Array[Texture2D] = []
var widget_template := ""
var widget_fill := 0.0
var widget_backdrop: Texture2D = null
var widget_mover: Texture2D = null
var widget_overlay: Texture2D = null
var widget_stamp: Texture2D = null
var widget_shared: Texture2D = null
## Magician PORTAL must never rotate either the crank family's Lamba-and-hat
## tableau or the delivered architectural doorway. The doorway stays fixed;
## only a future isolated ring (or today's code star field) may rotate.
var portal_mover_texture: Texture2D = null
var portal_ring_texture: Texture2D = null
var portal_overlay_texture: Texture2D = null
var racer_wheel_texture: Texture2D = null
var charge_astronaut_texture: Texture2D = null
var charge_popstar_texture: Texture2D = null
## Focused probes read the route last exercised by CanvasItem._draw(). Keeping
## this tiny diagnostic also makes accidental fallback to the copied generic
## spinner visible during future art swaps.
var last_contextual_draw_route := ""
var last_portal_layer_order := ""
## True between a phase being ARMED (station lit, art bound, child still
## wandering) and OPENED. Self-running clocks — oven heat, pipe fuel, the
## echo song — hold still until she actually arrives; without this the
## oven reached its toasty cap while she was still walking to the station.
var armed_only := false
## Pipe-dream tile art (ledger P1). Code-drawn until these land; the draw
## path prefers the texture whenever the face has one.
var pipe_tiles: Dictionary = {}
var pipe_tank_texture: Texture2D = null
var pipe_intake_texture: Texture2D = null
## Echo Song star pads (ledger P2), tinted per star at runtime.
var echo_unlit_texture: Texture2D = null
var echo_lit_texture: Texture2D = null
var crank_rotation := 0.0
## Trickle-by-assist (house pattern from fetch/melody/dolls): wrong input
## always celebrates but pays ~nothing, and repeat misses inside the
## cooldown pay zero — correct play must strictly beat mashing.
const MISS_COOLDOWN := {"tap": 0.5, "choice": 0.6, "timing": 1.0, "oven": 1.0}
var miss_cool := 0.0
## Swipe honesty: per-event travel cap plus a refilling per-second budget
## so scrubbing cannot trivialize goals; direction gates only when the
## phase declares one. One-way destination pushes use their own bounded lane
## state, so their demonstrated start-to-finish sweep bypasses this scrub cap.
var swipe_budget := 1.3
var swipe_require_dir := false
var long_push_engaged := false
var long_push_journey := 0.0


func _miss_pay() -> float:
	# first miss trickles a crumb; repeats inside the cooldown pay nothing
	if miss_cool > 0.0:
		return 0.0
	miss_cool = float(MISS_COOLDOWN.get(mode, 0.5))
	return 0.05


func configure(next_mode: String, next_accent: Color, choice: int = 1, next_context: String = "") -> void:
	mode = next_mode
	accent = next_accent
	target_choice = choice
	visual_context = next_context
	last_contextual_draw_route = ""
	last_portal_layer_order = ""
	# New specialist modes have an authored career backdrop even when the
	# caller uses the minimal configure(mode, accent) form. An explicit
	# context still wins, preserving the existing texture-hook API.
	if visual_context.is_empty():
		match next_mode:
			"dance_sequence":
				visual_context = "lanes_ballerina"
			"candy_sort":
				visual_context = "lanes_candymaker"
			"paint_reveal":
				visual_context = "trace_painter"
			"farm_lob":
				visual_context = "target_farmer"
			"boxer_rhythm":
				visual_context = "lanes_boxer"
			"xray_scan":
				visual_context = "target_doctor"
			"clue_board":
				visual_context = "clue_board"
			"crown_chest":
				visual_context = "crown_chest"
			"garden_plant":
				visual_context = "garden_plant"
			"magic_cabinet":
				visual_context = "magic_cabinet"
	widget_fill = 0.0
	completion_accepted = false
	feedback_t = 0.0
	feedback_positive = false
	feedback_position = 0.0
	feedback_anchor = Vector2.ZERO
	input_started = false
	crank_rotation = 0.0
	_load_widget_set()
	pour_mold_texture = null
	if visual_context == "pour_candymaker":
		# Reuse the accepted complete shell candy as the mold/fill target. The
		# old pour backdrop's copper molds are amputated at their source edge.
		pour_mold_texture = _load_widget_texture(CANDYMAKER_MOLD_PATH)
	charge_astronaut_texture = null
	charge_popstar_texture = null
	if visual_context == "charge_astronaut":
		charge_astronaut_texture = _load_widget_texture(
			"res://assets/opera/worlds/props/goal_astronaut.png")
	elif visual_context == "charge_popstar":
		charge_popstar_texture = _load_widget_texture(
			"res://assets/opera/worlds/props/goal_popstar.png")
	if (visual_context.begins_with("nursery_") or visual_context.ends_with("_nursery")) \
			and nursery_textures.is_empty():
		for index in range(3):
			var path := "res://assets/opera/worlds/nursery/baby_%d.png" % index
			var texture := load(path) as Texture2D
			if texture != null:
				nursery_textures.append(texture)
	held = false
	have_angle = false
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.4
	miss_cool = 0.0
	swipe_budget = 1.3
	swipe_require_dir = false
	long_push_engaged = false
	long_push_journey = 0.0
	swipe_dir = Vector2.RIGHT
	if _uses_long_push_context():
		# HERD and TO THE LINE are journeys to a visible destination, not generic
		# back-and-forth traces. Only a rightward swipe advances their mover.
		swipe_require_dir = true
	tap_marks = []
	trace_points = []
	trace_engaged = false
	trace_journey = 0.0
	shuffle_t = 0.0
	shuffle_from = -1
	oven_t = 0.0
	oven_peek = 0.0
	oven_done = false
	xray_scanner_pos = _xray_home_point()
	xray_dragging = false
	xray_found.clear()
	xray_found.resize(XRAY_SPOTS.size())
	xray_found.fill(false)
	xray_found_count = 0
	xray_complete = false
	xray_glow = 0.0
	xray_redraw = 0.0
	dance_show_index = -1
	dance_show_start = 0
	dance_show_t = 0.0
	dance_input_index = 0
	dance_listening = false
	dance_complete = false
	dance_last_pad = -1
	dance_glow = 0.0
	dance_redraw = 0.0
	candy_piece_index = 0
	candy_type = int(CANDY_SEQUENCE[0])
	candy_position = _candy_spawn_point()
	candy_drag_offset = Vector2.ZERO
	candy_dragging = false
	candy_sorted = 0
	candy_complete = false
	candy_loops = 0
	candy_last_bin = -1
	candy_glow = 0.0
	candy_redraw = 0.0
	paint_cells.clear()
	paint_cells.resize(PAINT_GRID_COLS * PAINT_GRID_ROWS)
	paint_cells.fill(false)
	paint_covered = 0
	paint_dragging = false
	paint_last_point = Vector2.ZERO
	paint_complete = false
	farm_piece_position = _farm_anchor_point()
	farm_drag_offset = Vector2.ZERO
	farm_dragging = false
	farm_flying = false
	farm_will_land = false
	farm_flight_t = 0.0
	farm_flight_start = farm_piece_position
	farm_flight_end = farm_piece_position
	farm_pause = 0.0
	farm_landed = 0
	farm_loops = 0
	farm_complete = false
	farm_land_glow = 0.0
	farm_redraw = 0.0
	farm_food_index = 0
	farm_last_landed_food = -1
	farm_munch_t = 0.0
	boxer_hit_index = 0
	boxer_expected = int(BOXER_SEQUENCE[0])
	boxer_last_mitt = -1
	boxer_flash = 1.2
	boxer_hit_glow = 0.0
	boxer_duck_pending = false
	boxer_duck_done = false
	boxer_duck_distance = 0.0
	boxer_complete = false
	boxer_redraw = 0.0
	clue_index = 0
	clue_token_pos = _clue_home_point()
	clue_dragging = false
	clue_drag_offset = Vector2.ZERO
	clue_return_from = clue_token_pos
	clue_return_t = 0.0
	clue_glow = 0.0
	clue_complete = false
	crown_opened = false
	crown_open_t = 0.0
	garden_seed_pos = _garden_seed_home()
	garden_seed_dragging = false
	garden_seed_offset = Vector2.ZERO
	garden_planted = 0
	garden_growth.clear()
	garden_growth.resize(GARDEN_HOLES.size())
	garden_growth.fill(0.0)
	cabinet_dragging = false
	cabinet_drag_start = Vector2.ZERO
	cabinet_travel = 0.0
	cabinet_open_t = 0.0
	cabinet_complete = false
	target_placed.clear()
	target_piece_anim.clear()
	target_piece_textures.clear()
	if _uses_anchored_targets():
		var anchor_count := _target_anchor_count()
		target_placed.resize(anchor_count)
		target_placed.fill(false)
		target_piece_anim.resize(anchor_count)
		target_piece_anim.fill(0.0)
		var career := visual_context.trim_prefix("target_")
		target_piece_textures.resize(3)
		for piece_index in range(3):
			var piece: Texture2D = _load_widget_texture(
				"res://assets/opera/worlds/widgets/widget_target_%s_piece_%d.png" \
				% [career, piece_index])
			target_piece_textures[piece_index] = piece
	nursery_burp_pat_t = 0.0
	nursery_blankets_tucked.clear()
	nursery_blankets_tucked.resize(3)
	nursery_blankets_tucked.fill(false)
	nursery_blanket_progress.clear()
	nursery_blanket_progress.resize(3)
	nursery_blanket_progress.fill(0.0)
	nursery_blanket_active = 0
	nursery_blanket_dragging = false
	nursery_blanket_drag_start = Vector2.ZERO
	nursery_bottle_texture = null
	nursery_bottle_art_valid = false
	if _is_nursery_feed_context():
		nursery_bottle_texture = _load_widget_texture(NURSERY_BOTTLE_PATH)
		nursery_bottle_art_valid = nursery_bottle_texture != null \
			and nursery_bottle_texture.resource_path == NURSERY_BOTTLE_PATH \
			and nursery_bottle_texture.get_size() == Vector2(256.0, 256.0)
	magic_vanish_hat_texture = null
	magic_vanish_wand_texture = null
	magic_vanish_reveal_texture = null
	if _is_magic_vanish_context():
		magic_vanish_hat_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_magic_vanish_hat.png")
		magic_vanish_wand_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_magic_vanish_wand.png")
		magic_vanish_reveal_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_magic_vanish_reveal.png")
	if next_mode == "clue_board":
		clue_board_empty_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_clue_board_empty.png")
		clue_board_complete_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_clue_board_complete.png")
		clue_board_tokens_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_clue_board_tokens.png")
	if next_mode == "crown_chest":
		crown_chest_closed_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_crown_chest_closed.png")
		crown_chest_open_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_crown_chest_open.png")
	if next_mode == "garden_plant":
		garden_seed_texture = _load_widget_texture("res://assets/mg/seed.png")
	if next_mode == "magic_cabinet":
		magic_cabinet_closed_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_magic_cabinet_closed.png")
		magic_cabinet_reveal_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_magic_cabinet_reveal.png")
	portal_mover_texture = null
	portal_ring_texture = null
	portal_overlay_texture = null
	racer_wheel_texture = null
	if _is_magician_portal_context():
		for portal_mover_path: String in [
			"res://assets/opera/worlds/widgets/widget_portal_magician_mover.png",
			"res://assets/opera/worlds/widgets/widget_crank_magician_portal_mover.png",
		]:
			portal_mover_texture = _load_widget_texture(portal_mover_path)
			if portal_mover_texture != null:
				break
		for portal_ring_path: String in [
			"res://assets/opera/worlds/widgets/widget_portal_magician_ring.png",
			"res://assets/opera/worlds/widgets/widget_crank_magician_portal_ring.png",
		]:
			portal_ring_texture = _load_widget_texture(portal_ring_path)
			if portal_ring_texture != null:
				break
		for portal_overlay_path: String in [
			"res://assets/opera/worlds/widgets/widget_portal_magician_overlay.png",
			"res://assets/opera/worlds/widgets/widget_crank_magician_portal_overlay.png",
		]:
			portal_overlay_texture = _load_widget_texture(portal_overlay_path)
			if portal_overlay_texture != null:
				break
		# The shipped crank progress file is already an isolated gold portal ring,
		# unlike the unsafe mover. Reuse it until a dedicated overlay supersedes it.
		if portal_overlay_texture == null:
			portal_overlay_texture = widget_overlay
	if _is_racer_tune_context():
		racer_wheel_texture = _load_widget_texture(
			"res://assets/opera/worlds/widgets/widget_crank_racer_wheel.png")
	if next_mode == "dance_sequence":
		_dance_restart_show(0.32)
	if next_mode == "candy_sort":
		_candy_reset_piece(false)
	if next_mode == "paint_reveal" and paint_reveal_texture == null:
		paint_reveal_texture = _load_widget_texture(
			"res://assets/opera/worlds/props/goal_painter.png")
	if next_mode == "farm_lob":
		farm_vegetable_textures.clear()
		for food_index in range(3):
			var food := _load_widget_texture(
				"res://assets/opera/worlds/widgets/widget_target_farmer_piece_%d.png" \
				% food_index)
			if food != null:
				farm_vegetable_textures.append(food)
		if farm_vegetable_texture == null:
			farm_vegetable_texture = _load_widget_texture(
				"res://assets/opera/worlds/props/goal_farmer.png")
	if next_mode == "pipe":
		pipe_round = 0
		_pipe_setup_round()
		if pipe_tiles.is_empty():
			var faces := {
				"H": "tile_h", "V": "tile_v", "NE": "elbow_ne",
				"NW": "elbow_nw", "SE": "elbow_se", "SW": "elbow_sw",
			}
			for face: String in faces.keys():
				var tile := _load_widget_texture(
					"res://assets/opera/worlds/widgets/widget_pipe_%s.png" % faces[face])
				if tile != null:
					pipe_tiles[face] = tile
			pipe_tank_texture = _load_widget_texture("res://assets/opera/worlds/widgets/widget_pipe_tank.png")
			pipe_intake_texture = _load_widget_texture("res://assets/opera/worlds/widgets/widget_pipe_intake.png")
	if next_mode == "echo" and echo_unlit_texture == null:
		echo_unlit_texture = _load_widget_texture("res://assets/opera/worlds/widgets/popstar_star_note_unlit.png")
		echo_lit_texture = _load_widget_texture("res://assets/opera/worlds/widgets/popstar_star_note_lit.png")
	if next_mode == "echo":
		echo_verse = 0
		echo_show_i = -1
		echo_show_t = 0.0
		echo_input_i = 0
		echo_listening = false
		echo_glow = 0.0
	if next_mode == "pourt":
		pour_tilt = 0.0
		pour_x = _pour_home_x()
		pour_level = 0.0
		pour_reserve = 1.2
		pour_hold = false
		pour_emit_acc = 0.0
	if next_mode != "bop":
		bop_targets = []
	queue_redraw()


func _load_widget_texture(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _load_widget_set() -> void:
	widget_template = visual_context.get_slice("_", 0) if not visual_context.is_empty() else ""
	widget_backdrop = null
	widget_mover = null
	widget_overlay = null
	widget_stamp = null
	widget_shared = null
	if widget_template.is_empty():
		return
	var prefix := "res://assets/opera/worlds/widgets/widget_%s" % visual_context
	widget_backdrop = _load_widget_texture("%s.png" % prefix)
	match widget_template:
		"gauge":
			widget_mover = _load_widget_texture("res://assets/opera/worlds/widgets/widget_gauge_shared_needle.png")
			widget_overlay = _load_widget_texture("%s_success.png" % prefix)
		"track":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_track_shared_hit.png")
		"pour":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_overlay = _load_widget_texture("%s_fill.png" % prefix)
		"basin":
			widget_overlay = _load_widget_texture("%s_bubbles.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_basin_shared_shine.png")
		"charge":
			widget_mover = _load_widget_texture("%s_glow.png" % prefix)
			widget_overlay = _load_widget_texture("%s_full.png" % prefix)
		"crank":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_overlay = _load_widget_texture("%s_progress.png" % prefix)
		"trace":
			widget_overlay = _load_widget_texture("%s_lit.png" % prefix)
		"push":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			var down := visual_context.ends_with("_boxer") or visual_context.ends_with("_nursery")
			var shared_name := "arrow_down" if down else "arrow_lr"
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_push_shared_%s.png" % shared_name)
		"target":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_stamp = _load_widget_texture("%s_mark.png" % prefix)
			widget_overlay = _load_widget_texture("%s_success.png" % prefix)
		"lanes":
			widget_mover = _load_widget_texture("%s_lit.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_lanes_shared_pick.png")


func note_input() -> void:
	input_started = true
	demo_active = false
	queue_redraw()


func note_result(accepted: bool) -> void:
	feedback_positive = accepted
	feedback_t = 0.32
	queue_redraw()


func accept_completion() -> void:
	completion_accepted = true
	feedback_positive = true
	feedback_t = maxf(feedback_t, 0.32)
	queue_redraw()


func restart_demo() -> void:
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.2
	if mode == "dance_sequence" and not dance_complete:
		# The phrase itself is the instruction. Rehints therefore replay all
		# four pads instead of pointing at a static center finger.
		_dance_restart_show(0.22)
	queue_redraw()


func reflash_choice() -> void:
	choice_flash = 1.2
	queue_redraw()


func _process(delta: float) -> void:
	if miss_cool > 0.0:
		miss_cool = maxf(0.0, miss_cool - delta)
	swipe_budget = minf(1.3, swipe_budget + delta * 1.3)
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - delta)
		queue_redraw()
	if choice_flash > 0.0 and mode == "choice":
		choice_flash -= delta
		if choice_flash <= 0.0:
			queue_redraw()
	if shuffle_t > 0.0 and mode == "choice":
		shuffle_t = maxf(0.0, shuffle_t - delta)
		queue_redraw()
	if mode == "pipe" and not completion_accepted and not armed_only:
		_pipe_tick(delta)
	if mode == "echo" and not completion_accepted and not armed_only:
		_echo_tick(delta)
	if mode == "pourt" and not armed_only:
		_pour_tick(delta)
	if mode == "xray_scan" and not completion_accepted and not armed_only:
		_xray_tick(delta)
	if mode == "dance_sequence" and not completion_accepted and not armed_only:
		_dance_tick(delta)
	if mode == "candy_sort" and not completion_accepted and not armed_only:
		_candy_tick(delta)
	if mode == "farm_lob" and not completion_accepted and not armed_only:
		_farm_tick(delta)
	if mode == "boxer_rhythm" and not completion_accepted and not armed_only:
		_boxer_tick(delta)
	if mode == "clue_board":
		_clue_tick(delta)
	if mode == "crown_chest":
		_crown_tick(delta)
	if mode == "garden_plant":
		_garden_tick(delta)
	if mode == "magic_cabinet":
		_cabinet_tick(delta)
	if mode == "tap" and _uses_anchored_targets():
		_target_tick(delta)
	if nursery_burp_pat_t > 0.0:
		nursery_burp_pat_t = maxf(0.0, nursery_burp_pat_t - delta)
		queue_redraw()
	if mode == "oven" and not completion_accepted and not armed_only:
		if oven_peek > 0.0:
			# door open for a peek — the heat politely waits
			oven_peek = maxf(0.0, oven_peek - delta)
		elif not oven_done:
			# STATIC rate: cold to a kind toasty cap in 8s. At cap the cake
			# waits indefinitely for the real mitt-handle tap: no passive win.
			oven_t = minf(1.0, oven_t + delta / 8.0)
		oven_redraw += delta
		if oven_redraw >= 0.05:
			oven_redraw = 0.0
			queue_redraw()
	if not demo_active:
		return
	demo_t += delta
	_demo_redraw += delta
	if _demo_redraw >= 0.05:
		_demo_redraw = 0.0
		queue_redraw()


func set_bop_targets(targets: Array) -> void:
	bop_targets = targets
	queue_redraw()


func bop_remaining() -> int:
	var left := 0
	for target: Dictionary in bop_targets:
		if not bool(target.get("popped", false)):
			left += 1
	return left


func set_timing_position(value: float) -> void:
	timing_position = clampf(value, 0.0, 1.0)
	if mode == "timing":
		queue_redraw()


func set_fill(value: float) -> void:
	widget_fill = clampf(value, 0.0, 1.0)
	if _uses_long_push_context():
		long_push_journey = widget_fill
	if _uses_authored_trace_context():
		trace_journey = widget_fill
	queue_redraw()


func _press(at: Vector2) -> void:
	note_input()
	held = true
	pointer_pos = at
	previous_pos = at
	previous_angle = (at - size * 0.5).angle()
	have_angle = true
	_last_spin = 0.0
	feedback_anchor = at
	feedback_position = timing_position
	match mode:
		"tap":
			if _uses_anchored_targets():
				_target_press(at)
			else:
				# Painter keeps true free placement; nursery BURP turns the same
				# payout into a visible pat instead of a false timing meter.
				tap_marks.append(at)
				if _is_nursery_burp_context():
					nursery_burp_pat_t = 0.42
				gesture.emit("tap", 1.0, 1.0)
		"choice":
			var lane := clampi(int(at.x / maxf(1.0, size.x) * float(choice_count)), 0, choice_count - 1)
			if lane == target_choice:
				gesture.emit("choice", 1.0, 1.0)
			else:
				gesture.emit("choice", _miss_pay(), 0.0)
		"timing":
			if timing_position >= timing_zone.x and timing_position <= timing_zone.y:
				gesture.emit("timing", 1.0, 1.0)
			else:
				gesture.emit("timing", _miss_pay(), 0.32)
		"bop":
			_bop_press(at)
		"pipe":
			if completion_accepted:
				gesture.emit("pipe", 0.0, 1.0)   # skips the completion hold
			else:
				_pipe_press(at)
		"echo":
			if completion_accepted:
				gesture.emit("echo", 0.0, 1.0)
			else:
				_echo_press(at)
		"pourt":
			if _pour_pitcher_hit_rect().has_point(at):
				pour_hold = true
				# Candymaker keeps the jug registered over its pictured mold when the
				# child grabs any part of the generous target. Dragging can still move
				# it, but never into a visible-yet-nonpaying dead zone.
				if not _is_candymaker_pour():
					var bounds := _pour_x_bounds()
					pour_x = clampf(at.x, bounds.x, bounds.y)
			else:
				# a tap on the bowl answers with a friendly ripple
				pour_hold = false
				gesture.emit("pourt", 0.0, 0.6)
		"oven":
			if oven_done or completion_accepted:
				gesture.emit("oven", 0.0, 1.0)
			elif not _oven_handle_hit_rect().has_point(at):
				# The rest of the card is a safe rehint only. It can never remove
				# the cake merely because the heat happens to be golden.
				feedback_positive = false
				feedback_t = 0.24
				demo_active = true
				demo_t = 0.0
				gesture.emit("oven", 0.0, 0.4)
			elif oven_t < 0.45:
				# a peek: door opens, the cake jiggles gooey, baking resumes.
				# Mashing neither pays NOR peeks — a drumming finger cannot
				# hold the door open and freeze the bake clock.
				var pay := _miss_pay()
				if pay > 0.0:
					oven_peek = 0.7
				demo_active = true
				demo_t = 0.0
				gesture.emit("oven", pay, 0.55)
			else:
				# she takes the cake out — golden is perfect, toasty is still
				# wonderful, and the difference is only the confetti's size
				oven_done = true
				gesture.emit("oven", 999.0, 1.0 if oven_t <= 0.80 else 0.7)
		"xray_scan":
			_xray_press(at)
		"dance_sequence":
			_dance_press(at)
		"candy_sort":
			_candy_press(at)
		"paint_reveal":
			_paint_press(at)
		"farm_lob":
			_farm_press(at)
		"boxer_rhythm":
			_boxer_press(at)
		"clue_board":
			_clue_press(at)
		"crown_chest":
			_crown_press(at)
		"garden_plant":
			_garden_press(at)
		"magic_cabinet":
			_cabinet_press(at)
		"hold":
			# Pressing arms the hold; the career-world tick pays only while the
			# finger remains down. A drum of stationary taps must not substitute
			# for the sustained verb.
			pass
		"swipe":
			# These verbs pay from qualifying motion in _drag(), never from the
			# initial stationary press. The idle rehint still restarts the demo.
			if _uses_authored_trace_context():
				trace_engaged = _trace_start_hit_rect().has_point(at)
				if not trace_engaged:
					_trace_rehint(at)
			elif _is_nursery_bedtime_context():
				_nursery_bedtime_press(at)
			elif _uses_long_push_context():
				long_push_engaged = _long_push_start_hit_rect().has_point(at)
				if not long_push_engaged:
					demo_active = true
					demo_t = 0.0
					gesture.emit("swipe", 0.0, 0.35)
		"circle":
			pass
	queue_redraw()


func _bop_press(at: Vector2) -> void:
	for target: Dictionary in bop_targets:
		if bool(target.get("popped", false)):
			continue
		var pos: Vector2 = target.get("pos", Vector2.ZERO)
		var reach := float(target.get("r", 44.0)) * 1.45
		if at.distance_to(pos) <= reach:
			target["hp"] = int(target.get("hp", 1)) - 1
			last_bop_pos = pos
			if int(target["hp"]) <= 0:
				target["popped"] = true
			gesture.emit("bop", 1.0, 1.0)
			return
	# a stray tap fizzles kindly and still trickles a little progress
	last_bop_pos = at
	gesture.emit("bop", 0.12, 0.2)


func _drag(at: Vector2) -> void:
	note_input()
	pointer_pos = at
	var distance := at.distance_to(previous_pos)
	if mode == "xray_scan":
		_xray_drag(at)
		previous_pos = at
		return
	if mode == "farm_lob":
		_farm_drag(at)
		previous_pos = at
		return
	if mode == "boxer_rhythm":
		_boxer_drag(at)
		previous_pos = at
		return
	if mode == "candy_sort":
		_candy_drag(at)
		previous_pos = at
		return
	if mode == "paint_reveal":
		_paint_drag(at)
		previous_pos = at
		return
	if mode == "clue_board":
		_clue_drag(at)
		previous_pos = at
		return
	if mode == "garden_plant":
		_garden_drag(at)
		previous_pos = at
		return
	if mode == "magic_cabinet":
		_cabinet_drag(at)
		previous_pos = at
		return
	if mode == "swipe" and _is_nursery_bedtime_context():
		_nursery_bedtime_drag(at)
		previous_pos = at
		return
	if mode == "swipe" and _uses_authored_trace_context():
		_authored_trace_drag(at)
		queue_redraw()
		return
	if mode == "swipe" and distance > 0.0:
		var travel := minf(distance, 34.0) / 150.0
		if not _uses_long_push_context():
			travel = minf(travel, swipe_budget)
		if travel > 0.0:
			var aligned := 1.0
			if swipe_require_dir:
				aligned = maxf(0.0, (at - previous_pos).normalized().dot(swipe_dir))
			var trace_allowed := not _uses_authored_trace_context() \
				or _trace_segment_on_corridor(previous_pos, at)
			var long_push_allowed := not _uses_long_push_context() or long_push_engaged
			if aligned >= 0.35 and trace_allowed and long_push_allowed:
				# Spend the motion allowance only after useful travel. A child can
				# stray, see the rehint, and immediately correct with the same swipe.
				if not _uses_long_push_context():
					swipe_budget -= travel
				if _uses_long_push_context():
					var lane := _long_push_end() - _long_push_start()
					var lane_delta := maxf(0.0, (at - previous_pos).dot(lane.normalized())) \
						/ maxf(1.0, lane.length())
					var next_journey := minf(1.0, long_push_journey + lane_delta)
					var journey_delta := next_journey - long_push_journey
					long_push_journey = next_journey
					widget_fill = long_push_journey
					gesture.emit("swipe", journey_delta * _long_push_goal_units(), 1.0)
				else:
					gesture.emit("swipe", travel, 1.0)
			else:
				# Long destination pushes require honest travel toward the visible
				# gate/arch. Wrong-direction motion rehints but cannot move the prop.
				var hard_gate := _uses_long_push_context() or _uses_authored_trace_context()
				var wrong_amount := 0.0 if hard_gate else travel * 0.2
				if hard_gate:
					demo_active = true
					demo_t = 0.0
				else:
					swipe_budget -= travel
				gesture.emit("swipe", wrong_amount, 0.4)
	if mode == "pipe":
		queue_redraw()
		previous_pos = at
		return
	if mode == "pourt":
		if pour_hold:
			var bounds := _pour_x_bounds()
			pour_x = clampf(at.x, bounds.x, bounds.y)
		queue_redraw()
		previous_pos = at
		return
	if mode == "swipe" and widget_template == "trace":
		var record_trace := not _uses_authored_trace_context() \
			or _trace_segment_on_corridor(previous_pos, at)
		if record_trace:
			if trace_points.is_empty():
				trace_points.append(previous_pos)
			if at.distance_to(trace_points[trace_points.size() - 1]) > 24.0:
				trace_points.append(at)
	elif mode == "circle":
		var center := size * 0.5
		var radius := at.distance_to(center)
		if radius > minf(size.x, size.y) * 0.13:
			var angle := (at - center).angle()
			if have_angle:
				var change := wrapf(angle - previous_angle, -PI, PI)
				crank_rotation = angle
				# straight-line scrubs cross the center as big sign-flipping
				# jumps; honest circling is small same-sign steps
				if absf(change) <= 0.9 and signf(change) == signf(_last_spin) and absf(_last_spin) > 0.0001:
					gesture.emit("circle", absf(change) / TAU, 1.0)
				_last_spin = change
			previous_angle = angle
			have_angle = true
	previous_pos = at
	queue_redraw()


func _release(at: Vector2) -> void:
	held = false
	pointer_pos = at
	have_angle = false
	long_push_engaged = false
	if mode == "pipe":
		_pipe_release(at)
	if mode == "pourt":
		pour_hold = false
	if mode == "xray_scan":
		_xray_release()
	if mode == "candy_sort":
		_candy_release(at)
	if mode == "paint_reveal":
		_paint_release()
	if mode == "farm_lob":
		_farm_release(at)
	if mode == "boxer_rhythm":
		_boxer_release()
	if mode == "clue_board":
		_clue_release(at)
	if mode == "garden_plant":
		_garden_release(at)
	if mode == "magic_cabinet":
		_cabinet_release()
	if mode == "swipe" and _is_nursery_bedtime_context():
		_nursery_bedtime_release()
	if mode == "swipe" and _uses_authored_trace_context():
		trace_engaged = false
		if trace_journey < 0.999 and not completion_accepted:
			demo_active = true
			demo_t = 0.0
	if mode == "hold" and widget_fill > 0.22:
		# the wind-up pays off on release — the hop, the swell, the flourish
		gesture.emit("hold_release", 0.0, 1.0)
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_press(touch.position)
		else:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_drag(drag.position)
		accept_event()
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION:
			return  # already handled as the touch event on tablets
		if button.pressed:
			_press(button.position)
		else:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and held:
		if (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _draw() -> void:
	var panel := Rect2(Vector2.ZERO, size)
	# light paper inset window per the StorybookUI language
	draw_rect(panel, Color(0.94, 0.97, 1.0, 0.96), true)
	draw_rect(panel.grow(-3.0), accent.lerp(Color("#382485"), 0.62), false, 4.0)
	var center := size * 0.5
	if mode == "pipe":
		_draw_pipe()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "echo":
		_draw_echo(center)
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "pourt":
		_draw_pour_scene(center)
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "oven":
		_draw_oven(center)
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "xray_scan":
		_draw_xray_scan()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "dance_sequence":
		_draw_dance_sequence()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "candy_sort":
		_draw_candy_sort()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "paint_reveal":
		_draw_paint_reveal()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "farm_lob":
		_draw_farm_lob()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "boxer_rhythm":
		_draw_boxer_rhythm()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "clue_board":
		_draw_clue_board()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "crown_chest":
		_draw_crown_chest()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "garden_plant":
		_draw_garden_plant()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "magic_cabinet":
		_draw_magic_cabinet()
		if demo_active:
			_draw_demo_finger()
		return
	if _draw_causal_context(center):
		if demo_active:
			_draw_demo_finger()
		return
	if widget_backdrop != null:
		# authored at 1024x608 (1.684); the panel is not that aspect, so a plain
		# stretch squashed every round object into an egg. Cover-fit instead.
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
		_draw_widget_layers(center)
		if demo_active:
			_draw_demo_finger()
		return
	if visual_context.begins_with("nursery"):
		_draw_nursery_context(center)
		if demo_active:
			_draw_demo_finger()
		return
	match mode:
		"tap":
			# free placement: the marks ARE the picture; no hotspot to chase.
			# The ghost-finger demo teaches "touch here makes a mark".
			for mark: Vector2 in tap_marks:
				draw_circle(mark, 13.0, Color(accent, 0.85))
				draw_circle(mark, 6.0, Color.WHITE)
			if held:
				draw_circle(pointer_pos, 26.0, Color(accent, 0.35))
		"hold":
			draw_circle(center, minf(size.x, size.y) * 0.25, Color(accent, 0.24))
			draw_arc(center, minf(size.x, size.y) * 0.25, 0.0, TAU, 48, accent, 10.0)
			draw_circle(center, 24.0 if held else 16.0, Color.WHITE)
		"swipe":
			var span := minf(size.x, size.y) * 0.42
			var tail := center - swipe_dir * span
			var head := center + swipe_dir * span
			var side := swipe_dir.orthogonal()
			draw_line(tail, head, accent, 16.0, true)
			draw_colored_polygon(PackedVector2Array([
				head + side * 34.0, head + swipe_dir * 58.0, head - side * 34.0,
			]), accent)
			draw_circle(tail, 22.0, Color.WHITE)
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			draw_arc(center, radius, -2.7, 2.2, 48, accent, 16.0)
			var tip := center + Vector2.from_angle(2.2) * radius
			draw_colored_polygon(PackedVector2Array([
				tip, tip + Vector2(-10, -36), tip + Vector2(30, -14),
			]), accent)
		"choice":
			var show_answer := choice_flash > 0.0 or demo_active
			for index in range(choice_count):
				var point := Vector2(size.x * (float(index) + 0.5) / float(choice_count), center.y)
				var is_answer := index == target_choice and show_answer
				var colour := Color(1.0, 0.86, 0.32) if is_answer else Color(0.34, 0.42, 0.62)
				draw_circle(point, 54.0, Color(colour, 0.34))
				draw_arc(point, 54.0, 0.0, TAU, 36, colour, 9.0)
				if is_answer:
					draw_circle(point, 15.0, Color.WHITE)
		"timing":
			var bar := Rect2(size.x * 0.12, center.y - 23.0, size.x * 0.76, 46.0)
			draw_rect(bar, Color(0.2, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 28.0), Vector2(marker_x, bar.end.y + 28.0), Color.WHITE, 12.0)
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					_draw_imp(target)
	if demo_active:
		_draw_demo_finger()


## Overlay ink bounds, cached per texture: the reveal must sweep the PAINTED
## band, not the whole 608px canvas. Sweeping the canvas made the pour
## saturate at 43% of the hold and then sit frozen — the exact playtest
## complaint ("no animation, no feedback").
var _ink_cache: Dictionary = {}


func _ink_bounds(texture: Texture2D) -> Vector2:
	var key := texture.resource_path
	if _ink_cache.has(key):
		return _ink_cache[key]
	var bounds := Vector2(0.0, 1.0)
	var image := texture.get_image()
	if image != null:
		var h := image.get_height()
		var w := image.get_width()
		var top := -1
		var bottom := -1
		for y in range(h):
			var painted := false
			for x in range(0, w, 4):
				if image.get_pixel(x, y).a > 0.08:
					painted = true
					break
			if painted:
				if top < 0:
					top = y
				bottom = y
		if top >= 0 and bottom > top:
			bounds = Vector2(float(top) / float(h), float(bottom + 1) / float(h))
	_ink_cache[key] = bounds
	return bounds


## Aspect-preserving cover rect: fills the panel, centred, never distorted.
func _cover_rect(texture: Texture2D) -> Rect2:
	var tex := texture.get_size()
	if tex.x <= 0.0 or tex.y <= 0.0:
		return Rect2(Vector2.ZERO, size)
	var scale := maxf(size.x / tex.x, size.y / tex.y)
	var drawn := tex * scale
	return Rect2((size - drawn) * 0.5, drawn)


func _draw_progress_overlay(texture: Texture2D, progress: float, horizontal: bool) -> void:
	var amount := clampf(progress, 0.0, 1.0)
	if amount <= 0.0:
		return
	var texture_size := texture.get_size()
	if horizontal:
		var source := Rect2(0.0, 0.0, texture_size.x * amount, texture_size.y)
		var destination := Rect2(0.0, 0.0, size.x * amount, size.y)
		draw_texture_rect_region(texture, destination, source)
		return
	# sweep the reveal edge across the ink band so 0%..100% of the hold maps
	# to 0%..100% of the visible liquid
	var ink := _ink_bounds(texture)
	var ink_top := ink.x
	var ink_bottom := ink.y
	var edge := ink_bottom - (ink_bottom - ink_top) * amount
	var source_y := texture_size.y * edge
	var source_h := texture_size.y * (ink_bottom - edge)
	if source_h <= 0.0:
		return
	var cover := _cover_rect(texture)
	var destination_y := cover.position.y + cover.size.y * edge
	var destination_h := cover.size.y * (ink_bottom - edge)
	draw_texture_rect_region(
		texture,
		Rect2(cover.position.x, destination_y, cover.size.x, destination_h),
		Rect2(0.0, source_y, texture_size.x, source_h)
	)


func _draw_widget_sprite(texture: Texture2D, center: Vector2, side: float, modulate := Color.WHITE) -> void:
	if texture == null:
		return
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side), false, modulate)


func _uses_long_push_context() -> bool:
	return mode == "swipe" and visual_context in ["push_farmer", "push_racer"]


func _long_push_goal_units() -> float:
	# Current shipping contracts are HERD 6 and TO THE LINE 5. Mapping the
	# complete pictured lane to that contract lets one continuous sweep move the
	# object all the way to its visible destination instead of requiring repeats.
	return 6.0 if visual_context == "push_farmer" else 5.0


func _long_push_actor_count() -> int:
	return 3 if visual_context == "push_farmer" else 1


func _long_push_start() -> Vector2:
	return Vector2(size.x * 0.16, size.y * 0.66)


func _long_push_end() -> Vector2:
	return Vector2(size.x * 0.84, size.y * 0.66)


func _long_push_position(progress: float) -> Vector2:
	var amount := clampf(progress, 0.0, 1.0)
	var eased := amount * amount * (3.0 - 2.0 * amount)
	return _long_push_start().lerp(_long_push_end(), eased)


func _long_push_mover_rect(progress: float) -> Rect2:
	if visual_context == "push_farmer":
		return _long_push_group_rect(progress)
	var side := minf(size.x * 0.25, size.y * 0.46)
	return Rect2(_long_push_position(progress) - Vector2.ONE * side * 0.5,
		Vector2.ONE * side)


func _long_push_group_rect(progress: float) -> Rect2:
	var group_size := Vector2(
		minf(size.x * 0.28, size.y * 0.48),
		minf(size.x * 0.25, size.y * 0.44))
	return Rect2(_long_push_position(progress) - group_size * 0.5, group_size)


func _long_push_start_hit_rect() -> Rect2:
	return _long_push_mover_rect(widget_fill).grow(
		maxf(24.0, minf(size.x, size.y) * 0.08)).intersection(
			Rect2(Vector2.ZERO, size))


func _draw_farmer_pig_group(progress: float) -> void:
	var group := _long_push_group_rect(progress)
	var center := group.get_center()
	var offsets: Array[Vector2] = [
		Vector2(-group.size.x * 0.24, group.size.y * 0.08),
		Vector2(0.0, -group.size.y * 0.09),
		Vector2(group.size.x * 0.24, group.size.y * 0.08),
	]
	for pig_index in range(offsets.size()):
		var pig_side := group.size.y * (0.54 if pig_index == 1 else 0.48)
		var pig_center := center + offsets[pig_index]
		if widget_mover != null:
			draw_texture_rect(widget_mover,
				Rect2(pig_center - Vector2.ONE * pig_side * 0.5,
					Vector2.ONE * pig_side), false)
		else:
			draw_set_transform(pig_center, 0.0, Vector2(1.22, 0.86))
			draw_circle(Vector2.ZERO, pig_side * 0.31, Color("#efaa9e"))
			draw_set_transform(Vector2.ZERO)
			draw_circle(pig_center + Vector2(pig_side * 0.23, 0.0),
				pig_side * 0.14, Color("#f5bdaf"))
			draw_circle(pig_center + Vector2(pig_side * 0.26, -pig_side * 0.025),
				pig_side * 0.026, Color("#6b4561"))
	if completion_accepted or progress >= 0.999:
		for pig_index in range(offsets.size()):
			draw_circle(center + offsets[pig_index] - Vector2(0.0, group.size.y * 0.35),
				3.0 + float(pig_index), Color("#ffe17a"))


func _draw_long_push() -> void:
	last_contextual_draw_route = "push:%s" % visual_context
	var playfield := Rect2(size.x * 0.055, size.y * 0.13,
		size.x * 0.89, size.y * 0.76)
	var farmer := visual_context == "push_farmer"
	var paper := Color("#eef7e8") if farmer else Color("#edf3ff")
	var ground := Color("#a7cf83") if farmer else Color("#b5c9e8")
	# The old backdrops paint a second static pig/kart in the middle. A clean
	# themed playfield over the card interior makes the approved isolated mover
	# the sole game object and gives its 68%-width journey a readable start/end.
	draw_rect(playfield, paper, true)
	draw_rect(playfield, Color("#3b2a68"), false, 4.0)
	draw_rect(Rect2(playfield.position.x, size.y * 0.59,
		playfield.size.x, size.y * 0.30), ground, true)
	var start := _long_push_start()
	var finish := _long_push_end()
	var position := _long_push_position(widget_fill)
	draw_line(start, finish, Color(0.28, 0.25, 0.46, 0.25), 14.0, true)
	draw_line(start, position, accent, 12.0, true)
	draw_circle(start, 13.0, Color(1.0, 1.0, 1.0, 0.88))
	draw_arc(start, 20.0, 0.0, TAU, 28, accent, 4.0)
	if farmer:
		# Barn gate destination.
		var post_color := Color("#9b613e")
		for post_sign: float in [-1.0, 1.0]:
			var post_x := finish.x + post_sign * size.x * 0.075
			draw_rect(Rect2(post_x - 8.0, size.y * 0.28, 16.0, size.y * 0.43),
				post_color, true)
		draw_line(Vector2(finish.x - size.x * 0.075, size.y * 0.31),
			Vector2(finish.x + size.x * 0.075, size.y * 0.31), post_color, 16.0, true)
		if widget_fill < 0.98:
			draw_line(Vector2(finish.x - size.x * 0.065, size.y * 0.50),
				Vector2(finish.x + size.x * 0.065, size.y * 0.50),
				Color("#d39a60"), 11.0, true)
	else:
		# Pearl starting arch destination.
		var arch_color := Color("#f2d57a")
		var arch_radius := size.x * 0.085
		draw_line(finish - Vector2(arch_radius, 0.0),
			finish - Vector2(arch_radius, size.y * 0.20), arch_color, 12.0, true)
		draw_line(finish + Vector2(arch_radius, 0.0),
			finish + Vector2(arch_radius, -size.y * 0.20), arch_color, 12.0, true)
		draw_arc(finish - Vector2(0.0, size.y * 0.20), arch_radius,
			PI, TAU, 32, arch_color, 12.0)
	# The mover advances from scalar progress generated only by aligned real
	# swipes; accepted completion leaves it parked at the destination.
	if farmer:
		_draw_farmer_pig_group(widget_fill)
	elif widget_mover != null:
		draw_texture_rect(widget_mover, _long_push_mover_rect(widget_fill), false)
	else:
		var fallback_rect := _long_push_mover_rect(widget_fill)
		draw_circle(fallback_rect.get_center(), fallback_rect.size.x * 0.34,
			Color("#efaa82") if farmer else Color("#ed7778"))
	if completion_accepted or widget_fill >= 0.999:
		draw_arc(finish, minf(size.x, size.y) * 0.19, 0.0, TAU, 36,
			Color(1.0, 0.87, 0.34, 0.72), 7.0)
		for sparkle_index in range(5):
			var sparkle_angle := float(sparkle_index) / 5.0 * TAU
			draw_circle(finish + Vector2.from_angle(sparkle_angle) * 48.0,
				4.0 + float(sparkle_index % 2) * 2.0,
				Color(1.0, 0.92, 0.55, 0.84))


func _uses_authored_trace_context() -> bool:
	return mode == "swipe" and visual_context in [
		"trace_chef", "trace_ballerina", "trace_doctor", "trace_magician",
	]


func _trace_demo_point(progress: float) -> Vector2:
	var amount := clampf(progress, 0.0, 1.0)
	match visual_context:
		"trace_chef":
			var angle := -PI * 0.75 + amount * TAU
			return Vector2(size.x * 0.50, size.y * 0.54) \
				+ Vector2(cos(angle) * size.x * 0.30, sin(angle) * size.y * 0.27)
		"trace_ballerina":
			return Vector2(size.x * lerpf(0.12, 0.88, amount),
				size.y * (0.50 + sin(amount * TAU) * 0.18))
		"trace_doctor":
			return Vector2(size.x * lerpf(0.18, 0.82, amount),
				size.y * (0.28 + amount * 0.45 + sin(amount * TAU) * 0.07))
		"trace_magician":
			return Vector2(size.x * lerpf(0.16, 0.84, amount),
				size.y * (0.27 + (1.0 - pow(2.0 * amount - 1.0, 2.0)) * 0.42))
	return size * 0.5


func _trace_goal_units() -> float:
	match visual_context:
		"trace_chef":
			return 6.0
		"trace_ballerina":
			return 5.5
		"trace_doctor", "trace_magician":
			return 5.0
	return 1.0


func _trace_progress_for_point(point: Vector2) -> float:
	if visual_context == "trace_chef":
		var normalized := (point - Vector2(size.x * 0.50, size.y * 0.54)) \
			/ Vector2(size.x * 0.30, size.y * 0.27)
		if normalized.length_squared() <= 0.001:
			return trace_journey
		var start_angle := -PI * 0.75
		var amount := fposmod(normalized.angle() - start_angle, TAU) / TAU
		# The frosting ring closes on its start point. Once most of the ring is
		# complete, the wrapped angle is the finish, not a reset back to zero.
		if trace_journey > 0.72 and amount < 0.24:
			amount += 1.0
		return clampf(amount, 0.0, 1.0)
	match visual_context:
		"trace_ballerina":
			return clampf(inverse_lerp(size.x * 0.12, size.x * 0.88, point.x), 0.0, 1.0)
		"trace_doctor":
			return clampf(inverse_lerp(size.x * 0.18, size.x * 0.82, point.x), 0.0, 1.0)
		"trace_magician":
			return clampf(inverse_lerp(size.x * 0.16, size.x * 0.84, point.x), 0.0, 1.0)
	return trace_journey


func _trace_start_hit_rect() -> Rect2:
	var reach := maxf(38.0, minf(size.x, size.y) * 0.16)
	return Rect2(_trace_demo_point(trace_journey) - Vector2.ONE * reach,
		Vector2.ONE * reach * 2.0).intersection(Rect2(Vector2.ZERO, size))


func _trace_rehint(at: Vector2) -> void:
	feedback_positive = false
	feedback_t = 0.24
	feedback_anchor = at
	demo_active = true
	demo_t = 0.0
	gesture.emit("swipe", 0.0, 0.35)


func _authored_trace_drag(at: Vector2) -> void:
	if not trace_engaged or trace_journey >= 0.999:
		return
	var candidate := _trace_progress_for_point(at)
	var journey_delta := candidate - trace_journey
	var follows_corridor := _trace_segment_on_corridor(previous_pos, at)
	# Ordered travel blocks reverse scrubbing and large chord shortcuts. The
	# 18% cap still permits coarse preschool touch samples on the small phone.
	if not follows_corridor or journey_delta <= 0.001 or journey_delta > 0.18:
		_trace_rehint(at)
		previous_pos = _trace_demo_point(trace_journey)
		return
	demo_active = false
	if trace_points.is_empty():
		trace_points.append(previous_pos)
	if at.distance_to(trace_points[trace_points.size() - 1]) > 10.0:
		trace_points.append(at)
	trace_journey = minf(1.0, candidate)
	widget_fill = trace_journey
	gesture.emit("swipe", journey_delta * _trace_goal_units(), 1.0)
	previous_pos = at


func _trace_corridor_contains(point: Vector2) -> bool:
	match visual_context:
		"trace_chef":
			var normalized := (point - Vector2(size.x * 0.50, size.y * 0.54)) \
				/ Vector2(size.x * 0.30, size.y * 0.27)
			return absf(normalized.length() - 1.0) <= 0.38
		"trace_ballerina":
			var amount := inverse_lerp(size.x * 0.12, size.x * 0.88, point.x)
			if amount < 0.0 or amount > 1.0:
				return false
			var expected_y := size.y * (0.50 + sin(amount * TAU) * 0.18)
			return absf(point.y - expected_y) <= size.y * 0.14
		"trace_doctor":
			var amount := inverse_lerp(size.x * 0.18, size.x * 0.82, point.x)
			if amount < 0.0 or amount > 1.0:
				return false
			var expected_y := size.y * (0.28 + amount * 0.45 + sin(amount * TAU) * 0.07)
			return absf(point.y - expected_y) <= size.y * 0.14
		"trace_magician":
			var amount := inverse_lerp(size.x * 0.16, size.x * 0.84, point.x)
			if amount < 0.0 or amount > 1.0:
				return false
			var expected_y := size.y * (0.27 + (1.0 - pow(2.0 * amount - 1.0, 2.0)) * 0.42)
			return absf(point.y - expected_y) <= size.y * 0.14
	return true


func _trace_segment_on_corridor(from: Vector2, to: Vector2) -> bool:
	var inside := 0
	for sample_index in range(5):
		var amount := float(sample_index) / 4.0
		if _trace_corridor_contains(from.lerp(to, amount)):
			inside += 1
	# A generous majority rule accepts imperfect tracing but refuses the old
	# exploit where one endpoint touched the object and the rest scrubbed away.
	return inside >= 3


func _draw_authored_trace_corridor() -> void:
	var previous := _trace_demo_point(0.0)
	for point_index in range(1, 33):
		var point := _trace_demo_point(float(point_index) / 32.0)
		draw_line(previous, point, Color(accent, 0.38), 12.0, true)
		draw_line(previous, point, Color(1.0, 1.0, 1.0, 0.38), 4.0, true)
		previous = point


func _is_magician_portal_context() -> bool:
	return mode == "circle" and visual_context == "crank_magician"


func _clean_widget_playfield_rect() -> Rect2:
	# Measured inner-card boundary: preserve the authored frame/title gutter while
	# still covering every old subject bbox (including top ribbons and platforms).
	return Rect2(size.x * 0.055, size.y * 0.07, size.x * 0.89, size.y * 0.875)


func _draw_clean_widget_playfield(top: Color, bottom: Color) -> void:
	var field := _clean_widget_playfield_rect()
	draw_rect(field, top, true)
	draw_rect(Rect2(field.position.x, field.position.y + field.size.y * 0.53,
		field.size.x, field.size.y * 0.47), bottom, true)
	draw_rect(field, Color("#463963"), false, 4.0)


func _portal_center() -> Vector2:
	return Vector2(size.x * 0.50, size.y * 0.51)


func _portal_radius() -> float:
	return minf(size.x, size.y) * 0.29


func _portal_rotating_texture() -> Texture2D:
	# Only an explicitly isolated ring may rotate. portal_mover_texture is the
	# architectural doorway and widget_mover is the Lamba-and-hat tableau.
	return portal_ring_texture


func _portal_doorway_rotation() -> float:
	return 0.0


func _draw_magician_portal() -> void:
	last_contextual_draw_route = "portal:%s" % visual_context
	last_portal_layer_order = ""
	# The legacy base is a complete Lamba/hat/platform tableau. Mask its entire
	# subject bbox first so only the portal ring—not detached tableau fragments—
	# survives inside the framed card.
	_draw_clean_widget_playfield(Color("#322654"), Color("#4e3a72"))
	var center := _portal_center()
	var radius := _portal_radius()
	var progress := clampf(widget_fill, 0.0, 1.0)
	if portal_overlay_texture != null:
		draw_texture_rect(portal_overlay_texture, Rect2(Vector2.ZERO, size), false,
			Color(1.0, 1.0, 1.0, 0.18 + progress * 0.82))
	# The delivered doorway may ease/fade into view, but its columns, curtains,
	# and threshold never rotate with the child's circular gesture.
	var doorway_scale := 0.88 + progress * 0.12
	draw_set_transform(center, _portal_doorway_rotation(), Vector2.ONE * doorway_scale)
	var doorway_side := radius * 2.28
	if portal_mover_texture != null:
		draw_texture_rect(portal_mover_texture,
			Rect2(Vector2.ONE * -doorway_side * 0.5, Vector2.ONE * doorway_side), false,
			Color(1.0, 1.0, 1.0, 0.52 + progress * 0.48))
	else:
		var frame_color := Color("#e7bd78")
		for side_sign: float in [-1.0, 1.0]:
			var post_x := side_sign * radius * 0.68
			draw_line(Vector2(post_x, -radius * 0.18),
				Vector2(post_x, radius * 0.74), frame_color, 12.0, true)
		draw_arc(Vector2(0.0, radius * 0.06), radius * 0.69,
			PI, TAU, 32, frame_color, 12.0)
		draw_line(Vector2(-radius * 0.80, radius * 0.76),
			Vector2(radius * 0.80, radius * 0.76), frame_color, 12.0, true)
	draw_set_transform(Vector2.ZERO)
	last_portal_layer_order = "doorway"
	var rotating := _portal_rotating_texture()
	var portal_scale := Vector2.ONE * (0.78 + progress * 0.22)
	draw_set_transform(center, crank_rotation, portal_scale)
	if rotating != null:
		var ring_side := radius * 1.22
		draw_texture_rect(rotating,
			Rect2(Vector2.ONE * -ring_side * 0.5, Vector2.ONE * ring_side), false)
	else:
		# Portal-only field: broken rings and star motes stay within the doorway's
		# aperture while the architectural columns remain physically stationary.
		for ring_index in range(3):
			var ring_radius := radius * (0.24 + float(ring_index) * 0.15)
			var gap := 0.42 - progress * 0.34
			var start_angle := float(ring_index) * 0.72
			draw_arc(Vector2.ZERO, ring_radius, start_angle + gap,
				start_angle + TAU - gap, 48,
				Color(1.0, 0.78 + float(ring_index) * 0.06, 0.25,
					0.55 + progress * 0.35), 8.0 - float(ring_index))
		for mote_index in range(6):
			var angle := float(mote_index) / 6.0 * TAU + progress * 1.4
			draw_circle(Vector2.from_angle(angle) * radius * 0.40,
				3.5 + float(mote_index % 2) * 2.0,
				Color(0.80, 0.96, 1.0, 0.52 + progress * 0.38))
	draw_set_transform(Vector2.ZERO)
	last_portal_layer_order += ">aperture"
	if completion_accepted or progress >= 0.999:
		draw_circle(center, radius * 0.38, Color(0.52, 0.32, 0.84, 0.42))
		draw_arc(center, radius * 0.82, 0.0, TAU, 48,
			Color(1.0, 0.88, 0.34, 0.82), 8.0)
		last_portal_layer_order += ">glow"


func _is_racer_tune_context() -> bool:
	return mode == "circle" and visual_context == "crank_racer"


func _racer_front_hub() -> Vector2:
	return Vector2(size.x * 0.215, size.y * 0.735)


func _racer_rear_hub() -> Vector2:
	return Vector2(size.x * 0.580, size.y * 0.725)


func _racer_wheel_rect(rear: bool, progress: float = 1.0) -> Rect2:
	var hub := _racer_rear_hub() if rear else _racer_front_hub()
	var amount := clampf(progress, 0.0, 1.0) if rear else 1.0
	var eased := amount * amount * (3.0 - 2.0 * amount)
	var side := minf(size.x, size.y) * 0.25 * (0.28 + eased * 0.72)
	return Rect2(hub - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _racer_wrench_rect() -> Rect2:
	var side := minf(size.x, size.y) * 0.32
	return Rect2(_racer_rear_hub() - Vector2.ONE * side * 0.5,
		Vector2.ONE * side)


func _racer_runtime_wheel_rects(progress: float) -> Array[Rect2]:
	# The revised base already paints the front wheel. Runtime installs only the
	# missing rear wheel so the finished kart has two wheels, not a doubled front.
	return [_racer_wheel_rect(true, progress)]


func _draw_racer_wheel(rect: Rect2) -> void:
	if racer_wheel_texture != null:
		draw_texture_rect(racer_wheel_texture, rect, false)
		return
	var center := rect.get_center()
	var radius := rect.size.x * 0.48
	draw_circle(center, radius, Color("#4a354f"))
	draw_circle(center, radius * 0.70, Color("#9ed2d0"))
	draw_circle(center, radius * 0.27, Color("#f1d18a"))
	draw_arc(center, radius, 0.0, TAU, 28, Color("#271f38"), 4.0)


func _draw_racer_tune() -> void:
	last_contextual_draw_route = "racer_tune:%s" % visual_context
	var progress := clampf(widget_fill, 0.0, 1.0)
	# The revised base contains its front wheel; only the rear grows and settles
	# into the remaining empty arch as the wrench turns.
	for wheel_rect: Rect2 in _racer_runtime_wheel_rects(progress):
		_draw_racer_wheel(wheel_rect)
	var rear_hub := _racer_rear_hub()
	var settle := sin(clampf(progress * 1.25, 0.0, 1.0) * PI) * 0.08
	draw_set_transform(rear_hub, crank_rotation,
		Vector2(1.0 + settle, 1.0 - settle))
	if widget_mover != null:
		var wrench_side := _racer_wrench_rect().size.x
		draw_texture_rect(widget_mover,
			Rect2(Vector2.ONE * -wrench_side * 0.5, Vector2.ONE * wrench_side), false)
	else:
		draw_line(Vector2(-30.0, 24.0), Vector2(28.0, -25.0),
			Color("#e8a76c"), 10.0, true)
	draw_set_transform(Vector2.ZERO)
	draw_arc(rear_hub, _racer_wheel_rect(true, progress).size.x * 0.62,
		-crank_rotation, -crank_rotation + TAU * progress, 36,
		Color(1.0, 0.82, 0.30, 0.60), 5.0)
	if completion_accepted or progress >= 0.999:
		for hub: Vector2 in [_racer_front_hub(), _racer_rear_hub()]:
			draw_arc(hub, minf(size.x, size.y) * 0.145, 0.0, TAU, 32,
				Color(1.0, 0.88, 0.38, 0.68), 5.0)


func _uses_contextual_crank() -> bool:
	return mode == "circle" and visual_context in [
		"crank_chef", "crank_ballerina", "crank_candymaker",
		"crank_doctor", "crank_astronaut", "crank_popstar",
	]


func _contextual_crank_uses_mover() -> bool:
	# Only these three delivered movers are genuinely isolated objects. The
	# ballerina/candy files repeat most of their whole backdrop, while Doctor's
	# roll does not communicate the bandage wrapping around the patient.
	return visual_context in ["crank_chef", "crank_astronaut", "crank_popstar"]


func _crank_action_rect() -> Rect2:
	match visual_context:
		"crank_chef":
			return Rect2(size.x * 0.29, size.y * 0.28, size.x * 0.42, size.y * 0.54)
		"crank_ballerina":
			return Rect2(size.x * 0.18, size.y * 0.15, size.x * 0.64, size.y * 0.72)
		"crank_candymaker":
			return Rect2(size.x * 0.20, size.y * 0.24, size.x * 0.60, size.y * 0.56)
		"crank_doctor":
			return Rect2(size.x * 0.20, size.y * 0.17, size.x * 0.60, size.y * 0.70)
		"crank_astronaut":
			return Rect2(size.x * 0.34, size.y * 0.08, size.x * 0.32, size.y * 0.45)
		"crank_popstar":
			return Rect2(size.x * 0.26, size.y * 0.14, size.x * 0.48, size.y * 0.72)
	return Rect2(size * 0.25, size * 0.5)


func _crank_legacy_subject_rect() -> Rect2:
	# Normalized bboxes measured from the original cards. These are audit data:
	# each contextual draw masks this whole area before placing its sole actor.
	match visual_context:
		"crank_chef":
			return Rect2(size.x * 0.30, size.y * 0.14, size.x * 0.40, size.y * 0.63)
		"crank_ballerina":
			return Rect2(size.x * 0.11, size.y * 0.14, size.x * 0.78, size.y * 0.72)
		"crank_candymaker":
			return Rect2(size.x * 0.20, size.y * 0.14, size.x * 0.60, size.y * 0.67)
		"crank_doctor":
			return Rect2(size.x * 0.18, size.y * 0.08, size.x * 0.64, size.y * 0.83)
		"crank_astronaut":
			return Rect2(size.x * 0.36, size.y * 0.10, size.x * 0.28, size.y * 0.34)
	return Rect2()


func _draw_chef_crank(progress: float) -> void:
	_draw_clean_widget_playfield(Color("#fff4df"), Color("#e7cfa7"))
	var rect := _crank_action_rect()
	var center := rect.get_center() + Vector2(0.0, rect.size.y * 0.05)
	var bowl_radius := minf(rect.size.x, rect.size.y) * 0.43
	# Fresh batter covers the whisk already painted into the old base. The
	# isolated whisk is now the only moving tool and stays inside the bowl.
	draw_set_transform(center, 0.0, Vector2(1.35, 0.62))
	draw_circle(Vector2.ZERO, bowl_radius, Color("#f2cf91"))
	draw_arc(Vector2.ZERO, bowl_radius, 0.0, TAU, 40, Color("#835071"), 5.0)
	draw_set_transform(Vector2.ZERO)
	var whisk_side := minf(rect.size.x, rect.size.y) * 0.66
	draw_set_transform(center, crank_rotation, Vector2.ONE)
	if widget_mover != null:
		draw_texture_rect(widget_mover,
			Rect2(Vector2.ONE * -whisk_side * 0.5, Vector2.ONE * whisk_side), false)
	else:
		draw_line(Vector2(0.0, -whisk_side * 0.45), Vector2(0.0, whisk_side * 0.10),
			Color("#94683f"), 8.0, true)
		for wire_offset: float in [-0.16, 0.0, 0.16]:
			draw_arc(Vector2(wire_offset * whisk_side, whisk_side * 0.18),
				whisk_side * 0.19, -1.85, 1.85, 16, Color("#f8f0df"), 3.0)
	draw_set_transform(Vector2.ZERO)
	for swirl_index in range(3):
		draw_arc(center, bowl_radius * (0.28 + float(swirl_index) * 0.20),
			crank_rotation + float(swirl_index) * 0.7,
			crank_rotation + PI * (0.72 + progress * 0.55), 24,
			Color(1.0, 0.95, 0.72, 0.36 + progress * 0.30), 3.0)


func _draw_ballerina_crank(progress: float) -> void:
	_draw_clean_widget_playfield(Color("#f5e8ff"), Color("#d9bee9"))
	var rect := _crank_action_rect()
	var center := rect.get_center()
	# A clean spotlight masks the repeated platform tableau in the old mover.
	# Only the ribbon flourish responds to circling.
	draw_set_transform(center, 0.0, Vector2(1.45, 0.76))
	draw_circle(Vector2.ZERO, minf(rect.size.x, rect.size.y) * 0.42,
		Color(0.95, 0.88, 1.0, 0.88))
	draw_set_transform(Vector2.ZERO)
	draw_line(Vector2(rect.position.x, rect.end.y - 14.0),
		Vector2(rect.end.x, rect.end.y - 14.0), Color("#9a72bd"), 7.0, true)
	var ribbon := PackedVector2Array()
	for point_index in range(28):
		var amount := float(point_index) / 27.0
		var angle := crank_rotation + amount * TAU * (0.82 + progress * 0.58)
		var radius := minf(rect.size.x * 0.43, rect.size.y * 0.43) \
			* (0.28 + amount * 0.72)
		ribbon.append(center + Vector2(cos(angle) * radius,
			sin(angle) * radius * 0.70))
	if ribbon.size() >= 2:
		draw_polyline(ribbon, Color("#e37aa7"), 9.0, true)
		draw_polyline(ribbon, Color(1.0, 0.89, 0.95, 0.76), 3.0, true)
	var tip := ribbon[ribbon.size() - 1]
	draw_circle(tip, 9.0 + progress * 5.0, Color("#ffe17a"))


func _draw_candymaker_crank(progress: float) -> void:
	_draw_clean_widget_playfield(Color("#fff2df"), Color("#f2c6d0"))
	var rect := _crank_action_rect()
	var center := rect.get_center()
	# The candy stays still while its wrapper ends twist in opposite directions.
	# The rejected mover duplicated both the candy and most of the backdrop.
	draw_rect(rect, Color("#fff0df"), true)
	draw_rect(rect, Color("#9c567b"), false, 4.0)
	var candy_half := rect.size.x * 0.18
	draw_set_transform(center, -0.10, Vector2(1.35, 0.72))
	draw_circle(Vector2.ZERO, candy_half, Color("#ed8c9c"))
	draw_arc(Vector2.ZERO, candy_half, 0.0, TAU, 36, Color("#7e426d"), 5.0)
	draw_set_transform(Vector2.ZERO)
	for side_sign: float in [-1.0, 1.0]:
		var knot := center + Vector2(side_sign * rect.size.x * 0.28, 0.0)
		draw_set_transform(knot, side_sign * crank_rotation, Vector2.ONE)
		var outward := side_sign * rect.size.x * 0.16
		draw_colored_polygon(PackedVector2Array([
			Vector2(side_sign * rect.size.x * 0.05, 0.0),
			Vector2(outward, -rect.size.y * 0.20),
			Vector2(outward * 1.18, 0.0),
			Vector2(outward, rect.size.y * 0.20),
		]), Color("#f5c25f"))
		draw_set_transform(Vector2.ZERO)
	for swirl_index in range(2):
		draw_arc(center, candy_half * (0.35 + float(swirl_index) * 0.32),
			crank_rotation, crank_rotation + PI * (1.0 + progress), 28,
			Color(1.0, 0.93, 0.72, 0.76), 4.0)


func _draw_doctor_crank(progress: float) -> void:
	_draw_clean_widget_playfield(Color("#ebfaf6"), Color("#bcded9"))
	var rect := _crank_action_rect()
	var center := rect.get_center()
	# Redraw the patient on a clean exam pad so the base's already-complete
	# bandage cannot leak through. The wrap itself grows across the plush.
	draw_rect(rect, Color("#e9f8f4"), true)
	draw_rect(rect, Color("#557497"), false, 4.0)
	var plush := center + Vector2(0.0, rect.size.y * 0.05)
	draw_circle(plush - Vector2(0.0, rect.size.y * 0.18), rect.size.y * 0.19,
		Color("#d59a70"))
	draw_circle(plush + Vector2(-rect.size.x * 0.12, -rect.size.y * 0.29),
		rect.size.y * 0.075, Color("#c38561"))
	draw_circle(plush + Vector2(rect.size.x * 0.12, -rect.size.y * 0.29),
		rect.size.y * 0.075, Color("#c38561"))
	draw_circle(plush, rect.size.y * 0.23, Color("#d59a70"))
	var wrap_left := plush.x - rect.size.x * 0.25
	var wrap_width := rect.size.x * 0.50 * progress
	for strip_index in range(4):
		var strip_y := plush.y - rect.size.y * 0.16 + float(strip_index) * rect.size.y * 0.095
		draw_line(Vector2(wrap_left, strip_y), Vector2(wrap_left + wrap_width, strip_y),
			Color("#fff4dc"), 12.0, true)
		if progress > 0.06:
			draw_line(Vector2(wrap_left, strip_y - 3.0),
				Vector2(wrap_left + wrap_width, strip_y - 3.0),
				Color(0.75, 0.60, 0.52, 0.32), 2.0, true)
	if progress >= 0.95:
		draw_line(plush - Vector2(10.0, 0.0), plush + Vector2(10.0, 0.0),
			Color("#e16e78"), 5.0, true)
		draw_line(plush - Vector2(0.0, 10.0), plush + Vector2(0.0, 10.0),
			Color("#e16e78"), 5.0, true)


func _draw_astronaut_crank(progress: float) -> void:
	_draw_clean_widget_playfield(Color("#293f68"), Color("#47678a"))
	var rect := _crank_action_rect()
	var center := rect.get_center()
	var side := minf(rect.size.x, rect.size.y) * 0.62
	# Occlude the painted valve first, then rotate only the isolated wheel at
	# the same hub—never a second wheel at card center.
	draw_circle(center, side * 0.56, Color("#263a60"))
	draw_set_transform(center, crank_rotation, Vector2.ONE)
	if widget_mover != null:
		draw_texture_rect(widget_mover,
			Rect2(Vector2.ONE * -side * 0.5, Vector2.ONE * side), false)
	else:
		draw_circle(Vector2.ZERO, side * 0.43, Color("#7cc5cf"))
		draw_circle(Vector2.ZERO, side * 0.13, Color("#f4d37a"))
		for spoke_index in range(6):
			var angle := float(spoke_index) / 6.0 * TAU
			draw_line(Vector2.from_angle(angle) * side * 0.12,
				Vector2.from_angle(angle) * side * 0.42, Color("#e8f5ee"), 5.0, true)
	draw_set_transform(Vector2.ZERO)
	draw_arc(center, side * 0.57, -PI * 0.5,
		-PI * 0.5 + TAU * progress, 36, Color("#ffe17a"), 6.0)


func _draw_popstar_crank(progress: float) -> void:
	var rect := _crank_action_rect()
	var center := rect.get_center() + Vector2(0.0, rect.size.y * 0.04)
	var side := minf(rect.size.x, rect.size.y) * 0.52
	# The microphone pulses and leans by a few degrees; crank_rotation is never
	# applied as a full spin. Notes and sound arcs make the sound-check causal.
	var pulse := 1.0 + sin(crank_rotation * 2.0) * 0.08
	var lean := sin(crank_rotation) * 0.18
	draw_set_transform(center, lean, Vector2.ONE * pulse)
	if widget_mover != null:
		draw_texture_rect(widget_mover,
			Rect2(Vector2.ONE * -side * 0.5, Vector2.ONE * side), false)
	else:
		draw_line(Vector2(0.0, side * 0.38), Vector2(0.0, -side * 0.18),
			Color("#d69568"), 11.0, true)
		draw_circle(Vector2(0.0, -side * 0.30), side * 0.16, Color("#f6ead0"))
	draw_set_transform(Vector2.ZERO)
	for wave_index in range(3):
		var radius := side * (0.32 + float(wave_index) * 0.22) * maxf(progress, 0.12)
		draw_arc(center, radius, -0.92, 0.92, 22,
			Color(0.42, 0.89, 0.95, 0.72 - float(wave_index) * 0.16), 4.0)
	for note_index in range(int(ceilf(progress * 4.0))):
		var note := center + Vector2(side * (0.38 + float(note_index) * 0.17),
			-side * (0.28 + float(note_index % 2) * 0.16))
		draw_circle(note, 5.0, Color("#ffe17a"))
		draw_line(note + Vector2(4.0, 0.0), note + Vector2(4.0, -14.0),
			Color("#ffe17a"), 3.0)


func _draw_contextual_crank() -> void:
	var progress := clampf(widget_fill, 0.0, 1.0)
	last_contextual_draw_route = "crank:%s" % visual_context
	match visual_context:
		"crank_chef":
			_draw_chef_crank(progress)
		"crank_ballerina":
			_draw_ballerina_crank(progress)
		"crank_candymaker":
			_draw_candymaker_crank(progress)
		"crank_doctor":
			_draw_doctor_crank(progress)
		"crank_astronaut":
			_draw_astronaut_crank(progress)
		"crank_popstar":
			_draw_popstar_crank(progress)


func _uses_contextual_charge() -> bool:
	return mode == "hold" and visual_context in [
		"charge_ballerina", "charge_astronaut", "charge_popstar",
	]


func _charge_action_rect() -> Rect2:
	match visual_context:
		"charge_ballerina":
			return Rect2(size.x * 0.28, size.y * 0.24, size.x * 0.44, size.y * 0.58)
		"charge_astronaut":
			return Rect2(size.x * 0.27, size.y * 0.05, size.x * 0.46, size.y * 0.90)
		"charge_popstar":
			return Rect2(size.x * 0.18, size.y * 0.05, size.x * 0.64, size.y * 0.90)
	return Rect2(size * 0.25, size * 0.5)


func _charge_legacy_subject_rect() -> Rect2:
	# Measured bboxes of the static subject painted into the old charge cards.
	# The clean playfield must enclose these before the isolated prop is drawn.
	match visual_context:
		"charge_ballerina":
			# Floating black stage remnant in the old card, measured at shipping.
			return Rect2(size.x * 0.13, size.y * 0.82,
				size.x * 0.74, size.y * 0.08)
		"charge_astronaut":
			return Rect2(size.x * 0.32, size.y * 0.08,
				size.x * 0.36, size.y * 0.84)
		"charge_popstar":
			return Rect2(size.x * 0.40, size.y * 0.13,
				size.x * 0.20, size.y * 0.78)
	return Rect2()


func _charge_rocket_center(progress: float) -> Vector2:
	var lift := clampf((progress - 0.64) / 0.36, 0.0, 1.0)
	lift = lift * lift * (3.0 - 2.0 * lift)
	return Vector2(size.x * 0.50, lerpf(size.y * 0.63, size.y * 0.34, lift))


func _draw_ballerina_blossom(progress: float) -> void:
	# Replace the full inner stage first; this removes the old floating horizontal
	# remnant near the floor while preserving the authored outer card frame.
	_draw_clean_widget_playfield(Color("#f7ebff"), Color("#d7bfe9"))
	var stage_y := size.y * 0.79
	draw_line(Vector2(size.x * 0.15, stage_y), Vector2(size.x * 0.85, stage_y),
		Color("#9e74ba"), 7.0, true)
	var center := Vector2(size.x * 0.50, size.y * 0.55)
	for petal_index in range(8):
		var angle := float(petal_index) / 8.0 * TAU - PI * 0.5
		var distance := lerpf(7.0, minf(size.x, size.y) * 0.20, progress)
		var petal_center := center + Vector2.from_angle(angle) * distance
		draw_set_transform(petal_center, angle,
			Vector2(1.0 + progress * 0.65, 0.62 + progress * 0.28))
		draw_circle(Vector2.ZERO, minf(size.x, size.y) * 0.065,
			Color(0.92, 0.65, 0.82, 0.62 + progress * 0.30))
		draw_set_transform(Vector2.ZERO)
	draw_circle(center, minf(size.x, size.y) * (0.07 + progress * 0.035),
		Color("#ffe58a"))
	if completion_accepted or progress >= 0.999:
		draw_arc(center, minf(size.x, size.y) * 0.28, 0.0, TAU, 40,
			Color(1.0, 0.91, 0.55, 0.70), 6.0)


func _draw_astronaut_launch(progress: float) -> void:
	var action := _charge_action_rect()
	# Replace the old card's static rocket inside a clean launch bay before the
	# isolated approved rocket moves. This prevents a second rocket remaining
	# underneath the lifting one.
	draw_rect(action, Color("#263963"), true)
	draw_rect(action, Color("#739dc0"), false, 4.0)
	for star_index in range(5):
		var star := action.position + Vector2(
			action.size.x * (0.12 + float(star_index) * 0.19),
			action.size.y * (0.14 + float(star_index % 2) * 0.16))
		draw_circle(star, 2.5 + float(star_index % 2), Color("#fff1a6"))
	var center := _charge_rocket_center(progress)
	var shake := sin(progress * 48.0) * 3.0 \
		* (1.0 - clampf((progress - 0.75) * 4.0, 0.0, 1.0))
	center.x += shake
	var body_height := minf(size.x, size.y) * 0.27
	var body_width := body_height * 0.40
	var exhaust := minf(size.x, size.y) * (0.08 + progress * 0.24)
	draw_colored_polygon(PackedVector2Array([
		center + Vector2(-body_width * 0.28, body_height * 0.48),
		center + Vector2(0.0, body_height * 0.48 + exhaust),
		center + Vector2(body_width * 0.28, body_height * 0.48),
	]), Color(1.0, 0.71, 0.25, 0.45 + progress * 0.55))
	for bubble_index in range(4):
		var bubble := center + Vector2(
			(float(bubble_index % 2) - 0.5) * body_width * 0.75,
			body_height * 0.62 + exhaust * (0.25 + float(bubble_index) * 0.20))
		draw_circle(bubble, 4.0 + float(bubble_index),
			Color(0.54, 0.92, 1.0, 0.45 + progress * 0.45))
	if charge_astronaut_texture != null:
		var rocket_side := minf(size.x, size.y) * 0.36
		draw_texture_rect(charge_astronaut_texture,
			Rect2(center - Vector2.ONE * rocket_side * 0.5, Vector2.ONE * rocket_side), false)
	else:
		draw_colored_polygon(PackedVector2Array([
			center + Vector2(0.0, -body_height * 0.62),
			center + Vector2(body_width * 0.55, -body_height * 0.12),
			center + Vector2(body_width * 0.48, body_height * 0.50),
			center + Vector2(-body_width * 0.48, body_height * 0.50),
			center + Vector2(-body_width * 0.55, -body_height * 0.12),
		]), Color("#e8eef7"))
		draw_circle(center - Vector2(0.0, body_height * 0.15), body_width * 0.24,
			Color("#6fd5de"))


func _draw_popstar_soundcheck(progress: float) -> void:
	var action := _charge_action_rect()
	# A clean stage patch removes the meter card's already-painted microphone;
	# the approved isolated prop below is the sole sounding object.
	draw_rect(action, Color("#342451"), true)
	draw_rect(action, Color("#8e65a5"), false, 4.0)
	draw_line(Vector2(action.position.x, action.end.y - 13.0),
		Vector2(action.end.x, action.end.y - 13.0), Color("#e6ad65"), 7.0, true)
	var center := Vector2(size.x * 0.50, size.y * 0.56)
	var pulse := 1.0 + sin(progress * PI * 6.0) * 0.06
	draw_set_transform(center, -0.32, Vector2.ONE * pulse)
	var length := minf(size.x, size.y) * 0.36
	if charge_popstar_texture != null:
		draw_texture_rect(charge_popstar_texture,
			Rect2(Vector2.ONE * -length * 0.5, Vector2.ONE * length), false)
	else:
		draw_line(Vector2(0.0, length * 0.28), Vector2(0.0, -length * 0.30),
			Color("#e4a173"), 13.0, true)
		draw_circle(Vector2(0.0, -length * 0.40), length * 0.16, Color("#f7ead0"))
	draw_set_transform(Vector2.ZERO)
	for wave_index in range(3):
		var radius := minf(size.x, size.y) \
			* (0.13 + float(wave_index) * 0.09) * progress
		if radius > 2.0:
			draw_arc(center, radius, -1.05, 1.05, 24,
				Color(0.45, 0.88, 0.95, 0.72 - float(wave_index) * 0.16), 5.0)
	for note_index in range(int(ceilf(progress * 4.0))):
		var note := center + Vector2(size.x * (0.10 + 0.055 * float(note_index)),
			-size.y * (0.13 + 0.055 * float(note_index % 2)))
		draw_circle(note, 6.0, Color("#ffe17a"))
		draw_line(note + Vector2(5.0, 0.0), note + Vector2(5.0, -18.0),
			Color("#ffe17a"), 4.0)


func _draw_contextual_charge() -> void:
	var progress := clampf(widget_fill, 0.0, 1.0)
	last_contextual_draw_route = "charge:%s" % visual_context
	match visual_context:
		"charge_ballerina":
			_draw_ballerina_blossom(progress)
		"charge_astronaut":
			_draw_astronaut_launch(progress)
		"charge_popstar":
			_draw_popstar_soundcheck(progress)


func _draw_widget_layers(center: Vector2) -> void:
	match widget_template:
		"gauge":
			if widget_mover != null:
				var pivot := Vector2(size.x * 0.5, size.y * 0.82)
				var rotation := deg_to_rad(lerpf(-60.0, 60.0, timing_position))
				draw_set_transform(pivot, rotation)
				draw_texture_rect(widget_mover, Rect2(-48.0, -84.0, 96.0, 96.0), false)
				draw_set_transform(Vector2.ZERO)
			if widget_overlay != null and (completion_accepted or (feedback_t > 0.0 and feedback_positive)):
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
		"track":
			var run_point := Vector2(lerpf(size.x * 0.12, size.x * 0.88, timing_position), size.y * 0.66)
			_draw_widget_sprite(widget_mover, run_point, 128.0)
			if widget_shared != null and feedback_t > 0.0 and feedback_positive:
				var hit_point := Vector2(lerpf(size.x * 0.12, size.x * 0.88, feedback_position), size.y * 0.66)
				_draw_widget_sprite(widget_shared, hit_point, 82.0)
		"pour":
			if held:
				_draw_widget_sprite(widget_mover, center - Vector2(0.0, 18.0), 138.0)
			if widget_overlay != null:
				_draw_progress_overlay(widget_overlay, widget_fill, false)
		"basin":
			if widget_overlay != null and (held or completion_accepted):
				_draw_progress_overlay(widget_overlay, widget_fill, false)
			if completion_accepted:
				_draw_widget_sprite(widget_shared, center, 118.0)
		"charge":
			if _uses_contextual_charge():
				_draw_contextual_charge()
			else:
				if widget_mover != null and (held or completion_accepted):
					_draw_widget_sprite(widget_mover, center, 108.0 + widget_fill * 126.0)
				if widget_overlay != null:
					if completion_accepted:
						draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
					else:
						# Legacy charge art remains only for contexts without an
						# authored causal object scene.
						_draw_progress_overlay(widget_overlay, widget_fill, false)
		"crank":
			if _is_magician_portal_context():
				_draw_magician_portal()
			elif _is_racer_tune_context():
				_draw_racer_tune()
			elif _uses_contextual_crank():
				_draw_contextual_crank()
			else:
				if widget_mover != null:
					draw_set_transform(center, crank_rotation)
					draw_texture_rect(widget_mover, Rect2(-70.0, -70.0, 140.0, 140.0), false)
					draw_set_transform(Vector2.ZERO)
				if widget_overlay != null:
					draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false, Color(1.0, 1.0, 1.0, widget_fill))
		"trace":
			if _uses_authored_trace_context() and not completion_accepted:
				_draw_authored_trace_corridor()
			if widget_overlay != null:
				if completion_accepted or widget_fill >= 0.999:
					draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
				else:
					_draw_trace_patches(widget_overlay)
		"push":
			if _uses_long_push_context():
				_draw_long_push()
			else:
				var mover_point := center + swipe_dir * widget_fill * 42.0
				_draw_widget_sprite(widget_mover, mover_point, 136.0)
				_draw_widget_sprite(widget_shared, center + swipe_dir * 92.0, 92.0, Color(1.0, 1.0, 1.0, 0.72))
		"target":
			if _uses_anchored_targets():
				_draw_anchored_targets()
			else:
				for mark: Vector2 in tap_marks:
					_draw_widget_sprite(widget_stamp, mark, 76.0)
				if held:
					# Painter's next free stamp rides the finger until placement.
					_draw_widget_sprite(widget_mover, pointer_pos, 142.0)
			if widget_overlay != null and completion_accepted and not _uses_anchored_targets():
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
		"lanes":
			var show_answer := choice_flash > 0.0 or demo_active
			if show_answer and widget_mover != null:
				var lane_point := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), size.y * 0.70)
				var source := Rect2(float(target_choice) * 256.0, 0.0, 256.0, 256.0)
				draw_texture_rect_region(widget_mover, Rect2(lane_point - Vector2(62.0, 62.0), Vector2(124.0, 124.0)), source)
			if shuffle_t > 0.0 and shuffle_from >= 0:
				_draw_shuffle_glide(target_choice)
			if widget_shared != null and feedback_t > 0.0:
				_draw_widget_sprite(widget_shared, feedback_anchor, 82.0,
					Color.WHITE if feedback_positive else Color(1.0, 0.82, 0.92, 0.82))


func _uses_anchored_targets() -> bool:
	return mode == "tap" and TARGET_ANCHORS.has(visual_context)


func _target_anchor_count() -> int:
	if not TARGET_ANCHORS.has(visual_context):
		return 0
	var anchors: Array = TARGET_ANCHORS[visual_context]
	return anchors.size()


func _target_anchor_point(index: int) -> Vector2:
	if not TARGET_ANCHORS.has(visual_context):
		return size * 0.5
	var anchors: Array = TARGET_ANCHORS[visual_context]
	if anchors.is_empty():
		return size * 0.5
	var normalized: Vector2 = anchors[clampi(index, 0, anchors.size() - 1)]
	return Vector2(size.x * normalized.x, size.y * normalized.y)


func _target_next_unplaced() -> int:
	for index in range(target_placed.size()):
		if not target_placed[index]:
			return index
	return -1


func _target_rehint(at: Vector2) -> void:
	feedback_positive = false
	feedback_t = 0.24
	feedback_anchor = at
	demo_active = true
	demo_t = 0.0
	gesture.emit("tap", 0.0, 0.35)


func _target_press(at: Vector2) -> void:
	if completion_accepted:
		return
	var reach := maxf(46.0, minf(size.x, size.y) * 0.15)
	var nearest := -1
	var nearest_distance := reach
	for index in range(target_placed.size()):
		if target_placed[index]:
			continue
		var distance := at.distance_to(_target_anchor_point(index))
		if distance <= nearest_distance:
			nearest_distance = distance
			nearest = index
	if nearest < 0:
		_target_rehint(at)
		return
	target_placed[nearest] = true
	target_piece_anim[nearest] = 0.42
	tap_marks.append(_target_anchor_point(nearest))
	feedback_positive = true
	feedback_t = 0.30
	feedback_anchor = _target_anchor_point(nearest)
	gesture.emit("tap", 1.0, 1.0)


func _target_tick(delta: float) -> void:
	var changed := false
	for index in range(target_piece_anim.size()):
		if target_piece_anim[index] > 0.0:
			target_piece_anim[index] = maxf(0.0, target_piece_anim[index] - delta)
			changed = true
	if changed:
		queue_redraw()


func _target_piece_texture(index: int) -> Texture2D:
	if not target_piece_textures.is_empty():
		var texture: Texture2D = target_piece_textures[index % target_piece_textures.size()]
		if texture != null:
			return texture
	return widget_stamp


func _target_piece_rect(index: int) -> Rect2:
	var side := maxf(62.0, minf(size.x, size.y) * 0.25)
	return Rect2(_target_anchor_point(index) - Vector2.ONE * side * 0.5,
		Vector2.ONE * side)


func _candymaker_recipient_rect(index: int) -> Rect2:
	var anchor := _target_anchor_point(index)
	var side := _target_piece_rect(index).size.x
	return Rect2(anchor - Vector2(side * 0.38, side * 0.56),
		Vector2(side * 0.76, side * 0.86))


func _draw_candymaker_recipients() -> void:
	var friend_colors: Array[Color] = [
		Color("#ef8ca5"), Color("#72c7c2"), Color("#b493df"),
		Color("#f0bd63"), Color("#7fb7df"), Color("#e69272"),
	]
	for index in range(_target_anchor_count()):
		var anchor := _target_anchor_point(index)
		var side := _target_piece_rect(index).size.x
		var face := anchor - Vector2(0.0, side * 0.28)
		var color: Color = friend_colors[index % friend_colors.size()]
		# Face, eyes, smile, reaching arm and open hand. Each palette differs so
		# six candies read as six distinct recipients rather than empty dots.
		draw_circle(face, side * 0.17, color)
		draw_circle(face + Vector2(-side * 0.055, -side * 0.025),
			side * 0.018, Color("#33203f"))
		draw_circle(face + Vector2(side * 0.055, -side * 0.025),
			side * 0.018, Color("#33203f"))
		draw_arc(face + Vector2(0.0, side * 0.015), side * 0.065,
			0.25, PI - 0.25, 10, Color("#6b3850"), 2.5)
		var shoulder := face + Vector2(side * (0.12 if index % 2 == 0 else -0.12),
			side * 0.12)
		draw_line(shoulder, anchor, color.darkened(0.08), side * 0.075, true)
		draw_circle(anchor, side * 0.105, color.lightened(0.12))
		for finger_index in range(3):
			var finger_angle := -2.55 + float(finger_index) * 0.42
			draw_line(anchor, anchor + Vector2.from_angle(finger_angle) * side * 0.16,
				color.lightened(0.12), side * 0.035, true)


func _draw_anchored_targets() -> void:
	var next_index := _target_next_unplaced()
	var base_side := _target_piece_rect(0).size.x
	if visual_context == "target_candymaker":
		_draw_candymaker_recipients()
	for index in range(target_placed.size()):
		var anchor := _target_anchor_point(index)
		if not target_placed[index]:
			var invitation_alpha := 0.28
			var invitation_width := 4.0
			if index == next_index:
				invitation_alpha = 0.62 + 0.18 * sin(demo_t * 4.0)
				invitation_width = 7.0
			draw_circle(anchor, base_side * 0.34, Color(accent, invitation_alpha * 0.20))
			draw_arc(anchor, base_side * 0.38, 0.0, TAU, 32,
				Color(accent, invitation_alpha), invitation_width)
			continue
		var animation := target_piece_anim[index]
		var settle := clampf(1.0 - animation / 0.42, 0.0, 1.0)
		var bounce := sin(settle * PI)
		var piece_scale := Vector2(1.0 + bounce * 0.26, 1.0 - bounce * 0.16)
		var piece: Texture2D = _target_piece_texture(index)
		draw_set_transform(anchor, 0.0, piece_scale)
		if piece != null:
			draw_texture_rect(piece,
				Rect2(Vector2.ONE * -base_side * 0.5, Vector2.ONE * base_side), false)
		else:
			# Asset-safe fallback: a placed pearl remains distinct from the hollow
			# invitation ring, so the one-use contract is readable without text.
			draw_circle(Vector2.ZERO, base_side * 0.28, accent)
			draw_circle(Vector2(-base_side * 0.08, -base_side * 0.08),
				base_side * 0.08, Color(1.0, 1.0, 1.0, 0.88))
		draw_set_transform(Vector2.ZERO)
		if animation > 0.0:
			draw_arc(anchor, base_side * (0.42 + bounce * 0.18), 0.0, TAU, 32,
				Color(1.0, 0.88, 0.32, animation / 0.42), 7.0)
	if next_index < 0:
		draw_arc(size * 0.5, minf(size.x, size.y) * 0.42, 0.0, TAU, 48,
			Color(1.0, 0.86, 0.34, 0.42), 6.0)


func _is_nursery_feed_context() -> bool:
	return visual_context in ["nursery_feed", "pour_nursery"]


func _is_nursery_bedtime_context() -> bool:
	return visual_context in ["nursery_bedtime", "push_nursery"]


func _is_nursery_burp_context() -> bool:
	return visual_context == "nursery_burp"


func _is_magic_vanish_context() -> bool:
	return visual_context == "magic_vanish"


func _draw_causal_context(center: Vector2) -> bool:
	if _is_nursery_feed_context():
		_draw_nursery_feed_scene(center)
		return true
	if _is_nursery_bedtime_context():
		_draw_nursery_bedtime_scene(center)
		return true
	if _is_nursery_burp_context():
		_draw_nursery_burp_scene(center)
		return true
	if _is_magic_vanish_context():
		_draw_magic_vanish_scene(center)
		return true
	return false


func _draw_causal_backdrop(top: Color, bottom: Color) -> void:
	draw_rect(Rect2(Vector2.ZERO, size), top, true)
	draw_rect(Rect2(0.0, size.y * 0.56, size.x, size.y * 0.44), bottom, true)
	for sparkle_index in range(6):
		var sparkle := Vector2(
			size.x * (0.10 + 0.16 * float(sparkle_index)),
			size.y * (0.12 + 0.055 * float(sparkle_index % 3)))
		draw_circle(sparkle, 3.0 + float(sparkle_index % 2),
			Color(1.0, 1.0, 1.0, 0.50))


func _nursery_baby_center(index: int) -> Vector2:
	return Vector2(size.x * (0.23 + 0.27 * float(index)), size.y * 0.62)


func _nursery_feed_bottle_pose(active: bool) -> Dictionary:
	var fill := clampf(widget_fill, 0.0, 1.0)
	var scaled := minf(fill * 3.0, 2.999)
	var baby_index := clampi(floori(scaled), 0, 2)
	var local := scaled - float(baby_index)
	var approach := clampf(local / 0.24, 0.0, 1.0) if active else 0.0
	if completion_accepted:
		baby_index = 2
		approach = 1.0
	var home := Vector2(size.x * 0.83, size.y * 0.27)
	var mouth := _nursery_baby_center(baby_index) + Vector2(size.x * 0.025, -size.y * 0.055)
	var position := home.lerp(mouth, approach)
	var rotation := lerpf(-0.10, -0.72, approach)
	return {
		"position": position,
		"rotation": rotation,
		"remaining": 1.0 - fill,
		"baby": baby_index,
	}


func _nursery_feed_bottle_rect(active: bool) -> Rect2:
	var pose := _nursery_feed_bottle_pose(active)
	var position: Vector2 = pose["position"]
	var side := minf(size.x, size.y) * 0.34
	return Rect2(position - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _nursery_bottle_art_ready() -> bool:
	# The approved bottle is intentionally 256×256. The build-time asset gate
	# owns its content hash; runtime validates the remap-safe loaded resource
	# identity/size and never reopens a source PNG that may be absent in the PCK.
	return nursery_bottle_art_valid


func _draw_nursery_feed_scene(_center: Vector2) -> void:
	_draw_causal_backdrop(Color("#e7f8f2"), Color("#c4e8df"))
	for index in range(3):
		var baby_center := _nursery_baby_center(index)
		draw_rect(Rect2(baby_center - Vector2(size.x * 0.105, size.y * 0.08),
			Vector2(size.x * 0.21, size.y * 0.19)), Color("#f4d8c8"), true)
		_draw_nursery_baby(index, baby_center, minf(size.x, size.y) * 0.29)
	var pose := _nursery_feed_bottle_pose(held or completion_accepted)
	var bottle_position: Vector2 = pose["position"]
	var bottle_rotation := float(pose["rotation"])
	var remaining := float(pose["remaining"])
	var bottle_side := minf(size.x, size.y) * 0.34
	draw_set_transform(bottle_position, bottle_rotation)
	if _nursery_bottle_art_ready():
		draw_texture_rect(nursery_bottle_texture,
			Rect2(Vector2(-bottle_side * 0.5, -bottle_side * 0.58),
				Vector2(bottle_side, bottle_side)), false)
	else:
		var bottle_rect := Rect2(-bottle_side * 0.17, -bottle_side * 0.36,
			bottle_side * 0.34, bottle_side * 0.62)
		draw_rect(bottle_rect, Color("#f7fff8"), true)
		draw_rect(Rect2(bottle_rect.position.x + 4.0,
			lerpf(bottle_rect.end.y - 4.0, bottle_rect.position.y + 4.0, remaining),
			bottle_rect.size.x - 8.0, bottle_rect.size.y * remaining - 8.0).abs(),
			Color("#ffe1a1"), true)
		draw_circle(Vector2(0.0, -bottle_side * 0.41), bottle_side * 0.075,
			Color("#efb0a8"))
		draw_rect(bottle_rect, Color("#6b5a75"), false, 3.0)
	draw_set_transform(Vector2.ZERO)
	# A separate drain pip stays readable even when the optional bottle art is
	# opaque or very small in the phone build.
	var drain := Rect2(size.x * 0.82, size.y * 0.08, size.x * 0.10, size.y * 0.30)
	draw_rect(drain, Color(1.0, 1.0, 1.0, 0.70), true)
	var drain_height := drain.size.y * remaining
	draw_rect(Rect2(drain.position.x, drain.end.y - drain_height,
		drain.size.x, drain_height), Color("#ffe1a1"), true)
	draw_rect(drain, Color("#6b5a75"), false, 3.0)


func _nursery_blanket_top(index: int) -> float:
	# The upper cloth edge rests below the face. Downward travel grows the lower
	# edge over the body; the previous implementation moved this edge down while
	# keeping the bottom fixed, which visibly *uncovered* the baby.
	return _nursery_baby_center(index).y - size.y * 0.02


func _nursery_blanket_bottom(index: int) -> float:
	var local := 0.0
	if index >= 0 and index < nursery_blanket_progress.size():
		local = nursery_blanket_progress[index]
		if index < nursery_blankets_tucked.size() and nursery_blankets_tucked[index]:
			local = 1.0
	var top := _nursery_blanket_top(index)
	var crib := _nursery_bedtime_crib_rect(index)
	return lerpf(top + size.y * 0.045, crib.end.y - size.y * 0.025,
		local * local * (3.0 - 2.0 * local))


func _nursery_bedtime_crib_rect(index: int) -> Rect2:
	var crib_center := _nursery_baby_center(index)
	return Rect2(crib_center - Vector2(size.x * 0.115, size.y * 0.13),
		Vector2(size.x * 0.23, size.y * 0.31))


func _nursery_bedtime_next_blanket() -> int:
	for index in range(nursery_blankets_tucked.size()):
		if not nursery_blankets_tucked[index]:
			return index
	return -1


func _nursery_bedtime_grab_point(index: int) -> Vector2:
	var baby := _nursery_baby_center(clampi(index, 0, 2))
	return baby - Vector2(0.0, size.y * 0.015)


func _nursery_bedtime_grab_rect(index: int) -> Rect2:
	var center := _nursery_bedtime_grab_point(index)
	var extent := Vector2(maxf(44.0, size.x * 0.10), maxf(38.0, size.y * 0.15))
	return Rect2(center - extent, extent * 2.0).intersection(Rect2(Vector2.ZERO, size))


func _nursery_bedtime_required_travel() -> float:
	return maxf(48.0, size.y * 0.20)


func _nursery_bedtime_rehint(at: Vector2) -> void:
	feedback_positive = false
	feedback_t = 0.24
	feedback_anchor = at
	demo_active = true
	demo_t = 0.0
	gesture.emit("swipe", 0.0, 0.35)


func _nursery_bedtime_press(at: Vector2) -> void:
	nursery_blanket_active = _nursery_bedtime_next_blanket()
	if nursery_blanket_active < 0:
		return
	if not _nursery_bedtime_grab_rect(nursery_blanket_active).has_point(at):
		_nursery_bedtime_rehint(at)
		return
	nursery_blanket_dragging = true
	nursery_blanket_drag_start = at
	nursery_blanket_progress[nursery_blanket_active] = 0.0


func _nursery_bedtime_drag(at: Vector2) -> void:
	if not nursery_blanket_dragging or nursery_blanket_active < 0:
		return
	var delta := at - nursery_blanket_drag_start
	if delta.y <= 0.0 or absf(delta.x) > maxf(34.0, delta.y * 1.15):
		nursery_blanket_progress[nursery_blanket_active] = 0.0
		nursery_blanket_dragging = false
		_nursery_bedtime_rehint(at)
		queue_redraw()
		return
	var progress := clampf(delta.y / _nursery_bedtime_required_travel(), 0.0, 1.0)
	nursery_blanket_progress[nursery_blanket_active] = progress
	if progress >= 0.999:
		nursery_blankets_tucked[nursery_blanket_active] = true
		nursery_blanket_progress[nursery_blanket_active] = 1.0
		feedback_positive = true
		feedback_t = 0.30
		feedback_anchor = _nursery_baby_center(nursery_blanket_active)
		gesture.emit("swipe", 1.0, 1.0)
		nursery_blanket_dragging = false
		nursery_blanket_active = _nursery_bedtime_next_blanket()
		if nursery_blanket_active >= 0:
			demo_active = true
			demo_t = 0.0
	queue_redraw()


func _nursery_bedtime_release() -> void:
	if not nursery_blanket_dragging:
		return
	if nursery_blanket_active >= 0 and nursery_blanket_active < nursery_blanket_progress.size():
		nursery_blanket_progress[nursery_blanket_active] = 0.0
	nursery_blanket_dragging = false
	_nursery_bedtime_rehint(pointer_pos)


func _draw_nursery_bedtime_scene(_center: Vector2) -> void:
	_draw_causal_backdrop(Color("#30375f"), Color("#4e5278"))
	for index in range(3):
		var crib_center := _nursery_baby_center(index)
		var crib := _nursery_bedtime_crib_rect(index)
		draw_rect(crib, Color("#e8c7b9"), true)
		_draw_nursery_baby(index, crib_center - Vector2(0.0, size.y * 0.04),
			minf(size.x, size.y) * 0.27)
		var blanket_top := _nursery_blanket_top(index)
		var blanket_bottom := _nursery_blanket_bottom(index)
		if blanket_bottom > blanket_top:
			var blanket := Rect2(crib.position.x + 5.0, blanket_top,
				crib.size.x - 10.0, blanket_bottom - blanket_top)
			draw_rect(blanket, Color("#72bfc2"), true)
			draw_arc(Vector2(blanket.get_center().x, blanket.position.y),
				blanket.size.x * 0.48, PI, TAU, 24, Color("#d7f4ee"), 5.0)
		draw_rect(crib, Color("#7a5965"), false, 4.0)
	var all_tucked := _nursery_bedtime_next_blanket() < 0
	if completion_accepted or all_tucked:
		for star_index in range(5):
			draw_circle(Vector2(size.x * (0.18 + 0.16 * float(star_index)),
				size.y * (0.16 + 0.04 * float(star_index % 2))), 6.0,
				Color("#ffe783"))


func _nursery_burp_hand_point(progress: float) -> Vector2:
	var baby := _nursery_baby_center(1) - Vector2(0.0, size.y * 0.07)
	var rest := baby + Vector2(size.x * 0.25, -size.y * 0.10)
	var contact := baby + Vector2(size.x * 0.07, 0.0)
	return rest.lerp(contact, clampf(progress, 0.0, 1.0))


func _draw_nursery_burp_scene(_center: Vector2) -> void:
	_draw_causal_backdrop(Color("#f4ecfb"), Color("#d8c7e9"))
	var pat_phase := 0.0
	if nursery_burp_pat_t > 0.0:
		pat_phase = sin(clampf(1.0 - nursery_burp_pat_t / 0.42, 0.0, 1.0) * PI)
	var baby_center := _nursery_baby_center(1) + Vector2(0.0, pat_phase * 5.0)
	draw_set_transform(baby_center, sin(pat_phase * PI) * -0.035,
		Vector2(1.0 + pat_phase * 0.06, 1.0 - pat_phase * 0.04))
	_draw_nursery_baby(1, Vector2.ZERO, minf(size.x, size.y) * 0.52)
	draw_set_transform(Vector2.ZERO)
	var hand := _nursery_burp_hand_point(pat_phase)
	draw_circle(hand, minf(size.x, size.y) * 0.09, Color("#ffd5bc"))
	draw_arc(hand, minf(size.x, size.y) * 0.14, -1.25, 1.25, 24, accent, 6.0)
	if pat_phase > 0.45:
		for reaction_index in range(3):
			var reaction := baby_center + Vector2(size.x * (0.08 + 0.04 * float(reaction_index)),
				-size.y * (0.18 + 0.055 * float(reaction_index)))
			draw_circle(reaction, 4.0 + float(reaction_index) * 2.0,
				Color(1.0, 1.0, 1.0, 0.78))


func _magic_vanish_hat_position(progress: float) -> Vector2:
	var amount := clampf(progress / 0.62, 0.0, 1.0)
	amount = amount * amount * (3.0 - 2.0 * amount)
	return Vector2(size.x * 0.29, size.y * 0.64).lerp(
		Vector2(size.x * 0.50, size.y * 0.58), amount)


func _magic_vanish_wand_position(progress: float) -> Vector2:
	return Vector2(size.x * 0.73, size.y * 0.36).lerp(
		Vector2(size.x * 0.64, size.y * 0.40), clampf(progress, 0.0, 1.0))


func _magic_vanish_wand_rotation(progress: float) -> float:
	var amount := clampf(progress, 0.0, 1.0)
	return lerpf(-0.32, 0.24, amount) + sin(amount * TAU) * 0.12


func _magic_vanish_reveal_amount(progress: float) -> float:
	return clampf((progress - 0.58) / 0.42, 0.0, 1.0)


func _magic_vanish_hat_rect(progress: float) -> Rect2:
	var side := minf(size.x, size.y) * 0.50
	return Rect2(_magic_vanish_hat_position(progress) - Vector2.ONE * side * 0.5,
		Vector2.ONE * side)


func _magic_vanish_wand_rect(progress: float) -> Rect2:
	var side := minf(size.x, size.y) * 0.46
	return Rect2(_magic_vanish_wand_position(progress) - Vector2.ONE * side * 0.5,
		Vector2.ONE * side)


func _magic_vanish_reveal_rect(progress: float) -> Rect2:
	var reveal_amount := _magic_vanish_reveal_amount(progress)
	var center := Vector2(size.x * 0.50, size.y * 0.52)
	var side := minf(size.x, size.y) * (0.50 + reveal_amount * 0.24)
	return Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _draw_magic_vanish_scene(center: Vector2) -> void:
	_draw_causal_backdrop(Color("#20183f"), Color("#3b2557"))
	var progress := clampf(widget_fill, 0.0, 1.0)
	var reveal_amount := _magic_vanish_reveal_amount(progress)
	var hat_center := _magic_vanish_hat_position(progress)
	# Lamba settles under the travelling hat first; only then does the authored
	# bunny-fish reveal grow out. This keeps hold -> wand -> hat -> reveal causal.
	var lamb_center := Vector2(center.x, lerpf(size.y * 0.42, size.y * 0.59, progress))
	var lamb_alpha := clampf(1.0 - progress / 0.72, 0.0, 1.0)
	draw_circle(lamb_center, minf(size.x, size.y) * 0.13,
		Color(0.95, 0.94, 1.0, lamb_alpha))
	draw_circle(lamb_center + Vector2(-14.0, -18.0), 11.0,
		Color(0.95, 0.94, 1.0, lamb_alpha))
	draw_circle(lamb_center + Vector2(14.0, -18.0), 11.0,
		Color(0.95, 0.94, 1.0, lamb_alpha))
	var hat_alpha := 1.0 - reveal_amount
	var hat_side := _magic_vanish_hat_rect(progress).size.x
	draw_set_transform(hat_center, lerpf(-0.24, -0.04, progress),
		Vector2.ONE * (0.82 + progress * 0.18))
	if magic_vanish_hat_texture != null:
		draw_texture_rect(magic_vanish_hat_texture,
			Rect2(Vector2.ONE * -hat_side * 0.5, Vector2.ONE * hat_side), false,
			Color(1.0, 1.0, 1.0, hat_alpha))
	else:
		var hat_width := minf(size.x * 0.44, size.y * 0.66)
		draw_rect(Rect2(-hat_width * 0.50, 0.0, hat_width, size.y * 0.075),
			Color(0.07, 0.07, 0.15, hat_alpha), true)
		draw_colored_polygon(PackedVector2Array([
			Vector2(-hat_width * 0.29, 0.0), Vector2(hat_width * 0.29, 0.0),
			Vector2(hat_width * 0.20, -size.y * 0.31),
			Vector2(-hat_width * 0.20, -size.y * 0.31),
		]), Color(0.19, 0.13, 0.30, hat_alpha))
	draw_set_transform(Vector2.ZERO)
	var wand_center := _magic_vanish_wand_position(progress)
	var wand_side := _magic_vanish_wand_rect(progress).size.x
	draw_set_transform(wand_center, _magic_vanish_wand_rotation(progress))
	if magic_vanish_wand_texture != null:
		draw_texture_rect(magic_vanish_wand_texture,
			Rect2(Vector2.ONE * -wand_side * 0.5, Vector2.ONE * wand_side), false)
	else:
		draw_line(Vector2(wand_side * -0.34, wand_side * 0.28),
			Vector2(wand_side * 0.30, wand_side * -0.30), Color("#f7e2a8"), 8.0, true)
		draw_circle(Vector2(wand_side * 0.30, wand_side * -0.30), 9.0,
			Color("#ffe56f"))
	draw_set_transform(Vector2.ZERO)
	if reveal_amount > 0.0:
		var reveal_rect := _magic_vanish_reveal_rect(progress)
		var reveal_center := reveal_rect.get_center()
		var reveal_side := reveal_rect.size.x
		if magic_vanish_reveal_texture != null:
			draw_texture_rect(magic_vanish_reveal_texture,
				reveal_rect, false,
				Color(1.0, 1.0, 1.0, reveal_amount))
		else:
			# Bunny-fish code fallback: pearl body, ears, fin and tail above hat.
			draw_circle(reveal_center, reveal_side * 0.16,
				Color(0.95, 0.58, 0.72, reveal_amount))
			for ear_sign: float in [-1.0, 1.0]:
				draw_colored_polygon(PackedVector2Array([
					reveal_center + Vector2(ear_sign * 8.0, -12.0),
					reveal_center + Vector2(ear_sign * 15.0, -46.0),
					reveal_center + Vector2(ear_sign * 27.0, -10.0),
				]), Color(0.98, 0.67, 0.77, reveal_amount))
			draw_colored_polygon(PackedVector2Array([
				reveal_center + Vector2(-18.0, 4.0),
				reveal_center + Vector2(-48.0, -15.0),
				reveal_center + Vector2(-46.0, 20.0),
			]), Color(0.76, 0.56, 0.82, reveal_amount))
	var magic_alpha := clampf((progress - 0.18) / 0.82, 0.0, 1.0)
	for sparkle_index in range(8):
		var angle := float(sparkle_index) / 8.0 * TAU + progress * 2.4
		var sparkle := Vector2(size.x * 0.50, size.y * 0.45) \
			+ Vector2.from_angle(angle) * (20.0 + 44.0 * magic_alpha)
		draw_circle(sparkle, 3.0 + float(sparkle_index % 3),
			Color(1.0, 0.86, 0.34, magic_alpha))
	if completion_accepted or progress >= 0.999:
		draw_arc(Vector2(size.x * 0.50, size.y * 0.45),
			minf(size.x, size.y) * 0.30, 0.0, TAU, 40,
			Color(1.0, 0.86, 0.34, 0.64), 7.0)


func _clue_home_point() -> Vector2:
	# Evidence tray sits below the board so the three approved silhouettes stay
	# readable as one left-to-right paw / feather / ribbon sequence.
	return Vector2(size.x * 0.50, size.y * 0.84)


func _clue_target_rect(index: int) -> Rect2:
	var target_index := clampi(index, 0, CLUE_BOARD_COUNT - 1)
	var center := Vector2(size.x * (0.28 + float(target_index) * 0.22), size.y * 0.47)
	return Rect2(center - Vector2(size.x * 0.095, size.y * 0.13),
		Vector2(size.x * 0.19, size.y * 0.26))


func _clue_token_rect() -> Rect2:
	var side := maxf(64.0, minf(size.x, size.y) * 0.30)
	return Rect2(clue_token_pos - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _clue_rehint(at: Vector2) -> void:
	feedback_positive = false
	feedback_t = 0.24
	feedback_anchor = at
	demo_active = true
	demo_t = 0.0
	gesture.emit("clue_board", 0.0, 0.35)


func _clue_press(at: Vector2) -> void:
	if clue_complete or completion_accepted:
		return
	if _clue_token_rect().grow(22.0).has_point(at):
		clue_dragging = true
		clue_drag_offset = clue_token_pos - at
		clue_return_t = 0.0
		return
	_clue_rehint(at)


func _clue_drag(at: Vector2) -> void:
	if not clue_dragging:
		return
	var margin := maxf(24.0, minf(size.x, size.y) * 0.07)
	clue_token_pos = Vector2(
		clampf(at.x + clue_drag_offset.x, margin, size.x - margin),
		clampf(at.y + clue_drag_offset.y, margin, size.y - margin))
	queue_redraw()


func _clue_release(at: Vector2) -> void:
	if not clue_dragging:
		return
	clue_dragging = false
	if _clue_target_rect(clue_index).grow(24.0).has_point(at):
		feedback_positive = true
		feedback_t = 0.32
		feedback_anchor = _clue_target_rect(clue_index).get_center()
		clue_glow = 0.48
		clue_index += 1
		clue_complete = clue_index >= CLUE_BOARD_COUNT
		clue_token_pos = _clue_home_point()
		gesture.emit("clue_board", 1.0, 1.0)
		return
	# A mismatch visibly travels home instead of teleporting or being lost.
	clue_return_from = clue_token_pos
	clue_return_t = 1.0
	_clue_rehint(at)


func _clue_tick(delta: float) -> void:
	var changed := false
	if clue_return_t > 0.0:
		clue_return_t = maxf(0.0, clue_return_t - delta / 0.38)
		var eased := clue_return_t * clue_return_t * (3.0 - 2.0 * clue_return_t)
		clue_token_pos = _clue_home_point().lerp(clue_return_from, eased)
		changed = true
	if clue_glow > 0.0:
		clue_glow = maxf(0.0, clue_glow - delta)
		changed = true
	if changed:
		queue_redraw()


func _draw_clue_token(index: int, center: Vector2, side: float, alpha := 1.0) -> void:
	if clue_board_tokens_texture != null:
		var texture_size := clue_board_tokens_texture.get_size()
		var source_width := texture_size.x / float(CLUE_BOARD_COUNT)
		var source := Rect2(source_width * float(clampi(index, 0, CLUE_BOARD_COUNT - 1)),
			0.0, source_width, texture_size.y)
		draw_texture_rect_region(clue_board_tokens_texture,
			Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side), source,
			Color(1.0, 1.0, 1.0, alpha))
		return
	var clue_colors: Array[Color] = [Color("#ef6f91"), Color("#5bc7c5"), Color("#f3c54f")]
	var color: Color = clue_colors[index % clue_colors.size()]
	draw_circle(center, side * 0.31, Color(color, alpha))
	draw_arc(center, side * 0.31, 0.0, TAU, 28,
		Color(0.22, 0.16, 0.36, alpha), 4.0)
	match index % CLUE_BOARD_COUNT:
		0:
			# paw print
			draw_circle(center + Vector2(0.0, side * 0.06), side * 0.105,
				Color(1.0, 1.0, 1.0, alpha))
			for toe_x: float in [-0.13, -0.045, 0.045, 0.13]:
				draw_circle(center + Vector2(side * toe_x, -side * 0.09),
					side * 0.045, Color(1.0, 1.0, 1.0, alpha))
		1:
			# feather and shaft
			draw_colored_polygon(PackedVector2Array([
				center + Vector2(-side * 0.14, side * 0.14),
				center + Vector2(-side * 0.07, -side * 0.12),
				center + Vector2(side * 0.14, -side * 0.17),
				center + Vector2(side * 0.07, side * 0.08),
			]), Color(1.0, 1.0, 1.0, alpha))
			draw_line(center + Vector2(-side * 0.15, side * 0.16),
				center + Vector2(side * 0.13, -side * 0.15),
				Color(color, alpha), 4.0)
		2:
			# prize ribbon with two tails
			draw_circle(center - Vector2(0.0, side * 0.05), side * 0.11,
				Color(1.0, 1.0, 1.0, alpha))
			draw_colored_polygon(PackedVector2Array([
				center + Vector2(-side * 0.08, side * 0.02),
				center + Vector2(-side * 0.14, side * 0.17),
				center + Vector2(0.0, side * 0.11),
				center + Vector2(side * 0.14, side * 0.17),
				center + Vector2(side * 0.08, side * 0.02),
			]), Color(1.0, 1.0, 1.0, alpha))


func _draw_clue_board() -> void:
	if clue_complete and clue_board_complete_texture != null:
		draw_texture_rect(clue_board_complete_texture,
			_cover_rect(clue_board_complete_texture), false)
	else:
		if clue_board_empty_texture != null:
			draw_texture_rect(clue_board_empty_texture,
				_cover_rect(clue_board_empty_texture), false)
		else:
			draw_rect(Rect2(size.x * 0.12, size.y * 0.16,
				size.x * 0.76, size.y * 0.58), Color("#7d5a48"), true)
			draw_rect(Rect2(size.x * 0.14, size.y * 0.19,
				size.x * 0.72, size.y * 0.52), Color("#eadcbf"), true)
	var token_side := maxf(58.0, minf(size.x, size.y) * 0.27)
	for index in range(CLUE_BOARD_COUNT):
		var target := _clue_target_rect(index)
		var accepted := index < clue_index
		draw_rect(target, Color(0.25, 0.18, 0.34, 0.13 if not accepted else 0.24), true)
		draw_rect(target, Color(0.31, 0.24, 0.38, 0.52), false, 4.0)
		if accepted:
			_draw_clue_token(index, target.get_center(), token_side)
		elif index == clue_index:
			_draw_clue_token(index, target.get_center(), token_side * 0.68, 0.20)
	if not clue_complete:
		_draw_clue_token(clue_index, clue_token_pos, token_side)
		draw_arc(_clue_home_point(), token_side * 0.45, 0.0, TAU, 32,
			Color(accent, 0.32), 5.0)
	if clue_glow > 0.0:
		var accepted_index := clampi(clue_index - 1, 0, CLUE_BOARD_COUNT - 1)
		draw_arc(_clue_target_rect(accepted_index).get_center(),
			token_side * (0.45 + (0.48 - clue_glow) * 0.34), 0.0, TAU, 32,
			Color(1.0, 0.86, 0.34, clue_glow / 0.48), 7.0)


func _crown_handle_rect() -> Rect2:
	return Rect2(size.x * 0.35, size.y * 0.63, size.x * 0.30, size.y * 0.16)


func _crown_press(at: Vector2) -> void:
	if crown_opened or completion_accepted:
		return
	if not _crown_handle_rect().grow(maxf(22.0, minf(size.x, size.y) * 0.06)).has_point(at):
		feedback_positive = false
		feedback_t = 0.24
		feedback_anchor = at
		demo_active = true
		demo_t = 0.0
		gesture.emit("crown_chest", 0.0, 0.35)
		return
	crown_opened = true
	crown_open_t = maxf(crown_open_t, 0.04)
	feedback_positive = true
	feedback_t = 0.32
	feedback_anchor = _crown_handle_rect().get_center()
	gesture.emit("crown_chest", 1.0, 1.0)


func _crown_tick(delta: float) -> void:
	if not crown_opened or crown_open_t >= 1.0:
		return
	crown_open_t = minf(1.0, crown_open_t + delta * 2.25)
	queue_redraw()


func _draw_crown_chest() -> void:
	_draw_causal_backdrop(Color("#e7f6f2"), Color("#bfded3"))
	if crown_chest_closed_texture != null:
		draw_texture_rect(crown_chest_closed_texture,
			_cover_rect(crown_chest_closed_texture), false,
			Color(1.0, 1.0, 1.0, 1.0 - crown_open_t))
	if crown_chest_open_texture != null and crown_open_t > 0.0:
		draw_texture_rect(crown_chest_open_texture,
			_cover_rect(crown_chest_open_texture), false,
			Color(1.0, 1.0, 1.0, crown_open_t))
	if crown_chest_closed_texture == null or crown_chest_open_texture == null:
		var chest := Rect2(size.x * 0.22, size.y * 0.43, size.x * 0.56, size.y * 0.36)
		draw_rect(chest, Color("#9c603d"), true)
		draw_rect(chest, Color("#59384b"), false, 6.0)
		var lid_y := lerpf(chest.position.y, chest.position.y - size.y * 0.19, crown_open_t)
		var lid := Rect2(chest.position.x - 4.0, lid_y, chest.size.x + 8.0, size.y * 0.16)
		draw_rect(lid, Color("#bd7949"), true)
		draw_rect(lid, Color("#59384b"), false, 6.0)
		var crown_center := Vector2(chest.get_center().x,
			lerpf(chest.get_center().y, chest.position.y - size.y * 0.12, crown_open_t))
		if crown_open_t > 0.0:
			draw_colored_polygon(PackedVector2Array([
				crown_center + Vector2(-48.0, 24.0),
				crown_center + Vector2(-40.0, -22.0),
				crown_center + Vector2(-12.0, 4.0),
				crown_center + Vector2(0.0, -32.0),
				crown_center + Vector2(16.0, 3.0),
				crown_center + Vector2(43.0, -21.0),
				crown_center + Vector2(48.0, 24.0),
			]), Color(1.0, 0.80, 0.20, crown_open_t))
	if not crown_opened:
		var handle := _crown_handle_rect()
		# The recorded direction says to tap the spotlight. Give that phrase a
		# literal, slowly breathing visual referent over the chest handle.
		var spotlight_width := handle.size.x * (1.7 + sin(demo_t * 2.4) * 0.08)
		draw_colored_polygon(PackedVector2Array([
			Vector2(size.x * 0.42, 0.0),
			Vector2(size.x * 0.58, 0.0),
			handle.get_center() + Vector2(spotlight_width, handle.size.y),
			handle.get_center() + Vector2(-spotlight_width, handle.size.y),
		]), Color(1.0, 0.94, 0.62, 0.13))
		draw_rect(handle, Color("#f3c95d"), true)
		draw_rect(handle, Color("#59384b"), false, 4.0)
		draw_arc(handle.get_center(), handle.size.y * 0.62 + sin(demo_t * 4.0) * 5.0,
			0.0, TAU, 32, Color(1.0, 0.86, 0.34, 0.55), 6.0)
	else:
		for sparkle_index in range(6):
			var angle := float(sparkle_index) / 6.0 * TAU
			var sparkle := Vector2(size.x * 0.5, size.y * 0.29) \
				+ Vector2.from_angle(angle) * (42.0 + crown_open_t * 22.0)
			draw_circle(sparkle, 4.0 + float(sparkle_index % 2) * 2.0,
				Color(1.0, 0.87, 0.34, crown_open_t))


func _garden_seed_home() -> Vector2:
	return Vector2(size.x * 0.13, size.y * 0.84)


func _garden_hole_point(index: int) -> Vector2:
	if GARDEN_HOLES.is_empty():
		return size * 0.5
	var normalized: Vector2 = GARDEN_HOLES[clampi(index, 0, GARDEN_HOLES.size() - 1)]
	return Vector2(size.x * normalized.x, size.y * normalized.y)


func _garden_seed_rect() -> Rect2:
	var side := maxf(54.0, minf(size.x, size.y) * 0.24)
	return Rect2(garden_seed_pos - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _garden_rehint(at: Vector2) -> void:
	demo_active = true
	demo_t = 0.0
	feedback_anchor = at
	gesture.emit("garden_plant", 0.0, 0.55)


func _garden_accept() -> void:
	if garden_planted >= GARDEN_HOLES.size():
		return
	garden_growth[garden_planted] = 0.04
	feedback_positive = true
	feedback_t = 0.32
	feedback_anchor = _garden_hole_point(garden_planted)
	garden_planted += 1
	garden_seed_dragging = false
	garden_seed_pos = _garden_seed_home()
	gesture.emit("garden_plant", 1.0, 1.0)


func _garden_press(at: Vector2) -> void:
	if garden_planted >= GARDEN_HOLES.size() or completion_accepted:
		return
	var hole := _garden_hole_point(garden_planted)
	var reach := maxf(42.0, minf(size.x, size.y) * 0.14)
	if at.distance_to(hole) <= reach:
		_garden_accept()
		return
	if _garden_seed_rect().grow(18.0).has_point(at):
		garden_seed_dragging = true
		garden_seed_offset = garden_seed_pos - at
		return
	_garden_rehint(at)


func _garden_drag(at: Vector2) -> void:
	if not garden_seed_dragging:
		return
	var margin := maxf(20.0, minf(size.x, size.y) * 0.06)
	garden_seed_pos = Vector2(
		clampf(at.x + garden_seed_offset.x, margin, size.x - margin),
		clampf(at.y + garden_seed_offset.y, margin, size.y - margin))
	queue_redraw()


func _garden_release(at: Vector2) -> void:
	if not garden_seed_dragging:
		return
	garden_seed_dragging = false
	var reach := maxf(48.0, minf(size.x, size.y) * 0.16)
	if at.distance_to(_garden_hole_point(garden_planted)) <= reach:
		_garden_accept()
		return
	garden_seed_pos = _garden_seed_home()
	_garden_rehint(at)


func _garden_tick(delta: float) -> void:
	var changed := false
	for index in range(garden_growth.size()):
		if garden_growth[index] > 0.0 and garden_growth[index] < 1.0:
			garden_growth[index] = minf(1.0, garden_growth[index] + delta * 1.9)
			changed = true
	if changed:
		queue_redraw()


func _draw_garden_plant() -> void:
	_draw_causal_backdrop(Color("#dff3d5"), Color("#89ba70"))
	draw_rect(Rect2(size.x * 0.12, size.y * 0.18, size.x * 0.76, size.y * 0.65),
		Color("#8c6541"), true)
	draw_rect(Rect2(size.x * 0.12, size.y * 0.18, size.x * 0.76, size.y * 0.65),
		Color("#5c463b"), false, 5.0)
	for index in range(GARDEN_HOLES.size()):
		var hole := _garden_hole_point(index)
		var growth := garden_growth[index]
		draw_circle(hole, minf(size.x, size.y) * 0.065, Color("#4e392f"))
		if index == garden_planted and garden_planted < GARDEN_HOLES.size():
			var pulse := 0.48 + 0.18 * sin(demo_t * 4.5)
			draw_arc(hole, minf(size.x, size.y) * 0.105, 0.0, TAU, 32,
				Color(1.0, 0.88, 0.34, pulse), 7.0)
		if growth > 0.0:
			var stem_top := hole - Vector2(0.0, size.y * 0.20 * growth)
			draw_line(hole, stem_top, Color("#397b48"), 8.0, true)
			draw_circle(stem_top + Vector2(-10.0, 7.0), 10.0 * growth,
				Color("#62a85b"))
			draw_circle(stem_top + Vector2(10.0, -2.0), 10.0 * growth,
				Color("#78bd68"))
			if growth >= 0.88:
				draw_circle(stem_top, 8.0, Color("#f4cf62"))
	if garden_planted < GARDEN_HOLES.size():
		var seed_side := maxf(50.0, minf(size.x, size.y) * 0.22)
		if garden_seed_texture != null:
			draw_texture_rect(garden_seed_texture,
				Rect2(garden_seed_pos - Vector2.ONE * seed_side * 0.5,
					Vector2.ONE * seed_side), false)
		else:
			draw_set_transform(garden_seed_pos, -0.45)
			draw_circle(Vector2.ZERO, seed_side * 0.19, Color("#e8b367"))
			draw_set_transform(Vector2.ZERO)


func _cabinet_handle_rect() -> Rect2:
	return Rect2(size.x * 0.38, size.y * 0.25, size.x * 0.24, size.y * 0.15)


func _cabinet_required_travel() -> float:
	return maxf(70.0, size.y * 0.28)


func _cabinet_rehint(at: Vector2) -> void:
	cabinet_dragging = false
	cabinet_travel = 0.0
	cabinet_open_t = 0.0
	feedback_positive = false
	feedback_t = 0.24
	feedback_anchor = at
	demo_active = true
	demo_t = 0.0
	gesture.emit("magic_cabinet", 0.0, 0.35)


func _cabinet_press(at: Vector2) -> void:
	if cabinet_complete or completion_accepted:
		return
	if not _cabinet_handle_rect().grow(maxf(22.0, minf(size.x, size.y) * 0.06)).has_point(at):
		_cabinet_rehint(at)
		return
	cabinet_dragging = true
	cabinet_drag_start = at
	cabinet_travel = 0.0


func _cabinet_drag(at: Vector2) -> void:
	if not cabinet_dragging or cabinet_complete:
		return
	var delta := at - cabinet_drag_start
	# Directness matters: horizontal scrubbing cannot be converted into door
	# travel, and only displacement below the original handle counts.
	cabinet_travel = maxf(0.0, delta.y - absf(delta.x) * 0.65)
	var ratio := clampf(cabinet_travel / _cabinet_required_travel(), 0.0, 1.0)
	cabinet_open_t = ratio * 0.62
	if ratio >= 1.0:
		cabinet_complete = true
		cabinet_dragging = false
		cabinet_open_t = maxf(cabinet_open_t, 0.64)
		feedback_positive = true
		feedback_t = 0.32
		feedback_anchor = at
		gesture.emit("magic_cabinet", 1.0, 1.0)
	queue_redraw()


func _cabinet_release() -> void:
	if cabinet_complete:
		return
	if not cabinet_dragging:
		return
	_cabinet_rehint(pointer_pos)


func _cabinet_tick(delta: float) -> void:
	if not cabinet_complete or cabinet_open_t >= 1.0:
		return
	cabinet_open_t = minf(1.0, cabinet_open_t + delta * 2.0)
	queue_redraw()


func _draw_magic_cabinet() -> void:
	_draw_causal_backdrop(Color("#221943"), Color("#4b2a62"))
	if magic_cabinet_closed_texture != null:
		draw_texture_rect(magic_cabinet_closed_texture,
			_cover_rect(magic_cabinet_closed_texture), false,
			Color(1.0, 1.0, 1.0, 1.0 - cabinet_open_t * 0.92))
	if magic_cabinet_reveal_texture != null and cabinet_complete:
		var reveal_alpha := clampf((cabinet_open_t - 0.55) / 0.45, 0.0, 1.0)
		draw_texture_rect(magic_cabinet_reveal_texture,
			_cover_rect(magic_cabinet_reveal_texture), false,
			Color(1.0, 1.0, 1.0, reveal_alpha))
	if magic_cabinet_closed_texture == null or magic_cabinet_reveal_texture == null:
		var body := Rect2(size.x * 0.22, size.y * 0.08, size.x * 0.56, size.y * 0.80)
		draw_rect(body, Color("#3a2455"), true)
		draw_rect(body, Color("#d6a34e"), false, 7.0)
		var inner := body.grow(-18.0)
		draw_rect(inner, Color(0.08, 0.05, 0.16, 0.95), true)
		# The revealed pearl rises before the doors finish opening.
		var reveal_center := Vector2(body.get_center().x,
			lerpf(body.end.y - size.y * 0.14, body.get_center().y, cabinet_open_t))
		if cabinet_complete:
			var fallback_reveal_alpha := clampf(
				(cabinet_open_t - 0.55) / 0.45, 0.0, 1.0)
			# Lamba's bunny-fish silhouette: ears above a pearl body, little
			# fins/tail below. This is the clear code fallback until the approved
			# separate reveal overlay is imported.
			draw_circle(reveal_center, minf(size.x, size.y) * 0.11,
				Color(0.78, 0.98, 1.0, fallback_reveal_alpha))
			for ear_sign: float in [-1.0, 1.0]:
				draw_colored_polygon(PackedVector2Array([
					reveal_center + Vector2(ear_sign * 8.0, -16.0),
					reveal_center + Vector2(ear_sign * 15.0, -42.0),
					reveal_center + Vector2(ear_sign * 23.0, -12.0),
				]), Color(0.88, 0.99, 1.0, fallback_reveal_alpha))
			draw_colored_polygon(PackedVector2Array([
				reveal_center + Vector2(-8.0, 18.0),
				reveal_center + Vector2(-34.0, 36.0),
				reveal_center + Vector2(-30.0, 8.0),
			]), Color(0.68, 0.91, 0.96, fallback_reveal_alpha))
			draw_circle(reveal_center - Vector2(9.0, 9.0), 5.0,
				Color(0.20, 0.18, 0.35, fallback_reveal_alpha))
		var half := inner.size.x * 0.5
		var door_offset := cabinet_open_t * size.x * 0.16
		var left := Rect2(inner.position - Vector2(door_offset, 0.0),
			Vector2(half, inner.size.y))
		var right := Rect2(Vector2(inner.position.x + half + door_offset, inner.position.y),
			Vector2(half, inner.size.y))
		draw_rect(left, Color("#704085"), true)
		draw_rect(right, Color("#704085"), true)
		draw_rect(left, Color("#d6a34e"), false, 4.0)
		draw_rect(right, Color("#d6a34e"), false, 4.0)
	if not cabinet_complete:
		var base_handle := _cabinet_handle_rect()
		var handle := Rect2(base_handle.position + Vector2.DOWN * cabinet_travel,
			base_handle.size)
		draw_rect(handle, Color("#f0c75a"), true)
		draw_rect(handle, Color("#4b2b56"), false, 4.0)
		draw_line(handle.get_center(),
			handle.get_center() + Vector2.DOWN * maxf(34.0, size.y * 0.13),
			Color(1.0, 0.86, 0.34, 0.58), 7.0, true)
	else:
		for sparkle_index in range(8):
			var angle := float(sparkle_index) / 8.0 * TAU + cabinet_open_t
			var sparkle := size * 0.5 + Vector2.from_angle(angle) \
				* minf(size.x, size.y) * (0.15 + cabinet_open_t * 0.08)
			draw_circle(sparkle, 4.0 + float(sparkle_index % 3),
				Color(1.0, 0.87, 0.34, cabinet_open_t))


func _draw_nursery_baby(texture_index: int, center: Vector2, extent: float) -> void:
	if nursery_textures.is_empty():
		draw_circle(center, extent * 0.30, Color("#ffd6bf"))
		return
	var texture: Texture2D = nursery_textures[posmod(texture_index, nursery_textures.size())]
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * extent * 0.5, Vector2.ONE * extent), false)


func _draw_nursery_context(center: Vector2) -> void:
	match visual_context:
		"nursery_wash":
			var basin := Rect2(center.x - 92.0, center.y - 12.0, 184.0, 82.0)
			draw_rect(basin, Color("#78cfd0"), true)
			draw_arc(Vector2(center.x, basin.position.y), 92.0, 0.0, PI, 32, Color("#ecfbf4"), 10.0)
			for index in range(7):
				var bubble := center + Vector2(-70.0 + float(index) * 23.0, -48.0 - float(index % 3) * 17.0)
				draw_circle(bubble, 9.0 + float(index % 2) * 4.0, Color(0.82, 0.97, 1.0, 0.62))
			draw_circle(center, 25.0 if held else 17.0, Color.WHITE)
			draw_arc(center, 58.0, 0.0, TAU, 40, accent, 9.0)
		"nursery_feed":
			for index in range(3):
				_draw_nursery_baby(index, Vector2(86.0 + float(index) * 100.0, center.y + 48.0), 88.0)
			var bottle_center := Vector2(center.x, center.y - 58.0)
			draw_rect(Rect2(bottle_center - Vector2(23, 38), Vector2(46, 76)), Color("#edf9ee"), true)
			draw_rect(Rect2(bottle_center - Vector2(17, 31), Vector2(34, 51)), Color("#ffe7ac"), true)
			draw_circle(bottle_center + Vector2(0, -44), 12.0, Color("#f1b1a1"))
			draw_arc(bottle_center, 61.0, 0.0, TAU, 40, accent, 9.0)
			draw_circle(bottle_center, 22.0 if held else 15.0, Color.WHITE)
		"nursery_burp":
			_draw_nursery_baby(1, Vector2(center.x, 70.0), 105.0)
			var hand := Vector2(center.x + 92.0, 78.0)
			draw_circle(hand, 28.0, Color("#ffd8bd"))
			draw_arc(hand, 45.0, -1.2, 1.2, 24, accent, 8.0)
			var bar := Rect2(size.x * 0.12, size.y - 82.0, size.x * 0.76, 42.0)
			draw_rect(bar, Color(0.20, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 22.0), Vector2(marker_x, bar.end.y + 22.0), Color.WHITE, 11.0)
		"nursery_bedtime":
			for index in range(3):
				var crib_center := Vector2(72.0 + float(index) * 114.0, center.y + 20.0)
				draw_rect(Rect2(crib_center - Vector2(48, 30), Vector2(96, 78)), Color("#f1d2c2"), true)
				_draw_nursery_baby(index, crib_center - Vector2(0, 10), 74.0)
				draw_rect(Rect2(crib_center.x - 43.0, crib_center.y + 7.0, 86.0, 37.0), Color(0.52, 0.81, 0.77, 0.94), true)
			for star in [Vector2(55, 44), Vector2(145, 30), Vector2(235, 50)]:
				draw_circle(star, 7.0, Color("#ffe483"))
			var arrow_x := size.x - 24.0
			draw_line(Vector2(arrow_x, 54.0), Vector2(arrow_x, size.y - 42.0), accent, 13.0, true)
			draw_colored_polygon(PackedVector2Array([
				Vector2(arrow_x - 28.0, size.y - 68.0), Vector2(arrow_x + 28.0, size.y - 68.0), Vector2(arrow_x, size.y - 28.0),
			]), accent)

func _demo_finger_pose() -> Dictionary:
	var center := size * 0.5
	var cycle := fmod(demo_t, 2.4)
	var pressing := cycle > 1.1
	var at := center
	match mode:
		"tap":
			if _uses_anchored_targets():
				var target_index := _target_next_unplaced()
				if target_index >= 0:
					var target := _target_anchor_point(target_index)
					at = center.lerp(target, clampf(cycle / 1.0, 0.0, 1.0))
					pressing = cycle >= 1.0
			elif _is_nursery_burp_context():
				var pat_target := _nursery_burp_hand_point(1.0)
				at = center.lerp(pat_target, clampf(cycle / 0.9, 0.0, 1.0))
				pressing = cycle >= 0.9
		"swipe":
			if _is_nursery_bedtime_context():
				var blanket_index := _nursery_bedtime_next_blanket()
				if blanket_index >= 0:
					var blanket_start := _nursery_bedtime_grab_point(blanket_index)
					var blanket_end := blanket_start \
						+ Vector2.DOWN * _nursery_bedtime_required_travel()
					var blanket_travel := clampf(cycle / 1.65, 0.0, 1.0)
					blanket_travel = blanket_travel * blanket_travel \
						* (3.0 - 2.0 * blanket_travel)
					at = blanket_start.lerp(blanket_end, blanket_travel)
					pressing = cycle <= 1.78
			elif _uses_authored_trace_context():
				var trace_travel := clampf(cycle / 1.85, 0.0, 1.0)
				at = _trace_demo_point(trace_travel)
				pressing = cycle <= 1.95
			elif _uses_long_push_context():
				var push_travel := clampf(cycle / 1.85, 0.0, 1.0)
				push_travel = push_travel * push_travel * (3.0 - 2.0 * push_travel)
				at = _long_push_start().lerp(_long_push_end(), push_travel)
				pressing = cycle <= 1.95
			else:
				var direction := swipe_dir.normalized()
				if direction.length_squared() < 0.01:
					direction = Vector2.RIGHT
				var span := minf(size.x, size.y) * 0.34
				var travel := clampf(cycle / 1.85, 0.0, 1.0)
				travel = travel * travel * (3.0 - 2.0 * travel)
				at = center + direction * lerpf(-span, span, travel)
				pressing = true
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			at = center + Vector2.from_angle(-2.7 + cycle * 2.0) * radius
			pressing = true
		"choice":
			var lane := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), center.y)
			at = center.lerp(lane, clampf(cycle / 1.1, 0.0, 1.0))
		"timing":
			var bar_x := lerpf(size.x * 0.12, size.x * 0.88, timing_position)
			at = Vector2(bar_x, center.y + 58.0)
			pressing = timing_position >= timing_zone.x and timing_position <= timing_zone.y
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					var pos: Vector2 = target.get("pos", Vector2.ZERO)
					at = center.lerp(pos, clampf(cycle / 1.1, 0.0, 1.0))
					break
		"hold":
			if _is_nursery_feed_context():
				var feed_pose := _nursery_feed_bottle_pose(true)
				at = feed_pose.get("position", center) as Vector2
			pressing = true
		"pourt":
			# Approach the actual pitcher, then stay pressed while it would tilt.
			# A small rock makes the sustained grab readable without moving the
			# real gameplay state or pretending the bowl itself is the control.
			var pitcher_center := _pour_pitcher_rect().get_center()
			var approach := clampf(cycle / 0.8, 0.0, 1.0)
			at = center.lerp(pitcher_center, approach)
			pressing = cycle >= 0.8
			if pressing:
				at += Vector2(sin((cycle - 0.8) * 5.0) * 10.0, 0.0)
		"oven":
			var meter := _oven_meter_rect()
			var handle := _oven_handle_rect()
			if oven_t < 0.45 and not oven_done:
				# Watch the rising thermometer without showing a false early tap.
				at = Vector2(meter.get_center().x,
					meter.end.y - meter.size.y * clampf(oven_t, 0.0, 1.0))
				pressing = false
			else:
				# Once golden, travel from the meter to the real mitt handle and tap.
				var approach := clampf(cycle / 1.0, 0.0, 1.0)
				at = meter.get_center().lerp(handle.get_center(), approach)
				pressing = cycle >= 1.0
		"xray_scan":
			var scan_target := _xray_target_center(xray_found_count)
			var scan_start := _xray_home_point()
			var scan_travel := clampf(cycle / 1.65, 0.0, 1.0)
			scan_travel = scan_travel * scan_travel * (3.0 - 2.0 * scan_travel)
			at = scan_start.lerp(scan_target, scan_travel)
			pressing = cycle <= 1.78
		"pipe":
			var target_cell := _pipe_demo_target_cell()
			if target_cell >= 0:
				var destination := _pipe_cell_rect(target_cell).get_center()
				var start := center
				var demonstrates_drag := false
				var target_tile := String(pipe_grid[target_cell])
				if PIPE_MOUTHS.has(target_tile) and not pipe_fixed[target_cell]:
					# A stuck wrong pipe is lifted back toward the visible tray.
					start = destination
					destination = _pipe_tray_rect(pipe_tray.size()).get_center()
					demonstrates_drag = true
				elif not pipe_tray.is_empty():
					var slot := _pipe_demo_tray_slot(target_cell)
					slot = clampi(slot, 0, pipe_tray.size() - 1)
					start = _pipe_tray_rect(slot).get_center()
					demonstrates_drag = true
				var travel := clampf(cycle / 1.75, 0.0, 1.0)
				travel = travel * travel * (3.0 - 2.0 * travel)
				at = start.lerp(destination, travel)
				pressing = demonstrates_drag and cycle <= 1.85
		"dance_sequence":
			var pad := int(DANCE_SEQUENCE[0])
			if dance_listening:
				pad = int(DANCE_SEQUENCE[clampi(
					dance_input_index, 0, DANCE_SEQUENCE.size() - 1)])
				var dance_target := _dance_pad_rect(pad).get_center()
				at = Vector2(center.x, size.y * 0.94).lerp(
					dance_target, clampf(cycle / 1.0, 0.0, 1.0))
				pressing = cycle >= 1.0
			else:
				if dance_show_index >= 0 and dance_show_index < DANCE_SEQUENCE.size():
					pad = int(DANCE_SEQUENCE[dance_show_index])
				at = Vector2(_dance_pad_rect(pad).get_center().x, size.y * 0.94)
				pressing = false
		"candy_sort":
			var candy_target := _candy_bin_rect(candy_type).get_center()
			var candy_travel := clampf((cycle - 0.35) / 1.45, 0.0, 1.0)
			candy_travel = candy_travel * candy_travel * (3.0 - 2.0 * candy_travel)
			at = candy_position.lerp(candy_target, candy_travel)
			pressing = cycle >= 0.35 and cycle <= 1.90
		"paint_reveal":
			var canvas := _paint_canvas_rect()
			var stroke_points: Array[Vector2] = [
				canvas.position + canvas.size * Vector2(0.16, 0.25),
				canvas.position + canvas.size * Vector2(0.84, 0.25),
				canvas.position + canvas.size * Vector2(0.16, 0.55),
				canvas.position + canvas.size * Vector2(0.84, 0.78),
			]
			var stroke_progress := clampf(cycle / 2.15, 0.0, 0.999)
			var stroke_scaled := stroke_progress * float(stroke_points.size() - 1)
			var stroke_index := clampi(floori(stroke_scaled), 0, stroke_points.size() - 2)
			at = stroke_points[stroke_index].lerp(
				stroke_points[stroke_index + 1], stroke_scaled - float(stroke_index))
			pressing = cycle >= 0.25 and cycle <= 2.18
		"farm_lob":
			var pull_target := _farm_demo_pull_point()
			var pull_travel := clampf(cycle / 1.15, 0.0, 1.0)
			pull_travel = pull_travel * pull_travel * (3.0 - 2.0 * pull_travel)
			at = _farm_anchor_point().lerp(pull_target, pull_travel)
			pressing = cycle <= 1.25
		"boxer_rhythm":
			if boxer_duck_pending:
				var duck_start := Vector2(center.x, size.y * 0.22)
				var duck_end := Vector2(center.x, size.y * 0.82)
				var duck_travel := clampf(cycle / 1.55, 0.0, 1.0)
				duck_travel = duck_travel * duck_travel * (3.0 - 2.0 * duck_travel)
				at = duck_start.lerp(duck_end, duck_travel)
				pressing = cycle <= 1.68
			else:
				var mitt_target := _boxer_mitt_rect(boxer_expected).get_center()
				at = Vector2(center.x, size.y * 0.92).lerp(
					mitt_target, clampf(cycle / 0.95, 0.0, 1.0))
				pressing = cycle >= 0.95
		"clue_board":
			var clue_target := _clue_target_rect(clue_index).get_center()
			var clue_travel := clampf(cycle / 1.6, 0.0, 1.0)
			clue_travel = clue_travel * clue_travel * (3.0 - 2.0 * clue_travel)
			at = _clue_home_point().lerp(clue_target, clue_travel)
			pressing = cycle <= 1.72
		"crown_chest":
			at = center.lerp(_crown_handle_rect().get_center(),
				clampf(cycle / 1.0, 0.0, 1.0))
			pressing = cycle >= 1.0
		"garden_plant":
			var hole := _garden_hole_point(garden_planted)
			var seed_travel := clampf(cycle / 1.55, 0.0, 1.0)
			seed_travel = seed_travel * seed_travel * (3.0 - 2.0 * seed_travel)
			at = _garden_seed_home().lerp(hole, seed_travel)
			pressing = cycle <= 1.68
		"magic_cabinet":
			var handle := _cabinet_handle_rect().get_center()
			var pull := clampf(cycle / 1.65, 0.0, 1.0)
			pull = pull * pull * (3.0 - 2.0 * pull)
			at = handle + Vector2.DOWN * _cabinet_required_travel() * pull
			pressing = cycle <= 1.78
		"echo":
			var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
			if echo_listening and not verse.is_empty():
				# Her turn: approach and tap the next actual singing star.
				var next_note := int(verse[clampi(echo_input_i, 0, verse.size() - 1)])
				var target := _echo_star_center(next_note)
				at = Vector2(center.x, size.y * 0.84).lerp(target,
					clampf(cycle / 1.0, 0.0, 1.0))
				pressing = cycle >= 1.0
			else:
				# During the song the hand waits below the lit star; no press ring
				# invites an eager tap before the call-and-response turn begins.
				var watch_x := center.x
				if echo_show_i >= 0 and echo_show_i < verse.size():
					watch_x = _echo_star_center(int(verse[echo_show_i])).x
				at = center.lerp(Vector2(watch_x, size.y * 0.84),
					clampf(cycle / 0.8, 0.0, 1.0))
				pressing = false
	return {"at": at, "pressing": pressing}


func _draw_demo_finger() -> void:
	var pose := _demo_finger_pose()
	var at: Vector2 = pose.get("at", size * 0.5)
	var pressing := bool(pose.get("pressing", false))
	var halo := 30.0 if pressing else 20.0
	draw_circle(at, halo, Color(0.22, 0.14, 0.52, 0.18))
	draw_circle(at, 14.5, Color("#382485"))
	draw_circle(at, 12.0, Color(1.0, 0.98, 0.86, 0.98))
	if pressing:
		var ring := 18.0 + fmod(demo_t * 46.0, 26.0)
		draw_arc(at, ring, 0.0, TAU, 24, Color(1.0, 0.95, 0.6, 0.6), 4.0)


func _xray_home_point() -> Vector2:
	return Vector2(size.x * 0.27, size.y * 0.74)


func _xray_target_center(index: int) -> Vector2:
	var spot_index := clampi(index, 0, XRAY_SPOTS.size() - 1)
	return size * XRAY_SPOTS[spot_index]


func _xray_scanner_radius() -> float:
	return maxf(38.0, minf(size.x, size.y) * 0.17)


func _xray_segment_hits(from: Vector2, to: Vector2, target: Vector2, radius: float) -> bool:
	var segment := to - from
	if segment.length_squared() <= 0.001:
		return false
	var along := clampf((target - from).dot(segment) / segment.length_squared(), 0.0, 1.0)
	return target.distance_to(from + segment * along) <= radius


func _xray_press(at: Vector2) -> void:
	if xray_complete or completion_accepted:
		return
	xray_dragging = true
	xray_scanner_pos = at.clamp(Vector2.ZERO, size)
	queue_redraw()


func _xray_drag(at: Vector2) -> void:
	if not xray_dragging or xray_complete or completion_accepted:
		return
	xray_scanner_pos = at.clamp(Vector2.ZERO, size)
	var travel := at.distance_to(previous_pos)
	if travel < 3.0 or xray_found_count >= XRAY_SPOTS.size():
		queue_redraw()
		return
	var target_index := xray_found_count
	var target := _xray_target_center(target_index)
	if not _xray_segment_hits(previous_pos, at, target, _xray_scanner_radius() * 0.72):
		queue_redraw()
		return
	xray_found[target_index] = true
	xray_found_count += 1
	xray_glow = 0.48
	feedback_anchor = target
	feedback_positive = true
	feedback_t = 0.30
	xray_complete = xray_found_count >= XRAY_SPOTS.size()
	gesture.emit("xray_scan", 1.0, 1.0)
	if not xray_complete:
		# Bank the diagnosis and quietly demonstrate the next sore spot. The
		# child may keep the same finger down or lift and follow the replay.
		demo_active = true
		demo_t = 0.0
	queue_redraw()


func _xray_release() -> void:
	xray_dragging = false
	if not xray_complete and not completion_accepted:
		demo_active = true
		demo_t = 0.0
	queue_redraw()


func _xray_tick(delta: float) -> void:
	xray_glow = maxf(0.0, xray_glow - delta)
	xray_redraw += delta
	if xray_redraw >= 0.05:
		xray_redraw = 0.0
		queue_redraw()


func _draw_xray_scan() -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(Vector2.ZERO, size), Color("#dff4f5"), true)
	var scan_at := xray_scanner_pos
	if demo_active and not xray_complete:
		scan_at = _demo_finger_pose().get("at", scan_at) as Vector2
	var radius := _xray_scanner_radius()
	for index in range(XRAY_SPOTS.size()):
		var target := _xray_target_center(index)
		if xray_found[index]:
			draw_circle(target, 13.0, Color(1.0, 0.91, 0.46, 0.88))
			draw_arc(target, 21.0, 0.0, TAU, 28, Color("#382485"), 4.0)
		elif index == xray_found_count:
			var nearness := clampf(1.0 - scan_at.distance_to(target) / (radius * 1.45), 0.0, 1.0)
			if nearness > 0.0:
				draw_circle(target, 7.0 + nearness * 10.0,
					Color(1.0, 0.91, 0.46, 0.20 + nearness * 0.58))
				draw_arc(target, 18.0 + nearness * 8.0, 0.0, TAU, 28,
					Color(0.40, 0.94, 0.95, 0.28 + nearness * 0.62), 4.0)
	# A square scan plate and moving beam distinguish this control from the
	# detective's round handled magnifying glass.
	var scan_rect := Rect2(scan_at - Vector2.ONE * radius, Vector2.ONE * radius * 2.0)
	draw_rect(scan_rect, Color(0.30, 0.90, 0.93, 0.14), true)
	draw_rect(scan_rect, Color(0.24, 0.76, 0.82, 0.90), false, 5.0)
	var beam_y := lerpf(scan_rect.position.y + 7.0, scan_rect.end.y - 7.0,
		0.5 + 0.5 * sin(demo_t * 4.2 + xray_glow * 8.0))
	draw_line(Vector2(scan_rect.position.x + 7.0, beam_y),
		Vector2(scan_rect.end.x - 7.0, beam_y), Color(0.84, 1.0, 1.0, 0.88), 4.0)
	for found_index in range(XRAY_SPOTS.size()):
		var dot := Vector2(size.x * 0.5 + (float(found_index) - 0.5) * 30.0, size.y * 0.075)
		draw_circle(dot, 7.0, Color("#ffd75e") if xray_found[found_index]
			else Color(0.30, 0.26, 0.42, 0.30))
	if xray_complete:
		draw_rect(Rect2(Vector2(8.0, 8.0), size - Vector2(16.0, 16.0)),
			Color(1.0, 0.86, 0.32, 0.72), false, 8.0)


func _dance_restart_show(delay: float = 0.32, preserve_prefix := false) -> void:
	dance_show_start = dance_input_index if preserve_prefix else 0
	dance_show_index = dance_show_start - 1
	dance_show_t = delay
	if not preserve_prefix:
		dance_input_index = 0
	dance_listening = false
	dance_last_pad = -1
	dance_glow = 0.0


func _dance_tick(delta: float) -> void:
	dance_glow = maxf(0.0, dance_glow - delta)
	if not dance_complete and not dance_listening:
		dance_show_t -= delta
		if dance_show_t <= 0.0:
			dance_show_index += 1
			if dance_show_index >= DANCE_SEQUENCE.size():
				dance_show_index = -1
				dance_listening = true
				dance_input_index = dance_show_start
			else:
				dance_last_pad = int(DANCE_SEQUENCE[dance_show_index])
				dance_glow = DANCE_SHOW_STEP * 0.78
				dance_show_t = DANCE_SHOW_STEP
	dance_redraw += delta
	if dance_redraw >= 0.05:
		dance_redraw = 0.0
		queue_redraw()


func _dance_pad_rect(pad: int) -> Rect2:
	var area := Rect2(size.x * 0.08, size.y * 0.15, size.x * 0.84, size.y * 0.72)
	var gap := maxf(8.0, minf(size.x, size.y) * 0.035)
	var cell_size := Vector2((area.size.x - gap) * 0.5, (area.size.y - gap) * 0.5)
	var col := pad % 2
	var row := floori(float(pad) / 2.0)
	return Rect2(
		area.position + Vector2(float(col) * (cell_size.x + gap), float(row) * (cell_size.y + gap)),
		cell_size
	)


func _dance_pad_color(pad: int) -> Color:
	match pad:
		0:
			return Color("#ef7d83")
		1:
			return Color("#62c9c4")
		2:
			return Color("#a77ad8")
		_:
			return Color("#f2bd58")


func _dance_press(at: Vector2) -> void:
	if dance_complete or completion_accepted:
		return
	var pressed_pad := -1
	for pad in range(4):
		if _dance_pad_rect(pad).grow(7.0).has_point(at):
			pressed_pad = pad
			break
	if pressed_pad < 0:
		return
	feedback_anchor = _dance_pad_rect(pressed_pad).get_center()
	if not dance_listening:
		# Eager taps during Roshan's call make that pad shimmer, but cannot
		# skip the phrase or accidentally bank progress.
		dance_last_pad = pressed_pad
		dance_glow = 0.24
		feedback_positive = true
		feedback_t = 0.20
		return
	var expected := int(DANCE_SEQUENCE[dance_input_index])
	if pressed_pad != expected:
		feedback_positive = false
		feedback_t = 0.28
		gesture.emit("dance_sequence", 0.0, 0.4)
		# Keep every correct step already danced. Replay only the remaining
		# suffix, then resume at the same next-required pad.
		_dance_restart_show(0.42, true)
		demo_active = true
		demo_t = 0.0
		return
	dance_last_pad = pressed_pad
	dance_glow = 0.34
	dance_input_index += 1
	feedback_positive = true
	feedback_t = 0.24
	if dance_input_index >= DANCE_SEQUENCE.size():
		dance_complete = true
		dance_listening = false
		gesture.emit("dance_sequence", 1.0, 1.0)


func _draw_dance_capsule(rect: Rect2, color: Color, lit: bool) -> void:
	var radius := rect.size.y * 0.5
	var outline := Color("#382485")
	var body := color.lightened(0.16) if lit else color.darkened(0.08)
	draw_rect(Rect2(rect.position + Vector2(radius, 0.0),
		Vector2(maxf(1.0, rect.size.x - radius * 2.0), rect.size.y)), outline, true)
	draw_circle(Vector2(rect.position.x + radius, rect.get_center().y), radius, outline)
	draw_circle(Vector2(rect.end.x - radius, rect.get_center().y), radius, outline)
	var inner := rect.grow(-5.0)
	var inner_radius := inner.size.y * 0.5
	draw_rect(Rect2(inner.position + Vector2(inner_radius, 0.0),
		Vector2(maxf(1.0, inner.size.x - inner_radius * 2.0), inner.size.y)), body, true)
	draw_circle(Vector2(inner.position.x + inner_radius, inner.get_center().y), inner_radius, body)
	draw_circle(Vector2(inner.end.x - inner_radius, inner.get_center().y), inner_radius, body)
	draw_circle(inner.get_center(), 11.0 if lit else 7.0, Color(1.0, 0.97, 0.78, 0.92))


func _draw_dance_sequence() -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	var pad_area := Rect2(size.x * 0.055, size.y * 0.10, size.x * 0.89, size.y * 0.82)
	# The approved ballerina card currently has three pads. This soft stage
	# inset keeps its context visible while four large hit shapes supply the
	# requested call-and-response grammar without fabricating replacement art.
	draw_rect(pad_area, Color(0.95, 0.97, 1.0, 0.86), true)
	draw_rect(pad_area, Color("#382485"), false, 3.0)
	for pad in range(4):
		var lit := (pad == dance_last_pad and dance_glow > 0.0) or dance_complete
		_draw_dance_capsule(_dance_pad_rect(pad), _dance_pad_color(pad), lit)
		if lit:
			draw_arc(_dance_pad_rect(pad).get_center(), _dance_pad_rect(pad).size.y * 0.55,
				0.0, TAU, 28, Color(1.0, 0.91, 0.45, 0.72), 5.0)
	for step in range(DANCE_SEQUENCE.size()):
		var step_center := Vector2(
			size.x * 0.5 + (float(step) - 1.5) * maxf(18.0, size.x * 0.045),
			size.y * 0.075)
		var step_done := step < dance_input_index or dance_complete
		draw_circle(step_center, 7.0, _dance_pad_color(int(DANCE_SEQUENCE[step]))
			if step_done else Color(0.32, 0.30, 0.48, 0.38))
	if dance_complete:
		draw_arc(size * 0.5, minf(size.x, size.y) * 0.45, 0.0, TAU, 48,
			Color(1.0, 0.88, 0.35, 0.62), 8.0)


func _candy_spawn_point() -> Vector2:
	return Vector2(size.x * 0.10, size.y * 0.24)


func _candy_piece_radius() -> float:
	return maxf(22.0, minf(size.x, size.y) * 0.085)


func _candy_piece_rect() -> Rect2:
	var radius := _candy_piece_radius()
	return Rect2(candy_position - Vector2.ONE * radius, Vector2.ONE * radius * 2.0)


func _candy_bin_rect(bin: int) -> Rect2:
	var width := size.x * 0.22
	var center_x := size.x * (0.20 + 0.30 * float(clampi(bin, 0, 2)))
	return Rect2(center_x - width * 0.5, size.y * 0.63, width, size.y * 0.27)


func _candy_reset_piece(advance: bool) -> void:
	if advance:
		candy_piece_index = posmod(candy_piece_index + 1, CANDY_SEQUENCE.size())
	candy_type = int(CANDY_SEQUENCE[candy_piece_index])
	candy_position = _candy_spawn_point()
	candy_drag_offset = Vector2.ZERO
	candy_dragging = false


func _candy_tick(delta: float) -> void:
	candy_glow = maxf(0.0, candy_glow - delta)
	if not candy_complete and not candy_dragging:
		candy_position.x += maxf(24.0, size.x * 0.08) * delta
		if candy_position.x > size.x * 0.91:
			candy_loops += 1
			candy_position = _candy_spawn_point()
	candy_redraw += delta
	if candy_redraw >= 0.05:
		candy_redraw = 0.0
		queue_redraw()


func _candy_press(at: Vector2) -> void:
	if candy_complete or completion_accepted:
		return
	if _candy_piece_rect().grow(20.0).has_point(at):
		candy_dragging = true
		candy_drag_offset = candy_position - at


func _candy_drag(at: Vector2) -> void:
	if not candy_dragging or candy_complete:
		return
	var radius := _candy_piece_radius()
	var desired := at + candy_drag_offset
	candy_position = Vector2(
		clampf(desired.x, radius, maxf(radius, size.x - radius)),
		clampf(desired.y, radius, maxf(radius, size.y - radius)))
	queue_redraw()


func _candy_release(at: Vector2) -> void:
	if not candy_dragging:
		return
	candy_dragging = false
	var bin := -1
	for candidate in range(3):
		if _candy_bin_rect(candidate).grow(8.0).has_point(at):
			bin = candidate
			break
	if bin == candy_type:
		candy_sorted += 1
		candy_last_bin = bin
		candy_glow = 0.42
		feedback_anchor = _candy_bin_rect(bin).get_center()
		feedback_positive = true
		feedback_t = 0.28
		gesture.emit("candy_sort", 1.0, 1.0)
		if candy_sorted >= CANDY_SEQUENCE.size():
			candy_complete = true
			candy_position = _candy_bin_rect(bin).get_center()
		else:
			_candy_reset_piece(true)
	else:
		# The same piece returns to the start. Nothing is lost and the hand
		# quietly demonstrates its matching silhouette again.
		if bin >= 0:
			feedback_anchor = _candy_bin_rect(bin).get_center()
			feedback_positive = false
			feedback_t = 0.28
			gesture.emit("candy_sort", 0.0, 0.4)
		_candy_reset_piece(false)
		demo_active = true
		demo_t = 0.0
	queue_redraw()


func _candy_color(kind: int) -> Color:
	match kind:
		0:
			return Color("#ef776f")
		1:
			return Color("#57c4c2")
		_:
			return Color("#ae64bd")


func _draw_candy_shape(center: Vector2, kind: int, radius: float, color: Color) -> void:
	match kind:
		0:
			for petal in range(6):
				var angle := TAU * float(petal) / 6.0
				draw_circle(center + Vector2.from_angle(angle) * radius * 0.48,
					radius * 0.43, color)
			draw_circle(center, radius * 0.50, color.lightened(0.12))
		1:
			var shell_points := PackedVector2Array([center + Vector2(0.0, radius * 0.78)])
			for point in range(7):
				var angle := lerpf(PI * 1.12, PI * 1.88, float(point) / 6.0)
				shell_points.append(center + Vector2.from_angle(angle) * radius)
			draw_colored_polygon(shell_points, color)
			for rib in range(1, 6):
				var rib_angle := lerpf(PI * 1.18, PI * 1.82, float(rib) / 6.0)
				draw_line(center + Vector2(0.0, radius * 0.70),
					center + Vector2.from_angle(rib_angle) * radius * 0.82,
					color.lightened(0.28), 2.5)
		_:
			var left := center + Vector2(-radius * 0.45, 0.0)
			var right := center + Vector2(radius * 0.45, 0.0)
			draw_circle(left, radius * 0.57, color)
			draw_circle(right, radius * 0.57, color)
			draw_colored_polygon(PackedVector2Array([
				center, center + Vector2(-radius, -radius * 0.72),
				center + Vector2(-radius, radius * 0.72),
			]), color)
			draw_colored_polygon(PackedVector2Array([
				center, center + Vector2(radius, -radius * 0.72),
				center + Vector2(radius, radius * 0.72),
			]), color)
			draw_circle(center, radius * 0.35, color.lightened(0.18))


func _draw_candy_sort() -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(Vector2.ZERO, size), Color("#f7eafa"), true)
	# A slow belt gives every piece unlimited chances; crossing the right edge
	# loops it with no penalty and no queue advance.
	var belt_y := size.y * 0.24
	draw_line(Vector2(size.x * 0.07, belt_y + _candy_piece_radius() + 9.0),
		Vector2(size.x * 0.93, belt_y + _candy_piece_radius() + 9.0),
		Color(0.30, 0.24, 0.48, 0.42), 7.0)
	for bin in range(3):
		var bin_rect := _candy_bin_rect(bin)
		var lit := bin == candy_last_bin and candy_glow > 0.0
		draw_rect(bin_rect, Color(_candy_color(bin), 0.16 if not lit else 0.32), true)
		draw_rect(bin_rect, Color("#382485") if not lit else Color("#ffd75e"),
			false, 4.0 if not lit else 7.0)
		var silhouette_center := bin_rect.get_center()
		var silhouette_radius := minf(bin_rect.size.x, bin_rect.size.y) * 0.24
		_draw_candy_shape(silhouette_center, bin, silhouette_radius * 1.18,
			Color(0.18, 0.16, 0.29, 0.28))
		_draw_candy_shape(silhouette_center, bin, silhouette_radius,
			Color(_candy_color(bin), 0.78))
	if not candy_complete or completion_accepted:
		_draw_candy_shape(candy_position + Vector2(3.0, 5.0), candy_type,
			_candy_piece_radius() * 1.04, Color(0.18, 0.12, 0.28, 0.28))
		_draw_candy_shape(candy_position, candy_type, _candy_piece_radius(),
			_candy_color(candy_type))
	for sorted_index in range(CANDY_SEQUENCE.size()):
		var dot := Vector2(size.x * 0.5 + (float(sorted_index) - 2.5) * maxf(14.0, size.x * 0.035),
			size.y * 0.075)
		draw_circle(dot, 6.0, _candy_color(int(CANDY_SEQUENCE[sorted_index]))
			if sorted_index < candy_sorted else Color(0.30, 0.26, 0.42, 0.32))


func _paint_canvas_rect() -> Rect2:
	var side := minf(size.x * 0.46, size.y * 0.72)
	return Rect2(size * 0.5 - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _paint_required_cells() -> int:
	return ceili(float(PAINT_GRID_COLS * PAINT_GRID_ROWS) * PAINT_REQUIRED_COVERAGE)


func paint_coverage() -> float:
	return float(paint_covered) / float(PAINT_GRID_COLS * PAINT_GRID_ROWS)


func _paint_press(at: Vector2) -> void:
	paint_dragging = not paint_complete and not completion_accepted and _paint_canvas_rect().has_point(at)
	paint_last_point = at


func _paint_mark_at(at: Vector2) -> int:
	var canvas := _paint_canvas_rect()
	if not canvas.has_point(at):
		return 0
	var local := (at - canvas.position) / canvas.size
	var col := clampi(floori(local.x * float(PAINT_GRID_COLS)), 0, PAINT_GRID_COLS - 1)
	var row := clampi(floori(local.y * float(PAINT_GRID_ROWS)), 0, PAINT_GRID_ROWS - 1)
	var added := 0
	# A cross-shaped, one-cell brush is forgiving on a small phone without
	# allowing a stationary press to flood the whole canvas.
	for dy in range(-1, 2):
		for dx in range(-1, 2):
			if absi(dx) + absi(dy) > 1:
				continue
			var brush_col := col + dx
			var brush_row := row + dy
			if brush_col < 0 or brush_col >= PAINT_GRID_COLS \
					or brush_row < 0 or brush_row >= PAINT_GRID_ROWS:
				continue
			var cell := brush_row * PAINT_GRID_COLS + brush_col
			if not paint_cells[cell]:
				paint_cells[cell] = true
				paint_covered += 1
				added += 1
	return added


func _paint_drag(at: Vector2) -> void:
	if not paint_dragging or paint_complete:
		return
	var distance := at.distance_to(paint_last_point)
	if distance < 2.0:
		return
	var canvas := _paint_canvas_rect()
	var cell_size := Vector2(
		canvas.size.x / float(PAINT_GRID_COLS),
		canvas.size.y / float(PAINT_GRID_ROWS))
	var spacing := maxf(3.0, minf(cell_size.x, cell_size.y) * 0.45)
	var steps := maxi(1, ceili(distance / spacing))
	var added := 0
	for step in range(1, steps + 1):
		added += _paint_mark_at(paint_last_point.lerp(at, float(step) / float(steps)))
	paint_last_point = at
	if added <= 0:
		return
	feedback_anchor = at
	feedback_positive = true
	feedback_t = 0.18
	if not paint_complete and paint_covered >= _paint_required_cells():
		paint_complete = true
		paint_dragging = false
		gesture.emit("paint_reveal", 1.0, 1.0)
	queue_redraw()


func _paint_release() -> void:
	paint_dragging = false


func _draw_paint_reveal() -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(Vector2.ZERO, size), Color("#eee9df"), true)
	var canvas := _paint_canvas_rect()
	draw_rect(canvas.grow(7.0), Color("#8b633d"), true)
	if paint_reveal_texture != null:
		draw_texture_rect(paint_reveal_texture, canvas, false)
	elif widget_overlay != null:
		draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
	else:
		draw_rect(canvas, Color("#f3d5a0"), true)
	var cell_size := Vector2(
		canvas.size.x / float(PAINT_GRID_COLS),
		canvas.size.y / float(PAINT_GRID_ROWS))
	if not paint_complete:
		for row in range(PAINT_GRID_ROWS):
			for col in range(PAINT_GRID_COLS):
				var cell := row * PAINT_GRID_COLS + col
				if paint_cells[cell]:
					continue
				var veil := Rect2(canvas.position + Vector2(float(col), float(row)) * cell_size,
					cell_size).grow(0.35)
				draw_rect(veil, Color("#eee7dc"), true)
	draw_rect(canvas.grow(7.0), Color("#382485") if not paint_complete else Color("#ffd75e"),
		false, 5.0 if not paint_complete else 8.0)
	for marker in range(8):
		var marker_center := Vector2(
			size.x * 0.5 + (float(marker) - 3.5) * maxf(13.0, size.x * 0.028),
			size.y * 0.93)
		var marker_filled := paint_covered >= ceili(
			float(marker + 1) / 8.0 * float(_paint_required_cells()))
		draw_circle(marker_center, 5.5,
			Color("#ffd75e") if marker_filled else Color(0.30, 0.26, 0.42, 0.30))
	if paint_complete:
		for sparkle in range(6):
			var angle := TAU * float(sparkle) / 6.0
			var sparkle_at := canvas.get_center() + Vector2.from_angle(angle) * canvas.size.x * 0.62
			draw_circle(sparkle_at, 7.0, Color(1.0, 0.88, 0.35, 0.72))


func _farm_anchor_point() -> Vector2:
	# This sits on the vegetable basket in widget_target_farmer.
	return Vector2(size.x * 0.42, size.y * 0.69)


func _farm_target_center() -> Vector2:
	# One large forgiving target, centered on the right-hand feeding piggy.
	return Vector2(size.x * 0.67, size.y * 0.38)


func _farm_target_radius() -> float:
	return maxf(44.0, minf(size.x, size.y) * 0.19)


func _farm_piece_radius() -> float:
	return maxf(21.0, minf(size.x, size.y) * 0.075)


func _farm_piece_rect() -> Rect2:
	var radius := _farm_piece_radius()
	return Rect2(farm_piece_position - Vector2.ONE * radius,
		Vector2.ONE * radius * 2.0)


func _farm_demo_pull_point() -> Vector2:
	var launch_direction := (_farm_target_center() - _farm_anchor_point()).normalized()
	return _farm_anchor_point() - launch_direction * minf(size.x, size.y) * 0.30


func _farm_reset_piece() -> void:
	farm_food_index = farm_landed % maxi(1, farm_vegetable_textures.size())
	farm_piece_position = _farm_anchor_point()
	farm_drag_offset = Vector2.ZERO
	farm_dragging = false
	farm_flying = false
	farm_will_land = false
	farm_flight_t = 0.0
	farm_flight_start = farm_piece_position
	farm_flight_end = farm_piece_position


func _farm_press(at: Vector2) -> void:
	if farm_complete or farm_flying or farm_pause > 0.0 or completion_accepted:
		return
	if _farm_piece_rect().grow(22.0).has_point(at):
		farm_dragging = true
		farm_drag_offset = farm_piece_position - at


func _farm_drag(at: Vector2) -> void:
	if not farm_dragging or farm_flying or farm_complete:
		return
	var radius := _farm_piece_radius()
	var desired := at + farm_drag_offset
	farm_piece_position = Vector2(
		clampf(desired.x, radius, maxf(radius, size.x - radius)),
		clampf(desired.y, radius, maxf(radius, size.y - radius)))
	queue_redraw()


func _farm_release(_at: Vector2) -> void:
	if not farm_dragging:
		return
	farm_dragging = false
	var anchor := _farm_anchor_point()
	var launch := anchor - farm_piece_position
	var target_direction := (_farm_target_center() - anchor).normalized()
	var enough_pull := launch.length() >= minf(size.x, size.y) * 0.11
	var alignment := launch.normalized().dot(target_direction) if launch.length_squared() > 1.0 else 0.0
	farm_will_land = enough_pull and alignment >= 0.55
	farm_flight_start = farm_piece_position
	farm_flight_end = _farm_target_center() if farm_will_land else anchor
	farm_flight_t = 0.0
	farm_flying = true
	queue_redraw()


func _farm_arc_point(start: Vector2, finish: Vector2, progress: float, height: float) -> Vector2:
	var t := clampf(progress, 0.0, 1.0)
	return start.lerp(finish, t) + Vector2.UP * sin(t * PI) * height


func _farm_tick(delta: float) -> void:
	farm_land_glow = maxf(0.0, farm_land_glow - delta)
	farm_munch_t = maxf(0.0, farm_munch_t - delta)
	if farm_pause > 0.0:
		farm_pause = maxf(0.0, farm_pause - delta)
		if farm_pause <= 0.0 and not farm_complete:
			_farm_reset_piece()
	if farm_flying:
		farm_flight_t = minf(1.0, farm_flight_t + delta / FARM_FLIGHT_DURATION)
		var arc_height := minf(size.x, size.y) * (0.28 if farm_will_land else 0.16)
		farm_piece_position = _farm_arc_point(
			farm_flight_start, farm_flight_end, farm_flight_t, arc_height)
		if farm_flight_t >= 1.0:
			farm_flying = false
			if farm_will_land:
				farm_last_landed_food = farm_food_index
				farm_landed += 1
				farm_land_glow = 0.48
				farm_munch_t = 0.58
				feedback_anchor = _farm_target_center()
				feedback_positive = true
				feedback_t = 0.30
				gesture.emit("farm_lob", 1.0, 1.0)
				if farm_landed >= FARM_LOB_GOAL:
					farm_complete = true
				else:
					farm_pause = 0.42
			else:
				# The miss completes its visible loop back into the basket. It
				# neither emits progress nor consumes a vegetable.
				farm_loops += 1
				farm_pause = 0.18
				demo_active = true
				demo_t = 0.0
	farm_redraw += delta
	if farm_redraw >= 0.04:
		farm_redraw = 0.0
		queue_redraw()


func _draw_farm_arc_guide(start: Vector2, finish: Vector2, height: float, color: Color) -> void:
	for guide_step in range(1, 12):
		var t := float(guide_step) / 12.0
		draw_circle(_farm_arc_point(start, finish, t, height),
			3.5 if guide_step % 2 == 0 else 2.2, color)


func _draw_farm_vegetable() -> void:
	var radius := _farm_piece_radius()
	var food_texture: Texture2D = null
	if not farm_vegetable_textures.is_empty():
		food_texture = farm_vegetable_textures[
			farm_food_index % farm_vegetable_textures.size()]
	elif farm_vegetable_texture != null:
		food_texture = farm_vegetable_texture
	if food_texture != null:
		draw_texture_rect(food_texture,
			Rect2(farm_piece_position - Vector2.ONE * radius * 1.30,
				Vector2.ONE * radius * 2.60), false)
		return
	# Texture-safe fallback remains an abstract draggable control token; it
	# does not invent replacement farmer art.
	draw_circle(farm_piece_position + Vector2(3.0, 5.0), radius,
		Color(0.20, 0.12, 0.28, 0.24))
	draw_circle(farm_piece_position, radius, Color("#ef9b45"))
	draw_arc(farm_piece_position, radius * 0.72, 0.0, TAU, 24,
		Color("#fff0b0"), 4.0)


func _draw_farm_munch_reaction() -> void:
	if farm_munch_t <= 0.0:
		return
	var amount := clampf(1.0 - farm_munch_t / 0.58, 0.0, 1.0)
	var squash := sin(amount * PI * 2.0) * 0.08
	var target := _farm_target_center()
	var face_side := _farm_target_radius() * 1.18
	draw_set_transform(target, 0.0, Vector2(1.0 + squash, 1.0 - squash))
	draw_circle(Vector2.ZERO, face_side * 0.36, Color("#efa89c"))
	draw_circle(Vector2(-face_side * 0.13, -face_side * 0.08),
		face_side * 0.035, Color("#50344f"))
	draw_circle(Vector2(face_side * 0.13, -face_side * 0.08),
		face_side * 0.035, Color("#50344f"))
	draw_set_transform(Vector2.ZERO)
	var chew_open := 0.5 + 0.5 * sin(amount * TAU * 2.0)
	draw_set_transform(target + Vector2(0.0, face_side * 0.10), 0.0,
		Vector2(1.0, 0.45 + chew_open * 0.55))
	draw_circle(Vector2.ZERO, face_side * 0.12, Color("#714257"))
	draw_circle(Vector2.ZERO, face_side * 0.065, Color("#f4c0b2"))
	draw_set_transform(Vector2.ZERO)
	for crumb_index in range(3):
		var crumb_angle := -1.1 + float(crumb_index) * 0.42
		draw_circle(target + Vector2.from_angle(crumb_angle) \
			* face_side * (0.34 + amount * 0.14), 3.0 + float(crumb_index),
			Color("#f3c25f"))


func _draw_farm_lob() -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(Vector2.ZERO, size), Color("#edf2cf"), true)
	var anchor := _farm_anchor_point()
	var target := _farm_target_center()
	var target_radius := _farm_target_radius()
	var target_pulse := 1.0 + (0.08 * sin(farm_land_glow * 30.0) if farm_land_glow > 0.0 else 0.0)
	draw_circle(target, target_radius * target_pulse, Color(1.0, 0.88, 0.45, 0.18))
	draw_arc(target, target_radius * target_pulse, 0.0, TAU, 40,
		Color("#ffd75e") if farm_land_glow > 0.0 else Color("#6e4c78"),
		8.0 if farm_land_glow > 0.0 else 5.0)
	# Basket anchor and backward-pull cue. The authored basket remains visible
	# beneath these translucent control rings.
	draw_circle(anchor, _farm_piece_radius() * 1.34, Color(0.35, 0.24, 0.24, 0.16))
	draw_arc(anchor, _farm_piece_radius() * 1.34, 0.0, TAU, 30,
		Color("#8b633d"), 4.0)
	if farm_dragging:
		draw_line(anchor, farm_piece_position, Color(0.25, 0.18, 0.36, 0.50), 5.0)
		var launch := anchor - farm_piece_position
		var target_direction := (target - anchor).normalized()
		var valid := launch.length() >= minf(size.x, size.y) * 0.11 \
			and launch.normalized().dot(target_direction) >= 0.55
		_draw_farm_arc_guide(farm_piece_position, target if valid else anchor,
			minf(size.x, size.y) * (0.28 if valid else 0.16),
			Color(1.0, 0.83, 0.32, 0.78) if valid else Color(0.55, 0.45, 0.65, 0.42))
	elif not farm_flying and farm_pause <= 0.0 and not farm_complete:
		var pull := _farm_demo_pull_point()
		draw_line(anchor, pull, Color(0.32, 0.24, 0.45, 0.28), 4.0)
		var direction := (pull - anchor).normalized()
		var side := direction.orthogonal()
		draw_colored_polygon(PackedVector2Array([
			pull + side * 10.0, pull + direction * 15.0, pull - side * 10.0,
		]), Color(0.32, 0.24, 0.45, 0.42))
	_draw_farm_vegetable()
	_draw_farm_munch_reaction()
	for landing in range(FARM_LOB_GOAL):
		var dot := Vector2(size.x * 0.5 + (float(landing) - 1.5) * maxf(18.0, size.x * 0.05),
			size.y * 0.075)
		draw_circle(dot, 7.0,
			Color("#ffd75e") if landing < farm_landed else Color(0.30, 0.26, 0.42, 0.30))
	if farm_complete:
		draw_arc(target, target_radius * 1.26, 0.0, TAU, 44,
			Color(1.0, 0.88, 0.35, 0.65), 8.0)


func _boxer_mitt_rect(side: int) -> Rect2:
	var area := Rect2(size.x * 0.075, size.y * 0.18, size.x * 0.85, size.y * 0.67)
	var gap := maxf(12.0, size.x * 0.045)
	var width := (area.size.x - gap) * 0.5
	return Rect2(area.position + Vector2(float(clampi(side, 0, 1)) * (width + gap), 0.0),
		Vector2(width, area.size.y))


func _boxer_tick(delta: float) -> void:
	boxer_flash = maxf(0.0, boxer_flash - delta)
	boxer_hit_glow = maxf(0.0, boxer_hit_glow - delta)
	boxer_redraw += delta
	if boxer_redraw >= 0.05:
		boxer_redraw = 0.0
		queue_redraw()


func _boxer_press(at: Vector2) -> void:
	if boxer_complete or completion_accepted:
		return
	if boxer_duck_pending:
		boxer_duck_distance = 0.0
		return
	var pressed_mitt := -1
	for side in range(2):
		if _boxer_mitt_rect(side).has_point(at):
			pressed_mitt = side
			break
	if pressed_mitt < 0:
		return
	feedback_anchor = _boxer_mitt_rect(pressed_mitt).get_center()
	if pressed_mitt != boxer_expected:
		feedback_positive = false
		feedback_t = 0.28
		boxer_flash = 1.2
		gesture.emit("boxer_rhythm", 0.0, 0.4)
		demo_active = true
		demo_t = 0.0
		return
	boxer_last_mitt = pressed_mitt
	boxer_hit_glow = 0.34
	boxer_hit_index += 1
	feedback_positive = true
	feedback_t = 0.24
	gesture.emit("boxer_rhythm", 1.0, 1.0)
	if boxer_hit_index >= BOXER_SEQUENCE.size():
		boxer_complete = true
		return
	boxer_expected = int(BOXER_SEQUENCE[boxer_hit_index])
	boxer_flash = 0.62
	if boxer_hit_index == BOXER_DUCK_AFTER and not boxer_duck_done:
		boxer_duck_pending = true
		boxer_duck_distance = 0.0
		demo_active = true
		demo_t = 0.0


func _boxer_drag(at: Vector2) -> void:
	if not boxer_duck_pending or boxer_complete:
		return
	var movement := at - previous_pos
	boxer_duck_distance += maxf(0.0, movement.y - absf(movement.x) * 0.35)
	if boxer_duck_distance >= maxf(52.0, minf(size.x, size.y) * 0.24):
		boxer_duck_pending = false
		boxer_duck_done = true
		boxer_flash = 1.2
		feedback_anchor = Vector2(size.x * 0.5, size.y * 0.72)
		feedback_positive = true
		feedback_t = 0.28
		demo_active = true
		demo_t = 0.0
	queue_redraw()


func _boxer_release() -> void:
	if boxer_duck_pending:
		# A short or sideways attempt simply replays the downward hand. The
		# three banked mitts remain banked and there is no timing reset.
		boxer_duck_distance = 0.0
		demo_active = true
		demo_t = 0.0


func _boxer_mitt_color(side: int) -> Color:
	return Color("#53bbb8") if side == 0 else Color("#ef7d75")


func _draw_boxer_mitt(rect: Rect2, side: int, highlighted: bool) -> void:
	var center := rect.get_center()
	var radius := minf(rect.size.x, rect.size.y) * 0.37
	var color := _boxer_mitt_color(side)
	var glow := highlighted or (side == boxer_last_mitt and boxer_hit_glow > 0.0) or boxer_complete
	draw_circle(center + Vector2(4.0, 7.0), radius * 1.06, Color(0.20, 0.12, 0.28, 0.24))
	draw_circle(center, radius, Color("#382485"))
	draw_circle(center, radius - 6.0, color.lightened(0.10) if glow else color.darkened(0.05))
	draw_circle(center, radius * 0.56, Color(0.98, 0.91, 0.75, 0.88))
	draw_arc(center, radius * 0.58, 0.0, TAU, 32, Color("#8b633d"), 4.0)
	var wrist := Rect2(center.x - radius * 0.46, center.y + radius * 0.68,
		radius * 0.92, radius * 0.46)
	draw_rect(wrist, color.darkened(0.16), true)
	draw_rect(wrist, Color("#382485"), false, 4.0)
	if highlighted:
		var pulse := 0.50 + 0.22 * sin(boxer_flash * 18.0)
		draw_arc(center, radius * 1.18, 0.0, TAU, 40,
			Color(1.0, 0.86, 0.30, pulse), 8.0)


func _draw_boxer_rhythm() -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(Vector2.ZERO, size), Color("#f3e6eb"), true)
	var mitt_panel := Rect2(size.x * 0.045, size.y * 0.12, size.x * 0.91, size.y * 0.78)
	draw_rect(mitt_panel, Color(0.96, 0.97, 1.0, 0.78), true)
	draw_rect(mitt_panel, Color("#382485"), false, 3.0)
	# The approved lane overlay's first square is the boxer focus-pad pair.
	# It remains visible as thematic art beneath the oversized touch geometry.
	if widget_mover != null:
		var texture_size := widget_mover.get_size()
		var source_side := minf(texture_size.x, texture_size.y)
		var art_side := minf(size.x * 0.44, size.y * 0.58)
		draw_texture_rect_region(widget_mover,
			Rect2(size * 0.5 - Vector2.ONE * art_side * 0.5, Vector2.ONE * art_side),
			Rect2(0.0, 0.0, source_side, source_side),
			Color(1.0, 1.0, 1.0, 0.40))
	for side in range(2):
		var highlighted := not boxer_duck_pending and not boxer_complete and side == boxer_expected
		_draw_boxer_mitt(_boxer_mitt_rect(side), side, highlighted)
	for hit in range(BOXER_SEQUENCE.size()):
		var sequence_center := Vector2(
			size.x * 0.5 + (float(hit) - 2.5) * maxf(14.0, size.x * 0.035),
			size.y * 0.068)
		var done := hit < boxer_hit_index
		draw_circle(sequence_center, 6.5,
			_boxer_mitt_color(int(BOXER_SEQUENCE[hit])) if done
			else Color(_boxer_mitt_color(int(BOXER_SEQUENCE[hit])), 0.28))
		if hit == boxer_hit_index and not boxer_complete:
			draw_arc(sequence_center, 10.5, 0.0, TAU, 20, Color("#ffd75e"), 3.0)
	if boxer_duck_pending:
		var duck_x := size.x * 0.5
		var duck_top := size.y * 0.20
		var duck_bottom := size.y * 0.79
		draw_rect(mitt_panel, Color(0.20, 0.16, 0.36, 0.38), true)
		draw_line(Vector2(duck_x, duck_top), Vector2(duck_x, duck_bottom - 22.0),
			Color("#ffd75e"), 16.0, true)
		draw_colored_polygon(PackedVector2Array([
			Vector2(duck_x - 35.0, duck_bottom - 34.0),
			Vector2(duck_x + 35.0, duck_bottom - 34.0),
			Vector2(duck_x, duck_bottom + 8.0),
		]), Color("#ffd75e"))
		# Fill the arrow from the child's real downward travel.
		var duck_progress := clampf(boxer_duck_distance /
			maxf(52.0, minf(size.x, size.y) * 0.24), 0.0, 1.0)
		draw_circle(Vector2(duck_x, lerpf(duck_top, duck_bottom, duck_progress)),
			18.0, Color(1.0, 0.95, 0.70, 0.72))
	if boxer_complete:
		draw_arc(size * 0.5, minf(size.x, size.y) * 0.43,
			0.0, TAU, 48, Color(1.0, 0.88, 0.35, 0.65), 8.0)


func _draw_imp(target: Dictionary) -> void:
	var pos: Vector2 = target.get("pos", Vector2.ZERO)
	var radius := float(target.get("r", 44.0))
	var captain := bool(target.get("captain", false))
	var texture := bop_captain_texture if captain else bop_texture
	if texture != null:
		var side := radius * 2.4
		draw_texture_rect(texture, Rect2(pos - Vector2(side, side) * 0.5, Vector2(side, side)), false)
		if captain:
			# plain gold band ring marks the captain over the costume sprite
			draw_arc(pos, radius * 1.16, 0.0, TAU, 36, Color("#e0b34c"), 6.0)
			if int(target.get("hp", 1)) > 1:
				draw_arc(pos, radius * 1.3, 0.0, TAU, 36, Color(1.0, 0.9, 0.5, 0.45), 4.0)
		return
	# basic place-in imp until the codex mischief-imp sprite set lands
	var body := Color("#7a4f9a") if not captain else Color("#5f3a85")
	var belly := Color("#b28ccd")
	draw_circle(pos, radius * 1.18, Color(1.0, 0.86, 0.4, 0.16))
	# curled striped horns
	for side_sign in [-1.0, 1.0]:
		var horn := pos + Vector2(side_sign * radius * 0.62, -radius * 0.78)
		draw_arc(horn, radius * 0.34, PI * 0.2, PI * 1.4, 12, Color("#e8d6a8"), 9.0)
		draw_arc(horn, radius * 0.34, PI * 0.5, PI * 1.1, 8, Color("#a8794f"), 9.0)
	# curled tail
	draw_arc(pos + Vector2(radius * 0.95, radius * 0.55), radius * 0.4, -PI * 0.6, PI * 0.7, 10, body.lightened(0.1), 8.0)
	draw_circle(pos, radius, body)
	draw_circle(pos + Vector2(0, radius * 0.3), radius * 0.55, belly)
	# amber eyes and a friendly fanged grin
	for side_sign in [-1.0, 1.0]:
		var eye := pos + Vector2(side_sign * radius * 0.34, -radius * 0.22)
		draw_circle(eye, radius * 0.17, Color("#f4b642"))
		draw_circle(eye, radius * 0.08, Color("#33203f"))
	draw_arc(pos + Vector2(0, radius * 0.1), radius * 0.34, 0.35, PI - 0.35, 12, Color("#33203f"), 5.0)
	for side_sign in [-1.0, 1.0]:
		var fang := pos + Vector2(side_sign * radius * 0.18, radius * 0.36)
		draw_colored_polygon(PackedVector2Array([
			fang + Vector2(-5, 0), fang + Vector2(5, 0), fang + Vector2(0, 10),
		]), Color.WHITE)
	if captain:
		# plain gold waistband marks the captain (no shell or crest motifs)
		draw_line(pos + Vector2(-radius * 0.8, radius * 0.62), pos + Vector2(radius * 0.8, radius * 0.62), Color("#e0b34c"), 8.0)
		if int(target.get("hp", 1)) > 1:
			draw_arc(pos, radius * 1.12, 0.0, TAU, 32, Color("#e0b34c"), 5.0)


func start_shuffle(from_lane: int) -> void:
	# magician TRACK: the fiction promises motion — show it. The answer glow
	# glides from the flashed lane to the true lane; a decoy arc crosses it.
	shuffle_from = clampi(from_lane, 0, choice_count - 1)
	shuffle_t = 1.5
	choice_flash = maxf(choice_flash, 2.2)
	queue_redraw()


func _lane_center(lane: int) -> Vector2:
	var lane_width := size.x / maxf(1.0, float(choice_count))
	return Vector2((float(lane) + 0.5) * lane_width, size.y * 0.55)


func _draw_shuffle_glide(target_lane: int) -> void:
	var t := clampf(1.0 - shuffle_t / 1.5, 0.0, 1.0)
	var eased := t * t * (3.0 - 2.0 * t)
	var from_point := _lane_center(shuffle_from)
	var to_point := _lane_center(target_lane)
	var main_point := from_point.lerp(to_point, eased)
	main_point.y -= sin(eased * PI) * 64.0
	var decoy_point := to_point.lerp(from_point, eased)
	decoy_point.y += sin(eased * PI) * 40.0
	draw_circle(decoy_point, 16.0, Color(1.0, 1.0, 1.0, 0.22))
	for i in range(4):
		var trail := clampf(eased - float(i) * 0.07, 0.0, 1.0)
		var trail_point := from_point.lerp(to_point, trail)
		trail_point.y -= sin(trail * PI) * 64.0
		draw_circle(trail_point, 20.0 - float(i) * 3.5, Color(accent, 0.85 - float(i) * 0.18))


func _draw_trace_patches(texture: Texture2D) -> void:
	# reveal the picture along the child's own finger path, patch by patch
	if trace_points.is_empty():
		return
	var texture_size := texture.get_size()
	var scale := Vector2(texture_size.x / maxf(1.0, size.x), texture_size.y / maxf(1.0, size.y))
	var patch := 96.0
	for point: Vector2 in trace_points:
		var destination := Rect2(point - Vector2(patch, patch) * 0.5, Vector2(patch, patch))
		var source := Rect2(destination.position * scale, destination.size * scale)
		draw_texture_rect_region(texture, destination, source)


func _oven_meter_rect() -> Rect2:
	return Rect2(size.x * 0.84, size.y * 0.12, 26.0, size.y * 0.64)


func _oven_handle_rect() -> Rect2:
	return Rect2(size.x * 0.20, size.y * 0.66, size.x * 0.44, size.y * 0.15)


func _oven_handle_hit_rect() -> Rect2:
	# The painted mitt handle stays trim, while the invisible touch target grows
	# to a preschool-friendly minimum on both the phone and the tablet panel.
	var padding := maxf(24.0, minf(size.x, size.y) * 0.055)
	return _oven_handle_rect().grow(padding)


func _draw_oven(_center: Vector2) -> void:
	# authored oven backdrop when present (gauge_chef ledger redirect);
	# a warm code-drawn oven face otherwise. NO green anywhere — the green
	# lock belongs to the retired ping-pong zones.
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(size.x * 0.08, size.y * 0.08, size.x * 0.68, size.y * 0.84), Color("#8a5a4a"), true)
		draw_rect(Rect2(size.x * 0.08, size.y * 0.08, size.x * 0.68, size.y * 0.84), Color("#5c3a30"), false, 6.0)
	# the window, and the cake tinting with the heat
	var window := Rect2(size.x * 0.16, size.y * 0.16, size.x * 0.52, size.y * 0.44)
	draw_rect(window, Color(0.23, 0.13, 0.10, 0.90), true)
	var heat := clampf(oven_t, 0.0, 1.0)
	var cake_color := Color("#f7ecd2").lerp(Color("#eab54e"), clampf(heat / 0.62, 0.0, 1.0))
	if heat > 0.80:
		cake_color = cake_color.lerp(Color("#9c6a30"), (heat - 0.80) * 5.0)
	var rise := 0.55 + 0.30 * heat
	var cake_base := Vector2(window.get_center().x, window.end.y - 10.0)
	var cake_width := window.size.x * 0.56
	var cake_height := window.size.y * 0.52 * rise
	var jiggle := 0.0
	if oven_peek > 0.0:
		jiggle = sin(oven_peek * 26.0) * 5.0
	if completion_accepted:
		jiggle = 0.0
	draw_rect(Rect2(cake_base.x - cake_width * 0.5 + jiggle, cake_base.y - cake_height, cake_width, cake_height), cake_color, true)
	draw_circle(Vector2(cake_base.x + jiggle, cake_base.y - cake_height), cake_width * 0.5, cake_color)
	# golden shimmer in the window during the ready band
	if heat >= 0.45 and heat <= 0.80:
		var shimmer := 0.30 + 0.20 * sin(heat * 90.0)
		draw_circle(Vector2(cake_base.x, cake_base.y - cake_height * 0.9), 10.0, Color(1.0, 0.92, 0.55, shimmer))
	# toasty steam curls — cozy, not alarming
	if heat > 0.80:
		for i in range(3):
			var sx := window.position.x + window.size.x * (0.28 + 0.22 * float(i))
			var sy := window.position.y + 14.0 - fmod(heat * 260.0 + float(i) * 23.0, 34.0)
			draw_arc(Vector2(sx, sy), 9.0, PI * 0.2, PI * 1.3, 12, Color(0.98, 0.92, 0.80, 0.5), 4.0)
	# the thermometer: rises bottom-to-top at the static rate, band-colored
	var slot := _oven_meter_rect()
	draw_rect(slot, Color(0.98, 0.97, 0.93, 0.9), true)
	draw_rect(slot, Color("#5c3a30"), false, 4.0)
	var fill_height := slot.size.y * heat
	var band_color := Color("#f3dfa8") if heat < 0.45 else (Color("#ffc94d") if heat <= 0.80 else Color("#d9813c"))
	draw_rect(Rect2(slot.position.x, slot.end.y - fill_height, slot.size.x, fill_height), band_color, true)
	for band: float in [0.45, 0.80]:
		var tick_y: float = slot.end.y - slot.size.y * band
		draw_line(Vector2(slot.position.x - 6.0, tick_y), Vector2(slot.end.x + 6.0, tick_y), Color("#5c3a30"), 3.0)
	# the mitt handle — the ONE verb. It glows gold through the ready band.
	var handle := _oven_handle_rect()
	var handle_center := handle.get_center()
	if oven_peek > 0.0:
		# the door swings open for the peek
		draw_rect(Rect2(handle.position.x, handle.position.y + 10.0, handle.size.x, handle.size.y), Color("#6e4638"), true)
	else:
		draw_rect(handle, Color("#6e4638"), true)
	draw_rect(handle, Color("#4a2c22"), false, 4.0)
	draw_circle(handle_center, 20.0, Color("#e8b24a"))
	if heat >= 0.45 and not oven_done:
		var pulse := 0.35 + 0.25 * (0.5 + 0.5 * sin(heat * 70.0))
		draw_arc(handle_center, 34.0 + 8.0 * pulse, 0.0, TAU, 40, Color(1.0, 0.83, 0.35, pulse), 7.0)
	if oven_done or completion_accepted:
		# Hold on the causal result: open door, finished cake and a warm crown of
		# sparkles. Never replace the baked scene with the generic gauge success.
		draw_rect(Rect2(handle.position + Vector2(0.0, 14.0), handle.size),
			Color("#6e4638"), true)
		draw_arc(window.get_center(), minf(window.size.x, window.size.y) * 0.44,
			0.0, TAU, 40, Color(1.0, 0.84, 0.30, 0.78), 7.0)
		for sparkle_index in range(5):
			var sparkle_angle := -PI * 0.9 + float(sparkle_index) * PI * 0.45
			var sparkle_pos := window.get_center() + Vector2.from_angle(sparkle_angle) * 78.0
			draw_circle(sparkle_pos, 5.0 + float(sparkle_index % 2) * 2.0,
				Color(1.0, 0.93, 0.60, 0.88))


func _pipe_setup_round() -> void:
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	pipe_grid = []
	pipe_fixed = []
	for _cell in range(PIPE_COLS * PIPE_ROWS):
		pipe_grid.append("")
		pipe_fixed.append(false)
	var fixed: Dictionary = round_data.get("fixed", {})
	for cell: int in fixed.keys():
		pipe_grid[cell] = String(fixed[cell])
		pipe_fixed[cell] = true
	for cell: int in (round_data.get("imps", []) as Array):
		pipe_grid[cell] = "IMP"
		pipe_fixed[cell] = true
	pipe_tray = (round_data.get("tray", []) as Array).duplicate()
	pipe_tray_sel = -1
	pipe_drag_tile = ""
	pipe_drag_from = -1
	pipe_flow = []
	pipe_flow_t = 0.0
	pipe_wait_t = 0.0
	pipe_pause = 0.0
	queue_redraw()


func _pipe_cell_rect(cell: int) -> Rect2:
	var col := cell % PIPE_COLS
	var row := floori(float(cell) / float(PIPE_COLS))
	return Rect2(PIPE_ORIGIN + Vector2(float(col), float(row)) * PIPE_CELL, Vector2(PIPE_CELL, PIPE_CELL))


func _pipe_cell_at(point: Vector2) -> int:
	var local := point - PIPE_ORIGIN
	if local.x < 0.0 or local.y < 0.0:
		return -1
	var col := int(local.x / PIPE_CELL)
	var row := int(local.y / PIPE_CELL)
	if col >= PIPE_COLS or row >= PIPE_ROWS:
		return -1
	return row * PIPE_COLS + col


func _pipe_tray_rect(slot: int) -> Rect2:
	return Rect2(Vector2(
		PIPE_TRAY_START_X + float(slot) * PIPE_TRAY_STEP,
		PIPE_ORIGIN.y + PIPE_CELL * float(PIPE_ROWS) + PIPE_TRAY_GAP_Y),
		Vector2.ONE * PIPE_TRAY_SIDE)


func _pipe_tank_rect(round_data: Dictionary) -> Rect2:
	var entry_rect := _pipe_cell_rect(int(round_data.get("entry", 4)))
	var center := Vector2(
		PIPE_ORIGIN.x - PIPE_TANK_SIDE * 0.5 - 4.0,
		entry_rect.get_center().y)
	return Rect2(center - Vector2.ONE * PIPE_TANK_SIDE * 0.5,
		Vector2.ONE * PIPE_TANK_SIDE)


func _pipe_intake_rect(round_data: Dictionary) -> Rect2:
	var exit_cell := int(round_data.get("exit", 7))
	var exit_dir: Vector2i = round_data.get("exit_dir", Vector2i(1, 0))
	var exit_rect := _pipe_cell_rect(exit_cell)
	var center := exit_rect.get_center() + Vector2(float(exit_dir.x), float(exit_dir.y)) \
		* (PIPE_CELL * 0.5 + PIPE_ENDPOINT_GAP)
	return Rect2(center - Vector2.ONE * PIPE_INTAKE_SIDE * 0.5,
		Vector2.ONE * PIPE_INTAKE_SIDE)


func _pipe_flow_cells() -> Array:
	var cells: Array = []
	for step: Array in pipe_flow:
		cells.append(int(step[0]))
	return cells


func _pipe_next_step() -> Array:
	# [next_cell, in_dir] the fuel would advance into, or [] if blocked/done
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	var entry := int(round_data.get("entry", 4))
	if pipe_flow.is_empty():
		return [entry, Vector2i(1, 0)] if pipe_grid[entry] != "" else []
	var head: Array = pipe_flow[pipe_flow.size() - 1]
	var head_cell := int(head[0])
	var in_dir: Vector2i = head[1]
	var tile := String(pipe_grid[head_cell])
	if not PIPE_MOUTHS.has(tile):
		return []
	var out_dir := Vector2i.ZERO
	for mouth: Vector2i in (PIPE_MOUTHS[tile] as Array):
		if mouth != -in_dir:
			out_dir = mouth
	if head_cell == int(round_data.get("exit", 7)) and out_dir == (round_data.get("exit_dir", Vector2i(1, 0)) as Vector2i):
		return [-1, out_dir]
	var col := head_cell % PIPE_COLS + out_dir.x
	var row := floori(float(head_cell) / float(PIPE_COLS)) + out_dir.y
	if col < 0 or col >= PIPE_COLS or row < 0 or row >= PIPE_ROWS:
		return []
	var next_cell := row * PIPE_COLS + col
	var next_tile := String(pipe_grid[next_cell])
	if not PIPE_MOUTHS.has(next_tile):
		return []
	var accepts := false
	for mouth: Vector2i in (PIPE_MOUTHS[next_tile] as Array):
		if mouth == -out_dir:
			accepts = true
	return [next_cell, out_dir] if accepts else []


func _pipe_path_complete() -> bool:
	# would the fuel reach the exit if it kept flowing? (drives acceleration)
	var probe_flow := pipe_flow.duplicate(true)
	var original := pipe_flow
	pipe_flow = probe_flow
	var reached := false
	for _guard in range(PIPE_COLS * PIPE_ROWS + 2):
		var step := _pipe_next_step()
		if step.is_empty():
			break
		if int(step[0]) < 0:
			reached = true
			break
		pipe_flow.append(step)
	pipe_flow = original
	return reached


func _pipe_tick(delta: float) -> void:
	if pipe_pause > 0.0:
		pipe_pause = maxf(0.0, pipe_pause - delta)
		if pipe_pause <= 0.0 and pipe_round < PIPE_ROUNDS.size():
			_pipe_setup_round()
		queue_redraw()
		return
	pipe_flow_t += delta
	var step_time := 0.35 if _pipe_path_complete() else 1.2
	if pipe_flow_t >= step_time:
		pipe_flow_t = 0.0
		var step := _pipe_next_step()
		if step.is_empty():
			# the fuel WAITS at the last good pipe, bulging patiently
			pipe_wait_t += step_time
			if pipe_wait_t >= 16.0:
				# waited twice the hint window: the wrong pipe hops back to
				# the tray on its own. Nothing lost, nothing failed.
				var wrong := _pipe_hint_cell()
				if wrong >= 0 and PIPE_MOUTHS.has(String(pipe_grid[wrong])) and not pipe_fixed[wrong]:
					var keep: Array = []
					for flow_step: Array in pipe_flow:
						if int(flow_step[0]) == wrong:
							break
						keep.append(flow_step)
					pipe_flow = keep
					pipe_tray.append(String(pipe_grid[wrong]))
					pipe_grid[wrong] = ""
				pipe_wait_t = 8.0
		elif int(step[0]) < 0:
			# reached the rocket! round done
			pipe_round += 1
			pipe_wait_t = 0.0
			gesture.emit("pipe", 1.0, 1.0)
			if pipe_round < PIPE_ROUNDS.size():
				pipe_pause = 1.0
		else:
			pipe_wait_t = 0.0
			pipe_flow.append(step)
	pipe_redraw += delta
	if pipe_redraw >= 0.06:
		pipe_redraw = 0.0
		queue_redraw()


func _pipe_press(at: Vector2) -> void:
	if completion_accepted:
		return
	for slot in range(pipe_tray.size()):
		if _pipe_tray_rect(slot).has_point(at):
			# CARRY the tile: it leaves the tray immediately, so no input
			# sequence can ever duplicate it (2026-08-05 release audit)
			pipe_drag_tile = String(pipe_tray[slot])
			pipe_tray.remove_at(slot)
			pipe_drag_from = -1
			pipe_tray_sel = -1
			queue_redraw()
			return
	var cell := _pipe_cell_at(at)
	if cell < 0:
		return
	var tile := String(pipe_grid[cell])
	if tile == "IMP":
		# giggle! he rolls over but keeps napping — route around him
		gesture.emit("pipe", 0.0, 0.6)
		queue_redraw()
		return
	if PIPE_MOUTHS.has(tile) and not pipe_fixed[cell]:
		# lift ANY placed pipe — even a fueled one. A wrong pipe the fuel
		# has entered was a permanent dead end (rounds 2 and 3 both had a
		# natural first move that killed the round); lifting it drains the
		# fuel back to the last good pipe and the child fixes her own plan.
		if cell in _pipe_flow_cells():
			var keep: Array = []
			for step: Array in pipe_flow:
				if int(step[0]) == cell:
					break
				keep.append(step)
			pipe_flow = keep
		pipe_drag_tile = tile
		pipe_drag_from = cell
		pipe_grid[cell] = ""
		pipe_tray_sel = -1
		pipe_wait_t = 0.0
		queue_redraw()
		return
	if tile == "" and pipe_tray_sel >= 0 and pipe_tray_sel < pipe_tray.size():
		# tap-tile-then-tap-cell: place the remembered tray tile here
		pipe_grid[cell] = String(pipe_tray[pipe_tray_sel])
		pipe_tray.remove_at(pipe_tray_sel)
		pipe_tray_sel = -1
		pipe_wait_t = 0.0
		gesture.emit("pipe", 0.0, 1.0)
		queue_redraw()


func _pipe_release(at: Vector2) -> void:
	if pipe_drag_tile == "":
		return
	var cell := _pipe_cell_at(at)
	if cell >= 0 and String(pipe_grid[cell]) == "":
		pipe_grid[cell] = pipe_drag_tile
		pipe_wait_t = 0.0
		gesture.emit("pipe", 0.0, 1.0)
	elif cell >= 0 and pipe_drag_from >= 0 and String(pipe_grid[pipe_drag_from]) == "":
		# dropped on an occupied cell: the tile hops back where it came from
		pipe_grid[pipe_drag_from] = pipe_drag_tile
	else:
		# released off the grid (the tray, or a stray drag): back to the
		# tray, SELECTED — a tap on the tray then a tap on a cell is the
		# whole one-finger placement grammar, and lifting a placed pipe
		# down to the tray must actually put it there
		pipe_tray.append(pipe_drag_tile)
		pipe_tray_sel = pipe_tray.size() - 1
	pipe_drag_tile = ""
	pipe_drag_from = -1
	queue_redraw()


func _pipe_hint_cell() -> int:
	# after 8s of waiting fuel, point at the cell the flow needs next
	if pipe_wait_t < 8.0:
		return -1
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	if pipe_flow.is_empty():
		return int(round_data.get("entry", 4))
	var head: Array = pipe_flow[pipe_flow.size() - 1]
	var head_cell := int(head[0])
	var in_dir: Vector2i = head[1]
	var tile := String(pipe_grid[head_cell])
	if not PIPE_MOUTHS.has(tile):
		return -1
	var out_dir := Vector2i.ZERO
	for mouth: Vector2i in (PIPE_MOUTHS[tile] as Array):
		if mouth != -in_dir:
			out_dir = mouth
	var col := head_cell % PIPE_COLS + out_dir.x
	var row := floori(float(head_cell) / float(PIPE_COLS)) + out_dir.y
	if col < 0 or col >= PIPE_COLS or row < 0 or row >= PIPE_ROWS:
		# blocked by the edge: the wrong pipe itself is the fix — lift it
		return head_cell if not pipe_fixed[head_cell] else -1
	var next_cell := row * PIPE_COLS + col
	if String(pipe_grid[next_cell]) == "IMP":
		# never mark the napping imp — the pipe pointing at him is the fix
		return head_cell if not pipe_fixed[head_cell] else -1
	return next_cell


func _pipe_demo_target_cell() -> int:
	# Rehints prefer the live fuel-gap diagnosis. On the first untouched
	# board, derive the cell immediately beyond the authored entry stub so the
	# hand demonstrates a useful tray-to-grid placement instead of dropping a
	# pipe on an arbitrary empty square.
	var hinted := _pipe_hint_cell()
	if hinted >= 0:
		return hinted
	if pipe_round < 0 or pipe_round >= PIPE_ROUNDS.size() or pipe_grid.is_empty():
		return -1
	var round_data: Dictionary = PIPE_ROUNDS[pipe_round]
	var entry := int(round_data.get("entry", 4))
	if entry < 0 or entry >= pipe_grid.size():
		return -1
	var tile := String(pipe_grid[entry])
	if PIPE_MOUTHS.has(tile):
		var incoming := Vector2i(1, 0)
		var outgoing := Vector2i.ZERO
		for mouth: Vector2i in (PIPE_MOUTHS[tile] as Array):
			if mouth != -incoming:
				outgoing = mouth
		var col := entry % PIPE_COLS + outgoing.x
		var row := floori(float(entry) / float(PIPE_COLS)) + outgoing.y
		if col >= 0 and col < PIPE_COLS and row >= 0 and row < PIPE_ROWS:
			var next_cell := row * PIPE_COLS + col
			if String(pipe_grid[next_cell]) == "":
				return next_cell
	for cell in range(pipe_grid.size()):
		if String(pipe_grid[cell]) == "":
			return cell
	return -1


func _pipe_demo_incoming_direction(target_cell: int) -> Vector2i:
	if target_cell < 0 or target_cell >= pipe_grid.size():
		return Vector2i.ZERO
	if not pipe_flow.is_empty():
		var head: Array = pipe_flow[pipe_flow.size() - 1]
		var head_cell := int(head[0])
		var in_dir: Vector2i = head[1]
		var tile := String(pipe_grid[head_cell])
		if PIPE_MOUTHS.has(tile):
			for mouth: Vector2i in (PIPE_MOUTHS[tile] as Array):
				if mouth != -in_dir:
					var next_col := head_cell % PIPE_COLS + mouth.x
					var next_row := floori(float(head_cell) / float(PIPE_COLS)) + mouth.y
					if next_row * PIPE_COLS + next_col == target_cell:
						return mouth
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	var entry := int(round_data.get("entry", 4))
	var entry_tile := String(pipe_grid[entry])
	if PIPE_MOUTHS.has(entry_tile):
		var entry_in := Vector2i(1, 0)
		for mouth: Vector2i in (PIPE_MOUTHS[entry_tile] as Array):
			if mouth != -entry_in:
				var next_col := entry % PIPE_COLS + mouth.x
				var next_row := floori(float(entry) / float(PIPE_COLS)) + mouth.y
				if next_row * PIPE_COLS + next_col == target_cell:
					return mouth
	return Vector2i.ZERO


func _pipe_demo_tray_slot(target_cell: int) -> int:
	## Select the first useful compatible tile, not simply the first tray slot.
	## This is essential in round three, where slot zero points into an imp and
	## the NW elbow in slot one is the demonstrated move.
	if pipe_tray.is_empty():
		return -1
	var incoming := _pipe_demo_incoming_direction(target_cell)
	if incoming == Vector2i.ZERO:
		return clampi(pipe_tray_sel, 0, pipe_tray.size() - 1) if pipe_tray_sel >= 0 else 0
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	var exit_cell := int(round_data.get("exit", 7))
	var exit_dir: Vector2i = round_data.get("exit_dir", Vector2i(1, 0))
	var best_slot := -1
	var best_score := -100000
	for slot in range(pipe_tray.size()):
		var tile := String(pipe_tray[slot])
		if not PIPE_MOUTHS.has(tile):
			continue
		var mouths: Array = PIPE_MOUTHS[tile]
		if -incoming not in mouths:
			continue
		var outgoing := Vector2i.ZERO
		for mouth: Vector2i in mouths:
			if mouth != -incoming:
				outgoing = mouth
		var score := 0
		if target_cell == exit_cell and outgoing == exit_dir:
			score = 1000
		else:
			var col := target_cell % PIPE_COLS + outgoing.x
			var row := floori(float(target_cell) / float(PIPE_COLS)) + outgoing.y
			if col < 0 or col >= PIPE_COLS or row < 0 or row >= PIPE_ROWS:
				score = -500
			else:
				var next_cell := row * PIPE_COLS + col
				var next_tile := String(pipe_grid[next_cell])
				if next_tile == "IMP":
					score = -400
				else:
					score = 100
					var exit_col := exit_cell % PIPE_COLS
					var exit_row := floori(float(exit_cell) / float(PIPE_COLS))
					score -= absi(col - exit_col) + absi(row - exit_row)
					if PIPE_MOUTHS.has(next_tile) and -outgoing in (PIPE_MOUTHS[next_tile] as Array):
						score += 40
		if score > best_score:
			best_score = score
			best_slot = slot
	return best_slot if best_slot >= 0 else 0


func _draw_pipe_tile(rect: Rect2, tile: String, fueled: bool) -> void:
	if pipe_tiles.has(tile):
		# authored tile: the art owns the look; fuel is a teal wash inside it
		draw_texture_rect(pipe_tiles[tile] as Texture2D, rect.grow(-6.0), false)
		if fueled:
			draw_texture_rect(pipe_tiles[tile] as Texture2D, rect.grow(-6.0), false,
				Color(0.37, 0.85, 0.81, 0.55))
		return
	var body := rect.grow(-10.0)
	draw_rect(body, Color("#caa269") if not fueled else Color("#d8b87e"), true)
	draw_rect(body, Color("#7a5a34"), false, 4.0)
	var center := rect.get_center()
	var bore := 26.0
	var fuel := Color("#5fd8cf")
	var glass := Color("#2e4a52")
	for mouth: Vector2i in (PIPE_MOUTHS.get(tile, []) as Array):
		var arm_end := center + Vector2(float(mouth.x), float(mouth.y)) * (rect.size.x * 0.5 - 8.0)
		draw_line(center, arm_end, glass, bore)
		if fueled:
			draw_line(center, arm_end, fuel, bore - 10.0)
		# open dark mouths: wordless orientation cues
		draw_circle(arm_end, bore * 0.42, Color(0.12, 0.10, 0.10, 0.95))
	draw_circle(center, bore * 0.62, glass)
	if fueled:
		draw_circle(center, bore * 0.40, fuel)


func _draw_pipe() -> void:
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	var flow_cells := _pipe_flow_cells()
	var hint := _pipe_hint_cell()
	# grid plates
	for cell in range(PIPE_COLS * PIPE_ROWS):
		var rect := _pipe_cell_rect(cell)
		draw_rect(rect.grow(-4.0), Color(0.16, 0.22, 0.34, 0.55), true)
		draw_rect(rect.grow(-4.0), Color(0.55, 0.66, 0.86, 0.5), false, 2.0)
		var tile := String(pipe_grid[cell])
		if tile == "IMP":
			# a napping mischief imp: he giggles if tapped, but stays
			var imp_center := rect.get_center()
			draw_circle(imp_center + Vector2(0, 12.0), 30.0, Color("#8d6bc8"))
			draw_circle(imp_center + Vector2(0, -16.0), 20.0, Color("#a186d6"))
			for z in range(2):
				draw_circle(imp_center + Vector2(26.0 + float(z) * 14.0, -30.0 - float(z) * 12.0), 4.0 + float(z) * 2.0, Color(1, 1, 1, 0.7))
		elif PIPE_MOUTHS.has(tile):
			_draw_pipe_tile(rect, tile, cell in flow_cells)
		if cell == hint:
			# Mewsha's stand-in twinkle: the kind nudge, never a demand
			var pulse := 0.5 + 0.4 * sin(pipe_wait_t * 5.0)
			draw_arc(rect.get_center(), 44.0, 0.0, TAU, 32, Color(1.0, 0.85, 0.35, pulse), 6.0)
	# fuel bulge where the flow waits
	if pipe_wait_t > 0.5 and not pipe_flow.is_empty():
		var head_rect := _pipe_cell_rect(int((pipe_flow[pipe_flow.size() - 1] as Array)[0]))
		var bulge := 6.0 + 3.0 * sin(pipe_wait_t * 6.0)
		draw_circle(head_rect.get_center(), 18.0 + bulge, Color(0.37, 0.85, 0.81, 0.55))
	# tank (entry) and rocket (exit) stubs outside the grid
	var tank_rect := _pipe_tank_rect(round_data)
	var tank_center := tank_rect.get_center()
	if pipe_tank_texture != null:
		draw_texture_rect(pipe_tank_texture, tank_rect, false)
	else:
		draw_circle(tank_center, 46.0, Color("#3f6f8a"))
		draw_circle(tank_center, 34.0, Color("#5fd8cf"))
	draw_rect(Rect2(tank_center.x + 34.0, tank_center.y - 13.0, PIPE_ORIGIN.x - tank_center.x - 34.0 + 6.0, 26.0), Color("#7a5a34"), true)
	var intake_rect := _pipe_intake_rect(round_data)
	var rocket_center := intake_rect.get_center()
	if pipe_intake_texture != null:
		draw_texture_rect(pipe_intake_texture, intake_rect, false)
	else:
		draw_circle(rocket_center, 44.0, Color("#c8cede"))
		draw_circle(rocket_center, 30.0, Color("#8090b0"))
	var round_done := pipe_round >= PIPE_ROUNDS.size() or pipe_pause > 0.0
	if round_done:
		draw_circle(rocket_center, 20.0, Color("#5fd8cf"))
		for ring in range(3):
			draw_arc(rocket_center, 52.0 + float(ring) * 16.0, 0.0, TAU, 32, Color(1.0, 0.9, 0.5, 0.5 - float(ring) * 0.13), 5.0)
	# the tray
	for slot in range(pipe_tray.size()):
		var tray_rect := _pipe_tray_rect(slot)
		draw_rect(tray_rect, Color(0.92, 0.95, 1.0, 0.9), true)
		draw_rect(tray_rect, Color("#7a5a34") if slot != pipe_tray_sel else Color("#ffcf4d"), false, 4.0 if slot != pipe_tray_sel else 6.0)
		_draw_pipe_tile(tray_rect, String(pipe_tray[slot]), false)
	# the tile riding the finger
	if pipe_drag_tile != "":
		_draw_pipe_tile(Rect2(pointer_pos - Vector2(PIPE_CELL, PIPE_CELL) * 0.5, Vector2(PIPE_CELL, PIPE_CELL)), pipe_drag_tile, false)


func _echo_star_center(star: int) -> Vector2:
	return Vector2(size.x * (0.22 + 0.28 * float(star)), size.y * 0.52)


func _echo_tick(delta: float) -> void:
	var glow_before := echo_glow
	echo_glow = maxf(0.0, echo_glow - delta)
	if not is_equal_approx(glow_before, echo_glow):
		# Listening used to return before scheduling a new frame, leaving the
		# last sung star visibly frozen until another input arrived.
		queue_redraw()
	if echo_listening:
		return
	# SHOW: the stars sing their verse one by one; then it is her turn
	echo_show_t -= delta
	if echo_show_t <= 0.0:
		var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
		echo_show_i += 1
		if echo_show_i >= verse.size():
			echo_listening = true
			echo_input_i = 0
		else:
			echo_last_note = int(verse[echo_show_i])
			echo_glow = 0.45
			gesture.emit("echo_note", 0.0, 1.0)
			echo_show_t = 0.55
	queue_redraw()


func _echo_press(at: Vector2) -> void:
	if completion_accepted:
		return
	var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
	var nearest := -1
	var nearest_d := 92.0
	for candidate in range(3):
		var d := at.distance_to(_echo_star_center(candidate))
		if d < nearest_d:
			nearest_d = d
			nearest = candidate
	for star in range(3):
		if star == nearest:
			if not echo_listening:
				# eager taps during the song just twinkle — no punishment
				echo_last_note = star
				gesture.emit("echo_note", 0.0, 0.8)
				return
			if star == int(verse[echo_input_i]):
				echo_last_note = star
				echo_glow = 0.45
				gesture.emit("echo_note", 0.0, 1.0)
				echo_input_i += 1
				if echo_input_i >= verse.size():
					# verse sung back! the song grows by one verse
					echo_verse += 1
					echo_listening = false
					echo_show_i = -1
					echo_show_t = 0.7
					gesture.emit("echo", 1.0, 1.0)
			else:
				# kind replay: the stars sing the verse again
				echo_last_note = star
				gesture.emit("echo", _miss_pay(), 0.4)
				echo_listening = false
				echo_show_i = -1
				echo_show_t = 0.9
			queue_redraw()
			return
	gesture.emit("echo", 0.0, 0.6)


func _draw_echo_star(center: Vector2, radius: float, color: Color) -> void:
	var art: Texture2D = echo_lit_texture if color.r > 0.9 and color.g > 0.7 else echo_unlit_texture
	if art != null:
		draw_texture_rect(art, Rect2(center - Vector2.ONE * radius, Vector2.ONE * radius * 2.0), false, color)
		return
	var points := PackedVector2Array()
	for i in range(10):
		var r := radius if i % 2 == 0 else radius * 0.45
		var a := -PI * 0.5 + TAU * float(i) / 10.0
		points.append(center + Vector2(cos(a), sin(a)) * r)
	draw_polygon(points, PackedColorArray([color]))


func _draw_echo(_center: Vector2) -> void:
	var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
	var showing := -1 if echo_listening or echo_show_i < 0 or echo_show_i >= verse.size() else int(verse[echo_show_i])
	for star in range(3):
		var star_center := _echo_star_center(star)
		var lit := star == showing or (star == echo_last_note and echo_glow > 0.0)
		var base := Color("#ffd75e") if lit else Color(0.72, 0.62, 0.92, 0.85)
		_draw_echo_star(star_center, 64.0 if lit else 54.0, base)
		if lit:
			draw_arc(star_center, 78.0, 0.0, TAU, 36, Color(1.0, 0.9, 0.5, 0.55), 6.0)
	# the assembled song: one small lit star per verse already sung
	for done in range(clampi(echo_verse, 0, ECHO_VERSES.size())):
		_draw_echo_star(Vector2(size.x * (0.38 + 0.12 * float(done)), size.y * 0.14), 18.0, Color("#ffd75e"))
	if echo_listening:
		# her turn: a soft ring invites the next star in the verse
		var next_center := _echo_star_center(int(verse[clampi(echo_input_i, 0, verse.size() - 1)]))
		draw_arc(next_center, 88.0, 0.0, TAU, 36, Color(accent, 0.35), 5.0)


func _is_candymaker_pour() -> bool:
	return mode == "pourt" and visual_context == "pour_candymaker"


func _pour_bowl_rect() -> Rect2:
	if _is_candymaker_pour():
		# One complete shell is the single source of truth for picture, fill,
		# stream landing and completion. Keep it wholly inside the 392x232
		# shipping surface instead of pointing at three conflicting old molds.
		var side := minf(size.x * 0.34, size.y * 0.47)
		return Rect2(Vector2(size.x * 0.30, size.y - side - 8.0), Vector2.ONE * side)
	return Rect2(size.x * 0.20, size.y * 0.62, size.x * 0.60, size.y * 0.30)


func _pour_home_x() -> float:
	if _is_candymaker_pour():
		return _pour_bowl_rect().end.x + 26.0
	return size.x * 0.34


func _pour_x_bounds() -> Vector2:
	if _is_candymaker_pour():
		var bowl := _pour_bowl_rect()
		# At either extreme the physical left-facing spout remains over the
		# shell throughout its whole rotation arc. The anchor's radius is the
		# worst-case left reach, plus a small landing margin.
		var left_reach := _candymaker_spout_local_anchor(_pour_pitcher_rect()).length()
		return Vector2(bowl.position.x + left_reach + 2.0, bowl.end.x + 26.0)
	return Vector2(size.x * 0.12, size.x * 0.88)


func _pour_pitcher_rect() -> Rect2:
	if _is_candymaker_pour():
		var side := minf(132.0, size.y * 0.54)
		return Rect2(Vector2(pour_x - side * 0.5, maxf(10.0, size.y * 0.12)),
			Vector2.ONE * side)
	return Rect2(pour_x - 70.0, size.y * 0.10, 140.0, 120.0)


func _pour_pitcher_hit_rect() -> Rect2:
	return _pour_pitcher_rect().grow(22.0 if _is_candymaker_pour() else 0.0)


func _pour_pitcher_rotation() -> float:
	return -pour_tilt * 1.05 if _is_candymaker_pour() else pour_tilt * 1.05


func _candymaker_spout_local_anchor(pitcher: Rect2) -> Vector2:
	return (CANDYMAKER_PITCHER_SPOUT_UV - Vector2.ONE * 0.5) * pitcher.size


func _pour_spout_point() -> Vector2:
	var pitcher := _pour_pitcher_rect()
	if _is_candymaker_pour():
		# Both approved pitcher sprites have a LEFT spout. Transform its measured
		# art anchor with the same rotation as the rendered jug so the stream stays
		# attached to the painted lip throughout the tilt.
		var local_anchor := _candymaker_spout_local_anchor(pitcher)
		return pitcher.get_center() + local_anchor.rotated(_pour_pitcher_rotation())
	return Vector2(pour_x + 52.0 + 26.0 * pour_tilt,
		pitcher.position.y + 58.0 + 30.0 * pour_tilt)


func _pour_landing_point() -> Vector2:
	var bowl := _pour_bowl_rect()
	var spout := _pour_spout_point()
	return Vector2(spout.x if _is_candymaker_pour() else spout.x + 10.0,
		bowl.position.y + 16.0)


func _pour_stream_active() -> bool:
	return pour_tilt > 0.36 and (pour_hold or not _is_candymaker_pour())


func _pour_tick(delta: float) -> void:
	if completion_accepted:
		# The final payout is synchronous: the owning world accepts completion
		# before this frame returns. Keep animating only the polite tilt-down;
		# never leave an empty jug frozen sideways during the success hold.
		pour_hold = false
		var settled_tilt := move_toward(pour_tilt, 0.0, delta / 0.35)
		if not is_equal_approx(settled_tilt, pour_tilt):
			pour_tilt = settled_tilt
			queue_redraw()
		return
	var want := 1.0 if pour_hold else 0.0
	var rate := delta / 0.8 if pour_hold else delta / 0.35
	pour_tilt = move_toward(pour_tilt, want, rate)
	var stream := _pour_stream_active()
	if stream:
		var spout_x := _pour_spout_point().x
		var bowl := _pour_bowl_rect()
		var on_target := spout_x >= bowl.position.x and spout_x <= bowl.end.x
		if on_target and pour_level < 1.0:
			var tilt_flow := (pour_tilt - 0.36) / 0.64
			var fill := 0.0
			if _is_candymaker_pour():
				# Roughly 3.5 seconds including the visible tilt-in: short enough to
				# read as responsive, long enough to see the shell fill.
				fill = tilt_flow * delta / CANDYMAKER_POUR_SECONDS
			else:
				var reserve_flow := maxf(pour_reserve, 0.12) / 1.2
				fill = tilt_flow * delta / 4.6 * reserve_flow
			var applied_fill := minf(fill, 1.0 - pour_level)
			pour_level += applied_fill
			var drain_scale := 1.2 if _is_candymaker_pour() else 1.0
			pour_reserve = maxf(0.0, pour_reserve - applied_fill * drain_scale)
			# the child controls the pour, not a clock: progress IS the fill
			pour_emit_acc += applied_fill
			if pour_emit_acc >= 0.04 or pour_level >= 1.0:
				gesture.emit("pourt", pour_emit_acc * 5.0, 1.0)
				pour_emit_acc = 0.0
			if pour_level >= 1.0:
				# brim! the pitcher politely rights itself with a ring
				pour_hold = false
				gesture.emit("pour_ding", 0.0, 1.0)
	pour_redraw += delta
	if pour_redraw >= 0.05:
		pour_redraw = 0.0
		queue_redraw()


func _draw_candymaker_pour_mold(bowl: Rect2) -> void:
	# A quiet glow makes the one destination obvious without words. The accepted
	# teal shell remains the artwork at every state; this is a non-destructive
	# dim-to-colour reveal, not a replacement design.
	draw_circle(bowl.get_center(), bowl.size.x * 0.52, Color(accent, 0.12))
	if pour_mold_texture == null:
		draw_circle(bowl.get_center(), bowl.size.x * 0.42, Color("#74d8d2"))
		return
	draw_texture_rect(pour_mold_texture, bowl, false, Color(0.48, 0.48, 0.62, 0.28))
	if pour_level > 0.0:
		var texture_size := pour_mold_texture.get_size()
		var source_y := texture_size.y * (1.0 - pour_level)
		var source_h := texture_size.y - source_y
		var destination_y := bowl.position.y + bowl.size.y * (1.0 - pour_level)
		var destination_h := bowl.end.y - destination_y
		draw_texture_rect_region(pour_mold_texture,
			Rect2(bowl.position.x, destination_y, bowl.size.x, destination_h),
			Rect2(0.0, source_y, texture_size.x, source_h))
	draw_arc(bowl.get_center(), bowl.size.x * 0.48, 0.0, TAU, 36,
		Color(accent, 0.46 + 0.18 * sin(demo_t * 4.0)), 5.0)


func _draw_pour_scene(_center: Vector2) -> void:
	if not _is_candymaker_pour() and widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	var bowl := _pour_bowl_rect()
	# the bowl and its rising batter (authored fill strip when present)
	if _is_candymaker_pour():
		_draw_candymaker_pour_mold(bowl)
	elif widget_overlay != null:
		_draw_progress_overlay(widget_overlay, pour_level, false)
	else:
		draw_rect(bowl, Color(0.90, 0.94, 1.0, 0.55), true)
		var level_height := bowl.size.y * 0.8 * pour_level
		var surface_y := bowl.end.y - 8.0 - level_height
		var wobble := sin(pour_tilt * 20.0 + pour_level * 30.0) * 2.0
		draw_rect(Rect2(bowl.position.x + 8.0, surface_y + wobble, bowl.size.x - 16.0, level_height), Color("#f2c66d"), true)
	if not _is_candymaker_pour():
		draw_rect(bowl, Color("#7a5a34"), false, 5.0)
	# the pitcher: tilts in the hand, visibly drains as it pours
	var pitcher := _pour_pitcher_rect()
	var pitcher_center := pitcher.get_center()
	draw_set_transform(pitcher_center, _pour_pitcher_rotation())
	if widget_mover != null:
		draw_texture_rect(widget_mover, Rect2(-pitcher.size * 0.5, pitcher.size), false)
	else:
		draw_rect(Rect2(-pitcher.size * 0.5, pitcher.size), Color("#8fb4d8"), true)
		var content_height := pitcher.size.y * 0.7 * (pour_reserve / 1.2)
		draw_rect(Rect2(-pitcher.size.x * 0.36, pitcher.size.y * 0.42 - content_height, pitcher.size.x * 0.72, content_height), Color("#f2c66d"), true)
		draw_rect(Rect2(-pitcher.size * 0.5, pitcher.size), Color("#4a5a7a"), false, 4.0)
	draw_set_transform(Vector2.ZERO)
	# the stream: it follows the spout, thick with the tilt, and lands
	if _pour_stream_active() and pour_level < 1.0:
		var spout := _pour_spout_point()
		var landing := _pour_landing_point()
		var thickness := 5.0 + 9.0 * (pour_tilt - 0.36) / 0.64
		var mid := Vector2(lerpf(spout.x, landing.x, 0.5) + 6.0, lerpf(spout.y, landing.y, 0.5))
		draw_line(spout, mid, Color("#f2c66d"), thickness)
		draw_line(mid, landing, Color("#f2c66d"), thickness * 0.9)
		for blip in range(3):
			var blip_t := fmod(pour_tilt * 8.0 + float(blip) * 0.33, 1.0)
			draw_circle(spout.lerp(landing, blip_t) + Vector2(4.0, 0.0), 4.0, Color("#f7dfa0"))
		# a bulge where the stream lands
		draw_circle(landing, thickness * 0.9, Color(0.95, 0.80, 0.45, 0.7))
	# near-empty: fat last drips
	if pour_reserve < 0.18 and _pour_stream_active():
		draw_circle(_pour_spout_point() + Vector2(0.0, 14.0), 6.0, Color("#f2c66d"))
