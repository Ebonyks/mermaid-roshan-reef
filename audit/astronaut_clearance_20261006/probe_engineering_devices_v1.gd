extends SceneTree
const Surface := preload("res://scripts/opera_astronaut_surface.gd")
var failures := 0
var checks := 0
var earned := 0.0


func _init() -> void:
	call_deferred("_run")


func check(label: String, passed: bool) -> void:
	checks += 1
	if not passed:
		failures += 1
	print("ENGINEER_DEVICES|", "PASS|" if passed else "FAIL|", label)


func touch(s: OperaAstronautSurface, at: Vector2, down: bool, finger: int = 7) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.position = at
	event.pressed = down
	s._gui_input(event)


func drag(s: OperaAstronautSurface, at: Vector2, finger: int = 7) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = at
	s._gui_input(event)


func gesture(_kind: String, amount: float, _quality: float) -> void:
	earned += amount


func _run() -> void:
	var s := Surface.new()
	root.add_child(s)
	s.size = Vector2(712, 560)
	s.gesture.connect(gesture)
	s.configure("gears", Color.WHITE)
	await process_frame
	check("new gear source is imported raster", s.devices.gear_texture != null)
	for index in range(180):
		s._process(1.0 / 30.0)
	check("six seconds passive gear demo earns nothing", is_zero_approx(earned) and s.devices.fitted == [false, false, false])
	touch(s, s.devices.home(0), true)
	touch(s, s.devices.home(1), true, 8)
	drag(s, s.devices.socket(1), 8)
	check("second finger cannot steal the carried gear", s.active_touch_index == 7 and s.devices.selected == 0 and s.devices.drag_at.is_equal_approx(s.devices.home(0)))
	drag(s, s.devices.socket(2))
	touch(s, s.devices.socket(2), false)
	check("wrong-sized socket returns piece with no request or payout", s.devices.pending == -1 and s.pipe_work_cell == -1 and is_zero_approx(earned))
	touch(s, s.devices.home(0), true)
	drag(s, s.devices.socket(0))
	touch(s, s.devices.socket(0), false)
	var request := s.pipe_work_request_id
	check("correct gear waits for world acknowledgment", s.devices.pending == 0 and not s.devices.fitted[0] and is_zero_approx(earned))
	check("stale acknowledgment cannot install it", not s.commit_device_work(request - 1))
	check("surface fixture acknowledgment installs exactly one", s.commit_device_work(request) and is_equal_approx(earned, 1.0) and s.devices.fitted == [true, false, false])
	check("repeated acknowledgment cannot award twice", not s.commit_device_work(request) and is_equal_approx(earned, 1.0))
	var saved := s.progress_snapshot()
	s.configure("gears", Color.WHITE)
	check("installed gear survives mechanic restore without ownership", s.restore_progress(saved, 1.0, 3.0) and s.devices.fitted == [true, false, false] and not s.held and s.active_touch_index == -1)
	check("state cannot fabricate a higher saved score", not s.restore_progress(saved, 2.0, 3.0))
	touch(s, s.devices.home(1), true)
	drag(s, s.devices.socket(1))
	s.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	touch(s, s.devices.socket(1), false)
	check("focus loss cancels uncommitted gear without erasing installed work", not s.held and s.devices.pending == -1 and s.devices.selected == -1 and s.devices.fitted == [true, false, false] and is_equal_approx(earned, 1.0))
	s.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	s.configure("pressure", Color.WHITE)
	earned = 0.0
	for index in range(180):
		s._process(1.0 / 30.0)
	check("passive pressure gauges never earn completion", is_zero_approx(earned) and s.devices.tuned == [false, false, false])
	touch(s, s.devices.valve(0), true)
	touch(s, s.devices.valve(0), false)
	check("stationary taps cannot substitute for pressure adjustment", s.devices.pending == -1 and is_zero_approx(earned))
	var start := s.devices.valve(0)
	touch(s, start, true)
	drag(s, start + Vector2(0, 30))
	touch(s, start + Vector2(0, 30), false)
	check("incorrect adjustment commits safely without payout", s.commit_device_work(s.pipe_work_request_id) and is_zero_approx(earned) and is_zero_approx(s.devices.values[0]) and not s.devices.tuned[0])
	start = s.devices.valve(0)
	touch(s, start, true)
	drag(s, start - Vector2(0, 63))
	s.notification(Node.NOTIFICATION_PAUSED)
	check("pause preserves last released pressure and drops preview", is_zero_approx(s.devices.values[0]) and s.devices.selected == -1 and not s.held)
	s.notification(Node.NOTIFICATION_UNPAUSED)
	touch(s, start, true)
	drag(s, start - Vector2(0, 63))
	touch(s, start - Vector2(0, 63), false)
	check("correct tuned gauge earns once through explicit acknowledgment", s.commit_device_work(s.pipe_work_request_id) and is_equal_approx(earned, 1.0) and s.devices.tuned[0])
	saved = s.progress_snapshot()
	s.configure("pressure", Color.WHITE)
	check("tuned gauge and valve setting survive mechanic restore", s.restore_progress(saved, 1.0, 3.0) and s.devices.tuned[0] and is_equal_approx(s.devices.values[0], 0.35))
	var corrupt := saved.duplicate(true)
	corrupt["devices"]["values"][0] = 0.0
	check("a tuned save outside its true band is rejected", not s.restore_progress(corrupt, 1.0, 3.0))
	var world := OperaCareerWorld2D.new()
	world.phases = (OperaCareerWorld2D.PHASES["astronaut"] as Array).duplicate(true)
	world.astronaut_legacy_phases = world.phases.duplicate(true)
	world._apply_astronaut_engineering_devices()
	world.astronaut_phase_signature = JSON.stringify(world.phases).sha256_text()
	var legacy_surface := Surface.new()
	legacy_surface.size = Vector2(712, 560)
	legacy_surface.configure("tap", Color.WHITE, 1, "target_astronaut")
	legacy_surface.target_placed[0] = true
	legacy_surface.target_placed[1] = true
	var old := {"version": 1, "phase_index": 1, "progress": 2.0, "complete": false, "mechanic": legacy_surface.progress_snapshot()}
	var migrated := world._migrate_astronaut_checkpoint(old)
	check("legacy partial repair retains upward-rounded earned gear credit and exact original", float(migrated.get("progress", 0.0)) == 2.0 and migrated.get("legacy_checkpoint_before_engineering", {}) == old)
	s.configure("gears", Color.WHITE)
	check("legacy converted gear state is internally consistent", s.restore_progress(migrated["mechanic"], 2.0, 3.0) and s.devices.fitted == [true, true, false])
	var forged := old.duplicate(true)
	forged["mechanic"]["targets"] = [false, false, false, false, false]
	check("legacy progress cannot fabricate unperformed repair work", world._migrate_astronaut_checkpoint(forged).is_empty())
	old["phase_index"] = 0
	old["progress"] = 1.0
	legacy_surface.configure("pipe", Color.WHITE)
	legacy_surface.pipe_grid[5] = "H"
	legacy_surface.pipe_grid[6] = "H"
	legacy_surface.pipe_tray.clear()
	legacy_surface.pipe_round = 1
	legacy_surface.pipe_pause = 1.0
	old["mechanic"] = legacy_surface.progress_snapshot()
	migrated = world._migrate_astronaut_checkpoint(old)
	check("old earned pipe boards become the complete single-board task", migrated.get("complete", false) and migrated.get("legacy_earned_pipe", false) and float(migrated.get("progress", 0.0)) == 1.0)
	old["progress"] = 999.0
	check("invalid legacy earned progress is rejected", world._migrate_astronaut_checkpoint(old).is_empty())
	legacy_surface.free()
	world.free()
	s.queue_free()
	await process_frame
	print("ENGINEER_DEVICES|RESULT|", JSON.stringify({"checks": checks, "failures": failures, "scope": "Surface event fixture and migration negatives. World native contact acceptance is separate."}))
	quit(0 if failures == 0 else 1)
