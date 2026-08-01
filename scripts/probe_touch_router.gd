extends SceneTree
# Deterministic point-to-interact ownership contract. Runtime touch navigation
# has no movement stick; world points, contextual activity actions and Pause
# each retain one clear ownership path.

var main: Node3D
var touch: CanvasLayer
var taps: Array[Vector2] = []
var fingers: Dictionary = {}
var failures := 0

func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(5)
	touch = main.touch_ui
	if touch == null or not touch.wants_touch():
		_bad("touch UI unavailable; run with -- --touch")
		_finish()
		return
	main._set_touch_mode("hybrid", false)
	touch.world_touched.connect(_record_tap)

	if not touch.movement_zone().has_area():
		print("TOUCH_ROUTER|OK point mode exposes no movement ownership zone")
	else:
		_bad("point mode still exposes a movement zone")
	if touch._stick_hint != null or touch._base.visible or touch._knob.visible:
		_bad("movement-stick chrome remains visible")
	if touch._act_button != null and touch._act_button.visible:
		_bad("context action is visible before an activity needs it")

	var viewport_size: Vector2 = get_root().get_viewport().get_visible_rect().size
	var world_pos := Vector2(viewport_size.x * 0.58, viewport_size.y * 0.30)
	var former_stick_pos := Vector2(viewport_size.x * 0.12, viewport_size.y * 0.78)
	_touch_tap(0, former_stick_pos)
	await process_frame
	if taps.size() != 1 or taps[0].distance_to(former_stick_pos) > 0.1:
		_bad("former joystick area did not route as a world point")
	if not touch.stick_vec.is_zero_approx():
		_bad("world point produced a movement-stick vector")

	var tap_count_before_drag: int = taps.size()
	_down(1, world_pos - Vector2(50.0, 0.0))
	_drag(1, world_pos + Vector2(50.0, 0.0))
	_up(1, fingers[1])
	await process_frame
	if taps.size() != tap_count_before_drag:
		_bad("world drag leaked a point command")
	if not touch._world_pend.is_empty():
		_bad("world drag left stale ownership")

	# Activities may request one contextual action shell; it is never a
	# navigation control and disappears again when not needed.
	touch.set_action_label("PLAY")
	touch.set_action_visible(true)
	if touch._act_button == null or not touch._act_button.visible:
		_bad("requested context action did not appear")
	else:
		var action_center: Vector2 = touch.action_zone().get_center()
		_down(2, action_center)
		await process_frame
		if not touch.action_down or not touch.action_just:
			_bad("context action press was dropped")
		_up(2, action_center)
		await process_frame
		if touch.action_down:
			_bad("context action stayed held after release")
	touch.consume_action()
	touch.set_action_visible(false)
	if touch._act_button != null and touch._act_button.visible:
		_bad("context action did not hide")

	# Overlay transitions clear every owner and cannot resurrect controls.
	touch.set_action_visible(true)
	main._open_craft_studio()
	await process_frame
	if touch.world_controls_enabled or not touch.touch_owners.is_empty():
		_bad("opening overlay retained world touch ownership")
	if touch._act_button != null and touch._act_button.visible:
		_bad("context action occludes a full-screen overlay")
	main._close_craft()
	await process_frame
	if not touch.world_controls_enabled or not touch.touch_owners.is_empty():
		_bad("closing overlay restored stale touch ownership")
	touch.set_action_visible(false)

	# Assisted navigation remains physical and uses the authored swim loop.
	var swim_start: Vector3 = main.player.position
	var swim_forward := Vector3(sin(float(main.player.yaw)), 0.0,
		cos(float(main.player.yaw)))
	main._tap_move_ref().start(swim_start + swim_forward * 16.0)
	var observed_swim_frames: Dictionary = {}
	for swim_test_frame in range(100):
		await process_frame
		var sheet: String = String(main.player.classic_sprite_sheet)
		if sheet == "swim_front" or sheet == "swim_back":
			observed_swim_frames[int(main.player.classic_sprite.frame)] = true
		if not bool(main.touch_auto_active) and swim_test_frame > 12:
			break
	var swim_distance: float = Vector2(main.player.position.x - swim_start.x,
		main.player.position.z - swim_start.z).length()
	if swim_distance < 1.5:
		_bad("point navigation did not physically move Roshan")
	if observed_swim_frames.size() < 2:
		_bad("point navigation did not display a looping swim atlas")
	main._tap_move_ref().cancel("probe complete")

	# Pause remains the sole persistent corner control.
	var pause_center: Vector2 = touch.pause_zone().get_center()
	_dispatch_mouse(pause_center, true)
	await process_frame
	if not main.get_tree().paused or main.pause_panel == null or not main.pause_panel.visible:
		_bad("Pause press did not open the pause sheet")
	_dispatch_mouse(pause_center, false)
	_dispatch_mouse(pause_center, true)
	await process_frame
	if main.get_tree().paused:
		_bad("Pause press did not resume")
	_dispatch_mouse(pause_center, false)

	# Classic remains a test-only compatibility path for controller/legacy
	# probes, but returning to point mode restores the no-stick contract.
	main._set_touch_mode("classic", false)
	if not touch.movement_zone().has_area():
		_bad("Classic compatibility zone is unavailable")
	main._set_touch_mode("hybrid", false)
	if touch.movement_zone().has_area() or touch._base.visible or touch._knob.visible:
		_bad("returning to point mode restored joystick chrome")

	touch.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	await process_frame
	if not touch.stick_vec.is_zero_approx() or touch.action_down \
			or not touch.touch_owners.is_empty():
		_bad("focus loss left owned touch state behind")
	_finish()

func _record_tap(pos: Vector2) -> void:
	taps.append(pos)

func _touch_tap(index: int, pos: Vector2) -> void:
	_down(index, pos)
	_up(index, pos)

func _down(index: int, pos: Vector2) -> void:
	fingers[index] = pos
	var event := InputEventScreenTouch.new()
	event.index = index
	event.position = pos
	event.pressed = true
	touch._unhandled_input(event)

func _drag(index: int, pos: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = index
	event.position = pos
	event.relative = pos - (fingers[index] as Vector2)
	fingers[index] = pos
	touch._unhandled_input(event)

func _up(index: int, pos: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index
	event.position = pos
	event.pressed = false
	touch._unhandled_input(event)
	fingers.erase(index)

func _dispatch_mouse(pos: Vector2, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.device = 1
	event.button_index = MOUSE_BUTTON_LEFT
	event.position = pos
	event.pressed = pressed
	touch._input(event)

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame

func _bad(message: String) -> void:
	failures += 1
	print("TOUCH_ROUTER|FAIL ", message)

func _finish() -> void:
	if failures == 0:
		print("TOUCH_ROUTER|ALL OK")
		quit()
	else:
		print("TOUCH_ROUTER|FAIL %d issue(s)" % failures)
		quit(1)
