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
	var a: Node2D = load("res://study.tscn").instantiate()
	root.add_child(a)
	await process_frame
	a.run_action = false
	a.set_process_input(false)
	var b: Node2D = Node2D.new()
	b.set_script(load("res://base.gd"))
	b.rig_source = "res://seed_rig_relocated.json"
	b.selected_parts = {"head":"original","body":"original","tail":"original"}
	root.add_child(b)
	await process_frame
	b.automatic = false
	b.set_process_input(false)
	var views: Array[SubViewport] = []
	for item: Node2D in [a,b]:
		var v: SubViewport = SubViewport.new()
		v.size = Vector2i(1024,1024)
		v.transparent_bg = true
		v.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(v)
		item.actor.reparent(v)
		item.actor.position = Vector2.ZERO
		item.actor.scale = Vector2.ONE
		views.append(v)
	a.set_parts({"head":"original","body":"original","tail":"original"})
	a.action = "arm_bend"
	a.pose_action("arm_bend",0.0)
	b.set_pose("arm_bend",0.0)
	var aa: Image = await snap(views[0])
	var bb: Image = await snap(views[1])
	aa.save_png(out.path_join("candidate.png"))
	bb.save_png(out.path_join("plain_seed.png"))
	var report: Dictionary = {"candidate_parts":a.selected_parts,"seed_parts":b.selected_parts,"candidate_vertices":a.body.polygon.size(),"seed_vertices":b.body.polygon.size(),"candidate_body_material":str(a.body.material),"seed_body_material":str(b.body.material),"candidate_state":a.state_record(),"seed_state":b.state_record()}
	var f: FileAccess = FileAccess.open(out.path_join("state.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify(report,"  "))
	print("ORIGINAL_DIAGNOSTIC_COMPLETE")
	quit(0)
