extends SceneTree
## Actual Mobile render capture, plus state/seek/transition stress. No gameplay saves.


func write_json(path: String, data: Variant) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(data))
	file.close()


func _initialize() -> void:
	run.call_deferred()


func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var out_dir: String = args[0] if args.size() > 0 else ProjectSettings.globalize_path("res://../evidence/render_v1")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.automatic = false
	var theme: String = args[1] if args.size() > 1 else "ballet"
	scene.set_parts({"head":theme,"body":theme,"tail":theme})
	var viewport: SubViewport = SubViewport.new()
	viewport.size = Vector2i(1024, 1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	scene.actor.reparent(viewport)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var samples: Array = []
	var clips: Array[String] = ["arm_bend", "blink", "tail_bend"]
	var total: int = 0
	for clip in clips:
		var folder: String = out_dir.path_join(clip)
		DirAccess.make_dir_recursive_absolute(folder)
		var length: float = scene.clip_length(clip)
		var count: int = int(round(length * 30.0))
		for i in range(count + 1):
			var t: float = minf(i / 30.0, length)
			scene.set_pose(clip, t)
			await process_frame
			RenderingServer.force_draw(false)
			var record: Dictionary = scene.state_record()
			record["clip"] = clip
			record["frame"] = i
			record["time"] = t
			samples.append(record)
			var picture: Image = viewport.get_texture().get_image()
			var error: Error = picture.save_png(folder.path_join("%04d.png" % i))
			if error != OK:
				push_error("PNG_SAVE_FAIL " + str(error))
				quit(2)
				return
			total += 1
		print("CAPTURE_OK ", clip, " frames=", count + 1)
	write_json(out_dir.path_join("samples.json"), samples)
	# Independent high-density sampling, variable-rate stepping and randomized seek order.
	var stress: Array = []
	var random: RandomNumberGenerator = RandomNumberGenerator.new()
	random.seed = 20261031
	var worst_repeat: float = 0.0
	var seeks: int = 0
	for cycle in range(120):
		var clip: String = clips[cycle % clips.size()]
		var length: float = scene.clip_length(clip)
		var rate: float = [15.0, 24.0, 30.0, 60.0, 120.0][cycle % 5]
		for i in range(int(ceil(length * rate)) + 1):
			var t: float = minf(i / rate, length)
			scene.set_pose(clip, t)
			var a: Dictionary = scene.state_record()
			var other: String = clips[(cycle + 1) % clips.size()]
			scene.set_pose(other, random.randf_range(0.0, scene.clip_length(other)))
			scene.set_pose(clip, t)
			var b: Dictionary = scene.state_record()
			if a.eyes_half != b.eyes_half or a.eyes_closed != b.eyes_closed:
				push_error("EYE_STATE_LEAK")
				quit(3)
				return
			for name in a.bones:
				for k in range(6):
					worst_repeat = maxf(worst_repeat, absf(float(a.bones[name][k]) - float(b.bones[name][k])))
			seeks += 3
			if cycle < 3 or cycle % 10 == 0:
				b["clip"] = clip
				b["time"] = t
				stress.append(b)
	write_json(out_dir.path_join("stress_samples.json"), stress)
	var summary: Dictionary = {
		"engine": Engine.get_version_info(),
		"rendering_method": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"frames_rendered": total,
		"cycles": 120,
		"state_seeks": seeks,
		"max_repeat_matrix_error": worst_repeat,
		"rates": [15, 24, 30, 60, 120],
		"device_claim": "desktop only; Lenovo/device/owner review pending"
	}
	write_json(out_dir.path_join("engine_receipt.json"), summary)
	print("STRESS_COMPLETE frames=", total, " seeks=", seeks, " repeat_error=", worst_repeat)
	quit(0 if worst_repeat < 0.00001 else 4)
