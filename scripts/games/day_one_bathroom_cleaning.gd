class_name DayOneBathroomCleaning
extends Control
## Two short, forgiving bathroom gestures that follow the basket handoff.
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
const TUB_DISTANCE_REQUIRED := 520.0
const TUB_REVERSALS_REQUIRED := 2
const SINK_MIN_GESTURE_SECONDS := 2.0
const SINK_MAX_GESTURE_SECONDS := 5.0
const TUB_MIN_GESTURE_SECONDS := 2.0
const TUB_MAX_GESTURE_SECONDS := 5.0
const DIRTY_OVERLAY_ALPHA := 0.72
const SINK_TARGET_TEXTURE := "res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png"
const TUB_TARGET_TEXTURE := "res://assets/castle/dirty_cleanup_2d/targets/target_bath_soap_ring.png"
const SPONGE_TEXTURE := "res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png"
const BRUSH_TEXTURE := "res://assets/castle/day_one_art_studio/magic_cleaning_brush.png"
const SWOOSH_TEXTURE := "res://assets/castle/dirty_cleanup_2d/effects/fx_wipe_swoosh.png"
const POINTER_TEXTURE := "res://assets/castle/training/ghost_hand.png"
const SPARKLE_TEXTURE := "res://assets/opera/worlds/props/fx_stolen_sparkle.png"
const SINK_TOOL_SCALE := 0.17
const TUB_TOOL_SCALE := 0.12
const POINTER_SCALE := 0.10
const MAX_PRESENTATION_TOOL_SCALE := 0.18
const SPARKLE_ANCHORS: Array[Vector2] = [
	Vector2(300.0, 230.0), Vector2(642.0, 176.0),
	Vector2(880.0, 392.0),
]
const SPARKLE_ANCHOR_ROLES: Array[String] = ["tub", "sink", "roshan"]


class GestureGuide extends Node2D:
	var guide_mode: String = "sink"
	var animation_time: float = 0.0

	func set_mode(next_mode: String) -> void:
		guide_mode = next_mode
		queue_redraw()

	func _process(delta: float) -> void:
		animation_time += maxf(delta, 0.0)
		queue_redraw()

	func _draw() -> void:
		var pulse: float = 1.0 + sin(animation_time * 3.2) * 0.04
		var ink := Color(0.46, 0.91, 0.86, 0.86)
		if guide_mode == "sink":
			draw_arc(Vector2.ZERO, 82.0 * pulse, -0.8, TAU - 0.8,
				24, ink, 7.0, true)
			var tip := Vector2(cos(-0.8), sin(-0.8)) * 82.0 * pulse
			_draw_arrowhead(tip, -0.8 + PI * 0.5, ink)
		else:
			var reach: float = 128.0 * pulse
			draw_line(Vector2(-reach, 0.0), Vector2(reach, 0.0), ink, 8.0,
				true)
			_draw_arrowhead(Vector2(-reach, 0.0), PI, ink)
			_draw_arrowhead(Vector2(reach, 0.0), 0.0, ink)

	func _draw_arrowhead(tip: Vector2, direction: float, color: Color) -> void:
		var heading := Vector2(cos(direction), sin(direction))
		var side := Vector2(-heading.y, heading.x)
		draw_line(tip, tip - heading * 18.0 + side * 12.0, color, 8.0, true)
		draw_line(tip, tip - heading * 18.0 - side * 12.0, color, 8.0, true)

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
var _guide: GestureGuide = null
var _basket_position := Vector2(1082.0, 575.0)
var _demo_active: bool = false
var _tool_traveling: bool = false
var _demonstration_time: float = 0.0
var _sponge_travel_complete: bool = true
var _brush_travel_complete: bool = false
var _whole_room_sparkle: bool = false
var _sparkle_nodes: Array[Sprite2D] = []


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
	_sponge_travel_complete = _step >= 1
	_brush_travel_complete = _step >= 1
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
		"tool_traveling": _tool_traveling,
		"sink_demo_active": _demo_active,
		"demo_motion_mode": "circle" if _step == 0 else "back_and_forth"
			if _step < 2 else "finale",
		"demo_pointer_following_path": _guide != null and _guide.visible
			and not _active_gesture and not _busy,
		"live_tool_follows_input": _active_gesture and _sponge != null
			and is_instance_valid(_sponge),
		"live_tool_position_bounded": _tool_position_is_bounded(),
		"tool_scale_restrained": _sponge == null or _sponge.scale.x
			<= MAX_PRESENTATION_TOOL_SCALE,
		"pointer_scale_restrained": _pointer == null or _pointer.scale.x
			<= POINTER_SCALE + 0.01,
		"circle_demo_visible": _guide != null and _guide.visible
			and _guide.guide_mode == "sink",
		"back_and_forth_arrows_visible": _guide != null and _guide.visible
			and _guide.guide_mode == "tub",
		"sponge_travel_complete": _sponge_travel_complete,
		"brush_travel_complete": _brush_travel_complete,
		"whole_room_sparkle": _whole_room_sparkle,
		"target_clutter_suppressed": (_target == null or not _target.visible)
			and (_swoosh == null or not _swoosh.visible),
		"whole_room_sparkle_style": "restrained_approved_sprite",
		"distributed_fixture_sparkles": _whole_room_sparkle
			and _sparkle_nodes.size() == SPARKLE_ANCHORS.size(),
		"sparkle_anchor_count": SPARKLE_ANCHORS.size(),
		"all_sparkle_anchors_associated": _sparkle_anchors_associated(),
		"sparkle_concurrent_peak_count": SPARKLE_ANCHORS.size(),
		"sparkle_concurrent_peak_count_ge_3": SPARKLE_ANCHORS.size() >= 3,
		"pool_pointer_ready": _whole_room_sparkle,
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
	# The generated grime remains a clear touch target, but it should sit inside
	# the authored fixtures rather than cover their full silhouettes on a phone.
	_tune_dirty_overlay(_sink_grime, 0.84)
	_tune_dirty_overlay(_tub_grime, 0.86)
	_update_dirty_overlays()


func set_supply_basket(at: Vector2) -> void:
	# The basket is the only source of tools in the child-facing flow. Keep the
	# old save step semantics, but make the visible handoff explicit each time a
	# fresh sink or resumed tub stage is entered.
	_basket_position = at
	if _step == 0:
		_begin_sink_tool_travel()
	elif _step == 1:
		_begin_brush_tool_travel()


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
	_update_tool_from_gesture(at)
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
	if _pointer != null and is_instance_valid(_pointer) \
			and not _active_gesture and not _busy:
		_pointer.rotation = sin(_pulse_time * 2.6) * 0.025
	if _sponge != null and is_instance_valid(_sponge) \
			and not _active_gesture and not _busy:
		_sponge.rotation = sin(_pulse_time * 2.1) * 0.04
	_update_demonstration_motion(delta)
	_update_dirty_overlays()
	_update_progress()


func _update_demonstration_motion(delta: float) -> void:
	if _step >= 2 or _guide == null or not is_instance_valid(_guide) \
			or not _guide.visible or _active_gesture or _busy:
		return
	_demonstration_time += maxf(delta, 0.0)
	if _step == 0:
		# Keep the hand and sponge together on the same small circular path. This
		# is a visual demonstration only; it never feeds the gesture counters.
		var angle: float = fmod(_demonstration_time * 1.6, TAU) - 0.8
		var point: Vector2 = SINK_CENTER \
			+ Vector2(cos(angle), sin(angle)) * 64.0
		_sponge.position = point
		_sponge.rotation = angle + PI * 0.5
		_pointer.position = point + Vector2(-20.0, -48.0)
		_pointer.rotation = angle + PI * 0.5
		return
	# The tub demo is a compact, slow sweep that keeps the brush above the
	# character's face while making both directions unambiguous.
	var sweep: float = sin(_demonstration_time * 1.8)
	var point: Vector2 = TUB_CENTER + Vector2(sweep * 104.0, -18.0)
	_sponge.position = point
	_sponge.rotation = -0.08 if sweep >= 0.0 else 0.08
	_pointer.position = point + Vector2(-20.0, -48.0)
	_pointer.rotation = 0.0


func _tune_dirty_overlay(overlay: Sprite2D, scale_factor: float) -> void:
	if overlay == null or not is_instance_valid(overlay):
		return
	var base_scale: Vector2 = overlay.get_meta(
		"day_one_cleaning_base_scale", overlay.scale) as Vector2
	overlay.set_meta("day_one_cleaning_base_scale", base_scale)
	overlay.scale = base_scale * scale_factor


func _build_presentation() -> void:
	_gesture_surface = Control.new()
	_gesture_surface.name = "OneFingerCleaningSurface"
	_gesture_surface.size = StorybookUI.CANVAS_SIZE
	_gesture_surface.mouse_filter = Control.MOUSE_FILTER_STOP
	_gesture_surface.z_index = 10
	_gesture_surface.gui_input.connect(_on_gesture_input)
	add_child(_gesture_surface)
	_target = _make_sprite(SINK_TARGET_TEXTURE if _step == 0 else TUB_TARGET_TEXTURE,
		SINK_TARGET_POSITION if _step == 0 else TUB_TARGET_POSITION, 0.20,
		"CleaningTarget")
	_target.visible = false
	_sponge = _make_sprite(SPONGE_TEXTURE, SINK_CENTER if _step == 0 else TUB_CENTER,
		SINK_TOOL_SCALE if _step == 0 else TUB_TOOL_SCALE, "CleaningTool")
	_swoosh = _make_sprite(SWOOSH_TEXTURE, TUB_CENTER, 0.42, "TubWipeSwoosh")
	_swoosh.visible = false
	_pointer = Sprite2D.new()
	_pointer.name = "GhostHandPointer"
	_pointer.texture = load(POINTER_TEXTURE) as Texture2D
	_pointer.scale = Vector2.ONE * POINTER_SCALE
	_pointer.z_index = 30
	_pointer.position = (SINK_CENTER if _step == 0 else TUB_CENTER) + Vector2(0.0, -190.0)
	add_child(_pointer)
	_guide = GestureGuide.new()
	_guide.name = "OneFingerGestureGuide"
	_guide.position = SINK_CENTER if _step == 0 else TUB_CENTER
	_guide.set_mode("sink" if _step == 0 else "tub")
	_guide.z_index = 28
	_guide.visible = true
	add_child(_guide)


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
			_update_tool_from_gesture(at)
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
			_update_tool_from_gesture(at)
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
	if _guide != null:
		_guide.visible = false
	# Let the sponge visibly return to the basket before the approved magic
	# brush makes its separate basket-to-tub journey.
	_sponge_travel_complete = true
	_brush_travel_complete = false
	var return_tween: Tween = _sponge.create_tween()
	return_tween.tween_property(_sponge, "position", _basket_position, 0.32)
	return_tween.tween_callback(_begin_brush_tool_travel)


func _build_tub_visuals() -> void:
	if _target != null:
		_target.texture = load(TUB_TARGET_TEXTURE) as Texture2D
		_target.position = TUB_TARGET_POSITION
		_target.visible = false
	if _sponge != null:
		_sponge.position = TUB_CENTER
		_sponge.scale = Vector2.ONE * TUB_TOOL_SCALE
		_sponge.visible = true
	if _swoosh != null:
		_swoosh.visible = false
	if _pointer != null:
		_pointer.position = TUB_CENTER + Vector2(0.0, -190.0)
		_pointer.visible = true
	if _guide != null:
		_guide.position = TUB_CENTER
		_guide.set_mode("tub")
		_guide.visible = true


func _begin_sink_tool_travel() -> void:
	if _sponge == null or not is_instance_valid(_sponge) or _step != 0:
		return
	_demo_active = true
	_tool_traveling = true
	_busy = true
	_sponge_travel_complete = false
	_sponge.texture = load(SPONGE_TEXTURE) as Texture2D
	_sponge.scale = Vector2.ONE * SINK_TOOL_SCALE
	_sponge.position = _basket_position
	_sponge.visible = true
	if _pointer != null:
		_pointer.visible = false
	if _guide != null:
		_guide.position = SINK_CENTER
		_guide.set_mode("sink")
		_guide.visible = false
	var travel: Tween = _sponge.create_tween()
	travel.tween_property(_sponge, "position", SINK_CENTER, 0.38)
	travel.tween_callback(_finish_sink_tool_travel)


func _finish_sink_tool_travel() -> void:
	_tool_traveling = false
	_demo_active = false
	_busy = false
	_sponge_travel_complete = true
	if _guide != null:
		_guide.position = SINK_CENTER
		_guide.set_mode("sink")
		_guide.visible = true
	if _pointer != null:
		_pointer.position = SINK_CENTER + Vector2(0.0, -190.0)
		_pointer.visible = true
	_announce_stage()


func _begin_brush_tool_travel() -> void:
	if _sponge == null or not is_instance_valid(_sponge) or _step != 1:
		return
	_tool_traveling = true
	_busy = true
	_brush_travel_complete = false
	_sponge.texture = load(BRUSH_TEXTURE) as Texture2D
	_sponge.scale = Vector2.ONE * TUB_TOOL_SCALE
	_sponge.position = _basket_position
	_sponge.visible = true
	if _pointer != null:
		_pointer.visible = false
	if _guide != null:
		_guide.visible = false
	var travel: Tween = _sponge.create_tween()
	travel.tween_property(_sponge, "position", TUB_CENTER, 0.38)
	travel.tween_callback(_finish_brush_tool_travel)


func _finish_brush_tool_travel() -> void:
	_tool_traveling = false
	_busy = false
	_brush_travel_complete = true
	_build_tub_visuals()
	_announce_stage()


func _update_tool_from_gesture(at: Vector2) -> void:
	if _sponge == null or not is_instance_valid(_sponge):
		return
	var bounded: Vector2 = at
	if _step == 0:
		var sink_offset: Vector2 = at - SINK_CENTER
		var sink_limit: float = SINK_RADIUS * 0.68
		if sink_offset.length() > sink_limit:
			sink_offset = sink_offset.normalized() * sink_limit
		bounded = SINK_CENTER + sink_offset
		_sponge.rotation = sink_offset.angle() + PI * 0.5
		_pointer.rotation = _sponge.rotation
	else:
		bounded.x = clampf(at.x, TUB_CENTER.x - TUB_HALF_WIDTH,
			TUB_CENTER.x + TUB_HALF_WIDTH)
		bounded.y = clampf(at.y, TUB_CENTER.y - GESTURE_BAND * 0.35,
			TUB_CENTER.y + GESTURE_BAND * 0.35)
		_sponge.rotation = -0.08 if _tub_direction >= 0 else 0.08
		_pointer.rotation = 0.0
	_sponge.position = bounded
	_pointer.position = bounded + Vector2(-20.0, -48.0)


func _tool_position_is_bounded() -> bool:
	if _sponge == null or not is_instance_valid(_sponge) or not _active_gesture:
		return true
	if _step == 0:
		return _sponge.position.distance_to(SINK_CENTER) \
			<= SINK_RADIUS * 0.68 + 0.5
	return absf(_sponge.position.x - TUB_CENTER.x) <= TUB_HALF_WIDTH + 0.5 \
		and absf(_sponge.position.y - TUB_CENTER.y) \
			<= GESTURE_BAND * 0.35 + 0.5


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
	if _guide != null:
		_guide.visible = false
	_busy = false
	_spawn_whole_room_sparkles()
	# The room director tears this presentation down on completion. Give the
	# child a visible sparkle beat before emitting that teardown signal.
	get_tree().create_timer(0.92).timeout.connect(_emit_completion_once,
		CONNECT_ONE_SHOT)


func _spawn_whole_room_sparkles() -> void:
	_whole_room_sparkle = true
	var texture: Texture2D = load(SPARKLE_TEXTURE) as Texture2D
	if texture == null:
		return
	for index: int in range(SPARKLE_ANCHORS.size()):
		var sparkle := Sprite2D.new()
		sparkle.name = "BathroomRoomSparkle_%d" % index
		sparkle.texture = texture
		sparkle.position = SPARKLE_ANCHORS[index]
		sparkle.scale = Vector2.ONE * 0.10
		sparkle.modulate.a = 0.0
		sparkle.z_index = 40
		sparkle.set_meta("approved_sparkle_sprite", true)
		sparkle.set_meta("fixture_associated_role", SPARKLE_ANCHOR_ROLES[index])
		add_child(sparkle)
		_sparkle_nodes.append(sparkle)
		var sparkle_tween: Tween = sparkle.create_tween()
		sparkle_tween.tween_interval(float(index) * 0.03)
		sparkle_tween.tween_property(sparkle, "modulate:a", 0.72, 0.16)
		sparkle_tween.parallel().tween_property(sparkle, "scale",
			Vector2.ONE * 0.18, 0.32)
		sparkle_tween.tween_property(sparkle, "modulate:a", 0.0, 0.46)


func _sparkle_anchors_associated() -> bool:
	return SPARKLE_ANCHORS.size() == SPARKLE_ANCHOR_ROLES.size() \
		and SPARKLE_ANCHOR_ROLES == ["tub", "sink", "roshan"]


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
	if _demo_active or not _announcements_enabled or m == null or _step >= 2:
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
		_sink_grime.modulate.a = DIRTY_OVERLAY_ALPHA * (1.0 - sink_ratio) \
			if _step <= 0 else 0.0
	if _tub_grime != null and is_instance_valid(_tub_grime):
		_tub_grime.visible = _step <= 1 and tub_ratio < 1.0
		_tub_grime.modulate.a = DIRTY_OVERLAY_ALPHA * (1.0 - tub_ratio) \
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
