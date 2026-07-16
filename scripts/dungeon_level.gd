class_name DungeonLevel
extends Node
# Ten-room adventure dungeon. CombatArena owns battles, DungeonPuzzleRoom owns
# visual puzzles, and this class owns room order, checkpoints and safe exits.

const ROOMS := [
	{"name": "Frozen Foyer", "type": "combat", "kind": "ice", "enemy_count": 4, "layout": "ring", "imp_speed": 1.1, "attack_gap": 3.8, "popcorn_count": 5, "win_spark_gap": 0.4, "floor": Color(0.52, 0.66, 0.84), "trim": Color(0.7, 0.95, 1.0)},
	{"name": "Crystal Chimes", "type": "puzzle", "puzzle": "sequence", "choices": ["◆", "●", "▲"], "solution": [0, 2, 1], "choice_count": 3, "voice": "Look at the three big crystal pictures. Swim to those crystal pads in the same order!", "floor": Color(0.38, 0.48, 0.72), "trim": Color(0.75, 0.68, 1.0)},
	{"name": "Frozen River", "type": "puzzle", "puzzle": "path", "solution": [0, 1, 1, 0], "voice": "The tiny ice stones show a path. Swim to the left or right arrow and freeze each step!", "floor": Color(0.28, 0.55, 0.72), "trim": Color(0.58, 0.96, 1.0)},
	{"name": "Popcorn Ambush", "type": "combat", "kind": "ice", "enemy_count": 6, "layout": "spiral", "imp_speed": 1.45, "attack_gap": 3.3, "popcorn_count": 5, "win_spark_gap": 0.4, "floor": Color(0.46, 0.43, 0.7), "trim": Color(0.78, 0.72, 1.0)},
	{"name": "Pepper Lanterns", "type": "puzzle", "puzzle": "torches", "solution": [1, 3, 0, 2], "voice": "Swim to the pepper lanterns and light them from shortest to tallest!", "floor": Color(0.5, 0.28, 0.2), "trim": Color(1.0, 0.58, 0.25)},
	{"name": "Turtle Gallery", "type": "puzzle", "puzzle": "rotate", "targets": [1, 0, 3], "voice": "Swim to each shell statue. Turn every golden nose toward the pearl!", "floor": Color(0.3, 0.52, 0.44), "trim": Color(0.65, 0.94, 0.62)},
	{"name": "Claw Guardian", "type": "combat", "kind": "fire", "boss_hp": 4, "peek_time": 4.8, "shell_time": 2.5, "shell_speed": 5.0, "attack_gap": 1.4, "floor": Color(0.56, 0.24, 0.24), "trim": Color(1.0, 0.48, 0.35)},
	{"name": "Moon Rune Vault", "type": "puzzle", "puzzle": "pairs", "cards": ["☾", "★", "☾", "★"], "button_count": 4, "voice": "Peek under two moon tiles. Find the pictures that match!", "floor": Color(0.28, 0.3, 0.58), "trim": Color(0.72, 0.7, 1.0)},
	{"name": "Elemental Door", "type": "puzzle", "puzzle": "elemental", "choices": ["❄", "🔥"], "solution": [0, 1, 0, 0, 1], "button_count": 2, "voice": "The big door shows ice and fire. Copy its magic picture order!", "floor": Color(0.4, 0.32, 0.5), "trim": Color(1.0, 0.72, 0.4)},
	{"name": "Dragon-Turtle Throne", "type": "combat", "kind": "dual", "dual_phase": true, "boss_hp": 4, "peek_time": 3.2, "shell_time": 5.0, "shell_speed": 5.2, "attack_gap": 1.25, "win_spark_gap": 0.4, "floor": Color(0.42, 0.16, 0.18), "trim": Color(1.0, 0.4, 0.18)},
]

var m: ReefMain
var finish_cb: Callable
var room_index := 0
var arena: CombatArena = null
var puzzle: DungeonPuzzleRoom = null
var hud: CanvasLayer = null
var progress_label: Label = null
var room_label: Label = null
var state := "active"

func start(main: ReefMain, checkpoint: int, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	room_index = 0 if checkpoint >= ROOMS.size() else clampi(checkpoint, 0, ROOMS.size() - 1)
	_build_hud()
	_update_hud()
	call_deferred("_begin_room")

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 16
	add_child(hud)
	var strip := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.035, 0.045, 0.12, 0.9)
	style.border_color = Color(0.78, 0.66, 1.0)
	style.set_border_width_all(3)
	style.set_corner_radius_all(20)
	strip.add_theme_stylebox_override("panel", style)
	strip.position = Vector2(245, 612)
	strip.size = Vector2(790, 88)
	strip.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(strip)
	progress_label = Label.new()
	progress_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	progress_label.add_theme_font_size_override("font_size", 31)
	progress_label.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	progress_label.add_theme_constant_override("outline_size", 7)
	progress_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	progress_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	progress_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	strip.add_child(progress_label)
	room_label = Label.new()
	room_label.position = Vector2(30, 620)
	room_label.size = Vector2(205, 70)
	room_label.add_theme_font_size_override("font_size", 25)
	room_label.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	room_label.add_theme_constant_override("outline_size", 7)
	room_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	room_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	room_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	room_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(room_label)
	var home := Button.new()
	home.text = "⌂"
	home.position = Vector2(1138, 24)
	home.size = Vector2(112, 100)
	home.add_theme_font_size_override("font_size", 58)
	var home_style := StyleBoxFlat.new()
	home_style.bg_color = Color(0.2, 0.18, 0.38, 0.94)
	home_style.border_color = Color(1.0, 0.86, 0.5)
	home_style.set_border_width_all(4)
	home_style.set_corner_radius_all(28)
	home.add_theme_stylebox_override("normal", home_style)
	home.add_theme_stylebox_override("hover", home_style)
	home.add_theme_stylebox_override("pressed", home_style)
	home.pressed.connect(_leave_early)
	hud.add_child(home)

func _update_hud() -> void:
	if progress_label == null:
		return
	var marks := ""
	for i in range(ROOMS.size()):
		if i < room_index:
			marks += "★ "
		elif i == room_index:
			marks += "◆ "
		else:
			marks += "◇ "
	progress_label.text = marks.strip_edges()
	var room: Dictionary = ROOMS[room_index]
	room_label.text = "%s\n%d / %d" % [String(room["name"]), room_index + 1, ROOMS.size()]

func _begin_room() -> void:
	if state != "active" or arena != null or puzzle != null:
		return
	var room: Dictionary = ROOMS[room_index].duplicate()
	room["room_tag"] = "ROOM %d / %d" % [room_index + 1, ROOMS.size()]
	room["win_time"] = 1.4
	if String(room.get("type", "combat")) == "combat":
		arena = CombatArena.new()
		add_child(arena)
		arena.start(m, String(room["kind"]), Callable(self, "_combat_won"), room)
	else:
		puzzle = DungeonPuzzleRoom.new()
		add_child(puzzle)
		puzzle.start(m, room, Callable(self, "_puzzle_won"))
	m.show_msg("Roshan", "%s! Room %d of %d — follow the golden sparkle!" % [String(room["name"]), room_index + 1, ROOMS.size()], "talk")

func _combat_won(_battle_kind: String) -> void:
	arena = null
	_room_won()

func _puzzle_won() -> void:
	puzzle = null
	_room_won()

func _room_won() -> void:
	room_index += 1
	m.dungeon_progress = maxi(m.dungeon_progress, room_index)
	m.pearl_count += 3
	m._write_save()
	m._update_hud()
	if room_index >= ROOMS.size():
		_complete_dungeon()
		return
	_update_hud()
	call_deferred("_begin_room")

func _complete_dungeon() -> void:
	state = "celebrate"
	if not m.dungeon_done:
		m.dungeon_done = true
		m.pearl_count += 50
	m.dungeon_progress = ROOMS.size()
	m._write_save()
	m._update_hud()
	progress_label.text = "★ ★ ★ ★ ★ ★ ★ ★ ★ ★"
	room_label.text = "DUNGEON\nHERO!"
	m.show_msg("Roshan", "All ten rooms! The dungeon is sparkling and safe!", "win")
	var timer := get_tree().create_timer(3.0)
	timer.timeout.connect(func(): _finish(true))

func _leave_early() -> void:
	if state != "active":
		return
	state = "leaving"
	if arena != null:
		arena.cancel()
		arena = null
	if puzzle != null:
		puzzle.cancel()
		puzzle = null
	m.show_msg("Roshan", "Checkpoint saved! We can come back to the next room any time.", "home")
	_finish(false)

func _finish(completed: bool) -> void:
	if state == "done":
		return
	state = "done"
	if finish_cb.is_valid():
		finish_cb.call(completed)
	queue_free()

func action_label() -> String:
	if arena != null:
		return arena.action_label()
	if puzzle != null:
		return "USE"
	return "READY"
