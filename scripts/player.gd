extends Node3D
# Roshan player: floaty swim + jump physics, procedural 26-bone swim animation.

const WATER_TOP := 58.0
const WORLD_R := 270.0

var yaw := 0.0
var vel := Vector3.ZERO
var swim_phase := 0.0
var jump_cool := 0.0
var idle_t := 0.0
var cam: Camera3D
var cam_back := 16.0   # chase distance (reduced indoors so the camera does not clip walls)
var cam_high := 6.5    # chase height
var skel: Skeleton3D
var bone_idx := {}
var rest := {}
var warned := false
var model_root: Node3D = null     # the 3D Roshan model (shown for the "classic" skin)
var model_v2 := false             # true = the rebuilt true-3D model (roshan_v2.glb)
var hair_sim: HairSim = null      # spring physics for hair_SS_J strand chains (v2)
var skin_sprite: Sprite3D = null  # billboard used for alternative full skins
var skin_sparkles: CPUParticles3D = null  # fairy sparkle trail for sparkly skins
var skin_id := "classic"
var skin_t := 0.0
# WW swim wake: ribbon contrail rebuilt each frame from recent tail positions,
# plus velocity-aligned dash particles that only appear at sprint speed
var trail_node: MeshInstance3D
var trail_mesh: ImmediateMesh
var trail_pts: Array = []       # front = newest; {p: Vector3, s: strength}
var trail_sample := 0.0
var trail_enabled := true       # cleared by main._apply_quality in speedy mode
var speed_lines: GPUParticles3D
var speed_pm: ParticleProcessMaterial

func _ready() -> void:
	position = Vector3(0, 26, 0)
	# Prefer the rebuilt true-3D model (multi-view Meshy + fitted rig, 2026-07-11);
	# the old flat-card model stays on disk as an instant fallback.
	var glb: PackedScene = null
	if ResourceLoader.exists("res://assets/characters/roshan_v2.glb"):
		glb = load("res://assets/characters/roshan_v2.glb") as PackedScene
		model_v2 = glb != null
	if glb == null:
		glb = load("res://assets/characters/roshan.glb") as PackedScene
	if glb != null:
		var inst: Node3D = glb.instantiate()
		if model_v2:
			# v2 is 1.9 units tall centred at origin; match the old visual size
			inst.scale = Vector3.ONE * 3.7
			inst.position.y = 0.89
		else:
			inst.scale = Vector3.ONE * 1.55
			inst.position.y = -1.6
		add_child(inst)
		model_root = inst
		if model_v2:
			_flatten_materials(inst)   # keep its own textures; kill specular/rim
		else:
			_upgrade_texture(inst)
		skel = _find_skeleton(inst)
		if skel != null:
			for n in ["root", "spine1", "chest", "neck", "head", "hair1", "hair2", "hair3",
					"hairL1", "hairL2", "armU", "armF", "hand", "armU2", "armF2", "hand2",
					"tail1", "tail2", "tail3", "tail4", "tail5", "tail6", "tail7", "tail8",
					"finTop", "finBot"]:
				var bi: int = skel.find_bone(n)
				bone_idx[n] = bi
				if bi >= 0:
					rest[n] = skel.get_bone_pose(bi)
			if model_v2:
				hair_sim = HairSim.new()
				add_child(hair_sim)
				hair_sim.setup(self)   # no-op if no hair_SS_J bones
	# billboard sprite used when an alternative full skin is worn (hidden by default)
	# pixel_size sized so the 707px-tall art ≈ the 7-unit classic model
	skin_sprite = Sprite3D.new()
	skin_sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	skin_sprite.pixel_size = 0.0100
	skin_sprite.position = Vector3(0, 0.6, 0)
	skin_sprite.visible = false
	add_child(skin_sprite)
	# fairy sparkle trail (only emits while a sparkly skin is worn)
	skin_sparkles = CPUParticles3D.new()
	skin_sparkles.amount = 28
	skin_sparkles.lifetime = 1.5
	skin_sparkles.local_coords = false
	skin_sparkles.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
	skin_sparkles.emission_sphere_radius = 2.2
	skin_sparkles.gravity = Vector3(0, 0.5, 0)
	skin_sparkles.initial_velocity_min = 0.2
	skin_sparkles.initial_velocity_max = 1.0
	skin_sparkles.scale_amount_min = 0.06
	skin_sparkles.scale_amount_max = 0.2
	skin_sparkles.hue_variation_min = -0.5
	skin_sparkles.hue_variation_max = 0.5
	var spm := BoxMesh.new(); spm.size = Vector3(0.14, 0.14, 0.14)
	skin_sparkles.mesh = spm
	var spmat := StandardMaterial3D.new()
	spmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	spmat.albedo_color = Color(1.0, 0.85, 0.95)
	spmat.emission_enabled = true; spmat.emission = Color(1.0, 0.8, 0.95); spmat.emission_energy_multiplier = 1.5
	skin_sparkles.material_override = spmat
	skin_sparkles.position = Vector3(0, 1.0, 0)
	skin_sparkles.emitting = false
	add_child(skin_sparkles)
	# wake ribbon (top_level so its points live in world space)
	trail_mesh = ImmediateMesh.new()
	trail_node = MeshInstance3D.new()
	trail_node.mesh = trail_mesh
	trail_node.top_level = true
	var tm := StandardMaterial3D.new()
	tm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	tm.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	tm.vertex_color_use_as_albedo = true
	tm.cull_mode = BaseMaterial3D.CULL_DISABLED
	tm.disable_receive_shadows = true
	trail_node.material_override = tm
	trail_node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(trail_node)
	# speed-line dashes: thin boxes aligned to their velocity, streaming past her
	speed_lines = GPUParticles3D.new()
	speed_lines.amount = 36
	speed_lines.lifetime = 0.55
	speed_lines.local_coords = false
	speed_lines.emitting = false
	speed_pm = ParticleProcessMaterial.new()
	speed_pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	speed_pm.emission_box_extents = Vector3(3.5, 2.5, 3.5)
	speed_pm.particle_flag_align_y = true
	speed_pm.gravity = Vector3.ZERO
	speed_pm.spread = 8.0
	speed_lines.process_material = speed_pm
	var slm := BoxMesh.new()
	slm.size = Vector3(0.05, 1.6, 0.05)
	speed_lines.draw_pass_1 = slm
	var smat := StandardMaterial3D.new()
	smat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	smat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	smat.albedo_color = Color(0.75, 0.95, 1.0, 0.55)
	speed_lines.material_override = smat
	speed_lines.position = Vector3(0, 1.0, 0)
	add_child(speed_lines)
	cam = Camera3D.new()
	cam.fov = 60.0
	get_parent().add_child.call_deferred(cam)

func set_skin(id: String, tex_path: String) -> void:
	# "classic" shows the 3D model; any other id swaps to a full-skin billboard
	skin_id = id
	var on_skin: bool = not (id == "classic" or tex_path == "")
	if on_skin:
		if skin_sprite != null:
			skin_sprite.texture = load(tex_path)
			skin_sprite.visible = true
			skin_sprite.scale = Vector3.ONE
		if model_root != null:
			model_root.visible = false
	else:
		if model_root != null:
			model_root.visible = true
		if skin_sprite != null:
			skin_sprite.visible = false
	if skin_sparkles != null:
		skin_sparkles.emitting = on_skin

func _flatten_materials(node: Node) -> void:
	# v2 model: keep the Meshy-baked textures but light them flat and evenly —
	# same reasoning as _upgrade_texture (specular/rim streaks read as glitches
	# on painted faces when the camera moves).
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		if mi.mesh != null:
			for si in range(mi.mesh.get_surface_count()):
				var m: Material = mi.mesh.surface_get_material(si)
				if m is BaseMaterial3D:
					var m2: BaseMaterial3D = (m as BaseMaterial3D).duplicate()
					m2.rim_enabled = false
					m2.roughness = 1.0
					m2.metallic = 0.0
					m2.metallic_specular = 0.0
					# self-lit fill: true-3D curvature goes murky in the dim
					# underwater scene; the painted look wants even brightness
					# (the old flat card was effectively camera-lit).
					m2.emission_enabled = true
					m2.emission_texture = m2.albedo_texture
					m2.emission = Color(0.05, 0.05, 0.05)
					mi.set_surface_override_material(si, m2)
	for c in node.get_children():
		_flatten_materials(c)

func _upgrade_texture(node: Node) -> void:
	# swap embedded 512px texture for the 2K re-bake from the source illustration
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		if mi.mesh != null:
			for si in range(mi.mesh.get_surface_count()):
				var m: Material = mi.mesh.surface_get_material(si)
				if m is BaseMaterial3D:
					var m2: BaseMaterial3D = (m as BaseMaterial3D).duplicate()
					m2.albedo_texture = load("res://assets/characters/roshan_tex_2k.webp")
					# NO rim / NO specular: on the near-flat painted face, moving cameras
					# (cutscenes) sweep fresnel + specular streaks across the painted EYES,
					# which reads as the eye glitch. Painted texture must light flat + evenly.
					m2.rim_enabled = false
					m2.roughness = 1.0
					m2.metallic = 0.0
					m2.metallic_specular = 0.0
					mi.set_surface_override_material(si, m2)
	for c in node.get_children():
		_upgrade_texture(c)

func _find_skeleton(node: Node) -> Skeleton3D:
	if node is Skeleton3D:
		return node
	for c in node.get_children():
		var r := _find_skeleton(c)
		if r != null:
			return r
	return null

func attach_bone(n: Node3D, bone: String) -> bool:
	if skel == null:
		return false
	var bi: int = skel.find_bone(bone)
	if bi < 0:
		return false
	var ba := BoneAttachment3D.new()
	ba.bone_name = bone
	skel.add_child(ba)
	ba.add_child(n)
	return true

func _rot_bone(bname: String, axis: Vector3, angle: float) -> void:
	# Rotate a bone about a MODEL-space axis, composed after its rest rotation.
	# The old card rig has identity rests (axis passes through unchanged); the
	# v2 rig's bones carry Blender rest orientations, so the axis must be
	# brought into the bone's local frame first.
	var bi: int = bone_idx.get(bname, -1)
	if bi < 0 or not rest.has(bname):
		return
	var base: Transform3D = rest[bname]
	var rq: Quaternion = base.basis.get_rotation_quaternion()
	var local_axis: Vector3 = (rq.inverse() * axis).normalized()
	skel.set_bone_pose_rotation(bi, rq * Quaternion(local_axis, angle))

func _process(delta: float) -> void:
	var _m0: Node = get_parent()
	if "intro_active" in _m0 and _m0.intro_active:
		return
	if "wardrobe_layer" in _m0 and _m0.wardrobe_layer != null:
		return   # frozen while the dress-up screen is open
	if "game" in _m0 and (String(_m0.game) == "slide" or String(_m0.game) == "fairyshoot"):
		return   # the slide / fairy-shooter minigames drive the player + camera themselves
	if "l2_cutscene_t" in _m0 and _m0.l2_cutscene_t >= 0.0:
		if cam != null and cam.is_inside_tree():
			cam.look_at(position + Vector3(0, 1.5, 0))
		return
	var fwd := 0.0
	var turn := 0.0
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W):
		fwd += 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		fwd -= 0.6
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		turn += 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		turn -= 1.0
	var jx: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	var jy: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.2:
		turn -= jx
	if absf(jy) > 0.2:
		fwd -= jy
	var m0: Node = get_parent()
	if "touch_ui" in m0 and m0.touch_ui != null:
		var tv: Vector2 = m0.touch_ui.stick_vec
		if absf(tv.x) > 0.15:
			turn -= tv.x
		if absf(tv.y) > 0.15:
			fwd -= tv.y
	var jump_held: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_joy_button_pressed(0, JOY_BUTTON_A)
	if "touch_ui" in m0 and m0.touch_ui != null and m0.touch_ui.action_down:
		jump_held = true

	jump_cool -= delta
	if jump_held and jump_cool <= 0.0:
		jump_cool = 0.4
		vel.y = 16.0
		if m0 != null and m0.has_method("on_player_jump"):
			m0.on_player_jump(position)   # surface splash ring near WATER_TOP

	yaw += turn * 1.8 * delta
	var dir := Vector3(sin(yaw), 0.0, cos(yaw))
	var smult := 1.0
	if "speed_mult" in m0:
		smult = float(m0.speed_mult)
	vel += dir * fwd * 43.7 * smult * delta      # 1.15x speed (x2 on beans)
	vel.y -= 13.0 * delta                # 1.3x weight
	vel *= pow(0.18, delta)
	position += vel * delta

	var m: Node = get_parent()
	if String(m.game) != "":
		# cutaway arena bounds: flat floor, cosy dome (configurable per arena)
		var ap: Vector3 = m.arena_center
		var dome: float = m.arena_dome
		var ceil_h: float = m.arena_ceil
		var floor_a: float = ap.y + 2.5
		if "lagoon_floor" in m and m.lagoon_floor:
			# Sky Lagoon: rest on the rolling-hill terrain; dip down into the river valleys
			floor_a = m.lagoon_h(position.x, position.z) + 2.0
		elif m.has_method("arena_floor_h"):
			# arenas can carve local dips below the flat floor (castle basement stairwell)
			floor_a = m.arena_floor_h(position) + 2.5
		if position.y < floor_a:
			position.y = floor_a
			vel.y = maxf(0.0, vel.y)
		if position.y > ap.y + ceil_h:
			position.y = ap.y + ceil_h
			vel.y = minf(0.0, vel.y)
		var da: float = Vector2(position.x - ap.x, position.z - ap.z).length()
		if da > dome:
			position.x = ap.x + (position.x - ap.x) * dome / da
			position.z = ap.z + (position.z - ap.z) * dome / da
		# soft-collision against arena walls (boxes) and columns (cylinders):
		# eject Roshan and cancel the inward velocity so he slides along the face.
		if "arena_solids" in m:
			for s in m.arena_solids:
				if position.y < s.y0 or position.y > s.y1:
					continue
				if s.box:
					var lx: float = position.x - s.cx
					var lz: float = position.z - s.cz
					if absf(lx) < s.hx and absf(lz) < s.hz:
						# inside the footprint — eject along the shallowest horizontal axis
						if s.hx - absf(lx) < s.hz - absf(lz):
							var sgx: float = signf(lx) if lx != 0.0 else 1.0
							position.x = s.cx + sgx * s.hx
							if vel.x * sgx < 0.0:
								vel.x = 0.0
						else:
							var sgz: float = signf(lz) if lz != 0.0 else 1.0
							position.z = s.cz + sgz * s.hz
							if vel.z * sgz < 0.0:
								vel.z = 0.0
				else:
					var dx: float = position.x - s.x
					var dz: float = position.z - s.z
					var dd: float = sqrt(dx * dx + dz * dz)
					if dd < s.r and dd > 0.001:
						var nx: float = dx / dd
						var nz: float = dz / dd
						position.x = s.x + nx * s.r
						position.z = s.z + nz * s.r
						var vn: float = vel.x * nx + vel.z * nz
						if vn < 0.0:
							vel.x -= vn * nx
							vel.z -= vn * nz
	else:
		var floor_y: float = m.seabed_y(position.x, position.z) + 3.0
		if position.y < floor_y:
			position.y = floor_y
			vel.y = maxf(0.0, vel.y)
		if position.y > WATER_TOP - 3.0:
			position.y = WATER_TOP - 3.0
			vel.y = minf(0.0, vel.y)
		var d: float = Vector2(position.x, position.z).length()
		if d > WORLD_R:
			position.x *= WORLD_R / d
			position.z *= WORLD_R / d
		# soft-collision against big structures (rock outcrops, shipwreck):
		# push Roshan out of any cylinder he enters and cancel inward velocity
		# so he slides along the surface instead of jittering or stopping dead.
		if "solids" in m:
			for s in m.solids:
				if position.y < s.y0 or position.y > s.y1:
					continue
				var dx: float = position.x - s.x
				var dz: float = position.z - s.z
				var dd: float = sqrt(dx * dx + dz * dz)
				if dd < s.r and dd > 0.001:
					var nx: float = dx / dd
					var nz: float = dz / dd
					position.x = s.x + nx * s.r
					position.z = s.z + nz * s.r
					var vn: float = vel.x * nx + vel.z * nz
					if vn < 0.0:
						vel.x -= vn * nx
						vel.z -= vn * nz

	rotation.y = yaw + PI

	if fwd != 0.0 or turn != 0.0 or jump_held:
		idle_t = 0.0
	else:
		idle_t += delta

	var speed: float = vel.length()
	_tick_wake(delta, speed)
	swim_phase += delta * (2.2 + speed * 0.9)
	var amp: float = 0.10 + minf(speed * 0.03, 0.26)
	var kick: float = sin(swim_phase)
	if skel != null:
		# Swing axis depends on the model:
		#  * v2 true-3D model (faces -Z): dolphin-kick pitch + arm paddling are
		#    rotations about model X (RIGHT).
		#  * old flat-card model (geometry in the XY plane): swings must stay
		#    in-plane, i.e. about model Z (BACK) — out-of-plane rotations shear
		#    the card edge-on and axially twist the X-aligned tail bones.
		var A: Vector3 = Vector3.RIGHT if model_v2 else Vector3.BACK
		for i in range(8):
			var ph: float = swim_phase - float(i) * 0.45
			var grow: float = 0.12 + 0.88 * pow(float(i) / 7.0, 1.5)
			_rot_bone("tail%d" % (i + 1), A, sin(ph) * amp * grow)
		var fin_ph: float = swim_phase - 3.6
		_rot_bone("finTop", A, sin(fin_ph - 0.25) * amp * 0.9)
		_rot_bone("finBot", A, sin(fin_ph - 0.55) * amp * 0.9)
		_rot_bone("spine1", A, -kick * amp * 0.16)
		_rot_bone("chest", A, -sin(swim_phase - 0.4) * amp * 0.12)
		_rot_bone("neck", A, sin(swim_phase - 0.7) * amp * 0.06)
		var idle_head: float = 0.0
		if idle_t > 6.0:
			idle_head = sin(Time.get_ticks_msec() / 1100.0) * 0.09
		_rot_bone("head", Vector3.BACK, sin(swim_phase * 0.5 + 0.6) * 0.02 + idle_head)
		if not model_v2:
			# card model: single-chain hair sway (v2 hair belongs to HairSim)
			_rot_bone("hair1", Vector3.BACK, sin(swim_phase * 0.65 + 0.8) * 0.045)
			_rot_bone("hair2", Vector3.BACK, sin(swim_phase * 0.65 + 0.25) * 0.065)
			_rot_bone("hair3", Vector3.BACK, sin(swim_phase * 0.65 - 0.35) * 0.085)
			_rot_bone("hairL1", Vector3.BACK, sin(swim_phase * 0.65 + 0.5) * 0.05)
			_rot_bone("hairL2", Vector3.BACK, sin(swim_phase * 0.65 - 0.1) * 0.075)
		# Arms: gentle paddle. Amplitude scales with speed (near-still arms when
		# idle), no constant offset (rest = the authored pose), and the far arm
		# trails the near arm slightly. Forearm follows with a small lag.
		var arm_amp: float = 0.06 + minf(speed * 0.02, 0.20)
		var arm_ph: float = swim_phase * 0.5
		_rot_bone("armU", A, sin(arm_ph) * arm_amp)
		_rot_bone("armF", A, sin(arm_ph - 0.5) * arm_amp * 0.7)
		_rot_bone("armU2", A, sin(arm_ph - 0.35) * arm_amp)
		_rot_bone("armF2", A, sin(arm_ph - 0.85) * arm_amp * 0.7)
	elif not warned:
		warned = true
		push_warning("Roshan skeleton not found in roshan.glb - check import")

	# full-skin billboard: gentle idle bob + a wing-flap squash so it feels alive without bones
	if skin_sprite != null and skin_sprite.visible:
		skin_t += delta * (2.2 + speed * 0.6)
		skin_sprite.position.y = 0.6 + sin(skin_t) * 0.3
		var flap: float = sin(skin_t * 2.4)               # quicker beat = wings flapping
		skin_sprite.scale = Vector3(1.0 + flap * 0.05, 1.0 - flap * 0.03, 1.0)

	if cam != null and cam.is_inside_tree():
		var target := position + Vector3(-sin(yaw) * cam_back, cam_high, -cos(yaw) * cam_back)
		cam.position = cam.position.lerp(target, 1.0 - pow(0.001, delta))
		cam.look_at(position + Vector3(0, 1.5, 0))

func _tick_wake(delta: float, speed: float) -> void:
	# WW motion language: contrail ribbon from the tail + dash particles at sprint speed
	var strength: float = clampf((speed - 7.0) / 16.0, 0.0, 1.0)
	if speed_lines != null:
		var sprinting: bool = trail_enabled and speed > 26.0
		speed_lines.emitting = sprinting
		if sprinting:
			speed_pm.direction = -vel.normalized()
			speed_pm.initial_velocity_min = speed * 0.5
			speed_pm.initial_velocity_max = speed * 0.8
	if trail_node == null:
		return
	if not trail_enabled:
		if trail_pts.size() > 0:
			trail_pts.clear()
			trail_mesh.clear_surfaces()
		return
	trail_sample -= delta
	if trail_sample <= 0.0:
		trail_sample = 0.05
		if strength > 0.01:
			var tail: Vector3 = position + Vector3(-sin(yaw), 0.0, -cos(yaw)) * 1.8 + Vector3(0, -0.4, 0)
			trail_pts.push_front({"p": tail, "s": strength})
			if trail_pts.size() > 22:
				trail_pts.pop_back()
		elif trail_pts.size() > 0:
			trail_pts.pop_back()   # ribbon dissolves from the tail when she slows
	_rebuild_trail()

func _rebuild_trail() -> void:
	trail_mesh.clear_surfaces()
	var n: int = trail_pts.size()
	if n < 3:
		return
	var eye: Vector3 = position + Vector3(0, 10, 10)
	if cam != null and cam.is_inside_tree():
		eye = cam.global_position
	trail_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
	for i in range(n):
		var pt: Vector3 = trail_pts[i]["p"]
		var s: float = trail_pts[i]["s"]
		var seg: Vector3 = (trail_pts[mini(i + 1, n - 1)]["p"] as Vector3) - (trail_pts[maxi(i - 1, 0)]["p"] as Vector3)
		if seg.length_squared() < 0.0001:
			seg = Vector3(sin(yaw), 0, cos(yaw))
		# camera-facing ribbon: widen perpendicular to both the path and the view
		var side: Vector3 = seg.normalized().cross((eye - pt).normalized())
		if side.length_squared() < 0.0001:
			side = Vector3.UP
		side = side.normalized()
		var u: float = float(i) / float(n - 1)
		var wdt: float = s * (0.12 + 0.85 * pow(sin(PI * u), 0.7))
		var a: float = (1.0 - u) * 0.5 * s
		var colr := Color(0.62 * a, 0.9 * a, 1.0 * a)   # additive: fade encoded in RGB
		trail_mesh.surface_set_color(colr)
		trail_mesh.surface_add_vertex(pt + side * wdt)
		trail_mesh.surface_set_color(colr)
		trail_mesh.surface_add_vertex(pt - side * wdt)
	trail_mesh.surface_end()
