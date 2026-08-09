extends SceneTree
## Runtime contract for the thirteen Canvas-based Pearl Opera career worlds.
##
## This intentionally forces the 2D path under headless Godot. The older
## probe_opera.gd continues to regression-test the detailed legacy mechanics,
## while this probe proves the shipping door path uses supplied paintings,
## 2D actors, one-finger phases, competition progress and clean teardown.

var main: ReefMain
var bad := 0
var widget_shot_out := ""
var rival_shot_out := ""
var scuffle_shot_out := ""
var scuffle_capture_career := ""
var stress_shot_out := ""


func _init() -> void:
	widget_shot_out = OS.get_environment("OPERA_WIDGET_SHOT_OUT").strip_edges()
	rival_shot_out = OS.get_environment("OPERA_RIVAL_SHOT_OUT").strip_edges()
	scuffle_shot_out = OS.get_environment("OPERA_SCUFFLE_SHOT_OUT").strip_edges()
	scuffle_capture_career = OS.get_environment("OPERA_SCUFFLE_CAPTURE_CAREER").strip_edges()
	stress_shot_out = OS.get_environment("OPERA_STRESS_SHOT_OUT").strip_edges()
	if not widget_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(widget_shot_out)
	if not rival_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(rival_shot_out)
	if not scuffle_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(scuffle_shot_out)
	if not stress_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(stress_shot_out)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.game = "opera"

	OS.set_environment("OPERA_FORCE_2D_LOBBY", "1")
	main.opera_stars = 0
	var lobby_touch_before := main.touch_ui.visible if main.touch_ui != null else false
	var house := OperaHouse.new()
	get_root().add_child(house)
	house.start(main, 0, Callable())
	await process_frame
	_check("shipping Opera entry uses the Canvas lobby", house.use_lobby_2d and house.lobby_2d != null)
	if house.lobby_2d != null:
		var lobby := house.lobby_2d
		_check("2D lobby has no 3D navigation children", house.find_children("*", "Node3D", true, false).is_empty())
		_check("2D lobby exposes three direct floor tabs", lobby.floor_tabs.size() == 3)
		_check("2D lobby shows four large job cards on floor one",
			lobby.card_buttons.size() == 5 and _visible_card_count(lobby.card_buttons) == 4)
		var roshan_only := true
		for card: Button in lobby.card_buttons:
			roshan_only = roshan_only and card.get_node_or_null("RoshanActor") != null
			roshan_only = roshan_only and card.get_node_or_null("RivalActor") == null
		_check("job cards show Roshan only, never imp matchup cards", roshan_only)
		_check("floor finale is gated by the four job stars", bool(lobby.boss_button.get_meta("locked", false)))
		lobby.refresh((1 << 4) | (1 << 9), 2)
		_check("Grand Gallery expands to five direct job cards", _visible_card_count(lobby.card_buttons) == 5)
		_check("Nursery Nurse is displayed as job twelve before Pop Star",
			int(lobby.card_buttons[3].get_meta("act_index", -1)) == 15
			and int(lobby.card_buttons[4].get_meta("act_index", -1)) == 13)
		_check("five Grand Gallery jobs gate the finale", bool(lobby.boss_button.get_meta("locked", false)))
		lobby.refresh(0, 0)
	house._leave_early()
	await process_frame
	OS.set_environment("OPERA_FORCE_2D_LOBBY", "0")
	if main.touch_ui != null:
		_check("2D lobby restores the touch layer on exit", main.touch_ui.visible == lobby_touch_before)
	var show_count := 0
	var total_widget_count := 0
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("type", "show")) == "boss":
			continue
		show_count += 1
		var config := source.duplicate(true)
		config["force_2d"] = true
		var touch_before := main.touch_ui.visible if main.touch_ui != null else false
		var act := OperaAct.new()
		get_root().add_child(act)
		act.start(main, config, Callable())
		await process_frame
		var career := String(config.get("costume", ""))
		_check("%s enters Canvas career world" % career,
			act.use_career_world_2d and act.career_world_2d != null)
		if act.career_world_2d == null:
			act.queue_free()
			continue
		var world := act.career_world_2d
		if not scuffle_shot_out.is_empty() and not scuffle_capture_career.is_empty():
			if career != scuffle_capture_career:
				act.cancel()
				await process_frame
				continue
			await _capture_scuffle_sequences(world, career)
			act.cancel()
			await process_frame
			if bad == 0:
				print("OPERA2D|result: ALL OK (scuffle capture)")
				quit()
			else:
				print("OPERA2D|result: %d FAIL" % bad)
				quit(1)
			return
		_check("%s uses no 3D children in career play" % career,
			act.find_children("*", "Node3D", true, false).is_empty())
		_check("%s builds a scalable code-native career world" % career,
			world.get_node_or_null("OperaCareerWorld2D/CareerWorldBackdrop") is OperaWorldBackdrop2D)
		_check("%s loads Mermaid Roshan's outfit actor" % career,
			world.player_actor != null and world.player_actor.texture != null)
		_check("%s loads its dressed rival or care partner" % career,
			world.rival_actor != null and world.rival_actor.texture != null)
		var cooperative := act.competition != null and act.competition.is_cooperative()
		if cooperative:
			_check("%s keeps its care partner beside Roshan from the first beat" % career,
				world.rival_actor.visible)
		else:
			_check("%s keeps the rival hidden during earlier minigames" % career,
				not world.rival_actor.visible and not world.in_competition_finale())
		_check("%s pauses competition scoring before the finale" % career,
			not act.competition.active)
		if not scuffle_shot_out.is_empty() and scuffle_capture_career.is_empty() \
				and career in ["chef", "detective", "ballerina", "candymaker", "nursery"]:
			await _capture_scuffle_sequences(world, career)
		_check("%s has a multi-phase job game" % career, world.phases.size() >= 4)
		_check("%s starts without passive progress" % career,
			is_equal_approx(world.progress(), 0.0))
		var modes: Array[String] = []
		for phase_dict: Dictionary in world.phases:
			modes.append(String(phase_dict.get("mode", "")))
		_check("%s opens with a friendly imp scuffle" % career,
			modes.size() > 0 and modes[0] == "bop")
		# Costume identity lock: bopping a dressed crew imp must never swap her
		# back to the base purple imp — that reads as a different character
		# every time she is bopped.
		#
		# The invariant is "never a base imp", NOT "always exactly the idle
		# costume texture". Painted per-pose art (rival_<costume>_windup.png and
		# friends) landed on dev, and _apply_imp_pose swaps to it by design, so
		# a crew imp legitimately wears a different texture depending on which
		# pose her brain is in on the frame this runs. Asserting equality with
		# the idle texture would pass or fail on tick timing rather than on the
		# thing that actually matters.
		if not cooperative and not world.combat_imps.is_empty():
			var base_imp := load("res://assets/opera/worlds/actors/imp_mischief.png") as Texture2D
			var base_captain := load("res://assets/opera/worlds/actors/imp_captain.png") as Texture2D
			var crew_dressed := true
			for imp_entry: Dictionary in world.combat_imps:
				var crew_node := imp_entry.get("node") as TextureRect
				crew_dressed = crew_dressed and crew_node != null \
					and crew_node.texture != null \
					and crew_node.texture != base_imp \
					and crew_node.texture != base_captain
			_check("%s scuffle crew wears the career costume" % career, crew_dressed)
			var victim: Dictionary = world.combat_imps[0]
			var victim_node := victim.get("node") as TextureRect
			world._hit_stage_imp(victim, Vector2(100.0, 100.0))
			_check("%s keeps its costume through the shoo-off" % career,
				victim_node != null and is_instance_valid(victim_node)
				and victim_node.texture != base_imp
				and victim_node.texture != base_captain)
			_check("%s plays the shoo-off clip about the imp" % career,
				victim_node != null and is_instance_valid(victim_node)
				and victim_node.pivot_offset.is_equal_approx(victim_node.size * 0.5))
			var authored_exact := true
			for state: String in OperaCareerWorld2D.IMP_PREWARM_STATES:
				var resolution := world._imp_texture_resolution({"captain": false}, state)
				authored_exact = authored_exact \
					and String(resolution.get("family", "")) == "rival_%s" % career \
					and String(resolution.get("resolution", "")) == "exact"
			_check("%s resolves every delivered state exactly within its costume family" % career,
				authored_exact)
			var idle_texture := world.rival_actor.texture
			_check("%s finale rival exposes authored taunt" % career,
				world._set_rival_pose("taunt")
				and world.rival_actor.texture.resource_path.ends_with("rival_%s_taunt.png" % career))
			world._restore_actor("rival", world.rival_actor)
			_check("%s finale rival exposes authored bow" % career,
				world._set_rival_pose("bow")
				and world.rival_actor.texture.resource_path.ends_with("rival_%s_bow.png" % career))
			world._restore_actor("rival", world.rival_actor)
			_check("%s rival pose restores the idle texture" % career,
				world.rival_actor.texture == idle_texture)
		if career == "chef":
			var player_rest: Dictionary = (world.actor_rests.get("player", {}) as Dictionary).duplicate()
			for _tap in range(20):
				world._bounce_actor(world.player_actor, 14.0)
			await create_timer(0.42).timeout
			_check("twenty rapid reactions return Roshan to her exact rest transform",
				_actor_matches_rest(world.player_actor, player_rest))
			if not stress_shot_out.is_empty():
				await _capture_viewport(stress_shot_out.path_join("rapid_input_rest.png"))
		var captain_scuffle := -1
		for mode_i in range(1, modes.size()):
			if modes[mode_i] == "bop" and mode_i < world._finale_start():
				captain_scuffle = mode_i
		_check("%s stages a bigger scuffle before the stage door" % career,
			captain_scuffle > 0 and captain_scuffle < world._finale_start()
			and float((world.phases[captain_scuffle] as Dictionary).get("goal", 0.0))
			> float((world.phases[0] as Dictionary).get("goal", 0.0)))
		var scuffle_free_finale := true
		for mode_i in range(world._finale_start(), modes.size()):
			scuffle_free_finale = scuffle_free_finale and modes[mode_i] != "bop"
		# detective's finale is the owner's ally-corner: the one career whose
		# job contest IS a shared scuffle (rival detective + Roshan vs captain)
		_check("%s keeps the stage finale for the job contest" % career,
			scuffle_free_finale or career == "detective")
		var backdrop := world.get_node_or_null("OperaCareerWorld2D/CareerWorldBackdrop") as OperaWorldBackdrop2D
		_check("%s starts in its job world, off the proscenium" % career,
			backdrop != null and not backdrop.stage_mode)
		_check("%s paints the supplied codex career world" % career,
			backdrop != null and backdrop.world_tiles.size() == 4)
		_check("%s owns a complete on-stage tile set" % career,
			backdrop != null and backdrop.stage_tiles.size() == 4)
		if not rival_shot_out.is_empty() and not cooperative:
			await _capture_rival_states(world, career, backdrop)
		var widgets_complete := true
		var widgets_causal := true
		var target_lock_checked := false
		var widget_count := 0
		for phase_number in range(world.phases.size()):
			var phase_dict: Dictionary = world.phases[phase_number]
			var template := world._widget_template(phase_dict)
			if template.is_empty():
				continue
			widget_count += 1
			total_widget_count += 1
			var widget_path := "res://assets/opera/worlds/widgets/widget_%s_%s.png" % [template, career]
			widgets_complete = widgets_complete and ResourceLoader.exists(widget_path)
			var context := "%s_%s" % [template, career]
			var before_progress := world.phase_progress
			world.surface.configure(String(phase_dict.get("mode", "tap")), Color.WHITE,
				world.choice_target, context)
			world.surface._process(0.8)
			widgets_causal = widgets_causal and is_equal_approx(world.phase_progress, before_progress) \
				and is_equal_approx(world.surface.widget_fill, 0.0) \
				and world.surface.demo_active
			world.surface.set_fill(1.0)
			widgets_causal = widgets_causal and not world.surface.completion_accepted
			world.surface.accept_completion()
			widgets_causal = widgets_causal and world.surface.completion_accepted
			world.surface.restart_demo()
			world.surface.note_input()
			widgets_causal = widgets_causal and not world.surface.demo_active \
				and world.surface.input_started
			if template == "target" and not target_lock_checked:
				world.surface.set_block_signals(true)
				var stamp_at := world.surface.size * Vector2(0.31, 0.62)
				var marks_before := world.surface.tap_marks.size()
				world.surface._press(stamp_at)
				world.surface._release(stamp_at)
				widgets_causal = widgets_causal \
					and world.surface.tap_marks.size() == marks_before + 1 \
					and (world.surface.tap_marks.back() as Vector2).is_equal_approx(stamp_at)
				world.surface.set_block_signals(false)
				target_lock_checked = true
			if not widget_shot_out.is_empty():
				await _capture_widget_states(world, career, phase_number, phase_dict, template)
		# detective (wander-and-talk crown hunt) and racer (3D kart lap) have
		# no card widgets by design — their beats play on the stage itself
		_check("%s loads every diegetic phase widget" % career,
			widgets_complete and (widget_count > 0 or career in ["detective", "racer"]))
		_check("%s widgets remain input-causal with owner-gated completion" % career,
			widgets_causal)
		world._show_phase()
		_check("%s loads the Storybook task frame and station beacon" % career,
			world.task_frame_texture != null and world.station_marker_texture != null)
		_check("%s loads the authored magnifier prop" % career,
			world.magnifier_texture != null)
		var captain_stage_seen := false
		if career == "detective":
			var original_phase_count := world.phases.size()
			while world.phase_index < world._finale_start():
				if world.phase_index == world.steal_index and backdrop != null:
					captain_stage_seen = captain_stage_seen or backdrop.stage_mode
				world._on_gesture("probe", 100.0, 1.0)
				act._process(0.05)
			_check("detective imp enters only for the final shared mystery",
				world.rival_actor.visible and world.in_competition_finale() and act.competition.active)
			act.competition.round_elapsed = float(act.competition.spec.get("par_time", 40.0)) * 1.2
			act._process(0.1)
			_check("2D detective rival can solve at the 40-second clock",
				world.reveal_t > 0.0 and not world.active)
			world.reveal_t = 0.01
			world._process(0.02)
			_check("2D detective shows the answer then restarts the same guided case",
				world.guided and world.active and world.phase_index == world._finale_start()
				and world.phases.size() == original_phase_count
				and act.competition.retries == 1)

		var saw_finale_imp := world.rival_actor.visible and world.in_competition_finale()
		var rival_hid_through_scuffles := true
		var guard := 0
		while act.state == "play" and guard < 80:
			rival_hid_through_scuffles = rival_hid_through_scuffles \
				and (cooperative or world.in_competition_finale() or not world.rival_actor.visible)
			if world.phase_index == world.steal_index and backdrop != null:
				captain_stage_seen = captain_stage_seen or backdrop.stage_mode
			world._on_gesture("probe", 100.0, 1.0)
			act._process(0.05)
			await process_frame
			guard += 1
			saw_finale_imp = saw_finale_imp or (world.rival_actor.visible and world.in_competition_finale())
		_check("%s brings in its dressed finale partner" % career, saw_finale_imp)
		_check("%s keeps the rival away from both imp scuffles" % career, rival_hid_through_scuffles)
		_check("%s brawls the captain at the stage door" % career, captain_stage_seen)
		if career == "nursery":
			_check("nursery curtain call records cooperative care",
				bool(act.performance_result.get("cooperative", false)))
		_check("%s finishes on the proscenium stage" % career,
			backdrop != null and backdrop.stage_mode)
		_check("%s can complete through one-finger phases" % career,
			act.state == "won" and is_equal_approx(act.competition.player_progress, 1.0))
		_check("%s awards a graded crowd reaction" % career,
			not act.performance_result.is_empty()
			and int(act.performance_result.get("tier", 0)) >= 1
			and int(act.performance_result.get("tier", 0)) <= 3)
		act.cancel()
		await process_frame
		if main.touch_ui != null:
			_check("%s restores the touch layer on exit" % career,
				main.touch_ui.visible == touch_before)

	var reentry_config: Dictionary = {}
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("costume", "")) == "chef":
			reentry_config = source.duplicate(true)
			reentry_config["force_2d"] = true
			break
	var reentry_clean := not reentry_config.is_empty()
	for cycle in range(5):
		var touch_before := main.touch_ui.visible if main.touch_ui != null else false
		var reentry_act := OperaAct.new()
		get_root().add_child(reentry_act)
		reentry_act.start(main, reentry_config, Callable())
		await process_frame
		var reentry_world := reentry_act.career_world_2d
		reentry_clean = reentry_clean and reentry_act.use_career_world_2d \
			and reentry_world != null and is_instance_valid(reentry_world)
		if reentry_world != null and is_instance_valid(reentry_world):
			reentry_world._bounce_actor(reentry_world.player_actor, 16.0)
			if reentry_world.rival_actor != null:
				reentry_world._set_rival_pose("taunt")
			await process_frame
			if not stress_shot_out.is_empty():
				await _capture_viewport(stress_shot_out.path_join(
					"early_reentry_%02d.png" % (cycle + 1)))
		reentry_act.cancel()
		await process_frame
		await process_frame
		reentry_clean = reentry_clean and not is_instance_valid(reentry_act) \
			and get_root().find_children("*", "OperaCareerWorld2D", true, false).is_empty()
		if main.touch_ui != null:
			reentry_clean = reentry_clean and main.touch_ui.visible == touch_before
	_check("five early exits and re-entries free every Opera world and restore touch",
		reentry_clean)

	_check("all thirteen career jobs were exercised", show_count == 13)
	# 46 after the 2026-08-04 logical rebuild: the ping-pong meters, the
	# scatter-tap boards and the racer widget set were retired in favour of
	# grammars that ARE the job (oven, tilt-pour, pipe dream, crown hunt,
	# echo song, 3D kart lap). Detective and the kart beat carry no card.
	_check("every art-backed career widget was exercised", total_widget_count == 46)
	if bad == 0:
		print("OPERA2D|result: ALL OK")
		quit()
	else:
		print("OPERA2D|result: %d FAIL" % bad)
		quit(1)


func _capture_viewport(path: String) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error := image.save_png(path)
	_check("saved review capture %s" % path.get_file(), error == OK)


func _capture_control(control: Control, path: String) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var viewport := get_root().get_viewport()
	var image: Image = viewport.get_texture().get_image()
	var visible_size := viewport.get_visible_rect().size
	var image_scale := Vector2(image.get_width(), image.get_height()) / visible_size
	var global_rect := control.get_global_rect()
	var region := Rect2i(
		Vector2i(global_rect.position * image_scale),
		Vector2i(global_rect.size * image_scale)
	)
	region = region.intersection(Rect2i(Vector2i.ZERO, image.get_size()))
	var crop := image.get_region(region)
	var error := crop.save_png(path)
	_check("saved review capture %s" % path.get_file(), error == OK)


func _capture_rival_states(world: OperaCareerWorld2D, career: String,
		backdrop: OperaWorldBackdrop2D) -> void:
	world._clear_stage_combat()
	world._restore_stage_actors()
	backdrop.set_stage(true)
	world._set_finale_visible(true)
	world.action_panel.visible = false
	world._set_rival_pose("taunt")
	world._bounce_actor(world.rival_actor, 14.0, 0.46)
	await create_timer(0.16).timeout
	await _capture_viewport(rival_shot_out.path_join("%s_rival_taunt.png" % career))
	world._restore_actor("rival", world.rival_actor)
	world._set_rival_pose("bow")
	world._bounce_actor(world.rival_actor, 10.0, 0.58)
	await create_timer(0.20).timeout
	await _capture_viewport(rival_shot_out.path_join("%s_rival_bow.png" % career))
	world._restore_actor("rival", world.rival_actor)
	backdrop.set_stage(false)
	world._set_finale_visible(false)


func _capture_scuffle_sequences(world: OperaCareerWorld2D, career: String) -> void:
	await _capture_one_scuffle(world, career, false)
	await _capture_one_scuffle(world, career, true)
	world.phase_index = 0
	world.phase_progress = 0.0
	world._show_phase()
	world.phase_gap = 0.0


func _capture_one_scuffle(world: OperaCareerWorld2D, career: String,
		captain_scuffle: bool) -> void:
	var target_phase := world.steal_index if captain_scuffle else 0
	world.phase_index = target_phase
	world.phase_progress = 0.0
	world._show_phase()
	world.phase_gap = 0.0
	var label := "captain" if captain_scuffle else "opening"
	var shot := 0
	while shot < 24 and world.phase_index == target_phase:
		await create_timer(0.16).timeout
		await _capture_viewport(scuffle_shot_out.path_join(
			"%s_%s_%02d.png" % [career, label, shot + 1]))
		var live_imp: Dictionary = {}
		for imp: Dictionary in world.combat_imps:
			if not bool(imp.get("popped", false)):
				live_imp = imp
				break
		if live_imp.is_empty():
			if world.phase_advance_pending:
				world._advance_completed_phase()
			break
		var center: Vector2 = live_imp.get("center", Vector2(640.0, 440.0))
		world.swipe_stroke += 1
		world._combat_strike(center, center)
		shot += 1
	if world.phase_advance_pending:
		await _capture_viewport(scuffle_shot_out.path_join(
			"%s_%s_%02d.png" % [career, label, shot + 1]))
		world._advance_completed_phase()


func _capture_widget_states(world: OperaCareerWorld2D, career: String,
		phase_number: int, phase: Dictionary, template: String) -> void:
	var surface := world.surface
	var mode := String(phase.get("mode", "tap"))
	var context := "%s_%s" % [template, career]
	world.action_panel.visible = true
	world.action_panel.position = Vector2(420.0, 154.0)
	surface.visible = true
	surface.configure(mode, Color(0.92, 0.58, 0.82), world.choice_target, context)
	match String(phase.get("dir", "")):
		"down": surface.swipe_dir = Vector2.DOWN
		"up": surface.swipe_dir = Vector2.UP
	var prefix := "%s_%02d_%s" % [career, phase_number + 1, template]
	surface.demo_t = 0.92
	surface.set_timing_position(0.18)
	await _capture_control(surface, widget_shot_out.path_join("%s_idle_demo.png" % prefix))

	surface.note_input()
	surface.held = mode == "hold"
	surface.set_fill(0.45)
	surface.set_timing_position(0.50)
	surface.crank_rotation = 0.72
	surface.feedback_anchor = surface.size * Vector2(0.5, 0.68)
	surface.feedback_position = 0.50
	if mode in ["tap", "choice", "timing"]:
		surface.note_result(true)
	if template == "target":
		surface.tap_marks = [surface.size * Vector2(0.42, 0.58)]
	await _capture_control(surface, widget_shot_out.path_join("%s_active_input.png" % prefix))

	surface.feedback_t = 0.0
	surface.held = mode == "hold"
	surface.set_fill(0.90)
	surface.set_timing_position(0.68)
	surface.crank_rotation = 1.34
	await _capture_control(surface, widget_shot_out.path_join("%s_near_completion.png" % prefix))

	surface.held = false
	surface.set_fill(1.0)
	surface.accept_completion()
	await _capture_control(surface, widget_shot_out.path_join("%s_accepted_completion.png" % prefix))


func _visible_card_count(cards: Array) -> int:
	var count := 0
	for card: Button in cards:
		if card.visible:
			count += 1
	return count


func _actor_matches_rest(actor: TextureRect, rest: Dictionary) -> bool:
	return actor.position.is_equal_approx(rest.get("position", actor.position) as Vector2) \
		and actor.size.is_equal_approx(rest.get("size", actor.size) as Vector2) \
		and actor.scale.is_equal_approx(rest.get("scale", actor.scale) as Vector2) \
		and is_equal_approx(actor.rotation, float(rest.get("rotation", actor.rotation))) \
		and actor.modulate.is_equal_approx(rest.get("modulate", actor.modulate) as Color) \
		and actor.flip_h == bool(rest.get("flip_h", actor.flip_h)) \
		and actor.texture == (rest.get("texture", actor.texture) as Texture2D)


func _check(label: String, condition: bool) -> void:
	if condition:
		print("OPERA2D|OK|", label)
	else:
		bad += 1
		print("OPERA2D|FAIL|", label)
