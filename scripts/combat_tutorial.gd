class_name CombatTutorial
extends Node3D
# THE INTRODUCTION TO COMBAT (owner 2026-08-01). When Crown and companion
# welcomes are complete, walking through the event-ready Royal Hall gate
# teleports Roshan to a little sparring arena where one
# friendly imp walks her through every direct interaction, one lesson at a
# time: TAP → the 1-2-3 COMBO → the three-stage CHARGE → a small graduation
# wave. The retired partner bubble is not part of the lesson path.
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
const IDLE_REDEMO := 9.0            # the opera ghost-finger revival beat
const LESSONS := ["tap", "combo", "charge", "wave"]
const LESSON_MSG := {
	"tap": "Tap the imp — right on its nose!",
	"combo": "Tap tap tap! Three stars pops it!",
	"charge": "Press and HOLD — let the ring grow, then let go!",
	"wave": "Imps everywhere! Show them ALL your moves!",
}
const LESSON_DEMO := {
	"tap": "press", "combo": "drum", "charge": "hold",
	"wave": "",
}

var m: ReefMain
var finish_cb: Callable
var prev_env: Environment = null
var cam: Camera3D = null
var avatar: Sprite3D = null
var backdrop_layer: CanvasLayer = null
var demo_layer: CanvasLayer = null
var demo: EncounterGestureGuide2D = null
var he: HitEngine = null
var enemies: Array[Dictionary] = []
var lesson := ""
var lesson_t := 0.0
var lesson_initial_hp := 3
var idle_t := 0.0
var charge_seen := 0
var state := "play"
var win_t := 0.0
var elapsed := 0.0
var prior_music := ""
var owns_music := false
var caption_position := Vector2.ZERO
var caption_size := Vector2.ZERO
var caption_font_size := 0
var caption_style: StyleBox = null

func start(main: ReefMain, done_cb: Callable) -> void:
	m = main
	m._navigation_push("combat_tutorial", self, Callable(self, "cancel"))
	finish_cb = done_cb
	prior_music = m.cur_track
	m._play_music("combat_tutorial")
	owns_music = m.cur_track == "combat_tutorial"
	_build_environment()
	_build_stage()
	_compact_caption()
	he = HitEngine.new(m)
	he.fx_root = self
	he.camera = cam
	he.targets = enemies
	m.hit_engines.append(he)
	_spawn_imp(Vector3(0, 1.0, -6.0))
	_begin_lesson("tap")

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	# Layer -10 becomes the spatial viewport's background, so the Canvas grotto
	# sits behind the retained actors instead of painting over them.
	env.background_mode = Environment.BG_CANVAS
	env.background_canvas_max_layer = -10
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.82, 0.78, 1.0)
	env.ambient_light_energy = 0.9
	env.glow_enabled = true
	env.glow_intensity = 0.65
	env.glow_bloom = 0.12
	m._speedy_glow_clamp(env)
	m.we_node.environment = env

func _compact_caption() -> void:
	if m.hud_msg == null:
		return
	caption_position = m.hud_msg.position
	caption_size = m.hud_msg.size
	caption_font_size = m.hud_msg.get_theme_font_size("font_size")
	caption_style = m.hud_msg.get_theme_stylebox("normal")
	m.hud_msg.text = ""
	m.hud_msg.add_theme_font_size_override("font_size", 20)
	m.hud_msg.add_theme_stylebox_override("normal", StorybookUI.panel_style(
		StorybookUI.LAVENDER, Color(0.94, 0.96, 1.0, 0.88), 18, 2))
	m.hud_msg.position = Vector2(320.0, 626.0)
	m.hud_msg.size = Vector2(640.0, 82.0)

func _restore_caption() -> void:
	if m == null or m.hud_msg == null:
		return
	m.hud_msg.text = ""
	if caption_style != null:
		m.hud_msg.add_theme_stylebox_override("normal", caption_style)
	m.hud_msg.position = caption_position
	m.hud_msg.size = caption_size
	if caption_font_size > 0:
		m.hud_msg.add_theme_font_size_override("font_size", caption_font_size)
	else:
		m.hud_msg.remove_theme_font_size_override("font_size")

func _build_stage() -> void:
	_add_training_backdrop()
	avatar = Sprite3D.new()
	avatar.pixel_size = 6.2 / 256.0
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = CENTER + Vector3(7.0, 1.1, 10.0)
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
	demo_layer = CanvasLayer.new()
	# Partner portraits use layer 15; the fingertip must remain above its target.
	# The opened pause sheet retains its existing layer-29 ownership.
	demo_layer.layer = 16
	m.add_child(demo_layer)
	demo = EncounterGestureGuide2D.new()
	demo_layer.add_child(demo)

func _add_training_backdrop() -> void:
	if not ResourceLoader.exists(TRAINING_BACKDROP_PATH):
		return
	var texture: Texture2D = load(TRAINING_BACKDROP_PATH) as Texture2D
	if texture == null:
		return
	backdrop_layer = CanvasLayer.new()
	backdrop_layer.layer = -10
	m.add_child(backdrop_layer)
	var backdrop := TextureRect.new()
	backdrop.name = "TrainingGrottoBackdrop"
	backdrop.texture = texture
	backdrop.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	backdrop.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	backdrop_layer.add_child(backdrop)

func _spawn_imp(offset: Vector3) -> Dictionary:
	var root := Node3D.new()
	root.position = CENTER + offset
	# Match the painted grotto's floor band instead of placing the target
	# against the upper water wall. Existing actor/camera staging is retained.
	root.position.z += 15.0
	root.position.x = root.position.x * 1.7 - 6.0
	add_child(root)
	var art := DustBunnySprite.new()
	art.scale = Vector3.ONE * 2.2
	root.add_child(art)
	var shadow := Sprite2D.new()
	shadow.texture = preload("res://assets/flats/castle/rooms/room_actor_shadow.png")
	shadow.position = cam.unproject_position(root.position)
	shadow.scale = Vector2(0.55, 0.16)
	backdrop_layer.add_child(shadow)
	# a friendly sparring imp: 3 hp per the damage grammar, "pop" finale,
	# and NO attack timer of any kind — it only ever bobs and waits
	var enemy: Dictionary = {"node": root, "pos": root.position,
		"state": "active", "hp": 3, "death": "pop", "phase": randf() * TAU,
		"shadow": shadow, "aim_h": 4.0, "screen_radius": 80.0}
	enemies.append(enemy)
	m._sparkle_burst(root.position + Vector3(0, 2.0, 0), Color(0.82, 0.70, 1.0))
	return enemy

func _begin_lesson(next: String) -> void:
	lesson = next
	lesson_t = 0.0
	idle_t = 0.0
	charge_seen = 0
	lesson_initial_hp = int(_lesson_target().get("hp", 3))
	var msg: String = String(LESSON_MSG.get(next, ""))
	if msg != "":
		m.show_msg("Roshan", msg, "talk")
	demo.mode = String(LESSON_DEMO.get(next, ""))
	demo.visible = demo.mode != ""
	demo.t = 0.0

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
	# the sparring imps only bob — the "pause" is that nothing ever rushes her
	for enemy in enemies:
		var shadow: Sprite2D = enemy.get("shadow") as Sprite2D
		if shadow != null:
			shadow.visible = String(enemy["state"]) == "active"
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
	if target.is_empty():
		demo.anchor = Vector2.ZERO
		return
	if demo.visible and cam != null:
		demo.anchor = cam.unproject_position(he.aim_point(target))

func _tick_lesson(delta: float) -> void:
	lesson_t += delta
	# the ghost finger hides once she acts, and returns after a quiet spell
	var target: Dictionary = _lesson_target()
	var acted: bool = not target.is_empty() and int(target.get("hp", 3)) < lesson_initial_hp
	if acted or not he.charge_enemy.is_empty():
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
			if not target.is_empty() and int(target.get("hp", 3)) < 3:
				m.show_msg("Roshan", "Bop! Right on the nose!",
					"tutorial_first_bop")
				_begin_lesson("combo")
		"combo":
			if _lesson_target().is_empty():
				m.show_msg("Roshan", "One, two, THREE! Popcorn!",
					"tutorial_combo")
				_spawn_imp(Vector3(2.5, 1.0, -5.0))
				_begin_lesson("charge")
		"charge":
			if _lesson_target().is_empty():
				if charge_seen > 0:
					m.show_msg("Roshan", "A full-power bubble POP!",
						"tutorial_power_pop")
				else:
					m.show_msg("Roshan", "Popped! Next time, try HOLDING too!",
						"tutorial_power_pop")
				_spawn_wave()
				_begin_lesson("wave")
		"wave":
			if _lesson_target().is_empty() and enemies.size() >= 4:
				_win()

func _spawn_wave() -> void:
	for offset in [Vector3(-4.0, 1.0, -5.0), Vector3(0.0, 1.0, -8.0), Vector3(4.0, 1.0, -5.0)]:
		_spawn_imp(offset as Vector3)

func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = 2.8
	demo.visible = false
	m.pearl_count += 5
	if not m.combat_tutorial_done:
		m.combat_tutorial_done = true
		m._write_save()
	m._audio_ref()._fanfare()
	m.show_msg("Roshan", "You know ALL the moves! Sparring class complete!",
		"tutorial_done")

func _finish() -> void:
	if state == "done":
		return
	m._navigation_remove("combat_tutorial")
	state = "done"
	m.hit_engines.erase(he)
	he.teardown()
	if demo_layer != null and is_instance_valid(demo_layer):
		demo_layer.queue_free()
	if backdrop_layer != null and is_instance_valid(backdrop_layer):
		backdrop_layer.queue_free()
	if prev_env != null:
		m.we_node.environment = prev_env
	_restore_caption()
	_restore_music()
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()

func cancel() -> void:
	if state == "done":
		return
	m._navigation_remove("combat_tutorial")
	if state == "won":
		_finish()
		return
	state = "done"
	m.hit_engines.erase(he)
	he.teardown()
	if demo_layer != null and is_instance_valid(demo_layer):
		demo_layer.queue_free()
	if backdrop_layer != null and is_instance_valid(backdrop_layer):
		backdrop_layer.queue_free()
	if prev_env != null:
		m.we_node.environment = prev_env
	_restore_caption()
	_restore_music()
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()


func _restore_music() -> void:
	if not owns_music:
		return
	owns_music = false
	var restore_track: String = prior_music
	prior_music = ""
	if restore_track != "":
		m._play_music(restore_track)
