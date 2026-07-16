extends SceneTree

const OUT := "res://audit/runtime_shots_2026-07-16"

var main: Node3D
var camera: Camera3D

func _frames(count: int) -> void:
	for i in range(count):
		await process_frame

func _shot(name: String, position: Vector3 = Vector3.ZERO, target: Vector3 = Vector3.ZERO, use_hold: bool = false) -> void:
	if use_hold:
		camera.position = position
		camera.look_at(target, Vector3.UP)
		camera.make_current()
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	image.save_png(OUT + "/" + name + ".png")
	print("ART_AUDIT|saved ", name)

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
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
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
	var hall: Vector3 = main.CASTLE_POS
	await _shot("06_castle_hall", hall + Vector3(0, 13, 40), hall + Vector3(0, 13, -24), true)
	await _shot("07_crown_star", hall + Vector3(0, 20, -2), hall + Vector3(0, 24, -28), true)
	await _shot("08_star_chamber", hall + Vector3(-18, 40, -35), hall + Vector3(-28, 42, -58), true)
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
	print("ART_AUDIT|DONE")
	quit()
