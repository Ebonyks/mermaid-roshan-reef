class_name BrawlGame
extends RefCounted
# Phase 8: the TOY CASTLE brawler — a Castle-Crashers-style walk-the-plane
# co-op on the SideScrollStage engine's brawl mode. Mischief imps have taken
# over Huluu's toy castle; Roshan walks the courtyard plane (x + depth) and
# POPS them with the one tap button, gates sliding the stage forward wave by
# wave. HULUU IS PLAYER 2: an illustrated-cutout hero who fights alongside —
# AI-driven solo, a second gamepad takes her over live.
# No fail: imps bump and giggle, never hurt. Agency rule (Phase 6): Huluu —
# human OR AI — only ever STUNS imps; ONLY Roshan's tap pops them, so a
# zero-input run can never win even with an AI partner on the field.
# All state stays on main (m.*); received by reference.

const SEG_W := 34.0                  # one courtyard segment per wave
const X0 := -17.0                    # left edge of segment 0 (stage-local)
const HALF_D := 7.0                  # walkable depth band (±z)
const WAVES := [3, 4, 5]             # imps per segment
const IMP_SPEED := 7.0
const HULUU_SPEED := 20.0
const STUN_T := 3.0                  # Huluu's stun duration
const STUN_R := 5.0                  # Huluu's stun reach
const BOP_R := 6.0                   # Roshan's base pop reach (mercy grows it)
const BANNERS := [Color(1.0, 0.72, 0.82), Color(0.62, 0.90, 0.78), Color(0.78, 0.72, 0.98), Color(1.0, 0.87, 0.55)]

var m: ReefMain
var stage: SideScrollStage

func _init(main: ReefMain) -> void:
	m = main
	stage = SideScrollStage.new(main)

func build(fr: Dictionary, _origin: Vector3) -> void:
	m.g["seg"] = 0
	m.g["bops"] = 0
	m.g["wave_t"] = 0.0
	m.g["enemies"] = []
	m.g["gates"] = []
	m.g["timer"] = -1.0
	_stage_open()
	stage.set_bounds(X0, X0 + SEG_W)
	m.show_msg(fr["fname"], "Mischief imps are in Huluu's toy castle! Tap to POP them — Huluu helps!")
	m._say("huluu", "greet", 2.0)

func _tick_brawl(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var r := stage.root()
	if r == null:
		return
	var s: Dictionary = stage.brawl_tick(delta)
	m.g["wave_t"] = float(m.g.get("wave_t", 0.0)) + delta
	var enemies: Array = m.g["enemies"]
	var seg: int = int(m.g["seg"])
	if enemies.is_empty() and seg < WAVES.size():
		_spawn_wave(seg)
		enemies = m.g["enemies"]
	# mercy: a long wave slows the imps and grows Roshan's pop reach
	var mercy: float = clampf((float(m.g["wave_t"]) - 45.0) / 60.0, 0.0, 1.0)
	var imp_spd: float = IMP_SPEED * (1.0 - 0.45 * mercy)
	var bop_r: float = BOP_R + 4.0 * mercy
	# Huluu (player 2): chase the nearest un-stunned imp, stun on contact.
	# Her taps (human) and her AI both STUN only — pops are Roshan's alone.
	var p2_want_x: float = float(s["px"]) - 4.0
	var p2_want_z: float = float(s["pz"])
	var p2_target: Dictionary = _nearest_imp(float(m.g.get("ss_p2x", 0.0)), float(m.g.get("ss_p2z", 0.0)), true)
	if not p2_target.is_empty():
		var tn: Node3D = p2_target["node"]
		p2_want_x = tn.position.x
		p2_want_z = tn.position.z
	var p2: Dictionary = stage.companion_tick(delta, p2_want_x, p2_want_z, HULUU_SPEED)
	m.g["p2_cd"] = maxf(0.0, float(m.g.get("p2_cd", 0.0)) - delta)
	var p2_stun_now: bool = bool(p2["tap"]) or (not bool(p2["human"]) and float(m.g["p2_cd"]) <= 0.0)
	if p2_stun_now and not p2_target.is_empty():
		var tn2: Node3D = p2_target["node"]
		if Vector2(tn2.position.x - float(p2["x"]), tn2.position.z - float(p2["z"])).length() < STUN_R:
			p2_target["stun"] = STUN_T
			m.g["p2_cd"] = 2.4
			m._sparkle_burst(tn2.global_position + Vector3(0, 2.5, 0), Color(0.75, 0.85, 1.0))
	# imps: chase the nearer hero, hop-bob, bump gently — never hurt
	for e in enemies:
		var en: Node3D = e["node"]
		if not is_instance_valid(en):
			continue
		e["stun"] = maxf(0.0, float(e.get("stun", 0.0)) - delta)
		if float(e["stun"]) > 0.0:
			en.rotation.y += delta * 6.0   # dizzy spin while stunned
			continue
		var tx: float = float(s["px"])
		var tz: float = float(s["pz"])
		if Vector2(float(p2["x"]) - en.position.x, float(p2["z"]) - en.position.z).length() < Vector2(tx - en.position.x, tz - en.position.z).length():
			tx = float(p2["x"])
			tz = float(p2["z"])
		var dv := Vector2(tx - en.position.x, tz - en.position.z)
		var dist: float = dv.length()
		if dist > 2.2:
			dv = dv.normalized() * imp_spd * delta
			en.position.x += dv.x
			en.position.z += dv.y
			en.rotation.y = atan2(dv.x, dv.y)
		elif tx == float(s["px"]) and dist < 2.2 and float(e.get("bump_cd", 0.0)) <= 0.0:
			# a giggly bump: shove the imp back, sparkle, no harm done
			e["bump_cd"] = 1.4
			en.position.x -= signf(dv.x) * 2.5
			m._sparkle_burst(en.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 0.55))
		e["bump_cd"] = maxf(0.0, float(e.get("bump_cd", 0.0)) - delta)
		en.position.y = 0.4 + absf(sin(float(m.g["t"]) * 4.0 + en.position.x)) * 0.8
	# Roshan's POP — the deliberate verb; only a fresh tap lands it
	if bool(s["tap"]):
		var hit: Dictionary = _nearest_imp(float(s["px"]), float(s["pz"]), false)
		if not hit.is_empty():
			var hn: Node3D = hit["node"]
			if Vector2(hn.position.x - float(s["px"]), hn.position.z - float(s["pz"])).length() < bop_r:
				enemies.erase(hit)
				m.g["bops"] = int(m.g["bops"]) + 1
				m._sparkle_burst(hn.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.75, 0.9))
				if m.voice != null:
					m.voice.pitch_scale = 1.05 + randf() * 0.25
					m.voice.play()
				var tw := hn.create_tween()
				tw.tween_property(hn, "scale", Vector3.ONE * 0.01, 0.3).set_ease(Tween.EASE_IN)
				tw.tween_callback(hn.queue_free)
	# wave cleared → the gate sparkles open and the courtyard slides forward
	if enemies.is_empty() and seg < WAVES.size():
		m.g["seg"] = seg + 1
		m.g["wave_t"] = 0.0
		if seg < WAVES.size() - 1:
			_open_gate(seg)
			# extend the right wall; the cleared courtyard stays walkable so
			# nobody ever gets snapped forward when a gate opens
			stage.set_bounds(X0, X0 + float(seg + 2) * SEG_W)
			m.show_msg("Huluu", "This way! More imps ahead! ➜")
			m._say("huluu", "talk", 4.0)
		else:
			m.pearl_count += 3   # portal payout, same size as the treasure chest
			m._say("huluu", "hero", 0.0)
			m._end_game(true, fr, "You and Huluu saved the toy castle! Hero high-five!")
			return
	m.hud_game.text = "POP the mischief imps!  %d popped" % int(m.g["bops"])

func stage_close() -> void:
	stage.close()

func _nearest_imp(x: float, z: float, skip_stunned: bool) -> Dictionary:
	var best: Dictionary = {}
	var best_d := 1e9
	var enemies: Array = m.g.get("enemies", [])
	for e in enemies:
		var en: Node3D = e["node"]
		if not is_instance_valid(en):
			continue
		if skip_stunned and float(e.get("stun", 0.0)) > 0.0:
			continue
		var d: float = Vector2(en.position.x - x, en.position.z - z).length()
		if d < best_d:
			best_d = d
			best = e
	return best

func _spawn_wave(seg: int) -> void:
	var r := stage.root()
	var left: float = X0 + float(seg) * SEG_W
	for i in range(int(WAVES[seg])):
		var imp := DungeonArt.spawn("imp", r,
			Vector3(left + SEG_W * 0.45 + randf() * SEG_W * 0.45,
				0.4, randf_range(-HALF_D + 1.0, HALF_D - 1.0)))
		imp.scale = Vector3.ONE * 1.6
		(m.g["enemies"] as Array).append({"node": imp, "stun": 0.0, "bump_cd": 0.0})

# ---- the toy castle courtyard ----------------------------------------------
func _stage_open() -> void:
	stage.open({
		"origin": m.ARENA_POS + Vector3(0, 2.5, 0),
		"half_w": X0 + SEG_W * float(WAVES.size()),
		"half_d": HALF_D,
		"hover": 3.0,
		"bob_amp": 0.5,
		"steer_speed": 24.8,
		"cam_h": 13.5,
		"cam_dist": 24.0,
		"look_h": 6.5,
		"cam_follow": 0.85,
	})
	m._play_music("race")   # the energetic track until the castle gets its own
	var r := stage.root()
	var total_w: float = SEG_W * float(WAVES.size())
	# castle wall along the back of the plane, pastel stone + crenellations
	var wall := MeshInstance3D.new()
	var wm := BoxMesh.new()
	wm.size = Vector3(total_w + 22.0, 12.0, 3.0)
	wall.mesh = wm
	wall.position = Vector3(X0 + total_w * 0.5, 6.0, -HALF_D - 5.5)
	wall.material_override = m._soft_mat(Color(0.86, 0.80, 0.88), 0.08)
	r.add_child(wall)
	for c in range(int(total_w / 7.0)):
		var cren := MeshInstance3D.new()
		var cm := BoxMesh.new()
		cm.size = Vector3(3.0, 2.4, 3.0)
		cren.mesh = cm
		cren.position = Vector3(X0 - 8.0 + float(c) * 7.0, 13.2, -HALF_D - 5.5)
		cren.material_override = m._soft_mat(Color(0.80, 0.73, 0.84), 0.08)
		r.add_child(cren)
	# towers with candy-cone roofs at the ends, banners along the wall
	for tx in [X0 - 9.0, X0 + total_w + 9.0]:
		var tower := MeshInstance3D.new()
		var tm := CylinderMesh.new()
		tm.top_radius = 4.2
		tm.bottom_radius = 4.8
		tm.height = 18.0
		tower.mesh = tm
		tower.position = Vector3(float(tx), 9.0, -HALF_D - 5.5)
		tower.material_override = m._soft_mat(Color(0.86, 0.80, 0.88), 0.08)
		r.add_child(tower)
		var roof := MeshInstance3D.new()
		var rm := CylinderMesh.new()
		rm.top_radius = 0.1
		rm.bottom_radius = 5.2
		rm.height = 6.5
		roof.mesh = rm
		roof.position = Vector3(float(tx), 21.2, -HALF_D - 5.5)
		roof.material_override = m._soft_mat(Color(0.78, 0.55, 0.75), 0.14)
		r.add_child(roof)
	for b in range(int(total_w / 12.0)):
		var ban := MeshInstance3D.new()
		var bqm := QuadMesh.new()
		bqm.size = Vector2(2.6, 4.2)
		ban.mesh = bqm
		ban.position = Vector3(X0 + 4.0 + float(b) * 12.0, 8.5, -HALF_D - 3.9)
		ban.material_override = m._soft_mat(BANNERS[b % BANNERS.size()], 0.2)
		r.add_child(ban)
	# gates between segments: chunky pastel portcullis bars that lift open
	for gx in range(WAVES.size() - 1):
		var gate := Node3D.new()
		gate.position = Vector3(X0 + float(gx + 1) * SEG_W, 0.0, 0.0)
		for bar in range(5):
			var bm2 := MeshInstance3D.new()
			var brm := BoxMesh.new()
			brm.size = Vector3(0.9, 11.0, 0.9)
			bm2.mesh = brm
			bm2.position = Vector3(0, 5.5, -HALF_D + 0.8 + float(bar) * 3.1)
			bm2.material_override = m._soft_mat(Color(0.94, 0.83, 0.55), 0.16)
			gate.add_child(bm2)
		r.add_child(gate)
		(m.g["gates"] as Array).append(gate)
	# HULUU, player 2: the stuffie herself as an illustrated-cutout hero
	stage.companion_open("res://assets/characters/friends/huluu.png", 5.5,
		Vector3(-6.0, 0, 3.0))

func _open_gate(seg: int) -> void:
	var gates: Array = m.g["gates"]
	if seg >= gates.size():
		return
	var gate: Node3D = gates[seg]
	if gate == null or not is_instance_valid(gate):
		return
	m._sparkle_burst(gate.global_position + Vector3(0, 5.0, 0), Color(1.0, 0.9, 0.5))
	var tw := gate.create_tween()
	tw.tween_property(gate, "position:y", 12.5, 0.9).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
