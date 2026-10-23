extends SceneTree
## Real GUI events with static layout references. Contacts are separately labelled fixtures.
const Preview := preload("res://scripts/popstar_concert_preview.gd")
const Band := preload("res://scripts/popstar_band_state.gd")
var failures: int = 0
var strike_count: int = 0
var stage: Control
func _initialize() -> void:
	_run.call_deferred()
func _run() -> void:
	root.size = Vector2i(1280,720)
	root.content_scale_size = Vector2i(1280,720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var chart: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/audio/music/popstar_concert/chart.json")) as Dictionary
	stage = Preview.new()
	root.add_child(stage)
	stage.setup(Band.create(chart),true)
	stage.manual_clock = true
	stage.set_process(false)
	stage.strike_requested.connect(_on_strike)
	await process_frame
	for a: int in range(4):
		for b: int in range(a+1,4):
			_check("owned targets do not overlap", Preview.TARGETS[a].distance_to(Preview.TARGETS[b]) >= 200.0)
	var cue: Dictionary = stage.data.beat.cues[0]
	stage.data.beat.clock = float(cue.beat)*60.0/float(chart.bpm)
	_touch(0,true,Preview.TARGETS[0])
	_check("touchdown strikes once", strike_count == 1)
	_touch(1,true,Preview.TARGETS[2])
	_check("foreign finger cannot strike", strike_count == 1 and stage.owner_finger == 0)
	_touch(1,false,Preview.TARGETS[2])
	_check("foreign release cannot steal owner", stage.owner_finger == 0)
	var drag: InputEventScreenDrag = InputEventScreenDrag.new()
	drag.index = 0
	drag.position = Preview.TARGETS[2]
	stage._gui_input(drag)
	_check("held motion cannot repeat", strike_count == 1)
	_check("no fake physical contact or reward from GUI input", int(stage.data.actions) == 0 and not bool(stage.data.complete))
	stage.pause_activity()
	_check("pause cancels finger, pending contact and music", stage.owner_finger == -99 and stage.data.pending.is_empty() and not stage.player.playing)
	var old_epoch: int = int(stage.epoch)
	stage.start_section()
	_check("resume restarts section in fresh epoch", int(stage.epoch) > old_epoch and float(stage.data.beat.clock) == 0.0)
	# Check the drawn cue bounds through the complete approach, with face/HUD present.
	stage.data.section = 2
	stage.start_section()
	var clear: bool = true
	for frame: int in range(241):
		stage.data.beat.clock = float(frame)/20.0
		stage._process(0.0)
		for card: TextureRect in stage.cues_visual.values():
			if card.visible and card.get_rect().intersects(Preview.FACE):
				clear = false
	_check("ribbon bounds never cross face", clear)
	# Animation-contact fixture is explicit: this does not establish drawn acting.
	stage.data = Band.create(chart,{"section":2})
	stage.data.beat.mercy = 2
	stage.start_section()
	var waiting_cue: Dictionary = stage.data.beat.cues[0]
	stage.data.beat.clock = 8.0
	_touch(0,true,Preview.TARGETS[int(waiting_cue.target)])
	_check("explicit animation-contact fixture confirms waiting hit",stage.confirm_authored_contact(String(waiting_cue.id),int(waiting_cue.target),int(stage.epoch)))
	_touch(0,false,Preview.TARGETS[int(waiting_cue.target)])
	var old_wait_epoch: int = int(stage.epoch)
	stage.data.beat.clock = 13.0
	stage._process(0.0)
	_check("native loop route retains fixture-confirmed hit",int(stage.epoch)>old_wait_epoch and stage.data.contacts.has(String(waiting_cue.id)) and int(stage.data.actions)==1)
	stage.data = Band.create(chart,{"section":2})
	stage.start_section()
	# Exercise clip-ended interludes through the actual controller signal path.
	stage.data = Band.create(chart,{"section":7})
	stage.start_section()
	var end_duration: float = float(Band.current(stage.data).bars)*4.0*60.0/float(chart.bpm)
	stage.data.restart_at = end_duration+1.5
	stage.data.beat.clock = end_duration
	var restart_epoch: int = int(stage.epoch)
	stage.player.finished.emit()
	await create_timer(2.05).timeout
	stage.audio_ended_at_us = Time.get_ticks_usec()-2000000
	stage._process(0.0)
	_check("ended clip advances contest restart clock",int(stage.epoch)>restart_epoch and float(stage.data.restart_at)<0.0)
	_check("old interlude time cannot consume restarted section",float(stage.data.beat.clock)==0.0 and int(stage.data.finished_epoch)!=int(stage.epoch))
	stage._on_audio_finished(restart_epoch)
	_check("old clip finished signal cannot end new epoch",int(stage.audio_ended_at_us)==-1)
	# Complete the whole concert through real GUI routing. Contact markers in
	# this fixture are explicit simulations, never evidence of drawn acting.
	stage.data = Band.create(chart)
	stage.start_section()
	var sections_driven: int = 0
	var all_touch_cues: bool = true
	while not bool(stage.data.complete) and sections_driven<16:
		var live_cues: Array = stage.data.beat.cues.duplicate(true)
		for live: Dictionary in live_cues:
			if String(live.role) not in ["answer","play","lead","finish"]:
				continue
			stage.data.beat.clock = float(live.beat)*60.0/float(stage.data.beat.bpm)+0.1
			_touch(0,true,Preview.TARGETS[int(live.target)])
			stage.data.beat.clock = float(stage.data.beat.clock)+0.05
			all_touch_cues = stage.confirm_authored_contact(String(live.id),int(live.target),int(stage.epoch)) and all_touch_cues
			_touch(0,false,Preview.TARGETS[int(live.target)])
		stage.data.beat.clock = float(Band.current(stage.data).bars)*4.0*60.0/float(stage.data.beat.bpm)+0.001
		stage._process(0.0)
		sections_driven += 1
		await process_frame
	_check("whole native concert controller completes with intentional fixture contacts",bool(stage.data.complete) and all_touch_cues and sections_driven==10)
	stage.data = Band.create(chart)
	stage.start_section()
	for idle_frame: int in range(2400):
		stage.data.beat.clock = float(stage.data.beat.clock)+0.05
		stage._process(0.05)
		if idle_frame%60==0:
			await process_frame
	_check("120s native idle loops earn nothing and never unlock mercy",not bool(stage.data.complete) and int(stage.data.section)==0 and int(stage.data.actions)==0 and int(stage.data.beat.mercy)==0)
	stage.data = Band.create(chart,{"section":2})
	stage.start_section()
	for argument: String in OS.get_cmdline_user_args():
		if argument.begins_with("--capture="):
			stage.data.beat.clock = 4.7
			stage._process(0.0)
			await process_frame
			await process_frame
			var image: Image = root.get_texture().get_image()
			_check("native Mobile capture contains pixels", image != null and not image.is_empty())
			if image != null and not image.is_empty():
				image.save_png(argument.trim_prefix("--capture="))
	stage.close()
	_check("close stops owned audio and cancels input", stage.owner_finger == -99 and not stage.player.playing and bool(stage.data.paused))
	stage = null
	await create_timer(0.12).timeout
	print("POPSTARPREVIEW|result: %s" % ("ALL OK" if failures == 0 else "%d FAIL" % failures))
	quit(0 if failures == 0 else 1)
func _touch(index: int, pressed: bool, point: Vector2) -> void:
	var event: InputEventScreenTouch = InputEventScreenTouch.new()
	event.index = index
	event.pressed = pressed
	event.position = point
	stage._gui_input(event)
func _on_strike(_cue: String, _target: int, _epoch: int) -> void:
	strike_count += 1
func _check(label: String, ok: bool) -> void:
	print("POPSTARPREVIEW|%s: %s" % [label,"OK" if ok else "FAIL"])
	if not ok:
		failures += 1
