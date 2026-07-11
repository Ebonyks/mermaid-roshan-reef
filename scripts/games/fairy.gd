class_name FairyGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# fairyshoot minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m._build_fairyshoot(origin)
	m._play_music("melody")   # dreamy track
	m.show_msg(fr["fname"], "Fly over the fairy pond! Dodge the shadow sparks — your wand zaps bugs all by itself! SPACE / TAP makes a sparkle shield!")

func _tick_fairyshoot(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var origin: Vector3 = m.ARENA_POS
	var phase: String = String(m.g.get("phase", "fly"))
	var tt: float = float(m.g["t"])
	# ---- restricted movement: flat screen-relative slide — no momentum, no jump ----
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
	var pos: Vector3 = m.player.position
	pos.x += clampf(inx, -1.0, 1.0) * m.FS_MOVE * delta
	pos.z -= clampf(iny, -1.0, 1.0) * m.FS_MOVE * delta   # stick up = up the screen
	pos.y = origin.y + m.FS_PLANE
	# keep Roshan inside the glowing rim (and out of the flower's heart)
	var off := Vector2(pos.x - origin.x, pos.z - origin.z)
	if off.length() > m.FS_R - 2.0:
		off = off.normalized() * (m.FS_R - 2.0)
		pos.x = origin.x + off.x; pos.z = origin.z + off.y
	if phase != "fly":
		var dcen: float = off.length()
		if dcen < m.FS_BOSS_KEEP:
			off = (off / dcen if dcen > 0.001 else Vector2.RIGHT) * m.FS_BOSS_KEEP
			pos.x = origin.x + off.x; pos.z = origin.z + off.y
	m.player.position = pos
	m.player.vel = Vector3.ZERO
	# ---- fixed overhead camera: the pond reads like a flat 2D map ----
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var focus := Vector3(origin.x + off.x * 0.12, origin.y, origin.z + off.y * 0.12)
		m.player.cam.position = m.player.cam.position.lerp(focus + Vector3(0, m.FS_CAM_H, 0), 1.0 - pow(0.002, delta))
		m.player.cam.look_at(focus, Vector3(0, 0, -1))
	# ---- sparkle-blink safety time after a bump ----
	m.g["hurt_t"] = maxf(0.0, float(m.g["hurt_t"]) - delta)
	m.player.visible = float(m.g["hurt_t"]) <= 0.0 or fmod(tt, 0.24) > 0.09
	# ---- sparkle shield: one big friendly button clears nearby sparks ----
	m.g["nova_cd"] = maxf(0.0, float(m.g["nova_cd"]) - delta)
	var nova_pressed: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_joy_button_pressed(0, JOY_BUTTON_A)
	if m.touch_ui != null and m.touch_ui.action_down:
		nova_pressed = true
	if nova_pressed and float(m.g["nova_cd"]) <= 0.0:
		m.g["nova_cd"] = m.FS_NOVA_CD
		for k in range(6):
			var na: float = float(k) / 6.0 * TAU
			m._sparkle_burst(pos + Vector3(cos(na) * 4.0, 0.5, sin(na) * 4.0), Color(0.7, 0.95, 1.0))
		var orbs0: Array = m.g["orbs"]
		for oi0 in range(orbs0.size() - 1, -1, -1):
			var od0: Dictionary = orbs0[oi0]
			var on0: Node3D = od0["node"]
			if not is_instance_valid(on0):
				orbs0.remove_at(oi0); continue
			if on0.position.distance_to(pos) < m.FS_NOVA_R:
				m._sparkle_burst(on0.position, Color(0.85, 0.7, 1.0))
				on0.queue_free(); orbs0.remove_at(oi0)
		if m.chime != null:
			m.chime.pitch_scale = 1.6; m.chime.play()
	# ---- shadow bugs circle the pond and lob slow sparks ----
	for td in m.g["targets"]:
		if not td["alive"] or not is_instance_valid(td["node"]):
			continue
		td["ang"] = float(td["ang"]) + float(td["spin"]) * delta
		var bp: Vector3 = origin + Vector3(cos(float(td["ang"])) * float(td["rad"]),
				m.FS_PLANE + sin(tt * 2.0 + float(td["ph"])) * 0.5, sin(float(td["ang"])) * float(td["rad"]))
		(td["node"] as Node3D).position = bp
		td["orb_cd"] = float(td["orb_cd"]) - delta
		if float(td["orb_cd"]) <= 0.0 and (m.g["orbs"] as Array).size() < m.FS_ORB_MAX:
			td["orb_cd"] = m.FS_ORB_CD_MIN + randf() * (m.FS_ORB_CD_MAX - m.FS_ORB_CD_MIN)
			var dirv := Vector3(pos.x - bp.x, 0, pos.z - bp.z)
			if dirv.length() > 0.5:
				m._fairy_spawn_orb(Vector3(bp.x, origin.y + m.FS_PLANE, bp.z), dirv.normalized())
	# ---- sparks drift; touching one costs a heart (then a safe sparkle-blink) ----
	var orbs: Array = m.g["orbs"]
	for oi in range(orbs.size() - 1, -1, -1):
		var od: Dictionary = orbs[oi]
		var on: Node3D = od["node"]
		if not is_instance_valid(on):
			orbs.remove_at(oi); continue
		on.position += (od["dir"] as Vector3) * m.FS_ORB_SPD * delta
		on.scale = Vector3.ONE * (1.0 + sin(tt * 6.0) * 0.12)
		if Vector2(on.position.x - origin.x, on.position.z - origin.z).length() > m.FS_R + 4.0:
			on.queue_free(); orbs.remove_at(oi); continue
		if float(m.g["hurt_t"]) <= 0.0 and on.position.distance_to(pos) < m.FS_ORB_R:
			on.queue_free(); orbs.remove_at(oi)
			m.g["hearts"] = int(m.g["hearts"]) - 1
			m.g["hurt_t"] = m.FS_HURT_T
			m._sparkle_burst(pos, Color(0.7, 0.4, 1.0))
			if m.chime != null:
				m.chime.pitch_scale = 0.7; m.chime.play()
			if int(m.g["hearts"]) <= 0:
				m.player.visible = true
				m.fs_fails += 1
				m._end_game(false, fr, "The shadow sparks tired Roshan out! Splash back in and try again!", "fail")
				return
	# ---- the wand aims itself: nearest zappable thing within reach ----
	var aim_pos := Vector3.ZERO
	var aim_found := false
	var best: float = m.FS_RANGE
	if phase == "fly":
		for td in m.g["targets"]:
			if td["alive"] and is_instance_valid(td["node"]):
				var d: float = (td["node"] as Node3D).position.distance_to(pos)
				if d < best:
					best = d; aim_pos = (td["node"] as Node3D).position; aim_found = true
	elif phase == "boss_leaves":
		for lf in m.g["leaves"]:
			if int(lf["hp"]) > 0 and is_instance_valid(lf["node"]):
				var d2: float = (lf["node"] as Node3D).position.distance_to(pos)
				if d2 < best:
					best = d2; aim_pos = (lf["node"] as Node3D).position; aim_found = true
	elif phase == "boss_bud":
		var center0: Vector3 = m.g["boss_center"]
		if center0.distance_to(pos) < m.FS_RANGE + 4.0:
			aim_pos = center0; aim_found = true
	if m.g.has("reticle") and is_instance_valid(m.g["reticle"]):
		var ret := m.g["reticle"] as Node3D
		ret.visible = aim_found
		if aim_found:
			ret.position = Vector3(aim_pos.x, origin.y + m.FS_PLANE + 1.5, aim_pos.z)
	# ---- firing (auto-shooter: the wand zaps by itself; you just fly close) ----
	m.g["fire_cd"] = maxf(0.0, float(m.g["fire_cd"]) - delta)
	if aim_found and float(m.g["fire_cd"]) <= 0.0:
		m.g["fire_cd"] = m.FS_FIRE_CD
		var bolt := MeshInstance3D.new()
		var bsm := SphereMesh.new(); bsm.radius = 0.6; bsm.height = 1.2
		bolt.mesh = bsm
		bolt.material_override = m._soft_mat(Color(0.6, 1.0, 0.9), 3.0)
		bolt.position = pos
		m.add_child(bolt); m.game_nodes.append(bolt)
		var bdir := Vector3(aim_pos.x - pos.x, 0, aim_pos.z - pos.z)
		(m.g["bolts"] as Array).append({"node": bolt,
				"dir": (bdir.normalized() if bdir.length() > 0.001 else Vector3.FORWARD), "fly": 0.0})
		if m.chime != null:
			m.chime.pitch_scale = 1.8; m.chime.play()
	# ---- advance bolts, check hits ----
	var bolts: Array = m.g["bolts"]
	for bi in range(bolts.size() - 1, -1, -1):
		var bd: Dictionary = bolts[bi]
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			bolts.remove_at(bi); continue
		bn.position += (bd["dir"] as Vector3) * m.FS_BOLT * delta
		bd["fly"] = float(bd["fly"]) + m.FS_BOLT * delta
		var dead: bool = float(bd["fly"]) > m.FS_RANGE + 8.0
		for td in m.g["targets"]:
			if not td["alive"]:
				continue
			if bn.position.distance_to((td["node"] as Node3D).position) < m.FS_HIT_R:
				td["alive"] = false
				m.g["hits"] = int(m.g["hits"]) + 1
				var tn: Node = td["node"]
				m._sparkle_burst((tn as Node3D).position, Color(1.0, 0.5, 0.7))
				if is_instance_valid(tn): tn.queue_free()
				if m.chime != null:
					m.chime.pitch_scale = 1.2; m.chime.play()
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
						if m.chime != null: m.chime.pitch_scale = 1.4; m.chime.play()
					dead = true
					break
		# boss: flower bud
		if not dead and phase == "boss_bud" and m.g.get("bud") != null and is_instance_valid(m.g["bud"]):
			var center1: Vector3 = m.g["boss_center"]
			if bn.position.distance_to(center1) < m.FS_BOSS_HIT_R + 1.0:
				m.g["bud_hp"] = int(m.g["bud_hp"]) - 1
				m._sparkle_burst(center1 + Vector3(randf() * 4 - 2, 0.5, randf() * 4 - 2), Color(1.0, 0.7, 0.85))
				if m.chime != null: m.chime.pitch_scale = 1.1 + 0.02 * float(m.FS_BUD_HP - int(m.g["bud_hp"])); m.chime.play()
				dead = true
		if dead:
			bn.queue_free(); bolts.remove_at(bi)
	# ---- firefly idle drift ----
	for ffd in m.g["fireflies"]:
		if is_instance_valid(ffd["node"]):
			var b: Vector3 = ffd["base"]
			(ffd["node"] as Node3D).position = b + Vector3(sin(tt * 1.3 + float(ffd["ph"])) * 2.0, 0, cos(tt * 1.1 + float(ffd["ph"])) * 1.5)
	# ---- phase logic ----
	var hearts_str: String = "💗".repeat(maxi(0, int(m.g["hearts"])))
	if phase == "fly":
		m.hud_game.text = "Fairy Pond!  Shadow bugs zapped: %d / %d   %s" % [int(m.g["hits"]), m.FS_WAVE * m.FS_WAVES, hearts_str]
		var alive_n := 0
		for td in m.g["targets"]:
			if td["alive"]:
				alive_n += 1
		if alive_n == 0:
			if int(m.g["wave"]) >= m.FS_WAVES:
				m._fairy_start_boss(origin)
			else:
				m._fairy_spawn_wave(origin)
				m.show_msg(m.fr_name_safe(), "More shadow bugs! Fly close and zap them!")
		return
	# ---- the flower puffs slow rings of sparks to weave through ----
	if phase != "boss_bloom":
		m.g["ring_cd"] = float(m.g.get("ring_cd", m.FS_RING_CD)) - delta
		if float(m.g["ring_cd"]) <= 0.0:
			m.g["ring_cd"] = m.FS_RING_CD
			var center2: Vector3 = m.g["boss_center"]
			for k in range(m.FS_RING_N):
				var ra: float = float(k) / float(m.FS_RING_N) * TAU + tt * 0.3
				m._fairy_spawn_orb(center2 + Vector3(cos(ra) * (m.FS_LEAF_RING + 2.0), 0, sin(ra) * (m.FS_LEAF_RING + 2.0)), Vector3(cos(ra), 0, sin(ra)))
	m.g["phase_t"] = float(m.g.get("phase_t", 0.0)) - delta
	var pt: float = maxf(0.0, float(m.g["phase_t"]))
	if phase == "boss_leaves":
		var left := 0
		# spin the leaf wreath slowly + rustle survivors (gentle scale pulse
		# keeps the GLB bushes upright)
		var center3: Vector3 = m.g["boss_center"]
		for lf in m.g["leaves"]:
			if int(lf["hp"]) > 0:
				left += 1
				if is_instance_valid(lf["node"]):
					lf["ang"] = float(lf["ang"]) + delta * 0.3
					(lf["node"] as Node3D).position = center3 + Vector3(cos(float(lf["ang"])) * m.FS_LEAF_RING, -1.0, sin(float(lf["ang"])) * m.FS_LEAF_RING)
					(lf["node"] as Node3D).scale = Vector3.ONE * (m.FS_LEAF_SCALE * (1.0 + sin(tt * 4.0 + float(lf["ang"])) * 0.06))
		m.hud_game.text = "Blast the leaves away!   leaves left: %d   %s   ⏱ %d" % [left, hearts_str, int(ceil(pt))]
		if left <= 0:
			m.g["phase"] = "boss_bud"
			m.g["phase_t"] = m.FS_BUD_T + 6.0 * float(mini(m.fs_fails, 2))
			if m.g.get("bud") != null and is_instance_valid(m.g["bud"]):
				(m.g["bud"] as Node3D).scale = Vector3.ONE * (m.FS_BUD_SCALE * 0.5)
			m.show_msg(m.fr_name_safe(), "The flower! Keep blasting to make it grow and bloom!")
		elif pt <= 0.0:
			m.player.visible = true
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
		m.hud_game.text = "Open the flower!   %d hits left   %s   ⏱ %d" % [maxi(0, hp), hearts_str, int(ceil(pt))]
		if hp <= 0:
			m._fairy_bloom_start()
			m.show_msg(m.fr_name_safe(), "It's blooming! 🌸")
		elif pt <= 0.0:
			m.player.visible = true
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
				var r: float = 3.0 + f * 9.0
				# petals open flat across the pond, like a blossom seen from above
				(pd["node"] as Node3D).position = center + Vector3(cos(a) * r, 0.5, sin(a) * r)
				(pd["node"] as Node3D).scale = Vector3.ONE * (1.0 + f * 6.0)
		if fmod(tt, 0.18) < delta:
			m._sparkle_burst(center + Vector3(randf() * 16 - 8, 1.0, randf() * 16 - 8), Color.from_hsv(randf(), 0.4, 1.0))
		if float(m.g["bloom_t"]) <= 0.0:
			m.player.visible = true
			m.fs_fails = 0
			m._end_game(true, fr, "The Fairy Flower blossomed! You did it!")
		return

