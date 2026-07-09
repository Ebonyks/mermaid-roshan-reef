class_name FairyGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# fairyshoot minigame. All state stays on main (m.*); received by reference.

var m

func _init(main) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m._build_fairyshoot(origin)
	m._play_music("melody")   # dreamy track
	m.show_msg(fr["fname"], "Fly the fairy! Move to dodge, hold SPACE / TAP to zap the shadow bugs!")

func _tick_fairyshoot(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var origin: Vector3 = m.ARENA_POS
	var phase: String = String(m.g.get("phase", "fly"))
	if phase == "fly":
		m.g["fz"] = float(m.g["fz"]) + m.FS_FWD * delta
	var fz: float = m.g["fz"]
	# ---- steering input (free 2D), x negated so 'right' reads screen-right ----
	var inx := 0.0
	var iny := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		inx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		inx += 1.0
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W):
		iny += 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		iny -= 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = m.joy_axis(JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.2: inx += jx
	if absf(jy) > 0.2: iny -= jy
	if m.touch_ui != null:
		if absf(m.touch_ui.stick_vec.x) > 0.15: inx += m.touch_ui.stick_vec.x
		if absf(m.touch_ui.stick_vec.y) > 0.15: iny -= m.touch_ui.stick_vec.y
	var ox: float = clampf(float(m.g["ox"]) - inx * m.FS_MOVE * delta, -m.FS_BX, m.FS_BX)
	var oy: float = clampf(float(m.g["oy"]) + iny * m.FS_MOVE * delta, -m.FS_BY, m.FS_BY)
	m.g["ox"] = ox; m.g["oy"] = oy
	var pos: Vector3 = origin + Vector3(ox, m.FS_BASE_Y + oy, fz)
	m.player.position = pos
	# ---- chase camera, locked behind ----
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var campos := Vector3(origin.x + ox * 0.4, origin.y + m.FS_BASE_Y + 5.0 + oy * 0.3, pos.z - 16.0)
		m.player.cam.position = m.player.cam.position.lerp(campos, 1.0 - pow(0.0006, delta))
		m.player.cam.look_at(pos + Vector3(0, 0.5, 26.0))
	# ---- reticle ahead of the player ----
	if m.g.has("reticle") and is_instance_valid(m.g["reticle"]):
		(m.g["reticle"] as Node3D).position = pos + Vector3(0, 0, 34.0)
	# ---- firing (auto-shooter: bolts fire on their own; you just aim by moving) ----
	m.g["fire_cd"] = maxf(0.0, float(m.g["fire_cd"]) - delta)
	if float(m.g["fire_cd"]) <= 0.0:
		m.g["fire_cd"] = m.FS_FIRE_CD
		var bolt := MeshInstance3D.new()
		var bsm := SphereMesh.new(); bsm.radius = 0.6; bsm.height = 1.2
		bolt.mesh = bsm
		bolt.material_override = m._soft_mat(Color(0.6, 1.0, 0.9), 3.0)
		bolt.position = pos + Vector3(0, 0, 3.0)
		m.add_child(bolt); m.game_nodes.append(bolt)
		(m.g["bolts"] as Array).append({"node": bolt})
		if m.chime != null:
			m.chime.pitch_scale = 0.95; m.chime.play()
	# ---- advance bolts, check hits ----
	var bolts: Array = m.g["bolts"]
	for bi in range(bolts.size() - 1, -1, -1):
		var bd: Dictionary = bolts[bi]
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			bolts.remove_at(bi); continue
		bn.position.z += m.FS_BOLT * delta
		var dead := bn.position.z > pos.z + 280.0
		for td in m.g["targets"]:
			if not td["alive"]:
				continue
			if bn.position.distance_to(td["node"].position) < m.FS_HIT_R:
				td["alive"] = false
				m.g["hits"] = int(m.g["hits"]) + 1
				var tn: Node = td["node"]
				m._sparkle_burst((tn as Node3D).position, Color(1.0, 0.5, 0.7))
				if is_instance_valid(tn): tn.queue_free()
				if m.chime != null:
					m.chime.pitch_scale = 0.85; m.chime.play()
				dead = true
				break
		# boss: leaf shield
		if not dead and phase == "boss_leaves":
			for lf in m.g["leaves"]:
				if int(lf["hp"]) <= 0 or not is_instance_valid(lf["node"]):
					continue
				if bn.position.distance_to((lf["node"] as Node3D).position) < m.FS_BOSS_HIT_R:
					lf["hp"] = int(lf["hp"]) - 1
					m._sparkle_burst((lf["node"] as Node3D).position, Color(0.5, 1.0, 0.5))
					if int(lf["hp"]) <= 0:
						(lf["node"] as Node3D).queue_free()
						if m.chime != null: m.chime.pitch_scale = 0.9; m.chime.play()
					dead = true
					break
		# boss: flower bud
		if not dead and phase == "boss_bud" and m.g.get("bud") != null and is_instance_valid(m.g["bud"]):
			if bn.position.distance_to((m.g["bud"] as Node3D).position) < m.FS_BOSS_HIT_R + 1.0:
				m.g["bud_hp"] = int(m.g["bud_hp"]) - 1
				m._sparkle_burst((m.g["bud"] as Node3D).position + Vector3(randf() * 4 - 2, randf() * 4 - 2, 0), Color(1.0, 0.7, 0.85))
				if m.chime != null: m.chime.pitch_scale = 0.8 + 0.015 * float(m.FS_BUD_HP - int(m.g["bud_hp"])); m.chime.play()
				dead = true
		if dead:
			bn.queue_free(); bolts.remove_at(bi)
	# ---- bug + firefly idle motion ----
	var tt: float = float(m.g["t"])
	for td in m.g["targets"]:
		if td["alive"] and is_instance_valid(td["node"]):
			(td["node"] as Node3D).position.y = (td["pos"] as Vector3).y + sin(tt * 2.0 + float(td["ph"])) * 0.8
	for ff in m.g["fireflies"]:
		if is_instance_valid(ff["node"]):
			var b: Vector3 = ff["base"]
			(ff["node"] as Node3D).position = b + Vector3(sin(tt * 1.3 + float(ff["ph"])) * 2.0, cos(tt * 1.1 + float(ff["ph"])) * 1.5, 0)
	# ---- phase logic ----
	if phase == "fly":
		m.hud_game.text = "Fairy Pond!  Shadow bugs zapped: %d / %d" % [int(m.g["hits"]), m.FS_NBUGS]
		if fz >= m.FS_LEN:
			m._fairy_start_boss(origin)
		return
	m.g["phase_t"] = float(m.g.get("phase_t", 0.0)) - delta
	var pt: float = maxf(0.0, float(m.g["phase_t"]))
	if phase == "boss_leaves":
		var left := 0
		for lf in m.g["leaves"]:
			if int(lf["hp"]) > 0:
				left += 1
			elif is_instance_valid(lf.get("node")):
				pass
		# rustle surviving leaves (gentle scale pulse — keeps the GLB bushes upright)
		for lf in m.g["leaves"]:
			if int(lf["hp"]) > 0 and is_instance_valid(lf["node"]):
				(lf["node"] as Node3D).scale = Vector3.ONE * (m.FS_LEAF_SCALE * (1.0 + sin(tt * 4.0 + float(lf["ang"])) * 0.06))
		m.hud_game.text = "Blast the leaves away!   leaves left: %d   ⏱ %d" % [left, int(ceil(pt))]
		if left <= 0:
			m.g["phase"] = "boss_bud"
			m.g["phase_t"] = m.FS_BUD_T + 6.0 * float(mini(m.fs_fails, 2))
			if m.g.get("bud") != null and is_instance_valid(m.g["bud"]):
				(m.g["bud"] as Node3D).scale = Vector3.ONE * (m.FS_BUD_SCALE * 0.5)
			m.show_msg(m.fr_name_safe(), "The flower! Keep blasting to make it grow and bloom!")
		elif pt <= 0.0:
			m.fs_fails += 1
			m._end_game(false, fr, "Oh no — the flower stayed shut! Fly back and try again!", "fail")
		return
	if phase == "boss_bud":
		var hp: int = int(m.g["bud_hp"])
		var bud: Node3D = m.g.get("bud")
		if bud != null and is_instance_valid(bud):
			# the flower GROWS bigger with every hit (0.5x -> 1.4x), plus a gentle pulse
			var grown: float = lerpf(0.5, 1.4, clampf(1.0 - float(hp) / float(m.FS_BUD_HP), 0.0, 1.0))
			var pulse: float = 1.0 + sin(tt * 8.0) * 0.05
			bud.scale = Vector3.ONE * (m.FS_BUD_SCALE * grown * pulse)
		m.hud_game.text = "Open the flower!   %d hits left   ⏱ %d" % [maxi(0, hp), int(ceil(pt))]
		if hp <= 0:
			m.fs_fails = 0
			m._fairy_bloom_start()
			m.show_msg(m.fr_name_safe(), "It's blooming! 🌸")
		elif pt <= 0.0:
			m.fs_fails += 1
			m._end_game(false, fr, "Oh no — the flower stayed shut! Fly back and try again!", "fail")
		return
	if phase == "boss_bloom":
		m.g["bloom_t"] = float(m.g.get("bloom_t", 0.0)) - delta
		var f: float = clampf(1.0 - float(m.g["bloom_t"]) / m.FS_BLOOM_T, 0.0, 1.0)
		var center: Vector3 = m.g["boss_center"]
		if m.g.get("bud") != null and is_instance_valid(m.g["bud"]):
			(m.g["bud"] as Node3D).scale = Vector3.ONE * (m.FS_BUD_SCALE * (1.0 - f * 0.55))
		for pd in m.g.get("petals", []):
			if is_instance_valid(pd["node"]):
				var a: float = pd["ang"]
				var r: float = 14.0 + f * 55.0
				(pd["node"] as Node3D).position = center + Vector3(cos(a) * r, sin(a) * r, 0)
				(pd["node"] as Node3D).scale = Vector3.ONE * (3.0 + f * 24.0)
		m.hud_game.text = "IT'S BLOOMING!!"
		if fmod(tt, 0.12) < delta:
			m._sparkle_burst(center + Vector3(randf() * 70 - 35, randf() * 60 - 30, randf() * 8 - 4), Color.from_hsv(randf(), 0.4, 1.0))
			if m.chime != null:
				m.chime.pitch_scale = 1.0 + f * 0.5
				m.chime.play()
		if float(m.g["bloom_t"]) <= 0.0:
			m._end_game(true, fr, "The GIANT Fairy Flower blossomed across the whole sky! You did it!")
		return
