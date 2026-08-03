class_name OctagonStage
extends RefCounted
# The OCTAGON STAGE — the shared BOSS ARENA rig, sibling to SideScrollStage.
#
# Why it exists (MINIGAME_ENGINES.md §1, duplication finding #4): combat_arena
# and dungeon_puzzle_room each carry their own copy of the same overhead ring
# — CENTER/RADIUS constants, a circle clamp, a fixed 3/4 camera, an avatar and
# an input read — and neither is reusable from a Family-A satellite. A boss
# encounter needs exactly that rig and nothing else, so it lives here once.
#
# What it gives a game:
#   open(cfg)            an eight-sided floor, low walls, corner posts, a
#                        fixed 3/4 camera that frames the WHOLE ring
#   tick(delta)          the one-finger read (drag ∥ stick ∥ keys ∥ pad-0),
#                        true octagon containment, face-the-run, tap edge
#   clamp_point(p, in)   the same containment for anything the game moves
#   flat()/glow()        cutout standees and additive halos, same as the
#                        side-scroll stage
#
# Child-first choices baked in: the camera NEVER follows and never pans, so
# nothing the child must watch can leave the screen; the ring is convex, so a
# finger dragged in any direction always makes progress and nobody can get
# wedged in a corner; there are no lights (CLAUDE.md: no new OmniLights) —
# the ring reads through unshaded pastel material and additive post halos.
#
# Satellite rules per CLAUDE.md: logic only, `main` by reference, all state on
# m.g ("oc_*" keys), every node under one root registered in m.game_nodes so
# _clear_game reclaims the whole arena.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ---- stage -----------------------------------------------------------------
func open(cfg: Dictionary) -> void:
	# cfg: origin, radius (circumradius), wall_h, floor_col, trim_col,
	# post_col, speed, hover, bob_amp, cam_h, cam_dist, look_h, cam_fov,
	# inset (how far inside the wall the walkable area stops)
	m.g["oc_cfg"] = cfg
	m.g["oc_bob"] = 0.0
	m.g["oc_tap_prev"] = false
	var rt := Node3D.new()
	rt.position = cfg.get("origin", m.ARENA_POS)
	m.add_child(rt)
	m.game_nodes.append(rt)
	m.g["oc_root"] = rt
	var radius: float = float(cfg.get("radius", 26.0))
	var wall_h: float = float(cfg.get("wall_h", 5.2))
	var floor_col: Color = cfg.get("floor_col", Color(0.84, 0.78, 0.90)) as Color
	var trim_col: Color = cfg.get("trim_col", Color(0.72, 0.66, 0.86)) as Color
	var post_col: Color = cfg.get("post_col", Color(0.95, 0.90, 0.99)) as Color
	# the floor IS an octagon: an 8-segment cylinder, rotated so a flat side
	# faces the camera instead of a vertex
	var floor_mi := MeshInstance3D.new()
	var fm := CylinderMesh.new()
	fm.top_radius = radius
	fm.bottom_radius = radius
	fm.height = 0.7
	fm.radial_segments = 8
	fm.rings = 1
	floor_mi.mesh = fm
	floor_mi.position = Vector3(0, -0.35, 0)
	floor_mi.rotation.y = PI / 8.0
	floor_mi.material_override = m._soft_mat(floor_col, 0.05)
	floor_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	rt.add_child(floor_mi)
	# a smaller concentric ring on the deck: it reads as a duelling circle and
	# gives the eye a centre without any text
	var ring := MeshInstance3D.new()
	var rm := CylinderMesh.new()
	rm.top_radius = radius * 0.55
	rm.bottom_radius = radius * 0.55
	rm.height = 0.12
	rm.radial_segments = 8
	rm.rings = 1
	ring.mesh = rm
	ring.position = Vector3(0, 0.06, 0)
	ring.rotation.y = PI / 8.0
	ring.material_override = m._soft_mat(trim_col, 0.10)
	ring.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	rt.add_child(ring)
	# eight low walls on the apothem + eight corner posts on the vertices
	var apo: float = apothem(radius)
	var side: float = 2.0 * radius * sin(PI / 8.0)
	for i in range(8):
		var ang: float = float(i) * PI / 4.0
		var wall := MeshInstance3D.new()
		var wm := BoxMesh.new()
		wm.size = Vector3(side + 0.6, wall_h, 1.1)
		wall.mesh = wm
		wall.position = Vector3(cos(ang) * (apo + 0.55), wall_h * 0.5, sin(ang) * (apo + 0.55))
		wall.rotation.y = -ang + PI * 0.5
		wall.material_override = m._soft_mat(trim_col, 0.05)
		wall.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		rt.add_child(wall)
		var vang: float = PI / 8.0 + float(i) * PI / 4.0
		var post := MeshInstance3D.new()
		var pm := CylinderMesh.new()
		pm.top_radius = 1.05
		pm.bottom_radius = 1.25
		pm.height = wall_h * 1.75
		post.mesh = pm
		post.position = Vector3(cos(vang) * radius, wall_h * 0.875, sin(vang) * radius)
		post.material_override = m._soft_mat(post_col, 0.10)
		post.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		rt.add_child(post)
		# a pastel lamp bead on each post — additive halo, never a real light
		var bead := glow(cfg.get("post_glow", Color(1.0, 0.90, 0.72)) as Color, 6.0)
		bead.position = post.position + Vector3(0, wall_h * 0.95, 0)
		rt.add_child(bead)
	# park the player just inside the ring, facing the middle, camera fixed
	var origin: Vector3 = rt.position
	var start: Vector2 = cfg.get("start", Vector2(0.0, radius * 0.62)) as Vector2
	m.player.position = origin + Vector3(start.x, float(cfg.get("hover", 1.05)), start.y)
	m.player.vel = Vector3.ZERO
	m.player.rotation.y = PI
	fit_camera()

func fit_camera() -> void:
	# Solve the framing ONCE against the real projection, then let
	# frame_camera() re-assert the solved pose every tick.
	#
	# Framing a boss arena by eye is how the action ends up off the phone: the
	# 2026-08-02 stress test found Roshan projecting to y=975 on a 1280x720
	# canvas — she was simply below the screen while every headless probe
	# passed. So the stage now pushes the lens back until the three points
	# that MUST be readable are inside the safe area:
	#   • the near rim of the ring at standing height (where the child is)
	#   • the far rim (so the ring reads as an enclosed place)
	#   • the apex of a leap plus the icon above it (the tell)
	var r := root()
	var cam: Camera3D = m.player.cam if m.player != null else null
	if r == null or cam == null or not cam.is_inside_tree():
		return
	var cfg: Dictionary = m.g.get("oc_cfg", {})
	var radius: float = float(cfg.get("radius", 26.0))
	var head: float = float(cfg.get("headroom", radius * 0.8))
	var apo: float = apothem(radius)
	var stand: float = float(cfg.get("hover", 1.05)) + 1.5
	var vp: Vector2 = Vector2(1280.0, 720.0)
	if cam.get_viewport() != null:
		vp = cam.get_viewport().get_visible_rect().size
	var margin: float = vp.y * 0.06
	var dist: float = radius * 1.55
	var high: float = radius * 1.15
	cam.fov = float(cfg.get("cam_fov", 55.0))
	for _step in range(26):
		cam.position = r.position + Vector3(0.0, high, dist)
		cam.look_at(r.position + Vector3(0.0, head * 0.42, 0.0))
		var near_p: Vector2 = cam.unproject_position(r.position + Vector3(0.0, stand, apo))
		var far_p: Vector2 = cam.unproject_position(r.position + Vector3(0.0, stand, -apo))
		var top_p: Vector2 = cam.unproject_position(r.position + Vector3(0.0, head, 0.0))
		if near_p.y <= vp.y - margin and top_p.y >= margin and far_p.y >= margin:
			break
		dist *= 1.07
		high *= 1.05
	m.g["oc_cam_pos"] = cam.position - r.position
	m.g["oc_cam_look"] = Vector3(0.0, head * 0.42, 0.0)

func frame_camera() -> void:
	# THE FRAMING IS DERIVED FROM THE RING, and re-asserted every tick.
	#
	# Two lessons from the 2026-08-02 boss stress test are baked in here:
	# (1) a mode that sets the lens ONCE loses it — player.gd re-aims the
	#     free-swim chase cam every frame for any game id missing from its
	#     ownership list, so the stage must keep asserting;
	# (2) framing the floor is not enough. A boss LEAPS, and the tell sits
	#     over his head, so the frame must contain radius*2 across AND the
	#     apex of the leap plus the icon above it — otherwise the one thing
	#     the child must read is cropped off the top of the phone.
	var r := root()
	var cam: Camera3D = m.player.cam if m.player != null else null
	if r == null or cam == null or not cam.is_inside_tree():
		return
	if not m.g.has("oc_cam_pos"):
		fit_camera()
		return
	var cfg: Dictionary = m.g.get("oc_cfg", {})
	cam.fov = float(cfg.get("cam_fov", 55.0))
	var offset: Vector3 = m.g["oc_cam_pos"]
	var look: Vector3 = m.g["oc_cam_look"]
	cam.position = r.position + offset
	cam.look_at(r.position + look)

func root() -> Node3D:
	return m.g.get("oc_root") as Node3D

func close() -> void:
	# nodes are reclaimed by _clear_game via game_nodes; just undo the lean so
	# Roshan is upright when the reef chase-cam resumes
	if m.player != null:
		m.player.rotation.z = 0.0

# ---- the ring ---------------------------------------------------------------
static func apothem(radius: float) -> float:
	return radius * cos(PI / 8.0)

func clamp_point(p: Vector2, inset: float = 0.0) -> Vector2:
	# TRUE octagon containment: the ring is the intersection of eight
	# half-planes, so push the point back inside each one it has left. Two
	# passes, because pushing off one edge can cross the neighbouring edge at
	# a corner. Analytic and allocation-free — probes stay deterministic.
	var cfg: Dictionary = m.g.get("oc_cfg", {})
	var limit: float = apothem(float(cfg.get("radius", 26.0))) - inset
	var q: Vector2 = p
	for _pass in range(2):
		for i in range(8):
			var n := Vector2(cos(float(i) * PI / 4.0), sin(float(i) * PI / 4.0))
			var d: float = q.dot(n)
			if d > limit:
				q -= n * (d - limit)
	return q

func player_local() -> Vector2:
	var r := root()
	if r == null:
		return Vector2.ZERO
	return Vector2(m.player.position.x - r.position.x, m.player.position.z - r.position.z)

# ---- the one-finger read ----------------------------------------------------
func tick(delta: float) -> Dictionary:
	# returns {mx, mz, px, pz, tap, moved}. Pad reads are DEVICE 0 ONLY, the
	# same convention as the side-scroll stage's brawl mode.
	var cfg: Dictionary = m.g.get("oc_cfg", {})
	var r := root()
	if r == null:
		return {"mx": 0.0, "mz": 0.0, "px": 0.0, "pz": 0.0, "tap": false, "moved": false}
	var mx := 0.0
	var mz := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		mx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		mx += 1.0
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W):
		mz -= 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		mz += 1.0
	var pads: Array = Input.get_connected_joypads()
	if pads.size() > 0:
		var jx: float = Input.get_joy_axis(int(pads[0]), JOY_AXIS_LEFT_X)
		var jy: float = Input.get_joy_axis(int(pads[0]), JOY_AXIS_LEFT_Y)
		if absf(jx) > 0.2:
			mx += jx
		if absf(jy) > 0.2:
			mz += jy
	if m.touch_ui != null:
		var tv: Vector2 = m.touch_ui.stick_vec
		if absf(tv.x) > 0.15:
			mx += tv.x
		if absf(tv.y) > 0.15:
			mz += tv.y
	mx = clampf(mx, -1.0, 1.0)
	mz = clampf(mz, -1.0, 1.0)
	var spd: float = float(cfg.get("speed", 24.0))
	var here: Vector2 = player_local() + Vector2(mx, mz) * spd * delta
	here = clamp_point(here, float(cfg.get("inset", 2.6)))
	m.g["oc_bob"] = float(m.g.get("oc_bob", 0.0)) + delta
	var hover: float = float(cfg.get("hover", 1.05)) \
		+ sin(float(m.g["oc_bob"]) * 2.2) * float(cfg.get("bob_amp", 0.35))
	m.player.position = r.position + Vector3(here.x, hover, here.y)
	m.player.vel = Vector3.ZERO
	if absf(mx) > 0.1 or absf(mz) > 0.1:
		m.player.rotation.y = lerp_angle(m.player.rotation.y, atan2(mx, mz), 1.0 - pow(0.002, delta))
	m.player.rotation.z = lerpf(m.player.rotation.z, -mx * 0.14, 1.0 - pow(0.001, delta))
	frame_camera()
	# tap edge: touch tap ∥ fresh action_down ∥ Space ∥ pad-0 A
	var down: bool = Input.is_physical_key_pressed(KEY_SPACE)
	if pads.size() > 0:
		down = down or Input.is_joy_button_pressed(int(pads[0]), JOY_BUTTON_A)
	if m.touch_ui != null and m.touch_ui.action_down:
		down = true
	var tap: bool = down and not bool(m.g.get("oc_tap_prev", false))
	m.g["oc_tap_prev"] = down
	if m.touch_ui != null and m.touch_ui.consume_action_just():
		tap = true
	return {"mx": mx, "mz": mz, "px": here.x, "pz": here.y, "tap": tap,
		"moved": absf(mx) > 0.05 or absf(mz) > 0.05}

# ---- dressing ---------------------------------------------------------------
func flat(tex_path: String, size: Vector2, x: float, z: float, y: float = 0.0, shadow: bool = true) -> Node3D:
	# a cutout standee standing at a real spot in the ring — unshaded, never
	# re-lit, bottom edge of the art is the ground line (art direction
	# 2026-07-27; same contract as SideScrollStage.flat)
	var r := root()
	if r == null or not ResourceLoader.exists(tex_path):
		return null
	var holder := Node3D.new()
	holder.position = Vector3(x, 0.0, z)
	r.add_child(holder)
	var q := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = size
	q.mesh = qm
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	mat.albedo_texture = load(tex_path)
	q.material_override = mat
	q.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	q.position = Vector3(0, size.y * 0.5 + y, 0)
	holder.add_child(q)
	if shadow:
		holder.add_child(contact_shadow(size.x * 0.6))
	return holder

func contact_shadow(width: float) -> MeshInstance3D:
	var sq := MeshInstance3D.new()
	var sqm := QuadMesh.new()
	sqm.size = Vector2(width, width)
	sq.mesh = sqm
	sq.rotation_degrees.x = -90.0
	var sm := StandardMaterial3D.new()
	sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	sm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	sm.albedo_color = Color(0.16, 0.28, 0.45, 0.26)
	sq.material_override = sm
	sq.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	sq.position = Vector3(0, 0.12, 0)
	return sq

func glow(col: Color, size: float) -> MeshInstance3D:
	# unparented additive billboard halo — the arena's only light source
	var gt := GradientTexture2D.new()
	gt.fill = GradientTexture2D.FILL_RADIAL
	gt.fill_from = Vector2(0.5, 0.5)
	gt.fill_to = Vector2(0.5, 0.0)
	var gr := Gradient.new()
	gr.set_color(0, Color(col.r, col.g, col.b, 0.5))
	gr.set_color(1, Color(col.r, col.g, col.b, 0.0))
	gt.gradient = gr
	var qm := QuadMesh.new()
	qm.size = Vector2(size, size)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	mat.albedo_texture = gt
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	qm.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = qm
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return mi
