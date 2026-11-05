extends SceneTree

func _initialize() -> void:
	run.call_deferred()

func snap(view: SubViewport) -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	await process_frame
	return view.get_texture().get_image()

func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.run_action = false
	var view: SubViewport = SubViewport.new()
	view.size = Vector2i(1024,1024)
	view.transparent_bg = true
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	scene.actor.reparent(view)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var rows: Array = []
	var full: bool = OS.get_cmdline_user_args().size()>1 and OS.get_cmdline_user_args()[1]=="full"
	for theme: String in ["boxer","racer","popstar"]:
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		scene.action = theme
		var count: int = int(round(scene.duration(theme)*30.0))+1 if full else 5
		for i: int in range(count):
			var t: float = float(i)/30.0 if full else [0.0,1.5,3.2,5.2,8.0][i]
			scene.pose_action(theme,t)
			var img: Image = await snap(view)
			var path: String = theme+"_%04d.png" % i
			img.save_png(out.path_join(path))
			var row: Dictionary = scene.record()
			row["time"] = t
			row["image"] = path
			rows.append(row)
	var file: FileAccess = FileAccess.open(out.path_join("samples.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(rows,"  "))
	print("CAPTURE_COMPLETE ",rows.size())
	quit(0)
