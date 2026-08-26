extends SceneTree
## Runtime contract for the thirteen Canvas-based Pearl Opera career worlds.
##
## This selects the ordinary Canvas career path used on every renderer. The
## companion probe_opera.gd protects stable save slots and real room lifecycle,
## while this probe proves the job path uses supplied paintings, 2D actors,
## one-finger phases, competition progress and clean teardown.

var main: ReefMain
var bad := 0
var widget_shot_out := ""
var widget_capture_career := ""
var rival_shot_out := ""
var stress_shot_out := ""
var lobby_shot_out := ""
var detective_shot_out := ""
var diegetic_shot_out := ""
var diegetic_shot_count := 0
var diegetic_shot_expected := 0

const StagePaths := preload("res://scripts/opera_stage_paths.gd")
const WorldHotspot := preload("res://scripts/opera_world_hotspot_2d.gd")
const HotspotCatalog := preload("res://scripts/opera_hotspot_catalog.gd")

const BOXING_MODES: Array[String] = [
	"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
]
const BOXING_GOALS: Array[float] = [2.0, 4.0, 3.0, 6.0, 1.0]
const BOXING_VOICES: Array[String] = [
	"op_boxer_work", "op_boxer_jab", "op_boxer_duck",
	"op_boxer_bell_chase", "op_boxer_belt",
]
const BalletSurface := preload("res://scripts/opera_ballet_surface.gd")

const DIRECT_SURFACE_CONTRACTS := {
	"detective": {
		"CASE BOARD": {"mode": "clue_board", "goal": 3.0, "context": "clue_board"},
		"CROWN": {"mode": "crown_chest", "goal": 1.0, "context": "crown_chest"},
	},
	"farmer": {
		"PLANT": {"mode": "garden_plant", "goal": 5.0, "context": "garden_plant"},
	},
	"ballerina": {
		"PEARL MIRROR": {"mode": "ballet_pose", "goal": 3.0, "context": ""},
		"RIBBON TRAIL": {"mode": "ballet_ribbon", "goal": 1.0, "context": ""},
		"GRAND TWIRL": {"mode": "ballet_twirl", "goal": 1.0, "context": ""},
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
	"racer": {
		"RACE": {"mode": "circle", "goal": 0.9, "context": ""},
	},
}

const RETAINED_ROTATIONS := {
	"chef": "STIR",
	"candymaker": "WRAP",
	"doctor": "CAST",
	"astronaut": "VALVE",
	"magician": "PORTAL",
	"racer": "TUNE",
	"popstar": "ENCORE",
}
const BALLERINA_PHASE_CONTRACTS := [
	{"name": "PEARL MIRROR", "mode": "ballet_pose", "goal": 3.0,
		"vo": "op_ballerina_watch"},
	{"name": "RIBBON TRAIL", "mode": "ballet_ribbon", "goal": 1.0,
		"vo": "op_ballerina_ribbon"},
	{"name": "GRAND TWIRL", "mode": "ballet_twirl", "goal": 1.0,
		"vo": "op_ballerina_twirl"},
]


func _audit_shipping_hotspot_specs() -> void:
	var shipping_phase_count := 0
	var missing_specs := PackedStringArray()
	for career: String in OperaCareerWorld2D.PHASES:
		var aliases: Dictionary = OperaCareerWorld2D.HOTSPOT_PHASE_ALIASES.get(
			career, {}) as Dictionary
		var career_phases: Array = OperaCareerWorld2D.PHASES.get(career, []) as Array
		for phase_value: Variant in career_phases:
			shipping_phase_count += 1
			var phase: Dictionary = phase_value as Dictionary
			var phase_name := String(phase.get("name", ""))
			var catalog_name := String(aliases.get(phase_name, phase_name))
			if HotspotCatalog.spec(career, catalog_name).is_empty():
				missing_specs.append("%s/%s -> %s" % [
					career, phase_name, catalog_name,
				])
	_check("all 53 shipping phases resolve through aliases to hotspot art specs",
		shipping_phase_count == 53 and missing_specs.is_empty())
	for missing_spec: String in missing_specs:
		print("OPERA2D|shipping_hotspot: missing %s" % missing_spec)


func _init() -> void:
	var catalog_errors: PackedStringArray = HotspotCatalog.validate_specs()
	_check("all cataloged diegetic object art passes resource, alpha, and aspect QA",
		catalog_errors.is_empty())
	for catalog_error: String in catalog_errors:
		print("OPERA2D|hotspot_catalog: %s" % catalog_error)
	_audit_shipping_hotspot_specs()
	widget_shot_out = OS.get_environment("OPERA_WIDGET_SHOT_OUT").strip_edges()
	widget_capture_career = OS.get_environment("OPERA_WIDGET_CAPTURE_CAREER").strip_edges()
	rival_shot_out = OS.get_environment("OPERA_RIVAL_SHOT_OUT").strip_edges()
	stress_shot_out = OS.get_environment("OPERA_STRESS_SHOT_OUT").strip_edges()
	lobby_shot_out = OS.get_environment("OPERA_LOBBY_SHOT_OUT").strip_edges()
	detective_shot_out = OS.get_environment("OPERA_DETECTIVE_SHOT_OUT").strip_edges()
	diegetic_shot_out = OS.get_environment("OPERA_DIEGETIC_SHOT_OUT").strip_edges()
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
	if not diegetic_shot_out.is_empty():
		DirAccess.make_dir_recursive_absolute(diegetic_shot_out)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.opera_stars = 0
	# Build the shipping room-route overlay on an isolated 1280x720 Castle
	# stage. probe_opera.gd separately drives these same controls through the
	# complete Castle and ReefMain lifecycle.
	var route_layer := CanvasLayer.new()
	main.add_child(route_layer)
	main.castle_room_layer = route_layer
	main.castle_room_stage = Control.new()
	main.castle_room_stage.name = "OperaRouteContractStage"
	main.castle_room_stage.size = StorybookUI.CANVAS_SIZE
	route_layer.add_child(main.castle_room_stage)
	var route_ui := CastleCareerRoutes.new(main)
	var route_rooms: Array[String] = [
		"kitchen", "opera_hall", "library", "craft_room", "playroom",
		"bubble_bath", "mermaid_pool", "dining_room", "movie_lounge",
	]
	var all_card_indices: Array[int] = []
	var all_route_art_ok := true
	for route_room: String in route_rooms:
		main.castle_room_id = route_room
		route_ui.sync()
		await process_frame
		if route_room == "opera_hall":
			route_ui.open_opera_venue()
			await process_frame
		var expected_indices := CastleCareerRoutes.act_indices_for_room(route_room)
		var actual_indices: Array[int] = []
		var room_art_ok := route_ui.root != null and route_ui.root.visible \
			and route_ui.root.size.is_equal_approx(StorybookUI.CANVAS_SIZE) \
			and not _has_spatial_descendants(route_ui.root)
		for card: Button in route_ui.buttons:
			var act_index := int(card.get_meta("act_index", -1))
			actual_indices.append(act_index)
			all_card_indices.append(act_index)
			if route_room == "opera_hall":
				var portal_focus := card.get_theme_stylebox("focus") \
					as StyleBoxFlat
				room_art_ok = room_art_ok and card.text.is_empty() \
					and card.visible and not card.clip_contents \
					and card.size.x >= StorybookUI.MIN_TOUCH.x \
					and card.size.y >= StorybookUI.MIN_TOUCH.y \
					and String(card.get_meta("castle_room_id", "")) == route_room \
					and String(card.get_meta("presentation", "")) \
						== "historical_three_floor_portal" \
					and not bool(card.get_meta("opaque_card", true)) \
					and bool(card.get_meta("painted_door_hit_region", false)) \
					and not bool(card.get_meta("floating_decoration", true)) \
					and card.get_child_count() == 0 \
					and portal_focus != null \
					and portal_focus.border_width_left == 0 \
					and is_zero_approx(portal_focus.bg_color.a)
				continue
			var actor := card.get_node_or_null("RoshanActor") as TextureRect
			var crest := card.get_node_or_null("CareerCrest") as TextureRect
			var frame := actor.texture as AtlasTexture if actor != null else null
			room_art_ok = room_art_ok and card.text.is_empty() \
				and card.visible and not card.disabled and not card.clip_contents \
				and card.size.x >= StorybookUI.MIN_TOUCH.x \
				and card.size.y >= StorybookUI.MIN_TOUCH.y \
				and bool(card.get_meta("picture_first", false)) \
				and String(card.get_meta("castle_room_id", "")) == route_room \
				and card.get_node_or_null("RivalActor") == null \
				and actor != null and actor.texture != null \
				and actor.position.x >= 0.0 and actor.position.y >= 0.0 \
				and actor.position.x + actor.size.x <= card.size.x \
				and actor.position.y + actor.size.y <= card.size.y \
				and frame != null and frame.atlas != null \
				and frame.atlas.resource_path.contains("/actors/animation/roshan_") \
				and crest != null and crest.texture != null \
				and crest.texture.resource_path.contains("/ui/crests/")
		_check("%s route uses its exact diegetic entrances and approved art" % route_room,
			actual_indices == expected_indices and room_art_ok)
		all_route_art_ok = all_route_art_ok and room_art_ok
		if route_room == "opera_hall":
			var venue := route_ui.opera_venue
			_check("Opera Hall guides the physical portal on Roshan's floor",
				venue != null and venue.guide_button != null \
				and int(venue.guide_button.get_meta("floor_index", -1)) \
					== venue.floor_index)
		else:
			_check("%s highlights exactly its preferred career atlas" % route_room,
				route_ui.highlighted_act \
					== CastleCareerRoutes.preferred_act_for_room(route_room, 0)
				and route_ui.active_animator != null
				and route_ui.active_animator.has_animation)
		if not lobby_shot_out.is_empty():
			await _capture_viewport(lobby_shot_out.path_join(
				"castle_career_routes_%s.png" % route_room))
	all_card_indices.sort()
	_check("nine room route sets cover all thirteen live sparse slots once",
		all_card_indices == OperaHouse.LIVE_ACT_INDICES and all_route_art_ok)
	_check("Opera Hall has only Ballerina, Pop Star and Magician",
		CastleCareerRoutes.act_indices_for_room("opera_hall") == [2, 13, 8])
	_check("the removed all-career lobby cannot load or appear",
		not ResourceLoader.exists("res://scripts/opera_lobby_2d.gd")
		and route_layer.find_children("*OperaLobby*", "Node", true, false).is_empty()
		and route_layer.find_children("*FloorTab*", "Node", true, false).is_empty())
	route_ui.clear()
	main.castle_room_layer = null
	main.castle_room_stage = null
	route_layer.queue_free()
	await process_frame

	main.game = "opera"
	var direct_touch_before := main.touch_ui.visible if main.touch_ui != null else false
	var house := OperaHouse.new()
	get_root().add_child(house)
	var direct_started := house.start(main, 0, Callable())
	await process_frame
	_check("OperaHouse starts one requested Canvas career with no picker",
		direct_started and house.act_index == 0 and house.act != null
		and not _has_spatial_descendants(house)
		and house.find_children("*OperaLobby*", "Node", true, false).is_empty())
	house._leave_early()
	await process_frame
	if main.touch_ui != null:
		_check("direct career cancel restores its caller's touch state",
			main.touch_ui.visible == direct_touch_before)
	_check("boxer keeps stable Opera save bit 128",
		OperaHouse.ACTS.size() > 7
		and String((OperaHouse.ACTS[7] as Dictionary).get("costume", "")) == "boxer"
		and (1 << 7) == 128)
	var show_count := 0
	var total_phase_count := 0
	var total_widget_count := 0
	var widget_contracts_complete := true
	var direct_surface_contracts_complete := true
	var circle_pacing_complete := true
	var retained_rotations_seen := 0
	for source_index: int in range(OperaHouse.ACTS.size()):
		if not OperaHouse.is_live_act_index(source_index):
			continue
		var source: Dictionary = OperaHouse.ACTS[source_index]
		show_count += 1
		var config := source.duplicate(true)
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
		diegetic_shot_expected += world.phases.size()
		if not diegetic_shot_out.is_empty():
			diegetic_shot_count += await _capture_diegetic_phase_rooms(
				world, career, show_count)
		var racer_node_bound := 0
		var racer_main_children_before: Array[int] = []
		if career == "racer":
			racer_node_bound = _subtree_node_count(world)
			racer_main_children_before = _direct_child_instance_ids(main)
			_check("racer Canvas world has a bounded post-build subtree",
				racer_node_bound <= 32)
			var racer_frame := world.player_actor.texture as AtlasTexture
			_check("racer uses the current animated Roshan atlas, rival and trophy art",
				racer_frame != null and racer_frame.atlas != null
				and racer_frame.atlas.resource_path.ends_with(
					"/animation/roshan_racer_sheet_a.png")
				and world.rival_actor.texture.resource_path.ends_with("/rival_racer.png")
				and world.prop_rect.texture.resource_path.ends_with("/goal_racer.png"))
		total_phase_count += world.phases.size()
		_check("%s uses no 3D children in career play" % career,
			not _has_spatial_descendants(act))
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
		if career == "ballerina":
			var ballet_phase_contract_ok := world.phases.size() \
				== BALLERINA_PHASE_CONTRACTS.size()
			for ballet_phase_index in range(BALLERINA_PHASE_CONTRACTS.size()):
				if ballet_phase_index >= world.phases.size():
					ballet_phase_contract_ok = false
					continue
				var actual_ballet_phase: Dictionary = world.phases[ballet_phase_index]
				var expected_ballet_phase: Dictionary = \
					BALLERINA_PHASE_CONTRACTS[ballet_phase_index]
				ballet_phase_contract_ok = ballet_phase_contract_ok \
					and String(actual_ballet_phase.get("name", "")) \
						== String(expected_ballet_phase.get("name", "")) \
					and String(actual_ballet_phase.get("mode", "")) \
						== String(expected_ballet_phase.get("mode", "")) \
					and is_equal_approx(float(actual_ballet_phase.get("goal", 0.0)),
						float(expected_ballet_phase.get("goal", -1.0))) \
					and String(actual_ballet_phase.get("vo", "")) \
						== String(expected_ballet_phase.get("vo", "")) \
					and ResourceLoader.exists(
						"res://assets/audio/voices/roshan_%s.ogg" \
						% String(expected_ballet_phase.get("vo", ""))) \
					and actual_ballet_phase.has("widget") \
					and String(actual_ballet_phase.get("widget", "missing")).is_empty() \
					and world._widget_template(actual_ballet_phase).is_empty()
			_check("ballerina has exactly PEARL MIRROR, RIBBON TRAIL, and GRAND TWIRL",
				ballet_phase_contract_ok)
		_check("%s waits at the room entrance in its costume idle" % career,
			world.player_animator != null and world.player_animator.has_animation
			and world.player_animator.current_animation == "idle")
		if world.player_animator != null and world.player_animator.has_animation:
			if career == "ballerina":
				world.player_animator.play("idle")
				var idle_frame_before := world.player_animator.current_frame
				world.player_animator._process(0.2)
				_check("ballerina idle is a deliberate held atlas pose",
					idle_frame_before == 2
					and world.player_animator.current_animation == "idle"
					and world.player_animator.current_frame == idle_frame_before)
				world.player_animator.play("work")
				var work_frame_before := world.player_animator.current_frame
				world.player_animator._process(0.2)
				_check("ballerina work is a deliberate held atlas pose",
					work_frame_before == 1
					and world.player_animator.current_animation == "work"
					and world.player_animator.current_frame == work_frame_before)
				var exact_pose_selection := true
				for selected_pose_frame in range(4):
					world.player_animator.show_pose("work", selected_pose_frame)
					world.player_animator._process(0.2)
					exact_pose_selection = exact_pose_selection \
						and world.player_animator.current_animation == "work" \
						and world.player_animator.current_frame == selected_pose_frame
				_check("ballerina show_pose holds the exact requested atlas cell",
					exact_pose_selection)
				world.player_animator.play("cheer")
				world.player_animator._process(0.4)
				var cheer_holds_bow := world.player_animator.current_frame == 0
				world.player_animator._process(0.2)
				var cheer_rises_slowly := world.player_animator.current_frame == 1
				world.player_animator._process(1.0)
				var cheer_reached_final := world.player_animator.current_frame == 3
				world.player_animator._process(5.0)
				_check("ballerina cheer bows once, rises, and holds its arms-up frame",
					cheer_holds_bow and cheer_rises_slowly and cheer_reached_final
					and world.player_animator.current_animation == "cheer"
					and world.player_animator.current_frame == 3
					and not world.player_animator.is_processing())
				world.player_animator.play("work")
			else:
				var frame_before := world.player_animator.current_frame
				# Idle runs at 4 fps. This crosses at least one frame boundary and
				# cannot wrap the four-frame atlas back onto the sampled cell.
				world.player_animator._process(0.3)
				_check("%s costume atlas advances frames" % career,
					world.player_animator.current_frame != frame_before)
		var expected_signature := {
			"chef": "oven", "detective": "lens", "ballerina": "ballet_pose",
			"candymaker": "candy_sort", "doctor": "xray_scan", "farmer": "farm_lob",
			"boxer": "boxing_guide", "magician": "magic_cabinet", "painter": "paint_reveal",
			"astronaut": "pipe", "racer": "circle", "nursery": "catch", "popstar": "echo",
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
		var direct_names_seen: Array[String] = []
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
			direct_names_seen.append(direct_name)
		var career_direct_contracts_complete := direct_names_seen.size() \
			== direct_contracts.size()
		for expected_direct_name: String in direct_contracts.keys():
			career_direct_contracts_complete = career_direct_contracts_complete \
				and direct_names_seen.has(expected_direct_name)
		if not direct_contracts.is_empty():
			_check("%s exposes every declared direct specialist phase" % career,
				career_direct_contracts_complete)
		direct_surface_contracts_complete = direct_surface_contracts_complete \
			and career_direct_contracts_complete
		var retained_rotation_ok := not RETAINED_ROTATIONS.has(career)
		for pacing_phase: Dictionary in world.phases:
			if String(pacing_phase.get("mode", "")) != "circle":
				continue
			# The Racer finale emits one accepted full loop from its specialist
			# steering surface. Its goal is a completed turn, not a rotation count.
			if career == "racer" \
					and String(pacing_phase.get("vo", "")) == "op_racer_lap_two":
				continue
			var rotations := float(pacing_phase.get("goal", 0.0))
			circle_pacing_complete = circle_pacing_complete \
				and rotations >= 1.5 and rotations <= 2.2
			_check("%s %s finishes in 1.5 to 2.2 rotations" \
				% [career, String(pacing_phase.get("name", "circle"))],
				rotations >= 1.5 and rotations <= 2.2)
			if String(pacing_phase.get("name", "")) \
					== String(RETAINED_ROTATIONS.get(career, "")):
				retained_rotation_ok = true
		if RETAINED_ROTATIONS.has(career):
			_check("%s retains its thematic rotation verb" % career,
				retained_rotation_ok)
			if retained_rotation_ok:
				retained_rotations_seen += 1
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
			var pearl_mirror_watch_count := 0
			var retired_generic_ballet_mode := false
			var ballet_silences_entry_voice := false
			for opera_cfg: Dictionary in OperaHouse.ACTS:
				if String(opera_cfg.get("costume", "")) == "ballerina":
					ballet_silences_entry_voice = bool(opera_cfg.get(
						"silence_entry_voice", false))
			for ballerina_phase: Dictionary in world.phases:
				var ballerina_mode := String(ballerina_phase.get("mode", ""))
				if String(ballerina_phase.get("name", "")) == "PEARL MIRROR" \
						and ballerina_mode == "ballet_pose" \
						and String(ballerina_phase.get("vo", "")) == "op_ballerina_watch":
					pearl_mirror_watch_count += 1
				retired_generic_ballet_mode = retired_generic_ballet_mode \
					or ballerina_mode in ["dance_sequence", "hold"]
			_check("ballerina watch cue belongs only to the specialist pearl mirror",
				pearl_mirror_watch_count == 1 and not retired_generic_ballet_mode)
			_check("ballerina clears any lobby voice before its watch instruction",
				ballet_silences_entry_voice)
			var ballet_steps_stream := load(
				"res://assets/audio/voices/roshan_op_ballerina_steps.ogg") as AudioStream
			var ballet_ribbon_stream := load(
				"res://assets/audio/voices/roshan_op_ballerina_ribbon.ogg") as AudioStream
			_check("ballerina lets each your-turn cue finish before the next phase",
				ballet_steps_stream != null and ballet_ribbon_stream != null
				and OperaCareerWorld2D.BALLET_PHASE_HOLD_SECONDS \
					>= maxf(ballet_steps_stream.get_length(),
						ballet_ribbon_stream.get_length()) + 0.05)
		if career == "candymaker":
			var syrup_goal := 0.0
			var syrup_phase_index := -1
			for candy_phase_i in range(world.phases.size()):
				var candy_phase: Dictionary = world.phases[candy_phase_i]
				if String(candy_phase.get("name", "")) == "SYRUP":
					syrup_goal = float(candy_phase.get("goal", 0.0))
					syrup_phase_index = candy_phase_i
			_check("candymaker SYRUP requires the full five-point pour",
				is_equal_approx(syrup_goal, 5.0) and syrup_phase_index >= 0)
			world.phase_index = syrup_phase_index
			world.phase_progress = 0.0
			world.phase_gap = 0.0
			world.reveal_t = 0.0
			world.phase_advance_pending = false
			world._show_phase()
			# Pixel 10's 2424x1080 framebuffer maps to a 1616x720 logical
			# canvas. Prove the fixed stage, actual right-docked card, shipping
			# touch surface and its real pitcher grab all survive that transform.
			var pixel_canvas := Vector2(1616.0, 720.0)
			var fit_scale := minf(pixel_canvas.x / OperaStagePaths.SCREEN.x,
				pixel_canvas.y / OperaStagePaths.SCREEN.y)
			var fit_offset := (pixel_canvas - OperaStagePaths.SCREEN * fit_scale) * 0.5
			var pixel_view := Rect2(Vector2.ZERO, pixel_canvas)
			var fitted_stage := Rect2(fit_offset, OperaStagePaths.SCREEN * fit_scale)
			var fitted_card := Rect2(fit_offset + world.action_panel.position * fit_scale,
				world.action_panel.size * fit_scale)
			var fitted_surface := Rect2(
				fit_offset + (world.action_panel.position + world.surface.position) * fit_scale,
				world.surface.size * fit_scale)
			var fitted_grab := fit_offset \
				+ (world.action_panel.position + world.surface.position
				+ world.surface._pour_pitcher_rect().get_center()) * fit_scale
			_check("Pixel 10 keeps candymaker SYRUP card and grab inside the fitted stage",
				pixel_view.encloses(fitted_stage) and fitted_stage.encloses(fitted_card)
				and fitted_card.encloses(fitted_surface)
				and fitted_surface.has_point(fitted_grab))
			var is_pixel_capture := OS.get_environment("OPERA_PIXEL10_CAPTURE") == "1"
			if is_pixel_capture and not widget_shot_out.is_empty() \
					and (widget_capture_career.is_empty()
						or widget_capture_career == "candymaker"):
				await _capture_viewport(widget_shot_out.path_join(
					"candymaker_pixel10_00_empty_world.png"))
			# Drive the shipping signal path: the real surface pays the real world,
			# which owns the five-point goal and accepts the completed picture.
			var pour_step := 1.0 / 30.0
			var pour_seconds := 0.0
			var pour_grab := world.surface._pour_pitcher_rect().get_center()
			world.surface._press(pour_grab)
			while world.surface.pour_level < 0.97 and pour_seconds < 4.0:
				world.surface._process(pour_step)
				pour_seconds += pour_step
			world.surface._release(pour_grab)
			_check("candymaker remains an empty-mold pour until the actual brim",
				world.surface.pour_level > 0.94 and world.surface.pour_level < 1.0
				and world.phase_progress < syrup_goal
				and not world.phase_advance_pending
				and not world.surface.completion_accepted)
			if is_pixel_capture and not widget_shot_out.is_empty() \
					and (widget_capture_career.is_empty()
						or widget_capture_career == "candymaker"):
				await _capture_viewport(widget_shot_out.path_join(
					"candymaker_pixel10_04_just_under_full_world.png"))
			var root_children_before_completion := world.root.get_child_count()
			_check("candymaker SYRUP selects its authored completion picture",
				world._uses_authored_completion_picture("pourt"))
			pour_grab = world.surface._pour_pitcher_rect().get_center()
			world.surface._press(pour_grab)
			while not world.phase_advance_pending and pour_seconds < 4.2:
				world.surface._process(pour_step)
				pour_seconds += pour_step
			world.surface._release(pour_grab)
			_check("candymaker real SYRUP hold completes its connected world",
				world.phase_advance_pending and world.surface.completion_accepted
				and is_equal_approx(world.phase_progress, syrup_goal)
				and is_equal_approx(world.surface.pour_level, 1.0)
				and pour_seconds < 4.2)
			_check("candymaker authored completion spawns no shared abstract burst",
				world.root.get_child_count() == root_children_before_completion)
			world.surface._process(0.36)
			_check("candymaker success hold rights its visibly empty ladle",
				is_zero_approx(world.surface.pour_tilt)
				and not world.surface._pour_stream_active()
				and is_zero_approx(world.surface._candymaker_full_ladle_alpha()))
			if is_pixel_capture and not widget_shot_out.is_empty() \
					and (widget_capture_career.is_empty()
						or widget_capture_career == "candymaker"):
				await _capture_viewport(widget_shot_out.path_join(
					"candymaker_pixel10_05_success_world.png"))
			world._advance_completed_phase()
			world._show_phase()
			var sort_phase: Dictionary = world.phases[world.phase_index]
			_check("candymaker brim advances cleanly to SORT without a stale ladle",
				String(sort_phase.get("name", "")) == "SORT"
				and world.surface.mode == "candy_sort"
				and world.surface.visual_context == "lanes_candymaker"
				and not world.surface.completion_accepted
				and world.surface.pour_empty_mover_texture == null)
			if not widget_shot_out.is_empty() \
					and (widget_capture_career.is_empty()
						or widget_capture_career == "candymaker"):
				await _capture_control(world.surface,
					widget_shot_out.path_join("candymaker_06_sort_transition.png"))
			# Leave the per-career probe at the same fresh opening state expected by
			# the generic widget contracts below.
			world.phase_index = syrup_phase_index
			world.phase_progress = 0.0
			world.phase_advance_pending = false
			world.phase_complete_t = 0.0
			world.phase_gap = 0.0
			world.reveal_t = 0.0
			world._show_phase()
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
		if career == "ballerina":
			var finale_stage_tiles_ok := backdrop != null and backdrop.stage_tiles.size() == 4
			if backdrop != null:
				for stage_tile: Texture2D in backdrop.stage_tiles:
					finale_stage_tiles_ok = finale_stage_tiles_ok \
						and stage_tile != null \
						and stage_tile.resource_path.contains("/stage/finale_stage_c")
			_check("ballerina begins in its navigable rehearsal room with finale art ready",
				world.phase_index == 0 and backdrop != null and not backdrop.stage_mode
				and finale_stage_tiles_ok)
			_check("ballerina maps every recital lesson to a painted room object",
				world.station_list.size() >= 3
				and world.station_for_phase.size() == world.phases.size())
			_check("ballerina arms one dedicated surface while its room object waits",
				world.surface != null and world.surface.get_script() == BalletSurface
				and not world.action_panel.visible and world.surface.armed_only
				and world.player_actor.visible)
			var ballet_surface: Variant = world.surface
			_check("ballerina recital maps heart, open, and crown atlas poses in order",
				BalletSurface.POSE_FRAMES == [3, 2, 1]
				and ballet_surface.pose_target_frame() == 3
				and ballet_surface.pose_option_frames() == [1, 3])
			ballet_surface.configure("ballet_pose", Color.WHITE)
			ballet_surface.armed_only = false
			var mirror_repeat_before := world.ballet_instruction_repeats
			world.reveal_t = 0.0
			world.idle_t = 6.95
			world._process(0.10)
			var mirror_idle_demo_silent: bool = \
				world.ballet_instruction_repeats == mirror_repeat_before \
				and ballet_surface.demo_active
			ballet_surface._process(ballet_surface.demo_duration() + 0.1)
			_check("ballerina idle replay waits until Mirror hands the turn back",
				mirror_idle_demo_silent
				and world.ballet_instruction_repeats == mirror_repeat_before + 1)
			_check("ballerina hides progress chrome, race bars, and the rival",
				world.phase_fill != null and not world.phase_fill.visible
				and world.player_bar != null and not world.player_bar.visible
				and world.rival_bar != null and not world.rival_bar.visible
				and world.rival_actor != null and not world.rival_actor.visible)
		else:
			_check("%s starts in its job world, off the proscenium" % career,
				backdrop != null and not backdrop.stage_mode)
		_check("%s paints the supplied codex career world" % career,
			backdrop != null and backdrop.world_tiles.size() == 4)
		_check("%s owns a complete on-stage tile set" % career,
			backdrop != null and backdrop.stage_tiles.size() == 4)
		if not rival_shot_out.is_empty() and not cooperative \
				and career not in ["ballerina", "boxer"]:
			await _capture_rival_states(world, career, backdrop)
		var widgets_complete := true
		var widgets_causal := true
		var widgets_borderless := true
		var widgets_grounded := true
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
			world.action_panel.visible = true
			world.surface.visible = true
			world.surface.queue_redraw()
			await process_frame
			var specialist_mode := phase_mode in [
				"pourt", "oven", "xray_scan", "dance_sequence",
				"candy_sort", "paint_reveal", "farm_lob",
			]
			widgets_borderless = widgets_borderless \
				and not OperaGestureSurface.DRAWS_FRAMED_WIDGET_BACKDROPS \
				and world.surface.widget_backdrop == null \
				and world.surface.retired_widget_backdrop_path == widget_path
			widgets_grounded = widgets_grounded \
				and (specialist_mode
					or world.surface.last_widget_ground_route == template)
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
				# The farmer surface is release-driven: a weak release loops safely;
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
			if not widget_shot_out.is_empty() \
					and (widget_capture_career.is_empty() or widget_capture_career == career):
				await _capture_widget_states(world, career, phase_number, phase_dict, template)
		# Direct specialist surfaces deliberately have no generic widget family;
		# those contracts are exercised above instead of requiring reskin assets.
		var career_widget_contract_complete := widgets_complete \
			and (widget_count > 0 \
				or career in ["ballerina", "boxer", "detective", "racer"])
		_check("%s loads every diegetic phase widget" % career,
			career_widget_contract_complete)
		widget_contracts_complete = widget_contracts_complete \
			and career_widget_contract_complete
		_check("%s widgets remain input-causal with owner-gated completion" % career,
			widgets_causal)
		_check("%s suppresses every retired framed widget backdrop" % career,
			widgets_borderless)
		_check("%s keeps a persistent borderless play affordance" % career,
			widgets_grounded)
		_audit_diegetic_room_flow(world, career)
		if career == "ballerina":
			_check("ballerina object opens its large borderless recital surface",
				world.task_open and world.action_panel.visible
				and world.surface is OperaBalletSurface
				and world.surface.size.x >= 800.0 and world.surface.size.y >= 600.0)
		elif career == "boxer":
			_check("boxer object opens its full-room two-glove view",
				world.task_open and world.action_panel.visible
				and world.surface is OperaBoxingSurface
				and world.surface.size.is_equal_approx(StorybookUI.CANVAS_SIZE)
				and not world.player_actor.visible)
		_check("%s loads the authored magnifier prop" % career,
			world.magnifier_texture != null)
		if world.action_panel.visible and world.player_actor.visible:
			var panel_rect := Rect2(world.action_panel.position, world.action_panel.size)
			var actor_rect := Rect2(world.player_actor.position,
				world.player_actor.size * world.player_actor.scale).grow(24.0)
			_check("%s borderless activity focus never covers animated Roshan" % career,
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
			# Reaching a finale now arms its room object instead of auto-opening it.
			# The trusted probe path still has to perform that explicit open before
			# auditing the rival clock.
			for _open_attempt in range(3):
				if world.task_open:
					break
				world._on_gesture("probe", 0.0, 1.0)
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
		var finale_cast_separated := career in ["ballerina", "boxer"]
		var racer_finale_exercised := false
		var guard := 0
		while act.state == "play" and guard < 80:
			rival_hidden_before_finale = rival_hidden_before_finale \
				and (cooperative or world.in_competition_finale() or not world.rival_actor.visible)
			if career == "racer" and world.phase_index == world._finale_start():
				if not racer_finale_exercised:
					finale_cast_separated = await _exercise_racer_finale(
						act, world, racer_node_bound, racer_main_children_before)
					racer_finale_exercised = true
			elif career == "boxer":
				_drive_boxer_phase(world)
			else:
				world._on_gesture("probe", 100.0, 1.0)
			act._process(0.05)
			await process_frame
			guard += 1
			saw_finale_imp = saw_finale_imp or _finale_partner_present(world, career)
			if world.task_open and world.in_competition_finale() \
					and world.player_actor.visible and world.rival_actor.visible:
				var player_rect := _actor_visual_rect(world.player_actor)
				var rival_rect := _actor_visual_rect(world.rival_actor)
				var activity_rect := Rect2(world.action_panel.position,
					world.action_panel.size)
				finale_cast_separated = _rect_inside(player_rect,
					Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)) \
					and _rect_inside(rival_rect,
						Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)) \
					and not player_rect.intersects(rival_rect) \
					and (not world.action_panel.visible
						or not rival_rect.intersects(activity_rect))
		_check("%s keeps the rival hidden before its stage contest" % career,
			rival_hidden_before_finale)
		if career == "ballerina":
			_check("ballerina keeps the recital rival-free through the curtain call",
				not saw_finale_imp and not world.rival_actor.visible)
		elif career == "boxer":
			_check("boxer finale uses one specialist padded imp, then a safe curtain call",
				saw_finale_imp and world.combat_imps.is_empty()
				and world.rival_actor.visible and not world.action_panel.visible)
		else:
			_check("%s brings in its dressed finale partner" % career, saw_finale_imp)
			_check("%s stages the room-finale partner clear of Roshan and the activity" % career,
				finale_cast_separated)
		if career == "racer":
			_check("racer finale was completed only through the real steering surface",
				racer_finale_exercised)
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
		var curtain_canvas := Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
		var curtain_player := _actor_rest_rect(world, "player")
		var curtain_rival := _actor_rest_rect(world, "rival")
		var curtain_prop := _actor_rest_rect(world, "prop")
		var prop_spotlight_ok := world.prop_rect.texture == null \
			or (_rect_inside(curtain_prop, curtain_canvas)
				and absf(curtain_prop.get_center().x
					- StorybookUI.CANVAS_SIZE.x * 0.5) <= 4.0)
		_check("%s gives the curtain-call cast distinct stage-local rests" % career,
			not world.action_panel.visible and not world.surface.visible
			and _rect_inside(curtain_player, curtain_canvas)
			and _rect_inside(curtain_rival, curtain_canvas)
			and curtain_player.get_center().x < curtain_rival.get_center().x
			and not curtain_player.intersects(curtain_rival)
			and prop_spotlight_ok)
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

	await _exercise_racer_cancel_and_reentry()

	var reentry_config: Dictionary = {}
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("costume", "")) == "chef":
			reentry_config = source.duplicate(true)
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
	_check("the current thirteen careers expose exactly fifty-three phases",
		total_phase_count == 53)
	_check("all shared art-family career widget contracts were exercised",
		widget_contracts_complete and total_widget_count > 0)
	_check("every declared direct specialist surface was exercised",
		direct_surface_contracts_complete)
	_check("every retained generic rotation uses the shortened pacing",
		circle_pacing_complete and retained_rotations_seen == RETAINED_ROTATIONS.size())
	if not diegetic_shot_out.is_empty():
		_check("diegetic review capture contains every shipping phase room state",
			diegetic_shot_count == diegetic_shot_expected)
	if bad == 0:
		print("OPERA2D|result: ALL OK")
		quit()
	else:
		print("OPERA2D|result: %d FAIL" % bad)
		quit(1)


func _capture_diegetic_phase_rooms(world: OperaCareerWorld2D, career: String,
		career_number: int) -> int:
	# Capture discovery, not an already-open minigame: Roshan idles at the
	# room entrance and exactly one phase-specific physical object invites her.
	# Every mutation below is probe-local and the ordinary phase-one lifecycle
	# is reconstructed before the broad gameplay checks resume.
	var captured := 0
	for phase_number in range(world.phases.size()):
		world.phase_index = phase_number
		world.phase_progress = 0.0
		world.phase_advance_pending = false
		world.phase_complete_t = 0.0
		world.reveal_t = 0.0
		world.active = true
		world._arm_phase()
		if world.m != null:
			world.m.clear_dialogue()
			world.m.hud_msg.visible = false
			world.m.msg_timer = 0.0
		var phase: Dictionary = world.phases[phase_number]
		var phase_name := String(phase.get("name", "phase_%d" % (phase_number + 1)))
		var filename := "%02d_%s_p%02d_%s_room.png" % [
			career_number, career, phase_number + 1, phase_name.to_snake_case()]
		await _capture_viewport(diegetic_shot_out.path_join(filename))
		captured += 1

	world.competition.pause()
	world.phase_index = 0
	world.phase_progress = 0.0
	world.phase_advance_pending = false
	world.phase_complete_t = 0.0
	world.reveal_t = 0.0
	world.active = true
	for hotspot: OperaWorldHotspot2D in _opera_hotspots(world):
		hotspot.elapsed = 0.0
	world._arm_phase()
	_check("%s capture restores the closed phase-one room lifecycle" % career,
		world.phase_index == 0 and world.active and not world.task_open
		and is_equal_approx(world.phase_progress, 0.0)
		and not world.competition.active and _armed_hotspots(world).size() == 1)
	return captured


func _audit_diegetic_room_flow(world: OperaCareerWorld2D, career: String) -> void:
	# Earlier mechanic-specific assertions deliberately configure arbitrary
	# phases. Restore the actual entry state before auditing room discovery.
	world.phase_index = 0
	world.phase_progress = 0.0
	world.phase_advance_pending = false
	world.phase_complete_t = 0.0
	world.reveal_t = 0.0
	world._arm_phase()
	var canvas_rect := Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
	var wander_input := world.root.get_node_or_null("WalkableRoomInput") as Control
	_check("%s replaces clipboard and beacon textures with the room itself" % career,
		world.task_frame_texture == null and world.station_marker_texture == null)
	_check("%s exposes one full-room constrained touch layer" % career,
		wander_input != null and wander_input == world.wander_layer
		and wander_input.size.is_equal_approx(StorybookUI.CANVAS_SIZE)
		and not wander_input.clip_contents)
	_check("%s starts with the room available and its task closed" % career,
		not world.task_open and not world.action_panel.visible
		and wander_input != null and wander_input.visible
		and wander_input.mouse_filter == Control.MOUSE_FILTER_STOP)

	var hotspots := _opera_hotspots(world)
	var hotspot_structure_ok := hotspots.size() == world.station_list.size() \
		and not hotspots.is_empty()
	var hotspot_text_free := true
	for hotspot: OperaWorldHotspot2D in hotspots:
		hotspot_structure_ok = hotspot_structure_ok \
			and hotspot.name == "ActivityHotspot_%s" % hotspot.station_id \
			and hotspot.get_parent() == world.root
		hotspot_text_free = hotspot_text_free and hotspot.touch_button != null \
			and hotspot.touch_button.text.is_empty() \
			and bool(hotspot.touch_button.get_meta("physical_object", false))
	_check("%s builds only named physical ActivityHotspot objects" % career,
		hotspot_structure_ok)
	_check("%s hotspot invitations are pictorial and never reading-dependent" % career,
		hotspot_text_free)

	var active := _audit_phase_hotspot_rearming(world, career, canvas_rect)
	if active == null:
		# Keep the rest of the broad career probe diagnostic after a focused
		# contract failure; this direct path is not accepted as a passing flow.
		world._show_phase()
		return

	var inactive := _first_inactive_hotspot(hotspots, active)
	if inactive != null:
		var inactive_phase := world.phase_index
		var inactive_progress := world.phase_progress
		var inactive_score := world.competition.player_score
		inactive.touch_button.pressed.emit()
		_check("%s blocks every inactive room object" % career,
			world.phase_index == inactive_phase
			and is_equal_approx(world.phase_progress, inactive_progress)
			and world.competition.player_score == inactive_score
			and not world.wander_walking and not world.hotspot_opening
			and not world.task_open)
	else:
		_check("%s blocks every inactive room object" % career, false)

	var phase_before := world.phase_index
	var progress_before := world.phase_progress
	var score_before := world.competition.player_score
	var competition_before := world.competition.player_progress
	var glow_elapsed_before := active.elapsed
	for _passive_tick in range(4):
		world._process(0.1)
		active._process(0.1)
	_check("%s animates its invitation without passive game progress" % career,
		active.elapsed > glow_elapsed_before
		and world.phase_index == phase_before
		and is_equal_approx(world.phase_progress, progress_before)
		and world.competition.player_score == score_before
		and is_equal_approx(world.competition.player_progress, competition_before)
		and not world.task_open)

	# Every real minigame gesture is inert until Roshan reaches the object.
	# `probe` remains the explicit trusted fast-forward path used later below.
	for real_gesture: String in ["tap", "hold", "swipe", "circle", "choice"]:
		world._on_gesture(real_gesture, 1.0, 1.0)
	_check("%s cannot open or score a closed task with real gestures" % career,
		world.phase_index == phase_before
		and is_equal_approx(world.phase_progress, progress_before)
		and world.competition.player_score == score_before
		and is_equal_approx(world.competition.player_progress, competition_before)
		and not world.task_open)

	var activation_before := active.activation_count
	active.touch_button.pressed.emit()
	var emitted_route := world.wander_route.duplicate()
	var expected_approach := StagePaths.station_approach(career, active.station_id)
	_check("%s hotspot tap starts an authored route, never the task" % career,
		not world.task_open and not world.hotspot_opening
		and active.activation_count == activation_before
		and world.wander_walking and not emitted_route.is_empty()
		and StagePaths.route_is_approved(career, emitted_route, 2.0)
		and emitted_route[emitted_route.size() - 1].distance_to(expected_approach) <= 2.0)
	_check("%s hotspot tap cannot award immediate progress" % career,
		world.phase_index == phase_before
		and is_equal_approx(world.phase_progress, progress_before)
		and world.competition.player_score == score_before
		and is_equal_approx(world.competition.player_progress, competition_before))

	var route_stayed_safe := true
	var progress_stayed_safe := true
	var saw_arrival := false
	var saw_opening := false
	var tested_opening_touch := false
	var opening_touch_ignored := true
	var route_ticks := 0
	while not world.task_open and route_ticks < 320:
		world._process(0.05)
		route_stayed_safe = route_stayed_safe \
			and StagePaths.point_is_on_approved_route(career, world.wander_feet, 3.0)
		saw_arrival = saw_arrival \
			or world.wander_feet.distance_to(expected_approach) <= 4.0
		saw_opening = saw_opening or world.hotspot_opening or active.opening \
			or active.activation_count > activation_before
		if world.hotspot_opening and not tested_opening_touch:
			var intent_before := world.interaction_requested
			var station_before := world.interaction_station
			var second_touch := InputEventScreenTouch.new()
			second_touch.pressed = true
			second_touch.position = Vector2(640.0, 560.0)
			world._wander_input(second_touch)
			opening_touch_ignored = world.hotspot_opening \
				and world.interaction_requested == intent_before \
				and world.interaction_station == station_before \
				and active.opening and active.touch_button.disabled
			tested_opening_touch = true
		progress_stayed_safe = progress_stayed_safe \
			and world.phase_index == phase_before \
			and is_equal_approx(world.phase_progress, progress_before) \
			and world.competition.player_score == score_before \
			and is_equal_approx(world.competition.player_progress, competition_before)
		active._process(0.05)
		saw_opening = saw_opening or world.hotspot_opening or active.opening \
			or active.activation_count > activation_before
		route_ticks += 1
	_check("%s stays on authored walkways from tap through arrival" % career,
		route_stayed_safe and saw_arrival)
	_check("%s arrives, plays one object opening, then opens the task" % career,
		world.task_open and saw_opening
		and active.activation_count == activation_before + 1
		and not world.wander_walking)
	_check("%s ignores an extra touch during the object opening flourish" % career,
		tested_opening_touch and opening_touch_ignored and world.task_open)
	_check("%s approach and opening remain passive-safe" % career,
		progress_stayed_safe
		and world.phase_index == phase_before
		and is_equal_approx(world.phase_progress, progress_before)
		and world.competition.player_score == score_before
		and is_equal_approx(world.competition.player_progress, competition_before))
	_check("%s hands input safely from the room to the minigame" % career,
		wander_input != null and not wander_input.visible
		and wander_input.mouse_filter == Control.MOUSE_FILTER_IGNORE)

	var panel_rect := Rect2(world.action_panel.position, world.action_panel.size)
	var panel_inside := not world.action_panel.visible \
		or _rect_inside(panel_rect, canvas_rect)
	var contents_inside := true
	if world.action_panel.visible:
		contents_inside = _rect_inside(
			Rect2(world.surface.position, world.surface.size),
			Rect2(Vector2.ZERO, world.action_panel.size))
		if world.nursery_catch != null and world.nursery_catch.visible:
			contents_inside = contents_inside and _rect_inside(
				Rect2(world.nursery_catch.position, world.nursery_catch.size),
				Rect2(Vector2.ZERO, world.action_panel.size))
	var actor_rect := Rect2(world.player_actor.position,
		world.player_actor.size * world.player_actor.scale)
	var visible_partner_clear := true
	if world.rival_actor != null and world.rival_actor.visible:
		var partner_rect := _actor_visual_rect(world.rival_actor)
		visible_partner_clear = _rect_inside(partner_rect, canvas_rect) \
			and not partner_rect.intersects(actor_rect) \
			and (not world.action_panel.visible
				or not partner_rect.intersects(panel_rect))
	_check("%s uses a transparent borderless activity focus" % career,
		world.task_frame_texture == null and world.station_marker_texture == null
		and not OperaGestureSurface.DRAWS_CARD_BACKING
		and world.action_panel.color.a <= 0.001
		and not world.action_panel.clip_contents
		and world.action_panel.find_children("*", "Label", true, false).is_empty())
	_check("%s keeps the opened activity and full Mermaid Roshan onscreen" % career,
		panel_inside and contents_inside and _rect_inside(actor_rect, canvas_rect)
		and not world.player_actor.clip_contents)
	_check("%s keeps every visible partner clear of Roshan and the activity" % career,
		visible_partner_clear)


func _audit_phase_hotspot_rearming(world: OperaCareerWorld2D, career: String,
		canvas_rect: Rect2) -> OperaWorldHotspot2D:
	var declared: Dictionary = OperaCareerWorld2D.PHASE_STATIONS.get(career, {}) \
		as Dictionary
	var previous_active: OperaWorldHotspot2D = null
	var every_transition_rearmed := true
	for phase_number in range(world.phases.size()):
		world.phase_index = phase_number
		world.phase_progress = 0.0
		world.phase_advance_pending = false
		world.phase_complete_t = 0.0
		world.reveal_t = 0.0
		world._arm_phase()
		var phase: Dictionary = world.phases[phase_number]
		var phase_name := String(phase.get("name", "phase_%d" % phase_number))
		var expected_id := String(declared.get(phase_name, ""))
		var expected_index := int(world.station_for_phase.get(phase_number, -1))
		var armed := _armed_hotspots(world)
		var active: OperaWorldHotspot2D = armed[0] if armed.size() == 1 else null
		var exact_mapping := active != null and not expected_id.is_empty() \
			and active.station_index == expected_index \
			and active.station_id == expected_id
		_check("%s %s arms exactly its themed room object" % [career, phase_name],
			armed.size() == 1 and exact_mapping
			and not world.task_open and not world.action_panel.visible)

		var themed_and_safe := active != null and active.object_texture != null \
			and not active.source_path.is_empty() \
			and not active.source_path.ends_with("station_marker.png") \
			and active.touch_button != null and active.touch_button.text.is_empty() \
			and not active.touch_button.disabled \
			and active.hit_size.x >= WorldHotspot.MIN_TOUCH.x \
			and active.hit_size.y >= WorldHotspot.MIN_TOUCH.y \
			and not active.clip_contents \
			and _rect_inside(active.stage_hit_rect(), canvas_rect) \
			and _rect_inside(active.stage_glow_rect(), canvas_rect)
		_check("%s %s hotspot art, glow, and touch target do not clip" \
			% [career, phase_name], themed_and_safe)
		var actor_object_overlap := INF
		if active != null:
			actor_object_overlap = _roshan_idle_semantic_rect(world).intersection(
				active.stage_object_rect()).get_area()
		_check("%s %s keeps its idle object clear of Roshan's body" \
			% [career, phase_name], actor_object_overlap <= 1.0)

		for hotspot: OperaWorldHotspot2D in _opera_hotspots(world):
			if hotspot == active:
				continue
			every_transition_rearmed = every_transition_rearmed \
				and not hotspot.armed and not hotspot.visible \
				and hotspot.touch_button != null and hotspot.touch_button.disabled
		if previous_active != null and previous_active != active:
			every_transition_rearmed = every_transition_rearmed \
				and not previous_active.armed \
				and previous_active.touch_button != null \
				and previous_active.touch_button.disabled
		if active != null:
			previous_active = active

	_check("%s re-arms only the next phase object and blocks all others" % career,
		every_transition_rearmed)
	world.competition.pause()
	world.phase_index = 0
	world.phase_progress = 0.0
	world.phase_advance_pending = false
	world.phase_complete_t = 0.0
	world.reveal_t = 0.0
	if world.m != null:
		world.m.clear_dialogue()
	world._arm_phase()
	var reset_armed := _armed_hotspots(world)
	_check("%s safely returns the phase-one invitation after rearm audit" % career,
		reset_armed.size() == 1 and not world.task_open
		and not world.action_panel.visible and not world.competition.active)
	return reset_armed[0] if reset_armed.size() == 1 else null


func _opera_hotspots(world: OperaCareerWorld2D) -> Array[OperaWorldHotspot2D]:
	var hotspots: Array[OperaWorldHotspot2D] = []
	for node: Control in world.station_nodes:
		var hotspot := node as OperaWorldHotspot2D
		if hotspot != null:
			hotspots.append(hotspot)
	return hotspots


func _armed_hotspots(world: OperaCareerWorld2D) -> Array[OperaWorldHotspot2D]:
	var armed: Array[OperaWorldHotspot2D] = []
	for hotspot: OperaWorldHotspot2D in _opera_hotspots(world):
		if hotspot.armed:
			armed.append(hotspot)
	return armed


func _first_inactive_hotspot(hotspots: Array[OperaWorldHotspot2D],
		active: OperaWorldHotspot2D) -> OperaWorldHotspot2D:
	for hotspot: OperaWorldHotspot2D in hotspots:
		if hotspot != active:
			return hotspot
	return null


func _rect_inside(inner: Rect2, outer: Rect2, slack: float = 0.1) -> bool:
	return inner.position.x >= outer.position.x - slack \
		and inner.position.y >= outer.position.y - slack \
		and inner.end.x <= outer.end.x + slack \
		and inner.end.y <= outer.end.y + slack


func _actor_visual_rect(actor: Control) -> Rect2:
	if actor == null:
		return Rect2()
	return Rect2(actor.position, actor.size * actor.scale)


func _actor_rest_rect(world: OperaCareerWorld2D, key: String) -> Rect2:
	var rest: Dictionary = world.actor_rests.get(key, {}) as Dictionary
	if rest.is_empty():
		return Rect2()
	var position: Vector2 = rest.get("position", Vector2.ZERO) as Vector2
	var size: Vector2 = rest.get("size", Vector2.ZERO) as Vector2
	var scale: Vector2 = rest.get("scale", Vector2.ONE) as Vector2
	return Rect2(position, size * scale)


func _roshan_idle_semantic_rect(world: OperaCareerWorld2D) -> Rect2:
	# Atlas cells include transparent breathing room plus expressive hair, hand,
	# and tail-tip flourishes. Those may cross a glow harmlessly. This central
	# body/tail-root footprint is the conservative semantic collision region.
	var visual_size := world.player_actor.size * world.player_actor.scale
	return Rect2(
		world.player_actor.position + visual_size * Vector2(0.27, 0.11),
		visual_size * Vector2(0.45, 0.82))


func _exercise_racer_finale(act: OperaAct, world: OperaCareerWorld2D,
		post_build_bound: int, direct_main_before: Array[int]) -> bool:
	var finale := world.phases[world._finale_start()] as Dictionary
	var racer_names: Array[String] = []
	for phase: Dictionary in world.phases:
		racer_names.append(String(phase.get("name", "")))
	_check("racer keeps the current three-beat career arc",
		world.phases.size() == 3
		and racer_names == ["TUNE", "TO THE LINE", "RACE"])
	_check("racer finale uses the exact recorded circle instruction",
		String(finale.get("vo", "")) == "op_racer_lap_two"
		and String(finale.get("voice", "")) \
			== "Loop the loop! Draw big racing circles!")
	_check("racer finale is a code-native one-finger steering turn",
		String(finale.get("mode", "")) == "circle"
		and finale.has("widget") and String(finale.get("widget", "x")).is_empty())

	# Enter the finale synchronously, then let ten seconds of normal update time
	# pass with no input. The ghost finger may teach, but it must never play.
	main.clear_dialogue()
	main.said_cool.erase("roshan_op_racer_lap_two")
	var voice_before: int = main.voice_i
	world._show_phase()
	await process_frame
	var open_player_rect := _actor_visual_rect(world.player_actor)
	var open_rival_rect := _actor_visual_rect(world.rival_actor)
	var open_activity_rect := Rect2(world.action_panel.position,
		world.action_panel.size)
	var open_finale_cast_separated := world.task_open \
		and world.player_actor.visible and world.rival_actor.visible \
		and _rect_inside(open_player_rect,
			Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)) \
		and _rect_inside(open_rival_rect,
			Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)) \
		and not open_player_rect.intersects(open_rival_rect) \
		and (not world.action_panel.visible \
			or not open_rival_rect.intersects(open_activity_rect))
	var voice_player: AudioStreamPlayer = null
	if main.voice_i > 0 and not main.voice_pool.is_empty():
		var voice_index := posmod(main.voice_i - 1, main.voice_pool.size())
		voice_player = main.voice_pool[voice_index] as AudioStreamPlayer
	var voice_path := "missing"
	if voice_player != null and voice_player.stream != null:
		voice_path = voice_player.stream.resource_path
	_check("racer finale makes one exact pooled speech request",
		main.voice_i == voice_before + 1
		and voice_path \
			== "res://assets/audio/voices/roshan_op_racer_lap_two.ogg")
	var racer_caption_hidden := not main.hud_msg.visible \
		and main.hud_msg.text.is_empty() and main.msg_timer <= 0.0
	var racer_fallback_quiet := main.voice == null or not main.voice.playing
	if not racer_caption_hidden or not racer_fallback_quiet:
		print("OPERA2D|racer voice detail|caption_visible=",
			main.hud_msg.visible, " caption=", main.hud_msg.text,
			" timer=", main.msg_timer,
			" fallback_playing=", main.voice != null and main.voice.playing,
			" exact_path=", voice_path)
	_check("recorded racer instruction needs no caption or yay fallback",
		racer_caption_hidden and racer_fallback_quiet)
	await create_timer(0.40).timeout
	var passive_progress := world.phase_progress
	for _second in range(10):
		world._process(1.0)
		world.surface._process(1.0)
	_check("ten quiet racer seconds award no progress or curtain call",
		is_equal_approx(world.phase_progress, passive_progress)
		and is_equal_approx(passive_progress, 0.0)
		and act.state == "play" and act.performance_result.is_empty())
	_check("racer finale stays visible inside the Opera Canvas world",
		world.root.visible and main.game == "opera"
		and main.kart_game == null and world.surface.mode == "circle"
		and world.action_panel.visible and world.surface.visible)
	_check("racer steering surface is large and contained by the 1280x720 stage",
		world.surface.size.x >= 176.0 and world.surface.size.y >= 176.0
		and _control_inside_stage(world.action_panel))
	_check("racer finale adds no nodes beyond its post-build Canvas bound",
		_subtree_node_count(world) <= post_build_bound)
	_check("racer owns exactly one active Canvas career world",
		get_root().find_children("*", "OperaCareerWorld2D", true, false).size() == 1)
	_check("racer finale launches no external main child",
		_direct_child_instance_ids(main) == direct_main_before)

	_drive_racer_turn(world.surface)
	_check("one honest steering turn owns the racer completion",
		world.surface.input_started and not world.surface.demo_active
		and world.surface.completion_accepted
		and (world.phase_advance_pending or act.state == "won"))
	act._process(0.05)
	world._process(2.21)
	await process_frame
	_check("racer turn returns the trophy with no placement fail branch",
		act.state == "won" and world.prop_rect.visible
		and not act.performance_result.is_empty())
	_check("racer completion never leaves Opera or adds an external runtime",
		main.game == "opera" and main.kart_game == null
		and world.root.visible and world.surface.mode == "circle"
		and _direct_child_instance_ids(main) == direct_main_before)
	return open_finale_cast_separated


func _exercise_racer_cancel_and_reentry() -> void:
	var config := _career_config("racer")
	_check("racer lifecycle fixture exists", not config.is_empty())
	if config.is_empty():
		return
	var touch_before := main.touch_ui.visible if main.touch_ui != null else false
	var direct_main_before := _direct_child_instance_ids(main)
	var interrupted_act := OperaAct.new()
	get_root().add_child(interrupted_act)
	interrupted_act.start(main, config, Callable())
	await process_frame
	var interrupted_world := interrupted_act.career_world_2d
	_check("racer lifecycle enters one Canvas world", interrupted_world != null)
	if interrupted_world == null:
		interrupted_act.cancel()
		await process_frame
		return
	interrupted_world.phase_index = interrupted_world._finale_start()
	interrupted_world.phase_progress = 0.0
	interrupted_world._show_phase()
	interrupted_world._process(3.0)
	var center := interrupted_world.surface.size * 0.5
	var radius := minf(interrupted_world.surface.size.x,
		interrupted_world.surface.size.y) * 0.32
	interrupted_world.surface._press(center + Vector2(radius, 0.0))
	interrupted_world.surface._drag(center + Vector2.from_angle(0.25) * radius)
	interrupted_world.surface._drag(center + Vector2.from_angle(0.50) * radius)
	_check("racer can be cancelled during a live one-finger turn",
		interrupted_world.surface.held and interrupted_world.phase_progress > 0.0
		and not interrupted_world.phase_advance_pending)
	var interrupted_act_ref: WeakRef = weakref(interrupted_act)
	var interrupted_world_ref: WeakRef = weakref(interrupted_world)
	var interrupted_surface_ref: WeakRef = weakref(interrupted_world.surface)
	interrupted_act.cancel()
	await process_frame
	await process_frame
	_check("mid-turn cancel frees the act, world and steering surface",
		interrupted_act_ref.get_ref() == null
		and interrupted_world_ref.get_ref() == null
		and interrupted_surface_ref.get_ref() == null)
	_check("mid-turn cancel restores touch and leaves no Opera world",
		(main.touch_ui == null or main.touch_ui.visible == touch_before)
		and get_root().find_children("*", "OperaCareerWorld2D", true, false).is_empty())
	_check("mid-turn cancel changes no direct main children",
		_direct_child_instance_ids(main) == direct_main_before)

	var fresh_act := OperaAct.new()
	get_root().add_child(fresh_act)
	fresh_act.start(main, config, Callable())
	await process_frame
	var fresh_world := fresh_act.career_world_2d
	_check("racer immediately re-enters one fresh Canvas world",
		fresh_world != null
		and get_root().find_children("*", "OperaCareerWorld2D", true, false).size() == 1)
	if fresh_world == null:
		fresh_act.cancel()
		await process_frame
		return
	fresh_world.phase_index = fresh_world._finale_start()
	fresh_world.phase_progress = 0.0
	fresh_world._show_phase()
	fresh_world._process(3.0)
	_check("fresh racer re-entry resets steering and progress",
		is_equal_approx(fresh_world.phase_progress, 0.0)
		and not fresh_world.surface.held
		and not fresh_world.surface.completion_accepted
		and fresh_world.surface.mode == "circle"
		and fresh_world.root.visible and main.game == "opera"
		and main.kart_game == null)
	_drive_racer_turn(fresh_world.surface)
	fresh_act._process(0.05)
	fresh_world._process(2.21)
	await process_frame
	_check("fresh racer re-entry can win and recover the approved trophy",
		fresh_act.state == "won" and fresh_world.prop_rect.visible
		and fresh_world.prop_rect.texture.resource_path.ends_with("/goal_racer.png")
		and not fresh_act.performance_result.is_empty())
	_check("fresh racer award adds no direct main child",
		main.kart_game == null and fresh_world.surface.mode == "circle"
		and _direct_child_instance_ids(main) == direct_main_before)
	var fresh_act_ref: WeakRef = weakref(fresh_act)
	var fresh_world_ref: WeakRef = weakref(fresh_world)
	fresh_act.cancel()
	await process_frame
	await process_frame
	_check("completed racer re-entry tears down cleanly and restores touch",
		fresh_act_ref.get_ref() == null and fresh_world_ref.get_ref() == null
		and (main.touch_ui == null or main.touch_ui.visible == touch_before)
		and get_root().find_children("*", "OperaCareerWorld2D", true, false).is_empty())


func _drive_racer_turn(surface: OperaGestureSurface) -> void:
	var center := surface.size * 0.5
	var radius := minf(surface.size.x, surface.size.y) * 0.32
	var start := center + Vector2(radius, 0.0)
	surface._press(start)
	for sample in range(1, 25):
		var angle := TAU * float(sample) / 24.0
		surface._drag(center + Vector2.from_angle(angle) * radius)
	surface._release(start)


func _career_config(costume: String) -> Dictionary:
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("costume", "")) == costume:
			return source.duplicate(true)
	return {}


func _direct_child_instance_ids(node: Node) -> Array[int]:
	var ids: Array[int] = []
	for child: Node in node.get_children():
		ids.append(int(child.get_instance_id()))
	ids.sort()
	return ids


func _subtree_node_count(node: Node) -> int:
	var count := 1
	for child: Node in node.get_children():
		count += _subtree_node_count(child)
	return count


func _has_spatial_descendants(node: Node) -> bool:
	# Keep one audited class-name sentinel instead of repeating a forbidden
	# production-medium token at every Canvas contract assertion.
	return not node.find_children("*", "Node3D", true, false).is_empty()


func _control_inside_stage(control: Control) -> bool:
	var rect := Rect2(control.position, control.size)
	return rect.position.x >= 0.0 and rect.position.y >= 0.0 \
		and rect.end.x <= 1280.0 and rect.end.y <= 720.0


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
	var exact_goals := world.phases.size() == BOXING_GOALS.size()
	var exact_voices := world.phases.size() == BOXING_VOICES.size()
	var surface_goals_match := world.phases.size() == BOXING_MODES.size()
	for index in range(mini(modes.size(), BOXING_MODES.size())):
		exact_modes = exact_modes and modes[index] == BOXING_MODES[index]
		var phase: Dictionary = world.phases[index] as Dictionary
		var phase_goal := float(phase.get("goal", -1.0))
		exact_goals = exact_goals \
			and is_equal_approx(phase_goal, BOXING_GOALS[index])
		exact_voices = exact_voices \
			and String(phase.get("vo", "")) == BOXING_VOICES[index]
		surface_goals_match = surface_goals_match \
			and int(OperaBoxingSurface.MODE_GOALS.get(modes[index], -1)) \
				== int(round(phase_goal))
	_check("boxer replaces every generic card and brawl with five glove modes",
		exact_modes and not modes.has("boxer_rhythm") and not modes.has("bop"))
	_check("boxer phase goals match every specialist glove round",
		exact_goals and surface_goals_match)
	_check("boxer preserves the exact five recorded instruction cues",
		exact_voices)
	_check("boxer waits in its room with a dedicated two-glove surface armed",
		world.surface is OperaBoxingSurface
		and world.surface.name == "BoxingGloveSurface"
		and world.station_list.size() >= BOXING_MODES.size()
		and world.station_for_phase.size() == world.phases.size()
		and not world.action_panel.visible and world.surface.armed_only
		and world.player_actor.visible
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
	if not world.task_open:
		# The shipping flow reaches and opens the next glowing room object. The
		# trusted driver performs that handoff explicitly before touching gloves.
		world._open_task()
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
	# The headless display driver never emits frame_post_draw on Windows 4.7.1;
	# waiting for it made optional CI review captures hang forever even though
	# the viewport texture was already readable.
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	if image == null:
		_check("saved review capture %s" % path.get_file(), false)
		return
	var error := image.save_png(path)
	_check("saved review capture %s" % path.get_file(), error == OK)


func _capture_control(control: Control, path: String) -> void:
	await process_frame
	await process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
	var viewport := get_root().get_viewport()
	var image: Image = viewport.get_texture().get_image()
	if image == null:
		_check("saved review capture %s" % path.get_file(), false)
		return
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
	if career == "candymaker" and mode == "pourt":
		await _capture_candymaker_pour_states(surface, prefix)
		return
	surface.demo_t = 0.92
	surface.set_timing_position(0.18)
	await _capture_control(surface, widget_shot_out.path_join("%s_idle_demo.png" % prefix))

	surface.note_input()
	surface.held = mode == "hold"
	surface.set_fill(0.45)
	if mode == "pourt":
		surface.pour_hold = true
		surface.pour_tilt = 0.58
		surface.pour_level = 0.45
		surface.pour_reserve = 0.66
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
	if mode == "pourt":
		surface.pour_hold = true
		surface.pour_tilt = 0.92
		surface.pour_level = 0.90
		surface.pour_reserve = 0.12
	surface.set_timing_position(0.68)
	surface.crank_rotation = 1.34
	await _capture_control(surface, widget_shot_out.path_join("%s_near_completion.png" % prefix))

	surface.held = false
	surface.set_fill(1.0)
	if mode == "pourt":
		surface.pour_level = 1.0
		surface.pour_reserve = 0.0
		surface.pour_hold = false
	surface.accept_completion()
	if mode == "pourt":
		# Review the real success transition rather than fabricating an upright
		# pitcher that runtime completion could not previously reach.
		surface._pour_tick(0.36)
	await _capture_control(surface, widget_shot_out.path_join("%s_accepted_completion.png" % prefix))


func _capture_candymaker_pour_states(surface: OperaGestureSurface, prefix: String) -> void:
	# Explicit story states make the visual contract reviewable: no finished candy
	# or stray target geometry can hide between the generic 45% and 90% samples.
	surface.note_input()
	surface.pour_tilt = 0.0
	surface.pour_level = 0.0
	surface.pour_reserve = 1.2
	surface.pour_hold = false
	await _capture_control(surface,
		widget_shot_out.path_join("%s_00_empty_no_demo.png" % prefix))

	surface.configure("pourt", Color(0.92, 0.58, 0.82), 1, "pour_candymaker")
	surface.demo_t = 0.92
	await _capture_control(surface,
		widget_shot_out.path_join("%s_01_idle_hint.png" % prefix))

	surface.note_input()
	surface.pour_tilt = 0.42
	surface.pour_level = 0.10
	surface.pour_reserve = 1.08
	surface.pour_hold = true
	await _capture_control(surface,
		widget_shot_out.path_join("%s_02_stream_start.png" % prefix))

	surface.pour_tilt = 0.72
	surface.pour_level = 0.50
	surface.pour_reserve = 0.60
	await _capture_control(surface,
		widget_shot_out.path_join("%s_03_half_fill.png" % prefix))

	surface.pour_tilt = 1.0
	surface.pour_level = 0.99
	surface.pour_reserve = 0.012
	await _capture_control(surface,
		widget_shot_out.path_join("%s_04_just_under_full.png" % prefix))

	surface.pour_level = 1.0
	surface.pour_reserve = 0.0
	surface.pour_hold = false
	surface.accept_completion()
	surface._pour_tick(0.36)
	await _capture_control(surface,
		widget_shot_out.path_join("%s_05_success_hold.png" % prefix))


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
