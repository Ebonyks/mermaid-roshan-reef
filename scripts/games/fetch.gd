class_name FetchGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# fetch minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

const BACKGROUND := "res://assets/minigames/fetch/background.png"
const CHUCK_SPRITE := "res://assets/minigames/fetch/chuck.png"
const BALL_SPRITE := "res://assets/minigames/fetch/ball.svg"
const ARROW_SPRITE := "res://assets/minigames/fetch/aim_arrow.svg"
const ROSHAN_THROW := "res://assets/minigames/shared/roshan_catch.png"

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["phase"] = "aim"
	m.g["round"] = 0
	m.g["miss"] = 0
	m.g["timer"] = -1.0
	m.player.set_skin("__minigame_2d", ROSHAN_THROW)
	m.g["ball"] = _sprite(BALL_SPRITE, 1.6, origin + Vector3(0, 1.0, 0))
	# One authored 2D plate replaces the old modeled snow, lake, rocks, dock,
	# forest, and floes while retaining the exact safe/wet gameplay boundary.
	var ground := Sprite3D.new()
	ground.texture = load(BACKGROUND)
	ground.pixel_size = 1.0 / maxf(1.0, float(ground.texture.get_height()))
	ground.rotation_degrees.x = -90.0
	ground.position = origin + Vector3(0, 0.15, 0)
	var ground_base_width: float = float(ground.texture.get_width()) * ground.pixel_size
	ground.scale = Vector3(170.0 / ground_base_width, 100.0, 1.0)
	ground.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	ground.shaded = false
	ground.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	m.add_child(ground)
	m.game_nodes.append(ground)
	var chuck_root := Node3D.new()
	chuck_root.position = origin + Vector3(-8, 0.5, -4)
	m.add_child(chuck_root)
	m.game_nodes.append(chuck_root)
	var chuck_sprite := Sprite3D.new()
	chuck_sprite.texture = load(CHUCK_SPRITE)
	chuck_sprite.pixel_size = 5.2 / maxf(1.0, float(chuck_sprite.texture.get_height()))
	chuck_sprite.position.y = 2.6
	chuck_sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	chuck_sprite.shaded = false
	chuck_sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	chuck_root.add_child(chuck_sprite)
	m.g["chuck"] = chuck_root
	m.g["chuck_sprite"] = chuck_sprite
	m.g["chuck_ap"] = null
	m.g["home"] = chuck_root.position
	m.g["arrow"] = _sprite(ARROW_SPRITE, 2.8, origin + Vector3(0, 2.0, 0))
	m.show_msg(fr["fname"], "Throw the ball for Chuck - but NOT into the lake! Press when the arrow is GREEN!")

func _sprite(path: String, height: float, pos: Vector3) -> Sprite3D:
	var sprite := Sprite3D.new()
	sprite.texture = load(path)
	sprite.pixel_size = height / maxf(1.0, float(sprite.texture.get_height()))
	sprite.position = pos
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	m.add_child(sprite)
	m.game_nodes.append(sprite)
	return sprite

func _chuck_play(anim: String, blend: float = 0.25) -> void:
	var ap: AnimationPlayer = m.g["chuck_ap"]
	if ap != null and ap.has_animation(anim) and ap.current_animation != anim:
		ap.play(anim, blend)

func _tick_fetch(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	var ball: Sprite3D = m.g["ball"]
	var chuck: Node3D = m.g["chuck"]
	if String(m.g["phase"]) == "aim" or String(m.g["phase"]) == "fly":
		# Chuck SITS on the snow, watching Roshan (the ball, once it flies)
		var watch: Vector3 = (ball.position if String(m.g["phase"]) == "fly" else ppos) - chuck.position
		if Vector2(watch.x, watch.z).length() > 0.1:
			chuck.rotation.y = atan2(watch.x, watch.z)
		_chuck_play("sit_excited" if String(m.g["phase"]) == "fly" else "sit_idle", 0.35)
	if String(m.g["phase"]) == "aim":
		var splash_pips: String = "💦".repeat(mini(int(m.g["miss"]), 10))
		m.hud_game.text = "Throw " + m._pips(int(m.g["round"]) + 1, 2, "🎾") + ("   " + splash_pips if splash_pips != "" else "")
		# Roshan HOLDS the ball
		var fdir = Vector3(sin(m.player.yaw + PI), 0, cos(m.player.yaw + PI))
		ball.position = ppos + fdir * 1.3 + Vector3(0, -0.2, 0)
		# sweeping aim — sim: the old 1.5 rad/s sweep outran a 4yo's ~1s reaction
		# (only ~1 in 4 finished). Slower sweep, and it slows FURTHER after each
		# splash so a struggling kid always gets there (skill still shows: fewer
		# splashes = faster win)
		var misses: int = int(m.g["miss"])
		# Each splash makes the safe snow side wider as well as slowing the
		# sweep. After three splashes every throw is safely on the snow, but
		# Roshan must still choose to press THROW to continue.
		var sweep_width := 1.25
		if misses == 2:
			sweep_width = 0.85
		elif misses >= 3:
			sweep_width = 0.55
		var sw: float = sin(float(m.g["t"]) * 0.9 * pow(0.72, float(misses))) * sweep_width
		var dirv := Vector3(sin(sw), 0, -cos(sw))
		m.g["aim_dir"] = dirv
		var arrow: Sprite3D = m.g["arrow"]
		arrow.position = ppos + dirv * 3.2
		arrow.rotation.z = -sw
		var landing: Vector3 = ppos + dirv * 14.0
		var wet: bool = landing.x - m.ARENA_POS.x > 8.2
		arrow.modulate = Color(1.0, 0.35, 0.35) if wet else Color(0.45, 1.0, 0.58)
		# non-reader timing cue: the arrow SWELLS while green and a soft tick
		# plays the moment it turns green — timing by ear, not just by color
		arrow.scale = Vector3.ONE if wet else Vector3.ONE * (1.22 + 0.10 * sin(float(m.g["t"]) * 9.0))
		if not wet and bool(m.g.get("was_wet", true)) and m.chime != null:
			m.chime.pitch_scale = 1.5
			m.chime.play()
		m.g["was_wet"] = wet
		# clicks that land on UI (pause gear, touch buttons) must not throw the ball
		var click_free: bool = Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and m.get_viewport().gui_get_hovered_control() == null
		var pressed: bool = Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B) or click_free or (m.touch_ui != null and m.touch_ui.action_down)
		if pressed and float(m.g.get("press_cool", 0.0)) <= 0.0:
			m.g["press_cool"] = 1.0
			m.g["vel"] = dirv * 11.5 + Vector3(0, 6.5, 0)
			m.g["phase"] = "fly"
			arrow.visible = false
			if m.voice != null:
				m.voice.pitch_scale = 1.1
				m.voice.play()
		m.g["press_cool"] = maxf(0.0, float(m.g.get("press_cool", 0.0)) - delta)
	elif String(m.g["phase"]) == "fly":
		m.hud_game.text = "Wheee!"
		var v: Vector3 = m.g["vel"]
		v.y -= 9.5 * delta
		m.g["vel"] = v
		ball.position += v * delta
		if ball.position.y <= m.ARENA_POS.y + 0.9:
			ball.position.y = m.ARENA_POS.y + 0.9
			if ball.position.x - m.ARENA_POS.x > 8.2:
				# SPLASH - into the lake! No mean buzzer: a cartoon puppy
				# whimper + Wacky hamming it up ("OH NO! Chuck is all WET!")
				m.g["miss"] = int(m.g["miss"]) + 1
				m._sparkle_burst(ball.position, Color(0.4, 0.7, 1.0))
				var bz := AudioStreamPlayer.new()
				bz.stream = load("res://assets/audio/voices/chuck_whimper.ogg")
				bz.bus = "Voice"
				m.add_child(bz)
				bz.play()
				bz.finished.connect(bz.queue_free)
				if int(m.g["miss"]) >= 3:
					m.show_msg(fr["fname"], "Chuck shakes off! Now the arrow stays on the safe snow — press when you're ready!", "splash")
				else:
					m.show_msg(fr["fname"], "SPLASH! Chuck can't swim out there! Try again — green arrow means SNOW!", "splash")
				m.g["phase"] = "aim"
				(m.g["arrow"] as Sprite3D).visible = true
			else:
				m.g["phase"] = "fetch"
	elif String(m.g["phase"]) == "pickup":
		# nose down to grab the ball, then turn for home
		m.hud_game.text = "Chuck is on it!"
		m.g["pickup_t"] = float(m.g.get("pickup_t", 0.8)) - delta
		if float(m.g["pickup_t"]) <= 0.35:
			var mouth := Vector3(sin(chuck.rotation.y), 0, cos(chuck.rotation.y))
			ball.position = chuck.position + mouth * 1.4 + Vector3(0, 1.0, 0)
		if float(m.g["pickup_t"]) <= 0.0:
			m.g["phase"] = "return"
			_chuck_play("run")
	else:
		var target: Vector3 = ball.position
		if String(m.g["phase"]) == "return":
			target = ppos
		var d: Vector3 = target - chuck.position
		d.y = 0.0
		m.hud_game.text = "Chuck is on it!"
		if d.length() > 2.0:
			chuck.position += d.normalized() * minf(40.0 * delta, d.length())
			chuck.rotation.y = atan2(d.x, d.z)
			_chuck_play("run")
			if String(m.g["phase"]) == "return":
				var mouth := Vector3(sin(chuck.rotation.y), 0, cos(chuck.rotation.y))
				ball.position = chuck.position + mouth * 1.4 + Vector3(0, 1.0, 0)
		elif String(m.g["phase"]) == "fetch":
			m.g["phase"] = "pickup"
			m.g["pickup_t"] = 0.8
			_chuck_play("pickup", 0.15)
		else:
			m.g["round"] = int(m.g["round"]) + 1
			_chuck_play("wag", 0.2)
			if int(m.g["round"]) >= 2:
				m._say("chuck", "bark")
				m._end_game(true, fr, "Chuck loves to fetch! What a good boy!")
			else:
				m.g["phase"] = "aim"
				(m.g["arrow"] as Sprite3D).visible = true
