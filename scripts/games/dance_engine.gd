class_name DanceEngine
extends CanvasLayer
# A self-contained, touch-first rhythm playground. The chart is generated from
# beat numbers, while note movement/judgement follows the AudioServer clock so
# a slow mobile frame cannot make the arrows drift away from the song.

signal closed

const SONGS := [
	{"track": "melody", "title": "Rainbow Stage", "bpm": 108.0, "offset": 0.18},
	{"track": "race", "title": "Rainbow Race", "bpm": 126.0, "offset": 0.12},
	{"track": "finale", "title": "Reef Celebration", "bpm": 116.0, "offset": 0.20},
]
const ARROWS := ["←", "↓", "↑", "→"]
const LANE_COLORS := [
	Color(0.36, 0.78, 1.0),
	Color(1.0, 0.56, 0.78),
	Color(0.55, 0.94, 0.62),
	Color(1.0, 0.83, 0.34),
]
const HIT_WINDOW := 0.46
const TRAVEL_TIME := 2.55
const ROUND_BEATS := 40

var main: ReefMain
var root: Control
var song_player: AudioStreamPlayer
var chime_player: AudioStreamPlayer
var title_label: Label
var prompt_label: Label
var magic_label: Label
var song_label: Label
var lane_buttons: Array[Button] = []
var lane_glows: Array[Panel] = []
var notes: Array[Dictionary] = []
var song_index := 0
var song_time := 0.0
var round_end := 0.0
var happy_hits := 0
var combo := 0
var best_combo := 0   # longest unbroken streak this round — the dance medal ranks on it
var active := false
var finishing := false
var guest_mode := false   # opera guest spot: the first happy round auto-closes
                          # instead of looping, so the act can take its bow
var prior_paused := false
var prior_stream: AudioStream = null
var prior_music_position := 0.0
var prior_music_playing := false
var pulse_t := 0.0
var chart_generation := 0


func _init(reef_main: ReefMain) -> void:
	main = reef_main
	layer = 40
	process_mode = Node.PROCESS_MODE_ALWAYS
	_build_ui()
	visible = false


func _build_ui() -> void:
	root = Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.process_mode = Node.PROCESS_MODE_ALWAYS
	add_child(root)

	var bg := ColorRect.new()
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.035, 0.075, 0.18, 0.97)
	bg.mouse_filter = Control.MOUSE_FILTER_STOP
	root.add_child(bg)

	# Pastel lane bands make direction readable even before the arrow glyphs.
	for lane in range(4):
		var band := ColorRect.new()
		band.name = "Lane%d" % lane
		band.color = Color(LANE_COLORS[lane], 0.085)
		band.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(band)

	var top_bar := Panel.new()
	top_bar.position = Vector2(24, 18)
	top_bar.size = Vector2(1232, 92)
	var top_style := StyleBoxFlat.new()
	top_style.bg_color = Color(0.1, 0.16, 0.34, 0.96)
	top_style.border_color = Color(0.48, 0.86, 1.0, 0.65)
	top_style.set_border_width_all(3)
	top_style.set_corner_radius_all(34)
	top_bar.add_theme_stylebox_override("panel", top_style)
	root.add_child(top_bar)

	var prev_song := Button.new()
	prev_song.text = "♫  ◀"
	prev_song.position = Vector2(20, 12)
	prev_song.size = Vector2(150, 68)
	prev_song.add_theme_font_size_override("font_size", 30)
	prev_song.pressed.connect(_change_song.bind(-1))
	top_bar.add_child(prev_song)

	song_label = Label.new()
	song_label.position = Vector2(186, 10)
	song_label.size = Vector2(860, 72)
	song_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	song_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	song_label.add_theme_font_size_override("font_size", 34)
	song_label.add_theme_color_override("font_color", Color(0.92, 0.98, 1.0))
	top_bar.add_child(song_label)

	var next_song := Button.new()
	next_song.text = "▶  ♫"
	next_song.position = Vector2(1062, 12)
	next_song.size = Vector2(150, 68)
	next_song.add_theme_font_size_override("font_size", 30)
	next_song.pressed.connect(_change_song.bind(1))
	top_bar.add_child(next_song)

	var close_button := Button.new()
	close_button.text = "✕"
	close_button.position = Vector2(1190, 124)
	close_button.size = Vector2(66, 66)
	close_button.add_theme_font_size_override("font_size", 30)
	close_button.pressed.connect(close_demo)
	root.add_child(close_button)

	prompt_label = Label.new()
	prompt_label.text = "Tap the matching arrows!"
	prompt_label.position = Vector2(180, 116)
	prompt_label.size = Vector2(920, 52)
	prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt_label.add_theme_font_size_override("font_size", 28)
	prompt_label.add_theme_color_override("font_color", Color(1.0, 0.93, 0.66))
	root.add_child(prompt_label)

	magic_label = Label.new()
	magic_label.position = Vector2(180, 164)
	magic_label.size = Vector2(920, 45)
	magic_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	magic_label.add_theme_font_size_override("font_size", 24)
	magic_label.add_theme_color_override("font_color", Color(1.0, 0.62, 0.84))
	root.add_child(magic_label)

	# Buttons are deliberately much larger than their art. A four-year-old can
	# press anywhere in the colored target, one finger at a time.
	for lane in range(4):
		var glow := Panel.new()
		glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var glow_style := StyleBoxFlat.new()
		glow_style.bg_color = Color(LANE_COLORS[lane], 0.18)
		glow_style.border_color = Color(LANE_COLORS[lane], 0.8)
		glow_style.set_border_width_all(7)
		glow_style.set_corner_radius_all(38)
		glow.add_theme_stylebox_override("panel", glow_style)
		root.add_child(glow)
		lane_glows.append(glow)

		var button := Button.new()
		button.text = ARROWS[lane]
		button.focus_mode = Control.FOCUS_NONE
		button.add_theme_font_size_override("font_size", 76)
		button.add_theme_color_override("font_color", Color.WHITE)
		button.add_theme_color_override("font_pressed_color", LANE_COLORS[lane].lightened(0.35))
		var normal := StyleBoxFlat.new()
		normal.bg_color = Color(LANE_COLORS[lane], 0.48)
		normal.border_color = LANE_COLORS[lane].lightened(0.2)
		normal.set_border_width_all(5)
		normal.set_corner_radius_all(32)
		button.add_theme_stylebox_override("normal", normal)
		var pressed := normal.duplicate() as StyleBoxFlat
		pressed.bg_color = LANE_COLORS[lane].lightened(0.18)
		pressed.expand_margin_left = 8.0
		pressed.expand_margin_right = 8.0
		pressed.expand_margin_top = 8.0
		pressed.expand_margin_bottom = 8.0
		button.add_theme_stylebox_override("pressed", pressed)
		button.pressed.connect(_press_lane.bind(lane))
		root.add_child(button)
		lane_buttons.append(button)

	title_label = Label.new()
	title_label.position = Vector2(140, 300)
	title_label.size = Vector2(1000, 120)
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	title_label.add_theme_font_size_override("font_size", 54)
	title_label.add_theme_color_override("font_color", Color(1.0, 0.9, 0.45))
	title_label.visible = false
	title_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(title_label)

	song_player = AudioStreamPlayer.new()
	song_player.bus = "Music"
	song_player.process_mode = Node.PROCESS_MODE_ALWAYS
	root.add_child(song_player)
	chime_player = AudioStreamPlayer.new()
	chime_player.bus = "SFX"
	chime_player.process_mode = Node.PROCESS_MODE_ALWAYS
	chime_player.stream = load("res://assets/audio/chime.ogg")
	chime_player.volume_db = -5.0
	root.add_child(chime_player)
func open_demo() -> void:
	if active:
		return
	prior_paused = get_tree().paused
	prior_stream = main.music.stream
	prior_music_position = main.music.get_playback_position()
	prior_music_playing = main.music.playing
	main.music.stop()
	get_tree().paused = true
	active = true
	visible = true
	_start_song()
	_say_dance("talk")


func close_demo() -> void:
	if not active:
		return
	active = false
	visible = false
	song_player.stop()
	_clear_notes()
	if prior_stream != null:
		main.music.stream = prior_stream
		if prior_music_playing:
			main.music.play(prior_music_position)
	main.music.volume_db = -8.0 if main.music_on else -60.0
	get_tree().paused = prior_paused
	closed.emit()


func _change_song(direction: int) -> void:
	if not active:
		return
	song_index = posmod(song_index + direction, SONGS.size())
	_start_song()


func _start_song() -> void:
	chart_generation += 1
	_clear_notes()
	happy_hits = 0
	combo = 0
	best_combo = 0
	finishing = false
	title_label.visible = false
	prompt_label.text = "Tap the matching arrows!"
	_update_magic()
	var song: Dictionary = SONGS[song_index]
	song_label.text = "♫  %s  ♫" % String(song["title"])
	var stream: AudioStream = load("res://assets/audio/music/%s.ogg" % String(song["track"]))
	if stream is AudioStreamOggVorbis:
		(stream as AudioStreamOggVorbis).loop = true
	song_player.stream = stream
	song_player.volume_db = -8.0 if main.music_on else -60.0
	song_player.play()
	song_time = 0.0
	_build_chart()
	var beat_len: float = 60.0 / float(song["bpm"])
	round_end = float(song["offset"]) + float(ROUND_BEATS + 6) * beat_len


func _build_chart() -> void:
	var song: Dictionary = SONGS[song_index]
	var beat_len: float = 60.0 / float(song["bpm"])
	var offset: float = float(song["offset"])
	# Four simple repeating phrases. They are intentionally learnable and use
	# only single notes: this interface never demands two-finger chords.
	var phrases := [
		[0, 1, 2, 3, 0, 2, 1, 3],
		[0, 0, 1, 2, 2, 1, 3, 3],
		[3, 2, 1, 0, 1, 3, 2, 0],
		[0, 2, 0, 3, 1, 3, 1, 2],
	]
	var pattern: Array = phrases[song_index % phrases.size()]
	for i in range(ROUND_BEATS):
		# First four beats are a calm count-in; later phrases add occasional
		# half-beat notes while preserving the one-note-at-a-time rule.
		var beat := 4.0 + float(i)
		_add_note(int(pattern[i % pattern.size()]), offset + beat * beat_len)
		if i >= 12 and i % 8 == 6:
			_add_note(int(pattern[(i + 3) % pattern.size()]), offset + (beat + 0.5) * beat_len)


func _add_note(lane: int, hit_time: float) -> void:
	var note := Label.new()
	note.text = ARROWS[lane]
	note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	note.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	note.add_theme_font_size_override("font_size", 72)
	note.add_theme_color_override("font_color", LANE_COLORS[lane].lightened(0.24))
	note.add_theme_color_override("font_outline_color", Color(0.05, 0.08, 0.2))
	note.add_theme_constant_override("outline_size", 12)
	note.mouse_filter = Control.MOUSE_FILTER_IGNORE
	note.visible = false
	root.add_child(note)
	note.move_to_front()
	notes.append({"lane": lane, "time": hit_time, "node": note, "judged": false})


func _clear_notes() -> void:
	for data in notes:
		var note: Label = data["node"]
		if is_instance_valid(note):
			note.queue_free()
	notes.clear()


func _process(delta: float) -> void:
	if not active:
		return
	pulse_t += delta
	_layout_lanes()
	var clock := _song_clock(delta)
	for data in notes:
		_update_note(data, clock)
	if not finishing and clock >= round_end:
		_finish_round()
	for lane in range(lane_glows.size()):
		var glow: Panel = lane_glows[lane]
		var breathe := 1.0 + sin(pulse_t * 2.4 + float(lane) * 0.7) * 0.025
		glow.scale = Vector2.ONE * breathe


func _song_clock(delta: float) -> float:
	# get_playback_position is mix-buffer based. Adding time since the last mix
	# and subtracting device latency gives the time the child actually hears.
	if song_player.playing:
		var heard: float = song_player.get_playback_position()
		heard += AudioServer.get_time_since_last_mix()
		heard -= AudioServer.get_output_latency()
		song_time = maxf(song_time, heard)
	else:
		# Headless/audio-less environments still animate deterministically.
		song_time += delta
	return song_time


func _layout_lanes() -> void:
	var view := get_viewport().get_visible_rect().size
	var left := maxf(30.0, view.x * 0.10)
	var usable := view.x - left * 2.0
	var lane_width := usable / 4.0
	var target_y := view.y - 178.0
	for lane in range(4):
		var x := left + float(lane) * lane_width
		var band: ColorRect = root.get_node("Lane%d" % lane)
		band.position = Vector2(x + 7.0, 218.0)
		band.size = Vector2(lane_width - 14.0, maxf(120.0, view.y - 218.0))
		var button: Button = lane_buttons[lane]
		button.position = Vector2(x + 12.0, target_y)
		button.size = Vector2(lane_width - 24.0, 148.0)
		var glow: Panel = lane_glows[lane]
		glow.position = button.position - Vector2(8, 8)
		glow.size = button.size + Vector2(16, 16)
		glow.pivot_offset = glow.size * 0.5


func _update_note(data: Dictionary, clock: float) -> void:
	var note: Label = data["node"]
	if bool(data["judged"]):
		note.visible = false
		return
	var until: float = float(data["time"]) - clock
	if until > TRAVEL_TIME:
		note.visible = false
		return
	if until < -HIT_WINDOW:
		data["judged"] = true
		note.visible = false
		combo = 0
		return
	var view := get_viewport().get_visible_rect().size
	var left := maxf(30.0, view.x * 0.10)
	var lane_width := (view.x - left * 2.0) / 4.0
	var target_y := view.y - 178.0
	var start_y := 218.0
	var progress := clampf(1.0 - until / TRAVEL_TIME, 0.0, 1.2)
	var lane := int(data["lane"])
	note.position = Vector2(left + float(lane) * lane_width + lane_width * 0.5 - 58.0, lerpf(start_y, target_y + 18.0, progress))
	note.size = Vector2(116, 116)
	note.visible = true
	var near_scale := 1.0 + maxf(0.0, 1.0 - absf(until) / HIT_WINDOW) * 0.18
	note.scale = Vector2.ONE * near_scale
	note.pivot_offset = note.size * 0.5


func _press_lane(lane: int) -> void:
	if not active or finishing:
		return
	var clock: float = _song_clock(0.0)
	var best: Dictionary = {}
	var best_distance := HIT_WINDOW + 0.001
	for data in notes:
		if bool(data["judged"]) or int(data["lane"]) != lane:
			continue
		var distance := absf(float(data["time"]) - clock)
		if distance < best_distance:
			best_distance = distance
			best = data
	_flash_lane(lane, best.is_empty())
	if best.is_empty():
		# Exploratory taps are welcome: no buzz, score loss, or fail state.
		prompt_label.text = "Follow the floating arrow!"
		return
	best["judged"] = true
	var note: Label = best["node"]
	note.visible = false
	happy_hits += 1
	combo += 1
	best_combo = maxi(best_combo, combo)
	prompt_label.text = ["Lovely!", "Sparkly!", "Great dancing!", "Keep going!"][happy_hits % 4]
	_update_magic()
	chime_player.pitch_scale = 0.92 + float(lane) * 0.09 + minf(float(combo), 8.0) * 0.015
	chime_player.play()
	_pop_feedback(lane)


func _flash_lane(lane: int, exploratory: bool) -> void:
	var button: Button = lane_buttons[lane]
	var original := button.modulate
	button.modulate = Color(0.82, 0.9, 1.0) if exploratory else Color.WHITE * 1.35
	var tween := button.create_tween()
	tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	tween.tween_property(button, "modulate", original, 0.20)


func _pop_feedback(lane: int) -> void:
	var heart := Label.new()
	heart.text = ["♥", "★", "✦"][happy_hits % 3]
	heart.add_theme_font_size_override("font_size", 68)
	heart.add_theme_color_override("font_color", LANE_COLORS[lane].lightened(0.25))
	heart.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var button: Button = lane_buttons[lane]
	heart.position = button.position + Vector2(button.size.x * 0.5 - 28.0, -10.0)
	heart.size = Vector2(70, 70)
	root.add_child(heart)
	heart.move_to_front()
	var tween := heart.create_tween()
	tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	tween.tween_property(heart, "position:y", heart.position.y - 145.0, 0.65).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.parallel().tween_property(heart, "modulate:a", 0.0, 0.65)
	tween.tween_callback(heart.queue_free)


func _update_magic() -> void:
	var hearts: int = mini(int(happy_hits / 4), 8)
	magic_label.text = "Dance magic  " + "♥".repeat(hearts) + "♡".repeat(8 - hearts)


func _finish_round() -> void:
	finishing = true
	if happy_hits > 0:
		title_label.text = "DANCE PARTY!  ★"
		prompt_label.text = "You made rainbow dance magic!"
		title_label.visible = true
		_say_dance("win")
		# a danced round is a completed round — rank the streak (loops forever,
		# so every round is another shot at gold)
		main._medal_ref().award_stats("dance", {"combo": best_combo, "hits": happy_hits})
		for lane in range(4):
			_pop_feedback(lane)
	else:
		title_label.text = "THE MUSIC IS WAITING  ♫"
		prompt_label.text = "Tap any floating arrow to join!"
		title_label.visible = true
	if guest_mode and happy_hits > 0:
		get_tree().create_timer(2.4, true).timeout.connect(_close_if_active)
	else:
		get_tree().create_timer(2.4, true).timeout.connect(_restart_round.bind(chart_generation))


func _restart_round(generation: int) -> void:
	if active and generation == chart_generation:
		_start_song()


func _close_if_active() -> void:
	if active:
		close_demo()


func _say_dance(event: String) -> void:
	# Objectives use the same family-voice pipeline as every other game. Voice
	# players process through the paused dance overlay so the cue is never lost.
	for player in main.voice_pool:
		(player as AudioStreamPlayer).process_mode = Node.PROCESS_MODE_ALWAYS
	main._say("gabby", event)


func _unhandled_input(event: InputEvent) -> void:
	if not active:
		return
	if event is InputEventKey:
		var key := event as InputEventKey
		if not key.pressed or key.echo:
			return
		match key.keycode:
			KEY_LEFT:
				_press_lane(0)
			KEY_DOWN:
				_press_lane(1)
			KEY_UP:
				_press_lane(2)
			KEY_RIGHT:
				_press_lane(3)
			KEY_ESCAPE:
				close_demo()
		get_viewport().set_input_as_handled()
	elif event is InputEventJoypadButton:
		var joy := event as InputEventJoypadButton
		if not joy.pressed:
			return
		match joy.button_index:
			JOY_BUTTON_DPAD_LEFT:
				_press_lane(0)
			JOY_BUTTON_DPAD_DOWN:
				_press_lane(1)
			JOY_BUTTON_DPAD_UP:
				_press_lane(2)
			JOY_BUTTON_DPAD_RIGHT:
				_press_lane(3)
			JOY_BUTTON_B:
				close_demo()
		get_viewport().set_input_as_handled()
