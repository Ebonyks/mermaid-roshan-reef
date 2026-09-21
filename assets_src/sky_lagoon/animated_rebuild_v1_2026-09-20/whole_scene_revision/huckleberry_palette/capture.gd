extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
func snap(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(label,get_root().get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(label+".png"))==OK)
func _capture(name: String) -> void:
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(1280,720)
	await process_frame
	await super._capture(name)
	if name not in ["canvas_screen_1_day","canvas_screen_2_day","canvas_screen_3_day","canvas_screen_3_night"]:
		return
	var running: bool = main.is_processing()
	main.set_process(false)
	var plants: Array = main.g["lagoon_huckleberry_cels"]
	var originals: Array[Texture2D] = []
	var frames: Array[int] = []
	for value: Variant in plants:
		var plant: Sprite2D = value as Sprite2D
		originals.append(plant.texture)
		frames.append(plant.frame)
		plant.frame = 0
	await snap(name+"_original")
	var trial: Texture2D = ImageTexture.create_from_image(Image.load_from_file("res://tmp/sky-lagoon-whole-scene-v2/huckleberry-grade/atlas.png"))
	for value: Variant in plants:
		(value as Sprite2D).texture = trial
	for i: int in range(8):
		for value: Variant in plants:
			(value as Sprite2D).frame = i
		await snap(name+"_trial_%d"%i)
	if main.is_night:
		for page: int in range(2):
			promenade.set_master_route_x(float(page)*2048.0+1024.0)
			promenade._apply_view_transform(true)
			for index: int in range(plants.size()):
				(plants[index] as Sprite2D).texture = originals[index]
				(plants[index] as Sprite2D).frame = 0
			await snap("night_%d_original"%page)
			for value: Variant in plants:
				(value as Sprite2D).texture = trial
			await snap("night_%d_trial"%page)
	for index: int in range(plants.size()):
		var plant: Sprite2D = plants[index] as Sprite2D
		plant.texture = originals[index]
		plant.frame = frames[index]
		_check("restored_"+name+str(index),plant.texture==originals[index] and plant.frame==frames[index])
	main.set_process(running)
