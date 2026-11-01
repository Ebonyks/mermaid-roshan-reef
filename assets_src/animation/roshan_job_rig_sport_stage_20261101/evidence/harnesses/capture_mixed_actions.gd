extends SceneTree

func _initialize() -> void:
	run.call_deferred()

func snap(view: SubViewport) -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	await process_frame
	return view.get_texture().get_image()

func hide_fixed(scene: Node2D) -> void:
	for item: CanvasItem in [scene.mitt,scene.wheel,scene.mic_lower,scene.mic_upper,scene.support]:
		item.visible = false

func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
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
	var rows: Array = []
	var names: Array[String] = ["original","ballet","magician","boxer","racer","popstar"]
	for action: String in ["boxer","racer","popstar"]:
		for body: String in names:
			for tail: String in names:
				scene.set_parts({"head":action,"body":body,"tail":tail})
				scene.action = action
				var prefix: String = action+"_"+body+"_"+tail
				scene.pose_action(action,0.0)
				hide_fixed(scene)
				var rest: Image = await snap(view)
				rest.save_png(out.path_join(prefix+"_rest_avatar.png"))
				scene.pose_action(action,3.2)
				var pic: Image = await snap(view)
				pic.save_png(out.path_join(prefix+"_contact.png"))
				var rec: Dictionary = scene.record()
				rec["parts"] = scene.selected_parts.duplicate(true)
				hide_fixed(scene)
				var avatar: Image = await snap(view)
				avatar.save_png(out.path_join(prefix+"_contact_avatar.png"))
				rec["rest_image"] = prefix+"_rest_avatar.png"
				rec["image"] = prefix+"_contact.png"
				rec["avatar_image"] = prefix+"_contact_avatar.png"
				rec["time"] = 3.2
				rows.append(rec)
	var file: FileAccess = FileAccess.open(out.path_join("samples.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(rows,"  "))
	print("MIXED_ACTION_CONTACT_COMPLETE ",rows.size())
	quit(0)
