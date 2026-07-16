class_name DungeonPuzzleRoom
extends Node3D
# Spatial, one-finger, no-fail dungeon puzzles. Roshan swims between oversized
# picture props and taps USE nearby. Text is supplementary; the geometry,
# symbols, golden pointer, chimes and existing family voice clips carry play.

const CENTER := Vector3(0.0, -2200.0, 0.0)
const RADIUS := 25.0
const MOVE_SPEED := 13.0

var m: ReefMain
var finish_cb: Callable
var config: Dictionary = {}
var puzzle_kind := "sequence"
var state := "play"
var step := 0
var values: Array[int] = []
var selected := -1
var solved_pairs: Array[int] = []
var interactives: Array[Dictionary] = []
var reveal_nodes: Array[Node3D] = []
var card_labels: Array[Label3D] = []
var buttons: Array[Button] = []
var pair_hide: Array[int] = []
var pair_hide_t := 0.0
var prev_env: Environment = null
var avatar: Sprite3D = null
var player_pos := Vector3.ZERO
var fire_prev := false
var door: MeshInstance3D = null
var exit_t := 0.0
var hud: CanvasLayer = null
var objective: Label = null
var hint: Label = null
var pointer: Label3D = null
var touch_pointer: Label = null
var clue_pos := CENTER + Vector3(0, 8.0, -12.0)
var materials := {}

func start(main: ReefMain, room_config: Dictionary, done_cb: Callable) -> void:
	m = main
	config = room_config
	finish_cb = done_cb
	puzzle_kind = String(config.get("puzzle", "sequence"))
	player_pos = CENTER + Vector3(0, 1.1, 17.0)
	_build_environment()
	_build_room()
	_build_avatar()
	_build_props()
	_build_camera()
	_build_hud()
	_update_visuals()
	m.show_msg("Roshan", String(config.get("voice", "Follow the pictures and golden sparkle!")), "talk")

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(config.get("background", Color(0.055, 0.065, 0.16)))
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.72, 0.78, 1.0)
	env.ambient_light_energy = 1.05
	env.glow_enabled = true
	env.glow_intensity = 0.5
	env.glow_bloom = 0.1
	m._speedy_glow_clamp(env)
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(0.82, 0.9, 1.0)
	sun.light_energy = 1.05
	sun.shadow_enabled = m.quality != "speedy"
	sun.rotation_degrees = Vector3(-52, -24, 0)
	add_child(sun)

func _mat(col: Color, glow: float = 0.0) -> StandardMaterial3D:
	var key := "%s:%.2f" % [col.to_html(true), glow]
	if materials.has(key):
		return materials[key]
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.68
	if glow > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = glow
	materials[key] = mat
	return mat

func _mesh(mesh: Mesh, pos: Vector3, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.mesh = mesh
	node.position = pos
	node.material_override = _mat(col, glow)
	var target: Node3D = self if parent == null else parent
	target.add_child(node)
	return node

func _sphere(pos: Vector3, radius: float, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius * 2.0
	mesh.radial_segments = 10
	mesh.rings = 5
	return _mesh(mesh, pos, col, glow, parent)

func _box(pos: Vector3, size: Vector3, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var mesh := BoxMesh.new()
	mesh.size = size
	return _mesh(mesh, pos, col, glow, parent)

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
		# Leave readable openings at the entrance and destination.
		if i == 0 or i == 4:
			continue
		var wall := _box(CENTER + Vector3(sin(angle) * 26.2, 2.0, cos(angle) * 26.2), Vector3(20.5, 4.5, 1.0), trim, 0.15)
		wall.rotation.y = angle
	for side in [-1.0, 1.0]:
		_box(CENTER + Vector3(side * 7.0, 5.0, -24.8), Vector3(5.0, 10.0, 1.4), trim)
	door = _box(CENTER + Vector3(0, 5.0, -24.7), Vector3(9.0, 10.0, 1.2), Color(0.16, 0.12, 0.3))
	_sphere(CENTER + Vector3(0, 8.0, -24.0), 0.85, Color(1.0, 0.88, 0.22), 1.2)
	# A short entrance bridge visually connects this room to the previous one.
	_box(CENTER + Vector3(0, 0.25, 25.5), Vector3(9.0, 0.5, 8.0), trim.darkened(0.25))

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	var tex := load("res://assets/characters/roshan_sprite.png") as Texture2D
	avatar.texture = tex
	avatar.pixel_size = 6.2 / maxf(float(tex.get_height()), 1.0) if tex != null else 0.01
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = player_pos
	add_child(avatar)

func _add_label(text: String, pos: Vector3, col: Color, size: int = 130) -> Label3D:
	var label := Label3D.new()
	label.text = text
	label.font_size = size
	label.pixel_size = 0.024
	label.outline_size = 20
	label.modulate = col
	label.position = pos
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(label)
	return label

func _add_pad(index: int, pos: Vector3, symbol: String, col: Color) -> Node3D:
	var root := Node3D.new()
	root.position = pos
	add_child(root)
	var pad := CylinderMesh.new()
	pad.top_radius = 3.4
	pad.bottom_radius = 3.8
	pad.height = 0.8
	pad.radial_segments = 8
	_mesh(pad, Vector3.ZERO, col, 0.2, root)
	var label := _add_label(symbol, pos + Vector3(0, 3.0, 0), Color.WHITE, 120)
	interactives.append({"index": index, "node": root, "label": label, "pos": pos})
	return root

func _choice_color(index: int) -> Color:
	var palette := [Color(0.28, 0.72, 1.0), Color(1.0, 0.38, 0.22), Color(0.72, 0.42, 1.0), Color(0.25, 0.82, 0.55)]
	return palette[index % palette.size()]

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
	var solution: Array = config.get("solution", [0, 1, 2])
	for i in range(solution.size()):
		_add_label(String(choices[int(solution[i])]), CENTER + Vector3((float(i) - float(solution.size() - 1) * 0.5) * 5.0, 7.0, -13.0), _choice_color(int(solution[i])))
	var count := int(config.get("choice_count", choices.size()))
	for i in range(count):
		_add_pad(i, CENTER + Vector3((float(i) - float(count - 1) * 0.5) * 8.0, 0.7, 4.0), String(choices[i]), _choice_color(i))
	clue_pos = CENTER + Vector3(0, 11.0, -13.0)

func _build_path_props() -> void:
	var solution: Array = config.get("solution", [0, 1, 0, 0])
	for i in range(solution.size()):
		var x := -4.5 if int(solution[i]) == 0 else 4.5
		var stone := _box(CENTER + Vector3(x, 0.8, 2.0 - float(i) * 5.0), Vector3(5.5, 0.7, 3.8), Color(0.5, 0.88, 1.0), 0.35)
		stone.scale = Vector3(0.12, 0.12, 0.12)
		reveal_nodes.append(stone)
	_add_pad(0, CENTER + Vector3(-6.5, 0.7, 11.0), "◀", _choice_color(0))
	_add_pad(1, CENTER + Vector3(6.5, 0.7, 11.0), "▶", _choice_color(1))
	clue_pos = CENTER + Vector3(0, 9.0, -7.0)

func _build_torch_props() -> void:
	var heights := [5.5, 3.0, 7.0, 4.2]
	for i in range(4):
		var x := (float(i) - 1.5) * 7.0
		var pos := CENTER + Vector3(x, 0.5, -6.0)
		_box(pos + Vector3(0, heights[i] * 0.5, 0), Vector3(1.2, heights[i], 1.2), Color(0.34, 0.2, 0.12))
		var flame := _sphere(pos + Vector3(0, heights[i] + 0.6, 0), 0.9, Color(1.0, 0.38, 0.08), 1.2)
		flame.visible = false
		reveal_nodes.append(flame)
		_add_pad(i, pos, "🌶", _choice_color(i))
	clue_pos = CENTER + Vector3(0, 11.0, -6.0)

func _build_shell_props() -> void:
	values = [0, 0, 0]
	for i in range(3):
		var root := Node3D.new()
		root.position = CENTER + Vector3((float(i) - 1.0) * 9.0, 1.0, -7.0)
		add_child(root)
		var shell := SphereMesh.new()
		shell.radius = 2.5
		shell.height = 4.0
		shell.radial_segments = 8
		_mesh(shell, Vector3.ZERO, Color(0.34, 0.65, 0.48), 0.0, root)
		_box(Vector3(0, 0.4, 2.4), Vector3(0.7, 0.7, 3.2), Color(1.0, 0.83, 0.25), 0.4, root)
		interactives.append({"index": i, "node": root, "pos": root.position})
	_sphere(CENTER + Vector3(0, 2.0, 2.0), 1.6, Color(1.0, 0.88, 0.35), 1.0)
	clue_pos = CENTER + Vector3(0, 9.0, 2.0)

func _build_pair_props() -> void:
	var symbols: Array = config.get("cards", ["☾", "★", "☾", "★"])
	for i in range(symbols.size()):
		var pos := CENTER + Vector3((float(i % 2) - 0.5) * 11.0, 0.7, 3.0 - float(i / 2) * 9.0)
		var root := _add_pad(i, pos, "?", Color(0.48, 0.34, 0.72))
		root.set_meta("symbol", String(symbols[i]))
		var entry: Dictionary = interactives[interactives.size() - 1]
		card_labels.append(entry["label"] as Label3D)
	clue_pos = CENTER + Vector3(0, 11.0, -2.0)

func _build_camera() -> void:
	var cam := Camera3D.new()
	cam.fov = 58.0
	cam.position = CENTER + Vector3(0, 31.0, 32.0)
	add_child(cam)
	cam.look_at(CENTER + Vector3(0, 1.5, -3.0), Vector3.UP)
	cam.make_current()

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 14
	add_child(hud)
	var banner := Panel.new()
	banner.mouse_filter = Control.MOUSE_FILTER_IGNORE
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
	objective.mouse_filter = Control.MOUSE_FILTER_IGNORE
	objective.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	objective.add_theme_font_size_override("font_size", 28)
	objective.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	objective.add_theme_constant_override("outline_size", 7)
	objective.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	objective.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	banner.add_child(objective)
	hint = Label.new()
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hint.position = Vector2(300, 520)
	hint.size = Vector2(680, 54)
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
	pointer.position = clue_pos
	add_child(pointer)

func _move_input() -> Vector2:
	var value := Vector2.ZERO
	if Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT): value.x -= 1.0
	if Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT): value.x += 1.0
	if Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP): value.y -= 1.0
	if Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN): value.y += 1.0
	if m.touch_ui != null and m.touch_ui.stick_vec.length() > 0.12:
		value = m.touch_ui.stick_vec
	return value.limit_length(1.0)

func _action_pressed() -> bool:
	var held: bool = Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	var just: bool = held and not fire_prev
	fire_prev = held
	if m.touch_ui != null and m.touch_ui.consume_action_just():
		just = true
	return just

func _process(delta: float) -> void:
	if m == null or state in ["done", "cancelled"]:
		return
	if pair_hide_t > 0.0:
		pair_hide_t -= delta
		if pair_hide_t <= 0.0:
			for idx in pair_hide:
				card_labels[idx].text = "?"
			pair_hide.clear()
	if state == "exit":
		exit_t += delta
		var exit_target := CENTER + Vector3(0, 1.1, -27.0)
		player_pos = player_pos.move_toward(exit_target, delta * 9.0)
		avatar.position = player_pos
		if player_pos.z <= CENTER.z - 24.0 or exit_t >= 4.0:
			_finish()
		return
	var move := _move_input()
	player_pos += Vector3(move.x, 0, move.y) * MOVE_SPEED * delta
	var flat := Vector2(player_pos.x - CENTER.x, player_pos.z - CENTER.z)
	if flat.length() > RADIUS - 2.0:
		flat = flat.normalized() * (RADIUS - 2.0)
		player_pos.x = CENTER.x + flat.x
		player_pos.z = CENTER.z + flat.y
	avatar.position = player_pos + Vector3(0, sin(Time.get_ticks_msec() * 0.004) * 0.12, 0)
	for entry: Dictionary in interactives:
		(entry["node"] as Node3D).scale = Vector3.ONE
	var near := _nearest_interactive()
	if near >= 0:
		var entry: Dictionary = interactives[near]
		var node: Node3D = entry["node"]
		node.scale = Vector3.ONE * (1.0 + sin(Time.get_ticks_msec() * 0.006) * 0.05)
		hint.text = "◆  TAP USE NEAR THE GLOWING PICTURE  ◆"
	if _action_pressed() and near >= 0 and pair_hide_t <= 0.0:
		_puzzle_action(int(interactives[near]["index"]))

func _nearest_interactive() -> int:
	var best := -1
	var best_d := 6.0 * 6.0
	for i in range(interactives.size()):
		var entry: Dictionary = interactives[i]
		var dist := player_pos.distance_squared_to(entry["pos"] as Vector3)
		if dist < best_d:
			best_d = dist
			best = i
	return best

func _puzzle_action(choice: int) -> void:
	if state != "play":
		return
	match puzzle_kind:
		"rotate": _rotate_action(choice)
		"pairs": _pair_action(choice)
		_: _sequence_action(choice)
	_update_visuals()

func _sequence_action(choice: int) -> void:
	var solution: Array = config.get("solution", [])
	if step >= solution.size():
		return
	if choice != int(solution[step]):
		_gentle_hint()
		return
	_step_chime(step)
	if puzzle_kind == "path" and step < reveal_nodes.size():
		reveal_nodes[step].scale = Vector3.ONE
		player_pos = CENTER + Vector3(0, 1.1, 17.0)
	elif puzzle_kind == "torches" and choice < reveal_nodes.size():
		reveal_nodes[choice].visible = true
	step += 1
	if step >= solution.size():
		_solve()

func _rotate_action(choice: int) -> void:
	if choice < 0 or choice >= values.size():
		return
	values[choice] = (values[choice] + 1) % 4
	(interactives[choice]["node"] as Node3D).rotation_degrees.y = float(values[choice]) * 90.0
	_step_chime(values[choice])
	var targets: Array = config.get("targets", [1, 0, 3])
	for i in range(values.size()):
		if values[i] != int(targets[i]):
			return
	_solve()

func _pair_action(choice: int) -> void:
	if choice in solved_pairs or choice < 0 or choice >= card_labels.size():
		return
	var card_root: Node3D = interactives[choice]["node"]
	card_labels[choice].text = String(card_root.get_meta("symbol"))
	if selected < 0:
		selected = choice
		_step_chime(0)
		return
	var first_root: Node3D = interactives[selected]["node"]
	if first_root.get_meta("symbol") == card_root.get_meta("symbol") and selected != choice:
		solved_pairs.append(selected)
		solved_pairs.append(choice)
		buttons[selected].disabled = true
		buttons[choice].disabled = true
		selected = -1
		_step_chime(2)
		if solved_pairs.size() == card_labels.size():
			_solve()
	else:
		# Keep both pictures visible long enough for a child to learn the mismatch.
		pair_hide = [selected, choice]
		pair_hide_t = 1.1
		selected = -1
		hint.text = "✨  LOOK AT BOTH PICTURES — THEN TRY AGAIN  ✨"
		m.show_msg("Roshan", "Those are different. Look at both pictures, then try again!", "oops")

func _step_chime(index: int) -> void:
	if m.chime != null:
		m.chime.pitch_scale = 0.9 + float(index % 4) * 0.12
		m.chime.play()

func _gentle_hint() -> void:
	hint.text = "✨  CHECK THE BIG PICTURE CLUE  ✨"
	m.show_msg("Roshan", "Almost! Look at the big picture and try again.", "oops")

func _update_visuals() -> void:
	if objective == null or state != "play":
		return
	if touch_pointer != null:
		touch_pointer.visible = false
	var solution: Array = config.get("solution", [])
	match puzzle_kind:
		"sequence": objective.text = "♫  SWIM TO THE CRYSTALS IN PICTURE ORDER  ♫"
		"path": objective.text = "❄  FREEZE THE PICTURED LEFT-RIGHT PATH  ❄"
		"torches": objective.text = "🌶  LIGHT SHORTEST TO TALLEST  🌶"
		"rotate": objective.text = "🐚  TURN THE GOLDEN NOSES TO THE PEARL  🐚"
		"pairs": objective.text = "☾  FIND THE TWO MATCHING PICTURES  ★"
		"elemental": objective.text = "❄  COPY THE ICE-FIRE DOOR PICTURES  🔥"
	if not solution.is_empty():
		hint.text = "◆  %d / %d  ◆" % [mini(step + 1, solution.size()), solution.size()]
	pointer.position = clue_pos + Vector3(0, sin(Time.get_ticks_msec() * 0.004) * 0.35, 0)

func _solve() -> void:
	if state != "play":
		return
	state = "exit"
	objective.text = "★  THE WAY FORWARD IS OPEN!  ★"
	hint.text = "✨  SWIM THROUGH THE GOLDEN DOOR  ✨"
	pointer.position = CENTER + Vector3(0, 11.0, -24.0)
	if door != null:
		var tween := door.create_tween()
		tween.tween_property(door, "position:y", CENTER.y - 6.0, 0.75).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	m.show_msg("Roshan", "The golden door is open! Swim through!", "win")

func force_solve() -> void:
	_solve()

func cancel() -> void:
	# Opening the door is the earned completion moment. If the child taps Home
	# during the short celebration, checkpoint it instead of discarding it.
	if state == "celebrate":
		_finish()
		return
	if state == "done" or state == "cancelled":
		return
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
