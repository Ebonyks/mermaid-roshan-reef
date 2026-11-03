extends SceneTree
## Isolate each actual shaded mesh at rest; other meshes cannot pollute its mask.

func _initialize() -> void:
	run.call_deferred()


func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var folder: String = args[0]
	var themes: PackedStringArray = args[1].split(",")
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
	var rows: Array = []
	for theme: String in themes:
		if not bool(scene.call("set_parts", {"head":theme, "body":theme, "tail":theme})):
			quit(2)
			return
		motion.call("apply", scene, 0.0, "loop")
		var sub: String = folder.path_join(theme)
		DirAccess.make_dir_recursive_absolute(sub)
		var states: Dictionary = {}
		var polygons: Array[Polygon2D] = []
		for node: Node in actor.find_children("*", "CanvasItem", true, false):
			if node is Polygon2D or node is Sprite2D or node is Line2D:
				var item: CanvasItem = node as CanvasItem
				states[item] = item.visible
				if item is Polygon2D and item.is_visible_in_tree():
					polygons.append(item as Polygon2D)
		for polygon: Polygon2D in polygons:
			for item: CanvasItem in states:
				item.visible = false
			polygon.visible = true
			await process_frame
			RenderingServer.force_draw(false)
			viewport.get_texture().get_image().save_png(sub.path_join("surface_" + String(polygon.name) + ".png"))
		for item: CanvasItem in states:
			item.visible = bool(states[item])
		rows.append({"theme":theme,"meshes":polygons.size()})
	var output: FileAccess = FileAccess.open(folder.path_join("surfaces_receipt.json"),FileAccess.WRITE)
	output.store_string(JSON.stringify({"completed":true,"rows":rows,"renderer":RenderingServer.get_current_rendering_method(),"version":Engine.get_version_info(),"source_sha256":FileAccess.get_sha256("res://swim_source.gd"),"capture_sha256":FileAccess.get_sha256("res://capture_surfaces.gd")}))
	output.close()
	quit()
