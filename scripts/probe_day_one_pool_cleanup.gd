extends SceneTree
## Focused headless contract probe for DayOnePoolCleanup.

const POOL_CLEANUP := preload("res://scripts/games/day_one_pool_cleanup.gd")
const RUNTIME_ASSETS: Array[String] = [
	"res://assets/castle/day_one_pool/pool_algae_trash.png",
	"res://assets/castle/day_one_pool/waterfall_growth.png",
	"res://assets/castle/day_one_pool/pool_rim_grime.png",
	"res://assets/castle/day_one_pool/seahorse_sick.png",
	"res://assets/castle/day_one_pool/rumi_violet.png",
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
	var cleanup: DayOnePoolCleanup = POOL_CLEANUP.new() as DayOnePoolCleanup
	host.add_child(cleanup)
	cleanup.setup(main, false)
	await process_frame
	var snapshot: Dictionary = cleanup.audit_snapshot()
	_check("four staged cleanup subjects",
		int(snapshot.get("cleanup_step_count", 0)) == 4
		and int(snapshot.get("sprite_count", 0)) == 4
		and int(snapshot.get("button_count", 0)) == 4)
	_check("seahorse is final step",
		bool(snapshot.get("seahorse_is_last", false)))
	_check("2D dingy-lighting contract",
		bool(snapshot.get("dingy_lighting", false))
		and bool(snapshot.get("node_3d_free", false)))
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
	for expected_step: int in range(1, 5):
		_check("cleanup step %d advances" % expected_step,
			cleanup.probe_advance_current_step()
			and main.day_one_pool_cleanup_step == expected_step)
	var final_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("finale creates Rumi reveal",
		bool(final_snapshot.get("finale_started", false))
		and bool(final_snapshot.get("rumi_present", false)))
	cleanup.teardown()
	await process_frame
	_check("teardown frees cleanup", not is_instance_valid(cleanup))
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
