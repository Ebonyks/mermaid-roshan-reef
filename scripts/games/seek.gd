class_name SeekGame
extends RefCounted
# Lamb-a's no-fail hide-and-seek loop, reconstructed as an authored 2D meadow
# plate with separate bush and character standees. State remains on main.

const BACKGROUND := "res://assets/minigames/seek/background.png"
const BUSH_SPRITE := "res://assets/minigames/seek/bush.png"
const LAMB_SPRITE := "res://assets/minigames/seek/lamb.png"
const ROSHAN_SEEK := "res://assets/minigames/shared/roshan_catch.png"

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _lamb_meadow_placement_allowed(local: Vector2, role: String) -> bool:
	# Retained as the deterministic layout contract used by the trusted audit:
	# hide sockets stay clear and tropical palms do not enter this meadow.
	if local.length() < 15.0 or local.length() > 44.0 or role == "tree_palm":
		return false
	var clearance: float = 12.0 if role.begins_with("tree_") else 8.5
	for bush_offset: Vector3 in m.BTN_OFFS:
		if local.distance_to(Vector2(bush_offset.x, bush_offset.z)) < clearance:
			return false
	return true

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["found"] = 0
	m.g["timer"] = -1.0
	m.g["help_t"] = 0.0
	m.g["seek_anchor"] = m.player.position
	m.g["bushes"] = []
	m.player.set_skin("__minigame_2d", ROSHAN_SEEK)
	_add_meadow_plate(origin)
	for i in range(4):
		var bush := _standee(BUSH_SPRITE, 5.8,
			origin + m.BTN_OFFS[i] + Vector3(0, 0.6, 0))
		(m.g["bushes"] as Array).append(bush)
	var lamb := _standee(LAMB_SPRITE, 4.8, origin)
	m.g["lamb"] = lamb
	_seek_hide()
	m.show_msg(fr["fname"], "Lamb-a' is playing in the meadow! Find her behind a wiggly bush!")

func _add_meadow_plate(origin: Vector3) -> void:
	var plate := Sprite3D.new()
	plate.texture = load(BACKGROUND)
	plate.pixel_size = 1.0 / maxf(1.0, float(plate.texture.get_height()))
	plate.rotation_degrees.x = -90.0
	plate.position = origin + Vector3(0, 0.15, 0)
	var base_width: float = float(plate.texture.get_width()) * plate.pixel_size
	plate.scale = Vector3(58.0 / base_width, 34.0, 1.0)
	plate.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	plate.shaded = false
	plate.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	m.add_child(plate)
	m.game_nodes.append(plate)

func _standee(path: String, height: float, pos: Vector3) -> Node3D:
	var holder := Node3D.new()
	holder.position = pos
	m.add_child(holder)
	m.game_nodes.append(holder)
	var sprite := Sprite3D.new()
	sprite.texture = load(path)
	sprite.pixel_size = height / maxf(1.0, float(sprite.texture.get_height()))
	sprite.position.y = height * 0.5
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	holder.add_child(sprite)
	return holder

func tick(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m.hud_game.text = "Find Lamb-a'!  " + m._pips(int(m.g["found"]), 4, "🐑")
	# Giggles remain an audio beacon, so the goal is never reading-dependent.
	m.g["gig_t"] = float(m.g.get("gig_t", 2.0)) - delta
	if float(m.g["gig_t"]) <= 0.0:
		m.g["gig_t"] = 2.8
		if m.voice != null:
			m.voice.pitch_scale = 1.45 + randf() * 0.15
			m.voice.play()
	var which: int = int(m.g.get("which", 0))
	var bush: Node3D = (m.g["bushes"] as Array)[which]
	m.g["help_t"] = float(m.g.get("help_t", 0.0)) + delta
	var help_radius: float = minf(9.0, 4.0 + float(m.g["help_t"]) * 0.35)
	var seek_anchor: Vector3 = m.g.get("seek_anchor", ppos)
	var moved_to_seek: bool = ppos.distance_to(seek_anchor) > 0.75
	var hit: bool = m._btn_pressed() == which or (moved_to_seek and bush.position.distance_to(ppos) < help_radius)
	if hit:
		m.g["slow_find"] = maxf(float(m.g.get("slow_find", 0.0)), float(m.g["help_t"]))
		m.g["found"] = int(m.g["found"]) + 1
		m.g["help_t"] = 0.0
		var lamb: Node3D = m.g["lamb"]
		lamb.position = bush.position + Vector3(0, 0.5, 0.8)
		var reveal := m.create_tween()
		reveal.tween_property(lamb, "scale", Vector3.ONE * 1.3, 0.2)
		reveal.tween_property(lamb, "scale", Vector3.ONE, 0.3)
		if m.voice != null:
			m.voice.pitch_scale = 1.0 + randf() * 0.3
			m.voice.play()
		if int(m.g["found"]) >= 4:
			m._end_game(true, fr, "You found Lamb-a' every time! Best seeker ever!")
			return
		_seek_hide()

func _seek_hide() -> void:
	m.g["seek_anchor"] = m.player.position
	m.g["which"] = randi() % 4
	var bush: Node3D = (m.g["bushes"] as Array)[int(m.g["which"])]
	var lamb: Node3D = m.g["lamb"]
	lamb.position = bush.position + Vector3(0, 0.5, -2.2)
	lamb.rotation.y = 0.0
	if m.g.get("wiggle_tw") != null and (m.g["wiggle_tw"] as Tween).is_valid():
		(m.g["wiggle_tw"] as Tween).kill()
	var wiggle := m.create_tween().set_loops()
	wiggle.tween_property(bush, "scale", Vector3(1.18, 0.84, 1.0), 0.16)
	wiggle.tween_property(bush, "scale", Vector3.ONE, 0.16)
	wiggle.tween_interval(0.9)
	m.g["wiggle_tw"] = wiggle
	m.g["gig_t"] = 2.2
