extends SceneTree
const MAIN_SCENE := preload("res://scenes/main.tscn")
const WORLD_SCRIPT := preload("res://scripts/opera_career_world_2d.gd")
var main: ReefMain
func _init() -> void:
	call_deferred("_run")
func _run() -> void:
	main = MAIN_SCENE.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	if main.start_menu_layer != null:
		main.start_menu_layer.visible = false
	main.start_menu_active = false
	main.clear_dialogue()
	main.hud_msg.visible = false
	main.chapter2_active = true
	main.chapter2_strawberry_mask = 0x1F
	main.set_process(false)
	var width := int(OS.get_environment("CHEF_CAPTURE_WIDTH"))
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_size(Vector2i(width, 720))
	await process_frame
	await process_frame
	var out := OS.get_environment("CHEF_CAPTURE_OUT")
	DirAccess.make_dir_recursive_absolute(out)
	var masks: Array[int] = [0, 1, 3, 7, 15, 31, 63, 127]
	for i in range(masks.size()):
		main.chapter2_cake_piece_mask = masks[i]
		var competition := OperaCompetition.new()
		competition.configure("chef")
		var world := WORLD_SCRIPT.new() as OperaCareerWorld2D
		main.add_child(world)
		world.setup(main, {"costume": "chef", "chapter": "chapter2",
			"phase_overrides": ChapterTwoCareerSceneAdapter.phase_set("chef").get("phases", []),
			"finale_start": 5, "chapter2_resume_phase_index": mini(i, 4)}, competition,
			Callable(), [], ChapterTwoCareerSceneAdapter.adapter_config("chef"),
			{"chapter": "chapter2"})
		await process_frame
		if OS.get_environment("CHEF_CAPTURE_BASELINE") == "1":
			world.backdrop_node.setup("chef")
			world.chapter2_cake_scene.set_kitchen_display_layout(false)
			world.chapter2_cake_scene.z_index = 4
		world.set_process(false)
		world.backdrop_node.set_process(false)
		world._place_on_stage(world.player_actor, Vector2(744, 425))
		world.player_animator.set_process(false)
		await process_frame
		await RenderingServer.frame_post_draw
		var image := get_root().get_texture().get_image()
		var path := out.path_join("mask_%02x.png" % masks[i])
		var error := image.save_png(path)
		print("CHEF_CAPTURE|", path, "|", image.get_size(), "|", error)
		world.free()
		await process_frame
	main.free()
	quit()