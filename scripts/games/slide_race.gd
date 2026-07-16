class_name SlideRaceGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# race minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.g["chains"] = []
	m._build_playplace(origin, fr)
	m.show_msg(fr["fname"], "Welcome to the play place! Touch the sparkles all the way up to the BIG slide!")

func build_slide(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0   # no countdown — reaching the bottom ends it (~12s run)
	var theme: String = String(fr.get("theme", "ice"))
	var mode: String = String(fr.get("mode", "fish"))
	m.g["mode"] = mode
	m._build_slide(origin, theme, mode)
	m._play_music("fetch")   # reuse the snowy track
	if theme == "rainbow":
		m.arena_env.background_color = Color(0.72, 0.86, 1.0)
		m.arena_env.ambient_light_color = Color(1.0, 0.97, 1.0)
		m.arena_env.ambient_light_energy = 0.9   # 1.35 clipped the pale track past ACES white (Android blowout)
	if mode == "chase":
		if m.beans_t >= 0.0:
			m.show_msg(fr["fname"], "BEANS POWER! Now catch that speedy penguin! GO GO GO!")
		else:
			m.show_msg(fr["fname"], "Race the baby penguin! Careful — he's SO speedy!")
			# non-reader breadcrumb to the beans: Roshan thinks out loud
			m.get_tree().create_timer(3.6).timeout.connect(func():
				if m.game == "slide" and String(m.g.get("mode", "")) == "chase" and m.beans_t < 0.0:
					m.show_msg("Roshan", "I sure am hungry... I bet I'd be faster after a good MEAL!", "hungry"))
	else:
		m.show_msg(fr["fname"], "Whooosh down the ice! Lean LEFT and RIGHT to grab all 5 fish!")

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m._tick_chains(delta, ppos)
	if m.g.has("mover_node"):
		var mvn: MeshInstance3D = m.g["mover_node"]
		mvn.position = (m.g["mover_base"] as Vector3) + Vector3(sin(float(m.g["t"]) * 0.9) * 6.0, 0, 0)
	# slide ride
	if String(m.g.get("phase", "")) == "slide":
		var path: Array = m.g["slide_path"]
		var st: float = float(m.g.get("slide_t", 0.0)) + delta * 13.0
		m.g["slide_t"] = st
		var total := 0.0
		for i in range(path.size() - 1):
			var seg_len: float = (path[i] as Vector3).distance_to(path[i + 1])
			if st <= total + seg_len:
				m.player.position = (path[i] as Vector3).lerp(path[i + 1], (st - total) / seg_len)
				m.player.vel = Vector3.ZERO
				m.hud_game.text = "WHEEEEE!"
				return
			total += seg_len
		m._sparkle_burst(m.player.position, Color(0.5, 0.85, 1.0))
		if m.chime != null:
			m.chime.play()
		m._end_game(true, fr, "What a SLIDE! Best play place ever!" if m.game == "race" else "")
		return
	var checks: Array = m.g.get("checks", [])
	var done := 0
	var nxt: Dictionary = {}
	for c in checks:
		if c["hit"]:
			done += 1
		elif nxt.is_empty():
			nxt = c
	m.hud_game.text = ("Climb the play place! Sparkles: %d / %d" if m.game == "race" else "Dive the caverns! Sparkles: %d / %d") % [done, checks.size()]
	if nxt.is_empty():
		return
	var node: Node3D = nxt["node"]
	node.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 5.0) * 0.15)
	node.rotate_z(delta * 0.75)
	# Phase 6: the FIRST sparkle must be earned — swim toward it to arm the
	# course. Until armed the magnet is off and checkpoints are inert, so a
	# player who does nothing goes nowhere; one little push starts the ride
	# and the magnet forgiveness carries her from there. Guide sparkles
	# point the way while she idles.
	var cprev: Vector3 = m.g.get("ppos_prev", ppos)
	var cvel: Vector3 = (ppos - cprev) / maxf(delta, 0.001)
	m.g["ppos_prev"] = ppos
	if not bool(m.g.get("armed", false)):
		var to_c: Vector3 = node.position - ppos
		if to_c.length() > 0.5 and cvel.dot(to_c.normalized()) > 2.0:
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
				m.show_msg(String(fr.get("fname", "Play Place")), "Swim to the twinkly sparkle to start!", "hint")
		if not bool(m.g.get("armed", false)):
			return
	var dd2: float = node.position.distance_to(ppos)
	# strong, far-reaching magnet carries a 4yo up the play-place automatically
	if dd2 < 34.0:
		m.player.position = m.player.position.lerp(node.position, minf(0.92, delta * 2.6 * (1.0 - dd2 / 34.0)))
		m.player.vel.y = maxf(m.player.vel.y, 0.0)
	if dd2 < 7.5:
		nxt["hit"] = true
		m._sparkle_burst(node.position, Color(1.0, 0.9, 0.5))
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + float(done) * 0.08
			m.chime.play()
		var kind := String(nxt["kind"])
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
