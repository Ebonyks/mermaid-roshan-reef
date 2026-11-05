extends SceneTree
## Capture actual Mobile-rendered RGBA, native bone telemetry and swap states.
var study: Node2D
var viewport: SubViewport
var destination: String


func _initialize() -> void:
	call_deferred("run")


func write_json(path: String, value: Variant) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(value, "\t") + "\n")


func snap(path: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	viewport.get_texture().get_image().save_png(path)


func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	destination = args[0]
	var full: bool = args.size() > 1 and args[1] == "full"
	DirAccess.make_dir_recursive_absolute(destination)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1024, 1024)
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
	await process_frame
	for job: String in ["detective", "geologist"]:
		study.set_job(job)
		var folder: String = destination.path_join(job)
		DirAccess.make_dir_recursive_absolute(folder)
		var records: Array = []
		for frame: int in range(193) if full else [0, 39, 69, 105, 135, 171, 192]:
			study.set_work_pose(frame / 30.0)
			await snap(folder.path_join("%04d.png" % frame))
			var record: Dictionary = study.job_record()
			record["frame"] = frame
			records.append(record)
		write_json(folder.path_join("samples.json"), records)
		for fault: String in ["grip_slip", "fixture_drift", "identity_scale", "original_underlay"]:
			study.fault = fault
			study.set_work_pose(2.3)
			await snap(folder.path_join("fault_" + fault + ".png"))
			write_json(folder.path_join("fault_" + fault + ".json"), study.job_record())
		study.fault = "none"
		study.set_parts({"head":job,"body":job,"tail":job})
		study.fixture.visible = false
		var samples: Array = []
		for clip: String in ["arm_bend", "blink", "tail_bend"]:
			DirAccess.make_dir_recursive_absolute(folder.path_join(clip))
			var count: int = int(round(study.clip_length(clip) * 30.0))
			for frame: int in range(count+1) if full else [0, int(count/2), count]:
				study.set_regression(clip, frame/30.0)
				await snap(folder.path_join(clip).path_join("%04d.png" % frame))
				var record: Dictionary = study.state_record()
				record.merge({"clip":clip,"time":frame/30.0,"frame":frame})
				samples.append(record)
		write_json(folder.path_join("samples_regression.json"), samples)
	# All125 combinations are rendered at rest and at the arm extreme; equality
	# alone is not a fit test. Every pair remains visible in the artifact packet.
	var mixes: Array = []
	DirAccess.make_dir_recursive_absolute(destination.path_join("mixes"))
	var themes: Array[String] = ["original","ballet","magician","detective","geologist"]
	for head: String in themes:
		if not full and head not in ["detective","geologist"]:
			continue
		for body: String in themes:
			if not full and body not in ["detective","geologist"]:
				continue
			for tail: String in themes:
				if not full and tail not in ["detective","geologist"]:
					continue
				study.set_parts({"head":head,"body":body,"tail":tail})
				for t: float in [0.0,1.55]:
					study.set_regression("arm_bend",t)
					var name: String = head+"_"+body+"_"+tail+"_"+("rest" if t==0.0 else "extreme")
					await snap(destination.path_join("mixes").path_join(name+".png"))
					mixes.append({"file":name+".png","parts":study.selected_parts.duplicate(),"time":t,"state":study.state_record()})
	write_json(destination.path_join("mixed_samples.json"),mixes)
	var live: Dictionary = {}
	study.set_parts({"head":"original","body":"original","tail":"original"})
	study.set_regression("arm_bend",1.55)
	await snap(destination.path_join("original_before_swaps.png"))
	var reference: Dictionary = study.state_record()
	var swaps: int = 0
	var drift: int = 0
	for iteration: int in range(52 if full else 1):
		for head: String in themes:
			for body: String in themes:
				for tail: String in themes:
					for slot: String in ["head","body","tail"]:
						study.set_parts({slot:{"head":head,"body":body,"tail":tail}[slot]})
						swaps += 1
						if study.state_record() != reference:
							drift += 1
	study.set_parts({"head":"original","body":"original","tail":"original"})
	study.set_regression("arm_bend",1.55)
	await snap(destination.path_join("original_after_swaps.png"))
	var prior: Dictionary = study.selected_parts.duplicate()
	live["invalid_atomic"] = not study.set_parts({"body":"not_a_costume"}) and study.selected_parts == prior
	live.merge({"swaps":swaps,"bone_or_eye_state_drift":drift,"floor":19248,"same_state_is_not_fit_evidence":true})
	write_json(destination.path_join("live_swaps.json"),live)
	write_json(destination.path_join("capture_environment.json"),{"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"adapter":RenderingServer.get_video_adapter_name(),"viewport":[1024,1024],"fps":30,"full":full,"source":"actual Godot SubViewport RGBA; no artwork composed by the capture runner"})
	print("NATIVE_CAPTURE_COMPLETE ",destination)
	quit()
