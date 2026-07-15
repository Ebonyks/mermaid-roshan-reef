class_name SeekGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# seek minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["found"] = 0
	m.g["timer"] = -1.0
	m.g["help_t"] = 0.0
	m.g["seek_anchor"] = m.player.position
	m.g["bushes"] = []
	for i in range(4):
		var bush := MeshInstance3D.new()
		var bm3 := SphereMesh.new()
		bm3.radius = 2.4
		bm3.height = 3.4
		bush.mesh = bm3
		var bmat3 := StandardMaterial3D.new()
		bmat3.albedo_color = m.BTN_COLS[i] * 0.55 + Color(0.25, 0.45, 0.25)
		bmat3.albedo_texture = load("res://assets/terrain/up_grass_col.jpg")
		bmat3.uv1_triplanar = true
		bmat3.uv1_scale = Vector3(3.0, 3.0, 3.0)
		bmat3.normal_enabled = true
		bmat3.normal_texture = load("res://assets/terrain/scales_normal.png")
		bmat3.normal_scale = 1.0
		bmat3.roughness = 1.0
		bmat3.emission_enabled = true
		bmat3.emission = m.BTN_COLS[i] * 0.3
		bmat3.emission_energy_multiplier = 0.7
		bush.material_override = bmat3
		bush.position = origin + m.BTN_OFFS[i] + Vector3(0, 2.2, 0)
		m.add_child(bush)
		m.game_nodes.append(bush)
		(m.g["bushes"] as Array).append(bush)
	var lamb_ps: PackedScene = load("res://assets/characters/lamb.glb")
	var lamb: Node3D
	if lamb_ps != null:
		lamb = lamb_ps.instantiate()
		lamb.scale = Vector3.ONE * 2.6
		m.add_child(lamb)
		m.game_nodes.append(lamb)
	else:
		lamb = m._game_ball(Color(1.0, 0.99, 0.95), 1.2)
	m.g["lamb"] = lamb
	m._decorate_lamb_meadow(origin)
	_seek_hide()
	m.show_msg(fr["fname"], "Lamb-a' is playing in the meadow! Find her behind a wiggly bush!")

func tick(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m.hud_game.text = "Find Lamb-a'! %d / 4" % int(m.g["found"])
	# giggle beacon: she can be HEARD from the wiggly bush, not just seen
	m.g["gig_t"] = float(m.g.get("gig_t", 2.0)) - delta
	if float(m.g["gig_t"]) <= 0.0:
		m.g["gig_t"] = 2.8
		if m.voice != null:
			m.voice.pitch_scale = 1.45 + randf() * 0.15
			m.voice.play()
	var which: int = int(m.g.get("which", 0))
	var bush: MeshInstance3D = (m.g["bushes"] as Array)[which]
	m.g["help_t"] = float(m.g.get("help_t", 0.0)) + delta
	var help_radius: float = minf(9.0, 4.0 + float(m.g["help_t"]) * 0.35)
	var seek_anchor: Vector3 = m.g.get("seek_anchor", ppos)
	var moved_to_seek: bool = ppos.distance_to(seek_anchor) > 0.75
	var hit: bool = m._btn_pressed() == which or (moved_to_seek and bush.position.distance_to(ppos) < help_radius)
	if hit:
		m.g["found"] = int(m.g["found"]) + 1
		m.g["help_t"] = 0.0
		var lamb2: Node3D = m.g["lamb"]
		lamb2.position = bush.position + Vector3(0, 4.8, 0)
		var twl = m.create_tween()
		twl.tween_property(lamb2, "scale", Vector3.ONE * 3.4, 0.2)
		twl.tween_property(lamb2, "scale", Vector3.ONE * 2.6, 0.3)
		if m.voice != null:
			m.voice.pitch_scale = 1.0 + randf() * 0.3
			m.voice.play()
		if int(m.g["found"]) >= 4:
			m._end_game(true, fr, "You found Lamb-a' every time! Best seeker ever!")
			return
		_seek_hide()

func _seek_hide() -> void:
	m.g["seek_anchor"] = m.player.position
	m.g["which"] = randi() % 4
	var bush: MeshInstance3D = (m.g["bushes"] as Array)[int(m.g["which"])]
	(m.g["lamb"] as Node3D).position = bush.position + Vector3(0, 0.5, -2.2)
	(m.g["lamb"] as Node3D).rotation.y = 0.0
	# audit: the wiggle used to stop after ~2.5s (8 loops) and every bush went
	# still — a slow seeker lost the only signal. It wiggles until found now.
	if m.g.get("wiggle_tw") != null and (m.g["wiggle_tw"] as Tween).is_valid():
		(m.g["wiggle_tw"] as Tween).kill()
	var tw = m.create_tween().set_loops()
	tw.tween_property(bush, "scale", Vector3(1.35, 0.75, 1.35), 0.16)
	tw.tween_property(bush, "scale", Vector3.ONE, 0.16)
	tw.tween_interval(0.9)
	m.g["wiggle_tw"] = tw
	m.g["gig_t"] = 2.2   # Lamb-a' giggles from her hiding spot (audio beacon)
