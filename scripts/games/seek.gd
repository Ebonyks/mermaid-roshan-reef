class_name SeekGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# seek minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _decorate_lamb_meadow(origin: Vector3) -> void:
	# a soft rolling green meadow for Lamb-a' to play in
	var hill := MeshInstance3D.new()
	var hs := SphereMesh.new()
	hs.radius = 60.0
	hs.height = 120.0
	hill.mesh = hs
	var hm := StandardMaterial3D.new()
	hm.albedo_texture = load("res://assets/terrain/up_grass_col.jpg")
	hm.albedo_color = Color(0.92, 1.0, 0.9)
	hm.normal_enabled = true
	hm.normal_texture = load("res://assets/terrain/up_grass_nrm.jpg")
	hm.uv1_triplanar = true
	hm.uv1_world_triplanar = true
	hm.uv1_scale = Vector3(0.05, 0.05, 0.05)
	hm.roughness = 1.0
	hill.material_override = hm
	hill.position = origin + Vector3(0, -56.0, 0)
	m.add_child(hill)
	m.game_nodes.append(hill)
	# scattered living things around the play circle (kept clear of the bushes)
	var trees := ["tree_pineRoundF", "tree_default_fall", "tree_simple_fall", "tree_fat"]
	var flowers := ["flower_redA", "flower_yellowB", "flower_purpleA"]
	var seed := 11
	for k in range(40):
		seed = (seed * 1103515245 + 12345) & 0x7fffffff
		var ang: float = float(seed % 1000) / 1000.0 * TAU
		var rad: float = 16.0 + float((seed / 1000) % 1000) / 1000.0 * 26.0
		var gp := origin + Vector3(cos(ang) * rad, 1.0, sin(ang) * rad)
		var pick := (seed / 7) % 10
		var yr := float(seed % 628) / 100.0
		var tree_name: String = trees[(seed / 13) % trees.size()] if pick < 3 else ""
		var placement_role: String = tree_name if pick < 3 else "soft_flora"
		if not _lamb_meadow_placement_allowed(Vector2(gp.x - origin.x, gp.z - origin.z), placement_role):
			continue
		if pick < 3:
			m._nature(tree_name, gp, 4.5 + float(seed % 3), yr)
			m._cyl_solid(gp + Vector3(0, 3.0, 0), 0.9, 3.0, 0.5)   # trunks solid; hide-bushes stay soft
		elif pick < 5:
			m._nature("plant_bushLargeTriangle", gp, 4.0, yr)
		elif pick < 6:
			m._nature("mushroom_red", gp, 4.0, yr)
		elif pick < 7:
			m._nature("mushroom_tanGroup", gp, 4.5, yr)
		elif pick < 8:
			m._nature("grass_leafsLarge", gp, 3.5, yr)
		else:
			m._nature(flowers[(seed / 17) % flowers.size()], gp, 4.5, yr)
	# Layered storybook clouds keep a readable silhouette and cool painted underside.
	for c in range(5):
		var cl: Node3D = LandmarkArtFactory.create_cloud(5.0 + randf() * 2.0, c)
		cl.position = origin + Vector3(randf() * 70.0 - 35.0, 28.0 + randf() * 10.0, randf() * 70.0 - 35.0)
		m.add_child(cl)
		m.game_nodes.append(cl)
	var sun := OmniLight3D.new()
	sun.light_color = Color(1.0, 0.95, 0.8)
	sun.light_energy = 0.9
	sun.omni_range = 70.0
	sun.position = origin + Vector3(18, 30, 12)
	m.add_child(sun)
	m.game_nodes.append(sun)


func _lamb_meadow_placement_allowed(local: Vector2, role: String) -> bool:
	if local.length() < 15.0 or local.length() > 44.0 or role == "tree_palm":
		return false
	var clearance: float = 12.0 if role.begins_with("tree_") else 8.5
	for bush_offset: Vector3 in m.BTN_OFFS:
		if local.distance_to(Vector2(bush_offset.x, bush_offset.z)) < clearance:
			return false
	return true

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["found"] = 0
	m.g["timer"] = -1.0
	m.g["help_t"] = 0.0
	m.g["seek_anchor"] = m.player.position
	m.g["bushes"] = []
	for i in range(4):
		var bush: Node3D = m._art35_prop(
			"res://assets/art35/arena/meadow_bush_%d.glb" % i,
			origin + m.BTN_OFFS[i] + Vector3(0, 0.6, 0), 1.40, float(i) * 0.55)
		if bush == null:
			continue
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
	_decorate_lamb_meadow(origin)
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
	var bush: Node3D = (m.g["bushes"] as Array)[which]
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
	var bush: Node3D = (m.g["bushes"] as Array)[int(m.g["which"])]
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
