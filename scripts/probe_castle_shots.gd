extends SceneTree
# Texture verification captures: reef seabed/rocks, snow + cavern arenas,
# Sky Lagoon keep, castle hall + side rooms.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/4b731d89-dcfc-4376-9e9b-a5171faf67ef/scratchpad/castle_shots"

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
	await _settle(30)
	# ---- Level 1 reef: seabed sand + rocks (BEFORE unlocking, so no finale/night state) ----
	await _shot("tex_reef_seabed", Vector3(20, 14, 40), Vector3(0, 0, 0))
	await _shot("tex_reef_rocks", Vector3(45, 8, 25), Vector3(60, 2, 5))
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	# ---- snow minigame arena ----
	main._enter_arena("fetch")
	await _settle(30)
	var a: Vector3 = main.ARENA_POS
	await _shot("tex_arena_snow", a + Vector3(0, 12, 30), a + Vector3(0, 0, 0))
	main.arena_env.glow_enabled = false
	await _shot("tex_arena_snow_noglow", a + Vector3(0, 12, 30), a + Vector3(0, 0, 0))
	main.arena_env.glow_enabled = true
	main._leave_arena()
	await _settle(10)
	# ---- treasure cavern arena ----
	main._enter_arena("treasure")
	await _settle(30)
	await _shot("tex_arena_cavern", a + Vector3(0, 12, 30), a + Vector3(0, 0, 0))
	main._leave_arena()
	await _settle(10)
	# ---- Sky Lagoon + castle ----
	main._enter_level2()
	await _settle(30)
	var o: Vector3 = main.LEVEL2_POS if "LEVEL2_POS" in main else main.arena_center
	var c: Vector3 = o + Vector3(0, 0, -120.0)
	await _shot("tex_keep_facade", c + Vector3(0, 20, 90), c + Vector3(0, 30, 0))
	main._enter_castle_interior()
	await _settle(30)
	var h: Vector3 = main.CASTLE_POS
	await _shot("tex_hall_entrance", h + Vector3(0, 10, 40), h + Vector3(0, 14, -20))
	await _shot("tex_hall_backroom", h + Vector3(0, 10, -36), h + Vector3(6, 4, -48))
	await _shot("tex_room_music", h + Vector3(-36, 12, -16), h + Vector3(-46, 2, -5))
	await _shot("tex_room_bedroom", h + Vector3(36, 12, -16), h + Vector3(46, 3, -16))
	print("PROBE DONE")
	quit()
