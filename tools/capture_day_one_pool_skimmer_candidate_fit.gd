extends "res://tools/capture_day_one_pool_normalized_layout_fit.gd"
## Fresh skimmer on the disposable normalized-prop layout; original controller retained.

func _bind_candidates() -> void:
	super._bind_candidates()
	var main: ReefMain = root.get_node_or_null("Main") as ReefMain
	var activity: PoolSkimmerActivity = main._castle_rooms_ref().day_one_pool_cleanup.skimmer_activity
	var source: String = "res://assets_src/imagegen/day1_pool_skimmer_v2_20261001/normalized1024/pool-skimmer.png"
	var provenance: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(source.get_base_dir().path_join("PROVENANCE.json"))) as Dictionary
	assert(FileAccess.get_sha256(source) == str(provenance["output_sha256"]))
	var image: Image = Image.load_from_file(source)
	assert(image.get_size() == Vector2i(1024, 683))
	var texture: ImageTexture = ImageTexture.create_from_image(image)
	texture.set_meta("audit_source_path", source)
	texture.set_meta("audit_source_sha256", provenance["output_sha256"])
	activity._skimmer.texture = texture
	activity._fit_sprite(activity._skimmer, PoolSkimmerActivity.SKIMMER_MAX_SIZE)
	activity._skimmer.position = activity._hand_offset - (PoolSkimmerActivity.HANDLE_PIXEL - texture.get_size() * 0.5) * activity._skimmer.scale
	candidate_bindings.append({"role": "fresh_pool_skimmer", "source": source,
		"sha256": provenance["output_sha256"], "dimensions": [1024, 683],
		"native_source_sha256": provenance["source_sha256"],
		"socket_qualification": "Original100,580 grip and780,190 contact points retained for this diagnostic; generated contour/socket fit requires visual measurement, not a copied identity/design acceptance."})

func _capture(name: String) -> void:
	await super._capture(name)
	var path: String = capture_root.path_join(name + ".json")
	var receipt: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path)) as Dictionary
	receipt["harness"] = "res://tools/capture_day_one_pool_skimmer_candidate_fit.gd"
	receipt["harness_sha256"] = FileAccess.get_sha256(str(receipt["harness"]))
	receipt["candidate_bindings"] = candidate_bindings
	receipt["qualification"] = str(receipt["qualification"]) + " New text-only skimmer generation, normalized1024x683, is mounted only in this disposable instance. Original socket coordinates retained for measured comparison; source/static/contact/complete action remain separate."
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
