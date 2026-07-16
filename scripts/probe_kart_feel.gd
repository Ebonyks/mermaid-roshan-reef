extends SceneTree
# KART FEEL TELEMETRY — run headless, no display:
#   $GODOT --headless -s scripts/probe_kart_feel.gd
# Measures the kart engine's handling against kart-class feel gates (KART_FEEL.md):
#   A. assist floor   — a zero-input solo run still finishes (auto-cruise)
#   B. racing line    — an inside-line policy beats an outside-line policy
#   C. skill ceiling  — a drift policy reaches tier >= 2 and beats hands-off
#   D. speed channel  — the camera FOV breathes with speed (range >= 8 deg)
#   E. integration    — full-pack terrain race completes; the X quit restores the world
#   F. determinism    — strip charge is delta-scaled; jumps keep the kart facing forward
#   G. touch path     — the real touch action edge earns the countdown rocket start
#   H. progress       — any finish commits its sticker before podium; quit banks pearls
#   I. portal safety  — exiting inside the gate cannot relaunch until leave + re-enter
# Steering is injected through the REAL touch path (touch_ui.stick_vec), so what
# it measures is what a finger gets. Prints FEEL| metric lines; prints FAIL on a
# broken gate so ci.sh / the probes workflow goes red.
var main: Node3D
var _race_place := -99
var _normal_save_path := ""
var _probe_save_path := ""
var _save_was_remapped := false
var _fallback_save_artifacts: Dictionary = {}
var _old_custom_user_dir := false
var _old_custom_user_dir_name := ""
const SOLO := [{"name": "Roshan", "col": Color(1.0, 0.4, 0.8), "sprite": "res://assets/characters/roshan_sprite.png", "player": true}]

func _init() -> void:
	seed(7)
	Engine.time_scale = 6.0
	_begin_save_isolation()
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

	# ---- F/G: deterministic interactions + real touch action path ----
	var engine_checks: Dictionary = await _engine_regression_checks()
	if not bool(engine_checks["ok"]):
		ok = false
	var pause_ok: bool = await _pause_persistence_check()
	if not pause_ok:
		ok = false
	var recovery_ok: bool = _generation_recovery_check()
	if not recovery_ok:
		ok = false

	# ---- H: a non-first finish must commit progress before the podium delay ----
	var completion_ok: bool = await _second_place_completion_check()
	if not completion_ok:
		ok = false

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
	# Launch from the actual gate position. Quitting must leave Roshan there but
	# disarm the gate until she has deliberately moved away and returned.
	main.player.position = main.kart_portal_pos
	main._start_kart_game(false, "terrain")
	await process_frame
	var pearls_before_quit: int = int(main.pearl_count)
	var saved_before_quit: int = int(_read_saved_state().get("pearls", -999999))
	main.kart_game._pearls_got = 3
	main.kart_game._quit_race()   # first tap arms the child-safe exit
	main.kart_game._quit_race()   # second tap confirms and tears down
	main.set_process(false)
	await process_frame
	await process_frame
	if main.game != "" or not main.player.visible:
		print("FAIL|X quit did not restore the world (game='%s' visible=%s)" % [main.game, main.player.visible]); ok = false
	else:
		print("FEEL|quit_restore=ok")
	var quit_delta: int = int(main.pearl_count) - pearls_before_quit
	var saved_after_quit: int = int(_read_saved_state().get("pearls", -999999))
	var saved_quit_delta: int = saved_after_quit - saved_before_quit
	print("FEEL|quit_pearl_delta=memory:%d disk:%d (target 3, no placement bonus)" % [quit_delta, saved_quit_delta])
	if quit_delta != 3 or saved_quit_delta != 3 or saved_after_quit != int(main.pearl_count):
		print("FAIL|X quit did not durably bank exactly 3 collected pearls"); ok = false

	# Expire the timer while Roshan remains inside. The gate must stay shut;
	# moving beyond its hysteresis radius and coming back must then open it.
	main.kart_cool = 0.0
	main.player.position = main.kart_portal_pos
	main._process(0.1)
	var stayed_out: bool = main.game != "kart"
	var reentered: bool = false
	if stayed_out:
		main.player.position = main.kart_portal_pos + Vector3(30.0, 0.0, 0.0)
		main._process(0.1)
		main.player.position = main.kart_portal_pos
		main._process(0.1)
		reentered = main.game == "kart"
	print("FEEL|portal_latch=blocked_inside:%s leave_reenter:%s" % [stayed_out, reentered])
	if not stayed_out:
		print("FAIL|kart portal relaunched without Roshan leaving the gate"); ok = false
	if stayed_out and not reentered:
		print("FAIL|kart portal did not rearm after leave + re-enter"); ok = false
	if main.game == "kart" and main.kart_game != null:
		main.kart_game._quit_race()
		main.kart_game._quit_race()
		await process_frame
	main.set_process(true)
	_end_save_isolation()
	print("KARTFEEL|%s" % ("ALL OK" if ok else "SEE FAIL LINES"))
	quit()

func _begin_save_isolation() -> void:
	# Probes run on developer machines as well as CI. Redirect user:// before the
	# main scene loads so no test payout or sticker can touch reef_save.json.
	_old_custom_user_dir = bool(ProjectSettings.get_setting("application/config/use_custom_user_dir", false))
	_old_custom_user_dir_name = String(ProjectSettings.get_setting("application/config/custom_user_dir_name", ""))
	_normal_save_path = ProjectSettings.globalize_path("user://reef_save.json")
	ProjectSettings.set_setting("application/config/use_custom_user_dir", true)
	ProjectSettings.set_setting("application/config/custom_user_dir_name", "mermaid-roshan-reef-kart-probe")
	_probe_save_path = ProjectSettings.globalize_path("user://reef_save.json")
	_save_was_remapped = _probe_save_path != _normal_save_path
	if _save_was_remapped:
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("user://"))
		_remove_save_artifacts(_probe_save_path)
		print("FEEL|save_isolation=redirected")
		return
	# Fallback for platforms that cache the user directory before scripts run.
	# Keep exact in-memory copies of the primary and transactional artifacts.
	for suffix: String in ["", ".tmp0", ".tmp1", ".tmp", ".bak"]:
		var path: String = _normal_save_path + suffix
		if FileAccess.file_exists(path):
			_fallback_save_artifacts[path] = FileAccess.get_file_as_bytes(path)
	print("FEEL|save_isolation=snapshot_restore")

func _end_save_isolation() -> void:
	if _save_was_remapped:
		_remove_save_artifacts(_probe_save_path)
	else:
		_remove_save_artifacts(_normal_save_path)
		for path: String in _fallback_save_artifacts:
			var out: FileAccess = FileAccess.open(path, FileAccess.WRITE)
			if out != null:
				out.store_buffer(_fallback_save_artifacts[path] as PackedByteArray)
				out.close()
	ProjectSettings.set_setting("application/config/use_custom_user_dir", _old_custom_user_dir)
	ProjectSettings.set_setting("application/config/custom_user_dir_name", _old_custom_user_dir_name)

func _remove_save_artifacts(base_path: String) -> void:
	for suffix: String in ["", ".tmp0", ".tmp1", ".tmp", ".bak"]:
		var path: String = base_path + suffix
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)

func _read_saved_state() -> Dictionary:
	var path: String = _probe_save_path if _save_was_remapped else _normal_save_path
	if not FileAccess.file_exists(path):
		return {}
	var f: FileAccess = FileAccess.open(path, FileAccess.READ)
	if f == null:
		return {}
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	return parsed as Dictionary if parsed is Dictionary else {}

func _engine_regression_checks() -> Dictionary:
	var kg: Node = load("res://scripts/kart.gd").new()
	main.add_child(kg)
	kg.configure({"theme": "rainbow", "ground": "float", "racers": SOLO, "pearl_payout": false,
		"pickups": [], "strips": [], "pearl_rows": [], "ramps": [], "hazards": [], "shortcut": false})
	main.game = "kart"
	kg.start(main, Callable(self, "_on_race_done"))
	_force_race_start(kg)
	kg.set_process(false)
	kg._state = "race"
	var k: Dictionary = kg._pl
	var kn: Node3D = k["node"]

	# Hold the kart on one strip for the same simulated second at 30 and 60 Hz.
	kg._strip_data = [{"pos": kn.position, "len": 1.0}]
	k["meter"] = 0.0
	for i in range(30):
		kg._check_strips(1.0 / 30.0)
	var strip_30: float = float(k["meter"])
	k["meter"] = 0.0
	for i in range(60):
		kg._check_strips(1.0 / 60.0)
	var strip_60: float = float(k["meter"])
	var strip_ok: bool = strip_30 > 0.005 and absf(strip_30 - strip_60) <= 0.02
	print("FEEL|strip_charge_1s=30hz:%.3f 60hz:%.3f" % [strip_30, strip_60])
	if not strip_ok:
		print("FAIL|strip charge depends on rendered frames: 30hz %.3f vs 60hz %.3f" % [strip_30, strip_60])

	# At jump apex, the root's visual forward axis must still follow the road.
	k["latv"] = 0.0
	k["drift"] = false
	k["air_t"] = float(kg.AIR_DUR) * 0.5
	kg._place_kart(k, 0.0)
	var expected_forward: Vector3 = kg._kart_frame(float(k["s"]), float(k["lat"]))[1]
	var visual_forward: Vector3 = -kn.global_transform.basis.z.normalized()
	var air_align: float = visual_forward.dot(expected_forward.normalized())
	var air_ok: bool = air_align >= 0.85
	print("FEEL|air_forward_alignment=%.3f (target >= 0.85)" % air_align)
	if not air_ok:
		print("FAIL|airborne kart points away from track tangent: alignment %.3f" % air_align)

	# Use TouchUI's one-shot action state, exactly as a released screen tap does.
	k["boost_t"] = 0.0
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_just = true
	kg._fire_prev = false
	kg._state = "countdown"
	kg._clock = 0.001
	kg._process(0.01)
	var rocket_boost: float = float(k["boost_t"])
	var rocket_ok: bool = rocket_boost >= 0.8
	print("FEEL|touch_countdown_rocket=%.2f (target >= 0.8)" % rocket_boost)
	if not rocket_ok:
		print("FAIL|touch action at GO did not trigger the rocket start")
	main.touch_ui.action_just = false

	kg._teardown(-1)
	await process_frame
	main.game = ""
	main.player.visible = true
	return {"ok": strip_ok and air_ok and rocket_ok}

func _pause_persistence_check() -> bool:
	var kg: Node = load("res://scripts/kart.gd").new()
	main.add_child(kg)
	kg.configure({"theme": "ocean", "ground": "float", "racers": SOLO, "pearl_payout": true,
		"pickups": [], "strips": [], "pearl_rows": [], "ramps": [], "hazards": [], "shortcut": false})
	main.game = "kart"
	kg.start(main, Callable(self, "_on_race_done"))
	_force_race_start(kg)
	kg.set_process(false)
	var pearls_before: int = int(main.pearl_count)
	kg._pearls_got = 2
	kg._notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
	var pearls_after_first: int = int(main.pearl_count)
	var disk_after_first: int = int(_read_saved_state().get("pearls", -999999))
	kg._notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
	var pearls_after_second: int = int(main.pearl_count)
	var disk_after_second: int = int(_read_saved_state().get("pearls", -999999))
	var passed: bool = pearls_after_first - pearls_before == 2 \
		and pearls_after_second == pearls_after_first \
		and disk_after_first == pearls_after_first \
		and disk_after_second == pearls_after_second
	print("FEEL|pause_bank=memory:%d disk:%d repeat:%d" % [pearls_after_first - pearls_before, disk_after_first - pearls_before, pearls_after_second - pearls_before])
	if not passed:
		print("FAIL|application pause did not durably and idempotently bank collected pearls")
	kg._teardown(-1)
	await process_frame
	main.game = ""
	main.player.visible = true
	return passed

func _generation_recovery_check() -> bool:
	# A power loss can leave a fully flushed, newer temp beside an older valid
	# primary. Recovery must compare generations instead of blindly trusting the
	# primary merely because its JSON still parses.
	var path: String = _probe_save_path if _save_was_remapped else _normal_save_path
	var newer: Dictionary = _read_saved_state().duplicate(true)
	var generation: int = int(newer.get("save_generation", 0)) + 1
	newer["save_generation"] = generation
	newer["kart_probe_newer"] = true
	var stage_path: String = path + (".tmp%d" % (generation & 1))
	var temp: FileAccess = FileAccess.open(stage_path, FileAccess.WRITE)
	if temp == null:
		print("FAIL|could not stage generation recovery check")
		return false
	temp.store_string(JSON.stringify(newer))
	temp.flush()
	var staged: bool = temp.get_error() == OK
	temp.close()
	var recovered: Variant = main._save_state._recover_save_if_needed() if staged else null
	var promoted: Dictionary = _read_saved_state()
	var passed: bool = recovered is Dictionary \
		and bool((recovered as Dictionary).get("kart_probe_newer", false)) \
		and bool(promoted.get("kart_probe_newer", false)) \
		and int(promoted.get("save_generation", -1)) == generation
	print("FEEL|save_generation_recovery=%s generation:%d" % [passed, generation])
	if not passed:
		print("FAIL|newer flushed kart save did not replace the older valid primary")
	main.save_generation = generation
	return passed

func _second_place_completion_check() -> bool:
	main.stickers.erase("racer")
	main.galaxy_unlocked = false
	main._start_kart_game(false, "float")
	var kg: Node = main.kart_game
	_force_race_start(kg)
	kg.set_process(false)
	kg._state = "race"
	kg._pl["s"] = 10.0
	var rival_ahead := false
	for k in kg._karts:
		if not bool(k["is_player"]) and not rival_ahead:
			k["s"] = 20.0
			rival_ahead = true
		elif not bool(k["is_player"]):
			k["s"] = 0.0
	var place: int = int(kg._placement())
	kg._finish()
	var before_podium: bool = main.game == "kart" and main.kart_game == kg
	var sticker_committed: bool = bool(main.stickers.get("racer", false))
	var galaxy_committed: bool = bool(main.galaxy_unlocked)
	var persisted: Dictionary = _read_saved_state()
	var persisted_stickers: Variant = persisted.get("stickers", {})
	var sticker_saved: bool = persisted_stickers is Dictionary and bool((persisted_stickers as Dictionary).get("racer", false))
	var galaxy_saved: bool = bool(persisted.get("galaxy", false))
	var passed: bool = place == 2 and before_podium and sticker_committed and galaxy_committed and sticker_saved and galaxy_saved
	print("FEEL|second_place_commit=place:%d memory:%s/%s disk:%s/%s before_podium:%s" % [place, sticker_committed, galaxy_committed, sticker_saved, galaxy_saved, before_podium])
	if not passed:
		print("FAIL|second-place completion did not commit racer/Galaxy progress before podium")
	# Use the quit callback only to avoid launching the much larger Galaxy scene;
	# the assertions above happen after the real finish transaction has completed.
	kg._teardown(-1)
	await process_frame
	return passed

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
	var guard := 0.0
	var race_elapsed := 0.0
	var drift_up := 0.0
	var tier_max := 0
	var fov_lo := 999.0
	var fov_hi := 0.0
	while _race_place == -99 and guard < 260.0:
		guard += 1.0 / 60.0 * Engine.time_scale
		if kg._state == "race":
			var race_now: float = float(kg._race_t)
			var race_delta: float = maxf(0.0, race_now - race_elapsed)
			race_elapsed = race_now
			main.touch_ui.stick_vec = Vector2(_steer_for(policy, kg), 0)
			if bool(kg._pl.get("drift", false)):
				drift_up += race_delta
				tier_max = maxi(tier_max, kg._drift_tier(float(kg._pl["drift_t"])))
			fov_lo = minf(fov_lo, kg._cam.fov)
			fov_hi = maxf(fov_hi, kg._cam.fov)
		await process_frame
	main.touch_ui.stick_vec = Vector2.ZERO
	main.game = ""
	main.player.visible = true
	await process_frame
	print("  run[%s]: t=%.2f done=%s drift_up=%.1f tier_max=%d" % [policy, race_elapsed, _race_place != -99, drift_up, tier_max])
	return {"t": race_elapsed, "done": _race_place != -99, "drift_up": drift_up, "tier_max": tier_max, "fov_range": fov_hi - fov_lo}

func _on_race_done(place: int) -> void:
	_race_place = place
