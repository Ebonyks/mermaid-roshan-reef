extends SceneTree
# Export source-owned static environment cards in native master coordinates.
var main: ReefMain
var rows: Array[Dictionary] = []
var output: String
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	output = OS.get_environment("SKY_MASTER_EXPORT")
	if output.is_empty():
		push_error("SKY_MASTER_EXPORT must name a review directory")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(output.path_join("cells"))
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	for frame: int in range(4):
		await process_frame
	if main.intro_active:
		main._skip_intro()
	main.day_one_active = false
	main._day_one_ref().clear_day_one_routing()
	main.is_night = false
	main.save_data["lagoon_plane_departed"] = true
	main.g["lagoon_art_version"] = "animated_v1"
	main._enter_level2_now(false, false, false)
	main.set_process(false)
	var space: Node2D = main.g["lagoon_master_space"] as Node2D
	collect(space, space, 0, Color.WHITE, false)
	var file: FileAccess = FileAccess.open(output.path_join("scene-layers.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"canvas": [6144, 2048], "scope": "editable day/rest environment; gameplay actors, cues, particles and shaders excluded", "layers": rows}, "\t"))
	print("SKYMASTER|source_owned_cards|%d" % rows.size())
	quit(0)
func collect(node: Node, space: Node2D, parent_z: int, parent_tint: Color, excluded: bool) -> void:
	var tint: Color = parent_tint
	var z: int = parent_z
	if node is CanvasItem:
		var item: CanvasItem = node as CanvasItem
		tint *= item.modulate
		z = parent_z + item.z_index if item.z_as_relative else item.z_index
	var label: String = String(node.name)
	var skip: bool = excluded or label.contains("Roshan") or label.contains("Animal") or label.contains("Focus") or label.contains("Highlight") or label.contains("WaterTap") or label.contains("Firefly")
	if node is Sprite2D and not skip:
		var card: Sprite2D = node as Sprite2D
		if card.texture != null and card.texture.resource_path.begins_with("res://"):
			var image: Image = card.texture.get_image()
			if image != null:
				if image.is_compressed():
					image.decompress()
				var region: Rect2i = Rect2i(card.region_rect) if card.region_enabled else Rect2i(Vector2i.ZERO, Vector2i(image.get_size() / Vector2i(card.hframes, card.vframes)))
				image = image.get_region(region)
				if card.flip_h:
					image.flip_x()
				if card.flip_v:
					image.flip_y()
				var filename: String = "cells/%03d.png" % rows.size()
				image.save_png(output.path_join(filename))
				var transform: Transform2D = space.global_transform.affine_inverse() * card.global_transform
				var origin: Vector2 = transform * card.get_rect().position
				var colour: Color = tint * card.self_modulate
				rows.append({"name": label, "source": card.texture.resource_path.trim_prefix("res://"), "source_sha256": FileAccess.get_sha256(card.texture.resource_path), "cell": filename, "region": [region.position.x, region.position.y, region.size.x, region.size.y], "transform": [transform.x.x, transform.y.x, origin.x, transform.x.y, transform.y.y, origin.y], "z": z, "order": rows.size(), "tint": [colour.r, colour.g, colour.b, colour.a], "visible": card.is_visible_in_tree(), "role": String(card.get_meta("canvas_layer_role", ""))})
	for child: Node in node.get_children():
		collect(child, space, z, tint, skip)
