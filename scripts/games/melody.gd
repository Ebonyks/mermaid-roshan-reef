class_name MelodyGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# melody minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["caught"] = 0
	m.g["orbs"] = []
	# the whole Gabby concert page is the stage backdrop
	var bd := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(46.0, 41.8)
	bd.mesh = qm
	var bdm := StandardMaterial3D.new()
	bdm.albedo_texture = load("res://assets/book/gabby_stage.jpg")
	bdm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	bd.material_override = bdm
	bd.position = origin + Vector3(0, 19.0, -15.0)
	m.add_child(bd)
	m.game_nodes.append(bd)
	# ---- 3D concert stage set dressing (rich, themed — like the fetch/seek worlds) ----
	var stage_f: float = m.ARENA_POS.y + 0.6
	var rcols := [Color(1.0, 0.2, 0.2), Color(1.0, 0.55, 0.15), Color(1.0, 0.9, 0.2), Color(0.25, 0.9, 0.3), Color(0.2, 0.55, 1.0), Color(0.35, 0.25, 0.9), Color(0.7, 0.3, 0.9)]
	# raised stage platform with a glowing edge
	var plat = m._course_box(origin + Vector3(0, stage_f + 0.8, -8.0), Vector3(40, 1.6, 26), Color(0.18, 0.12, 0.28))
	plat.material_override.metallic = 0.4; plat.material_override.roughness = 0.3
	var edge = m._course_box(origin + Vector3(0, stage_f + 1.7, -8.0), Vector3(41, 0.4, 27), Color(1.0, 0.3, 0.7))
	edge.material_override = m._soft_mat(Color(1.0, 0.3, 0.7), 1.6)
	# big speaker stacks flanking the stage
	for sx in [-17.0, 17.0]:
		for sy in range(3):
			var spk = m._course_box(origin + Vector3(sx, stage_f + 3.0 + float(sy) * 5.0, -12.0), Vector3(7, 4.6, 6), Color(0.08, 0.08, 0.1))
			spk.material_override.roughness = 0.8
			var cone := MeshInstance3D.new()
			var cmh := CylinderMesh.new(); cmh.top_radius = 2.2; cmh.bottom_radius = 0.6; cmh.height = 0.8
			cone.mesh = cmh
			cone.material_override = m._soft_mat(Color(0.3, 0.3, 0.35), 0.1)
			cone.rotation_degrees = Vector3(90, 0, 0)
			cone.position = origin + Vector3(sx, stage_f + 3.0 + float(sy) * 5.0, -8.9)
			m.add_child(cone); m.game_nodes.append(cone)
	# overhead lighting truss with colored spotlights + beams
	var truss = m._course_box(origin + Vector3(0, stage_f + 24.0, -10.0), Vector3(44, 1.0, 1.0), Color(0.2, 0.2, 0.22))
	truss.material_override.metallic = 0.6
	for li in range(5):
		var lx2: float = -18.0 + float(li) * 9.0
		var lc: Color = rcols[li % rcols.size()]
		var sl := OmniLight3D.new()
		sl.light_color = lc; sl.light_energy = 2.6; sl.omni_range = 26.0
		sl.position = origin + Vector3(lx2, stage_f + 22.0, -8.0)
		m.add_child(sl); m.game_nodes.append(sl)
		var beam := MeshInstance3D.new()
		var bcone := CylinderMesh.new(); bcone.top_radius = 0.4; bcone.bottom_radius = 5.0; bcone.height = 22.0
		beam.mesh = bcone
		var bmm := StandardMaterial3D.new()
		bmm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bmm.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		bmm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bmm.albedo_color = Color(lc.r, lc.g, lc.b, 0.14)
		beam.material_override = bmm
		beam.position = origin + Vector3(lx2, stage_f + 12.0, -9.0)
		m.add_child(beam); m.game_nodes.append(beam)
	# floating music notes drifting over the crowd
	for ni in range(10):
		var note := Label3D.new()
		note.text = ["♪", "♫", "♩", "♬"][ni % 4]
		note.font_size = 120; note.modulate = rcols[ni % rcols.size()]
		note.outline_size = 10; note.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		note.position = origin + Vector3(randf() * 36.0 - 18.0, stage_f + 6.0 + randf() * 14.0, 2.0 + randf() * 12.0)
		m.add_child(note); m.game_nodes.append(note)
	var rainbow := rcols
	for i in range(7):
		var orb := MeshInstance3D.new()
		var sph := SphereMesh.new()
		sph.radius = 1.25
		sph.height = 2.5
		orb.mesh = sph
		var om := StandardMaterial3D.new()
		om.albedo_color = rainbow[i]
		om.emission_enabled = true
		om.emission = rainbow[i]
		om.emission_energy_multiplier = 1.5
		orb.material_override = om
		orb.position = origin + Vector3(-12.0 + float(i) * 4.0, 5.0 + fmod(float(i) * 2.7, 8.0), -6.0 + fmod(float(i) * 3.3, 12.0))
		m.add_child(orb)
		m.game_nodes.append(orb)
		var ov := Vector3(sin(float(i) * 2.1), sin(float(i) * 1.3) * 0.6, cos(float(i) * 1.7)).normalized() * (6.0 + float(i % 3) * 2.0)
		(m.g["orbs"] as Array).append({"node": orb, "vel": ov, "caught": false})
	m.show_msg(fr["fname"], "Catch all 7 colors of the rainbow! Swim into the bouncing orbs!")

func _tick_melody(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	var caught: int = int(m.g["caught"])
	m.hud_game.text = "Rainbow colors: %d / 7" % caught
	# Phase 6: the one deliberate verb — orbs WAIT just out of reach until
	# Roshan swims toward them. No timer, no fail: a held orb hovers and
	# sparkles at the hold ring, and drifts in the moment she moves at it.
	var mprev: Vector3 = m.g.get("ppos_prev", ppos)
	var mvel: Vector3 = (ppos - mprev) / maxf(delta, 0.001)
	m.g["ppos_prev"] = ppos
	if mvel.length() < 2.0 and caught == 0:
		m.g["still_t"] = float(m.g.get("still_t", 0.0)) + delta
	else:
		m.g["still_t"] = 0.0
	if float(m.g.get("still_t", 0.0)) > 8.0 and not bool(m.g.get("hinted", false)):
		m.g["hinted"] = true
		m.show_msg("Gabby", "Swim to the colors! They are waiting for YOU!", "hint")
	for ob in m.g["orbs"]:
		if bool(ob["caught"]):
			continue
		var node: MeshInstance3D = ob["node"]
		var v: Vector3 = ob["vel"]
		node.position += v * delta
		var rel: Vector3 = node.position - m.ARENA_POS
		if absf(rel.x) > 16.0:
			v.x = -v.x
			node.position.x = m.ARENA_POS.x + clampf(rel.x, -16.0, 16.0)
		if rel.y < 2.6 or rel.y > 17.0:
			v.y = -v.y
			node.position.y = m.ARENA_POS.y + clampf(rel.y, 2.6, 17.0)
		if absf(rel.z) > 12.0:
			v.z = -v.z
			node.position.z = m.ARENA_POS.z + clampf(rel.z, -12.0, 12.0)
		ob["vel"] = v
		node.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 6.0 + node.position.x) * 0.10)
		# hold ring AFTER the wall clamps so a wall can never shove a held orb
		# back into the catch box; 22 clears the whole 14x7x14 box (diag ~21).
		# The `continue` also gates the catch itself — a stationary player
		# cannot catch, no matter where the orb bounces.
		var to_orb: Vector3 = node.position - ppos
		var d2p: float = maxf(to_orb.length(), 0.001)
		if d2p < 22.0 and mvel.dot(to_orb / d2p) < 2.0:
			node.position = ppos + (to_orb / d2p) * 22.0
			if float(m.g.get("still_t", 0.0)) > 4.0 and fmod(float(m.g["t"]), 1.5) < delta:
				# visual pointer while she idles: a sparkle midway to the orb
				m._sparkle_burst(ppos.lerp(node.position, 0.4), Color(1.0, 0.95, 0.7))
			continue
		if absf(node.position.x - ppos.x) < 14.0 and absf(node.position.y - ppos.y) < 7.0 and absf(node.position.z - ppos.z) < 14.0:
			ob["caught"] = true
			node.visible = false
			caught += 1
			m.g["caught"] = caught
			m._sparkle_burst(node.position, (node.material_override as StandardMaterial3D).albedo_color)
			if m.chime != null:
				m.chime.pitch_scale = 0.9 + float(caught) * 0.07
				m.chime.play()
			if m.voice != null and caught % 2 == 0:
				m.voice.pitch_scale = 1.0 + randf() * 0.25
				m.voice.play()
			if caught >= 7:
				m._end_game(true, fr, "You caught the WHOLE rainbow! Gabby and her friends cheer!")
				return
