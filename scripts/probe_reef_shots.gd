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
	await _shot("reef_02_kelp_cathedral", Vector3(28, 28, 98), Vector3(-35, 8, 165))
	await _shot("reef_03_wreck_ravine", Vector3(-82, 30, 72), Vector3(-160, -4, 135))
	await _shot("reef_04_moon_grotto", Vector3(-82, 23, -25), Vector3(-160, -5, 5))
	await _shot("reef_05_rainbow_flats", Vector3(18, 22, -94), Vector3(-40, -4, -165))
	await _shot("reef_06_ice_current", Vector3(72, 30, -58), Vector3(140, 2, -115))
	await _shot("reef_07_faron_nursery_lane", Vector3(-18, 14, 24), Vector3(-72, -2, 8))
	print("REEFSHOT|DONE|", out_dir)
	quit()
