extends SceneTree
# Import/runtime contract for the generated Fairy Pond art family. Visual
# composition is captured by probe_human_art_audit; this gate protects file
# presence, texture limits, transparent padding, mesh depth, and Mobile budget.

const BACKGROUNDS: Array[String] = [
	"res://assets/fairy/pond_dawn.png",
	"res://assets/fairy/pond_twilight.png",
	"res://assets/fairy/pond_boss_clearing.png",
]

const MODELS: Array[Dictionary] = [
	{"path": "res://assets/fairy/models/bug_jewel.glb", "max_triangles": 4000},
	{"path": "res://assets/fairy/models/bug_moth.glb", "max_triangles": 4000},
	{"path": "res://assets/fairy/models/bug_firefly.glb", "max_triangles": 4000},
	{"path": "res://assets/fairy/models/boss_leaf.glb", "max_triangles": 4000},
	{"path": "res://assets/fairy/models/boss_seed.glb", "max_triangles": 7000},
	{"path": "res://assets/fairy/models/boss_sprout.glb", "max_triangles": 7000},
	{"path": "res://assets/fairy/models/boss_bud.glb", "max_triangles": 10000},
	{"path": "res://assets/fairy/models/boss_opening.glb", "max_triangles": 14000},
	{"path": "res://assets/fairy/models/boss_bloom.glb", "max_triangles": 15000},
]

func _triangle_count(mesh: Mesh) -> int:
	var triangles := 0
	for surface_index in range(mesh.get_surface_count()):
		var arrays: Array = mesh.surface_get_arrays(surface_index)
		var indices: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		if indices.is_empty():
			var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
			triangles += vertices.size() / 3
		else:
			triangles += indices.size() / 3
	return triangles

func _inspect(node: Node, result: Dictionary) -> void:
	if node is Light3D or node is CollisionObject3D or node is Skeleton3D:
		result["forbidden"].append(String(node.get_class()) + ":" + String(node.name))
	if node is MeshInstance3D:
		var mesh_node: MeshInstance3D = node as MeshInstance3D
		if mesh_node.mesh != null:
			result["triangles"] = int(result["triangles"]) + _triangle_count(mesh_node.mesh)
			result["meshes"] = int(result["meshes"]) + 1
			var bounds: AABB = mesh_node.mesh.get_aabb()
			result["relief_depth"] = maxf(float(result["relief_depth"]), bounds.size.y)
	for child in node.get_children():
		_inspect(child, result)

func _audit_texture(path: String, require_alpha: bool) -> bool:
	if not FileAccess.file_exists(path):
		print("FAIRY_ART|FAIL|missing_texture=", path)
		return false
	var image := Image.new()
	var error: int = image.load(ProjectSettings.globalize_path(path))
	if error != OK or image.is_empty():
		print("FAIRY_ART|FAIL|load_texture=", path, " error=", error)
		return false
	if image.get_width() != 1024 or image.get_height() != 1024:
		print("FAIRY_ART|FAIL|texture_size=", image.get_size(), " path=", path)
		return false
	if require_alpha:
		var corners := [
			image.get_pixel(0, 0).a,
			image.get_pixel(image.get_width() - 1, 0).a,
			image.get_pixel(0, image.get_height() - 1).a,
			image.get_pixel(image.get_width() - 1, image.get_height() - 1).a,
		]
		for alpha_value in corners:
			if float(alpha_value) > 0.01:
				print("FAIRY_ART|FAIL|opaque_corner=", corners, " path=", path)
				return false
	print("FAIRY_ART|texture=", path.get_file(), " size=1024x1024 alpha=", require_alpha)
	return true

func _run() -> void:
	var failed := false
	var total_triangles := 0
	for path in BACKGROUNDS:
		if not _audit_texture(path, false):
			failed = true
	for asset in MODELS:
		var path: String = String(asset["path"])
		if not ResourceLoader.exists(path):
			print("FAIRY_ART|FAIL|missing_model=", path)
			failed = true
			continue
		var packed: PackedScene = load(path) as PackedScene
		if packed == null:
			print("FAIRY_ART|FAIL|load_model=", path)
			failed = true
			continue
		var instance: Node = packed.instantiate()
		var result: Dictionary = {"triangles": 0, "meshes": 0, "relief_depth": 0.0, "forbidden": []}
		_inspect(instance, result)
		var triangles: int = int(result["triangles"])
		var max_triangles: int = int(asset["max_triangles"])
		if triangles <= 0 or triangles > max_triangles:
			print("FAIRY_ART|FAIL|triangles=", triangles, " max=", max_triangles, " path=", path)
			failed = true
		if int(result["meshes"]) <= 0 or float(result["relief_depth"]) < 0.02:
			print("FAIRY_ART|FAIL|not_relief=", result, " path=", path)
			failed = true
		if not result["forbidden"].is_empty():
			print("FAIRY_ART|FAIL|forbidden=", result["forbidden"], " path=", path)
			failed = true
		total_triangles += triangles
		print("FAIRY_ART|model=", path.get_file(), " triangles=", triangles, " depth=", result["relief_depth"])
		instance.free()
	if total_triangles > 70000:
		print("FAIRY_ART|FAIL|family_triangles=", total_triangles)
		failed = true
	print("FAIRY_ART|RESULT=", "FAIL" if failed else "OK", " family_triangles=", total_triangles)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
