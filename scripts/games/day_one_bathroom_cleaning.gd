class_name DayOneBathroomCleaning
extends Control
## Two short, forgiving bathroom gestures that follow the supply hunt.
##
## Sink is a circular scrub (arc + distance); tub is a back-and-forth brush
## (distance + direction reversals). Both only advance from a live one-finger
## gesture, so a quiet screen can never win by waiting.

signal cleanup_step_completed(step: int, cleanup_id: String)
signal finale_started
signal cleanup_completed

const SINK_CENTER := Vector2(642.0, 280.0)
const TUB_CENTER := Vector2(310.0, 349.0)
const SINK_TARGET_POSITION := SINK_CENTER
const TUB_TARGET_POSITION := Vector2(310.0, 325.0)
const SINK_RADIUS := 142.0
const TUB_HALF_WIDTH := 210.0
const GESTURE_BAND := 172.0
const SINK_ARC_REQUIRED := TAU * 1.05
const SINK_DISTANCE_REQUIRED := 520.0
const TUB_DISTANCE_REQUIRED := 760.0
const TUB_REVERSALS_REQUIRED := 4
const SINK_MIN_GESTURE_SECONDS := 2.0
const SINK_MAX_GESTURE_SECONDS := 5.0
const TUB_MIN_GESTURE_SECONDS := 2.0
const TUB_MAX_GESTURE_SECONDS := 5.0
const SINK_TARGET_TEXTURE := "res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png"
const TUB_TARGET_TEXTURE := "res://assets/castle/dirty_cleanup_2d/targets/target_bath_soap_ring.png"
const SPONGE_TEXTURE := "res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png"
const SWOOSH_TEXTURE := "res://assets/castle/dirty_cleanup_2d/effects/fx_wipe_swoosh.png"
const POINTER_TEXTURE := "res://assets/castle/training/ghost_hand.png"

var m: ReefMain
var _step: int = 0
var _active_gesture: bool = false
var _last_point := Vector2.ZERO
var _last_angle: float = 0.0
var _sink_arc: float = 0.0
var _sink_distance: float = 0.0
var _tub_distance: float = 0.0
var _tub_reversals: int = 0
var _tub_direction: int = 0
var _last_tub_x: float = 0.0
var _valid_motion_seconds: float = 0.0
var _motion_since_last_tick: bool = false
var _busy: bool = false
var _completion_sent: bool = false
var _announcements_enabled: bool = true
var _pulse_time: float = 0.0
var _gesture_surface: Control = null
var _pointer: Sprite2D = null
var _sponge: Sprite2D = null
var _target: Sprite2D = null
var _swoosh: Sprite2D = null
var _progress: ColorRect = null
var _sink_grime: Sprite2D = null
var _tub_grime: Sprite2D = null


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	name = "DayOneBathroomCleaning"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	m.set_meta("day_one_bathroom_cleaning_announcements", announcements_enabled)
	m.set_meta("day_one_bathroom_cleaning_canvas_only", true)
	m.set_meta("day_one_bathroom_cleaning_mobile_texture_limit", true)
	if not m.has_meta("day_one_bathroom_cleaning_completion_count"):
		m.set_meta("day_one_bathroom_cleaning_completion_count", 0)
	_step = clampi(m.day_one_bathroom_cleanup_step, 0, 3)
	if _step >= 2:
		# A save can land after the tub gesture but before the director's room
		# completion callback. Re-emit that boundary once on re-entry.
		if _step == 2 or not m._day_one_ref().is_room_completed("bathroom"):
			_emit_completion_once()
		else:
			_completion_sent = true
		return
	_build_presentation()
	set_process(true)
	call_deferred("_announce_stage")


func teardown() -> void:
	set_process(false)
	if is_inside_tree():
		queue_free()
	else:
		free()


func audit_snapshot() -> Dictionary:
	return {
		"active_step": _step,
		"active_stage": "sink" if _step == 0 else "tub" if _step == 1 else "finale",
		"sink_arc": _sink_arc,
		"sink_distance": _sink_distance,
		"tub_distance": _tub_distance,
		"tub_reversals": _tub_reversals,
		"valid_motion_seconds": _valid_motion_seconds,
		"sink_arc_required": SINK_ARC_REQUIRED,
		"sink_distance_required": SINK_DISTANCE_REQUIRED,
		"tub_distance_required": TUB_DISTANCE_REQUIRED,
		"tub_reversals_required": TUB_REVERSALS_REQUIRED,
		"passive_progress": false,
		"gesture_budget": {
			"sink_min_seconds": SINK_MIN_GESTURE_SECONDS,
			"sink_max_seconds": SINK_MAX_GESTURE_SECONDS,
			"tub_min_seconds": TUB_MIN_GESTURE_SECONDS,
			"tub_max_seconds": TUB_MAX_GESTURE_SECONDS,
		},
		"has_visual_pointer": _pointer != null,
		"has_gesture_surface": _gesture_surface != null,
		"grime_overlays_bound": _sink_grime != null and _tub_grime != null,
		"sink_grime_visible": _sink_grime != null and _sink_grime.visible,
		"tub_grime_visible": _tub_grime != null and _tub_grime.visible,
		"grime_fade_progress": _grime_fade_progress(),
		"sink_gesture_reachable": SINK_CENTER.x > 0.0 and SINK_CENTER.y > 0.0
			and SINK_CENTER.x < StorybookUI.CANVAS_SIZE.x
			and SINK_CENTER.y < StorybookUI.CANVAS_SIZE.y,
		"tub_gesture_reachable": TUB_CENTER.x > 0.0 and TUB_CENTER.y > 0.0
			and TUB_CENTER.x < StorybookUI.CANVAS_SIZE.x
			and TUB_CENTER.y < StorybookUI.CANVAS_SIZE.y,
		"canvas_only": _all_canvas_children(self),
		"completion_sent": _completion_sent,
	}


func is_sink_active() -> bool:
	return _step == 0 and not _busy


func is_tub_active() -> bool:
	return _step == 1 and not _busy


func set_dirty_overlays(sink_grime: Sprite2D, tub_grime: Sprite2D) -> void:
	_sink_grime = sink_grime
	_tub_grime = tub_grime
	_update_dirty_overlays()


func probe_begin_gesture(at: Vector2) -> bool:
	if _busy or _step >= 2:
		return false
	if _step == 0 and at.distance_to(SINK_CENTER) > SINK_RADIUS + GESTURE_BAND:
		return false
	if _step == 1 and absf(at.x - TUB_CENTER.x) > TUB_HALF_WIDTH + GESTURE_BAND:
		return false
	_active_gesture = true
	_last_point = at
	_last_angle = (at - SINK_CENTER).angle()
	_last_tub_x = at.x
	_tub_direction = 0
	_valid_motion_seconds = 0.0
	_motion_since_last_tick = false
	return true


func probe_gesture_to(at: Vector2, motion_seconds: float = 0.0) -> bool:
	if not _active_gesture or _busy:
		return false
	_consume_gesture(at)
	if motion_seconds > 0.0:
		_valid_motion_seconds += motion_seconds
	return true


func probe_end_gesture() -> void:
	_active_gesture = false


func probe_sink_circle(points: Array[Vector2], motion_seconds: float = 0.06) -> bool:
	if not is_sink_active() or points.is_empty():
		return false
	if not probe_begin_gesture(points[0]):
		return false
	for point: Vector2 in points.slice(1):
		probe_gesture_to(point, motion_seconds)
		if _step >= 1:
			break
	probe_end_gesture()
	return _step >= 1


func probe_tub_strokes(points: Array[Vector2], motion_seconds: float = 0.55) -> bool:
	if not is_tub_active() or points.is_empty():
		return false
	if not probe_begin_gesture(points[0]):
		return false
	for point: Vector2 in points.slice(1):
		probe_gesture_to(point, motion_seconds)
		if _step >= 2:
			break
	probe_end_gesture()
	return _step >= 2


func _process(delta: float) -> void:
	_pulse_time += maxf(delta, 0.0)
	if _active_gesture and _motion_since_last_tick:
		_valid_motion_seconds += maxf(delta, 0.0)
	_motion_since_last_tick = false
	if _pointer != null and is_instance_valid(_pointer):
		_pointer.rotation = sin(_pulse_time * 2.6) * 0.05
	if _sponge != null and is_instance_valid(_sponge):
		_sponge.rotation = sin(_pulse_time * 2.1) * 0.08
	_update_dirty_overlays()
	_update_progress()


func _build_presentation() -> void:
	_gesture_surface = Control.new()
	_gesture_surface.name = "OneFingerCleaningSurface"
	_gesture_surface.size = StorybookUI.CANVAS_SIZE
	_gesture_surface.mouse_filter = Control.MOUSE_FILTER_STOP
	_gesture_surface.z_index = 10
	_gesture_surface.gui_input.connect(_on_gesture_input)
	add_child(_gesture_surface)
	_target = _make_sprite(SINK_TARGET_TEXTURE if _step == 0 else TUB_TARGET_TEXTURE,
		SINK_TARGET_POSITION if _step == 0 else TUB_TARGET_POSITION, 0.30,
		"CleaningTarget")
	_sponge = _make_sprite(SPONGE_TEXTURE, SINK_CENTER if _step == 0 else TUB_CENTER,
		0.34, "CleaningTool")
	_swoosh = _make_sprite(SWOOSH_TEXTURE, TUB_CENTER, 0.42, "TubWipeSwoosh")
	_swoosh.visible = _step == 1
	_pointer = Sprite2D.new()
	_pointer.name = "GhostHandPointer"
	_pointer.texture = load(POINTER_TEXTURE) as Texture2D
	_pointer.scale = Vector2.ONE * 0.18
	_pointer.z_index = 30
	_pointer.position = (SINK_CENTER if _step == 0 else TUB_CENTER) + Vector2(0.0, -190.0)
	add_child(_pointer)


func _make_sprite(path: String, at: Vector2, scale_factor: float, node_name: String) -> Sprite2D:
	var sprite := Sprite2D.new()
	sprite.name = node_name
	sprite.texture = load(path) as Texture2D
	sprite.position = at
	sprite.scale = Vector2.ONE * scale_factor
	sprite.z_index = 5
	add_child(sprite)
	return sprite


func _on_gesture_input(event: InputEvent) -> void:
	if _busy or _step >= 2:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			probe_begin_gesture(touch.position)
		else:
			probe_end_gesture()
		get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag:
		probe_gesture_to((event as InputEventScreenDrag).position)
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_LEFT:
			if button.pressed:
				probe_begin_gesture(button.position)
			else:
				probe_end_gesture()
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseMotion and _active_gesture:
		probe_gesture_to((event as InputEventMouseMotion).position)
		get_viewport().set_input_as_handled()


func _consume_gesture(at: Vector2) -> void:
	if _step == 0:
		var previous_angle: float = _last_angle
		var angle: float = (at - SINK_CENTER).angle()
		var angle_delta: float = wrapf(angle - previous_angle, -PI, PI)
		if at.distance_to(SINK_CENTER) <= SINK_RADIUS + GESTURE_BAND:
			var moved: float = _last_point.distance_to(at)
			_sink_arc += absf(angle_delta)
			_sink_distance += moved
			if moved > 1.0:
				_motion_since_last_tick = true
		_last_angle = angle
		_last_point = at
		if _sink_arc >= SINK_ARC_REQUIRED \
				and _sink_distance >= SINK_DISTANCE_REQUIRED \
				and _valid_motion_seconds >= SINK_MIN_GESTURE_SECONDS:
			_finish_sink()
	else:
		var delta_x: float = at.x - _last_tub_x
		var direction: int = 1 if delta_x > 0.0 else -1 if delta_x < 0.0 else 0
		if absf(delta_x) > 2.0:
			_tub_distance += absf(delta_x)
			_motion_since_last_tick = true
			if direction != 0 and _tub_direction != 0 \
					and direction != _tub_direction:
				_tub_reversals += 1
			_tub_direction = direction
			_last_tub_x = at.x
			_last_point = at
		if _tub_distance >= TUB_DISTANCE_REQUIRED \
				and _tub_reversals >= TUB_REVERSALS_REQUIRED \
				and _valid_motion_seconds >= TUB_MIN_GESTURE_SECONDS:
			_finish_tub()


func _finish_sink() -> void:
	if _busy or _step != 0:
		return
	_busy = true
	_active_gesture = false
	_step = 1
	if m != null:
		m.day_one_record_bathroom_cleanup_step(1)
	cleanup_step_completed.emit(1, "sink")
	if _target != null:
		_target.visible = false
	if _sponge != null:
		_sponge.visible = false
	if _pointer != null:
		_pointer.visible = false
	_busy = false
	_build_tub_visuals()
	_announce_stage()


func _build_tub_visuals() -> void:
	if _target != null:
		_target.texture = load(TUB_TARGET_TEXTURE) as Texture2D
		_target.position = TUB_TARGET_POSITION
		_target.visible = true
	if _sponge != null:
		_sponge.position = TUB_CENTER
		_sponge.visible = true
	if _swoosh != null:
		_swoosh.visible = true
	if _pointer != null:
		_pointer.position = TUB_CENTER + Vector2(0.0, -190.0)
		_pointer.visible = true


func _finish_tub() -> void:
	if _busy or _step != 1:
		return
	_busy = true
	_active_gesture = false
	_step = 2
	if m != null:
		m.day_one_record_bathroom_cleanup_step(2)
	cleanup_step_completed.emit(2, "tub")
	finale_started.emit()
	if m != null and _announcements_enabled:
		m.show_msg("Roshan", "The bathroom is sparkling!", "win")
		m._say("roshan", "win", 0.6)
	if _pointer != null:
		_pointer.visible = false
	if _target != null:
		_target.visible = false
	if _sponge != null:
		_sponge.visible = false
	if _swoosh != null:
		_swoosh.visible = false
	_busy = false
	_emit_completion_once()


func _emit_completion_once() -> void:
	if _completion_sent:
		return
	_completion_sent = true
	if m != null:
		var completion_count: int = int(m.get_meta(
			"day_one_bathroom_cleaning_completion_count", 0))
		if completion_count == 0:
			m.set_meta("day_one_bathroom_cleaning_completion_count", 1)
	cleanup_completed.emit()


func _announce_stage() -> void:
	if not _announcements_enabled or m == null or _step >= 2:
		return
	if _step == 0:
		m.show_msg("Roshan", "Scrub the sink in little circles!", "talk")
	else:
		m.show_msg("Roshan", "Brush the tub back and forth!", "talk")
	m._say("roshan", "talk", 0.8)


func _update_progress() -> void:
	if _progress == null or not is_instance_valid(_progress):
		return
	var ratio: float = 0.0
	if _step == 0:
		ratio = minf(1.0, minf(_sink_arc / SINK_ARC_REQUIRED,
			minf(_sink_distance / SINK_DISTANCE_REQUIRED,
				_valid_motion_seconds / SINK_MIN_GESTURE_SECONDS)))
	elif _step == 1:
		ratio = minf(1.0, minf(_tub_distance / TUB_DISTANCE_REQUIRED,
			minf(float(_tub_reversals) / float(TUB_REVERSALS_REQUIRED),
				_valid_motion_seconds / TUB_MIN_GESTURE_SECONDS)))
	_progress.size.x = 860.0 * ratio


func _update_dirty_overlays() -> void:
	var sink_ratio: float = _gesture_ratio(0)
	var tub_ratio: float = _gesture_ratio(1)
	if _sink_grime != null and is_instance_valid(_sink_grime):
		_sink_grime.visible = _step <= 0 and sink_ratio < 1.0
		_sink_grime.modulate.a = 0.86 * (1.0 - sink_ratio) \
			if _step <= 0 else 0.0
	if _tub_grime != null and is_instance_valid(_tub_grime):
		_tub_grime.visible = _step <= 1 and tub_ratio < 1.0
		_tub_grime.modulate.a = 0.86 * (1.0 - tub_ratio) \
			if _step <= 1 else 0.0


func _gesture_ratio(stage: int) -> float:
	if _step != stage:
		return 1.0 if _step > stage else 0.0
	if stage == 0:
		return minf(1.0, minf(_sink_arc / SINK_ARC_REQUIRED,
			minf(_sink_distance / SINK_DISTANCE_REQUIRED,
				_valid_motion_seconds / SINK_MIN_GESTURE_SECONDS)))
	return minf(1.0, minf(_tub_distance / TUB_DISTANCE_REQUIRED,
		minf(float(_tub_reversals) / float(TUB_REVERSALS_REQUIRED),
			_valid_motion_seconds / TUB_MIN_GESTURE_SECONDS)))


func _grime_fade_progress() -> Dictionary:
	return {
		"sink": _gesture_ratio(0),
		"tub": _gesture_ratio(1),
	}


func _all_canvas_children(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem or not _all_canvas_children(child):
			return false
	return true
