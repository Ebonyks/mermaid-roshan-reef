extends "res://tools/capture_day_one_pool_candidate_actions.gd"
## Separate reversible fixture:512px source normalization and explicit caller-intended depth.

func _bind_candidates() -> void:
	var main: ReefMain = root.get_node_or_null("Main") as ReefMain
	assert(main != null)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var pool: DayOnePoolCleanup = rooms.day_one_pool_cleanup
	assert(pool != null and pool.skimmer_activity != null)
	var items: Array = (JSON.parse_string(FileAccess.get_file_as_string(
		CANDIDATE_ROOT + "normalized512/PROVENANCE.json")) as Dictionary)["items"]
	assert(items.size() == 5)
	for item: Variant in items:
		var record: Dictionary = item as Dictionary
		var source_path: String = str(record["output_path"])
		var expected: String = str(record["output_sha256"])
		assert(FileAccess.get_sha256(source_path) == expected)
		var image: Image = Image.load_from_file(source_path)
		assert(image.get_size() == Vector2i(512, 512))
		var texture: ImageTexture = ImageTexture.create_from_image(image)
		texture.set_meta("audit_source_path", source_path)
		texture.set_meta("audit_source_sha256", expected)
		var slot: int = int(SLOT_BY_NAME[str(record["name"])])
		var sprite: Sprite2D = pool.skimmer_activity._trash_sprites[slot]
		sprite.texture = texture
		pool.skimmer_activity._fit_sprite(sprite, PoolSkimmerActivity.TRASH_MAX_SIZES[slot])
		candidate_bindings.append({"slot": slot, "source": source_path, "sha256": expected,
			"native_source_sha256": record["source_sha256"], "dimensions": [512, 512],
			"scale": [sprite.scale.x, sprite.scale.y], "rotation": sprite.rotation,
			"modulate": [sprite.modulate.r, sprite.modulate.g, sprite.modulate.b, sprite.modulate.a]})
	pool.skimmer_activity.z_index = 210
	pool.skimmer_activity._trash_base_positions[1] = Vector2(575.0, 330.0)
	pool.skimmer_activity._trash_sprites[1].position = Vector2(575.0, 330.0)
	candidate_bound = true

func _capture(name: String) -> void:
	await super._capture(name)
	var receipt_path: String = capture_root.path_join(name + ".json")
	var receipt: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(receipt_path)) as Dictionary
	receipt["harness"] = "res://tools/capture_day_one_pool_normalized_layout_fit.gd"
	receipt["harness_sha256"] = FileAccess.get_sha256(str(receipt["harness"]))
	receipt["candidate_binding_lane"] = "Disposable512px normalized source/layout fixture. Skimmer depth210 restored after setup; can base575,330; all other base points/tints/rotations/logical extents, original leaf and real progress/control behavior retained. Production files unchanged."
	receipt["qualification"] = str(receipt["qualification"]).replace(
		"native1254px desktop fixture inputs", "whole-canvas normalized512px fixture inputs")
	receipt["layout_profile_sha256"] = FileAccess.get_sha256(CANDIDATE_ROOT + "NORMALIZED_LAYOUT_PROFILE.json")
	var file: FileAccess = FileAccess.open(receipt_path, FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
