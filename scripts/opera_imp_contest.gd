class_name OperaImpContest
extends RefCounted
## One job-skill attempt. No scene, reward, save, audio or wall-clock ownership.

const IDLE_SECONDS := 4.0
const CONTESTS := {
	"chef": {"phase": "TOP", "mode": "tap", "context": "target_chef", "units": 7.0, "seconds": 13.0, "flub_at": 4.0, "flub_seconds": 1.8, "poses": [["stagger", 0.4], ["bopped", 1.0], ["recover", 0.4]]},
	"detective": {"phase": "SPARKLE RACE", "before": "CROWN", "mode": "lens", "units": 3.0, "seconds": 21.0, "flub_at": 2.0, "flub_seconds": 2.0, "poses": [["guard", 0.6], ["recover", 1.0], ["idle", 0.4]]},
	"ballerina": {"phase": "GRAND TWIRL", "mode": "ballet_twirl", "units": 3.0, "seconds": 10.5, "flub_at": 2.0, "flub_seconds": 2.0, "poses": [["hop_b", 0.3], ["stagger", 0.4], ["bopped", 1.3]]},
	"candymaker": {"phase": "SHARE", "mode": "tap", "context": "target_candymaker", "units": 6.0, "seconds": 11.0, "flub_at": 3.0, "flub_seconds": 1.8, "poses": [["hop_b", 0.5], ["taunt", 0.6], ["recover", 0.7]]},
	"doctor": {"phase": "BANDAGE", "mode": "swipe", "context": "trace_doctor", "units": 3.0, "seconds": 14.0, "flub_at": 2.0, "flub_seconds": 2.0, "poses": [["stagger", 0.4], ["guard", 1.0], ["recover", 0.6]]},
	"farmer": {"phase": "PICNIC", "mode": "farm_lob", "units": 4.0, "seconds": 17.0, "flub_at": 2.0, "flub_seconds": 1.8, "poses": [["charge", 0.3], ["bopped", 1.1], ["recover", 0.4]]},
	"boxer": {"phase": "TITLE IMP", "mode": "boxing_imp", "units": 6.0, "points": true, "flub_at": 3.0, "flub_seconds": 2.0, "poses": [["stagger", 0.8], ["recover", 1.2]]},
	"magician": {"phase": "HAT DUEL", "before": "PORTAL", "mode": "choice", "context": "lanes_magician", "units": 3.0, "points": true, "flub_at": 2.0, "flub_seconds": 2.0, "poses": [["taunt", 0.4], ["stagger", 0.6], ["recover", 1.0]]},
	"painter": {"phase": "PAINT-OFF", "before": "GALLERY", "mode": "paint_reveal", "units": 1.0, "seconds": 16.0, "flub_at": 0.55, "flub_seconds": 2.0, "poses": [["slash", 0.3], ["stagger", 0.5], ["recover", 1.2]]},
	"astronaut": {"phase": "LAUNCH", "mode": "tap", "context": "target_astronaut", "units": 6.0, "seconds": 12.0, "flub_at": 3.0, "flub_seconds": 1.8, "poses": [["stagger", 0.5], ["bopped", 0.9], ["recover", 0.4]]},
	"racer": {"phase": "RACE", "mode": "kart_race", "units": 2.0, "external_race": true, "flub_at": 1.1, "flub_seconds": 1.5, "poses": []},
	"popstar": {"phase": "SING-OFF", "before": "ENCORE", "mode": "echo", "units": 3.0, "points": true, "flub_at": 2.0, "flub_seconds": 1.5, "poses": [["taunt", 0.4], ["stagger", 0.5], ["recover", 0.6]]},
}

const VOICE_TEXT := {
	"imp_op_astronaut_arrive": "I was sent to learn the SENDING. Nobody sends US anything.",
	"imp_op_astronaut_bop": "Wheee — oh. I landed. That's the hard bit.",
	"imp_op_astronaut_challenge": "Rocket race! Patch the leaks and blast off first!",
	"imp_op_astronaut_copy": "My rocket went sideways. Into a wall. Twice.",
	"imp_op_astronaut_steal": "No invitations, no guests! Hee hee hee!",
	"imp_op_ballerina_arrive": "I was sent to learn the DANCING. Watch my twirl!",
	"imp_op_ballerina_bop": "Whoops! I'm dizzy. Dizzy is a kind of dancing.",
	"imp_op_ballerina_challenge": "Twirl-off! Three big spins. Ready? Spin!",
	"imp_op_ballerina_copy": "Spin, spin, spin, FALL. That's the hard part.",
	"imp_op_ballerina_steal": "The music box! No music, no party, hee hee!",
	"imp_op_boxer_arrive": "I was sent to learn the BOUNCING. Put 'em up!",
	"imp_op_boxer_bop": "Good one! Best two out of three? No? Okay.",
	"imp_op_boxer_challenge": "First to six! Put 'em up!",
	"imp_op_boxer_copy": "Left! Right! ...which one is left again?",
	"imp_op_boxer_steal": "The shiny belt! Champions get invited to things!",
	"imp_op_candymaker_arrive": "I was sent to learn the SWEETS. I am very good at sweets.",
	"imp_op_candymaker_bop": "Oof! My tummy hurts anyway. Too many gumdrops.",
	"imp_op_candymaker_challenge": "Candy race! First to give every friend a sweet wins!",
	"imp_op_candymaker_copy": "One for the bag, two for me. That's how it works!",
	"imp_op_candymaker_steal": "Candy! Every party needs candy and now WE have it!",
	"imp_op_captain_intro": "Two taps will stop me!",
	"imp_op_captain_rally": "Crew! Back to me! Hee hee!",
	"imp_op_chef_arrive": "I was sent to learn the CAKE. Don't mind me, I'm learning.",
	"imp_op_chef_bop": "Fine! The cake needed more sugar anyway!",
	"imp_op_chef_challenge": "Bake-off! Whoever tops their cake first wins!",
	"imp_op_chef_copy": "Flour goes in the bowl... or on my head. Either way!",
	"imp_op_chef_steal": "Mine now! A birthday needs a cake and I HAVE one!",
	"imp_op_contest_win": "I won! I won! Let's play again!",
	"imp_op_detective_arrive": "I was sent to learn the SEARCHING. Where is everything?",
	"imp_op_detective_bop": "Aww. It didn't even fit on my horns.",
	"imp_op_detective_challenge": "Race you to the sparkles! Mine are purple!",
	"imp_op_detective_copy": "I looked under here. And here. Nothing! Detecting is hard.",
	"imp_op_detective_steal": "The sparkly crown! Now everyone will look at ME!",
	"imp_op_doctor_arrive": "I was sent to learn the MENDING. Something of mine is torn too.",
	"imp_op_doctor_bop": "Ouch! Can you fix ME after?",
	"imp_op_doctor_challenge": "Bandage race! Wrap all three paws!",
	"imp_op_doctor_copy": "Bandage on... bandage off. Bandage on my nose?",
	"imp_op_doctor_steal": "I'm taking the patient! He likes me better!",
	"imp_op_farmer_arrive": "I was sent to learn the FEEDING. What do piggies even eat?",
	"imp_op_farmer_bop": "Blegh! I got mud in my mouth.",
	"imp_op_farmer_challenge": "Feeding race! My piggies eat first!",
	"imp_op_farmer_copy": "I planted a rock. Nothing grew. Farming is tricky!",
	"imp_op_farmer_steal": "Snack time! This picnic is OUR picnic now!",
	"imp_op_magician_arrive": "I was sent to learn the MAGIC. Abraca-... something.",
	"imp_op_magician_bop": "Ta-daa! That was supposed to happen. Really.",
	"imp_op_magician_challenge": "Watch my hats! Can you find Lamb-a'?",
	"imp_op_magician_copy": "I made it disappear! ...where did it go? Uh oh.",
	"imp_op_magician_steal": "Now you see the show, now you DON'T!",
	"imp_op_nursery_arrive": "I was sent to learn the QUIET. I am bad at quiet.",
	"imp_op_nursery_bop": "Sorry! Was that too loud? Was it?",
	"imp_op_nursery_copy": "I tried to be quiet. Sorry! Sorry!",
	"imp_op_nursery_steal": "The star mobile! Ours is just a sock on a string!",
	"imp_op_painter_arrive": "I was sent to learn the DECORATING. Ours is very grey.",
	"imp_op_painter_bop": "Bonk! Now I'm a different colour.",
	"imp_op_painter_challenge": "Paint-off! First to finish their picture wins!",
	"imp_op_painter_copy": "I painted my hands. And the wall. And a bit of the floor.",
	"imp_op_painter_steal": "Pretty colours! Our party needs pretty too!",
	"imp_op_popstar_arrive": "I learned a new song. Listen to me sing!",
	"imp_op_popstar_bop": "My ears! Okay okay, you sing it.",
	"imp_op_popstar_challenge": "Sing-off! Sing my song back to me!",
	"imp_op_popstar_copy": "Was that the right note? It felt like a note.",
	"imp_op_popstar_steal": "No microphone, no singing! Our band is better anyway!",
	"imp_op_racer_arrive": "I was sent to learn the FAST. I am already fast!",
	"imp_op_racer_bop": "Pit stop! Pit stop! I need a pit stop!",
	"imp_op_racer_challenge": "Two laps! First one home wins! Go, go, go!",
	"imp_op_racer_copy": "Whoa whoa WHOA — how do you stop this thing?",
	"imp_op_racer_steal": "Catch me! You won't! ...you might!",
	"imp_op_retry": "I found it first! Watch the glowing answer, then solve the same mystery with your sparkle memory!",
	"roshan_op_astronaut_contest": "Patch every leak, then hold to blast off!",
	"roshan_op_ballerina_contest": "Twirl around the music box three times!",
	"roshan_op_boxer_contest": "Punch when the star shines, and guard when he winds up!",
	"roshan_op_candymaker_contest": "Give a candy to every friend before the imp does!",
	"roshan_op_chef_contest": "Put the toppings on my cake before the imp finishes his!",
	"roshan_op_contest_again": "Again! I can do it this time!",
	"roshan_op_detective_contest": "Find my gold sparkles before the imp finds his purple ones!",
	"roshan_op_doctor_contest": "Wrap every sore paw, gentle and quick!",
	"roshan_op_farmer_contest": "Pull back and toss four veggies to the hungry piggy!",
	"roshan_op_magician_contest": "Watch the hat with Lamb-a', then tap it when it stops!",
	"roshan_op_painter_contest": "Paint the whole picture before the imp finishes his!",
	"roshan_op_popstar_contest": "Listen to the imp's song, then sing it back!",
	"roshan_op_racer_steer": "Swipe to steer through the coral gates!",
}

var career := ""
var spec: Dictionary = {}
var state := "waiting"
var attempt := 0
var rematches := 0
var her_units := 0.0
var his_units := 0.0
var his_rate := 1.0
var flub_done := false
var idle_t := IDLE_SECONDS
var beat_t := 0.0
var margin := 0.0
var _overtaken_cool := 0.0
var _was_leading := false
var _worried := false


static func enabled(costume: String, config: Dictionary) -> bool:
	return CONTESTS.has(costume) and not bool(config.get("chapter2_tutorial", false)) \
		and not bool(config.get("tutorial", false)) \
		and String(config.get("reward_policy", "")) != "chapter2_story" \
		and not config.has("phase_overrides") and not config.has("scene_adapter")


static func apply(costume: String, source: Array, two_act: bool) -> Array:
	var output: Array = []
	if not CONTESTS.has(costume):
		return source.duplicate(true)
	var definition: Dictionary = CONTESTS[costume]
	for original: Dictionary in source:
		var phase := original.duplicate(true)
		var stage := not two_act or String(phase.get("performance_part", "")) == "stage"
		if stage and String(phase["name"]) == String(definition.get("before", "")):
			var inserted := {"name": definition["phase"], "performance_part": "stage"}
			output.append(_contest_phase(costume, inserted, definition))
		if stage and String(phase["name"]) == String(definition["phase"]):
			phase = _contest_phase(costume, phase, definition)
		output.append(phase)
	return output


static func _contest_phase(costume: String, phase: Dictionary, definition: Dictionary) -> Dictionary:
	phase["contest"] = definition.duplicate(true)
	phase["mode"] = definition["mode"]
	phase["goal"] = definition["units"]
	phase["vo"] = "op_%s_contest" % costume if costume != "racer" else "op_racer_steer"
	phase["voice"] = String(VOICE_TEXT.get("roshan_" + String(phase["vo"]), ""))
	if definition.has("context"):
		phase["visual_context"] = definition["context"]
	if costume == "detective":
		phase["clue_spot_indices"] = [3, 4, 5]
	return phase


func configure(costume: String) -> void:
	career = costume
	spec = (CONTESTS.get(costume, {}) as Dictionary).duplicate(true)
	rematches = 0
	attempt = 0
	reset_attempt(false)


func configure_inverted(costume: String = "teacher") -> void:
	# Preparation for the separately gated Teacher artwork. No wall-clock points.
	career = costume
	spec = {"units": 3.0, "points": true, "inverted": true}
	rematches = 0
	attempt = 0
	reset_attempt(false)


func score_round(result_name: String) -> Array[String]:
	# The caller commits this only after the child places the true answer.
	var events: Array[String] = []
	if not bool(spec.get("inverted", false)) or not accepting_input():
		return events
	if result_name == "fixed":
		her_units += 1.0
		events.append("player_point")
	elif result_name == "tricked":
		his_units += 1.0
		events.append("imp_point")
	elif result_name != "hinted":
		return events
	if her_units >= player_target():
		state = "player_won"
		margin = clampf(1.0 - his_units / rival_target(), 0.0, 1.0)
		events.append("player_won")
	elif his_units >= rival_target():
		state = "imp_won"
		events.append("imp_won")
	return events


func reset_attempt(rematch: bool = true) -> void:
	if rematch:
		rematches += 1
	attempt += 1
	state = "waiting"
	her_units = 0.0
	his_units = 0.0
	his_rate = maxf(0.75, pow(0.9, rematches)) if career == "racer" \
		else maxf(0.55, pow(0.8, rematches))
	flub_done = false
	idle_t = IDLE_SECONDS
	beat_t = 0.0
	margin = 0.0
	_overtaken_cool = 0.0
	_was_leading = false
	_worried = false


func player_target() -> float:
	return float(spec.get("units", 1.0))


func rival_target() -> float:
	return player_target() + (mini(rematches, 2) if bool(spec.get("points", false)) else 0)


func accepting_input() -> bool:
	return state not in ["imp_won", "player_won", "stopped"]


func note_touch() -> void:
	if not accepting_input():
		return
	idle_t = 0.0
	if state == "waiting" or state == "idle":
		state = "running"


func rival_point() -> void:
	if accepting_input() and idle_t < IDLE_SECONDS and state != "flub":
		his_units += 1.0


func observe_rival(units: float) -> void:
	if accepting_input() and idle_t < IDLE_SECONDS and state != "flub":
		his_units = maxf(his_units, units)


func tick(delta: float, units: float, touched: bool) -> Array[String]:
	var events: Array[String] = []
	if not accepting_input() or spec.is_empty():
		return events
	if bool(spec.get("inverted", false)):
		return events
	her_units = clampf(units, 0.0, player_target())
	# Resolve her accepted final unit before advancing his work: same-frame ties are hers.
	if her_units >= player_target():
		state = "player_won"
		margin = clampf(1.0 - his_units / rival_target(), 0.0, 1.0)
		events.append("player_won")
		return events
	var was_idle := state == "idle"
	if touched:
		note_touch()
		if was_idle:
			events.append("idle_resume")
	var dt := maxf(0.0, delta)
	var working_dt := minf(dt, maxf(0.0, IDLE_SECONDS - idle_t))
	idle_t += dt
	_overtaken_cool = maxf(0.0, _overtaken_cool - dt)
	if state == "waiting":
		return events
	if state == "flub":
		beat_t = maxf(0.0, beat_t - dt)
		if beat_t <= 0.0:
			state = "running"
			events.append("flub_end")
		return events
	if idle_t >= IDLE_SECONDS and state != "idle":
		state = "idle"
		events.append("idle_pause")
	if working_dt > 0.0 and not bool(spec.get("points", false)) \
			and not bool(spec.get("external_race", false)):
		var before := floori(his_units)
		his_units = minf(rival_target(), his_units + working_dt * player_target() \
			/ maxf(0.1, float(spec.get("seconds", 12.0))) * his_rate)
		if floori(his_units) > before:
			events.append("imp_unit")
	var flub_ready := his_units >= float(spec.get("flub_at", 999.0))
	if career in ["magician", "popstar"]:
		flub_ready = flub_ready and his_units >= her_units
	if not flub_done and flub_ready:
		flub_done = true
		state = "flub"
		beat_t = float(spec.get("flub_seconds", 2.0))
		events.append("flub_start")
		return events
	if his_units >= rival_target():
		state = "imp_won"
		events.append("imp_won")
		return events
	var leading := her_units > his_units
	if leading and not _was_leading and _overtaken_cool <= 0.0:
		_overtaken_cool = 3.0
		events.append("imp_overtaken")
	_was_leading = leading
	if her_units >= player_target() * 0.8 and leading and not _worried:
		_worried = true
		events.append("imp_worried")
	return events


func result() -> Dictionary:
	var tier := 3 if margin >= 0.35 else (2 if margin >= 0.15 else 1)
	if rematches > 0:
		tier = mini(tier, 2)
	return {"margin": margin, "tier": tier, "rematches": rematches}
