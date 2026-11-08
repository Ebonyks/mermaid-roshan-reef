extends "res://audit/cycles/reef-kart-roadside-20261107/drive.gd"
## Reuse the input-only eight-leg race sweep with fixed native captures.

func _run() -> void:
	root.unresizable = true
	root.min_size = Vector2i(1280, 720)
	root.max_size = Vector2i(1280, 720)
	await super._run()


func _sample() -> void:
	if race.state != "finished" and not frames.is_empty() and elapsed() - float(frames.back()["t"]) < 1.7:
		return
	super._sample()
