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
const NORTH_ASSET_DIR := "res://assets/northern/"
const NORTH_ASSETS := {
	"pass_arch": "northern_pass_arch.glb",
	"peak_a": "northern_peak_a.glb",
	"peak_b": "northern_peak_b.glb",
	"pine_a": "northern_pine_a.glb",
	"pine_b": "northern_pine_b.glb",
	"pine_c": "northern_pine_c.glb",
	"mushrooms_red": "northern_mushrooms_red.glb",
	"mushrooms_tan": "northern_mushrooms_tan.glb",
	"house_red": "northern_house_red.glb",
	"house_amber": "northern_house_amber.glb",
	"house_aqua": "northern_house_aqua.glb",
	"house_rose": "northern_house_rose.glb",
	"house_blue": "northern_house_blue.glb",
	"house_orange": "northern_house_orange.glb",
	"fjord_dock": "northern_fjord_dock.glb",
	"center_castle": "northern_center_castle.glb",
	"wisp": "northern_wisp.glb",
}

var north_asset_cache: Dictionary = {}


func _init(main: ReefMain) -> void:
	m = main


func _fit_authored_prop(model: Node3D, target_long: float) -> float:
	# Northern GLBs already use the approved matte pastel palette. Calling the
	# general imported-CC0 _toonify pass a second time lifts them toward white.
	var boxes: Array = []
	m._local_aabbs(model, Transform3D.IDENTITY, boxes)
	if boxes.is_empty():
		return 0.0
	var bounds: AABB = boxes[0]
	for index in range(1, boxes.size()):
		bounds = bounds.merge(boxes[index])
	var longest: float = maxf(maxf(bounds.size.x, bounds.size.z), 0.001)
	var prop_scale: float = target_long / longest
	model.scale = Vector3.ONE * prop_scale
	var center: Vector3 = bounds.position + bounds.size * 0.5
	model.position = Vector3(-center.x * prop_scale, -bounds.position.y * prop_scale,
		-center.z * prop_scale)
	return bounds.size.y * prop_scale


func _north_prop(kind: String, pos: Vector3, target_long: float,
		yrot: float = 0.0) -> Node3D:
	if not NORTH_ASSETS.has(kind):
		return null
	if not north_asset_cache.has(kind):
		var path: String = NORTH_ASSET_DIR + String(NORTH_ASSETS[kind])
		north_asset_cache[kind] = load(path) if ResourceLoader.exists(path) else null
	var packed: PackedScene = north_asset_cache[kind] as PackedScene
	if packed == null:
		return null
	var wrap := Node3D.new()
	wrap.name = "Northern_%s" % kind
	var model: Node3D = packed.instantiate()
	_fit_authored_prop(model, target_long)
	wrap.add_child(model)
	wrap.position = pos
	wrap.rotation.y = yrot
	m.add_child(wrap)
	m.game_nodes.append(wrap)
	m.g["north_authored_asset_instance_count"] = int(m.g.get(
		"north_authored_asset_instance_count", 0)) + 1
	return wrap


func _light_wisp(node: Node) -> void:
	if node is MeshInstance3D:
		var mesh_node := node as MeshInstance3D
		if mesh_node.mesh != null:
			for surface in range(mesh_node.mesh.get_surface_count()):
				var material: Material = mesh_node.get_active_material(surface)
				if material is StandardMaterial3D:
					var standard := material as StandardMaterial3D
					standard.emission_enabled = true
					standard.emission = standard.albedo_color
					standard.emission_energy_multiplier = 0.72
	for child in node.get_children():
		_light_wisp(child)


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
	m.g["north_authored_asset_family_count"] = NORTH_ASSETS.size()
	m.g["north_authored_asset_instance_count"] = 0
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
		var orb: Node3D = item.get("node") as Node3D
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
	m.arena_env.ambient_light_energy = 0.30 if m.is_night else 0.38
	m._apply_scene_grade(m.arena_env, "bright_pastel")
	m.arena_env.glow_enabled = false
	m.arena_env.tonemap_exposure = 0.56 if m.quality == "speedy" else 0.64
	m.arena_env.adjustment_brightness = 0.90
	m.we_node.environment = m.arena_env

	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-52.0, -28.0, 0.0)
	sun.light_color = Color(0.66, 0.74, 0.98) if m.is_night else Color(1.0, 0.93, 0.78)
	sun.light_energy = 0.30 if m.is_night else 0.46
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
	terrain.material_override = m._up_mat("grass", 0.042, Color(0.52, 0.74, 0.61))
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
	road.material_override = m._castle_mat("cobble", 0.07, Color(0.68, 0.66, 0.72))
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

		# Authored rope piers replace the former slabs and posts. The fish carving
		# sits on the water-side end on both banks.
		_north_prop("fjord_dock", o + Vector3(side * 121.0, -1.3, 2.0), 46.0,
			PI if side < 0.0 else 0.0)


func _build_mountain_pass(o: Vector3) -> void:
	for row: Array in [
		[Vector2(-53.0, 174.0), 38.0, 66.0, "peak_a"],
		[Vector2(52.0, 179.0), 35.0, 61.0, "peak_b"],
		[Vector2(-82.0, 145.0), 25.0, 45.0, "peak_b"],
		[Vector2(82.0, 148.0), 24.0, 43.0, "peak_a"],
	]:
		_mountain_peak(o, row[0], float(row[1]), float(row[2]), String(row[3]))

	var pass_y: float = _north_local(PASS_LOCAL.x, PASS_LOCAL.y)
	_north_prop("pass_arch", o + Vector3(0.0, pass_y, PASS_LOCAL.y), 18.0)
	for side: float in [-1.0, 1.0]:
		var pillar_pos: Vector3 = o + Vector3(side * 7.2, pass_y + 6.0, PASS_LOCAL.y)
		m._wall_solid(pillar_pos, Vector3(3.4, 12.0, 4.0), 0.6)
	m.g["north_return_pos"] = o + Vector3(0.0, pass_y + 4.0, PASS_LOCAL.y)


func _mountain_peak(o: Vector3, lp: Vector2, radius: float, height: float,
		kind: String) -> void:
	var base_y: float = _north_local(lp.x, lp.y) - 7.0
	var peak_pos: Vector3 = o + Vector3(lp.x, base_y, lp.y)
	var peak: Node3D = _north_prop(kind, peak_pos, radius * 2.0, lp.x * 0.013)
	if peak != null:
		m._set_vis_range(peak, 270.0)
	m._cyl_solid(peak_pos + Vector3(0.0, height * 0.5, 0.0),
		radius * 0.42, height * 0.5, 0.6)


func _build_magic_forest(o: Vector3) -> void:
	var tree_spots: Array[Vector2] = [
		Vector2(-29, 146), Vector2(31, 143), Vector2(-52, 132), Vector2(54, 128),
		Vector2(-31, 116), Vector2(35, 112), Vector2(-68, 105), Vector2(69, 99),
		Vector2(-43, 88), Vector2(45, 82), Vector2(-77, 74), Vector2(75, 66),
		Vector2(-34, 59), Vector2(37, 54), Vector2(-62, 43), Vector2(63, 39),
	]
	for i in range(tree_spots.size()):
		var lp: Vector2 = tree_spots[i]
		var gy: float = _north_local(lp.x, lp.y)
		var target: float = 9.4 + float(i % 4) * 1.1
		var pine_kind: String = String(["pine_a", "pine_b", "pine_c"][i % 3])
		var tree: Node3D = _north_prop(pine_kind, o + Vector3(lp.x, gy - 0.35, lp.y),
			target, float(i) * 0.71)
		if tree != null:
			m._set_vis_range(tree, 185.0)
		m._cyl_solid(o + Vector3(lp.x, gy + 5.0, lp.y), 1.2, 5.0, 0.55)

	var mushroom_spots: Array[Vector2] = [
		Vector2(-18, 137), Vector2(20, 126), Vector2(-22, 105), Vector2(19, 91),
		Vector2(-24, 76), Vector2(22, 62), Vector2(-19, 48), Vector2(24, 39),
	]
	for i in range(mushroom_spots.size()):
		var mp: Vector2 = mushroom_spots[i]
		var kind := "mushrooms_red" if i % 2 == 0 else "mushrooms_tan"
		var plant: Node3D = _north_prop(kind, o + Vector3(mp.x,
			_north_local(mp.x, mp.y) - 0.2, mp.y), 5.2 + float(i % 3), float(i) * 0.8)
		if plant != null:
			m._set_vis_range(plant, 120.0)
	m.g["north_tree_count"] = tree_spots.size()


func _build_town(o: Vector3) -> void:
	var houses: Array = [
		[Vector2(-76, 31), "house_red"],
		[Vector2(76, 28), "house_amber"],
		[Vector2(-83, -4), "house_aqua"],
		[Vector2(84, -8), "house_rose"],
		[Vector2(-82, -43), "house_blue"],
		[Vector2(82, -48), "house_orange"],
	]
	for row: Array in houses:
		_nordic_house(o, row[0], String(row[1]))
	m.g["north_house_count"] = houses.size()

	# Low, open docks and pennants make the settlement read as a fjord town.
	for side: float in [-1.0, 1.0]:
		var flag: Node3D = m._kit("castle/flag", o + Vector3(side * 103.0, 8.0, 2.0), 3.0,
			-PI * 0.5 if side < 0.0 else PI * 0.5)
		if flag != null:
			m._set_vis_range(flag, 170.0)


func _nordic_house(o: Vector3, lp: Vector2, kind: String) -> void:
	var gy: float = _north_local(lp.x, lp.y)
	var center: Vector3 = o + Vector3(lp.x, gy, lp.y)
	var inward_rotation: float = -PI * 0.5 if lp.x > 0.0 else PI * 0.5
	var house: Node3D = _north_prop(kind, center, 19.5, inward_rotation)
	if house != null:
		m._set_vis_range(house, 205.0)
	m._wall_solid(center + Vector3(0.0, 7.2, 0.0), Vector3(15.0, 14.4, 15.0), 0.7)


func _build_center_castle(o: Vector3) -> void:
	var cx: float = CASTLE_LOCAL.x
	var cz: float = CASTLE_LOCAL.y
	var gy: float = _north_local(cx, cz)
	var c: Vector3 = o + Vector3(cx, gy, cz)
	var castle: Node3D = _north_prop("center_castle", c, 74.0)
	if castle != null:
		m._set_vis_range(castle, 245.0)

	# Analytic solids stay independent from the authored scene so collision
	# remains cheap and deterministic on the phone.
	_castle_wall(c + Vector3(0, 7, -37), Vector3(68, 14, 4))
	_castle_wall(c + Vector3(-36, 7, 0), Vector3(4, 14, 70))
	_castle_wall(c + Vector3(36, 7, 0), Vector3(4, 14, 70))
	_castle_wall(c + Vector3(-24, 7, 37), Vector3(24, 14, 4))
	_castle_wall(c + Vector3(24, 7, 37), Vector3(24, 14, 4))

	for corner: Vector2 in [Vector2(-36, -37), Vector2(36, -37),
		Vector2(-36, 37), Vector2(36, 37)]:
		var tower_base: Vector3 = c + Vector3(corner.x, -0.2, corner.y)
		m._cyl_solid(tower_base + Vector3(0, 9, 0), 6.6, 9.0, 0.6)

	# The keep stays open as a destination: there is no lock, score, or fail state.
	var keep_pos: Vector3 = c + Vector3(0, 10.0, -13.0)
	m._wall_solid(keep_pos, Vector3(30, 20, 24), 0.8)

	var fountain: Node3D = m._kit("park/fountain", c + Vector3(0, 0.15, 18.0), 12.0)
	if fountain != null:
		m._set_vis_range(fountain, 170.0)
		m._cyl_solid(c + Vector3(0, 3.0, 18.0), 4.5, 3.0, 0.5)


func _castle_wall(pos: Vector3, size: Vector3) -> void:
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
		var orb: Node3D = _north_prop("wisp", base, 3.3, float(i) * 0.57)
		if orb != null:
			_light_wisp(orb)
			m._set_vis_range(orb, 145.0)
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
