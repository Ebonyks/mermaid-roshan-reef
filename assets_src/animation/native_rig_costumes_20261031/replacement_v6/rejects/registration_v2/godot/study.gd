extends Node2D
## Isolated owner-authorized rig experiment. Does not load the game or a save.

var clothing_material: ShaderMaterial
var garment_textures: Dictionary = {}
var selected_parts: Dictionary = {"head":"ballet", "body":"ballet", "tail":"ballet"}
var polygons: Dictionary = {}
var skeleton: Skeleton2D
var bones: Dictionary = {}
var rig: Dictionary = {}
var player: AnimationPlayer
var body: Polygon2D
var eye_half: Sprite2D
var eye_closed: Sprite2D
var rest_world: Dictionary = {}
var actor: Node2D
var time_seconds: float = 0.0
var automatic: bool = true
var current_clip: String = "arm_bend"
var label: Label


func load_png(path: String) -> ImageTexture:
	var image: Image = Image.load_from_file(ProjectSettings.globalize_path(path))
	return ImageTexture.create_from_image(image)


func stage_transform(node: Node2D) -> Transform2D:
	return actor.global_transform.affine_inverse() * node.global_transform


func _ready() -> void:
	build_actor()
	var bg: ColorRect = ColorRect.new()
	bg.color = Color(0.08, 0.12, 0.19)
	bg.size = Vector2(1280, 720)
	bg.z_index = -20
	add_child(bg)
	label = Label.new()
	label.position = Vector2(28, 26)
	label.add_theme_font_size_override("font_size", 25)
	add_child(label)
	var help: Label = Label.new()
	help.text = "1  Shoulder + arm     2  Blink     3  Tail     Space  Pause\nB Ballet / M Magician / O Original / H Head / J Body / K Tail"
	help.position = Vector2(28, 640)
	help.add_theme_font_size_override("font_size", 18)
	add_child(help)
	actor.position = Vector2(340, 0)
	actor.scale = Vector2(0.7, 0.7)
	set_pose("arm_bend", 0.0)


func build_actor() -> void:
	rig = JSON.parse_string(FileAccess.get_file_as_string("res://rig.json"))
	actor = Node2D.new()
	actor.name = "Actor"
	add_child(actor)
	skeleton = Skeleton2D.new()
	skeleton.name = "Skeleton"
	actor.add_child(skeleton)
	for data in rig.bones:
		var bone: Bone2D = Bone2D.new()
		bone.name = str(data.name)
		bone.set_autocalculate_length_and_angle(false)
		var parent: Node2D = skeleton if data.parent == null else bones[str(data.parent)]
		parent.add_child(bone)
		var head: Vector2 = Vector2(data.head[0], data.head[1])
		var tail: Vector2 = Vector2(data.tail[0], data.tail[1])
		bone.transform = stage_transform(parent).affine_inverse() * Transform2D((tail - head).angle(), head)
		bone.set_autocalculate_length_and_angle(false)
		bone.set_length(head.distance_to(tail))
		bone.set_bone_angle(0.0)
		bone.rest = bone.transform
		bones[str(data.name)] = bone
		rest_world[str(data.name)] = stage_transform(bone)
	for mesh in rig.meshes:
		var polygon: Polygon2D = Polygon2D.new()
		polygon.name = str(mesh.name)
		polygons[str(mesh.name)] = polygon
		polygon.texture = load_png("res://" + str(mesh.texture))
		polygon.z_index = int(mesh.z)
		polygon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var points: PackedVector2Array = PackedVector2Array()
		for p in mesh.vertices:
			points.append(Vector2(p[0], p[1]))
		polygon.polygon = points
		polygon.uv = points
		var triangles: Array = []
		for tri in mesh.triangles:
			triangles.append(PackedInt32Array(tri))
		polygon.polygons = triangles
		actor.add_child(polygon)
		polygon.skeleton = polygon.get_path_to(skeleton)
		for bone_name in mesh.weights:
			polygon.add_bone(skeleton.get_path_to(bones[bone_name]), PackedFloat32Array(mesh.weights[bone_name]))
		if mesh.name == "Body":
			body = polygon
	var head_bone: Bone2D = bones["Head"]
	for state in ["half", "closed"]:
		var eye: Sprite2D = Sprite2D.new()
		eye.name = "Eyes" + state.capitalize()
		eye.texture = load_png("res://../../../native_rig_stress_20261031/art/eyes_" + state + ".png")
		eye.centered = false
		eye.z_index = 2
		head_bone.add_child(eye)
		eye.transform = stage_transform(head_bone).affine_inverse()
		eye.visible = false
		if state == "half":
			eye_half = eye
		else:
			eye_closed = eye
	player = AnimationPlayer.new()
	player.name = "AnimationPlayer"
	actor.add_child(player)
	player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var library: AnimationLibrary = AnimationLibrary.new()
	for clip in ["arm_bend", "blink", "tail_bend"]:
		library.add_animation(clip, build_animation(clip))
	player.add_animation_library("", library)
	set_parts(selected_parts)


func ease5(value: float) -> float:
	var v: float = clampf(value, 0.0, 1.0)
	return v * v * v * (v * (v * 6.0 - 15.0) + 10.0)


func pulse(t: float, start: float, peak: float, hold: float, finish: float) -> float:
	if t < peak:
		return ease5((t - start) / (peak - start))
	if t < hold:
		return 1.0
	return 1.0 - ease5((t - hold) / (finish - hold))


func authored_pose(clip: String, t: float) -> Dictionary:
	var pose: Dictionary = {}
	for name in bones:
		pose[name] = 0.0
	pose["eyes"] = "open"
	if clip == "arm_bend":
		var reach: float = pulse(t, 0.45, 1.35, 1.8, 2.85)
		var anticipation: float = pulse(t, 0.05, 0.25, 0.3, 0.65)
		pose["LeftUpper"] = deg_to_rad(12.0 * reach - 2.0 * anticipation)
		pose["LeftFore"] = deg_to_rad(45.0 * reach)
		pose["LeftHand"] = 0.0
		pose["Torso"] = deg_to_rad(-1.4 * reach + 0.5 * anticipation)
		# The unsegmented painted head/hair follows the torso as one rigid unit.
		pose["Head"] = 0.0
		pose["TailA"] = deg_to_rad(1.0 * reach)
		pose["TailB"] = deg_to_rad(-1.0 * reach)
	elif clip == "blink":
		# A brisk closing and slightly slower opening, discrete authored eyelid drawings.
		if t >= 1.0 and t < 1.05:
			pose["eyes"] = "half"
		elif t >= 1.05 and t < 1.13:
			pose["eyes"] = "closed"
		elif t >= 1.13 and t < 1.21:
			pose["eyes"] = "half"
	elif clip == "tail_bend":
		# One effort left, one gentle return through the opposite side, then a still settle.
		var bend: float = pulse(t, 0.3, 1.1, 1.25, 2.1) - 0.7 * pulse(t, 1.55, 2.35, 2.5, 3.55)
		pose["TailA"] = deg_to_rad(2.7 * bend)
		pose["TailB"] = deg_to_rad(4.5 * bend)
		pose["TailC"] = deg_to_rad(-3.6 * bend)
		pose["TailD"] = deg_to_rad(-2.7 * bend)
		pose["Fin"] = deg_to_rad(1.8 * bend)
		pose["Torso"] = deg_to_rad(-0.8 * bend)
		pose["Head"] = 0.0
	return pose


func clip_length(clip: String) -> float:
	return 4.0 if clip == "tail_bend" else 3.2 if clip == "arm_bend" else 2.4


func build_animation(clip: String) -> Animation:
	var animation: Animation = Animation.new()
	animation.length = clip_length(clip)
	animation.loop_mode = Animation.LOOP_LINEAR
	var tracks: Dictionary = {}
	for name in bones:
		var track: int = animation.add_track(Animation.TYPE_VALUE)
		animation.track_set_path(track, NodePath(str(actor.get_path_to(bones[name])) + ":rotation"))
		animation.track_set_interpolation_type(track, Animation.INTERPOLATION_LINEAR)
		tracks[name] = track
	for name in ["half", "closed"]:
		var track: int = animation.add_track(Animation.TYPE_VALUE)
		var eye: Sprite2D = eye_half if name == "half" else eye_closed
		animation.track_set_path(track, NodePath(str(actor.get_path_to(eye)) + ":visible"))
		animation.value_track_set_update_mode(track, Animation.UPDATE_DISCRETE)
		tracks["eyes_" + name] = track
	var count: int = int(round(animation.length * 120.0))
	for i in range(count + 1):
		var t: float = i / 120.0
		var pose: Dictionary = authored_pose(clip, t)
		for name in bones:
			var bone: Bone2D = bones[name]
			animation.track_insert_key(tracks[name], t, bone.rest.get_rotation() + float(pose[name]))
		for name in ["half", "closed"]:
			animation.track_insert_key(tracks["eyes_" + name], t, pose["eyes"] == name)
	return animation


func set_pose(clip: String, t: float) -> void:
	if player.current_animation != clip:
		player.play(clip)
	player.seek(t, true)
	current_clip = clip
	if label != null:
		label.text = {"arm_bend": "Shoulder + arm bend", "blink": "Natural blink", "tail_bend": "Tail bend + settle"}[clip]


func state_record() -> Dictionary:
	var states: Dictionary = {}
	for name in bones:
		var bone: Bone2D = bones[name]
		var xf: Transform2D = stage_transform(bone)
		states[name] = [xf.x.x, xf.x.y, xf.y.x, xf.y.y, xf.origin.x, xf.origin.y]
	return {"bones": states, "eyes_half": eye_half.visible, "eyes_closed": eye_closed.visible}


func _process(delta: float) -> void:
	if automatic:
		time_seconds = fmod(time_seconds + delta, clip_length(current_clip))
		set_pose(current_clip, time_seconds)


func _unhandled_key_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		automatic = not automatic
	if event is InputEventKey and event.pressed:
		var key: InputEventKey = event
		if key.keycode in [KEY_1, KEY_2, KEY_3]:
			current_clip = ["arm_bend", "blink", "tail_bend"][key.keycode - KEY_1]
			time_seconds = 0.0


func set_parts(parts: Dictionary) -> bool:
	# Validate all requested slots before changing any state; unknown IDs fail closed.
	for slot: String in parts:
		if slot not in ["head", "body", "tail"] or String(parts[slot]) not in ["original", "ballet", "magician"]:
			return false
	var next: Dictionary = selected_parts.duplicate(true)
	for slot: String in parts:
		next[slot] = String(parts[slot])
	if clothing_material == null:
		clothing_material = ShaderMaterial.new()
		clothing_material.shader = load("res://costume.gdshader")
		body.material = clothing_material
		for theme: String in ["ballet", "magician"]:
			for slot: String in ["head", "body", "tail", "scalp"]:
				garment_textures[theme + "_" + slot] = load_png("res://../art/" + theme + "_" + slot + ".png")
		garment_textures["original"] = load_png("res://../../../native_rig_stress_20261031/art/body.png")
		garment_textures["ownership"] = load_png("res://../art/ownership.png")
		clothing_material.set_shader_parameter("ownership", garment_textures["ownership"])
	for slot: String in ["body", "tail"]:
		var theme: String = String(next[slot])
		clothing_material.set_shader_parameter(slot + "_paint", garment_textures["original" if theme == "original" else theme + "_" + slot])
	var head_theme: String = String(next.head)
	clothing_material.set_shader_parameter("scalp_paint", garment_textures["original" if head_theme == "original" else head_theme + "_scalp"])
	var head: Polygon2D = polygons["Headwear"]
	head.visible = String(next.head) != "original"
	if head.visible:
		head.texture = garment_textures[String(next.head) + "_head"]
	selected_parts = next
	return true


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		var key: InputEventKey = event
		if key.keycode in [KEY_B, KEY_M, KEY_O]:
			var theme: String = "ballet" if key.keycode == KEY_B else ("magician" if key.keycode == KEY_M else "original")
			set_parts({"head":theme, "body":theme, "tail":theme})
		for slot: String in ["head", "body", "tail"]:
			var code: int = {"head":KEY_H, "body":KEY_J, "tail":KEY_K}[slot]
			if key.keycode == code:
				var options: Array[String] = ["original", "ballet", "magician"]
				set_parts({slot:options[(options.find(String(selected_parts[slot])) + 1) % 3]})


func equip_catalog_ids(ids: Dictionary) -> bool:
	var registry: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://costumes.json"))
	var request: Dictionary = {}
	for slot: String in ids:
		if slot not in ["head", "body", "tail"]:
			return false
		var found: bool = false
		var original: String = "roshan_original" if slot == "body" else slot + "_original"
		if String(ids[slot]) == original:
			request[slot] = "original"
			found = true
		for theme: String in registry.stable_catalog_ids:
			if String(registry.stable_catalog_ids[theme][slot]) == String(ids[slot]):
				request[slot] = theme
				found = true
		if not found:
			return false
	return set_parts(request)
