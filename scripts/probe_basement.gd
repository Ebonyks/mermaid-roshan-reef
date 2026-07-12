extends SceneTree
# Verify the castle basement feature: glowing stand, slide-away reveal,
# stairwell + basement geometry, floor clamp, and the hallway toilet.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/9934dffd-4309-4be8-9356-d02892717e45/scratchpad/basement_verify"

var cam: Camera3D

func _shot(name: String, pos: Vector3, look: Vector3) -> void:
	cam.position = pos
	cam.look_at(look, Vector3.UP)
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + name + ".png")
	print("saved ", name)

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	cam = Camera3D.new()
	cam.fov = 70.0
	get_root().add_child(cam)
	cam.current = true
	DirAccess.make_dir_recursive_absolute(OUT)
	main.is_night = false
	main._apply_time_of_day()
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	await _settle(10)
	main._enter_level2()
	await _settle(30)
	main._enter_castle_interior()
	await _settle(30)
	var h: Vector3 = main.CASTLE_POS
	var br: Vector3 = h + Vector3(0, 0, -46.0)
	# park the player away from every trigger (hall entrance) for the "before" shots
	main.player.position = h + Vector3(0, 6, 30)
	main.player.vel = Vector3.ZERO
	await _settle(10)
	# 1) closed stand on its carpet (glow pulse) + hallway with toilet at the end
	await _shot("v_stand_closed", br + Vector3(0, 8, 9), br + Vector3(0, 3, -3))
	await _shot("v_hallway_toilet", br + Vector3(-8, 7, 5), br + Vector3(-21, 3, 0))
	await _shot("v_toilet_close", br + Vector3(-15, 6, 4), br + Vector3(-21, 3, 0))
	# 2) trigger the reveal, let the tween + sound run
	main._slide_basement_stand()
	await _settle(130)
	print("stand_open=", main.g.get("stand_open"), " secret_door=", main.g.get("secret_door"))
	await _shot("v_stand_open_top", br + Vector3(0, 10, 10), br + Vector3(0, -2, -3))
	await _shot("v_stairwell", br + Vector3(0, 4, 6), br + Vector3(0, -8, -6))
	# 3) drop the player into the basement ROOM (clear of the stair ramp), check the
	# floor clamp holds her down there
	main.player.position = br + Vector3(10, -6, 0)
	main.player.vel = Vector3.ZERO
	await _settle(60)
	var py: float = main.player.position.y - h.y
	print("player y rel hall floor after settle (expect about -9.5): ", py)
	await _shot("v_basement_room", br + Vector3(-14, -4, 7), br + Vector3(8, -9, -3))
	await _shot("v_basement_stairs", br + Vector3(-8, -6, -7), br + Vector3(2, -2, 3))
	# 4) player can NOT sink through the hallway floor away from the opening
	main.player.position = br + Vector3(-15, 4, 5)
	main.player.vel = Vector3.ZERO
	await _settle(60)
	print("player y on hallway floor (expect about +2.5): ", main.player.position.y - h.y)
	# 5) chase-cam view: player descending the stairs (cutaway check)
	main.player.position = br + Vector3(0, -3, -2)
	main.player.vel = Vector3.ZERO
	await _settle(40)
	var pc: Camera3D = main.player.cam
	if pc != null:
		cam.position = pc.global_position
		cam.rotation = pc.global_rotation
		await process_frame
		await RenderingServer.frame_post_draw
		get_root().get_viewport().get_texture().get_image().save_png(OUT + "/v_chasecam_stairs.png")
		print("saved v_chasecam_stairs")
	print("PROBE DONE")
	quit()
