extends Control
## Isolated nonrewarding native preview. It never writes saves or career stars.
## Static band art proves layout only. The animation owner must emit contact;
## no delayed timer or automatic demonstration fabricates a physical strike.
signal strike_requested(cue_id: String, target: int, epoch: int)
signal judged(result: Dictionary)
const Band := preload("res://scripts/popstar_band_state.gd")
const BeatKit := preload("res://scripts/beat_kit.gd")
const TARGETS: Array[Vector2] = [Vector2(450, 440), Vector2(620, 600), Vector2(820, 345), Vector2(1120, 570)]
const FACE: Rect2 = Rect2(520, 190, 180, 170)
const RIBBON_START: Array[Vector2] = [Vector2(390, 60),Vector2(790, 60),Vector2(1040, 60),Vector2(1160, 60)]
const ROOT_PATH: String = "res://assets/prototypes/popstar_concert/"
var data: Dictionary = {}
var player: AudioStreamPlayer
var speech: AudioStreamPlayer
var hits: Array[AudioStreamPlayer] = []
var owner_finger: int = -99
var rings: Array[TextureRect] = []
var cues_visual: Dictionary = {}
var epoch: int = 0
var manual_clock: bool = false
var muted: bool = false
var call_played: Dictionary = {}
var finish_connection: Callable
var audio_ended_at_us: int = -1
var caption: Label

func setup(state: Dictionary, silent: bool = false) -> void:
	data = state
	muted = silent
	mouse_filter = Control.MOUSE_FILTER_STOP
	size = Vector2(1280,720)
	for row: int in range(2):
		for col: int in range(2):
			var tile: TextureRect = _card("res://assets/opera/worlds/backdrops/stage_popstar_c%dr%d.png" % [col,row], Rect2(col*640,row*360,640,360))
			var atlas: AtlasTexture = AtlasTexture.new()
			atlas.atlas = tile.texture
			atlas.region = Rect2(0,448 if row == 0 else 0,1024,576)
			tile.texture = atlas
	_card(ROOT_PATH+"daddy_ukulele.png",Rect2(130,265,300,330))
	_card(ROOT_PATH+"eagle_bass.png",Rect2(945,260,280,310))
	_card(ROOT_PATH+"roshan_drums.png",Rect2(360,170,580,500))
	for target: int in range(4):
		var ring: TextureRect = _card("res://assets/opera/worlds/props/fx_invite_ring_%d.png" % mini(3,target),Rect2(TARGETS[target]-Vector2(100,100),Vector2(200,200)))
		ring.visible = false
		rings.append(ring)
	player = AudioStreamPlayer.new()
	add_child(player)
	speech = AudioStreamPlayer.new()
	add_child(speech)
	for instrument: String in ["tom","bass","cymbal","stick"]:
		var hit: AudioStreamPlayer = AudioStreamPlayer.new()
		hit.stream = load("res://assets/audio/music/popstar_concert/"+instrument+".ogg") as AudioStream
		add_child(hit)
		hits.append(hit)
	caption = Label.new()
	caption.text = "RHYTHM REBUILD PREVIEW — static layout reference; animation contact and rewards disabled"
	caption.position = Vector2(100,675)
	caption.add_theme_font_size_override("font_size",16)
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(caption)
	start_section()

func _card(path: String, rect: Rect2) -> TextureRect:
	var card: TextureRect = TextureRect.new()
	card.position = rect.position
	card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	card.texture = load(path) as Texture2D
	card.size = rect.size
	card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(card)
	return card

func start_section(preserve_wait: bool = false) -> void:
	cancel_touch()
	for card: TextureRect in cues_visual.values():
		card.queue_free()
	cues_visual.clear()
	call_played.clear()
	epoch = Band.continue_wait(data) if preserve_wait else Band.begin(data)
	var section: Dictionary = Band.current(data)
	player.stop()
	player.stream_paused = false
	if finish_connection.is_valid() and player.finished.is_connected(finish_connection):
		player.finished.disconnect(finish_connection)
	audio_ended_at_us = -1
	finish_connection = _on_audio_finished.bind(epoch)
	player.finished.connect(finish_connection)
	player.stream = load(String(section.audio)) as AudioStream
	player.pitch_scale = 0.5 if Band.slow_contest(data) else 1.0
	player.volume_db = -80.0 if muted else -7.0
	if not muted:
		player.play()
	for cue: Dictionary in data.beat.cues:
		if String(cue.role) in BeatKit.CHILD_ROLES:
			var card: TextureRect = _card(ROOT_PATH+"cues/"+["teal","lavender","gold","ghost"][int(cue.target)]+".png",Rect2(0,0,110,170))
			card.visible = false
			cues_visual[String(cue.id)] = card
	_speak(String(section.kind))

func _speak(kind: String) -> void:
	var file: String = "echo" if kind == "contest" else kind
	if file not in ["rehearsal","echo","play","lead","finish"]:
		return
	var path: String = ROOT_PATH+"voices/"+file+".ogg"
	if ResourceLoader.exists(path) and not muted:
		speech.stop()
		speech.stream = load(path) as AudioStream
		speech.play()

func _on_audio_finished(generation: int) -> void:
	if generation == epoch and not bool(data.paused):
		audio_ended_at_us = Time.get_ticks_usec() + int(AudioServer.get_output_latency()*1000000.0)

func audible_time() -> float:
	if manual_clock:
		return float(data.beat.clock)
	# Hardware-clock formula, never accumulated frame delta. Short sections
	# restart an epoch before playback position can wrap or reset.
	return BeatKit.observe(data.beat,player.get_playback_position()/player.pitch_scale,AudioServer.get_time_since_last_mix(),AudioServer.get_output_latency())

func _process(_delta: float) -> void:
	if data.is_empty() or bool(data.paused) or bool(data.complete):
		return
	var time: float = audible_time()
	if audio_ended_at_us >= 0 and Time.get_ticks_usec() >= audio_ended_at_us:
		time = float(Band.current(data).bars)*4.0*60.0/float(data.beat.bpm) + maxf(0.0,float(Time.get_ticks_usec()-audio_ended_at_us)/1000000.0)
		data.beat.clock = time
	player.volume_db = -80.0 if muted else (-17.0 if speech.playing else -7.0)
	for ring: TextureRect in rings:
		ring.visible = false
	var beat: float = time * float(data.beat.bpm) / 60.0
	var waiting_marked: bool = false
	for cue: Dictionary in data.beat.cues:
		var target: int = int(cue.target)
		if String(cue.role) == "call":
			if beat >= float(cue.beat) and not call_played.has(String(cue.id)):
				call_played[String(cue.id)] = true
				# Calls are authored in the backing. This glow is not child input.
			if beat >= float(cue.beat) and beat < float(cue.beat)+0.45:
				rings[target].visible = true
			continue
		if not cues_visual.has(String(cue.id)):
			continue
		var card: TextureRect = cues_visual[String(cue.id)]
		var resolved: bool = data.beat.results.has(String(cue.id))
		var until: float = float(cue.beat)-beat
		if int(data.beat.mercy) == 2:
			card.visible = not resolved and not waiting_marked
			if card.visible:
				waiting_marked = true
				card.position = TARGETS[target]-Vector2(55,155)
				rings[target].visible = true
		else:
			var scaffold: int = int(data.beat.scaffold) if String(cue.role) == "answer" else 1
			card.visible = scaffold == 1 and not resolved and until <= 4.0 and until >= -0.65
			var approach: float = clampf(1.0-until/4.0,0.0,1.0)
			# Centre lane goes beside her face before bending in below it.
			var bend: Vector2 = Vector2(RIBBON_START[target].x,TARGETS[target].y-100.0)
			var point: Vector2 = RIBBON_START[target].lerp(bend, minf(1.0,approach/0.75))
			if approach > 0.75:
				point = bend.lerp(TARGETS[target],(approach-0.75)/0.25)
			card.position = point-Vector2(55,155)
			if absf(until) < 0.4 and not resolved and scaffold <= 2:
				rings[target].visible = true
	var event: String = Band.tick(data,time)
	if event == "invite":
		_speak(String(Band.current(data).kind))
	elif event == "contest_idle":
		player.stream_paused = true
	elif event == "restart":
		start_section()
		return
	var duration: float = float(Band.current(data).bars)*4.0*60.0/float(data.beat.bpm)
	if time >= duration and event not in ["rest","contest_idle"]:
		var outcome: String = Band.finish_section(data,time)
		if outcome in ["advance","vamp","wait_loop"]:
			start_section(outcome == "wait_loop")

func _gui_input(event: InputEvent) -> void:
	if data.is_empty() or bool(data.paused):
		return
	if event is InputEventScreenTouch:
		var touch: InputEventScreenTouch = event as InputEventScreenTouch
		if touch.pressed and owner_finger == -99:
			owner_finger = touch.index
			_strike(touch.position)
		elif not touch.pressed and touch.index == owner_finger:
			owner_finger = -99
		accept_event()
	elif event is InputEventMouseButton:
		var button: InputEventMouseButton = event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed and owner_finger == -99:
			owner_finger = -1
			_strike(button.position)
		elif not button.pressed and owner_finger == -1:
			owner_finger = -99
		accept_event()

func _strike(point: Vector2) -> void:
	for target: int in range(4):
		if target == 3 and String(Band.current(data).kind) != "lead":
			continue
		if point.distance_to(TARGETS[target]) <= 100.0:
			if not muted:
				hits[target].play()
			player.stream_paused = false
			var result: Dictionary = Band.input(data,target,audible_time(),epoch)
			judged.emit(result)
			strike_requested.emit(String(result.get("cue_id","")),target,epoch)
			return

func confirm_authored_contact(cue_id: String, target: int, generation: int) -> bool:
	return Band.contact(data,cue_id,target,generation,audible_time())

func cancel_touch() -> void:
	owner_finger = -99

func pause_activity() -> void:
	cancel_touch()
	Band.pause(data)
	player.stop()
	speech.stop()
	for hit: AudioStreamPlayer in hits:
		hit.stop()

func _notification(what: int) -> void:
	if what in [NOTIFICATION_APPLICATION_FOCUS_OUT,NOTIFICATION_APPLICATION_PAUSED] and not data.is_empty():
		pause_activity()

func close() -> void:
	pause_activity()
	set_process(false)
	player.stream = null
	speech.stream = null
	for hit: AudioStreamPlayer in hits:
		hit.stream = null
	queue_free()
