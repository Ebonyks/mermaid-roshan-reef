class_name MelodyGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# melody minigame. All state stays on main (m.*); received by reference.

var m: ReefMain
var stage_root: Node3D

const NAVY := Color(0.075, 0.065, 0.16)
const INK := Color(0.12, 0.10, 0.24)
const AQUA := Color(0.25, 0.78, 0.82)
const AQUA_DARK := Color(0.12, 0.42, 0.52)
const LAVENDER := Color(0.58, 0.42, 0.78)
const PINK := Color(0.94, 0.42, 0.67)
const GOLD := Color(1.0, 0.78, 0.30)
const RAINBOW := [
	Color(1.0, 0.24, 0.28),
	Color(1.0, 0.54, 0.18),
	Color(1.0, 0.86, 0.24),
	Color(0.30, 0.84, 0.42),
	Color(0.24, 0.68, 0.96),
	Color(0.39, 0.38, 0.88),
	Color(0.72, 0.40, 0.90),
]


func _init(main: ReefMain) -> void:
	m = main


func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["caught"] = 0
	m.g["orbs"] = []

	# Daddy Mermaid's rainbow theater — an original 3D playset: crown
	# proscenium, rainbow tree, stage wings, sound towers, runway and seating.
	stage_root = Node3D.new()
	stage_root.name = "RainbowTheater3D"
	stage_root.position = origin
	m.add_child(stage_root)
	m.game_nodes.append(stage_root)

	_build_room()
	_build_stage_deck()
	_build_rainbow_scenery()
	_build_crown_proscenium()
	_build_sound_towers()
	_build_lighting_rig()
	_build_runway()
	_build_audience()
	_build_streamers()
	_add_star_performer()

	# The set has physical depth without putting invisible barriers across the
	# catch area. Only the back wall and the outboard sound towers are solid.
	m._wall_solid(origin + Vector3(0.0, 18.0, -28.0), Vector3(54.0, 38.0, 1.6), 0.5)
	m._wall_solid(origin + Vector3(-23.0, 7.5, -15.0), Vector3(5.8, 13.0, 4.0), 0.35)
	m._wall_solid(origin + Vector3(23.0, 7.5, -15.0), Vector3(5.8, 13.0, 4.0), 0.35)

	_build_rainbow_orbs(origin)
	m.show_msg(fr["fname"], "Catch all 7 colors of the rainbow! Swim into the bouncing orbs!")


func _build_room() -> void:
	_box("BackWall", Vector3(0.0, 18.0, -28.0), Vector3(54.0, 38.0, 1.6), NAVY)
	_box("ScenicWall", Vector3(0.0, 16.5, -26.9), Vector3(43.0, 31.0, 0.8), Color(0.18, 0.58, 0.67))
	_box("CeilingHeader", Vector3(0.0, 37.0, -25.0), Vector3(56.0, 3.0, 7.0), INK)
	_box("LeftWing", Vector3(-25.0, 18.0, -22.5), Vector3(5.0, 36.0, 10.0), Color(0.10, 0.30, 0.40))
	_box("RightWing", Vector3(25.0, 18.0, -22.5), Vector3(5.0, 36.0, 10.0), Color(0.10, 0.30, 0.40))

	# Deep vertical ribs turn the blue illustrated wall into a toy-theater shell.
	var rib_positions: Array[Vector3] = []
	var rib_colors: Array[Color] = []
	for i in range(13):
		var x: float = -24.0 + float(i) * 4.0
		rib_positions.append(Vector3(x, 18.0, -26.0))
		rib_colors.append(Color(0.16, 0.42, 0.50) if i % 2 == 0 else Color(0.12, 0.34, 0.44))
	_add_box_multimesh("WallRibs", rib_positions, rib_colors, Vector3(0.45, 35.0, 0.65))

	# Pleated side curtains clearly frame an opening instead of reading as trees.
	var curtain_positions: Array[Vector3] = []
	var curtain_colors: Array[Color] = []
	for side in [-1.0, 1.0]:
		for i in range(4):
			var x: float = side * (20.7 + float(i) * 1.25)
			curtain_positions.append(Vector3(x, 17.0, -23.8 + float(i) * 0.18))
			curtain_colors.append([PINK, LAVENDER, Color(0.30, 0.66, 0.90), AQUA][i])
	_add_capsule_multimesh("StageCurtains", curtain_positions, curtain_colors, 0.72, 29.0)


func _build_stage_deck() -> void:
	_box("StageDeck", Vector3(0.0, 0.75, -10.5), Vector3(48.0, 1.5, 31.0), INK)
	_box("StageSurface", Vector3(0.0, 1.62, -10.5), Vector3(46.0, 0.28, 29.0), Color(0.31, 0.70, 0.72), Vector3.ZERO, 0.16)
	_box("StageApron", Vector3(0.0, 1.25, 5.0), Vector3(47.0, 2.1, 1.8), LAVENDER)
	_box("ApronGlow", Vector3(0.0, 2.0, 6.0), Vector3(45.0, 0.30, 0.30), PINK, Vector3.ZERO, 0.65)

	# Broad central steps make the raised deck legible from the first camera view.
	_box("StageStepLow", Vector3(0.0, 0.25, 9.5), Vector3(15.0, 0.5, 3.0), INK)
	_box("StageStepMid", Vector3(0.0, 0.55, 7.8), Vector3(13.0, 0.65, 2.5), AQUA_DARK)
	_box("StageStepHigh", Vector3(0.0, 0.95, 6.2), Vector3(11.0, 0.85, 2.2), LAVENDER)


func _build_rainbow_scenery() -> void:
	# Seven nested 3D torus bands form the rainbow arch. Their lower halves sink
	# behind the deck, leaving a clean theater rainbow rather than loose objects.
	for i in range(RAINBOW.size()):
		var radius: float = 20.0 - float(i) * 1.18
		var torus := TorusMesh.new()
		torus.inner_radius = radius - 0.38
		torus.outer_radius = radius + 0.38
		torus.rings = 48
		torus.ring_segments = 8
		_mesh("RainbowArc%d" % i, torus, Vector3(0.0, 2.2, -25.9 + float(i) * 0.05), _mat(RAINBOW[i], 0.34), Vector3(90.0, 0.0, 0.0))

	# A single intentional rainbow-tree sculpture anchors the scenic design from
	# the book. It is made from curved colored trunks, never generated foliage.
	var trunk_cols: Array[Color] = [Color(0.96, 0.60, 0.55), GOLD, AQUA, LAVENDER]
	var tree_segments: Array[Dictionary] = []
	for ti in range(trunk_cols.size()):
		var x0: float = -1.35 + float(ti) * 0.9
		var p0 := Vector3(x0, 1.8, -25.2)
		var p1 := Vector3(x0 * 0.65, 9.0, -25.15)
		var p2 := Vector3(x0 * 1.15, 18.0, -25.1)
		var p3 := Vector3(x0 * 0.35, 28.5, -25.0)
		tree_segments.append({"a": p0, "b": p1, "r": 0.58, "col": trunk_cols[ti]})
		tree_segments.append({"a": p1, "b": p2, "r": 0.54, "col": trunk_cols[ti]})
		tree_segments.append({"a": p2, "b": p3, "r": 0.48, "col": trunk_cols[ti]})
	for side in [-1.0, 1.0]:
		tree_segments.append({"a": Vector3(side * 0.5, 19.0, -25.05), "b": Vector3(side * 8.0, 25.0, -25.0), "r": 0.48, "col": AQUA})
		tree_segments.append({"a": Vector3(side * 0.8, 22.0, -25.0), "b": Vector3(side * 12.0, 28.0, -24.95), "r": 0.42, "col": LAVENDER})
	_add_tube_multimesh("RainbowTreeSculpture", tree_segments)


func _build_crown_proscenium() -> void:
	# Explicit silhouette points draw a royal three-point crown over the stage
	# opening — Reef-of-Light royalty, matching the castle's gold language.
	var points: Array[Vector3] = [
		Vector3(-21.0, 2.0, -24.1),
		Vector3(-21.0, 26.0, -24.1),
		Vector3(-14.0, 34.0, -24.1),
		Vector3(-7.5, 28.5, -24.1),
		Vector3(0.0, 35.5, -24.1),
		Vector3(7.5, 28.5, -24.1),
		Vector3(14.0, 34.0, -24.1),
		Vector3(21.0, 26.0, -24.1),
		Vector3(21.0, 2.0, -24.1),
	]
	var ink_segments: Array[Dictionary] = []
	var face_segments: Array[Dictionary] = []
	for i in range(points.size() - 1):
		ink_segments.append({"a": points[i] + Vector3(0.0, 0.0, -0.18), "b": points[i + 1] + Vector3(0.0, 0.0, -0.18), "r": 1.22, "col": INK})
		face_segments.append({"a": points[i], "b": points[i + 1], "r": 0.86, "col": GOLD.darkened(0.15)})
	_add_tube_multimesh("CrownFrameInk", ink_segments)
	_add_tube_multimesh("CrownFrame", face_segments)
	# a pearl on each crown peak
	for peak in [Vector3(-14.0, 34.0, -24.1), Vector3(0.0, 35.5, -24.1), Vector3(14.0, 34.0, -24.1)]:
		_sphere("CrownPearl", peak + Vector3(0.0, 1.3, 0.0), 0.85, Color(0.98, 0.95, 1.0), 0.45)
	_add_proscenium_bulbs(points)


func _build_sound_towers() -> void:
	for side in [-1.0, 1.0]:
		var x: float = side * 23.0
		var label: String = "Left" if side < 0.0 else "Right"
		_box("Speaker%s" % label, Vector3(x, 7.5, -15.0), Vector3(5.8, 13.0, 4.0), NAVY, Vector3(0.0, -side * 5.0, 0.0))
		_box("SpeakerTrim%s" % label, Vector3(x, 7.5, -12.88), Vector3(5.0, 12.2, 0.25), LAVENDER, Vector3.ZERO, 0.08)
		for ci in range(2):
			var cy: float = 4.5 + float(ci) * 6.0
			var cone := CylinderMesh.new()
			cone.top_radius = 1.65
			cone.bottom_radius = 0.75
			cone.height = 0.72
			cone.radial_segments = 16
			_mesh("SpeakerCone", cone, Vector3(x, cy, -12.45), _mat(Color(0.22, 0.28, 0.38), 0.10), Vector3(90.0, 0.0, 0.0))
			_sphere("SpeakerCore", Vector3(x, cy, -12.0), 0.52, AQUA, 0.35)

		# A glowing pearl finial ties each sound tower to the crown arch.
		_sphere("SpeakerPearl", Vector3(x, 15.4, -13.0), 0.95, Color(0.98, 0.95, 1.0), 0.45)


func _build_lighting_rig() -> void:
	_box("LightingTruss", Vector3(0.0, 32.5, -15.5), Vector3(39.0, 0.65, 0.65), Color(0.18, 0.20, 0.28))
	for i in range(4):
		var x: float = -13.5 + float(i) * 9.0
		var col: Color = RAINBOW[i * 2]
		_capsule("StageLamp", Vector3(x, 30.7, -15.5), 0.62, 2.4, INK)
		_sphere("StageLampLens", Vector3(x, 29.45, -15.0), 0.62, col, 0.75)
		# Speedy avoids the only translucent stage geometry; the glowing physical
		# fixtures still communicate concert lighting on the target tablet.
		if m.quality != "speedy":
			_light_beam("StageLightBeam", Vector3(x, 29.0, -14.8), Vector3(x * 0.35, 2.2, -7.0), col)


func _build_runway() -> void:
	_box("Runway", Vector3(0.0, 0.48, 15.0), Vector3(11.0, 0.85, 20.0), INK)
	_box("RunwaySurface", Vector3(0.0, 0.98, 15.0), Vector3(10.2, 0.18, 19.2), Color(0.25, 0.66, 0.70), Vector3.ZERO, 0.12)
	var rail_segments: Array[Dictionary] = []
	for side in [-1.0, 1.0]:
		for i in range(RAINBOW.size()):
			var x: float = side * (5.75 + float(i) * 0.20)
			var y: float = 1.20 + float(i) * 0.08
			rail_segments.append({"a": Vector3(x, y, 5.5), "b": Vector3(x, y, 24.5), "r": 0.115, "col": RAINBOW[i]})
	_add_tube_multimesh("RainbowRunwayRails", rail_segments)
	_sphere("RunwayMedallion", Vector3(0.0, 1.35, 23.8), 1.35, GOLD, 0.34)


func _build_audience() -> void:
	_box("CenterAisle", Vector3(0.0, 0.12, 35.0), Vector3(7.0, 0.20, 20.0), LAVENDER)
	var seat_positions: Array[Vector3] = []
	var seat_colors: Array[Color] = []
	var xs: Array[float] = [-20.0, -16.0, -12.0, 12.0, 16.0, 20.0]
	for row in range(3):
		for xi in range(xs.size()):
			var x: float = xs[xi]
			seat_positions.append(Vector3(x, 0.0, 29.0 + float(row) * 5.5 + absf(x) * 0.035))
			seat_colors.append([Color(0.22, 0.46, 0.62), LAVENDER, Color(0.54, 0.30, 0.58)][row])
	_add_seat_multimesh("TheaterSeats", seat_positions, seat_colors, false)
	_add_seat_multimesh("TheaterSeatBacks", seat_positions, seat_colors, true)


func _build_streamers() -> void:
	# Fixed ribbons echo the reference composition without random placement.
	var specs: Array = [
		[-1.0, 27.5, PINK], [-1.0, 22.0, GOLD], [-1.0, 16.5, Color(0.30, 0.72, 0.92)],
		[1.0, 27.0, Color(0.45, 0.82, 0.42)], [1.0, 21.5, LAVENDER], [1.0, 16.0, Color(1.0, 0.52, 0.20)],
	]
	var streamer_segments: Array[Dictionary] = []
	for si in range(specs.size()):
		var spec: Array = specs[si]
		var side: float = float(spec[0])
		var y0: float = float(spec[1])
		var col: Color = spec[2]
		var points: Array[Vector3] = []
		for k in range(6):
			var f: float = float(k) / 5.0
			points.append(Vector3(side * (25.0 - f * 6.0), y0 - f * 9.5 + sin(f * TAU * 1.5 + float(si)) * 1.1, -18.0 + f * 3.0))
		for k in range(points.size() - 1):
			streamer_segments.append({"a": points[k], "b": points[k + 1], "r": 0.16, "col": col})
	_add_tube_multimesh("StageStreamers", streamer_segments)


func _add_star_performer() -> void:
	# Daddy Mermaid on the podium. Sprite cutout today; when the gen2 Meshy
	# model lands at friends/daddy.glb the loader below upgrades him to 3D.
	var podium := CylinderMesh.new()
	podium.top_radius = 4.8
	podium.bottom_radius = 5.3
	podium.height = 0.9
	podium.radial_segments = 24
	_mesh("StarPodium", podium, Vector3(0.0, 2.25, -20.5), _mat(PINK, 0.22))

	var performer := Sprite3D.new()
	performer.name = "StarPerformer"
	performer.texture = m._cutout_tex("daddy")
	performer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	performer.pixel_size = 0.018
	performer.position = Vector3(0.0, 10.0, -20.5)
	stage_root.add_child(performer)


func _build_rainbow_orbs(origin: Vector3) -> void:
	for i in range(RAINBOW.size()):
		var orb := MeshInstance3D.new()
		orb.name = "RainbowCatchOrb%d" % i
		var sph := SphereMesh.new()
		sph.radius = 1.12
		sph.height = 2.24
		sph.radial_segments = 12
		sph.rings = 6
		orb.mesh = sph
		orb.material_override = _mat(RAINBOW[i], 0.85)
		orb.position = origin + Vector3(-12.0 + float(i) * 4.0, 5.0 + fmod(float(i) * 2.7, 8.0), -6.0 + fmod(float(i) * 3.3, 12.0))

		# A tilted solid torus makes each target a tiny 3D stage light, not a
		# context-free glowing ball. As a child it follows pulse/hide automatically.
		var halo := MeshInstance3D.new()
		var torus := TorusMesh.new()
		torus.inner_radius = 1.38
		torus.outer_radius = 1.62
		torus.rings = 20
		torus.ring_segments = 6
		halo.mesh = torus
		halo.material_override = _mat(RAINBOW[i].lightened(0.30), 0.45)
		halo.rotation_degrees = Vector3(62.0, float(i) * 31.0, 18.0)
		orb.add_child(halo)

		m.add_child(orb)
		m.game_nodes.append(orb)
		var ov := Vector3(sin(float(i) * 2.1), sin(float(i) * 1.3) * 0.6, cos(float(i) * 1.7)).normalized() * (6.0 + float(i % 3) * 2.0)
		(m.g["orbs"] as Array).append({"node": orb, "vel": ov, "caught": false})


func _mat(col: Color, glow: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.72
	if glow > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = glow
	return mat


func _mesh(node_name: String, mesh: Mesh, pos: Vector3, mat: Material, rotdeg: Vector3 = Vector3.ZERO) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.name = node_name
	node.mesh = mesh
	node.material_override = mat
	node.position = pos
	node.rotation_degrees = rotdeg
	stage_root.add_child(node)
	return node


func _box(node_name: String, pos: Vector3, size: Vector3, col: Color, rotdeg: Vector3 = Vector3.ZERO, glow: float = 0.0) -> MeshInstance3D:
	var box := BoxMesh.new()
	box.size = size
	return _mesh(node_name, box, pos, _mat(col, glow), rotdeg)


func _sphere(node_name: String, pos: Vector3, radius: float, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var sphere := SphereMesh.new()
	sphere.radius = radius
	sphere.height = radius * 2.0
	sphere.radial_segments = 12
	sphere.rings = 6
	return _mesh(node_name, sphere, pos, _mat(col, glow))


func _capsule(node_name: String, pos: Vector3, radius: float, height: float, col: Color) -> MeshInstance3D:
	var capsule := CapsuleMesh.new()
	capsule.radius = radius
	capsule.height = height
	capsule.radial_segments = 10
	capsule.rings = 4
	return _mesh(node_name, capsule, pos, _mat(col, 0.06))


func _add_box_multimesh(node_name: String, positions: Array[Vector3], colors: Array[Color], size: Vector3) -> void:
	var box := BoxMesh.new()
	box.size = size
	_add_colored_multimesh(node_name, box, positions, colors)


func _add_capsule_multimesh(node_name: String, positions: Array[Vector3], colors: Array[Color], radius: float, height: float) -> void:
	var capsule := CapsuleMesh.new()
	capsule.radius = radius
	capsule.height = height
	capsule.radial_segments = 10
	capsule.rings = 4
	_add_colored_multimesh(node_name, capsule, positions, colors)


func _add_colored_multimesh(node_name: String, mesh: Mesh, positions: Array[Vector3], colors: Array[Color]) -> void:
	var mat := _mat(Color.WHITE)
	mat.vertex_color_use_as_albedo = true
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.use_colors = true
	multimesh.mesh = mesh
	multimesh.instance_count = positions.size()
	for i in range(positions.size()):
		multimesh.set_instance_transform(i, Transform3D(Basis(), positions[i]))
		multimesh.set_instance_color(i, colors[i])
	var instances := MultiMeshInstance3D.new()
	instances.name = node_name
	instances.multimesh = multimesh
	instances.material_override = mat
	stage_root.add_child(instances)


func _add_tube_multimesh(node_name: String, segments: Array[Dictionary]) -> void:
	var tube := CylinderMesh.new()
	tube.top_radius = 1.0
	tube.bottom_radius = 1.0
	tube.height = 1.0
	tube.radial_segments = 10
	var mat := _mat(Color.WHITE)
	mat.vertex_color_use_as_albedo = true
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.use_colors = true
	multimesh.mesh = tube
	multimesh.instance_count = segments.size()
	for i in range(segments.size()):
		var segment: Dictionary = segments[i]
		var a: Vector3 = segment["a"]
		var b: Vector3 = segment["b"]
		var radius: float = float(segment["r"])
		var direction: Vector3 = b - a
		var y_axis: Vector3 = direction.normalized()
		var helper: Vector3 = Vector3.RIGHT if absf(y_axis.dot(Vector3.RIGHT)) < 0.9 else Vector3.FORWARD
		var z_axis: Vector3 = helper.cross(y_axis).normalized()
		var x_axis: Vector3 = y_axis.cross(z_axis).normalized()
		var basis := Basis(x_axis * radius, y_axis * direction.length(), z_axis * radius)
		multimesh.set_instance_transform(i, Transform3D(basis, (a + b) * 0.5))
		var col: Color = segment["col"]
		multimesh.set_instance_color(i, col)
	var instances := MultiMeshInstance3D.new()
	instances.name = node_name
	instances.multimesh = multimesh
	instances.material_override = mat
	stage_root.add_child(instances)


func _light_beam(node_name: String, from: Vector3, to: Vector3, col: Color) -> MeshInstance3D:
	var direction: Vector3 = to - from
	var cone := CylinderMesh.new()
	cone.top_radius = 0.35
	cone.bottom_radius = 3.8
	cone.height = direction.length()
	cone.radial_segments = 12
	var mat := _mat(Color(col.r, col.g, col.b, 0.10), 0.35)
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	var node := _mesh(node_name, cone, (from + to) * 0.5, mat)
	node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	node.quaternion = Quaternion(Vector3.UP, direction.normalized())
	return node


func _add_proscenium_bulbs(points: Array[Vector3]) -> void:
	var positions: Array[Vector3] = []
	for i in range(points.size() - 1):
		var distance: float = points[i].distance_to(points[i + 1])
		var count: int = maxi(2, ceili(distance / 1.35))
		for j in range(count):
			positions.append(points[i].lerp(points[i + 1], float(j) / float(count)))
	positions.append(points[-1])

	var bulb := SphereMesh.new()
	bulb.radius = 0.27
	bulb.height = 0.54
	bulb.radial_segments = 8
	bulb.rings = 4
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.mesh = bulb
	multimesh.instance_count = positions.size()
	for i in range(positions.size()):
		multimesh.set_instance_transform(i, Transform3D(Basis(), positions[i] + Vector3(0.0, 0.0, 0.82)))
	var bulbs := MultiMeshInstance3D.new()
	bulbs.name = "ProsceniumBulbs"
	bulbs.multimesh = multimesh
	bulbs.material_override = _mat(Color(1.0, 0.91, 0.66), 0.90)
	bulbs.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	stage_root.add_child(bulbs)


func _add_seat_multimesh(node_name: String, positions: Array[Vector3], colors: Array[Color], backs: bool) -> void:
	var seat_mesh := BoxMesh.new()
	seat_mesh.size = Vector3(3.2, 3.0, 0.55) if backs else Vector3(3.2, 0.55, 2.4)
	var mat := _mat(Color.WHITE)
	mat.vertex_color_use_as_albedo = true
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.use_colors = true
	multimesh.mesh = seat_mesh
	multimesh.instance_count = positions.size()
	for i in range(positions.size()):
		var offset := Vector3(0.0, 2.55, 0.95) if backs else Vector3(0.0, 1.15, 0.0)
		multimesh.set_instance_transform(i, Transform3D(Basis(), positions[i] + offset))
		multimesh.set_instance_color(i, colors[i])
	var seats := MultiMeshInstance3D.new()
	seats.name = node_name
	seats.multimesh = multimesh
	seats.material_override = mat
	stage_root.add_child(seats)


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
		m.show_msg("Daddy Mermaid", "Swim to the colors! They are waiting for YOU!", "hint")
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
				m._end_game(true, fr, "You caught the WHOLE rainbow! Daddy Mermaid cheers for you!")
				return
