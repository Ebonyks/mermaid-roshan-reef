extends SceneTree
# Dust Bunny Boss probe: the boss AI contract (DUST_BUNNY_BOSS_2026-08-02.md).
# The showing runs before the fight; taps land damage ONLY while he is
# airborne with his star flashing, one hit per window; hit 1 turns him dizzy
# (slower), hit 2 turns him angry (faster), hit 3 ends the fight as friends;
# a window that closes unhit is not a failure. Five consecutive misses switch
# on the slower assist pace. A landed round resets that streak but keeps the
# earned pace for the encounter. Every hit here comes from a real tap edge on
# touch_ui, so nothing in this file can win the fight without input.
# Frame pacing differs per machine, so every wait here is on a CONDITION.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260802)
	Engine.time_scale = 3.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	_prepare_day_one_terminal_boundary()
	await _open_case()
	if main.game == "dustboss":
		await _splash_case()
		await _framing_case()
		await _showing_case()
		await _mastery_ui_case()
		await _dodge_case()
		await _shield_case()
		await _bump_case()
		await _first_hit_case()
		await _second_hit_case()
		await _mercy_case()
		await _win_case()
	await _pose_replay_case()
	print("DUSTBOSS|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("DUSTBOSS|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _event_count(history: Array[Dictionary], event_name: String) -> int:
	var count := 0
	for record: Dictionary in history:
		if String(record.get("event", "")) == event_name:
			count += 1
	return count


func _prepare_day_one_terminal_boundary() -> void:
	# Enter through the legacy physical attic portal below, but make its story
	# state match the real first-run route: every room is complete and the boss
	# door has already fired its one-shot trigger. The live DustBoss ending then
	# owns the terminal director/main seam; this fixture never calls completion.
	var director: DayOneDirector = main._day_one_ref()
	# The rendered probe uses the normal user:// save path. Reset only the two
	# story directors so a developer's already-complete save cannot turn this
	# first-win integration case into a rematch.
	director.restore_state({})
	main._chapter_two_ref().restore_state({})
	director.bathroom_tools_authorized = true
	director.bathroom_supply_hunt_step = 2
	director.bathroom_cleanup_step = 2
	director.complete_tutorial("bathroom")
	director.complete_placeholder("pool", "pool_activity")
	director.complete_activity("stuffie", "stuffie_activity")
	director.complete_activity("art", "art_activity")
	director.giant_dust_bunny_boss_triggered = true
	_ck("the full boss case starts at the valid Day-One terminal boundary",
		director.day_one_active and director.boss_door_glow
		and director.giant_dust_bunny_boss_triggered
		and not director.giant_dust_bunny_boss_defeated)

func _boss() -> DustBossGame:
	return main._game_obj("dustboss", DustBossGame) as DustBossGame

func _state() -> String:
	return String(main.g.get("db_state", ""))

func _hits() -> int:
	return int(main.g.get("db_hits", 0))

func _await_state(want: String, cap: int) -> bool:
	var n := 0
	while n < cap:
		if main.game != "dustboss":
			return false
		if _state() == want:
			return true
		n += 1
		await process_frame
	return false

func _await_airborne(cap: int) -> bool:
	# airborne AND the kit has opened its own vulnerability window
	var n := 0
	while n < cap:
		if main.game != "dustboss" or _state() != "vuln":
			return false
		var k: DustBunnyBossSprite = main.g.get("db_kit") as DustBunnyBossSprite
		if float(main.g.get("db_y", 0.0)) > 2.0 and k != null and k.vulnerable:
			return true
		n += 1
		await process_frame
	return false

func _await_helper_taps(expected: int, cap: int) -> bool:
	# Wait for the gameplay-owned insertion, not just the first airborne frame:
	# the kit may finish opening on a later process tick than the boss state.
	var n := 0
	while n < cap:
		if main.game != "dustboss":
			return false
		if int(main.g.get("db_helper_taps_total", 0)) >= expected:
			return true
		n += 1
		await process_frame
	return false

func _park(x: float, z: float) -> void:
	# stand Roshan at a ring-local spot; OctagonStage.tick reads her live
	# position, so this is placement only — it can never stand in for the tap
	var r: Node3D = main.g.get("oc_root") as Node3D
	if r == null:
		return
	main.player.position = r.position + Vector3(x, 3.0, z)
	main.player.vel = Vector3.ZERO

func _player_local() -> Vector2:
	var r: Node3D = main.g.get("oc_root") as Node3D
	if r == null:
		return Vector2.ZERO
	return Vector2(main.player.position.x - r.position.x,
		main.player.position.z - r.position.z)

func _park_on_boss() -> void:
	_park(float(main.g.get("db_x", 0.0)), float(main.g.get("db_z", 0.0)))

func _tap() -> void:
	# a real fresh tap edge through the virtual hand: release, press, release
	main.touch_ui.action_down = false
	await process_frame
	main.touch_ui.action_down = true
	await process_frame
	main.touch_ui.action_down = false
	await process_frame

func _strike(max_windows: int) -> bool:
	# A round is THREE QUICK TAPS inside one window (the owner's 2026-07-29
	# contract, owned by DustBunnyBossSprite). Wait for a flashing window,
	# stand under him, and drum. A window that closes short costs a retry,
	# never the run — exactly what a small player's slow hand costs.
	var want: int = _hits() + 1
	for w in range(max_windows):
		if main.game != "dustboss":
			return false
		if _state() != "vuln":
			var opened: bool = await _await_state("vuln", 4000)
			if not opened:
				return false
		var up: bool = await _await_airborne(600)
		if not up:
			continue
		_park_on_boss()
		var guard := 0
		while guard < 400 and main.game == "dustboss" and _hits() < want:
			# a real drum on the virtual hand: press, release, press...
			main.touch_ui.action_down = (guard % 2) == 0
			guard += 1
			await process_frame
			if _state() != "vuln" and _hits() < want:
				break
		main.touch_ui.action_down = false
		if _hits() >= want:
			return true
	return false

# ---- the attic opens -------------------------------------------------------
func _open_case() -> void:
	await _frames(10)
	_ck("attic portal exists in the reef", main.dust_boss_portal_pos != Vector3.ZERO)
	main.dust_boss_cool = 0.0
	var wait := 0
	while main.game == "" and wait < 900:
		wait += 1
		main.player.position = main.dust_boss_portal_pos + Vector3(0, 2, 3)
		main.player.vel = Vector3.ZERO
		if main.touch_uses_explicit_interactions():
			main._activate_touch_interactable("reef:dustboss")
		await process_frame
	_ck("swimming to the attic door opens the boss fight", main.game == "dustboss")

# ---- the camera contract ---------------------------------------------------
func _framing_case() -> void:
	# THE FRAMING IS PART OF THE FIGHT. The 2026-08-02 stress test shipped a
	# boss whose whole tell was cropped off the top of the phone and whose
	# player was 255px below the bottom, with every behavioural probe green.
	# These checks make that impossible to repeat: the ring, the child and the
	# apex of a leap with its icon must all project inside the 1280x720 canvas.
	var cam: Camera3D = main.player.cam
	var r: Node3D = main.g.get("oc_root") as Node3D
	_ck("the arena owns the camera", cam != null and r != null)
	if cam == null or r == null:
		return
	var vp: Vector2 = cam.get_viewport().get_visible_rect().size
	var apo: float = OctagonStage.apothem(DustBossGame.RADIUS)
	var near_p: Vector2 = cam.unproject_position(r.position + Vector3(0, 4.5, apo))
	var far_p: Vector2 = cam.unproject_position(r.position + Vector3(0, 4.5, -apo))
	var apex: Vector2 = cam.unproject_position(r.position
		+ Vector3(0, DustBossGame.LEAP_H + DustBossGame.BOSS_H + 3.5, 0))
	_ck("the near rim of the ring is on screen", near_p.y < vp.y and near_p.y > 0.0)
	_ck("the far rim of the ring is on screen", far_p.y > 0.0 and far_p.y < vp.y)
	_ck("the top of a leap and its icon are on screen", apex.y > 0.0 and apex.y < vp.y)
	var her: Vector2 = cam.unproject_position(main.player.global_position + Vector3(0, 3.0, 0))
	_ck("Roshan herself is on screen at the start of the fight",
		her.x > 0.0 and her.x < vp.x and her.y > 0.0 and her.y < vp.y)
	# and the arena must KEEP the lens: player.gd hands the camera to a stage
	# by game id, so a mode missing from that list silently loses it
	var before: Vector3 = cam.position
	await _frames(20)
	_ck("the arena keeps the camera while the fight runs",
		cam.position.distance_to(before) < 1.0)


# ---- the reusable boss splash ---------------------------------------------
func _splash_case() -> void:
	_ck("the fight opens on the reusable boss splash", _state() == "splash")
	var splash: BossSplash2D = main.g.get("db_splash") as BossSplash2D
	_ck("the splash is a true-2D input-blocking canvas",
		splash != null
		and splash.get_node_or_null("BossSplashRoot") is Control
		and splash.get_node_or_null(
			"BossSplashRoot/BossSplashStage/BossSplashCharacterAnchor/BossSplashCharacter") \
			is AnimatedSprite2D)
	if splash != null:
		_ck("the splash begins with Grand Puff's jump", splash.current_beat() == "jump")
		var saw_grin := false
		var saw_flash := false
		var guard := 0
		while main.game == "dustboss" and _state() == "splash" and guard < 1200:
			if splash != null and is_instance_valid(splash):
				saw_grin = saw_grin or splash.current_beat() == "grin"
				saw_flash = saw_flash or splash.current_beat() == "flash"
			guard += 1
			await process_frame
		_ck("the splash shows the grin before the vulnerability flash",
			saw_grin and saw_flash)
	_ck("the splash hands off to the safe teaching beat", _state() == "showing")

# ---- the art contract ------------------------------------------------------
func _pose_case() -> void:
	# The boss draws one pose PER BEAT (BOSS_ART_INTEGRATION_2026-08-02.md).
	# Every pose is optional and falls back to the placeholder card, so this
	# asserts the MAP, not the files — it stays green before the art lands and
	# catches a beat wired to the wrong drawing after it does. Sampled EVERY
	# frame, because the interesting poses (wind-up, open) last under a second.
	var boss := _boss()
	var seen: Dictionary = {}
	for key: String in ["idle", "jump", "laugh_vulnerable", "flinch_3",
			"angry_jump_final", "implode"]:
		seen[key] = false
	_ck("every beat maps to a named pose", boss.pose_for_state() != "")
	var guard := 0
	while main.game == "dustboss" and guard < 20000:
		var pose: String = boss.pose_for_state()
		if seen.has(pose):
			seen[pose] = true
		# land the three hits as they come, without skipping past any beat
		var kk: DustBunnyBossSprite = main.g.get("db_kit") as DustBunnyBossSprite
		if _state() == "vuln" and kk != null and kk.vulnerable:
			_park_on_boss()
			main.touch_ui.action_down = (guard % 2) == 0
		else:
			main.touch_ui.action_down = false
		guard += 1
		await process_frame
	main.touch_ui.action_down = false
	var used: Array[String] = []
	var unused: Array[String] = []
	for key: String in seen.keys():
		if bool(seen[key]):
			used.append(key)
		else:
			unused.append(key)
	_ck("the fight plays jump, the vulnerable laugh, the flinch and the final jump",
		bool(seen.get("jump", false)) and bool(seen.get("laugh_vulnerable", false))
		and bool(seen.get("flinch_3", false)) and bool(seen.get("angry_jump_final", false)))
	_ck("the befriending beat is the authored implosion", bool(seen.get("implode", false)))
	print("DUSTBOSS|poses used: ", ", ".join(used), " | not reached in this run: ",
		", ".join(unused))

# ---- the showing -----------------------------------------------------------
func _showing_case() -> void:
	_ck("the fight opens with the showing, not the fight", _state() == "showing")
	_ck("the boss cutout and its head star are built",
		main.g.get("db_boss") != null and main.g.get("db_star") != null)
	# taps during the reveal teach nothing bad: they cannot scratch him
	for i in range(4):
		await _tap()
	_ck("taps during the showing land no damage", _hits() == 0)
	# and they must not be counted against her medal, nor scold her over the
	# teaching line — the showing is where the rule is taught
	_ck("taps during the showing cost her no medal tier",
		int(main.g.get("db_wasted", 0)) == 0)
	# The shared action label must say what it does; swipe remains world input.
	var boss0 := _boss()
	_ck("the shared action label reads WAIT while he is shut",
		boss0.action_label() == "WAIT")
	var reached: bool = await _await_state("prowl", 3000)
	_ck("the showing hands over to the prowl", reached)

# ---- shielded: he is a ball of dust ---------------------------------------
func _shield_case() -> void:
	var before: int = int(main.g.get("db_shield_taps", 0))
	var feedback_before: int = int(main.g.get("db_shield_feedbacks", 0))
	for i in range(4):
		_park_on_boss()
		await _tap()
	_ck("taps while he bounces around land no damage", _hits() == 0)
	_ck("a shielded tap still answers with a poof",
		int(main.g.get("db_shield_taps", 0)) > before)
	_ck("shield feedback is strong but rate-limited",
		int(main.g.get("db_shield_feedbacks", 0)) - feedback_before >= 1
		and int(main.g.get("db_shield_feedbacks", 0)) - feedback_before <= 2)
	var windup: bool = await _await_state("windup", 3000)
	_ck("the prowl telegraphs the leap with a wind-up", windup)

# ---- optional mastery: picture-first, partial, and always replayable -------
func _mastery_ui_case() -> void:
	var layer: CanvasLayer = main.g.get("db_mastery_layer") as CanvasLayer
	var stars: Label = main.g.get("db_mastery_stars") as Label
	var gem: Label = main.g.get("db_perfect_gem") as Label
	_ck("the fight shows three earned-or-empty mastery stars without reading",
		layer != null and stars != null and stars.text == "★★★")
	_ck("the clean-run bonus has its own visible diamond target",
		gem != null and gem.text == "💎")
	_ck("dodge adds no separate UI button or pointer",
		main.g.get("db_dodge_button") == null
		and main.g.get("db_dodge_pointer") == null)
	_ck("bump mastery maps 0/1 to gold, 2 to silver, and 3+ to bronze",
		DustBossGame.mastery_tier_for_bumps(0) == 3
		and DustBossGame.mastery_tier_for_bumps(1) == 3
		and DustBossGame.mastery_tier_for_bumps(2) == 2
		and DustBossGame.mastery_tier_for_bumps(3) == 1
		and DustBossGame.mastery_tier_for_bumps(9) == 1)
	main.g["db_bumps"] = 2
	_boss()._update_mastery_ui()
	var silver_read: bool = stars != null and stars.text == "★★☆" \
		and gem != null and gem.text == "◇"
	main.g["db_bumps"] = 3
	_boss()._update_mastery_ui()
	var bronze_read: bool = stars != null and stars.text == "★☆☆"
	main.g["db_bumps"] = 0
	_boss()._update_mastery_ui()
	_ck("missing stars stay outlined so the higher mastery remains visible",
		silver_read and bronze_read)

# ---- optional dodge: contact becomes a twirl, never a hidden fail state ----
func _dodge_case() -> void:
	var boss := _boss()
	_ck("incoming attacks provide at least the established 2.2 second reaction",
		DustBossGame.dodge_hop_gap(0.46, true) == DustBossGame.DODGE_ATTACK_MIN_T
		and DustBossGame.dodge_hop_gap(0.46, false) == 0.46
		and DustBossGame.DODGE_ATTACK_MIN_T
			* (1.0 - DustBossGame.DODGE_FLASH_START_U) >= 2.2)
	var gap: float = DustBossGame.DODGE_ATTACK_MIN_T
	_ck("the flash begins on the authored committed beat and closes at landing",
		not DustBossGame.dodge_window_for_hop(gap * 0.249, gap, true)
		and DustBossGame.dodge_window_for_hop(gap * 0.25, gap, true)
		and DustBossGame.dodge_window_for_hop(gap - 0.001, gap, true)
		and not DustBossGame.dodge_window_for_hop(gap, gap, true)
		and not DustBossGame.dodge_window_for_hop(gap * 0.5, gap, false))
	_ck("contact cannot resolve before the child has seen the cue",
		DustBossGame.DODGE_CONTACT_START_U > DustBossGame.DODGE_FLASH_START_U
		and gap * (DustBossGame.DODGE_CONTACT_START_U
			- DustBossGame.DODGE_FLASH_START_U) >= 1.7)
	_ck("swipe boundaries accept both directions and reject non-horizontal motion",
		DustBossGame.dodge_swipe_direction(Vector2.ZERO,
			Vector2(DustBossGame.DODGE_SWIPE_MIN_PX, 0.0)) == 1.0
		and DustBossGame.dodge_swipe_direction(Vector2.ZERO,
			Vector2(-DustBossGame.DODGE_SWIPE_MIN_PX, 0.0)) == -1.0
		and DustBossGame.dodge_swipe_direction(Vector2.ZERO,
			Vector2(53.99, 0.0)) == 0.0
		and DustBossGame.dodge_swipe_direction(Vector2.ZERO,
			Vector2(90.0, 60.0)) != 0.0
		and DustBossGame.dodge_swipe_direction(Vector2.ZERO,
			Vector2(89.99, 60.0)) == 0.0)
	var rng := RandomNumberGenerator.new()
	rng.seed = 20260831
	var classifications_ok := true
	for _i in range(4096):
		var dx: float = rng.randf_range(-240.0, 240.0)
		var dy: float = rng.randf_range(-180.0, 180.0)
		var expected: float = 0.0
		if absf(dx) >= DustBossGame.DODGE_SWIPE_MIN_PX \
				and absf(dx) >= absf(dy) * DustBossGame.DODGE_HORIZONTAL_DOMINANCE:
			expected = 1.0 if dx > 0.0 else -1.0
		if DustBossGame.dodge_swipe_direction(Vector2.ZERO,
				Vector2(dx, dy)) != expected:
			classifications_ok = false
			break
	_ck("4096 seeded gesture classifications match the exact contract",
		classifications_ok)
	var easing_ok := true
	for hz in [20, 30, 60, 120]:
		var elapsed := 0.0
		var integrated := 0.0
		var step: float = 1.0 / float(hz)
		while elapsed < DustBossGame.DODGE_MOVE_T:
			var next_t: float = minf(DustBossGame.DODGE_MOVE_T, elapsed + step)
			integrated += DustBossGame.dodge_ease(
				next_t / DustBossGame.DODGE_MOVE_T) - DustBossGame.dodge_ease(
				elapsed / DustBossGame.DODGE_MOVE_T)
			elapsed = next_t
		if not is_finite(integrated) or not is_equal_approx(integrated, 1.0):
			easing_ok = false
	_ck("dodge easing integrates to full distance at 20/30/60/120 Hz",
		easing_ok)
	_park(0.0, 0.0)
	var before: Vector2 = _player_local()
	var bumps_before: int = int(main.g.get("db_bumps", 0))
	var dodges_before: int = int(main.g.get("db_dodges", 0))
	var hits_before: int = _hits()
	var misses_before: int = int(main.g.get("db_miss", 0))
	main.g["db_from"] = before - Vector2(1.0, 0.0)
	main.g["db_to"] = before + Vector2(1.0, 0.0)
	main.g["db_hop_gap"] = gap
	main.g["db_hop_t"] = gap * 0.5
	main.g["db_bump_cd"] = 0.0
	boss._hop_move(0.0, {"px": before.x, "pz": before.y})
	_ck("an overlapping bunny cannot contact before final descent",
		int(main.g.get("db_bumps", 0)) == bumps_before)
	main.g["db_dodge_window"] = false
	var attempts_before: int = int(main.g.get("db_dodge_attempts", 0))
	_ck("early and vertical swipes stay harmless",
		not boss.on_world_swipe(Vector2(500.0, 360.0), Vector2(670.0, 364.0))
		and not boss.on_world_swipe(Vector2(640.0, 300.0), Vector2(644.0, 470.0))
		and int(main.g.get("db_dodge_attempts", 0)) == attempts_before)
	main.g["db_dodge_window"] = true
	main.g["db_dodge_flash"] = 1.0
	boss._place_boss(0.0)
	var star: Node = main.g.get("db_star") as Node
	var star_color: Color = star.get("modulate") if star != null else Color.BLACK
	var guide: DodgeTutorialGuide = main.g.get("db_dodge_guide") \
		as DodgeTutorialGuide
	_ck("the warning flashes coral on Grand Puff himself",
		star != null and star_color.r > 0.95 and star_color.g < 0.5
		and not (main.g.get("db_kit") as DustBunnyBossSprite).vulnerable)
	_ck("the first warning demonstrates a swipe without adding a button",
		guide != null and guide.visible and guide.demo != null
		and guide.demo.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	main._on_world_drag_end(Vector2(500.0, 360.0), Vector2(670.0, 364.0))
	_ck("a right swipe during the flash starts one dodge",
		int(main.g.get("db_dodge_attempts", 0)) == attempts_before + 1
		and bool(main.g.get("db_dodge_committed", false))
		and not guide.visible)
	for _frame in range(24):
		boss._tick_dodge_motion(1.0 / 60.0)
	var after_right: Vector2 = _player_local()
	_ck("accepted swipe immediately eases Roshan in its direction",
		after_right.x > before.x + 5.0 and main.player.verb == "twirl")
	main.g["db_dodge_window"] = true
	_ck("one incoming hop accepts only one dodge",
		not boss.on_world_swipe(Vector2(500.0, 360.0), Vector2(670.0, 364.0))
		and int(main.g.get("db_dodge_attempts", 0)) == attempts_before + 1)
	var edge: Vector2 = boss.stage.clamp_point(Vector2(100.0, 0.0),
		DustBossGame.PLAYER_INSET)
	_ck("an outward edge swipe chooses one safe mirrored direction",
		boss._safe_dodge_direction(edge, Vector2.RIGHT).x < 0.0)
	main.g["db_dodge_t"] = 0.0
	main.g["db_dodge_cd"] = 0.0
	main.g["db_dodge_committed"] = false
	main.g["db_dodge_window"] = true
	var left_ok: bool = boss.on_world_swipe(
		Vector2(670.0, 360.0), Vector2(500.0, 356.0))
	_ck("a left swipe uses the same pre-impact window",
		left_ok and int(main.g.get("db_dodge_attempts", 0)) == attempts_before + 2
		and (main.g.get("db_dodge_move_dir", Vector2.ZERO) as Vector2).x < 0.0)
	var cancel_position: Vector2 = _player_local()
	boss.cancel_dodge_motion()
	boss._tick_dodge_motion(0.2)
	_ck("focus cancellation stops remaining motion without inventing input",
		_player_local().is_equal_approx(cancel_position)
		and int(main.g.get("db_dodge_attempts", 0)) == attempts_before + 2)
	boss._resolve_player_contact(before - Vector2(1.0, 0.0))
	var after: Vector2 = _player_local()
	_ck("a timed dodge remains displaced when its committed hop contacts",
		after.distance_to(before) > 5.0 and main.player.verb == "twirl")
	_ck("a dodged contact counts a dodge and not a bump",
		int(main.g.get("db_dodges", 0)) == dodges_before + 1
		and int(main.g.get("db_bumps", 0)) == bumps_before)
	_ck("dodge removes no progress and creates no miss",
		_hits() == hits_before and int(main.g.get("db_miss", 0)) == misses_before
		and main.game == "dustboss")

# ---- contact feedback: readable, brief and never punitive ------------------
func _bump_case() -> void:
	var boss := _boss()
	_park(0.0, 0.0)
	var before: Vector2 = _player_local()
	var hits_before: int = _hits()
	var misses_before: int = int(main.g.get("db_miss", 0))
	# Exercise the same helper the live prowl collision calls. Put the contact
	# just to Roshan's left so the expected recoil has an unambiguous direction.
	boss._bump_player(before - Vector2(1.0, 0.0))
	var after: Vector2 = _player_local()
	_ck("a boss bump visibly pushes Roshan away", after.x > before.x + 2.5)
	_ck("a boss bump plays Roshan's short boing reaction", main.player.verb == "boing")
	_ck("a boss bump removes no progress and creates no miss",
		_hits() == hits_before and int(main.g.get("db_miss", 0)) == misses_before
		and main.game == "dustboss")

# ---- window 1: the only place damage exists -------------------------------
func _first_hit_case() -> void:
	var open_now: bool = await _await_state("vuln", 3000)
	_ck("the wind-up becomes an airborne flashing window", open_now)
	var up: bool = await _await_airborne(600)
	_ck("he really is in the air while the star flashes", up)
	_ck("the shared action label reads BONK! exactly while he is open",
		_boss().action_label() == "BONK!")
	# an open window on the far side of the ring is not a free hit: stand
	# diametrically opposite him, inside the octagon, and tap on the flash
	var boss := _boss()
	var him := Vector2(float(main.g.get("db_x", 0.0)), float(main.g.get("db_z", 0.0)))
	var away: Vector2 = (-him).normalized() if him.length() > 0.5 else Vector2(1.0, 0.0)
	var far_spot: Vector2 = away * (OctagonStage.apothem(DustBossGame.RADIUS) - 3.0)
	_park(far_spot.x, far_spot.y)
	var closer_before: int = int(main.g.get("db_closer_feedbacks", 0))
	await _tap()
	var gap: float = (Vector2(float(main.g.get("db_x", 0.0)),
		float(main.g.get("db_z", 0.0))) - _player_local()).length()
	_ck("an open window still needs her to be near him",
		gap > boss.reach() and _hits() == 0)
	_ck("an open-far tap gives a closer picture and voice cue",
		int(main.g.get("db_closer_feedbacks", 0)) == closer_before + 1)
	# Mashing the same far spot keeps the one clear cue, without bunching a
	# second picture/voice response inside its cooldown.
	for i in range(3):
		await _tap()
	_ck("repeated open-too-far taps share the feedback cooldown",
		int(main.g.get("db_closer_feedbacks", 0)) == closer_before + 1)
	# HYBRID TOUCH: the finger goes ON him. Route a world tap through main's
	# own router (the path the touch layer uses) and it must register one of
	# the window's three taps — not a walk order, and not a whole round.
	var opened_again: bool = await _await_state("vuln", 4000)
	var up2: bool = await _await_airborne(600)
	if opened_again and up2:
		var cam: Camera3D = main.player.cam
		var b: Node3D = main.g.get("db_boss") as Node3D
		var on_him: Vector2 = cam.unproject_position(b.global_position
			+ Vector3(0, DustBossGame.BOSS_H * 0.5, 0))
		var kit0: DustBunnyBossSprite = main.g.get("db_kit") as DustBunnyBossSprite
		var taps_before: int = kit0.accepted_taps if kit0 != null else -1
		main._on_touch_world(on_him)
		await process_frame
		_ck("tapping the boss himself is a bonk, not a walk order",
			kit0 != null and kit0.accepted_taps == taps_before + 1)
	var hit1: bool = _hits() >= 1
	if not hit1:
		hit1 = await _strike(4)
	_ck("three quick taps on the flash take one damage round", hit1)
	_ck("the landed hit closes the window", _state() == "struck")
	await _tap()
	await _tap()
	_ck("more taps during the flinch reaction add no damage", _hits() == 1)

# ---- dizzy, then window 2 → angry -----------------------------------------
func _second_hit_case() -> void:
	var boss := _boss()
	_ck("round 1 turns him dizzy", String(boss.phase_cfg()["name"]) == "dizzy")
	_ck("dizzy moves slower than his opening pace",
		boss.hop_speed() < float(DustBossGame.PHASES[0]["hop_speed"]))
	_ck("a damage round is three taps, not one",
		DustBossGame.TAPS_PER_ROUND == 3 and DustBossGame.HP == 3)
	_ck("landed phases include a brief celebration beat",
		DustBossGame.PHASE_BEAT_T > 0.0
		and boss.phase_beat_len(1) == DustBossGame.PHASE_BEAT_T
		and boss.phase_beat_len(2) == DustBossGame.PHASE_BEAT_T
		and boss.celebration_beat_len(1) == DustBossGame.CELEBRATION_BEAT_T
		and boss.celebration_beat_len(2) == DustBossGame.CELEBRATION_BEAT_T)
	_ck("quick wins have a bounded positive pacing floor",
		DustBossGame.POSITIVE_PACING_FLOOR >= 38.0
		and DustBossGame.POSITIVE_PACING_FLOOR < 45.0)
	var hit2: bool = await _strike(4)
	_ck("the second window takes the second round", hit2)
	await _tap()
	_ck("a tap after the round lands adds nothing", _hits() == 2)
	_ck("round 2 turns him angry", String(boss.phase_cfg()["name"]) == "angry")
	var kit2: DustBunnyBossSprite = main.g.get("db_kit") as DustBunnyBossSprite
	_ck("round 2 starts the kit's final round at 1.25x",
		kit2 != null and kit2.final_round_active
		and kit2.combat_speed_scale == DustBunnyBossSprite.FINAL_ROUND_SPEED_SCALE)
	_ck("the final round tightens the window to 0.65s",
		kit2 != null and kit2.current_vulnerability_window()
		== DustBunnyBossSprite.FINAL_ROUND_VULNERABILITY_WINDOW)
	_ck("angry moves at a faster pace than either earlier phase",
		float(DustBossGame.PHASES[2]["hop_speed"]) > float(DustBossGame.PHASES[0]["hop_speed"])
		and float(DustBossGame.PHASES[2]["hop_speed"]) > float(DustBossGame.PHASES[1]["hop_speed"]))
	_ck("the boss is the authored animation kit, not a static card",
		(main.g.get("db_kit") as DustBunnyBossSprite) != null)

# ---- a window let go: mercy, never failure --------------------------------
func _mercy_case() -> void:
	var boss := _boss()
	# Start from a known streak so the check proves attempts 1-2 are unchanged,
	# attempt 3 is the first gentle assist, and miss five owns strong mercy.
	main.g["db_miss"] = 0
	main.g["db_miss_streak"] = 0
	var window_before: float = boss.window_len()
	var reach_before: float = boss.reach()
	var speed_before: float = boss.hop_speed()
	var windup_before: float = boss.windup_len()
	var prowl_before: float = boss.prowl_len()
	var all_missed := true
	var early_lively := true
	var preassist_started := false
	for expected_streak in range(1, DustBossGame.MERCY_TRIGGER_STREAK + 1):
		var open_now: bool = await _await_state("vuln", 4000)
		var back: bool = open_now and await _await_state("prowl", 4000)
		all_missed = all_missed and back and _hits() == 2 \
			and int(main.g.get("db_miss_streak", 0)) == expected_streak
		if expected_streak == DustBossGame.PREASSIST_TRIGGER_STREAK:
			preassist_started = boss.preassist_tier() == 1 \
				and boss.window_len() > window_before \
				and boss.prowl_len() < prowl_before
		if expected_streak < DustBossGame.PREASSIST_TRIGGER_STREAK:
			var early_same: bool = is_equal_approx(boss.window_len(), window_before) \
				and is_equal_approx(boss.reach(), reach_before) \
				and is_equal_approx(boss.hop_speed(), speed_before) \
				and is_equal_approx(boss.prowl_len(), prowl_before)
			all_missed = all_missed and early_same
			early_lively = early_lively and early_same
	_ck("five windows can pass harmlessly with no loss", all_missed and main.game == "dustboss")
	_ck("misses two through four add only gentle bounded help",
		preassist_started and boss.mercy_tier() == 1 and boss.preassist_tier() == 2
		and boss.prowl_len() < prowl_before and boss.reach() > reach_before
		and boss.landing_radius() < 4.0)
	_ck("attempts one and two keep the lively opening pace",
		early_lively and boss.mercy_tier() == 1 and boss.preassist_tier() == 2)
	_ck("miss five switches on a longer next window", boss.window_len() > window_before)
	_ck("miss five owns the strong tier exactly",
		boss.mercy_tier() == 1 and boss.preassist_tier() == 2
		and is_equal_approx(boss.window_len(), window_before
			+ DustBossGame.PREASSIST_WINDOW_MAX
			+ DustBossGame.MERCY_WINDOW_PER_TIER))
	_ck("miss five widens Roshan's forgiving reach", boss.reach() > reach_before)
	_ck("miss five slows the boss and lengthens the tell",
		boss.hop_speed() < speed_before and boss.windup_len() > windup_before)
	_ck("the first assist tier still requires Roshan's input",
		boss._free_taps() == 1 and boss._free_taps() < DustBossGame.TAPS_PER_ROUND)
	var helper_before: int = int(main.g.get("db_helper_taps_total", 0))
	var mercy_open: bool = await _await_state("vuln", 4000)
	var assisted_open: bool = mercy_open and await _await_airborne(1200)
	var helper_inserted: bool = assisted_open \
		and await _await_helper_taps(helper_before + 1, 1200)
	_ck("strong mercy inserts one authoritative helper tap",
		helper_inserted and int(main.g.get("db_helper_taps_total", 0)) == helper_before + 1)

# ---- the third hit ends it as friends -------------------------------------
func _win_case() -> void:
	# The contact helpers above intentionally exercised both outcomes. Reset the
	# mastery-only counter and block incidental prowl contact so this completion
	# deterministically covers the real zero-bump reward path.
	main.g["db_bumps"] = 0
	main.g["db_bump_cd"] = 9999.0
	var pearls_before: int = main.pearl_count
	var day_one_before: bool = main.day_one_is_active()
	var hit3: bool = await _strike(5)
	_ck("the fight keeps offering windows until she lands them", hit3)
	_ck("the third round finishes the fight", _hits() == 3)
	_ck("a landed round resets the streak but keeps the earned assist pace",
		int(main.g.get("db_miss_streak", -1)) == 0 and _boss().mercy_tier() == 1)
	_ck("the ending is a befriending beat, not a defeat", _state() == "friends")
	var wait := 0
	while main.game == "dustboss" and wait < 4000:
		wait += 1
		await process_frame
	_ck("the win banner closes the fight", main.game == "")
	_ck("a clean victory pays the base pearls plus the no-hit bonus",
		main.pearl_count >= pearls_before + DustBossGame.BASE_WIN_PEARLS
		+ DustBossGame.PERFECT_BONUS_PEARLS)
	# MEDALS.md is binding: "Bronze = completion. Every finished game earns at
	# least bronze." The first boss in the game had no medal row at all.
	_ck("a clean boss victory earns the three-star gold medal",
		int(main.medals.get("dustboss", 0)) == MedalSystem.GOLD)
	var award := main.get_node_or_null("MedalCelebrationLayer") as CanvasLayer
	var award_stars := award.get_node_or_null(
		"MedalCelebrationCard/MedalCelebrationStars") as Label if award != null else null
	_ck("the result shows earned stars and the separate perfect-bonus gem",
		award != null and bool(award.get_meta("perfect_bonus", false))
		and award_stars != null and award_stars.text == "★★★"
		and award.get_node_or_null(
			"MedalCelebrationCard/PerfectBonusGem") != null)
	await _frames(2)
	_ck("the real DustBoss seam records defeat and starts Chapter 2",
		main.day_one_giant_dust_bunny_boss_defeated
		and main.chapter2_active
		and main.chapter2_unlocked_opera_mask
		== ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK
		and _event_count(main.day_one_event_history,
			DayOneDirector.EVENT_GIANT_DUST_BUNNY_BOSS_DEFEATED) == 1
		and _event_count(main.chapter2_event_history,
			ChapterTwoDirector.EVENT_CHAPTER_STARTED) == 1)
	var repeated_terminal := main.day_one_complete_boss_and_begin_day_two()
	_ck("repeated terminal callbacks cannot duplicate story events",
		not repeated_terminal
		and _event_count(main.day_one_event_history,
			DayOneDirector.EVENT_GIANT_DUST_BUNNY_BOSS_DEFEATED) == 1
		and _event_count(main.day_one_event_history,
			DayOneDirector.EVENT_DAY_TWO_BEGINS) == 1
		and _event_count(main.chapter2_event_history,
			ChapterTwoDirector.EVENT_CHAPTER_STARTED) == 1)
	_ck("the first victory advances the saved story into Day Two",
		day_one_before and not main.day_one_is_active()
		and not main.day_one_jobs_locked() and main.day_one_opera_enabled())
	_ck("Day Two begins with a picture-first full-screen transition",
		main.day_two_transition_active
		and main.day_two_transition_layer != null
		and main.day_two_transition_layer.get_node_or_null("DayTwoTransitionRoot") != null)
	var transition_wait := 0
	while main.day_two_transition_active and transition_wait < 1200:
		transition_wait += 1
		await process_frame
	_ck("the Day Two transition closes automatically without a reading gate",
		not main.day_two_transition_active and transition_wait < 1200)
	main.touch_ui.action_down = false

# ---- a second fight, walked beat by beat, to check the pose map ------------
func _pose_replay_case() -> void:
	main.dust_boss_cool = 0.0
	main.game = ""
	main._start_game_now(main.dust_boss_fr)
	await _frames(4)
	if main.game != "dustboss":
		_ck("the attic reopens for a second fight", false)
		return
	await _pose_case()
	if main.game == "dustboss":
		main._clear_game()
		main.game = ""
