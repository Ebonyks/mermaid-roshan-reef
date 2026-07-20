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
var card_labels: Array[Node3D] = []
var pair_hide: Array[int] = []
var pair_hide_t := 0.0
var prev_env: Environment = null
var avatar: Sprite3D = null
var player_pos := Vector3.ZERO
var fire_prev := false
var door: Node3D = null
var exit_t := 0.0
var hud: CanvasLayer = null
var objective: Label = null
var hint: Label = null
var pointer: Label3D = null
var clue_pos := CENTER + Vector3(0, 8.0, -12.0)
var materials := {}
var idle_t := 0.0
var remind_stage := 0
var wrong_streak := 0
var guided := false
var clue_symbols: Array[Node3D] = []
var statue_marks: Array[MeshInstance3D] = []
var statue_done: Array[bool] = []

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

func _build_room() -> void:
	var floor_col := Color(config.get("floor", Color(0.32, 0.42, 0.62)))
	var trim: Color = Color(config.get("trim", Color(0.65, 0.92, 1.0)))
	var arena := DungeonArt.spawn("arena", self, CENTER)
	DungeonArt.tint(arena, _mat(floor_col), _mat(trim, 0.15))
	door = DungeonArt.spawn("door", self, CENTER + Vector3(0, 0, -24.7))
	DungeonArt.tint(door, _mat(floor_col.darkened(0.2)), _mat(trim))

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	var tex := load("res://assets/characters/roshan_sprite.png") as Texture2D
	avatar.texture = tex
	avatar.pixel_size = 6.2 / maxf(float(tex.get_height()), 1.0) if tex != null else 0.01
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = player_pos
	add_child(avatar)

func _add_pad(index: int, pos: Vector3, symbol: String, col: Color, keep_kinds: Array[String] = []) -> Node3D:
	var root := Node3D.new()
	root.position = pos
	add_child(root)
	var pedestal := DungeonArt.spawn("pedestal", root)
	DungeonArt.tint(pedestal, _mat(col.darkened(0.35)), _mat(col, 0.18))
	var picture := DungeonArt.add_pictogram(symbol, root, Vector3(0, 3.0, 0), 1.15, keep_kinds)
	interactives.append({"index": index, "node": root, "picture": picture, "pos": pos})
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
	var solution: Array = config.get("solution", [0, 1, 2])
	for i in range(solution.size()):
		var choice_index := int(solution[i])
		var kind := _element_kind(choice_index) if puzzle_kind == "elemental" else _sequence_kind(choice_index)
		# The clue row IS the objective for a non-reader: each symbol sits on a
		# dark disc for contrast, close enough to the camera to read at a glance.
		var slot := CENTER + Vector3((float(i) - float(solution.size() - 1) * 0.5) * 6.5, 8.0, -10.0)
		var disc := CylinderMesh.new()
		disc.top_radius = 2.6
		disc.bottom_radius = 2.6
		disc.height = 0.3
		_mesh(disc, slot, Color(0.05, 0.06, 0.16))
		clue_symbols.append(DungeonArt.add_pictogram(kind, self, slot + Vector3(0, 0.55, 0), 1.8))
	var default_count := 2 if puzzle_kind == "elemental" else 3
	var count := int(config.get("choice_count", default_count))
	for i in range(count):
		var kind := _element_kind(i) if puzzle_kind == "elemental" else _sequence_kind(i)
		_add_pad(i, CENTER + Vector3((float(i) - float(count - 1) * 0.5) * 8.0, 0.7, 4.0), kind, _choice_color(i))
	clue_pos = CENTER + Vector3(0, 11.0, -10.0)

func _sequence_kind(index: int) -> String:
	return ["diamond", "orb", "triangle"][index % 3]

func _element_kind(index: int) -> String:
	return "ice" if index % 2 == 0 else "flame"

func _build_path_props() -> void:
	var solution: Array = config.get("solution", [0, 1, 0, 0])
	for i in range(solution.size()):
		var x := -4.5 if int(solution[i]) == 0 else 4.5
		var stone := DungeonArt.spawn("stone", self, CENTER + Vector3(x, 0.8, 2.0 - float(i) * 5.0))
		stone.scale = Vector3(0.3, 0.3, 0.3)
		reveal_nodes.append(stone)
	_add_pad(0, CENTER + Vector3(-6.5, 0.7, 11.0), "left", _choice_color(0))
	_add_pad(1, CENTER + Vector3(6.5, 0.7, 11.0), "right", _choice_color(1))
	clue_pos = CENTER + Vector3(0, 9.0, -7.0)

func _build_torch_props() -> void:
	# Same shortest→tallest answer order as before, but every adjacent pair of
	# lanterns differs enough in height for a four-year-old to compare at sight.
	var heights := [5.6, 2.4, 7.6, 4.0]
	for i in range(4):
		var x := (float(i) - 1.5) * 7.0
		var pos := CENTER + Vector3(x, 0.5, -6.0)
		var lantern := DungeonArt.spawn("lantern", self, pos)
		lantern.scale.y = heights[i] / 5.5
		var flame := DungeonArt.find_part(lantern, "Glow")
		flame.visible = false
		reveal_nodes.append(flame)
		_add_pad(i, pos, "pepper", _choice_color(i))
	clue_pos = CENTER + Vector3(0, 11.0, -6.0)

func _build_shell_props() -> void:
	values = [0, 0, 0]
	statue_done = [false, false, false]
	var gold := Color(1.0, 0.85, 0.3)
	for i in range(3):
		var root := DungeonArt.spawn("statue", self, CENTER + Vector3((float(i) - 1.0) * 9.0, 1.0, -7.0))
		interactives.append({"index": i, "node": root, "pos": root.position})
		# The sculpted nose is unreadable from the high camera, so each statue
		# carries an oversized golden beak that makes its facing obvious.
		var beak := CylinderMesh.new()
		beak.top_radius = 0.0
		beak.bottom_radius = 0.6
		beak.height = 2.0
		var nose := _mesh(beak, Vector3(0, 2.4, 2.6), gold, 1.1, root)
		nose.rotation_degrees.x = 90.0
		var mark := _sphere(root.position + Vector3(0, 5.6, 0), 0.55, gold, 1.6)
		mark.visible = false
		statue_marks.append(mark)
	DungeonArt.spawn("pedestal", self, CENTER + Vector3(0, 0.7, 3.0))
	_sphere(CENTER + Vector3(0, 3.6, 3.0), 1.6, Color(1.0, 0.88, 0.35), 1.0)
	clue_pos = CENTER + Vector3(0, 9.0, 3.0)
	_refresh_statue_marks(false)

func _build_pair_props() -> void:
	var symbols: Array = config.get("cards", ["☾", "★", "☾", "★"])
	for i in range(symbols.size()):
		var pos := CENTER + Vector3((float(i % 2) - 0.5) * 11.0, 0.7, 3.0 - float(i / 2) * 9.0)
		var symbol_kind := "moon" if i % 2 == 0 else "star"
		var root := _add_pad(i, pos, "question", Color(0.48, 0.34, 0.72), ["question", symbol_kind])
		root.set_meta("symbol", String(symbols[i]))
		root.set_meta("symbol_kind", symbol_kind)
		var entry: Dictionary = interactives[interactives.size() - 1]
		card_labels.append(entry["picture"] as Node3D)
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
				DungeonArt.show_pictogram(card_labels[idx], "question")
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
	_tick_guidance(delta)
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
		if not _note_wrong():
			_gentle_hint()
		return
	_note_progress()
	_step_chime(step)
	if puzzle_kind == "path" and step < reveal_nodes.size():
		reveal_nodes[step].scale = Vector3.ONE
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
	idle_t = 0.0
	_refresh_statue_marks()
	var targets: Array = config.get("targets", [1, 0, 3])
	for i in range(values.size()):
		if values[i] != int(targets[i]):
			return
	_solve()

func _pair_action(choice: int) -> void:
	if choice in solved_pairs or choice < 0 or choice >= card_labels.size():
		return
	var card_root: Node3D = interactives[choice]["node"]
	DungeonArt.show_pictogram(card_labels[choice], String(card_root.get_meta("symbol_kind")))
	if selected < 0:
		selected = choice
		idle_t = 0.0
		_step_chime(0)
		return
	var first_root: Node3D = interactives[selected]["node"]
	if first_root.get_meta("symbol") == card_root.get_meta("symbol") and selected != choice:
		solved_pairs.append(selected)
		solved_pairs.append(choice)
		selected = -1
		_note_progress()
		_step_chime(2)
		if solved_pairs.size() == card_labels.size():
			_solve()
	else:
		# Keep both pictures visible long enough for a child to learn the mismatch.
		pair_hide = [selected, choice]
		pair_hide_t = 1.1
		selected = -1
		hint.text = "✨  LOOK AT BOTH PICTURES — THEN TRY AGAIN  ✨"
		if not _note_wrong():
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
	for i in range(clue_symbols.size()):
		clue_symbols[i].scale = Vector3.ONE * (1.1 if i < step else (2.4 if i == step else 1.8))

func _note_progress() -> void:
	idle_t = 0.0
	remind_stage = 0
	wrong_streak = 0
	guided = false

func _note_wrong() -> bool:
	idle_t = 0.0
	wrong_streak += 1
	if wrong_streak >= 2 and not guided:
		remind_stage = 2
		guided = true
		m.show_msg("Roshan", "Watch the golden arrow! Swim under it and tap USE!", "talk")
		return true
	return false

func _tick_guidance(delta: float) -> void:
	# Escalating stuck help: repeat the spoken objective, then drop into guided
	# mode where the golden arrow marks the exact next thing to tap. Guidance
	# only ever points — it never solves, so the win still belongs to the child.
	idle_t += delta
	if remind_stage == 0 and idle_t >= 10.0:
		remind_stage = 1
		m.show_msg("Roshan", String(config.get("voice", "Follow the pictures and golden sparkle!")), "talk")
	elif remind_stage == 1 and idle_t >= 20.0:
		remind_stage = 2
		guided = true
		m.show_msg("Roshan", "Watch the golden arrow! Swim under it and tap USE!", "talk")
	elif remind_stage == 2 and idle_t >= 32.0:
		idle_t = 20.0
		m.show_msg("Roshan", "The golden arrow shows the way — tap USE right under it!", "talk")
	pointer.position = _pointer_anchor() + Vector3(0, sin(Time.get_ticks_msec() * 0.004) * 0.35, 0)

func _pointer_anchor() -> Vector3:
	# Torch and statue rooms have no picture clue, so their arrow always marks
	# the next real target; picture rooms teach from the clue first and only
	# point at the answer pad once the child is stuck.
	if guided or puzzle_kind in ["torches", "rotate"]:
		var target := _guided_target()
		if target != Vector3.INF:
			return target + Vector3(0, 9.0, 0)
	match puzzle_kind:
		"sequence", "elemental":
			if step < clue_symbols.size():
				return clue_symbols[step].position + Vector3(0, 2.6, 0)
		"path":
			if step < reveal_nodes.size():
				return reveal_nodes[step].position + Vector3(0, 4.5, 0)
		"pairs":
			var idx := _pair_suggestion()
			for entry: Dictionary in interactives:
				if int(entry["index"]) == idx:
					return (entry["pos"] as Vector3) + Vector3(0, 6.0, 0)
	return clue_pos

func _pair_suggestion() -> int:
	for i in range(card_labels.size()):
		if i in solved_pairs or i == selected:
			continue
		return i
	return -1

func _guided_target() -> Vector3:
	var idx := -1
	match puzzle_kind:
		"sequence", "elemental", "path", "torches":
			var solution: Array = config.get("solution", [])
			if step < solution.size():
				idx = int(solution[step])
		"rotate":
			var targets: Array = config.get("targets", [1, 0, 3])
			for i in range(values.size()):
				if values[i] != int(targets[i]):
					idx = i
					break
		"pairs":
			if selected >= 0:
				var want := String((interactives[selected]["node"] as Node3D).get_meta("symbol"))
				for i in range(interactives.size()):
					if i != selected and i not in solved_pairs and String((interactives[i]["node"] as Node3D).get_meta("symbol")) == want:
						idx = i
						break
			else:
				idx = _pair_suggestion()
	for entry: Dictionary in interactives:
		if int(entry["index"]) == idx:
			return entry["pos"]
	return Vector3.INF

func _refresh_statue_marks(announce: bool = true) -> void:
	var targets: Array = config.get("targets", [1, 0, 3])
	for i in range(values.size()):
		var correct: bool = i < targets.size() and values[i] == int(targets[i])
		if i < statue_marks.size():
			statue_marks[i].visible = correct
		if announce and correct and not statue_done[i]:
			_step_chime(3)
		statue_done[i] = correct

func _solve() -> void:
	if state != "play":
		return
	state = "exit"
	objective.text = "★  THE WAY FORWARD IS OPEN!  ★"
	hint.text = "✨  SWIM THROUGH THE GOLDEN DOOR  ✨"
	pointer.position = CENTER + Vector3(0, 11.0, -24.0)
	if door != null:
		var tween := door.create_tween()
		tween.tween_property(door, "position:y", CENTER.y - 10.0, 0.75).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	m.show_msg("Roshan", "The golden door is open! Swim through!", "win")

func force_solve() -> void:
	_solve()

func cancel() -> void:
	# Opening the door is the earned completion moment. If the child taps Home
	# during the short celebration, checkpoint it instead of discarding it.
	if state == "exit":
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
