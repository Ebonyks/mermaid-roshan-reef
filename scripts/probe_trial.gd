extends SceneTree
# CHILD-PACED PLAYTEST: naive navigation (follows the guide), slow reactions,
# occasional wrong buttons. Logs sim-time pacing for the audit.
var sim_t := 0.0
var log_lines: Array = []

func _init() -> void:
	Engine.time_scale = 6.0
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	var t0 := 0.0
	var react := 0.0
	var wrong_done := {}
	var last_pearls: int = main.pearl_count
	var frame_i := 0
	while main.trophies < 5 and sim_t < 900.0:
		var delta: float = 1.0 / 60.0 * Engine.time_scale
		sim_t += 1.0 / 60.0 * Engine.time_scale
		frame_i += 1
		if main.pearl_count != last_pearls:
			log_lines.append("%6.1f  pearl collected (#%d)" % [sim_t, main.pearl_count])
			last_pearls = main.pearl_count
		if String(main.game) == "":
			# follow the guide like a kid: drift toward it with wander
			var target := Vector3.ZERO
			var best := 1.0e9
			for f in main.friends:
				if not bool(f["won"]):
					var d: float = (f["node"] as Sprite3D).position.distance_to(player.position)
					if d < best:
						best = d
						target = (f["node"] as Sprite3D).position
			if best < 1.0e8:
				var dir: Vector3 = (target - player.position).normalized()
				var wob := Vector3(sin(sim_t * 0.9) * 0.55, sin(sim_t * 1.7) * 0.2, cos(sim_t * 1.1) * 0.55)
				player.vel = (dir + wob).normalized() * 17.0
		else:
			var g: Dictionary = main.g
			var gname := String(main.game)
			react += 1.0 / 60.0 * Engine.time_scale
			if gname == "fetch":
				if String(g.get("phase", "")) == "aim" and react > 1.4:
					react = 0.0
					main.touch_ui.action_down = true
				else:
					main.touch_ui.action_down = false
			elif gname == "seek":
				if g.has("which") and react > 1.6:
					react = 0.0
					var which: int = int(g["which"])
					if not wrong_done.has([gname, int(g.get("found", 0))]) and randf() < 0.3:
						wrong_done[[gname, int(g.get("found", 0))]] = true
						main.melody_pressed = (which + 1) % 4
					else:
						main.melody_pressed = which
			elif gname == "melody":
				if String(g.get("stage", "show")) == "input" and react > 1.1:
					react = 0.0
					var seq: Array = g["seq"]
					var idx: int = int(g["input_i"])
					if idx < seq.size():
						main.melody_pressed = int(seq[idx])
			elif gname == "dolls":
				var dolls: Array = g.get("dolls", [])
				if dolls.size() > 0 and main.dolls_catcher != null:
					var lowest: ColorRect = dolls[0]
					for d in dolls:
						if (d as ColorRect).position.y > lowest.position.y:
							lowest = d
					main.dolls_catcher.position.x = lerpf(main.dolls_catcher.position.x, lowest.position.x - 40.0, 0.09)
			elif gname == "race":
				var rings: Array = g.get("rings", [])
				for rg in rings:
					if not rg["hit"]:
						var dir3: Vector3 = ((rg["node"] as Node3D).position - player.position).normalized()
						player.vel = dir3 * 15.0
						break
		# event edge logging
		if main.game != "" and not g_active:
			g_active = true
			log_lines.append("%6.1f  GAME START: %s" % [sim_t, main.game])
		elif main.game == "" and g_active:
			g_active = false
			log_lines.append("%6.1f  game end (trophies=%d)" % [sim_t, main.trophies])
		await process_frame
	log_lines.append("%6.1f  SESSION DONE trophies=%d pearls=%d" % [sim_t, main.trophies, main.pearl_count])
	print("=== CHILD-PACED TRIAL LOG (sim seconds) ===")
	for l in log_lines:
		print(l)
	quit()

var g_active := false
