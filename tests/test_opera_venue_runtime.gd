extends SceneTree

var bad := 0
var launched: Array[int] = []

func _init() -> void:
	call_deferred("run")

func check(label: String, ok: bool) -> void:
	if not ok:
		bad += 1
		print("FAIL: " + label)

func run() -> void:
	root.size = Vector2i(1280, 720)
	var main := ReefMain.new()
	main.chapter2_active = false
	var venue := OperaHouseVenue2D.new()
	var review_root := OS.get_environment("OPERA_REVIEW_ART")
	if not review_root.is_empty():
		for i in range(2):
			venue.background_textures.append(ImageTexture.create_from_image(
				Image.load_from_file(review_root.path_join("venue_%d.png" % i))))
	venue.setup(main, 0, func(index: int) -> void: launched.append(index))
	root.add_child(venue)
	venue.open(0)
	venue.set_process(false)
	for button: Button in venue.buttons:
		var portrait := button.get_node("CareerPortrait") as TextureRect
		check("career portrait stays inside its door", Rect2(Vector2.ZERO, button.size).encloses(Rect2(portrait.position, portrait.size)))
	check("actor retains child-readable authored size", venue.actor.size == Vector2(74, 88))
	check("no decorative status stripe beneath actor", not venue.floor_glow.visible)
	check("fifteen careers plus one mystery", venue.buttons.size() == 15 and venue.mystery_door != null)
	check("four opening doors enabled", venue.buttons.filter(func(b: Button) -> bool: return not b.disabled).size() == 4)
	var start := venue.foot
	venue._choose_career(17)
	check("locked career cannot start moving", venue.foot == start and venue.waypoints.is_empty())
	var mask := 0
	for i in range(12):
		mask |= 1 << OperaVenueNavigation.LIVE_ORDER[i]
	main.opera_stars = mask
	venue.refresh(mask)
	check("all floor access unlocked after twelve", venue.current_stage == 3)
	venue.get_node("LeftElevatorUpper").emit_signal("pressed")
	for i in range(2500): venue._process(1.0 / 60.0)
	check("tap a remote upper landing arrives there", venue.floor_index == 2 and launched.is_empty())
	venue.get_node("LeftElevatorUpper").emit_signal("pressed")
	for i in range(1500): venue._process(1.0 / 60.0)
	check("tap at the upper landing rides down", venue.floor_index == 1 and launched.is_empty())
	venue._choose_career(17)
	for i in range(4000):
		venue._process(1.0 / 60.0)
		if not launched.is_empty(): break
	check("tap upper door travels then launches once", launched == [17] and venue.floor_index == 3)
	launched.clear()
	venue._choose_mystery()
	for i in range(800): venue._process(1.0 / 60.0)
	check("mystery does not launch or award", launched.is_empty() and main.opera_stars == mask)
	venue._choose_career(0)
	for i in range(35): venue._process(1.0 / 60.0)
	venue.point_to(Vector2(530, 689))
	for i in range(2500): venue._process(1.0 / 60.0)
	check("retarget cancels pending career launch", launched.is_empty() and venue.foot.distance_to(Vector2(530, 689)) < 1.0)
	venue._choose_career(17)
	venue.close()
	for i in range(1000): venue._process(1.0 / 60.0)
	check("closing cancels transit launch", launched.is_empty() and venue.waypoints.is_empty())
	venue.open(mask)
	var events: Array[String] = []
	venue.foreground.animation_requested.connect(func(action: StringName, phase: StringName, context: Dictionary) -> void:
		events.append(String(action) + "." + String(phase))
		check("interaction exposes canvas sockets", context.has("hand") and context.has("mouth") and context.has("seat")))
	venue.foreground.animation_requested.connect(func(_action: StringName, phase: StringName, context: Dictionary) -> void:
		if phase == &"reach":
			var expected_right: bool = String(context["object_id"]) == "lemonade"
			check("Roshan faces the physical cart on either side", venue.actor.flip_h == expected_right)
			check("palm socket follows the authored facing", venue.foreground._hand_fraction().x > 0.5 if expected_right else venue.foreground._hand_fraction().x < 0.5))
	await process_frame
	var touch := InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = true
	touch.position = Vector2(70, 480)
	root.push_input(touch, false)
	touch = InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = false
	touch.position = Vector2(70, 480)
	root.push_input(touch, false)
	await process_frame
	check("raw touch targets flower stand", venue.pending_interaction == "flowers")
	venue.point_to(Vector2(530, 689))
	for frame in range(1000): venue._process(1.0 / 60.0)
	for id: String in OperaVenueForeground.OBJECTS:
		venue.foreground.hit_targets[id].emit_signal("pressed")
		for frame in range(3000):
			venue._process(1.0 / 60.0)
			check("bounded petal particles", venue.foreground.particles.size() <= OperaVenueForeground.MAX_PARTICLES)
			if venue.foreground.seated or (venue.waypoints.is_empty() and venue.foreground.active_object.is_empty()):
				break
		check("foreground arrival stays on foyer", venue.floor_index == 0)
		if "couch" in id or id == "planter":
			check("chair touch seats Roshan", venue.foreground.seated and venue.foreground.phase == "seated")
			venue.point_to(Vector2(530, 689))
			for frame in range(400): venue._process(1.0 / 60.0)
			check("tap leaves chair cleanly", not venue.foreground.seated and venue.foreground.actor_offset == Vector2.ZERO)
	check("flower phases performed", "flower.pick" in events and "flower.hold" in events)
	check("drink fills before drinking", events.find("lemonade.fill") >= 0 and events.find("lemonade.fill") < events.find("lemonade.drink"))
	check("cupcake bite performed", "cupcake.bite" in events)
	check("foreground never awards career progress", main.opera_stars == mask and launched.is_empty())
	check("eaten cake stays absent from its tray", venue.foreground.cake_eaten and int(venue.foreground.body_states["snacks"]) == 1)
	check("no independent prop is drawn while idle", not venue.foreground.held_card.visible and not venue.foreground.jug_card.visible)
	# Point to a physical prop from the top floor: both elevators and stairs
	# must be traversed before the hand action starts in the foyer.
	venue.foreground.cancel(true)
	venue.floor_index = 3
	venue.foot = Vector2(820, OperaVenueNavigation.FLOOR_Y[3])
	venue.request_foreground("lemonade")
	var arrived_from_upstairs := false
	for frame in range(5000):
		venue._process(1.0 / 60.0)
		if venue.foreground.active_object == "lemonade":
			arrived_from_upstairs = venue.floor_index == 0
			break
	check("upper-floor tap reaches the actual foyer cart", arrived_from_upstairs)
	venue.foreground.begin("lemonade")
	venue._process(0.71)
	check("pickup removes the actual cup from cart", int(venue.foreground.body_states["lemonade"]) == 1 and venue.foreground.held_card.visible)
	check("held cup retains exact scene scale", venue.foreground.held_size == venue.foreground._part_rect("cup").size)
	venue._process(0.9)
	check("pour removes and tilts the actual pitcher", int(venue.foreground.body_states["lemonade"]) == 3 and venue.foreground.jug_card.visible and absf(venue.foreground.jug_card.rotation) > 0.01)
	venue.foreground.cancel(true)
	check("cancel returns both original cart pieces", int(venue.foreground.body_states["lemonade"]) == 0 and not venue.foreground.held_card.visible and not venue.foreground.jug_card.visible)
	venue.request_foreground("flowers")
	venue.point_to(Vector2(530, 689))
	for frame in range(1500): venue._process(1.0 / 60.0)
	check("retarget cancels queued prop", venue.foreground.active_object.is_empty() and venue.pending_interaction.is_empty())
	venue.foreground.begin("flowers")
	venue._process(1.6)
	check("flower emits petals", venue.foreground.particles.size() == OperaVenueForeground.MAX_PARTICLES)
	venue.close()
	check("close clears props and particles", venue.foreground.active_object.is_empty() and venue.foreground.particles.is_empty() and venue.foreground.held_texture == null)
	venue.open(mask)
	await process_frame
	await process_frame
	if DisplayServer.get_name() != "headless":
		for id: String in ["flowers", "lemonade", "snacks", "left_couch", "planter", "right_couch"]:
			var spec: Dictionary = OperaVenueForeground.OBJECTS[id]
			venue.floor_index = 0
			venue.foot = spec["approach"]
			venue.foreground.reset_scene()
			venue.foreground.begin(id)
			for frame in range(100 if id == "flowers" else 145): venue._process(1.0 / 60.0)
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://tmp/opera-interaction-%s.png" % id)
			venue.foreground.cancel(true)
		for stage in range(4):
			var stage_mask := 0
			for i in range(stage * 4): stage_mask |= 1 << OperaVenueNavigation.LIVE_ORDER[i]
			main.opera_stars = stage_mask
			venue.refresh(stage_mask)
			venue.floor_index = stage
			venue.foot = Vector2(540, OperaVenueNavigation.FLOOR_Y[stage])
			venue._update_actor()
			venue.guide_current_floor()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://tmp/opera-stage-%d.png" % stage)
	print("OPERA VENUE RUNTIME ALL OK" if bad == 0 else "OPERA VENUE RUNTIME FAIL %d" % bad)
	venue.close()
	venue.queue_free()
	main.free()
	quit(0 if bad == 0 else 1)
