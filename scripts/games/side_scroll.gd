class_name SideScrollStage
extends RefCounted
# Phase 8: the SIDE-SCROLL STAGE engine — one shared 2.5D rig for "flat
# stage" minigames. It puts the real player CONTROLLER on a left/right line in
# front of a side-on camera. Clients provide a 2D avatar sprite; the controller
# stays responsible for movement while its retired model visuals remain hidden.
# The engine owns the one-finger composite input read
# (drag-to-point ∥ virtual stick ∥ arrows/AD ∥ gamepad axis). Games built on
# it own only their objective logic and set dressing.
#   catch mode:  tick(delta)       — steer left/right under falling things
#   run mode:    run_tick(delta)   — auto-run + tap-to-hop (Mario-run style
#                one-touch games; the engine seam is here, no game uses it yet)
#   walk mode:   walk_tick(delta)  — touch-the-world promenade travel for the
#                2.5D world redesign (GAME_REDESIGN_2P5D_2026-07-27.md):
#                tap/hold the world and Roshan travels there; stick/pad/keys
#                merged as an override. Engine seam — no client yet (P2 is
#                the reef promenade pilot).
#   brawl mode:  brawl_tick(delta) — walk-the-plane with DEPTH (Castle
#                Crashers style): x + z inside a band, sliding stage bounds,
#                facing the run, tap = the bop. Plus a two-hero companion
#                (companion_open/companion_tick): AI-driven by default, a
#                second gamepad takes over live and hands back after idling.
# Clients: dolls nursery (catch), toy-castle brawler (brawl). Candidates to
# migrate: the picture-game snowman chase (same catcher verb), future runners.
# Satellite rules per CLAUDE.md: logic only — all state lives on main
# (m.g "ss_*" keys, freed with the rest of the game scratch by _clear_game;
# every node is registered in m.game_nodes so _clear_game reclaims it).

var m: ReefMain

const CONTACT_SHADOW := "res://assets/minigames/shared/contact_shadow.svg"
const FLAT_PLACEHOLDER := "res://assets/minigames/shared/flat_placeholder.svg"

func _init(main: ReefMain) -> void:
	m = main

# ---- stage -----------------------------------------------------------------
func open(cfg: Dictionary) -> void:
	# cfg: origin (stage floor center, world), half_w, hover (avatar float
	# height), cam_h / cam_dist / look_h / cam_follow (side-on framing),
	# cam_fov (locks the lens for the whole stage — 0/absent leaves whatever
	# the chase cam last set), bob_amp, backdrop (texture path, optional),
	# backdrop_size (Vector2), backdrop_z, run_speed / jump_v / gravity (run
	# mode), layers (parallax flat stack, back-to-front: [{tex, size, y, z,
	# lock, alpha, tile}] — lock ∈ [0,1] is the camera-follow factor, 0 =
	# pinned to the stage, 1 = rides the camera like a sky; tile repeats the
	# quad sideways).
	# THE MURAL IS THE SCREEN (owner note 2026-07-27): screen_half_w +
	# screen_z declare the painted wall's half-width and depth, and the camera
	# glide then REFUSES to pan past its painted edges, so the frame is always
	# filled by the painting and never by raw environment sky.
	# Scale note: the v4 Roshan is ~7 world units tall (3.7× model scale in
	# player.gd) — size stages against HER, not against a 2-unit toy.
	m.g["ss_cfg"] = cfg
	m.g["ss_bob"] = 0.0
	m.g["ss_run_x"] = 0.0
	m.g["ss_run_vy"] = 0.0
	var avatar_path: String = String(cfg.get("avatar_sprite", ""))
	if avatar_path != "" and ResourceLoader.exists(avatar_path):
		m.player.set_skin("__minigame_2d", avatar_path)
	var rt := Node3D.new()
	rt.position = cfg.get("origin", m.ARENA_POS)
	m.add_child(rt)
	m.game_nodes.append(rt)
	m.g["ss_root"] = rt
	var bpath: String = String(cfg.get("backdrop", ""))
	if bpath != "" and ResourceLoader.exists(bpath):
		var bq := Sprite3D.new()
		var backdrop_texture: Texture2D = load(bpath)
		var backdrop_size: Vector2 = cfg.get("backdrop_size", Vector2(16, 9)) as Vector2
		bq.texture = backdrop_texture
		bq.pixel_size = 1.0 / maxf(1.0, float(backdrop_texture.get_height()))
		var backdrop_base_width: float = float(backdrop_texture.get_width()) * bq.pixel_size
		bq.scale = Vector3(backdrop_size.x / backdrop_base_width, backdrop_size.y, 1.0)
		bq.billboard = BaseMaterial3D.BILLBOARD_DISABLED
		bq.shaded = false
		bq.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
		bq.position = Vector3(0, backdrop_size.y * 0.5 + 0.4, float(cfg.get("backdrop_z", -7.0)))
		rt.add_child(bq)
	# the parallax flat stack (world redesign P1) — each layer is a holder
	# node the camera glide slides by its lock factor; tiles repeat sideways
	# so a wide promenade never runs out of painting
	var stack: Array = []
	for ld_v in (cfg.get("layers", []) as Array):
		var ld: Dictionary = ld_v as Dictionary
		var lpath: String = String(ld.get("tex", ""))
		if lpath == "" or not ResourceLoader.exists(lpath):
			continue
		var holder := Node3D.new()
		holder.position = Vector3(0, 0, float(ld.get("z", -20.0)))
		rt.add_child(holder)
		var lsize: Vector2 = ld.get("size", Vector2(32, 16)) as Vector2
		var ltex: Texture2D = load(lpath)
		var tiles: int = maxi(1, int(ld.get("tile", 1)))
		for i in tiles:
			var lq := Sprite3D.new()
			lq.texture = ltex
			lq.pixel_size = 1.0 / maxf(1.0, float(ltex.get_height()))
			var layer_base_width: float = float(ltex.get_width()) * lq.pixel_size
			lq.scale = Vector3(lsize.x / layer_base_width, lsize.y, 1.0)
			lq.billboard = BaseMaterial3D.BILLBOARD_DISABLED
			lq.shaded = false
			lq.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED if not bool(ld.get("alpha", false)) else SpriteBase3D.ALPHA_CUT_DISCARD
			lq.position = Vector3((float(i) - float(tiles - 1) * 0.5) * lsize.x,
				lsize.y * 0.5 + float(ld.get("y", 0.0)), 0.0)
			holder.add_child(lq)
		stack.append({"node": holder, "lock": clampf(float(ld.get("lock", 0.0)), 0.0, 1.0)})
	m.g["ss_layers"] = stack
	# park Roshan mid-stage facing the camera, camera snapped side-on
	var origin: Vector3 = rt.position
	m.player.position = origin + Vector3(0, float(cfg.get("hover", 1.05)), 0)
	m.player.vel = Vector3.ZERO
	m.player.rotation.y = PI
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var lens: float = float(cfg.get("cam_fov", 0.0))
		if lens > 0.0:
			m.player.cam.fov = lens
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
		m._apply_skin()

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

# ---- walk mode: touch-the-world promenade travel (world redesign P1) -------
func walk_tick(delta: float) -> Dictionary:
	# The promenade verb (GAME_REDESIGN_2P5D_2026-07-27.md): tap or hold the
	# world and Roshan travels there — the press is projected through the
	# real camera onto the vertical stage plane, screen height mapped into
	# the depth band. A tap's goal persists until arrival (assisted travel,
	# same contract as Hybrid); any stick/pad/key input cancels the goal
	# instantly and steers directly (the Hybrid manual-override rule). No
	# tap-button semantics here — in the world, tap belongs to the
	# interaction director. Returns {px, pz, moved, pointing, arrived}.
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var r := root()
	if r == null:
		return {"px": 0.0, "pz": 0.0, "moved": false, "pointing": false, "arrived": true}
	var half_w: float = float(cfg.get("half_w", 23.2))
	var half_d: float = float(cfg.get("half_d", 7.0))
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
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = m.joy_axis(JOY_AXIS_LEFT_Y)
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
	var spd: float = float(cfg.get("steer_speed", 24.8))
	var x := px()
	var z: float = m.player.position.z - r.position.z
	var manual: bool = absf(mx) > 0.05 or absf(mz) > 0.05
	var pointing := false
	var moved := manual
	var dx := 0.0
	if manual:
		m.g["ss_walk_goal"] = null
		x = clampf(x + mx * spd * delta, -half_w, half_w)
		z = clampf(z + mz * spd * 0.8 * delta, -half_d, half_d)
		dx = mx
	else:
		if bool(cfg.get("touch_travel", true)) and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
			# finger -> ray -> the stage plane; screen height on that plane maps
			# into the depth band. Touch reaches here through Godot's emulated
			# mouse. A stage that routes presses itself (a promenade whose
			# standees are tappable) sets touch_travel false and calls
			# plane_goal() for the presses its director judges to be travel.
			var vp := m.get_viewport()
			if vp != null:
				var goal_here: Variant = plane_goal(vp.get_mouse_position())
				if goal_here is Vector2:
					m.g["ss_walk_goal"] = goal_here
					pointing = true
		var goal_v: Variant = m.g.get("ss_walk_goal")
		if goal_v is Vector2:
			var goal := goal_v as Vector2
			var to := Vector2(goal.x - x, goal.y - z)
			if to.length() <= float(cfg.get("arrive_r", 1.2)):
				m.g["ss_walk_goal"] = null
			else:
				var step := to.limit_length(spd * delta)
				x = clampf(x + step.x, -half_w, half_w)
				z = clampf(z + step.y, -half_d, half_d)
				dx = to.normalized().x
				moved = true
	var walk_route: Array = cfg.get("route", [])
	if walk_route.size() >= 2:
		# on the spine: the path owns her x range and her depth, so a tap that
		# lands off the painted way still walks her along it
		var span: Vector2 = route_span(cfg)
		x = clampf(x, span.x, span.y)
		z = 0.0
	if bool(cfg.get("keep_on_screen", false)):
		x = keep_on_screen(cfg, x)
	m.g["ss_bob"] = float(m.g.get("ss_bob", 0.0)) + delta
	var base_hover: float = float(cfg.get("hover", 3.0))
	if walk_route.size() >= 2:
		base_hover = route_y(cfg, x, base_hover)
	var hover: float = base_hover + sin(float(m.g["ss_bob"]) * 2.2) * float(cfg.get("bob_amp", 0.5))
	if swell_amp() > 0.0:
		# Roshan rides the same tide as the props and layers — analytically,
		# never on a body (her hover just samples the shared wave)
		hover += sin(swell_phase(x) + 0.9) * 0.35 * swell_amp()
	m.player.position = r.position + Vector3(x, hover, z)
	m.player.vel = Vector3.ZERO
	# face the run: screen-left/right while traveling, the camera when idle
	var want_rot: float = PI
	if absf(dx) > 0.1:
		want_rot = -PI * 0.5 if dx > 0.0 else PI * 0.5
	m.player.rotation.y = lerp_angle(m.player.rotation.y, want_rot, 1.0 - pow(0.002, delta))
	m.player.rotation.z = lerpf(m.player.rotation.z, -dx * 0.16, 1.0 - pow(0.001, delta))
	_glide_camera(delta, cfg, r, x * float(cfg.get("cam_follow", 0.25)))
	return {"px": x, "pz": z, "moved": moved, "pointing": pointing,
		"arrived": not (m.g.get("ss_walk_goal") is Vector2)}

func plane_goal(screen_pos: Vector2) -> Variant:
	# THE promenade projection, in one place: a screen press → the walk band.
	# The ray is crossed with the vertical stage plane at z 0; the hit's height
	# is read through the band window (band_y .. band_y + band_h) so the front
	# of the window is the near edge of the depth band and the back of it the
	# far edge. Returns a stage-local Vector2(x, z) goal, or null when the press
	# cannot reach the plane at all. Both the engine's own hold-to-travel and a
	# client's tap router call this, so the two can never drift apart.
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var r := root()
	var cam: Camera3D = m.player.cam
	if r == null or cam == null or not cam.is_inside_tree():
		return null
	var from: Vector3 = cam.project_ray_origin(screen_pos)
	var dirv: Vector3 = cam.project_ray_normal(screen_pos)
	if absf(dirv.z) <= 0.001:
		return null
	var t: float = (r.position.z - from.z) / dirv.z
	if t <= 0.0:
		return null
	var hit: Vector3 = from + dirv * t
	var half_w: float = float(cfg.get("half_w", 23.2))
	var half_d: float = float(cfg.get("half_d", 7.0))
	var band_y: float = float(cfg.get("band_y", 0.0))
	var band_h: float = maxf(0.01, float(cfg.get("band_h", 6.0)))
	var gz: float = remap(clampf(hit.y - r.position.y - band_y, 0.0, band_h),
		0.0, band_h, half_d, -half_d)
	var gx: float = clampf(hit.x - r.position.x, -half_w, half_w)
	if (cfg.get("route", []) as Array).size() >= 2:
		# a press anywhere on the screen resolves ONTO the walkable path
		var span: Vector2 = route_span(cfg)
		return Vector2(clampf(gx, span.x, span.y), 0.0)
	return Vector2(gx, gz)

func view_half_size(cfg: Dictionary, cam: Camera3D, plane_z: float) -> Vector2:
	# Half (width, height) of the frustum where it crosses a stage-local depth,
	# in world units. Camera3D keeps the VERTICAL fov (KEEP_HEIGHT), so height
	# is device-independent and width grows with the phone's aspect.
	var aspect := 16.0 / 9.0
	var vp := m.get_viewport()
	if vp != null:
		var vsz: Vector2 = vp.get_visible_rect().size
		if vsz.y > 1.0:
			aspect = vsz.x / vsz.y
	var dist: float = absf(float(cfg.get("cam_dist", 20.5)) - plane_z)
	var half_h: float = tan(deg_to_rad(cam.fov * 0.5)) * dist
	return Vector2(half_h * aspect, half_h)

# ---- the walkable spine ----------------------------------------------------
# A promenade is a PATH, not an open field. The child may touch anywhere on the
# screen, but Roshan walks the painted route: cfg "route" is an Array of
# Vector2 waypoints in stage-local space, (x, avatar y), ordered left to right.
# Travel clamps to its span and her height follows it, so she stays on the
# painted way and can walk onto what the picture actually draws - a drawbridge,
# a jetty - instead of drifting across ground the painting never offered.
func route_span(cfg: Dictionary) -> Vector2:
	var route: Array = cfg.get("route", [])
	if route.size() < 2:
		return Vector2.ZERO
	return Vector2((route[0] as Vector2).x, (route[route.size() - 1] as Vector2).x)

func route_y(cfg: Dictionary, x: float, fallback: float) -> float:
	# avatar height at x, linear between waypoints; flat outside the span
	var route: Array = cfg.get("route", [])
	if route.size() < 2:
		return fallback
	if x <= (route[0] as Vector2).x:
		return (route[0] as Vector2).y
	for i in range(1, route.size()):
		var b: Vector2 = route[i] as Vector2
		if x <= b.x:
			var a: Vector2 = route[i - 1] as Vector2
			var span: float = b.x - a.x
			if span <= 0.0001:
				return b.y
			return lerpf(a.y, b.y, (x - a.x) / span)
	return (route[route.size() - 1] as Vector2).y

func keep_on_screen(cfg: Dictionary, x: float) -> float:
	# Past the mural's pan limit the lens is PINNED, so the avatar keeps
	# walking while the frame stands still — hold the stick and she strolls off
	# the side of the screen, where a 4-year-old cannot find her again. Bound
	# her to the frame the lens is actually holding, with a margin so she never
	# even touches the edge. Opt-in per stage (cfg keep_on_screen).
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return x
	var pan: float = screen_pan_limit(cfg, cam)
	if pan < 0.0:
		return x
	var follow: float = clampf(x * float(cfg.get("cam_follow", 0.25)), -pan, pan)
	var edge: float = maxf(2.0,
		view_half_size(cfg, cam, 0.0).x - float(cfg.get("edge_margin", 5.0)))
	return clampf(x, follow - edge, follow + edge)

func screen_pan_limit(cfg: Dictionary, cam: Camera3D) -> float:
	# How far the lens may pan before the painted wall runs out. 0 = the mural
	# is narrower than the frame, so it can only ever be shown dead-centre.
	var half_w: float = float(cfg.get("screen_half_w", 0.0))
	if half_w <= 0.0 or cam == null or not cam.is_inside_tree():
		return -1.0   # no mural declared (or no lens yet): the client frames itself
	return maxf(0.0, half_w - view_half_size(cfg, cam, float(cfg.get("screen_z", -18.0))).x)

func _glide_camera(delta: float, cfg: Dictionary, r: Node3D, follow_x: float) -> void:
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return
	var lens: float = float(cfg.get("cam_fov", 0.0))
	if lens > 0.0:
		# hold the stage lens: the free-swim chase cam breathes fov with speed
		# and would otherwise leave the promenade zoomed at whatever value it
		# was carrying when the stage opened
		cam.fov = lens
	var pan_limit: float = screen_pan_limit(cfg, cam)
	if pan_limit >= 0.0:
		follow_x = clampf(follow_x, -pan_limit, pan_limit)
	var goal: Vector3 = r.position + Vector3(follow_x, float(cfg.get("cam_h", 12.0)), float(cfg.get("cam_dist", 20.5)))
	cam.position = cam.position.lerp(goal, 1.0 - pow(0.002, delta))
	cam.look_at(r.position + Vector3(follow_x, float(cfg.get("look_h", 10.5)), 0))
	# parallax: locked layers ride the (lerped) camera by their lock factor,
	# so a lock-1 sky never recedes and a lock-0 skirt stays stage-pinned;
	# under a swell the near layers also breathe with the shared wave (the
	# lock-1 sky stays fixed — the horizon doesn't ride the current)
	var sway_x := 0.0
	if swell_amp() > 0.0:
		sway_x = swell_sway(0.0).x
	for e_v in (m.g.get("ss_layers", []) as Array):
		var e: Dictionary = e_v as Dictionary
		var holder: Node3D = e.get("node") as Node3D
		if holder != null and is_instance_valid(holder):
			var lockf: float = float(e.get("lock", 0.0))
			holder.position.x = (cam.position.x - r.position.x) * lockf \
				+ sway_x * (1.0 - lockf) * 0.5

# ---- brawl mode: walk-the-plane with depth (Castle Crashers style) ---------
func set_bounds(l: float, r: float) -> void:
	# the sliding stage window: clear a wave, the game slides these forward
	m.g["ss_bl"] = l
	m.g["ss_br"] = r

func brawl_tick(delta: float) -> Dictionary:
	# P1 = Roshan: x AND z movement inside a depth band, facing her run,
	# tap = THE button. Pad reads here are DEVICE 0 ONLY (unlike main.joy_axis's
	# merge-all-pads) so a second pad can drive the companion without ghosting
	# player 1's stick.
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var r := root()
	if r == null:
		return {"mx": 0.0, "mz": 0.0, "px": 0.0, "pz": 0.0, "tap": false, "moved": false}
	var half_d: float = float(cfg.get("half_d", 7.0))
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
	var spd: float = float(cfg.get("steer_speed", 24.8))
	var half_w: float = float(cfg.get("half_w", 23.2))
	var x: float = clampf(px() + mx * spd * delta,
		float(m.g.get("ss_bl", -half_w)), float(m.g.get("ss_br", half_w)))
	var z: float = clampf((m.player.position.z - r.position.z) + mz * spd * 0.8 * delta,
		-half_d, half_d)
	m.g["ss_bob"] = float(m.g.get("ss_bob", 0.0)) + delta
	var hover: float = float(cfg.get("hover", 3.0)) + sin(float(m.g["ss_bob"]) * 2.2) * float(cfg.get("bob_amp", 0.5))
	if swell_amp() > 0.0:
		hover += sin(swell_phase(x) + 0.9) * 0.35 * swell_amp()
	m.player.position = r.position + Vector3(x, hover, z)
	m.player.vel = Vector3.ZERO
	# face the run: screen-left/right while dashing, the camera when idle
	var want_rot: float = PI
	if absf(mx) > 0.1:
		want_rot = -PI * 0.5 if mx > 0.0 else PI * 0.5
	m.player.rotation.y = lerp_angle(m.player.rotation.y, want_rot, 1.0 - pow(0.002, delta))
	m.player.rotation.z = lerpf(m.player.rotation.z, -mx * 0.16, 1.0 - pow(0.001, delta))
	# tap edge: touch tap ∥ fresh action_down ∥ Space ∥ pad-0 A
	var down: bool = Input.is_physical_key_pressed(KEY_SPACE)
	if pads.size() > 0:
		down = down or Input.is_joy_button_pressed(int(pads[0]), JOY_BUTTON_A)
	if m.touch_ui != null and m.touch_ui.action_down:
		down = true
	var tap: bool = down and not bool(m.g.get("ss_tap_prev", false))
	m.g["ss_tap_prev"] = down
	if m.touch_ui != null and m.touch_ui.consume_action_just():
		tap = true
	_glide_camera(delta, cfg, r, x * float(cfg.get("cam_follow", 0.25)))
	return {"mx": mx, "mz": mz, "px": x, "pz": z, "tap": tap, "moved": absf(mx) > 0.05 or absf(mz) > 0.05}

# ---- the companion: player 2 as a storybook cutout -------------------------
func companion_open(tex_path: String, height: float, start: Vector3) -> void:
	# an illustrated-cutout second hero per the art direction (billboard,
	# unshaded, idle bob, contact shadow) — never a re-lit 3D model
	var r := root()
	if r == null:
		return
	var spr := Sprite3D.new()
	spr.texture = load(tex_path)
	spr.pixel_size = height / maxf(1.0, float(spr.texture.get_height()))
	spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	spr.shaded = false
	r.add_child(spr)
	var shadow := Sprite3D.new()
	shadow.texture = load(CONTACT_SHADOW)
	shadow.pixel_size = (height * 0.62) / maxf(1.0, float(shadow.texture.get_width()))
	shadow.rotation_degrees.x = -90.0
	shadow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	shadow.shaded = false
	shadow.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	r.add_child(shadow)
	m.g["ss_p2"] = spr
	m.g["ss_p2_shadow"] = shadow
	m.g["ss_p2h"] = height
	m.g["ss_p2x"] = start.x
	m.g["ss_p2z"] = start.z
	m.g["ss_p2_h"] = 0.0

func companion_tick(delta: float, want_x: float, want_z: float, speed: float) -> Dictionary:
	# AI walks toward (want_x, want_z); a second gamepad (device index 1)
	# takes over the moment its stick or A button moves, and hands control
	# back to the AI after 4s of idle — "player 2 when present, helper when
	# not", with zero menus.
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var r := root()
	var spr: Sprite3D = m.g.get("ss_p2") as Sprite3D
	if r == null or spr == null or not is_instance_valid(spr):
		return {"x": 0.0, "z": 0.0, "tap": false, "human": false}
	var x: float = float(m.g.get("ss_p2x", 0.0))
	var z: float = float(m.g.get("ss_p2z", 0.0))
	var pads: Array = Input.get_connected_joypads()
	var hx := 0.0
	var hz := 0.0
	var hdown := false
	if pads.size() >= 2:
		hx = Input.get_joy_axis(int(pads[1]), JOY_AXIS_LEFT_X)
		hz = Input.get_joy_axis(int(pads[1]), JOY_AXIS_LEFT_Y)
		hdown = Input.is_joy_button_pressed(int(pads[1]), JOY_BUTTON_A)
		if absf(hx) > 0.25 or absf(hz) > 0.25 or hdown:
			m.g["ss_p2_h"] = 4.0
	m.g["ss_p2_h"] = maxf(0.0, float(m.g.get("ss_p2_h", 0.0)) - delta)
	var human: bool = float(m.g["ss_p2_h"]) > 0.0
	if human:
		if absf(hx) > 0.25:
			x += hx * speed * delta
		if absf(hz) > 0.25:
			z += hz * speed * 0.8 * delta
	else:
		x = move_toward(x, want_x, speed * 0.8 * delta)
		z = move_toward(z, want_z, speed * 0.65 * delta)
	var half_w: float = float(cfg.get("half_w", 23.2))
	x = clampf(x, float(m.g.get("ss_bl", -half_w)), float(m.g.get("ss_br", half_w)))
	z = clampf(z, -float(cfg.get("half_d", 7.0)), float(cfg.get("half_d", 7.0)))
	m.g["ss_p2x"] = x
	m.g["ss_p2z"] = z
	var half_h: float = float(m.g.get("ss_p2h", 5.5)) * 0.5
	spr.position = Vector3(x, half_h + 0.6 + sin(float(m.g.get("ss_bob", 0.0)) * 2.6 + 1.3) * 0.4, z)
	var shadow: Sprite3D = m.g.get("ss_p2_shadow") as Sprite3D
	if shadow != null and is_instance_valid(shadow):
		shadow.position = Vector3(x, 0.15, z)
	var tap: bool = hdown and not bool(m.g.get("ss_p2_tap_prev", false))
	m.g["ss_p2_tap_prev"] = hdown
	return {"x": x, "z": z, "tap": human and tap, "human": human}

# ---- standee flats: 2D designs standing IN the 3D stage --------------------
func flat(tex_path: String, size: Vector2, x: float, z: float, y: float = 0.0, shadow: bool = true) -> Node3D:
	# The layering rule (owner note 2026-07-27, charter §1): a stage set is
	# never one painting — each design is broken into depth-classed pieces.
	# Murals live in "layers"; anything Roshan can pass IN FRONT OF or BEHIND
	# is a standee — one cutout sprite standing at a real z inside/around the
	# walk band, so the depth buffer sorts her against it correctly as she
	# moves and the interaction reads true. Alpha-scissor keeps depth writes
	# on (standee-vs-standee sorting) and the outlines storybook-crisp.
	# Unshaded, never re-lit; bottom edge of the art is the ground line.
	var r := root()
	if r == null or not ResourceLoader.exists(tex_path):
		return null
	var holder := Node3D.new()
	holder.position = Vector3(x, 0.0, z)
	r.add_child(holder)
	var q := Sprite3D.new()
	var flat_texture: Texture2D = load(tex_path)
	q.texture = flat_texture
	q.pixel_size = 1.0 / maxf(1.0, float(flat_texture.get_height()))
	var flat_base_width: float = float(flat_texture.get_width()) * q.pixel_size
	q.scale = Vector3(size.x / flat_base_width, size.y, 1.0)
	q.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	q.shaded = false
	q.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	q.position = Vector3(0, size.y * 0.5 + y, 0)
	holder.add_child(q)
	if shadow:
		var sq := Sprite3D.new()
		sq.texture = load(CONTACT_SHADOW)
		sq.pixel_size = (size.x * 0.6) / maxf(1.0, float(sq.texture.get_width()))
		sq.rotation_degrees.x = -90.0
		sq.billboard = BaseMaterial3D.BILLBOARD_DISABLED
		sq.shaded = false
		sq.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
		sq.position = Vector3(0, 0.12, 0)
		holder.add_child(sq)
	return holder

# ---- physical standees: Jolt-driven sprite props (prototype 2026-07-27) ----
# prop() puts a flat()-style cutout on a real RigidBody3D so the Jolt engine
# (project.godot [physics]) is what moves it: settling, tumbling, shoves and
# bounces come from the solver instead of tween/animation code. The GPU cost
# of a prop is one alpha-scissor quad; its motion is CPU-side and ~free once
# the body sleeps. Garnish only, never objective logic — probes must stay
# deterministic, so nothing win-critical may ride a body ("logic analytic,
# garnish Jolt", JOLT_PHYSICS_AUDIT_2026-07-18.md). The flat walk band is
# what makes engine bodies affordable here at all: whole-stage collision is
# five primitives, versus the procedural free-swim floor that keeps the rest
# of the game analytic (PHYSICS_ENGINE.md).
const PROPS_MAX := 12   # sleep-enabled fleet cap per stage (audit F2 budget)

func props_arena() -> void:
	# the invisible static shell: a floor slab under the walk band plus four
	# low walls just outside the stage bounds, so bodies settle and stay on
	# the promenade with zero per-frame containment code
	var r := root()
	if r == null:
		return
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	var half_w: float = float(cfg.get("half_w", 23.2))
	var half_d: float = float(cfg.get("half_d", 7.0))
	var span_x: float = half_w * 2.0 + 12.0
	var span_z: float = half_d * 2.0 + 12.0
	var shell: Array = [
		[Vector3(0.0, -0.5, 0.0), Vector3(span_x, 1.0, span_z)],
		[Vector3(-half_w - 1.6, 5.5, 0.0), Vector3(1.0, 12.0, span_z)],
		[Vector3(half_w + 1.6, 5.5, 0.0), Vector3(1.0, 12.0, span_z)],
		[Vector3(0.0, 5.5, -half_d - 1.6), Vector3(span_x, 12.0, 1.0)],
		[Vector3(0.0, 5.5, half_d + 1.6), Vector3(span_x, 12.0, 1.0)],
	]
	for e_v in shell:
		var pos: Vector3 = e_v[0]
		var sz: Vector3 = e_v[1]
		var sb := StaticBody3D.new()
		sb.collision_layer = 1
		sb.collision_mask = 0
		var cs := CollisionShape3D.new()
		var bx := BoxShape3D.new()
		bx.size = sz
		cs.shape = bx
		sb.add_child(cs)
		sb.position = pos
		r.add_child(sb)
	m.g["ss_props"] = []

func prop(tex_path: String, size: Vector2, x: float, z: float, cfg: Dictionary = {}) -> RigidBody3D:
	# A physical standee. cfg keys, all optional: shape ("box"|"ball"),
	# depth (box thickness), mass, gravity_scale, damp, tumble (may tip in
	# the screen plane; false = locked upright), drop (spawn height above
	# the floor), floor_y, color (placeholder tint when tex_path is "" or
	# absent — the P2 placeholder-flat convention), parent + register:false
	# (dev-lab spawns outside a stage own their cleanup). Returns null past
	# the fleet cap — the cap is the perf contract, not a suggestion.
	var parent: Node3D = cfg.get("parent", root())
	if parent == null:
		return null
	var register: bool = bool(cfg.get("register", true))
	var fleet: Array = m.g.get("ss_props", [])
	if register and fleet.size() >= PROPS_MAX:
		return null
	var body := RigidBody3D.new()
	body.collision_layer = 2
	body.collision_mask = 1 | 2
	body.mass = float(cfg.get("mass", 1.0))
	body.gravity_scale = float(cfg.get("gravity_scale", 1.0))
	var damp: float = float(cfg.get("damp", 0.4))
	body.linear_damp = damp
	body.angular_damp = damp * 2.2
	body.can_sleep = true
	# toy props slide like beach toys, not bricks: the default material's
	# friction at full gravity eats the gentle push/swell forces entirely
	# (probe-caught 2026-07-27) — low friction keeps the fleet shovable
	var pm := PhysicsMaterial.new()
	pm.friction = float(cfg.get("friction", 0.35))
	pm.bounce = float(cfg.get("bounce", 0.15))
	body.physics_material_override = pm
	# cutouts rotate only in the screen plane (z) — never show their paper
	# edge (x) or spin to face away (y)
	body.axis_lock_angular_x = true
	body.axis_lock_angular_y = true
	body.axis_lock_angular_z = not bool(cfg.get("tumble", true))
	var cs := CollisionShape3D.new()
	if String(cfg.get("shape", "box")) == "ball":
		var sph := SphereShape3D.new()
		sph.radius = size.x * 0.5
		cs.shape = sph
	else:
		var bx := BoxShape3D.new()
		bx.size = Vector3(size.x * 0.9, size.y, float(cfg.get("depth", maxf(0.6, size.x * 0.45))))
		cs.shape = bx
	body.add_child(cs)
	var q := Sprite3D.new()
	var prop_texture: Texture2D
	if tex_path != "" and ResourceLoader.exists(tex_path):
		prop_texture = load(tex_path)
	else:
		prop_texture = load(FLAT_PLACEHOLDER)
		q.modulate = cfg.get("color", Color(0.98, 0.82, 0.90))
	q.texture = prop_texture
	q.pixel_size = 1.0 / maxf(1.0, float(prop_texture.get_height()))
	var prop_base_width: float = float(prop_texture.get_width()) * q.pixel_size
	q.scale = Vector3(size.x / prop_base_width, size.y, 1.0)
	q.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	q.shaded = false
	q.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	body.add_child(q)
	# the swell's two channels need handles: the quad for the cosmetic tide
	# on sleepers, the stir stamp for the fading solver tide on awake bodies
	body.set_meta("ss_quad", q)
	body.set_meta("ss_stir", float(m.g.get("ss_swell_t", 0.0)))
	body.position = Vector3(x,
		float(cfg.get("floor_y", 0.0)) + size.y * 0.5 + float(cfg.get("drop", 0.0)) + 0.05, z)
	parent.add_child(body)
	if register:
		fleet.append(body)
		m.g["ss_props"] = fleet
	return body

# ---- the swell: one wave, every channel (underwater stages) -----------------
# A single deterministic traveling wave — pure function of the stage clock
# and x, no state, no sim — that every motion channel samples so the whole
# diorama breathes to the same tide: awake props feel it as a real (fading)
# solver force, sleeping props rock their sprite cosmetically WITHOUT waking
# (the sleep/perf contract survives), Roshan's hover and the parallax layers
# add the same phase. Opt-in per stage: cfg "swell" ∈ [0,2], 0 (default) =
# off — underwater promenades turn it on, interiors stay still. PAIRING
# RULE: a swell stage should waterlog its props (gravity_scale ≲ 0.4, damp
# ~1.0) — friction scales with held-down weight, and the gentle tide only
# out-pulls friction on buoyant bodies; a full-gravity grounded box will
# not ride it (by design — deck furniture stays put, sea toys drift). Not
# a water sim; the oceanfft addon stays dead.

func swell_amp() -> float:
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	return clampf(float(cfg.get("swell", 0.0)), 0.0, 2.0)

func swell_phase(x: float) -> float:
	# time phase minus x phase: an ~11 s swell rolling visibly across the
	# frame (wavelength ~105 units, about two stage widths)
	return float(m.g.get("ss_swell_t", 0.0)) * 0.55 - x * 0.06

func swell_force(x: float) -> Vector3:
	# the shared field for awake bodies: surge along x, softer lift, zero
	# net drift (pure oscillation — damping bleeds the energy back out)
	var ph := swell_phase(x)
	return Vector3(sin(ph) * 1.8, sin(ph * 1.8 + 1.7) * 0.6, 0.0) * swell_amp()

func swell_sway(x: float) -> Vector2:
	# the cosmetic channel for sleepers, hover and layers: (x offset,
	# z rotation) — small on purpose; it reads as current, not motion
	var ph := swell_phase(x)
	return Vector2(sin(ph) * 0.22, sin(ph + 0.6) * 0.06) * swell_amp()

func props_tick(delta: float) -> Dictionary:
	# Roshan -> prop coupling, the promenade cousin of the physlab swim-wake
	# shove in main._physics_process: a firm contact push plus a softer carry
	# from her velocity, so walking through the fleet scatters it. Owns the
	# swell clock and applies the tide per body: awake bodies get the solver
	# force, fading over ~6 s since their last disturbance so they can still
	# settle and SLEEP; sleeping bodies get the cosmetic quad sway and are
	# never woken by the wave (only Roshan's push wakes a prop, which stamps
	# it back into the real tide). Prunes freed bodies and reports how much
	# of the fleet is awake — the perf signal. Returns {count, awake}.
	m.g["ss_swell_t"] = float(m.g.get("ss_swell_t", 0.0)) + delta
	var fleet: Array = m.g.get("ss_props", [])
	if fleet.is_empty():
		return {"count": 0, "awake": 0}
	var alive: Array = []
	var awake := 0
	var amp := swell_amp()
	var t: float = float(m.g.get("ss_swell_t", 0.0))
	var ppos: Vector3 = m.player.global_position
	var pvel: Vector3 = m.player.vel
	for p_v in fleet:
		var b := p_v as RigidBody3D
		if b == null or not is_instance_valid(b):
			continue
		alive.append(b)
		var d: Vector3 = b.global_position - ppos
		var dist: float = d.length()
		if dist <= 4.5 and dist >= 0.001:
			var flatv := Vector3(d.x, d.y * 0.2, d.z)
			if flatv.length() < 0.001:
				flatv = Vector3(pvel.x, 0.0, pvel.z)
			var imp: Vector3 = flatv.normalized() * (maxf(0.0, 3.2 - dist) * 16.0)
			imp += pvel * (maxf(0.0, 1.0 - dist / 4.5) * 0.6)
			if imp.length_squared() > 0.0001:
				b.apply_central_impulse(imp * delta * b.mass)   # wakes it
				b.set_meta("ss_stir", t)
		var q: Sprite3D = b.get_meta("ss_quad", null) as Sprite3D
		if b.sleeping:
			if amp > 0.0 and q != null and is_instance_valid(q):
				var sw := swell_sway(b.global_position.x)
				q.position.x = sw.x
				q.rotation.z = sw.y
		else:
			awake += 1
			if amp > 0.0:
				var fade: float = clampf(1.0 - (t - float(b.get_meta("ss_stir", 0.0))) / 6.0, 0.0, 1.0)
				if fade > 0.0:
					b.apply_central_impulse(swell_force(b.global_position.x) * fade * delta * b.mass)
			if q != null and is_instance_valid(q):
				# hand the sprite back to the solver smoothly
				q.position.x *= 0.8
				q.rotation.z *= 0.8
	m.g["ss_props"] = alive
	return {"count": alive.size(), "awake": awake}

# ---- shared bits for stage dressing ----------------------------------------
func glow(col: Color, size: float) -> Sprite3D:
	# unparented additive billboard glow — halo for pickups / fallers
	var gt := GradientTexture2D.new()
	gt.width = 512
	gt.height = 512
	gt.fill = GradientTexture2D.FILL_RADIAL
	gt.fill_from = Vector2(0.5, 0.5)
	gt.fill_to = Vector2(0.5, 0.0)
	var gr := Gradient.new()
	gr.set_color(0, Color(col.r, col.g, col.b, 0.5))
	gr.set_color(1, Color(col.r, col.g, col.b, 0.0))
	gt.gradient = gr
	var mi := Sprite3D.new()
	mi.texture = gt
	mi.pixel_size = size / 512.0
	mi.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	mi.shaded = false
	mi.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	mi.no_depth_test = true
	return mi
