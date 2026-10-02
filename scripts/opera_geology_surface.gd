class_name OperaGeologySurface
extends OperaGestureSurface
## Full-canvas, one-finger geology work. Each mode changes the pictured
## material under the finger and emits one completion unit exactly once.

signal progress_changed(snapshot: Dictionary)

const SUPPORTED_MODES: Array[String] = [
	"geology_river", "geology_fossil", "geology_pan", "geology_geode",
]
const WORK_RECT := Rect2(330.0, 130.0, 860.0, 490.0)
const RIVER_GRID_ORIGIN := Vector2(360.0, 180.0)
const RIVER_CELL := Vector2(88.0, 76.0)
const RIVER_COLS := 9
const RIVER_ROWS := 5
const RIVER_BRUSH_RADIUS := 46.0
const RIVER_PATH: Array[Vector2i] = [
	Vector2i(0, 2), Vector2i(1, 2), Vector2i(2, 2), Vector2i(2, 1),
	Vector2i(3, 1), Vector2i(4, 1), Vector2i(4, 2), Vector2i(4, 3),
	Vector2i(5, 3), Vector2i(6, 3), Vector2i(6, 2), Vector2i(7, 2),
	Vector2i(8, 2),
]
const FOSSIL_SOIL_WIDTH := 300.0 * 881.0 / 684.0
const FOSSIL_RECT := Rect2(780.0 - FOSSIL_SOIL_WIDTH * 0.5, 215.0, FOSSIL_SOIL_WIDTH, 300.0)
const FOSSIL_ART_WIDTH := 234.0 * 802.0 / 674.0
const FOSSIL_TARGET_RECT := Rect2(805.0 - FOSSIL_ART_WIDTH * 0.5, 205.0, FOSSIL_ART_WIDTH, 234.0)
const FOSSIL_GRID_COLS := 8
const FOSSIL_GRID_ROWS := 5
const FOSSIL_REQUIRED_CELLS := 26
const FOSSIL_BRUSH_RADIUS := 44.0
const FOSSIL_PIECE_SIZE := Vector2(FOSSIL_ART_WIDTH / 3.0, 234.0)
const PAN_RECT := Rect2(520.0, 220.0, 520.0, 320.0)
const PAN_REQUIRED_REVERSALS := 9
const PAN_RUN_DISTANCE := 46.0
const GEODE_RECT := Rect2(550.0, 165.0, 440.0, 350.0)
const GEODE_PULL_DISTANCE := 120.0
const GEODE_SEAM_RADIUS := 56.0
const GEODE_SEAM_SPOTS: Array[Vector2] = [
	Vector2(766.0, 216.0), Vector2(735.0, 278.0), Vector2(778.0, 340.0),
	Vector2(744.0, 401.0), Vector2(770.0, 466.0),
]
## Painted geology props share reviewed source art and measured alpha regions.
## Painted river regions retain separate room, actor and complete-action reviews.
const WORK_ART := "res://assets/opera/worlds/geology/painted_work_v1_20261001/"
const FOSSIL_PATH := WORK_ART + "fossil.png"
const GEODE_ART := "res://assets/opera/worlds/geology/coherent_geode_v1_20261002/"
const GEODE_STATE_PATHS: Array[String] = [
	GEODE_ART + "opening_six_states.png",
	GEODE_ART + "opening_six_states.png",
	GEODE_ART + "opening_six_states.png",
	GEODE_ART + "opening_bridge.png",
	GEODE_ART + "opening_six_states.png",
	GEODE_ART + "opening_six_states.png",
	GEODE_ART + "opening_six_states.png",
]
const GEODE_STATE_REGIONS: Array[Rect2] = [
	Rect2(96.974069898534, 68.112739571590, 473.325817361894, 421.375422773393),
	Rect2(773.483652762120, 64.649379932356, 481.406989853439, 425.993235625705),
	Rect2(1448.838782412627, 76.193912063134, 524.121758737317, 416.757609921082),
	Rect2(1077.104847801578, 202.029312288613, 895.855693348365, 668.428410372041),
	Rect2(45.023675310034, 562.218714768884, 573.763246899662, 384.432919954904),
	Rect2(714.606538895152, 556.446448703495, 602.624577226607, 391.359639233371),
	Rect2(1392.270574971815, 556.446448703495, 617.632468996618, 393.668545659527),
]
const ROCK_PATH := WORK_ART + "layered_rock.png"
const BRUSH_PATH := "res://assets/castle/day_one_art_studio/magic_cleaning_brush.png"
const PAN_PATH := WORK_ART + "pan.png"
const CRYSTALS_PATH := WORK_ART + "mineral.png"
const RIVER_ART := "res://assets/opera/worlds/geology/painted_river_v1_20261002/"
const RIVER_NATIVE_TO_RUNTIME := 1024.0 / 1254.0

var fossil_texture: Texture2D = null
var geode_texture: Texture2D = null
var _geode_states: Array[Texture2D] = []
var rock_texture: Texture2D = null
var brush_texture: Texture2D = null
var pan_texture: Texture2D = null
var crystals_texture: Texture2D = null
var _work_slab_texture: Texture2D = null
var _pan_grain_texture: Texture2D = null
var _fossil_soil_texture: Texture2D = null
var _river_source_textures: Dictionary = {}
var _river_atlas_regions: Dictionary = {}
var _river_dry_circle: Texture2D = null
var _river_wet_circle: Texture2D = null
var _river_earth: Texture2D = null

var touch_owner := -1
var river_wet: Array[bool] = []
var fossil_cleared: Array[bool] = []
var fossil_stage := 0
var fossil_snapped: Array[bool] = [false, false, false]
var fossil_drag_piece := -1
var fossil_drag_position := Vector2.ZERO
var pan_reversals := 0
var pan_wash := 0.0
var pan_minerals := 0
var pan_last_direction := 0
var pan_run_distance := 0.0
var pan_visual_x := 0.0
var geode_seams: Array[bool] = [false, false, false, false, false]
var geode_tap_candidate := -1
var geode_dragging := false
var geode_pull := 0.0
var geode_pull_start := 0.0
var _press_position := Vector2.ZERO
var _last_position := Vector2.ZERO
var _completion_emitted := false
var _restored_completion_pending := false
var _redraw_t := 0.0


func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	assert(next_mode in SUPPORTED_MODES,
		"OperaGeologySurface supports only its four geology modes")
	super.configure(next_mode, next_accent, choice, next_context)
	_load_textures()
	touch_owner = -1
	river_wet.resize(RIVER_COLS * RIVER_ROWS)
	river_wet.fill(false)
	fossil_cleared.resize(FOSSIL_GRID_COLS * FOSSIL_GRID_ROWS)
	fossil_cleared.fill(false)
	fossil_stage = 0
	fossil_snapped = [false, false, false]
	fossil_drag_piece = -1
	fossil_drag_position = Vector2.ZERO
	pan_reversals = 0
	pan_wash = 0.0
	pan_minerals = 0
	pan_last_direction = 0
	pan_run_distance = 0.0
	pan_visual_x = 0.0
	geode_seams = [false, false, false, false, false]
	geode_tap_candidate = -1
	geode_dragging = false
	geode_pull = 0.0
	geode_pull_start = 0.0
	_completion_emitted = false
	_restored_completion_pending = false
	_redraw_t = 0.0
	held = false
	demo_active = true
	demo_t = 0.0
	queue_redraw()


func stage_name() -> String:
	match mode:
		"geology_river":
			return "RIVER"
		"geology_fossil":
			return "FOSSIL_BRUSH" if fossil_stage == 0 else "FOSSIL_ASSEMBLE"
		"geology_pan":
			return "PAN"
		"geology_geode":
			return "GEODE_SEAM" if _seam_count() < GEODE_SEAM_SPOTS.size() else "GEODE_OPEN"
	return ""


func progress() -> float:
	match mode:
		"geology_river":
			if _river_connected():
				return 1.0
			return minf(0.95, float(river_wet.count(true)) / float(RIVER_PATH.size()))
		"geology_fossil":
			if fossil_stage == 0:
				return 0.5 * minf(1.0,
					float(_cleared_count()) / float(FOSSIL_REQUIRED_CELLS))
			return 0.5 + 0.5 * float(_snapped_count()) / 3.0
		"geology_pan":
			return pan_wash
		"geology_geode":
			if _seam_count() < GEODE_SEAM_SPOTS.size():
				return 0.6 * float(_seam_count()) / float(GEODE_SEAM_SPOTS.size())
			return 0.6 + 0.4 * clampf(geode_pull / GEODE_PULL_DISTANCE, 0.0, 1.0)
	return 0.0


func river_path_point(index: int) -> Vector2:
	var cell := RIVER_PATH[clampi(index, 0, RIVER_PATH.size() - 1)]
	return RIVER_GRID_ORIGIN + (Vector2(cell) + Vector2(0.5, 0.5)) * RIVER_CELL


func fossil_piece_home(index: int) -> Vector2:
	return Vector2(500.0 + float(clampi(index, 0, 2)) * 245.0, 450.0)


func fossil_piece_target(index: int) -> Vector2:
	var third := FOSSIL_TARGET_RECT.size.x / 3.0
	return FOSSIL_TARGET_RECT.position + Vector2(
		third * (float(clampi(index, 0, 2)) + 0.5), FOSSIL_TARGET_RECT.size.y * 0.5)


func geode_seam_spot(index: int) -> Vector2:
	return GEODE_SEAM_SPOTS[clampi(index, 0, GEODE_SEAM_SPOTS.size() - 1)]


func geode_half_center() -> Vector2:
	return _geode_right_rect().get_center()


func progress_snapshot() -> Dictionary:
	var snapshot := {"version": 1, "mode": mode, "stage": stage_name(),
		"complete": _completion_emitted}
	match mode:
		"geology_river":
			snapshot["wet"] = _true_indices(river_wet)
		"geology_fossil":
			snapshot["cleared"] = _true_indices(fossil_cleared)
			snapshot["fossil_stage"] = fossil_stage
			snapshot["snapped"] = fossil_snapped.duplicate()
		"geology_pan":
			snapshot["reversals"] = pan_reversals
			snapshot["wash"] = pan_wash
			snapshot["minerals"] = pan_minerals
		"geology_geode":
			snapshot["seams"] = geode_seams.duplicate()
			snapshot["pull"] = geode_pull
	return snapshot


func restore_progress(snapshot: Dictionary) -> void:
	if String(snapshot.get("mode", "")) != mode:
		return
	match mode:
		"geology_river":
			_restore_true_indices(river_wet, snapshot.get("wet", []))
		"geology_fossil":
			_restore_true_indices(fossil_cleared, snapshot.get("cleared", []))
			fossil_stage = 1 if _cleared_count() >= FOSSIL_REQUIRED_CELLS else 0
			_restore_bools(fossil_snapped, snapshot.get("snapped", []))
			if fossil_stage == 0:
				fossil_snapped.fill(false)
		"geology_pan":
			var saved_reversals: Variant = snapshot.get("reversals", 0)
			pan_reversals = clampi(int(saved_reversals), 0, PAN_REQUIRED_REVERSALS) \
				if _is_number(saved_reversals) else 0
			pan_wash = float(pan_reversals) / float(PAN_REQUIRED_REVERSALS)
			pan_minerals = mini(3, floori(pan_wash * 3.0 + 0.001))
		"geology_geode":
			_restore_bools(geode_seams, snapshot.get("seams", []))
			var saved_pull: Variant = snapshot.get("pull", 0.0)
			geode_pull = clampf(float(saved_pull), 0.0, GEODE_PULL_DISTANCE) \
				if _is_number(saved_pull) and _seam_count() == GEODE_SEAM_SPOTS.size() \
				else 0.0
	_completion_emitted = false
	_restored_completion_pending = progress() >= 0.999
	widget_fill = progress()
	demo_active = not _restored_completion_pending
	cancel_input(false)
	queue_redraw()


func cancel_input(emit_checkpoint := true) -> void:
	held = false
	touch_owner = -1
	fossil_drag_piece = -1
	pan_last_direction = 0
	pan_run_distance = 0.0
	pan_visual_x = 0.0
	geode_tap_candidate = -1
	geode_dragging = false
	if emit_checkpoint:
		_emit_checkpoint()
	queue_redraw()


func restart_demo() -> void:
	if completion_accepted or _completion_emitted:
		return
	demo_active = true
	demo_t = 0.0
	queue_redraw()


func _load_textures() -> void:
	fossil_texture = _geode_atlas(FOSSIL_PATH, Rect2(115, 171, 802, 674))
	_geode_states.clear()
	geode_texture = null
	if mode == "geology_geode":
		for index: int in range(GEODE_STATE_PATHS.size()):
			_geode_states.append(_geode_atlas(GEODE_STATE_PATHS[index],
				GEODE_STATE_REGIONS[index]))
		geode_texture = _geode_states[0]
	rock_texture = _geode_atlas(ROCK_PATH, Rect2(120, 188, 800, 674))
	brush_texture = _optional_texture(BRUSH_PATH)
	pan_texture = _geode_atlas(PAN_PATH, Rect2(44, 75, 936, 455))
	crystals_texture = _geode_atlas(CRYSTALS_PATH, Rect2(231, 130, 569, 767))
	_work_slab_texture = _geode_atlas(WORK_ART + "work_slab.png", Rect2(68, 332, 889, 369))
	_pan_grain_texture = _geode_atlas(WORK_ART + "grain.png", Rect2(228, 120, 569, 439))
	_fossil_soil_texture = _geode_atlas(WORK_ART + "fossil_soil.png", Rect2(72, 171, 881, 684))
	_river_atlas_regions.clear()
	_river_source_textures.clear()
	_river_dry_circle = null
	_river_wet_circle = null
	_river_earth = null
	if mode == "geology_river":
		_river_earth = _optional_texture(RIVER_ART + "earth_bed.png")
		_river_dry_circle = _river_region("nodes.png", Rect2(44, 167, 560, 547))
		_river_wet_circle = _river_region("nodes.png", Rect2(655, 167, 560, 547))



func _optional_texture(path: String) -> Texture2D:
	return load(path) as Texture2D if not path.is_empty() and ResourceLoader.exists(path) else null


func _input_blocked() -> bool:
	return armed_only or completion_accepted or _completion_emitted


func _press(at: Vector2) -> void:
	if _input_blocked():
		return
	held = true
	input_started = true
	demo_active = false
	pointer_pos = at
	previous_pos = at
	_press_position = at
	_last_position = at
	match mode:
		"geology_fossil":
			if fossil_stage == 1:
				fossil_drag_piece = _piece_at(at)
				if fossil_drag_piece >= 0:
					fossil_drag_position = at
		"geology_pan":
			if not PAN_RECT.grow(36.0).has_point(at):
				pan_last_direction = 0
		"geology_geode":
			if _seam_count() < GEODE_SEAM_SPOTS.size():
				geode_tap_candidate = _seam_at(at)
			elif _geode_right_rect().grow(30.0).has_point(at):
				geode_dragging = true
				geode_pull_start = geode_pull
	queue_redraw()


func _drag(at: Vector2) -> void:
	if not held or _input_blocked():
		return
	pointer_pos = at
	var travel := _last_position.distance_to(at)
	if travel < 2.0:
		return
	match mode:
		"geology_river":
			_river_stroke(_last_position, at)
		"geology_fossil":
			if fossil_stage == 0:
				_fossil_brush(_last_position, at)
			elif fossil_drag_piece >= 0:
				fossil_drag_position = at.clamp(WORK_RECT.position, WORK_RECT.end)
		"geology_pan":
			_pan_drag(_last_position, at)
		"geology_geode":
			_geode_drag(at)
	_last_position = at
	previous_pos = at
	queue_redraw()


func _release(at: Vector2) -> void:
	if not held:
		touch_owner = -1
		return
	pointer_pos = at
	if mode == "geology_fossil" and fossil_drag_piece >= 0:
		var target := fossil_piece_target(fossil_drag_piece)
		if at.distance_to(target) <= 92.0:
			fossil_snapped[fossil_drag_piece] = true
			_emit_checkpoint()
			if _snapped_count() == 3:
				_complete_mode()
		fossil_drag_piece = -1
	elif mode == "geology_geode" and not geode_dragging \
			and geode_tap_candidate >= 0 \
			and _press_position.distance_to(at) <= 34.0 \
			and at.distance_to(geode_seam_spot(geode_tap_candidate)) \
				<= GEODE_SEAM_RADIUS:
		geode_seams[geode_tap_candidate] = true
		_emit_checkpoint()
	held = false
	touch_owner = -1
	pan_last_direction = 0
	pan_run_distance = 0.0
	pan_visual_x = 0.0
	geode_tap_candidate = -1
	geode_dragging = false
	_emit_checkpoint()
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed and touch_owner == -1 and not _input_blocked():
			touch_owner = touch.index
			_press(touch.position)
		elif not touch.pressed and touch.index == touch_owner:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == touch_owner:
			_drag(drag.position)
		accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION \
				or button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed and touch_owner == -1 and not _input_blocked():
			touch_owner = -2
			_press(button.position)
		elif not button.pressed and touch_owner == -2:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and touch_owner == -2:
		var motion := event as InputEventMouseMotion
		if motion.device != InputEvent.DEVICE_ID_EMULATION:
			_drag(motion.position)
			accept_event()


func _notification(what: int) -> void:
	if what in [NOTIFICATION_PAUSED, NOTIFICATION_APPLICATION_PAUSED,
			NOTIFICATION_APPLICATION_FOCUS_OUT]:
		cancel_input()


func _process(delta: float) -> void:
	if _restored_completion_pending and not armed_only:
		_restored_completion_pending = false
		_complete_mode()
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - delta)
	if demo_active and not _input_blocked():
		demo_t += maxf(0.0, delta)
	_redraw_t += maxf(0.0, delta)
	if _redraw_t >= 0.05:
		_redraw_t = 0.0
		queue_redraw()


func _river_stroke(from: Vector2, to: Vector2) -> void:
	var changed := false
	for index in range(RIVER_COLS * RIVER_ROWS):
		var path_cell := Vector2i(index % RIVER_COLS, index / RIVER_COLS)
		if river_wet[index]:
			continue
		var nearest := Geometry2D.get_closest_point_to_segment(
			river_path_cell_center(path_cell), from, to)
		if nearest.distance_to(river_path_cell_center(path_cell)) <= RIVER_BRUSH_RADIUS:
			river_wet[index] = true
			changed = true
	if changed:
		_note_material_change(to)
		if _river_connected():
			_complete_mode()


func river_path_cell_center(cell: Vector2i) -> Vector2:
	return RIVER_GRID_ORIGIN + (Vector2(cell) + Vector2(0.5, 0.5)) * RIVER_CELL


func _river_connected() -> bool:
	var start := RIVER_PATH[0]
	var finish := RIVER_PATH[-1]
	var start_index := start.y * RIVER_COLS + start.x
	if not river_wet[start_index]:
		return false
	var open: Array[Vector2i] = [start]
	var seen := {start_index: true}
	while not open.is_empty():
		var cell: Vector2i = open.pop_front()
		if cell == finish:
			return true
		for step: Vector2i in [Vector2i.LEFT, Vector2i.RIGHT,
				Vector2i.UP, Vector2i.DOWN]:
			var next := cell + step
			if next.x < 0 or next.y < 0 or next.x >= RIVER_COLS \
					or next.y >= RIVER_ROWS:
				continue
			var index := next.y * RIVER_COLS + next.x
			if river_wet[index] and not seen.has(index):
				seen[index] = true
				open.append(next)
	return false


func _fossil_brush(from: Vector2, to: Vector2) -> void:
	var changed := false
	var cell_size := Vector2(FOSSIL_RECT.size.x / float(FOSSIL_GRID_COLS),
		FOSSIL_RECT.size.y / float(FOSSIL_GRID_ROWS))
	for row in range(FOSSIL_GRID_ROWS):
		for column in range(FOSSIL_GRID_COLS):
			var index := row * FOSSIL_GRID_COLS + column
			if fossil_cleared[index]:
				continue
			var center := FOSSIL_RECT.position \
				+ (Vector2(column, row) + Vector2(0.5, 0.5)) * cell_size
			var nearest := Geometry2D.get_closest_point_to_segment(center, from, to)
			if center.distance_to(nearest) <= FOSSIL_BRUSH_RADIUS:
				fossil_cleared[index] = true
				changed = true
	if changed:
		if _cleared_count() >= FOSSIL_REQUIRED_CELLS:
			fossil_stage = 1
		_note_material_change(to)


func _piece_at(at: Vector2) -> int:
	for index in range(3):
		if fossil_snapped[index]:
			continue
		var rect := Rect2(fossil_piece_home(index) - FOSSIL_PIECE_SIZE * 0.5,
			FOSSIL_PIECE_SIZE)
		if rect.grow(24.0).has_point(at):
			return index
	return -1


func _pan_drag(from: Vector2, to: Vector2) -> void:
	if not PAN_RECT.grow(42.0).has_point(from):
		return
	var dx := to.x - from.x
	if absf(dx) < 4.0:
		return
	pan_visual_x = clampf(pan_visual_x + dx * 0.35, -70.0, 70.0)
	var direction := 1 if dx > 0.0 else -1
	if pan_last_direction == 0:
		pan_last_direction = direction
		pan_run_distance = absf(dx)
	elif direction == pan_last_direction:
		pan_run_distance += absf(dx)
	else:
		if pan_run_distance >= PAN_RUN_DISTANCE:
			pan_reversals = mini(PAN_REQUIRED_REVERSALS, pan_reversals + 1)
			pan_wash = float(pan_reversals) / float(PAN_REQUIRED_REVERSALS)
			pan_minerals = mini(3, floori(pan_wash * 3.0 + 0.001))
			_note_material_change(to)
			if pan_reversals >= PAN_REQUIRED_REVERSALS:
				_complete_mode()
		pan_last_direction = direction
		pan_run_distance = absf(dx)


func _geode_drag(at: Vector2) -> void:
	if not geode_dragging or _seam_count() < GEODE_SEAM_SPOTS.size():
		return
	var next_pull := clampf(geode_pull_start + at.x - _press_position.x,
		0.0, GEODE_PULL_DISTANCE)
	if next_pull <= geode_pull + 1.0:
		return
	geode_pull = next_pull
	_note_material_change(at)
	if geode_pull >= GEODE_PULL_DISTANCE:
		_complete_mode()


func _seam_at(at: Vector2) -> int:
	for index in range(GEODE_SEAM_SPOTS.size()):
		if not geode_seams[index] \
				and at.distance_to(GEODE_SEAM_SPOTS[index]) <= GEODE_SEAM_RADIUS:
			return index
	return -1


func _geode_state_index() -> int:
	if geode_pull <= 0.0:
		return 0
	return mini(6, 1 + int(geode_pull / 20.0))


func _geode_right_rect() -> Rect2:
	if not _geode_states.is_empty():
		var pair := _geode_pair_rect(_geode_states[_geode_state_index()], 350.0)
		return Rect2(Vector2(pair.get_center().x, pair.position.y),
			Vector2(pair.size.x * 0.5, pair.size.y))
	return Rect2(Vector2(GEODE_RECT.get_center().x, GEODE_RECT.position.y),
		Vector2(GEODE_RECT.size.x * 0.5, GEODE_RECT.size.y))

func _note_material_change(at: Vector2) -> void:
	widget_fill = progress()
	feedback_positive = true
	feedback_t = 0.24
	feedback_anchor = at
	input_started = true
	demo_active = false
	_emit_checkpoint()
	queue_redraw()


func _complete_mode() -> void:
	if _completion_emitted:
		return
	_completion_emitted = true
	widget_fill = 1.0
	held = false
	touch_owner = -1
	gesture.emit(mode, 1.0, 1.0)
	_emit_checkpoint()
	queue_redraw()


func _emit_checkpoint() -> void:
	progress_changed.emit(progress_snapshot())


func _wet_path_count() -> int:
	var count := 0
	for cell: Vector2i in RIVER_PATH:
		if river_wet[cell.y * RIVER_COLS + cell.x]:
			count += 1
	return count


func _cleared_count() -> int:
	return fossil_cleared.count(true)


func _snapped_count() -> int:
	return fossil_snapped.count(true)


func _seam_count() -> int:
	return geode_seams.count(true)


func _true_indices(values: Array[bool]) -> Array[int]:
	var indices: Array[int] = []
	for index in range(values.size()):
		if values[index]:
			indices.append(index)
	return indices


func _restore_true_indices(values: Array[bool], source: Variant) -> void:
	values.fill(false)
	if not source is Array:
		return
	var indices := source as Array
	for raw_index: Variant in indices:
		if typeof(raw_index) not in [TYPE_INT, TYPE_FLOAT]:
			continue
		var numeric_index := float(raw_index)
		if not is_finite(numeric_index) or numeric_index != floorf(numeric_index):
			continue
		var index := int(numeric_index)
		if index >= 0 and index < values.size():
			values[index] = true


func _restore_bools(values: Array[bool], raw_source: Variant) -> void:
	values.fill(false)
	if not raw_source is Array:
		return
	var source := raw_source as Array
	for index in range(mini(values.size(), source.size())):
		if typeof(source[index]) == TYPE_BOOL:
			values[index] = bool(source[index])


func _is_number(value: Variant) -> bool:
	return typeof(value) in [TYPE_INT, TYPE_FLOAT] and is_finite(float(value))


func _draw() -> void:
	_draw_work_surface()
	match mode:
		"geology_river":
			_draw_river()
		"geology_fossil":
			_draw_fossil()
		"geology_pan":
			_draw_pan()
		"geology_geode":
			_draw_geode()
	if feedback_t > 0.0:
		draw_circle(feedback_anchor, 22.0 + feedback_t * 28.0,
			Color(1.0, 0.91, 0.48, feedback_t))
	if demo_active and not armed_only and not _completion_emitted:
		_draw_demo_finger()


func _river_region(source_name: String, native_rect: Rect2) -> Texture2D:
	var key := source_name + str(native_rect)
	if _river_atlas_regions.has(key):
		return _river_atlas_regions[key] as Texture2D
	if not _river_source_textures.has(source_name):
		_river_source_textures[source_name] = _optional_texture(RIVER_ART + source_name)
	var source := _river_source_textures[source_name] as Texture2D
	if source == null:
		return null
	var atlas := AtlasTexture.new()
	atlas.atlas = source
	atlas.region = Rect2(native_rect.position * RIVER_NATIVE_TO_RUNTIME,
		native_rect.size * RIVER_NATIVE_TO_RUNTIME)
	_river_atlas_regions[key] = atlas
	return atlas


func _draw_river_circle_art(center: Vector2, wet: bool, width_now: float) -> void:
	var art := _river_wet_circle if wet else _river_dry_circle
	if art == null:
		return
	var size_now := Vector2(width_now,width_now * art.get_height() / float(art.get_width()))
	draw_texture_rect(art,Rect2(center-size_now*0.5,size_now),false)

func _river_neighbor_mask(cell: Vector2i) -> int:
	var result := 0
	var steps: Array[Vector2i] = [Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP]
	for bit: int in range(4):
		var next := cell + steps[bit]
		if next.x >= 0 and next.x < RIVER_COLS and next.y >= 0 and next.y < RIVER_ROWS \
				and river_wet[next.y * RIVER_COLS + next.x]:
			result |= 1 << bit
	return result

func _draw_river_field(center: Vector2, kind: String, angle: float, wet: bool) -> void:
	var source_path := "wet_junctions.png" if wet else "dry_junctions.png"
	var anchor := Vector2(941.0,915.5)
	var pixel_scale := 0.18
	if kind == "elbow":
		anchor = Vector2(889.0,407.0)
	elif kind == "tee":
		anchor = Vector2(317.0,963.0)
	var turned := not is_zero_approx(sin(angle))
	var extent := Vector2(76.0,88.0) if turned else Vector2(88.0,76.0)
	var region_now := Rect2(anchor - extent * 0.5 / pixel_scale,extent / pixel_scale)
	if kind == "endcap":
		anchor = Vector2(345.5555556,345.0)
		pixel_scale = 0.18
		# Keep the complete closed bowl; only its open right stub ends on its port plane.
		region_now = Rect2(53.0,119.0,anchor.x + extent.x * 0.5 / pixel_scale - 53.0,423.0)
	elif kind == "straight":
		source_path = "wet_straight.png" if wet else "dry_straight.png"
		var height_now := 302.0 if wet else 300.0
		var source_y := 734.0 if wet else 310.0
		pixel_scale = extent.x / 586.0
		region_now = Rect2(334.5,source_y,586.0,height_now)
		anchor = region_now.get_center()
	var art := _river_region(source_path,region_now)
	if art == null:
		return
	draw_set_transform(center,angle)
	draw_texture_rect(art,Rect2((region_now.position-anchor)*pixel_scale,
		region_now.size*pixel_scale),false)
	draw_set_transform(Vector2.ZERO)

func _draw_river() -> void:
	var flowing := _river_flow_indices()
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS,index / RIVER_COLS)
		var center := river_path_cell_center(cell)
		var mask := _river_neighbor_mask(cell)
		var wet := flowing.has(index)
		if mask == 0:
			_draw_river_circle_art(center,wet,60.0)
		elif mask in [1,2,4,8]:
			var angle := 0.0 if mask == 1 else PI*0.5 if mask == 2 else PI if mask == 4 else -PI*0.5
			_draw_river_field(center,"endcap",angle,wet)
		elif mask in [5,10]:
			_draw_river_field(center,"straight",0.0 if mask == 5 else PI*0.5,wet)
		elif mask in [9,3,6,12]:
			var angle := 0.0 if mask == 9 else PI*0.5 if mask == 3 else PI if mask == 6 else -PI*0.5
			_draw_river_field(center,"elbow",angle,wet)
		elif mask in [13,11,7,14]:
			var angle := 0.0 if mask == 13 else PI*0.5 if mask == 11 else PI if mask == 7 else -PI*0.5
			_draw_river_field(center,"tee",angle,wet)
		else:
			assert(mask == 15)
			_draw_river_field(center,"cross",0.0,wet)
	if not river_wet[RIVER_PATH[0].y * RIVER_COLS + RIVER_PATH[0].x]:
		_draw_river_circle_art(river_path_point(0),true,86.0)
	if not river_wet[RIVER_PATH[-1].y * RIVER_COLS + RIVER_PATH[-1].x]:
		_draw_river_circle_art(river_path_point(RIVER_PATH.size()-1),false,94.0)
	if held:
		_draw_brush(pointer_pos)


func _river_flow_indices() -> Dictionary:
	var start := RIVER_PATH[0]
	var start_index := start.y * RIVER_COLS + start.x
	if not river_wet[start_index]:
		return {}
	var open: Array[Vector2i] = [start]
	var seen := {start_index: true}
	while not open.is_empty():
		var cell: Vector2i = open.pop_front()
		for step: Vector2i in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var next := cell + step
			if next.x < 0 or next.y < 0 or next.x >= RIVER_COLS or next.y >= RIVER_ROWS:
				continue
			var index := next.y * RIVER_COLS + next.x
			if river_wet[index] and not seen.has(index):
				seen[index] = true
				open.append(next)
	return seen


func _draw_fossil() -> void:
	if fossil_stage == 0:
		_draw_fossil_whole(FOSSIL_RECT.grow(-24.0), Color(1, 1, 1, 0.62))
		var cell_size := Vector2(FOSSIL_RECT.size.x / float(FOSSIL_GRID_COLS),
			FOSSIL_RECT.size.y / float(FOSSIL_GRID_ROWS))
		for row in range(FOSSIL_GRID_ROWS):
			for column in range(FOSSIL_GRID_COLS):
				var index := row * FOSSIL_GRID_COLS + column
				if not fossil_cleared[index]:
					if _fossil_soil_texture != null:
						var source_cell := _fossil_soil_texture.get_size() \
							/ Vector2(FOSSIL_GRID_COLS, FOSSIL_GRID_ROWS)
						draw_texture_rect_region(_fossil_soil_texture,
							Rect2(FOSSIL_RECT.position + Vector2(column, row) * cell_size,
								cell_size), Rect2(Vector2(column, row) * source_cell, source_cell))
		if held:
			_draw_brush(pointer_pos)
		return
	_draw_fossil_whole(FOSSIL_TARGET_RECT, Color(1, 1, 1, 0.22))
	for index in range(3):
		var center := fossil_piece_target(index) if fossil_snapped[index] \
			else fossil_piece_home(index)
		if fossil_drag_piece == index:
			center = fossil_drag_position
		_draw_fossil_piece(index,
			Rect2(center - FOSSIL_PIECE_SIZE * 0.5, FOSSIL_PIECE_SIZE))


func _draw_fossil_whole(rect: Rect2, tint: Color) -> void:
	if fossil_texture != null:
		var scale_factor := minf(rect.size.x / fossil_texture.get_width(),
			rect.size.y / fossil_texture.get_height())
		var fit_size := fossil_texture.get_size() * scale_factor
		draw_texture_rect(fossil_texture, Rect2(rect.get_center() - fit_size * 0.5,
			fit_size), false, tint)
	else:
		draw_arc(rect.get_center(), minf(rect.size.x, rect.size.y) * 0.38,
			0.0, TAU * 1.8, 54, Color("#f5ddaa", tint.a), 30.0, true)


func _draw_fossil_piece(index: int, rect: Rect2) -> void:
	if fossil_texture != null:
		var source_size := fossil_texture.get_size()
		var third := source_size.x / 3.0
		draw_texture_rect_region(fossil_texture, rect,
			Rect2(Vector2(third * float(index), 0.0),
				Vector2(third, source_size.y)))
	else:
		draw_arc(rect.get_center(), rect.size.x * 0.34,
			float(index) * 1.8, float(index + 1) * 1.8,
			18, Color("#f8dca1"), 24.0, true)


func _draw_brush(at: Vector2) -> void:
	if brush_texture != null:
		# The approved brush is diagonal. Its bristle contact, not the middle of
		# its canvas, follows the same point as the excavation gesture.
		var brush_size := Vector2(156.0, 156.0 * brush_texture.get_height() / brush_texture.get_width())
		draw_texture_rect(brush_texture,
			Rect2(at - brush_size * Vector2(0.25, 0.78), brush_size), false)
	else:
		var axis := Vector2(1.0, 1.0).normalized()
		var normal := Vector2(-axis.y, axis.x)
		var bristle_root := at - axis * 8.0
		var bristle_tip := at - axis * 48.0
		var bristles := PackedVector2Array([
			bristle_root - normal * 18.0,
			bristle_root + normal * 18.0,
			bristle_tip + normal * 28.0,
			bristle_tip + normal * 18.0,
			bristle_tip,
			bristle_tip - normal * 18.0,
			bristle_tip - normal * 28.0,
		])
		draw_colored_polygon(bristles, Color("#8fe3dc"))
		var bristle_outline := bristles.duplicate()
		bristle_outline.append(bristles[0])
		draw_polyline(bristle_outline, Color("#392958"), 8.0, true)
		var ferrule_center := bristle_root + axis * 8.0
		draw_line(ferrule_center - normal * 22.0, ferrule_center + normal * 22.0,
			Color("#e9b963"), 16.0, true)
		draw_line(bristle_root + axis * 13.0, at + axis * 52.0,
			Color("#392958"), 23.0, true)
		draw_line(bristle_root + axis * 13.0, at + axis * 52.0,
			Color("#b97852"), 13.0, true)
		draw_circle(at + axis * 53.0, 10.0, Color("#e9b963"))
		draw_circle(at + axis * 53.0, 4.0, Color("#72e0d3"))


func _draw_pan() -> void:
	if pan_texture == null or _pan_grain_texture == null or crystals_texture == null:
		return
	var ratio := pan_texture.get_width() / float(pan_texture.get_height())
	var fit_size := Vector2(PAN_RECT.size.x, PAN_RECT.size.x / ratio)
	var rect := Rect2(PAN_RECT.get_center() + Vector2(pan_visual_x, 0.0)
		- fit_size * 0.5, fit_size)
	draw_texture_rect(pan_texture, rect, false)
	var water_center := rect.position + fit_size * Vector2(0.50, 0.44)
	var grain_count := maxi(3, 20 - floori(pan_wash * 17.0))
	for index in range(grain_count):
		var angle := float(index) * 2.399
		var radial := sqrt((float(index) + 0.5) / float(grain_count))
		var grain_pos := water_center \
			+ Vector2(cos(angle) * 122.0, sin(angle) * 31.0) * radial
		grain_pos.x += pan_visual_x * 0.12 \
			+ sin(float(index) + pan_visual_x * 0.02) * 6.0
		var grain_size := Vector2(15.0 * _pan_grain_texture.get_width()
			/ float(_pan_grain_texture.get_height()), 15.0)
		draw_texture_rect(_pan_grain_texture,
			Rect2(grain_pos - grain_size * 0.5, grain_size), false)
	for index in range(pan_minerals):
		var mineral_size := Vector2(68.0 * crystals_texture.get_width()
			/ float(crystals_texture.get_height()), 68.0)
		var base := water_center + Vector2(-82.0 + float(index) * 82.0, 20.0)
		_draw_ellipse(base + Vector2(0.0, -2.0), Vector2(24.0, 6.0),
			Color(0.22, 0.60, 0.65, 0.35), Color(0.57, 0.89, 0.88, 0.72), 2.0)
		draw_texture_rect(crystals_texture,
			Rect2(base - Vector2(mineral_size.x * 0.5, mineral_size.y),
				mineral_size), false)


func _geode_atlas(path: String, region: Rect2) -> Texture2D:
	var texture := _optional_texture(path)
	if texture == null:
		push_error("Missing painted geology source: " + path)
		return null
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = region
	return atlas


func _geode_pair_rect(texture: Texture2D, height: float) -> Rect2:
	var size := Vector2(height * texture.get_width() / float(texture.get_height()), height)
	var center := Vector2(GEODE_RECT.get_center().x,
		GEODE_RECT.end.y - height * 0.5)
	return Rect2(center - size * 0.5, size)


func _draw_geode() -> void:
	if _geode_states.is_empty():
		return
	var texture := _geode_states[_geode_state_index()]
	# Every state includes both mineral cavities and their rooted crystals.
	draw_texture_rect(texture, _geode_pair_rect(texture, 350.0), false)
	if geode_pull <= 0.0:
		for index: int in range(GEODE_SEAM_SPOTS.size()):
			draw_circle(GEODE_SEAM_SPOTS[index], 15.0,
				Color("#8ce6dd") if geode_seams[index] else Color("#ffe69a"))

func _draw_work_surface() -> void:
	if mode == "geology_river" and _river_earth != null:
		draw_texture_rect(_river_earth,
			Rect2(Vector2(248.0, 114.0), Vector2(1024.0, 512.0)), false)
		return
	if mode != "geology_river" and _work_slab_texture != null:
		var slab_width := 900.0 if mode == "geology_fossil" else 860.0
		var slab_center := Vector2(760.0, 400.0)
		var slab_size := Vector2(slab_width, slab_width
			* _work_slab_texture.get_height() / float(_work_slab_texture.get_width()))
		draw_texture_rect(_work_slab_texture,
			Rect2(slab_center - slab_size * 0.5, slab_size), false)
		return
	var surface := Rect2(330.0, 130.0, 860.0, 560.0)
	_draw_rounded_rect(Rect2(surface.position + Vector2(0.0, 14.0),
		surface.size), 34.0,
		Color(0.12, 0.09, 0.22, 0.56), Color(0.12, 0.09, 0.22, 0.0), 0.0)
	_draw_rounded_rect(surface, 34.0, Color("#d4aa78"), Color("#392958"), 10.0)
	_draw_rounded_rect(Rect2(surface.position + Vector2(18.0, 18.0),
		surface.size - Vector2(36.0, 36.0)), 24.0,
		Color(0.93, 0.78, 0.56, 0.18), Color(0.93, 0.78, 0.56, 0.0), 0.0)


func _draw_rounded_rect(rect: Rect2, radius: float, fill: Color,
		outline: Color, outline_width: float) -> void:
	var r := minf(radius, minf(rect.size.x, rect.size.y) * 0.5)
	draw_rect(Rect2(rect.position + Vector2(r, 0.0),
		Vector2(rect.size.x - r * 2.0, rect.size.y)), fill, true)
	draw_rect(Rect2(rect.position + Vector2(0.0, r),
		Vector2(rect.size.x, rect.size.y - r * 2.0)), fill, true)
	for corner in [
		rect.position + Vector2(r, r),
		rect.position + Vector2(rect.size.x - r, r),
		rect.position + Vector2(rect.size.x - r, rect.size.y - r),
		rect.position + Vector2(r, rect.size.y - r),
	]:
		draw_circle(corner, r, fill)
	if outline_width <= 0.0 or outline.a <= 0.0:
		return
	draw_line(rect.position + Vector2(r, 0.0),
		rect.position + Vector2(rect.size.x - r, 0.0), outline, outline_width, true)
	draw_line(rect.position + Vector2(rect.size.x, r),
		rect.position + Vector2(rect.size.x, rect.size.y - r), outline,
		outline_width, true)
	draw_line(rect.position + Vector2(rect.size.x - r, rect.size.y),
		rect.position + Vector2(r, rect.size.y), outline, outline_width, true)
	draw_line(rect.position + Vector2(0.0, rect.size.y - r),
		rect.position + Vector2(0.0, r), outline, outline_width, true)
	draw_arc(rect.position + Vector2(r, r), r, PI, PI * 1.5, 12,
		outline, outline_width, true)
	draw_arc(rect.position + Vector2(rect.size.x - r, r), r, PI * 1.5, TAU, 12,
		outline, outline_width, true)
	draw_arc(rect.position + Vector2(rect.size.x - r, rect.size.y - r), r, 0.0,
		PI * 0.5, 12, outline, outline_width, true)
	draw_arc(rect.position + Vector2(r, rect.size.y - r), r, PI * 0.5, PI, 12,
		outline, outline_width, true)


func _draw_ellipse(center: Vector2, radii: Vector2, fill: Color,
		outline: Color, outline_width: float) -> void:
	var points := PackedVector2Array()
	for index in range(40):
		var angle := TAU * float(index) / 40.0
		points.append(center + Vector2(cos(angle) * radii.x, sin(angle) * radii.y))
	draw_colored_polygon(points, fill)
	if outline_width > 0.0 and outline.a > 0.0:
		var closed := points.duplicate()
		closed.append(points[0])
		draw_polyline(closed, outline, outline_width, true)


func _draw_mineral(center: Vector2, radius: float, color: Color) -> void:
	var points := PackedVector2Array([
		center + Vector2(-radius * 0.82, radius * 0.15),
		center + Vector2(-radius * 0.34, -radius * 0.78),
		center + Vector2(radius * 0.42, -radius * 0.60),
		center + Vector2(radius * 0.84, radius * 0.12),
		center + Vector2(radius * 0.18, radius * 0.80),
	])
	draw_colored_polygon(points, color)
	var closed := points.duplicate()
	closed.append(points[0])
	draw_polyline(closed, Color("#392958"), 6.0, true)
	draw_line(center + Vector2(-radius * 0.28, -radius * 0.55),
		center + Vector2(radius * 0.18, radius * 0.50),
		Color(1.0, 0.96, 0.70, 0.64), 4.0, true)


func _geode_half_points(seam_x: float, center_y: float, side: float,
		_unused: float) -> PackedVector2Array:
	var center := Vector2(seam_x, center_y)
	var points := PackedVector2Array([center + Vector2(0.0, -132.0)])
	var start := -PI * 0.5
	var end := -PI * 1.5 if side < 0.0 else PI * 0.5
	for index in range(1, 25):
		var angle := lerpf(start, end, float(index) / 24.0)
		points.append(Vector2(center.x + cos(angle) * 220.0,
			center.y + sin(angle) * 132.0))
	points.append(center + Vector2(0.0, 132.0))
	return points


func _draw_crystal_gallery(center: Vector2) -> void:
	var colours := [Color("#72e0d3"), Color("#d797e8"), Color("#8ce6dd")]
	for index in range(3):
		var x := center.x + float(index - 1) * 34.0
		var height := 62.0 + float(index % 2) * 25.0
		var points := PackedVector2Array([
			Vector2(x - 17.0, center.y + 48.0), Vector2(x - 13.0, center.y - height * 0.42),
			Vector2(x, center.y - height), Vector2(x + 16.0, center.y - height * 0.38),
			Vector2(x + 20.0, center.y + 48.0),
		])
		draw_colored_polygon(points, colours[index])
		var closed := points.duplicate()
		closed.append(points[0])
		draw_polyline(closed, Color("#392958"), 6.0, true)


func _demo_finger_pose() -> Dictionary:
	var cycle := fmod(demo_t, 2.4)
	match mode:
		"geology_river":
			var unresolved := 0
			for index in range(RIVER_PATH.size()):
				var cell := RIVER_PATH[index]
				if not river_wet[cell.y * RIVER_COLS + cell.x]:
					unresolved = index
					break
			var next := mini(RIVER_PATH.size() - 1, unresolved + 1)
			return {"at": river_path_point(unresolved).lerp(river_path_point(next),
				clampf(cycle / 1.7, 0.0, 1.0)), "pressing": cycle < 1.8}
		"geology_fossil":
			if fossil_stage == 0:
				var row := _cleared_count() / FOSSIL_GRID_COLS
				var y := FOSSIL_RECT.position.y + (float(row) + 0.5) \
					* FOSSIL_RECT.size.y / float(FOSSIL_GRID_ROWS)
				return {"at": Vector2(lerpf(FOSSIL_RECT.position.x + 30.0,
					FOSSIL_RECT.end.x - 30.0, clampf(cycle / 1.7, 0.0, 1.0)), y),
					"pressing": cycle < 1.8}
			var piece := maxi(0, fossil_snapped.find(false))
			return {"at": fossil_piece_home(piece).lerp(fossil_piece_target(piece),
				clampf(cycle / 1.7, 0.0, 1.0)), "pressing": cycle < 1.8}
		"geology_pan":
			return {"at": PAN_RECT.get_center()
				+ Vector2(sin(cycle * TAU / 1.2) * 150.0, 0.0), "pressing": true}
		"geology_geode":
			if _seam_count() < GEODE_SEAM_SPOTS.size():
				return {"at": geode_seam_spot(maxi(0, geode_seams.find(false))),
					"pressing": fmod(cycle, 0.8) > 0.38}
			return {"at": geode_half_center() + Vector2(
				clampf(cycle / 1.7, 0.0, 1.0) * GEODE_PULL_DISTANCE, 0.0),
				"pressing": cycle < 1.8}
	return {"at": WORK_RECT.get_center(), "pressing": false}
