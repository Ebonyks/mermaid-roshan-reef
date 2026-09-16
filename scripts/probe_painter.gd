extends SceneTree


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	if "--capture" in OS.get_cmdline_user_args():
		root.mode = Window.MODE_WINDOWED
		root.size = Vector2i(1280, 800 if "--tall" in OS.get_cmdline_user_args() else 720)
		await process_frame
		await process_frame
	var probe := preload("res://scripts/painter/painter_probe.gd").new()
	var passed: bool = await probe.run(self)
	probe = null
	await process_frame
	# Let the audio server retire stopped playbacks before process teardown.
	await create_timer(0.1).timeout
	quit(0 if passed else 1)
