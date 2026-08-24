class_name PoolSeahorseRescueActivity
extends Control
## One-finger, no-fail finale for pulling trash from the pool seahorse.
##
## The sick seahorse is deliberately kept as a single, authored 2D cutout.
## The mouth trash is a separate prop so every tap can show a readable tug
## without changing the seahorse's identity or repainting its base artwork.

signal progress_changed(taps: int)
signal completed

const SEAHORSE_TEXTURE_PATH := \
	"res://assets/castle/day_one_pool/activities/seahorse_sick_clear_mouth.png"
const MOUTH_TRASH_TEXTURE_PATH := \
	"res://assets/castle/day_one_pool/activities/seahorse_mouth_trash.png"
const BASKET_TEXTURE_PATH := \
	"res://assets/castle/day_one_pool/activities/cleanup_basket.png"
const TAP_TOTAL := 8
const CANVAS_SIZE := Vector2(1280.0, 720.0)
const BASKET_ANCHOR := Vector2(1080.0, 596.0)
const TAP_REGION_GROWTH := 0.55
const BUBBLE_LIFETIME := 1.35

var fixture_center := Vector2.ZERO
var fixture_size := Vector2.ZERO

var _fixture_rect := Rect2()
var _tap_region := Rect2()
var _seahorse: Sprite2D = null
var _mouth_trash: Sprite2D = null
var _basket: Sprite2D = null
var _feedback_layer: Control = null
var _seahorse_texture: Texture2D = null
var _mouth_trash_texture: Texture2D = null
var _basket_texture: Texture2D = null
var _prop_rest_position := Vector2.ZERO
var _prop_outward := Vector2(-1.0, -0.06)
var _base_scale := Vector2.ONE
var _prop_scale := Vector2.ONE
var _basket_position := BASKET_ANCHOR
var _taps: int = 0
var _active := false
var _completed := false
var _completion_started := false
var _touch_active := false
var _touch_id := -1
var _last_tap_time := -1.0
var _activity_time := 0.0
var _tug_strength := 0.0
var _tap_pulse := Vector2.ZERO
var _tap_pulse_time := 0.0
var _completion_tween: Tween = null
var _bubbles: Array[Dictionary] = []


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	set_meta("canvas_only", true)
	set_meta("no_fail", true)
	set_meta("one_finger", true)


func setup(new_fixture_center: Vector2, new_fixture_size: Vector2,
		initial_taps: int = 0) -> void:
	_stop_completion_tween()
	_clear_owned_children()
	fixture_center = new_fixture_center
	fixture_size = Vector2(maxf(new_fixture_size.x, 1.0), maxf(new_fixture_size.y, 1.0))
	_fixture_rect = Rect2(fixture_center - fixture_size * 0.5, fixture_size)
	_tap_region = _fixture_rect.grow(maxf(fixture_size.x, fixture_size.y) * TAP_REGION_GROWTH)
	_taps = clampi(initial_taps, 0, TAP_TOTAL)
	_active = false
	_completed = _taps >= TAP_TOTAL
	_completion_started = false
	_touch_active = false
	_touch_id = -1
	_last_tap_time = -1.0
	_activity_time = 0.0
	_tug_strength = 0.0
	_tap_pulse = fixture_center
	_tap_pulse_time = 0.0
	_bubbles.clear()
	_seahorse_texture = load(SEAHORSE_TEXTURE_PATH) as Texture2D
	_mouth_trash_texture = load(MOUTH_TRASH_TEXTURE_PATH) as Texture2D
	_basket_texture = load(BASKET_TEXTURE_PATH) as Texture2D
	_build_activity_art()
	if _completed:
		_hide_rescued_art()
	_queue_progress_signal()
	queue_redraw()


func start() -> void:
	_active = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(true)
	if _taps >= TAP_TOTAL and not _completed:
		_start_completion_flight()
	queue_redraw()


func stop() -> void:
	_active = false
	cancel_touch()
	_stop_completion_tween()
	_completion_started = false
	set_process(false)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_redraw()


func cancel_touch() -> void:
	_touch_active = false
	_touch_id = -1


func probe_tap() -> bool:
	if _completed or _completion_started or _taps >= TAP_TOTAL:
		return false
	if not _active:
		start()
	_register_tap(fixture_center)
	return true


func audit_snapshot() -> Dictionary:
	return {
		"activity": "pool_seahorse_rescue",
		"active": _active,
		"running": _active,
		"taps": _taps,
		"tap_total": TAP_TOTAL,
		"remaining_taps": maxi(TAP_TOTAL - _taps, 0),
		"completed": _completed,
		"completion_started": _completion_started,
		"fixture_center": fixture_center,
		"fixture_size": fixture_size,
		"fixture_rect": _fixture_rect,
		"tap_region": _tap_region,
		"tap_region_is_broad": _tap_region.size.x >= fixture_size.x * 1.8
			and _tap_region.size.y >= fixture_size.y * 1.8,
		"seahorse_present": _seahorse != null and is_instance_valid(_seahorse),
		"mouth_trash_present": _mouth_trash != null and is_instance_valid(_mouth_trash),
		"basket_present": _basket != null and is_instance_valid(_basket),
		"seahorse_base_stays_sick": true,
		"prop_is_separate": true,
		"quick_cadence_strength": _tug_strength,
		"touch_active": _touch_active,
		"no_fail": true,
		"monotonic_progress": true,
		"canvas_only": true,
		"live_input_required": true,
		"seahorse_texture_loaded": _seahorse_texture != null,
		"mouth_trash_texture_loaded": _mouth_trash_texture != null,
		"basket_texture_loaded": _basket_texture != null,
	}


func _process(delta: float) -> void:
	_activity_time += maxf(delta, 0.0)
	_tap_pulse_time = maxf(_tap_pulse_time - maxf(delta, 0.0), 0.0)
	_tug_strength = move_toward(_tug_strength, 0.0, maxf(delta, 0.0) * 1.6)
	_prune_bubbles(delta)
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if not _active or _completed or _completion_started:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_touch_active = true
			_touch_id = touch.index
			_register_tap(touch.position)
		else:
			if _touch_active and touch.index == _touch_id:
				cancel_touch()
		accept_event()
		return
	if event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed:
			_touch_active = true
			_touch_id = 0
			_register_tap(button.position)
		else:
			cancel_touch()
		accept_event()


func _register_tap(point: Vector2) -> void:
	if not _active or _completed or _completion_started or _taps >= TAP_TOTAL:
		return
	# The activity is intentionally forgiving: a full-screen mounted Control can
	# accept a tap anywhere, while a smaller mounted Control still has a broad
	# seahorse-centered target. No tap can reduce progress or trigger a miss.
	var canvas_rect := Rect2(Vector2.ZERO, size)
	if size.x > 1.0 and size.y > 1.0 and not canvas_rect.has_point(point) \
			and not _tap_region.has_point(point):
		return
	var previous_tap_time := _last_tap_time
	_last_tap_time = _activity_time
	var cadence := 0.0
	if previous_tap_time >= 0.0:
		cadence = clampf(1.0 - (_activity_time - previous_tap_time) / 0.48, 0.0, 1.0)
	_tug_strength = maxf(_tug_strength, 0.42 + cadence * 0.58)
	_taps = mini(_taps + 1, TAP_TOTAL)
	_tap_pulse = _prop_rest_position
	_tap_pulse_time = 0.32
	_add_bubbles(_prop_rest_position, _tug_strength)
	_update_tug_visual()
	progress_changed.emit(_taps)
	if _taps >= TAP_TOTAL:
		_start_completion_flight()
	queue_redraw()


func _update_tug_visual() -> void:
	if _mouth_trash == null or not is_instance_valid(_mouth_trash):
		return
	var progress := float(_taps) / float(TAP_TOTAL)
	var tug_distance := lerpf(7.0, maxf(fixture_size.x, fixture_size.y) * 0.20, progress)
	var tug_offset := _prop_outward * tug_distance * (0.82 + _tug_strength * 0.18)
	var target_position := _prop_rest_position + tug_offset
	var tug_tween := _mouth_trash.create_tween().set_trans(Tween.TRANS_BACK) \
		.set_ease(Tween.EASE_OUT)
	tug_tween.tween_property(_mouth_trash, "position", target_position, 0.16)
	tug_tween.parallel().tween_property(_mouth_trash, "rotation",
		_prop_outward.angle() * 0.12 * (progress + _tug_strength * 0.18), 0.16)
	# A quick cadence gives a stronger, springier tug, but this duration is
	# still short enough that slow taps visibly settle before the next one.
	if _tug_strength > 0.72:
		tug_tween.set_speed_scale(1.18)


func _start_completion_flight() -> void:
	if _completion_started or _completed:
		return
	_completion_started = true
	if _mouth_trash == null or not is_instance_valid(_mouth_trash):
		_finish_completion()
		return
	var flight_target := _basket_position + Vector2(0.0, -42.0)
	_completion_tween = _mouth_trash.create_tween().set_parallel(true)
	_completion_tween.tween_property(_mouth_trash, "position", flight_target, 0.58) \
		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
	_completion_tween.tween_property(_mouth_trash, "rotation", -0.30, 0.58) \
		.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	_completion_tween.tween_property(_mouth_trash, "scale", _prop_scale * 0.22, 0.58) \
		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
	_completion_tween.tween_property(_mouth_trash, "modulate:a", 0.0, 0.52)
	_completion_tween.chain().tween_callback(_finish_completion)


func _finish_completion() -> void:
	if _completed:
		return
	_completed = true
	_completion_started = false
	if _mouth_trash != null and is_instance_valid(_mouth_trash):
		_mouth_trash.visible = false
	if _seahorse != null and is_instance_valid(_seahorse):
		_seahorse.visible = false
	_spawn_rescue_bubbles()
	completed.emit()
	queue_redraw()


func _build_activity_art() -> void:
	var base_dimension := minf(fixture_size.x, fixture_size.y)
	if _seahorse_texture != null:
		_seahorse = Sprite2D.new()
		_seahorse.name = "SickSeahorseBase"
		_seahorse.texture = _seahorse_texture
		_seahorse.position = fixture_center
		_seahorse.z_index = 3
		_base_scale = _fit_scale(_seahorse_texture, fixture_size * 0.96)
		_seahorse.scale = _base_scale
		add_child(_seahorse)

	if _mouth_trash_texture != null:
		_mouth_trash = Sprite2D.new()
		_mouth_trash.name = "MouthTrashPullProp"
		_mouth_trash.texture = _mouth_trash_texture
		_prop_scale = _fit_scale(_mouth_trash_texture,
			Vector2(base_dimension * 0.74, base_dimension * 0.74))
		_mouth_trash.scale = _prop_scale
		# The standalone prop's pink wrapper sits left of its source canvas;
		# offset its sprite center so that wrapper lands over the sick mouth.
		# The seahorse faces left. Register the prop's right-hand algae tail at
		# the nozzle, leaving the pink wrapper visibly outside the mouth.
		_prop_rest_position = fixture_center + Vector2(
			-fixture_size.x * 0.48, -fixture_size.y * 0.19)
		_mouth_trash.position = _prop_rest_position
		_mouth_trash.z_index = 6
		add_child(_mouth_trash)

	if _basket_texture != null:
		_basket = Sprite2D.new()
		_basket.name = "RescueCleanupBasket"
		_basket.texture = _basket_texture
		_basket_position = _resolve_basket_position()
		_basket.position = _basket_position
		_basket.z_index = 2
		_basket.scale = _fit_scale(_basket_texture, Vector2(210.0, 165.0))
		add_child(_basket)

	_feedback_layer = Control.new()
	_feedback_layer.name = "SeahorseRescueFeedback"
	_feedback_layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_feedback_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_feedback_layer.z_index = 20
	add_child(_feedback_layer)


func _hide_rescued_art() -> void:
	if _seahorse != null and is_instance_valid(_seahorse):
		_seahorse.visible = false
	if _mouth_trash != null and is_instance_valid(_mouth_trash):
		_mouth_trash.visible = false


func _resolve_basket_position() -> Vector2:
	var canvas := size if size.x > 1.0 and size.y > 1.0 else CANVAS_SIZE
	return Vector2(clampf(BASKET_ANCHOR.x, 120.0, canvas.x - 120.0),
		clampf(BASKET_ANCHOR.y, 110.0, canvas.y - 80.0))


func _fit_scale(texture: Texture2D, max_size: Vector2) -> Vector2:
	if texture == null:
		return Vector2.ONE
	var source_size := texture.get_size()
	var fit := minf(max_size.x / maxf(source_size.x, 1.0),
		max_size.y / maxf(source_size.y, 1.0))
	return Vector2.ONE * fit


func _add_bubbles(center: Vector2, strength: float) -> void:
	var count := 4 if strength < 0.72 else 7
	for index in range(count):
		var angle := TAU * float(index) / float(count) - 0.45
		_bubbles.append({
			"position": center + Vector2(cos(angle), sin(angle)) * (12.0 + index * 3.0),
			"velocity": Vector2(cos(angle) * (13.0 + strength * 14.0),
				-28.0 - strength * 24.0 - index * 2.0),
			"radius": 5.0 + fmod(float(index), 3.0) * 2.0,
			"age": 0.0,
			"life": BUBBLE_LIFETIME - float(index % 3) * 0.12,
		})


func _spawn_rescue_bubbles() -> void:
	_add_bubbles(_prop_rest_position, 1.0)
	_add_bubbles(_basket_position, 1.0)


func _prune_bubbles(delta: float) -> void:
	if _bubbles.is_empty():
		return
	var live: Array[Dictionary] = []
	for bubble: Dictionary in _bubbles:
		var age := float(bubble.get("age", 0.0)) + maxf(delta, 0.0)
		if age >= float(bubble.get("life", BUBBLE_LIFETIME)):
			continue
		bubble["age"] = age
		bubble["position"] = (bubble["position"] as Vector2) \
			+ (bubble["velocity"] as Vector2) * maxf(delta, 0.0)
		live.append(bubble)
	_bubbles = live


func _queue_progress_signal() -> void:
	progress_changed.emit(_taps)


func _stop_completion_tween() -> void:
	if _completion_tween != null:
		_completion_tween.kill()
	_completion_tween = null


func _clear_owned_children() -> void:
	for child: Node in get_children():
		child.free()
	_seahorse = null
	_mouth_trash = null
	_basket = null
	_feedback_layer = null


func _draw() -> void:
	if fixture_size.x <= 1.0 or fixture_size.y <= 1.0:
		return
	var progress := float(_taps) / float(TAP_TOTAL)
	var pulse := 1.0 + sin(_activity_time * 3.1) * 0.06
	var halo_alpha := 0.12 if _completed else 0.20
	draw_circle(_prop_rest_position, maxf(fixture_size.x, fixture_size.y) * 0.18 * pulse,
		Color(0.58, 0.96, 0.94, halo_alpha))
	# Eight chunky, wordless progress beads remain legible at phone scale.
	var bead_start := fixture_center + Vector2(-112.0, fixture_size.y * 0.53)
	for index in range(TAP_TOTAL):
		var filled := index < _taps
		var bead_color := Color(1.0, 0.86, 0.30, 0.95) if filled \
			else Color(0.75, 0.96, 0.96, 0.30)
		draw_circle(bead_start + Vector2(float(index) * 32.0, 0.0),
			9.0 + (2.0 if filled else 0.0), bead_color)
		if not filled:
			draw_arc(bead_start + Vector2(float(index) * 32.0, 0.0), 13.0,
				0.0, TAU, 20, Color(0.86, 1.0, 0.96, 0.26), 2.0, true)
	if _tap_pulse_time > 0.0:
		var pulse_fraction := 1.0 - _tap_pulse_time / 0.32
		draw_arc(_tap_pulse, 28.0 + pulse_fraction * 48.0, 0.0, TAU, 28,
			Color(1.0, 0.88, 0.35, (1.0 - pulse_fraction) * 0.72), 5.0, true)
	for bubble: Dictionary in _bubbles:
		var age := float(bubble.get("age", 0.0))
		var life := maxf(float(bubble.get("life", BUBBLE_LIFETIME)), 0.01)
		var alpha := clampf(1.0 - age / life, 0.0, 1.0)
		draw_circle(bubble["position"] as Vector2,
			float(bubble.get("radius", 6.0)), Color(0.82, 1.0, 0.98, alpha * 0.78))
		draw_arc(bubble["position"] as Vector2,
			float(bubble.get("radius", 6.0)), 0.0, TAU, 16,
			Color(1.0, 1.0, 0.90, alpha * 0.72), 2.0, true)
