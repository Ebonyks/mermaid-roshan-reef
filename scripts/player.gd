extends Node3D
# Roshan player: floaty swim + jump physics, procedural 26-bone swim animation.

const WATER_TOP := 58.0
const WORLD_R := 270.0

func joy_axis(axis: int) -> float:
	# delegate to main's gamepad layer (multi-device + raw fallback for pads
	# Godot has no SDL mapping for, like the 8BitDo Lite family)
	var m: Node = get_parent()
	if m != null and m.has_method("joy_axis"):
		return m.joy_axis(axis)
	return Input.get_joy_axis(0, axis)

func joy_pressed(btn: int) -> bool:
	var m: Node = get_parent()
	if m != null and m.has_method("joy_pressed"):
		return m.joy_pressed(btn)
	return Input.is_joy_button_pressed(0, btn)

var yaw := 0.0
var vel := Vector3.ZERO
var swim_phase := 0.0
var jump_cool := 0.0
var idle_t := 0.0

# ---- R2-C verb layer: authored gestures blended over the procedural swim ----
# One writer owns every bone. A verb samples its keyframes and slerps OVER
# whatever the swim just wrote (weight ramps in/out), so entry and exit
# blends are free and the two systems can never fight. Angles in radians on
# ONE axis per bone per verb — same idiom as the swim's _rot_bone calls.
# "sig" = [signature bone, min radians] so probe_verbs.gd can SEE each verb.
var verb := ""
var verb_t := 0.0
var idle_verb_cool := 0.0

const VERB_LIB := {
	"wave": {"len": 2.6, "sig": ["armU2", 1.2], "tracks": {
		"armU2": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.5, -1.9], [2.1, -1.9], [2.6, 0.2]]},
		"armF2": {"axis": Vector3.BACK, "keys": [[0.0, 0.0], [0.6, 0.55], [0.9, -0.45], [1.2, 0.55], [1.5, -0.45], [1.8, 0.55], [2.2, 0.0]]},
		"head": {"axis": Vector3.BACK, "keys": [[0.0, 0.0], [0.7, 0.16], [2.0, 0.16], [2.6, 0.0]]},
	}},
	"cheer": {"len": 2.2, "sig": ["armU", 1.2], "tracks": {
		"armU": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.4, -2.1], [1.7, -2.1], [2.2, 0.2]]},
		"armU2": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.4, -2.1], [1.7, -2.1], [2.2, 0.2]]},
		"head": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [0.5, -0.25], [1.7, -0.25], [2.2, 0.0]]},
		"chest": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [0.5, -0.12], [1.7, -0.12], [2.2, 0.0]]},
	}},
	"clap": {"len": 2.0, "sig": ["armU", 0.7], "tracks": {
		"armU": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.35, -1.15], [1.7, -1.15], [2.0, 0.2]]},
		"armU2": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.35, -1.15], [1.7, -1.15], [2.0, 0.2]]},
		"armF": {"axis": Vector3.UP, "keys": [[0.0, 0.0], [0.5, 0.5], [0.65, 0.1], [0.8, 0.5], [0.95, 0.1], [1.1, 0.5], [1.25, 0.1], [1.4, 0.5], [1.7, 0.0]]},
		"armF2": {"axis": Vector3.UP, "keys": [[0.0, 0.0], [0.5, -0.5], [0.65, -0.1], [0.8, -0.5], [0.95, -0.1], [1.1, -0.5], [1.25, -0.1], [1.4, -0.5], [1.7, 0.0]]},
	}},
	"twirl": {"len": 1.9, "sig": ["armU", 0.7], "spin": true, "tracks": {
		"armU": {"axis": Vector3.FORWARD, "keys": [[0.0, 0.0], [0.4, -1.2], [1.5, -1.2], [1.9, 0.0]]},
		"armU2": {"axis": Vector3.FORWARD, "keys": [[0.0, 0.0], [0.4, 1.2], [1.5, 1.2], [1.9, 0.0]]},
		"hair1": {"axis": Vector3.BACK, "keys": [[0.0, 0.0], [0.9, 0.3], [1.9, 0.0]]},
	}},
	"look": {"len": 3.4, "sig": ["head", 0.35], "tracks": {
		"neck": {"axis": Vector3.UP, "keys": [[0.0, 0.0], [0.7, 0.5], [1.4, 0.5], [2.1, -0.5], [2.8, -0.5], [3.4, 0.0]]},
		"head": {"axis": Vector3.UP, "keys": [[0.0, 0.0], [0.7, 0.55], [1.4, 0.55], [2.1, -0.55], [2.8, -0.55], [3.4, 0.0]]},
	}},
	"giggle": {"len": 1.5, "sig": ["armU", 0.4], "tracks": {
		"chest": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [0.2, -0.14], [0.4, 0.02], [0.6, -0.14], [0.8, 0.02], [1.0, -0.14], [1.5, 0.0]]},
		"head": {"axis": Vector3.BACK, "keys": [[0.0, 0.0], [0.25, 0.18], [0.55, -0.18], [0.85, 0.18], [1.15, -0.18], [1.5, 0.0]]},
		"armU": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.3, -0.8], [1.2, -0.8], [1.5, 0.2]]},
		"armU2": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [0.3, -0.8], [1.2, -0.8], [1.5, 0.2]]},
	}},
	"sleep": {"len": 6.0, "sig": ["head", 0.3], "tracks": {
		"head": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.2, 0.5], [5.0, 0.5], [6.0, 0.0]]},
		"neck": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.2, 0.32], [5.0, 0.32], [6.0, 0.0]]},
		"chest": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.2, 0.26], [5.0, 0.26], [6.0, 0.0]]},
		"armU": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [1.2, 0.7], [5.0, 0.7], [6.0, 0.2]]},
		"armU2": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.2], [1.2, 0.7], [5.0, 0.7], [6.0, 0.2]]},
		"tail3": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.4, -0.22], [5.0, -0.22], [6.0, 0.0]]},
		"tail4": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.4, -0.3], [5.0, -0.3], [6.0, 0.0]]},
		"tail5": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.4, -0.38], [5.0, -0.38], [6.0, 0.0]]},
		"tail6": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.4, -0.46], [5.0, -0.46], [6.0, 0.0]]},
		"tail7": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.4, -0.52], [5.0, -0.52], [6.0, 0.0]]},
		"tail8": {"axis": Vector3.RIGHT, "keys": [[0.0, 0.0], [1.4, -0.58], [5.0, -0.58], [6.0, 0.0]]},
	}},
}

func play_verb(vname: String) -> bool:
	if not VERB_LIB.has(vname):
		return false
	verb = vname
	verb_t = 0.0
	return true

func _sample_keys(keys: Array, t: float) -> float:
	if t <= float(keys[0][0]):
		return float(keys[0][1])
	for i in range(1, keys.size()):
		if t <= float(keys[i][0]):
			var a: Array = keys[i - 1]
			var b: Array = keys[i]
			var f: float = (t - float(a[0])) / maxf(float(b[0]) - float(a[0]), 0.001)
			return lerpf(float(a[1]), float(b[1]), smoothstep(0.0, 1.0, f))
	return float(keys[-1][1])

func _apply_verb(delta: float) -> void:
	if verb == "" or skel == null:
		return
	var spec: Dictionary = VERB_LIB[verb]
	var vlen: float = spec["len"]
	verb_t += delta
	if verb_t >= vlen:
		verb = ""
		if model_root != null:
			model_root.rotation.y = 0.0
		return
	var w: float = smoothstep(0.0, 0.25, verb_t) * (1.0 - smoothstep(vlen - 0.3, vlen, verb_t))
	var tracks: Dictionary = spec["tracks"]
	for bname in tracks:
		var bi: int = bone_idx.get(bname, -1)
		if bi < 0 or not rest.has(bname):
			continue
		var tr: Dictionary = tracks[bname]
		var ang: float = _sample_keys(tr["keys"], verb_t)
		var target: Quaternion = (rest[bname] as Transform3D).basis.get_rotation_quaternion() * Quaternion(tr["axis"], ang)
		skel.set_bone_pose_rotation(bi, skel.get_bone_pose_rotation(bi).slerp(target, w))
	if bool(spec.get("spin", false)) and model_root != null:
		# a full pirouette that always lands facing forward again
		model_root.rotation.y = TAU * smoothstep(0.0, 1.0, verb_t / vlen)
var cam: Camera3D
# STORYBOOK DIORAMA LENS: longer + narrower than a normal chase cam — the
# compressed perspective flattens the world toward 2.5D so it reads as a
# toy diorama instead of open 3D. Subject size on screen stays the same
# (fov 60->38 is ~1.55x zoom; distance grew by the same factor).
var cam_back := 25.0   # chase distance (reduced indoors so the camera does not clip walls)
var cam_high := 9.0    # chase height
var cam_orbit := 0.0        # right-stick look-around: yaw offset, drifts back behind Roshan
var cam_pitch_off := 0.0    # right-stick look-around: height offset
var skel: Skeleton3D
var bone_idx := {}
var rest := {}
var warned := false
var model_root: Node3D = null     # the 3D Roshan model (shown for the "classic" skin)
# model-backed skins: rigged plushies sharing Roshan's bone names, so the
# procedural swim drives every one of them (billboards never made sense)
const SKIN_MODELS := {"huluu": "res://assets/characters/huluu.glb", "fairy": "res://assets/characters/fairy_v2.glb"}
const SKIN_TIARA_Y := {"huluu": 2.5}   # V2 bodies are fuller up top; the plushie Huluu keeps the low halo

func _tiara_y() -> float:
	return float(SKIN_TIARA_Y.get(skin_id, 4.0))
var skin_models := {}             # id -> instantiated Node3D
var _roshan_skel: Skeleton3D = null
var _roshan_maps: Array = []      # [bone_idx, rest] for Roshan, to restore on skin swap
var skin_sprite: Sprite3D = null  # billboard used for alternative full skins
var skin_sparkles: CPUParticles3D = null  # fairy sparkle trail for sparkly skins
var skin_id := "classic"
var skin_t := 0.0

func _ready() -> void:
	position = Vector3(0, 26, 0)
	# THE 3D Roshan (owner 2026-07-11: the stuffed-animal-era model is gone
	# from the game; roshan.glb remains on disk only as the rig donor for
	# tools/roshan_v2_retarget.py)
	var glb: PackedScene = load("res://assets/characters/roshan_v2.glb") as PackedScene
	if glb == null:
		glb = load("res://assets/characters/roshan.glb") as PackedScene
	if glb != null:
		var inst: Node3D = glb.instantiate()
		inst.scale = Vector3.ONE * 1.55
		inst.position.y = -1.6
		add_child(inst)
		model_root = inst
		skel = _find_skeleton(inst)
		_map_bones()
		_roshan_skel = skel
		_roshan_maps = [bone_idx.duplicate(), rest.duplicate()]
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
	cam.fov = 38.0   # diorama lens (see cam_back note)
	get_parent().add_child.call_deferred(cam)

func _map_bones() -> void:
	bone_idx = {}
	rest = {}
	if skel == null:
		return
	for n in ["root", "spine1", "chest", "neck", "head", "hair1", "hair2", "hair3",
			"hairL1", "hairL2", "armU", "armF", "hand", "armU2", "armF2", "hand2",
			"tail1", "tail2", "tail3", "tail4", "tail5", "tail6", "tail7", "tail8",
			"finTop", "finBot", "wingL", "wingR"]:
		var bi: int = skel.find_bone(n)
		bone_idx[n] = bi
		if bi >= 0:
			rest[n] = skel.get_bone_pose(bi)

func _attach_wing_cards(mdl: Node3D) -> void:
	# CARD WINGS: the Meshy sculpt fused its wings into her back (relief, not
	# separable geometry), so those stay as static painted detail and the
	# REAL flap is two textured plates on the measured wingL/wingR hinge
	# bones — a rigid shader rotation around the hinge, like the butterflies.
	var sk := _find_skeleton(mdl)
	if sk == null or not ResourceLoader.exists("res://assets/characters/skins/fairy_wing_card.png"):
		return
	var tex: Texture2D = load("res://assets/characters/skins/fairy_wing_card.png")
	for wi in range(2):
		var bname: String = "wingL" if wi == 0 else "wingR"
		if sk.find_bone(bname) < 0:
			continue
		var att := BoneAttachment3D.new()
		att.bone_name = bname
		sk.add_child(att)
		var mi := MeshInstance3D.new()
		var qm := QuadMesh.new()
		qm.size = Vector2(1.6, 2.75)   # wing art aspect 282x489
		qm.center_offset = Vector3(0.8, 0.0, 0.0)   # hinge edge at the origin
		mi.mesh = qm
		# map the quad's outward X onto the bone's along-axis (Y), keep it
		# upright: columns are the bone-local images of quad X/Y/Z
		mi.transform.basis = Basis(Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(1, 0, 0))
		var wm := ShaderMaterial.new()
		wm.shader = load("res://assets/shaders/fairy_wing.gdshader")
		wm.set_shader_parameter("wing_tex", tex)
		wm.set_shader_parameter("phase", 0.0 if wi == 0 else 0.18)
		wm.set_shader_parameter("flip", 0.0 if wi == 0 else 1.0)
		mi.material_override = wm
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		att.add_child(mi)

func set_skin(id: String, tex_path: String) -> void:
	# "classic" shows the 3D model; any other id swaps to a full-skin billboard
	skin_id = id
	if _tiara != null:
		_tiara.position.y = _tiara_y()
	if SKIN_MODELS.has(id) and ResourceLoader.exists(String(SKIN_MODELS[id])):
		# the full Roshan treatment: a rigged double-sided plushie with the SAME
		# bone names, so the procedural swim drives her directly
		if not skin_models.has(id):
			var mdl: Node3D = (load(String(SKIN_MODELS[id])) as PackedScene).instantiate()
			if id == "fairy":
				# fairy_v2 is exported at Roshan's world size, so it takes
				# the classic transform, not the plushie one. NO
				# _upgrade_texture: that helper swaps in the OLD atlas,
				# which is UV-gibberish on Meshy meshes.
				mdl.scale = Vector3.ONE * 1.55
				mdl.position.y = -1.6
				var mn0: Node = get_parent()
				if mn0 != null and mn0.has_method("_toonify"):
					# flat toon response = world lighting reads the same on
					# her as on everything else
					mn0._toonify(mdl)
				_attach_wing_cards(mdl)
			else:
				mdl.scale = Vector3.ONE * 3.9
				mdl.position.y = -3.4
			add_child(mdl)
			skin_models[id] = mdl
		for k in skin_models:
			(skin_models[k] as Node3D).visible = (k == id)
		skel = _find_skeleton(skin_models[id])
		_map_bones()
		if model_root != null:
			model_root.visible = false
		if skin_sprite != null:
			skin_sprite.visible = false
		if skin_sparkles != null:
			skin_sparkles.emitting = true   # every plushie skin gets the sparkle trail
		return
	# non-model skin: restore Roshan's skeleton for the swim code
	for k in skin_models:
		(skin_models[k] as Node3D).visible = false
	if _roshan_skel != null and skel != _roshan_skel:
		skel = _roshan_skel
		bone_idx = _roshan_maps[0]
		rest = _roshan_maps[1]
	var on_skin: bool = not (id == "classic" or id == "pearl" or tex_path == "")
	if on_skin:
		if skin_sprite != null:
			var tex: Texture2D = load(tex_path)
			skin_sprite.texture = tex
			# normalise so EVERY skin stands ~7 units tall regardless of art size
			# (a fixed pixel_size made differently-sized art render giant or tiny)
			skin_sprite.pixel_size = 7.0 / maxf(float(tex.get_height()), 1.0)
			skin_sprite.visible = true
			skin_sprite.scale = Vector3.ONE
		if model_root != null:
			model_root.visible = false
	else:
		if model_root != null:
			model_root.visible = true
		if skin_sprite != null:
			skin_sprite.visible = false
	# PEARL PRINCESS (Pearl Shop, 250 pearls): the classic model wrapped in an
	# iridescent mother-of-pearl shimmer overlay
	_set_pearl_overlay(id == "pearl")
	if skin_sparkles != null:
		skin_sparkles.emitting = on_skin or id == "pearl" or rainbow_trail

var _pearl_mat: StandardMaterial3D = null
var rainbow_trail := false
var _tiara: Node3D = null

func _set_pearl_overlay(on: bool) -> void:
	if _pearl_mat == null and on:
		_pearl_mat = StandardMaterial3D.new()
		_pearl_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		_pearl_mat.albedo_color = Color(1.0, 0.92, 1.0, 0.22)
		_pearl_mat.rim_enabled = true
		_pearl_mat.rim = 1.0
		_pearl_mat.rim_tint = 0.6
		_pearl_mat.emission_enabled = true
		_pearl_mat.emission = Color(0.9, 0.75, 1.0)
		_pearl_mat.emission_energy_multiplier = 0.45
	_apply_overlay(model_root, _pearl_mat if on else null)

func _apply_overlay(n: Node, mat: Material) -> void:
	if n == null:
		return
	if n is MeshInstance3D:
		(n as MeshInstance3D).material_overlay = mat
	for c in n.get_children():
		_apply_overlay(c, mat)

func set_rainbow_trail(on: bool) -> void:
	# Pearl Shop treasure: sparkles follow Roshan forever, in every look
	rainbow_trail = on
	if on and skin_sparkles != null:
		skin_sparkles.amount = 44
		var grad := Gradient.new()
		grad.set_color(0, Color(1.0, 0.5, 0.7))
		grad.set_color(1, Color(0.5, 0.8, 1.0))
		var gt := GradientTexture1D.new()
		gt.gradient = grad
		skin_sparkles.color_ramp = grad
		skin_sparkles.emitting = true

func set_tiara(on: bool) -> void:
	# Pearl Shop treasure: a floating golden tiara ringed with pearls
	if on and _tiara == null:
		_tiara = Node3D.new()
		var ring := MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 0.5
		tm.outer_radius = 0.72
		ring.mesh = tm
		var gm := StandardMaterial3D.new()
		gm.albedo_color = Color(1.0, 0.85, 0.35)
		gm.metallic = 0.85
		gm.roughness = 0.2
		gm.emission_enabled = true
		gm.emission = Color(1.0, 0.8, 0.3)
		gm.emission_energy_multiplier = 0.9
		ring.material_override = gm
		_tiara.add_child(ring)
		for pi in range(5):
			var pearl := MeshInstance3D.new()
			var sm := SphereMesh.new()
			sm.radius = 0.13
			sm.height = 0.26
			pearl.mesh = sm
			var pm := StandardMaterial3D.new()
			pm.albedo_color = Color(1.0, 0.97, 1.0)
			pm.metallic = 0.5
			pm.roughness = 0.15
			pm.emission_enabled = true
			pm.emission = Color(1.0, 0.9, 0.98)
			pm.emission_energy_multiplier = 0.6
			pearl.material_override = pm
			var pa: float = TAU * float(pi) / 5.0
			pearl.position = Vector3(cos(pa) * 0.61, 0.12, sin(pa) * 0.61)
			_tiara.add_child(pearl)
		_tiara.position = Vector3(0, _tiara_y(), 0)   # floats just above her head in every look
		add_child(_tiara)
		var tw := _tiara.create_tween().set_loops()
		tw.tween_property(_tiara, "rotation:y", TAU, 6.0).from(0.0)
	if _tiara != null:
		_tiara.visible = on

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
	if "stickers_layer" in _m0 and _m0.stickers_layer != null:
		return   # frozen while the sticker book is open
	if "sleep_t" in _m0 and float(_m0.sleep_t) >= 0.0:
		return   # tucked into bed — the sleep cutscene drives her
	if "pose_t" in _m0 and float(_m0.pose_t) >= 0.0:
		return   # trophy pose — hold still for the curtain call!
	if "mg_kind" in _m0 and String(_m0.mg_kind) != "":
		return   # a 2D minigame overlay is up — stick input belongs to IT (snowball rolling!)
	if "craft_layer" in _m0 and _m0.craft_layer != null:
		return   # frozen while the craft studio is open (was drifting behind the overlay)
	if "game" in _m0 and (String(_m0.game) == "slide" or String(_m0.game) == "fairyshoot" or String(_m0.game) == "kart" or String(_m0.game) == "galaxy"):
		return   # the slide / fairy-shooter / kart / galaxy modes drive the player + camera themselves
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
	var jx: float = joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = joy_axis(JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.2:
		turn -= jx
	if absf(jy) > 0.2:
		fwd -= jy
	# D-pad swims too (nice on small pads like the 8BitDo Lite)
	if joy_pressed(JOY_BUTTON_DPAD_UP):
		fwd += 1.0
	if joy_pressed(JOY_BUTTON_DPAD_DOWN):
		fwd -= 0.6
	if joy_pressed(JOY_BUTTON_DPAD_LEFT):
		turn += 1.0
	if joy_pressed(JOY_BUTTON_DPAD_RIGHT):
		turn -= 1.0
	var m0: Node = get_parent()
	if "touch_ui" in m0 and m0.touch_ui != null:
		var tv: Vector2 = m0.touch_ui.stick_vec
		if absf(tv.x) > 0.15:
			turn -= tv.x
		if absf(tv.y) > 0.15:
			fwd -= tv.y
	var jump_held: bool = Input.is_physical_key_pressed(KEY_SPACE) or joy_pressed(JOY_BUTTON_A) or joy_pressed(JOY_BUTTON_B)
	if "touch_ui" in m0 and m0.touch_ui != null and m0.touch_ui.action_down:
		jump_held = true

	jump_cool -= delta
	if jump_held and jump_cool <= 0.0:
		jump_cool = 0.4
		vel.y = 16.0

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
			# Sky Lagoon: rest on the rolling-hill terrain (plus the bridge deck /
			# star platforms); dip down into the river valleys and the castle moat
			floor_a = m.lagoon_walk_h(position.x, position.z) + 2.0
		var ceil_a: float = ap.y + ceil_h
		if "arena_zones" in m:
			# Y-BANDED level zones (castle balcony/top chambers/basement): a
			# floor override only exists for someone inside its height band,
			# so a balcony never blocks the throne room underneath it
			var lx: float = position.x - ap.x
			var lz: float = position.z - ap.z
			var ly: float = position.y - ap.y
			for zz in m.arena_zones:
				if not (zz["rect"] as Rect2).has_point(Vector2(lx, lz)):
					continue
				var band: Vector2 = zz.get("band", Vector2(-1e6, 1e6))
				if ly < band.x or ly > band.y:
					continue
				if zz.has("floor"):
					floor_a = ap.y + float(zz["floor"])
				if zz.has("ceil"):
					ceil_a = ap.y + float(zz["ceil"])
		if position.y < floor_a:
			position.y = floor_a
			vel.y = maxf(0.0, vel.y)
		if position.y > ceil_a:
			position.y = ceil_a
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
	_apply_verb(delta)
	# idle life: after a quiet while she looks around; at night she dozes off
	# (free swim only — verbs never interrupt a minigame)
	idle_verb_cool = maxf(0.0, idle_verb_cool - delta)
	if verb == "" and idle_verb_cool <= 0.0 and idle_t > 12.0:
		var mn: Node = get_parent()
		if "game" in mn and String(mn.game) == "":
			if "is_night" in mn and bool(mn.is_night) and idle_t > 25.0:
				play_verb("sleep")
				idle_verb_cool = 22.0
			else:
				play_verb("look")
				idle_verb_cool = 15.0

	# full-skin billboard: gentle idle bob + a wing-flap squash so it feels alive without bones
	if skin_sprite != null and skin_sprite.visible:
		skin_t += delta * (2.2 + speed * 0.6)
		skin_sprite.position.y = 0.6 + sin(skin_t) * 0.3
		var flap: float = sin(skin_t * 2.4)               # quicker beat = wings flapping
		skin_sprite.scale = Vector3(1.0 + flap * 0.05, 1.0 - flap * 0.03, 1.0)

	# right-stick camera: peek around / up / down, then drift back behind her
	var rx: float = joy_axis(JOY_AXIS_RIGHT_X)
	var ry: float = joy_axis(JOY_AXIS_RIGHT_Y)
	if absf(rx) > 0.25:
		cam_orbit = clampf(cam_orbit - rx * 2.6 * delta, -PI * 0.9, PI * 0.9)
	else:
		cam_orbit = lerpf(cam_orbit, 0.0, 1.0 - pow(0.35, delta))
	if absf(ry) > 0.25:
		cam_pitch_off = clampf(cam_pitch_off + ry * 9.0 * delta, -4.5, 8.0)
	else:
		cam_pitch_off = lerpf(cam_pitch_off, 0.0, 1.0 - pow(0.35, delta))

	if cam != null and cam.is_inside_tree():
		var cyaw: float = yaw + cam_orbit
		var target := position + Vector3(-sin(cyaw) * cam_back, cam_high + cam_pitch_off, -cos(cyaw) * cam_back)
		cam.position = cam.position.lerp(target, 1.0 - pow(0.001, delta))
		cam.look_at(position + Vector3(0, 1.5, 0))
