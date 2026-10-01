extends "res://tools/capture_day_one_pool_art_inventory.gd"
## Disposable test-instance texture substitutions only; no production resource writes.
const CANDIDATE_ROOT := "res://assets_src/imagegen/day1_pool_trash_v2_20261001/"
const SLOT_BY_NAME := {"star-wrapper": 0, "metal-can": 1, "blue-cap": 2,
	"purple-ribbon": 4, "yellow-sponge": 5}
var candidate_bound: bool = false
var candidate_bindings: Array[Dictionary] = []

func _bind_candidates() -> void:
	var main: ReefMain = root.get_node_or_null("Main") as ReefMain
	assert(main != null)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var pool: DayOnePoolCleanup = rooms.day_one_pool_cleanup
	assert(pool != null and pool.skimmer_activity != null)
	var records: Array = JSON.parse_string(FileAccess.get_file_as_string(
		CANDIDATE_ROOT + "RETAINED_ATTEMPTS_01.json")) as Array
	assert(records.size() == 5)
	for item: Variant in records:
		var record: Dictionary = item as Dictionary
		var source_path: String = "res://" + str(record["planned_native_path"])
		var source_hash: String = str(record["sha256"])
		assert(FileAccess.get_sha256(source_path) == source_hash)
		var texture: ImageTexture = ImageTexture.create_from_image(Image.load_from_file(source_path))
		texture.set_meta("audit_source_path", source_path)
		texture.set_meta("audit_source_sha256", source_hash)
		var slot: int = int(SLOT_BY_NAME[str(record["name"])])
		var sprite: Sprite2D = pool.skimmer_activity._trash_sprites[slot]
		sprite.texture = texture
		pool.skimmer_activity._fit_sprite(sprite, PoolSkimmerActivity.TRASH_MAX_SIZES[slot])
		candidate_bindings.append({"slot": slot, "source": source_path, "sha256": source_hash,
			"scale": [sprite.scale.x, sprite.scale.y], "rotation": sprite.rotation,
			"modulate": [sprite.modulate.r, sprite.modulate.g, sprite.modulate.b, sprite.modulate.a]})
	candidate_bound = true

func _capture(name: String) -> void:
	if not candidate_bound:
		_bind_candidates()
	await super._capture(name)
	var receipt_path: String = capture_root.path_join(name + ".json")
	var receipt: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(receipt_path)) as Dictionary
	receipt["fixture_parent_harness"] = "res://tools/capture_day_one_pool_art_inventory.gd"
	receipt["fixture_parent_harness_sha256"] = FileAccess.get_sha256(str(receipt["fixture_parent_harness"]))
	receipt["harness"] = "res://tools/capture_day_one_pool_candidate_fit.gd"
	receipt["harness_sha256"] = FileAccess.get_sha256(str(receipt["harness"]))
	receipt["candidate_binding_lane"] = "Five texture replacements on a disposable native test instance; original production files/bindings unchanged. Same positions, rotations, tints, logical max sizes and progress controller. The original leaf is retained."
	receipt["candidate_bindings"] = candidate_bindings
	receipt["qualification"] = str(receipt["qualification"]) + " Candidate source textures are native1254px desktop fixture inputs, not approved runtime-resolution or device assets."
	var receipt_file: FileAccess = FileAccess.open(receipt_path, FileAccess.WRITE)
	receipt_file.store_string(JSON.stringify(receipt, "\t") + "\n")
	receipt_file.close()
