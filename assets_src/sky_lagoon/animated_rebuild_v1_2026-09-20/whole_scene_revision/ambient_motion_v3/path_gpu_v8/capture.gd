extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
const Whole := preload("res://scripts/arena/sky_lagoon_whole_scene_cels.gd")
func snap(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(label, root.get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(label + ".png")) == OK)
func _capture(name: String) -> void:
	await super._capture(name)
	if name not in ["canvas_screen_3_day", "canvas_screen_3_night"]:
		return
	var processing: bool = main.is_processing()
	var saved_time: float = Engine.time_scale
	var old_route: float = promenade.master_route_x()
	main.set_process(false)
	Engine.time_scale = 0.0
	promenade.set_master_route_x(5120.0)
	promenade._apply_view_transform(true)
	Whole.tick(main.g, 0.0, false)
	var bank: Sprite2D = null
	for value: Variant in main.g["lagoon_whole_cards"] as Array:
		var card: Sprite2D = value as Sprite2D
		if str((card.get_meta("definition") as Dictionary)["id"]) == "castle_approach_bank":
			bank = card
	_check("path_bank_rest_" + name, bank != null and bank.frame == 0)
	if bank != null:
		var holder: Node2D = main.g["lagoon_base_layer"] as Node2D
		var transform: Transform2D = holder.get_global_transform_with_canvas()
		var source: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/ambient_motion_v3/motion_quarantine_v7/path-RESULT.json")) as Dictionary
		var points: Array = []
		for point: Array in source["corridor_points_local"] as Array:
			var screen: Vector2 = transform * (Vector2(3970, 510) + Vector2(float(point[0]), float(point[1])))
			points.append([screen.x, screen.y])
		var evidence: Dictionary = {"screen_points": points, "width": transform.x.length() * 10.0, "texture": bank.texture.resource_path, "frame_count": bank.hframes * bank.vframes, "motion_enabled": (bank.get_meta("definition") as Dictionary).get("motion_enabled", true)}
		var file: FileAccess = FileAccess.open(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(name + "_geometry.json"), FileAccess.WRITE)
		file.store_string(JSON.stringify(evidence, "  "))
		await snap(name + "_rest")
		for k: int in range(1, 4):
			bank.frame = k
			await snap(name + "_retired%d" % k)
			Whole.tick(main.g, 0.0, false)
			_check("path_bank_reset_%s_%d" % [name, k], bank.frame == 0)
			await snap(name + "_restored%d" % k)
	promenade.set_master_route_x(old_route)
	promenade._apply_view_transform(true)
	Engine.time_scale = saved_time
	main.set_process(processing)
