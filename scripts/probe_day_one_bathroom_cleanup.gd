extends SceneTree
## Focused Canvas/mobile contract probe for DayOneBathroomCleanup.

const BATHROOM_CLEANUP := preload(
	"res://scripts/games/day_one_bathroom_cleanup.gd")
const RUNTIME_ASSETS: Array[String] = [
	"res://assets/castle/dirty_cleanup_2d/targets/target_cloudy_mirror.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_bath_soap_ring.png",
	"res://assets/castle/dirty_cleanup_2d/targets/target_floor_scuff.png",
	"res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_clean_ring.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png",
	"res://assets/castle/dirty_cleanup_2d/effects/fx_wipe_swoosh.png",
]

var checks_failed: int = 0
var completion_signals: int = 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var main := ReefMain.new()
	var host := Control.new()
	host.name = "DayOneBathroomProbeHost"
	host.size = StorybookUI.CANVAS_SIZE
	get_root().add_child(host)
	var cleanup: DayOneBathroomCleanup = BATHROOM_CLEANUP.new() \
		as DayOneBathroomCleanup
	host.add_child(cleanup)
	cleanup.cleanup_completed.connect(_on_cleanup_completed)
	cleanup.setup(main, false)
	await process_frame
	var snapshot: Dictionary = cleanup.audit_snapshot()
	_check("three short staged cleanup subjects",
		int(snapshot.get("cleanup_step_count", 0)) == 3
		and int(snapshot.get("sprite_count", 0)) == 3
		and int(snapshot.get("button_count", 0)) == 3)
	_check("single active one-finger target",
		int(snapshot.get("active_target_count", 0)) == 1)
	_check("older-phone touch targets stay generous",
		float(snapshot.get("minimum_touch_side", 0.0)) >= 96.0)
	_check("voice and picture guidance are configured",
		bool(snapshot.get("voice_guidance_configured", false))
		and bool(snapshot.get("has_visual_pointer", false)))
	_check("Canvas-only lighting and node tree",
		bool(snapshot.get("dingy_lighting", false))
		and bool(snapshot.get("canvas_only", false))
		and _all_runtime_children_are_canvas_items(cleanup))
	_check("only mirror initially accepts touch",
		not (cleanup.get_node("Clean_cloudy_mirror") as Button).disabled
		and (cleanup.get_node("Clean_bath_soap_ring") as Button).disabled
		and (cleanup.get_node("Clean_floor_scuff") as Button).disabled)
	await create_timer(0.12).timeout
	_check("passive time cannot clean a target",
		main.day_one_bathroom_cleanup_step == 0)
	for asset_path: String in RUNTIME_ASSETS:
		var texture: Texture2D = load(asset_path) as Texture2D
		_check("runtime asset %s" % asset_path.get_file(),
			texture != null
			and maxf(texture.get_size().x, texture.get_size().y) <= 1024.0)
	for expected_step: int in range(1, 4):
		_check("cleanup step %d advances" % expected_step,
			cleanup.probe_advance_current_step()
			and main.day_one_bathroom_cleanup_step == expected_step)
	var finale_snapshot: Dictionary = cleanup.audit_snapshot()
	_check("finale starts only after the third explicit touch",
		bool(finale_snapshot.get("finale_started", false))
		and completion_signals == 0)
	_check("finale commits once", cleanup.probe_finish_finale()
		and completion_signals == 1
		and bool(cleanup.audit_snapshot().get("completion_emitted", false))
		and not cleanup.probe_finish_finale())
	cleanup.teardown()
	await process_frame
	_check("teardown frees cleanup", not is_instance_valid(cleanup))

	var restored_main := ReefMain.new()
	restored_main.day_one_bathroom_cleanup_step = 2
	var restored: DayOneBathroomCleanup = BATHROOM_CLEANUP.new() \
		as DayOneBathroomCleanup
	host.add_child(restored)
	restored.setup(restored_main, false)
	await process_frame
	var restored_snapshot: Dictionary = restored.audit_snapshot()
	_check("re-entry restores the next unfinished stage",
		int(restored_snapshot.get("current_step", -1)) == 2
		and int(restored_snapshot.get("active_target_count", 0)) == 1
		and not (restored.get_node("Dirty_cloudy_mirror") as Sprite2D).visible
		and not (restored.get_node("Dirty_bath_soap_ring") as Sprite2D).visible
		and (restored.get_node("Dirty_floor_scuff") as Sprite2D).visible)
	restored.teardown()
	await process_frame
	host.queue_free()
	main.free()
	restored_main.free()
	print("DAY_ONE_BATHROOM|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _on_cleanup_completed() -> void:
	completion_signals += 1


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
