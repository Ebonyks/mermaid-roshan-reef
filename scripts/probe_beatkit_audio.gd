extends SceneTree
## Bounded exact-runtime clock comparison. Target-phone proof remains separate.
var player: AudioStreamPlayer
var receipt: Dictionary = {"engine":Engine.get_version_info(),"backend":AudioServer.get_driver_name(),"lanes":{}}
func _initialize() -> void:
	_run.call_deferred()
func _run() -> void:
	player = AudioStreamPlayer.new()
	root.add_child(player)
	player.volume_db = -70.0
	var ogg: AudioStream = load("res://assets/audio/music/popstar_concert/chorus_1.ogg") as AudioStream
	for lane: String in ["ogg","interactive","ogg_half"]:
		player.pitch_scale = 0.5 if lane == "ogg_half" else 1.0
		if lane != "interactive":
			player.stream = ogg
		else:
			var interactive: AudioStreamInteractive = AudioStreamInteractive.new()
			interactive.set_clip_count(1)
			interactive.set_clip_stream(0,ogg)
			interactive.set_initial_clip(0)
			player.stream = interactive
		player.play()
		var readings: Array = []
		for sample: int in range(8):
			await create_timer(0.1).timeout
			readings.append({"position":player.get_playback_position(),"since_mix":AudioServer.get_time_since_last_mix(),"output_latency":AudioServer.get_output_latency()})
		receipt.lanes[lane] = readings
		player.stop()
		player.stream = null
		await create_timer(0.12).timeout
	receipt.audio_sha256 = FileAccess.get_sha256("res://assets/audio/music/popstar_concert/chorus_1.ogg")
	receipt.choice = "one Ogg per section"
	receipt.reason = "Interactive playback position is not usable" if float(receipt.lanes.interactive.back().position) <= 0.01 else "Both advance; fallback keeps section epochs directly observable. Interactive transitions not yet proven."
	var destination: String = "res://build/popstar-rebuild-20261022/audio_clock.json"
	var f: FileAccess = FileAccess.open(destination,FileAccess.WRITE)
	f.store_string(JSON.stringify(receipt,"\t")+"\n")
	f.close()
	var ok: bool = float(receipt.lanes.ogg.back().position) > 0.5
	player.queue_free()
	await create_timer(0.15).timeout
	print("BEATKITAUDIO|%s|%s" % ["ALL OK" if ok else "FAIL",receipt.reason])
	quit(0 if ok else 1)
