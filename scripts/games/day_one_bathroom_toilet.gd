class_name DayOneBathroomToilet
extends Control
## Final bathroom scrub. The demonstration never earns progress.
signal cleaned

const CENTER := Vector2(1040.0, 330.0)
const TOUCH_RADIUS := 145.0
const ARC_REQUIRED := TAU * 1.05
const DISTANCE_REQUIRED := 400.0
const MOTION_SECONDS_REQUIRED := 1.5
const HANDLE_PIXEL := Vector2(670.0, 320.0)
const BRISTLE_PIXEL := Vector2(300.0, 760.0)
const BRUSH_ANGLE := -PI * 0.5
const HAND := Vector2(43.7, 21.85)
const BRUSH := preload("res://assets/castle/day_one_art_studio/magic_cleaning_brush.png")
const POINTER := preload("res://assets/castle/training/ghost_hand.png")
const ROSHAN := preload("res://assets/characters/roshan_25d/roshan_directional.png")

var m: ReefMain
var _announcements: bool = true
var _finger: int = -1
var _last := Vector2.ZERO
var _arc: float = 0.0
var _distance: float = 0.0
var _motion: float = 0.0
var _pending_motion: bool = false
var _done: bool = false
var _arrived: bool = false
var _approaching: bool = false
var _focus_suspended: bool = false
var _pause_suspended: bool = false
var _time: float = 0.0
var _idle: float = 0.0
var _reprompts: int = 0
var _actor: Node2D
var _portrait: Sprite2D
var _brush: Sprite2D
var _grime: Sprite2D
var _pointer: Sprite2D
var _hand := HAND
var _room_visible: bool = true
var _shadow_visible: bool = true
var _claimed: bool = false

func setup(main: ReefMain, announcements: bool) -> void:
	m = main
	_announcements = announcements
	name = "ToiletCleaning"
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 45
	gui_input.connect(_on_input)
	_actor = Node2D.new()
	_actor.name = "RoshanCleaningToilet"
	_actor.position = Vector2(810.0, 470.0)
	add_child(_actor)
	_portrait = Sprite2D.new()
	var pose := AtlasTexture.new()
	pose.atlas = ROSHAN
	pose.region = Rect2(256.0, 0.0, 256.0, 256.0)
	_portrait.texture = pose
	_portrait.scale = Vector2.ONE * 0.95
	_actor.add_child(_portrait)
	if is_instance_valid(m.castle_room_player_sprite):
		var room: Sprite2D = m.castle_room_player_sprite
		_actor.position = get_global_transform().affine_inverse() * room.global_position
		if m.skin_id in ["fairy", "huluu"] and room.texture != null:
			_portrait.texture = room.texture
			_portrait.scale = Vector2.ONE * (243.2 / maxf(room.texture.get_width(), room.texture.get_height()))
			var hand_uv := Vector2(0.705, 0.552) if m.skin_id == "fairy" else Vector2(0.811, 0.353)
			_hand = (hand_uv - Vector2(0.5, 0.5)) * room.texture.get_size() * _portrait.scale
		_room_visible = room.visible
		room.visible = false
		_claimed = true
	_brush = Sprite2D.new()
	_brush.texture = BRUSH
	_brush.scale = Vector2.ONE * 0.12
	# The handle remains at Roshan's hand; the bristles work inside the bowl.
	_brush.offset = BRUSH.get_size() * 0.5 - HANDLE_PIXEL
	_brush.rotation = BRUSH_ANGLE
	_brush.position = _hand
	_actor.add_child(_brush)
	_grime = Sprite2D.new()
	_grime.texture = preload("res://assets/castle/dirty_cleanup_2d/targets/target_sink_grime_v1.png")
	_grime.position = CENTER
	_grime.scale = Vector2.ONE * 0.07
	_grime.modulate.a = 0.65
	_grime.z_index = -1
	add_child(_grime)
	_pointer = Sprite2D.new()
	_pointer.texture = POINTER
	_pointer.scale = Vector2.ONE * 0.10
	_pointer.visible = false
	add_child(_pointer)
	if is_instance_valid(m.castle_room_player_shadow):
		_shadow_visible = m.castle_room_player_shadow.visible
		m.castle_room_player_shadow.visible = false
	# Getting the brush into place is staging, like the earlier bathroom tools.
	# The child's first short touch must not strand Roshan halfway to the bowl.
	_approaching = true

func _exit_tree() -> void:
	cancel_gesture()
	_approaching = false
	if m == null or not is_instance_valid(m):
		return
	if _claimed and is_instance_valid(m.castle_room_player_sprite):
		m.castle_room_player_sprite.visible = _room_visible
	if is_instance_valid(m.castle_room_player_shadow):
		m.castle_room_player_shadow.visible = _shadow_visible

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		_focus_suspended = true
	elif what == NOTIFICATION_APPLICATION_FOCUS_IN:
		_focus_suspended = false
	elif what == NOTIFICATION_PAUSED:
		_pause_suspended = true
	elif what == NOTIFICATION_UNPAUSED:
		_pause_suspended = false
	else:
		return
	if _focus_suspended or _pause_suspended:
		cancel_gesture()
		_approaching = false
		if is_instance_valid(_pointer):
			_pointer.visible = false
	else:
		_approaching = not _arrived and not _done
	queue_redraw()

func _on_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			begin_gesture(touch.position, touch.index)
		elif touch.index == _finger:
			cancel_gesture()
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == _finger:
			move_gesture(drag.position)
		accept_event()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			begin_gesture(event.position, 0)
		else:
			cancel_gesture()
		accept_event()
	elif event is InputEventMouseMotion and _finger == 0:
		move_gesture(event.position)
		accept_event()

func begin_gesture(at: Vector2, finger: int = 0) -> bool:
	if _done or _focus_suspended or _pause_suspended \
			or _finger != -1 or at.distance_to(CENTER) > TOUCH_RADIUS:
		return false
	_finger = finger
	_last = at
	_idle = 0.0
	return true

func move_gesture(at: Vector2, seconds: float = 0.0) -> bool:
	if _done or _focus_suspended or _pause_suspended or _finger == -1 or not _arrived:
		_last = at
		return false
	if at.distance_to(CENTER) > TOUCH_RADIUS:
		_last = at
		return false
	var distance: float = _last.distance_to(at)
	if distance > 1.0 and _last.distance_to(CENTER) <= TOUCH_RADIUS:
		_arc += absf(wrapf((at - CENTER).angle() - (_last - CENTER).angle(), -PI, PI))
		_distance += distance
		_pending_motion = true
		_motion += clampf(seconds, 0.0, 0.10)
		_brush.rotation = BRUSH_ANGLE + sin((at - CENTER).angle()) * 0.16
		_idle = 0.0
	_last = at
	_grime.modulate.a = 0.65 * (1.0 - minf(0.92, minf(_arc / ARC_REQUIRED, _distance / DISTANCE_REQUIRED)))
	if _arc >= ARC_REQUIRED and _distance >= DISTANCE_REQUIRED and _motion >= MOTION_SECONDS_REQUIRED:
		_done = true
		cancel_gesture()
		_pointer.visible = false
		_grime.visible = false
		m.day_one_record_bathroom_toilet_cleaned()
		cleaned.emit()
	return _done

func cancel_gesture() -> void:
	_finger = -1
	_pending_motion = false

func _process(delta: float) -> void:
	_time += delta
	if _done or _focus_suspended or _pause_suspended:
		return
	var approaching_this_frame: bool = _approaching
	if _approaching:
		var destination: Vector2 = CENTER - _hand - ((BRISTLE_PIXEL - HANDLE_PIXEL) * _brush.scale).rotated(BRUSH_ANGLE)
		_actor.position = _actor.position.move_toward(destination, delta * 360.0)
		_arrived = _actor.position.distance_to(destination) < 1.0
		if _arrived:
			_approaching = false
			_idle = 0.0
			_announce()
	if _pending_motion and _finger != -1:
		_motion += minf(delta, 0.1)
	_pending_motion = false
	if _arrived and not approaching_this_frame:
		_idle += delta
	if _arrived and _idle >= (5.0 if _reprompts == 0 else 12.0) and _reprompts < 3:
		_reprompts += 1
		_idle = 0.0
		_announce()
	_pointer.visible = _arrived and _finger == -1
	_pointer.position = CENTER + Vector2(cos(_time * 2.2), sin(_time * 2.2)) * 48.0 + Vector2(-18.0, -44.0)
	queue_redraw()

func _draw() -> void:
	if _arrived and not _done and not _focus_suspended and not _pause_suspended \
			and _finger == -1:
		draw_arc(CENTER, 48.0, -0.8, TAU - 0.8, 28, Color(0.46, 0.91, 0.86, 0.7), 5.5, true)

func _announce() -> void:
	if _announcements and m != null:
		if m.hud_msg != null:
			m.hud_msg.text = "Little circles, scrubby-scrub!"
		m.say_day_one_context("day1_bathroom_sink_scrub", "Little circles, scrubby-scrub!", "bathroom", "bathroom_toilet_%d" % get_instance_id(), _reprompts)

func audit_snapshot() -> Dictionary:
	return {"done": _done, "arrived": _arrived, "approaching": _approaching,
		"suspended": _focus_suspended or _pause_suspended,
		"arc": _arc, "distance": _distance, "motion_seconds": _motion,
		"finger": _finger, "clean_progress": minf(0.92, minf(_arc / ARC_REQUIRED, _distance / DISTANCE_REQUIRED)),
		"hand_contact_error": _brush.position.distance_to(_hand),
		"bristle_contact_error": (_actor.position + _hand + ((BRISTLE_PIXEL - HANDLE_PIXEL) * _brush.scale).rotated(_brush.rotation)).distance_to(CENTER),
		"actor_position": _actor.position, "pointer_visible": _pointer.visible}
