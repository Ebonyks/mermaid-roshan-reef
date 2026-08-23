extends SceneTree

const PoolSurfaceLife := preload("res://scripts/castle_pool_surface_life.gd")
const CASTLE_ROOMS_SOURCE := "res://scripts/arena/castle_rooms_25d.gd"
const PLAYER_BACK_DEPTH := 1.25
const SEAHORSE_STREAM_OFFSET := 0.013

var failures: Array[String] = []


func _init() -> void:
	print("=== probe_castle_pool_life_2d ===")
	var surface: CastlePoolSurfaceLife = PoolSurfaceLife.new()
	root.add_child(surface)
	var snapshot: Dictionary = surface.audit_snapshot()
	_check(bool(snapshot.get("canvas_only", false)),
		"pool life is a CanvasItem")
	_check(int(snapshot.get("point_count", 0)) == 4,
		"pool life is one bounded quad")
	_check(int(snapshot.get("surface_pixels", 0))
		<= int(snapshot.get("max_surface_pixels", 0)),
		"bounded fragment footprint stays within mobile budget")
	_check(float(snapshot.get("depth", 99.0)) < PLAYER_BACK_DEPTH,
		"water motion stays behind Roshan at every walk depth")
	_check(ResourceLoader.exists(String(snapshot.get("shader", ""))),
		"pool-life Canvas shader exists")
	_check(ResourceLoader.exists(String(snapshot.get("ripple", ""))),
		"approved ripple texture exists")
	_check(ResourceLoader.exists(String(snapshot.get("caustics", ""))),
		"approved caustics texture exists")
	var shader: Shader = load(String(snapshot.get("shader", ""))) as Shader
	_check(shader != null and "TIME" in shader.code,
		"water surface has continuous time-based motion")
	_check(shader != null and "pool_mask" in shader.code,
		"water motion is analytically clipped to the pool")
	var source := FileAccess.get_file_as_string(CASTLE_ROOMS_SOURCE)
	_check("CASTLE_POOL_SURFACE_LIFE.new()" in source,
		"Mermaid Pool builds the living surface")
	var seahorse_depth := _seahorse_depth_from_source(source)
	_check(seahorse_depth + SEAHORSE_STREAM_OFFSET < PLAYER_BACK_DEPTH,
		"seahorse body and stream always stay behind Roshan")
	_check("sprite.z_index = _depth_to_z_index(player_z)" in source,
		"tweened swims continuously refresh player depth")
	_check(_all_canvas_items(surface),
		"pool-life runtime subtree is true 2D")
	surface.queue_free()
	if failures.is_empty():
		print("PROBE castle pool life 2D: ALL OK")
		quit(0)
	else:
		for failure: String in failures:
			print("FAIL | ", failure)
		quit(1)


func _seahorse_depth_from_source(source: String) -> float:
	var marker := "\"pos\": Vector2(635, 90), \"z\": PLAYER_BACK_Z - 0.05"
	return PLAYER_BACK_DEPTH - 0.05 if marker in source else 99.0


func _all_canvas_items(node: Node) -> bool:
	if not node is CanvasItem:
		return false
	for child: Node in node.get_children():
		if not _all_canvas_items(child):
			return false
	return true


func _check(condition: bool, label: String) -> void:
	if condition:
		print("OK | ", label)
	else:
		failures.append(label)
