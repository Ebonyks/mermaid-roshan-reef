extends SceneTree
# Dust Bunny Boss probe: the boss AI contract (DUST_BUNNY_BOSS_2026-08-02.md).
# The showing runs before the fight; taps land damage ONLY while he is
# airborne with his star flashing, one hit per window; hit 1 turns him dizzy
# (slower), hit 2 turns him angry (faster), hit 3 ends the fight as friends;
# a window that closes unhit is not a failure but a mercy step that lengthens
# the next window and grows her reach. Every hit here comes from a real tap
# edge on touch_ui, so nothing in this file can win the fight without input.
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
		await _showing_case()
		await _shield_case()
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
		n += 1
		await process_frame
	return false

func _await_airborne(cap: int) -> bool:
	var n := 0
	while n < cap:
		if main.game != "dustboss" or _state() != "vuln":
			return false
		if float(main.g.get("db_y", 0.0)) > 2.0 and float(main.g.get("db_flash", 0.0)) >= 0.99:
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
	# wait for a flashing window, stand under him, tap. A tap that arrives
	# after the window closed costs a retry, never the run — exactly what a
	# small player's late tap costs.
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
		await _tap()
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

# ---- the art contract ------------------------------------------------------
func _pose_case() -> void:
	# The boss draws one pose PER BEAT (BOSS_ART_INTEGRATION_2026-08-02.md).
	# Every pose is optional and falls back to the placeholder card, so this
	# asserts the MAP, not the files — it stays green before the art lands and
	# catches a beat wired to the wrong drawing after it does. Sampled EVERY
	# frame, because the interesting poses (wind-up, open) last under a second.
	var boss := _boss()
	var seen: Dictionary = {}
	for key: String in DustBossGame.BOSS_POSES.keys():
		seen[key] = false
	_ck("every beat maps to a named pose", boss.pose_for_state() != "")
	var guard := 0
	while main.game == "dustboss" and guard < 20000:
		var pose: String = boss.pose_for_state()
		if seen.has(pose):
			seen[pose] = true
		# land the three hits as they come, without skipping past any beat
		if _state() == "vuln" and float(main.g.get("db_y", 0.0)) > 2.0:
			_park_on_boss()
			main.touch_ui.action_down = (guard % 6) < 3
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
	_ck("the fight shows the idle, wind-up, open, dizzy and angry poses",
		bool(seen.get("idle", false)) and bool(seen.get("windup", false))
		and bool(seen.get("open", false)) and bool(seen.get("dizzy", false))
		and bool(seen.get("angry", false)))
	_ck("the befriending beat has its own pose", bool(seen.get("friends", false)))
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
	# the button must say what it does, in a fight whose only verb is a bonk
	var boss0 := _boss()
	_ck("the button reads WAIT while he is shut", boss0.action_label() == "WAIT")
	var reached: bool = await _await_state("prowl", 3000)
	_ck("the showing hands over to the prowl", reached)

# ---- shielded: he is a ball of dust ---------------------------------------
func _shield_case() -> void:
	var before: int = int(main.g.get("db_shield_taps", 0))
	for i in range(4):
		_park_on_boss()
		await _tap()
	_ck("taps while he bounces around land no damage", _hits() == 0)
	_ck("a shielded tap still answers with a poof",
		int(main.g.get("db_shield_taps", 0)) > before)
	var windup: bool = await _await_state("windup", 3000)
	_ck("the prowl telegraphs the leap with a wind-up", windup)

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
	await _tap()
	var gap: float = (Vector2(float(main.g.get("db_x", 0.0)),
		float(main.g.get("db_z", 0.0))) - _player_local()).length()
	_ck("an open window still needs her to be near him",
		gap > boss.reach() and _hits() == 0)
	# HYBRID TOUCH: the finger goes ON him. Route a world tap through main's
	# own router (the path the touch layer uses) and it must be the bonk.
	var opened_again: bool = await _await_state("vuln", 4000)
	var up2: bool = await _await_airborne(600)
	if opened_again and up2:
		var cam: Camera3D = main.player.cam
		var b: Node3D = main.g.get("db_boss") as Node3D
		var on_him: Vector2 = cam.unproject_position(b.global_position
			+ Vector3(0, DustBossGame.BOSS_H * 0.5, 0))
		var hits_before: int = _hits()
		main._on_touch_world(on_him)
		await process_frame
		_ck("tapping the boss himself is the bonk, not a walk order",
			_hits() == hits_before + 1)
	var hit1: bool = _hits() >= 1
	if not hit1:
		hit1 = await _strike(4)
	_ck("the first flash she reaches takes damage", hit1)
	_ck("the landed hit closes the window", _state() == "struck")
	await _tap()
	await _tap()
	_ck("more taps during the hit reaction add no damage", _hits() == 1)

# ---- dizzy, then window 2 → angry -----------------------------------------
func _second_hit_case() -> void:
	var boss := _boss()
	_ck("hit 1 turns him dizzy", String(boss.phase_cfg()["name"]) == "dizzy")
	_ck("dizzy moves slower than his opening pace",
		boss.hop_speed() < float(DustBossGame.PHASES[0]["hop_speed"]))
	_ck("dizzy is given a longer window than his opening one",
		float(DustBossGame.PHASES[1]["window_t"]) > float(DustBossGame.PHASES[0]["window_t"]))
	var hit2: bool = await _strike(4)
	_ck("the second flash takes the second damage", hit2)
	await _tap()
	_ck("a tap after the landing hit adds nothing", _hits() == 2)
	_ck("hit 2 turns him angry", String(boss.phase_cfg()["name"]) == "angry")
	_ck("angry moves at a faster pace than either earlier phase",
		float(DustBossGame.PHASES[2]["hop_speed"]) > float(DustBossGame.PHASES[0]["hop_speed"])
		and float(DustBossGame.PHASES[2]["hop_speed"]) > float(DustBossGame.PHASES[1]["hop_speed"]))
	_ck("angry windows are shorter than the opening ones",
		float(DustBossGame.PHASES[2]["window_t"]) < float(DustBossGame.PHASES[0]["window_t"]))

# ---- a window let go: mercy, never failure --------------------------------
func _mercy_case() -> void:
	var boss := _boss()
	# start the ramp from a known step so the check reads the ramp itself and
	# not whatever retries earlier cases happened to spend
	main.g["db_miss"] = 0
	var missed_before: int = 0
	var window_before: float = boss.window_len()
	var reach_before: float = boss.reach()
	var open_now: bool = await _await_state("vuln", 4000)
	_ck("he opens another window while angry", open_now)
	# deliberately let this one go by without a tap
	var back: bool = await _await_state("prowl", 4000)
	_ck("a window nobody hits simply closes again", back and _hits() == 2)
	_ck("the missed window is counted as mercy, not as a loss",
		int(main.g.get("db_miss", 0)) > missed_before and main.game == "dustboss")
	_ck("mercy makes the next window longer", boss.window_len() > window_before)
	_ck("mercy makes her reach bigger", boss.reach() > reach_before)

# ---- the third hit ends it as friends -------------------------------------
func _win_case() -> void:
	var pearls_before: int = main.pearl_count
	var hit3: bool = await _strike(5)
	_ck("the fight keeps offering windows until she lands them", hit3)
	_ck("the third flash finishes the fight", _hits() == 3)
	_ck("the ending is a befriending beat, not a defeat", _state() == "friends")
	var wait := 0
	while main.game == "dustboss" and wait < 4000:
		wait += 1
		await process_frame
	_ck("the win banner closes the fight", main.game == "")
	_ck("befriending him pays the portal pearls", main.pearl_count >= pearls_before + 3)
	# MEDALS.md is binding: "Bronze = completion. Every finished game earns at
	# least bronze." The first boss in the game had no medal row at all.
	_ck("beating the boss earns a medal", int(main.medals.get("dustboss", 0)) >= 1)
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
