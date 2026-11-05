extends Node2D

const MASTER_SIZE := Vector2(6144.0, 2048.0)
const FRAME_COUNT: int = 32
const PERIOD: float = 4.0

var clock: float = 0.0
var motion_enabled: bool = true
var camera: Camera2D
var loops: Array[Dictionary] = []
var pressed: bool = false
var dragged: bool = false
var press_origin := Vector2.ZERO
var previous_screen := Vector2.ZERO
var capture_mode: bool = false

func _ready() -> void:
	for row in range(2):
		for column in range(6):
			var sprite := Sprite2D.new()
			sprite.texture = load("res://background/%d_%d.png" % [row, column]) as Texture2D
			sprite.centered = false
			sprite.position = Vector2(column * 1024, row * 1024)
			add_child(sprite)
	var textures_by_sha: Dictionary = {}
	var data: Array = JSON.parse_string(FileAccess.get_file_as_string("res://loops.json"))
	for entry: Dictionary in data:
		var sprite := Sprite2D.new()
		sprite.centered = false
		var box: Array = entry["box"]
		sprite.position = Vector2(float(box[0]), float(box[1]))
		var frames: Array[Texture2D] = []
		for index in range(FRAME_COUNT):
			var hash_value: String = entry["frames_sha256"][index]
			if not textures_by_sha.has(hash_value):
				textures_by_sha[hash_value] = load("res://%s/%02d.png" % [entry["id"], index]) as Texture2D
			frames.append(textures_by_sha[hash_value] as Texture2D)
		sprite.texture = frames[0]
		add_child(sprite)
		loops.append({"id": entry["id"], "sprite": sprite, "frames": frames,
			"phase": float(entry["phase"]), "index": 0,
			"bounds": Rect2(sprite.position, frames[0].get_size())})
	camera = Camera2D.new()
	camera.position = Vector2(1820, 1024)
	add_child(camera)
	camera.make_current()
	get_viewport().size_changed.connect(_fit_camera)
	_fit_camera()
	if "--verify" in OS.get_cmdline_user_args():
		set_process(false)
		_verify()
	elif "--capture-tour" in OS.get_cmdline_user_args():
		capture_mode = true
		set_process(false)
		_capture_tour()

func _process(delta: float) -> void:
	if motion_enabled:
		clock = fposmod(clock + delta, PERIOD)
	_update_frames()

func _update_frames() -> void:
	var half_view: Vector2 = get_viewport_rect().size / camera.zoom / 2.0
	var visible_world := Rect2(camera.position - half_view, half_view * 2.0)
	for entry in loops:
		var sprite: Sprite2D = entry["sprite"]
		sprite.visible = visible_world.intersects(entry["bounds"])
		var phase: float = fposmod(clock / PERIOD + float(entry["phase"]), 1.0)
		var index: int = int(floor(phase * FRAME_COUNT)) if motion_enabled else 0
		if int(entry["index"]) != index:
			var frames: Array[Texture2D] = entry["frames"]
			sprite.texture = frames[index]
			entry["index"] = index

func _unhandled_input(event: InputEvent) -> void:
	if capture_mode:
		return
	if event is InputEventScreenTouch:
		_pointer(event.position, event.pressed)
	elif event is InputEventScreenDrag:
		_drag(event.position)
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		_pointer(event.position, event.pressed)
	elif event is InputEventMouseMotion and pressed:
		_drag(event.position)
	elif event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_M:
		motion_enabled = not motion_enabled
		_update_frames()

func _pointer(screen: Vector2, down: bool) -> void:
	pressed = down
	if down:
		press_origin = screen
		previous_screen = screen
		dragged = false
	elif not dragged:
		# A tap reframes the existing painting without changing object pixels.
		var world: Vector2 = get_global_mouse_position()
		if DisplayServer.is_touchscreen_available():
			world = camera.position + (screen - get_viewport_rect().size / 2.0) / camera.zoom
		camera.position.x = world.x
		_clamp_camera()
		_update_frames()

func _drag(screen: Vector2) -> void:
	if not pressed:
		return
	if screen.distance_to(press_origin) > 12.0:
		dragged = true
	if dragged:
		camera.position.x -= (screen.x - previous_screen.x) / camera.zoom.x
		_clamp_camera()
		_update_frames()
	previous_screen = screen

func _fit_camera() -> void:
	var viewport_size: Vector2 = get_viewport_rect().size
	var zoom_value: float = maxf(viewport_size.y / MASTER_SIZE.y, viewport_size.x / MASTER_SIZE.x)
	camera.zoom = Vector2.ONE * zoom_value
	_clamp_camera()
	_update_frames()

func _clamp_camera() -> void:
	var half_width: float = get_viewport_rect().size.x / camera.zoom.x / 2.0
	camera.position.x = clampf(camera.position.x, half_width, MASTER_SIZE.x - half_width)

func _verify() -> void:
	# Let Camera2D and the window settle before the first pixel comparison.
	for frame in range(3):
		await RenderingServer.frame_post_draw
	var passed: bool = RenderingServer.get_current_rendering_method() == "mobile"
	var seen: Dictionary = {}
	for entry in loops:
		seen[entry["id"]] = {}
	for index in range(FRAME_COUNT):
		clock = float(index) * PERIOD / FRAME_COUNT
		_update_frames()
		for entry in loops:
			seen[entry["id"]][entry["index"]] = true
	for entry in loops:
		passed = passed and seen[entry["id"]].size() == FRAME_COUNT
	# Phase-offset rest comparisons always select the exact original crop.
	motion_enabled = false
	_update_frames()
	await RenderingServer.frame_post_draw
	var rest: Image = get_viewport().get_texture().get_image()
	for entry in loops:
		var sprite: Sprite2D = entry["sprite"]
		sprite.hide()
	await RenderingServer.frame_post_draw
	var flat: Image = get_viewport().get_texture().get_image()
	var exact_rest: bool = rest.get_data() == flat.get_data()
	var rest_bytes: PackedByteArray = rest.get_data()
	var flat_bytes: PackedByteArray = flat.get_data()
	var max_rest_error: int = 0
	for byte_index in range(rest_bytes.size()):
		max_rest_error = maxi(max_rest_error, absi(int(rest_bytes[byte_index]) - int(flat_bytes[byte_index])))
	# Measured 8-bit texture-sampler rounding, with exact source-crop checks.
	passed = passed and max_rest_error <= 1
	motion_enabled = true
	clock = 0.63
	_update_frames()
	await RenderingServer.frame_post_draw
	var moving: Image = get_viewport().get_texture().get_image()
	var visible_motion: bool = moving.get_data() != flat.get_data()
	passed = passed and visible_motion
	moving.save_png("res://mobile-review.png")
	var old_x: float = camera.position.x
	_pointer(Vector2(900, 350), true)
	_drag(Vector2(60, 350))
	_pointer(Vector2(60, 350), false)
	passed = passed and camera.position.x > old_x and camera.position.x <= MASTER_SIZE.x
	var receipt: Dictionary = {"result": "PASS" if passed else "FAIL",
		"engine": Engine.get_version_info(), "renderer": RenderingServer.get_current_rendering_method(),
		"frames_per_loop": FRAME_COUNT, "loops": loops.size(),
		"exact_rendered_rest_against_flat": exact_rest, "maximum_rest_channel_error": max_rest_error,
		"rendered_rest_tolerance": 1, "visible_rendered_motion": visible_motion,
		"drag_pan": camera.position.x > old_x, "physical_device_acceptance": "PENDING"}
	var file: FileAccess = FileAccess.open("res://desktop-verification.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t"))
	file.close()
	print("SKY_OVERLAY ", "PASS" if passed else "FAIL", " | exact_rest=", exact_rest,
		" | max_rest_error=", max_rest_error, " | visible_motion=", visible_motion, " | loops=", loops.size())
	get_tree().quit(0 if passed else 1)

func _capture_tour() -> void:
	DirAccess.make_dir_recursive_absolute("res://capture")
	for index in range(96):
		var t: float = float(index) / 95.0
		camera.zoom = Vector2.ONE * (720.0 / MASTER_SIZE.y)
		camera.position = Vector2(1820.0 + 2504.0 * smoothstep(0.0, 1.0, t), 1024.0)
		clock = float(index) / 12.0
		_update_frames()
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("res://capture/%03d.png" % index)
	get_tree().quit()
