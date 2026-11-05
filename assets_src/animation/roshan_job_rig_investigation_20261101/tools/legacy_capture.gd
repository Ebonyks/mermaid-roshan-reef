extends SceneTree
## Same capture harness for the immutable v8 actor and the candidate actor.
var viewport: SubViewport
var actor: Node2D

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var destination: String = args[0]
	var candidate: bool = args[1] == "candidate"
	DirAccess.make_dir_recursive_absolute(destination)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1024,1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	actor = load("res://investigation.gd" if candidate else "res://study.gd").new()
	viewport.add_child(actor)
	actor.automatic = false
	actor.actor.position = Vector2.ZERO
	actor.actor.scale = Vector2.ONE
	for child: Node in actor.get_children():
		if child != actor.actor and child is CanvasItem:
			child.hide()
	var index: Array = []
	for head: String in ["original","ballet","magician"]:
		for body: String in ["original","ballet","magician"]:
			for tail: String in ["original","ballet","magician"]:
				actor.set_parts({"head":head,"body":body,"tail":tail})
				for clip: String in ["arm_bend","blink","tail_bend"]:
					var times: Array = [0.0,1.55,3.2] if clip=="arm_bend" else ([0.0,1.08,2.4] if clip=="blink" else [0.0,1.1,2.35,4.0])
					for t: float in times:
						if candidate:
							actor.set_regression(clip,t)
						else:
							actor.set_pose(clip,t)
						await process_frame
						await RenderingServer.frame_post_draw
						var name: String = "%s_%s_%s_%s_%04d.png" % [head,body,tail,clip,int(round(t*1000))]
						viewport.get_texture().get_image().save_png(destination.path_join(name))
						index.append({"file":name,"parts":{"head":head,"body":body,"tail":tail},"clip":clip,"time":t,"state":actor.state_record()})
	var file: FileAccess = FileAccess.open(destination.path_join("index.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(index,"\t")+"\n")
	print("LEGACY_CAPTURE_COMPLETE ",index.size())
	quit()
