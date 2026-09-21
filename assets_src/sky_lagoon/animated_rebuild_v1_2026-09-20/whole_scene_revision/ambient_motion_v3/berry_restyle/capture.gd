extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
func snap(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(label, root.get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(label + ".png")) == OK)
func _capture(name: String) -> void:
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(1280, 720)
	await process_frame
	await super._capture(name)
	if name not in ["canvas_screen_1_day", "canvas_screen_2_day", "canvas_screen_3_day", "canvas_screen_3_night"]:
		return
	var processing: bool = main.is_processing()
	var time_scale: float = Engine.time_scale
	main.set_process(false)
	Engine.time_scale = 0.0
	var plants: Array = main.g["lagoon_huckleberry_cels"] as Array
	var textures: Array[Texture2D] = []
	var frames: Array[int] = []
	var grids: Array[Vector2i] = []
	for value: Variant in plants:
		var card: Sprite2D = value as Sprite2D
		textures.append(card.texture)
		frames.append(card.frame)
		grids.append(Vector2i(card.hframes, card.vframes))
	var trial: Texture2D = ImageTexture.create_from_image(Image.load_from_file("res://assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/ambient_motion_v3/berry_restyle/eight-cel-atlas.png"))
	var original_clock: float = float(main.g.get("lagoon_huckleberry_cel_t", 0.0))
	var views: int = 3 if main.is_night else 1
	for page: int in range(views):
		if main.is_night:
			promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
			promenade._apply_view_transform(true)
		for i: int in range(plants.size()):
			var card: Sprite2D = plants[i] as Sprite2D
			card.texture = textures[i]
			card.hframes = grids[i].x
			card.vframes = grids[i].y
			card.frame = 0
		await snap(name + "_page%d_current" % page)
		for value: Variant in plants:
			var card: Sprite2D = value as Sprite2D
			card.frame = 0
			card.hframes = 4
			card.vframes = 2
			card.texture = trial
		var seen: Dictionary = {}
		for i: int in range(32):
			main.g["lagoon_huckleberry_cel_t"] = float(i) * 0.08
			promenade.HuckleberryCels.tick(main.g, 0.0, false)
			for value: Variant in plants:
				var plant: Sprite2D = value as Sprite2D
				if not seen.has(plant.name):
					seen[plant.name] = {}
				(seen[plant.name] as Dictionary)[plant.frame] = true
			await snap(name + "_page%d_motion_%02d" % [page, i])
		for value: Variant in plants:
			var plant: Sprite2D = value as Sprite2D
			_check("all_eight_" + name + String(plant.name), (seen[plant.name] as Dictionary).size() == 8)
	for i: int in range(plants.size()):
		var card: Sprite2D = plants[i] as Sprite2D
		card.texture = textures[i]
		card.hframes = grids[i].x
		card.vframes = grids[i].y
		card.frame = frames[i]
		_check("restored_" + name + String(card.name), card.texture == textures[i] and card.frame == frames[i] and card.hframes == grids[i].x and card.vframes == grids[i].y)
	main.g["lagoon_huckleberry_cel_t"] = original_clock
	Engine.time_scale = time_scale
	main.set_process(processing)
