class_name DayOneBathroomSearch
extends Control
## First Day One tutorial activity: find three cleaning supplies with one finger.
##
## This scene owns only CanvasItem children and reports monotonic progress to
## ReefMain. It has no timer, failure, penalty, or reading dependency.

signal progress_changed(mask: int)
signal completed

const CANVAS_SIZE: Vector2 = Vector2(1280.0, 720.0)
const MAGNIFIER_PATH: String = "res://assets/opera/worlds/ui/magnifier.png"
const MAGIC_BRUSH_PATH: String = \
	"res://assets/castle/day_one_art_studio/magic_cleaning_brush.png"
const SKIMMER_PATH: String = \
	"res://assets/castle/day_one_pool/activities/pool_skimmer.png"
const SCRUBBER_PATH: String = \
	"res://assets/castle/day_one_pool/activities/waterfall_scrubber.png"
const SUPPLY_COUNT: int = 3
const ALL_MASK: int = (1 << SUPPLY_COUNT) - 1
const MAGNIFIER_SIZE: Vector2 = Vector2(194.0, 194.0)
const MAGNIFIER_LENS_OFFSET: Vector2 = Vector2(-31.0, -32.0)
const MAGNIFIER_RADIUS: float = 82.0
const SUPPLY_MAX_SIZE: Vector2 = Vector2(150.0, 120.0)
const SUPPLY_POSITIONS: Array[Vector2] = [
	Vector2(310.0, 278.0),
	Vector2(640.0, 412.0),
	Vector2(970.0, 278.0),
]
const SUPPLY_TEXTURE_PATHS: Array[String] = [
	MAGIC_BRUSH_PATH, SKIMMER_PATH, SCRUBBER_PATH,
]

var _progress_mask: int = 0
var _running: bool = false
var _completed: bool = false
var _completed_emitted: bool = false
var _dragging: bool = false
var _touch_id: int = -1
var _magnifier_position: Vector2 = CANVAS_SIZE * 0.5
var _last_input_position: Vector2 = CANVAS_SIZE * 0.5
var _pulse_time: float = 0.0
var _wrong_feedback_time: float = 0.0
var _feedback_position: Vector2 = CANVAS_SIZE * 0.5
var _feedback_color: Color = Color(0.68, 0.86, 1.0, 0.9)
var _magnifier: Sprite2D = null
var _supply_sprites: Array[Sprite2D] = []


func _ready() -> void:
	if _magnifier == null:
		setup()


func setup(restored_mask: int = 0) -> void:
	_clear_owned_children()
	_progress_mask = restored_mask & ALL_MASK
	_running = false
	_completed = _progress_mask == ALL_MASK
	_completed_emitted = false
	_dragging = false
	_touch_id = -1
	_magnifier_position = CANVAS_SIZE * 0.5
	_last_input_position = _magnifier_position
	_wrong_feedback_time = 0.0
	_pulse_time = 0.0
	if size.x < 2.0 or size.y < 2.0:
		size = CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 24
	set_process(false)
	set_meta("canvas_only", true)
	set_meta("one_finger", true)
	set_meta("no_fail_state", true)
	set_meta("no_timer", true)
	set_meta("live_input_required", true)
	set_meta("progress_mask", _progress_mask)
	_build_art()
	progress_changed.emit(_progress_mask)
	queue_redraw()


func start() -> void:
	if _magnifier == null:
		setup(_progress_mask)
	_running = true
	set_process(true)
	mouse_filter = Control.MOUSE_FILTER_STOP
	if _magnifier != null:
		_magnifier.visible = not _completed
	queue_redraw()


func stop() -> void:
	_running = false
	cancel_touch()
	set_process(false)
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func teardown() -> void:
	stop()
	_clear_owned_children()
	if is_inside_tree():
		queue_free()
	else:
		free()


func cancel_touch() -> void:
	_dragging = false
	_touch_id = -1
	_last_input_position = _magnifier_position


func probe_reveal_next() -> bool:
	if not _running or _completed:
		return false
	for index: int in range(SUPPLY_COUNT):
		var bit: int = 1 << index
		if (_progress_mask & bit) == 0:
			_move_magnifier(SUPPLY_POSITIONS[index], true)
			_try_reveal(SUPPLY_POSITIONS[index])
			return true
	return false


func audit_snapshot() -> Dictionary:
	var revealed_count: int = 0
	for index: int in range(SUPPLY_COUNT):
		if (_progress_mask & (1 << index)) != 0:
			revealed_count += 1
	return {
		"activity": "day_one_bathroom_search",
		"running": _running,
		"progress_mask": _progress_mask,
		"remaining_count": SUPPLY_COUNT - revealed_count,
		"supply_count": SUPPLY_COUNT,
		"completed": _completed,
		"completed_emitted": _completed_emitted,
		"magnifier_present": _magnifier != null,
		"revealed_sprites_present": _supply_sprites.size() == SUPPLY_COUNT,
		"touch_active": _dragging,
		"canvas_only": true,
		"one_finger": true,
		"no_fail_state": true,
		"no_timer": true,
	}


func _process(delta: float) -> void:
	_pulse_time += delta
	if _wrong_feedback_time > 0.0:
		_wrong_feedback_time = maxf(0.0, _wrong_feedback_time - delta)
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if not _running or _completed:
		return
	if event is InputEventScreenTouch:
		var touch: InputEventScreenTouch = event as InputEventScreenTouch
		if touch.pressed:
			if _touch_id == -1:
				_begin_touch(touch.position, touch.index)
				accept_event()
		elif touch.index == _touch_id:
			_end_touch()
			accept_event()
	elif event is InputEventScreenDrag:
		var drag: InputEventScreenDrag = event as InputEventScreenDrag
		if drag.index == _touch_id:
			_update_touch(drag.position, drag.index)
			accept_event()
	elif event is InputEventMouseButton:
		var mouse_button: InputEventMouseButton = event as InputEventMouseButton
		if mouse_button.button_index == MOUSE_BUTTON_LEFT:
			if mouse_button.pressed and _touch_id == -1:
				_begin_touch(mouse_button.position, 0)
				accept_event()
			elif not mouse_button.pressed and _touch_id == 0:
				_end_touch()
				accept_event()
	elif event is InputEventMouseMotion and _touch_id == 0:
		var motion: InputEventMouseMotion = event as InputEventMouseMotion
		if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
			_update_touch(motion.position, 0)
			accept_event()


func _begin_touch(point: Vector2, touch_id: int) -> void:
	_dragging = true
	_touch_id = touch_id
	_last_input_position = point
	_move_magnifier(point, true)
	if not _try_reveal(point):
		_show_wrong_feedback(point)


func _update_touch(point: Vector2, touch_id: int) -> void:
	if not _dragging or touch_id != _touch_id:
		return
	_move_magnifier(point, true)
	var revealed: bool = _try_reveal(point)
	if not revealed and point.distance_to(_last_input_position) >= 18.0:
		_show_wrong_feedback(point)
	_last_input_position = point


func _end_touch() -> void:
	cancel_touch()


func _move_magnifier(point: Vector2, show_it: bool) -> void:
	var bounded := Vector2(
		clampf(point.x, MAGNIFIER_RADIUS, CANVAS_SIZE.x - MAGNIFIER_RADIUS),
		clampf(point.y, MAGNIFIER_RADIUS, CANVAS_SIZE.y - MAGNIFIER_RADIUS))
	_magnifier_position = bounded
	if _magnifier != null:
		_magnifier.position = bounded - MAGNIFIER_LENS_OFFSET
		_magnifier.visible = show_it and not _completed


func _try_reveal(point: Vector2) -> bool:
	var did_reveal: bool = false
	for index: int in range(SUPPLY_COUNT):
		var bit: int = 1 << index
		if (_progress_mask & bit) != 0 \
				or point.distance_to(SUPPLY_POSITIONS[index]) > MAGNIFIER_RADIUS:
			continue
		_progress_mask |= bit
		did_reveal = true
		if index < _supply_sprites.size():
			_supply_sprites[index].visible = true
			_supply_sprites[index].scale *= 1.04
		_feedback_position = SUPPLY_POSITIONS[index]
		_feedback_color = Color(1.0, 0.84, 0.32, 0.95)
		_wrong_feedback_time = 0.46
		progress_changed.emit(_progress_mask)
	if did_reveal:
		set_meta("progress_mask", _progress_mask)
		if _progress_mask == ALL_MASK:
			_completed = true
			if not _completed_emitted:
				_completed_emitted = true
				completed.emit()
				if _magnifier != null:
					_magnifier.visible = false
		queue_redraw()
	return did_reveal


func _show_wrong_feedback(point: Vector2) -> void:
	if _wrong_feedback_time > 0.0:
		return
	_feedback_position = point
	_feedback_color = Color(0.68, 0.86, 1.0, 0.9)
	_wrong_feedback_time = 0.28
	queue_redraw()


func _build_art() -> void:
	var magnifier_texture: Texture2D = load(MAGNIFIER_PATH) as Texture2D
	if magnifier_texture != null:
		_magnifier = Sprite2D.new()
		_magnifier.name = "SearchMagnifier"
		_magnifier.texture = magnifier_texture
		_magnifier.z_index = 20
		_magnifier.scale = _fit_scale(magnifier_texture, MAGNIFIER_SIZE)
		_magnifier.position = _magnifier_position - MAGNIFIER_LENS_OFFSET
		_magnifier.visible = false
		add_child(_magnifier)
	for index: int in range(SUPPLY_COUNT):
		var sprite := Sprite2D.new()
		sprite.name = "HiddenSupply_%02d" % index
		var texture: Texture2D = load(SUPPLY_TEXTURE_PATHS[index]) as Texture2D
		if texture != null:
			sprite.texture = texture
			sprite.scale = _fit_scale(texture, SUPPLY_MAX_SIZE)
		sprite.position = SUPPLY_POSITIONS[index]
		sprite.z_index = 12
		sprite.visible = (_progress_mask & (1 << index)) != 0
		add_child(sprite)
		_supply_sprites.append(sprite)


func _fit_scale(texture: Texture2D, target_size: Vector2) -> Vector2:
	var source_size := Vector2(texture.get_width(), texture.get_height())
	if source_size.x <= 0.0 or source_size.y <= 0.0:
		return Vector2.ONE
	var ratio: float = minf(
		target_size.x / source_size.x, target_size.y / source_size.y)
	return Vector2.ONE * ratio


func _clear_owned_children() -> void:
	for child: Node in get_children():
		child.free()
	_supply_sprites.clear()
	_magnifier = null


func _draw() -> void:
	for index: int in range(SUPPLY_COUNT):
		if (_progress_mask & (1 << index)) != 0:
			continue
		var center: Vector2 = SUPPLY_POSITIONS[index]
		var phase: float = sin(_pulse_time * 2.4 + float(index)) * 0.5 + 0.5
		var alpha: float = 0.12 + phase * 0.12
		draw_arc(center, 42.0 + phase * 5.0, -2.7, -0.45, 18,
			Color(0.76, 0.92, 1.0, alpha), 4.0)
		draw_circle(center + Vector2(-22.0, -16.0), 5.0,
			Color(1.0, 0.9, 0.45, alpha + 0.06))
		draw_circle(center + Vector2(24.0, 18.0), 4.0,
			Color(0.78, 0.92, 1.0, alpha))
	if _wrong_feedback_time > 0.0:
		var phase: float = 1.0 - (_wrong_feedback_time / 0.46)
		var radius: float = 18.0 + phase * 34.0
		draw_arc(_feedback_position, radius, 0.0, TAU, 24,
			Color(_feedback_color, _feedback_color.a * (1.0 - phase)), 7.0)
		draw_circle(_feedback_position, 7.0,
			Color(_feedback_color, _feedback_color.a * (1.0 - phase)))
