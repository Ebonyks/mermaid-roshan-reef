extends SceneTree
## Deterministic concert policy probe. This is model evidence, not proof of art contact.
const Band := preload("res://scripts/popstar_band_state.gd")
const BeatKit := preload("res://scripts/beat_kit.gd")
var failures: int = 0
func _initialize() -> void:
	var chart: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/audio/music/popstar_concert/chart.json")) as Dictionary
	_check("nine musical sections with source hashes", chart.sections.size() == 9 and String(chart.score_sha256).length() == 64)
	for section: Dictionary in chart.sections:
		var cues: Array[Dictionary] = []
		for cue: Dictionary in section.cues:
			cues.append(cue)
		_check("valid generated chart: " + String(section.id), BeatKit.validate_cues(cues, float(chart.bpm)).is_empty())
	var s: Dictionary = Band.create(chart)
	var epoch: int = Band.begin(s)
	for loop: int in range(12):
		_check("idle section never completes", Band.finish_section(s, 120.0) == "vamp" and int(s.section) == 0 and not bool(s.complete))
		Band.begin(s)
	_check("idle cannot escalate mercy", int(s.beat.mercy) == 0)
	_check("idle gets invitation", Band.tick(s, 7.1) == "invite")
	s = Band.create(chart)
	epoch = Band.begin(s)
	var first: Dictionary = s.beat.cues[0]
	var time: float = float(first.beat) * 60.0 / float(chart.bpm)
	var result: Dictionary = Band.input(s, int(first.target), time, epoch)
	_check("touchdown is provisional until actual contact", result.status == "credited" and int(s.actions) == 0)
	_check("wrong physical target cannot commit", not Band.contact(s, String(first.id), 2, epoch, time + 0.1))
	_check("contact cannot precede its touchdown",not Band.contact(s,String(first.id),int(first.target),epoch,time-0.1))
	_check("matching authored contact commits once", Band.contact(s, String(first.id), int(first.target), epoch, time + 0.1) and not Band.contact(s, String(first.id), int(first.target), epoch, time + 0.12))
	Band.pause(s)
	_check("pause cancels stale contact/input", not Band.contact(s, String(first.id), int(first.target), epoch, time + 0.2) and Band.input(s,0,time,epoch).status == "inactive")
	Band.begin(s)
	_check("resume new epoch", int(s.beat.epoch) > epoch)
	# Every actual child cue is touched and confirmed, including a deliberate final crash.
	s = Band.create(chart, {}, true)
	var steps: int = 0
	while not bool(s.complete) and steps < 20:
		epoch = Band.begin(s)
		for cue: Dictionary in s.beat.cues:
			if String(cue.role) not in BeatKit.CHILD_ROLES:
				continue
			time = float(cue.beat) * 60.0 / float(chart.bpm) + 0.15
			result = Band.input(s, int(cue.target), time, epoch)
			_check("intentional cue: " + String(cue.id), result.status == "credited" and Band.contact(s,String(cue.id),int(cue.target),epoch,time + 0.05))
		_check("intentional section advances without vamp", Band.finish_section(s,time+1.0) in ["advance", "complete"])
		var saved: Dictionary = Band.checkpoint(s)
		var restored: Dictionary = Band.create(chart,saved,true)
		_check("section/scaffold checkpoint round trip", int(restored.section) == int(saved.section) and int(restored.scaffold) == int(saved.scaffold))
		steps += 1
	_check("story deliberately completes without imp", bool(s.complete) and int(s.contest_attempt) == 0 and int(s.vamps) == 0)
	_check("credited rehearsal learns and clamps signed offset",is_equal_approx(float(s.offset),0.12))
	# A child consistently .6s late must reach waiting mercy; idle never does.
	s = Band.create(chart)
	for attempt: int in range(4):
		epoch = Band.begin(s)
		for cue: Dictionary in s.beat.cues:
			if String(cue.role) in BeatKit.CHILD_ROLES:
				time = float(cue.beat)*60.0/float(chart.bpm)+0.6
				Band.input(s,int(cue.target),time,epoch)
		Band.finish_section(s,time+1.0)
	_check("engaged late child reaches wait after four vamps", int(s.beat.mercy) == 2)
	epoch = Band.begin(s)
	for cue: Dictionary in s.beat.cues:
		if String(cue.role) in BeatKit.CHILD_ROLES:
			time += 1.0
			result = Band.input(s,int(cue.target),time,epoch)
			Band.contact(s,String(cue.id),int(cue.target),epoch,time+0.05)
	_check("waiting mode completes with own contacts", Band.finish_section(s,time+1.0) == "advance")
	s = Band.create(chart,{"section":7})
	Band.begin(s)
	_check("contest idle unresolved", Band.tick(s,11.0) == "contest_idle" and Band.finish_section(s,20.0) == "vamp" and s.contest_points == [0,0])
	for loss: int in range(2):
		for attempt: int in range(5):
			Band.begin(s)
			s.beat.clear_taps = 2
			var outcome: String = Band.finish_section(s,20.0)
			if outcome == "contest_restart":
				_check("contest-only restart within two seconds", Band.tick(s,21.5) == "restart" and int(s.section) == 7)
				break
	_check("two losses enable half time", Band.slow_contest(s) and int(s.contest_losses) == 2)
	# A slow waiting child retains verified notes across audio epochs.
	s = Band.create(chart,{"section":2})
	s.beat.mercy = 2
	epoch = Band.begin(s)
	var waiting_cues: Array = s.beat.cues.duplicate(true)
	for index: int in range(2):
		var cue: Dictionary = waiting_cues[index]
		time = 8.0+index
		Band.input(s,int(cue.target),time,epoch)
		Band.contact(s,String(cue.id),int(cue.target),epoch,time+0.1)
	_check("partial waiting section keeps playing without reset",Band.finish_section(s,13.0) == "wait_loop")
	var retained: int = int(s.actions)
	var before_loop_epoch: int = epoch
	epoch = Band.continue_wait(s)
	_check("new audio epoch retains only verified wait contacts",epoch > before_loop_epoch and s.contacts.size()==2 and int(s.actions)==retained)
	_check("old epoch cannot commit after audio loop",not Band.contact(s,String(waiting_cues[1].id),int(waiting_cues[1].target),before_loop_epoch,1.0))
	for index: int in range(2,waiting_cues.size()):
		var cue: Dictionary = waiting_cues[index]
		time = 1.0+index
		Band.input(s,int(cue.target),time,epoch)
		Band.contact(s,String(cue.id),int(cue.target),epoch,time+0.1)
	_check("slow waiting child finishes after a preserved loop",Band.finish_section(s,13.0)=="advance")
	_check("one epoch cannot complete two sections",Band.finish_section(s,13.1)=="inactive" and int(s.section)==3)
	# Echo skills advance on phrases; choruses cannot train memory.
	s = Band.create(chart,{"section":1})
	epoch = Band.begin(s)
	for cue: Dictionary in s.beat.cues:
		if String(cue.role)=="answer":
			time = float(cue.beat)*60.0/float(chart.bpm)
			Band.input(s,int(cue.target),time,epoch)
			Band.contact(s,String(cue.id),int(cue.target),epoch,time+0.05)
	Band.finish_section(s,13.0)
	_check("two clean echo phrases raise only echo2",int(s.scaffolds.echo2.level)==2 and int(s.scaffolds.echo3.level)==1)
	epoch = Band.begin(s)
	for cue: Dictionary in s.beat.cues:
		if String(cue.role) in BeatKit.CHILD_ROLES:
			time = float(cue.beat)*60.0/float(chart.bpm)
			Band.input(s,int(cue.target),time,epoch)
			Band.contact(s,String(cue.id),int(cue.target),epoch,time+0.05)
	Band.finish_section(s,13.0)
	_check("a clean chorus cannot raise echo difficulty",int(s.scaffolds.echo2.level)==2 and int(s.scaffolds.echo2.clean_streak)==0)
	var skills_save: Dictionary = Band.checkpoint(s)
	var skills_restored: Dictionary = Band.create(chart,skills_save)
	_check("per-skill scaffold checkpoint survives re-entry",skills_restored.scaffolds==s.scaffolds)
	var future: Dictionary = {"section":1,"future_key":{"keep":77},"scaffolds":{"future_skill":{"keep":88}}}
	var future_state: Dictionary = Band.create(chart,future)
	var future_saved: Dictionary = Band.checkpoint(future_state)
	_check("checkpoint preserves unknown future save keys",future_saved.future_key==future.future_key and future_saved.scaffolds.future_skill==future.scaffolds.future_skill)
	for route: int in range(4):
		var mash: Dictionary = Band.create(chart)
		var mash_epoch: int = Band.begin(mash)
		var wins: int = 0
		for n: int in range(600):
			var mash_target: int = n % 3 if route == 3 else route
			var judged: Dictionary = Band.input(mash,mash_target,n*0.2,mash_epoch)
			if judged.status == "credited":
				wins += 1
				Band.contact(mash,String(judged.cue_id),mash_target,mash_epoch,n*0.2+0.02)
		_check("5Hz route %d cannot farm cues" % route,wins <= 1 and int(mash.actions) <= 1 and Band.finish_section(mash,120.0) == "vamp")
	print("POPSTARBAND|result: %s" % ("ALL OK" if failures == 0 else "%d FAIL" % failures))
	quit(0 if failures == 0 else 1)
func _check(label: String, ok: bool) -> void:
	print("POPSTARBAND|%s: %s" % [label, "OK" if ok else "FAIL"])
	if not ok:
		failures += 1
