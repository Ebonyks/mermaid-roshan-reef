extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
const STUDY: String = "res://tmp/sky-lagoon-whole-scene-v2/grass-group-study/"
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
	var old_time_scale: float = Engine.time_scale
	var old_route_x: float = promenade.master_route_x()
	main.set_process(false)
	Engine.time_scale = 0.0
	var holder: Node2D = main.g["lagoon_base_layer"] as Node2D
	var old_children: int = holder.get_child_count()
	var cards: Array = main.g["lagoon_grass_groups"] as Array
	var saved_time: float = float(main.g["lagoon_grass_group_t"])
	var saved_frames: Array[int] = []
	for card: Sprite2D in cards:
		saved_frames.append(card.frame)
	var views: int = 3 if main.is_night else 1
	for page: int in range(views):
		if main.is_night:
			promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
			promenade._apply_view_transform(true)
		for card: Sprite2D in cards:
			card.visible = false
		await snap(name + "_page%d_current" % page)
		for card: Sprite2D in cards:
			card.visible = true
		var seen: Dictionary = {}
		for sample: int in range(32):
			var time: float = float(sample) * 0.05
			main.g["lagoon_grass_group_t"] = time
			preload("res://scripts/arena/sky_lagoon_grass_groups.gd").tick(main.g, 0.0, false)
			for card: Sprite2D in cards:
				if not seen.has(card.name):
					seen[card.name] = {}
				(seen[card.name] as Dictionary)[card.frame] = true
				_check("fixed_root_%s_%d" % [card.name, sample], (card.position + Vector2(128, 220) * card.scale).is_equal_approx(preload("res://scripts/arena/sky_lagoon_grass_groups.gd").GROUPS[cards.find(card)]["root"] as Vector2))
			await snap(name + "_page%d_motion_%02d" % [page, sample])
		for card: Sprite2D in cards:
			_check("all_four_%s_%s" % [name, card.name], (seen[card.name] as Dictionary).size() == 4)
	for i: int in range(cards.size()):
		(cards[i] as Sprite2D).frame = saved_frames[i]
	main.g["lagoon_grass_group_t"] = saved_time
	_check("grass_trial_nodes_removed_" + name, holder.get_child_count() == old_children)
	promenade.set_master_route_x(old_route_x)
	promenade._apply_view_transform(true)
	Engine.time_scale = old_time_scale
	main.set_process(processing)
