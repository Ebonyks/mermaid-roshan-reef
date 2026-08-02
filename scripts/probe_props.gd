extends SceneTree
# Physical-standee probe (2.5D redesign, charter 2026-07-27): the E2 prop()
# primitive puts flat-art cutouts on real Jolt RigidBody3Ds so the physics
# engine, not animation code, moves them. Asserts: the arena shell and fleet
# build; bodies fall and settle onto the stage floor through the solver;
# a settled fleet stays put when nobody is near (motion only ever comes from
# presence — the sleep/perf contract); the player contact push in
# props_tick() shoves a prop away; the spawn cap holds; teardown reclaims
# every body. Props are garnish with no objective, so there is no win path
# here for probe_passive to worry about.

var main: ReefMain
var stage: SideScrollStage
var bad := 0

const ORIGIN := Vector3(0, 300, 0)
const PROP_SIZE := Vector2(2.4, 3.2)

func _init() -> void:
	seed(20260727)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _stage_case()
	await _settle_case()
	await _idle_case()
	await _push_case()
	await _swell_case()
	await _fx_case()
	await _cap_case()
	await _teardown_case()
	print("PROPS|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("PROPS|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _pump(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _fleet() -> Array:
	return main.g.get("ss_props", [])

func _dt() -> float:
	# the REAL scaled frame delta: clients pass their process delta, which
	# time_scale multiplies — the swell clock must advance at the same rate
	# as the physics sim, or the fade window and the sleep assertions drift
	# apart (a fixed 1/60 here runs the clock 6x slower than the physics)
	return maxf(main.get_process_delta_time(), 1.0 / 60.0)

func _park_player_far() -> void:
	# outside the 4.5-unit coupling radius so props_tick applies no impulse
	main.player.position = ORIGIN + Vector3(0, 30, 40)
	main.player.vel = Vector3.ZERO

func _stage_case() -> void:
	stage = SideScrollStage.new(main)
	stage.open({"origin": ORIGIN, "half_w": 20.0, "half_d": 6.0, "hover": 1.0})
	stage.props_arena()
	_ck("stage + arena shell build", stage.root() != null and (main.g.get("ss_props") is Array))
	var specs: Array = [
		[-10.0, 0.0, {"drop": 2.0}],
		[-4.0, 1.5, {"drop": 2.5, "tumble": false}],
		[4.0, -1.5, {"drop": 3.0, "shape": "ball", "damp": 1.0}],
		[10.0, 0.0, {"drop": 3.5}],
	]
	var made := 0
	for s_v in specs:
		var scfg: Dictionary = s_v[2]
		var b := stage.prop("", PROP_SIZE, float(s_v[0]), float(s_v[1]), scfg)
		if b != null:
			made += 1
	_ck("4 props spawn under the cap", made == 4 and _fleet().size() == 4)

func _settle_case() -> void:
	_park_player_far()
	for i in range(150):
		_park_player_far()
		await process_frame
	var settled := true
	var contained := true
	for p_v in _fleet():
		var b := p_v as RigidBody3D
		if b == null or not is_instance_valid(b):
			settled = false
			continue
		var lp: Vector3 = b.global_position - ORIGIN
		if b.linear_velocity.length() > 0.8:
			settled = false
		if lp.y < 0.2 or lp.y > 3.0:
			settled = false
		if absf(lp.x) > 22.0 or absf(lp.z) > 8.0:
			contained = false
	_ck("fleet settles on the stage floor via the solver", settled)
	_ck("arena walls keep the fleet on the promenade", contained)

func _idle_case() -> void:
	_park_player_far()
	var before: Array = []
	for p_v in _fleet():
		var b := p_v as RigidBody3D
		before.append(b.global_position)
	var awake_last := 0
	for i in range(60):
		_park_player_far()
		var s: Dictionary = stage.props_tick(_dt())
		awake_last = int(s.get("awake", 99))
		await process_frame
	var still := true
	var idx := 0
	for p_v in _fleet():
		var b := p_v as RigidBody3D
		var was: Vector3 = before[idx]
		idx += 1
		if (b.global_position - was).length() > 0.2:
			still = false
	_ck("settled fleet stays put with nobody near", still)
	_ck("settled fleet is asleep (perf contract)", awake_last == 0)

func _push_case() -> void:
	var target: RigidBody3D = null
	for p_v in _fleet():
		var b := p_v as RigidBody3D
		if b != null and is_instance_valid(b) and not b.axis_lock_angular_z:
			target = b
			break
	if target == null:
		_ck("a pushable prop exists", false)
		return
	var start_x: float = target.global_position.x
	for i in range(40):
		# hold Roshan just to the prop's +x side, moving toward it, so the
		# contact push + velocity carry both point -x
		main.player.position = target.global_position + Vector3(2.5, 0.3, 0.0)
		main.player.vel = Vector3(-14.0, 0.0, 0.0)
		stage.props_tick(_dt())
		await process_frame
	main.player.vel = Vector3.ZERO
	var dx: float = target.global_position.x - start_x
	_ck("contact push shoves the prop away", dx < -0.5)

func _swell_case() -> void:
	# flip the tide on mid-stage (the opt-in "swell" cfg key), stir one prop
	# awake through the push coupling, and verify all three swell contracts:
	# a stirred prop rides the real solver tide; the fade lets the fleet
	# settle back to sleep (the perf contract survives the wave); a sleeping
	# prop sways its sprite cosmetically while its body never moves.
	var cfg: Dictionary = main.g.get("ss_cfg", {})
	cfg["swell"] = 1.0
	# a dedicated WATERLOGGED target mid-stage, per the engine's pairing
	# rule: buoyant props (low gravity_scale) are the ones the tide can
	# out-pull friction on — and mid-stage means the stir cannot corner it
	# against a wall like the push-case survivor (run #841 failure)
	var target := stage.prop("", PROP_SIZE, 6.0, 0.0,
		{"drop": 1.0, "gravity_scale": 0.35, "damp": 1.0})
	if target == null:
		_ck("a swell target exists", false)
		return
	for i in range(30):
		_park_player_far()
		stage.props_tick(_dt())
		await process_frame
	for i in range(8):
		main.player.position = target.global_position + Vector3(2.2, 0.3, 0.0)
		main.player.vel = Vector3(-10.0, 0.0, 0.0)
		stage.props_tick(_dt())
		await process_frame
	_park_player_far()
	var base_x: float = target.global_position.x
	var moved_peak := 0.0
	for i in range(50):
		_park_player_far()
		stage.props_tick(_dt())
		moved_peak = maxf(moved_peak, absf(target.global_position.x - base_x))
		await process_frame
	_ck("stirred prop rides the solver tide", moved_peak > 0.1)
	# settle-until-asleep with a generous cap: the fade window is ~6 clock
	# seconds past the last stir, then damping + sleep take over
	var awake_last := 99
	for i in range(500):
		_park_player_far()
		var s: Dictionary = stage.props_tick(_dt())
		awake_last = int(s.get("awake", 99))
		await process_frame
		if awake_last == 0:
			break
	_ck("tide fades and the fleet sleeps again", awake_last == 0)
	var q: MeshInstance3D = target.get_meta("ss_quad", null) as MeshInstance3D
	var body_x: float = target.global_position.x
	var sway_peak := 0.0
	var body_drift := 0.0
	for i in range(40):
		_park_player_far()
		stage.props_tick(_dt())
		if q != null and is_instance_valid(q):
			sway_peak = maxf(sway_peak, absf(q.rotation.z))
		body_drift = maxf(body_drift, absf(target.global_position.x - body_x))
		await process_frame
	_ck("sleeping sprite sways with the wave", sway_peak > 0.005)
	_ck("cosmetic tide never moves the body", body_drift < 0.05)
	cfg["swell"] = 0.0

func _fx_case() -> void:
	# The shared water-FX vocabulary (fx_water.gd): a proc spawns cards that
	# animate out and free themselves; the per-emitter cooldown collapses
	# machine-gun procs; the concurrent cap holds; the styled placeholder
	# visuals must run headless with no atlas art on disk; and an awake prop
	# falling through the stage's opt-in waterline procs a splash.
	var fx: FxWater = main._fx_water_ref()
	var t0: int = main.fxw_total
	fx.splash(ORIGIN + Vector3(0, 2, 0), 20.0, "probe_a")
	_ck("a breach-tier proc spawns splash + ripple cards",
		main.fxw_total == t0 + 2 and main.fxw_cards.size() >= 2)
	fx.splash(ORIGIN + Vector3(0, 2, 0), 20.0, "probe_a")
	_ck("the per-emitter cooldown holds", main.fxw_total == t0 + 2)
	for i in range(10):
		fx.card("splash_small", ORIGIN + Vector3(float(i), 2.0, 0.0))
	_ck("the concurrent-card cap holds", main.fxw_cards.size() <= FxWater.CAP)
	var spawned: int = main.fxw_cards.size()
	var gone := false
	for i in range(300):
		await process_frame
		if main.fxw_cards.is_empty():
			gone = true
			break
	_ck("cards animate out and free themselves", gone and spawned > 0)
	# the waterline: a prop dropped through cfg water_y procs on the way down
	var cfg: Dictionary = main.g.get("ss_cfg", {})
	cfg["water_y"] = 3.0
	var t1: int = main.fxw_total
	var faller := stage.prop("", PROP_SIZE, -14.0, -3.0, {"drop": 7.0})
	if faller == null:
		_ck("a waterline faller exists", false)
	else:
		for i in range(90):
			_park_player_far()
			stage.props_tick(_dt())
			await process_frame
			if main.fxw_total > t1:
				break
		_ck("a prop crossing the waterline procs a splash", main.fxw_total >= t1 + 2)
	cfg.erase("water_y")

func _cap_case() -> void:
	var have: int = _fleet().size()
	var extra := 0
	var last: RigidBody3D = null
	for i in range(10):
		last = stage.prop("", PROP_SIZE, -16.0 + float(i) * 3.5, 3.0, {"drop": 1.0})
		if last != null:
			extra += 1
	var s: Dictionary = stage.props_tick(_dt())
	_ck("fleet cap holds at PROPS_MAX",
		extra == SideScrollStage.PROPS_MAX - have and last == null
		and int(s.get("count", 0)) == SideScrollStage.PROPS_MAX)

func _teardown_case() -> void:
	var bodies: Array = _fleet().duplicate()
	main._clear_game()
	await _pump(6)
	var freed := true
	for p_v in bodies:
		if is_instance_valid(p_v):
			freed = false
	_ck("teardown reclaims every body", freed and not (main.g.get("ss_props") is Array))
	var after := stage.prop("", PROP_SIZE, 0.0, 0.0, {})
	_ck("no orphan spawns after teardown", after == null)
