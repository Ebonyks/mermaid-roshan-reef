extends SceneTree
# Castle-basement stairwell probe: the golden stand seals the undercroft's
# back stairwell, glows, and rumbles aside when Roshan gets close; a small
# royal loo lives at the end of the treasure room. Prints OK/FAIL lines
# (ci.sh convention). When run with a display it also saves screenshots to
# user://probe_basement/.

var main: Node
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("BASEMENT|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _wait_ms(ms: int) -> void:
	# headless frames are not 1/60s — waits that must cover tweens/gravity
	# (which advance by delta seconds) go by wall clock instead
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < ms:
		await process_frame

func _shot(name: String, pos: Vector3, look: Vector3) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var cam: Camera3D = main.player.cam
	if cam == null:
		return
	var hold := Camera3D.new()
	hold.fov = 70.0
	get_root().add_child(hold)
	hold.position = pos
	hold.look_at(look, Vector3.UP)
	hold.current = true
	await process_frame
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("user://probe_basement")
	get_root().get_viewport().get_texture().get_image().save_png("user://probe_basement/" + name + ".png")
	print("BASEMENT|shot saved: ", name)
	cam.current = true
	hold.queue_free()

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	await _frames(10)
	main._enter_level2()
	await _frames(20)
	main._enter_castle_interior()
	await _frames(20)
	var h: Vector3 = main.CASTLE_POS
	var br: Vector3 = h + Vector3(0, 0, -46.0)
	var player: Node3D = main.player
	# 1) the stand starts closed and the shaft is sealed from above: parked over
	# the opening at hallway level, Roshan must NOT sink through the floor.
	# (Spawn is far away at the entrance, so the stand trigger cannot fire yet.)
	player.position = br + Vector3(0, 4, 8)
	player.vel = Vector3.ZERO
	main.g["stand_armed"] = false   # pin: this check must run against the sealed shaft
	player.position = br + Vector3(0, 4, -1)
	await _frames(40)
	_ck("sealed shaft holds the hallway floor", player.position.y - h.y > 1.5,
		"y=%.1f" % (player.position.y - h.y))
	_ck("stand starts closed", not bool(main.g.get("stand_open", false)))
	await _shot("closed_stand", br + Vector3(0, 8, 9), br + Vector3(0, 3, -3))
	# 2) sealed from below too: dropped into the shaft, she cannot pop up into
	# the hallway (the closed zone caps her at -2).
	player.position = br + Vector3(0, -4, -1)
	player.vel = Vector3(0, 20, 0)
	await _wait_ms(800)
	_ck("sealed shaft caps from below", player.position.y - h.y < -1.0,
		"y=%.1f" % (player.position.y - h.y))
	# 3) arm (>14 away) then approach: the stand slides aside with the rumble.
	player.position = br + Vector3(0, 4, 8)   # out of the shaft first
	player.vel = Vector3.ZERO
	await _frames(5)
	player.position = h + Vector3(0, 6, 20)   # far: arms the trigger
	player.vel = Vector3.ZERO
	await _frames(10)
	_ck("stand armed after distance", bool(main.g.get("stand_armed", false)))
	player.position = br + Vector3(0, 4, 8)   # ~9.5 from the stand: fires
	player.vel = Vector3.ZERO
	await _frames(10)
	_ck("stand slides on approach", bool(main.g.get("stand_open", false)))
	await _wait_ms(2500)   # let the tween + rumble finish (1.6s, by wall clock)
	var chest: Node3D = main.g.get("stand_chest")
	_ck("stand cleared the opening", is_instance_valid(chest) and absf(chest.position.x - br.x) > 8.0,
		"chest_x_off=%.1f" % (chest.position.x - br.x if is_instance_valid(chest) else 0.0))
	var zd: Dictionary = main.g.get("stand_zone", {})
	_ck("shaft zone opened", not zd.has("ceil") and (zd.get("band", Vector2.ZERO) as Vector2).y > 3.0)
	await _shot("open_stairwell", br + Vector3(0, 10, 10), br + Vector3(0, -2, -3))
	# 4) the revealed staircase is SOLID: Roshan lands on the top steps instead
	# of free-falling through them, then walks the flight down into the basement
	player.position = br + Vector3(0, 4, -1)
	player.vel = Vector3.ZERO
	await _wait_ms(1500)
	var sy: float = player.position.y - h.y
	_ck("lands on the stairwell steps", sy < -1.0 and sy > -8.0, "y=%.1f" % sy)
	var t1 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t1 < 3000:
		player.vel = Vector3(0, -4.0, 9.0)   # walk down the flight (toward +z)
		await process_frame
	player.vel = Vector3.ZERO
	await _wait_ms(800)
	_ck("stairs walk down to the basement", player.position.y - h.y < -14.0,
		"y=%.1f" % (player.position.y - h.y))
	await _shot("undercroft", br + Vector3(0, -12, 6), br + Vector3(0, -16, -2))
	# 5) the treasure-room floor still holds everywhere else
	player.position = br + Vector3(-15, 4, 5)
	player.vel = Vector3.ZERO
	await _frames(40)
	_ck("hallway floor intact off the opening", player.position.y - h.y > 1.5,
		"y=%.1f" % (player.position.y - h.y))
	# 6) the basement wing: the widened hallway and the side rooms all hold the
	# basement floor (each point was OUTSIDE the old 12-wide corridor zone)
	# (the craft-room point stays >7 from the easel or the craft studio would
	# open and freeze player physics for the rest of the probe)
	for wp in [Vector3(7, -12, -20), Vector3(-17, -12, -2), Vector3(13, -12, -28), Vector3(-30, -12, -28)]:
		player.position = h + wp
		player.vel = Vector3.ZERO
		await _wait_ms(900)
		_ck("basement floor at (%d, %d)" % [int(wp.x), int(wp.z)], player.position.y - h.y < -14.0,
			"y=%.1f" % (player.position.y - h.y))
		if main.craft_layer != null:
			main._close_craft()   # safety: never leave an overlay freezing physics
			await _frames(5)
	await _shot("basement_hallway", h + Vector3(0, -8, 0), h + Vector3(0, -16, -30))
	# 7) the royal loo hides in the secret privy behind the Bubble Bath — deep
	# in the far corner of the basement, not out in the open
	_ck("toilet exists", main.g.has("toilet"))
	if main.g.has("toilet"):
		var tpos: Vector3 = (main.g["toilet"] as Dictionary)["pos"]
		_ck("toilet hides deep in the basement", tpos.y - h.y < -10.0 and tpos.x - h.x < -25.0,
			"rel=(%.1f, %.1f, %.1f)" % [tpos.x - h.x, tpos.y - h.y, tpos.z - h.z])
		player.position = h + Vector3(-30.5, -15.5, -28.0)
		player.vel = Vector3.ZERO
		await _frames(30)
		var td: Dictionary = main.g["toilet"]
		_ck("toilet toots on approach", not bool(td.get("armed", true)))
		await _shot("royal_loo", h + Vector3(-27, -13, -24), h + Vector3(-32, -16, -28))
	# 7b) the craft easel moved into its dedicated basement craft room
	if main.g.has("craft_easel"):
		var cev: Vector3 = main.g["craft_easel"]
		_ck("craft easel lives in the craft room", cev.y - h.y < -8.0 and cev.x - h.x > 14.0,
			"rel=(%.1f, %.1f, %.1f)" % [cev.x - h.x, cev.y - h.y, cev.z - h.z])
	# 7c) the Dreaming Floor: the flight up holds, and the bedroom floor holds
	player.position = h + Vector3(-12, 44, -41)    # mid-flight to the third story
	player.vel = Vector3.ZERO
	await _wait_ms(900)
	_ck("dreaming stairs hold", player.position.y - h.y > 39.0 and player.position.y - h.y < 45.0,
		"y=%.1f" % (player.position.y - h.y))
	player.position = h + Vector3(-36, 54, -57.5)  # Princess Huluu's bedroom
	player.vel = Vector3.ZERO
	await _wait_ms(900)
	_ck("dreaming floor holds", player.position.y - h.y > 49.5 and player.position.y - h.y < 52.5,
		"y=%.1f" % (player.position.y - h.y))
	# 7d) WALK the flight both ways — the whole route, not just static points.
	# (Two launch bugs hid here: an ungoverned strip of the opening was an
	# invisible floor, and the chamber divider's collider walled off the top.)
	player.position = h + Vector3(-22, 36, -41)    # Star Chamber floor, at the flight's base
	player.vel = Vector3.ZERO
	await _wait_ms(600)
	var t2 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t2 < 3000:
		player.vel = Vector3(9.0, 4.0, 0)    # walk east, up the flight
		await process_frame
	player.vel = Vector3.ZERO
	await _wait_ms(600)
	_ck("dreaming stairs walk up", player.position.y - h.y > 49.5,
		"y=%.1f x=%.1f" % [player.position.y - h.y, player.position.x - h.x])
	player.position = h + Vector3(-4, 51, -41)     # east edge of the opening
	player.vel = Vector3.ZERO
	await _wait_ms(600)
	var t3 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t3 < 3000:
		player.vel = Vector3(-9.0, -4.0, 0)   # walk west, down the flight
		await process_frame
	player.vel = Vector3.ZERO
	await _wait_ms(600)
	_ck("dreaming stairs walk back down", player.position.y - h.y < 40.0,
		"y=%.1f" % (player.position.y - h.y))
	await _shot("dreaming_floor", h + Vector3(-6, 56, -39), h + Vector3(-20, 51, -57))
	# 8) every castle staircase is solid — Roshan rests ON the steps at the
	# ramp height for that spot instead of sinking through to the floor below
	player.position = h + Vector3(0, 12, -16)      # royal staircase, mid-flight
	player.vel = Vector3.ZERO
	await _wait_ms(900)
	_ck("royal staircase holds", player.position.y - h.y > 4.0 and player.position.y - h.y < 12.0,
		"y=%.1f" % (player.position.y - h.y))
	player.position = h + Vector3(30.5, 24, -28)   # balcony stairs (right), mid-flight
	player.vel = Vector3.ZERO
	await _wait_ms(900)
	_ck("balcony stairs hold (right)", player.position.y - h.y > 17.0 and player.position.y - h.y < 24.0,
		"y=%.1f" % (player.position.y - h.y))
	player.position = h + Vector3(-30.5, 24, -28)  # balcony stairs (left), mid-flight
	player.vel = Vector3.ZERO
	await _wait_ms(900)
	_ck("balcony stairs hold (left)", player.position.y - h.y > 17.0 and player.position.y - h.y < 24.0,
		"y=%.1f" % (player.position.y - h.y))
	player.position = h + Vector3(-24, 2, 28)      # front-shaft stairs down
	player.vel = Vector3.ZERO
	await _wait_ms(900)
	_ck("front shaft stairs hold", player.position.y - h.y > -7.0 and player.position.y - h.y < -2.0,
		"y=%.1f" % (player.position.y - h.y))
	print("BASEMENT|RESULT: ", ("ALL OK" if checks_failed == 0 else "%d FAIL" % checks_failed))
	quit()
