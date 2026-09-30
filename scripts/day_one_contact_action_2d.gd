class_name DayOneContactAction2D
extends Node2D
## Temporary Canvas ownership for one requested job. Durable progress stays on
## ReefMain; a gesture earns its callback only after travel, hand contact and work.
const ATLAS := preload("res://assets/characters/roshan_25d/roshan_directional.png")
const SHADOW := preload("res://assets/flats/castle/rooms/room_actor_shadow.png")
var room_actor: Sprite2D
var room_shadow: Sprite2D
var avatar: Sprite2D
var shadow: Sprite2D
var hand_offset := Vector2(46.0, 23.0) * 0.95
var target := Vector2.ZERO
var active: bool = false
var work_time: float = 0.0
var done: Callable
var actor_visible: bool = true
var shadow_visible: bool = true
var unit_scale: float = 1.0

func bind(actor: Sprite2D, actor_shadow: Sprite2D, skin: String) -> void:
	room_actor = actor
	room_shadow = actor_shadow
	unit_scale = 1.0 / maxf(get_global_transform().get_scale().x, 0.01)
	hand_offset *= unit_scale
	avatar = Sprite2D.new()
	var pose := AtlasTexture.new()
	pose.atlas = ATLAS
	pose.region = Rect2(256.0, 0.0, 256.0, 256.0)
	avatar.texture = pose
	avatar.scale = Vector2.ONE * 0.95 * unit_scale
	if is_instance_valid(actor) and actor.texture != null and skin in ["fairy", "huluu"]:
		avatar.texture = actor.texture
		avatar.scale = Vector2.ONE * 243.2 * unit_scale / maxf(actor.texture.get_height(), 1.0)
		var hand_uv := Vector2(0.705, 0.552) if skin == "fairy" else Vector2(0.811, 0.353)
		hand_offset = (hand_uv - Vector2(0.5, 0.5)) * actor.texture.get_size() * avatar.scale
	shadow = Sprite2D.new()
	shadow.texture = SHADOW
	shadow.position = Vector2(0.0, 110.0) * unit_scale
	shadow.scale = Vector2(90.0, 22.0) * unit_scale / SHADOW.get_size()
	add_child(shadow)
	add_child(avatar)
	z_index = 500
	visible = false

func available() -> bool:
	return is_instance_valid(room_actor) and avatar != null

func request(point: Vector2, callback: Callable = Callable()) -> bool:
	if active or not available():
		return false
	actor_visible = room_actor.visible
	shadow_visible = room_shadow.visible if is_instance_valid(room_shadow) else false
	position = get_parent().get_global_transform().affine_inverse() * room_actor.global_position
	room_actor.visible = false
	if is_instance_valid(room_shadow):
		room_shadow.visible = false
	visible = true
	active = true
	target = point
	work_time = 0.0
	done = callback
	return true

func follow(point: Vector2) -> void:
	if active:
		target = point
		work_time = 0.0

func arm(callback: Callable) -> void:
	if active:
		done = callback

func hand_point() -> Vector2:
	return position + hand_offset

func in_contact() -> bool:
	return active and hand_point().distance_to(target) <= 2.0 * unit_scale

func _process(delta: float) -> void:
	if not active:
		return
	position = position.move_toward(target - hand_offset, maxf(delta, 0.0) * 440.0 * unit_scale)
	if not in_contact():
		queue_redraw()
		return
	queue_redraw()
	work_time += maxf(delta, 0.0)
	if work_time >= 0.42 and done.is_valid():
		var callback: Callable = done
		cancel()
		callback.call()

func cancel() -> void:
	if not active:
		return
	active = false
	done = Callable()
	if is_instance_valid(room_actor):
		room_actor.global_position = global_position
		var foot: Vector2 = (room_actor.get_parent() as CanvasItem).get_global_transform().affine_inverse() * to_global(Vector2(0.0, 110.0) * unit_scale)
		room_actor.set_meta("stage_foot", foot)
		room_actor.set_meta("current_stage_foot", foot)
		room_actor.visible = actor_visible
	if is_instance_valid(room_shadow):
		room_shadow.global_position = to_global(Vector2(0.0, 110.0) * unit_scale)
		room_shadow.visible = shadow_visible
	visible = false

func _exit_tree() -> void:
	cancel()


func _notification(what: int) -> void:
	if what in [NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_APPLICATION_PAUSED]:
		cancel()


func _draw() -> void:
	if in_contact():
		# Sparse bubbles mark local hand work; they never advance the job.
		for index: int in range(3):
			var angle: float = work_time * 4.0 + float(index) * TAU / 3.0
			draw_circle(hand_offset + Vector2.from_angle(angle) * 11.0 * unit_scale,
				3.0 * unit_scale, Color(0.6, 0.95, 1.0, 0.75))
