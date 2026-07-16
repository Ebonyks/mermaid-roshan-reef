extends SceneTree
# Runtime contract audit for the imagegen-guided Royal Kitchen assets.
# Visual composition is covered by assets_src/blender/qa_kitchen_props; this
# probe keeps the imported Godot scenes lightweight and material-rig compatible.

const ASSETS: Array[Dictionary] = [
	{
		"path": "res://assets/castle/kitchen_counter.glb",
		"roles": ["CounterWood", "CounterTop", "CounterMetal"],
		"max_triangles": 1300,
	},
	{
		"path": "res://assets/castle/kitchen_sink.glb",
		"roles": ["SinkPorcelain", "SinkBasin", "SinkMetal", "SinkWater"],
		"max_triangles": 1900,
	},
	{
		"path": "res://assets/castle/kitchen_stove.glb",
		"roles": ["StoveBody", "StoveCream", "StoveTrim", "StoveMetal", "StoveGlass", "StoveBurnerHot", "StoveBurnerWarm", "StoveBurnerDark"],
		"max_triangles": 2000,
	},
]

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

func _inspect(node: Node, roles: Array, result: Dictionary) -> void:
	if node is Skeleton3D or node is AnimationPlayer or node is Light3D or node is CollisionObject3D:
		result["forbidden"].append(String(node.get_class()) + ":" + String(node.name))
	if node is MeshInstance3D:
		var mesh_node: MeshInstance3D = node as MeshInstance3D
		if mesh_node.mesh != null:
			result["triangles"] = int(result["triangles"]) + _triangle_count(mesh_node.mesh)
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
			print("KITCHEN|FAIL|missing=", path)
			failed = true
			continue
		var packed: PackedScene = load(path) as PackedScene
		if packed == null:
			print("KITCHEN|FAIL|load=", path)
			failed = true
			continue
		var instance: Node = packed.instantiate()
		var result: Dictionary = {"triangles": 0, "found": {}, "forbidden": []}
		_inspect(instance, roles, result)
		for role_value in roles:
			var role: String = String(role_value)
			if not bool(result["found"].get(role, false)):
				print("KITCHEN|FAIL|role=", role, " path=", path)
				failed = true
		var triangles: int = int(result["triangles"])
		var max_triangles: int = int(asset["max_triangles"])
		if triangles > max_triangles:
			print("KITCHEN|FAIL|triangles=", triangles, " max=", max_triangles, " path=", path)
			failed = true
		if not result["forbidden"].is_empty():
			print("KITCHEN|FAIL|forbidden=", result["forbidden"], " path=", path)
			failed = true
		total_triangles += triangles
		print("KITCHEN|asset=", path.get_file(), " triangles=", triangles, " roles=", roles.size())
		instance.free()
	if total_triangles > 5200:
		print("KITCHEN|FAIL|total_triangles=", total_triangles)
		failed = true
	print("KITCHEN|RESULT=", "FAIL" if failed else "OK", " total_triangles=", total_triangles)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
