extends SceneTree
## Reef of Light Opera career playthrough harness (audit-local, untracked).
##
## Run:  godot --path . [--headless --fixed-fps 60] -s res://audit_local/reef_play.gd -- \
##         career=boxer policy=child_sim seed=3 out=/abs/dir mode=fast max_seconds=600
## Prefer the wrapper /home/claude/audit_work/harness/reef_play.sh (isolates user://).
##
## Every input is a real InputEventScreenTouch / InputEventScreenDrag fed to
## Input.parse_input_event() at window coordinates, so it travels the same
## path as a finger (viewport GUI routing, touch->mouse emulation, hit tests).
## The policy only READS game state to decide where a finger would go.

const GeologySurfaceScript := preload("res://scripts/opera_geology_surface.gd")
const TeacherSurfaceScript := preload("res://scripts/opera_teacher_surface.gd")
const BalletSurfaceScript := preload("res://scripts/opera_ballet_surface.gd")

const POLICIES := ["expert", "child_sim", "slow", "random_tapper", "idle"]
const CANVAS := Vector2(1280.0, 720.0)
const DEAD_TOUCH_WINDOW := 0.40
## Surface fields whose change means the touch visibly moved/changed something
## (a carried piece, a placed tile, a glove following the finger...). Pure
## timers are excluded so a decaying old effect is not mistaken for a response.
const VISIBLE_STATE_PROPS := [
	"farm_flying", "farm_dragging", "farm_landed", "pour_hold", "pour_x", "trace_journey",
	"widget_fill", "candy_position", "garden_planted", "clue_index", "pipe_drag_tile",
	"pipe_grid", "pipe_tray_sel", "ribbon_progress", "twirl_progress", "pose_round", "counted",
	"joined", "river_wet", "fossil_cleared", "fossil_snapped", "fossil_drag_piece",
	"pan_reversals", "geode_seams", "geode_pull", "race_steer", "race_started",
	"glove_positions", "tap_marks", "xray_found_count", "oven_done", "echo_input_i",
	"dance_input_index", "crank_rotation", "wrong_attempts", "selected",
]
const PERIODIC_FRAME_S := 3.0


class Clock extends Node:
	var t := 0.0
	var last_delta := 0.0
	func _process(delta: float) -> void:
		t += delta
		last_delta = delta


## Wraps the game's AudioDirector so every voice/message/sfx request is logged
## before the real implementation runs.
class VoiceTap extends AudioDirector:
	var sink: Callable
	func _init(main_ref: ReefMain) -> void:
		super(main_ref)
	func _say(speaker: String, event: String = "", min_gap: float = 0.0) -> void:
		if sink.is_valid():
			sink.call("say", speaker, event, "")
		super(speaker, event, min_gap)
	func show_msg(who: String, txt: String, vo: String = "talk",
			voice_min_gap: float = 0.5) -> void:
		if sink.is_valid():
			sink.call("msg", who, vo, txt)
		super(who, txt, vo, voice_min_gap)
	func say_sequence(lines: Array, opening_hold: float = 0.0) -> void:
		if sink.is_valid():
			sink.call("sequence", "", str(lines.size()) + " lines", str(lines).left(300))
		super(lines, opening_hold)
	func sfx(name: String, pitch: float = 1.0, volume_db: float = -6.0) -> void:
		if sink.is_valid():
			sink.call("sfx", "", name, "")
		super(name, pitch, volume_db)
	func play_success_yay(pitch_scale: float = 1.0) -> void:
		if sink.is_valid():
			sink.call("yay", "", "success_yay", "")
		super(pitch_scale)


var cfg := {
	"career": "chef", "policy": "expert", "seed": 1, "out": "",
	"mode": "fast", "max_seconds": 600.0, "input": "finger",
}
var rng := RandomNumberGenerator.new()
var clock: Clock
var main: ReefMain
var house: OperaHouse
var act: OperaAct
var world: OperaCareerWorld2D
var act_index := -1
var career_key := ""
var career_name := ""
var rendered := false
var frames_dir := ""

# input executor
var action: Dictionary = {}
var next_ready_t := 0.0
var finger_down := false
var last_touch_t := -99.0
var last_finger_vp := Vector2(-1, -1)
var total_inputs := 0
var total_moves := 0
var dead_touches := 0
var pending_touches: Array = []

# observation
var phases: Array = []
var cur_phase: Dictionary = {}
var phase_seq := 0
var last_phase_key := ""
var last_task_open := false
var last_advance_pending := false
var last_idle_t := 0.0
var last_demo_t := 0.0
var last_surface_id := 0
var last_assist_level := 0
var last_teacher_assisted := false
var last_retries := 0
var last_interaction_requested := false
var last_lens_hint := -1
var gesture_count := 0
var sound_starts := 0
var progress_events := 0
var voice_lines: Array = []
var audio_starts: Array = []
var events: Array = []
var problems: Array = []
var frames: Array = []
var audio_players: Array = []
var audio_state: Dictionary = {}
var no_input_span_start := -1.0
var longest_wait := {"seconds": 0.0, "start_s": 0.0, "phase": ""}
var no_input_total := 0.0
var won_t := -1.0
var house_done := false
var house_completed := false
var finished := false
var last_periodic_frame := -99.0
var pending_captures: Array = []
var save_info: Dictionary = {}
var stuck_flagged: Dictionary = {}
var phase_last_progress_t := 0.0
var phase_progress_sig := ""
var started_wall_ms := 0
var capture_ms := 0
var hover_probe_done := false
var voice_carry: Array = []


func _init() -> void:
	_parse_args()
	rng.seed = int(cfg["seed"])
	seed(int(cfg["seed"]))
	started_wall_ms = Time.get_ticks_msec()
	rendered = String(cfg["mode"]) == "rendered" and DisplayServer.get_name() != "headless"
	if String(cfg["mode"]) == "rendered" and not rendered:
		problems.append("mode=rendered requested but display server is headless; no frames")
	var out := String(cfg["out"])
	DirAccess.make_dir_recursive_absolute(out)
	frames_dir = out.path_join("frames")
	if rendered:
		DirAccess.make_dir_recursive_absolute(frames_dir)
	if String(cfg["input"]) == "touch_only":
		# Diagnostic path: no OS touch->mouse emulation (NOT what a tablet does).
		Input.emulate_mouse_from_touch = false
	if not _resolve_career():
		_fail_early("unknown career '%s'" % String(cfg["career"]))
		return
	clock = Clock.new()
	clock.process_priority = -1000
	clock.process_mode = Node.PROCESS_MODE_ALWAYS
	get_root().add_child(clock)
	node_added.connect(_on_node_added)
	save_info = _save_probe("before")
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	var tap := VoiceTap.new(main)
	tap.sink = Callable(self, "_on_voice")
	main._audio_dir = tap
	get_root().add_child(main)
	await process_frame
	_fix_headless_root()
	await process_frame
	_fix_headless_root()
	main.day_one_active = false
	main._skip_intro()
	if main.start_menu_active:
		# Display builds open the title menu (CanvasLayer 20) on top of
		# everything; headless builds never do. Dismiss it exactly as its own
		# Continue path does, without launching a save.
		main._start_menu_ref()._dismiss_menu()
		_event("start_menu_dismissed")
	main.game = "opera"
	house = OperaHouse.new()
	get_root().add_child(house)
	var ok := house.start(main, act_index, Callable(self, "_on_house_done"), {},
		{"reward_policy": "dev_playtest"})
	if not ok or house.act == null:
		_fail_early("OperaHouse.start failed for %s" % career_key)
		return
	act = house.act
	world = act.career_world_2d
	if world == null:
		_fail_early("career has no OperaCareerWorld2D")
		return
	_event("start", {"phases": world.phases.size(), "dev_playtest": true,
		"window": DisplayServer.window_get_size(), "root": get_root().size,
		"screen_xform": str(get_root().get_screen_transform())})
	await _run_loop()


var audio_sync_wall := -1.0
var audio_sync_game := 0.0


## Fast mode runs game time faster than the wall clock, but the (dummy) audio
## driver plays streams in wall time. Scale global playback speed to the
## measured game/wall ratio so voice lines last their game-time length and
## "is speech still playing" gates behave as on a device.
func _sync_audio_clock(now: float) -> void:
	if rendered and not OS.get_cmdline_args().has("--fixed-fps"):
		return
	var wall := float(Time.get_ticks_usec()) / 1000000.0
	if audio_sync_wall < 0.0:
		audio_sync_wall = wall
		audio_sync_game = now
		return
	if wall - audio_sync_wall >= 0.25:
		var ratio := (now - audio_sync_game) / maxf(0.001, wall - audio_sync_wall)
		AudioServer.playback_speed_scale = clampf(ratio, 0.05, 64.0)
		audio_sync_wall = wall
		audio_sync_game = now


func _fix_headless_root() -> void:
	# Headless reports a 64x64 window; give the root the real 1280x720 canvas
	# so layout and coordinate mapping match the game on a device.
	if DisplayServer.get_name() == "headless" and get_root().size != Vector2i(1280, 720):
		get_root().size = Vector2i(1280, 720)


func _parse_args() -> void:
	for raw: String in OS.get_cmdline_user_args():
		var arg := raw.trim_prefix("--")
		var eq := arg.find("=")
		if eq < 0:
			continue
		var key := arg.left(eq).strip_edges()
		var value := arg.substr(eq + 1).strip_edges()
		if key == "out_dir":
			key = "out"
		match key:
			"seed":
				cfg["seed"] = int(value)
			"max_seconds":
				cfg["max_seconds"] = float(value)
			_:
				cfg[key] = value
	if String(cfg["policy"]) not in POLICIES:
		push_error("unknown policy %s" % cfg["policy"])
		cfg["policy"] = "expert"
	if String(cfg["out"]).is_empty():
		cfg["out"] = "/tmp/reef_play_%s_%s_%d" % [cfg["career"], cfg["policy"], int(cfg["seed"])]


func _norm(text: String) -> String:
	return text.to_lower().replace(" ", "").replace("_", "").replace("-", "")


func _resolve_career() -> bool:
	var want := _norm(String(cfg["career"]))
	var aliases := {"stuffiesurgeon": "doctor", "surgeon": "doctor", "pastry": "chef",
		"racecar": "racer", "racecardriver": "racer", "driver": "racer",
		"nurse": "nursery", "nurserynurse": "nursery", "astronautengineer": "astronaut",
		"engineer": "astronaut", "candy": "candymaker", "popstar": "popstar"}
	if aliases.has(want):
		want = String(aliases[want])
	for index: int in OperaHouse.LIVE_ACT_INDICES:
		var entry: Dictionary = OperaHouse.ACTS[index]
		var keys := [_norm(String(entry.get("costume", ""))), _norm(String(entry.get("career", ""))),
			_norm(String(entry.get("name", "")))]
		if want in keys:
			act_index = index
			career_key = String(entry.get("costume", ""))
			career_name = String(entry.get("career", ""))
			return true
	return false


func _fail_early(reason: String) -> void:
	problems.append(reason)
	push_error("REEF_PLAY|" + reason)
	_write_json(false)
	quit(2)


# ---------------------------------------------------------------- main loop

func _run_loop() -> void:
	var max_s := float(cfg["max_seconds"])
	while not finished:
		await process_frame
		_fix_headless_root()
		var now := clock.t
		_sync_audio_clock(now)
		_poll_audio(now)
		_observe(now)
		_resolve_dead_touches(now)
		if won_t < 0.0 and act != null and is_instance_valid(act) and act.state == "won":
			won_t = now
			_finish_wait_span(now)
			_close_phase(now, "won")
			_event("won", {"result": str(act.performance_result)})
			_release_finger()
			action = {}
			_request_capture("finale", now + 2.0)
		if won_t < 0.0 and not house_done:
			_drive(now)
		if rendered:
			if now - last_periodic_frame >= PERIODIC_FRAME_S:
				last_periodic_frame = now
				_capture("tick")
			_service_captures(now)
		if won_t >= 0.0 and now >= won_t + 2.6:
			finished = true
		elif house_done and won_t < 0.0:
			problems.append("house finished without a win")
			finished = true
		elif now >= max_s:
			_event("timeout", {"max_seconds": max_s})
			finished = true
	_close_phase(clock.t, "end")
	_release_finger()
	if won_t < 0.0:
		_finish_wait_span(clock.t)
	await process_frame
	var completed := won_t >= 0.0
	save_info.merge(_save_probe("after"), true)
	_write_json(completed)
	if house != null and is_instance_valid(house) and not house_done:
		house._leave_early()
	await process_frame
	print("REEF_PLAY|done career=%s policy=%s completed=%s seconds=%.1f inputs=%d phases=%d" % [
		career_key, cfg["policy"], completed, won_t if completed else clock.t,
		total_inputs, phases.size()])
	quit(0)


func _on_house_done(completed: bool) -> void:
	house_done = true
	house_completed = completed


# ------------------------------------------------------------ observation

func _phase_dict() -> Dictionary:
	if world == null or not is_instance_valid(world):
		return {}
	if world.phase_index < 0 or world.phase_index >= world.phases.size():
		return {}
	return world.phases[world.phase_index] as Dictionary


func _phase_key() -> String:
	if world == null or not is_instance_valid(world):
		return ""
	var retries := act.competition.retries if act != null and act.competition != null else 0
	return "%d/%d" % [world.phase_index, retries]


func _open_phase(now: float) -> void:
	var phase := _phase_dict()
	phase_seq += 1
	cur_phase = {
		"n": phase_seq, "index": world.phase_index,
		"name": String(phase.get("name", "?")), "mode": String(phase.get("mode", "?")),
		"part": String(phase.get("performance_part", "")),
		"finale": world.phase_index >= world._finale_start(),
		"start_s": snappedf(now, 0.01), "open_s": -1.0, "end_s": -1.0,
		"inputs": 0, "drag_moves": 0, "dead_touches": 0, "hints": 0,
		"assists_or_mercy_events": 0, "hint_events": [], "assist_events": [],
		"voice": [], "outcome": "",
	}
	phases.append(cur_phase)
	(cur_phase["voice"] as Array).append_array(voice_carry)
	voice_carry.clear()
	phase_last_progress_t = now
	phase_progress_sig = ""


func _close_phase(now: float, outcome: String) -> void:
	if cur_phase.is_empty() or float(cur_phase["end_s"]) >= 0.0:
		return
	cur_phase["end_s"] = snappedf(now, 0.01)
	cur_phase["outcome"] = outcome
	cur_phase["seconds"] = snappedf(now - float(cur_phase["start_s"]), 0.01)


func _observe(now: float) -> void:
	if world == null or not is_instance_valid(world) or won_t >= 0.0:
		return
	var key := _phase_key()
	if key != last_phase_key:
		last_task_open = false  # a phase that starts already open still counts as opened
		if not cur_phase.is_empty() and float(cur_phase["end_s"]) < 0.0:
			var outcome := "completed"
			if act.competition != null and act.competition.retries > last_retries:
				outcome = "rival_solved_guided_retry"
			_close_phase(now, outcome)
		last_phase_key = key
		if world.phase_index < world.phases.size():
			_open_phase(now)
			_event("phase_armed", {"phase": cur_phase["name"], "index": world.phase_index})
	if cur_phase.is_empty():
		return
	# task open
	if world.task_open and not last_task_open and float(cur_phase["open_s"]) < 0.0:
		cur_phase["open_s"] = snappedf(now, 0.01)
		_event("phase_open", {"phase": cur_phase["name"]})
		_request_capture("p%02d_open_%s" % [int(cur_phase["n"]), _slug(cur_phase["name"])], now + 0.6)
	last_task_open = world.task_open
	# completion
	if world.phase_advance_pending and not last_advance_pending:
		_event("phase_complete", {"phase": cur_phase["name"]})
		_request_capture("p%02d_done_%s" % [int(cur_phase["n"]), _slug(cur_phase["name"])], now + 0.15)
		_close_phase(now, "completed")
	last_advance_pending = world.phase_advance_pending
	# surface tracking
	var s: Variant = world.surface
	if s != null and is_instance_valid(s) and s.get_instance_id() != last_surface_id:
		last_surface_id = s.get_instance_id()
		for sig: String in ["gesture", "race_event", "progress_changed", "lesson_completed",
				"counter_touched"]:
			if s.has_signal(sig) and not s.is_connected(sig, _on_any_signal):
				s.connect(sig, _on_any_signal)
		last_demo_t = float(s.get("demo_t")) if s.get("demo_t") != null else 0.0
		last_assist_level = int(s.get("_assist_level")) if s.get("_assist_level") != null else 0
		last_teacher_assisted = bool(s.get("assisted")) if s.get("assisted") != null else false
	if world.nursery_catch != null and is_instance_valid(world.nursery_catch):
		for sig2: String in ["baby_caught", "baby_missed"]:
			if world.nursery_catch.has_signal(sig2) \
					and not world.nursery_catch.is_connected(sig2, _on_any_signal):
				world.nursery_catch.connect(sig2, _on_any_signal)
	var recent_input := now - last_touch_t < 0.35 or finger_down
	# idle re-hints and room assists (career world)
	var idle := world.idle_t
	var hinted_this_frame := false
	if world.active and not world.phase_advance_pending:
		if not world.task_open:
			if last_idle_t < 9.0 and idle >= 9.0:
				_hint(now, "room_reprompt_9s")
				hinted_this_frame = true
			if last_idle_t >= 19.5 and idle < 10.0 and not recent_input:
				_assist(now, "auto_walk_to_station_20s")
		elif last_idle_t > 5.0 and idle < 0.5 and not recent_input:
			_hint(now, "idle_rehint_%.0fs" % last_idle_t)
			hinted_this_frame = true
	last_idle_t = idle
	if s != null and is_instance_valid(s):
		var demo_v: Variant = s.get("demo_t")
		if demo_v != null:
			var demo_t := float(demo_v)
			if demo_t + 0.02 < last_demo_t and not hinted_this_frame \
					and float(cur_phase["open_s"]) >= 0.0 and now - float(cur_phase["open_s"]) > 0.5:
				_hint(now, "touch_rehint" if recent_input else "surface_rehint")
			last_demo_t = demo_t
		var assist_v: Variant = s.get("_assist_level")
		if assist_v != null:
			if int(assist_v) > last_assist_level:
				_assist(now, "assist_level_%d" % int(assist_v))
			last_assist_level = int(assist_v)
		var assisted_v: Variant = s.get("assisted")
		if assisted_v != null and s.get_script() == TeacherSurfaceScript:
			if bool(assisted_v) and not last_teacher_assisted:
				_assist(now, "teacher_help_shown")
			last_teacher_assisted = bool(assisted_v)
	if world.lens_hint_target >= 0 and last_lens_hint < 0:
		_hint(now, "lens_glisten_12s")
	last_lens_hint = world.lens_hint_target
	if act.competition != null:
		if act.competition.retries > last_retries:
			_assist(now, "guided_retry_after_rival_win")
		last_retries = act.competition.retries
	if world.interaction_requested and not last_interaction_requested and not recent_input \
			and not world.task_open:
		_event("auto_interaction", {"phase": cur_phase["name"]})
	last_interaction_requested = world.interaction_requested
	# progress signature for stuck detection
	var sig := "%d|%.3f|%s|%d" % [world.phase_index, world.phase_progress,
		str(world.task_open), gesture_count]
	if s != null and is_instance_valid(s) and s.has_method("progress"):
		sig += "|%.3f" % float(s.progress())
	if sig != phase_progress_sig:
		phase_progress_sig = sig
		phase_last_progress_t = now
	if now - phase_last_progress_t > 25.0 and not stuck_flagged.has(key):
		stuck_flagged[key] = true
		var info := _debug_state()
		info["phase"] = String(cur_phase.get("name", ""))
		info["task_open"] = world.task_open
		info["input_possible"] = _input_possible()
		_event("stuck", info)
		problems.append("no progress for 25 s in %s (%s)%s" % [cur_phase.get("name", ""),
			cur_phase.get("mode", ""), "" if _policy() in ["expert", "child_sim"] else " [expected for this policy]"])
	# no-input-possible spans (tracked until the win; the curtain call is excluded)
	if won_t >= 0.0:
		return
	if _input_possible():
		_finish_wait_span(now)
	elif no_input_span_start < 0.0:
		no_input_span_start = now


func _finish_wait_span(now: float) -> void:
	if no_input_span_start < 0.0:
		return
	var span := now - no_input_span_start
	no_input_total += span
	if span > float(longest_wait["seconds"]):
		longest_wait = {"seconds": snappedf(span, 0.01), "start_s": snappedf(no_input_span_start, 0.01),
			"phase": String(cur_phase.get("name", ""))}
	no_input_span_start = -1.0


func _input_possible() -> bool:
	if act == null or not is_instance_valid(act) or act.state != "play":
		return false
	if not world.active or world.phase_advance_pending or world.reveal_t > 0.0 \
			or world.phase_index >= world.phases.size():
		return false
	if not world.task_open:
		if world.hotspot_opening or (world.interaction_requested and world.wander_walking):
			return false
		return world.armed_station >= 0
	var mode := String(_phase_dict().get("mode", ""))
	if mode == "talk":
		return false
	if mode in ["lens", "catch"]:
		return true
	var s: Variant = world.surface
	if s == null or not is_instance_valid(s):
		return false
	if bool(s.get("completion_accepted")) or bool(s.get("armed_only")):
		return false
	if s.has_method("_input_blocked") and bool(s._input_blocked()):
		return false
	match String(s.get("mode")):
		"echo":
			return bool(s.echo_listening)
		"dance_sequence":
			return bool(s.dance_listening)
		"kart_race":
			return not bool(s.race_finished) and bool(s.get("_career_active"))
		"boxing_imp":
			return true
	return true


func _hint(now: float, kind: String) -> void:
	if cur_phase.is_empty():
		return
	cur_phase["hints"] = int(cur_phase["hints"]) + 1
	(cur_phase["hint_events"] as Array).append({"t": snappedf(now, 0.01), "kind": kind})


func _assist(now: float, kind: String) -> void:
	if cur_phase.is_empty():
		return
	cur_phase["assists_or_mercy_events"] = int(cur_phase["assists_or_mercy_events"]) + 1
	(cur_phase["assist_events"] as Array).append({"t": snappedf(now, 0.01), "kind": kind})
	_event("assist", {"kind": kind, "phase": cur_phase["name"]})


func _on_any_signal(_a: Variant = null, _b: Variant = null, _c: Variant = null) -> void:
	gesture_count += 1


func _on_voice(kind: String, speaker: String, event: String, text: String) -> void:
	var now := clock.t if clock != null else 0.0
	# Attribute to the phase the world is on at call time (a new phase's prompt
	# is spoken in the same frame the previous one advances).
	var live_name := String(cur_phase.get("name", ""))
	var live_index := int(cur_phase.get("index", -1))
	if world != null and is_instance_valid(world) and world.phase_index < world.phases.size():
		live_index = world.phase_index
		live_name = String((world.phases[live_index] as Dictionary).get("name", ""))
	var entry := {"t": snappedf(now, 0.01), "kind": kind, "speaker": speaker,
		"event": event, "phase": live_name}
	if not text.is_empty():
		entry["text"] = text.left(160)
	if kind == "sfx":
		return  # sfx are counted through audio_starts; keep voice list readable
	voice_lines.append(entry)
	if kind == "say":
		if cur_phase.is_empty() or int(cur_phase.get("index", -1)) != live_index \
				or float(cur_phase.get("end_s", -1.0)) >= 0.0:
			voice_carry.append(event)
			return
		(cur_phase["voice"] as Array).append(event)
		var low := event.to_lower()
		if low.contains("help") or low.contains("hint") or low.contains("peek"):
			_hint(now, "voice_" + event)


func _on_node_added(node: Node) -> void:
	if node is AudioStreamPlayer or node is AudioStreamPlayer2D:
		audio_players.append(weakref(node))


func _poll_audio(now: float) -> void:
	var keep: Array = []
	for ref: WeakRef in audio_players:
		var player: Variant = ref.get_ref()
		if player == null:
			continue
		keep.append(ref)
		var id := (player as Node).get_instance_id()
		var playing := bool(player.playing)
		var pos := float(player.get_playback_position()) if playing else 0.0
		var stream_path := ""
		if player.stream != null:
			stream_path = String(player.stream.resource_path)
		var prev: Dictionary = audio_state.get(id, {})
		var started := playing and (not bool(prev.get("playing", false))
			or String(prev.get("path", "")) != stream_path
			or pos + 0.05 < float(prev.get("pos", 0.0)))
		if started:
			sound_starts += 1
			var item := {"t": snappedf(now, 0.01), "path": stream_path.get_file()}
			audio_starts.append(item)
		audio_state[id] = {"playing": playing, "path": stream_path, "pos": pos}
	audio_players = keep


# ------------------------------------------------------------ dead touches

func _touch_snapshot() -> Dictionary:
	var s: Variant = world.surface if world != null and is_instance_valid(world) else null
	var snap := {
		"gest": gesture_count, "snd": sound_starts,
		"prog": world.phase_progress, "pidx": world.phase_index,
		"task": world.task_open, "walk": world.wander_walking,
		"ireq": world.interaction_requested, "lens": world.lens_pos,
		"fb": 0.0, "demo": 999.0, "sprog": -1.0,
	}
	if s != null and is_instance_valid(s):
		if s.get("feedback_t") != null:
			snap["fb"] = float(s.feedback_t)
		if s.get("demo_t") != null:
			snap["demo"] = float(s.demo_t)
		if s.has_method("progress"):
			snap["sprog"] = float(s.progress())
		var vis := ""
		for prop: String in VISIBLE_STATE_PROPS:
			var v: Variant = s.get(prop)
			if v != null:
				vis += prop + "=" + str(v) + ";"
		snap["vis"] = vis.md5_text()
	if world.nursery_catch != null and is_instance_valid(world.nursery_catch):
		snap["vis2"] = str(world.nursery_catch.get("catcher_x"))
	return snap


func _resolve_dead_touches(now: float) -> void:
	if pending_touches.is_empty() or world == null or not is_instance_valid(world):
		return
	var cur := _touch_snapshot()
	var keep: Array = []
	for pending: Dictionary in pending_touches:
		var snap: Dictionary = pending["snap"]
		var responded := int(cur["gest"]) != int(snap["gest"]) \
			or int(cur["snd"]) != int(snap["snd"]) \
			or not is_equal_approx(float(cur["prog"]), float(snap["prog"])) \
			or int(cur["pidx"]) != int(snap["pidx"]) \
			or bool(cur["task"]) != bool(snap["task"]) \
			or (bool(cur["walk"]) and not bool(snap["walk"])) \
			or bool(cur["ireq"]) != bool(snap["ireq"]) \
			or (cur["lens"] as Vector2).distance_to(snap["lens"] as Vector2) > 1.0 \
			or float(cur["fb"]) > float(snap["fb"]) + 0.01 \
			or float(cur["demo"]) + 0.02 < float(snap["demo"]) \
			or not is_equal_approx(float(cur["sprog"]), float(snap["sprog"])) \
			or String(cur.get("vis", "")) != String(snap.get("vis", "")) \
			or String(cur.get("vis2", "")) != String(snap.get("vis2", ""))
		if responded:
			continue
		if float(pending["up_t"]) >= 0.0 and now - float(pending["up_t"]) >= DEAD_TOUCH_WINDOW:
			dead_touches += 1
			if not hover_probe_done:
				hover_probe_done = true
				_event("first_dead_touch_top_control", {"control": _top_control_at(
					Vector2(float(pending["pos"][0]), float(pending["pos"][1])))})
			if not cur_phase.is_empty():
				cur_phase["dead_touches"] = int(cur_phase["dead_touches"]) + 1
			if events.size() < 4000:
				_event("dead_touch", {"pos": pending["pos"], "phase": cur_phase.get("name", "")})
		else:
			keep.append(pending)
	pending_touches = keep


## Diagnostic only (once per run): which Control the GUI would pick at a point.
func _top_control_at(vp: Vector2) -> String:
	var motion := InputEventMouseMotion.new()
	motion.position = vp
	motion.global_position = vp
	get_root().push_input(motion, true)
	var hit := get_root().gui_get_hovered_control()
	if hit == null:
		return "none (falls through to _unhandled_input / world layers)"
	var script_path := ""
	if hit.get_script() != null:
		script_path = String((hit.get_script() as Script).resource_path).get_file()
	return "%s [%s] %s" % [hit.name, hit.get_class(), script_path]


# ---------------------------------------------------------------- input io

func _to_window(vp: Vector2) -> Vector2:
	return get_root().get_screen_transform() * vp


func _ci_vp(item: CanvasItem, local: Vector2) -> Vector2:
	return item.get_global_transform_with_canvas() * local


func _send(kind: String, vp: Vector2) -> void:
	var now := clock.t
	var win := _to_window(vp)
	if kind == "down":
		if finger_down:
			_send("up", last_finger_vp)
		var ev := InputEventScreenTouch.new()
		ev.index = 0
		ev.position = win
		ev.pressed = true
		Input.parse_input_event(ev)
		finger_down = true
		total_inputs += 1
		last_touch_t = now
		if not cur_phase.is_empty():
			cur_phase["inputs"] = int(cur_phase["inputs"]) + 1
		if world != null and is_instance_valid(world):
			pending_touches.append({"t": now, "up_t": -1.0,
				"pos": [snappedf(vp.x, 1), snappedf(vp.y, 1)], "snap": _touch_snapshot()})
	elif kind == "move":
		if not finger_down:
			return
		var drag := InputEventScreenDrag.new()
		drag.index = 0
		drag.position = win
		drag.relative = win - _to_window(last_finger_vp)
		drag.screen_relative = drag.relative
		var dt := maxf(clock.last_delta, 1.0 / 120.0)
		drag.velocity = drag.relative / dt
		drag.screen_velocity = drag.velocity
		Input.parse_input_event(drag)
		total_moves += 1
		last_touch_t = now
		if not cur_phase.is_empty():
			cur_phase["drag_moves"] = int(cur_phase["drag_moves"]) + 1
	elif kind == "up":
		if not finger_down:
			return
		var up := InputEventScreenTouch.new()
		up.index = 0
		up.position = win
		up.pressed = false
		Input.parse_input_event(up)
		finger_down = false
		for pending: Dictionary in pending_touches:
			if float(pending["up_t"]) < 0.0:
				pending["up_t"] = now
		last_touch_t = now
	last_finger_vp = vp


func _release_finger() -> void:
	if finger_down:
		_send("up", last_finger_vp)


# ------------------------------------------------------------ policy layer

func _policy() -> String:
	return String(cfg["policy"])


func _think_time() -> float:
	match _policy():
		"expert":
			return rng.randf_range(0.12, 0.22)
		"child_sim":
			return rng.randf_range(0.5, 0.9)
		"slow":
			return rng.randf_range(10.0, 20.0)
	return 0.5


func _drag_speed() -> float:
	match _policy():
		"expert":
			return 1100.0
		"child_sim":
			return rng.randf_range(380.0, 620.0)
		"slow":
			return 600.0
	return 800.0


func _is_child() -> bool:
	return _policy() == "child_sim"


func _wrong_pick() -> bool:
	return _is_child() and rng.randf() < 0.15


func _miss_offset(p: Vector2) -> Vector2:
	if _is_child() and rng.randf() < 0.25:
		return p + Vector2.from_angle(rng.randf() * TAU) * rng.randf_range(40.0, 120.0)
	return p


func _drive(now: float) -> void:
	if world == null or not is_instance_valid(world) or act == null or not is_instance_valid(act):
		return
	if not action.is_empty():
		if _tick_action(action, now):
			action = {}
			next_ready_t = now + _think_time()
		return
	var policy := _policy()
	if policy == "idle":
		return
	if now < next_ready_t:
		return
	if policy == "random_tapper":
		var p := Vector2(rng.randf_range(8.0, CANVAS.x - 8.0), rng.randf_range(8.0, CANVAS.y - 8.0))
		action = _tap(p, false)
		_start_action(action, now)
		next_ready_t = now + rng.randf_range(0.38, 0.62)
		return
	var planned := _plan(now)
	if planned.is_empty():
		next_ready_t = now + 0.1
		return
	action = planned
	_start_action(action, now)


func _start_action(a: Dictionary, now: float) -> void:
	a["t0"] = now
	a["i"] = 0
	a["started"] = false
	a["key"] = _phase_key()
	if _policy() == "random_tapper":
		action = a
		return
	if events.size() < 4000:
		var info := {"kind": String(a.get("kind", a.get("type", ""))),
			"phase": String(cur_phase.get("name", ""))}
		if a.has("steps"):
			var st: Array = a["steps"]
			var p0: Vector2 = (st[0] as Array)[2]
			var p1: Vector2 = (st[st.size() - 1] as Array)[2]
			info["from"] = [snappedf(p0.x, 1), snappedf(p0.y, 1)]
			info["to"] = [snappedf(p1.x, 1), snappedf(p1.y, 1)]
		if OS.get_environment("REEF_DEBUG") == "1":
			info["state"] = _debug_state()
		_event("action", info)


func _debug_state() -> Dictionary:
	var out := {"phase_progress": world.phase_progress}
	var s: Variant = world.surface
	if s == null or not is_instance_valid(s):
		return out
	if s.has_method("_input_blocked"):
		out["input_blocked"] = bool(s._input_blocked())
	if s.has_method("_mode_complete"):
		out["mode_complete"] = bool(s._mode_complete())
	for prop: String in ["mode", "trace_journey", "widget_fill", "held", "pipe_grid", "pipe_tray",
			"pipe_flow", "pipe_round", "pipe_wait_t", "completion_accepted", "_assist_level",
			"armed_only", "demo_active", "ribbon_progress", "twirl_progress", "pose_round",
			"_ribbon_engaged", "_completion_emitted", "race_finished"]:
		if s.get(prop) != null:
			out[prop] = str(s.get(prop))
	return out


## Returns true when the action is finished.
func _tick_action(a: Dictionary, now: float) -> bool:
	var rel := now - float(a["t0"])
	match String(a["type"]):
		"steps":
			var steps: Array = a["steps"]
			while int(a["i"]) < steps.size() and float((steps[int(a["i"])] as Array)[0]) <= rel:
				var step: Array = steps[int(a["i"])]
				_send(String(step[1]), step[2] as Vector2)
				a["i"] = int(a["i"]) + 1
			return int(a["i"]) >= steps.size()
		"hold":
			if not bool(a["started"]):
				a["started"] = true
				_send("down", a["p"] as Vector2)
				return false
			if bool(a.get("rock", false)):
				_send("move", (a["p"] as Vector2) + Vector2(sin(rel * 5.0) * 10.0, 0.0))
			if _hold_done(a, rel):
				_send("up", last_finger_vp)
				return true
			return false
		"circle":
			var center: Vector2 = a["c"]
			var radius := float(a["r"])
			if not bool(a["started"]):
				a["started"] = true
				a["last"] = rel
				_send("down", center + Vector2.from_angle(float(a["ang"])) * radius)
				return false
			var dt := rel - float(a["last"])
			a["last"] = rel
			a["ang"] = float(a["ang"]) + clampf(float(a["speed"]) * dt, -0.45, 0.45)
			var wob := 0.0
			if _is_child():
				wob = sin(rel * 3.1) * radius * 0.12 + rng.randf_range(-4.0, 4.0)
			_send("move", center + Vector2.from_angle(float(a["ang"])) * (radius + wob))
			if _hold_done(a, rel):
				_send("up", last_finger_vp)
				return true
			return false
		"racer":
			return _tick_racer(a, rel)
		"catch":
			return _tick_catch(a, rel)
	return true


func _hold_done(a: Dictionary, rel: float) -> bool:
	if rel >= float(a.get("max", 8.0)):
		return true
	if _phase_key() != String(a["key"]) or world.phase_advance_pending or act.state != "play":
		return true
	var s: Variant = world.surface
	if s != null and is_instance_valid(s) and bool(s.get("completion_accepted")):
		return true
	if a.has("until_prop"):
		var v: Variant = s.get(String(a["until_prop"])) if s != null else null
		if v != null and float(v) >= float(a.get("until_value", 1.0)):
			return true
	if a.has("release_at") and rel >= float(a["release_at"]):
		return true
	return false


# ------------------------------------------------------------ action builders

func _tap(vp: Vector2, may_miss := true) -> Dictionary:
	var p := _miss_offset(vp) if may_miss else vp
	return {"type": "steps", "kind": "tap", "steps": [[0.0, "down", p], [0.08, "up", p]]}


func _drag(points: Array, speed: float = -1.0, end_hold: float = 0.06) -> Dictionary:
	if speed <= 0.0:
		speed = _drag_speed()
	var steps: Array = []
	var start: Vector2 = points[0]
	if _is_child() and rng.randf() < 0.25:
		start += Vector2.from_angle(rng.randf() * TAU) * rng.randf_range(10.0, 35.0)
	steps.append([0.0, "down", start])
	var t := 0.05
	var travelled := 0.0
	var amp := rng.randf_range(8.0, 22.0) if _is_child() else 0.0
	var phase_off := rng.randf() * TAU
	var prev: Vector2 = points[0]
	for i in range(1, points.size()):
		var target: Vector2 = points[i]
		var length := prev.distance_to(target)
		var n := maxi(1, ceili(length / (speed / 30.0)))
		var dir := (target - prev).normalized() if length > 0.01 else Vector2.RIGHT
		var perp := Vector2(-dir.y, dir.x)
		for k in range(1, n + 1):
			var p := prev.lerp(target, float(k) / float(n))
			travelled += length / float(n)
			if amp > 0.0:
				p += perp * (sin(phase_off + travelled * 0.03) * amp + rng.randf_range(-4.0, 4.0))
			t += length / float(n) / speed
			steps.append([t, "move", p])
		prev = target
	var last: Vector2 = (steps[steps.size() - 1] as Array)[2]
	if _is_child() and rng.randf() < 0.10 and steps.size() > 4:
		# early lift: the child lets go part way
		var cut := int(steps.size() * rng.randf_range(0.4, 0.8))
		steps = steps.slice(0, cut)
		last = (steps[steps.size() - 1] as Array)[2]
		t = float((steps[steps.size() - 1] as Array)[0])
	steps.append([t + end_hold, "up", last])
	return {"type": "steps", "kind": "drag", "steps": steps}


func _hold(vp: Vector2, max_s: float, rock := false) -> Dictionary:
	var a := {"type": "hold", "kind": "hold", "p": vp, "max": max_s, "rock": rock}
	if _is_child() and rng.randf() < 0.2:
		a["release_at"] = rng.randf_range(0.8, 2.5)
	return a


func _circle(center_vp: Vector2, radius_vp: float, start_angle: float, speed: float, max_s: float) -> Dictionary:
	return {"type": "circle", "kind": "circle", "c": center_vp, "r": radius_vp,
		"ang": start_angle, "speed": speed, "max": max_s}


func _with_dwell(a: Dictionary, extra: float) -> Dictionary:
	# keep the finger at its last point for `extra` seconds before lifting
	var steps: Array = a["steps"]
	var up: Array = steps.pop_back()
	var t := float(up[0])
	var p: Vector2 = up[2]
	var k := 0.0
	while k < extra:
		k += 1.0 / 15.0
		steps.append([t + k, "move", p + Vector2(sin(k * 9.0) * 2.0, 0.0)])
	steps.append([t + extra + 0.05, "up", p])
	return a


# ---------------------------------------------------------------- planner

func _plan(now: float) -> Dictionary:
	var w := world
	if act.state != "play" or not w.active:
		return {}
	if w.phase_advance_pending or w.reveal_t > 0.0 or w.phase_index >= w.phases.size():
		return {}
	var phase := _phase_dict()
	var mode := String(phase.get("mode", ""))
	if not w.task_open:
		if w.hotspot_opening or (w.interaction_requested and w.wander_walking):
			return {}
		if w.armed_station < 0 or w.armed_station >= w.station_nodes.size():
			return {}
		var hotspot := w.station_nodes[w.armed_station] as Control
		var centre: Vector2 = hotspot.get_meta("visual_pos", hotspot.position + hotspot.size * 0.5)
		var parent := hotspot.get_parent() as CanvasItem
		var a := _tap(_ci_vp(parent, centre))
		a["kind"] = "hotspot"
		return a
	if mode == "talk":
		return {}
	if mode == "lens":
		return _plan_lens()
	if mode == "catch":
		return _plan_catch()
	var s: Variant = w.surface
	if s == null or not is_instance_valid(s) or not (s as Control).is_visible_in_tree():
		return {}
	if bool(s.get("completion_accepted")) or bool(s.get("armed_only")):
		return {}
	if s.has_method("_input_blocked") and bool(s._input_blocked()):
		return {}
	var stuck := now - phase_last_progress_t > 25.0
	if stuck and rng.randf() < 0.35 and s.has_method("_demo_finger_pose"):
		return _demo_mimic(s)
	if s is OperaBoxingSurface:
		return _plan_boxing(s, mode)
	if s.get_script() == BalletSurfaceScript:
		return _plan_ballet(s)
	if s.get_script() == TeacherSurfaceScript:
		return _plan_teacher(s)
	if s.get_script() == GeologySurfaceScript:
		return _plan_geology(s)
	if s is OperaRacerSurface and String(s.mode) == "kart_race":
		return {"type": "racer", "kind": "steer"}
	return _plan_generic(s)


func _sv(s: Variant, p: Vector2) -> Vector2:
	return _ci_vp(s as CanvasItem, p)


func _sscale(s: Variant) -> float:
	return (s as CanvasItem).get_global_transform_with_canvas().x.length()


func _plan_generic(s: Variant) -> Dictionary:
	var mode := String(s.mode)
	var size: Vector2 = (s as Control).size
	match mode:
		"tap":
			if bool(s._uses_anchored_targets()):
				var idx := int(s._target_next_unplaced())
				if idx < 0:
					return {}
				return _tap(_sv(s, s._target_anchor_point(idx)))
			if bool(s._is_nursery_burp_context()):
				var a := _tap(_sv(s, s._nursery_burp_hand_point(1.0)))
				return a
			var pose: Dictionary = s._demo_finger_pose()
			var at: Vector2 = pose.get("at", size * 0.5)
			at += Vector2(rng.randf_range(-160.0, 160.0), rng.randf_range(-90.0, 90.0))
			at = at.clamp(size * 0.12, size * 0.88)
			return _tap(_sv(s, at))
		"choice":
			if float(s.shuffle_t) > 0.0:
				return {}
			var count := maxi(1, int(s.choice_count))
			var lane := int(s.target_choice)
			if _wrong_pick() and count > 1:
				lane = (lane + 1 + rng.randi_range(0, count - 2)) % count
			var lane_pt := Vector2(size.x * (float(lane) + 0.5) / float(count), size.y * 0.5)
			return _tap(_sv(s, lane_pt))
		"timing":
			var tp := float(s.timing_position)
			var zone: Vector2 = s.timing_zone
			if tp < zone.x + 0.05 or tp > zone.y - 0.05:
				return {}
			return _tap(_sv(s, (s._demo_finger_pose() as Dictionary).get("at", size * 0.5)))
		"hold":
			var hp := _demo_press_point(s)
			return _hold(_sv(s, hp), 12.0)
		"pourt":
			return _hold(_sv(s, (s._pour_pitcher_hit_rect() as Rect2).get_center()), 15.0, true)
		"oven":
			if not bool(s.oven_done) and float(s.oven_t) < 0.47:
				if _is_child() and float(s.oven_t) > 0.2 and rng.randf() < 0.05:
					return _tap(_sv(s, (s._oven_handle_rect() as Rect2).get_center()))
				return {}
			return _tap(_sv(s, (s._oven_handle_rect() as Rect2).get_center()))
		"circle":
			var pivot: Vector2 = s._circle_pivot()
			var min_r := float(s._circle_min_radius())
			var r := maxf(min_r + 45.0, minf(size.x, size.y) * 0.26)
			var speed := 5.2 if not _is_child() else rng.randf_range(2.6, 4.0)
			if _policy() == "slow":
				speed = 3.5
			return _circle(_sv(s, pivot), r * _sscale(s), rng.randf() * TAU, speed,
				12.0 if not _is_child() else rng.randf_range(3.0, 8.0))
		"echo":
			if not bool(s.echo_listening):
				return {}
			if _wrong_pick():
				return _tap(_sv(s, s._echo_star_center(rng.randi_range(0, 2))), false)
			return _demo_mimic(s)
		"dance_sequence":
			if not bool(s.dance_listening):
				return {}
			if _wrong_pick():
				return _tap(_sv(s, (s._dance_pad_rect(rng.randi_range(0, 3)) as Rect2).get_center()), false)
			return _demo_mimic(s)
		"pipe":
			return _plan_pipe(s)
		"farm_lob":
			if bool(s.farm_flying) or float(s.farm_pause) > 0.0 or bool(s.farm_complete):
				return {}
			return _demo_mimic(s)
		"candy_sort", "geology_sort":
			var piece: Vector2 = s.candy_position
			var bin := int(s.candy_type)
			if _wrong_pick():
				bin = (bin + 1) % 3
			return _drag([_sv(s, piece), _sv(s, (s._candy_bin_rect(bin) as Rect2).get_center())])
		"paint_reveal":
			var canvas: Rect2 = s._paint_canvas_rect()
			var pts: Array = []
			var rows := 6
			for row in range(rows):
				var y := canvas.position.y + canvas.size.y * (float(row) + 0.5) / float(rows)
				var xa := canvas.position.x + canvas.size.x * 0.06
				var xb := canvas.position.x + canvas.size.x * 0.94
				pts.append(_sv(s, Vector2(xa if row % 2 == 0 else xb, y)))
				pts.append(_sv(s, Vector2(xb if row % 2 == 0 else xa, y)))
			return _drag(pts)
		"swipe":
			if bool(s._uses_long_push_context()) and not bool(s._is_nursery_bedtime_context()) \
					and not bool(s._uses_authored_trace_context()):
				var from: Vector2 = s._long_push_position(float(s.widget_fill))
				var to: Vector2 = s._long_push_end() + Vector2(30.0, 0.0)
				return _drag([_sv(s, from), _sv(s, from.lerp(to, 0.5)), _sv(s, to)])
			if bool(s._uses_authored_trace_context()):
				var j := float(s.trace_journey)
				var tpts: Array = []
				var q := j
				while q < 1.0:
					tpts.append(_sv(s, s._trace_demo_point(q)))
					q += 0.04
				tpts.append(_sv(s, s._trace_demo_point(1.0)))
				if tpts.size() < 2:
					tpts.append(_sv(s, s._trace_demo_point(1.0) + Vector2(6.0, 0.0)))
				var ta := _drag(tpts, minf(_drag_speed(), 700.0))
				ta["kind"] = "trace"
				return ta
			return _demo_mimic(s)
	return _demo_mimic(s)


## Pipe board: the same diagnosis the game's 8-second hint uses, without the wait.
func _pipe_next_cell(s: Variant) -> int:
	var G := OperaGestureSurface
	var grid: Array = s.pipe_grid
	if grid.is_empty():
		return -1
	var flow: Array = s.pipe_flow
	if flow.is_empty():
		var target := int(s._pipe_demo_target_cell())
		var rd: Dictionary = G.PIPE_ROUNDS[clampi(int(s.pipe_round), 0, G.PIPE_ROUNDS.size() - 1)]
		var entry := int(rd.get("entry", 4))
		# the entry stub already holds a tile: fuel is about to flow, wait
		if String(grid[entry]) != "" and target >= 0 and target != entry \
				and float(s.pipe_wait_t) < 1.5:
			var e_tile := String(grid[entry])
			if G.PIPE_MOUTHS.has(e_tile):
				return -1
		return target
	var head: Array = flow[flow.size() - 1]
	var head_cell := int(head[0])
	var in_dir: Vector2i = head[1]
	var tile := String(grid[head_cell])
	if not G.PIPE_MOUTHS.has(tile):
		return -1
	var out_dir := Vector2i.ZERO
	for mouth: Vector2i in (G.PIPE_MOUTHS[tile] as Array):
		if mouth != -in_dir:
			out_dir = mouth
	var col := head_cell % G.PIPE_COLS + out_dir.x
	var row := floori(float(head_cell) / float(G.PIPE_COLS)) + out_dir.y
	if col < 0 or col >= G.PIPE_COLS or row < 0 or row >= G.PIPE_ROWS:
		var rd2: Dictionary = G.PIPE_ROUNDS[clampi(int(s.pipe_round), 0, G.PIPE_ROUNDS.size() - 1)]
		if head_cell == int(rd2.get("exit", -1)) and out_dir == (rd2.get("exit_dir", Vector2i.ZERO) as Vector2i):
			return -1  # fuel is leaving through the real exit: wait for the rocket
		return head_cell if not bool((s.pipe_fixed as Array)[head_cell]) else -1
	var next_cell := row * G.PIPE_COLS + col
	var next_tile := String(grid[next_cell])
	if next_tile == "IMP":
		return head_cell if not bool((s.pipe_fixed as Array)[head_cell]) else -1
	if next_tile == "":
		return next_cell
	# occupied: fuel is flowing into it, or it is the wrong shape and fuel waits
	return next_cell if float(s.pipe_wait_t) > 1.5 else -1


func _plan_pipe(s: Variant) -> Dictionary:
	if bool(s.completion_accepted):
		return {}
	var cell := _pipe_next_cell(s)
	if cell < 0:
		return {}
	var grid: Array = s.pipe_grid
	var dest: Vector2 = (s._pipe_cell_rect(cell) as Rect2).get_center()
	var tile := String(grid[cell])
	if tile != "" and OperaGestureSurface.PIPE_MOUTHS.has(tile):
		if bool((s.pipe_fixed as Array)[cell]):
			return {}
		var tray_end: Vector2 = (s._pipe_tray_rect((s.pipe_tray as Array).size()) as Rect2).get_center()
		var lift := _drag([_sv(s, dest), _sv(s, dest.lerp(tray_end, 0.5)), _sv(s, tray_end)])
		lift["kind"] = "pipe_lift"
		return lift
	var tray: Array = s.pipe_tray
	if tray.is_empty():
		# no tray tile left: move a stray placed pipe that fuel never reached
		var flow_cells: Array = s._pipe_flow_cells()
		var fixed: Array = s.pipe_fixed
		for c in range(grid.size()):
			var t := String(grid[c])
			if c != cell and OperaGestureSurface.PIPE_MOUTHS.has(t) and not bool(fixed[c]) \
					and not flow_cells.has(c):
				var src: Vector2 = (s._pipe_cell_rect(c) as Rect2).get_center()
				var move := _drag([_sv(s, src), _sv(s, src.lerp(dest, 0.5)), _sv(s, dest)])
				move["kind"] = "pipe_move"
				return move
		return {}
	var slot := int(s._pipe_demo_tray_slot(cell))
	if _wrong_pick() and tray.size() > 1:
		slot = rng.randi_range(0, tray.size() - 1)
	slot = clampi(slot, 0, tray.size() - 1)
	var from: Vector2 = (s._pipe_tray_rect(slot) as Rect2).get_center()
	var place := _drag([_sv(s, from), _sv(s, from.lerp(dest, 0.5)), _sv(s, dest)])
	place["kind"] = "pipe_place"
	return place


## First pressing point of the surface's own ghost-finger demo.
func _demo_press_point(s: Variant) -> Vector2:
	var samples := _demo_samples(s)
	for pose: Dictionary in samples:
		if bool(pose.get("pressing", false)):
			return pose.get("at", Vector2.ZERO)
	return (samples[samples.size() - 1] as Dictionary).get("at", Vector2.ZERO)


func _demo_samples(s: Variant) -> Array:
	var saved_t := float(s.demo_t)
	var samples: Array = []
	var k := 0
	while k <= 60:
		s.demo_t = float(k) * 0.04
		samples.append(s._demo_finger_pose())
		k += 1
	s.demo_t = saved_t
	return samples


## Copy the gesture the game's own ghost finger demonstrates.
func _demo_mimic(s: Variant) -> Dictionary:
	var samples := _demo_samples(s)
	var run: Array = []
	var in_run := false
	for pose: Dictionary in samples:
		var pressing := bool(pose.get("pressing", false))
		if pressing:
			run.append(pose.get("at", Vector2.ZERO))
			in_run = true
		elif in_run:
			break
	if run.is_empty():
		var last: Vector2 = (samples[samples.size() - 1] as Dictionary).get("at", Vector2.ZERO)
		var tap := _tap(_sv(s, last))
		tap["kind"] = "demo_tap"
		return tap
	var travel := 0.0
	for i in range(1, run.size()):
		travel += (run[i - 1] as Vector2).distance_to(run[i])
	if travel < 14.0:
		var t2 := _tap(_sv(s, run[0]))
		t2["kind"] = "demo_tap"
		return t2
	var pts: Array = []
	for p: Vector2 in run:
		pts.append(_sv(s, p))
	var d := _drag(pts)
	d["kind"] = "demo_drag"
	return d


func _plan_boxing(b: Variant, mode: String) -> Dictionary:
	var hand := int(b.round_index()) % 2
	var fingers: Array = b.glove_fingers
	var target: Vector2
	match mode:
		"boxing_guide":
			if int(b.round_index()) >= 2:
				return {}
			var done: Array = b._guide_done
			hand = -1
			for h in range(2):
				if not bool(done[h]) and int(fingers[h]) == -1:
					hand = h
					break
			if hand < 0:
				return {}  # every unguided glove is held by some (possibly phantom) finger
			target = b.guide_target_position(hand)
		"boxing_imp":
			if not bool(b.imp_is_open()):
				return {}
			target = b.active_target_position()
		_:
			target = b.active_target_position()
	if mode != "boxing_guide" and int(fingers[hand]) != -1:
		hand = 1 - hand
	if int(fingers[hand]) != -1:
		return {}
	var start: Vector2 = b.glove_rest(hand)
	var a := _drag([_sv(b, start), _sv(b, start.lerp(target, 0.5)), _sv(b, target)],
		maxf(_drag_speed(), 700.0) if not _is_child() else _drag_speed())
	if mode == "boxing_guard":
		var counter := float(b.get("_counter_t")) if b.get("_counter_t") != null else 1.0
		a = _with_dwell(a, clampf(counter + 0.2, 0.4, 3.5))
	a["kind"] = "punch_" + mode
	return a


func _plan_ballet(s: Variant) -> Dictionary:
	match String(s.mode):
		"ballet_pose":
			var frames: Array = s.pose_option_frames()
			var rects: Array = s.pose_option_rects()
			var want := int(s.pose_target_frame())
			var right := -1
			var others: Array = []
			for i in range(rects.size()):
				if int(frames[i]) == want:
					right = i
				else:
					others.append(i)
			if right < 0:
				return {}
			var pick := right
			if _wrong_pick() and not others.is_empty():
				pick = int(others[rng.randi_range(0, others.size() - 1)])
			return _tap(_sv(s, (rects[pick] as Rect2).get_center()))
		"ballet_ribbon":
			var p0 := float(s.ribbon_progress)
			var pts: Array = []
			var p := p0
			while p < 1.0:
				pts.append(_sv(s, s.ribbon_point(p)))
				p += 0.025
			pts.append(_sv(s, s.ribbon_point(1.0)))
			if pts.size() < 2:
				return {}
			return _drag(pts, minf(_drag_speed(), 650.0))
		"ballet_twirl":
			var c: Vector2 = s.twirl_center()
			var handle: Vector2 = s.twirl_handle_position()
			var a := _circle(_sv(s, c), float(s.twirl_radius()) * _sscale(s),
				(handle - c).angle(), 3.6 if not _is_child() else rng.randf_range(2.0, 3.0), 12.0)
			a["until_prop"] = "twirl_progress"
			a["until_value"] = 1.0
			return a
	return _demo_mimic(s)


func _plan_teacher(s: Variant) -> Dictionary:
	if String(s.lesson_kind()) == "add" and not bool(s.joined):
		return _tap(_sv(s, TeacherSurfaceScript.JOIN_CENTER))
	var counted: Array = s.counted
	for i in range(counted.size()):
		if not bool(counted[i]):
			return _tap(_sv(s, s.counter_position(i)))
	if not bool(s.can_answer()):
		return {}
	var answer := int(s.answer_index())
	var lesson: Dictionary = s.lesson
	var choices: int = (lesson.get("choices", []) as Array).size()
	if _wrong_pick() and choices > 1:
		answer = (answer + 1 + rng.randi_range(0, choices - 2)) % choices
	return _tap(_sv(s, (s.choice_rect(answer) as Rect2).get_center()))


func _plan_geology(s: Variant) -> Dictionary:
	var G := GeologySurfaceScript
	match String(s.mode):
		"geology_river":
			var pts: Array = []
			for i in range(G.RIVER_PATH.size()):
				pts.append(_sv(s, s.river_path_point(i)))
			return _drag(pts, minf(_drag_speed(), 700.0))
		"geology_fossil":
			if int(s.fossil_stage) == 0:
				var cell := Vector2(G.FOSSIL_RECT.size.x / G.FOSSIL_GRID_COLS,
					G.FOSSIL_RECT.size.y / G.FOSSIL_GRID_ROWS)
				var pts2: Array = []
				for row in range(G.FOSSIL_GRID_ROWS):
					for side in [0, 1]:
						var col := (G.FOSSIL_GRID_COLS - 1) if (row % 2 == 0) == (side == 1) else 0
						pts2.append(_sv(s, G.FOSSIL_RECT.position + (Vector2(col, row) + Vector2(0.5, 0.5)) * cell))
				return _drag(pts2, minf(_drag_speed(), 800.0))
			var snapped: Array = s.fossil_snapped
			for piece in range(snapped.size()):
				if not bool(snapped[piece]):
					return _drag([_sv(s, s.fossil_piece_home(piece)), _sv(s, s.fossil_piece_target(piece))])
			return {}
		"geology_pan":
			var center: Vector2 = G.PAN_RECT.get_center()
			var pts3: Array = [_sv(s, center)]
			for swing in range(G.PAN_REQUIRED_REVERSALS + 2):
				var dir := 1.0 if swing % 2 == 0 else -1.0
				pts3.append(_sv(s, center + Vector2(dir * 150.0, 0.0)))
			return _drag(pts3, minf(_drag_speed(), 700.0))
		"geology_geode":
			var seams: Array = s.geode_seams
			for i in range(seams.size()):
				if not bool(seams[i]):
					return _tap(_sv(s, s.geode_seam_spot(i)))
			var half: Vector2 = s.geode_half_center()
			return _drag([_sv(s, half), _sv(s, half + Vector2(G.GEODE_PULL_DISTANCE + 20.0, 0.0))], 500.0)
	return _demo_mimic(s)


func _plan_lens() -> Dictionary:
	var w := world
	var target := -1
	for i in range(w.lens_clues.size()):
		if not w.lens_found[i]:
			target = i
			break
	if target < 0:
		return {}
	var layer := w.lens_layer
	var goal: Vector2 = w._clamped_lens_position(w.lens_clues[target])
	if _is_child() and rng.randf() < 0.25:
		goal += Vector2.from_angle(rng.randf() * TAU) * rng.randf_range(40.0, 120.0)
	var from: Vector2 = w.lens_pos
	var a := _drag([_ci_vp(layer, from), _ci_vp(layer, from.lerp(goal, 0.5)), _ci_vp(layer, goal)],
		minf(_drag_speed(), 700.0))
	a = _with_dwell(a, 0.8 if not _is_child() else rng.randf_range(0.3, 1.2))
	a["kind"] = "lens_sweep"
	return a


func _plan_catch() -> Dictionary:
	if world.nursery_catch == null or not is_instance_valid(world.nursery_catch) \
			or not world.nursery_catch.is_visible_in_tree():
		return {}
	return {"type": "catch", "kind": "cradle_follow", "max": 60.0, "target_x": 0.5}


func _tick_catch(a: Dictionary, rel: float) -> bool:
	var c: Variant = world.nursery_catch
	if c == null or not is_instance_valid(c) or _phase_key() != String(a["key"]) \
			or world.phase_advance_pending or rel > float(a["max"]):
		_send("up", last_finger_vp)
		return true
	var size: Vector2 = (c as Control).size
	var x := float(c.lowest_baby_x())
	if x >= 0.0:
		if _is_child():
			# a child reacts late and overshoots a little
			if fmod(rel, 0.6) < 0.02:
				a["target_x"] = x + rng.randf_range(-0.08, 0.08)
		else:
			a["target_x"] = x
	var p := _ci_vp(c, Vector2(float(a["target_x"]) * size.x, size.y * 0.74))
	if not bool(a["started"]):
		a["started"] = true
		_send("down", p)
	else:
		_send("move", last_finger_vp.lerp(p, 0.35 if not _is_child() else 0.12))
	return false


func _tick_racer(a: Dictionary, rel: float) -> bool:
	var s: Variant = world.surface
	if s == null or not is_instance_valid(s) or not (s is OperaRacerSurface) \
			or bool(s.race_finished) or _phase_key() != String(a["key"]) \
			or world.phase_advance_pending or act.state != "play":
		_send("up", last_finger_vp)
		return true
	var center: Vector2 = OperaRacerSurface.STEERING_RECT.get_center()
	if not bool(a["started"]):
		a["started"] = true
		a["steer"] = 0.0
		a["next_update"] = 0.0
		_send("down", _sv(s, center))
		return false
	if not finger_down or not bool(s.held):
		# finger lost (e.g. race reset): put it back down
		_send("down", _sv(s, center))
		return false
	var kart: Dictionary = s.kart
	var curvature := float(s.road_curvature(float(kart.get("s", 0.0))))
	var half := float(s._engine._rhalf()) if s.get("_engine") != null else 1.0
	var target_lat: float = -signf(curvature) * half * 0.4
	var ideal := clampf((target_lat - float(kart.get("lat", 0.0))) * 0.38
		- float(kart.get("latv", 0.0)) * 0.08, -0.55, 0.55)
	if _is_child():
		if rel >= float(a["next_update"]):
			a["next_update"] = rel + rng.randf_range(0.5, 0.9)
			a["steer"] = clampf(ideal + rng.randf_range(-0.35, 0.35), -0.9, 0.9)
	elif _policy() == "slow":
		if rel >= float(a["next_update"]):
			a["next_update"] = rel + 1.5
			a["steer"] = ideal
	else:
		a["steer"] = ideal
	_send("move", _sv(s, center + Vector2(float(a["steer"]) * OperaRacerSurface.STEERING_RANGE, 0.0)))
	return false


# ---------------------------------------------------------------- frames

func _slug(text: Variant) -> String:
	return String(text).to_lower().replace(" ", "_").replace("-", "_").replace("/", "_")


func _request_capture(tag: String, at: float) -> void:
	if rendered:
		pending_captures.append({"tag": tag, "at": at})


func _service_captures(now: float) -> void:
	var keep: Array = []
	for item: Dictionary in pending_captures:
		if now >= float(item["at"]):
			_capture(String(item["tag"]))
		else:
			keep.append(item)
	pending_captures = keep


func _capture(tag: String) -> void:
	var tex := get_root().get_texture()
	if tex == null:
		return
	var image := tex.get_image()
	if image == null:
		return
	var name := "f_%07.2f_%s.png" % [clock.t, tag]
	var path := frames_dir.path_join(name)
	var t0 := Time.get_ticks_msec()
	image.save_png(path)
	capture_ms += Time.get_ticks_msec() - t0
	frames.append({"t": snappedf(clock.t, 0.01), "tag": tag, "file": "frames/" + name})


# ---------------------------------------------------------------- output

func _event(kind: String, data: Dictionary = {}) -> void:
	if kind == "action" and data.has("kind"):
		kind = String(data["kind"])
	var item := {"t": snappedf(clock.t if clock != null else 0.0, 0.01), "kind": kind}
	item.merge(data, true)
	events.append(item)


func _save_probe(label: String) -> Dictionary:
	var path := "user://reef_save.json"
	var info := {}
	info["user_data_dir"] = OS.get_user_data_dir()
	info["save_exists_" + label] = FileAccess.file_exists(path)
	info["save_mtime_" + label] = FileAccess.get_modified_time(path) if FileAccess.file_exists(path) else 0
	return info


func _write_json(completed: bool) -> void:
	var out := String(cfg["out"])
	var seconds := won_t if won_t >= 0.0 else (clock.t if clock != null else 0.0)
	var phase_rows: Array = []
	for p: Dictionary in phases:
		phase_rows.append(p)
	var session := maxf(0.001, seconds)
	var data := {
		"harness": "reef_play.gd v1",
		"career": career_key, "career_name": career_name, "act_index": act_index,
		"policy": cfg["policy"], "seed": int(cfg["seed"]), "mode": cfg["mode"],
		"input_path": cfg["input"],
		"rendered": rendered, "max_seconds": float(cfg["max_seconds"]),
		"completed": completed,
		"seconds": snappedf(seconds, 0.01),
		"session_seconds": snappedf(clock.t if clock != null else 0.0, 0.01),
		"wall_seconds": snappedf(float(Time.get_ticks_msec() - started_wall_ms) / 1000.0, 0.1),
		"total_inputs": total_inputs, "total_drag_moves": total_moves,
		"dead_touches": dead_touches,
		"hints": _sum_phase("hints"), "assists_or_mercy_events": _sum_phase("assists_or_mercy_events"),
		"longest_no_input_wait": longest_wait,
		"no_input_total_s": snappedf(no_input_total, 0.01),
		"no_input_pct": snappedf(100.0 * no_input_total / session, 0.1),
		"phase_count": phase_rows.size(),
		"phases": phase_rows,
		"voice_lines": voice_lines,
		"voice_line_count": voice_lines.size(),
		"audio_starts": audio_starts.size(),
		"audio_start_log": audio_starts.slice(0, 600),
		"performance_result": str(act.performance_result) if act != null and is_instance_valid(act) else "",
		"performance_stats": world.performance_stats.duplicate() if world != null and is_instance_valid(world) else {},
		"frames": frames,
		"frame_capture_ms_total": capture_ms,
		"save_isolation": save_info,
		"problems": problems,
		"events": events,
	}
	var file := FileAccess.open(out.path_join("run.json"), FileAccess.WRITE)
	if file == null:
		push_error("REEF_PLAY|cannot write run.json in " + out)
		return
	file.store_string(JSON.stringify(data, "  "))
	file.close()


func _sum_phase(key: String) -> int:
	var total := 0
	for p: Dictionary in phases:
		total += int(p.get(key, 0))
	return total
