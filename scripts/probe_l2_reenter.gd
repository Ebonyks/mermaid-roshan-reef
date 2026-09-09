extends SceneTree
# Regression probe for stacked Sky Lagoon builds. A re-entry must synchronously
# release the prior CanvasLayer and construct exactly one fresh Canvas stage.

const TARGET_IDS: Array[String] = [
	"castle_gate", "seesaw", "slide", "swing",
]

var main: ReefMain


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _spatial_descendants(node: Node) -> int:
	var count := 1 if node.is_class("Node" + "3D") else 0
	for child: Node in node.get_children():
		count += _spatial_descendants(child)
	return count


func _named_layer_count(node: Node) -> int:
	var count := 1 if node is CanvasLayer \
		and node.name == &"SkyLagoonCanvasLayer" else 0
	for child: Node in node.get_children():
		count += _named_layer_count(child)
	return count


func _target_ids() -> Array[String]:
	var ids: Array[String] = []
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		ids.append(String((value as Dictionary).get("id", "")))
	ids.sort()
	return ids


func _tile_count(root_node: Node) -> int:
	var count := 1 if root_node is Sprite2D \
		and root_node.name.begins_with("SkyLagoonBackdrop_") else 0
	for child: Node in root_node.get_children():
		count += _tile_count(child)
	return count


func _init() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.intro_active:
		main._skip_intro()
	await _frames(2)
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.save_data["lagoon_plane_departed"] = true
	main._enter_level2()
	await _frames(12)
	var first: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var first_root: CanvasLayer = first.root()
	first.set_master_route_x(3072.0)
	await _frames(4)
	var first_ok: bool = first_root != null and is_instance_valid(first_root) \
		and first_root.layer == main.SKY_LAGOON_STAGE_CANVAS_LAYER \
		and _spatial_descendants(first_root) == 0 \
		and _tile_count(first_root) == 12 and _target_ids() == TARGET_IDS \
		and _named_layer_count(get_root()) == 1

	# Galaxy/kart returns use this path without a caller-side teardown. A stale
	# layer must be invalid immediately after build, not merely queued for later.
	main._enter_level2(true)
	var second: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var second_root: CanvasLayer = second.root()
	await _frames(4)
	var second_ok: bool = second_root != null and is_instance_valid(second_root) \
		and second_root != first_root and not is_instance_valid(first_root) \
		and second_root.layer == main.SKY_LAGOON_STAGE_CANVAS_LAYER \
		and _spatial_descendants(second_root) == 0 \
		and _tile_count(second_root) == 12 and _target_ids() == TARGET_IDS \
		and _named_layer_count(get_root()) == 1
	print("REENTER|canvas_first: ", "OK" if first_ok else "FAIL")
	print("REENTER|canvas_rebuild_no_stack: ", "OK" if second_ok else "FAIL")
	if not (first_ok and second_ok):
		print("FAIL|Sky Lagoon Canvas re-entry regression")
		quit(1)
	else:
		print("REENTER|ALL OK")
		quit(0)
