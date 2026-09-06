class_name DayOnePoolCleanup
extends Control
## Three bespoke, one-finger cleanup activities for Day One's Mermaid Pool.
## Persistent progress stays on ReefMain; legacy completion remains step 4.

signal cleanup_step_completed(step: int, cleanup_id: String)
signal finale_started
signal reveal_completed

const POOL_SKIMMER_ACTIVITY := preload(
	"res://scripts/games/pool_skimmer_activity.gd")
const POOL_WATERFALL_ACTIVITY := preload(
	"res://scripts/games/pool_waterfall_activity.gd")
const POOL_SEAHORSE_ACTIVITY := preload(
	"res://scripts/games/pool_seahorse_rescue_activity.gd")
const DUST_BUNNY_SWIMMER := preload(
	"res://scripts/games/day_one_dust_bunny_swimmer.gd")
const ACTIVITY_IDS: Array[String] = ["pool_surface", "waterfall", "seahorse"]
const LEGACY_COMPLETE_STEP := 4
const ART_TO_STAGE := 1.25
const WATERFALL_FALLBACK_CENTER := Vector2(461.875, 216.25)
const WATERFALL_FALLBACK_SIZE := Vector2(162.5, 220.0)
const SEAHORSE_FALLBACK_CENTER := Vector2(921.875, 245.625)
const SEAHORSE_FALLBACK_SIZE := Vector2(208.75, 241.25)
const RUMI_POOL_ATLAS := \
	"res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png"
const RUMI_POSE_ATLAS := \
	"res://assets/characters/rumi/rumi_eight_pose_runtime.png"
const RUMI_POOL_CELL_SIZE := Vector2(256.0, 256.0)
const RUMI_POSE_CELL_SIZE := Vector2(256.0, 384.0)
const RUMI_SWIM_SCALE := 1.02
const RUMI_UPRIGHT_START_SCALE := 0.83
const RUMI_UPRIGHT_SCALE := 0.96
const DINGY_ROOM_TINT := Color(0.78, 0.86, 0.76, 1.0)
const SWIMMER_WATER_BOUNDS := Rect2(300.0, 285.0, 680.0, 235.0)
const SWIMMER_START := Vector2(820.0, 455.0)
const SKIMMER_PICKUP_CAPTIONS: Array[String] = [
	"One leaf scooped!", "Another leaf is gone!", "The water looks clearer!",
	"Scoop, scoop!", "Almost sparkling!", "The last leaf is out!",
]
const WATERFALL_LANE_CAPTIONS: Array[String] = [
	"The left waterfall lane is clear!", "The middle waterfall lane is clear!",
	"The right waterfall lane is clear!",
]
const SKIMMER_CUE_IDS: Array[String] = [
	"day1_pool_skimmer_01", "day1_pool_skimmer_02", "day1_pool_skimmer_03",
	"day1_pool_skimmer_04", "day1_pool_skimmer_05", "day1_pool_skimmer_06",
]
const WATERFALL_CUE_IDS: Array[String] = [
	"day1_pool_waterfall_lane_left", "day1_pool_waterfall_lane_center",
	"day1_pool_waterfall_lane_right",
]

var m: ReefMain
var skimmer_activity: PoolSkimmerActivity = null
var waterfall_activity: PoolWaterfallActivity = null
var seahorse_activity: PoolSeahorseRescueActivity = null
var _phase: int = 0
var _busy: bool = false
var _finale_started: bool = false
var _announcements_enabled: bool = true
var _lighting_target: CanvasItem = null
var _lighting_target_rest_modulate := Color.WHITE
var _rumi: AnimatedSprite2D = null
var _swimming_bunny: DayOneDustBunnySwimmer = null
var _clean_waterfall: Sprite2D = null
var _healthy_seahorse: Sprite2D = null
var _hidden_fixture_items: Array[Dictionary] = []
var _interaction_layer_visibility: Array[Dictionary] = []
var _announced_skimmer_mask: int = 0
var _announced_waterfall_mask: int = 0
var _announced_seahorse_milestone: int = 0


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	_announce_progress_from_save()
	name = "DayOnePoolCleanup"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 0
	# The owner mounts the controller on the room stage for lifecycle ownership.
	# Move this activity under the authored world root so its explicit z values
	# interleave with Roshan and the foreground instead of becoming screen UI.
	if m.castle_room_world_root != null and get_parent() != m.castle_room_world_root:
		reparent(m.castle_room_world_root)
	_capture_interaction_layers()
	_capture_room_lighting()
	_capture_clean_waterfall()
	_capture_healthy_seahorse()
	_build_swimming_dust_bunny()
	_build_activities()
	_phase = _phase_from_legacy_step(m.day_one_pool_cleanup_step)
	_apply_restored_progress()
	if _phase >= ACTIVITY_IDS.size():
		call_deferred("_begin_finale")
	else:
		call_deferred("_announce_current_activity")


func teardown() -> void:
	_stop_activities()
	_restore_interaction_layers()
	if _lighting_target != null and is_instance_valid(_lighting_target):
		_lighting_target.modulate = _lighting_target_rest_modulate
	if _clean_waterfall != null and is_instance_valid(_clean_waterfall):
		_clean_waterfall.visible = true
	if _healthy_seahorse != null and is_instance_valid(_healthy_seahorse):
		_healthy_seahorse.visible = true
	for record: Dictionary in _hidden_fixture_items:
		var item: CanvasItem = record.get("item") as CanvasItem
		if item != null and is_instance_valid(item):
			item.visible = bool(record.get("was_visible", true))
	_hidden_fixture_items.clear()
	if is_inside_tree():
		queue_free()
	else:
		free()


func _capture_interaction_layers() -> void:
	_interaction_layer_visibility.clear()
	for interaction_layer: CanvasItem in [m.castle_room_item_hotspot_layer,
			m.castle_room_door_hotspot_layer, m.castle_room_link_layer]:
		if interaction_layer == null:
			continue
		_interaction_layer_visibility.append({
			"layer": interaction_layer,
			"visible": interaction_layer.visible,
		})
		interaction_layer.visible = false


func _restore_interaction_layers() -> void:
	for visibility_record: Dictionary in _interaction_layer_visibility:
		var interaction_layer: CanvasItem = visibility_record.get("layer") as CanvasItem
		if interaction_layer != null and is_instance_valid(interaction_layer):
			interaction_layer.visible = bool(
				visibility_record.get("visible", true))
	_interaction_layer_visibility.clear()


func audit_snapshot() -> Dictionary:
	return {
		"activity_count": ACTIVITY_IDS.size(),
		"activity_ids": ACTIVITY_IDS.duplicate(),
		"current_activity_index": _phase,
		"current_activity": ACTIVITY_IDS[_phase]
			if _phase < ACTIVITY_IDS.size() else "complete",
		"legacy_completion_step": LEGACY_COMPLETE_STEP,
		"seahorse_is_last": ACTIVITY_IDS[-1] == "seahorse",
		"standalone_pool_rim_gate": false,
		"dingy_lighting": _lighting_target != null,
		"finale_started": _finale_started,
		"clean_waterfall_visible": _clean_waterfall != null
			and is_instance_valid(_clean_waterfall) and _clean_waterfall.visible,
		"animated_water_hidden": _animated_fixture_water_hidden(),
		"waterfall_center": _waterfall_fixture_center(),
		"waterfall_size": _waterfall_fixture_size(),
		"skimmer": skimmer_activity.audit_snapshot()
			if skimmer_activity != null else {},
		"waterfall": waterfall_activity.audit_snapshot()
			if waterfall_activity != null else {},
		"seahorse": seahorse_activity.audit_snapshot()
			if seahorse_activity != null else {},
		"rumi_present": _rumi != null and is_instance_valid(_rumi),
		"rumi_approved_identity": _rumi != null and is_instance_valid(_rumi)
			and bool(_rumi.get_meta("approved_private_canon", false)),
		"rumi_authored_animation": _rumi != null and is_instance_valid(_rumi)
			and _rumi.sprite_frames != null
			and _rumi.sprite_frames.get_frame_count(&"idle") == 2
			and _rumi.sprite_frames.get_frame_count(&"wave") == 2
			and _rumi.sprite_frames.get_frame_count(&"swim") == 4,
		"rumi_animation": String(_rumi.animation)
			if _rumi != null and is_instance_valid(_rumi) else "",
		"dust_bunny_count": 2,
		"land_bunny_owner": "day_one_castle_dressing",
		"swimming_bunny": _swimming_bunny.audit_snapshot()
			if _swimming_bunny != null and is_instance_valid(_swimming_bunny)
			else {},
		"canvas_only": true,
		"no_fail": true,
	}


func probe_complete_current_activity() -> bool:
	if _busy or _phase >= ACTIVITY_IDS.size():
		return false
	match _phase:
		0:
			while skimmer_activity.probe_collect_next():
				pass
		1:
			while waterfall_activity.probe_clear_next_lane():
				pass
		2:
			while seahorse_activity.probe_tap():
				pass
	return true


func cancel_touch() -> void:
	if skimmer_activity != null:
		skimmer_activity.cancel_touch()
	if waterfall_activity != null:
		waterfall_activity.cancel_touch()
	if seahorse_activity != null:
		seahorse_activity.cancel_touch()


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		cancel_touch()


func _capture_room_lighting() -> void:
	# Tint the authored room and cleanup cast together. A full-screen ColorRect
	# made the activity read as a translucent modal pasted over the V4 room.
	_lighting_target = m.castle_room_world_root as CanvasItem \
		if m != null and m.castle_room_world_root != null else self
	_lighting_target_rest_modulate = _lighting_target.modulate
	_lighting_target.set_meta("day_one_pool_dingy_lighting", true)


func _capture_clean_waterfall() -> void:
	var record: Dictionary = m.castle_room_item_sprites.get(
		"waterfall", {}) as Dictionary
	_clean_waterfall = record.get("sprite") as Sprite2D
	if _clean_waterfall != null:
		_clean_waterfall.visible = false
	_capture_fixture_water(record)


func _capture_healthy_seahorse() -> void:
	var record: Dictionary = m.castle_room_item_sprites.get(
		"seahorse_fountain", {}) as Dictionary
	_healthy_seahorse = record.get("sprite") as Sprite2D
	if _healthy_seahorse != null:
		_healthy_seahorse.visible = false
	_capture_fixture_water(record)


func _capture_fixture_water(record: Dictionary) -> void:
	var fixture_rig: Dictionary = record.get("fixture_rig", {}) as Dictionary
	for water_value: Variant in fixture_rig.get("water", []):
		var water: Dictionary = water_value as Dictionary
		var water_item: CanvasItem = water.get("node") as CanvasItem
		if water_item == null:
			continue
		_hidden_fixture_items.append({
			"item": water_item,
			"was_visible": water_item.visible,
		})
		water_item.visible = false


func _build_activities() -> void:
	skimmer_activity = POOL_SKIMMER_ACTIVITY.new() as PoolSkimmerActivity
	skimmer_activity.name = "SkimThePool"
	skimmer_activity.position = Vector2.ZERO
	skimmer_activity.size = StorybookUI.CANVAS_SIZE
	skimmer_activity.z_index = 210
	skimmer_activity.setup(m.day_one_pool_skimmer_mask)
	skimmer_activity.progress_changed.connect(_on_skimmer_progress)
	skimmer_activity.completed.connect(_on_skimmer_completed)
	add_child(skimmer_activity)
	skimmer_activity.bind_room_actor(m.castle_room_player_sprite,
		m.castle_room_player_shadow as Sprite2D, m.skin_id)

	waterfall_activity = POOL_WATERFALL_ACTIVITY.new() as PoolWaterfallActivity
	waterfall_activity.name = "ClearTheWaterfall"
	waterfall_activity.position = Vector2.ZERO
	waterfall_activity.size = StorybookUI.CANVAS_SIZE
	waterfall_activity.z_index = 70
	waterfall_activity.setup(_waterfall_fixture_center(),
		_waterfall_fixture_size(), m.day_one_pool_waterfall_mask)
	waterfall_activity.progress_changed.connect(_on_waterfall_progress)
	waterfall_activity.completed.connect(_on_waterfall_completed)
	add_child(waterfall_activity)

	seahorse_activity = POOL_SEAHORSE_ACTIVITY.new() as PoolSeahorseRescueActivity
	seahorse_activity.name = "HelpTheSeahorse"
	seahorse_activity.position = Vector2.ZERO
	seahorse_activity.size = StorybookUI.CANVAS_SIZE
	seahorse_activity.z_index = 70
	seahorse_activity.setup(_seahorse_fixture_center(),
		_seahorse_fixture_size(), m.day_one_pool_seahorse_tugs)
	seahorse_activity.progress_changed.connect(_on_seahorse_progress)
	seahorse_activity.completed.connect(_on_seahorse_completed)
	add_child(seahorse_activity)


func _build_swimming_dust_bunny() -> void:
	_swimming_bunny = DUST_BUNNY_SWIMMER.new() as DayOneDustBunnySwimmer
	add_child(_swimming_bunny)
	if not _swimming_bunny.setup(
			SWIMMER_WATER_BOUNDS, SWIMMER_START, 118.0, Vector2(52.0, 12.0),
			205, Vector2(94.0, 20.0), Color(0.58, 0.88, 0.90, 0.18)):
		_swimming_bunny.queue_free()
		_swimming_bunny = null


func _apply_restored_progress() -> void:
	_stop_activities()
	skimmer_activity.visible = _phase == 0
	waterfall_activity.visible = _phase < 2
	seahorse_activity.visible = _phase < 3
	if _clean_waterfall != null and is_instance_valid(_clean_waterfall):
		_clean_waterfall.visible = _phase >= 1
	if _healthy_seahorse != null and is_instance_valid(_healthy_seahorse):
		_healthy_seahorse.visible = _phase >= 3
	match _phase:
		0:
			skimmer_activity.start()
		1:
			waterfall_activity.start()
		2:
			seahorse_activity.start()
	_update_dingy_lighting()


func _stop_activities() -> void:
	if skimmer_activity != null:
		skimmer_activity.stop()
	if waterfall_activity != null:
		waterfall_activity.stop()
	if seahorse_activity != null:
		seahorse_activity.stop()


func _on_skimmer_progress(mask: int) -> void:
	if m == null:
		return
	var newly_collected: int = mask & ~_announced_skimmer_mask
	for index: int in range(SKIMMER_PICKUP_CAPTIONS.size()):
		if (newly_collected & (1 << index)) != 0:
			_say_context(SKIMMER_CUE_IDS[index],
				SKIMMER_PICKUP_CAPTIONS[index],
				"day_one")
	_announced_skimmer_mask = mask
	m.day_one_record_pool_activity_progress(
		mask, m.day_one_pool_waterfall_mask, m.day_one_pool_seahorse_tugs)
	m._ui_tap()
	_update_dingy_lighting()


func _on_skimmer_completed() -> void:
	if _phase != 0 or _busy:
		return
	_busy = true
	await get_tree().create_timer(0.58).timeout
	_say_context("day1_pool_skimmer_complete", "The pool surface is clear!",
		"day_one")
	_commit_activity(1, "pool_surface")


func _on_waterfall_progress(mask: int) -> void:
	if m == null:
		return
	var newly_cleared: int = mask & ~_announced_waterfall_mask
	for lane: int in range(WATERFALL_LANE_CAPTIONS.size()):
		if (newly_cleared & (1 << lane)) != 0:
			_say_context(WATERFALL_CUE_IDS[lane],
				WATERFALL_LANE_CAPTIONS[lane],
				"day_one")
	_announced_waterfall_mask = mask
	m.day_one_record_pool_activity_progress(
		m.day_one_pool_skimmer_mask, mask, m.day_one_pool_seahorse_tugs)
	m._ui_tap()
	_update_dingy_lighting()


func _on_waterfall_completed() -> void:
	if _phase != 1 or _busy:
		return
	_busy = true
	await get_tree().create_timer(0.42).timeout
	_say_context("day1_pool_waterfall_complete",
		"All three waterfall lanes are clear!", "day_one")
	_commit_activity(2, "waterfall")


func _on_seahorse_progress(taps: int) -> void:
	if m == null:
		return
	if taps >= 1 and _announced_seahorse_milestone < 1:
		_announced_seahorse_milestone = 1
		_say_context("day1_pool_seahorse_early", "A little tug! Keep going!",
			"day_one")
	if taps >= 4 and _announced_seahorse_milestone < 2:
		_announced_seahorse_milestone = 2
		_say_context("day1_pool_seahorse_middle", "We are halfway there!",
			"day_one")
	if taps >= 7 and _announced_seahorse_milestone < 3:
		_announced_seahorse_milestone = 3
		_say_context("day1_pool_seahorse_final", "One more tug!",
			"day_one")
	m.day_one_record_pool_activity_progress(
		m.day_one_pool_skimmer_mask, m.day_one_pool_waterfall_mask, taps)
	m._ui_tap()
	_update_dingy_lighting()


func _on_seahorse_completed() -> void:
	if _phase != 2 or _busy:
		return
	_busy = true
	if _healthy_seahorse != null and is_instance_valid(_healthy_seahorse):
		_healthy_seahorse.visible = true
	_announced_seahorse_milestone = 4
	_say_context("day1_pool_seahorse_free", "The seahorse is free!", "day_one")
	_commit_activity(LEGACY_COMPLETE_STEP, "seahorse")


func _commit_activity(legacy_step: int, activity_id: String) -> void:
	if m == null:
		_busy = false
		return
	_phase += 1
	m.day_one_record_pool_cleanup_step(legacy_step)
	cleanup_step_completed.emit(legacy_step, activity_id)
	# Completion is a save boundary, not another debounce event. The child can
	# leave or the app can be suspended immediately after the activity resolves;
	# persist the monotonic mask/step before swapping the next activity in.
	m._write_save()
	_busy = false
	_apply_restored_progress()
	if _phase >= ACTIVITY_IDS.size():
		_begin_finale()
	else:
		_announce_current_activity()


func _announce_current_activity() -> void:
	if not _announcements_enabled or m == null \
			or _phase >= ACTIVITY_IDS.size():
		return
	match ACTIVITY_IDS[_phase]:
		"pool_surface":
			_say_context("day1_pool_skimmer_hint",
				"Sweep the skimmer through every piece of trash!",
				_context_visit_id())
		"waterfall":
			_say_context("day1_pool_waterfall_hint",
				"Pull the trash down from the clogged rainbow waterfall!",
				_context_visit_id())
		"seahorse":
			_say_context("day1_pool_seahorse_hint",
				"Tap fast to pull the trash off the seahorse!",
				_context_visit_id())


func _phase_from_legacy_step(step: int) -> int:
	if step >= LEGACY_COMPLETE_STEP:
		return 3
	if step >= 2:
		# Legacy step 3 completed the removed rim tap but not the seahorse.
		return 2
	return clampi(step, 0, 1)


func _waterfall_fixture_center() -> Vector2:
	if _clean_waterfall != null and is_instance_valid(_clean_waterfall):
		return _clean_waterfall.position
	return WATERFALL_FALLBACK_CENTER


func _waterfall_fixture_size() -> Vector2:
	if _clean_waterfall != null and is_instance_valid(_clean_waterfall):
		var source_rect: Rect2 = _clean_waterfall.get_meta(
			"source_art_rect", Rect2()) as Rect2
		if source_rect.size.x > 1.0 and source_rect.size.y > 1.0:
			return source_rect.size * ART_TO_STAGE
	return WATERFALL_FALLBACK_SIZE


func _seahorse_fixture_center() -> Vector2:
	if _healthy_seahorse != null and is_instance_valid(_healthy_seahorse):
		return _healthy_seahorse.position
	return SEAHORSE_FALLBACK_CENTER


func _seahorse_fixture_size() -> Vector2:
	if _healthy_seahorse != null and is_instance_valid(_healthy_seahorse):
		var source_rect: Rect2 = _healthy_seahorse.get_meta(
			"source_art_rect", Rect2()) as Rect2
		if source_rect.size.x > 1.0 and source_rect.size.y > 1.0:
			return source_rect.size * ART_TO_STAGE
	return SEAHORSE_FALLBACK_SIZE


func _animated_fixture_water_hidden() -> bool:
	for record: Dictionary in _hidden_fixture_items:
		var item: CanvasItem = record.get("item") as CanvasItem
		if item != null and is_instance_valid(item) and item.visible:
			return false
	return true


func _update_dingy_lighting() -> void:
	if _lighting_target == null or not is_instance_valid(_lighting_target):
		return
	var completed_actions: int = 0
	if m != null:
		completed_actions = _count_bits(m.day_one_pool_skimmer_mask, 0x3F) \
			+ _count_bits(m.day_one_pool_waterfall_mask, 0x07) \
			+ clampi(m.day_one_pool_seahorse_tugs, 0, 8)
	var remaining_ratio: float = 1.0 - float(completed_actions) / 17.0
	_lighting_target.modulate = _lighting_target_rest_modulate * Color.WHITE.lerp(
		DINGY_ROOM_TINT, clampf(remaining_ratio, 0.0, 1.0))


func _count_bits(value: int, mask: int) -> int:
	var remaining: int = value & mask
	var count: int = 0
	while remaining != 0:
		count += remaining & 1
		remaining >>= 1
	return count


func _begin_finale() -> void:
	if _finale_started:
		return
	_finale_started = true
	_busy = true
	_say_context("day1_pool_complete", "The whole pool is shiny!", "day_one")
	_stop_activities()
	if _swimming_bunny != null and is_instance_valid(_swimming_bunny):
		_swimming_bunny.fade_out(0.32)
	if _lighting_target != null and is_instance_valid(_lighting_target):
		var light_tween: Tween = _lighting_target.create_tween()
		light_tween.tween_property(
			_lighting_target, "modulate", _lighting_target_rest_modulate, 0.85)
	finale_started.emit()
	var rooms: CastleRooms25D = m._castle_rooms_ref() if m != null else null
	if rooms != null:
		rooms._activate_room_item("seahorse_fountain")
	_spawn_rumi_rise()


func _spawn_rumi_rise() -> void:
	var pool_atlas: Texture2D = load(RUMI_POOL_ATLAS) as Texture2D
	var pose_atlas: Texture2D = load(RUMI_POSE_ATLAS) as Texture2D
	if pool_atlas == null or pose_atlas == null:
		push_error("Missing approved Rumi animation atlases: %s / %s" % [
			RUMI_POOL_ATLAS, RUMI_POSE_ATLAS])
		_finish_rumi_reveal()
		return
	_rumi = AnimatedSprite2D.new()
	_rumi.name = "RumiVioletReveal"
	_rumi.sprite_frames = _build_rumi_sprite_frames(pool_atlas, pose_atlas)
	_rumi.animation_finished.connect(_on_rumi_animation_finished)
	_rumi.position = Vector2(640.0, 610.0)
	_rumi.scale = Vector2.ONE * RUMI_SWIM_SCALE * 0.72
	_rumi.modulate.a = 0.0
	_rumi.z_index = 18
	_rumi.set_meta("approved_private_canon", true)
	_rumi.set_meta("source_working_name", "Violet Tide")
	add_child(_rumi)
	_rumi.play(&"swim")
	_spawn_reveal_ripple()
	var rise_tween: Tween = _rumi.create_tween().set_parallel(true)
	rise_tween.tween_property(
		_rumi, "position", Vector2(650.0, 350.0), 1.15
	).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	rise_tween.tween_property(
		_rumi, "scale", Vector2.ONE * RUMI_SWIM_SCALE, 1.0
	).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	rise_tween.tween_property(_rumi, "modulate:a", 1.0, 0.52)
	rise_tween.chain().tween_callback(_finish_rumi_reveal)


func _build_rumi_sprite_frames(
		pool_atlas: Texture2D, pose_atlas: Texture2D) -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.remove_animation(&"default")
	frames.add_animation(&"idle")
	frames.set_animation_speed(&"idle", 1.5)
	frames.set_animation_loop(&"idle", true)
	for column: int in range(2):
		frames.add_frame(&"idle", _rumi_atlas_frame(
			pose_atlas, column, 0, RUMI_POSE_CELL_SIZE))
	frames.add_animation(&"wave")
	frames.set_animation_speed(&"wave", 2.0)
	frames.set_animation_loop(&"wave", false)
	for column: int in range(2, 4):
		frames.add_frame(&"wave", _rumi_atlas_frame(
			pose_atlas, column, 0, RUMI_POSE_CELL_SIZE))
	frames.add_animation(&"swim")
	frames.set_animation_speed(&"swim", 5.0)
	frames.set_animation_loop(&"swim", true)
	for column: int in range(4):
		frames.add_frame(&"swim", _rumi_atlas_frame(
			pool_atlas, column, 1, RUMI_POOL_CELL_SIZE))
	return frames


func _rumi_atlas_frame(atlas: Texture2D, column: int, row: int,
		cell_size: Vector2) -> AtlasTexture:
	var frame := AtlasTexture.new()
	frame.atlas = atlas
	frame.region = Rect2(
		Vector2(float(column) * cell_size.x, float(row) * cell_size.y),
		cell_size)
	return frame


func _on_rumi_animation_finished() -> void:
	if _rumi != null and is_instance_valid(_rumi) \
			and _rumi.animation == &"wave":
		_rumi.play(&"idle")


func _spawn_reveal_ripple() -> void:
	var ripple := Label.new()
	ripple.name = "RumiRiseRipple"
	ripple.text = "○"
	ripple.position = Vector2(490.0, 470.0)
	ripple.size = Vector2(300.0, 110.0)
	ripple.pivot_offset = ripple.size * 0.5
	ripple.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ripple.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	ripple.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ripple.z_index = 17
	ripple.scale = Vector2(0.45, 0.20)
	StorybookUI.style_label(ripple, 92, Color(0.54, 0.96, 1.0), 5)
	add_child(ripple)
	var ripple_tween: Tween = ripple.create_tween().set_parallel(true)
	ripple_tween.tween_property(ripple, "scale", Vector2(2.1, 0.56), 1.0)
	ripple_tween.tween_property(ripple, "modulate:a", 0.0, 1.0)
	ripple_tween.chain().tween_callback(ripple.queue_free)


func _finish_rumi_reveal() -> void:
	_busy = false
	if _rumi != null and is_instance_valid(_rumi):
		_rumi.scale = Vector2.ONE * RUMI_UPRIGHT_START_SCALE
		_rumi.play(&"wave")
		var settle_tween: Tween = _rumi.create_tween()
		settle_tween.tween_property(
			_rumi, "scale", Vector2.ONE * RUMI_UPRIGHT_SCALE, 0.35
		).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		var idle_tween: Tween = _rumi.create_tween().set_loops()
		idle_tween.tween_property(
			_rumi, "position:y", _rumi.position.y - 7.0, 1.15
		).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		idle_tween.tween_property(
			_rumi, "position:y", _rumi.position.y + 7.0, 1.15
		).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	if m != null:
		_say_context("day1_pool_rumi_reply",
			"We saved the pool and the seahorse! Hi, Rumi!",
			"day_one")
	reveal_completed.emit()


func _announce_progress_from_save() -> void:
	_announced_skimmer_mask = m.day_one_pool_skimmer_mask if m != null else 0
	_announced_waterfall_mask = m.day_one_pool_waterfall_mask if m != null else 0
	_announced_seahorse_milestone = 4 if m != null \
		and m.day_one_pool_seahorse_tugs >= 8 else 3 if m != null \
		and m.day_one_pool_seahorse_tugs >= 7 else 2 if m != null \
		and m.day_one_pool_seahorse_tugs >= 4 else 1 if m != null \
		and m.day_one_pool_seahorse_tugs >= 1 else 0


func _say_context(cue_id: String, caption: String,
		session_id: String = "day_one", variant: int = 0) -> bool:
	if not _announcements_enabled or m == null:
		return false
	var spoken: bool = m.say_day_one_context(cue_id, caption, "pool",
		session_id, variant)
	if spoken and m.hud_msg != null:
		m.hud_msg.text = caption
		m.hud_msg.visible = caption != ""
		m.msg_timer = 5.0
	return spoken


func _context_visit_id() -> String:
	return "pool_visit_%d" % get_instance_id()
