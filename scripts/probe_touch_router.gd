extends SceneTree
# Deterministic ownership/rollback contract for the reversible touch router.
# Run with -- --touch.

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

	# One-finger movement: no action pulse and no accidental world command.
	_down(0, move_start)
	_drag(0, move_start + Vector2(74.0, -40.0))
	await process_frame
	if (touch.stick_vec as Vector2).length() < 0.45:
		_bad("hybrid stick did not engage")
	if bool(touch.action_just) or not taps.is_empty():
		_bad("movement leaked into action/world tap")

	# A simultaneous world tap keeps its own owner while movement remains live.
	_down(1, world_pos)
	_up(1, world_pos)
	await process_frame
	if taps.size() != 1 or taps[0].distance_to(world_pos) > 0.1:
		_bad("simultaneous world tap was lost or moved")
	if (touch.stick_vec as Vector2).length() < 0.45:
		_bad("world tap stole movement ownership")

	# A swipe over the world is neither a tap command nor leaked finger state.
	var tap_count_before_drag: int = taps.size()
	_down(4, world_pos + Vector2(-40.0, 0.0))
	_drag(4, world_pos + Vector2(40.0, 0.0))
	_up(4, fingers[4])
	await process_frame
	if taps.size() != tap_count_before_drag:
		_bad("world drag leaked a tap-to-move command")
	if not touch._world_pend.is_empty():
		_bad("world drag left stale pending touch state")

	_up(0, fingers[0])
	await process_frame
	if not (touch.stick_vec as Vector2).is_zero_approx():
		_bad("stick remained active after release")

	# The visible action bubble is a real press/hold target.
	touch.consume_action()
	touch._on_action_button_down()
	if not bool(touch.action_down) or not bool(touch.action_just):
		_bad("hybrid action button did not press")
	touch._on_action_button_up()
	if bool(touch.action_down):
		_bad("hybrid action button remained held")

	# Manual steering cancels assisted travel immediately.
	main._tap_move_ref().start(main.player.position + Vector3(30.0, 0.0, 0.0))
	_down(2, move_start)
	_drag(2, move_start + Vector2(80.0, 0.0))
	await process_frame
	if bool(main.touch_auto_active):
		_bad("manual movement did not cancel assisted movement")
	_up(2, fingers[2])

	# Runtime rollback: Classic produces no world taps and restores tap-action.
	main._set_touch_mode("classic", false)
	var tap_count: int = taps.size()
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
	print("TOUCH_ROUTER|ISSUE ", message)

func _finish() -> void:
	if failures == 0:
		print("TOUCH_ROUTER|ALL OK")
	else:
		print("TOUCH_ROUTER|RESULT %d issue(s)" % failures)
	quit()
