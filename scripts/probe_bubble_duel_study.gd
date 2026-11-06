extends SceneTree
## Complete bouts driven by observable-state input policies; no mid-bout warps.
const Arena := preload("res://scripts/bubble_duel_arena.gd")
const Fighter := preload("res://scripts/bubble_duel_fighter.gd")
const Brain := preload("res://scripts/bubble_duel_brain.gd")

var failures: Array[String] = []
var checks: int = 0
var host: ReefMain
var geometry: BubbleDuelGeometry
var source_cases: Array = []


func _init() -> void:
	call_deferred("_run")


func _expect(value: bool, message: String) -> void:
	checks += 1
	if not value and failures.size() < 40:
		failures.append(message)


func _profile(person: String, gear: String = "classic") -> Dictionary:
	return {"character": person, "gear": gear, "look": "set:classic", "color": 0}


func _run() -> void:
	host = (load("res://scripts/main.gd") as GDScript).new() as ReefMain
	geometry = BubbleDuelGeometry.new(BubbleDuelCast.new(host))
	source_cases = JSON.parse_string(FileAccess.get_file_as_string("res://assets_src/bubble_duel_physics_20261105/reference-traces.json"))["cases"]
	var variants: Array = [{"id": "reference-pilot", "params": {}}]
	var input: String = OS.get_environment("DUEL_STUDY_CONFIG")
	if not input.is_empty():
		var raw: Variant = JSON.parse_string(FileAccess.get_file_as_string(input))
		if not raw is Dictionary or not raw.get("variants") is Array:
			print("DUEL_STUDY|FAIL|bad config")
			quit(1)
			return
		variants = raw["variants"]
	_expect(variants.size() > 0 and variants.size() <= 50, "variant budget")
	var all_results: Array[Dictionary] = []
	for value: Variant in variants:
		var variant: Dictionary = value
		var bouts: Array[Dictionary] = []
		for index: int in range(int(variant.get("bouts", 5))):
			var enemies: int = 1 + index % 3
			bouts.append(_bout(variant, index, enemies))
		var result: Dictionary = {"id": variant["id"], "params": variant["params"], "bouts": bouts, "source_rms_error": _trace_error(variant["params"])}
		all_results.append(result)
		print("DUEL_STUDY|VARIANT|", variant["id"], "|bouts=", bouts.size())
	_passive_and_held_controls()
	var output: String = OS.get_environment("DUEL_STUDY_REPORT")
	if output.is_empty():
		output = "res://assets_src/bubble_duel_physics_20261105/pilot-bouts.json"
	var report: Dictionary = {"result": "PASS" if failures.is_empty() else "FAIL", "checks": checks,
		"failures": failures, "variants": all_results, "engine": Engine.get_version_info(),
		"hashes": {"arena": FileAccess.get_sha256("res://scripts/bubble_duel_arena.gd"),
			"motion": FileAccess.get_sha256("res://scripts/bubble_duel_motion.gd"),
			"brain": FileAccess.get_sha256("res://scripts/bubble_duel_brain.gd"),
			"fighter": FileAccess.get_sha256("res://scripts/bubble_duel_fighter.gd")},
		"scope": "Production source-alpha geometry on the actual shared engine, all six characters, input-only policies at3.3–5Hz, one/two/three enemies and all four inflation stages. Numerical fidelity and bot pacing only; no human fun or physical-device acceptance."}
	var file: FileAccess = FileAccess.open(output, FileAccess.WRITE)
	if file == null:
		failures.append("cannot write report")
	else:
		file.store_string(JSON.stringify(report, "\t") + "\n")
		file.close()
	for failure: String in failures:
		print("DUEL_STUDY|FAIL|", failure)
	print("DUEL_STUDY|RESULT|", "PASS" if failures.is_empty() else "FAIL", "|checks=", checks)
	host.free()
	quit(0 if failures.is_empty() else 1)


func _bout(variant: Dictionary, index: int, enemies: int) -> Dictionary:
	var world: BubbleDuelArena = Arena.new()
	world.reset(index % 4, 7001 + index * 137)
	world.prepare_geometry = geometry.apply
	_expect(world.motion.configure(variant["params"]), "valid closed tuning")
	var player: BubbleDuelFighter = world.add_human(_profile(BubbleDuelCast.PEOPLE[index % 6]), 0, 0, 0, enemies > 1)
	for enemy: int in range(enemies):
		world.add_cpu(_profile(["rumi", "marlo", "daddy_mermaid"][enemy]), 25.0 + float(enemy) * 15.0,
			30.0 + float(enemy) * 15.0, 10 + enemy * 20, 1, 0)
	for fighter: BubbleDuelFighter in world.fighters:
		geometry.apply(fighter, 0)
	var policy := BubbleDuelTestPolicy.new(9173 + index * 83, 6 + index % 4, true)
	world.queue_kick(0, 0.0)
	var steps: int = 0
	while not world.finished and steps < 7200:
		var action: Dictionary = policy.observe(player, world, steps)
		world.set_direction(0, float(action["axis"]))
		if bool(action["flap"]): world.queue_kick(0, float(action["axis"]))
		world.step()
		steps += 1
		if steps % 30 == 0:
			for fighter: BubbleDuelFighter in world.fighters:
				_expect(fighter.position.is_finite() and fighter.velocity.is_finite(), "finite movement")
				_expect(fighter.position.x >= -15.001 and fighter.position.x <= 415.001, "wrap bounds")
				_expect(fighter.bubbles >= 0 and fighter.bubbles <= 2 and fighter.spares >= 0, "stock bounds")
				_expect(fighter.charge >= 0.0 and fighter.charge <= 100.001, "charge bounds")
	if not world.finished:
		for f: BubbleDuelFighter in world.fighters:
			print("STALL|",f.slot,"|",f.position,"|",f.velocity,"|bubbles=",f.bubbles,"|lost=",f.lost)
	_expect(world.started and player.consumed_inputs > 0, "real queued human control starts bout")
	if bool(variant.get("require_complete", true)):
		_expect(world.finished, "bout completes without relocation or forced outcome %s/%d" % [String(variant["id"]), index])
	_expect(world.pops > 0, "physical bubble contacts occur")
	return {"index": index, "enemy_count": enemies, "stage": world.stage,
		"complete": world.finished, "winner_team": world.winner, "ticks": steps,
		"seconds": float(steps) / 30.0, "pops": world.pops, "bump_contacts": world.bumps,
		"exchanged_motion": world.exchanged_motion, "player_flaps": player.kick_count,
		"player_pops": player.pops, "player_rescues": player.rescues,
		"input_policy": "observer-controlled maximum5Hz original-style impulses; no position/velocity edits to fighters"}


func _passive_and_held_controls() -> void:
	var world: BubbleDuelArena = Arena.new()
	world.reset()
	var player: BubbleDuelFighter = world.add_human(_profile("roshan"), 0, 0)
	world.add_cpu(_profile("rumi"), 100.0, 100.0, 100)
	var at: Vector2 = player.position
	for tick: int in range(300):
		world.set_direction(0, 1.0)
		world.step()
	_expect(not world.started and not world.finished and world.frame == 0, "direction alone cannot start or win")
	_expect(player.position == at and player.kick_count == 0, "held direction is not thrust")
	world.queue_kick(0, 1.0)
	world.step()
	var kicks: int = player.kick_count
	for tick: int in range(10):
		world.set_direction(0, 1.0)
		world.step()
	_expect(player.kick_count == kicks, "one press yields one impulse")
	var momentum: Vector2 = player.velocity
	world.clear_controls()
	_expect(player.velocity == momentum, "input neutralization keeps lawful momentum")


func _trace_error(params: Dictionary) -> float:
	var error: float = 0.0
	var count: int = 0
	for value: Variant in source_cases:
		var spec: Dictionary = value
		var motion := BubbleDuelMotion.new()
		motion.configure(params)
		var f := BubbleDuelFighter.new()
		f.human = 0
		f.reset(Vector2(float(spec.get("x", 200)), float(spec.get("y", 160))), float(spec.get("vy", 0)))
		f.velocity.x = float(spec.get("vx", 0))
		f.spares = int(spec.get("spares", 4))
		f.bubbles = int(spec.get("bubbles", 2))
		f.held = int(spec.get("held", 0))
		var drift: float = float(spec.get("drift", 0.5))
		var kicks := PackedInt32Array()
		for item: Variant in spec.get("kicks", []): kicks.append(int(item))
		for tick: int in range(int(spec["frames"])):
			var dirs: Dictionary = spec.get("dirs", {})
			var axis: float = float(dirs.get(str(tick), spec.get("dir", 0)))
			var period: int = int(spec.get("period", 0))
			var press: bool = tick in kicks or (period > 0 and tick % period == 0)
			if not f.lost:
				if f.held > 0:
					f.held -= 1
					axis = 0.0
					press = false
				if press: motion.kick(f, axis)
				motion.integrate(f, drift, int(spec.get("stage", 0)), bool(spec.get("kind", false)))
			drift = maxf(0.0, drift - 0.002)
			var expected: Array = spec["trace"][tick]
			for field: int in range(4):
				var actual: float = [f.position.x, f.position.y, f.velocity.x, f.velocity.y][field]
				error += pow(actual - float(expected[field]), 2)
				count += 1
	return sqrt(error / float(maxi(1, count)))
