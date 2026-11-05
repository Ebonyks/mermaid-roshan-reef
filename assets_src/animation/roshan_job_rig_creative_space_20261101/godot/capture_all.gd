extends SceneTree
## Exact Mobile rendering. The production game and save system are never loaded.

var out: String
var viewport: SubViewport
var scene: Node2D
var failures: Array = []

func _initialize() -> void:
	run.call_deferred()

func save_json(path: String, value: Variant) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(value))

func capture() -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	return viewport.get_texture().get_image()

func setup_actor(instance: Node2D) -> void:
	instance.automatic = false
	instance.actor.reparent(viewport)
	instance.actor.position = Vector2.ZERO
	instance.actor.scale = Vector2.ONE

func run() -> void:
	out = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1024, 1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	scene = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	setup_actor(scene)
	var oracle: Node2D = load("res://seed.tscn").instantiate()
	root.add_child(oracle)
	await process_frame
	setup_actor(oracle)
	oracle.actor.visible = false
	var themes: Array[String] = ["original", "ballet", "magician", "painter", "astronaut"]
	var clips: Array[String] = ["arm_bend", "blink", "tail_bend"]
	var baseline_cases: int = 0
	var frames: int = 0
	for theme: String in themes:
		var folder: String = out.path_join(theme)
		DirAccess.make_dir_recursive_absolute(folder)
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		scene.set_pose("arm_bend",0.0)
		# Actual rest-rendered Body alpha, including the replacement's own contour.
		for mesh_name: String in scene.polygons:
			scene.polygons[mesh_name].visible = mesh_name == "Body"
		scene.helmet.visible = false
		var body_alpha: Image = await capture()
		body_alpha.save_png(folder.path_join("body_alpha.png"))
		if theme in ["painter", "astronaut"]:
			scene.polygons["Body"].visible = false
			scene.polygons["GarmentExtension"].visible = true
			var extension_alpha: Image = await capture()
			extension_alpha.save_png(folder.path_join("extension_alpha.png"))
		for mesh_name: String in scene.polygons:
			scene.polygons[mesh_name].visible = true
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		var samples: Array = []
		var theme_clips: Array[String] = clips.duplicate()
		if theme == "painter":
			theme_clips.append("paint_banner")
		if theme == "astronaut":
			theme_clips.append("turn_valve")
		for clip: String in theme_clips:
			DirAccess.make_dir_recursive_absolute(folder.path_join(clip))
			var length: float = scene.clip_length(clip)
			for index: int in range(int(round(length * 30.0)) + 1):
				var t: float = minf(index / 30.0, length)
				scene.set_pose(clip,t)
				var picture: Image = await capture()
				picture.save_png(folder.path_join(clip).path_join("%04d.png" % index))
				var row: Dictionary = scene.state_record()
				row.merge({"theme":theme,"clip":clip,"time":t,"frame":index,"socket":scene.socket_record()})
				samples.append(row)
				frames += 1
				if theme in ["original", "ballet", "magician"]:
					oracle.set_parts({"head":theme,"body":theme,"tail":theme})
					oracle.set_pose(clip,t)
					scene.actor.visible = false
					oracle.actor.visible = true
					var expected: Image = await capture()
					if picture.get_data() != expected.get_data():
						failures.append({"baseline_rgba":theme,"clip":clip,"frame":index})
					oracle.actor.visible = false
					scene.actor.visible = true
					baseline_cases += 1
			print("CAPTURE ",theme," ",clip)
		save_json(folder.path_join("samples.json"),samples)
		save_json(folder.path_join("stress_samples.json"),[])
	oracle.actor.queue_free()
	oracle.queue_free()
	# Every independent slot mixture compared with a newly constructed actor.
	var mix_cases: int = 0
	for head: String in themes:
		for body: String in themes:
			for tail: String in themes:
				var parts: Dictionary = {"head":head,"body":body,"tail":tail}
				var fresh: Node2D = load("res://study.tscn").instantiate()
				root.add_child(fresh)
				setup_actor(fresh)
				for clip: String in clips:
					fresh.set_parts(parts)
					fresh.set_pose(clip,1.5)
					scene.actor.visible = false
					fresh.actor.visible = true
					var expected: Image = await capture()
					fresh.actor.visible = false
					scene.actor.visible = true
					scene.set_parts({"head":"astronaut","body":"magician","tail":"original"})
					scene.set_pose("blink",1.08)
					scene.set_parts(parts)
					scene.set_pose(clip,1.5)
					var actual: Image = await capture()
					if expected.get_data() != actual.get_data():
						failures.append({"mix":parts,"clip":clip})
					mix_cases += 1
				fresh.actor.queue_free()
				fresh.queue_free()
		print("MIX_HEAD ",head)
	# Mid-pose swaps cannot change bone or eye state, allocate bones, or accumulate nodes.
	var before_ids: Array = []
	for name: String in scene.bones:
		before_ids.append(scene.bones[name].get_instance_id())
	var nodes: int = scene.actor.get_child_count()
	var swaps: int = 0
	var state_failures: int = 0
	var all_clips: Array[String] = ["arm_bend","blink","tail_bend","paint_banner","turn_valve"]
	for cycle: int in range(120):
		var clip: String = all_clips[cycle % all_clips.size()]
		var rate: float = [15.0,24.0,30.0,60.0,120.0][cycle % 5]
		for index: int in range(int(ceil(scene.clip_length(clip)*rate))+1):
			scene.set_pose(clip,minf(index/rate,scene.clip_length(clip)))
			var before: String = JSON.stringify(scene.state_record())
			scene.set_parts({"head":themes[(cycle+index)%5],"body":themes[(cycle+index/5)%5],"tail":themes[(cycle+index/25)%5]})
			if before != JSON.stringify(scene.state_record()):
				state_failures += 1
			swaps += 1
	var stable: bool = scene.actor.get_child_count() == nodes
	for i: int in range(before_ids.size()):
		stable = stable and scene.bones[scene.bones.keys()[i]].get_instance_id() == before_ids[i]
	var selected: Dictionary = scene.selected_parts.duplicate(true)
	var invalid: bool = not scene.set_parts({"body":"../../bad"}) and not scene.set_parts({"feet":"painter"}) and not scene.equip_catalog_ids({"body":"head_painter_v1"}) and selected == scene.selected_parts
	# Old source poison must not enter any replacement skin.
	var original: Texture2D = scene.original_body_texture
	var poison: Image = original.get_image()
	poison.fill(Color.GREEN)
	var poison_texture: ImageTexture = ImageTexture.create_from_image(poison)
	var controls: Dictionary = {}
	for theme: String in ["ballet","magician","painter","astronaut"]:
		scene.original_body_texture = original
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		scene.set_pose("arm_bend",1.5)
		var normal: Image = await capture()
		scene.original_body_texture = poison_texture
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		var poisoned: Image = await capture()
		controls[theme+"_source_poison_excluded"] = normal.get_data() == poisoned.get_data()
		scene.original_body_texture = original
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		scene.body.texture = original
		var underlay: Image = await capture()
		controls[theme+"_old_underlay_detected"] = normal.get_data() != underlay.get_data()
		underlay.save_png(out.path_join("negative_"+theme+"_old_underlay.png"))
	var report: Dictionary = {"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"adapter":RenderingServer.get_video_adapter_name(),"frames":frames,"seed_exact_rgba_cases":baseline_cases,"independent_mixes":125,"fresh_instance_pixel_cases":mix_cases,"live_swaps":swaps,"state_failures":state_failures,"stable_bone_nodes":stable,"invalid_ids_atomically_rejected":invalid,"negative_controls":controls,"failures":failures,"limits":"Desktop Mobile source prototype only. Numerical success does not establish natural motion, owner, device, child, runtime integration or master-audit acceptance."}
	var passed: bool = failures.is_empty() and state_failures == 0 and stable and invalid
	for value: bool in controls.values():
		passed = passed and value
	report["pass"] = passed
	save_json(out.path_join("native_audit.json"),report)
	print("NATIVE_AUDIT ",passed," frames=",frames," baseline=",baseline_cases," mixes=",mix_cases," swaps=",swaps)
	quit(0 if passed else 1)
