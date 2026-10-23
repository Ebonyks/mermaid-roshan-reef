extends RefCounted
## Audio timing and cue judgments only. The activity owns this dictionary and
## all progress/rewards. No timer or demo callback can award a cue.
const EARLY: float = 0.20
const LATE: float = 0.32
const CHILD_ROLES: Array[String] = ["answer", "play", "lead", "finish"]

static func create_state() -> Dictionary:
	return {"epoch": 0, "clock": 0.0, "cues": [], "results": {}, "bpm": 118.0,
		"recent": [], "last_target": {}, "clear_taps": 0, "engaged_vamps": 0,
		"mercy": 0, "rest_until": 0.0, "offset": 0.0, "offset_samples": [],
		"scaffold": 1, "clean_streak": 0, "wait_armed": false}

static func start(s: Dictionary, cues: Array[Dictionary], bpm: float) -> int:
	s.epoch = int(s.epoch) + 1
	s.clock = 0.0
	s.cues = cues.duplicate(true)
	if int(s.mercy) == 1:
		var kept: Array[Dictionary] = []
		var child_index: int = 0
		for cue: Dictionary in s.cues:
			if String(cue.get("role", "")) in CHILD_ROLES:
				if child_index % 2 == 0:
					kept.append(cue)
				child_index += 1
			else:
				kept.append(cue)
		s.cues = kept
	s.results = {}
	s.bpm = bpm
	s.recent = []
	s.last_target = {}
	s.clear_taps = 0
	s.rest_until = 0.0
	s.wait_armed = false
	return int(s.epoch)

static func cancel(s: Dictionary) -> void:
	s.epoch = int(s.epoch) + 1
	s.recent = []
	s.last_target = {}

static func observe(s: Dictionary, playback: float, since_mix: float, latency: float) -> float:
	var candidate: float = playback + since_mix - latency
	if is_finite(candidate):
		s.clock = maxf(float(s.clock), candidate)
	return float(s.clock)

static func tap(s: Dictionary, target: int, audible_time: float, generation: int) -> Dictionary:
	var result: Dictionary = {"status": "offbeat", "epoch": generation, "cue_id": "", "error": 0.0, "precise": false}
	if generation != int(s.epoch):
		result.status = "stale"
		return result
	if target < 0 or target > 3 or not is_finite(audible_time):
		result.status = "invalid"
		return result
	var last: float = float(s.last_target.get(target, -1000.0))
	if audible_time - last < 0.12:
		result.status = "bounce"
		return result
	s.last_target[target] = audible_time
	var recent: Array = []
	for time: float in s.recent:
		if audible_time - time < 0.75:
			recent.append(time)
	var damped: bool = recent.size() >= 3
	recent.append(audible_time)
	s.recent = recent
	if audible_time < float(s.rest_until):
		result.status = "rest"
		return result
	var t: float = audible_time - float(s.offset)
	var early: float = 0.30 if int(s.mercy) == 1 else EARLY
	var late: float = 0.45 if int(s.mercy) == 1 else LATE
	var closest: Dictionary = {}
	var distance: float = INF
	for cue: Dictionary in s.cues:
		if String(cue.get("role", "")) not in CHILD_ROLES or s.results.has(String(cue.id)):
			continue
		var due: float = float(cue.beat) * 60.0 / float(s.bpm)
		var error: float = t - due
		# Offbeat, undamped participation on the cued instrument drives mercy.
		if not damped and int(cue.target) == target and absf(error) < distance:
			distance = absf(error)
			closest = cue
		if int(s.mercy) == 2:
			if not bool(s.wait_armed) and audible_time < 6.0 * 60.0 / float(s.bpm):
				return result
			s.wait_armed = true
			if damped:
				result.status = "damped"
				return result
			result.cue_id = String(cue.id)
			if target != int(cue.target):
				s.rest_until = audible_time + 60.0 / float(s.bpm)
				result.status = "wrong"
				return result
			s.results[String(cue.id)] = "credited"
			s.clear_taps = int(s.clear_taps) + 1
			result.status = "credited"
			return result
		if error < -early - 0.00001 or error > late + 0.00001:
			continue
		result.cue_id = String(cue.id)
		result.error = error
		result.precise = error >= -0.12 and error <= 0.18
		result.status = "damped" if damped else ("credited" if target == int(cue.target) else "wrong")
		s.results[String(cue.id)] = result.status
		if result.status == "credited":
			s.clear_taps = int(s.clear_taps) + 1
		return result
	if not closest.is_empty() and distance <= 1.0:
		s.clear_taps = int(s.clear_taps) + 1
	if damped:
		result.status = "damped"
	return result

static func credited(s: Dictionary) -> int:
	var count: int = 0
	for value: String in s.results.values():
		if value == "credited":
			count += 1
	return count

static func child_count(s: Dictionary) -> int:
	var count: int = 0
	for cue: Dictionary in s.cues:
		if String(cue.get("role", "")) in CHILD_ROLES:
			count += 1
	return count

static func section_met(s: Dictionary) -> bool:
	var count: int = child_count(s)
	if count == 0 or credited(s) < ceili(count * 0.6):
		return false
	var phrases: Dictionary = {}
	for cue: Dictionary in s.cues:
		if String(cue.get("role", "")) != "answer":
			continue
		var phrase: String = String(cue.get("phrase", "answer"))
		if not phrases.has(phrase):
			phrases[phrase] = [0, 0]
		phrases[phrase][0] += 1
		if s.results.get(String(cue.id), "") == "credited":
			phrases[phrase][1] += 1
	for counts: Array in phrases.values():
		if int(counts[1]) < int(counts[0]) - (1 if int(counts[0]) == 3 else 0):
			return false
	return true

static func vamp(s: Dictionary) -> void:
	if int(s.clear_taps) >= 2:
		s.engaged_vamps = int(s.engaged_vamps) + 1
		s.mercy = mini(2, int(s.engaged_vamps) / 2)
	s.scaffold = maxi(1, int(s.scaffold) - 1)
	s.clean_streak = 0
	s.clear_taps = 0

static func scaffold_result(s: Dictionary, clean: bool, notes: int) -> void:
	if not clean:
		s.scaffold = maxi(1, int(s.scaffold) - 1)
		s.clean_streak = 0
		return
	s.clean_streak = int(s.clean_streak) + 1
	if int(s.clean_streak) >= 2:
		s.scaffold = mini(2 if notes > 2 else 3, int(s.scaffold) + 1)
		s.clean_streak = 0

static func learn_offset(s: Dictionary, signed_error: float) -> void:
	if not is_finite(signed_error):
		return
	s.offset_samples.append(signed_error)
	if s.offset_samples.size() > 24:
		s.offset_samples.pop_front()
	if s.offset_samples.size() < 6:
		return
	var errors: Array = s.offset_samples.duplicate()
	errors.sort()
	var middle: int = errors.size() / 2
	var median: float = float(errors[middle])
	if errors.size() % 2 == 0:
		median = (median + float(errors[middle - 1])) * 0.5
	s.offset = clampf(median, -0.12, 0.12)

static func validate_cues(cues: Array[Dictionary], bpm: float) -> Array[String]:
	var errors: Array[String] = []
	var previous: float = -INF
	var ids: Dictionary = {}
	if bpm <= 0.0 or not is_finite(bpm):
		errors.append("invalid BPM")
		return errors
	for cue: Dictionary in cues:
		var id: String = String(cue.get("id", ""))
		var beat: float = float(cue.get("beat", -1.0))
		if id.is_empty() or ids.has(id):
			errors.append("missing/duplicate cue id")
		ids[id] = true
		if beat < 0.0 or not is_equal_approx(beat * 2.0, roundf(beat * 2.0)):
			errors.append("off-grid cue")
		if String(cue.get("role", "")) not in CHILD_ROLES and String(cue.get("role", "")) not in ["call", "count_in"]:
			errors.append("unknown role")
		if int(cue.get("target", -1)) == 3 and String(cue.get("role", "")) != "lead":
			errors.append("microphone outside crowd lead")
		if int(cue.get("target", -1)) not in [0, 1, 2, 3]:
			errors.append("unknown target")
		if String(cue.get("role", "")) in CHILD_ROLES:
			var due: float = beat * 60.0 / bpm
			if beat < 6.0:
				errors.append("child cue before count-in plus two beats")
			if due - previous < EARLY + LATE - 0.00001:
				errors.append("overlapping child windows")
			previous = due
	return errors
