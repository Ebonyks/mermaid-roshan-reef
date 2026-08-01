extends SceneTree

var main: ReefMain

func _settle(frames: int) -> void:
	for _frame_index in range(frames):
		await process_frame

func _save(name: String, out_dir: String) -> void:
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name))
	print("SWINGREVIEW|%s|%s" % [name, "OK" if error == OK else "FAIL"])

func _init() -> void:
	var out_dir: String = OS.get_environment("SWING_REVIEW_OUT")
	if out_dir.is_empty():
		out_dir = ProjectSettings.globalize_path("res://tmp/swing_review")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var packed: PackedScene = load("res://scenes/main.tscn")
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.intro_active:
		main._skip_intro()
	main._apply_quality("speedy")
	main._set_night(false)
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _settle(20)
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.touch_ui != null:
		main.touch_ui.visible = false
	if main.pause_layer != null:
		main.pause_layer.visible = false
	main.player.position.x = main.LEVEL2_POS.x + 3.0
	main.g["ss_walk_goal"] = null
	await _settle(50)
	var swing: Node3D = null
	for target_value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = target_value as Dictionary
		if String(target.get("id", "")) == "swing":
			swing = target.get("node") as Node3D
			break
	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	promenade._start_playground_animation("swing", swing)
	await _settle(25)
	await _save("swing_forward.png", out_dir)
	await _settle(51)
	await _save("swing_back.png", out_dir)
	quit()

