extends RefCounted
## Read-only visible-tree resource references at native visual-probe capture points.
## Occlusion, clipping, offscreen position and custom draw pixels still need visual review.

static func describe_texture(texture: Texture2D) -> Dictionary:
	var row: Dictionary = {"class": texture.get_class(), "path": texture.resource_path,
		"dimensions": [texture.get_width(), texture.get_height()]}
	if texture is AtlasTexture:
		var atlas: AtlasTexture = texture as AtlasTexture
		row["region"] = [atlas.region.position.x, atlas.region.position.y,
			atlas.region.size.x, atlas.region.size.y]
		if atlas.atlas != null:
			row["atlas"] = describe_texture(atlas.atlas)
	if texture.resource_path.begins_with("res://") and FileAccess.file_exists(texture.resource_path):
		row["sha256"] = FileAccess.get_sha256(texture.resource_path)
	return row

static func trace(root_node: Node) -> Array[Dictionary]:
	var rows: Array[Dictionary] = []
	var pending: Array[Node] = [root_node]
	while not pending.is_empty():
		var node: Node = pending.pop_back()
		for child: Node in node.get_children():
			pending.append(child)
		if not node is CanvasItem:
			continue
		var canvas: CanvasItem = node as CanvasItem
		if not canvas.is_visible_in_tree():
			continue
		var script: Script = node.get_script() as Script
		var row: Dictionary = {"node": str(node.get_path()), "class": node.get_class(),
			"script": script.resource_path if script != null else "",
			"z_index": canvas.z_index, "modulate_alpha": canvas.modulate.a,
			"self_modulate_alpha": canvas.self_modulate.a, "textures": [],
			"observation": "Visible in tree only; clipping/occlusion/offscreen/custom-draw interpretation needs review"}
		var references: Array[Dictionary] = []
		for prop: Dictionary in node.get_property_list():
			var key: String = str(prop.get("name", ""))
			if key not in ["texture", "texture_normal", "texture_pressed", "texture_hover",
				"texture_disabled", "texture_focused", "texture_progress", "texture_under", "texture_over"]:
				continue
			var texture: Texture2D = node.get(key) as Texture2D
			if texture != null:
				references.append({"property": key, "reference": describe_texture(texture),
					"qualification": "Referenced visible-node texture property; button/state selection is not independently inferred"})
		if canvas.material is ShaderMaterial:
			var material: ShaderMaterial = canvas.material as ShaderMaterial
			for prop: Dictionary in material.get_property_list():
				var key: String = str(prop.get("name", ""))
				if not key.begins_with("shader_parameter/"):
					continue
				var value: Variant = material.get(key)
				if value is Texture2D:
					var texture: Texture2D = value as Texture2D
					references.append({"property": key, "reference": describe_texture(texture),
						"qualification": "Shader input; technical source is not standalone displayed artwork"})
		if node is Control:
			var control: Control = node as Control
			var rectangle: Rect2 = control.get_global_rect()
			row["global_rect"] = [rectangle.position.x, rectangle.position.y, rectangle.size.x, rectangle.size.y]
			row["rect_intersects_viewport"] = rectangle.intersects(control.get_viewport_rect())
			row["clip_contents"] = control.clip_contents
		elif node is Sprite2D:
			var sprite: Sprite2D = node as Sprite2D
			var rectangle: Rect2 = sprite.get_global_transform_with_canvas() * sprite.get_rect()
			row["canvas_rect"] = [rectangle.position.x, rectangle.position.y, rectangle.size.x, rectangle.size.y]
			row["rect_intersects_viewport"] = rectangle.intersects(sprite.get_viewport_rect())
		row["textures"] = references
		if not references.is_empty() or script != null:
			rows.append(row)
	return rows

static func save_frame_receipt(root_node: Window, name: String, output: String, harness: String,
		base_probe: String) -> void:
	var image: Image = root_node.get_texture().get_image()
	var picture: String = output.path_join(name + ".webp")
	assert(not image.is_empty() and image.save_webp(picture, false) == OK)
	var receipt: Dictionary = {"capture": name, "native_image": picture,
		"image_sha256": FileAccess.get_sha256(picture),
		"dimensions": [image.get_width(), image.get_height()],
		"engine": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(),
		"harness": harness, "harness_sha256": FileAccess.get_sha256(harness),
		"base_probe": base_probe, "base_probe_sha256": FileAccess.get_sha256(base_probe),
		"tracer_sha256": FileAccess.get_sha256("res://tools/job_art_scene_trace.gd"),
		"main_sha256": FileAccess.get_sha256("res://scripts/main.gd"),
		"references": trace(root_node), "source_score": null, "mounted_score": null, "action_score": null,
		"qualification": "Native visual-probe scene at a named forced setup/gesture capture point. A visible-tree resource reference is evidence to inspect, not proof of every pixel or whole ordinary route. Scores require individual visual review; phone/child/owner/full coverage are pending."}
	var file := FileAccess.open(output.path_join(name + ".json"), FileAccess.WRITE)
	assert(file != null)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
