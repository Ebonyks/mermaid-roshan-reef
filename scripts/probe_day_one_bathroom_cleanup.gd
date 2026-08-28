extends SceneTree
## Deterministic Canvas/mobile contract probe for the Day One supply hunt.

const BATHROOM_CLEANUP := preload(
	"res://scripts/games/day_one_bathroom_cleanup.gd")
const BATHROOM_CLEANING := preload(
	"res://scripts/games/day_one_bathroom_cleaning.gd")
const SINK_CENTER := Vector2(642.0, 280.0)
const TUB_CENTER := Vector2(310.0, 349.0)
const RUNTIME_ASSETS: Array[String] = [
	"res://assets/opera/worlds/ui/magnifier.png",
	"res://assets/opera/worlds/props/fx_stolen_sparkle.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_bath_soap_ring.png",
	"res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_wipe_swoosh.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_sink_grime_v1.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_tub_grime_v1.png",
	"res://assets/castle/day_one_pool/activities/cleanup_basket.png",
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
	_check("two cabinet supplies are staged",
		int(snapshot.get("supply_count", 0)) == 2
		and int(snapshot.get("cabinet_target_count", 0)) == 2
		and int(snapshot.get("found_count", -1)) == 0)
	_check("one-finger drag target is generous",
		float(snapshot.get("minimum_touch_side", 0.0)) >= 160.0
		and float(snapshot.get("minimum_drag_distance", 0.0)) >= 32.0
		and bool(snapshot.get("magnifier_following_drag", false))
		and not bool(snapshot.get("guidance_discloses_target", true)))
	_check("voice and picture guidance are configured",
		bool(snapshot.get("voice_guidance_configured", false))
		and bool(snapshot.get("has_visual_pointer", false)))
	_check("rescue owns one pulsing front-right collection basket",
		bool(snapshot.get("basket_visible", false))
		and bool(snapshot.get("basket_pulsing", false))
		and bool(snapshot.get("basket_collects_supplies", false))
		and bool(snapshot.get("floating_sink_box_suppressed", false))
		and (snapshot.get("basket_position", Vector2.ZERO) as Vector2).x > 960.0
		and (snapshot.get("basket_position", Vector2.ZERO) as Vector2).y > 480.0)
	_check("ordinary HUD and room hotspots stay out of rescue",
		bool(snapshot.get("normal_hud_suppressed", false))
		and bool(snapshot.get("room_hotspots_suppressed", false)))
	_check("sink and tub grime are visible at rescue entry",
		bool(snapshot.get("dirty_overlays_visible", false))
		and bool(snapshot.get("sink_grime_visible", false))
		and bool(snapshot.get("tub_grime_visible", false)))
	_check("Canvas-only node tree",
		bool(snapshot.get("canvas_only", false))
		and _all_runtime_children_are_canvas_items(hunt))
	_check("supplies begin hidden inside cabinets",
		not (hunt.get_node("HiddenSupply_brush") as Node2D).visible
		and not (hunt.get_node("HiddenSupply_cleaner") as Node2D).visible)
	_check("normal room affordances are suppressed during rescue",
		not item_hotspots.visible and not door_hotspots.visible
		and not room_links.visible and not action_button.visible
		and bool(snapshot.get("room_hotspots_suppressed", false))
		and bool(snapshot.get("room_links_suppressed", false))
		and bool(snapshot.get("room_action_suppressed", false)))
	await create_timer(0.18).timeout
	_check("passive time cannot collect a supply",
		main.day_one_bathroom_supply_hunt_step == 0
		and found_signals == 0)
	for asset_path: String in RUNTIME_ASSETS:
		var texture: Texture2D = load(asset_path) as Texture2D
		_check("runtime asset %s" % asset_path.get_file(),
			texture != null
			and maxf(texture.get_size().x, texture.get_size().y) <= 1024.0)
	_check("wrong-position drag does not collect",
		hunt.probe_begin_drag(Vector2(84.0, 84.0))
		and hunt.probe_drag_to(Vector2(640.0, 620.0))
		and main.day_one_bathroom_supply_hunt_step == 0)
	hunt.probe_end_drag()
	_check("tap at a hidden target does not collect",
		hunt.probe_begin_drag(Vector2(138.0, 592.0))
		and main.day_one_bathroom_supply_hunt_step == 0)
	hunt.probe_end_drag()
	_check("brush requires explicit lens positioning",
		hunt.probe_reveal_supply(0)
		and main.day_one_bathroom_supply_hunt_step == 1
		and found_signals == 1)
	await create_timer(0.62).timeout
	_check("cleaner remains the only next hunt target",
		int(hunt.audit_snapshot().get("current_supply_step", -1)) == 1
		and int(hunt.audit_snapshot().get("active_target_count", 0)) == 1)
	_check("cleaner requires explicit lens positioning",
		hunt.probe_reveal_supply(1)
		and main.day_one_bathroom_supply_hunt_step == 2
		and found_signals == 2)
	await create_timer(0.62).timeout
	_check("found tools remain visibly collected in the front-right basket",
		bool(hunt.audit_snapshot().get("found_tools_visible_in_basket", false))
		and (hunt.get_node("HiddenSupply_brush") as Node2D).visible
		and (hunt.get_node("HiddenSupply_cleaner") as Node2D).visible)
	_check("hunt handoff waits for both supplies",
		hunt.is_supply_hunt_complete()
		and hunt.is_handoff_ready()
		and hunt_complete_signals == 1
		and not hunt.probe_reveal_supply(1))
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
	# progress. Mirror that order so director initialization cannot overwrite a
	# synthetic pre-director fixture value.
	restored_main._day_one_ref()
	restored_main.day_one_bathroom_supply_hunt_step = 1
	var restored: DayOneBathroomCleanup = BATHROOM_CLEANUP.new() \
		as DayOneBathroomCleanup
	host.add_child(restored)
	restored.setup(restored_main, false)
	await process_frame
	var restored_snapshot: Dictionary = restored.audit_snapshot()
	_check("re-entry restores the next unfinished supply",
		int(restored_snapshot.get("current_supply_step", -1)) == 1
		and int(restored_snapshot.get("found_count", 0)) == 1
		and (restored.get_node("HiddenSupply_brush") as Node2D).visible
		and bool(restored_snapshot.get("found_tools_visible_in_basket", false))
		and not (restored.get_node("HiddenSupply_cleaner") as Node2D).visible)
	restored_main.day_one_record_bathroom_supply_step(0)
	_check("supply persistence is monotonic",
		restored_main.day_one_bathroom_supply_hunt_step == 1)
	restored.teardown()
	await process_frame
	_probe_cleaning_gestures(host)
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
	var before: Dictionary = cleaning.audit_snapshot()
	_check("sink phase has a visible one-finger pointer",
		String(before.get("active_stage", "")) == "sink"
		and bool(before.get("has_visual_pointer", false))
		and (cleaning.get_node("GhostHandPointer") as Label).visible)
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
	cleaning_main.day_one_record_bathroom_cleanup_step(0)
	_check("cleanup persistence is monotonic",
		cleaning_main.day_one_bathroom_cleanup_step == 1)

	var tub_stage: DayOneBathroomCleaning = BATHROOM_CLEANING.new() \
		as DayOneBathroomCleaning
	host.add_child(tub_stage)
	tub_stage.setup(cleaning_main, false)
	_check("re-entry resumes tub after sink", tub_stage.is_tub_active())
	_check("tub phase keeps its visual pointer and spoken guidance seam",
		String(tub_stage.audit_snapshot().get("active_stage", "")) == "tub"
		and bool(tub_stage.audit_snapshot().get("has_visual_pointer", false))
		and (tub_stage.get_node("GhostHandPointer") as Label).visible)
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
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
	]
	_check("back-and-forth tub brush needs reversals, distance, and time",
		tub_stage.probe_tub_strokes(tub_points, 0.55)
		and cleaning_main.day_one_bathroom_cleanup_step == 2)
	# The re-entry stage shares the same bound overlays in production; bind the
	# probe's pair too so completion verifies the final tub fade, not just state.
	tub_stage.set_dirty_overlays(sink_grime, tub_grime)
	tub_stage._process(0.0)
	_check("tub grime fades away after the final scrub",
		not sink_grime.visible and not tub_grime.visible)
	_check("cleaning completion emits exactly once",
		int(cleaning_main.get_meta(
			"day_one_bathroom_cleaning_completion_count", 0)) == 1
		and not tub_stage.probe_tub_strokes(tub_points, 0.55))
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
