extends SceneTree
# Focused live-world audit for the Royal Bathroom. The GLB contract probe owns
# mesh/material budgets; this probe protects placement, the privy route, and
# the existing toilet interaction from later room-dressing regressions.

var main: ReefMain
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("BATHROOM_WORLD|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _collect_visible_canvas_layers(node: Node, result: Array[CanvasLayer]) -> void:
	if node is CanvasLayer:
		var layer: CanvasLayer = node as CanvasLayer
		if layer.visible:
			result.append(layer)
			layer.visible = false
	for child in node.get_children():
		_collect_visible_canvas_layers(child, result)

func _shot(name_value: String, position: Vector3, target: Vector3) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var hidden_layers: Array[CanvasLayer] = []
	_collect_visible_canvas_layers(root, hidden_layers)
	var camera: Camera3D = Camera3D.new()
	camera.fov = 68.0
	root.add_child(camera)
	camera.position = position
	camera.look_at(target, Vector3.UP)
	camera.current = true
	await process_frame
	await RenderingServer.frame_post_draw
	var qa_dir: String = ProjectSettings.globalize_path("res://assets_src/blender/qa_bathroom_props")
	DirAccess.make_dir_recursive_absolute(qa_dir)
	var output_path: String = qa_dir.path_join("in_game_" + name_value + ".png")
	var save_error: Error = root.get_viewport().get_texture().get_image().save_png(output_path)
	print("BATHROOM_WORLD|shot saved: ", output_path, " error=", save_error)
	camera.queue_free()
	for layer in hidden_layers:
		if is_instance_valid(layer):
			layer.visible = true

func _fixture_exists(name_value: String) -> bool:
	return main.find_child(name_value, true, false) != null

func _route_result(relative_target: Vector3) -> Dictionary:
	var player: Node3D = main.player as Node3D
	player.position = main.CASTLE_POS + relative_target
	player.set("vel", Vector3.ZERO)
	await _frames(24)
	var relative_actual: Vector3 = player.position - main.CASTLE_POS
	var holds: bool = (
		absf(relative_actual.x - relative_target.x) < 0.8
		and relative_actual.y >= -17.8
		and relative_actual.y <= -14.2
		and absf(relative_actual.z - relative_target.z) < 0.8
	)
	return {"holds": holds, "actual": relative_actual}

func _run() -> void:
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	await _frames(8)
	main._enter_level2()
	await _frames(18)
	main._enter_castle_interior()
	await _frames(24)

	_ck("bathtub instance", _fixture_exists("BathroomBathtub"))
	_ck("vanity instance", _fixture_exists("BathroomSink"))
	_ck("toilet instance", _fixture_exists("BathroomToilet"))
	var bath_route: Dictionary = await _route_result(Vector3(-22.0, -15.5, -28.0))
	_ck("floor-height route beside tub", bool(bath_route["holds"]), "actual=" + str(bath_route["actual"]))
	var privy_door: Dictionary = await _route_result(Vector3(-26.5, -15.5, -28.0))
	_ck("privy doorway return bubble clear", bool(privy_door["holds"]), "actual=" + str(privy_door["actual"]))

	_ck("toilet trigger exists", main.g.has("toilet"))
	if main.g.has("toilet"):
		var toilet_data: Dictionary = main.g["toilet"] as Dictionary
		var toilet_pos: Vector3 = toilet_data["pos"]
		var player: Node3D = main.player as Node3D
		toilet_data["armed"] = true
		player.position = toilet_pos + Vector3(1.5, 0.4, 0.0)
		player.set("vel", Vector3.ZERO)
		await _frames(30)
		_ck("toilet proximity interaction", not bool(toilet_data.get("armed", true)))

	await _shot(
		"bubble_bath_overview",
		main.CASTLE_POS + Vector3(-5.8, -8.5, -27.8),
		main.CASTLE_POS + Vector3(-18.5, -14.4, -27.5),
	)
	await _shot(
		"vanity_closeup",
		main.CASTLE_POS + Vector3(-8.8, -10.0, -29.6),
		main.CASTLE_POS + Vector3(-12.0, -14.0, -34.2),
	)
	await _shot(
		"royal_loo_closeup",
		main.CASTLE_POS + Vector3(-27.0, -12.0, -24.0),
		main.CASTLE_POS + Vector3(-32.0, -15.0, -28.0),
	)

	print("BATHROOM_WORLD|RESULT: ", checks_failed, (" FAIL" if checks_failed > 0 else " OK"))
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
