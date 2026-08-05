class_name CombatTutorial
extends Node3D
# THE INTRODUCTION TO COMBAT (owner 2026-08-01). When Crown and companion
# welcomes are complete, walking through the event-ready Royal Hall gate
# teleports Roshan to a little sparring arena where one
# friendly imp walks her through every attack, one lesson at a time:
#   TAP → the 1-2-3 COMBO → the three-stage CHARGE → (partner bubble if a
#   stuffie follows) → a small graduation wave.
# Each lesson "pauses" the fight — the imp just waits and bobs, it NEVER
# attacks here — while a golden pointer and a looping ghost-finger
# demonstration act out the gesture on screen. The child then performs it
# for real: nothing advances without her own input (Phase-6, probe-gated),
# nothing punishes a wrong move. An unfinished class stays eligible at the
# Royal Hall until graduation. Runs on the shared HitEngine default pipeline, so
# the damage grammar, harm animation, chain pips, SUPER and charge ring
# behave exactly as everywhere else — that is the point of the lesson.

const CENTER := Vector3(0.0, -2600.0, 0.0)
const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")
const TRAINING_BACKDROP_PATH := "res://assets/castle/training/training_grotto_backdrop.png"
const GHOST_HAND_PATH := "res://assets/castle/training/ghost_hand.png"
const IDLE_REDEMO := 9.0            # the opera ghost-finger revival beat
const LESSONS := ["tap", "combo", "charge", "partner", "wave"]
const LESSON_MSG := {
	"tap": "Tap the imp — right on its nose!",
	"combo": "Tap tap tap! Three stars pops it!",
	"charge": "Press and HOLD — let the ring grow, then let go!",
	"partner": "Your partner is ready! Tap the bubble!",
	"wave": "Imps everywhere! Show them ALL your moves!",
}
const LESSON_DEMO := {
	"tap": "press", "combo": "drum", "charge": "hold", "partner": "press",
	"wave": "",
}

var m: ReefMain
var finish_cb: Callable
var prev_env: Environment = null
var cam: Camera3D = null
var avatar: Sprite3D = null
var pointer: Label3D = null
var demo_layer: CanvasLayer = null
var demo: DemoFinger = null
var he: HitEngine = null
var pa: PartnerAssist = null
var enemies: Array[Dictionary] = []
var lesson := ""
var lesson_t := 0.0
var idle_t := 0.0
var charge_seen := 0
var state := "play"
var win_t := 0.0
var elapsed := 0.0

# The looping ghost-finger demonstration (opera_gesture_surface's beat:
# 2.4 s cycle, halo 30/20 px, 13 px core dot), drawn at the live screen
# position of the lesson's target. Modes: press · drum (three quick
# presses) · hold (sustained press with the growing stage-colored arc).
class DemoFinger:
	extends Control
	var mode := "press"
	var t := 0.0
	var anchor := Vector2.ZERO
	var hand_texture: Texture2D = null
	func _process(delta: float) -> void:
		t += delta
		queue_redraw()
	func _pressing() -> bool:
		var cycle: float = fmod(t, 2.4)
		match mode:
			"drum":
				return (cycle > 0.9 and cycle < 1.1) \
					or (cycle > 1.3 and cycle < 1.5) \
					or (cycle > 1.7 and cycle < 1.9)
			"hold":
				return cycle > 0.7 and cycle < 2.2
		return cycle > 1.1
	func _draw() -> void:
		if anchor == Vector2.ZERO:
			return
		var pressing: bool = _pressing()
		var halo: float = 30.0 if pressing else 20.0
		draw_circle(anchor, halo, Color(1.0, 0.95, 0.7, 0.28))
		if hand_texture != null:
			var hand_size := Vector2(82.0, 82.0)
			draw_texture_rect(hand_texture,
				Rect2(anchor - hand_size * 0.5, hand_size), false)
		else:
			draw_circle(anchor, 13.0, Color(1.0, 0.98, 0.88, 0.95))
		if pressing:
			var ring: float = 18.0 + fmod(t * 46.0, 26.0)
			draw_arc(anchor, ring, 0.0, TAU, 32, Color(1.0, 0.95, 0.6, 0.7), 3.0, true)
		if mode == "hold" and pressing:
			# the charge preview: an arc that grows and walks the stage colors
			var cycle: float = fmod(t, 2.4)
			var grow: float = clampf((cycle - 0.7) / 1.45, 0.0, 1.0)
			var stage_col: Color = HitEngine.CHARGE_COLORS[clampi(int(grow * 3.0), 0, 2)]
			draw_arc(anchor, 34.0 + grow * 26.0, -PI * 0.5,
				-PI * 0.5 + TAU * maxf(grow, 0.06), 40,
				Color(stage_col.r, stage_col.g, stage_col.b, 0.85), 5.0, true)

func start(main: ReefMain, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	_build_environment()
	_build_stage()
	he = HitEngine.new(m)
	he.fx_root = self
	he.camera = cam
	he.targets = enemies
	m.hit_engines.append(he)
	_spawn_imp(Vector3(0, 1.0, -6.0))
	if m.companion_id != "":
		pa = PartnerAssist.new(m)
	_begin_lesson("tap")

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.13, 0.10, 0.22)   # the lavender dojo
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.82, 0.78, 1.0)
	env.ambient_light_energy = 0.9
	env.glow_enabled = true
	env.glow_intensity = 0.65
	env.glow_bloom = 0.12
	m._speedy_glow_clamp(env)
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(0.86, 0.80, 1.0)
	sun.light_energy = 1.1
	sun.shadow_enabled = m.quality != "speedy"
	sun.rotation_degrees = Vector3(-48, -28, 0)
	add_child(sun)

func _build_stage() -> void:
	var arena := DungeonArt.spawn("arena", self, CENTER, "")
	DungeonArt.tint(arena, _soft(Color(0.52, 0.46, 0.75)), _soft(Color(0.82, 0.70, 1.0), 0.18))
	avatar = Sprite3D.new()
	avatar.pixel_size = 6.2 / 256.0
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = CENTER + Vector3(0, 1.1, 8.0)
	add_child(avatar)
	var animator := ROSHAN_SPRITE_LOOP.new()
	avatar.add_child(animator)
	animator.setup_sprite_3d(avatar, false, avatar)
	cam = Camera3D.new()
	cam.fov = 58.0
	cam.position = CENTER + Vector3(0, 26.0, 27.0)
	add_child(cam)
	cam.look_at(CENTER + Vector3(0, 1.5, 0), Vector3.UP)
	cam.make_current()
	_add_training_backdrop()
	pointer = Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 150
	pointer.pixel_size = 0.022
	pointer.outline_size = 24
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(pointer)
	demo_layer = CanvasLayer.new()
	demo_layer.layer = 15
	m.add_child(demo_layer)
	demo = DemoFinger.new()
	if ResourceLoader.exists(GHOST_HAND_PATH):
		demo.hand_texture = load(GHOST_HAND_PATH) as Texture2D
	demo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	demo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	demo_layer.add_child(demo)

func _add_training_backdrop() -> void:
	if cam == null or not ResourceLoader.exists(TRAINING_BACKDROP_PATH):
		return
	var texture: Texture2D = load(TRAINING_BACKDROP_PATH) as Texture2D
	if texture == null:
		return
	# Camera-local placement keeps the 2:1 painting perpendicular to the
	# steep arena camera while its center still lands at world z ~= -30.
	var distance := 77.0
	var height := 2.0 * distance * tan(deg_to_rad(cam.fov * 0.5))
	var aspect: float = float(texture.get_width()) / float(texture.get_height())
	var quad := QuadMesh.new()
	quad.size = Vector2(height * aspect, height)
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.albedo_texture = texture
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	var backdrop := MeshInstance3D.new()
	backdrop.name = "TrainingGrottoBackdrop"
	backdrop.mesh = quad
	backdrop.material_override = material
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	backdrop.position = Vector3(0.0, 0.0, -distance)
	cam.add_child(backdrop)

func _soft(col: Color, emission: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.62
	if emission > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = emission
	return mat

func _spawn_imp(offset: Vector3) -> Dictionary:
	var root := Node3D.new()
	root.position = CENTER + offset
	add_child(root)
	DungeonArt.spawn("imp", root, Vector3.ZERO, "")
	# a friendly sparring imp: 3 hp per the damage grammar, "pop" finale,
	# and NO attack timer of any kind — it only ever bobs and waits
	var enemy: Dictionary = {"node": root, "pos": root.position,
		"state": "active", "hp": 3, "death": "pop", "phase": randf() * TAU}
	enemies.append(enemy)
	m._sparkle_burst(root.position + Vector3(0, 2.0, 0), Color(0.82, 0.70, 1.0))
	return enemy

func _begin_lesson(next: String) -> void:
	lesson = next
	lesson_t = 0.0
	idle_t = 0.0
	charge_seen = 0
	var msg: String = String(LESSON_MSG.get(next, ""))
	if msg != "":
		m.show_msg("Roshan", msg, "talk")
	demo.mode = String(LESSON_DEMO.get(next, ""))
	demo.visible = demo.mode != ""
	demo.t = 0.0
	if next == "partner" and pa != null and pa.bubble == null:
		pa.attach("stuffie", Callable(self, "_partner_super"))

func _lesson_target() -> Dictionary:
	for enemy in enemies:
		if String(enemy["state"]) == "active":
			return enemy
	return {}

func _process(delta: float) -> void:
	if m == null or state == "done":
		return
	elapsed += delta
	he.tick(delta)
	if pa != null:
		pa.tick(delta)
	# the sparring imps only bob — the "pause" is that nothing ever rushes her
	for enemy in enemies:
		var node_value: Variant = enemy.get("node")
		if node_value != null and is_instance_valid(node_value) and String(enemy["state"]) == "active":
			var node: Node3D = node_value
			node.position = (enemy["pos"] as Vector3) + Vector3(0, sin(elapsed * 3.0 + float(enemy["phase"])) * 0.25, 0)
	if state == "won":
		win_t -= delta
		if fmod(win_t, 0.32) < delta:
			m._sparkle_burst(CENTER + Vector3(randf_range(-9.0, 9.0), randf_range(1.0, 6.0), randf_range(-7.0, 7.0)), Color.from_hsv(randf(), 0.55, 1.0))
		if win_t <= 0.0:
			_finish()
		return
	charge_seen = maxi(charge_seen, he.charge_stage)
	_tick_pointer_and_demo()
	_tick_lesson(delta)

func _tick_pointer_and_demo() -> void:
	var target: Dictionary = _lesson_target()
	if lesson == "partner" and pa != null and pa.bubble != null:
		pointer.visible = false
		demo.anchor = pa.bubble.position + pa.bubble.size * 0.5
		return
	pointer.visible = not target.is_empty() and state == "play"
	if target.is_empty():
		demo.anchor = Vector2.ZERO
		return
	var node: Node3D = target["node"]
	pointer.position = node.position + Vector3(0, 5.6 + sin(elapsed * 4.0) * 0.4, 0)
	if demo.visible and cam != null:
		demo.anchor = cam.unproject_position(node.global_position + Vector3(0, 1.8, 0))

func _tick_lesson(delta: float) -> void:
	lesson_t += delta
	# the ghost finger hides once she acts, and returns after a quiet spell
	if he.chain > 0 or not he.charge_enemy.is_empty():
		demo.visible = false
		idle_t = 0.0
	elif String(LESSON_DEMO.get(lesson, "")) != "":
		idle_t += delta
		if idle_t >= IDLE_REDEMO and not demo.visible:
			demo.visible = true
			demo.t = 0.0
			var msg: String = String(LESSON_MSG.get(lesson, ""))
			if msg != "":
				m.show_msg("Roshan", msg, "talk")
			idle_t = 0.0
	match lesson:
		"tap":
			var target: Dictionary = _lesson_target()
			if not target.is_empty() and int(target.get("hp", 3)) < 3:
				m.show_msg("Roshan", "Bop! Right on the nose!", "win")
				_begin_lesson("combo")
		"combo":
			if _lesson_target().is_empty():
				m.show_msg("Roshan", "One, two, THREE! Popcorn!", "win")
				_spawn_imp(Vector3(2.5, 1.0, -5.0))
				_begin_lesson("charge")
		"charge":
			if _lesson_target().is_empty():
				if charge_seen > 0:
					m.show_msg("Roshan", "A full-power bubble POP!", "win")
				else:
					m.show_msg("Roshan", "Popped! Next time, try HOLDING too!", "win")
				if pa != null:
					_begin_lesson("partner")
				else:
					_spawn_wave()
					_begin_lesson("wave")
		"partner":
			if pa != null and pa.bubble != null and pa.cool > 0.0:
				m.show_msg("Roshan", "Partner power! Now finish them!", "win")
				_begin_lesson("wave")
			elif _lesson_target().is_empty() and enemies.size() < 6:
				_spawn_wave()
		"wave":
			if _lesson_target().is_empty() and enemies.size() >= 4:
				_win()

func _spawn_wave() -> void:
	for offset in [Vector3(-4.0, 1.0, -5.0), Vector3(0.0, 1.0, -8.0), Vector3(4.0, 1.0, -5.0)]:
		_spawn_imp(offset as Vector3)

# The stuffie's classroom stampede: identical rules to the arena — pops
# nearest fodder by hp, dizzies nothing here (they are already waiting),
# grants the Big Taps so her graduation swings feel enormous.
func _partner_super(_partner_kind: String) -> void:
	if enemies.is_empty() or state != "play":
		return
	var felled := 0
	for enemy in enemies:
		if String(enemy["state"]) != "active" or felled >= PartnerAssist.STAMPEDE_POPS:
			continue
		enemy["hp"] = 0
		he.play_death(enemy)
		felled += 1
	he.big_taps = PartnerAssist.BIG_TAPS
	m._sparkle_burst(CENTER + Vector3(0, 3.0, -5.0), Color(0.95, 0.75, 1.0))

func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = 2.8
	pointer.visible = false
	demo.visible = false
	m.pearl_count += 5
	if not m.combat_tutorial_done:
		m.combat_tutorial_done = true
		m._write_save()
	m._audio_ref()._fanfare()
	m.show_msg("Roshan", "You know ALL the moves! Sparring class complete!", "win")

func _finish() -> void:
	if state == "done":
		return
	state = "done"
	m.hit_engines.erase(he)
	he.teardown()
	if pa != null:
		pa.detach()
	if demo_layer != null and is_instance_valid(demo_layer):
		demo_layer.queue_free()
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()

func cancel() -> void:
	if state == "done":
		return
	if state == "won":
		_finish()
		return
	state = "done"
	m.hit_engines.erase(he)
	he.teardown()
	if pa != null:
		pa.detach()
	if demo_layer != null and is_instance_valid(demo_layer):
		demo_layer.queue_free()
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()
