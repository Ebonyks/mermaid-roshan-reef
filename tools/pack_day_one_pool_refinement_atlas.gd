extends SceneTree
## Whole-canvas runtime packing only. Originals and accepted sources are unchanged.

const FOLDER: String = "res://assets/castle/day_one_pool/activities/refinement_v2"
const REVIEW: String = "res://audit/day_one_pool_live_refinement_v2_20261001"
const SOURCES: Array[String] = ["star-wrapper", "metal-can", "blue-cap", "", "purple-ribbon", "yellow-sponge"]

func _initialize() -> void:
	call_deferred("_pack")

func _pack() -> void:
	assert(DirAccess.make_dir_recursive_absolute(FOLDER) == OK)
	assert(not FileAccess.file_exists(FOLDER.path_join("floating_trash_atlas.png")))
	assert(not FileAccess.file_exists(FOLDER.path_join("pool_skimmer.png")))
	var original: String = "res://assets/castle/day_one_pool/activities/floating_trash_atlas.png"
	var original_hash: String = FileAccess.get_sha256(original)
	var old: Image = Image.load_from_file(original)
	var atlas: Image = Image.create(1024, 1024, false, Image.FORMAT_RGBA8)
	atlas.fill(Color.TRANSPARENT)
	var rows: Array[Dictionary] = []
	for index: int in range(6):
		var origin: Vector2i = Vector2i((index % 3) * 341, (index / 3) * 341)
		if index == 0:
			origin.x = 12
		elif index == 1:
			origin.x = 352
		var source: String = original if index == 3 else "res://assets_src/imagegen/day1_pool_trash_v2_20261001/normalized512/" + SOURCES[index] + ".png"
		var source_hash: String = FileAccess.get_sha256(source)
		var image: Image
		if index == 3:
			image = old.get_region(Rect2i(0, 341, 341, 341))
		else:
			image = Image.load_from_file(source)
			assert(image.get_size() == Vector2i(512, 512))
			image.resize(341, 341, Image.INTERPOLATE_LANCZOS)
		atlas.blit_rect(image, Rect2i(Vector2i.ZERO, image.get_size()), origin)
		assert(FileAccess.get_sha256(source) == source_hash)
		rows.append({"slot": index, "source": source, "source_sha256": source_hash,
			"output_region": [origin.x, origin.y, 341, 341],
			"method": "Original341x341 leaf source window copied unchanged" if index == 3 else "Complete512x512 canvas uniformly resized to341x341 then packed; no subject repair"})
	var atlas_path: String = FOLDER.path_join("floating_trash_atlas.png")
	assert(atlas.save_png(atlas_path) == OK)
	assert(FileAccess.get_sha256(original) == original_hash)
	var net_source: String = "res://assets_src/imagegen/day1_pool_skimmer_v2_20261001/normalized1024/pool-skimmer.png"
	var net_hash: String = FileAccess.get_sha256(net_source)
	var net: Image = Image.load_from_file(net_source)
	assert(net.get_size() == Vector2i(1024, 683))
	var padded: Image = Image.create(1024, 1024, false, Image.FORMAT_RGBA8)
	padded.fill(Color.TRANSPARENT)
	padded.blit_rect(net, Rect2i(0, 0, 1024, 683), Vector2i.ZERO)
	var net_path: String = FOLDER.path_join("pool_skimmer.png")
	assert(padded.save_png(net_path) == OK)
	assert(FileAccess.get_sha256(net_source) == net_hash)
	var provenance: Dictionary = {"schema": "reef.pool-runtime-packing.v1", "engine": Engine.get_version_info(),
		"atlas": {"path": atlas_path, "sha256": FileAccess.get_sha256(atlas_path), "dimensions": [1024, 1024], "slots": rows},
		"skimmer": {"source": net_source, "source_sha256": net_hash, "path": net_path,
			"sha256": FileAccess.get_sha256(net_path), "dimensions": [1024, 1024],
			"method": "Complete1024x683 canvas copied at0,0 into transparent1024POT canvas; source pixels unchanged",
			"fit": "205x205 logical card preserves205px painted width; pixel sockets unchanged by padding"},
		"original_atlas_sha256": original_hash, "owner_accepted": false,
		"qualification": "Technical packing only; original approved leaf and complete selected source pixels preserved. No new generated subject, source edit, mounted/action/device acceptance."}
	var file: FileAccess = FileAccess.open(REVIEW.path_join("PACKING_PROVENANCE.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(provenance, "\t") + "\n")
	file.close()
	print("POOL_RUNTIME_PACKING|PASS|two1024POT textures|original source hashes preserved")
	quit()
