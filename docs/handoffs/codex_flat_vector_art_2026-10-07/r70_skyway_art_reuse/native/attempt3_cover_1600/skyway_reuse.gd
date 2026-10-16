extends RefCounted
# Nonproduction candidate: reuse the original source nodes and painted textures.
# No child input, source progress, foreground geometry, or callback replacement.
const MASTER_SIZE := Vector2(3640.0, 2048.0)
const TILE_SIZE := Vector2(910.0, 1024.0)
var _source: WeakRef
var _root_ref: WeakRef
var variant: String = ""
var applied_count: int = 0

func attach(source: RefCounted, requested: String) -> bool:
	if source == null or requested not in ["z_only", "cover"]:
		return false
	var root_control: Control = source.get("_root") as Control
	var tiles: Array = source.get("_tiles") as Array
	if root_control == null or tiles.size() != 8:
		return false
	for value: Variant in tiles:
		var tile: Sprite2D = value as Sprite2D
		if tile == null or tile.texture == null or tile.texture.get_size() != TILE_SIZE:
			return false
	_source = weakref(source)
	_root_ref = weakref(root_control)
	variant = requested
	root_control.resized.connect(_apply_visual_layout)
	_apply_visual_layout()
	return applied_count == 1

func _apply_visual_layout() -> void:
	var source: RefCounted = _source.get_ref() as RefCounted if _source != null else null
	var root_control: Control = _root_ref.get_ref() as Control if _root_ref != null else null
	if source == null or root_control == null:
		return
	var backdrop: ColorRect = source.get("_backdrop") as ColorRect
	var world: Node2D = source.get("_world") as Node2D
	if backdrop == null or world == null:
		return
	backdrop.z_index = -30
	if variant == "cover":
		var tiles: Array = source.get("_tiles") as Array
		var scale_value: float = maxf(root_control.size.x / MASTER_SIZE.x, root_control.size.y / MASTER_SIZE.y) / world.scale.x
		var center: Vector2 = world.transform.affine_inverse() * (root_control.size * 0.5)
		for index: int in range(tiles.size()):
			var tile: Sprite2D = tiles[index] as Sprite2D
			var row: int = index / 4
			var column: int = index % 4
			tile.scale = Vector2.ONE * scale_value
			tile.position = center + (Vector2(float(column) + 0.5, float(row) + 0.5) * TILE_SIZE - MASTER_SIZE * 0.5) * scale_value
	applied_count += 1

func audit_snapshot() -> Dictionary:
	var source: RefCounted = _source.get_ref() as RefCounted if _source != null else null
	var root_control: Control = _root_ref.get_ref() as Control if _root_ref != null else null
	return {"variant": variant, "applied_count": applied_count, "source_alive": source != null, "root_alive": root_control != null, "nodes_added": 0, "textures_replaced": 0, "progress_written": false, "foreground_geometry_written": false, "missing_resource_recovery_proven": false}
