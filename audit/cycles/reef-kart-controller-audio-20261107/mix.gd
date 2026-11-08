extends SceneTree
## Capture the stereo Voice bus after the per-race panner, using the Windows mixer.

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
var failures := 0
var capture := AudioEffectCapture.new()

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var voice_bus := AudioServer.get_bus_index("Voice")
	if voice_bus < 0:
		quit(1)
		return
	capture.buffer_length = 6.0
	AudioServer.add_bus_effect(voice_bus, capture)
	print("MIX|device=", AudioServer.output_device, "|speaker_mode=", AudioServer.get_speaker_mode(),
		"|rate=", AudioServer.get_mix_rate())
	var pc := Scene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	pc._show_garage(2, 6)
	pc._join(11)
	for course in range(4):
		pc._choose_course(course)
		pc._start_race()
		var voice: Node = pc._race.item_voice
		var track: String = pc._race.track.id
		for kind: String in ["zoom", "sparkle", "kelp", "pearls"]:
			for slot: int in ([-1, 0, 1] if kind == "zoom" else [0, 1]):
				voice.clear()
				await create_timer(0.10).timeout
				capture.clear_buffer()
				voice.award(slot, kind)
				var cue_duration: float = voice.stream.get_length()
				var expected := int(AudioServer.get_mix_rate() * (cue_duration + 0.15))
				var deadline := Time.get_ticks_msec() + int(cue_duration * 1000.0) + 6000
				while capture.get_frames_available() < expected and Time.get_ticks_msec() < deadline:
					await process_frame
				var frames := capture.get_buffer(capture.get_frames_available())
				var powers := Vector2.ZERO
				var peak := 0.0
				for frame: Vector2 in frames:
					powers += frame * frame
					peak = maxf(peak, maxf(absf(frame.x), absf(frame.y)))
				var ratio := sqrt(powers.x / maxf(0.000001, powers.y))
				var correct: bool = frames.size() >= expected and peak > 0.01 and peak < 1.0 and 				((slot == -1 and absf(ratio - 1.0) <= 0.05) or (slot == 0 and ratio >= 2.0) or (slot == 1 and ratio <= 0.50))
				print("MIX|", track, "|", kind, "|", slot + 1, "|frames=", frames.size(), "|left_right_rms=", ratio,
					"|peak=", peak, "|", "PASS" if correct else "FAIL")
				failures += int(not correct)
		pc._return_to_garage()
	AudioServer.remove_bus_effect(voice_bus, AudioServer.get_bus_effect_count(voice_bus) - 1)
	pc.queue_free()
	await create_timer(0.1).timeout
	print("MIX|DONE|", failures)
	quit(failures)
