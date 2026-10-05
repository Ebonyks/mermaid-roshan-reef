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
# The floating pieces in atlas order (floating_trash_atlas.png, 3 x 2 cells).
const SKIMMER_ITEM_NAMES: Array[String] = [
	"wrapper", "cup", "lid", "leaf", "ribbon", "sponge",
]
const SKIMMER_LEAF_INDEX := 3
# Object-neutral pickup lines chosen by how many pieces are out, as indexes into
# the two tables above. The leaf line plays only for the leaf, so no spoken line
# can name the wrong object (DL-SND-01, DL-MOT-04).
const SKIMMER_COUNT_LINE: Dictionary = {1: 3, 3: 2, 5: 4}
# Exact per-object takes may be added to the catalogue later; they win when READY.
const SKIMMER_ITEM_CUE_PREFIX := "day1_pool_skimmer_item_"
const IDLE_REPROMPT_SECONDS := 8.0
const MAX_IDLE_REPROMPTS := 2
# A quiet child hears the activity's other exact line, then its hint again.
const IDLE_REPROMPT_LINES: Dictionary = {
	"pool_surface": [
		["day1_pool_skimmer_clean", "Scoop every floaty bit with the net!"],
		["day1_pool_skimmer_hint", "Sweep the skimmer through every piece of trash!"],
	],
	"waterfall": [
		["day1_pool_waterfall_clean", "The rainbow waterfall is stuck! Pull the trash down!"],
		["day1_pool_waterfall_hint", "Pull the trash down from the clogged rainbow waterfall!"],
	],
	"seahorse": [
		["day1_pool_seahorse_clean", "Oh no, seahorse! I'll tug the trash out!"],
		["day1_pool_seahorse_hint", "Tap fast to pull the trash off the seahorse!"],
	],
}
# Rumi rises once, in the room-completion story clip `d1_pool_clean` (owner
# answer QP-1, 2026-10-05): the room's finale reveals the clean pool and leaves
# her rise to the clip, so no in-room Rumi is staged before it.
const RUMI_RISE_CLIP_ID := "d1_pool_clean"
# The clean-pool reveal is the earned reward beat: the light returns, the
# waterfall and fountain play their authored sequences and the completion line
# plays out before the room completes, because completion starts the story
# clip, which pauses the tree (freezing a line mid-word) and covers the room.
# Both bounds count from the start of the finale.
const REVEAL_BEAT_MIN_SECONDS := 2.4
const REVEAL_BEAT_MAX_SECONDS := 5.6

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
var _swimming_bunny: DayOneDustBunnySwimmer = null
var _clean_waterfall: Sprite2D = null
var _healthy_seahorse: Sprite2D = null
var _hidden_fixture_items: Array[Dictionary] = []
var _interaction_layer_visibility: Array[Dictionary] = []
var _announced_skimmer_mask: int = 0
var _announced_waterfall_mask: int = 0
var _announced_seahorse_milestone: int = 0
var _last_skimmer_line: String = ""
var _idle_seconds: float = 0.0
var _idle_reprompts: int = 0
var _reprompt_log: Array[String] = []
var _tint_ratio: float = 0.0
var _counter_tinted: Array[Sprite2D] = []
var _reveal_beat_active: bool = false
var _reveal_beat_seconds: float = 0.0
var _reveal_emitted: bool = false


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
	# The cleanup supplies the room's motion and guidance while it is mounted, so
	# the living-world layer's code-drawn ambient motifs pause above it (OD3).
	add_to_group(LivingWorldDirector.QUIET_GROUP)
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
	_clear_identity_counter_tint()
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
		"in_room_rumi_rise": false,
		"rumi_rise_owner": RUMI_RISE_CLIP_ID,
		"dust_bunny_count": 2,
		"land_bunny_owner": "day_one_castle_dressing",
		"swimming_bunny": _swimming_bunny.audit_snapshot()
			if _swimming_bunny != null and is_instance_valid(_swimming_bunny)
			else {},
		"canvas_only": true,
		"no_fail": true,
		"last_skimmer_line": _last_skimmer_line,
		"idle_reprompts": _reprompt_log.duplicate(),
		"idle_seconds": _idle_seconds,
		"tint_ratio": _tint_ratio,
		"identity_color_preserved": identity_color_preserved(),
		"reveal_beat_holding": _reveal_beat_active,
		"reveal_completed": _reveal_emitted,
		"one_room_basket": skimmer_activity != null and seahorse_activity != null
			and not bool(skimmer_activity.audit_snapshot().get("basket_visible", true))
			and seahorse_activity.room_basket() != null,
		"living_world_quiet": is_in_group(LivingWorldDirector.QUIET_GROUP),
	}


## The truthful line for one pickup: an exact per-object take when its recording
## is READY, the leaf line only for the leaf, then object-neutral lines by count.
## An empty result means the pickup is answered by sound and sight only.
static func skimmer_pickup_line(item_index: int, collected_count: int) -> Dictionary:
	if item_index >= 0 and item_index < SKIMMER_ITEM_NAMES.size():
		var item_cue: String = SKIMMER_ITEM_CUE_PREFIX + SKIMMER_ITEM_NAMES[item_index]
		var row: Dictionary = DayOneContextualVoiceCatalog.row(item_cue)
		if String(row.get("status", "")) == "READY":
			return {"cue_id": item_cue, "caption": String(row.get("caption", ""))}
	if item_index == SKIMMER_LEAF_INDEX:
		return {"cue_id": SKIMMER_CUE_IDS[0], "caption": SKIMMER_PICKUP_CAPTIONS[0]}
	if SKIMMER_COUNT_LINE.has(collected_count):
		var line_index: int = int(SKIMMER_COUNT_LINE[collected_count])
		return {"cue_id": SKIMMER_CUE_IDS[line_index],
			"caption": SKIMMER_PICKUP_CAPTIONS[line_index]}
	return {}


## True when every Roshan cutout inside the dingy room shows her own colours.
func identity_color_preserved() -> bool:
	var factor: Color = _tint_factor(_tint_ratio)
	for sprite: Sprite2D in _identity_sprites():
		if not _is_tinted(sprite):
			continue
		var shown := Color(factor.r * sprite.self_modulate.r,
			factor.g * sprite.self_modulate.g, factor.b * sprite.self_modulate.b)
		if absf(shown.r - 1.0) > 0.01 or absf(shown.g - 1.0) > 0.01 \
				or absf(shown.b - 1.0) > 0.01:
			return false
	return true


func _process(delta: float) -> void:
	if _reveal_beat_active:
		_advance_reveal_beat(maxf(delta, 0.0))
		return
	# A quiet child hears the current activity's exact line again (twice at
	# most); the guide hands keep pointing in the meantime. Never during a
	# completion, the finale, or before the controller is live.
	if m == null or _busy or _finale_started or _phase >= ACTIVITY_IDS.size():
		return
	_idle_seconds += maxf(delta, 0.0)
	if _idle_seconds < IDLE_REPROMPT_SECONDS or _idle_reprompts >= MAX_IDLE_REPROMPTS:
		return
	_idle_seconds = 0.0
	var lines: Array = IDLE_REPROMPT_LINES.get(ACTIVITY_IDS[_phase], []) as Array
	if lines.is_empty():
		return
	var line: Array = lines[_idle_reprompts % lines.size()] as Array
	_idle_reprompts += 1
	_reprompt_log.append(String(line[0]))
	# A fresh session id lets the exact take play again for this quiet moment.
	_say_context(String(line[0]), String(line[1]),
		"%s_idle_%d" % [_context_visit_id(), _reprompt_log.size()])


func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch or event is InputEventScreenDrag \
			or event is InputEventMouseButton:
		_idle_seconds = 0.0


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
	waterfall_activity.bind_room_actor(m.castle_room_player_sprite, m.castle_room_player_shadow as Sprite2D, m.skin_id)

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
	seahorse_activity.bind_room_actor(m.castle_room_player_sprite, m.castle_room_player_shadow as Sprite2D, m.skin_id)
	# The rescue's basket stays in the room through all three activities at the
	# skimmer's landing point; show one basket, never two identical ones (OD1).
	var room_basket: Sprite2D = seahorse_activity.room_basket()
	if room_basket != null \
			and room_basket.position.is_equal_approx(PoolSkimmerActivity.BASKET_POSITION):
		skimmer_activity.set_basket_visible(false)


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
	_idle_seconds = 0.0
	var newly_collected: int = mask & ~_announced_skimmer_mask
	var collected_count: int = _count_bits(mask, 0x3F)
	for index: int in range(SKIMMER_PICKUP_CAPTIONS.size()):
		if (newly_collected & (1 << index)) != 0:
			var line: Dictionary = skimmer_pickup_line(index, collected_count)
			_last_skimmer_line = String(line.get("cue_id", ""))
			if not line.is_empty():
				_say_context(String(line["cue_id"]), String(line["caption"]),
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
	_idle_seconds = 0.0
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
	_idle_seconds = 0.0
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
	_idle_seconds = 0.0
	_idle_reprompts = 0
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
	_set_tint_ratio(clampf(remaining_ratio, 0.0, 1.0))


func _tint_factor(ratio: float) -> Color:
	return Color.WHITE.lerp(DINGY_ROOM_TINT, clampf(ratio, 0.0, 1.0))


func _set_tint_ratio(ratio: float) -> void:
	# The room reads dingy, but Roshan keeps her approved colours: each of her
	# cutouts inside the tinted tree carries the exact inverse (DL-MED-05).
	_tint_ratio = clampf(ratio, 0.0, 1.0)
	if _lighting_target == null or not is_instance_valid(_lighting_target):
		return
	var factor: Color = _tint_factor(_tint_ratio)
	_lighting_target.modulate = _lighting_target_rest_modulate * factor
	var counter := Color(1.0 / maxf(factor.r, 0.01), 1.0 / maxf(factor.g, 0.01),
		1.0 / maxf(factor.b, 0.01), 1.0)
	for sprite: Sprite2D in _identity_sprites():
		if not _is_tinted(sprite):
			continue
		sprite.self_modulate = Color(counter.r, counter.g, counter.b, sprite.self_modulate.a)
		if not _counter_tinted.has(sprite):
			_counter_tinted.append(sprite)


func _identity_sprites() -> Array[Sprite2D]:
	var sprites: Array[Sprite2D] = []
	if m != null and m.castle_room_player_sprite != null \
			and is_instance_valid(m.castle_room_player_sprite):
		sprites.append(m.castle_room_player_sprite)
	for activity: Variant in [skimmer_activity, waterfall_activity, seahorse_activity]:
		if activity == null or not is_instance_valid(activity):
			continue
		var sprite: Sprite2D = (activity as Object).call("identity_sprite") as Sprite2D
		if sprite != null and is_instance_valid(sprite):
			sprites.append(sprite)
	return sprites


func _is_tinted(sprite: Sprite2D) -> bool:
	return _lighting_target != null and is_instance_valid(_lighting_target) \
		and (sprite == _lighting_target or _lighting_target.is_ancestor_of(sprite))


func _clear_identity_counter_tint() -> void:
	for sprite: Sprite2D in _counter_tinted:
		if sprite != null and is_instance_valid(sprite):
			sprite.self_modulate = Color(1.0, 1.0, 1.0, sprite.self_modulate.a)
	_counter_tinted.clear()


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
		# Fade the room and Roshan's counter-tint together, so she never flashes.
		var light_tween: Tween = create_tween()
		light_tween.tween_method(_set_tint_ratio, _tint_ratio, 0.0, 0.85)
	finale_started.emit()
	var rooms: CastleRooms25D = m._castle_rooms_ref() if m != null else null
	if rooms != null:
		rooms._activate_room_item("seahorse_fountain")
	# Hold the room completion until the clean-pool reveal and its line have
	# played (bounded), so the story clip, which owns Rumi's one rise, follows
	# the reward beat instead of cutting into it.
	_reveal_beat_seconds = 0.0
	_reveal_beat_active = true


func _advance_reveal_beat(delta: float) -> void:
	_reveal_beat_seconds += delta
	if _reveal_beat_seconds < REVEAL_BEAT_MIN_SECONDS:
		return
	if _reveal_beat_seconds < REVEAL_BEAT_MAX_SECONDS and _voice_lane_busy():
		return
	_reveal_beat_active = false
	if _reveal_emitted:
		return
	_reveal_emitted = true
	reveal_completed.emit()


func _voice_lane_busy() -> bool:
	if m == null:
		return false
	for player: AudioStreamPlayer in m.voice_pool:
		if player != null and is_instance_valid(player) and player.playing:
			return true
	return false


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
