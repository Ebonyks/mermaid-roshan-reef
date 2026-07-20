extends SceneTree

# Fixed Mobile-render captures for the northern kingdom. These are the visual
# acceptance evidence for the 4.5/5 art gate: gameplay, mid, and near views of
# every distinct authored family and the larger runtime compositions.

var cam: Camera3D
var main: ReefMain
var out_dir := ""


func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame


func _shot(name: String, pos: Vector3, look: Vector3, fov: float = 64.0) -> void:
	cam.fov = fov
	cam.position = pos
	cam.look_at(look, Vector3.UP)
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var err: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("NORTHSHOT|", name, "|", "OK" if err == OK else "FAIL")


func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("NORTHSHOT|RESULT|HEADLESS SKIP")
		quit()
		return
	var requested: String = OS.get_environment("NORTH_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path("res://tmp/northern_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.intro_active:
		main._skip_intro()
	await _settle(12)
	main._enter_northern_kingdom()
	await _settle(45)
	main.set_process(false)
	main.player.set_process(false)
	main.player.visible = false
	if main.hud_layer != null:
		main.hud_layer.visible = false
	cam = Camera3D.new()
	cam.fov = 64.0
	cam.far = 720.0
	get_root().add_child(cam)
	cam.current = true
	var o: Vector3 = main.NORTHERN_POS
	await _shot("north_01_pass_gameplay", o + Vector3(0, 50, 405),
		o + Vector3(0, 24, 348))
	await _shot("north_02_pass_mid", o + Vector3(55, 48, 385),
		o + Vector3(0, 22, 348))
	await _shot("north_03_forest_gameplay", o + Vector3(38, 23, 245),
		o + Vector3(-8, 7, 198))
	await _shot("north_04_forest_mushrooms", o + Vector3(25, 14, 182),
		o + Vector3(14, 4, 170))
	await _shot("north_05_spirit_clearing", o + Vector3(12, 9, 124),
		o + Vector3(31, 5, 138), 52.0)
	await _shot("north_06_log_bridge", o + Vector3(-20, 28, -8),
		o + Vector3(-20, 3, -28))
	await _shot("north_07_town_overview", o + Vector3(96, 48, -120),
		o + Vector3(0, 8, -190))
	await _shot("north_08_house_red", o + Vector3(2, 13, -150),
		o + Vector3(-26, 7, -150))
	await _shot("north_09_house_amber", o + Vector3(2, 12, -196),
		o + Vector3(-24, 7, -196))
	await _shot("north_10_house_aqua", o + Vector3(0, 12, -232),
		o + Vector3(-26, 7, -232))
	await _shot("north_11_house_rose", o + Vector3(-4, 13, -138),
		o + Vector3(22, 7, -138))
	await _shot("north_12_house_blue", o + Vector3(-2, 12, -172),
		o + Vector3(24, 7, -172))
	await _shot("north_13_house_orange", o + Vector3(-2, 12, -240),
		o + Vector3(24, 7, -240))
	await _shot("north_14_forge", o + Vector3(6, 12, -202),
		o + Vector3(-13, 4, -206))
	await _shot("north_15_dock", o + Vector3(54, 12, -140),
		o + Vector3(35, 2, -158))
	await _shot("north_16_mill", o + Vector3(27, 14, -199),
		o + Vector3(52, 5, -218))
	await _shot("north_17_castle_gameplay", o + Vector3(0, 20, -255),
		o + Vector3(0, 18, -318))
	await _shot("north_18_castle_mid", o + Vector3(104, 54, -252),
		o + Vector3(0, 17, -318))
	await _shot("north_19_castle_gate", o + Vector3(16, 17, -252),
		o + Vector3(0, 11, -292), 58.0)
	await _shot("north_20_hall_wide", o + Vector3(0, 13, -306),
		o + Vector3(0, 10, -328), 72.0)
	await _shot("north_21_hall_centerpiece", o + Vector3(5, 12, -307),
		o + Vector3(0, 9, -320), 66.0)
	await _shot("north_22_hall_bedrooms", o + Vector3(-19, 28, -336),
		o + Vector3(-19, 18.5, -344), 82.0)
	await _shot("north_23_wisp_near", o + Vector3(9, 44, 318),
		o + Vector3(3, 37, 330))
	print("NORTHSHOT|DONE|", out_dir)
	quit()
