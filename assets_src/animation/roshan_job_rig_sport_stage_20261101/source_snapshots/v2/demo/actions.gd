extends "res://base.gd"
## Owner-commissioned source-only skins and object studies. No game or save APIs.

var elapsed: float = 0.0
var action: String = "boxer"
var run_action: bool = true
var rig_contract: Dictionary = {}
var action_parts: Dictionary = {}
var part_textures: Dictionary = {}
var hip_panel: Sprite2D
var action_body: Polygon2D
var new_head: Sprite2D
var glove: Sprite2D
var mitt: Sprite2D
var wheel: Sprite2D
var mic_lower: Sprite2D
var popstar_grip: Sprite2D
var mic_upper: Sprite2D
var grip_pictures: Dictionary = {}
var joint_caps: Dictionary = {}
var view_pictures: Dictionary = {}
var active_contact: bool = false
var prop_owner: String = "fixture"
var selected_view: String = "guard"
var control: String = "none"
var prop_target_left: Vector2 = Vector2.ZERO
var prop_target_right: Vector2 = Vector2.ZERO
var fixture_rest: Vector2 = Vector2.ZERO
var fixture_actual: Vector2 = Vector2.ZERO
var support: Line2D

func _ready() -> void:
	super._ready()
	automatic = false
	clothing_material.set_shader_parameter("action_mask",load_png("res://art/action_mask.png"))
	rig_contract = JSON.parse_string(FileAccess.get_file_as_string("res://contract.json"))
	assert(rig_contract.id == "roshan.canvas.shared" and rig_contract.version == "1.0.0")
	new_head = Sprite2D.new()
	new_head.centered = false
	new_head.z_index = 7
	bones["Head"].add_child(new_head)
	new_head.transform = stage_transform(bones["Head"]).affine_inverse()
	hip_panel = Sprite2D.new()
	hip_panel.texture = load_png("res://art/racer_hip_panel.png")
	hip_panel.centered = false
	hip_panel.z_index = 1
	bones["Torso"].add_child(hip_panel)
	hip_panel.transform = stage_transform(bones["Torso"]).affine_inverse()*Transform2D(0.0,Vector2(574,440))
	action_body = body.duplicate()
	action_body.name = "ReplacementActionBody"
	actor.add_child(action_body)
	action_body.skeleton = action_body.get_path_to(skeleton)
	for name: String in ["LeftUpper","LeftFore","LeftHand","RightUpper","RightFore","RightHand"]:
		var part: Sprite2D = Sprite2D.new()
		part.name = name + "Action"
		part.centered = false
		part.z_index = 5 if "Hand" in name else 1
		bones[name].add_child(part)
		part.transform = stage_transform(bones[name]).affine_inverse()
		action_parts[name] = part
	for side: String in ["Left","Right"]:
		var cap: Sprite2D = Sprite2D.new()
		cap.texture = load_png("res://art/"+side+"ElbowCap.png")
		cap.centered = false
		cap.z_index = 2
		bones[side+"Fore"].add_child(cap)
		cap.transform = stage_transform(bones[side+"Fore"]).affine_inverse()
		joint_caps[side] = cap
	glove = make_prop("glove_guard",6)
	mitt = make_prop("focus_mitt",4)
	wheel = make_prop("wheel",3)
	popstar_grip = make_prop("popstar_grip",6)
	mic_lower = make_prop("mic_lower",3)
	mic_upper = make_prop("mic_upper",3)
	for side: String in ["left","right"]:
		grip_pictures[side] = make_prop("racer_grip_"+side,6)
	for name: String in ["guard","jab","palm"]:
		view_pictures[name] = load_png("res://art/glove_"+name+".png")
	support = Line2D.new()
	support.name = "FixedFixtureDiagram"
	support.default_color = Color(0.36,0.56,0.65)
	support.width = 4.0
	support.z_index = -2
	actor.add_child(support)
	for child: Node in get_children():
		if child is Label and child != label:
			child.text = "SOURCE ONLY | 1 Boxer / 2 Racer / 3 Pop star / 4-6 original motions\nSpace pause | Left/Right frame step | H/J/K mix slots | O exact original"
	set_parts({"head":"boxer","body":"boxer","tail":"boxer"})
	pose_action(action,0.0)

func make_prop(texture_name: String, order: int) -> Sprite2D:
	var node: Sprite2D = Sprite2D.new()
	node.texture = load_png("res://art/"+texture_name+".png")
	node.centered = false
	node.z_index = order
	actor.add_child(node)
	return node

func set_parts(parts: Dictionary) -> bool:
	if not super.set_parts(parts):
		return false
	if hip_panel != null:
		hip_panel.visible = String(selected_parts.body) == "racer"
	if new_head != null:
		var theme: String = String(selected_parts.head)
		new_head.visible = theme in ["boxer","racer","popstar"]
		if new_head.visible:
			new_head.texture = garment_textures[theme+"_head"]
			polygons["Headwear"].visible = false
	return true

func duration(clip: String) -> float:
	return 8.0 if clip in ["boxer","racer","popstar"] else clip_length(clip)

func socket(side: String) -> Vector2:
	var id: String = "grip.screen_left" if side == "Left" else "grip.screen_right"
	for entry: Dictionary in rig_contract.sockets:
		if String(entry.id) == id:
			return stage_transform(bones[side+"Hand"]) * Vector2(entry.position_px[0],entry.position_px[1])
	assert(false,"Unknown shared grip socket")
	return Vector2.INF

func solve_arm(side: String,target: Vector2,sign_elbow: float) -> void:
	var upper: Bone2D = bones[side+"Upper"]
	var fore: Bone2D = bones[side+"Fore"]
	var hand: Bone2D = bones[side+"Hand"]
	var shoulder: Vector2 = stage_transform(upper).origin
	var distal: Vector2 = hand.rest.origin + Vector2(24.0,0.0).rotated(hand.rest.get_rotation())
	var l1: float = upper.get_length()
	var l2: float = distal.length()
	var v: Vector2 = target-shoulder
	var distance: float = clampf(v.length(),absf(l1-l2)+0.01,l1+l2-0.01)
	var elbow: float = sign_elbow*acos(clampf((distance*distance-l1*l1-l2*l2)/(2.0*l1*l2),-1.0,1.0))
	var angle: float = v.angle()-atan2(l2*sin(elbow),l1+l2*cos(elbow))
	upper.rotation = angle-stage_transform(upper.get_parent()).get_rotation()
	fore.rotation = elbow-distal.angle()
	hand.rotation = hand.rest.get_rotation()

func solve_wrist(side: String,palm: Vector2,hand_angle: float,sign_elbow: float) -> void:
	var upper: Bone2D = bones[side+"Upper"]
	var fore: Bone2D = bones[side+"Fore"]
	var hand: Bone2D = bones[side+"Hand"]
	var target: Vector2 = palm-Vector2(24,0).rotated(hand_angle)
	var vector: Vector2 = target-stage_transform(upper).origin
	var l1: float = upper.get_length()
	var l2: float = fore.get_length()
	var distance: float = clampf(vector.length(),absf(l1-l2)+0.01,l1+l2-0.01)
	var elbow: float = sign_elbow*acos(clampf((distance*distance-l1*l1-l2*l2)/(2*l1*l2),-1,1))
	var angle: float = vector.angle()-atan2(l2*sin(elbow),l1+l2*cos(elbow))
	upper.rotation = angle-stage_transform(upper.get_parent()).get_rotation()
	fore.rotation = elbow
	hand.rotation = hand_angle-stage_transform(fore).get_rotation()


func place(node: Sprite2D,pivot: Vector2,point: Vector2,factor: float,angle: float=0.0) -> void:
	node.transform = Transform2D(angle,Vector2.ONE*factor,0.0,point) * Transform2D(0.0,-pivot)

func pose_action(clip: String,t: float) -> void:
	if new_head == null:
		return
	for bone: Bone2D in bones.values():
		bone.scale = Vector2.ONE
	set_parts(selected_parts)
	set_pose(clip if clip in ["arm_bend","blink","tail_bend"] else "arm_bend",t if clip in ["arm_bend","blink","tail_bend"] else 0.0)
	var working: bool = clip in ["boxer","racer","popstar"]
	if working:
		t = t/2.0 # Declared8second study; original three curves are unchanged.
	for cap: Sprite2D in joint_caps.values():
		cap.visible = working
	body.visible = not working
	action_body.visible = working
	for n: String in ["UpperArm","Forearm"]:
		polygons[n].visible = not working
	for n: String in action_parts:
		action_parts[n].visible = working
	for prop: Sprite2D in [glove,mitt,wheel,mic_lower,mic_upper,popstar_grip]:
		prop.visible = false
	for grip: Sprite2D in grip_pictures.values():
		grip.visible = false
	support.points = PackedVector2Array()
	active_contact = false
	prop_owner = "none"
	selected_view = "front"
	fixture_rest = Vector2.ZERO
	fixture_actual = Vector2.ZERO
	clothing_material.set_shader_parameter("action_enabled",working)
	if not working:
		return
	var skin: String = String(selected_parts.body)
	if not part_textures.has(skin+"_mask"):
		part_textures[skin+"_mask"] = load_png("res://art/"+skin+"_action_mask.png")
	clothing_material.set_shader_parameter("action_mask",part_textures[skin+"_mask"])
	for name: String in action_parts:
		var texture_key: String = skin+"_"+name
		if not part_textures.has(texture_key):
			part_textures[texture_key] = load_png("res://art/"+texture_key+".png")
		action_parts[name].texture = part_textures[texture_key]
	action_body.texture = garment_textures["anatomy"]
	action_body.material = clothing_material
	var approach: float = pulse(t,0.0,1.25,2.75,4.0) if clip == "boxer" else pulse(t,0.0,0.75,3.25,4.0)
	var left: Vector2 = rest_world["LeftHand"]*Vector2(24,0)
	var right: Vector2 = rest_world["RightHand"]*Vector2(24,0)
	if clip == "boxer":
		var jab: float = pulse(t,1.05,1.52,1.66,2.35)
		bones["Torso"].rotation += deg_to_rad(-1.4*jab)
		bones["TailA"].rotation += deg_to_rad(1.2*jab)
		bones["TailB"].rotation += deg_to_rad(-0.9*jab)
		left = left.lerp(Vector2(430,465-44*jab),approach)
		solve_wrist("Left",left,lerp_angle(rest_world["LeftHand"].get_rotation(),-PI/2.0,approach),-1.0)
		selected_view = "guard" if jab<0.35 else "jab" if t<1.85 else "palm"
		glove.texture = view_pictures["guard" if control == "frozen_view" else selected_view]
		var pivot: Vector2 = Vector2(256,250) if selected_view == "guard" else Vector2(256,280) if selected_view == "jab" else Vector2(340,260)
		var cuff: Vector2 = Vector2(151,417) if selected_view == "guard" else Vector2(256,437) if selected_view == "jab" else Vector2(340,413)
		var desired: Vector2 = stage_transform(bones["LeftHand"]).origin-socket("Left")
		place(glove,pivot,socket("Left"),desired.length()/(cuff-pivot).length(),desired.angle()-(cuff-pivot).angle())
		glove.visible = true
		action_parts["LeftHand"].visible = false
		fixture_rest = Vector2(430,390.1)
		place(mitt,Vector2(256,256),fixture_rest,0.20)
		mitt.visible = true
		fixture_actual = mitt.transform*Vector2(256,256)
		prop_target_left = glove.transform*pivot
		active_contact = t>=1.52 and t<=1.66
		prop_owner = "left_hand; mitt_fixed_support"
	elif clip == "racer":
		var turn: float = pulse(t,0.8,1.5,1.65,2.25)-pulse(t,2.0,2.6,2.75,3.3)
		var angle: float = deg_to_rad(14.0*turn)
		bones["Torso"].rotation += deg_to_rad(0.8*turn)
		bones["TailA"].rotation += deg_to_rad(-0.8*turn)
		fixture_rest = Vector2(538,520)
		place(wheel,Vector2(256,256),fixture_rest,0.40,angle)
		wheel.visible = true
		fixture_actual = wheel.transform*Vector2(256,256)
		prop_target_left = wheel.transform*Vector2(43,256)
		prop_target_right = wheel.transform*Vector2(469,256)
		left = left.lerp(prop_target_left,approach)
		right = right.lerp(prop_target_right,approach)
		solve_arm("Left",left,-1.0)
		solve_arm("Right",right,1.0)
		active_contact = t>=0.75 and t<=3.25
		prop_owner = "fixed_axle_two_hands_at_rim"
		if active_contact:
			for side: String in ["left","right"]:
				var grip: Sprite2D = grip_pictures[side]
				var is_left: bool = side == "left"
				var pivot: Vector2 = Vector2(96,236) if is_left else Vector2(173,259)
				var hand_name: String = "LeftHand" if is_left else "RightHand"
				var world_palm: Vector2 = socket("Left" if is_left else "Right")
				var desired: Vector2 = stage_transform(bones[hand_name]).origin-world_palm
				var native_wrist: Vector2 = Vector2(86,250) if is_left else Vector2(189,260)
				var native_direction: Vector2 = native_wrist-pivot
				place(grip,pivot,world_palm,desired.length()/native_direction.length(),desired.angle()-native_direction.angle())
				grip.visible = true
				action_parts["LeftHand" if is_left else "RightHand"].visible = false
		support.points = PackedVector2Array([Vector2(538,520),Vector2(538,665),Vector2(485,665),Vector2(590,665)])
	elif clip == "popstar":
		var adjust: float = pulse(t,1.0,1.6,2.1,2.8)
		bones["Torso"].rotation += deg_to_rad(-1.0*adjust)
		bones["TailA"].rotation += deg_to_rad(0.8*adjust)
		fixture_rest = Vector2(470,500)
		place(mic_lower,Vector2(256,270),fixture_rest,0.80)
		place(mic_upper,Vector2(256,270),fixture_rest,0.80,deg_to_rad(-8.0*adjust))
		mic_lower.visible = true
		mic_upper.visible = true
		fixture_actual = mic_lower.transform*Vector2(256,270)
		prop_target_left = mic_upper.transform*Vector2(256,270)
		left = left.lerp(prop_target_left,approach)
		solve_arm("Left",left,-1.0)
		active_contact = t>=0.75 and t<=3.25
		prop_owner = "stand_base_fixed; upper_mic_pivots_at_clamp; left_hand_support"
		if active_contact:
			var palm: Vector2 = socket("Left")
			var desired: Vector2 = stage_transform(bones["LeftHand"]).origin-palm
			var original_direction: Vector2 = Vector2(94,210)-Vector2(95,185)
			place(popstar_grip,Vector2(95,185),palm,desired.length()/original_direction.length(),desired.angle()-original_direction.angle())
			popstar_grip.visible = true
			action_parts["LeftHand"].visible = false
	if control == "grip_slip":
		if clip == "racer":
			wheel.position.x += 28.0
			prop_target_left = wheel.transform*Vector2(43,256)
		elif clip == "popstar":
			mic_upper.position.x += 28.0
			prop_target_left = mic_upper.transform*Vector2(256,270)
		else:
			glove.position.x += 28.0
			prop_target_left.x += 28.0
	if control == "fixture_drift":
		fixture_actual.x += 28.0
		if clip == "racer": wheel.position.x += 28.0
		elif clip == "popstar": mic_lower.position.x += 28.0
		else: mitt.position.x += 28.0
	if control == "missing_arm":
		action_parts["RightFore"].visible = false
	if control == "original_underlay":
		body.visible = true
		body.texture = original_body_texture
		body.material = null
	if control == "identity_scale":
		bones["Head"].scale = Vector2(1.2,0.8)
	else:
		bones["Head"].scale = Vector2.ONE
	label.text = clip+" | "+selected_view+" | "+control+" | SOURCE ONLY"

func record() -> Dictionary:
	var rec: Dictionary = state_record()
	rec["action"] = action
	rec["parts"] = selected_parts.duplicate(true)
	rec["contact_active"] = active_contact
	rec["left_grip"] = [socket("Left").x,socket("Left").y]
	rec["right_grip"] = [socket("Right").x,socket("Right").y]
	rec["left_target"] = [prop_target_left.x,prop_target_left.y]
	rec["right_target"] = [prop_target_right.x,prop_target_right.y]
	rec["contact_error"] = maxf(socket("Left").distance_to(prop_target_left),socket("Right").distance_to(prop_target_right) if action == "racer" else 0.0) if active_contact else 0.0
	var measured_fixture: Vector2 = wheel.transform*Vector2(256,256) if action == "racer" else mic_lower.transform*Vector2(256,270) if action == "popstar" else mitt.transform*Vector2(256,256)
	rec["fixture_error"] = measured_fixture.distance_to(fixture_rest) if action in ["boxer","racer","popstar"] else 0.0
	rec["fixture_actual"] = [measured_fixture.x,measured_fixture.y]
	rec["fixture_expected"] = [fixture_rest.x,fixture_rest.y]
	if action == "boxer" and active_contact:
		var knuckle: Vector2 = glove.transform*Vector2(256,78)
		rec["knuckle_mitt_error"] = knuckle.distance_to(mitt.transform*Vector2(256,256))
		rec["painted_wrist_error"] = (glove.transform*Vector2(256,437)).distance_to(stage_transform(bones["LeftHand"]).origin)
	if action == "racer" and active_contact:
		var left_wrist: Vector2 = grip_pictures["left"].transform*Vector2(86,250)
		var right_wrist: Vector2 = grip_pictures["right"].transform*Vector2(189,260)
		rec["painted_wrist_error"] = maxf(left_wrist.distance_to(stage_transform(bones["LeftHand"]).origin),right_wrist.distance_to(stage_transform(bones["RightHand"]).origin))
	if action == "popstar" and active_contact:
		rec["painted_wrist_error"] = (popstar_grip.transform*Vector2(94,210)).distance_to(stage_transform(bones["LeftHand"]).origin)
	rec["view"] = selected_view
	rec["owner"] = prop_owner
	rec["control"] = control
	rec["underlay_visible"] = body.visible and action in ["boxer","racer","popstar"]
	return rec

func _process(delta: float) -> void:
	if run_action and new_head != null:
		elapsed = fmod(elapsed+delta,duration(action))
		pose_action(action,elapsed)

func _input(event: InputEvent) -> void:
	if new_head == null or not event is InputEventKey:
		return
	var key: InputEventKey = event
	if not key.pressed or key.echo:
		return
	if key.keycode == KEY_SPACE:
		run_action = not run_action
	if key.keycode in [KEY_1,KEY_2,KEY_3,KEY_4,KEY_5,KEY_6]:
		action = ["boxer","racer","popstar","arm_bend","blink","tail_bend"][key.keycode-KEY_1]
		elapsed = 0.0
		if action in ["boxer","racer","popstar"]:
			set_parts({"head":action,"body":action,"tail":action})
	if key.keycode in [KEY_LEFT,KEY_RIGHT]:
		run_action = false
		elapsed = clampf(elapsed+(-1.0 if key.keycode == KEY_LEFT else 1.0)/30.0,0.0,duration(action))
	if key.keycode == KEY_O:
		set_parts({"head":"original","body":"original","tail":"original"})
		action = "arm_bend"
	for slot: String in ["head","body","tail"]:
		if key.keycode == {"head":KEY_H,"body":KEY_J,"tail":KEY_K}[slot]:
			var options: Array[String] = ["original","ballet","magician","boxer","racer","popstar"]
			set_parts({slot:options[(options.find(String(selected_parts[slot]))+1)%options.size()]})
	pose_action(action,elapsed)
