extends SceneTree

# Blocking contract probe for the reusable one-finger dodge engine.  This is
# deliberately a pure SceneTree probe: no arena, camera, or player scene can
# hide timing, touch, or allocation mistakes in the movement primitive.

const EPS := 0.0001
const EDGE_APOTHEM := 24.0
const ITERATIONS := 4096
const SAMPLE_HZ := [20.0, 30.0, 60.0, 120.0]

var failures := 0

func _init() -> void:
	_case_window_availability()
	_case_threat_proximity()
	_case_gesture_shapes()
	_case_landing_frame()
	_case_eased_rate_invariance()
	_case_arena_edge_clamp()
	_case_seeded_stress()
	_case_zero_input()
	var verdict: String = "ALL OK" if failures == 0 else "%d check(s) FAILED" % failures
	print("DODGEENGINE|result: ", verdict)
	quit(0 if failures == 0 else 1)

func _ck(label: String, ok: bool) -> void:
	print("DODGEENGINE|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		failures += 1

func _new_landing(landing: Vector2 = Vector2.ZERO, eta: float = 0.0,
		player: Vector2 = Vector2.ZERO) -> DodgeEngine:
	var engine := DodgeEngine.new()
	engine.begin_landing(landing, eta)
	engine.update_window(eta, player)
	return engine

func _valid_horizontal(engine: DodgeEngine, direction: float = 1.0,
		length: float = 120.0) -> bool:
	var from := Vector2.ZERO
	var to := Vector2(length * direction, 0.0)
	return engine.try_swipe(from, to)

func _case_window_availability() -> void:
	var early := DodgeEngine.new()
	early.begin_landing(Vector2.ZERO, DodgeEngine.READY_LEAD_T + EPS)
	_ck("early window stays closed", not early.update_window(
		DodgeEngine.READY_LEAD_T + EPS, Vector2.ZERO) and not early.available)

	var near := DodgeEngine.new()
	near.begin_landing(Vector2.ZERO, 0.40)
	_ck("near landing exposes dodge", near.update_window(0.40, Vector2(
		DodgeEngine.DANGER_RADIUS - EPS, 0.0)) and near.available)

	var far := DodgeEngine.new()
	far.begin_landing(Vector2.ZERO, 0.40)
	_ck("far landing stays unavailable", not far.update_window(0.40, Vector2(
		DodgeEngine.DANGER_RADIUS + EPS, 0.0)) and not far.available)

	var on_time := DodgeEngine.new()
	on_time.begin_landing(Vector2.ZERO, 0.0)
	_ck("on-time landing exposes dodge", on_time.update_window(0.0, Vector2.ZERO))

	var late := DodgeEngine.new()
	late.begin_landing(Vector2.ZERO, -DodgeEngine.LATE_GRACE_T - EPS)
	_ck("late window closes", not late.update_window(
		-DodgeEngine.LATE_GRACE_T - EPS, Vector2.ZERO) and not late.available)

	var boundary := DodgeEngine.new()
	boundary.begin_landing(Vector2.ZERO, -DodgeEngine.LATE_GRACE_T)
	_ck("landing grace includes exact boundary", boundary.update_window(
		-DodgeEngine.LATE_GRACE_T, Vector2.ZERO))

func _case_threat_proximity() -> void:
	var engine := DodgeEngine.new()
	engine.begin_landing(Vector2.ZERO, 0.40)
	engine.set_threat_position(Vector2(DodgeEngine.DANGER_RADIUS + EPS, 0.0))
	_ck("far bunny keeps dodge closed", not engine.update_window(0.40, Vector2.ZERO)
		and not engine.available)
	engine.set_threat_position(Vector2(DodgeEngine.DANGER_RADIUS - EPS, 0.0))
	_ck("near bunny exposes dodge", engine.update_window(0.40, Vector2.ZERO)
		and engine.available)

func _case_gesture_shapes() -> void:
	var right := _new_landing()
	_ck("right swipe accepted", right.try_swipe(Vector2(100.0, 200.0),
		Vector2(220.0, 200.0)))
	_ck("right movement points right", right.motion_dir == Vector2.RIGHT)

	var left := _new_landing()
	_ck("left swipe accepted", left.try_swipe(Vector2(220.0, 200.0),
		Vector2(100.0, 200.0)))
	_ck("left movement points left", left.motion_dir == Vector2.LEFT)

	var slow := _new_landing()
	_ck("slow deliberate horizontal swipe accepted", _valid_horizontal(slow, 1.0,
		DodgeEngine.SWIPE_MIN_PX))

	var short := _new_landing()
	_ck("short swipe rejected", not _valid_horizontal(short, 1.0,
		DodgeEngine.SWIPE_MIN_PX - EPS))

	var vertical := _new_landing()
	_ck("vertical swipe rejected", not vertical.try_swipe(Vector2.ZERO,
		Vector2(0.0, DodgeEngine.SWIPE_MIN_PX + 40.0)))

	var diagonal := _new_landing()
	_ck("diagonal swipe rejected", not diagonal.try_swipe(Vector2.ZERO,
		Vector2(120.0, 81.0)))

	var exact_dominance := _new_landing()
	_ck("horizontal dominance boundary accepted", exact_dominance.try_swipe(
		Vector2.ZERO, Vector2(120.0, 80.0)))

	var unavailable := DodgeEngine.new()
	unavailable.begin_landing(Vector2.ZERO, 2.0)
	unavailable.update_window(2.0, Vector2.ZERO)
	_ck("valid swipe outside timing rejected", not _valid_horizontal(unavailable))

	var once := _new_landing()
	var first: bool = _valid_horizontal(once)
	var second: bool = _valid_horizontal(once, -1.0)
	_ck("one dodge per landing", first and not second and once.accepted_count == 1
		and once.rejected_count >= 1 and once.accepted)
	_ck("accepted dodge closes availability", not once.available)

func _integrate_motion(engine: DodgeEngine, hz: float) -> Vector2:
	var total := Vector2.ZERO
	var elapsed := 0.0
	var dt: float = 1.0 / hz
	while elapsed < DodgeEngine.DODGE_T - EPS:
		var step: float = minf(dt, DodgeEngine.DODGE_T - elapsed)
		total += engine.consume_motion(step)
		elapsed += step
	return total

func _case_landing_frame() -> void:
	var exact := _new_landing(Vector2(12.0, -3.0), 0.0, Vector2(12.0, -3.0))
	var before_accepted: int = exact.accepted_count
	var before_rejected: int = exact.rejected_count
	var dodged: bool = _valid_horizontal(exact, -1.0)
	var exact_hit: bool = exact.resolve_landing(Vector2(12.0, -3.0))
	var repeated: bool = exact.resolve_landing(Vector2(12.0, -3.0))
	_ck("exact landing-frame swipe is accepted", dodged)
	_ck("exact landing-frame dodge avoids contact", not exact_hit and not repeated)
	_ck("landing resolution does not alter gesture counters",
		exact.accepted_count == before_accepted + 1
		and exact.rejected_count == before_rejected)

	var missed := _new_landing(Vector2.ZERO, 0.0, Vector2.ZERO)
	var miss_hit: bool = missed.resolve_landing(Vector2.ZERO)
	var miss_again: bool = missed.resolve_landing(Vector2.ZERO)
	_ck("unavoided landing resolves once", miss_hit and not miss_again)
	_ck("landing miss is harmless engine state", missed.accepted_count == 0
		and missed.rejected_count == 0 and missed.landing_resolved)

	var outside := _new_landing(Vector2.ZERO, 0.0, Vector2(DodgeEngine.LANDING_HIT_RADIUS + EPS, 0.0))
	_ck("landing outside hit radius is safe", not outside.resolve_landing(Vector2(
		DodgeEngine.LANDING_HIT_RADIUS + EPS, 0.0)))

func _case_eased_rate_invariance() -> void:
	var baselines: Array[Vector2] = []
	for hz: float in SAMPLE_HZ:
		var engine := _new_landing()
		_valid_horizontal(engine)
		var displacement: Vector2 = _integrate_motion(engine, hz)
		baselines.append(displacement)
		_ck("eased displacement finite at %.0fHz" % hz,
			is_finite(displacement.x) and is_finite(displacement.y))
		_ck("eased displacement bounded at %.0fHz" % hz,
			displacement.length() <= DodgeEngine.DODGE_DISTANCE + EPS)
		_ck("eased displacement reaches full distance at %.0fHz" % hz,
			is_equal_approx(displacement.x, DodgeEngine.DODGE_DISTANCE))
	for i in range(1, baselines.size()):
		_ck("rate invariant between %.0fHz and %.0fHz" % [SAMPLE_HZ[i - 1], SAMPLE_HZ[i]],
			baselines[i].distance_to(baselines[0]) <= EPS)

static func _clamp_octagon(point: Vector2) -> Vector2:
	var result := point
	for _pass in range(2):
		for side in range(8):
			var normal := Vector2(cos(float(side) * PI / 4.0),
				sin(float(side) * PI / 4.0))
			var over: float = result.dot(normal) - EDGE_APOTHEM
			if over > 0.0:
				result -= normal * over
	return result

static func _inside_octagon(point: Vector2) -> bool:
	for side in range(8):
		var normal := Vector2(cos(float(side) * PI / 4.0),
			sin(float(side) * PI / 4.0))
		if point.dot(normal) > EDGE_APOTHEM + EPS:
			return false
	return true

func _case_arena_edge_clamp() -> void:
	var right_edge := _new_landing()
	_valid_horizontal(right_edge, 1.0)
	var right_raw := Vector2(EDGE_APOTHEM - 0.1, 0.0) + _integrate_motion(
		right_edge, 60.0)
	var right_clamped := _clamp_octagon(right_raw)
	_ck("right arena edge clamps dodge", right_raw.x > EDGE_APOTHEM
		and _inside_octagon(right_clamped))

	var left_edge := _new_landing()
	_valid_horizontal(left_edge, -1.0)
	var left_raw := Vector2(-EDGE_APOTHEM + 0.1, 0.0) + _integrate_motion(
		left_edge, 60.0)
	var left_clamped := _clamp_octagon(left_raw)
	_ck("left arena edge clamps dodge", left_raw.x < -EDGE_APOTHEM
		and _inside_octagon(left_clamped))

	var rng := RandomNumberGenerator.new()
	rng.seed = 20260830
	var all_inside := true
	for _i in range(256):
		var angle: float = rng.randf_range(0.0, TAU)
		var point := Vector2(cos(angle), sin(angle)) * (EDGE_APOTHEM + 3.0)
		var clamped := _clamp_octagon(point)
		all_inside = all_inside and _inside_octagon(clamped)
	_ck("octagon clamp remains inside for seeded edge points", all_inside)

func _case_seeded_stress() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 0xD0D6E
	var checks := 0
	var accepted_total := 0
	var rejected_total := 0
	var finite := true
	for i in range(ITERATIONS):
		var landing := Vector2(rng.randf_range(-30.0, 30.0),
			rng.randf_range(-30.0, 30.0))
		var player := landing + Vector2(rng.randf_range(-16.0, 16.0),
			rng.randf_range(-16.0, 16.0))
		var eta: float = rng.randf_range(-0.40, 1.40)
		var engine := DodgeEngine.new()
		engine.begin_landing(landing, eta)
		var available_now: bool = engine.update_window(eta, player)
		var expected_available: bool = eta <= DodgeEngine.READY_LEAD_T \
			and eta >= -DodgeEngine.LATE_GRACE_T \
			and player.distance_to(landing) <= DodgeEngine.DANGER_RADIUS
		if available_now != expected_available:
			failures += 1
		var shape := i % 4
		var length: float = DodgeEngine.SWIPE_MIN_PX + rng.randf_range(0.0, 260.0)
		var stroke_to := Vector2(length if rng.randf() >= 0.5 else -length, 0.0)
		match shape:
			1:
				stroke_to = Vector2(DodgeEngine.SWIPE_MIN_PX - EPS, 0.0)
			2:
				stroke_to = Vector2(0.0, length)
			3:
				stroke_to = Vector2(120.0, 81.0)
		var expected_valid_shape: bool = shape == 0
		var accepted: bool = engine.try_swipe(Vector2.ZERO, stroke_to)
		var expected_accepted: bool = expected_available and expected_valid_shape
		if accepted != expected_accepted:
			failures += 1
		if accepted:
			accepted_total += 1
			var movement := _integrate_motion(engine, SAMPLE_HZ[i % SAMPLE_HZ.size()])
			finite = finite and is_finite(movement.x) and is_finite(movement.y) \
				and movement.length() <= DodgeEngine.DODGE_DISTANCE + EPS
			_ck_stress_finite(engine, finite)
		else:
			rejected_total += 1
		checks += 1
	var totals_ok: bool = accepted_total > 0 and rejected_total > 0 \
		and accepted_total + rejected_total == ITERATIONS
	_ck("%d seeded timing/direction iterations agree" % checks, totals_ok and failures == 0)
	_ck("seeded stress values stay finite and bounded", finite)

func _ck_stress_finite(engine: DodgeEngine, ok: bool) -> void:
	# Keep the thousands-iteration loop quiet while still checking every sample.
	if not ok:
		return
	if not is_finite(engine.motion_progress) or not is_finite(engine.motion_t):
		failures += 1
	if engine.motion_progress < -EPS or engine.motion_progress > 1.0 + EPS:
		failures += 1

func _case_zero_input() -> void:
	var engine := DodgeEngine.new()
	engine.begin_landing(Vector2.ZERO, 0.0)
	engine.update_window(0.0, Vector2.ZERO)
	var total := Vector2.ZERO
	for _i in range(120):
		total += engine.consume_motion(1.0 / 60.0)
	_ck("zero input never accepts a dodge", engine.accepted_count == 0
		and not engine.accepted and total == Vector2.ZERO)
	_ck("zero input does not resolve as a dodge", engine.resolve_landing(Vector2.ZERO)
		and engine.accepted_count == 0)

	var cancelled := _new_landing()
	_valid_horizontal(cancelled)
	var partial: Vector2 = cancelled.consume_motion(DodgeEngine.DODGE_T * 0.25)
	cancelled.cancel_motion()
	var stale: Vector2 = cancelled.consume_motion(DodgeEngine.DODGE_T)
	_ck("focus cancellation discards remaining dash motion",
		partial.length() > 0.0 and stale == Vector2.ZERO and cancelled.accepted)
