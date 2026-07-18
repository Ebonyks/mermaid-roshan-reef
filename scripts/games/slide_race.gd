class_name SlideRaceGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# race minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_playplace(origin: Vector3, fr: Dictionary) -> void:
	var gy: float = m.ARENA_POS.y
	var pads := [Color(1.0, 0.5, 0.6), Color(1.0, 0.85, 0.35), Color(0.4, 0.85, 0.95), Color(0.7, 0.55, 1.0)]
	if m.rainbow_slide_mode:
		pads = [Color(1.0, 0.25, 0.3), Color(1.0, 0.6, 0.15), Color(1.0, 0.9, 0.25), Color(0.3, 0.85, 0.4), Color(0.3, 0.55, 1.0), Color(0.6, 0.35, 0.9)]
	# spiral story platforms (3 stories)
	for i in range(9):
		var aa: float = float(i) * 0.75
		var rr: float = 14.0 - float(i) * 0.8
		var pp := Vector3(origin.x + cos(aa) * rr, gy + 2.0 + float(i) * 3.0, origin.z + sin(aa) * rr)
		m._course_box(pp, Vector3(5.5, 0.8, 4.2), pads[i % pads.size()])
	# story rims (visual floors)
	for st in range(3):
		var rim := MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 16.5
		tm.outer_radius = 17.3
		rim.mesh = tm
		rim.material_override = m._soft_mat(pads[st % pads.size()], 0.3)
		rim.position = Vector3(origin.x, gy + 10.0 + float(st) * 9.0, origin.z)
		m.add_child(rim)
		m.game_nodes.append(rim)
	# ball pit (colorful balls in a ring pool)
	var pit := Vector3(origin.x + 14.0, gy + 0.8, origin.z)
	var wall := MeshInstance3D.new()
	var wt := TorusMesh.new()
	wt.inner_radius = 5.4
	wt.outer_radius = 6.6
	wall.mesh = wt
	wall.material_override = m._soft_mat(Color(0.45, 0.6, 1.0), 0.2)
	wall.position = pit
	m.add_child(wall)
	m.game_nodes.append(wall)
	var mmi := MultiMeshInstance3D.new()
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var bms := SphereMesh.new()
	bms.radius = 0.55
	bms.height = 1.1
	var bmat := StandardMaterial3D.new()
	bmat.vertex_color_use_as_albedo = true
	bmat.roughness = 0.4
	bms.material = bmat
	mm.mesh = bms
	mm.instance_count = 90
	for bi in range(90):
		var ba: float = randf() * TAU
		var br: float = sqrt(randf()) * 4.8
		var bp := Vector3(pit.x + cos(ba) * br, gy + 0.7 + randf() * 1.6, pit.z + sin(ba) * br)
		mm.set_instance_transform(bi, Transform3D(Basis(), bp))
		mm.set_instance_color(bi, pads[bi % pads.size()])
	mmi.multimesh = mm
	m.add_child(mmi)
	m.game_nodes.append(mmi)
	# trampoline
	var tramp := Vector3(origin.x - 13.0, gy + 1.2, origin.z + 8.0)
	m._course_box(tramp, Vector3(4.6, 0.7, 4.6), Color(0.25, 0.45, 0.95))
	m._course_box(tramp + Vector3(0, -0.8, 0), Vector3(3.6, 0.9, 3.6), Color(0.15, 0.2, 0.4))
	m.g["tramp_pos"] = tramp
	# finger curtains (2 passages)
	m._build_chain_curtain(Vector3(origin.x - 5.0, gy + 17.5, origin.z - 11.0), Vector3(origin.x + 5.0, gy + 17.5, origin.z - 11.0), 7)
	m._build_chain_curtain(Vector3(origin.x + 4.0, gy + 27.5, origin.z + 3.0), Vector3(origin.x + 4.0, gy + 27.5, origin.z + 13.0), 7)
	# moving ring obstacle (story 2)
	var mv := MeshInstance3D.new()
	var mt := TorusMesh.new()
	mt.inner_radius = 2.6
	mt.outer_radius = 3.4
	mv.mesh = mt
	mv.material_override = m._soft_mat(Color(0.5, 1.0, 0.6), 0.6)
	mv.rotation_degrees = Vector3(90, 0, 0)
	mv.position = Vector3(origin.x - 6.0, gy + 19.0, origin.z + 6.0)
	m.add_child(mv)
	m.game_nodes.append(mv)
	m.g["mover_node"] = mv
	m.g["mover_base"] = mv.position
	# THE BIG SLIDE: yellow chute from the top to the ground
	var path: Array = [
		Vector3(origin.x, gy + 29.0, origin.z),
		Vector3(origin.x + 6.0, gy + 25.5, origin.z + 4.0),
		Vector3(origin.x + 11.0, gy + 21.0, origin.z + 8.0),
		Vector3(origin.x + 14.5, gy + 15.5, origin.z + 12.0),
		Vector3(origin.x + 16.0, gy + 10.0, origin.z + 16.5),
		Vector3(origin.x + 15.0, gy + 5.0, origin.z + 21.0),
		Vector3(origin.x + 12.5, gy + 2.8, origin.z + 25.0)]
	m.g["slide_path"] = path
	for i in range(path.size() - 1):
		var a2: Vector3 = path[i]
		var b2: Vector3 = path[i + 1]
		var mid: Vector3 = (a2 + b2) * 0.5
		var seg := MeshInstance3D.new()
		var sb := BoxMesh.new()
		sb.size = Vector3(3.4, 0.5, a2.distance_to(b2) + 0.7)
		seg.mesh = sb
		seg.material_override = m._soft_mat(Color(1.0, 0.8, 0.2), 0.25)
		m.add_child(seg)
		seg.look_at_from_position(mid, b2, Vector3.UP)
		m.game_nodes.append(seg)
		for sgn in [-1.0, 1.0]:
			var rail := MeshInstance3D.new()
			var rb := BoxMesh.new()
			rb.size = Vector3(0.4, 1.0, a2.distance_to(b2) + 0.7)
			rail.mesh = rb
			rail.material_override = m._soft_mat(Color(1.0, 0.55, 0.25), 0.2)
			m.add_child(rail)
			rail.look_at_from_position(mid, b2, Vector3.UP)
			rail.translate_object_local(Vector3(sgn * 1.7, 0.5, 0))
			m.game_nodes.append(rail)
	# friend cheering at the slide top (only when this game has a friend sprite — the Rainbow Slide has none)
	var cheer_node = fr.get("node")
	if cheer_node != null and is_instance_valid(cheer_node) and cheer_node is Sprite3D:
		var sis := Sprite3D.new()
		sis.texture = (cheer_node as Sprite3D).texture
		sis.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		sis.pixel_size = 0.013
		sis.position = path[0] + Vector3(-3.0, 3.0, -2.0)
		m.add_child(sis)
		m.game_nodes.append(sis)
	# checkpoints: ballpit -> trampoline -> curtain 1 -> moving ring -> curtain 2 -> slide
	m._add_check(pit + Vector3(0, 1.6, 0), "ball")
	m._add_check(m.g["tramp_pos"] + Vector3(0, 1.8, 0), "tramp")
	m._add_check(Vector3(origin.x, gy + 14.6, origin.z - 11.0), "curtain")
	m._add_check(mv.position, "mover")
	m._add_check(Vector3(origin.x + 4.0, gy + 24.6, origin.z + 8.0), "curtain")
	m._add_check(path[0], "slide")

# ===================== PENGUIN ICE SLIDE =====================
# A short N64-style downhill chute. Roshan slides on momentum (gravity along the
# slope); the player only steers left/right. 5 fish to grab, ~12 seconds.
const SLIDE_WIDTH := 18.0          # chute interior width
const SLIDE_GRAV := 44.0           # along-slope gravity pull
const SLIDE_FRICT := 0.32          # speed-proportional drag (sets terminal speed)
const SLIDE_VMAX := 26.0
const SLIDE_VMIN := 13.0           # keeps the flat finish from crawling
const SLIDE_STEER := 38.0          # lateral acceleration from steering
const SLIDE_RIDE := 2.2            # how far above the chute surface Roshan rides
const SLIDE_LEAD := 22.0           # baby penguin's head start (shrinks to 0 at the bottom)

func _slide_plank(a: Vector3, b: Vector3, width: float, mat: StandardMaterial3D, thick: float = 0.8) -> void:
	var mid: Vector3 = (a + b) * 0.5
	var dir: Vector3 = b - a
	var seg: float = dir.length()
	if seg < 0.001:
		return
	var fwd: Vector3 = dir / seg
	var right: Vector3 = Vector3.UP.cross(fwd)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	right = right.normalized()
	var up2: Vector3 = fwd.cross(right).normalized()
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(width, thick, seg)
	mi.mesh = bm
	mi.material_override = mat
	mi.transform = Transform3D(Basis(right, up2, fwd), mid)
	m.add_child(mi)
	m.game_nodes.append(mi)

func _aq_game(model: String, pos: Vector3, scl: float) -> Node3D:
	# spawn an aquatic model as a GAME object (freed with the arena, no flora_nodes leak)
	if m.CREATURE_GEN2.has(model):
		# the slide's baby penguin, cheer squad and bonus fish are HER art
		# too (owner 2026-07-11) - same family model + swim/waddle sway as
		# the reef, registered on the game-lifetime node list instead
		var cw := m._gen2_creature(String(m.CREATURE_GEN2[model]), pos, scl * 2.0)
		if cw != null:
			m.game_nodes.append(cw)
			return cw
	var ps := m._aq(model)
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	if not m.model_cache.has("aq2_" + model):
		m._paint_aq(inst, m._aq_mat(model))   # Riley models are untextured; gen2 aren't
	m.add_child(inst)
	m.game_nodes.append(inst)
	return inst

func _build_slide(origin: Vector3, theme: String = "ice", mode: String = "fish") -> void:
	# ---- centerline: an S-curve that descends, then flattens out at the bottom ----
	var path: Array = []
	var N := 26
	for i in range(N + 1):
		var t: float = float(i) / float(N)
		var z: float = lerp(-110.0, 120.0, t)
		var x: float = sin(t * TAU * 0.85) * 24.0
		# steep at the top (quick whoosh), easing flat near the bottom for a gentle finish
		var y: float = 2.0 + 48.0 * pow(1.0 - t, 1.2)
		path.append(origin + Vector3(x, y, z))
	m.g["path"] = path
	# precompute cumulative arc length
	var cum: Array = [0.0]
	var total := 0.0
	for i in range(path.size() - 1):
		total += (path[i + 1] - path[i]).length()
		cum.append(total)
	m.g["cum"] = cum
	m.g["total"] = total
	m.g["s"] = 0.0
	m.g["v"] = SLIDE_VMIN
	m.g["x"] = 0.0
	m.g["vx"] = 0.0
	m.g["got"] = 0
	m.g["caught"] = false
	# ---- build the chute: themed floor planks + glowing side rails ----
	var rainbow := [Color(0.90, 0.32, 0.42), Color(0.94, 0.58, 0.30), Color(0.92, 0.82, 0.30), Color(0.36, 0.76, 0.46), Color(0.34, 0.67, 0.90), Color(0.50, 0.44, 0.88), Color(0.78, 0.42, 0.84)]
	var rail := m._ice_mat(Color(0.42, 0.68, 0.90), 0.15) if theme == "ice" else m._ice_mat(Color(0.84, 0.72, 0.34), 0.18)
	for i in range(path.size() - 1):
		var a: Vector3 = path[i]
		var b: Vector3 = path[i + 1]
		# plank albedo stays UNDER 1.0 — over-white components push the snow
		# past ACES white and the surface detail clips away (Android blowout)
		var pmat: StandardMaterial3D = m._ice_mat(rainbow[i % rainbow.size()], 0.10) if theme == "rainbow" else m._ice_mat(Color(0.68, 0.78, 0.90), 0.02, "snow")
		_slide_plank(a, b, SLIDE_WIDTH, pmat)
		# side rails sit on the chute edges
		var smp := _slide_dir(i)
		var rt: Vector3 = smp[1]
		_slide_plank(a + rt * (SLIDE_WIDTH * 0.5), b + rt * (SLIDE_WIDTH * 0.5), 1.4, rail, 4.0)
		_slide_plank(a - rt * (SLIDE_WIDTH * 0.5), b - rt * (SLIDE_WIDTH * 0.5), 1.4, rail, 4.0)
		if i % 4 == 1:
			var bank_mid: Vector3 = (a + b) * 0.5
			var bank_fwd: Vector3 = (b - a).normalized()
			var bank_yaw: float = atan2(-bank_fwd.z, bank_fwd.x)
			for bank_side in [-1.0, 1.0]:
				m._art35_prop("res://assets/art35/arena/slide_snowbank_%d.glb" % ((int(i / 4) + int(bank_side > 0.0)) % 2), bank_mid + rt * bank_side * (SLIDE_WIDTH * 0.5 + 2.8), 1.20, bank_yaw)
		if i % 4 == 3:
			var tree_side: float = -1.0 if int(i / 4) % 2 == 0 else 1.0
			var tree_pos: Vector3 = (a + b) * 0.5 + rt * tree_side * (SLIDE_WIDTH * 0.5 + 7.2)
			m._art35_prop("res://assets/art35/arena/winter_tree_%d.glb" % (int(i / 4) % 3), tree_pos, 1.05, randf() * TAU)
	# A large physical star arch makes the bottom of the run readable from the
	# first bend and replaces the tiny generic finish bar.
	var finish_dir: Vector3 = ((path[path.size() - 1] as Vector3) - (path[path.size() - 2] as Vector3)).normalized()
	var finish_yaw: float = atan2(finish_dir.x, finish_dir.z)
	m._art35_prop("res://assets/art35/arena/slide_finish_arch.glb", path[path.size() - 1] as Vector3, 1.70, finish_yaw)
	# ---- penguins cheering on the banks ----
	for k in range(6):
		var tt: float = 0.12 + 0.72 * float(k) / 5.0
		var ps := _slide_sample(tt * total)
		var side: float = -1.0 if k % 2 == 0 else 1.0
		var peng := _aq_game("Penguin", ps[0] + ps[2] * (side * (SLIDE_WIDTH * 0.5 + 4.0)) + Vector3(0, 2.0, 0), 3.0)
		if peng != null:
			# gen2 creatures face local -X (mover convention): atan2(-t.z, t.x)
			# points the face UP-slope, at the oncoming racer
			peng.rotation.y = atan2(-ps[1].z, ps[1].x) + (0.4 if side > 0.0 else -0.4)
			m._play_clip(peng, "cheer", 0.85 + 0.12 * float(k))   # phase-varied crowd
	m.g["fish"] = []
	if mode == "chase":
		# ---- the baby penguin you race + catch (positioned each frame in _tick_slide) ----
		var baby := _aq_game("Penguin", _slide_sample(40.0)[0] + Vector3(0, SLIDE_RIDE, 0), 2.2)
		m.g["peng_node"] = baby
		m.g["peng_x"] = 0.0
		if baby != null:
			# continuous snow spray kicked up at his tail (+X local: face is -X)
			# so his speed reads even when he's just a dot up the track
			var spray := CPUParticles3D.new()
			spray.amount = 70
			spray.lifetime = 0.7
			spray.direction = Vector3(1.0, 0.7, 0.0)
			spray.spread = 28.0
			spray.initial_velocity_min = 5.0
			spray.initial_velocity_max = 11.0
			spray.gravity = Vector3(0, -16.0, 0)
			spray.scale_amount_min = 0.16
			spray.scale_amount_max = 0.40
			var sbm := BoxMesh.new()
			sbm.size = Vector3(0.3, 0.3, 0.3)
			spray.mesh = sbm
			var spm := StandardMaterial3D.new()
			spm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			# icy BLUE, not white — white spray vanishes into the bright snow
			spm.albedo_color = Color(0.55, 0.8, 1.0)
			spray.material_override = spm
			spray.position = Vector3(1.8, 0.5, 0)
			baby.add_child(spray)
			m.g["peng_spray"] = spray
	else:
		# ---- 5 fish collectables, spaced along the run, alternating sides ----
		var spots := [0.16, 0.34, 0.52, 0.70, 0.86]
		var sides := [-1.0, 1.0, -0.4, 1.0, -1.0]
		for k in range(spots.size()):
			var samp := _slide_sample(float(spots[k]) * total)
			var fpos: Vector3 = samp[0] + samp[2] * (sides[k] * SLIDE_WIDTH * 0.32) + Vector3(0, SLIDE_RIDE + 1.6, 0)
			var fish := _aq_game("ClownFish", fpos, 3.0)
			if fish == null:
				fish = m._check_star(fpos)   # fallback if the model is missing
			var halo := m._halo(fpos, Color(1.0, 0.85, 0.4), 6.0)
			m.game_nodes.append(halo)
			(m.g["fish"] as Array).append({"node": fish, "halo": halo, "pos": fpos, "got": false})
		# ---- a big ball rolling behind, for the "chase" feel (decor only) ----
		var ball := MeshInstance3D.new()
		var bs := SphereMesh.new(); bs.radius = 7.0; bs.height = 14.0
		ball.mesh = bs
		ball.material_override = m._ice_mat(Color(1.0, 0.85, 0.4), 0.5) if theme == "rainbow" else m._ice_mat(Color(0.88, 0.93, 1.0), 0.05, "snow")
		m.add_child(ball); m.game_nodes.append(ball)
		m.g["ball"] = ball
	# ---- place Roshan at the top, facing down the chute ----
	var top := _slide_sample(0.0)
	m.player.position = top[0] + Vector3(0, SLIDE_RIDE, 0)
	m.player.vel = Vector3.ZERO
	m.player.yaw = atan2(top[1].x, top[1].z)

func _slide_dir(i: int) -> Array:
	# tangent + horizontal-right for segment i of the path
	var path: Array = m.g["path"]
	var j: int = clampi(i, 0, path.size() - 2)
	var fwd: Vector3 = (path[j + 1] - path[j]).normalized()
	var right: Vector3 = Vector3.UP.cross(fwd)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [fwd, right.normalized()]

func _slide_pos(s: float) -> Vector3:
	# R1: Catmull-Rom position at arc-length s. The MOTION/CAMERA path is
	# C1-smooth; the plank visuals still sit on the raw polyline (they look
	# fine and the rider floats SLIDE_RIDE above them).
	var path: Array = m.g["path"]
	var cum: Array = m.g["cum"]
	var total: float = m.g["total"]
	s = clampf(s, 0.0, total)
	var i := 0
	while i < cum.size() - 2 and float(cum[i + 1]) < s:
		i += 1
	var seg_len: float = float(cum[i + 1]) - float(cum[i])
	var f: float = 0.0 if seg_len < 0.001 else (s - float(cum[i])) / seg_len
	var p0: Vector3 = path[maxi(i - 1, 0)]
	var p1: Vector3 = path[i]
	var p2: Vector3 = path[mini(i + 1, path.size() - 1)]
	var p3: Vector3 = path[mini(i + 2, path.size() - 1)]
	var f2: float = f * f
	var f3: float = f2 * f
	return ((p1 * 2.0) + (p2 - p0) * f + (p0 * 2.0 - p1 * 5.0 + p2 * 4.0 - p3) * f2 + (p1 * 3.0 - p0 - p2 * 3.0 + p3) * f3) * 0.5

func _slide_sample(s: float) -> Array:
	# returns [pos, tangent, right] at arc-length s along the chute.
	# R1: tangent by central difference of the spline (ds=1.5m), never from
	# segment indices - heading is continuous, no more per-joint yaw snaps.
	var pos := _slide_pos(s)
	var fwd: Vector3 = _slide_pos(s + 1.5) - _slide_pos(s - 1.5)
	var fwd_n: Vector3 = fwd.normalized() if fwd.length() > 0.001 else Vector3.FORWARD
	var right: Vector3 = Vector3.UP.cross(fwd_n)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [pos, fwd_n, right.normalized()]

func _tick_slide(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var total: float = m.g["total"]
	var s: float = m.g["s"]
	var samp := _slide_sample(s)
	var tangent: Vector3 = samp[1]
	var right: Vector3 = samp[2]
	# --- steering input (left/right only) ---
	var steer := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		steer -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		steer += 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		steer += jx
	if m.touch_ui != null and absf(m.touch_ui.stick_vec.x) > 0.15:
		steer += m.touch_ui.stick_vec.x
	steer = clampf(steer, -1.0, 1.0)
	if absf(steer) > 0.15:
		m.g["steered"] = true
	# --- along-slope physics: gravity pulls down the gradient, drag caps speed ---
	var v: float = m.g["v"]
	var grade: float = -tangent.y          # >0 going downhill
	v += (SLIDE_GRAV * grade - SLIDE_FRICT * v) * delta
	v = clampf(v, SLIDE_VMIN, SLIDE_VMAX)
	m.g["v"] = v
	m.g["s"] = s + v * delta
	# --- lateral steering with damping + soft walls ---
	# (negated: the chase-cam looks down +tangent, so the chute's "right" vector
	#  is screen-left — flip so pressing right steers screen-right)
	var vx: float = m.g["vx"]
	vx -= steer * SLIDE_STEER * delta
	vx *= pow(0.02, delta)
	var x: float = float(m.g["x"]) + vx * delta
	var lim: float = SLIDE_WIDTH * 0.5 - 2.0
	if absf(x) > lim:
		x = clampf(x, -lim, lim)
		vx *= -0.3                         # gentle bounce off the ice banks
	m.g["x"] = x
	m.g["vx"] = vx
	# --- place + orient Roshan ---
	var pos: Vector3 = samp[0] + right * x + Vector3(0, SLIDE_RIDE, 0)
	m.player.position = pos
	m.player.yaw = atan2(tangent.x, tangent.z)
	m.player.rotation = Vector3(-0.35, m.player.yaw + PI, -clampf(vx * 0.02, -0.5, 0.5))
	# --- chase camera, locked behind and above ---
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var cam_target: Vector3 = pos - tangent * 15.0 + Vector3(0, 7.0, 0)
		m.player.cam.position = m.player.cam.position.lerp(cam_target, 1.0 - pow(0.0008, delta))
		m.player.cam.look_at(pos + tangent * 6.0 + Vector3(0, 1.0, 0))
	if String(m.g.get("mode", "fish")) == "chase":
		# ===== RACE THE BABY PENGUIN — the BEAN PUZZLE =====
		# Without magic beans he is simply too fast: his lead never shrinks into catch
		# range and he crosses the finish first. EAT BEANS (Pearl Shop) and Roshan gets
		# the super-speed to reel him in — that's the puzzle.
		var p: float = s / total
		var beany: bool = m.beans_t >= 0.0 or bool(m.g.get("beany", false))
		m.g["beany"] = beany   # latch: beans active at any point during the ride count
		var gap: float
		if beany:
			gap = maxf(0.0, SLIDE_LEAD * (1.0 - p * 1.45))   # bean power: reel him in!
		else:
			# NO catch without beans (owner 2026-07-12, supersedes the old
			# "he tires at the bottom" window): the gap teases shut, but the
			# moment Roshan gets close he PANICS — a burst of speed rockets
			# him ahead again. Repeated near-misses sell "he's too speedy";
			# the Pearl Shop beans are the real answer.
			var burst: float = float(m.g.get("burst", 0.0))
			var base_gap: float = SLIDE_LEAD * maxf(0.18, 1.0 - p * 0.75)
			if base_gap + burst < 10.0:
				burst = minf(burst + 34.0 * delta, 18.0)
				m.g["panic_cool"] = float(m.g.get("panic_cool", 5.0)) - delta
				if float(m.g["panic_cool"]) <= 0.0:
					m.g["panic_cool"] = 5.0
					var pn0 = m.g.get("peng_node")
					if pn0 != null and is_instance_valid(pn0):
						m._sparkle_burst((pn0 as Node3D).position + Vector3(0, 1.5, 0), Color(0.7, 0.9, 1.0))
					if m.peng_giggle != null:
						m.peng_giggle.pitch_scale = 1.0 + randf() * 0.15   # cheeky escape giggle
						m.peng_giggle.play()
					if int(m.g.get("panic_n", 0)) < 2:
						m.g["panic_n"] = int(m.g.get("panic_n", 0)) + 1
						m.show_msg(fr["fname"], "WHEEE! He zoomed away! Maybe magic BEANS from the Pearl Shop would help!")
			else:
				burst = maxf(0.0, burst - 3.5 * delta)
			m.g["burst"] = burst
			gap = base_gap + burst
		var peng_s: float = minf(s + gap, total)
		# he FLEES sideways away from Roshan (slower than she can steer), pinned by the
		# chute walls — so a passive player never catches him; you must corner him.
		var px: float = float(m.g.get("peng_x", 0.0))
		var flee_dir: float = signf(px - x)
		if flee_dir == 0.0:
			flee_dir = 1.0 if sin(float(m.g["t"]) * 1.3) >= 0.0 else -1.0
		px += flee_dir * 7.5 * delta
		px += sin(float(m.g["t"]) * 2.5) * 1.2 * delta            # lively wander
		px = clampf(px, -lim, lim)
		m.g["peng_x"] = px
		var psamp := _slide_sample(peng_s)
		var pbpos: Vector3 = psamp[0] + psamp[2] * px + Vector3(0, SLIDE_RIDE, 0)
		var pnode = m.g.get("peng_node")
		if pnode != null and is_instance_valid(pnode):
			var pnd := pnode as Node3D
			pnd.position = pbpos
			var sprinting: bool = float(m.g.get("burst", 0.0)) > 0.5 or (beany and gap < 13.0)
			# gen2 creatures face local -X (mover convention): atan2(t.z, -t.x)
			# points his face DOWN-slope, the way he's racing. Euler is YXZ, so
			# z = innermost = nose-down luge lean, x = body shimmy roll.
			var pyaw: float = atan2(psamp[1].z, -psamp[1].x)
			var shimmy: float = sin(float(m.g["t"]) * (13.0 if sprinting else 9.0)) * (0.12 if sprinting else 0.18)
			pnd.rotation = Vector3(shimmy, pyaw, 0.30 if sprinting else 0.12)
			# rigged clips: he's RACING the whole ride — sprint luge always,
			# kicked faster while panicking or being reeled in
			m._play_clip(pnd, "sprint", 1.6 if sprinting else 1.1)
			var spray = m.g.get("peng_spray")
			if spray != null and is_instance_valid(spray):
				(spray as CPUParticles3D).speed_scale = 1.7 if sprinting else 1.0
		# catch when you've cornered him — BEANS ONLY (he escapes anyone slower)
		if beany and bool(m.g.get("steered", false)) and not bool(m.g.get("caught", false)) and gap < 9.0 and absf(x - px) < 4.5:
			m.g["caught"] = true
			m.award_sticker("penguin")
			var cn = m.g.get("peng_node")
			if cn != null and is_instance_valid(cn):
				m._play_clip(cn as Node3D, "cheer", 1.0)
			m._sparkle_burst(pbpos + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.4))
			if m.peng_giggle != null:
				m.peng_giggle.pitch_scale = 0.95
				m.peng_giggle.play()
			if m.chime != null:
				m.chime.pitch_scale = 1.5; m.chime.play()
			m._end_game(true, fr, "You caught the baby penguin! Hee hee, great race!")
			return
		if beany:
			m.hud_game.text = "BEAN POWER! Catch him!   ← →" if p > 0.3 else "Beans! Toot toot! GO GO GO!"
		elif float(m.g.get("burst", 0.0)) > 0.5:
			m.hud_game.text = "WHEE — too speedy! Beans from the Pearl Shop! ← →"
		else:
			m.hud_game.text = "Catch the baby penguin! ...he's SO fast!"
		if float(m.g["s"]) >= total - 0.5:
			if bool(m.g.get("steered", false)):
				m._end_game(true, fr, "What a race! The baby penguin zoomed ahead — and wants to race you again! Magic Beans can help you catch him.")
			else:
				# Auto-slide alone cannot complete the activity. Restart at the top
				# and demonstrate the one deliberate verb without a loss screen.
				m.g["s"] = 0.0
				m.g["x"] = 0.0
				m.g["vx"] = 0.0
				m.g["burst"] = 0.0
				m.show_msg(fr["fname"], "Lean LEFT or RIGHT to join the race! Take your time.", "hint")
			return
	else:
		# ===== COLLECT THE FISH =====
		# rolling chase snowball behind (decor)
		if m.g.has("ball") and is_instance_valid(m.g["ball"]):
			var bsamp := _slide_sample(maxf(0.0, s - 26.0))
			(m.g["ball"] as Node3D).position = bsamp[0] + Vector3(0, 5.0, 0)
			(m.g["ball"] as Node3D).rotate_x(delta * 3.0)
		for fd in m.g.get("fish", []):
			if fd["got"]:
				continue
			if (fd["pos"] as Vector3).distance_to(pos) < 4.2:
				fd["got"] = true
				m.g["got"] = int(m.g["got"]) + 1
				var fn: Node = fd["node"]
				if is_instance_valid(fn):
					fn.queue_free()
				var fh: Node = fd["halo"]
				if is_instance_valid(fh):
					fh.queue_free()
				m._sparkle_burst(pos + Vector3(0, 1.5, 0), Color(1.0, 0.85, 0.4))
				if m.chime != null:
					m.chime.pitch_scale = 1.0 + 0.12 * float(m.g["got"])
					m.chime.play()
		m.hud_game.text = "Slide!  Fish: %d / 5" % int(m.g["got"])
		if float(m.g["s"]) >= total - 0.5:
			var got: int = int(m.g["got"])
			if bool(m.g.get("steered", false)):
				var msg := "WHEEE! You grabbed every fish! Best slider ever!" if got >= 5 else "What a ride! You caught %d fish!" % got
				m._end_game(true, fr, msg)
			else:
				m.g["s"] = 0.0
				m.g["x"] = 0.0
				m.g["vx"] = 0.0
				m.show_msg(fr["fname"], "Lean LEFT or RIGHT to join the slide! Take your time.", "hint")

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.g["chains"] = []
	_build_playplace(origin, fr)
	m.show_msg(fr["fname"], "Welcome to the play place! Touch the sparkles all the way up to the BIG slide!")

func build_slide(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0   # no countdown — reaching the bottom ends it (~12s run)
	var theme: String = String(fr.get("theme", "ice"))
	var mode: String = String(fr.get("mode", "fish"))
	m.g["mode"] = mode
	_build_slide(origin, theme, mode)
	m._play_music("fetch")   # reuse the snowy track
	if theme == "rainbow":
		m.arena_env.background_color = Color(0.52, 0.72, 0.92)
		m.arena_env.ambient_light_color = Color(0.88, 0.90, 1.0)
		m.arena_env.ambient_light_energy = 0.62
		m._apply_scene_grade(m.arena_env, "bright_pastel")
	if mode == "chase":
		if m.beans_t >= 0.0:
			m.show_msg(fr["fname"], "BEANS POWER! Now catch that speedy penguin! GO GO GO!")
		else:
			m.show_msg(fr["fname"], "Race the baby penguin! Careful — he's SO speedy!")
			# non-reader breadcrumb to the beans: Roshan thinks out loud
			m.get_tree().create_timer(3.6).timeout.connect(func():
				if m.game == "slide" and String(m.g.get("mode", "")) == "chase" and m.beans_t < 0.0:
					m.show_msg("Roshan", "I sure am hungry... I bet I'd be faster after a good MEAL!", "hungry"))
	else:
		m.show_msg(fr["fname"], "Whooosh down the ice! Lean LEFT and RIGHT to grab all 5 fish!")

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m._tick_chains(delta, ppos)
	if m.g.has("mover_node"):
		var mvn: MeshInstance3D = m.g["mover_node"]
		mvn.position = (m.g["mover_base"] as Vector3) + Vector3(sin(float(m.g["t"]) * 0.9) * 6.0, 0, 0)
	# slide ride
	if String(m.g.get("phase", "")) == "slide":
		var path: Array = m.g["slide_path"]
		var st: float = float(m.g.get("slide_t", 0.0)) + delta * 13.0
		m.g["slide_t"] = st
		var total := 0.0
		for i in range(path.size() - 1):
			var seg_len: float = (path[i] as Vector3).distance_to(path[i + 1])
			if st <= total + seg_len:
				m.player.position = (path[i] as Vector3).lerp(path[i + 1], (st - total) / seg_len)
				m.player.vel = Vector3.ZERO
				m.hud_game.text = "WHEEEEE!"
				return
			total += seg_len
		m._sparkle_burst(m.player.position, Color(0.5, 0.85, 1.0))
		if m.chime != null:
			m.chime.play()
		m._end_game(true, fr, "What a SLIDE! Best play place ever!" if m.game == "race" else "")
		return
	var checks: Array = m.g.get("checks", [])
	var done := 0
	var nxt: Dictionary = {}
	for c in checks:
		if c["hit"]:
			done += 1
		elif nxt.is_empty():
			nxt = c
	m.hud_game.text = ("Climb the play place! Sparkles: %d / %d" if m.game == "race" else "Dive the caverns! Sparkles: %d / %d") % [done, checks.size()]
	if nxt.is_empty():
		return
	var node: Node3D = nxt["node"]
	node.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 5.0) * 0.15)
	node.rotate_z(delta * 0.75)
	# Phase 6: the FIRST sparkle must be earned — swim toward it to arm the
	# course. Until armed the magnet is off and checkpoints are inert, so a
	# player who does nothing goes nowhere; one little push starts the ride
	# and the magnet forgiveness carries her from there. Guide sparkles
	# point the way while she idles.
	var cprev: Vector3 = m.g.get("ppos_prev", ppos)
	var cvel: Vector3 = (ppos - cprev) / maxf(delta, 0.001)
	m.g["ppos_prev"] = ppos
	if not bool(m.g.get("armed", false)):
		var to_c: Vector3 = node.position - ppos
		if to_c.length() > 0.5 and cvel.dot(to_c.normalized()) > 2.0:
			m.g["arm_t"] = float(m.g.get("arm_t", 0.0)) + delta
			if float(m.g["arm_t"]) >= 0.2:
				m.g["armed"] = true
				m._sparkle_burst(ppos, Color(1.0, 0.95, 0.6))
		else:
			m.g["arm_t"] = 0.0
			m.g["guide_t"] = float(m.g.get("guide_t", 0.0)) - delta
			if float(m.g["guide_t"]) <= 0.0:
				m.g["guide_t"] = 0.8
				m._sparkle_burst(ppos.lerp(node.position, 0.35), Color(1.0, 0.9, 0.5))
				m._sparkle_burst(ppos.lerp(node.position, 0.65), Color(1.0, 0.9, 0.5))
			m.g["arm_hint_t"] = float(m.g.get("arm_hint_t", 0.0)) + delta
			if float(m.g["arm_hint_t"]) > 6.0 and not bool(m.g.get("arm_hinted", false)):
				m.g["arm_hinted"] = true
				m.show_msg(String(fr.get("fname", "Play Place")), "Swim to the twinkly sparkle to start!", "hint")
		if not bool(m.g.get("armed", false)):
			return
	var dd2: float = node.position.distance_to(ppos)
	# strong, far-reaching magnet carries a 4yo up the play-place automatically
	if dd2 < 34.0:
		m.player.position = m.player.position.lerp(node.position, minf(0.92, delta * 2.6 * (1.0 - dd2 / 34.0)))
		m.player.vel.y = maxf(m.player.vel.y, 0.0)
	if dd2 < 7.5:
		nxt["hit"] = true
		m._sparkle_burst(node.position, Color(1.0, 0.9, 0.5))
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + float(done) * 0.08
			m.chime.play()
		var kind := String(nxt["kind"])
		if kind == "tramp":
			m.player.vel.y = 26.0
			m.show_msg(fr["fname"], "BOING! Up you go!")
		elif kind == "slide":
			m.g["phase"] = "slide"
			m.g["slide_t"] = 0.0
		elif kind == "chest":
			m.pearl_count += 3
			m._update_hud()
			m._write_save()
			m._sparkle_burst(node.position, Color(1.0, 0.85, 0.3))
			m.award_sticker("treasure")
			m._end_game(true, fr, "TREASURE! +3 rainbow pearls for the Pearl Shop!")
		else:
			node.visible = false
