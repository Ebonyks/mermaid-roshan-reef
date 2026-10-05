extends SceneTree
## Focused exact-Godot contract probe for the three Day One pool activities.

const POOL_CLEANUP := preload("res://scripts/games/day_one_pool_cleanup.gd")
const POOL_SKIMMER := preload("res://scripts/games/pool_skimmer_activity.gd")
const POOL_WATERFALL := preload("res://scripts/games/pool_waterfall_activity.gd")
const POOL_SEAHORSE := preload("res://scripts/games/pool_seahorse_rescue_activity.gd")
const RUNTIME_ASSETS: Array[String] = [
	"res://assets/castle/day_one_pool/activities/pool_skimmer.png",
	"res://assets/castle/day_one_pool/activities/floating_trash_atlas.png",
	"res://assets/castle/day_one_pool/activities/cleanup_basket.png",
	"res://assets/castle/day_one_pool/activities/waterfall_clogged_original_match.png",
	"res://assets/castle/day_one_pool/activities/waterfall_scrubber.png",
	"res://assets/castle/day_one_pool/activities/seahorse_sick_clear_mouth.png",
	"res://assets/castle/day_one_pool/activities/seahorse_mouth_trash.png",
	"res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png",
	"res://assets/characters/rumi/rumi_eight_pose_runtime.png",
	"res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png",
]

var checks_failed: int = 0
var restored_completion_events: Dictionary = {}


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var main := ReefMain.new()
	var host := Control.new()
	host.name = "DayOnePoolProbeHost"
	host.size = StorybookUI.CANVAS_SIZE
	get_root().add_child(host)
	await _probe_seahorse_mouth_contact(host)
	_probe_seahorse_input_contract(host)
	_probe_contact_action(host)
	var tap_player := AudioStreamPlayer.new()
	host.add_child(tap_player)
	main._tap_player = tap_player
	var clean_waterfall := Sprite2D.new()
	clean_waterfall.name = "CleanWaterfallProbeFixture"
	clean_waterfall.position = Vector2(461.875, 216.25)
	clean_waterfall.set_meta("source_art_rect", Rect2(309.0, 90.0, 121.0, 166.0))
	host.add_child(clean_waterfall)
	var flowing_water := Sprite2D.new()
	flowing_water.name = "FlowingWaterProbeLayer"
	host.add_child(flowing_water)
	var clean_seahorse := Sprite2D.new()
	clean_seahorse.name = "CleanSeahorseProbeFixture"
	clean_seahorse.position = Vector2(921.875, 245.625)
	clean_seahorse.set_meta("source_art_rect", Rect2(821.0, 149.0, 167.0, 193.0))
	host.add_child(clean_seahorse)
	main.castle_room_item_sprites["waterfall"] = {
		"sprite": clean_waterfall,
		"fixture_rig": {"water": [{"node": flowing_water}]},
	}
	main.castle_room_item_sprites["seahorse_fountain"] = {
		"sprite": clean_seahorse,
		"fixture_rig": {"water": []},
	}
	var cleanup: DayOnePoolCleanup = POOL_CLEANUP.new() as DayOnePoolCleanup
	host.add_child(cleanup)
	cleanup.setup(main, false)
	await process_frame

	var initial: Dictionary = cleanup.audit_snapshot()
	_probe_trash_atlas_sampling(cleanup.skimmer_activity)
	_check("three bespoke ordered activities",
		int(initial.get("activity_count", 0)) == 3
		and initial.get("activity_ids", []) == ["pool_surface", "waterfall", "seahorse"]
		and not bool(initial.get("standalone_pool_rim_gate", true)))
	_check("dirty arrival starts skimmer only",
		String(initial.get("current_activity", "")) == "pool_surface"
		and bool((initial.get("skimmer", {}) as Dictionary).get("running", false))
		and not bool((initial.get("waterfall", {}) as Dictionary).get("active", true))
		and not bool((initial.get("seahorse", {}) as Dictionary).get("active", true)))
	_check("dirty arrival hides pristine rainbow and flow",
		not clean_waterfall.visible and not flowing_water.visible)
	_check("canvas no-fail contract",
		bool(initial.get("canvas_only", false))
		and bool(initial.get("no_fail", false))
		and bool(initial.get("dingy_lighting", false)))
	_check("dingy room keeps Roshan's approved colours",
		float(initial.get("tint_ratio", 0.0)) > 0.9
		and bool(initial.get("identity_color_preserved", false))
		and cleanup.skimmer_activity.identity_sprite().self_modulate.r > 1.2)
	_check("pool guides and effects use approved art, not code shapes or glyphs",
		bool((initial.get("skimmer", {}) as Dictionary).get("demo_pointer_authored", false))
		and bool((initial.get("waterfall", {}) as Dictionary).get("guide_hand_authored", false))
		and bool((initial.get("seahorse", {}) as Dictionary).get("guide_hand_authored", false))
		and bool((initial.get("seahorse", {}) as Dictionary).get("authored_progress_beads", false))
		and not bool((initial.get("skimmer", {}) as Dictionary).get("code_drawn_effects", true))
		and not bool((initial.get("seahorse", {}) as Dictionary).get("code_drawn_effects", true))
		and not bool((initial.get("waterfall", {}) as Dictionary).get("code_drawn_guides", true)))
	# MA-VIS-009: one basket, no code-drawn ambience over the cleanup, and the
	# swimmer grounded by approved ripple art rather than code arcs.
	var room_basket: Sprite2D = cleanup.seahorse_activity.room_basket()
	_check("the room shows one cleanup basket, at the skimmer's landing point",
		bool(initial.get("one_room_basket", false))
		and room_basket != null and room_basket.visible
		and room_basket.position.is_equal_approx(PoolSkimmerActivity.BASKET_POSITION)
		and not bool((initial.get("skimmer", {}) as Dictionary).get("basket_visible", true)))
	_check("the cleanup quiets the code-drawn living-world layer while mounted",
		bool(initial.get("living_world_quiet", false))
		and cleanup.is_in_group(LivingWorldDirector.QUIET_GROUP))
	var initial_swimmer: Dictionary = initial.get("swimming_bunny", {}) as Dictionary
	_check("the swimmer's water contact is approved ripple art, not code arcs",
		bool(initial_swimmer.get("ripple_authored", false))
		and not bool(initial_swimmer.get("code_drawn_ripple", true))
		and not FileAccess.get_file_as_string(
			"res://scripts/games/day_one_dust_bunny_swimmer.gd").contains("func _draw("))
	_probe_contextual_voice_wiring()
	_probe_truthful_skimmer_lines()
	_probe_roshan_contact(host)
	var swimmer: Dictionary = initial.get("swimming_bunny", {}) as Dictionary
	_check("exact pool bunny cast keeps one land and one swimmer",
		int(initial.get("dust_bunny_count", 0)) == 2
		and String(initial.get("land_bunny_owner", ""))
			== "day_one_castle_dressing"
		and bool(swimmer.get("present", false))
		and bool(swimmer.get("true_2d", false)))
	_check("swimmer remains inside central water with a simple 2D loop",
		bool(swimmer.get("inside_bounds", false))
		and bool(swimmer.get("fully_contained", false))
		and swimmer.get("bounds", Rect2()) == Rect2(300.0, 285.0, 680.0, 235.0)
		and String(swimmer.get("animation", "")) == "bounded_bob_paddle"
		and String(swimmer.get("asset", "")).ends_with(
			"dust_bunny_swimming.png")
		and float(swimmer.get("display_width", 0.0)) <= 124.0
		and float(swimmer.get("display_width", 0.0)) >= 112.0)
	for asset_path: String in RUNTIME_ASSETS:
		var texture: Texture2D = load(asset_path) as Texture2D
		_check("runtime asset %s" % asset_path.get_file(),
			texture != null
			and maxf(texture.get_size().x, texture.get_size().y) <= 1024.0)

	# A complete mask/tug count restored from disk must still advance the owner
	# once, but repeated starts/re-entry may never duplicate the completion.
	var restored_skimmer: PoolSkimmerActivity = POOL_SKIMMER.new()
	var restored_waterfall: PoolWaterfallActivity = POOL_WATERFALL.new()
	var restored_seahorse: PoolSeahorseRescueActivity = POOL_SEAHORSE.new()
	host.add_child(restored_skimmer)
	host.add_child(restored_waterfall)
	host.add_child(restored_seahorse)
	restored_completion_events = {"skimmer": 0, "waterfall": 0, "seahorse": 0}
	restored_skimmer.completed.connect(_record_restored_completion.bind("skimmer"))
	restored_waterfall.completed.connect(_record_restored_completion.bind("waterfall"))
	restored_seahorse.completed.connect(_record_restored_completion.bind("seahorse"))
	restored_skimmer.setup(0x3F)
	restored_waterfall.setup(Vector2(460.0, 216.0), Vector2(150.0, 207.0), 0x07)
	restored_seahorse.setup(Vector2(922.0, 246.0), Vector2(209.0, 241.0), 8)
	restored_skimmer.start()
	restored_waterfall.start()
	restored_seahorse.start()
	restored_skimmer.start()
	restored_waterfall.start()
	restored_seahorse.start()
	await process_frame
	_check("restored complete pool activities emit once",
		restored_completion_events == {"skimmer": 1, "waterfall": 1, "seahorse": 1})
	restored_skimmer.stop()
	restored_waterfall.stop()
	restored_seahorse.stop()
	restored_skimmer.start()
	restored_waterfall.start()
	restored_seahorse.start()
	await process_frame
	_check("re-entered complete pool activities stay one-shot",
		restored_completion_events == {"skimmer": 1, "waterfall": 1, "seahorse": 1})

	await create_timer(0.12).timeout
	var passive: Dictionary = cleanup.audit_snapshot()
	_check("passive demo never advances",
		int(main.day_one_pool_skimmer_mask) == 0
		and int((passive.get("skimmer", {}) as Dictionary).get("progress_mask", -1)) == 0)
	# A quiet child: thirty seconds of zero input earn nothing, and the exact
	# lines come back twice at most (the other line first, then the hint).
	for _second: int in range(30):
		cleanup._process(1.0)
		cleanup.skimmer_activity._process(1.0)
	var quiet: Dictionary = cleanup.audit_snapshot()
	_check("thirty quiet seconds re-prompt twice and award nothing",
		quiet.get("idle_reprompts", []) == ["day1_pool_skimmer_clean", "day1_pool_skimmer_hint"]
		and int(main.day_one_pool_skimmer_mask) == 0
		and bool((quiet.get("skimmer", {}) as Dictionary).get("demo_pointer_visible", false)))

	# Six real touches: each one travels, scoops and lands in the basket.
	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	for piece: int in range(PoolSkimmerActivity.TRASH_COUNT):
		var press := InputEventScreenTouch.new()
		press.index = 0
		press.pressed = true
		press.position = skimmer._trash_contact_position(piece)
		skimmer._gui_input(press)
		press.pressed = false
		skimmer._gui_input(press)
		for _tick: int in range(240):
			skimmer._process(1.0 / 60.0)
			if (int(main.day_one_pool_skimmer_mask) & (1 << piece)) != 0:
				break
	_check("skimmer activity accepts six real touch collections",
		int(main.day_one_pool_skimmer_mask) == 0x3F)
	_check("the last pickup line never names the wrong object",
		String(cleanup.audit_snapshot().get("last_skimmer_line", "x")) == "")
	await create_timer(0.72).timeout
	var after_pool: Dictionary = cleanup.audit_snapshot()
	_check("skimmer completion persists and unlocks waterfall",
		main.day_one_pool_skimmer_mask == 0x3F
		and main.day_one_pool_cleanup_step == 1
		and String(after_pool.get("current_activity", "")) == "waterfall")
	_check("dirty waterfall is registered to live V4 fixture",
		(after_pool.get("waterfall_center", Vector2.ZERO) as Vector2).is_equal_approx(
			clean_waterfall.position)
		and (after_pool.get("waterfall_size", Vector2.ZERO) as Vector2).is_equal_approx(
			Vector2(151.25, 207.5)))
	_check("clean stripe feedback sits above dirty waterfall lanes",
		bool((after_pool.get("waterfall", {}) as Dictionary).get(
			"wash_feedback_above_grime", false)))
	_check("static clean card under scrub lanes but flow remains stopped",
		clean_waterfall.visible and not flowing_water.visible
		and bool(after_pool.get("animated_water_hidden", false)))

	# A quiet second brings the approved guide hand down the next lane.
	var waterfall_activity: PoolWaterfallActivity = cleanup.waterfall_activity
	for _quarter: int in range(4):
		waterfall_activity._process(0.25)
	_check("quiet waterfall shows the authored stroke guide on the next lane",
		bool(waterfall_activity.audit_snapshot().get("guide_hand_visible", false)))
	# Three real downward strokes, one per lane, through the real input path.
	var lane_width: float = waterfall_activity.fixture_size.x / 3.0
	for lane: int in range(3):
		var x: float = waterfall_activity._fixture_rect.position.x + lane_width * (float(lane) + 0.5)
		var top := Vector2(x, waterfall_activity._fixture_rect.position.y + 8.0)
		var bottom := Vector2(x, waterfall_activity._fixture_rect.end.y - 4.0)
		var stroke := InputEventScreenTouch.new()
		stroke.index = 0
		stroke.pressed = true
		stroke.position = top
		waterfall_activity._gui_input(stroke)
		if lane == 0:
			_check("a touch hides the guide hand",
				not bool(waterfall_activity.audit_snapshot().get("guide_hand_visible", true)))
		var drag := InputEventScreenDrag.new()
		drag.index = 0
		drag.position = top.lerp(bottom, 0.5)
		waterfall_activity._gui_input(drag)
		if lane == 0:
			var partial: Sprite2D = waterfall_activity._slice_nodes[0]
			_check("a half stroke wipes the authored dirt away from the top",
				partial.region_rect.position.y > 1.0 and partial.offset.y > 0.5
				and int(main.day_one_pool_waterfall_mask) == 0)
		drag.position = bottom
		waterfall_activity._gui_input(drag)
		stroke.pressed = false
		stroke.position = bottom
		waterfall_activity._gui_input(stroke)
	_check("waterfall activity clears three lanes with real strokes",
		int(main.day_one_pool_waterfall_mask) == 0x07)
	await create_timer(0.56).timeout
	var after_waterfall: Dictionary = cleanup.audit_snapshot()
	_check("waterfall completion persists and unlocks seahorse",
		main.day_one_pool_waterfall_mask == 0x07
		and main.day_one_pool_cleanup_step == 2
		and String(after_waterfall.get("current_activity", "")) == "seahorse")
	_check("sick seahorse uses exact live V4 fixture bounds",
		((after_waterfall.get("seahorse", {}) as Dictionary).get(
			"fixture_size", Vector2.ZERO) as Vector2).is_equal_approx(
				Vector2(208.75, 241.25)))
	_check("rainbow animation still waits for rescue finale",
		clean_waterfall.visible and not flowing_water.visible)

	var seahorse_activity: PoolSeahorseRescueActivity = cleanup.seahorse_activity
	var tug := InputEventScreenTouch.new()
	tug.index = 0
	tug.position = seahorse_activity.fixture_center
	tug.pressed = true
	seahorse_activity._gui_input(tug)
	tug.pressed = false
	seahorse_activity._gui_input(tug)
	_check("one real seahorse tap advances monotonically",
		seahorse_activity._taps == 1)
	await process_frame
	_check("partial tug saves without premature finale",
		main.day_one_pool_seahorse_tugs == 1
		and main.day_one_pool_cleanup_step == 2
		and not bool(cleanup.audit_snapshot().get("finale_started", false)))
	# Three deliberate pulls (two tugs each) and one tap finish the rescue: a
	# purposeful pull is twice a tap, so pulling is the fastest way through.
	for _pull: int in range(3):
		tug.pressed = true
		tug.position = seahorse_activity.fixture_center
		seahorse_activity._gui_input(tug)
		var pull := InputEventScreenDrag.new()
		pull.index = 0
		pull.position = seahorse_activity.fixture_center + Vector2(-70.0, 30.0)
		seahorse_activity._gui_input(pull)
		pull.position += Vector2(-60.0, 10.0)
		seahorse_activity._gui_input(pull)
		tug.pressed = false
		tug.position = pull.position
		seahorse_activity._gui_input(tug)
	_check("each real pull is worth two tugs, never more",
		seahorse_activity._taps == 7)
	tug.pressed = true
	tug.position = seahorse_activity.fixture_center
	seahorse_activity._gui_input(tug)
	tug.pressed = false
	seahorse_activity._gui_input(tug)
	_check("remaining real tap starts causal extraction",
		seahorse_activity._taps == 8 and seahorse_activity._completion_started)
	await create_timer(0.82).timeout
	var final_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("seahorse extraction completes legacy step four",
		main.day_one_pool_seahorse_tugs == 8
		and main.day_one_pool_cleanup_step == 4
		and String(final_snapshot.get("current_activity", "")) == "complete")
	_check("finale creates approved Rumi reveal",
		bool(final_snapshot.get("finale_started", false))
		and bool(final_snapshot.get("rumi_present", false))
		and bool(final_snapshot.get("rumi_approved_identity", false))
		and bool(final_snapshot.get("rumi_authored_animation", false))
		and String(final_snapshot.get("rumi_animation", "")) == "swim")
	_check("Rumi rises through the approved water ripple, not the cleaning ring",
		String(final_snapshot.get("rise_ripple_asset", ""))
			== DayOnePoolCleanup.RISE_RIPPLE_ATLAS_PATH)
	cleanup.m = null
	await create_timer(0.52).timeout
	await create_timer(0.74).timeout
	var wave_snapshot: Dictionary = cleanup.audit_snapshot()
	var finale_swimmer: Dictionary = wave_snapshot.get(
		"swimming_bunny", {}) as Dictionary
	_check("ambient swimmer yields the finale focal point",
		not bool(finale_swimmer.get("visible", true))
		and float(finale_swimmer.get("opacity", 1.0)) <= 0.01)
	_check("Rumi performs authored wave after rising",
		String(wave_snapshot.get("rumi_animation", "")) == "wave")
	var reveal_signals: Array[int] = [0]
	cleanup.reveal_completed.connect(func() -> void: reveal_signals[0] += 1)
	_check("the room completion waits for Rumi's wave and reply",
		bool(wave_snapshot.get("reveal_beat_holding", false))
		and not bool(wave_snapshot.get("reveal_completed", true)))
	await create_timer(1.1).timeout
	var idle_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("Rumi settles into authored idle",
		String(idle_snapshot.get("rumi_animation", "")) == "idle")
	_check("the reward beat ends in exactly one room completion",
		bool(idle_snapshot.get("reveal_completed", false))
		and not bool(idle_snapshot.get("reveal_beat_holding", true))
		and reveal_signals[0] == 1)
	cleanup.teardown()
	await process_frame
	_check("teardown frees cleanup", not is_instance_valid(cleanup))
	_check("teardown restores clean fixtures", clean_waterfall.visible
		and clean_seahorse.visible and flowing_water.visible)
	host.queue_free()
	main.free()
	await process_frame
	print("DAY_ONE_POOL|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _probe_roshan_contact(host: Control) -> void:
	var actor := Sprite2D.new()
	actor.position = Vector2(700.0, 490.0)
	host.add_child(actor)
	var shadow := Sprite2D.new()
	host.add_child(shadow)
	var activity: PoolSkimmerActivity = POOL_SKIMMER.new()
	host.add_child(activity)
	activity.setup()
	activity.bind_room_actor(actor, shadow)
	activity.start()
	activity.set_process(false)
	var before: Dictionary = activity.audit_snapshot()
	_check("one visible Roshan owns the held skimmer",
		bool(before.get("roshan_present", false)) and not actor.visible
		and not shadow.visible and float(before.get("hand_grip_error", INF)) < 0.01)
	var touch := InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = true
	touch.position = PoolSkimmerActivity.TRASH_POSITIONS[0]
	activity._gui_input(touch)
	_check("far touch cannot collect remotely", int(activity.audit_snapshot()["mask"]) == 0)
	activity._process(0.1)
	var moving: Dictionary = activity.audit_snapshot()
	var travelled: float = (moving["roshan_position"] as Vector2).distance_to(
		before["roshan_position"] as Vector2)
	_check("Roshan travels at bounded speed before collection",
		travelled > 1.0 and travelled <= PoolSkimmerActivity.SWIM_SPEED * 0.1 + 0.01
		and int(moving["mask"]) == 0)
	var second := InputEventScreenTouch.new()
	second.index = 1
	second.pressed = true
	second.position = PoolSkimmerActivity.TRASH_POSITIONS[5]
	activity._gui_input(second)
	_check("second finger cannot steal cleaning target", int(activity.audit_snapshot()["target_index"]) == 0)
	touch.pressed = false
	touch.canceled = true
	activity._gui_input(touch)
	for _tick: int in range(180):
		activity._process(1.0 / 60.0)
	_check("canceled touch cannot finish later", int(activity.audit_snapshot()["mask"]) == 0)
	touch.canceled = false
	touch.pressed = true
	activity._gui_input(touch)
	touch.pressed = false
	activity._gui_input(touch)
	var saw_scoop: bool = false
	for _tick: int in range(240):
		activity._process(1.0 / 60.0)
		var state: Dictionary = activity.audit_snapshot()
		if float(state["scoop_time"]) > 0.0:
			saw_scoop = true
			_check("scoop keeps hand attached before awarding progress",
				float(state["hand_grip_error"]) < 0.01 and int(state["mask"]) == 0
				and not bool(state["demo_pointer_visible"]))
		if int(state["mask"]) != 0:
			break
	_check("quick tap travels then visibly scoops exactly one item",
		saw_scoop and int(activity.audit_snapshot()["mask"]) == 1)
	var last_position: Vector2 = activity.audit_snapshot()["roshan_position"] as Vector2
	activity.stop()
	_check("stop restores room actor at the action location",
		actor.visible and shadow.visible and actor.position.distance_to(last_position) < 0.01)
	activity.start()
	activity.cancel_touch()
	for _tick: int in range(180):
		activity._process(1.0 / 60.0)
	_check("re-entry and focus cancellation retain only completed work",
		int(activity.audit_snapshot()["mask"]) == 1)
	touch.pressed = true
	touch.position = PoolSkimmerActivity.TRASH_POSITIONS[1]
	activity._gui_input(touch)
	var drag := InputEventScreenDrag.new()
	drag.index = 0
	drag.position = PoolSkimmerActivity.TRASH_POSITIONS[5]
	activity._gui_input(drag)
	var drag_start: Vector2 = activity.audit_snapshot()["roshan_position"] as Vector2
	activity._process(10.0)
	var drag_state: Dictionary = activity.audit_snapshot()
	_check("drag retarget cancels old work and slow frames never teleport",
		int(drag_state["target_index"]) == 5 and int(drag_state["mask"]) == 1
		and (drag_state["roshan_position"] as Vector2).distance_to(drag_start)
			<= PoolSkimmerActivity.SWIM_SPEED / 15.0 + 0.01)
	activity.cancel_touch()
	activity.stop()
	for skin: String in ["fairy", "huluu"]:
		actor.texture = load("res://assets/characters/skins/fairy_mermaid.png"
			if skin == "fairy" else "res://assets/characters/friends/huluu.png") as Texture2D
		activity.bind_room_actor(actor, shadow, skin)
		activity.start()
		var cutout: Sprite2D = activity.get_node(
			"RoshanHoldingSkimmer/RoshanApprovedCutout") as Sprite2D
		_check("cleaner retains selected %s cutout and hand socket" % skin,
			cutout.texture == actor.texture
			and float(activity.audit_snapshot()["hand_grip_error"]) < 0.01)
		activity.stop()
	activity.setup(PoolSkimmerActivity.ALL_MASK)
	activity.start()
	_check("restored complete mask never creates a second Roshan",
		actor.visible and not bool(activity.audit_snapshot()["roshan_present"]))
	activity.stop()
	activity.free()
	actor.free()
	shadow.free()


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_POOL|", label, ": ", "OK" if ok else "FAIL")


func _probe_contextual_voice_wiring() -> void:
	var source := FileAccess.get_file_as_string(
		"res://scripts/games/day_one_pool_cleanup.gd")
	_check("pool has exact pickup and lane cue wiring",
		source.contains("SKIMMER_PICKUP_CAPTIONS")
		and source.contains("WATERFALL_LANE_CAPTIONS")
		and source.contains("day1_pool_skimmer_01")
		and source.contains("day1_pool_skimmer_06")
		and source.contains("day1_pool_skimmer_complete")
		and source.contains("day1_pool_waterfall_lane_left")
		and source.contains("day1_pool_waterfall_lane_center")
		and source.contains("day1_pool_waterfall_lane_right")
		and source.contains("day1_pool_waterfall_complete"))
	_check("pool has monotonic seahorse milestones and finale cues",
		source.contains("day1_pool_seahorse_early")
		and source.contains("day1_pool_seahorse_middle")
		and source.contains("day1_pool_seahorse_final")
		and source.contains("day1_pool_seahorse_free")
		and source.contains("day1_pool_complete")
		and source.contains("day1_pool_rumi_reply"))
	_check("pool activity has no generic voice fallback",
		not source.contains("m.show_msg")
		and not source.contains("m._say"))


func _record_restored_completion(activity_id: String) -> void:
	restored_completion_events[activity_id] = int(
		restored_completion_events.get(activity_id, 0)) + 1


func _probe_seahorse_mouth_contact(host: Control) -> void:
	var activity: PoolSeahorseRescueActivity = POOL_SEAHORSE.new()
	host.add_child(activity)
	# Different aspect ratios expose mapping against the fixture rectangle
	# instead of the fitted artwork. These pixels are measured in the source PNGs.
	for bounds: Vector2 in [Vector2(208.75, 241.25), Vector2(400, 160), Vector2(120, 360)]:
		activity.setup(Vector2(921.875, 245.625), bounds, 3)
		activity.start()
		var seahorse: Sprite2D = activity.get_node("SickSeahorseBase") as Sprite2D
		var prop: Sprite2D = activity.get_node("MouthTrashPullProp") as Sprite2D
		var mouth_pixel := Vector2(394, 322) - seahorse.texture.get_size() * 0.5
		var stem_pixel := Vector2(1011.712, 393.984) - prop.texture.get_size() * 0.5
		var maximum_gap: float = prop.to_global(stem_pixel).distance_to(
			seahorse.to_global(mouth_pixel))
		# Slow, then overlapping rapid tugs; sample every rendered frame.
		activity.probe_tap()
		for frame: int in range(30):
			if frame == 15 or frame == 16:
				activity.probe_tap()
			await process_frame
			maximum_gap = maxf(maximum_gap, prop.to_global(stem_pixel).distance_to(
				seahorse.to_global(mouth_pixel)))
		activity.stop()
		await create_timer(0.40).timeout
		maximum_gap = maxf(maximum_gap, prop.to_global(stem_pixel).distance_to(
			seahorse.to_global(mouth_pixel)))
		_check("seahorse stem stays in mouth through restored/slow/rapid/stopped tugs %s" % bounds,
			maximum_gap < 0.5 and is_zero_approx(prop.rotation))
		_check("socket animation preserves partial progress without completing",
			int(activity.audit_snapshot().get("taps", 0)) == 6
			and not bool(activity.audit_snapshot().get("completed", true)))
	activity.free()


func _probe_trash_atlas_sampling(activity: PoolSkimmerActivity) -> void:
	var sampled: int = 0
	for index: int in range(2):
		if activity == null or activity._trash_sprites.size() <= index:
			continue
		var piece: Sprite2D = activity._trash_sprites[index]
		var frame: AtlasTexture = piece.texture as AtlasTexture
		if frame == null or frame.atlas == null:
			continue
		sampled += 1
		var expected_subject: Rect2 = Rect2(19, 31, 327, 282) if index == 0 \
			else Rect2(381, 56, 286, 243)
		_check("trash %d sampled region contains the complete measured subject" % index,
			frame.region.encloses(expected_subject)
			and frame.region.size == Vector2(341, 341) and frame.filter_clip)
		var source_image: Image = frame.atlas.get_image()
		if source_image.is_compressed():
			source_image.decompress()
		var sampled_image: Image = source_image.get_region(Rect2i(frame.region))
		var edge_alpha: float = 0.0
		for coordinate: int in range(341):
			for point: Vector2i in [Vector2i(0, coordinate), Vector2i(340, coordinate),
					Vector2i(coordinate, 0), Vector2i(coordinate, 340)]:
				edge_alpha = maxf(edge_alpha, sampled_image.get_pixelv(point).a)
		_check("trash %d live texture has transparent sampled edges without neighbor pixels" % index,
			edge_alpha <= 1.0 / 255.0)
	_check("both wrapper and can live textures were checked", sampled == 2)


func _probe_seahorse_input_contract(host: Control) -> void:
	var activity: PoolSeahorseRescueActivity = POOL_SEAHORSE.new()
	host.add_child(activity)
	activity.size = StorybookUI.CANVAS_SIZE
	for bounds: Vector2 in [Vector2(208.75, 241.25), Vector2(400, 160), Vector2(120, 360)]:
		activity.setup(Vector2(921.875, 245.625), bounds)
		activity.start()
		var touch := InputEventScreenTouch.new()
		touch.index = 0
		touch.position = Vector2(20, 20)
		for _tap: int in range(8):
			touch.pressed = true
			activity._gui_input(touch)
			touch.pressed = false
			activity._gui_input(touch)
		_check("off-target seahorse taps never earn rescue %s" % bounds,
			activity._taps == 0 and not activity._completion_started)
		touch.position = activity.fixture_center
		touch.pressed = true
		activity._gui_input(touch)
		activity._gui_input(touch)
		var second := InputEventScreenTouch.new()
		second.index = 1
		second.position = activity.fixture_center
		second.pressed = true
		activity._gui_input(second)
		second.pressed = false
		activity._gui_input(second)
		_check("held/secondary seahorse presses preserve the first owner %s" % bounds,
			activity._taps == 1 and activity._touch_active and activity._touch_id == 0)
		touch.canceled = true
		activity._gui_input(touch)
		_check("canceled press earns nothing and releases its owner %s" % bounds,
			activity._taps == 1 and not activity._touch_active)
		touch.canceled = false
		for _tap: int in range(7):
			touch.pressed = true
			activity._gui_input(touch)
			touch.pressed = false
			activity._gui_input(touch)
		_check("eight deliberate seahorse taps start one rescue %s" % bounds,
			activity._taps == 8 and activity._completion_started)
		activity.stop()
	activity.setup(Vector2(921.875, 245.625), Vector2(208.75, 241.25))
	activity.start()
	var press := InputEventScreenTouch.new()
	press.index = 0
	press.pressed = true
	press.position = activity.fixture_center
	activity._gui_input(press)
	var short_drag := InputEventScreenDrag.new()
	short_drag.index = 0
	short_drag.position = activity.fixture_center + Vector2(-20.0, 0.0)
	activity._gui_input(short_drag)
	_check("a small wobble is still one tug", activity._taps == 1)
	var other_finger := InputEventScreenDrag.new()
	other_finger.index = 1
	other_finger.position = activity.fixture_center + Vector2(-200.0, 0.0)
	activity._gui_input(other_finger)
	_check("another finger's drag cannot pull for the owner", activity._taps == 1)
	short_drag.position = activity.fixture_center + Vector2(-80.0, 20.0)
	activity._gui_input(short_drag)
	short_drag.position = activity.fixture_center + Vector2(-160.0, 40.0)
	activity._gui_input(short_drag)
	_check("one deliberate pull adds exactly one more tug per press", activity._taps == 2)
	press.pressed = false
	activity._gui_input(press)
	activity.stop()
	activity.free()


func _probe_truthful_skimmer_lines() -> void:
	# Every spoken pickup line must be true of the piece just scooped: only the
	# leaf may hear a leaf line, whatever order the child chooses.
	var leaf_lines_only_for_leaf := true
	var voiced: int = 0
	for item: int in range(PoolSkimmerActivity.TRASH_COUNT):
		for count: int in range(1, PoolSkimmerActivity.TRASH_COUNT + 1):
			var line: Dictionary = DayOnePoolCleanup.skimmer_pickup_line(item, count)
			if line.is_empty():
				continue
			voiced += 1
			var caption: String = String(line.get("caption", "")).to_lower()
			if caption.contains("leaf") and item != DayOnePoolCleanup.SKIMMER_LEAF_INDEX:
				leaf_lines_only_for_leaf = false
			var row: Dictionary = DayOneContextualVoiceCatalog.row(String(line.get("cue_id", "")))
			if String(row.get("status", "")) != "READY" \
					or String(row.get("caption", "")) != String(line.get("caption", "")):
				leaf_lines_only_for_leaf = false
	_check("pickup lines are exact recordings and never name the wrong object",
		leaf_lines_only_for_leaf and voiced > 0)
	_check("scooping the sponge first sounds object-neutral",
		String(DayOnePoolCleanup.skimmer_pickup_line(5, 1).get("cue_id", "")) == "day1_pool_skimmer_04")
	_check("scooping the leaf names the leaf",
		String(DayOnePoolCleanup.skimmer_pickup_line(3, 4).get("cue_id", "")) == "day1_pool_skimmer_01")


func _probe_contact_action(host: Control) -> void:
	var actor := Sprite2D.new()
	host.add_child(actor)
	actor.position = Vector2(80.0, 600.0)
	var action := DayOneContactAction2D.new()
	host.add_child(action)
	action.bind(actor, null, "classic")
	var calls: Array[int] = [0]
	_check("contact action accepts one deliberate job", action.request(Vector2(850.0, 280.0), func() -> void: calls[0] += 1))
	_check("a second job cannot steal the active approach", not action.request(Vector2.ZERO))
	action._process(0.2)
	_check("travel and waiting never award before hand contact", calls[0] == 0 and not action.in_contact() and not actor.visible)
	for index: int in range(80):
		action._process(0.05)
	_check("arrival and local work complete exactly once", calls[0] == 1 and actor.visible and not action.active)
	action.request(Vector2(40.0, 280.0), func() -> void: calls[0] += 1)
	action.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	action._process(10.0)
	_check("focus interruption cancels unearned local work", calls[0] == 1 and actor.visible and not action.active)
	var seahorse: PoolSeahorseRescueActivity = POOL_SEAHORSE.new()
	host.add_child(seahorse)
	seahorse.size = StorybookUI.CANVAS_SIZE
	seahorse.setup(Vector2(960.0, 390.0), Vector2(208.75, 241.25), 0)
	seahorse.bind_room_actor(actor, null, "classic")
	seahorse.start()
	seahorse._register_tap(seahorse.fixture_center)
	_check("seahorse tap requests work without instant credit", seahorse._taps == 0 and seahorse._contact_action.active)
	for index: int in range(80):
		seahorse._contact_action._process(0.05)
	_check("seahorse earns one tug after real contact", seahorse._taps == 1 and actor.visible)
	for _quick: int in range(3):
		seahorse._register_tap(seahorse.fixture_center)
	_check("quick taps during Roshan's tug wait their turn instead of vanishing",
		seahorse._taps == 1 and int(seahorse.audit_snapshot().get("queued_tugs", -1)) == 2)
	for index: int in range(80):
		seahorse._contact_action._process(0.05)
	_check("every waiting tap becomes its own contact tug",
		seahorse._taps == 4 and int(seahorse.audit_snapshot().get("queued_tugs", -1)) == 0
		and actor.visible)
	seahorse._register_tap(seahorse.fixture_center)
	seahorse._register_tap(seahorse.fixture_center)
	seahorse.cancel_touch()
	for index: int in range(80):
		seahorse._contact_action._process(0.05)
	_check("focus loss drops waiting taps with the unearned work",
		seahorse._taps == 4 and int(seahorse.audit_snapshot().get("queued_tugs", -1)) == 0)
	seahorse.stop()
	seahorse.free()
	actor.position = Vector2(80.0, 600.0)
	var waterfall: PoolWaterfallActivity = POOL_WATERFALL.new()
	host.add_child(waterfall)
	waterfall.size = StorybookUI.CANVAS_SIZE
	waterfall.setup(Vector2(700.0, 290.0), Vector2(260.0, 240.0), 0)
	waterfall.bind_room_actor(actor, null, "classic")
	waterfall.start()
	waterfall._begin_touch(waterfall.fixture_center, 4)
	waterfall._end_touch(waterfall.fixture_center, 4)
	var retarget_point: Vector2 = waterfall.fixture_center + Vector2(70.0, 0.0)
	waterfall._begin_touch(retarget_point, 5)
	_check("a touch on another lane retargets the unearned approach instead of vanishing",
		waterfall._lane_progress[1] == 0.0 and waterfall._touch_active
		and waterfall._touch_lane == 2 and waterfall._contact_action.active
		and int(waterfall.audit_snapshot().get("pending_lane", -1)) == 2)
	waterfall._end_touch(retarget_point, 5)
	waterfall._contact_action.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	waterfall._contact_action._process(10.0)
	_check("canceled waterfall work earns no progress",
		waterfall._lane_progress[1] == 0.0 and waterfall._lane_progress[2] == 0.0 and actor.visible)
	waterfall._begin_touch(waterfall.fixture_center, 4)
	waterfall._end_touch(waterfall.fixture_center, 4)
	for index: int in range(80):
		if index == 30:
			# Tapping the lane Roshan is already working never restarts her work.
			waterfall._begin_touch(waterfall.fixture_center, 6)
			waterfall._end_touch(waterfall.fixture_center, 6)
		waterfall._contact_action._process(0.05)
		waterfall._process(0.05)
	_check("waterfall earns one local scrub after arrival, even with a same-lane re-tap",
		is_equal_approx(waterfall._lane_progress[1], waterfall.TAP_ASSIST)
		and not waterfall._scrubber.visible and actor.visible)
	var stroke_start: Vector2 = waterfall.fixture_center - Vector2(waterfall.fixture_size.x / 3.0, 96.0)
	var stroke_end: Vector2 = stroke_start + Vector2(0.0, waterfall.fixture_size.y)
	waterfall._begin_touch(stroke_start, 7)
	waterfall._update_touch(stroke_end, 7)
	waterfall._end_touch(stroke_end, 7)
	_check("quick waterfall swipe waits for contact without remote credit", waterfall._lane_progress[0] == 0.0 and waterfall._contact_action.active)
	for index: int in range(80):
		waterfall._contact_action._process(0.05)
		waterfall._process(0.05)
	_check("released quick stroke completes locally and frees its owner", (waterfall._clear_mask & 1) != 0 and not waterfall._contact_action.active and actor.visible)
	waterfall._begin_touch(waterfall.fixture_center, 8)
	_check("waterfall accepts the next gesture after a quick stroke", waterfall._touch_active and waterfall._touch_id == 8)
	waterfall.cancel_touch()
	waterfall.stop()
	waterfall.free()
	action.free()
	actor.free()
