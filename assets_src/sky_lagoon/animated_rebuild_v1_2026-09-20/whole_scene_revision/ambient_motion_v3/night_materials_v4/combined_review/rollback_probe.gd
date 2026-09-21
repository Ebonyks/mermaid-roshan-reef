extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
const Night = preload("res://scripts/arena/sky_lagoon_night_materials.gd")
func snap(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(label, root.get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(label + ".png")) == OK)
func _capture(name: String) -> void:
	await super._capture(name)
	if name == "canvas_screen_1_day":
		_check("day_has_no_night_material", not main.g.has("lagoon_night_leaf_material") and not main.g.has("lagoon_window_material_card"))
	if name != "canvas_screen_3_night":
		return
	var processing: bool = main.is_processing()
	var old_time: float = Engine.time_scale
	var route: float = promenade.master_route_x()
	main.set_process(false)
	Engine.time_scale = 0.0
	var actor: Sprite2D = main.g.get("lagoon_roshan_card") as Sprite2D
	var castle: Sprite2D = main.g.get("lagoon_castle_card") as Sprite2D
	var actor_material: Material = actor.material
	var actor_tint: Color = actor.modulate
	var castle_texture: Texture2D = castle.texture
	for page: int in range(3):
		promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
		promenade._apply_view_transform(true)
		_check("material_owner_count_%d" % page, (main.g.get("lagoon_night_leaf_cards", []) as Array).size() == 63)
		await snap("page%d_graded" % page)
		Night.clear(main.g)
		_check("clear_removes_ownership_%d" % page, not main.g.has("lagoon_night_leaf_cards") and not main.g.has("lagoon_window_material_card"))
		await snap("page%d_ungraded" % page)
		_check("rebuild_%d" % page, Night.build(main.g, true))
		_check("repeated_build_%d" % page, Night.build(main.g, true))
		var windows: int = 0
		for child: Node in castle.get_children():
			if child.name == "SkyLagoonCastleWindowMaterial":
				windows += 1
		_check("one_window_owner_%d" % page, windows == 1)
		_check("protected_actor_and_castle_unchanged_%d" % page, actor.material == actor_material and actor.modulate == actor_tint and castle.texture == castle_texture)
		await snap("page%d_rebuilt" % page)
	promenade.set_master_route_x(route)
	promenade._apply_view_transform(true)
	Engine.time_scale = old_time
	main.set_process(processing)
