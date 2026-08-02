class_name CombatArena
extends Node3D
# Child-friendly one-button combat arena. Enemies can bump Roshan, but there is
# no health bar and no fail state. All movement/collision is analytic so this
# stays inside the mobile performance budget.

const CENTER := Vector3(0.0, -2200.0, 0.0)
const RADIUS := 27.0
const MOVE_SPEED := 14.0
const CLEAN_BUBBLE_PATH := "res://assets/sprites/dust_bunnies/dust_bunny_clean_bubbles.png"
const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")

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
var he: HitEngine = null
var imp_brain: ImpAI = null      # the shared crew brain (scripts/imp_ai.gd)
var pa: PartnerAssist = null
var encounter := {}
var room_tag := ""
var art_theme := ""
var materials := {}
var mic_live := false   # microphone armed AND both spells taught

func start(main: ReefMain, battle_kind: String, done_cb: Callable, config: Dictionary = {}) -> void:
	m = main
	kind = battle_kind
	finish_cb = done_cb
	encounter = config
	room_tag = String(encounter.get("room_tag", ""))
	art_theme = String(encounter.get("art_theme", ""))
	player_pos = CENTER + Vector3(0, 1.1, 8.0)
	_build_environment()
	_build_octagon()
	_build_avatar()
	_build_camera()
	_build_hud()
	# the shared hit pipeline: taps and projectiles both damage through it
	he = HitEngine.new(m)
	he.fx_root = self
	he.camera = cam
	he.on_hit = Callable(self, "_on_engine_hit")
	# Spoken spells are an ADDITION to the buttons, never a replacement: the
	# hint is only spoken when the microphone is actually listening and the
	# words have actually been taught (MIC_SPELLS.md).
	mic_live = _arm_mic()
	if kind == "ice":
		var ice_msg := "Ice Berry ready! Tap the big ICE button and freeze every mischief imp!"
		if m.touch_uses_explicit_interactions():
			ice_msg += " Or tap an imp right on its nose!"
		if mic_live:
			ice_msg += " Or shout FREEZE!"
		_build_ice_swarm()
		m.show_msg("Roshan", ice_msg, "talk")
	elif kind == "dust":
		_build_dust_bunny_swarm()
		m.show_msg("Roshan", "Dust bunnies! Tap the big CLEAN button and give each one a sparkling bubble poof!", "talk")
	else:
		_build_pepper_boss()
		if kind == "dual":
			var dual_msg := "Freeze the spinning shell with ICE, then use FIRE when the dragon-turtle peeks out!"
			if mic_live:
				dual_msg += " You can shout FREEZE and FIREBALL too!"
			m.show_msg("Roshan", dual_msg, "talk")
		else:
			var fire_msg := "Spicy garden peppers! Tap FIRE when the turtle-lizard peeks out of its shell!"
			if mic_live:
				fire_msg += " Or shout FIREBALL!"
			m.show_msg("Roshan", fire_msg, "talk")
	he.targets = enemies if kind in ["ice", "dust"] else [boss]
	m.hit_engines.append(he)   # enemy priority: this battle's taps outrank the world
	# Partner Assist: the following stuffie brings her SPARKLE STAMPEDE super
	# on a 12 s cooldown (per-partner supers, owner 2026-08-01)
	if m.companion_id != "":
		pa = PartnerAssist.new(m)
		pa.attach("stuffie", Callable(self, "_partner_super"))
	_update_hud()

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	var default_bg := Color(0.18, 0.055, 0.035)
	if kind == "ice":
		default_bg = Color(0.08, 0.05, 0.16)
	elif kind == "dust":
		default_bg = Color(0.14, 0.08, 0.22)
	env.background_color = encounter.get("background", default_bg)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1.0, 0.68, 0.42)
	if kind == "ice":
		env.ambient_light_color = Color(0.65, 0.78, 1.0)
	elif kind == "dust":
		env.ambient_light_color = Color(0.88, 0.78, 1.0)
	env.ambient_light_energy = 0.9
	env.glow_enabled = true
	env.glow_intensity = 0.65
	env.glow_bloom = 0.12
	m._speedy_glow_clamp(env)
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(1.0, 0.72, 0.45)
	if kind == "ice":
		sun.light_color = Color(0.72, 0.86, 1.0)
	elif kind == "dust":
		sun.light_color = Color(0.92, 0.84, 1.0)
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
	var default_floor := Color(0.48, 0.25, 0.20)
	var default_trim := Color(1.0, 0.48, 0.20)
	if kind == "ice":
		default_floor = Color(0.46, 0.55, 0.78)
		default_trim = Color(0.55, 0.92, 1.0)
	elif kind == "dust":
		default_floor = Color(0.52, 0.43, 0.68)
		default_trim = Color(0.58, 0.96, 1.0)
	var floor_col: Color = encounter.get("floor", default_floor)
	var trim_col: Color = encounter.get("trim", default_trim)
	var arena := DungeonArt.spawn("arena", self, CENTER, art_theme)
	DungeonArt.tint(arena, _mat(floor_col), _mat(trim_col, 0.18))

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	avatar.pixel_size = 6.2 / 256.0
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.no_depth_test = false
	avatar.position = player_pos
	add_child(avatar)
	var animator := ROSHAN_SPRITE_LOOP.new()
	avatar.add_child(animator)
	animator.setup_sprite_3d(avatar, false, avatar)

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
	var accent := StorybookUI.CORAL
	if kind == "ice":
		accent = StorybookUI.MINT
	elif kind == "dust":
		accent = StorybookUI.LAVENDER
	var banner := StorybookUI.add_hud_panel(hud, Rect2(220, 22, 840, 112), accent, Color(0.94, 0.98, 1.0, 0.96), 32)
	banner.name = "CombatObjectiveCard"
	objective = Label.new()
	objective.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	StorybookUI.style_hud_label(objective, 28)
	objective.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	objective.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	objective.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	banner.add_child(objective)
	var counter_card := StorybookUI.add_hud_panel(hud, Rect2(24, 22, 172, 112), accent, Color(0.94, 0.98, 1.0, 0.96), 32)
	counter_card.name = "CombatProgressCard"
	counter = Label.new()
	counter.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	counter.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	counter.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_hud_label(counter, 34)
	counter_card.add_child(counter)
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
	# the shared crew brain (scripts/imp_ai.gd): arena metres, and the
	# encounter's own imp_speed still sets the crew's walking pace
	var pace: float = maxf(1.0, float(encounter.get("imp_speed", 1.5))) * 2.6
	imp_brain = ImpAI.new({
		"strike_range": 12.0,
		"stand_off": 7.5,
		"contact": 3.4,
		"speed": pace,
		"charge_speed": pace * 3.4,
		"flee_speed": pace * 1.6,
		"windup": 1.0,
		"charge_time": 0.45,
		"slash_time": 0.28,
		"recover": 1.25,
		"cool_min": float(encounter.get("attack_gap", 3.0)) * 0.8,
		"cool_max": float(encounter.get("attack_gap", 3.0)) * 1.7,
		"max_attackers": 2,
	}, room_tag.hash() + count * 31)
	imp_brain.begin_crew(count)
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
		DungeonArt.spawn("imp", root, Vector3.ZERO, art_theme)
		var mind: Dictionary = imp_brain.spawn_mind(i, false)
		mind["pos"] = Vector2(pos.x, pos.z)
		enemies.append({"node": root, "pos": pos, "state": "active", "timer": 0.0,
			"attack": 1.0 + float(i) * 0.18, "phase": a, "ai": mind,
			"pose": "prowl", "hp": int(encounter.get("imp_hp", 3))})


func _build_dust_bunny_swarm() -> void:
	var count: int = int(encounter.get("enemy_count", 5))
	var layout: String = String(encounter.get("layout", "spiral"))
	var seed_base: int = int(encounter.get("dust_seed", 20260728))
	for i in range(count):
		var angle: float = float(i) * TAU / float(count)
		var spawn_radius: float = 16.0
		if layout == "double":
			spawn_radius = 11.0 if i % 2 == 0 else 19.0
		elif layout == "spiral":
			spawn_radius = 9.0 + float(i) / maxf(float(count - 1), 1.0) * 10.0
		var pos := CENTER + Vector3(
			sin(angle) * spawn_radius,
			1.0,
			cos(angle) * spawn_radius
		)
		var bunny := DustBunnySprite.new()
		bunny.position = pos
		add_child(bunny)
		var brain := DustBunnyAI.new()
		brain.setup(pos, CENTER, RADIUS - 3.0, seed_base + i * 101, 0.25 + float(i) * 0.12)
		enemies.append({
			"node": bunny,
			"brain": brain,
			"pos": pos,
			"state": "active",
			"timer": 0.0,
			"phase": angle,
			"type": "dust_bunny",
		})


func _build_pepper_boss() -> void:
	# A little basket makes the ability source readable even without text.
	DungeonArt.spawn("basket", self, CENTER + Vector3(-8.0, 0.7, 10.0), art_theme)
	var root := DungeonArt.spawn("boss", self, CENTER + Vector3(0, 1.0, -10.0), art_theme)
	root.scale = Vector3.ONE * 1.3
	var head := DungeonArt.find_part(root, "Head")
	var shell := DungeonArt.find_part(root, "Shell")
	var first_phase := "shell" if kind == "dual" else "peek"
	var first_time := float(encounter.get("shell_time", 4.5)) if kind == "dual" else float(encounter.get("peek_time", 4.5))
	boss = {"node": root, "head": head, "shell": shell, "hp": int(encounter.get("boss_hp", 7)), "phase": first_phase, "timer": first_time, "attack": 1.2, "pos": root.position, "aim_h": 3.0, "screen_radius": 170.0}
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

# Opens the capture device for this battle only. Returns true when a spoken
# spell can actually land, so callers never promise the child something the
# permission state or an untaught word cannot deliver.
func _arm_mic() -> bool:
	if m == null or not m.mic_on:
		return false
	var mic: MicInput = m._mic_ref()
	mic.arm()
	return m.mic_state == "listening" and mic.all_words_taught()

# A recognised spell word, mapped to a power this arena can actually cast. A
# word this battle has no use for is silently dropped — saying FIREBALL at the
# imps simply does nothing, which is the no-fail-state rule applied to speech.
func _mic_power() -> String:
	if state != "play" or not mic_live or m == null or m.mic_sys == null:
		return ""
	var word: String = m.mic_sys.poll_word()
	if word == "":
		return ""
	if kind == "dual":
		return word          # the spoken word chooses the power
	return word if word == kind else ""

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
	if he != null:
		he.tick(delta)   # pop-chain window decay (a lapsed chain fades silently)
	if pa != null:
		pa.tick(delta)
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
	var spoken: String = _mic_power()
	if spoken != "" and shot_cool <= 0.0:
		_fire(spoken)
	elif _action_pressed() and shot_cool <= 0.0:
		_fire()
	_tick_shots(delta)
	_tick_enemy_shots(delta)
	if kind == "ice":
		_tick_imps(delta)
	elif kind == "dust":
		_tick_dust_bunnies(delta)
	else:
		_tick_boss(delta)
	_tick_pointer()

# A screen tap from the touch router (Hybrid mode). The engine picks the
# enemy under the finger and routes it through the shared hit() interface —
# the same path the projectiles take.
func on_world_tap(screen_pos: Vector2) -> void:
	if state != "play" or he == null:
		return
	he.tap(screen_pos)

# Every damage source lands here with its origin: "tap", "shot_ice",
# "shot_fire" today; combo verbs tomorrow. Imps freeze into the popcorn
# death; the boss keeps its phase rules whatever the source.
func _on_engine_hit(enemy: Dictionary, damage: int, source: String) -> void:
	if kind == "ice":
		if imp_brain != null:
			imp_brain.on_player_swing(true)
		# every landed hit chains 1-2-3; the armed hit after chain 3 is the
		# SUPER: +2 damage (a basic imp is out in one) plus a 1-damage splash
		# to the nearby swarm — harmed or felled by their own hp
		var super_now: bool = he.consume_super()
		if super_now:
			damage += 2
		he.note_hit(enemy["pos"] as Vector3)
		if pa != null:
			pa.note_child_pop()
		_damage_imp(enemy, damage)
		if super_now:
			m._sparkle_burst((enemy["pos"] as Vector3) + Vector3(0, 3.5, 0), Color(1.0, 0.95, 0.6))
			for other in enemies:
				if other != enemy and String(other["state"]) == "active" and (other["pos"] as Vector3).distance_to(enemy["pos"] as Vector3) < HitEngine.SUPER_R:
					_damage_imp(other, 1)
		return
	if kind == "dust":
		_clean_dust_bunny(enemy)
		return
	var power: String = source.trim_prefix("shot_") if source.begins_with("shot_") else action_label().to_lower()
	_hit_boss(power)

# The damage grammar's harm-or-eliminate rule: a surviving imp plays the
# shared harm animation; an emptied one freezes into the popcorn finale.
func _damage_imp(enemy: Dictionary, damage: int) -> void:
	if String(enemy["state"]) != "active":
		return
	enemy["hp"] = maxi(0, int(enemy.get("hp", 3)) - damage)
	if int(enemy["hp"]) > 0:
		he.play_harm(enemy)
	else:
		_freeze_imp(enemy)

func _nearest_target() -> Vector3:
	if kind not in ["ice", "dust"] and not boss.is_empty():
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

func _fire(power_override: String = "") -> void:
	# power_override is set when a spoken spell named the power; otherwise the
	# button casts whatever this arena's phase logic currently offers.
	var power: String = power_override if power_override != "" else action_label().to_lower()
	var target := _nearest_target()
	var dir: Vector3 = target - player_pos
	dir.y = 0.0
	if dir.length() < 0.1:
		dir = Vector3(sin(player_yaw), 0, cos(player_yaw))
	dir = dir.normalized()
	var shot_pos: Vector3 = player_pos + Vector3(0, 2.2, 0) + dir * 1.5
	var orb: Node3D
	if power == "clean":
		orb = _clean_bubble_projectile(shot_pos)
	else:
		var role := "ice_berry_projectile" if power == "ice" else "pepper_projectile"
		orb = DungeonArt.spawn(role, self, shot_pos, art_theme)
		if orb.name.begins_with("MissingDungeonArt"):
			var orb_col := Color(0.55, 0.92, 1.0) if power == "ice" else Color(1.0, 0.25, 0.06)
			orb.queue_free()
			orb = _sphere(self, shot_pos, 0.65, orb_col, 1.8)
		else:
			orb.scale = Vector3.ONE * (0.82 if power == "ice" else 0.74)
			orb.rotation.y = atan2(dir.x, dir.z)
	shots.append({"node": orb, "vel": dir * 27.0, "life": 1.6, "power": power})
	shot_cool = 0.32
	player_yaw = atan2(dir.x, dir.z)


func _clean_bubble_projectile(pos: Vector3) -> Sprite3D:
	var bubble := Sprite3D.new()
	var texture: Texture2D = load(CLEAN_BUBBLE_PATH) as Texture2D
	bubble.name = "CleanBubbleProjectile"
	bubble.texture = texture
	bubble.position = pos
	bubble.pixel_size = 3.2 / maxf(float(texture.get_height()), 1.0) if texture != null else 0.006
	bubble.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	bubble.shaded = false
	bubble.double_sided = true
	bubble.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	bubble.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(bubble)
	return bubble


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
					he.hit(enemy, 1, "shot_ice")
					hit = true
					break
		elif kind == "dust":
			for enemy in enemies:
				if String(enemy["state"]) == "active" and node.position.distance_to((enemy["pos"] as Vector3) + Vector3(0, 2.2, 0)) < 2.8:
					_clean_dust_bunny(enemy)
					hit = true
					break
		elif not boss.is_empty() and node.position.distance_to((boss["pos"] as Vector3) + Vector3(0, 2.5, 0)) < 5.2:
			he.hit(boss, 1, "shot_" + String(shot.get("power", "fire")))
			hit = true
		if hit or float(shot["life"]) <= 0.0:
			node.queue_free()
			shots.remove_at(i)

## One imp, one pose, played on the transform — the toy imps carry no
## animation clips, so the crouch, the dash, the swipe and the slumped
## recovery are all built here (art states: the codex handoff).
func _pose_imp(node: Node3D, pos: Vector3, pose: String, t: float, phase: float) -> void:
	var hop: float = sin(elapsed * 3.0 + phase) * 0.25
	var squash := Vector3.ONE
	var tilt := 0.0
	match pose:
		"windup":
			hop = -0.1
			squash = Vector3(1.22, 0.76, 1.22)
			tilt = -0.24
		"charge":
			hop = 0.45
			squash = Vector3(0.88, 1.2, 0.88)
			tilt = 0.34
		"slash":
			hop = 0.3
			squash = Vector3(1.14, 0.94, 1.14)
			tilt = lerpf(-0.6, 0.6, clampf(t / 0.28, 0.0, 1.0))
		"recover":
			hop = -0.05
			squash = Vector3(1.16, 0.82, 1.16)
			tilt = -0.32
		"stagger":
			node.rotate_y(0.14)
			squash = Vector3(1.1, 0.9, 1.1)
		"taunt", "rally":
			hop = absf(sin(t * 9.0)) * 0.7
			squash = Vector3(0.94, 1.1, 0.94)
		"flee":
			hop = absf(sin(elapsed * 9.0 + phase)) * 0.6
			tilt = -0.2
	node.position = pos + Vector3(0.0, hop, 0.0)
	node.scale = squash
	node.rotation.z = tilt
	if pose != "stagger":
		var look: Vector3 = player_pos - pos
		if pose == "flee":
			look = -look
		if Vector2(look.x, look.z).length() > 0.05:
			node.rotation.y = atan2(look.x, look.z)


func _arena_brain_events() -> void:
	for ev: Dictionary in imp_brain.drain_events():
		var at: Vector2 = ev.get("pos", Vector2.ZERO)
		var world_at := CENTER + Vector3(at.x, 2.4, at.y)
		match String(ev.get("kind", "")):
			"telegraph":
				m._sparkle_burst(world_at + Vector3(0, 1.2, 0), Color(1.0, 0.82, 0.3))
			"charge":
				m._sparkle_burst(world_at, Color(1.0, 0.7, 0.45))
			"contact":
				# still just the bubble-shield bump: a push and sparkles
				_bump_player(world_at)
			"whiff":
				m._sparkle_burst(world_at, Color(0.9, 0.95, 1.0))
			"taunt", "rally":
				m._sparkle_burst(world_at + Vector3(0, 1.0, 0), Color(1.0, 0.72, 0.88))


func _freeze_imp(enemy: Dictionary) -> void:
	if String(enemy["state"]) != "active":
		return
	enemy["state"] = "frozen"
	enemy["timer"] = 1.7
	var mind: Dictionary = enemy.get("ai", {})
	if imp_brain != null and not mind.is_empty():
		# frozen imps stop deciding, and the crew feels the gap
		imp_brain.on_hit(mind, true)
	var node: Node3D = enemy["node"]
	DungeonArt.apply_material(node, _mat(Color(0.45, 0.88, 1.0), 0.45))
	m._audio_ref().sfx("combat_freeze")
	m._sparkle_burst(enemy["pos"] + Vector3(0, 2.5, 0), Color(0.55, 0.92, 1.0))
	_update_hud()

func _tick_imps(delta: float) -> void:
	# the crew decides together: who closes in, who telegraphs a lunge, who
	# hangs back and throws instead (scripts/imp_ai.gd)
	var hero := Vector2(player_pos.x - CENTER.x, player_pos.z - CENTER.z)
	if imp_brain != null:
		var minds: Array = []
		for enemy in enemies:
			var mind: Dictionary = enemy.get("ai", {})
			if mind.is_empty():
				continue
			var live: bool = String(enemy["state"]) == "active"
			mind["alive"] = live
			if live:
				var at: Vector3 = enemy["pos"]
				mind["pos"] = Vector2(at.x - CENTER.x, at.z - CENTER.z)
				minds.append(mind)
		imp_brain.tick(delta, minds, hero)
		_arena_brain_events()
	var remaining := 0
	for enemy in enemies:
		var node: Node3D = enemy["node"]
		if String(enemy["state"]) == "active":
			remaining += 1
			# partner-stunned imps just spin dizzily — no chasing, no shots
			var stun: float = float(enemy.get("stun_t", 0.0))
			if stun > 0.0:
				enemy["stun_t"] = stun - delta
				node.rotation.y += delta * 6.0
				continue
			var pos: Vector3 = enemy["pos"]
			var mind: Dictionary = enemy.get("ai", {})
			var pose := "prowl"
			var state_t := 0.0
			if not mind.is_empty():
				var want: Vector2 = mind.get("pos", Vector2(pos.x - CENTER.x, pos.z - CENTER.z))
				# the floor is the truth: nobody walks through the trim
				if want.length() > RADIUS - 2.5:
					want = want.normalized() * (RADIUS - 2.5)
				mind["pos"] = want
				pos = Vector3(CENTER.x + want.x, pos.y, CENTER.z + want.y)
				pose = String(mind.get("pose", "prowl"))
				state_t = float(mind.get("t", 0.0))
			enemy["pos"] = pos
			enemy["pose"] = pose
			_pose_imp(node, pos, pose, state_t, float(enemy["phase"]))
			# an imp that cannot reach her throws instead of standing about
			enemy["attack"] = float(enemy["attack"]) - delta
			var far: bool = pos.distance_to(player_pos) > 13.0
			var settled: bool = pose == "prowl" or pose == "stalk" or pose == "flank" or pose == "taunt"
			if float(enemy["attack"]) <= 0.0 and far and settled:
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
	# the dying animation now lives in the shared engine as the "pop" style
	he.play_death(enemy, "pop", {"count": int(encounter.get("popcorn_count", 7)), "art_theme": art_theme})
	_update_hud()

func _clean_dust_bunny(enemy: Dictionary) -> void:
	if String(enemy["state"]) != "active":
		return
	enemy["state"] = "cleaning"
	var bunny: DustBunnySprite = enemy["node"] as DustBunnySprite
	var direction_x: float = (enemy["pos"] as Vector3).x - player_pos.x
	var duration: float = bunny.play_defeat(direction_x)
	enemy["timer"] = maxf(duration, 0.1)
	_update_hud()


func _tick_dust_bunnies(delta: float) -> void:
	var remaining := 0
	for enemy in enemies:
		var bunny: DustBunnySprite = enemy["node"] as DustBunnySprite
		var enemy_state: String = String(enemy["state"])
		if enemy_state == "active":
			remaining += 1
			var brain: DustBunnyAI = enemy["brain"] as DustBunnyAI
			var events: Dictionary = brain.tick(delta, player_pos)
			enemy["pos"] = brain.pos
			bunny.position = brain.pos
			if StringName(events["action"]) == &"hop":
				bunny.play_hop(brain.facing_x)
			if bool(events["bump"]):
				_bump_player(brain.pos)
		elif enemy_state == "cleaning":
			remaining += 1
			enemy["timer"] = float(enemy["timer"]) - delta
			if float(enemy["timer"]) <= 0.0:
				_finish_dust_bunny_clean(enemy)
	if remaining == 0:
		_win()


func _finish_dust_bunny_clean(enemy: Dictionary) -> void:
	enemy["state"] = "popped"
	var bunny: DustBunnySprite = enemy["node"] as DustBunnySprite
	bunny.visible = false
	_update_hud()


# The partner SUPER (PartnerAssist fires this only from the child's tap).
# Stuffie — SPARKLE STAMPEDE: pops the nearest fodder outright, dizzies the
# rest, and grants Big Taps so her own next freezes pop almost instantly.
# Boss arenas: never defeats — extends the peek window and chips one point.
func _partner_super(_partner_kind: String) -> void:
	if state != "play":
		return
	if kind == "ice":
		var actives: Array[Dictionary] = []
		for enemy in enemies:
			if String(enemy["state"]) == "active":
				actives.append(enemy)
		actives.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
			return (a["pos"] as Vector3).distance_to(player_pos) < (b["pos"] as Vector3).distance_to(player_pos))
		for i in range(actives.size()):
			var enemy: Dictionary = actives[i]
			if i < PartnerAssist.STAMPEDE_POPS:
				enemy["hp"] = 0
				_freeze_imp(enemy)
				enemy["timer"] = 0.05
			else:
				enemy["stun_t"] = PartnerAssist.STUN_T
			m._sparkle_burst((enemy["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(0.95, 0.75, 1.0))
		he.big_taps = PartnerAssist.BIG_TAPS
	elif not boss.is_empty():
		boss["timer"] = float(boss["timer"]) + PartnerAssist.STUN_T
		if String(boss["phase"]) == "peek":
			boss["hp"] = maxi(0, int(boss["hp"]) - 1)
			m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.95, 0.75, 1.0))
			if int(boss["hp"]) <= 0:
				_win()
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
			m._audio_ref().sfx("combat_freeze")
			m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.55, 0.92, 1.0))
			m.show_msg("Roshan", "Frozen shell! Now use FIRE on the peeking dragon-turtle!", "talk")
		else:
			m._audio_ref().sfx("combat_fizzle", 0.9, -8.0)
			m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.65, 0.85, 0.55))
		return
	if phase == "shell" or (kind == "dual" and power != "fire"):
		m._audio_ref().sfx("combat_fizzle", 0.9, -8.0)
		m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.65, 0.85, 0.55))
		return
	# damaging hits chain; the hit after chain 3 is a SUPER for double damage
	var super_bonus: bool = he.consume_super()
	boss["hp"] = int(boss["hp"]) - (2 if super_bonus else 1)
	he.note_hit(boss["pos"] as Vector3)
	if pa != null:
		pa.note_child_pop()
	if super_bonus:
		m._sparkle_burst((boss["pos"] as Vector3) + Vector3(0, 4.5, 0), Color(1.0, 0.95, 0.6))
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
	# hitstop: the engine stamps a beat of stillness on impact (40-90 ms) —
	# read here so the boss visibly "takes" the hit before phase logic moves
	boss["hitstop"] = maxf(0.0, float(boss.get("hitstop", 0.0)) - delta)
	if float(boss["hitstop"]) > 0.0:
		return
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
	var orb: Node3D
	if art_theme == "ember":
		orb = DungeonArt.spawn("pepper_projectile", self, from, art_theme)
		orb.scale = Vector3.ONE * 0.5
	else:
		orb = _sphere(self, from, 0.58, col, 1.4)
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
	# A listening microphone is shown, never assumed: the glyph is the only
	# promise the child gets that shouting will do anything.
	var ear: String = "🎤  " if mic_live else ""
	if kind == "ice":
		var left := 0
		for enemy in enemies:
			if String(enemy["state"]) != "popped": left += 1
		objective.text = (room_tag + "  •  " if room_tag != "" else "") + ear + "🫐  ICE BERRY: tap ICE • follow the golden arrow  ❄"
		counter.text = "❄  %d" % left
	elif kind == "dust":
		var left := 0
		for enemy in enemies:
			if String(enemy["state"]) != "popped":
				left += 1
		objective.text = (room_tag + " - " if room_tag != "" else "") \
			+ "CLEAN: tap CLEAN - follow the golden arrow"
		counter.text = "CLEAN  %d" % left
	else:
		var shell: bool = not boss.is_empty() and String(boss["phase"]) == "shell"
		var action_text := "❄  FREEZE THE SPINNING SHELL!" if kind == "dual" and shell else ("🔥  PEEKING — USE FIRE!" if kind == "dual" else ("🌶  SHELL UP — dodge!" if shell else "🌶  PEEKING — tap FIRE!"))
		objective.text = (room_tag + "  •  " if room_tag != "" else "") + ear + action_text
		counter.text = "🔥  %d" % maxi(0, int(boss.get("hp", 0)))

func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = float(encounter.get("win_time", 3.5))
	# standalone arena battles rank on time-to-victory; dungeon rooms
	# (room_tag set) roll into the single "dungeon" medal instead
	if room_tag == "" and kind in ["ice", "fire"]:
		m._medal_ref().award_stats("combat_ice" if kind == "ice" else "combat_fire", {"time": elapsed})
	pointer.visible = false
	if kind == "ice":
		objective.text = "✨  POPCORN PARTY!  ✨"
	elif kind == "dust":
		objective.text = "✨  ALL CLEAN!  ✨"
	else:
		objective.text = "✨  DRAGON-TURTLE TAMED!  ✨"
	counter.text = "★"
	if kind == "ice":
		m.show_msg("Roshan", "Pop pop pop! The frozen imps melted into popcorn!", "win")
	elif kind == "dust":
		m.show_msg("Roshan", "Poof! Every dust bunny is sparkling clean!", "win")
	else:
		m.show_msg("Roshan", "The spicy peppers did it! The turtle-lizard wants to be friends!", "win")

func _finish() -> void:
	state = "done"
	_disarm_mic()
	m.hit_engines.erase(he)
	he.teardown()
	if pa != null:
		pa.detach()
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
	_disarm_mic()
	m.hit_engines.erase(he)
	he.teardown()
	if pa != null:
		pa.detach()
	if prev_env != null:
		m.we_node.environment = prev_env
	if notify_finish and finish_cb.is_valid():
		finish_cb.call("")
	queue_free()

# Closing the arena closes the capture device: the audio HAL is only awake
# while a battle is running, never for the rest of the session.
func _disarm_mic() -> void:
	mic_live = false
	if m != null and m.mic_sys != null:
		m.mic_sys.disarm()

func action_label() -> String:
	if kind == "ice":
		return "ICE"
	if kind == "dust":
		return "CLEAN"
	if kind == "dual" and not boss.is_empty() and String(boss.get("phase", "shell")) == "shell":
		return "ICE"
	return "FIRE"
