extends RefCounted

const INK := Color(0.16, 0.12, 0.28)
const PEARL := Color(1.0, 0.94, 0.86)
const AQUA := Color(0.38, 0.88, 0.82)
const CORAL := Color(1.0, 0.48, 0.55)
const LAVENDER := Color(0.68, 0.51, 0.92)
const GOLD := Color(1.0, 0.76, 0.24)

static func _mat(color: Color, emission: float = 0.0) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.92
	material.metallic = 0.0
	material.metallic_specular = 0.08
	if emission > 0.0:
		material.emission_enabled = true
		material.emission = color
		material.emission_energy_multiplier = emission
	return material

static func _star_points(radius: float, inner_ratio: float = 0.46) -> PackedVector2Array:
	var points := PackedVector2Array()
	for i in range(10):
		var radius_i := radius if i % 2 == 0 else radius * inner_ratio
		var angle := -PI * 0.5 + float(i) * PI / 5.0
		points.append(Vector2(cos(angle), sin(angle)) * radius_i)
	return points

static func _polygon_prism(points: PackedVector2Array, depth: float) -> ArrayMesh:
	var surface := SurfaceTool.new()
	surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	var triangles := Geometry2D.triangulate_polygon(points)
	var front_z := depth * 0.5
	for i in range(0, triangles.size(), 3):
		for j in [0, 1, 2]:
			var p := points[triangles[i + j]]
			surface.set_normal(Vector3.FORWARD)
			surface.add_vertex(Vector3(p.x, p.y, front_z))
	for i in range(0, triangles.size(), 3):
		for j in [2, 1, 0]:
			var p := points[triangles[i + j]]
			surface.set_normal(Vector3.BACK)
			surface.add_vertex(Vector3(p.x, p.y, -front_z))
	for i in range(points.size()):
		var a := points[i]
		var b := points[(i + 1) % points.size()]
		var normal := Vector3(b.y - a.y, a.x - b.x, 0.0).normalized()
		for v in [Vector3(a.x, a.y, -front_z), Vector3(b.x, b.y, -front_z), Vector3(b.x, b.y, front_z),
				Vector3(a.x, a.y, -front_z), Vector3(b.x, b.y, front_z), Vector3(a.x, a.y, front_z)]:
			surface.set_normal(normal)
			surface.add_vertex(v)
	return surface.commit()

static func _polygon_node(points: PackedVector2Array, depth: float, color: Color, emission: float = 0.0) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.mesh = _polygon_prism(points, depth)
	node.material_override = _mat(color, emission)
	return node

static func _scaled_points(points: PackedVector2Array, scale_value: float) -> PackedVector2Array:
	var result := PackedVector2Array()
	for point in points:
		result.append(point * scale_value)
	return result

static func create_star(size: float, accent: Color = GOLD, crown: bool = false, simple: bool = false) -> Node3D:
	var root := Node3D.new()
	var points := _star_points(size)
	var outline := _polygon_node(_scaled_points(points, 1.12), size * 0.22, INK)
	outline.position.z = -size * 0.08
	root.add_child(outline)
	var face := _polygon_node(points, size * 0.24, accent, 0.22)
	root.add_child(face)
	if not simple:
		var inset := _polygon_node(_scaled_points(points, 0.56), size * 0.12, PEARL, 0.12)
		inset.position.z = size * 0.16
		root.add_child(inset)
		for i in range(5):
			var pearl := MeshInstance3D.new()
			var pearl_mesh := SphereMesh.new()
			pearl_mesh.radius = size * 0.07
			pearl_mesh.height = size * 0.14
			pearl_mesh.radial_segments = 8
			pearl_mesh.rings = 4
			pearl.mesh = pearl_mesh
			pearl.material_override = _mat([AQUA, CORAL, LAVENDER, GOLD, AQUA][i], 0.16)
			var angle := -PI * 0.5 + float(i) * TAU / 5.0
			pearl.position = Vector3(cos(angle), sin(angle), 0.28) * size * 0.72
			root.add_child(pearl)
	if crown:
		var crown_points := PackedVector2Array([
			Vector2(-0.62, 0.0), Vector2(-0.52, 0.58), Vector2(-0.18, 0.27),
			Vector2(0.0, 0.72), Vector2(0.18, 0.27), Vector2(0.52, 0.58), Vector2(0.62, 0.0)
		])
		var crown_outline := _polygon_node(_scaled_points(crown_points, size * 0.48), size * 0.2, INK)
		crown_outline.position = Vector3(0.0, size * 0.92, 0.0)
		root.add_child(crown_outline)
		var crown_face := _polygon_node(_scaled_points(crown_points, size * 0.39), size * 0.22, GOLD, 0.2)
		crown_face.position = Vector3(0.0, size * 0.94, size * 0.08)
		root.add_child(crown_face)
	root.set_meta("landmark_art", "crown_star" if crown else "dream_star")
	return root

static func _wing(root: Node3D, points: PackedVector2Array, color: Color, detail: Color, z: float) -> Node3D:
	var holder := Node3D.new()
	var outline := _polygon_node(_scaled_points(points, 1.08), 0.13, INK)
	outline.position.z = z - 0.05
	holder.add_child(outline)
	var face := _polygon_node(points, 0.15, color, 0.08)
	face.position.z = z
	holder.add_child(face)
	var inset := _polygon_node(_scaled_points(points, 0.66), 0.09, detail, 0.1)
	inset.position.z = z + 0.1
	holder.add_child(inset)
	root.add_child(holder)
	return holder

static func _portal_material() -> ShaderMaterial:
	var shader := Shader.new()
	shader.code = """shader_type spatial;
render_mode blend_mix, unshaded, cull_disabled, depth_prepass_alpha;
void fragment() {
	vec2 p = UV - vec2(0.5);
	float edge = smoothstep(0.5, 0.39, length(p * vec2(1.0, 0.72)));
	float band = fract(atan(p.y, p.x) / 6.28318 + length(p) * 1.6 - TIME * 0.08);
	vec3 a = vec3(0.35, 0.88, 0.82);
	vec3 b = vec3(0.95, 0.48, 0.62);
	ALBEDO = mix(a, b, smoothstep(0.15, 0.85, band));
	ALPHA = edge * 0.72;
}"""
	var material := ShaderMaterial.new()
	material.shader = shader
	return material

static func create_butterfly_gate(scale_value: float) -> Node3D:
	var root := Node3D.new()
	var portal := MeshInstance3D.new()
	var portal_mesh := QuadMesh.new()
	portal_mesh.size = Vector2(1.55, 2.2)
	portal.mesh = portal_mesh
	portal.material_override = _portal_material()
	portal.position = Vector3(0.0, 0.12, -0.08)
	root.add_child(portal)
	var upper := PackedVector2Array([
		Vector2(0.0, -0.78), Vector2(0.12, -0.22), Vector2(0.42, 0.42),
		Vector2(0.88, 0.78), Vector2(1.42, 0.62), Vector2(1.64, 0.12),
		Vector2(1.46, -0.38), Vector2(0.82, -0.72)
	])
	var lower := PackedVector2Array([
		Vector2(0.0, 0.66), Vector2(0.42, 0.52), Vector2(1.16, 0.22),
		Vector2(1.42, -0.26), Vector2(1.12, -0.82), Vector2(0.56, -0.92),
		Vector2(0.14, -0.52)
	])
	for side in [-1.0, 1.0]:
		var mirrored_upper := PackedVector2Array()
		var mirrored_lower := PackedVector2Array()
		for point in upper:
			mirrored_upper.append(Vector2(point.x * side, point.y) + Vector2(side * 0.7, 0.62))
		for point in lower:
			mirrored_lower.append(Vector2(point.x * side, point.y) + Vector2(side * 0.72, -0.58))
		var upper_holder := _wing(root, mirrored_upper, LAVENDER if side < 0.0 else AQUA, AQUA if side < 0.0 else CORAL, 0.0)
		upper_holder.name = "UpperLeft" if side < 0.0 else "UpperRight"
		upper_holder.set_meta("gate_wing", true)
		var lower_holder := _wing(root, mirrored_lower, CORAL if side < 0.0 else GOLD, GOLD if side < 0.0 else LAVENDER, 0.02)
		lower_holder.name = "LowerLeft" if side < 0.0 else "LowerRight"
		lower_holder.set_meta("gate_wing", true)
	var head := MeshInstance3D.new()
	var head_mesh := SphereMesh.new()
	head_mesh.radius = 0.27
	head_mesh.height = 0.54
	head_mesh.radial_segments = 12
	head_mesh.rings = 6
	head.mesh = head_mesh
	head.material_override = _mat(AQUA)
	head.position = Vector3(0.0, 1.18, 0.18)
	root.add_child(head)
	var body := MeshInstance3D.new()
	var body_mesh := CapsuleMesh.new()
	body_mesh.radius = 0.22
	body_mesh.height = 1.18
	body_mesh.radial_segments = 12
	body_mesh.rings = 4
	body.mesh = body_mesh
	body.material_override = _mat(INK)
	body.position = Vector3(0.0, 0.42, 0.12)
	root.add_child(body)
	var animation := Animation.new()
	animation.length = 2.4
	animation.loop_mode = Animation.LOOP_LINEAR
	for wing_name: String in ["UpperLeft", "LowerLeft", "UpperRight", "LowerRight"]:
		var track: int = animation.add_track(Animation.TYPE_VALUE)
		animation.track_set_path(track, NodePath("%s:rotation:y" % wing_name))
		var direction: float = -1.0 if wing_name.ends_with("Left") else 1.0
		animation.track_insert_key(track, 0.0, direction * 0.035)
		animation.track_insert_key(track, 1.2, direction * 0.11)
		animation.track_insert_key(track, 2.4, direction * 0.035)
	var library := AnimationLibrary.new()
	library.add_animation("breathe", animation)
	var player := AnimationPlayer.new()
	player.add_animation_library("", library)
	root.add_child(player)
	player.autoplay = "breathe"
	root.scale = Vector3.ONE * scale_value
	root.set_meta("landmark_art", "butterfly_gate")
	return root

static func create_cloud(size: float, variant: int = 0, sleepy: bool = false) -> Node3D:
	var root := Node3D.new()
	var profiles := [
		[Vector3(-0.88, 0.0, 0.0), Vector3(-0.34, 0.34, 0.04), Vector3(0.18, 0.46, 0.0), Vector3(0.72, 0.18, 0.03), Vector3(0.96, -0.08, 0.0)],
		[Vector3(-0.94, -0.04, 0.0), Vector3(-0.52, 0.28, 0.02), Vector3(-0.02, 0.52, 0.0), Vector3(0.5, 0.3, 0.03), Vector3(0.94, 0.0, 0.0)],
		[Vector3(-0.9, 0.08, 0.0), Vector3(-0.4, 0.42, 0.03), Vector3(0.06, 0.26, 0.0), Vector3(0.46, 0.52, 0.02), Vector3(0.92, 0.06, 0.0)]
	]
	var profile: Array = profiles[posmod(variant, profiles.size())]
	for i in range(profile.size()):
		var lobe := MeshInstance3D.new()
		var sphere := SphereMesh.new()
		var radius: float = size * float([0.42, 0.5, 0.58, 0.48, 0.38][i])
		sphere.radius = radius
		sphere.height = radius * 2.0
		sphere.radial_segments = 12
		sphere.rings = 6
		lobe.mesh = sphere
		lobe.material_override = _mat(Color(0.98, 0.96, 1.0) if not sleepy else Color(0.76, 0.69, 0.92))
		lobe.position = (profile[i] as Vector3) * size
		lobe.scale = Vector3(1.0, 0.78, 0.72)
		root.add_child(lobe)
	var underside := MeshInstance3D.new()
	var underside_mesh := SphereMesh.new()
	underside_mesh.radius = size * 0.92
	underside_mesh.height = size * 1.84
	underside_mesh.radial_segments = 12
	underside_mesh.rings = 4
	underside.mesh = underside_mesh
	underside.material_override = _mat(Color(0.62, 0.72, 0.9) if not sleepy else Color(0.43, 0.35, 0.68))
	underside.position = Vector3(0.0, -size * 0.3, -size * 0.05)
	underside.scale = Vector3(1.45, 0.25, 0.72)
	root.add_child(underside)
	root.set_meta("landmark_art", "sleepy_cloud" if sleepy else "storybook_cloud")
	return root
