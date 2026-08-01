class_name OperaCompetition
extends RefCounted
## Shared competition contract for the thirteen Pearl Opera career worlds.
##
## The career engine still owns its tactile minigames. This director turns
## those verbs into one readable stage performance: Roshan versus a dressed
## rival, or Roshan and Faron as a team, with audience meter and graded curtain call.
## Completing the act always earns the career star. The sole retry is the
## Detective's guided rematch: the rival reveals the answer first, so the
## second attempt is recognition rather than lost progress.

const CAREERS := {
	"chef": {
		"world": "REEF BAKE-OFF",
		"contest": "Finish the brightest celebration cake",
		"rival_verb": "whisks",
		"par_time": 92.0,
		"rival_cap": 0.82,
		"accent": Color(1.0, 0.58, 0.52),
	},
	"detective": {
		"world": "TWO-DETECTIVE MYSTERY",
		"contest": "Solve the same missing-tiara case",
		"rival_verb": "checks a clue",
		"par_time": 40.0,
		"rival_cap": 1.0,
		"timed_retry": true,
		"accent": Color(0.58, 0.78, 1.0),
	},
	"ballerina": {
		"world": "TWIN-RIBBON RECITAL",
		"contest": "Win the crowd with rhythm and grace",
		"rival_verb": "turns",
		"par_time": 74.0,
		"rival_cap": 0.84,
		"accent": Color(1.0, 0.58, 0.82),
	},
	"candymaker": {
		"world": "CANDY WORKSHOP CUP",
		"contest": "Make the happiest parade batch",
		"rival_verb": "wraps a sweet",
		"par_time": 82.0,
		"rival_cap": 0.83,
		"accent": Color(1.0, 0.62, 0.72),
	},
	"doctor": {
		"world": "STUFFIE SURGEON RELAY",
		"contest": "Find each ouch, check the X-ray and wrap every stuffie",
		"rival_verb": "repairs a stuffie",
		"par_time": 104.0,
		"rival_cap": 0.80,
		"accent": Color(0.48, 0.86, 0.92),
	},
	"farmer": {
		"world": "PIGGY PICNIC CHALLENGE",
		"contest": "Grow, feed and guide the happiest herd",
		"rival_verb": "feeds a piggy",
		"par_time": 86.0,
		"rival_cap": 0.82,
		"accent": Color(0.58, 0.84, 0.46),
	},
	"boxer": {
		"world": "FRIENDLY CHAMPIONSHIP",
		"contest": "Three rounds against the padded imp",
		"rival_verb": "guards",
		"par_time": 76.0,
		"rival_cap": 0.86,
		"accent": Color(1.0, 0.48, 0.42),
	},
	"magician": {
		"world": "GRAND ILLUSION DUEL",
		"contest": "Top the rival's tricks, then open the star portal",
		"rival_verb": "casts a trick",
		"par_time": 88.0,
		"rival_cap": 0.85,
		"accent": Color(0.82, 0.58, 1.0),
	},
	"painter": {
		"world": "SUNRISE PAINT-OFF",
		"contest": "Race two canvases toward the gallery reveal",
		"rival_verb": "paints a band",
		"par_time": 94.0,
		"rival_cap": 0.84,
		"accent": Color(1.0, 0.62, 0.34),
	},
	"astronaut": {
		"world": "ROCKET REPAIR RACE",
		"contest": "Route the bubbles and launch first",
		"rival_verb": "fits a pipe",
		"par_time": 96.0,
		"rival_cap": 0.82,
		"accent": Color(0.50, 0.82, 1.0),
	},
	"racer": {
		"world": "OPERA GRAND PRIX",
		"contest": "Two laps against the helmeted imp",
		"rival_verb": "takes a corner",
		"par_time": 78.0,
		"rival_cap": 0.94,
		"accent": Color(1.0, 0.42, 0.40),
	},
	"nursery": {
		"world": "MOONBEAM NURSERY TEAM",
		"contest": "Catch, feed, burp and tuck in every baby with Faron",
		"rival_verb": "helps a sleepy baby",
		"par_time": 104.0,
		"rival_cap": 0.82,
		"cooperative": true,
		"partner": "Nurse Faron",
		"accent": Color(0.64, 0.88, 0.82),
	},
	"popstar": {
		"world": "STARLIGHT SOUND-OFF",
		"contest": "Lift the crowd higher than the rival act",
		"rival_verb": "sings a phrase",
		"par_time": 72.0,
		"rival_cap": 0.84,
		"accent": Color(1.0, 0.52, 0.90),
	},
}

var career_id := ""
var spec: Dictionary = {}
var active := false
var completed := false
var elapsed := 0.0
var round_elapsed := 0.0
var player_progress := 0.0
var rival_progress := 0.0
var player_score := 0
var rival_score := 0
var mistakes := 0
var retries := 0
var rival_step := 0
var cheer_tier := 1
var _last_player_progress := 0.0
var _rival_finish_sent := false


func configure(costume: String) -> void:
	career_id = costume
	spec = (CAREERS.get(costume, {}) as Dictionary).duplicate(true)
	active = false
	completed = false
	elapsed = 0.0
	round_elapsed = 0.0
	player_progress = 0.0
	rival_progress = 0.0
	player_score = 0
	rival_score = 0
	mistakes = 0
	retries = 0
	rival_step = 0
	cheer_tier = 1
	_last_player_progress = 0.0
	_rival_finish_sent = false


func is_valid() -> bool:
	return not spec.is_empty()


func is_cooperative() -> bool:
	return bool(spec.get("cooperative", false))


func begin() -> void:
	if not is_valid() or completed:
		return
	active = true
	round_elapsed = 0.0


func pause() -> void:
	active = false


func note_miss() -> void:
	if active:
		mistakes += 1


func note_success(points: int = 12) -> void:
	if active:
		player_score += maxi(points, 0)


func tick(delta: float, observed_progress: float) -> Array[String]:
	var events: Array[String] = []
	if not active or completed:
		return events
	elapsed += delta
	round_elapsed += delta
	player_progress = maxf(player_progress, clampf(observed_progress, 0.0, 1.0))
	var gained := maxf(0.0, player_progress - _last_player_progress)
	if gained > 0.0001:
		player_score += maxi(1, int(round(gained * 760.0)))
		_last_player_progress = player_progress

	var par_time := maxf(10.0, float(spec.get("par_time", 80.0)))
	var cap := clampf(float(spec.get("rival_cap", 0.82)), 0.2, 1.0)
	var rhythm := 0.94 + sin(round_elapsed * 0.73 + float(retries) * 1.9) * 0.06
	var wanted := clampf((round_elapsed / par_time) * cap * rhythm, 0.0, cap)
	rival_progress = maxf(rival_progress, wanted)
	rival_score = int(round(rival_progress * 720.0))
	var wanted_step := mini(5, int(floor(rival_progress * 6.0)))
	while rival_step < wanted_step:
		rival_step += 1
		events.append("rival_step")
	if bool(spec.get("timed_retry", false)) and rival_progress >= 0.999 and player_progress < 0.999 and not _rival_finish_sent:
		_rival_finish_sent = true
		events.append("rival_solved")
	return events


func guided_retry() -> void:
	retries += 1
	active = true
	round_elapsed = 0.0
	player_progress = 0.0
	rival_progress = 0.0
	rival_step = 0
	_last_player_progress = 0.0
	_rival_finish_sent = false
	# The revealed layout makes the rematch intentionally slower for the rival.
	spec["par_time"] = float(spec.get("par_time", 40.0)) + 12.0


func complete() -> Dictionary:
	if completed:
		return result()
	active = false
	completed = true
	player_progress = 1.0
	if is_cooperative():
		rival_progress = 1.0
		player_score += 180
		rival_score = maxi(rival_score, int(round(float(player_score) * 0.72)))
	else:
		player_score = maxi(player_score + 180, rival_score + 40)
	var par_time := maxf(10.0, float(spec.get("par_time", 80.0)))
	var speed_quality := clampf(1.0 - maxf(0.0, elapsed - par_time * 0.58) / (par_time * 0.9), 0.0, 1.0)
	var care_quality := clampf(1.0 - float(mistakes) * 0.055 - float(retries) * 0.18, 0.0, 1.0)
	var quality := speed_quality * 0.58 + care_quality * 0.42
	if quality >= 0.76:
		cheer_tier = 3
	elif quality >= 0.48:
		cheer_tier = 2
	else:
		cheer_tier = 1
	return result()


func result() -> Dictionary:
	var cheer := "WARM CHEERS"
	if cheer_tier == 2:
		cheer = "BIG CHEERS"
	elif cheer_tier >= 3:
		cheer = "STANDING OVATION"
	return {
		"tier": cheer_tier,
		"cheer": cheer,
		"player_score": player_score,
		"rival_score": rival_score,
		"elapsed": elapsed,
		"retries": retries,
		"cooperative": is_cooperative(),
	}


func time_left() -> float:
	if not bool(spec.get("timed_retry", false)):
		return -1.0
	return maxf(0.0, float(spec.get("par_time", 40.0)) - round_elapsed)


func audience_energy() -> float:
	var lead := clampf(player_progress - rival_progress + 0.5, 0.0, 1.0)
	return clampf(player_progress * 0.72 + lead * 0.28, 0.0, 1.0)
