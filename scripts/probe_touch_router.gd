extends SceneTree
# Deterministic ownership/rollback contract for the reversible touch router.
# Run with -- --touch.

var main: Node3D
var touch: CanvasLayer
var taps: Array[Vector2] = []
var fingers: Dictionary = {}
var failures := 0
var pointer_pressed := 0
var pointer_moved := 0
var pointer_released := 0

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
	touch.world_pointer_pressed.connect(func(_pos: Vector2): pointer_pressed += 1)
	touch.world_pointer_moved.connect(func(_pos: Vector2): pointer_moved += 1)
	touch.world_pointer_released.connect(func(_pos: Vector2, _dragged: bool): pointer_released += 1)

	var move_zone: Rect2 = touch.movement_zone()
	var action_zone: Rect2 = touch.action_zone()
	if move_zone.intersects(action_zone):
		_bad("movement and action ownership zones overlap")
	if move_zone.size.x < 390.0 or move_zone.size.y < 300.0:
		_bad("movement thumb bay is too small: %s" % move_zone)
	var move_start: Vector2 = move_zone.get_center()
	var world_pos := Vector2(
		get_root().get_viewport().get_visible_rect().size.x * 0.58,
		get_root().get_viewport().get_visible_rect().size.y * 0.30)

	# The old lower-left thumb bay is world space in Hybrid: touch and mouse
	# both use the same point-to-move route.
	_down(0, move_start)
	await process_frame
	if not (touch.stick_vec as Vector2).is_zero_approx():
		_bad("Hybrid lower-left press still engaged the legacy stick")
	if pointer_pressed != 1 or not bool(touch.pointer_down):
		_bad("Hybrid lower-left press did not claim the world pointer")

	# The pink action target keeps exclusive ownership even if a world pointer
	# is already down.
	touch.consume_action()
	var action_center: Vector2 = touch.action_zone().get_center()
	_down(6, action_center)
	await process_frame
	if not bool(touch.action_down) or not bool(touch.action_just):
		_bad("action press was dropped while the world pointer was held")
	if pointer_pressed != 1 or not touch.touch_owners.has(0):
		_bad("action press stole or duplicated the held world pointer")
	_up(6, action_center)
	await process_frame
	if bool(touch.action_down):
		_bad("action button stayed held after second-finger release")
	touch.consume_action()
	_up(0, fingers[0])
	await process_frame
	if taps.size() != 1 or taps[0].distance_to(move_start) > 0.1:
		_bad("Hybrid point-to-move tap was lost or moved")
	if pointer_released != 1 or bool(touch.pointer_down):
		_bad("Hybrid point-to-move release left pointer ownership active")

	# Holding and sliding retargets continuously but does not add a second tap.
	var tap_count_before_drag: int = taps.size()
	_down(4, world_pos + Vector2(-40.0, 0.0))
	_drag(4, world_pos + Vector2(40.0, 0.0))
	_up(4, fingers[4])
	await process_frame
	if taps.size() != tap_count_before_drag:
		_bad("world hold-retarget leaked a second tap command")
	if pointer_moved < 1 or pointer_released != 2:
		_bad("world hold-retarget missed move/release edges")
	if not touch._world_pend.is_empty():
		_bad("world drag left stale pending touch state")

	# The visible action bubble is a real press/hold target.
	touch.consume_action()
	touch._on_action_button_down()
	if not bool(touch.action_down) or not bool(touch.action_just):
		_bad("hybrid action button did not press")
	touch._on_action_button_up()
	if bool(touch.action_down):
		_bad("hybrid action button remained held")
	await _frames(4)
	if bool(touch.action_just):
		_bad("released action edge remained armed for a future interaction")
	touch.set_action_label("PLAY")
	if touch._act_lbl == null or String(touch._act_lbl.text) == "PLAY" or not "\n" in String(touch._act_lbl.text):
		_bad("action target is word-only instead of pictogram plus word")

	# A full-screen overlay can swallow the original finger-up. Opening and
	# closing it must still clear the stick owner and restore neutral controls.
	_down(5, move_start)
	_drag(5, move_start + Vector2(76.0, -22.0))
	main._open_craft_studio()
	await process_frame
	if touch.world_controls_enabled or not touch.touch_owners.is_empty() or not (touch.stick_vec as Vector2).is_zero_approx():
		_bad("opening overlay stranded held movement state")
	if touch._act_button != null and touch._act_button.visible:
		_bad("world action button occludes a full-screen overlay")
	# The release is intentionally omitted: this simulates a Control consuming
	# it before the gameplay router sees it.
	main._close_craft()
	await process_frame
	if not touch.world_controls_enabled or not touch.touch_owners.is_empty() or not (touch.stick_vec as Vector2).is_zero_approx():
		_bad("closing overlay restored stale held movement")

	# Manual steering remains a cancellation seam for WASD and Classic.
	main._tap_move_ref().start(main.player.position + Vector3(30.0, 0.0, 0.0))
	main._on_touch_manual_move()
	if bool(main.touch_auto_active):
		_bad("manual movement did not cancel assisted movement")

	# Runtime rollback: Classic restores the drag-anywhere stick and tap-action.
	main._set_touch_mode("classic", false)
	var tap_count: int = taps.size()
	_down(2, move_start)
	_drag(2, move_start + Vector2(80.0, 0.0))
	await process_frame
	if (touch.stick_vec as Vector2).length() < 0.45:
		_bad("Classic rollback did not restore the virtual stick")
	_up(2, fingers[2])
	await process_frame
	touch.consume_action()
	_down(3, world_pos)
	_up(3, world_pos)
	await process_frame
	if taps.size() != tap_count:
		_bad("Classic leaked a Hybrid world tap")
	if not bool(touch.consume_action_just()):
		_bad("Classic tap-action rollback is missing")

	touch.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	await process_frame
	if not (touch.stick_vec as Vector2).is_zero_approx() or bool(touch.action_down) or not touch.touch_owners.is_empty():
		_bad("focus loss left owned touch state behind")
	_finish()

func _record_tap(pos: Vector2) -> void:
	taps.append(pos)

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
