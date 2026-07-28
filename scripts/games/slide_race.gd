class_name SlideRaceGame
extends RefCounted
# Two related movement games with separate visual identities:
# an indoor soft-play climb and a downhill winter/rainbow slide.

const PLAYPLACE_BACKGROUND := "res://assets/minigames/slide_race/playplace.png"
const PENGUIN_BACKGROUND := "res://assets/minigames/slide_race/penguin_slide.png"
const RAINBOW_BACKGROUND := "res://assets/minigames/slide_race/rainbow_slide.png"
const PENGUIN_SPRITE := "res://assets/minigames/slide_race/penguin.png"
const CHECKPOINT_SPRITE := "res://assets/minigames/slide_race/checkpoint.svg"
const HOOP_SPRITE := "res://assets/minigames/slide_race/hoop.svg"
const FISH_SPRITE := "res://assets/minigames/slide_race/fish.svg"
const SNOWBALL_SPRITE := "res://assets/minigames/slide_race/snowball.svg"
const ICE_TRACK := "res://assets/minigames/slide_race/track_ice.svg"
const RAINBOW_TRACK := "res://assets/minigames/slide_race/track_rainbow.svg"
const ROSHAN_SLIDE := "res://assets/minigames/shared/roshan_catch.png"

const SLIDE_WIDTH := 18.0
const SLIDE_GRAV := 44.0
const SLIDE_FRICT := 0.32
const SLIDE_VMAX := 26.0
const SLIDE_VMIN := 13.0
const SLIDE_STEER := 38.0
const SLIDE_RIDE := 2.2
const SLIDE_LEAD := 22.0

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

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

func _background(path: String, height: float, pos: Vector3) -> Sprite3D:
	var plate := _sprite(path, height, pos)
	plate.name = "AuthoredBackgroundPlate"
	plate.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	plate.render_priority = -10
	return plate

func _add_check(pos: Vector3, kind: String) -> void:
	var node := _sprite(CHECKPOINT_SPRITE, 3.5, pos)
	node.name = "CourseCheckpoint_%s" % kind
	(m.g["checks"] as Array).append({"node": node, "hit": false, "kind": kind})

func _build_playplace(origin: Vector3, fr: Dictionary) -> void:
	var ground_y: float = m.ARENA_POS.y
	_background(PLAYPLACE_BACKGROUND, 34.0, origin + Vector3(0.0, 17.0, -20.0))
	m.g["chains"] = []

	var pit := Vector3(origin.x + 14.0, ground_y + 2.4, origin.z)
	var trampoline := Vector3(origin.x - 13.0, ground_y + 3.0, origin.z + 8.0)
	m.g["tramp_pos"] = trampoline

	var mover_pos := Vector3(origin.x - 6.0, ground_y + 19.0, origin.z + 6.0)
	var mover := _sprite(HOOP_SPRITE, 6.2, mover_pos)
	mover.name = "MovingSoftPlayHoop"
	m.g["mover_node"] = mover
	m.g["mover_base"] = mover.position

	var path: Array = [
		Vector3(origin.x, ground_y + 29.0, origin.z),
		Vector3(origin.x + 6.0, ground_y + 25.5, origin.z + 4.0),
		Vector3(origin.x + 11.0, ground_y + 21.0, origin.z + 8.0),
		Vector3(origin.x + 14.5, ground_y + 15.5, origin.z + 12.0),
		Vector3(origin.x + 16.0, ground_y + 10.0, origin.z + 16.5),
		Vector3(origin.x + 15.0, ground_y + 5.0, origin.z + 21.0),
		Vector3(origin.x + 12.5, ground_y + 2.8, origin.z + 25.0),
	]
	m.g["slide_path"] = path

	var friend_node: Variant = fr.get("node")
	if friend_node != null and is_instance_valid(friend_node) and friend_node is Sprite3D:
		var cheer := Sprite3D.new()
		cheer.texture = (friend_node as Sprite3D).texture
		cheer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		cheer.shaded = false
		cheer.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		cheer.pixel_size = 7.0 / maxf(1.0, float(cheer.texture.get_height()))
		cheer.position = (path[0] as Vector3) + Vector3(-3.0, 3.0, -2.0)
		m.add_child(cheer)
		m.game_nodes.append(cheer)

	_add_check(pit + Vector3(0, 1.6, 0), "ball")
	_add_check(trampoline + Vector3(0, 1.8, 0), "tramp")
	_add_check(Vector3(origin.x, ground_y + 14.6, origin.z - 11.0), "curtain")
	_add_check(mover_pos, "mover")
	_add_check(Vector3(origin.x + 4.0, ground_y + 24.6, origin.z + 8.0), "curtain")
	_add_check(path[0] as Vector3, "slide")

func _track_card(a: Vector3, b: Vector3, texture_path: String) -> void:
	var direction: Vector3 = b - a
	var length: float = direction.length()
	if length < 0.001:
		return
	var forward: Vector3 = direction / length
	var right: Vector3 = Vector3.UP.cross(forward)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	right = right.normalized()
	var up: Vector3 = forward.cross(right).normalized()
	var card := Sprite3D.new()
	card.texture = load(texture_path)
	card.pixel_size = 1.0 / maxf(1.0, float(card.texture.get_height()))
	var base_width: float = float(card.texture.get_width()) * card.pixel_size
	card.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	card.shaded = false
	card.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	card.transform = Transform3D(Basis(-right, forward, up), (a + b) * 0.5 + up * 0.04)
	card.scale = Vector3((SLIDE_WIDTH + 2.4) / base_width, length + 1.2, 1.0)
	m.add_child(card)
	m.game_nodes.append(card)

func _build_slide(origin: Vector3, theme: String = "ice", mode: String = "fish") -> void:
	var path: Array = []
	var sample_count := 26
	for i in range(sample_count + 1):
		var fraction: float = float(i) / float(sample_count)
		var z: float = lerp(-110.0, 120.0, fraction)
		var x: float = sin(fraction * TAU * 0.85) * 24.0
		var y: float = 2.0 + 48.0 * pow(1.0 - fraction, 1.2)
		path.append(origin + Vector3(x, y, z))
	m.g["path"] = path

	var cumulative: Array = [0.0]
	var total := 0.0
	for i in range(path.size() - 1):
		total += (path[i + 1] as Vector3).distance_to(path[i] as Vector3)
		cumulative.append(total)
	m.g["cum"] = cumulative
	m.g["total"] = total
	m.g["s"] = 0.0
	m.g["v"] = SLIDE_VMIN
	m.g["x"] = 0.0
	m.g["vx"] = 0.0
	m.g["got"] = 0
	m.g["caught"] = false

	var track_texture := RAINBOW_TRACK if theme == "rainbow" else ICE_TRACK
	for i in range(path.size() - 1):
		_track_card(path[i] as Vector3, path[i + 1] as Vector3, track_texture)

	var backdrop_path := RAINBOW_BACKGROUND if theme == "rainbow" else PENGUIN_BACKGROUND
	var backdrop := _background(backdrop_path, 58.0, origin + Vector3(0.0, 30.0, -35.0))
	backdrop.name = "MovingSlideVista"
	m.g["slide_backdrop"] = backdrop

	for k in range(6):
		var fraction: float = 0.12 + 0.72 * float(k) / 5.0
		var sample: Array = _slide_sample(fraction * total)
		var side: float = -1.0 if k % 2 == 0 else 1.0
		var cheer_pos: Vector3 = (sample[0] as Vector3) \
			+ (sample[2] as Vector3) * (side * (SLIDE_WIDTH * 0.5 + 4.0)) \
			+ Vector3(0, 2.0, 0)
		var cheer := _sprite(PENGUIN_SPRITE, 4.0, cheer_pos)
		cheer.flip_h = side < 0.0
		cheer.rotation.z = side * 0.12

	m.g["fish"] = []
	if mode == "chase":
		var baby_pos: Vector3 = (_slide_sample(40.0)[0] as Vector3) + Vector3(0, SLIDE_RIDE, 0)
		var baby := _sprite(PENGUIN_SPRITE, 4.6, baby_pos)
		baby.name = "RacingBabyPenguin"
		m.g["peng_node"] = baby
		m.g["peng_x"] = 0.0
	else:
		var spots := [0.16, 0.34, 0.52, 0.70, 0.86]
		var sides := [-1.0, 1.0, -0.4, 1.0, -1.0]
		for k in range(spots.size()):
			var sample: Array = _slide_sample(float(spots[k]) * total)
			var fish_pos: Vector3 = (sample[0] as Vector3) \
				+ (sample[2] as Vector3) * (float(sides[k]) * SLIDE_WIDTH * 0.32) \
				+ Vector3(0, SLIDE_RIDE + 1.6, 0)
			var glow := _sprite(CHECKPOINT_SPRITE, 5.2, fish_pos)
			glow.modulate = Color(1.0, 0.9, 0.5, 0.42)
			var fish := _sprite(FISH_SPRITE, 2.8, fish_pos)
			fish.flip_h = k % 2 == 1
			(m.g["fish"] as Array).append({
				"node": fish,
				"halo": glow,
				"pos": fish_pos,
				"got": false,
			})
		var ball := _sprite(SNOWBALL_SPRITE, 12.0, origin)
		ball.name = "FriendlyChaseSnowball"
		m.g["ball"] = ball

	var top: Array = _slide_sample(0.0)
	m.player.position = (top[0] as Vector3) + Vector3(0, SLIDE_RIDE, 0)
	m.player.vel = Vector3.ZERO
	m.player.yaw = atan2((top[1] as Vector3).x, (top[1] as Vector3).z)

func _slide_pos(distance: float) -> Vector3:
	var path: Array = m.g["path"]
	var cumulative: Array = m.g["cum"]
	var total: float = float(m.g["total"])
	distance = clampf(distance, 0.0, total)
	var i := 0
	while i < cumulative.size() - 2 and float(cumulative[i + 1]) < distance:
		i += 1
	var segment_length: float = float(cumulative[i + 1]) - float(cumulative[i])
	var fraction: float = 0.0 if segment_length < 0.001 else \
		(distance - float(cumulative[i])) / segment_length
	var p0: Vector3 = path[maxi(i - 1, 0)]
	var p1: Vector3 = path[i]
	var p2: Vector3 = path[mini(i + 1, path.size() - 1)]
	var p3: Vector3 = path[mini(i + 2, path.size() - 1)]
	var f2: float = fraction * fraction
	var f3: float = f2 * fraction
	return ((p1 * 2.0) + (p2 - p0) * fraction \
		+ (p0 * 2.0 - p1 * 5.0 + p2 * 4.0 - p3) * f2 \
		+ (p1 * 3.0 - p0 - p2 * 3.0 + p3) * f3) * 0.5

func _slide_sample(distance: float) -> Array:
	var pos := _slide_pos(distance)
	var direction: Vector3 = _slide_pos(distance + 1.5) - _slide_pos(distance - 1.5)
	var forward := direction.normalized() if direction.length() > 0.001 else Vector3.FORWARD
	var right: Vector3 = Vector3.UP.cross(forward)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [pos, forward, right.normalized()]

func _tick_slide(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var total: float = float(m.g["total"])
	var distance: float = float(m.g["s"])
	var sample: Array = _slide_sample(distance)
	var tangent: Vector3 = sample[1]
	var right: Vector3 = sample[2]
	var steer := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		steer -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		steer += 1.0
	var joy_x: float = m.joy_axis(JOY_AXIS_LEFT_X)
	if absf(joy_x) > 0.2:
		steer += joy_x
	if m.touch_ui != null and absf(m.touch_ui.stick_vec.x) > 0.15:
		steer += m.touch_ui.stick_vec.x
	steer = clampf(steer, -1.0, 1.0)
	if absf(steer) > 0.15:
		m.g["steered"] = true

	var speed: float = float(m.g["v"])
	var grade: float = -tangent.y
	speed += (SLIDE_GRAV * grade - SLIDE_FRICT * speed) * delta
	speed = clampf(speed, SLIDE_VMIN, SLIDE_VMAX)
	m.g["v"] = speed
	m.g["s"] = distance + speed * delta

	var lateral_speed: float = float(m.g["vx"])
	lateral_speed -= steer * SLIDE_STEER * delta
	lateral_speed *= pow(0.02, delta)
	var lateral: float = float(m.g["x"]) + lateral_speed * delta
	var limit: float = SLIDE_WIDTH * 0.5 - 2.0
	if absf(lateral) > limit:
		lateral = clampf(lateral, -limit, limit)
		lateral_speed *= -0.3
	m.g["x"] = lateral
	m.g["vx"] = lateral_speed

	var pos: Vector3 = (sample[0] as Vector3) + right * lateral + Vector3(0, SLIDE_RIDE, 0)
	m.player.position = pos
	m.player.yaw = atan2(tangent.x, tangent.z)
	m.player.rotation = Vector3(-0.2, m.player.yaw + PI, -clampf(lateral_speed * 0.02, -0.45, 0.45))
	var backdrop: Sprite3D = m.g["slide_backdrop"]
	backdrop.position = pos + tangent * 72.0 + Vector3(0.0, 20.0, 0.0)
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var camera_target := pos - tangent * 15.0 + Vector3(0, 7.0, 0)
		m.player.cam.position = m.player.cam.position.lerp(
			camera_target, 1.0 - pow(0.0008, delta))
		m.player.cam.look_at(pos + tangent * 6.0 + Vector3(0, 1.0, 0))

	if String(m.g.get("mode", "fish")) == "chase":
		_tick_penguin_chase(delta, fr, distance, total, lateral, limit, pos)
	else:
		_tick_fish_slide(delta, fr, distance, total, pos)

func _tick_penguin_chase(
		delta: float,
		fr: Dictionary,
		distance: float,
		total: float,
		lateral: float,
		limit: float,
		pos: Vector3) -> void:
	var progress: float = distance / total
	var beany: bool = m.beans_t >= 0.0 or bool(m.g.get("beany", false))
	m.g["beany"] = beany
	var gap: float
	if beany:
		gap = maxf(0.0, SLIDE_LEAD * (1.0 - progress * 1.45))
	else:
		var burst: float = float(m.g.get("burst", 0.0))
		var base_gap: float = SLIDE_LEAD * maxf(0.18, 1.0 - progress * 0.75)
		if base_gap + burst < 10.0:
			burst = minf(burst + 34.0 * delta, 18.0)
			m.g["panic_cool"] = float(m.g.get("panic_cool", 5.0)) - delta
			if float(m.g["panic_cool"]) <= 0.0:
				m.g["panic_cool"] = 5.0
				var baby: Variant = m.g.get("peng_node")
				if baby != null and is_instance_valid(baby):
					m._sparkle_burst((baby as Node3D).position + Vector3(0, 1.5, 0),
						Color(0.7, 0.9, 1.0))
				if m.peng_giggle != null:
					m.peng_giggle.pitch_scale = 1.0 + randf() * 0.15
					m.peng_giggle.play()
				if int(m.g.get("panic_n", 0)) < 2:
					m.g["panic_n"] = int(m.g.get("panic_n", 0)) + 1
					m.show_msg(fr["fname"], "He zoomed away! Magic Beans can help!")
		else:
			burst = maxf(0.0, burst - 3.5 * delta)
		m.g["burst"] = burst
		gap = base_gap + burst

	var penguin_distance: float = minf(distance + gap, total)
	var penguin_x: float = float(m.g.get("peng_x", 0.0))
	var flee_direction: float = signf(penguin_x - lateral)
	if flee_direction == 0.0:
		flee_direction = 1.0 if sin(float(m.g["t"]) * 1.3) >= 0.0 else -1.0
	penguin_x += flee_direction * 7.5 * delta
	penguin_x += sin(float(m.g["t"]) * 2.5) * 1.2 * delta
	penguin_x = clampf(penguin_x, -limit, limit)
	m.g["peng_x"] = penguin_x
	var penguin_sample: Array = _slide_sample(penguin_distance)
	var penguin_pos: Vector3 = (penguin_sample[0] as Vector3) \
		+ (penguin_sample[2] as Vector3) * penguin_x \
		+ Vector3(0, SLIDE_RIDE, 0)
	var penguin_node: Variant = m.g.get("peng_node")
	if penguin_node != null and is_instance_valid(penguin_node):
		var penguin: Sprite3D = penguin_node
		penguin.position = penguin_pos
		penguin.flip_h = penguin_x < lateral
		var sprinting: bool = float(m.g.get("burst", 0.0)) > 0.5 or (beany and gap < 13.0)
		penguin.rotation.z = sin(float(m.g["t"]) * (13.0 if sprinting else 9.0)) \
			* (0.08 if sprinting else 0.13)
		penguin.scale = Vector3.ONE * (1.08 if sprinting else 1.0)

	if beany and bool(m.g.get("steered", false)) \
			and not bool(m.g.get("caught", false)) \
			and gap < 9.0 and absf(lateral - penguin_x) < 4.5:
		m.g["caught"] = true
		m.award_sticker("penguin")
		m._sparkle_burst(penguin_pos + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.4))
		if m.peng_giggle != null:
			m.peng_giggle.pitch_scale = 0.95
			m.peng_giggle.play()
		if m.chime != null:
			m.chime.pitch_scale = 1.5
			m.chime.play()
		m._end_game(true, fr, "You caught the baby penguin! Great race!")
		return

	if beany:
		m.hud_game.text = "BEAN POWER! Catch him!   ← →"
	elif float(m.g.get("burst", 0.0)) > 0.5:
		m.hud_game.text = "Too speedy! Beans from the Pearl Shop!   ← →"
	else:
		m.hud_game.text = "Catch the baby penguin!"
	if float(m.g["s"]) >= total - 0.5:
		if bool(m.g.get("steered", false)):
			m._end_game(true, fr, "What a race! Magic Beans can help you catch him next time.")
		else:
			m.g["s"] = 0.0
			m.g["x"] = 0.0
			m.g["vx"] = 0.0
			m.g["burst"] = 0.0
			m.show_msg(fr["fname"], "Lean LEFT or RIGHT to join the race!", "hint")

func _tick_fish_slide(
		delta: float,
		fr: Dictionary,
		_distance: float,
		total: float,
		pos: Vector3) -> void:
	var ball: Variant = m.g.get("ball")
	if ball != null and is_instance_valid(ball):
		var ball_sample: Array = _slide_sample(maxf(0.0, float(m.g["s"]) - 26.0))
		var snowball: Sprite3D = ball
		snowball.position = (ball_sample[0] as Vector3) + Vector3(0, 5.0, 0)
		snowball.rotation.z += delta * 2.2
	for raw_fish in m.g.get("fish", []):
		var fish_data: Dictionary = raw_fish
		if bool(fish_data["got"]):
			continue
		if (fish_data["pos"] as Vector3).distance_to(pos) < 4.2:
			fish_data["got"] = true
			m.g["got"] = int(m.g["got"]) + 1
			var fish_node: Node = fish_data["node"]
			if is_instance_valid(fish_node):
				fish_node.queue_free()
			var glow_node: Node = fish_data["halo"]
			if is_instance_valid(glow_node):
				glow_node.queue_free()
			m._sparkle_burst(pos + Vector3(0, 1.5, 0), Color(1.0, 0.85, 0.4))
			if m.chime != null:
				m.chime.pitch_scale = 1.0 + 0.12 * float(m.g["got"])
				m.chime.play()
	m.hud_game.text = "Slide!  " + m._pips(int(m.g["got"]), 5, "🐟")
	if float(m.g["s"]) >= total - 0.5:
		var caught: int = int(m.g["got"])
		if bool(m.g.get("steered", false)):
			var message := "You grabbed every fish!" if caught >= 5 \
				else "What a ride! You caught %d fish!" % caught
			m._end_game(true, fr, message)
		else:
			m.g["s"] = 0.0
			m.g["x"] = 0.0
			m.g["vx"] = 0.0
			m.show_msg(fr["fname"], "Lean LEFT or RIGHT to join the slide!", "hint")

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.player.set_skin("__minigame_2d", ROSHAN_SLIDE)
	_build_playplace(origin, fr)
	m.show_msg(fr["fname"], "Swim to each glowing shell, all the way up to the BIG slide!")

func build_slide(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	var theme: String = String(fr.get("theme", "ice"))
	var mode: String = String(fr.get("mode", "fish"))
	m.g["mode"] = mode
	m.player.set_skin("__minigame_2d", ROSHAN_SLIDE)
	_build_slide(origin, theme, mode)
	m._play_music("fetch")
	if mode == "chase":
		if m.beans_t >= 0.0:
			m.show_msg(fr["fname"], "BEAN POWER! Steer and catch that speedy penguin!")
		else:
			m.show_msg(fr["fname"], "Race the baby penguin! Steer LEFT and RIGHT!")
			m.get_tree().create_timer(3.6).timeout.connect(func() -> void:
				if m.game == "slide" and String(m.g.get("mode", "")) == "chase" \
						and m.beans_t < 0.0:
					m.show_msg("Roshan", "A snack from the Pearl Shop might make me faster!", "hungry"))
	else:
		m.show_msg(fr["fname"], "Whoosh! Lean LEFT and RIGHT to grab all five fish!")

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	if m.g.has("mover_node"):
		var mover: Sprite3D = m.g["mover_node"]
		mover.position = (m.g["mover_base"] as Vector3) \
			+ Vector3(sin(float(m.g["t"]) * 0.9) * 6.0, 0, 0)
	if String(m.g.get("phase", "")) == "slide":
		var path: Array = m.g["slide_path"]
		var travel: float = float(m.g.get("slide_t", 0.0)) + delta * 13.0
		m.g["slide_t"] = travel
		var accumulated := 0.0
		for i in range(path.size() - 1):
			var segment_length: float = (path[i] as Vector3).distance_to(path[i + 1])
			if travel <= accumulated + segment_length:
				m.player.position = (path[i] as Vector3).lerp(
					path[i + 1], (travel - accumulated) / segment_length)
				m.player.vel = Vector3.ZERO
				m.hud_game.text = "WHEEEEE!"
				return
			accumulated += segment_length
		m._sparkle_burst(m.player.position, Color(0.5, 0.85, 1.0))
		if m.chime != null:
			m.chime.play()
		m._end_game(true, fr, "What a SLIDE! Best play place ever!")
		return

	var checks: Array = m.g.get("checks", [])
	var done := 0
	var next_check: Dictionary = {}
	for raw_check in checks:
		var check: Dictionary = raw_check
		if bool(check["hit"]):
			done += 1
		elif next_check.is_empty():
			next_check = check
	m.hud_game.text = "Glowing shells  " + m._pips(done, checks.size(), "✨")
	if next_check.is_empty():
		return
	var node: Node3D = next_check["node"]
	node.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 5.0) * 0.15)
	node.rotation.z += delta * 0.75

	var previous: Vector3 = m.g.get("ppos_prev", ppos)
	var movement: Vector3 = (ppos - previous) / maxf(delta, 0.001)
	m.g["ppos_prev"] = ppos
	if not bool(m.g.get("armed", false)):
		var toward: Vector3 = node.position - ppos
		if toward.length() > 0.5 and movement.dot(toward.normalized()) > 2.0:
			m.g["arm_t"] = float(m.g.get("arm_t", 0.0)) + delta
			if float(m.g["arm_t"]) >= 0.2:
				m.g["armed"] = true
				m._sparkle_burst(ppos, Color(1.0, 0.95, 0.6))
		else:
			m.g["arm_t"] = 0.0
			m.g["guide_t"] = float(m.g.get("guide_t", 0.0)) - delta
			if float(m.g["guide_t"]) <= 0.0:
				m.g["guide_t"] = 0.8
				m._sparkle_burst(ppos.lerp(node.position, 0.35), Color(1.0, 0.9, 0.5))
				m._sparkle_burst(ppos.lerp(node.position, 0.65), Color(1.0, 0.9, 0.5))
			m.g["arm_hint_t"] = float(m.g.get("arm_hint_t", 0.0)) + delta
			if float(m.g["arm_hint_t"]) > 6.0 and not bool(m.g.get("arm_hinted", false)):
				m.g["arm_hinted"] = true
				m.show_msg(String(fr.get("fname", "Play Place")),
					"Swim to the twinkly shell to start!", "hint")
		if not bool(m.g.get("armed", false)):
			return

	var distance: float = node.position.distance_to(ppos)
	if distance < 34.0:
		m.player.position = m.player.position.lerp(
			node.position, minf(0.92, delta * 2.6 * (1.0 - distance / 34.0)))
		m.player.vel.y = maxf(m.player.vel.y, 0.0)
	if distance < 7.5:
		next_check["hit"] = true
		m._sparkle_burst(node.position, Color(1.0, 0.9, 0.5))
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + float(done) * 0.08
			m.chime.play()
		var kind := String(next_check["kind"])
		if kind == "tramp":
			m.player.vel.y = 26.0
			m.show_msg(fr["fname"], "BOING! Up you go!")
		elif kind == "slide":
			m.g["phase"] = "slide"
			m.g["slide_t"] = 0.0
		elif kind == "chest":
			m.pearl_count += 3
			m._update_hud()
			m._write_save()
			m._sparkle_burst(node.position, Color(1.0, 0.85, 0.3))
			m.award_sticker("treasure")
			m._end_game(true, fr, "TREASURE! +3 rainbow pearls for the Pearl Shop!")
		else:
			node.visible = false
