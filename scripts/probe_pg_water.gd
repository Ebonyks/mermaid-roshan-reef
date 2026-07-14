extends SceneTree
# Diagnoses which water body floods the playground: enters level2, then dumps
# every MeshInstance3D whose material is a toon-water ShaderMaterial (global
# AABB) and, for each toy, the local terrain height vs every water surface
# overlapping its footprint. Dev-only.

var main: Node

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	for i in range(20):
		await process_frame
	var o: Vector3 = main.LEVEL2_POS
	print("=== WATER MESHES (lagoon-local y = global - %.0f) ===" % o.y)
	var waters: Array = []
	var stack: Array = [main]
	while not stack.is_empty():
		var nd: Node = stack.pop_back()
		for c in nd.get_children():
			stack.push_back(c)
		if nd is MeshInstance3D:
			var mi: MeshInstance3D = nd
			var mo: Material = mi.material_override
			if mo is ShaderMaterial and (mo as ShaderMaterial).shader != null:
				var code: String = (mo as ShaderMaterial).shader.code
				if code.contains("ripple") or code.contains("caustic"):
					var ab: AABB = mi.global_transform * mi.get_aabb()
					waters.append(mi)
					print("water @ local(%.0f..%.0f, %.0f..%.0f) surface_y(local)=%.1f..%.1f  name=%s parent=%s" % [
						ab.position.x - o.x, ab.end.x - o.x, ab.position.z - o.z, ab.end.z - o.z,
						ab.position.y - o.y, ab.end.y - o.y, mi.name, mi.get_parent().name])
	print("=== TOYS vs WATER ===")
	var lag = main._lagoon_ref()
	for toy in (main.g.get("toys", []) as Array):
		var base: Vector3 = toy["base"]
		var lx: float = base.x - o.x
		var lz: float = base.z - o.z
		var gy: float = lag._lagoon_local(lx, lz)
		var line: String = "%s local(%.0f,%.0f) ground=%.1f" % [String(toy["kind"]), lx, lz, gy]
		for w in waters:
			var ab2: AABB = (w as MeshInstance3D).global_transform * (w as MeshInstance3D).get_aabb()
			if base.x >= ab2.position.x and base.x <= ab2.end.x and base.z >= ab2.position.z and base.z <= ab2.end.z:
				var wy: float = ab2.end.y - o.y
				line += "  | inside %s waterline=%.1f%s" % [(w as MeshInstance3D).name, wy, ("  *** UNDERWATER by %.1f" % (wy - gy)) if wy > gy else " (dry, water below)"]
		print(line)
	print("=== DONE ===")
	quit()
