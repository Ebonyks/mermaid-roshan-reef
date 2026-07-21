class_name CourtyardTrain
extends RefCounted
# The COURTYARD TRAIN: a storybook ride circling Princess Huluu's castle in
# the Sky Lagoon. Its five authored bodies and shell-canopy station come from
# the unified Sky Lagoon quality kit; the lightweight runtime chassis keeps the
# proven wheel animation, smoke, ride anchors, and moving collision contract.
# Phase 7 satellite: logic only, ALL state lives on main in m.g["train"] and
# the seat toys in m.g["toys"].
#
# Layout (owner 2026-07-14: "much larger"): a GRAND TOUR ring of track,
# radius 191.5 about local (0,-3.5), circling the whole courtyard — over
# both hill summits (railhead peaks ~14.6, a little mountain railway),
# across each river mouth on a low causeway bridge (the track rides at
# bank level + a gentle hump, skimming above the water), and around the
# NORTH END of the grand path behind the gatehouse, so the loop never
# enters the path corridor at all (the old viaduct is gone) and never
# blocks the route a 4yo (or the audit bot) swims to the castle. Offline
# sweep: 9.3 units min clearance to every deterministic solid, max
# origin-distance 195 (island rim slope starts at 205).
#
# Consist (front to back): puffing engine, coal tender, an open-sided
# passenger coach with a bench INSIDE for Roshan, an open-top gondola with a
# cushion, and a caboose with an open back balcony — three places she can
# ride, all through the existing playground play-moment system.
#
# Hop on / hop off ANY TIME (owner 2026-07-14): boarding is a wide 9-unit
# proximity plop (moving or parked, station optional), the ride never
# times out, and she leaves whenever she chooses — a jump press, or the
# swim stick held for a beat, pops her off with a giggle (short 2s seat
# cooldown so she can hop right back on). Headless probes see no input,
# so they can neither board nor dismount by accident.
#
# Clipping contract (owner request): the corridor is kept clear at build
# time (tree/undergrowth spawning skips the track band, sky_lagoon.gd), the
# cars carry moving colliders so Roshan can never swim through the train,
# and a runtime guard hides the whole train the moment any car would
# intersect terrain or a pre-existing solid — including whenever the game
# leaves the courtyard phase (castle hall) — so it can never be seen
# clipping through anything.

var m: ReefMain

const RING_CX := 0.0          # grand-tour ring centre (local, island middle)
const RING_CZ := -3.5
const RING_R := 191.5         # hugs the whole courtyard; origin-dist tops out at 195
const RAIL_LIFT := 0.55       # railhead above the terrain
const CAR_SOLID_R := 3.1      # moving-collider radius per bogie point
const CAR_SOLID_H := 10.0     # collider top above the railhead (clears the coach roof)
const STATION_A := 2.1        # station bearing on the ring (flat southeast meadow)
const DWELL_T := 8.0          # station stop, seconds
const GUARD_DT := 0.25        # clip-guard cadence, seconds
const BOARD_RAD := 9.0        # hop-on proximity (toys default 6.5)
const SPD_MAX := 12.0         # cruise speed (owner 2026-07-14: 1.5x the original 8)
const LAGOON_TRAIN_KIT_ROOT := "res://assets/sky_lagoon/lagoon_kit/"


func _init(main: ReefMain) -> void:
	m = main


# ---------------- track geometry ----------------

func _ring_r(a: float) -> float:
	# variable ring radius: a broad WEST-side sweep around the whole Alpine
	# corner (the 70-tall mountain baked into _lagoon_local at -135,-165
	# r66, the three chalets, decorated tree, pines, snowman and cairn
	# trail — master 2026-07-14 composed them beyond the OLD radius-78
	# corridor). The ring ducks to ~151.5 across the mountain's foot,
	# passes north of chalet row A/B/C, and eases back out along the moat
	# constraint (castle-distance ≥ 68; the moat band ends at 64) while
	# clearing the secret hatch at (0,-175). East/south bearings need no
	# tuck at all now. Every number is swept offline against every solid
	# and visual prop before it ships.
	var aw: float = wrapf(a, -PI, PI)
	if aw >= 0.0:
		return RING_R
	var b: float = -aw
	return RING_R - 40.0 * (smoothstep(2.02, 2.35, b) - smoothstep(2.66, 2.98, b))


func _track_h(a: float) -> float:
	# local railhead height at ring bearing a: the terrain, with the river
	# carve added BACK (the track crosses each channel at bank level, like
	# a causeway) plus a gentle bridge hump so the deck skirt always clears
	# the water surface. Hills are ridden as-is — that's the fun part.
	var r: float = _ring_r(a)
	var lx: float = RING_CX + sin(a) * r
	var lz: float = RING_CZ + cos(a) * r
	var dip: float = m._lagoon_river_dip(lx, lz)
	return m._lagoon_local(lx, lz) + dip + minf(1.2, dip * 0.25) + RAIL_LIFT


func _track_pt(a: float) -> Vector3:
	var r: float = _ring_r(a)
	return Vector3(RING_CX + sin(a) * r, _track_h(a), RING_CZ + cos(a) * r)


func _track_perp(a: float) -> Vector3:
	# horizontal unit normal to the actual path (finite difference, NOT the
	# radial — in the village tuck the radius changes fast enough that the
	# radial would skew the ribbon and ties by up to ~30 degrees)
	var t: Vector3 = _track_pt(a + 0.004) - _track_pt(a - 0.004)
	t.y = 0.0
	t = t.normalized() if t.length() > 0.0001 else Vector3(cos(a), 0, -sin(a))
	return Vector3(-t.z, 0, t.x)


# ---------------- build ----------------

func _build_train(o: Vector3) -> void:
	# clip-guard snapshot: everything solid that exists BEFORE the train —
	# trees, lamps, towers, gatehouse. The track's own piers are added after
	# this so the viaduct never trips its own guard.
	var static_solids: Array = m.arena_solids.duplicate()
	_build_track(o)
	_build_station(o)
	# ----- the consist: [label, colour, length, wheelbase, s-offset behind engine] -----
	var cars: Array = []
	var engine: Node3D = _build_engine(o)
	cars.append({"node": engine, "off": 0.0, "wb": 6.5, "axles": engine.get_meta("axles"),
		"wr": 1.3, "rods": engine.get_meta("rods"), "solid_z": [-3.0, 3.0], "solids": []})
	var tender: Node3D = _build_tender(o)
	cars.append({"node": tender, "off": 9.5, "wb": 5.0, "axles": tender.get_meta("axles"),
		"wr": 0.9, "rods": [], "solid_z": [-1.8, 1.8], "solids": []})
	var coach: Node3D = _build_coach(o)
	cars.append({"node": coach, "off": 18.0, "wb": 5.0, "axles": coach.get_meta("axles"),
		"wr": 0.9, "rods": [], "solid_z": [-2.4, 2.4], "solids": []})
	var gondola: Node3D = _build_gondola(o)
	cars.append({"node": gondola, "off": 27.3, "wb": 5.0, "axles": gondola.get_meta("axles"),
		"wr": 0.9, "rods": [], "solid_z": [-2.2, 2.2], "solids": []})
	var caboose: Node3D = _build_caboose(o)
	cars.append({"node": caboose, "off": 36.2, "wb": 5.0, "axles": caboose.get_meta("axles"),
		"wr": 0.9, "rods": [], "solid_z": [-2.2, 2.2], "solids": []})
	# moving colliders: two y-gated cylinders per car so Roshan slides along
	# the train instead of swimming through it (updated every frame)
	for car: Dictionary in cars:
		for _sz: float in (car["solid_z"] as Array):
			m.arena_solids.append({"box": false, "x": 0.0, "z": 0.0, "r": CAR_SOLID_R,
				"y0": -9000.0, "y1": -9000.0})
			(car["solids"] as Array).append(m.arena_solids.back())
	# ----- ride seats, through the playground play-moment system -----
	# [kind, car index, seat offset in car space]. dur is effectively
	# forever — she rides until SHE hops off (jump, or stick held a beat)
	var seat_rows: Array = [
		["train_cabin", 2, Vector3(0.0, 4.5, -1.2)],   # bench INSIDE the coach
		["train_deck", 3, Vector3(0.0, 4.25, 0.0)],    # open-top gondola cushion
		["train_deck", 4, Vector3(0.0, 3.5, -2.9)],    # caboose back balcony
	]
	if not m.g.has("toys"):
		m.g["toys"] = []
	var seats: Array = []
	for row: Array in seat_rows:
		var car: Dictionary = cars[int(row[1])]
		var seat := {"kind": String(row[0]), "anchor": o, "base": o,
			"fwd": Vector3.FORWARD, "left": Vector3.LEFT, "tgt": 6.0,
			"node": car["node"], "seat": row[2], "cool": 4.0, "dur": 9999.0,
			"rad": BOARD_RAD}
		(m.g["toys"] as Array).append(seat)
		seats.append(seat)
	m.g["train"] = {"o": o, "cars": cars, "seats": seats, "s": STATION_A * RING_R,
		"spd": 0.0, "spd_max": SPD_MAX, "state": "dwell", "dwell": DWELL_T, "dwells": 0,
		"hidden": false, "guard_t": 0.0, "static": static_solids}
	_tick_train(0.0, m.player.position if m.player != null else o)


func _build_track(o: Vector3) -> void:
	# ballast/deck ribbon with side skirts, two navy rails, wooden ties —
	# three cheap SurfaceTool/MultiMesh nodes for the whole ring. The skirt
	# is shallow (1.2) so the causeway deck skims ABOVE the river surface
	# at the crossings instead of walling the channel (fish swim under it).
	_ring_ribbon(o, 0.0, 2.7, -0.45, 1.2, Color(0.78, 0.68, 0.52))
	_ring_ribbon(o, -1.55, 0.17, 0.30, 0.6, Color(0.30, 0.28, 0.50))
	_ring_ribbon(o, 1.55, 0.17, 0.30, 0.6, Color(0.30, 0.28, 0.50))
	var ties := MultiMeshInstance3D.new()
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	var tie_mesh: Mesh = _mesh_from_authored_scene("lagoon_track_tie")
	if tie_mesh == null:
		var fallback_tie := BoxMesh.new()
		fallback_tie.size = Vector3(4.6, 0.2, 1.1)
		fallback_tie.material = _train_mat(Color(0.50, 0.36, 0.22))
		tie_mesh = fallback_tie
	mm.mesh = tie_mesh
	var tie_n := 240
	mm.instance_count = tie_n
	for i in range(tie_n):
		var a: float = float(i) / float(tie_n) * TAU
		var p: Vector3 = _track_pt(a) + Vector3(0, -0.68, 0)
		var perp: Vector3 = _track_perp(a)
		# right-handed basis (perp x UP = this z), else the box mirrors
		mm.set_instance_transform(i, Transform3D(Basis(perp, Vector3.UP, Vector3(-perp.z, 0, perp.x)), p))
	ties.multimesh = mm
	ties.position = o
	m.add_child(ties)
	m.game_nodes.append(ties)
	var counts: Dictionary = m.g.get("lagoon_art_counts", {})
	counts["lagoon_track_tie"] = tie_n
	m.g["lagoon_art_counts"] = counts


func _ring_ribbon(o: Vector3, lat: float, half_w: float, y_off: float, skirt: float, col: Color) -> void:
	# closed ribbon following the ring at lateral offset `lat`: a flat top
	# strip plus two vertical skirts so the raised viaduct reads solid from
	# the side (the same trick the rivers use to hug their banks)
	var n := 360
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in range(n):
		var a0: float = float(i) / float(n) * TAU
		var a1: float = float(i + 1) / float(n) * TAU
		var pts: Array = []
		for a: float in [a0, a1]:
			var c: Vector3 = _track_pt(a)
			var perp: Vector3 = _track_perp(a)
			pts.append(c + perp * (lat - half_w) + Vector3(0, y_off, 0))
			pts.append(c + perp * (lat + half_w) + Vector3(0, y_off, 0))
		var i0: Vector3 = pts[0]
		var o0: Vector3 = pts[1]
		var i1: Vector3 = pts[2]
		var o1: Vector3 = pts[3]
		var pn: Vector3 = _track_perp(a0)
		_quad(st, i0, o0, o1, i1, Vector3.UP)             # top
		var drop := Vector3(0, -skirt, 0)
		_quad(st, i0 + drop, i0, i1, i1 + drop, -pn)      # inner skirt
		_quad(st, o0, o0 + drop, o1 + drop, o1, pn)       # outer skirt
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = _train_mat(col)
	mi.position = o
	m.add_child(mi)
	m.game_nodes.append(mi)


func _quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3, nrm: Vector3) -> void:
	# clockwise front-face winding (matches the terrain builder)
	for v: Vector3 in [a, c, b, a, d, c]:
		st.set_normal(nrm)
		st.add_vertex(v)


func _build_station(o: Vector3) -> void:
	# An authored shell-roof station replaces the primitive post-and-slab stop.
	# It remains low and NON-solid so nobody can ever get pinched by it.
	var radial := Vector3(sin(STATION_A), 0, cos(STATION_A))
	var c: Vector3 = Vector3(RING_CX, 0, RING_CZ) + radial * (_ring_r(STATION_A) + 6.5)
	c.y = m._lagoon_local(c.x, c.z)
	var station: Node3D = m._art35_prop(
		"res://assets/sky_lagoon/lagoon_kit/lagoon_train_station.glb", o + c, 1.0, 0.0)
	if station != null:
		station.set_meta("lagoon_art_role", "lagoon_train_station")
		var counts: Dictionary = m.g.get("lagoon_art_counts", {})
		counts["lagoon_train_station"] = int(counts.get("lagoon_train_station", 0)) + 1
		m.g["lagoon_art_counts"] = counts


# ---------------- car construction ----------------

func _mesh_from_authored_scene(name: String) -> Mesh:
	var packed: PackedScene = load(LAGOON_TRAIN_KIT_ROOT + name + ".glb") as PackedScene
	if packed == null:
		return null
	var scene_root: Node3D = packed.instantiate() as Node3D
	var found: Mesh
	if scene_root is MeshInstance3D:
		found = (scene_root as MeshInstance3D).mesh
	else:
		var mesh_nodes: Array[Node] = scene_root.find_children("*", "MeshInstance3D", true, false)
		if not mesh_nodes.is_empty():
			found = (mesh_nodes[0] as MeshInstance3D).mesh
	scene_root.free()
	return found


func _authored_train_body(parent: Node3D, name: String) -> Node3D:
	var packed: PackedScene = load(LAGOON_TRAIN_KIT_ROOT + name + ".glb") as PackedScene
	if packed == null:
		return null
	var body: Node3D = packed.instantiate() as Node3D
	body.set_meta("lagoon_art_role", name)
	parent.add_child(body)
	var counts: Dictionary = m.g.get("lagoon_art_counts", {})
	counts[name] = int(counts.get(name, 0)) + 1
	m.g["lagoon_art_counts"] = counts
	return body


func _train_mat(col: Color, glow: float = 0.0, metal: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.85 - metal * 0.4
	mat.metallic = metal
	if glow > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = glow
	return mat


func _tpart(parent: Node3D, pos: Vector3, size: Vector3, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var b := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	b.mesh = bm
	b.material_override = _train_mat(col, glow)
	b.position = pos
	parent.add_child(b)
	return b


func _tcyl(parent: Node3D, pos: Vector3, rt: float, rb: float, h: float, col: Color,
		rotx: float = 0.0, rotz: float = 0.0, glow: float = 0.0) -> MeshInstance3D:
	var cyl := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = rt
	cm.bottom_radius = rb
	cm.height = h
	cm.radial_segments = 14
	cyl.mesh = cm
	cyl.material_override = _train_mat(col, glow)
	cyl.position = pos
	cyl.rotation = Vector3(rotx, 0, rotz)
	parent.add_child(cyl)
	return cyl


func _tsphere(parent: Node3D, pos: Vector3, r: float, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var sp := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = r
	sm.height = r * 2.0
	sp.mesh = sm
	sp.material_override = _train_mat(col, glow)
	sp.position = pos
	parent.add_child(sp)
	return sp


func _axle(parent: Node3D, z: float, r: float, wx: float) -> Node3D:
	# a spinning axle: wheel disc each side + a gold crank pin so the roll reads
	var ax := Node3D.new()
	ax.position = Vector3(0, r + 0.3, z)
	parent.add_child(ax)
	for sx: float in [-1.0, 1.0]:
		_tcyl(ax, Vector3(sx * wx, 0, 0), r, r, 0.5, Color(0.24, 0.24, 0.42), 0.0, PI * 0.5)
		_tsphere(ax, Vector3(sx * (wx + 0.3), r * 0.55, 0), 0.22, Color(0.95, 0.8, 0.4))
	return ax


func _car_base(o: Vector3, length: float, col: Color, axz: Array, r: float) -> Node3D:
	# shared chassis: root sits ON the railhead at the bogie midpoint, +Z = travel
	var car := Node3D.new()
	car.position = o
	m.add_child(car)
	m.game_nodes.append(car)
	_tpart(car, Vector3(0, 2.0, 0), Vector3(4.4, 0.7, length), col.darkened(0.35))
	var axles: Array = []
	for z: float in axz:
		axles.append(_axle(car, z, r, 2.4))
	car.set_meta("axles", axles)
	car.set_meta("rods", [])
	return car


func _build_engine(o: Vector3) -> Node3D:
	var car := _car_base(o, 9.0, Color(0.16, 0.18, 0.32), [-1.9, 0.2, 2.3], 1.3)
	_authored_train_body(car, "lagoon_train_engine")
	# Smoke and animated side rods stay procedural gameplay accents around the
	# authored body; neither changes its modeled silhouette or palette.
	var puff := CPUParticles3D.new()
	puff.amount = 16
	puff.lifetime = 2.4
	puff.preprocess = 1.0
	puff.direction = Vector3.UP
	puff.spread = 12.0
	puff.initial_velocity_min = 2.0
	puff.initial_velocity_max = 3.6
	puff.gravity = Vector3(0, 1.2, 0)
	puff.scale_amount_min = 0.8
	puff.scale_amount_max = 2.2
	var pm := SphereMesh.new()
	pm.radius = 0.55
	pm.height = 1.1
	pm.radial_segments = 8
	pm.rings = 4
	puff.mesh = pm
	var pmat := StandardMaterial3D.new()
	pmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	pmat.albedo_color = Color(0.90, 0.93, 1.0, 0.78)
	puff.material_override = pmat
	puff.position = Vector3(0, 7.55, 2.55)
	car.add_child(puff)
	car.set_meta("puff", puff)
	var rods: Array = []
	for sx: float in [-1.0, 1.0]:
		rods.append(_tpart(car, Vector3(sx * 2.75, 1.6, 0.2),
			Vector3(0.22, 0.3, 5.2), Color(0.91, 0.65, 0.25)))
	car.set_meta("rods", rods)
	return car


func _build_tender(o: Vector3) -> Node3D:
	var car := _car_base(o, 6.4, Color(0.16, 0.18, 0.32), [-1.8, 1.8], 0.9)
	_authored_train_body(car, "lagoon_train_tender")
	return car


func _build_coach(o: Vector3) -> Node3D:
	var car := _car_base(o, 8.8, Color(0.55, 0.47, 0.72), [-2.6, 2.6], 0.9)
	_authored_train_body(car, "lagoon_train_coach")
	return car


func _build_gondola(o: Vector3) -> Node3D:
	var car := _car_base(o, 8.0, Color(0.94, 0.76, 0.34), [-2.4, 2.4], 0.9)
	_authored_train_body(car, "lagoon_train_gondola")
	return car


func _build_caboose(o: Vector3) -> Node3D:
	var car := _car_base(o, 8.0, Color(0.88, 0.43, 0.45), [-2.4, 2.4], 0.9)
	_authored_train_body(car, "lagoon_train_caboose")
	return car


func _legacy_build_engine_unused(o: Vector3) -> Node3D:
	var teal := Color(0.35, 0.75, 0.78)
	var navy := Color(0.22, 0.22, 0.40)
	var gold := Color(0.95, 0.80, 0.40)
	var car := _car_base(o, 9.0, navy, [-1.9, 0.2, 2.3], 1.3)
	# boiler + smokebox face
	_tcyl(car, Vector3(0, 3.8, 1.4), 1.9, 1.9, 5.2, teal, PI * 0.5)
	_tcyl(car, Vector3(0, 3.8, 4.2), 2.05, 2.05, 0.6, navy, PI * 0.5)
	_tsphere(car, Vector3(0, 3.8, 4.6), 0.55, gold, 2.0)   # headlamp (emissive, no light)
	# gold boiler bands
	for bz: float in [0.0, 2.6]:
		_tcyl(car, Vector3(0, 3.8, bz), 1.98, 1.98, 0.3, gold, PI * 0.5)
	# funnel + steam dome
	_tcyl(car, Vector3(0, 6.4, 3.2), 1.0, 0.55, 1.7, navy)
	_tsphere(car, Vector3(0, 5.9, 0.8), 0.8, gold)
	# cab with a warm window
	_tpart(car, Vector3(0, 4.6, -2.9), Vector3(4.4, 3.8, 2.8), teal)
	_tpart(car, Vector3(0, 6.75, -2.9), Vector3(5.0, 0.5, 3.4), navy)
	for sx: float in [-1.0, 1.0]:
		_tpart(car, Vector3(sx * 2.25, 5.1, -2.9), Vector3(0.1, 1.5, 1.5), Color(1.0, 0.92, 0.65), 1.2)
	# cowcatcher
	var cow := _tcyl(car, Vector3(0, 1.3, 5.1), 0.2, 2.1, 1.9, navy, -PI * 0.5)
	cow.scale = Vector3(1.0, 1.0, 0.55)
	# smoke puffs from the funnel
	var puff := CPUParticles3D.new()
	puff.amount = 16
	puff.lifetime = 2.4
	puff.preprocess = 1.0
	puff.direction = Vector3.UP
	puff.spread = 12.0
	puff.initial_velocity_min = 2.0
	puff.initial_velocity_max = 3.6
	puff.gravity = Vector3(0, 1.2, 0)
	puff.scale_amount_min = 0.8
	puff.scale_amount_max = 2.2
	var pm := SphereMesh.new()
	pm.radius = 0.55
	pm.height = 1.1
	pm.radial_segments = 8
	pm.rings = 4
	puff.mesh = pm
	var pmat := StandardMaterial3D.new()
	pmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	pmat.albedo_color = Color(0.96, 0.96, 1.0, 0.85)
	puff.material_override = pmat
	puff.position = Vector3(0, 7.5, 3.2)
	car.add_child(puff)
	car.set_meta("puff", puff)
	# side rods riding the driver crank pins (positioned every frame)
	var rods: Array = []
	for sx: float in [-1.0, 1.0]:
		rods.append(_tpart(car, Vector3(sx * 2.75, 1.6, 0.2), Vector3(0.22, 0.3, 5.2), gold))
	car.set_meta("rods", rods)
	return car


func _legacy_build_tender_unused(o: Vector3) -> Node3D:
	var car := _car_base(o, 6.4, Color(0.30, 0.55, 0.60), [-1.8, 1.8], 0.9)
	_tpart(car, Vector3(0, 3.4, 0), Vector3(4.4, 2.2, 6.0), Color(0.35, 0.75, 0.78))
	var sd := 5
	for k in range(5):
		sd = (sd * 1103515245 + 12345) & 0x7fffffff
		_tsphere(car, Vector3(float(sd % 5) * 0.6 - 1.2, 4.7, float((sd >> 3) % 5) * 0.8 - 1.6),
			0.75, Color(0.16, 0.15, 0.2))
	return car


func _legacy_build_coach_unused(o: Vector3) -> Node3D:
	# the passenger coach: open-sided excursion car with a bench INSIDE, so
	# Roshan is really sitting in the cabin and still fully visible
	var lav := Color(0.72, 0.65, 0.92)
	var cream := Color(0.97, 0.93, 0.86)
	var car := _car_base(o, 8.8, lav, [-2.6, 2.6], 0.9)
	_tpart(car, Vector3(0, 2.5, 0), Vector3(4.6, 0.4, 8.4), cream)                 # cabin floor
	# tall cabin: seated Roshan (origin ~4.5, head ~+3.5) needs the roof
	# underside above ~8.2 so she NEVER clips through her own carriage
	for sz: float in [-4.2, 4.2]:
		_tpart(car, Vector3(0, 5.6, sz), Vector3(4.6, 6.2, 0.4), lav)              # end walls
		_tpart(car, Vector3(0, 5.8, sz + signf(sz) * -0.01), Vector3(1.8, 1.6, 0.5), Color(1.0, 0.92, 0.65), 1.0)
	for sx: float in [-1.0, 1.0]:
		_tpart(car, Vector3(sx * 2.2, 3.4, 0), Vector3(0.35, 1.5, 8.4), lav)       # low side walls (big open windows)
		for pz: float in [-4.2, 0.0, 4.2]:
			_tpart(car, Vector3(sx * 2.2, 6.2, pz), Vector3(0.4, 5.0, 0.4), cream)  # roof posts
	_tpart(car, Vector3(0, 8.95, 0), Vector3(5.6, 0.5, 9.4), Color(0.95, 0.62, 0.66))
	_tpart(car, Vector3(0, 9.35, 0), Vector3(3.6, 0.4, 8.0), Color(0.95, 0.72, 0.74))
	_tpart(car, Vector3(0, 3.15, -1.2), Vector3(3.2, 0.55, 1.7), Color(0.95, 0.55, 0.55))   # her bench
	_tpart(car, Vector3(0, 3.9, -1.95), Vector3(3.2, 1.5, 0.35), Color(0.95, 0.55, 0.55))   # backrest
	return car


func _legacy_build_gondola_unused(o: Vector3) -> Node3D:
	# open-top gondola: low walls all round and a big cushion to plop onto
	var butter := Color(0.98, 0.85, 0.45)
	var car := _car_base(o, 8.0, butter, [-2.4, 2.4], 0.9)
	_tpart(car, Vector3(0, 2.5, 0), Vector3(4.6, 0.4, 7.6), butter.darkened(0.15))
	for sx: float in [-1.0, 1.0]:
		_tpart(car, Vector3(sx * 2.25, 3.3, 0), Vector3(0.35, 1.4, 7.6), butter)
	for sz: float in [-3.8, 3.8]:
		_tpart(car, Vector3(0, 3.3, sz), Vector3(4.6, 1.4, 0.35), butter)
	_tpart(car, Vector3(0, 2.9, 0), Vector3(2.8, 0.6, 2.8), Color(0.95, 0.62, 0.78))   # cushion
	return car


func _legacy_build_caboose_unused(o: Vector3) -> Node3D:
	# caboose: a little coral house with a cupola and an OPEN back balcony
	var coral := Color(0.95, 0.55, 0.55)
	var cream := Color(0.97, 0.93, 0.86)
	var car := _car_base(o, 8.0, coral, [-2.4, 2.4], 0.9)
	_tpart(car, Vector3(0, 2.5, 0), Vector3(4.6, 0.4, 7.6), cream)                 # deck (balcony floor)
	_tpart(car, Vector3(0, 4.2, 0.9), Vector3(4.2, 3.4, 4.8), coral)               # house
	_tpart(car, Vector3(0, 6.15, 0.9), Vector3(5.0, 0.5, 5.6), Color(0.60, 0.55, 0.80))
	_tpart(car, Vector3(0, 6.9, 0.9), Vector3(2.2, 1.2, 1.9), coral)               # cupola
	_tpart(car, Vector3(0, 7.7, 0.9), Vector3(2.8, 0.4, 2.5), Color(0.60, 0.55, 0.80))
	for sx: float in [-1.0, 1.0]:
		_tpart(car, Vector3(sx * 2.11, 4.4, 0.9), Vector3(0.1, 1.3, 1.3), Color(1.0, 0.92, 0.65), 1.0)
	# balcony railing around the open back
	for sx: float in [-1.0, 1.0]:
		_tpart(car, Vector3(sx * 2.15, 3.2, -2.7), Vector3(0.3, 1.1, 2.2), cream)
	_tpart(car, Vector3(0, 3.2, -3.75), Vector3(4.6, 1.1, 0.3), cream)
	return car


# ---------------- per-frame drive ----------------

func _tick_train(delta: float, ppos: Vector3) -> void:
	var tr: Dictionary = m.g.get("train", {})
	if tr.is_empty() or m.game != "level2":
		return
	# the castle-hall teardown frees the whole courtyard (train included) —
	# drop the stale state instead of ever touching freed nodes (assigning a
	# freed instance to a typed var is a runtime error, CI 2026-07-13)
	var cars_arr: Array = tr["cars"]
	if cars_arr.is_empty() or not is_instance_valid((cars_arr[0] as Dictionary)["node"]):
		m.g.erase("train")
		_drop_train_ride()
		return
	# outside the courtyard phase (castle hall) the train hides completely —
	# it must never be caught clipping through interior geometry
	if String(m.g.get("phase", "court")) != "court":
		_set_hidden(tr, true)
		return
	var L: float = TAU * RING_R
	var s: float = float(tr["s"])
	var spd: float = float(tr["spd"])
	var spd_max: float = float(tr["spd_max"])
	# ----- station stop state machine -----
	if String(tr["state"]) == "dwell":
		tr["dwell"] = float(tr["dwell"]) - delta
		spd = 0.0
		if float(tr["dwell"]) <= 0.0:
			tr["state"] = "run"
			s = fposmod(s + 1.0, L)   # nudge clear of the stop point
	else:
		var d_st: float = fposmod(STATION_A * RING_R - s, L)
		var target: float = spd_max
		if d_st < 30.0:
			target = maxf(2.0, spd_max * d_st / 30.0)
		spd = move_toward(spd, target, 7.0 * delta)
		if d_st <= maxf(0.6, spd * delta * 1.3):
			s = STATION_A * RING_R
			spd = 0.0
			tr["state"] = "dwell"
			tr["dwell"] = DWELL_T
			tr["dwells"] = int(tr["dwells"]) + 1
	s = fposmod(s + spd * delta, L)
	tr["s"] = s
	tr["spd"] = spd
	# ----- place every car on the ring by its two bogie points -----
	var o: Vector3 = tr["o"]
	var hidden: bool = bool(tr["hidden"])
	for car: Dictionary in (tr["cars"] as Array):
		if not is_instance_valid(car["node"]):
			continue
		var node: Node3D = car["node"]
		var sc: float = fposmod(s - float(car["off"]), L)
		var half_wb: float = float(car["wb"]) * 0.5
		var pf: Vector3 = _track_pt(fposmod(sc + half_wb, L) / RING_R)
		var pr: Vector3 = _track_pt(fposmod(sc - half_wb, L) / RING_R)
		var fwd: Vector3 = (pf - pr).normalized()
		var right: Vector3 = Vector3.UP.cross(fwd).normalized()
		var upv: Vector3 = fwd.cross(right)
		node.global_transform = Transform3D(Basis(right, upv, fwd), o + (pf + pr) * 0.5)
		# wheels roll, side rods ride the crank pins
		var wr: float = float(car["wr"])
		for ax: Node3D in (car["axles"] as Array):
			if is_instance_valid(ax):
				ax.rotation.x = fposmod(ax.rotation.x + spd * delta / wr, TAU)
		var rods: Array = car["rods"]
		if rods.size() > 0:
			var th: float = (car["axles"][0] as Node3D).rotation.x
			for rod: MeshInstance3D in rods:
				if is_instance_valid(rod):
					rod.position.y = 1.6 + cos(th) * 0.7
					rod.position.z = 0.2 + sin(th) * 0.7
		# moving colliders track the car (parked while hidden)
		var solids: Array = car["solids"]
		var zoffs: Array = car["solid_z"]
		for k in range(solids.size()):
			var sd: Dictionary = solids[k]
			if hidden:
				sd["y0"] = -9000.0
				sd["y1"] = -9000.0
				continue
			var pc: Vector3 = node.global_position + fwd * float(zoffs[k])
			sd["x"] = pc.x
			sd["z"] = pc.z
			sd["y0"] = node.global_position.y - 0.5
			sd["y1"] = node.global_position.y + CAR_SOLID_H
	# ----- ride seats follow their cars -----
	for seat: Dictionary in (tr["seats"] as Array):
		if not is_instance_valid(seat["node"]):
			continue
		var cn: Node3D = seat["node"]
		seat["anchor"] = cn.to_global(seat["seat"] as Vector3)
		seat["base"] = seat["anchor"]
		var sf: Vector3 = cn.global_transform.basis.z
		sf.y = 0.0
		seat["fwd"] = sf.normalized() if sf.length() > 0.01 else Vector3.FORWARD
	if is_instance_valid((tr["cars"] as Array)[0]["node"]):
		var eng: Node3D = (tr["cars"] as Array)[0]["node"]
		# smoke only while rolling
		if eng.has_meta("puff"):
			(eng.get_meta("puff") as CPUParticles3D).emitting = (not hidden) and spd > 0.5
		# one-time friendly introduction when she first wanders near
		if not bool(m.g.get("train_intro", false)):
			if Vector2(eng.global_position.x - ppos.x, eng.global_position.z - ppos.z).length() < 34.0:
				m.g["train_intro"] = true
				m.show_msg("Roshan", "A little castle train! Let's hop on for a ride!")
	# ----- clip guard -----
	tr["guard_t"] = float(tr["guard_t"]) - delta
	if float(tr["guard_t"]) <= 0.0:
		tr["guard_t"] = GUARD_DT
		_set_hidden(tr, _clip_check(tr))


func _clip_check(tr: Dictionary) -> bool:
	# true if ANY car would currently intersect terrain or a solid that
	# existed before the train was built — the train hides rather than clip
	var o: Vector3 = tr["o"]
	for car: Dictionary in (tr["cars"] as Array):
		if not is_instance_valid(car["node"]):
			continue
		var node: Node3D = car["node"]
		var base: Vector3 = node.global_position
		var rail_y: float = base.y
		# terrain must stay below the car floor
		if o.y + m._lagoon_local(base.x - o.x, base.z - o.z) > rail_y + 1.4:
			return true
		var fwd: Vector3 = node.global_transform.basis.z
		for zoff: float in (car["solid_z"] as Array):
			var pc: Vector3 = base + fwd * zoff
			for sd: Dictionary in (tr["static"] as Array):
				if rail_y + CAR_SOLID_H < float(sd["y0"]) or rail_y > float(sd["y1"]):
					continue
				if bool(sd["box"]):
					if absf(pc.x - float(sd["cx"])) < float(sd["hx"]) + CAR_SOLID_R and \
							absf(pc.z - float(sd["cz"])) < float(sd["hz"]) + CAR_SOLID_R:
						return true
				else:
					var dx: float = pc.x - float(sd["x"])
					var dz: float = pc.z - float(sd["z"])
					if sqrt(dx * dx + dz * dz) < float(sd["r"]) + CAR_SOLID_R:
						return true
	return false


func _set_hidden(tr: Dictionary, hid: bool) -> void:
	if bool(tr["hidden"]) == hid:
		return
	tr["hidden"] = hid
	for car: Dictionary in (tr["cars"] as Array):
		if is_instance_valid(car["node"]):
			var node: Node3D = car["node"]
			node.visible = not hid
		if hid:
			for sd: Dictionary in (car["solids"] as Array):
				sd["y0"] = -9000.0
				sd["y1"] = -9000.0
	if is_instance_valid((tr["cars"] as Array)[0]["node"]):
		var eng: Node3D = (tr["cars"] as Array)[0]["node"]
		if eng.has_meta("puff"):
			(eng.get_meta("puff") as CPUParticles3D).emitting = not hid
	if hid:
		_drop_train_ride()


func _drop_train_ride() -> void:
	# never leave Roshan riding an invisible (or freed) train
	if not m.toy_play.is_empty() and String(m.toy_play.get("kind", "")).begins_with("train"):
		m.toy_play = {}
		if m.player != null:
			m.player.rotation.x = 0.0


func _ride_jump_pressed() -> bool:
	# the deliberate hop-off gesture: the same jump inputs the swim uses
	if Input.is_physical_key_pressed(KEY_SPACE):
		return true
	if m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B):
		return true
	if "touch_ui" in m and m.touch_ui != null and m.touch_ui.action_down:
		return true
	return false


func _ride_move_held() -> bool:
	# any swim input (keys, left stick, d-pad, touch stick) — held for a
	# beat it also hops her off, so holding the stick can never trap her
	# on the train (probes see no input, so headless never dismounts)
	for k: int in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_W, KEY_A, KEY_S, KEY_D]:
		if Input.is_physical_key_pressed(k):
			return true
	if absf(m.joy_axis(JOY_AXIS_LEFT_X)) > 0.3 or absf(m.joy_axis(JOY_AXIS_LEFT_Y)) > 0.3:
		return true
	if m.joy_pressed(JOY_BUTTON_DPAD_UP) or m.joy_pressed(JOY_BUTTON_DPAD_DOWN) \
			or m.joy_pressed(JOY_BUTTON_DPAD_LEFT) or m.joy_pressed(JOY_BUTTON_DPAD_RIGHT):
		return true
	if "touch_ui" in m and m.touch_ui != null and (m.touch_ui.stick_vec as Vector2).length() > 0.3:
		return true
	return false


func _hop_off(toy: Dictionary) -> void:
	# end the ride on HER terms: giggle, sparkle, a little upward pop, and
	# a short seat cooldown so she can hop straight back on
	toy["cool"] = 2.0
	m.toy_play = {}
	var pl: Node3D = m.player
	if pl != null:
		pl.rotation.x = 0.0
		if "vel" in pl:
			pl.vel = Vector3(0, 9.0, 0)
		m._sparkle_burst(pl.position, Color(0.7, 0.95, 1.0))
		if pl.has_method("play_verb"):
			pl.play_verb("giggle")
