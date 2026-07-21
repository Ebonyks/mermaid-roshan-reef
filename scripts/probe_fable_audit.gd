extends SceneTree
# Mobile-renderer audit captures for the Fable kit (R-GOV4 / R-QA4 / R-QA5 /
# R-REP1): child-height near/mid/far views, dense field stress, station
# approach/boarding, ride POV, castle-return context. Run with
# --rendering-method mobile at 1280x720. Prints FAUD|... lines.

const OUT := "res://audit/fable_kit_mobile"

var main: ReefMain = null
var camera: Camera3D = null


func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame


func _shot(name: String, position: Vector3, target: Vector3, fov: float = 62.0) -> void:
	camera.fov = fov
	camera.position = position
	camera.look_at(target, Vector3.UP)
	camera.make_current()
	await _frames(6)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var err: Error = image.save_png(OUT + "/" + name + ".png")
	print("FAUD|", name, "|", error_string(err))


func _init() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	print("FAUD|renderer|", RenderingServer.get_current_rendering_method())
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(4)
	for layer_value: Variant in [main.hud_layer, main.speech_layer,
		main.collection_button_layer, main.touch_ui, main.pause_layer]:
		if layer_value is CanvasItem:
			(layer_value as CanvasItem).visible = false
		elif layer_value is CanvasLayer:
			(layer_value as CanvasLayer).visible = false
	camera = Camera3D.new()
	get_root().add_child(camera)
	# ---- reef flora: child-height near / mid / far over the kelp meadow,
	# ---- dense-field stress pan, and mixed floor with old + new families
	var kp: Vector3 = main._district_ref().scatter_point("kelp")
	kp.y = main.seabed_h(kp.x, kp.z) if main.has_method("seabed_h") else kp.y
	await _shot("kelp_near", kp + Vector3(4, 2.2, 4), kp + Vector3(0, 2.2, 0), 62.0)
	await _shot("kelp_mid", kp + Vector3(12, 3.0, 12), kp + Vector3(0, 2, 0), 62.0)
	await _shot("kelp_far", kp + Vector3(30, 6.0, 30), kp + Vector3(0, 2, 0), 62.0)
	await _shot("kelp_field_oblique", kp + Vector3(-16, 2.4, 6), kp + Vector3(10, 2, -8), 70.0)
	var mp: Vector3 = main._district_ref().scatter_point("mixed")
	await _shot("coral_near", mp + Vector3(4, 2.2, -4), mp + Vector3(0, 1.2, 0), 62.0)
	await _shot("coral_mid", mp + Vector3(11, 3.0, -11), mp + Vector3(0, 1, 0), 62.0)
	# ---- sky lagoon train contexts
	main.pearl_count = main.PEARL_TOTAL
	for f: Dictionary in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _frames(10)
	var tr: Dictionary = main.g.get("train", {})
	if tr.is_empty():
		print("FAUD|train|FAIL no g[train]")
		quit()
		return
	var eng: Node3D = (tr["cars"] as Array)[0]["node"]
	var ep: Vector3 = eng.global_position
	var efwd: Vector3 = eng.global_transform.basis.z
	var ergt: Vector3 = eng.global_transform.basis.x
	# child-height station approach (as if walking up to the stop)
	await _shot("station_approach", ep + efwd * -6.0 + ergt * 14.0 + Vector3(0, 2.2, 0),
		ep + Vector3(0, 3, 0), 62.0)
	# boarding view beside the coach (car 2 sits ~18 back along the ring)
	var coach: Node3D = (tr["cars"] as Array)[2]["node"]
	var cp: Vector3 = coach.global_position
	var cfwd: Vector3 = coach.global_transform.basis.z
	var crgt: Vector3 = coach.global_transform.basis.x
	await _shot("boarding_view", cp + crgt * 8.0 + Vector3(0, 2.2, 0),
		cp + Vector3(0, 3.5, 0), 62.0)
	# ride POV from the cabin bench looking over the engine
	await _shot("ride_pov", cp + Vector3(0, 5.4, 0) + cfwd * -1.0,
		ep + Vector3(0, 5, 0) + efwd * 6.0, 70.0)
	# train + castle return context (far, with the castle behind)
	await _shot("castle_context", ep + efwd * 26.0 + ergt * -14.0 + Vector3(0, 7, 0),
		ep + Vector3(0, 4, 0), 55.0)
	# track perspective down the line (motion-extreme stand-in, low oblique)
	await _shot("track_perspective", ep + efwd * 12.0 + ergt * 1.8 + Vector3(0, 1.4, 0),
		ep + efwd * 30.0, 70.0)
	print("FAUD|done")
	quit()
