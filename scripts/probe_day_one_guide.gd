extends SceneTree
# Day One guide gate (owner 2026-08-03).
#
# Two things this covers that nothing else does:
#   1. the cut Huluu storybook opener leaves NO overlay behind — the child goes
#      straight into play while the flight movie is undelivered;
#   2. the three-step movement/interaction guide runs in the Sky Lagoon, in
#      order, completes only on the real action, and never runs twice.
#
# It also holds the no-fail line: the guide must never block input, never time
# out, and never be able to move a step backwards.

var failures := 0
var main: ReefMain

func _check(label: String, ok: bool) -> void:
	print("DAYONEGUIDE|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		failures += 1

func _init() -> void:
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame

	# ---- the opener is gone, and left nothing behind ------------------------
	main._build_intro()
	await process_frame
	_check("no opener overlay while the flight movie is undelivered",
		not main.intro_active and main.intro_layer == null)
	_check("the flight movie has a stable undelivered drop path",
		not ResourceLoader.exists(IntroOverlay.OPENING_VIDEO))
	main._skip_intro()
	await process_frame
	_check("_skip_intro is a safe no-op with no opener", not main.intro_active)

	# ---- the guide comes up with the promenade ------------------------------
	main.save_data.erase(DayOneGuide.SAVE_KEY)
	main._enter_level2_now(false, false, true)
	await process_frame
	await process_frame
	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	_check("promenade built the guide on a fresh save",
		promenade != null and promenade.guide != null and promenade.guide.active)
	if promenade == null or promenade.guide == null:
		print("DAYONEGUIDE|RESULT: ", failures, " failure(s)")
		quit()
		return
	var guide: DayOneGuide = promenade.guide

	# The opening line gets its breath before the first instruction; drive the
	# gap out deterministically rather than waiting on wall time.
	for i in range(8):
		guide.tick(0.2)
	_check("step 1 teaches travel first",
		String(main.g.get("lagoon_guide_step", "")) == "walk")
	var pointer: Sprite3D = guide.pointer
	_check("step 1 shows one world-space pointer card",
		pointer != null and is_instance_valid(pointer)
		and not pointer.shaded
		and pointer.billboard == BaseMaterial3D.BILLBOARD_DISABLED)
	_check("the pointer stands above the walk surface, not buried in it",
		pointer != null
		and pointer.position.y > promenade.guide_floor_y(pointer.position.x))
	_check("the guide adds no Control node and cannot block a tap",
		main.get_node_or_null("DayOneGuideLayer") == null)

	# Walking anywhere else must NOT complete the step — a pointer that clears
	# on any movement teaches nothing.
	main.player.position.x = promenade.stage.root().position.x \
		+ guide.walk_goal_x - DayOneGuide.WALK_ARRIVE * 4.0
	guide.tick(0.2)
	_check("walking short of the goal does not complete step 1",
		String(main.g.get("lagoon_guide_step", "")) == "walk")

	# Arriving does.
	main.player.position.x = promenade.stage.root().position.x + guide.walk_goal_x
	guide.tick(0.2)
	for i in range(10):
		guide.tick(0.2)
	_check("arriving completes step 1 and opens step 2",
		String(main.g.get("lagoon_guide_step", "")) == "play")

	# Step 2 is satisfied by a real second press, not by proximity.
	guide.tick(0.2)
	_check("standing near the plane does not complete step 2",
		String(main.g.get("lagoon_guide_step", "")) == "play")
	main.g["lagoon_guide_event"] = "play"
	guide.tick(0.2)
	for i in range(10):
		guide.tick(0.2)
	_check("a second press completes step 2 and opens step 3",
		String(main.g.get("lagoon_guide_step", "")) == "animal")
	_check("step 3 still points somewhere on-stage while no animal is on camera",
		guide.pointer != null and is_instance_valid(guide.pointer))

	# Step 3 completes on a real animal tap, and that finishes the guide.
	main.g["lagoon_guide_event"] = "animal"
	guide.tick(0.2)
	_check("tapping an animal finishes the guide",
		not guide.active and guide.pointer == null)
	_check("the guide persists as done", bool(
		main.save_data.get(DayOneGuide.SAVE_KEY, false)))
	_check("a finished guide leaves no step marker behind",
		String(main.g.get("lagoon_guide_step", "")) == "")

	# ---- it never runs twice ------------------------------------------------
	_check("a taught save is recognised as finished", DayOneGuide.is_finished(main))
	main._enter_level2_now(false, false, true)
	await process_frame
	await process_frame
	var second: SkyLagoonPromenade = main._lagoon_promenade_ref()
	_check("re-entering the lagoon does not re-teach a taught child",
		second != null and (second.guide == null or not second.guide.active))

	print("DAYONEGUIDE|RESULT: ", failures, " failure(s)")
	if failures == 0:
		print("DAYONEGUIDE|ALL OK")
	quit()
