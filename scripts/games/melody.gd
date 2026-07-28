class_name MelodyGame
extends RefCounted
# Daddy Mermaid's seven-color catch concert. The gameplay remains spatial and
# no-fail; its presentation is now a custom 2D pavilion with live sprite orbs.

const BACKGROUND := "res://assets/minigames/melody/background.png"
const ORB_SPRITE := "res://assets/minigames/melody/orb.svg"
const ROSHAN_CATCH := "res://assets/minigames/shared/roshan_catch.png"
const RAINBOW := [
	Color(1.0, 0.24, 0.28),
	Color(1.0, 0.54, 0.18),
	Color(1.0, 0.86, 0.24),
	Color(0.30, 0.84, 0.42),
	Color(0.24, 0.68, 0.96),
	Color(0.39, 0.38, 0.88),
	Color(0.72, 0.40, 0.90),
]

var m: ReefMain
var stage_root: Node3D

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["caught"] = 0
	m.g["orbs"] = []
	m.player.set_skin("__minigame_2d", ROSHAN_CATCH)
	stage_root = Node3D.new()
	stage_root.name = "RainbowTheater2D"
	stage_root.position = origin
	m.add_child(stage_root)
	m.game_nodes.append(stage_root)
	_add_background()
	_add_stage_anchors()
	_add_daddy()
	_build_rainbow_orbs(origin)
	m.show_msg(fr["fname"], "Catch all 7 colors of the rainbow! Swim into the bouncing orbs!")

func _add_background() -> void:
	var background := Sprite3D.new()
	background.name = "BackWall"
	background.texture = load(BACKGROUND)
	background.pixel_size = 32.0 / maxf(1.0, float(background.texture.get_height()))
	background.position = Vector3(0, 16.0, -28.0)
	background.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	background.shaded = false
	background.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	background.render_priority = -10
	stage_root.add_child(background)

func _add_stage_anchors() -> void:
	# Stable names preserve debug/probe lookups while the authored plate carries
	# their visuals. These are non-rendering scene anchors, not model fallbacks.
	for node_name in ["StageDeck", "RainbowArc0", "ProsceniumBulbs", "Runway", "TheaterSeats"]:
		var anchor := Node3D.new()
		anchor.name = node_name
		stage_root.add_child(anchor)

func _add_daddy() -> void:
	var performer := Sprite3D.new()
	performer.name = "StarPerformer"
	performer.texture = m._cutout_tex("daddy")
	performer.pixel_size = 12.0 / maxf(1.0, float(performer.texture.get_height()))
	performer.position = Vector3(0.0, 8.0, -22.0)
	performer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	performer.shaded = false
	performer.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	stage_root.add_child(performer)

func _build_rainbow_orbs(origin: Vector3) -> void:
	for i in range(RAINBOW.size()):
		var orb := Sprite3D.new()
		orb.name = "RainbowCatchOrb%d" % i
		orb.texture = load(ORB_SPRITE)
		orb.pixel_size = 2.7 / maxf(1.0, float(orb.texture.get_height()))
		orb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		orb.shaded = false
		orb.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		orb.modulate = RAINBOW[i]
		orb.position = origin + Vector3(-12.0 + float(i) * 4.0,
			5.0 + fmod(float(i) * 2.7, 8.0),
			-6.0 + fmod(float(i) * 3.3, 12.0))
		m.add_child(orb)
		m.game_nodes.append(orb)
		var velocity := Vector3(sin(float(i) * 2.1),
			sin(float(i) * 1.3) * 0.6,
			cos(float(i) * 1.7)).normalized() * (6.0 + float(i % 3) * 2.0)
		(m.g["orbs"] as Array).append({"node": orb, "vel": velocity, "caught": false})

func _tick_melody(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	var caught: int = int(m.g["caught"])
	m.hud_game.text = "Rainbow colors  " + m._pips(caught, 7, "🌈")
	# The deliberate verb remains swimming toward a color. While Roshan idles,
	# a nearby orb holds outside catch range and sends a visual sparkle pointer.
	var previous: Vector3 = m.g.get("ppos_prev", ppos)
	var movement: Vector3 = (ppos - previous) / maxf(delta, 0.001)
	m.g["ppos_prev"] = ppos
	if movement.length() < 2.0 and caught == 0:
		m.g["still_t"] = float(m.g.get("still_t", 0.0)) + delta
	else:
		m.g["still_t"] = 0.0
	if float(m.g.get("still_t", 0.0)) > 8.0 and not bool(m.g.get("hinted", false)):
		m.g["hinted"] = true
		m.show_msg("Daddy Mermaid", "Swim to the colors! They are waiting for YOU!", "hint")
	for orb_data in m.g["orbs"]:
		if bool(orb_data["caught"]):
			continue
		var orb: Sprite3D = orb_data["node"]
		var velocity: Vector3 = orb_data["vel"]
		orb.position += velocity * delta
		var relative: Vector3 = orb.position - m.ARENA_POS
		if absf(relative.x) > 16.0:
			velocity.x = -velocity.x
			orb.position.x = m.ARENA_POS.x + clampf(relative.x, -16.0, 16.0)
		if relative.y < 2.6 or relative.y > 17.0:
			velocity.y = -velocity.y
			orb.position.y = m.ARENA_POS.y + clampf(relative.y, 2.6, 17.0)
		if absf(relative.z) > 12.0:
			velocity.z = -velocity.z
			orb.position.z = m.ARENA_POS.z + clampf(relative.z, -12.0, 12.0)
		orb_data["vel"] = velocity
		orb.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 6.0 + orb.position.x) * 0.10)
		var to_orb: Vector3 = orb.position - ppos
		var distance: float = maxf(to_orb.length(), 0.001)
		if distance < 22.0 and movement.dot(to_orb / distance) < 2.0:
			orb.position = ppos + (to_orb / distance) * 22.0
			if float(m.g.get("still_t", 0.0)) > 4.0 and fmod(float(m.g["t"]), 1.5) < delta:
				m._sparkle_burst(ppos.lerp(orb.position, 0.4), Color(1.0, 0.95, 0.7))
			continue
		if absf(orb.position.x - ppos.x) < 14.0 \
				and absf(orb.position.y - ppos.y) < 7.0 \
				and absf(orb.position.z - ppos.z) < 14.0:
			orb_data["caught"] = true
			orb.visible = false
			caught += 1
			m.g["caught"] = caught
			m._sparkle_burst(orb.position, orb.modulate)
			if m.chime != null:
				m.chime.pitch_scale = 0.9 + float(caught) * 0.07
				m.chime.play()
			if m.voice != null and caught % 2 == 0:
				m.voice.pitch_scale = 1.0 + randf() * 0.25
				m.voice.play()
			if caught >= 7:
				m._end_game(true, fr, "You caught the WHOLE rainbow! Daddy Mermaid cheers for you!")
				return
