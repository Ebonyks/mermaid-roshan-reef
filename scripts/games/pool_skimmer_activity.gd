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
const BASKET_POSITION := Vector2(980.0, 560.0)
const SKIMMER_MAX_SIZE := Vector2(205.0, 150.0)
const BASKET_MAX_SIZE := Vector2(145.0, 112.0)
const ROSHAN_ATLAS := preload("res://assets/characters/roshan_25d/roshan_directional.png")
# Measured on the existing art: right hand in directional cell 1, handle
# grip and net centre in the complete 1024x682 skimmer. No art is regenerated.
const HAND_OFFSET := Vector2(46.0, 23.0) * 0.95
const HANDLE_PIXEL := Vector2(100.0, 580.0)
const NET_PIXEL := Vector2(780.0, 190.0)
const SWIM_SPEED := 440.0
const CONTACT_RADIUS := 24.0
const SCOOP_SECONDS := 0.42
# Approved Day One guide and effect art; replaces the emoji pointer and glyph sparkles.
const GUIDE_HAND_PATH := "res://assets/castle/training/ghost_hand.png"
const BUBBLES_PATH := "res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png"
const CLEAR_RING_PATH := "res://assets/castle/dirty_cleanup_2d/effects/fx_clean_ring.png"
const GUIDE_HAND_SIZE := 60.0
# Measured fingertip of the 512px ghost hand, relative to its centre.
const GUIDE_FINGERTIP := Vector2(-38.5, 191.0)
const POOL_VISUAL_BOUNDS := Rect2(170.0, 220.0, 940.0, 250.0)
const TRASH_POSITIONS: Array[Vector2] = [
	Vector2(310.0, 316.0),
	Vector2(535.0, 276.0),
	Vector2(795.0, 292.0),
	Vector2(404.0, 401.0),
	Vector2(676.0, 425.0),
	Vector2(955.0, 382.0),
]
const TRASH_TINTS: Array[Color] = [
	Color(0.78, 0.83, 0.71, 0.90),
	Color(0.70, 0.81, 0.74, 0.90),
	Color(0.72, 0.82, 0.78, 0.88),
	Color(0.82, 0.80, 0.64, 0.90),
	Color(0.72, 0.76, 0.80, 0.88),
	Color(0.78, 0.82, 0.68, 0.90),
]
const TRASH_MAX_SIZES: Array[Vector2] = [
	Vector2(68.0, 68.0),
	Vector2(62.0, 62.0),
	Vector2(66.0, 66.0),
	Vector2(82.0, 82.0),
	Vector2(88.0, 88.0),
	Vector2(78.0, 78.0),
]
const TRASH_ROTATIONS: Array[float] = [
	-0.13, 0.09, -0.05, 0.18, -0.10, 0.08,
]

var _progress_mask: int = 0
var _running: bool = false
var _dragging: bool = false
var _completed: bool = false
var _completed_emitted: bool = false
var _demo_time: float = 0.0
var _last_input_time: float = 0.0
var _skimmer_position := Vector2(640.0, 380.0)
var _trash_sprites: Array[Sprite2D] = []
var _trash_base_positions: Array[Vector2] = []
var _flight_tweens: Array[Tween] = []
var _skimmer: Sprite2D = null
var _basket: Sprite2D = null
var _demo_pointer: Sprite2D = null
var _feedback_layer: Control = null
var _bubbles_texture: Texture2D = null
var _clear_ring_texture: Texture2D = null
var _atlas: Texture2D = null
var _cleaner: Node2D = null
var _roshan: Sprite2D = null
var _room_roshan: Sprite2D = null
var _room_shadow: Sprite2D = null
var _room_visibility: bool = true
var _shadow_visibility: bool = true
var _owns_actor: bool = false
var _target_index: int = -1
var _scoop_time: float = 0.0
var _owned_touch: int = -1
var _hand_offset: Vector2 = HAND_OFFSET


func setup(initial_mask: int = 0) -> void:
	_release_room_actor()
	_stop_flights()
	_clear_owned_children()
	_progress_mask = initial_mask & ALL_MASK
	_running = false
	_dragging = false
	_completed = _progress_mask == ALL_MASK
	_completed_emitted = false
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
	if not _completed:
		_claim_room_actor()
	if _demo_pointer != null and is_instance_valid(_demo_pointer):
		_demo_pointer.visible = not _completed
	if _completed:
		_emit_completed_once()
	set_process(true)
	queue_redraw()


func stop() -> void:
	_running = false
	_dragging = false
	cancel_touch()
	_release_room_actor()
	_stop_flights()
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	if _demo_pointer != null and is_instance_valid(_demo_pointer):
		_demo_pointer.visible = false
	set_process(false)


func cancel_touch() -> void:
	_dragging = false
	_owned_touch = -1
	_target_index = -1
	_scoop_time = 0.0
	if _cleaner != null:
		_cleaner.rotation = 0.0
	_last_input_time = _demo_time


func probe_collect_next() -> bool:
	if _completed:
		return false
	if not _running:
		start()
	for index: int in range(TRASH_COUNT):
		if (_progress_mask & (1 << index)) == 0:
			_begin_live_drag(_trash_contact_position(index))
			_dragging = false
			# Exercise the same travel/contact/action gate in bounded simulation.
			for _tick: int in range(240):
				_advance_cleaning(1.0 / 60.0)
				if (_progress_mask & (1 << index)) != 0:
					return true
			return false
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
		"basket_visible": _basket != null and is_instance_valid(_basket)
			and _basket.visible,
		"trash_sprite_count": _trash_sprites.size(),
		"atlas_cell_size": TRASH_CELL_SIZE,
		"catch_radius": CATCH_RADIUS,
		"roshan_present": _roshan != null and _roshan.is_visible_in_tree(),
		"roshan_position": _cleaner.position if _cleaner != null else Vector2.ZERO,
		"net_position": _skimmer_position,
		"target_index": _target_index,
		"scoop_time": _scoop_time,
		"contact_radius": CONTACT_RADIUS,
		"hand_grip_error": _hand_grip_error(),
		"live_input_required": true,
		"one_finger": true,
		"no_fail_state": true,
		"canvas_only": true,
		"borderless_room_grown": true,
		"demo_pointer_visible": _demo_pointer != null
			and is_instance_valid(_demo_pointer) and _demo_pointer.visible,
		"demo_pointer_authored": _demo_pointer != null
			and is_instance_valid(_demo_pointer) and _demo_pointer.texture != null
			and _demo_pointer.texture.resource_path == GUIDE_HAND_PATH,
		"code_drawn_effects": false,
	}


## The approved Roshan cutout that holds the skimmer.
func identity_sprite() -> Sprite2D:
	return _roshan


## Hide this activity's own basket when the room already shows the one cleanup
## basket at BASKET_POSITION, so the same picture is never drawn twice (OD1).
func set_basket_visible(shown: bool) -> void:
	if _basket != null and is_instance_valid(_basket):
		_basket.visible = shown


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
	_advance_cleaning(maxf(delta, 0.0))
	if _demo_pointer == null or not is_instance_valid(_demo_pointer):
		queue_redraw()
		return
	if not _running or _completed or _dragging or _target_index >= 0:
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
		var route_position: Vector2 = _trash_contact_position(route_index)
		# The approved guide hand taps down onto the live piece from above; it
		# never catches anything without live input.
		var fingertip: Vector2 = route_position + Vector2(0.0,
			-30.0 - absf(sin(_demo_time * 3.2)) * 12.0)
		_demo_pointer.position = fingertip - GUIDE_FINGERTIP * _demo_pointer.scale
		_demo_pointer.rotation = sin(_demo_time * 2.0) * 0.04
		_demo_pointer.modulate.a = 0.86 + route_phase * 0.12
	for index: int in range(_trash_sprites.size()):
		var piece: Sprite2D = _trash_sprites[index]
		if piece == null or not is_instance_valid(piece) \
				or bool(piece.get_meta("in_flight", false)):
			continue
		var phase: float = _demo_time * (0.75 + float(index) * 0.07) \
			+ float(index) * 1.31
		piece.position = _trash_base_positions[index] + Vector2(
			sin(phase) * (3.0 + float(index % 2)), cos(phase * 0.83) * 2.4)
		piece.rotation = TRASH_ROTATIONS[index] + sin(phase * 0.62) * 0.025
	# The authored V4 pool is the one visible water surface: no code-drawn
	# contact arcs. The generous catch radius stays entirely invisible.


func _gui_input(event: InputEvent) -> void:
	if not _running or _completed:
		return
	if event is InputEventScreenTouch:
		var touch: InputEventScreenTouch = event as InputEventScreenTouch
		if touch.pressed:
			if _owned_touch >= 0:
				return
			_owned_touch = touch.index
			_begin_live_drag(touch.position)
		elif touch.index == _owned_touch:
			if touch.canceled:
				cancel_touch()
			else:
				_dragging = false
				_owned_touch = -1
		accept_event()
		return
	if event is InputEventScreenDrag:
		var drag: InputEventScreenDrag = event as InputEventScreenDrag
		if _dragging and drag.index == _owned_touch:
			_update_live_drag(drag.position)
		accept_event()
		return
	if event is InputEventMouseButton:
		if _owned_touch >= 0:
			return
		var mouse_button: InputEventMouseButton = event as InputEventMouseButton
		if mouse_button.button_index != MOUSE_BUTTON_LEFT:
			return
		if mouse_button.pressed:
			_begin_live_drag(mouse_button.position)
		else:
			_dragging = false
		accept_event()
		return
	if event is InputEventMouseMotion:
		var mouse_motion: InputEventMouseMotion = event as InputEventMouseMotion
		if _dragging and _owned_touch < 0:
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
	var nearest: int = -1
	var distance: float = CATCH_RADIUS
	for index: int in range(TRASH_COUNT):
		if (_progress_mask & (1 << index)) != 0:
			continue
		var candidate: float = position.distance_to(_trash_contact_position(index))
		if candidate <= distance:
			distance = candidate
			nearest = index
	if nearest != _target_index:
		_scoop_time = 0.0
		_cleaner.rotation = 0.0
	_target_index = nearest


func _advance_cleaning(delta: float) -> void:
	if not _running or _completed or _target_index < 0 or _cleaner == null:
		return
	# A slow frame or resume must not collapse travel and acting into one jump.
	delta = clampf(delta, 0.0, 1.0 / 15.0)
	var contact: Vector2 = _trash_contact_position(_target_index)
	var net_offset: Vector2 = _hand_offset + (NET_PIXEL - HANDLE_PIXEL) * _skimmer.scale
	var destination: Vector2 = contact - net_offset
	_cleaner.position = _cleaner.position.move_toward(destination, SWIM_SPEED * delta)
	if _cleaner.position.distance_to(destination) > 1.0:
		_scoop_time = 0.0
		_cleaner.rotation = 0.0
	else:
		_scoop_time += delta
		# The complete approved cutout leans with its held tool, keeping the
		# measured hand/handle joint fixed through the visible scoop.
		_cleaner.rotation = sin(minf(_scoop_time / SCOOP_SECONDS, 1.0) * TAU) * 0.055
	_sync_net_position()
	if _scoop_time >= SCOOP_SECONDS and _skimmer_position.distance_to(contact) <= CONTACT_RADIUS:
		var collected: int = _target_index
		_target_index = -1
		_scoop_time = 0.0
		_cleaner.rotation = 0.0
		_sync_net_position()
		_collect_item(collected)


func _sync_net_position() -> void:
	_skimmer_position = get_global_transform().affine_inverse() * _skimmer.to_global(
		NET_PIXEL - _skimmer.texture.get_size() * 0.5)


func _hand_grip_error() -> float:
	if _skimmer == null or _cleaner == null:
		return INF
	return _cleaner.to_global(_hand_offset).distance_to(_skimmer.to_global(
		HANDLE_PIXEL - _skimmer.texture.get_size() * 0.5))


func bind_room_actor(actor: Sprite2D, shadow: Sprite2D, skin: String = "classic") -> void:
	_room_roshan = actor
	_room_shadow = shadow
	# Preserve the wardrobe selection using its existing complete cutout.
	# These normalized hand sockets are measured on the two current skins.
	if is_instance_valid(actor) and actor.texture != null and skin in ["fairy", "huluu"]:
		_roshan.texture = actor.texture
		_fit_sprite(_roshan, Vector2(243.2, 243.2))
		var hand_uv: Vector2 = Vector2(0.705, 0.552) if skin == "fairy" else Vector2(0.811, 0.353)
		_hand_offset = (hand_uv - Vector2(0.5, 0.5)) * actor.texture.get_size() * _roshan.scale
		_skimmer.position = _hand_offset - (HANDLE_PIXEL - _skimmer.texture.get_size() * 0.5) * _skimmer.scale


func _claim_room_actor() -> void:
	if _owns_actor or _cleaner == null:
		return
	_owns_actor = true
	_cleaner.visible = true
	if is_instance_valid(_room_roshan):
		_room_visibility = _room_roshan.visible
		_cleaner.position = get_global_transform().affine_inverse() * _room_roshan.global_position
		_room_roshan.visible = false
	if is_instance_valid(_room_shadow):
		_shadow_visibility = _room_shadow.visible
		_room_shadow.visible = false
	_sync_net_position()


func _release_room_actor() -> void:
	if not _owns_actor:
		return
	_owns_actor = false
	if is_instance_valid(_room_roshan):
		_room_roshan.global_position = _cleaner.global_position
		var foot: Vector2 = _cleaner.position + Vector2(0.0, 110.0)
		_room_roshan.set_meta("stage_foot", foot)
		_room_roshan.set_meta("current_stage_foot", foot)
		_room_roshan.visible = _room_visibility
	if is_instance_valid(_room_shadow):
		_room_shadow.global_position = _cleaner.to_global(Vector2(0.0, 100.0))
		_room_shadow.visible = _shadow_visibility
	if _cleaner != null:
		_cleaner.visible = false


func _exit_tree() -> void:
	_release_room_actor()


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
			piece.set_meta("in_flight", true)
			piece.z_index = 176
			var flight: Tween = piece.create_tween().set_parallel(true)
			_flight_tweens.append(flight)
			flight.tween_property(piece, "position", BASKET_POSITION, 0.48) \
				.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
			flight.tween_property(piece, "scale", piece.scale * 0.42, 0.48)
			flight.tween_property(piece, "modulate:a", 0.0, 0.12).set_delay(0.39)
			flight.chain().tween_callback(_finish_piece_flight.bind(index, flight))
	if _progress_mask == ALL_MASK:
		_completed = true
		_dragging = false
		if _demo_pointer != null and is_instance_valid(_demo_pointer):
			_demo_pointer.visible = false
		_emit_completed_once()
	queue_redraw()


func _emit_completed_once() -> void:
	if _completed_emitted:
		return
	_completed_emitted = true
	completed.emit()


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
	_basket.z_index = 175
	_basket.modulate = Color(0.84, 0.88, 0.82, 0.96)
	_fit_sprite(_basket, BASKET_MAX_SIZE)
	add_child(_basket)

	for index: int in range(TRASH_COUNT):
		var piece := Sprite2D.new()
		piece.name = "FloatingTrash_%02d" % index
		piece.texture = _atlas_frame(index)
		piece.position = TRASH_POSITIONS[index]
		piece.z_index = 2 + int(round((piece.position.y - 260.0) / 22.0))
		piece.modulate = TRASH_TINTS[index]
		piece.rotation = TRASH_ROTATIONS[index]
		piece.set_meta("trash_index", index)
		piece.set_meta("in_flight", false)
		_fit_sprite(piece, TRASH_MAX_SIZES[index])
		add_child(piece)
		_trash_sprites.append(piece)
		_trash_base_positions.append(piece.position)

	_skimmer = Sprite2D.new()
	_skimmer.name = "PoolSkimmer"
	_skimmer.texture = load(SKIMMER_PATH) as Texture2D
	_skimmer.z_index = 35
	_fit_sprite(_skimmer, SKIMMER_MAX_SIZE)
	_cleaner = Node2D.new()
	_cleaner.name = "RoshanHoldingSkimmer"
	_cleaner.position = Vector2(640.0, 490.0)
	_cleaner.z_index = 34
	_cleaner.visible = false
	add_child(_cleaner)
	_roshan = Sprite2D.new()
	_roshan.name = "RoshanApprovedCutout"
	var pose := AtlasTexture.new()
	pose.atlas = ROSHAN_ATLAS
	pose.region = Rect2(256.0, 0.0, 256.0, 256.0)
	_roshan.texture = pose
	_roshan.scale = Vector2.ONE * 0.95
	_cleaner.add_child(_roshan)
	_skimmer.position = HAND_OFFSET - (HANDLE_PIXEL - _skimmer.texture.get_size() * 0.5) * _skimmer.scale
	_cleaner.add_child(_skimmer)
	_sync_net_position()

	_demo_pointer = Sprite2D.new()
	_demo_pointer.name = "SkimmerDemoPointer"
	var guide_texture := load(GUIDE_HAND_PATH) as Texture2D
	_demo_pointer.texture = guide_texture
	if guide_texture != null:
		_demo_pointer.scale = Vector2.ONE * GUIDE_HAND_SIZE / maxf(guide_texture.get_width(), 1.0)
	_demo_pointer.z_index = 180 # Above the floating pieces and basket it points at.
	_demo_pointer.visible = false
	add_child(_demo_pointer)
	_bubbles_texture = load(BUBBLES_PATH) as Texture2D
	_clear_ring_texture = load(CLEAR_RING_PATH) as Texture2D

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
	var origin: Vector2 = Vector2(float(index % 3) * TRASH_CELL_SIZE.x,
		float(index / 3) * TRASH_CELL_SIZE.y)
	# The approved wrapper extends through x345 across the nominal x341 grid.
	# Shift these equal-size source windows to retain its tip and keep it out
	# of the can. Measured alpha bounds leave transparent edges in both windows.
	if index == 0:
		origin.x = 12.0
	elif index == 1:
		origin.x = 352.0
	frame.region = Rect2(origin, TRASH_CELL_SIZE)
	frame.filter_clip = true
	return frame


func _trash_contact_position(index: int) -> Vector2:
	if index >= 0 and index < _trash_sprites.size():
		var piece: Sprite2D = _trash_sprites[index]
		if piece != null and is_instance_valid(piece):
			return piece.position
	return TRASH_POSITIONS[index]


func _fit_sprite(sprite: Sprite2D, max_size: Vector2) -> void:
	if sprite.texture == null:
		return
	var source_size: Vector2 = sprite.texture.get_size()
	var fit_scale: float = minf(
		max_size.x / maxf(source_size.x, 1.0),
		max_size.y / maxf(source_size.y, 1.0))
	sprite.scale = Vector2.ONE * fit_scale


func _spawn_catch_feedback(center: Vector2) -> void:
	# Approved clean ring plus a few soap bubbles: the same authored feedback the
	# bathroom uses, with no font-dependent glyphs.
	if _feedback_layer == null or not is_instance_valid(_feedback_layer):
		return
	if _clear_ring_texture != null:
		var ring := Sprite2D.new()
		ring.name = "CatchCleanRing"
		ring.texture = _clear_ring_texture
		ring.position = center
		var base := Vector2.ONE * 104.0 / maxf(_clear_ring_texture.get_width(), 1.0)
		ring.scale = base * 0.45
		_feedback_layer.add_child(ring)
		var ring_tween: Tween = ring.create_tween().set_parallel(true)
		ring_tween.tween_property(ring, "scale", base, 0.40).set_trans(Tween.TRANS_BACK) \
			.set_ease(Tween.EASE_OUT)
		ring_tween.tween_property(ring, "modulate:a", 0.0, 0.26).set_delay(0.28)
		ring_tween.chain().tween_callback(ring.queue_free)
	if _bubbles_texture == null:
		return
	for index: int in range(3):
		var bubble := Sprite2D.new()
		bubble.name = "CatchBubbles"
		bubble.texture = _bubbles_texture
		bubble.scale = Vector2.ONE * (22.0 + index * 6.0) / maxf(_bubbles_texture.get_width(), 1.0)
		var angle: float = TAU * float(index) / 3.0 - 1.2
		var start: Vector2 = center + Vector2(cos(angle), sin(angle)) * 14.0
		var finish: Vector2 = center + Vector2(cos(angle), sin(angle)) * (54.0 + index * 6.0) \
			+ Vector2(0.0, -18.0)
		bubble.position = start
		_feedback_layer.add_child(bubble)
		var bubble_tween: Tween = bubble.create_tween().set_parallel(true)
		bubble_tween.tween_property(bubble, "position", finish, 0.46)
		bubble_tween.tween_property(bubble, "modulate:a", 0.0, 0.46).set_ease(Tween.EASE_IN)
		bubble_tween.chain().tween_callback(bubble.queue_free)


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
	_cleaner = null
	_roshan = null
	_target_index = -1
	_scoop_time = 0.0
	_hand_offset = HAND_OFFSET
