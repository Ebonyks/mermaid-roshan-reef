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
	await _open_case()
	if main.game == "dustboss":
		await _framing_case()
		await _splash_case()
		await _showing_case()
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
		if want != "pounce" and _state() == "pounce":
			var dodge: DodgeEngine = main.g.get("db_dodge") as DodgeEngine
			if dodge != null and dodge.available:
				_boss().on_world_swipe(Vector2(520.0, 420.0), Vector2(650.0, 424.0))
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
	var guide: DodgeTutorialGuide = main.g.get("db_dodge_guide") as DodgeTutorialGuide
	_ck("the dodge lesson reuses a true-2D picture-first guide",
		guide != null and guide.get_node_or_null("DodgeTutorialGuideRoot") is Control)
	# taps during the reveal teach nothing bad: they cannot scratch him
	for i in range(4):
		await _tap()
	_ck("taps during the showing land no damage", _hits() == 0)
	# and they must not be counted against her medal, nor scold her over the
	# teaching line — the showing is where the rule is taught
	_ck("taps during the showing cost her no medal tier",
		int(main.g.get("db_wasted", 0)) == 0)
	# the button must say what it does, in a fight whose only verb is a bonk
	var boss0 := _boss()
	_ck("the button reads WAIT while he is shut", boss0.action_label() == "WAIT")
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
	await _dodge_tutorial_case()
	var windup: bool = await _await_state("windup", 3000)
	_ck("the dodge pounce recovers into the separate bonk wind-up", windup)

func _dodge_tutorial_case() -> void:
	var pounce: bool = await _await_state("pounce", 3000)
	_ck("the prowl opens a separate committed landing pounce", pounce)
	if not pounce:
		return
	var dodge: DodgeEngine = main.g.get("db_dodge") as DodgeEngine
	_ck("the pounce owns the reusable 2D dodge engine", dodge != null)
	if dodge == null:
		return
	var bumps_before: int = int(main.g.get("db_bumps", 0))
	var first_attack: int = int(main.g.get("db_dodge_attack_id", 0))
	while _state() == "pounce":
		await process_frame
	_ck("the first safe lesson cannot advance passively",
		not bool(main.g.get("db_dodge_lesson_done", false))
		and int(main.g.get("db_bumps", 0)) == bumps_before and _hits() == 0)
	var replayed: bool = await _await_state("pounce", 3000)
	_ck("an unanswered lesson replays a fresh committed pounce",
		replayed and int(main.g.get("db_dodge_attack_id", 0)) == first_attack + 1)
	if not replayed:
		return
	dodge = main.g.get("db_dodge") as DodgeEngine
	var committed: Vector2 = dodge.landing
	# Vertical movement is a harmless wrong gesture and cannot graduate the
	# picture-first lesson or move Roshan.
	while _state() == "pounce" and not dodge.available:
		await process_frame
	var before: Vector2 = _player_local()
	var rejected: bool = not _boss().on_world_swipe(
		Vector2(640.0, 430.0), Vector2(646.0, 560.0))
	_ck("a vertical gesture cannot trigger the lateral dodge",
		rejected and not bool(main.g.get("db_dodge_lesson_done", false)))
	_ck("the encounter exposes the same world-swipe owner in Classic preference",
		main.touch_ui.control_mode == "hybrid")
	var accepted_before: int = dodge.accepted_count
	var press := InputEventScreenTouch.new()
	press.index = 7
	press.position = Vector2(560.0, 300.0)
	press.pressed = true
	main.touch_ui._input(press)
	var drag := InputEventScreenDrag.new()
	drag.index = 7
	drag.position = Vector2(730.0, 304.0)
	drag.relative = Vector2(170.0, 4.0)
	main.touch_ui._input(drag)
	var release := InputEventScreenTouch.new()
	release.index = 7
	release.position = drag.position
	release.pressed = false
	main.touch_ui._input(release)
	var accepted: bool = dodge.accepted_count == accepted_before + 1
	await _frames(3)
	var partial: Vector2 = _player_local()
	main._on_world_press_cancel()
	await _frames(8)
	var after: Vector2 = _player_local()
	_ck("a real right swipe graduates the dodge lesson",
		accepted and bool(main.g.get("db_dodge_lesson_done", false))
		and int(main.g.get("db_dodge_successes", 0)) == 1)
	_ck("the dodge begins within one rendered frame and moves laterally",
		partial.x > before.x + 0.05 and absf(partial.y - before.y) < 0.5)
	_ck("focus cancellation leaves no stale dash to resume",
		after.distance_to(partial) < 0.01)
	_ck("the bunny never re-homes after the swipe",
		dodge.landing.distance_to(committed) < 0.001)
	_ck("dodge practice changes no boss progress",
		_hits() == 0 and int(main.g.get("db_miss", 0)) == 0)
	var edge: Vector2 = Vector2(OctagonStage.apothem(DustBossGame.RADIUS) - 2.7, 0.0)
	var fallback_dir: Vector2 = _boss().safe_dodge_direction(edge, Vector2.RIGHT)
	var fallback: Vector2 = edge
	for _i in range(21):
		fallback = _boss().safe_dodge_target(fallback,
			fallback_dir * (DodgeEngine.DODGE_DISTANCE / 21.0))
	_ck("an outward wall swipe chooses one inward direction for the full dodge",
		fallback_dir == Vector2.LEFT and fallback.x < edge.x - 5.0
		and _boss().stage.clamp_point(fallback, 2.6).distance_to(fallback) < 0.001)

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
	_ck("the button reads BONK! exactly while he is open",
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
	_ck("fight teardown restores the player's prior touch preference",
		main.touch_ui.control_mode == main.touch_mode)
	_ck("befriending him pays the portal pearls", main.pearl_count >= pearls_before + 3)
	# MEDALS.md is binding: "Bronze = completion. Every finished game earns at
	# least bronze." The first boss in the game had no medal row at all.
	_ck("beating the boss earns a medal", int(main.medals.get("dustboss", 0)) >= 1)
	await _frames(2)
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
