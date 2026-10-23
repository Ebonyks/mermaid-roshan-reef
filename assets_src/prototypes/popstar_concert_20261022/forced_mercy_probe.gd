extends SceneTree
## Independent GUI fairness fixture; animation contacts are simulated explicitly.
const Preview := preload("res://scripts/popstar_concert_preview.gd")
const Band := preload("res://scripts/popstar_band_state.gd")
var stage: Control
var last: Dictionary = {}
func _initialize() -> void:
	_run.call_deferred()
func _run() -> void:
	var chart: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/audio/music/popstar_concert/chart.json")) as Dictionary
	stage = Preview.new()
	root.add_child(stage)
	stage.setup(Band.create(chart,{"section":2}),true)
	stage.manual_clock = true
	stage.set_process(false)
	stage.judged.connect(_judged)
	stage.data.beat.mercy = 2
	stage.start_section()
	var advanced_at: float = -1.0
	for n: int in range(600):
		stage.data.beat.clock = float(stage.data.beat.clock)+0.2
		var touch: InputEventScreenTouch = InputEventScreenTouch.new()
		touch.index = 0
		touch.pressed = true
		touch.position = Preview.TARGETS[n%3]
		last = {}
		stage._gui_input(touch)
		if String(last.get("status",""))=="credited":
			stage.confirm_authored_contact(String(last.cue_id),n%3,int(stage.epoch))
		touch.pressed = false
		stage._gui_input(touch)
		stage._process(0.2)
		if int(stage.data.section)!=2:
			advanced_at = (n+1)*0.2
			break
		if n%30==0:
			await process_frame
	var intentional_bound: float = float(chart.sections[2].bars)*4.0*60.0/float(chart.bpm)
	var ok: bool = advanced_at>intentional_bound and advanced_at<=120.0
	print("FORCEDMERCY|intentional section bar-end seconds: %.3f" % intentional_bound)
	print("FORCEDMERCY|5Hz three-target GUI cycle advance seconds: %.3f" % advanced_at)
	print("FORCEDMERCY|result: %s" % ("ALL OK" if ok else "FAIL"))
	stage.close()
	stage = null
	await create_timer(0.12).timeout
	quit(0 if ok else 1)
func _judged(result: Dictionary) -> void:
	last = result
