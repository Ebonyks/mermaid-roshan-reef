extends SceneTree
## Standalone native Mobile renderer; no game, input, save or gameplay events.

func _initialize() -> void:
	run.call_deferred()


func write_json(path: String, value: Variant) -> void:
	var output: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	output.store_string(JSON.stringify(value))
	output.close()


func record(scene: Node2D, t: float, index: int, clip: String) -> Dictionary:
	var result: Dictionary = {"time":t, "frame":index, "clip":clip, "bones":{}}
	var bones: Dictionary = scene.get("bones")
	for bone_name: String in bones:
		var transform: Transform2D = scene.call("stage_transform", bones[bone_name])
		result.bones[bone_name] = [transform.x.x, transform.x.y, transform.y.x, transform.y.y, transform.origin.x, transform.origin.y]
	var actor: Node2D = scene.get("actor")
	result["root"] = [actor.position.x, actor.position.y]
	result["eyes_half"] = scene.get("eye_half").visible
	result["eyes_closed"] = scene.get("eye_closed").visible
	return result


func meshes(scene: Node2D, folder: String) -> Array:
	var result: Array = []
	var actor: Node2D = scene.get("actor")
	var skeleton: Skeleton2D = scene.get("skeleton")
	for node: Node in actor.find_children("*", "Polygon2D", true, false):
		var polygon: Polygon2D = node as Polygon2D
		if not polygon.is_visible_in_tree():
			continue
		var vertices: Array = []
		for point: Vector2 in polygon.polygon:
			vertices.append([point.x, point.y])
		var triangles: Array = []
		for triangle: PackedInt32Array in polygon.polygons:
			triangles.append(Array(triangle))
		var weights: Dictionary = {}
		for index in range(polygon.get_bone_count()):
			var bone: Bone2D = skeleton.get_node(polygon.get_bone_path(index)) as Bone2D
			weights[String(bone.name)] = Array(polygon.get_bone_weights(index))
		if weights.is_empty():
			continue
		var texture_name: String = "mesh_" + String(polygon.name) + ".png"
		polygon.texture.get_image().save_png(folder.path_join(texture_name))
		result.append({"name":String(polygon.name), "vertices":vertices, "triangles":triangles, "weights":weights, "texture":texture_name})
	return result


func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var folder: String = args[0]
	var themes: PackedStringArray = args[1].split(",")
	var mode: String = args[2] if args.size() > 2 else "full"
	var motion: RefCounted = load("res://swim_motion.gd").new()
	var viewport: SubViewport = SubViewport.new()
	viewport.size = Vector2i(1024, 1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var scene: Node2D = load("res://swim_source.gd").new()
	root.add_child(scene)
	await process_frame
	scene.set("automatic", false)
	var actor: Node2D = scene.get("actor")
	actor.reparent(viewport)
	actor.position = Vector2.ZERO
	actor.scale = Vector2.ONE
	write_json(folder.path_join("runtime_rig.json"), scene.get("rig"))
	var complete: Array = []
	for theme: String in themes:
		if not bool(scene.call("set_parts", {"head":theme, "body":theme, "tail":theme})):
			push_error("COSTUME_NOT_BOUND " + theme)
			quit(2)
			return
		var theme_folder: String = folder.path_join(theme)
		DirAccess.make_dir_recursive_absolute(theme_folder)
		write_json(theme_folder.path_join("runtime_meshes.json"), meshes(scene, theme_folder))
		var samples: Array = []
		var counts: Dictionary = {}
		for clip: String in ["loop", "travel"]:
			var duration: float = 1.8 if clip == "loop" else 7.2
			var count: int = int(round(duration * 30.0)) + 1 if mode == "full" else 7
			var sub: String = theme_folder.path_join(clip)
			DirAccess.make_dir_recursive_absolute(sub)
			for index in range(count):
				var t: float = duration * index / float(count - 1)
				motion.call("apply", scene, t, clip)
				await process_frame
				RenderingServer.force_draw(false)
				var picture: Image = viewport.get_texture().get_image()
				picture.save_png(sub.path_join("%04d.png" % index))
				var sample: Dictionary = record(scene, t, index, clip)
				sample["phase"] = motion.call("phase", t, clip)
				samples.append(sample)
			counts[clip] = count
			print("SWIM_CAPTURE_OK ", theme, " ", clip, " ", count)
		write_json(theme_folder.path_join("samples.json"), samples)
		# Phase must survive costume changes and arbitrary seeks without resetting.
		var seeks: int = 0
		var maximum: float = 0.0
		for rate: float in [15.0, 24.0, 30.0, 60.0, 120.0]:
			for index in range(int(ceil(1.8 * rate)) + 1):
				var t: float = minf(index / rate, 1.8)
				motion.call("apply", scene, t, "loop")
				var first: Dictionary = record(scene, t, index, "loop")
				motion.call("apply", scene, 4.73, "travel")
				scene.call("set_parts", {"head":"original", "body":"original", "tail":"original"})
				scene.call("set_parts", {"head":theme, "body":theme, "tail":theme})
				motion.call("apply", scene, t, "loop")
				var again: Dictionary = record(scene, t, index, "loop")
				for bone_name: String in first.bones:
					for k in range(6):
						maximum = maxf(maximum, absf(float(first.bones[bone_name][k]) - float(again.bones[bone_name][k])))
				seeks += 3
		var receipt: Dictionary = {"theme":theme, "frames":counts, "seeks":seeks, "max_matrix_error":maximum, "pass":maximum < 0.00001}
		write_json(theme_folder.path_join("native_receipt.json"), receipt)
		complete.append(receipt)
	write_json(folder.path_join("engine.json"), {"version":Engine.get_version_info(), "renderer":RenderingServer.get_current_rendering_method(), "adapter":RenderingServer.get_video_adapter_name(), "mode":mode, "costumes":complete, "completed":true, "device":"desktop only", "input_hashes":{"capture.gd":FileAccess.get_sha256("res://capture.gd"), "swim_motion.gd":FileAccess.get_sha256("res://swim_motion.gd"), "swim_source.gd":FileAccess.get_sha256("res://swim_source.gd")}})
	quit()
