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
	m.show_msg(fr["fname"], "Fly up the fairy pond! Slide to dodge the shadow sparks — your wand zaps ahead all by itself! SPACE / TAP makes a sparkle shield!")

func _tick_fairyshoot(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var origin: Vector3 = m.ARENA_POS
	var phase: String = String(m.g.get("phase", "fly"))
	var tt: float = float(m.g["t"])
	# ---- the track scrolls on its own; the stick only slides Roshan around ----
	if phase == "fly":
		m.g["fz"] = float(m.g["fz"]) + m.FS_FWD * delta
	var fz: float = m.g["fz"]
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
	# x negated so 'right' reads screen-right under the overhead camera
	var ox: float = clampf(float(m.g["ox"]) - clampf(inx, -1.0, 1.0) * m.FS_MOVE * delta, -m.FS_BX, m.FS_BX)
	var oz: float = clampf(float(m.g["oz"]) + clampf(iny, -1.0, 1.0) * m.FS_MOVE * delta, -m.FS_BZB, m.FS_BZF)
	m.g["ox"] = ox; m.g["oz"] = oz
	var pos: Vector3 = origin + Vector3(ox, m.FS_PLANE, fz + oz)
	m.player.position = pos
	m.player.vel = Vector3.ZERO
	# ---- fixed overhead camera glides up the track: reads like a scrolling 2D map ----
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var focus: Vector3 = origin + Vector3(ox * 0.15, 0, fz + m.FS_LOOK)
		m.player.cam.position = m.player.cam.position.lerp(focus + Vector3(0, m.FS_CAM_H, 0), 1.0 - pow(0.002, delta))
		m.player.cam.look_at(focus, Vector3(0, 0, 1))
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
	# ---- fairy rings sparkle as Roshan flies over them ----
	for rd in m.g["rings"]:
		if not rd["done"] and is_instance_valid(rd["node"]):
			if absf(pos.x - (origin.x + float(rd["x"]))) < 4.5 and absf(pos.z - (origin.z + float(rd["z"]))) < 3.0:
				rd["done"] = true
				m._sparkle_burst(pos, Color(1.0, 0.95, 0.6))
				if m.chime != null:
					m.chime.pitch_scale = 1.5; m.chime.play()
	# ---- shadow bugs bob in place; the ones on screen lob slow sparks ----
	for td in m.g["targets"]:
		if not td["alive"] or not is_instance_valid(td["node"]):
			continue
		var b0: Vector3 = td["base"]
		var bp: Vector3 = b0 + Vector3(sin(tt * 0.8 + float(td["ph"])) * 3.0, sin(tt * 2.0 + float(td["ph"])) * 0.5, 0)
		(td["node"] as Node3D).position = bp
		var ahead: float = bp.z - pos.z
		if ahead > -4.0 and ahead < m.FS_BUG_WAKE:
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
		if on.position.z < pos.z - 14.0 or on.position.z > pos.z + 52.0 or absf(on.position.x - origin.x) > 46.0:
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
	# ---- wand aim guide floats up-screen of Roshan ----
	if m.g.has("reticle") and is_instance_valid(m.g["reticle"]):
		var ret := m.g["reticle"] as Node3D
		ret.visible = phase != "boss_bloom"
		ret.position = pos + Vector3(0, 1.5, 12.0)
	# ---- firing (auto-shooter: bolts zap straight up the screen; you just line up) ----
	m.g["fire_cd"] = maxf(0.0, float(m.g["fire_cd"]) - delta)
	if phase != "boss_bloom" and float(m.g["fire_cd"]) <= 0.0:
		m.g["fire_cd"] = m.FS_FIRE_CD
		var bolt := MeshInstance3D.new()
		var bsm := SphereMesh.new(); bsm.radius = 0.6; bsm.height = 1.2
		bolt.mesh = bsm
		bolt.material_override = m._soft_mat(Color(0.6, 1.0, 0.9), 3.0)
		bolt.position = pos + Vector3(0, 0, 2.0)
		m.add_child(bolt); m.game_nodes.append(bolt)
		(m.g["bolts"] as Array).append({"node": bolt, "fly": 0.0})
		if m.chime != null:
			m.chime.pitch_scale = 1.8; m.chime.play()
	# ---- advance bolts, check hits ----
	var bolts: Array = m.g["bolts"]
	for bi in range(bolts.size() - 1, -1, -1):
		var bd: Dictionary = bolts[bi]
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			bolts.remove_at(bi); continue
		bn.position.z += m.FS_BOLT * delta
		bd["fly"] = float(bd["fly"]) + m.FS_BOLT * delta
		var dead: bool = float(bd["fly"]) > m.FS_BOLT_FLY
		for td in m.g["targets"]:
			if not td["alive"] or not is_instance_valid(td["node"]):
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
		m.hud_game.text = "Fairy Pond!  Shadow bugs zapped: %d / %d   %s" % [int(m.g["hits"]), m.FS_NBUGS, hearts_str]
		if fz >= m.FS_LEN:
			m._fairy_start_boss(origin)
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
