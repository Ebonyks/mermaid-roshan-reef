extends "res://scripts/probe_opera_gesture_quality.gd"

func _init() -> void:
	call_deferred("_run_only")

func _run_only() -> void:
	await _test_astronaut_pipe_routes()
	print("ASTRO_PIPE_RESULT|" + JSON.stringify({"checks": checks, "failed": failed,
		"input": "genuine Input.parse_input_event viewport press/drag/release",
		"clock": "normal engine processing; no direct tick or progress injection",
		"completion": "fixture acknowledges third earned award; whole-world caller unverified",
		"scope": "three authored pipe routes only; not visual, return or save clearance"}))
	quit(0 if failed == 0 else 1)
