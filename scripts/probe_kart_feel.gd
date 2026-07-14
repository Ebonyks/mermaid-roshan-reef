extends SceneTree
# KART FEEL TELEMETRY — run headless, no display:
#   $GODOT --headless -s scripts/probe_kart_feel.gd
# Measures the kart engine's handling against kart-class feel gates (KART_FEEL.md):
#   A. assist floor   — a zero-input solo run still finishes (auto-cruise)
#   B. racing line    — an inside-line policy beats an outside-line policy
#   C. skill ceiling  — a drift policy reaches tier >= 2 and beats hands-off
#   D. speed channel  — the camera FOV breathes with speed (range >= 8 deg)
#   E. integration    — full-pack terrain race completes; the X quit restores the world
# Steering is injected through the REAL touch path (touch_ui.stick_vec), so what
# it measures is what a finger gets. Prints FEEL| metric lines; prints FAIL on a
# broken gate so ci.sh / the probes workflow goes red.
var main: Node3D
var _race_place := -99
const SOLO := [{"name": "Roshan", "col": Color(1.0, 0.4, 0.8), "sprite": "res://assets/characters/roshan_sprite.png", "player": true}]

func _init() -> void:
	seed(7)
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame

	var none: Dictionary = await _solo_run("none")
	var outside: Dictionary = await _solo_run("outside")
	var inside: Dictionary = await _solo_run("inside")
	var drift: Dictionary = await _solo_run("drift")

	var t_none: float = float(none["t"])
	var line_adv: float = float(outside["t"]) - float(inside["t"])
	var drift_gain: float = t_none - float(drift["t"])
	print("FEEL|t_none=%.2f t_outside=%.2f t_inside=%.2f t_drift=%.2f" % [t_none, float(outside["t"]), float(inside["t"]), float(drift["t"])])
	print("FEEL|line_advantage=%.2f (outside-inside, target >= 0.8)" % line_adv)
	print("FEEL|drift_gain=%.2f (none-drift, target >= 0.8) tier_max=%d uptime=%.1f" % [drift_gain, int(drift["tier_max"]), float(drift["drift_up"])])
	print("FEEL|fov_range=%.1f (target >= 8)" % float(drift["fov_range"]))
	var ok := true
	if not bool(none["done"]):
		print("FAIL|assist floor broken: zero-input run did not finish"); ok = false
	if line_adv < 0.3:
		print("FAIL|racing line not real: line_advantage %.2f < 0.3" % line_adv); ok = false
	if int(drift["tier_max"]) < 2:
		print("FAIL|drift tiers unreachable: tier_max %d < 2" % int(drift["tier_max"])); ok = false
	if drift_gain < 0.3:
		print("FAIL|drift has no payoff: drift_gain %.2f < 0.3" % drift_gain); ok = false
	if float(drift["fov_range"]) < 8.0:
		print("FAIL|fov does not breathe: range %.1f < 8" % float(drift["fov_range"])); ok = false

	# ---- E: full-pack terrain race through the real glue + X-quit restore ----
	_race_place = -99
	main._start_kart_game(false, "terrain")
	var kg = main.kart_game
	_force_race_start(kg)
	var guard := 0.0
	while main.game == "kart" and guard < 260.0:
		guard += 1.0 / 60.0 * Engine.time_scale
		main.touch_ui.stick_vec = Vector2.ZERO
		await process_frame
	if main.game == "kart":
		print("FAIL|full-pack terrain race never finished"); ok = false
	else:
		print("FEEL|full_pack_race=done game='%s'" % main.game)
	await process_frame
	main._start_kart_game(false, "terrain")
	await process_frame
	main.kart_game._quit_race()
	await process_frame
	await process_frame
	if main.game != "" or not main.player.visible:
		print("FAIL|X quit did not restore the world (game='%s' visible=%s)" % [main.game, main.player.visible]); ok = false
	else:
		print("FEEL|quit_restore=ok")
	print("KARTFEEL|%s" % ("ALL OK" if ok else "SEE FAIL LINES"))
	quit()

func _force_race_start(kg: Node) -> void:
	# replicate the select-confirm path (probe skips the 2x8s pick screens)
	for sn in kg._sel_nodes:
		(sn["slot"] as Node3D).queue_free()
	kg._sel_nodes.clear()
	kg._paint_orbs.clear()
	kg._build_karts("kart", {})
	kg._state = "countdown"
	kg._clock = 0.05
	kg._meter_bg.visible = true

func _steer_for(policy: String, kg: Node) -> float:
	# line policies are proportional controllers to a target lat (a constant
	# push would just grind the rail and measure wall physics, not the line)
	var s: float = float(kg._pl["s"])
	var kap: float = kg._curv_at(s)
	var lat: float = float(kg._pl["lat"])
	var room: float = kg._width_at(kg._eff(s)) - 1.6
	var side := 0.0
	if absf(kap) > 0.004:
		side = -signf(kap)   # inside of the bend
	match policy:
		"inside":
			return clampf((side * room * 0.55 - lat) * 0.35, -0.55, 0.55)   # below the 0.6 drift threshold
		"outside":
			return clampf((-side * room * 0.55 - lat) * 0.35, -0.55, 0.55)
		"drift":   # commit hard into every bend — the drift holds the carve line
			return side * 1.0
	return 0.0

func _solo_run(policy: String) -> Dictionary:
	_race_place = -99
	var kg: Node = load("res://scripts/kart.gd").new()
	main.add_child(kg)
	# bare track: no pickups/strips/pearls/shortcut so the measurement is the
	# HANDLING, not which boosts a line happens to sweep through
	kg.configure({"theme": "rainbow", "ground": "float", "racers": SOLO, "pearl_payout": false,
		"pickups": [], "strips": [], "pearl_rows": [], "ramps": [], "hazards": [], "shortcut": false})
	main.game = "kart"
	kg.start(main, Callable(self, "_on_race_done"))
	_force_race_start(kg)
	var t := 0.0
	var drift_up := 0.0
	var tier_max := 0
	var fov_lo := 999.0
	var fov_hi := 0.0
	while _race_place == -99 and t < 260.0:
		t += 1.0 / 60.0 * Engine.time_scale
		if kg._state == "race":
			main.touch_ui.stick_vec = Vector2(_steer_for(policy, kg), 0)
			if bool(kg._pl.get("drift", false)):
				drift_up += 1.0 / 60.0 * Engine.time_scale
				tier_max = maxi(tier_max, kg._drift_tier(float(kg._pl["drift_t"])))
			fov_lo = minf(fov_lo, kg._cam.fov)
			fov_hi = maxf(fov_hi, kg._cam.fov)
		await process_frame
	main.touch_ui.stick_vec = Vector2.ZERO
	main.game = ""
	main.player.visible = true
	await process_frame
	print("  run[%s]: t=%.2f done=%s drift_up=%.1f tier_max=%d" % [policy, t, _race_place != -99, drift_up, tier_max])
	return {"t": t, "done": _race_place != -99, "drift_up": drift_up, "tier_max": tier_max, "fov_range": fov_hi - fov_lo}

func _on_race_done(place: int) -> void:
	_race_place = place
