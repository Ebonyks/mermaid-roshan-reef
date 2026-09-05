extends SceneTree

const FRAME_CAP := 9000
const CONTRACT_CHECKS = preload("res://scripts/encounter_contract_checks.gd")
var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260905)
	Engine.time_scale = 3.0
	# Frame-count watchdogs must leave real timers time to advance on fast CI.
	Engine.max_fps = 120
	main = load("res://scenes/main.tscn").instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		await process_frame
	main._skip_intro()
	await process_frame
	main._set_touch_mode(main.TOUCH_MODE_HYBRID, false)
	# This headless fixture bypasses the normal menu/intro completion callbacks;
	# establish their same neutral no-overlay input boundary explicitly.
	main.touch_control_blocks.clear()
	main._set_world_controls_enabled(true, "dustboss_probe")
	_prepare_terminal_boundary()
	await _open_boss()
	if main.game == "dustboss":
		await _splash_and_geometry_case()
		await _negative_input_case()
		await _adaptive_completion_case()
	print("DUSTBOSS|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit(1 if bad > 0 else 0)

func _ck(label: String, ok: bool) -> void:
	print("DUSTBOSS|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _state() -> String:
	return String(main.g.get("db_state", ""))

func _hits() -> int:
	return int(main.g.get("db_hits", 0))

func _damage() -> int:
	return int(main.g.get("db_damage_taken", 0))

func _boss() -> DustBossGame:
	return main._game_obj("dustboss", DustBossGame) as DustBossGame

func _wait_state(wanted: Array[String], cap: int) -> bool:
	for _i in range(cap):
		if wanted.has(_state()):
			return true
		await process_frame
	return false

func _tap_edge() -> void:
	main.touch_ui.action_down = false
	await process_frame
	main.touch_ui.action_down = true
	await process_frame
	main.touch_ui.action_down = false

func _tap_boss_world() -> void:
	var boss_node: Node3D = main.g.get("db_boss") as Node3D
	var screen_point: Vector2 = main.player.cam.unproject_position(
		boss_node.global_position + Vector3(0.0, DustBossGame.BOSS_H * 0.5, 0.0))
	_ck("flashing boss head remains inside the touch viewport",
		main.get_viewport().get_visible_rect().has_point(screen_point))
	var hits_before: int = _hits()
	main.get_tree().paused = true
	await _push_screen_tap(screen_point, 71)
	main.get_tree().paused = false
	_ck("paused screen touch cannot counter", _hits() == hits_before)
	await _push_screen_tap(screen_point, 72)

func _push_screen_tap(screen_point: Vector2, touch_index: int) -> void:
	var press := InputEventScreenTouch.new()
	press.index = touch_index
	press.position = screen_point
	press.pressed = true
	main.get_viewport().push_input(press, true)
	await process_frame
	var release := InputEventScreenTouch.new()
	release.index = touch_index
	release.position = screen_point
	release.pressed = false
	main.get_viewport().push_input(release, true)
	await process_frame

func _move_one_frame_toward(point: Vector2) -> void:
	var offset: Vector2 = point - _boss().stage.player_local()
	main.touch_ui.stick_vec = offset.limit_length(1.0) if offset.length() > 0.08 else Vector2.ZERO
	await process_frame

func _prepare_terminal_boundary() -> void:
	var director: DayOneDirector = main._day_one_ref()
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
	director.boss_door_glow = true
	director.giant_dust_bunny_boss_defeated = false
	main.save_data["dustboss_pending_rounds"] = 0

func _open_boss() -> void:
	if main.game != "":
		main._clear_game()
		await _frames(2)
	main.game = ""
	main.g = {}
	main.player.visible = true
	main.we_node.environment = main.world_env
	main.dust_boss_cool = 0.0
	var explicit_activation_sent := false
	for _i in range(900):
		main.player.position = main.dust_boss_portal_pos + Vector3(0, 2, 3)
		main.player.vel = Vector3.ZERO
		if main.touch_uses_explicit_interactions() and not explicit_activation_sent:
			main._activate_touch_interactable("reef:dustboss")
			explicit_activation_sent = true
		await process_frame
		if main.game == "dustboss":
			break
	_ck("attic door opens the live boss fight", main.game == "dustboss")

func _splash_and_geometry_case() -> void:
	_ck("fight opens on an input-blocking 2D splash", _state() == "splash" and main.g.get("db_splash") is BossSplash2D)
	var splash: BossSplash2D = main.g.get("db_splash") as BossSplash2D
	var splash_elapsed: float = float(splash.get("_elapsed")) if splash != null else -1.0
	main.get_tree().paused = true
	await _frames(8)
	var paused_elapsed: float = float(splash.get("_elapsed")) if splash != null else -2.0
	_ck("pause freezes splash progression", splash_elapsed == paused_elapsed and _state() == "splash")
	main.get_tree().paused = false
	var attic: CanvasLayer = main.g.get("db_attic_layer") as CanvasLayer
	var floor_warning: DustBossTelegraph2D = main.g.get("db_floor_telegraph") as DustBossTelegraph2D
	var overlay: DustBossTelegraph2D = main.g.get("db_telegraph") as DustBossTelegraph2D
	_ck("floor warnings sit behind actors while gesture cues stay above",
		floor_warning != null and floor_warning.get_parent() == attic
		and floor_warning.draw_floor and not floor_warning.draw_overlay
		and overlay != null and not overlay.draw_floor and overlay.draw_overlay)
	var background: TextureRect = attic.get_node_or_null("DustBossAtticBackdrop") as TextureRect \
		if attic != null else null
	_ck("the August 30 dusty room is the input-transparent Canvas background",
		background != null and background.texture != null
		and background.texture.resource_path == "res://assets/flats/castle/boss/dusty_attic_arena_2048.png"
		and background.mouse_filter == Control.MOUSE_FILTER_IGNORE
		and attic.layer == -20 and main.arena_env.background_canvas_max_layer == -20)
	var contract_failures: Array[String] = CONTRACT_CHECKS.run()
	_ck("shared encounter contract checks pass", contract_failures.is_empty())
	if not contract_failures.is_empty():
		print("DUSTBOSS|contract_failures|", contract_failures)
	await _wait_state(["showing"], 1600)
	_ck("showing follows splash", _state() == "showing")
	_ck("encounter uses direct hybrid world touch without an action medallion",
		main.touch_ui.encounter_press.is_valid()
		and main.find_child("JumpButton", true, false) == null)
	main.touch_ui.set_mode("classic")
	_ck("encounter keeps direct classic world touch without an action medallion",
		main.touch_ui.encounter_press.is_valid()
		and main.find_child("JumpButton", true, false) == null)
	main.touch_ui.set_mode("hybrid")
	_navigation_roundtrip_case()
	_pattern_geometry_case()

func _negative_input_case() -> void:
	await _frames(340)
	await _tap_edge()
	await _wait_state(["tell"], 900)
	_safe_navigation_case()
	var hits_before: int = _hits()
	var damage_before: int = _damage()
	var no_input_recovery := await _wait_state(["damage_recovery"], 900)
	_ck("zero input takes a harmless bump but cannot damage the boss",
		no_input_recovery and _damage() > damage_before and _hits() == hits_before)
	await _wait_state(["tell"], 900)
	damage_before = _damage()
	var saw_tell := false
	var saw_strike := false
	var saw_recovery := false
	for i in range(1300):
		var state: String = _state()
		saw_tell = saw_tell or state == "tell"
		saw_strike = saw_strike or state == "strike"
		saw_recovery = saw_recovery or state == "damage_recovery"
		main.touch_ui.action_down = i % 8 < 2
		await process_frame
		if saw_recovery and _damage() > damage_before and state == "tell":
			break
	main.touch_ui.action_down = false
	_ck("stationary tap spam traverses real tell, strike, and recovery", saw_tell and saw_strike and saw_recovery and _damage() > damage_before)
	_ck("stationary tap spam cannot damage the boss", main.game == "dustboss" and _hits() == hits_before)
	await _wait_state(["tell"], 900)
	main.touch_ui.action_down = true
	var held_saw_vuln := false
	for _i in range(1500):
		held_saw_vuln = held_saw_vuln or _state() == "vuln"
		if _state() == "tell":
			await _move_one_frame_toward(_boss().danger_geometry().get(
				"safe_point", Vector2.ZERO) as Vector2)
		else:
			main.touch_ui.stick_vec = Vector2.ZERO
			await process_frame
		if held_saw_vuln and _state() == "tell":
			break
	main.touch_ui.action_down = false
	main.touch_ui.stick_vec = Vector2.ZERO
	_ck("held action reaches an opening without auto-countering", held_saw_vuln and _hits() == hits_before)
	_ck("no-input and held input cannot finish", main.game == "dustboss")

func _safe_navigation_case() -> void:
	var boss: DustBossGame = _boss()
	var danger: Dictionary = boss.danger_geometry()
	var safe: Vector2 = danger.get("safe_point", Vector2.ZERO) as Vector2
	var screen_point: Vector2 = boss.stage.project_floor_point(safe)
	var before: Vector2 = boss.stage.player_local()
	boss.on_world_tap(screen_point)
	var destination: Vector2 = boss.navigation.destination
	_ck("safe ground tap arms real encounter navigation", boss.navigation.travelling
		and destination.distance_to(safe) < 0.2)
	await _frames(12)
	var after: Vector2 = boss.stage.player_local()
	_ck("safe ground navigation moves the player", after.distance_to(before) > 0.05)
	boss.navigation.move_to(safe)
	main.touch_ui.cancel_all_touches()
	_ck("focus or touch cancellation drops encounter destination", not boss.navigation.travelling)
	main.get_tree().paused = true
	main.touch_ui.cancel_all_touches()
	main.get_tree().paused = false
	_ck("pause cancellation leaves no stale encounter destination", not boss.navigation.travelling)

func _navigation_roundtrip_case() -> void:
	var boss: DustBossGame = _boss()
	var all_ok := true
	for index: int in range(16):
		var angle: float = TAU * float(index) / 16.0
		var floor_point: Vector2 = boss.stage.clamp_point(
			Vector2(cos(angle), sin(angle)) * 22.0, 2.6)
		var screen_point: Vector2 = boss.stage.project_floor_point(floor_point)
		var roundtrip: Vector2 = boss.navigation.screen_to_floor(screen_point)
		all_ok = all_ok and roundtrip.distance_to(floor_point) < 0.05
	_ck("2D floor and screen navigation round-trips 16 arena points", all_ok)

func _adaptive_completion_case() -> void:
	var saw_phase := [false, false, false]
	var saw_phase_one_combo := false
	var saw_final_lane := false
	var saw_telegraph := false
	var snapshot_checked := false
	var last_tell_key := ""
	var locked_target := Vector2.ZERO
	var tapped_opening := false
	var checkpoint_done := false
	var final_checkpoint_done := false
	var used_world_touch := false
	var checkpoint_pearls := main.pearl_count
	for _i in range(FRAME_CAP):
		if main.game != "dustboss":
			break
		var state: String = _state()
		if state != "vuln":
			tapped_opening = false
		if state == "tell":
			var danger: Dictionary = _boss().danger_geometry()
			var phase: int = int(danger.get("phase", -1))
			var step: int = int(danger.get("step", -1))
			if phase >= 0 and phase < saw_phase.size():
				saw_phase[phase] = true
			saw_phase_one_combo = saw_phase_one_combo or (phase == 1 and int(danger.get("step_count", 0)) == 2 and step == 1)
			saw_final_lane = saw_final_lane or (phase == 2 and step == 1 and String(danger.get("shape", "")) == "lane")
			var telegraph: DustBossTelegraph2D = main.g.get("db_telegraph") as DustBossTelegraph2D
			var mastery_layer: CanvasLayer = main.g.get("db_mastery_layer") as CanvasLayer
			saw_telegraph = saw_telegraph or (telegraph != null and is_instance_valid(telegraph)
				and telegraph.visible and bool(telegraph._visible)
				and mastery_layer != null and mastery_layer.visible)
			var tell_key := "%d:%d:%d" % [phase, step, _hits()]
			var target: Vector2 = danger.get("locked_center", danger.get("center", Vector2.ZERO)) as Vector2
			if tell_key != last_tell_key:
				last_tell_key = tell_key
				locked_target = target
				_ck("live tell %s lasts at least 1.4 seconds" % tell_key, float(danger.get("tell_duration", 0.0)) >= 1.4)
			elif target.distance_to(locked_target) < 0.05:
				snapshot_checked = true
			await _move_one_frame_toward(danger.get("safe_point", Vector2.ZERO) as Vector2)
			continue
		main.touch_ui.stick_vec = Vector2.ZERO
		var kit: DustBunnyBossSprite = _boss().kit()
		if state == "vuln" and kit != null and kit.vulnerable and not tapped_opening:
			tapped_opening = true
			if _hits() == 2:
				used_world_touch = true
				await _tap_corner_rejected()
				await _tap_boss_world()
			else:
				await _tap_edge()
			if _hits() == 1 and not checkpoint_done:
				checkpoint_done = true
				checkpoint_pearls = main.pearl_count
				await _checkpoint_restart_case(checkpoint_pearls)
				last_tell_key = ""
				continue
			if _hits() == DustBossGame.HP and not final_checkpoint_done:
				final_checkpoint_done = true
				await _final_checkpoint_restart_case(main.pearl_count)
				continue
		await process_frame
	var completion_pearls: int = main.pearl_count
	_ck("adaptive movement observes all three phases", bool(saw_phase[0]) and bool(saw_phase[1]) and bool(saw_phase[2]))
	_ck("phase one executes both warned circles", saw_phase_one_combo)
	_ck("phase two executes its warned lane", saw_final_lane)
	_ck("live tells keep their captured target while the player moves", snapshot_checked)
	_ck("a visible 2D telegraph accompanies live danger", saw_telegraph)
	_ck("hybrid head touch can land a real counter", used_world_touch)
	_ck("one fresh counter edge per opening completes three rounds", main.game == "")
	_ck("the earned final round survives interruption", final_checkpoint_done)
	_ck("completion grants the base reward exactly once", completion_pearls == checkpoint_pearls + DustBossGame.BASE_WIN_PEARLS)
	var director: DayOneDirector = main._day_one_ref()
	_ck("completion saves defeat and begins Day Two", director.giant_dust_bunny_boss_defeated and not main.day_one_is_active() and main.chapter2_active and int(main.save_data.get("dustboss_pending_rounds", -1)) == 0)
	var event_count: int = _event_count(DayOneDirector.EVENT_DAY_TWO_BEGINS)
	var pearls_before_repeat: int = main.pearl_count
	var repeated: bool = main.day_one_complete_boss_and_begin_day_two()
	await process_frame
	_ck("Day Two and reward cannot duplicate", not repeated and _event_count(DayOneDirector.EVENT_DAY_TWO_BEGINS) == event_count and main.pearl_count == pearls_before_repeat)

func _checkpoint_restart_case(pearls_before: int) -> void:
	var old_attic: CanvasLayer = main.g.get("db_attic_layer") as CanvasLayer
	var damage_before: int = _damage()
	var misses_before: int = int(main.g.get("db_opening_misses", 0))
	_ck("landed round writes its checkpoint", int(main.save_data.get("dustboss_pending_rounds", 0)) == 1)
	main._clear_game()
	await _frames(3)
	_ck("interrupt removes the dusty room Canvas", not is_instance_valid(old_attic))
	_ck("interrupt preserves progress without reward", int(main.save_data.get("dustboss_pending_rounds", 0)) == 1 and main.pearl_count == pearls_before)
	if main._castle_rooms_ref().is_open():
		main._castle_rooms_ref().close()
	main.touch_control_blocks.clear()
	main._set_world_controls_enabled(true, "checkpoint_probe")
	main._day_one_ref().giant_dust_bunny_boss_triggered = true
	main._start_game_now(main.dust_boss_fr)
	await process_frame
	_ck("re-entry restores the exact completed round", main.game == "dustboss" and _hits() == 1)
	_ck("checkpoint preserves damage mastery and opening assistance",
		_damage() == damage_before and int(main.g.get("db_bumps", 0)) == damage_before
		and int(main.g.get("db_opening_misses", 0)) == misses_before)
	await _wait_state(["showing"], 1600)
	await _frames(340)
	await _tap_edge()

func _tap_corner_rejected() -> void:
	var hits_before: int = _hits()
	var viewport: Rect2 = main.get_viewport().get_visible_rect()
	var corner := viewport.position + Vector2(viewport.size.x - 24.0, viewport.size.y - 24.0)
	await _push_screen_tap(corner, 70)
	_ck("old screen corner tap cannot counter", _hits() == hits_before)

func _final_checkpoint_restart_case(pearls_before: int) -> void:
	_ck("final counter writes all three earned rounds before celebration",
		int(main.save_data.get("dustboss_pending_rounds", 0)) == DustBossGame.HP
		and _hits() == DustBossGame.HP)
	main._clear_game()
	await _frames(3)
	_ck("final-round interruption grants no early or duplicate reward",
		int(main.save_data.get("dustboss_pending_rounds", 0)) == DustBossGame.HP
		and main.pearl_count == pearls_before)
	if main._castle_rooms_ref().is_open():
		main._castle_rooms_ref().close()
	main.touch_control_blocks.clear()
	main._set_world_controls_enabled(true, "final_checkpoint_probe")
	main._day_one_ref().giant_dust_bunny_boss_triggered = true
	main._start_game_now(main.dust_boss_fr)
	await process_frame
	_ck("final checkpoint restores three rounds exactly", main.game == "dustboss"
		and _hits() == DustBossGame.HP)
	var repeated_combat := false
	var resumed_friends := false
	for _i in range(1800):
		var state: String = _state()
		repeated_combat = repeated_combat or state == "tell" or state == "strike" \
			or state == "damage_recovery" or state == "vuln"
		if state == "friends":
			resumed_friends = true
			break
		await process_frame
	_ck("final checkpoint resumes friendship without repeated combat",
		resumed_friends and not repeated_combat and _hits() == DustBossGame.HP)

func _event_count(event_name: String) -> int:
	var count := 0
	for event: Dictionary in main._day_one_ref().event_history():
		if String(event.get("event", event.get("name", ""))) == event_name:
			count += 1
	return count

func _pattern_geometry_case() -> void:
	var stage: OctagonStage = _boss().stage
	var points: Array[Vector2] = []
	for i in range(16):
		var angle: float = TAU * float(i) / 16.0
		points.append(stage.clamp_point(Vector2(cos(angle), sin(angle)) * 80.0, 2.6))
	var all_ok := true
	for phase in range(3):
		for point_index in range(points.size()):
			var sequencer := DustBossPatterns.new()
			var expected: Vector2 = points[point_index]
			sequencer.begin_phase(phase, expected, Vector2.ZERO, DustBossGame.RADIUS)
			for step in range(sequencer.step_count()):
				var readout: Dictionary = sequencer.readout()
				var expected_shape := "lane" if phase == 2 and step == 1 else "circle"
				var captured: Vector2 = readout.get("locked_center", readout.get("center", Vector2.ZERO)) as Vector2
				var safe: Vector2 = readout.get("safe_point", Vector2.ZERO) as Vector2
				var step_ok: bool = String(readout.get("shape", "")) == expected_shape
				step_ok = step_ok and captured.distance_to(expected) < 0.05
				step_ok = step_ok and sequencer.contains(expected)
				step_ok = step_ok and not sequencer.contains(safe)
				step_ok = step_ok and safe.distance_to(stage.clamp_point(safe, 2.6)) < 0.05
				if not step_ok and all_ok:
					print("DUSTBOSS|geometry_failure|phase=", phase, "|step=", step,
						"|point=", expected, "|captured=", captured, "|safe=", safe,
						"|safe_inside=", sequencer.contains(safe), "|readout=", readout)
				all_ok = all_ok and step_ok
				if step + 1 < sequencer.step_count():
					expected = points[(point_index + step + 5) % points.size()]
					sequencer.advance_combo(expected, Vector2.ZERO, DustBossGame.RADIUS)
	_ck("all 16 edge targets are captured, covered, escapable, and stage-valid in every phase step", all_ok)
