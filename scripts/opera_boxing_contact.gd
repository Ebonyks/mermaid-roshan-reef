class_name OperaBoxingContact
extends RefCounted
## Continuous contact for two linearly moving padded discs. Radii may change
## linearly too. Returns earliest normalized contact time, or -1 for no contact.
## Pure geometry: no input, scene, progress, timing, or save ownership.

static func sweep(a0: Vector2, a1: Vector2, ar0: float, ar1: float,
		b0: Vector2, b1: Vector2, br0: float, br1: float) -> float:
	if not a0.is_finite() or not a1.is_finite() \
			or not b0.is_finite() or not b1.is_finite():
		return -1.0
	if not is_finite(ar0) or not is_finite(ar1) \
			or not is_finite(br0) or not is_finite(br1) \
			or minf(minf(ar0, ar1), minf(br0, br1)) < 0.0:
		return -1.0
	# Vector2 dot/length operations use single-precision engine reals. Build
	# coefficients from scalar doubles so long sweeps against small padding
	# retain a precise first-contact time, especially near tangency.
	var px: float = float(a0.x) - float(b0.x)
	var py: float = float(a0.y) - float(b0.y)
	var vx: float = (float(a1.x) - float(a0.x)) - (float(b1.x) - float(b0.x))
	var vy: float = (float(a1.y) - float(a0.y)) - (float(b1.y) - float(b0.y))
	var r := ar0 + br0
	var dr := ar1 + br1 - r
	var c := px * px + py * py - r * r
	if c <= 0.0:
		return 0.0
	var a := vx * vx + vy * vy - dr * dr
	var b := 2.0 * (px * vx + py * vy - r * dr)
	if absf(a) < 0.0000001:
		if b >= 0.0:
			return -1.0
		var linear := -c / b
		return linear if linear >= 0.0 and linear <= 1.0 else -1.0
	var discriminant := b * b - 4.0 * a * c
	if discriminant < 0.0:
		return -1.0
	# Stable quadratic form avoids cancellation on long, fast sweeps.
	var q := -0.5 * (b + (1.0 if b >= 0.0 else -1.0) * sqrt(discriminant))
	var first := q / a
	var second := c / q if absf(q) > 0.0000001 else first
	if first > second:
		var swap := first
		first = second
		second = swap
	if first >= 0.0 and first <= 1.0:
		return first
	if second >= 0.0 and second <= 1.0:
		return second
	return -1.0
