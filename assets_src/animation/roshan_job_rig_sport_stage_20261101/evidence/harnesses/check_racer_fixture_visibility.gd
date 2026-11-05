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
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.run_action = false
	scene.set_process_input(false)
	var view: SubViewport = SubViewport.new()
	view.size = Vector2i(1024,1024)
	view.transparent_bg = true
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	scene.actor.reparent(view)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	scene.set_parts({"head":"racer","body":"racer","tail":"racer"})
	scene.action = "racer"
	scene.pose_action("racer",0.0)
	scene.support.visible = false
	scene.pose_action("racer",3.2)
	var hidden: Image = await snap(view)
	hidden.save_png(out.path_join("racer_fixture_hidden_by_harness.png"))
	scene.support.visible = true
	var restored: Image = await snap(view)
	restored.save_png(out.path_join("racer_fixture_restored_after_diagnostic.png"))
	var file: FileAccess = FileAccess.open(out.path_join("racer_fixture_visibility_state.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(scene.record(),"  "))
	print("FIXTURE_VISIBILITY_DIAGNOSTIC_COMPLETE")
	quit(0)
