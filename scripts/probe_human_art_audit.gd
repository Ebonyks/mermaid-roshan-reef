extends SceneTree

const OUT := "res://audit/runtime_shots_2026-07-16"

var main: Node3D
var camera: Camera3D
# Where the frames actually land. The CI capture step runs this probe inside
# the same block as probe_reef_shots and uploads $REEF_SHOT_OUT/*.png — a
# hardcoded res:// path renders the shots into the workspace and throws them
# away, so honour the same env var the sibling capture probes use (2026-08-02:
# that is why the water-FX inspection frames never reached the artifact).
var out_dir := ""

func _frames(count: int) -> void:
	for i in range(count):
		await process_frame

func _shot(name: String, position: Vector3 = Vector3.ZERO, target: Vector3 = Vector3.ZERO, use_hold: bool = false, up: Vector3 = Vector3.UP) -> void:
	if use_hold:
		camera.position = position
		camera.look_at(target, up)
		camera.make_current()
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var err: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("ART_AUDIT|saved ", name, " -> ", out_dir, (" ERR %d" % err) if err != OK else "")

func _fresh_main() -> Node3D:
	if main != null and is_instance_valid(main):
		main.queue_free()
		await _frames(3)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as Node3D
	get_root().add_child(main)
	await _frames(3)
	main._skip_intro()
	await _frames(20)
	return main

func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("ART_AUDIT|RESULT: HEADLESS SKIP (visual capture requires a display renderer)")
		quit()
		return
	var requested: String = OS.get_environment("REEF_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path(OUT)
	DirAccess.make_dir_recursive_absolute(out_dir)
	camera = Camera3D.new()
	camera.fov = 66.0
	get_root().add_child(camera)
	await _fresh_main()
	await _shot("01_reef_hub", Vector3(20, 15, 42), Vector3(0, 3, 0), true)
	await _shot("02_reef_props", Vector3(52, 11, 28), Vector3(62, 3, 8), true)
	main._enter_level2()
	await _frames(35)
	var level_origin: Vector3 = main.LEVEL2_POS
	await _shot("03_sky_lagoon_overview", level_origin + Vector3(80, 58, 88), level_origin + Vector3(0, 18, -90), true)
	await _shot("04_clouds_and_castle", level_origin + Vector3(5, 52, -35), level_origin + Vector3(0, 48, -125), true)
	await _shot("05_dream_star", level_origin + main.L2_STAR_SPOTS[0] + Vector3(12, 8, 18), level_origin + main.L2_STAR_SPOTS[0] + Vector3(0, 4, 0), true)
	main._enter_castle_interior()
	await _frames(30)
	var castle_rooms: CastleRooms25D = main._castle_rooms_ref()
	castle_rooms.show_room("main_hall", false)
	await _shot("06_castle_main_hall_sprite3d")
	castle_rooms.show_room("opera_hall", false)
	await _shot("07_castle_opera_hall_sprite3d")
	castle_rooms.show_room("bubble_bath", false)
	await _shot("08_castle_bubble_bath_sprite3d")
	await _fresh_main()
	main._start_galaxy()
	await _frames(45)
	await _shot("09_butterfly_world")
	var galaxy: Node = main.galaxy_game
	if galaxy != null and galaxy.get("_home_pos") != null:
		var home: Vector3 = galaxy.get("_home_pos")
		await _shot("10_butterfly_home_gate", home + Vector3(10, 7, 14), home + Vector3(0, 3, 0), true)
	await _fresh_main()
	main.game = "level2"
	main.g["t"] = 0.0
	main.dungeon_progress = 0
	main._start_dungeon()
	await _frames(35)
	await _shot("11_dungeon_combat")
	if main.dungeon_game != null:
		main.dungeon_game._leave_early()
	await _frames(8)
	main.dungeon_progress = 1
	main._start_dungeon()
	await _frames(35)
	await _shot("12_dungeon_puzzle")
	await _fresh_main()
	main._start_kart_game(false, "terrain")
	await _frames(45)
	await _shot("13_kart_world")
	await _fresh_main()
	main._start_game(main.fairy_fr)
	await _frames(25)
	var fairy_origin: Vector3 = main.ARENA_POS
	await _shot("14_fairy_pond_flight", fairy_origin + Vector3(0, 58, 95), fairy_origin + Vector3(0, 0, 95), true, Vector3(0, 0, 1))
	main.g["fz"] = FairyGame.FS_LEN
	main._game_obj("fairyshoot", FairyGame)._fairy_start_boss(fairy_origin)
	await _frames(5)
	var flower: Vector3 = main.g["boss_center"]
	await _shot("15_fairy_flower_seed", flower + Vector3(0, 58, 0), flower, true, Vector3(0, 0, 1))
	for leaf_data in main.g["leaves"]:
		if is_instance_valid(leaf_data["node"]):
			(leaf_data["node"] as Node3D).queue_free()
	main.g["leaves"] = []
	main.g["phase"] = "boss_bud"
	main.g["phase_t"] = 99.0
	main.g["bud_hp"] = 10
	await _frames(3)
	await _shot("16_fairy_flower_sprout", flower + Vector3(0, 58, 0), flower, true, Vector3(0, 0, 1))
	main.g["bud_hp"] = 6
	await _frames(3)
	await _shot("17_fairy_flower_bud", flower + Vector3(0, 58, 0), flower, true, Vector3(0, 0, 1))
	main.g["bud_hp"] = 2
	await _frames(3)
	await _shot("18_fairy_flower_opening", flower + Vector3(0, 58, 0), flower, true, Vector3(0, 0, 1))
	main._game_obj("fairyshoot", FairyGame)._fairy_bloom_start()
	main.g["bloom_t"] = FairyGame.FS_BLOOM_T * 0.2
	await _frames(3)
	await _shot("19_fairy_flower_bloom", flower + Vector3(0, 58, 0), flower, true, Vector3(0, 0, 1))
	# ---- water physics + FX institution (2026-08-02): the Jolt prop fleet,
	# the swell and the fx_water card vocabulary have NEVER been human-
	# inspected (probe-validated only). These frames are the first look.
	await _fresh_main()
	main.brawl_cool = 0.0
	main._start_game(main.brawl_fr)
	await _frames(50)
	var brawl_o: Vector3 = main.ARENA_POS + Vector3(0, 2.5, 0)
	await _shot("20_toy_castle_block_fleet_swell", brawl_o + Vector3(-8, 9, 21), brawl_o + Vector3(-6, 1.5, 0), true)
	main.fx_splash(brawl_o + Vector3(-2, 3.5, 2.0), 20.0, "art_audit_a")
	await _frames(8)
	await _shot("21_water_fx_breach_card", brawl_o + Vector3(-2, 5, 14), brawl_o + Vector3(-2, 3, 0), true)
	main._fx_water_ref().card("splash_small", brawl_o + Vector3(-6, 3.5, 2.0))
	main._fx_water_ref().card("bubble_burst", brawl_o + Vector3(2, 3.5, 2.0))
	await _frames(6)
	await _shot("22_water_fx_small_and_bubbles", brawl_o + Vector3(-2, 5, 14), brawl_o + Vector3(-2, 3, 0), true)
	print("ART_AUDIT|DONE")
	quit()
