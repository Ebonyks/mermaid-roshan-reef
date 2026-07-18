extends SceneTree
# Runtime contract audit for the imagegen-guided Royal Bathroom assets.
# Visual composition is covered by assets_src/blender/qa_bathroom_props; this
# probe keeps the imported Godot scenes lightweight and material-rig compatible.

const ASSETS: Array[Dictionary] = [
	{
		"path": "res://assets/castle/bathroom_bathtub.glb",
		"roles": ["TubPorcelain", "TubInterior", "TubAccent", "TubMetal", "TubWater", "TubFoam"],
		"max_triangles": 10000,
	},
	{
		"path": "res://assets/castle/bathroom_sink.glb",
		"roles": ["VanityBody", "VanityTop", "VanityBasin", "VanityMetal", "VanityMirror"],
		"max_triangles": 10000,
	},
	{
		"path": "res://assets/castle/bathroom_toilet.glb",
		"roles": ["ToiletPorcelain", "ToiletSeat", "ToiletWater", "ToiletMetal"],
		"max_triangles": 10000,
	},
]

# These three hero fixtures share one small room. A 30k static-room envelope is
# still light on the target Mali-G52 while leaving enough geometry for genuinely
# hollow bowls, curved plumbing, layered molding, and readable shell relief.
const MAX_TOTAL_TRIANGLES := 30000
const FLOOR_TOLERANCE := 0.05

func _triangle_count(mesh: Mesh) -> int:
	var triangles: int = 0
	for surface_index in range(mesh.get_surface_count()):
		var arrays: Array = mesh.surface_get_arrays(surface_index)
		var indices: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		if indices.is_empty():
			var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
			triangles += vertices.size() / 3
		else:
			triangles += indices.size() / 3
	return triangles

func _degenerate_count(mesh: Mesh) -> int:
	var degenerate: int = 0
	for surface_index in range(mesh.get_surface_count()):
		if mesh.surface_get_primitive_type(surface_index) != Mesh.PRIMITIVE_TRIANGLES:
			continue
		var arrays: Array = mesh.surface_get_arrays(surface_index)
		var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		var indices: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		var element_count: int = indices.size() if not indices.is_empty() else vertices.size()
		for element_index in range(0, element_count - 2, 3):
			var a_index: int = indices[element_index] if not indices.is_empty() else element_index
			var b_index: int = indices[element_index + 1] if not indices.is_empty() else element_index + 1
			var c_index: int = indices[element_index + 2] if not indices.is_empty() else element_index + 2
			var edge_ab: Vector3 = vertices[b_index] - vertices[a_index]
			var edge_ac: Vector3 = vertices[c_index] - vertices[a_index]
			if edge_ab.cross(edge_ac).length_squared() <= 0.000000000001:
				degenerate += 1
	return degenerate

func _inspect(node: Node, roles: Array, result: Dictionary) -> void:
	if node is Skeleton3D or node is AnimationPlayer or node is Light3D or node is CollisionObject3D:
		result["forbidden"].append(String(node.get_class()) + ":" + String(node.name))
	if node is MeshInstance3D:
		var mesh_node: MeshInstance3D = node as MeshInstance3D
		if mesh_node.mesh != null:
			result["triangles"] = int(result["triangles"]) + _triangle_count(mesh_node.mesh)
			result["degenerate"] = int(result["degenerate"]) + _degenerate_count(mesh_node.mesh)
			var mesh_bounds: AABB = mesh_node.global_transform * mesh_node.get_aabb()
			if not bool(result["has_bounds"]):
				result["bounds"] = mesh_bounds
				result["has_bounds"] = true
			else:
				result["bounds"] = (result["bounds"] as AABB).merge(mesh_bounds)
		var node_name: String = String(mesh_node.name)
		for role_value in roles:
			var role: String = String(role_value)
			if node_name.begins_with(role):
				result["found"][role] = true
	for child in node.get_children():
		_inspect(child, roles, result)

func _run() -> void:
	var failed := false
	var total_triangles: int = 0
	for asset in ASSETS:
		var path: String = String(asset["path"])
		var roles: Array = asset["roles"]
		if not ResourceLoader.exists(path):
			print("BATHROOM|FAIL|missing=", path)
			failed = true
			continue
		var packed: PackedScene = load(path) as PackedScene
		if packed == null:
			print("BATHROOM|FAIL|load=", path)
			failed = true
			continue
		var instance: Node = packed.instantiate()
		root.add_child(instance)
		var result: Dictionary = {
			"triangles": 0,
			"degenerate": 0,
			"found": {},
			"forbidden": [],
			"has_bounds": false,
			"bounds": AABB(),
		}
		_inspect(instance, roles, result)
		for role_value in roles:
			var role: String = String(role_value)
			if not bool(result["found"].get(role, false)):
				print("BATHROOM|FAIL|role=", role, " path=", path)
				failed = true
		var triangles: int = int(result["triangles"])
		var max_triangles: int = int(asset["max_triangles"])
		if triangles > max_triangles:
			print("BATHROOM|FAIL|triangles=", triangles, " max=", max_triangles, " path=", path)
			failed = true
		if int(result["degenerate"]) > 0:
			print("BATHROOM|FAIL|degenerate=", result["degenerate"], " path=", path)
			failed = true
		if not result["forbidden"].is_empty():
			print("BATHROOM|FAIL|forbidden=", result["forbidden"], " path=", path)
			failed = true
		if not bool(result["has_bounds"]):
			print("BATHROOM|FAIL|bounds=empty path=", path)
			failed = true
		else:
			var bounds: AABB = result["bounds"] as AABB
			if bounds.size.x <= 0.0 or bounds.size.y <= 0.0 or bounds.size.z <= 0.0:
				print("BATHROOM|FAIL|bounds=degenerate value=", bounds, " path=", path)
				failed = true
			if absf(bounds.position.y) > FLOOR_TOLERANCE:
				print("BATHROOM|FAIL|floor_y=", bounds.position.y, " tolerance=", FLOOR_TOLERANCE, " path=", path)
				failed = true
		total_triangles += triangles
		print("BATHROOM|asset=", path.get_file(), " triangles=", triangles, " roles=", roles.size(), " bounds=", result["bounds"])
		instance.free()
	if total_triangles > MAX_TOTAL_TRIANGLES:
		print("BATHROOM|FAIL|total_triangles=", total_triangles, " max=", MAX_TOTAL_TRIANGLES)
		failed = true
	print("BATHROOM|RESULT=", "FAIL" if failed else "OK", " total_triangles=", total_triangles)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
