class_name GrottoPuzzle
extends RefCounted
# E2 push-block grotto (ZELDA_GAMEPLAY_WORKORDER): the reef's first embodied
# mini-dungeon. A coral ring with an open mouth hides a 3x3 sand grid, two
# pastel blocks and two golden pad pools. Swim into a block and keep pushing
# — it glides one cell. Park a block on each pad and the grotto celebrates:
# fanfare, sparkles, five pearls, a cheer. Grid-snapped and fully analytic
# (no engine bodies), and deadlock-free by construction: she swims, so she
# can always get behind a block — every position is recoverable, no fail
# states. Pads stay lit once won (session toy afterwards, no re-reward).

const CENTER := Vector3(-70.0, 0.0, 62.0)
const CELL := 5.0
const WALL_R := 17.0
const PADS := [Vector2i(0, 1), Vector2i(1, 1)]
const BLOCK_START := [Vector2i(-1, 0), Vector2i(1, -1)]
const WALL_KINDS := ["coral1", "coral2", "coral3", "coral4", "coral5", "coral6"]

var m: ReefMain
var floor_y := 0.0
var blocks: Array = []   # {node, cell, solid, from, to, move_t, push_t}
var pads: Array = []     # {cell, halo, lit}
var done := false
var hinted := false

func _init(main: ReefMain) -> void:
	m = main
	floor_y = ReefMain.seabed_y(CENTER.x, CENTER.z)
	_build()

func cell_pos(c: Vector2i) -> Vector3:
	return Vector3(CENTER.x + float(c.x) * CELL, floor_y + 2.1, CENTER.z + float(c.y) * CELL)

func _build() -> void:
	# coral wall ring with an entrance gap facing the reef heart
	var gap_ang: float = atan2(-CENTER.z, -CENTER.x)
	for i in range(10):
		var ang: float = float(i) / 10.0 * TAU
		if absf(wrapf(ang - gap_ang, -PI, PI)) < 0.55:
			continue
		var wx: float = CENTER.x + cos(ang) * WALL_R
		var wz: float = CENTER.z + sin(ang) * WALL_R
		var wy: float = ReefMain.seabed_y(wx, wz)
		var prop: Node3D = m._gen2_prop(WALL_KINDS[i % WALL_KINDS.size()],
			Vector3(wx, wy, wz), 9.0, randf() * TAU, 0.3)
		if prop != null and "flora_nodes" in m:
			m.flora_nodes.append(prop)
		m.solids.append({"x": wx, "z": wz, "r": 4.0, "y0": wy - 1.0, "y1": wy + 12.0})
	for c in PADS:
		var pp: Vector3 = cell_pos(c)
		var halo: MeshInstance3D = m._halo(Vector3(pp.x, floor_y + 0.5, pp.z), Color(1.0, 0.85, 0.5), 6.5)
		pads.append({"cell": c, "halo": halo, "lit": false})
	for i in range(BLOCK_START.size()):
		var c: Vector2i = BLOCK_START[i]
		var bp: Vector3 = cell_pos(c)
		var mi := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(3.9, 3.9, 3.9)
		mi.mesh = bm
		mi.material_override = m._soft_mat(
			[Color(1.0, 0.72, 0.85), Color(0.7, 0.95, 0.85)][i % 2], 0.2)
		mi.position = bp
		m.add_child(mi)
		var solid := {"x": bp.x, "z": bp.z, "r": 2.8, "y0": floor_y - 1.0, "y1": floor_y + 6.0}
		m.solids.append(solid)
		blocks.append({"node": mi, "cell": c, "solid": solid,
			"from": bp, "to": bp, "move_t": -1.0, "push_t": 0.0})

func tick(delta: float, ppos: Vector3) -> void:
	if not hinted and ppos.distance_to(Vector3(CENTER.x, floor_y + 3.0, CENTER.z)) < 24.0:
		hinted = true
		m._say("roshan", "")   # her curious line as she discovers the grotto
	for b in blocks:
		if float(b["move_t"]) >= 0.0:
			b["move_t"] = float(b["move_t"]) + delta
			var f: float = clampf(float(b["move_t"]) / 0.35, 0.0, 1.0)
			var np: Vector3 = (b["from"] as Vector3).lerp(b["to"], smoothstep(0.0, 1.0, f))
			(b["node"] as Node3D).position = np
			b["solid"]["x"] = np.x
			b["solid"]["z"] = np.z
			if f >= 1.0:
				b["move_t"] = -1.0
				_landed()
			continue
		# push: her nose on the block, still swimming into it after a beat
		var bp: Vector3 = (b["node"] as Node3D).position
		var flat: Vector3 = bp - ppos
		flat.y = 0.0
		var d: float = flat.length()
		var pv: Vector3 = Vector3.ZERO
		if m.player != null:
			pv = m.player.vel
		if d > 0.01 and d < 4.6 and Vector3(pv.x, 0.0, pv.z).dot(flat / d) > 3.0:
			b["push_t"] = float(b["push_t"]) + delta
			if float(b["push_t"]) > 0.3:
				b["push_t"] = 0.0
				var stepc := Vector2i(0, 0)
				if absf(flat.x) > absf(flat.z):
					stepc = Vector2i(1 if flat.x > 0.0 else -1, 0)
				else:
					stepc = Vector2i(0, 1 if flat.z > 0.0 else -1)
				_try_slide(b, stepc)
		else:
			b["push_t"] = maxf(0.0, float(b["push_t"]) - delta * 2.0)

func _try_slide(b: Dictionary, stepc: Vector2i) -> bool:
	if float(b["move_t"]) >= 0.0:
		return false   # already gliding — one cell per push
	var nc: Vector2i = (b["cell"] as Vector2i) + stepc
	if nc.x < -1 or nc.x > 1 or nc.y < -1 or nc.y > 1:
		return false
	for ob in blocks:
		if ob != b and (ob["cell"] as Vector2i) == nc:
			return false
	b["cell"] = nc
	b["from"] = (b["node"] as Node3D).position
	b["to"] = cell_pos(nc)
	b["move_t"] = 0.0
	if m.chime != null:
		m.chime.pitch_scale = 0.7
		m.chime.play()
	m._sparkle_burst((b["to"] as Vector3) - Vector3(0, 1.2, 0), Color(0.95, 0.9, 0.7))
	return true

func _landed() -> void:
	var lit_n: int = 0
	for pd in pads:
		var occupied := false
		for ob in blocks:
			if (ob["cell"] as Vector2i) == (pd["cell"] as Vector2i) and float(ob["move_t"]) < 0.0:
				occupied = true
		if occupied and not bool(pd["lit"]):
			pd["lit"] = true
			(pd["halo"] as MeshInstance3D).scale = Vector3.ONE * 1.6
			m._sparkle_burst(cell_pos(pd["cell"]), Color(1.0, 0.9, 0.5))
			if m.chime != null:
				m.chime.pitch_scale = 1.2
				m.chime.play()
		elif not occupied and bool(pd["lit"]) and not done:
			pd["lit"] = false
			(pd["halo"] as MeshInstance3D).scale = Vector3.ONE
		if bool(pd["lit"]):
			lit_n += 1
	if lit_n == pads.size() and not done:
		done = true
		m.pearl_count += 5
		m._update_hud()
		m._fanfare()
		m._sparkle_burst(Vector3(CENTER.x, floor_y + 4.0, CENTER.z), Color(1.0, 0.85, 0.95))
		m._say("roshan", ["pearl", "pearl2", "pearl3"][randi() % 3])
		if m.player != null:
			m.player.play_verb("cheer")
