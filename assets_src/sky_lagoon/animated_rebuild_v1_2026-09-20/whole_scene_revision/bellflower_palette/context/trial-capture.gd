extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
func _capture(name: String) -> void:
	get_root().mode=Window.MODE_WINDOWED
	get_root().size=Vector2i(1280,720)
	await process_frame
	await super._capture(name)
	if name not in ["canvas_screen_1_day","canvas_screen_3_day","canvas_screen_3_night"]: return
	var running: bool = main.is_processing()
	main.set_process(false)
	var cards: Array = main.g["lagoon_plant_cels"] as Array
	var originals: Array[Texture2D] = []
	var old_frames: Array[int] = []
	var out: String = OS.get_environment("LIVING_CARD_SHOT_OUT")
	for v: Variant in cards:
		var c: Sprite2D = v as Sprite2D
		originals.append(c.texture);old_frames.append(c.frame);c.frame=0
	await RenderingServer.frame_post_draw
	get_root().get_texture().get_image().save_png(out.path_join(name+"-before.png"))
	var im: Image = Image.load_from_file("res://assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/bellflower_palette/bellflower-leaf-grade.png")
	var texture: ImageTexture = ImageTexture.create_from_image(im)
	for v: Variant in cards: (v as Sprite2D).texture=texture
	for pose: int in range(8):
		for v: Variant in cards: (v as Sprite2D).frame=pose
		await process_frame
		await RenderingServer.frame_post_draw
		_check("leaf_grade_capture_%s_%d"%[name,pose],get_root().get_texture().get_image().save_png(out.path_join(name+"-after-%d.png"%pose))==OK)
	for i: int in range(cards.size()):
		var c: Sprite2D=cards[i] as Sprite2D
		c.texture=originals[i];c.frame=old_frames[i]
	_check("leaf_grade_trial_restored_"+name,(cards[0] as Sprite2D).texture==originals[0] and (cards[1] as Sprite2D).texture==originals[1])
	main.set_process(running)
