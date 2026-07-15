class_name DollsGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# dolls minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["spawned"] = 0
	m.g["caught"] = 0
	m.g["resolved"] = 0
	m.g["missed"] = 0
	m.g["next"] = 0.6
	m.g["dolls"] = []
	m.g["timer"] = -1.0
	_dolls2d_open(fr)
	m.show_msg(fr["fname"], "Catch 3 sleepy dolls in your arms!")

func _tick_dolls(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	if m.dolls_root == null:
		return
	# move the 2D catcher: stick / arrows / mouse-touch x
	var mx := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		mx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		mx += 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		mx += jx
	if m.touch_ui != null and absf((m.touch_ui.stick_vec as Vector2).x) > 0.15:
		mx += (m.touch_ui.stick_vec as Vector2).x
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		var target_x: float = m.dolls_root.get_global_mouse_position().x - 60.0
		m.dolls_catcher.position.x = lerpf(m.dolls_catcher.position.x, target_x, 0.2)
	m.dolls_catcher.position.x = clampf(m.dolls_catcher.position.x + mx * 620.0 * delta, 0.0, 1160.0)
	# Phase 6: catching needs a live hand on the controls — any stick / key /
	# mouse / touch inside the last 2s counts. Lucky drops onto an abandoned
	# catcher no longer score (a passive run could fluke 3 catches before).
	if absf(mx) > 0.05 or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		m.g["verb_t"] = 2.0
	else:
		m.g["verb_t"] = maxf(0.0, float(m.g.get("verb_t", 0.0)) - delta)
	var hands_on: bool = float(m.g.get("verb_t", 0.0)) > 0.0
	m.g["next"] = float(m.g["next"]) - delta
	if float(m.g["next"]) <= 0.0 and int(m.g["caught"]) < 3:
		m.g["spawned"] = int(m.g["spawned"]) + 1
		m.g["next"] = 1.2
		var doll := ColorRect.new()
		doll.color = Color(0, 0, 0, 0)
		doll.size = Vector2(96, 86)
		var missed: int = int(m.g["missed"])
		var drop_x: float = 80.0 + randf() * 1100.0
		if missed >= 2:
			# Bring later dolls toward Roshan and slow them down. A live touch or
			# stick movement is still required, so an unattended game cannot win.
			var spread: float = maxf(35.0, 220.0 - float(missed - 2) * 35.0)
			drop_x = clampf(m.dolls_catcher.position.x + 17.0 + randf_range(-spread, spread), 0.0, 1160.0)
		doll.position = Vector2(drop_x, -100.0)
		doll.set_meta("fall_speed", maxf(105.0, 190.0 - float(missed) * 15.0))
		var dtex := TextureRect.new()
		dtex.texture = load(["res://assets/book/baby_doll.png", "res://assets/book/baby_doll2.png", "res://assets/book/baby_doll3.png"][int(m.g["spawned"]) % 3])
		dtex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		dtex.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		dtex.set_anchors_preset(Control.PRESET_FULL_RECT)
		doll.add_child(dtex)
		m.dolls_root.add_child(doll)
		(m.g["dolls"] as Array).append(doll)
	var dolls: Array = m.g["dolls"]
	for i in range(dolls.size() - 1, -1, -1):
		var doll: ColorRect = dolls[i]
		doll.position.y += float(doll.get_meta("fall_speed", 190.0)) * delta
		doll.position.x += sin(float(m.g["t"]) * 1.6 + float(i) * 2.0) * 60.0 * delta
		doll.rotation = sin(float(m.g["t"]) * 2.0 + float(i)) * 0.25
		var caught: bool = hands_on and doll.position.y > 490.0 and absf(doll.position.x + 48.0 - (m.dolls_catcher.position.x + 65.0)) < 115.0
		if caught:
			m.g["caught"] = int(m.g["caught"]) + 1
			m.g["resolved"] = int(m.g["resolved"]) + 1
			doll.queue_free()
			dolls.remove_at(i)
			if m.voice != null:
				m.voice.pitch_scale = 1.0 + randf() * 0.25
				m.voice.play()
		elif doll.position.y > 700.0:
			m.g["resolved"] = int(m.g["resolved"]) + 1
			m.g["missed"] = int(m.g["missed"]) + 1
			# a baby got away! Faron gasps (min-gap so two misses don't overlap)
			m._say("faron", "miss", 3.0)
			doll.queue_free()
			dolls.remove_at(i)
	# audit: hud_game sits BEHIND the opaque nursery overlay — write the score
	# onto the dolls layer itself so it is actually visible
	if m.dolls_score_lbl != null:
		m.dolls_score_lbl.text = "Sleepy dolls caught: %d  (catch 3 to win!)" % int(m.g["caught"])
	if int(m.g["caught"]) >= 3:
		_dolls2d_close()
		m._end_game(true, fr, "You tucked in %d dolls! All cozy now." % int(m.g["caught"]))

func _dolls2d_open(fr: Dictionary) -> void:
	if m.dolls_layer == null:
		m.dolls_layer = CanvasLayer.new()
		m.dolls_layer.layer = 6
		m.add_child(m.dolls_layer)
	m.dolls_root = Control.new()
	m.dolls_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.dolls_layer.add_child(m.dolls_root)
	var bg := TextureRect.new()
	bg.texture = load("res://assets/book/nursery_bg.jpg")
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.dolls_root.add_child(bg)
	var tint := ColorRect.new()
	tint.color = Color(0.08, 0.05, 0.2, 0.25)
	tint.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.dolls_root.add_child(tint)
	var faron := TextureRect.new()
	faron.texture = (fr["node"] as Sprite3D).texture
	faron.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	faron.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	faron.custom_minimum_size = Vector2(170, 200)
	faron.size = Vector2(170, 200)
	faron.position = Vector2(40, 60)
	m.dolls_root.add_child(faron)
	m.dolls_score_lbl = Label.new()
	m.dolls_score_lbl.add_theme_font_size_override("font_size", 34)
	m.dolls_score_lbl.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15))
	m.dolls_score_lbl.add_theme_constant_override("outline_size", 10)
	m.dolls_score_lbl.position = Vector2(230, 24)
	m.dolls_root.add_child(m.dolls_score_lbl)
	m.dolls_catcher = TextureRect.new()
	m.dolls_catcher.texture = load(m.skin_sprite_path())
	m.dolls_catcher.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	m.dolls_catcher.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	m.dolls_catcher.custom_minimum_size = Vector2(130, 165)
	m.dolls_catcher.size = Vector2(130, 165)
	m.dolls_catcher.position = Vector2(580, 530)
	m.dolls_root.add_child(m.dolls_catcher)

func _dolls2d_close() -> void:
	if m.dolls_root != null and is_instance_valid(m.dolls_root):
		m.dolls_root.queue_free()
	m.dolls_root = null
	m.dolls_catcher = null
	m.dolls_score_lbl = null
