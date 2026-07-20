class_name NorthernKingdom
extends RefCounted

# A separately loaded storybook world beyond the Sky Lagoon's Alpine cave star.
# State remains on ReefMain (mostly in g); this satellite only builds and ticks
# the region. Keeping it separate means the Mali-G52 never renders both large
# outdoor worlds at once.
#
# REDESIGN 2026-07-17: the old round diorama is now a LONG strip stage with
# three acts walked south from the mountain pass:
#   1. Mystical autumn forest (~430u, a 20-30s walk): winding path, a small
#      stream that crosses it twice, dense tree walls, understory brush,
#      mushrooms, two spirit-stone clearings (future spirit-boss arenas),
#      warm mist and drifting leaves. Palette after autumn folklore forests:
#      magenta/ochre canopies against grey-lavender mist.
#   2. Riverside town: ONE road runs straight through (the road IS the town),
#      squeezed between the river on the east and a steep mountainside on the
#      west — timber houses, an inn, a smith's open forge porch, and a lumber
#      mill on its own island.
#   3. Ice castle on a plateau at the far end: curtain wall, forecourt with a
#      frozen fountain, and an enterable GRAND HALL with twin sweeping
#      staircases up to a mezzanine of three little bedrooms.

var m: ReefMain

# Authored northern GLB family (matte pastel palette, audited): every prop
# with an authored model uses it; procedural blockwork only fills the gaps
# that have no authored equivalent yet (mill, castle + grand hall interior).
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

const PASS_LOCAL := Vector2(0.0, 348.0)
const SPAWN_LOCAL := Vector2(0.0, 332.0)
const FOREST_LOCAL := Vector2(0.0, 140.0)    # forest heart
const TOWN_LOCAL := Vector2(0.0, -180.0)
const CASTLE_LOCAL := Vector2(0.0, -318.0)
const CLEARING_A := Vector2(18.0, 138.0)     # spirit clearings (boss arenas later)
const CLEARING_B := Vector2(-20.0, -58.0)
const HALL_FLOOR := 6.0                      # castle plateau height
const MEZZ_FLOOR := 17.0                     # bedroom mezzanine height
const STRIP_X := 150.0                       # built terrain half-width
const STRIP_Z := 385.0                       # built terrain half-length


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
	m.g["north_hall_center"] = o + Vector3(0.0, HALL_FLOOR, -326.0)
	m.g["north_return_armed"] = false
	m.g["north_forest_greeted"] = false
	m.g["north_town_greeted"] = false
	m.g["north_hall_greeted"] = false
	m.g["north_hint_t"] = 1.0
	m.g["north_wisps"] = []
	m.g["north_spins"] = []
	m.g["north_authored_asset_family_count"] = NORTH_ASSETS.size()
	m.g["north_authored_asset_instance_count"] = 0
	_build_environment()
	_build_terrain(o)
	_build_fjords(o)
	_build_stream(o)
	_build_mountain_pass(o)
	_build_backdrop_peaks(o)
	_build_magic_forest(o)
	_build_spirit_clearings(o)
	_build_forest_pois(o)
	_build_town(o)
	_build_castle(o)
	_build_grand_hall(o)
	_build_wisp_trail(o)
	_build_leaf_drift(o)


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

	# Cosmetic rotors: the mill's water wheel and the hall chandelier.
	for spin: Dictionary in m.g.get("north_spins", []):
		var node: Node3D = spin.get("node") as Node3D
		if not is_instance_valid(node):
			continue
		if String(spin.get("axis", "y")) == "x":
			node.rotation.x += delta * float(spin.get("speed", 0.6))
		else:
			node.rotation.y += delta * float(spin.get("speed", 0.6))

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
		and forest_center.distance_to(ppos) < 90.0):
		m.g["north_forest_greeted"] = true
		m.show_msg("Roshan", "A misty magic forest! The little lights know the way!", "pearl2")
	var town_center: Vector3 = m.g["north_town_center"]
	if (not bool(m.g.get("north_town_greeted", false))
		and town_center.distance_to(ppos) < 80.0):
		m.g["north_town_greeted"] = true
		m.show_msg("Roshan", "A little river town! The castle is past the houses!", "pearl3")
	var hall_center: Vector3 = m.g["north_hall_center"]
	if (not bool(m.g.get("north_hall_greeted", false))
		and hall_center.distance_to(ppos) < 24.0):
		m.g["north_hall_greeted"] = true
		m.show_msg("Roshan", "The great ice hall! Look at the swirly stairs!", "pearl")

	# A cheap moving pointer supplements the permanent wisp chain. It is visual
	# and voiced, so the route never depends on reading the HUD.
	m.g["north_hint_t"] = float(m.g.get("north_hint_t", 0.0)) - delta
	if float(m.g["north_hint_t"]) <= 0.0:
		m.g["north_hint_t"] = 2.4
		var castle_pos: Vector3 = m.g["north_castle_center"]
		if castle_pos.distance_to(ppos) > 34.0:
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
	# Log bridge over the stream's second crossing keeps the road dry.
	var bx: float = _stream_x(-28.0)
	if absf(lz + 28.0) < 4.2 and absf(lx - bx) < 4.0:
		h = maxf(h, 2.3)
	# Plank bridge from the town road out to the mill island.
	if absf(lz + 213.0) < 3.4 and lx > 30.0 and lx < 48.5:
		h = maxf(h, 2.7)
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
		psky.sky_top_color = Color(0.30, 0.62, 0.88)
		psky.sky_horizon_color = Color(0.88, 0.90, 0.94)
		psky.ground_bottom_color = Color(0.22, 0.40, 0.46)
		psky.ground_horizon_color = Color(0.70, 0.76, 0.76)
	psky.sky_curve = 0.14
	psky.ground_curve = 0.20
	sky.sky_material = psky
	m.arena_env.sky = sky
	m.arena_env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	m.arena_env.ambient_light_energy = 0.54 if m.is_night else 0.62
	# The forest's mystical read is mostly MIST: warm grey-lavender depth fog
	# that pushes the tree layers back (cheap distance fog, not volumetric).
	m.arena_env.fog_enabled = true
	m.arena_env.fog_light_color = (Color(0.42, 0.50, 0.70) if m.is_night
		else Color(0.86, 0.81, 0.88))
	m.arena_env.fog_density = 0.006 if m.is_night else 0.0042
	m.arena_env.fog_sky_affect = 0.12
	m._wind_waker_bloom(m.arena_env, 0.48, 0.08, 1.12)
	m._grade(m.arena_env)
	m.arena_env.tonemap_exposure = 0.88
	m.arena_env.tonemap_white = 1.4
	m.we_node.environment = m.arena_env

	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48.0, -30.0, 0.0)
	sun.light_color = Color(0.66, 0.74, 0.98) if m.is_night else Color(1.0, 0.90, 0.74)
	sun.light_energy = 0.42 if m.is_night else 0.72
	sun.shadow_enabled = m.quality != "speedy"
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sun.directional_shadow_max_distance = 115.0
	m.add_child(sun)
	m.game_nodes.append(sun)


func _build_terrain(o: Vector3) -> void:
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var cells_x := 40
	var cells_z := 104
	var step_x: float = STRIP_X * 2.0 / float(cells_x)
	var step_z: float = STRIP_Z * 2.0 / float(cells_z)
	var hs: PackedFloat32Array = PackedFloat32Array()
	hs.resize((cells_x + 1) * (cells_z + 1))
	for ix in range(cells_x + 1):
		var x: float = -STRIP_X + float(ix) * step_x
		for iz in range(cells_z + 1):
			var z: float = -STRIP_Z + float(iz) * step_z
			hs[ix * (cells_z + 1) + iz] = _north_local(x, z)
	for ix in range(cells_x):
		var x0: float = -STRIP_X + float(ix) * step_x
		var x1: float = x0 + step_x
		for iz in range(cells_z):
			var z0: float = -STRIP_Z + float(iz) * step_z
			var z1: float = z0 + step_z
			var y00: float = hs[ix * (cells_z + 1) + iz]
			var y10: float = hs[(ix + 1) * (cells_z + 1) + iz]
			var y01: float = hs[ix * (cells_z + 1) + iz + 1]
			var y11: float = hs[(ix + 1) * (cells_z + 1) + iz + 1]
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
	# Warmer gold-green than the lagoon: autumn floor under magenta canopies.
	terrain.material_override = m._up_mat("grass", 0.042, Color(0.84, 0.88, 0.66))
	terrain.position = o
	m.add_child(terrain)
	m.game_nodes.append(terrain)

	# The road ribbon follows the real ground AND the winding path line from
	# the pass, through town, to the castle gate. Dirt in the forest, cobble
	# from the town gate south (the town's one street IS the town).
	for span: Array in [[344.0, -112.0, "dirt", Color(0.82, 0.72, 0.58), 5.4],
		[-112.0, -294.0, "cobble", Color(0.88, 0.86, 0.90), 6.6]]:
		var path: SurfaceTool = SurfaceTool.new()
		path.begin(Mesh.PRIMITIVE_TRIANGLES)
		var z_top: float = span[0]
		var z_bot: float = span[1]
		var seg_len := 5.5
		var segments: int = int((z_top - z_bot) / seg_len)
		var w: float = span[4]
		for i in range(segments):
			var z0: float = z_top - float(i) * seg_len
			var z1: float = maxf(z0 - seg_len, z_bot)
			var c0: float = _path_x(z0)
			var c1: float = _path_x(z1)
			_path_v(path, c0 - w, z0)
			_path_v(path, c1 + w, z1)
			_path_v(path, c1 - w, z1)
			_path_v(path, c0 - w, z0)
			_path_v(path, c0 + w, z0)
			_path_v(path, c1 + w, z1)
		path.generate_normals()
		path.generate_tangents()
		var road: MeshInstance3D = MeshInstance3D.new()
		road.mesh = path.commit()
		var mat_key: String = span[2]
		if mat_key == "dirt":
			road.material_override = m._up_mat("grass", 0.09, span[3])
		else:
			road.material_override = m._castle_mat("cobble", 0.07, span[3])
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
		mesh.size = Vector3(74.0, 0.35, 790.0)
		fjord.mesh = mesh
		fjord.material_override = water_mat
		fjord.position = o + Vector3(side * 152.0, -4.8, 0.0)
		m.add_child(fjord)
		m.game_nodes.append(fjord)


func _build_stream(o: Vector3) -> void:
	# The small forest stream: born on the pass slope, it crosses the road at
	# the stepping-stone ford (lz 175) and the log bridge (lz -28), then
	# swings east and widens into the town river past the mill island.
	var water_mat: ShaderMaterial = m._toon_water_mat(Color(0.16, 0.46, 0.62),
		Color(0.55, 0.85, 0.92), 0.82, 0.14, 0.06)
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var z_top := 338.0
	var z_bot := -382.0
	var seg := 9.0
	var count: int = int((z_top - z_bot) / seg)
	for i in range(count):
		var z0: float = z_top - float(i) * seg
		var z1: float = maxf(z0 - seg, z_bot)
		var c0: float = _stream_x(z0)
		var c1: float = _stream_x(z1)
		var w0: float = _stream_w(z0) * 0.92
		var w1: float = _stream_w(z1) * 0.92
		var y0: float = _north_local(c0, z0) + 1.35
		var y1: float = _north_local(c1, z1) + 1.35
		st.set_uv(Vector2((c0 - w0) * 0.05, z0 * 0.05))
		st.add_vertex(Vector3(c0 - w0, y0, z0))
		st.set_uv(Vector2((c1 + w1) * 0.05, z1 * 0.05))
		st.add_vertex(Vector3(c1 + w1, y1, z1))
		st.set_uv(Vector2((c1 - w1) * 0.05, z1 * 0.05))
		st.add_vertex(Vector3(c1 - w1, y1, z1))
		st.set_uv(Vector2((c0 - w0) * 0.05, z0 * 0.05))
		st.add_vertex(Vector3(c0 - w0, y0, z0))
		st.set_uv(Vector2((c0 + w0) * 0.05, z0 * 0.05))
		st.add_vertex(Vector3(c0 + w0, y0, z0))
		st.set_uv(Vector2((c1 + w1) * 0.05, z1 * 0.05))
		st.add_vertex(Vector3(c1 + w1, y1, z1))
	st.generate_normals()
	var stream: MeshInstance3D = MeshInstance3D.new()
	stream.mesh = st.commit()
	stream.material_override = water_mat
	stream.position = o
	m.add_child(stream)
	m.game_nodes.append(stream)

	# Stepping stones at the first ford: the crossing is a shallow splashy
	# wade, and the stones make it read as the intended route.
	var ford_x: float = _stream_x(175.0)
	for i in range(4):
		var sx: float = ford_x - 4.5 + float(i) * 3.0
		var sy: float = _north_local(sx, 175.0)
		var stone: MeshInstance3D = MeshInstance3D.new()
		var sm: SphereMesh = SphereMesh.new()
		sm.radius = 1.5
		sm.height = 1.7
		sm.radial_segments = 8
		sm.rings = 5
		stone.mesh = sm
		stone.material_override = m._up_mat("cliff", 0.09, Color(0.68, 0.70, 0.76))
		stone.position = o + Vector3(sx, sy + 1.1, 175.0 + (0.9 if i % 2 == 0 else -0.9))
		m.add_child(stone)
		m.game_nodes.append(stone)

	# Log bridge at the second crossing (walk_h keeps its deck dry).
	var bx: float = _stream_x(-28.0)
	var deck: MeshInstance3D = m._l2_box(o + Vector3(bx, 2.0, -28.0),
		Vector3(12.0, 0.8, 6.4), Color(0.48, 0.30, 0.19))
	deck.material_override = m._castle_mat("wood", 0.16, Color(0.86, 0.70, 0.52))
	for side: float in [-1.0, 1.0]:
		var rail: MeshInstance3D = m._l2_box(o + Vector3(bx, 3.3, -28.0 + side * 3.0),
			Vector3(12.4, 0.5, 0.5), Color(0.40, 0.25, 0.16))
		rail.material_override = m._castle_mat("wood", 0.18, Color(0.70, 0.52, 0.36))


func _build_mountain_pass(o: Vector3) -> void:
	var pass_y: float = _north_local(PASS_LOCAL.x, PASS_LOCAL.y)
	# The authored arch is the gate; analytic solids keep collision cheap.
	_north_prop("pass_arch", o + Vector3(0.0, pass_y, PASS_LOCAL.y), 18.0)
	for side: float in [-1.0, 1.0]:
		var pillar_pos: Vector3 = o + Vector3(side * 7.2, pass_y + 6.0, PASS_LOCAL.y)
		m._wall_solid(pillar_pos, Vector3(3.4, 12.0, 4.0), 0.6)

	var veil: MeshInstance3D = m._l2_box(o + Vector3(0.0, pass_y + 6.0, PASS_LOCAL.y + 0.3),
		Vector3(10.5, 9.5, 0.25), Color(0.40, 0.88, 1.0), 1.5)
	veil.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	veil.material_override.albedo_color.a = 0.34
	veil.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.g["north_return_pos"] = o + Vector3(0.0, pass_y + 4.0, PASS_LOCAL.y)

	var rune: Label3D = Label3D.new()
	rune.text = "❄"
	rune.font_size = 230
	rune.pixel_size = 0.025
	rune.outline_size = 28
	rune.modulate = Color(0.72, 0.96, 1.0)
	rune.outline_modulate = Color(0.18, 0.24, 0.48)
	rune.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	rune.position = o + Vector3(0.0, pass_y + 8.0, PASS_LOCAL.y - 0.5)
	m.add_child(rune)
	m.game_nodes.append(rune)

	# Flanking peaks frame the pass itself.
	_mountain_peak(o, Vector2(-56.0, 340.0), 38.0, 66.0, "peak_a")
	_mountain_peak(o, Vector2(55.0, 344.0), 35.0, 61.0, "peak_b")
	_mountain_peak(o, Vector2(-96.0, 300.0), 26.0, 46.0, "peak_b")
	_mountain_peak(o, Vector2(95.0, 305.0), 25.0, 44.0, "peak_a")


func _build_backdrop_peaks(o: Vector3) -> void:
	# A painted mountain rim walls the long strip: the forest edge, the
	# town's steep western side, and a big massif behind the castle.
	for row: Array in [
		[Vector2(-128.0, 210.0), 30.0, 52.0], [Vector2(130.0, 195.0), 28.0, 50.0],
		[Vector2(-134.0, 80.0), 32.0, 56.0], [Vector2(133.0, 60.0), 30.0, 52.0],
		[Vector2(-130.0, -40.0), 30.0, 54.0], [Vector2(134.0, -70.0), 28.0, 48.0],
		[Vector2(-118.0, -160.0), 36.0, 70.0], [Vector2(-126.0, -225.0), 34.0, 64.0],
		[Vector2(128.0, -195.0), 30.0, 50.0],
		[Vector2(-70.0, -372.0), 40.0, 74.0], [Vector2(66.0, -374.0), 38.0, 70.0],
		[Vector2(0.0, -386.0), 52.0, 88.0],
	]:
		var lp: Vector2 = row[0]
		_mountain_peak(o, lp, float(row[1]), float(row[2]),
			"peak_a" if int(absf(lp.x + lp.y)) % 2 == 0 else "peak_b")


func _mountain_peak(o: Vector3, lp: Vector2, radius: float, height: float,
		kind: String = "peak_a") -> void:
	var base_y: float = _north_local(lp.x, lp.y) - 7.0
	var peak_pos: Vector3 = o + Vector3(lp.x, base_y, lp.y)
	var peak: Node3D = _north_prop(kind, peak_pos, radius * 2.0, lp.x * 0.013)
	if peak != null:
		m._set_vis_range(peak, 420.0)
	m._cyl_solid(peak_pos + Vector3(0.0, height * 0.5, 0.0),
		radius * 0.42, height * 0.5, 0.6)


func _jit(i: int, salt: float) -> float:
	# Deterministic 0..1 jitter so the forest layout is stable run to run.
	return fposmod(sin(float(i) * 12.9898 + salt) * 43758.5453, 1.0)


func _clearing_d(lx: float, lz: float) -> float:
	return minf(Vector2(lx - CLEARING_A.x, lz - CLEARING_A.y).length(),
		Vector2(lx - CLEARING_B.x, lz - CLEARING_B.y).length())


func _north_flora_allowed(role: String, lx: float, lz: float) -> bool:
	# Scatter substrate rules for the LONG strip: the single road, the
	# stream/river, the spirit clearings, the town street frontage and the
	# castle plateau are never planted, even though terrain continues there.
	if absf(lx) > 115.0 or absf(lz) > 360.0:
		return false
	if absf(lx - _path_x(lz)) < 8.0:
		return false
	if absf(lx - _stream_x(lz)) < 8.0:
		return false
	if _clearing_d(lx, lz) < 20.0:
		return false
	if Vector2(lx * 0.82, lz - CASTLE_LOCAL.y).length() < 88.0:
		return false
	if lz < -112.0 and lz > -256.0 and absf(lx) < 40.0:
		return false
	# The kingdom is cool northern grassland: temperate pines, autumn
	# broadleaves and fungi fit here, tropical plants do not.
	return role != "tree_palm"


func _forest_tree(i: int, pos: Vector3, target: float, yrot: float,
		vis: float) -> void:
	# The tree walls MIX the authored pine family with the gen2 autumn
	# broadleaves — pines carry the northern silhouette, the magenta/gold
	# canopies carry the mystical-autumn palette.
	var tree: Node3D
	if i % 2 == 0:
		var pine_kind: String = String(["pine_a", "pine_b", "pine_c"][(i / 2) % 3])
		tree = _north_prop(pine_kind, pos, target * 0.9, yrot)
	else:
		var fall_kind: String = String(["tree_default_fall", "tree_simple_fall",
			"tree_fat"][(i / 2) % 3])
		tree = m._nature(fall_kind, pos, target, yrot)
	if tree != null:
		m._set_vis_range(tree, vis)


func _build_magic_forest(o: Vector3) -> void:
	# DENSE tree walls flank the winding path the whole way down the forest
	# act. Two ranks: a near rank that shapes the corridor (with trunk
	# solids) and a far scatter rank that reads as depth through the mist.
	var tree_count := 0
	var i := 0
	var lz := 312.0
	while lz > -104.0 and tree_count < 96:
		for side: float in [-1.0, 1.0]:
			var px: float = _path_x(lz)
			# near rank: 13..26u off the path edge, jittered
			var off: float = 13.0 + _jit(i, side * 3.7) * 13.0
			var lx: float = px + side * off
			i += 1
			if (_north_flora_allowed("tree_pineRoundF", lx, lz)
				and _clearing_d(lx, lz) > 25.0):
				var gy: float = _north_local(lx, lz)
				var scale: float = 8.5 + _jit(i, 1.3) * 4.5
				_forest_tree(i, o + Vector3(lx, gy - 0.35, lz), scale,
					_jit(i, 7.7) * TAU, 165.0)
				m._cyl_solid(o + Vector3(lx, gy + 5.0, lz), 1.2, 5.0, 0.55)
				tree_count += 1
			# far rank: 34..58u out, every other row, no solids (mist dressing)
			if i % 2 == 0 and tree_count < 96:
				var fx: float = px + side * (34.0 + _jit(i, 9.1) * 24.0)
				if _north_flora_allowed("tree_pineRoundF", fx, lz):
					var fy: float = _north_local(fx, lz)
					_forest_tree(i + 1, o + Vector3(fx, fy - 0.4, lz),
						10.0 + _jit(i, 4.2) * 4.0, _jit(i, 2.9) * TAU, 130.0)
					tree_count += 1
		lz -= 12.0
	m.g["north_tree_count"] = tree_count

	# Understory: brush, big leaves and flowers hug the path edges so the
	# corridor feels grown-in rather than mowed.
	var brush_count := 0
	var bkinds: Array[String] = ["plant_bush", "plant_bushLargeTriangle",
		"grass_leafsLarge", "plant_bush", "flower_purpleA", "grass_leafsLarge",
		"flower_redA", "plant_bushLargeTriangle", "flower_yellowB"]
	var bz := 306.0
	var bi := 0
	while bz > -100.0:
		var bside: float = -1.0 if bi % 2 == 0 else 1.0
		var bx: float = _path_x(bz) + bside * (8.5 + _jit(bi, 5.5) * 4.5)
		bi += 1
		if _north_flora_allowed("plant_bush", bx, bz):
			var by: float = _north_local(bx, bz)
			var plant: Node3D = m._nature(bkinds[bi % bkinds.size()],
				o + Vector3(bx, by - 0.15, bz), 2.6 + _jit(bi, 3.3) * 2.2,
				_jit(bi, 6.1) * TAU)
			if plant != null:
				m._set_vis_range(plant, 95.0)
			brush_count += 1
		bz -= 9.0
	m.g["north_brush_count"] = brush_count

	# Mushroom clusters dot the path edge; a few glow-mote orbs make the
	# deepest stands read as enchanted rather than dark.
	var shroom_count := 0
	var mz := 288.0
	var mi := 0
	while mz > -92.0:
		var mside: float = 1.0 if mi % 2 == 0 else -1.0
		var mx: float = _path_x(mz) + mside * (9.0 + _jit(mi, 8.8) * 6.0)
		mi += 1
		var mrole := "mushroom_red" if mi % 2 == 0 else "mushroom_tanGroup"
		if _north_flora_allowed(mrole, mx, mz):
			var my: float = _north_local(mx, mz)
			var asset_kind := "mushrooms_red" if mi % 2 == 0 else "mushrooms_tan"
			var plant: Node3D = _north_prop(asset_kind, o + Vector3(mx, my - 0.2, mz),
				4.6 + _jit(mi, 2.2) * 2.4, _jit(mi, 4.4) * TAU)
			if plant != null:
				m._set_vis_range(plant, 100.0)
			shroom_count += 1
			if mi % 3 == 0:
				var mote: MeshInstance3D = MeshInstance3D.new()
				var sm: SphereMesh = SphereMesh.new()
				sm.radius = 0.34
				sm.height = 0.68
				sm.radial_segments = 6
				sm.rings = 4
				mote.mesh = sm
				mote.material_override = m._soft_mat(Color(0.95, 0.62, 0.98), 1.6)
				mote.position = o + Vector3(mx + 1.6, my + 2.2, mz)
				mote.visibility_range_end = 90.0
				m.add_child(mote)
				m.game_nodes.append(mote)
		mz -= 26.0
	m.g["north_mushroom_count"] = shroom_count

	# Warm leaf-litter pads under the near trees: the ground cover carries
	# the same magenta/ochre note as the canopy.
	var li := 0
	var pz := 296.0
	while pz > -90.0:
		var pside: float = 1.0 if li % 2 == 0 else -1.0
		var px2: float = _path_x(pz) + pside * (11.0 + _jit(li, 1.9) * 8.0)
		li += 1
		if absf(px2 - _stream_x(pz)) > 8.0:
			var pad: MeshInstance3D = MeshInstance3D.new()
			var pm: CylinderMesh = CylinderMesh.new()
			pm.top_radius = 3.6 + _jit(li, 3.1) * 2.6
			pm.bottom_radius = pm.top_radius
			pm.height = 0.14
			pm.radial_segments = 9
			pad.mesh = pm
			var warm: Color = (Color(0.88, 0.46, 0.62) if li % 3 == 0
				else Color(0.90, 0.66, 0.40) if li % 3 == 1 else Color(0.72, 0.52, 0.70))
			pad.material_override = m._up_mat("grass", 0.10, warm)
			pad.position = o + Vector3(px2, _north_local(px2, pz) + 0.10, pz)
			pad.visibility_range_end = 85.0
			m.add_child(pad)
			m.game_nodes.append(pad)
		pz -= 24.0

	# Layered mist cards between the tree ranks: unshaded translucent panels
	# that catch the fog color and sell the wall-of-mist boundary.
	for card: Array in [
		[Vector2(-52.0, 250.0), 0.35], [Vector2(56.0, 220.0), -0.3],
		[Vector2(-60.0, 160.0), 0.2], [Vector2(58.0, 120.0), -0.25],
		[Vector2(-56.0, 55.0), 0.3], [Vector2(54.0, 10.0), -0.2],
		[Vector2(-52.0, -50.0), 0.25], [Vector2(50.0, -85.0), -0.3],
	]:
		var cp: Vector2 = card[0]
		var mist: MeshInstance3D = m._l2_box(
			o + Vector3(cp.x, _north_local(cp.x, cp.y) + 7.0, cp.y),
			Vector3(34.0, 13.0, 0.3), Color(0.90, 0.86, 0.94), 0.5)
		mist.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mist.material_override.albedo_color.a = 0.15
		mist.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		mist.rotation.y = float(card[1])
		mist.visibility_range_end = 150.0


func _build_spirit_clearings(o: Vector3) -> void:
	# Two open circles off the path — flattened, ringed by standing stones
	# with glowing element glyphs. These are the future spirit-boss arenas,
	# so the ground is kept clear and the stones carry all the dressing.
	var glyphs: Array[String] = ["✦", "❄", "▲", "●", "✦"]
	var stone_count := 0
	for ci in range(2):
		var cc: Vector2 = CLEARING_A if ci == 0 else CLEARING_B
		var tint: Color = (Color(0.95, 0.55, 0.98) if ci == 0
			else Color(0.55, 0.92, 0.98))
		for si in range(5):
			var ang: float = TAU * float(si) / 5.0 + float(ci) * 0.6
			var sp: Vector3 = o + Vector3(cc.x + cos(ang) * 13.0, 0.0,
				cc.y + sin(ang) * 13.0)
			sp.y = _north_local(sp.x - o.x, sp.z - o.z)
			var h: float = 5.6 + _jit(si + ci * 5, 2.4) * 2.2
			var stone: MeshInstance3D = m._l2_box(sp + Vector3(0, h * 0.5, 0),
				Vector3(2.4, h, 1.6), Color(0.48, 0.52, 0.64))
			stone.material_override = m._up_mat("cliff", 0.09, Color(0.52, 0.56, 0.68))
			stone.rotation.y = ang + 0.4
			m._wall_solid(sp + Vector3(0, h * 0.5, 0), Vector3(2.4, h, 1.6), 0.5)
			stone_count += 1

			var glyph: Label3D = Label3D.new()
			glyph.text = glyphs[si]
			glyph.font_size = 120
			glyph.pixel_size = 0.02
			glyph.outline_size = 20
			glyph.modulate = tint
			glyph.outline_modulate = Color(0.20, 0.16, 0.40)
			glyph.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			glyph.position = sp + Vector3(0, h + 1.3, 0)
			m.add_child(glyph)
			m.game_nodes.append(glyph)

		# a little stacked-stone altar marks the circle's heart (the spirit
		# boss will land here later)
		var ay: float = _north_local(cc.x, cc.y)
		for ai in range(3):
			var stone_w: float = 3.2 - float(ai) * 0.9
			var altar: MeshInstance3D = m._l2_box(
				o + Vector3(cc.x, ay + 0.5 + float(ai) * 0.85, cc.y),
				Vector3(stone_w, 0.9, stone_w * 0.8), Color(0.55, 0.58, 0.70))
			altar.material_override = m._up_mat("cliff", 0.10, Color(0.58, 0.61, 0.72))
			altar.rotation.y = float(ai) * 0.5
		m._cyl_solid(o + Vector3(cc.x, ay + 1.4, cc.y), 1.9, 1.4, 0.4)

		# a soft mote hovers over the circle's heart
		var heart: MeshInstance3D = MeshInstance3D.new()
		var hm: SphereMesh = SphereMesh.new()
		hm.radius = 0.9
		hm.height = 1.8
		hm.radial_segments = 8
		hm.rings = 5
		heart.mesh = hm
		heart.material_override = m._soft_mat(tint, 2.0)
		heart.position = o + Vector3(cc.x,
			_north_local(cc.x, cc.y) + 5.0, cc.y)
		heart.visibility_range_end = 120.0
		m.add_child(heart)
		m.game_nodes.append(heart)
	m.g["north_stone_count"] = stone_count


func _build_forest_pois(o: Vector3) -> void:
	# Discrete points of interest every 40-60u so the walk is a chain of
	# little discoveries at GROUND level — the reason not to fly over the
	# forest is that everything worth finding lives under the canopy.
	var pois := 0

	# 1. WATERFALL + POND: the stream tumbles off the pass shoulder into a
	# splash pool (the bowl is carved in _north_local).
	var fall_top: Vector3 = o + Vector3(15.0, _north_local(15.0, 278.0) + 1.2, 278.0)
	var fall_bot: Vector3 = o + Vector3(13.0, _north_local(13.0, 267.0) + 1.0, 267.0)
	for ci in range(2):
		var card: MeshInstance3D = m._l2_box(
			fall_top.lerp(fall_bot, 0.30 + float(ci) * 0.42),
			Vector3(5.0 - float(ci) * 1.2, 6.5, 0.6), Color(0.92, 0.98, 1.0), 0.7)
		card.material_override.albedo_texture = null   # pure water sheet, not brick
		card.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		card.material_override.albedo_color.a = 0.5
		card.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		card.rotation.x = -0.9
	for mi2 in range(3):
		var foam: MeshInstance3D = MeshInstance3D.new()
		var fs: SphereMesh = SphereMesh.new()
		fs.radius = 1.0 - float(mi2) * 0.2
		fs.height = fs.radius * 2.0
		fs.radial_segments = 7
		fs.rings = 4
		foam.mesh = fs
		foam.material_override = m._soft_mat(Color(0.95, 0.99, 1.0), 0.8)
		foam.position = fall_bot + Vector3(float(mi2 - 1) * 2.0, 0.4, 1.5)
		foam.visibility_range_end = 120.0
		m.add_child(foam)
		m.game_nodes.append(foam)
	for rk: Vector2 in [Vector2(8.0, 274.0), Vector2(21.0, 271.0), Vector2(7.0, 261.0)]:
		var rock: Node3D = m._nature("rock_largeA",
			o + Vector3(rk.x, _north_local(rk.x, rk.y) - 0.2, rk.y), 4.2, rk.x * 0.7)
		if rock != null:
			m._set_vis_range(rock, 120.0)
	pois += 1

	# 2. FAIRY RING: a mushroom circle with a glow heart — a dance spot.
	var ring_c := Vector2(-34.0, 214.0)
	for fi in range(7):
		var fang: float = TAU * float(fi) / 7.0
		var fp: Vector3 = o + Vector3(ring_c.x + cos(fang) * 5.0, 0.0,
			ring_c.y + sin(fang) * 5.0)
		fp.y = _north_local(fp.x - o.x, fp.z - o.z) - 0.15
		var shroom: Node3D = _north_prop("mushrooms_red" if fi % 2 == 0
			else "mushrooms_tan", fp, 2.4, fang)
		if shroom != null:
			m._set_vis_range(shroom, 110.0)
	var ring_heart: MeshInstance3D = MeshInstance3D.new()
	var rh: SphereMesh = SphereMesh.new()
	rh.radius = 0.55
	rh.height = 1.1
	rh.radial_segments = 8
	rh.rings = 5
	ring_heart.mesh = rh
	ring_heart.material_override = m._soft_mat(Color(0.98, 0.80, 0.45), 1.9)
	ring_heart.position = o + Vector3(ring_c.x,
		_north_local(ring_c.x, ring_c.y) + 2.6, ring_c.y)
	ring_heart.visibility_range_end = 110.0
	m.add_child(ring_heart)
	m.game_nodes.append(ring_heart)
	pois += 1

	# 3. FALLEN-LOG GATE: a mossy log rests on two stumps ACROSS the path —
	# Roshan swims right under it (solids only on the stumps).
	var log_z := 128.0
	var log_x: float = _path_x(log_z)
	for side: float in [-1.0, 1.0]:
		var sx2: float = log_x + side * 7.5
		var sy2: float = _north_local(sx2, log_z)
		var stump: MeshInstance3D = MeshInstance3D.new()
		var sm2: CylinderMesh = CylinderMesh.new()
		sm2.top_radius = 1.6
		sm2.bottom_radius = 2.0
		sm2.height = 5.4
		sm2.radial_segments = 8
		stump.mesh = sm2
		stump.material_override = m._castle_mat("wood", 0.14, Color(0.62, 0.46, 0.32))
		stump.position = o + Vector3(sx2, sy2 + 2.7, log_z)
		m.add_child(stump)
		m.game_nodes.append(stump)
		m._cyl_solid(stump.position, 2.0, 2.7, 0.4)
	var big_log: MeshInstance3D = MeshInstance3D.new()
	var blm: CylinderMesh = CylinderMesh.new()
	blm.top_radius = 1.9
	blm.bottom_radius = 1.9
	blm.height = 19.0
	blm.radial_segments = 9
	big_log.mesh = blm
	big_log.material_override = m._castle_mat("wood", 0.12, Color(0.58, 0.42, 0.30))
	big_log.rotation.z = PI * 0.5
	big_log.rotation.y = 0.12
	big_log.position = o + Vector3(log_x, _north_local(log_x, log_z) + 6.6, log_z)
	m.add_child(big_log)
	m.game_nodes.append(big_log)
	for gm in range(3):
		var moss: MeshInstance3D = m._l2_box(big_log.position
			+ Vector3(float(gm - 1) * 4.5, 1.6, 0.0),
			Vector3(2.6, 0.5, 2.2), Color(0.55, 0.80, 0.55))
		moss.material_override = m._up_mat("grass", 0.14, Color(0.60, 0.85, 0.58))
	pois += 1

	# 4. CRYSTAL GROTTO: rocks cradling glowing ice shards, cool against the
	# warm forest — a peek of the castle's ice long before it appears.
	var gro := Vector2(-30.0, 96.0)
	for rk2: Vector2 in [Vector2(-4.0, 2.0), Vector2(3.5, -1.5), Vector2(0.5, 4.5)]:
		var grock: Node3D = m._nature("cliff_block_rock",
			o + Vector3(gro.x + rk2.x, _north_local(gro.x + rk2.x, gro.y + rk2.y) - 0.3,
			gro.y + rk2.y), 5.0, rk2.x)
		if grock != null:
			m._set_vis_range(grock, 120.0)
	m._cyl_solid(o + Vector3(gro.x, _north_local(gro.x, gro.y) + 1.5, gro.y), 4.0, 1.5, 0.5)
	for si2 in range(5):
		var sang: float = TAU * float(si2) / 5.0
		var shard: MeshInstance3D = m._l2_box(
			o + Vector3(gro.x + cos(sang) * 2.4,
			_north_local(gro.x, gro.y) + 1.6 + float(si2 % 3) * 0.7,
			gro.y + sin(sang) * 2.4),
			Vector3(0.9, 2.8 + float(si2 % 2) * 1.3, 0.9),
			Color(0.62, 0.92, 1.0) if si2 % 2 == 0 else Color(0.90, 0.68, 1.0), 1.1)
		shard.rotation.z = cos(sang) * 0.35
		shard.rotation.x = sin(sang) * 0.35
	pois += 1

	# 5. BUTTERFLY HOLLOW: gen2 butterflies bob over a flower patch (they
	# ride the wisp ticker so they flutter without their own timer).
	var hollow := Vector2(30.0, 56.0)
	var wisps: Array = m.g.get("north_wisps", [])
	for bfi in range(3):
		var bpos: Vector3 = o + Vector3(hollow.x + float(bfi - 1) * 3.4,
			_north_local(hollow.x, hollow.y) + 3.0 + float(bfi) * 0.8,
			hollow.y + float(bfi % 2) * 2.6)
		var fly: Node3D = m._gen2_prop("butterfly_story", bpos, 1.7,
			float(bfi) * 2.1, 0.0)
		if fly != null:
			m.game_nodes.append(fly)
			wisps.append({"node": fly, "base": bpos})
	m.g["north_wisps"] = wisps
	for ffi in range(4):
		var flower: Node3D = m._nature(["flower_redA", "flower_yellowB",
			"flower_purpleA", "flower_redA"][ffi],
			o + Vector3(hollow.x - 3.0 + float(ffi) * 2.0,
			_north_local(hollow.x, hollow.y) + 0.1, hollow.y - 2.0), 1.9, float(ffi))
		if flower != null:
			m._set_vis_range(flower, 90.0)
	pois += 1

	# 6. PICNIC REST: a bench, a lantern and flowers at the halfway mark.
	var rest := Vector2(8.0, 4.0)
	var rest_y: float = _north_local(rest.x, rest.y)
	var bench2: Node3D = m._kit("park/bench", o + Vector3(rest.x, rest_y + 0.1, rest.y),
		3.2, -PI * 0.5)
	if bench2 != null:
		m._set_vis_range(bench2, 110.0)
	var rl_post: MeshInstance3D = m._l2_box(o + Vector3(rest.x + 2.4, rest_y + 2.2, rest.y),
		Vector3(0.5, 4.4, 0.5), Color(0.38, 0.26, 0.18))
	rl_post.material_override = m._castle_mat("wood", 0.2, Color(0.58, 0.42, 0.30))
	var rl_lamp: MeshInstance3D = MeshInstance3D.new()
	var rlm: SphereMesh = SphereMesh.new()
	rlm.radius = 0.6
	rlm.height = 1.2
	rlm.radial_segments = 8
	rlm.rings = 5
	rl_lamp.mesh = rlm
	rl_lamp.material_override = m._soft_mat(Color(1.0, 0.88, 0.55), 1.7)
	rl_lamp.position = o + Vector3(rest.x + 2.4, rest_y + 4.7, rest.y)
	rl_lamp.visibility_range_end = 120.0
	m.add_child(rl_lamp)
	m.game_nodes.append(rl_lamp)
	pois += 1

	# 7. RUINED GATE: two cracked, leaning pylons where an older kingdom's
	# road once had a gate — foreshadows the castle ahead.
	for side2: float in [-1.0, 1.0]:
		var px3: float = _path_x(-92.0) + side2 * 8.0
		var py3: float = _north_local(px3, -92.0)
		var pylon: MeshInstance3D = m._l2_box(o + Vector3(px3, py3 + 3.2, -92.0),
			Vector3(2.6, 6.4, 2.2), Color(0.52, 0.55, 0.66))
		pylon.material_override = m._up_mat("cliff", 0.09, Color(0.55, 0.58, 0.68))
		pylon.rotation.z = side2 * 0.12
		m._wall_solid(pylon.position, Vector3(2.6, 6.4, 2.2), 0.5)
	var fallen: MeshInstance3D = m._l2_box(
		o + Vector3(_path_x(-92.0) + 11.5, _north_local(_path_x(-92.0) + 11.5, -94.0) + 0.6,
		-94.0), Vector3(6.5, 1.4, 2.0), Color(0.50, 0.53, 0.64))
	fallen.material_override = m._up_mat("cliff", 0.09, Color(0.53, 0.56, 0.66))
	fallen.rotation.y = 0.5
	fallen.rotation.z = 0.1
	pois += 1

	# 8. LILY POND: pads float on the town river by the dock.
	for li2 in range(3):
		var pad2: MeshInstance3D = MeshInstance3D.new()
		var pdm: CylinderMesh = CylinderMesh.new()
		pdm.top_radius = 1.3 - float(li2) * 0.25
		pdm.bottom_radius = pdm.top_radius
		pdm.height = 0.12
		pdm.radial_segments = 9
		pad2.mesh = pdm
		pad2.material_override = m._up_mat("grass", 0.16, Color(0.42, 0.78, 0.52))
		pad2.position = o + Vector3(42.0 + float(li2) * 2.6,
			_north_local(44.0, -162.0) + 1.55, -162.0 - float(li2) * 2.0)
		pad2.visibility_range_end = 100.0
		m.add_child(pad2)
		m.game_nodes.append(pad2)
	var lily: Node3D = m._nature("flower_purpleA",
		o + Vector3(42.0, _north_local(44.0, -162.0) + 1.6, -162.0), 1.4, 0.6)
	if lily != null:
		m._set_vis_range(lily, 100.0)
	pois += 1

	m.g["north_poi_count"] = pois


func _build_town(o: Vector3) -> void:
	# Riverside town: ONE straight street between the western mountainside
	# and the eastern river — houses face the street from both sides, the
	# smith works under an open porch, and the mill turns on its own island.
	var houses: Array = [
		# [lp, authored kind, footprint] — west side backs onto the mountain
		[Vector2(-26, -150), "house_red", 26.0],     # the inn, biggest roofline
		[Vector2(-24, -196), "house_amber", 19.5],   # smith's house by the porch
		[Vector2(-26, -232), "house_aqua", 18.0],
		[Vector2(22, -138), "house_rose", 21.0],     # the trader greets arrivals
		[Vector2(24, -172), "house_blue", 18.0],
		[Vector2(24, -240), "house_orange", 18.0],
	]
	for row: Array in houses:
		_nordic_house(o, row[0], String(row[1]), float(row[2]))
	_build_mill(o)
	m.g["north_house_count"] = houses.size() + 1   # + the mill

	# Smith's open forge porch beside his house, facing the street.
	var forge_c: Vector3 = o + Vector3(-13.0, _north_local(-13.0, -206.0), -206.0)
	for px: Vector2 in [Vector2(-3.4, -3.0), Vector2(3.4, -3.0),
		Vector2(-3.4, 3.0), Vector2(3.4, 3.0)]:
		var post: MeshInstance3D = m._l2_box(forge_c + Vector3(px.x, 2.6, px.y),
			Vector3(0.7, 5.2, 0.7), Color(0.40, 0.25, 0.16))
		post.material_override = m._castle_mat("wood", 0.18, Color(0.66, 0.48, 0.34))
	var porch_roof: MeshInstance3D = m._l2_box(forge_c + Vector3(0, 5.6, 0),
		Vector3(9.0, 0.7, 8.2), Color(0.42, 0.30, 0.22))
	porch_roof.material_override = m._castle_mat("roof", 0.14, Color(0.60, 0.46, 0.34))
	var anvil: MeshInstance3D = m._l2_box(forge_c + Vector3(-1.2, 1.0, 0.6),
		Vector3(1.6, 1.0, 0.9), Color(0.35, 0.36, 0.42))
	anvil.material_override = m._up_mat("cliff", 0.14, Color(0.40, 0.42, 0.48))
	var hearth: MeshInstance3D = m._l2_box(forge_c + Vector3(1.8, 1.2, -1.2),
		Vector3(2.2, 2.4, 2.2), Color(0.52, 0.50, 0.56))
	hearth.material_override = m._up_mat("cliff", 0.11, Color(0.56, 0.54, 0.60))
	var ember: MeshInstance3D = m._l2_box(forge_c + Vector3(1.8, 2.55, -1.2),
		Vector3(1.4, 0.4, 1.4), Color(1.0, 0.55, 0.25), 1.6)
	ember.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	# Palisade stubs mark both town gates without enclosing anything.
	for gz: float in [-116.0, -252.0]:
		for side: float in [-1.0, 1.0]:
			for k in range(4):
				var gx: float = side * (9.0 + float(k) * 3.2)
				var gy: float = _north_local(gx, gz)
				var stake: MeshInstance3D = m._l2_box(o + Vector3(gx, gy + 2.2, gz),
					Vector3(1.1, 4.4 - float(k) * 0.35, 1.1), Color(0.46, 0.31, 0.20))
				stake.material_override = m._castle_mat("wood", 0.17, Color(0.68, 0.50, 0.34))
		# gate posts + pennant right at the road edge
		for side: float in [-1.0, 1.0]:
			var post_y: float = _north_local(side * 7.6, gz)
			var gpost: MeshInstance3D = m._l2_box(o + Vector3(side * 7.6, post_y + 3.4, gz),
				Vector3(1.3, 6.8, 1.3), Color(0.42, 0.28, 0.18))
			gpost.material_override = m._castle_mat("wood", 0.16, Color(0.64, 0.46, 0.32))
	var flag: Node3D = m._kit("castle/flag", o + Vector3(7.6,
		_north_local(7.6, -116.0) + 6.8, -116.0), 3.0, PI * 0.5)
	if flag != null:
		m._set_vis_range(flag, 150.0)

	# Street dressing: lantern posts, firewood, a fish-drying rack, benches.
	for lz: float in [-132.0, -160.0, -188.0, -216.0, -244.0]:
		var side: float = 1.0 if int(lz) % 3 == 0 else -1.0
		var lx: float = side * 8.4
		var ly: float = _north_local(lx, lz)
		var lpost: MeshInstance3D = m._l2_box(o + Vector3(lx, ly + 2.4, lz),
			Vector3(0.5, 4.8, 0.5), Color(0.38, 0.26, 0.18))
		lpost.material_override = m._castle_mat("wood", 0.2, Color(0.58, 0.42, 0.30))
		var lamp: MeshInstance3D = MeshInstance3D.new()
		var lm: SphereMesh = SphereMesh.new()
		lm.radius = 0.62
		lm.height = 1.24
		lm.radial_segments = 8
		lm.rings = 5
		lamp.mesh = lm
		lamp.material_override = m._soft_mat(Color(1.0, 0.88, 0.55), 1.7)
		lamp.position = o + Vector3(lx, ly + 5.1, lz)
		lamp.visibility_range_end = 130.0
		m.add_child(lamp)
		m.game_nodes.append(lamp)
	var wood_y: float = _north_local(-18.0, -212.0)
	for wk in range(3):
		var logrow: MeshInstance3D = m._l2_box(
			o + Vector3(-18.0, wood_y + 0.5 + float(wk) * 0.8, -212.0 - float(wk) * 0.1),
			Vector3(3.4, 0.8, 1.6 - float(wk) * 0.3), Color(0.52, 0.36, 0.24))
		logrow.material_override = m._castle_mat("wood", 0.2, Color(0.70, 0.52, 0.36))
	# authored dock steps off the street down to the river
	var dock: Node3D = _north_prop("fjord_dock",
		o + Vector3(35.0, _north_local(33.0, -158.0), -158.0), 13.0, -PI * 0.5)
	if dock != null:
		m._set_vis_range(dock, 150.0)
	# drying rack by the river
	var rack_y: float = _north_local(30.0, -186.0)
	for rx: float in [-2.2, 2.2]:
		var rpost: MeshInstance3D = m._l2_box(o + Vector3(30.0 + rx, rack_y + 1.9, -186.0),
			Vector3(0.5, 3.8, 0.5), Color(0.42, 0.28, 0.18))
		rpost.material_override = m._castle_mat("wood", 0.2, Color(0.62, 0.44, 0.30))
	var rbar: MeshInstance3D = m._l2_box(o + Vector3(30.0, rack_y + 3.6, -186.0),
		Vector3(5.4, 0.4, 0.4), Color(0.42, 0.28, 0.18))
	rbar.material_override = m._castle_mat("wood", 0.2, Color(0.62, 0.44, 0.30))
	for fi in range(3):
		var fish: MeshInstance3D = m._l2_box(
			o + Vector3(28.6 + float(fi) * 1.4, rack_y + 2.7, -186.0),
			Vector3(0.5, 1.4, 0.2), Color(0.62, 0.80, 0.86))
		fish.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	for bench_lp: Vector2 in [Vector2(9.0, -150.0), Vector2(-9.0, -170.0)]:
		var bench: Node3D = m._kit("park/bench",
			o + Vector3(bench_lp.x, _north_local(bench_lp.x, bench_lp.y) + 0.1, bench_lp.y),
			3.2, PI * 0.5 if bench_lp.x > 0.0 else -PI * 0.5)
		if bench != null:
			m._set_vis_range(bench, 110.0)

	# Garden patches behind the east cottages (the river keeps them green).
	for gp: Vector2 in [Vector2(31.0, -168.0), Vector2(31.0, -244.0)]:
		var gy2: float = _north_local(gp.x, gp.y)
		var soil: MeshInstance3D = m._l2_box(o + Vector3(gp.x, gy2 + 0.2, gp.y),
			Vector3(7.0, 0.4, 5.0), Color(0.46, 0.34, 0.24))
		soil.material_override = m._up_mat("grass", 0.12, Color(0.60, 0.46, 0.32))
		for fi2 in range(3):
			var fl: Node3D = m._nature(["flower_redA", "flower_yellowB",
				"flower_purpleA"][fi2], o + Vector3(gp.x - 2.0 + float(fi2) * 2.0,
				gy2 + 0.35, gp.y), 1.6, float(fi2) * 1.3)
			if fl != null:
				m._set_vis_range(fl, 80.0)


func _build_mill(o: Vector3) -> void:
	# The lumber mill sits on a little island in the river, reached by a
	# plank bridge — deck, turning water wheel, and a log ramp into the water.
	var c: Vector3 = o + Vector3(52.0, _north_local(52.0, -218.0), -218.0)
	var body: MeshInstance3D = m._l2_box(c + Vector3(0, 3.6, -1.0),
		Vector3(10.0, 7.2, 8.0), Color(0.60, 0.44, 0.30))
	body.material_override = m._castle_mat("wood", 0.16, Color(0.74, 0.56, 0.40))
	m._wall_solid(c + Vector3(0, 3.6, -1.0), Vector3(10.0, 7.2, 8.0), 0.6)
	for side: float in [-1.0, 1.0]:
		var roof: MeshInstance3D = m._l2_box(c + Vector3(side * 2.6, 8.2, -1.0),
			Vector3(6.6, 0.7, 9.4), Color(0.44, 0.32, 0.24))
		roof.rotation.z = side * 0.6
		roof.material_override = m._castle_mat("roof", 0.13, Color(0.58, 0.44, 0.32))
	# wrap-around work deck
	var deck: MeshInstance3D = m._l2_box(c + Vector3(0, 0.55, 3.6),
		Vector3(12.0, 0.7, 4.4), Color(0.52, 0.38, 0.26))
	deck.material_override = m._castle_mat("wood", 0.15, Color(0.78, 0.60, 0.44))
	# water wheel on the river side, spun in tick()
	var wheel_root: Node3D = Node3D.new()
	wheel_root.position = c + Vector3(-8.0, -1.35, -6.0)
	var wheel: MeshInstance3D = MeshInstance3D.new()
	var wm: CylinderMesh = CylinderMesh.new()
	wm.top_radius = 3.4
	wm.bottom_radius = 3.4
	wm.height = 1.0
	wm.radial_segments = 10
	wheel.mesh = wm
	wheel.material_override = m._castle_mat("wood", 0.14, Color(0.68, 0.50, 0.36))
	wheel.rotation.z = PI * 0.5
	wheel_root.add_child(wheel)
	for pk in range(6):
		var paddle: MeshInstance3D = MeshInstance3D.new()
		var pm: BoxMesh = BoxMesh.new()
		pm.size = Vector3(1.2, 7.6, 0.5)
		paddle.mesh = pm
		paddle.material_override = m._castle_mat("wood", 0.14, Color(0.62, 0.46, 0.32))
		paddle.rotation.x = TAU * float(pk) / 6.0
		wheel_root.add_child(paddle)
	m.add_child(wheel_root)
	m.game_nodes.append(wheel_root)
	var spins: Array = m.g.get("north_spins", [])
	spins.append({"node": wheel_root, "axis": "x", "speed": 0.7})
	m.g["north_spins"] = spins
	# log ramp + floating logs
	var ramp: MeshInstance3D = m._l2_box(c + Vector3(-4.0, 0.6, 4.4),
		Vector3(2.6, 0.5, 6.0), Color(0.52, 0.38, 0.26))
	ramp.rotation.x = -0.35
	ramp.material_override = m._castle_mat("wood", 0.16, Color(0.70, 0.52, 0.36))
	for lg in range(2):
		var flog: MeshInstance3D = MeshInstance3D.new()
		var fm: CylinderMesh = CylinderMesh.new()
		fm.top_radius = 0.7
		fm.bottom_radius = 0.7
		fm.height = 5.0
		fm.radial_segments = 7
		flog.mesh = fm
		flog.material_override = m._castle_mat("wood", 0.16, Color(0.66, 0.48, 0.34))
		flog.rotation.z = PI * 0.5
		flog.rotation.y = 0.4 * float(lg)
		flog.position = c + Vector3(-2.0 + float(lg) * 3.0, -1.1, 9.0 + float(lg) * 2.5)
		m.add_child(flog)
		m.game_nodes.append(flog)
	# plank bridge from the street bank across the channel (walk_h holds it)
	var bridge: MeshInstance3D = m._l2_box(o + Vector3(39.5, 2.35,
		-213.0), Vector3(17.0, 0.6, 4.6), Color(0.50, 0.36, 0.24))
	bridge.material_override = m._castle_mat("wood", 0.15, Color(0.76, 0.58, 0.42))
	for px: float in [33.0, 46.0]:
		var bpost: MeshInstance3D = m._l2_box(o + Vector3(px, 1.2, -215.2),
			Vector3(0.7, 3.4, 0.7), Color(0.40, 0.25, 0.16))
		bpost.material_override = m._castle_mat("wood", 0.18, Color(0.64, 0.46, 0.32))


func _nordic_house(o: Vector3, lp: Vector2, kind: String,
		footprint: float = 19.5) -> void:
	# Authored timber houses; each turns its gable/door face to the one
	# street, plus a warm smoke puff so the town reads lived-in.
	var gy: float = _north_local(lp.x, lp.y)
	var center: Vector3 = o + Vector3(lp.x, gy, lp.y)
	var inward_rotation: float = -PI * 0.5 if lp.x > 0.0 else PI * 0.5
	var house: Node3D = _north_prop(kind, center, footprint, inward_rotation)
	if house != null:
		m._set_vis_range(house, 205.0)
	var solid: float = footprint * 0.77
	m._wall_solid(center + Vector3(0.0, solid * 0.48, 0.0),
		Vector3(solid, solid * 0.96, solid), 0.7)
	var puff: MeshInstance3D = MeshInstance3D.new()
	var pmesh: SphereMesh = SphereMesh.new()
	pmesh.radius = 1.0
	pmesh.height = 2.0
	pmesh.radial_segments = 7
	pmesh.rings = 4
	puff.mesh = pmesh
	puff.material_override = m._soft_mat(Color(0.94, 0.93, 0.96), 0.5)
	puff.position = center + Vector3(footprint * 0.2, footprint * 0.72, footprint * 0.14)
	puff.visibility_range_end = 120.0
	m.add_child(puff)
	m.game_nodes.append(puff)


func _build_castle(o: Vector3) -> void:
	# The ice castle closes the stage on its plateau: curtain wall and gate,
	# a frozen-fountain forecourt, and the keep whose grand hall is real.
	var c: Vector3 = o + Vector3(CASTLE_LOCAL.x, HALL_FLOOR, CASTLE_LOCAL.y)
	var wall_col: Color = Color(0.78, 0.84, 0.96)
	var roof_col: Color = Color(0.32, 0.40, 0.66)

	# Curtain wall: front (gated), sides, back.
	for seg: Array in [
		[Vector3(-25.0, 7.0, 30.0), Vector3(38.0, 14.0, 3.6)],
		[Vector3(25.0, 7.0, 30.0), Vector3(38.0, 14.0, 3.6)],
		[Vector3(-44.0, 7.0, -4.0), Vector3(3.6, 14.0, 72.0)],
		[Vector3(44.0, 7.0, -4.0), Vector3(3.6, 14.0, 72.0)],
		[Vector3(0.0, 7.0, -38.0), Vector3(91.0, 14.0, 3.6)],
	]:
		_castle_wall(c + seg[0], seg[1], wall_col)
	var arch: MeshInstance3D = m._l2_box(c + Vector3(0, 14.5, 30.0),
		Vector3(14.0, 3.5, 4.0), wall_col.lightened(0.08))
	arch.material_override = m._castle_mat("wall", 0.07, wall_col.lightened(0.08))

	for tower_lp: Vector2 in [Vector2(-10.0, 30.0), Vector2(10.0, 30.0),
		Vector2(-44.0, -38.0), Vector2(44.0, -38.0)]:
		var tower_base: Vector3 = c + Vector3(tower_lp.x, -0.2, tower_lp.y)
		var tower: Node3D = m._kit("castle/tower-square", tower_base, 13.0)
		if tower != null:
			m._set_vis_range(tower, 320.0)
		m._cyl_solid(tower_base + Vector3(0, 8, 0), 5.8, 8.0, 0.6)
		m._kit("castle/flag", tower_base + Vector3(0, 17.0, 0), 2.4)

	# Forecourt: the fountain is FROZEN mid-splash — ice-tinted marble with
	# leaning glow jets arrested in the air.
	var fountain: Node3D = m._kit("park/fountain", c + Vector3(0, 0.15, 18.0), 10.0)
	if fountain != null:
		m._set_vis_range(fountain, 220.0)
		m._cyl_solid(c + Vector3(0, 3.0, 18.0), 4.2, 3.0, 0.5)
	for ji in range(5):
		var jang: float = TAU * float(ji) / 5.0
		var jet: MeshInstance3D = m._l2_box(
			c + Vector3(cos(jang) * 2.6, 4.6, 18.0 + sin(jang) * 2.6),
			Vector3(0.5, 3.4, 0.5), Color(0.72, 0.93, 1.0), 0.9)
		jet.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		jet.material_override.albedo_color.a = 0.6
		jet.rotation.z = cos(jang) * 0.5
		jet.rotation.x = -sin(jang) * 0.5

	# THE KEEP: walls with a grand door opening, rounded corner towers with
	# cone caps, gabled roof and a tall crowned spire.
	var front_z := 23.0     # keep front (door wall), lz -303 world-local
	var back_z := -23.0     # keep back, lz -349
	var half_w := 31.0
	var wall_h := 24.0
	# front wall: two segments + lintel leave a 10-wide door opening
	_castle_wall(c + Vector3(-18.25, wall_h * 0.5, front_z), Vector3(25.5, wall_h, 2.5), wall_col)
	_castle_wall(c + Vector3(18.25, wall_h * 0.5, front_z), Vector3(25.5, wall_h, 2.5), wall_col)
	_castle_wall(c + Vector3(0.0, 12.0 + (wall_h - 12.0) * 0.5, front_z),
		Vector3(11.0, wall_h - 12.0, 2.5), wall_col)
	_castle_wall(c + Vector3(-half_w, wall_h * 0.5, 0.0), Vector3(2.5, wall_h, 46.0), wall_col)
	_castle_wall(c + Vector3(half_w, wall_h * 0.5, 0.0), Vector3(2.5, wall_h, 46.0), wall_col)
	_castle_wall(c + Vector3(0.0, wall_h * 0.5, back_z), Vector3(64.0, wall_h, 2.5), wall_col)
	# gabled roof slabs over the hall — wide enough to close the eaves against
	# the side walls, so no sky gap is visible from inside the hall
	for side: float in [-1.0, 1.0]:
		var roof: MeshInstance3D = m._l2_box(c + Vector3(side * 12.0, wall_h + 3.6, 0.0),
			Vector3(29.0, 1.4, 50.0), roof_col)
		roof.rotation.z = side * 0.52
		roof.material_override = m._castle_mat("roof", 0.11, roof_col)
	# rounded corner towers — the "Elsa" silhouette is cylinders + cones
	for corner: Vector2 in [Vector2(-half_w, front_z), Vector2(half_w, front_z),
		Vector2(-half_w, back_z), Vector2(half_w, back_z)]:
		var rt: MeshInstance3D = MeshInstance3D.new()
		var rm: CylinderMesh = CylinderMesh.new()
		rm.top_radius = 4.6
		rm.bottom_radius = 5.2
		rm.height = 30.0
		rm.radial_segments = 10
		rt.mesh = rm
		rt.material_override = m._castle_mat("wall", 0.065, wall_col.lightened(0.05))
		rt.position = c + Vector3(corner.x, 15.0, corner.y)
		rt.visibility_range_end = 340.0
		m.add_child(rt)
		m.game_nodes.append(rt)
		m._cyl_solid(rt.position, 5.2, 15.0, 0.5)
		var cone: MeshInstance3D = MeshInstance3D.new()
		var cm: CylinderMesh = CylinderMesh.new()
		cm.top_radius = 0.0
		cm.bottom_radius = 5.8
		cm.height = 9.0
		cm.radial_segments = 10
		cone.mesh = cm
		cone.material_override = m._castle_mat("roof", 0.10, roof_col.lightened(0.10))
		cone.position = c + Vector3(corner.x, 34.5, corner.y)
		cone.visibility_range_end = 340.0
		m.add_child(cone)
		m.game_nodes.append(cone)
	# central spire
	var spire: MeshInstance3D = MeshInstance3D.new()
	var spm: CylinderMesh = CylinderMesh.new()
	spm.top_radius = 3.0
	spm.bottom_radius = 3.8
	spm.height = 44.0
	spm.radial_segments = 10
	spire.mesh = spm
	spire.material_override = m._castle_mat("wall", 0.06, wall_col.lightened(0.08))
	spire.position = c + Vector3(0.0, 22.0, -27.0)
	spire.visibility_range_end = 380.0
	m.add_child(spire)
	m.game_nodes.append(spire)
	var spire_cone: MeshInstance3D = MeshInstance3D.new()
	var scm: CylinderMesh = CylinderMesh.new()
	scm.top_radius = 0.0
	scm.bottom_radius = 4.6
	scm.height = 11.0
	scm.radial_segments = 10
	spire_cone.mesh = scm
	spire_cone.material_override = m._castle_mat("roof", 0.10, roof_col.lightened(0.14))
	spire_cone.position = c + Vector3(0.0, 49.5, -27.0)
	spire_cone.visibility_range_end = 380.0
	m.add_child(spire_cone)
	m.game_nodes.append(spire_cone)
	# glowing facade windows — tall cyan slits
	for wx: float in [-12.0, 12.0]:
		var slit: MeshInstance3D = m._l2_box(c + Vector3(wx, 15.0, front_z + 1.4),
			Vector3(2.2, 7.5, 0.3), Color(0.55, 0.92, 1.0), 1.1)
		slit.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	var crown: Label3D = Label3D.new()
	crown.text = "♛"
	crown.font_size = 290
	crown.pixel_size = 0.028
	crown.outline_size = 32
	crown.modulate = Color(1.0, 0.84, 0.36)
	crown.outline_modulate = Color(0.24, 0.22, 0.48)
	crown.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	crown.position = c + Vector3(0, 57.0, -27.0)
	m.add_child(crown)
	m.game_nodes.append(crown)
	var star: Label3D = Label3D.new()
	star.text = "✦"
	star.font_size = 180
	star.pixel_size = 0.024
	star.outline_size = 24
	star.modulate = Color(0.72, 0.96, 1.0)
	star.outline_modulate = Color(0.20, 0.24, 0.50)
	star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	star.position = c + Vector3(0, 14.5, front_z + 1.0)
	m.add_child(star)
	m.game_nodes.append(star)

	# ---- BUILD-OUT PASS: the palace needs real massing, not four walls ----
	# Gatehouse: mini turrets + a little balcony crown the grand door.
	for side: float in [-1.0, 1.0]:
		var mt: MeshInstance3D = MeshInstance3D.new()
		var mtm: CylinderMesh = CylinderMesh.new()
		mtm.top_radius = 1.6
		mtm.bottom_radius = 1.9
		mtm.height = 15.0
		mtm.radial_segments = 8
		mt.mesh = mtm
		mt.material_override = m._castle_mat("wall", 0.07, wall_col.lightened(0.06))
		mt.position = c + Vector3(side * 6.8, 7.5, front_z + 0.6)
		m.add_child(mt)
		m.game_nodes.append(mt)
		var mtc: MeshInstance3D = MeshInstance3D.new()
		var mtcm: CylinderMesh = CylinderMesh.new()
		mtcm.top_radius = 0.0
		mtcm.bottom_radius = 2.3
		mtcm.height = 4.2
		mtcm.radial_segments = 8
		mtc.mesh = mtcm
		mtc.material_override = m._castle_mat("roof", 0.10, roof_col.lightened(0.12))
		mtc.position = c + Vector3(side * 6.8, 17.1, front_z + 0.6)
		m.add_child(mtc)
		m.game_nodes.append(mtc)
	var balcony: MeshInstance3D = m._l2_box(c + Vector3(0.0, 13.2, front_z + 1.6),
		Vector3(10.0, 0.8, 2.6), wall_col.lightened(0.08))
	balcony.material_override = m._castle_mat("wall", 0.08, wall_col.lightened(0.08))
	for bp in range(5):
		var bpost: MeshInstance3D = m._l2_box(
			c + Vector3(-4.0 + float(bp) * 2.0, 14.4, front_z + 2.6),
			Vector3(0.35, 1.6, 0.35), wall_col.lightened(0.10))
		bpost.material_override = m._castle_mat("wall", 0.09, wall_col.lightened(0.10))

	# Facade banners in the bedroom quilt colors.
	for bside: float in [-1.0, 1.0]:
		var banner: MeshInstance3D = m._l2_box(
			c + Vector3(bside * 13.0, 16.0, front_z + 1.5),
			Vector3(2.4, 5.6, 0.3),
			Color(0.92, 0.55, 0.68) if bside < 0.0 else Color(0.55, 0.75, 0.94))
		banner.material_override = m._castle_mat("fabric", 0.15,
			Color(0.94, 0.62, 0.74) if bside < 0.0 else Color(0.62, 0.80, 0.96))
		var btip: MeshInstance3D = m._l2_box(
			c + Vector3(bside * 13.0, 12.9, front_z + 1.5),
			Vector3(1.4, 0.8, 0.3), Color(1.0, 0.86, 0.44), 0.4)
		btip.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	# Buttresses give the long side walls their gothic rhythm.
	for side3: float in [-1.0, 1.0]:
		for bz2: float in [14.0, 0.0, -14.0]:
			var butt: MeshInstance3D = m._l2_box(
				c + Vector3(side3 * (half_w + 1.8), 5.0, bz2),
				Vector3(2.4, 11.0, 3.0), wall_col.darkened(0.04))
			butt.material_override = m._castle_mat("wall", 0.08, wall_col.darkened(0.02))
			butt.rotation.z = -side3 * 0.16

	# Window rows on the flanks and back so every face glows at dusk.
	for side4: float in [-1.0, 1.0]:
		for wz2: float in [12.0, -2.0, -16.0]:
			var slit2: MeshInstance3D = m._l2_box(
				c + Vector3(side4 * (half_w + 1.35), 14.0, wz2),
				Vector3(0.3, 6.0, 2.0), Color(0.55, 0.92, 1.0), 1.0)
			slit2.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	for wx2: float in [-10.0, 10.0]:
		var bslit: MeshInstance3D = m._l2_box(c + Vector3(wx2, 15.0, back_z - 1.35),
			Vector3(2.0, 6.0, 0.3), Color(0.55, 0.92, 1.0), 1.0)
		bslit.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	# Crenellated curtain wall: merlons march along the front rampart.
	for mx in range(-8, 9):
		var mxf: float = float(mx) * 5.0
		if absf(mxf) < 8.0:
			continue
		var merlon: MeshInstance3D = m._l2_box(c + Vector3(mxf, 15.1, 30.0),
			Vector3(2.4, 2.2, 3.8), wall_col.lightened(0.04))
		merlon.material_override = m._castle_mat("wall", 0.08, wall_col.lightened(0.04))

	# The tall REAR KEEP block layers the silhouette the way the reference
	# palace stacks toward its spires (pure exterior massing, above the
	# hall's interior ceiling zone).
	var rear: MeshInstance3D = m._l2_box(c + Vector3(0.0, 30.0, -15.0),
		Vector3(42.0, 14.0, 20.0), wall_col.lightened(0.03))
	rear.material_override = m._castle_mat("wall", 0.06, wall_col.lightened(0.03))
	for side5: float in [-1.0, 1.0]:
		var rroof: MeshInstance3D = m._l2_box(c + Vector3(side5 * 8.5, 39.4, -15.0),
			Vector3(21.0, 1.2, 23.0), roof_col)
		rroof.rotation.z = side5 * 0.5
		rroof.material_override = m._castle_mat("roof", 0.10, roof_col)
	for rwx: float in [-13.0, 0.0, 13.0]:
		var rslit: MeshInstance3D = m._l2_box(c + Vector3(rwx, 30.5, -3.9),
			Vector3(2.0, 6.5, 0.3), Color(0.55, 0.92, 1.0), 1.0)
		rslit.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	# satellite spires complete the cluster around the existing central one
	for sside: float in [-1.0, 1.0]:
		var sat: MeshInstance3D = MeshInstance3D.new()
		var satm: CylinderMesh = CylinderMesh.new()
		satm.top_radius = 1.9
		satm.bottom_radius = 2.4
		satm.height = 30.0
		satm.radial_segments = 9
		sat.mesh = satm
		sat.material_override = m._castle_mat("wall", 0.06, wall_col.lightened(0.07))
		sat.position = c + Vector3(sside * 10.0, 30.0, -24.0)
		sat.visibility_range_end = 380.0
		m.add_child(sat)
		m.game_nodes.append(sat)
		var satc: MeshInstance3D = MeshInstance3D.new()
		var satcm: CylinderMesh = CylinderMesh.new()
		satcm.top_radius = 0.0
		satcm.bottom_radius = 3.0
		satcm.height = 8.0
		satcm.radial_segments = 9
		satc.mesh = satcm
		satc.material_override = m._castle_mat("roof", 0.10, roof_col.lightened(0.14))
		satc.position = c + Vector3(sside * 10.0, 49.0, -24.0)
		satc.visibility_range_end = 380.0
		m.add_child(satc)
		m.game_nodes.append(satc)

	# Ice lanterns line the forecourt walk from the gate to the door.
	for lz2: float in [26.0, 21.0, 16.0, 11.0]:
		for lside: float in [-1.0, 1.0]:
			var lpost2: MeshInstance3D = m._l2_box(c + Vector3(lside * 7.0, 1.6, lz2),
				Vector3(0.5, 3.2, 0.5), wall_col.darkened(0.06))
			lpost2.material_override = m._castle_mat("wall", 0.09, wall_col.darkened(0.03))
			var lorb: MeshInstance3D = MeshInstance3D.new()
			var lom: SphereMesh = SphereMesh.new()
			lom.radius = 0.55
			lom.height = 1.1
			lom.radial_segments = 8
			lom.rings = 5
			lorb.mesh = lom
			lorb.material_override = m._soft_mat(Color(0.75, 0.94, 1.0), 1.6)
			lorb.position = c + Vector3(lside * 7.0, 3.6, lz2)
			lorb.visibility_range_end = 150.0
			m.add_child(lorb)
			m.game_nodes.append(lorb)


func _build_grand_hall(o: Vector3) -> void:
	# INSIDE the keep: a tall ice hall. Frozen fountain centerpiece, six
	# pillars on a hex ring, twin staircases sweeping up the side walls to a
	# mezzanine holding three little bedrooms. Floors are made real through
	# m.arena_zones ramps/bands (same system as the Sky Lagoon castle).
	var c: Vector3 = o + Vector3(0.0, HALL_FLOOR, -326.0)
	var ice: Color = Color(0.80, 0.90, 1.0)
	var ice_deep: Color = Color(0.46, 0.62, 0.92)

	# polished floor slab + a six-point star inlay
	var floor_slab: MeshInstance3D = m._l2_box(c + Vector3(0, -0.1, 0),
		Vector3(60.0, 0.5, 44.0), ice.lightened(0.05))
	floor_slab.material_override = m._castle_mat("marble", 0.10, Color(0.88, 0.95, 1.0))
	var inlay: Label3D = Label3D.new()
	inlay.text = "✦"
	inlay.font_size = 420
	inlay.pixel_size = 0.03
	inlay.modulate = Color(0.62, 0.88, 1.0, 0.85)
	inlay.outline_size = 30
	inlay.outline_modulate = Color(0.30, 0.44, 0.80)
	inlay.rotation.x = -PI * 0.5
	inlay.position = c + Vector3(0, 0.35, 4.0)
	inlay.no_depth_test = false
	m.add_child(inlay)
	m.game_nodes.append(inlay)

	# hex ring of ice pillars (phased so the door->fountain axis stays clear)
	for pi in range(6):
		var ang: float = TAU * float(pi) / 6.0
		var pp: Vector3 = c + Vector3(cos(ang) * 15.0, 8.0, sin(ang) * 11.0 + 2.0)
		var pillar: MeshInstance3D = MeshInstance3D.new()
		var pm: CylinderMesh = CylinderMesh.new()
		pm.top_radius = 1.3
		pm.bottom_radius = 1.7
		pm.height = 16.0
		pm.radial_segments = 8
		pillar.mesh = pm
		pillar.material_override = m._castle_mat("marble", 0.09, ice)
		pillar.position = pp
		m.add_child(pillar)
		m.game_nodes.append(pillar)
		m._cyl_solid(pp, 1.7, 8.0, 0.4)

	# frozen fountain centerpiece: stacked ice tiers + arrested glow jets
	var f_c: Vector3 = c + Vector3(0.0, 0.0, 6.0)
	for tier: Array in [[4.6, 1.2, 0.6], [2.9, 1.0, 1.7], [1.5, 2.2, 3.2]]:
		var td: MeshInstance3D = MeshInstance3D.new()
		var tm: CylinderMesh = CylinderMesh.new()
		tm.top_radius = float(tier[0]) * 0.85
		tm.bottom_radius = float(tier[0])
		tm.height = float(tier[1])
		tm.radial_segments = 10
		td.mesh = tm
		td.material_override = m._castle_mat("marble", 0.08, Color(0.84, 0.94, 1.0))
		td.position = f_c + Vector3(0, float(tier[2]), 0)
		m.add_child(td)
		m.game_nodes.append(td)
	m._cyl_solid(f_c + Vector3(0, 2.0, 0), 4.6, 2.0, 0.4)
	for ji in range(6):
		var jang: float = TAU * float(ji) / 6.0
		var jet: MeshInstance3D = m._l2_box(
			f_c + Vector3(cos(jang) * 2.2, 5.2, sin(jang) * 2.2),
			Vector3(0.4, 2.8, 0.4), Color(0.72, 0.94, 1.0), 1.0)
		jet.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		jet.material_override.albedo_color.a = 0.6
		jet.rotation.z = cos(jang) * 0.55
		jet.rotation.x = -sin(jang) * 0.55

	# interior wall glow windows
	for side: float in [-1.0, 1.0]:
		for wz: float in [-10.0, 4.0]:
			var slit: MeshInstance3D = m._l2_box(c + Vector3(side * 29.6, 12.0, wz),
				Vector3(0.3, 8.0, 2.4), Color(0.55, 0.92, 1.0), 1.0)
			slit.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	# TWIN SWEEPING STAIRCASES: straight runs up the side walls whose last
	# steps arc inward onto the mezzanine — the rounded-stair read with an
	# axis-aligned ramp underneath (m.arena_zones does the walking).
	for side: float in [-1.0, 1.0]:
		for si in range(12):
			var t: float = float(si) / 11.0
			var step_z: float = 18.0 - float(si) * 2.35
			var curve_in: float = maxf(0.0, float(si - 8)) * 1.5
			var sp: Vector3 = c + Vector3(side * (24.0 - curve_in),
				(MEZZ_FLOOR - HALL_FLOOR) * t + 0.45, step_z)
			var stp: MeshInstance3D = m._l2_box(sp, Vector3(7.6, 0.9, 2.5), ice_deep)
			stp.material_override = m._castle_mat("marble", 0.09, Color(0.72, 0.84, 1.0))
			stp.rotation.y = side * minf(float(maxi(0, si - 8)) * 0.16, 0.5)
		# a sweeping banister follows each flight
		var ban: MeshInstance3D = m._l2_box(c + Vector3(side * 20.2,
			(MEZZ_FLOOR - HALL_FLOOR) * 0.5 + 1.6, 4.0),
			Vector3(0.5, 0.6, 29.0), ice_deep)
		ban.rotation.x = -atan2(MEZZ_FLOOR - HALL_FLOOR, 28.0)
		ban.material_override = m._castle_mat("marble", 0.10, Color(0.66, 0.80, 1.0))

	# MEZZANINE slab across the back + guardrail with stair-landing gaps
	var mezz_y: float = MEZZ_FLOOR - HALL_FLOOR
	var mezz: MeshInstance3D = m._l2_box(c + Vector3(0, mezz_y - 0.45, -14.5),
		Vector3(60.0, 0.9, 15.0), ice.lightened(0.03))
	mezz.material_override = m._castle_mat("marble", 0.09, Color(0.86, 0.93, 1.0))
	for rx in range(-4, 5):
		var post: MeshInstance3D = m._l2_box(
			c + Vector3(float(rx) * 4.6, mezz_y + 0.9, -7.4),
			Vector3(0.4, 1.8, 0.4), ice_deep)
		post.material_override = m._castle_mat("marble", 0.10, Color(0.70, 0.82, 1.0))
	var rail: MeshInstance3D = m._l2_box(c + Vector3(0, mezz_y + 1.8, -7.4),
		Vector3(41.0, 0.4, 0.5), ice_deep)
	rail.material_override = m._castle_mat("marble", 0.10, Color(0.70, 0.82, 1.0))

	# THREE BEDROOMS along the mezzanine: open bays with arched headers,
	# little beds, rugs, lamps and a bookcase each.
	var bay_x: Array[float] = [-19.0, 0.0, 19.0]
	var quilts: Array[Color] = [Color(0.92, 0.55, 0.68), Color(0.55, 0.75, 0.94),
		Color(0.72, 0.62, 0.94)]
	for bi in range(3):
		var bx: float = bay_x[bi]
		# partition walls between bays
		if bi < 2:
			var part: MeshInstance3D = m._l2_box(
				c + Vector3(bx + 9.5, mezz_y + 4.0, -15.0),
				Vector3(0.8, 8.0, 13.0), ice)
			part.material_override = m._castle_mat("marble", 0.09, ice)
			m._wall_solid(part.position, Vector3(0.8, 8.0, 13.0), 0.4)
		# arched header over each bay's opening
		var header: MeshInstance3D = m._l2_box(
			c + Vector3(bx, mezz_y + 7.0, -8.2), Vector3(14.0, 2.4, 0.8), ice)
		header.material_override = m._castle_mat("marble", 0.09, ice)
		# bed: frame, mattress, pillow, headboard
		var bed_c: Vector3 = c + Vector3(bx, mezz_y, -18.0)
		var frame: MeshInstance3D = m._l2_box(bed_c + Vector3(0, 0.6, 0),
			Vector3(4.6, 1.2, 6.6), Color(0.52, 0.38, 0.26))
		frame.material_override = m._castle_mat("wood", 0.16, Color(0.70, 0.52, 0.36))
		var quilt: MeshInstance3D = m._l2_box(bed_c + Vector3(0, 1.45, 0.6),
			Vector3(4.2, 0.6, 5.0), quilts[bi])
		quilt.material_override = m._castle_mat("fabric", 0.14, quilts[bi])
		var pillow: MeshInstance3D = m._l2_box(bed_c + Vector3(0, 1.6, -2.4),
			Vector3(3.2, 0.6, 1.4), Color(0.97, 0.96, 0.92))
		pillow.material_override = m._castle_mat("fabric", 0.16, Color(0.97, 0.96, 0.92))
		var headboard: MeshInstance3D = m._l2_box(bed_c + Vector3(0, 1.9, -3.3),
			Vector3(4.6, 2.6, 0.5), Color(0.48, 0.34, 0.24))
		headboard.material_override = m._castle_mat("wood", 0.16, Color(0.66, 0.48, 0.34))
		# rug
		var rug: MeshInstance3D = MeshInstance3D.new()
		var rm: CylinderMesh = CylinderMesh.new()
		rm.top_radius = 2.6
		rm.bottom_radius = 2.6
		rm.height = 0.12
		rm.radial_segments = 10
		rug.mesh = rm
		rug.material_override = m._castle_mat("fabric", 0.13, quilts[bi].lightened(0.25))
		rug.position = c + Vector3(bx, mezz_y + 0.12, -11.5)
		m.add_child(rug)
		m.game_nodes.append(rug)
		# bedside lamp
		var lamp: MeshInstance3D = MeshInstance3D.new()
		var lm: SphereMesh = SphereMesh.new()
		lm.radius = 0.5
		lm.height = 1.0
		lm.radial_segments = 8
		lm.rings = 5
		lamp.mesh = lm
		lamp.material_override = m._soft_mat(Color(1.0, 0.88, 0.60), 1.5)
		lamp.position = c + Vector3(bx + 3.2, mezz_y + 1.8, -18.5)
		m.add_child(lamp)
		m.game_nodes.append(lamp)
		var bookcase: Node3D = m._kit("furniture/bookcase",
			c + Vector3(bx - 5.2, mezz_y, -19.0), 3.4)
		if bookcase != null:
			m._set_vis_range(bookcase, 90.0)
	m.g["north_bedroom_count"] = 3

	# chandelier: a slow-turning glow ring high over the fountain
	var chand_root: Node3D = Node3D.new()
	chand_root.position = c + Vector3(0, 19.0, 2.0)
	var chand_ring: MeshInstance3D = MeshInstance3D.new()
	var tor: TorusMesh = TorusMesh.new()
	tor.inner_radius = 3.4
	tor.outer_radius = 4.0
	tor.rings = 12
	tor.ring_segments = 6
	chand_ring.mesh = tor
	chand_ring.material_override = m._soft_mat(Color(0.75, 0.92, 1.0), 1.1)
	chand_root.add_child(chand_ring)
	for oi in range(6):
		var oang: float = TAU * float(oi) / 6.0
		var orb: MeshInstance3D = MeshInstance3D.new()
		var om: SphereMesh = SphereMesh.new()
		om.radius = 0.6
		om.height = 1.2
		om.radial_segments = 8
		om.rings = 5
		orb.mesh = om
		orb.material_override = m._soft_mat(Color(0.88, 0.97, 1.0), 1.9)
		orb.position = Vector3(cos(oang) * 3.7, -0.4, sin(oang) * 3.7)
		chand_root.add_child(orb)
	var rod: MeshInstance3D = MeshInstance3D.new()
	var rodm: CylinderMesh = CylinderMesh.new()
	rodm.top_radius = 0.18
	rodm.bottom_radius = 0.18
	rodm.height = 4.5
	rodm.radial_segments = 6
	rod.mesh = rodm
	rod.material_override = m._castle_mat("marble", 0.1, Color(0.80, 0.88, 1.0))
	rod.position = Vector3(0, 2.6, 0)
	chand_root.add_child(rod)
	m.add_child(chand_root)
	m.game_nodes.append(chand_root)
	var spins: Array = m.g.get("north_spins", [])
	spins.append({"node": chand_root, "axis": "y", "speed": 0.25})
	m.g["north_spins"] = spins

	# ---- INTERIOR DRESSING PASS: the hall reads royal, not empty ----
	# Indigo carpet runner from the grand door to the frozen fountain.
	var carpet: MeshInstance3D = m._l2_box(c + Vector3(0.0, 0.32, 15.5),
		Vector3(5.2, 0.22, 15.0), Color(0.30, 0.32, 0.58))
	carpet.material_override = m._castle_mat("fabric", 0.12, Color(0.38, 0.40, 0.66))
	var carpet2: MeshInstance3D = m._l2_box(c + Vector3(0.0, 0.32, -2.0),
		Vector3(5.2, 0.22, 8.0), Color(0.30, 0.32, 0.58))
	carpet2.material_override = m._castle_mat("fabric", 0.12, Color(0.38, 0.40, 0.66))

	# Hanging banners along both side walls.
	for bside2: float in [-1.0, 1.0]:
		for bi2 in range(2):
			var wb: MeshInstance3D = m._l2_box(
				c + Vector3(bside2 * 28.6, 13.5, -4.0 + float(bi2) * 12.0),
				Vector3(0.3, 6.4, 2.8), quilts[bi2 if bside2 < 0.0 else 2 - bi2])
			wb.material_override = m._castle_mat("fabric", 0.14,
				quilts[bi2 if bside2 < 0.0 else 2 - bi2].lightened(0.1))
			var wbt: MeshInstance3D = m._l2_box(
				c + Vector3(bside2 * 28.6, 10.0, -4.0 + float(bi2) * 12.0),
				Vector3(0.3, 0.7, 1.6), Color(1.0, 0.86, 0.44), 0.4)
			wbt.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	# Vault ribs rise from the pillar ring to a glowing boss — the ceiling
	# reads as a six-fold crystal vault instead of a void.
	var apex: Vector3 = c + Vector3(0.0, 21.0, 2.0)
	for ri in range(6):
		var rang: float = TAU * float(ri) / 6.0
		var rstart: Vector3 = c + Vector3(cos(rang) * 15.0, 16.0, sin(rang) * 11.0 + 2.0)
		var rdir: Vector3 = apex - rstart
		var rib: MeshInstance3D = m._l2_box(rstart + rdir * 0.5,
			Vector3(0.7, 0.7, rdir.length()), ice_deep)
		rib.material_override = m._castle_mat("marble", 0.10, Color(0.70, 0.84, 1.0))
		rib.rotation.y = atan2(rdir.x, rdir.z)
		rib.rotation.x = -atan2(rdir.y, Vector2(rdir.x, rdir.z).length())
	var boss: MeshInstance3D = MeshInstance3D.new()
	var bossm: SphereMesh = SphereMesh.new()
	bossm.radius = 1.0
	bossm.height = 2.0
	bossm.radial_segments = 8
	bossm.rings = 5
	boss.mesh = bossm
	boss.material_override = m._soft_mat(Color(0.85, 0.96, 1.0), 1.6)
	boss.position = apex
	m.add_child(boss)
	m.game_nodes.append(boss)

	# A warm fireplace nook under the mezzanine breaks the ice palette —
	# the snuggest corner of the palace lives beneath the bedrooms.
	var fire_c: Vector3 = c + Vector3(-20.0, 0.0, -21.4)
	var breast: MeshInstance3D = m._l2_box(fire_c + Vector3(0.0, 4.5, 0.0),
		Vector3(5.4, 9.0, 2.4), Color(0.62, 0.64, 0.74))
	breast.material_override = m._up_mat("cliff", 0.09, Color(0.66, 0.67, 0.76))
	m._wall_solid(breast.position, Vector3(5.4, 9.0, 2.4), 0.4)
	var mantel: MeshInstance3D = m._l2_box(fire_c + Vector3(0.0, 3.4, 0.9),
		Vector3(4.6, 0.5, 1.4), Color(0.55, 0.57, 0.68))
	mantel.material_override = m._up_mat("cliff", 0.10, Color(0.60, 0.62, 0.72))
	var ember2: MeshInstance3D = m._l2_box(fire_c + Vector3(0.0, 1.2, 0.9),
		Vector3(2.6, 2.0, 0.8), Color(1.0, 0.58, 0.28), 1.5)
	ember2.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	for st_i in range(2):
		var stool: MeshInstance3D = m._l2_box(
			fire_c + Vector3(-1.8 + float(st_i) * 3.6, 0.55, 3.6),
			Vector3(1.3, 1.1, 1.3), Color(0.60, 0.44, 0.30))
		stool.material_override = m._castle_mat("wood", 0.16, Color(0.72, 0.54, 0.38))

	# Two little thrones overlook the hall from the mezzanine rail.
	for tside: float in [-1.0, 1.0]:
		var tc: Vector3 = c + Vector3(tside * 2.9, mezz_y, -10.2)
		var seat: MeshInstance3D = m._l2_box(tc + Vector3(0.0, 0.65, 0.0),
			Vector3(2.3, 1.3, 2.1), Color(0.86, 0.92, 1.0))
		seat.material_override = m._castle_mat("marble", 0.10, Color(0.88, 0.94, 1.0))
		var back: MeshInstance3D = m._l2_box(tc + Vector3(0.0, 2.6, -0.85),
			Vector3(2.3, 3.6, 0.5), Color(0.82, 0.90, 1.0))
		back.material_override = m._castle_mat("marble", 0.10, Color(0.86, 0.92, 1.0))
		var finial: MeshInstance3D = MeshInstance3D.new()
		var fm2: SphereMesh = SphereMesh.new()
		fm2.radius = 0.4
		fm2.height = 0.8
		fm2.radial_segments = 8
		fm2.rings = 5
		finial.mesh = fm2
		finial.material_override = m._soft_mat(Color(1.0, 0.86, 0.44), 1.4)
		finial.position = tc + Vector3(0.0, 4.7, -0.85)
		m.add_child(finial)
		m.game_nodes.append(finial)

	# Newel orbs mark each staircase foot; per-bay windows + toy chests
	# finish the bedrooms.
	for nside: float in [-1.0, 1.0]:
		var newel: MeshInstance3D = MeshInstance3D.new()
		var nm: SphereMesh = SphereMesh.new()
		nm.radius = 0.7
		nm.height = 1.4
		nm.radial_segments = 8
		nm.rings = 5
		newel.mesh = nm
		newel.material_override = m._soft_mat(Color(0.78, 0.94, 1.0), 1.3)
		newel.position = c + Vector3(nside * 24.0, 2.2, 19.8)
		m.add_child(newel)
		m.game_nodes.append(newel)
	for bwi in range(3):
		var bwx: float = bay_x[bwi]
		var bwin: MeshInstance3D = m._l2_box(
			c + Vector3(bwx, mezz_y + 4.6, -22.3),
			Vector3(2.6, 3.8, 0.3), Color(0.62, 0.94, 1.0), 1.1)
		bwin.material_override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		var chest: MeshInstance3D = m._l2_box(
			c + Vector3(bwx + 4.6, mezz_y + 0.7, -13.2),
			Vector3(2.3, 1.4, 1.5), Color(0.58, 0.42, 0.28))
		chest.material_override = m._castle_mat("wood", 0.16, Color(0.72, 0.54, 0.38))
		var lid: MeshInstance3D = m._l2_box(
			c + Vector3(bwx + 4.6, mezz_y + 1.5, -13.2),
			Vector3(2.4, 0.35, 1.6), quilts[bwi])
		lid.material_override = m._castle_mat("fabric", 0.15, quilts[bwi])

	# ---------- the y-banded zones that make the hall's stories real
	# (rects are lx/lz local to NORTHERN_POS; floors/ceils relative to its y)
	var hall_top: float = HALL_FLOOR + 21.0
	m.arena_zones.append({"rect": Rect2(-30.0, -348.0, 60.0, 44.0),
		"band": Vector2(0.0, 40.0), "ceil": hall_top})
	# under-mezzanine airspace is capped below the slab (center only — the
	# stair strips stay open so the flights can climb past it)
	m.arena_zones.append({"rect": Rect2(-18.0, -348.0, 36.0, 14.5),
		"band": Vector2(HALL_FLOOR - 4.0, HALL_FLOOR + 8.5),
		"ceil": MEZZ_FLOOR - 1.4})
	# mezzanine deck (bands start above the under-slab airspace)
	m.arena_zones.append({"rect": Rect2(-30.0, -348.0, 60.0, 15.0),
		"band": Vector2(HALL_FLOOR + 8.5, 40.0), "floor": MEZZ_FLOOR})
	# stair ramps: lz -308 (bottom, hall floor) to -334 (top, mezzanine)
	m.arena_zones.append({"rect": Rect2(19.0, -336.0, 10.0, 29.0),
		"band": Vector2(0.0, 40.0),
		"ramp": [2, -307.0, HALL_FLOOR, -334.0, MEZZ_FLOOR]})
	m.arena_zones.append({"rect": Rect2(-29.0, -336.0, 10.0, 29.0),
		"band": Vector2(0.0, 40.0),
		"ramp": [2, -307.0, HALL_FLOOR, -334.0, MEZZ_FLOOR]})


func _castle_wall(pos: Vector3, size: Vector3, col: Color) -> void:
	var wall: MeshInstance3D = m._l2_box(pos, size, col)
	wall.material_override = m._castle_mat("wall", 0.07, col)
	m._wall_solid(pos, size, 0.65)


func _build_wisp_trail(o: Vector3) -> void:
	# The permanent guide: paired-color wisps hover over the path from the
	# pass all the way to the castle gate, denser near the spirit clearings.
	var wisps: Array = []
	var lz := 330.0
	var i := 0
	while lz > -292.0:
		var lx: float = _path_x(lz) + (3.0 if i % 2 == 0 else -3.0)
		var base: Vector3 = o + Vector3(lx, _north_local(lx, lz) + 4.2, lz)
		var orb: Node3D = _north_prop("wisp", base, 3.3, float(i) * 0.57)
		if orb != null:
			_light_wisp(orb)
			m._set_vis_range(orb, 145.0)
			wisps.append({"node": orb, "base": base})
		i += 1
		lz -= 32.0 if _clearing_d(lx, lz) > 40.0 else 22.0
	m.g["north_wisps"] = wisps
	m.g["north_wisp_count"] = wisps.size()


func _build_leaf_drift(o: Vector3) -> void:
	# Wind-carried leaves drifting through the forest air — the cheapest
	# possible "the forest is alive" effect (skipped on speedy quality).
	if m.quality == "speedy":
		return
	for cfg: Array in [[Color(0.94, 0.44, 0.72), 0.0], [Color(0.95, 0.72, 0.34), 40.0]]:
		var leaves: GPUParticles3D = GPUParticles3D.new()
		leaves.amount = 42
		leaves.lifetime = 8.0
		leaves.local_coords = false
		leaves.emitting = true
		var pm: ParticleProcessMaterial = ParticleProcessMaterial.new()
		pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
		pm.emission_box_extents = Vector3(56.0, 11.0, 205.0)
		pm.gravity = Vector3(0.5, -0.75, 0.25)
		pm.initial_velocity_min = 0.6
		pm.initial_velocity_max = 1.8
		pm.angular_velocity_min = -110.0
		pm.angular_velocity_max = 110.0
		pm.spread = 60.0
		leaves.process_material = pm
		var quad: QuadMesh = QuadMesh.new()
		quad.size = Vector2(0.55, 0.4)
		leaves.draw_pass_1 = quad
		var lmat: StandardMaterial3D = StandardMaterial3D.new()
		lmat.albedo_color = cfg[0]
		lmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		lmat.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
		lmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		leaves.material_override = lmat
		leaves.position = o + Vector3(0.0, 15.0, 104.0 + float(cfg[1]))
		leaves.visibility_range_end = 190.0
		m.add_child(leaves)
		m.game_nodes.append(leaves)


func _bump(lx: float, lz: float, cx: float, cz: float, radius: float, amp: float) -> float:
	var d2: float = (lx - cx) * (lx - cx) + (lz - cz) * (lz - cz)
	var r2: float = radius * radius
	if d2 >= r2:
		return 0.0
	var f: float = 1.0 - d2 / r2
	return amp * f * f


func _path_x(lz: float) -> float:
	# The single spine of the whole stage. It WINDS through the forest act
	# (so the 430u walk is a sequence of reveals, not a straight hallway)
	# and straightens into the town street and castle approach.
	var amp: float = 26.0 * smoothstep(-100.0, -8.0, lz) * (1.0 - smoothstep(292.0, 326.0, lz))
	return amp * sin((lz - 20.0) * 0.021)


func _stream_x(lz: float) -> float:
	# The stream is path-relative: an oscillating offset crosses the road at
	# lz 175 (stepping stones) and lz -28 (log bridge), then locks east to
	# become the town river, sliding further out to skirt the castle plateau.
	var osc: float = 36.0 * sin((lz - 175.0) * 0.0155)
	var s_town: float = 1.0 - smoothstep(-110.0, -40.0, lz)
	var off: float = lerpf(osc, 44.0, s_town)
	var s_castle: float = 1.0 - smoothstep(-300.0, -260.0, lz)
	off = lerpf(off, 60.0, s_castle)
	return _path_x(lz) + off


func _stream_w(lz: float) -> float:
	# narrow forest brook, widening into the town river
	return lerpf(5.0, 8.0, 1.0 - smoothstep(-120.0, -60.0, lz))


func _north_local(lx: float, lz: float) -> float:
	var h := 2.0
	# The opening pass begins high, then settles into gently rolling forest.
	h += _bump(lx, lz, 0.0, 350.0, 95.0, 34.0)
	h += _bump(lx, lz, -70.0, 220.0, 55.0, 7.0)
	h += _bump(lx, lz, 75.0, 160.0, 60.0, 8.0)
	h += _bump(lx, lz, -80.0, 60.0, 58.0, 7.0)
	h += _bump(lx, lz, 70.0, -20.0, 52.0, 6.0)
	# The town squeezes between a steep mountainside (west) and the river:
	# the Riverwood trick — terrain itself walls the single street.
	h += _bump(lx, lz, -118.0, -180.0, 85.0, 26.0)
	h += _bump(lx, lz, 120.0, -195.0, 70.0, 14.0)
	# Fjords cut into both sides while the central strip stays broad and safe.
	var side: float = smoothstep(112.0, 176.0, absf(lx))
	h -= side * 13.0
	# Flatten the road corridor (skipped on the pass descent so the entry
	# stays a real downhill ride; eased in below it).
	var flat_w: float = 0.86 * (1.0 - smoothstep(240.0, 300.0, lz))
	var path_mask: float = 1.0 - smoothstep(9.0, 20.0, absf(lx - _path_x(lz)))
	h = lerpf(h, 2.0, path_mask * flat_w)
	# Spirit clearings are stamped flat — future boss arenas need open floor.
	for cc: Vector2 in [CLEARING_A, CLEARING_B]:
		var cd: float = Vector2(lx - cc.x, lz - cc.y).length()
		h = lerpf(h, 2.0, 1.0 - smoothstep(17.0, 27.0, cd))
	# The castle plateau lifts the finale above the town rooftops.
	var castle_d: float = Vector2(lx * 0.82, lz - CASTLE_LOCAL.y).length()
	h = lerpf(h, HALL_FLOOR, 1.0 - smoothstep(56.0, 88.0, castle_d))
	# The stream carves its bed through everything it winds across.
	var sd: float = absf(lx - _stream_x(lz))
	var sw: float = _stream_w(lz)
	var depth: float = lerpf(2.4, 3.2, 1.0 - smoothstep(-120.0, -60.0, lz))
	h -= depth * (1.0 - smoothstep(sw * 0.5, sw + 4.0, sd))
	# The waterfall pond: a wider bowl where the cascade lands.
	var pond_d: float = Vector2(lx - 13.0, lz - 266.0).length()
	h -= 2.0 * (1.0 - smoothstep(4.0, 10.0, pond_d))
	# The mill island rises back out of the river's east half; the channel
	# keeps flowing on its west side.
	h += _bump(lx, lz, 52.0, -218.0, 9.0, 5.0)
	# The long strip falls into painted cliffs just past the playable rim.
	var ex: float = maxf(0.0, absf(lx) - 134.0)
	var ez: float = maxf(0.0, absf(lz) - 362.0)
	h -= (ex + ez) * 0.75
	return h
