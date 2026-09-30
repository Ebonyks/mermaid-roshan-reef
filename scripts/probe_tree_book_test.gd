extends SceneTree
func _init() -> void:
	call_deferred("_run")
func _run() -> void:
	var checks := preload("res://scripts/tree_book_test_checks.gd").new()
	var ok: bool = await checks.run(root)
	print("TREE_BOOK|ALL OK" if ok else "TREE_BOOK|FAIL")
	quit(0 if ok else 1)
