extends "res://study.gd"
## Source-only front-view work phrases. No game/save/reward dependencies.

var job: String = "detective"
var tool: Sprite2D
var grip: Sprite2D
var fixture: Node2D
var clue: Sprite2D
var soil: Sprite2D
var work_slab: Sprite2D
var job_time: float = 0.0
var fixture_center: Vector2
var tool_grip_px: Vector2
var tool_tip_px: Vector2
var tool_scale: float
var fixture_rest: Vector2
var fault: String = "none"
var contact_active: bool = false
var contact_error: float = 0.0
var hand_reference: Transform2D
var job_active: bool = false
var upper_work_texture: Texture2D
var fore_work_texture: Texture2D
var original_fore_texture: Texture2D
var complete_headwear: Sprite2D
var sleeve: Sprite2D
var sleeve_textures: Dictionary = {}
var garment_nodes: Dictionary = {}
var empty_paint: Texture2D
var legacy_anatomy: Texture2D
var legacy_anatomy_no_fin: Texture2D
var new_anatomy_with_legacy_fin: Texture2D
var legacy_ownership: Texture2D


func _ready() -> void:
	super._ready()
	automatic = false
	upper_work_texture = load_png("res://art/upper_work.png")
	fore_work_texture = load_png("res://art/fore_work.png")
	original_fore_texture = polygons["Forearm"].texture
	for theme: String in ["detective","geologist"]:
		sleeve_textures[theme] = load_png("res://art/"+theme+"_sleeve.png")
	var empty_image: Image = Image.create(1,1,false,Image.FORMAT_RGBA8)
	empty_image.fill(Color.TRANSPARENT)
	empty_paint = ImageTexture.create_from_image(empty_image)
	legacy_anatomy = load_png("res://art/anatomy.png")
	legacy_anatomy_no_fin = load_png("res://art/seed_anatomy_no_fin.png")
	new_anatomy_with_legacy_fin = load_png("res://art/new_anatomy_legacy_fin.png")
	legacy_ownership = load_png("res://art/ownership.png")
	build_garments()
	complete_headwear = sprite("detective_head.png", bones["Head"], 1)
	complete_headwear.centered = false
	complete_headwear.transform = rest_world["Head"].affine_inverse()
	sleeve = sprite("detective_sleeve.png", bones["LeftUpper"], 1)
	sleeve.centered = false
	sleeve.transform = rest_world["LeftUpper"].affine_inverse()
	fixture = Node2D.new()
	fixture.name = "FixedWorkFixture"
	fixture.z_index = -4
	actor.add_child(fixture)
	work_slab = sprite("slab.png", fixture, -2)
	clue = sprite("specimen.png", fixture, 0)
	soil = sprite("soil.png", fixture, 1)
	tool = sprite("magnifier_glass.png", actor, 5)
	grip = sprite("grip_front.png", bones["LeftHand"], 6)
	grip.centered = false
	grip.transform = rest_world["LeftHand"].affine_inverse()
	hand_reference = rest_world["LeftHand"]
	set_job("detective")
	label.text = "Source prototype: detective / geologist | D / G | 1–3 regressions | 4 work"


func sprite(path: String, parent: Node2D, depth: int) -> Sprite2D:
	var node: Sprite2D = Sprite2D.new()
	node.texture = load_png("res://art/" + path)
	node.z_index = depth
	parent.add_child(node)
	return node


func set_job(value: String) -> bool:
	if value not in ["detective", "geologist"]:
		return false
	job = value
	set_parts({"head":job,"body":job,"tail":job})
	tool.texture = load_png("res://art/magnifier_glass.png" if job == "detective" else "res://art/brush.png")
	tool_grip_px = Vector2(345, 369) if job == "detective" else Vector2(660, 400)
	tool_tip_px = Vector2(177, 151) if job == "detective" else Vector2(234, 799)
	tool_scale = 0.29 if job == "detective" else 0.18
	clue.texture = load_png("res://art/specimen.png" if job == "detective" else "res://art/fossil.png")
	clue.scale = Vector2.ONE * (0.14 if job == "detective" else 0.21)
	work_slab.scale = Vector2(0.32, 0.32)
	soil.scale = Vector2(0.22, 0.22)
	work_slab.visible = job == "geologist"
	soil.visible = job == "geologist"
	set_work_pose(2.3)
	fixture_center = tool.to_global(tool_tip_px - tool.texture.get_size() * 0.5)
	fixture.position = actor.to_local(fixture_center)
	fixture_rest = fixture.position
	set_work_pose(0.0)
	return true


func set_parts(parts: Dictionary) -> bool:
	if not super.set_parts(parts):
		return false
	if complete_headwear != null:
		var theme: String = String(selected_parts.head)
		complete_headwear.visible = theme in ["detective","geologist"]
		if complete_headwear.visible:
			complete_headwear.texture = garment_textures[theme+"_head"]
			polygons["Headwear"].visible = false
	if sleeve != null:
		var theme: String = String(selected_parts.body)
		sleeve.visible = theme in ["detective","geologist"]
		if sleeve.visible:
			sleeve.texture = sleeve_textures[theme]
	for name: String in garment_nodes:
		var bits: PackedStringArray = name.split("_")
		garment_nodes[name].visible = String(selected_parts[bits[1]]) == bits[0]
	if not garment_nodes.is_empty():
		var new_body: bool = String(selected_parts.body) in ["detective","geologist"]
		var new_tail: bool = String(selected_parts.tail) in ["detective","geologist"]
		clothing_material.set_shader_parameter("new_body_binding",new_body)
		clothing_material.set_shader_parameter("ownership",garment_textures["ownership"] if new_tail else legacy_ownership)
		var all_original: bool = selected_parts.head=="original" and selected_parts.body=="original" and selected_parts.tail=="original"
		if not all_original:
			if new_body:
				body.texture = garment_textures["anatomy"] if new_tail else new_anatomy_with_legacy_fin
			else:
				body.texture = legacy_anatomy_no_fin if new_tail else legacy_anatomy
		for slot: String in ["body","tail"]:
			if String(selected_parts[slot]) in ["detective","geologist"]:
				clothing_material.set_shader_parameter(slot+"_paint",empty_paint)
	return true


func build_garments() -> void:
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://garment_meshes.json"))
	for mesh: Dictionary in data.meshes:
		var polygon: Polygon2D = Polygon2D.new()
		polygon.name = String(mesh.name)
		polygon.texture = load_png("res://"+String(mesh.texture))
		polygon.z_index = int(mesh.z)
		var points: PackedVector2Array = PackedVector2Array()
		for p: Array in mesh.vertices:
			points.append(Vector2(p[0],p[1]))
		polygon.polygon = points
		polygon.uv = points
		var triangles: Array = []
		for t: Array in mesh.triangles:
			triangles.append(PackedInt32Array(t))
		polygon.polygons = triangles
		actor.add_child(polygon)
		polygon.skeleton = polygon.get_path_to(skeleton)
		for name: String in mesh.weights:
			polygon.add_bone(skeleton.get_path_to(bones[name]),PackedFloat32Array(mesh.weights[name]))
		garment_nodes[String(mesh.name)] = polygon


func work_curve(t: float) -> Dictionary:
	var pose: Dictionary = authored_pose("arm_bend", 0.0)
	var reach: float = pulse(t, 0.35, 1.25, 4.5, 5.65)
	var work: float = pulse(t, 1.25, 1.6, 3.9, 4.45)
	var stroke: float = sin((t - 1.6) * TAU * 0.8) * work
	pose["LeftUpper"] = deg_to_rad(12.0 * reach + 1.8 * stroke)
	pose["LeftFore"] = deg_to_rad(45.0 * reach + 6.0 * stroke)
	pose["Torso"] = deg_to_rad(-1.4 * reach + 0.5 * stroke)
	pose["TailA"] = deg_to_rad(1.0 * reach)
	pose["TailB"] = deg_to_rad(-1.0 * reach - 0.2 * stroke)
	return pose


func set_work_pose(t: float) -> void:
	job_active = true
	job_time = t
	player.stop()
	var pose: Dictionary = work_curve(t)
	for name: String in bones:
		var bone: Bone2D = bones[name]
		bone.transform = bone.rest
		bone.rotation = bone.rest.get_rotation() + float(pose[name])
	eye_half.visible = false
	eye_closed.visible = false
	polygons["UpperArm"].texture = upper_work_texture
	polygons["Forearm"].texture = fore_work_texture
	grip.visible = true
	fixture.visible = true
	tool.visible = true
	var hand: Bone2D = bones["LeftHand"]
	var socket: Vector2 = stage_transform(hand) * Vector2(24, 0)
	var delta_angle: float = stage_transform(hand).get_rotation() - hand_reference.get_rotation()
	var tool_basis: Transform2D = Transform2D(delta_angle, Vector2.ZERO).scaled(Vector2.ONE * tool_scale)
	var offset: Vector2 = tool_grip_px - tool.texture.get_size() * 0.5
	tool.transform = Transform2D(tool_basis.x, tool_basis.y, socket - tool_basis.basis_xform(offset))
	if fault == "grip_slip":
		tool.position += Vector2(18, -12)
	if fault == "identity_scale":
		bones["Head"].scale = Vector2(1.15, 1.15)
	if fault == "fixture_drift":
		fixture.position = fixture_rest + Vector2(14, 0)
	else:
		fixture.position = fixture_rest
	var actual: Vector2 = tool.transform * offset
	contact_error = actual.distance_to(socket)
	var tip: Vector2 = tool.transform * (tool_tip_px - tool.texture.get_size() * 0.5)
	contact_active = t >= 1.6 and t <= 4.1 and tip.distance_to(fixture.position) <= 70.0
	soil.modulate.a = 1.0 - clampf((t - 1.6) / 2.5, 0.0, 1.0) if contact_active or t > 4.1 else 1.0
	if fault == "original_underlay":
		body.texture = original_body_texture
		body.material = null


func set_regression(clip: String, t: float) -> void:
	job_active = false
	set_parts(selected_parts)
	polygons["Forearm"].texture = original_fore_texture
	grip.visible = false
	tool.visible = false
	fixture.visible = false
	super.set_pose(clip,t)


func job_record() -> Dictionary:
	var record: Dictionary = state_record()
	var socket: Vector2 = stage_transform(bones["LeftHand"]) * Vector2(24, 0)
	var point: Vector2 = tool.transform * (tool_grip_px - tool.texture.get_size() * 0.5)
	var tip: Vector2 = tool.transform * (tool_tip_px - tool.texture.get_size() * 0.5)
	record.merge({"job":job,"time":job_time,"view":"front","grip_error_px":point.distance_to(socket),"socket":[socket.x,socket.y],"tool_grip":[point.x,point.y],"tool_tip":[tip.x,tip.y],"fixture":[fixture.position.x,fixture.position.y],"fixture_drift_px":fixture.position.distance_to(fixture_rest),"contact_active":contact_active,"soil_alpha":soil.modulate.a,"tool_z":tool.z_index,"fingers_z":grip.z_index,"fault":fault})
	return record


func _process(delta: float) -> void:
	if automatic:
		time_seconds = minf(time_seconds + delta,6.4) if job_active else fmod(time_seconds + delta,clip_length(current_clip))
		if job_active:
			set_work_pose(time_seconds)
			if time_seconds >= 6.4:
				automatic = false
		else:
			set_regression(current_clip, time_seconds)


func _input(event: InputEvent) -> void:
	super._input(event)
	if event is InputEventKey and event.pressed and not event.echo:
		var key: InputEventKey = event
		if key.keycode == KEY_D or key.keycode == KEY_G:
			set_job("detective" if key.keycode == KEY_D else "geologist")
			time_seconds = 0.0
			job_active = true
			automatic = true
		if key.keycode == KEY_4:
			job_active = true
			time_seconds = 0.0
			automatic = true


func _unhandled_key_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		automatic = not automatic
	if event is InputEventKey and event.pressed and event.keycode in [KEY_1,KEY_2,KEY_3]:
		current_clip = ["arm_bend","blink","tail_bend"][event.keycode-KEY_1]
		time_seconds = 0.0
		set_regression(current_clip, 0.0)
		automatic = true
