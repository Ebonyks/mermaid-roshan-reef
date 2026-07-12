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
	# 4) Roshan can now descend through the opening to the undercroft floor
	player.position = br + Vector3(0, 4, -1)
	player.vel = Vector3.ZERO
	await _wait_ms(4000)   # gravity sink, by wall clock
	_ck("descends to the undercroft", player.position.y - h.y < -14.0,
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
	for wp in [Vector3(7, -12, -20), Vector3(-17, -12, -2), Vector3(17, -12, -28)]:
		player.position = h + wp
		player.vel = Vector3.ZERO
		await _wait_ms(900)
		_ck("basement floor at (%d, %d)" % [int(wp.x), int(wp.z)], player.position.y - h.y < -14.0,
			"y=%.1f" % (player.position.y - h.y))
	await _shot("basement_hallway", h + Vector3(0, -8, 0), h + Vector3(0, -16, -30))
	# 7) the royal loo waits at the very bottom of the basement hallway
	_ck("toilet exists", main.g.has("toilet"))
	if main.g.has("toilet"):
		var tpos: Vector3 = (main.g["toilet"] as Dictionary)["pos"]
		_ck("toilet is down in the basement", tpos.y - h.y < -10.0 and tpos.z - h.z < -35.0,
			"rel=(%.1f, %.1f, %.1f)" % [tpos.x - h.x, tpos.y - h.y, tpos.z - h.z])
		player.position = h + Vector3(-3.0, -15.5, -41.0)
		player.vel = Vector3.ZERO
		await _frames(30)
		var td: Dictionary = main.g["toilet"]
		_ck("toilet toots on approach", not bool(td.get("armed", true)))
		await _shot("royal_loo", h + Vector3(1, -13, -36), h + Vector3(-6, -16, -42))
	print("BASEMENT|RESULT: ", ("ALL OK" if checks_failed == 0 else "%d FAIL" % checks_failed))
	quit()
