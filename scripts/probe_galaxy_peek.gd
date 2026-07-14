extends SceneTree
# Galaxy-mode look-around check: start the Butterfly World, inject a
# right-button drag, and confirm the galaxy camera orbits/pitches, holds
# while the button is down, and drifts back after release. Mirrors
# probe_mouselook.gd (free-swim); wall-clock waits per the headless rule.

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for f in range(20):
		await process_frame
	main._start_galaxy()
	for f in range(30):
		await process_frame
	var g: Node = main.galaxy_game
	if g == null:
		print("FAIL galaxy did not start")
		quit()
		return
	print("galaxy up: orbit=%.4f pitch=%.4f" % [g._cam_orbit, g._cam_pitch])

	# LEFT-drag control: must not move the peek
	_send_button(MOUSE_BUTTON_LEFT, true)
	for f in range(10):
		_send_motion(Vector2(40, 0), MOUSE_BUTTON_MASK_LEFT)
		await process_frame
	_send_button(MOUSE_BUTTON_LEFT, false)
	await process_frame
	if absf(g._cam_orbit) > 0.02:
		print("FAIL left-drag moved galaxy camera: %.4f" % g._cam_orbit)
	else:
		print("PASS left-drag ignored")

	# RIGHT-drag: orbit + pitch
	_send_button(MOUSE_BUTTON_RIGHT, true)
	for f in range(15):
		_send_motion(Vector2(30, 12), MOUSE_BUTTON_MASK_RIGHT)
		await process_frame
	var oh: float = g._cam_orbit
	var ph: float = g._cam_pitch
	print("after right-drag: orbit=%.4f pitch=%.4f" % [oh, ph])
	if absf(oh) < 0.2 or absf(ph) < 0.3:
		print("FAIL right-drag did not move galaxy camera")
	else:
		print("PASS right-drag orbits + pitches")

	# camera position actually responds (not just the state vars)
	var cam: Camera3D = g._cam
	var p0: Vector3 = cam.position
	for f in range(20):
		await process_frame
	print("cam moved %.2f units while peeked" % p0.distance_to(cam.position))

	# release -> drift back (wall clock)
	_send_button(MOUSE_BUTTON_RIGHT, false)
	var t0: int = Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 3000:
		await process_frame
	print("after release: orbit=%.4f pitch=%.4f" % [g._cam_orbit, g._cam_pitch])
	if absf(g._cam_orbit) < absf(oh) * 0.25 and absf(g._cam_pitch) < absf(ph) * 0.25:
		print("PASS drifts back after release")
	else:
		print("FAIL did not drift back after release")
	quit()

func _send_button(idx: int, pressed: bool) -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = idx
	ev.pressed = pressed
	ev.position = Vector2(800, 450)
	Input.parse_input_event(ev)

func _send_motion(rel: Vector2, mask: int) -> void:
	var ev := InputEventMouseMotion.new()
	ev.relative = rel
	ev.position = Vector2(800, 450)
	ev.button_mask = mask
	Input.parse_input_event(ev)
