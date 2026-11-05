extends SceneTree

func _initialize() -> void:
	call_deferred("_verify_inactive")

func _verify_inactive() -> void:
	if EngineDebugger.is_active() or not ProjectSettings.has_setting("autoload/MCPGameBridge"):
		printerr("MCPINACTIVE|FAIL|Needs standalone launch and installed bridge")
		quit(1)
		return
	await process_frame
	await process_frame
	if root.get_node_or_null("MCPGameBridge") != null:
		printerr("MCPINACTIVE|FAIL|Standalone bridge remains in the tree")
		quit(1)
		return
	print("MCPINACTIVE|PASS|Bridge removed without debugger; no runtime sampler or callbacks")
	quit(0)
