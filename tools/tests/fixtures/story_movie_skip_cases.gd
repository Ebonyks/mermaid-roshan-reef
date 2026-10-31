extends RefCounted
## Shared real-player input cases, called by the trusted story probe and the
## small standalone fixture so the same cases can run without all game art.

class ClockPlayer extends "res://scripts/day_one_story_clips.gd":
	var test_ms: int = 1000
	func _pointer_time_ms() -> int:
		return test_ms

var tree: SceneTree
var check: Callable
var signals: int = 0

func run(scene_tree: SceneTree, assertion: Callable) -> void:
	tree = scene_tree
	check = assertion
	DayOneStoryClips.headless_override = true
	var original_paused: bool = tree.paused
	tree.paused = false
	var player: ClockPlayer = _player()
	await tree.process_frame
	await tree.process_frame
	check.call("double-tap fixture plays the real movie", player.player.is_playing())
	_tap(player, 0, Vector2(400, 300))
	check.call("one touch tap keeps the movie and game pause", signals == 0 and tree.paused)
	# Touch-generated mouse events must not become the second tap.
	_mouse(player, true, InputEvent.DEVICE_ID_EMULATION)
	_mouse(player, false, InputEvent.DEVICE_ID_EMULATION)
	check.call("emulated mouse does not duplicate a physical tap", signals == 0)
	_tap(player, 0, Vector2(410, 305))
	check.call("two short touch taps skip and restore gameplay once", signals == 1 and not tree.paused)
	player.skip()
	check.call("double-tap followed by Back cannot finish twice", signals == 1)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	player.test_ms += DayOneStoryClips.DOUBLE_TAP_MS + 1
	_tap(player, 0, Vector2(400, 300))
	check.call("separated taps do not skip", signals == 0 and tree.paused)
	_close(player)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	_tap(player, 0, Vector2(800, 300))
	check.call("two distant taps do not skip", signals == 0)
	_close(player)
	await tree.process_frame
	player = _player()
	_touch(player, 0, true, Vector2(400, 300))
	player.test_ms += DayOneStoryClips.MAX_TAP_MS + 1
	_touch(player, 0, false, Vector2(400, 300))
	_tap(player, 0, Vector2(400, 300))
	check.call("a hold followed by a tap does not skip", signals == 0)
	_close(player)
	await tree.process_frame
	player = _player()
	_touch(player, 0, true, Vector2(400, 300))
	var drag: InputEventScreenDrag = InputEventScreenDrag.new()
	drag.index = 0
	drag.position = Vector2(500, 300)
	player._input(drag)
	# Returning to the press point must not turn the drag into a tap.
	_touch(player, 0, false, Vector2(400, 300))
	_tap(player, 0, Vector2(400, 300))
	check.call("drag and return followed by a tap do not skip", signals == 0)
	_close(player)
	await tree.process_frame
	player = _player()
	_touch(player, 0, true, Vector2(400, 300))
	_touch(player, 1, true, Vector2(420, 300))
	_touch(player, 1, false, Vector2(420, 300))
	_touch(player, 0, false, Vector2(400, 300))
	_tap(player, 0, Vector2(400, 300))
	check.call("two simultaneous fingers followed by one tap do not skip", signals == 0)
	_close(player)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	var cancel: InputEventScreenTouch = InputEventScreenTouch.new()
	cancel.index = 0
	cancel.canceled = true
	player._input(cancel)
	_tap(player, 0, Vector2(400, 300))
	check.call("canceled touch clears the first tap", signals == 0)
	_close(player)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	player._notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_tap(player, 0, Vector2(400, 300))
	check.call("focus loss suppresses movie skip input", signals == 0 and player.player.paused)
	player._notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_tap(player, 0, Vector2(400, 300))
	check.call("focus return starts a fresh tap pair", signals == 0)
	_tap(player, 0, Vector2(400, 300))
	check.call("a fresh double tap works after focus return", signals == 1)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	player._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	_tap(player, 0, Vector2(400, 300))
	check.call("backgrounding suppresses movie skip input", signals == 0)
	player._notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	_tap(player, 0, Vector2(400, 300))
	check.call("app resume clears the earlier tap", signals == 0)
	_tap(player, 0, Vector2(400, 300))
	check.call("a fresh double tap works after app resume", signals == 1)
	await tree.process_frame
	player = _player()
	_mouse(player, true)
	_mouse(player, false)
	check.call("one mouse click keeps the movie", signals == 0)
	_mouse(player, true)
	_mouse(player, false)
	check.call("two mouse clicks skip the movie", signals == 1)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	_close(player)
	await tree.process_frame
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	check.call("the next movie does not inherit the previous tap", signals == 0)
	_close(player)
	await tree.process_frame
	tree.paused = true
	player = _player()
	_tap(player, 0, Vector2(400, 300))
	_tap(player, 0, Vector2(400, 300))
	check.call("skip preserves a caller that was already paused", signals == 1 and tree.paused)
	await tree.process_frame
	# Use actual viewport dispatch for the input-ownership check.
	tree.paused = false
	player = _player()
	await tree.process_frame
	_touch(player, 0, true, Vector2(400, 300), true)
	_touch(player, 0, false, Vector2(400, 300), true)
	check.call("viewport-dispatched single tap keeps the story", signals == 0 and tree.paused)
	_touch(player, 0, true, Vector2(400, 300), true)
	_touch(player, 0, false, Vector2(400, 300), true)
	check.call("viewport double-tap release is consumed before resume",
		signals == 1 and tree.root.is_input_handled() and not tree.paused)
	await tree.process_frame
	tree.paused = original_paused
	DayOneStoryClips.headless_override = false

func _player() -> ClockPlayer:
	signals = 0
	var player: ClockPlayer = ClockPlayer.new()
	tree.root.add_child(player)
	player.finished.connect(func(_id: String, _status: String) -> void:
		signals += 1)
	check.call("skip case sets up a real OGV", player.setup("d1_rainbow_route"))
	return player

func _close(player: ClockPlayer) -> void:
	player.skip()

func _touch(player: ClockPlayer, index: int, pressed: bool,
		position: Vector2, dispatch: bool = false) -> void:
	player.test_ms += 40
	var event: InputEventScreenTouch = InputEventScreenTouch.new()
	event.index = index
	event.pressed = pressed
	event.position = position
	if dispatch:
		tree.root.push_input(event)
	else:
		player._input(event)

func _tap(player: ClockPlayer, index: int, position: Vector2) -> void:
	_touch(player, index, true, position)
	_touch(player, index, false, position)

func _mouse(player: ClockPlayer, pressed: bool, device: int = 0) -> void:
	player.test_ms += 40
	var event: InputEventMouseButton = InputEventMouseButton.new()
	event.device = device
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = Vector2(400, 300)
	player._input(event)
