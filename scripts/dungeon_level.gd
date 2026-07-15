class_name DungeonLevel
extends Node
# Ten-room campaign wrapper around CombatArena. The arena remains the sole
# combat engine; this class owns room order, checkpoint saves and the safe exit.

const ROOMS := [
	{"name": "Frozen Foyer", "kind": "ice", "enemy_count": 4, "layout": "ring", "imp_speed": 1.1, "attack_gap": 3.8, "floor": Color(0.52, 0.66, 0.84), "trim": Color(0.7, 0.95, 1.0)},
	{"name": "Berry Barracks", "kind": "ice", "enemy_count": 5, "layout": "double", "imp_speed": 1.3, "attack_gap": 3.5, "floor": Color(0.42, 0.55, 0.78), "trim": Color(0.62, 0.86, 1.0)},
	{"name": "Spiral Pantry", "kind": "ice", "enemy_count": 6, "layout": "spiral", "imp_speed": 1.4, "attack_gap": 3.3, "floor": Color(0.48, 0.45, 0.72), "trim": Color(0.78, 0.72, 1.0)},
	{"name": "Pepper Guard", "kind": "fire", "boss_hp": 3, "peek_time": 5.2, "shell_time": 2.2, "shell_speed": 4.5, "floor": Color(0.52, 0.29, 0.20), "trim": Color(1.0, 0.58, 0.25)},
	{"name": "Crystal Crossing", "kind": "ice", "enemy_count": 7, "layout": "double", "imp_speed": 1.55, "attack_gap": 3.1, "floor": Color(0.34, 0.58, 0.70), "trim": Color(0.5, 1.0, 0.92)},
	{"name": "Claw Gallery", "kind": "fire", "boss_hp": 4, "peek_time": 4.8, "shell_time": 2.5, "shell_speed": 5.0, "attack_gap": 1.4, "floor": Color(0.56, 0.24, 0.24), "trim": Color(1.0, 0.48, 0.35)},
	{"name": "Snowflake Vault", "kind": "ice", "enemy_count": 8, "layout": "spiral", "imp_speed": 1.7, "attack_gap": 2.9, "floor": Color(0.40, 0.50, 0.76), "trim": Color(0.8, 0.9, 1.0)},
	{"name": "Ember Shell Hall", "kind": "fire", "boss_hp": 5, "peek_time": 4.4, "shell_time": 2.7, "shell_speed": 5.4, "attack_gap": 1.2, "floor": Color(0.48, 0.20, 0.16), "trim": Color(1.0, 0.66, 0.18)},
	{"name": "Popcorn Gauntlet", "kind": "ice", "enemy_count": 10, "layout": "double", "imp_speed": 1.85, "attack_gap": 2.7, "floor": Color(0.40, 0.42, 0.68), "trim": Color(0.72, 0.78, 1.0)},
	{"name": "Dragon-Turtle Throne", "kind": "fire", "boss_hp": 9, "peek_time": 4.0, "shell_time": 3.0, "shell_speed": 5.8, "attack_gap": 1.0, "floor": Color(0.42, 0.16, 0.18), "trim": Color(1.0, 0.40, 0.18)},
]

var m: ReefMain
var finish_cb: Callable
var room_index := 0
var arena: CombatArena = null
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
	hud.add_child(strip)
	progress_label = Label.new()
	progress_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	progress_label.add_theme_font_size_override("font_size", 31)
	progress_label.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	progress_label.add_theme_constant_override("outline_size", 7)
	progress_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	progress_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
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
	if state != "active" or arena != null:
		return
	var room: Dictionary = ROOMS[room_index].duplicate()
	room["room_tag"] = "ROOM %d / %d" % [room_index + 1, ROOMS.size()]
	room["win_time"] = 1.4
	arena = CombatArena.new()
	add_child(arena)
	arena.start(m, String(room["kind"]), Callable(self, "_room_won"), room)
	m.show_msg("Roshan", "%s! Room %d of %d — follow the golden arrow!" % [String(room["name"]), room_index + 1, ROOMS.size()], "dungeon_room")

func _room_won(_battle_kind: String) -> void:
	arena = null
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
	m.show_msg("Roshan", "All TEN rooms! The dungeon is sparkling and safe!", "win")
	var timer := get_tree().create_timer(3.0)
	timer.timeout.connect(func(): _finish(true))

func _leave_early() -> void:
	if state != "active":
		return
	state = "leaving"
	if arena != null:
		arena.cancel()
		arena = null
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
	if arena == null:
		return "READY"
	return "ICE" if arena.kind == "ice" else "FIRE"
