class_name ImpAI
extends RefCounted
# ONE BRAIN FOR EVERY MISCHIEF IMP (2026-08-02).
#
# Before this, each imp fight had its own two-line "walk at the hero" loop:
# the opera stage imps ping-ponged along the painted walkway waiting to be
# tapped, the brawl imps beelined and bumped, the arena imps drifted to 7m
# and lobbed one slow orb. They never decided anything, so they never read
# as characters. This module is the decision layer they share.
#
# WHAT IT IS
#   * pure logic, no nodes, no engine coupling — every fight keeps its own
#     rendering and its own state (Phase 7 satellite rules)
#   * plane-agnostic: the brain thinks in an abstract 2D plane in WHATEVER
#     units the caller uses (screen px for the opera stage, metres on the
#     x/z floor for the 3D fights). Ranges/speeds come from the caller's
#     tuning dict, so one brain serves a 1280px stage and a 27m arena.
#   * seeded RNG only — same seed, same decisions, so probes can assert on
#     the decision stream instead of on luck.
#
# THE LOOP (per imp)
#   prowl/stalk/flank  — hold the crew's spacing ring, close the gap
#   windup             — TELEGRAPH: freeze, crouch, "!" — never below
#                        MIN_WINDUP seconds, however bold the crew gets
#   charge             — commit to the aim locked at windup (committing is
#                        what makes it dodgeable — it does not home)
#   slash              — the swipe at the end of the charge
#   recover            — the counter window: slow, wide open, easy to bop
#   guard              — captains only, and a guard always drops on its own
#   taunt / rally / flee — the crew reacting to how the fight is going
#
# THE CREW BRAIN (per tick)
#   * attack tokens: only a few imps may be winding up at once, so the
#     child never faces a wall of simultaneous attacks
#   * flank slots: alive imps get evenly-spaced angles around the hero, so
#     they surround instead of forming a conga line
#   * morale: falls as the crew is popped — a thinned crew hangs back,
#     taunts and regroups instead of swarming, and the fight winds down
#   * aggression: rises while the child is NOT landing hits (the imps come
#     to her — nothing ever stalls) and drops on every pop (breathing room)
#   * mercy: a long fight slows everything and lengthens every telegraph
#
# NO-FAIL CONTRACT (binding, CLAUDE.md)
#   The brain never deals damage and never scores. A landed slash emits a
#   "contact" event and nothing else; the caller turns it into a bubble
#   shield bump, a sparkle and a shove. Imps cannot end a fight, cannot
#   take progress away, and cannot make progress happen either — a
#   zero-input run must still win nothing (probe_passive).
#
# Poses are advisory strings the renderer maps to whatever art it has
# (see CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md for the state sprites
# being drawn for these); a renderer with only an idle sprite can still
# play every pose procedurally.

## Every pose the brain can ask a renderer for, in the order a fight
## naturally walks through them. Renderers must handle all of these
## (fallback: idle) — probe_imp_ai asserts the list is covered.
const POSES: Array[String] = [
	"idle", "prowl", "stalk", "flank", "windup", "charge", "slash",
	"recover", "guard", "taunt", "rally", "flee", "stagger", "bopped",
]

## The readability floor. No amount of boldness, aggression or crew size
## may telegraph an attack faster than this — a four-year-old has to see
## it coming. Enforced in windup_time(), asserted by the probe.
const MIN_WINDUP := 0.55

## Caller units. Every distance/speed below is in the caller's own plane
## units; the defaults are metre-ish (the 3D fights) and the opera stage
## passes a pixel-scaled override.
const DEFAULTS := {
	"strike_range": 7.0,     # close enough to commit a charge
	"stand_off": 4.6,        # preferred spacing ring while stalking
	"contact": 2.4,          # how near a slash has to pass to land
	"speed": 5.5,            # stalk speed
	"charge_speed": 15.0,    # dash speed while committed
	"flee_speed": 8.0,
	"windup": 0.9,           # telegraph seconds before a charge
	"charge_time": 0.42,
	"slash_time": 0.26,
	"recover": 1.05,         # the counter window after a swing
	"stagger": 0.5,          # reeling after a non-popping hit
	"guard_time": 0.85,
	"taunt_time": 0.9,
	"flee_time": 1.2,        # a retreat always ends — nobody runs forever
	"rally_time": 1.0,
	"cool_min": 2.2,         # attack cooldown at full aggression
	"cool_max": 4.8,         # attack cooldown at rest
	"max_attackers": 2,      # hard ceiling on simultaneous winders-up
	"contact_gap": 5.0,      # crew-wide floor between landed bumps: being
	                         # bumped is an event, never a nagging drizzle
	"taunt_gap": 5.5,        # per-imp floor between showing off
	"lunges": true,          # false: the CALLER owns attacking (QTE fights),
	                         # the brain still owns spacing, mood and poses
	"captain_scale": 1.25,   # captains are bolder and hit a little wider
	"mercy_delay": 45.0,     # seconds before a long fight starts easing
	"mercy_ramp": 60.0,
}

var tune: Dictionary = {}
var rng := RandomNumberGenerator.new()

# crew-level mood
var crew_size := 0
var alive := 0
var morale := 1.0
var aggression := 0.35
var mercy := 0.0
var elapsed := 0.0
var since_player_hit := 0.0    # rises while the child lands nothing
var since_player_try := 0.0    # rises while the child does nothing at all
var attackers := 0
var last_contact := -99.0
var events: Array[Dictionary] = []


func _init(config: Dictionary = {}, seed_value: int = 20260802) -> void:
	tune = DEFAULTS.duplicate()
	configure(config)
	rng.seed = seed_value


func configure(config: Dictionary) -> void:
	for key: String in config:
		tune[key] = config[key]


## One fresh mind. The caller keeps it wherever its enemy record lives and
## writes "pos" (and "alive") before each tick; everything else is ours.
func spawn_mind(index: int, captain: bool = false) -> Dictionary:
	return {
		"index": index,
		"captain": captain,
		"state": "prowl",
		"pose": "prowl",
		"t": 0.0,               # seconds in the current state
		"pos": Vector2.ZERO,
		"aim": Vector2.ZERO,    # locked at windup — a charge does NOT home
		"face": 1.0,
		"alive": true,
		"cool": 1.2 + float(index) * 0.35,
		"token": false,
		"slot": float(index),
		"stun": 0.0,
		"contacted": false,
		"boldness": 0.35 + float(index % 3) * 0.18 + (0.3 if captain else 0.0),
		"hits": 0,
		"acts": 0,              # attacks committed — decision-stream evidence
		"flee_cd": 0.0,         # per-imp floor between retreats
		"taunt_cd": 2.5,        # per-imp floor between show-off beats
		"seen": {},             # states this imp has actually played
	}


## Start (or restart) a crew of `count` imps. Morale/aggression reset with
## it so the second wave does not inherit the first wave's exhaustion.
func begin_crew(count: int) -> void:
	crew_size = maxi(1, count)
	alive = crew_size
	morale = 1.0
	aggression = 0.35
	mercy = 0.0
	elapsed = 0.0
	since_player_hit = 0.0
	since_player_try = 0.0
	attackers = 0
	last_contact = -99.0
	events.clear()


## The child swung. `landed` false means she missed — the crew reads that
## as "she needs a slower fight" and eases off; landing hits emboldens it.
func on_player_swing(landed: bool) -> void:
	since_player_try = 0.0
	if landed:
		since_player_hit = 0.0
		aggression = clampf(aggression - 0.22, 0.05, 1.0)
	else:
		aggression = clampf(aggression - 0.08, 0.0, 1.0)


## An imp took a hit. `popped` retires it; otherwise it reels (captains).
func on_hit(mind: Dictionary, popped: bool) -> void:
	mind["hits"] = int(mind.get("hits", 0)) + 1
	mind["token"] = false
	if popped:
		mind["alive"] = false
		_set_state(mind, "bopped")
		alive = maxi(0, alive - 1)
		morale = clampf(float(alive) / float(maxi(1, crew_size)), 0.0, 1.0)
		_emit("popped", mind)
	else:
		mind["stun"] = float(tune.get("stagger", 0.5))
		_set_state(mind, "stagger")
		_emit("stagger", mind)


## Something held this imp still (Huluu's stun bubble, a freeze berry). It
## reels for `seconds` and cannot decide anything until it wears off.
func on_stun(mind: Dictionary, seconds: float) -> void:
	mind["token"] = false
	mind["stun"] = maxf(seconds, float(tune.get("stagger", 0.5)))
	_set_state(mind, "stagger")
	_emit("stagger", mind)


## FX/voice hooks: the caller drains these each frame and decides what a
## telegraph or a rally looks and sounds like in its own scene.
func drain_events() -> Array[Dictionary]:
	var out: Array[Dictionary] = events.duplicate()
	events.clear()
	return out


## How many imps may be winding up or charging right now.
func attackers_allowed() -> int:
	var ceiling: int = int(tune.get("max_attackers", 2))
	var want: int = 1 + int(floorf(aggression * 2.0))
	if morale < 0.4:
		want = 1                       # a thinned crew stops swarming
	if alive <= 2:
		want = 1
	want = mini(want, ceiling)
	if mercy > 0.5:
		want = 1                       # a long fight is a one-at-a-time fight
	return maxi(1, want)


## The telegraph length actually used right now, floor included.
func windup_time() -> float:
	var base: float = float(tune.get("windup", 0.9))
	var quick: float = base * (1.0 - 0.22 * aggression)
	return maxf(MIN_WINDUP, quick * (1.0 + 0.4 * mercy))


## Attack cooldown after a swing — bold crews come back sooner.
func cooldown_time() -> float:
	var lo: float = float(tune.get("cool_min", 2.2))
	var hi: float = float(tune.get("cool_max", 4.8))
	# the jitter is seeded, so it stays deterministic per fight while
	# keeping the crew from breathing in lockstep
	return lerpf(hi, lo, aggression) * (1.0 + 0.55 * mercy) + rng.randf_range(0.0, 0.8)


## Speed multiplier every mover honours, so mercy slows the whole crew.
func pace() -> float:
	return (0.85 + 0.35 * aggression) * (1.0 - 0.4 * mercy)


## The whole crew thinks. `crew` is an array of minds (spawn_mind results);
## the caller writes each mind's "pos" first and reads "pos"/"pose"/"face"
## back after. `hero` is the child's position in the same plane.
func tick(delta: float, crew: Array, hero: Vector2) -> void:
	if delta <= 0.0:
		return
	elapsed += delta
	since_player_hit += delta
	since_player_try += delta
	var delay: float = float(tune.get("mercy_delay", 45.0))
	var ramp: float = maxf(1.0, float(tune.get("mercy_ramp", 60.0)))
	mercy = clampf((elapsed - delay) / ramp, 0.0, 1.0)
	# nobody is landing hits -> the imps come to her. This is the anti-stall
	# rule: a child who stops playing still gets something to react to.
	aggression = clampf(aggression + delta * (0.10 if since_player_hit > 3.0 else 0.02), 0.0, 1.0)

	var live: Array[Dictionary] = []
	for entry: Dictionary in crew:
		if bool(entry.get("alive", false)):
			live.append(entry)
	alive = live.size()
	if crew_size <= 0:
		crew_size = maxi(1, alive)
	morale = clampf(float(alive) / float(maxi(1, crew_size)), 0.0, 1.0)

	_assign_slots(live, hero)
	_grant_tokens(live, hero)
	for mind: Dictionary in live:
		_think(mind, delta, hero)


# ---------------------------------------------------------------- crew brain

func _assign_slots(live: Array[Dictionary], hero: Vector2) -> void:
	# evenly spaced approach angles around the hero, handed out by the angle
	# each imp already holds — imps keep their side of the fight instead of
	# trading places every frame, and they never stack into one column
	if live.is_empty():
		return
	var order: Array[Dictionary] = live.duplicate()
	order.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var pa: Vector2 = a.get("pos", Vector2.ZERO)
		var pb: Vector2 = b.get("pos", Vector2.ZERO)
		return (pa - hero).angle() < (pb - hero).angle())
	for i in range(order.size()):
		var mind: Dictionary = order[i]
		mind["slot"] = float(i) * TAU / float(order.size())


func _grant_tokens(live: Array[Dictionary], hero: Vector2) -> void:
	# count who is already committed, then hand the spare tokens to the
	# closest ready imps — the crew decides WHO attacks, not each imp alone
	if not bool(tune.get("lunges", true)):
		attackers = 0
		return
	var busy := 0
	for mind: Dictionary in live:
		var state: String = String(mind.get("state", "prowl"))
		if state == "windup" or state == "charge" or state == "slash":
			busy += 1
		elif bool(mind.get("token", false)):
			busy += 1
	attackers = busy
	var spare: int = attackers_allowed() - busy
	if spare <= 0:
		return
	var ready: Array[Dictionary] = []
	for mind: Dictionary in live:
		if bool(mind.get("token", false)) or float(mind.get("cool", 0.0)) > 0.0:
			continue
		var state: String = String(mind.get("state", "prowl"))
		if state != "prowl" and state != "stalk" and state != "flank" and state != "taunt":
			continue
		var pos: Vector2 = mind.get("pos", Vector2.ZERO)
		if pos.distance_to(hero) > float(tune.get("strike_range", 7.0)) * 2.2:
			continue
		ready.append(mind)
	if ready.is_empty():
		return
	ready.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var pa: Vector2 = a.get("pos", Vector2.ZERO)
		var pb: Vector2 = b.get("pos", Vector2.ZERO)
		var ba: float = float(a.get("boldness", 0.5))
		var bb: float = float(b.get("boldness", 0.5))
		return pa.distance_to(hero) - ba * 2.0 < pb.distance_to(hero) - bb * 2.0)
	for i in range(mini(spare, ready.size())):
		var mind: Dictionary = ready[i]
		mind["token"] = true


# ------------------------------------------------------------- per-imp brain

func _set_state(mind: Dictionary, state: String) -> void:
	mind["state"] = state
	mind["pose"] = state
	mind["t"] = 0.0
	var seen: Dictionary = mind.get("seen", {})
	seen[state] = int(seen.get(state, 0)) + 1
	mind["seen"] = seen


func _emit(kind: String, mind: Dictionary) -> void:
	events.append({
		"kind": kind,
		"index": int(mind.get("index", 0)),
		"captain": bool(mind.get("captain", false)),
		"pos": mind.get("pos", Vector2.ZERO),
	})


func _step(mind: Dictionary, toward: Vector2, speed: float, delta: float) -> void:
	var pos: Vector2 = mind.get("pos", Vector2.ZERO)
	var away: Vector2 = toward - pos
	if away.length() < 0.001:
		return
	var move: Vector2 = away.normalized() * speed * delta
	if move.length() > away.length():
		move = away
	mind["pos"] = pos + move
	if absf(move.x) > 0.0001:
		mind["face"] = signf(move.x)


## Close in the way a circling crew does: pull the RADIUS toward the ring
## while sliding the ANGLE toward this imp's slot. Walking straight at a
## ring point on the far side would march an imp clean through Roshan;
## orbiting can't, so nobody ever stands inside her.
func _orbit_step(mind: Dictionary, hero: Vector2, radius: float, speed: float, delta: float) -> void:
	var pos: Vector2 = mind.get("pos", hero)
	var rel: Vector2 = pos - hero
	var r: float = maxf(rel.length(), 0.001)
	var a: float = rel.angle()
	var wobble: float = sin(elapsed * 1.3 + float(mind.get("index", 0))) * 0.22
	var want_a: float = float(mind.get("slot", 0.0)) + wobble
	var dr: float = clampf(radius - r, -speed * delta, speed * delta)
	var swing: float = speed * delta / maxf(r, radius * 0.35)
	var da: float = clampf(wrapf(want_a - a, -PI, PI), -swing, swing)
	var next: Vector2 = hero + Vector2(cos(a + da), sin(a + da)) * (r + dr)
	if absf(next.x - pos.x) > 0.0001:
		mind["face"] = signf(next.x - pos.x)
	mind["pos"] = next


func _think(mind: Dictionary, delta: float, hero: Vector2) -> void:
	mind["t"] = float(mind.get("t", 0.0)) + delta
	mind["cool"] = maxf(0.0, float(mind.get("cool", 0.0)) - delta)
	mind["flee_cd"] = maxf(0.0, float(mind.get("flee_cd", 0.0)) - delta)
	mind["taunt_cd"] = maxf(0.0, float(mind.get("taunt_cd", 0.0)) - delta)
	var state: String = String(mind.get("state", "prowl"))
	var pos: Vector2 = mind.get("pos", Vector2.ZERO)
	var dist: float = pos.distance_to(hero)
	var t: float = float(mind["t"])
	var boost: float = float(tune.get("captain_scale", 1.25)) if bool(mind.get("captain", false)) else 1.0

	match state:
		"stagger":
			mind["stun"] = maxf(0.0, float(mind.get("stun", 0.0)) - delta)
			# reeling backwards, then straight into the guard a captain owes
			_step(mind, pos + (pos - hero), float(tune.get("speed", 5.5)) * 0.6, delta)
			if float(mind["stun"]) <= 0.0:
				if bool(mind.get("captain", false)):
					_set_state(mind, "guard")
					_emit("guard", mind)
				else:
					_set_state(mind, "prowl")
			return
		"guard":
			# a guard ALWAYS drops on its own clock: nothing a child can do
			# wrong, nothing she has to wait out twice
			if t >= float(tune.get("guard_time", 0.85)) * (1.0 - 0.3 * mercy):
				_set_state(mind, "prowl")
				mind["cool"] = cooldown_time() * 0.5
			return
		"windup":
			# frozen and readable. The aim is locked the moment the crouch
			# starts, so leaning out of the way actually works.
			if t >= windup_time():
				# aim SHORT of her: the lunge stops a body-width away, so
				# it reads as a swipe at Roshan instead of walking into her
				var lunge: Vector2 = hero - pos
				var short: float = float(tune.get("contact", 2.4)) * 0.55
				mind["aim"] = (hero - lunge.normalized() * short) if lunge.length() > short else pos
				mind["contacted"] = false
				_set_state(mind, "charge")
				_emit("charge", mind)
			return
		"charge":
			var aim: Vector2 = mind.get("aim", hero)
			_step(mind, aim, float(tune.get("charge_speed", 15.0)) * boost * pace(), delta)
			var landed_at: Vector2 = mind.get("pos", pos)
			var reached: bool = landed_at.distance_to(aim) < 0.35
			if reached or t >= float(tune.get("charge_time", 0.42)):
				_set_state(mind, "slash")
			return
		"slash":
			var reach: float = float(tune.get("contact", 2.4)) * boost
			if not bool(mind.get("contacted", false)) and dist <= reach:
				mind["contacted"] = true
				if elapsed - last_contact >= float(tune.get("contact_gap", 5.0)):
					last_contact = elapsed
					_emit("contact", mind)  # a bump, never damage
				else:
					# she was bumped a moment ago: this one is theatre only
					_emit("whiff", mind)
			if t >= float(tune.get("slash_time", 0.26)):
				if not bool(mind.get("contacted", false)):
					_emit("whiff", mind)
				mind["acts"] = int(mind.get("acts", 0)) + 1
				mind["token"] = false
				mind["cool"] = cooldown_time()
				_set_state(mind, "recover")
			return
		"recover":
			# the counter window: backing off slowly, wide open to a tap
			_orbit_step(mind, hero, float(tune.get("stand_off", 4.6)) * 1.15,
				float(tune.get("speed", 5.5)) * 0.45, delta)
			if t >= float(tune.get("recover", 1.05)) * (1.0 + 0.4 * mercy):
				_set_state(mind, "prowl")
			return
		"taunt":
			if t >= float(tune.get("taunt_time", 0.9)):
				_set_state(mind, "prowl")
			return
		"rally":
			if t >= float(tune.get("rally_time", 1.0)):
				_set_state(mind, "prowl")
			return
		"flee":
			_step(mind, pos + (pos - hero), float(tune.get("flee_speed", 8.0)) * pace(), delta)
			if t >= float(tune.get("flee_time", 1.2)):
				# a retreat always ends: nobody runs somewhere she cannot reach
				_set_state(mind, "prowl")
			return

	# ---- interruptible states: prowl / stalk / flank -> decide afresh
	var strike: float = float(tune.get("strike_range", 7.0)) * boost
	var stand: float = float(tune.get("stand_off", 4.6))
	if bool(mind.get("token", false)) and float(mind["cool"]) <= 0.0 and dist <= strike:
		mind["token"] = false
		_set_state(mind, "windup")
		_emit("telegraph", mind)
		return
	var seen: Dictionary = mind.get("seen", {})
	if bool(mind.get("captain", false)) and morale <= 0.5 and float(mind["cool"]) <= 0.0 \
			and int(seen.get("rally", 0)) < 3 and dist > stand * 0.8:
		# the captain calls the thinned crew back together — a beat of
		# theatre that also tells the child the fight is nearly won
		_set_state(mind, "rally")
		_emit("rally", mind)
		mind["cool"] = cooldown_time() * 0.6
		return
	if morale <= 0.34 and dist < stand * 0.75 and float(mind.get("flee_cd", 0.0)) <= 0.0:
		# the last of the crew loses its nerve and scampers — briefly, and
		# never more often than flee_cd allows, so it stays catchable
		mind["flee_cd"] = 3.4
		_set_state(mind, "flee")
		_emit("flee", mind)
		return
	if since_player_try > 3.5 and dist <= strike and float(mind.get("taunt_cd", 0.0)) <= 0.0:
		# she has not played in a while: come into view and show off. The
		# taunt is the invitation — it is where the pointer wants her eye.
		mind["taunt_cd"] = float(tune.get("taunt_gap", 5.5))
		_set_state(mind, "taunt")
		_emit("taunt", mind)
		return
	if dist > stand * 1.2:
		if state != "stalk":
			_set_state(mind, "stalk")
		_orbit_step(mind, hero, stand, float(tune.get("speed", 5.5)) * pace(), delta)
		return
	if state != "flank":
		_set_state(mind, "flank")
	# circling the ring keeps the crew spread and keeps every imp reachable
	_orbit_step(mind, hero, stand, float(tune.get("speed", 5.5)) * 0.7 * pace(), delta)
