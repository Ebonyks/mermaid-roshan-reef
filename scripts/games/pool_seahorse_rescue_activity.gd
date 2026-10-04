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
const BASKET_ANCHOR := Vector2(980.0, 560.0)
const TAP_REGION_GROWTH := 0.55
const BUBBLE_LIFETIME := 1.35
# Normalized centered-texture anchors: nozzle center (394, 322) in the
# 936x1024 seahorse and the far weed tip in the obstruction. Keeping these as
# explicit visual anchors makes the growth enter the mouth instead of hovering
# beside it; the broad toddler tap envelope remains independent below.
const SEAHORSE_MOUTH_ANCHOR := Vector2(394.0 / 936.0 - 0.5, 322.0 / 1024.0 - 0.5)
const PROP_NOZZLE_ANCHOR := Vector2(0.488, 0.184)
# Approved Day One guide and effect art; replaces code-drawn rings and dots.
const GUIDE_HAND_PATH := "res://assets/castle/training/ghost_hand.png"
const BUBBLES_PATH := "res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png"
const CLEAR_RING_PATH := "res://assets/castle/dirty_cleanup_2d/effects/fx_clean_ring.png"
const GUIDE_HAND_SIZE := 62.0
# Measured fingertip of the 512px ghost hand, relative to its centre.
const GUIDE_FINGERTIP := Vector2(-38.5, 191.0)
const GUIDE_IDLE_SECONDS := 2.0
# A deliberate pull away from the mouth earns a second tug in the same gesture,
# so purposeful pulling finishes in half the presses of tapping (DL-AGE-05).
const PULL_DISTANCE := 48.0
# Taps while Roshan is already tugging wait their turn instead of vanishing.
const MAX_QUEUED_TUGS := 3
const BEAD_SIZE := 18.0

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
var _mouth_anchor := Vector2.ZERO
var _prop_nozzle_offset := Vector2.ZERO
var _base_scale := Vector2.ONE
var _prop_scale := Vector2.ONE
var _basket_position := BASKET_ANCHOR
var _taps: int = 0
var _active := false
var _completed := false
var _completed_emitted := false
var _completion_started := false
var _contact_action: DayOneContactAction2D
var _touch_active := false
var _touch_id := -1
var _last_tap_time := -1.0
var _activity_time := 0.0
var _tug_strength := 0.0
var _tap_pulse := Vector2.ZERO
var _tap_pulse_time := 0.0
var _completion_tween: Tween = null
var _tug_tween: Tween = null
var _queued_tugs := 0
var _touch_start := Vector2.ZERO
var _pulled_this_touch := false
var _idle_time := 0.0
var _guide_hand: Sprite2D = null
var _bubbles_texture: Texture2D = null
var _clear_ring_texture: Texture2D = null
var _bead_sprites: Array[Sprite2D] = []


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	set_meta("canvas_only", true)
	set_meta("no_fail", true)
	set_meta("one_finger", true)


func setup(new_fixture_center: Vector2, new_fixture_size: Vector2,
		initial_taps: int = 0) -> void:
	_stop_tug_tween()
	_stop_completion_tween()
	_clear_owned_children()
	fixture_center = new_fixture_center
	fixture_size = Vector2(maxf(new_fixture_size.x, 1.0), maxf(new_fixture_size.y, 1.0))
	_fixture_rect = Rect2(fixture_center - fixture_size * 0.5, fixture_size)
	_tap_region = _fixture_rect.grow(maxf(fixture_size.x, fixture_size.y) * TAP_REGION_GROWTH)
	_taps = clampi(initial_taps, 0, TAP_TOTAL)
	_active = false
	_completed = _taps >= TAP_TOTAL
	_completed_emitted = false
	_completion_started = false
	_touch_active = false
	_touch_id = -1
	_last_tap_time = -1.0
	_activity_time = 0.0
	_tug_strength = 0.0
	_tap_pulse = fixture_center
	_tap_pulse_time = 0.0
	_queued_tugs = 0
	_pulled_this_touch = false
	_idle_time = 0.0
	_seahorse_texture = load(SEAHORSE_TEXTURE_PATH) as Texture2D
	_mouth_trash_texture = load(MOUTH_TRASH_TEXTURE_PATH) as Texture2D
	_basket_texture = load(BASKET_TEXTURE_PATH) as Texture2D
	_bubbles_texture = load(BUBBLES_PATH) as Texture2D
	_clear_ring_texture = load(CLEAR_RING_PATH) as Texture2D
	_build_activity_art()
	if _completed:
		_hide_rescued_art()
	_update_beads()
	_queue_progress_signal()
	queue_redraw()


## The temporary Roshan cutout used while she tugs, if any.
func identity_sprite() -> Sprite2D:
	return _contact_action.identity_sprite() if _contact_action != null else null


func bind_room_actor(actor: Sprite2D, shadow: Sprite2D, skin: String) -> void:
	_contact_action = DayOneContactAction2D.new()
	add_child(_contact_action)
	_contact_action.bind(actor, shadow, skin)


func start() -> void:
	_active = true
	_idle_time = 0.0
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(true)
	if _completed:
		_emit_completed_once()
	elif _taps >= TAP_TOTAL:
		_start_completion_flight()
	queue_redraw()


func stop() -> void:
	_active = false
	if _contact_action != null:
		_contact_action.cancel()
	cancel_touch()
	_stop_tug_tween()
	if not _completion_started:
		_set_tug_rotation(0.0)
	_stop_completion_tween()
	_completion_started = false
	_update_guide_hand()
	set_process(false)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_redraw()


func cancel_touch(cancel_work: bool = true) -> void:
	if cancel_work:
		# Unearned queued tugs belong to the interrupted work; none is paid later.
		_queued_tugs = 0
		if _contact_action != null:
			_contact_action.cancel()
	_touch_active = false
	_touch_id = -1
	_pulled_this_touch = false


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
		"queued_tugs": _queued_tugs,
		"pull_distance": PULL_DISTANCE,
		"guide_hand_visible": _guide_hand != null and is_instance_valid(_guide_hand)
			and _guide_hand.visible,
		"guide_hand_authored": _guide_hand != null and is_instance_valid(_guide_hand)
			and _guide_hand.texture != null
			and _guide_hand.texture.resource_path == GUIDE_HAND_PATH,
		"authored_progress_beads": _bead_sprites.size() == TAP_TOTAL,
		"code_drawn_effects": false,
	}


func _process(delta: float) -> void:
	_activity_time += maxf(delta, 0.0)
	_idle_time += maxf(delta, 0.0)
	_tap_pulse_time = maxf(_tap_pulse_time - maxf(delta, 0.0), 0.0)
	_tug_strength = move_toward(_tug_strength, 0.0, maxf(delta, 0.0) * 1.6)
	_update_guide_hand()


func _gui_input(event: InputEvent) -> void:
	if not _active or _completed or _completion_started:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.canceled:
			if _touch_active and touch.index == _touch_id:
				cancel_touch()
		elif touch.pressed:
			if not _touch_active:
				_begin_press(touch.index, touch.position)
		else:
			if _touch_active and touch.index == _touch_id:
				cancel_touch(false)
		accept_event()
		return
	if event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if _touch_active and drag.index == _touch_id:
			_check_pull(drag.position)
		accept_event()
		return
	if event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed:
			if not _touch_active:
				_begin_press(0, button.position)
		else:
			if _touch_active and _touch_id == 0:
				cancel_touch(false)
		accept_event()
		return
	if event is InputEventMouseMotion and _touch_active and _touch_id == 0:
		_check_pull((event as InputEventMouseMotion).position)
		accept_event()


func _begin_press(touch_id: int, point: Vector2) -> void:
	_touch_active = true
	_touch_id = touch_id
	_touch_start = point
	_pulled_this_touch = false
	_register_tap(point)


func _check_pull(point: Vector2) -> void:
	# One pull per press: dragging the trash away from the mouth is the strong,
	# purposeful version of the tug and counts once more.
	if _pulled_this_touch or point.distance_to(_touch_start) < PULL_DISTANCE:
		return
	_pulled_this_touch = true
	_register_tap(_touch_start)


func _register_tap(point: Vector2) -> void:
	if not _active or _completed or _completion_started or _taps >= TAP_TOTAL:
		return
	# The generous envelope belongs to the visible seahorse, even when this
	# activity owns a full-screen Control. Off-target taps preserve progress.
	if not _tap_region.has_point(point):
		return
	_idle_time = 0.0
	if _contact_action != null and _contact_action.available():
		if _contact_action.active:
			# Roshan is already on her way or tugging: this tap waits its turn and
			# answers at once, so a quick child never loses a tap.
			_queued_tugs = mini(_queued_tugs + 1,
				mini(MAX_QUEUED_TUGS, maxi(TAP_TOTAL - _taps - 1, 0)))
			_add_bubbles(_prop_rest_position, 0.4)
			return
		_contact_action.request(_prop_rest_position, Callable(self, "_finish_tug"))
		return
	_finish_tug()


func _finish_tug() -> void:
	if not _active or _completed or _completion_started:
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
	_idle_time = 0.0
	_add_bubbles(_prop_rest_position, _tug_strength)
	_update_tug_visual()
	_update_beads()
	progress_changed.emit(_taps)
	if _taps >= TAP_TOTAL:
		_queued_tugs = 0
		_start_completion_flight()
	elif _queued_tugs > 0 and _contact_action != null and _contact_action.available() \
			and not _contact_action.active:
		# Each waiting tap is its own tug: Roshan's hand stays on the trash and
		# does the full local work again before the next one is paid.
		_queued_tugs -= 1
		_contact_action.request(_prop_rest_position, Callable(self, "_finish_tug"))
	queue_redraw()


func _update_tug_visual() -> void:
	if _mouth_trash == null or not is_instance_valid(_mouth_trash):
		return
	_stop_tug_tween()
	var progress := float(_taps) / float(TAP_TOTAL)
	var tug_angle := -lerpf(0.06, 0.18, progress) * (0.82 + _tug_strength * 0.18)
	_tug_tween = _mouth_trash.create_tween().set_trans(Tween.TRANS_BACK) \
		.set_ease(Tween.EASE_OUT)
	# Rotate around the embedded stem tip, not the texture center. The blockage
	# stays in the mouth until the final extraction, including during rapid taps.
	_tug_tween.tween_method(_set_tug_rotation, _mouth_trash.rotation, tug_angle, 0.16)
	_tug_tween.tween_method(_set_tug_rotation, tug_angle, 0.0, 0.20)
	# A quick cadence gives a stronger, springier tug, but this duration is
	# still short enough that slow taps visibly settle before the next one.
	if _tug_strength > 0.72:
		_tug_tween.set_speed_scale(1.18)


func _set_tug_rotation(angle: float) -> void:
	if _mouth_trash == null or not is_instance_valid(_mouth_trash):
		return
	_mouth_trash.rotation = angle
	_mouth_trash.position = _mouth_anchor - _prop_nozzle_offset.rotated(angle)


func _stop_tug_tween() -> void:
	if _tug_tween != null:
		_tug_tween.kill()
	_tug_tween = null


func _start_completion_flight() -> void:
	if _completion_started or _completed:
		return
	_stop_tug_tween()
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
	# Keep the recovered prop readable through basket contact, then let the rim
	# swallow it instead of fading a floating token in mid-air.
	_completion_tween.tween_property(
		_mouth_trash, "modulate:a", 0.0, 0.10).set_delay(0.50)
	if _basket != null and is_instance_valid(_basket):
		var basket_settle: Tween = _basket.create_tween()
		basket_settle.tween_interval(0.46)
		basket_settle.tween_property(
			_basket, "position:y", _basket_position.y + 5.0, 0.08)
		basket_settle.tween_property(
			_basket, "position:y", _basket_position.y, 0.14) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
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
	_pop_clear_ring(_prop_rest_position)
	_update_guide_hand()
	_emit_completed_once()
	queue_redraw()


func _emit_completed_once() -> void:
	if _completed_emitted:
		return
	_completed_emitted = true
	completed.emit()


func _build_activity_art() -> void:
	var base_dimension := minf(fixture_size.x, fixture_size.y)
	if _seahorse_texture != null:
		_seahorse = Sprite2D.new()
		_seahorse.name = "SickSeahorseBase"
		_seahorse.texture = _seahorse_texture
		_seahorse.position = fixture_center
		_seahorse.z_index = 2
		_base_scale = _fit_scale(_seahorse_texture, fixture_size * 0.96)
		_seahorse.scale = _base_scale
		_seahorse.modulate = Color(0.84, 0.90, 0.82, 0.98)
		add_child(_seahorse)

	if _mouth_trash_texture != null:
		_mouth_trash = Sprite2D.new()
		_mouth_trash.name = "MouthTrashPullProp"
		_mouth_trash.texture = _mouth_trash_texture
		_prop_scale = _fit_scale(_mouth_trash_texture,
			Vector2(base_dimension * 0.62, base_dimension * 0.62))
		_mouth_trash.scale = _prop_scale
		# Register the prop's right-hand weed tip to the seahorse's authored
		# mouth anchor. These visual anchors are independent of the broad hit box.
		_mouth_anchor = fixture_center
		if _seahorse != null:
			_mouth_anchor = _seahorse.position + _seahorse.texture.get_size() \
				* _seahorse.scale * SEAHORSE_MOUTH_ANCHOR
		var prop_display_size: Vector2 = _mouth_trash_texture.get_size() * _prop_scale
		_prop_nozzle_offset = prop_display_size * PROP_NOZZLE_ANCHOR
		_prop_rest_position = _mouth_anchor - _prop_nozzle_offset
		_mouth_trash.position = _prop_rest_position
		_mouth_trash.z_index = 6
		_mouth_trash.modulate = Color(0.78, 0.82, 0.68, 0.96)
		add_child(_mouth_trash)

	if _basket_texture != null:
		_basket = Sprite2D.new()
		_basket.name = "RescueCleanupBasket"
		_basket.texture = _basket_texture
		_basket_position = _resolve_basket_position()
		_basket.position = _basket_position
		_basket.z_index = 320
		_basket.scale = _fit_scale(_basket_texture, Vector2(145.0, 112.0))
		_basket.modulate = Color(0.84, 0.88, 0.82, 0.96)
		add_child(_basket)

	_feedback_layer = Control.new()
	_feedback_layer.name = "SeahorseRescueFeedback"
	_feedback_layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_feedback_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_feedback_layer.z_index = 20
	add_child(_feedback_layer)

	# Progress reads as eight approved soap bubbles under the seahorse.
	_bead_sprites.clear()
	if _bubbles_texture != null:
		var bead_start := fixture_center + Vector2(-84.0, fixture_size.y * 0.48)
		for index in range(TAP_TOTAL):
			var bead := Sprite2D.new()
			bead.name = "TugProgressBubble%d" % index
			bead.texture = _bubbles_texture
			bead.position = bead_start + Vector2(float(index) * 24.0, 0.0)
			bead.z_index = 7
			add_child(bead)
			_bead_sprites.append(bead)

	var guide_texture := load(GUIDE_HAND_PATH) as Texture2D
	if guide_texture != null:
		_guide_hand = Sprite2D.new()
		_guide_hand.name = "SeahorseTugGuideHand"
		_guide_hand.texture = guide_texture
		_guide_hand.scale = Vector2.ONE * GUIDE_HAND_SIZE / maxf(guide_texture.get_width(), 1.0)
		_guide_hand.z_index = 520
		_guide_hand.visible = false
		add_child(_guide_hand)


func _hide_rescued_art() -> void:
	if _seahorse != null and is_instance_valid(_seahorse):
		_seahorse.visible = false
	if _mouth_trash != null and is_instance_valid(_mouth_trash):
		_mouth_trash.visible = false
	for bead: Sprite2D in _bead_sprites:
		if bead != null and is_instance_valid(bead):
			bead.visible = false


func _update_beads() -> void:
	if _bubbles_texture == null:
		return
	var full := BEAD_SIZE / maxf(_bubbles_texture.get_width(), 1.0)
	for index in range(_bead_sprites.size()):
		var bead := _bead_sprites[index]
		if bead == null or not is_instance_valid(bead):
			continue
		var filled := index < _taps
		bead.scale = Vector2.ONE * full * (1.0 if filled else 0.72)
		bead.modulate = Color(1.0, 1.0, 1.0, 1.0 if filled else 0.32)


func _update_guide_hand() -> void:
	if _guide_hand == null or not is_instance_valid(_guide_hand):
		return
	var working := _contact_action != null and _contact_action.active
	var demonstrating := _active and not _completed and not _completion_started \
		and not working and not _touch_active and _idle_time >= GUIDE_IDLE_SECONDS
	_guide_hand.visible = demonstrating
	if not demonstrating:
		return
	# A small tap-tap bob right on the trash in the mouth: the live target.
	var bob := absf(sin(_activity_time * 3.4)) * -14.0
	var fingertip := _prop_rest_position + Vector2(0.0, -10.0 + bob)
	_guide_hand.position = fingertip - GUIDE_FINGERTIP * _guide_hand.scale


func _pop_clear_ring(center: Vector2) -> void:
	if _clear_ring_texture == null or _feedback_layer == null \
			or not is_instance_valid(_feedback_layer):
		return
	var ring := Sprite2D.new()
	ring.name = "SeahorseFreeRing"
	ring.texture = _clear_ring_texture
	ring.position = center
	var base := Vector2.ONE * 150.0 / maxf(_clear_ring_texture.get_width(), 1.0)
	ring.scale = base * 0.5
	_feedback_layer.add_child(ring)
	var tween := ring.create_tween().set_parallel(true)
	tween.tween_property(ring, "scale", base, 0.45).set_trans(Tween.TRANS_BACK) \
		.set_ease(Tween.EASE_OUT)
	tween.tween_property(ring, "modulate:a", 0.0, 0.32).set_delay(0.34)
	tween.chain().tween_callback(ring.queue_free)


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
	# Approved soap-bubble clusters drift up and fade; each owns its own tween.
	if _bubbles_texture == null or _feedback_layer == null \
			or not is_instance_valid(_feedback_layer):
		return
	var count := 2 if strength < 0.72 else 4
	for index in range(count):
		var angle := TAU * float(index) / float(count) - 0.45
		var bubble := Sprite2D.new()
		bubble.name = "TugBubble"
		bubble.texture = _bubbles_texture
		var size_px := 16.0 + fmod(float(index), 3.0) * 6.0 + strength * 6.0
		bubble.scale = Vector2.ONE * size_px / maxf(_bubbles_texture.get_width(), 1.0)
		bubble.position = center + Vector2(cos(angle), sin(angle)) * (12.0 + index * 3.0)
		_feedback_layer.add_child(bubble)
		var life := BUBBLE_LIFETIME - float(index % 3) * 0.12
		var drift := Vector2(cos(angle) * (13.0 + strength * 14.0),
			-28.0 - strength * 24.0 - index * 2.0) * life
		var tween := bubble.create_tween().set_parallel(true)
		tween.tween_property(bubble, "position", bubble.position + drift, life)
		tween.tween_property(bubble, "modulate:a", 0.0, life).set_ease(Tween.EASE_IN)
		tween.chain().tween_callback(bubble.queue_free)


func _spawn_rescue_bubbles() -> void:
	_add_bubbles(_prop_rest_position, 1.0)
	_add_bubbles(_basket_position, 1.0)


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
	_guide_hand = null
	_bead_sprites.clear()
