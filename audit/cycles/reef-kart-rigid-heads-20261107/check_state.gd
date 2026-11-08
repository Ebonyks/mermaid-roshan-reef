extends SceneTree

const ART := preload("res://scripts/racer/reef_kart_rider_art.gd")

func _initialize() -> void:
	var failures := 0
	for driver: String in ART.SLOTS.keys() + ["roshan"]:
		var sheet := ART.motion_atlas(driver)
		if sheet == null or sheet.get_size() != Vector2(1000, 1000) or sheet.get_image().get_mipmap_count() != 9:
			failures += 1
	var kart := {"motion_sheet": true, "rider_pose": Vector2.ZERO,
		"steer_vis": -1.0, "boost_t": 0.0, "spin_t": 0.0}
	var sequence: Array[int] = [0]
	for phase in [Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1), Vector2(0, 0)]:
		kart["steer_vis"] = phase.x
		kart["boost_t"] = phase.y
		for step in range(12):
			ART.advance_motion(kart, 1.0 / 60.0, true)
			var frame := ART.motion_frame(kart["rider_pose"])
			if sequence.back() != frame:
				sequence.append(frame)
	print("POSE_STATE|", sequence, "|failures=", failures)
	if sequence != [0, 1, 2, 1, 0, 3, 4, 3, 0, 5, 6, 5, 0]:
		failures += 1
	quit(failures)
