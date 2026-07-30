extends SceneTree
# Sprite animation contract: every Roshan verb must visit all four authored
# atlas frames and finish, while both 16-frame swim views and playground poses
# remain selectable. No character skeleton may exist below the player.
const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")

func _count_skeletons(node: Node) -> int:
	var total := 1 if node is Skeleton3D else 0
	for child in node.get_children():
		total += _count_skeletons(child)
	return total

func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(20):
		await process_frame
	var pl: Node = main.player
	if pl == null:
		print("FAIL: no player for Roshan sprite probe")
		quit()
		return
	if pl.classic_sprite == null or not pl.classic_sprite.visible:
		print("FAIL: primary Roshan 2.5D sprite is missing or hidden")
	if _count_skeletons(pl) != 0:
		print("FAIL: retired character skeleton still exists below Roshan")
	var expected_sizes: Dictionary = {
		"directional": Vector2i(1024, 512),
		"swim_front": Vector2i(1024, 1024),
		"swim_back": Vector2i(1024, 1024),
		"gesture_a": Vector2i(1024, 1024),
		"gesture_b": Vector2i(1024, 1024),
		"gesture_c": Vector2i(1024, 1024),
		"gesture_d": Vector2i(1024, 512),
		"play_a": Vector2i(1024, 1024),
		"play_b": Vector2i(1024, 1024),
	}
	for sheet_key in expected_sizes:
		var sheet_name := String(sheet_key)
		var sheet_spec: Array = pl.ROSHAN_25D_SHEETS[sheet_name]
		var sheet_tex: Texture2D = sheet_spec[0]
		var actual_size := Vector2i(sheet_tex.get_width(), sheet_tex.get_height())
		var expected_size: Vector2i = expected_sizes[sheet_name]
		if actual_size != expected_size:
			print("FAIL: Roshan atlas ", sheet_name, " is ", actual_size,
				", expected ", expected_size)
	var original_key_count: int = pl.VERB_LIB.size() + 1 \
		+ pl.ROSHAN_25D_PLAY.size() + 8
	var expanded_key_count: int = (pl.ROSHAN_25D_GESTURES.size()
		+ pl.ROSHAN_25D_PLAY.size()) * int(pl.ROSHAN_25D_KEYFRAMES) + 32
	if expanded_key_count != original_key_count * 4:
		print("FAIL: Roshan keyframe expansion is ", original_key_count, " -> ",
			expanded_key_count, ", expected exactly 4x")
	else:
		print("sprite keyframes: ", original_key_count, " -> ",
			expanded_key_count, " (exactly 4x)")
	if pl.play_verb("nonsense"):
		print("FAIL: play_verb accepted an unknown verb")
	for verb_key in pl.VERB_LIB:
		var vname := String(verb_key)
		var spec: Dictionary = pl.VERB_LIB[vname]
		if not pl.play_verb(vname):
			print("FAIL: play_verb rejected ", vname)
			continue
		await process_frame
		var sprite_sequence: Array = pl.ROSHAN_25D_GESTURES[vname]
		var expected_sheet := String(sprite_sequence[0])
		var expected_base: int = int(sprite_sequence[1]) * int(pl.ROSHAN_25D_KEYFRAMES)
		var observed_frames: Dictionary = {}
		var deadline: int = Time.get_ticks_msec() + int((float(spec["len"]) + 2.5) * 1000.0)
		while String(pl.verb) == vname and Time.get_ticks_msec() < deadline:
			if String(pl.classic_sprite_sheet) == expected_sheet:
				observed_frames[int(pl.classic_sprite.frame)] = true
			await process_frame
		if String(pl.verb) == vname:
			print("FAIL: verb ", vname, " never finished")
		for phase in range(int(pl.ROSHAN_25D_KEYFRAMES)):
			var expected_frame: int = expected_base + phase
			if not observed_frames.has(expected_frame):
				print("FAIL: verb ", vname, " never displayed ",
					expected_sheet, " frame ", expected_frame)
		print("verb ", vname, ": ", observed_frames.size(), "/4 sprite frames")
		for i in range(5):
			await process_frame
	# With controls suspended by an overlay, Roshan must still visibly breathe
	# and advance her idle atlas. This exercises the early-return path that used
	# to freeze on one directional card.
	pl.verb = ""
	pl.verb_t = 0.0
	pl.vel = Vector3.ZERO
	pl.land_blend = 0.0
	pl.land_dry = false
	pl.classic_toy_pose_until_msec = 0
	main.intro_active = true
	var suspended_idle_frames: Dictionary = {}
	var suspended_deadline: int = Time.get_ticks_msec() + 1400
	while Time.get_ticks_msec() < suspended_deadline:
		if String(pl.classic_sprite_sheet) in ["swim_front", "swim_back"]:
			suspended_idle_frames[int(pl.classic_sprite.frame)] = true
		await process_frame
	main.intro_active = false
	if suspended_idle_frames.size() < 3:
		print("FAIL: suspended gameplay froze Roshan's idle loop: ",
			suspended_idle_frames)
	# A dry-land stop is a four-frame seated idle rather than a static view.
	pl.land_blend = 1.0
	pl.land_dry = true
	pl.land_rest = true
	pl.hop_amp = 0.0
	for phase in range(int(pl.ROSHAN_25D_KEYFRAMES)):
		pl.swim_phase = (float(phase) + 0.01) \
			/ float(pl.ROSHAN_25D_KEYFRAMES) * TAU
		pl._tick_classic_sprite(0.0)
		var expected_seated_frame: int = 8 + phase
		if String(pl.classic_sprite_sheet) != "play_b" \
			or int(pl.classic_sprite.frame) != expected_seated_frame:
			print("FAIL: land idle phase ", phase, " selected ",
				pl.classic_sprite_sheet, " frame ", pl.classic_sprite.frame)
	# Cutaway avatars use an independent component so their idle continues even
	# when their host mode returns early (win screens, countdowns, and exits).
	var cutaway_sprite := Sprite3D.new()
	root.add_child(cutaway_sprite)
	var cutaway_loop := ROSHAN_SPRITE_LOOP.new()
	cutaway_sprite.add_child(cutaway_loop)
	cutaway_loop.setup_sprite_3d(cutaway_sprite)
	var cutaway_frames: Dictionary = {}
	var cutaway_deadline: int = Time.get_ticks_msec() + 1100
	while Time.get_ticks_msec() < cutaway_deadline:
		cutaway_frames[int(cutaway_sprite.frame)] = true
		await process_frame
	if cutaway_frames.size() < 3:
		print("FAIL: cutaway Roshan loop froze: ", cutaway_frames)
	cutaway_sprite.queue_free()
	# Force each chronological phase through both runtime swim-view branches.
	pl.verb = ""
	pl.land_blend = 0.0
	pl.land_dry = false
	pl.land_rest = false
	pl.classic_toy_pose_until_msec = 0
	var swim_views: Dictionary = {"swim_front": 20.0, "swim_back": -20.0}
	for swim_key in swim_views:
		var swim_sheet := String(swim_key)
		pl.cam.global_position = pl.global_position + Vector3(0, 5, float(swim_views[swim_sheet]))
		for phase in range(16):
			pl.swim_phase = (float(phase) + 0.01) / 16.0 * TAU
			pl._tick_classic_sprite(5.0)
			if String(pl.classic_sprite_sheet) != swim_sheet \
				or int(pl.classic_sprite.frame) != phase:
				print("FAIL: ", swim_sheet, " phase ", phase,
					" selected ", pl.classic_sprite_sheet, " frame ", pl.classic_sprite.frame)
	var play_samples: Dictionary = {
		"swing": ["swing", 0.625, 2],
		"climb": ["climb", 0.5, 2],
		"ride": ["ride", 1.0, 3],
		"land": ["land", 0.5, 2],
		"dig_l": ["dig", PI * 0.5, 2],
		"dig_r": ["dig", -PI * 0.5, 2],
		"seat": ["seat", 0.2, 2],
	}
	for pose_key in play_samples:
		var pose_name := String(pose_key)
		var pose_spec: Array = play_samples[pose_name]
		pl.toy_pose(String(pose_spec[0]), 1.0, float(pose_spec[1]))
		var play_sequence: Array = pl.ROSHAN_25D_PLAY[pose_name]
		var play_sheet := String(play_sequence[0])
		var play_frame: int = int(play_sequence[1]) * int(pl.ROSHAN_25D_KEYFRAMES) \
			+ int(pose_spec[2])
		if String(pl.classic_sprite_sheet) != play_sheet \
			or int(pl.classic_sprite.frame) != play_frame:
			print("FAIL: playground pose ", pose_name, " did not select ",
				play_sheet, " frame ", play_frame)
	for swing_phase in range(int(pl.ROSHAN_25D_KEYFRAMES)):
		var swing_u: float = (float(swing_phase) + 0.1) \
			/ float(pl.ROSHAN_25D_KEYFRAMES)
		# Deliberately vary t independently: the phase input from the swing,
		# not a second character clock, must be the only frame selector.
		pl.toy_pose("swing", 50.0 + float(swing_phase) * 7.0, swing_u)
		var expected_swing_frame: int = swing_phase
		if String(pl.classic_sprite_sheet) != "play_a" \
			or int(pl.classic_sprite.frame) != expected_swing_frame:
			print("FAIL: swing phase ", swing_phase,
				" drifted from its seat phase to ", pl.classic_sprite_sheet,
				" frame ", pl.classic_sprite.frame)
	print("Roshan sprite animation probe complete")
	quit()
