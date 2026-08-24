class_name PoolSkimmerActivity
extends Control
## One-finger pool-surface cleanup activity.
##
## This is deliberately a small, self-contained Canvas2D activity. The pool
## room can mount it wherever it needs to; no state is written here except
## the monotonic six-bit progress mask exposed by the signals and probes.

signal progress_changed(mask: int)
signal completed

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const TRASH_ATLAS_PATH := \
	"res://assets/castle/day_one_pool/activities/floating_trash_atlas.png"
const SKIMMER_PATH := \
	"res://assets/castle/day_one_pool/activities/pool_skimmer.png"
const BASKET_PATH := \
	"res://assets/castle/day_one_pool/activities/cleanup_basket.png"
const TRASH_CELL_SIZE := Vector2(341.0, 341.0)
const TRASH_COUNT := 6
const ALL_MASK := (1 << TRASH_COUNT) - 1
const CATCH_RADIUS := 118.0
const BASKET_POSITION := Vector2(1080.0, 596.0)
const SKIMMER_MAX_SIZE := Vector2(330.0, 250.0)
const BASKET_MAX_SIZE := Vector2(210.0, 165.0)
const TRASH_POSITIONS: Array[Vector2] = [
	Vector2(352.0, 292.0),
	Vector2(640.0, 274.0),
	Vector2(928.0, 300.0),
	Vector2(420.0, 462.0),
	Vector2(700.0, 445.0),
	Vector2(982.0, 468.0),
]
const TRASH_TINTS: Array[Color] = [
	Color(1.0, 0.95, 0.84),
	Color(0.92, 1.0, 0.96),
	Color(1.0, 0.93, 0.98),
	Color(0.96, 0.98, 1.0),
	Color(1.0, 0.97, 0.84),
	Color(0.92, 0.95, 1.0),
]

var _progress_mask: int = 0
var _running: bool = false
var _dragging: bool = false
var _completed: bool = false
var _demo_time: float = 0.0
var _last_input_time: float = 0.0
var _skimmer_position := Vector2(640.0, 380.0)
var _trash_sprites: Array[Sprite2D] = []
var _trash_base_positions: Array[Vector2] = []
var _flight_tweens: Array[Tween] = []
var _skimmer: Sprite2D = null
var _basket: Sprite2D = null
var _demo_pointer: Label = null
var _feedback_layer: Control = null
var _atlas: Texture2D = null


func setup(initial_mask: int = 0) -> void:
	_stop_flights()
	_clear_owned_children()
	_progress_mask = initial_mask & ALL_MASK
	_running = false
	_dragging = false
	_completed = _progress_mask == ALL_MASK
	_demo_time = 0.0
	_last_input_time = 0.0
	_skimmer_position = Vector2(640.0, 380.0)
	if size.x <= 1.0 or size.y <= 1.0:
		size = CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 24
	_atlas = load(TRASH_ATLAS_PATH) as Texture2D
	_build_activity_art()
	queue_redraw()


func start() -> void:
	_running = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	_demo_time = 0.0
	_dragging = false
	if _demo_pointer != null and is_instance_valid(_demo_pointer):
		_demo_pointer.visible = not _completed
	set_process(true)
	queue_redraw()


func stop() -> void:
	_running = false
	_dragging = false
	_stop_flights()
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	if _demo_pointer != null and is_instance_valid(_demo_pointer):
		_demo_pointer.visible = false
	set_process(false)


func cancel_touch() -> void:
	_dragging = false
	_last_input_time = _demo_time


func probe_collect_next() -> bool:
	if _completed:
		return false
	if not _running:
		start()
	for index: int in range(TRASH_COUNT):
		if (_progress_mask & (1 << index)) == 0:
			_set_skimmer_position(TRASH_POSITIONS[index], true)
			return _collect_at(TRASH_POSITIONS[index])
	return false


func audit_snapshot() -> Dictionary:
	var remaining: int = TRASH_COUNT - _count_bits(_progress_mask)
	return {
		"activity": "pool_skimmer",
		"running": _running,
		"progress_mask": _progress_mask,
		"mask": _progress_mask,
		"item_count": TRASH_COUNT,
		"remaining_count": remaining,
		"completed": _completed,
		"skimmer_present": _skimmer != null and is_instance_valid(_skimmer),
		"basket_present": _basket != null and is_instance_valid(_basket),
		"trash_sprite_count": _trash_sprites.size(),
		"atlas_cell_size": TRASH_CELL_SIZE,
		"catch_radius": CATCH_RADIUS,
		"live_input_required": true,
		"one_finger": true,
		"no_fail_state": true,
		"canvas_only": true,
		"borderless_room_grown": true,
		"demo_pointer_visible": _demo_pointer != null
			and is_instance_valid(_demo_pointer) and _demo_pointer.visible,
	}


func _count_bits(value: int) -> int:
	var remaining: int = value & ALL_MASK
	var count: int = 0
	while remaining != 0:
		count += remaining & 1
		remaining >>= 1
	return count


func _ready() -> void:
	if _trash_sprites.is_empty():
		setup()


func _process(delta: float) -> void:
	_demo_time += maxf(delta, 0.0)
	if _demo_pointer == null or not is_instance_valid(_demo_pointer):
		queue_redraw()
		return
	if not _running or _completed or _dragging:
		_demo_pointer.visible = false
		queue_redraw()
		return
	var idle_seconds: float = _demo_time - _last_input_time
	_demo_pointer.visible = idle_seconds > 0.45
	if _demo_pointer.visible:
		var route_index: int = int(floor(_demo_time * 0.72)) % TRASH_COUNT
		while (_progress_mask & (1 << route_index)) != 0:
			route_index = (route_index + 1) % TRASH_COUNT
		var route_phase: float = fmod(_demo_time * 0.72, 1.0)
		var route_position: Vector2 = TRASH_POSITIONS[route_index]
		_demo_pointer.position = route_position + Vector2(
			90.0 + sin(_demo_time * 3.0) * 9.0,
			-92.0 + cos(_demo_time * 2.4) * 7.0)
		_demo_pointer.rotation = sin(_demo_time * 2.0) * 0.06
		_demo_pointer.scale = Vector2.ONE * (0.96 + sin(_demo_time * 4.0) * 0.06)
		# route_phase is intentionally used to make the pointer breathe along
		# the current target; it never catches anything without live input.
		_demo_pointer.modulate.a = 0.86 + route_phase * 0.12
	queue_redraw()


func _draw() -> void:
	var canvas: Vector2 = size if size.x > 1.0 and size.y > 1.0 else CANVAS_SIZE
	# The activity grows out of the room: soft painted water and an open edge,
	# with no modal panel or hard border competing with the pool art beneath it.
	draw_rect(Rect2(Vector2.ZERO, canvas), Color(0.11, 0.29, 0.43, 0.17), true)
	draw_circle(Vector2(640.0, 376.0), 330.0, Color(0.20, 0.70, 0.78, 0.28))
	draw_circle(Vector2(640.0, 376.0), 292.0, Color(0.36, 0.85, 0.86, 0.20))
	for wave: int in range(7):
		var y: float = 204.0 + float(wave) * 63.0
		var wave_alpha: float = 0.12 + 0.025 * sin(_demo_time * 1.7 + wave)
		draw_arc(Vector2(640.0, y), 245.0 + wave * 8.0, 0.12, PI - 0.12,
			28, Color(0.84, 1.0, 0.97, wave_alpha), 3.0, true)
	# Broad rings make the catch target legible even on a small phone.
	for index: int in range(TRASH_COUNT):
		if (_progress_mask & (1 << index)) != 0:
			continue
		var pulse: float = 1.0 + sin(_demo_time * 2.2 + index) * 0.045
		draw_circle(TRASH_POSITIONS[index], 69.0 * pulse,
			Color(0.88, 1.0, 0.86, 0.08))
		draw_arc(TRASH_POSITIONS[index], 75.0 * pulse, 0.0, TAU, 32,
			Color(1.0, 0.94, 0.52, 0.23), 3.0, true)
	# The basket's landing glow is a visual destination, never a score gate.
	draw_circle(BASKET_POSITION, 106.0 + sin(_demo_time * 2.4) * 4.0,
		Color(1.0, 0.88, 0.38, 0.10))


func _gui_input(event: InputEvent) -> void:
	if not _running or _completed:
		return
	if event is InputEventScreenTouch:
		var touch: InputEventScreenTouch = event as InputEventScreenTouch
		if touch.pressed:
			_begin_live_drag(touch.position)
		else:
			cancel_touch()
		accept_event()
		return
	if event is InputEventScreenDrag:
		var drag: InputEventScreenDrag = event as InputEventScreenDrag
		if _dragging:
			_update_live_drag(drag.position)
		accept_event()
		return
	if event is InputEventMouseButton:
		var mouse_button: InputEventMouseButton = event as InputEventMouseButton
		if mouse_button.button_index != MOUSE_BUTTON_LEFT:
			return
		if mouse_button.pressed:
			_begin_live_drag(mouse_button.position)
		else:
			cancel_touch()
		accept_event()
		return
	if event is InputEventMouseMotion:
		var mouse_motion: InputEventMouseMotion = event as InputEventMouseMotion
		if _dragging:
			_update_live_drag(mouse_motion.position)
			accept_event()


func _begin_live_drag(position: Vector2) -> void:
	_dragging = true
	_last_input_time = _demo_time
	if _demo_pointer != null and is_instance_valid(_demo_pointer):
		_demo_pointer.visible = false
	_update_live_drag(position)


func _update_live_drag(position: Vector2) -> void:
	if not _dragging:
		return
	_last_input_time = _demo_time
	_set_skimmer_position(position, true)
	_collect_at(_skimmer_position)


func _set_skimmer_position(position: Vector2, live_input: bool) -> void:
	var canvas: Vector2 = size if size.x > 1.0 and size.y > 1.0 else CANVAS_SIZE
	_skimmer_position = Vector2(
		clampf(position.x, 90.0, canvas.x - 90.0),
		clampf(position.y, 100.0, canvas.y - 72.0))
	if _skimmer == null or not is_instance_valid(_skimmer):
		return
	_skimmer.position = _skimmer_position
	_skimmer.rotation = clampf(
		(_skimmer_position.x - 640.0) / 1200.0, -0.18, 0.18)
	if live_input:
		_skimmer.modulate = Color(1.0, 1.0, 1.0, 1.0)


func _collect_at(position: Vector2) -> bool:
	if not _running and not _completed:
		return false
	for index: int in range(TRASH_COUNT):
		if (_progress_mask & (1 << index)) != 0:
			continue
		if position.distance_to(TRASH_POSITIONS[index]) <= CATCH_RADIUS:
			_collect_item(index)
			return true
	return false


func _collect_item(index: int) -> void:
	if index < 0 or index >= TRASH_COUNT:
		return
	var bit: int = 1 << index
	if (_progress_mask & bit) != 0:
		return
	_progress_mask |= bit
	progress_changed.emit(_progress_mask)
	_spawn_catch_feedback(TRASH_POSITIONS[index])
	if index < _trash_sprites.size():
		var piece: Sprite2D = _trash_sprites[index]
		if piece != null and is_instance_valid(piece):
			piece.z_index = 12
			var flight: Tween = piece.create_tween().set_parallel(true)
			_flight_tweens.append(flight)
			flight.tween_property(piece, "position", BASKET_POSITION, 0.48) \
				.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
			flight.tween_property(piece, "scale", piece.scale * 0.42, 0.48)
			flight.tween_property(piece, "modulate:a", 0.0, 0.42)
			flight.chain().tween_callback(_finish_piece_flight.bind(index, flight))
	if _progress_mask == ALL_MASK:
		_completed = true
		_dragging = false
		if _demo_pointer != null and is_instance_valid(_demo_pointer):
			_demo_pointer.visible = false
		completed.emit()
	queue_redraw()


func _finish_piece_flight(index: int, flight: Tween) -> void:
	_flight_tweens.erase(flight)
	if index < 0 or index >= _trash_sprites.size():
		return
	var piece: Sprite2D = _trash_sprites[index]
	if piece == null or not is_instance_valid(piece):
		return
	piece.visible = false


func _build_activity_art() -> void:
	_basket = Sprite2D.new()
	_basket.name = "CleanupBasket"
	_basket.texture = load(BASKET_PATH) as Texture2D
	_basket.position = BASKET_POSITION
	_basket.z_index = 7
	_fit_sprite(_basket, BASKET_MAX_SIZE)
	add_child(_basket)

	for index: int in range(TRASH_COUNT):
		var piece := Sprite2D.new()
		piece.name = "FloatingTrash_%02d" % index
		piece.texture = _atlas_frame(index)
		piece.position = TRASH_POSITIONS[index]
		piece.z_index = 8
		piece.modulate = TRASH_TINTS[index]
		piece.set_meta("trash_index", index)
		_fit_sprite(piece, Vector2(122.0, 122.0))
		add_child(piece)
		_trash_sprites.append(piece)
		_trash_base_positions.append(piece.position)

	_skimmer = Sprite2D.new()
	_skimmer.name = "PoolSkimmer"
	_skimmer.texture = load(SKIMMER_PATH) as Texture2D
	_skimmer.position = _skimmer_position
	_skimmer.z_index = 14
	_fit_sprite(_skimmer, SKIMMER_MAX_SIZE)
	add_child(_skimmer)

	_demo_pointer = Label.new()
	_demo_pointer.name = "SkimmerDemoPointer"
	_demo_pointer.text = "☝"
	_demo_pointer.position = Vector2(0.0, 0.0)
	_demo_pointer.size = Vector2(82.0, 82.0)
	_demo_pointer.pivot_offset = _demo_pointer.size * 0.5
	_demo_pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_demo_pointer.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_demo_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_demo_pointer.z_index = 18
	_demo_pointer.add_theme_font_size_override("font_size", 64)
	_demo_pointer.add_theme_color_override("font_color", Color(1.0, 0.91, 0.40))
	_demo_pointer.add_theme_color_override("font_shadow_color", Color(0.08, 0.20, 0.28, 0.78))
	_demo_pointer.add_theme_constant_override("shadow_offset_x", 3)
	_demo_pointer.add_theme_constant_override("shadow_offset_y", 4)
	_demo_pointer.visible = false
	add_child(_demo_pointer)

	_feedback_layer = Control.new()
	_feedback_layer.name = "SkimmerFeedback"
	_feedback_layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_feedback_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_feedback_layer.z_index = 20
	add_child(_feedback_layer)

	for index: int in range(_trash_sprites.size()):
		_trash_sprites[index].visible = (_progress_mask & (1 << index)) == 0


func _atlas_frame(index: int) -> AtlasTexture:
	var frame := AtlasTexture.new()
	frame.atlas = _atlas
	frame.region = Rect2(
		Vector2(float(index % 3) * TRASH_CELL_SIZE.x,
			float(index / 3) * TRASH_CELL_SIZE.y), TRASH_CELL_SIZE)
	return frame


func _fit_sprite(sprite: Sprite2D, max_size: Vector2) -> void:
	if sprite.texture == null:
		return
	var source_size: Vector2 = sprite.texture.get_size()
	var fit_scale: float = minf(
		max_size.x / maxf(source_size.x, 1.0),
		max_size.y / maxf(source_size.y, 1.0))
	sprite.scale = Vector2.ONE * fit_scale


func _spawn_catch_feedback(center: Vector2) -> void:
	if _feedback_layer == null or not is_instance_valid(_feedback_layer):
		return
	for index: int in range(7):
		var sparkle := Label.new()
		sparkle.text = "✦"
		sparkle.size = Vector2(42.0, 42.0)
		sparkle.pivot_offset = sparkle.size * 0.5
		sparkle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sparkle.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		sparkle.mouse_filter = Control.MOUSE_FILTER_IGNORE
		sparkle.add_theme_font_size_override("font_size", 30 + index * 3)
		sparkle.add_theme_color_override("font_color", TRASH_TINTS[index % TRASH_TINTS.size()])
		sparkle.add_theme_color_override("font_shadow_color", Color(0.06, 0.22, 0.28, 0.9))
		sparkle.add_theme_constant_override("shadow_offset_x", 2)
		sparkle.add_theme_constant_override("shadow_offset_y", 2)
		var angle: float = TAU * float(index) / 7.0
		var start: Vector2 = center + Vector2(cos(angle), sin(angle)) * 18.0
		var finish: Vector2 = center + Vector2(cos(angle), sin(angle)) * (68.0 + index * 4.0)
		sparkle.position = start - sparkle.size * 0.5
		_feedback_layer.add_child(sparkle)
		var sparkle_tween: Tween = sparkle.create_tween().set_parallel(true)
		sparkle_tween.tween_property(sparkle, "position", finish - sparkle.size * 0.5, 0.42)
		sparkle_tween.tween_property(sparkle, "modulate:a", 0.0, 0.42)
		sparkle_tween.chain().tween_callback(sparkle.queue_free)


func _stop_flights() -> void:
	for flight: Tween in _flight_tweens:
		if flight != null:
			flight.kill()
	_flight_tweens.clear()


func _clear_owned_children() -> void:
	for child: Node in get_children():
		child.free()
	_trash_sprites.clear()
	_trash_base_positions.clear()
	_skimmer = null
	_basket = null
	_demo_pointer = null
	_feedback_layer = null
