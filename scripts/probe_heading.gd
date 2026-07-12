extends SceneTree
# Heading fix check, analytic: compare each mover creature's world facing
# (+Z model axis) against its velocity direction. Angle should be ~0 deg.

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for f in range(20):
		await process_frame
	var prev := {}
	for mv in main.aquatic_movers:
		prev[mv["node"]] = (mv["node"] as Node3D).position
	for f in range(12):
		await process_frame
	var count := 0
	for mv in main.aquatic_movers:
		var n: Node3D = mv["node"]
		var vel: Vector3 = n.position - prev[n]
		vel.y = 0.0
		if vel.length() < 0.01:
			continue
		var facing: Vector3 = n.global_transform.basis.z
		facing.y = 0.0
		var ang: float = rad_to_deg(facing.normalized().angle_to(vel.normalized()))
		print("HEADING %s angle_off=%.1f deg" % [n.name, ang])
		count += 1
		if count >= 10:
			break
	quit()
