extends SceneTree
# Dedicated win and Daddy Mermaid animation probe for the melody orb-catch
# game, split out so an early audit death cannot silently drop coverage.

const DADDY_IDLE: Texture2D = preload("res://assets/characters/daddy_25d/daddy_idle.png")
const DADDY_SWIM: Texture2D = preload("res://assets/characters/daddy_25d/daddy_swim.png")
const DADDY_GESTURES: Texture2D = preload("res://assets/characters/daddy_25d/daddy_gesture_a.png")

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
	main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	var fr: Dictionary = {}
	for f: Dictionary in main.friends:
		if String(f["game"]) == "melody":
			fr = f
	if fr.is_empty():
		_ck("melody friend is registered", false)
		print("MELODY|result: %d check(s) FAILED" % bad)
		quit()
		return
	print("MELODY|boot OK friend=", fr["fname"])
	main._start_game(fr)
	await process_frame
	var melody: MelodyGame = main._games.get("melody") as MelodyGame
	var performer: Sprite3D = null
	if melody != null and melody.stage_root != null:
		performer = melody.stage_root.get_node_or_null("StarPerformer") as Sprite3D
	_ck("StarPerformer is the authoritative idle Daddy sprite",
		performer != null and melody.performer_animator != null
		and performer.texture == DADDY_IDLE
		and performer.hframes == 4 and performer.vframes == 2
		and melody.performer_animator.animation_state() == "idle"
		and bool(performer.get_meta("daddy_sprite_authoritative", false)))
	if performer == null or melody == null or melody.performer_animator == null:
		print("MELODY|result: %d check(s) FAILED" % bad)
		quit()
		return

	melody.performer_animator.set_moving(true)
	melody.performer_animator._process(0.01)
	_ck("explicit movement selects the tail-swimming loop",
		performer.texture == DADDY_SWIM
		and melody.performer_animator.animation_state() == "swim")
	melody.performer_animator.set_moving(false)

	melody.performer_animator.play_hug()
	_ck("hug uses the fourth gesture row",
		performer.texture == DADDY_GESTURES
		and melody.performer_animator.animation_state() == "hug"
		and melody.performer_animator.current_frame() >= 12
		and melody.performer_animator.current_frame() < 16)
	melody.performer_animator.play_wave()
	_ck("wave uses the first gesture row",
		performer.texture == DADDY_GESTURES
		and melody.performer_animator.animation_state() == "wave"
		and melody.performer_animator.current_frame() >= 0
		and melody.performer_animator.current_frame() < 4)

	player.position = main.ARENA_POS + Vector3(0, 8, 0)
	player.vel = Vector3.ZERO
	main.g["still_t"] = 8.01
	main.g["hinted"] = false
	main.g["ppos_prev"] = player.position
	melody._tick_melody(0.1, fr, player.position)
	_ck("eight seconds still triggers Daddy's invite gesture",
		bool(main.g.get("hinted", false))
		and int(main.g.get("caught", -1)) == 0
		and performer.texture == DADDY_GESTURES
		and melody.performer_animator.animation_state() == "invite"
		and melody.performer_animator.current_frame() >= 4
		and melody.performer_animator.current_frame() < 8)
	_ck("stationary Roshan cannot fluke an orb catch",
		int(main.g.get("caught", -1)) == 0)

	var orbs: Array = main.g.get("orbs", [])
	_ck("melody builds seven catchable colors", orbs.size() == 7)
	if orbs.size() != 7:
		print("MELODY|result: %d check(s) FAILED" % bad)
		quit()
		return
	var original_positions: Array[Vector3] = []
	var original_velocities: Array[Vector3] = []
	for i in range(orbs.size()):
		var ob: Dictionary = orbs[i]
		var orb_node: MeshInstance3D = ob["node"]
		original_positions.append(orb_node.position)
		original_velocities.append(ob["vel"] as Vector3)
		if i == 0:
			orb_node.position = player.position + Vector3(1.0, 0.0, 0.0)
			ob["vel"] = Vector3.ZERO
		else:
			ob["caught"] = true
	main.g["ppos_prev"] = player.position - Vector3(1.0, 0.0, 0.0)
	melody._tick_melody(0.1, fr, player.position)
	_ck("a nonfinal orb catch triggers Daddy's clap",
		int(main.g.get("caught", 0)) == 1
		and performer.texture == DADDY_GESTURES
		and melody.performer_animator.animation_state() == "clap"
		and melody.performer_animator.current_frame() >= 8
		and melody.performer_animator.current_frame() < 12)

	# Restore five real targets and keep the seventh temporarily held out. This
	# preserves the original probe's approach-velocity drive through the game,
	# while guaranteeing the final catch can be checked in its exact tick.
	for i in range(1, orbs.size()):
		var ob: Dictionary = orbs[i]
		var orb_node: MeshInstance3D = ob["node"]
		orb_node.position = original_positions[i]
		ob["vel"] = original_velocities[i]
		ob["caught"] = i == orbs.size() - 1

	var fcount := 0
	var last_caught := 1
	while main.game == "melody" and int(main.g.get("caught", 0)) < 6 \
			and fcount < 60 * 90:
		fcount += 1
		var caught: int = int(main.g.get("caught", 0))
		if caught != last_caught or fcount % 900 == 0:
			print("MELODY|f=", fcount, " caught=", caught, "/7")
			last_caught = caught
		for ob_value: Variant in orbs:
			var ob: Dictionary = ob_value
			if not bool(ob["caught"]):
				player.position = player.position.lerp(
					(ob["node"] as Node3D).position, 0.14)
				player.vel = Vector3.ZERO
				break
		await process_frame
	_ck("approach driving catches six colors without a passive win",
		main.game == "melody" and int(main.g.get("caught", 0)) == 6)
	if main.game != "melody" or int(main.g.get("caught", 0)) != 6:
		print("MELODY|result: %d check(s) FAILED" % bad)
		quit()
		return

	var final_orb: Dictionary = orbs[orbs.size() - 1]
	var final_node: MeshInstance3D = final_orb["node"]
	player.position = main.ARENA_POS + Vector3(0, 8, 0)
	player.vel = Vector3.ZERO
	final_orb["caught"] = false
	final_orb["vel"] = Vector3.ZERO
	final_node.visible = true
	final_node.position = player.position + Vector3(1.0, 0.0, 0.0)
	main.g["ppos_prev"] = player.position - Vector3(1.0, 0.0, 0.0)
	melody._tick_melody(0.1, fr, player.position)
	_ck("the final catch rewards immediately without an animation delay",
		bool(fr.get("won", false)) and main.game != "melody")
	print("MELODY|END game=", main.game, " won=", fr.get("won"), \
		" frames=", fcount)
	print("MELODY|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()
