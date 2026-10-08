extends SceneTree

func _init() -> void:
	print("ENGINEERING_CUES|BEGIN")
	call_deferred("_run")

func _run() -> void:
	var director_script: GDScript = load("res://scripts/audio_director.gd")
	print("ENGINEERING_CUES|LOADED")
	var director: RefCounted = director_script.new(null)
	var failed: int = 0
	for cue: String in ["op_astronaut_gears", "op_astronaut_pressure"]:
		var path: String = String(director.call("_voice_path", "roshan", cue, false))
		var expected: String = "res://assets/audio/voices/astronaut_engineering_v1/roshan_" + cue + ".ogg"
		var stream: AudioStream = load(path) as AudioStream if path != "" else null
		var okay: bool = path == expected and stream != null
		print("ENGINEERING_CUES|", cue, "|", "PASS" if okay else "FAIL")
		if not okay:
			failed += 1
	print("ENGINEERING_CUES|", "ALL OK" if failed == 0 else "FAIL")
	quit(0 if failed == 0 else 1)
