extends SceneTree
## Focused contract for Faron's three-doll Canvas catcher.
##
## Covers the real one-finger verb, zero-input safety, mercy, picture-first
## progress, approved art, bounded nodes, neutral exit, rapid replacement,
## persistence, medal upgrade semantics, and clean re-entry.

const PANEL_SIZE := Vector2(1024.0, 608.0)
const EXPECTED_WORLD_TILES: Array[String] = [
	"res://assets/opera/worlds/backdrops/world_nursery_c0r0.png",
	"res://assets/opera/worlds/backdrops/world_nursery_c1r0.png",
	"res://assets/opera/worlds/backdrops/world_nursery_c0r1.png",
	"res://assets/opera/worlds/backdrops/world_nursery_c1r1.png",
]
const EXPECTED_BABIES: Array[String] = [
	"res://assets/opera/worlds/nursery/baby_0.png",
	"res://assets/opera/worlds/nursery/baby_1.png",
	"res://assets/opera/worlds/nursery/baby_2.png",
]
const PLACEHOLDER_WIDGETS: Array[String] = [
	"res://assets/opera/worlds/widgets/widget_catch_nursery.png",
	"res://assets/opera/worlds/widgets/widget_catch_nursery_cradle.png",
	"res://assets/opera/worlds/widgets/widget_catch_nursery_pillows.png",
]
const MAX_STAGE_NODES := 5
const TOUCH_INDEX := 41

var main: ReefMain
var bad := 0
var finger_pos := Vector2.ZERO


func _init() -> void:
	seed(20260809)
	Engine.time_scale = 6.0
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await _frames(8)

	var friend: Dictionary = _dolls_friend()
	_check("Faron's Dolls friend exists", not friend.is_empty())
	if friend.is_empty():
		_finish()
		return
	_check("fresh isolated save has not pre-won Dolls",
		not bool(friend.get("won", false))
		and int(main.medals.get("dolls", 0)) == 0)
	friend["found"] = true

	# Materialise the optional speaker layer before taking the lifecycle
	# baseline so its intended z-order is tested without changing teardown math.
	main._flash_speaker_icon("faron")
	await process_frame
	var direct_baseline: Dictionary = _direct_child_ids()
	var game_nodes_baseline: Array[int] = _game_node_ids()
	var controls_baseline: Dictionary = main.touch_control_blocks.duplicate(true)
	var progress_baseline: Dictionary = _progress_snapshot(friend)
	var save_generation_baseline: int = main.save_generation

	# A cached Dolls satellite that does not own the block may never re-enable
	# controls belonging to another overlay.
	var dolls_game := main._game_obj("dolls", DollsGame) as DollsGame
	main._set_world_controls_enabled(false, "probe_foreign")
	dolls_game.stage_close()
	_check("unowned close preserves another control owner's block",
		main.touch_control_blocks.has("probe_foreign")
		and not main.touch_ui.world_controls_enabled)
	main._set_world_controls_enabled(true, "probe_foreign")
	_check("foreign fixture cleanup restores the exact control baseline",
		main.touch_control_blocks == controls_baseline
		and main.touch_ui.world_controls_enabled)

	# First entry is deliberately passive: misses are safe, never score, and
	# never mutate save, medal, or trophy progress.
	main._start_game(friend)
	var first_entry_layer := _active_layer()
	var first_entry_direct_ok := _only_layer_added(
		direct_baseline, first_entry_layer)
	await _frames(12)
	var layer := _active_layer()
	var surface := _active_surface()
	var world := _active_world_backdrop()
	var backing := _active_backing()
	var catcher := _active_catcher()
	_check_entry_contract(layer, surface, world, backing, catcher,
		first_entry_direct_ok, game_nodes_baseline)
	if layer == null or surface == null or world == null \
			or backing == null or catcher == null:
		_finish()
		return
	var center_fixture_guard := 0
	while surface.fallers.is_empty() and center_fixture_guard < 30:
		center_fixture_guard += 1
		await process_frame
	_check("passive fixture uses a center-lane falling baby",
		_force_center_faller(surface))
	await _capture_requested("falling")

	var passive_max_nodes := _subtree_node_count(layer)
	var passive_max_fallers := surface.fallers.size()
	var passive_max_landings := surface.safe_landings.size()
	var passive_guard := 0
	var miss_capture_written := false
	while main.game == "dolls" and surface.missed < 2 and passive_guard < 420:
		passive_guard += 1
		passive_max_nodes = maxi(passive_max_nodes, _subtree_node_count(layer))
		passive_max_fallers = maxi(passive_max_fallers, surface.fallers.size())
		passive_max_landings = maxi(
			passive_max_landings, surface.safe_landings.size())
		await process_frame
		if not miss_capture_written and surface.missed >= 1 \
				and not surface.safe_landings.is_empty():
			_check("center-lane miss rests below every active target and sling",
				_center_safe_geometry_ok(surface, catcher))
			await _capture_requested("miss_safe")
			miss_capture_written = true
			if OS.get_environment("DOLLS_CAPTURE_ONLY") == "1":
				print("DOLLS|result: CAPTURE OK")
				quit()
				return
	_check("zero input makes two pillow-safe misses and no catch",
		surface.missed >= 2 and surface.caught == 0 and surface.active
		and main.game == "dolls")
	_check("passive play leaves all persistent progress unchanged",
		_progress_snapshot(friend) == progress_baseline
		and main.save_generation == save_generation_baseline)
	_check("runtime mirrors the exact miss metric and picture pip count",
		int(main.g.get("missed", -1)) == surface.missed
		and int(main.g.get("caught", -1)) == 0
		and String(main.hud_game.text)
			== "Sleepy dolls  " + main._pips(0, 3, "🎎")
		and surface.goal == 3 and surface.settled.is_empty())
	_check("passive dictionaries stay bounded without child growth",
		passive_max_nodes <= MAX_STAGE_NODES
		and passive_max_fallers <= 1
		and passive_max_landings <= 2
		and surface.settled.size() <= 3)
	_check("a safe miss invokes the exact rate-limited Faron cue",
		main.said_cool.has("faron_miss")
		and _voice_pool_has("res://assets/audio/voices/faron_miss.ogg"))

	var mercy_guard := 0
	while surface.fallers.is_empty() and mercy_guard < 80:
		mercy_guard += 1
		await process_frame
	var mercy_ok := false
	if not surface.fallers.is_empty():
		var mercy_entry: Dictionary = surface.fallers[0]
		mercy_ok = absf(float(mercy_entry.get("base_x", -1.0))
			- surface.catcher_x) <= 0.091 \
			and float(mercy_entry.get("speed", 1.0)) <= 0.184
	_check("after two misses the next baby is nearer and slower", mercy_ok)

	var passive_layer_ref: WeakRef = weakref(layer)
	var passive_surface_ref: WeakRef = weakref(surface)
	var passive_world_ref: WeakRef = weakref(world)
	var passive_backing_ref: WeakRef = weakref(backing)
	var passive_catcher_ref: WeakRef = weakref(catcher)
	var direct_before_neutral_exit: Dictionary = _direct_child_ids()
	var direct_after_neutral_exit: Dictionary = \
		direct_before_neutral_exit.duplicate(true)
	direct_after_neutral_exit.erase(layer.get_instance_id())
	main._leave_current_activity()
	_check("neutral exit synchronously detaches Dolls only",
		main.game == "" and main.g.is_empty()
		and _active_layer_count() == 0
		and layer.get_parent() == null
		and _direct_child_ids() == direct_after_neutral_exit
		and _game_node_ids() == game_nodes_baseline
		and main.touch_control_blocks == controls_baseline
		and main.touch_ui.world_controls_enabled)
	await _frames(2)
	_check("neutral exit frees the complete five-node subtree",
		passive_layer_ref.get_ref() == null
		and passive_surface_ref.get_ref() == null
		and passive_world_ref.get_ref() == null
		and passive_backing_ref.get_ref() == null
		and passive_catcher_ref.get_ref() == null)
	_check("neutral exit is neither a win nor an award",
		_progress_snapshot(friend) == progress_baseline
		and main.save_generation > save_generation_baseline)

	# Re-enter, then exercise build's defensive synchronous replacement. This
	# proves repeated taps/manual calls cannot accumulate a second live layer.
	var reentry_direct_baseline: Dictionary = _direct_child_ids()
	main._start_game(friend)
	var reentry_layer := _active_layer()
	var reentry_direct_ok := _only_layer_added(
		reentry_direct_baseline, reentry_layer)
	await _frames(12)
	var replaced_layer := _active_layer()
	var replaced_layer_ref: WeakRef = weakref(replaced_layer)
	var replacement_baseline: Dictionary = _direct_child_ids()
	replacement_baseline.erase(replaced_layer.get_instance_id())
	dolls_game.build(friend)
	var win_layer := _active_layer()
	var win_surface := _active_surface()
	var replacement_direct_ok := _only_layer_added(
		replacement_baseline, win_layer)
	_check("rapid rebuild replaces, rather than duplicates, the Canvas layer",
		replaced_layer != null and replaced_layer.get_parent() == null
		and win_layer != null and win_layer != replaced_layer
		and _active_layer_count() == 1
		and reentry_direct_ok and replacement_direct_ok
		and _game_node_ids() == game_nodes_baseline
		and main.touch_control_blocks.has("dolls_game"))
	await process_frame
	_check("rapidly replaced layer is freed on the next frame",
		replaced_layer_ref.get_ref() == null)
	_check_entry_contract(win_layer, win_surface, _active_world_backdrop(),
		_active_backing(), _active_catcher(), replacement_direct_ok,
		game_nodes_baseline)

	var miss_guard := 0
	while win_surface != null and win_surface.missed < 2 and miss_guard < 420:
		miss_guard += 1
		await process_frame
	var first_win_layer_ref: WeakRef = weakref(win_layer)
	var first_win_surface_ref: WeakRef = weakref(win_surface)
	var first_run: Dictionary = await _drive_to_win(win_surface)
	await _frames(2)
	var first_missed: int = int(first_run.get("missed", -1))
	var first_tier: int = main._medal_ref().evaluate(
		"dolls", {"missed": first_missed})
	var first_save: Dictionary = _read_save()
	_check("real press, drag, and release completes the three-doll verb",
		bool(first_run.get("pressed", false))
		and bool(first_run.get("dragged", false))
		and bool(first_run.get("released", false))
		and bool(first_run.get("routed_exact", false))
		and bool(first_run.get("catcher_moved", false))
		and bool(first_run.get("world_stick_untouched", false))
		and bool(first_run.get("control_block_sole", false))
		and int(first_run.get("caught", 0)) == 3
		and bool(first_run.get("catch_feedback", false)))
	_check("missed count flows into the exact saved medal tier",
		first_missed >= 2 and first_tier > 0
		and int(main.medals.get("dolls", 0)) == first_tier
		and int((first_save.get("medals", {}) as Dictionary).get(
			"dolls", 0)) == first_tier)
	_check("first win awards exactly one trophy and persists Faron",
		bool(friend.get("won", false))
		and main.trophies == int(progress_baseline["trophies"]) + 1
		and bool((first_save.get("won", {}) as Dictionary).get("Faron", false)))
	_check("win removes Dolls and restores controls without game-node mutation",
		main.game == "" and _active_layer_count() == 0
		and _game_node_ids() == game_nodes_baseline
		and not main.touch_control_blocks.has("dolls_game")
		and main.touch_ui.world_controls_enabled)
	_check("win teardown frees its layer and surface",
		first_win_layer_ref.get_ref() == null
		and first_win_surface_ref.get_ref() == null)

	# Let bounded global reward layers finish, then replay cleanly. A better run
	# upgrades the medal but the already-won friend can never mint a trophy twice.
	await _frames(90)
	var replay_direct_baseline: Dictionary = _direct_child_ids()
	var trophy_before_replay: int = main.trophies
	main._start_game(friend)
	var replay_entry_layer := _active_layer()
	var replay_direct_ok := _only_layer_added(
		replay_direct_baseline, replay_entry_layer)
	await _frames(12)
	var replay_layer := _active_layer()
	var replay_surface := _active_surface()
	_check("post-win re-entry starts one fresh zeroed surface",
		replay_layer != null and replay_surface != null
		and _active_layer_count() == 1
		and replay_direct_ok
		and replay_surface.caught == 0 and replay_surface.missed == 0
		and replay_surface.fallers.size() <= 1
		and _subtree_node_count(replay_layer) <= MAX_STAGE_NODES
		and _game_node_ids() == game_nodes_baseline)
	var replay_layer_ref: WeakRef = weakref(replay_layer)
	var replay_surface_ref: WeakRef = weakref(replay_surface)
	var replay_run: Dictionary = await _drive_to_win(replay_surface)
	await _frames(2)
	var replay_save: Dictionary = _read_save()
	_check("fresh one-finger replay catches three with no miss",
		int(replay_run.get("caught", 0)) == 3
		and int(replay_run.get("missed", -1)) == 0
		and bool(replay_run.get("pressed", false))
		and bool(replay_run.get("dragged", false))
		and bool(replay_run.get("released", false))
		and bool(replay_run.get("routed_exact", false))
		and bool(replay_run.get("catcher_moved", false))
		and bool(replay_run.get("world_stick_untouched", false))
		and bool(replay_run.get("control_block_sole", false)))
	_check("better replay upgrades to gold without duplicating the trophy",
		int(main.medals.get("dolls", 0)) == MedalSystem.GOLD
		and main.trophies == trophy_before_replay
		and int((replay_save.get("medals", {}) as Dictionary).get(
			"dolls", 0)) == MedalSystem.GOLD
		and bool((replay_save.get("won", {}) as Dictionary).get("Faron", false)))
	_check("replay teardown is clean and leaves no duplicate Dolls layer",
		main.game == "" and _active_layer_count() == 0
		and replay_layer_ref.get_ref() == null
		and replay_surface_ref.get_ref() == null
		and _game_node_ids() == game_nodes_baseline
		and not main.touch_control_blocks.has("dolls_game")
		and main.touch_ui.world_controls_enabled)
	_finish()


func _check_entry_contract(
		layer: CanvasLayer, surface: OperaNurseryCatch,
		world: OperaWorldBackdrop2D, backing: ColorRect,
		catcher: TextureRect, direct_add_ok: bool,
		game_nodes_baseline: Array[int]) -> void:
	_check("entry adds exactly one direct Dolls Canvas child",
		layer != null and _active_layer_count() == 1 and direct_add_ok)
	if layer == null or surface == null or world == null \
			or backing == null or catcher == null:
		_check("entry constructs the complete Canvas subtree", false)
		return
	_check("stage is exactly five nodes with no per-baby scene children",
		_subtree_node_count(layer) == MAX_STAGE_NODES
		and layer.get_child_count() == 3
		and surface.get_child_count() == 1)
	_check("Dolls sits above hidden HUD and below speech and pause",
		layer.layer == 7 and main.hud_layer.layer < layer.layer
		and main.speech_layer != null and main.speech_layer.layer == 8
		and main.pause_layer.layer == 12
		and main.speech_layer.layer > layer.layer
		and main.pause_layer.layer > layer.layer)
	_check("approved 2x2 nursery world tiles are the only backdrop art",
		_texture_paths(world.world_tiles) == EXPECTED_WORLD_TILES
		and world.career_id == "nursery"
		and world.world_tiles.size() == 4)
	var placeholders_absent := surface.backdrop_texture == null \
		and surface.cradle_texture == null and surface.pillows_texture == null \
		and not bool(surface.get_meta("placeholder_widgets_loaded", true))
	for placeholder_path: String in PLACEHOLDER_WIDGETS:
		placeholders_absent = placeholders_absent \
			and not ResourceLoader.has_cached(placeholder_path)
	_check("known P3 widget placeholders are neither loaded nor displayed",
		placeholders_absent)
	_check("all three approved baby cutouts are active",
		_texture_paths(surface.textures) == EXPECTED_BABIES)
	_check("goal, no-fail and two-second live-input gate are unchanged",
		surface.goal == 3 and surface.active
		and bool(surface.get_meta("no_fail", false))
		and is_equal_approx(float(surface.get_meta(
			"live_input_gate_seconds", 0.0)), 2.0))
	_check("picture-first pointer remains while the exact goal clip is missing",
		bool(surface.get_meta("visual_pointer", false))
		and String(surface.get_meta("objective_recording_gap", ""))
			== "faron_catch_three")
	var styled_surface := surface as DollsGame.DollsNurserySurface
	var focus_at_zero := styled_surface.focus_rect_at(0.0)
	var focus_at_motion := styled_surface.focus_rect_at(0.35)
	var skin_rect := Rect2(catcher.position, catcher.size)
	var bowl_rect := styled_surface.bowl_rect()
	var targets_clear := true
	for entry: Dictionary in surface.fallers:
		var target_rect := styled_surface.faller_rect(entry)
		targets_clear = targets_clear \
			and not focus_at_zero.intersects(target_rect) \
			and not bowl_rect.intersects(target_rect)
	_check("cradle focus visibly bobs and pulses without a tween or node",
		focus_at_zero != focus_at_motion
		and focus_at_zero.size.x > bowl_rect.size.x
		and focus_at_zero.size.y > 0.0)
	_check("focus and bowl leave Roshan and the falling target unobscured",
		not focus_at_zero.intersects(skin_rect)
		and not bowl_rect.intersects(skin_rect)
		and targets_clear)
	var viewport_size: Vector2 = main.get_viewport().get_visible_rect().size
	var stage_rect := Rect2(surface.position, surface.size * surface.scale)
	var viewport_rect := Rect2(Vector2.ZERO, viewport_size)
	_check("native nursery panel stays centered, bounded and never upscaled",
		surface.size == PANEL_SIZE
		and surface.scale.x <= 1.0 and surface.scale.y <= 1.0
		and surface.scale.x > 0.0
		and viewport_rect.encloses(stage_rect)
		and stage_rect.get_center().is_equal_approx(viewport_rect.get_center())
		and world.position.is_equal_approx(surface.position)
		and world.scale.is_equal_approx(surface.scale))
	_check("opaque backing covers the viewport behind the authored panel",
		backing.color.a >= 0.999
		and backing.position.is_zero_approx()
		and backing.size.is_equal_approx(viewport_size))
	var skin_path: String = main.skin_sprite_path()
	_check("selected skin follows the catcher behind every gameplay draw",
		catcher.get_parent() == surface and catcher.show_behind_parent
		and catcher.mouse_filter == Control.MOUSE_FILTER_IGNORE
		and catcher.texture != null
		and catcher.texture.resource_path == skin_path
		and is_equal_approx(
			catcher.position.x + catcher.size.x * 0.5,
			surface.catcher_x * PANEL_SIZE.x)
		and catcher.position.x >= 0.0
		and catcher.position.x + catcher.size.x <= PANEL_SIZE.x)
	_check("entry neither mutates game_nodes nor constructs a hidden arena",
		_game_node_ids() == game_nodes_baseline
		and main.we_node.environment == main.return_env
		and main.player.position.is_equal_approx(main.return_pos)
		and main.kart_game == null)
	_check("Dolls exclusively owns and blocks world controls while active",
		main.touch_control_blocks.has("dolls_game")
		and not main.touch_ui.world_controls_enabled)


func _force_center_faller(surface: OperaNurseryCatch) -> bool:
	if surface == null or surface.fallers.is_empty():
		return false
	var entry: Dictionary = surface.fallers[0]
	entry["base_x"] = 0.5
	entry["x"] = 0.5
	entry["sway"] = 0.0
	surface.fallers[0] = entry
	return is_equal_approx(float(entry.get("x", -1.0)), 0.5) \
		and surface.input_live_t <= 0.0


func _center_safe_geometry_ok(surface: OperaNurseryCatch,
		catcher: TextureRect) -> bool:
	if surface == null or catcher == null \
			or surface.safe_landings.is_empty():
		return false
	var styled_surface := surface as DollsGame.DollsNurserySurface
	if styled_surface == null:
		return false
	var landing: Dictionary = surface.safe_landings[0]
	var safe_rect := styled_surface.safe_landing_rect(landing)
	var panel_rect := Rect2(Vector2.ZERO, surface.size)
	var skin_rect := Rect2(catcher.position, catcher.size)
	var clear := is_equal_approx(float(landing.get("x", -1.0)), 0.5) \
		and panel_rect.encloses(safe_rect) \
		and styled_surface.safe_mat_rect().encloses(safe_rect) \
		and not safe_rect.intersects(styled_surface.bowl_rect()) \
		and not safe_rect.intersects(styled_surface.focus_envelope_rect()) \
		and not safe_rect.intersects(skin_rect)
	for entry: Dictionary in surface.fallers:
		clear = clear \
			and not safe_rect.intersects(styled_surface.faller_rect(entry))
	return clear


func _drive_to_win(surface: OperaNurseryCatch) -> Dictionary:
	var world_stick_baseline: Vector2 = main.touch_ui.stick_vec
	var result: Dictionary = {
		"pressed": false,
		"dragged": false,
		"released": false,
		"routed_exact": true,
		"catcher_moved": false,
		"world_stick_untouched": true,
		"control_block_sole": true,
		"catch_feedback": false,
		"caught": surface.caught,
		"missed": surface.missed,
	}
	var guard := 0
	var last_caught: int = surface.caught
	var finger_down := false
	while main.game == "dolls" and guard < 720:
		guard += 1
		if not is_instance_valid(surface):
			break
		var target_x: float = surface.lowest_baby_x()
		if target_x < 0.0:
			target_x = 0.5
		var local_point := _surface_local_point(surface, target_x)
		var before_x: float = surface.catcher_x
		var expected_x := clampf(target_x, 0.1, 0.9)
		var routed_ok := false
		if not finger_down:
			routed_ok = _press(surface, local_point)
			finger_down = true
			result["pressed"] = true
		else:
			routed_ok = _drag(surface, local_point)
			result["dragged"] = true
		result["routed_exact"] = bool(result["routed_exact"]) \
			and routed_ok and is_equal_approx(surface.catcher_x, expected_x)
		result["catcher_moved"] = bool(result["catcher_moved"]) \
			or (not is_equal_approx(before_x, expected_x)
			and is_equal_approx(surface.catcher_x, expected_x))
		result["world_stick_untouched"] = \
			bool(result["world_stick_untouched"]) \
			and main.touch_ui.stick_vec.is_equal_approx(world_stick_baseline)
		result["control_block_sole"] = bool(result["control_block_sole"]) \
			and main.touch_control_blocks.size() == 1 \
			and main.touch_control_blocks.has("dolls_game") \
			and not main.touch_ui.world_controls_enabled
		await process_frame
		if is_instance_valid(surface):
			result["caught"] = surface.caught
			result["missed"] = surface.missed
			if surface.caught > last_caught:
				last_caught = surface.caught
				result["catch_feedback"] = result["catch_feedback"] \
					or (main.voice != null
					and float(main.voice.pitch_scale) >= 1.0
					and float(main.voice.pitch_scale) <= 1.25)
			if surface.caught >= surface.goal:
				result["released"] = _release(surface, finger_pos)
				finger_down = false
				break
	if finger_down and is_instance_valid(surface):
		result["released"] = _release(surface, finger_pos)
	await process_frame
	return result


func _surface_local_point(surface: OperaNurseryCatch,
		normalized_x: float) -> Vector2:
	return Vector2(clampf(normalized_x, 0.1, 0.9) * surface.size.x,
		surface.size.y * 0.72)


func _press(surface: OperaNurseryCatch, position: Vector2) -> bool:
	finger_pos = position
	var expected_x := clampf(position.x / maxf(1.0, surface.size.x), 0.1, 0.9)
	var event := InputEventScreenTouch.new()
	event.index = TOUCH_INDEX
	event.position = surface.get_screen_transform() * position
	event.pressed = true
	surface.get_viewport().push_input(event, true)
	return is_equal_approx(surface.catcher_x, expected_x)


func _drag(surface: OperaNurseryCatch, position: Vector2) -> bool:
	var prior_screen: Vector2 = surface.get_screen_transform() * finger_pos
	var screen_position: Vector2 = surface.get_screen_transform() * position
	var expected_x := clampf(position.x / maxf(1.0, surface.size.x), 0.1, 0.9)
	var event := InputEventScreenDrag.new()
	event.index = TOUCH_INDEX
	event.position = screen_position
	event.relative = screen_position - prior_screen
	finger_pos = position
	surface.get_viewport().push_input(event, true)
	return is_equal_approx(surface.catcher_x, expected_x)


func _release(surface: OperaNurseryCatch, position: Vector2) -> bool:
	if not is_instance_valid(surface):
		return false
	var catcher_before: float = surface.catcher_x
	var event := InputEventScreenTouch.new()
	event.index = TOUCH_INDEX
	event.position = surface.get_screen_transform() * position
	event.pressed = false
	surface.get_viewport().push_input(event, true)
	return is_equal_approx(surface.catcher_x, catcher_before)


func _dolls_friend() -> Dictionary:
	for friend: Dictionary in main.friends:
		if String(friend.get("game", "")) == "dolls":
			return friend
	return {}


func _active_layer() -> CanvasLayer:
	return main.get_node_or_null("DollsCatchLayer") as CanvasLayer


func _active_surface() -> OperaNurseryCatch:
	var layer := _active_layer()
	return layer.get_node_or_null("DollsCatchSurface") as OperaNurseryCatch \
		if layer != null else null


func _active_world_backdrop() -> OperaWorldBackdrop2D:
	var layer := _active_layer()
	return layer.get_node_or_null(
		"DollsApprovedNurseryBackdrop") as OperaWorldBackdrop2D \
		if layer != null else null


func _active_backing() -> ColorRect:
	var layer := _active_layer()
	return layer.get_node_or_null("DollsCanvasBacking") as ColorRect \
		if layer != null else null


func _active_catcher() -> TextureRect:
	var surface := _active_surface()
	return surface.get_node_or_null(
		"DollsSelectedSkinCatcher") as TextureRect \
		if surface != null else null


func _active_layer_count() -> int:
	var total := 0
	for child_value: Variant in main.get_children():
		var child := child_value as Node
		if child != null and child.name == &"DollsCatchLayer":
			total += 1
	return total


func _direct_child_ids() -> Dictionary:
	var ids: Dictionary = {}
	for child_value: Variant in main.get_children():
		var child := child_value as Node
		if child != null:
			ids[child.get_instance_id()] = true
	return ids


func _only_layer_added(baseline: Dictionary, layer: CanvasLayer) -> bool:
	if layer == null or not is_instance_valid(layer) \
			or baseline.has(layer.get_instance_id()):
		return false
	var current: Dictionary = _direct_child_ids()
	if current.size() != baseline.size() + 1 \
			or not current.has(layer.get_instance_id()):
		return false
	for instance_id: Variant in baseline:
		if not current.has(instance_id):
			return false
	return true


func _game_node_ids() -> Array[int]:
	var ids: Array[int] = []
	for node_value: Variant in main.game_nodes:
		var node := node_value as Node
		if node != null and is_instance_valid(node):
			ids.append(node.get_instance_id())
	return ids


func _subtree_node_count(node: Node) -> int:
	var total := 1
	for child_value: Variant in node.get_children():
		var child := child_value as Node
		if child != null:
			total += _subtree_node_count(child)
	return total


func _texture_paths(textures: Array[Texture2D]) -> Array[String]:
	var paths: Array[String] = []
	for texture: Texture2D in textures:
		paths.append(texture.resource_path if texture != null else "")
	return paths


func _voice_pool_has(path: String) -> bool:
	for player_value: Variant in main.voice_pool:
		var audio := player_value as AudioStreamPlayer
		if audio != null and audio.stream != null \
				and audio.stream.resource_path == path:
			return true
	return false


func _progress_snapshot(friend: Dictionary) -> Dictionary:
	return {
		"won": bool(friend.get("won", false)),
		"trophies": main.trophies,
		"medals": (main.medals as Dictionary).duplicate(true),
	}


func _read_save() -> Dictionary:
	var file := FileAccess.open("user://reef_save.json", FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed as Dictionary if parsed is Dictionary else {}


func _capture_requested(label: String) -> void:
	var capture_dir := OS.get_environment("DOLLS_CAPTURE_DIR")
	if capture_dir.is_empty():
		return
	await process_frame
	await process_frame
	var image: Image = main.get_viewport().get_texture().get_image()
	if image.get_size() != Vector2i(1280, 720):
		image.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
	DirAccess.make_dir_recursive_absolute(capture_dir)
	var capture_path := capture_dir.path_join("dolls_%s_1280x720.png" % label)
	var save_error: Error = image.save_png(capture_path)
	_check("%s Mobile-renderer capture saved at 1280x720" % label,
		save_error == OK and image.get_size() == Vector2i(1280, 720))
	if save_error == OK:
		print("DOLLS|CAPTURE|", capture_path)


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _check(label: String, condition: bool) -> void:
	if condition:
		print("DOLLS|OK|", label)
	else:
		bad += 1
		print("DOLLS|FAIL|", label)


func _finish() -> void:
	if bad == 0:
		print("DOLLS|result: ALL OK")
		quit()
	else:
		print("DOLLS|result: %d FAIL" % bad)
		quit(1)
