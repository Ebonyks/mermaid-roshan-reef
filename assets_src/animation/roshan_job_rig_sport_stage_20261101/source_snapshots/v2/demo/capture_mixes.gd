extends SceneTree

func _initialize() -> void:
	run.call_deferred()

func snap(view: SubViewport) -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	await process_frame
	return view.get_texture().get_image()

func prepare(scene: Node2D,view: SubViewport) -> void:
	scene.run_action = false
	scene.actor.reparent(view)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE

func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	var packed: PackedScene = load("res://study.tscn")
	var scene: Node2D = packed.instantiate()
	root.add_child(scene)
	await process_frame
	var view: SubViewport = SubViewport.new()
	view.size = Vector2i(1024,1024)
	view.transparent_bg = true
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	prepare(scene,view)
	var other: SubViewport = SubViewport.new()
	other.size = Vector2i(1024,1024)
	other.transparent_bg = true
	other.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(other)
	var options: Array[String] = ["original","ballet","magician","boxer","racer","popstar"]
	var states: Array[Dictionary] = []
	for h: String in options:
		for b: String in options:
			for tail: String in options:
				states.append({"head":h,"body":b,"tail":tail})
	var records: Array = []
	var mismatches: int = 0
	var raw_mismatch: int = 0
	var pose_names: Array[String] = ["arm_bend","arm_bend","tail_bend"]
	var times: Array[float] = [0.0,1.6,2.35]
	for idx: int in range(states.size()):
		var fresh: Node2D = packed.instantiate()
		root.add_child(fresh)
		await process_frame
		prepare(fresh,other)
		fresh.set_parts(states[idx])
		scene.set_parts(states[idx])
		for k: int in range(3):
			var clip: String = pose_names[k]
			scene.action = clip
			fresh.action = clip
			scene.pose_action(clip,times[k])
			fresh.pose_action(clip,times[k])
			var a: Image = await snap(view)
			var b: Image = await snap(other)
			var equal: bool = a.get_data() == b.get_data()
			if not equal:
				mismatches += 1
			var path: String = "mix_%03d_%d.png" % [idx,k]
			a.save_png(out.path_join(path))
			records.append({"parts":states[idx],"image":path,"clip":clip,"time":times[k],"fresh_equal":equal,"bones":scene.state_record().bones})
		fresh.actor.free()
		fresh.free()
		if idx % 18 == 0:
			print("MIX_PROGRESS ",idx,"/",states.size())
	var worst: float = 0.0
	var swaps: int = 0
	var eye_leaks: int = 0
	for cycle: int in range(32):
		var clip: String = ["arm_bend","blink","tail_bend"][cycle%3]
		var t: float = fmod(float(cycle)*0.173,scene.clip_length(clip))
		for idx: int in range(states.size()):
			scene.set_parts(states[idx])
			scene.action = clip
			scene.pose_action(clip,t)
			var a: Dictionary = scene.state_record()
			scene.set_parts(states[(idx+73)%states.size()])
			scene.pose_action("blink",1.08)
			scene.set_parts(states[idx])
			scene.pose_action(clip,t)
			var b: Dictionary = scene.state_record()
			if a.eyes_half != b.eyes_half or a.eyes_closed != b.eyes_closed:
				eye_leaks += 1
			for name: String in a.bones:
				for j: int in range(6):
					worst = maxf(worst,absf(float(a.bones[name][j])-float(b.bones[name][j])))
			swaps += 3
	# A plain seed actor uses the original6902-vertex mesh and the exact old skin.
	var baseline: Node2D = Node2D.new()
	baseline.set_script(load("res://base.gd"))
	baseline.rig_source = "res://seed_rig_relocated.json"
	baseline.selected_parts = {"head":"original","body":"original","tail":"original"}
	root.add_child(baseline)
	await process_frame
	baseline.automatic = false
	baseline.actor.reparent(other)
	baseline.actor.position = Vector2.ZERO
	baseline.actor.scale = Vector2.ONE
	scene.set_parts({"head":"original","body":"original","tail":"original"})
	var original_restore_errors: int = 0
	for clip: String in ["arm_bend","blink","tail_bend"]:
		for t: float in [0.0,1.1,2.1]:
			scene.action = clip
			scene.pose_action(clip,t)
			baseline.set_pose(clip,t)
			var a: Image = await snap(view)
			var b: Image = await snap(other)
			if a.get_data()!=b.get_data():
				original_restore_errors += 1
	baseline.actor.free()
	baseline.free()
	var before: Dictionary = scene.selected_parts.duplicate(true)
	var rejected: bool = not scene.set_parts({"body":"retired_job","tail":"racer"})
	var atomic: bool = rejected and before == scene.selected_parts
	var file: FileAccess = FileAccess.open(out.path_join("samples.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"  "))
	file.close()
	file = FileAccess.open(out.path_join("switch_receipt.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"combinations":states.size(),"actual_fresh_instances":states.size(),"fresh_pixel_pairs":records.size(),"pixel_mismatches":mismatches,"live_swaps":swaps,"max_matrix_error":worst,"eye_state_leaks":eye_leaks,"original_seed_restore_comparisons":9,"original_seed_restore_errors":original_restore_errors,"invalid_binding_atomic":atomic,"switching_pass":mismatches==0 and worst<0.00001 and eye_leaks==0 and atomic and original_restore_errors==0,"limits":"State switching equality only. The independent per-mix outline/component/hole/waist/contact audit and exact visual review must also pass."},"  "))
	print("MIX_CAPTURE_COMPLETE ",records.size()," pairs; ",swaps," swaps; mismatches=",mismatches)
	quit(0 if mismatches==0 and worst<0.00001 and eye_leaks==0 and atomic and original_restore_errors==0 else 1)
