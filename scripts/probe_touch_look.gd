extends SceneTree
# Touch look-around check (run with `-- --touch` so wants_touch() is true):
# finger 0 steers; a second finger must split three ways —
#   quick tap        -> jump pulse (action_just)
#   still hold       -> HELD jump (action_down) after JUMP_HOLD_MS
#   drag past slop   -> camera peek (orbit/pitch), NO jump, drift back on lift
# Covered in free swim AND galaxy mode. Wall-clock waits (headless frames
# are not 1/60s).

var _f := {}   # finger idx -> last position

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for f in range(20):
		await process_frame
	var touch: CanvasLayer = main.touch_ui
	var player: Node = main.get_node_or_null("Player")
	if player == null:
		for c in main.get_children():
			if c.get_script() != null and String(c.get_script().resource_path).ends_with("player.gd"):
				player = c
				break
	if touch == null or player == null:
		print("FAIL touch_ui or player missing")
		quit()
		return
	if not touch.wants_touch():
		print("FAIL wants_touch() false — probe must run with -- --touch")
		quit()
		return

	# ---- steer with finger 0 (stick sanity)
	_down(0, Vector2(400, 700))
	_move(0, Vector2(460, 700))
	await process_frame
	if (touch.stick_vec as Vector2).length() < 0.3:
		print("FAIL stick did not engage: %s" % touch.stick_vec)
	else:
		print("PASS stick steers")

	# ---- second finger quick tap = jump pulse
	touch.consume_action_just()
	_down(1, Vector2(1200, 700))
	await process_frame
	_up(1, Vector2(1200, 700))
	await process_frame
	if bool(touch.consume_action_just()):
		print("PASS second-finger tap jumps")
	else:
		print("FAIL second-finger tap did not jump")

	# ---- second finger DRAG = camera, and must NOT jump
	touch.consume_action_just()
	var orbit0: float = player.cam_orbit
	_down(1, Vector2(1200, 700))
	for i in range(12):
		_move(1, Vector2(1200 + 40 * (i + 1), 700 - 8 * (i + 1)))
		await process_frame
	var jumped: bool = bool(touch.consume_action_just())
	print("drag: orbit=%.4f pitch=%.4f look_active=%s" % [player.cam_orbit, player.cam_pitch_off, touch.look_active()])
	if absf(player.cam_orbit - orbit0) < 0.2:
		print("FAIL camera drag did not orbit")
	elif jumped:
		print("FAIL camera drag fired a jump")
	else:
		print("PASS second-finger drag drives camera, no jump")
	var oh: float = player.cam_orbit

	# ---- lift the camera finger -> peek drifts back (wall clock)
	_up(1, _f[1])
	var t0: int = Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 3000:
		await process_frame
	if absf(player.cam_orbit) < absf(oh) * 0.25:
		print("PASS drifts back after camera finger lifts")
	else:
		print("FAIL no drift back: orbit=%.4f (was %.4f)" % [player.cam_orbit, oh])

	# ---- second finger HELD STILL = held jump after the decision window
	touch.consume_action_just()
	_down(1, Vector2(1300, 800))
	t0 = Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 300:
		await process_frame
	if bool(touch.action_down):
		print("PASS still hold becomes HELD jump")
	else:
		print("FAIL still hold did not become held jump")
	_up(1, Vector2(1300, 800))
	await process_frame
	if not bool(touch.action_down):
		print("PASS held jump releases")
	else:
		print("FAIL action_down stuck after release")

	# Home/interruption can arrive without matching finger-up events.  The
	# lifecycle notification must clear every held gesture immediately.
	_down(0, Vector2(400, 700))
	_move(0, Vector2(470, 700))
	_down(1, Vector2(1200, 700))
	await process_frame
	touch.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	await process_frame
	if (touch.stick_vec as Vector2).is_zero_approx() and not bool(touch.action_down) and not touch.look_active():
		print("PASS focus loss clears touch state")
	else:
		print("FAIL focus loss left touch state active")
	_up(0, _f[0])
	await process_frame

	# ---- galaxy mode: same gesture drives the galaxy camera
	main._start_galaxy()
	for f in range(30):
		await process_frame
	var g: Node = main.galaxy_game
	if g == null:
		print("FAIL galaxy did not start")
		quit()
		return
	_down(0, Vector2(400, 700))
	_move(0, Vector2(430, 700))
	await process_frame
	_down(1, Vector2(1200, 700))
	for i in range(12):
		_move(1, Vector2(1200 + 40 * (i + 1), 700))
		await process_frame
	print("galaxy drag: orbit=%.4f" % g._cam_orbit)
	if absf(g._cam_orbit) > 0.2:
		print("PASS galaxy touch camera works")
	else:
		print("FAIL galaxy touch camera dead")
	_up(1, _f[1])
	_up(0, _f[0])
	quit()

func _down(idx: int, pos: Vector2) -> void:
	_f[idx] = pos
	var ev := InputEventScreenTouch.new()
	ev.index = idx
	ev.position = pos
	ev.pressed = true
	Input.parse_input_event(ev)

func _move(idx: int, pos: Vector2) -> void:
	var ev := InputEventScreenDrag.new()
	ev.index = idx
	ev.position = pos
	ev.relative = pos - (_f[idx] as Vector2)
	_f[idx] = pos
	Input.parse_input_event(ev)

func _up(idx: int, pos: Vector2) -> void:
	var ev := InputEventScreenTouch.new()
	ev.index = idx
	ev.position = pos
	ev.pressed = false
	Input.parse_input_event(ev)
