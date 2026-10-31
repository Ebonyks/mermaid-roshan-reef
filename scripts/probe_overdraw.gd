extends SceneTree
## Overdraw meter for the gold-star C7 overdraw checks (numbers only: this probe
## never renders, captures or writes an image). It walks the live Canvas at
## named game states, counts drawn layers per 10 px cell from each texture's
## real alpha, and prints one OVERDRAW|STATE line per state for
## tools/measure_overdraw.py. Run one group per process:
##   godot --headless -s scripts/probe_overdraw.gd -- --group=pool
##   godot --headless -s scripts/probe_overdraw.gd -- --group=opera

const CELL := 10.0
const COLS := 128
const ROWS := 72
const CANVAS := Vector2(1280.0, 720.0)
const ALPHA_VISIBLE := 0.1
const ALPHA_OPAQUE := 0.98
const SHAPE_CALLS: Array[String] = [
	"draw_rect(", "draw_circle(", "draw_arc(", "draw_line(", "draw_polyline(",
	"draw_polygon(", "draw_colored_polygon(", "draw_multiline(", "draw_string(",
	"draw_style_box(",
]
const EFFECT_SAMPLES: Array[float] = [0.1, 0.3, 0.6, 1.0, 1.5, 2.0]

var group: String = "pool"
var only: PackedStringArray = PackedStringArray()
var states_written: int = 0
var errors: int = 0
var _images: Dictionary = {}
var _script_info: Dictionary = {}
var _preorder: int = 0
# Self-test only: spawns a layer after the counter material is applied.
var _selftest_spawn: Callable = Callable()


func _init() -> void:
	for argument: String in OS.get_cmdline_user_args():
		if argument.begins_with("--group="):
			group = argument.trim_prefix("--group=")
		elif argument.begins_with("--only="):
			only = argument.trim_prefix("--only=").split(",", false)
	call_deferred("_run")


func _run() -> void:
	Engine.time_scale = 4.0
	if group == "pool":
		await _measure_pool()
	elif group == "opera":
		await _measure_opera()
	elif group == "selftest":
		await _selftest()
	else:
		_error("unknown group %s" % group)
	print("OVERDRAW|DONE|", JSON.stringify({"group": group, "states": states_written,
		"errors": errors}))
	quit(1 if errors > 0 else 0)


# --- Boot -------------------------------------------------------------------

func _boot_main() -> ReefMain:
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await process_frame
	return main


func _frames(count: int) -> void:
	for _frame: int in range(count):
		await process_frame


func _wait(seconds: float) -> void:
	await create_timer(seconds).timeout


# --- Mermaid Pool in its real castle room -------------------------------------

func _measure_pool() -> void:
	var main: ReefMain = await _boot_main()
	var director: DayOneDirector = main._day_one_ref()
	director.restore_state({"day_one_active": true, "day_one_completed_rooms": []})
	# Main keeps processing, as in play: it advances the room's entry transition.
	director.bathroom_supply_hunt_step = 2
	director.bathroom_tools_authorized = true
	director.bathroom_cleanup_step = 2
	director.bathroom_toilet_cleaned = true
	if not director.complete_tutorial("bathroom"):
		_error("pool: the bathroom could not be completed to open the pool")
	main.pearl_count = main.PEARL_TOTAL
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(16)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("mermaid_pool", false)
	await _frames(6)
	rooms.start_day_one_pool_cleanup()
	await _frames(6)
	var cleanup: DayOnePoolCleanup = rooms.day_one_pool_cleanup
	if cleanup == null:
		_error("pool: the cleanup did not start in the real room")
		return
	# The room's entry cross-fade briefly draws both compositions; it is reported
	# separately and is not a play state.
	await _wait(0.3)
	_emit("day_one_pool", "entry_transition", await _snapshot_with_gpu())
	# A first-arrival story clip plays between scenes; skip it through the same
	# route as its skip button so the measured states are the child's play.
	await _settle_story_clips(main)
	await _wait(1.5)
	_emit("day_one_pool", "start", await _snapshot_with_gpu())

	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	_touch(skimmer, skimmer._trash_contact_position(0), true)
	_touch(skimmer, skimmer._trash_contact_position(0), false)
	for _tick: int in range(240):
		await process_frame
		if skimmer._scoop_time > 0.05:
			break
	_emit("day_one_pool", "skimmer_contact", await _snapshot_with_gpu())
	var before_catch: Dictionary = _ids(_collect())
	var catch_bit: int = 1
	for _tick: int in range(240):
		if (int(main.day_one_pool_skimmer_mask) & catch_bit) != 0:
			break
		await process_frame
	_emit_effects("day_one_pool", "skimmer_catch", before_catch, await _effects(before_catch))
	for piece: int in range(1, PoolSkimmerActivity.TRASH_COUNT):
		_touch(skimmer, skimmer._trash_contact_position(piece), true)
		_touch(skimmer, skimmer._trash_contact_position(piece), false)
		for _tick: int in range(600):
			if (int(main.day_one_pool_skimmer_mask) & (1 << piece)) != 0:
				break
			await process_frame
	await _wait(0.9)
	_emit("day_one_pool", "waterfall_start", await _snapshot_with_gpu())

	var waterfall: PoolWaterfallActivity = cleanup.waterfall_activity
	var lane_width: float = waterfall.fixture_size.x / 3.0
	for lane: int in range(3):
		var x: float = waterfall._fixture_rect.position.x + lane_width * (float(lane) + 0.5)
		var top := Vector2(x, waterfall._fixture_rect.position.y + 8.0)
		var bottom := Vector2(x, waterfall._fixture_rect.end.y - 4.0)
		_touch(waterfall, top, true)
		_drag(waterfall, top.lerp(bottom, 0.5))
		if lane == 0:
			for _tick: int in range(120):
				await process_frame
			_emit("day_one_pool", "waterfall_stroke", await _snapshot_with_gpu())
		var before_lane: Dictionary = _ids(_collect())
		_drag(waterfall, bottom)
		_touch(waterfall, bottom, false)
		if lane == 0:
			_emit_effects("day_one_pool", "waterfall_lane_clear", before_lane,
				await _effects(before_lane))
		else:
			await _wait(0.4)
	await _wait(0.9)
	_emit("day_one_pool", "seahorse_start", await _snapshot_with_gpu())

	var seahorse: PoolSeahorseRescueActivity = cleanup.seahorse_activity
	var before_tug: Dictionary = _ids(_collect())
	_touch(seahorse, seahorse.fixture_center, true)
	_touch(seahorse, seahorse.fixture_center, false)
	for _tick: int in range(30):
		await process_frame
	_emit("day_one_pool", "seahorse_tug", await _snapshot_with_gpu())
	_emit_effects("day_one_pool", "seahorse_tug_effects", before_tug, await _effects(before_tug))
	for _tap: int in range(12):
		if seahorse._completion_started:
			break
		_touch(seahorse, seahorse.fixture_center, true)
		_touch(seahorse, seahorse.fixture_center, false)
		await _wait(0.6)
	# The clean-pool reveal is measured during its reward beat, at real speed: on
	# the probe's 4x clock the beat had already ended and the room-completion
	# story clip covered the screen, so "finale" had measured the clip. Rumi
	# rises once, in that clip (owner QP-1), so the room stages no Rumi here.
	Engine.time_scale = 1.0
	for _tick: int in range(600):
		if bool(cleanup.audit_snapshot().get("finale_started", false)):
			break
		await process_frame
	await _wait(0.6)
	_emit("day_one_pool", "finale", await _snapshot_with_gpu())
	# The room-completion clip plays between scenes over the room (DL-CIN-16). It
	# is recorded, not budgeted as a play state (gold_star.json states_not_budgeted).
	for _tick: int in range(600):
		if main._day_one_story_clip != null and is_instance_valid(main._day_one_story_clip):
			break
		await process_frame
	if main._day_one_story_clip != null and is_instance_valid(main._day_one_story_clip):
		await _wait(0.3)
		_emit("day_one_pool", "story_clip", await _snapshot_with_gpu())
	Engine.time_scale = 4.0


func _settle_story_clips(main: ReefMain) -> void:
	for _attempt: int in range(20):
		await _frames(4)
		var clip: DayOneStoryClips = main._day_one_story_clip
		if clip == null or not is_instance_valid(clip):
			return
		clip.skip()


func _touch(target: Control, position: Vector2, pressed: bool) -> void:
	var touch := InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = pressed
	touch.position = position
	target._gui_input(touch)


func _drag(target: Control, position: Vector2) -> void:
	var drag := InputEventScreenDrag.new()
	drag.index = 0
	drag.position = position
	target._gui_input(drag)


# --- Opera careers in free play ------------------------------------------------

func _measure_opera() -> void:
	# Free play after Day One: each career opens from its owner Castle room through
	# the real route, so the castle is suspended exactly as it is for the child.
	var main: ReefMain = await _boot_main()
	main._day_one_ref().restore_state({"day_one_active": false})
	main.pearl_count = main.PEARL_TOTAL
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(16)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	print("OVERDRAW|INFO|", JSON.stringify({"chapter2_active": main.chapter2_is_active(),
		"day_one_active": main.day_one_is_active(), "castle_open": rooms.is_open()}))
	for act_index: int in range(OperaHouse.ACTS.size()):
		if not OperaHouse.is_live_act_index(act_index):
			continue
		var career: String = String((OperaHouse.ACTS[act_index] as Dictionary).get("costume", ""))
		if not only.is_empty() and not only.has(career):
			continue
		var room: String = CastleCareerRoutes.room_for_act(act_index)
		rooms.show_room(room, false)
		await _wait(0.8)
		if main.castle_room_id != room:
			_error("opera: %s owner room %s did not open" % [career, room])
			continue
		main._start_opera_from_room(act_index, room)
		var world: OperaCareerWorld2D = null
		for _tick: int in range(600):
			await process_frame
			if main.opera_game != null and main.opera_game.act != null 					and main.opera_game.act.career_world_2d != null:
				world = main.opera_game.act.career_world_2d
				break
		if world == null:
			_error("opera: %s did not launch from %s" % [career, room])
			continue
		await _wait(0.8)
		_emit(career, "world", await _snapshot_with_gpu())
		var armed: Array[OperaWorldHotspot2D] = []
		for node: Control in world.station_nodes:
			var hotspot := node as OperaWorldHotspot2D
			if hotspot != null and hotspot.armed:
				armed.append(hotspot)
		if armed.size() == 1 and armed[0].touch_button != null:
			armed[0].touch_button.pressed.emit()
			for _tick: int in range(1200):
				if world.task_open and not world.wander_walking:
					break
				await process_frame
		if world.task_open:
			await _wait(0.4)
			_emit(career, "task_open", await _snapshot_with_gpu())
			var before_phase: Dictionary = _ids(_collect())
			world._on_gesture("probe", 100.0, 1.0)
			_emit_effects(career, "phase_done", before_phase, await _effects(before_phase))
			_emit(career, "after_phase", await _snapshot_with_gpu())
		else:
			_error("opera: %s task did not open from its armed hotspot" % career)
		if main.opera_game != null:
			main.opera_game._leave_early()
		for _tick: int in range(600):
			await process_frame
			if main.opera_game == null and rooms.is_open():
				break
		await _wait(0.6)


# --- Meter --------------------------------------------------------------------

func _collect() -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	_preorder = 0
	_walk(get_root(), 0, out)
	return out


func _walk(node: Node, layer: int, out: Array[Dictionary]) -> void:
	var current_layer: int = layer
	if node is CanvasLayer:
		var canvas_layer := node as CanvasLayer
		if not canvas_layer.visible:
			return
		current_layer = canvas_layer.layer
	elif node is Viewport and node != get_root():
		return
	if node is CanvasItem:
		var item := node as CanvasItem
		if not item.visible:
			return
		_preorder += 1
		for entry: Dictionary in _describe(item, current_layer):
			out.append(entry)
	for child: Node in node.get_children():
		_walk(child, current_layer, out)


func _describe(item: CanvasItem, layer: int) -> Array[Dictionary]:
	var entries: Array[Dictionary] = []
	var base: Dictionary = {
		"id": item.get_instance_id(),
		"name": String(item.name),
		"path": String(item.get_path()),
		"order": [layer, _absolute_z(item), _preorder],
		"alpha": _effective_alpha(item),
		"xf": item.get_global_transform_with_canvas(),
	}
	var info: Dictionary = _script(item)
	if not bool(info.get("custom_draw", false)):
		# A script-less layer can draw through a connected `draw` callback; judge
		# the connected method of its owner script, or code shapes stay invisible.
		info = _connected_draw(item, info)
	if item is Sprite2D:
		var sprite := item as Sprite2D
		if sprite.texture != null:
			var inner := Rect2(Vector2.ZERO, sprite.texture.get_size())
			if sprite.region_enabled:
				inner = sprite.region_rect
			if sprite.hframes > 1 or sprite.vframes > 1:
				var frame_size: Vector2 = inner.size / Vector2(float(sprite.hframes), float(sprite.vframes))
				inner = Rect2(inner.position + Vector2(sprite.frame_coords) * frame_size, frame_size)
			entries.append(_textured(base, sprite.texture, inner, sprite.get_rect(),
				sprite.flip_h, sprite.flip_v, "sprite"))
	elif item is AnimatedSprite2D:
		var animated := item as AnimatedSprite2D
		if animated.sprite_frames != null and animated.sprite_frames.has_animation(animated.animation):
			var frame_texture: Texture2D = animated.sprite_frames.get_frame_texture(
				animated.animation, animated.frame)
			if frame_texture != null:
				var size: Vector2 = frame_texture.get_size()
				var origin: Vector2 = animated.offset - (size * 0.5 if animated.centered else Vector2.ZERO)
				entries.append(_textured(base, frame_texture, Rect2(Vector2.ZERO, size),
					Rect2(origin, size), animated.flip_h, animated.flip_v, "sprite"))
	elif item is TextureRect:
		var texture_rect := item as TextureRect
		if texture_rect.texture != null:
			var entry: Dictionary = _textured(base, texture_rect.texture,
				Rect2(Vector2.ZERO, texture_rect.texture.get_size()),
				Rect2(Vector2.ZERO, texture_rect.size), texture_rect.flip_h,
				texture_rect.flip_v, "texture_rect")
			entry["stretch"] = texture_rect.stretch_mode
			entries.append(entry)
	elif item is NinePatchRect:
		var patch := item as NinePatchRect
		if patch.texture != null:
			var region: Rect2 = patch.region_rect
			if region.size == Vector2.ZERO:
				region = Rect2(Vector2.ZERO, patch.texture.get_size())
			entries.append(_textured(base, patch.texture, region,
				Rect2(Vector2.ZERO, patch.size), false, false, "nine_patch"))
	elif item is ColorRect:
		var color_rect := item as ColorRect
		var vector: Dictionary = base.duplicate()
		vector["kind"] = "vector"
		vector["alpha"] = float(base["alpha"]) * color_rect.color.a
		vector["local"] = Rect2(Vector2.ZERO, color_rect.size)
		entries.append(vector)
	elif item is Polygon2D:
		var polygon := item as Polygon2D
		if polygon.polygon.size() >= 3:
			var shape: Dictionary = base.duplicate()
			shape["kind"] = "vector"
			shape["alpha"] = float(base["alpha"]) * polygon.color.a
			var points := PackedVector2Array()
			for point: Vector2 in polygon.polygon:
				points.append(point + polygon.offset)
			shape["polygon"] = points
			shape["local"] = _bounds(points)
			entries.append(shape)
	elif item is Line2D:
		var line := item as Line2D
		if line.points.size() >= 2:
			var stroke: Dictionary = base.duplicate()
			stroke["kind"] = "vector"
			stroke["alpha"] = float(base["alpha"]) * line.default_color.a
			stroke["line"] = line.points
			stroke["width"] = line.width
			stroke["local"] = _bounds(line.points).grow(line.width * 0.5)
			entries.append(stroke)
	elif item is Panel or item is PanelContainer or item is Button:
		var control := item as Control
		var style_name: String = "normal" if item is Button else "panel"
		var style: StyleBox = control.get_theme_stylebox(style_name)
		if style is StyleBoxFlat and (style as StyleBoxFlat).bg_color.a > 0.01:
			var panel: Dictionary = base.duplicate()
			panel["kind"] = "vector"
			panel["alpha"] = float(base["alpha"]) * (style as StyleBoxFlat).bg_color.a
			panel["local"] = Rect2(Vector2.ZERO, control.size)
			entries.append(panel)
	elif item is Label or item is RichTextLabel:
		var text: Dictionary = base.duplicate()
		text["kind"] = "text"
		entries.append(text)
	elif item is CPUParticles2D or item is GPUParticles2D:
		var particles: Dictionary = base.duplicate()
		particles["kind"] = "particles"
		entries.append(particles)
	if bool(info.get("custom_draw", false)):
		var custom: Dictionary = base.duplicate()
		custom["kind"] = "custom"
		custom["shapes"] = bool(info.get("shapes", false))
		custom["script"] = String(info.get("path", ""))
		if item is Control:
			custom["local"] = Rect2(Vector2.ZERO, (item as Control).size)
		entries.append(custom)
	for entry: Dictionary in entries:
		_cover(entry)
	return entries


func _textured(base: Dictionary, texture: Texture2D, inner: Rect2, local: Rect2,
		flip_h: bool, flip_v: bool, kind: String) -> Dictionary:
	var entry: Dictionary = base.duplicate()
	var source_texture: Texture2D = texture
	var origin := Vector2.ZERO
	var guard: int = 0
	while source_texture is AtlasTexture and guard < 4:
		var atlas := source_texture as AtlasTexture
		origin += atlas.region.position
		source_texture = atlas.atlas
		guard += 1
	entry["kind"] = kind
	entry["image"] = source_texture.resource_path if source_texture != null else ""
	entry["src"] = Rect2(origin + inner.position, inner.size)
	entry["local"] = local
	entry["flip_h"] = flip_h
	entry["flip_v"] = flip_v
	entry["texture_size"] = texture.get_size()
	return entry


func _cover(entry: Dictionary) -> void:
	var cells := PackedInt32Array()
	var opaque := PackedInt32Array()
	var translucent: int = 0
	entry["cells"] = cells
	entry["opaque"] = opaque
	entry["translucent"] = 0
	if not entry.has("local"):
		return
	var local: Rect2 = entry["local"]
	if local.size.x <= 0.0 or local.size.y <= 0.0:
		return
	var xf: Transform2D = entry["xf"]
	var inverse: Transform2D = xf.affine_inverse()
	var corners: Array[Vector2] = [xf * local.position, xf * Vector2(local.end.x, local.position.y),
		xf * local.end, xf * Vector2(local.position.x, local.end.y)]
	var low := Vector2(INF, INF)
	var high := Vector2(-INF, -INF)
	for corner: Vector2 in corners:
		low = Vector2(minf(low.x, corner.x), minf(low.y, corner.y))
		high = Vector2(maxf(high.x, corner.x), maxf(high.y, corner.y))
	entry["screen"] = Rect2(low, high - low)
	var x0: int = clampi(int(floor(low.x / CELL)), 0, COLS)
	var x1: int = clampi(int(ceil(high.x / CELL)), 0, COLS)
	var y0: int = clampi(int(floor(low.y / CELL)), 0, ROWS)
	var y1: int = clampi(int(ceil(high.y / CELL)), 0, ROWS)
	var alpha: float = float(entry["alpha"])
	var image: Image = null
	if entry.has("image"):
		image = _image(String(entry["image"]))
	for row: int in range(y0, y1):
		for column: int in range(x0, x1):
			var point: Vector2 = inverse * Vector2((float(column) + 0.5) * CELL, (float(row) + 0.5) * CELL)
			if not local.has_point(point):
				continue
			var sample: float = _sample(entry, image, point)
			if sample * alpha < ALPHA_VISIBLE:
				continue
			cells.append(row * COLS + column)
			if sample * alpha < ALPHA_OPAQUE:
				translucent += 1
			elif String(entry.get("kind", "")) != "custom":
				opaque.append(row * COLS + column)
	entry["cells"] = cells
	entry["opaque"] = opaque
	entry["translucent"] = translucent


func _sample(entry: Dictionary, image: Image, point: Vector2) -> float:
	if entry.has("polygon"):
		return 1.0 if Geometry2D.is_point_in_polygon(point, entry["polygon"]) else 0.0
	if entry.has("line"):
		var line_points: PackedVector2Array = entry["line"]
		var half: float = float(entry["width"]) * 0.5
		for index: int in range(line_points.size() - 1):
			var closest: Vector2 = Geometry2D.get_closest_point_to_segment(point,
				line_points[index], line_points[index + 1])
			if closest.distance_to(point) <= half:
				return 1.0
		return 0.0
	if image == null:
		return 1.0
	var local: Rect2 = entry["local"]
	var uv: Vector2 = (point - local.position) / local.size
	if String(entry.get("kind", "")) == "texture_rect":
		uv = _stretch_uv(entry, point)
		if uv.x < 0.0:
			return 0.0
	if bool(entry.get("flip_h", false)):
		uv.x = 1.0 - uv.x
	if bool(entry.get("flip_v", false)):
		uv.y = 1.0 - uv.y
	var src: Rect2 = entry["src"]
	var pixel: Vector2 = src.position + uv * src.size
	var x: int = clampi(int(pixel.x), 0, image.get_width() - 1)
	var y: int = clampi(int(pixel.y), 0, image.get_height() - 1)
	return image.get_pixel(x, y).a


func _stretch_uv(entry: Dictionary, point: Vector2) -> Vector2:
	var local: Rect2 = entry["local"]
	var texture_size: Vector2 = entry["texture_size"]
	var mode: int = int(entry.get("stretch", TextureRect.STRETCH_SCALE))
	var draw := Rect2(Vector2.ZERO, local.size)
	if mode == TextureRect.STRETCH_TILE:
		return Vector2(fposmod(point.x, texture_size.x) / texture_size.x,
			fposmod(point.y, texture_size.y) / texture_size.y)
	if mode == TextureRect.STRETCH_KEEP:
		draw = Rect2(Vector2.ZERO, texture_size)
	elif mode == TextureRect.STRETCH_KEEP_CENTERED:
		draw = Rect2((local.size - texture_size) * 0.5, texture_size)
	elif mode in [TextureRect.STRETCH_KEEP_ASPECT, TextureRect.STRETCH_KEEP_ASPECT_CENTERED,
			TextureRect.STRETCH_KEEP_ASPECT_COVERED]:
		var scale_x: float = local.size.x / maxf(texture_size.x, 1.0)
		var scale_y: float = local.size.y / maxf(texture_size.y, 1.0)
		var scale_value: float = maxf(scale_x, scale_y) \
			if mode == TextureRect.STRETCH_KEEP_ASPECT_COVERED else minf(scale_x, scale_y)
		var size: Vector2 = texture_size * scale_value
		var position: Vector2 = Vector2.ZERO if mode == TextureRect.STRETCH_KEEP_ASPECT \
			else (local.size - size) * 0.5
		draw = Rect2(position, size)
	if not draw.has_point(point):
		return Vector2(-1.0, -1.0)
	return (point - draw.position) / draw.size


func _image(path: String) -> Image:
	if _images.has(path):
		return _images[path] as Image
	var image: Image = null
	if path != "" and not path.ends_with(".tres") and not path.ends_with(".res") \
			and FileAccess.file_exists(path):
		image = Image.load_from_file(path)
		if image != null and image.is_compressed():
			image.decompress()
	_images[path] = image
	return image


func _script(item: CanvasItem) -> Dictionary:
	var script: Script = item.get_script() as Script
	if script == null:
		return {}
	var key: String = script.resource_path
	if _script_info.has(key):
		return _script_info[key] as Dictionary
	var custom_draw: bool = false
	var shapes: bool = false
	var current: Script = script
	while current != null:
		var source: String = current.source_code
		if source.contains("func _draw("):
			custom_draw = true
			for call: String in SHAPE_CALLS:
				if source.contains(call):
					shapes = true
		current = current.get_base_script()
	var info: Dictionary = {"path": key, "custom_draw": custom_draw, "shapes": shapes}
	_script_info[key] = info
	return info


func _connected_draw(item: CanvasItem, info: Dictionary) -> Dictionary:
	for connection: Dictionary in item.get_signal_connection_list("draw"):
		var callable: Callable = connection.get("callable", Callable()) as Callable
		var owner: Object = callable.get_object()
		if owner == null:
			continue
		var script: Script = owner.get_script() as Script
		if script == null:
			continue
		var key: String = "%s::%s" % [script.resource_path, String(callable.get_method())]
		if not _script_info.has(key):
			var body: String = _method_body(script, String(callable.get_method()))
			var shapes: bool = false
			for call: String in SHAPE_CALLS:
				if body.contains(call):
					shapes = true
			_script_info[key] = {"path": script.resource_path, "custom_draw": true,
				"shapes": shapes, "connected_method": String(callable.get_method())}
		var found: Dictionary = _script_info[key] as Dictionary
		if bool(found.get("shapes", false)) or not bool(info.get("custom_draw", false)):
			info = found
	return info


func _method_body(script: Script, method: String) -> String:
	var current: Script = script
	while current != null:
		var source: String = current.source_code
		var start: int = source.find("func %s(" % method)
		if start >= 0:
			var finish: int = source.find("\nfunc ", start + 1)
			return source.substr(start, finish - start) if finish > start else source.substr(start)
		current = current.get_base_script()
	return ""


func _effective_alpha(item: CanvasItem) -> float:
	var alpha: float = item.self_modulate.a
	var node: Node = item
	while node != null and not (node is CanvasLayer):
		if node is CanvasItem:
			alpha *= (node as CanvasItem).modulate.a
		node = node.get_parent()
	return alpha


func _absolute_z(item: CanvasItem) -> int:
	var z: int = item.z_index
	var current: CanvasItem = item
	while current.z_as_relative:
		var parent: Node = current.get_parent()
		if not (parent is CanvasItem):
			break
		current = parent as CanvasItem
		z += current.z_index
	return z


func _bounds(points: PackedVector2Array) -> Rect2:
	var low := Vector2(INF, INF)
	var high := Vector2(-INF, -INF)
	for point: Vector2 in points:
		low = Vector2(minf(low.x, point.x), minf(low.y, point.y))
		high = Vector2(maxf(high.x, point.x), maxf(high.y, point.y))
	return Rect2(low, high - low)


func _is_roshan(entry: Dictionary) -> bool:
	var text: String = (String(entry.get("name", "")) + " " + String(entry.get("image", ""))).to_lower()
	return text.contains("roshan") and String(entry.get("kind", "")) in ["sprite", "texture_rect"]


func _order_less(a: Array, b: Array) -> bool:
	for index: int in range(3):
		if int(a[index]) != int(b[index]):
			return int(a[index]) < int(b[index])
	return false


func _ids(entries: Array[Dictionary]) -> Dictionary:
	var ids: Dictionary = {}
	for entry: Dictionary in entries:
		ids[int(entry["id"])] = true
	return ids


func _gpu_available() -> bool:
	return DisplayServer.get_name() != "headless"


func _counter_material(translucent_only: bool) -> ShaderMaterial:
	# Every fragment that a visible item really draws adds exactly 1/255 to red.
	# The minimum of the sampled texture alpha and the vertex/modulate alpha is
	# the drawn alpha whether or not the engine pre-multiplies the texture.
	var shader := Shader.new()
	var keep: String = "a < 0.1 || a >= 0.98" if translucent_only else "a < 0.1"
	shader.code = """shader_type canvas_item;
render_mode blend_add, unshaded;
void fragment() {
	float a = min(texture(TEXTURE, UV).a, COLOR.a);
	if (%s) {
		discard;
	}
	COLOR = vec4(1.0 / 255.0, 0.0, 0.0, 1.0);
}
""" % keep
	var material := ShaderMaterial.new()
	material.shader = shader
	return material


func _gpu_counts(translucent_only: bool) -> Dictionary:
	# Numbers only: the frame is read into memory, reduced to a histogram and
	# discarded. Nothing is saved, shown or printed as an image.
	if not _gpu_available():
		return {}
	var material: ShaderMaterial = _counter_material(translucent_only)
	var saved: Array[Dictionary] = []
	var stack: Array[Node] = [get_root()]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for child: Node in node.get_children():
			stack.append(child)
		if node is CanvasModulate:
			saved.append({"node": node, "modulate": true, "visible": (node as CanvasModulate).visible})
			(node as CanvasModulate).visible = false
		elif node is CanvasItem:
			var item := node as CanvasItem
			saved.append({"node": item, "material": item.material,
				"use_parent": item.use_parent_material})
			item.material = material
			item.use_parent_material = false
	# An effect spawned during the counted frames (a bubble, ring or star) would
	# otherwise draw in its real colours and read as up to 255 layers; it counts
	# exactly like everything else (proven by the self-test's late layer).
	var on_added := func(node: Node) -> void:
		if node is CanvasItem:
			var late := node as CanvasItem
			saved.append({"node": late, "material": late.material,
				"use_parent": late.use_parent_material})
			late.material = material
			late.use_parent_material = false
	node_added.connect(on_added)
	if _selftest_spawn.is_valid():
		_selftest_spawn.call()
		_selftest_spawn = Callable()
	var clear: Color = RenderingServer.get_default_clear_color()
	RenderingServer.set_default_clear_color(Color.BLACK)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	RenderingServer.set_default_clear_color(clear)
	node_added.disconnect(on_added)
	for record: Dictionary in saved:
		# Effects may free themselves during the two counted frames.
		var value: Variant = record["node"]
		if not is_instance_valid(value):
			continue
		var node: Node = value
		if record.has("modulate"):
			(node as CanvasModulate).visible = bool(record["visible"])
		else:
			var item := node as CanvasItem
			item.material = record["material"]
			item.use_parent_material = bool(record["use_parent"])
	if image == null or image.is_empty():
		return {"error": "no frame"}
	image.convert(Image.FORMAT_RGBA8)
	var data: PackedByteArray = image.get_data()
	var width: int = image.get_width()
	var height: int = image.get_height()
	# canvas_items/expand keeps the 1280x720 canvas at the frame's top-left at one
	# uniform scale, so sample a fixed canvas grid wherever the window landed.
	var scale_value: float = minf(float(width) / CANVAS.x, float(height) / CANVAS.y)
	var histogram: Dictionary = {}
	var samples: int = 0
	var total: int = 0
	for row_index: int in range(144):
		var y: int = mini(height - 1, int((float(row_index) + 0.5) * 5.0 * scale_value))
		for column_index: int in range(256):
			var x: int = mini(width - 1, int((float(column_index) + 0.5) * 5.0 * scale_value))
			var count: int = data[(y * width + x) * 4]
			histogram[count] = int(histogram.get(count, 0)) + 1
			samples += 1
			total += count
	var levels: Array = histogram.keys()
	levels.sort()
	var running: int = 0
	var p50: int = 0
	var p95: int = 0
	var share: Dictionary = {3: 0, 4: 0, 6: 0}
	for level: int in levels:
		var amount: int = int(histogram[level])
		if running < samples * 0.5 and running + amount >= samples * 0.5:
			p50 = level
		if running < samples * 0.95 and running + amount >= samples * 0.95:
			p95 = level
		running += amount
		for threshold: int in share.keys():
			if level >= threshold:
				share[threshold] = int(share[threshold]) + amount
	return {
		"frame": [width, height],
		"mean": snappedf(float(total) / maxf(float(samples), 1.0), 0.01),
		"p50": p50,
		"p95": p95,
		"max": int(levels[levels.size() - 1]) if not levels.is_empty() else 0,
		"share_ge3": snappedf(float(share[3]) / float(samples), 0.001),
		"share_ge4": snappedf(float(share[4]) / float(samples), 0.001),
		"share_ge6": snappedf(float(share[6]) / float(samples), 0.001),
	}


func _snapshot_with_gpu() -> Dictionary:
	# Three frames 0.15 s apart: the budget reads the median frame and the worst
	# frame is kept as the peak, so a brief burst is recorded without flaking.
	var metrics: Dictionary = _snapshot()
	if not _gpu_available():
		return metrics
	var frames: Array[Dictionary] = []
	var translucent_frames: Array[Dictionary] = []
	for sample: int in range(3):
		if sample > 0:
			await _wait(0.15)
		frames.append(await _gpu_counts(false))
		translucent_frames.append(await _gpu_counts(true))
	metrics["gpu_layers"] = _median_frame(frames)
	metrics["gpu_translucent_layers"] = _median_frame(translucent_frames)
	var peak: int = 0
	for frame: Dictionary in frames:
		peak = maxi(peak, int(frame.get("max", 0)))
	metrics["gpu_peak_layers"] = peak
	return metrics


func _median_frame(frames: Array[Dictionary]) -> Dictionary:
	var ordered: Array[Dictionary] = frames.duplicate()
	ordered.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return float(a.get("mean", 0.0)) < float(b.get("mean", 0.0)))
	return ordered[int(float(ordered.size()) / 2.0)]


func _selftest() -> void:
	# Five opaque full-screen layers, one half-transparent full-screen layer and a
	# texture with transparent margins: the counts must come back exactly.
	var layer := CanvasLayer.new()
	get_root().add_child(layer)
	for index: int in range(5):
		var rect := ColorRect.new()
		rect.color = Color(0.2 * float(index), 0.5, 0.5, 1.0)
		rect.size = CANVAS
		layer.add_child(rect)
	var wash := ColorRect.new()
	wash.color = Color(0.2, 0.1, 0.3, 0.5)
	wash.size = CANVAS
	layer.add_child(wash)
	var hidden := ColorRect.new()
	hidden.color = Color(1.0, 1.0, 1.0, 1.0)
	hidden.size = CANVAS
	hidden.visible = false
	layer.add_child(hidden)
	await _frames(3)
	var metrics: Dictionary = await _snapshot_with_gpu()
	_emit("selftest", "six_layers", metrics)
	var gpu: Dictionary = metrics.get("gpu_layers", {}) as Dictionary
	var translucent: Dictionary = metrics.get("gpu_translucent_layers", {}) as Dictionary
	if not _gpu_available():
		_error("selftest needs a rendering window; run without --headless")
	elif int(gpu.get("p50", -1)) != 6 or int(gpu.get("max", -1)) != 6 			or int(translucent.get("max", -1)) != 1:
		_error("selftest: expected 6 layers and 1 translucent, got %s / %s" % [gpu, translucent])
	if int((metrics["depth"] as Dictionary).get("p50", -1)) != 6:
		_error("selftest: node meter expected 6 layers, got %s" % metrics["depth"])
	# A white opaque layer added while the frame is being counted is one more
	# layer, never its own colour (an unswapped white layer reads as 255).
	var late := ColorRect.new()
	late.name = "SelftestLateLayer"
	late.color = Color.WHITE
	late.size = CANVAS
	_selftest_spawn = func() -> void: layer.add_child(late)
	var late_metrics: Dictionary = await _snapshot_with_gpu()
	_emit("selftest", "late_layer", late_metrics)
	var late_gpu: Dictionary = late_metrics.get("gpu_layers", {}) as Dictionary
	var late_translucent: Dictionary = late_metrics.get("gpu_translucent_layers", {}) as Dictionary
	if _gpu_available() and (int(late_gpu.get("p50", -1)) != 7 or int(late_gpu.get("max", -1)) != 7 \
			or int(late_metrics.get("gpu_peak_layers", -1)) != 7 or int(late_translucent.get("max", -1)) != 1):
		_error("selftest: a layer added while counting must count once, got %s / %s" % [
			late_gpu, late_translucent])
	# A script-less layer drawing through a connected callback is code drawing.
	var connected := Control.new()
	connected.name = "SelftestConnectedDraw"
	connected.size = Vector2(40.0, 40.0)
	connected.draw.connect(_selftest_connected_draw.bind(connected))
	layer.add_child(connected)
	var connected_info: Dictionary = _connected_draw(connected, {})
	if not bool(connected_info.get("custom_draw", false)) or not bool(connected_info.get("shapes", false)) \
			or String(connected_info.get("connected_method", "")) != "_selftest_connected_draw":
		_error("selftest: a connected draw callback was not seen as code drawing: %s" % connected_info)
	layer.queue_free()
	await _frames(2)


func _selftest_connected_draw(target: Control) -> void:
	target.draw_rect(Rect2(Vector2.ZERO, target.size), Color(1.0, 1.0, 1.0, 0.5))


func _snapshot() -> Dictionary:
	var entries: Array[Dictionary] = _collect()
	var total: int = COLS * ROWS
	var depth := PackedInt32Array()
	depth.resize(total)
	var depth_upper := PackedInt32Array()
	depth_upper.resize(total)
	var top_opaque: Dictionary = {}
	for entry: Dictionary in entries:
		for cell: int in entry.get("opaque", PackedInt32Array()):
			if not top_opaque.has(cell) or _order_less(top_opaque[cell], entry["order"]):
				top_opaque[cell] = entry["order"]
	var layer_cells: int = 0
	var hidden_cells: int = 0
	var listing: Array = []
	var custom_cells: Dictionary = {}
	var kinds: Dictionary = {}
	var full_width_alpha: Array = []
	var overlays: Array = []
	var custom_items: Array = []
	var focal: Dictionary = {}
	var focal_order: Array = [-1000000, -1000000, -1]
	for entry: Dictionary in entries:
		var kind: String = String(entry.get("kind", ""))
		kinds[kind] = int(kinds.get(kind, 0)) + 1
		var cells: PackedInt32Array = entry["cells"]
		var hidden: int = 0
		for cell: int in cells:
			depth_upper[cell] += 1
			layer_cells += 1
			if top_opaque.has(cell) and _order_less(entry["order"], top_opaque[cell]):
				hidden += 1
		hidden_cells += hidden
		if cells.size() > 0 or kind in ["custom", "particles"]:
			listing.append({"name": entry["name"], "kind": kind,
				"image": String(entry.get("image", "")).get_file(),
				"script": String(entry.get("script", "")).get_file(),
				"order": entry["order"], "cells": cells.size(),
				"opaque": (entry.get("opaque", PackedInt32Array()) as PackedInt32Array).size(),
				"translucent": entry["translucent"], "hidden": hidden,
				"alpha": snappedf(float(entry["alpha"]), 0.01)})
		if kind == "custom":
			for cell: int in cells:
				custom_cells[cell] = true
			custom_items.append({"name": entry["name"], "script": entry.get("script", ""),
				"shapes": entry.get("shapes", false), "cells": cells.size(),
				"area_known": entry.has("local")})
			continue
		for cell: int in cells:
			depth[cell] += 1
		var screen: Rect2 = entry.get("screen", Rect2())
		var translucent_share: float = float(entry["translucent"]) / maxf(float(cells.size()), 1.0)
		if screen.size.x >= CANVAS.x * 0.9 and cells.size() > 0 \
				and (translucent_share >= 0.05 or float(entry["alpha"]) < ALPHA_OPAQUE):
			full_width_alpha.append({"name": entry["name"], "image": entry.get("image", ""),
				"translucent_share": snappedf(translucent_share, 0.01)})
		if float(cells.size()) >= float(total) * 0.5 \
				and (translucent_share >= 0.5 or (kind == "vector" and float(entry["alpha"]) < ALPHA_OPAQUE)):
			overlays.append({"name": entry["name"], "kind": kind, "image": entry.get("image", ""),
				"screen_share": snappedf(float(cells.size()) / float(total), 0.01),
				"translucent_share": snappedf(translucent_share, 0.01), "order": entry["order"]})
		if _is_roshan(entry):
			for cell: int in cells:
				focal[cell] = true
			if _order_less(focal_order, entry["order"]):
				focal_order = entry["order"]
	var duplicates: Array = _duplicates(entries)
	var covered: Dictionary = {}
	var coverers: Dictionary = {}
	if not focal.is_empty():
		for entry: Dictionary in entries:
			if String(entry.get("kind", "")) in ["custom", "text", "particles"] or _is_roshan(entry):
				continue
			if not _order_less(focal_order, entry["order"]):
				continue
			var hits: int = 0
			for cell: int in entry["cells"]:
				if focal.has(cell):
					covered[cell] = true
					hits += 1
			if hits > 0:
				coverers[String(entry["name"])] = int(coverers.get(String(entry["name"]), 0)) + hits
	listing.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return _order_less(a["order"], b["order"]))
	var upper: Array = []
	for value: int in depth_upper:
		upper.append(value)
	upper.sort()
	var counts: Array = []
	for value: int in depth:
		counts.append(value)
	counts.sort()
	var drawn: int = 0
	var at_least: Dictionary = {3: 0, 4: 0, 6: 0}
	for value: int in counts:
		drawn += value
		for threshold: int in at_least.keys():
			if value >= threshold:
				at_least[threshold] = int(at_least[threshold]) + 1
	return {
		"items": entries.size(),
		"kinds": kinds,
		"depth": {
			"mean": snappedf(float(drawn) / float(total), 0.01),
			"p50": counts[int(total * 0.5)],
			"p95": counts[mini(total - 1, int(total * 0.95))],
			"max": counts[total - 1],
			"share_ge3": snappedf(float(at_least[3]) / float(total), 0.001),
			"share_ge4": snappedf(float(at_least[4]) / float(total), 0.001),
			"share_ge6": snappedf(float(at_least[6]) / float(total), 0.001),
		},
		"depth_with_code_drawn_upper": {
			"p50": upper[int(total * 0.5)],
			"p95": upper[mini(total - 1, int(total * 0.95))],
			"max": upper[total - 1],
		},
		"hidden_share": snappedf(float(hidden_cells) / maxf(float(layer_cells), 1.0), 0.01),
		"listing": listing,
		"full_width_alpha_layers": full_width_alpha,
		"broad_overlays": overlays,
		"duplicates": duplicates,
		"custom_draw": {
			"items": custom_items,
			"with_shapes": custom_items.filter(func(item: Dictionary) -> bool: return bool(item["shapes"])).size(),
			"screen_share_upper_bound": snappedf(float(custom_cells.size()) / float(total), 0.001),
		},
		"vector_items": int(kinds.get("vector", 0)),
		"roshan": {
			"cells": focal.size(),
			"covered_share": snappedf(float(covered.size()) / maxf(float(focal.size()), 1.0), 0.01),
			"coverers": coverers,
		},
	}


func _duplicates(entries: Array[Dictionary]) -> Array:
	var groups: Dictionary = {}
	for entry: Dictionary in entries:
		if not entry.has("image") or String(entry["image"]) == "":
			continue
		var cells: PackedInt32Array = entry["cells"]
		if cells.size() < 4:
			continue
		var src: Rect2 = entry["src"]
		var key: String = "%s|%d,%d,%d,%d" % [entry["image"], int(src.position.x), int(src.position.y),
			int(src.size.x), int(src.size.y)]
		if not groups.has(key):
			groups[key] = []
		(groups[key] as Array).append(entry)
	var found: Array = []
	for key: String in groups.keys():
		var members: Array = groups[key]
		for first: int in range(members.size()):
			for second: int in range(first + 1, members.size()):
				var a: Dictionary = members[first]
				var b: Dictionary = members[second]
				var set_a: Dictionary = {}
				for cell: int in a["cells"]:
					set_a[cell] = true
				var shared: int = 0
				for cell: int in b["cells"]:
					if set_a.has(cell):
						shared += 1
				var smaller: int = mini((a["cells"] as PackedInt32Array).size(), (b["cells"] as PackedInt32Array).size())
				if smaller > 0 and float(shared) / float(smaller) >= 0.3:
					found.append({"image": a["image"], "names": [a["name"], b["name"]],
						"overlap": snappedf(float(shared) / float(smaller), 0.01)})
	return found


func _effects(before: Dictionary) -> Dictionary:
	var lifetimes: Dictionary = {}
	var elapsed: float = 0.0
	var focal: Dictionary = {}
	for sample_time: float in EFFECT_SAMPLES:
		await _wait(sample_time - elapsed)
		elapsed = sample_time
		var entries: Array[Dictionary] = _collect()
		for entry: Dictionary in entries:
			if _is_roshan(entry):
				for cell: int in entry["cells"]:
					focal[cell] = true
		for entry: Dictionary in entries:
			var id: int = int(entry["id"])
			if before.has(id) or String(entry.get("kind", "")) in ["text"]:
				continue
			var cells: PackedInt32Array = entry["cells"]
			var record: Dictionary = lifetimes.get(id, {"name": entry["name"],
				"kind": entry.get("kind", ""), "image": entry.get("image", ""),
				"first": sample_time, "last": sample_time, "max_cells": 0,
				"translucent_share": 0.0, "over_roshan": 0}) as Dictionary
			record["last"] = sample_time
			record["max_cells"] = maxi(int(record["max_cells"]), cells.size())
			record["translucent_share"] = maxf(float(record["translucent_share"]),
				float(entry["translucent"]) / maxf(float(cells.size()), 1.0))
			var over: int = 0
			for cell: int in cells:
				if focal.has(cell):
					over += 1
			record["over_roshan"] = maxi(int(record["over_roshan"]), over)
			lifetimes[id] = record
	var last_sample: float = EFFECT_SAMPLES[EFFECT_SAMPLES.size() - 1]
	var transient: Array = []
	var persistent: Array = []
	for record: Dictionary in lifetimes.values():
		record["max_screen_share"] = snappedf(float(record["max_cells"]) / float(COLS * ROWS), 0.001)
		record["over_roshan_share"] = snappedf(float(record["over_roshan"]) / maxf(float(focal.size()), 1.0), 0.01)
		record["translucent_share"] = snappedf(float(record["translucent_share"]), 0.01)
		if float(record["last"]) < last_sample:
			transient.append(record)
		else:
			persistent.append(record)
	return {"transient": transient, "persistent": persistent, "roshan_cells": focal.size()}


# --- Output -------------------------------------------------------------------

func _emit(game: String, state: String, metrics: Dictionary) -> void:
	metrics["game"] = game
	metrics["state"] = state
	print("OVERDRAW|STATE|", JSON.stringify(metrics))
	states_written += 1


func _emit_effects(game: String, state: String, _before: Dictionary, effects: Dictionary) -> void:
	effects["game"] = game
	effects["state"] = state
	print("OVERDRAW|EFFECTS|", JSON.stringify(effects))
	states_written += 1


func _error(message: String) -> void:
	errors += 1
	print("OVERDRAW|ERROR|", message)
