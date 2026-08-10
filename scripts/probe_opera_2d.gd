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
var stress_shot_out := ""
var lobby_shot_out := ""
var detective_shot_out := ""

const BOXING_MODES: Array[String] = [
	"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
]
const BOXING_GOALS: Array[float] = [2.0, 4.0, 3.0, 6.0, 1.0]
const BOXING_VOICES: Array[String] = [
	"op_boxer_work", "op_boxer_jab", "op_boxer_duck",
	"op_boxer_bell_chase", "op_boxer_belt",
]

const DIRECT_SURFACE_CONTRACTS := {
	"detective": {
		"CASE BOARD": {"mode": "clue_board", "goal": 3.0, "context": "clue_board"},
		"CROWN": {"mode": "crown_chest", "goal": 1.0, "context": "crown_chest"},
	},
	"farmer": {
		"PLANT": {"mode": "garden_plant", "goal": 5.0, "context": "garden_plant"},
	},
	"magician": {
		"VANISH": {"mode": "hold", "goal": 3.8, "context": "magic_vanish"},
		"CABINET": {"mode": "magic_cabinet", "goal": 1.0, "context": "magic_cabinet"},
	},
	"nursery": {
		"WASH HANDS": {"mode": "hold", "goal": 3.4, "context": "nursery_wash"},
		"FEED": {"mode": "hold", "goal": 4.0, "context": "nursery_feed"},
		"BURP": {"mode": "tap", "goal": 4.0, "context": "nursery_burp"},
		"BEDTIME": {"mode": "swipe", "goal": 3.0, "context": "nursery_bedtime"},
	},
}

const RETAINED_ROTATIONS := {
	"chef": "STIR",
	"ballerina": "TWIRL",
	"astronaut": "VALVE",
	"magician": "PORTAL",
}


func _init() -> void:
	widget_shot_out = OS.get_environment("OPERA_WIDGET_SHOT_OUT").strip_edges()
	rival_shot_out = OS.get_environment("OPERA_RIVAL_SHOT_OUT").strip_edges()
	stress_shot_out = OS.get_environment("OPERA_STRESS_SHOT_OUT").strip_edges()
	lobby_shot_out = OS.get_environment("OPERA_LOBBY_SHOT_OUT").strip_edges()
	detective_shot_out = OS.get_environment("OPERA_DETECTIVE_SHOT_OUT").strip_edges()
	if not widget_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(widget_shot_out)
	if not rival_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(rival_shot_out)
	if not stress_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(stress_shot_out)
	if not lobby_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(lobby_shot_out)
	if not detective_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(detective_shot_out)
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
		var lobby_stage := lobby.stage as Control
		_check("Opera lobby uses one centered uniform 1280 by 720 stage",
			lobby_stage != null
			and lobby_stage.size.is_equal_approx(StorybookUI.CANVAS_SIZE)
			and is_equal_approx(lobby_stage.scale.x, lobby_stage.scale.y))
		var buttons_are_pictures := lobby.boss_button.text.is_empty()
		var touch_targets_safe := lobby.boss_button.size.x >= StorybookUI.MIN_TOUCH.x \
			and lobby.boss_button.size.y >= StorybookUI.MIN_TOUCH.y
		var cards_unclipped := not lobby.boss_button.clip_contents
		var crests_complete := true
		var actors_fully_framed := true
		var actors_use_audited_atlases := true
		var active_animators := 0
		for tab: Button in lobby.floor_tabs:
			buttons_are_pictures = buttons_are_pictures and tab.text.is_empty()
			touch_targets_safe = touch_targets_safe \
				and tab.size.x >= StorybookUI.MIN_TOUCH.x \
				and tab.size.y >= StorybookUI.MIN_TOUCH.y
			var floor_crest := tab.get_node_or_null("FloorCrest") as TextureRect
			crests_complete = crests_complete and floor_crest != null \
				and floor_crest.texture != null
		var boss_crest := lobby.boss_button.get_node_or_null("BossCrest") as TextureRect
		crests_complete = crests_complete and boss_crest != null and boss_crest.texture != null
		for card: Button in lobby.card_buttons:
			buttons_are_pictures = buttons_are_pictures and card.text.is_empty()
			cards_unclipped = cards_unclipped and not card.clip_contents
			if not card.visible:
				continue
			touch_targets_safe = touch_targets_safe \
				and card.size.x >= StorybookUI.MIN_TOUCH.x \
				and card.size.y >= StorybookUI.MIN_TOUCH.y
			var actor := card.get_node_or_null("RoshanActor") as TextureRect
			var crest := card.get_node_or_null("CareerCrest") as TextureRect
			crests_complete = crests_complete and crest != null and crest.texture != null
			actors_fully_framed = actors_fully_framed and actor != null \
				and actor.texture != null \
				and actor.position.x >= 0.0 and actor.position.y >= 0.0 \
				and actor.position.x + actor.size.x <= card.size.x \
				and actor.position.y + actor.size.y <= card.size.y \
				and crest.position.y >= actor.position.y + actor.size.y
			var actor_frame := actor.texture as AtlasTexture if actor != null else null
			actors_use_audited_atlases = actors_use_audited_atlases \
				and actor_frame != null and actor_frame.atlas != null \
				and actor_frame.atlas.resource_path.contains("/actors/animation/roshan_")
			if bool(card.get_meta("animator_active", false)):
				active_animators += 1
		var back_button := lobby.stage.get_node_or_null("OperaBackButton") as Button
		buttons_are_pictures = buttons_are_pictures and back_button != null \
			and back_button.text.is_empty()
		_check("Opera lobby keeps every Button visually text-free", buttons_are_pictures)
		_check("Opera lobby cards and finale never clip their pictures", cards_unclipped)
		_check("every visible Opera choice has its approved pictorial crest", crests_complete)
		_check("every Roshan portrait is fully framed above its crest", actors_fully_framed)
		_check("every visible menu portrait uses its audited full-tail atlas",
			actors_use_audited_atlases)
		_check("every Opera lobby touch target is at least 110 pixels", touch_targets_safe)
		_check("only the highlighted career card owns the active animator",
			active_animators == 1 and lobby.active_actor_animator != null
			and lobby.active_actor_animator.has_animation)
		_check("floor finale is gated by the four job stars", bool(lobby.boss_button.get_meta("locked", false)))
		if not lobby_shot_out.is_empty():
			await _capture_viewport(lobby_shot_out.path_join("opera_lobby_floor_1.png"))
		lobby.refresh((1 << 4) | (1 << 9), 2)
		_check("Grand Gallery expands to five direct job cards", _visible_card_count(lobby.card_buttons) == 5)
		_check("Nursery Nurse is displayed as job twelve before Pop Star",
			int(lobby.card_buttons[3].get_meta("act_index", -1)) == 15
			and int(lobby.card_buttons[4].get_meta("act_index", -1)) == 13)
		_check("five Grand Gallery jobs gate the finale", bool(lobby.boss_button.get_meta("locked", false)))
		if not lobby_shot_out.is_empty():
			await _capture_viewport(lobby_shot_out.path_join("opera_lobby_floor_3.png"))
		lobby.refresh(0, 0)
	house._leave_early()
	await process_frame
	OS.set_environment("OPERA_FORCE_2D_LOBBY", "0")
	if main.touch_ui != null:
		_check("2D lobby restores the touch layer on exit", main.touch_ui.visible == lobby_touch_before)
	_check("boxer keeps stable Opera save bit 128",
		OperaHouse.ACTS.size() > 7
		and String((OperaHouse.ACTS[7] as Dictionary).get("costume", "")) == "boxer"
		and (1 << 7) == 128)
	var show_count := 0
	var total_widget_count := 0
	var direct_surface_count := 0
	var total_circle_count := 0
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
		_check("%s has a multi-phase job game" % career, world.phases.size() >= 3)
		_check("%s starts without passive progress" % career,
			is_equal_approx(world.progress(), 0.0))
		var modes: Array[String] = []
		for phase_dict: Dictionary in world.phases:
			modes.append(String(phase_dict.get("mode", "")))
		_check("%s opens with its job verb, not the shared brawl" % career,
			modes.size() > 0 and modes[0] != "bop")
		_check("%s uses real costume-frame animation" % career,
			world.player_animator != null and world.player_animator.has_animation
			and world.player_animator.current_animation == "work")
		if world.player_animator != null and world.player_animator.has_animation:
			var frame_before := world.player_animator.current_frame
			# Work runs at 7 fps. A 0.5s sample can advance 3 or 4 frames
			# depending on the accumulated fraction and wrap onto the same cell.
			# 0.2s always crosses at least one boundary and cannot wrap four.
			world.player_animator._process(0.2)
			_check("%s costume atlas advances frames" % career,
				world.player_animator.current_frame != frame_before)
		var expected_signature := {
			"chef": "oven", "detective": "lens", "ballerina": "dance_sequence",
			"candymaker": "candy_sort", "doctor": "xray_scan", "farmer": "farm_lob",
			"boxer": "boxing_guide", "magician": "magic_cabinet", "painter": "paint_reveal",
			"astronaut": "pipe", "racer": "kart", "nursery": "catch", "popstar": "echo",
		}
		_check("%s contains its signature mechanic" % career,
			modes.has(String(expected_signature.get(career, ""))))
		if career == "boxer":
			_exercise_boxing_surface(world, act, modes)
		if career == "farmer":
			var picnic_phase: Dictionary = world.phases[3]
			var picnic_anchors: Array = OperaGestureSurface.TARGET_ANCHORS.get(
				"target_farmer", [])
			_check("farmer PICNIC gives one unique snack to each of three piggies",
				String(picnic_phase.get("name", "")) == "PICNIC"
				and is_equal_approx(float(picnic_phase.get("goal", 0.0)), 3.0)
				and picnic_anchors.size() == 3)
		var direct_contracts: Dictionary = DIRECT_SURFACE_CONTRACTS.get(career, {})
		for direct_phase: Dictionary in world.phases:
			var direct_name := String(direct_phase.get("name", ""))
			if not direct_contracts.has(direct_name):
				continue
			var direct_contract: Dictionary = direct_contracts[direct_name]
			var direct_mode := String(direct_phase.get("mode", ""))
			var requested_context := String(direct_phase.get("visual_context", ""))
			world.surface.configure(direct_mode, Color.WHITE,
				world.choice_target, requested_context)
			var direct_ok := direct_phase.has("widget") \
				and String(direct_phase.get("widget", "missing")).is_empty() \
				and world._widget_template(direct_phase).is_empty() \
				and direct_mode == String(direct_contract.get("mode", "")) \
				and is_equal_approx(float(direct_phase.get("goal", 0.0)),
					float(direct_contract.get("goal", -1.0))) \
				and world.surface.mode == direct_mode \
				and world.surface.visual_context == String(direct_contract.get("context", ""))
			if direct_name == "BEDTIME":
				direct_ok = direct_ok and String(direct_phase.get("dir", "")) == "down"
			_check("%s %s uses its direct specialist surface" % [career, direct_name],
				direct_ok)
			direct_surface_count += 1
		var retained_rotation_ok := not RETAINED_ROTATIONS.has(career)
		for pacing_phase: Dictionary in world.phases:
			if String(pacing_phase.get("mode", "")) != "circle":
				continue
			total_circle_count += 1
			var rotations := float(pacing_phase.get("goal", 0.0))
			_check("%s %s finishes in 1.5 to 2.2 rotations" \
				% [career, String(pacing_phase.get("name", "circle"))],
				rotations >= 1.5 and rotations <= 2.2)
			if String(pacing_phase.get("name", "")) \
					== String(RETAINED_ROTATIONS.get(career, "")):
				retained_rotation_ok = true
		if RETAINED_ROTATIONS.has(career):
			_check("%s retains its thematic rotation verb" % career,
				retained_rotation_ok)
		# Every accepted generic choice must immediately cue its newly selected
		# answer. Magician TRACK spends the same cue on a fresh hat shuffle.
		for choice_phase_index in range(world.phases.size()):
			var choice_phase: Dictionary = world.phases[choice_phase_index]
			if String(choice_phase.get("mode", "")) != "choice":
				continue
			world.phase_index = choice_phase_index
			world.phase_progress = 0.0
			world.phase_gap = 0.0
			world.phase_advance_pending = false
			world.reveal_t = 0.0
			world.task_open = true
			world.choice_target = 0
			var choice_template := world._widget_template(choice_phase)
			var choice_context := "%s_%s" % [choice_template, career] \
				if not choice_template.is_empty() else ""
			if choice_phase.has("visual_context"):
				choice_context = String(choice_phase.get("visual_context", choice_context))
			world.surface.configure("choice", Color.WHITE, 0, choice_context)
			world.surface.choice_flash = 0.0
			world.surface.shuffle_t = 0.0
			var previous_choice := world.choice_target
			world._on_gesture("choice", 1.0, 1.0)
			_check("%s %s visibly cues its next correct choice" \
				% [career, String(choice_phase.get("name", "choice"))],
				world.choice_target != previous_choice
				and world.surface.target_choice == world.choice_target
				and world.surface.choice_flash > 0.0)
			if career == "magician":
				_check("magician TRACK starts a fresh shuffle after every accepted hat",
					world.surface.shuffle_t > 0.0
					and world.surface.shuffle_from == previous_choice)
		world.phase_index = 0
		world.phase_progress = 0.0
		world.phase_advance_pending = false
		world.phase_complete_t = 0.0
		if career == "detective":
			var case_voice_ok := false
			var crown_voice_ok := false
			for detective_phase: Dictionary in world.phases:
				if String(detective_phase.get("name", "")) == "CASE BOARD":
					case_voice_ok = String(detective_phase.get("vo", "")) \
						== "op_detective_match"
				if String(detective_phase.get("name", "")) == "CROWN":
					crown_voice_ok = String(detective_phase.get("vo", "")) \
						== "op_detective_name"
			_check("detective CASE BOARD reuses the exact matching voice cue",
				case_voice_ok)
			_check("detective CROWN uses its exact spotlight voice cue",
				crown_voice_ok)
			_check("detective opens with theft then search voice recordings",
				OperaCareerWorld2D.DETECTIVE_INTRO_LINES.size() == 2
				and String(OperaCareerWorld2D.DETECTIVE_INTRO_LINES[0].get("vo", ""))
					== "op_detective_steal"
				and String(OperaCareerWorld2D.DETECTIVE_INTRO_LINES[1].get("vo", ""))
					== "op_detective_search")
		if career == "ballerina":
			var watch_voice_count := 0
			for ballerina_phase: Dictionary in world.phases:
				if String(ballerina_phase.get("name", "")) in ["PHRASE", "POSE"] \
						and String(ballerina_phase.get("vo", "")) == "op_ballerina_watch":
					watch_voice_count += 1
			_check("ballerina demonstration and hold reuse the watch voice cue",
				watch_voice_count == 2)
		if career == "candymaker":
			var syrup_goal := 0.0
			for candy_phase: Dictionary in world.phases:
				if String(candy_phase.get("name", "")) == "SYRUP":
					syrup_goal = float(candy_phase.get("goal", 0.0))
			_check("candymaker SYRUP requires the full five-point pour",
				is_equal_approx(syrup_goal, 5.0))
		if career in ["doctor", "farmer"]:
			var station_phase_name := "X-RAY" if career == "doctor" else "TOSS"
			var expected_station_id := "exam_booth" if career == "doctor" else "hay_bales"
			var station_phase_index := -1
			for station_phase_i in range(world.phases.size()):
				if String((world.phases[station_phase_i] as Dictionary).get("name", "")) \
						== station_phase_name:
					station_phase_index = station_phase_i
					break
			var resolved_station_id := ""
			var resolved_station_index := int(world.station_for_phase.get(
				station_phase_index, -1))
			if resolved_station_index >= 0 \
					and resolved_station_index < world.station_list.size():
				resolved_station_id = String(world.station_list[resolved_station_index].get(
					"id", ""))
			_check("%s %s resolves to the thematic %s landmark" \
				% [career, station_phase_name, expected_station_id],
				resolved_station_id == expected_station_id)
		if career == "nursery":
			var catch_phase: Dictionary = {}
			for nursery_phase: Dictionary in world.phases:
				if String(nursery_phase.get("name", "")) == "CATCH BABIES":
					catch_phase = nursery_phase
					break
			world._apply_panel_layout(catch_phase)
			var catch_rect := Rect2(world.nursery_catch.position,
				world.nursery_catch.size)
			var fill_rect := Rect2(world.phase_fill.position, world.phase_fill.size)
			_check("nursery catch surface stays above and clear of its progress bar",
				not catch_phase.is_empty()
				and catch_rect.intersection(fill_rect).get_area() <= 0.01
				and catch_rect.position.x >= 0.0 and catch_rect.position.y >= 0.0
				and catch_rect.end.x <= world.action_panel.size.x
				and catch_rect.end.y <= world.action_panel.size.y)
		_check("%s avoids copied combat phases" % career,
			modes.count("bop") == 0 and world.steal_index < 0
			and world.combat_imps.is_empty())
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
		var copied_combat_free_finale := true
		for mode_i in range(world._finale_start(), modes.size()):
			copied_combat_free_finale = copied_combat_free_finale and modes[mode_i] != "bop"
		_check("%s keeps the stage finale for the job contest" % career,
			copied_combat_free_finale)
		var backdrop := world.get_node_or_null("OperaCareerWorld2D/CareerWorldBackdrop") as OperaWorldBackdrop2D
		_check("%s starts in its job world, off the proscenium" % career,
			backdrop != null and not backdrop.stage_mode)
		_check("%s paints the supplied codex career world" % career,
			backdrop != null and backdrop.world_tiles.size() == 4)
		_check("%s owns a complete on-stage tile set" % career,
			backdrop != null and backdrop.stage_tiles.size() == 4)
		if not rival_shot_out.is_empty() and not cooperative and career != "boxer":
			await _capture_rival_states(world, career, backdrop)
		var widgets_complete := true
		var widgets_causal := true
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
			var phase_mode := String(phase_dict.get("mode", "tap"))
			var before_progress := world.phase_progress
			world.surface.configure(phase_mode, Color.WHITE,
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
			if template == "target" and phase_mode == "tap":
				# The owner-gate check above intentionally leaves the surface in its
				# achieved hold. Re-arm the phase before driving its real target so
				# completion_accepted cannot make this input assertion a false failure.
				world.surface.configure(phase_mode, Color.WHITE,
					world.choice_target, context)
				world.surface.set_block_signals(true)
				if career == "painter":
					var stamp_at := world.surface.size * Vector2(0.31, 0.62)
					var marks_before := world.surface.tap_marks.size()
					world.surface._press(stamp_at)
					world.surface._release(stamp_at)
					var painter_free := not OperaGestureSurface.TARGET_ANCHORS.has(context) \
						and world.surface.tap_marks.size() == marks_before + 1 \
						and (world.surface.tap_marks.back() as Vector2).is_equal_approx(stamp_at)
					_check("painter STAMPS preserves true free finger placement",
						painter_free)
					widgets_causal = widgets_causal and painter_free
				else:
					var anchors: Array = OperaGestureSurface.TARGET_ANCHORS.get(context, [])
					var anchored_ok := not anchors.is_empty() \
						and world.surface.target_placed.size() == anchors.size()
					if anchored_ok:
						var anchor: Vector2 = anchors[0]
						var target_at := world.surface.size * anchor
						world.surface._press(target_at)
						world.surface._release(target_at)
						anchored_ok = bool(world.surface.target_placed[0])
					_check("%s %s places pieces on authored surface anchors" \
						% [career, String(phase_dict.get("name", "target"))],
						anchored_ok)
					widgets_causal = widgets_causal and anchored_ok
				world.surface.set_block_signals(false)
			elif phase_mode == "xray_scan":
				# A target-family backdrop no longer implies free-placement taps.
				# Drive Doctor's actual drag grammar with signals blocked so this
				# integration check cannot mutate the live career phase.
				world.surface.configure(phase_mode, Color.WHITE,
					world.choice_target, context)
				world.surface.set_block_signals(true)
				var sore_spot := world.surface._xray_target_center(0)
				world.surface._press(sore_spot)
				world.surface._release(sore_spot)
				widgets_causal = widgets_causal and world.surface.xray_found_count == 0
				world.surface._press(world.surface._xray_home_point())
				world.surface._drag(sore_spot)
				world.surface._release(sore_spot)
				widgets_causal = widgets_causal and world.surface.xray_found_count == 1
				world.surface.set_block_signals(false)
			elif phase_mode == "farm_lob":
				# The farmer card is release-driven: a weak release loops safely;
				# only the completed arc changes its deterministic landing state.
				world.surface.configure(phase_mode, Color.WHITE,
					world.choice_target, context)
				world.surface.set_block_signals(true)
				var basket := world.surface._farm_anchor_point()
				world.surface._press(basket)
				world.surface._release(basket)
				world.surface._farm_tick(OperaGestureSurface.FARM_FLIGHT_DURATION + 0.01)
				widgets_causal = widgets_causal and world.surface.farm_landed == 0 \
					and world.surface.farm_loops == 1
				world.surface._farm_tick(0.20)
				world.surface._press(world.surface._farm_anchor_point())
				world.surface._drag(world.surface._farm_demo_pull_point())
				world.surface._release(world.surface._farm_demo_pull_point())
				world.surface._farm_tick(OperaGestureSurface.FARM_FLIGHT_DURATION + 0.01)
				widgets_causal = widgets_causal and world.surface.farm_landed == 1
				world.surface.set_block_signals(false)
			if not widget_shot_out.is_empty():
				await _capture_widget_states(world, career, phase_number, phase_dict, template)
		# Direct specialist surfaces deliberately have no generic widget family;
		# those contracts are exercised above instead of requiring reskin assets.
		_check("%s loads every diegetic phase widget" % career,
			widgets_complete and (widget_count > 0 or career in ["boxer", "detective", "racer"]))
		_check("%s widgets remain input-causal with owner-gated completion" % career,
			widgets_causal)
		world._show_phase()
		_check("%s loads the Storybook task frame and station beacon" % career,
			world.task_frame_texture != null and world.station_marker_texture != null)
		_check("%s loads the authored magnifier prop" % career,
			world.magnifier_texture != null)
		if world.action_panel.visible and world.player_actor.visible:
			var panel_rect := Rect2(world.action_panel.position, world.action_panel.size)
			var actor_rect := Rect2(world.player_actor.position,
				world.player_actor.size * world.player_actor.scale).grow(24.0)
			_check("%s task card never covers animated Roshan" % career,
				panel_rect.intersection(actor_rect).get_area() <= 0.01)
		if career == "detective":
			_check("detective lens is enlarged around its real glass centre",
				OperaCareerWorld2D.LENS_GRAPHIC_SIZE.x >= 400.0
				and OperaCareerWorld2D.LENS_RADIUS >= 125.0)
			_check("detective lens samples the painted room at true magnification",
				world.lens_zoom_surface != null and world.lens_zoom_surface.visible
				and world.lens_zoom_material != null
				and float(world.lens_zoom_material.get_shader_parameter("magnification")) >= 1.7
				and world.lens_zoom_material.shader.code.contains("hint_screen_texture"))
			_check("detective room exposes many safe inspection targets",
				world.lens_room_objects.size() >= 16)
			var full_glass_on_screen := true
			for requested_lens: Vector2 in [Vector2(-1000.0, -1000.0),
					Vector2(10000.0, 10000.0)]:
				world._set_lens_position(requested_lens)
				full_glass_on_screen = full_glass_on_screen \
					and world.lens_pos.x - OperaCareerWorld2D.LENS_RADIUS >= 0.0 \
					and world.lens_pos.y - OperaCareerWorld2D.LENS_RADIUS >= 0.0 \
					and world.lens_pos.x + OperaCareerWorld2D.LENS_RADIUS \
						<= StorybookUI.CANVAS_SIZE.x \
					and world.lens_pos.y + OperaCareerWorld2D.LENS_RADIUS \
						<= StorybookUI.CANVAS_SIZE.y
			_check("detective clamp keeps the complete functional glass onscreen",
				full_glass_on_screen)
			var every_clue_reachable := not world.lens_clues.is_empty()
			for clue: Vector2 in world.lens_clues:
				every_clue_reachable = every_clue_reachable \
					and world._clamped_lens_position(clue).distance_to(clue) \
					<= OperaCareerWorld2D.LENS_CLUE_CAPTURE_RADIUS
			_check("detective glass clamp reaches every shipping clue",
				every_clue_reachable)
			world._set_lens_position(Vector2(640.0, 400.0))
			world.lens_demo = true
			var demo_clue_index := world._next_unfound_lens_clue()
			var demo_distance_before := INF
			var demo_target := Vector2.ZERO
			if demo_clue_index >= 0:
				demo_target = world._clamped_lens_position(
					world.lens_clues[demo_clue_index])
				demo_distance_before = world.lens_pos.distance_to(demo_target)
			world._tick_lens(0.25)
			_check("detective wordless demo travels toward the next unresolved clue",
				demo_clue_index >= 0
				and world.lens_pos.distance_to(demo_target) < demo_distance_before)
			var search_progress_before := world.phase_progress
			var room_reactions_before := world.lens_room_reactions
			var first_room_object: Dictionary = world.lens_room_objects[0]
			_check("ordinary detective props react without solving the case",
				world._try_lens_room_object(first_room_object.get("pos", Vector2.ZERO))
				and world.lens_room_reactions == room_reactions_before + 1
				and is_equal_approx(world.phase_progress, search_progress_before))
			world.lens_demo = false
			world.lens_since_find = OperaCareerWorld2D.LENS_HINT_DELAY - 0.05
			world._tick_lens(0.10)
			_check("detective glistens one unfound clue after twelve quiet seconds",
				world.lens_hint_target >= 0
				and not world.lens_found[world.lens_hint_target])
			if not detective_shot_out.is_empty():
				world._set_lens_position(Vector2(518.0, 248.0))
				await process_frame
				await process_frame
				await _capture_viewport(detective_shot_out.path_join("detective_search_zoom_and_hint.png"))
			var original_phase_count := world.phases.size()
			while world.phase_index < world._finale_start():
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

		var saw_finale_imp := _finale_partner_present(world, career)
		var rival_hidden_before_finale := true
		var guard := 0
		while act.state == "play" and guard < 80:
			rival_hidden_before_finale = rival_hidden_before_finale \
				and (cooperative or world.in_competition_finale() or not world.rival_actor.visible)
			if career == "boxer":
				_drive_boxer_phase(world)
			else:
				world._on_gesture("probe", 100.0, 1.0)
			act._process(0.05)
			await process_frame
			guard += 1
			saw_finale_imp = saw_finale_imp or _finale_partner_present(world, career)
		_check("%s brings in its dressed finale partner" % career, saw_finale_imp)
		_check("%s keeps the rival hidden before its stage contest" % career,
			rival_hidden_before_finale)
		if career == "boxer":
			_check("boxer finale uses one specialist padded imp, then a safe curtain call",
				saw_finale_imp and world.combat_imps.is_empty()
				and world.rival_actor.visible and not world.action_panel.visible)
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
		var closing_boxing: OperaBoxingSurface = null
		var close_claim_started := true
		if career == "boxer" and world.surface is OperaBoxingSurface:
			closing_boxing = world.surface as OperaBoxingSurface
			closing_boxing.configure("boxing_jab", Color.WHITE)
			_boxing_touch(closing_boxing, 73, true, closing_boxing.glove_rest(0))
			close_claim_started = closing_boxing.touch_owner_snapshot().has(73)
		act.cancel()
		if closing_boxing != null:
			_check("boxer close clears live finger claims before freeing its surface",
				close_claim_started and closing_boxing.touch_owner_snapshot().is_empty()
				and not closing_boxing.held)
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
	# Boxer's five first-person glove beats own their complete presentation and
	# deliberately add no generic card. The remaining careers retain 36 shared
	# art-family cards and nine direct specialist/context surfaces.
	_check("all thirty-six art-family career widgets were exercised",
		total_widget_count == 36)
	_check("all nine direct specialist/context surfaces were exercised",
		direct_surface_count == 9)
	_check("all eight retained circle phases use the shortened rotation pacing",
		total_circle_count == 8)
	if bad == 0:
		print("OPERA2D|result: ALL OK")
		quit()
	else:
		print("OPERA2D|result: %d FAIL" % bad)
		quit(1)


func _boxing_touch(surface: OperaBoxingSurface, finger: int, pressed: bool,
		position: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.position = position
	event.pressed = pressed
	surface._gui_input(event)


func _boxing_drag(surface: OperaBoxingSurface, finger: int,
		position: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = position
	surface._gui_input(event)


func _exercise_boxing_surface(world: OperaCareerWorld2D, act: OperaAct,
		modes: Array[String]) -> void:
	var exact_modes := modes.size() == BOXING_MODES.size()
	for index in range(mini(modes.size(), BOXING_MODES.size())):
		exact_modes = exact_modes and modes[index] == BOXING_MODES[index]
	_check("boxer replaces every generic card and brawl with five glove modes",
		exact_modes and not modes.has("boxer_rhythm") and not modes.has("bop"))
	_check("boxer owns a full-stage dedicated two-glove surface",
		world.surface is OperaBoxingSurface
		and world.surface.name == "BoxingGloveSurface"
		and world.surface.position.is_equal_approx(Vector2.ZERO)
		and world.surface.size.is_equal_approx(Vector2(1280.0, 720.0))
		and world.station_list.is_empty() and not world.player_actor.visible
		and not world.rival_actor.visible)
	_check("boxer teaches three drills before its one-imp finale",
		world._finale_start() == 3 and world.phases.size() == 5
		and ResourceLoader.exists(
			"res://assets/opera/worlds/actors/rival_boxer.png")
		and world.combat_imps.is_empty())
	var voices_complete := true
	for phase: Dictionary in world.phases:
		var voice_id := String(phase.get("vo", ""))
		voices_complete = voices_complete and not voice_id.is_empty() \
			and not String(phase.get("voice", "")).is_empty() \
			and ResourceLoader.exists(
				"res://assets/audio/voices/roshan_%s.ogg" % voice_id)
	_check("every boxer drill and finale has recorded and visible instruction",
		voices_complete)

	var boxing := OperaBoxingSurface.new()
	boxing.size = Vector2(1280.0, 720.0)
	get_root().add_child(boxing)
	boxing.set_process(false)
	var passive_safe := true
	for mode_name: String in BOXING_MODES:
		boxing.configure(mode_name, Color.WHITE)
		for tick in range(60):
			boxing._process(0.5)
		passive_safe = passive_safe and boxing.landed_count() == 0 \
			and boxing.round_index() == 0 and not boxing.finished
	_check("thirty idle seconds never land a glove or finish a boxing mode",
		passive_safe)

	boxing.configure("boxing_guide", Color.WHITE)
	_boxing_touch(boxing, 7, true, boxing.glove_rest(0))
	_boxing_touch(boxing, 13, true, boxing.glove_rest(1))
	var owners := boxing.touch_owner_snapshot()
	_boxing_drag(boxing, 7, Vector2(700.0, 610.0))
	_boxing_drag(boxing, 13, Vector2(580.0, 610.0))
	var crossed_owners := boxing.touch_owner_snapshot()
	_check("crossed fingers keep independent left and right glove ownership",
		owners.size() == 2 and int(owners.get(7, -1)) == 0
		and int(owners.get(13, -1)) == 1
		and int(crossed_owners.get(7, -1)) == 0
		and int(crossed_owners.get(13, -1)) == 1)
	_boxing_touch(boxing, 7, false, Vector2(700.0, 610.0))
	var one_owner := boxing.touch_owner_snapshot()
	_check("releasing one glove leaves the other finger in control",
		one_owner.size() == 1 and int(one_owner.get(13, -1)) == 1
		and boxing.held)
	_boxing_touch(boxing, 13, false, Vector2(580.0, 610.0))

	boxing.configure("boxing_guide", Color.WHITE)
	for hand in range(2):
		_boxing_touch(boxing, 0, true, boxing.glove_rest(hand))
		_boxing_drag(boxing, 0, boxing.guide_target_position(hand))
		_boxing_touch(boxing, 0, false, boxing.guide_target_position(hand))
	_check("one finger can alternate and finish both floating glove lessons",
		boxing.landed_count() == 2 and boxing.round_index() == 2
		and boxing.touch_owner_snapshot().is_empty())

	boxing.configure("boxing_jab", Color.WHITE)
	_boxing_touch(boxing, 0, true, boxing.glove_rest(0))
	var jab_target := boxing.active_target_position()
	_boxing_drag(boxing, 0, jab_target)
	_boxing_drag(boxing, 0, jab_target)
	_boxing_drag(boxing, 0, jab_target + Vector2(1.0, 0.0))
	_boxing_touch(boxing, 0, false, jab_target)
	_check("one forward extension latches to exactly one accepted jab",
		boxing.landed_count() == 1 and boxing.round_index() == 1)
	var landed_before := boxing.landed_count()
	var round_before := boxing.round_index()
	var fill_before := boxing.widget_fill
	var phase_before := world.phase_progress
	var competition_before := act.competition.player_progress
	var score_before := act.competition.player_score
	var mistakes_before := act.competition.mistakes
	var stars_before := main.opera_stars
	var progress_before := main.opera_progress
	var done_before := main.opera_done
	for hit in range(8):
		boxing.receive_friendly_hit()
		world._on_gesture("boxing_contact", 0.0, 1.0)
	_check("friendly hits are cosmetic across surface, career, contest, and save state",
		boxing.has_friendly_hit_feedback()
		and boxing.landed_count() == landed_before
		and boxing.round_index() == round_before
		and is_equal_approx(boxing.widget_fill, fill_before)
		and is_equal_approx(world.phase_progress, phase_before)
		and is_equal_approx(act.competition.player_progress, competition_before)
		and act.competition.player_score == score_before
		and act.competition.mistakes == mistakes_before
		and main.opera_stars == stars_before
		and main.opera_progress == progress_before
		and main.opera_done == done_before)
	boxing.cancel_all_touches()
	_check("boxing cancellation returns both gloves to guard with no owner",
		boxing.touch_owner_snapshot().is_empty() and not boxing.held
		and boxing.glove_positions[0].is_equal_approx(boxing.glove_rest(0))
		and boxing.glove_positions[1].is_equal_approx(boxing.glove_rest(1)))
	boxing.queue_free()


func _drive_boxer_phase(world: OperaCareerWorld2D) -> void:
	if world.phase_advance_pending:
		world._advance_completed_phase()
		return
	if world.phase_index >= world.phases.size() \
			or not (world.surface is OperaBoxingSurface):
		return
	var boxing := world.surface as OperaBoxingSurface
	var mode := String((world.phases[world.phase_index] as Dictionary).get(
		"mode", ""))
	var hand := boxing.round_index() % 2
	match mode:
		"boxing_guide":
			if boxing.round_index() < 2:
				hand = boxing.round_index()
				_boxing_touch(boxing, 0, true, boxing.glove_rest(hand))
				_boxing_drag(boxing, 0, boxing.guide_target_position(hand))
				_boxing_touch(boxing, 0, false, boxing.guide_target_position(hand))
		"boxing_jab":
			_boxing_touch(boxing, 0, true, boxing.glove_rest(hand))
			var target := boxing.active_target_position()
			_boxing_drag(boxing, 0, target)
			_boxing_touch(boxing, 0, false, target)
			boxing._process(0.5)
		"boxing_guard":
			_boxing_touch(boxing, 0, true, boxing.glove_rest(hand))
			var target := boxing.active_target_position()
			_boxing_drag(boxing, 0, target)
			boxing._process(boxing._counter_t + 0.01)
			_boxing_touch(boxing, 0, false, target)
			boxing._process(0.5)
		"boxing_imp":
			var ticks := 0
			while not boxing.imp_is_open() and ticks < 20:
				boxing._process(0.4)
				ticks += 1
			if boxing.imp_is_open():
				_boxing_touch(boxing, 0, true, boxing.glove_rest(hand))
				var target := boxing.active_target_position()
				_boxing_drag(boxing, 0, target)
				_boxing_touch(boxing, 0, false, target)
				boxing._process(0.5)
		"boxing_belt":
			_boxing_touch(boxing, 0, true, boxing.glove_rest(hand))
			var target := boxing.active_target_position()
			_boxing_drag(boxing, 0, target)
			_boxing_touch(boxing, 0, false, target)
			boxing._process(0.5)


func _finale_partner_present(world: OperaCareerWorld2D, career: String) -> bool:
	if career != "boxer":
		return world.rival_actor.visible and world.in_competition_finale()
	if world.phase_index >= world.phases.size() \
			or not (world.surface is OperaBoxingSurface):
		return false
	var mode := String((world.phases[world.phase_index] as Dictionary).get(
		"mode", ""))
	var boxing := world.surface as OperaBoxingSurface
	return mode == "boxing_imp" and world.in_competition_finale() \
		and not world.rival_actor.visible \
		and (boxing._imp_textures.get("idle") as Texture2D) != null


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
