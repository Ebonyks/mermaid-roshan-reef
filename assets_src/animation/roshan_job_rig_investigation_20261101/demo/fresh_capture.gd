extends "res://capture.gd"
## Independent new actor for every outfit combination; shares no skin state.


func run() -> void:
	destination = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(destination)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1024,1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var themes: Array[String] = ["original","ballet","magician","detective","geologist"]
	for head: String in themes:
		for body: String in themes:
			for tail: String in themes:
				study = load("res://investigation.gd").new()
				viewport.add_child(study)
				study.automatic = false
				study.actor.position = Vector2.ZERO
				study.actor.scale = Vector2.ONE
				for child: Node in study.get_children():
					if child != study.actor and child is CanvasItem:
						child.hide()
				study.set_parts({"head":head,"body":body,"tail":tail})
				for t: float in [0.0,1.55]:
					study.set_regression("arm_bend",t)
					var name: String = head+"_"+body+"_"+tail+"_"+("rest" if t==0.0 else "extreme")
					await snap(destination.path_join(name+".png"))
				study.queue_free()
				await process_frame
	print("FRESH_CAPTURE_COMPLETE")
	quit()
