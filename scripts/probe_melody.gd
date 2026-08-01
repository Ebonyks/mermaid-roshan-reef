extends SceneTree
# Dedicated win probe for Daddy Mermaid's melody orb-catch game (split out of
# probe_audit.gd so an early audit death cannot silently drop coverage).
# Mirrors the audit driving: lerp toward the first uncaught orb each frame —
# the lerp supplies the approach velocity the Phase 6 hold ring requires, so
# a stationary player can never fluke a catch. Win = all 7 colors caught.

const DADDY_IDLE: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_idle.png")
const DADDY_SWIM: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_swim.png")
const DADDY_GESTURES: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_gesture_a.png")

var bad := 0

func _ck(label: String, ok: bool) -> void:
	print("MELODY|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _init() -> void:
	Engine.time_scale = 6.0
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: ReefMain = root.get_child(root.get_child_count() - 1) as ReefMain
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	var fr: Dictionary = {}
	for f in main.friends:
		if String(f["game"]) == "melody":
			fr = f
	if fr.is_empty():
		print("FAIL: no melody friend found in main.friends")
		quit()
		return
	print("MELODY|boot OK friend=", fr["fname"])
	main._start_game(fr)
	await process_frame
	var performer: Sprite3D = main.get_node_or_null(
		"RainbowTheater3D/StarPerformer") as Sprite3D
	var daddy_animator: DaddySpriteLoop = null
	if performer != null and performer.get_child_count() > 0:
		daddy_animator = performer.get_child(0) as DaddySpriteLoop
	_ck("Daddy stage performer uses the idle atlas",
		performer != null and daddy_animator != null
		and performer.texture == DADDY_IDLE
		and performer.hframes == 4 and performer.vframes == 2
		and daddy_animator.animation_state() == "idle")
	daddy_animator.set_moving(true)
	await process_frame
	_ck("explicit movement uses Daddy swim atlas",
		daddy_animator.animation_state() == "swim"
		and performer.texture == DADDY_SWIM
		and performer.hframes == 4 and performer.vframes == 4)
	daddy_animator.set_moving(false)
	await process_frame
	await process_frame
	daddy_animator.play_hug()
	_ck("Daddy hug interaction selects row four",
		daddy_animator.animation_state() == "hug"
		and performer.texture == DADDY_GESTURES and performer.frame == 12)
	daddy_animator.play_wave()
	_ck("Daddy wave interaction selects row one",
		daddy_animator.animation_state() == "wave"
		and performer.texture == DADDY_GESTURES and performer.frame == 0)
	var fcount := 0
	var last_caught := -1
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	main.g["still_t"] = 8.1
	main.g["hinted"] = false
	main.g["ppos_prev"] = player.position
	main._tick_melody(0.01, fr, player.position)
	_ck("eight-second hint plays Daddy invite",
		daddy_animator != null
		and daddy_animator.animation_state() == "invite"
		and performer.texture == DADDY_GESTURES)

	# Catch exactly one orb while the other six are temporarily skipped. This
	# verifies the ordinary feedback path without accidentally reaching the win.
	var orbs_for_clap: Array = main.g.get("orbs", [])
	for i in range(1, orbs_for_clap.size()):
		var skipped_orb: Dictionary = orbs_for_clap[i]
		skipped_orb["caught"] = true
	var first_orb: Dictionary = orbs_for_clap[0]
	var first_orb_node: Node3D = first_orb["node"]
	player.position = first_orb_node.position - Vector3.RIGHT
	main.g["ppos_prev"] = player.position - Vector3.RIGHT
	main._tick_melody(0.05, fr, player.position)
	for i in range(1, orbs_for_clap.size()):
		var skipped_orb: Dictionary = orbs_for_clap[i]
		skipped_orb["caught"] = false
	_ck("first nonfinal catch plays Daddy clap",
		int(main.g.get("caught", 0)) == 1 and main.game == "melody"
		and not bool(fr.get("won", false)) and daddy_animator != null
		and daddy_animator.animation_state() == "clap"
		and performer.texture == DADDY_GESTURES)
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	main.g["ppos_prev"] = player.position
	while main.game == "melody" and fcount < 60 * 90:
		fcount += 1
		var g: Dictionary = main.g
		var caught: int = int(g.get("caught", 0))
		if caught != last_caught or fcount % 900 == 0:
			print("MELODY|f=", fcount, " caught=", caught, "/7")
			last_caught = caught
		var orbs: Array = g.get("orbs", [])
		for ob in orbs:
			if not bool(ob["caught"]):
				player.position = player.position.lerp((ob["node"] as Node3D).position, 0.14)
				player.vel = Vector3.ZERO
				break
		await process_frame
	print("END game=", main.game, " won=", fr.get("won"), " frames=", fcount)
	_ck("final catch awards immediately",
		bool(fr.get("won", false)) and main.game != "melody")
	print("MELODY|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()
