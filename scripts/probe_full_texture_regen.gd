extends SceneTree

# Import and Mobile-budget contract for the isolated full-regeneration pack.
# Visual grading lives in audit/full_regen_2026-07-18; this probe ensures every
# accepted candidate remains loadable as a real Godot resource.

const MODEL_DIR := "res://assets/full_texture_regen_2026-07-18/models"
const TEXTURE_DIR := "res://assets/full_texture_regen_2026-07-18/textures"
const EXPECTED_MODELS := 137
const EXPECTED_TEXTURES := 30
const MAX_MODEL_TRIANGLES := 12000
const MAX_TEXTURE_SIDE := 1024


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


func _inspect_model(node: Node, result: Dictionary) -> void:
	if node is Light3D or node is CollisionObject3D or node is Skeleton3D:
		result["forbidden"].append(String(node.get_class()) + ":" + String(node.name))
	if node is MeshInstance3D:
		var mesh_node: MeshInstance3D = node as MeshInstance3D
		if mesh_node.mesh != null:
			result["meshes"] = int(result["meshes"]) + 1
			result["triangles"] = int(result["triangles"]) + _triangle_count(mesh_node.mesh)
			var bounds: AABB = mesh_node.mesh.get_aabb()
			result["max_extent"] = maxf(float(result["max_extent"]), bounds.size.length())
	for child in node.get_children():
		_inspect_model(child, result)


func _is_power_of_two(value: int) -> bool:
	return value > 0 and (value & (value - 1)) == 0


func _audit_model(file_name: String) -> bool:
	var path: String = MODEL_DIR.path_join(file_name)
	if not ResourceLoader.exists(path):
		print("FULL_REGEN|ERROR|missing_model=", path)
		return false
	var packed: PackedScene = load(path) as PackedScene
	if packed == null:
		print("FULL_REGEN|ERROR|load_model=", path)
		return false
	var instance: Node = packed.instantiate()
	var result: Dictionary = {"meshes": 0, "triangles": 0, "max_extent": 0.0, "forbidden": []}
	_inspect_model(instance, result)
	instance.free()
	if int(result["meshes"]) <= 0 or int(result["triangles"]) <= 0:
		print("FULL_REGEN|ERROR|empty_model=", file_name, " result=", result)
		return false
	if int(result["triangles"]) > MAX_MODEL_TRIANGLES:
		print("FULL_REGEN|ERROR|triangle_budget=", file_name, " result=", result)
		return false
	if float(result["max_extent"]) <= 0.001:
		print("FULL_REGEN|ERROR|zero_bounds=", file_name)
		return false
	if not result["forbidden"].is_empty():
		print("FULL_REGEN|ERROR|forbidden_nodes=", file_name, " nodes=", result["forbidden"])
		return false
	return true


func _audit_texture(file_name: String) -> bool:
	var path: String = TEXTURE_DIR.path_join(file_name)
	if not ResourceLoader.exists(path):
		print("FULL_REGEN|ERROR|missing_texture=", path)
		return false
	var texture: Texture2D = load(path) as Texture2D
	if texture == null:
		print("FULL_REGEN|ERROR|load_texture=", path)
		return false
	var width: int = texture.get_width()
	var height: int = texture.get_height()
	if width <= 0 or height <= 0:
		print("FULL_REGEN|ERROR|empty_texture=", file_name)
		return false
	if maxi(width, height) > MAX_TEXTURE_SIDE and not (_is_power_of_two(width) and _is_power_of_two(height)):
		print("FULL_REGEN|ERROR|texture_budget=", file_name, " size=", Vector2i(width, height))
		return false
	return true


func _run() -> void:
	var failed: bool = false
	var model_files: PackedStringArray = []
	for file_name in DirAccess.get_files_at(MODEL_DIR):
		if file_name.get_extension().to_lower() == "glb":
			model_files.append(file_name)
	var texture_files: PackedStringArray = []
	for file_name in DirAccess.get_files_at(TEXTURE_DIR):
		if file_name.get_extension().to_lower() == "png":
			texture_files.append(file_name)
	model_files.sort()
	texture_files.sort()
	if model_files.size() != EXPECTED_MODELS:
		print("FULL_REGEN|ERROR|model_count=", model_files.size(), " expected=", EXPECTED_MODELS)
		failed = true
	if texture_files.size() != EXPECTED_TEXTURES:
		print("FULL_REGEN|ERROR|texture_count=", texture_files.size(), " expected=", EXPECTED_TEXTURES)
		failed = true
	var model_ok: int = 0
	for file_name in model_files:
		if _audit_model(file_name):
			model_ok += 1
		else:
			failed = true
	var texture_ok: int = 0
	for file_name in texture_files:
		if _audit_texture(file_name):
			texture_ok += 1
		else:
			failed = true
	print("FULL_REGEN|RESULT=", "ERROR" if failed else "OK", " models=", model_ok, " textures=", texture_ok)
	quit(1 if failed else 0)


func _init() -> void:
	call_deferred("_run")
