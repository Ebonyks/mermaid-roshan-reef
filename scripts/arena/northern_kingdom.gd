class_name NorthernKingdom
extends RefCounted

# A separately loaded storybook world beyond the Sky Lagoon's Alpine cave star.
# State remains on ReefMain (mostly in g); this satellite only builds and ticks
# the region. Keeping it separate means the Mali-G52 never renders both large
# outdoor worlds at once.

var m: ReefMain

const PASS_LOCAL := Vector2(0.0, 184.0)
const FOREST_LOCAL := Vector2(0.0, 92.0)
const TOWN_LOCAL := Vector2(0.0, 4.0)
const CASTLE_LOCAL := Vector2(0.0, -55.0)
const WORLD_RADIUS := 214.0
const MOUNTAIN_LAYOUT: Array = [
	[Vector2(-53.0, 174.0), 38.0, 66.0], [Vector2(52.0, 179.0), 35.0, 61.0],
	[Vector2(-82.0, 145.0), 25.0, 45.0], [Vector2(82.0, 148.0), 24.0, 43.0],
]
const TOWN_HOUSE_CENTERS: Array[Vector2] = [
	Vector2(-76, 31), Vector2(76, 28), Vector2(-83, -4),
	Vector2(84, -8), Vector2(-82, -43), Vector2(82, -48),
]


func _init(main: ReefMain) -> void:
	m = main


func build(o: Vector3) -> void:
	m.g["north_pass_pos"] = o + Vector3(PASS_LOCAL.x,
		_north_local(PASS_LOCAL.x, PASS_LOCAL.y) + 4.0, PASS_LOCAL.y)
	m.g["north_forest_center"] = o + Vector3(FOREST_LOCAL.x,
		_north_local(FOREST_LOCAL.x, FOREST_LOCAL.y), FOREST_LOCAL.y)
	m.g["north_town_center"] = o + Vector3(TOWN_LOCAL.x,
		_north_local(TOWN_LOCAL.x, TOWN_LOCAL.y), TOWN_LOCAL.y)
	m.g["north_castle_center"] = o + Vector3(CASTLE_LOCAL.x,
		_north_local(CASTLE_LOCAL.x, CASTLE_LOCAL.y), CASTLE_LOCAL.y)
	m.g["north_return_armed"] = false
	m.g["north_forest_greeted"] = false
	m.g["north_town_greeted"] = false
	m.g["north_hint_t"] = 1.0
	m.g["north_wisps"] = []
	_build_environment()
	_build_terrain(o)
	_build_fjords(o)
	_build_mountain_pass(o)
	_build_magic_forest(o)
	_build_town(o)
	_build_center_castle(o)
	_build_wisp_trail(o)


func tick(delta: float, ppos: Vector3) -> void:
	m.g["t"] = float(m.g.get("t", 0.0)) + delta
	var t: float = float(m.g["t"])
	var wisps: Array = m.g.get("north_wisps", [])
	for i in range(wisps.size()):
		var item: Dictionary = wisps[i]
		var orb: MeshInstance3D = item.get("node") as MeshInstance3D
		if not is_instance_valid(orb):
			continue
		var base: Vector3 = item["base"]
		orb.position.y = base.y + sin(t * 2.1 + float(i) * 0.8) * 1.2
		orb.rotation.y += delta * (0.7 + float(i % 3) * 0.16)

	var return_pos: Vector3 = m.g.get("north_return_pos", Vector3.ZERO)
	var return_dist: float = return_pos.distance_to(ppos)
	if not bool(m.g.get("north_return_armed", false)):
		if return_dist > 19.0:
			m.g["north_return_armed"] = true
	elif return_dist < 9.0:
		m._enter_level2(false, true)
		return

	var forest_center: Vector3 = m.g["north_forest_center"]
	if (not bool(m.g.get("north_forest_greeted", false))
		and forest_center.distance_to(ppos) < 65.0):
		m.g["north_forest_greeted"] = true
		m.show_msg("Roshan", "The forest lights are showing us the way!", "pearl2")
	var town_center: Vector3 = m.g["north_town_center"]
	if (not bool(m.g.get("north_town_greeted", false))
		and town_center.distance_to(ppos) < 72.0):
		m.g["north_town_greeted"] = true
		m.show_msg("Roshan", "A tiny fjord town, and a castle in the middle!", "pearl3")

	# A cheap moving pointer supplements the permanent wisp chain. It is visual
	# and voiced, so the route never depends on reading the HUD.
	m.g["north_hint_t"] = float(m.g.get("north_hint_t", 0.0)) - delta
	if float(m.g["north_hint_t"]) <= 0.0:
		m.g["north_hint_t"] = 2.4
		var castle_pos: Vector3 = m.g["north_castle_center"]
		if castle_pos.distance_to(ppos) > 28.0:
			var flat_target: Vector3 = castle_pos
			flat_target.y = ppos.y + 1.5
			for k in range(3):
				var amount: float = 0.07 + float(k) * 0.065
				m._sparkle_burst(ppos.lerp(flat_target, amount), Color(0.72, 0.96, 1.0))
	m.hud_game.text = "Follow the glowing forest lights to the castle!"


func walk_h(x: float, z: float) -> float:
	var lx: float = x - m.NORTHERN_POS.x
	var lz: float = z - m.NORTHERN_POS.z
	var h: float = _north_local(lx, lz)
	# The two little timber piers are optional play spaces over the fjord.
	if absf(lz - 2.0) < 4.5 and absf(lx) > 98.0 and absf(lx) < 145.0:
		h = maxf(h, -1.3)
	return m.NORTHERN_POS.y + h


func _build_environment() -> void:
	m.arena_env = Environment.new()
	m.arena_env.background_mode = Environment.BG_SKY
	var sky: Sky = Sky.new()
	var psky: ProceduralSkyMaterial = ProceduralSkyMaterial.new()
	if m.is_night:
		psky.sky_top_color = Color(0.05, 0.10, 0.27)
		psky.sky_horizon_color = Color(0.33, 0.42, 0.64)
		psky.ground_bottom_color = Color(0.04, 0.13, 0.22)
		psky.ground_horizon_color = Color(0.24, 0.38, 0.52)
	else:
		psky.sky_top_color = Color(0.30, 0.66, 0.88)
		psky.sky_horizon_color = Color(0.82, 0.93, 0.96)
		psky.ground_bottom_color = Color(0.20, 0.42, 0.50)
		psky.ground_horizon_color = Color(0.60, 0.80, 0.78)
	psky.sky_curve = 0.14
	psky.ground_curve = 0.20
	sky.sky_material = psky
	m.arena_env.sky = sky
	m.arena_env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	m.arena_env.ambient_light_energy = 0.54 if m.is_night else 0.62
	m._wind_waker_bloom(m.arena_env, 0.48, 0.08, 1.12)
	m._grade(m.arena_env)
	m.arena_env.tonemap_exposure = 0.88
	m.arena_env.tonemap_white = 1.4
	m.we_node.environment = m.arena_env

	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-52.0, -28.0, 0.0)
	sun.light_color = Color(0.66, 0.74, 0.98) if m.is_night else Color(1.0, 0.93, 0.78)
	sun.light_energy = 0.42 if m.is_night else 0.72
	sun.shadow_enabled = m.quality != "speedy"
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sun.directional_shadow_max_distance = 115.0
	m.add_child(sun)
	m.game_nodes.append(sun)


func _build_terrain(o: Vector3) -> void:
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var cells := 56
	var span := 216.0
	var step: float = span * 2.0 / float(cells)
	var hs: PackedFloat32Array = PackedFloat32Array()
	hs.resize((cells + 1) * (cells + 1))
	for ix in range(cells + 1):
		var x: float = -span + float(ix) * step
		for iz in range(cells + 1):
			var z: float = -span + float(iz) * step
			hs[ix * (cells + 1) + iz] = _north_local(x, z)
	for ix in range(cells):
		var x0: float = -span + float(ix) * step
		var x1: float = x0 + step
		for iz in range(cells):
			var z0: float = -span + float(iz) * step
			var z1: float = z0 + step
			var center: Vector2 = Vector2((x0 + x1) * 0.5, (z0 + z1) * 0.5)
			if center.length() > WORLD_RADIUS:
				continue
			var y00: float = hs[ix * (cells + 1) + iz]
			var y10: float = hs[(ix + 1) * (cells + 1) + iz]
			var y01: float = hs[ix * (cells + 1) + iz + 1]
			var y11: float = hs[(ix + 1) * (cells + 1) + iz + 1]
			_terrain_v(st, x0, z0, y00)
			_terrain_v(st, x1, z1, y11)
			_terrain_v(st, x0, z1, y01)
			_terrain_v(st, x0, z0, y00)
			_terrain_v(st, x1, z0, y10)
			_terrain_v(st, x1, z1, y11)
	st.generate_normals()
	st.generate_tangents()
	var terrain: MeshInstance3D = MeshInstance3D.new()
	terrain.mesh = st.commit()
	terrain.material_override = m._up_mat("grass", 0.042, Color(0.70, 0.90, 0.78))
	terrain.position = o
	m.add_child(terrain)
	m.game_nodes.append(terrain)

	# A cobble ribbon follows the real ground from the pass to the castle gate.
	var path: SurfaceTool = SurfaceTool.new()
	path.begin(Mesh.PRIMITIVE_TRIANGLES)
	var segments := 34
	for i in range(segments):
		var z0: float = 174.0 - float(i) * 5.75
		var z1: float = z0 - 5.75
		_path_v(path, -7.0, z0)
		_path_v(path, 7.0, z1)
		_path_v(path, -7.0, z1)
		_path_v(path, -7.0, z0)
		_path_v(path, 7.0, z0)
		_path_v(path, 7.0, z1)
	path.generate_normals()
	path.generate_tangents()
	var road: MeshInstance3D = MeshInstance3D.new()
	road.mesh = path.commit()
	road.material_override = m._castle_mat("cobble", 0.07, Color(0.88, 0.86, 0.90))
	road.position = o
	m.add_child(road)
	m.game_nodes.append(road)


func _terrain_v(st: SurfaceTool, x: float, z: float, y: float) -> void:
	st.set_uv(Vector2(x * 0.04, z * 0.04))
	st.add_vertex(Vector3(x, y, z))


func _path_v(st: SurfaceTool, x: float, z: float) -> void:
	st.set_uv(Vector2(x * 0.1, z * 0.1))
	st.add_vertex(Vector3(x, _north_local(x, z) + 0.22, z))


func _build_fjords(o: Vector3) -> void:
	var water_mat: ShaderMaterial = m._toon_water_mat(Color(0.12, 0.42, 0.63),
		Color(0.48, 0.80, 0.90), 0.86, 0.18, 0.045)
	water_mat.set_shader_parameter("foam_width", 2.0)
	for side: float in [-1.0, 1.0]:
		var fjord: MeshInstance3D = MeshInstance3D.new()
		var mesh: BoxMesh = BoxMesh.new()
		mesh.size = Vector3(74.0, 0.35, 330.0)
		fjord.mesh = mesh
		fjord.material_override = water_mat
		fjord.position = o + Vector3(side * 166.0, -4.8, -6.0)
		m.add_child(fjord)
		m.game_nodes.append(fjord)

		# Timber piers make the fjord town readable from the main path.
		var pier: MeshInstance3D = m._l2_box(o + Vector3(side * 121.0, -0.9, 2.0),
			Vector3(46.0, 1.0, 8.0), Color(0.48, 0.30, 0.19))
		pier.material_override = m._castle_mat("wood", 0.16, Color(0.88, 0.73, 0.56))
		for px: float in [side * 103.0, side * 121.0, side * 139.0]:
			# Posts reach from the deck through the fjord surface instead of
			# stopping in mid-water above it.
			var post: MeshInstance3D = m._l2_box(o + Vector3(px, -3.0, -1.5),
				Vector3(1.0, 4.0, 1.0), Color(0.40, 0.25, 0.16))
			post.material_override = m._castle_mat("wood", 0.18, Color(0.72, 0.54, 0.38))


func _build_mountain_pass(o: Vector3) -> void:
	for row: Array in MOUNTAIN_LAYOUT:
		_mountain_peak(o, row[0], float(row[1]), float(row[2]))

	var pass_y: float = _north_local(PASS_LOCAL.x, PASS_LOCAL.y)
	var stone: Color = Color(0.50, 0.55, 0.66)
	var gate_scene: PackedScene = load("res://assets/art35/northern/northern_gate.glb")
	var authored_gate: Node3D = null
	if gate_scene != null:
		authored_gate = gate_scene.instantiate() as Node3D
		m._fit_prop(authored_gate, 17.8)
		authored_gate.position = o + Vector3(0.0, pass_y, PASS_LOCAL.y)
		m.add_child(authored_gate)
		m.game_nodes.append(authored_gate)
	for side: float in [-1.0, 1.0]:
		var pillar_pos: Vector3 = o + Vector3(side * 7.2, pass_y + 6.0, PASS_LOCAL.y)
		if authored_gate == null:
			var pillar: MeshInstance3D = m._l2_box(pillar_pos, Vector3(3.4, 12.0, 4.0), stone)
			pillar.material_override = m._up_mat("cliff", 0.08, stone)
		m._wall_solid(pillar_pos, Vector3(3.4, 12.0, 4.0), 0.6)
	if authored_gate == null:
		var lintel_pos: Vector3 = o + Vector3(0.0, pass_y + 12.0, PASS_LOCAL.y)
		var lintel: MeshInstance3D = m._l2_box(lintel_pos, Vector3(17.8, 3.0, 4.0), stone)
		lintel.material_override = m._up_mat("cliff", 0.08, stone)

	var veil: MeshInstance3D = m._l2_box(o + Vector3(0.0, pass_y + 6.0, PASS_LOCAL.y + 0.3),
		Vector3(10.5, 9.5, 0.25), Color(0.40, 0.88, 1.0), 1.5)
	veil.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	veil.material_override.albedo_color.a = 0.34
	veil.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.g["north_return_pos"] = o + Vector3(0.0, pass_y + 4.0, PASS_LOCAL.y)

	var rune: Label3D = Label3D.new()
	rune.text = "\u2744"
	rune.font_size = 230
	rune.pixel_size = 0.025
	rune.outline_size = 28
	rune.modulate = Color(0.72, 0.96, 1.0)
	rune.outline_modulate = Color(0.18, 0.24, 0.48)
	rune.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	rune.position = o + Vector3(0.0, pass_y + 8.0, PASS_LOCAL.y - 0.5)
	m.add_child(rune)
	m.game_nodes.append(rune)


func _mountain_peak(o: Vector3, lp: Vector2, radius: float, height: float) -> void:
	var base_y: float = _north_local(lp.x, lp.y) - 7.0
	var mountain_scene: PackedScene = load("res://assets/art35/northern/northern_mountain.glb")
	if mountain_scene != null:
		var authored_mountain: Node3D = mountain_scene.instantiate() as Node3D
		m._fit_prop(authored_mountain, radius * 2.0)
		authored_mountain.position = o + Vector3(lp.x, base_y, lp.y)
		authored_mountain.rotation.y = lp.x * 0.013
		m.add_child(authored_mountain)
		m.game_nodes.append(authored_mountain)
		m._set_vis_range(authored_mountain, 280.0)
		m._cyl_solid(o + Vector3(lp.x, base_y + height * 0.5, lp.y), radius * 0.42, height * 0.5, 0.6)
		return
	var peak: MeshInstance3D = MeshInstance3D.new()
	var mesh: CylinderMesh = CylinderMesh.new()
	mesh.top_radius = radius * 0.06
	mesh.bottom_radius = radius
	mesh.height = height
	mesh.radial_segments = 10
	peak.mesh = mesh
	peak.material_override = m._up_mat("cliff", 0.055, Color(0.54, 0.58, 0.66))
	peak.position = o + Vector3(lp.x, base_y + height * 0.5, lp.y)
	peak.visibility_range_end = 260.0
	m.add_child(peak)
	m.game_nodes.append(peak)
	m._cyl_solid(peak.position, radius * 0.42, height * 0.5, 0.6)

	var snow: MeshInstance3D = MeshInstance3D.new()
	var cap: CylinderMesh = CylinderMesh.new()
	cap.top_radius = 0.0
	cap.bottom_radius = radius * 0.54
	cap.height = height * 0.30
	cap.radial_segments = 10
	snow.mesh = cap
	snow.material_override = m._up_mat("snow", 0.07, Color(0.90, 0.96, 1.0))
	snow.position = o + Vector3(lp.x, base_y + height * 0.84, lp.y)
	snow.visibility_range_end = 270.0
	m.add_child(snow)
	m.game_nodes.append(snow)


func _build_magic_forest(o: Vector3) -> void:
	var tree_spots: Array[Vector2] = [
		Vector2(-29, 146), Vector2(31, 143), Vector2(-52, 132), Vector2(54, 128),
		Vector2(-31, 116), Vector2(35, 112), Vector2(-68, 105), Vector2(69, 99),
		Vector2(-43, 88), Vector2(45, 82), Vector2(-77, 74), Vector2(75, 66),
		Vector2(-34, 59), Vector2(37, 54), Vector2(-62, 43), Vector2(63, 39),
	]
	var tree_count := 0
	for i in range(tree_spots.size()):
		var lp: Vector2 = tree_spots[i]
		if not _north_flora_allowed("tree_pineRoundF", lp.x, lp.y):
			continue
		var gy: float = _north_local(lp.x, lp.y)
		var scale: float = 9.0 + float(i % 4) * 1.25
		var tree: Node3D = m._nature("tree_pineRoundF", o + Vector3(lp.x, gy - 0.35, lp.y),
			scale, float(i) * 0.71)
		if tree != null:
			tree_count += 1
			m._set_vis_range(tree, 185.0)
		m._cyl_solid(o + Vector3(lp.x, gy + 5.0, lp.y), 1.2, 5.0, 0.55)

	var mushroom_spots: Array[Vector2] = [
		Vector2(-18, 137), Vector2(20, 126), Vector2(-22, 105), Vector2(19, 91),
		Vector2(-24, 76), Vector2(22, 62), Vector2(-19, 48), Vector2(24, 39),
	]
	var mushroom_count := 0
	for i in range(mushroom_spots.size()):
		var mp: Vector2 = mushroom_spots[i]
		var kind := "mushroom_red" if i % 2 == 0 else "mushroom_tanGroup"
		if not _north_flora_allowed(kind, mp.x, mp.y):
			continue
		var plant: Node3D = m._nature(kind, o + Vector3(mp.x,
			_north_local(mp.x, mp.y) - 0.2, mp.y), 4.8 + float(i % 3), float(i) * 0.8)
		if plant != null:
			mushroom_count += 1
			m._set_vis_range(plant, 120.0)
	m.g["north_tree_count"] = tree_count
	m.g["north_mushroom_count"] = mushroom_count


func _build_town(o: Vector3) -> void:
	var houses: Array = [
		[Vector2(-76, 31), Color(0.90, 0.42, 0.35), Color(0.27, 0.34, 0.48)],
		[Vector2(76, 28), Color(0.96, 0.73, 0.32), Color(0.35, 0.24, 0.40)],
		[Vector2(-83, -4), Color(0.40, 0.72, 0.70), Color(0.24, 0.32, 0.45)],
		[Vector2(84, -8), Color(0.82, 0.48, 0.68), Color(0.27, 0.29, 0.43)],
		[Vector2(-82, -43), Color(0.55, 0.67, 0.88), Color(0.31, 0.26, 0.45)],
		[Vector2(82, -48), Color(0.91, 0.60, 0.38), Color(0.25, 0.34, 0.40)],
	]
	for house_i in range(houses.size()):
		var row: Array = houses[house_i]
		_nordic_house(o, row[0], row[1], row[2], house_i % 3)
	m.g["north_house_count"] = houses.size()

	# Low, open docks and pennants make the settlement read as a fjord town.
	for side: float in [-1.0, 1.0]:
		var mast: MeshInstance3D = m._l2_box(o + Vector3(side * 103.0, 4.6, 2.0),
			Vector3(0.65, 10.0, 0.65), Color(0.43, 0.27, 0.17))
		mast.material_override = m._castle_mat("wood", 0.18, Color(0.72, 0.54, 0.38))
		var flag: Node3D = m._kit("castle/flag", o + Vector3(side * 103.0, 8.0, 2.0), 3.0,
			-PI * 0.5 if side < 0.0 else PI * 0.5)
		if flag != null:
			m._set_vis_range(flag, 170.0)


func _nordic_house(o: Vector3, lp: Vector2, body_col: Color, roof_col: Color, variant: int) -> void:
	var gy: float = _north_local(lp.x, lp.y)
	var center: Vector3 = o + Vector3(lp.x, gy, lp.y)
	var body_pos: Vector3 = center + Vector3(0.0, 6.0, 0.0)
	var house_scene: PackedScene = load("res://assets/art35/northern/northern_house_%d.glb" % variant)
	if house_scene != null:
		var authored_house: Node3D = house_scene.instantiate() as Node3D
		m._fit_prop(authored_house, 18.0)
		authored_house.position = center
		authored_house.rotation.y = PI * 0.5 if lp.x > 0.0 else -PI * 0.5
		m.add_child(authored_house)
		m.game_nodes.append(authored_house)
		m._set_vis_range(authored_house, 190.0)
		m._wall_solid(body_pos, Vector3(18.0, 12.0, 15.0), 0.7)
		return
	var body: MeshInstance3D = m._l2_box(body_pos, Vector3(18.0, 12.0, 15.0), body_col)
	body.material_override = m._castle_mat("wood", 0.18, body_col)
	m._wall_solid(body_pos, Vector3(18.0, 12.0, 15.0), 0.7)

	# Two thick roof cards form the steep snow-shedding gable silhouette.
	for side: float in [-1.0, 1.0]:
		var roof: MeshInstance3D = m._l2_box(center + Vector3(side * 4.25, 13.7, 0.0),
			Vector3(11.2, 1.0, 17.2), roof_col)
		roof.rotation.z = side * 0.64
		roof.material_override = m._castle_mat("roof", 0.13, roof_col)

	var inward: float = -1.0 if lp.x > 0.0 else 1.0
	var door_pos: Vector3 = center + Vector3(inward * 9.1, 3.1, 0.0)
	var door: MeshInstance3D = m._l2_box(door_pos, Vector3(0.35, 6.2, 3.8), Color(0.34, 0.22, 0.18))
	door.material_override = m._castle_mat("door", 0.18, Color(0.72, 0.50, 0.34))
	for zoff: float in [-4.6, 4.6]:
		var window: MeshInstance3D = m._l2_box(center + Vector3(inward * 9.2, 7.1, zoff),
			Vector3(0.3, 3.3, 3.0), Color(0.70, 0.91, 1.0), 0.55)
		window.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	# White corner boards give the little houses their painted timber character.
	for zedge: float in [-7.55, 7.55]:
		var trim: MeshInstance3D = m._l2_box(center + Vector3(inward * 9.25, 6.2, zedge),
			Vector3(0.45, 12.4, 0.7), Color(0.95, 0.96, 0.91))
		trim.material_override = m._castle_mat("wood", 0.22, Color(0.95, 0.96, 0.91))


func _build_center_castle(o: Vector3) -> void:
	var cx: float = CASTLE_LOCAL.x
	var cz: float = CASTLE_LOCAL.y
	var gy: float = _north_local(cx, cz)
	var c: Vector3 = o + Vector3(cx, gy, cz)
	var stone: Color = Color(0.70, 0.72, 0.84)

	# Square curtain wall; the broad south gate stays open and easy to swim through.
	_castle_wall(c + Vector3(0, 7, -37), Vector3(68, 14, 4), stone)
	_castle_wall(c + Vector3(-36, 7, 0), Vector3(4, 14, 70), stone)
	_castle_wall(c + Vector3(36, 7, 0), Vector3(4, 14, 70), stone)
	_castle_wall(c + Vector3(-24, 7, 37), Vector3(24, 14, 4), stone)
	_castle_wall(c + Vector3(24, 7, 37), Vector3(24, 14, 4), stone)
	var arch: MeshInstance3D = m._l2_box(c + Vector3(0, 13.0, 37),
		Vector3(24, 4, 4.4), stone.lightened(0.08))
	arch.material_override = m._castle_mat("wall", 0.07, stone.lightened(0.08))

	for corner: Vector2 in [Vector2(-36, -37), Vector2(36, -37),
		Vector2(-36, 37), Vector2(36, 37)]:
		var tower_base: Vector3 = c + Vector3(corner.x, -0.2, corner.y)
		var tower: Node3D = m._kit("castle/tower-square", tower_base, 15.0)
		if tower != null:
			m._set_vis_range(tower, 235.0)
		m._cyl_solid(tower_base + Vector3(0, 9, 0), 6.6, 9.0, 0.6)
		m._kit("castle/flag", tower_base + Vector3(0, 19.0, 0), 2.5)

	# The former keep was an open box with two tilted slabs for a roof. Keep its
	# broad collision footprint, but present one authored, closed toy-castle
	# silhouette with a framed door, snow caps, windows and readable towers.
	var keep_base: Vector3 = c + Vector3(0, 0.0, -13.0)
	var castle_scene: PackedScene = load("res://assets/art35/northern/northern_castle.glb")
	var authored_castle: Node3D = null
	if castle_scene != null:
		authored_castle = castle_scene.instantiate() as Node3D
	if authored_castle != null:
		m._fit_prop(authored_castle, 52.0)
		authored_castle.position = keep_base
		authored_castle.rotation.y = PI
		m.add_child(authored_castle)
		m.game_nodes.append(authored_castle)
		m._set_vis_range(authored_castle, 260.0)
	else:
		var keep: MeshInstance3D = m._l2_box(keep_base + Vector3(0, 10.0, 0), Vector3(30, 20, 24), Color(0.77, 0.78, 0.89))
		keep.material_override = m._castle_mat("wall", 0.065, Color(0.77, 0.78, 0.89))
	m._wall_solid(keep_base + Vector3(0, 10.0, 0), Vector3(30, 20, 24), 0.8)

	var fountain: Node3D = m._kit("park/fountain", c + Vector3(0, 0.15, 18.0), 12.0)
	if fountain != null:
		m._set_vis_range(fountain, 170.0)
		m._cyl_solid(c + Vector3(0, 3.0, 18.0), 4.5, 3.0, 0.5)


func _castle_wall(pos: Vector3, size: Vector3, col: Color) -> void:
	var wall: MeshInstance3D = m._l2_box(pos, size, col)
	wall.material_override = m._castle_mat("wall", 0.07, col)
	m._wall_solid(pos, size, 0.65)


func _build_wisp_trail(o: Vector3) -> void:
	var spots: Array[Vector2] = [
		Vector2(0, 158), Vector2(-5, 132), Vector2(5, 106), Vector2(-4, 80),
		Vector2(4, 54), Vector2(-3, 29), Vector2(3, 4), Vector2(0, -15),
	]
	var wisps: Array = []
	for i in range(spots.size()):
		var lp: Vector2 = spots[i]
		var base: Vector3 = o + Vector3(lp.x, _north_local(lp.x, lp.y) + 4.2, lp.y)
		var orb: MeshInstance3D = MeshInstance3D.new()
		var sphere: SphereMesh = SphereMesh.new()
		sphere.radius = 0.75
		sphere.height = 1.5
		sphere.radial_segments = 8
		sphere.rings = 5
		orb.mesh = sphere
		var col: Color = Color(0.54, 0.94, 1.0) if i % 2 == 0 else Color(0.88, 0.66, 1.0)
		orb.material_override = m._soft_mat(col, 1.8)
		orb.position = base
		orb.visibility_range_end = 145.0

		var ring: MeshInstance3D = MeshInstance3D.new()
		var torus: TorusMesh = TorusMesh.new()
		torus.inner_radius = 1.4
		torus.outer_radius = 1.7
		torus.rings = 10
		torus.ring_segments = 6
		ring.mesh = torus
		ring.material_override = m._soft_mat(col, 1.15)
		ring.rotation.x = PI * 0.5
		orb.add_child(ring)
		m.add_child(orb)
		m.game_nodes.append(orb)
		wisps.append({"node": orb, "base": base})
	m.g["north_wisps"] = wisps
	m.g["north_wisp_count"] = wisps.size()


func _bump(lx: float, lz: float, cx: float, cz: float, radius: float, amp: float) -> float:
	var d2: float = (lx - cx) * (lx - cx) + (lz - cz) * (lz - cz)
	var r2: float = radius * radius
	if d2 >= r2:
		return 0.0
	var f: float = 1.0 - d2 / r2
	return amp * f * f


func _north_flora_allowed(role: String, lx: float, lz: float) -> bool:
	var p := Vector2(lx, lz)
	if p.length() > 198.0:
		return false
	# Water, the maintained cobble route and authored play structures are never
	# scatter substrates, even when the terrain mesh continues underneath them.
	if absf(lx) > 128.0 and absf(lx) < 205.0 and lz > -173.0 and lz < 160.0:
		return false
	if absf(lx) < 11.0 and lz > -23.0 and lz < 178.0:
		return false
	if p.distance_to(CASTLE_LOCAL) < 48.0:
		return false
	for house_center: Vector2 in TOWN_HOUSE_CENTERS:
		if p.distance_to(house_center) < 15.0:
			return false
	for row: Array in MOUNTAIN_LAYOUT:
		var center: Vector2 = row[0]
		var radius: float = float(row[1])
		var mountain_d: float = p.distance_to(center)
		if mountain_d < radius * 0.55:
			return false
		if mountain_d < radius * 1.15:
			return role == "tree_pineRoundF"
	# The kingdom's ordinary low terrain is cool grassland: temperate pines and
	# fungi fit here, while tropical plants do not.
	return role != "tree_palm"


func _north_local(lx: float, lz: float) -> float:
	var h := 2.0
	# The opening pass begins high, then settles into a gently rolling forest.
	h += _bump(lx, lz, 0.0, 178.0, 92.0, 36.0)
	h += _bump(lx, lz, -78.0, 95.0, 68.0, 10.0)
	h += _bump(lx, lz, 82.0, 82.0, 72.0, 9.0)
	h += _bump(lx, lz, -98.0, -82.0, 64.0, 7.0)
	h += _bump(lx, lz, 104.0, -92.0, 68.0, 8.0)
	# Fjords cut into both sides while the central kingdom stays broad and safe.
	var side: float = smoothstep(112.0, 176.0, absf(lx))
	h -= side * 13.0
	# Flatten the road after the steep pass and the town/castle play spaces.
	if lz < 134.0:
		var path_mask: float = 1.0 - smoothstep(12.0, 25.0, absf(lx))
		h = lerpf(h, 2.0, path_mask * 0.84)
	var castle_d: float = Vector2(lx - CASTLE_LOCAL.x, lz - CASTLE_LOCAL.y).length()
	var castle_mask: float = 1.0 - smoothstep(62.0, 92.0, castle_d)
	h = lerpf(h, 2.0, castle_mask)
	# The round diorama falls into painted cliffs just outside the playable rim.
	var r: float = Vector2(lx, lz).length()
	if r > 198.0:
		h -= (r - 198.0) * 0.75
	return h
