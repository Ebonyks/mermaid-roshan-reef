extends SceneTree
## Focused headless contract probe for DayOnePoolCleanup.

const POOL_CLEANUP := preload("res://scripts/games/day_one_pool_cleanup.gd")
const RUNTIME_ASSETS: Array[String] = [
	"res://assets/castle/day_one_pool/pool_algae_trash.png",
	"res://assets/castle/day_one_pool/waterfall_clogged_turgid.png",
	"res://assets/castle/day_one_pool/pool_rim_grime.png",
	"res://assets/castle/day_one_pool/seahorse_sick.png",
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
	var clean_waterfall := Sprite2D.new()
	clean_waterfall.name = "CleanWaterfallProbeFixture"
	host.add_child(clean_waterfall)
	var flowing_water := Sprite2D.new()
	flowing_water.name = "FlowingWaterProbeLayer"
	host.add_child(flowing_water)
	main.castle_room_item_sprites["waterfall"] = {
		"sprite": clean_waterfall,
		"fixture_rig": {
			"water": [{"node": flowing_water}],
		},
	}
	var cleanup: DayOnePoolCleanup = POOL_CLEANUP.new() as DayOnePoolCleanup
	host.add_child(cleanup)
	cleanup.setup(main, false)
	await process_frame
	_check("dirty arrival hides pristine rainbow card",
		not clean_waterfall.visible)
	_check("dirty arrival stops animated rainbow flow",
		not flowing_water.visible)
	var snapshot: Dictionary = cleanup.audit_snapshot()
	_check("four staged cleanup subjects",
		int(snapshot.get("cleanup_step_count", 0)) == 4
		and int(snapshot.get("sprite_count", 0)) == 4
		and int(snapshot.get("button_count", 0)) == 4)
	_check("seahorse is final step",
		bool(snapshot.get("seahorse_is_last", false)))
	_check("2D dingy-lighting contract",
		bool(snapshot.get("dingy_lighting", false))
		and bool(snapshot.get("canvas_only", false)))
	_check("only first target initially accepts touch",
		not (cleanup.get_node("Clean_pool_surface") as Button).disabled
		and (cleanup.get_node("Clean_rainbow_fountain") as Button).disabled
		and (cleanup.get_node("Clean_pool_rim") as Button).disabled
		and (cleanup.get_node("Clean_seahorse") as Button).disabled)
	for asset_path: String in RUNTIME_ASSETS:
		var texture: Texture2D = load(asset_path) as Texture2D
		_check("runtime asset %s" % asset_path.get_file(),
			texture != null
			and maxf(texture.get_size().x, texture.get_size().y) <= 1024.0)
	var clogged_texture: Texture2D = load(
		"res://assets/castle/day_one_pool/waterfall_clogged_turgid.png"
	) as Texture2D
	var clogged_image: Image = clogged_texture.get_image() \
		if clogged_texture != null else null
	_check("clogged fixture fully occludes central rainbow lanes",
		clogged_image != null
		and clogged_image.get_pixel(501, 220).a > 0.98
		and clogged_image.get_pixel(501, 512).a > 0.98
		and clogged_image.get_pixel(501, 790).a > 0.98)
	for expected_step: int in range(1, 5):
		_check("cleanup step %d advances" % expected_step,
			cleanup.probe_advance_current_step()
			and main.day_one_pool_cleanup_step == expected_step)
		if expected_step == 1:
			_check("rainbow stays hidden before its cleanup step",
				not clean_waterfall.visible)
		elif expected_step == 2:
			_check("clean rainbow card returns after its cleanup step",
				clean_waterfall.visible)
		_check("animated rainbow flow remains stopped before finale activation",
			not flowing_water.visible)
	var final_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("finale creates Rumi reveal",
		bool(final_snapshot.get("finale_started", false))
		and bool(final_snapshot.get("rumi_present", false))
		and bool(final_snapshot.get("rumi_approved_identity", false))
		and bool(final_snapshot.get("rumi_authored_animation", false))
		and String(final_snapshot.get("rumi_animation", "")) == "swim")
	# The focused harness does not build ReefMain's HUD/audio tree. Detach the
	# stub before the delayed reveal callback while preserving animation checks.
	cleanup.m = null
	await create_timer(1.25).timeout
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
	_check("teardown restores pristine rainbow card", clean_waterfall.visible)
	_check("teardown restores prior animated-flow visibility", flowing_water.visible)
	host.queue_free()
	main.free()
	print("DAY_ONE_POOL|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_POOL|", label, ": ", "OK" if ok else "FAIL")
