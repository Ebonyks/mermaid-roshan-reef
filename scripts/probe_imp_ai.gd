extends SceneTree
# THE IMP BRAIN PROBE (scripts/imp_ai.gd).
#
# The brain is pure logic with a seeded RNG, so this probe runs it headless
# with no scene at all: it drives whole fights at a fixed step and asserts
# on the DECISION STREAM. What it guards:
#
#   * readability — every charge is announced by a telegraph, and no
#     telegraph is ever shorter than MIN_WINDUP
#   * commitment  — a charge aims where she WAS, so stepping aside works
#   * fairness    — never more than the crew's ceiling attacking at once,
#     and a landed bump can never come in a drizzle
#   * no fail     — the brain pops nobody, scores nothing, and a crew left
#     completely alone can never resolve itself
#   * mood        — a thinned crew hangs back (flee/rally), a long fight
#     eases (mercy), a child who lands hits meets a bolder crew
#   * determinism — same seed, same fight; different seed, different fight

const STEP := 1.0 / 60.0
const STAGE_TUNE := {
	"strike_range": 300.0,
	"stand_off": 186.0,
	"contact": 104.0,
	"speed": 132.0,
	"charge_speed": 520.0,
	"flee_speed": 250.0,
	"windup": 0.95,
	"charge_time": 0.4,
	"slash_time": 0.28,
	"recover": 1.15,
	"cool_min": 2.4,
	"cool_max": 5.0,
	"max_attackers": 2,
	"captain_scale": 1.2,
}
const KNOWN_EVENTS := [
	"telegraph", "charge", "contact", "whiff", "taunt", "rally",
	"flee", "stagger", "guard", "popped",
]

var bad := 0
var hero := Vector2(640.0, 470.0)


func _init() -> void:
	var main_run: Dictionary = _run({"seconds": 60.0})
	_report(main_run)
	_dodge_case()
	_thinned_case()
	_captain_case()
	_quiet_case()
	_mercy_and_floor_case()
	_determinism_case()
	print("IMPAI|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()


func _ck(label: String, ok: bool) -> void:
	print("IMPAI|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1


## One headless fight. Options: seconds, count, seed, pop_at (pop all but two
## at that time), swing_every (a child landing hits), lunges.
func _run(opts: Dictionary) -> Dictionary:
	hero = Vector2(640.0, 470.0)
	var count: int = int(opts.get("count", 6))
	var tune: Dictionary = STAGE_TUNE.duplicate()
	if opts.has("lunges"):
		tune["lunges"] = bool(opts["lunges"])
	var brain := ImpAI.new(tune, int(opts.get("seed", 4242)))
	brain.begin_crew(count)
	var crew: Array[Dictionary] = []
	for i in range(count):
		var mind: Dictionary = brain.spawn_mind(i, i == count - 1)
		mind["pos"] = Vector2(120.0 + float(i) * 180.0, 470.0)
		crew.append(mind)
	var events: Array[Dictionary] = []
	var poses: Dictionary = {}
	var counts: Dictionary = {}
	var max_committed := 0
	var seconds: float = float(opts.get("seconds", 60.0))
	var steps: int = int(seconds / STEP)
	var pop_at: float = float(opts.get("pop_at", -1.0))
	var swing_every: float = float(opts.get("swing_every", -1.0))
	for step in range(steps):
		var now: float = float(step) * STEP
		brain.tick(STEP, crew, hero)
		for ev: Dictionary in brain.drain_events():
			ev["at"] = now
			events.append(ev)
			var kind: String = String(ev.get("kind", ""))
			counts[kind] = int(counts.get(kind, 0)) + 1
		var committed := 0
		for mind: Dictionary in crew:
			if not bool(mind.get("alive", false)):
				continue
			var state: String = String(mind.get("state", ""))
			if state == "windup" or state == "charge" or state == "slash":
				committed += 1
			poses[String(mind.get("pose", ""))] = true
		max_committed = maxi(max_committed, committed)
		if pop_at > 0.0 and absf(now - pop_at) < STEP * 0.5:
			for i in range(crew.size() - 2):
				brain.on_hit(crew[i], true)
		if swing_every > 0.0 and fmod(now, swing_every) < STEP:
			brain.on_player_swing(true)
	return {"brain": brain, "crew": crew, "events": events, "poses": poses,
		"counts": counts, "max_committed": max_committed}


func _kinds(events: Array[Dictionary]) -> Array[String]:
	var out: Array[String] = []
	for ev: Dictionary in events:
		out.append("%s:%d" % [String(ev.get("kind", "")), int(ev.get("index", -1))])
	return out


func _report(run: Dictionary) -> void:
	var events: Array = run["events"]
	var counts: Dictionary = run["counts"]
	var poses: Dictionary = run["poses"]
	var brain: ImpAI = run["brain"]
	var crew: Array = run["crew"]

	_ck("the crew actually acts instead of waiting to be tapped",
		int(counts.get("telegraph", 0)) >= 8 and int(counts.get("charge", 0)) >= 8)

	# every charge is announced, and the announcement is long enough to read
	var telegraphed: Dictionary = {}
	var unannounced := 0
	var shortest := 99.0
	for ev: Dictionary in events:
		var kind: String = String(ev.get("kind", ""))
		var index: int = int(ev.get("index", -1))
		if kind == "telegraph":
			telegraphed[index] = float(ev.get("at", 0.0))
		elif kind == "charge":
			if not telegraphed.has(index):
				unannounced += 1
			else:
				shortest = minf(shortest, float(ev.get("at", 0.0)) - float(telegraphed[index]))
				telegraphed.erase(index)
	_ck("no imp ever charges without telegraphing first", unannounced == 0)
	_ck("every telegraph is at least the readability floor",
		shortest >= ImpAI.MIN_WINDUP - STEP * 2.0)

	_ck("the crew never exceeds its simultaneous-attacker ceiling",
		int(run["max_committed"]) <= int(STAGE_TUNE["max_attackers"]))

	# bumps are events, not a drizzle
	var last := -99.0
	var too_soon := 0
	for ev: Dictionary in events:
		if String(ev.get("kind", "")) != "contact":
			continue
		var at: float = float(ev.get("at", 0.0))
		if at - last < float(brain.tune.get("contact_gap", 5.0)) - 0.05:
			too_soon += 1
		last = at
	_ck("landed bumps keep the crew-wide breathing gap", too_soon == 0)

	# the decision stream is varied — a real repertoire, not one behaviour
	var wanted: Array[String] = ["prowl", "stalk", "flank", "windup", "charge",
		"slash", "recover", "taunt"]
	var missing_pose := ""
	for pose: String in wanted:
		if not poses.has(pose):
			missing_pose = pose
	_ck("the crew plays its whole repertoire of poses", missing_pose == "")
	var stray := ""
	for pose: String in poses:
		if not ImpAI.POSES.has(pose):
			stray = pose
	_ck("every pose it asks a renderer for is a declared pose", stray == "")
	var unknown := ""
	for kind: String in counts:
		if not KNOWN_EVENTS.has(kind):
			unknown = kind
	_ck("the brain only emits declared, harmless events", unknown == "")

	# NO FAIL: nobody left alone resolves anything
	var all_alive := true
	for mind: Dictionary in crew:
		all_alive = all_alive and bool(mind.get("alive", false))
	_ck("the brain never pops an imp by itself", all_alive
		and int(counts.get("popped", 0)) == 0)
	_ck("an untouched crew grows bolder instead of stalling",
		brain.aggression > 0.35)


func _dodge_case() -> void:
	# a charge is aimed where she WAS: stepping aside must beat it
	hero = Vector2(640.0, 470.0)
	var brain := ImpAI.new(STAGE_TUNE, 77)
	brain.begin_crew(4)
	var crew: Array[Dictionary] = []
	for i in range(4):
		var mind: Dictionary = brain.spawn_mind(i, false)
		mind["pos"] = Vector2(200.0 + float(i) * 260.0, 470.0)
		crew.append(mind)
	var watched := -1
	var outcome := ""
	var locked := Vector2.ZERO
	var aim_drift := 0.0
	for step in range(int(40.0 / STEP)):
		brain.tick(STEP, crew, hero)
		for ev: Dictionary in brain.drain_events():
			var kind: String = String(ev.get("kind", ""))
			var index: int = int(ev.get("index", -1))
			if kind == "charge" and watched < 0:
				watched = index
				locked = crew[index].get("aim", Vector2.ZERO)
				hero += Vector2(420.0, 0.0)      # she steps out of the way
			elif index == watched and outcome == "" and (kind == "contact" or kind == "whiff"):
				outcome = kind
		if watched >= 0 and outcome == "":
			# only while THAT lunge is still in the air — a later attack is
			# allowed a fresh aim, that is the whole point of committing
			if String(crew[watched].get("state", "")) == "charge":
				var aim: Vector2 = crew[watched].get("aim", Vector2.ZERO)
				aim_drift = maxf(aim_drift, aim.distance_to(locked))
	_ck("a committed charge can be stepped out of", outcome == "whiff")
	_ck("a charge never re-homes onto her once committed", aim_drift <= 1.0)


func _thinned_case() -> void:
	var run: Dictionary = _run({"seconds": 60.0, "pop_at": 12.0, "seed": 91})
	var brain: ImpAI = run["brain"]
	var counts: Dictionary = run["counts"]
	var poses: Dictionary = run["poses"]
	_ck("a thinned crew loses its nerve and scampers", poses.has("flee")
		and int(counts.get("flee", 0)) > 0)
	_ck("the captain rallies what is left of the crew", int(counts.get("rally", 0)) > 0)
	_ck("a thinned crew stops swarming", brain.morale <= 0.4
		and brain.attackers_allowed() == 1)
	_ck("a rally is a beat, not a loop", int(counts.get("rally", 0)) <= 6)


func _captain_case() -> void:
	# a captain who takes a hit reels, then guards, and the guard always drops
	hero = Vector2(640.0, 470.0)
	var brain := ImpAI.new(STAGE_TUNE, 5150)
	brain.begin_crew(2)
	var crew: Array[Dictionary] = []
	var boss: Dictionary = brain.spawn_mind(0, true)
	boss["pos"] = Vector2(760.0, 470.0)
	crew.append(boss)
	var mate: Dictionary = brain.spawn_mind(1, false)
	mate["pos"] = Vector2(500.0, 470.0)
	crew.append(mate)
	brain.tick(STEP, crew, hero)
	brain.on_hit(boss, false)
	_ck("a hit that does not pop leaves the imp reeling",
		String(boss.get("state", "")) == "stagger" and bool(boss.get("alive", false)))
	var saw_guard := false
	for step in range(int(6.0 / STEP)):
		brain.tick(STEP, crew, hero)
		saw_guard = saw_guard or String(boss.get("state", "")) == "guard"
	_ck("a staggered captain comes up guarding", saw_guard)
	_ck("a guard always drops on its own clock",
		String(boss.get("state", "")) != "guard")
	brain.on_hit(boss, true)
	_ck("a popped imp leaves the fight for good",
		not bool(boss.get("alive", false)) and String(boss.get("pose", "")) == "bopped")


func _quiet_case() -> void:
	# QTE fights (stuffie battle) borrow the spacing brain with lunges off:
	# the crew still circles and shows off, but never attacks on its own
	var run: Dictionary = _run({"seconds": 30.0, "lunges": false, "seed": 3131})
	var counts: Dictionary = run["counts"]
	var poses: Dictionary = run["poses"]
	_ck("a QTE fight keeps attacking to itself",
		int(counts.get("telegraph", 0)) == 0 and int(counts.get("charge", 0)) == 0
		and int(counts.get("contact", 0)) == 0)
	_ck("a QTE fight still gets crew spacing and showmanship",
		poses.has("stalk") and poses.has("taunt"))


func _mercy_and_floor_case() -> void:
	hero = Vector2(640.0, 470.0)
	var brain := ImpAI.new(STAGE_TUNE, 2026)
	brain.begin_crew(5)
	var crew: Array[Dictionary] = []
	for i in range(5):
		var mind: Dictionary = brain.spawn_mind(i, false)
		mind["pos"] = Vector2(240.0 + float(i) * 200.0, 470.0)
		crew.append(mind)
	for step in range(int(120.0 / STEP)):
		brain.tick(STEP, crew, hero)
		brain.drain_events()
	_ck("a long fight eases into full mercy", is_equal_approx(brain.mercy, 1.0))
	_ck("mercy makes it a one-at-a-time fight", brain.attackers_allowed() == 1)
	_ck("mercy lengthens the telegraph, never shortens it",
		brain.windup_time() >= float(STAGE_TUNE["windup"]))
	# the readability floor holds even for the boldest possible crew
	brain.aggression = 1.0
	brain.mercy = 0.0
	_ck("the readability floor survives a fully bold crew",
		brain.windup_time() >= ImpAI.MIN_WINDUP)


func _determinism_case() -> void:
	var a: Dictionary = _run({"seconds": 25.0, "seed": 606})
	var b: Dictionary = _run({"seconds": 25.0, "seed": 606})
	var c: Dictionary = _run({"seconds": 25.0, "seed": 909})
	var ka: Array[String] = _kinds(a["events"])
	var kb: Array[String] = _kinds(b["events"])
	var kc: Array[String] = _kinds(c["events"])
	_ck("the same fight replays exactly the same way", ka == kb and not ka.is_empty())
	_ck("a different fight is a different fight", ka != kc)
