extends SceneTree
func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"): main._skip_intro()
	await process_frame
	var n := 0
	for ln in ["talk","whale","ship","wreck","intro1","intro4","win","pearl"]:
		if ResourceLoader.exists("res://assets/audio/voices/roshan_%s.ogg" % ln):
			n += 1
	print("Roshan voice clips present: %d / 8" % n)
	main._say("roshan", "whale")
	main._say("roshan", "win")
	await process_frame
	print("voice playback: no error")
	quit()
