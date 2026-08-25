class_name DayOneTutorialOverlay
extends Control

## First-entry, picture-first demonstrations for Day One's five room events.
##
## This surface owns no gameplay progress.  It owns only the short visual
## lesson and consumes the first press of every lesson segment so a skip can
## never fall through into the room below it.  The caller supplies `main` and
## may replace the event presets with a measured room-specific configuration.

signal segment_changed(event_id: String, segment_index: int)
signal tutorial_finished(event_id: String)
signal tutorial_skipped(event_id: String, segment_index: int)

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const CONTROL_REASON: String = "day_one_tutorial"
const MAGNIFIER_PATH: String = "res://assets/opera/worlds/ui/magnifier.png"
const GHOST_HAND_PATH: String = "res://assets/castle/training/ghost_hand.png"
const BRUSH_PATH: String = "res://assets/castle/day_one_art_studio/magic_cleaning_brush.png"
const RAINBOW_PATH: String = "res://assets/mg/rainbow_swatch.png"
const DEMO_LENGTH: float = 2.25
const SEGMENT_DURATION: float = 3.15
const TAP_HALO_RADIUS: float = 68.0
const TARGET_RADIUS: float = 82.0

var m: ReefMain = null
var event_id: String = ""
var segments: Array[Dictionary] = []
var segment_index: int = -1
var segment_time: float = 0.0
var active: bool = false
var _gate_owned: bool = false
var _touch_id: int = -1
var _touch_active: bool = false
var _last_press_consumed: bool = false
var _finish_pending: bool = false
var _magnifier: Texture2D = null
var _ghost_hand: Texture2D = null
var _brush: Texture2D = null
var _rainbow: Texture2D = null


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if size.x < 2.0 or size.y < 2.0:
		position = Vector2.ZERO
		size = CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	focus_mode = Control.FOCUS_ALL
	process_mode = Node.PROCESS_MODE_ALWAYS
	z_index = 80
	_load_assets()


## Start the configured event.  `configured_segments` is optional so a room
## can use the shared presets while probes and future rooms can inject exact
## measured sockets and voice names without changing this overlay.
func setup(main: ReefMain, next_event_id: String,
		configured_segments: Array[Dictionary] = []) -> void:
	m = main
	event_id = next_event_id.strip_edges().to_lower()
	segments = configured_segments.duplicate(true)
	if segments.is_empty():
		segments = preset_segments(event_id)
	segment_index = -1
	segment_time = 0.0
	active = true
	_touch_active = false
	_touch_id = -1
	_last_press_consumed = false
	_finish_pending = false
	_claim_input_gate()
	_advance_segment(false)
	queue_redraw()


func teardown() -> void:
	active = false
	_finish_pending = false
	_cancel_touch()
	_release_input_gate()
	segments.clear()
	if is_inside_tree():
		queue_free()
	else:
		free()


func cancel() -> void:
	teardown()


func current_segment() -> Dictionary:
	if segment_index < 0 or segment_index >= segments.size():
		return {}
	return segments[segment_index].duplicate(true)


func audit_snapshot() -> Dictionary:
	var current: Dictionary = current_segment()
	return {
		"event_id": event_id,
		"active": active,
		"segment_count": segments.size(),
		"segment_index": segment_index,
		"segment_id": String(current.get("id", "")),
		"gesture": String(current.get("gesture", "")),
		"demo_progress": _demo_progress(),
		"segment_duration": SEGMENT_DURATION,
		"input_blocked": m != null and m.touch_control_blocks.has(CONTROL_REASON),
		"canvas_only": true,
		"no_progress_owner": true,
		"consumes_any_press": true,
		"last_press_consumed": _last_press_consumed,
		"magnifier_loaded": _magnifier != null,
		"ghost_hand_loaded": _ghost_hand != null,
		"brush_loaded": _brush != null,
		"rainbow_loaded": _rainbow != null,
	}


func _process(delta: float) -> void:
	if not active:
		return
	segment_time += maxf(delta, 0.0)
	if segment_time >= SEGMENT_DURATION:
		_advance_segment(false)
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if not active and not _finish_pending:
		return
	if event is InputEventScreenTouch:
		var touch: InputEventScreenTouch = event as InputEventScreenTouch
		if touch.pressed:
			_touch_active = true
			_touch_id = touch.index
			_skip_current_segment()
		else:
			if _touch_active and touch.index == _touch_id:
				_cancel_touch()
		accept_event()
		get_viewport().set_input_as_handled()
		if not touch.pressed and _finish_pending:
			_finish_tutorial()
		return
	if event is InputEventScreenDrag:
		var drag: InputEventScreenDrag = event as InputEventScreenDrag
		if _touch_active and drag.index == _touch_id:
			accept_event()
			get_viewport().set_input_as_handled()
		return
	if event is InputEventMouseButton:
		var mouse: InputEventMouseButton = event as InputEventMouseButton
		if mouse.button_index != MOUSE_BUTTON_LEFT:
			return
		if mouse.pressed:
			_touch_active = true
			_touch_id = 0
			_skip_current_segment()
		else:
			_cancel_touch()
		accept_event()
		get_viewport().set_input_as_handled()
		if not mouse.pressed and _finish_pending:
			_finish_tutorial()


func _notification(what: int) -> void:
	match what:
		NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_APPLICATION_PAUSED:
			# Focus loss must never turn a stale release into a tutorial skip.
			_cancel_touch()
		NOTIFICATION_WM_GO_BACK_REQUEST:
			_cancel_touch()
		NOTIFICATION_WM_CLOSE_REQUEST:
			_cancel_touch()


func _skip_current_segment() -> void:
	if not active or segment_index < 0:
		return
	_last_press_consumed = true
	var skipped_index: int = segment_index
	tutorial_skipped.emit(event_id, skipped_index)
	_advance_segment(true)


func _advance_segment(was_skipped: bool) -> void:
	segment_index += 1
	segment_time = 0.0
	if not was_skipped:
		_cancel_touch()
	if segment_index >= segments.size():
		active = false
		_finish_pending = true
		if not _touch_active:
			_finish_tutorial.call_deferred()
		return
	segment_changed.emit(event_id, segment_index)
	_announce_segment(was_skipped)
	queue_redraw()


func _finish_tutorial() -> void:
	if not _finish_pending:
		return
	_finish_pending = false
	_release_input_gate()
	tutorial_finished.emit(event_id)


func _announce_segment(was_skipped: bool) -> void:
	if m == null:
		return
	var segment: Dictionary = current_segment()
	var message: String = String(segment.get("message", ""))
	var voice: String = String(segment.get("voice", ""))
	var speaker: String = String(segment.get("speaker", "roshan"))
	if message != "" and m.has_method("show_msg"):
		m.show_msg(speaker, message, voice if voice != "" else "talk")
	elif voice != "" and m.has_method("_say"):
		m._say(speaker, voice, 0.0)
	# A skip advances immediately and must not replay the prior line.  The next
	# segment's own cue is still spoken, preserving the wordless route.
	if was_skipped and voice == "" and m.has_method("_say"):
		m._say(speaker, "talk", 0.0)


func _claim_input_gate() -> void:
	if m == null or _gate_owned:
		return
	if m.has_method("_set_world_controls_enabled"):
		m._set_world_controls_enabled(false, CONTROL_REASON)
		_gate_owned = true


func _release_input_gate() -> void:
	if m == null or not _gate_owned:
		return
	if m.has_method("_set_world_controls_enabled"):
		m._set_world_controls_enabled(true, CONTROL_REASON)
	_gate_owned = false


func _cancel_touch() -> void:
	_touch_active = false
	_touch_id = -1


func _load_assets() -> void:
	_magnifier = _load_texture(MAGNIFIER_PATH)
	_ghost_hand = _load_texture(GHOST_HAND_PATH)
	_brush = _load_texture(BRUSH_PATH)
	_rainbow = _load_texture(RAINBOW_PATH)


func _load_texture(path: String) -> Texture2D:
	if not ResourceLoader.exists(path):
		return null
	return load(path) as Texture2D


func _demo_progress() -> float:
	return clampf(fmod(segment_time, DEMO_LENGTH) / DEMO_LENGTH, 0.0, 1.0)


func _canvas_point(value: Vector2) -> Vector2:
	var scale_value := Vector2(
		size.x / maxf(CANVAS_SIZE.x, 1.0),
		size.y / maxf(CANVAS_SIZE.y, 1.0))
	return Vector2(value.x * scale_value.x, value.y * scale_value.y)


func _segment_point(key: String, fallback: Vector2) -> Vector2:
	var segment: Dictionary = current_segment()
	var value: Variant = segment.get(key, fallback)
	if value is Vector2:
		return _canvas_point(value as Vector2)
	if value is Array and (value as Array).size() >= 2:
		var pair: Array = value as Array
		return _canvas_point(Vector2(float(pair[0]), float(pair[1])))
	return _canvas_point(fallback)


func _draw() -> void:
	if not active or segment_index < 0:
		return
	var segment: Dictionary = current_segment()
	var target: Vector2 = _segment_point("target", Vector2(640.0, 360.0))
	var start: Vector2 = _segment_point("start", target - Vector2(150.0, 0.0))
	var finish: Vector2 = _segment_point("end", target + Vector2(150.0, 0.0))
	var gesture: String = String(segment.get("gesture", "tap"))
	var p: float = _demo_progress()
	var pulse: float = 1.0 + sin(segment_time * 4.0) * 0.08
	# The overlay is transparent over the room; only the target and one action
	# trail are drawn, preserving the room's authored figure/ground hierarchy.
	draw_circle(target, TARGET_RADIUS * pulse, Color(1.0, 0.86, 0.35, 0.18))
	draw_arc(target, TARGET_RADIUS * pulse, 0.0, TAU, 36,
		Color(1.0, 0.88, 0.35, 0.88), 6.0, true)
	if gesture == "swipe" or gesture == "drag":
		_draw_swipe_demo(start, finish, p)
	else:
		_draw_tap_demo(target, p)
	_draw_tool(segment, target, start, finish, p, gesture)
	_draw_hand(target, start, finish, p, gesture)


func _draw_tap_demo(target: Vector2, progress: float) -> void:
	var tap_phase: float = fmod(progress * 2.0, 1.0)
	var radius: float = TAP_HALO_RADIUS * (0.60 + tap_phase * 0.50)
	draw_circle(target, radius, Color(1.0, 0.95, 0.65, 0.18))
	draw_arc(target, radius, 0.0, TAU, 32,
		Color(1.0, 0.92, 0.48, 0.82), 5.0, true)


func _draw_swipe_demo(start: Vector2, finish: Vector2, progress: float) -> void:
	var eased: float = 0.5 - cos(progress * PI) * 0.5
	var current: Vector2 = start.lerp(finish, eased)
	var trail_start: Vector2 = start.lerp(current, 0.25)
	for index: int in range(6):
		var offset: float = float(index) / 5.0
		var point: Vector2 = trail_start.lerp(current, offset)
		draw_circle(point, 20.0 - offset * 7.0,
			Color.from_hsv(0.08 + offset * 0.72, 0.58, 1.0, 0.44))
	draw_line(start, current, Color(1.0, 0.74, 0.34, 0.36), 12.0, true)
	draw_line(start, current, Color(0.58, 0.94, 1.0, 0.66), 4.0, true)


func _draw_tool(segment: Dictionary, target: Vector2, start: Vector2,
		finish: Vector2, progress: float, gesture: String) -> void:
	var tool: String = String(segment.get("tool", "rainbow"))
	var position: Vector2 = target
	if gesture == "swipe" or gesture == "drag":
		position = start.lerp(finish, 0.5 - cos(progress * PI) * 0.5)
	var texture: Texture2D = null
	if tool == "magnifier":
		texture = _magnifier
	elif tool == "brush":
		texture = _brush
	else:
		texture = _rainbow
	if texture != null:
		var tool_size := Vector2(116.0, 116.0)
		if tool == "brush":
			tool_size = Vector2(128.0, 128.0)
		draw_texture_rect(texture, Rect2(position - tool_size * 0.5, tool_size),
			false, Color(1.0, 1.0, 1.0, 0.92))
	else:
		_draw_tool_fallback(position, tool)


func _draw_tool_fallback(position: Vector2, tool: String) -> void:
	if tool == "magnifier":
		draw_circle(position - Vector2(12.0, 14.0), 42.0,
			Color(0.86, 0.69, 0.32, 0.88))
		draw_circle(position - Vector2(12.0, 14.0), 30.0,
			Color(0.56, 0.86, 0.94, 0.72))
		draw_line(position + Vector2(18.0, 18.0), position + Vector2(55.0, 55.0),
			Color(0.18, 0.46, 0.56, 1.0), 14.0, true)
		return
	# Broad fallback brush with the rainbow swatch embedded in its bristles.
	var bristles := PackedVector2Array([
		position + Vector2(-54.0, -20.0), position + Vector2(32.0, -20.0),
		position + Vector2(50.0, 28.0), position + Vector2(-48.0, 28.0)])
	draw_colored_polygon(bristles, Color(1.0, 0.50, 0.54, 0.94))
	draw_line(position + Vector2(-12.0, -4.0), position + Vector2(54.0, -72.0),
			Color(0.93, 0.72, 0.30, 1.0), 18.0, true)


func _draw_hand(target: Vector2, start: Vector2, finish: Vector2,
		progress: float, gesture: String) -> void:
	var hand_position: Vector2 = target
	if gesture == "swipe" or gesture == "drag":
		hand_position = start.lerp(finish, 0.5 - cos(progress * PI) * 0.5)
	if _ghost_hand != null:
		var hand_size := Vector2(88.0, 88.0)
		draw_texture_rect(_ghost_hand,
			Rect2(hand_position + Vector2(34.0, 26.0), hand_size), false,
			Color(1.0, 1.0, 1.0, 0.86))
	else:
		draw_circle(hand_position + Vector2(68.0, 58.0), 16.0,
			Color(1.0, 0.98, 0.88, 0.94))
		draw_line(hand_position + Vector2(68.0, 58.0), hand_position + Vector2(20.0, 10.0),
			Color(1.0, 0.98, 0.88, 0.88), 12.0, true)


static func preset_segments(next_event_id: String) -> Array[Dictionary]:
	match next_event_id.strip_edges().to_lower():
		"bathroom":
			return [
				{"id": "bathroom_pick_magnifier", "gesture": "tap",
					"tool": "magnifier", "target": Vector2(640, 360),
					"message": "Tap the shiny glass!", "voice": "op_detective_lens"},
				{"id": "bathroom_sweep_clue", "gesture": "swipe",
					"tool": "magnifier", "start": Vector2(310, 278),
					"end": Vector2(970, 278), "target": Vector2(640, 278),
					"message": "Sweep the glass to find the sparkle!",
					"voice": "op_detective_search"},
			]
		"art", "dirty_art":
			return [
				{"id": "art_pick_brush", "gesture": "tap", "tool": "brush",
					"target": Vector2(344, 390),
					"message": "Tap the shiny art supplies!", "voice": "op_painter_sketch"},
				{"id": "art_swipe_grime", "gesture": "swipe", "tool": "brush",
					"start": Vector2(120, 385), "end": Vector2(240, 385),
					"target": Vector2(180, 385),
					"message": "Swipe across the yucky spot!",
					"voice": "op_painter_strokes"},
			]
		"stuffie":
			return [
				{"id": "stuffie_wake_bunny", "gesture": "tap", "tool": "rainbow",
					"target": Vector2(556, 456),
					"message": "Tap the wiggly bunny!", "voice": "talk"},
				{"id": "stuffie_clean_bunny", "gesture": "swipe", "tool": "brush",
					"start": Vector2(466, 456), "end": Vector2(646, 456),
					"target": Vector2(556, 456),
					"message": "Swipe the rainbow brush!", "voice": "talk"},
			]
		"pool":
			return [
				{"id": "pool_sweep_skimmer", "gesture": "swipe", "tool": "rainbow",
					"start": Vector2(330, 330), "end": Vector2(860, 330),
					"target": Vector2(590, 330),
					"message": "Sweep the trash into the basket!", "voice": "talk"},
				{"id": "pool_scrub_waterfall", "gesture": "swipe", "tool": "brush",
					"start": Vector2(520, 230), "end": Vector2(520, 500),
					"target": Vector2(520, 360),
					"message": "Scrub down the waterfall!", "voice": "talk"},
				{"id": "pool_help_seahorse", "gesture": "tap", "tool": "rainbow",
					"target": Vector2(930, 300),
					"message": "Tap-tap to help your friend!", "voice": "talk"},
			]
		"boss", "bunny_boss":
			return [
				{"id": "boss_watch_flash", "gesture": "tap", "tool": "rainbow",
					"target": Vector2(660, 300),
					"message": "Star flashes—tap-tap-tap!", "voice": "dustboss_show"},
				{"id": "boss_rainbow_swipe", "gesture": "swipe", "tool": "brush",
					"start": Vector2(500, 340), "end": Vector2(820, 340),
					"target": Vector2(660, 340),
					"message": "Or sweep the rainbow brush three times!",
					"voice": "dustboss_again"},
			]
	return []
