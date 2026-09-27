extends Control
## Isolated review prototype. Never writes the production reef save.
## Static instrument cutouts are gameplay candidates, never cinematic pixels.
const DESIGN := Vector2(1280, 720)
const PATTERN := [0, 1, 0, 2, 1, 0, 2, 0, 1, 2, 0, 2]
const DRUMS := [Vector2(425, 390), Vector2(535, 390), Vector2(646, 355)]
const SAVE_PATH := "user://battle_of_bands_prototype.cfg"
@export var recording: AudioStream = preload("res://assets/prototypes/bands/iko_iko_v89.ogg")
@export var king_outburst_cues: Array[Vector2] = [Vector2(25.303105, 31.061953), Vector2(83.059965, 88.359965)] ## Recording seconds: start/end.
@export var prince_outburst_cues: Array[Vector2] = [Vector2(48.268411, 54.027259), Vector2(83.059965, 88.359965)]
@export var persist_progress := true
@export var progress_path := SAVE_PATH
var resume_seconds := 0.0
var song_finished := false
var hits := 0
var story_step := 0
var elapsed := 0.0
var flash := 0.0
var last_drum := -1
var suspended := false
var touch_owner := -1
var actor: TextureRect
var king: TextureRect
var prince: TextureRect
var candle: TextureRect
var caption: Label
var track: AudioStreamPlayer
var advance: Button
var speech: AudioStreamPlayer
var percussion: AudioStreamPlayer
var daddy: TextureRect
var eagle: TextureRect
var replay: Button

func _ready() -> void:
	name = "BattleOfBandsPrototype"
	size = DESIGN
	clip_contents = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	if persist_progress:
		var saved := ConfigFile.new()
		var loaded := saved.load(progress_path)
		if loaded != OK:
			loaded = saved.load(progress_path + ".bak")
		if loaded == OK:
			resume_seconds = clampf(float(saved.get_value("band", "song_seconds", 0.0)), 0.0, 90.9)
			song_finished = bool(saved.get_value("band", "song_finished", false))
			hits = clampi(int(saved.get_value("band", "hits", 0)), 0, PATTERN.size())
			story_step = clampi(int(saved.get_value("band", "story", 0)), 0, 3) if hits == PATTERN.size() else 0
	# Literal central meadow crop: native x1536..4608, y320..2048.
	for row: int in range(2):
		for column: int in range(1, 5):
			var tile := _picture("res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png" % [row, column],
				Rect2((column * 1024 - 1536) * (5.0 / 12.0), (row * 1024 - 320) * (5.0 / 12.0), 1024 * (5.0 / 12.0), 1024 * (5.0 / 12.0)))
			tile.stretch_mode = TextureRect.STRETCH_SCALE
	daddy = _picture("res://assets/prototypes/bands/daddy_ukulele.png", Rect2(110, 155, 235, 400))
	prince = _picture("res://assets/prototypes/bands/prince_drums.png", Rect2(760, 190, 400, 300))
	king = _picture("res://assets/prototypes/bands/king_guitar.png", Rect2(970, 310, 250, 270))
	actor = _picture("res://assets/prototypes/bands/roshan_drums.png", Rect2(335, 215, 350, 350))
	eagle = _picture("res://assets/prototypes/bands/eagle_bass.png", Rect2(640, 350, 160, 215))
	_picture(ChapterTwoPartyTable2D.TABLE_TEXTURE, Rect2(622, 280, 145, 70))
	_picture("res://assets/chapter2/birthday/chapter2_grand_five_strawberry_cake.png", Rect2(640, 184, 110, 125))
	candle = _picture("res://assets/chapter2/birthday/rainbow_candle_large_flame.png", Rect2(670, 139, 50, 85))
	var kit := Control.new()
	kit.name = "ForegroundDrumKit"
	kit.mouse_filter = Control.MOUSE_FILTER_IGNORE
	kit.draw.connect(_draw_kit.bind(kit))
	add_child(kit)
	caption = Label.new()
	caption.position = Vector2(190, 24)
	caption.size = Vector2(890, 68)
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(caption, 30, Color.WHITE)
	add_child(caption)
	advance = Button.new()
	advance.text = "➜"
	advance.position = Vector2(1100, 580)
	advance.size = Vector2(140, 110)
	StorybookUI.style_button(advance, "gold", 44)
	advance.pressed.connect(_advance_story)
	add_child(advance)
	replay = Button.new()
	replay.text = "↻"
	replay.position = advance.position
	replay.size = advance.size
	StorybookUI.style_button(replay, "gold", 44)
	replay.pressed.connect(_replay)
	add_child(replay)
	var back := Button.new()
	back.text = "←"
	back.position = Vector2(20, 20)
	back.size = Vector2(110, 110)
	StorybookUI.style_back_button(back)
	back.pressed.connect(func() -> void: _checkpoint(); get_tree().quit())
	add_child(back)
	track = AudioStreamPlayer.new()
	track.stream = recording
	track.volume_db = 0.0
	track.finished.connect(_on_song_finished)
	add_child(track)
	speech = AudioStreamPlayer.new()
	add_child(speech)
	percussion = AudioStreamPlayer.new()
	percussion.volume_db = -12.0
	add_child(percussion)
	song_finished = song_finished or story_step > 0
	_say("bands_tap_glowing_drum")
	_refresh()
	set_meta("cinematic_delivery_accepted", false)
	if hits > 0 and not song_finished and recording != null:
		track.play(resume_seconds)
	set_meta("recording_bound", recording != null)
	set_meta("exact_spoken_objective_missing", true)

func _picture(path: String, rect: Rect2) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = load(path) as Texture2D
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.position = rect.position
	picture.size = rect.size
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(picture)
	return picture

func _say(cue: String) -> void:
	# Deliberately no unrelated voice substitution for an unrecorded objective.
	var path := "res://assets/audio/voices/roshan_" + cue + ".ogg"
	if ResourceLoader.exists(path):
		speech.stream = load(path) as AudioStream
		speech.play()

func _process(delta: float) -> void:
	var viewport_size := get_viewport_rect().size
	var factor := minf(viewport_size.x / DESIGN.x, viewport_size.y / DESIGN.y)
	scale = Vector2.ONE * factor
	position = (viewport_size - DESIGN * factor) * 0.5
	if suspended:
		return
	elapsed += delta
	flash = maxf(0.0, flash - delta)
	(get_node("ForegroundDrumKit") as Control).queue_redraw()
	var king_active := _in_cue(king_outburst_cues)
	var prince_active := _in_cue(prince_outburst_cues)
	king.modulate = Color(1.0, 0.78, 0.72) if king_active else Color.WHITE
	prince.modulate = Color(1.0, 0.78, 0.72) if prince_active else Color.WHITE
	set_meta("outburst_active", king_active or prince_active)

func _in_cue(cues: Array[Vector2]) -> bool:
	if not track.playing:
		return false
	var time := track.get_playback_position()
	for cue: Vector2 in cues:
		if time >= cue.x and time < cue.y:
			return true
	return false

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		_set_suspended(true)
	elif what == NOTIFICATION_APPLICATION_FOCUS_IN:
		_set_suspended(false)

func _set_suspended(value: bool) -> void:
	suspended = value
	touch_owner = -1
	if is_instance_valid(track):
		track.stream_paused = value
	if is_instance_valid(speech):
		speech.stop()
	if is_instance_valid(percussion):
		percussion.stop()
	if value:
		_checkpoint()

func _gui_input(event: InputEvent) -> void:
	if suspended:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed and touch_owner == -1:
			touch_owner = touch.index
			_hit_at(touch.position)
		elif not touch.pressed and touch_owner == touch.index:
			touch_owner = -1
		accept_event()
	elif event is InputEventMouseButton:
		var mouse := event as InputEventMouseButton
		if mouse.device != InputEvent.DEVICE_ID_EMULATION and mouse.button_index == MOUSE_BUTTON_LEFT and mouse.pressed:
			_hit_at(mouse.position)
		accept_event()

func _hit_at(point: Vector2) -> void:
	for index: int in range(DRUMS.size()):
		if point.distance_to(DRUMS[index]) <= 56.0:
			strike(index)
			return

func strike(index: int) -> bool:
	if suspended or hits >= PATTERN.size() or index < 0 or index >= DRUMS.size():
		return false
	last_drum = index
	flash = 0.22
	_play_drum(index)
	if index != PATTERN[hits]:
		return false
	if recording != null and not track.playing and not song_finished:
		track.play()
	hits += 1
	_checkpoint()
	_refresh()
	return true

func _on_song_finished() -> void:
	song_finished = true
	_checkpoint()
	_refresh()

func _advance_story() -> void:
	if suspended or touch_owner != -1 or hits != PATTERN.size() or story_step >= 3 or not song_finished:
		return
	story_step += 1
	_checkpoint()
	_refresh()

func _refresh() -> void:
	advance.visible = hits == PATTERN.size() and story_step < 3 and song_finished
	replay.visible = story_step == 3
	if hits < PATTERN.size():
		caption.text = "Tap the glowing drum!"
	elif not song_finished:
		caption.text = "The whole band is playing!"
	else:
		caption.text = ["Roshan finishes her song!", "The King cheats and takes the candle!",
			"Prince: That wasn't fair, Father.", "We will find our rainbow together."][story_step]
	candle.position = Vector2(1040, 385) if story_step >= 1 else Vector2(670, 139)
	king.visible = story_step < 3
	prince.visible = story_step < 3
	candle.visible = story_step < 3

func _replay() -> void:
	if suspended or touch_owner != -1 or story_step != 3:
		return
	hits = 0
	song_finished = false
	story_step = 0
	track.stop()
	_checkpoint()
	_refresh()

func _play_drum(index: int) -> void:
	# Quiet procedural preview percussion; never substitutes for the song master.
	var bytes := PackedByteArray()
	var count := 4410
	bytes.resize(count * 2)
	for sample_index: int in range(count):
		var time := float(sample_index) / 22050.0
		var frequency := [120.0, 185.0, 1800.0][index] as float
		var sample := sin(TAU * frequency * time) * exp(-time * 35.0)
		if index == 2:
			sample *= sin(TAU * 2777.0 * time)
		bytes.encode_s16(sample_index * 2, int(sample * 12000.0))
	var sound := AudioStreamWAV.new()
	sound.format = AudioStreamWAV.FORMAT_16_BITS
	sound.mix_rate = 22050
	sound.data = bytes
	percussion.stream = sound
	percussion.play()

func _checkpoint() -> void:
	if not persist_progress:
		return
	var saved := ConfigFile.new()
	saved.set_value("band", "hits", hits)
	saved.set_value("band", "story", story_step)
	saved.set_value("band", "song_finished", song_finished)
	saved.set_value("band", "song_seconds", track.get_playback_position() if is_instance_valid(track) else resume_seconds)
	var temporary := progress_path + ".tmp"
	var error := saved.save(temporary)
	if error != OK:
		push_error("Band prototype progress could not be saved: %s" % error)
		return
	var target := ProjectSettings.globalize_path(progress_path)
	var backup := target + ".bak"
	var previous := ConfigFile.new()
	# Never replace a usable backup with a corrupt primary after recovery.
	if previous.load(progress_path) == OK:
		error = DirAccess.copy_absolute(target, backup)
		if error != OK:
			push_error("Band prototype backup could not be saved: %s" % error)
			return
	error = DirAccess.rename_absolute(ProjectSettings.globalize_path(temporary), target)
	if error != OK:
		push_error("Band prototype checkpoint could not be installed: %s" % error)

func _draw_kit(canvas: Control) -> void:
	var ink := Color("403051")
	# Feedback overlays only: the generated candidate owns all instrument pixels.
	for index: int in range(DRUMS.size()):
		var center: Vector2 = DRUMS[index]
		if hits < PATTERN.size() and PATTERN[hits] == index:
			canvas.draw_arc(center, 56 + sin(elapsed * 4) * 3, 0, TAU, 64, Color("fff1a7"), 6, true)
			canvas.draw_colored_polygon(PackedVector2Array([center + Vector2(-13, -88), center + Vector2(13, -88), center + Vector2(0, -66)]), Color("fff1a7"))
		if flash > 0 and index == last_drum:
			canvas.draw_arc(center, 64, 0, TAU, 32, Color.WHITE, 5, true)
	for index: int in range(3):
		canvas.draw_circle(Vector2(440 + index * 45, 605), 13, Color("fff1a7") if hits >= (index + 1) * 4 else ink)
