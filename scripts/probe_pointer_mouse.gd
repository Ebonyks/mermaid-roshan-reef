extends SceneTree
# Physical desktop-mouse contract. This probe intentionally runs without
# --touch: LMB must still use the same Hybrid ownership and navigation route.

var failures := 0
var pressed_count := 0
var moved_count := 0
var released_count := 0

func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await _frames(4)
	main._set_touch_mode("hybrid", false)
	var touch = main.touch_ui
	if touch == null:
		_bad("TouchUI missing")
		_finish()
		return
	if touch.wants_touch():
		_bad("probe must run without --touch")
	touch.world_pointer_pressed.connect(func(_pos: Vector2): pressed_count += 1)
	touch.world_pointer_moved.connect(func(_pos: Vector2): moved_count += 1)
	touch.world_pointer_released.connect(func(_pos: Vector2, _dragged: bool): released_count += 1)
	main.touch_interactables.clear()
	main.touch_registry_t = 999.0
	main._pointer_nav_ref().set_context("probe")
	var viewport_size: Vector2 = get_root().get_viewport().get_visible_rect().size
	var start := viewport_size * Vector2(0.52, 0.42)
	var moved := start + Vector2(90.0, 34.0)

	_mouse_button(touch, start, true)
	await process_frame
	if pressed_count != 1 or not touch.pointer_down:
		_bad("physical LMB down did not claim the world pointer")
	if not main.pointer_nav_goal_active:
		_bad("physical LMB down did not start a navigation goal")
	_mouse_motion(touch, moved)
	await process_frame
	if moved_count < 1 or touch.pointer_pos.distance_to(moved) > 0.1:
		_bad("physical mouse hold did not retarget")
	_mouse_button(touch, moved, false)
	await process_frame
	if released_count != 1 or touch.pointer_down:
		_bad("physical LMB release left pointer ownership active")
	if not main.pointer_nav_goal_active or main.pointer_nav_pointer_down:
		_bad("click goal did not persist after release")
	var nav_axis: float = main._pointer_nav_ref().axis_x(0.0, 0.0, -10.0, 10.0)
	if nav_axis <= 0.0:
		_bad("persistent click did not steer toward its screen-side goal")
	main._pointer_nav_ref().begin(start)
	main._pointer_nav_ref().finish(start)
	var manual_axis: float = main._pointer_nav_ref().axis_x(-0.7, 0.0, -10.0, 10.0)
	if not is_equal_approx(manual_axis, -0.7) or main.pointer_nav_goal_active:
		_bad("manual axis did not take priority and cancel the click goal")
	main._pointer_nav_ref().begin(start)
	main._pointer_nav_ref().finish(start)
	main._on_touch_manual_move()
	if main.pointer_nav_goal_active:
		_bad("manual movement did not cancel pointer navigation")

	var world_before_action := pressed_count
	var action_pos: Vector2 = touch.action_zone().get_center()
	if touch._act_button == null or not touch._act_button.visible:
		_bad("desktop Hybrid mode has no visible action target")
	_mouse_button(touch, action_pos, true)
	if not touch.action_down or not touch.action_just:
		_bad("desktop action target did not press")
	if pressed_count != world_before_action:
		_bad("action target leaked into world navigation")
	_mouse_button(touch, action_pos, false)
	if touch.action_down:
		_bad("desktop action target remained held")
	touch.consume_action()

	touch.set_drag_mode(true)
	var world_before_gesture := pressed_count
	_mouse_button(touch, start, true)
	_mouse_motion(touch, moved)
	if not touch.drag_active or touch.drag_pos.distance_to(moved) > 0.1:
		_bad("desktop gesture did not populate the shared drag channel")
	if pressed_count != world_before_gesture:
		_bad("gesture press leaked into world navigation")
	_mouse_button(touch, moved, false)
	if touch.drag_active:
		_bad("desktop gesture remained active after release")
	touch.set_drag_mode(false)

	var emulated := InputEventMouseButton.new()
	emulated.device = InputEvent.DEVICE_ID_EMULATION
	emulated.button_index = MOUSE_BUTTON_LEFT
	emulated.position = start
	emulated.pressed = true
	touch._unhandled_input(emulated)
	if pressed_count != world_before_gesture:
		_bad("emulated mouse duplicate was not ignored")
	_finish()

func _mouse_button(touch: CanvasLayer, pos: Vector2, down: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.position = pos
	event.pressed = down
	touch._unhandled_input(event)

func _mouse_motion(touch: CanvasLayer, pos: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = pos
	touch._unhandled_input(event)

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame

func _bad(message: String) -> void:
	failures += 1
	print("POINTER_MOUSE|FAIL ", message)

func _finish() -> void:
	if failures == 0:
		print("POINTER_MOUSE|ALL OK")
		quit()
	else:
		print("POINTER_MOUSE|FAIL %d issue(s)" % failures)
		quit(1)
