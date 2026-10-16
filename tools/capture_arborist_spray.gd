extends SceneTree
## Deterministic Mobile-renderer review using real viewport touch dispatch.
const OUT := "res://assets_src/review/arborist_spray_20261015/"
var level: OperaTreeBookTest
var failures := 0

func _init() -> void:
	call_deferred("_run")

func check(label: String, ok: bool) -> void:
	print("SPRAY_CAPTURE|%s|%s" % ["PASS" if ok else "FAIL", label])
	if not ok:
		failures += 1

func touch(down: bool, point: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 1
	event.pressed = down
	event.position = level.get_global_transform_with_canvas() * point
	root.push_input(event, true)
	await process_frame

func shot(label: String) -> void:
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	var result := root.get_texture().get_image().save_png(OUT + label + ".png")
	check("saved " + label, result == OK)

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	check("approved Mobile renderer", RenderingServer.get_current_rendering_method() == "mobile")
	root.size = Vector2i(1280, 720)
	level = OperaTreeBookTest.new()
	root.add_child(level)
	level.set_process(false)
	level.restore_progress({"version": 1, "patient": "orange_spots", "stage": 3})
	level.advance(0.55)
	await shot("01_approach")
	level.advance(0.55)
	await shot("02_ready")
	await touch(true, level.treatment_hint_rect().position + OperaTreeBookTest.HINT_TIP)
	check("pictured fingertip touch owns visible canopy", level.spray_active())
	for tick: int in range(8):
		level.advance(0.1)
	check("intentional hold gives partial healing", level.treatment > 0.4 and level.treatment < 0.6)
	await shot("03_spraying")
	await touch(false, OperaTreeBookTest.SPRAY_CONTACT)
	var dose := level.treatment
	level.advance(1.0)
	check("release stops spray and preserves healing", not level.spray_active() and is_equal_approx(dose, level.treatment))
	await shot("04_released")
	await touch(true, level.treatment_hint_rect().position + OperaTreeBookTest.HINT_TIP)
	for tick: int in range(12):
		level.advance(0.1)
	check("earned healthy endpoint", level.stage == 5 and level.treatment == 1.0)
	await shot("05_healthy")
	await touch(false, OperaTreeBookTest.SPRAY_CONTACT)
	root.size = Vector2i(1920, 900)
	await process_frame
	level.restore_progress({"version": 1, "patient": "orange_spots", "stage": 4, "treatment": 0.4})
	await touch(true, level.treatment_hint_rect().position + OperaTreeBookTest.HINT_TIP)
	check("wide viewport maps pictured fingertip touch", level.spray_active())
	level.advance(0.1)
	await shot("06_wide_touch")
	level.shutdown()
	level.queue_free()
	await process_frame
	print("SPRAY_CAPTURE|ALL OK" if failures == 0 else "SPRAY_CAPTURE|FAIL")
	quit(0 if failures == 0 else 1)
