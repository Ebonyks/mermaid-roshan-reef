extends SceneTree
const MAIN := preload("res://scenes/main.tscn")
const WORLD := preload("res://scripts/opera_career_world_2d.gd")
var main: ReefMain
func _init() -> void:
	call_deferred("_run")
func _run() -> void:
	main = MAIN.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.day_one_active = false
	main.start_menu_active = false
	main.start_menu_layer.visible = false
	main.clear_dialogue()
	main.hud_msg.visible = false
	main.set_process(false)
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_size(Vector2i(1280, 720))
	await process_frame
	var out := OS.get_environment("CHEF_CAPTURE_OUT")
	DirAccess.make_dir_recursive_absolute(out)
	var rows: Array[Dictionary] = []
	for career: String in ["candymaker", "doctor", "farmer", "magician", "painter", "astronaut", "popstar", "nursery"]:
		main.chapter2_active = false
		var competition := OperaCompetition.new()
		competition.configure(career)
		var world := WORLD.new() as OperaCareerWorld2D
		main.add_child(world)
		world.setup(main, {"costume": career}, competition, Callable(), [])
		await process_frame
		world.set_process(false)
		var captured := 0
		for phase_index in range(world.phases.size()):
			var phase := world.phases[phase_index] as Dictionary
			var mode := String(phase.get("mode", ""))
			if mode in ["bop", "lens", "talk"]:
				continue
			world.phase_index = phase_index
			world.task_open = false
			world._arm_phase()
			world.reveal_t = 0.0
			world.phase_gap = 0.0
			var station_index := int(world.station_for_phase.get(phase_index, -1))
			if station_index < 0:
				rows.append({"career": career, "phase": phase.get("name", ""), "status": "missing_station"})
				continue
			var feet: Vector2 = world.station_list[station_index].get("approach_pos", Vector2.ZERO)
			world.wander_feet = feet
			world._place_on_stage(world.player_actor, feet)
			world._open_task()
			world.surface.set_process(false)
			world.player_animator.set_process(false)
			world.backdrop_node.set_process(false)
			for frame in range(20):
				await process_frame
			rows.append({"career": career, "phase": phase.get("name", ""), "mode": mode,
				"panel": str(Rect2(world.action_panel.position, world.action_panel.size)),
				"actor_overlap": world.get_meta("activity_layout_actor_overlap", 0.0),
				"landmark_overlap": world.get_meta("activity_layout_context_overlap", 0.0)})
			if captured < 2:
				await RenderingServer.frame_post_draw
				get_root().get_texture().get_image().save_png(out.path_join("%s_%d.png" % [career, phase_index]))
				captured += 1
		world.free()
		await process_frame
	var file := FileAccess.open(out.path_join("LAYOUT_REVIEW.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"renderer": RenderingServer.get_current_rendering_method(), "viewport": str(get_root().size), "rows": rows}, "\t"))
	file.close()
	main.free()
	print("ACTIVITY_LAYOUT|COMPLETE|", rows.size(), " phases")
	quit()