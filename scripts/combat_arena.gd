class_name CombatArena
extends Node3D
# Child-friendly one-button combat arena. Enemies can bump Roshan, but there is
# no health bar and no fail state. All movement/collision is analytic so this
# stays inside the mobile performance budget.

const CENTER := Vector3(0.0, -2200.0, 0.0)
const RADIUS := 27.0
const MOVE_SPEED := 14.0

var m: ReefMain
var kind := "ice"
var finish_cb: Callable
var prev_env: Environment = null
var cam: Camera3D = null
var avatar: Sprite3D = null
var hud: CanvasLayer = null
var objective: Label = null
var counter: Label = null
var pointer: Label3D = null
var player_pos := Vector3.ZERO
var player_yaw := PI
var shot_cool := 0.0
var fire_prev := false
var elapsed := 0.0
var state := "play"
var win_t := 0.0
var bump_cool := 0.0
var enemies: Array[Dictionary] = []
var shots: Array[Dictionary] = []
var enemy_shots: Array[Dictionary] = []
var boss: Dictionary = {}
var encounter := {}
var room_tag := ""
var materials := {}

func start(main: ReefMain, battle_kind: String, done_cb: Callable, config: Dictionary = {}) -> void:
	m = main
	kind = battle_kind
	finish_cb = done_cb
	encounter = config
	room_tag = String(encounter.get("room_tag", ""))
	player_pos = CENTER + Vector3(0, 1.1, 8.0)
	_build_environment()
	_build_octagon()
	_build_avatar()
	_build_camera()
	_build_hud()
	if kind == "ice":
		_build_ice_swarm()
		m.show_msg("Roshan", "Ice Berry ready! Tap the big ICE button and freeze every mischief imp!", "talk")
	else:
		_build_pepper_boss()
		if kind == "dual":
			m.show_msg("Roshan", "Freeze the spinning shell with ICE, then use FIRE when the dragon-turtle peeks out!", "talk")
		else:
			m.show_msg("Roshan", "Spicy garden peppers! Tap FIRE when the turtle-lizard peeks out of its shell!", "talk")
	_update_hud()

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	var default_bg := Color(0.08, 0.05, 0.16) if kind == "ice" else Color(0.18, 0.055, 0.035)
	env.background_color = encounter.get("background", default_bg)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.65, 0.78, 1.0) if kind == "ice" else Color(1.0, 0.68, 0.42)
	env.ambient_light_energy = 0.9
	env.glow_enabled = true
	env.glow_intensity = 0.65
	env.glow_bloom = 0.12
	m._speedy_glow_clamp(env)
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(0.72, 0.86, 1.0) if kind == "ice" else Color(1.0, 0.72, 0.45)
	sun.light_energy = 1.15
	sun.shadow_enabled = m.quality != "speedy"
	sun.rotation_degrees = Vector3(-48, -28, 0)
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

func _mesh(parent: Node3D, mesh: Mesh, pos: Vector3, col: Color, emission: float = 0.0) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.mesh = mesh
	node.position = pos
	node.material_override = _mat(col, emission)
	parent.add_child(node)
	return node

func _sphere(parent: Node3D, pos: Vector3, radius: float, col: Color, emission: float = 0.0) -> MeshInstance3D:
	var shape := SphereMesh.new()
	shape.radius = radius
	shape.height = radius * 2.0
	shape.radial_segments = 12
	shape.rings = 6
	return _mesh(parent, shape, pos, col, emission)

func _build_octagon() -> void:
	var default_floor := Color(0.46, 0.55, 0.78) if kind == "ice" else Color(0.48, 0.25, 0.20)
	var default_trim := Color(0.55, 0.92, 1.0) if kind == "ice" else Color(1.0, 0.48, 0.20)
	var floor_col: Color = encounter.get("floor", default_floor)
	var trim_col: Color = encounter.get("trim", default_trim)
	var arena := DungeonArt.spawn("arena", self, CENTER)
	DungeonArt.tint(arena, _mat(floor_col), _mat(trim_col, 0.18))

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	var avatar_tex := load("res://assets/characters/roshan_sprite.png") as Texture2D
	avatar.texture = avatar_tex
	avatar.pixel_size = 6.2 / maxf(float(avatar_tex.get_height()), 1.0) if avatar_tex != null else 0.01
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.no_depth_test = false
	avatar.position = player_pos
	add_child(avatar)

func _build_camera() -> void:
	cam = Camera3D.new()
	cam.fov = 58.0
	cam.position = CENTER + Vector3(0, 30.0, 31.0)
	add_child(cam)
	cam.look_at(CENTER + Vector3(0, 1.5, 0), Vector3.UP)
	cam.make_current()

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 14
	add_child(hud)
	var banner := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.08, 0.18, 0.88)
	style.border_color = Color(0.55, 0.9, 1.0) if kind == "ice" else Color(1.0, 0.55, 0.25)
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
	pointer = Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 150
	pointer.pixel_size = 0.022
	pointer.outline_size = 24
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(pointer)

func _build_ice_swarm() -> void:
	var count: int = int(encounter.get("enemy_count", 8))
	var layout: String = String(encounter.get("layout", "ring"))
	for i in range(count):
		var a: float = float(i) * TAU / float(count)
		var spawn_r := 18.0
		if layout == "double":
			spawn_r = 11.0 if i % 2 == 0 else 20.0
		elif layout == "spiral":
			spawn_r = 9.0 + float(i) / maxf(float(count - 1), 1.0) * 12.0
		var pos := CENTER + Vector3(sin(a) * spawn_r, 1.0, cos(a) * spawn_r)
		var root := Node3D.new()
		root.position = pos
		add_child(root)
		DungeonArt.spawn("imp", root)
		enemies.append({"node": root, "pos": pos, "state": "active", "timer": 0.0, "attack": 1.0 + float(i) * 0.18, "phase": a})

func _build_pepper_boss() -> void:
	# A little basket makes the ability source readable even without text.
	DungeonArt.spawn("basket", self, CENTER + Vector3(-8.0, 0.7, 10.0))
	var root := DungeonArt.spawn("boss", self, CENTER + Vector3(0, 1.0, -10.0))
	root.scale = Vector3.ONE * 1.3
	var head := DungeonArt.find_part(root, "Head")
	var shell := DungeonArt.find_part(root, "Shell")
	var first_phase := "shell" if kind == "dual" else "peek"
	var first_time := float(encounter.get("shell_time", 4.5)) if kind == "dual" else float(encounter.get("peek_time", 4.5))
	boss = {"node": root, "head": head, "shell": shell, "hp": int(encounter.get("boss_hp", 7)), "phase": first_phase, "timer": first_time, "attack": 1.2, "pos": root.position}
	if kind == "dual":
		head.visible = false

func _move_input() -> Vector2:
	var value := Vector2.ZERO
	if Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT): value.x -= 1.0
	if Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT): value.x += 1.0
	if Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP): value.y -= 1.0
	if Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN): value.y += 1.0
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

func _process(delta: float) -> void:
	if m == null or state == "done":
		return
	elapsed += delta
	shot_cool = maxf(0.0, shot_cool - delta)
	bump_cool = maxf(0.0, bump_cool - delta)
	if state == "won":
		win_t -= delta
		if fmod(win_t, float(encounter.get("win_spark_gap", 0.32))) < delta:
			m._sparkle_burst(CENTER + Vector3(randf_range(-10.0, 10.0), randf_range(1.0, 6.0), randf_range(-8.0, 8.0)), Color.from_hsv(randf(), 0.55, 1.0))
		if win_t <= 0.0:
			_finish()
		return
	var move := _move_input()
	player_pos += Vector3(move.x, 0, move.y) * MOVE_SPEED * delta
	var flat := Vector2(player_pos.x - CENTER.x, player_pos.z - CENTER.z)
	if flat.length() > RADIUS - 3.0:
		flat = flat.normalized() * (RADIUS - 3.0)
		player_pos.x = CENTER.x + flat.x
		player_pos.z = CENTER.z + flat.y
	if move.length() > 0.08:
		player_yaw = atan2(move.x, move.y)
	avatar.position = player_pos + Vector3(0, sin(elapsed * 4.0) * 0.12, 0)
	if _action_pressed() and shot_cool <= 0.0:
		_fire()
	_tick_shots(delta)
	_tick_enemy_shots(delta)
	if kind == "ice":
		_tick_imps(delta)
	else:
		_tick_boss(delta)
	_tick_pointer()

func _nearest_target() -> Vector3:
	if kind != "ice" and not boss.is_empty():
		return boss["pos"]
	var best := CENTER
	var best_d := INF
	for enemy in enemies:
		if String(enemy["state"]) != "active":
			continue
		var dist: float = player_pos.distance_squared_to(enemy["pos"])
		if dist < best_d:
			best_d = dist
			best = enemy["pos"]
	return best

func _fire() -> void:
	var power := action_label().to_lower()
	var target := _nearest_target()
	var dir: Vector3 = target - player_pos
	dir.y = 0.0
	if dir.length() < 0.1:
		dir = Vector3(sin(player_yaw), 0, cos(player_yaw))
	dir = dir.normalized()
	var orb_col := Color(0.55, 0.92, 1.0) if power == "ice" else Color(1.0, 0.25, 0.06)
	var orb := _sphere(self, player_pos + Vector3(0, 2.2, 0) + dir * 1.5, 0.65, orb_col, 1.8)
	shots.append({"node": orb, "vel": dir * 27.0, "life": 1.6, "power": power})
	shot_cool = 0.32
	player_yaw = atan2(dir.x, dir.z)

func _tick_shots(delta: float) -> void:
	for i in range(shots.size() - 1, -1, -1):
		var shot: Dictionary = shots[i]
		var node: Node3D = shot["node"]
		node.position += (shot["vel"] as Vector3) * delta
		shot["life"] = float(shot["life"]) - delta
		var hit := false
		if kind == "ice":
			for enemy in enemies:
				if String(enemy["state"]) == "active" and node.position.distance_to((enemy["pos"] as Vector3) + Vector3(0, 2.2, 0)) < 2.6:
					_freeze_imp(enemy)
					hit = true
					break
		elif not boss.is_empty() and node.position.distance_to((boss["pos"] as Vector3) + Vector3(0, 2.5, 0)) < 5.2:
			_hit_boss(String(shot.get("power", "fire")))
			hit = true
		if hit or float(shot["life"]) <= 0.0:
			node.queue_free()
			shots.remove_at(i)

func _freeze_imp(enemy: Dictionary) -> void:
	if String(enemy["state"]) != "active":
		return
	enemy["state"] = "frozen"
	enemy["timer"] = 1.7
	var node: Node3D = enemy["node"]
	DungeonArt.apply_material(node, _mat(Color(0.45, 0.88, 1.0), 0.45))
	m._sparkle_burst(enemy["pos"] + Vector3(0, 2.5, 0), Color(0.55, 0.92, 1.0))
	_update_hud()

func _tick_imps(delta: float) -> void:
	var remaining := 0
	for enemy in enemies:
		var node: Node3D = enemy["node"]
		if String(enemy["state"]) == "active":
			remaining += 1
			var pos: Vector3 = enemy["pos"]
			var toward: Vector3 = player_pos - pos
			toward.y = 0.0
			if toward.length() > 7.0:
				pos += toward.normalized() * delta * float(encounter.get("imp_speed", 1.5))
			enemy["pos"] = pos
			node.position = pos + Vector3(0, sin(elapsed * 3.0 + float(enemy["phase"])) * 0.25, 0)
			enemy["attack"] = float(enemy["attack"]) - delta
			if float(enemy["attack"]) <= 0.0:
				enemy["attack"] = float(encounter.get("attack_gap", 3.0)) + randf() * 1.5
				_spawn_enemy_shot(pos + Vector3(0, 2.4, 0), player_pos, Color(0.72, 0.34, 0.92))
		elif String(enemy["state"]) == "frozen":
			remaining += 1
			enemy["timer"] = float(enemy["timer"]) - delta
			node.scale = Vector3.ONE * (1.0 + sin(elapsed * 12.0) * 0.04)
			if float(enemy["timer"]) <= 0.0:
				_pop_imp(enemy)
	if remaining == 0:
		_win()

func _pop_imp(enemy: Dictionary) -> void:
	enemy["state"] = "popped"
	var pos: Vector3 = enemy["pos"]
	(enemy["node"] as Node3D).visible = false
	var corn_count := int(encounter.get("popcorn_count", 7))
	for i in range(corn_count):
		var a: float = float(i) * TAU / float(corn_count)
		var corn := _sphere(self, pos + Vector3(cos(a) * 1.2, 1.0 + float(i % 3), sin(a) * 1.2), 0.42, Color(1.0, 0.92, 0.62), 0.25)
		var tw := corn.create_tween()
		tw.tween_property(corn, "position", corn.position + Vector3(cos(a) * 3.0, 3.0 + randf() * 2.0, sin(a) * 3.0), 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(corn, "scale", Vector3.ZERO, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
		tw.tween_callback(corn.queue_free)
	m._sparkle_burst(pos + Vector3(0, 2.0, 0), Color(1.0, 0.85, 0.45))
	_update_hud()

func _hit_boss(power: String = "fire") -> void:
	if state != "play":
		return
	var phase := String(boss["phase"])
	if kind == "dual" and phase == "shell":
		if power == "ice":
			boss["phase"] = "peek"
			boss["timer"] = float(encounter.get("peek_time", 3.2))
			boss["attack"] = 0.55
			m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.55, 0.92, 1.0))
			m.show_msg("Roshan", "Frozen shell! Now use FIRE on the peeking dragon-turtle!", "talk")
		else:
			m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.65, 0.85, 0.55))
		return
	if phase == "shell" or (kind == "dual" and power != "fire"):
		m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.65, 0.85, 0.55))
		return
	boss["hp"] = int(boss["hp"]) - 1
	m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 3.0, 3.5), Color(1.0, 0.3, 0.08))
	if int(boss["hp"]) <= 0:
		_win()
	elif kind == "dual":
		boss["phase"] = "shell"
		boss["timer"] = float(encounter.get("shell_time", 5.0))
		boss["attack"] = 0.8
	_update_hud()

func _tick_boss(delta: float) -> void:
	if boss.is_empty() or state != "play":
		return
	var root: Node3D = boss["node"]
	boss["timer"] = float(boss["timer"]) - delta
	boss["attack"] = float(boss["attack"]) - delta
	var phase: String = boss["phase"]
	if phase == "peek":
		(boss["head"] as Node3D).visible = true
		root.rotation.y = sin(elapsed * 1.4) * 0.18
		if float(boss["attack"]) <= 0.0:
			boss["attack"] = float(encounter.get("attack_gap", 1.25))
			if (boss["pos"] as Vector3).distance_to(player_pos) < 9.0:
				# The bright ivory claws swipe, but Roshan's bubble shield makes
				# contact playful: a push and sparkles, never damage or failure.
				_bump_player(boss["pos"])
			else:
				_spawn_enemy_shot((boss["pos"] as Vector3) + Vector3(0, 3.2, 4.2), player_pos, Color(1.0, 0.24, 0.04))
		if float(boss["timer"]) <= 0.0:
			boss["phase"] = "shell"
			boss["timer"] = float(encounter.get("shell_time", 2.8))
			boss["attack"] = 0.8
	else:
		(boss["head"] as Node3D).visible = false
		root.rotate_y(delta * 6.0)
		var pos: Vector3 = boss["pos"]
		var chase: Vector3 = player_pos - pos
		chase.y = 0.0
		if chase.length() > 1.0:
			pos += chase.normalized() * delta * float(encounter.get("shell_speed", 5.5))
		boss["pos"] = pos
		root.position = pos
		if pos.distance_to(player_pos) < 6.0:
			_bump_player(pos)
		if float(boss["timer"]) <= 0.0 and kind == "dual":
			# No fail state: keep presenting the required ice action and repeat
			# the picture/voice hint until the child freezes the shell.
			boss["timer"] = 1.5
			m.show_msg("Roshan", "The shell keeps spinning. Freeze it with ICE!", "talk")
		elif float(boss["timer"]) <= 0.0:
			boss["phase"] = "peek"
			boss["timer"] = float(encounter.get("peek_time", 4.8))
			boss["attack"] = 0.35
			var back: Vector3 = CENTER + Vector3(0, 1.0, -10.0)
			boss["pos"] = back
			root.position = back
	_update_hud()

func _spawn_enemy_shot(from: Vector3, to: Vector3, col: Color) -> void:
	var dir: Vector3 = to - from
	dir.y = 0.0
	if dir.length() < 0.1:
		return
	var orb := _sphere(self, from, 0.58, col, 1.4)
	enemy_shots.append({"node": orb, "vel": dir.normalized() * 10.0, "life": 3.5})

func _tick_enemy_shots(delta: float) -> void:
	for i in range(enemy_shots.size() - 1, -1, -1):
		var shot: Dictionary = enemy_shots[i]
		var node: Node3D = shot["node"]
		node.position += (shot["vel"] as Vector3) * delta
		shot["life"] = float(shot["life"]) - delta
		if node.position.distance_to(player_pos + Vector3(0, 1.5, 0)) < 2.0:
			_bump_player(node.position)
			shot["life"] = 0.0
		if float(shot["life"]) <= 0.0:
			node.queue_free()
			enemy_shots.remove_at(i)

func _bump_player(from: Vector3) -> void:
	var away: Vector3 = player_pos - from
	away.y = 0.0
	if away.length() < 0.1:
		away = Vector3.FORWARD
	player_pos += away.normalized() * 3.5
	m._sparkle_burst(player_pos + Vector3(0, 2.0, 0), Color(0.55, 0.92, 1.0))
	if bump_cool <= 0.0:
		bump_cool = 4.0
		m.show_msg("Roshan", "My bubble shield bounced it away! Keep going!", "talk")

func _tick_pointer() -> void:
	var target := _nearest_target()
	pointer.visible = state == "play"
	pointer.position = target + Vector3(0, 7.2 + sin(elapsed * 4.0) * 0.45, 0)

func _update_hud() -> void:
	if objective == null:
		return
	if kind == "ice":
		var left := 0
		for enemy in enemies:
			if String(enemy["state"]) != "popped": left += 1
		objective.text = (room_tag + "  •  " if room_tag != "" else "") + "🫐  ICE BERRY: tap ICE • follow the golden arrow  ❄"
		counter.text = "❄  %d" % left
	else:
		var shell: bool = not boss.is_empty() and String(boss["phase"]) == "shell"
		var action_text := "❄  FREEZE THE SPINNING SHELL!" if kind == "dual" and shell else ("🔥  PEEKING — USE FIRE!" if kind == "dual" else ("🌶  SHELL UP — dodge!" if shell else "🌶  PEEKING — tap FIRE!"))
		objective.text = (room_tag + "  •  " if room_tag != "" else "") + action_text
		counter.text = "🔥  %d" % maxi(0, int(boss.get("hp", 0)))

func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = float(encounter.get("win_time", 3.5))
	pointer.visible = false
	objective.text = "✨  POPCORN PARTY!  ✨" if kind == "ice" else "✨  DRAGON-TURTLE TAMED!  ✨"
	counter.text = "★"
	if kind == "ice":
		m.show_msg("Roshan", "Pop pop pop! The frozen imps melted into popcorn!", "win")
	else:
		m.show_msg("Roshan", "The spicy peppers did it! The turtle-lizard wants to be friends!", "win")

func _finish() -> void:
	state = "done"
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call(kind)
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

func action_label() -> String:
	if kind == "ice":
		return "ICE"
	if kind == "dual" and not boss.is_empty() and String(boss.get("phase", "shell")) == "shell":
		return "ICE"
	return "FIRE"
