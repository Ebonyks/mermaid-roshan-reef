extends SceneTree
## Opt-in recording of real gamepad events in the normal desktop game.
## Use -- <path> to select an NDJSON output file. This harness injects no input.

class TracePC extends "res://scripts/racer/reef_kart_pc.gd":
	var trace: FileAccess
	var gas_arrival: Array[int] = [-1, -1]
	var gas_input: Array[float] = [0.0, 0.0]
	var gas_applied: Array[float] = [0.0, 0.0]
	var active_cue: Dictionary = {}

	func record(event: String, fields: Dictionary) -> void:
		var row := {"event": event, "usec": Time.get_ticks_usec()}
		row.merge(fields)
		trace.store_line(JSON.stringify(row))

	func scan(device: int, connected: bool) -> void:
		record("device", {"id": device, "connected": connected, "name": Input.get_joy_name(device),
			"guid": Input.get_joy_guid(device), "mapped": Input.is_joy_known(device)})

	func _input(event: InputEvent) -> void:
		if _screen == Screen.RACE and not _paused and _race.state == "race":
			var slot := _devices.find(event.device)
			if slot >= 0 and ((event is InputEventJoypadButton and event.button_index == JOY_BUTTON_A)
					or (event is InputEventJoypadMotion and event.axis == JOY_AXIS_TRIGGER_RIGHT)):
				var at := Time.get_ticks_usec()
				var level := 1.0 if Input.is_joy_button_pressed(event.device, JOY_BUTTON_A) else 					_trigger_gas(Input.get_joy_axis(event.device, JOY_AXIS_TRIGGER_RIGHT))
				if not is_equal_approx(level, gas_input[slot]):
					record("gas_event", {"slot": slot + 1, "device": event.device, "level": level})
					if level > 0.0 and gas_input[slot] == 0.0:
						gas_arrival[slot] = at
					gas_input[slot] = level
		super._input(event)

	func _race_command(slot: int) -> Dictionary:
		var command := super._race_command(slot)
		var throttle := float(command.get("throttle", 0.0))
		if not is_equal_approx(gas_applied[slot], throttle) or (gas_arrival[slot] >= 0 and throttle > 0.0):
			var elapsed := Time.get_ticks_usec() - gas_arrival[slot] if gas_arrival[slot] >= 0 and throttle > 0.0 else -1
			record("gas_step", {"slot": slot + 1, "device": _devices[slot], "level": throttle,
				"event_to_step_usec": elapsed})
			if elapsed >= 0:
				gas_arrival[slot] = -1
			gas_applied[slot] = throttle
		return command

	func _start_race() -> void:
		super._start_race()
		if _screen != Screen.RACE:
			return
		gas_arrival.fill(-1)
		gas_input.fill(0.0)
		gas_applied.fill(0.0)
		active_cue.clear()
		record("race_start", {"track": _race.track.id, "devices": _devices})
		_race.item_awarded.connect(func(slot: int, kind: String) -> void:
			record("item_award", {"slot": slot + 1, "kind": kind}))
		trace.flush()

	func _pause() -> void:
		super._pause()
		gas_arrival.fill(-1)
		gas_input.fill(0.0)
		gas_applied.fill(0.0)
		record("pause", {"devices": _devices})
		trace.flush()

	func _update_race_ui() -> void:
		super._update_race_ui()
		if _screen == Screen.RACE and _race.item_voice.active != active_cue:
			active_cue = _race.item_voice.active.duplicate()
			if not active_cue.is_empty():
				record("item_cue", {"slot": int(active_cue["slot"]) + 1, "kind": active_cue["kind"],
					"pan": _race.item_voice._panner.pan if _count == 2 else 0.0})
			trace.flush()

	func _show_result() -> void:
		record("finish", {"track": _race.track.id, "winner": _race.winner_slot + 1, "devices": _devices})
		trace.flush()
		super._show_result()


func _initialize() -> void:
	call_deferred("_open")


func _open() -> void:
	var args := OS.get_cmdline_user_args()
	var output := args[0] if not args.is_empty() else "user://reef_kart_physical_playtest.jsonl"
	var pc := TracePC.new()
	pc.trace = FileAccess.open(output, FileAccess.WRITE)
	if pc.trace == null:
		push_error("Cannot open physical controller test log")
		quit(1)
		return
	pc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.add_child(pc)
	current_scene = pc
	root.title = "Reef Grand Prix | physical controller test"
	Input.joy_connection_changed.connect(pc.scan)
	for id: int in Input.get_connected_joypads():
		pc.scan(id, true)
	pc.record("ready", {"engine": Engine.get_version_info()["string"], "detected": Input.get_connected_joypads().size()})
	pc.trace.flush()
