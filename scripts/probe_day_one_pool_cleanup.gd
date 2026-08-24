extends SceneTree
## Focused exact-Godot contract probe for the three Day One pool activities.

const POOL_CLEANUP := preload("res://scripts/games/day_one_pool_cleanup.gd")
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
]

var checks_failed: int = 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var main := ReefMain.new()
	var host := Control.new()
	host.name = "DayOnePoolProbeHost"
	host.size = StorybookUI.CANVAS_SIZE
	get_root().add_child(host)
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
	for asset_path: String in RUNTIME_ASSETS:
		var texture: Texture2D = load(asset_path) as Texture2D
		_check("runtime asset %s" % asset_path.get_file(),
			texture != null
			and maxf(texture.get_size().x, texture.get_size().y) <= 1024.0)

	await create_timer(0.12).timeout
	var passive: Dictionary = cleanup.audit_snapshot()
	_check("passive demo never advances",
		int(main.day_one_pool_skimmer_mask) == 0
		and int((passive.get("skimmer", {}) as Dictionary).get("progress_mask", -1)) == 0)

	_check("skimmer activity accepts six real collections",
		cleanup.probe_complete_current_activity())
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
			Vector2(162.5, 220.0)))
	_check("static clean card under scrub lanes but flow remains stopped",
		clean_waterfall.visible and not flowing_water.visible
		and bool(after_pool.get("animated_water_hidden", false)))

	_check("waterfall activity clears three independent lanes",
		cleanup.probe_complete_current_activity())
	await create_timer(0.56).timeout
	var after_waterfall: Dictionary = cleanup.audit_snapshot()
	_check("waterfall completion persists and unlocks seahorse",
		main.day_one_pool_waterfall_mask == 0x07
		and main.day_one_pool_cleanup_step == 2
		and String(after_waterfall.get("current_activity", "")) == "seahorse")
	_check("rainbow animation still waits for rescue finale",
		clean_waterfall.visible and not flowing_water.visible)

	_check("one seahorse tap advances monotonically",
		cleanup.seahorse_activity.probe_tap())
	await process_frame
	_check("partial tug saves without premature finale",
		main.day_one_pool_seahorse_tugs == 1
		and main.day_one_pool_cleanup_step == 2
		and not bool(cleanup.audit_snapshot().get("finale_started", false)))
	_check("remaining rapid taps start causal extraction",
		cleanup.probe_complete_current_activity())
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

	cleanup.m = null
	await create_timer(0.52).timeout
	await create_timer(0.74).timeout
	var wave_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("Rumi performs authored wave after rising",
		String(wave_snapshot.get("rumi_animation", "")) == "wave")
	await create_timer(1.1).timeout
	var idle_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("Rumi settles into authored idle",
		String(idle_snapshot.get("rumi_animation", "")) == "idle")
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


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_POOL|", label, ": ", "OK" if ok else "FAIL")
