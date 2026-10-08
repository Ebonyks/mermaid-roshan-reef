extends "res://scripts/probe_opera_gesture_quality.gd"

func _init() -> void:
	call_deferred("_run_only")

func _run_only() -> void:
	await _test_astronaut_input()
	print("ASTRO_INPUT_RESULT|" + JSON.stringify({"checks": checks, "failed": failed,
		"input": "genuine Input.parse_input_event viewport dispatch",
		"focus": "synthetic notification boundary; not device acceptance",
		"pause": "SceneTree.paused engine notification",
		"scope": "input lifecycle regression only; not full action or visual grading"}))
	quit(0 if failed == 0 else 1)
