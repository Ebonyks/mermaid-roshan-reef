extends Node3D
# Roshan player: floaty swim + jump physics with a camera-facing 2.5D sprite.

const ROSHAN_SPRITE_ANCHORS := preload(
	"res://scripts/roshan_sprite_anchors.gd")
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

# mouse look-around: hold the RIGHT button and drag (left button belongs to
# minigames / the touch stick). Deltas accumulate here between frames and are
# consumed at the top of _process, so frames the player logic skips (overlays,
# minigame modes) just discard them instead of applying one big camera jump.
var _mlook_dx := 0.0
var _mlook_dy := 0.0

func _input(ev: InputEvent) -> void:
	if ev is InputEventMouseMotion and (ev.button_mask & MOUSE_BUTTON_MASK_RIGHT) != 0:
		_mlook_dx += ev.relative.x
		_mlook_dy += ev.relative.y

var yaw := 0.0
var vel := Vector3.ZERO
var swim_phase := 0.0
var arm_swim_phase := 0.0
var jump_cool := 0.0
var idle_t := 0.0

# ---- sprite verb layer ---------------------------------------------------
# Verb durations preserve the established gameplay timing; visible motion is
# selected from the four-keyframe gesture atlases in _tick_classic_sprite().
var verb := ""
var verb_t := 0.0
var idle_verb_cool := 0.0
var bump_verb_cool := 0.0    # keeps wall-bump "boing" from re-firing every frame
var was_airborne := false    # free-swim only: tracks surface crossings for splashes

# ---- land locomotion (comedy dept.) ----
# A mermaid has no legs, so dry ground is covered in tiny determined hops.
# The sprite layer supplies the pose and bounce while movement physics stay
# byte-identical. main.water_surface_y is the wet/dry oracle.
var land_rest := false       # resting on an arena floor this frame
var land_dry := false        # that spot is dry land, not water
var land_blend := 0.0        # 0 = swim pose, 1 = land pose (smoothed)
var hop_phase := 0.0
var hop_amp := 0.0           # hop envelope: ramps in only while scooting
var hop_prev := 0.0          # last frame's hop height, for touchdown detection
var land_hops := 0           # session touchdown count (gates the one-time giggle line)
var hop_dust: CPUParticles3D = null
var _hop_node: Node3D = null       # visual node the hop bounce is applied to
var _hop_base_y := 0.0
var _hop_base_scale := Vector3.ONE

const VERB_LIB := {
	"wave": {"len": 2.6},
	"cheer": {"len": 2.2},
	"clap": {"len": 2.0},
	"twirl": {"len": 1.9},
	"look": {"len": 3.4},
	"giggle": {"len": 1.5},
	"sleep": {"len": 6.0},
	"point": {"len": 2.0},
	"collect": {"len": 1.1},
	"boing": {"len": 0.8},
	"hairtwirl": {"len": 3.0},
	"hum": {"len": 3.4},
	"flop": {"len": 3.4},
}

const ROSHAN_25D_SHEETS := {
	"directional": [preload("res://assets/characters/roshan_25d/roshan_directional.png"), 4, 2],
	"swim_front": [preload("res://assets/characters/roshan_25d/roshan_swim_front.png"), 4, 4],
	"swim_back": [preload("res://assets/characters/roshan_25d/roshan_swim_back.png"), 4, 4],
	"gesture_a": [preload("res://assets/characters/roshan_25d/roshan_gesture_a.png"), 4, 4],
	"gesture_b": [preload("res://assets/characters/roshan_25d/roshan_gesture_b.png"), 4, 4],
	"gesture_c": [preload("res://assets/characters/roshan_25d/roshan_gesture_c.png"), 4, 4],
	"gesture_d": [preload("res://assets/characters/roshan_25d/roshan_gesture_d.png"), 4, 2],
	"play_a": [preload("res://assets/characters/roshan_25d/roshan_play_a.png"), 4, 4],
	"play_b": [preload("res://assets/characters/roshan_25d/roshan_play_b.png"), 4, 4],
}
const ROSHAN_25D_KEYFRAMES := 4
const ROSHAN_25D_GESTURES := {
	"wave": ["gesture_a", 0], "cheer": ["gesture_a", 1],
	"clap": ["gesture_a", 2], "twirl": ["gesture_a", 3],
	"look": ["gesture_b", 0], "giggle": ["gesture_b", 1],
	"sleep": ["gesture_b", 2], "point": ["gesture_b", 3],
	"collect": ["gesture_c", 0], "boing": ["gesture_c", 1],
	"hairtwirl": ["gesture_c", 2], "hum": ["gesture_c", 3],
	"flop": ["gesture_d", 0], "carry": ["gesture_d", 1],
}
const ROSHAN_25D_PLAY := {
	"swing": ["play_a", 0], "climb": ["play_a", 1],
	"ride": ["play_a", 2], "land": ["play_a", 3],
	"dig_l": ["play_b", 0], "dig_r": ["play_b", 1],
	"seat": ["play_b", 2], "hop": ["play_b", 3],
}

func play_verb(vname: String) -> bool:
	if not VERB_LIB.has(vname):
		return false
	verb = vname
	verb_t = 0.0
	# A gesture is activity. Reset the idle clock so an explicitly played
	# "look" cannot finish and immediately auto-start the same idle verb.
	idle_t = 0.0
	return true


func _apply_verb(delta: float) -> void:
	if verb == "":
		return
	var spec: Dictionary = VERB_LIB[verb]
	var vlen: float = float(spec["len"])
	verb_t += delta
	if verb_t >= vlen:
		verb = ""
		if classic_sprite != null:
			classic_sprite.rotation.z = 0.0
var cam: Camera3D
# STORYBOOK DIORAMA LENS: longer + narrower than a normal chase cam — the
# compressed perspective flattens the world toward 2.5D so it reads as a
# toy diorama instead of open 3D. Subject size on screen stays the same
# (fov 60->38 is ~1.55x zoom; distance grew by the same factor).
var cam_back := 25.0   # chase distance (reduced indoors so the camera does not clip walls)
var cam_high := 9.0    # chase height
var cam_orbit := 0.0        # right-stick look-around: yaw offset, drifts back behind Roshan
var cam_pitch_off := 0.0    # right-stick look-around: height offset
var classic_motion_root: Node3D = null
var classic_sprite: Sprite3D = null
var classic_sprite_sheet := ""
var classic_sprite_frame := -1
var classic_sprite_flip := false
var classic_toy_pose_until_msec := 0
var classic_carry_started_msec := 0
var classic_was_carrying := false
var classic_life_phase := 0.0
# Alternative looks are also flat cutouts; no character model is loaded.
const SKIN_TEXTURES := {
	"fairy": "res://assets/characters/skins/fairy_mermaid.png",
	"huluu": "res://assets/characters/friends/huluu.png",
}
var skin_sprite: Sprite3D = null  # billboard used for alternative full skins
var skin_sparkles: CPUParticles3D = null  # fairy sparkle trail for sparkly skins
var skin_id := "classic"
var skin_t := 0.0
# OperaAct drives position/yaw and reports speed while this same sprite clock
# keeps Roshan alive. Input, physics, and camera remain with the act.
var puppet := false
var puppet_speed := 0.0
# Career selection remains gameplay state. Dedicated 2D outfit atlases can
# layer on this contract later; the animated base sprite never disappears.
var costume_id := ""
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
	# Sprite3D is the only Roshan renderer. The retired GLB rig is never loaded.
	classic_motion_root = Node3D.new()
	classic_motion_root.name = "AlwaysAliveMotion"
	add_child(classic_motion_root)
	classic_sprite = Sprite3D.new()
	classic_sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	classic_sprite.pixel_size = 7.4 / 256.0
	classic_sprite.position = Vector3(0, 0.35, 0)
	classic_sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	classic_sprite.shaded = false
	classic_sprite.double_sided = true
	classic_motion_root.add_child(classic_sprite)
	_set_classic_sprite_frame("directional", 4)
	_refresh_classic_visual()
	# billboard sprite used when an alternative full skin is worn (hidden by default)
	# pixel_size sized so the 707px-tall art ≈ the 7-unit classic model
	skin_sprite = Sprite3D.new()
	skin_sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	skin_sprite.pixel_size = 0.0100
	skin_sprite.position = Vector3(0, 0.6, 0)
	skin_sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	skin_sprite.shaded = false
	skin_sprite.double_sided = true
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
	# landing puffs for the on-land hop (one-shot, restarted per touchdown)
	hop_dust = CPUParticles3D.new()
	hop_dust.amount = 9
	hop_dust.lifetime = 0.45
	hop_dust.one_shot = true
	hop_dust.explosiveness = 1.0
	hop_dust.local_coords = false
	hop_dust.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
	hop_dust.emission_sphere_radius = 0.9
	hop_dust.direction = Vector3.UP
	hop_dust.spread = 75.0
	hop_dust.gravity = Vector3(0, -1.5, 0)
	hop_dust.initial_velocity_min = 1.2
	hop_dust.initial_velocity_max = 3.0
	hop_dust.scale_amount_min = 0.10
	hop_dust.scale_amount_max = 0.24
	var hdm := SphereMesh.new()
	hdm.radius = 0.5
	hdm.height = 1.0
	hdm.radial_segments = 6
	hdm.rings = 3
	hop_dust.mesh = hdm
	var hdmat := StandardMaterial3D.new()
	hdmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	hdmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	hdmat.albedo_color = Color(0.96, 0.92, 0.80, 0.7)
	hdmat.disable_receive_shadows = true
	hop_dust.material_override = hdmat
	hop_dust.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	hop_dust.position = Vector3(0, -1.7, 0)
	hop_dust.emitting = false
	add_child(hop_dust)
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
	cam.fov = 38.0   # diorama lens (see cam_back note)
	get_parent().add_child.call_deferred(cam)

func _refresh_classic_visual() -> void:
	if classic_sprite != null:
		classic_sprite.visible = skin_id == "classic"

func _set_classic_sprite_frame(sheet: String, frame_idx: int, flip: bool = false) -> void:
	if classic_sprite == null or not ROSHAN_25D_SHEETS.has(sheet):
		return
	var spec: Array = ROSHAN_25D_SHEETS[sheet]
	var frame_count: int = int(spec[1]) * int(spec[2])
	var safe_frame: int = clampi(frame_idx, 0, frame_count - 1)
	if classic_sprite_sheet != sheet:
		classic_sprite.texture = spec[0] as Texture2D
		classic_sprite.hframes = int(spec[1])
		classic_sprite.vframes = int(spec[2])
		classic_sprite_sheet = sheet
		classic_sprite_frame = -1
	if classic_sprite_frame != safe_frame:
		classic_sprite.frame = safe_frame
		classic_sprite_frame = safe_frame
	if classic_sprite_flip != flip:
		classic_sprite.flip_h = flip
		classic_sprite_flip = flip
	if ROSHAN_SPRITE_ANCHORS.has_sheet(sheet):
		classic_sprite.offset = ROSHAN_SPRITE_ANCHORS.correction(
			sheet, safe_frame, Vector2(128.0, 116.0), flip)
	else:
		classic_sprite.offset = Vector2.ZERO

func _set_classic_sequence(sequence: Array, phase: int, flip: bool = false) -> void:
	var sheet: String = String(sequence[0])
	var row: int = int(sequence[1])
	_set_classic_sprite_frame(sheet,
		row * ROSHAN_25D_KEYFRAMES + clampi(phase, 0, ROSHAN_25D_KEYFRAMES - 1),
		flip)

func _classic_view_angle() -> float:
	if cam == null or not cam.is_inside_tree():
		return PI
	var to_camera: Vector3 = cam.global_position - global_position
	to_camera.y = 0.0
	if to_camera.length_squared() < 0.0001:
		return PI
	to_camera = to_camera.normalized()
	var forward := Vector3(sin(yaw), 0.0, cos(yaw))
	return atan2(forward.cross(to_camera).y, forward.dot(to_camera))

func _classic_direction_frame(view_angle: float) -> int:
	var sector: int = int(round(view_angle / (PI * 0.25)))
	return posmod(-sector, 8)

func _classic_is_carrying() -> bool:
	var mn: Node = get_parent()
	return mn != null and "carry_sys" in mn and mn.carry_sys != null \
		and bool(mn.carry_sys.is_carrying())

func _tick_classic_sprite(speed: float,
	tap_move_commanded: bool = false) -> void:
	if classic_sprite == null or not classic_sprite.visible:
		return
	# Lagoon toys author a pose from the parent controller once per frame.
	# Hold it briefly so player process ordering cannot immediately replace it.
	if Time.get_ticks_msec() < classic_toy_pose_until_msec:
		return
	var view_angle: float = _classic_view_angle()
	var flip: bool = view_angle > 0.15
	var carrying: bool = _classic_is_carrying()
	if tap_move_commanded and not carrying:
		# A pressed world point owns the locomotion pose while its assisted
		# route is actually commanding movement. This deliberately precedes
		# idle/gesture and dry-land pose selection so Roshan always visibly
		# swims toward the chosen point instead of sliding in a held pose.
		classic_sprite.rotation.z = 0.0
		var tap_phase: int = int(floor(fposmod(
			swim_phase / TAU * 16.0, 16.0)))
		var tap_sheet := "swim_back" \
			if cos(view_angle) < -0.15 else "swim_front"
		_set_classic_sprite_frame(tap_sheet, tap_phase, flip)
		return
	if verb != "" and ROSHAN_25D_GESTURES.has(verb):
		var verb_len: float = maxf(float(VERB_LIB[verb]["len"]), 0.001)
		var verb_phase: int = mini(
			int(floor(clampf(verb_t / verb_len, 0.0, 0.9999) * ROSHAN_25D_KEYFRAMES)),
			ROSHAN_25D_KEYFRAMES - 1)
		_set_classic_sequence(ROSHAN_25D_GESTURES[verb] as Array, verb_phase, flip)
		if verb == "twirl":
			var spin_u: float = verb_t / verb_len
			classic_sprite.rotation.z = sin(spin_u * TAU) * 0.10
			var spin_flip: bool = spin_u >= 0.5
			classic_sprite.flip_h = spin_flip
			classic_sprite_flip = spin_flip
		else:
			classic_sprite.rotation.z = 0.0
		return
	classic_sprite.rotation.z = 0.0
	if carrying:
		var now_msec: int = Time.get_ticks_msec()
		if not classic_was_carrying:
			classic_carry_started_msec = now_msec
			classic_was_carrying = true
		var carry_elapsed: int = now_msec - classic_carry_started_msec
		var carry_phase: int = mini(
			int(carry_elapsed / 140), ROSHAN_25D_KEYFRAMES - 2)
		if carry_elapsed >= 420:
			# The first three frames lift the toy into place; the final two
			# alternate forever as a gentle hold/breath loop. Previously the
			# carry pose saturated on frame four and became a dead cutout.
			carry_phase = 2 + posmod(int((carry_elapsed - 420) / 320), 2)
		_set_classic_sequence(ROSHAN_25D_GESTURES["carry"] as Array, carry_phase, flip)
		return
	classic_was_carrying = false
	if land_blend > 0.55 and (hop_amp > 0.10 or (land_dry and speed > 2.5)):
		var hop_frame: int = int(floor(
			fposmod(hop_phase, PI) / PI * ROSHAN_25D_KEYFRAMES))
		_set_classic_sequence(ROSHAN_25D_PLAY["hop"] as Array, hop_frame, flip)
		return
	if speed > 0.7 and land_blend < 0.65:
		var phase: int = int(floor(fposmod(
			swim_phase / TAU * 16.0, 16.0)))
		var swim_sheet := "swim_back" if cos(view_angle) < -0.15 else "swim_front"
		_set_classic_sprite_frame(swim_sheet, phase, flip)
		return
	if land_blend > 0.55:
		# A parked mermaid curls her tail under and gently shifts on the
		# four-frame seated loop instead of becoming a single directional card.
		var seated_phase: int = int(floor(fposmod(
			swim_phase / TAU * float(ROSHAN_25D_KEYFRAMES),
			float(ROSHAN_25D_KEYFRAMES))))
		_set_classic_sequence(ROSHAN_25D_PLAY["seat"] as Array, seated_phase, flip)
		return
	# Stopping has a readable end: return to the matching directional pose.
	# AlwaysAliveMotion keeps this pose breathing, so idle is distinct from
	# locomotion without ever becoming a dead cutout.
	_set_classic_sprite_frame(
		"directional", _classic_direction_frame(view_angle), false)

func _tick_always_alive_visual(delta: float, speed: float) -> void:
	# Atlas frames do most of the acting. A tiny independent breath prevents
	# long authored key poses (notably sleep) from reading as a stopped render.
	# Playground choreography is excluded because its sprite must stay locked
	# to the physical seat/rope phase with no second bobbing clock.
	classic_life_phase = fposmod(
		classic_life_phase + delta * (1.35 + minf(speed * 0.025, 0.6)), TAU)
	if classic_motion_root != null:
		if Time.get_ticks_msec() < classic_toy_pose_until_msec:
			classic_motion_root.position = Vector3.ZERO
			classic_motion_root.scale = Vector3.ONE
		else:
			var breath: float = sin(classic_life_phase)
			classic_motion_root.position.y = breath * 0.055
			classic_motion_root.scale = Vector3(
				1.0 + breath * 0.008, 1.0 - breath * 0.006, 1.0)
	if skin_sprite != null and skin_sprite.visible:
		skin_t += delta * (2.2 + speed * 0.6)
		# Alternate full-skin cutouts do not have atlases, so their established
		# bob and squash remain their continuous idle/motion language.
		skin_sprite.position.y = 0.6 + lerpf(
			sin(skin_t) * 0.3,
			absf(sin(skin_t * 1.6)) * 0.7,
			land_blend)
		var flap: float = sin(skin_t * 2.4)
		skin_sprite.scale = Vector3(
			1.0 + flap * 0.05, 1.0 - flap * 0.03, 1.0)


func set_skin(id: String, tex_path: String) -> void:
	skin_id = id
	var resolved_path: String = tex_path
	if resolved_path == "" and SKIN_TEXTURES.has(id):
		resolved_path = String(SKIN_TEXTURES[id])
	var on_skin: bool = id != "classic" and resolved_path != "" \
		and ResourceLoader.exists(resolved_path)
	if id != "classic" and not on_skin:
		skin_id = "classic"
	if skin_sprite != null:
		skin_sprite.visible = on_skin
		if on_skin:
			var tex: Texture2D = load(resolved_path)
			skin_sprite.texture = tex
			# Every cutout stands about seven world units tall regardless of source size.
			skin_sprite.pixel_size = 7.0 / maxf(float(tex.get_height()), 1.0)
			skin_sprite.scale = Vector3.ONE
	_refresh_classic_visual()
	if skin_sparkles != null:
		skin_sparkles.emitting = on_skin

# ---------------- career costumes (Pearl Opera House) ----------------
# Costume ids remain part of opera/save behavior. Roshan stays on her animated
# sprite atlas until matching 2D costume layers are available.
func set_costume(id: String) -> void:
	costume_id = id
	_refresh_classic_visual()

func clear_costume() -> void:
	costume_id = ""
	_refresh_classic_visual()

# ---- playground choreography (Sky Lagoon toy play-moments) ----
func toy_pose(kind: String, t: float, aux: float = 0.0) -> void:
	if classic_sprite == null or not classic_sprite.visible:
		return
	var sprite_pose: String = kind
	var sprite_phase := 0
	if kind == "dig":
		var dig_angle: float = fposmod(aux, TAU)
		sprite_pose = "dig_l" if dig_angle < PI else "dig_r"
		sprite_phase = int(floor(
			fposmod(dig_angle, PI) / PI * ROSHAN_25D_KEYFRAMES))
	elif kind == "swing":
		# SkyLagoon passes the normalized phase from the very same pendulum
		# clock that moves the seat. Never free-run this pose from t: even a
		# small frequency mismatch makes Roshan pump against the ropes.
		sprite_phase = int(floor(
			fposmod(aux, 1.0) * ROSHAN_25D_KEYFRAMES))
	elif kind == "climb" or kind == "ride" or kind == "land":
		sprite_phase = mini(
			int(floor(clampf(aux, 0.0, 0.9999) * ROSHAN_25D_KEYFRAMES)),
			ROSHAN_25D_KEYFRAMES - 1)
	else:
		sprite_phase = int(floor(fposmod(
			t * 2.0, float(ROSHAN_25D_KEYFRAMES))))
	if ROSHAN_25D_PLAY.has(sprite_pose):
		_set_classic_sequence(ROSHAN_25D_PLAY[sprite_pose] as Array, sprite_phase)
		if classic_motion_root != null:
			classic_motion_root.position = Vector3.ZERO
			classic_motion_root.scale = Vector3.ONE
		classic_toy_pose_until_msec = Time.get_ticks_msec() + 100

func _process(delta: float) -> void:
	# consume mouse-look deltas up front: early returns below then drop them
	var mlook_x: float = _mlook_dx
	var mlook_y: float = _mlook_dy
	_mlook_dx = 0.0
	_mlook_dy = 0.0
	var _m0: Node = get_parent()
	# Visual life runs before every gameplay early-return. Overlays, cutscenes,
	# externally-driven modes and puppet staging may suspend controls or physics,
	# but a visible Roshan never suspends her atlas clock or breathing motion.
	var visual_speed: float = puppet_speed if puppet else vel.length()
	_tick_swim_bones(delta, visual_speed)
	_apply_verb(delta)
	_tick_always_alive_visual(delta, visual_speed)
	_tick_classic_sprite(visual_speed)
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
	if "toy_play" in _m0 and not (_m0.toy_play as Dictionary).is_empty():
		return   # she is ON a playground toy — the play moment drives her
	if "mg_kind" in _m0 and String(_m0.mg_kind) != "":
		return   # a 2D minigame overlay is up — stick input belongs to IT (snowball rolling!)
	if "craft_layer" in _m0 and _m0.craft_layer != null:
		return   # frozen while the craft studio is open (was drifting behind the overlay)
	if "collection_layer" in _m0 and _m0.collection_layer != null:
		vel = Vector3.ZERO
		return   # the icon-led Critter Book is a full-screen touch overlay
	if "game" in _m0 and (String(_m0.game) == "slide" or String(_m0.game) == "fairyshoot" or String(_m0.game) == "kart" or String(_m0.game) == "galaxy" or String(_m0.game) == "combat" or String(_m0.game) == "stuffie" or String(_m0.game) == "dungeon" or String(_m0.game) == "dolls" or String(_m0.game) == "brawl"):
		return   # these modes drive the player + camera themselves (dolls: the side-scroll stage)
	if "g" in _m0 and String((_m0.g as Dictionary).get("phase", "")) == "promenade":
		# The promenade owns movement and its side-on camera, but the visual
		# clock above still runs so its externally positioned Roshan stays alive.
		vel = Vector3.ZERO
		return
	if "l2_cutscene_t" in _m0 and _m0.l2_cutscene_t >= 0.0:
		if cam != null and cam.is_inside_tree():
			cam.look_at(position + Vector3(0, 1.5, 0))
		return
	if puppet:
		_tick_classic_sprite(puppet_speed)
		# settle toward idle unless the act keeps reporting movement, so she
		# never treads water at sprint pace while standing for the applause
		puppet_speed = lerpf(puppet_speed, 0.0, 1.0 - pow(0.05, delta))
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
	# while a pad holds R1 it is Player 2's — its left stick steers the stuffie
	# companion (companion.gd), so Roshan must ignore it for that beat
	var pad_is_p2: bool = "companion_p2" in _m0 and bool(_m0.companion_p2)
	var jx: float = 0.0 if pad_is_p2 else joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = 0.0 if pad_is_p2 else joy_axis(JOY_AXIS_LEFT_Y)
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
		# 0.10 (was 0.15): the stick now ramps from 0 at its 22px slop edge, so
		# a 0.15 gate on top would leave the first ~8px past slop dead — the
		# slop itself is the dead zone now, this only filters jitter
		if absf(tv.x) > 0.10:
			turn -= tv.x
		if absf(tv.y) > 0.10:
			fwd -= tv.y
	# Hybrid tap-to-move is an assisted steering source, never a second physics
	# controller. Any real keyboard/pad/stick intent wins immediately.
	var manual_move: bool = absf(fwd) > 0.08 or absf(turn) > 0.08
	var tap_move_commanded := false
	if manual_move and m0.has_method("_on_touch_manual_move"):
		m0._on_touch_manual_move()
	elif not manual_move and m0.has_method("touch_auto_direction"):
		var auto_dir: Vector3 = m0.touch_auto_direction()
		if auto_dir.length() > 0.01:
			var desired_yaw: float = atan2(auto_dir.x, auto_dir.z)
			var yaw_error: float = wrapf(desired_yaw - yaw, -PI, PI)
			# A rearward tap used to rotate in place for ~1.7 s before Roshan
			# moved at all. Assisted steering gets a quicker turn ceiling and a
			# gentle early arc; the manual stick/keyboard path above is unchanged.
			turn = clampf(yaw_error * 2.0, -2.4, 2.4)
			if absf(yaw_error) < 2.6:
				fwd = clampf(1.0 - absf(yaw_error) / 2.6, 0.18, 1.0)
				tap_move_commanded = true
		# Elevated targets (portals, the penguin floe) need a climb/dive the
		# yaw/fwd steering above cannot give. Swim medium only: on dry land she
		# hops and breached in air she is ballistic — both keep their existing
		# rules, and the stall recovery owns whatever stays unreachable.
		if m0.has_method("touch_auto_vertical") and not land_dry and not (String(m0.game) == "" and position.y > WATER_TOP):
			var want_vy: float = m0.touch_auto_vertical()
			if absf(want_vy) > 0.05:
				vel.y = move_toward(vel.y, want_vy, 52.0 * delta)
				tap_move_commanded = true
	var jump_held: bool = Input.is_physical_key_pressed(KEY_SPACE) or joy_pressed(JOY_BUTTON_A) or joy_pressed(JOY_BUTTON_B)
	if "touch_ui" in m0 and m0.touch_ui != null and m0.touch_ui.action_down:
		jump_held = true

	jump_cool -= delta
	bump_verb_cool = maxf(0.0, bump_verb_cool - delta)
	var free_swim: bool = String(m0.game) == ""
	# no swim-kicks while breached above the surface — she is ballistic in air
	if jump_held and jump_cool <= 0.0 and not (free_swim and position.y > WATER_TOP):
		jump_cool = 0.4
		vel.y = 16.0
		if m0 != null and m0.has_method("on_player_jump"):
			m0.on_player_jump(position)   # surface splash ring near WATER_TOP

	yaw += turn * 1.8 * delta
	var dir := Vector3(sin(yaw), 0.0, cos(yaw))
	var smult := 1.0
	if "speed_mult" in m0:
		smult = float(m0.speed_mult)
	# media rules (ReefPhysics presets, applied inline): breaching the reef
	# surface swaps water rules for air — ballistic gravity, thin thrust
	# authority — and a buoyant band just under the waterline settles her into
	# a gentle bob instead of the old invisible ceiling clamp.
	if free_swim and position.y > WATER_TOP:
		vel += dir * fwd * 43.7 * smult * 0.3 * delta
		vel.y -= 30.0 * delta
		vel *= pow(0.90, delta)
	elif land_dry:
		# LAND medium (ReefPhysics.land_medium, applied inline; land_dry is
		# last frame's oracle — one frame of lag on the wet/dry switch is
		# invisible). Real-enough gravity keeps her on the grass between hops
		# but stays soft enough to hop rivers and reach every dream star; the
		# repeated jump impulse is deliberately kept, so holding A still
		# bounce-climbs like it always has. Ground friction bites only when
		# resting, stick idle AND already slow, so releasing the stick stops
		# the scoot instead of the old underwater glide — and a probe (or a
		# player) at commanded speed never feels it.
		vel += dir * fwd * 43.7 * smult * delta
		vel.y -= 20.0 * delta
		vel *= pow(0.15, delta)
		if land_rest and fwd == 0.0 and turn == 0.0 and vel.length() < 6.0:
			var gf: float = pow(0.001, delta)
			vel.x *= gf
			vel.z *= gf
	else:
		vel += dir * fwd * 43.7 * smult * delta      # 1.15x speed (x2 on beans)
		vel.y -= 13.0 * delta                # 1.3x weight
		vel *= pow(0.18, delta)
		if free_swim:
			var depth: float = WATER_TOP - position.y
			if depth < 4.5:
				vel.y += 34.0 * (1.0 - depth / 4.5) * delta
			# authored reef currents: stream rides + the breathing geyser lift
			if "flow_sys" in m0 and m0.flow_sys != null:
				vel += (m0.flow_sys.accel_at(position) as Vector3) * delta
	position += vel * delta
	if free_swim:
		var now_air: bool = position.y > WATER_TOP
		if now_air != was_airborne and absf(vel.y) > 5.0:
			if m0.has_method("on_player_jump"):
				m0.on_player_jump(Vector3(position.x, WATER_TOP - 1.0, position.z))
			if now_air and vel.y > 10.0 and verb == "":
				play_verb("twirl")   # a joyful breach pirouette
		was_airborne = now_air

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
		elif "northern_floor" in m and m.northern_floor:
			# The separately loaded northern kingdom has its own mountain-to-fjord
			# heightfield, with the same forgiving two-unit swim clearance.
			floor_a = m.northern_walk_h(position.x, position.z) + 2.0
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
				if zz.has("ramp"):
					# sloped stair floor: [axis (0=x, 2=z), p0, floor0, p1, floor1] —
					# the floor tracks the staircase so Roshan rests ON the steps
					# instead of swimming through them
					var rp: Array = zz["ramp"]
					var pv: float = lx if int(rp[0]) == 0 else lz
					var rt: float = clampf((pv - float(rp[1])) / (float(rp[3]) - float(rp[1])), 0.0, 1.0)
					floor_a = ap.y + lerpf(float(rp[2]), float(rp[4]), rt)
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
								if vel.x * sgx < -14.0 and bump_verb_cool <= 0.0 and verb == "":
									play_verb("boing")
									bump_verb_cool = 2.0
								vel.x = 0.0
						else:
							var sgz: float = signf(lz) if lz != 0.0 else 1.0
							position.z = s.cz + sgz * s.hz
							if vel.z * sgz < 0.0:
								if vel.z * sgz < -14.0 and bump_verb_cool <= 0.0 and verb == "":
									play_verb("boing")
									bump_verb_cool = 2.0
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
							if vn < -14.0 and bump_verb_cool <= 0.0 and verb == "":
								play_verb("boing")
								bump_verb_cool = 2.0
		# comic-hop oracle: is she resting on this arena floor, and is it dry?
		land_rest = position.y <= floor_a + 0.08
		land_dry = m.has_method("water_surface_y") and position.y >= float(m.water_surface_y(position.x, position.z))
	else:
		land_rest = false
		land_dry = false
		var floor_y: float = m.seabed_y(position.x, position.z) + 3.0
		if position.y < floor_y:
			position.y = floor_y
			vel.y = maxf(0.0, vel.y)
		if position.y > WATER_TOP + 14.0:
			# far above any breach arc — a safety net, not the old surface wall
			position.y = WATER_TOP + 14.0
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
						if vn < -14.0 and bump_verb_cool <= 0.0 and verb == "":
							play_verb("boing")   # a fast bonk is a toy, not a wall
							bump_verb_cool = 2.0

	rotation.y = yaw + PI
	# body language: bank into turns and pitch with climbs/dives — she arcs
	# like a fish instead of rotating flat (visual only; heading stays yaw)
	var spd_n: float = clampf(vel.length() / 26.0, 0.0, 1.0)
	var bank_t: float = clampf(turn, -1.0, 1.0) * (0.10 + 0.30 * spd_n)
	var pitch_t: float = clampf(vel.y * 0.020, -0.38, 0.34)
	rotation.z = lerpf(rotation.z, bank_t, 1.0 - pow(0.02, delta))
	rotation.x = lerpf(rotation.x, pitch_t, 1.0 - pow(0.03, delta))

	if fwd != 0.0 or turn != 0.0 or jump_held:
		idle_t = 0.0
	else:
		idle_t += delta

	var speed: float = vel.length()
	land_blend = move_toward(land_blend, 1.0 if land_dry else 0.0, delta * (4.0 if land_dry else 2.2))
	_tick_wake(delta, speed)
	_apply_land_pose(delta, speed)
	_tick_classic_sprite(speed, tap_move_commanded)
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
				# small idle repertoire so a quiet minute stays alive
				play_verb(["look", "hairtwirl", "hum"][randi() % 3])
				idle_verb_cool = 15.0
		elif land_blend > 0.7 and land_rest:
			# parked on dry land: sometimes she just gives up and flops over
			play_verb(["flop", "look", "hum"][randi() % 3])
			idle_verb_cool = 18.0

	# right-stick / right-drag / second-finger-drag camera: peek around and up
	# or down, then drift back behind her once every look input is released
	var rx: float = joy_axis(JOY_AXIS_RIGHT_X)
	var ry: float = joy_axis(JOY_AXIS_RIGHT_Y)
	var mlook: bool = Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)
	if "touch_ui" in _m0 and _m0.touch_ui != null and _m0.touch_ui.has_method("consume_look"):
		var tl: Vector2 = _m0.touch_ui.consume_look()
		mlook_x += tl.x
		mlook_y += tl.y
		mlook = mlook or bool(_m0.touch_ui.look_active())
	if absf(rx) > 0.25:
		cam_orbit = clampf(cam_orbit - rx * 2.6 * delta, -PI * 0.9, PI * 0.9)
	elif mlook:
		cam_orbit = clampf(cam_orbit - mlook_x * 0.005, -PI * 0.9, PI * 0.9)
	else:
		cam_orbit = lerpf(cam_orbit, 0.0, 1.0 - pow(0.35, delta))
	if absf(ry) > 0.25:
		cam_pitch_off = clampf(cam_pitch_off + ry * 9.0 * delta, -4.5, 8.0)
	elif mlook:
		cam_pitch_off = clampf(cam_pitch_off + mlook_y * 0.02, -4.5, 8.0)
	else:
		cam_pitch_off = lerpf(cam_pitch_off, 0.0, 1.0 - pow(0.35, delta))

	if cam != null and cam.is_inside_tree():
		var cyaw: float = yaw + cam_orbit
		# WW sail-stretch: the chase distance and lens breathe out a little at
		# sprint speed, so going fast LOOKS fast (identical at rest)
		var cam_spd: float = clampf(vel.length() / 26.0, 0.0, 1.0)
		var back_eff: float = cam_back * (1.0 + 0.10 * cam_spd)
		var target := position + Vector3(-sin(cyaw) * back_eff, cam_high + cam_pitch_off, -cos(cyaw) * back_eff)
		var focus := position + Vector3(0, 1.5, 0)
		# analytic boom (CAMERA_AUDIT_2026_07 P0): resolve the ideal spot
		# against walls/terrain/ceilings, glide toward it, then resolve the
		# glide too — so the boom shortens INSTANTLY when geometry intrudes
		# but relaxes back out smoothly once it has passed
		var want := CameraKit.resolve(_m0, focus, target)
		var glide := cam.position.lerp(want, 1.0 - pow(0.001, delta))
		cam.position = CameraKit.resolve(_m0, focus, glide)
		cam.look_at(focus)
		cam.fov = lerpf(cam.fov, 38.0 + 3.5 * cam_spd, 1.0 - pow(0.1, delta))

func _tick_swim_bones(delta: float, speed: float) -> void:
	# This legacy API name now advances only the 16-frame sprite-atlas clock.
	swim_phase += delta * (2.2 + speed * 0.9)
	arm_swim_phase += delta * (1.0 + minf(speed * 0.035, 0.9))

func snap_cam() -> void:
	# Place the chase camera at its resolved rest pose INSTANTLY. Call after
	# any teleport or mode handback: the worlds sit thousands of units apart
	# and the chase lerp would otherwise fly the lens through everything
	# between them for a full second.
	if cam == null or not cam.is_inside_tree():
		return
	cam_orbit = 0.0
	cam_pitch_off = 0.0
	var target := position + Vector3(-sin(yaw) * cam_back, cam_high, -cos(yaw) * cam_back)
	var focus := position + Vector3(0, 1.5, 0)
	cam.position = CameraKit.resolve(get_parent(), focus, target)
	cam.look_at(focus)

func _hop_visual_node() -> Node3D:
	if classic_sprite != null and classic_sprite.visible:
		return classic_sprite
	if skin_sprite != null and skin_sprite.visible:
		return skin_sprite
	return null

func _apply_land_pose(delta: float, speed: float) -> void:
	# The on-land hop layer (see the land locomotion vars). Runs after the
	# swim writes and before _apply_verb, so a wave or cheer still wins on top.
	if land_blend <= 0.01:
		hop_phase = 0.0
		hop_amp = 0.0
		hop_prev = 0.0
		if _hop_node != null:
			if is_instance_valid(_hop_node):
				_hop_node.position.y = _hop_base_y
				_hop_node.scale = _hop_base_scale
			_hop_node = null
		return
	var lb: float = land_blend
	var scooting: bool = land_rest and speed > 2.5
	hop_amp = move_toward(hop_amp, 1.0 if scooting else 0.0, delta * 5.0)
	if hop_amp > 0.01:
		hop_phase += delta * (6.5 + minf(speed * 0.35, 5.0))
	else:
		hop_phase = 0.0
	var hop: float = absf(sin(hop_phase)) * hop_amp
	if land_dry and not land_rest:
		# airborne over land (the big jump): tail springs out, arms fly up
		hop = maxf(hop, clampf(absf(vel.y) * 0.06, 0.0, 1.0))
	# touchdown: the bounce comes back down -> dust poof + boing at her tail
	if hop_prev >= 0.25 and hop < 0.10 and land_rest:
		if hop_dust != null:
			hop_dust.restart()
		var mh: Node = get_parent()
		if mh != null and mh.has_method("on_player_hop_land"):
			mh.on_player_hop_land()
		land_hops += 1
		if land_hops == 3 and mh != null and mh.has_method("show_msg"):
			# one giggle line per session, the first time she really scoots
			mh.show_msg("Roshan", "Hopping is hard work with a tail!", "talk")
	hop_prev = hop
	# Bounce the visible sprite, never the physics origin.
	var node: Node3D = _hop_visual_node()
	if node != _hop_node:
		if _hop_node != null and is_instance_valid(_hop_node):
			_hop_node.position.y = _hop_base_y
			_hop_node.scale = _hop_base_scale
		_hop_node = node
		if node != null:
			_hop_base_y = node.position.y
			_hop_base_scale = node.scale
	if node != null:
		node.position.y = _hop_base_y + hop * 1.1 * lb
		# squash-and-stretch: settled at contact, stretched at the top of the arc
		var sq: float = 1.0 + (hop - 0.35) * 0.14 * lb
		node.scale = _hop_base_scale * Vector3(2.0 - sq, sq, 2.0 - sq)

func _tick_wake(delta: float, speed: float) -> void:
	# WW motion language: contrail ribbon from the tail + dash particles at sprint speed
	var strength: float = clampf((speed - 7.0) / 16.0, 0.0, 1.0)
	strength *= 1.0 - land_blend   # no water contrail while hopping on dry land
	if speed_lines != null:
		var sprinting: bool = trail_enabled and speed > 26.0 and land_blend < 0.5
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
