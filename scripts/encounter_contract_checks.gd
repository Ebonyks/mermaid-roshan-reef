class_name EncounterContractChecks
extends RefCounted

## Bounded, host independent checks for the reusable 2D encounter contract.
## The trusted boss probe calls run() so this stays out of the CI roster.

const ARENA_RADIUS: float = 26.0
const BOSS_POSITION := Vector2.ZERO
const PLAYER_POSITION := Vector2(8.0, -6.0)

static func run() -> Array[String]:
	var failures: Array[String] = []
	_check_profile("grand_puff", EncounterProfile2D.grand_puff(), failures)
	_check_profile("pepper", EncounterProfile2D.pepper(7), failures)
	_check_custom_order(failures)
	_check_restore(failures)
	return failures


static func _check_profile(label: String, profile: EncounterProfile2D,
		failures: Array[String]) -> void:
	if not profile.is_valid():
		_fail(failures, "%s profile is invalid" % label)
		return
	if profile.phases.size() < 2:
		_fail(failures, "%s does not exercise variable phase counts" % label)
	_check_geometry(profile, label, failures)
	_check_no_input(profile, label, failures)
	_check_repeated_impact(profile, label, failures)
	_check_clean_completion(profile, label, failures)
	_check_assistance(profile, label, failures)


static func _check_geometry(profile: EncounterProfile2D, label: String,
		failures: Array[String]) -> void:
	var patterns := EncounterPatterns2D.new(profile)
	for phase_index: int in range(profile.phases.size()):
		var phase: EncounterPhase2D = profile.phases[phase_index]
		for step_index: int in range(phase.attacks.size()):
			var player := _edge_point(step_index * 3 + phase_index)
			patterns.begin_phase(phase_index, player, BOSS_POSITION, ARENA_RADIUS)
			for _advance: int in range(step_index):
				patterns.advance_combo(player, BOSS_POSITION, ARENA_RADIUS)
			var first: Dictionary = patterns.readout()
			var expected_shape: String = "lane" if phase.attacks[step_index].shape == EncounterAttack2D.Shape.LANE else "circle"
			if String(first.get("shape", "")) != expected_shape:
				_fail(failures, "%s phase %d step %d shape mismatch" % [label, phase_index, step_index])
			if not bool(first.get("locked", false)) or not bool(first.get("active", false)):
				_fail(failures, "%s phase %d step %d is not locked during tell" % [label, phase_index, step_index])
			var safe: Vector2 = first.get("safe_point", Vector2.ZERO) as Vector2
			if patterns.contains(safe, 1.2) or not _inside_octagon(safe):
				_fail(failures, "%s phase %d step %d has unsafe escape point" % [label, phase_index, step_index])
			patterns.tick(0.2)
			var moved: Dictionary = patterns.readout()
			if not _same_geometry(first, moved):
				_fail(failures, "%s phase %d step %d target moved during tell" % [label, phase_index, step_index])
			for edge_index: int in range(16):
				var edge_player := _edge_point(edge_index)
				patterns.begin_phase(phase_index, edge_player, BOSS_POSITION, ARENA_RADIUS)
				var edge_safe: Vector2 = patterns.readout().get("safe_point", Vector2.ZERO) as Vector2
				if patterns.contains(edge_safe, 1.2) or not _inside_octagon(edge_safe):
					_fail(failures, "%s phase %d edge %d cannot escape" % [label, phase_index, edge_index])


static func _check_no_input(profile: EncounterProfile2D, label: String,
		failures: Array[String]) -> void:
	var encounter := BossEncounter2D.new()
	encounter.configure(profile)
	encounter.begin_attack(PLAYER_POSITION, BOSS_POSITION, ARENA_RADIUS)
	encounter.tick_tell(20.0)
	if encounter.completed_rounds != 0 or encounter.finished():
		_fail(failures, "%s no input auto-completed" % label)
	if encounter.try_counter(true, true, true):
		_fail(failures, "%s stale counter succeeded before strike" % label)


static func _check_repeated_impact(profile: EncounterProfile2D, label: String,
		failures: Array[String]) -> void:
	var encounter := BossEncounter2D.new()
	encounter.configure(profile)
	encounter.begin_attack(PLAYER_POSITION, BOSS_POSITION, ARENA_RADIUS)
	encounter.tick_tell(20.0)
	encounter.begin_strike()
	var danger: Vector2 = encounter.patterns.readout().get("center", PLAYER_POSITION) as Vector2
	if encounter.resolve_impact(danger, BOSS_POSITION, ARENA_RADIUS) != BossEncounter2D.Impact.HIT:
		_fail(failures, "%s did not register an intentional hit" % label)
	if encounter.resolve_impact(danger, BOSS_POSITION, ARENA_RADIUS) != BossEncounter2D.Impact.IGNORED:
		_fail(failures, "%s repeated impact was not ignored" % label)


static func _check_clean_completion(profile: EncounterProfile2D, label: String,
		failures: Array[String]) -> void:
	var encounter := BossEncounter2D.new()
	encounter.configure(profile)
	while not encounter.finished():
		encounter.begin_attack(PLAYER_POSITION, BOSS_POSITION, ARENA_RADIUS)
		var guard: int = 0
		while encounter.state == BossEncounter2D.State.TELL and guard < 16:
			encounter.tick_tell(20.0)
			encounter.begin_strike()
			var safe: Vector2 = encounter.patterns.readout().get("safe_point", Vector2.ZERO) as Vector2
			var impact: BossEncounter2D.Impact = encounter.resolve_impact(safe, BOSS_POSITION, ARENA_RADIUS)
			guard += 1
			if impact == BossEncounter2D.Impact.IGNORED or impact == BossEncounter2D.Impact.HIT:
				_fail(failures, "%s clean movement failed at round %d" % [label, encounter.completed_rounds])
				return
		if guard >= 16:
			_fail(failures, "%s combo did not resolve" % label)
			return
		if encounter.state != BossEncounter2D.State.COUNTER_READY:
			_fail(failures, "%s clean combo did not open counter" % label)
			return
		encounter.open_counter()
		var before: int = encounter.completed_rounds
		if not encounter.try_counter(true, true, true) or encounter.completed_rounds != before + 1:
			_fail(failures, "%s intentional counter did not complete once" % label)
			return
		if encounter.try_counter(true, true, true) or encounter.completed_rounds != before + 1:
			_fail(failures, "%s repeated counter succeeded" % label)


static func _check_assistance(profile: EncounterProfile2D, label: String,
		failures: Array[String]) -> void:
	var encounter := BossEncounter2D.new()
	encounter.configure(profile, 0, 2, 1)
	encounter.begin_attack(PLAYER_POSITION, BOSS_POSITION, ARENA_RADIUS)
	if encounter.patterns.tell_time <= profile.phases[0].attacks[0].warning_seconds:
		_fail(failures, "%s damage/miss assistance did not extend tell" % label)
	if encounter.counter_window() <= profile.counter_seconds:
		_fail(failures, "%s miss assistance did not extend counter" % label)
	if encounter.try_counter(true, false, true) or encounter.try_counter(false, true, true):
		_fail(failures, "%s invalid or held counter succeeded" % label)


static func _check_custom_order(failures: Array[String]) -> void:
	var profile := EncounterProfile2D.new()
	profile.encounter_id = &"custom_order"
	profile.phases = [
		EncounterPhase2D.make(&"three", [EncounterAttack2D.lane(), EncounterAttack2D.circle(), EncounterAttack2D.lane()]),
		EncounterPhase2D.make(&"one", [EncounterAttack2D.circle()]),
	]
	_check_profile("custom_order", profile, failures)


static func _check_restore(failures: Array[String]) -> void:
	for pair: Array in [[EncounterProfile2D.grand_puff(), 3], [EncounterProfile2D.pepper(7), 7]]:
		var encounter := BossEncounter2D.new()
		encounter.configure(pair[0] as EncounterProfile2D, pair[1] as int)
		if not encounter.finished() or encounter.state != BossEncounter2D.State.COMPLETE:
			_fail(failures, "restore final %d did not complete" % int(pair[1]))


static func _edge_point(index: int) -> Vector2:
	var angle: float = TAU * float(index % 16) / 16.0
	return Vector2(cos(angle), sin(angle)) * ARENA_RADIUS


static func _inside_octagon(point: Vector2) -> bool:
	var limit: float = ARENA_RADIUS * cos(PI / 8.0) - 2.6
	for index: int in range(8):
		var normal := Vector2(cos(float(index) * PI / 4.0), sin(float(index) * PI / 4.0))
		if point.dot(normal) > limit + 0.05:
			return false
	return true


static func _same_geometry(a: Dictionary, b: Dictionary) -> bool:
	if String(a.get("shape", "")) != String(b.get("shape", "")):
		return false
	for key: String in ["center", "locked_center", "direction", "from", "to"]:
		if a.has(key) and (a.get(key) as Vector2).distance_to(b.get(key) as Vector2) > 0.01:
			return false
	return true


static func _fail(failures: Array[String], message: String) -> void:
	failures.append(message)
