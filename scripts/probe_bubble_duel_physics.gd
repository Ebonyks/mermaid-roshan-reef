extends SceneTree
## Source-bound numerical comparison, not a rendered playthrough or fun rating.

const Fighter := preload("res://scripts/bubble_duel_fighter.gd")
const Motion := preload("res://scripts/bubble_duel_motion.gd")
var failures: Array[String] = []
var checks: int = 0


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var raw: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://assets_src/bubble_duel_physics_20261105/reference-traces.json"))
	if not raw is Dictionary:
		print("DUEL_REFERENCE|FAIL|missing reference")
		quit(1)
		return
	var source: Dictionary = raw
	var results: Array[Dictionary] = []
	var motion: BubbleDuelMotion = Motion.new()
	for value: Variant in source["cases"]:
		var spec: Dictionary = value
		var fighter: BubbleDuelFighter = Fighter.new()
		fighter.reset(Vector2(float(spec.get("x", 200)), float(spec.get("y", 160))), float(spec.get("vy", 0)))
		fighter.human = 0
		fighter.velocity.x = float(spec.get("vx", 0))
		fighter.spares = int(spec.get("spares", 4))
		fighter.bubbles = int(spec.get("bubbles", 2))
		fighter.held = int(spec.get("held", 0))
		var drift: float = float(spec.get("drift", 0.5))
		var worst: float = 0.0
		var squared: float = 0.0
		var numeric_count: int = 0
		var kicks := PackedInt32Array()
		for kick_value: Variant in spec.get("kicks", []):
			kicks.append(int(kick_value))
		for tick: int in range(int(spec["frames"])):
			var dirs: Dictionary = spec.get("dirs", {})
			var axis: float = float(dirs.get(str(tick), spec.get("dir", 0)))
			var period: int = int(spec.get("period", 0))
			var press: bool = tick in kicks or (period > 0 and tick % period == 0)
			if not fighter.lost:
				if fighter.held > 0:
					fighter.held -= 1
					axis = 0.0
					press = false
				fighter.direction = axis
				if axis != 0.0:
					fighter.facing = signf(axis)
				if press:
					motion.kick(fighter, axis)
				motion.integrate(fighter, drift, int(spec.get("stage", 0)), bool(spec.get("kind", false)))
			drift = maxf(0.0, drift - 0.002)
			var actual: Array = [fighter.position.x, fighter.position.y, fighter.velocity.x, fighter.velocity.y,
				fighter.bubbles, fighter.spares, fighter.inflation, fighter.charge, fighter.invincible, fighter.held, fighter.lost]
			var expected: Array = spec["trace"][tick]
			for field: int in range(10):
				var difference: float = absf(float(actual[field]) - float(expected[field]))
				worst = maxf(worst, difference)
				squared += difference * difference
				numeric_count += 1
				checks += 1
				if difference > 0.001 and failures.size() < 30:
					failures.append("%s tick%d field%d error%f" % [String(spec["id"]), tick, field, difference])
			checks += 1
			if bool(actual[10]) != bool(expected[10]):
				failures.append("%s lost state differs" % String(spec["id"]))
		results.append({"id": spec["id"], "max_logical_error": worst,
			"rms_error": sqrt(squared / float(maxi(1, numeric_count))), "steps": spec["frames"]})
	for value: Variant in source["wrap_samples"]:
		var sample: Array = value
		checks += 1
		if absf(Motion.wrapped_dx(float(sample[0])) - float(sample[1])) > 0.00001:
			failures.append("wrapped half-width tie differs at %s" % str(sample[0]))
	var output: String = OS.get_environment("DUEL_PHYSICS_REPORT")
	if output.is_empty():
		output = "res://assets_src/bubble_duel_physics_20261105/reference-check.json"
	var report: Dictionary = {"engine": Engine.get_version_info(), "checks": checks, "cases": results,
		"failures": failures, "result": "PASS" if failures.is_empty() else "FAIL",
		"source_hashes": {"motion": FileAccess.get_sha256("res://scripts/bubble_duel_motion.gd"),
			"fighter": FileAccess.get_sha256("res://scripts/bubble_duel_fighter.gd"),
			"reference": FileAccess.get_sha256("res://assets_src/bubble_duel_physics_20261105/reference-traces.json")},
		"scope": "Original-frame movement traces with strict0.001 logical-unit tolerance (0.0021 canvas pixels); not human feel, rendering, or whole-game acceptance."}
	var file: FileAccess = FileAccess.open(output, FileAccess.WRITE)
	if file != null:
		file.store_string(JSON.stringify(report, "\t") + "\n")
		file.close()
	else:
		failures.append("cannot record report")
	for failure: String in failures:
		print("DUEL_REFERENCE|FAIL|", failure)
	print("DUEL_REFERENCE|RESULT|", report["result"], "|checks=", checks)
	quit(0 if failures.is_empty() else 1)
