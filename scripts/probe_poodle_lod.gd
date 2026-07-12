extends SceneTree
const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/95e90298-f74a-40cb-b3b4-6e45745fdde0/scratchpad/poodle_lod_compare.png"

func _init() -> void:
	var scene := Node3D.new()
	root.add_child(scene)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-45, 30, 0)
	scene.add_child(sun)
	var env := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(0.55, 0.7, 0.85)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(0.8, 0.85, 0.9)
	e.ambient_light_energy = 0.7
	env.environment = e
	scene.add_child(env)
	var orig: Node3D = (load("res://assets/characters/chuck_poodle.glb") as PackedScene).instantiate()
	orig.position = Vector3(-1.2, 0, 0)
	scene.add_child(orig)
	var slim: Node3D = (load("res://assets/characters/chuck_poodle_slim.glb") as PackedScene).instantiate()
	slim.position = Vector3(1.2, 0, 0)
	scene.add_child(slim)
	var cam := Camera3D.new()
	cam.position = Vector3(0, 0.6, 4.2)
	cam.look_at(Vector3(0, 0.1, 0), Vector3.UP)
	scene.add_child(cam)
	cam.make_current()
	for i in range(6):
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_viewport().get_texture().get_image().save_png(OUT)
	print("saved compare: original(L, 603k tris) vs slim(R, 72k tris)")
	quit()
