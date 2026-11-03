extends SceneTree
## Actual Godot Mobile frames and full source-space bone telemetry.
var viewport: SubViewport
var study: Node2D


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var destination: String = args[0]
	DirAccess.make_dir_recursive_absolute(destination)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1280, 720)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	study = load("res://motion.gd").new()
	viewport.add_child(study)
	study.automatic = false
	await process_frame
	DirAccess.make_dir_recursive_absolute(destination.path_join("rgba"))
	var samples: Array = []
	for frame: int in range(331):
		var t: float = frame / 30.0
		study.set_sequence_time(t)
		await process_frame
		await RenderingServer.frame_post_draw
		viewport.get_texture().get_image().save_png(destination.path_join("%04d.png" % frame))
		for child: Node in study.get_children():
			if child != study.actor and child is CanvasItem:
				child.hide()
		await process_frame
		await RenderingServer.frame_post_draw
		viewport.get_texture().get_image().save_png(destination.path_join("rgba").path_join("%04d.png" % frame))
		for child: Node in study.get_children():
			if child != study.actor and child is CanvasItem:
				child.show()
		var record: Dictionary = study.state_record()
		record.merge({"frame":frame, "time":t, "pose":study.sequence_pose(t), "actor_scale":[study.actor.scale.x,study.actor.scale.y]})
		samples.append(record)
	var file: FileAccess = FileAccess.open(destination.path_join("samples.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(samples) + "\n")
	var environment: FileAccess = FileAccess.open(destination.path_join("environment.json"), FileAccess.WRITE)
	environment.store_string(JSON.stringify({"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"adapter":RenderingServer.get_video_adapter_name(),"frames":331,"fps":30,"viewport":[1280,720],"lane":"source-only current-rig study","facing_turn_coverage":"missing: route reversal shown"},"\t") + "\n")
	print("LAURA_STUDY_CAPTURE_COMPLETE frames=331")
	quit()
