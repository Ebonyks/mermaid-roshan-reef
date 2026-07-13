extends SceneTree
# Mouse-look check: inject a right-button drag and confirm cam_orbit /
# cam_pitch_off move, then release and confirm they drift back toward zero.
# Also injects a LEFT-button drag to confirm it does NOT move the camera.

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for f in range(20):
		await process_frame
	var player: Node = main.get_node_or_null("Player")
	if player == null:
		for c in main.get_children():
			if c.get_script() != null and String(c.get_script().resource_path).ends_with("player.gd"):
				player = c
				break
	if player == null:
		print("FAIL no player node found")
		quit()
		return
	print("orbit_start=%.4f pitch_start=%.4f" % [player.cam_orbit, player.cam_pitch_off])

	# LEFT-button drag must not orbit (left belongs to games / touch stick)
	_send_button(MOUSE_BUTTON_LEFT, true)
	for f in range(10):
		_send_motion(Vector2(40, 0), MOUSE_BUTTON_MASK_LEFT)
		await process_frame
	_send_button(MOUSE_BUTTON_LEFT, false)
	await process_frame
	var orbit_left: float = player.cam_orbit
	if absf(orbit_left) > 0.02:
		print("FAIL left-drag moved camera: orbit=%.4f" % orbit_left)
	else:
		print("PASS left-drag ignored: orbit=%.4f" % orbit_left)

	# RIGHT-button drag must orbit and pitch
	_send_button(MOUSE_BUTTON_RIGHT, true)
	for f in range(15):
		_send_motion(Vector2(30, 12), MOUSE_BUTTON_MASK_RIGHT)
		await process_frame
	var orbit_held: float = player.cam_orbit
	var pitch_held: float = player.cam_pitch_off
	print("after right-drag: orbit=%.4f pitch=%.4f" % [orbit_held, pitch_held])
	if absf(orbit_held) < 0.2 or absf(pitch_held) < 0.5:
		print("FAIL right-drag did not move camera enough")
	else:
		print("PASS right-drag orbits + pitches")

	# holding still with button down must HOLD the peek (no drift)
	for f in range(30):
		await process_frame
	if absf(player.cam_orbit - orbit_held) > 0.05:
		print("FAIL peek did not hold while button down: orbit=%.4f" % player.cam_orbit)
	else:
		print("PASS peek holds while button down")

	# release: camera drifts back behind her (wall-clock wait — headless
	# frames are not 1/60s, and the drift lerp runs on real delta)
	_send_button(MOUSE_BUTTON_RIGHT, false)
	var t0: int = Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 3000:
		await process_frame
	print("after release: orbit=%.4f pitch=%.4f" % [player.cam_orbit, player.cam_pitch_off])
	if absf(player.cam_orbit) < absf(orbit_held) * 0.25 and absf(player.cam_pitch_off) < absf(pitch_held) * 0.25:
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
