extends SceneTree

# Structural and visual acceptance probe for the pearl-castle art pass. The
# headless run audits import budgets and live placement; Xvfb additionally
# emits fixed Mobile-render review frames.

const KIT_DIR := "res://assets/castle/pearl_kit/"
const ASSET_NAMES: Array[String] = [
	"pearl_column",
	"pearl_balustrade",
	"pearl_shell_arch",
	"pearl_rainbow_window",
	"pearl_shell_sconce",
	"pearl_shell_chandelier",
	"pearl_floor_medallion",
	"pearl_throne_canopy",
	"pearl_shell_throne",
	"pearl_shell_planter",
	"pearl_shell_bench",
	"pearl_cloud_settee",
	"pearl_cloud_pouf",
	"pearl_shell_fountain",
	"pearl_rainbow_gate",
	"pearl_shell_banner_a",
	"pearl_shell_banner_b",
	"pearl_stair_rail",
]
const MIN_RUNTIME_COUNTS := {
	"pearl_column": 8,
	"pearl_balustrade": 12,
	"pearl_shell_arch": 12,
	"pearl_rainbow_window": 1,
	"pearl_shell_sconce": 8,
	"pearl_shell_chandelier": 8,
	"pearl_floor_medallion": 1,
	"pearl_throne_canopy": 1,
	"pearl_shell_throne": 1,
	"pearl_shell_planter": 4,
	"pearl_shell_bench": 2,
	"pearl_cloud_settee": 2,
	"pearl_cloud_pouf": 2,
	"pearl_shell_fountain": 2,
	"pearl_rainbow_gate": 1,
	"pearl_shell_banner_a": 4,
	"pearl_shell_banner_b": 2,
	"pearl_stair_rail": 2,
}
const MAX_ASSET_TRIANGLES := 10000
const MAX_ASSET_SURFACES := 12

var main: ReefMain
var camera: Camera3D
var out_dir := ""
var checks_failed := 0


func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CASTLE_ART|", label, "|", "OK" if ok else "FAIL", "|", detail)


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


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


func _inspect_asset(node: Node, result: Dictionary) -> void:
	if node is Light3D or node is Skeleton3D or node is AnimationPlayer or node is CollisionObject3D:
		var forbidden: Array = result["forbidden"] as Array
		forbidden.append(String(node.get_class()) + ":" + String(node.name))
	if node is MeshInstance3D:
		var mesh_node: MeshInstance3D = node as MeshInstance3D
		if mesh_node.mesh != null:
			result["mesh_count"] = int(result["mesh_count"]) + 1
			result["triangles"] = int(result["triangles"]) + _triangle_count(mesh_node.mesh)
			result["surfaces"] = int(result["surfaces"]) + mesh_node.mesh.get_surface_count()
	for child in node.get_children():
		_inspect_asset(child, result)


func _audit_assets() -> void:
	for asset_name in ASSET_NAMES:
		var path := KIT_DIR + asset_name + ".glb"
		var exists := ResourceLoader.exists(path)
		_ck("asset_exists_" + asset_name, exists, path)
		if not exists:
			continue
		var packed: PackedScene = load(path) as PackedScene
		_ck("asset_load_" + asset_name, packed != null, path)
		if packed == null:
			continue
		var instance: Node = packed.instantiate()
		root.add_child(instance)
		var result := {
			"mesh_count": 0,
			"triangles": 0,
			"surfaces": 0,
			"forbidden": [],
		}
		_inspect_asset(instance, result)
		_ck("single_mesh_" + asset_name, int(result["mesh_count"]) == 1, str(result))
		_ck("triangle_budget_" + asset_name, int(result["triangles"]) <= MAX_ASSET_TRIANGLES, str(result))
		_ck("surface_budget_" + asset_name, int(result["surfaces"]) <= MAX_ASSET_SURFACES, str(result))
		_ck("static_only_" + asset_name, (result["forbidden"] as Array).is_empty(), str(result))
		instance.free()


func _collect_runtime_assets(node: Node, counts: Dictionary) -> void:
	if node.has_meta("pearl_castle_asset"):
		var asset_name: String = String(node.get_meta("pearl_castle_asset"))
		counts[asset_name] = int(counts.get(asset_name, 0)) + 1
	for child in node.get_children():
		_collect_runtime_assets(child, counts)


func _collect_visible_layers(node: Node, layers: Array[CanvasLayer]) -> void:
	if node is CanvasLayer:
		var layer: CanvasLayer = node as CanvasLayer
		if layer.visible:
			layers.append(layer)
			layer.visible = false
	for child in node.get_children():
		_collect_visible_layers(child, layers)


func _shot(name_value: String, position: Vector3, target: Vector3, fov_value: float = 66.0) -> void:
	camera.fov = fov_value
	camera.position = position
	camera.look_at(target, Vector3.UP)
	await _frames(4)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name_value + ".png"))
	_ck("shot_" + name_value, error == OK, out_dir.path_join(name_value + ".png"))


func _capture_castle() -> void:
	if DisplayServer.get_name() == "headless":
		return
	var requested: String = OS.get_environment("CASTLE_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path("res://tmp/castle_pearl_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var hidden_layers: Array[CanvasLayer] = []
	_collect_visible_layers(root, hidden_layers)
	main.set_process(false)
	if main.player != null:
		main.player.set_process(false)
		main.player.visible = false
	camera = Camera3D.new()
	camera.fov = 66.0
	camera.far = 420.0
	root.add_child(camera)
	camera.current = true
	var o: Vector3 = main.CASTLE_POS
	await _shot("castle_01_hall_overview", o + Vector3(0, 14, 40), o + Vector3(0, 15, -24))
	await _shot("castle_02_throne_focal", o + Vector3(19, 20, -2), o + Vector3(0, 23, -29))
	await _shot("castle_03_entrance_motifs", o + Vector3(0, 12, 18), o + Vector3(0, 5, 40), 68.0)
	await _shot("castle_04_wall_fixture", o + Vector3(4, 17, 6), o + Vector3(33, 18, 4))
	await _shot("castle_05_upper_gallery", o + Vector3(39, 40, 15), o + Vector3(52, 41, -7), 70.0)
	await _shot("castle_06_cloud_lounge", o + Vector3(7, 40, -40), o + Vector3(26, 38, -53), 64.0)
	await _shot("castle_07_star_chamber", o + Vector3(-6, 40, -40), o + Vector3(-27, 40, -53), 64.0)
	await _shot("castle_08_royal_bedroom", o + Vector3(36, 10, -8), o + Vector3(48, 7, -19), 70.0)
	await _shot("castle_09_music_room", o + Vector3(-35, 10, -15), o + Vector3(-46, 8, -2), 70.0)
	await _shot("castle_10_royal_loo", o + Vector3(-27.2, -10.5, -23.5), o + Vector3(-32, -15, -28), 76.0)
	await _shot("castle_11_back_chamber", o + Vector3(20, 12, -37), o + Vector3(0, 8, -46), 68.0)


func _run() -> void:
	_audit_assets()
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	await _frames(8)
	main._enter_level2()
	await _frames(18)
	main._enter_castle_interior()
	await _frames(30)
	var counts := {}
	_collect_runtime_assets(main, counts)
	for asset_name in MIN_RUNTIME_COUNTS:
		var minimum: int = int(MIN_RUNTIME_COUNTS[asset_name])
		var actual: int = int(counts.get(asset_name, 0))
		_ck("runtime_" + String(asset_name), actual >= minimum, "actual=%d minimum=%d" % [actual, minimum])
	_ck("hall_exit_marker", main.g.has("hall_exit"), str(main.g.get("hall_exit", Vector3.ZERO)))
	_ck("toilet_contract_preserved", main.g.has("toilet"), "royal loo interaction remains active")
	await _capture_castle()
	print("CASTLE_ART|RESULT=", "FAIL" if checks_failed > 0 else "OK", " checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _init() -> void:
	call_deferred("_run")
