class_name PictureGames
extends RefCounted
# Phase 7.4b: mechanical extraction of the 2D picture-game suite from
# main.gd (snowman build/face/chase, garden, trampoline, slide GO screen,
# xmas, plus the shared mg2d canvas helpers and win/close flow). All
# state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _mg2d_open(kind: String) -> void:
	if kind == "slide":
		m._l2_start_slide()   # the rainbow slide is always the 3D play-place, never the old 2D screen
		return
	m.mg_kind = kind
	m.mg = {"t": 0.0, "btns": []}
	if m.mg2d_layer == null:
		m.mg2d_layer = CanvasLayer.new()
		m.mg2d_layer.layer = 7
		m.add_child(m.mg2d_layer)
	m.mg2d_root = Control.new()
	m.mg2d_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.mg2d_layer.add_child(m.mg2d_root)
	m.mg2d_layer.visible = true
	# clean themed gradient background (no busy book page behind the toys)
	var themes := {
		"snowman": [Color(0.50, 0.66, 0.86), Color(0.88, 0.94, 1.0)],
		"garden": [Color(0.45, 0.78, 0.95), Color(0.7, 0.92, 0.6)],
		"trampoline": [Color(0.45, 0.72, 1.0), Color(0.86, 0.95, 1.0)],
		"slide": [Color(0.55, 0.7, 1.0), Color(1.0, 0.85, 0.92)],
		"xmas": [Color(0.10, 0.18, 0.30), Color(0.25, 0.40, 0.48)]}
	var grad := Gradient.new()
	grad.set_color(0, themes[kind][0])
	grad.set_color(1, themes[kind][1])
	var gt := GradientTexture2D.new()
	gt.gradient = grad
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	gt.width = 64
	gt.height = 64
	var bg := TextureRect.new()
	bg.texture = gt
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.stretch_mode = TextureRect.STRETCH_SCALE
	m.mg2d_root.add_child(bg)
	# responsive 1280x720 stage, scaled + centred to any screen (fixes landscape)
	m.mg2d_stage = Control.new()
	m.mg2d_stage.size = Vector2(1280, 720)
	var vp: Vector2 = m.get_viewport().get_visible_rect().size
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	m.mg2d_stage.scale = Vector2(sc, sc)
	m.mg2d_stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	m.mg2d_root.add_child(m.mg2d_stage)
	m.mg["hud"] = _mg_label("", 40, Vector2(40, 26))
	# a friendly ✕ so ANY config can leave without finishing (controller: B)
	var xb := Button.new()
	xb.text = "✕"
	xb.add_theme_font_size_override("font_size", 42)
	xb.custom_minimum_size = Vector2(76, 76)
	xb.position = Vector2(1186, 14)
	var xsb := StyleBoxFlat.new()
	xsb.bg_color = Color(0.1, 0.12, 0.25, 0.55)
	xsb.set_corner_radius_all(38)
	xb.add_theme_stylebox_override("normal", xsb)
	xb.add_theme_stylebox_override("hover", xsb)
	xb.add_theme_stylebox_override("pressed", xsb)
	xb.pressed.connect(_mg2d_close)
	m.mg2d_stage.add_child(xb)
	m.mg["xbtn"] = xb
	if kind == "snowman": _mg_build_snowman()
	elif kind == "garden": _mg_build_garden()
	elif kind == "trampoline": _mg_build_trampoline()
	elif kind == "slide": _mg_build_slide()
	elif kind == "xmas": _mg_build_xmas()


func _mg_label(txt: String, size: int, pos: Vector2) -> Label:
	var l := Label.new()
	l.text = txt
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15, 0.95))
	l.add_theme_constant_override("outline_size", 12)
	l.position = pos
	m.mg2d_stage.add_child(l)
	return l


func _mg_circle(pos: Vector2, r: float, col: Color) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(r))
	sb.shadow_color = Color(0, 0, 0, 0.28)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 5)
	sb.border_color = col.darkened(0.22)              # soft rim for roundness
	sb.set_border_width_all(maxi(2, int(r * 0.05)))
	p.add_theme_stylebox_override("panel", sb)
	p.size = Vector2(r * 2.0, r * 2.0)
	p.position = pos - Vector2(r, r)
	m.mg2d_stage.add_child(p)
	# glossy highlight (upper-left) gives a 3D ball sheen
	var hl := Panel.new()
	var hsb := StyleBoxFlat.new()
	hsb.bg_color = Color(1, 1, 1, 0.38)
	hsb.set_corner_radius_all(int(r * 0.5))
	hl.add_theme_stylebox_override("panel", hsb)
	hl.size = Vector2(r * 0.85, r * 0.6)
	hl.position = Vector2(r * 0.32, r * 0.22)
	hl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	p.add_child(hl)
	return p


func _mg_sprite(path: String, pos: Vector2, sz: Vector2) -> TextureRect:
	var t := TextureRect.new()
	t.texture = load(path)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.size = sz
	t.position = pos - sz * 0.5
	m.mg2d_stage.add_child(t)
	return t


func _mg_artbtn(path: String, pos: Vector2, sz: Vector2) -> Button:
	var b := Button.new()
	b.position = pos - sz * 0.5
	b.custom_minimum_size = sz
	b.size = sz
	b.flat = true
	var t := TextureRect.new()
	t.texture = load(path)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.set_anchors_preset(Control.PRESET_FULL_RECT)
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(t)
	m.mg2d_stage.add_child(b)
	(m.mg["btns"] as Array).append(b)
	return b


func _mg_roundbtn(pos: Vector2, r: float, col: Color, txt: String = "") -> Button:
	var b := Button.new()
	b.position = pos - Vector2(r, r)
	b.custom_minimum_size = Vector2(r * 2.0, r * 2.0)
	b.size = Vector2(r * 2.0, r * 2.0)
	b.text = txt
	b.add_theme_font_size_override("font_size", 44)
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(r))
	b.add_theme_stylebox_override("normal", sb)
	var sb2: StyleBoxFlat = sb.duplicate()
	sb2.bg_color = col.lightened(0.3)
	b.add_theme_stylebox_override("pressed", sb2)
	b.add_theme_stylebox_override("hover", sb)
	m.mg2d_stage.add_child(b)
	(m.mg["btns"] as Array).append(b)
	return b


func _mg2d_win(msg: String) -> void:
	m._reward(false)   # RewardDirector: same chime run on every win
	if m.mg_kind == "snowman":
		m.award_sticker("snowman")
	if bool(m.mg.get("won", false)):
		return
	m.mg["won"] = true
	m.show_msg("Roshan", msg, "win")
	for i in range(8):
		m._sparkle_burst(m.player.position + Vector3(randf() * 8 - 4, randf() * 6, randf() * 8 - 4), Color.from_hsv(randf(), 0.6, 1.0))
	m.pearl_count += 2
	m._update_hud()
	m._write_save()
	# hide the buttons + show a celebratory banner over the FINISHED scene, hold ~1.6s, then close
	for b in (m.mg.get("btns", []) as Array):
		if is_instance_valid(b):
			b.disabled = true
			b.visible = false
	if m.mg.get("xbtn") != null and is_instance_valid(m.mg["xbtn"]):
		(m.mg["xbtn"] as Button).visible = false
	if m.mg2d_stage != null and is_instance_valid(m.mg2d_stage):
		var banner := _mg_label("\u2b50  Yay! You did it!  \u2b50", 76, Vector2(330, 26))
		banner.add_theme_color_override("font_color", Color(1.0, 0.95, 0.4))
		for ci in range(40):
			var conf := ColorRect.new()
			conf.color = Color.from_hsv(randf(), 0.7, 1.0)
			conf.size = Vector2(18, 18)
			conf.position = Vector2(randf() * 1280, -20.0 - randf() * 200.0)
			conf.rotation = randf() * TAU
			m.mg2d_stage.add_child(conf)
			var tw = m.create_tween()
			tw.tween_property(conf, "position:y", 760.0, 1.3 + randf() * 0.5).set_delay(randf() * 0.3)
	m.get_tree().create_timer(1.6).timeout.connect(_mg2d_close)


func _mg2d_close() -> void:
	if m.mg2d_root != null and is_instance_valid(m.mg2d_root):
		m.mg2d_root.queue_free()
	m.mg2d_root = null
	m.mg2d_stage = null
	if m.mg2d_layer != null:
		m.mg2d_layer.visible = false
	m.mg_kind = ""
	m.mg = {}
	m.mg_cool = 8.0

# ---- SNOWMAN: ROLL the snow into balls (stick circles / finger circles),
# ---- watch each ball grow, then stack it and place the face ----


func _mg_build_snowman() -> void:
	m.mg["phase"] = "roll"
	m.mg["balls"] = 0
	m.mg["face"] = 0
	m.mg["motor_assist"] = false
	(m.mg["hud"] as Label).text = "Spin the stick - or draw circles with your finger!"
	# ground
	_mg_circle(Vector2(640, 980), 700.0, Color(0.95, 0.97, 1.0, 0.5))
	m.mg["body"] = []   # stacked balls (centre-right)
	# the big flashing call-to-action
	var fl := _mg_label("ROLL UP THE SNOWBALLS!", 64, Vector2(255, 92))
	fl.add_theme_color_override("font_color", Color(1.0, 0.95, 0.4))
	fl.pivot_offset = Vector2(385, 40)
	m.mg["flash"] = fl
	# orbiting hint arrow showing the circular motion
	var ar := _mg_label("↻", 84, Vector2(0, 0))
	ar.add_theme_color_override("font_color", Color(0.5, 0.75, 1.0))
	m.mg["hint_arrow"] = ar
	_mg_snow_new_ball()


func _mg_snow_new_ball() -> void:
	var done: int = int(m.mg["balls"])                      # balls finished so far
	var ball = _mg_circle(m.SNOW_ROLL_C, 26.0, Color(0.97, 0.99, 1.0))
	m.mg["roll_ball"] = ball
	m.mg["final_r"] = 150.0 - float(done + 1) * 26.0        # 124, 98, 72
	m.mg["rot_need"] = (3.0 - float(done) * 0.5) * TAU      # 3 / 2.5 / 2 full circles
	m.mg["rot_acc"] = 0.0
	m.mg["rot_prev"] = 0.0
	m.mg["prev_ang"] = null
	m.mg["stall"] = 0.0
	m.mg["stall_acc"] = 0.0


func _mg_snow_ball_size(ball: Panel, r: float, center: Vector2) -> void:
	ball.size = Vector2(r * 2.0, r * 2.0)
	ball.position = center - Vector2(r, r)
	var sb = ball.get_theme_stylebox("panel") as StyleBoxFlat
	if sb != null:
		sb.set_corner_radius_all(int(r))
		sb.set_border_width_all(maxi(2, int(r * 0.05)))
	if ball.get_child_count() > 0:
		var hl = ball.get_child(0) as Panel
		if hl != null:
			hl.size = Vector2(r * 0.85, r * 0.6)
			hl.position = Vector2(r * 0.32, r * 0.22)
			var hsb = hl.get_theme_stylebox("panel") as StyleBoxFlat
			if hsb != null:
				hsb.set_corner_radius_all(int(r * 0.5))


func _mg_snow_ball_done() -> void:
	var b: int = int(m.mg["balls"]) + 1
	m.mg["balls"] = b
	var ball: Panel = m.mg["roll_ball"]
	m.mg.erase("roll_ball")
	var r: float = float(m.mg["final_r"])
	var bc := Vector2(980, 560.0 - float(b - 1) * 175.0)
	var tw = m.create_tween()
	tw.tween_property(ball, "position", bc - Vector2(r, r), 0.5).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	(m.mg["body"] as Array).append(ball)
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + float(b) * 0.15
		m.chime.play()
	m._sparkle_burst(m.player.position + Vector3(0, 1, 0), Color(0.8, 0.92, 1.0))
	if b >= 3:
		m.mg["head_pos"] = bc
		if m.mg.has("flash") and is_instance_valid(m.mg["flash"]):
			(m.mg["flash"] as Label).visible = false
		if m.mg.has("hint_arrow") and is_instance_valid(m.mg["hint_arrow"]):
			(m.mg["hint_arrow"] as Label).visible = false
		_mg_snow_face_phase()
	else:
		_mg_snow_new_ball()


func _mg_snow_face_phase() -> void:
	m.mg["phase"] = "face"
	(m.mg["hud"] as Label).text = "Now give him a face! Tap the carrot and coal."
	var carrot := _mg_artbtn("res://assets/mg/carrot.png", Vector2(360, 600), Vector2(150, 110))
	carrot.pressed.connect(func(): _mg_snow_face("carrot", carrot))
	for i in range(2):
		var coal := _mg_artbtn("res://assets/mg/coal.png", Vector2(250 + float(i) * 220, 600), Vector2(90, 90))
		var idx := i
		coal.pressed.connect(func(): _mg_snow_face("coal" + str(idx), coal))


func _mg_snow_face(_part: String, b: Button) -> void:
	if m.mg_kind != "snowman" or String(m.mg["phase"]) != "face" or not b.visible:
		return
	b.visible = false
	var head: Vector2 = m.mg.get("head_pos", Vector2(980, 210))
	var bit: TextureRect
	if _part == "carrot":
		bit = _mg_sprite("res://assets/mg/carrot.png", head + Vector2(0, 14), Vector2(95, 60))
		m.mg["carrot_bit"] = bit
	elif _part == "coal0":
		bit = _mg_sprite("res://assets/mg/coal.png", head + Vector2(-24, -18), Vector2(42, 42))
	else:
		bit = _mg_sprite("res://assets/mg/coal.png", head + Vector2(24, -18), Vector2(42, 42))
	if not m.mg.has("face_bits"):
		m.mg["face_bits"] = []
	(m.mg["face_bits"] as Array).append(bit)
	m.mg["face"] = int(m.mg["face"]) + 1
	if int(m.mg["face"]) >= 3:
		m.award_sticker("snowman")
		_mg_snow_chase_phase()


func _mg_snow_chase_phase() -> void:
	# HE'S ALIVE! The snowman makes a run for it — chase him down and EAT him,
	# biggest snowball first, until only the carrot is left. Nom nom.
	m.mg["phase"] = "chase"
	m.mg["run_x"] = 980.0
	m.mg["bite_cool"] = 1.0
	m.mg["bites"] = 0
	(m.mg["hud"] as Label).text = "He's ALIVE! Chase him and EAT him!  ← →"
	if m.voice != null:
		m.voice.pitch_scale = 1.4
		m.voice.play()
	var rosh = _mg_sprite(m.skin_sprite_path(), Vector2(160, 470), Vector2(140, 180))
	m.mg["chaser"] = rosh
	m.mg["chaser_x"] = 230.0


func _mg_snow_runner_bits() -> Array:
	var bits: Array = []
	for bv in m.mg.get("body", []):
		if is_instance_valid(bv):
			bits.append(bv)
	for fv in m.mg.get("face_bits", []):
		if is_instance_valid(fv):
			bits.append(fv)
	return bits


func _mg_tick_snow_chase(delta: float) -> void:
	# chaser: stick / arrows / mouse-touch x (same controls as the dolls catcher)
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
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and m.mg2d_stage != null:
		var tx: float = m.mg2d_stage.get_local_mouse_position().x
		mx = clampf((tx - float(m.mg["chaser_x"])) / 120.0, -1.0, 1.0)
	m.mg["chaser_x"] = clampf(float(m.mg["chaser_x"]) + mx * 540.0 * delta, 90.0, 1190.0)
	var chaser: TextureRect = m.mg["chaser"]
	if is_instance_valid(chaser):
		chaser.position.x = float(m.mg["chaser_x"]) - 70.0
		chaser.flip_h = mx < -0.05
	m.mg["bite_cool"] = maxf(0.0, float(m.mg["bite_cool"]) - delta)
	var cx: float = float(m.mg["chaser_x"])
	var rx: float = float(m.mg["run_x"])
	if String(m.mg["phase"]) == "chase":
		# the snowman flees (faster with every bite), pinned to the stage
		var bites: int = int(m.mg["bites"])
		var flee: float = signf(rx - cx)
		if flee == 0.0:
			flee = 1.0
		var spd: float = 250.0 + float(bites) * 90.0
		var nrx: float = rx + flee * spd * delta + sin(float(m.mg["t"]) * 3.0) * 40.0 * delta
		if nrx < 110.0 or nrx > 1170.0:
			nrx = clampf(nrx, 110.0, 1170.0)
		var dx: float = nrx - rx
		m.mg["run_x"] = nrx
		for bit in _mg_snow_runner_bits():
			(bit as Control).position.x += dx
			(bit as Control).rotation = sin(float(m.mg["t"]) * 10.0) * 0.08   # frantic waddle
		# CHOMP: catch him and the biggest snowball disappears
		if float(m.mg["bite_cool"]) <= 0.0 and absf(nrx - cx) < 95.0:
			m.mg["bite_cool"] = 0.9
			m.mg["bites"] = bites + 1
			if m.chime != null:
				m.chime.pitch_scale = 0.62 + float(bites) * 0.08
				m.chime.play()
			(m.mg["hud"] as Label).text = ["CHOMP!", "NOM NOM!", "CRUNCH!"][mini(bites, 2)] + "  Keep eating!"
			var body: Array = m.mg.get("body", [])
			if not body.is_empty():
				var ball: Panel = body.pop_front()   # biggest (bottom) first
				if is_instance_valid(ball):
					var bt = ball.create_tween()
					bt.tween_property(ball, "scale", Vector2(1.3, 0.2), 0.18)
					bt.tween_callback(ball.queue_free)
			if int(m.mg["bites"]) >= 3:
				# only the carrot survives — it drops to the snow
				m.mg["phase"] = "carrot"
				(m.mg["hud"] as Label).text = "He's all gone... but the CARROT! Grab it!"
				for fv in m.mg.get("face_bits", []):
					if is_instance_valid(fv) and fv != m.mg.get("carrot_bit"):
						(fv as Control).queue_free()
				var car: TextureRect = m.mg.get("carrot_bit")
				if is_instance_valid(car):
					var ct := car.create_tween()
					ct.tween_property(car, "position", Vector2(float(m.mg["run_x"]) - 47.0, 560.0), 0.5).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	elif String(m.mg["phase"]) == "carrot":
		var car2: TextureRect = m.mg.get("carrot_bit")
		if is_instance_valid(car2) and absf((car2.position.x + 47.0) - cx) < 75.0:
			# Stop polling the carrot during the victory-close tween. Leaving the
			# phase on "carrot" retries a queued-free node every frame.
			m.mg["phase"] = "done"
			m.mg.erase("carrot_bit")
			car2.queue_free()
			if m.chime != null:
				m.chime.pitch_scale = 1.5
				m.chime.play()
			m.award_sticker("carrot")
			_mg2d_win("CRUNCH! Best snowman snack EVER!")

# ---- GARDEN: tap sprouts to grow them into flowers ----


func _mg_build_garden() -> void:
	m.mg["grown"] = 0
	m.mg["stage"] = [0, 0, 0, 0, 0]
	m.mg["flowers"] = ["k_flower1", "flower", "flower2", "k_flower2", "flower3"]   # each plant ends as a DIFFERENT flower
	(m.mg["hud"] as Label).text = "Tap each seed to grow it: seed, then sprout, then a FLOWER!"
	_mg_sprite("res://assets/mg/sun.png", Vector2(120, 130), Vector2(180, 180))
	# a soft grassy mound across the bottom
	var mound := _mg_circle(Vector2(640, 1050), 760.0, Color(0.5, 0.78, 0.45))
	mound.size.y = 500.0
	mound.position = Vector2(-120, 640)
	# five clay pots, each starting as a SEED
	for i in range(5):
		var x := 180.0 + float(i) * 240.0
		var potm := _mg_circle(Vector2(x, 640), 64.0, Color(0.78, 0.42, 0.28))
		potm.size = Vector2(150, 100)
		potm.position = Vector2(x - 75, 600)
		var sp := _mg_artbtn("res://assets/mg/seed.png", Vector2(x, 600), Vector2(72, 72))
		sp.set_meta("hx", x)
		var idx := i
		sp.pressed.connect(func(): _mg_garden_tap(idx, sp))
	# Roshan watering, watching over the garden
	_mg_sprite(m.skin_sprite_path(), Vector2(1140, 360), Vector2(180, 230))
	_mg_sprite("res://assets/mg/wateringcan.png", Vector2(1010, 430), Vector2(150, 130))
	# a couple of drifting butterflies
	for bi in range(3):
		var bf := _mg_sprite("res://assets/mg/butterfly.png", Vector2(300 + float(bi) * 350, 220), Vector2(90, 90))
		bf.set_meta("bf", float(bi))


func _mg_garden_tap(i: int, b: Button) -> void:
	if m.mg_kind != "garden":
		return
	var st: Array = m.mg["stage"]
	if int(st[i]) >= 2:
		return
	st[i] = int(st[i]) + 1
	var x: float = b.get_meta("hx")
	m._sparkle_burst(m.player.position + Vector3(0, 1, 0), Color(0.4, 0.7, 1.0))
	var tex = b.get_child(0) as TextureRect
	if int(st[i]) == 1:
		# seed -> seedling (same small sprout for every plant)
		tex.texture = load("res://assets/mg/k_sprout.png")
		b.size = Vector2(120, 150)
		b.custom_minimum_size = b.size
		b.position = Vector2(x, 540) - b.size * 0.5
	else:
		# seedling -> a distinct flower, with a happy pop
		tex.texture = load("res://assets/mg/" + String((m.mg["flowers"] as Array)[i]) + ".png")
		b.size = Vector2(175, 205)
		b.custom_minimum_size = b.size
		b.position = Vector2(x, 495) - b.size * 0.5
		b.pivot_offset = b.size * 0.5
		b.disabled = true
		var tw = m.create_tween()
		tw.tween_property(b, "scale", Vector2(1.2, 1.2), 0.12)
		tw.tween_property(b, "scale", Vector2(1.0, 1.0), 0.12)
		m.mg["grown"] = int(m.mg["grown"]) + 1
		if int(m.mg["grown"]) >= 5:
			_mg2d_win("Look at my beautiful flower garden!")

# ---- TRAMPOLINE: tap BOUNCE to jump up to the star ----


func _mg_build_trampoline() -> void:
	m.mg["bounces"] = 0
	m.mg["star_y"] = 90.0
	(m.mg["hud"] as Label).text = "Tap JUMP to bounce up and TOUCH the star!"
	m.mg["star"] = _mg_sprite("res://assets/mg/star.png", Vector2(640, 90), Vector2(140, 140))
	# trampoline (kept high enough that the JUMP button fits on the 1280x720 stage in landscape)
	var tramp := _mg_circle(Vector2(640, 520), 200.0, Color(0.25, 0.5, 0.85))
	tramp.size.y = 56.0
	tramp.position = Vector2(640 - 200, 492)
	m.mg["rest_y"] = 430.0
	m.mg["roshan"] = _mg_sprite(m.skin_sprite_path(), Vector2(640, 430), Vector2(150, 190))
	var b := _mg_roundbtn(Vector2(640, 648), 66.0, Color(0.3, 0.6, 1.0), "JUMP")
	b.pressed.connect(_mg_tramp_tap)


func _mg_tramp_tap() -> void:
	if m.mg_kind != "trampoline":
		return
	m.mg["bounces"] = int(m.mg["bounces"]) + 1
	var r: TextureRect = m.mg["roshan"]
	var rest_y: float = float(m.mg.get("rest_y", 430.0))
	var star_y: float = float(m.mg.get("star_y", 90.0))
	# each bounce reaches higher; Roshan only WINS when her sprite actually reaches the star
	var apex_center: float = rest_y - float(m.mg["bounces"]) * 85.0
	var sprite_top: float = apex_center - 95.0
	var reached: bool = sprite_top <= star_y + 35.0
	if reached:
		apex_center = star_y + 110.0   # land her right at the star
	var rest_top: float = rest_y - 95.0
	var tw = m.create_tween()
	tw.tween_property(r, "position:y", apex_center - 95.0, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(r, "position:y", rest_top, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	if reached:
		tw.tween_callback(func(): _mg2d_win("Boing! I touched the star!"))

# ---- SLIDE: tap GO, ride the rainbow slide ----


func _mg_build_slide() -> void:
	m.mg["phase"] = "ready"
	(m.mg["hud"] as Label).text = "Tap GO for the rainbow slide!"
	# the rainbow slide bands (diagonal)
	var cols := [Color(0.9, 0.2, 0.3), Color(1.0, 0.6, 0.2), Color(1.0, 0.9, 0.3), Color(0.3, 0.8, 0.4), Color(0.3, 0.6, 1.0), Color(0.6, 0.4, 0.9)]
	for i in range(cols.size()):
		var band := ColorRect.new()
		band.color = cols[i]
		band.size = Vector2(1500, 60)
		band.position = Vector2(-100, 150 + float(i) * 58.0)
		band.rotation = 0.5
		m.mg2d_stage.add_child(band)
	m.mg["roshan"] = _mg_sprite(m.skin_sprite_path(), Vector2(160, 150), Vector2(140, 180))
	var b := _mg_roundbtn(Vector2(640, 650), 80.0, Color(1.0, 0.5, 0.7), "GO!")
	b.pressed.connect(_mg_slide_go)


func _mg_slide_go() -> void:
	if m.mg_kind != "slide" or String(m.mg["phase"]) != "ready":
		return
	m.mg["phase"] = "ride"
	m.mg["ride_t"] = 0.0
	(m.mg["btns"] as Array)[0].visible = false

# ---- XMAS: tap ornaments onto the tree, friendship flower on top ----


func _mg_build_xmas() -> void:
	m.mg["placed"] = 0
	(m.mg["hud"] as Label).text = "Tap the ornaments onto the tree!"
	_mg_sprite("res://assets/mg/xtree.png", Vector2(640, 430), Vector2(420, 560))
	m.mg["orn_spots"] = [Vector2(640, 300), Vector2(580, 400), Vector2(700, 400), Vector2(600, 520), Vector2(700, 520)]
	for i in range(5):
		var o := _mg_artbtn("res://assets/mg/orn" + str(i + 1) + ".png", Vector2(180 + float(i) * 150, 660), Vector2(110, 110))
		var idx := i
		o.pressed.connect(func(): _mg_xmas_tap(idx, o))
	var fl := _mg_artbtn("res://assets/book/friendship_flower.png", Vector2(1050, 660), Vector2(130, 130))
	fl.disabled = true
	fl.modulate = Color(0.5, 0.5, 0.5)
	fl.pressed.connect(_mg_xmas_flower)
	m.mg["flowerbtn"] = fl


func _mg_xmas_tap(i: int, b: Button) -> void:
	if m.mg_kind != "xmas" or not b.visible:
		return
	b.visible = false
	var spots: Array = m.mg["orn_spots"]
	_mg_sprite("res://assets/mg/orn" + str(i + 1) + ".png", spots[i], Vector2(70, 70))
	m.mg["placed"] = int(m.mg["placed"]) + 1
	if int(m.mg["placed"]) >= 5:
		(m.mg["flowerbtn"] as Button).disabled = false
		(m.mg["flowerbtn"] as Button).modulate = Color(1.3, 1.3, 1.0)


func _mg_xmas_flower() -> void:
	if m.mg_kind != "xmas" or int(m.mg["placed"]) < 5:
		return
	_mg_sprite("res://assets/book/friendship_flower.png", Vector2(640, 200), Vector2(140, 130))
	_mg2d_win("The friendship flower on top! It is beautiful!")
