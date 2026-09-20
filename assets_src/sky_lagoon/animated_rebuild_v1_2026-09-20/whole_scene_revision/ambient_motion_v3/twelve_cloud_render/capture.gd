extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
func _capture(name: String) -> void:
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(1280,720)
	await process_frame
	await super._capture(name)
	if name not in ["canvas_screen_1_day","canvas_screen_2_day","canvas_screen_3_day","canvas_screen_3_night"]:
		return
	var running: bool = main.is_processing()
	main.set_process(false)
	var old_whole: float = float(main.g.get("lagoon_whole_t",0.0))
	var old_plant: float = float(main.g.get("lagoon_plant_cel_t",0.0))
	var views: int = 3 if main.is_night else 1
	var seen: Dictionary = {}
	for page: int in range(views):
		if main.is_night:
			promenade.set_master_route_x(float(page)*2048.0+1024.0)
			promenade._apply_view_transform(true)
		for i: int in range(64):
			main.g["lagoon_whole_t"] = (float(i)*.1 if i < 48 else float(i-48)*3.2)
			main.g["lagoon_plant_cel_t"] = (float(i)*.1 if i < 48 else float(i-48)*3.2)
			promenade.WholeSceneCels.tick(main.g,0.0,false)
			promenade.PlantCels.tick(main.g,0.0,false)
			for value: Variant in main.g["lagoon_whole_cards"]:
				var card: Sprite2D = value as Sprite2D
				if not seen.has(card.name):
					seen[card.name] = {}
				(seen[card.name] as Dictionary)[card.frame] = true
			await process_frame
			await RenderingServer.frame_post_draw
			_check("capture_"+name+"_%d_%02d"%[page,i],get_root().get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(name+"_%d_%02d.png"%[page,i]))==OK)
	for value: Variant in main.g["lagoon_whole_cards"]:
		var card: Sprite2D = value as Sprite2D
		var definition: Dictionary = card.get_meta("definition") as Dictionary
		_check("observed_cels_"+name+String(card.name),(seen[card.name] as Dictionary).size()==int(definition["frames"]))
	main.g["lagoon_whole_t"] = old_whole
	main.g["lagoon_plant_cel_t"] = old_plant
	promenade.WholeSceneCels.tick(main.g,0.0,false)
	promenade.PlantCels.tick(main.g,0.0,false)
	main.set_process(running)
