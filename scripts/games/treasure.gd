class_name TreasureGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# treasure minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_cavern(origin: Vector3) -> void:
	var gy: float = m.ARENA_POS.y
	var pts := [
		Vector3(origin.x, gy + 8.0, origin.z + 14.0),
		Vector3(origin.x - 10.0, gy + 6.0, origin.z + 4.0),
		Vector3(origin.x - 6.0, gy + 4.2, origin.z - 8.0),
		Vector3(origin.x + 6.0, gy + 3.4, origin.z - 12.0),
		Vector3(origin.x + 12.0, gy + 3.0, origin.z - 2.0)]
	# rock tunnels around each passage
	for i in range(pts.size() - 1):
		var a2: Vector3 = pts[i]
		var b2: Vector3 = pts[i + 1]
		var mid: Vector3 = (a2 + b2) * 0.5
		var dirv: Vector3 = (b2 - a2).normalized()
		var side: Vector3 = dirv.cross(Vector3.UP).normalized()
		var up2: Vector3 = side.cross(dirv).normalized()
		for k in range(4):
			var ra: float = float(k) / 4.0 * TAU
			var rp: Vector3 = mid + (side * cos(ra) + up2 * sin(ra)) * 5.2
			var rk := m._place_aq("Rock%d" % (1 + (k + i) % 11), rp, 1.5 + randf() * 1.2, false)
			if rk != null:
				m.game_nodes.append(rk)
	# glowing anemones light the way
	for point_index in range(pts.size()):
		# The last route point belongs to the treasure silhouette. A glowing
		# anemone here hid the chest from the actual approach camera.
		if point_index == pts.size() - 1:
			continue
		var p2: Vector3 = pts[point_index]
		var apos: Vector3 = p2 + Vector3(1.5, -2.5, 1.0)
		var an: Node3D = m._gen2_prop("anemone_story", apos, 4.6, randf() * TAU, 0.03)
		if an == null:
			var old_an := MeshInstance3D.new()
			old_an.mesh = m._anemone_mesh()
			old_an.material_override = m._glow_tip_mat()
			old_an.scale = Vector3.ONE * 1.8
			old_an.position = apos + Vector3(0, 0.5, 0)
			m.add_child(old_an)
			an = old_an
		m.game_nodes.append(an)
	# The final chamber now resolves into one deliberate chest-on-dais focal
	# composition instead of another equally bright scatter cluster.
	var chest_approach: Vector3 = (pts[pts.size() - 2] - pts[pts.size() - 1]).normalized()
	var chest_yaw: float = atan2(chest_approach.x, chest_approach.z)
	m._art35_prop("res://assets/art35/arena/treasure_dais.glb", pts[pts.size() - 1] + Vector3(0, -3.1, 0), 1.08, chest_yaw)
	var chest: Node3D = m._art35_prop("res://assets/art35/arena/treasure_chest.glb", pts[pts.size() - 1] + Vector3(0, -2.4, 0), 1.22, chest_yaw)
	m.g["treasure_chest"] = chest
	var gl := OmniLight3D.new()
	gl.light_color = Color(1.0, 0.85, 0.4)
	gl.light_energy = 1.15
	gl.omni_range = 12.0
	gl.position = pts[pts.size() - 1]
	m.add_child(gl)
	m.game_nodes.append(gl)
	# ---- treasure-cave dressing: glowing crystals, gems, gold coins, pearls ----
	var gem_cols := [Color(1.0, 0.3, 0.45), Color(0.4, 0.7, 1.0), Color(0.5, 1.0, 0.65), Color(1.0, 0.85, 0.35), Color(0.8, 0.45, 1.0)]
	var seed2 := 7
	for k in range(12):
		seed2 = (seed2 * 1103515245 + 12345) & 0x7fffffff
		# Keep the final route point clear so the authored treasure dais and chest
		# remain the unmistakable reward silhouette.
		var pa: Vector3 = pts[(seed2 / 31) % (pts.size() - 1)]
		var off := Vector3(float(seed2 % 100) / 100.0 * 9.0 - 4.5, -2.2 - float((seed2 / 100) % 100) / 100.0 * 1.6, float((seed2 / 7) % 100) / 100.0 * 9.0 - 4.5)
		var spot: Vector3 = pa + off
		if spot.distance_to(pts[pts.size() - 1] as Vector3) < 9.0:
			continue
		var kind := (seed2 / 13) % 4
		if kind == 0:                      # glowing crystal cluster
			m._art35_prop("res://assets/art35/arena/treasure_cluster_%d.glb" % (k % 3), spot, 0.72 + randf() * 0.32, randf() * TAU)
		elif kind == 1:                    # bright gem
			var gem := MeshInstance3D.new()
			var sp := SphereMesh.new(); sp.radius = 0.55; sp.height = 1.1
			gem.mesh = sp
			gem.material_override = m._soft_mat(gem_cols[(seed2 / 5) % gem_cols.size()], 0.55)
			gem.position = spot + Vector3(0, 1.0, 0)
			m.add_child(gem); m.game_nodes.append(gem)
		elif kind == 2:                    # stack of gold coins
			for c in range(3):
				var coin := MeshInstance3D.new()
				var cyl := CylinderMesh.new(); cyl.top_radius = 0.5; cyl.bottom_radius = 0.5; cyl.height = 0.12
				coin.mesh = cyl
				var cmat := StandardMaterial3D.new()
				cmat.albedo_color = Color(1.0, 0.82, 0.3); cmat.metallic = 0.9; cmat.roughness = 0.25
				cmat.emission_enabled = true; cmat.emission = Color(0.8, 0.6, 0.2); cmat.emission_energy_multiplier = 0.4
				coin.material_override = cmat
				coin.position = spot + Vector3(0, 0.2 + float(c) * 0.13, 0)
				m.add_child(coin); m.game_nodes.append(coin)
		else:                              # glowing pearl
			var pl := MeshInstance3D.new()
			var ps := SphereMesh.new(); ps.radius = 0.6; ps.height = 1.2
			pl.mesh = ps
			pl.material_override = m._soft_mat(Color(1.0, 0.92, 0.97), 1.1)
			pl.position = spot + Vector3(0, 0.6, 0)
			m.add_child(pl); m.game_nodes.append(pl)
	for i in range(pts.size()):
		m._add_check(pts[i], "chest" if i == pts.size() - 1 else "way")

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.g["chains"] = []
	_build_cavern(origin)
	m.show_msg(fr["fname"], "Shhh... secret caverns! Follow the sparkles down to the treasure!")
