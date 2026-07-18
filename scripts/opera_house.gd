class_name OperaHouse
extends Node
# The Pearl Opera House (Peach Showtime-inspired): eight costume acts across
# two floors. Each floor runs three career shows and ends with a gentle boss
# showdown. OperaAct owns each performance; this class owns act order,
# checkpoints, the progress HUD and safe exits — mirroring DungeonLevel.

const ACTS := [
	# ---------- FLOOR 1: the Lagoon Lights Stage ----------
	{"name": "The Great Cake Show", "career": "Pastry Chef", "costume": "chef", "story": 1, "type": "show",
		"kind": "order", "props": "cake", "order": [0, 2, 1],
		"voice": "Chef hat on! Look at the recipe over the bowl — bring the cake layers up in that same order!",
		"win_line": "The show cake is PERFECT! Everybody wants a slice!",
		"floor_col": Color(0.72, 0.5, 0.62), "trim": Color(1.0, 0.78, 0.86), "curtain": Color(0.85, 0.3, 0.4)},
	{"name": "The Missing Tiara", "career": "Detective", "costume": "detective", "story": 1, "type": "show",
		"kind": "order", "props": "clue", "order": [1, 0, 2], "reveal_one": true,
		"voice": "Detective Roshan is on the case! Follow the sparkling clues one at a time and find the missing tiara!",
		"win_line": "Case closed! The tiara was in the treasure box all along!",
		"floor_col": Color(0.42, 0.46, 0.62), "trim": Color(0.72, 0.85, 1.0), "curtain": Color(0.3, 0.35, 0.6)},
	{"name": "The Dance Recital", "career": "Ballerina", "costume": "ballerina", "story": 1, "type": "show",
		"kind": "echo", "pads": 4, "rounds": [1, 2, 3], "pitch": 0.6,
		"voice": "Ballerina twirl! Watch the glowing dance tiles twinkle, then dance the same steps!",
		"win_line": "What a beautiful dance! The whole reef is clapping!",
		"floor_col": Color(0.62, 0.45, 0.72), "trim": Color(1.0, 0.72, 0.86), "curtain": Color(0.55, 0.3, 0.62)},
	{"name": "The Curtain Dragon", "career": "Sparkle Knight", "costume": "knight", "story": 1, "type": "boss",
		"kind": "boss", "boss_hp": 3, "peek_time": 4.5, "hide_time": 2.2,
		"voice": "A grumbly dragon is hiding in the curtains! Be brave — tap SPARKLE when he peeks out!",
		"win_line": "The dragon isn't grumbly anymore — he just wanted to be in the show!",
		"floor_col": Color(0.45, 0.3, 0.4), "trim": Color(1.0, 0.65, 0.4), "curtain": Color(0.62, 0.2, 0.28)},
	# ---------- FLOOR 2: the Starlight Balcony ----------
	{"name": "The Moonlight Aria", "career": "Opera Star", "costume": "singer", "story": 2, "type": "show",
		"kind": "echo", "pads": 3, "rounds": [1, 2, 3], "pitch": 0.9, "props": "bells",
		"voice": "Sing, Roshan, sing! Listen to the golden bells, then ring the very same song!",
		"win_line": "Bravissima! That was the prettiest song the opera has ever heard!",
		"floor_col": Color(0.35, 0.38, 0.66), "trim": Color(1.0, 0.88, 0.5), "curtain": Color(0.28, 0.24, 0.55)},
	{"name": "The Magic Hat Trick", "career": "Magician", "costume": "magician", "story": 2, "type": "show",
		"kind": "shuffle", "rounds": 2,
		"voice": "Abracadabra! Watch the bunny-fish hop under a hat, keep your eyes on it, then pick the right one!",
		"win_line": "Magic! The bunny-fish says you have the sharpest eyes in the sea!",
		"floor_col": Color(0.36, 0.3, 0.55), "trim": Color(0.85, 0.7, 1.0), "curtain": Color(0.4, 0.22, 0.6)},
	{"name": "Paint the Sunrise", "career": "Painter", "costume": "painter", "story": 2, "type": "show",
		"kind": "order", "props": "paint", "order": [2, 0, 1],
		"voice": "Painter Roshan! Look at the colors over the canvas — dip in the paint pots in that same order!",
		"win_line": "The sunrise backdrop is finished! It's a masterpiece!",
		"floor_col": Color(0.65, 0.5, 0.42), "trim": Color(1.0, 0.82, 0.55), "curtain": Color(0.75, 0.42, 0.3)},
	{"name": "The Shadow Phantom", "career": "Star Cape", "costume": "starcape", "story": 2, "type": "boss",
		"kind": "boss", "dual": true, "boss_hp": 3, "peek_time": 5.0, "hide_time": 2.0,
		"voice": "A shy shadow is hiding on the stage! Light the twinkling lantern with SHINE, then tap SPARKLE when he peeks!",
		"win_line": "The shadow was a lonely little phantom — now he's the star of the curtain call!",
		"floor_col": Color(0.24, 0.22, 0.42), "trim": Color(0.95, 0.9, 0.6), "curtain": Color(0.16, 0.14, 0.34)},
]

var m: ReefMain
var finish_cb: Callable
var act_index := 0
var act: OperaAct = null
var hud: CanvasLayer = null
var progress_label: Label = null
var act_label: Label = null
var state := "active"

func start(main: ReefMain, checkpoint: int, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	act_index = 0 if checkpoint >= ACTS.size() else clampi(checkpoint, 0, ACTS.size() - 1)
	_build_hud()
	_update_hud()
	call_deferred("_begin_act")

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 16
	add_child(hud)
	var strip := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.03, 0.1, 0.9)
	style.border_color = Color(1.0, 0.82, 0.5)
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
	act_label = Label.new()
	act_label.position = Vector2(30, 620)
	act_label.size = Vector2(205, 70)
	act_label.add_theme_font_size_override("font_size", 23)
	act_label.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	act_label.add_theme_constant_override("outline_size", 7)
	act_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	act_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	act_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	act_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(act_label)
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
	for i in range(ACTS.size()):
		if i == 4:
			marks += "‖ "   # the staircase between the two floors
		if i < act_index:
			marks += "★ "
		elif i == act_index:
			marks += "◆ "
		else:
			marks += "◇ "
	progress_label.text = marks.strip_edges()
	var cfg: Dictionary = ACTS[act_index]
	act_label.text = "%s\nFloor %d — %d / %d" % [String(cfg["career"]), int(cfg["story"]), act_index + 1, ACTS.size()]

func _begin_act() -> void:
	if state != "active" or act != null:
		return
	var cfg: Dictionary = ACTS[act_index].duplicate()
	cfg["act_tag"] = "ACT %d / %d" % [act_index + 1, ACTS.size()]
	# announce the costume first so the act's own instruction line lands last
	m.show_msg("Roshan", "%s! Costume time — %s Roshan!" % [String(cfg["name"]), String(cfg["career"])], "talk")
	act = OperaAct.new()
	add_child(act)
	act.start(m, cfg, Callable(self, "_act_won"))

func _act_won() -> void:
	act = null
	act_index += 1
	m.opera_progress = maxi(m.opera_progress, act_index)
	m.pearl_count += 3
	m._write_save()
	m._update_hud()
	if act_index >= ACTS.size():
		_complete_opera()
		return
	_update_hud()
	call_deferred("_begin_act")

func _complete_opera() -> void:
	state = "celebrate"
	if not m.opera_done:
		m.opera_done = true
		m.pearl_count += 50
		m.award_sticker("showtime")
	m.opera_progress = ACTS.size()
	m._write_save()
	m._update_hud()
	progress_label.text = "★ ★ ★ ★ ‖ ★ ★ ★ ★"
	act_label.text = "OPERA\nSTAR!"
	m.show_msg("Roshan", "Every show, every costume, both floors! Take a bow, Opera Star Roshan!", "win")
	var timer := get_tree().create_timer(3.0)
	timer.timeout.connect(func() -> void: _finish(true))

func _leave_early() -> void:
	if state == "celebrate":
		_finish(true)
		return
	if state != "active":
		return
	state = "leaving"
	if act != null:
		# an act in mid-performance is a checkpoint, not a win; an act already
		# taking its bow still reports completion through OperaAct._finish()
		act.cancel()
		act = null
	var completed: bool = m.opera_done
	m.show_msg("Roshan", "The whole opera sparkles!" if completed else "Checkpoint saved! The stage will wait for our next show.", "win" if completed else "home")
	_finish(completed)

func _finish(completed: bool) -> void:
	if state == "done":
		return
	state = "done"
	if finish_cb.is_valid():
		finish_cb.call(completed)
	queue_free()

func action_label() -> String:
	if act != null:
		return act.action_label()
	return "READY"
