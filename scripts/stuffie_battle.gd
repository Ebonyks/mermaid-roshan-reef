class_name StuffieBattle
extends Node3D
# THE STUFFIE BATTLE ENGINE — the companion wing's arena mode. The child
# CONTROLS THE CREATURE (not Roshan): stick to scamper, ONE attack button
# (PECK for the baby eagle, CLAW for Kitty), and a quick-time DODGE — when an
# opponent telegraphs, a giant pulsing DODGE bubble appears and any tap inside
# the forgiving window hops the stuffie clear. Getting "hit" is always a
# harmless sparkle-bump: no health, no damage, no fail state. Opponents get
# dizzy and BEFRIENDED, never hurt. All motion is analytic (probe-friendly,
# mobile-renderer budget), same Family-B shape as CombatArena.

const CENTER := Vector3(0.0, -2400.0, 0.0)
const RADIUS := 27.0

# The sparring ladder. One round per den visit; after all three are won the
# den serves them again in rotation, a little livelier each time.
const LADDER := [
	{"tag": "round1", "imps": 2, "hp": 2, "attack_gap": 4.6, "telegraph": 2.4, "layout": "ring"},
	{"tag": "round2", "imps": 3, "hp": 2, "attack_gap": 3.8, "telegraph": 2.2, "layout": "double"},
	{"tag": "round3", "imps": 0, "boss": true, "hp": 5, "attack_gap": 3.4, "telegraph": 2.0},
]

var m: ReefMain
var finish_cb: Callable
var round_cfg := {}
var round_tag := ""
var prev_env: Environment = null
var cam: Camera3D = null
var creature: Node3D = null
var creature_def := {}
var hud: CanvasLayer = null
var objective: Label = null
var counter: Label = null
var dodge_btn: Button = null
var pointer: Label3D = null
var pal_pos := Vector3.ZERO
var pal_yaw := PI
var elapsed := 0.0
var state := "play"
var win_t := 0.0
var attack_cool := 0.0
var fire_prev := false
var lunge_t := -1.0
var lunge_vec := Vector3.ZERO
var enemies: Array[Dictionary] = []
var enemy_shots: Array[Dictionary] = []
var befriended_count := 0
# QTE state — one telegraph at a time so the moment is unmissable
var qte_enemy := {}
var qte_t := -1.0
var qte_gap := 0.0
var dodge_success_count := 0
var miss_count := 0
var miss_streak := 0        # consecutive misses → mercy widens the window
var hop_t := -1.0
var hop_vec := Vector3.ZERO
var materials := {}

func start(main: ReefMain, ladder_index: int, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	round_cfg = LADDER[clampi(ladder_index, 0, LADDER.size() - 1)]
	round_tag = String(round_cfg["tag"])
	creature_def = m._companion_ref().active_def()
	pal_pos = CENTER + Vector3(0, 1.2, 9.0)
	_build_environment()
	_build_arena()
	_build_creature()
	_build_camera()
	_build_hud()
	if bool(round_cfg.get("boss", false)):
		_build_boss()
	else:
		_build_imps()
	qte_gap = float(round_cfg.get("attack_gap", 4.0))
	var atk := attack_word()
	m.show_msg(String(creature_def.get("name", "Stuffie")),
		"Play-battle time! Tap %s to bop the imps — and tap the big DODGE bubble when it pops up!" % atk, "talk")
	_update_hud()

func attack_word() -> String:
	return String(creature_def.get("attack", "BOP"))

func action_label() -> String:
	return attack_word()

# ===================== build =====================

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.10, 0.07, 0.20)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.85, 0.75, 1.0)
	env.ambient_light_energy = 0.95
	env.glow_enabled = true
	env.glow_intensity = 0.65
	env.glow_bloom = 0.12
	m._speedy_glow_clamp(env)
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(1.0, 0.9, 0.8)
	sun.light_energy = 1.1
	sun.shadow_enabled = m.quality != "speedy"
	sun.rotation_degrees = Vector3(-50, -30, 0)
	add_child(sun)

func _mat(col: Color, emission: float = 0.0) -> StandardMaterial3D:
	var key := "%s:%.2f" % [col.to_html(true), emission]
	if materials.has(key):
		return materials[key]
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.62
	if emission > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = emission
	materials[key] = mat
	return mat

func _sphere(parent: Node3D, pos: Vector3, radius: float, col: Color, emission: float = 0.0) -> MeshInstance3D:
	var shape := SphereMesh.new()
	shape.radius = radius
	shape.height = radius * 2.0
	shape.radial_segments = 12
	shape.rings = 6
	var node := MeshInstance3D.new()
	node.mesh = shape
	node.position = pos
	node.material_override = _mat(col, emission)
	parent.add_child(node)
	return node

func _build_arena() -> void:
	# the same proven octagon room, painted as a pastel toy mat
	var arena := DungeonArt.spawn("arena", self, CENTER)
	DungeonArt.tint(arena, _mat(Color(0.72, 0.62, 0.90)), _mat(Color(1.0, 0.78, 0.88), 0.2))

func _build_creature() -> void:
	creature = m._companion_ref().make_creature()
	if creature == null:
		creature = _sphere(self, pal_pos, 1.6, Color(1.0, 0.7, 0.8), 0.4)
	else:
		add_child(creature)
	creature.position = pal_pos

func _build_camera() -> void:
	cam = Camera3D.new()
	cam.fov = 58.0
	cam.position = CENTER + Vector3(0, 28.0, 30.0)
	add_child(cam)
	cam.look_at(CENTER + Vector3(0, 1.5, 0), Vector3.UP)
	cam.make_current()

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 14
	add_child(hud)
	var banner := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.08, 0.05, 0.18, 0.88)
	style.border_color = Color(1.0, 0.75, 0.88)
	style.set_border_width_all(4)
	style.set_corner_radius_all(22)
	banner.add_theme_stylebox_override("panel", style)
	banner.position = Vector2(220, 22)
	banner.size = Vector2(840, 112)
	hud.add_child(banner)
	objective = Label.new()
	objective.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	objective.add_theme_font_size_override("font_size", 28)
	objective.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	objective.add_theme_constant_override("outline_size", 8)
	objective.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	objective.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	objective.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	banner.add_child(objective)
	counter = Label.new()
	counter.position = Vector2(30, 28)
	counter.add_theme_font_size_override("font_size", 34)
	counter.add_theme_color_override("font_outline_color", Color(0.05, 0.03, 0.12))
	counter.add_theme_constant_override("outline_size", 9)
	hud.add_child(counter)
	# THE dodge bubble: huge, center-low, hot pink, only alive during a telegraph
	dodge_btn = Button.new()
	dodge_btn.text = "🛡  DODGE!"
	dodge_btn.add_theme_font_size_override("font_size", 46)
	dodge_btn.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	dodge_btn.offset_left = -240.0
	dodge_btn.offset_right = 240.0
	dodge_btn.offset_top = -290.0
	dodge_btn.offset_bottom = -140.0
	var dstyle := StyleBoxFlat.new()
	dstyle.bg_color = Color(1.0, 0.30, 0.55, 0.94)
	dstyle.border_color = Color(1.0, 0.9, 0.95)
	dstyle.set_border_width_all(6)
	dstyle.set_corner_radius_all(70)
	dodge_btn.add_theme_stylebox_override("normal", dstyle)
	var dpressed := dstyle.duplicate() as StyleBoxFlat
	dpressed.bg_color = Color(0.55, 0.95, 0.65, 0.96)
	dodge_btn.add_theme_stylebox_override("pressed", dpressed)
	dodge_btn.visible = false
	dodge_btn.pressed.connect(press_dodge)
	hud.add_child(dodge_btn)
	pointer = Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 150
	pointer.pixel_size = 0.022
	pointer.outline_size = 24
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(pointer)

func _build_imps() -> void:
	var count: int = int(round_cfg.get("imps", 2))
	var layout: String = String(round_cfg.get("layout", "ring"))
	for i in range(count):
		var a: float = float(i) * TAU / float(count) + PI
		var spawn_r := 14.0
		if layout == "double":
			spawn_r = 10.0 if i % 2 == 0 else 17.0
		var pos := CENTER + Vector3(sin(a) * spawn_r, 1.0, cos(a) * spawn_r)
		var root := Node3D.new()
		root.position = pos
		add_child(root)
		DungeonArt.spawn("imp", root)
		enemies.append({"node": root, "pos": pos, "state": "active", "hp": int(round_cfg.get("hp", 2)),
			"timer": 0.0, "attack": 2.5 + float(i) * 1.4, "phase": a, "boss": false})

func _build_boss() -> void:
	# the dragon-turtle comes back for a FRIENDLY sparring rematch
	var root := DungeonArt.spawn("boss", self, CENTER + Vector3(0, 1.0, -10.0))
	root.scale = Vector3.ONE * 1.2
	enemies.append({"node": root, "pos": root.position, "state": "active", "hp": int(round_cfg.get("hp", 5)),
		"timer": 0.0, "attack": 3.0, "phase": 0.0, "boss": true})

# ===================== input =====================

func _move_input() -> Vector2:
	var value := Vector2.ZERO
	if Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT): value.x -= 1.0
	if Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT): value.x += 1.0
	if Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP): value.y -= 1.0
	if Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN): value.y += 1.0
	# every connected pad steers — that IS the casual P2 mode: hand a pad to a
	# grown-up (or sibling) and they pilot the stuffie while P1 watches or taps
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = m.joy_axis(JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.18: value.x = jx
	if absf(jy) > 0.18: value.y = jy
	if m.touch_ui != null and m.touch_ui.stick_vec.length() > 0.12:
		value = m.touch_ui.stick_vec
	return value.limit_length(1.0)

func _action_pressed() -> bool:
	var held: bool = Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	var just: bool = held and not fire_prev
	fire_prev = held
	if m.touch_ui != null and m.touch_ui.consume_action_just():
		just = true
	return just

func press_dodge() -> void:
	# the QTE button (also X on keyboard/pad via _process below)
	if state != "play" or qte_t <= 0.0:
		return
	_dodge_success()

# ===================== tick =====================

func _process(delta: float) -> void:
	if m == null or state == "done":
		return
	elapsed += delta
	attack_cool = maxf(0.0, attack_cool - delta)
	if state == "won":
		win_t -= delta
		if fmod(win_t, 0.32) < delta:
			m._sparkle_burst(CENTER + Vector3(randf_range(-10.0, 10.0), randf_range(1.0, 6.0), randf_range(-8.0, 8.0)), Color.from_hsv(randf(), 0.55, 1.0))
		if win_t <= 0.0:
			_finish()
		return
	_tick_move(delta)
	var attack_tap := _action_pressed()
	# hidden mercy: after two missed dodges in a row, ANY button counts as the
	# dodge — mashing the attack bubble still saves the day for little thumbs
	if attack_tap and qte_t > 0.0 and miss_streak >= 2:
		_dodge_success()
	elif attack_tap and attack_cool <= 0.0:
		_attack()
	if Input.is_physical_key_pressed(KEY_X) or m.joy_pressed(JOY_BUTTON_X) or m.joy_pressed(JOY_BUTTON_Y):
		if qte_t > 0.0:
			_dodge_success()
	_tick_enemies(delta)
	_tick_qte(delta)
	_tick_enemy_shots(delta)
	_tick_pointer()

func _tick_move(delta: float) -> void:
	var speed: float = 14.0 * (1.0 + minf(float(m._companion_ref().level()) * 0.01, 0.25))
	if hop_t > 0.0:
		# dodge hop owns the body for a beat — a happy analytic leap
		hop_t -= delta
		pal_pos += hop_vec * delta
		pal_pos.y = CENTER.y + 1.2 + sin((0.45 - maxf(hop_t, 0.0)) / 0.45 * PI) * 2.4
	elif lunge_t > 0.0:
		lunge_t -= delta
		pal_pos += lunge_vec * delta
		if lunge_t <= 0.0:
			_lunge_land()
	else:
		pal_pos.y = CENTER.y + 1.2
		var move := _move_input()
		pal_pos += Vector3(move.x, 0, move.y) * speed * delta
		if move.length() > 0.08:
			pal_yaw = atan2(move.x, move.y)
	var flat := Vector2(pal_pos.x - CENTER.x, pal_pos.z - CENTER.z)
	if flat.length() > RADIUS - 3.0:
		flat = flat.normalized() * (RADIUS - 3.0)
		pal_pos.x = CENTER.x + flat.x
		pal_pos.z = CENTER.z + flat.y
	creature.position = pal_pos + Vector3(0, sin(elapsed * 4.0) * 0.15, 0)
	# gen2 face = local -X (same convention the follower uses in companion.gd)
	var face := Vector3(sin(pal_yaw), 0, cos(pal_yaw))
	creature.rotation.y = lerp_angle(creature.rotation.y, atan2(face.z, -face.x), 1.0 - pow(0.001, delta))

# ---------- attacking (peck / claw) ----------

func _attack() -> void:
	var target := _nearest_enemy()
	if target.is_empty():
		return
	var dir: Vector3 = (target["pos"] as Vector3) - pal_pos
	dir.y = 0.0
	if dir.length() < 0.1:
		dir = Vector3(sin(pal_yaw), 0, cos(pal_yaw))
	dir = dir.normalized()
	pal_yaw = atan2(dir.x, dir.z)
	# the lunge: a quick analytic dash toward the pal's opponent
	lunge_vec = dir * 26.0
	lunge_t = 0.22
	var lvl: int = m._companion_ref().level()
	attack_cool = clampf(0.55 - float(lvl) * 0.02, 0.30, 0.55)
	if String(creature_def.get("kind", "")) == "cat":
		_claw_flash(dir)
	else:
		_peck_flash(dir)

func _lunge_land() -> void:
	var reach: float = 4.2 * (1.3 if m._companion_ref().tier() >= 2 else 1.0)
	var hits: int = 2 if m._companion_ref().tier() >= 3 else 1
	var target := _nearest_enemy()
	if target.is_empty():
		return
	if ((target["pos"] as Vector3) - pal_pos).length() < reach:
		for i in range(hits):
			_hit_enemy(target)

func _claw_flash(dir: Vector3) -> void:
	# three pastel swipe streaks arcing in front of Kitty
	for i in range(3):
		var streak := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(0.25, 0.25, 3.4)
		streak.mesh = bm
		streak.material_override = _mat(Color(1.0, 0.85, 0.95), 2.0)
		var side: Vector3 = Vector3(dir.z, 0, -dir.x) * (float(i) - 1.0) * 1.1
		streak.position = pal_pos + dir * 2.6 + side + Vector3(0, 2.0, 0)
		streak.rotation.y = atan2(dir.x, dir.z)
		add_child(streak)
		var tw := streak.create_tween()
		tw.tween_property(streak, "position", streak.position + dir * 2.4, 0.18)
		tw.parallel().tween_property(streak, "scale", Vector3(0.1, 0.1, 1.4), 0.18)
		tw.tween_callback(streak.queue_free)
	m._sparkle_burst(pal_pos + dir * 3.0 + Vector3(0, 2.0, 0), Color(0.95, 0.7, 0.9))

func _peck_flash(dir: Vector3) -> void:
	# a golden double-jab spark at the beak
	for i in range(2):
		var jab := _sphere(self, pal_pos + dir * (2.4 + float(i) * 1.2) + Vector3(0, 2.2, 0), 0.5, Color(1.0, 0.9, 0.4), 2.0)
		var tw := jab.create_tween()
		tw.tween_interval(float(i) * 0.08)
		tw.tween_property(jab, "scale", Vector3.ZERO, 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
		tw.tween_callback(jab.queue_free)
	m._sparkle_burst(pal_pos + dir * 3.0 + Vector3(0, 2.2, 0), Color(1.0, 0.9, 0.4))

func _hit_enemy(enemy: Dictionary) -> void:
	if String(enemy["state"]) != "active" or state != "play":
		return
	enemy["hp"] = int(enemy["hp"]) - 1
	m._sparkle_burst((enemy["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(1.0, 0.8, 0.5))
	if m.chime != null:
		m.chime.pitch_scale = 1.1 + randf() * 0.2
		m.chime.play()
	if int(enemy["hp"]) <= 0:
		enemy["state"] = "dizzy"
		enemy["timer"] = 1.3
		if not qte_enemy.is_empty() and qte_enemy == enemy:
			_qte_clear()
	_update_hud()

func _nearest_enemy() -> Dictionary:
	var best := {}
	var best_d := INF
	for enemy in enemies:
		if String(enemy["state"]) != "active":
			continue
		var dd: float = pal_pos.distance_squared_to(enemy["pos"])
		if dd < best_d:
			best_d = dd
			best = enemy
	return best

# ---------- enemies + befriending ----------

func _tick_enemies(delta: float) -> void:
	var remaining := 0
	for enemy in enemies:
		var node: Node3D = enemy["node"]
		var est := String(enemy["state"])
		if est == "active":
			remaining += 1
			var pos: Vector3 = enemy["pos"]
			var toward: Vector3 = pal_pos - pos
			toward.y = 0.0
			var keep: float = 9.0 if bool(enemy["boss"]) else 6.5
			if toward.length() > keep:
				pos += toward.normalized() * delta * (2.2 if bool(enemy["boss"]) else 1.8)
			enemy["pos"] = pos
			node.position = pos + Vector3(0, sin(elapsed * 3.0 + float(enemy["phase"])) * 0.25, 0)
			node.rotation.y = atan2(toward.x, toward.z)
			# only schedule an attack when nobody else is telegraphing
			if qte_t <= 0.0 and qte_enemy.is_empty():
				enemy["attack"] = float(enemy["attack"]) - delta
				if float(enemy["attack"]) <= 0.0:
					enemy["attack"] = qte_gap + randf() * 1.5
					_qte_begin(enemy)
		elif est == "dizzy":
			remaining += 1
			enemy["timer"] = float(enemy["timer"]) - delta
			node.rotation.y += delta * 9.0
			node.position = (enemy["pos"] as Vector3) + Vector3(0, sin(elapsed * 8.0) * 0.3, 0)
			if float(enemy["timer"]) <= 0.0:
				_befriend(enemy)
		elif est == "friend":
			# befriended pals bounce happily along the arena rim
			var seat: Vector3 = enemy["pos"]
			node.position = seat + Vector3(0, absf(sin(elapsed * 4.0 + float(enemy["phase"]))) * 0.8, 0)
			node.rotation.y = atan2(pal_pos.x - seat.x, pal_pos.z - seat.z)
	if remaining == 0 and state == "play":
		_win()

func _befriend(enemy: Dictionary) -> void:
	enemy["state"] = "friend"
	befriended_count += 1
	var pos: Vector3 = enemy["pos"]
	var out := Vector2(pos.x - CENTER.x, pos.z - CENTER.z)
	if out.length() < 0.5:
		out = Vector2(0, 1)
	out = out.normalized() * (RADIUS - 5.0)
	enemy["pos"] = CENTER + Vector3(out.x, 1.0, out.y)
	m._greet_heart(pos + Vector3(0, 3.0, 0))
	m._sparkle_burst(pos + Vector3(0, 2.0, 0), Color(1.0, 0.6, 0.8))
	m.show_msg(String(creature_def.get("name", "Stuffie")), "We're friends now! Hooray!", "talk")
	_update_hud()

# ---------- the DODGE QTE ----------

func _qte_window() -> float:
	var base: float = float(round_cfg.get("telegraph", 2.2))
	if m._companion_ref().tier() >= 1:
		base += 0.5
	return base + minf(float(miss_streak) * 0.6, 1.8)   # mercy: misses widen it

func _qte_begin(enemy: Dictionary) -> void:
	qte_enemy = enemy
	qte_t = _qte_window()
	var node: Node3D = enemy["node"]
	# the telegraph: the opponent puffs up and blinks warm-white
	var tw := node.create_tween().set_loops(3)
	tw.tween_property(node, "scale", node.scale * 1.18, 0.18)
	tw.tween_property(node, "scale", node.scale, 0.18)
	m._sparkle_burst((enemy["pos"] as Vector3) + Vector3(0, 3.5, 0), Color(1.0, 0.45, 0.45))
	if dodge_btn != null:
		dodge_btn.visible = true
		dodge_btn.pivot_offset = dodge_btn.size * 0.5
	_update_hud()

func _tick_qte(delta: float) -> void:
	if qte_t <= 0.0:
		return
	qte_t -= delta
	if dodge_btn != null:
		var pulse_s: float = 1.0 + sin(elapsed * 9.0) * 0.09
		dodge_btn.scale = Vector2(pulse_s, pulse_s)
	if String(qte_enemy.get("state", "")) != "active":
		_qte_clear()   # target got bopped dizzy mid-telegraph
		return
	if qte_t <= 0.0:
		_dodge_missed()

func _dodge_success() -> void:
	if qte_t <= 0.0:
		return
	dodge_success_count += 1
	miss_streak = 0
	# the hop: leap sideways away from the attacker, sparkle trail, jingle
	var from: Vector3 = qte_enemy.get("pos", pal_pos + Vector3.FORWARD)
	var away: Vector3 = pal_pos - from
	away.y = 0.0
	if away.length() < 0.1:
		away = Vector3.FORWARD
	var side := Vector3(away.z, 0, -away.x) * (1.0 if randf() > 0.5 else -1.0)
	hop_vec = (away.normalized() * 0.6 + side.normalized()).normalized() * 16.0
	hop_t = 0.45
	m._sparkle_burst(pal_pos + Vector3(0, 2.0, 0), Color(0.55, 0.95, 1.0))
	if m.chime != null:
		m.chime.pitch_scale = 1.4
		m.chime.play()
	_qte_clear()
	_update_hud()

func _dodge_missed() -> void:
	miss_count += 1
	miss_streak += 1
	# the attack lands as a harmless sparkle-bump — a push and encouragement,
	# NEVER damage or failure (same bubble-shield fiction as Roshan's)
	var from: Vector3 = qte_enemy.get("pos", pal_pos + Vector3.FORWARD)
	_spawn_enemy_shot(from + Vector3(0, 2.4, 0), pal_pos)
	_qte_clear()
	_update_hud()

func _qte_clear() -> void:
	qte_t = -1.0
	qte_enemy = {}
	if dodge_btn != null:
		dodge_btn.visible = false
		dodge_btn.scale = Vector2.ONE

func _spawn_enemy_shot(from: Vector3, to: Vector3) -> void:
	var dir: Vector3 = to - from
	dir.y = 0.0
	if dir.length() < 0.1:
		return
	var orb := _sphere(self, from, 0.58, Color(0.72, 0.34, 0.92), 1.4)
	enemy_shots.append({"node": orb, "vel": dir.normalized() * 11.0, "life": 3.0})

func _tick_enemy_shots(delta: float) -> void:
	for i in range(enemy_shots.size() - 1, -1, -1):
		var shot: Dictionary = enemy_shots[i]
		var node: Node3D = shot["node"]
		node.position += (shot["vel"] as Vector3) * delta
		shot["life"] = float(shot["life"]) - delta
		if node.position.distance_to(pal_pos + Vector3(0, 1.5, 0)) < 2.2:
			_bump_pal(node.position)
			shot["life"] = 0.0
		if float(shot["life"]) <= 0.0:
			node.queue_free()
			enemy_shots.remove_at(i)

func _bump_pal(from: Vector3) -> void:
	var away: Vector3 = pal_pos - from
	away.y = 0.0
	if away.length() < 0.1:
		away = Vector3.FORWARD
	pal_pos += away.normalized() * 3.5
	m._sparkle_burst(pal_pos + Vector3(0, 2.0, 0), Color(0.55, 0.92, 1.0))
	m.show_msg(String(creature_def.get("name", "Stuffie")), "Boing! I'm okay! Tap the big DODGE bubble next time!", "talk")

# ---------- pointer / HUD / win ----------

func _tick_pointer() -> void:
	pointer.visible = state == "play"
	var target := _nearest_enemy()
	if target.is_empty():
		pointer.visible = false
		return
	pointer.position = (target["pos"] as Vector3) + Vector3(0, 7.2 + sin(elapsed * 4.0) * 0.45, 0)

func _update_hud() -> void:
	if objective == null:
		return
	if state == "won":
		objective.text = "✨  EVERYBODY'S FRIENDS NOW!  ✨"
		counter.text = "★"
		return
	if qte_t > 0.0:
		objective.text = "🛡  TAP THE BIG DODGE BUBBLE!"
	else:
		objective.text = "%s  tap %s and bop the wigglers — follow the golden arrow!" % ["🐦" if String(creature_def.get("kind", "")) == "bird" else "🐾", attack_word()]
	var active := 0
	for enemy in enemies:
		if String(enemy["state"]) != "friend":
			active += 1
	counter.text = "💗  %d" % active

func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = 3.5
	_qte_clear()
	pointer.visible = false
	_update_hud()
	m.show_msg(String(creature_def.get("name", "Stuffie")), "We did it! Everyone wants to play with us now!", "win")

func _finish() -> void:
	state = "done"
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call(round_tag)
	queue_free()

func cancel(notify_finish: bool = true) -> void:
	if state == "done":
		return
	if state == "won":
		_finish()   # the victory was already earned; leaving skips only the delay
		return
	state = "done"
	if prev_env != null:
		m.we_node.environment = prev_env
	if notify_finish and finish_cb.is_valid():
		finish_cb.call("")
	queue_free()
