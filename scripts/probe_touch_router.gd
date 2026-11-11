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
	# DIRECTION AGREEMENT (owner report 2026-08-03). The thumb bay draws no pad,
	# so the stick anchors on the finger and a drag's direction IS the commanded
	# direction — asserted at both ends of the bay and in the middle, because the
	# old fixed anchor sat at the bay's far left and made most of it push right.
	for probe_x: float in [move_zone.position.x + 40.0, move_zone.get_center().x,
			move_zone.end.x - 40.0]:
		var bay_press := Vector2(probe_x, move_zone.get_center().y)
		_down(8, bay_press)
		await process_frame
		if not (touch.stick_vec as Vector2).is_zero_approx():
			_bad("a press with no drag pushed the stick at x=%.0f: %s" \
				% [probe_x, touch.stick_vec])
		_drag(8, bay_press + Vector2(-70.0, 0.0))
		await process_frame
		if (touch.stick_vec as Vector2).x > -0.45:
			_bad("dragging LEFT at x=%.0f did not steer left: %s" \
				% [probe_x, touch.stick_vec])
		_up(8, fingers[8])
		await process_frame
	# The bay is an accessibility stick, not a hole in the world: a press there
	# that never became a drag still reaches the world as a tap.
	var bay_taps: int = taps.size()
	_down(9, move_start)
	_up(9, move_start)
	await process_frame
	if taps.size() != bay_taps + 1:
		_bad("a tap in the thumb bay was swallowed instead of reaching the world")
	# Hold-to-travel clients read the emulated pointer, which knows nothing about
	# ownership. They ask this instead, so a held button never means "walk here".
	if not touch.reserved_zone_hit(touch.action_zone().get_center()):
		_bad("holding the action medallion is not reserved from hold-to-travel")
	if not touch.reserved_zone_hit(move_start):
		_bad("holding inside the thumb bay is not reserved from hold-to-travel")
	main._tap_move_ref().cancel("probe reset")
	main._interaction_ref().clear_focus()
	taps.clear()
	var world_pos := Vector2(
		get_root().get_viewport().get_visible_rect().size.x * 0.58,
		get_root().get_viewport().get_visible_rect().size.y * 0.30)
	if touch.reserved_zone_hit(world_pos):
		_bad("open world space is wrongly reserved from hold-to-travel")

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
	# A second-finger activation that does not change scenes must not cancel
	# the left-stick owner. (World transitions intentionally clear all input.)
	main._activate_touch_interactable("court:star:0")
	if (touch.stick_vec as Vector2).length() < 0.45 or not touch.touch_owners.has(0):
		_bad("non-transition activation stole held movement")

	# Fix regression: the pink action target must hear a SECOND finger while
	# the stick is held. A Control Button only receives the first finger
	# (mouse-from-touch emulation), so the router claims raw ScreenTouch
	# presses inside the action zone itself.
	touch.consume_action()
	var action_center: Vector2 = touch.action_zone().get_center()
	_down(6, action_center)
	await process_frame
	if not bool(touch.action_down) or not bool(touch.action_just):
		_bad("second-finger action press was dropped while the stick was held")
	if (touch.stick_vec as Vector2).length() < 0.45 or not touch.touch_owners.has(0):
		_bad("second-finger action press stole the held stick")
	_up(6, action_center)
	await process_frame
	if bool(touch.action_down):
		_bad("action button stayed held after second-finger release")
	touch.consume_action()

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

	# Manual steering cancels assisted travel immediately.
	main._tap_move_ref().start(main.player.position + Vector3(30.0, 0.0, 0.0))
	_down(2, move_start)
	_drag(2, move_start + Vector2(80.0, 0.0))
	await process_frame
	if bool(main.touch_auto_active):
		_bad("manual movement did not cancel assisted movement")
	_up(2, fingers[2])

	# A selected world point must drive the authored swim loop for the whole
	# physical approach. Begin during an idle gesture to catch pose-priority
	# regressions where Roshan slides toward the tap in a held frame.
	main.player.play_verb("look")
	var swim_start: Vector3 = main.player.position
	var swim_forward := Vector3(
		sin(float(main.player.yaw)), 0.0,
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
	var swim_distance: float = Vector2(
		main.player.position.x - swim_start.x,
		main.player.position.z - swim_start.z).length()
	if swim_distance < 1.5:
		_bad("tap-to-move swim animation test did not physically move Roshan")
	if observed_swim_frames.size() < 2:
		_bad("tap-to-move did not display a looping swim atlas: %s" \
			% observed_swim_frames)
	main._tap_move_ref().cancel("probe complete")
	main.player.verb = ""

	# Priority dispatch: fixed controls are claimed in _input before ordinary
	# GUI routing. Headless display drivers do not forward synthetic mouse
	# events through a viewport, so exercise that priority handler directly.
	var pause_center: Vector2 = touch.pause_zone().get_center()
	_dispatch_mouse(pause_center, true)
	await process_frame
	if not main.get_tree().paused or main.pause_panel == null or not main.pause_panel.visible:
		_bad("screen-dispatched Pause press did not open the pause sheet")
	_dispatch_mouse(pause_center, false)
	await process_frame
	_dispatch_mouse(pause_center, true)
	await process_frame
	if main.get_tree().paused:
		_bad("screen-dispatched Pause press did not resume")
	_dispatch_mouse(pause_center, false)
	await process_frame

	await _pointer_contract_gate(move_start)

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

# POINT-AND-DRAG CONTRACT (2026-11-11). Tap and drag are ONE travel system with
# one owner: the router's world pointer. Reserved controls never become a point,
# a quick press stays a tap, a drag or a hold steers the same assisted route a
# tap would start, a steering finger never also fires a tap on lift, and a
# route pulled back from past the world's edge is shown as an edge.
func _pointer_contract_gate(move_start: Vector2) -> void:
	main._tap_move_ref().cancel("pointer reset")
	main._interaction_ref().clear_focus()
	touch.consume_action()
	var screen: Vector2 = get_root().get_viewport().get_visible_rect().size
	var open_point := Vector2(-1.0, -1.0)
	for candidate: Vector2 in [Vector2(0.62, 0.34), Vector2(0.50, 0.28),
			Vector2(0.70, 0.45), Vector2(0.40, 0.22), Vector2(0.56, 0.52)]:
		var at: Vector2 = candidate * screen
		if not touch.reserved_zone_hit(at) \
				and not main._interaction_ref().has_target_at(at) \
				and not main._interaction_ref().has_target_at(at + Vector2(150.0, 0.0)):
			open_point = at
			break
	if open_point.x < 0.0:
		_bad("pointer contract found no open water to point at")
		return

	_down(10, touch.action_zone().get_center())
	_down(11, move_start)
	await process_frame
	if not touch.world_point().is_empty():
		_bad("the action bubble or thumb bay became a world pointer")
	_up(10, touch.action_zone().get_center())
	_up(11, move_start)
	await process_frame
	touch.consume_action()
	main._tap_move_ref().cancel("pointer reset")
	main._interaction_ref().clear_focus()
	taps.clear()

	_down(12, open_point)
	var fresh: Dictionary = touch.world_point()
	if fresh.is_empty() or bool(fresh.get("held", true)):
		_bad("a fresh world press was not a pending tap: %s" % [fresh])
	_up(12, open_point)
	await process_frame
	if taps.size() != 1:
		_bad("a quick world press did not resolve as exactly one tap (%d)" % taps.size())
	main._tap_move_ref().cancel("pointer reset")
	main._interaction_ref().clear_focus()
	taps.clear()

	var drag_to: Vector2 = open_point + Vector2(150.0, 0.0)
	_down(13, open_point)
	await process_frame
	_drag(13, drag_to)
	await _frames(3)
	var point: Dictionary = touch.world_point()
	if point.is_empty() or not bool(point.get("held", false)) \
			or not bool(point.get("moved", false)) \
			or (point.get("pos", Vector2.ZERO) as Vector2).distance_to(drag_to) > 0.5:
		_bad("a world drag is not reported as a moving point: %s" % [point])
	if not bool(main.touch_follow_active):
		_bad("dragging on open water did not steer Roshan toward the finger")
	elif bool(main.touch_auto_active) and not bool(main.touch_auto_at_edge):
		var camera: Camera3D = get_root().get_viewport().get_camera_3d()
		var aimed: Vector2 = camera.unproject_position(main.touch_auto_target)
		if aimed.distance_to(drag_to) > 48.0:
			_bad("drag route aims at %s, not under the finger at %s" % [aimed, drag_to])
		if not touch.travel_goal_visible():
			_bad("a dragged route shows no destination marker")
	_up(13, drag_to)
	await process_frame
	if not taps.is_empty():
		_bad("a steering drag also fired a tap on lift")
	if not touch._world_pend.is_empty() or not touch.world_point().is_empty():
		_bad("a lifted drag left a live world pointer")
	main._tap_move_ref().cancel("pointer reset")
	taps.clear()

	_down(14, open_point)
	var hold_start: int = Time.get_ticks_msec()
	while Time.get_ticks_msec() - hold_start < int(touch.HOLD_MS) + 80:
		await process_frame
	await _frames(2)
	if not bool(touch.world_point().get("held", false)):
		_bad("a still press held past HOLD_MS did not become a point")
	if not bool(main.touch_follow_active):
		_bad("holding on open water did not steer Roshan toward the finger")
	_up(14, open_point)
	await process_frame
	if not taps.is_empty():
		_bad("a steering hold also fired a tap on lift")
	main._tap_move_ref().cancel("pointer reset")
	taps.clear()

	var forward := Vector3(sin(float(main.player.yaw)), 0.0, cos(float(main.player.yaw)))
	main._tap_move_ref().start(main.player.position + forward * 5000.0)
	if not bool(main.touch_auto_at_edge):
		_bad("a route clamped at the world's edge is not reported as an edge")
	await _frames(2)
	if not touch.travel_goal_at_edge():
		_bad("an edge route does not show the edge marker")
	main._tap_move_ref().cancel("pointer reset")
	await _frames(6)
	if touch.travel_goal_visible():
		_bad("the destination marker outlived its route")
	main.clear_dialogue()

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

func _dispatch_mouse(pos: Vector2, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.device = 0
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
