extends SceneTree
## Builds res://rig_wave.tscn from res://rig.json (rig parts, meshes, weights) and the solved
## LTX motion in ../data/rig_pose.json. Rules-off pilot run 1 (2026-10-07); study only.
## godot --headless --path run1_godot -s res://tools/build_rig.gd

const FPS := 24.0


func stage_xf(node: Node, stage: Node2D) -> Transform2D:
	var t := Transform2D.IDENTITY
	var n := node
	while n != stage:
		t = (n as Node2D).transform * t
		n = n.get_parent()
	return t


func v2(a: Array) -> Vector2:
	return Vector2(a[0], a[1])


func _initialize() -> void:
	var rig: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://rig.json"))
	var pose_path := ProjectSettings.globalize_path("res://").path_join("../data/rig_pose.json")
	var pose: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(pose_path))
	var stage := Node2D.new()
	stage.name = "Stage"
	stage.scale = Vector2(2, 2)
	root.add_child(stage)
	var skel := Skeleton2D.new()
	skel.name = "Skeleton"
	stage.add_child(skel)
	var bones := {}
	for b in rig.bones:
		var bone := Bone2D.new()
		bone.name = b.name
		var parent: Node2D = skel if b.parent == null else bones[b.parent]
		parent.add_child(bone)
		var head := v2(b.head)
		var tail := v2(b.tail)
		bone.transform = stage_xf(parent, stage).affine_inverse() * Transform2D((tail - head).angle(), head)
		bone.set_autocalculate_length_and_angle(false)
		bone.set_length((tail - head).length())
		bone.set_bone_angle(0.0)
		bone.rest = bone.transform
		bones[b.name] = bone
	for m in rig.meshes:
		var poly := Polygon2D.new()
		poly.name = m.name
		poly.texture = load("res://" + m.texture)
		var pts := PackedVector2Array()
		for v in m.vertices:
			pts.append(v2(v))
		poly.polygon = pts
		poly.uv = pts
		var polys := []
		for t in m.triangles:
			polys.append(PackedInt32Array(t))
		poly.polygons = polys
		poly.z_index = int(m.z)
		stage.add_child(poly)
		poly.skeleton = poly.get_path_to(skel)
		for bname in m.weights:
			poly.add_bone(skel.get_path_to(bones[bname]), PackedFloat32Array(m.weights[bname]))
	for s in rig.sprites:
		var spr := Sprite2D.new()
		spr.name = s.name
		spr.texture = load("res://" + s.texture)
		spr.centered = false
		spr.z_index = int(s.z)
		var bone: Bone2D = bones[s.bone]
		bone.add_child(spr)
		var want := Transform2D.IDENTITY
		if s.cell_wrist != null:
			var hb: Dictionary = {}
			for b in rig.bones:
				if b.name == "Hand":
					hb = b
			var w0 := v2(hb.head)
			var phi0 := (v2(hb.tail) - w0).angle()
			var w := v2(s.cell_wrist)
			var phi := (v2(s.cell_tip) - w).angle()
			var k: float = s.scale
			want = Transform2D(phi0, w0) * Transform2D(0.0, Vector2(k, k), 0.0, Vector2.ZERO) * Transform2D(-phi, Vector2.ZERO) * Transform2D(0.0, -w)
		spr.transform = stage_xf(bone, stage).affine_inverse() * want
		spr.visible = s.name != "HandOpen"
	# Animation from the solved pose.
	var anim := Animation.new()
	anim.length = pose.frames.size() / FPS
	anim.step = 1.0 / FPS
	anim.loop_mode = Animation.LOOP_LINEAR
	var tracks := {}
	var add := func(path: String, discrete: bool) -> int:
		var i := anim.add_track(Animation.TYPE_VALUE)
		anim.track_set_path(i, NodePath(path))
		anim.value_track_set_update_mode(i, Animation.UPDATE_DISCRETE if discrete else Animation.UPDATE_CONTINUOUS)
		anim.track_set_interpolation_type(i, Animation.INTERPOLATION_LINEAR)
		return i
	var bp := func(n: String) -> String:
		return str(stage.get_path_to(bones[n]))
	var rot_tracks := ["Torso", "Head", "Hair", "UpperArm", "Fore", "Hand", "Tail1", "Tail2", "Fin"]
	for n in rot_tracks:
		tracks[n] = add.call(bp.call(n) + ":rotation", false)
	tracks["RootPos"] = add.call(bp.call("Root") + ":position", false)
	tracks["ArmPos"] = add.call(bp.call("UpperArm") + ":position", false)
	tracks["HandRest"] = add.call(bp.call("Hand") + "/HandRest:visible", true)
	tracks["HandOpen"] = add.call(bp.call("Hand") + "/HandOpen:visible", true)
	var delta_key := {"Torso": "torso", "Head": "head", "Hair": "hair", "Tail1": "tail1", "Tail2": "tail2", "Fin": "fin"}
	for f in pose.frames:
		var t: float = f.index / FPS
		var d: Dictionary = f.body_delta
		for n in delta_key:
			anim.track_insert_key(tracks[n], t, bones[n].rest.get_rotation() + float(d[delta_key[n]]))
		anim.track_insert_key(tracks["RootPos"], t, bones["Root"].rest.origin + Vector2(d.root_dx, d.root_dy))
		var torso_world: float = bones["Root"].rest.get_rotation() + bones["Torso"].rest.get_rotation() + float(d.torso)
		var A: Array = f.arm_world_angles_rad
		var R: Array = f.arm_local_angles_rad
		anim.track_insert_key(tracks["UpperArm"], t, float(A[0]) - torso_world)
		anim.track_insert_key(tracks["Fore"], t, float(R[1]))
		anim.track_insert_key(tracks["Hand"], t, float(R[2]))
		var shrug := Vector2(f.shoulder_offset_cell[0], f.shoulder_offset_cell[1]).rotated(-torso_world)
		anim.track_insert_key(tracks["ArmPos"], t, bones["UpperArm"].rest.origin + shrug)
		anim.track_insert_key(tracks["HandRest"], t, f.hand_drawing == "rest")
		anim.track_insert_key(tracks["HandOpen"], t, f.hand_drawing == "open")
	var ap := AnimationPlayer.new()
	ap.name = "AnimationPlayer"
	stage.add_child(ap)
	var lib := AnimationLibrary.new()
	lib.add_animation("wave", anim)
	ap.add_animation_library("", lib)
	ap.autoplay = "wave"
	for n in stage.find_children("*", "", true, false):
		n.owner = stage
	var packed := PackedScene.new()
	var err := packed.pack(stage)
	if err != OK or ResourceSaver.save(packed, "res://rig_wave.tscn") != OK:
		push_error("RIG_BUILD_FAIL")
		quit(1)
		return
	print("RIG_BUILD_OK bones=%d meshes=%d sprites=%d frames=%d" % [bones.size(), rig.meshes.size(), rig.sprites.size(), pose.frames.size()])
	quit(0)
