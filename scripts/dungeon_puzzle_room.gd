class_name DungeonPuzzleRoom
extends Node3D
# One-finger, no-fail dungeon puzzles. Each room presents its instructions as
# large symbols in the world and repeats the prompt through ReefMain._say().

const CENTER := Vector3(0.0, -2200.0, 0.0)

var m: ReefMain
var finish_cb: Callable
var config: Dictionary = {}
var puzzle_kind := "sequence"
var state := "play"
var step := 0
var values: Array[int] = []
var selected := -1
var solved_pairs: Array[int] = []
var props: Array[Node3D] = []
var buttons: Array[Button] = []
var prev_env: Environment = null
var hud: CanvasLayer = null
var objective: Label = null
var hint: Label = null
var pointer: Label3D = null

func start(main: ReefMain, room_config: Dictionary, done_cb: Callable) -> void:
	m = main
	config = room_config
	finish_cb = done_cb
	puzzle_kind = String(config.get("puzzle", "sequence"))
	_build_environment()
	_build_room()
	_build_props()
	_build_camera()
	_build_hud()
	_update_visuals()
	m.show_msg("Roshan", String(config.get("voice", "Follow the golden sparkle and solve the picture puzzle!")), "dungeon_puzzle")

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(config.get("background", Color(0.055, 0.065, 0.16)))
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.72, 0.78, 1.0)
	env.ambient_light_energy = 1.05
	env.glow_enabled = true
	env.glow_intensity = 0.55
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(0.82, 0.9, 1.0)
	sun.light_energy = 1.1
	sun.rotation_degrees = Vector3(-52, -24, 0)
	add_child(sun)

func _mat(col: Color, glow: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.68
	if glow > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = glow
	return mat

func _mesh(mesh: Mesh, pos: Vector3, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.mesh = mesh
	node.position = pos
	node.material_override = _mat(col, glow)
	add_child(node)
	return node

func _sphere(pos: Vector3, radius: float, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius * 2.0
	mesh.radial_segments = 12
	mesh.rings = 6
	return _mesh(mesh, pos, col, glow)

func _box(pos: Vector3, size: Vector3, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var mesh := BoxMesh.new()
	mesh.size = size
	return _mesh(mesh, pos, col, glow)

func _build_room() -> void:
	var floor := CylinderMesh.new()
	floor.top_radius = 27.0
	floor.bottom_radius = 27.0
	floor.height = 1.0
	floor.radial_segments = 8
	_mesh(floor, CENTER, Color(config.get("floor", Color(0.32, 0.42, 0.62))))
	var trim: Color = Color(config.get("trim", Color(0.65, 0.92, 1.0)))
	for i in range(8):
		var angle := float(i) * TAU / 8.0
		var wall := _box(CENTER + Vector3(sin(angle) * 26.2, 1.2, cos(angle) * 26.2), Vector3(20.5, 3.0, 1.0), trim, 0.18)
		wall.rotation.y = angle
	# The far doorway is the common goal and visibly opens on completion.
	_box(CENTER + Vector3(0, 5.0, -24.8), Vector3(9.0, 10.0, 1.4), Color(0.16, 0.12, 0.3))
	_sphere(CENTER + Vector3(0, 7.0, -24.0), 0.85, Color(1.0, 0.88, 0.22), 1.3)

func _build_props() -> void:
	match puzzle_kind:
		"sequence", "elemental":
			_build_sequence_props()
		"path":
			_build_path_props()
		"torches":
			_build_torch_props()
		"rotate":
			_build_shell_props()
		"pairs":
			_build_pair_props()

func _build_sequence_props() -> void:
	var choices: Array = config.get("choices", ["◆", "●", "▲"])
	var sequence: Array = config.get("solution", [0, 1, 2])
	for i in range(sequence.size()):
		var label := Label3D.new()
		label.text = String(choices[int(sequence[i])])
		label.font_size = 130
		label.pixel_size = 0.024
		label.outline_size = 20
		label.modulate = _choice_color(int(sequence[i]))
		label.position = CENTER + Vector3((float(i) - float(sequence.size() - 1) * 0.5) * 5.0, 6.0, -12.0)
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		add_child(label)
		props.append(label)

func _build_path_props() -> void:
	var sequence: Array = config.get("solution", [0, 1, 0, 0])
	for i in range(sequence.size()):
		var x := -4.2 if int(sequence[i]) == 0 else 4.2
		var stone := _box(CENTER + Vector3(x, 0.8, 7.0 - float(i) * 7.0), Vector3(5.4, 0.7, 4.5), Color(0.35, 0.48, 0.65))
		stone.scale = Vector3(0.2, 0.2, 0.2)
		props.append(stone)

func _build_torch_props() -> void:
	var order: Array = config.get("solution", [1, 3, 0, 2])
	var heights := [5.5, 3.0, 7.0, 4.2]
	for i in range(4):
		var x := (float(i) - 1.5) * 7.0
		var pole := _box(CENTER + Vector3(x, heights[i] * 0.5, -8.0), Vector3(1.0, heights[i], 1.0), Color(0.34, 0.2, 0.12))
		props.append(pole)
		_sphere(CENTER + Vector3(x, heights[i] + 0.5, -8.0), 0.65, Color(0.22, 0.15, 0.12))
	# The config order is deliberately shortest-to-tallest and drives validation.
	config["solution"] = order

func _build_shell_props() -> void:
	values = [0, 0, 0]
	for i in range(3):
		var root := Node3D.new()
		root.position = CENTER + Vector3((float(i) - 1.0) * 9.0, 1.0, -8.0)
		add_child(root)
		var shell := SphereMesh.new()
		shell.radius = 2.5
		shell.height = 4.0
		shell.radial_segments = 8
		var shell_node := MeshInstance3D.new()
		shell_node.mesh = shell
		shell_node.material_override = _mat(Color(0.34, 0.65, 0.48))
		root.add_child(shell_node)
		var nose := BoxMesh.new()
		nose.size = Vector3(0.7, 0.7, 3.2)
		var nose_node := MeshInstance3D.new()
		nose_node.mesh = nose
		nose_node.position = Vector3(0, 0.4, 2.4)
		nose_node.material_override = _mat(Color(1.0, 0.83, 0.25), 0.4)
		root.add_child(nose_node)
		props.append(root)
	_sphere(CENTER + Vector3(0, 2.0, 1.0), 1.5, Color(1.0, 0.88, 0.35), 1.0)

func _build_pair_props() -> void:
	var symbols: Array = config.get("cards", ["☾", "★", "☾", "★"])
	for i in range(symbols.size()):
		var label := Label3D.new()
		label.text = "?"
		label.font_size = 150
		label.pixel_size = 0.025
		label.outline_size = 20
		label.modulate = Color(0.72, 0.63, 1.0)
		label.position = CENTER + Vector3((float(i % 2) - 0.5) * 10.0, 5.0, -6.0 - float(i / 2) * 8.0)
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		label.set_meta("symbol", String(symbols[i]))
		add_child(label)
		props.append(label)

func _build_camera() -> void:
	var cam := Camera3D.new()
	cam.fov = 58.0
	cam.position = CENTER + Vector3(0, 30.0, 31.0)
	add_child(cam)
	cam.look_at(CENTER + Vector3(0, 2.0, -3.0), Vector3.UP)
	cam.make_current()

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 14
	add_child(hud)
	var banner := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.04, 0.05, 0.14, 0.9)
	style.border_color = Color(1.0, 0.82, 0.25)
	style.set_border_width_all(4)
	style.set_corner_radius_all(22)
	banner.add_theme_stylebox_override("panel", style)
	banner.position = Vector2(250, 20)
	banner.size = Vector2(780, 94)
	hud.add_child(banner)
	objective = Label.new()
	objective.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	objective.add_theme_font_size_override("font_size", 28)
	objective.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	objective.add_theme_constant_override("outline_size", 7)
	objective.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	objective.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	banner.add_child(objective)
	hint = Label.new()
	hint.position = Vector2(300, 520)
	hint.size = Vector2(680, 58)
	hint.add_theme_font_size_override("font_size", 25)
	hint.add_theme_color_override("font_outline_color", Color(0.03, 0.02, 0.1))
	hint.add_theme_constant_override("outline_size", 7)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hud.add_child(hint)
	pointer = Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 145
	pointer.pixel_size = 0.022
	pointer.outline_size = 22
	pointer.modulate = Color(1.0, 0.9, 0.18)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(pointer)
	var labels: Array = config.get("choices", ["◀", "▶"])
	var count := int(config.get("button_count", labels.size()))
	if puzzle_kind == "pairs":
		count = 4
		labels = ["?", "?", "?", "?"]
	elif puzzle_kind == "rotate":
		count = 3
		labels = ["↻", "↻", "↻"]
	for i in range(count):
		var button := Button.new()
		button.text = String(labels[i]) if i < labels.size() else "◆"
		button.position = Vector2(640.0 - float(count) * 73.0 + float(i) * 146.0, 584)
		button.size = Vector2(132, 112)
		button.add_theme_font_size_override("font_size", 50)
		var button_style := StyleBoxFlat.new()
		button_style.bg_color = _choice_color(i)
		button_style.border_color = Color(1.0, 0.92, 0.5)
		button_style.set_border_width_all(5)
		button_style.set_corner_radius_all(30)
		button.add_theme_stylebox_override("normal", button_style)
		button.add_theme_stylebox_override("hover", button_style)
		button.add_theme_stylebox_override("pressed", button_style)
		button.pressed.connect(_puzzle_action.bind(i))
		hud.add_child(button)
		buttons.append(button)

func _choice_color(index: int) -> Color:
	var palette := [Color(0.28, 0.72, 1.0), Color(1.0, 0.38, 0.22), Color(0.72, 0.42, 1.0), Color(0.25, 0.82, 0.55)]
	return palette[index % palette.size()]

func _puzzle_action(choice: int) -> void:
	if state != "play":
		return
	match puzzle_kind:
		"rotate":
			_rotate_action(choice)
		"pairs":
			_pair_action(choice)
		_:
			_sequence_action(choice)
	_update_visuals()

func _sequence_action(choice: int) -> void:
	var solution: Array = config.get("solution", [])
	if step >= solution.size():
		return
	if choice == int(solution[step]):
		step += 1
		if puzzle_kind == "path" and step <= props.size():
			props[step - 1].scale = Vector3.ONE
		elif puzzle_kind == "torches" and choice < props.size():
			var pole: Node3D = props[choice]
			_sphere(pole.position + Vector3(0, 3.8, 0), 1.0, Color(1.0, 0.42, 0.08), 1.4)
	else:
		hint.text = "✨  TRY THE GOLDEN CLUE  ✨"
		m.show_msg("Roshan", "Almost! Look at the golden picture and try that one.", "gentle_hint")
	if step >= solution.size():
		_solve()

func _rotate_action(choice: int) -> void:
	if choice < 0 or choice >= values.size():
		return
	values[choice] = (values[choice] + 1) % 4
	props[choice].rotation_degrees.y = float(values[choice]) * 90.0
	var targets: Array = config.get("targets", [1, 2, 3])
	var all_ready := true
	for i in range(values.size()):
		if values[i] != int(targets[i]):
			all_ready = false
	if all_ready:
		_solve()

func _pair_action(choice: int) -> void:
	if choice in solved_pairs or choice < 0 or choice >= props.size():
		return
	var card := props[choice] as Label3D
	card.text = String(card.get_meta("symbol"))
	if selected < 0:
		selected = choice
		return
	var first := props[selected] as Label3D
	if first.get_meta("symbol") == card.get_meta("symbol") and selected != choice:
		solved_pairs.append(selected)
		solved_pairs.append(choice)
		selected = -1
		if solved_pairs.size() == props.size():
			_solve()
	else:
		first.text = "?"
		card.text = "?"
		selected = -1
		hint.text = "✨  PICTURES HID AGAIN — TRY ONCE MORE!  ✨"

func _update_visuals() -> void:
	if objective == null or state != "play":
		return
	var solution: Array = config.get("solution", [])
	match puzzle_kind:
		"sequence":
			objective.text = "♫  COPY THE CRYSTAL SONG  ♫"
		"path":
			objective.text = "❄  BUILD THE PICTURED ICE PATH  ❄"
		"torches":
			objective.text = "🌶  LIGHT THE SHORTEST TORCH FIRST  🌶"
		"rotate":
			objective.text = "🐚  TURN EVERY GOLDEN NOSE TO THE PEARL  🐚"
		"pairs":
			objective.text = "☾  FIND THE TWO MATCHING PICTURES  ★"
		"elemental":
			objective.text = "❄  COPY THE ICE AND FIRE DOOR  🔥"
	if puzzle_kind in ["sequence", "path", "torches", "elemental"] and step < solution.size():
		var next := int(solution[step])
		if next < buttons.size():
			hint.text = "◆  %d / %d  ◆" % [step + 1, solution.size()]
		pointer.position = CENTER + Vector3((float(next) - float(buttons.size() - 1) * 0.5) * 6.0, 10.0, -8.0)
	elif puzzle_kind == "rotate":
		pointer.position = CENTER + Vector3(0, 10.0, 1.0)
	elif puzzle_kind == "pairs":
		pointer.position = CENTER + Vector3(0, 11.0, -9.0)

func _solve() -> void:
	if state != "play":
		return
	state = "celebrate"
	objective.text = "★  DOOR OPEN!  ★"
	hint.text = "✨  PUZZLE SOLVED  ✨"
	pointer.position = CENTER + Vector3(0, 11.0, -24.0)
	for button in buttons:
		button.disabled = true
	m.show_msg("Roshan", "You solved it! The golden door is open!", "win")
	var timer := get_tree().create_timer(float(config.get("win_time", 1.2)))
	timer.timeout.connect(_finish)

func force_solve() -> void:
	_solve()

func cancel() -> void:
	state = "cancelled"
	_restore_environment()
	queue_free()

func _finish() -> void:
	if state == "done":
		return
	state = "done"
	_restore_environment()
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()

func _restore_environment() -> void:
	if m != null and m.we_node != null:
		m.we_node.environment = prev_env
