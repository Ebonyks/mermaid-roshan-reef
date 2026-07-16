extends SceneTree
# BEAK PROBE — close-up turntable of the gen2 penguin's head, raw glb import
# (no game shaders), to inspect beak geometry/paint. Windowed run:
#   Godot_console.exe --path . --resolution 1024x1024 -s res://scripts/probe_penguin_beak.gd

func _init() -> void:
	var root := get_root()
	var world := Node3D.new()
	root.add_child(world)
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.25, 0.28, 0.35)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1)
	env.ambient_light_energy = 1.0
	var we := WorldEnvironment.new()
	we.environment = env
	world.add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation = Vector3(-0.9, 0.4, 0)
	world.add_child(sun)
	var ps: PackedScene = load("res://assets/props/gen2/penguin.glb")
	var peng: Node3D = ps.instantiate()
	world.add_child(peng)
	# --- candidate beak graft (mirror of main.gd _attach_penguin_beak) ---
	var skels := peng.find_children("*", "Skeleton3D", true, false)
	print("BEAK|skeletons=", skels.size())
	if skels.size() > 0:
		var skel: Skeleton3D = skels[0]
		print("BEAK|bones=", skel.get_bone_count(), " head_idx=", skel.find_bone("head"))
		var att := BoneAttachment3D.new()
		skel.add_child(att)
		att.bone_name = "head"
		var beak := MeshInstance3D.new()
		var cone := CylinderMesh.new()
		cone.top_radius = 0.0
		cone.bottom_radius = 0.07
		cone.height = 0.18
		cone.radial_segments = 24
		beak.mesh = cone
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = Color(1.0, 0.66, 0.12)
		bmat.roughness = 0.9
		beak.material_override = bmat
		att.add_child(beak)
		beak.position = Vector3(0, 0.50, 0.14)
		beak.rotation = Vector3(-0.32, 0, 0)
	# center on its AABB
	var aabb := AABB()
	var first := true
	for mi in peng.find_children("*", "MeshInstance3D", true, false):
		var b: AABB = (mi as MeshInstance3D).global_transform * (mi as MeshInstance3D).get_aabb()
		aabb = b if first else aabb.merge(b)
		first = false
	var c := aabb.get_center()
	var r: float = aabb.size.length() * 0.5
	print("BEAK|aabb center=", c, " size=", aabb.size)
	var cam := Camera3D.new()
	world.add_child(cam)
	cam.current = true
	var outdir: String = ProjectSettings.globalize_path("res://tools/out/penguin_probe")
	DirAccess.make_dir_recursive_absolute(outdir)
	# the sculpt faces -Y in Blender frame -> after glTF import the head sits
	# toward -Z or +Z; orbit all the way around at head height to be sure
	var views := [0.0, 0.5, 1.0, 1.5]   # quarter turns
	for i in range(views.size()):
		var a: float = float(views[i]) * PI
		cam.position = c + Vector3(sin(a) * r * 1.6, r * 0.35, cos(a) * r * 1.6)
		cam.look_at(c)
		for k in range(6):
			await process_frame
		await RenderingServer.frame_post_draw
		get_root().get_viewport().get_texture().get_image().save_png(outdir + "/beak_%d.png" % i)
	print("BEAK|done")
	quit()
