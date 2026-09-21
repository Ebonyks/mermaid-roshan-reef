extends "res://scripts/probe_sky_lagoon_animals.gd"
func _frames(count: int) -> void:
	await super._frames(count)
	if main != null and main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
		await process_frame
		await process_frame
func _capture_pair(label: String, actor: Dictionary, definition: Dictionary) -> void:
	await super._capture_pair(label, actor, definition)
	var node: Sprite2D = actor["node"] as Sprite2D
	var saved: Dictionary = actor.duplicate()
	var texture: Texture2D = node.texture
	var region: Rect2 = node.region_rect
	var position: Vector2 = node.position
	var mode: Node.ProcessMode = main.process_mode
	var time: float = Engine.time_scale
	main.process_mode = Node.PROCESS_MODE_DISABLED
	Engine.time_scale = 0.0
	promenade._startle_animal(actor)
	for k: int in range(4):
		promenade._tick_animal_startle(actor, 0.10 if k == 0 else 0.20)
		_check("gpu_pose_%s_%d" % [label,k], _atlas_frame(node) == k)
		await process_frame
		await RenderingServer.frame_post_draw
		var path: String = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT").path_join(label+"_pose%d.png" % k)
		_check("gpu_capture_%s_%d" % [label,k], root.get_texture().get_image().save_png(path) == OK)
		var moved_position: Vector2 = node.position
		node.position = position
		promenade._sync_contact_shadow(node)
		await process_frame
		await RenderingServer.frame_post_draw
		path = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT").path_join(label+"_fixed_pose%d.png" % k)
		_check("gpu_fixed_contour_%s_%d" % [label,k], root.get_texture().get_image().save_png(path) == OK)
		node.position = moved_position
		promenade._sync_contact_shadow(node)

	actor.clear()
	actor.merge(saved)
	node.texture = texture
	node.region_rect = region
	node.position = position
	promenade._sync_contact_shadow(node)
	Engine.time_scale = time
	main.process_mode = mode
