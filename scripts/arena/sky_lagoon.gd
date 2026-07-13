class_name SkyLagoon
extends RefCounted
# Phase 7.3: mechanical extraction of the Sky Lagoon courtyard from main.gd
# (pearl-castle build, terrain + rivers + moat math, night dressing, fairy
# pond, courtyard tick). All state stays on main; main delegates through
# the original entry points, so lagoon_h()/player callers are unchanged.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_pearl_castle(o: Vector3) -> void:
	m.wall_pics = []
	# ---------- warm daytime sun for the sky lagoon (soft shadows) ----------
	var sun2 := DirectionalLight3D.new()
	sun2.rotation_degrees = Vector3(-48.0, 35.0, 0.0)
	sun2.light_color = Color(0.6, 0.68, 0.95) if m.is_night else Color(1.0, 0.96, 0.86)
	sun2.light_energy = 0.5 if m.is_night else 1.15
	sun2.shadow_enabled = (m.quality != "speedy")
	sun2.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sun2.directional_shadow_max_distance = 110.0
	sun2.light_specular = 0.3
	m.add_child(sun2)
	m.game_nodes.append(sun2)
	# ---------- rolling-hill grass terrain + carved river valleys (real -Y depth) ----------
	_build_lagoon_terrain(o)
	# ---------- rocky floating-island underside ----------
	var cliff := MeshInstance3D.new()
	var cc := CylinderMesh.new()
	cc.top_radius = 236.0
	cc.bottom_radius = 120.0
	cc.height = 54.0
	cc.radial_segments = 40
	cliff.mesh = cc
	cliff.material_override = m._up_mat("cliff", 0.04, Color(0.8, 0.74, 0.68))   # rugged rock face
	cliff.position = o + Vector3(0, -29.0, 0)
	m.add_child(cliff)
	m.game_nodes.append(cliff)
	# ---------- grand path from the spawn to the castle ----------
	var path := MeshInstance3D.new()
	var pb := BoxMesh.new()
	pb.size = Vector3(18.0, 0.6, 270.0)
	path.mesh = pb
	path.material_override = m._up_mat("cobble", 0.05)   # cobblestone path to the castle (same stone size as the basement floors)
	path.position = o + Vector3(0, 2.4, 45.0)
	m.add_child(path)
	m.game_nodes.append(path)
	# lamp posts + banners (her book art) line the path
	var banners := ["p_seattle", "p_snowman", "p_garden", "p_trampoline", "p_slide", "p_xmas"]
	for li in range(6):
		var z := 150.0 - float(li) * 46.0
		for sgn in [-1.0, 1.0]:
			var post = m._l2_box(o + Vector3(sgn * 13.0, 6.0, z), Vector3(1.0, 12.0, 1.0), Color(0.5, 0.36, 0.22))
			m._cyl_solid(o + Vector3(sgn * 13.0, 6.0, z), 0.9, 6.0, 0.5)
			var lampbulb := MeshInstance3D.new()
			var lb := SphereMesh.new()
			lb.radius = 1.1
			lb.height = 2.2
			lampbulb.mesh = lb
			var lm := StandardMaterial3D.new()
			lm.emission_enabled = true
			lm.emission = Color(1.0, 0.85, 0.5)
			lm.emission_energy_multiplier = 3.0
			lampbulb.material_override = lm
			lampbulb.position = o + Vector3(sgn * 13.0, 12.5, z)
			m.add_child(lampbulb)
			m.game_nodes.append(lampbulb)
			var lo := OmniLight3D.new()
			lo.light_color = Color(1.0, 0.85, 0.55)
			lo.light_energy = 1.6
			lo.omni_range = 26.0
			lo.position = lampbulb.position
			m.add_child(lo)
			m.game_nodes.append(lo)
		# a hanging banner of her memories on the left posts
		m._hang_portrait(o + Vector3(-13.0, 7.0, z) + Vector3(0.7, 0, 0), Vector3(0, 90, 0), banners[li])
	# ---------- Phase 4a: courtyard GATEHOUSE (Kenney Castle Kit, CC0) ----------
	# a chunky storybook welcome framing the path entrance near the spawn. The
	# path itself stays fully open — towers sit flush with the path edges
	# (x ±15, solids leave a clear |x| < 8 channel), no arch overhead, no pinch.
	var gz := 164.0
	for gsgn: float in [-1.0, 1.0]:
		var tx: float = gsgn * 15.0
		var ty: float = _lagoon_local(tx, gz)
		m._kit("castle/tower-square", o + Vector3(tx, ty - 0.4, gz), 13.0)   # 1x1x1.31 piece -> ~17 tall
		m._cyl_solid(o + Vector3(tx, ty + 8.5, gz), 6.6, 9.0, 0.8)
		m._kit("castle/flag", o + Vector3(tx, ty + 16.6, gz), 2.6)
		# a lower bastion stub outboard of each tower
		var wx: float = gsgn * 26.0
		var wy: float = _lagoon_local(wx, gz)
		m._kit("castle/wall", o + Vector3(wx, wy - 0.4, gz), 11.0)
		m._wall_solid(o + Vector3(wx, wy + 6.0, gz), Vector3(11.0, 12.0, 11.0), 0.8)
	# ---------- decorate the meadow with CC0 nature (dense, grounded, clustered) ----------
	var trees := ["tree_palm", "tree_pineRoundF", "tree_default_fall", "tree_simple_fall", "tree_fat"]
	var flowers := ["flower_redA", "flower_yellowB", "flower_purpleA"]
	var sd := 3
	# tree CLUSTERS (little groves read as a real forest edge)
	for grove in range(14):
		sd = (sd * 1103515245 + 12345) & 0x7fffffff
		var ga: float = float(sd % 1000) / 1000.0 * TAU
		@warning_ignore("integer_division")
		var grad: float = 60.0 + float((sd / 1000) % 1000) / 1000.0 * 165.0
		var gcx: float = cos(ga) * grad
		var gcz: float = sin(ga) * grad
		if absf(gcx) < 26.0 and gcz > -95.0 and gcz < 165.0:
			continue
		# keep the train corridor clear: no grove may straddle the ring of
		# track around the castle (radius 78 about (0,-120); trees scatter
		# up to ±10 from the grove centre, hence the wide 26-unit band)
		if absf(sqrt(gcx * gcx + (gcz + 120.0) * (gcz + 120.0)) - 78.0) < 26.0:
			continue
		@warning_ignore("integer_division")
		for t in range(3 + (sd / 3) % 4):
			sd = (sd * 1103515245 + 12345) & 0x7fffffff
			var ox: float = float(sd % 200) / 10.0 - 10.0
			@warning_ignore("integer_division")
			var oz: float = float((sd / 200) % 200) / 10.0 - 10.0
			var tpos := o + Vector3(gcx + ox, _lagoon_local(gcx + ox, gcz + oz) - 0.5, gcz + oz)
			@warning_ignore("integer_division")
			var tname: String = trees[(sd / 11) % trees.size()]
			if tname == "tree_pineRoundF":
				# GEN2 pilot: the round puff tree is the family-style one now
				var gtree = m._gen2_prop("tree_pineroundf", tpos, 8.0 + float(sd % 5), float(sd % 628) / 100.0)
				if gtree != null:
					m.game_nodes.append(gtree)
				else:
					m._nature(tname, tpos, 9.0 + float(sd % 5), float(sd % 628) / 100.0)
			else:
				m._nature(tname, tpos, 9.0 + float(sd % 5), float(sd % 628) / 100.0)
			# collision audit #1: the whole forest was ghost — trunks are solid now
			m._cyl_solid(tpos + Vector3(0, 6.0, 0), 1.3, 6.0, 0.6)
	# undergrowth: bushes, mushrooms, grass tufts, flower clumps
	for k in range(90):
		sd = (sd * 1103515245 + 12345) & 0x7fffffff
		var ang: float = float(sd % 1000) / 1000.0 * TAU
		@warning_ignore("integer_division")
		var rad: float = 26.0 + float((sd / 1000) % 1000) / 1000.0 * 200.0
		var px: float = cos(ang) * rad
		var pz: float = sin(ang) * rad
		if absf(px) < 13.0 and pz > -92.0 and pz < 168.0:
			continue
		# undergrowth also stays off the train track band
		if absf(sqrt(px * px + (pz + 120.0) * (pz + 120.0)) - 78.0) < 13.0:
			continue
		@warning_ignore("integer_division")
		var pick := (sd / 7) % 10
		var gp := Vector3(px, _lagoon_local(px, pz) - 0.2, pz)
		var yr := float(sd % 628) / 100.0
		if pick < 3:
			m._nature("plant_bushLargeTriangle", o + gp, 6.0, yr)
		elif pick < 5:
			m._nature("plant_bush", o + gp, 5.0, yr)
		elif pick < 6:
			m._nature("mushroom_red", o + gp, 5.0, yr)
		elif pick < 7:
			m._nature("mushroom_tanGroup", o + gp, 5.5, yr)
		elif pick < 8:
			m._nature("grass_leafsLarge", o + gp, 5.0, yr)
		else:
			@warning_ignore("integer_division")
			m._nature(flowers[(sd / 17) % flowers.size()], o + gp, 6.0, yr)
	# a calm pond off to the side, ringed with cattails
	var pond := MeshInstance3D.new()
	var pondm := CylinderMesh.new()
	pondm.top_radius = 34.0
	pondm.bottom_radius = 34.0
	pondm.height = 0.6
	pond.mesh = pondm
	# Phase 5: shared toon water — the pond gets a foam ring right at its rim
	var pmm = m._toon_water_mat(Color(0.24, 0.55, 0.78), Color(0.5, 0.82, 0.92), 0.82, 0.12, 0.06)
	pmm.set_shader_parameter("foam_width", 1.8)
	pond.material_override = pmm
	pond.position = o + Vector3(-95, _lagoon_local(-95, 70) + 0.6, 70)
	m.add_child(pond)
	m.game_nodes.append(pond)
	for ct in range(14):
		var cta: float = float(ct) / 14.0 * TAU
		var cpx: float = -95 + cos(cta) * 36.0
		var cpz: float = 70 + sin(cta) * 36.0
		m._nature("grass_leafsLarge", o + Vector3(cpx, _lagoon_local(cpx, cpz) - 0.3, cpz), 5.5, randf() * TAU)
	# ---------- Phase 4b: PLAYGROUND corner + park dressing (Tiny Treats, CC0) ----------
	# a real play-place on the east meadow: slide, swings, merry-go-round,
	# seesaw, sandbox and a spring horse. Pure toy, no objectives — and the
	# sandbox stays non-solid on purpose so Roshan can plop right into it.
	# [name, local pos, footprint, y-rot, solid radius, solid half-height]
	# owner 2026-07-11: toys sized for ROSHAN (she is ~7 units) so riding them
	# reads true, and each records a play anchor for the play-moments below.
	# Playground audit 2026-07-11: the east river runs (150,40)->(95,110)->
	# (45,180) right through the old spots — the swing sat 9.9 units deep in
	# the channel, the carousel 8.4, the pony 3.9. Everything now stays west
	# of the river with >5 units of dry bank, and the slide is rotated so the
	# chute empties into the open meadow instead of at the waterline.
	var pg: Array = [
		["play/slide_A", Vector3(78.0, 0, 88.0), 18.0, -2.0, 6.5, 6.5, "slide", 5.6],
		["play/swing_A_large", Vector3(58.0, 0, 92.0), 18.0, -0.4, 7.5, 6.5, "swing", 6.2],
		["play/merry_go_round", Vector3(60.0, 0, 120.0), 14.0, 0.0, 7.5, 4.5, "merry", 4.6],
		["play/seesaw_large", Vector3(70.0, 0, 106.0), 13.0, 1.2, 5.0, 3.2, "seesaw", 3.6],
		["play/sandbox_round_decorated", Vector3(92.0, 0, 74.0), 15.0, 0.0, 0.0, 0.0, "sandbox", 4.6],
		["play/spring_horse_A", Vector3(88.0, 0, 60.0), 9.0, -1.8, 3.5, 4.0, "horse", 3.4],
	]
	m.g["toys"] = []
	for row: Array in pg:
		var pgx: float = (row[1] as Vector3).x
		var pgz: float = (row[1] as Vector3).z
		var pgy: float = _lagoon_local(pgx, pgz)
		var tgt: float = float(row[2])
		var tyrot: float = float(row[3])
		var tnode: Node3D = m._kit(row[0], o + Vector3(pgx, pgy - 0.3, pgz), tgt, tyrot)
		if float(row[4]) > 0.0:
			m._cyl_solid(o + Vector3(pgx, pgy + float(row[5]), pgz), float(row[4]), float(row[5]), 0.6)
		var kind: String = String(row[6])
		var base := o + Vector3(pgx, pgy, pgz)
		var fwd := Vector3(sin(tyrot), 0, cos(tyrot))
		var left := Vector3(cos(tyrot), 0, -sin(tyrot))
		var anchor: Vector3 = base
		match kind:
			"swing":
				anchor = base + Vector3(0, tgt * 0.22, 0)   # the seat at rest, under the bar
			"slide":
				# the LADDER FOOT (-fwd side): she climbs the steps herself now,
				# so the moment starts on the ground, not teleported to the top
				anchor = base - fwd * (tgt * 0.40) + Vector3(0, 2.0, 0)
			"seesaw":
				# the OPEN seat is the -left end (owner playtest 2026-07-11:
				# the anchor sat on the painted side — the wrong side to ride)
				anchor = base - left * tgt * 0.32 + Vector3(0, tgt * 0.24, 0)
			"sandbox":
				anchor = base + Vector3(0, 1.6, 0)
			"merry":
				anchor = base + Vector3(0, tgt * 0.18, 0)
			"horse":
				anchor = base + Vector3(0, tgt * 0.52, 0)
		(m.g["toys"] as Array).append({"kind": kind, "anchor": anchor, "base": base,
			"fwd": fwd, "left": left, "tgt": tgt, "node": tnode, "cool": 4.0, "dur": float(row[7])})
	# park dressing: a fountain plaza beside the path near the spawn, benches
	# by the pond, and soft hedges lining the grand path (low + non-solid so
	# neither Roshan nor the audit probe can ever get pinched by decoration)
	var fy: float = _lagoon_local(-30.0, 140.0)
	m._kit("park/fountain", o + Vector3(-30.0, fy - 0.3, 140.0), 12.0)
	m._cyl_solid(o + Vector3(-30.0, fy + 2.4, 140.0), 6.4, 2.6, 0.6)
	for brow: Array in [[-55.0, 62.0, 2.2], [-88.0, 112.0, -0.6], [-38.0, 132.0, 2.8]]:
		var bpy: float = _lagoon_local(float(brow[0]), float(brow[1]))
		m._kit("park/bench", o + Vector3(float(brow[0]), bpy - 0.2, float(brow[1])), 5.0, float(brow[2]))
	for hz: float in [127.0, 81.0, 35.0]:
		for hsgn: float in [-1.0, 1.0]:
			var hy: float = _lagoon_local(hsgn * 17.0, hz)
			m._kit("park/hedge_straight_long", o + Vector3(hsgn * 17.0, hy - 0.3, hz), 10.0, PI * 0.5)
	# (rivers + fish are built as real carved valleys in _build_lagoon_terrain above)
	# player-crafted FRIENDS from the Crafting Studio hang around the courtyard
	m.g["crafted"] = []
	for fi in range(m.custom_friends.size()):
		var cf2: Array = m.custom_friends[fi]
		if cf2.size() < 7:
			continue
		var frn = m._make_creature_node(String(cf2[0]), Color(cf2[1], cf2[2], cf2[3]), Color(cf2[4], cf2[5], cf2[6]))
		var fang: float = float(fi) * 1.3
		frn.position = o + Vector3(cos(fang) * (34.0 + float(fi % 5) * 11.0), 6.0, 70.0 + sin(fang) * 45.0)
		m.add_child(frn)
		m.game_nodes.append(frn)
		(m.g["crafted"] as Array).append({"node": frn, "cool": 0.0})
	# a big rainbow arc over the meadow
	var rainbow := MeshInstance3D.new()
	var rt := TorusMesh.new()
	rt.inner_radius = 118.0
	rt.outer_radius = 130.0
	rt.rings = 48
	rt.ring_segments = 24
	rainbow.mesh = rt
	var rbsh := Shader.new()
	rbsh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded;\nvoid fragment(){\n\tfloat b = UV.y;\n\tvec3 c = vec3(0.0);\n\tif(b<0.16)c=vec3(0.9,0.2,0.3);else if(b<0.33)c=vec3(1.0,0.6,0.2);else if(b<0.5)c=vec3(1.0,0.9,0.3);else if(b<0.66)c=vec3(0.3,0.8,0.4);else if(b<0.83)c=vec3(0.3,0.6,1.0);else c=vec3(0.6,0.4,0.9);\n\tALBEDO=c;\n\tEMISSION=c*0.4;\n\tALPHA=0.6;\n}"
	var rbm := ShaderMaterial.new()
	rbm.shader = rbsh
	rainbow.material_override = rbm
	rainbow.position = o + Vector3(40, 0, -10)
	rainbow.rotation_degrees = Vector3(0, 0, 90)
	m.add_child(rainbow)
	m.game_nodes.append(rainbow)
	# the two legs of the rainbow are the Rainbow Road race gateways (right leg = reversed lap)
	var rb_center := o + Vector3(40, 0, -10)
	var legaz: float = rb_center.z + 124.0
	var legbz: float = rb_center.z - 124.0
	m.kart_legA = Vector3(rb_center.x, m.lagoon_h(rb_center.x, legaz) + 6.0, legaz)
	m.kart_legB = Vector3(rb_center.x, m.lagoon_h(rb_center.x, legbz) + 6.0, legbz)
	m._kart_gateway(m.kart_legA, "Rainbow Race!", Color(0.4, 0.85, 1.0))
	m._kart_gateway(m.kart_legB, "Rainbow Race!\n(reverse lap)", Color(1.0, 0.6, 0.95))
	# the door to LEVEL 3 sits between the two race legs. Locked until the
	# rainbow race has carried Roshan there once; a direct portal afterwards.
	var bwz: float = (legaz + legbz) * 0.5
	m.bw_portal_pos = Vector3(rb_center.x, m.lagoon_h(rb_center.x, bwz) + 14.0, bwz)
	if m.galaxy_unlocked:
		m._kart_gateway(m.bw_portal_pos, "🦋 Butterfly World!\nSwim in!", Color(1.0, 0.8, 0.3))
		var bwg = m._butterfly_gate(4.2)
		bwg.position = m.bw_portal_pos
		m.add_child(bwg)
		m.game_nodes.append(bwg)
	else:
		var lockl := Label3D.new()
		lockl.text = "🦋 Butterfly World\nwin the Rainbow Race to soar there!"
		lockl.font_size = 54
		lockl.pixel_size = 0.03
		lockl.outline_size = 12
		lockl.modulate = Color(1.0, 0.9, 0.6)
		lockl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		lockl.position = m.bw_portal_pos + Vector3(0, 4.0, 0)
		m.add_child(lockl)
		m.game_nodes.append(lockl)
	# (home portal removed — the way back to the ocean is now inside the castle / Level 3)
	# drifting butterflies for life — GEN2 pilot: real family-style
	# butterfly art instead of the flower.png stand-in
	var bfly := CPUParticles3D.new()
	bfly.amount = 26
	bfly.lifetime = 6.0
	bfly.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
	bfly.emission_box_extents = Vector3(180, 14, 180)
	bfly.gravity = Vector3.ZERO
	bfly.initial_velocity_min = 2.0
	bfly.initial_velocity_max = 5.0
	bfly.angular_velocity_min = -90.0
	bfly.angular_velocity_max = 90.0
	bfly.scale_amount_min = 1.2
	bfly.scale_amount_max = 2.0
	var bq := QuadMesh.new()
	bq.size = Vector2(1.2, 1.2)
	bfly.mesh = bq
	var bmat := StandardMaterial3D.new()
	bmat.albedo_texture = load("res://assets/props/gen2/butterfly1.png")
	bmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	bmat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	bmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	bfly.material_override = bmat
	bfly.position = o + Vector3(0, 14, 30)
	m.add_child(bfly)
	m.game_nodes.append(bfly)
	# ...and six HERO butterflies that really flap (vertex-sine wing fold,
	# assets/shaders/butterfly_flap.gdshader) hovering over the meadow
	var flap_sh = load("res://assets/shaders/butterfly_flap.gdshader")
	var wing_texs := ["res://assets/props/gen2/butterfly1.png", "res://assets/props/gen2/butterfly2.png"]
	var hero_spots := [Vector3(60, 9, 80), Vector3(-70, 8, 60), Vector3(95, 10, -30),
		Vector3(-95, 11, 74), Vector3(40, 8, 150), Vector3(-45, 9, -70)]
	for hb in range(hero_spots.size()):
		var hq := QuadMesh.new()
		hq.size = Vector2(3.2, 2.6)
		hq.orientation = PlaneMesh.FACE_Y
		var hmat := ShaderMaterial.new()
		hmat.shader = flap_sh
		hmat.set_shader_parameter("wing_tex", load(wing_texs[hb % 2]))
		hmat.set_shader_parameter("phase", float(hb) * 1.7)
		hmat.set_shader_parameter("flap_speed", 8.0 + float(hb % 3))
		var hmi := MeshInstance3D.new()
		hmi.mesh = hq
		hmi.material_override = hmat
		hmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		var hpos: Vector3 = hero_spots[hb]
		hmi.position = o + Vector3(hpos.x, _lagoon_local(hpos.x, hpos.z) + hpos.y, hpos.z)
		hmi.rotation.y = float(hb) * 1.1
		m.add_child(hmi)
		m.game_nodes.append(hmi)
	# ---------- the castle (back of the island) ----------
	var c := o + Vector3(0, 0, -120.0)
	# the moat is carved into the lagoon terrain (see _lagoon_moat_dip); the bridge crosses it
	# a long wooden bridge from the courtyard, ACROSS the moat, right up to the door
	var bridge = m._l2_box(c + Vector3(0, 2.6, 40.0), Vector3(13.0, 0.8, 60.0), Color(0.62, 0.45, 0.28))
	bridge.material_override = m._up_mat("wood", 0.12, Color(0.82, 0.6, 0.42))   # real wood-plank PBR (was a flat tan slab)
	# bridge railings + posts
	for bsgn in [-1.0, 1.0]:
		m._l2_box(c + Vector3(bsgn * 6.2, 4.0, 40.0), Vector3(0.6, 2.2, 60.0), Color(0.5, 0.36, 0.22))
		m._wall_solid(c + Vector3(bsgn * 6.2, 4.0, 40.0), Vector3(0.6, 2.2, 60.0), 0.4)   # rails keep her ON the bridge
		for bp in range(7):
			m._l2_box(c + Vector3(bsgn * 6.2, 4.2, 12.0 + float(bp) * 9.0), Vector3(1.0, 3.0, 1.0), Color(0.45, 0.32, 0.2))
	# keep + battlements
	# keep — a STONE shell with a real doorway opening, so the open door reveals a warm interior (not a white void)
	var _stone := load("res://assets/terrain/up_castle_col.jpg")
	var _keep_parts := [
		m._l2_box(c + Vector3(-18, 26, 12), Vector3(20, 52, 1.5), Color(0.88, 0.86, 0.92)),
		m._l2_box(c + Vector3(18, 26, 12), Vector3(20, 52, 1.5), Color(0.88, 0.86, 0.92)),
		m._l2_box(c + Vector3(0, 38, 12), Vector3(16, 28, 1.5), Color(0.88, 0.86, 0.92)),
		m._l2_box(c + Vector3(0, 26, -28), Vector3(56, 52, 1.5), Color(0.82, 0.80, 0.87)),
		m._l2_box(c + Vector3(-28, 26, -8), Vector3(1.5, 52, 40), Color(0.84, 0.82, 0.89)),
		m._l2_box(c + Vector3(28, 26, -8), Vector3(1.5, 52, 40), Color(0.84, 0.82, 0.89)),
		m._l2_box(c + Vector3(0, 52, -8), Vector3(56, 1.5, 40), Color(0.82, 0.80, 0.87))]
	for _kp in _keep_parts:
		_kp.material_override = m._up_mat("marble", 0.05, Color(0.99, 0.97, 1.0))   # royal white marble, ONE scale across keep/battlements/turrets
	# --- collision: the keep shell is SOLID. The doorway (and the secret moat
	# hatch) are the only ways in — without these the star-gated door was cosmetic.
	# collision audit #3: solids reach the courtyard CEILING (y120) — the walls
	# are 52 tall but the mermaid could float to y54+ and drift straight over
	# the keep, skipping the Dream-Star door entirely
	m._wall_solid(c + Vector3(-18, 60, 12), Vector3(20, 120, 1.5))   # front wall, left of the door
	m._wall_solid(c + Vector3(18, 60, 12), Vector3(20, 120, 1.5))    # front wall, right of the door
	m._wall_solid(c + Vector3(0, 72, 12), Vector3(16, 96, 1.5))      # lintel + air above the doorway
	m._wall_solid(c + Vector3(0, 60, -28), Vector3(56, 120, 1.5))    # back wall
	m._wall_solid(c + Vector3(-28, 60, -8), Vector3(1.5, 120, 40))   # side walls
	m._wall_solid(c + Vector3(28, 60, -8), Vector3(1.5, 120, 40))
	# ---- warm interior foyer, visible through the doorway ----
	var _foyback = m._l2_box(c + Vector3(0, 12, -2), Vector3(22, 24, 1.0), Color(0.9, 0.66, 0.45))
	_foyback.material_override.albedo_texture = _stone
	_foyback.material_override.uv1_triplanar = true
	_foyback.material_override.uv1_scale = Vector3(0.05, 0.05, 0.05)
	m._l2_box(c + Vector3(0, 0.7, 5), Vector3(13, 0.4, 16), Color(0.72, 0.16, 0.22))      # red carpet leading in
	m._l2_box(c + Vector3(-11, 12, 5), Vector3(1.0, 24, 14), Color(0.84, 0.82, 0.89))     # foyer left wall
	m._l2_box(c + Vector3(11, 12, 5), Vector3(1.0, 24, 14), Color(0.84, 0.82, 0.89))      # foyer right wall
	m._l2_box(c + Vector3(0, 24, 5), Vector3(22, 1.0, 14), Color(0.80, 0.78, 0.85))       # foyer ceiling
	var _foylight := OmniLight3D.new()
	_foylight.light_color = Color(1.0, 0.82, 0.5)
	_foylight.light_energy = 3.2
	_foylight.omni_range = 32.0
	_foylight.position = c + Vector3(0, 14, 6)
	m.add_child(_foylight); m.game_nodes.append(_foylight)
	m._hang_portrait(c + Vector3(0, 13, -1.3), Vector3(0, 0, 0), "p_seattle")             # a glimpse of 'inside'''
	for bx in range(-4, 5):
		m._l2_box(c + Vector3(float(bx) * 6.0, 53.0, -8.0), Vector3(3.5, 6.0, 40.0), Color(0.9, 0.88, 0.95))
	# four big towers (solid shafts — Roshan slides around them)
	for tw_off: Vector3 in [Vector3(-32.0, 2.0, 10.0), Vector3(32.0, 2.0, 10.0), Vector3(-32.0, 2.0, -28.0), Vector3(32.0, 2.0, -28.0)]:
		_l2_tower(c + tw_off, 1.9)
		m._cyl_solid(c + tw_off + Vector3(0, 60.0, 0), 5.6, 60.0)   # tower solids reach the sky too
		# STORYBOOK FORK: coral cone roofs turn the stone towers into a shell palace
		var roof := MeshInstance3D.new()
		var rcone := CylinderMesh.new()
		rcone.top_radius = 0.2
		rcone.bottom_radius = 7.4
		rcone.height = 9.0
		rcone.radial_segments = 14
		roof.mesh = rcone
		var rmat := StandardMaterial3D.new()
		rmat.albedo_color = Color(0.96, 0.62, 0.66)
		rmat.roughness = 1.0
		roof.material_override = rmat
		roof.position = c + tw_off + Vector3(0, 52.0, 0)
		m.add_child(roof)
		m.game_nodes.append(roof)
	# scallop-shell crest along the front wall top + painted glowing windows
	for si2 in range(7):
		var shell := MeshInstance3D.new()
		var ssm := SphereMesh.new()
		ssm.radius = 2.6
		ssm.height = 5.2
		shell.mesh = ssm
		var shm := StandardMaterial3D.new()
		shm.albedo_color = Color(0.98, 0.80, 0.86) if si2 % 2 == 0 else Color(0.78, 0.86, 0.97)
		shm.roughness = 1.0
		shell.material_override = shm
		shell.position = c + Vector3(-18.0 + float(si2) * 6.0, 52.5, 12.0)
		m.add_child(shell)
		m.game_nodes.append(shell)
	for wx2: float in [-11.0, 11.0]:
		var winq := MeshInstance3D.new()
		var wqm := QuadMesh.new()
		wqm.size = Vector2(4.5, 7.0)
		winq.mesh = wqm
		var wmm := StandardMaterial3D.new()
		wmm.albedo_color = Color(0.82, 0.78, 0.98)
		wmm.emission_enabled = true
		wmm.emission = Color(1.0, 0.9, 0.7)
		wmm.emission_energy_multiplier = 1.1
		winq.material_override = wmm
		winq.position = c + Vector3(wx2, 20.0, 12.85)
		m.add_child(winq)
		m.game_nodes.append(winq)
	# ---- the Mermaid Roshan stained glass — the grand centrepiece on the FRONT facade ----
	m._glass_window(c + Vector3(0, 38.0, 12.3), Vector3(0, 0, 0), 30.0)
	# gold frame around the rose window
	for fxg in [-1.0, 1.0]:
		m._l2_box(c + Vector3(fxg * 11.5, 38.0, 12.2), Vector3(1.2, 32.0, 1.0), Color(0.95, 0.8, 0.4), 0.3)
	m._l2_box(c + Vector3(0, 54.0, 12.2), Vector3(24.0, 1.2, 1.0), Color(0.95, 0.8, 0.4), 0.3)
	m._l2_box(c + Vector3(0, 22.0, 12.2), Vector3(24.0, 1.2, 1.0), Color(0.95, 0.8, 0.4), 0.3)
	# ---- crenellated battlements along the keep top ----
	for cz2 in [12.0, -28.0]:
		for cmx in range(-4, 5):
			var mr = m._l2_box(c + Vector3(float(cmx) * 6.4, 53.5, cz2), Vector3(3.2, 5.0, 2.0), Color(0.9, 0.88, 0.95))
			mr.material_override = m._up_mat("marble", 0.05, Color(0.99, 0.97, 1.0))
	for cmx2 in range(-3, 4):
		for csx in [-28.0, 28.0]:
			var mr2 = m._l2_box(c + Vector3(csx, 53.5, -8.0 + float(cmx2) * 6.4), Vector3(2.0, 5.0, 3.2), Color(0.9, 0.88, 0.95))
			mr2.material_override = m._up_mat("marble", 0.05, Color(0.99, 0.97, 1.0))
	# ---- royal banners flanking the door ----
	for bxs in [-1.0, 1.0]:
		var ban := MeshInstance3D.new()
		var banq := QuadMesh.new(); banq.size = Vector2(5.0, 18.0)
		ban.mesh = banq
		var banm := StandardMaterial3D.new()
		banm.albedo_color = Color(0.7, 0.18, 0.3) if bxs < 0.0 else Color(0.2, 0.35, 0.7)
		banm.emission_enabled = true; banm.emission = banm.albedo_color * 0.4
		banm.cull_mode = BaseMaterial3D.CULL_DISABLED; banm.roughness = 0.9
		ban.material_override = banm
		ban.position = c + Vector3(bxs * 9.5, 17.0, 12.6)
		m.add_child(ban); m.game_nodes.append(ban)
		# a little gold star crest on the banner
		var crest := Label3D.new()
		crest.text = "★"; crest.font_size = 110; crest.modulate = Color(1.0, 0.88, 0.4)
		crest.position = c + Vector3(bxs * 9.5, 19.0, 12.8)
		m.add_child(crest); m.game_nodes.append(crest)
	# big arched door (starts closed)
	var door = m._l2_box(c + Vector3(0, 12.0, 12.4), Vector3(16.0, 24.0, 1.2), Color(0.62, 0.42, 0.26), 0.0)
	door.material_override = m._up_mat("door", 0.045, Color(1, 1, 1))   # GEN2 castle-door planks + iron strapwork (audit: wood read as the road)
	door.material_override.uv1_world_triplanar = false   # the door slides open — keep its planks glued to the mesh, not the world
	m.l2_door = door
	m.g["door_closed_y"] = door.position.y
	m.g["entry"] = door.position
	# the closed door is solid; _open_castle_door removes this entry when it slides up
	m._wall_solid(door.position, Vector3(16.0, 24.0, 1.2))
	m.g["door_solid"] = m.arena_solids.back()
	# glowing archway frame (revealed when the door opens)
	var arch = m._l2_box(c + Vector3(0, 12.0, 12.0), Vector3(17.0, 25.0, 0.4), Color(0.55, 0.9, 1.0), 0.0)
	arch.visible = false
	m.g["arch"] = arch
	# ---------- HIDDEN BACK DOOR: a secret hatch on the moat floor behind the keep ----------
	# A curious explorer who dives into the moat and swims around the back finds a way in
	# that bypasses the 3 Dream Stars. It sits at the DEEPEST point of the carved ring
	# behind the castle (the trench runs at ring-distance 46..64 from the keep, so the
	# hatch lives at the trench midline, ~y -15 — NOT against the wall, which is dry land).
	var back_pos: Vector3 = c + Vector3(0, -14.5, -55.0)   # moat-trench floor, directly behind the keep
	var recess = m._l2_box(c + Vector3(0, -10.0, -49.0), Vector3(11.0, 10.0, 1.0), Color(0.04, 0.06, 0.08))
	recess.material_override.roughness = 1.0                 # a dark opening in the trench's inner bank
	var hatch = m._l2_box(back_pos, Vector3(9.0, 1.0, 7.0), Color(0.2, 0.22, 0.28))
	hatch.material_override = m._up_mat("castle", 0.08, Color(0.7, 0.72, 0.8))   # stone hatch on the floor
	var bglow := OmniLight3D.new()                          # dim glow: findable, but still 'hidden'
	bglow.light_color = Color(0.5, 0.85, 1.0); bglow.light_energy = 1.3; bglow.omni_range = 13.0
	bglow.position = back_pos + Vector3(0, 2.2, 0)
	m.add_child(bglow); m.game_nodes.append(bglow)
	m.g["back_entry"] = back_pos
	var dl := Label3D.new()
	dl.text = "Princess Huluu\u2019s Castle"
	dl.font_size = 90
	dl.outline_size = 18
	dl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	dl.position = c + Vector3(0, 30.0, 14.0)
	m.add_child(dl)
	m.game_nodes.append(dl)
	# ---------- 3 Dream Stars: low + along the path, easy for a 4yo ----------
	var spots: Array = m.L2_STAR_SPOTS
	for idx in range(spots.size()):
		var sp: Vector3 = o + spots[idx]
		# a low, friendly platform with a soft ramp feel
		var _plat = m._l2_box(sp + Vector3(0, -3.5, 0), Vector3(12, 1.4, 12), Color(0.9, 0.82, 0.98), 0.1)
		m._nature("flower_yellowB", sp + Vector3(-3, -2.6, -3), 4.0, 0.0)
		m._nature("flower_redA", sp + Vector3(3, -2.6, 3), 4.0, 1.0)
		var star := Label3D.new()
		star.text = "\u2605"
		star.font_size = 340
		star.pixel_size = 0.05
		star.modulate = Color(1.0, 1.0, 1.0)
		star.outline_size = 34
		star.set_meta("rainbow", randf() * TAU)
		star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		star.position = sp + Vector3(0, 4.0, 0)
		m.add_child(star)
		m.game_nodes.append(star)
		var sl := OmniLight3D.new()
		sl.light_color = Color(1.0, 0.9, 0.5)
		sl.light_energy = 3.2
		sl.omni_range = 34.0
		star.add_child(sl)
		var pre_got: bool = idx < m.l2_star_progress.size() and bool(m.l2_star_progress[idx])
		if pre_got:
			star.visible = false
		m.l2_stars.append({"node": star, "got": pre_got})
	# ---------- clouds + rainbow accents ----------
	for cz in range(14):
		var cloud := MeshInstance3D.new()
		var cs := SphereMesh.new()
		cs.radius = 8.0 + randf() * 7.0
		cs.height = 10.0
		cloud.mesh = cs
		var cm2 := StandardMaterial3D.new()
		cm2.albedo_color = Color(1, 1, 1)
		cm2.roughness = 1.0
		cloud.material_override = cm2
		cloud.position = o + Vector3(randf() * 380.0 - 190.0, 55.0 + randf() * 40.0, randf() * 380.0 - 190.0)
		cloud.scale = Vector3(2.2, 0.7, 1.7)
		m.add_child(cloud)
		m.game_nodes.append(cloud)
	# ---------- the COURTYARD TRAIN: a ride circling the castle ----------
	# built LAST so its clip-guard can snapshot every solid above; the ride
	# seats join g["toys"] and play through the same play-moment system
	m._train_ref()._build_train(o)
	_build_fairy_pond(o)


func _build_lagoon_terrain(o: Vector3) -> void:
	# blended terrain material: lush grass on the hills/plains, muddy dirt down in the
	# river valleys (CC0 Poly Haven sets), with normal maps for real surface depth
	var tsh := Shader.new()
	tsh.code = "shader_type spatial;\n" + \
		"uniform sampler2D grass_t; uniform sampler2D grass_n; uniform sampler2D dirt_t; uniform sampler2D dirt_n;\n" + \
		"uniform float tile = 0.045; uniform float blo = -6.0; uniform float bhi = 2.5;\n" + \
		"varying float ly;\n" + \
		"void vertex(){ ly = VERTEX.y; }\n" + \
		"void fragment(){\n" + \
		"  vec2 uv = UV * tile;\n" + \
		"  float g = smoothstep(blo, bhi, ly);\n" + \
		"  ALBEDO = mix(texture(dirt_t, uv).rgb, texture(grass_t, uv).rgb, g);\n" + \
		"  NORMAL_MAP = mix(texture(dirt_n, uv).rgb, texture(grass_n, uv).rgb, g);\n" + \
		"  ROUGHNESS = 0.95;\n" + \
		"}"
	var gm := ShaderMaterial.new()
	gm.shader = tsh
	gm.set_shader_parameter("grass_t", load("res://assets/terrain/up_grass_col.jpg"))
	gm.set_shader_parameter("grass_n", load("res://assets/terrain/up_grass_nrm.jpg"))
	gm.set_shader_parameter("dirt_t", load("res://assets/terrain/up_dirt_col.jpg"))
	gm.set_shader_parameter("dirt_n", load("res://assets/terrain/up_dirt_nrm.jpg"))
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	# 128 (was 64): at 7.7-unit quads the mesh cut corners across the path
	# shoulder / moat rim (features ~12 units wide), so the visual floor sat
	# up to a few units off lagoon_walk_h and Roshan read as buried (playtest
	# 2026-07-11). Heights are cached one-per-grid-point, so this builds with
	# FEWER _lagoon_local calls than the old 6-per-quad recompute.
	var N := 128
	var span := 245.0
	var step: float = span * 2.0 / float(N)
	var hs := PackedFloat32Array()
	hs.resize((N + 1) * (N + 1))
	for i in range(N + 1):
		var hx: float = -span + float(i) * step
		for j in range(N + 1):
			hs[i * (N + 1) + j] = _lagoon_local(hx, -span + float(j) * step)
	for i in range(N):
		var x0: float = -span + float(i) * step
		var x1: float = x0 + step
		for j in range(N):
			var z0: float = -span + float(j) * step
			var z1: float = z0 + step
			var cx: float = (x0 + x1) * 0.5
			var cz: float = (z0 + z1) * 0.5
			if sqrt(cx * cx + cz * cz) > 245.0:
				continue
			var y00: float = hs[i * (N + 1) + j]
			var y10: float = hs[(i + 1) * (N + 1) + j]
			var y01: float = hs[i * (N + 1) + j + 1]
			var y11: float = hs[(i + 1) * (N + 1) + j + 1]
			# winding gives upward-facing normals
			_terr_v(st, x0, z0, y00); _terr_v(st, x1, z1, y11); _terr_v(st, x0, z1, y01)
			_terr_v(st, x0, z0, y00); _terr_v(st, x1, z0, y10); _terr_v(st, x1, z1, y11)
	st.generate_normals()
	st.generate_tangents()   # needed so the terrain normal maps light correctly
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = gm
	mi.position = o
	m.add_child(mi)
	m.game_nodes.append(mi)
	# ---- river water sitting low in each carved valley, with fish ----
	m.g["l2_fish"] = []
	var fishkinds := ["ClownFish", "Dory", "Carp", "Tuna", "Eel"]
	# Phase 5: shared toon water — streams get tight ripples, gentle wobble,
	# and (on capable tiers) foam edges hugging the carved banks
	var river_mat = m._toon_water_mat(Color(0.2, 0.55, 0.8), Color(0.5, 0.82, 0.9), 0.82, 0.25, 0.05)
	river_mat.set_shader_parameter("foam_width", 2.6)
	river_mat.set_shader_parameter("depth_fade", 7.0)
	for rv in m.LAGOON_RIVERS:
		# the stream is a RIBBON that hugs the carved valley floor sample-by-sample —
		# flat planes got buried wherever the river path crossed a hill (rock on top,
		# water hidden inside the terrain)
		var pts: Array = []
		for i in range(rv.size() - 1):
			var a2: Vector2 = rv[i]
			var b2: Vector2 = rv[i + 1]
			var seg_len: float = a2.distance_to(b2)
			var steps: int = maxi(2, int(seg_len / 4.0))
			for si in range(steps):
				pts.append(a2.lerp(b2, float(si) / float(steps)))
		pts.append(rv[rv.size() - 1])
		var st2 := SurfaceTool.new()
		st2.begin(Mesh.PRIMITIVE_TRIANGLES)
		for i in range(pts.size()):
			var p2: Vector2 = pts[i]
			var pn: Vector2 = pts[mini(i + 1, pts.size() - 1)]
			var pp: Vector2 = pts[maxi(i - 1, 0)]
			var d2: Vector2 = (pn - pp)
			d2 = d2.normalized() if d2.length() > 0.001 else Vector2(0, 1)
			var perp := Vector2(-d2.y, d2.x) * 16.3
			# the water FILLS the channel: surface 1.5 under the bank rim, and the
			# ribbon is slightly wider than the waterline so its edges bury into
			# the banks (no gap, no floating-band look). Depth ~10.5 = deep swims.
			var floor_h: float = _lagoon_local(p2.x, p2.y)
			var dip_h: float = _lagoon_river_dip(p2.x, p2.y)
			var wy: float = maxf(floor_h + 0.8, (floor_h + dip_h) - 1.5)
			var v: float = float(i) / float(pts.size())
			st2.set_normal(Vector3.UP)
			st2.set_uv(Vector2(0.0, v * 6.0))
			st2.add_vertex(Vector3(p2.x + perp.x, wy, p2.y + perp.y))
			st2.set_normal(Vector3.UP)
			st2.set_uv(Vector2(1.0, v * 6.0))
			st2.add_vertex(Vector3(p2.x - perp.x, wy, p2.y - perp.y))
		for i in range(pts.size() - 1):
			var a3 := i * 2
			st2.add_index(a3); st2.add_index(a3 + 1); st2.add_index(a3 + 3)
			st2.add_index(a3); st2.add_index(a3 + 3); st2.add_index(a3 + 2)
		st2.generate_tangents()   # toon_water writes NORMAL_MAP -> mesh must carry tangents
		var water := MeshInstance3D.new()
		water.mesh = st2.commit()
		water.material_override = river_mat
		water.position = o
		m.add_child(water); m.game_nodes.append(water)
		# fish swimming down the channel
		var ra: Vector2 = rv[0]
		var rb: Vector2 = rv[rv.size() - 1]
		var rdir3: Vector3 = Vector3(rb.x - ra.x, 0, rb.y - ra.y).normalized()
		var rlen: float = ra.distance_to(rb)
		for fz in range(6):
			var fishinst = m._place_aq(fishkinds[fz % fishkinds.size()], Vector3.ZERO, 1.0 + randf() * 0.6, true)
			if fishinst != null:
				m.game_nodes.append(fishinst)
				var fa := o + Vector3(ra.x, _lagoon_local(ra.x, ra.y) + 1.5, ra.y)
				(m.g["l2_fish"] as Array).append({"node": fishinst, "a": fa, "dir": rdir3, "len": rlen, "off": randf() * rlen, "spd": 4.0 + randf() * 4.0, "lane": randf() * 6.0 - 3.0})
	# ---- moat water: the channel is FULL (surface 2.5 under the rim, like the
	# rivers), mostly opaque, and painted with the GEN2 family-style water
	# albedo. The old sheet sat at -6 in a 16-deep trench, so from the grounds
	# you saw six units of bare mud wall and barely any water — the moat kept
	# reading as a dry dirt ditch (owner report x5). Still divable: the sheet
	# has no collision and the hidden hatch sits at the floor below. ----
	var mst := SurfaceTool.new()
	mst.begin(Mesh.PRIMITIVE_TRIANGLES)
	var mseg := 72
	for i in range(mseg + 1):
		var ma2: float = float(i) / float(mseg) * TAU
		var ca2: float = cos(ma2)
		var sa2: float = sin(ma2)
		var v2: float = float(i) / float(mseg)
		mst.set_normal(Vector3.UP)
		mst.set_uv(Vector2(0.0, v2 * 14.0))
		mst.add_vertex(Vector3(m.MOAT_CX + ca2 * (m.MOAT_INNER - 1.5), -2.5, m.MOAT_CZ + sa2 * (m.MOAT_INNER - 1.5)))
		mst.set_normal(Vector3.UP)
		mst.set_uv(Vector2(1.0, v2 * 14.0))
		mst.add_vertex(Vector3(m.MOAT_CX + ca2 * (m.MOAT_OUTER + 1.5), -2.5, m.MOAT_CZ + sa2 * (m.MOAT_OUTER + 1.5)))
	for i in range(mseg):
		var a4 := i * 2
		mst.add_index(a4); mst.add_index(a4 + 1); mst.add_index(a4 + 3)
		mst.add_index(a4); mst.add_index(a4 + 3); mst.add_index(a4 + 2)
	mst.generate_tangents()   # toon_water writes NORMAL_MAP -> mesh must carry tangents
	var moatw := MeshInstance3D.new()
	moatw.mesh = mst.commit()
	# Phase 5: shared toon water + GEN2 painted albedo so it reads as WATER
	# from every angle and on every quality tier
	var mwmat = m._toon_water_mat(Color(0.16, 0.45, 0.7), Color(0.42, 0.75, 0.88), 0.92, 0.2, 0.04)
	mwmat.set_shader_parameter("foam_width", 2.4)
	mwmat.set_shader_parameter("albedo_tex", load("res://assets/terrain/gen2_water_col.jpg"))
	mwmat.set_shader_parameter("albedo_mix", 0.85)
	mwmat.set_shader_parameter("albedo_scale", 0.035)
	moatw.material_override = mwmat
	moatw.position = o
	m.add_child(moatw)
	m.game_nodes.append(moatw)


func _build_lagoon_night(o: Vector3) -> void:
	# subtle night dressing for the Sky Lagoon: a moon + a scatter of twinkling stars
	var moon := MeshInstance3D.new()
	var ms := SphereMesh.new(); ms.radius = 16.0; ms.height = 32.0
	moon.mesh = ms
	moon.material_override = m._soft_mat(Color(1.0, 0.97, 0.85), 2.2)
	moon.position = o + Vector3(-120.0, 130.0, -180.0)
	m.add_child(moon); m.game_nodes.append(moon)
	var ml := OmniLight3D.new()
	ml.light_color = Color(0.7, 0.78, 1.0); ml.light_energy = 1.2; ml.omni_range = 400.0
	ml.position = moon.position; m.add_child(ml); m.game_nodes.append(ml)
	var sd := 91
	for k in range(60):
		sd = (sd * 1103515245 + 12345) & 0x7fffffff
		var ang: float = float(sd % 1000) / 1000.0 * TAU
		@warning_ignore("integer_division")
		var el: float = 0.3 + float((sd / 1000) % 1000) / 1000.0 * 0.6
		var dist := 260.0
		var star := MeshInstance3D.new()
		var ss := SphereMesh.new(); ss.radius = 0.7 + float(sd % 5) * 0.25; ss.height = ss.radius * 2.0
		star.mesh = ss
		star.material_override = m._soft_mat(Color(1.0, 1.0, 0.92), 3.0)
		star.position = o + Vector3(cos(ang) * dist * cos(el), 60.0 + el * 150.0, sin(ang) * dist * cos(el))
		m.add_child(star); m.game_nodes.append(star)


func _build_fairy_pond(o: Vector3) -> void:
	# a glowing fairy pond off in the courtyard — swim into it (after the castle opens)
	# to fly the top-down fairy sparkle dodger
	var c: Vector3 = o + Vector3(125.0, 0.0, 35.0)
	m.fairy_pond_pos = c + Vector3(0, 6.0, 0)
	var pond := MeshInstance3D.new()
	var cm := CylinderMesh.new(); cm.top_radius = 17.0; cm.bottom_radius = 17.0; cm.height = 1.0
	pond.mesh = cm
	var pmat := StandardMaterial3D.new()
	pmat.albedo_color = Color(0.4, 0.55, 0.95); pmat.metallic = 0.85; pmat.roughness = 0.07
	pmat.emission_enabled = true; pmat.emission = Color(0.5, 0.55, 1.0); pmat.emission_energy_multiplier = 0.6
	pond.material_override = pmat
	pond.position = c + Vector3(0, 2.6, 0)
	m.add_child(pond); m.game_nodes.append(pond)
	# a ring of glowing fairy flowers around it
	for k in range(10):
		var a: float = float(k) / 10.0 * TAU
		var fl := MeshInstance3D.new()
		var fm := SphereMesh.new(); fm.radius = 1.3; fm.height = 2.6
		fl.mesh = fm
		fl.material_override = m._soft_mat(Color.from_hsv(float(k) / 10.0, 0.5, 1.0), 1.5)
		fl.position = c + Vector3(cos(a) * 17.0, 3.4, sin(a) * 17.0)
		m.add_child(fl); m.game_nodes.append(fl)
	var l := OmniLight3D.new()
	l.light_color = Color(0.7, 0.72, 1.0); l.light_energy = 2.6; l.omni_range = 32.0
	l.position = c + Vector3(0, 9, 0); m.add_child(l); m.game_nodes.append(l)
	var lab := Label3D.new()
	lab.text = "🧚 Fairy Pond — fly!"
	lab.font_size = 64; lab.pixel_size = 0.05; lab.outline_size = 14
	lab.modulate = Color(0.88, 0.82, 1.0); lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.position = c + Vector3(0, 13, 0); m.add_child(lab); m.game_nodes.append(lab)


func _sand_puff(pos: Vector3) -> void:
	# a soft cloud of dug-up sand (matte + falls back down — NOT sparkles)
	var cp := CPUParticles3D.new()
	cp.one_shot = true
	cp.emitting = true
	cp.amount = 34
	cp.lifetime = 1.5
	cp.explosiveness = 0.9
	cp.direction = Vector3.UP
	cp.spread = 55.0
	cp.initial_velocity_min = 3.0
	cp.initial_velocity_max = 7.0
	cp.gravity = Vector3(0, -7.0, 0)
	cp.damping_min = 1.0
	cp.damping_max = 2.5
	cp.scale_amount_min = 0.4
	cp.scale_amount_max = 0.9
	var gm := SphereMesh.new()
	gm.radius = 0.22
	gm.height = 0.44
	gm.radial_segments = 6
	gm.rings = 3
	cp.mesh = gm
	var pm := StandardMaterial3D.new()
	pm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	pm.albedo_color = Color(0.85, 0.7, 0.48)
	cp.material_override = pm
	cp.position = pos
	m.add_child(cp)
	var tw: Tween = m.create_tween()
	tw.tween_interval(1.8)
	tw.tween_callback(cp.queue_free)


func _tick_toys(delta: float, ppos: Vector3) -> void:
	# HER PLAYGROUND (owner 2026-07-11, animation pass 2026-07-11): swim close
	# to a toy in the courtyard and Roshan really PLAYS it — she grips the
	# swing chains and pumps a true pendulum arc while the frame rocks with
	# her, hops step by step up the slide ladder and rides the chute down
	# (along it, never through it), digs the sandbox with alternating arms in
	# a cloud of sand, bounces the OPEN seat of her one-sided seesaw (the
	# plank dips under her weight), and rides the carousel and spring pony
	# glued to the moving toy. Cosmetic, short, cooled down; never during a
	# quest moment (hall phase) and never for the headless probes.
	# While a moment runs player._process early-returns, so this tick is the
	# ONE writer for her position, facing, lean and every bone (toy_pose).
	var tp: Dictionary = m.toy_play
	if not tp.is_empty():
		tp["t"] = float(tp["t"]) + delta
		var tt: float = float(tp["t"])
		var kind: String = String(tp["kind"])
		var toy: Dictionary = tp["toy"]
		var a: Vector3 = toy["anchor"]
		var base: Vector3 = toy["base"]
		var tgt: float = float(toy["tgt"])
		var fwd: Vector3 = toy["fwd"]
		var left: Vector3 = toy["left"]
		var dur: float = float(tp["dur"])
		var pl: Node3D = m.player
		var pos: Vector3 = a
		var face: Vector3 = fwd
		var lean := 0.0
		match kind:
			"swing":
				# a real pendulum about the top bar: the arc pumps up, flies,
				# then settles before she hops off; the frame rocks in sync
				var amp: float = 0.45 * smoothstep(0.0, 1.6, tt) * (1.0 - smoothstep(dur - 1.1, dur - 0.15, tt))
				var th: float = amp * sin(tt * 2.5)
				# measured: the top bar sits at 0.75 of the footprint (14 units
				# up), the painted seats hang at 0.22 — a 0.53 rope. She rides
				# a SEAT (offset from the frame centre), not the empty middle.
				var piv: Vector3 = base + left * (tgt * 0.185) + Vector3(0, tgt * 0.75, 0)
				var arm: float = tgt * 0.53
				pos = piv + fwd * (sin(th) * arm) - Vector3(0, cos(th) * arm, 0)
				lean = th
				var sw: Node3D = toy["node"]
				if is_instance_valid(sw):
					sw.rotation.x = th * 0.05
				pl.toy_pose("swing", tt, th)
			"slide":
				# up the ladder hop by hop, a beat at the top, then down the
				# chute on a curve that hugs the slope — and a proud landing
				var climb_T := 2.2
				var pause_T := 0.5
				var ride_T := 1.7
				# measured on play_slide (probe 2026-07-11): ladder foot -0.40,
				# rung plane inclines to -0.26 at the 0.52 platform, hood over
				# the platform (top 0.76 — she ducks under it), chute lip at
				# +0.03 running out to +0.47. Her origin rides ~1.1 above the
				# surface she is on (seated) / ~2.0 (upright on the ground).
				var lfoot: Vector3 = a
				var ltop: Vector3 = base - fwd * (tgt * 0.26) + Vector3(0, tgt * 0.59, 0)
				var lip: Vector3 = base + fwd * (tgt * 0.03) + Vector3(0, tgt * 0.50 + 1.1, 0)
				var mid: Vector3 = base + fwd * (tgt * 0.25) + Vector3(0, tgt * 0.26 + 0.9, 0)
				var out: Vector3 = base + fwd * (tgt * 0.47) + Vector3(0, 2.0, 0)
				if tt < climb_T:
					var hops := 4
					var hd: float = climb_T / float(hops)
					var hk: int = mini(int(tt / hd), hops - 1)
					var hf: float = (tt - float(hk) * hd) / hd
					var p0: Vector3 = lfoot.lerp(ltop, float(hk) / float(hops))
					var p1: Vector3 = lfoot.lerp(ltop, float(hk + 1) / float(hops))
					pos = p0.lerp(p1, hf) + Vector3(0, sin(hf * PI) * 0.8, 0)
					pl.toy_pose("climb", tt, hf)
				elif tt < climb_T + pause_T:
					# scooting over the platform to the lip, ducked under the
					# hood — the duck is a whole-body lean (rotation.x), which
					# stresses no skinning; deep chest pitch tore the ruffle
					pos = ltop.lerp(lip, (tt - climb_T) / pause_T)
					lean = -0.4
					pl.toy_pose("ride", tt, 0.0)
				elif tt < climb_T + pause_T + ride_T:
					var rf: float = (tt - climb_T - pause_T) / ride_T
					var u: float = pow(rf, 1.35)   # gravity: slow off the lip, quick at the bottom
					pos = lip.lerp(mid, u).lerp(mid.lerp(out, u), u)
					lean = -0.4 + smoothstep(0.1, 0.45, u) * 0.55   # duck eases into a gentle whee lean-back
					pl.toy_pose("ride", tt, u)
					if not bool(tp.get("cheered", false)):
						tp["cheered"] = true
						m._sparkle_burst(lip, Color(0.9, 0.95, 1.0))
				else:
					pos = out
					pl.toy_pose("land", tt, (tt - climb_T - pause_T - ride_T) / maxf(dur - climb_T - pause_T - ride_T, 0.01))
					if not bool(tp.get("landed", false)):
						tp["landed"] = true
						m._sparkle_burst(out, Color(1.0, 0.9, 0.6))
			"seesaw":
				# she bounces the open end; her weight presses the plank down
				# on contact and the empty painted end bobs up in answer
				var bnc: float = absf(sin(tt * 3.0))
				var press: float = 1.0 - bnc
				pos = a + Vector3(0, bnc * 1.3 - press * 0.42, 0)
				face = left   # the open seat is the -left end; she faces the unicorn pivot
				lean = -press * 0.12   # presses INTO the handle on each landing
				var ss: Node3D = toy["node"]
				if is_instance_valid(ss):
					ss.rotation.z = 0.10 * press
				pl.toy_pose("seat", tt, bnc * 0.5)
			"sandbox":
				# plopped in the sand, digging with alternating arms — each
				# scoop beat throws a little cloud from that hand
				pos = a + Vector3(0, 0.3, 0)   # nestled into the sand fill (rim is 3.3 high)
				lean = -0.3   # whole-body lean over the sand (kind to the waist ruffle)
				var dph: float = tt * 4.4
				pl.toy_pose("dig", tt, dph)
				var scoop: int = int(floor(dph / PI))
				if scoop != int(tp.get("digs", 0)):
					tp["digs"] = scoop
					var side: float = 1.0 if scoop % 2 == 0 else -1.0
					_sand_puff(pos + fwd * 1.5 + left * (side * 0.9) - Vector3(0, 1.2, 0))
			"merry":
				# glued to the spinning carousel at the angle she grabbed on,
				# facing the way it carries her
				var mn: Node3D = toy["node"]
				var ang: float = (mn.rotation.y if is_instance_valid(mn) else tt) + float(tp.get("ph", 0.0))
				# seated ON the deck just inside the handle bars (base+2.1: deck
				# top ~0.7 + her seated height; 0.36R put her IN the bars)
				pos = Vector3(base.x, base.y + 2.0, base.z) + Vector3(sin(ang), 0, cos(ang)) * (tgt * 0.30)
				face = Vector3(cos(ang), 0, -sin(ang))
				pl.toy_pose("seat", tt, sin(tt * 2.0) * 0.3)
			"horse":
				# she and the pony rock as ONE: the ambient bob is paused and
				# this drives the toy's pitch, seating her on the moving saddle
				var rock: float = sin(tt * 3.3) * 0.16 * smoothstep(0.0, 0.7, tt)
				var hn: Node3D = toy["node"]
				if is_instance_valid(hn):
					hn.rotation.x = rock
				var sh: float = tgt * 0.52
				pos = base + Vector3(0, sh * cos(rock) + 0.35, 0) + fwd * (sh * sin(rock))
				lean = rock
				pl.toy_pose("seat", tt, rock * 3.0)
			"train_cabin", "train_deck":
				# seated on the moving train: glued to the car's seat point,
				# facing the way it carries her, with a gentle carriage sway
				# (validity check BEFORE the typed assign — a freed instance
				# into a typed var is a runtime error)
				if is_instance_valid(toy["node"]):
					var carn: Node3D = toy["node"]
					pos = carn.to_global(toy["seat"] as Vector3) + Vector3(0, sin(tt * 2.6) * 0.12, 0)
					var tface: Vector3 = carn.global_transform.basis.z
					tface.y = 0.0
					if tface.length() > 0.01:
						face = tface.normalized()
				else:
					pos = a
				lean = sin(tt * 1.7) * 0.05
				pl.toy_pose("seat", tt, sin(tt * 2.0) * 0.25)
		# glide onto the toy over the first beat instead of teleporting
		var w: float = smoothstep(0.0, 0.4, tt)
		pl.position = (tp["from"] as Vector3).lerp(pos, w)
		pl.yaw = lerp_angle(float(tp["yaw0"]), atan2(face.x, face.z), w)
		pl.rotation.y = pl.yaw + PI
		pl.rotation.x = lean * w
		# keep the play in frame (the player cam chase is dormant right now)
		var cam: Camera3D = pl.cam
		if cam != null and cam.is_inside_tree():
			cam.position = cam.position.lerp(pl.position - face * 20.0 + Vector3(0, 8.0, 0), 1.0 - pow(0.05, delta))
			cam.look_at(pl.position + Vector3(0, 1.5, 0))
		if tt >= dur:
			toy["cool"] = 24.0
			m.toy_play = {}
			pl.rotation.x = 0.0
			var tn: Node3D = toy["node"]
			if is_instance_valid(tn):
				if kind == "swing" or kind == "horse":
					tn.rotation.x = 0.0
				if tn.has_meta("toy_tw"):
					(tn.get_meta("toy_tw") as Tween).play()   # ambient toy motion resumes
			if "vel" in pl:
				pl.vel = Vector3.ZERO
			if pl.has_method("play_verb"):
				pl.play_verb("cheer" if kind == "slide" else "giggle")
		return
	if String(m.g.get("phase", "")) != "court" or DisplayServer.get_name() == "headless":
		return
	for toy in (m.g.get("toys", []) as Array):
		toy["cool"] = maxf(0.0, float(toy["cool"]) - delta)
		if float(toy["cool"]) <= 0.0 and ppos.distance_to(toy["anchor"]) < 6.5:
			var ph := 0.0
			if String(toy["kind"]) == "merry" and is_instance_valid(toy["node"]):
				var dp: Vector3 = ppos - (toy["base"] as Vector3)
				ph = atan2(dp.x, dp.z) - (toy["node"] as Node3D).rotation.y
			m.toy_play = {"kind": toy["kind"], "toy": toy, "t": 0.0, "dur": toy["dur"], "ph": ph,
				"from": ppos, "yaw0": float(m.player.yaw)}
			var tw: Node3D = toy["node"]
			if is_instance_valid(tw) and tw.has_meta("toy_tw"):
				(tw.get_meta("toy_tw") as Tween).pause()   # she takes the wheel
			m._sparkle_burst(toy["anchor"], Color(1.0, 0.9, 0.6))
			break

func _tick_level2(delta: float, ppos: Vector3) -> void:
	# the train moves first so the ride seats' anchors are fresh when the
	# toy tick reads them (it also hides itself whenever phase != "court")
	m._train_ref()._tick_train(delta, ppos)
	_tick_toys(delta, ppos)
	if m.mg_kind != "":
		m._tick_mg2d(delta)
		return
	if m.l2_cutscene_t >= 0.0:
		m._tick_cutscene(delta)
		return
	if String(m.g.get("phase", "court")) == "hall":
		m._tick_castle_hall(delta, ppos)
		return
	# crafted friends WAVE back: heart puff + happy chirp when Roshan visits
	for cd in m.g.get("crafted", []):
		cd["cool"] = maxf(0.0, float(cd["cool"]) - delta)
		var cn: Node3D = cd["node"]
		if is_instance_valid(cn) and float(cd["cool"]) <= 0.0 and cn.position.distance_to(ppos) < 6.5:
			cd["cool"] = 9.0
			m._greet_heart(cn.position + Vector3(0, 3.0, 0))
			var hop_y: float = cn.position.y
			var hop := cn.create_tween()
			hop.tween_property(cn, "position:y", hop_y + 1.2, 0.18)
			hop.tween_property(cn, "position:y", hop_y, 0.3).set_trans(Tween.TRANS_BOUNCE)
	# night magic: shooting stars streak over the lagoon after bedtime
	if m.is_night:
		m.night_star_t -= delta
		if m.night_star_t <= 0.0:
			m.night_star_t = 5.0 + randf() * 7.0
			m._spawn_shooting_star(ppos)
	# Rainbow Road race — swim into either leg of the rainbow arch (right leg = reversed lap)
	m.kart_cool = maxf(0.0, m.kart_cool - delta)
	m.bw_cool = maxf(0.0, m.bw_cool - delta)
	if m.galaxy_unlocked and m.bw_portal_pos != Vector3.ZERO and m.bw_cool <= 0.0 and m.kart_cool <= 0.0:
		if Vector2(m.bw_portal_pos.x - ppos.x, m.bw_portal_pos.z - ppos.z).length() < 9.0 and absf(m.bw_portal_pos.y - ppos.y) < 10.0:
			m.bw_cool = 10.0
			m.show_msg("Roshan", "To the Butterfly World! Wheee!")
			m._start_galaxy()
			return
	if m.kart_legA != Vector3.ZERO:
		# horizontal distance + generous height tolerance (same forgiving test as the fairy pond)
		var dA: float = Vector2(m.kart_legA.x - ppos.x, m.kart_legA.z - ppos.z).length()
		var dB: float = Vector2(m.kart_legB.x - ppos.x, m.kart_legB.z - ppos.z).length()
		# explicit one-time introduction when you first reach the rainbow
		if not bool(m.g.get("kart_intro", false)) and minf(dA, dB) < 48.0:
			m.g["kart_intro"] = true
			m.show_msg("Rainbow Road", "The rainbow road to ROSHAN GALAXY! Race the rainbow to reach the stars — each side goes a different way around!")
		if minf(dA, dB) < 48.0:
			m.hud_game.text = "Swim INTO the rainbow to race your go-kart!"
		if m.kart_cool <= 0.0:
			if dA < 14.0 and absf(m.kart_legA.y - ppos.y) < 18.0:
				m._start_kart_game(false, "float")
				return
			if dB < 14.0 and absf(m.kart_legB.y - ppos.y) < 18.0:
				m._start_kart_game(true, "float")
				return
	for fd in m.g.get("l2_fish", []):
		var fn2: Node3D = fd["node"]
		if not is_instance_valid(fn2):
			continue
		fd["off"] = fmod(float(fd["off"]) + float(fd["spd"]) * delta, float(fd["len"]))
		var base: Vector3 = (fd["a"] as Vector3) + (fd["dir"] as Vector3) * float(fd["off"])
		var side: Vector3 = (fd["dir"] as Vector3).cross(Vector3.UP).normalized()
		var fp: Vector3 = base + side * float(fd["lane"])
		# swim a fixed height above the LOCAL carved floor (hills cross the rivers)
		fp.y = m.lagoon_h(fp.x, fp.z) + 2.4 + sin(float(m.g.get("t", 0.0)) * 3.0 + float(fd["off"])) * 0.4
		fn2.position = fp
		fn2.look_at(fp + (fd["dir"] as Vector3) * 2.0, Vector3.UP)
	var got := 0
	var nxt: Node3D = null
	for sd in m.l2_stars:
		if bool(sd["got"]):
			got += 1
			continue
		var star: Label3D = sd["node"]
		star.position.y += sin(float(m.g["t"]) * 2.0 + star.position.x) * 0.02
		star.rotate_y(delta * 1.6)
		star.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 4.0) * 0.12)
		if nxt == null:
			nxt = star
		var d: float = star.position.distance_to(ppos)
		# gentle magnet so a 4yo who swims close gets pulled in
		if d < 32.0:
			m.player.position = m.player.position.lerp(star.position, minf(0.85, delta * 1.7 * (1.0 - d / 32.0)))
		if d < 14.0:
			sd["got"] = true
			var sidx: int = m.l2_stars.find(sd)
			if sidx >= 0 and sidx < m.l2_star_progress.size():
				m.l2_star_progress[sidx] = true
			got += 1
			m._sparkle_burst(star.position, Color(1.0, 0.9, 0.4))
			if m.chime != null:
				m.chime.pitch_scale = 1.0 + float(got) * 0.12
				m.chime.play()
			if m.voice != null:
				m.voice.pitch_scale = 1.0 + randf() * 0.2
				m.voice.play()
			star.visible = false
			if star.get_child_count() > 0:
				star.get_child(0).queue_free()
			if got >= 3:
				m._open_castle_door()
	if got >= 3 and not m.l2_open:
		m._open_castle_door()
	# iridescent rainbow shimmer on the dream stars
	for sd2 in m.l2_stars:
		var stn: Label3D = sd2["node"]
		if is_instance_valid(stn) and stn.has_meta("rainbow"):
			var hue: float = fmod(float(m.g["t"]) * 0.4 + float(stn.get_meta("rainbow")), 1.0)
			stn.modulate = Color.from_hsv(hue, 0.55, 1.0)
	# fairy pond — fly the top-down sparkle dodger (active once the castle is open)
	# (the fairy flight now launches from the Fairy Fountain in the Butterfly
	# World — the courtyard pond stays as scenery)
	# the rainbow gateway always takes you back to the ocean
	m.mg_cool = maxf(0.0, m.mg_cool - delta)
	# Phase 1: pictures are OPTIONAL play — inert until the castle is open, so
	# the natural swim line to the Dream Stars can't hijack into a minigame and
	# wipe star progress. Tight 3.5 radius + 0.6s dwell = deliberate visits only.
	if m.mg_cool <= 0.0 and m.mg_kind == "" and m.l2_open:
		var dw: Dictionary = m.g.get("pic_dwell", {})
		for wp in m.wall_pics:
			var wpp: Vector3 = wp["pos"]
			var akey := String(wp["art"])
			if Vector2(wpp.x - ppos.x, wpp.z - ppos.z).length() < 3.5 and absf(wpp.y - ppos.y) < 9.0:
				dw[akey] = float(dw.get(akey, 0.0)) + delta
				if float(dw[akey]) >= 0.6:
					dw[akey] = 0.0
					m.g["pic_dwell"] = dw
					if akey == "p_slide":
						m._l2_start_slide()
					else:
						m._mg2d_open(String(m.PIC_GAME[akey]))
					return
			else:
				dw[akey] = 0.0
		m.g["pic_dwell"] = dw
	# hidden back door: a secret underwater entrance that works even before the stars
	if m.g.has("back_entry"):
		var bpos: Vector3 = m.g["back_entry"]
		if bpos.distance_to(ppos) < 9.0:
			m._enter_castle_interior(true)   # secret hatch -> Daddy's treasure room
			return
	if not m.l2_open:
		m.hud_game.text = "Dream Stars: %d / 3  -  follow the sparkles!" % got
	else:
		m.hud_game.text = "The castle is OPEN!  Swim to the glowing door!"
		# magnet toward the fixed doorway (the door itself slides up out of view)
		var entry: Vector3 = m.g.get("entry", m.l2_door.position)
		var dd: float = Vector2(entry.x - ppos.x, entry.z - ppos.z).length()
		if dd < 36.0:
			var pull: Vector3 = entry + Vector3(0, 2, 10)
			m.player.position = m.player.position.lerp(pull, minf(0.75, delta * 1.5 * (1.0 - dd / 36.0)))
		if dd < 20.0:
			m._enter_castle_interior()

# ============ STAGE 2 MINIGAMES (2D tap overlays, launched from wall pictures) ============


func _l2_tower(pos: Vector3, sc: float = 1.0) -> void:
	# fantasy turret: textured stone shaft, gold band, glowing window, conic roof, flag
	var shaft := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = 3.0 * sc
	cm.bottom_radius = 3.7 * sc
	cm.height = 26.0 * sc
	cm.radial_segments = 16
	shaft.mesh = cm
	shaft.material_override = m._up_mat("marble", 0.05, Color(0.99, 0.97, 1.0))
	shaft.position = pos + Vector3(0, 13.0 * sc, 0)
	m.add_child(shaft)
	m.game_nodes.append(shaft)
	# decorative gold band near the top
	var band := MeshInstance3D.new()
	var bcm := CylinderMesh.new()
	bcm.top_radius = 3.85 * sc; bcm.bottom_radius = 3.85 * sc; bcm.height = 1.4 * sc; bcm.radial_segments = 16
	band.mesh = bcm
	var bm := StandardMaterial3D.new()
	bm.albedo_color = Color(0.95, 0.8, 0.4); bm.metallic = 0.8; bm.roughness = 0.3
	bm.emission_enabled = true; bm.emission = Color(0.9, 0.7, 0.3); bm.emission_energy_multiplier = 0.3
	band.material_override = bm
	band.position = pos + Vector3(0, 24.0 * sc, 0)
	m.add_child(band); m.game_nodes.append(band)
	# glowing arched window facing the courtyard
	var win = m._l2_box(pos + Vector3(0, 16.0 * sc, 3.5 * sc), Vector3(1.8 * sc, 4.2 * sc, 0.5 * sc), Color(1.0, 0.85, 0.5))
	win.material_override.emission_enabled = true
	win.material_override.emission = Color(1.0, 0.8, 0.45)
	win.material_override.emission_energy_multiplier = 1.6
	# steeper conic roof
	var roof := MeshInstance3D.new()
	var rc := CylinderMesh.new()
	rc.top_radius = 0.0
	rc.bottom_radius = 5.0 * sc
	rc.height = 9.5 * sc
	rc.radial_segments = 16
	roof.mesh = rc
	roof.material_override = m._up_mat("roof", 0.12, Color(1.0, 0.7, 0.7))   # clay roof tiles
	roof.position = pos + Vector3(0, 30.7 * sc, 0)
	m.add_child(roof)
	m.game_nodes.append(roof)
	# flagpole + flag
	m._l2_box(pos + Vector3(0, 36.0 * sc, 0), Vector3(0.3 * sc, 8.0 * sc, 0.3 * sc), Color(0.35, 0.28, 0.2))
	var flag := MeshInstance3D.new()
	var fq := QuadMesh.new()
	fq.size = Vector2(3.0 * sc, 1.6 * sc)
	flag.mesh = fq
	var fm := StandardMaterial3D.new()
	fm.albedo_color = Color.from_hsv(randf(), 0.6, 1.0)
	fm.emission_enabled = true
	fm.emission = fm.albedo_color
	fm.emission_energy_multiplier = 0.4
	fm.cull_mode = BaseMaterial3D.CULL_DISABLED
	flag.material_override = fm
	flag.position = pos + Vector3(1.6 * sc, 38.0 * sc, 0)
	m.add_child(flag)
	m.game_nodes.append(flag)


func _seg_dist(p: Vector2, a: Vector2, b: Vector2) -> float:
	var ab: Vector2 = b - a
	var l2: float = ab.length_squared()
	var t := 0.0
	if l2 > 0.0001:
		t = clampf((p - a).dot(ab) / l2, 0.0, 1.0)
	return p.distance_to(a + ab * t)


func _lagoon_river_dip(lx: float, lz: float) -> float:
	var p := Vector2(lx, lz)
	var best := 9999.0
	for rv in m.LAGOON_RIVERS:
		for i in range(rv.size() - 1):
			best = minf(best, _seg_dist(p, rv[i], rv[i + 1]))
	if best >= m.LAGOON_RIVER_W:
		return 0.0
	var t: float = best / m.LAGOON_RIVER_W
	return m.LAGOON_RIVER_DEPTH * (1.0 - t * t)   # parabolic channel, deepest at the centre


func _lagoon_moat_dip(lx: float, lz: float) -> float:
	# annular channel around the castle; flat-ish floor so the hidden door sits low
	var d: float = sqrt((lx - m.MOAT_CX) * (lx - m.MOAT_CX) + (lz - m.MOAT_CZ) * (lz - m.MOAT_CZ))
	if d <= m.MOAT_INNER or d >= m.MOAT_OUTER:
		return 0.0
	var mid: float = (m.MOAT_INNER + m.MOAT_OUTER) * 0.5
	var half: float = (m.MOAT_OUTER - m.MOAT_INNER) * 0.5
	var t: float = absf(d - mid) / half
	return m.MOAT_DEPTH * (1.0 - t * t)


func _lagoon_bump(lx: float, lz: float, cx: float, cz: float, rad: float, amp: float) -> float:
	var d2: float = (lx - cx) * (lx - cx) + (lz - cz) * (lz - cz)
	var r2: float = rad * rad
	if d2 >= r2:
		return 0.0
	var f: float = 1.0 - d2 / r2
	return amp * f * f


func _lagoon_local(lx: float, lz: float) -> float:
	var r: float = sqrt(lx * lx + lz * lz)
	var h := 0.0
	# rolling hills (away from the central castle + path so gameplay stays clear)
	h += _lagoon_bump(lx, lz, -130.0, 20.0, 62.0, 20.0)
	h += _lagoon_bump(lx, lz, 128.0, -20.0, 64.0, 18.0)
	h += _lagoon_bump(lx, lz, -60.0, 168.0, 54.0, 15.0)
	h += _lagoon_bump(lx, lz, 100.0, 150.0, 54.0, 14.0)
	# rivers carve valleys
	h -= _lagoon_river_dip(lx, lz)
	# smoothly flatten the castle disc + the path corridor so they stay solid & level
	var m_disc: float = 1.0 - smoothstep(50.0, 72.0, r)
	var m_path := 0.0
	if lz > -95.0 and lz < 172.0:
		m_path = 1.0 - smoothstep(16.0, 28.0, absf(lx))
	h = lerpf(h, 0.0, maxf(m_disc, m_path))
	# castle moat — carved LAST so it digs even through the flattened path/disc
	h -= _lagoon_moat_dip(lx, lz)
	# island rim falls away at the edge
	if r > 205.0:
		h -= (r - 205.0) * 1.2
	return h


func _terr_v(st: SurfaceTool, lx: float, lz: float, y: float) -> void:
	st.set_uv(Vector2(lx, lz))
	st.add_vertex(Vector3(lx, y, lz))
