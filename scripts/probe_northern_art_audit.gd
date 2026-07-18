extends SceneTree

# Fixed Mobile-render captures for the northern kingdom. These are the visual
# acceptance evidence for the 4/5 art gate: gameplay, mid, and near views of
# every distinct asset family introduced with the world.

var cam: Camera3D
var main: ReefMain
var out_dir := ""


func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame


func _shot(name: String, pos: Vector3, look: Vector3) -> void:
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
	await _shot("north_01_pass_gameplay", o + Vector3(0, 48, 214), o + Vector3(0, 24, 152))
	await _shot("north_02_pass_mid", o + Vector3(0, 50, 250), o + Vector3(0, 22, 158))
	await _shot("north_03_forest_gameplay", o + Vector3(42, 24, 134), o + Vector3(0, 8, 82))
	await _shot("north_04_forest_mid", o + Vector3(0, 18, 120), o + Vector3(0, 7, 76))
	await _shot("north_05_town_overview", o + Vector3(118, 52, 58), o + Vector3(0, 8, -2))
	await _shot("north_06_house_near", o + Vector3(-48, 14, 31), o + Vector3(-76, 8, 31))
	await _shot("north_07_dock_near", o + Vector3(154, 13, 30), o + Vector3(121, 1, 2))
	await _shot("north_08_castle_gameplay", o + Vector3(0, 24, 44), o + Vector3(0, 14, -55))
	await _shot("north_09_castle_mid", o + Vector3(92, 48, -4), o + Vector3(0, 14, -55))
	await _shot("north_10_castle_near", o + Vector3(0, 18, -5), o + Vector3(0, 12, -55))
	await _shot("north_11_wisp_near", o + Vector3(10, 8, 60), o + Vector3(4, 6.5, 54))
	print("NORTHSHOT|DONE|", out_dir)
	quit()
