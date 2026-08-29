class_name DayOneMainHallCleanup
extends Control
## Stage 1 Main Hall interaction layer. Progress remains on ReefMain.

const Affordance := preload("res://scripts/interaction_affordance.gd")

const TARGETS: Array[Dictionary] = [
	{"id": "light_left", "pos": Vector2(430.0, 220.0), "size": Vector2(180.0, 160.0), "kind": "light"},
	{"id": "light_right", "pos": Vector2(1260.0, 220.0), "size": Vector2(180.0, 160.0), "kind": "light"},
	{"id": "light_b_left", "pos": Vector2(1892.0, 220.0), "size": Vector2(180.0, 160.0), "kind": "light"},
	{"id": "light_b_right", "pos": Vector2(2752.0, 220.0), "size": Vector2(180.0, 160.0), "kind": "light"},
	{"id": "wall_a", "pos": Vector2(1450.0, 390.0), "size": Vector2(190.0, 170.0), "kind": "scrub"},
	{"id": "runner_a", "pos": Vector2(1370.0, 685.0), "size": Vector2(220.0, 170.0), "kind": "scrub"},
	{"id": "floor_a", "pos": Vector2(650.0, 815.0), "size": Vector2(230.0, 170.0), "kind": "scrub"},
	{"id": "wall_b", "pos": Vector2(1822.0, 390.0), "size": Vector2(190.0, 170.0), "kind": "scrub"},
	{"id": "floor_b", "pos": Vector2(2792.0, 810.0), "size": Vector2(230.0, 170.0), "kind": "scrub"},
	{"id": "sleepy_bunny", "pos": Vector2(900.0, 830.0), "size": Vector2(150.0, 115.0), "kind": "bunny"},
	{"id": "shell_bunny", "pos": Vector2(1250.0, 830.0), "size": Vector2(150.0, 115.0), "kind": "bunny"},
	{"id": "runner_bunny", "pos": Vector2(2050.0, 830.0), "size": Vector2(165.0, 120.0), "kind": "bunny"},
]
const GESTURE_SHEET := "res://assets/characters/roshan_25d/roshan_gesture_b.png"

var main: ReefMain
var hall: CastleRooms25D
var _buttons: Dictionary = {}
var _active := false
var _shock_blocked := false
var _shock_sprite: Sprite2D = null
var _affordance_halo: Sprite2D = null
var _affordance_time := 0.0

func setup(owner: ReefMain, room_hall: CastleRooms25D) -> void:
	main = owner
	hall = room_hall
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 27
	for target: Dictionary in TARGETS:
		if String(target["kind"]) == "bunny":
			continue
		var id: String = String(target["id"])
		var button := Button.new()
		button.name = "CleanTarget_%s" % id
		button.flat = true
		button.focus_mode = Control.FOCUS_NONE
		button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		button.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
		button.set_meta("day_one_hall_target_id", id)
		button.set_meta("day_one_hall_target_kind", String(target["kind"]))
		button.set_meta("day_one_hall_art_center", target["pos"] as Vector2)
		button.set_meta("day_one_hall_art_size", target["size"] as Vector2)
		button.pressed.connect(_clean_target.bind(id))
		add_child(button)
		_buttons[id] = button
	_affordance_halo = Affordance.make_radial_halo_2d(
		Affordance.INTERACTION, Vector2(112.0, 112.0))
	_affordance_halo.name = "DayOneHallCleanupAffordance"
	_affordance_halo.visible = false
	add_child(_affordance_halo)
	_active = true
	set_process(true)
	_place_buttons()

func set_hall_active(active: bool) -> void:
	_active = active
	_place_buttons()

func _process(delta: float) -> void:
	if _active and hall != null:
		_place_buttons()
		_update_affordance(delta)
	elif _affordance_halo != null:
		_affordance_halo.visible = false

func _place_buttons() -> void:
	if hall == null or main == null:
		return
	var available: bool = _active and not _shock_blocked \
		and main.day_one_is_active() \
		and not main._day_one_ref().hall_cleanup_complete()
	var xform := Transform2D.IDENTITY
	if main.castle_room_world_root != null:
		xform = main.castle_room_world_root.get_global_transform_with_canvas()
	for target: Dictionary in TARGETS:
		var id: String = String(target["id"])
		var button: Button = _buttons.get(id) as Button
		if button == null:
			continue
		var canvas_center: Vector2 = xform * hall._hall_art_to_world(
			target["pos"] as Vector2, 4.0)
		var stage_center: Vector2 = hall._canvas_to_stage(canvas_center)
		var stage_size: Vector2 = (target["size"] as Vector2) \
			* hall.HALL_STAGE_SCALE
		button.size = Vector2(maxf(145.0, stage_size.x),
			maxf(145.0, stage_size.y))
		button.position = stage_center - button.size * 0.5
		button.visible = available \
			and not main._day_one_ref().hall_target_clean(id)

func _update_affordance(delta: float) -> void:
	if _affordance_halo == null or _shock_blocked \
			or main._day_one_ref().hall_cleanup_complete():
		if _affordance_halo != null:
			_affordance_halo.visible = false
		return
	var candidates: Array[Dictionary] = []
	var canvas_rect := Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
	for target: Dictionary in TARGETS:
		if String(target["kind"]) == "bunny":
			continue
		var button: Button = _buttons.get(String(target["id"])) as Button
		if button != null and button.visible \
				and Rect2(button.position, button.size).intersects(canvas_rect):
			candidates.append({
				"id": String(target["id"]),
				"center": button.position + button.size * 0.5,
				"size": button.size,
				"kind": Affordance.INTERACTION,
			})
	for bunny_id: String in DayOneDirector.HALL_BUNNY_TARGET_IDS:
		var record: Dictionary = main.castle_room_item_sprites.get(
			bunny_id, {}) as Dictionary
		var bunny: Sprite2D = record.get("sprite") as Sprite2D
		if bunny == null or not is_instance_valid(bunny) or not bunny.visible:
			continue
		var center: Vector2 = hall._canvas_to_stage(
			bunny.get_global_transform_with_canvas().origin)
		var bunny_size := Vector2(124.0, 112.0)
		if Rect2(center - bunny_size * 0.5, bunny_size).intersects(canvas_rect):
			candidates.append({
				"id": bunny_id,
				"center": center,
				"size": bunny_size,
				"kind": Affordance.ANIMATION,
			})
	if candidates.is_empty():
		_affordance_halo.visible = false
		return
	_affordance_time += maxf(0.0, delta)
	var index: int = int(floor(_affordance_time / 2.4)) % candidates.size()
	var candidate: Dictionary = candidates[index]
	var halo_size: Vector2 = candidate["size"] as Vector2 * 1.08
	var affordance_kind: String = String(candidate["kind"])
	Affordance.configure_radial_halo_2d(
		_affordance_halo, affordance_kind, halo_size)
	var wave: float = sin(_affordance_time * Affordance.pulse_speed(
		affordance_kind, false))
	var base_scale: Vector2 = _affordance_halo.get_meta(
		"affordance_base_scale", Vector2.ONE) as Vector2
	_affordance_halo.scale = base_scale * (1.0 + wave * 0.035)
	_affordance_halo.position = candidate["center"] as Vector2
	_affordance_halo.modulate = Affordance.color(affordance_kind, false)
	_affordance_halo.set_meta("affordance_target", String(candidate["id"]))
	_affordance_halo.visible = true

func _clean_target(target_id: String) -> void:
	if not _active or _shock_blocked or main.day_one_hall_cleanup_modal \
			or main.castle_room_menu_open:
		return
	if not main._day_one_ref().clean_hall_target(target_id):
		return
	main._ui_tap()
	_spawn_target_feedback(target_id)
	main._write_save()
	if main._day_one_ref().hall_cleanup_complete():
		main.day_one_complete_main_hall()
	else:
		hall.sync_day_one_dirty_tiles()
	_place_buttons()

func begin_shock_beat() -> bool:
	if _shock_blocked or main == null:
		return false
	_shock_blocked = true
	main.day_one_hall_cleanup_modal = true
	main._set_world_controls_enabled(false, "day_one_hall_shock")
	main._say("roshan", "talk", 0.0)
	if hall != null and ResourceLoader.exists("res://assets/audio/hop_boing.ogg"):
		hall._play_item_sfx("hop_boing.ogg", 0.68)
	main.show_msg("Roshan",
		"Oh! Tap the dusty spots, sleepy lights, and dust bunnies!", "hint")
	_show_gesture_frames()
	_place_buttons()
	var pointer := Label.new()
	pointer.name = "DayOneHallCleanPointer"
	pointer.text = "☝"
	StorybookUI.style_label(pointer, 52, StorybookUI.GOLD, 4)
	pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(pointer)
	_place_pointer(pointer)
	var tween := pointer.create_tween().set_loops()
	tween.tween_property(pointer, "position:y", pointer.position.y + 12.0, 0.45)
	tween.tween_property(pointer, "position:y", pointer.position.y, 0.45)
	get_tree().create_timer(2.2).timeout.connect(func() -> void:
		if is_instance_valid(pointer):
			pointer.queue_free()
		_finish_shock_beat()
	)
	return true

func _place_pointer(pointer: Label) -> void:
	for target: Dictionary in TARGETS:
		var button: Button = _buttons.get(String(target["id"])) as Button
		if button != null \
				and not main._day_one_ref().hall_target_clean(String(target["id"])):
			pointer.position = button.position + Vector2(
				button.size.x * 0.5 - 18.0, -34.0)
			return
	pointer.position = Vector2(568.0, 470.0)

func _show_gesture_frames() -> void:
	var actor: Sprite2D = main.castle_room_player_sprite
	if actor == null or not is_instance_valid(actor):
		return
	var gesture_texture: Texture2D = load(GESTURE_SHEET) as Texture2D
	if gesture_texture == null or main.castle_room_world_root == null:
		return
	_shock_sprite = Sprite2D.new()
	_shock_sprite.name = "DayOneHallRoshanShockGesture"
	_shock_sprite.texture = gesture_texture
	_shock_sprite.position = actor.position
	_shock_sprite.scale = actor.scale
	_shock_sprite.flip_h = actor.flip_h
	_shock_sprite.z_index = actor.z_index + 1
	_shock_sprite.set_meta("gesture_sheet", "gesture_b")
	_shock_sprite.set_meta("gesture_frames", [4, 5, 6, 7])
	main.castle_room_world_root.add_child(_shock_sprite)
	actor.visible = false
	_set_gesture_frame(4)
	var tween := create_tween()
	for frame: int in [5, 6, 7]:
		tween.tween_interval(0.18)
		tween.tween_callback(_set_gesture_frame.bind(frame))

func _set_gesture_frame(frame: int) -> void:
	if _shock_sprite == null or not is_instance_valid(_shock_sprite):
		return
	RoshanSpriteFrames.apply_region_2d(_shock_sprite, "gesture_b", frame, 4)

func _finish_shock_beat() -> void:
	if _shock_sprite != null and is_instance_valid(_shock_sprite):
		_shock_sprite.queue_free()
	_shock_sprite = null
	if main.castle_room_player_sprite != null \
			and is_instance_valid(main.castle_room_player_sprite):
		main.castle_room_player_sprite.visible = true
	_shock_blocked = false
	if main != null:
		main.day_one_hall_cleanup_modal = false
		main._set_world_controls_enabled(true, "day_one_hall_shock")
	_place_buttons()

func _spawn_target_feedback(target_id: String) -> void:
	var target: Dictionary = {}
	for candidate: Dictionary in TARGETS:
		if String(candidate["id"]) == target_id:
			target = candidate
			break
	var kind: String = String(target.get("kind", "scrub"))
	var effect := Label.new()
	effect.text = "✦  ✦" if kind == "light" else "◜  ✧"
	StorybookUI.style_label(effect, 32, StorybookUI.GOLD, 4)
	effect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(effect)
	var button: Button = _buttons.get(target_id) as Button
	if button != null:
		effect.position = button.position + button.size * 0.5 \
			- Vector2(20.0, 18.0)
	else:
		effect.position = Vector2(560.0, 330.0)
	var tw := effect.create_tween().set_parallel(true)
	tw.tween_property(effect, "position:y", effect.position.y - 22.0, 0.48)
	if kind == "light":
		effect.scale = Vector2(0.72, 0.72)
		tw.tween_property(effect, "scale", Vector2(1.28, 1.28), 0.48) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	else:
		tw.tween_property(effect, "position:x", effect.position.x + 34.0, 0.48) \
			.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(effect, "modulate:a", 0.0, 0.48)
	tw.finished.connect(effect.queue_free)

func play_completion_celebration() -> void:
	if main == null or hall == null:
		return
	# A sparse Canvas2D sweep spans the complete 3344px hall, including the
	# off-camera half. The renderer naturally culls those short-lived cards.
	for index: int in range(9):
		var art_position := Vector2(
			180.0 + float(index) * (2984.0 / 8.0),
			650.0 - float(index % 3) * 105.0)
		hall._item_burst(hall._hall_art_to_world(art_position, 4.0),
			Color(StorybookUI.GOLD), 3, "day_one_hall_cleanup")
	_point_to_bubble_bath()

func _point_to_bubble_bath() -> void:
	var door: Button = main.castle_room_buttons.get("bubble_bath") as Button
	if door == null:
		return
	var target_center: Vector2
	if door.visible:
		target_center = door.position + door.size * 0.5
	else:
		for portal: Dictionary in CastleRooms25D.HALL_PORTALS:
			if String(portal.get("id", "")) != "bubble_bath":
				continue
			var art_rect: Rect2 = portal["rect"] as Rect2
			var xform: Transform2D = main.castle_room_world_root \
				.get_global_transform_with_canvas()
			target_center = hall._canvas_to_stage(xform * hall._hall_art_to_world(
				art_rect.get_center(), 4.0))
			break
	var pointer := Label.new()
	pointer.name = "DayOneBubbleBathPointer"
	pointer.text = "←" if target_center.x < 40.0 else (
		"→" if target_center.x > StorybookUI.CANVAS_SIZE.x - 40.0 else "☝")
	StorybookUI.style_label(pointer, 52, StorybookUI.GOLD, 4)
	pointer.position = Vector2(
		clampf(target_center.x - 18.0, 28.0,
			StorybookUI.CANVAS_SIZE.x - 76.0),
		clampf(target_center.y - 90.0, 64.0,
			StorybookUI.CANVAS_SIZE.y - 96.0))
	pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(pointer)
	var tween := pointer.create_tween().set_loops(3)
	tween.tween_property(pointer, "position:y", pointer.position.y + 12.0, 0.35)
	tween.tween_property(pointer, "position:y", pointer.position.y, 0.35)
	tween.finished.connect(pointer.queue_free)

func teardown() -> void:
	set_process(false)
	_finish_shock_beat()
	if main != null:
		main.day_one_hall_cleanup_modal = false
	if is_inside_tree():
		queue_free()
	else:
		free()
