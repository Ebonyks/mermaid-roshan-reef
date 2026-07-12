class_name CastleHall
extends RefCounted
# Phase 7.2: mechanical extraction of the Grand Hall (build + tick + the
# music room and bedroom it owns) from main.gd. All state stays on main;
# this class receives main by reference and owns only the logic.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(o: Vector3) -> void:
	# polished marble flr
	var flr := MeshInstance3D.new()
	var fb := BoxMesh.new()
	fb.size = Vector3(70, 1.0, 80)
	flr.mesh = fb
	var fm = m._up_mat("marble", 0.045, Color(0.95, 0.93, 0.98))   # polished marble hall flr (same 0.045 scale as the _iwall stone so floor + walls read as one build)
	fm.metallic = 0.25
	fm.roughness = 0.22
	flr.material_override = fm
	flr.position = o + Vector3(0, 0, 6)
	m.add_child(flr)
	m.game_nodes.append(flr)
	# checker accent tiles
	for cxx in range(-3, 4):
		for czz in range(-3, 5):
			if (cxx + czz) % 2 == 0:
				continue
			var tile = m._l2_box(o + Vector3(float(cxx) * 9.0, 0.55, 6.0 + float(czz) * 9.0), Vector3(8.6, 0.1, 8.6), Color(0.55, 0.5, 0.72))
			tile.material_override = m._up_mat("flagstone", 0.05, Color(0.7, 0.66, 0.85))
	# plush red carpet runner from the entrance up to the stairs
	var runner = m._l2_box(o + Vector3(0, 0.62, 14.0), Vector3(10.0, 0.15, 52.0), Color(0.72, 0.16, 0.22))
	runner.material_override = m._up_mat("fabric", 0.10, Color(0.8, 0.22, 0.28))   # real woven carpet
	for trim in [-5.4, 5.4]:
		m._l2_box(o + Vector3(trim, 0.66, 14.0), Vector3(0.7, 0.2, 52.0), Color(0.95, 0.8, 0.35), 0.15)
	# walls (each upright wall also registers a solid collider so Roshan can't swim through it)
	var wcol := Color(0.95, 0.92, 0.97)
	var scol := Color(0.93, 0.9, 0.95)
	# back wall, SEGMENTED to leave two real doorway openings at x=+-22 (the side archways)
	# GRAND EXPANSION (owner 2026-07-11): the hall rises to 52 — a real great
	# hall — and the center wall gains a GALLERY DOORWAY (x -8..8, y 33..42)
	# from the new balcony into the top chambers.
	m._iwall(o + Vector3(0, 16.5, -34), Vector3(35.0, 33, 1.5), wcol, "marble")    # center, below the gallery door
	m._iwall(o + Vector3(-12.75, 42.5, -34), Vector3(9.5, 19, 1.5), wcol, "marble")  # gallery door, left pier
	m._iwall(o + Vector3(12.75, 42.5, -34), Vector3(9.5, 19, 1.5), wcol, "marble")   # gallery door, right pier
	m._iwall(o + Vector3(0, 47, -34), Vector3(16.0, 10, 1.5), wcol, "marble")        # gallery door, top strip
	m._iwall(o + Vector3(-30.75, 26, -34), Vector3(8.5, 52, 1.5), wcol, "marble")  # left edge
	m._iwall(o + Vector3(30.75, 26, -34), Vector3(8.5, 52, 1.5), wcol, "marble")   # right edge
	m._iwall(o + Vector3(-22, 33.5, -34), Vector3(9.0, 37, 1.5), wcol, "marble")   # lintel over left arch
	m._iwall(o + Vector3(22, 33.5, -34), Vector3(9.0, 37, 1.5), wcol, "marble")    # lintel over right arch
	# side walls, SEGMENTED in three layers (owner 2026-07-12: the upper story
	# wraps around BOTH wings, so the y 33..49 band gains three ARCH OPENINGS
	# per side — swim from the hall straight into the wing galleries):
	#   lower  y 0..33  — downstairs wall with the music/bedroom doorway (z -21..-11)
	#   upper  y 33..49 — arcade: arches at z -21..-11, -1..9 and 19..29
	#   crown  y 49..52 — solid band up to the ceiling
	var bal_gold := Color(0.95, 0.8, 0.35)
	for sgn in [-1.0, 1.0]:
		var sx: float = sgn * 35.0
		m._iwall(o + Vector3(sx, 16.5, 17.5), Vector3(1.5, 33, 57), scol, "marble")   # lower front (z -11..46)
		m._iwall(o + Vector3(sx, 16.5, -27.5), Vector3(1.5, 33, 13), scol, "marble")  # lower back (z -34..-21)
		m._iwall(o + Vector3(sx, 25.5, -16), Vector3(1.5, 15, 10), scol, "marble")    # lintel over the wing door
		m._iwall(o + Vector3(sx, 41, -27.5), Vector3(1.5, 16, 13), scol, "marble")    # arcade pier (z -34..-21)
		m._iwall(o + Vector3(sx, 41, -6), Vector3(1.5, 16, 10), scol, "marble")       # arcade pier (z -11..-1)
		m._iwall(o + Vector3(sx, 41, 14), Vector3(1.5, 16, 10), scol, "marble")       # arcade pier (z 9..19)
		m._iwall(o + Vector3(sx, 41, 37.5), Vector3(1.5, 16, 17.5), scol, "marble")   # arcade pier (z 29..46)
		m._iwall(o + Vector3(sx, 50.5, 6), Vector3(1.5, 3, 80), scol, "marble")       # crown band (y 49..52)
		# gold balustrade across each arch so the openings read as balconies
		for az in [-16.0, 4.0, 24.0]:
			m._l2_box(o + Vector3(sx, 34.6, az), Vector3(0.5, 0.5, 9.0), bal_gold, 0.2)
			for pz in [-3.0, 0.0, 3.0]:
				m._l2_box(o + Vector3(sx, 33.9, az + pz), Vector3(0.4, 1.6, 0.4), bal_gold, 0.15)
	m._l2_box(o + Vector3(0, 51, 6), Vector3(70, 1.5, 80), Color(0.85, 0.82, 0.9))      # ceiling (no collider; the hall zone caps height)
	# regal stained-glass panels behind the throne (the Mermaid Roshan glass now lives
	# on the castle's FRONT exterior — this is a plain coloured rose window for Huluu)
	m._panel_glass(o + Vector3(0, 23, -33.0), Vector3(0, 0, 0), 17.0, 24.0)
	# royal red-carpet staircase up to the throne dais
	for st in range(7):
		m._l2_box(o + Vector3(0, 1.5 + float(st) * 2.0, -10.0 - float(st) * 2.2), Vector3(16.0 - float(st) * 0.6, 2.0, 3.0), Color(0.8, 0.25, 0.3))
	# throne dais
	m._l2_box(o + Vector3(0, 15.0, -27.0), Vector3(14, 2.0, 6), Color(0.95, 0.85, 0.55), 0.2)
	# collision audit #2: the throne centerpiece was ghostly — the player swam
	# straight through the stairs/dais/throne. Solid up to y14 (dais underside);
	# the crown updraft still lifts her over the top from the front
	m._wall_solid(o + Vector3(0, 7.0, -21.5), Vector3(15, 14, 15), 0.8)
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
	# Princess Huluu on her throne — the full plushie treatment (rigged model,
	# tail swaying), no more flat quivering billboard
	if ResourceLoader.exists("res://assets/characters/huluu.glb"):
		var hn: Node3D = (load("res://assets/characters/huluu.glb") as PackedScene).instantiate()
		hn.scale = Vector3.ONE * 3.6
		hn.position = o + Vector3(0, 16.2, -27.0)
		hn.rotation.y = PI
		m.add_child(hn)
		m.game_nodes.append(hn)
		var hskel = m._find_skel(hn)
		if hskel != null:
			m.g["huluu_skel"] = hskel
	else:
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
			clmat.albedo_color = Color(0.96, 0.93, 0.98)
			clmat.roughness = 0.4
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
			sc.light_energy = 1.7
			sc.omni_range = 24.0
			sc.position = o + Vector3(cx * 0.86, 20.0, cz)
			m.add_child(sc)
			m.game_nodes.append(sc)
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
	var tcols := [Color(0.7, 0.2, 0.3), Color(0.25, 0.4, 0.75), Color(0.45, 0.3, 0.65), Color(0.2, 0.55, 0.45)]
	for ti in range(4):
		for sgn in [-1.0, 1.0]:
			var tap := MeshInstance3D.new()
			var tq := QuadMesh.new()
			tq.size = Vector2(7.0, 16.0)
			tap.mesh = tq
			var tm2 := StandardMaterial3D.new()
			tm2.albedo_color = tcols[ti]
			tm2.roughness = 1.0
			tm2.cull_mode = BaseMaterial3D.CULL_DISABLED
			tm2.emission_enabled = true
			tm2.emission = tcols[ti] * 0.2
			tap.material_override = tm2
			tap.position = o + Vector3(sgn * 34.0, 20.0, -24.0 + float(ti) * 16.0)
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
		chm.emission_energy_multiplier = 0.8
		ch.material_override = chm
		ch.position = o + Vector3(0, 30.0, chz)
		m.add_child(ch)
		m.game_nodes.append(ch)
		var chl := OmniLight3D.new()
		chl.light_color = Color(1.0, 0.85, 0.55)
		chl.light_energy = 2.2
		chl.omni_range = 30.0
		chl.position = o + Vector3(0, 28.0, chz)
		m.add_child(chl)
		m.game_nodes.append(chl)
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
		m.fade_walls.append({"node": fseg, "c": fseg.position, "h": (fseg.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	m._l2_box(br + Vector3(0, 33.0, 0), Vector3(52, 1.5, 22), Color(0.82, 0.79, 0.88))           # ceiling
	m._iwall(br + Vector3(0, 16, -10.5), Vector3(52, 34, 1.5), Color(0.93, 0.9, 0.95), "marble")          # back wall
	m._iwall(br + Vector3(-25.5, 16, 0), Vector3(1.5, 34, 22), Color(0.93, 0.9, 0.95), "marble")          # left wall
	m._iwall(br + Vector3(25.5, 16, 0), Vector3(1.5, 34, 22), Color(0.93, 0.9, 0.95), "marble")           # right wall
	# warm light + a soft red runner inside
	var brl := OmniLight3D.new(); brl.light_color = Color(1.0, 0.85, 0.6); brl.light_energy = 2.0; brl.omni_range = 34.0
	brl.position = br + Vector3(0, 20, 0); m.add_child(brl); m.game_nodes.append(brl)
	m._l2_box(br + Vector3(0, 1.0, 6.6), Vector3(10, 0.2, 10.8), Color(0.72, 0.16, 0.22))        # carpet from arch to the stand
	# a glowing royal treasure chest = the bonus trigger. It doubles as the
	# GOLDEN STAND sealing the undercroft's back stairwell: it pulses
	# invitingly and rumbles aside when Roshan gets close (see slide_stand).
	var chest = m._l2_box(br + Vector3(0, 3.0, -1.0), Vector3(7, 5, 4.5), Color(0.95, 0.78, 0.35), 0.6)
	chest.material_override.metallic = 0.6
	var chest_lid = m._l2_box(br + Vector3(0, 6.0, -1.0), Vector3(7.4, 1.4, 5.0), Color(0.8, 0.62, 0.25), 0.5)   # lid rim
	m.g["secret_door"] = chest.position
	m.g["stand_chest"] = chest
	m.g["stand_lid"] = chest_lid
	m.g["stand_open"] = false
	m.g["stand_armed"] = false   # arms once Roshan is >14 away (the moat hatch spawns right beside it)
	var ctw: Tween = chest.create_tween().set_loops()
	ctw.tween_property(chest.material_override, "emission_energy_multiplier", 1.7, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	ctw.tween_property(chest.material_override, "emission_energy_multiplier", 0.6, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	var sl2 := OmniLight3D.new(); sl2.light_color = Color(0.6, 0.95, 1.0); sl2.light_energy = 2.2; sl2.omni_range = 16.0
	sl2.position = chest.position + Vector3(0, 4, 0); m.add_child(sl2); m.game_nodes.append(sl2)
	# Daddy mermaid lives in the secret room (his real recorded voice greets Roshan)
	var daddy := Sprite3D.new()
	daddy.texture = m._cutout_tex("daddy")
	daddy.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	daddy.pixel_size = 0.0066
	daddy.position = br + Vector3(10, 8, -3)
	m.add_child(daddy); m.game_nodes.append(daddy)
	var dlt := OmniLight3D.new(); dlt.light_color = Color(1.0, 0.9, 0.8); dlt.light_energy = 1.8; dlt.omni_range = 22.0
	dlt.position = daddy.position + Vector3(0, 2, 5); m.add_child(dlt); m.game_nodes.append(dlt)
	var sl := OmniLight3D.new()
	sl.light_color = Color(0.5, 0.9, 1.0)
	sl.light_energy = 1.5
	sl.omni_range = 14.0
	sl.position = o + Vector3(-22, 7, -33.0)   # invite glow at the left archway
	m.add_child(sl)
	m.game_nodes.append(sl)
	var sl3 := OmniLight3D.new()
	sl3.light_color = Color(0.5, 0.9, 1.0)
	sl3.light_energy = 1.5
	sl3.omni_range = 14.0
	sl3.position = o + Vector3(22, 7, -33.0)   # invite glow at the right archway
	m.add_child(sl3)
	m.game_nodes.append(sl3)
	var slab := Label3D.new()
	slab.text = "\u2728 Daddy Mermaid \u2728"
	slab.font_size = 40
	slab.pixel_size = 0.02
	slab.outline_size = 10
	slab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	slab.position = m.g["secret_door"] + Vector3(0, 7.0, 0)
	m.add_child(slab)
	m.game_nodes.append(slab)
	m.g["stand_label"] = slab
	# (the royal loo lives down in the basement wing — see build_basement_wing)
	# just TWO framed memories on the side walls (fewer pictures)
	# (the swim-through xylophone now lives in the dedicated MUSIC ROOM off the left wall \u2014 see _build_castle_music_room)
	# ---------- CRAFTING STUDIO easel (color your own fish!) ----------
	var _easel = m._l2_box(o + Vector3(31.0, 7.0, 2.0), Vector3(0.6, 11.0, 8.0), Color(0.55, 0.4, 0.26))
	m._wall_solid(o + Vector3(31.0, 7.0, 2.0), Vector3(0.6, 11.0, 8.0), 0.5)
	var canvas = m._l2_box(o + Vector3(30.4, 9.0, 2.0), Vector3(0.4, 7.0, 6.0), Color(0.97, 0.96, 0.92), 0.1)
	m._mg_noop_ref(canvas)
	var craft_fish_icon := Sprite3D.new()
	craft_fish_icon.texture = load("res://assets/mg/fish_line.png")
	craft_fish_icon.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	craft_fish_icon.pixel_size = 0.012
	craft_fish_icon.position = o + Vector3(29.9, 9.0, 2.0)
	m.add_child(craft_fish_icon); m.game_nodes.append(craft_fish_icon)
	var csign := Label3D.new()
	csign.text = "\U0001f3a8 Crafting Studio"
	csign.font_size = 56; csign.pixel_size = 0.03; csign.outline_size = 12
	csign.modulate = Color(0.95, 0.9, 1.0); csign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	csign.position = o + Vector3(29.0, 14.0, 2.0)
	m.add_child(csign); m.game_nodes.append(csign)
	m.g["craft_easel"] = o + Vector3(29.0, 7.0, 2.0)
	# hanging chandeliers
	for cz in [-14.0, 8.0]:
		var ch := OmniLight3D.new()
		ch.light_color = Color(1.0, 0.8, 0.5)
		ch.light_energy = 2.0
		ch.omni_range = 26.0
		ch.position = o + Vector3(0, 26, cz)
		m.add_child(ch)
		m.game_nodes.append(ch)
		var bulb := MeshInstance3D.new()
		var bs := SphereMesh.new()
		bs.radius = 0.8
		bs.height = 1.6
		bulb.mesh = bs
		var bm := StandardMaterial3D.new()
		bm.emission_enabled = true
		bm.emission = Color(1.0, 0.85, 0.5)
		bm.emission_energy_multiplier = 3.0
		bulb.material_override = bm
		bulb.position = ch.position
		m.add_child(bulb)
		m.game_nodes.append(bulb)
	# the crown Star atop the throne — the goal
	var crown := Label3D.new()
	crown.text = "\u2605"
	crown.font_size = 340
	crown.modulate = Color(1.0, 0.9, 0.3)
	crown.outline_size = 34
	crown.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	crown.position = o + Vector3(0, 24.0, -28.0)
	m.add_child(crown)
	m.game_nodes.append(crown)
	m.l2_stars = [{"node": crown, "got": false}]
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
	var exlab := Label3D.new()
	exlab.text = "\u2190 leave the castle"
	exlab.font_size = 60
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
	deck.material_override = m._up_mat("marble", 0.05, Color(0.9, 0.87, 0.96))
	for px in range(-6, 7):
		m._l2_box(o + Vector3(float(px) * 4.0, 34.6, -21.4), Vector3(0.5, 3.2, 0.5), gold, 0.2)
	m._l2_box(o + Vector3(0, 36.4, -21.4), Vector3(52, 0.5, 0.6), gold, 0.25)
	# twin marble stairs hugging the side walls up to the deck
	for sgn in [-1.0, 1.0]:
		for i in range(10):
			m._l2_box(o + Vector3(sgn * 30.5, 3.0 + float(i) * 3.0, -6.0 - float(i) * 2.1), Vector3(7.0, 0.9, 3.6), Color(0.93, 0.9, 0.95))
	# ---------- THE UPPER STORY (owner 2026-07-12): wraps around BOTH wings.
	# A full-width back block (z -36..-64, x -53..53) holds the enlarged Star
	# Chamber + Cloud Lounge; two long WING GALLERIES run above the music room
	# (left) and the bedroom/craft wing (right), z -36..18 — so upstairs rooms
	# extend on all three sides. Reached from the balcony gallery door OR by
	# swimming through the new hall arcade arches.
	var uf = m._l2_box(o + Vector3(0, 33.0, -50.0), Vector3(106, 1.2, 28), Color(0.9, 0.86, 0.94))
	uf.material_override = m._up_mat("flagstone", 0.05, Color(0.85, 0.8, 0.95))
	for wsgn in [-1.0, 1.0]:
		var wf = m._l2_box(o + Vector3(wsgn * 44.25, 33.0, -9.0), Vector3(17.5, 1.2, 54), Color(0.9, 0.86, 0.94))
		wf.material_override = m._up_mat("flagstone", 0.05, Color(0.85, 0.8, 0.95))
	m._iwall(o + Vector3(0, 41, -64), Vector3(106, 16, 1.5), wcol, "castle")      # far wall, full width
	m._iwall(o + Vector3(-53.5, 41, -22.6), Vector3(1.5, 16, 83), wcol, "castle") # left outer wall (z -64..18.75)
	m._iwall(o + Vector3(53.5, 41, -22.6), Vector3(1.5, 16, 83), wcol, "castle")  # right outer wall
	m._iwall(o + Vector3(-44.25, 41, 18.75), Vector3(18.5, 16, 1.5), wcol, "castle")  # left wing front wall
	m._iwall(o + Vector3(44.25, 41, 18.75), Vector3(18.5, 16, 1.5), wcol, "castle")   # right wing front wall
	m._iwall(o + Vector3(0, 41, -39.5), Vector3(1.5, 16, 7), wcol, "castle")    # divider, front seg
	m._iwall(o + Vector3(0, 41, -58.5), Vector3(1.5, 16, 11), wcol, "castle")   # divider, back seg (door z -43..-53)
	m._l2_box(o + Vector3(0, 49, -50), Vector3(106, 1.2, 28), Color(0.84, 0.8, 0.9))         # back-block ceiling
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
		var star := Label3D.new()
		star.text = "✦"
		star.font_size = 64 + (st % 3) * 28
		star.modulate = Color(1.0, 0.95, 0.6, 0.9)
		star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
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
	# ---------- the UNDERCROFT: stone basement under the front hall
	var shaft := Vector3(-24, 0, 30)
	for e in [Vector3(-5.5, 0, 0), Vector3(5.5, 0, 0)]:
		m._l2_box(o + shaft + e + Vector3(0, 0.9, 0), Vector3(0.9, 0.5, 11), gold, 0.3)
	for e2 in [Vector3(0, 0, -5.5), Vector3(0, 0, 5.5)]:
		m._l2_box(o + shaft + e2 + Vector3(0, 0.9, 0), Vector3(11, 0.5, 0.9), gold, 0.3)
	for i in range(8):
		m._l2_box(o + shaft + Vector3(0, -1.5 - float(i) * 2.1, -3.5 + float(i) * 1.0), Vector3(8.0, 0.8, 2.6), Color(0.62, 0.58, 0.66))
	var bf = m._l2_box(o + Vector3(0, -18.6, 24.0), Vector3(60, 1.2, 32), Color(0.6, 0.56, 0.64))
	bf.material_override = m._up_mat("cobble", 0.05, Color(0.75, 0.7, 0.8))
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
		{"rect": Rect2(-29, 25, 10, 10), "band": Vector2(-18.0, 3.5), "floor": -17.4},
		{"rect": Rect2(-6, -50, 12, 12), "band": Vector2(-18.0, -2.0), "floor": -17.4, "ceil": -2.8},
	]
	# The back stairwell starts SEALED under the golden stand: its band stops
	# below the hallway floor (nobody sinks in from above or pops up from
	# below) until slide_stand() opens the band up to the hallway. The seal's
	# ceil sits 0.8 BELOW the band top: at the band edge itself a fast upward
	# swim could cross the whole band in one frame and tunnel out.
	m.g["stand_zone"] = m.arena_zones[m.arena_zones.size() - 1]

func build_basement_wing(o: Vector3) -> void:
	# ============ THE BASEMENT WING (owner 2026-07-12) ============
	# The old 12-wide corridor grows into a proper basement: a 16-wide hallway
	# running from the undercroft (z +8) to the golden-stand stairs (z -44),
	# two pairs of side rooms (pantry / toy den / bubble bath / gem vault) and
	# the royal loo at the very bottom of the hallway beside the stair base.
	# Emissive dressing only — the OmniLight budget stays untouched. Vertical
	# physics comes from the three basement zone rects in build_expansion.
	var stone := Color(0.7, 0.66, 0.74)
	var gold := Color(0.95, 0.8, 0.35)
	# ---------- the hallway floor
	var cfl = m._l2_box(o + Vector3(0, -18.6, -18.0), Vector3(16, 1.2, 52), Color(0.6, 0.56, 0.64))
	cfl.material_override = m._up_mat("cobble", 0.05, Color(0.75, 0.7, 0.8))
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
		ewn.material_override = m._up_mat("castle", 0.045, stone)
		m.fade_walls.append({"node": ewn, "c": ewn.position, "h": (ewn.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	var ewl = m._l2_box(o + Vector3(0, -2.75, -44.0), Vector3(8.8, 4.5, 1.5), stone)
	ewl.material_override = m._up_mat("castle", 0.045, stone)
	m.fade_walls.append({"node": ewl, "c": ewl.position, "h": (ewl.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
	# warm lanterns alternate down the hallway (emissive boxes, no lights)
	for li2 in range(6):
		m._l2_box(o + Vector3(-7.2 + float(li2 % 2) * 14.4, -12.0, -40.0 + float(li2) * 9.0), Vector3(0.6, 1.4, 1.0), Color(1.0, 0.8, 0.45), 3.2)
	# ---------- THE ROYAL LOO at the very bottom of the hallway, beside the
	# stair base, facing whoever comes down the golden-stand stairs
	build_toilet(o + Vector3(-5.8, -18.0, -41.5))
	# ---------- four side rooms off the hallway ----------
	var rooms := [
		{"c": Vector3(-17, 0, -2), "name": "✨ Pantry ✨", "tint": Color(0.85, 0.78, 0.62)},
		{"c": Vector3(17, 0, -2), "name": "✨ Toy Den ✨", "tint": Color(0.78, 0.72, 0.85)},
		{"c": Vector3(-17, 0, -28), "name": "✨ Bubble Bath ✨", "tint": Color(0.7, 0.8, 0.88)},
		{"c": Vector3(17, 0, -28), "name": "✨ Gem Vault ✨", "tint": Color(0.72, 0.68, 0.8)},
	]
	for rd in rooms:
		var rc: Vector3 = rd["c"]
		var sx2: float = signf(rc.x)
		var rfl = m._l2_box(o + rc + Vector3(0, -18.6, 0), Vector3(18, 1.2, 16), Color(0.6, 0.56, 0.64))
		rfl.material_override = m._up_mat("cobble", 0.05, rd["tint"])
		var rcl = m._l2_box(o + rc + Vector3(0, -0.9, 0), Vector3(19, 0.8, 17), Color(0.55, 0.52, 0.6))   # ceiling
		m.fade_walls.append({"node": rcl, "c": rcl.position, "h": (rcl.mesh as BoxMesh).size * 0.5, "base_a": 1.0, "a": 1.0})
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
	# TOY DEN: pillow pile, beach ball, toy blocks
	var tc: Vector3 = o + Vector3(17, 0, -2)
	for pi2 in range(5):
		m._l2_box(tc + Vector3(-3.0 + float(pi2 % 3) * 4.0, -16.6 + float(pi2 / 3) * 1.4, 3.0 - float(pi2 % 2) * 2.0), Vector3(3.6, 1.5, 3.6), Color(1.0, 0.75, 0.85) if pi2 % 2 == 0 else Color(0.75, 0.85, 1.0))
	var ball := MeshInstance3D.new()
	var bsm := SphereMesh.new(); bsm.radius = 1.6; bsm.height = 3.2
	ball.mesh = bsm
	ball.material_override = m._soft_mat(Color(1.0, 0.55, 0.3), 0.3)
	ball.position = tc + Vector3(4.5, -15.8, -4.0)
	m.add_child(ball); m.game_nodes.append(ball)
	for tb in range(3):
		m._l2_box(tc + Vector3(-5.0 + float(tb) * 2.2, -16.6, -5.0), Vector3(1.8, 1.8, 1.8), [Color(0.95, 0.5, 0.5), Color(0.5, 0.8, 0.95), Color(0.95, 0.85, 0.4)][tb], 0.3)
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
	# GEM VAULT: glow crystals, gold piles, a little chest
	var gc: Vector3 = o + Vector3(17, 0, -28)
	for ci2 in range(4):
		var cr = m._l2_box(gc + Vector3(-4.0 + float(ci2) * 2.8, -16.4 + float(ci2 % 2) * 0.4, -5.0), Vector3(1.0, 2.6 + float(ci2 % 3) * 0.8, 1.0), Color(0.55, 0.9, 1.0), 1.4)
		cr.rotation_degrees = Vector3(float(ci2) * 8.0 - 12.0, 0, 14.0 - float(ci2) * 8.0)
	for gp in range(5):
		m._l2_box(gc + Vector3(3.0 + float(gp % 3) * 2.6, -16.9 + float(gp / 3) * 1.0, 3.0 + float(gp % 2) * 2.0), Vector3(2.2, 1.0, 2.2), gold, 0.5)
	var vchest = m._l2_box(gc + Vector3(6.0, -16.2, -3.0), Vector3(3.2, 2.6, 2.2), Color(0.95, 0.78, 0.35), 0.5)
	vchest.material_override.metallic = 0.6


func build_music_room(o: Vector3) -> void:
	# Roomy music hall off the LEFT wall (doorway x=-35, z=-16).
	# Footprint x:-52..-35 (width 17), z:-24..+14 (depth 38) — a long room so the
	# xylophone has space. Interior corners stay inside the dome (r<58).
	var mo: Vector3 = o + Vector3(-43.5, 0, -5)           # room centre
	var wall := Color(0.86, 0.88, 0.98)                  # cool lilac plaster
	# flr + ceiling (no colliders — flr clamp / arena_ceil handle vertical)
	var mfloor = m._l2_box(mo + Vector3(0, 0.4, 0), Vector3(19, 1.0, 40), Color(0.5, 0.45, 0.7))
	mfloor.material_override.roughness = 0.9
	m._l2_box(mo + Vector3(0, 33.0, 0), Vector3(19, 1.5, 40), Color(0.8, 0.82, 0.92))
	# enclosing walls (the right/hall side is the segmented hall wall already built)
	m._iwall(mo + Vector3(-9.25, 16, 0), Vector3(1.5, 34, 40), wall, "marble")       # far wall (x=-52.75)
	m._iwall(mo + Vector3(0, 16, -19.75), Vector3(19, 34, 1.5), wall, "marble")      # back wall (z=-24.75)
	m._iwall(mo + Vector3(0, 16, 19.75), Vector3(19, 34, 1.5), wall, "marble")       # front wall (z=+14.75)
	# gold doorway frame around the opening in the hall wall
	for dz in [-21.0, -11.0]:
		m._l2_box(o + Vector3(-35, 8, dz), Vector3(1.2, 16, 1.2), Color(0.85, 0.72, 0.45), 0.15)
	# soft rug by the entrance
	var rug = m._l2_box(mo + Vector3(3.0, 0.95, -11.0), Vector3(9, 0.1, 8), Color(0.35, 0.3, 0.6))
	rug.material_override = m._up_mat("fabric", 0.14, Color(0.5, 0.45, 0.75))   # woven rug
	# ---------- the swim-through xylophone (a free-play music toy) ----------
	# bells run in a spaced row down the length of the room (no overlap)
	var bellcols := [Color(1, 0.3, 0.3), Color(1, 0.6, 0.2), Color(1, 0.9, 0.3), Color(0.3, 0.85, 0.4), Color(0.3, 0.6, 1.0), Color(0.5, 0.4, 0.9), Color(0.95, 0.4, 0.8)]
	var bellpitch := [0.5, 0.56, 0.63, 0.75, 0.84, 0.94, 1.0]   # warmer, lower octave — gentler for little ears
	m.g["bells"] = []
	for bi in range(7):
		var bell := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(2.6, 9.0 - float(bi) * 0.5, 2.6)
		bell.mesh = bm
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = bellcols[bi]
		bmat.emission_enabled = true
		bmat.emission = bellcols[bi]
		bmat.emission_energy_multiplier = 0.7
		bmat.metallic = 0.4
		bmat.roughness = 0.3
		bell.material_override = bmat
		bell.position = mo + Vector3(0.0, 5.0, -13.5 + float(bi) * 4.5)   # spaced 4.5 along z
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
	ssl.light_energy = 1.6
	ssl.omni_range = 9.0
	ssl.position = song_star.position
	m.add_child(ssl)
	m.game_nodes.append(ssl)
	m.g["song_star"] = song_star.position
	m.g["bellgame"] = {"state": "idle", "seq": [], "i": 0, "t": 0.0, "round": 0, "cool": 0.0}
	# two warm fill lights down the length
	for lz in [-12.0, 10.0]:
		var ml := OmniLight3D.new()
		ml.light_color = Color(0.85, 0.85, 1.0); ml.light_energy = 1.7; ml.omni_range = 28.0
		ml.position = mo + Vector3(0, 22, lz); m.add_child(ml); m.game_nodes.append(ml)
	# glowing windows on the far wall
	for wz in [-10.0, 10.0]:
		var win = m._l2_box(mo + Vector3(-9.1, 20, wz), Vector3(0.4, 7, 6), Color(0.7, 0.8, 1.0), 0.8)
		win.material_override.emission_energy_multiplier = 1.2
	# sign over the doorway
	var msign := Label3D.new()
	msign.text = "♪ Music Room ♪"
	msign.font_size = 56; msign.pixel_size = 0.028; msign.outline_size = 12
	msign.modulate = Color(0.85, 0.9, 1.0); msign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	msign.position = o + Vector3(-35, 20.0, -16); m.add_child(msign); m.game_nodes.append(msign)
	# cool invite glow at the doorway
	var il := OmniLight3D.new()
	il.light_color = Color(0.6, 0.7, 1.0); il.light_energy = 1.6; il.omni_range = 14.0
	il.position = o + Vector3(-34, 7, -16); m.add_child(il); m.game_nodes.append(il)


func build_bedroom(o: Vector3) -> void:
	# Roomy royal bedroom off the right-wall doorway (x=35, z=-16).
	# Footprint x:35..57, z:-28..-6 (22x22) — corners r<65, inside the dome (66).
	var bo: Vector3 = o + Vector3(46, 0, -17)            # room centre
	var wall := Color(0.96, 0.9, 0.86)                   # warm rosy plaster
	# flr + ceiling (no colliders — handled by the flr clamp / arena_ceil)
	var bfloor = m._l2_box(bo + Vector3(0, 0.4, 0), Vector3(22, 1.0, 22), Color(0.78, 0.6, 0.5))
	bfloor.material_override.roughness = 0.9
	m._l2_box(bo + Vector3(0, 33.0, 0), Vector3(22, 1.5, 22), Color(0.9, 0.84, 0.82))
	# enclosing walls (the left/hall side is the segmented hall wall already built)
	m._iwall(bo + Vector3(11, 16, 0), Vector3(1.5, 34, 22), wall, "marble")          # far wall (x=57)
	m._iwall(bo + Vector3(0, 16, -11), Vector3(22, 34, 1.5), wall, "marble")         # back wall (z=-28)
	m._iwall(bo + Vector3(0, 16, 11), Vector3(22, 34, 1.5), wall, "marble")          # front wall (z=-6)
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
	bedsign.text = "zZz  snuggle in!"
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
	lmat.emission_enabled = true; lmat.emission = Color(1.0, 0.82, 0.5); lmat.emission_energy_multiplier = 3.0
	lampbulb.material_override = lmat
	lampbulb.position = Vector3(bcx - 6.5, o.y + 4.6, bcz - 5.0)
	m.add_child(lampbulb); m.game_nodes.append(lampbulb)
	var lamp := OmniLight3D.new()
	lamp.light_color = Color(1.0, 0.82, 0.55); lamp.light_energy = 2.0; lamp.omni_range = 18.0
	lamp.position = lampbulb.position; m.add_child(lamp); m.game_nodes.append(lamp)
	# big soft rug in the middle of the room
	var rug = m._l2_box(bo + Vector3(-5.0, 0.95, 3.0), Vector3(10, 0.1, 8), Color(0.7, 0.3, 0.4))
	rug.material_override = m._up_mat("fabric", 0.14, Color(0.8, 0.4, 0.5))   # woven rug
	# toy chest by the far wall (decor)
	var chest = m._l2_box(bo + Vector3(8.5, 1.6, 6.0), Vector3(3.4, 2.4, 2.4), Color(0.75, 0.5, 0.3))
	chest.material_override.roughness = 0.85
	m._wall_solid(bo + Vector3(8.5, 1.6, 6.0), Vector3(3.4, 2.4, 2.4), 0.4)
	m._l2_box(bo + Vector3(8.5, 3.0, 6.0), Vector3(3.6, 0.5, 2.6), Color(0.55, 0.34, 0.2))
	# ---------- DRESS-UP VANITY: a wardrobe + mirror (swim up to pick your outfit) ----------
	var vpos: Vector3 = bo + Vector3(-6.0, 0, 9.0)        # against the front wall, facing the room
	var wardrobe = m._l2_box(vpos + Vector3(0, 7.0, 1.0), Vector3(7, 14, 1.6), Color(0.55, 0.34, 0.22))
	wardrobe.material_override.roughness = 0.8
	var mirror = m._l2_box(vpos + Vector3(0, 7.5, 0.1), Vector3(4.5, 9.0, 0.2), Color(0.7, 0.92, 1.0), 0.6)  # glowing mirror glass
	mirror.material_override.metallic = 0.9
	mirror.material_override.roughness = 0.05
	for fx in [-2.6, 2.6]:                                 # gold mirror frame posts
		m._l2_box(vpos + Vector3(fx, 7.5, 0.2), Vector3(0.6, 9.5, 0.5), Color(0.95, 0.8, 0.4), 0.2)
	m._l2_box(vpos + Vector3(0, 12.4, 0.2), Vector3(5.7, 0.6, 0.5), Color(0.95, 0.8, 0.4), 0.2)   # frame top
	m._wall_solid(vpos + Vector3(0, 7.0, 1.0), Vector3(7, 14, 1.6))   # the wardrobe is solid
	var vsign := Label3D.new()
	vsign.text = "\U0001f457 Dress Up!"
	vsign.font_size = 48; vsign.pixel_size = 0.028; vsign.outline_size = 12
	vsign.modulate = Color(1.0, 0.8, 0.95); vsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	vsign.position = vpos + Vector3(0, 13.6, 0); m.add_child(vsign); m.game_nodes.append(vsign)
	var vl := OmniLight3D.new()
	vl.light_color = Color(1.0, 0.85, 0.95); vl.light_energy = 1.6; vl.omni_range = 14.0
	vl.position = vpos + Vector3(0, 8, -2); m.add_child(vl); m.game_nodes.append(vl)
	m.g["wardrobe"] = vpos + Vector3(0, 6, -2)
	# fill light so the room reads warm
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.88, 0.78); bl.light_energy = 2.0; bl.omni_range = 36.0
	bl.position = bo + Vector3(0, 22, 0); m.add_child(bl); m.game_nodes.append(bl)
	# glowing windows on the far and back walls for ambiance
	var win = m._l2_box(bo + Vector3(10.4, 20, 0), Vector3(0.4, 7, 6), Color(0.6, 0.85, 1.0), 0.8)
	win.material_override.emission_energy_multiplier = 1.2
	var win2 = m._l2_box(bo + Vector3(-4.0, 20, -10.4), Vector3(6, 7, 0.4), Color(0.6, 0.85, 1.0), 0.8)
	win2.material_override.emission_energy_multiplier = 1.2
	# label over the doorway
	var blab := Label3D.new()
	blab.text = "\U0001f6cf️ Bedroom"
	blab.font_size = 56; blab.pixel_size = 0.03; blab.outline_size = 12
	blab.modulate = Color(1.0, 0.9, 0.85)
	blab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	blab.position = o + Vector3(35, 20.0, -16)
	m.add_child(blab); m.game_nodes.append(blab)
	# warm invite glow at the doorway
	var il := OmniLight3D.new()
	il.light_color = Color(1.0, 0.8, 0.6); il.light_energy = 1.6; il.omni_range = 14.0
	il.position = o + Vector3(34, 7, -16); m.add_child(il); m.game_nodes.append(il)


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
	# the little loo toots a bubbly parp when Roshan swims up to it (re-arms
	# when she swims away)
	if m.g.has("toilet"):
		var td: Dictionary = m.g["toilet"]
		var tpp: Vector3 = td["pos"]
		if tpp.distance_to(ppos) > 7.5:
			td["armed"] = true
		elif bool(td.get("armed", false)) and tpp.distance_to(ppos) < 4.5:
			td["armed"] = false
			(td["player"] as AudioStreamPlayer).play()
			m._sparkle_burst(tpp + Vector3(0, 2.0, 0), Color(0.6, 0.9, 1.0))
	# leave the castle from the entrance
	if m.g.has("hall_exit") and float(m.g["t"]) > 2.5:
		var hx: Vector3 = m.g["hall_exit"]
		if hx.distance_to(ppos) > 14.0:
			m.g["hall_exit_armed"] = true
		if bool(m.g.get("hall_exit_armed", false)) and hx.distance_to(ppos) < 6.0:
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
	var crown: Label3D = m.l2_stars[0]["node"]
	crown.rotate_y(delta * 1.4)
	crown.position.y += sin(float(m.g["t"]) * 2.0) * 0.02
	# GENTLE STAIR HELPER (not a black hole): only a soft updraft when the player is in
	# FRONT of the throne and below the crown. No far-reaching horizontal pull, so the
	# back room behind the throne stays reachable. Finishing requires actually touching the crown.
	var d: float = crown.position.distance_to(ppos)
	var in_front: bool = ppos.z > crown.position.z + 3.0
	if in_front and d < 16.0 and ppos.y < crown.position.y - 1.0:
		m.player.position = m.player.position.lerp(crown.position, minf(0.16, delta * 0.5))
		m.player.vel.y = maxf(m.player.vel.y, 0.0)
	if d < 5.0:
		m._finish_level2()

