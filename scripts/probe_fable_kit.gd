extends SceneTree
# Visual evidence for the Fable-kit constructed models (not a CI probe —
# needs a display renderer). Captures: reef meadow with the new volumetric
# kelp + bare coral, the authored locomotive on the ring, the authored track
# segments, and the station platform + shelter. Prints FKIT|... lines.

const OUT := "res://audit/fable_kit_shots"

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
	print("FKIT|", name, "|", error_string(err))


func _init() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
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
	# ---- reef meadow: the new kelp + coral scatter around the player start
	var pp: Vector3 = main.player.position
	await _shot("reef_meadow_wide", pp + Vector3(14, 9, 14), pp + Vector3(0, 1, 0))
	await _shot("reef_meadow_low", pp + Vector3(-18, 4, 8), pp + Vector3(0, 2, -6))
	# close-ups over the kelp meadow and mixed reef floor (habitat centers)
	var kp: Vector3 = main._district_ref().scatter_point("kelp")
	await _shot("kelp_habitat", kp + Vector3(10, 6, 10), kp + Vector3(0, 2, 0), 55.0)
	var mp: Vector3 = main._district_ref().scatter_point("mixed")
	await _shot("mixed_habitat", mp + Vector3(9, 5, -9), mp + Vector3(0, 1, 0), 55.0)
	# ---- sky lagoon: train, track, station
	main.pearl_count = main.PEARL_TOTAL
	for f: Dictionary in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _frames(10)
	var tr: Dictionary = main.g.get("train", {})
	if tr.is_empty():
		print("FKIT|train|FAIL no g[train]")
		quit()
		return
	var eng: Node3D = (tr["cars"] as Array)[0]["node"]
	var kids: Array = []
	for ch: Node in eng.get_children():
		kids.append(ch.name)
	print("FKIT|engine children: ", str(kids))
	var ep: Vector3 = eng.global_position
	var efwd: Vector3 = eng.global_transform.basis.z
	var ergt: Vector3 = eng.global_transform.basis.x
	await _shot("loco_three_q", ep + efwd * 13.0 + ergt * 8.0 + Vector3(0, 5, 0),
		ep + Vector3(0, 3.5, 0))
	await _shot("loco_side", ep + ergt * 13.0 + Vector3(0, 3, 0), ep + Vector3(0, 3.5, 0))
	await _shot("track_low", ep + efwd * 16.0 + ergt * 2.0 + Vector3(0, 1.6, 0),
		ep + efwd * 4.0, 55.0)
	# station: dwell point area (engine parks at bearing STATION_A)
	var o: Vector3 = tr["o"]
	var a: float = CourtyardTrain.STATION_A
	var radial := Vector3(sin(a), 0, cos(a))
	var sc: Vector3 = Vector3(0.0, 0, -3.5) + radial * (191.5 + 6.5)
	sc.y = main._lagoon_local(sc.x, sc.z)
	var sw: Vector3 = o + sc
	await _shot("station_area", sw + Vector3(16, 10, -22), sw + Vector3(-4, 2, -10))
	var ap: float = a - 0.09
	var rad2 := Vector3(sin(ap), 0, cos(ap))
	var pc: Vector3 = Vector3(0.0, 0, -3.5) + rad2 * (191.5 + 6.2)
	pc.y = main._lagoon_local(pc.x, pc.z)
	var pw: Vector3 = o + pc
	await _shot("platform_shelter", pw + Vector3(-12, 7, 10), pw + Vector3(0, 2, 0))
	print("FKIT|done")
	quit()
