class_name CastleHall
extends RefCounted

const LandmarkArtFactory = preload("res://scripts/landmark_art.gd")
# Phase 7.2: mechanical extraction of the Grand Hall (build + tick + the
# music room and bedroom it owns) from main.gd. All state stays on main;
# this class receives main by reference and owns only the logic.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(o: Vector3) -> void:
	m.g["castle_detail_lights"] = []
	# Quiet lavender stone floor: broad value shapes keep the long hall legible
	# without the high-frequency checker/vein noise of the old marble stack.
	var flr := MeshInstance3D.new()
	var fb := BoxMesh.new()
	fb.size = Vector3(70, 1.0, 80)
	flr.mesh = fb
	var fm: StandardMaterial3D = m._castle_mat("floor", 0.028, Color(0.82, 0.79, 0.90))
	flr.material_override = fm
	flr.position = o + Vector3(0, 0, 6)
	m.add_child(flr)
	m.game_nodes.append(flr)
	# plush red carpet runner from the entrance up to the stairs
	var runner = m._l2_box(o + Vector3(0, 0.62, 14.0), Vector3(10.0, 0.15, 52.0), Color(0.72, 0.16, 0.22))
	runner.material_override = m._castle_mat("carpet", 0.055, Color(0.82, 0.72, 0.78))
	for trim in [-5.4, 5.4]:
		m._l2_box(o + Vector3(trim, 0.66, 14.0), Vector3(0.7, 0.2, 52.0), Color(0.95, 0.8, 0.35), 0.15)
	# walls (each upright wall also registers a solid collider so Roshan can't swim through it)
	var wcol := Color(0.76, 0.72, 0.84)
	var scol := Color(0.68, 0.66, 0.78)
	# back wall, SEGMENTED to leave two real doorway openings at x=+-22 (the side archways)
	# GRAND EXPANSION (owner 2026-07-11): the hall rises to 52 — a real great
	# hall — and the center wall gains a GALLERY DOORWAY (x -8..8, y 33..42)
	# from the new balcony into the top chambers.
	m._iwall(o + Vector3(0, 16.5, -34), Vector3(35.0, 33, 1.5), wcol, "castle")    # center, below the gallery door
	m._iwall(o + Vector3(-12.75, 42.5, -34), Vector3(9.5, 19, 1.5), wcol, "castle")  # gallery door, left pier
	m._iwall(o + Vector3(12.75, 42.5, -34), Vector3(9.5, 19, 1.5), wcol, "castle")   # gallery door, right pier
	m._iwall(o + Vector3(0, 47, -34), Vector3(16.0, 10, 1.5), wcol, "castle")        # gallery door, top strip
	m._iwall(o + Vector3(-30.75, 26, -34), Vector3(8.5, 52, 1.5), wcol, "castle")  # left edge
	m._iwall(o + Vector3(30.75, 26, -34), Vector3(8.5, 52, 1.5), wcol, "castle")   # right edge
	m._iwall(o + Vector3(-22, 33.5, -34), Vector3(9.0, 37, 1.5), wcol, "castle")   # lintel over left arch
	m._iwall(o + Vector3(22, 33.5, -34), Vector3(9.0, 37, 1.5), wcol, "castle")    # lintel over right arch
	# side walls, SEGMENTED in three layers (owner 2026-07-12: the upper story
	# wraps around BOTH wings, so the y 33..49 band gains three ARCH OPENINGS
	# per side — swim from the hall straight into the wing galleries):
	#   lower  y 0..33  — downstairs wall with the music/bedroom doorway (z -21..-11)
	#   upper  y 33..49 — arcade: arches at z -21..-11, -1..9 and 19..29
	#   crown  y 49..52 — solid band up to the ceiling
	var bal_gold := Color(0.95, 0.8, 0.35)
	for sgn in [-1.0, 1.0]:
		var sx: float = sgn * 35.0
		m._iwall(o + Vector3(sx, 16.5, 17.5), Vector3(1.5, 33, 57), scol, "castle")   # lower front (z -11..46)
		m._iwall(o + Vector3(sx, 16.5, -27.5), Vector3(1.5, 33, 13), scol, "castle")  # lower back (z -34..-21)
		m._iwall(o + Vector3(sx, 25.5, -16), Vector3(1.5, 15, 10), scol, "castle")    # lintel over the wing door
		m._iwall(o + Vector3(sx, 41, -27.5), Vector3(1.5, 16, 13), scol, "castle")    # arcade pier (z -34..-21)
		m._iwall(o + Vector3(sx, 41, -6), Vector3(1.5, 16, 10), scol, "castle")       # arcade pier (z -11..-1)
		m._iwall(o + Vector3(sx, 41, 14), Vector3(1.5, 16, 10), scol, "castle")       # arcade pier (z 9..19)
		m._iwall(o + Vector3(sx, 41, 37.5), Vector3(1.5, 16, 17.5), scol, "castle")   # arcade pier (z 29..46)
		m._iwall(o + Vector3(sx, 50.5, 6), Vector3(1.5, 3, 80), scol, "castle")       # crown band (y 49..52)
		# gold balustrade across each arch so the openings read as balconies
		for az in [-16.0, 4.0, 24.0]:
			m._l2_box(o + Vector3(sx, 34.6, az), Vector3(0.5, 0.5, 9.0), bal_gold, 0.2)
			for pz in [-3.0, 0.0, 3.0]:
				m._l2_box(o + Vector3(sx, 33.9, az + pz), Vector3(0.4, 1.6, 0.4), bal_gold, 0.15)
	# Projecting bases and cornices give the enormous walls a readable scale and
	# keep floor/wall/ceiling transitions from looking like intersecting slabs.
	for trim_side: float in [-1.0, 1.0]:
		m._l2_box(o + Vector3(trim_side * 34.1, 1.3, 6), Vector3(1.1, 2.6, 78), Color(0.42, 0.38, 0.58))
		m._l2_box(o + Vector3(trim_side * 34.1, 49.2, 6), Vector3(1.1, 2.0, 78), Color(0.66, 0.52, 0.36))
	m._l2_box(o + Vector3(0, 1.3, -33.1), Vector3(68, 2.6, 1.1), Color(0.42, 0.38, 0.58))
	m._l2_box(o + Vector3(0, 51, 6), Vector3(70, 1.5, 80), Color(0.58, 0.54, 0.66))      # ceiling (no collider; the hall zone caps height)
	# regal stained-glass panels behind the throne (the Mermaid Roshan glass now lives
	# on the castle's FRONT exterior — this is a plain coloured rose window for Huluu)
	m._panel_glass(o + Vector3(0, 23, -33.0), Vector3(0, 0, 0), 17.0, 24.0)
	# Dark plum stage piers and a shallow canopy isolate the throne from the wall
	# texture. The window becomes a backdrop rather than the brightest whole wall.
	for stage_side: float in [-1.0, 1.0]:
		m._l2_box(o + Vector3(stage_side * 10.0, 20.0, -32.0), Vector3(2.0, 29.0, 2.2), Color(0.30, 0.24, 0.46))
		var stage_hood: MeshInstance3D = m._l2_box(o + Vector3(stage_side * 5.2, 35.0, -32.0), Vector3(1.8, 13.0, 2.2), Color(0.72, 0.55, 0.28))
		stage_hood.rotation_degrees.z = stage_side * 52.0
	# royal red-carpet staircase up to the throne dais
	for st in range(7):
		var stair: MeshInstance3D = m._l2_box(o + Vector3(0, 1.5 + float(st) * 2.0, -10.0 - float(st) * 2.2), Vector3(16.0 - float(st) * 0.6, 2.0, 3.0), Color(0.72, 0.16, 0.24))
		stair.material_override = m._castle_mat("carpet", 0.055, Color(0.82, 0.72, 0.78))
	# throne dais
	var dais: MeshInstance3D = m._l2_box(o + Vector3(0, 15.0, -27.0), Vector3(14, 2.0, 6), Color(0.72, 0.16, 0.24))
	dais.material_override = m._castle_mat("carpet", 0.055, Color(0.82, 0.72, 0.78))
	m._l2_box(o + Vector3(0, 14.1, -27.0), Vector3(15.0, 0.8, 7.0), Color(0.76, 0.58, 0.28))
	# collision audit #2 (+ stairs pass 2026-07-12): the throne centerpiece was
	# ghostly. The dais/throne block keeps a solid; the STAIRCASE itself is now
	# a ramp-floor zone (see build_expansion) so Roshan rests on and climbs the
	# steps instead of swimming through them. The old one-box solid covered the
	# upper flight and would eject her off the new walkable steps.
	m._wall_solid(o + Vector3(0, 8.0, -27.0), Vector3(14, 16, 6), 0.8)
	if ResourceLoader.exists("res://assets/castle/throne.glb"):
		var tmodel: Node3D = (load("res://assets/castle/throne.glb") as PackedScene).instantiate()
		var th := Node3D.new()
		th.add_child(tmodel)
		m._fit_prop(tmodel, 7.0)
		th.rotation.y = PI            # backrest at +Z in the GLB — turn to face the hall
		th.position = o + Vector3(0, 16.0, -28.0)
		m.add_child(th)
		m.game_nodes.append(th)
	else:
		var throne = m._l2_box(o + Vector3(0, 18.5, -28.0), Vector3(5, 6, 2), Color(0.95, 0.8, 0.4), 0.3)
		throne.material_override.metallic = 0.7
	# Protected book cutout until an owner-approved source-faithful model exists.
	var huluu := Sprite3D.new()
	huluu.texture = load("res://assets/characters/friends/huluu.png")
	huluu.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	huluu.pixel_size = 0.011
	huluu.position = o + Vector3(0, 21.0, -27.0)
	m.add_child(huluu)
	m.game_nodes.append(huluu)
	var hl := OmniLight3D.new()
	hl.light_color = Color(1.0, 0.9, 0.95)
	hl.light_energy = 1.4
	hl.omni_range = 16.0
	hl.position = o + Vector3(0, 22.0, -24.0)
	m.add_child(hl)
	m.game_nodes.append(hl)
	m._register_castle_light(hl, true)
	# ---------- columns line the hall ----------
	for cz in [-24.0, -8.0, 8.0, 24.0]:
		for cx in [-28.0, 28.0]:
			var col := MeshInstance3D.new()
			var colm := CylinderMesh.new()
			colm.top_radius = 2.2
			colm.bottom_radius = 2.6
			colm.height = 34.0
			col.mesh = colm
			var clmat := StandardMaterial3D.new()
			clmat.albedo_color = Color(0.68, 0.64, 0.78)
			clmat.roughness = 0.72
			col.material_override = clmat
			col.position = o + Vector3(cx, 17.0, cz)
			m.add_child(col)
			m.game_nodes.append(col)
			m._cyl_solid(col.position, 2.6, 17.0)   # pillars are solid — Roshan slides around them
			# gold capital + base
			m._l2_box(o + Vector3(cx, 33.6, cz), Vector3(6, 1.4, 6), Color(0.95, 0.8, 0.4), 0.2)
			m._l2_box(o + Vector3(cx, 1.0, cz), Vector3(6, 2.0, 6), Color(0.9, 0.85, 0.7))
			# warm sconce glow at each column
			var sc := OmniLight3D.new()
			sc.light_color = Color(1.0, 0.78, 0.5)
			sc.light_energy = 1.1
			sc.omni_range = 16.0
			sc.position = o + Vector3(cx * 0.86, 20.0, cz)
			m.add_child(sc)
			m.game_nodes.append(sc)
			m._register_castle_light(sc, false)
			var flame := MeshInstance3D.new()
			var fl := SphereMesh.new()
			fl.radius = 0.7
			fl.height = 1.4
			flame.mesh = fl
			var flm := StandardMaterial3D.new()
			flm.emission_enabled = true
			flm.emission = Color(1.0, 0.7, 0.35)
			flm.emission_energy_multiplier = 4.0
			flame.material_override = flm
			flame.position = sc.position
			m.add_child(flame)
			m.game_nodes.append(flame)
	# ---------- tapestries between the columns ----------
	var tcols := [Color(0.46, 0.18, 0.30), Color(0.24, 0.30, 0.52)]
	for ti in range(3):
		for sgn in [-1.0, 1.0]:
			var tap := MeshInstance3D.new()
			var tq := QuadMesh.new()
			tq.size = Vector2(6.0, 13.0)
			tap.mesh = tq
			var tm2 := StandardMaterial3D.new()
			tm2.albedo_color = tcols[ti % tcols.size()]
			tm2.roughness = 1.0
			tm2.cull_mode = BaseMaterial3D.CULL_DISABLED
			tap.material_override = tm2
			tap.position = o + Vector3(sgn * 34.0, 20.0, -20.0 + float(ti) * 24.0)
			tap.rotation_degrees = Vector3(0, -90.0 * sgn, 0)
			m.add_child(tap)
			m.game_nodes.append(tap)
	# ---------- Phase 4c: a lived-in reading nook (Quaternius furniture, CC0) ----------
	# light touch only — the hall keeps its bespoke throne/stairs/columns. A tall
	# bookcase against the left wall bay and a little tea table with two chairs
	# in the right bay, all pastel-restyled by _kit() so the dark wood reads soft.
	m._kit("furniture/bookcase", o + Vector3(-31.5, 0.1, 2.0), 7.0, PI * 0.5)
	m._wall_solid(o + Vector3(-31.5, 6.0, 2.0), Vector3(2.8, 12.0, 7.4), 0.8)
	m._kit("furniture/table", o + Vector3(29.0, 0.1, 0.0), 8.0, PI * 0.5)
	m._cyl_solid(o + Vector3(29.0, 1.5, 0.0), 3.2, 1.5, 0.6)
	m._kit("furniture/chair", o + Vector3(26.0, 0.1, 3.6), 2.2, PI * 0.75)
	m._kit("furniture/chair", o + Vector3(26.0, 0.1, -3.6), 2.2, PI * 1.25)
	# ---------- her memories framed along the hall walls ----------
	# (Roshan wall-art portraits removed from the Grand Hall — inconsistent with how the games work here)
	# ---------- potted plants flank the throne + entrance ----------
	for pp in [Vector3(-9, 1.0, -22), Vector3(9, 1.0, -22), Vector3(-7, 1.0, 36), Vector3(7, 1.0, 36)]:
		var pot := MeshInstance3D.new()
		var potm := CylinderMesh.new()
		potm.top_radius = 1.6
		potm.bottom_radius = 1.2
		potm.height = 2.4
		pot.mesh = potm
		var ptm := StandardMaterial3D.new()
		ptm.albedo_color = Color(0.7, 0.4, 0.3)
		ptm.roughness = 0.7
		pot.material_override = ptm
		pot.position = o + pp + Vector3(0, 0.5, 0)
		m.add_child(pot)
		m.game_nodes.append(pot)
		m._nature("plant_bushLargeTriangle", o + pp + Vector3(0, 1.6, 0), 3.0, randf() * TAU)
	# ---------- hanging chandeliers (mesh + light) ----------
	for chz in [-12.0, 10.0]:
		var ch := MeshInstance3D.new()
		var cht := TorusMesh.new()
		cht.inner_radius = 2.4
		cht.outer_radius = 3.2
		ch.mesh = cht
		var chm := StandardMaterial3D.new()
		chm.albedo_color = Color(0.95, 0.8, 0.4)
		chm.metallic = 0.8
		chm.roughness = 0.3
		chm.emission_enabled = true
		chm.emission = Color(1.0, 0.8, 0.4)
		chm.emission_energy_multiplier = 0.35
		ch.material_override = chm
		ch.position = o + Vector3(0, 30.0, chz)
		m.add_child(ch)
		m.game_nodes.append(ch)
		var chl := OmniLight3D.new()
		chl.light_color = Color(1.0, 0.85, 0.55)
		chl.light_energy = 1.45
		chl.omni_range = 22.0
		chl.position = o + Vector3(0, 28.0, chz)
		m.add_child(chl)
		m.game_nodes.append(chl)
		m._register_castle_light(chl, true)
	# OPEN back doorways (dark archways) flanking the throne
	for dx in [-22.0, 22.0]:
		m._l2_box(o + Vector3(dx - 5.0, 8, -33.2), Vector3(1.2, 16, 1.2), Color(0.8, 0.7, 0.5), 0.1)  # gold frame posts
		m._l2_box(o + Vector3(dx + 5.0, 8, -33.2), Vector3(1.2, 16, 1.2), Color(0.8, 0.7, 0.5), 0.1)
		m._l2_box(o + Vector3(dx, 15.5, -33.2), Vector3(11, 1.2, 1.2), Color(0.8, 0.7, 0.5), 0.1)
	# ---------- REAL BACK ROOM behind the throne (entered through the two side archways) ----------
	var br := o + Vector3(0, 0, -46.0)   # back-room center
	# flr is SEGMENTED around the undercroft's back-stairwell opening
	# (x -3.4..3.4, z -3.2..1.2 rel br) — sized to hide COMPLETELY under the
	# golden stand. Segments register for camera cutaway fade so the descent
	# stays readable from above once the stand has slid aside.
	var brsegs: Array[MeshInstance3D] = []
	brsegs.append(m._l2_box(br + Vector3(-14.7, 0.4, 0), Vector3(22.6, 1.0, 22), Color(0.86, 0.82, 0.92)))   # left of opening
	brsegs.append(m._l2_box(br + Vector3(14.7, 0.4, 0), Vector3(22.6, 1.0, 22), Color(0.86, 0.82, 0.92)))    # right of opening
	brsegs.append(m._l2_box(br + Vector3(0, 0.4, -7.1), Vector3(6.8, 1.0, 7.8), Color(0.86, 0.82, 0.92)))    # back strip
	brsegs.append(m._l2_box(br + Vector3(0, 0.4, 6.1), Vector3(6.8, 1.0, 9.8), Color(0.86, 0.82, 0.92)))     # front strip
	for fseg in brsegs:
		fseg.material_override = m._castle_mat("floor", 0.035, Color(0.72, 0.68, 0.82))
		m.fade_walls.append({"node": fseg, "c": fseg.position, "h": (fseg.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	m._l2_box(br + Vector3(0, 33.0, 0), Vector3(52, 1.5, 22), Color(0.58, 0.54, 0.66))           # ceiling
	m._iwall(br + Vector3(0, 16, -10.5), Vector3(52, 34, 1.5), Color(0.76, 0.70, 0.84), "castle")          # back wall
	m._iwall(br + Vector3(-25.5, 16, 0), Vector3(1.5, 34, 22), Color(0.72, 0.67, 0.81), "castle")          # left wall
	m._iwall(br + Vector3(25.5, 16, 0), Vector3(1.5, 34, 22), Color(0.72, 0.67, 0.81), "castle")           # right wall
	# warm light + a soft red runner inside
	var brl := OmniLight3D.new(); brl.light_color = Color(1.0, 0.85, 0.6); brl.light_energy = 0.9; brl.omni_range = 26.0
	brl.position = br + Vector3(0, 20, 0); m.add_child(brl); m.game_nodes.append(brl)
	m._register_castle_light(brl, false)
	var back_runner: MeshInstance3D = m._l2_box(br + Vector3(0, 1.0, 6.6), Vector3(10, 0.2, 10.8), Color(0.72, 0.16, 0.22))
	back_runner.material_override = m._castle_mat("carpet", 0.055, Color(0.82, 0.72, 0.78))
	# a glowing royal treasure chest = the bonus trigger. It doubles as the
	# GOLDEN STAND sealing the undercroft's back stairwell: it pulses
	# invitingly and rumbles aside when Roshan gets close (see slide_stand).
	var chest = m._l2_box(br + Vector3(0, 3.0, -1.0), Vector3(7, 5, 4.5), Color(0.76, 0.56, 0.20), 0.12)
	chest.material_override.metallic = 0.6
	var chest_lid = m._l2_box(br + Vector3(0, 6.0, -1.0), Vector3(7.4, 1.4, 5.0), Color(0.68, 0.47, 0.17), 0.08)   # lid rim
	m.g["secret_door"] = chest.position
	m.g["stand_chest"] = chest
	m.g["stand_lid"] = chest_lid
	m.g["stand_open"] = false
	m.g["stand_armed"] = false   # arms once Roshan is >14 away (the moat hatch spawns right beside it)
	var ctw: Tween = chest.create_tween().set_loops()
	ctw.tween_property(chest.material_override, "emission_energy_multiplier", 0.32, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	ctw.tween_property(chest.material_override, "emission_energy_multiplier", 0.10, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	var sl2 := OmniLight3D.new(); sl2.light_color = Color(0.6, 0.95, 1.0); sl2.light_energy = 0.75; sl2.omni_range = 11.0
	sl2.position = chest.position + Vector3(0, 4, 0); m.add_child(sl2); m.game_nodes.append(sl2)
	m._register_castle_light(sl2, true)
	# Daddy mermaid lives in the secret room (his real recorded voice greets Roshan)
	var daddy := Sprite3D.new()
	daddy.texture = m._cutout_tex("daddy")
	daddy.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	daddy.pixel_size = 0.0066
	daddy.position = br + Vector3(10, 8, -3)
	m.add_child(daddy); m.game_nodes.append(daddy)
	var dlt := OmniLight3D.new(); dlt.light_color = Color(1.0, 0.9, 0.8); dlt.light_energy = 0.9; dlt.omni_range = 18.0
	dlt.position = daddy.position + Vector3(0, 2, 5); m.add_child(dlt); m.game_nodes.append(dlt)
	m._register_castle_light(dlt, false)
	var sl := OmniLight3D.new()
	sl.light_color = Color(0.5, 0.9, 1.0)
	sl.light_energy = 1.5
	sl.omni_range = 14.0
	sl.position = o + Vector3(-22, 7, -33.0)   # invite glow at the left archway
	m.add_child(sl)
	m.game_nodes.append(sl)
	m._register_castle_light(sl, false)
	var sl3 := OmniLight3D.new()
	sl3.light_color = Color(0.5, 0.9, 1.0)
	sl3.light_energy = 1.5
	sl3.omni_range = 14.0
	sl3.position = o + Vector3(22, 7, -33.0)   # invite glow at the right archway
	m.add_child(sl3)
	m.game_nodes.append(sl3)
	m._register_castle_light(sl3, false)
	var slab := Label3D.new()
	slab.text = "\u2726"
	slab.font_size = 140
	slab.pixel_size = 0.02
	slab.outline_size = 16
	slab.modulate = Color(1.0, 0.82, 0.28)
	slab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	slab.position = m.g["secret_door"] + Vector3(0, 7.0, 0)
	m.add_child(slab)
	m.game_nodes.append(slab)
	m.g["stand_label"] = slab
	# (the royal loo lives down in the basement wing — see build_basement_wing)
	# just TWO framed memories on the side walls (fewer pictures)
	# (the swim-through xylophone now lives in the dedicated MUSIC ROOM off the left wall \u2014 see _build_castle_music_room)
	# (the crafting easel now lives in its own dedicated CRAFT ROOM down in the
	# basement wing — see build_basement_wing; the hall keeps the reading nook)
	# The Crown Star is authored landmark geometry rather than a font glyph.
	# The audited chandelier pair above remains the hall's only overhead lights.
	var crown: Node3D = LandmarkArtFactory.create_star(5.2, Color(1.0, 0.76, 0.24), true)
	crown.position = o + Vector3(0, 24.0, -28.0)
	crown.set_meta("base_y", crown.position.y)
	m.add_child(crown)
	m.game_nodes.append(crown)
	# On later visits the Crown Star remains as a royal keepsake, but it cannot
	# replay the ownership win or pull Roshan toward an already-completed goal.
	if m.level2_done_once:
		m.g["crown_won"] = true
	m.l2_stars = [{"node": crown, "got": m.level2_done_once}]
	# A short, non-reading sparkle trail connects the runner and stairs to the
	# crown. It is visual guidance only; the existing objective and collision
	# contracts remain unchanged.
	var crown_guides: Array[Label3D] = []
	for guide_i in range(3):
		var guide := Label3D.new()
		guide.text = "\u2726"
		guide.font_size = 150
		guide.pixel_size = 0.018
		guide.outline_size = 18
		guide.modulate = Color(1.0, 0.80, 0.28, 0.82)
		guide.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		guide.position = o + Vector3(0, 5.0 + float(guide_i) * 4.6, -11.0 - float(guide_i) * 5.2)
		guide.visible = not m.level2_done_once
		m.add_child(guide)
		m.game_nodes.append(guide)
		crown_guides.append(guide)
	m.g["crown_guides"] = crown_guides
	# EXIT door at the entrance — swim into it to go back to the ocean
	var exit := MeshInstance3D.new()
	var et := TorusMesh.new()
	et.inner_radius = 3.4
	et.outer_radius = 4.6
	exit.mesh = et
	exit.material_override = m._rainbow_mat()
	exit.position = o + Vector3(0, 5.0, 44.0)
	m.add_child(exit)
	m.game_nodes.append(exit)
	var exl := OmniLight3D.new()
	exl.light_color = Color(0.6, 0.9, 1.0)
	exl.light_energy = 2.0
	exl.omni_range = 18.0
	exl.position = exit.position
	m.add_child(exl)
	m.game_nodes.append(exl)
	m._register_castle_light(exl, true)
	var exlab := Label3D.new()
	exlab.text = "\u2190"
	exlab.font_size = 120
	exlab.pixel_size = 0.03
	exlab.outline_size = 12
	exlab.modulate = Color(0.7, 0.95, 1.0)
	exlab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	exlab.position = exit.position + Vector3(0, 6.5, 0)
	m.add_child(exlab)
	m.game_nodes.append(exlab)
	m.g["hall_exit"] = exit.position
	# (no ocean ring here — reaching Princess Huluu / the Crown Star at the throne is the link back to the ocean)
	# a cosy royal bedroom opens off the right-hand wall (doorway at z=-16)
	build_bedroom(o)
	# ...and a music room opens off the left-hand wall (doorway at z=-16)
	build_music_room(o)


func build_expansion(o: Vector3) -> void:
	# ============ THE GRAND CASTLE (owner 2026-07-11) ============
	# A balcony off the throne, a gallery doorway into two TOP CHAMBERS above
	# the treasure room, and an UNDERCROFT below the hall that connects to
	# the room where Roshan meets Daddy. Stories work through y-banded player
	# zones (m.arena_zones): a floor only exists for someone in its band, so
	# the balcony never blocks the throne beneath it.
	var wcol := Color(0.95, 0.92, 0.97)
	var gold := Color(0.95, 0.8, 0.35)
	# ---------- balcony deck along the raised back wall, above the throne
	var deck = m._l2_box(o + Vector3(0, 32.4, -27.0), Vector3(52, 1.2, 12), wcol)
	deck.material_override = m._castle_mat("floor", 0.035, Color(0.88, 0.84, 0.94))
	for px in range(-6, 7):
		m._l2_box(o + Vector3(float(px) * 4.0, 34.6, -21.4), Vector3(0.5, 3.2, 0.5), gold, 0.2)
	m._l2_box(o + Vector3(0, 36.4, -21.4), Vector3(52, 0.5, 0.6), gold, 0.25)
	# twin stone stairs hugging the side walls up to the deck. STEEP flights
	# along the doorless back stretch (z -21..-33) — the old shallow run
	# crossed the music/bedroom doorways at z -16, and its ramp + under-stair
	# mass sealed them shut (probe_upstairs caught it). Treads are a ramp-floor
	# zone; a stepped under-stair mass blocks swimming in underneath.
	for sgn in [-1.0, 1.0]:
		for i in range(10):
			m._l2_box(o + Vector3(sgn * 30.5, 3.0 + float(i) * 3.0, -21.9 - float(i) * 1.13), Vector3(7.0, 0.9, 2.4), Color(0.93, 0.9, 0.95))
		m._wall_solid(o + Vector3(sgn * 30.5, 5.8, -28.0), Vector3(7, 13.8, 4.0), 0.4)
		m._wall_solid(o + Vector3(sgn * 30.5, 11.4, -31.75), Vector3(7, 25.0, 3.5), 0.4)
	# ---------- THE UPPER STORY (owner 2026-07-12): wraps around BOTH wings.
	# A full-width back block (z -36..-64, x -53..53) holds the enlarged Star
	# Chamber + Cloud Lounge; two long WING GALLERIES run above the music room
	# (left) and the bedroom/craft wing (right), z -36..18 — so upstairs rooms
	# extend on all three sides. Reached from the balcony gallery door OR by
	# swimming through the new hall arcade arches.
	var uf = m._l2_box(o + Vector3(0, 33.0, -50.0), Vector3(106, 1.2, 28), Color(0.9, 0.86, 0.94))
	uf.material_override = m._castle_mat("floor", 0.035, Color(0.84, 0.80, 0.94))
	for wsgn in [-1.0, 1.0]:
		var wf = m._l2_box(o + Vector3(wsgn * 44.25, 33.0, -9.0), Vector3(17.5, 1.2, 54), Color(0.9, 0.86, 0.94))
		wf.material_override = m._castle_mat("floor", 0.035, Color(0.84, 0.80, 0.94))
	m._iwall(o + Vector3(0, 41, -64), Vector3(106, 16, 1.5), wcol, "castle")      # far wall, full width
	m._iwall(o + Vector3(-53.5, 41, -22.6), Vector3(1.5, 16, 83), wcol, "castle") # left outer wall (z -64..18.75)
	m._iwall(o + Vector3(53.5, 41, -22.6), Vector3(1.5, 16, 83), wcol, "castle")  # right outer wall
	m._iwall(o + Vector3(-44.25, 41, 18.75), Vector3(18.5, 16, 1.5), wcol, "castle")  # left wing front wall
	m._iwall(o + Vector3(44.25, 41, 18.75), Vector3(18.5, 16, 1.5), wcol, "castle")   # right wing front wall
	m._iwall(o + Vector3(0, 41, -39.5), Vector3(1.5, 16, 7), wcol, "castle")    # divider, front seg
	m._iwall(o + Vector3(0, 41, -58.5), Vector3(1.5, 16, 11), wcol, "castle")   # divider, back seg (door z -43..-53)
	# back-block ceiling, SEGMENTED around the Dreaming Floor stairwell opening
	# (x -9..-3, z -44..-38). The flight lives ENTIRELY in the Star Chamber,
	# west of the x-0 divider wall: the first cut ran the stairs straight
	# through the divider's collider, which walled the top of the flight off
	# in both directions and trapped Roshan on the top floor. The opening also
	# ends AT the stair top — a wider hole left a strip the stair ramp zone
	# did not govern, an invisible floor she could stand on but not sink through.
	m._l2_box(o + Vector3(-31, 49, -50), Vector3(44, 1.2, 28), Color(0.84, 0.8, 0.9))
	m._l2_box(o + Vector3(25, 49, -50), Vector3(56, 1.2, 28), Color(0.84, 0.8, 0.9))
	m._l2_box(o + Vector3(-6, 49, -54), Vector3(6, 1.2, 20), Color(0.84, 0.8, 0.9))
	m._l2_box(o + Vector3(-6, 49, -37), Vector3(6, 1.2, 2), Color(0.84, 0.8, 0.9))
	for csgn in [-1.0, 1.0]:
		m._l2_box(o + Vector3(csgn * 44.25, 49, -9.0), Vector3(18.5, 1.2, 54), Color(0.84, 0.8, 0.9))  # wing ceilings
	# soft window glows down the outer walls (emissive only — light budget stays)
	for wz in [-22.0, -4.0, 12.0]:
		for wsgn2 in [-1.0, 1.0]:
			var win = m._l2_box(o + Vector3(wsgn2 * 53.2, 42, wz), Vector3(0.4, 6, 5), Color(0.75, 0.85, 1.0), 0.9)
			win.material_override.emission_energy_multiplier = 1.2
	for wx in [-40.0, -20.0, 20.0, 40.0]:
		var win2 = m._l2_box(o + Vector3(wx, 42, -63.8), Vector3(5, 6, 0.4), Color(0.75, 0.85, 1.0), 0.9)
		win2.material_override.emission_energy_multiplier = 1.2
	# STAR CHAMBER (left, now ~52 wide): her observatory
	m._l2_box(o + Vector3(-26, 33.9, -50), Vector3(42, 0.3, 20), Color(0.2, 0.2, 0.42))   # midnight rug
	var scope = m._l2_box(o + Vector3(-24, 36.2, -55), Vector3(1.6, 1.6, 7.0), gold, 0.25)
	scope.rotation_degrees = Vector3(-30, 20, 0)
	m._l2_box(o + Vector3(-24, 34.2, -55), Vector3(2.6, 1.4, 2.6), Color(0.5, 0.4, 0.3))
	for st in range(14):
		var star: Node3D = LandmarkArtFactory.create_star(0.7 + float(st % 3) * 0.18, [Color(1.0, 0.76, 0.3), Color(0.45, 0.86, 0.82), Color(0.74, 0.58, 0.94)][st % 3], false, true)
		star.position = o + Vector3(-30.0 + float(st % 7) * 4.3, 42.0 + float(st % 4) * 1.6, -60.5 + float(st / 7) * 2.0)
		m.add_child(star)
		m.game_nodes.append(star)
	# CLOUD LOUNGE (right): pillow pile + her memory portraits
	for ci in range(6):
		var cc := Color(1.0, 0.75, 0.85) if ci % 2 == 0 else Color(0.75, 0.85, 1.0)
		m._l2_box(o + Vector3(12.0 + float(ci % 3) * 6.5, 34.2 + float(ci / 3) * 1.3, -52.0 + float(ci % 2) * 4.0), Vector3(5.0, 1.6, 5.0), cc)
	m._hang_portrait(o + Vector3(52.4, 41.0, -46.0), Vector3(0, -90, 0), "p_seattle")
	m._hang_portrait(o + Vector3(52.4, 41.0, -54.0), Vector3(0, -90, 0), "p_garden")
	m._l2_box(o + Vector3(26, 33.9, -50), Vector3(42, 0.3, 20), Color(0.85, 0.7, 0.9))    # lounge rug (fills the wider chamber)
	# gallery lamps (back block + one down each wing)
	for lx in [-14.0, 14.0]:
		m._l2_box(o + Vector3(lx, 46.0, -50.0), Vector3(1.2, 1.2, 1.2), Color(1.0, 0.9, 0.6), 3.0)
	for lsgn in [-1.0, 1.0]:
		for lz in [-20.0, 4.0]:
			m._l2_box(o + Vector3(lsgn * 44.25, 46.0, lz), Vector3(1.2, 1.2, 1.2), Color(1.0, 0.9, 0.6), 3.0)
	# ---------- LEFT WING GALLERY: the ROYAL LIBRARY ----------
	var shelf_cols := [Color(0.85, 0.3, 0.3), Color(0.3, 0.55, 0.85), Color(0.95, 0.8, 0.35), Color(0.45, 0.75, 0.45), Color(0.7, 0.45, 0.85)]
	for sh in range(4):
		var shz: float = -28.0 + float(sh) * 12.0
		m._l2_box(o + Vector3(-51.8, 38.0, shz), Vector3(1.4, 10.0, 9.0), Color(0.5, 0.34, 0.22))     # bookcase
		for row in range(3):
			m._l2_box(o + Vector3(-51.0, 34.6 + float(row) * 3.0, shz), Vector3(0.8, 1.8, 8.0), shelf_cols[(sh + row) % shelf_cols.size()], 0.12)
	m._l2_box(o + Vector3(-44, 33.9, 2.0), Vector3(12, 0.3, 22), Color(0.55, 0.4, 0.65))              # reading rug
	m._l2_box(o + Vector3(-44, 34.8, 9.0), Vector3(4.5, 1.6, 4.5), Color(0.95, 0.85, 0.6))            # story cushion
	var lsign := Label3D.new()
	lsign.text = "📚 Royal Library"
	lsign.font_size = 52
	lsign.pixel_size = 0.028
	lsign.outline_size = 12
	lsign.modulate = Color(0.9, 0.85, 1.0)
	lsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lsign.position = o + Vector3(-44, 45.5, 12)
	m.add_child(lsign)
	m.game_nodes.append(lsign)
	# ---------- RIGHT WING GALLERY: the TOY ROOM ----------
	var block_cols := [Color(0.9, 0.4, 0.4), Color(0.4, 0.6, 0.9), Color(0.95, 0.8, 0.3), Color(0.5, 0.8, 0.5)]
	for bi in range(4):
		m._l2_box(o + Vector3(48.5 - float(bi % 2) * 3.4, 34.9 + float(bi / 2) * 3.4, -24.0 + float(bi % 2) * 1.5), Vector3(3.0, 3.0, 3.0), block_cols[bi], 0.15)
	var tchest = m._l2_box(o + Vector3(49.5, 34.9, -4.0), Vector3(5.5, 3.4, 4.0), Color(0.62, 0.42, 0.26))
	tchest.material_override.roughness = 0.8
	m._l2_box(o + Vector3(49.5, 36.9, -4.0), Vector3(5.9, 1.0, 4.4), Color(0.95, 0.8, 0.35), 0.3)     # gold chest lid
	m._l2_box(o + Vector3(44, 33.9, 2.0), Vector3(12, 0.3, 22), Color(0.95, 0.75, 0.8))               # play rug
	for hb in range(3):
		m._l2_box(o + Vector3(41.0, 34.4, 8.0 + float(hb) * 3.2), Vector3(2.4, 0.9, 2.4), Color(1.0, 0.9, 0.55), 0.4)  # hopscotch pads
	var tsign := Label3D.new()
	tsign.text = "🧸 Toy Room"
	tsign.font_size = 52
	tsign.pixel_size = 0.028
	tsign.outline_size = 12
	tsign.modulate = Color(1.0, 0.9, 0.85)
	tsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tsign.position = o + Vector3(44, 45.5, 12)
	m.add_child(tsign)
	m.game_nodes.append(tsign)
	# ---------- THE DREAMING FLOOR: five legacy bedrooms over the back block
	build_dreaming_floor(o)
	# ---------- the UNDERCROFT: stone basement under the front hall
	var shaft := Vector3(-24, 0, 30)
	for e in [Vector3(-5.5, 0, 0), Vector3(5.5, 0, 0)]:
		m._l2_box(o + shaft + e + Vector3(0, 0.9, 0), Vector3(0.9, 0.5, 11), gold, 0.3)
	for e2 in [Vector3(0, 0, -5.5), Vector3(0, 0, 5.5)]:
		m._l2_box(o + shaft + e2 + Vector3(0, 0.9, 0), Vector3(11, 0.5, 0.9), gold, 0.3)
	for i in range(8):
		m._l2_box(o + shaft + Vector3(0, -1.5 - float(i) * 2.1, -3.5 + float(i) * 1.0), Vector3(8.0, 0.8, 2.6), Color(0.62, 0.58, 0.66))
	var bf = m._l2_box(o + Vector3(0, -18.6, 24.0), Vector3(60, 1.2, 32), Color(0.6, 0.56, 0.64))
	bf.material_override = m._castle_mat("cobble", 0.05, Color(0.75, 0.70, 0.80))
	m._iwall(o + Vector3(0, -9.5, 40), Vector3(60, 18, 1.5), Color(0.7, 0.66, 0.74), "castle")
	# front wall SEGMENTED: the basement hallway opens through it at x -8..8
	# (this wall used to seal the corridor off from the undercroft entirely)
	m._iwall(o + Vector3(-19, -9.5, 8), Vector3(22, 18, 1.5), Color(0.7, 0.66, 0.74), "castle")
	m._iwall(o + Vector3(19, -9.5, 8), Vector3(22, 18, 1.5), Color(0.7, 0.66, 0.74), "castle")
	for hp in [-8.0, 8.0]:
		m._l2_box(o + Vector3(hp, -10.0, 8.0), Vector3(1.2, 16, 1.2), gold, 0.2)   # gold posts frame the hallway mouth
	m._iwall(o + Vector3(-30, -9.5, 24), Vector3(1.5, 18, 32), Color(0.7, 0.66, 0.74), "castle")
	m._iwall(o + Vector3(30, -9.5, 24), Vector3(1.5, 18, 32), Color(0.7, 0.66, 0.74), "castle")
	for px2 in [-15.0, 0.0, 15.0]:
		m._l2_box(o + Vector3(px2, -9.5, 24.0), Vector3(3.0, 18, 3.0), Color(0.65, 0.6, 0.7))
	# cosy clutter: barrels, crates, a treasure glint, warm lanterns (emissive
	# only - the OmniLight budget stays untouched)
	for bi in range(5):
		m._l2_box(o + Vector3(-24.0 + float(bi) * 4.5, -16.8, 36.0), Vector3(3.0, 3.6, 3.0), Color(0.55, 0.4, 0.26))
	for cr in range(3):
		m._l2_box(o + Vector3(20.0 + float(cr) * 4.0, -17.0, 12.0 + float(cr) * 2.0), Vector3(3.4, 3.0, 3.4), Color(0.66, 0.5, 0.32))
	for li in range(4):
		m._l2_box(o + Vector3(-26.0 + float(li) * 17.0, -12.0, 39.2), Vector3(1.0, 1.4, 0.6), Color(1.0, 0.8, 0.45), 3.2)
	# ---------- the BASEMENT WING: wide hallway, side rooms, the royal loo
	build_basement_wing(o)
	# stair back up into Daddy's room — recentered directly under the golden
	# stand, which seals the opening until Roshan gets close (see slide_stand);
	# the gold rim hugs the stand's footprint like a plinth ring
	for i2 in range(8):
		m._l2_box(o + Vector3(0, -1.5 - float(i2) * 2.1, -47.5 + float(i2) * 1.0), Vector3(6.8, 0.8, 2.6), Color(0.62, 0.58, 0.66))
	for e3 in [Vector3(-3.9, 0, 0), Vector3(3.9, 0, 0)]:
		m._l2_box(o + Vector3(0, 0.9, -47.0) + e3, Vector3(0.9, 0.5, 5.3), gold, 0.3)
	for e4 in [Vector3(0, 0, -2.7), Vector3(0, 0, 2.7)]:
		m._l2_box(o + Vector3(0, 0.9, -47.0) + e4, Vector3(8.7, 0.5, 0.9), gold, 0.3)
	# ---------- the y-banded zones that make the stories real
	m.arena_zones = [
		{"rect": Rect2(-35, -70, 70, 116), "band": Vector2(-0.5, 60.0), "ceil": 50.0},
		{"rect": Rect2(-26, -33, 52, 12), "band": Vector2(30.0, 50.0), "floor": 33.4},
		{"rect": Rect2(-53, -64, 106, 28), "band": Vector2(30.0, 50.0), "floor": 34.2, "ceil": 48.0},
		{"rect": Rect2(-53, -36, 18, 55), "band": Vector2(30.0, 50.0), "floor": 34.2, "ceil": 48.0},
		{"rect": Rect2(35, -36, 18, 55), "band": Vector2(30.0, 50.0), "floor": 34.2, "ceil": 48.0},
		{"rect": Rect2(-30, 8, 60, 32), "band": Vector2(-18.0, -1.0), "floor": -17.4, "ceil": -2.0},
		{"rect": Rect2(-8, -44, 16, 52), "band": Vector2(-18.0, -1.0), "floor": -17.4, "ceil": -2.0},
		{"rect": Rect2(-26, -10, 52, 16), "band": Vector2(-18.0, -1.0), "floor": -17.4, "ceil": -2.0},
		{"rect": Rect2(-26, -36, 52, 16), "band": Vector2(-18.0, -1.0), "floor": -17.4, "ceil": -2.0},
		{"rect": Rect2(-29, 25, 10, 10), "band": Vector2(-18.0, 3.5), "floor": -17.4, "ramp": [2, 26.5, -0.7, 33.5, -15.4]},
		# staircase RAMP floors (stairs pass 2026-07-12) — every castle flight is
		# walkable, not swim-through decor. Royal-stairs band stops below the
		# balcony deck band (30..50) or it would re-floor the deck airspace.
		{"rect": Rect2(-8, -24.7, 16, 16.2), "band": Vector2(-0.5, 29.5), "ramp": [2, -10.0, 2.9, -23.2, 14.9]},   # royal stairs to the throne
		{"rect": Rect2(26.5, -34.0, 7.5, 13.5), "band": Vector2(-0.5, 32.0), "ramp": [2, -21.9, 3.85, -32.1, 30.85]},   # balcony stairs, right
		{"rect": Rect2(-34.0, -34.0, 7.5, 13.5), "band": Vector2(-0.5, 32.0), "ramp": [2, -21.9, 3.85, -32.1, 30.85]},  # balcony stairs, left
		{"rect": Rect2(-34.5, -33.5, 9, 11), "band": Vector2(-18.0, -1.0), "floor": -17.4, "ceil": -2.0},   # hidden privy behind the Bubble Bath
		# the DREAMING FLOOR (3rd story). Its band starts ABOVE the back-block
		# ceil (48) so the two can never both claim the y 48..50 airspace, and
		# the stair zone comes AFTER it so the ramp wins inside the stairwell.
		{"rect": Rect2(-53, -64, 106, 28), "band": Vector2(49.8, 66.0), "floor": 50.6, "ceil": 63.5},
		{"rect": Rect2(-20, -44, 17, 6), "band": Vector2(33.0, 53.0), "ramp": [0, -20.0, 34.6, -4.0, 50.2], "ceil": 52.5},   # dreaming stairs (rect spans the WHOLE opening, x -20..-3)
		{"rect": Rect2(-6, -50, 12, 12), "band": Vector2(-18.0, -2.0), "ramp": [2, -47.5, -3.4, -40.5, -15.4], "ceil": -2.8},
	]
	# The back stairwell starts SEALED under the golden stand: its band stops
	# below the hallway floor (nobody sinks in from above or pops up from
	# below) until slide_stand() opens the band up to the hallway. The seal's
	# ceil sits 0.8 BELOW the band top: at the band edge itself a fast upward
	# swim could cross the whole band in one frame and tunnel out.
	m.g["stand_zone"] = m.arena_zones[m.arena_zones.size() - 1]

func build_dreaming_floor(o: Vector3) -> void:
	# ============ THE DREAMING FLOOR (owner 2026-07-12) ============
	# Third story over the back block: five little bedrooms, one for each part
	# of the Mermaid Roshan legacy — Princess Huluu, Daddy Mermaid, Mama & Baby,
	# Kareem and Gabby — plus a basket for Wacky & Chuck at the corridor's end.
	# Reached up a marble flight from the Star Chamber (ramp zone through the
	# opening cut in the y-49 ceiling). Emissive lamps only — light budget safe.
	var wcol := Color(0.95, 0.92, 0.97)
	var gold := Color(0.95, 0.8, 0.35)
	# ---------- the flight up from the Star Chamber + its under-stair mass
	# (x -20..-4: clear of the x-0 chamber divider and its collider pad)
	for i in range(8):
		m._l2_box(o + Vector3(-19.0 + 2.0 * float(i), 35.1 + 1.95 * float(i), -41.0), Vector3(2.1, 0.9, 5.0), Color(0.93, 0.9, 0.95))
	m._wall_solid(o + Vector3(-11.0, 36.5, -41.0), Vector3(5.4, 5.4, 6.0), 0.4)
	m._wall_solid(o + Vector3(-5.75, 39.7, -41.0), Vector3(4.5, 11.2, 6.0), 0.4)
	# gold rim around the stairwell opening upstairs
	for rx in [-9.4, -2.6]:
		m._l2_box(o + Vector3(rx, 50.1, -41.0), Vector3(0.8, 0.5, 7.0), gold, 0.3)
	for rz in [-44.4, -37.6]:
		m._l2_box(o + Vector3(-6.0, 50.1, rz), Vector3(7.6, 0.5, 0.8), gold, 0.3)
	# ---------- shell: perimeter walls + roof (the floor is the y-49 slab)
	m._iwall(o + Vector3(0, 57, -64), Vector3(106, 15, 1.5), wcol, "castle")       # back wall
	m._iwall(o + Vector3(0, 57, -36), Vector3(106, 15, 1.5), wcol, "castle")       # front wall
	m._iwall(o + Vector3(-53.5, 57, -50), Vector3(1.5, 15, 28), wcol, "castle")    # west end
	m._iwall(o + Vector3(53.5, 57, -50), Vector3(1.5, 15, 28), wcol, "castle")     # east end
	m._l2_box(o + Vector3(0, 65, -50), Vector3(108, 1.2, 30), Color(0.82, 0.79, 0.88))   # roof
	# ---------- five bedrooms across the back (z -63..-52), corridor in front
	m._iwall(o + Vector3(-45, 57, -57.5), Vector3(1.5, 15, 11), wcol, "castle")    # west end of the room row
	m._iwall(o + Vector3(45, 57, -57.5), Vector3(1.5, 15, 11), wcol, "castle")     # east end
	for px in [-27.0, -9.0, 9.0, 27.0]:
		m._iwall(o + Vector3(px, 57, -57.5), Vector3(1.5, 15, 11), wcol, "castle")   # partitions
	var bedrooms := [
		{"cx": -36.0, "name": "✨ Princess Huluu ✨", "tex": "huluu", "col": Color(1.0, 0.72, 0.85), "keep": "crown"},
		{"cx": -18.0, "name": "✨ Daddy Mermaid ✨", "tex": "daddy", "col": Color(0.45, 0.75, 0.95), "keep": "chest"},
		{"cx": 0.0, "name": "✨ Mama & Baby ✨", "tex": "mama_baby", "col": Color(0.82, 0.68, 0.95), "keep": "cradle"},
		{"cx": 18.0, "name": "✨ Kareem ✨", "tex": "kareem", "col": Color(0.55, 0.85, 0.62), "keep": "star"},
		{"cx": 36.0, "name": "✨ Gabby ✨", "tex": "gabby", "col": Color(1.0, 0.66, 0.5), "keep": "note"},
	]
	for rd in bedrooms:
		var cx: float = rd["cx"]
		var bcol: Color = rd["col"]
		# front wall with a doorway + gold posts
		m._iwall(o + Vector3(cx - 6.5, 57, -52), Vector3(5, 15, 1.5), wcol, "castle")
		m._iwall(o + Vector3(cx + 6.5, 57, -52), Vector3(5, 15, 1.5), wcol, "castle")
		for gp in [-4.0, 4.0]:
			m._l2_box(o + Vector3(cx + gp, 53.5, -52), Vector3(0.9, 7.5, 0.9), gold, 0.2)
		# rug + bed (frame, mattress, pillow, character-colored blanket)
		m._l2_box(o + Vector3(cx - 4.0, 49.85, -55.5), Vector3(6, 0.25, 5), bcol.lightened(0.35))
		m._l2_box(o + Vector3(cx + 3.0, 50.5, -59.5), Vector3(5.5, 1.8, 7), Color(0.5, 0.34, 0.22))     # frame
		m._l2_box(o + Vector3(cx + 3.0, 51.6, -59.5), Vector3(4.8, 1.0, 6.4), Color(0.98, 0.97, 1.0))   # mattress
		m._l2_box(o + Vector3(cx + 3.0, 52.3, -61.8), Vector3(3.8, 0.7, 1.8), Color(1.0, 1.0, 1.0))     # pillow
		m._l2_box(o + Vector3(cx + 3.0, 52.2, -57.8), Vector3(5.0, 0.5, 3.6), bcol)                     # blanket
		m._l2_box(o + Vector3(cx + 3.0, 51.9, -62.9), Vector3(5.5, 3.2, 0.8), Color(0.45, 0.28, 0.17))  # headboard
		m._wall_solid(o + Vector3(cx + 3.0, 50.8, -59.5), Vector3(5.5, 2.4, 7), 0.4)
		# glowing bedside lamp (emissive — no light-budget cost) + their window
		m._l2_box(o + Vector3(cx - 2.0, 51.2, -61.5), Vector3(1.6, 3.2, 1.6), Color(0.5, 0.34, 0.22))
		m._l2_box(o + Vector3(cx - 2.0, 53.3, -61.5), Vector3(1.1, 1.1, 1.1), Color(1.0, 0.85, 0.55), 3.0)
		var win = m._l2_box(o + Vector3(cx, 57.5, -63.2), Vector3(4.5, 4.5, 0.4), Color(0.75, 0.85, 1.0), 0.9)
		win.material_override.emission_energy_multiplier = 1.2
		# the character themselves, home at last
		var spr := Sprite3D.new()
		spr.texture = m._cutout_tex(rd["tex"])
		spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		spr.pixel_size = 0.0052
		spr.position = o + Vector3(cx - 4.0, 53.6, -58.5)
		m.add_child(spr); m.game_nodes.append(spr)
		# name plate over the door
		var nsign := Label3D.new()
		nsign.text = rd["name"]
		nsign.font_size = 40; nsign.pixel_size = 0.02; nsign.outline_size = 10
		nsign.modulate = Color(1.0, 0.95, 0.85)
		nsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		nsign.position = o + Vector3(cx, 56.5, -51)
		m.add_child(nsign); m.game_nodes.append(nsign)
		# a keepsake that tells THEIR part of the story
		match String(rd["keep"]):
			"crown":   # Huluu's little tiara on the rug
				for ci in range(3):
					m._l2_box(o + Vector3(cx - 5.5 + float(ci) * 1.1, 50.4 + (0.5 if ci == 1 else 0.0), -55.0), Vector3(0.8, 1.0 + (0.5 if ci == 1 else 0.0), 0.8), gold, 0.8)
			"chest":   # Daddy's mini treasure chest
				var kchest = m._l2_box(o + Vector3(cx - 5.0, 50.6, -55.0), Vector3(2.6, 2.0, 1.8), gold, 0.5)
				kchest.material_override.metallic = 0.6
			"cradle":  # the baby's cradle beside Mama's bed
				m._l2_box(o + Vector3(cx - 5.0, 50.7, -55.0), Vector3(2.4, 1.6, 3.4), Color(0.98, 0.97, 1.0))
				m._l2_box(o + Vector3(cx - 5.0, 51.4, -55.0), Vector3(2.0, 0.4, 3.0), Color(1.0, 0.75, 0.85), 0.3)
			"star":    # Kareem's wishing star
				var kstar := Label3D.new()
				kstar.text = "✦"
				kstar.font_size = 140
				kstar.modulate = Color(1.0, 0.9, 0.4)
				kstar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
				kstar.position = o + Vector3(cx - 5.0, 52.4, -55.0)
				m.add_child(kstar); m.game_nodes.append(kstar)
			"note":    # Gabby's song
				var knote := Label3D.new()
				knote.text = "♪"
				knote.font_size = 150
				knote.modulate = Color(1.0, 0.8, 0.5)
				knote.billboard = BaseMaterial3D.BILLBOARD_ENABLED
				knote.position = o + Vector3(cx - 5.0, 52.4, -55.0)
				m.add_child(knote); m.game_nodes.append(knote)
	# Wacky & Chuck curl up in a basket at the corridor's end
	var wb: Vector3 = o + Vector3(48.0, 0, -44.0)
	m._l2_box(wb + Vector3(0, 50.2, 0), Vector3(4.4, 1.2, 4.4), Color(0.72, 0.52, 0.3))
	m._l2_box(wb + Vector3(0, 50.8, 0), Vector3(3.4, 0.6, 3.4), Color(1.0, 0.8, 0.9))
	var wspr := Sprite3D.new()
	wspr.texture = m._cutout_tex("wacky_chuck")
	wspr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	wspr.pixel_size = 0.0048
	wspr.position = wb + Vector3(0, 53.0, -1.0)
	m.add_child(wspr); m.game_nodes.append(wspr)
	var wsign := Label3D.new()
	wsign.text = "✨ Wacky & Chuck ✨"
	wsign.font_size = 36; wsign.pixel_size = 0.018; wsign.outline_size = 9
	wsign.modulate = Color(0.9, 0.95, 1.0)
	wsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	wsign.position = wb + Vector3(0, 56.0, 0)
	m.add_child(wsign); m.game_nodes.append(wsign)
	# floor sign at the stair top + soft star lamps down the corridor
	var fsign := Label3D.new()
	fsign.text = "✨ The Dreaming Floor ✨"
	fsign.font_size = 48; fsign.pixel_size = 0.024; fsign.outline_size = 12
	fsign.modulate = Color(0.85, 0.88, 1.0)
	fsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	fsign.position = o + Vector3(-6, 56.5, -40)
	m.add_child(fsign); m.game_nodes.append(fsign)
	for lx in [-30.0, 0.0, 30.0]:
		m._l2_box(o + Vector3(lx, 62.5, -44.0), Vector3(1.2, 1.2, 1.2), Color(1.0, 0.9, 0.6), 3.0)


func build_basement_wing(o: Vector3) -> void:
	# ============ THE BASEMENT WING (owner 2026-07-12) ============
	# The old 12-wide corridor grows into a proper basement: a 16-wide hallway
	# running from the undercroft (z +8) to the golden-stand stairs (z -44),
	# two pairs of REAL rooms (pantry / royal kitchen / bubble bath / craft
	# room) and the royal loo HIDDEN in a secret privy behind the Bubble Bath,
	# deep in the basement's far corner — not parked out in the open.
	# Emissive dressing only — the OmniLight budget stays untouched. Vertical
	# physics comes from the basement zone rects in build_expansion.
	var stone := Color(0.7, 0.66, 0.74)
	var gold := Color(0.95, 0.8, 0.35)
	# ---------- the hallway floor
	var cfl = m._l2_box(o + Vector3(0, -18.6, -18.0), Vector3(16, 1.2, 52), Color(0.6, 0.56, 0.64))
	cfl.material_override = m._castle_mat("cobble", 0.05, Color(0.75, 0.70, 0.80))
	# hallway walls, SEGMENTED for the side-room doorways
	# (row 1 doors z -8..2, row 2 doors z -34..-24, both sides)
	for sx in [-1.0, 1.0]:
		m._iwall(o + Vector3(sx * 8.0, -9.5, -39.0), Vector3(1.5, 18, 10), stone, "castle")   # z -44..-34
		m._iwall(o + Vector3(sx * 8.0, -9.5, -16.0), Vector3(1.5, 18, 16), stone, "castle")   # z -24..-8
		m._iwall(o + Vector3(sx * 8.0, -9.5, 5.0), Vector3(1.5, 18, 6), stone, "castle")      # z  +2..+8
	# gold posts frame every doorway
	for dp in [Vector2(-8, -34), Vector2(-8, -24), Vector2(-8, -8), Vector2(-8, 2), Vector2(8, -34), Vector2(8, -24), Vector2(8, -8), Vector2(8, 2)]:
		m._l2_box(o + Vector3(dp.x, -10.0, dp.y), Vector3(1.0, 16, 1.0), gold, 0.2)
	# end wall framing the stair nook (VISUAL only, no solid — a collider pad
	# here would shove Roshan off the staircase that passes through this plane)
	for ew in [Vector3(-6.2, -9.5, -44.0), Vector3(6.2, -9.5, -44.0)]:
		var ewn = m._l2_box(o + ew, Vector3(3.6, 18, 1.5), stone)
		ewn.material_override = m._castle_mat("wall", 0.045, stone)
		m.fade_walls.append({"node": ewn, "c": ewn.position, "h": (ewn.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	var ewl = m._l2_box(o + Vector3(0, -2.75, -44.0), Vector3(8.8, 4.5, 1.5), stone)
	ewl.material_override = m._castle_mat("wall", 0.045, stone)
	m.fade_walls.append({"node": ewl, "c": ewl.position, "h": (ewl.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	# warm lanterns alternate down the hallway (emissive boxes, no lights)
	for li2 in range(6):
		m._l2_box(o + Vector3(-7.2 + float(li2 % 2) * 14.4, -12.0, -40.0 + float(li2) * 9.0), Vector3(0.6, 1.4, 1.0), Color(1.0, 0.8, 0.45), 3.2)
	# ---------- four side rooms off the hallway ----------
	var rooms := [
		{"c": Vector3(-17, 0, -2), "name": "✨ Pantry ✨", "tint": Color(0.85, 0.78, 0.62)},
		{"c": Vector3(17, 0, -2), "name": "✨ Royal Kitchen ✨", "tint": Color(0.95, 0.82, 0.66)},
		{"c": Vector3(-17, 0, -28), "name": "✨ Bubble Bath ✨", "tint": Color(0.7, 0.8, 0.88), "ensuite": true},
		{"c": Vector3(17, 0, -28), "name": "✨ Craft Room ✨", "tint": Color(0.85, 0.75, 0.9)},
	]
	for rd in rooms:
		var rc: Vector3 = rd["c"]
		var sx2: float = signf(rc.x)
		var rfl = m._l2_box(o + rc + Vector3(0, -18.6, 0), Vector3(18, 1.2, 16), Color(0.6, 0.56, 0.64))
		rfl.material_override = m._castle_mat("cobble", 0.05, rd["tint"])
		var rcl = m._l2_box(o + rc + Vector3(0, -0.9, 0), Vector3(19, 0.8, 17), Color(0.55, 0.52, 0.6))   # ceiling
		m.fade_walls.append({"node": rcl, "c": rcl.position, "h": (rcl.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
		if bool(rd.get("ensuite", false)):
			# far wall split around the secret privy door (z -32..-24)
			m._iwall(o + rc + Vector3(sx2 * 9.0, -9.5, -6), Vector3(1.5, 18, 4), stone, "castle")
			m._iwall(o + rc + Vector3(sx2 * 9.0, -9.5, 6), Vector3(1.5, 18, 4), stone, "castle")
		else:
			m._iwall(o + rc + Vector3(sx2 * 9.0, -9.5, 0), Vector3(1.5, 18, 16), stone, "castle")   # far wall (x +-26)
		m._iwall(o + rc + Vector3(0, -9.5, -8), Vector3(18, 18, 1.5), stone, "castle")          # back wall
		m._iwall(o + rc + Vector3(0, -9.5, 8), Vector3(18, 18, 1.5), stone, "castle")           # front wall
		# glowing lantern on the far wall + a name plate over the doorway
		m._l2_box(o + rc + Vector3(sx2 * 8.0, -12.0, 0), Vector3(0.6, 1.4, 1.0), Color(1.0, 0.8, 0.45), 3.2)
		var rsign := Label3D.new()
		rsign.text = rd["name"]
		rsign.font_size = 40; rsign.pixel_size = 0.02; rsign.outline_size = 10
		rsign.modulate = Color(0.9, 0.95, 1.0)
		rsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		rsign.position = o + Vector3(sx2 * 8.0, -3.5, rc.z)
		m.add_child(rsign); m.game_nodes.append(rsign)
	# PANTRY: shelves of glowing jam jars + barrels
	var pc: Vector3 = o + Vector3(-17, 0, -2)
	for sh in range(2):
		m._l2_box(pc + Vector3(-7.0, -14.0 + float(sh) * 3.4, 0), Vector3(1.6, 0.5, 12), Color(0.55, 0.4, 0.26))
		for ji in range(4):
			m._l2_box(pc + Vector3(-7.0, -13.2 + float(sh) * 3.4, -4.5 + float(ji) * 3.0), Vector3(1.1, 1.3, 1.1), [Color(1.0, 0.5, 0.55), Color(1.0, 0.75, 0.3), Color(0.6, 0.85, 0.4), Color(0.6, 0.7, 1.0)][ji], 0.8)
	for bi2 in range(2):
		m._l2_box(pc + Vector3(4.0 + float(bi2) * 4.0, -16.2, 5.0), Vector3(3.0, 3.6, 3.0), Color(0.55, 0.4, 0.26))
	# ROYAL KITCHEN: counters, a glowing stove with soup on the boil, a tea
	# table set for two — the pantry is right across the hallway, the way a
	# real castle kitchen works (the old toy den moved up to the Toy Room)
	var tc: Vector3 = o + Vector3(17, 0, -2)
	m._l2_box(tc + Vector3(-2.0, -16.4, -6.6), Vector3(10, 3.2, 2.6), Color(0.6, 0.42, 0.28))     # counter
	m._l2_box(tc + Vector3(-2.0, -14.6, -6.6), Vector3(10.4, 0.5, 3.0), Color(0.95, 0.93, 0.88))  # counter top
	m._wall_solid(tc + Vector3(-2.0, -16.0, -6.6), Vector3(10, 4.5, 2.6), 0.4)
	var stove = m._l2_box(tc + Vector3(6.0, -16.1, -6.4), Vector3(3.8, 3.8, 3.0), Color(0.88, 0.9, 0.94))
	stove.material_override.roughness = 0.4
	m._wall_solid(tc + Vector3(6.0, -16.1, -6.4), Vector3(3.8, 3.8, 3.0), 0.4)
	m._l2_box(tc + Vector3(5.2, -14.0, -6.4), Vector3(1.3, 0.25, 1.3), Color(1.0, 0.45, 0.25), 2.2)   # hot burner
	m._l2_box(tc + Vector3(6.9, -14.0, -6.4), Vector3(1.3, 0.25, 1.3), Color(1.0, 0.65, 0.35), 1.4)   # warm burner
	m._l2_box(tc + Vector3(6.0, -16.6, -4.8), Vector3(2.7, 1.7, 0.3), Color(1.0, 0.85, 0.5), 1.2)     # oven window glow
	m._l2_box(tc + Vector3(6.0, -15.4, -4.8), Vector3(3.0, 0.3, 0.35), gold, 0.4)                     # gold oven handle
	var pot := MeshInstance3D.new()   # copper soup pot bubbling on the hot burner
	var pcy := CylinderMesh.new(); pcy.top_radius = 0.9; pcy.bottom_radius = 0.8; pcy.height = 1.1
	pot.mesh = pcy
	pot.material_override = m._soft_mat(Color(0.85, 0.55, 0.35), 0.2)
	pot.position = tc + Vector3(5.2, -13.4, -6.4)
	m.add_child(pot); m.game_nodes.append(pot)
	m._l2_box(tc + Vector3(5.2, -12.8, -6.4), Vector3(1.2, 0.2, 1.2), Color(0.7, 0.95, 0.6), 0.9)     # the soup!
	var kettle := MeshInstance3D.new()
	var ksp := SphereMesh.new(); ksp.radius = 0.7; ksp.height = 1.2
	kettle.mesh = ksp
	kettle.material_override = m._soft_mat(Color(0.9, 0.9, 0.95), 0.15)
	kettle.position = tc + Vector3(-4.0, -13.9, -6.6)
	m.add_child(kettle); m.game_nodes.append(kettle)
	for pn in range(3):   # copper pans hang over the counter
		m._l2_box(tc + Vector3(-5.0 + float(pn) * 2.2, -11.0, -6.9), Vector3(1.4, 1.4, 0.25), Color(0.8, 0.6, 0.4), 0.15)
	var ttab := MeshInstance3D.new()   # tea table set for two
	var tcy := CylinderMesh.new(); tcy.top_radius = 2.2; tcy.bottom_radius = 0.5; tcy.height = 2.6
	ttab.mesh = tcy
	ttab.material_override = m._soft_mat(Color(0.7, 0.5, 0.34))
	ttab.position = tc + Vector3(-2.0, -16.6, 3.5)
	m.add_child(ttab); m.game_nodes.append(ttab)
	m._cyl_solid(tc + Vector3(-2.0, -16.6, 3.5), 2.2, 1.4, 0.3)
	m._l2_box(tc + Vector3(-2.0, -15.1, 3.5), Vector3(1.4, 0.5, 1.4), Color(0.95, 0.9, 0.98), 0.5)    # teapot
	for stx in [-4.8, 0.8]:
		var stool := MeshInstance3D.new()
		var scy := CylinderMesh.new(); scy.top_radius = 1.0; scy.bottom_radius = 0.8; scy.height = 1.6
		stool.mesh = scy
		stool.material_override = m._soft_mat(Color(0.95, 0.75, 0.8))
		stool.position = tc + Vector3(stx, -17.1, 3.5)
		m.add_child(stool); m.game_nodes.append(stool)
	# BUBBLE BATH: a tub of glowy water, a rubber ducky, fluffy towels
	var bc: Vector3 = o + Vector3(-17, 0, -28)
	var tub = m._l2_box(bc + Vector3(-3.0, -16.4, 0), Vector3(7.5, 3.2, 5.0), Color(0.97, 0.97, 1.0))
	tub.material_override = m._soft_mat(Color(0.97, 0.97, 1.0))
	m._l2_box(bc + Vector3(-3.0, -15.0, 0), Vector3(6.3, 0.3, 3.8), Color(0.55, 0.85, 1.0), 0.8)
	m._wall_solid(bc + Vector3(-3.0, -16.4, 0), Vector3(7.5, 3.2, 5.0), 0.4)
	var duck := MeshInstance3D.new()
	var dm := SphereMesh.new(); dm.radius = 0.9; dm.height = 1.8
	duck.mesh = dm
	duck.material_override = m._soft_mat(Color(1.0, 0.9, 0.25), 0.4)
	duck.position = bc + Vector3(-4.0, -14.4, 0.3)
	m.add_child(duck); m.game_nodes.append(duck)
	var dh := MeshInstance3D.new()
	var dhm := SphereMesh.new(); dhm.radius = 0.55; dhm.height = 1.1
	dh.mesh = dhm
	dh.material_override = m._soft_mat(Color(1.0, 0.9, 0.25), 0.4)
	dh.position = bc + Vector3(-3.1, -13.6, 0.3)
	m.add_child(dh); m.game_nodes.append(dh)
	m._l2_box(bc + Vector3(-2.55, -13.6, 0.3), Vector3(0.7, 0.35, 0.5), Color(1.0, 0.6, 0.2), 0.4)   # beak
	for tw2 in range(2):
		m._l2_box(bc + Vector3(5.5, -15.6 + float(tw2) * 1.1, -4.0), Vector3(2.6, 1.0, 2.2), Color(1.0, 0.8, 0.9) if tw2 == 0 else Color(0.8, 0.9, 1.0))
	# CRAFT ROOM: the color-a-fish easel finally gets its own dedicated studio
	# (moved down from the grand hall), with paint pots and a paper table
	var gc: Vector3 = o + Vector3(17, 0, -28)
	var easel = m._l2_box(gc + Vector3(7.4, -13.4, 0), Vector3(0.6, 9.0, 7.0), Color(0.55, 0.4, 0.26))
	m._mg_noop_ref(easel)
	m._wall_solid(gc + Vector3(7.4, -13.4, 0), Vector3(0.6, 9.0, 7.0), 0.5)
	var canvas = m._l2_box(gc + Vector3(6.8, -12.4, 0), Vector3(0.4, 6.0, 5.2), Color(0.97, 0.96, 0.92), 0.15)
	m._mg_noop_ref(canvas)
	var craft_fish_icon := Sprite3D.new()
	craft_fish_icon.texture = load("res://assets/mg/fish_line.png")
	craft_fish_icon.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	craft_fish_icon.pixel_size = 0.012
	craft_fish_icon.position = gc + Vector3(6.3, -12.4, 0)
	m.add_child(craft_fish_icon); m.game_nodes.append(craft_fish_icon)
	m.g["craft_easel"] = gc + Vector3(5.5, -13.4, 0)
	var potcols := [Color(0.92, 0.3, 0.3), Color(1.0, 0.8, 0.25), Color(0.35, 0.75, 0.4), Color(0.35, 0.6, 0.95), Color(0.7, 0.4, 0.9)]
	for pi3 in range(potcols.size()):   # paint pots along the back wall
		m._l2_box(gc + Vector3(-6.0 + float(pi3) * 3.0, -16.6, -6.5), Vector3(1.6, 2.2, 1.6), Color(0.85, 0.82, 0.78))
		m._l2_box(gc + Vector3(-6.0 + float(pi3) * 3.0, -15.3, -6.5), Vector3(1.3, 0.4, 1.3), potcols[pi3], 0.5)
	m._l2_box(gc + Vector3(-3.0, -16.2, 3.0), Vector3(6.5, 3.0, 4.5), Color(0.7, 0.5, 0.34))   # paper table
	m._wall_solid(gc + Vector3(-3.0, -16.2, 3.0), Vector3(6.5, 3.0, 4.5), 0.4)
	m._l2_box(gc + Vector3(-3.8, -14.5, 2.4), Vector3(2.6, 0.25, 3.4), Color(0.98, 0.98, 0.95), 0.2)   # drawing paper
	for cy2 in range(3):   # crayons scattered beside it
		var cray = m._l2_box(gc + Vector3(-1.0 + float(cy2) * 0.9, -14.45, 3.6), Vector3(0.5, 0.3, 2.2), potcols[cy2], 0.4)
		cray.rotation_degrees = Vector3(0, -14.0 + float(cy2) * 14.0, 0)
	# ---------- the hidden ROYAL LOO: a secret privy tucked BEHIND the Bubble
	# Bath, deep in the basement's far corner. Find the little door!
	m._iwall(o + Vector3(-26, -9.5, -34), Vector3(1.5, 18, 4), stone, "castle")   # privy door pier (z -36..-32)
	m._iwall(o + Vector3(-26, -9.5, -22), Vector3(1.5, 18, 4), stone, "castle")   # privy door pier (z -24..-20)
	for gp2 in [-32.0, -24.0]:
		m._l2_box(o + Vector3(-26, -10.0, gp2), Vector3(1.0, 16, 1.0), gold, 0.2)   # gold posts mark the secret door
	var lc: Vector3 = o + Vector3(-30.25, 0, -28)   # privy centre (interior x -34.25..-26.75)
	var lfl = m._l2_box(lc + Vector3(0, -18.6, 0), Vector3(10, 1.2, 12), Color(0.6, 0.56, 0.64))
	lfl.material_override = m._castle_mat("cobble", 0.05, Color(0.72, 0.78, 0.85))
	var lcl = m._l2_box(lc + Vector3(0, -0.9, 0), Vector3(10.5, 0.8, 13), Color(0.55, 0.52, 0.6))   # ceiling
	m.fade_walls.append({"node": lcl, "c": lcl.position, "h": (lcl.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	m._iwall(lc + Vector3(-4.75, -9.5, 0), Vector3(1.5, 18, 12), stone, "castle")   # far wall (x -35)
	m._iwall(lc + Vector3(0, -9.5, -6), Vector3(10, 18, 1.5), stone, "castle")      # back wall
	m._iwall(lc + Vector3(0, -9.5, 6), Vector3(10, 18, 1.5), stone, "castle")       # front wall
	m._l2_box(lc + Vector3(-4.0, -12.0, 0), Vector3(0.6, 1.4, 1.0), Color(1.0, 0.8, 0.45), 3.2)   # lantern
	build_toilet(lc + Vector3(-1.75, -18.0, 0))
	build_dungeon_gate(o + Vector3(0, -18.0, 5.0))

func build_dungeon_gate(ground: Vector3) -> void:
	# The ten-room gate waits at the basement hall entrance. Its two large
	# ability icons explain the lock without reading; approaching also speaks it.
	var root := Node3D.new()
	root.position = ground
	m.add_child(root)
	m.game_nodes.append(root)
	var arch_col := Color(0.64, 0.52, 0.92)
	for i in range(8):
		var a: float = float(i) * TAU / 8.0
		var seg := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(3.0, 0.7, 0.8)
		seg.mesh = box
		seg.material_override = m._soft_mat(arch_col, 0.8)
		seg.position = Vector3(cos(a) * 3.5, 4.0 + sin(a) * 3.5, 0)
		seg.rotation.z = a + PI * 0.5
		root.add_child(seg)
	var veil := MeshInstance3D.new()
	var quad := QuadMesh.new()
	quad.size = Vector2(5.8, 5.8)
	veil.mesh = quad
	var veil_mat := StandardMaterial3D.new()
	veil_mat.albedo_color = Color(0.28, 0.18, 0.55, 0.58)
	veil_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	veil_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	veil_mat.emission_enabled = true
	veil_mat.emission = Color(0.38, 0.28, 0.75)
	veil_mat.emission_energy_multiplier = 0.7
	veil.material_override = veil_mat
	veil.position = Vector3(0, 4.0, 0)
	root.add_child(veil)
	var label := Label3D.new()
	label.text = "❄ + 🌶\n◇ ◇ ◇ ◇ ◇\n◇ ◇ ◇ ◇ ◇"
	label.font_size = 70
	label.pixel_size = 0.022
	label.outline_size = 14
	label.modulate = Color(0.9, 0.86, 1.0)
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	label.position = Vector3(0, 9.0, 0)
	root.add_child(label)
	m.g["dungeon_gate"] = {"node": root, "veil": veil, "label": label, "pos": ground + Vector3(0, 3.0, 0), "armed": true, "cool": 0.0, "ready": false}


func build_music_room(o: Vector3) -> void:
	# Roomy music hall off the LEFT wall (doorway x=-35, z=-16).
	# Footprint x:-52..-35 (width 17), z:-24..+14 (depth 38) — a long room so the
	# xylophone has space. Interior corners stay inside the dome (r<58).
	var mo: Vector3 = o + Vector3(-43.5, 0, -5)           # room centre
	var wall := Color(0.62, 0.65, 0.80)                  # cool lilac plaster
	# flr + ceiling (no colliders — flr clamp / arena_ceil handle vertical)
	var mfloor = m._l2_box(mo + Vector3(0, 0.4, 0), Vector3(19, 1.0, 40), Color(0.5, 0.45, 0.7))
	mfloor.material_override = m._castle_mat("floor", 0.035, Color(0.58, 0.60, 0.78))
	m._l2_box(mo + Vector3(0, 33.0, 0), Vector3(19, 1.5, 40), Color(0.54, 0.56, 0.68))
	# enclosing walls (the right/hall side is the segmented hall wall already built)
	m._iwall(mo + Vector3(-9.25, 16, 0), Vector3(1.5, 34, 40), wall)       # far wall (x=-52.75)
	m._iwall(mo + Vector3(0, 16, -19.75), Vector3(19, 34, 1.5), wall)      # back wall (z=-24.75)
	m._iwall(mo + Vector3(0, 16, 19.75), Vector3(19, 34, 1.5), wall)       # front wall (z=+14.75)
	# gold doorway frame around the opening in the hall wall
	for dz in [-21.0, -11.0]:
		m._l2_box(o + Vector3(-35, 8, dz), Vector3(1.2, 16, 1.2), Color(0.85, 0.72, 0.45), 0.15)
	# soft rug by the entrance
	var rug = m._l2_box(mo + Vector3(3.0, 0.95, -11.0), Vector3(9, 0.1, 8), Color(0.35, 0.3, 0.6))
	rug.material_override = m._castle_mat("carpet", 0.065, Color(0.62, 0.58, 0.82))
	# ---------- the swim-through xylophone (a free-play music toy) ----------
	# bells run in a spaced row down the length of the room (no overlap)
	var bellcols := [Color(1, 0.3, 0.3), Color(1, 0.6, 0.2), Color(1, 0.9, 0.3), Color(0.3, 0.85, 0.4), Color(0.3, 0.6, 1.0), Color(0.5, 0.4, 0.9), Color(0.95, 0.4, 0.8)]
	var bellpitch := [0.5, 0.56, 0.63, 0.75, 0.84, 0.94, 1.0]   # warmer, lower octave — gentler for little ears
	m.g["bells"] = []
	for rail_x: float in [-4.1, 4.1]:
		var rail: MeshInstance3D = m._l2_box(mo + Vector3(rail_x, 1.25, 0.0), Vector3(0.8, 1.0, 32.0), Color(0.28, 0.18, 0.24))
		rail.material_override = m._castle_mat("wood", 0.14, Color(0.42, 0.30, 0.38))
	for bi in range(7):
		var bell := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(8.4 - float(bi) * 0.55, 1.25, 2.8)
		bell.mesh = bm
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = bellcols[bi]
		bmat.emission_enabled = true
		bmat.emission = bellcols[bi]
		bmat.emission_energy_multiplier = 0.10
		bmat.metallic = 0.1
		bmat.roughness = 0.58
		bell.material_override = bmat
		bell.position = mo + Vector3(0.0, 2.6, -13.5 + float(bi) * 4.5)   # spaced 4.5 along z
		m.add_child(bell)
		m.game_nodes.append(bell)
		var bp := AudioStreamPlayer.new()
		bp.stream = load("res://assets/audio/chime.ogg")
		bp.pitch_scale = bellpitch[bi]
		bp.volume_db = -13.0   # much softer bells
		bell.add_child(bp)   # parent to the bell so it frees with the room (game_nodes is Array[Node3D])
		(m.g["bells"] as Array).append({"node": bell, "player": bp, "cool": 0.0, "base_y": bell.position.y, "tw": null})
	# ECHO BELLS: the golden song-star starts a copy-me bell song — a gentle
	# Simon-says for little ears. Wrong notes just replay the song (no fail);
	# three rounds (2, 3, 4 notes) earn +2 rainbow pearls.
	var song_star := Label3D.new()
	song_star.text = "♪"
	song_star.font_size = 220
	song_star.pixel_size = 0.02
	song_star.outline_size = 18
	song_star.modulate = Color(1.0, 0.85, 0.3)
	song_star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	song_star.position = mo + Vector3(0, 6.5, -18.5)
	m.add_child(song_star)
	m.game_nodes.append(song_star)
	var ssl := OmniLight3D.new()
	ssl.light_color = Color(1.0, 0.9, 0.4)
	ssl.light_energy = 0.9
	ssl.omni_range = 9.0
	ssl.position = song_star.position
	m.add_child(ssl)
	m.game_nodes.append(ssl)
	m._register_castle_light(ssl, true)
	m.g["song_star"] = song_star.position
	m.g["bellgame"] = {"state": "idle", "seq": [], "i": 0, "t": 0.0, "round": 0, "cool": 0.0}
	# two warm fill lights down the length
	for lz in [-12.0, 10.0]:
		var ml := OmniLight3D.new()
		ml.light_color = Color(0.85, 0.85, 1.0); ml.light_energy = 0.85; ml.omni_range = 24.0
		ml.position = mo + Vector3(0, 22, lz); m.add_child(ml); m.game_nodes.append(ml)
		m._register_castle_light(ml, false)
	# glowing windows on the far wall
	for wz in [-10.0, 10.0]:
		var win = m._l2_box(mo + Vector3(-9.1, 20, wz), Vector3(0.4, 7, 6), Color(0.42, 0.56, 0.82), 0.12)
		win.material_override.emission_energy_multiplier = 0.18
	# sign over the doorway
	var msign := Label3D.new()
	msign.text = "♪"
	msign.font_size = 56; msign.pixel_size = 0.028; msign.outline_size = 12
	msign.modulate = Color(0.85, 0.9, 1.0); msign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	msign.position = o + Vector3(-35, 20.0, -16); m.add_child(msign); m.game_nodes.append(msign)
	# cool invite glow at the doorway
	var il := OmniLight3D.new()
	il.light_color = Color(0.6, 0.7, 1.0); il.light_energy = 1.6; il.omni_range = 14.0
	il.position = o + Vector3(-34, 7, -16); m.add_child(il); m.game_nodes.append(il)
	m._register_castle_light(il, true)


func build_bedroom(o: Vector3) -> void:
	# Roomy royal bedroom off the right-wall doorway (x=35, z=-16).
	# Footprint x:35..57, z:-28..-6 (22x22) — corners r<65, inside the dome (66).
	var bo: Vector3 = o + Vector3(46, 0, -17)            # room centre
	var wall := Color(0.66, 0.54, 0.60)                  # warm rosy plaster
	# flr + ceiling (no colliders — handled by the flr clamp / arena_ceil)
	var bfloor = m._l2_box(bo + Vector3(0, 0.4, 0), Vector3(22, 1.0, 22), Color(0.78, 0.6, 0.5))
	bfloor.material_override = m._castle_mat("floor", 0.035, Color(0.82, 0.70, 0.72))
	m._l2_box(bo + Vector3(0, 33.0, 0), Vector3(22, 1.5, 22), Color(0.56, 0.48, 0.54))
	# enclosing walls (the left/hall side is the segmented hall wall already built)
	m._iwall(bo + Vector3(11, 16, 0), Vector3(1.5, 34, 22), wall)          # far wall (x=57)
	m._iwall(bo + Vector3(0, 16, -11), Vector3(22, 34, 1.5), wall)         # back wall (z=-28)
	m._iwall(bo + Vector3(0, 16, 11), Vector3(22, 34, 1.5), wall)          # front wall (z=-6)
	# Base and cornice bands stop the compact room reading as three intersecting
	# blank planes; all are visual-only and stay tight to the existing shell.
	for trim_y: float in [1.6, 29.8]:
		m._l2_box(bo + Vector3(10.2, trim_y, 0), Vector3(0.8, 1.6, 20.5), Color(0.46, 0.31, 0.46))
		m._l2_box(bo + Vector3(0, trim_y, -10.2), Vector3(20.5, 1.6, 0.8), Color(0.46, 0.31, 0.46))
		m._l2_box(bo + Vector3(0, trim_y, 10.2), Vector3(20.5, 1.6, 0.8), Color(0.46, 0.31, 0.46))
	# gold doorway frame around the opening in the hall wall
	for dz in [-21.0, -11.0]:
		m._l2_box(o + Vector3(35, 8, dz), Vector3(1.2, 16, 1.2), Color(0.85, 0.72, 0.45), 0.15)
	# ---------- the royal bed (head against the back wall, room to walk all around) ----------
	var bcx: float = bo.x + 4.0
	var bcz: float = bo.z - 2.0
	if ResourceLoader.exists("res://assets/castle/bed.glb"):
		# real Kenney bed (CC0). Length runs along Z; the headboard sits at +Z in
		# the GLB (verified render) so spin PI to put it against the back wall.
		var bmodel: Node3D = (load("res://assets/castle/bed.glb") as PackedScene).instantiate()
		var bh := Node3D.new()
		bh.add_child(bmodel)
		m._fit_prop(bmodel, 12.0)
		bh.rotation.y = PI
		bh.position = Vector3(bcx, o.y + 0.9, bcz)
		m.add_child(bh)
		m.game_nodes.append(bh)
	else:
		var frame = m._l2_box(Vector3(bcx, o.y + 2.0, bcz), Vector3(7, 2.5, 12), Color(0.5, 0.32, 0.2))   # wooden frame
		frame.material_override.roughness = 0.8
		m._l2_box(Vector3(bcx, o.y + 3.7, bcz), Vector3(6, 1.2, 11), Color(0.98, 0.97, 1.0))               # mattress
		m._l2_box(Vector3(bcx, o.y + 4.4, bcz + 2.0), Vector3(6.2, 0.5, 6.5), Color(0.45, 0.62, 0.92))     # folded blanket
		m._l2_box(Vector3(bcx, o.y + 4.6, bcz - 4.2), Vector3(5.0, 0.9, 2.4), Color(1.0, 1.0, 1.0))        # pillow
		var headboard = m._l2_box(Vector3(bcx, o.y + 5.8, bcz - 5.8), Vector3(7, 6.5, 0.9), Color(0.45, 0.28, 0.17))
		headboard.material_override.roughness = 0.7
	# bed collider: SLIM pad — the old 1.6 pad ejected Roshan outside the sleep
	# trigger radius, so climbing into bed could never fire the cutscene
	m._wall_solid(Vector3(bcx, o.y + 2.0, bcz), Vector3(7, 2.5, 12), 0.5)
	m.g["bed_pos"] = Vector3(bcx, o.y + 3.6, bcz)   # mattress top — the go-to-sleep trigger
	var bedsign := Label3D.new()
	bedsign.text = "zZz"
	bedsign.font_size = 40
	bedsign.pixel_size = 0.02
	bedsign.outline_size = 10
	bedsign.modulate = Color(0.8, 0.85, 1.0)
	bedsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	bedsign.position = Vector3(bcx, o.y + 10.0, bcz)
	m.add_child(bedsign)
	m.game_nodes.append(bedsign)
	# ---------- bedside table + glowing lamp (at the bed's head) ----------
	var table = m._l2_box(Vector3(bcx - 6.5, o.y + 1.8, bcz - 5.0), Vector3(2.4, 3.2, 2.4), Color(0.5, 0.32, 0.2))
	table.material_override.roughness = 0.8
	m._wall_solid(Vector3(bcx - 6.5, o.y + 1.8, bcz - 5.0), Vector3(2.4, 3.2, 2.4), 0.4)
	var lampbulb := MeshInstance3D.new()
	var ls := SphereMesh.new(); ls.radius = 0.7; ls.height = 1.4
	lampbulb.mesh = ls
	var lmat := StandardMaterial3D.new()
	lmat.emission_enabled = true; lmat.emission = Color(1.0, 0.82, 0.5); lmat.emission_energy_multiplier = 0.55
	lampbulb.material_override = lmat
	lampbulb.position = Vector3(bcx - 6.5, o.y + 4.6, bcz - 5.0)
	m.add_child(lampbulb); m.game_nodes.append(lampbulb)
	var lamp := OmniLight3D.new()
	lamp.light_color = Color(1.0, 0.82, 0.55); lamp.light_energy = 0.85; lamp.omni_range = 11.0
	lamp.position = lampbulb.position; m.add_child(lamp); m.game_nodes.append(lamp)
	m._register_castle_light(lamp, true)
	# big soft rug in the middle of the room
	var rug = m._l2_box(bo + Vector3(-5.0, 0.95, 3.0), Vector3(10, 0.1, 8), Color(0.7, 0.3, 0.4))
	rug.material_override = m._castle_mat("carpet", 0.065, Color(0.82, 0.66, 0.72))
	# toy chest by the far wall (decor)
	var chest = m._l2_box(bo + Vector3(8.5, 1.6, 6.0), Vector3(3.4, 2.4, 2.4), Color(0.75, 0.5, 0.3))
	chest.material_override.roughness = 0.85
	m._wall_solid(bo + Vector3(8.5, 1.6, 6.0), Vector3(3.4, 2.4, 2.4), 0.4)
	m._l2_box(bo + Vector3(8.5, 3.0, 6.0), Vector3(3.6, 0.5, 2.6), Color(0.55, 0.34, 0.2))
	# ---------- DRESS-UP VANITY: a wardrobe + mirror (swim up to pick your outfit) ----------
	var vpos: Vector3 = bo + Vector3(-6.0, 0, 9.0)        # against the front wall, facing the room
	var wardrobe = m._l2_box(vpos + Vector3(0, 7.0, 1.0), Vector3(7, 14, 1.6), Color(0.55, 0.34, 0.22))
	wardrobe.material_override.roughness = 0.8
	var mirror = m._l2_box(vpos + Vector3(0, 7.5, 0.1), Vector3(4.5, 9.0, 0.2), Color(0.45, 0.68, 0.82), 0.15)  # softly glowing mirror glass
	mirror.material_override.metallic = 0.55
	mirror.material_override.roughness = 0.18
	for fx in [-2.6, 2.6]:                                 # gold mirror frame posts
		m._l2_box(vpos + Vector3(fx, 7.5, 0.2), Vector3(0.6, 9.5, 0.5), Color(0.95, 0.8, 0.4), 0.2)
	m._l2_box(vpos + Vector3(0, 12.4, 0.2), Vector3(5.7, 0.6, 0.5), Color(0.95, 0.8, 0.4), 0.2)   # frame top
	m._wall_solid(vpos + Vector3(0, 7.0, 1.0), Vector3(7, 14, 1.6))   # the wardrobe is solid
	var vsign := Label3D.new()
	vsign.text = "\U0001f457"
	vsign.font_size = 48; vsign.pixel_size = 0.028; vsign.outline_size = 12
	vsign.modulate = Color(1.0, 0.8, 0.95); vsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	vsign.position = vpos + Vector3(0, 13.6, 0); m.add_child(vsign); m.game_nodes.append(vsign)
	var vl := OmniLight3D.new()
	vl.light_color = Color(1.0, 0.85, 0.95); vl.light_energy = 0.9; vl.omni_range = 12.0
	vl.position = vpos + Vector3(0, 8, -2); m.add_child(vl); m.game_nodes.append(vl)
	m._register_castle_light(vl, false)
	m.g["wardrobe"] = vpos + Vector3(0, 6, -2)
	# fill light so the room reads warm
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.88, 0.78); bl.light_energy = 0.8; bl.omni_range = 22.0
	bl.position = bo + Vector3(0, 22, 0); m.add_child(bl); m.game_nodes.append(bl)
	m._register_castle_light(bl, false)
	# glowing windows on the far and back walls for ambiance
	var win = m._l2_box(bo + Vector3(10.4, 20, 0), Vector3(0.4, 7, 6), Color(0.38, 0.62, 0.82), 0.12)
	win.material_override.emission_energy_multiplier = 0.18
	var win2 = m._l2_box(bo + Vector3(-4.0, 20, -10.4), Vector3(6, 7, 0.4), Color(0.38, 0.62, 0.82), 0.12)
	win2.material_override.emission_energy_multiplier = 0.18
	# label over the doorway
	var blab := Label3D.new()
	blab.text = "\U0001f6cf️"
	blab.font_size = 56; blab.pixel_size = 0.03; blab.outline_size = 12
	blab.modulate = Color(1.0, 0.9, 0.85)
	blab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	blab.position = o + Vector3(35, 20.0, -16)
	m.add_child(blab); m.game_nodes.append(blab)
	# warm invite glow at the doorway
	var il := OmniLight3D.new()
	il.light_color = Color(1.0, 0.8, 0.6); il.light_energy = 1.6; il.omni_range = 14.0
	il.position = o + Vector3(34, 7, -16); m.add_child(il); m.game_nodes.append(il)
	m._register_castle_light(il, true)


func build_toilet(ground: Vector3) -> void:
	# a tiny royal loo. `ground` sits ON the floor (y = floor top); the cistern
	# faces -x, so place it with a wall on its left.
	var porcelain := Color(0.97, 0.97, 1.0)
	var bmat = m._l2_box(ground + Vector3(0.4, 0.1, 0), Vector3(4.5, 0.15, 4.5), Color(0.62, 0.85, 0.95))   # soft bath mat
	bmat.material_override.roughness = 1.0
	var base := MeshInstance3D.new()
	var bcy := CylinderMesh.new(); bcy.top_radius = 1.0; bcy.bottom_radius = 1.2; bcy.height = 1.8
	base.mesh = bcy
	base.material_override = m._soft_mat(porcelain)
	base.position = ground + Vector3(0, 0.9, 0)
	m.add_child(base); m.game_nodes.append(base)
	var bowl := MeshInstance3D.new()
	var bw := CylinderMesh.new(); bw.top_radius = 1.6; bw.bottom_radius = 1.1; bw.height = 1.4
	bowl.mesh = bw
	bowl.material_override = m._soft_mat(porcelain)
	bowl.position = ground + Vector3(0, 2.3, 0)
	m.add_child(bowl); m.game_nodes.append(bowl)
	var wat := MeshInstance3D.new()   # glowy water in the bowl
	var wc := CylinderMesh.new(); wc.top_radius = 0.95; wc.bottom_radius = 0.95; wc.height = 0.12
	wat.mesh = wc
	wat.material_override = m._soft_mat(Color(0.55, 0.85, 1.0), 0.5)
	wat.position = ground + Vector3(0, 2.82, 0)
	m.add_child(wat); m.game_nodes.append(wat)
	var seat := MeshInstance3D.new()   # rosy seat ring
	var sr := TorusMesh.new(); sr.inner_radius = 1.0; sr.outer_radius = 1.7
	seat.mesh = sr
	seat.material_override = m._soft_mat(Color(1.0, 0.8, 0.9))
	seat.position = ground + Vector3(0, 3.05, 0)
	m.add_child(seat); m.game_nodes.append(seat)
	# cistern against the wall + a gold flush handle
	var tank = m._l2_box(ground + Vector3(-1.9, 2.5, 0), Vector3(1.2, 3.2, 3.0), porcelain)
	tank.material_override.roughness = 0.25
	m._l2_box(ground + Vector3(-1.9, 4.3, 1.0), Vector3(0.5, 0.4, 0.9), Color(0.95, 0.8, 0.4), 0.4)
	m._wall_solid(ground + Vector3(-0.5, 1.6, 0), Vector3(3.4, 5.0, 3.2), 0.4)
	var tsign := Label3D.new()
	tsign.text = "✨ Royal Loo ✨"
	tsign.font_size = 40; tsign.pixel_size = 0.02; tsign.outline_size = 10
	tsign.modulate = Color(0.8, 0.92, 1.0)
	tsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tsign.position = ground + Vector3(0, 6.1, 0)
	m.add_child(tsign); m.game_nodes.append(tsign)
	# bubbly toot, gentle volume for little ears (tick re-arms it on swim-away)
	var tap := AudioStreamPlayer.new()
	tap.stream = load("res://assets/audio/fart.ogg")
	tap.volume_db = -8.0
	tap.pitch_scale = 1.1
	base.add_child(tap)   # frees with the toilet
	m.g["toilet"] = {"pos": ground + Vector3(0, 2.1, 0), "player": tap, "armed": true}


func slide_stand() -> void:
	# The golden stand wakes: a deep stone rumble, then it slides clear of the
	# stairwell it was sealing and the shaft zone opens up to the hallway. The
	# hug-chest trigger moves with it and stays gated on stand_open, so the
	# hug can never fire mid-slide.
	m.g["stand_open"] = true
	m.g["secret_armed"] = false   # swim away and back to the chest's new spot for the hug
	var chest: Node3D = m.g["stand_chest"]
	var lid: Node3D = m.g["stand_lid"]
	if not is_instance_valid(chest) or not is_instance_valid(lid):
		return
	var slide := Vector3(-12.0, 0.0, -3.0)   # over toward the loo end, clear of the opening
	m.g["secret_door"] = chest.position + slide
	if m.g.has("stand_zone"):
		var zd: Dictionary = m.g["stand_zone"]
		zd["band"] = Vector2(-18.0, 3.5)   # the shaft now reaches the hallway floor
		zd["ramp"] = [2, -47.5, -0.7, -40.5, -15.4]   # stair ramp rises to the opening
		zd.erase("ceil")
	var rumble := AudioStreamPlayer.new()
	rumble.stream = load("res://assets/audio/buzz.ogg")
	rumble.pitch_scale = 0.45   # deep slow buzz = stone grinding
	chest.add_child(rumble)   # frees with the chest
	rumble.play()
	var tw: Tween = chest.create_tween().set_parallel(true).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(chest, "position", chest.position + slide, 1.6)
	tw.tween_property(lid, "position", lid.position + slide, 1.6)
	if m.g.has("stand_label") and is_instance_valid(m.g["stand_label"]):
		tw.tween_property(m.g["stand_label"], "position", (m.g["stand_label"] as Node3D).position + slide, 1.6)
	m._sparkle_burst(chest.position + Vector3(0, 4, 0), Color(1.0, 0.85, 0.4))
	m.show_msg("Pearl Castle", "The golden stand rumbles aside... a secret staircase! Swim down to the basement!")


func tick(delta: float, ppos: Vector3) -> void:
	# Princess Huluu's tail sways gently on the throne (rigged plushie idle)
	if m.g.has("huluu_skel"):
		var hs: Skeleton3D = m.g["huluu_skel"]
		if is_instance_valid(hs):
			var ht: float = float(m.g.get("t", 0.0))
			for hb in range(8):
				var hbi: int = hs.find_bone("tail%d" % (hb + 1))
				if hbi >= 0:
					hs.set_bone_pose_rotation(hbi, Quaternion(Vector3.RIGHT, sin(ht * 1.6 - float(hb) * 0.5) * 0.06 * (0.3 + float(hb) / 8.0)))
			var hdi: int = hs.find_bone("head")
			if hdi >= 0:
				hs.set_bone_pose_rotation(hdi, Quaternion(Vector3.BACK, sin(ht * 0.8) * 0.05))
	if m.wardrobe_layer != null:
		return   # dressing up — pause all hall triggers
	if m.sleep_t >= 0.0:
		m._tick_sleep(delta)
		return
	# bedtime: snuggle onto the bed to sleep the day away (or the night!)
	m.sleep_cool = maxf(0.0, m.sleep_cool - delta)
	if m.g.has("bed_pos") and m.sleep_cool <= 0.0 and m.mg_kind == "" and m.craft_layer == null:
		var bpv: Vector3 = m.g["bed_pos"]
		# generous: fires the moment Roshan touches the bed from ANY side (the old
		# 4.0 radius sat entirely inside the collider's eject distance — unreachable)
		if Vector2(bpv.x - ppos.x, bpv.z - ppos.z).length() < 7.0 and absf(bpv.y - ppos.y) < 8.0:
			m._begin_sleep()
			return
	m.hud_game.text = "Swim up the stairs to Princess Huluu and the Crown Star!"
	# --- the golden stand: glows, then rumbles aside to reveal the basement
	# stairs. Armed only after Roshan has been >14 away, so the moat-hatch
	# spawn (right beside it) never fires the reveal mid-greeting.
	if not bool(m.g.get("stand_open", false)) and m.g.has("stand_chest"):
		var stn: Node3D = m.g["stand_chest"]
		if is_instance_valid(stn):
			var sdist: float = stn.position.distance_to(ppos)
			if sdist > 14.0:
				m.g["stand_armed"] = true
			elif bool(m.g.get("stand_armed", false)) and sdist < 11.0:
				slide_stand()
	# The royal loo is the hidden doorway to the pepper battle. It still gives
	# its familiar bubbly toot, then transforms the room into the combat arena.
	# Once won, it returns to being a harmless re-arming joke prop.
	if m.g.has("toilet"):
		var td: Dictionary = m.g["toilet"]
		var tpp: Vector3 = td["pos"]
		if tpp.distance_to(ppos) > 7.5:
			td["armed"] = true
		elif bool(td.get("armed", false)) and tpp.distance_to(ppos) < 4.5:
			td["armed"] = false
			(td["player"] as AudioStreamPlayer).play()
			m._sparkle_burst(tpp + Vector3(0, 2.0, 0), Color(0.6, 0.9, 1.0))
			if not m.combat_fire_done and m.combat_game == null:
				m.call_deferred("_start_combat", "fire")
				return
	# Elemental dungeon gate: both tutorial encounters unlock it. Lingering at
	# the threshold cannot retrigger it; the safe-home return places Roshan aside.
	if m.g.has("dungeon_gate"):
		var dg: Dictionary = m.g["dungeon_gate"]
		dg["cool"] = maxf(0.0, float(dg["cool"]) - delta)
		var ready: bool = m.combat_ice_done and m.combat_fire_done
		if ready != bool(dg["ready"]):
			dg["ready"] = ready
			(dg["label"] as Label3D).text = "★  TEN ROOMS  ★\n◆ ◆ ◆ ◆ ◆\n◆ ◆ ◆ ◆ ◆" if ready else "❄ + 🌶\n◇ ◇ ◇ ◇ ◇\n◇ ◇ ◇ ◇ ◇"
			var veil: MeshInstance3D = dg["veil"]
			var veil_mat: StandardMaterial3D = veil.material_override as StandardMaterial3D
			if veil_mat != null:
				veil_mat.albedo_color = Color(1.0, 0.82, 0.45, 0.58) if ready else Color(0.28, 0.18, 0.55, 0.58)
				veil_mat.emission = Color(1.0, 0.72, 0.24) if ready else Color(0.38, 0.28, 0.75)
		var gate_pos: Vector3 = dg["pos"]
		var gate_dist: float = gate_pos.distance_to(ppos)
		if gate_dist > 8.0:
			dg["armed"] = true
		elif gate_dist < 5.0 and bool(dg["armed"]) and float(dg["cool"]) <= 0.0:
			dg["armed"] = false
			dg["cool"] = 5.0
			if ready and m.dungeon_game == null:
				m.call_deferred("_start_dungeon")
				return
			m.show_msg("Roshan", "The dungeon needs BOTH powers: the Ice Berry and the spicy garden pepper!", "locked")
	# leave the castle from the entrance
	if m.g.has("hall_exit") and float(m.g["t"]) > 2.5:
		var hx: Vector3 = m.g["hall_exit"]
		if hx.distance_to(ppos) > 14.0:
			m.g["hall_exit_armed"] = true
		# The solid front wall stops Roshan about 11.7 units from this centre point;
		# catch her on the playable side of the arch instead of behind the blocker.
		if bool(m.g.get("hall_exit_armed", false)) and hx.distance_to(ppos) < 12.0:
			m._return_to_courtyard()
			return
	# crafting studio: swim up to the easel to color a fish
	if m.g.has("craft_easel") and m.craft_layer == null and m.mg_cool <= 0.0 and m.mg_kind == "":
		var ce: Vector3 = m.g["craft_easel"]
		if ce.distance_to(ppos) < 7.0:
			m._open_craft_studio()
			return
	# dress-up vanity: swim up to the bedroom wardrobe to pick your outfit
	if m.g.has("wardrobe") and m.wardrobe_layer == null and m.craft_layer == null and m.mg_cool <= 0.0 and m.mg_kind == "":
		var wp: Vector3 = m.g["wardrobe"]
		if wp.distance_to(ppos) < 7.0:
			m._open_wardrobe()
			return
	# music room: swim near a bell to play its note. Short cooldown so rapid
	# passes re-trigger almost instantly; the prior bob tween is killed and the
	# bell reset to base each strike so overlapping hits stay snappy, not jittery.
	var bg2: Dictionary = m.g.get("bellgame", {})
	var bells2: Array = m.g.get("bells", [])
	for bi2 in range(bells2.size()):
		var bd: Dictionary = bells2[bi2]
		bd["cool"] = maxf(0.0, float(bd["cool"]) - delta)
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			continue
		var near_b: bool = bn.position.distance_to(ppos) < 5.0
		var was_near: bool = bool(bd.get("near", false))
		bd["near"] = near_b
		if String(bg2.get("state", "")) == "play":
			continue   # the song-star is singing — listen first!
		if String(bg2.get("state", "")) == "echo":
			# during the echo, a ring fires once per visit (edge-triggered) so
			# lingering next to a bell can't spam wrong notes
			if near_b and not was_near:
				bd["cool"] = 0.12
				m._ring_bell(bd)
				m._bellgame_echo(bg2, bi2)
		elif near_b and float(bd["cool"]) <= 0.0:
			bd["cool"] = 0.12
			m._ring_bell(bd)
	m._tick_bellgame(bg2, delta, ppos)
	# secret easter-egg chest behind the throne -> ONE consistent bonus game.
	# Fires once when you reach it; will not fire again until you swim away and come back
	# (so it never spins randomly through games while you linger nearby).
	# gated on stand_open (the chest is busy being the stand until then), and a
	# tight radius: its slid-aside spot is near the stairwell, so the hug must
	# not grab Roshan while she is heading down to the basement
	if m.g.has("secret_door") and bool(m.g.get("stand_open", false)) and m.mg_cool <= 0.0 and m.mg_kind == "":
		var sd: Vector3 = m.g["secret_door"]
		var near: bool = sd.distance_to(ppos) < 8.0
		if not near:
			m.g["secret_armed"] = true
		elif bool(m.g.get("secret_armed", true)):
			m.g["secret_armed"] = false
			m._play_hug_cutscene()
			return
	m.mg_cool = maxf(0.0, m.mg_cool - delta)
	# Princess Huluu greets Roshan as she gets near the throne
	var hpos: Vector3 = m.CASTLE_POS + Vector3(0, 21.0, -27.0)
	if not bool(m.g.get("huluu_greeted", false)) and hpos.distance_to(ppos) < 26.0:
		m.g["huluu_greeted"] = true
		if m.fairy_skin_unlocked:
			# the story loops back: Huluu acknowledges the Butterfly World rescue
			m.show_msg("Princess Huluu", "You saved Rosalina's butterflies? You're a HERO, Mermaid Roshan!", "hero")
		else:
			m.show_msg("Princess Huluu", "Thank you, Mermaid Roshan, you did a great job! This is now your castle!", "win")
	var crown: Node3D = m.l2_stars[0]["node"]
	var crown_t: float = float(m.g["t"])
	crown.rotate_y(delta * 1.4)
	var crown_won: bool = bool(m.g.get("crown_won", false))
	if not crown_won:
		var crown_base_y: float = float(crown.get_meta("base_y", crown.position.y))
		crown.position.y = crown_base_y + sin(crown_t * 2.0) * 0.55
		var crown_pulse: float = 1.0 + sin(crown_t * 3.2) * 0.08
		crown.scale = Vector3.ONE * crown_pulse
	var crown_guides: Array = m.g.get("crown_guides", [])
	for guide_i in range(crown_guides.size()):
		var guide: Label3D = crown_guides[guide_i] as Label3D
		if not is_instance_valid(guide):
			continue
		guide.visible = not crown_won
		var guide_pulse: float = 0.90 + sin(crown_t * 3.0 - float(guide_i) * 0.85) * 0.14
		guide.scale = Vector3.ONE * guide_pulse
	# Touching the Crown Star CELEBRATES IN PLACE (owner 2026-07-12: it used to
	# call _finish_level2() and eject Roshan to the ocean — touching the throne
	# yanked her out of her own castle). The win still counts (level2_done_once
	# + save); she keeps the castle and leaves by the front door when SHE wants.
	if not crown_won:
		# gentle stair helper (not a black hole): only a soft updraft when the player
		# is in FRONT of the throne and below the crown; retired once the crown is won
		var d: float = crown.position.distance_to(ppos)
		var in_front: bool = ppos.z > crown.position.z + 3.0
		if in_front and d < 16.0 and ppos.y < crown.position.y - 1.0:
			m.player.position = m.player.position.lerp(crown.position, minf(0.16, delta * 0.5))
			m.player.vel.y = maxf(m.player.vel.y, 0.0)
		if d < 5.0:
			m.g["crown_won"] = true
			m.level2_done_once = true
			m._write_save()
			if m.voice != null:
				m.voice.pitch_scale = 1.15
				m.voice.play()
			for i in range(10):
				m._sparkle_burst(ppos + Vector3(randf() * 12 - 6, randf() * 8, randf() * 12 - 6), Color.from_hsv(randf(), 0.6, 1.0))
			var ctw: Tween = crown.create_tween()
			ctw.tween_property(crown, "position:y", crown.position.y + 5.0, 0.8).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			ctw.parallel().tween_property(crown, "scale", Vector3.ONE * 1.15, 0.8)
			m.show_msg("Pearl Castle", "The Crown Star is yours! This castle is YOURS now - explore every room, and leave by the front door whenever you like!", "win")

