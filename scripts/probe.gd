extends SceneTree
func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var root_node: Node = ms.instantiate()
	get_root().add_child(root_node)
	await process_frame
	await process_frame
	var counts := {}
	_walk(root_node, counts)
	print("NODE CLASS COUNTS: ", counts)
	quit()
func _walk(n: Node, counts: Dictionary) -> void:
	var c: String = n.get_class()
	counts[c] = int(counts.get(c, 0)) + 1
	for ch in n.get_children():
		_walk(ch, counts)
