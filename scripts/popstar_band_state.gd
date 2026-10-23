extends RefCounted
## Concert policy without a scene or reward authority. Main/caller owns s.
const BeatKit := preload("res://scripts/beat_kit.gd")

static func create(chart: Dictionary, checkpoint: Dictionary = {}, story: bool = false) -> Dictionary:
	return {"chart": chart, "section": clampi(int(checkpoint.get("section", 0)), 0, chart.sections.size() - 1),
		"beat": BeatKit.create_state(), "contacts": {}, "pending": {}, "vamps": 0,
		"last_input": 0.0, "last_invite": 0.0, "paused": false, "complete": false,
		"rehearsal_hits": [0, 0, 0], "story": story, "contest_points": [0, 0],
		"contest_losses": 0, "contest_attempt": 0, "contest_idle": false,
		"contest_resolved": false, "imp_flub_used": false, "contest_scored_epoch": -1, "restart_at": -1.0, "actions": 0, "misses": 0,
		"assists": 0, "scaffold": clampi(int(checkpoint.get("scaffold", 1)), 1, 3),
		"offset": clampf(float(checkpoint.get("offset", 0.0)), -0.12, 0.12),
		"scaffolds": _read_scaffolds(checkpoint), "finished_epoch": -1, "checkpoint_extra": checkpoint.duplicate(true)}

static func _read_scaffolds(checkpoint: Dictionary) -> Dictionary:
	var saved: Variant = checkpoint.get("scaffolds", {})
	var result: Dictionary = (saved as Dictionary).duplicate(true) if saved is Dictionary else {}
	for key: String in ["echo2", "echo3"]:
		var entry: Variant = saved.get(key, {}) if saved is Dictionary else {}
		var fallback: int = int(checkpoint.get("scaffold", 1)) if key == "echo2" else 1
		result[key] = {"level": clampi(int(entry.get("level", fallback)) if entry is Dictionary else fallback, 1, 3 if key == "echo2" else 2),
			"clean_streak": clampi(int(entry.get("clean_streak", 0)) if entry is Dictionary else 0, 0, 1)}
	return result

static func scaffold_key(s: Dictionary) -> String:
	var section: Dictionary = current(s)
	if String(section.kind) in ["echo", "contest"]:
		var patterns: Array = section.get("patterns", [])
		if not patterns.is_empty() and patterns[0].size() > 2:
			return "echo3"
	return "echo2"

static func _sync_scaffold(s: Dictionary) -> void:
	var key: String = scaffold_key(s)
	s.scaffolds[key] = {"level": int(s.beat.scaffold), "clean_streak": int(s.beat.clean_streak)}
	s.scaffold = int(s.beat.scaffold)

static func _assess_echo(s: Dictionary, b: Dictionary) -> void:
	var phrases: Dictionary = {}
	for cue: Dictionary in b.cues:
		if String(cue.role) != "answer":
			continue
		var id: String = String(cue.phrase)
		if not phrases.has(id):
			phrases[id] = [0, 0]
		phrases[id][0] += 1
		if b.results.get(String(cue.id), "") == "credited":
			phrases[id][1] += 1
	for counts: Array in phrases.values():
		BeatKit.scaffold_result(s.beat, int(counts[0]) == int(counts[1]), 3 if scaffold_key(s) == "echo3" else 2)
	if not phrases.is_empty():
		_sync_scaffold(s)

static func current(s: Dictionary) -> Dictionary:
	return s.chart.sections[int(s.section)]

static func begin(s: Dictionary) -> int:
	s.contacts = {}
	s.pending = {}
	s.last_input = 0.0
	s.last_invite = 0.0
	s.paused = false
	s.contest_idle = false
	var b: Dictionary = s.beat
	b.offset = float(s.offset)
	b.scaffold = int(s.scaffolds[scaffold_key(s)].level)
	b.clean_streak = int(s.scaffolds[scaffold_key(s)].clean_streak)
	s.scaffold = int(b.scaffold)
	var cues: Array[Dictionary] = []
	for cue: Dictionary in current(s).cues:
		cues.append(cue.duplicate(true))
	return BeatKit.start(b, cues, float(s.chart.bpm) * (0.5 if slow_contest(s) else 1.0))

static func slow_contest(s: Dictionary) -> bool:
	return String(current(s).kind) == "contest" and int(s.contest_losses) >= 2

static func input(s: Dictionary, target: int, time: float, epoch: int) -> Dictionary:
	if bool(s.paused) or bool(s.complete) or float(s.restart_at) >= 0.0:
		return {"status": "inactive", "epoch": epoch}
	var result: Dictionary = BeatKit.tap(s.beat, target, time, epoch)
	if result.status in ["stale", "invalid", "bounce", "rest"]:
		return result
	s.last_input = time
	s.contest_idle = false
	if result.status == "credited":
		# The judged touchdown only authorizes this exact strike. Actual authored
		# contact must return this epoch/cue/target before progress is committed.
		if String(current(s).kind) == "rehearsal":
			BeatKit.learn_offset(s.beat, float(result.error) + float(s.offset))
			s.offset = float(s.beat.offset)
		s.pending[String(result.cue_id)] = {"epoch": epoch, "target": target, "not_before": time, "expires": time + 0.75}
	elif result.status == "wrong":
		s.misses = int(s.misses) + 1
	return result

static func contact(s: Dictionary, cue_id: String, target: int, epoch: int, time: float) -> bool:
	if bool(s.paused) or epoch != int(s.beat.epoch) or not s.pending.has(cue_id) or s.contacts.has(cue_id):
		return false
	var pending: Dictionary = s.pending[cue_id]
	if not is_finite(time) or int(pending.epoch) != epoch or int(pending.target) != target or time < float(pending.not_before) or time > float(pending.expires):
		return false
	s.pending.erase(cue_id)
	s.contacts[cue_id] = true
	s.actions = int(s.actions) + 1
	if String(current(s).kind) == "rehearsal" and target < 3:
		s.rehearsal_hits[target] = mini(3, int(s.rehearsal_hits[target]) + 1)
	return true

static func confirmed(s: Dictionary) -> Dictionary:
	var b: Dictionary = s.beat.duplicate(true)
	for id: String in b.results.keys():
		if b.results[id] == "credited" and not s.contacts.has(id):
			b.results[id] = "no_contact"
	return b

static func finish_section(s: Dictionary, time: float) -> String:
	if bool(s.paused) or bool(s.complete) or int(s.finished_epoch) == int(s.beat.epoch):
		return "inactive"
	s.finished_epoch = int(s.beat.epoch)
	var b: Dictionary = confirmed(s)
	var kind: String = String(current(s).kind)
	var met: bool = BeatKit.section_met(b)
	if kind == "rehearsal":
		met = met and s.rehearsal_hits == [3, 3, 3]
	if bool(current(s).get("required_final", false)):
		var last: String = String(current(s).cues.back().id)
		met = met and s.contacts.has(last)
	# A band loop must not erase a waiting child's completed notes.
	if not met and int(s.beat.mercy) == 2:
		return "wait_loop"
	if kind == "contest":
		if met:
			_assess_echo(s, b)
		var outcome: String = contest_round(s, b, time)
		if not met and outcome in ["vamp", "contest_restart"]:
			BeatKit.vamp(s.beat)
			s.vamps = int(s.vamps) + 1
			_sync_scaffold(s)
		return outcome
	if not met:
		var engaged: bool = int(s.beat.clear_taps) >= 2
		BeatKit.vamp(s.beat)
		s.vamps = int(s.vamps) + 1
		s.assists = int(s.assists) + (1 if engaged else 0)
		if kind in ["echo", "rehearsal"]:
			_sync_scaffold(s)
		return "vamp"
	_assess_echo(s, b)
	return advance(s)

static func continue_wait(s: Dictionary) -> int:
	# Only verified old contacts survive. Pending animation callbacks from the
	# previous audio epoch cannot finish a new cue or strand it as consumed.
	for id: String in s.beat.results.keys():
		if s.beat.results[id] == "credited" and not s.contacts.has(id):
			s.beat.results.erase(id)
	var remaining_rest: float = maxf(0.0, float(s.beat.rest_until) - maxf(float(s.beat.clock), float(s.last_input)))
	BeatKit.cancel(s.beat)
	s.beat.clock = 0.0
	s.beat.rest_until = remaining_rest
	s.beat.wait_armed = true
	s.pending = {}
	s.last_input = 0.0
	s.last_invite = 0.0
	return int(s.beat.epoch)

static func advance(s: Dictionary) -> String:
	s.section = int(s.section) + 1
	if bool(s.story) and int(s.section) < s.chart.sections.size() and String(current(s).kind) == "contest":
		s.section = int(s.section) + 1
	if int(s.section) >= s.chart.sections.size():
		s.section = s.chart.sections.size() - 1
		s.complete = true
		BeatKit.cancel(s.beat)
		return "complete"
	s.beat.engaged_vamps = 0
	s.beat.mercy = 0
	return "advance"

static func contest_round(s: Dictionary, b: Dictionary, time: float) -> String:
	# Idle cannot grant either side a point. No input during call bars counts.
	if int(b.clear_taps) < 2:
		return "vamp"
	if int(s.contest_scored_epoch) == int(s.beat.epoch):
		return "vamp"
	s.contest_scored_epoch = int(s.beat.epoch)
	s.contest_attempt = int(s.contest_attempt) + 1
	var phrases: Dictionary = {}
	for cue: Dictionary in b.cues:
		if String(cue.role) != "answer":
			continue
		var phrase: String = String(cue.phrase)
		if not phrases.has(phrase):
			phrases[phrase] = [0, 0]
		phrases[phrase][0] += 1
		if b.results.get(String(cue.id), "") == "credited":
			phrases[phrase][1] += 1
	for counts: Array in phrases.values():
		var won: bool = int(counts[1]) >= int(counts[0]) - (1 if int(counts[0]) == 3 else 0)
		if won:
			s.contest_points[0] += 1
		elif int(s.contest_points[1]) == 2 and int(s.contest_points[1]) >= int(s.contest_points[0]) and not bool(s.imp_flub_used):
			s.imp_flub_used = true
		else:
			s.contest_points[1] += 1
		if int(s.contest_points[0]) >= 3 or int(s.contest_points[1]) >= 3 + (3 if int(s.contest_losses) >= 2 else 0):
			break
	if int(s.contest_points[0]) >= 3:
		s.contest_resolved = true
		return advance(s)
	if int(s.contest_points[1]) >= 3 + (3 if int(s.contest_losses) >= 2 else 0):
		s.contest_losses = int(s.contest_losses) + 1
		s.restart_at = time + 1.5
		return "contest_restart"
	return "vamp"

static func tick(s: Dictionary, time: float) -> String:
	if bool(s.paused) or bool(s.complete):
		return "inactive"
	if float(s.restart_at) >= 0.0:
		if time >= float(s.restart_at):
			s.restart_at = -1.0
			s.contest_points = [0, 0]
			s.contest_attempt = 0
			s.imp_flub_used = false
			return "restart"
		return "rest"
	var contest_origin: float = float(s.last_input)
	if String(current(s).kind) == "contest":
		for cue: Dictionary in s.beat.cues:
			if String(cue.role) in BeatKit.CHILD_ROLES:
				contest_origin = maxf(contest_origin,float(cue.beat)*60.0/float(s.beat.bpm))
				break
	if String(current(s).kind) == "contest" and time - contest_origin >= 4.0:
		s.contest_idle = true
		return "contest_idle"
	if time - maxf(float(s.last_input), float(s.last_invite)) >= 7.0:
		s.last_invite = time
		return "invite"
	return "playing"

static func pause(s: Dictionary) -> void:
	s.paused = true
	s.pending = {}
	BeatKit.cancel(s.beat)

static func checkpoint(s: Dictionary) -> Dictionary:
	var result: Dictionary = s.checkpoint_extra.duplicate(true)
	result.merge({"version": 1, "section": 0 if bool(s.complete) else int(s.section),
		"scaffold": int(s.scaffold), "offset": float(s.offset), "scaffolds": s.scaffolds.duplicate(true)}, true)
	return result
