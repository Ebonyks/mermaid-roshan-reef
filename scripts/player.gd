extends Node3D
# Roshan player: swim / air / land movement on the ReefPhysics engine,
# procedural 26-bone swim animation.

const WATER_TOP := 58.0
const WORLD_R := 270.0

const SWIM_ACCEL := 43.7      # thrust, u/s^2 (1.15x speed, x2 on beans)
const TURN_RATE := 1.8        # rad/s
const JUMP_WATER := 16.0      # dolphin-kick boost / surface breach impulse
const JUMP_LAND := 12.0       # Sky-Lagoon hop
const JUMP_COOL := 0.4

var yaw := 0.0
var vel := Vector3.ZERO
var body: ReefPhysics.Body
var world: ReefPhysics.World
var med_water: ReefPhysics.Medium
var med_air: ReefPhysics.Medium
var med_land: ReefPhysics.Medium
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
var skin_sprite: Sprite3D = null  # billboard used for alternative full skins
var skin_sparkles: CPUParticles3D = null  # fairy sparkle trail for sparkly skins
var skin_id := "classic"
var skin_t := 0.0

func _ready() -> void:
	position = Vector3(0, 26, 0)
	med_water = ReefPhysics.water_medium()
	med_air = ReefPhysics.air_medium()
	med_land = ReefPhysics.land_medium()
	body = ReefPhysics.Body.new(med_water, med_air)
	world = ReefPhysics.World.new()
	# (Roshan never collides with Jolt bodies directly — her motion stays
	# analytic; main._physics_process couples her body to the rigid props
	# via explicit contact + swim-wake impulses.)
	var glb: PackedScene = load("res://assets/characters/roshan.glb") as PackedScene
	if glb != null:
		var inst: Node3D = glb.instantiate()
		inst.scale = Vector3.ONE * 1.55
		inst.position.y = -1.6
		add_child(inst)
		model_root = inst
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
					m2.rim_enabled = true          # cheap fresnel sheen on Roshan's edges
					m2.rim = 0.35
					m2.rim_tint = 0.4
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

# Point the shared physics world at wherever Roshan currently is: the open
# reef (real water surface, seabed heightfield), the Sky Lagoon (solid land —
# air/ground rules, terrain heightfield), or a cutaway arena (flat floor,
# cosy dome, all-water). Field writes only; no allocations.
func _configure_world(m: Node) -> void:
	if String(m.game) != "":
		var ap: Vector3 = m.arena_center
		world.center = ap
		world.bound_r = float(m.arena_dome)
		world.ceil_y = ap.y + float(m.arena_ceil)
		world.solids = m.arena_solids if "arena_solids" in m else []
		if "lagoon_floor" in m and m.lagoon_floor:
			# Sky Lagoon is LAND: gravity holds Roshan to the rolling hills,
			# releasing the stick stops her, SPACE is a hop instead of a kick
			world.floor_fn = Callable(m, "lagoon_h")
			world.floor_y = -INF
			world.floor_pad = 2.0
			world.water_y = -INF
			body.air = med_land
			body.water = med_land
		else:
			world.floor_fn = Callable()
			world.floor_y = ap.y + 2.5
			world.floor_pad = 0.0
			world.water_y = INF   # cutaway arenas are dream-water throughout
			body.air = med_water
			body.water = med_water
	else:
		world.center = Vector3.ZERO
		world.bound_r = WORLD_R
		world.ceil_y = WATER_TOP + 14.0   # safety lid well above any breach arc
		world.solids = m.solids if "solids" in m else []
		world.floor_fn = Callable(m, "seabed_y")
		world.floor_y = -INF
		world.floor_pad = 3.0
		world.water_y = WATER_TOP         # a real surface: jumps can breach it
		body.water = med_water
		body.air = med_air

func _rot_bone(bname: String, axis: Vector3, angle: float) -> void:
	var bi: int = bone_idx.get(bname, -1)
	if bi < 0 or not rest.has(bname):
		return
	var base: Transform3D = rest[bname]
	skel.set_bone_pose_rotation(bi, base.basis.get_rotation_quaternion() * Quaternion(axis, angle))

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

	var m: Node = get_parent()
	_configure_world(m)

	jump_cool -= delta
	if jump_held and jump_cool <= 0.0 and body.state != ReefPhysics.ST_AIR:
		jump_cool = JUMP_COOL
		vel.y = JUMP_WATER if body.state == ReefPhysics.ST_SWIM else JUMP_LAND

	yaw += turn * TURN_RATE * delta
	var dir := Vector3(sin(yaw), 0.0, cos(yaw))
	var smult := 1.0
	if "speed_mult" in m0:
		smult = float(m0.speed_mult)
	# probes and cutscenes write position/vel directly, so the body syncs
	# through the node's fields rather than owning them
	body.pos = position
	body.vel = vel
	ReefPhysics.step(body, world, dir * fwd * SWIM_ACCEL * smult, delta)
	position = body.pos
	vel = body.vel
	if body.splashed != 0 and m.has_method("_sparkle_burst"):
		# breaching / re-entering the ocean surface
		m._sparkle_burst(Vector3(position.x, WATER_TOP - 0.2, position.z), Color(0.55, 0.82, 1.0))

	rotation.y = yaw + PI

	if fwd != 0.0 or turn != 0.0 or jump_held:
		idle_t = 0.0
	else:
		idle_t += delta

	var speed: float = vel.length()
	swim_phase += delta * (2.2 + speed * 0.9)
	var amp: float = 0.10 + minf(speed * 0.03, 0.26)
	var kick: float = sin(swim_phase)
	if skel != null:
		for i in range(8):
			var ph: float = swim_phase - float(i) * 0.45
			var grow: float = 0.12 + 0.88 * pow(float(i) / 7.0, 1.5)
			_rot_bone("tail%d" % (i + 1), Vector3.RIGHT, sin(ph) * amp * grow)
		var fin_ph: float = swim_phase - 3.6
		_rot_bone("finTop", Vector3.RIGHT, sin(fin_ph - 0.25) * amp * 0.9)
		_rot_bone("finBot", Vector3.RIGHT, sin(fin_ph - 0.55) * amp * 0.9)
		_rot_bone("spine1", Vector3.RIGHT, -kick * amp * 0.16)
		_rot_bone("chest", Vector3.RIGHT, -sin(swim_phase - 0.4) * amp * 0.12)
		_rot_bone("neck", Vector3.RIGHT, sin(swim_phase - 0.7) * amp * 0.06)
		var idle_head: float = 0.0
		if idle_t > 6.0:
			idle_head = sin(Time.get_ticks_msec() / 1100.0) * 0.09
		_rot_bone("head", Vector3.BACK, sin(swim_phase * 0.5 + 0.6) * 0.02 + idle_head)
		_rot_bone("hair1", Vector3.BACK, sin(swim_phase * 0.65 + 0.8) * 0.045)
		_rot_bone("hair2", Vector3.BACK, sin(swim_phase * 0.65 + 0.25) * 0.065)
		_rot_bone("hair3", Vector3.BACK, sin(swim_phase * 0.65 - 0.35) * 0.085)
		_rot_bone("armU", Vector3.RIGHT, sin(swim_phase * 0.5) * 0.35 + 0.18)
		_rot_bone("armF", Vector3.RIGHT, sin(swim_phase * 0.5 - 0.6) * 0.30 + 0.22)
		_rot_bone("armU2", Vector3.RIGHT, sin(swim_phase * 0.5 + PI * 0.8) * 0.35 + 0.18)
		_rot_bone("armF2", Vector3.RIGHT, sin(swim_phase * 0.5 + PI * 0.8 - 0.6) * 0.30 + 0.22)
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
