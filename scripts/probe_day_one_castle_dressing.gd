extends SceneTree
## Focused headless contract probe for DayOneCastleDressing.

const DRESSING := preload("res://scripts/arena/day_one_castle_dressing.gd")


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var bad := 0
	var host := Node2D.new()
	host.name = "DayOneDressingProbeHost"
	get_root().add_child(host)
	var dressing: DayOneCastleDressing = DRESSING.create_dressing(host)
	await process_frame
	var snapshot: Dictionary = dressing.audit_snapshot()
	var expected_rooms: Array[String] = [
		"bubble_bath", "mermaid_pool", "playroom", "craft_room",
	]
	if dressing.room_ids() != expected_rooms or int(snapshot.get("room_count", 0)) != 4:
		print("DAY_ONE_DRESSING|rooms: FAIL ", snapshot)
		bad += 1
	else:
		print("DAY_ONE_DRESSING|rooms: OK four rooms")
	if int(snapshot.get("dirty_room_count", 0)) != 4 \
			or not bool(snapshot.get("exterior_grime", false)) \
			or not bool(snapshot.get("interior_disrepair", false)) \
			or int(snapshot.get("dust_bunny_count", 0)) != 4:
		print("DAY_ONE_DRESSING|interior overlay: FAIL")
		bad += 1
	else:
		print("DAY_ONE_DRESSING|interior overlay: OK four dirty rooms")
	if int(snapshot.get("readable_door_count", 0)) != 4 \
			or String(snapshot.get("door_visual_owner", "")) != "castle_rooms" \
			or bool(snapshot.get("independent_door_glows", true)):
		print("DAY_ONE_DRESSING|door handoff: FAIL ", snapshot)
		bad += 1
	else:
		print("DAY_ONE_DRESSING|door handoff: OK no independent glows")
	if not bool(snapshot.get("procedural_canvas", false)) \
			or not bool(snapshot.get("dust_bunny_sprite2d", false)) \
			or not bool(snapshot.get("canvas_only", false)):
		print("DAY_ONE_DRESSING|2D contract: FAIL ", snapshot)
		bad += 1
	else:
		print("DAY_ONE_DRESSING|2D contract: OK")
	dressing.set_visible_room("mermaid_pool")
	dressing.update_dressing(0.25)
	var land_snapshot: Dictionary = dressing.audit_snapshot().get(
		"pool_land_bunny", {}) as Dictionary
	if int(land_snapshot.get("count", 0)) != 1 \
			or not bool(land_snapshot.get("landlocked", false)) \
			or not String(land_snapshot.get("asset", "")).ends_with(
				"dust_bunny_curl_ears.png"):
		print("DAY_ONE_DRESSING|pool shore bunny: FAIL ", land_snapshot)
		bad += 1
	else:
		print("DAY_ONE_DRESSING|pool shore bunny: OK one landlocked cutout")
	dressing.set_visible_room("bubble_bath")
	dressing.update_dressing(0.25)
	var bathroom_bunny: Sprite2D = dressing.get_node("DustBunny_bubble_bath") as Sprite2D
	if not bathroom_bunny.visible:
		print("DAY_ONE_DRESSING|approved bunny: FAIL room-visible card hidden")
		bad += 1
	else:
		print("DAY_ONE_DRESSING|approved bunny: OK visible room card")
	dressing.set_room_dirty("mermaid_pool", false)
	dressing.set_door_unlocked("mermaid_pool", true)
	dressing.set_visible_room("mermaid_pool")
	dressing.update_dressing(0.25)
	var pool_bunny: Sprite2D = dressing.get_node("DustBunny_mermaid_pool") as Sprite2D
	if dressing.room_is_dirty("mermaid_pool") or pool_bunny.visible \
			or not dressing.door_is_unlocked("mermaid_pool"):
		print("DAY_ONE_DRESSING|clean room visibility: FAIL")
		bad += 1
	else:
		print("DAY_ONE_DRESSING|clean room visibility: OK bunny hidden")
	dressing.set_visible_room("main_hall")
	dressing.set_room_door_rect(
		"bubble_bath", Rect2(88.0, 210.0, 126.0, 260.0))
	dressing.activate_boss_back_door()
	dressing.update_dressing(0.25)
	var active_snapshot: Dictionary = dressing.audit_snapshot()
	if not dressing.boss_back_door_is_active() \
			or dressing.visible_room_id() != "main_hall" \
			or int(active_snapshot.get("visible_hall_door_count", -1)) != 1 \
			or int(active_snapshot.get("dirty_room_count", -1)) != 3 \
			or int(active_snapshot.get("unlocked_door_count", -1)) != 1:
		print("DAY_ONE_DRESSING|state update: FAIL ", active_snapshot)
		bad += 1
	else:
		print("DAY_ONE_DRESSING|state update: OK")
	dressing.teardown()
	await process_frame
	if is_instance_valid(dressing):
		print("DAY_ONE_DRESSING|teardown: FAIL node still valid")
		bad += 1
	else:
		print("DAY_ONE_DRESSING|teardown: OK")
	host.queue_free()
	print("DAY_ONE_DRESSING|result: ", ("ALL OK" if bad == 0 else "%d failure(s)" % bad))
	quit(bad)
