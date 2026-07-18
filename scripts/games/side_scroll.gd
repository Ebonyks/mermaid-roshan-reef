class_name SideScrollStage
extends RefCounted
# Phase 8: the SIDE-SCROLL STAGE engine — one shared 2.5D rig for "flat
# stage" minigames. It puts the REAL player node (the rigged 3D Roshan with
# whatever wardrobe skin she is wearing) on a left/right line in front of a
# side-on camera, and owns the one-finger composite input read
# (drag-to-point ∥ virtual stick ∥ arrows/AD ∥ gamepad axis). Games built on
# it own only their objective logic and set dressing.
#   catch mode:  tick(delta)      — steer left/right under falling things
#   run mode:    run_tick(delta)  — auto-run + tap-to-hop (Mario-run style
#                one-touch games; the engine seam is here, no game uses it yet)
# First client: the dolls nursery (games/dolls.gd). Candidates to migrate:
# the picture-game snowman chase (same catcher verb) and future runners.
# Satellite rules per CLAUDE.md: logic only — all state lives on main
# (m.g "ss_*" keys, freed with the rest of the game scratch by _clear_game;
# every node is registered in m.game_nodes so _clear_game reclaims it).

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ---- stage -----------------------------------------------------------------
func open(cfg: Dictionary) -> void:
	# cfg: origin (stage floor center, world), half_w, hover (avatar float
	# height), cam_h / cam_dist / look_h / cam_follow (side-on framing),
	# bob_amp, backdrop (texture path, optional), backdrop_size (Vector2),
	# backdrop_z, run_speed / jump_v / gravity (run mode).
	# Scale note: the v4 Roshan is ~7 world units tall (3.7× model scale in
	# player.gd) — size stages against HER, not against a 2-unit toy.
	m.g["ss_cfg"] = cfg
	m.g["ss_bob"] = 0.0
	m.g["ss_run_x"] = 0.0
	m.g["ss_run_vy"] = 0.0
	var rt := Node3D.new()
	rt.position = cfg.get("origin", m.ARENA_POS)
	m.add_child(rt)
	m.game_nodes.append(rt)
	m.g["ss_root"] = rt
	var bpath: String = String(cfg.get("backdrop", ""))
	if bpath != "" and ResourceLoader.exists(bpath):
		var bq := MeshInstance3D.new()
		var qm := QuadMesh.new()
		qm.size = cfg.get("backdrop_size", Vector2(16, 9)) as Vector2
		bq.mesh = qm
		var bm := StandardMaterial3D.new()
		bm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bm.albedo_texture = load(bpath)
		bq.material_override = bm
		bq.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		bq.position = Vector3(0, (qm.size.y as float) * 0.5 + 0.4, float(cfg.get("backdrop_z", -7.0)))
		rt.add_child(bq)
	# park Roshan mid-stage facing the camera, camera snapped side-on
	var origin: Vector3 = rt.position
	m.player.position = origin + Vector3(0, float(cfg.get("hover", 1.05)), 0)
	m.player.vel = Vector3.ZERO
	m.player.rotation.y = PI
	if m.player.cam != null and m.player.cam.is_inside_tree():
		m.player.cam.position = origin + Vector3(0, float(cfg.get("cam_h", 12.0)), float(cfg.get("cam_dist", 20.5)))
		m.player.cam.look_at(origin + Vector3(0, float(cfg.get("look_h", 10.5)), 0))

func root() -> Node3D:
	return m.g.get("ss_root") as Node3D

func px() -> float:
	# avatar x in stage-local units (0 = stage center)
	var r := root()
	if r == null:
		return 0.0
	return m.player.position.x - r.position.x

func close() -> void:
	# nodes are reclaimed by _clear_game via game_nodes; just undo the lean
	# so Roshan is upright when the reef chase-cam resumes. Safe to call
	# when the stage never opened (it runs for every game teardown).
	if m.player != null:
		m.player.rotation.z = 0.0

# ---- catch mode: steer on a line -------------------------------------------
func tick(delta: float) -> Dictionary:
	# returns {mx, px, moved} — game code layers objectives on top
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var r := root()
	if r == null:
		return {"mx": 0.0, "px": 0.0, "moved": false}
	var half_w: float = float(cfg.get("half_w", 23.2))
	var mx := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		mx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		mx += 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		mx += jx
	if m.touch_ui != null and absf((m.touch_ui.stick_vec as Vector2).x) > 0.15:
		mx += (m.touch_ui.stick_vec as Vector2).x
	mx = clampf(mx, -1.0, 1.0)
	var x := px()
	var pointing := false
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		# point-and-she-swims-there: finger/mouse screen x maps to stage x
		# (touch reaches here through Godot's emulated mouse, same as the old
		# 2D catcher's drag control)
		var vp := m.get_viewport()
		if vp != null:
			var vsz: Vector2 = vp.get_visible_rect().size
			if vsz.x > 1.0:
				var t: float = clampf(vp.get_mouse_position().x / vsz.x, 0.0, 1.0)
				x = lerpf(x, (t * 2.0 - 1.0) * half_w * 1.05, 0.2)
				pointing = true
	x = clampf(x + mx * float(cfg.get("steer_speed", 24.8)) * delta, -half_w, half_w)
	m.g["ss_bob"] = float(m.g.get("ss_bob", 0.0)) + delta
	var hover: float = float(cfg.get("hover", 3.0)) + sin(float(m.g["ss_bob"]) * 2.2) * float(cfg.get("bob_amp", 0.5))
	m.player.position = r.position + Vector3(x, hover, 0)
	m.player.vel = Vector3.ZERO
	# storybook body language: face the camera, lean into the dash
	m.player.rotation.y = PI - mx * 0.45
	m.player.rotation.z = lerpf(m.player.rotation.z, -mx * 0.22, 1.0 - pow(0.001, delta))
	_glide_camera(delta, cfg, r, x * float(cfg.get("cam_follow", 0.25)))
	return {"mx": mx, "px": x, "moved": absf(mx) > 0.05 or pointing}

# ---- run mode: auto-run + tap-to-hop (future Mario-run games) --------------
func run_tick(delta: float) -> Dictionary:
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var r := root()
	if r == null:
		return {"x": 0.0, "y": 0.0, "grounded": true, "hopped": false}
	var x: float = float(m.g.get("ss_run_x", 0.0)) + float(cfg.get("run_speed", 20.0)) * delta
	var vy: float = float(m.g.get("ss_run_vy", 0.0))
	var hover: float = float(cfg.get("hover", 3.0))
	var y: float = m.player.position.y - r.position.y
	var grounded: bool = y <= hover + 0.02 and vy <= 0.0
	var hopped := false
	var tap: bool = Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A)
	if m.touch_ui != null and m.touch_ui.consume_action_just():
		tap = true
	if tap and grounded:
		vy = float(cfg.get("jump_v", 30.0))
		hopped = true
	vy -= float(cfg.get("gravity", 64.0)) * delta
	y = maxf(hover, y + vy * delta)
	if y <= hover:
		vy = 0.0
	m.g["ss_run_x"] = x
	m.g["ss_run_vy"] = vy
	m.player.position = r.position + Vector3(x, y, 0)
	m.player.vel = Vector3.ZERO
	m.player.rotation.y = PI - 0.9   # running toward screen-right
	_glide_camera(delta, cfg, r, x)
	return {"x": x, "y": y, "grounded": y <= hover + 0.02, "hopped": hopped}

func _glide_camera(delta: float, cfg: Dictionary, r: Node3D, follow_x: float) -> void:
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return
	var goal: Vector3 = r.position + Vector3(follow_x, float(cfg.get("cam_h", 12.0)), float(cfg.get("cam_dist", 20.5)))
	cam.position = cam.position.lerp(goal, 1.0 - pow(0.002, delta))
	cam.look_at(r.position + Vector3(follow_x, float(cfg.get("look_h", 10.5)), 0))

# ---- shared bits for stage dressing ----------------------------------------
func glow(col: Color, size: float) -> MeshInstance3D:
	# unparented additive billboard glow — halo for pickups / fallers
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
