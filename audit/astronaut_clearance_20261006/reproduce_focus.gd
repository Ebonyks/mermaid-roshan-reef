extends SceneTree

const SurfaceScript := preload("res://scripts/opera_gesture_surface.gd")
var surface: OperaGestureSurface
var rows: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	get_root().size = Vector2i(1280, 720)
	surface = SurfaceScript.new() as OperaGestureSurface
	surface.position = Vector2(40, 40)
	surface.size = Vector2(852, 560)
	surface.mouse_filter = Control.MOUSE_FILTER_STOP
	get_root().add_child(surface)
	surface.configure("hold", Color.WHITE, 1, "charge_astronaut")
	await process_frame
	var touch := InputEventScreenTouch.new()
	touch.index = 7
	touch.pressed = true
	touch.position = surface.get_global_transform_with_canvas() * (surface.size * 0.5)
	Input.parse_input_event(touch)
	await process_frame
	rows.append({"check": "genuine viewport touch arms launch hold", "pass": surface.held,
		"held": surface.held, "owner": surface.active_touch_index})
	surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	await process_frame
	rows.append({"check": "focus loss clears held launch input", "pass": not surface.held,
		"held": surface.held, "owner": surface.active_touch_index})
	var failures := 0
	for row: Dictionary in rows:
		if not bool(row["pass"]):
			failures += 1
	print("ASTRO_FOCUS_EVIDENCE|" + JSON.stringify({"rows": rows, "failures": failures,
		"input": "Input.parse_input_event -> viewport GUI dispatch",
		"focus_boundary": "Node.notification(APPLICATION_FOCUS_OUT), not real-device evidence",
		"scope": "Surface cancellation reproduction; whole-world action/score/capture acceptance absent"}))
	surface.queue_free()
	await process_frame
	quit(1 if failures > 0 else 0)
