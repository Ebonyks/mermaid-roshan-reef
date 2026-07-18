class_name DollsGame
extends RefCounted
# Phase 7.4 extraction, rebuilt Phase 8 on the SideScrollStage engine: the
# catch-the-babies game is now a 2.5D nursery diorama — the real 3D Roshan
# (wardrobe skin and all) slides under a side-on camera catching 3D swaddled
# babies that drift down in front of the floating nursery book page. Caught
# babies tuck into a cradle; missed ones land safely on pillows (no fail).
# All state stays on main (m.*); received by reference.
# Scale: the v4 Roshan is ~7 world units tall — the 2D era's geometry maps
# at 25 px per unit (1160 px playfield → 46.4 units).

const BLANKETS := [Color(0.62, 0.90, 0.78), Color(1.0, 0.72, 0.82), Color(0.78, 0.72, 0.98)]
const HALF_W := 23.2       # stage half-width
const SPAWN_Y := 28.0      # babies drift down from here (stage-local)
const CATCH_Y := 8.8       # below this they can land in her arms…
const FLOOR_Y := 1.2       # …and at this height they missed (soft pillow landing)
const CATCH_W := 5.4       # horizontal catch forgiveness
const CRADLE_SLOTS := [Vector3(17.8, 3.1, -2), Vector3(20.0, 3.1, -2), Vector3(22.2, 3.1, -2)]

var m: ReefMain
var stage: SideScrollStage

func _init(main: ReefMain) -> void:
	m = main
	stage = SideScrollStage.new(main)

func build(fr: Dictionary, _origin: Vector3) -> void:
	m.g["spawned"] = 0
	m.g["caught"] = 0
	m.g["resolved"] = 0
	m.g["missed"] = 0
	m.g["next"] = 0.6
	m.g["dolls"] = []
	m.g["timer"] = -1.0
	_stage_open()
	m.show_msg(fr["fname"], "Catch 3 sleepy dolls in your arms!")

func _tick_dolls(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var r := stage.root()
	if r == null:
		return
	var s: Dictionary = stage.tick(delta)
	# Phase 6 verb gate, unchanged from the 2D era: catching needs a live hand
	# on the controls inside the last 2s — a passive run must never fluke 3
	# catches, even with the mercy drops steering toward her.
	if bool(s["moved"]):
		m.g["verb_t"] = 2.0
	else:
		m.g["verb_t"] = maxf(0.0, float(m.g.get("verb_t", 0.0)) - delta)
	var hands_on: bool = float(m.g.get("verb_t", 0.0)) > 0.0
	m.g["next"] = float(m.g["next"]) - delta
	if float(m.g["next"]) <= 0.0 and int(m.g["caught"]) < 3:
		m.g["spawned"] = int(m.g["spawned"]) + 1
		m.g["next"] = 1.2
		var missed: int = int(m.g["missed"])
		var drop_x: float = -HALF_W + 3.2 + randf() * (HALF_W * 2.0 - 6.4)
		if missed >= 2:
			# mercy: later babies drift down nearer Roshan, and slower
			var spread: float = maxf(1.4, 8.8 - float(missed - 2) * 1.4)
			drop_x = clampf(float(s["px"]) + randf_range(-spread, spread), -HALF_W, HALF_W)
		var baby := _make_baby(int(m.g["spawned"]))
		baby.position = Vector3(drop_x, SPAWN_Y, 0)
		baby.set_meta("fall_speed", maxf(4.2, 7.6 - float(missed) * 0.6))
		r.add_child(baby)
		(m.g["dolls"] as Array).append(baby)
	var dolls: Array = m.g["dolls"]
	for i in range(dolls.size() - 1, -1, -1):
		var baby: Node3D = dolls[i]
		baby.position.y -= float(baby.get_meta("fall_speed", 7.6)) * delta
		baby.position.x += sin(float(m.g["t"]) * 1.6 + float(i) * 2.0) * 2.4 * delta
		baby.rotation.z = sin(float(m.g["t"]) * 2.0 + float(i)) * 0.25
		var caught: bool = hands_on and baby.position.y < CATCH_Y and absf(baby.position.x - float(s["px"])) < CATCH_W
		if caught:
			m.g["caught"] = int(m.g["caught"]) + 1
			m.g["resolved"] = int(m.g["resolved"]) + 1
			dolls.remove_at(i)
			m._sparkle_burst(baby.global_position, Color(1.0, 0.75, 0.9))
			_tuck_in(baby, int(m.g["caught"]) - 1)
			if m.voice != null:
				m.voice.pitch_scale = 1.0 + randf() * 0.25
				m.voice.play()
		elif baby.position.y < FLOOR_Y:
			m.g["resolved"] = int(m.g["resolved"]) + 1
			m.g["missed"] = int(m.g["missed"]) + 1
			# a baby got away! Faron gasps (min-gap so two misses don't overlap)
			m._say("faron", "miss", 3.0)
			dolls.remove_at(i)
			_land_on_pillow(baby)
	m.hud_game.text = "Sleepy dolls caught: %d  (catch 3 to win!)" % int(m.g["caught"])
	if int(m.g["caught"]) >= 3:
		m._end_game(true, fr, "You tucked in %d dolls! All cozy now." % int(m.g["caught"]))

func stage_close() -> void:
	stage.close()

# ---- the nursery diorama ---------------------------------------------------
func _stage_open() -> void:
	stage.open({
		"origin": m.ARENA_POS + Vector3(0, 2.5, 0),
		"half_w": HALF_W,
		"hover": 3.0,
		"bob_amp": 0.5,
		"steer_speed": 24.8,
		"cam_h": 12.0,
		"cam_dist": 20.5,
		"look_h": 10.5,
		"cam_follow": 0.25,
		"backdrop": "res://assets/book/nursery_bg.jpg",
		"backdrop_size": Vector2(36.0, 49.8),   # the book page at its true portrait aspect
		"backdrop_z": -28.0,
	})
	var r := stage.root()
	# soft pillow row where missed babies land
	for i in range(7):
		var p := MeshInstance3D.new()
		var pmesh := SphereMesh.new()
		pmesh.radius = 3.4
		pmesh.height = 6.8
		p.mesh = pmesh
		p.scale = Vector3(1.25, 0.42, 0.9)
		p.position = Vector3(-21.0 + float(i) * 7.0, 0.5, 0.0)
		p.material_override = m._soft_mat((BLANKETS[i % BLANKETS.size()] as Color).lightened(0.25), 0.08)
		r.add_child(p)
	# the cradle caught babies tuck into (screen right, just behind the play line)
	var base := MeshInstance3D.new()
	var bmesh := BoxMesh.new()
	bmesh.size = Vector3(8.4, 2.0, 4.0)
	base.mesh = bmesh
	base.position = Vector3(20.0, 1.0, -2.0)
	base.material_override = m._soft_mat(Color(0.85, 0.72, 0.58), 0.08)
	r.add_child(base)
	for ex in [15.9, 24.1]:
		var board := MeshInstance3D.new()
		var bomesh := BoxMesh.new()
		bomesh.size = Vector3(0.6, 4.0, 4.0)
		board.mesh = bomesh
		board.position = Vector3(float(ex), 2.0, -2.0)
		board.material_override = m._soft_mat(Color(0.85, 0.72, 0.58), 0.08)
		r.add_child(board)
	# toy blocks (screen left) + dream sky: moon and stars around the book page
	for k in range(3):
		var blk := MeshInstance3D.new()
		var blmesh := BoxMesh.new()
		blmesh.size = Vector3.ONE * 2.2
		blk.mesh = blmesh
		blk.position = [Vector3(-20.5, 1.1, 0), Vector3(-18.3, 1.1, 1.0), Vector3(-19.5, 3.3, 0.4)][k]
		blk.rotation.y = float(k) * 0.4
		blk.material_override = m._soft_mat(BLANKETS[k], 0.14)
		r.add_child(blk)
	var moon := stage.glow(Color(1.0, 0.92, 0.7), 12.8)
	moon.position = Vector3(-26.0, 43.0, -26.5)
	r.add_child(moon)
	for sp in [Vector2(-32, 36), Vector2(-26, 49), Vector2(8, 52), Vector2(24, 41), Vector2(34, 30), Vector2(28, 50)]:
		var star := stage.glow(Color(0.92, 0.9, 1.0), 3.6)
		star.position = Vector3((sp as Vector2).x, (sp as Vector2).y, -27.0)
		r.add_child(star)

func _make_baby(idx: int) -> Node3D:
	# a swaddled 3D baby doll: blanket capsule, head, sleep cap, pompom, halo.
	# Built at doll-scale then×2.6 so it reads about half Roshan's height,
	# matching the book-art dolls' proportion in the 2D era.
	var b := Node3D.new()
	b.scale = Vector3.ONE * 2.6
	var blanket: Color = BLANKETS[idx % BLANKETS.size()]
	var swaddle := MeshInstance3D.new()
	var cmesh := CapsuleMesh.new()
	cmesh.radius = 0.34
	cmesh.height = 0.95
	swaddle.mesh = cmesh
	swaddle.material_override = m._soft_mat(blanket, 0.18)
	b.add_child(swaddle)
	var head := MeshInstance3D.new()
	var hmesh := SphereMesh.new()
	hmesh.radius = 0.24
	hmesh.height = 0.48
	head.mesh = hmesh
	head.position.y = 0.52
	head.material_override = m._soft_mat(Color(1.0, 0.86, 0.72), 0.10)
	b.add_child(head)
	var cap := MeshInstance3D.new()
	var cymesh := CylinderMesh.new()
	cymesh.top_radius = 0.03
	cymesh.bottom_radius = 0.20
	cymesh.height = 0.26
	cap.mesh = cymesh
	cap.position.y = 0.74
	cap.material_override = m._soft_mat(blanket.darkened(0.25), 0.15)
	b.add_child(cap)
	var pom := MeshInstance3D.new()
	var pommesh := SphereMesh.new()
	pommesh.radius = 0.06
	pommesh.height = 0.12
	pom.mesh = pommesh
	pom.position.y = 0.89
	pom.material_override = m._soft_mat(Color(1, 1, 1), 0.5)
	b.add_child(pom)
	var halo := stage.glow(Color(0.8, 0.75, 1.0), 2.0)
	halo.position.y = 0.3
	b.add_child(halo)
	return b

func _tuck_in(baby: Node3D, slot: int) -> void:
	var tw := baby.create_tween()
	tw.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	tw.tween_property(baby, "position", CRADLE_SLOTS[clampi(slot, 0, 2)] as Vector3, 0.7)
	tw.parallel().tween_property(baby, "rotation", Vector3.ZERO, 0.7)

func _land_on_pillow(baby: Node3D) -> void:
	# no-fail kindness: the baby flops safely onto the pillows, then Faron
	# quietly scoops it away off-screen
	var tw := baby.create_tween()
	tw.tween_property(baby, "position:y", 1.5, 0.35).set_ease(Tween.EASE_OUT)
	tw.parallel().tween_property(baby, "rotation:z", 1.35, 0.35)
	tw.tween_interval(1.1)
	tw.tween_property(baby, "scale", Vector3.ONE * 0.01, 0.45).set_ease(Tween.EASE_IN)
	tw.tween_callback(baby.queue_free)
