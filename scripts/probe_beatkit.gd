extends SceneTree
## Real clock/judging negatives; no reward authority in the timing helper.
const BeatKit := preload("res://scripts/beat_kit.gd")
var failures: int = 0
func _initialize() -> void:
	var cues: Array[Dictionary] = [{"id": "one", "beat": 4.0, "target": 0, "role": "play"}, {"id": "two", "beat": 6.0, "target": 1, "role": "play"}]
	var half_clock: Dictionary = BeatKit.create_state()
	_check("half-tempo clock uses elapsed audible seconds",is_equal_approx(BeatKit.observe(half_clock,0.4/0.5,0.03,0.08),0.75))
	var s: Dictionary = BeatKit.create_state()
	var epoch: int = BeatKit.start(s, cues, 120.0)
	_check("latency-corrected clock", is_equal_approx(BeatKit.observe(s, 2.0, 0.03, 0.08), 1.95))
	_check("monotonic within epoch", is_equal_approx(BeatKit.observe(s, 1.8, 0.0, 0.0), 1.95))
	_check("wrong first tap owns cue", BeatKit.tap(s, 2, 2.0, epoch).status == "wrong")
	_check("cannot rescue consumed cue", BeatKit.tap(s, 0, 2.01, epoch).status == "offbeat")
	_check("late asymmetry credits", BeatKit.tap(s, 1, 3.30, epoch).status == "credited")
	var next_epoch: int = BeatKit.start(s, cues, 120.0)
	_check("restart opens epoch and resets time", next_epoch > epoch and s.clock == 0.0)
	_check("stale callback cannot credit", BeatKit.tap(s, 0, 2.0, epoch).status == "stale")
	_check("early boundary credits", BeatKit.tap(s, 0, 1.8, next_epoch).status == "credited")
	_check("bounce ignored", BeatKit.tap(s, 0, 1.85, next_epoch).status == "bounce")
	BeatKit.start(s, cues, 120.0)
	for t: float in [1.4, 1.6, 1.8]:
		BeatKit.tap(s, 2, t, int(s.epoch))
	_check("fourth tap damped", BeatKit.tap(s, 1, 2.0, int(s.epoch)).status == "damped")
	BeatKit.start(s, cues, 120.0)
	BeatKit.tap(s, 0, 2.6, int(s.epoch))
	BeatKit.tap(s, 1, 3.6, int(s.epoch))
	_check("engaged late child counts clear play", int(s.clear_taps) == 2 and BeatKit.credited(s) == 0)
	for attempt: int in range(4):
		s.clear_taps = 2
		BeatKit.vamp(s)
	_check("four engaged vamps reach waiting mercy", int(s.mercy) == 2)
	BeatKit.start(s, cues, 120.0)
	_check("waiting cue accepts deliberate late hit", BeatKit.tap(s, 0, 20.0, int(s.epoch)).status == "credited")
	_check("waiting wrong target makes rest", BeatKit.tap(s, 2, 21.0, int(s.epoch)).status == "wrong")
	_check("rest blocks immediate correction", BeatKit.tap(s, 1, 21.2, int(s.epoch)).status == "rest")
	_check("waiting next target remains", BeatKit.tap(s, 1, 21.6, int(s.epoch)).status == "credited")
	var idle: Dictionary = BeatKit.create_state()
	BeatKit.start(idle, cues, 120.0)
	for attempt: int in range(8):
		BeatKit.vamp(idle)
	_check("idle never unlocks mercy", int(idle.mercy) == 0)
	_check("zero input never credits", BeatKit.credited(idle) == 0)
	for error: float in [0.3, 0.28, 0.32, 0.27, 0.29, 0.31]:
		BeatKit.learn_offset(idle, error)
	_check("learned offset requires six and clamps", is_equal_approx(float(idle.offset), 0.12))
	_check("source chart rejects overlapping windows", not BeatKit.validate_cues([{"id":"a", "beat":4.0,"target":0,"role":"play"}, {"id":"b","beat":4.5,"target":1,"role":"play"}],120.0).is_empty())
	_check("source chart accepts spaced grid", BeatKit.validate_cues([{"id":"x","beat":6.0,"target":0,"role":"play"}, {"id":"y","beat":8.0,"target":1,"role":"play"}],120.0).is_empty())
	print("BEATKIT|result: %s" % ("ALL OK" if failures == 0 else "%d FAIL" % failures))
	quit(0 if failures == 0 else 1)
func _check(label: String, ok: bool) -> void:
	print("BEATKIT|%s: %s" % [label, "OK" if ok else "FAIL"])
	if not ok:
		failures += 1

