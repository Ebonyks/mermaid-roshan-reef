extends "res://capture.gd"


func run() -> void:
	destination = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(destination)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1024,1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	study = load("res://investigation.gd").new()
	viewport.add_child(study)
	study.automatic = false
	study.actor.position = Vector2.ZERO
	study.actor.scale = Vector2.ONE
	for child: Node in study.get_children():
		if child != study.actor and child is CanvasItem:
			child.hide()
	var original: Texture2D = study.original_body_texture
	var image: Image = Image.create(1024,1024,false,Image.FORMAT_RGBA8)
	image.fill(Color.MAGENTA)
	var poison: Texture2D = ImageTexture.create_from_image(image)
	for job: String in ["detective","geologist"]:
		study.set_job(job)
		study.set_work_pose(2.3)
		await snap(destination.path_join(job+"_normal.png"))
		study.original_body_texture = poison
		study.set_parts({"head":job,"body":job,"tail":job})
		study.set_work_pose(2.3)
		await snap(destination.path_join(job+"_poison_old_source.png"))
		study.original_body_texture = original
		var underlay: Sprite2D = Sprite2D.new()
		underlay.texture = original
		underlay.centered = false
		underlay.z_index = -3
		study.actor.add_child(underlay)
		await snap(destination.path_join(job+"_reinsert_old_underlay.png"))
		underlay.queue_free()
		await process_frame
	print("SOURCE_CONTROLS_COMPLETE")
	quit()
