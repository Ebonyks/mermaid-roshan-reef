extends SceneTree

func snap(scene: Node2D, viewport: SubViewport, parts: Dictionary, clip: String, time: float) -> Image:
	scene.set_parts(parts)
	scene.set_pose(clip, time)
	await process_frame
	RenderingServer.force_draw(false)
	return viewport.get_texture().get_image()

func equal_state(a: Dictionary, b: Dictionary) -> bool:
	return JSON.stringify(a) == JSON.stringify(b)

func _initialize() -> void:
	run.call_deferred()

func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var out: String = args[0]
	DirAccess.make_dir_recursive_absolute(out)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.automatic = false
	var viewport: SubViewport = SubViewport.new()
	viewport.size = Vector2i(1024, 1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	scene.actor.reparent(viewport)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var bone_ids: Array = []
	for name: String in scene.bones:
		bone_ids.append(scene.bones[name].get_instance_id())
	var child_count: int = scene.actor.get_child_count()
	var material_id: int = scene.clothing_material.get_instance_id()
	var choices: Array[String] = ["original", "ballet", "magician"]
	var clips: Array[String] = ["arm_bend", "blink", "tail_bend"]
	var cases: Array = []
	var failures: Array = []
	var checked: int = 0
	# Every mixed outfit gets independent fresh-instance rendering as its pixel oracle.
	for head: String in choices:
		for body: String in choices:
			for tail: String in choices:
				var parts: Dictionary = {"head":head, "body":body, "tail":tail}
				for clip: String in clips:
					for time: float in [0.0, 1.08, 1.5]:
						var fresh: Node2D = load("res://study.tscn").instantiate()
						root.add_child(fresh)
						fresh.automatic = false
						fresh.actor.reparent(viewport)
						fresh.actor.position = Vector2.ZERO
						fresh.actor.scale = Vector2.ONE
						scene.actor.visible = false
						var reference: Image = await snap(fresh, viewport, parts, clip, time)
						fresh.actor.visible = false
						scene.actor.visible = true
						scene.set_parts({"head":"magician", "body":"ballet", "tail":"original"})
						scene.set_pose("blink", 1.08)
						var actual: Image = await snap(scene, viewport, parts, clip, time)
						var exact: bool = reference.get_data() == actual.get_data()
						if not exact:
							failures.append({"parts":parts,"clip":clip,"time":time})
						if time == 1.5:
							actual.save_png(out.path_join("%s_%s_%s_%s.png" % [head,body,tail,clip]))
						cases.append({"parts":parts,"clip":clip,"time":time,"rgba_exact":exact})
						checked += 1
						fresh.actor.queue_free()
						fresh.queue_free()
	var swaps: int = 0
	var worst: float = 0.0
	for cycle: int in range(120):
		var clip: String = clips[cycle % 3]
		var rate: float = [15.0, 24.0, 30.0, 60.0, 120.0][cycle % 5]
		var length: float = scene.clip_length(clip)
		for i: int in range(int(ceil(length * rate)) + 1):
			var time: float = minf(i / rate, length)
			scene.set_pose(clip, time)
			var before: Dictionary = scene.state_record()
			var parts: Dictionary = {"head":choices[(cycle+i)%3], "body":choices[(cycle+i/3)%3], "tail":choices[(cycle+i/9)%3]}
			scene.set_parts(parts)
			var after: Dictionary = scene.state_record()
			for name: String in before.bones:
				for k: int in range(6):
					worst = maxf(worst, absf(float(before.bones[name][k])-float(after.bones[name][k])))
			if before.eyes_half != after.eyes_half or before.eyes_closed != after.eyes_closed:
				failures.append("SWAP_CHANGED_EYES")
			swaps += 1
	var before_invalid: Dictionary = scene.selected_parts.duplicate(true)
	var invalid_rejected: bool = not scene.set_parts({"body":"../../bad"}) and not scene.set_parts({"feet":"ballet"}) and not scene.equip_catalog_ids({"body":"head_ballet_v1"})
	invalid_rejected = invalid_rejected and equal_state(before_invalid,scene.selected_parts)
	var stable: bool = scene.actor.get_child_count() == child_count and scene.clothing_material.get_instance_id() == material_id and scene.garment_textures.size() == 11
	for index: int in range(bone_ids.size()):
		stable = stable and scene.bones[scene.bones.keys()[index]].get_instance_id() == bone_ids[index]
	var catalog_ok: bool = true
	for theme: String in ["ballet", "magician"]:
		catalog_ok = catalog_ok and scene.equip_catalog_ids({"head":"head_"+theme+"_v1", "body":"body_"+theme+"_v1", "tail":"tail_"+theme+"_v1"}) and scene.selected_parts == {"head":theme,"body":theme,"tail":theme}
	catalog_ok = catalog_ok and scene.equip_catalog_ids({"head":"head_original","body":"roshan_original","tail":"tail_original"})
	var fault_reference: Image = await snap(scene, viewport, {"head":"ballet","body":"ballet","tail":"ballet"}, "arm_bend", 1.5)
	scene.clothing_material.set_shader_parameter("body_paint", scene.garment_textures["magician_body"])
	await process_frame
	RenderingServer.force_draw(false)
	var stale_body_detected: bool = viewport.get_texture().get_image().get_data() != fault_reference.get_data()
	scene.set_parts({"head":"ballet","body":"ballet","tail":"ballet"})
	scene.polygons["Headwear"].texture = scene.garment_textures["magician_head"]
	await process_frame
	RenderingServer.force_draw(false)
	var stale_head_detected: bool = viewport.get_texture().get_image().get_data() != fault_reference.get_data()
	scene.set_parts({"head":"ballet","body":"ballet","tail":"ballet"})
	var pass_all: bool = failures.is_empty() and worst < 0.00001 and stable and invalid_rejected and catalog_ok and stale_body_detected and stale_head_detected
	var record: Dictionary = {"pass":pass_all,"negative_controls":{"stale_body_uniform_detected":stale_body_detected,"stale_head_texture_detected":stale_head_detected},"engine":Engine.get_version_info(),"pixel_cases":checked,"all_27_mixes":true,"fresh_instance_rgba_cases":cases,"swaps":swaps,"cycles":120,"rates":[15,24,30,60,120],"max_swap_matrix_error":worst,"stable_bone_node_material_and_texture_counts":stable,"invalid_ids_atomically_rejected":invalid_rejected,"existing_catalog_ids_bound":catalog_ok,"failures":failures,"limits":"Desktop Mobile only. Snapshot equality does not accept mixed-costume artistic combinations, arbitrary new costumes, blends, device/child/owner performance."}
	var file: FileAccess = FileAccess.open(out.path_join("swap_audit.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(record))
	file.close()
	print("SWAP_AUDIT ",pass_all," pixels=",checked," swaps=",swaps," matrix_error=",worst)
	quit(0 if pass_all else 1)
