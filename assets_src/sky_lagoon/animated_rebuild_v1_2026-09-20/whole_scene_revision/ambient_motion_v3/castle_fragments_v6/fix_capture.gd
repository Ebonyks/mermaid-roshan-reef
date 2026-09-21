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
	main.set_process(false)
	Engine.time_scale = 0.0
	Whole.tick(main.g, 0.0, false)
	var fragments: Array[Sprite2D] = []
	for value: Variant in main.g["lagoon_whole_cards"] as Array:
		var card: Sprite2D = value as Sprite2D
		if str((card.get_meta("definition") as Dictionary)["id"]) in ["castle_left_verge", "castle_right_verge"]:
			fragments.append(card)
			_check("fragment_runtime_rest_" + card.name, card.frame == 0)
	_check("two_fragment_owners", fragments.size() == 2)
	await snap(name + "_rest")
	for k: int in range(1, 4):
		for card: Sprite2D in fragments:
			card.frame = k
		await snap(name + "_historical_fragment_pose%d" % k)
		Whole.tick(main.g, 0.0, false)
		for card: Sprite2D in fragments:
			_check("fragment_restored_" + card.name, card.frame == 0)
		await snap(name + "_restored%d" % k)
	Engine.time_scale = saved_time
	main.set_process(processing)
