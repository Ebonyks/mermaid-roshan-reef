extends SceneTree
func _initialize() -> void:
	run.call_deferred()
func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.automatic = false
	var viewport: SubViewport = SubViewport.new()
	viewport.size = Vector2i(1024,1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	scene.actor.reparent(viewport)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var rows: Array = []
	for theme: String in ["original","ballet","magician","painter","astronaut"]:
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		for clip: String in ["arm_bend","blink","tail_bend","paint_banner","turn_valve"]:
			for t: float in [0.0,1.5,2.0]:
				scene.set_pose(clip,t)
				await process_frame
				RenderingServer.force_draw(false)
				var file: String = "%s_%s_%03d.png" % [theme,clip,int(t*30)]
				viewport.get_texture().get_image().save_png(out.path_join(file))
				rows.append({"theme":theme,"clip":clip,"time":t,"file":file,"socket":scene.socket_record()})
	var f: FileAccess = FileAccess.open(out.path_join("samples.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify(rows))
	print("PRECHECK_CAPTURE ", rows.size())
	quit()
