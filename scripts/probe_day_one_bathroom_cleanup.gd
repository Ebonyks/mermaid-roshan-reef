extends SceneTree
## Deterministic Canvas/mobile contract probe for the Day One supply hunt.

const BATHROOM_CLEANUP := preload(
	"res://scripts/games/day_one_bathroom_cleanup.gd")
const BATHROOM_CLEANING := preload(
	"res://scripts/games/day_one_bathroom_cleaning.gd")
const SINK_CENTER := Vector2(642.0, 280.0)
const TUB_CENTER := Vector2(310.0, 349.0)
const RUNTIME_ASSETS: Array[String] = [
	"res://assets/castle/day_one_pool/activities/cleanup_basket.png",
	"res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png",
	"res://assets/castle/day_one_art_studio/magic_cleaning_brush.png",
	"res://assets/castle/training/ghost_hand.png",
	"res://assets/opera/worlds/props/fx_stolen_sparkle.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_bath_soap_ring.png",
	"res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_wipe_swoosh.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_sink_grime_v1.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_tub_grime_v1.png",
]

var checks_failed: int = 0
var found_signals: int = 0
var hunt_complete_signals: int = 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var main := ReefMain.new()
	var host := Control.new()
	host.name = "DayOneBathroomSupplyProbeHost"
	host.size = StorybookUI.CANVAS_SIZE
	get_root().add_child(host)
	var item_hotspots := Control.new()
	var door_hotspots := Control.new()
	var room_links := Control.new()
	var action_button := Button.new()
	item_hotspots.name = "RoomItemHotspots"
	door_hotspots.name = "RoomDoorHotspots"
	room_links.name = "RoomLinks"
	action_button.name = "RoomAction"
	for layer: Control in [item_hotspots, door_hotspots, room_links]:
		layer.visible = true
		host.add_child(layer)
	action_button.visible = true
	host.add_child(action_button)
	main.castle_room_item_hotspot_layer = item_hotspots
	main.castle_room_door_hotspot_layer = door_hotspots
	main.castle_room_link_layer = room_links
	main.castle_room_action_button = action_button
	var hunt: DayOneBathroomCleanup = BATHROOM_CLEANUP.new() \
		as DayOneBathroomCleanup
	host.add_child(hunt)
	hunt.supply_found.connect(_on_supply_found)
	hunt.supply_hunt_completed.connect(_on_hunt_completed)
	hunt.setup(main, false)
	await process_frame
	var snapshot: Dictionary = hunt.audit_snapshot()
	_check("bathroom entry is automatically dirty and interactive",
		bool(snapshot.get("dirty_overlays_visible", false))
		and bool(snapshot.get("sink_grime_visible", false))
		and bool(snapshot.get("tub_grime_visible", false))
		and bool(snapshot.get("basket_visible", false)))
	_check("rescue has no passive win or fail state",
		not bool(snapshot.get("won", false))
		and not bool(snapshot.get("failed", false))
		and not bool(snapshot.get("game_over", false)))
	_check("rescue owns one pulsing front-right basket",
		bool(snapshot.get("basket_visible", false))
		and bool(snapshot.get("basket_pulsing", false))
		and bool(snapshot.get("basket_collects_supplies", false))
		and bool(snapshot.get("floating_sink_box_suppressed", false))
		and (snapshot.get("basket_position", Vector2.ZERO) as Vector2).x > 760.0
		and (snapshot.get("basket_position", Vector2.ZERO) as Vector2).y > 480.0)
	_check("basket contains sponge and brush, never cleaner",
		(snapshot.get("basket_item_ids", []) as Array) == ["sponge", "brush"]
		and not (snapshot.get("basket_item_ids", []) as Array).has("cleaner"))
	_check("no magnifier or cabinet search route exists",
		not bool(snapshot.get("magnifier_following_drag", false))
		and int(snapshot.get("cabinet_target_count", 0)) == 0
		and not bool(snapshot.get("cabinet_search_active", false)))
	_check("basket tap has spoken and visual invitation",
		bool(snapshot.get("basket_tap_prompt_voice", false))
		and bool(snapshot.get("basket_tap_prompt_visual", false)))
	_check("ordinary HUD and room hotspots stay out of rescue",
		bool(snapshot.get("normal_hud_suppressed", false))
		and bool(snapshot.get("room_hotspots_suppressed", false)))
	_check("Canvas-only node tree",
		bool(snapshot.get("canvas_only", false))
		and _all_runtime_children_are_canvas_items(hunt))
	_check("normal room affordances are suppressed during rescue",
		not item_hotspots.visible and not door_hotspots.visible
		and not room_links.visible and not action_button.visible
		and bool(snapshot.get("room_hotspots_suppressed", false))
		and bool(snapshot.get("room_links_suppressed", false))
		and bool(snapshot.get("room_action_suppressed", false)))
	await create_timer(0.18).timeout
	_check("passive time cannot collect a supply",
		main.day_one_bathroom_supply_hunt_step == 0
		and found_signals == 0
		and main.day_one_bathroom_cleanup_step == 0)
	for asset_path: String in RUNTIME_ASSETS:
		var texture: Texture2D = load(asset_path) as Texture2D
		_check("runtime asset %s" % asset_path.get_file(),
			texture != null
			and maxf(texture.get_size().x, texture.get_size().y) <= 1024.0)
	var basket_tap_result: Variant = null
	if hunt.has_method("probe_tap_basket"):
		basket_tap_result = hunt.call("probe_tap_basket")
	_check("real basket tap starts the rescue handoff",
		hunt.has_method("probe_tap_basket")
		and bool(basket_tap_result)
		and bool(hunt.audit_snapshot().get("basket_tap_count", 0))
		and not bool(hunt.audit_snapshot().get(
			"basket_tap_pointer_visible", true)))
	await create_timer(0.48).timeout
	var tapped_snapshot: Dictionary = hunt.audit_snapshot()
	_check("sponge travels from basket toward the sink",
		bool(tapped_snapshot.get("sponge_travel_complete", false))
		and bool(tapped_snapshot.get("sink_circle_demo_visible", false)))
	_check("basket tap does not expose a magnifier or cabinet target",
		not bool(tapped_snapshot.get("magnifier_following_drag", false))
		and int(tapped_snapshot.get("cabinet_target_count", 0)) == 0)
	_check("hunt handoff opens the sink gesture without a fail state",
		bool(hunt.is_handoff_ready())
		and bool(hunt.cleaning_audit_snapshot().get("active", false))
		and not bool(hunt.cleaning_audit_snapshot().get("failed", false)))
	_check("supply hunt does not unlock the pool",
		main.day_one_current_room_id == "bathroom"
		and main.day_one_bathroom_cleanup_step == 0)
	_check("partial bathroom completion is rejected",
		not main.day_one_complete_bathroom_scene()
		and main.day_one_current_room_id == "bathroom")
	_check("rejected pool overlay remains absent",
		not FileAccess.file_exists("res://scripts/castle_pool_surface_life.gd")
		and not FileAccess.file_exists(
			"res://assets/shaders/castle_pool_surface_life.gdshader"))
	hunt.teardown()
	await process_frame
	_check("teardown frees hunt", not is_instance_valid(hunt))
	_check("normal room affordances restore after rescue teardown",
		item_hotspots.visible and door_hotspots.visible and room_links.visible
		and action_button.visible)

	var restored_main := ReefMain.new()
	# Production constructs the director before a room overlay can restore its
	# progress. Mirror that order so a mid-gesture save resumes the tub.
	restored_main._day_one_ref()
	restored_main.day_one_bathroom_cleanup_step = 1
	var restored: DayOneBathroomCleaning = BATHROOM_CLEANING.new() \
		as DayOneBathroomCleaning
	host.add_child(restored)
	restored.setup(restored_main, false)
	await process_frame
	var restored_snapshot: Dictionary = restored.audit_snapshot()
	_check("re-entry restores the next unfinished brush gesture",
		int(restored_snapshot.get("active_step", -1)) == 1
		and bool(restored_snapshot.get("has_visual_pointer", false)))
	restored_main.day_one_record_bathroom_cleanup_step(0)
	_check("cleanup persistence is monotonic on re-entry",
		restored_main.day_one_bathroom_cleanup_step == 1)
	restored.teardown()
	await process_frame
	await _probe_cleaning_gestures(host)
	host.queue_free()
	main.free()
	restored_main.free()
	print("DAY_ONE_BATHROOM|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _probe_cleaning_gestures(host: Control) -> void:
	var cleaning_main := ReefMain.new()
	var cleaning: DayOneBathroomCleaning = BATHROOM_CLEANING.new() \
		as DayOneBathroomCleaning
	host.add_child(cleaning)
	cleaning.setup(cleaning_main, false)
	var sink_grime := Sprite2D.new()
	var tub_grime := Sprite2D.new()
	host.add_child(sink_grime)
	host.add_child(tub_grime)
	cleaning.set_dirty_overlays(sink_grime, tub_grime)
	cleaning.set_supply_basket(Vector2(1130.0, 590.0))
	await create_timer(0.42).timeout
	var before: Dictionary = cleaning.audit_snapshot()
	_check("sink phase has a visible one-finger pointer",
		String(before.get("active_stage", "")) == "sink"
		and bool(before.get("has_visual_pointer", false))
		and (cleaning.get_node("GhostHandPointer") as Sprite2D).visible
		and tub_grime.visible)
	_check("sink phase shows a circle demo and travelling sponge",
		bool(before.get("circle_demo_visible", false))
		and bool(before.get("sponge_travel_complete", false)))
	cleaning._process(4.0)
	var after_wait: Dictionary = cleaning.audit_snapshot()
	_check("passive wait does not advance sink",
		int(after_wait["active_step"]) == int(before["active_step"])
		and float(after_wait["sink_arc"]) == float(before["sink_arc"]))
	_check("sink early motion does not complete",
		cleaning.probe_begin_gesture(SINK_CENTER + Vector2(120.0, 0.0))
		and cleaning.probe_gesture_to(
			SINK_CENTER + Vector2(0.0, 120.0), 0.25)
		and cleaning.probe_gesture_to(
			SINK_CENTER + Vector2(-120.0, 0.0), 0.25)
		and int(cleaning.audit_snapshot()["active_step"]) == 0)
	cleaning.probe_end_gesture()
	var sink_points: Array[Vector2] = []
	for index: int in range(49):
		var angle: float = float(index) / 48.0 * TAU * 1.2
		sink_points.append(SINK_CENTER \
			+ Vector2(cos(angle), sin(angle)) * 120.0)
	_check("circular sink scrub needs arc, distance, and valid motion time",
		cleaning.probe_sink_circle(sink_points, 0.06)
		and cleaning_main.day_one_bathroom_cleanup_step == 1)
	cleaning._process(0.0)
	_check("sink grime fades away and tub grime becomes the next target",
		not sink_grime.visible and tub_grime.visible
		and float(cleaning.audit_snapshot()["grime_fade_progress"]["sink"])
		>= 1.0)
	await create_timer(0.76).timeout
	_check("sink completion leaves a clean visible basin",
		not bool(cleaning.audit_snapshot().get("sink_grime_visible", true))
		and bool(cleaning.audit_snapshot().get("brush_travel_complete", false)))
	cleaning_main.day_one_record_bathroom_cleanup_step(0)
	_check("cleanup persistence is monotonic",
		cleaning_main.day_one_bathroom_cleanup_step == 1)

	var tub_stage: DayOneBathroomCleaning = BATHROOM_CLEANING.new() \
		as DayOneBathroomCleaning
	host.add_child(tub_stage)
	tub_stage.setup(cleaning_main, false)
	tub_stage.set_supply_basket(Vector2(1130.0, 590.0))
	await create_timer(0.42).timeout
	_check("re-entry resumes tub after sink", tub_stage.is_tub_active())
	_check("tub phase keeps its visual pointer and spoken guidance seam",
		String(tub_stage.audit_snapshot().get("active_stage", "")) == "tub"
		and bool(tub_stage.audit_snapshot().get("has_visual_pointer", false))
		and (tub_stage.get_node("GhostHandPointer") as Sprite2D).visible
		and bool(tub_stage.audit_snapshot().get("back_and_forth_arrows_visible", false))
		and bool(tub_stage.audit_snapshot().get("brush_travel_complete", false)))
	var before_tub_wait: Dictionary = tub_stage.audit_snapshot()
	tub_stage._process(4.0)
	var after_tub_wait: Dictionary = tub_stage.audit_snapshot()
	_check("passive wait does not advance tub",
		int(after_tub_wait["active_step"]) == 1
		and float(after_tub_wait["tub_distance"])
			== float(before_tub_wait["tub_distance"])
		and int(after_tub_wait["tub_reversals"])
			== int(before_tub_wait["tub_reversals"]))
	var tub_circle: Array[Vector2] = []
	for index: int in range(49):
		var tub_angle: float = float(index) / 48.0 * TAU
		tub_circle.append(TUB_CENTER \
			+ Vector2(cos(tub_angle), sin(tub_angle)) * 110.0)
	_check("circular sink motion cannot complete the tub",
		not tub_stage.probe_tub_strokes(tub_circle, 0.06)
		and tub_stage.is_tub_active())
	var tub_points: Array[Vector2] = [
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
	]
	_check("back-and-forth tub brush needs reversals, distance, and time",
		tub_stage.probe_tub_strokes(tub_points, 1.1)
		and cleaning_main.day_one_bathroom_cleanup_step == 2)
	_check("two-to-three forgiving tub strokes are enough",
		int(tub_stage.audit_snapshot().get("tub_reversals", 0)) <= 3)
	# The re-entry stage shares the same bound overlays in production; bind the
	# probe's pair too so completion verifies the final tub fade, not just state.
	tub_stage.set_dirty_overlays(sink_grime, tub_grime)
	tub_stage._process(0.0)
	_check("tub grime fades away after the final scrub",
		not sink_grime.visible and not tub_grime.visible)
	await create_timer(0.98).timeout
	_check("cleaning completion emits exactly once",
		int(cleaning_main.get_meta(
			"day_one_bathroom_cleaning_completion_count", 0)) == 1
		and not tub_stage.probe_tub_strokes(tub_points, 0.55))
	_check("finale has whole-room sparkle and pool pointer seam",
		bool(tub_stage.audit_snapshot().get("whole_room_sparkle", false))
		and bool(tub_stage.audit_snapshot().get("pool_pointer_ready", false)))
	_check("cleaning exposes no fail state",
		not bool(tub_stage.audit_snapshot().get("failed", false))
		and not bool(tub_stage.audit_snapshot().get("game_over", false)))
	var final_snapshot: Dictionary = tub_stage.audit_snapshot()
	_check("cleaning gestures are reachable, Canvas-only, and budgeted 2-5s",
		bool(final_snapshot["canvas_only"])
		and bool(final_snapshot["sink_gesture_reachable"])
		and bool(final_snapshot["tub_gesture_reachable"])
		and float(final_snapshot["gesture_budget"]["sink_min_seconds"]) >= 2.0
		and float(final_snapshot["gesture_budget"]["sink_max_seconds"]) <= 5.0
		and float(final_snapshot["gesture_budget"]["tub_min_seconds"]) >= 2.0
		and float(final_snapshot["gesture_budget"]["tub_max_seconds"]) <= 5.0)

	var interrupted_main := ReefMain.new()
	interrupted_main._day_one_ref()
	interrupted_main.day_one_bathroom_cleanup_step = 2
	var interrupted: DayOneBathroomCleaning = BATHROOM_CLEANING.new() \
		as DayOneBathroomCleaning
	host.add_child(interrupted)
	interrupted.setup(interrupted_main, false)
	_check("interrupted completed tub re-emits completion once",
		bool(interrupted.audit_snapshot()["completion_sent"])
		and int(interrupted_main.get_meta(
			"day_one_bathroom_cleaning_completion_count", 0)) == 1)
	cleaning.teardown()
	tub_stage.teardown()
	interrupted.teardown()
	cleaning_main.free()
	interrupted_main.free()


func _on_supply_found(_index: int, _supply_id: String) -> void:
	found_signals += 1


func _on_hunt_completed() -> void:
	hunt_complete_signals += 1


func _all_runtime_children_are_canvas_items(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem \
				or not _all_runtime_children_are_canvas_items(child):
			return false
	return true


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_BATHROOM|", label, ": ", "OK" if ok else "FAIL")
