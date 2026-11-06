class_name BubbleDuelBrain
extends RefCounted
## Rule-based competitors: observe, evade threats, gain height, then intercept.
## They use the same discrete flap and equipment inputs as the human controls.


static func opponent(me: BubbleDuelFighter, fighters: Array[BubbleDuelFighter]) -> BubbleDuelFighter:
	var selected: BubbleDuelFighter = null
	var best: float = INF
	for other: BubbleDuelFighter in fighters:
		if other == me or other.team == me.team or other.lost or other.swallowed:
			continue
		var distance: float = absf(BubbleDuelMotion.wrapped_dx(other.position.x - me.position.x)) \
			+ absf(other.position.y - me.position.y) * 0.35
		if other.bubbles <= 0:
			distance += 500.0
		if distance < best:
			selected = other
			best = distance
	return selected


static func decide(me: BubbleDuelFighter, fighters: Array[BubbleDuelFighter], hazard_x: float = INF) -> void:
	me.kick_edge = false
	me.power_edge = false
	me.power_held = false
	var foe: BubbleDuelFighter = opponent(me, fighters)
	if foe == null or me.lost or me.swallowed:
		return
	me.history[me.history_cursor] = foe.position
	me.history_cursor = (me.history_cursor + 1) % 10
	me.history_count = mini(10, me.history_count + 1)
	if not _roll(me, me.cpu_reflex * 1.25):
		return
	# Source-style evasion otherwise camps the ceiling indefinitely in team bouts.
	# Release flaps through a real falling arc; do not move or slow the fighter.
	if me.position.y < 55.0: me.ceiling_release = true
	if me.position.y > 100.0: me.ceiling_release = false
	if me.ceiling_release: return
	var dx: float = BubbleDuelMotion.wrapped_dx(foe.position.x - me.position.x)
	var toward: float = signf(dx) if absf(dx) > 0.001 else 1.0
	var oldest: Vector2 = me.history[me.history_cursor if me.history_count == 10 else 0]
	var prediction: Vector2 = Vector2(BubbleDuelMotion.wrapped_dx(foe.position.x - oldest.x),
		foe.position.y - oldest.y) / float(maxi(1, me.history_count))
	var skill: float = me.cpu_skill
	var near_cap: bool = me.velocity.x * toward > me.max_vx * 0.85
	if me.position.y + me.velocity.y * 18.0 > 250.0 \
			or (is_finite(hazard_x) and absf(BubbleDuelMotion.wrapped_dx(hazard_x - me.position.x)) < 90.0 and me.position.y > 210.0):
		if _roll(me, 40.0 + skill * 0.5):
			_flap(me, 0.0)
		return
	var future_y: float = foe.position.y + prediction.y * 12.0 - me.position.y - me.velocity.y * 12.0
	var future_x: float = BubbleDuelMotion.wrapped_dx(foe.position.x + prediction.x * 12.0 - me.position.x - me.velocity.x * 12.0)
	if future_y < -8.0 and absf(future_x) < 40.0 and _roll(me, skill * 0.9):
		_flap(me, -toward)
		return
	if me.position.y >= foe.position.y - 12.0:
		if me.velocity.y > -1.5 and _roll(me, 30.0 + skill * 0.5):
			_flap(me, 0.0 if near_cap else toward)
		return
	if absf(dx) > 14.0 and not near_cap and _roll(me, skill * 0.6):
		if foe.position.y - me.position.y < 70.0 or _roll(me, 30.0):
			_flap(me, toward)
	if me.gear not in ["classic", "tidewing"] and absf(dx) < 120.0 and _roll(me, skill / 8.0):
		me.power_edge = true
	if me.gear == "moonpearl":
		me.power_held = me.position.y > 200.0


static func _roll(me: BubbleDuelFighter, percent: float) -> bool:
	return me.rng.randf() * 100.0 < percent


static func _flap(me: BubbleDuelFighter, direction: float) -> void:
	me.direction = direction
	me.kick_edge = true
