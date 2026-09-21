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
	var snapshots: Array[Dictionary] = []
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tmp/sky-lagoon-whole-scene-v2/cloud-candidate-pack/PACKING.json"))
	for entry: Dictionary in manifest["entries"]:
		var card: Sprite2D = (main.g["lagoon_base_layer"] as Node2D).get_node("WholeScene_"+String(entry["id"])) as Sprite2D
		snapshots.append({"node":card,"texture":card.texture,"position":card.position,"scale":card.scale,"frame":card.frame,"h":card.hframes,"v":card.vframes,"cycle":float(entry["pose_cycle_seconds"])})
		card.texture = ImageTexture.create_from_image(Image.load_from_file("res://tmp/sky-lagoon-whole-scene-v2/cloud-candidate-pack/"+String(entry["atlas"])))
		card.hframes = 2
		card.vframes = 2
		card.scale /= float(entry["uniform_scale"])
		card.position += Vector2(float(entry["runtime_position_offset"][0]),float(entry["runtime_position_offset"][1]))-Vector2(2,2)*card.scale
		snapshots[-1]["trial_home"] = card.position
	var plants: Array = main.g["lagoon_plant_cels"]
	var old_textures: Array[Texture2D] = []
	var old_frames: Array[int] = []
	var leaf_atlas: Texture2D = ImageTexture.create_from_image(Image.load_from_file("res://tmp/sky-lagoon-whole-scene-v2/bellflower-whole-leaf/atlas.png"))
	for value: Variant in plants:
		var plant: Sprite2D = value as Sprite2D
		old_textures.append(plant.texture)
		old_frames.append(plant.frame)
		plant.texture = leaf_atlas
	var grass := Sprite2D.new()
	grass.centered = false
	grass.texture = ImageTexture.create_from_image(Image.load_from_file("res://tmp/sky-lagoon-whole-scene-v2/grass-pointed-trial/blade-layers/runtime-trial-atlas.png"))
	grass.hframes = 2
	grass.vframes = 2
	grass.z_index = 4
	var pack_scale: float = 252.0/426.0
	grass.scale = Vector2.ONE * 300.0/(1472.0*640.0/1537.0*pack_scale)
	grass.position = Vector2(800,2048)-(Vector2(798,917)*640.0/1537.0*pack_scale+Vector2(2,2))*grass.scale
	(main.g["lagoon_foreground_geography_layer"] as Node2D).add_child(grass)
	if main.is_night:
		grass.modulate = Color(.48,.56,.82)
	var views: int = 3 if main.is_night else 1
	for page: int in range(views):
		if main.is_night:
			promenade.set_master_route_x(float(page)*2048.0+1024.0)
			promenade._apply_view_transform(true)
		for i: int in range(24):
			var t: float = float(i)*.2
			for state: Dictionary in snapshots:
				var cloud: Sprite2D = state["node"] as Sprite2D
				cloud.frame = int(floor(fposmod(t,float(state["cycle"]))/float(state["cycle"])*3.0))
				cloud.position = (state["trial_home"] as Vector2)+Vector2(sin(t*TAU/48.0)*24.0,0)
			for value: Variant in plants:
				(value as Sprite2D).frame = promenade.PlantCels.frame_at(t)
			grass.frame = int(floor(fposmod(t,2.6)/.65))
			await process_frame
			await RenderingServer.frame_post_draw
			_check("capture_"+name+"_%d_%02d"%[page,i],get_root().get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(name+"_%d_%02d.png"%[page,i]))==OK)
	grass.free()
	for state: Dictionary in snapshots:
		var cloud: Sprite2D = state["node"] as Sprite2D
		cloud.frame = 0
		cloud.hframes = int(state["h"])
		cloud.vframes = int(state["v"])
		cloud.texture = state["texture"]
		cloud.scale = state["scale"]
		cloud.position = state["position"]
		cloud.frame = int(state["frame"])
		_check("cloud_restore_"+name+String(cloud.name),cloud.texture==state["texture"] and cloud.position==state["position"] and cloud.scale==state["scale"])
	for i: int in range(plants.size()):
		(plants[i] as Sprite2D).texture = old_textures[i]
		(plants[i] as Sprite2D).frame = old_frames[i]
	main.set_process(running)
