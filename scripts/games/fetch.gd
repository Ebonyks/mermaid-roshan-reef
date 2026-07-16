class_name FetchGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# fetch minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["phase"] = "aim"
	m.g["round"] = 0
	m.g["miss"] = 0
	m.g["timer"] = -1.0
	m.g["ball"] = m._game_ball(Color(1.0, 0.4, 0.25), 0.8)
	# ----- a real 3D winter Lake Michigan scene -----
	# snowy play field (the LEFT side, where Roshan and Chuck are)
	var snow := MeshInstance3D.new()
	var snm := BoxMesh.new()
	snm.size = Vector3(70.0, 1.0, 170.0)
	snow.mesh = snm
	var snmat := StandardMaterial3D.new()
	snmat.albedo_color = Color(0.96, 0.98, 1.0)
	snmat.roughness = 0.85
	snow.material_override = snmat
	snow.position = origin + Vector3(-27.0, 0.0, 0.0)
	m.add_child(snow)
	m.game_nodes.append(snow)
	# the VAST icy lake — stretches the whole length on the right, out to the horizon
	var lake := MeshInstance3D.new()
	var lb := BoxMesh.new()
	lb.size = Vector3(220.0, 0.6, 320.0)
	lake.mesh = lb
	var lm := StandardMaterial3D.new()
	lm.albedo_color = Color(0.45, 0.66, 0.82)
	lm.metallic = 0.85
	lm.roughness = 0.06
	lm.emission_enabled = true
	lm.emission = Color(0.3, 0.55, 0.72)
	lm.emission_energy_multiplier = 0.2
	lake.material_override = lm
	lake.position = origin + Vector3(118.0, 0.3, 0.0)
	m.add_child(lake)
	m.game_nodes.append(lake)
	# snowdrift shoreline ridge along the waterline (the whole length)
	m._course_box(origin + Vector3(8.2, 0.7, 0.0), Vector3(2.0, 1.4, 170.0), Color(0.99, 1.0, 1.0))
	# drifting ice floes far out on the lake
	for fl in range(8):
		var floe := MeshInstance3D.new()
		var fm := CylinderMesh.new()
		fm.top_radius = 2.0 + randf() * 3.0
		fm.bottom_radius = fm.top_radius + 0.3
		fm.height = 0.5
		floe.mesh = fm
		floe.material_override = m._soft_mat(Color(0.95, 0.98, 1.0), 0.1)
		floe.position = origin + Vector3(18.0 + randf() * 90.0, 0.8, -75.0 + randf() * 150.0)
		m.add_child(floe)
		m.game_nodes.append(floe)
	# snowy pine forest + hills along the far shore and behind
	for tz in range(16):
		var tang := float(tz) / 16.0
		var tx: float = -52.0 + randf() * 14.0
		var tzz: float = -80.0 + tang * 160.0
		# snowy hill
		if tz % 3 == 0:
			var hill := MeshInstance3D.new()
			var hs := SphereMesh.new()
			hs.radius = 12.0 + randf() * 8.0
			hill.mesh = hs
			hill.material_override = snmat
			hill.position = origin + Vector3(tx - 8.0, -2.0, tzz)
			hill.scale.y = 0.45
			m.add_child(hill)
			m.game_nodes.append(hill)
		# snowy pine (green cone capped with snow)
		var pine := MeshInstance3D.new()
		var pc := CylinderMesh.new()
		pc.top_radius = 0.0
		pc.bottom_radius = 3.0 + randf() * 1.5
		pc.height = 9.0 + randf() * 4.0
		pine.mesh = pc
		var pmat := StandardMaterial3D.new()
		pmat.albedo_color = Color(0.25, 0.42, 0.32)
		pine.material_override = pmat
		pine.position = origin + Vector3(tx, pc.height * 0.5, tzz)
		m.add_child(pine)
		m.game_nodes.append(pine)
		var cap := MeshInstance3D.new()
		var cc := CylinderMesh.new()
		cc.top_radius = 0.0
		cc.bottom_radius = pc.bottom_radius * 0.7
		cc.height = pc.height * 0.45
		cap.mesh = cc
		cap.material_override = snmat
		cap.position = pine.position + Vector3(0, pc.height * 0.32, 0)
		m.add_child(cap)
		m.game_nodes.append(cap)
	# gently falling snow over the scene
	var snowfall := GPUParticles3D.new()
	snowfall.amount = 120
	snowfall.lifetime = 6.0
	snowfall.preprocess = 4.0
	var spm := ParticleProcessMaterial.new()
	spm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	spm.emission_box_extents = Vector3(60, 1, 80)
	spm.gravity = Vector3(1.0, -4.0, 0)
	spm.initial_velocity_min = 0.5
	spm.initial_velocity_max = 1.5
	spm.scale_min = 0.1
	spm.scale_max = 0.3
	snowfall.process_material = spm
	var sflake := SphereMesh.new()
	sflake.radius = 0.5
	sflake.height = 1.0
	sflake.radial_segments = 5
	sflake.rings = 3
	var sfm := StandardMaterial3D.new()
	sfm.albedo_color = Color(1, 1, 1)
	sfm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	sflake.material = sfm
	snowfall.draw_pass_1 = sflake
	snowfall.position = origin + Vector3(-10, 30, 0)
	m.add_child(snowfall)
	m.game_nodes.append(snowfall)
	# ---- explorable detail: snowy boulders, a wooden dock, a cleared shore path ----
	var rockmat := StandardMaterial3D.new()
	rockmat.albedo_texture = load("res://assets/terrain/up_cliff_col.jpg")
	rockmat.albedo_color = Color(0.78, 0.8, 0.86)
	rockmat.normal_enabled = true
	rockmat.normal_texture = load("res://assets/terrain/up_cliff_nrm.jpg")
	rockmat.uv1_triplanar = true
	rockmat.uv1_scale = Vector3(0.12, 0.12, 0.12)
	rockmat.roughness = 0.95
	var rsd := 7
	for ri in range(10):
		rsd = (rsd * 1103515245 + 12345) & 0x7fffffff
		var rx: float = -52.0 + float(rsd % 50)
		var rz: float = -75.0 + float((rsd / 50) % 150)
		var rsz: float = 1.4 + float(rsd % 3)
		var rk := MeshInstance3D.new()
		var rm := SphereMesh.new(); rm.radius = rsz; rm.height = rsz * 1.5
		rk.mesh = rm
		rk.material_override = rockmat
		rk.position = origin + Vector3(rx, rsz * 0.35, rz)
		rk.scale.y = 0.7
		m.add_child(rk); m.game_nodes.append(rk)
		var rcap := MeshInstance3D.new()
		var rcm := SphereMesh.new(); rcm.radius = rsz * 0.85; rcm.height = rsz * 0.9
		rcap.mesh = rcm; rcap.material_override = snmat
		rcap.position = rk.position + Vector3(0, rsz * 0.32, 0); rcap.scale.y = 0.4
		m.add_child(rcap); m.game_nodes.append(rcap)
	# a wooden dock reaching out over the ice (somewhere to explore)
	var dmat := StandardMaterial3D.new()
	dmat.albedo_texture = load("res://assets/terrain/up_wood_col.jpg")
	dmat.normal_enabled = true
	dmat.normal_texture = load("res://assets/terrain/up_wood_nrm.jpg")
	dmat.uv1_triplanar = true; dmat.uv1_scale = Vector3(0.08, 0.08, 0.08); dmat.roughness = 0.9
	var dock = m._course_box(origin + Vector3(17.0, 1.1, 0.0), Vector3(30.0, 0.5, 6.0), Color(0.6, 0.44, 0.28))
	dock.material_override = dmat
	for dp in range(6):
		m._course_box(origin + Vector3(4.0 + float(dp) * 6.0, 0.0, 3.2), Vector3(0.8, 2.2, 0.8), Color(0.4, 0.3, 0.2))
		m._course_box(origin + Vector3(4.0 + float(dp) * 6.0, 0.0, -3.2), Vector3(0.8, 2.2, 0.8), Color(0.4, 0.3, 0.2))
	# a cleared path along the snowy shore
	var pth = m._course_box(origin + Vector3(-27.0, 0.56, 0.0), Vector3(9.0, 0.1, 150.0), Color(0.82, 0.86, 0.92))
	pth.material_override.roughness = 1.0
	# Chuck waits on the snow — rigged 3D poodle (built in-house: see
	# reef2/tools/build_chuck_rig.py + animate_chuck.py; clips sit_idle,
	# sit_excited, run, pickup, wag; root faces glTF +Z = atan2 convention)
	var chuck_root := Node3D.new()
	chuck_root.position = origin + Vector3(-8, 0.5, -4)
	m.add_child(chuck_root)
	m.game_nodes.append(chuck_root)
	var pood: Node3D = (load("res://assets/characters/chuck_poodle_rigged.glb") as PackedScene).instantiate()
	pood.scale = Vector3.ONE * 1.5
	pood.position.y = 0.95 * 1.5
	chuck_root.add_child(pood)
	var chuck_ap: AnimationPlayer = pood.find_child("AnimationPlayer", true, false)
	for an in ["sit_idle", "sit_excited", "run", "wag"]:
		if chuck_ap != null and chuck_ap.has_animation(an):
			chuck_ap.get_animation(an).loop_mode = Animation.LOOP_LINEAR
	m.g["chuck"] = chuck_root
	m.g["chuck_ap"] = chuck_ap
	m.g["home"] = chuck_root.position
	# aim arrow Roshan points while holding the ball
	var arrow := MeshInstance3D.new()
	var ab := PrismMesh.new()
	ab.size = Vector3(1.6, 2.6, 0.5)
	arrow.mesh = ab
	arrow.material_override = m._soft_mat(Color(0.4, 1.0, 0.5), 0.9)
	m.add_child(arrow)
	m.game_nodes.append(arrow)
	m.g["arrow"] = arrow
	m.show_msg(fr["fname"], "Throw the ball for Chuck - but NOT into the lake! Press when the arrow is GREEN!")

func _chuck_play(anim: String, blend: float = 0.25) -> void:
	var ap: AnimationPlayer = m.g["chuck_ap"]
	if ap != null and ap.has_animation(anim) and ap.current_animation != anim:
		ap.play(anim, blend)

func _tick_fetch(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	var ball: MeshInstance3D = m.g["ball"]
	var chuck: Node3D = m.g["chuck"]
	if String(m.g["phase"]) == "aim" or String(m.g["phase"]) == "fly":
		# Chuck SITS on the snow, watching Roshan (the ball, once it flies)
		var watch: Vector3 = (ball.position if String(m.g["phase"]) == "fly" else ppos) - chuck.position
		if Vector2(watch.x, watch.z).length() > 0.1:
			chuck.rotation.y = atan2(watch.x, watch.z)
		_chuck_play("sit_excited" if String(m.g["phase"]) == "fly" else "sit_idle", 0.35)
	if String(m.g["phase"]) == "aim":
		m.hud_game.text = "Throw %d / 2   (oops: %d / 3)" % [int(m.g["round"]) + 1, int(m.g["miss"])]
		# Roshan HOLDS the ball
		var fdir = Vector3(sin(m.player.yaw + PI), 0, cos(m.player.yaw + PI))
		ball.position = ppos + fdir * 1.3 + Vector3(0, -0.2, 0)
		# sweeping aim — sim: the old 1.5 rad/s sweep outran a 4yo's ~1s reaction
		# (only ~1 in 4 finished). Slower sweep, and it slows FURTHER after each
		# splash so a struggling kid always gets there (skill still shows: fewer
		# splashes = faster win)
		var sw: float = sin(float(m.g["t"]) * 0.9 * pow(0.72, float(m.g["miss"]))) * 1.25
		var dirv := Vector3(sin(sw), 0, -cos(sw))
		m.g["aim_dir"] = dirv
		var arrow: MeshInstance3D = m.g["arrow"]
		arrow.position = ppos + dirv * 3.2
		arrow.look_at(ppos + dirv * 9.0, Vector3.UP)
		arrow.rotation.x = -PI * 0.5
		var landing: Vector3 = ppos + dirv * 14.0
		var wet: bool = landing.x - m.ARENA_POS.x > 8.2
		(arrow.material_override as StandardMaterial3D).albedo_color = Color(1.0, 0.3, 0.3) if wet else Color(0.4, 1.0, 0.5)
		(arrow.material_override as StandardMaterial3D).emission = (Color(1.0, 0.25, 0.25) if wet else Color(0.3, 1.0, 0.45)) * 0.9
		# non-reader timing cue: the arrow SWELLS while green and a soft tick
		# plays the moment it turns green — timing by ear, not just by color
		arrow.scale = Vector3.ONE if wet else Vector3.ONE * (1.22 + 0.10 * sin(float(m.g["t"]) * 9.0))
		if not wet and bool(m.g.get("was_wet", true)) and m.chime != null:
			m.chime.pitch_scale = 1.5
			m.chime.play()
		m.g["was_wet"] = wet
		# clicks that land on UI (pause gear, touch buttons) must not throw the ball
		var click_free: bool = Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and m.get_viewport().gui_get_hovered_control() == null
		var pressed: bool = Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B) or click_free or (m.touch_ui != null and m.touch_ui.action_down)
		if pressed and float(m.g.get("press_cool", 0.0)) <= 0.0:
			m.g["press_cool"] = 1.0
			m.g["vel"] = dirv * 11.5 + Vector3(0, 6.5, 0)
			m.g["phase"] = "fly"
			arrow.visible = false
			if m.voice != null:
				m.voice.pitch_scale = 1.1
				m.voice.play()
		m.g["press_cool"] = maxf(0.0, float(m.g.get("press_cool", 0.0)) - delta)
	elif String(m.g["phase"]) == "fly":
		m.hud_game.text = "Wheee!"
		var v: Vector3 = m.g["vel"]
		v.y -= 9.5 * delta
		m.g["vel"] = v
		ball.position += v * delta
		if ball.position.y <= m.ARENA_POS.y + 0.9:
			ball.position.y = m.ARENA_POS.y + 0.9
			if ball.position.x - m.ARENA_POS.x > 8.2:
				# SPLASH - into the lake! No mean buzzer: a cartoon puppy
				# whimper + Wacky hamming it up ("OH NO! Chuck is all WET!")
				m.g["miss"] = int(m.g["miss"]) + 1
				m._sparkle_burst(ball.position, Color(0.4, 0.7, 1.0))
				var bz := AudioStreamPlayer.new()
				bz.stream = load("res://assets/audio/voices/chuck_whimper.ogg")
				bz.bus = "Voice"
				m.add_child(bz)
				bz.play()
				bz.finished.connect(bz.queue_free)
				if int(m.g["miss"]) >= 3:
					m._end_game(false, fr, "Aww... now Chuck is all wet!", "fail")
					return
				m.show_msg(fr["fname"], "SPLASH! Chuck can't swim out there! Try again — green arrow means SNOW!", "splash")
				m.g["phase"] = "aim"
				(m.g["arrow"] as MeshInstance3D).visible = true
			else:
				m.g["phase"] = "fetch"
	elif String(m.g["phase"]) == "pickup":
		# nose down to grab the ball, then turn for home
		m.hud_game.text = "Chuck is on it!"
		m.g["pickup_t"] = float(m.g.get("pickup_t", 0.8)) - delta
		if float(m.g["pickup_t"]) <= 0.35:
			var mouth := Vector3(sin(chuck.rotation.y), 0, cos(chuck.rotation.y))
			ball.position = chuck.position + mouth * 1.4 + Vector3(0, 1.0, 0)
		if float(m.g["pickup_t"]) <= 0.0:
			m.g["phase"] = "return"
			_chuck_play("run")
	else:
		var target: Vector3 = ball.position
		if String(m.g["phase"]) == "return":
			target = ppos
		var d: Vector3 = target - chuck.position
		d.y = 0.0
		m.hud_game.text = "Chuck is on it!"
		if d.length() > 2.0:
			chuck.position += d.normalized() * minf(40.0 * delta, d.length())
			chuck.rotation.y = atan2(d.x, d.z)
			_chuck_play("run")
			if String(m.g["phase"]) == "return":
				var mouth := Vector3(sin(chuck.rotation.y), 0, cos(chuck.rotation.y))
				ball.position = chuck.position + mouth * 1.4 + Vector3(0, 1.0, 0)
		elif String(m.g["phase"]) == "fetch":
			m.g["phase"] = "pickup"
			m.g["pickup_t"] = 0.8
			_chuck_play("pickup", 0.15)
		else:
			m.g["round"] = int(m.g["round"]) + 1
			_chuck_play("wag", 0.2)
			if int(m.g["round"]) >= 2:
				m._say("chuck", "bark")
				m._end_game(true, fr, "Chuck loves to fetch! What a good boy!")
			else:
				m.g["phase"] = "aim"
				(m.g["arrow"] as MeshInstance3D).visible = true
