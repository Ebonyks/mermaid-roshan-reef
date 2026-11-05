extends SceneTree
## Independent numbers-only check of OperaBoxingContact.sweep.
## Reference: the gap g(t) = |p + v t| - (r + dr t) is convex in t, so the
## earliest contact is found by a golden-section minimum plus bisection,
## without using the engine's quadratic formula. Evaluation only; not shipped.

const Contact := preload("res://scripts/opera_boxing_contact.gd")
const PHI := 0.6180339887498949

var rng := RandomNumberGenerator.new()


func _initialize() -> void:
	call_deferred("_run")


func _gap(px: float, py: float, vx: float, vy: float, r: float, dr: float, t: float) -> float:
	var x := px + vx * t
	var y := py + vy * t
	return sqrt(x * x + y * y) - (r + dr * t)


## Returns [earliest_t or -1.0, minimum gap over [0, 1], relative path length].
func _reference(a0: Vector2, a1: Vector2, ar0: float, ar1: float,
		b0: Vector2, b1: Vector2, br0: float, br1: float) -> Array:
	var px := float(a0.x) - float(b0.x)
	var py := float(a0.y) - float(b0.y)
	var vx := (float(a1.x) - float(a0.x)) - (float(b1.x) - float(b0.x))
	var vy := (float(a1.y) - float(a0.y)) - (float(b1.y) - float(b0.y))
	var r := ar0 + br0
	var dr := ar1 + br1 - r
	var travel := sqrt(vx * vx + vy * vy) + absf(dr)
	var g0 := _gap(px, py, vx, vy, r, dr, 0.0)
	if g0 <= 0.0:
		return [0.0, g0, travel]
	var lo := 0.0
	var hi := 1.0
	var x1 := hi - PHI * (hi - lo)
	var x2 := lo + PHI * (hi - lo)
	var f1 := _gap(px, py, vx, vy, r, dr, x1)
	var f2 := _gap(px, py, vx, vy, r, dr, x2)
	for i in range(90):
		if f1 <= f2:
			hi = x2
			x2 = x1
			f2 = f1
			x1 = hi - PHI * (hi - lo)
			f1 = _gap(px, py, vx, vy, r, dr, x1)
		else:
			lo = x1
			x1 = x2
			f1 = f2
			x2 = lo + PHI * (hi - lo)
			f2 = _gap(px, py, vx, vy, r, dr, x2)
	var tmin := 0.5 * (lo + hi)
	var gmin := _gap(px, py, vx, vy, r, dr, tmin)
	var g1 := _gap(px, py, vx, vy, r, dr, 1.0)
	if g1 < gmin:
		gmin = g1
		tmin = 1.0
	if gmin > 0.0:
		return [-1.0, gmin, travel]
	var low := 0.0
	var high := tmin
	for i in range(100):
		var mid := 0.5 * (low + high)
		if _gap(px, py, vx, vy, r, dr, mid) > 0.0:
			low = mid
		else:
			high = mid
	return [high, gmin, travel]


func _new_stats() -> Dictionary:
	return {"cases": 0, "ref_contacts": 0, "engine_contacts": 0, "missed": 0, "false": 0,
		"ambiguous": 0, "max_late_px": 0.0, "max_early_px": 0.0, "max_gap_at_engine_t": 0.0,
		"late_over_half_px": 0, "worst": ""}


## Tolerance: cases whose true minimum gap lies within `tol` px of zero are
## tangency-ambiguous at single-precision Vector2 inputs and are only counted.
func _compare(stats: Dictionary, a0: Vector2, a1: Vector2, ar0: float, ar1: float,
		b0: Vector2, b1: Vector2, br0: float, br1: float, tol: float) -> void:
	var ref := _reference(a0, a1, ar0, ar1, b0, b1, br0, br1)
	var t_ref := float(ref[0])
	var gmin := float(ref[1])
	var travel := float(ref[2])
	var t_eng := Contact.sweep(a0, a1, ar0, ar1, b0, b1, br0, br1)
	stats["cases"] += 1
	if t_ref >= 0.0:
		stats["ref_contacts"] += 1
	if t_eng >= 0.0:
		stats["engine_contacts"] += 1
	if absf(gmin) <= tol:
		stats["ambiguous"] += 1
		return
	if t_ref >= 0.0 and t_eng < 0.0:
		stats["missed"] += 1
		if String(stats["worst"]).is_empty():
			stats["worst"] = "MISS gmin=%f a0=%s a1=%s ar=%f,%f b0=%s b1=%s br=%f,%f" % [gmin, a0, a1, ar0, ar1, b0, b1, br0, br1]
		return
	if t_ref < 0.0 and t_eng >= 0.0:
		stats["false"] += 1
		if String(stats["worst"]).is_empty():
			stats["worst"] = "FALSE gmin=%f a0=%s a1=%s ar=%f,%f b0=%s b1=%s br=%f,%f t=%f" % [gmin, a0, a1, ar0, ar1, b0, b1, br0, br1, t_eng]
		return
	if t_ref < 0.0:
		return
	var px := float(a0.x) - float(b0.x)
	var py := float(a0.y) - float(b0.y)
	var vx := (float(a1.x) - float(a0.x)) - (float(b1.x) - float(b0.x))
	var vy := (float(a1.y) - float(a0.y)) - (float(b1.y) - float(b0.y))
	var r := ar0 + br0
	var dr := ar1 + br1 - r
	if t_ref > 0.0:
		var gap_at := absf(_gap(px, py, vx, vy, r, dr, t_eng))
		stats["max_gap_at_engine_t"] = maxf(float(stats["max_gap_at_engine_t"]), gap_at)
	var late := (t_eng - t_ref) * travel
	if late > 0.0:
		stats["max_late_px"] = maxf(float(stats["max_late_px"]), late)
		if late > 0.5:
			stats["late_over_half_px"] += 1
	else:
		stats["max_early_px"] = maxf(float(stats["max_early_px"]), -late)


func _rv(span_x: float, span_y: float) -> Vector2:
	return Vector2(rng.randf_range(-span_x, span_x), rng.randf_range(-span_y, span_y))


func _print(label: String, s: Dictionary) -> void:
	print("GEOM|%s|cases=%d|ref_contacts=%d|engine_contacts=%d|missed=%d|false=%d|ambiguous=%d|max_late_px=%.9f|max_early_px=%.9f|max_gap_at_engine_t=%.9f|late_over_half_px=%d" % [
		label, s["cases"], s["ref_contacts"], s["engine_contacts"], s["missed"], s["false"],
		s["ambiguous"], s["max_late_px"], s["max_early_px"], s["max_gap_at_engine_t"], s["late_over_half_px"]])
	if not String(s["worst"]).is_empty():
		print("GEOM|%s|first_disagreement|%s" % [label, s["worst"]])


func _run() -> void:
	rng.seed = 0x5EED2026
	var tol := 0.01

	var s := _new_stats()
	for i in range(100000):
		_compare(s, _rv(1600, 900), _rv(1600, 900), rng.randf_range(0, 200), rng.randf_range(0, 200),
			_rv(1600, 900), _rv(1600, 900), rng.randf_range(0, 200), rng.randf_range(0, 200), tol)
	_print("uniform_wide", s)

	# Game scale: 1280x720 stage, glove radius 52-75, fist radius 42-56,
	# per-sample motion up to a 3000 px/s swat at 15 Hz (200 px).
	s = _new_stats()
	for i in range(100000):
		var a0 := Vector2(rng.randf_range(0, 1280), rng.randf_range(0, 720))
		var b0 := Vector2(rng.randf_range(0, 1280), rng.randf_range(0, 720))
		var a1 := a0 + _rv(200, 200)
		var b1 := b0 + _rv(40, 40)
		_compare(s, a0, a1, rng.randf_range(52, 75), rng.randf_range(52, 75),
			b0, b1, rng.randf_range(42, 56), rng.randf_range(42, 56), tol)
	_print("game_scale", s)

	# Constructed near-tangent cases: shift the second disc so the true minimum
	# gap is +/- delta px, for delta in {0.02, 0.1, 1, 5}.
	for delta: float in [0.02, 0.1, 1.0, 5.0]:
		s = _new_stats()
		for i in range(20000):
			var a0 := Vector2(rng.randf_range(0, 1280), rng.randf_range(0, 720))
			var a1 := a0 + _rv(300, 300)
			var b0 := Vector2(rng.randf_range(0, 1280), rng.randf_range(0, 720))
			var b1 := b0 + _rv(40, 40)
			var ar := rng.randf_range(52, 75)
			var br := rng.randf_range(42, 56)
			var ref := _reference(a0, a1, ar, ar, b0, b1, br, br)
			var gmin := float(ref[1])
			# Move b along the direction from b to a at the minimum by (gmin - target).
			var target := delta if i % 2 == 0 else -delta
			var tm := 0.0
			var best := INF
			for k in range(2001):
				var tt := float(k) / 2000.0
				var d := a0.lerp(a1, tt).distance_to(b0.lerp(b1, tt))
				if d < best:
					best = d
					tm = tt
			var dir := (a0.lerp(a1, tm) - b0.lerp(b1, tm))
			if dir.length() < 0.001:
				continue
			var shift := dir.normalized() * (gmin - target)
			_compare(s, a0, a1, ar, ar, b0 + shift, b1 + shift, br, br, delta * 0.5)
		_print("near_tangent_%s" % str(delta), s)

	# Radii growing faster than the discs close (quadratic opens downward).
	s = _new_stats()
	for i in range(20000):
		var a0 := _rv(400, 400)
		var b0 := a0 + _rv(400, 400)
		_compare(s, a0, a0 + _rv(20, 20), rng.randf_range(0, 30), rng.randf_range(100, 400),
			b0, b0 + _rv(20, 20), rng.randf_range(0, 30), rng.randf_range(0, 200), tol)
	_print("radius_dominated", s)

	# Zero relative motion with changing radii (linear branch).
	s = _new_stats()
	for i in range(20000):
		var a0 := _rv(600, 600)
		var move := _rv(300, 300)
		var b0 := a0 + _rv(300, 300)
		_compare(s, a0, a0 + move, rng.randf_range(0, 120), rng.randf_range(0, 120),
			b0, b0 + move, rng.randf_range(0, 120), rng.randf_range(0, 120), tol)
	_print("same_velocity", s)

	# Long sweeps: precision stress for small padding over long travel.
	s = _new_stats()
	for i in range(20000):
		var a0 := _rv(50000, 50000)
		var a1 := _rv(50000, 50000)
		var b0 := a0.lerp(a1, rng.randf()) + _rv(150, 150)
		_compare(s, a0, a1, rng.randf_range(20, 75), rng.randf_range(20, 75),
			b0, b0 + _rv(5, 5), rng.randf_range(20, 56), rng.randf_range(20, 56), 0.05)
	_print("long_sweeps", s)

	# Invalid inputs must never report contact.
	var invalid_ok := 0
	var invalid_cases: Array = [
		[Vector2(NAN, 0), Vector2.ZERO, 10.0, 10.0, Vector2.ZERO, Vector2.ZERO, 10.0, 10.0],
		[Vector2.ZERO, Vector2(INF, 0), 10.0, 10.0, Vector2.ZERO, Vector2.ZERO, 10.0, 10.0],
		[Vector2.ZERO, Vector2.ZERO, NAN, 10.0, Vector2.ZERO, Vector2.ZERO, 10.0, 10.0],
		[Vector2.ZERO, Vector2.ZERO, 10.0, -0.001, Vector2.ZERO, Vector2.ZERO, 10.0, 10.0],
		[Vector2.ZERO, Vector2.ZERO, 10.0, 10.0, Vector2(0, -INF), Vector2.ZERO, 10.0, 10.0],
	]
	for c: Array in invalid_cases:
		if Contact.sweep(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]) < 0.0:
			invalid_ok += 1
	print("GEOM|invalid_inputs|rejected=%d/%d" % [invalid_ok, invalid_cases.size()])

	# Cost per call on this desktop (for the mobile budget estimate only).
	var start := Time.get_ticks_usec()
	var sink := 0.0
	for i in range(200000):
		sink += Contact.sweep(Vector2(i % 1280, 300), Vector2(640, 400), 60, 70,
			Vector2(600, 144), Vector2(610, 160), 45, 46)
	var elapsed := float(Time.get_ticks_usec() - start)
	print("GEOM|cost|calls=200000|usec_per_call=%.3f|sink=%f" % [elapsed / 200000.0, sink])
	print("GEOM|DONE")
	quit(0)
