extends SceneTree

# Fixed composition captures for the six first-world districts. Set
# REEF_SHOT_OUT to choose an absolute output folder; otherwise user:// is used.

var cam: Camera3D
var main: ReefMain
var out_dir := ""

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _shot(name: String, pos: Vector3, look: Vector3) -> void:
	cam.position = pos
	cam.look_at(look, Vector3.UP)
	await _settle(3)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var err: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("REEFSHOT|", name, "|", "OK" if err == OK else "FAIL")

func _init() -> void:
	var requested: String = OS.get_environment("REEF_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path("res://tmp/reef_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.intro_active:
		main._skip_intro()
	if main.hud_layer != null:
		main.hud_layer.visible = false
	cam = Camera3D.new()
	cam.fov = 68.0
	cam.far = 700.0
	get_root().add_child(cam)
	cam.current = true
	await _settle(35)
	await _shot("reef_01_pearl_garden", Vector3(38, 17, 58), Vector3(4, 1, 2))
	await _shot("reef_02_kelp_cathedral", Vector3(42, 24, 76), Vector3(-24, 13, 124))
	await _shot("reef_03_wreck_ravine", Vector3(-66, 24, 58), Vector3(-122, -2, 102))
	await _shot("reef_04_moon_grotto", Vector3(-62, 19, -30), Vector3(-126, -5, 3))
	await _shot("reef_05_rainbow_flats", Vector3(28, 17, -54), Vector3(-10, -2, -108))
	await _shot("reef_06_ice_current", Vector3(22, 37, -18), Vector3(82, 26, -62))
	print("REEFSHOT|DONE|", out_dir)
	quit()
