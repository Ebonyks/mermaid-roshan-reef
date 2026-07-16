extends SceneTree
# Audio routing smoke test: important sound families must not collapse back to
# Master, where dialogue cannot be protected independently.

var bad := 0

func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	for bus_name: String in ["Music", "Voice", "SFX", "Ambience", "UI"]:
		_check("%s bus exists" % bus_name, AudioServer.get_bus_index(bus_name) >= 0)
	_check("music is routed", main.music != null and main.music.bus == "Music")
	_check("voice fallback is routed", main.voice != null and main.voice.bus == "Voice")
	_check("voice pool is routed", not main.voice_pool.is_empty() and (main.voice_pool[0] as AudioStreamPlayer).bus == "Voice")
	_check("effects are routed", main.chime != null and main.chime.bus == "SFX")
	_check("ambience is routed", main.ambience != null and main.ambience.bus == "Ambience")
	main._ui_tap()
	await process_frame
	_check("UI taps are routed", main._tap_player != null and main._tap_player.bus == "UI")
	print("AUDIO|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _check(label: String, ok: bool) -> void:
	print("AUDIO|%s: %s" % [label, "OK" if ok else "FAIL"])
	if not ok:
		bad += 1
