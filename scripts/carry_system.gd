class_name CarrySystem
extends RefCounted
# Overworld grab / carry / throw (ZELDA_GAMEPLAY_WORKORDER E1) plus singing-
# shell throw targets (E3, v1). Two plush starfish live in the reef: swim
# close and press ACTION to scoop one up, press again to toss it. A toss that
# lands on a singing shell rings a chime arpeggio, bursts sparkles and pops
# out a pearl. Everything is analytic (a ReefPhysics free_medium-style
# projectile) — no engine bodies, nothing here gates progress, and
# probe_passive stays silent because the system only reacts to ACTION.

const PICK_R := 6.5        # scoop reach
const CARRY_FWD := 2.6     # the held star floats here, in front of her hands
const CARRY_UP := 2.4
const THROW_FWD := 26.0
const THROW_UP := 9.0
const GRAV := 9.5          # free_medium(9.5): the fetch-ball feel
const DRAG := 0.55         # velocity retained per second underwater
const SHELL_R := 5.0       # generous no-fail hit window
const SING_COOL := 6.0

var m: ReefMain
var stars: Array = []      # {node, state: idle|held|fly, vel, seat, spin, fly_t}
var shells: Array = []     # {node, mouth, sing_t, note_i, cool, halo}
var act_prev := false
var hinted := false

func _init(main: ReefMain) -> void:
	m = main
	_build()

func _build() -> void:
	for sp in [Vector3(20.0, 0.0, 14.0), Vector3(-16.0, 0.0, -22.0)]:
		var y: float = ReefMain.seabed_y(sp.x, sp.z) + 0.4
		var n: Node3D = m._gen2_prop("starfish", Vector3(sp.x, y, sp.z), 2.6, randf() * TAU, 0.0)
		if n == null:
			continue
		stars.append({"node": n, "state": "idle", "vel": Vector3.ZERO,
			"seat": Vector3(sp.x, y, sp.z), "spin": randf() * TAU, "fly_t": 0.0,
			"aim": -1})
	for sp in [Vector3(34.0, 0.0, -6.0), Vector3(-28.0, 0.0, 20.0)]:
		var y: float = ReefMain.seabed_y(sp.x, sp.z) + 0.1
		var n: Node3D = m._gen2_prop("spiralshell", Vector3(sp.x, y, sp.z), 4.6, randf() * TAU, 0.05)
		if n == null:
			continue
		# soft lavender pool = the "throw here" pointer (no new OmniLights)
		var halo: MeshInstance3D = m._halo(Vector3(sp.x, y + 0.4, sp.z), Color(0.75, 0.7, 1.0), 9.0)
		shells.append({"node": n, "mouth": Vector3(sp.x, y + 2.2, sp.z),
			"sing_t": -1.0, "note_i": 0, "cool": 0.0, "halo": halo})

func is_carrying() -> bool:
	for s in stars:
		if String(s["state"]) == "held":
			return true
	return false

func tick(delta: float, ppos: Vector3) -> void:
	# ACTION edge — overlays and minigames own the button while they are up
	var blocked: bool = m.get("wardrobe_layer") != null \
		or m.get("stickers_layer") != null or m.get("craft_layer") != null \
		or m.get("collection_layer") != null or m.intro_active
	var mgv: Variant = m.get("mg_kind")
	if mgv != null and String(mgv) != "":
		blocked = true
	var act: bool = Input.is_physical_key_pressed(KEY_SPACE)
	if m.has_method("joy_pressed"):
		act = act or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	if m.touch_ui != null and m.touch_ui.action_down:
		act = true
	if act and not act_prev and not blocked:
		_action(ppos)
	act_prev = act

	for s in stars:
		var n: Node3D = s["node"]
		s["spin"] = float(s["spin"]) + delta
		match String(s["state"]):
			"idle":
				var seat: Vector3 = s["seat"]
				n.position.y = seat.y + 0.35 + sin(float(s["spin"]) * 1.7) * 0.22
				n.rotation.y += delta * 0.5
			"held":
				var pl: Node3D = m.player
				var yawv: float = float(pl.yaw)
				var carry_pt: Vector3 = pl.position \
					+ Vector3(sin(yawv), 0.0, cos(yawv)) * CARRY_FWD \
					+ Vector3(0.0, CARRY_UP + sin(float(s["spin"]) * 3.0) * 0.12, 0.0)
				n.position = n.position.lerp(carry_pt, 1.0 - pow(0.0005, delta))
				n.rotation.y += delta * 2.0
			"fly":
				s["fly_t"] = float(s["fly_t"]) + delta
				var v: Vector3 = s["vel"]
				v.y -= GRAV * delta
				v *= pow(DRAG, delta)
				# aim assist: a toss roughly at a shell curves into its mouth —
				# a four-year-old's "at" is the whole point of the toy
				var ai: int = int(s.get("aim", -1))
				if ai >= 0:
					var mouth: Vector3 = shells[ai]["mouth"]
					var to_t: Vector3 = mouth - n.position
					if to_t.length() < 0.8 or v.dot(to_t) <= 0.0:
						s["aim"] = -1   # arrived or flew past — stop steering
					else:
						var vlen: float = v.length()
						if vlen > 0.5:
							v = (v / vlen).slerp(to_t.normalized(), 1.0 - pow(0.2, delta)) * vlen
				n.position += v * delta
				n.rotation.y += delta * 7.0
				if n.position.y > ReefMain.WATER_TOP - 0.5:
					n.position.y = ReefMain.WATER_TOP - 0.5
					v.y = minf(0.0, v.y)
				var dxz: float = Vector2(n.position.x, n.position.z).length()
				if dxz > ReefMain.WORLD_R:
					n.position.x *= ReefMain.WORLD_R / dxz
					n.position.z *= ReefMain.WORLD_R / dxz
				var fl: float = ReefMain.seabed_y(n.position.x, n.position.z) + 1.0
				if n.position.y < fl:
					n.position.y = fl
					if v.length() < 3.5 or float(s["fly_t"]) > 6.0:
						s["state"] = "idle"
						s["seat"] = Vector3(n.position.x, fl - 0.6, n.position.z)
					else:
						v.y = -v.y * 0.45
						v.x *= 0.7
						v.z *= 0.7
						m._sparkle_burst(n.position, Color(0.8, 0.95, 1.0))
				s["vel"] = v
				for sh in shells:
					if float(sh["cool"]) <= 0.0 and n.position.distance_to(sh["mouth"]) < SHELL_R:
						_sing(sh)
						s["vel"] = (n.position - (sh["mouth"] as Vector3)).normalized() * 8.0 + Vector3(0, 4.0, 0)

	for sh in shells:
		sh["cool"] = maxf(0.0, float(sh["cool"]) - delta)
		if float(sh["sing_t"]) >= 0.0:
			sh["sing_t"] = float(sh["sing_t"]) + delta
			var want_i: int = int(float(sh["sing_t"]) / 0.16)
			if want_i > int(sh["note_i"]) and want_i <= 4:
				sh["note_i"] = want_i
				if m.chime != null:
					m.chime.pitch_scale = 0.9 * pow(2.0, float(ReefMain.PENT[(want_i * 2) % 7]) / 12.0)
					m.chime.play()
			# squash-and-stretch while it sings
			var pn: Node3D = sh["node"]
			var pulse: float = maxf(0.0, 1.0 - float(sh["sing_t"]) / 0.8)
			pn.scale = Vector3.ONE * (1.0 + sin(float(sh["sing_t"]) * 18.0) * 0.08 * pulse)
			if float(sh["sing_t"]) > 1.2:
				sh["sing_t"] = -1.0
				pn.scale = Vector3.ONE

func _action(ppos: Vector3) -> void:
	# throw if holding, otherwise scoop the nearest idle star within reach
	for s in stars:
		if String(s["state"]) == "held":
			_throw(s)
			return
	var best: Dictionary = {}
	var best_d: float = PICK_R
	for s in stars:
		if String(s["state"]) != "idle":
			continue
		var d: float = (s["node"] as Node3D).position.distance_to(ppos)
		if d < best_d:
			best_d = d
			best = s
	if best.is_empty():
		return
	best["state"] = "held"
	if m.player != null:
		# this press was a scoop, not a jump (main ticks before the player)
		m.player.jump_cool = maxf(float(m.player.jump_cool), 0.5)
		m.player.play_verb("collect")
	m._sparkle_burst((best["node"] as Node3D).position, Color(1.0, 0.9, 0.7))
	if not hinted:
		hinted = true
		m._say("roshan", "")   # her delighted generic line, first scoop only

func _throw(s: Dictionary) -> void:
	var pl: Node3D = m.player
	if pl == null:
		return
	var yawv: float = float(pl.yaw)
	s["state"] = "fly"
	s["fly_t"] = 0.0
	s["vel"] = Vector3(sin(yawv), 0.0, cos(yawv)) * THROW_FWD \
		+ Vector3(0.0, THROW_UP, 0.0) + (pl.vel as Vector3) * 0.6
	# lock aim assist onto a shell the throw is roughly facing
	s["aim"] = -1
	var pos0: Vector3 = (s["node"] as Node3D).position
	var vdir: Vector3 = (s["vel"] as Vector3).normalized()
	var best_dot: float = 0.7
	for i in range(shells.size()):
		var to_s: Vector3 = (shells[i]["mouth"] as Vector3) - pos0
		var d: float = to_s.length()
		if d < 1.0 or d > 34.0:
			continue
		var facing: float = vdir.dot(to_s / d)
		if facing > best_dot:
			best_dot = facing
			s["aim"] = i
	pl.jump_cool = maxf(float(pl.jump_cool), 0.5)

func _sing(sh: Dictionary) -> void:
	sh["sing_t"] = 0.0
	sh["note_i"] = 0
	sh["cool"] = SING_COOL
	m.pearl_count += 1
	m._update_hud()
	m._sparkle_burst(sh["mouth"], Color(0.8, 0.75, 1.0))
	m._say("roshan", ["pearl", "pearl2", "pearl3"][randi() % 3], 3.0)
