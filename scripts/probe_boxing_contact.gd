extends SceneTree
## Focused entry point; the same cases also run in trusted probe_opera_2d.

func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var start := Time.get_ticks_usec()
	var suite := preload("res://scripts/probe_boxing_contact_cases.gd").new()
	var results: Array[Dictionary] = suite.run(root)
	results.append_array(await suite.run_routed(root))
	var bad := 0
	for result: Dictionary in results:
		var passed := bool(result["passed"])
		print("BOXINGCONTACT|", "PASS" if passed else "FAIL", "|", result["label"])
		if not passed:
			bad += 1
	print("BOXINGCONTACT|COUNTS|geometry=", suite.geometry_cases, "|held_flights=", suite.flight_cases,
		"|adversarial_events=", suite.fuzz_events, "|desktop_elapsed_ms=", float(Time.get_ticks_usec() - start) / 1000.0)
	print("BOXINGCONTACT|RESULT|", "ALL OK" if bad == 0 else "FAIL")
	# Let awaited probe states and their script references unwind before exit.
	call_deferred("quit", 0 if bad == 0 else 1)
