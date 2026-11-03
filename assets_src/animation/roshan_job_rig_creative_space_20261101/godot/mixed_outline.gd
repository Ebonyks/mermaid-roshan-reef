extends SceneTree
func _initialize() -> void:
	run.call_deferred()
func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	var viewport: SubViewport = SubViewport.new()
	viewport.size = Vector2i(1024,1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	scene.automatic = false
	scene.actor.reparent(viewport)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var choices: Array[String] = ["original","ballet","magician","painter","astronaut"]
	var rows: Array = []
	for head: String in choices:
		for body: String in choices:
			for tail: String in choices:
				for clip: String in ["arm_bend","blink","tail_bend"]:
					scene.set_parts({"head":head,"body":body,"tail":tail})
					scene.set_pose(clip,1.5)
					await process_frame
					RenderingServer.force_draw(false)
					var name: String = "%s_%s_%s_%s.png" % [head,body,tail,clip]
					viewport.get_texture().get_image().save_png(out.path_join(name))
					rows.append({"head":head,"body":body,"tail":tail,"clip":clip,"time":1.5,"file":name})
		print("OUTLINE_HEAD ",head)
	var file: FileAccess = FileAccess.open(out.path_join("samples.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(rows))
	print("MIXED_OUTLINE_CAPTURE ",rows.size())
	quit()
