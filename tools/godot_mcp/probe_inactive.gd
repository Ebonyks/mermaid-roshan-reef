extends SceneTree

func _initialize() -> void:
	call_deferred("_verify_inactive")

func _verify_inactive() -> void:
	var bridge: Node = root.get_node_or_null("MCPGameBridge")
	if EngineDebugger.is_active() or bridge == null:
		printerr("MCPINACTIVE|FAIL|Needs standalone launch and installed bridge")
		quit(1)
		return
	if bridge.is_processing() or bridge.is_physics_processing() or bridge.get_child_count() != 0:
		printerr("MCPINACTIVE|FAIL|Standalone bridge has active callbacks or children")
		quit(1)
		return
	print("MCPINACTIVE|PASS|No processing, physics callbacks or runtime sampler without debugger")
	quit(0)
