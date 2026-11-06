class_name BubbleDuelArena
extends RefCounted
## Shared original-style bout engine. The overlay owns this transient world.
## Human, CPU and cooperative competitors all use the same motion/combat path.

const Fighter := preload("res://scripts/bubble_duel_fighter.gd")
const Motion := preload("res://scripts/bubble_duel_motion.gd")
const Brain := preload("res://scripts/bubble_duel_brain.gd")
const MAX_FIGHTERS: int = 6
const MAX_HITS: int = 36
const SIDES: Array[int] = [-1, 1]
const SPAWNS: Array[Vector2] = [Vector2(90, 300), Vector2(310, 300),
	Vector2(160, 300), Vector2(250, 300), Vector2(45, 300), Vector2(355, 300)]

var prepare_geometry: Callable
var motion: BubbleDuelMotion = Motion.new()
var fighters: Array[BubbleDuelFighter] = []
var events: Array[Dictionary] = []
var event_count: int = 0
var competitive: bool = false
var exchanged_motion: float = 0.0
var shots: Array[Dictionary] = []
var frame: int = 0
var stage: int = 0
var drift: float = 0.5
var started: bool = false
var finished: bool = false
var winner: int = -2
var paused: bool = false
var round_limit: int = 0
var timed_draw: bool = false
var seed_value: int = 1
var pops: int = 0
var bumps: int = 0
var contacts := PackedByteArray()
var hit_attack := PackedInt32Array()
var hit_target := PackedInt32Array()
var hit_side := PackedInt32Array()
var hit_count: int = 0


func _init() -> void:
	for index: int in range(48):
		events.append({"kind": "", "position": Vector2.ZERO, "actor": -1})
	for index: int in range(24):
		shots.append({"owner": 0, "position": Vector2.ZERO, "previous": Vector2.ZERO, "vx": 0.0, "life": 0})
	contacts.resize(MAX_FIGHTERS * MAX_FIGHTERS)
	hit_attack.resize(MAX_HITS)
	hit_target.resize(MAX_HITS)
	hit_side.resize(MAX_HITS)


func reset(stage_index: int = 0, seed_number: int = 1) -> void:
	fighters.clear()
	event_count = 0
	competitive = false
	exchanged_motion = 0.0
	for shot: Dictionary in shots:
		shot["life"] = 0
	contacts.fill(0)
	frame = 0
	stage = clampi(stage_index, 0, 3)
	drift = 0.5
	started = false
	finished = false
	winner = -2
	paused = false
	round_limit = 0
	timed_draw = false
	seed_value = seed_number
	pops = 0
	bumps = 0


func add_human(profile: Dictionary, player: int, team: int, spares: int = 4, forgiving: bool = false) -> BubbleDuelFighter:
	var fighter: BubbleDuelFighter = _add(profile, team, spares)
	if fighter != null:
		fighter.human = player
		fighter.unlimited_rescues = forgiving
	return fighter


func add_cpu(profile: Dictionary, skill: float, reflex: float, rank: int,
		team: int = 1, spares: int = 1) -> BubbleDuelFighter:
	var fighter: BubbleDuelFighter = _add(profile, team, spares)
	if fighter != null:
		fighter.cpu_skill = skill
		fighter.cpu_reflex = reflex
		fighter.max_vx = 2.0 + 0.04 * float(clampi(rank, 1, 120))
		fighter.max_vy = 2.0 + 0.03 * float(clampi(rank, 1, 120))
	return fighter


func _add(profile: Dictionary, team: int, spares: int) -> BubbleDuelFighter:
	if fighters.size() >= MAX_FIGHTERS:
		return null
	var fighter: BubbleDuelFighter = Fighter.new()
	fighter.slot = fighters.size()
	fighter.profile = profile.duplicate(true)
	fighter.team = team
	fighter.spares = maxi(0, spares)
	fighter.gear = String(profile.get("gear", "classic"))
	fighter.facing = 1.0 if fighter.slot % 2 == 0 else -1.0
	fighter.rng.seed = seed_value * 7919 + fighter.slot * 104729 + 17
	fighter.reset(SPAWNS[fighter.slot])
	for other: BubbleDuelFighter in fighters:
		if other.team != team:
			competitive = true
	fighters.append(fighter)
	return fighter


func queue_kick(player: int, axis: float) -> bool:
	var fighter: BubbleDuelFighter = human(player)
	if fighter == null or fighter.lost or paused or finished:
		return false
	fighter.direction = clampf(axis, -1.0, 1.0)
	fighter.kick_direction = fighter.direction
	fighter.kick_edge = true
	return true


func set_direction(player: int, axis: float) -> void:
	var fighter: BubbleDuelFighter = human(player)
	if fighter != null:
		fighter.direction = clampf(axis, -1.0, 1.0)


func queue_power(player: int, held: bool, edge: bool = true) -> bool:
	var fighter: BubbleDuelFighter = human(player)
	if fighter == null or fighter.lost or paused or finished:
		return false
	fighter.power_held = held
	fighter.power_edge = fighter.power_edge or edge
	return true


func human(player: int) -> BubbleDuelFighter:
	for fighter: BubbleDuelFighter in fighters:
		if fighter.human == player:
			return fighter
	return null


func clear_controls() -> void:
	for fighter: BubbleDuelFighter in fighters:
		fighter.clear_controls()


func step() -> void:
	event_count = 0
	if paused or finished:
		return
	if not started:
		for fighter: BubbleDuelFighter in fighters:
			if fighter.human >= 0 and fighter.kick_edge:
				started = true
		if not started:
			return
	frame += 1
	for fighter: BubbleDuelFighter in fighters:
		fighter.previous_fin = _fin(fighter)
		fighter.previous_sway = fighter.sway
		fighter.previous_facing = fighter.facing
		if fighter.human < 0:
			Brain.decide(fighter, fighters)
	for fighter: BubbleDuelFighter in fighters:
		if fighter.lost:
			continue
		var muted: bool = fighter.held > 0
		if muted:
			fighter.held -= 1
			fighter.direction = 0.0
			fighter.kick_edge = false
			fighter.power_edge = false
			fighter.power_held = false
		if fighter.direction != 0.0:
			fighter.facing = signf(fighter.direction)
		if fighter.kick_edge and motion.kick(fighter, fighter.kick_direction if fighter.human >= 0 else fighter.direction):
			fighter.consumed_inputs += 1
			_event("kick", fighter.position, fighter.slot)
		_apply_power(fighter)
		fighter.kick_edge = false
		fighter.power_edge = false
		var before_bounce: int = fighter.ceiling_bounces
		var before_rescue: int = fighter.rescues
		motion.integrate(fighter, drift, stage)
		if fighter.ceiling_bounces > before_bounce:
			_event("bonk", fighter.position, fighter.slot)
		if fighter.rescues > before_rescue:
			_event("rescue", fighter.position, fighter.slot)
	if prepare_geometry.is_valid():
		for fighter: BubbleDuelFighter in fighters:
			prepare_geometry.call(fighter, frame)
	drift = maxf(0.0, drift - 0.002)
	hit_count = 0
	for a: int in range(fighters.size()):
		for b: int in range(fighters.size()):
			if a != b and fighters[a].team != fighters[b].team:
				_check_pop(a, b)
	_step_shots()
	for index: int in range(hit_count):
		_pop(hit_attack[index], hit_target[index], hit_side[index])
	for a: int in range(fighters.size()):
		for b: int in range(a + 1, fighters.size()):
			var touching: bool = _body_touch(fighters[a], fighters[b])
			var key: int = a * MAX_FIGHTERS + b
			if touching and contacts[key] == 0:
				_bump(fighters[a], fighters[b])
				_event("bump", (fighters[a].position + fighters[b].position) * 0.5, a)
			contacts[key] = 1 if touching else 0
	_resolve_finish()
	if not finished and round_limit > 0 and frame >= round_limit:
		finished = true
		winner = -1
		timed_draw = true
		_event("finish", Vector2.ZERO, -1)


func _apply_power(fighter: BubbleDuelFighter) -> void:
	if fighter.gear == "tidewing":
		fighter.auto_timer = maxi(0, fighter.auto_timer - 1)
		if fighter.velocity.y > 1.8 and fighter.auto_timer == 0 and fighter.bubbles > 0:
			if motion.kick(fighter, fighter.direction):
				fighter.auto_timer = 12
		return
	if fighter.gear == "moonpearl":
		if (fighter.power_held or fighter.power_edge) and fighter.charge >= 2.0 and fighter.bubbles > 0:
			if not fighter.hover_last:
				fighter.charms_used += 1
				fighter.consumed_inputs += 1
			fighter.hover_last = true
			fighter.floating = true
			fighter.velocity.y *= 0.85
			fighter.charge -= 2.0
		else:
			fighter.hover_last = false
		return
	if not fighter.power_edge or fighter.held > 0 or fighter.swallowed:
		return
	var cost: float = 0.0
	match fighter.gear:
		"swiftconch": cost = 40.0
		"rainbow": cost = 50.0
		"kelp": cost = 60.0
		"lullaby": cost = 70.0
		"squid": cost = 80.0
		_: return
	if fighter.charge < cost:
		return
	var other: BubbleDuelFighter = Brain.opponent(fighter, fighters)
	match fighter.gear:
		"swiftconch":
			fighter.velocity.x += fighter.facing * 8.0
		"rainbow":
			var free_shot: Dictionary = {}
			for shot: Dictionary in shots:
				if int(shot["life"]) <= 0:
					free_shot = shot
					break
			if free_shot.is_empty():
				return
			free_shot["owner"] = fighter.slot
			free_shot["position"] = fighter.position + Vector2(fighter.shot_tip.x * fighter.facing, fighter.shot_tip.y)
			free_shot["previous"] = free_shot["position"]
			free_shot["vx"] = fighter.facing * 6.0
			free_shot["life"] = 45
		"kelp":
			if other == null:
				return
			var offset := Vector2(Motion.wrapped_dx(fighter.position.x - other.position.x), fighter.position.y - other.position.y)
			var length: float = maxf(1.0, offset.length())
			other.velocity += Vector2(offset.x / length * 5.0, offset.y / length * 3.0)
		"lullaby":
			if other == null:
				return
			other.charge = maxf(0.0, other.charge - 100.0)
		"squid":
			if other == null or other.invincible > 0:
				return
			other.held = 40
			other.velocity *= 0.2
	fighter.charge -= cost
	fighter.charms_used += 1
	fighter.consumed_inputs += 1
	_event("power", fighter.position, fighter.slot)


func _fin(fighter: BubbleDuelFighter) -> Vector2:
	return fighter.position + Vector2(fighter.fin_center.x * fighter.facing, fighter.fin_center.y)


func bubble_position(fighter: BubbleDuelFighter, side: int, old: bool = false) -> Vector2:
	var lean: float = deg_to_rad(fighter.previous_sway if old else fighter.sway)
	var origin: Vector2 = fighter.previous if old else fighter.position
	# The supplied bubble anchor is its tether tip, not its visual center.
	return origin + Vector2(float(side) * 8.0 + sin(lean) * 22.0, -24.0 * cos(lean) - 13.0)


func bubble_radius(fighter: BubbleDuelFighter) -> float:
	return 11.0 * sqrt(fighter.inflation / 100.0)


func _side_exists(fighter: BubbleDuelFighter, side: int) -> bool:
	return fighter.bubbles > 0 and (fighter.bubbles == 2 or fighter.survivor_side == side)


func _check_pop(attacker_index: int, defender_index: int) -> void:
	var attacker: BubbleDuelFighter = fighters[attacker_index]
	var defender: BubbleDuelFighter = fighters[defender_index]
	if attacker.lost or defender.lost or attacker.swallowed or defender.swallowed \
			or attacker.bubbles <= 0 or defender.bubbles <= 0 or defender.invincible > 0:
		return
	if minf(attacker.position.y - defender.position.y, attacker.previous.y - defender.previous.y) >= -10.0:
		return
	for side: int in SIDES:
		if not _side_exists(defender, side):
			continue
		var from: Vector2 = attacker.previous_fin - bubble_position(defender, side, true)
		var to: Vector2 = _fin(attacker) - bubble_position(defender, side)
		from.x = Motion.wrapped_dx(from.x)
		to.x = from.x + Motion.wrapped_dx(to.x - from.x)
		var radius: float = bubble_radius(defender)
		var span := Vector2(radius + attacker.fin_half.x, radius + attacker.fin_half.y)
		var closest: Vector2 = Geometry2D.get_closest_point_to_segment(Vector2.ZERO, from / span, to / span)
		if closest.length_squared() <= 1.0:
			_hit(attacker_index, defender_index, side)
			return


func _hit(attacker: int, defender: int, side: int) -> void:
	if hit_count < MAX_HITS:
		hit_attack[hit_count] = attacker
		hit_target[hit_count] = defender
		hit_side[hit_count] = side
		hit_count += 1


func _pop(attacker_index: int, defender_index: int, side: int) -> void:
	var defender: BubbleDuelFighter = fighters[defender_index]
	if not _side_exists(defender, side):
		return
	_event("pop", bubble_position(defender, side), defender_index)
	defender.bubbles -= 1
	if defender.bubbles == 1:
		defender.survivor_side = -side
	var attacker: BubbleDuelFighter = fighters[attacker_index]
	attacker.pops += 1
	pops += 1
	_bump(attacker, defender)
	attacker.velocity.y = minf(attacker.velocity.y, -motion.pop_hop)


func _body_touch(a: BubbleDuelFighter, b: BubbleDuelFighter) -> bool:
	if a.lost or b.lost or a.swallowed or b.swallowed:
		return false
	var first := Rect2(a.position + a.body_box.position, a.body_box.size)
	var shifted := Vector2(a.position.x + Motion.wrapped_dx(b.position.x - a.position.x), b.position.y)
	return first.intersects(Rect2(shifted + b.body_box.position, b.body_box.size))


func _bump(a: BubbleDuelFighter, b: BubbleDuelFighter) -> void:
	var before: Vector2 = a.velocity
	if absf(Motion.wrapped_dx(a.position.x - b.position.x)) > 6.0:
		var previous_x: float = a.velocity.x
		a.velocity.x = b.velocity.x
		b.velocity.x = previous_x
	if absf(a.position.y - b.position.y) > 6.0:
		var previous_y: float = a.velocity.y
		a.velocity.y = b.velocity.y
		b.velocity.y = previous_y
	exchanged_motion += (a.velocity - before).length()
	a.body_bounces += 1
	b.body_bounces += 1
	bumps += 1


func _step_shots() -> void:
	for index: int in range(shots.size() - 1, -1, -1):
		var shot: Dictionary = shots[index]
		if int(shot["life"]) <= 0:
			continue
		var old: Vector2 = shot["position"]
		var point: Vector2 = old + Vector2(float(shot["vx"]), 0.0)
		if point.x > Motion.WRAP_MAX: point.x = Motion.WRAP_MIN
		if point.x < Motion.WRAP_MIN: point.x = Motion.WRAP_MAX
		shot["previous"] = old
		shot["position"] = point
		shot["life"] = int(shot["life"]) - 1
		var owner: int = int(shot["owner"])
		for defender: BubbleDuelFighter in fighters:
			if defender.team == fighters[owner].team or defender.lost or defender.swallowed or defender.invincible > 0:
				continue
			for side: int in SIDES:
				if not _side_exists(defender, side):
					continue
				var from: Vector2 = old - bubble_position(defender, side, true)
				var to: Vector2 = point - bubble_position(defender, side)
				from.x = Motion.wrapped_dx(from.x)
				to.x = from.x + Motion.wrapped_dx(to.x - from.x)
				if Geometry2D.get_closest_point_to_segment(Vector2.ZERO, from, to).length() <= bubble_radius(defender) + 5.0:
					_hit(owner, defender.slot, side)
					shot["life"] = 0
					break
			if int(shot["life"]) <= 0:
				break


func _resolve_finish() -> void:
	if not competitive:
		return
	var alive_team: int = -1
	var multiple: bool = false
	for fighter: BubbleDuelFighter in fighters:
		if fighter.lost:
			continue
		if alive_team < 0:
			alive_team = fighter.team
		elif alive_team != fighter.team:
			multiple = true
	if not multiple:
		if alive_team >= 0:
			var viable: bool = false
			for fighter: BubbleDuelFighter in fighters:
				if not fighter.lost and (fighter.bubbles > 0 or fighter.spares > 0 or fighter.unlimited_rescues):
					viable = true
			if not viable:
				return
		finished = true
		winner = alive_team
		_event("finish", Vector2.ZERO, winner)


func _event(kind: String, at: Vector2, actor: int) -> void:
	if event_count < events.size():
		var event: Dictionary = events[event_count]
		event["kind"] = kind
		event["position"] = at
		event["actor"] = actor
		event_count += 1
