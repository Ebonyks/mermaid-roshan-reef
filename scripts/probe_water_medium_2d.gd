extends SceneTree

const WATER_MEDIUM_STATE_SCRIPT := preload("res://scripts/water/water_medium_state_2d.gd")
const TEST_BODY_HEIGHT: float = 100.0
const TIME_EPSILON: float = 0.00001

var _failed: bool = false


func _sample(
		column_ratio: float,
		support_acquired: bool,
		contact_inside: bool,
		face_ratio: float = -0.5,
		intent: int = WATER_MEDIUM_STATE_SCRIPT.Intent.NONE,
		dive_contact_complete: bool = false,
		emerge_contact_complete: bool = false,
		normal_velocity_hps: float = 0.0
) -> Dictionary:
	return {
		"body_height": TEST_BODY_HEIGHT,
		"water_column_depth": column_ratio * TEST_BODY_HEIGHT,
		"support_acquired": support_acquired,
		"contact_inside": contact_inside,
		"face_depth": face_ratio * TEST_BODY_HEIGHT,
		"normal_velocity_hps": normal_velocity_hps,
		"intent": intent,
		"dive_contact_complete": dive_contact_complete,
		"emerge_contact_complete": emerge_contact_complete,
	}


func _check(condition: bool, label: String) -> void:
	if condition:
		return
	_failed = true
	print("WATER_MEDIUM|FAIL|", label)


func _transition_time(
		reducer: Variant,
		hz: int,
		sample: Dictionary,
		expected_state: int,
		required_hold: float,
		label: String
) -> float:
	var delta_seconds: float = 1.0 / float(hz)
	var elapsed: float = 0.0
	for _step: int in range(hz):
		reducer.advance(delta_seconds, sample)
		elapsed += delta_seconds
		if reducer.current_state == expected_state:
			_check(elapsed + TIME_EPSILON >= required_hold,
				label + " transitioned before its stable hold")
			_check(elapsed < required_hold + delta_seconds + TIME_EPSILON,
				label + " transitioned later than one sample after its stable hold")
			return elapsed
	_check(false, label + " did not transition")
	return -1.0


func _run_matrix(hz: int) -> Array[float]:
	var reducer: Variant = WATER_MEDIUM_STATE_SCRIPT.new()
	var timings: Array[float] = []
	timings.append(_transition_time(reducer, hz,
		_sample(0.15, true, true), WATER_MEDIUM_STATE_SCRIPT.State.SHALLOW_WADE,
		WATER_MEDIUM_STATE_SCRIPT.DRY_WADE_HOLD_SECONDS, "dry to wade at %d Hz" % hz))
	timings.append(_transition_time(reducer, hz,
		_sample(0.75, false, true, -0.10, WATER_MEDIUM_STATE_SCRIPT.Intent.DEEP_TARGET),
		WATER_MEDIUM_STATE_SCRIPT.State.SURFACE_SWIM,
		WATER_MEDIUM_STATE_SCRIPT.WADE_SURFACE_HOLD_SECONDS, "wade to surface at %d Hz" % hz))
	timings.append(_transition_time(reducer, hz,
		_sample(0.75, false, true, 0.22, WATER_MEDIUM_STATE_SCRIPT.Intent.DEEP_TARGET, true),
		WATER_MEDIUM_STATE_SCRIPT.State.SUBMERGED,
		WATER_MEDIUM_STATE_SCRIPT.SURFACE_SUBMERGED_HOLD_SECONDS,
		"surface to submerged at %d Hz" % hz))
	timings.append(_transition_time(reducer, hz,
		_sample(0.75, false, true, 0.05, WATER_MEDIUM_STATE_SCRIPT.Intent.RISE_OR_EXIT,
			false, true), WATER_MEDIUM_STATE_SCRIPT.State.SURFACE_SWIM,
		WATER_MEDIUM_STATE_SCRIPT.SURFACE_SUBMERGED_HOLD_SECONDS,
		"submerged to surface at %d Hz" % hz))
	timings.append(_transition_time(reducer, hz,
		_sample(0.45, true, true), WATER_MEDIUM_STATE_SCRIPT.State.SHALLOW_WADE,
		WATER_MEDIUM_STATE_SCRIPT.SURFACE_WADE_HOLD_SECONDS, "surface to wade at %d Hz" % hz))
	timings.append(_transition_time(reducer, hz,
		_sample(0.03, true, false), WATER_MEDIUM_STATE_SCRIPT.State.DRY,
		WATER_MEDIUM_STATE_SCRIPT.DRY_WADE_HOLD_SECONDS, "wade to dry at %d Hz" % hz))
	_check(reducer.transition_count == 6,
		"matrix at %d Hz should contain exactly six transitions" % hz)
	return timings


func _check_rate_equivalence() -> void:
	var timings_30: Array[float] = _run_matrix(30)
	var timings_60: Array[float] = _run_matrix(60)
	_check(timings_30.size() == timings_60.size(), "rate matrices have different sizes")
	for index: int in range(mini(timings_30.size(), timings_60.size())):
		_check(absf(timings_30[index] - timings_60[index]) <= (1.0 / 60.0) + TIME_EPSILON,
			"30/60 Hz transition timing differs at matrix index %d" % index)


func _assert_jitter(
		hz: int,
		initial_state: int,
		first_sample: Dictionary,
		second_sample: Dictionary,
		label: String
) -> void:
	var reducer: Variant = WATER_MEDIUM_STATE_SCRIPT.new()
	reducer.reset(initial_state)
	var delta_seconds: float = 1.0 / float(hz)
	for step: int in range(hz * 2):
		var sample: Dictionary = first_sample if step % 2 == 0 else second_sample
		reducer.advance(delta_seconds, sample)
	_check(reducer.current_state == initial_state, "%s changed state at %d Hz" % [label, hz])
	_check(reducer.transition_count == 0, "%s emitted a transition at %d Hz" % [label, hz])


func _check_threshold_jitter() -> void:
	for hz: int in [30, 60]:
		_assert_jitter(hz, WATER_MEDIUM_STATE_SCRIPT.State.DRY,
			_sample(0.121, true, true), _sample(0.119, true, true), "dry/wade enter jitter")
		_assert_jitter(hz, WATER_MEDIUM_STATE_SCRIPT.State.SHALLOW_WADE,
			_sample(0.059, true, false), _sample(0.061, true, true), "wade/dry exit jitter")
		_assert_jitter(hz, WATER_MEDIUM_STATE_SCRIPT.State.SHALLOW_WADE,
			_sample(0.681, false, true), _sample(0.679, false, true),
			"wade/surface enter jitter")
		_assert_jitter(hz, WATER_MEDIUM_STATE_SCRIPT.State.SURFACE_SWIM,
			_sample(0.519, true, true), _sample(0.521, true, true),
			"surface/wade exit jitter")
		_assert_jitter(hz, WATER_MEDIUM_STATE_SCRIPT.State.SURFACE_SWIM,
			_sample(0.75, false, true, 0.181, WATER_MEDIUM_STATE_SCRIPT.Intent.DEEP_TARGET, true),
			_sample(0.75, false, true, 0.179, WATER_MEDIUM_STATE_SCRIPT.Intent.DEEP_TARGET, true),
			"surface/submerged enter jitter")
		_assert_jitter(hz, WATER_MEDIUM_STATE_SCRIPT.State.SUBMERGED,
			_sample(0.75, false, true, 0.079, WATER_MEDIUM_STATE_SCRIPT.Intent.RISE_OR_EXIT,
				false, true),
			_sample(0.75, false, true, 0.081, WATER_MEDIUM_STATE_SCRIPT.Intent.RISE_OR_EXIT,
				false, true), "submerged/surface exit jitter")


func _check_interrupted_hold() -> void:
	var reducer: Variant = WATER_MEDIUM_STATE_SCRIPT.new()
	var delta_seconds: float = 1.0 / 60.0
	var enter_sample: Dictionary = _sample(0.15, true, true)
	for _step: int in range(5):
		reducer.advance(delta_seconds, enter_sample)
	_check(reducer.current_state == WATER_MEDIUM_STATE_SCRIPT.State.DRY,
		"partial hold should remain dry")
	reducer.advance(delta_seconds, _sample(0.119, true, true))
	for _step: int in range(5):
		reducer.advance(delta_seconds, enter_sample)
	_check(reducer.current_state == WATER_MEDIUM_STATE_SCRIPT.State.DRY,
		"an interrupted hold should restart from zero")
	reducer.advance(delta_seconds, enter_sample)
	_check(reducer.current_state == WATER_MEDIUM_STATE_SCRIPT.State.SHALLOW_WADE,
		"a restarted full hold should enter wade")


func _check_passive() -> void:
	var reducer: Variant = WATER_MEDIUM_STATE_SCRIPT.new()
	var passive_sample: Dictionary = _sample(0.0, true, false)
	for _step: int in range(60 * 10):
		reducer.advance(1.0 / 60.0, passive_sample)
	_check(reducer.current_state == WATER_MEDIUM_STATE_SCRIPT.State.DRY,
		"passive dry input should remain dry")
	_check(reducer.transition_count == 0, "passive dry input should emit zero transitions")
	_check(reducer.pending_state == -1, "passive dry input should leave no held candidate")


func _run() -> void:
	print("=== probe_water_medium_2d ===")
	_check_rate_equivalence()
	_check_threshold_jitter()
	_check_interrupted_hold()
	_check_passive()
	print("WATER_MEDIUM|RESULT=", "FAIL" if _failed else "OK")
	quit(1 if _failed else 0)


func _init() -> void:
	call_deferred("_run")
