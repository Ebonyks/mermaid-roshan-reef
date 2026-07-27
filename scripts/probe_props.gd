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
		var s: Dictionary = stage.props_tick(1.0 / 60.0)
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
		stage.props_tick(1.0 / 60.0)
		await process_frame
	main.player.vel = Vector3.ZERO
	var dx: float = target.global_position.x - start_x
	_ck("contact push shoves the prop away", dx < -0.5)

func _cap_case() -> void:
	var extra := 0
	var last: RigidBody3D = null
	for i in range(10):
		last = stage.prop("", PROP_SIZE, -16.0 + float(i) * 3.5, 3.0, {"drop": 1.0})
		if last != null:
			extra += 1
	var s: Dictionary = stage.props_tick(1.0 / 60.0)
	_ck("fleet cap holds at PROPS_MAX",
		extra == SideScrollStage.PROPS_MAX - 4 and last == null
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
