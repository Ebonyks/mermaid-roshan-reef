class_name DollsGame
extends RefCounted
# Phase 7.4 extraction, rebuilt Phase 8 on the SideScrollStage engine: the
# catch-the-babies game is now a 2D-sprite nursery diorama. The real player
# controller slides under a side-on camera while a 2D Roshan catches Faron's
# three protected baby-doll sprites. Caught babies tuck into a regenerated
# cradle; missed ones land safely on regenerated pillows (no fail).
# All state stays on main (m.*); received by reference.
# Scale: the v4 Roshan is ~7 world units tall — the 2D era's geometry maps
# at 25 px per unit (1160 px playfield → 46.4 units).

const HALF_W := 23.2       # stage half-width
const SPAWN_Y := 28.0      # babies drift down from here (stage-local)
const CATCH_Y := 8.8       # below this they can land in her arms…
const FLOOR_Y := 1.2       # …and at this height they missed (soft pillow landing)
const CATCH_W := 5.4       # horizontal catch forgiveness
const CRADLE_SLOTS := [Vector3(11.5, 3.1, -1.0), Vector3(16.0, 3.1, -1.0), Vector3(20.5, 3.1, -1.0)]
const BABY_SPRITES := [
	"res://assets/book/baby_doll.png",
	"res://assets/book/baby_doll2.png",
	"res://assets/book/baby_doll3.png",
]
const BACKGROUND := "res://assets/minigames/dolls/background.png"
const CRADLE := "res://assets/minigames/dolls/cradle.png"
const PILLOW_BANK := "res://assets/minigames/dolls/pillow_bank.png"
const ROSHAN_CATCH := "res://assets/minigames/shared/roshan_catch.png"

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
	m.hud_game.text = "Sleepy dolls  " + m._pips(int(m.g["caught"]), 3, "🎎")
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
		"cam_fov": 58.0,
		"avatar_sprite": ROSHAN_CATCH,
		"backdrop": BACKGROUND,
		"backdrop_size": Vector2(56.0, 28.0),
		"backdrop_z": -28.0,
	})
	stage.flat(PILLOW_BANK, Vector2(48.0, 8.0), 0.0, -1.0, 0.0, false)
	stage.flat(CRADLE, Vector2(16.0, 8.0), 16.0, -2.0, 0.0, false)

func _make_baby(idx: int) -> Node3D:
	# Faron's babies are the protected originals. They remain separate sprites;
	# never bake them into a background, redraw, recolor, resize in place, or
	# route them through generated fallback art.
	var b := Node3D.new()
	var tex: Texture2D = load(BABY_SPRITES[idx % BABY_SPRITES.size()])
	var sprite := Sprite3D.new()
	sprite.texture = tex
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.pixel_size = 4.2 / maxf(1.0, float(tex.get_height()))
	sprite.position.y = 2.1
	b.add_child(sprite)
	var halo := stage.glow(Color(0.8, 0.75, 1.0), 2.0)
	halo.position.y = 2.0
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
