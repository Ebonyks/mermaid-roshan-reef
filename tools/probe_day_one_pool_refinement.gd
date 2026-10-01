extends SceneTree
## Independent contact/carry/drop, interruption and exact-pixel packing assertions.

var checks: Array[Dictionary] = []
var completion_count: int = 0

func _initialize() -> void:
	_run.call_deferred()

func _run() -> void:
	var activity: PoolSkimmerActivity = PoolSkimmerActivity.new()
	root.add_child(activity)
	activity.setup()
	activity.completed.connect(_completed)
	activity.start()
	activity.set_process(false)
	var cue_targets: Array[int] = []
	var truthful_cue: bool = true
	for _tick: int in range(600):
		activity._process(1.0 / 60.0)
		if activity._demo_pointer.visible:
			var target: int = activity._demo_target_index
			if not cue_targets.has(target):
				cue_targets.append(target)
			var intended_tip: Vector2 = activity._trash_contact_position(target) + Vector2(0.0,
				PoolSkimmerActivity.TRASH_MAX_SIZES[target].y * 0.5 + PoolSkimmerActivity.POINTER_TARGET_MARGIN)
			var actual_tip: Vector2 = activity._demo_pointer.get_transform() * PoolSkimmerActivity.POINTER_TIP_OFFSET
			truthful_cue = truthful_cue and actual_tip.distance_to(intended_tip) < 0.25
	_check("passive actor never collects", int(activity.audit_snapshot()["mask"]) == 0)
	_check("idle cue visits all six real objects", cue_targets.size() == 6)
	_check("breathing cue fingertip remains below actual target", truthful_cue)
	for index: int in range(6):
		_tap(activity, index)
		var ticks: int = 0
		while (int(activity.audit_snapshot()["mask"]) & (1 << index)) == 0 and ticks < 360:
			activity._process(1.0 / 60.0)
			ticks += 1
		_check("item%d catch waits for local action" % index, ticks > 24 and activity.has_pending_transfer())
		_check("item%d caught mask monotonic" % index, int(activity.audit_snapshot()["mask"]) == (1 << (index + 1)) - 1)
		var attached: bool = true
		var stable_scale: bool = true
		var transparent: bool = false
		var saw_drop: bool = false
		var landing_exact: bool = false
		var return_seen: bool = false
		var return_bounded: bool = true
		ticks = 0
		while activity.has_pending_transfer() and ticks < 360:
			var before_return: Vector2 = activity._cleaner.position
			var was_returning: bool = activity._returning_to_room
			activity._process(1.0 / 60.0)
			if was_returning:
				return_seen = true
				return_bounded = return_bounded and activity._cleaner.position.distance_to(before_return) <= PoolSkimmerActivity.SWIM_SPEED / 60.0 + 0.01
			var piece: Sprite2D = activity._trash_sprites[index]
			if activity._transport_index >= 0:
				transparent = transparent or piece.modulate.a < 0.8 or not piece.visible
				if activity._drop_time <= 0.0:
					attached = attached and piece.position.distance_to(activity._skimmer_position) < 0.01
					stable_scale = stable_scale and piece.scale.is_equal_approx(activity._transport_scale)
				else:
					saw_drop = true
			else:
				var stored: Sprite2D = activity._basket_contents[index]
				landing_exact = piece.position.is_equal_approx(stored.position) and piece.scale.is_equal_approx(stored.scale)
			ticks += 1
		_check("item%d stays attached/full-sized/opaque during carry" % index, attached and stable_scale and not transparent)
		_check("item%d visible drop ends at exact stored pose" % index, saw_drop and landing_exact and activity._basket_contents[index].visible)
		if index == 5:
			_check("last landing precedes bounded visible room return", return_seen and return_bounded and activity._cleaner.position.is_equal_approx(PoolSkimmerActivity.ROOM_RETURN_POSITION))
	_check("six stored items and one completion", activity._visible_basket_contents() == 6 and completion_count == 1)
	activity.stop()
	activity.show_basket_only(true)
	_check("later-phase basket passive and free pieces hidden", activity.mouse_filter == Control.MOUSE_FILTER_IGNORE and _all_hidden(activity))
	activity.setup(21)
	_check("partial restore shows exact stored count", activity._visible_basket_contents() == 3)
	activity.start()
	activity.set_process(false)
	_tap(activity, 1)
	for _tick: int in range(360):
		activity._process(1.0 / 60.0)
		if activity.has_pending_transfer():
			break
	_check("interruption fixture caught before landing", activity.has_pending_transfer() and activity._progress_mask == 23)
	activity.cancel_touch()
	activity.stop()
	_check("interrupt settles caught item without progress loss", not activity.has_pending_transfer() and activity._progress_mask == 23 and activity._basket_contents[1].visible)
	activity.setup(23)
	_check("re-entry restores four caught items", activity._visible_basket_contents() == 4)
	var rescue: PoolSeahorseRescueActivity = PoolSeahorseRescueActivity.new()
	root.add_child(rescue)
	rescue.size = Vector2(1280.0, 720.0)
	rescue.setup(Vector2(920.0, 245.0), Vector2(209.0, 241.0))
	_check("standalone rescue retains visible local basket", rescue._basket.visible)
	rescue.bind_cleanup_basket(activity._basket)
	_check("composed rescue hides duplicate basket", not rescue._basket.visible)
	_check("shared target resolves actual basket transform", rescue._basket_position.is_equal_approx(activity._basket.global_position))
	rescue.bind_cleanup_basket(null)
	_check("unbound rescue restores local basket", rescue._basket.visible)
	rescue.free()
	_probe_pixels()
	activity.free()
	var failures: int = 0
	for check: Dictionary in checks:
		if not bool(check["pass"]):
			failures += 1
	var output: String = OS.get_environment("POOL_REFINEMENT_PROBE_OUT")
	if output != "":
		var file: FileAccess = FileAccess.open(output, FileAccess.WRITE)
		file.store_string(JSON.stringify({"engine": Engine.get_version_info(), "checks": checks, "failures": failures}, "\t") + "\n")
		file.close()
	print("POOL_REFINEMENT|RESULT: %s checks=%d failures=%d" % ["PASS" if failures == 0 else "FAIL", checks.size(), failures])
	quit(1 if failures > 0 else 0)

func _probe_pixels() -> void:
	var source: Image = Image.load_from_file("res://assets/castle/day_one_pool/activities/floating_trash_atlas.png")
	var packed: Image = Image.load_from_file(PoolSkimmerActivity.TRASH_ATLAS_PATH)
	_check("packed atlas POT1024", packed.get_size() == Vector2i(1024, 1024))
	_check("original leaf RGBA bytes preserved", source.get_region(Rect2i(0, 341, 341, 341)).get_data() == packed.get_region(Rect2i(0, 341, 341, 341)).get_data())
	var tool_source: Image = Image.load_from_file("res://assets_src/imagegen/day1_pool_skimmer_v2_20261001/normalized1024/pool-skimmer.png")
	var tool: Image = Image.load_from_file(PoolSkimmerActivity.SKIMMER_PATH)
	_check("POT padding retains complete skimmer RGBA", tool.get_size() == Vector2i(1024, 1024) and tool.get_region(Rect2i(0, 0, 1024, 683)).get_data() == tool_source.get_data())

func _all_hidden(activity: PoolSkimmerActivity) -> bool:
	for piece: Sprite2D in activity._trash_sprites:
		if piece.visible:
			return false
	return true

func _tap(activity: PoolSkimmerActivity, index: int) -> void:
	var event: InputEventScreenTouch = InputEventScreenTouch.new()
	event.index = 0
	event.pressed = true
	event.position = activity._trash_contact_position(index)
	activity._gui_input(event)
	event.pressed = false
	activity._gui_input(event)

func _completed() -> void:
	completion_count += 1

func _check(name: String, passed: bool) -> void:
	checks.append({"name": name, "pass": passed})
	print("POOL_REFINEMENT|%s|%s" % ["PASS" if passed else "FAIL", name])
